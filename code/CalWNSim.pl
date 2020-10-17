#!/usr/bin/perl
use strict;
use warnings;
use WordNet::QueryData;

use WordNet::Similarity::lch;
use WordNet::Similarity::hso;
use WordNet::Similarity::jcn;
use WordNet::Similarity::lesk;
use WordNet::Similarity::lin;
use WordNet::Similarity::res;
use WordNet::Similarity::vector;
use WordNet::Similarity::wup;

my $sense1='';
my $sense2='';
my $merge ='';
my $lch='';
my $hso='';
my $jcn='';
my $leskvalue='';
my $linvalue='';
my $resvalue='';
my $vecvalue='';
my $wupvalue='';


open(my $fh, "</Users/gary/Documents/2020Fall/IntroNLP/project/OntoNotes_SensesPairs.csv")
  or die "Could not open file $!";

open(my $out, ">>/Users/gary/Documents/2020Fall/IntroNLP/project/note_pairs_wnsimilarity.csv")
  or die "Could not open wnsim file $!";
print $out "sense1,sense2,lch,hso,jcn,leskvalue,linvalue,resvalue,vecvalue,wupvalue,merge\n";
while (my $row = <$fh>) {
  chomp $row;
  print "$row\n";
  my @fields = split "," , $row;
  $sense1 = $fields[2];
  $sense2 = $fields[3];
  $merge = $fields[4];


  my $wn = WordNet::QueryData->new;
  my $measure = WordNet::Similarity::lch->new ($wn);

  $lch = $measure->getRelatedness($sense1, $sense2);
  #print "lch= $lch\n";

  my $object = WordNet::Similarity::hso->new($wn);
  $hso = $object->getRelatedness($sense1, $sense2);
  #print "hso= $hso\n";

  my $rel = WordNet::Similarity::jcn->new($wn);
  $jcn = $rel->getRelatedness($sense1, $sense2);
  #print "jcn= $jcn\n";

  my $lesk = WordNet::Similarity::lesk->new($wn);
  $leskvalue = $lesk->getRelatedness($sense1, $sense2);
  #print "lesk= $leskvalue\n";

  my $lin = WordNet::Similarity::lin->new($wn);
  $linvalue = $lin->getRelatedness($sense1, $sense2);
  #print "lin= $linvalue\n";

  my $res = WordNet::Similarity::res->new($wn);
  $resvalue = $res->getRelatedness($sense1, $sense2);
  #print "res= $resvalue\n";

  my $vector = WordNet::Similarity::vector->new($wn);
  $vecvalue = $vector->getRelatedness($sense1, $sense2);
  #print "vector= $vecvalue\n";

  my $wup = WordNet::Similarity::wup->new($wn);
  $wupvalue = $wup->getRelatedness($sense1, $sense2);
  #print "wup= $wupvalue\n";

  print $out "$sense1,$sense2,$lch,$hso,$jcn,$leskvalue,$linvalue,$resvalue,$vecvalue,$wupvalue,$merge\n";
  }

print "done\n";
