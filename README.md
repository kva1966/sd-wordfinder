# sd-wordfinder

## Spec

<https://gist.github.com/adamc00/898f686967dc4f097531cbfc303cfc6e>



## Run A Pre-Built Image

```
#
# Assumes your Docker login/context is hub.docker.com
#

docker pull kva1966/sd-wordfinder:latest


#
# Run:
# 
# Replace /usr/share/dict/words with a valid host path if necessary
# Expecting a file with one word per line

docker run \
    -d \
    -p 8080:5000 \
    --name sd-wordfinder-zing \
    -v /usr/share/dict/words:/app/words \
    kva1966/sd-wordfinder:latest

```

## Build and Run from Source

```
#
# Clone
#

git clone git@github.com:kva1966/sd-wordfinder.git


#
# Build
#

cd sd-wordfinder/py
docker build -t sd-wordfinder:latest .


#
# Run:
# 
# Replace /usr/share/dict/words with a valid host path if necessary
# Expecting a file with one word per line

docker run \
    -d \
    -p 8080:5000 \
    --name sd-wordfinder-kapow \
    -v /usr/share/dict/words:/app/words \
    sd-wordfinder:latest
```


## Verify Container Up and Running

```
docker ps -a | grep sd-wordfinder

# Output better say "Up <time>"
# c954a9c25b24        kva1966/sd-wordfinder:latest   "python -m wordfinde…"   4 minutes ago       Up 4 minutes        0.0.0.0:8080->5000/tcp             sd-wordfinder-zing

docker logs --tail 10 <(name|hash) from docker ps>

# Expecting messages like so:
# ...
# [2018-08-09 02:29:02,725] INFO in app: Index Built -> TreeIndex[wordsIndexed=99171]
# * Serving Flask app "wordfinder-webapp" (lazy loading)
# * Environment: production
#   WARNING: Do not use the development server in a production environment.
#   Use a production WSGI server instead.
# * Debug mode: off
# * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
# Depending on the data size, this may take some time.

```


## Execute Queries

```
curl http://localhost:8080/ping

curl http://localhost:8080/wordfinder/mogalicious

```


## Notes

Main dataset used to play is Linux-installed `/usr/share/dict/words`, around
99k words on my machine.

### Indexing: Update 2018-08-09

Implement n-ary tree based indexing. Way faster than old hash and chunking
combo; more importantly, degrades much more gracefully with query/letter
count. Serves me right for taking the name of permutations in vain. :-|

Index is completely in-memory, no disk-serialised representation.


### Indexing: Old

Index is completely in-memory, no disk-serialised representation.

Simple 2-level index: primary index is 4-char chunks, secondary is 1-char for
words of length less than 4 chars. (Implementation still puts all this into one 
map however, not separate entities). The expectation is that that there's a much
smaller no. of < 4 char words (at least this is the case in the Linux dict words
dataset, 1080 vs. 98091). 

Possibly, one could have dynamic levels falling back to a lower chunk size 
depending on the word being indexed, but this has not been implemented. More
extensive Tree-esque structures and taking advantage of sorting are other
unexplored alternatives. This implementation is very much a combination of 
hashing and O(N) operations for reasonably low values of N depending on the 
data distribution across keys/buckets.

### Inputs and Outputs

One-letter words may be returned in the query result if they exist in the 
dataset; they are not excluded (though it would have likely made my life 
easier!).

Punctuation and other special characters are not filtered out, and treated as 
part of the word and thus part of an index key, a letter effectively. Feature/Bug 
depending on how precise searching needs to be. More likely a bug, I know. :-)

Everything is lower-cased, original case is not stored --- thus queries only 
ever return lowercased results. In particular, this has funny implications 
like not differentiating between acronyms and regular words, otherwise 
separate entries in, say, the Linux dictionary file.

Error conditions on building index, please beware when using your own file:

* Blank words
* Empty file, unexpected, generally


### Container

Very basic container; a Python process runs a Flask script wrapping the index.

Process doesn't cleanly handle SIGINT or whatever Docker uses to shutdown 
processes (need to read-up on this), and will just die without executing any 
clean-up code.

For this scenario, the data file is completely read and closed once the index 
is built, so not a big issue.

Only tested on Linux Mint Debian Edition 2 (LMDE2).


```

$ docker --version
Docker version 18.06.0-ce, build 0ffa825

$ cat /etc/debian_version 
8.11

```
