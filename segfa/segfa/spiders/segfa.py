import scrapy
from ..items import SegfaItem
from bs4 import BeautifulSoup

# 思否（SegmentFault）爬虫
class SegfaSpider(scrapy.Spider):
    name = "segfa"
    allowed_domains = ['segmentfault.com']
    # 初始URL
    start_urls = [
        "https://segmentfault.com/questions?page=%d" % (i+101) for i in range(300)
    ]

    # 爬取目录
    def parse(self, response):
        nodes = response.xpath("//section[@class='stream-list__item']")
        for node in nodes:
            href = node.xpath("div[@class='summary']/h2/a/@href").extract()
            '''
            # 只爬取被解决的问题
            if len(node.xpath("div[@class='qa-rank']/div[@class='answers answered solved']/small/text()").extract()) == 0:
                continue
            '''
            detailed_url = 'https://segmentfault.com'+href[0]
            yield scrapy.Request(detailed_url, callback=self.parse_detailed_page)

    # 爬取详细页面
    def parse_detailed_page(self, response):
        # 删除pre标签下的文本(转换成BeautifulSoup再处理)
        soup = BeautifulSoup(response.body, 'html5lib')
        for node in soup.find_all('pre'):
            node.extract()
        response = response.replace(body=bytes(str(soup), encoding='UTF-8'))

        qa = SegfaItem()
        # 标题（String）
        qa['title'] = response.xpath("//h1[@class='h3 post-topheader__info--title']/a/text()").extract()[0]
        # 标签（List）
        qa['tags'] = [s.strip(' \n') for s in response.xpath("//li[@class='tagPopup mb5']/a[@class='tag']/text()").extract()]
        # 描述（String）
        qa['desc'] = ','.join(response.xpath("//div[@class='question fmt']").xpath('string(.)').extract())
        # 非最佳答案（List）
        qa['answers_other'] = []
        for node in response.xpath("//article[@class='clearfix widget-answers__item']//div[@class='answer fmt']"):
           qa['answers_other'].append('.'.join(node.xpath('p').xpath('string(.)').extract()))
        # 最佳答案（String）
        qa['answer_best'] = ','.join\
            (response.xpath("//article[@class='clearfix widget-answers__item accepted']//div[@class='answer fmt']").xpath('string(.)').extract())
        return qa

