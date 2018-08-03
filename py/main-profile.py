from wordfinder.indexer import Indexer, IndexType


WORD_FILE_PATH = '/usr/share/dict/words'

Indexer.DEBUG = False

# INDEX_TYPE = IndexType.HASH
INDEX_TYPE = IndexType.LIST

if __name__ == '__main__':
  with open(WORD_FILE_PATH) as f:
    index = Indexer(f, INDEX_TYPE).index()
    print('Index built {}'.format(index))

  max_runs = 22

  queries = [
    'caligula',
    'supermanhasnobrains',
    'hello',
    'horatio',
    'mingle',
    'morticity',
    'itty',
    'bitty',
    'zoology',
    'dgo',
    'morons',
    'total',
    'delicious',
    'withholding',
    'abc',
    'eerraggg',
    'wwoentoosa'
  ]

  for i in range(0, max_runs):
    print('Run {} of {}'.format(i + 1, max_runs))
    for q in queries:
      index.query(q)
