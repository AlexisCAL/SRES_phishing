import json
import logging
import time

import certstream


def pre_process(domain):
    if domain not in officials:
        feed_main(domain)


def new_cert(message, context):
    if message['message_type'] != "heartbeat":
        if message['message_type'] == "certificate_update":
            all_domains = message['data']['leaf_cert']['all_domains']

            if len(all_domains) != 0:
                pre_process(all_domains)


certstream.listen_for_events(new_cert)
