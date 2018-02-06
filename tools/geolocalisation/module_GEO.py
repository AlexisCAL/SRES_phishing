# git clone https://github.com/CIRCL/bgpranking-redis-api.git
# cd bgpranking-redis-api/example/api_web/client
# python setup.py build
# python setup.py install

import json

import dns.resolver
import ipapi

import bgpranking_web

# host = 'animadores.ceroveinticinco.gov.ar'
host = 'gold.service.gov.au'


def IPs_from_URL(geo_dict):
    IP = {}
    url = geo_dict['url']
    try:
        answers_IP = dns.resolver.query(url, 'A')
        for rdata in answers_IP:
            IP['IP'] = rdata.address
        geo_dict['IP'] = IP['IP']
    except:
        print('No IPv4 address found')
        geo_dict['IP'] = None

    if geo_dict['IP'] == None:
        try:
            answers_IPv6 = dns.resolver.query(url, 'AAAA')
            for rdata in answers_IPv6:
                IP['IP'] = rdata.address
            geo_dict['IP'] = IP['IP']
        except:
            print('No IPv6 address found')
            geo_dict['IP'] = None

    return geo_dict


def Country_from_IPs(geo_dict):
    try:
        geo_dict['country'] = ipapi.location(geo_dict['IP'], None, 'country')
    except:
        print('No matching country found for IP:', IPlist['IP'])
        geo_dict['country'] = None

    return geo_dict


def matching_country(country1, geo_dict):
    country2 = geo_dict['country']

    if country1 == country2:
        geo_dict['geo_score'] = True
    else:
        geo_dict['geo_score'] = False

    return geo_dict


def Circl_API_call(geo_dict):
    ip = geo_dict['IP']
    circl_lookup = bgpranking_web.ip_lookup(ip)

    country = circl_lookup['history'][0]['descriptions'][0][-1].split(' ')[-1]
    geo_dict = matching_country(country, geo_dict)
    try:
        asn = int(circl_lookup['history'][0]['asn'])
        # asn = 43765 # Top ranked asn on 02/05
        geo_dict['asn'] = asn
        circl_ranks = bgpranking_web.all_ranks_single_asn(
            asn, None, None, None, None)
        ranks = []
        average = 0
        try:
            for date in circl_ranks:
                ranks.append(circl_ranks[str(date)]['total'])

            # Find a way to exploit Circl's bgpranking
            # Average
            # for rank in ranks:
            #     average = average + rank
            # average = average / len(ranks)
            # Last reference
            average = ranks[-1]
        except:
            print('No ranks found for ASN : ', asn)

        geo_dict['circl_score'] = average
    except:
        print('No ASN found for IP : ', ip)
        geo_dict['asn'] = None

    return geo_dict


def localisation(url):
    geo_dict = {'url': url, 'IP': None, 'asn': None,
                'country': None, 'geo_score': False, 'circl_score': None}
    geo_dict = IPs_from_URL(geo_dict)
    if geo_dict['IP'] == None:
        geo_json = json.dumps(geo_dict)
        print(geo_json)
        return geo_json
    else:
        geo_dict = Country_from_IPs(geo_dict)
        geo_dict = Circl_API_call(geo_dict)
        geo_json = json.dumps(geo_dict)
        print(geo_json)
        return geo_json


localisation(host)
