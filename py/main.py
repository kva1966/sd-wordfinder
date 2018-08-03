from wordfinder.indexer import Indexer, IndexType

WORD_FILE_PATH = '/usr/share/dict/words'

Indexer.DEBUG = True

if __name__ == '__main__':
  with open(WORD_FILE_PATH) as f:
    index = Indexer(f, IndexType.LIST).index()

  print("Index built\n")

  try:
    while True:
      q = input("query: ")
      results = index.query(q, True)
      print("Results:\n {}\n\n".format(results))
  except (EOFError, KeyboardInterrupt):
    print("\nBye.")
  except Exception:
    raise
