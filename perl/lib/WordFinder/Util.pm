package WordFinder::Util;
use strict;
use warnings FATAL => 'all';

sub distribution_of {
  my ($word) = @_;
  my %wdist = ();

  foreach my $ch (split('', $word)) {
    if (exists $wdist{$ch}) {
      $wdist{$ch} += 1;
    } else {
      $wdist{$ch} = 1;
    }
  }

  return \%wdist;
}

sub trim {
  my ($s) = @_;

  if (!defined($s)) {
    return $s;
  }
  return $s =~ s/^\s+|\s+$//gr;
}

1;
