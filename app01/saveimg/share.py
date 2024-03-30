# 熏小漏 2024/3/29 21:56
import http.server
import socketserver

PORT = 8002

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
