import os
import sys

from flask import Flask
from flask_restful import Resource, Api
from flask.ext.restful.utils import cors

from db import PostgreSQL

app = Flask(__name__)
api = Api(app)
api.decorators = [cors.crossdomain(
    origin="*", headers=['accept', 'Content-Type'],
    methods=['HEAD', 'OPTIONS', 'GET', 'PUT', 'POST', 'DELETE'])]

class BlastImage(Resource):

    def __init__(self):
        if 'IMAGE_DB_SERVICE_HOST' in os.environ:
            self._db = PostgreSQL(os.getenv('POSTGRESQL_USER'), \
                os.getenv('POSTGRESQL_PASSWORD'), \
                os.getenv('IMAGE_DB_SERVICE_HOST'), \
                os.getenv('IMAGE_DB_SERVICE_PORT'))
        else:
            self._db = PostgreSQL('user', 'password', 'localhost', '5432')

    def get(self, tag):
        items = []
        try:
            for obj in self._db.get(tag):
                items.append({'tag': obj['tag'], 'image': obj['image']})
        except Exception as e:
            print(e, file=sys.stderr)
        return items


api.add_resource(BlastImage, '/blast/api/v1.0/image/<string:tag>')

if __name__ == '__main__':
    app.run(debug=os.getenv('BLAST_DEBUG')=='True')
