from flask import Flask, json
from http import HTTPStatus
from logging import INFO
from os import environ

from wordfinder.indexer import Indexer, IndexType

is_containerised = environ.get('SD_WORDFINDER_CONTAINER')

WORD_FILE_PATH = '/app/words' if is_containerised else '/usr/share/dict/words'

app = Flask('wordfinder-webapp')

app.logger.setLevel(INFO)

with open(WORD_FILE_PATH) as f:
  index = Indexer(f, IndexType.LIST).index()
  app.logger.info('Index Built -> %s', index)


@app.route('/')
def home():
  return str(index), HTTPStatus.OK


@app.route('/ping')
def ping():
  return 'OK\n', HTTPStatus.OK


@app.route('/wordfinder/<query>')
def wordfinder(query):
  app.logger.info('Querying[%s]', query)
  results = index.query(query, True)
  return json.jsonify(results)


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)
