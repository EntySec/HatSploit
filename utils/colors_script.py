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

from core.badges import badges

class colors_script:
    def __init__(self):
        self.badges = badges()
        
        self.script_extension = "colors"
        
        self.commands = {
            '%black': self.badges.BLACK,
            '%red': self.badges.RED,
            '%green': self.badges.GREEN,
            '%yellow': self.badges.YELLOW,
            '%blue': self.badges.BLUE,
            '%purple': self.badges.PURPLE,
            '%cyan': self.badges.CYAN,
            '%white': self.badges.WHITE,

            '%end': self.badges.END,
            '%bold': self.badges.BOLD,
            '%dark': self.badges.DARK,
            '%bent': self.badges.BENT,
            '%line': self.badges.LINE,
            '%twink': self.badges.TWINK,
            '%back': self.badges.BACK,
            
            '%remove': self.badges.REMOVE,
            '%clear': self.badges.CLEAR,
            
            '%newline': self.badges.NEWLINE
        }
        
    def _read_file_lines(self, path):
        lines = list()
        with open(path) as file:
            for line in file:
                if line and line[0:8] != "%comment" and not line.isspace():
                    lines.append(line)
        return lines

    def _reverse_read_lines(self, path):
        lines = list()
        with open(path) as file:
            for line in reversed(list(file)):
                lines.append(line)
        return lines

    def _reversed_find_last_commands(self, lines):
        buffer_commands = list()
        for line in lines:
            buffer_line = line
            for command in self.commands.keys():
                if command in buffer_line:
                    buffer_line = buffer_line.replace(command, " ")
            if buffer_line.isspace():
                buffer_commands.append(line.strip())
            else:
                break
        buffer_commands.reverse()
        return buffer_commands
        
    def _remove_empty_lines(self, lines):
        line_id = -1
        for _ in range(len(lines)):
            buffer_line = lines[line_id]
            for command in self.commands.keys():
                if command in buffer_line:
                    buffer_line = buffer_line.replace(command, " ")
            if buffer_line.isspace():
                lines.pop(line_id)
        return lines

    def parse_colors_script(self, path):
        result = ""
        lines = self._read_file_lines(path)
        reversed_lines = self._reverse_read_lines(path)
        last_commands = self._reversed_find_last_commands(reversed_lines)
        last_commands = "".join(map(str, last_commands))
        lines = self._remove_empty_lines(lines)
        lines[-1] = lines[-1].strip('\n') + last_commands
        if path.endswith(self.script_extension):
            try:
                buffer_commands = ""
                for line in lines:
                    buffer_line = line
                    for command in self.commands.keys():
                        if command in buffer_line:
                            buffer_line = buffer_line.replace(command, " ")
                    if buffer_line.isspace():
                        buffer_commands += line.strip()
                    else:
                        line = buffer_commands + line
                        buffer_commands = ""
                        for command in self.commands.keys():
                            line = line.partition('%comment')[0]
                            line = line.replace(command, self.commands[command])
                        result += line
                return result
            except Exception:
                return None
        else:
            return None

    def compile_colors_script(self, path, outfile='a.out'):
        result = self.parse_colors_script(path)
        if result:
            output = open(outfile, 'wb')
            output.write(result.encode())
            output.close()
