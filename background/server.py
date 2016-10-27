import os
import threading
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer


class ExploitHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)

        mimeType = 'text/html'
        if self.path == '/':
            self.path = '/index.html'
        if self.path == '/favicon.ico':
            return
        if '.mp4' in self.path:
            mimeType = 'video/mp4'

        self.send_header('Content-type', mimeType)
        self.end_headers()

        file_path = os.path.join(os.path.join(os.getcwd(), 'site/'), self.path[1:len(self.path)])
        with open(file_path, 'rb') as html_data:
            self.wfile.write(html_data.read())
        return


class ExploitServer():

    def __init__(self):
        self.listen_port = 8000
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.machine_ip = s.getsockname()[0]
        s.close()
        self.server_address = ('0.0.0.0', self.listen_port)

    def start(self):
        print("Exploit server listening at {}".format(self.get_listen_url()))
        self.server = HTTPServer(self.server_address, ExploitHandler)
        self.listenThread = threading.Thread(target=self.server.serve_forever)
        self.listenThread.daemon = True
        self.listenThread.start()

    def stop(self):
        print("Stopping exploit server")
        self.server.shutdown()
        self.server.socket.close()

    def get_listen_url(self):
        return "http://{}:{}".format(self.machine_ip, self.listen_port)

    def handle_message(self, message):
        getattr(self, message)()

    def background(self):
        nothing = True
