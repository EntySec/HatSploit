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

import logging

from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response

from hatsploit.utils.string import StringTools


class API:
    def __init__(self, username, password):
        self.string_tools
        self.username = username
        self.password = password

        self.token = self.string_tools.random_string(32)

    def run(self):
        rest_api = Flask("HatSploit")

        log = logging.getLogger("werkzeug")
        log.setLevel(logging.ERROR)

        @rest_api.before_request
        def validate_token():
            if request.path != '/login':
                token = request.args.get('token')
                if token != self.token:
                    return make_response('', 401)

        @rest_api.route('/login', methods=['POST'])
        def server_login():
            username = request.form['username']
            password = request.form['password']

            if username == self.username and password == self.password:
                return jsonify(token=self.token)
            else:
                return make_response('', 401)
