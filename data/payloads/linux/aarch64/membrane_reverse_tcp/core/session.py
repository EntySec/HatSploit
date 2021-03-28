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

import os

from core.lib.session import Session
from utils.tcp.tcp import TCPClient
from utils.string.string import StringTools
from utils.fs.fs import FSTools

class HatSploitSession(Session, TCPClient, StringTools, FSTools):
    details = {
        'Platform': "linux",
        'Type': "membrane"
    }

    def open(self, client):
        self.connect(client)

    def close(self):
        self.disconnect()

    def send_command(self, command, arguments=None, output=True, timeout=10):
        if arguments:
            command += " " + arguments

        output = self.send_cmd(command + '\x04', output, timeout)

        if "error" in output:
            return False, ""
        return True, output

    def interact(self):
        self.interactive('\x04')

    def download(self, input_file, output_path):
        exists, path_type = self.exists_directory(output_path)
        if exists:
            if path_type != "file":
                if output_path[-1] == "/":
                    output_path = output_path + os.path.split(input_file)[1]
                else:
                    output_path = output_path + "/" + os.path.split(input_file)[1]

            error_status = self.random_string()
            payload = f"download {input_file}\x04"

            self.send(payload.encode())
            self.send((error_status + '\x04').encode())

            status = self.recv(None)
            status = status.decode()

            if status:
                if "success" in status:
                    self.output_process("Downloading " + input_file + "...")

                    output_file = open(output_path, 'wb')
                    data = self.recv(None)

                    if not data.decode() == error_status:
                        output_file.write(data)
                        output_file.close()
                    else:
                        output_file.close()
                        os.remove(output_path)

                        self.output_error("Failed to upload!")
                        return

                    self.output_process("Saving to " + output_path + "...")
                    self.output_success("Saved to " + output_path + "!")
                else:
                    self.output_error(status)

    def upload(self, input_file, output_path):
        if self.file(input_file):
            output_directory = output_path
            output_filename = os.path.split(input_file)[1]

            error_status = self.random_string() + '\x04'
            stop_status = self.random_string() + '\x04'

            payload = f"upload {output_directory}:{output_filename}\x04"
            self.send(payload.encode())

            self.send(error_status.encode())
            self.send(stop_status.encode())

            status = self.recv(None)
            status = status.decode()

            if status:
                if "success" in status:
                    self.output_process("Uploading " + input_file + "...")
                    with open(input_file, "rb") as file:
                        for data in iter(lambda: file.read(4100), b""):
                            try:
                                self.send(data)
                            except (KeyboardInterrupt, EOFError):
                                file.close()
                                self.send(error_status)
                                self.output_error("Failed to upload!")
                                return
                    self.send("\x04".encode())
                    self.send(stop_status.encode())

                    self.output_process(self.recv().decode().strip())
                    self.output_success(self.recv().decode().strip())
                else:
                    self.output_error(status)
