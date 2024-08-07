"""
This plugin requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from pex.proto.tcp import TCPClient
from pex.proto.ssh import SSHClient
from pex.proto.channel import ChannelClient

from hatsploit.lib.core.plugin import Plugin


class HatSploitPlugin(Plugin):
    def __init__(self):
        super().__init__({
            'Name': "HatSploit Network Utilities",
            'Plugin': "netutils",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - plugin developer"
            ],
            'Description': "Network utilities plugin for HatSploit.",
        })

        self.commands.update({
            'telnet': {
                'Description': "Connect to TCP server.",
                'Usage': "telnet <host> <port>",
                'MinArgs': 2,
            },
            'ssh': {
                'Description': "Connect to SSH server.",
                'Usage': "ssh [user]@[host] [port]",
                'MinArgs': 1
            }
        })

    @staticmethod
    def telnet(args):
        client = TCPClient(host=args[1], port=int(args[2]))
        client.connect()

        channel = ChannelClient(client.sock)
        channel.interact()

    def ssh(self, args):
        port = 22

        if len(args) > 2:
            port = int(args[2])

        pair = args[1].split('@')

        if len(pair) != 2:
            self.print_usage(self.commands['ssh']['Usage'])
            return

        password = self.input_empty(f"{args[1]}'s password: ", is_password=True)

        client = SSHClient(
            host=pair[1],
            port=port,
            username=pair[0],
            password=password
        )
        client.connect()
        client.interact()

    def load(self):
        self.print_information("HatSploit Network Utils")
        self.print_information("Copyright (c) Ivan Nikolskiy 2024")

        banner = r"""
     _______________                        %purple|*\_/*|%end________
    |  ___________  |     %red.-.     .-.%end      |%purple|_/-\_|%end______  |
    | |           | |    %red.****. .****.%end     | |           | |
    | |   0   0   | |    %red.*****.*****.%end     | |   0   0   | |
    | |     -     | |     %red.*********.%end      | |     -     | |
    | |   \___/   | |      %red.*******.%end       | |   \___/   | |
    | |___     ___| |       %red.*****.%end        | |___________| |
    |_____%yellow|\_/|%end_____|        %red.***.%end         |_______________|
      _|__%yellow|/ \|%end_|_.............%red*%end.............._|________|_
     / %dark**********%end \                          / %dark**********%end \
   /  %dark************%end  \                      /  %dark************%end  \
   --------------------                    --------------------
"""

        self.print_empty(banner)
        self.print_information("Commands: %greentelnet%end, %greenssh%end")
