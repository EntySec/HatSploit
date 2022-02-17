#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.modules import Modules


class HatSploitCommand(Command):
    modules = Modules()

    details = {
        'Category': "modules",
        'Name': "use",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Use specified module.",
        'Usage': "use <module|number>",
        'MinArgs': 1
    }

    complete = modules.modules_completer

    def run(self, argc, argv):
        self.modules.use_module(argv[1])
