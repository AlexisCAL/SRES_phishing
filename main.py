#!/usr/bin/env python3
# pip install python-Levenshtein pillow stix2 dnspython ipapi pytesseract
# install tesseract

import sys

import stix2
from datetime import datetime

ext = open('open_data/clean_ext')
word = open('open_data/clean_word')
add = open('open_data/clean_add')

with ext as f:
    extensions = f.readlines()
extensions = [x.strip() for x in extensions]

with word as f:
    words = f.readlines()
words = [x.strip() for x in words]

with add as f:
    officials = f.readlines()
officials = [x.strip() for x in officials]

known_list = extensions + words
known = open('open_data/white_list', 'w')
for w in known_list:
    known.write("%s\n" % w)

def consume(bundle):
    for obj in bundle.objects:
        if obj == indicator:
            print("------------------")
            print("== INDICATOR ==")
            print("------------------")
            print("ID: " + obj.id)
            print("Created: " + str(obj.created))
            print("Modified: " + str(obj.modified))
            print("Name: " + obj.name)
            print("Description: " + obj.description)
            print("Labels: " + obj.labels[0])
            print("Pattern: " + obj.pattern)
            print("Valid From: " + str(obj.valid_from))


def phishing(domain):
    now = datetime.today().astimezone().isoformat()
    indicator = stix2.Indicator(
        created=now,
        modified=now,
        name="Malicious site trying fishing",
        description="This organized threat actor group operates to get fishes.",
        labels=["malicious-activity"],
        pattern="[url:value = '" + domain + "']",
        valid_from=now
    )

    foothold = stix2.KillChainPhase(
        kill_chain_name="mandiant-attack-lifecycle-model",
        phase_name="establish-foothold"
    )

    bundle = stix2.Bundle(objects=[indicator])
    print(consume(bundle))


def feed_main(domain):
    print(domain, "\n")
    if dakl(domain) > 0:
        geo_result = localisation(domain)
        if geo_result['IP'] == None:
            print("Error on ipapi for ", domain)
            return
        if geo_result['geo_score'] or geo_result['circl_score'] > 0.1:
            phishing(domain)
            return
        if cowd(domain, gep_result['country']) > 0:
            vt_result = VT_API_call(domain)
            if vt_result == {}:
                print("Error on virus total for ", domain)
                return
            if vt_result['VT_score'] > 0:
                phishing(domain)
                return
            known_list += domain.split('.')
            for w in domain.split('.'):
                known.write("%s\n" % w)
            return
    known_list += domain.split('.')
    for w in domain.split('.'):
        known.write("%s\n" % w)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('You need to input an argument:')
        print('cs, geo, vt, sn, all')
    elif len(sys.argv) == 2:
        if sys.argv[1] == 'cs':
            exec(open('tools/certstream/module_CS.py').read())
        elif sys.argv[1] == 'geo':
            exec(open('tools/geolocalisation/module_GEO.py').read())
        elif sys.argv[1] == 'vt':
            exec(open('tools/virus_total/module_VT.py').read())
        elif sys.argv[1] == 'sn':
            exec(open('tools/levenshtein/module_SN.py').read())
        elif sys.argv[1] == 'all':
            exec(open('tools/geolocalisation/module_GEO.py').read())
            exec(open('tools/virus_total/module_VT.py').read())
            exec(open('tools/levenshtein/module_SN.py').read())
            exec(open('tools/certstream/module_CS.py').read())
