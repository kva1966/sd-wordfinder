import unittest

from test_wordfinder.util import Util, WORD_LIST
from wordfinder.indexer import Indexer

u = Util()


class IndexTest(unittest.TestCase):
  def test_index_query_null(self):
    index = Indexer(WORD_LIST).index()

    self.assertEqual(set(), index.query(None))
    self.assertEqual(set(), index.query(''))

  def test_index_query_basic(self):
    index = Indexer(WORD_LIST).index()

    self.assertEqual(
      {'do', 'dog', 'go', 'god'},
      index.query('dgo')
    )
    self.assertEqual(
      {'gone', 'gno', 'go'},
      index.query('noge')
    )

  def test_index_query_basic_sorted(self):
    index = Indexer(WORD_LIST).index()

    self.assertEqual(
      ['do', 'dog', 'go', 'god'],
      index.query('dgo', True)
    )
    self.assertEqual(
      ['gno', 'go', 'gone'],
      index.query('noge', True)
    )

  def test_index_query_results_must_contain_only_queried_letters_or_subset(self):
    index = Indexer(WORD_LIST).index()

    self.assertEqual(
      set(),
      index.query('wa')
    )
    self.assertEqual(
      set(),
      index.query('san')
    )
    self.assertEqual(
      {'iwa'},
      index.query('iwa')
    )
    self.assertEqual(
      {'jiwa', 'iwa'},
      index.query('jiwa')
    )
    self.assertEqual(
      {'arsanata', 'nata'},
      index.query('arsanata')
    )

  def test_index_query_letter_use_max_count_respected_1(self):
    index = Indexer(WORD_LIST).index()

    self.assertEqual(
      {'do', 'dog', 'go', 'god', 'dogg'},
      index.query('dgog')
    )

  def test_index_query_letter_use_max_count_respected_2(self):
    index = Indexer(WORD_LIST).index()

    self.assertEqual(
      {'do', 'dog', 'go', 'god', 'good'},
      index.query('dogo')
    )

  def test_index_query_letter_use_excess_query_letter_count_okay(self):
    index = Indexer(WORD_LIST).index()
    self.assertEqual(
      {'do', 'dog', 'go', 'god', 'good', 'dogg', 'doggg'},
      index.query('dogooggggg')
    )

