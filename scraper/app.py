import random
import os

from os.path import getsize
from scrapy.crawler import CrawlerProcess
from spider import DataSpider, TextItem

WORDS_FILE = 'words.txt'


def random_word():
    offset = random.randrange(getsize(WORDS_FILE))
    with open(WORDS_FILE) as file:
        file.seek(offset)
        file.readline()
        return file.readline()

if __name__ == '__main__':
    user, passwd, host, port = 'user', 'password', 'localhost', '27017'
    if 'TEXT_DB_SERVICE_HOST' in os.environ:
        user = os.getenv('TEXT_MONGODB_USER')
        passwd = os.getenv('TEXT_MONGODB_PASSWORD')
        host = os.getenv('TEXT_DB_SERVICE_HOST')
        port = os.getenv('TEXT_DB_SERVICE_PORT')

    # create the spider
    word = random_word()
    process = CrawlerProcess()
    process.crawl(DataSpider,
        start_urls=['https://www.google.com/search?q='+word],
        textdb={'user':user, 'passwd':passwd, 'host':host, 'port':port})
    process.start()
