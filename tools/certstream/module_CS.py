import json
import logging
import time

import certstream


def pre_process(domains):
    possible_threats = []
    for domain in domains:
        if domain not in officials and domain in (extensions + words):
            possible_threats.add(domain)
    if len(possible_threats) == 0:
        return
    feed_main(possible_threats)


def new_cert(message, context):
    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        if len(all_domains) == 0:
            return
        pre_process(all_domains)


certstream.listen_for_events(new_cert)
