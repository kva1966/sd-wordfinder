#!/usr/bin/perl
use strict;
use warnings FATAL => 'all';
use Data::Dumper;
use Time::HiRes qw(gettimeofday);
use WordFinder::Indexer;

$Data::Dumper::Indent = 1;

use constant WORD_FILE_PATH => '/usr/share/dict/words';

sub _exit {
  print "\nBye.\n";
  exit 0;
}

$SIG{'INT'} = sub {
  _exit
};

open my $word_file_fh, WORD_FILE_PATH
  or die 'Cannot read dictionary file[' . WORD_FILE_PATH . ']';

my $index = WordFinder::Indexer->new($word_file_fh)->index();

close $word_file_fh;

print 'query: ';

while (my $q = <>) {
  chomp($q);
  my $start_secs = gettimeofday();
  my @results = @{$index->query($q, 1)};
  my $query_time_ms = (gettimeofday() - $start_secs) * 1000;
  my $result_list = Dumper(\@results);
  my $info = sprintf("
Results:
%s
%d words found.
Query took %d ms.\n
", $result_list, scalar @results, $query_time_ms);
  print $info;
  print 'query: ';
}

_exit;
