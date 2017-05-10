import os
import sys

from flask import Flask
from flask_restful import Resource, Api
from flask_restful.utils import cors

from db import Mongo

app = Flask(__name__)
api = Api(app)
api.decorators = [cors.crossdomain(
    origin="*", headers=['accept', 'Content-Type'],
    methods=['HEAD', 'OPTIONS', 'GET', 'PUT', 'POST', 'DELETE'])]

class BlastText(Resource):

    def __init__(self):
        if 'TEXT_DB_SERVICE_HOST' in os.environ:
            self.db = Mongo(os.getenv('MONGODB_USER'), \
                os.getenv('MONGODB_PASSWORD'), \
                os.getenv('TEXT_DB_SERVICE_HOST'), \
                os.getenv('TEXT_DB_SERVICE_PORT'))
        else:
            self.db = Mongo('user', 'password', 'localhost', '27017')

    def get(self, text):
        items = []
        try:
            for obj in self.db.get(text):
                items.append({'id': str(obj['_id']), 'url': obj['url'], 'text': obj['text']})
        except Exception as e:
            print(e, file=sys.stderr)
        return items


api.add_resource(BlastText, '/blast/api/v1.0/text/<string:text>')

if __name__ == '__main__':
    app.run(debug=os.getenv('BLAST_DEBUG')=='True')
