# pip install ipapi
# apt-get install python-dnspython

# git clone https://github.com/CIRCL/bgpranking-redis-api.git
# cd bgpranking-redis-api/example/api_web/client
# python setup.py build
# python setup.py install

import dns.resolver
import ipapi
import json
import bgpranking_web


# host = 'animadores.ceroveinticinco.gov.ar'
host = 'gold.service.gov.au'



def IPs_from_URL (url):
    IPlist = {}
    try :
        answers_IPv4 = dns.resolver.query(url, 'A')
        for rdata in answers_IPv4:
            IPlist['IPv4'] = rdata.address
    except :
        print 'No IPv4 address found'
        IPlist['IPv4'] = None

    # try :
    #     answers_IPv6 = dns.resolver.query(url, 'AAAA')
    #     for rdata in answers_IPv6:
    #         IPlist['IPv6'] = rdata.address
    # except :
    #     print 'No IPv6 address found'

    return IPlist

def Country_from_IPs (IPlist,url):
    geo_dict = {'url':url}
    geo_dict['IPv4'] = IPlist['IPv4']
    try :
        geo_dict['country'] = ipapi.location(IPlist['IPv4'],None,'country')
    except :
        print 'No matching country found for IPv4:', IPlist['IPv4']
        geo_dict['country'] = None

    return geo_dict

def matching_country (geo_dict):
    domain = geo_dict['url'].split(".")[-1]
    country = geo_dict['country']

    if domain == country :
        geo_dict['geo_score'] = 1
    else :
        geo_dict['geo_score'] = 0

    return geo_dict

def Circl_API_call (geo_dict):
    ip = geo_dict['IPv4']
    circl_lookup = bgpranking_web.ip_lookup(ip)
    try :
        asn = int(circl_lookup['history'][0]['asn'])
        # asn = 43765
        geo_dict['asn'] = asn
        circl_ranks = bgpranking_web.all_ranks_single_asn(asn, None, None, None, None)
        ranks = []
        average = 0
        try :
            for date in circl_ranks:
                ranks.append(circl_ranks[str(date)]['total'])

            # Find a way to exploit Circl's bgpranking
            for rank in ranks:
                average = average + rank
            average = average / len(ranks)
        except :
            print 'No ranks found for ASN : ', asn

        geo_dict['circl_score'] = average
    except :
        print 'No ASN found for IPv4 : ', ip
        geo_dict['asn'] = None


    return geo_dict


def localisation (url):
    IPlist = IPs_from_URL(url)
    geo_dict = Country_from_IPs(IPlist, url)
    geo_dict = matching_country(geo_dict)
    geo_dict = Circl_API_call(geo_dict)
    geo_json = json.dumps(geo_dict)

    print geo_json
    return geo_json

localisation(host)
