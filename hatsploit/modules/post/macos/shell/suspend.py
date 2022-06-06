"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.module import Module
from hatsploit.lib.sessions import Sessions


class HatSploitModule(Module, Sessions):
    details = {
        "Category": "post",
        "Name": "macOS Shell Suspend",
        "Module": "post/macos/shell/suspend",
        "Authors": ["Ivan Nikolsky (enty8080) - module developer"],
        "Description": "Suspend macOS through shell.",
        "Platform": "macos",
        "Rank": "medium",
    }

    options = {
        "SESSION": {
            "Description": "Session to run on.",
            "Value": None,
            "Type": {"session": {"Platforms": ["macos"], "Type": "shell"}},
            "Required": True,
        }
    }

    def run(self):
        session = self.parse_options(self.options)
        session = self.get_session(session)

        if session:
            session.send_command(
                "/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend"
            )
