import unittest

WORD_LIST = [
  'do', 'dog', 'go', 'god', 'good', 'gno', 'gone', 'dogg', 'doggg',
  'Iwa', 'Rahadian', 'Arsanata', 'Jiwa', 'nata'
]


class Util(unittest.TestCase):
  def expect_fail(self, fn, msg):
    try:
      fn()
      self.fail('Test passed, expected to fail!')
    except AssertionError as e:
      self.assertEqual(msg, str(e))
