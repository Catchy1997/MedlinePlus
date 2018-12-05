from scrapy import cmdline
cmdline.execute("scrapy crawl mediline_spider -o Mediline.xml".split())   #运行爬虫，将爬回的数据以json的形式存放到data.json文件中
# cmdline.execute("scrapy crawl mediline_spider".split())