#!/usr/bin/env python3
# pip install python-Levenshtein pillow stix2 dnspython ipapi pytesseract
# install tesseract

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

known_list = extensions + words


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
            return
    known_list += domain.split('.')


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
