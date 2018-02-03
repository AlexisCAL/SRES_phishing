# Testing URL
# funding.tmp.govt.nz
# vienkiemsattv.gov.vn


# some curl to be sure
# curl -v --request POST --url 'https://www.virustotal.com/vtapi/v2/url/report' -d apikey=${7d683f2eeae6790c17b6a12d295894e9692bc06aa2af43e7851e7faba5dc8bcc} -d 'resource=http://www.funding.tmp.govt.nz/'
import requests
import json

params = {'apikey': '7d683f2eeae6790c17b6a12d295894e9692bc06aa2af43e7851e7faba5dc8bcc', 'url':'http://www.funding.tmp.govt.nz'}
response = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=params)
json_response = response.json()

print json_response

# scan_id = json_response.scan_id

# headers1 = {
#     "Accept-Encoding": "gzip, deflate",
#     "User-Agent": "gzip, ImNotAPhish"
#     }
#
# params1 = {'apikey': '7d683f2eeae6790c17b6a12d295894e9692bc06aa2af43e7851e7faba5dc8bcc', 'ressource':'http://www.funding.tmp.govt.nz'}
# response1 = requests.post('https://wwww.virustotal.com/vtapi/v2/url/report', params=params1, headers=headers1)
# json_response1 = response1.json()
#
# print json_response1
