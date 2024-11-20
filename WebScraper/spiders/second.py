import scrapy
from WebScraper.items import SecondHandHouse
from scrapy_selenium import SeleniumRequest

class SecondSpider(scrapy.Spider):
    name = "second"
    allowed_domains = ["bj.lianjia.com"]
    base_url = 'https://bj.lianjia.com/ershoufang/'
    base_page = 3
    range_ = 5

    def start_requests(self):
        # 动态生成 URLs
        urls = [f"{self.base_url}pg{self.base_page + i}" for i in range(self.range_)]
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        li_list = response.xpath('//*[@id="content"]/div[1]/ul/li')
        for item in li_list:
            house = SecondHandHouse()
            house['name'] = item.xpath('./div[1]/div[1]/a/text()').get()
            region = item.xpath('./div[1]/div[2]/div/a[1]/text()').get()
            area = item.xpath('./div[1]/div[2]/div/a[2]/text()').get()
            location = f"{region} - {area}"
            house['location'] = location
            house['houseType'] = item.xpath('./div[1]/div[3]/div/text()').get()
            house['unitPrice'] = item.xpath('./div[1]/div[6]/div[2]/span/text()').get()
            totalPrice_num = item.xpath('./div[1]/div[6]/div[1]/span/text()').get()
            totalPrice = f"{totalPrice_num}万"
            house['totalPrice'] = totalPrice
            yield house