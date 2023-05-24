"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.commands import Commands


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.commands = Commands()

        self.details.update({
            'Category': "core",
            'Name': "help",
            'Authors': [
                'Ivan Nikolsky (enty8080) - command developer',
            ],
            'Description': "Show available commands.",
            'Usage': "help",
            'MinArgs': 0,
        })


    def run(self, argc, argv):
        self.commands.execute_command(['?'])
