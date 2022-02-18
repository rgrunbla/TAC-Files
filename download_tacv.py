#!/usr/bin/env nix-shell
#! nix-shell -i python3 -p python3Packages.requests

import os
import json
from pathlib import Path
import requests
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

token = os.environ.get('token')
retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"],
)
adapter = HTTPAdapter(max_retries=retry_strategy)

class EnhancedSession(requests.Session):
    def __init__(self, timeout=(3, 4)):
        self.timeout = timeout
        return super().__init__()

    def request(self, method, url, **kwargs):
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout
        return super().request(method, url, **kwargs)

def download_blacklist(session, hash_type, filename):
    elements = []
    lastIndexBlacklist = None
    iter = 0
    while True:
        url = f"https://portail.tacv.myservices-ingroupe.com/api/client/configuration/blacklist/tacv/{hash_type}/{iter}"
        answer = session.get(url, allow_redirects=True).json()
        if "elements" in answer:
            elements = elements + answer["elements"]
        if lastIndexBlacklist == None and "lastIndexBlacklist" in answer:
            lastIndexBlacklist = answer["lastIndexBlacklist"]
        iter += 5000
        if iter > lastIndexBlacklist:
            break
    data = {
        'elements': elements,
        'lastIndexBlacklist': lastIndexBlacklist
    }
    d = json.dumps(data, indent=2, sort_keys=True)
    with open(filename, 'w') as handler:
        handler.write(d)

session = EnhancedSession()
session.mount("https://", adapter)
session.mount("http://", adapter)
session.headers.update(
    {
        "Authorization": f"Bearer {token}"
    }
)


download_blacklist(session, 'dcc', "blacklist_qrcode_tacv.json")
download_blacklist(session, '2ddoc', "blacklist_2ddoc_tacv.json")