import scrapy
import re
from MedlinePlus.items import MedlineplusItem
import os
import urllib.request

class MedlinePlusspiderSpider(scrapy.Spider):
    name = 'mediline_spider'
    start_urls = ['https://medlineplus.gov/encyclopedia.html',]

    def parse(self, response):
        for urls in response.xpath(".//div[@id='az-section2']//li"):
            url = response.urljoin(urls.xpath("./a/@href").extract_first())
            # print(url)
            yield scrapy.Request(url,callback=self.parse1)

    def parse1(self,response):
        for rlt in response.xpath(".//ul[@id='index']/li"):
            url_front = rlt.xpath("./a/@href").extract_first().split('/')[0]
            if url_front == "patientinstructions":
                url = response.urljoin(rlt.xpath("./a/@href").extract_first())
                # print(url)
                yield scrapy.Request(url, callback=self.parse2)
            else:
                continue

    def parse2(self,response):
        item = MedlineplusItem()
        item['title'] = response.xpath(".//h1/text()").extract_first()
        item['url'] = response.url
        if response.xpath(".//div[@class='main']/div[@id='ency_summary']"):
            summary = ""
            for text in response.xpath(".//div[@class='main']/div[@id='ency_summary']/*").extract():
                if text[1:4] == "img":
                    url = re.findall(r'src="([\s\S]*?)"', text)
                    name = re.findall(r'title="([\s\S]*?)"', text)
                    img_url = "https:" + url[0]
                    img_name = name[0]
                    summary = summary + "<picname>" + img_name + "</picname>"
                    summary = summary + "<picurl>" + img_url + "</picurl>"
                    img_number = url[0].split('/')[-1]
                    # 自己电脑测试
                    file_path = 'D:/MedlinePlus/data/medlineplus.gov/ency/images/ency/fullsize/'
                    # 云服务器测试
                    # file_path = 'E:/MedlinePlus/data/medlineplus.gov/ency/images/ency/fullsize/'
                    try:
                        if not os.path.exists(file_path):
                            os.makedirs(file_path) # 如果不存在则创建路径
                        filename = '{}{}'.format(file_path, img_number) # 拼接图片名（包含路径）
                        # print(filename)
                        urllib.request.urlretrieve(img_url, filename=filename) # 下载图片，并保存到文件夹中
                    except IOError as e:
                        print("IOError")
                    except Exception as e:
                        print("Exception")
                p = re.compile(r'<p>', re.S)
                text = p.sub('<text>', text)
                p = re.compile(r'</p>', re.S)
                text = p.sub('</text>', text)
                p = re.compile(r'<ul\b[^>]*>|</ul>|<strong>|</strong>|<a\b[^>]*>|</a>|<img\b[^>]*>',re.S)  # 去b和div标签及文字
                text = p.sub('', text)
                p = re.compile(r'<li>', re.S)
                text = p.sub('<detail>', text)
                p = re.compile(r'</li>', re.S)
                text = p.sub('</detail>', text)
                summary = summary + text
            item['summary'] = summary
        elif response.xpath(".//div[@class='main-single']/div[@id='ency_summary']"):
            summary = ""
            for text in response.xpath(".//div[@class='main-single']/div[@id='ency_summary']/*").extract():
                if text[1:4] == "img":
                    url = re.findall(r'src="([\s\S]*?)"', text)
                    name = re.findall(r'title="([\s\S]*?)"', text)
                    img_url = "https:" + url[0]
                    img_name = name[0]
                    summary = summary + "<picname>" + img_name + "</picname>"
                    summary = summary + "<picurl>" + img_url + "</picurl>"
                    img_number = url[0].split('/')[-1]
                    # 自己电脑测试
                    file_path = 'D:/MedlinePlus/data/medlineplus.gov/ency/images/ency/fullsize/'
                    # 云服务器测试
                    # file_path = 'E:/MedlinePlus/data/medlineplus.gov/ency/images/ency/fullsize/'
                    try:
                        if not os.path.exists(file_path):
                            os.makedirs(file_path) # 如果不存在则创建路径
                        filename = '{}{}'.format(file_path, img_number) # 拼接图片名（包含路径）
                        # print(filename)
                        urllib.request.urlretrieve(img_url, filename=filename) # 下载图片，并保存到文件夹中
                    except IOError as e:
                        print("IOError")
                    except Exception as e:
                        print("Exception")
                p = re.compile(r'<p>', re.S)
                text = p.sub('<text>', text)
                p = re.compile(r'</p>', re.S)
                text = p.sub('</text>', text)
                p = re.compile(r'<ul\b[^>]*>|</ul>|<strong>|</strong>|<a\b[^>]*>|</a>|<img\b[^>]*>', re.S)  # 去b和div标签及文字
                text = p.sub('', text)
                p = re.compile(r'<li>', re.S)
                text = p.sub('<detail>', text)
                p = re.compile(r'</li>', re.S)
                text = p.sub('</detail>', text)
                summary = summary + text
            item['summary'] = summary

        pre_text = ""
        if response.xpath(".//div[@class='main']/section/div[@class='section']"):
            for h2_content in response.xpath(".//div[@class='main']/section/div[@class='section']"):
                h2_title = h2_content.xpath(".//h2/text()").extract_first()
                if h2_title != "References":
                    pre_text = pre_text + "<h2 title=\"" + h2_title + "\"aaa>"
                    content = ""
                    h3time = 0
                    for text in h2_content.xpath(".//div[@class='section-body']/*").extract():
                        if text[1:3] == "h3":
                            if h3time > 0:
                                content = content + "</h3>"
                            p = re.compile(r'<a\b[^>]*></a>', re.S)
                            text = p.sub('', text)
                            p = re.compile(r'<h3\b[^>]*>', re.S)
                            text = p.sub('<h3 title=\"', text)
                            p = re.compile(r'</h3>', re.S)
                            text = p.sub('\"aaa>', text)
                            h3time = h3time + 1
                        if text[1:4] == "img":
                            url = re.findall(r'src="([\s\S]*?)"', text)
                            name = re.findall(r'title="([\s\S]*?)"', text)
                            img_url = "https:" + url[0]
                            img_name = name[0]
                            content = content + "<picname>" + img_name + "</picname>"
                            content = content + "<picurl>" + img_url + "</picurl>"
                            img_number = url[0].split('/')[-1]
                            # 自己电脑测试
                            file_path = 'D:/MedlinePlus/data/medlineplus.gov/ency/images/ency/fullsize/'
                            # 云服务器测试
                            # file_path = 'E:/MedlinePlus/data/medlineplus.gov/ency/images/ency/fullsize/'
                            try:
                                if not os.path.exists(file_path):
                                    os.makedirs(file_path)  # 如果不存在则创建路径
                                filename = '{}{}'.format(file_path,img_number)  # 拼接图片名（包含路径）
                                # print(filename)
                                urllib.request.urlretrieve(img_url,filename=filename)  # 下载图片，并保存到文件夹中
                            except IOError as e:
                                print("IOError")
                            except Exception as e:
                                print("Exception")
                        p = re.compile(r'<p\b[^>]*>', re.S)  # 替换p标签
                        text = p.sub('<text>', text)
                        p = re.compile(r'</p>', re.S)
                        text = p.sub('</text>', text)
                        p = re.compile(r'<div\b[^>]*>|</div>|<ul>|</ul>|<strong>|</strong>|<a\b[^>]*>|</a>|<img\b[^>]*>', re.S)  # 替换p标签
                        text = p.sub('', text)
                        p = re.compile(r'<a\b[^>]*>|</a>', re.S)  # 替换a
                        text = p.sub(' ', text)
                        p = re.compile(r'<li>', re.S)  # 替换li标签
                        text = p.sub('<detail>', text)
                        p = re.compile(r'</li>', re.S)
                        text = p.sub('</detail>', text)
                        content = content + text
                    if h3time > 0 :
                        content = content + "</h3>"
                    pre_text = pre_text + content + "</h2>"
            item['other'] = pre_text
        elif response.xpath(".//div[@class='main-single']/section/div[@class='section']"):
            for h2_content in response.xpath(".//div[@class='main-single']/section/div[@class='section']"):
                h2_title = h2_content.xpath(".//h2/text()").extract_first()
                if h2_title != "References":
                    pre_text = pre_text + "<h2 title=\"" + h2_title + "\"aaa>"
                    content = ""
                    h3time = 0
                    for text in h2_content.xpath(
                            ".//div[@class='section-body']/*").extract():
                        if text[1:3] == "h3":
                            if h3time > 0:
                                content = content + "</h3>"
                            p = re.compile(r'<a\b[^>]*></a>', re.S)
                            text = p.sub('', text)
                            p = re.compile(r'<h3\b[^>]*>', re.S)
                            text = p.sub('<h3 title=\"', text)
                            p = re.compile(r'</h3>', re.S)
                            text = p.sub('\"aaa>', text)
                            h3time = h3time + 1
                        if text[1:4] == "img":
                            url = re.findall(r'src="([\s\S]*?)"', text)
                            name = re.findall(r'title="([\s\S]*?)"', text)
                            img_url = "https:" + url[0]
                            img_name = name[0]
                            content = content + "<picname>" + img_name + "</picname>"
                            content = content + "<picurl>" + img_url + "</picurl>"
                            img_number = url[0].split('/')[-1]
                            # 自己电脑测试
                            file_path = 'D:/MedlinePlus/data/medlineplus.gov/ency/images/ency/fullsize/'
                            # 云服务器测试
                            # file_path = 'E:/MedlinePlus/data/medlineplus.gov/ency/images/ency/fullsize/'
                            try:
                                if not os.path.exists(file_path):
                                    os.makedirs(file_path)  # 如果不存在则创建路径
                                filename = '{}{}'.format(file_path,
                                                         img_number)  # 拼接图片名（包含路径）
                                # print(filename)
                                urllib.request.urlretrieve(img_url,
                                                           filename=filename)  # 下载图片，并保存到文件夹中
                            except IOError as e:
                                print("IOError")
                            except Exception as e:
                                print("Exception")
                        p = re.compile(r'<p\b[^>]*>', re.S)  # 替换p标签
                        text = p.sub('<text>', text)
                        p = re.compile(r'</p>', re.S)
                        text = p.sub('</text>', text)
                        p = re.compile(
                            r'<div\b[^>]*>|</div>|<ul>|</ul>|<strong>|</strong>|<a\b[^>]*>|</a>|<img\b[^>]*>',
                            re.S)  # 替换p标签
                        text = p.sub('', text)
                        p = re.compile(r'<a\b[^>]*>|</a>', re.S)  # 替换a
                        text = p.sub(' ', text)
                        p = re.compile(r'<li>', re.S)  # 替换li标签
                        text = p.sub('<detail>', text)
                        p = re.compile(r'</li>', re.S)
                        text = p.sub('</detail>', text)
                        content = content + text
                    if h3time > 0:
                        content = content + "</h3>"
                    pre_text = pre_text + content + "</h2>"
            item['other'] = pre_text

        # 云服务器
        name = item['title'] + ".html"
        p = re.compile(r':|%|/', re.S)
        name = p.sub('_', name)
        # with open("E:/MedlinePlus/data/html/other/" + name, "wb") as f:
        # 自己电脑
        with open("D:/MedlinePlus/data/html/other/" + name, "wb") as f:
            f.write(response.body)
            f.close()
        yield item