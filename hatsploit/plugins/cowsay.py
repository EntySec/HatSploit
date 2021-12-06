#!/usr/bin/env python3

#
# This plugin requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

import textwrap

from hatsploit.lib.plugin import Plugin


class HatSploitPlugin(Plugin):
    details = {
        'Name': "cowsay",
        'Authors': [
            'Ivan Nikolsky (enty8080) - plugin developer'
        ],
        'Description': "Cowsay plugin for HatSploit."
    }

    commands = {
        'cowsay': {
            'cowsay': {
                'Description': "Ask cow to say message.",
                'Usage': "cowsay <message>",
                'MinArgs': 1
            }
        }
    }

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
         \   ^__^ 
          \  (oo)\_______
             (__)\       )\/\\
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

    def cowsay(self, argc, argv):
        message = argv[1]
        cow = self.ask_cow(message, len(message))
        self.print_empty(cow)

    def run(self):
        message = "Cow here, moo!"
        cow = self.ask_cow(message, len(message))
        self.print_empty(cow)

        self.print_information("Use " + self.GREEN + "cowsay" + self.END + " to call me.")
