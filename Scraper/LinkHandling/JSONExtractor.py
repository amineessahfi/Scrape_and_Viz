import requests
from bs4 import BeautifulSoup
import json
import lxml


class JSONExtractor():
    def __init__(self):
        self.requestSession=requests.Session()
    def ExtratScripts(self,LinkList):
        RequestArray=[]
        for link in LinkList:
            RequestArray.append(BeautifulSoup(self.requestSession.get(link).content,'lxml'))
        return RequestArray
    def FormatJSON(self,RequestArray):
        ScriptArray=[ element.find_all("script")[-5] for element in RequestArray]
        json_data= [ element.text.strip()[17:-1] for element in ScriptArray]
        return json_data
    def AppendJSON(self,JSONData):
        data=[]
        for idx,element in enumerate(JSONData):
            try:
                data.append( json.loads(JSONData[idx])['products'] for idx,element in enumerate(JSONData) )
            except KeyError:
                pass
        return data
    def AppendToOne(self,data):
        array=[]
        for element in data:
            for ele in element:
                array.append(ele)
        return array        

    def ExportJSON(self,data):
        with open('ScrapedProducts.json','w') as f:
            json.dump(data,f)





    


