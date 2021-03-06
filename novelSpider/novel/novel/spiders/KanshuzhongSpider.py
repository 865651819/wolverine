import urllib

import redis
import scrapy
from pymongo import MongoClient
from scrapy.http import Request

r = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client.wolverine

SITE_URL = 'http://www.unionchina.top/novel'


class KanshuzhongSpider(scrapy.Spider):
    name = 'kanshuzhong'

    start_urls = ['http://www.kanshuzhong.com/book/104416/']
    id = 45

    def parse(self, response):

        # Parse novel's title
        title = response.xpath('//div[@class="book_title"]//h1/text()').extract()[0]
        print title

        # Parse novel's category
        category = response.xpath('//div[@class="top_left"]/a/text()').extract()[1]
        print category

        # download image
        avator = response.xpath('//div[@class="readtip"]//img/@src').extract()
        urllib.urlretrieve(avator[0], str(self.id) + '.jpg')

        nodes = response.xpath('//div[@class="readtip"]/node()').extract()
        summary = nodes[5]

        # Parse chapters
        chapter_els = response.xpath('//div[@class="bookcontent"]/dl/dd')

        chapters = []

        chapter_idx = 0
        for el in chapter_els:

            if chapter_idx > 100:
                break

            try:
                link = self.start_urls[0] + el.xpath('a/@href').extract()[0]
                print link

                chapter = {
                    "title": str((el.xpath('a/text()').extract()[0]).encode('utf-8')),
                    "index": str(chapter_idx)
                }
                # c = chapter['title'] + ' ' + chapter['link']
                # print c.encode('utf-8')
                # print "\n"
                chapters.append(chapter)
                yield Request(url=link,
                              callback=self.content_parse,
                              meta={
                                  "chapter_index": chapter_idx,
                                  "novel_id": self.id,
                                  "chapter_title": chapter['title']})
                chapter_idx += 1

            except:
                print 'Parsing failed.'
                print el
                raise
                pass

        cur_novel = {
            "title": title.encode('utf-8'),
            "id": self.id,
            "category": category.encode('utf-8'),
            "chapters": chapters,
            "summary": summary
        }
        db.novels.insert_one(cur_novel)

    def content_parse(self, response):
        chapter_index = response.meta.get('chapter_index')
        novel_id = response.meta.get('novel_id')
        chapter_title = response.meta.get('chapter_title')
        contents = response.selector.xpath('//div[@class="textcontent"]/text()').extract()
        res = ""
        for c in contents:
            res += str(c.encode('utf-8'))
        print 'parsed' + str(chapter_index)

        db.chapters.insert_one({
            "novel_id": novel_id,
            "chapter_index": chapter_index,
            "content": res,
            "title": chapter_title
        })
