"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

import shlex

from badges.cmd import Command
from hatsploit.lib.ui.show import Show

from hatsploit.lib.ui.modules import Modules
from hatsploit.lib.ui.payloads import Payloads
from hatsploit.lib.ui.encoders import Encoders
from hatsploit.lib.ui.plugins import Plugins


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "core",
            'Name': "search",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Search payloads, modules and plugins.",
            'MinArgs': 1,
            'Options': [
                (
                    ('keyword',),
                    {
                        'help': 'Keyword to search for.',
                    }
                ),
                (
                    ('-f', '--filter'),
                    {
                        'help': 'Filter search result separated by comma ('
                                'filters: CVE; EDB; URL)',
                    }
                ),
            ],
            'Examples': [
                "search -f CVE:2013-7389 dlink",
                "search -f CVE:2013-7389 ''"
                "search apple_ios"
            ]
        })

        self.show = Show()
        self.modules = Modules()
        self.payloads = Payloads()
        self.encoders = Encoders()
        self.plugins = Plugins()

    def run(self, args):
        filter = {}

        if args.keyword:
            filter.update({
                'BaseName': args.keyword,
            })

        if args.filter:
            for query in args.filter.split(','):
                query = shlex.split(query)[0]
                query = query.split(':')

                if len(query) != 2:
                    continue

                if query[0] in ['CVE', 'EDB', 'URL']:
                    filter['References'] = {query[0]: query[1]}

        self.show.show_search_modules(
            self.modules.get_modules(query=filter), args.keyword)
        self.show.show_search_payloads(
            self.payloads.get_payloads(query=filter), args.keyword)
        self.show.show_search_encoders(
            self.encoders.get_encoders(query=filter), args.keyword)
        self.show.show_search_plugins(
            self.plugins.get_plugins(query=filter), args.keyword)
