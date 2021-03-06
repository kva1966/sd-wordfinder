from collections import defaultdict

from typing import Dict, Iterable


def distribution_of(word: str) -> Dict[str, int]:
  wdist = defaultdict(lambda: 0)
  for ch in word:
    wdist[ch] += 1
  return wdist


def distribution_of2(chars: Iterable[str]) -> Dict[str, int]:
  wdist = defaultdict(lambda: 0)
  for ch in chars:
    wdist[ch] += 1
  return wdist
