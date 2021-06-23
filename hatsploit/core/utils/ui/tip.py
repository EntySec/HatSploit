#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os
import random

from hatsploit.core.base.config import Config
from hatsploit.core.cli.badges import Badges
from hatsploit.core.cli.colors import Colors
from hatsploit.core.cli.parser import Parser
from hatsploit.core.utils.ui.colors_script import ColorsScript


class Tip:
    def __init__(self):
        self.parser = Parser()
        self.config = Config()
        self.badges = Badges()
        self.colors = Colors()

        self.colors_script = ColorsScript()

    def print_random_tip(self):
        if os.path.exists(self.config.path_config['tips_path']):
            tips = list()
            all_tips = os.listdir(self.config.path_config['tips_path'])
            for tip in all_tips:
                tips.append(tip)
            if tips:
                tip = ""
                while not tip:
                    random_tip = random.randint(0, len(tips) - 1)
                    tip = self.colors_script.parse_colors_script(
                        self.config.path_config['tips_path'] + tips[random_tip])
                self.badges.output_empty(self.colors.END + "HatSploit Tip: " + tip + self.colors.END)
            else:
                self.badges.output_warning("No tips detected.")
        else:
            self.badges.output_warning("No tips detected.")
