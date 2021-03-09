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

import re
import sys
import time
import socket
import telnetlib
import selectors

from core.cli.badges import badges
from core.base.exceptions import exceptions

class tcp_tools:
    def __init__(self):
        self.badges = badges()
        self.exceptions = exceptions()
        
        self.client = None
    
    #
    # Functions to manipulate local addresses
    #

    def get_local_host(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server.connect(("192.168.1.1", 80))
            local_host = server.getsockname()[0]
            server.close()
            local_host = local_host
        except Exception:
            local_host = "127.0.0.1"
        return local_host

    #
    # TCP requests
    #
    
    def tcp_request(self, host, port, data, buffer_size=1024, timeout=10):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, int(port)))
        sock.send(data.encode())
        output = sock.recv(buffer_size)
        sock.close()
        return output.decode().strip()
    
    #
    # TCP ports
    #
    
    def check_tcp_port(self, host, port, timeout=10):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        if sock.connect_ex((host, int(port))) == 0:
            sock.close()
            return True
        sock.close()
        return False
    
    #
    # Functions to connect or disconnect
    #
        
    def connect(self, client):
        self.client = telnetlib.Telnet()
        self.client.sock = client
        
    def disconnect(self):
        self.client.close()
        
    #
    # Functions to send and recv from client and to client
    #
    
    def send(self, buffer):
        if self.client:
            self.client.write(buffer)
            
    def interactive(self):
        if self.client:
            selector = selectors.SelectSelector()

            selector.register(self.client, selectors.EVENT_READ)
            selector.register(sys.stdin, selectors.EVENT_READ)
            
            while True:
                for key, events in selector.select():
                    if key.fileobj is self.client:
                        try:
                            response = self.client.read_eager()
                        except Exception:
                            self.badges.output_warning("Connection terminated.")
                            return
                        if response:
                            self.badges.output_empty(response.decode())
                    elif key.fileobj is sys.stdin:
                        line = sys.stdin.readline()
                        if not line:
                            pass
                        if line == "exit\n":
                            return
                        self.client.write(line.encode())

    def recv(self, timeout=10):
        if self.client:
            result = b""
            if timeout is not None:
                timeout = time.time() + timeout
                while True:
                    data = self.client.read_very_eager()
                    result += data
                    if data:
                        break
                    if time.time() > timeout:
                        self.badges.output_warning("Timeout waiting for response.")
                        break
            else:
                while True:
                    data = self.client.read_very_eager()
                    result += data
                    if data:
                        break
            return result
        return None
        
    #
    # Functions to send system commands to client
    #

    def send_command(self, command, timeout=10):
        if self.client:
            buffer = command.encode()
            self.send(buffer)
            
            output = self.recv(timeout)
            output = output.decode().strip()
            
            return output
        return None
        
    #
    # Functions to manipulate 
    #
        
    def start_server(self, local_host, local_port):
        self.badges.output_process("Binding to " + local_host + ":" + local_port + "...")
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((local_host, int(local_port)))
            server.listen(1)
        except Exception:
            self.badges.output_error("Failed to bind to " + local_host + ":" + local_port + "!")
            raise self.exceptions.GlobalException
        return server
