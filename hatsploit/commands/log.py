"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command
from hatsploit.lib.log import Log


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "log",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Log HatSploit output to log file.",
            'MinArgs': 1,
            'Options': [
                (
                    ('-e', '--enable'),
                    {
                        'help': "Enable logging to file.",
                        'metavar': 'FILE',
                    }
                ),
                (
                    ('-d', '--disable'),
                    {
                        'help': "Disable logging to file.",
                        'action': 'store_true'
                    }
                )
            ]
        })

        self.log = Log()

    def run(self, args):
        if args.enable:
            self.log.enable_log(args.enable)

        elif args.disable:
            self.log.disable_log()
