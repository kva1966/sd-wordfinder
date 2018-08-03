# sd-wordfinder

## Spec

<https://gist.github.com/adamc00/898f686967dc4f097531cbfc303cfc6e>

## Run



## Assumptions, Limitations, Notes

Main dataset used to play is Linux-installed `/usr/share/dict/words`, around
99k words on my machine.

Index is completely in memory, no disk-serialised representation. Index built
as part of server start-up. In general, trading off space to get time gains.

Simple 2-level index: primary index is 4-char chunks, secondary is 1-char for
words of length less than 4 chars, nothing more sophisticated. Sweet spot for
this simple scheme is probably 4-char and 1-char combo. Implementation still
puts all this into one map however, not separate entities. The expectation is
that that there's a much smaller no. of < 4 char words (at least this is the 
case in the Linux dict words dataset, 1080 vs. 98091). 

Possibly, one could have dynamic levels falling back to a lower chunk size 
depending on the word being indexed, but this has not been implemented.

One-letter words are possible if they exist on the dataset, and not excluded 
(though it would have likely made my life easier).

Special characters like apostrophes are not filtered out, and treated as part
of the word and thus part of an index key, a letter by itself. Feature/Bug 
depending on how precise searching needs to be. More likely a bug. :-)

Everything is lower-cased, original case is not stored --- thus queries only 
ever return lowercased results. In particular, this has funny implications 
like not differentiating between acronyms and regular words, otherwise 
separate entries in the source data file.

Error conditions on building index:

* Blank words
* Empty iterable, unexpected, generally

On Docker, the index is built as part of server start-up, assumes the dataset
to be the container's `/usr/share/dict/words`, not externalised as a mount
variable.
