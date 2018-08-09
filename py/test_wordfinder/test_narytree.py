import unittest

from wordfinder.treeindex import NaryTree
from test_wordfinder.util import WORD_LIST

class NaryTreeTest(unittest.TestCase):
  def test_exists(self):
    t = NaryTree()
    items = ['c', 'bye', 'hello', 'hell', 'hello', 'meow']

    for item in items:
      t.insert(item)

    for item in items:
      self.assertTrue(t.exists(item))

    self.assertFalse(t.exists('h'))
    self.assertFalse(t.exists('he'))
    self.assertFalse(t.exists('hel'))
    self.assertFalse(t.exists('b'))
    self.assertFalse(t.exists('by'))

  def test_query_words_containing_small(self):
    t = NaryTree()
    items = ['c', 'bye', 'hello', 'hell', 'hello', 'meow', 'by']

    for item in items:
      t.insert(item)

    for item in items:
      self.assertTrue(t.exists(item))

    self.assertEqual(set(), set(t.query_words_containing_only(None)))
    self.assertEqual(set(), set(t.query_words_containing_only('')))

    self.assertEqual(
      set(),
      set(t.query_words_containing_only('h'))
    )
    self.assertEqual(
      {'hello', 'hell'},
      set(t.query_words_containing_only('hlleo'))
    )
    self.assertEqual(
      set(),
      set(t.query_words_containing_only('hl'))
    )
    self.assertEqual(
      {'bye', 'by'},
      set(t.query_words_containing_only('bye'))
    )
    self.assertEqual(
      {'meow'},
      set(t.query_words_containing_only('meow'))
    )
    self.assertEqual(
      {'c'},
      set(t.query_words_containing_only('c'))
    )

  def test_query_words_containing_medium(self):
    t = NaryTree()

    for word in WORD_LIST:
      t.insert(word)

    for word in WORD_LIST:
      self.assertTrue(t.exists(word))

    self.assertEqual(
      {'do', 'dog', 'go', 'god', 'dogg'},
      set(t.query_words_containing_only('dgog'))
    )
