import scrapy
import redis
import urllib
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

r = redis.StrictRedis(host='localhost', port=6379)

SITE_URL = 'http://www.unionchina.top/novel'


class KanshuzhongSpider(scrapy.Spider):
    name = 'kanshuzhong'

    start_urls = ['http://www.kanshuzhong.com/book/23729/']
    id = 3

    def parse(self, response):

        # Parse novel's title
        title = response.xpath('//div[@class="book_title"]//h1/text()').extract()[0]
        print title.encode('utf-8')

        # Parse novel's category
        category = response.xpath('//div[@class="top_left"]/a/text()').extract()[1]

        # download image
        avator = response.xpath('//div[@class="readtip"]//img/@src').extract()
        urllib.urlretrieve(avator[0], str(self.id) + '.jpg')

        # Parse chapters
        chapter_els = response.xpath('//div[@class="bookcontent"]/dl/dd')

        chapters = []

        chapter_idx = 0
        for el in chapter_els:

            try:
                link = self.start_urls[0] + el.xpath('a/@href').extract()[0]
                print link

                chapter = {
                    'title': el.xpath('a/text()').extract()[0].encode('utf-8'),
                    'link': SITE_URL + '/' + str(self.id) + '/' + str(chapter_idx)
                }
                # c = chapter['title'] + ' ' + chapter['link']
                # print c.encode('utf-8')
                # print "\n"
                chapters.append(chapter)
                if chapter_idx == 2 or chapter_idx == 3:
                    yield Request(url=link,
                                  callback=self.content_parse,
                                  meta={
                                      'chapter_index': str(chapter_idx),
                                      'novel_id': str(self.id),
                                      'chapter_title': chapter['title']})
                chapter_idx += 1

            except:
                print 'Parsing failed.'
                print el
                raise
                pass

        cur_novel = {
            'title': title,
            'id': self.id,
            'category': category,
            'chapters': chapters
        }

        r.set('novel:' + str(self.id), cur_novel)

    def content_parse(self, response):
        chapter_index = response.meta.get('chapter_index')
        novel_id = response.meta.get('novel_id')
        chapter_title = response.meta.get('chapter_title')
        contents = response.selector.xpath('//div[@class="textcontent"]/text()').extract()
        res = ""
        for c in contents:
            res += c.encode('utf-8')
        print res
        r.set('novel:' + novel_id + ':' + chapter_index, {
            'novel_id': novel_id,
            'chapter_index': chapter_index,
            'content': res,
            'chapter_title': chapter_title
        })
