#!/usr/bin/env python3

#
# This plugin requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

import socket
from pyngrok import ngrok

from hatsploit.lib.plugin import Plugin


class HatSploitPlugin(Plugin):
    tunnels = {}
    handler = ngrok

    details = {
        'Name': "HatSploit Ngrok Implementation",
        'Plugin': "ngrok",
        'Authors': [
            'Ivan Nikolsky (enty8080) - plugin developer'
        ],
        'Description': "Manage ngrok service right from HatSploit."
    }

    usage = ""
    usage += "ngrok <option> [arguments]\n\n"
    usage += "  -l, --list               List all active tunnels.\n"
    usage += "  -o, --open <port>        Open tunnel for specified port.\n"
    usage += "  -c, --close <tunnel_id>  Close tunnel by its id.\n"
    usage += "  -a, --auth <token>       Authenticate ngrok API token.\n"

    commands = {
        'ngrok': {
            'ngrok': {
                'Description': "Manage ngrok service.",
                'Usage': usage,
                'MinArgs': 1
            }
        }
    }

    @staticmethod
    def parse_tunnel(tunnel):
        tunnel = tunnel.public_url.strip('tcp://').split(':')

        host = socket.gethostbyname(tunnel[0])
        port = tunnel[1]

        return host, port

    def ngrok(self, argc, argv):
        if argv[1] in ['-o', '--open']:
            if argc < 2:
                self.print_usage(self.commands['ngrok']['ngrok']['Usage'])
            else:
                try:
                    self.print_process(f"Opening tunnel for port {argv[2]}...")

                    tunnel = self.handler.connect(int(argv[2]), "tcp")
                    data = self.parse_tunnel(tunnel)

                    route = f"127.0.0.1:{argv[2]} -> {data[0]}:{data[1]}"

                    self.print_success(f"Tunnel opened ({route})!")
                    self.tunnels.append([route, tunnel])
                except Exception:
                    self.print_error(f"Failed to open tunnel port {argv[2]}!")

        elif argv[1] in ['-a', '--auth']:
            if argc < 2:
                self.print_usage(self.commands['ngrok']['ngrok']['Usage'])
            else:
                self.handler.set_auth_token(argv[2])

        elif argv[1] in ['-c', '--close']:
            if argc < 2:
                self.print_usage(self.commands['ngrok']['ngrok']['Usage'])
            else:
                try:
                    self.print_process(f"Closing tunnel {argv[2]}...")

                    self.handler.disconnect(self.tunnels[int(argv[2])][1])
                    self.tunnels.remove(self.tunnels[int(argv[2])][0])
                except Exception:
                    self.print_error(f"Invalid tunnel given!")

        elif argv[1] in ['-l', '--list']:
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

    def run(self):
        pass
