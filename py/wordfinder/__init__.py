from collections import defaultdict

from typing import Dict



def distribution_of(word: str) -> Dict[str, int]:
  wdist = defaultdict(lambda: 0)
  for ch in word:
    wdist[ch] += 1
  return wdist

IndexTypes = {

}