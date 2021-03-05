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

from core.cli.badges import badges

class handler(http.server.SimpleHTTPRequestHandler):
    def log_request(self, fmt, *args):
        pass
        
    def do_GET(self):
        self.badges = badges()
        
        self.badges.output_success("Connection from " + self.client_address[0] + "!")
        self.badges.output_process("Performing User-Agent capture...")
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        self.wfile.write(bytes("Neo... Where are you?", "utf8"))
        
        if 'User-Agent' in self.headers.keys():
            user_agent = self.headers['User-Agent']
            self.badges.output_information("User-Agent: " + user_agent)
            
            self.badges.output_success("User-Agent capture done!")
        else:
            self.badges.output_error("User-Agent capture failed!")
