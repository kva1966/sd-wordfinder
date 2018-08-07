import unittest

from wordfinder.treeindex import NaryTree


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

