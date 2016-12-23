import scrapy
import redis
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

r = redis.StrictRedis(host='localhost', port=6379)


class KanshuzhongSpider(scrapy.Spider):
    name = 'kanshuzhong'

    start_urls = ['http://www.kanshuzhong.com/book/87102/']
    id = 1

    def parse(self, response):

        title = response.xpath('//div[@class="book_title"]//h1/text()').extract()[0]
        print title.encode('utf-8')

        category = response.xpath('//div[@class="top_left"]/a/text()').extract()[1]
        print category

        summary = response.xpath('//div[@class="readtip"]')[0]
        #print summary

        print [summary.xpath('''.//div/node()[count(preceding-sibling::br)=%d]
                           [not(self::br)]''' % i).extract()
               for i in range(0, len(summary.xpath('.//div/br')) + 1)][0]

        chapter_els = response.xpath('//div[@class="bookcontent"]/dl/dd')

        chapters = []

        for el in chapter_els:
            chapter = {
                'title': el.xpath('a/text()').extract()[0].encode('utf-8'),
                'link': self.start_urls[0] + el.xpath('a/@href').extract()[0]
            }
            # c = chapter['title'] + ' ' + chapter['link']
            # print c.encode('utf-8')
            # print "\n"
            chapters.append(chapter)

        # yield Request(url=chapters[1]['link'], callback=self.content_parse)

        cur_novel = {
            'title': title,
            'chapters': chapters
        }

        r.set('novel:' + str(self.id), cur_novel)

    def content_parse(self, response):
        contents = response.selector.xpath('//div[@class="textcontent"]/text()').extract()
        res = ""
        for c in contents:
            res += c.encode('utf-8')
        print res
