#!/usr/bin/perl
use strict;
use warnings;
use Test::More;
use WordFinder::Util;

#
# Tests for distribution_of
#


is_deeply(\WordFinder::Util::distribution_of("hello"), \{
  'h' => 1,
  'e' => 1,
  'l' => 2,
  'o' => 1
}, "letter distribution of 'hello'");

is_deeply(\WordFinder::Util::distribution_of("meheelloom"), \{
  'e' => 3,
  'h' => 1,
  'l' => 2,
  'o' => 2,
  'm' => 2
}, "letter distribution of 'meheelloom'");

sub test_trim {
  my ($input, $expected) = @_;
  is(WordFinder::Util::trim($input), $expected, 'Trim[' . $input . ']');
}

test_trim(undef, undef);
test_trim('', '');
test_trim('   hello', 'hello');
test_trim('hello  ', 'hello');
test_trim("\n\rwhy so serious\t\n\r", 'why so serious');


done_testing();


