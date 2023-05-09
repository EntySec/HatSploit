"""
MIT License

Copyright (c) 2020-2023 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

from hatsploit.lib.commands import Commands


class RPC(object):
    """ Subclass of hatsploit.core.utils module.

    This subclass of hatsploit.core.utils module is intended for providing
    an implementation of a remote procedure calls for HatSploit.
    """

    def __init__(self, host: str, port: int = 1006) -> None:
        """ Initialize RPC server.

        :param str host: host to start RPC server on
        :param int port: port to start RPC server on
        """

        self.host = host
        self.port = int(port)

        self.commands = Commands()

    def run(self) -> None:
        """ Run RPC server.

        :return None: None
        """

        rpc = SimpleJSONRPCServer((self.host, self.port))
        commands = self.commands.get_commands()

        for command in commands:
            name = command
            command = commands[command]

            if hasattr(command, 'rpc'):
                rpc.register_function(command.rpc, name)

        rpc.serve_forever()
