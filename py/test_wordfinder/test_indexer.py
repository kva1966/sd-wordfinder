import unittest

from test_wordfinder.util import Util, WORD_LIST
from wordfinder.indexer import Indexer, IndexType

Indexer.DEBUG = False

u = Util()


class BaseIndexerTest:
  def test_init_no_words(self):
    msg = 'Iterator not supplied or empty'
    u.expect_fail(lambda: self.new_indexer([]), msg)
    u.expect_fail(lambda: self.new_indexer(None), msg)

  def test_init_ok(self):
    self.new_indexer(WORD_LIST)

  def test_index_create_succeeds(self):
    self.new_indexer(WORD_LIST).index()

  def test_index_create_fails_with_empty_word(self):
    u.expect_fail(lambda: self.new_indexer(['zing', ' ', '', None]).index(), 'Blank/empty word')

  def new_indexer(self, data):
    pass


class HashIndexTest(BaseIndexerTest, unittest.TestCase):
  def new_indexer(self, data):
    return Indexer(data, IndexType.HASH)


class ListIndexTest(BaseIndexerTest, unittest.TestCase):
  def new_indexer(self, data):
    return Indexer(data, IndexType.LIST)
