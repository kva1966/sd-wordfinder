#!/bin/sh

docker run \
    -d \
    -p 8080:5000 \
    --name sd-wordfinder-pl \
    -v /usr/share/dict/words:/app/words \
    kva1966/sd-wordfinder-pl:latest
