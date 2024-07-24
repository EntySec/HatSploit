"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command
from hatsploit.lib.log import Log


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "developer",
            'Name': "log",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Log HatSploit output to log file.",
            'Usage': "log <option> [arguments]",
            'MinArgs': 1,
            'Options': {
                'on': ['<file>', "Turn logging on."],
                'off': ['', "Turn logging off."],
            },
        })

        self.log = Log()

    def run(self, args):
        if args[1] == 'on':
            self.log.enable_log(args[2])

        elif args[1] == 'off':
            self.log.disable_log()
