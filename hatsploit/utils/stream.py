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

from hatsploit.core.cli.badges import Badges


class Streamer:
    def __init__(self, path, image):
        self.path = path
        self.image = image

        self.badges = Badges()
        self.streamer = """
<html>
<head>
<META HTTP-EQUIV="PRAGMA" CONTENT="NO-CACHE">
<META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">
<title>HatSploit Framework - Streamer</title>

<script language="javascript">
function updateStatus(msg) {
    var status = document.getElementById("status");
    status.innerText = msg;
}

function noImage() {
  document.getElementById("streamer").style = "display:none";
  updateStatus("Waiting...");
}

var i = 0;

function updateFrame() {
  var img = document.getElementById("streamer");
  img.src = """ + self.image + """ + i;
  img.style = "display:";
  updateStatus("Playing...");
  i++;
}

setInterval(function() {
  updateFrame();
}, 25);
</script>
</head>

<body>
<noscript>
    <h2><font color="red">Error: You need Javascript enabled to watch the stream.</font></h2>
</noscript>

<pre>
Time   : #{::Time.now}
Status : <span id="status"></span>
</pre>

<br>
<img onerror="noImage()" id="streamer">
</body>
</html>
        """

    def create(self):
        if os.path.isdir(self.path):
            self.path += '/streamer.html'

        if os.access(os.path.split(self.path)[0], os.W_OK):
            with open(self.path, 'w') as f:
                f.write(self.streamer)
            return True

        self.badges.print_error("Failed to create streamer!")
        return False

    def stream(self):
        self.badges.print_process("Streaming...")
        os.system(f'open {self.path} &')


class StreamClient:
    @staticmethod
    def open_stream(path, image):
        return Streamer(path, image)
