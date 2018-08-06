from collections import defaultdict
from itertools import permutations as perms

from statistics import median, mean
from typing import Iterable, List, Set

from wordfinder import distribution_of
from wordfinder.index import WordIndex, chunk


class ListIndex(WordIndex):
  """Replace buckets holds lists rather than sets, faster, but may take
  more memory with duplicate words -- assume dictionary files have unique
  entries generally. Main index is still a map/hash.

  Initially this was a minor variation on the hashsets, single char index keys.
  Now enhanced a bit to have configurable index key lengths for speed."""
  DEBUG = False

  # Sweet spot appears to be around 3 and 4 for medium sized words
  # and the ability to query them with a small no. of letters
  CHUNK_LEN = 4

  def __init__(self):
    # map of: letter -> list(word1, word2 ...)
    self.__idx = defaultdict(list)
    # building distribution takes a long time from profiling, cache it, more so
    # because per index key, words can be repeated making the cache worth it
    self.__word_distributions = {}
    self.__word_count = 0

  def put(self, word: str) -> None:
    assert word, 'Blank/empty word'
    assert word.strip(), 'Blank/empty word'

    lcword = word.strip().lower()
    self.__store_distribution(lcword)

    # Small words, in the minority, can go into smaller lists indexed by the
    # first letter. Of course, if our chunk size is much bigger, or our data
    # distributions are vastly different, we may need to revisit this.
    if len(lcword) < ListIndex.CHUNK_LEN:
      self.__idx[lcword[0]].append(lcword)
    else:
      assert len(lcword) >= ListIndex.CHUNK_LEN
      for chk in chunk(lcword, ListIndex.CHUNK_LEN):
        self.__idx[chk].append(lcword)

    self.__word_count += 1

  def query(self, letters: str, sort: bool = False) -> Iterable[str]:
    if not letters:
      return []

    lcletters = letters.lower()  # normalise

    # incoming letters have no inherent ordering, where as the index chunks in
    # order, so we take the cost here of getting permutations of the letters,
    # one or more of which should match index items
    index_keys = [key for key in ListIndex.__perms(lcletters)]

    # collect word lists for each index key and get a union of them all, as
    # plenty of repeated words per index, unnecessarily increasing the no. of
    # words to process.
    word_lists = [self.__idx[key] for key in index_keys]
    words = ListIndex.__union_of(word_lists)

    # We want words with length <= than the max letter count and only containing
    # the expected letters, OR a subset thereof. Returns a new set containing
    # only such words.
    lettersdist = distribution_of(lcletters)

    def word_acceptable(word: str):
      wdist = self.__word_distributions[word]
      for ch in wdist:
        ok = ch in lcletters and wdist[ch] <= lettersdist[ch]
        if not ok:
          return False  # no point looking at next char
      return True

    results = [w for w in words if word_acceptable(w)]

    return sorted(results) if sort else results

  @staticmethod
  def __union_of(wordlists: List[List[str]]) -> Set[str]:
    return {
      word
      for wset in wordlists
      for word in wset
    }

  @staticmethod
  def __perms(lcletters: str) -> List[str]:
    # There's no inherent ordering to query letters, and we support single words
    # so, we want both permutations of the letters for faster look-up on smaller
    # lists, but also single letter look-ups, for one-letter word corner cases
    single_letter_keys = [ch for ch in lcletters]

    if len(lcletters) < ListIndex.CHUNK_LEN:
      return single_letter_keys

    # The larger the query length, the worse this performs, of course, perms lead
    # to very big numbers.
    chunked_keys = [''.join(p) for p in perms(lcletters, ListIndex.CHUNK_LEN)]

    return single_letter_keys + chunked_keys

  def __store_distribution(self, word: str) -> None:
    wdist = distribution_of(word)
    self.__word_distributions[word] = wdist

  def key_count(self):
    return len(self.__idx)

  def __bucket_lengths(self):
    return [len(self.__idx[key]) for key in self.__idx]

  def __str__(self):
    bucket_lengths = self.__bucket_lengths()
    median_len = median(bucket_lengths)
    mean_len = mean(bucket_lengths)

    # Needs to be trimmed for big indexes! But handy for testing.
    metadata = (
        'ListIndex[keyCount={},' +
        'meanBucketLen={},' +
        'medianBucketLen={},' +
        'wordsIndexed={}]'
    ).format(self.key_count(), mean_len, median_len, self.__word_count)

    if ListIndex.DEBUG:
      return '{}\n'.format(metadata, str(self.__idx))
    else:
      return metadata
