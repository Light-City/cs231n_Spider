import requests
from urllib import request
from lxml import etree
import os
import re
import time
base_url = 'http://cs231n.stanford.edu/slides/'
class slides_Spider:
    def __init__(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        self.headers = headers
    def get_Html(self,url):
        html = requests.get(url, headers=self.headers).text
        selector = etree.HTML(html)
        return selector
    def get_yearUrl(self,url):
        selector = self.get_Html(url)
        year_Href=selector.xpath('//a[starts-with(@href, "20")]/text()')
        print(year_Href)
        year_sildeHref = []
        for i in range(len(year_Href)):
            year_sildeHref.append(base_url+year_Href[i])
        print(year_sildeHref)
        return year_Href,year_sildeHref
    def get_AllUrl(self,url):
        year_Href,year_sildeHref = self.get_yearUrl(url)

        pdf_dict = {}
        for i in range(len(year_sildeHref)):
            pdf_list = []
            selector = self.get_Html(year_sildeHref[i])
            pdf_response = selector.xpath('//a[contains(@href,"pdf")]/text()')
            year_Href[i] = year_Href[i].replace('/','')
            for j in pdf_response:
                pdf_list.append(year_sildeHref[i]+j)
            pdf_dict[year_Href[i]] = pdf_list

        print(pdf_dict)
        return pdf_dict

    def downLoad_Pdf(self,url):
        pdf_dict = self.get_AllUrl(url)
        for key in pdf_dict:
            path = key
            if not os.path.exists(path):
                os.mkdir(path)
            else:
                print("目录已存在")
            print("---------"+ key +"年资料正在下载---------")
            for each in pdf_dict[key]:
                pdf_name = re.split('/', each)[-1]
                print(pdf_name)
                content = requests.get(each,headers=self.headers)
                with open(path+'/'+pdf_name, 'wb') as f:
                    for chunk in content.iter_content(chunk_size=32):
                        f.write(chunk)
                time.sleep(2)
            print("---------" + key + "年资料下载完毕---------")

        print("---------下载完毕---------")

s = slides_Spider()
allPdf_url = s.downLoad_Pdf(base_url)
print(allPdf_url)








