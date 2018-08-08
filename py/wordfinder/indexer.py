from enum import Enum
from typing import Iterator

from wordfinder.hashindex import HashIndex
from wordfinder.index import WordIndex
from wordfinder.listindex import ListIndex
from wordfinder.treeindex import TreeIndex


class IndexType(Enum):
  HASH = 1
  LIST = 2
  TREE = 3

class Indexer:
  DEBUG = False

  def __init__(self, word_iterator: Iterator[str], index_type: IndexType = IndexType.LIST):
    assert word_iterator, 'Iterator not supplied or empty'
    self.word_iterator = word_iterator
    self.index_type = index_type

  def index(self) -> WordIndex:
    idx_type = self.index_type
    if idx_type == IndexType.HASH:
      index = HashIndex()
    elif idx_type == IndexType.LIST:
      index = ListIndex()
    elif idx_type == IndexType.TREE:
      index = TreeIndex()
    else:
      raise Exception("Unknown index type {}".format(idx_type))
    i = 0

    for word in self.word_iterator:
      i += 1
      index.put(word)

    if Indexer.DEBUG:
      print('Indexed {} words\n{}'.format(i, index))

    return index
