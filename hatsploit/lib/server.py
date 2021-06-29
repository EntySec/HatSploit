#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
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

import socket

import http.server
import socketserver

from hatsploit.core.cli.badges import Badges
from hatsploit.core.base.exceptions import Exceptions


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_request(self, fmt, *args):
        pass

    def do_GET(self):
        self.badges = Badges()

        if self.path == self.payload_path:
            self.badges.output_success(f"Connection from {self.client_address[0]}!")
            self.badges.output_process("Sending payload stage...")

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(bytes(self.payload, "utf8"))
            self.badges.output_success("Payload sent successfully!")


class Server:
    def __init__(self):
        self.badges = Badges()
        self.exceptions = Exceptions()

    def start_server(self, host, port, payload, forever=True, path='/'):
        try:
            self.badges.output_process(f"Starting http server on port {str(port)}...")
            httpd = socketserver.TCPServer((host, int(port)), Handler)

            self.badges.output_process("Serving payload on http server...")
            httpd.RequestHandlerClass.payload_path = path
            httpd.RequestHandlerClass.payload = payload

            if forever:
                while True:
                    self.badges.output_process("Listening for connections...")
                    httpd.handle_request()
            else:
                self.badges.output_process("Listening for connections...")
                httpd.handle_request()
            httpd.server_close()
        except Exception:
            self.badges.output_error(f"Failed to start http server on port {str(port)}!")

    def connect(self, remote_host, remote_port, timeout=None):
        address = remote_host + ':' + str(remote_port)
        self.badges.output_process("Connecting to " + address + "...")
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.settimeout(timeout)

            server.connect((remote_host, int(remote_port)))
            self.badges.output_process("Establishing connection...")
        except socket.timeout:
            self.badges.output_warning("Connection timeout.")
            raise self.exceptions.GlobalException
        except Exception:
            self.badges.output_error("Failed to connect to " + address + "!")
            raise self.exceptions.GlobalException
        return server

    def listen(self, local_host, local_port, timeout=None):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.settimeout(timeout)
            server.bind((local_host, int(local_port)))
            server.listen(1)

            self.badges.output_process("Listening on port " + str(local_port) + "...")
            client, address = server.accept()
            self.badges.output_process("Connecting to " + address[0] + "...")
            self.badges.output_process("Establishing connection...")

            server.close()
        except socket.timeout:
            self.badges.output_warning("Timeout waiting for connection.")

            server.close()
            raise self.exceptions.GlobalException
        except Exception:
            self.badges.output_error("Failed to listen on port " + str(local_port) + "!")
            raise self.exceptions.GlobalException
        return client, address[0]
