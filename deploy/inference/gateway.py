#!/usr/bin/env python3
"""Private, token-authenticated Ollama pilot gateway; no model administration."""
import hmac
import http.client
import json
import os
from pathlib import Path
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MODEL = os.getenv('INFERENCE_MODEL', 'qwen3.5:9b-q4_K_M')
MAX_BODY = 128 * 1024
SLOT = threading.BoundedSemaphore(1)
SAFE_OPTIONS = {'temperature', 'top_p', 'top_k', 'min_p', 'repeat_penalty', 'seed', 'stop'}


def constrain(path, body):
    if not isinstance(body, dict) or body.get('model') != MODEL:
        raise ValueError('Only the configured local model is allowed')
    if path == '/api/show':
        return {'model': MODEL}
    if path not in ('/api/chat', '/api/generate'):
        raise ValueError('Unsupported operation')
    options = body.get('options') or {}
    if not isinstance(options, dict):
        raise ValueError('Invalid options')
    limited = {k: v for k, v in options.items() if k in SAFE_OPTIONS}
    requested = options.get('num_predict', 1024)
    if not isinstance(requested, int) or isinstance(requested, bool) or requested < 1:
        requested = 1024
    limited.update(num_ctx=8192, num_predict=min(requested, 2048))
    result = {'model': MODEL, 'options': limited, 'keep_alive': '60s',
              'stream': body.get('stream', True), 'think': body.get('think', False)}
    if not isinstance(result['stream'], bool) or not isinstance(result['think'], bool):
        raise ValueError('stream and think must be booleans')
    if path == '/api/chat':
        messages = body.get('messages')
        if not isinstance(messages, list) or not 1 <= len(messages) <= 128:
            raise ValueError('Expected 1–128 text messages')
        for message in messages:
            if not isinstance(message, dict) or message.get('images'):
                raise ValueError('This pilot accepts text messages only')
        result['messages'] = messages
        if 'tools' in body:
            result['tools'] = body['tools']
    else:
        if body.get('images') or not isinstance(body.get('prompt'), str):
            raise ValueError('This pilot accepts text prompts only')
        result['prompt'] = body['prompt']
        if 'system' in body:
            result['system'] = body['system']
    if 'format' in body:
        result['format'] = body['format']
    return result


class Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'

    def setup(self):
        super().setup()
        self.connection.settimeout(15)

    def log_message(self, fmt, *args):
        # Do not log headers, tokens, prompts or model output.
        pass

    def reply(self, status, error):
        data = json.dumps({'error': error}).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self.proxy()

    def do_POST(self):
        self.proxy()

    def proxy(self):
        if self.client_address[0] not in self.server.allowed_peers:
            self.reply(403, 'Source not permitted')
            return
        supplied = self.headers.get('Authorization', '')
        if not hmac.compare_digest(supplied, 'Bearer ' + self.server.token):
            self.reply(401, 'Authentication required')
            return
        allowed = {'GET': {'/api/tags', '/api/version', '/api/ps'},
                   'POST': {'/api/show', '/api/chat', '/api/generate'}}
        if self.path not in allowed.get(self.command, set()):
            self.reply(403, 'Operation not permitted')
            return
        data = None
        if self.command == 'POST':
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= MAX_BODY or self.headers.get('Transfer-Encoding'):
                    raise ValueError('Invalid request size')
                data = json.dumps(constrain(self.path, json.loads(self.rfile.read(size)))).encode()
            except (ValueError, TypeError):
                self.reply(400, 'Invalid model or request; text-only bounded pilot')
                return
        generation = self.path in ('/api/chat', '/api/generate')
        if generation and not SLOT.acquire(blocking=False):
            self.reply(429, 'Inference is busy; retry after this request finishes')
            return
        conn = http.client.HTTPConnection(*self.server.upstream, timeout=600)
        started = False
        try:
            conn.request(self.command, self.path, data, {'Content-Type': 'application/json'})
            response = conn.getresponse()
            self.send_response(response.status)
            self.send_header('Content-Type', response.getheader('Content-Type', 'application/json'))
            self.send_header('Connection', 'close')
            self.end_headers()
            started = True
            while chunk := response.read1(8192):
                self.wfile.write(chunk)
                self.wfile.flush()
        except (OSError, http.client.HTTPException):
            if not started:
                self.reply(503, 'Local inference unavailable; check host admission/guard')
        finally:
            conn.close()
            if generation:
                SLOT.release()


def main():
    server = ThreadingHTTPServer(('0.0.0.0', 11435), Handler)
    server.daemon_threads = True
    server.token = Path(os.environ['INFERENCE_TOKEN_FILE']).read_text().strip()
    if len(server.token) < 32:
        raise ValueError('A strong runtime token is required')
    server.allowed_peers = set(os.environ['INFERENCE_ALLOWED_PEERS'].split(','))
    server.upstream = ('127.0.0.1', 11434)
    server.serve_forever()


if __name__ == '__main__':
    main()
