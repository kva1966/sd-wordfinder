#!/bin/sh

carton install
perl -Ilib/ -Ilocal/lib/perl5 main.pl

