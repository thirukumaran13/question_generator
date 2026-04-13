"""
Simple local web server for the Question Generator app.
Usage:  python server.py          (default port 8080)
        python server.py 5000     (custom port)
"""

import http.server
import socketserver
import webbrowser
import sys
import os

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

# Serve from the directory this script lives in
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler that suppresses per-request log noise."""

    def log_message(self, fmt, *args):
        code = args[1] if len(args) > 1 else ""
        try:
            if int(code) >= 400:
                super().log_message(fmt, *args)
        except (ValueError, TypeError):
            pass


with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:
    url = f"http://localhost:{PORT}"
    print("=" * 54)
    print(f"  Question Generator running at {url}")
    print(f"  Serving files from: {os.getcwd()}")
    print("  Press Ctrl+C to stop.")
    print("=" * 54)
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
