from http.server import HTTPServer, CGIHTTPRequestHandler

server_address = ("", 8000)


handler_class = CGIHTTPRequestHandler #1 ハンドラを設定
httpd = HTTPServer(server_address, handler_class)
httpd.serve_forever()
