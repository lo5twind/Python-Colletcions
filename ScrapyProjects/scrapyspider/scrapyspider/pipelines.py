# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class ScrapyspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ScrapyspiderImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            # print 'get_media_requests: %s' % image_url
            yield Request(image_url)

    def item_completed(self, results, item, info):
        print 'item_completed: %s' % results
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url
        # 'url': 'http://www.example.com/images/product1.jpg'
        lurl = url.split('/')
        try:
            category = '/'.join(lurl[-3:-1])
            image_name = lurl[-1]
        except KeyError:
            category = 'unknow'
            image_name = '%s.jpg' % hashlib.sha1(to_bytes(url)).hexdigest()

        # print 'save file to: %s/%s' % (category, image_name)
        return '%s/%s' % (category, image_name)
