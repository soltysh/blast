import binascii
import sys

import psycopg2

class PostgreSQL():

    def __init__(self, username, password, host, port):
        try:
            self.conn = psycopg2.connect(user=username, password=password, \
                host=host, port=port, database='blast_image')
        except psycopg2.OperationalError:
            print("Could not connect to postgresql!", file=sys.stderr)
            self.conn = None

    def get(self, tag):
        result = []
        if self.conn:
            cur = self.conn.cursor()
            cur.execute("select tag, image from image where tag=%s", (tag, ))
            for rec in cur:
                # needs some magic to get to base64 form
                data = rec[1].tobytes()
                data = binascii.unhexlify(data)
                image = binascii.b2a_base64(data)
                print(image)
                result.append({'tag': rec[0], 'image': image.decode('utf-8')})
            cur.close()
        return result
