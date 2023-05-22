from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from link_service import LinkService

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        status, this_link = LinkService().get(self.path[1:])

        if status == 200:
            self.send_response(status)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(f'<head><link rel="icon" href="data:;base64,="><meta http-equiv="refresh" content="0;URL=\'{this_link}\' " '
                         f'/></head>'.encode())
        else:
            self.send_response(status)

    def do_POST(self):
        status, this_hash = LinkService().push(parse_qs(urlparse(self.path).query).get('source')[0])

        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(f'http://localhost:8000/{this_hash}', "utf-8"))


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
print("start server")
httpd.serve_forever()
httpd.server_close()
