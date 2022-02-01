#!/usr/bin/env nix-shell
#! nix-shell -i python3 -p nix-update nix-prefetch-github python3Packages.requests python3Packages.protobuf

import json
from io import BytesIO
import requests
import gzip    
from proto import hashes_pb2

BASE_URL="https://app-static.tousanticovid.gouv.fr/"
VERSIONED_PATH="json/version-37/"
VERSIONED_SERVER_URL=BASE_URL+VERSIONED_PATH

MAINTENANCE_BASE_URL="https://app.tousanticovid.gouv.fr/"
MAINTENANCE_FOLDER="maintenance/"
MAINTENANCE_FILENAME="info-maintenance-v2.json"
MAINTENANCE_URL=MAINTENANCE_BASE_URL+MAINTENANCE_FOLDER+MAINTENANCE_FILENAME

VACCINATION_ASSET_ZIP_GEOLOC_FILE_PATH="VaccinationCenter/zip-geoloc.json"
VACCINATION_CENTER_FILENAME="centres-vaccination.json"
VACCINATION_CENTER_LAST_UPDATE_FILENAME="lastUpdate.json"
VACCINATION_FOLDER="/infos/dep/"
VACCINATION_URL=BASE_URL+VACCINATION_FOLDER
VACCINATION_CENTER_SUFFIX="-centers.json"
VACCINATION_LAST_UPDATE_SUFFIX="-lastUpdate.json"

KEY_FIGURES_NATIONAL_SUFFIX="nat"
KEY_FIGURES_LOCAL_FILENAME_TEMPLATE="key-figures-%s.pb.gz"
KEY_FIGURES_URL=BASE_URL+"infos/v2%s/$LOCAL_FILENAME_TEMPLATE"

MORE_KEY_FIGURES_FOLDER="MoreKeyFigures/"
MORE_KEY_FIGURES_URL=VERSIONED_SERVER_URL+MORE_KEY_FIGURES_FOLDER
MORE_KEY_FIGURES_FILE_PREFIX="morekeyfigures-"

ATTESTATIONS_FILENAME="form.json"
ATTESTATIONS_FOLDER="Attestations/"
ATTESTATIONS_URL=VERSIONED_SERVER_URL+ATTESTATIONS_FOLDER+ATTESTATIONS_FILENAME
ATTESTATIONS_ASSET_FILE_PATH=ATTESTATIONS_FOLDER+ATTESTATIONS_FILENAME

INFO_CENTER_FOLDER="InfoCenter/"
INFO_CENTER_URL=VERSIONED_SERVER_URL+INFO_CENTER_FOLDER
INFO_CENTER_LOCAL_FALLBACK_FILENAME="info-labels-en.json"
INFO_CENTER_STRINGS_PREFIX="info-labels-"
INFO_CENTER_TAGS_PREFIX="info-tags"
INFO_CENTER_INFOS_PREFIX="info-center"
INFO_CENTER_LAST_UPDATE_PREFIX="info-center-lastupdate"

LINKS_FOLDER="Links/"
LINKS_URL=VERSIONED_SERVER_URL+LINKS_FOLDER
LINKS_FILE_PREFIX="links-"

PRIVACY_FOLDER="Privacy/"
PRIVACY_URL=VERSIONED_SERVER_URL+PRIVACY_FOLDER
PRIVACY_FILE_PREFIX="privacy-"

RISKS_FILENAME="risks.json"
RISKS_FOLDER="Risks/"
RISKS_URL=VERSIONED_SERVER_URL+RISKS_FOLDER+RISKS_FILENAME
RISKS_ASSET_FILE_PATH=RISKS_FOLDER+RISKS_FILENAME

LABELS_FOLDER="Strings/"
LABELS_URL=VERSIONED_SERVER_URL+LABELS_FOLDER
LABELS_FILE_PREFIX="strings-"

WALLET_FOLDER="Wallet/"
WALLET_URL=VERSIONED_SERVER_URL+WALLET_FOLDER

DCC_CERTIFICATES_FOLDER="Certs/"
DCC_CERTIFICATES_URL=VERSIONED_SERVER_URL+DCC_CERTIFICATES_FOLDER

CONFIG_FOLDER="Config/"
CONFIG_LOCAL_FILENAME="config.json"
CONFIG_URL=VERSIONED_SERVER_URL+CONFIG_FOLDER+CONFIG_LOCAL_FILENAME

CALIBRATION_FOLDER="Calibration/"
CALIBRATION_LOCAL_FILENAME="calibrationBle.json"
CALIBRATION_URL=VERSIONED_SERVER_URL+CALIBRATION_FOLDER+CALIBRATION_LOCAL_FILENAME

BLACKLIST_FOLDER="json/blacklist/v2/CertList/"
BLACKLIST_DCC_ITERATION_PATH_TEMPLATE="dcc/%d/"
BLACKLIST_DCC_FILENAME="certlist.pb.gz"
BLACKLIST_DCC_URL=BASE_URL+BLACKLIST_FOLDER+BLACKLIST_DCC_ITERATION_PATH_TEMPLATE+BLACKLIST_DCC_FILENAME

BLACKLIST_2DDOC_ITERATION_PATH_TEMPLATE="2ddoc/%d/"
BLACKLIST_2DDOC_FILENAME="2ddoc_list.pb.gz"
BLACKLIST_2DDOC_URL=BASE_URL+BLACKLIST_FOLDER+BLACKLIST_2DDOC_ITERATION_PATH_TEMPLATE+BLACKLIST_2DDOC_FILENAME


URLS_PB = {
"blacklist_2ddoc.json": BLACKLIST_2DDOC_URL,
"blacklist_qrcode.json": BLACKLIST_DCC_URL
}

URLS = {
"calibrationBle.json": CALIBRATION_URL,
"config.json": CONFIG_URL
}

timeout = 10

# Downloading Blacklists
for filename, url in URLS_PB.items():
    out = []
    i = 0
    while True:
        print(f"Downloading chunk {i} : {url % i}")
        try:
            response = requests.get(url % i, timeout=timeout)
        except requests.exceptions.ReadTimeout:
            break

        if response.status_code != 200:
            break
        gzip_file = BytesIO(response.content)
        file = gzip.GzipFile(fileobj=gzip_file)
        hashes = hashes_pb2.Hashes()        
        hashes.ParseFromString(file.read())
        out += hashes.hash
        i+=1
    with open(filename, "w") as f:
        f.write(json.dumps(out, indent=2, sort_keys=True))

URLS = {
"calibrationBle.json": CALIBRATION_URL,
"config.json": CONFIG_URL
}

# Downloading various files
for filename, url in URLS.items():
    print(f"Downloading {url}")
    try:
        response = requests.get(url, timeout=timeout)
    except requests.exceptions.ReadTimeout:
       break
        
    if response.status_code != 200:
        continue
    with open(filename, "w") as f:
        f.write(json.dumps(response.json(), indent=2, sort_keys=True))
