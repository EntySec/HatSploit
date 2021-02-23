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

        self.http_client = requests.request
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    
    #
    # Functions to manipulate responses
    #
    
    def generate_fake_response(self):
        fake_response = requests.models.Response()
        
        fake_response.code = ""
        fake_response.error_type = ""
        fake_response.status_code = 0
        fake_response.headers = {'Server': ''}
        
        return fake_response
    
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
    
    def check_url_access(self, url, path='/', new_user_agent=True, timeout=10):
        response = self.http_request(
            method="HEAD",
            url=url, 
            path=path, 
            user_agent=user_agent, 
            timeout=timeout
        )
        
        if response.status_code != 0:
            return True
        return False
    
    def check_url_ssl(self, url, set_user_agent=True, timeout=10):
        try:
            if set_user_agent:
                response = verify=False, headers=self.get_user_agent_header(), timeout=timeout)
            else:
                response = requests.get(url, verify=False, timeout=timeout)
        except Exception:
            response = self.generate_fake_response()
        
        if response.status_code == 400:
            return True
        return False
    
    #
    # HTTP requests
    #

    def http_request(self, method: None, url: None, path: None, data=None, user_agent=True, timeout=10):
        url = self.normalize_url(url, timeout=timeout)
        
        if not path.startswith('/') and not url.endswith('/'):
            path = '/' + path
        url += path
        
        headers = None
        if user_agent:
            headers = self.get_user_agent_header()
        
        try:
            response = self.http_client(
                method=method,
                url=url,
                data=data,
                headers=headers,
                timeout=timeout,
                verify=False
            )
        except Exception:
            return self.generate_fake_response()
        return response
    
    #
    # TCP requests
    #
    
    def tcp_reqeust(self, remote_host: None, remote_port: None, data: None, buffer_size=1024, timeout=10):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((remote_host, int(remote_port)))
        sock.send(data.encode())
        output = sock.recv(buffer_size)
        sock.close()
        return output.decode().strip()
    
    #
    # TCP ports
    #
    
    def check_tcp_port(self, remote_host: None, remote_port: None, timeout=10):
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
    
    def craft_url(self, remote_host, remote_port, timeout=10):
        url = remote_host + ':' + remote_port
        return self.normalize_url(url, timeout=timeout)
    
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
    
    def normalize_url(self, url, check_ssl=True, timeout=10):
        if check_ssl:
            if self.check_url_ssl(url, timeout=timeout):
                url = self.add_https_to_url(url)
                return url

        url = self.add_http_to_url(url)
        return url
