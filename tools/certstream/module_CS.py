import json
import logging
import time

import certstream

exec(open('main.py').read())


def new_cert(message, context):
    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        if len(all_domains) == 0:
            return
        feed_main(all_domains)


certstream.listen_for_events(new_cert)
