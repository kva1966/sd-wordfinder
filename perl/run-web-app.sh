#!/bin/sh

carton
perl -Ilib -Ilocal/lib/perl5 "-mWordFinder::Web::App"
