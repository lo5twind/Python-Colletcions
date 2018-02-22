from scrapy.spiders import Spider
from scrapy.http import Request
from scrapyspider.items import ScrapyspiderItem 

class MilphSpider(Spider):
    name = 'milph'
    start_urls = ['http://milph.net']


    def parse(self, response):
        url = response.url
        if url == MilphSpider.start_urls[0]:
            for i in response.xpath('//div[@class="face"]'):
                try:
                    new_url = i.xpath('a/@href').re("http://.*\.php")[0]
                except Exception as e:
                    print 'error dealing url[%s]: %s' % (i.extract(), e)
                    continue
                # print new_url
                yield Request(new_url, callback=self.parse)
        elif 'gallery' in url:
            if url.endswith('php'):
                jpg = response.xpath('//img').re("\d+\.jpg")
                # url: http://xxx.yy/category/z.php
                # host: http://xxx.yy/category/
                lurl = url.rsplit('/', 1)
                host_url = lurl[0]
                # lurl[-1] = jpg
                # jpg_url = '/'.join(lurl)
                # print 'dealing pic url[%s]' % jpg_url 
                item = ScrapyspiderItem()
                print 'dealing pic url: %s' % [ '/'.join([host_url, jpg_url]) for jpg_url in jpg ]
                item['image_urls'] = [ '/'.join([host_url, jpg_url]) for jpg_url in jpg ]
                yield item
            else:
                print 'dealing gallery url[%s]' % url
                for i in response.xpath('//div[@class="item"]'):
                    pic_url = ''.join([url, i.xpath('a/@href').extract()[0]])
                    yield Request(pic_url, callback=self.parse)
        else:
            print 'dealing category url[%s]' % url
            for i in response.xpath('//div[@class="tplace"]'):
                gallery_urls = i.xpath('a/@href').re("http://milforia.com/gallery.*")
                for g_url in gallery_urls:
                    yield Request(g_url, callback=self.parse)