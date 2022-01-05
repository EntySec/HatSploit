#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2022 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import http.server
import socket
import socketserver
import time

from hatsploit.core.base.exceptions import Exceptions
from hatsploit.core.cli.badges import Badges


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_request(self, fmt, *args):
        pass

    def do_GET(self):
        self.badges = Badges()

        if self.path == self.payload_path:
            self.badges.print_process(f"Connecting to {self.client_address[0]}...")

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(bytes(self.payload, "utf8"))


class Server:
    badges = Badges()
    exceptions = Exceptions()

    def start_server(self, host, port, payload, forever=False, path='/'):
        try:
            self.badges.print_process(f"Starting HTTP listener on port {str(port)}...")
            httpd = socketserver.TCPServer((host, int(port)), Handler)

            httpd.RequestHandlerClass.payload_path = path
            httpd.RequestHandlerClass.payload = payload

            if forever:
                while True:
                    httpd.handle_request()
            else:
                httpd.handle_request()
            httpd.server_close()
            httpd.shutdown()
        except Exception:
            self.badges.print_error(f"Failed to start HTTP listener on port {str(port)}!")

    def connect(self, remote_host, remote_port, timeout=None):
        try:
            if timeout is not None:
                timeout = time.time() + timeout

                while True:
                    try:
                        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        server.connect((remote_host, int(remote_port)))

                        self.badges.print_process(f"Establishing connection (0.0.0.0:{remote_port} -> {remote_host}:{remote_port})...")
                        break
                    except Exception:
                        if time.time() > timeout:
                            raise socket.timeout
            else:
                while True:
                    try:
                        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        server.connect((remote_host, int(remote_port)))

                        self.badges.print_process(f"Establishing connection (0.0.0.0:{remote_port} -> {remote_host}:{remote_port})...")
                        break
                    except Exception:
                        pass
        except socket.timeout:
            self.badges.print_warning("Connection timeout.")
            raise self.exceptions.GlobalException
        except Exception:
            self.badges.print_error(f"Failed to connect to {remote_host}!")
            raise self.exceptions.GlobalException
        return server

    def listen(self, local_host, local_port, timeout=None):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.settimeout(timeout)
            server.bind((local_host, int(local_port)))
            server.listen(1)

            self.badges.print_process(f"Starting TCP listener on port {str(local_port)}...")
            client, address = server.accept()
            self.badges.print_process(f"Establishing connection ({address[0]}:{address[1]} -> {local_host}:{local_port})...")

            server.close()
        except socket.timeout:
            self.badges.print_warning("Timeout waiting for connection.")

            server.close()
            raise self.exceptions.GlobalException
        except Exception:
            self.badges.print_error(f"Failed to start TCP listener on port {str(port)}!")
            raise self.exceptions.GlobalException
        return client, address[0]
