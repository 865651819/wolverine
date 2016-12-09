import scrapy

from ip_pool.items import IPItem
from ip_pool.checkin import checkin, utils


class XiciSpider(scrapy.Spider):
    name = 'xici'

    # construct start urls
    start_urls = ['http://www.xicidaili.com/nn']
    for n in range(2, 3):
        start_urls.append('http://www.xicidaili.com/nn/' + str(n))

    def parse(self, response):
        rows = response.xpath('//table[@id="ip_list"]/tr')
        ip_items = []

        for row in rows:
            try:
                # validate ip and port
                ip_candidate = row.xpath('td[2]/text()').extract()
                port_candidate = row.xpath('td[3]/text()').extract()
                protocol_candidate = row.xpath('td[6]/text()').extract()
                if not ip_candidate or len(ip_candidate) == 0 or not utils.is_valid_ip(ip_candidate[0]):
                    continue
                if not port_candidate or len(port_candidate) == 0 or not utils.is_valid_port(port_candidate[0]):
                    continue
                if not protocol_candidate or len(protocol_candidate) == 0:
                    continue

                ip_item = IPItem()
                ip_item['ipAddress'] = str(ip_candidate[0])
                ip_item['port'] = str(port_candidate[0])

                ip_item = IPItem(
                    ipAddress=ip_candidate[0],
                    port=port_candidate[0],
                    type=protocol_candidate[0],
                )

                ip_items.append(ip_item)
            except (TypeError, NameError, RuntimeError):
                pass

        # save ip address
        checkin.save(ip_items, XiciSpider.name)
