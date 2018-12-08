from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from gem.core import Endpoint, Event


class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(b"ok")


class HealthEndpoint(Endpoint):
    """Health endpoint."""

    def __init__(self, host, port):
        """
        Initialize new instance of the HealthEndpoint class.

        Arguments:
            host {str} -- Host.
            port {int} -- Port.
        """
        super().__init__()
        self.__httpd = HTTPServer((host, port), MyHandler)
        self.__thread = Thread(target=self.__thread, args=(self.__httpd,))

    def open(self):
        self.__thread.start()

    def close(self):
        self.__httpd.server_close()

    def emit(self, event, data, to=None):
        pass

    def join(self, sid, room):
        pass

    def leave(self, sid, room):
        pass

    @staticmethod
    def __thread(httpd):
        httpd.serve_forever()
