#!/usr/bin/perl
use strict;
use warnings;
use Carp;
use Data::Dumper;
use Test::More;

use WordFinder::TreeIndex::NaryTree;

#
# Small List
#

my @small_list = qw(c bye hello hell hello meow);
my $small_index = init_tree(\@small_list);
test_all_items_exist($small_index, \@small_list);


#
# Medium List
#

my @medium_list = qw(
  do
  dog
  go
  god
  good
  gno
  gone
  dogg
  doggg
  Iwa
  Rahadian
  Arsanata
  Jiwa
  nata
  m
  x
  yz
  rx
);
my $medium_index = init_tree(\@medium_list);
test_all_items_exist($medium_index, \@medium_list);

done_testing();


#
# Util Functions
#

sub init_tree {
  my ($items) = @_;
  my $index = WordFinder::TreeIndex::NaryTree->new;

  foreach my $item (@$items) {
    $index->insert($item);
  }

  return $index;
}

sub test_all_items_exist {
  my ($index, $items) = @_;

  foreach my $item (@$items) {
    ok($index->exists($item), "exist[$item]");
  }
}
