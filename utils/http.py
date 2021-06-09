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

import http.server
import socketserver

import requests
import socket
import urllib3

from core.cli.badges import Badges

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_request(self, fmt, *args):
        pass

    def do_GET(self):
        self.badges = Badges()

        self.badges.output_success(f"Connection from {self.client_address[0]}!")
        self.badges.output_process("Sending payload stage...")

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes(self.payload, "utf8"))
        self.badges.output_success("Payload sent successfully!")


class HTTPClient:
    def __init__(self):
        self.badges = Badges()

    def start_server(self, host, port, payload, forever=True):
        try:
            self.badges.output_process(f"Starting http server on port {str(port)}...")
            httpd = socketserver.TCPServer((host, int(port)), Handler)

            self.badges.output_process("Serving payload on http server...")
            httpd.RequestHandlerClass.payload = payload

            if forever:
                while True:
                    self.badges.output_process("Listening for connections...")
                    httpd.handle_request()
            else:
                self.badges.output_process("Listening for connections...")
                httpd.handle_request()
        except Exception:
            self.badges.output_error(f"Failed to start http server on port {str(port)}!")

    def http_request(self, method, host, port, path, ssl=False, timeout=10, output=True, session=requests, **kwargs):
        if not output:
            timeout = 0
        kwargs.setdefault("timeout", timeout)
        kwargs.setdefault("verify", False)
        kwargs.setdefault("allow_redirects", True)

        if not ssl:
            ssl = int(port) in [443]
        url = self.normalize_url(host, port, path, ssl)

        try:
            return getattr(session, method.lower())(url, **kwargs)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
            self.badges.output_error("Invalid URL format: {}!".format(url))
        except requests.exceptions.ConnectionError:
            self.badges.output_error("Connection error: {}!".format(url))
        except requests.exceptions.ReadTimeout:
            if not output:
                self.badges.output_warning("Timeout waiting for response.")
        except requests.RequestException as e:
            self.badges.output_error("Request error: {}!".format(str(e)))
        except socket.error:
            self.badges.output_error("Socket is not connected!")

        return None

    @staticmethod
    def normalize_url(host, port, path, ssl=False):
        if ssl:
            url = "https://"
        else:
            url = "http://"

        url += "{}:{}{}".format(host, port, path)

        return url
