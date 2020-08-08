
import numpy as np
import math
import sys
import argparse
import json
import html
import requests
import os

prefix = "https://iiif.dl.itc.u-tokyo.ac.jp/omekac"
dir = "data"

def saveFile(id):
    data = requests.get(id).json()

    path = id.replace(prefix, dir)

    dirname = os.path.dirname(path)

    os.makedirs(dirname, exist_ok=True)

    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))

    return data

manifest = "https://iiif.dl.itc.u-tokyo.ac.jp/omekac/oa/collections/24/manifest.json"

m_data = saveFile(manifest)

canvases = m_data["sequences"][0]["canvases"]

for canvas in canvases:
    annoList = canvas["otherContent"][0]["@id"]

    saveFile(annoList)
