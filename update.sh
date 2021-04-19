#!/bin/bash

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

I="\033[1;77m[i] \033[0m"
G="\033[1;34m[*] \033[0m"
S="\033[1;32m[+] \033[0m"
E="\033[1;31m[-] \033[0m"
P="\033[1;77m[>] \033[0m"

while [[ $(sudo -n id -u 2>&1) != 0 ]]; do
    {
        sudo -v -p "$(echo -e -n $P)Password for $(whoami): " 
    } &> /dev/null
done

echo -e $G"Updating HatSploit Framework..."

if [[ -f /data/data/com.termux/files/usr/bin/hsf ]]; then
    update=true
else
    if [[ -f /usr/local/bin/hsf ]]; then
        update=true
    else
        if [[ -f /usr/bin/hsf ]]; then
            update=true
        else
            update=false
        fi
    fi
fi

{
    sudo rm -rf /opt/hsf
    sudo rm /usr/local/bin/hsf
    sudo rm /data/data/com.termux/files/usr/bin/hsf
    git clone https://github.com/EntySec/HatSploit.git /opt/hsf
    if [[ $update ]]; then
        cd /opt/hsf/hsf
        sudo chmod +x install.sh
        sudo ./install.sh
    fi
} &> /dev/null

if [[ ! -d /opt/hsf ]]; then
    echo -e $E"Installation failed!"
    exit 1
fi

echo -e $S"Successfully updated!"
exit 0
