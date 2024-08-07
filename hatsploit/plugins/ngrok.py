"""
This plugin requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

import socket
from pyngrok import ngrok

from hatsploit.lib.core.plugin import Plugin


class HatSploitPlugin(Plugin):
    def __init__(self):
        super().__init__({
            'Name': "HatSploit Ngrok Implementation",
            'Plugin': "ngrok",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - plugin developer"
            ],
            'Description': "Manage ngrok service right from HatSploit.",
        })

        self.commands.update({
            'ngrok': {
                'Description': "Manage ngrok service.",
                'Usage': "ngrok <option> [arguments]",
                'MinArgs': 1,
                'Options': {
                    '-l': ['', "List all active tunnels."],
                    '-o': ['<port>', "Open tunnel for specified port."],
                    '-c': ['<id>', "Close specified tunnel."],
                    '-a': ['<token>', "Authenticate ngrok API token."],
                },
            }
        })

        self.tunnels = []
        self.handler = ngrok

    @staticmethod
    def parse_tunnel(tunnel):
        tunnel = tunnel.public_url.strip('tcp://').split(':')

        host = socket.gethostbyname(tunnel[0])
        port = tunnel[1]

        return host, port

    def ngrok(self, args):
        if args[1] in ['-o', '--open']:
            try:
                self.print_process(f"Opening tunnel for port {args[2]}...")

                tunnel = self.handler.connect(int(args[2]), "tcp")
                data = self.parse_tunnel(tunnel)

                route = f"127.0.0.1:{args[2]} -> {data[0]}:{data[1]}"

                self.print_success(f"Tunnel opened ({route})!")
                self.tunnels.append([route, tunnel])
            except Exception:
                self.print_error(f"Failed to open tunnel port {args[2]}!")

        elif args[1] in ['-a', '--auth']:
            self.handler.set_auth_token(args[2])

        elif args[1] in ['-c', '--close']:
            try:
                self.print_process(f"Closing tunnel {args[2]}...")

                self.handler.disconnect(self.tunnels[int(args[2])][1])
                self.tunnels.pop(int(args[2]))

            except Exception:
                self.print_error(f"Invalid tunnel given!")

        elif args[1] in ['-l', '--list']:
            headers = ('ID', 'Connection')

            tunnel_id = 0
            tunnels_data = []

            for tunnel in self.tunnels:
                tunnels_data.append((tunnel_id, tunnel[0]))
                tunnel_id += 1

            if tunnels_data:
                self.print_table('Active Tunnels', headers, *tunnels_data)
            else:
                self.print_warning("No active tunnels available.")

    def load(self):
        pass
