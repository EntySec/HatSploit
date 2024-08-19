"""
This plugin requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

import textwrap

from badges.cmd import Command
from hatsploit.lib.core.plugin import Plugin


class HatSploitPlugin(Plugin):
    def __init__(self):
        super().__init__({
            'Name': "HatSploit Cowsay Implementation",
            'Plugin': "cowsay",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - plugin developer"
            ],
            'Description': "Cowsay plugin for HatSploit.",
        })

        self.commands = [
            Command({
                'Name': 'cowsay',
                'Description': "Ask cow to say message.",
                'Usage': "cowsay <message>",
                'MinArgs': 1,
            })
        ]

    def ask_cow(self, message, length=40):
        return self.build_bubble(message, length) + self.build_cow()

    @staticmethod
    def get_border(lines, index):
        if len(lines) < 2:
            return ["<", ">"]
        if index == 0:
            return ["/", "\\"]
        if index == len(lines) - 1:
            return ["\\", "/"]
        return ["|", "|"]

    @staticmethod
    def build_cow():
        return """
         \\   ^__^ 
          \\  (oo)\\_______
             (__)\\       )\\/\\
                 ||----w |
                 ||     ||
        """

    @staticmethod
    def normalize_text(message, length):
        lines = textwrap.wrap(message, length)
        maxlen = len(max(lines, key=len))
        return [line.ljust(maxlen) for line in lines]

    def build_bubble(self, message, length=40):
        bubble = []
        lines = self.normalize_text(message, length)
        bordersize = len(lines[0])
        bubble.append(" __" + "_" * bordersize)
        for index, line in enumerate(lines):
            border = self.get_border(lines, index)
            bubble.append("%s %s %s" % (border[0], line, border[1]))
        bubble.append(" --" + "-" * bordersize)
        return "\n".join(bubble)

    def cowsay(self, args):
        cow = self.ask_cow(args[1], len(args[1]))
        self.print_empty(cow)

    def load(self):
        self.cowsay(["cowsay", "Cow here, moo!"])
        self.print_information("Use %greencowsay%end to call me.")
