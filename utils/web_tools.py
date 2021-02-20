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
import random
import requests

from core.config import config

from requests.packages.urllib3.exceptions import InsecureRequestWarning

class web_tools:
    def __init__(self):
        self.config = config()
        
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    
    #
    # Functions to manipulate User-Agent
    #
    
    def new_user_agent(self):
        file = open(self.config.path_config['base_paths']['data_path'] + 'utils/web_tools/user_agents.txt')
        user_agents = list(filter(None, file.read().split('\n')))
        
        file.close()
        
        number = random.randint(0, len(user_agents))
        return user_agents[number]
    
    def get_user_agent_header(self):
        user_agent = self.new_user_agent()
        headers = {
            'User-Agent': user_agent
        }
        
        return headers
    
    #
    # Functions to check URL stability
    #
    
    def check_url_access(self, url, path=None, new_user_agent=True):
        response = self.send_head_to_url(url, path, new_user_agent)
        if response:
            return True
        return False
    
    def check_url_ssl(self, url, set_user_agent=True):
        try:
            if set_user_agent:
                response = requests.get(url, verify=False, headers=self.get_user_agent_header())
            else:
                response = requests.get(url, verify=False)
        except Exception:
            response = None
        
        if response:
            if response.status_code == 400:
                return True
        return False
    
    #
    # Functions to send something to URL
    #
    
    def send_head_to_url(self, url, path=None, set_user_agent=True):
        url = self.normalize_url(url)
        if path:
            if not path.startswith('/') and not url.endswith('/'):
                path = '/' + path
            url += path
        try:
            if set_user_agent:
                response = requests.head(url, verify=False, headers=self.get_user_agent_header())
            else:
                response = requests.head(url, verify=False)
        except Exception:
            return None
        return response
    
    def send_get_to_url(self, url, path=None, set_user_agent=True):
        url = self.normalize_url(url)
        if path:
            if not path.startswith('/') and not url.endswith('/'):
                path = '/' + path
            url += path
        try:
            if set_user_agent:
                response = requests.get(url, verify=False, headers=self.get_user_agent_header())
            else:
                response = requests.get(url, verify=False)
        except Exception:
            return None
        return response
    
    def send_post_to_url(self, url, data, path=None, set_user_agent=True):
        url = self.normalize_url(url)
        if path:
            if not path.startswith('/') and not url.endswith('/'):
                path = '/' + path
            url += path
        try:
            if set_user_agent:
                response = requests.post(url, data, verify=False, headers=self.get_user_agent_header())
            else:
                response = requests.post(url, data, verify=False)
        except Exception:
            return None
        return response
    
    #
    # Functions to send something to host and port
    #
    
    def send_post_to_host(self, remote_host, remote_port, data, buffer_size=1024, timeout=10):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((remote_host, int(remote_port)))
        sock.send(data.encode())
        output = sock.recv(buffer_size)
        sock.close()
        return output.decode().strip()
    
    def check_port_opened(self, remote_host, remote_port, timeout=10):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        if sock.connect_ex((remote_host, int(remote_port))) == 0:
            sock.close()
            return True
        sock.close()
        return False
    
    #
    # Functions to parse host and port
    #
    
    def format_host_and_port(self, remote_host, remote_port):
        return remote_host + ':' + str(remote_port)
    
    #
    # Functions to parse URL
    #
    
    def craft_url(self, remote_host, remote_port):
        url = remote_host + ':' + remote_port
        return self.normalize_url(url)
    
    def get_url_port(self, url):
        url = self.strip_scheme(url)
        return url.split(':')[1]
        
    def get_url_host(self, url):
        url = self.strip_scheme(url)
        return url.split(':')[0]
    
    def strip_scheme(self, url, strip_path=True):
        url = url.replace('http://', '', 1)
        url = url.replace('https://', '', 1)
        if strip_path:
            url = url.split('/')[0]
        return url
    
    def add_http_to_url(self, url):
        url = self.strip_scheme(url, False)
        url = 'http://' + url
        
        return url
    
    def add_https_to_url(self, url):
        url = self.strip_scheme(url, False)
        url = 'https://' + url
        
        return url
    
    def normalize_url(self, url, check_ssl=True):
        if check_ssl:
            if self.check_url_ssl(url):
                url = self.add_https_to_url(url)
                return url

        url = self.add_http_to_url(url)
        return url

    #
    # Functions to get something from URL
    #
    
    def get_url_server(self, url):
        headers = self.send_head_to_url(url).headers
        if headers:
            if 'Server' in headers.keys():
                return headers['Server']
        return None
