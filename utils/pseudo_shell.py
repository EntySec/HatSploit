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
import requests.exceptions

from core.cli.badges import badges
from core.base.jobs import jobs
from core.base.exceptions import exceptions

class pseudo_shell:
    def __init__(self):
        self.badges = badges()
        self.jobs = jobs()
        self.exceptions = exceptions()
        
        self.prompt = 'pseudo % '
        
    def pseudo_shell_header(self):
        self.badges.output_empty("")
        self.badges.output_information("--=( Welcome to Pseudo shell )=--")
        self.badges.output_information("Interface for executing commands on the target.")
        self.badges.output_information("Commands are sent to the target via provided execute method.")
        self.badges.output_empty("")
        
    def execute_command(self, execute_method, command, arguments=()):
        try:
            if command == "exit":
                return
            if isinstance(arguments, tuple):
                output = execute_method(*arguments, command).strip()
            else:
                output = execute_method(arguments, command).strip()
            if isinstance(output, tuple) and len(output) == 2:
                if output[0]:
                    if output[1]:
                        self.badges.output_empty(output[1])
                    else:
                        self.badges.output_warning("No output provided by command.")
                else:
                    self.badges.output_error("Failed to execute command!")
            else:
                self.badges.output_error("Invalid execute method!")
        except (requests.exceptions.Timeout, socket.timeout):
            self.badges.output_warning("Timeout waiting for response.")
        except Exception as e:
            self.badges.output_error("An error occurred: " + str(e) + "!")
        
    def spawn_pseudo_shell(self, module_name, execute_method, arguments=()):
        self.badges.output_process("Spawning Pseudo shell...")
        
        if self.jobs.check_module_job(module_name):
            self.badges.output_error("Failed to spawn Pseudo shell!")
            self.badges.output_warning("Pseudo shell can not be background job.")
        else:
            self.badges.output_success("Congratulations, you won Pseudo shell!")
        
            self.pseudo_shell_header()
            self.launch_pseudo_shell(execute_method, arguments)
        
    def launch_pseudo_shell(self, execute_method, arguments):
        while True:
            try:
                command = self.badges.input_empty(self.prompt)
            except (KeyboardInterrupt, EOFError, self.exceptions.GlobalException):
                pass
            self.execute_command(execute_method, command, arguments)
