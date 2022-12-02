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
        self._curPage = 1
        self.threads = []
        

        # cretae dowload dir if not present
        if not os.path.isdir(self.downloadLocation):
            os.mkdir(self.downloadLocation)
    
    def fetch(self):
        self._result = requests.get(self.url+f"&p={self._curPage}")
        print(self.url+f"?p={self._curPage}")
        self._soup = BeautifulSoup(self._result.content,'html.parser')

        
        self._totalPage = int(self._soup.find("p",{"class":"pagination"}).span.text.strip().split(" ")[-1])
        self._images = self._soup.find("ul",id="thumbs2").find_all("li")

    def start(self):
        self.fetch()
        for img in self._images:
            try:
                mediaurl = img.div.a.img['src']
                self.threads.append(threading.Thread(target=self.download,args=(mediaurl.split("/")[-1],self.downloadLocation,)))
                # self.download(mediaurl.split("/")[-1],self.downloadLocation)
            except Exception:
                print("error getting media url")
            
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()
        self.threads = []
        if self._curPage<self._totalPage:
            self._curPage +=1
            print(self._curPage)
            self.start()

        



    def download(self,url,location):
        self._hurl = "https://s1.zerochan.net/Genshin.Impact.600."
        os.system(f"wget -q --show-progress {self._hurl}{url} -O {location}/{url.split('/')[-1]}")
        # print(url)

downloadLocation = "downloads"

zchan = ZeroChan(url,downloadLocation)
zchan.start()



# print(images)



