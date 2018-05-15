from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        try:
            print(self.path)
            len_of_response = int(self.path[1:])
            print(len_of_response)
            response = 'o' * len_of_response
            print('response = ', response)
            self.wfile.write("<html><body><h1>{}</h1></body></html>".format(response))
        except Exception:
            self.wfile.write("<html><body><h1>HEADER</h1></body></html>")

def run(server_class=HTTPServer, handler_class=Server, port=9191):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()

