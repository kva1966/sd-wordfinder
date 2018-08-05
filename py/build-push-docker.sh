#!/bin/sh

docker build -t kva1966/sd-wordfinder:latest . &&\
    docker push kva1966/sd-wordfinder:latest

