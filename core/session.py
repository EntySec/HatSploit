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

'''
sessions = {
    'session_property': {
        session_id: {
            session_object: '',
            ...
        }
    }
}
'''

from core.storage import local_storage

class session:
    def __init__(self):
        self.local_storage = local_storage()
        
    def add_session(self, session_id, session_property, session_object):
        if not self.local_storage.get("sessions"):
            self.local_storage.set("sessions", dict())

        if session_property in self.local_storage.get("sessions").keys():
            sessions = self.local_storage.get("sessions")
            sessions[session_property][int(session_id)] = {
                'session_object': session_object
            }
        else:
            sessions = {
                session_property: {
                    int(session_id): {
                        'session_object': session_object
                    }
                }
            }
        
        self.local_storage.update("sessions", sessions)
    
    def close_session(self, session_id, session_property):
        pass
    
    def get_session(self, session_id, session_property):
        sessions = self.local_storage.get("sessions")
        if sessions:
            if session_property in sessions.keys():
                if int(session_id) in sessions[session_property].keys():
                    return sessions[session_property][int(session_id)]['session_object']
        return None
