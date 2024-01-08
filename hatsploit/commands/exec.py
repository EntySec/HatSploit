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
            'Category': "developer",
            'Name': "exec",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Execute local system command.",
            'Usage': "exec <command>",
            'MinArgs': 1,
        })

    def run(self, argc, argv):
        commands = self.format_commands(argv[1])
        self.commands.execute_system_command(commands)
