package WordFinder::TreeIndex::NaryTree;

use strict;
use warnings FATAL => 'all';
use Carp;

use WordFinder::TreeIndex::Node;
use WordFinder::Util;

sub new {
  my ($class) = @_;
  return bless {
    root => WordFinder::TreeIndex::Node->new
  }, $class;
}

sub insert {
  my ($self, $word) = @_;
  $word or croak "Word not supplied";
  $self->{root}->insert($word, 0);
  return $self;
}

sub exists {
  my ($self, $word) = @_;
  if (!defined $word) {
    return 0;
  }

  return $self->{root}->exists($word, 0);
}

sub query_words_containing_only {
  my ($self, $letters) = @_;

  if (!$letters) {
    return [()];
  }

  return $self->{root}->query_words_containing_only($letters);
}


1;
