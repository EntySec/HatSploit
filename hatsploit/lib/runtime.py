#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2022 EntySec
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
import sys

import traceback

from hatsploit.lib.config import Config
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.loot import Loot
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.modules import Modules
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.options import Options

from hatsploit.core.cli.badges import Badges
from hatsploit.core.base.loader import Loader


class Runtime:
    config = Config()
    jobs = Jobs()
    loot = Loot()
    sessions = Sessions()
    modules = Modules()
    payloads = Payloads()
    options = Options()

    badges = Badges()
    loader = Loader()

    def check(self):
        if not os.path.exists(self.config.path_config['root_path']):
            raise RuntimeError("HatSploit Framework is not installed!")

    def start(self):
        try:
            self.loader.load_all()
        except Exception as e:
            raise RuntimeError(f"An error occured: {str(e)}")

    def update(self):
        current_module = self.modules.get_current_module()
        current_payload = self.payloads.get_current_payload()

        self.jobs.stop_dead()
        self.sessions.close_dead()

        self.options.add_handler_options(current_module, current_payload)

    def catch(self, function, args=[]):
        try:
            function(*args)
            return True

        except (KeyboardInterrupt, EOFError):
            return True

        except RuntimeError as e:
            self.badges.print_error(str(e))

        except RuntimeWarning as w:
            self.badges.print_warning(str(w))

        except Exception as e:
            self.badges.print_error(f"An error occured: {str(e)}!")
            traceback.print_stack(file=sys.stdout)

        return False
