import importlib.util
import json
from pathlib import Path
import threading
import unittest
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

spec = importlib.util.spec_from_file_location('gateway', Path(__file__).parents[1]/'deploy/inference/gateway.py')
gateway = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gateway)


class GatewayTests(unittest.TestCase):
    def test_resource_overrides_cannot_escape_budget(self):
        result = gateway.constrain('/api/chat', {'model': gateway.MODEL,
            'messages': [{'role': 'user', 'content': 'hello'}], 'keep_alive': -1,
            'options': {'num_ctx': 262144, 'num_gpu': 0, 'num_predict': -1,
                        'num_batch': 4096, 'temperature': .2}})
        self.assertEqual(result['options'], {'num_ctx': 8192, 'num_predict': 1024, 'temperature': .2})
        self.assertEqual(result['keep_alive'], '60s')
        self.assertFalse(result['think'])

    def test_wrong_model_and_vision_rejected(self):
        for body in ({'model': 'other', 'messages': []},
                     {'model': gateway.MODEL, 'messages': [{'images': ['base64']}]},
                     {'model': gateway.MODEL, 'messages': []}):
            with self.assertRaises(ValueError):
                gateway.constrain('/api/chat', body)

    def test_output_cap(self):
        result = gateway.constrain('/api/generate', {'model': gateway.MODEL,
            'prompt': 'hello', 'options': {'num_predict': 1000000}})
        self.assertEqual(result['options']['num_predict'], 2048)

    def test_gateway_auth_admin_denial_and_busy(self):
        server = ThreadingHTTPServer(('127.0.0.1', 0), gateway.Handler)
        server.token = 'x' * 48
        server.allowed_peers = {'127.0.0.1'}
        server.upstream = ('127.0.0.1', 1)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        def request(path, token=None, data=None):
            headers = {'Authorization': 'Bearer '+token} if token else {}
            req = urllib.request.Request(f'http://127.0.0.1:{server.server_port}'+path,
                data=json.dumps(data).encode() if data is not None else None, headers=headers)
            try:
                return urllib.request.urlopen(req, timeout=3).status
            except urllib.error.HTTPError as exc:
                return exc.code
        try:
            self.assertEqual(request('/api/tags'), 401)
            self.assertEqual(request('/api/pull', server.token, {'model': gateway.MODEL}), 403)
            self.assertEqual(request('/api/tags', server.token), 503)
            gateway.SLOT.acquire()
            try:
                self.assertEqual(request('/api/chat', server.token, {'model': gateway.MODEL,
                    'messages': [{'role': 'user', 'content': 'hi'}]}), 429)
            finally:
                gateway.SLOT.release()
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == '__main__':
    unittest.main()
