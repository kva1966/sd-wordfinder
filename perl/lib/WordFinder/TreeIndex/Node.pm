package WordFinder::TreeIndex::Node;

use strict;
use warnings FATAL => 'all';

# N-ary node, each node is a letter/character key that is part of a word.
# A node where one or more words terminates has its is_word attrib set to
# True. Handles sharing letters across words, and repeated letters in words,
# e.g. 'hello' and 'help' share the nodes for 'h', 'e', 'l', then split off
# into 'l' and 'p', the nodes containing 'o' and 'p' have is_word True. Subsets
# of words will consequently have their node's is_word be True, e.g. 'hello' and
# 'hell', 'o' and the second 'l' node will have is_word True.


sub new {
  my ($class) = @_;
  return bless {
    keys    => {},
    is_word => 0
  }, $class;
}

sub insert {
  my ($self, $word, $idx) = @_;

  if (length($word) == $idx) {
    $self->{is_word} = 1;
    return
  }

  my $ch = substr($word, $idx, 1);

  if (exists $self->{keys}{$ch}) {
    $self->{keys}{$ch}->insert($word, $idx + 1);
  } else {
    my $n = WordFinder::TreeIndex::Node->new();
    $self->{keys}{$ch} = $n;
    $n->insert($word, $idx + 1);
  }
}

sub exists {
  my ($self, $word, $idx) = @_;

  if (length($word) == $idx) {
    return $self->{is_word};
  }

  my $ch = substr($word, $idx, 1);

  if (exists $self->{keys}{$ch}) {
    return $self->{keys}{$ch}->exists($word, $idx + 1);
  }

  return 0;
}


sub query_words_containing_only {
  my ($self, $letters) = @_;
  my $max_depth = length($letters);
  my @results = ();
  my $letter_dist = WordFinder::Util::distribution_of($letters);

  local *get_remaining = sub {
    my ($used) = @_;
    my @used = @$used;
    my @remain = ();
    foreach my $ch (keys %$letter_dist) {
      my $ch_count = grep { $_ eq  $ch } @used;
      if ($letter_dist->{$ch} > $ch_count) {
        push @remain, $ch;
      }
    }
    return \@remain;
  };

  local *traverse_depth = sub {
    my ($node, $collector_ref, $curr_depth) = @_;
    my @collector = @$collector_ref;

    if ($node->{is_word}) {
      my $w = join('', @collector);
      push @results, $w;
    }

    if ($curr_depth == $max_depth) {
      return;
    }

    # At each depth we wish to go through the available letters
    foreach my $ch (@{get_remaining(\@collector)}) {
      if (exists $node->{keys}{$ch}) {
        push @collector, $ch;
        my $next_node = $node->{keys}{$ch};
        traverse_depth($next_node, \@collector, $curr_depth + 1);
        pop @collector;
      }
    }
  };

  traverse_depth($self, [()], 0);
  return \@results;
}

1;
