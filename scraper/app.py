import random
import os
import traceback
import kubernetes.client as k8s

from os.path import getsize
from scrapy.crawler import CrawlerProcess
from spider import DataSpider

WORDS_FILE = 'words.txt'
SERVICEACCOUNT_LOCATION = '/var/run/secrets/kubernetes.io/serviceaccount/'

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
    with open(SERVICEACCOUNT_LOCATION + name) as f:
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
    k8s.configuration.ssl_ca_cert = SERVICEACCOUNT_LOCATION + 'ca.crt'
    # we assume the ConfigMap name is 'config'
    obj = k8s.CoreV1Api().read_namespaced_config_map('config', namespace)

    return obj.data['text_db_user'], obj.data['text_db_pass'], \
        os.getenv('TEXT_DB_SERVICE_HOST'), os.getenv('TEXT_DB_SERVICE_PORT')


if __name__ == '__main__':
    user, passwd, host, port = 'user', 'password', 'localhost', '27017'
    if 'KUBERNETES_SERVICE_HOST' in os.environ:
        try:
            user, passwd, host, port = read_configmap()
        except k8s.rest.ApiException as e:
            print("Error reading config map!", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
    # create the spider
    word = random_word()
    process = CrawlerProcess()
    process.crawl(DataSpider,
        start_urls=['https://www.google.com/search?q='+word],
        textdb={'user':user, 'passwd':passwd, 'host':host, 'port':port})
    process.start()
