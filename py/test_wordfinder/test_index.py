import unittest

from test_wordfinder.util import Util, WORD_LIST
from wordfinder.index import chunk
from wordfinder.listindex import ListIndex
from wordfinder.indexer import Indexer, IndexType

u = Util()


class BaseIndexTest:
  def test_index_query_null(self):
    index = self.new_index(WORD_LIST)

    self.assertEqual(set([]), set(index.query(None)))
    self.assertEqual(set([]), set(index.query('')))

  def test_index_query_basic(self):
    ListIndex.DEBUG = False
    index = self.new_index(WORD_LIST)
    # print(index)

    self.assertEqual(
      {'do', 'dog', 'go', 'god'},
      set(index.query('dgo'))
    )
    self.assertEqual(
      {'gone', 'gno', 'go'},
      set(index.query('noge'))
    )
    self.assertEqual(
      {'m'},
      set(index.query('M'))
    )
    self.assertEqual(
      {'m', 'x'},
      set(index.query('Mx'))
    )
    self.assertEqual(
      {'rx', 'x'},
      set(index.query('rx'))
    )
    self.assertEqual(
      {'yz'},
      set(index.query('yz'))
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
      set([]),
      set(index.query('wa'))
    )
    self.assertEqual(
      set([]),
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


class TreeIndexTest(BaseIndexTest, unittest.TestCase):
  def new_index(self, data):
    return Indexer(data, IndexType.TREE).index()


class ModuleTests(unittest.TestCase):
  def test_chunk(self):
    self.assertEqual(
      set(),
      chunk('', 10)
    )
    self.assertEqual(
      set(),
      chunk('abcde', 10)
    )
    self.assertEqual(
      {'a'},
      chunk('a', 10)
    )
    self.assertEqual(
      {'a', 'b', 'c'},
      chunk('abc', 1)
    )
    self.assertEqual(
      {'ab', 'bc'},
      chunk('abc', 2)
    )
    self.assertEqual(
      {'ab', 'bc', 'cd'},
      chunk('abcd', 2)
    )
    self.assertEqual(
      {'abc', 'bcd'},
      chunk('abcd', 3)
    )
    self.assertEqual(
      {'abcd'},
      chunk('abcd', 4)
    )
    self.assertEqual(
      {'abcd', 'bcde'},
      chunk('abcde', 4)
    )
