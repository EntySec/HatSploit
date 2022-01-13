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

import requests
import socket
import urllib3

from hatsploit.lib.server import Server
from hatsploit.core.cli.badges import Badges

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HTTPClient:
    server = Server()
    badges = Badges()

    def http_server(self, host, port, data, forever=False, path='/'):
        self.server.start_server(host, port, data, forever, path)

    def http_request(self, method, host, port, path='/', ssl=False, timeout=10, output=True, session=requests,
                     **kwargs):
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
            self.badges.print_error("Invalid URL format: {}!".format(url))
        except requests.exceptions.ConnectionError:
            self.badges.print_error("Connection error: {}!".format(url))
        except requests.exceptions.ReadTimeout:
            if not output:
                self.badges.print_warning("Timeout waiting for response.")
        except requests.RequestException as e:
            self.badges.print_error("Request error: {}!".format(str(e)))
        except socket.error:
            self.badges.print_error("Socket is not connected!")

        return None

    @staticmethod
    def normalize_url(host, port, path, ssl=False):
        if ssl:
            url = "https://"
        else:
            url = "http://"

        url += "{}:{}{}".format(host, port, path)

        return url
