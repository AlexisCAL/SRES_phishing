# Testing URL
# funding.tmp.govt.nz
# vienkiemsattv.gov.vn
# transparencia.mogeiro.pb.gov.br
# banovici.gov.ba

# some curl to be sure
# curl -v --request POST --url 'https://www.virustotal.com/vtapi/v2/url/report' -d apikey=7d683f2eeae6790c17b6a12d295894e9692bc06aa2af43e7851e7faba5dc8bcc -d 'resource=http://www.funding.tmp.govt.nz/'

import requests
import json
import time
import logging


VT_URL_report = 'https://www.virustotal.com/vtapi/v2/url/report'
VT_URL_scan   = 'https://www.virustotal.com/vtapi/v2/url/scan'
VT_API_key    = '7d683f2eeae6790c17b6a12d295894e9692bc06aa2af43e7851e7faba5dc8bcc'

def format_url(url):
    # If we need the 'http://' format
    new_url = 'http://www.' + url
    return new_url

def scan_request(url):
    params = {'apikey': VT_API_key, 'url':url}
    response = requests.post(VT_URL_scan, params=params)
    json_response = response.json()
    return json_response

def report_request(url):
    params = {'apikey': VT_API_key, 'resource':url}
    response = requests.post(VT_URL_report, params=params)
    json_response = response.json()
    return json_response

#
def parsing_response(report_json):
    # report_data = json.dumps(report_json)

    result_data = {}
    result_data['url'] = report_json['url']
    result_data['VT_score'] = report_json['positives']
    result_data['VT_scan'] = []

    # Append positive scan to VT_scan but it doesn't parse through 'scans.detected'

    result_json = json.dumps(result_data)
    return result_json

def VT_API_call(url):
    new_url = format_url(url)

    try :
        scan_json = scan_request(new_url)
        print 'scan_request sucessful'
        # print scan_json
    except :
        print 'scan_request failed for ', new_url

    # Threading ? Or Queueing ?
    time.sleep( 10 ) # waiting for verification completion

    try :
        report_json = report_request(new_url)
        print 'report_request sucessful'
        # print report_json
    except :
        print 'report_request failed for ', new_url

    try :
        ret = parsing_response(report_json)
        print 'Result from VirusTotal verification :'
        print ' >>>', ret
    except :
        print 'parsing_response failed for ', new_url


VT_API_call('banovici.gov.ba')
