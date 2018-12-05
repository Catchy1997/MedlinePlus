from scrapy import cmdline
cmdline.execute("scrapy crawl test_spider -o test-118.xml".split())   #运行爬虫，将爬回的数据以json的形式存放到data.json文件中
# cmdline.execute("scrapy crawl test_spider".split())