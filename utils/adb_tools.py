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

import shutil
import subprocess

from core.badges import badges

class adb_tools:
    def __init__(self):
        self.badges = badges()
        
        self.adb = "adb"

    #
    # Functions to check dependencies
    #
        
    def check_adb_installation(self):
        if shutil.where(self.adb):
            return True
        return False
    
    #
    # Functions to control ADB server
    #
    
    def start_adb_server(self):
        self.execute_adb_command("start-server", output=False)
        
    def stop_adb_server(self):
        self.execute_adb_command("disconnect", output=False)
        self.execute_adb_command("kill-server", output=False)
    
    
    #
    # Functions to connect/disconnect devices
    #
    
    def connect(self, target_addr):
        self.execute_adb_command("connect", target_addr, False)
        
    def disconnect(self, target_addr):
        self.execute_adb_command("disconnect", target_addr, False)
        
    #
    # Functions to check connection to devices
    #
        
    def check_connected(self, target_addr):
        is_connected = self.execute_adb_command("devices", f"| grep {target_addr}")
        offline_devices = self.execute_adb_command("devices", "| grep offline")
        
        if not is_connected:
            return False
        elif target_addr in offline_devices:
            return False
        
        return True
    
    #
    # Functions to send commands to ADB server
    #
    
    def execute_adb_command(self, command, arguments="", output=True):
        if self.check_adb_installation():
            command_output = subprocess.getoutput(f"{self.adb} {command} {arguments}")
            if output:
                return command_output.strip()
        else:
            self.badges.output_error("Failed to execute command!")
