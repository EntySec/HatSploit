"""
This plugin requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command
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

        self.commands = [
            Command({
                'Name': 'ngrok',
                'Description': "Manage ngrok service.",
                'MinArgs': 1,
                'Options': [
                    (
                        ('-l', '--list'),
                        {
                            'help': "List all active tunnels.",
                            'action': 'store_true'
                        }
                    ),
                    (
                        ('-o', '--open'),
                        {
                            'help': "Open tunnel for specified port.",
                            'metavar': 'PORT',
                            'type': int,
                        }
                    ),
                    (
                        ('-c', '--close'),
                        {
                            'help': "Close active tunnel by ID.",
                            'metavar': 'ID',
                            'type': int
                        }
                    ),
                    (
                        ('-a', '--auth'),
                        {
                            'help': "Authenticate ngrok API by token.",
                            'metavar': 'TOKEN',
                        }
                    )
                ]
            })
        ]

        self.tunnels = []
        self.handler = ngrok

    @staticmethod
    def parse_tunnel(tunnel):
        tunnel = tunnel.public_url.strip('tcp://').split(':')

        host = tunnel[0]
        port = tunnel[1]

        return host, port

    def ngrok(self, args):
        if args.open:
            try:
                self.print_process(f"Opening tunnel for port {str(args.open)}...")

                tunnel = self.handler.connect(args.open, "tcp")
                data = self.parse_tunnel(tunnel)

                route = f"127.0.0.1:{str(args.open)} -> {data[0]}:{data[1]}"

                self.print_success(f"Tunnel opened ({route})!")
                self.tunnels.append([route, tunnel])

            except Exception:
                self.print_error(f"Failed to open tunnel port {tr(args.open)}!")

        elif args.auth:
            self.handler.set_auth_token(args.auth)

        elif args.close is not None:
            try:
                self.print_process(f"Closing tunnel {str(args.close)}...")

                self.handler.disconnect(self.tunnels[args.close][1])
                self.tunnels.pop(args.close)

            except Exception:
                self.print_error(f"Invalid tunnel ID given!")

        elif args.list:
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
        banner = r"""%yellow
                             __  
     ____  ____ __________  / /__
    / __ \/ __ `/ ___/ __ \/ //_/
   / / / / /_/ / /  / /_/ / ,<   
  /_/ /_/\__, /_/   \____/_/|_|  
        /____/%end
"""

        self.print_empty(banner)
        self.print_information("Use %greenngrok%end to invoke ngrok.")
