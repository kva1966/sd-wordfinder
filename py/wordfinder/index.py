from typing import Iterable


class WordIndex:
  def put(self, word: str) -> None:
    pass

  def query(self, letters: str, sort: bool = False) -> Iterable[str]:
    pass
