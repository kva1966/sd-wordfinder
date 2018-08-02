import unittest


class Util(unittest.TestCase):
  def expect_fail(self, fn, msg):
    try:
      fn()
      self.fail('Test passed, expected to fail!')
    except AssertionError as e:
      self.assertEqual(msg, str(e))
