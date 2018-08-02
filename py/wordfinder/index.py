from collections import defaultdict

from typing import Set, Dict, List, Iterable


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
    assert word.strip(), 'Blank/empty word'

    lcword = word.strip().lower()
    self.__store_distribution(lcword)
    for ch in lcword:
      self.__idx[ch].add(lcword)

  def query(self, letters: str, sort: bool = False) -> Iterable[str]:
    if not letters:
      return set()

    # normalise
    lcletters = letters.lower()

    # collect word sets for each letter and get a union of them all, as plenty of
    # repetition is likely, unnecessarily increasing the no. of words to process.
    word_sets = [self.__idx[ch] for ch in lcletters]
    words = Index.__union_of(word_sets)

    # filter each set further to only matching words
    results = self.__filter_matching_letters(words, lcletters)

    return sorted(results) if sort else results

  @staticmethod
  def __union_of(wordsets: List[Set[str]]) -> Set[str]:
    return {
      word
      for wset in wordsets
      for word in wset
    }

  def __filter_matching_letters(self, words: Set[str],
                                letters: str) -> Set[str]:
    """
    We want words with length <= than the max letter count and only containing
    the expected letters, OR a subset thereof. Returns a new set containing
    only such words.
    """
    letter_dist = Index.__build_distribution(letters)

    def word_acceptable(word: str):
      wdist = self.__word_distributions[word]

      for ch in wdist:
        ok = ch in letter_dist and wdist[ch] <= letter_dist[ch]
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
