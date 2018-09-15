package WordFinder::Web::App;
use strict;
use warnings FATAL => 'all';

use Mojolicious::Lite;
use WordFinder::Indexer;

use constant IS_CONTAINERISED => defined $ENV{SD_WORDFINDER_CONTAINER};
use constant WORD_FILE_PATH => (IS_CONTAINERISED ? '/app/words' : '/usr/share/dict/words');

sub build_index {
  open my $word_file_fh, WORD_FILE_PATH
    or die 'Cannot read dictionary file[' . WORD_FILE_PATH . ']';
  my $index = WordFinder::Indexer->new($word_file_fh)->index();
  close $word_file_fh;

  return $index;
}

my $index = build_index();
app->log->info('Index built -> ' . $index->to_string);

get '/' => sub {
  my $c = shift;
  $c->render(text => $index->to_string);
};

get '/ping' => sub {
  my $c = shift;
  $c->render(text => "OK\n");
};

get '/wordfinder/:query' => sub {
  my $c = shift;
  my $q = $c->stash('query');
  $c->app->log->info("Querying[$q]");

  my $results = $index->query($q, 1);

  $c->render(json => $results);
};

app->mode(IS_CONTAINERISED ? 'production' : 'development');
app->log->info("Running in [" . app->mode . "] mode");

app->start('daemon', '-l', 'http://*:5000');

1;
