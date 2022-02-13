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
from flask_restful import Resource, Api, reqparse

from hatsploit.lib.sessions import Sessions
from hatsploit.lib.config import Config


class SessionManager(Resource):
    sessions = Sessions()
    config = Config()

    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id')
        parser.add_argument('command')
        parser.add_argument('output')

        parser.add_argument('path')
        parser.add_argument('download')
        parser.add_argument('upload')

        parser.add_argument('close')
        parser.add_argument('count')
        parser.add_argument('list')

        args = parser.parse_args()

        if args['id']:
            if args['command']:
                session = self.sessions.get_session(args['id'])

                if session:
                    if args['output']:
                        if args['output'].lower() in ['yes', 'y']:
                            output = session.send_command(args['command'], output=True)
                            return output, 200

                    session.send_command(args['command'])
                return "", 200

            if args['download']:
                self.sessions.download_from_session(
                    args['id'],
                    args['download'],
                    args['path'] if args['path'] else self.config.path_config['loot_path']
                )

            elif args['upload'] and args['path']:
                self.session.upload_to_session(
                    args['id'],
                    args['upload'],
                    args['path']
                )

        else:
            if args['close']:
                self.sessions.close_session(args['close'])
                return "", 200

        
            if args['count']:
                sessions = self.sessions.get_all_sessions()
                if sessions:
                    if args['count'] == 'all':
                        return len(sessions), 200
                    counter = 0
                    for session in sessions:
                        if sessions[session]['platform'] == args['count']:
                            counter += 1
                    return counter, 200
                return 0, 200

            if args['list']:
                sessions = self.sessions.get_all_sessions()
                data = {}

                if sessions:
                    for session in sessions:
                        if args['list'] == 'all':
                            data.update({
                                session: {
                                    'platform': sessions[session]['platform'],
                                    'architecture': sessions[session]['architecture'],
                                    'type': sessions[session]['type'],
                                    'host': sessions[session]['host'],
                                    'port': sessions[session]['port']
                                }
                            })
                        else:
                            if sessions[session]['platform'] == args['list']:
                                data.update({
                                    session: {
                                        'platform': sessions[session]['platform'],
                                        'architecture': sessions[session]['architecture'],
                                        'type': sessions[session]['type'],
                                        'host': sessions[session]['host'],
                                        'port': sessions[session]['port']
                                    }
                                })
                return data, 200

        return "", 200


class API:
    app = Flask(__name__)
    api = Api(app)

    def init(self, port=8008):
        self.api.add_resource(SessionManager, '/sessions')
        self.app.logger.disabled = True

        log = logging.getLogger('werkzeug')
        log.disabled = True

        self.app.run(host='127.0.0.1', port=int(port))
