import xml.etree.ElementTree as ET
import requests
import urllib2
import math
import arbetsformedlingen
a = math.ceil(11.9/2)
print(a)


#
# headers = {
#     'Accept': 'application/xml',
#     'Accept-Language': 'en-US',
# }
# url = "http://api.arbetsformedlingen.se/platsannons/soklista/lan"
# req = requests.get(url, headers=headers)
# xml_string = req.text
#
# xml_root = ET.fromstring(xml_string.encode('utf-8'))
#
# listings = []
# for listing in xml_root.findall('sokdata'):
#     id = listing.find('id').text
#
#     print(id)

API_URL = 'http://api.arbetsformedlingen.se/platsannons/matchning'
API_ROOT_URL = 'http://api.arbetsformedlingen.se/platsannons/'

# listings = arbetsformedlingen.get_listings(page=6, lanid=10)
# for listing in listings:
#     print listing

def _request_listings(page=1, lanid=1):
  params = {
      'lanid': lanid,
      'sida': page,
  }
  headers = {
      'Accept': 'application/xml',
      'Accept-Language': 'en-US',
  }
  req = requests.get(API_URL, params = params, headers = headers)
  print(req.text)
  return req.text

# _request_listings(6,10)

listings = arbetsformedlingen.get_listings(page=24, lanid=10)
for listing in listings:
    print listing