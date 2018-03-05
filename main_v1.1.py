import arbetsformedlingen
import json
import xml.etree.ElementTree as ET
import requests
#First page of listings (20 at a time)
import math
import threading
import time

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
            job_cnt = int(listing.find('antal_platsannonser').text)
            page_cnt = int(math.floor(job_cnt/20) + 1)

            for page_num in range(1, page_cnt+1, 1):
                self.lan_page_lists.append(
                    [id, page_num]
                )

        self.lan_page_lists.reverse()

        logTxt = "Parsing is done."
        print(logTxt)

    def total_get_alldata(self):

        logTxt = "Started getting all data..."
        print(logTxt)

        self.threads = []
        self.max_threads = 30

        while self.threads or self.lan_page_lists:
            for thread in self.threads:
                if not thread.is_alive():
                    self.threads.remove(thread)

            while len(self.threads) < self.max_threads and self.lan_page_lists:
                thread = threading.Thread(target=self.get_one_page)
                thread.setDaemon(True)
                thread.start()
                self.threads.append(thread)

        logTxt = "Done getting data."
        print(logTxt)

    def get_one_page(self):

        [id, page_num] = self.lan_page_lists.pop()

        listings = arbetsformedlingen.get_listings(page=page_num, lanid=id)
        if listings:
            self.total_data.extend(listings)
        else:
            self.cleanup_lan_page_lists(id, page_num)

        logTxt = "-+-+-+-+-+-+-+-+-+-+-+ id: {}, page: {} -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+".format(id,
                                                                                                               page_num)
        print(logTxt)

        logTxt = "\tTotal Cnt: {}".format(len(self.total_data))
        print(logTxt)

    def cleanup_lan_page_lists(self, id, page_num):

        lan_page_lists = []

        for row in self.lan_page_lists:
            if row[0] == id and row[1] > page_num:
                pass
            else:
                lan_page_lists.append(row)

        self.lan_page_lists = lan_page_lists

    def saveJSON(self):
        with open('result.json', 'w') as outfile:
            json.dump(self.total_data, outfile)

def takeFourth(elem):
    return elem[0]

if __name__ == '__main__':
    start_t = time.time()
    app = mainScraper()
    app.parse_lan()
    app.total_get_alldata()
    app.saveJSON()

    print(time.time() - start_t)
