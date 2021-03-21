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

import binascii
import os
import time

from core.cli.badges import Badges
from utils.fs.fs import fs
from utils.tcp.tcp import tcp


class transfer:
    def __init__(self, client):
        self.badges = Badges()

        self.fs = fs()
        self.tcp = tcp()

        self.tcp.connect(client)

    def download(self, input_file, output_path):
        exists, path_type = self.fs.exists_directory(output_path)
        if exists:
            if path_type != "file":
                if output_path[-1] == "/":
                    output_path = output_path + os.path.split(input_file)[1]
                else:
                    output_path = output_path + "/" + os.path.split(input_file)[1]

            error_status = binascii.hexlify(os.urandom(8)).decode()
            payload = f"download {input_file}\x04"

            self.tcp.send(payload.encode())
            self.tcp.send((error_status + '\x04').encode())

            status = self.tcp.recv(None)
            status = status.decode()

            if status:
                if "success" in status:
                    self.badges.output_process("Downloading " + input_file + "...")

                    output_file = open(output_path, 'wb')
                    data = self.tcp.recv(None)

                    if not data.decode() == error_status:
                        output_file.write(data)
                        output_file.close()
                    else:
                        output_file.close()
                        os.remove(output_path)

                        self.badges.output_error("Failed to upload!")
                        return

                    self.badges.output_process("Saving to " + output_path + "...")
                    self.badges.output_success("Saved to " + output_path + "!")
                else:
                    self.badges.output_error(status)

    def upload(self, input_file, output_path):
        if self.fs.file(input_file):
            output_directory = output_path
            output_filename = os.path.split(input_file)[1]

            error_status = binascii.hexlify(os.urandom(8)).decode() + '\x04'
            stop_status = binascii.hexlify(os.urandom(8)).decode() + '\x04'

            payload = f"upload {output_directory}:{output_filename}\x04"
            self.tcp.send(payload.encode())

            self.tcp.send(error_status.encode())
            self.tcp.send(stop_status.encode())

            status = self.tcp.recv(None)
            status = status.decode()

            if status:
                if "success" in status:
                    self.badges.output_process("Uploading " + input_file + "...")
                    with open(input_file, "rb") as file:
                        for data in iter(lambda: file.read(4100), b""):
                            try:
                                self.tcp.send(data)
                            except (KeyboardInterrupt, EOFError):
                                file.close()
                                self.tcp.send(error_status)
                                self.badges.output_error("Failed to upload!")
                                return
                    self.tcp.send("\x04".encode())
                    self.tcp.send(stop_status.encode())

                    self.badges.output_process(self.tcp.recv().decode().strip())
                    self.badges.output_success(self.tcp.recv().decode().strip())
                else:
                    self.badges.output_error(status)
