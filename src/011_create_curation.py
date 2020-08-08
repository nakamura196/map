
import numpy as np
import math
import sys
import argparse
import json
import html
import requests
import os
from bs4 import BeautifulSoup

title = "大明地理之図"
legend = "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/toyo.tif/20764,21600,5248,1568/1200,/0/default.jpg"
curation_id = "https://nakamura196.github.io/map/curation/test.json"

iconMap = {
    "道額" : "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/toyo.tif/25490,21697,277,457/30,60/0/default.jpg#xy=15,30",
    "五嶺": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/toyo.tif/23200,21684,380,244/60,30/0/default.jpg#xy=30,15",
    "五嶽": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/toyo.tif/23588,21668,400,260/60,30/0/default.jpg#xy=30,15",
    "五山" : "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/toyo.tif/23052,21656,156,332/30,60/0/default.jpg#xy=15,30"
}

manifest = "https://nakamura196.github.io/map/iiif/main/manifest.json"

with open('data/oa/items/6063/annolist.json') as f:
    df = json.load(f)

resources = df["resources"]

members = []

for i in range(len(resources)):
    index = str(i + 1)

    resource = resources[i]

    canvas = resource["on"][0]["full"]
    xywh = resource["on"][0]["selector"]["default"]["value"]

    xywhSplitTmp = xywh.split(",")



    memberId = canvas + "#" + xywh
    text = resource["resource"][0]["chars"]
    
    cleantext = BeautifulSoup(text, "lxml").text

    splitTmp = cleantext.replace("]", "[").split("[")

    label = splitTmp[0]
    種類 = splitTmp[1]


    icon = iconMap[種類]

    metadata = [
        {
            "value": [
            {
                "motivation": "sc:painting",
                "resource": {
                "chars": label,
                "@type": "cnt:ContentAsText",
                "format": "text/html",
                "marker": {
                    "@id": icon,
                    "@type": "dctypes:Image"
                }
                },
                "@id": memberId+"_",
                "on": memberId,
                "@type": "oa:Annotation"
            }
            ],
            "label": "Annotation"
        },
        {
            "value": 種類,
            "label": "種類"
        }
    ]

    member = {
          "label": "Marker "+index,
          "@type": "sc:Canvas",
          "metadata": metadata,
          "@id": memberId
        }

    members.append(member)


curation = {
  "@type": "cr:Curation",
  "viewingHint": "annotation",
  "@context": [
    "http://iiif.io/api/presentation/2/context.json",
    "http://codh.rois.ac.jp/iiif/curation/1/context.json"
  ],
  "label": title,
  "selections": [
    {
      "within": {
        "@id": manifest,
        "@type": "sc:Manifest"
      },
      "@id": curation_id + "/range1",
      "label": "Markers",
      "members": members,
      "@type": "sc:Range"
    }
  ],
  "@id": curation_id,
  "related": {
    "@type": "cr:MarkerLegend",
    "@id": legend
  }
}

with open("../docs/curation/test.json", 'w') as f:
    json.dump(curation, f, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))