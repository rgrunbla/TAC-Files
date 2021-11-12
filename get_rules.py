#!/usr/bin/env python3

import json
import requests
import os

environ = os.environ

token = environ['token']
timeout = 10
headers = {
    'Authorization': 'Bearer ' + token
}

retry = 0
while True:
    if retry > 10:
        print("Error fetching hashes. Exiting")
        exit(-1)
    
    r = requests.get('https://portail.tacv.myservices-ingroupe.com/api/client/configuration/rules/tacv', timeout=timeout, headers = headers)

    if r.status_code != 200:
        # Error trying to fetch rules. Retrying.
        retry += 1
        continue
    else:
        break

rules = r.json()
rule_hashes = [rule['hash'] for rule in rules]

retry = 0
while True:
    if retry > 10:
        print("Error fetching rules. Exiting.")
        exit(-1)

    r = requests.post('https://portail.tacv.myservices-ingroupe.com/api/client/configuration/rules/hashes/tacv', timeout=timeout, headers = headers, json = rule_hashes)

    if r.status_code != 200:
        retry += 1
        continue
    else:
        break

print(json.dumps(r.json(), indent=4, sort_keys=True))
