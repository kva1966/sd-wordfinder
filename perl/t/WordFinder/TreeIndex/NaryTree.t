#!/usr/bin/perl
use strict;
use warnings;
use Carp;
use Data::Dumper;
use Test::More;

use WordFinder::TreeIndex::NaryTree;

my @WORD_LIST = qw(
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

#
# tests exists
#

my @items = qw(c bye hello hell hello meow);

sub init_index {
  my ($items) = @_;
  my $index = WordFinder::TreeIndex::NaryTree->new;

  foreach my $item (@$items) {
    $index->insert($item);
  }

  return $index;
}

sub array_to_set {
  my ($items) = @_;
  my %set = ();

  # print "arraytoset[" . $items . "]";
  #
  # init set with keys, and each set to undef
  @set{@$items} = ();

  return \%set;
}

sub test_all_items_exist {
  my ($index, $items) = @_;

  foreach my $item (@$items) {
    ok($index->exists($item), "exists[" . $item . "]");
  }
}

sub test_query {
  my ($index, $query, $expected_results) = @_;

  my $results = $index->query_words_containing_only($query);

  # print "Actual Array -> " . Dumper($results);
  # print "Expected Array -> " . Dumper($expected_results);

  my $result_set = array_to_set($results);
  my $expected_set = array_to_set($expected_results);

  # print "Actual Set -> " . Dumper($result_set);
  # print "Expected Set -> " . Dumper($expected_set);

  is_deeply(
    \array_to_set($results),
    \array_to_set($expected_results),
    'query_words_containing_only[' . (defined($query) ? $query : '<undef>') . ']'
  )
}

# my $index1 = init_index [qw(c bye hello hell hello meow)];
# test_all_items_exist $index1, \@items;


#
# Small List
#

my $small_index = init_index [qw(c bye hello hell hello meow by)];
test_all_items_exist $small_index, \@items;
test_query($small_index, undef, [()]);
test_query($small_index, '', [()]);
test_query($small_index, 'h', [()]);
test_query($small_index, 'hlleo', [qw(hello hell)]);
test_query($small_index, 'hl', [()]);
test_query($small_index, 'bye', [qw(bye by)]);
test_query($small_index, 'meow', [qw(meow)]);
test_query($small_index, 'c', [qw(c)]);


#
# Medium List
#

my $medium_index = init_index \@WORD_LIST;
test_all_items_exist $medium_index, \@WORD_LIST;
test_query($medium_index, 'dgog', [qw(do dog go god dogg)]);

done_testing();
