from typing import Iterable

from collections import defaultdict

from wordfinder.index import WordIndex

DEBUG = False


class Node:
  """N-ary node, each node is a letter/character key that is part of a word.
  A node where one or more words terminates has its is_word attrib set to
  True. Handles sharing letters across words, and repeated letters in words,
  e.g. 'hello' and 'help' share the nodes for 'h', 'e', 'l', then split off
  into 'l' and 'p', the nodes containing 'o' and 'p' have is_word True. Subsets
  of words will consequently have their node's is_word be True, e.g. 'hello' and
  'hell', 'o' and the second 'l' node will have is_word True."""
  def __init__(self):
    self.keys = {}
    self.is_word = False

  def insert(self, word: str, idx: int = 0):
    if len(word) == idx:
      self.is_word = True
      return

    ch = word[idx]

    if ch in self.keys:
      self.keys[ch].insert(word, idx + 1)
    else:
      n = Node()
      self.keys[ch] = n
      n.insert(word, idx + 1)

  def exists(self, word: str, idx: int = 0) -> bool:
    if len(word) == idx:
      return self.is_word

    ch = word[idx]

    if ch in self.keys:
      return self.keys[ch].exists(word, idx + 1)

    return False


class NaryTree:
  def __init__(self):
    self.__root = Node()

  def insert(self, word: str):
    assert word
    self.__root.insert(word)
    return self

  def exists(self, word: str):
    return False if not word else self.__root.exists(word)


class TreeIndex(WordIndex):
  """Binary tree-based index."""
  DEBUG = False

  def __init__(self):
    self.__tree = NaryTree()
    self.__word_count = 0

  def put(self, word: str) -> None:
    assert word, 'Blank/empty word'
    assert word.strip(), 'Blank/empty word'

    lcword = word.strip().lower()

    self.__tree.insert(lcword)
    self.__word_count += 1

  def query(self, letters: str, sort: bool = False) -> Iterable[str]:
    pass

  def __str__(self):
    metadata = (
      '{}[wordsIndexed={}]'
    ).format(self.__class__.__name__, self.__word_count)

    if TreeIndex.DEBUG:
      return '{}\n'.format(metadata, str(self.__tree))
    else:
      return metadata
