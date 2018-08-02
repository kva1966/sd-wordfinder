from collections import defaultdict

from typing import Iterator, Set, Dict


class Index:
  DEBUG = False

  def __init__(self):
    # map of: letter -> setOf(word1, word2 ...)
    self.__idx = defaultdict(set)
    # building distribution takes a long time from profiling, cache it, more so
    # because per index key, words can be repeated making the cache worth it
    self.__word_distributions = {}

  def put(self, word: str) -> None:
    assert word, 'Blank/empty word'
    lcword = word.strip().lower()
    self.__store_distribution(lcword)
    for ch in lcword:
      self.__idx[ch].add(lcword)

  def query(self, letters: str) -> Set[str]:
    if not letters:
      return set()

    # normalise
    lcletters = letters.lower()

    # collect word sets for each letter
    word_sets = [self.__idx[ch] for ch in lcletters]

    # filter each set further to only matching words
    letter_dist = Index.__build_distribution(lcletters)

    filtered_sets = [
      self.__filter_matching_letters(wset, letter_dist)
      for wset in word_sets
    ]

    # return results without dupes.
    return {
      word for wordset in filtered_sets
      for word in wordset
    }

  def __filter_matching_letters(self, words: Set[str],
                                letter_distribution: Dict[str, int]) -> Set[str]:
    """
    We want words with length <= than the max letter count and only containing
    the expected letters, OR a subset thereof. Returns a new set containing
    only such words.
    """

    def word_acceptable(word: str):
      wdist = self.__word_distributions[word]
      for ch in wdist:
        ok = ch in letter_distribution and wdist[ch] <= letter_distribution[ch]
        if not ok:
          return False  # no point looking at next char
      return True

    return {w for w in words if word_acceptable(w)}

  def __store_distribution(self, word: str) -> None:
    wdist = Index.__build_distribution(word)
    self.__word_distributions[word] = wdist

  @staticmethod
  def __build_distribution(word: str) -> Dict[str, int]:
    wdist = defaultdict(lambda: 0)
    for ch in word:
      wdist[ch] += 1
    return wdist

  def key_count(self):
    return len(self.__idx)

  def __str__(self):
    # Needs to be trimmed for big indexes! But handy for testing.
    return str(self.__idx) if Index.DEBUG else (
      'Index[keyCount={}]'.format(self.key_count())
    )


class Indexer:
  DEBUG = False

  def __init__(self, word_iterator: Iterator[str]):
    assert word_iterator, 'Iterator not supplied or empty'
    self.word_iterator = word_iterator

  def index(self) -> Index:
    index = Index()
    i = 0

    for word in self.word_iterator:
      i += 1
      index.put(word)

    if Indexer.DEBUG:
      print('Indexed {} words, index key count {}'.format(i, index.key_count()))

    return index
