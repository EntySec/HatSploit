"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "developer",
            'Name': "repeat",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Repeat specified command.",
            'Usage': "repeat <times> <command>",
            'MinArgs': 2,
        })

    def run(self, args):
        if args[1].isdigit():
            for _ in range(int(args[1])):
                self.console.onecmd(' '.join(args[2:]))
        else:
            self.print_error("Times expected!")
