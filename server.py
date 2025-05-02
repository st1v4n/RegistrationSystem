from http.server import HTTPServer, BaseHTTPRequestHandler

class Server(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            file = open(self.path[1:]).read()
        except:
            file = "File Not Found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file, 'utf-8'))

protocol = HTTPServer(('localhost', 8080), Server)
protocol.serve_forever()