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
import shutil

from setuptools import setup, find_packages

setup(name='hatsploit',
      version='1.0',
      description='Modular penetration testing platform that enables you to write, test, and execute exploit code.',
      url='http://github.com/EntySec/HatSploit',
      author='EntySec',
      author_email='entysec@gmail.com',
      license='MIT',
      python_requires='>=3.7.0',
      packages=find_packages(),
      entry_points={
          "console_scripts": [
                "hsf = hatsploit.hsf:main"
          ]
      },
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.8",
      ],
      install_requires=[
          'pyyaml',
          'requests',
          'scapy',
          'paramiko'
      ],
      include_package_data=True,
      zip_safe=False
)

home = os.path.expanduser('~') + '/.hsf'

if not os.path.exists(home):
    with open('config/path_config.yml', 'r') as f:
        config = f.read().replace('HOME', home)

    with open('config/path_config.yml', 'w') as f:
        f.write(config)

    os.mkdir(home)
    shutil.copytree('config', f'{home}/config')

    shutil.copytree('modules', f'{home}/modules')
    shutil.copytree('commands', f'{home}/commands')
    shutil.copytree('payloads', f'{home}/payloads')
    shutil.copytree('plugins', f'{home}/plugins')

    shutil.copytree('data', f'{home}/data')
    shutil.copy('TERMS_OF_SERVICE.md', f'{home}/TERMS_OF_SERVICE.md')
