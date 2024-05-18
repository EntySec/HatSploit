"""
MIT License

Copyright (c) 2020-2024 EntySec

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

import os
import sys
import traceback

from typing import Callable, Any, Union

from badges import Badges

from hatsploit.core.base.loader import Loader
from hatsploit.lib.config import Config
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.loot import Loot
from hatsploit.lib.sessions import Sessions


class Runtime(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    an API interface for HatSploit runtime handler.
    """

    def __init__(self) -> None:
        super().__init__()

        self.config = Config()
        self.jobs = Jobs()
        self.loot = Loot()
        self.sessions = Sessions()

        self.badges = Badges()
        self.loader = Loader()

    def check(self) -> None:
        """ Check if HatSploit is set up correctly and
        fix it in case if problems.

        :return None: None
        :raises RuntimeError: with trailing error message
        """

        if os.path.exists(self.config.path_config['root_path']):
            workspace = self.config.path_config['user_path']
            loot = self.config.path_config['loot_path']

            if not os.path.isdir(workspace):
                os.mkdir(workspace)

            if not os.path.isdir(loot):
                self.loot.create_loot()

        else:
            raise RuntimeError("HatSploit Framework is not installed!")

    def start(self, build_base: bool = False, silent: bool = False) -> None:
        """ Start HatSploit Framework and load all databases.

        :param bool build_base: True if you want to build
        base databases else False
        :param bool silent: display loading message if True
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        try:
            self.loader.load_all(build_base, silent)
        except Exception as e:
            raise RuntimeError(f"An error occured: {str(e)}")

    def update(self) -> None:
        """ Update HatSploit states: stop dead jobs,
        close dead sessions.

        :return None: None
        """

        self.jobs.stop_dead()
        self.sessions.close_dead()

    def catch(self, target: Callable[..., Any], args: list = []) -> Union[Any, None, Exception]:
        """ Catch exception and format error message.

        :param Callable[..., Any] target: target function
        :param list args: extra target function arguments
        :return Union[Any, None, Exception]: target function return value, None
        in case of KeyboardInterrupt/EOFError or Exception in case of exception
        """

        try:
            return target(*args)

        except (KeyboardInterrupt, EOFError):
            return

        except RuntimeError as e:
            self.badges.print_error(str(e))

        except RuntimeWarning as w:
            self.badges.print_warning(str(w))

        except Exception as e:
            self.badges.print_error(f"An error occurred: {str(e)}!")
            traceback.print_stack(file=sys.stdout)

        return Exception
