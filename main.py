#!/usr/bin/env python3
# pip3 install python-Levenshtein pillow stix2 dnspython ipapi pytesseract certstream tqdm termcolor
# install tesseract
#   pacman -S tesseract tesseract-data-eng
#   apt install tesseract-ocr  tesseract-ocr-eng
#
# git clone https://github.com/CIRCL/bgpranking-redis-api.git
# cd bgpranking-redis-api/example/api_web/client
# 2to3 . -w
# python3 setup.py build
# sudo python3 setup.py install

import json
import logging
import sys
import time
from datetime import datetime

import certstream
import stix2
import tqdm
from termcolor import colored, cprint

from tools.geo import *
from tools.sn import *
from tools.vt import *

extensions = []
addresses = []
words = []

with open('open_data/clean_ext') as f:
    extensions = f.readlines()
extensions = [x.strip() for x in extensions]

with open('open_data/clean_word') as f:
    words = f.readlines()
words = [x.strip() for x in words]

with open('open_data/clean_add') as f:
    addresses = f.readlines()
addresses = [x.strip() for x in addresses]


def consume(bundle):
    for obj in bundle.objects:
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


def phishing(domain, score):
    indicator = stix2.Indicator(
        name="Potential phishing website",
        description="This website has got a score of " + str(score) + ".",
        labels=["phishing"],
        pattern="[url:value = '" + domain + "']",
    )

    bundle = stix2.Bundle(objects=[indicator])
    print(consume(bundle))


def score_domain(domain):
    score = 0

    # Remove initial '*.' for wildcard certificates bug
    if domain.startswith('*.'):
        domain = domain[2:]

    # Testing keywords
    for word in words:
        if word in domain:
            score += 20

    # Lots of '-' (ie. www.paypal-datacenter.com-acccount-alert.com)
    if 'xn--' not in domain and domain.count('-') >= 4:
        score += domain.count('-') * 3

    # Deeply nested subdomains (ie. www.paypal.com.security.accountupdate.gq)
    if domain.count('.') >= 4:
        score += domain.count('.') * 3

    # Testing Levenshtein distance for keywords in our list
    if dakl(domain, words) > 0:
        score += 10

    # Testing if the server is hosted in the same country as the extension suggests
    geo_result = localisation(domain)
    if geo_result['IP'] == None:
        print("\nIP not found for", domain)
        return score
    # Testing for the score from CIRCL also
    elif not geo_result['geo_score'] or geo_result['circl_score'] > 0.1:
        score += 25

        # Testing for lookalike characters
        if cowd(domain, geo_result['country']) > 0:
            score += 25

    # If the site is suspicious enough, send it to VirusTotal for analysis
    if score >= 100:
        vt_result = VT_API_call(domain)
        if vt_result == {}:
            print("\nError on virus total for", domain)
            return score
        score += 50 * vt_result['VT_score']

    return score


def new_cert(message, context):
    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        for domain in all_domains:
            pbar.update(1)
            score = score_domain(domain)

            # If issued from a free CA = more suspicious
            if "Let's Encrypt" in message['data']['chain'][0]['subject']['aggregated']:
                score += 10

            if score >= 115:
                tqdm.tqdm.write(
                    "[!] Suspicious: "
                    "{} (score={})".format(colored(domain, 'red', attrs=['underline', 'bold']), score))
            elif score >= 100:
                tqdm.tqdm.write(
                    "[!] Suspicious: "
                    "{} (score={})".format(colored(domain, 'red', attrs=['underline']), score))
            elif score >= 90:
                tqdm.tqdm.write(
                    "[!] Likely    : "
                    "{} (score={})".format(colored(domain, 'yellow', attrs=['underline']), score))
            elif score >= 75:
                tqdm.tqdm.write(
                    "[+] Potential : "
                    "{} (score={})".format(colored(domain, attrs=['underline']), score))

            if score >= 100:
                phishing(domain, score)


pbar = tqdm.tqdm(desc='certificate_update', unit='cert')
certstream.listen_for_events(new_cert)
