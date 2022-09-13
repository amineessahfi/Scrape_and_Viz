import ssl
import requests
from bs4 import BeautifulSoup
import lxml
import cchardet
import aiohttp

class LinkGetter():
    ''' only works for getting primary links'''
    def __init__(self,BaseUrl):
        self.requestSession=requests.Session()
        self.requestSession.verify=False
        self.BaseUrl=BaseUrl
        
    def SynchronousGet(self):
        req = self.requestSession.get(self.BaseUrl).text
        ParsedContent=BeautifulSoup(req,'lxml')
        data = []
        for element in ParsedContent.find_all('a',{"class":"-db -pvs -phxl -hov-bg-gy05"},href=True):            
            data.append(element['href'])
        return data

    def SecondaryLinks(self):
        '''Sub Links for In-depth Scraping'''
        ParsedLinks=LinkGetter.SynchronousGet(self)
        Urls= [ self.BaseUrl + element for element in ParsedLinks]
        RequestArray=[]
        Links=[]
        for element in Urls:
            RequestArray.append(BeautifulSoup(self.requestSession.get(element).text,'lxml'))

        for subelement in RequestArray:
            for ele in subelement.find_all('a',{"class":"-db -pvs -phxl -hov-bg-gy05"},href=True):
                Links.append(ele['href'])
        return [self.BaseUrl + Link for Link in Links]

    def TertiaryLinks(self):
        '''For 3rd Order SubCategories Link Scraping'''
        SecondaryLinks=LinkGetter.SecondaryLinks(self)
        RequestArray= []
        Links=[]
        for element in SecondaryLinks:
            RequestArray.append(BeautifulSoup(self.requestSession.get(element).text,'lxml'))
        for subelement in RequestArray:
            for ele in subelement.find_all('a',{"class":"-db -pvs -phxl -hov-bg-gy05"},href=True):
                Links.append(ele['href'])
        return [self.BaseUrl + Link for Link in Links]

    async def asyncGetLinks(self):
        async with aiohttp.ClientSession() as session:
            response= await session.get(self.BaseUrl,ssl=False)
            text=response.text()
            ParsedContent=BeautifulSoup( await text,"lxml")
            data = []
            for element in ParsedContent.find_all('a',{"class":"-db -pvs -phxl -hov-bg-gy05"},href=True):            
                data.append(element['href'])
            return data








