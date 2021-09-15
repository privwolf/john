#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET

def process_file(filename):
    try:
        fd = open(filename, "rb")
    except IOError:
        e = sys.exc_info()[1]
        sys.stderr.write("%s\n" % str(e))
        return

    tree = ET.parse(filename)
    root = tree.getroot()

    for user in root.findall('system/user'):
        username = user.find('name').text
        if user.find('bcrypt-hash') is not None:
            sys.stdout.write("%s:%s\n" % (username, user.find('bcrypt-hash').text))
        elif user.find('md5-hash') is not None:
            sys.stdout.write("%s:%s\n" % (username, user.find('md5-hash').text))
        elif user.find('password') is not None:
            sys.stdout.write("%s:%s\n" % (username, user.find('password').text))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s <pfSense/OPNsense config.xml>\n" % sys.argv[0])
        sys.exit(-1)

    for i in range(1, len(sys.argv)):
        process_file(sys.argv[i])
