import unittest

from test_wordfinder.util import Util, WORD_LIST
from wordfinder.indexer import Indexer

Indexer.DEBUG = False

u = Util()


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
    u.expect_fail(lambda: Indexer(['zing', ' ', '', None]).index(), 'Blank/empty word')


