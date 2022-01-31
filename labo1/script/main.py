#!/usr/bin/env python3

__authors__ = ["Baptiste Coudray", "Quentin Berthet"]
__date__ = "15.02.2021"
__course__ = "Software Defined Networks"
__description__ = "Get VLAN info from switches"

import json
from telnetlib import Telnet
from ntc_templates.parse import parse_output
import switches
import re

# Labo1-correction don't work, so we use the DNS name
switches_host = [
    ("hepia.infolibre.ch", 21035),
    ("hepia.infolibre.ch", 21031),
    ("hepia.infolibre.ch", 21033),
    ("hepia.infolibre.ch", 21038),
]

if __name__ == '__main__':
    switches = switches.Switches([])
    for host, port in switches_host:
        with Telnet(host, port) as tn:
            tn.write(b"\r")
            tn.write(b"enable\r")
            tn.read_until(b"Password:", timeout=10)
            tn.write(b"iti\r")
            tn.write(b"terminal length 0\r")
            tn.write(b"show vlan\r")
            tn.write(b"show interfaces trunk\r")
            tn.write(b"exit\r")
            output = tn.read_until(match=f"#exit".encode("ascii")).decode("ascii")
            hostname = re.search(r"(\w+)#", output)
            tis = re.findall(r"(Gi\d/\d).*trunking", output)
            vlan_parsed = parse_output(platform="cisco_ios", command="show vlan", data=output)
            switches.add_switch(hostname.group(1), vlan_parsed, tis)
    with open("output.json", "w") as fp:
        json.dump(switches.to_dict(), fp, indent=2)
