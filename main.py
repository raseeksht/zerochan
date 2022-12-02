import requests
from bs4 import BeautifulSoup
import threading
import os

url = "https://www.zerochan.net/Kamisato+Ayaka?q=Kamisato+Ayaka"
# url  = input("url: ")

class ZeroChan:
    def __init__(self,url,downloadLocation):
        self.url = url
        self.downloadLocation = os.path.abspath(downloadLocation)
        self.threads = []
        

        # cretae dowload dir if not present
        if not os.path.isdir(self.downloadLocation):
            os.mkdir(self.downloadLocation)
    
    def fetch(self):
        self._result = requests.get(self.url)
        self._soup = BeautifulSoup(self._result.content,'html.parser')

        self._totalPage = int(self._soup.find("p",{"class":"pagination"}).span.text.strip().split(" ")[-1])
        self._images = self._soup.find("ul",id="thumbs2").find_all("li")

    def start(self):
        self.fetch()
        for img in self._images:
            try:
                mediaurl = img.div.a.img['src']
                self.download(mediaurl,self.downloadLocation)
            except Exception:
                print("error getting media url")
            




    def download(self,url,location):
        os.system(f"wget -q --show-progress {url} -O {location}/{url.split('/')[-1]}")

downloadLocation = "downloads"

zchan = ZeroChan(url,downloadLocation)
zchan.start()



# print(images)



