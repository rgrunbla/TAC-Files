#!/usr/bin/env nix-shell
#! nix-shell -i python3 -p nix-update nix-prefetch-github python3Packages.requests python3Packages.protobuf

import json
import urllib.request
import os
import time
import requests

environ = os.environ

token = environ['token']
timeout = 5
headers = {
    'Authorization': 'Bearer ' + token
}
retry = 0
while True:
    if retry > 10:
        print("Error fetching hashes. Exiting")
        exit(-1)
    
    url = 'https://portail.tacv.myservices-ingroupe.com/api/client/configuration/rules/tacv'
    req = urllib.request.Request(url, headers=headers)
    r = urllib.request.urlopen(req)
    if r.getcode() != 200:
        print("Error trying to fetch rules. Retrying.")
        retry += 1
        time.sleep(5)
        continue
    else:
        break
rules = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
rule_hashes = sorted([rule['hash'] for rule in rules])
chunk_size = 100
data = []
for i in range(0, len(rule_hashes), chunk_size):
    hashes = rule_hashes[i:i+chunk_size]
    retry = 0
    while True:
        if retry > 10:
            print("Error fetching rules. Exiting.")
            exit(-1)
        r = requests.post('https://portail.tacv.myservices-ingroupe.com/api/client/configuration/rules/hashes/tacv', timeout=timeout, headers = headers, json = hashes)

        if r.status_code != 200:
            retry += 1
            time.sleep(5)
            continue
        else:
            break
    data.append(r.json())

print(json.dumps(data, indent=4, sort_keys=True))