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
        if shutil.which(self.adb):
            return True
        return False
    
    #
    # Functions to control ADB server
    #
    
    def start_adb_server(self):
        server_log = self.execute_adb_command("start-server")
        
        if not server_log or "failed" in server_log:
            return False
        return True
        
    def stop_adb_server(self):
        self.execute_adb_command("disconnect", output=False)
        server_log = self.execute_adb_command("kill-server")
        
        if server_log:
            if "cannot" in server_log:
                return False
        return True
    
    #
    # Functions to connect/disconnect devices
    #
    
    def connect(self, target_addr):
        server_log = self.execute_adb_command("connect", target_addr)
        
        if not server_log or "failed" in server_log:
            return False
        return True
        
    def disconnect(self, target_addr):
        server_log = self.execute_adb_command("disconnect", target_addr)
        
        if not server_log or "error" in server_log:
            return False
        return True
        
    #
    # Functions to check connection to devices
    #
        
    def check_connected(self, target_addr):
        device = self.execute_adb_command("devices", f"| grep {target_addr}")
        device = device.split('\t')
        
        if len(device) == 2:
            device_addr = device[0]
            device_state = device[1]
            
            if device_addr == target_addr:
                if device_state == 'device':
                    return True
        
        return False
    
    #
    # Functions to send commands to ADB server
    #
    
    def execute_adb_command(self, command, arguments="", output=True):
        if self.check_adb_installation():
            command_output = subprocess.getoutput(f"{self.adb} {command} {arguments}")
            if output:
                return command_output.strip()
        else:
            return False
