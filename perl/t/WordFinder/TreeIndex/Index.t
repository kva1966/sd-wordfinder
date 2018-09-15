#!/usr/bin/perl
use strict;
use warnings;
use Carp;
use Data::Dumper;
use Test::More;

use WordFinder::TreeIndex::Index;


#
# Small List
#

my @small_list = qw(c bye hello hell hello meow by);
my $small_index = init_index(\@small_list);
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

my $medium_index = init_index(\@medium_list);
test_query($medium_index, 'dgo', [qw(do dog go god)]);
test_query($medium_index, 'dgog', [qw(do dog go god dogg)]);
test_query($medium_index, 'noge', [qw(gone gno go)]);
test_query($medium_index, 'M', [qw(m)]);
test_query($medium_index, 'rx', [qw(rx x)]);
test_query($medium_index, 'yz', [qw(yz)]);
test_query($medium_index, 'wa', [()]);
test_query($medium_index, 'san', [()]);
test_query($medium_index, 'iwa', [qw(iwa)]);
test_query($medium_index, 'jiwa', [qw(jiwa iwa)]);
test_query($medium_index, 'arsanata', [qw(arsanata nata)]);
test_query($medium_index, 'dgog', [qw(do dog go god dogg)]);
test_query($medium_index, 'dogo', [qw(do dog go god good)]);
test_query($medium_index, 'dogooggggg', [qw(do dog go god good dogg doggg)]);

done_testing();


#
# Util Functions
#

sub init_index {
  my ($items) = @_;
  my $index = WordFinder::TreeIndex::Index->new;

  foreach my $item (@$items) {
    $index->put($item);
  }

  return $index;
}

sub test_query {
  my ($index, $query, $expected_results) = @_;

  local *array_to_set = sub {
    my ($items) = @_;
    my %set = ();

    # init set with keys, and each set to undef
    @set{@$items} = ();

    return \%set;
  };

  my $results = $index->query($query);

  # print "Actual Array -> " . Dumper($results);
  # print "Expected Array -> " . Dumper($expected_results);

  my $result_set = array_to_set($results);
  my $expected_set = array_to_set($expected_results);

  # print "Actual Set -> " . Dumper($result_set);
  # print "Expected Set -> " . Dumper($expected_set);

  is_deeply(
    \array_to_set($results),
    \array_to_set($expected_results),
    'query[' . (defined($query) ? $query : '<undef>') . ']'
  )
}

