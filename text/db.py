import sys

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

class Mongo():

    def __init__(self, username, password, host, port):
        try:
            self.client = MongoClient('mongodb://{}:{}@{}:{}/blast_text'
                .format(username, password, host, port))
            self.client.server_info()
        except ServerSelectionTimeoutError:
            print("Could not connect to mongo!", file=sys.stderr)
            self.client = None

    def get(self, text):
        result = []
        if self.client:
            collection = self.client.blast_text.text
            for obj in collection.find({'text': {'$regex': text}}):
                result.append(obj)
        return result

