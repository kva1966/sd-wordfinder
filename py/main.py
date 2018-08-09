from wordfinder.indexer import Indexer, IndexType
from time import time

WORD_FILE_PATH = '/usr/share/dict/words'

Indexer.DEBUG = True

if __name__ == '__main__':
  with open(WORD_FILE_PATH) as f:
    index = Indexer(f, IndexType.TREE).index()

  print("Index built\n")

  try:
    while True:
      q = input("query: ")
      start_secs = time()
      results = index.query(q, True)
      query_time_ms = (time() - start_secs) * 1000
      result_list = list(results)
      info = """
Results:
{}
{} words found.
Query took {} ms.     
""".format(result_list, len(result_list), query_time_ms)
      print(info)
  except (EOFError, KeyboardInterrupt):
    print("\nBye.")
  except Exception:
    raise
