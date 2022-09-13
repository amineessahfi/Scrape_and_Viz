
from pydoc import pager
from LinkHandling import PageIterator
from LinkHandling.linkGetter import LinkGetter
from LinkHandling import JSONExtractor
import json




def main():
    data= LinkGetter("https://www.jumia.ma/all-products","https://www.jumia.ma/all-products")
#data1=data.GetLinks()
#print(data1)

#data2=data.TertiaryLinks()
#print(data2)
    PageIterator=PageIterator.PageIterator(BaseUrl="https://www.jumia.ma/all-products",ParentUrl="https://www.jumia.ma/all-products")
    pagenum=PageIterator.findPageNumber("https://www.jumia.ma/ordinateurs-accessoires-informatique/all-products/")
    placeholder=PageIterator.GetUrls("https://www.jumia.ma/ordinateurs-accessoires-informatique/all-products/",pagenum)


    jsonExtractor=JSONExtractor.JSONExtractor(BaseUrl="https://www.jumia.ma/all-products",ParentUrl="https://www.jumia.ma/all-products")
    scripts=jsonExtractor.ExtratScripts(placeholder)
    scripts_parsed=jsonExtractor.FormatJSON(scripts)
    jsondata=jsonExtractor.AppendJSON(scripts_parsed)
    finalAppendedData=jsonExtractor.AppendToOne(jsondata)
    jsonExtractor.ExportJSON(finalAppendedData)


if __name__== "__main__":
    main()