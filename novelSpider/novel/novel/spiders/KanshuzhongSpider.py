import scrapy
import redis
import urllib
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


        avator = response.xpath('//div[@class="readtip"]//img/@src').extract()
        print avator
        urllib.urlretrieve(avator[0], str(self.id) + '.jpg')


        summary = response.xpath('//div[@class="readtip"]')[0]
        #print summary

        #print [summary.xpath('''.//div/node()[count(preceding-sibling::br)=%d]
        #                   [not(self::br)]''' % i).extract()
        #       for i in range(0, len(summary.xpath('.//div/br')) + 1)][0]

        chapter_els = response.xpath('//div[@class="bookcontent"]/dl/dd')

        chapters = []

        chapter_idx = 0
        for el in chapter_els:
            chapter = {
                'title': el.xpath('a/text()').extract()[0].encode('utf-8'),
                'link': self.start_urls[0] + el.xpath('a/@href').extract()[0]
            }
            # c = chapter['title'] + ' ' + chapter['link']
            # print c.encode('utf-8')
            # print "\n"
            chapters.append(chapter)
            if chapter_idx == 2 or chapter_idx == 3:
                yield Request(url=chapter['link'],
                              callback=self.content_parse,
                              meta={
                                'chapter_index': str(chapter_idx),
                                'novel_id': str(self.id)})
            chapter_idx += 1

        cur_novel = {
            'title': title,
            'chapters': chapters
        }

        r.set('novel:' + str(self.id), cur_novel)

    def content_parse(self, response):
        chapter_index = response.meta.get('chapter_index')
        novel_id = response.meta.get('novel_id')
        contents = response.selector.xpath('//div[@class="textcontent"]/text()').extract()
        res = ""
        for c in contents:
            res += c.encode('utf-8')
        print res
        r.set('novel:' + novel_id + ':' + chapter_index, res)
