import re
import sys

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from scrapy import Item, Field
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule

GOOGLE_RE = re.compile('https://www.google\.\w{2,3}')


class TextItem(Item):
    url = Field()


class DataSpider(CrawlSpider):
    name = 'data_spider'

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='r']"), callback='parse_item'),
    )

    def __init__(self, textdb=None, *a, **kw):
        super(DataSpider, self).__init__(*a, **kw)
        try:
            self._client = MongoClient('mongodb://{user}:{passwd}@{host}:{port}/blast_text'
                .format(**textdb))
            self._client.server_info()
        except ServerSelectionTimeoutError:
            self.logger.info("Could not connect to mongo, nothing will be saved!")
            self._client = None

    def parse_item(self, response):
        if GOOGLE_RE.match(response.url):
            return
        selector = Selector(response)
        title = selector.xpath('//title/text()').extract()[0]
        self.logger.info("Saving %s - %s", title, response.url)
        if self._client:
            try:
                self._client.blast_text.text.insert_one({'text': title, 'url': response.url})
            except Exception as e:
                print(e, file=sys.stderr)
