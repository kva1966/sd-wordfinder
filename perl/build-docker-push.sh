#!/bin/sh

# Build only
# docker build -t kva1966/sd-wordfinder-pl:latest .

docker build -t kva1966/sd-wordfinder-pl:latest . &&\
    docker push kva1966/sd-wordfinder-pl:latest
