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


class SSLTools:
    @staticmethod
    def dump_pubkey(pubkey):
        TYPE_PEM = OpenSSL.crypto.FILETYPE_PEM
        return OpenSSL.crypto.dump_privatekey(TYPE_PEM, pubkey)

    @staticmethod
    def dump_certificate(certificate):
        TYPE_PEM = OpenSSL.crypto.FILETYPE_PEM
        return OpenSSL.crypto.dump_certificate_request(TYPE_PEM, certificate)

    @staticmethod
    def generate_pubkey():
        TYPE_RSA = OpenSSL.crypto.TYPE_RSA

        pubkey = OpenSSL.crypto.PKey()
        pubkey.generate_type(TYPE_RSA, 2048)

        return pubkey

    @staticmethod
    def generate_certificate(pubkey, nodename='HatSploit', country='US', state='HatSploit',
                             location='HatSploit', organization='HatSploit', unit='HatSploit'):
        certificate = OpenSSL.crypto.X509Req()
        certificate.get_subject().CN = nodename
        certificate.get_subject().countryName = country
        certificate.get_subject().stateOrProvinceName = state
        certificate.get_subject().localityName = location
        certificate.get_subject().organizationName = organization
        certificate.get_subject().organizationalUnitName = unit

        x509_extensions = ([
            OpenSSL.crypto.X509Extension(b"keyUsage", False, b"Digital Signature, Non Repudiation, Key Encipherment"),
            OpenSSL.crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE"),
        ])

        certificate.add_extensions(x509_extensions)

        certificate.set_pubkey(pubkey)
        certificate.sign(pubkey, "sha1")

        return certificate
