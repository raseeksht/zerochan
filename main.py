import requests
from bs4 import BeautifulSoup
import threading
import os

loginurl = "https://www.zerochan.net/login"

# requests = requests.session()
# resp = requests.post(loginurl,{
#     'ref':'/',
#     'name':'raseekshrestha',
#     'password':'onichan',
#     'login':'Login'
#     }
# )


# print(resp.headers)
# exit()

# url = "https://www.zerochan.net/Kamisato+Ayaka?q=Kamisato+Ayaka"
url  = input("zerochan url: ")

class ZeroChan:
    def __init__(self,url,downloadLocation):
        self.url = url
        self.downloadLocation = os.path.abspath(downloadLocation)
        self._curPage = 1
        self.threads = []
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
        

        # cretae dowload dir if not present
        if not os.path.isdir(self.downloadLocation):
            os.mkdir(self.downloadLocation)
    
    def fetch(self):
        self._result = requests.get(self.url+f"&p={self._curPage}",headers=self.headers)
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
            except Exception as e:
                print("error getting media url,may be registration required")
            
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
        os.system(f"""wget -U '{self.headers['User-Agent']}' -q --show-progress {self._hurl}{url} -O {location}/{url.split('/')[-1]}""")
        # print(url)

with open("downloadLocation.txt") as f:
    downloadLocation = f.read().strip()

zchan = ZeroChan(url,downloadLocation)
zchan.start()



# print(images)



