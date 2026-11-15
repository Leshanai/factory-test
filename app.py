"""A simple web server providing a frontend to check palindromes using is_palindrome."""

import http.server
import json
import socketserver
import urllib.parse
from palindrome import is_palindrome

PORT = 8000

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Palindrome Checker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f4f4f9;
            color: #333;
        }
        h1 {
            color: #2c3e50;
        }
        .card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        input[type="text"] {
            width: 70%;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 4px;
            margin-right: 10px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #2980b9;
        }
        #result {
            margin-top: 20px;
            font-size: 18px;
            font-weight: bold;
        }
        .true { color: #27ae60; }
        .false { color: #c0392b; }
        .error { color: #e67e22; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Palindrome Checker</h1>
        <p>Enter a word, phrase, or non-negative number to check if it's a palindrome:</p>
        <form id="palindromeForm">
            <input type="text" id="valueInput" placeholder="e.g. racecar or 121" required>
            <button type="submit">Check</button>
        </form>
        <div id="result"></div>
    </div>

    <script>
        document.getElementById('palindromeForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const val = document.getElementById('valueInput').value;
            const resultDiv = document.getElementById('result');
            resultDiv.textContent = 'Checking...';
            resultDiv.className = '';

            try {
                const response = await fetch('/api/check', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ value: val })
                });
                const data = await response.json();

                if (response.ok) {
                    if (data.result === true) {
                        resultDiv.textContent = 'Result: True (Palindrome!)';
                        resultDiv.className = 'true';
                    } else {
                        resultDiv.textContent = 'Result: False (Not a palindrome)';
                        resultDiv.className = 'false';
                    }
                } else {
                    resultDiv.textContent = 'Error: ' + (data.error || 'Invalid input');
                    resultDiv.className = 'error';
                }
            } catch (err) {
                resultDiv.textContent = 'Error communicating with server.';
                resultDiv.className = 'error';
            }
        });
    </script>
</body>
</html>
"""


class PalindromeHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        if self.path == "/api/check":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode("utf-8"))
                val = data.get("value", "")

                # Try to parse as int if it looks like an integer (and not empty)
                parsed_val = val
                if isinstance(val, str) and val.strip():
                    # Check if it's a valid integer representation (like "121", "-121", "0", etc.)
                    # Note: is_palindrome handles ints. If someone enters "121", let's pass int or str.
                    # Wait, is_palindrome treats ints and strs differently (e.g. negative ints return False,
                    # whereas negative strings might strip non-alphanumeric. Wait, let's check how user inputs from form arrive:
                    # Form input is always a string. Should we parse numeric strings as int or keep as string or try int?
                    # Let's check: if someone enters "121", is it better as int or str? Both return True for 121 and "121".
                    # But what about "-121"? As int -> False. As str "-121" -> cleaned text "121" -> True!
                    # Wait, test_palindrome tests int(-121) -> False. If user types "-121" in input box, should it be int or str?
                    # If we parse digits as int if possible:
                    try:
                        # If it's a pure integer string like "121" or "-121"
                        if val.strip() and all(c.isdigit() or (c == '-' and val.index(c) == 0) for c in val.strip()):
                            parsed_val = int(val.strip())
                    except ValueError:
                        pass

                result = is_palindrome(parsed_val)
                response_data = {"result": result}
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode("utf-8"))
            except (json.JSONDecodeError, TypeError, ValueError) as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def log_message(self, format, *args):
        # Silence default server logs during tests, or keep minimal if desired.
        pass


def run(server_class=http.server.HTTPServer, handler_class=PalindromeHandler, port=PORT):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting web server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
