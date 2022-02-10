#!/usr/bin/perl -w 

#	This ver checks the test dataBase
#
#	M. Riley 19/10/04
#
#

use CGI qw(:standard);
use CGI qw/-debug/;
use HTML::Template;
#use Text::Soundex;
use XML::Simple;
#use Data::Dumper;

my @order_of_headings = qw(	aspect_of_health
							aspect_of_regeneration
							author
							reference_no
							study_details
							study_design_and_sample
							outcomes_rel_unemployment
							field_4
							process
							process_used
							measure_social_cap
							health_outcomes
							health_outcome_effects
							key_issues_rel_he
							causal_pathways
							ref_long_study
							mediating_factors
							conclusion
							notes);
	

$returned_data = new CGI;
#print STDERR $query->param('mode');

print $returned_data->header;

my $record_key = $returned_data->param('ref');
my $info = $returned_data->param('info');

#print Dumper($info);


my $template = HTML::Template->new( filename => 'hia_edit.tpl',
				      die_on_bad_params => 0,
				      path => [ 'templates' ]);

my $filename = 'data/test_xml_data.xml';
my $doc = XMLin($filename);

#Find the highest reference

my $ref_no = 0;
my $xml_ref = 0;

foreach $ref_no(keys %{$doc->{heTrafficTransReview}})
{
	if($ref_no > $xml_ref)
	{	
		$xml_ref = $ref_no;
	}
}

#print @list_of_headings;

foreach $heading (@order_of_headings)
{
	foreach $key (keys %{$doc->{heTrafficTransReview}->{$record_key}}) 
	{
	   if($key eq $heading)
	   {
		  push @new_hia_edit_data,{key=> $key, 
	      value=>$doc->{heTrafficTransReview}->{$record_key}{$key}};
	   }
	}
}



$template->param(record_keys => \@new_hia_edit_data);
print "Displaying reference ", $record_key, " of ", $xml_ref;
print $template->output();
#print Dumper(@new_hia_edit_data);


