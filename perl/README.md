# sd-wordfinder

## Spec

<https://gist.github.com/adamc00/898f686967dc4f097531cbfc303cfc6e>

## Run A Pre-Built Image

```
#
# Assumes your Docker login/context is hub.docker.com
#

docker pull kva1966/sd-wordfinder-pl:latest


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
    kva1966/sd-wordfinder-pl:latest

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

cd sd-wordfinder/perl
docker build -t sd-wordfinder-pl:latest .


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
    sd-wordfinder-pl:latest
```

## Verify Container Up and Running

```
docker ps -a | grep sd-wordfinder

# Output better say "Up <time>"
# a0fbf319ba3a        kva1966/sd-wordfinder-pl:latest   "perl -Ilib/ -mWordF…"   9 seconds ago       Up 8 seconds        0.0.0.0:8080->5000/tcp 

docker logs --tail 10 <(name|hash) from docker ps>

# Expecting messages like so:
# ...
# [Sat Sep 15 06:05:08 2018] [info] Index built -> WordFinder::TreeIndex::Index[wordsIndexed=99171]
# [Sat Sep 15 06:05:08 2018] [info] Running in [production] mode
# [Sat Sep 15 06:05:08 2018] [info] Listening at "http://*:5000"


```


## Execute Queries

As per the same section in top-level readme, same API.


# Notes

The Perl version has only ported over the n-ary tree-based index. See the
the top-level `README.md` **Notes** section for further discussion.
