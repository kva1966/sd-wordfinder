from wordfinder.indexer import Indexer, Index
from test_wordfinder.util import Util

import unittest

Index.DEBUG = True

WORD_LIST = [
  'do', 'dog', 'go', 'god', 'good', 'gno', 'gone', 'dogg', 'doggg',
  'Iwa', 'Rahadian', 'Arsanata', 'Jiwa', 'nata'
]

u = Util()


#
# Reading test_foo_bar_baz names like these makes me miss Groovy Spock-like
# frameworks.
#

class IndexerTest(unittest.TestCase):
  def test_init_no_words(self):
    msg = 'Iterator not supplied or empty'
    u.expect_fail(lambda: Indexer([]), msg)
    u.expect_fail(lambda: Indexer(None), msg)

  def test_init_ok(self):
    Indexer(WORD_LIST)

  def test_index_create_succeeds(self):
    Indexer(WORD_LIST).index()

  def test_index_create_fails_with_empty_word(self):
    u.expect_fail(lambda: Indexer(['zing', '']).index(), 'Blank/empty word')


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

