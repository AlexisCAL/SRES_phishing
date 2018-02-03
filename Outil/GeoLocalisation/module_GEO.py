import dns.resolver
import ipapi
import json
# import bgpranking_web


host = 'animadores.ceroveinticinco.gov.ar'


def IPs_from_URL (url):
    IPlist = {}

    try :
        answers_IPv4 = dns.resolver.query(url, 'A')
        for rdata in answers_IPv4:
            IPlist['IPv4'] = rdata.address
    except :
        print 'No IPv4 address found'

    try :
        answers_IPv6 = dns.resolver.query(url, 'AAAA')
        for rdata in answers_IPv6:
            IPlist['IPv6'] = rdata.address
    except :
        print 'No IPv6 address found'

    return IPlist

def Country_from_IPs (IPlist,url):
    geo_dict = {'url':url}
    geo_dict['IPv4'] = IPlist['IPv4']
    geo_dict['country'] = ipapi.location(IPlist['IPv4'],None,'country')

    return geo_dict

def localisation (url):
    IPlist = IPs_from_URL(url)
    geo_dict = Country_from_IPs(IPlist, url)
    geo_json = json.dumps(geo_dict)
    print geo_json


localisation(host)
