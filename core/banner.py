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

from core.parser import parser
from core.config import config
from core.badges import badges

from external.colors_script import colors_script

class banner:
    def __init__(self):
        self.parser = parser()
        self.config = config()
        self.badges = badges()
        
        self.colors_script = colors_script()
        
    def print_random_banner(self):
        if os.path.exists(self.config.path_config['base_paths']['banners_path']):
            banners = list()
            all_banners = os.listdir(self.config.path_config['base_paths']['banners_path'])
            for banner in all_banners:
                banners.append(banner)
            if banners:
                banner = ""
                while not banner:
                    random_banner = random.randint(0, len(banners) - 1)
                    banner = self.colors_script.parse_colors_script(self.config.path_config['base_paths']['banners_path'] + banners[random_banner])
                self.badges.output_empty(self.badges.END + banner + self.badges.END)
            else:
                self.badges.output_warning("No banners detected.")
        else:
            self.badges.output_warning("No banners detected.")
