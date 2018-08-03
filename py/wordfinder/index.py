from typing import Iterable, Set


class WordIndex:
  def put(self, word: str) -> None:
    pass

  def query(self, letters: str, sort: bool = False) -> Iterable[str]:
    pass


def chunk(word: str, chunk_len: int) -> Set[str]:
  assert chunk_len >= 1

  if not word:
    return set()

  if len(word) == 1:
    return {word}

  return {
    word[i:i + chunk_len]
    for i in range(0, len(word))
    if len(word[i:i + chunk_len]) == chunk_len
  }


