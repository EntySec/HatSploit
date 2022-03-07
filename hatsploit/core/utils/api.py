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
from flask import jsonify
from flask import request
from flask import make_response

from hatsploit.utils.string import StringTools

from hatsploit.lib.jobs import Jobs
from hatsploit.lib.modules import Modules
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.config import Config


class API:
    def __init__(self, username, password, host='127.0.0.1', port=8008):
        self.string_tools = StringTools()

        self.jobs = Jobs()
        self.modules = Modules()
        self.payloads = Payloads()
        self.sessions = Sessions()
        self.config = Config()

        self.host = host
        self.port = int(port)

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
                token = request.form['token']
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

        @rest_api.route('/modules', methods=['POST'])
        def server_modules():
            action = request.form['action']

            if action == 'list':
                data = {}
                all_modules = self.modules.get_modules()
                number = 0
                
                for database in sorted(all_modules):
                    data.update({
                        number: {
                            'Module': modules[module]['Module'],
                            'Rank': modules[module]['Rank'],
                            'Name': modules[module]['Name'],
                            'Platform': modules[module]['Platform']
                        }
                    })
                    
                    number += 1

                return jsonify(data)

            elif action == 'options':
                data = {}
                current_module = self.modules.get_current_module_object()

                if current_module:
                    options = current_module.options

                    for option in sorted(options):
                        value, required = options[option]['Value'], options[option]['Required']
                        if required:
                            required = 'yes'
                        else:
                            required = 'no'
                        if not value and value != 0:
                            value = ""
                        data.update({
                            option: {
                                'Value': value,
                                'Required': required,
                                'Description': options[option]['Description']
                            }
                        })

                    if hasattr(current_module, "payload"):
                        current_payload = self.payloads.get_current_payload()

                        if hasattr(current_payload, "options"):
                            options = current_payload.options

                            for option in sorted(options):
                                value, required = options[option]['Value'], options[option]['Required']
                                if required:
                                    required = 'yes'
                                else:
                                    required = 'no'
                                if not value and value != 0:
                                    value = ""
                                data.update({
                                    option: {
                                        'Value': value,
                                        'Required': required,
                                        'Description': options[option]['Description']
                                    }
                                })

                return jsonify(data)

            if action == 'use':
                self.modules.use_module(request.form['module'])

            if action == 'set':
                self.modules.set_current_module_option(
                    request.form['option'],
                    request.form['value']
                )

            if action == 'run':
                current_module = self.modules.get_current_module_object()

                if current_module:
                    self.jobs.create_job(current_module.details['Name'],
                                         current_module.details['Module'],
                                         self.modules.run_current_module)

            return make_response('', 200)

        @rest_api.route('/sessions', methods=['POST'])
        def server_sessions():
            action = request.form['action']

            if action == 'close':
                session = request.form['session']
                self.sessions.close_session(session)

            elif action == 'list':
                data = {}
                sessions = self.sessions.get_all_sessions()
                fetch = request.form['fetch']

                if sessions:
                    for session in sessions:
                        if fetch == 'all':
                            data.update({
                                session: {
                                    'platform': sessions[session]['platform'],
                                    'architecture': sessions[session]['architecture'],
                                    'type': sessions[session]['type'],
                                    'host': sessions[session]['host'],
                                    'port': sessions[session]['port']
                                }
                            })
                        elif fetch == sessions[session]['platform']:
                            data.update({
                                session: {
                                    'platform': sessions[session]['platform'],
                                    'architecture': sessions[session]['architecture'],
                                    'type': sessions[session]['type'],
                                    'host': sessions[session]['host'],
                                    'port': sessions[session]['port']
                                }
                            })

                return jsonify(data)

            elif action == 'execute':
                session = request.form['session']
                session = self.sessions.get_session(session)
                
                if session:
                    if request.form['output'].lower() in ['yes', 'y']:
                        output = session.send_command(request.form['command'], output=True)
                        return jsonify(output=output)

                    session.send_command(request.form['command'])

            elif action == 'download':
                if 'local_path' in request.form:
                    local_path = request.form['local_path']
                else:
                    local_path = self.config.path_config['loot_path']

                self.sessions.download_from_session(
                    request.form['session'],
                    request.form['remote_file'],
                    local_path
                )

            elif action == 'upload':
                self.session.upload_to_session(
                    request.form['session'],
                    request.form['local_file'],
                    request.form['remote_path']
                )

            return make_response('', 200)

        rest_api.run(host=self.host, port=self.port)
