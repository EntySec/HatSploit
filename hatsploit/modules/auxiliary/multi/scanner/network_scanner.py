#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

import scapy.all

from hatsploit.base.module import Module


class HatSploitModule(Module):
    details = {
        'Name': "Network Scanner",
        'Module': "auxiliary/multi/scanner/network_scanner",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Scan local network.",
        'Comments': [
            ''
        ],
        'Platform': "multi",
        'Risk': "low"
    }

    options = {
        'RANGE': {
            'Description': "IP range.",
            'Value': "192.168.1.1/24",
            'Type': "ipv4_range",
            'Required': True
        },
        'TIMEOUT': {
            'Description': "Timeout to scan.",
            'Value': 10,
            'Type': "number",
            'Required': True
        }
    }

    def run(self):
        ip_range, timeout = self.parse_options(self.options)

        self.output_process("Scanning local network...")

        try:
            arp = scapy.all.ARP(pdst=ip_range)
            ether = scapy.all.Ether(dst="ff:ff:ff:ff:ff:ff")
            result = scapy.all.srp(ether / arp, timeout=float(timeout), verbose=False)[0]

            if len(result) > 0:
                net_data = list()
                headers = ("Host", "MAC")
                for _, received in result:
                    net_data.append((received.psrc, received.hwsrc))
                self.print_table("Network Devices", headers, *net_data)
            else:
                self.output_warning("No hosts detected in local network.")
        except Exception:
            self.output_error("Failed to scan local network!")
