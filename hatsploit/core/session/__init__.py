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

from hatsploit.lib.session import Session
from hatsploit.lib.loot import Loot

from pex.post.pull import Pull
from pex.post.push import Push

from pex.client.channel import ChannelClient


class HatSploitSession(Session, Loot, Pull, Push, ChannelClient):
    channel = None

    details = {
        'Post': "",
        'Platform': "",
        'Architecture': "",
        'Type': "shell"
    }

    def open(self, client):
        self.channel = self.open_channel(client)

    def close(self):
        self.channel.disconnect()

    def heartbeat(self):
        return not self.channel.terminated

    def send_command(self, command, output=False, decode=True):
        return self.channel.send_command(
            (command + '\n'),
            output,
            decode
        )

    def download(self, remote_file, local_path):
        self.print_process(f"Downloading {remote_file}...")

        data = self.pull(
            platform=self.details['Platform'],
            sender=self.send_command,
            location=remote_file,
            args={
                'decode': False,
                'output': True
            }
        )

        if data:
            return self.save_file(
                location=local_path,
                data=data,
                filename=remote_file
            )

        return None

    def upload(self, local_file, remote_path):
        self.print_process(f"Uploading {local_file}...")
        data = self.get_file(local_file)

        if data:
            self.print_process(f"Saving to {remote_path}...")
            remote_path = self.push(
                platform=self.details['Platform'],
                sender=self.send_command,
                data=data,
                location=remote_path,
                method=self.details['Post']
            )

            self.print_success(f"Saved to {remote_path}!")
            return remote_path

        return None

    def interact(self):
        if not self.channel.interact():
            if not self.heartbeat():
                self.print_warning("Connection terminated.")
            else:
                self.print_error("Failed to interact with session!")

