from typing import Iterable, List

from wordfinder.index import WordIndex
from wordfinder import distribution_of

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

  def query_words_containing_only(self, letters: str) -> List[str]:
    max_depth = len(letters)
    results = []
    letter_dist = distribution_of(letters)

    def get_remaining(used: List[str]):
      remain = []
      for ch in letter_dist:
        ch_count = used.count(ch)
        if letter_dist[ch] > ch_count:
          remain.append(ch)
      return remain

    def traverse_depth(node: Node, collector: List[str], curr_depth: int):
      if node.is_word:
        w = ''.join(collector)
        results.append(w)

      if curr_depth == max_depth:
        return

      # At each depth we wish to go through the available letters
      for ch in get_remaining(collector):
        if ch in node.keys:
          collector.append(ch)
          next_node = node.keys[ch]
          traverse_depth(next_node, collector, curr_depth + 1)
          collector.pop() # explore next branch, clear last char

    traverse_depth(self, [], 0)
    return results


class NaryTree:
  def __init__(self):
    self.__root = Node()

  def insert(self, word: str) -> 'NaryTree':
    assert word
    self.__root.insert(word)
    return self

  def exists(self, word: str) -> bool:
    return False if not word else self.__root.exists(word)

  def query_words_containing_only(self, letters: str) -> Iterable[str]:
    if not letters:
      return []
    return self.__root.query_words_containing_only(letters)


class TreeIndex(WordIndex):
  """Nary tree-based index."""
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
    if not letters:
      return []

    lcletters = letters.lower()  # normalise
    words = self.__tree.query_words_containing_only(lcletters)
    return sorted(words) if sort else words

  def __str__(self):
    metadata = (
      '{}[wordsIndexed={}]'
    ).format(self.__class__.__name__, self.__word_count)

    if TreeIndex.DEBUG:
      return '{}\n'.format(metadata, str(self.__tree))
    else:
      return metadata
