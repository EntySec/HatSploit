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

from core.badges import badges
from core.exceptions import exceptions

from data.modules.auxiliary.multi.listener.tcp.core.server import server
from data.modules.auxiliary.multi.listener.tcp.core.controller import controller

class listener:
    def __init__(self):
        self.badges = badges()
        self.exceptions = exceptions()
        self.server = server()
        
        self.controller = None

    def start_listener(self, local_host, local_port):
        try:
            server = self.server.start_server(local_host, local_port)
            self.badges.output_success("Listener started on port " + local_port + "!")
            return server
        except Exception:
            self.badges.output_error("Failed to start listener!")
            raise self.exceptions.GlobalException

    def listen(self, local_host, local_port, server):
        try:
            client, address = server.accept()
            self.badges.output_process("Connecting to " + address[0] + "...")
            self.badges.output_process("Establishing connection...")
            client, address = server.accept()
            self.controller = controller(client)
            return (self.controller, address[0])
        except Exception:
            self.badges.output_error("Failed to listen!")
            raise self.exceptions.GlobalException
