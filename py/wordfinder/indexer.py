from typing import Iterator

from wordfinder.index import Index


class Indexer:
  DEBUG = False

  def __init__(self, word_iterator: Iterator[str]):
    assert word_iterator, 'Iterator not supplied or empty'
    self.word_iterator = word_iterator

  def index(self) -> Index:
    index = Index()
    i = 0

    for word in self.word_iterator:
      i += 1
      index.put(word)

    if Indexer.DEBUG:
      print('Indexed {} words, index key count {}'.format(i, index.key_count()))

    return index
