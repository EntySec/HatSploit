"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.module.basic import *


class HatSploitModule(Module):
    def __init__(self):
        super().__init__({
            'Category': "post",
            'Name': "Unix Shell Get PID",
            'Module': "post/unix/shell/getpid",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - module developer",
            ],
            'Description': "Get current session process id.",
            'Platform': OS_UNIX,
            'Rank': MEDIUM_RANK,
        })

        self.session = SessionOption('SESSION', None, "Session to run on.", True,
                                     platforms=[OS_UNIX],
                                     type='shell')

    def run(self):
        pid = self.session.session.send_command("printf $$", True).strip()

        if pid:
            self.print_information(f"PID: {pid}")
