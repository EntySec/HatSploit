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

from flask import Flask, json
from flask_restful import Resource, Api, reqparse
import ast
import logging

from hatsploit.lib.sessions import Sessions

class SessionManager(Resource):
    sessions = Sessions()

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('platform')
        parser.add_argument('type')
        parser.add_argument('id', type=int)
        parser.add_argument('command')
        parser.add_argument('close', action='store_true')
        parser.add_argument('count', action='store_true')
        args = parser.parse_args()

        if args['platform'] and args['type'] and args['id'] and args['command']:
            session = self.sessions.get_session(
                args['platform'], args['type'], args['id']
            )

            if session:
                return session.send_command(args['command'], output=True), 200
            return "", 200

        elif args['platform'] and args['id'] and args['close']:
            self.sessions.close_session(
                args['platform'], args['id']
            )

            return "", 200

        elif args['count']:
            sessions = self.sessions.get_all_sessions()
            if sessions:
                if args['platform']:
                    if args['platform'] in sessions.keys():
                        return len(sessions[args['platform']]), 200
                    return 0, 200
                return len(sessions), 200
            return 0, 200

        sessions = self.sessions.get_all_sessions()
        if sessions:
            for platform in sessions.keys():
                for session_id in sessions[platform].keys():
                    del sessions[platform][session_id]['object']
            return sessions, 200
        return dict(), 200

class API:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)

    def init(self):
        self.api.add_resource(SessionManager, '/sessions')
        #self.app.logger.disabled = True
        #log = logging.getLogger('werkzeug')
        #log.disabled = True
        self.app.run()
    
