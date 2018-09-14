package WordFinder::TreeIndex::Index;

use strict;
use warnings FATAL => 'all';
use Carp;
use WordFinder::TreeIndex::NaryTree;
use WordFinder::Util;

sub new {
  my ($class) = @_;
  return bless {
    class_name => $class,
    tree => WordFinder::TreeIndex::NaryTree->new,
    word_count => 0
  }
}

sub put {
  my ($self, $word) = @_;
  $word or croak 'Blank/empty word';
  WordFinder::Util::trim($word) or croak 'Blank/empty word';

  my $lcword = lc(WordFinder::Util::trim($word));

  $self->{tree}->insert($lcword);
  $self->{word_count} += 1;
}

sub query {
  my ($self, $letters, $sort) = @_;

  if (!$letters) {
    return [()];
  }

  my $lcletters = lc($letters);

  my $words = $self->{tree}->query_words_containing_only($lcletters);

  if ($sort) {
    my @sorted = sort @$words;
    return \@sorted;
  } else {
    return $words;
  }
}

sub to_string {
  my ($self) = @_;
  return sprintf("%s[wordsIndexed=%d]",
    $self->{class_name}, $self->{word_count});
}

1;
