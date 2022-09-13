import requests
from bs4 import BeautifulSoup
import lxml

class PageIterator():
    def __init__(self):
        self.requestSession=requests.Session()
        
    def findPageNumber(self,Link):
        ParsedContent=BeautifulSoup(self.requestSession.get(Link).content,'lxml')
        if ParsedContent.find_all("a",{"class":"pg"}) != [] :
            plcHolder=ParsedContent.find_all("a",{"class":"pg"})[-1]["href"]
            pageLimit = int(plcHolder[plcHolder.find('page'):][5:-16])
        else:
            pageLimit=1
        return pageLimit

    def GetUrls(self,Link,PageNumber):
        requestArray=[]
        Urls=[ Link + "?page=" + str(i+1) for i in range(PageNumber)]
        return Urls 

        


        