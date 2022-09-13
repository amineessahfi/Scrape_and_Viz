
import asyncio
import time  
import aiohttp
from bs4 import BeautifulSoup
from limiter import Limiter

LIMIT= Limiter(rate=3)

BaseUrl="https://www.jumia.ma/all-products"



@LIMIT
async def asyncGetLinks(BaseUrl):
    async with aiohttp.ClientSession() as session:
        
        async with LIMIT:
            response= await session.get(BaseUrl,ssl=False)
            text=response.text()
            ParsedContent=BeautifulSoup( await text,"lxml")
            data=[]
            for element in ParsedContent.find_all('a',{"class":"-db -pvs -phxl -hov-bg-gy05"},href=True):            
                data.append(element['href'])
        return data
@LIMIT
def getTasks(session,elements):
    Tasks=[]
    print("Number of Requests to be processed : {}".format(len(elements)))
    for element in elements:
        '''(len(Tasks)/(time.time()-start))''' #to be implemented
        try:    
                Tasks.append(session.get(element,ssl=False,timeout=60))
        except asyncio.exceptions.TimeoutError:
            pass
        print("Gathering {} info".format(element))
        print("elapsed time : {} seconds".format(round(time.time()-start,2)))
        print("Current Rate {} per second".format(round((len(Tasks)/(time.time()-start)),2)))
    return Tasks



@LIMIT
async def asyncSecondaryLinks():

        async with aiohttp.ClientSession() as session:
            ParsedLinks=await asyncGetLinks(BaseUrl)
            Urls= [ BaseUrl + element for element in ParsedLinks]
            RequestArray= getTasks(session,Urls)
            responses= await asyncio.gather(*RequestArray)
            results=[]
            ParsedContent=[]
            FinalResults=[]
            for response in responses:
                results.append(await response.text())
            for result in results:
                ParsedContent.append(BeautifulSoup(result,'lxml'))
            Links= [Content.findAll('a',{"class":"-db -pvs -phxl -hov-bg-gy05"},href=True) for Content in ParsedContent]
            for link in Links:
                for sub in link:
                    FinalResults.append(sub['href'])
            return [BaseUrl + FinalResult for FinalResult in FinalResults]
            
@LIMIT
async def asyncTertiaryLinks(SecondaryLinks):

        async with aiohttp.ClientSession() as session:
            
            RequestArray=getTasks(session,SecondaryLinks)
            responses= await asyncio.gather(*RequestArray)
            results=[]
            ParsedContent=[]
            FinalResults=[]
            for response in responses:
                results.append(await response.text())
            for result in results:
                ParsedContent.append(BeautifulSoup(result,'lxml'))
            Links= [Content.findAll('a',{"class":"-db -pvs -phxl -hov-bg-gy05"},href=True) for Content in ParsedContent]
            for link in Links:
                for sub in link:
                    FinalResults.append(sub['href'])
            return [BaseUrl + FinalResult for FinalResult in FinalResults]
    # We need to set up a coroutine / gather *

#---------------------------------PageNumbers-----------------------------------
async def AsyncfindPageNumber(Link):
    async with aiohttp.ClientSession() as session:
        response=await session.get(Link,ssl=False)
        text=response.text()
        ParsedContent=BeautifulSoup(await text,'lxml')
        if ParsedContent.find_all("a",{"class":"pg"}) != [] :
            plcHolder=ParsedContent.find_all("a",{"class":"pg"})[-1]["href"]
            pageLimit = int(plcHolder[plcHolder.find('page'):][5:-16])
        else:
            pageLimit=1
        return pageLimit
        
        
       





def newGetUrls(array,Numberpages):
    newlist=[]
    for idx,element in enumerate(array):
        for i in range(Numberpages[idx]):
            newlist.append(element+"?page="+str(i+1))
    return newlist



'''
        ParsedContent=BeautifulSoup(self.requestSession.get(Link).content,'lxml')
        if ParsedContent.find_all("a",{"class":"pg"}) != [] :
            plcHolder=ParsedContent.find_all("a",{"class":"pg"})[-1]["href"]
            pageLimit = int(plcHolder[plcHolder.find('page'):][5:-16])
        else:
            pageLimit=1
        return pageLimit
'''

#----------------------------Execution--------------------------------------------
start=time.time()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

SecondaryLinks= asyncio.new_event_loop().run_until_complete(asyncSecondaryLinks())
TertiaryLink=asyncio.new_event_loop().run_until_complete(asyncTertiaryLinks(SecondaryLinks))
#getPages=asyncio.new_event_loop().run_until_complete(AsyncfindPageNumber(TertiaryLink))
#TotalLinks=newGetUrls(TertiaryLink,getPages)

async def ContinueAsync(TertiaryLink):
    MaxpageList=[]
    for link in TertiaryLink:
        print("loading {}".format(link))
        MaxpageList.append(await AsyncfindPageNumber(link))
    return MaxpageList

#MaxpageList=asyncio.new_event_loop().run_until_complete(ContinueAsync(TertiaryLink))


end=time.time()
ExecTime=end-start
print(len(TertiaryLink))
#print(len(MaxpageList))
#print(MaxpageList)
print(" {} requests Executed in {} seconds".format(len(TertiaryLink),round(ExecTime,2)))
#---------------------------------------------------------------------------------
