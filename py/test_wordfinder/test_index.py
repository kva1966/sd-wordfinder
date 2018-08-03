import unittest

from test_wordfinder.util import Util, WORD_LIST
from wordfinder.indexer import Indexer, IndexType

u = Util()


class BaseIndexTest:
  def test_index_query_null(self):
    index = self.new_index(WORD_LIST)

    self.assertEqual(set(), index.query(None))
    self.assertEqual(set(), index.query(''))

  def test_index_query_basic(self):
    index = self.new_index(WORD_LIST)

    self.assertEqual(
      {'do', 'dog', 'go', 'god'},
      set(index.query('dgo'))
    )
    self.assertEqual(
      {'gone', 'gno', 'go'},
      set(index.query('noge'))
    )

  def test_index_query_basic_sorted(self):
    index = self.new_index(WORD_LIST)

    self.assertEqual(
      ['do', 'dog', 'go', 'god'],
      index.query('dgo', True)
    )
    self.assertEqual(
      ['gno', 'go', 'gone'],
      index.query('noge', True)
    )

  def test_index_query_results_must_contain_only_queried_letters_or_subset(self):
    index = self.new_index(WORD_LIST)

    self.assertEqual(
      set(),
      set(index.query('wa'))
    )
    self.assertEqual(
      set(),
      set(index.query('san'))
    )
    self.assertEqual(
      {'iwa'},
      set(index.query('iwa'))
    )
    self.assertEqual(
      {'jiwa', 'iwa'},
      set(index.query('jiwa'))
    )
    self.assertEqual(
      {'arsanata', 'nata'},
      set(index.query('arsanata'))
    )

  def test_index_query_letter_use_max_count_respected_1(self):
    index = self.new_index(WORD_LIST)

    self.assertEqual(
      {'do', 'dog', 'go', 'god', 'dogg'},
      set(index.query('dgog'))
    )

  def test_index_query_letter_use_max_count_respected_2(self):
    index = self.new_index(WORD_LIST)

    self.assertEqual(
      {'do', 'dog', 'go', 'god', 'good'},
      set(index.query('dogo'))
    )

  def test_index_query_letter_use_excess_query_letter_count_okay(self):
    index = self.new_index(WORD_LIST)
    self.assertEqual(
      {'do', 'dog', 'go', 'god', 'good', 'dogg', 'doggg'},
      set(index.query('dogooggggg'))
    )

  def new_index(self, data):
    pass


class HashIndexTest(BaseIndexTest, unittest.TestCase):
  def new_index(self, data):
    return Indexer(data, IndexType.HASH).index()


class ListIndexTest(BaseIndexTest, unittest.TestCase):
  def new_index(self, data):
    return Indexer(data, IndexType.LIST).index()
