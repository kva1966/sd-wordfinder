from typing import Iterable

from wordfinder.index import WordIndex

DEBUG = False


class Node:
  """Binary nodes of letters in a word, each node is marked as being a word or not
  depending on where the final letter of a word terminates. Handles sharing letters
  across words, and repeated letters in words, e.g. 'hello' and 'help' share
  the nodes for 'h', 'e', 'l', then split off into 'l' and 'p'."""
  def __init__(self):
    self.ch = None
    self.left = None
    self.right = None
    self.is_word = False
    self.depth = 0

  def insert(self, word: str, idx: int):
    if len(word) == idx:
      self.is_word = True
      return

    ch = word[idx]

    if self.ch is None:
      self.ch = ch
      self.depth = idx
      self.insert(word, idx + 1)
    elif self.ch == ch:
      if self.depth == idx:
        self.insert(word, idx + 1) # skip to next, already inserted
      else:
        # same char at different index, always to left of node.
        if self.left is None:
          self.left = Node() # create if necessary
        self.left.insert(word, idx)
    elif ch < self.ch:
      if self.left is None:
        self.left = Node()
      self.left.insert(word, idx)
    else:
      if self.right is None:
        self.right = Node()
      self.right.insert(word, idx)

class TreeNode:
  def __init__(self, word: str):
    assert len(word) > 0
    self.root = Node()
    self.root.insert(word, 0)

  def insert(self, word: str):
    assert len(word) > 0
    self.root.insert(word, 0)

  def query(self, word: str):
    pass

class TreeIndex(WordIndex):
  """Binary tree-based index."""
  DEBUG = False

  def __init__(self):
    self.__root = None
    self.__word_count = 0

  def put(self, word: str) -> None:
    assert word, 'Blank/empty word'
    assert word.strip(), 'Blank/empty word'

    lcword = word.strip().lower()

    if self.__root is None:
      self.__root = TreeNode(lcword)
    else:
      self.__root.insert(lcword)

    self.__word_count += 1

  def query(self, letters: str, sort: bool = False) -> Iterable[str]:
    pass

  def __str__(self):
    metadata = (
      '{}[wordsIndexed={}]'
    ).format(self.__class__.__name__, self.__word_count)

    if TreeIndex.DEBUG:
      return '{}\n'.format(metadata, str(self.__root))
    else:
      return metadata
