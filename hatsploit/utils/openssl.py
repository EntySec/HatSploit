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

import ssl
import OpenSSL

from hatsploit.lib.loot import Loot


class OpenSSLTools:
    loot = Loot().loot

    def wrap_client(self, client, protocol=ssl.PROTOCOL_TLS, nodename='HatSploit',
                    country='US', state='HatSploit', location='HatSploit',
                    organization='HatSploit', unit='HatSploit'):
        key = self.generate_key()
        cert = self.generate_cert(
            key,
            nodename=nodename,
            country=country,
            state=state,
            location=location,
            organization=organization,
            unit=unit
        )

        keyfile = self.loot + 'hatsploit.key'
        certfile = self.loot + 'hatsploit.crt'

        self.write_key(key, keyfile)
        self.write_cert(cert, certfile)

        return ssl.wrap_socket(
            client,
            server_side=True,
            certfile=keyfile,
            keyfile=certfile,
            ssl_version=protocol
        )

    def write_key(self, key, filename):
        with open(filename, 'w') as f:
            f.write(self.dump_key(key))

    def write_cert(self, cert, filename):
        with open(filename, 'w') as f:
            f.write(self.dump_cert(cert))

    @staticmethod
    def dump_key(key):
        TYPE_PEM = OpenSSL.crypto.FILETYPE_PEM
        return OpenSSL.crypto.dump_privatekey(TYPE_PEM, key)

    @staticmethod
    def dump_cert(cert):
        TYPE_PEM = OpenSSL.crypto.FILETYPE_PEM
        return OpenSSL.crypto.dump_certificate_request(TYPE_PEM, cert)

    @staticmethod
    def generate_key():
        TYPE_RSA = OpenSSL.crypto.TYPE_RSA

        key = OpenSSL.crypto.PKey()
        key.generate_key(TYPE_RSA, 2048)

        return key

    @staticmethod
    def generate_cert(key, nodename='HatSploit', country='US', state='HatSploit',
                      location='HatSploit', organization='HatSploit', unit='HatSploit'):
        cert = OpenSSL.crypto.X509Req()
        cert.get_subject().CN = nodename
        cert.get_subject().countryName = country
        cert.get_subject().stateOrProvinceName = state
        cert.get_subject().localityName = location
        cert.get_subject().organizationName = organization
        cert.get_subject().organizationalUnitName = unit

        x509_extensions = ([
            OpenSSL.crypto.X509Extension(b"keyUsage", False, b"Digital Signature, Non Repudiation, Key Encipherment"),
            OpenSSL.crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE"),
        ])

        cert.add_extensions(x509_extensions)

        cert.set_pubkey(key)
        cert.sign(key, "sha1")

        return cert
