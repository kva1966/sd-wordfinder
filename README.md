# sd-wordfinder

## Spec

<https://gist.github.com/adamc00/898f686967dc4f097531cbfc303cfc6e>


## Assumptions/Limitations

Main dataset used to play is Linux-installed `/usr/share/dict/words`.

Index is completely in memory, no disk-serialised representation. Index built
as part of server start-up.

Special characters like apostrophes are not filtered out, and treated as an
index key, a letter by itself. Feature/Bug depending on how precise searching 
needs to be. More likely a bug. :-)

Everything is lower-cased, original case not stored in index and indexed
data --- thus queries only ever return lowercased results. In particular, this
has funny implications like not differentiating between acronyms and regular
words, otherwise separate entries in the source data file.

Terribly hash-reliant. Tree-like structures and thinking about sorting may yield
a better-performing design, but I've simply used what's available in stock 
Python. (And I'll likely have to brush up on a data structures text were I to
think deeper!).

Error conditions on building index:

* Blank words
* Empty iterable, unexpected.
