import arbetsformedlingen
import json
import xml.etree.ElementTree as ET
import requests
#First page of listings (20 at a time)
import math

class mainScraper():
    def __init__(self):
        self.total_data = []

    def parse_lan(self):
        logTxt = "Parsing xml from lan api..."
        print(logTxt)

        headers = {
            'Accept': 'application/xml',
            'Accept-Language': 'en-US',
        }
        url = "http://api.arbetsformedlingen.se/platsannons/soklista/lan"
        req = requests.get(url, headers=headers)
        xml_string = req.text

        xml_root = ET.fromstring(xml_string.encode('utf-8'))

        self.lan_page_lists = []
        for listing in xml_root.findall('sokdata'):
            id = int(listing.find('id').text)
            job_num = int(listing.find('antal_platsannonser').text)
            page_num = int(math.floor(job_num/20) + 1)
            self.lan_page_lists.append([id, page_num])

        logTxt = "Parsing is done."
        print(logTxt)

    def get_alldata(self):
        logTxt = "Started getting all data..."
        print(logTxt)

        for id, page_num in self.lan_page_lists:
            for page_index in range(page_num):

                logTxt = "-+-+-+-+-+-+-+-+-+-+-+ id: {}, page: {} -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+".format(id, page_index)
                print(logTxt)

                listings = arbetsformedlingen.get_listings(page=page_index + 1, lanid=id)
                if listings:
                    self.total_data.extend(listings)
                else:
                    break

        logTxt = "Done getting data."
        print(logTxt)

        with open('result.json', 'w') as outfile:
            json.dump(self.total_data, outfile)

if __name__ == '__main__':
    app = mainScraper()
    app.parse_lan()
    app.get_alldata()
