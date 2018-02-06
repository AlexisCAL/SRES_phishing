#!/usr/bin/env python3
# pip install python-Levenshtein pillow stix2

import sys
import stix2

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


def feed_main(domain):
    print(domain, "\n")
    if dakl(domain) > 0:
        country = localisation(domain)
        print('dakl')
        # IPAPI pour trouver la langue pour l'océrisation
        # OCR:
            # if cowd(domain) > 0:
                # if VirusTotal:
                    # PHISHING


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
