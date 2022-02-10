#!/usr/bin/perl -w

##################################################################
#
#
#
#
#
#
#
##################################################################

#use strict;
use CGI qw(:standard);
use CGI qw/-debug/;
use XML::Simple;
use HTML::Template;
use Data::Dumper;

$query = new CGI;
#print STDERR $query->param('mode');


if ($query->param('mode') eq "") 
{
	enter_record($query);
}
elsif($query->param('mode') eq "display_data")
{
	save_record($query);
}
else
{
	display_record($query);
}

sub enter_record
{
	print header;
	
	my $template = HTML::Template->new
	(
		filename => 'mytest.tpl',
		die_on_bad_params => 0,
		#loop_context_vars => 1,
		path => [ 'templates' ]
	);	
	
	print $template->output();
}

sub display_record
{	
	my($query) = @_;

	print header;

	my $template = HTML::Template->new
	(
		filename => 'hia_add.tpl',
		die_on_bad_params => 0,
		loop_context_vars => 1,
		path => [ 'templates' ]
	);

	#open an empty template XML file

	my $file = 'data/template.xml';

	my $xs = XML::Simple->new(noattr=>0, rootname=>"records", 
			keeproot=>0, keyattr=>{"heTrafficTransReview"=>"key"});
	my $doc = $xs->XMLin($file);

	my $xshealth = XML::Simple->new(noattr=>0, rootname=>"records", 
			keeproot=>0, keyattr=>{"health_keywords"=>"key"});
	my $healthdoc = $xshealth->XMLin($file);

	my $doc2 = XMLin('data/test_xml_data.xml');
	my $healthdoc2 = XMLin('data/thealthKw.xml');
 

	my $newdoc = XML::Simple->new( noattr=>0, rootname=>"records", 
			keeproot=>0, keyattr=>{"heTrafficTransReview"=>"key"});

	#push $doc, ('test text');

	#my $finaldoc = ('heTrafficTransReview'=>'hello');

	my $xml_ref = 0;
	my $ref_no;
	my @data_check = ();

	#Find the highest reference

	foreach $ref_no(keys %{$doc2->{heTrafficTransReview}})
	{
		if($ref_no > $xml_ref)
		{	
			$xml_ref = $ref_no;
		}
	}

	

	print Dumper($query->param('aspect_of_health'));

	print "<a href='etest/more_xml_data.xml'>";
	print "<p>XML merge status =  ", "<br />";
	print "<p>Aspect of regeneration:- ", param('aspect_of_regeneration'),"<br />";
	print "<p>Author:- ", param('author'),"</p>";
}

