import scrapy
import re
from MedlinePlus.items import MedlineplusItem
import urllib.request
import requests
import os

class MedlinePlusspiderSpider(scrapy.Spider):
    name = 'test_spider'
    start_urls = ['https://medlineplus.gov/encyclopedia.html',]

    def parse(self, response):
        for urls in response.xpath(".//div[@id='az-section2']//li"):
            url = response.urljoin(urls.xpath("./a/@href").extract_first())
            yield scrapy.Request(url,callback=self.parse1)

    def parse1(self,response):
        for rlt in response.xpath(".//ul[@id='index']/li"):
            url_front = rlt.xpath("./a/@href").extract_first().split('/')[0]
            if url_front != "patientinstructions":
                url = response.urljoin(rlt.xpath("./a/@href").extract_first())
                yield scrapy.Request(url, callback=self.parse2)
            else:
                continue

    def parse2(self,response):
        test = response.xpath(".//div[@class='main-single']//section[1]//h2/text()").extract_first()
        if test == "How the Test is Performed":
            item = MedlineplusItem()
            item['title'] = response.xpath(".//h1/text()").extract_first()
            item['url'] = response.url
            for texts in response.xpath(".//section"):
                h2_key = texts.xpath(".//h2/text()").extract_first()
                text = texts.xpath(".//div[@class='section-body']").extract_first()
                p = re.compile(r'<p\b[^>]*>', re.S)  # 替换p标签
                text = p.sub('<text>', text)
                p = re.compile(r'</p>', re.S)
                text = p.sub('</text>', text)
                p = re.compile(r'<em>|</em>|<div\b[^>]*>|</div>|<ul>|</ul>|\n',re.S)  # 去b和div标签及文字
                text = p.sub('', text)
                p = re.compile(r'<a\b[^>]*>|</a>',re.S)  # 替换a
                text = p.sub(' ', text)
                p = re.compile(r'<li>', re.S)  # 替换li标签
                text = p.sub('<detail>', text)
                p = re.compile(r'</li>', re.S)
                text = p.sub('</detail>', text)
                if h2_key == "How to Prepare for the Test":
                    item['HowtoPreparefortheTest'] = text
                if h2_key == "Why the Test is Performed":
                    item['WhytheTestisPerformed'] = text
                if h2_key == "Normal Results":
                    item['NormalResults'] = text
                if h2_key == "What Abnormal Results Mean":
                    item['WhatAbnormalResultsMean'] = text
                if h2_key == "Alternative Names":
                    p = re.compile(r'<text>', re.S)  # 替换li标签
                    text = p.sub('<detail>', text)
                    p = re.compile(r'</text>', re.S)
                    text = p.sub('</detail>', text)
                    p = re.compile(r';', re.S) # 替换分号
                    text = p.sub('</detail><detail>', text)
                    item['AlternativeNames'] = text
                # 图片的下载处理
                if h2_key == "Images":
                    img_list = list()
                    for imgs in texts.xpath(".//li"):
                        i = {}
                        i['img_name'] = imgs.xpath("./a/text()").extract_first()
                        detail_url = response.urljoin(imgs.xpath("./a/@href").extract_first())
                        new_response = requests.get(detail_url)
                        response = response.replace(body=new_response.text)
                        img_url = "https:" + response.xpath(".//div[@class='main']//img/@src").extract_first()
                        img_number = response.xpath(".//div[@class='main']//img/@src").extract_first().split('/')[-1]
                        i['img_url'] = img_url
                        img_list.append(i)
                        # 下载图片到指定文件路径
                        # print(img_url)
                        # 自己电脑测试
                        # file_path = 'D:/MedlinePlus/data/medlineplus.gov/ency/images/ency/fullsize/'
                        # 云服务器测试
                        # file_path = 'E:/MedlinePlus/data/medlineplus.gov/ency/images/ency/fullsize/'
                        # try:
                        #     if not os.path.exists(file_path):
                        #         os.makedirs(file_path) # 如果不存在则创建路径
                        #     filename = '{}{}'.format(file_path, img_number) # 拼接图片名（包含路径）
                        #     # print(filename)
                        #     urllib.request.urlretrieve(img_url, filename=filename) # 下载图片，并保存到文件夹中
                        # except IOError as e:
                        #     print("IOError")
                        # except Exception as e:
                        #     print("Exception")
                    item['Images'] = img_list
            name = item['title'] + ".html"
            # 云服务器
            with open("E:/MedlinePlus/data/html/test/" + name, "wb") as f:
            # 自己电脑
            #with open("D:/MedlinePlus/data/html/test/" + "1.html","wb") as f:
                f.write(response.body)
                f.close()
            yield item