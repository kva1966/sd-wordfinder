package WordFinder::Indexer;
use strict;
use warnings FATAL => 'all';
use WordFinder::TreeIndex::Index;
use 5.010;

sub new {
  my ($class, $word_fh) = @_;
  return bless {
    word_fh => $word_fh
  }, $class;
}

sub index {
  my ($self) = @_;
  my $fh = $self->{word_fh};
  my $index = WordFinder::TreeIndex::Index->new;

  while (my $line = <$fh>) {
    chomp($line);
    $index->put($line);
  }

  say $index->to_string;

  return $index;
}

1;
