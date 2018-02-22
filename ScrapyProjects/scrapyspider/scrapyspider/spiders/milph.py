from scrapy.spiders import Spider
from scrapy.http import Request

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
                jpg = response.xpath('//img').re("\d+\.jpg")[0]
                lurl = url.split('/')
                lurl[-1] = jpg
                jpg_url = '/'.join(lurl)
                print 'dealing pic url[%s]' % jpg_url 
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