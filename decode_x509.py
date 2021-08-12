#!/usr/bin/env python3

import subprocess
import sys
import json
import base64
import tempfile

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <certificates.json>")
    exit(0)

filename = sys.argv[1]

with open(filename, 'r') as f:
    data = json.load(f)
    for key in data['certificatesDCC']:
        cert = base64.b64decode(base64.b64decode(data['certificatesDCC'][key]))
        cert_file = tempfile.NamedTemporaryFile(mode='w+b')
        cert_file.write(cert)
        cert_file.flush()
        cert_txt = subprocess.check_output(["openssl", "x509", "-text", "-inform", "der", "-noout", "-in", cert_file.name])
        print(cert_txt.decode('utf8'))

