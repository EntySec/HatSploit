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

import curses
import random
import time

from core.lib.plugin import Plugin


class HatSploitPlugin(Plugin):
    details = {
        'Name': "sky",
        'Authors': [
            'enty8080'
        ],
        'Description': "Sky plugin for HatSploit.",
        'Comments': [
            ''
        ]
    }

    commands = {
        'sky': {
            'sky': {
                'Description': "Show sky.",
                'Usage': "sky",
                'MinArgs': 0
            }
        }
    }

    @staticmethod
    def generateSky(y, x, req):
	      ysky = []
	      xsky = []

	      for iy in range(0, y):
		        for ix in range(0, x):
			          if random.uniform(0, 1) < req:
				            xsky.append(["✱"])
			          else:
				            xsky.append([" "])

		        ysky.append(xsky)
		        xsky = []

	      return ysky

    @staticmethod
    def animateSky(sky):
	      for i in sky:
		        for x in i:
			          if x[0] == "✱" and random.uniform(0, 1) < 0.0015:
				            x[0] = "⋆"
			          elif x[0] == "⋆":
				            x[0] = "✱"

    @staticmethod
    def renderSky(screen, sky):
	      screen.clear()
		    for i in sky:
			      for x in i:
				        screen.addstr(x[0])
			          screen.addstr("\n")
	      screen.refresh()

    def sky(self, argc, argv):
        try:
		        screen = curses.initscr()
		        size = screen.getmaxyx()
		        sky = self.generateSky(size[0]-1, size[1]-1, 0.025)

		        while True:
			      if size[0] != screen.getmaxyx()[0] and size[1] != screen.getmaxyx()[1]:
				        size = screen.getmaxyx()
				        sky = self.generateSky(size[0]-1, size[1]-1, 0.05)

			      self.animateSky(sky)
			      self.renderSky(screen, sky)
			      time.sleep(1)

		        curses.endwin()
	      except (KeyboardInterrupt, EOFError):
		        curses.endwin()
	      except Exception:
		        curses.endwin()

    def run(self):
        self.output_information("Use " + self.GREEN + "sky" + self.END + " to view sky.")
