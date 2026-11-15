import unittest
import threading
import time
import http.client
import json
from app import run, PalindromeHandler, PORT
import http.server


class AppWebServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.HTTPServer(("", PORT), PalindromeHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.1)  # give server a moment to start

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join(timeout=1)

    def test_get_index(self):
        conn = http.client.HTTPConnection("localhost", PORT)
        conn.request("GET", "/")
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertIn("text/html", response.getheader("Content-Type"))
        body = response.read().decode("utf-8")
        self.assertIn("Palindrome Checker", body)
        self.assertIn("palindromeForm", body)
        conn.close()

    def test_post_check_palindrome_true_string(self):
        conn = http.client.HTTPConnection("localhost", PORT)
        headers = {"Content-Type": "application/json"}
        conn.request("POST", "/api/check", body=json.dumps({"value": "racecar"}), headers=headers)
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        data = json.loads(response.read().decode("utf-8"))
        self.assertEqual(data, {"result": True})
        conn.close()

    def test_post_check_palindrome_false_string(self):
        conn = http.client.HTTPConnection("localhost", PORT)
        headers = {"Content-Type": "application/json"}
        conn.request("POST", "/api/check", body=json.dumps({"value": "hello"}), headers=headers)
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        data = json.loads(response.read().decode("utf-8"))
        self.assertEqual(data, {"result": False})
        conn.close()

    def test_post_check_palindrome_number(self):
        conn = http.client.HTTPConnection("localhost", PORT)
        headers = {"Content-Type": "application/json"}
        conn.request("POST", "/api/check", body=json.dumps({"value": "121"}), headers=headers)
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        data = json.loads(response.read().decode("utf-8"))
        self.assertEqual(data, {"result": True})
        conn.close()

    def test_post_check_invalid_type(self):
        conn = http.client.HTTPConnection("localhost", PORT)
        headers = {"Content-Type": "application/json"}
        # Sending a list or object that is not handled or invalid
        conn.request("POST", "/api/check", body=json.dumps({"value": [1, 2, 1]}), headers=headers)
        response = conn.getresponse()
        self.assertEqual(response.status, 400)
        data = json.loads(response.read().decode("utf-8"))
        self.assertIn("error", data)
        conn.close()

    def test_404(self):
        conn = http.client.HTTPConnection("localhost", PORT)
        conn.request("GET", "/nonexistent")
        response = conn.getresponse()
        self.assertEqual(response.status, 404)
        conn.close()


if __name__ == "__main__":
    unittest.main()
