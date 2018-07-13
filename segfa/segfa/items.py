# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 定义爬取内容
class SegfaItem(scrapy.Item):
    # 问题标题
    title = scrapy.Field()
    # 问题标签
    tags = scrapy.Field()
    # 问题描述
    desc = scrapy.Field()
    # 最佳答案
    answer_best = scrapy.Field()
    # 答案
    answers_other = scrapy.Field()
