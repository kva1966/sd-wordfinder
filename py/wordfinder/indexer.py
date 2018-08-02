from collections import defaultdict

from typing import Iterator, Set


class Index:
  DEBUG = False

  def __init__(self):
    # map of: letter -> setOf(word1, word2 ...)
    self.__idx = defaultdict(set)

  def put(self, word: str) -> None:
    assert word, 'Blank/empty word'
    lcw = word.strip().lower()
    for ch in lcw:
      self.__idx[ch].add(lcw)

  def query(self, letters: str) -> Set[str]:
    if not letters:
      return set()

    # normalise
    lcletters = letters.lower()

    # collect word sets for each letter
    word_sets = [self.__idx[ch] for ch in lcletters]

    # filter sets further to only matching words
    letter_set = set(lcletters)
    maxwordlen = len(lcletters)
    filtered_sets = [
      Index.__filter_matching_letters(s, letter_set, maxwordlen)
      for s in word_sets
    ]

    # return results without dupes.
    return {
      word for wordset in filtered_sets
      for word in wordset
    }

  @staticmethod
  def __filter_matching_letters(words: Set[str],
                                letter_set: Set[str],
                                maxwordlen: int) -> Set[str]:
    """
    We want words with length <= than the max letter count and only containing
    the expected letters, OR a subset thereof. Returns a new set containing
    only such words.
    """

    def to_set(word): return {ch for ch in word}

    return {
      w for w in words
      if len(w) <= maxwordlen and to_set(w).issubset(letter_set)
    }

  def __str__(self):
    # Needs to be trimmed for big indexes! But handy for testing.
    # Pandas does this stuff really nicely.
    return str(self.__idx) if Index.DEBUG else (
      'Index[keyCount={}]'.format(len(self.__idx))
    )


class Indexer:
  def __init__(self, word_iterator: Iterator[str]):
    assert word_iterator, 'Iterator not supplied or empty'
    self.word_iterator = word_iterator

  def index(self) -> Index:
    index = Index()
    for word in self.word_iterator:
      index.put(word)
    return index
