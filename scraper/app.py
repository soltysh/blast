import random
import os

import kubernetes.client as k8s

from os.path import getsize
from scrapy.crawler import CrawlerProcess
from spider import DataSpider, TextItem

WORDS_FILE = 'words.txt'


def random_word():
    """
    Reads random word from the attached words.txt file.
    """
    offset = random.randrange(getsize(WORDS_FILE))
    with open(WORDS_FILE) as file:
        file.seek(offset)
        file.readline()
        return file.readline()

def read_file(name):
    """
    Reads configuration from serviceaccounts files.
    """
    with open('/var/run/secrets/kubernetes.io/serviceaccount/' + name) as f:
        return f.read()

def read_configmap():
    """
    Reads ConfigMap object storing secrets to databases.
    """

        namespace = read_file('namespace')
        k8s.configuration.host = 'https://{}:{}'.format(
            os.getenv('KUBERNETES_SERVICE_HOST'),
            os.getenv('KUBERNETES_SERVICE_PORT'))
        k8s.configuration.api_key_prefix['authorization'] = 'Bearer'
        k8s.configuration.api_key['authorization'] = read_file('token')
        k8s.configuration.ssl_ca_cert = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
        # we assume the ConfigMap name is 'config'
        obj = k8s.CoreV1Api().read_namespaced_config_map('config', namespace)
        return obj.data['text_db_user'], \
            obj.data['text_db_pass'], \
            os.getenv('TEXT_DB_SERVICE_HOST'), \
            os.getenv('TEXT_DB_SERVICE_PORT')


if __name__ == '__main__':
    user, passwd, host, port = 'user', 'password', 'localhost', '27017'
    if 'KUBERNETES_SERVICE_HOST' in os.environ:
        try:
            user, passwd, host, port = read_configmap()
        except k8s.rest.ApiException:
            print(e, file=sys.stderr)
            return
    # create the spider
    word = random_word()
    process = CrawlerProcess()
    process.crawl(DataSpider,
        start_urls=['https://www.google.com/search?q='+word],
        textdb={'user':user, 'passwd':passwd, 'host':host, 'port':port})
    process.start()
