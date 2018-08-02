from wordfinder.indexer import Indexer, Index
import unittest

Index.DEBUG = True

WORD_LIST_MEDIUM = [
  'Jiraiya',
  'Naruto',
  'Angel',
  'Cage',
  'Luke',
  'Jones',
  'Jessica',
  'Peter',
  'Parker',
  'Bandung',
  'Karate',
  'Club',
  'Go',
  'Good',
  'Gone',
  'Dog',
  'Iwa',
  'Rahadian',
  'Arsanata'
]

WORD_LIST_SMALL = [
  'do', 'dog', 'go', 'god', 'good', 'gno', 'gone'
]


class IndexerTest(unittest.TestCase):
  def test_init_no_words(self):
    msg = 'Iterator not supplied or empty'
    self.__fail(lambda: Indexer([]), msg)
    self.__fail(lambda: Indexer(None), msg)

  def test_init_ok(self):
    Indexer(WORD_LIST_SMALL)

  def test_index_create_succeeds(self):
    Indexer(WORD_LIST_SMALL).index()
    Indexer(WORD_LIST_MEDIUM).index()

  def test_index_create_fails_with_empty_word(self):
    self.__fail(lambda: Indexer(['zing', '']).index(), 'Blank/empty word')

  def test_index_query_null(self):
    index = Indexer(WORD_LIST_SMALL).index()
    self.assertEqual(set(), index.query(None))
    self.assertEqual(set(), index.query(''))

  def test_index_query_small_1(self):
    index = Indexer(WORD_LIST_SMALL).index()
    # print(index)
    self.assertEqual(
      {'do', 'dog', 'go', 'god'},
      index.query('dgo')
    )
    self.assertEqual(
      {'do', 'dog', 'go', 'god', 'good'},
      index.query('dogo')
    )
    self.assertEqual(
      {'gone', 'gno', 'go'},
      index.query('noge')
    )

  def __fail(self, fn, msg):
    try:
      fn()
      self.fail('Test passed, expected to fail!')
    except AssertionError as e:
      self.assertEqual(msg, str(e))
