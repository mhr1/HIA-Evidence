#!/usr/bin/perl -w

##################################################################
#
#	Last updated 5/12/04 Mike Riley
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
print STDERR $query->param('mode');


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
		filename => 'hia_ad_dat.tpl',
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

# open an empty template XML file

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

	my $xml_ref = 0;
	my $ref_no;
	my @data_check = ();

# Find the highest reference

	foreach $ref_no(keys %{$doc2->{heTrafficTransReview}})
	{
		if($ref_no > $xml_ref)
		{	
			$xml_ref = $ref_no;
		}
	}

# Next available empty reference

	$xml_ref++;

# Stuff the data into that reference and into a hash for display

	$doc->{heTrafficTransReview}->{$xml_ref}
		{'aspect_of_health'} = [$query->param('aspect_of_health')];

	push @data_check,{key => 'aspect_of_health',
		value => $query->param('aspect_of_health')}; 

	$doc->{heTrafficTransReview}->{$xml_ref}
		{'aspect_of_regeneration'} = [$query->param('aspect_of_regeneration')];
	push @data_check,{key => 'aspect_of_regeneration',
		value => $query->param('aspect_of_regeneration')};

	$doc->{heTrafficTransReview}->{$xml_ref}
		{'author'} = [$query->param('author')];
	push @data_check,{key => 'author', 
		value => $query->param('author')};

	$doc->{heTrafficTransReview}->{$xml_ref}
		{'reference_no'} = [$query->param('reference_no')];
	push @data_check,{key => 'reference_no', 
		value => $query->param('reference_no')};

	$doc->{heTrafficTransReview}->{$xml_ref}
		{'study_details'} = [$query->param('study_details')];
	push @data_check,{key => 'study_details', 
		value => $query->param('study_details')};

	$doc->{heTrafficTransReview}->{$xml_ref}
		{'process'} = [$query->param('process')];
	push @data_check,{key => 'process', 
		value => $query->param('process')};

	$doc->{heTrafficTransReview}->{$xml_ref}
		{'health_outcome_effects'} = [$query->param('health_outcome_effects')];
	push @data_check,{key => 'health_outcome_effects', 
		value => $query->param('health_outcome_effects')};

	$doc->{heTrafficTransReview}->{$xml_ref}
		{'mediating_factors'} = [$query->param('mediating_factors')];
	push @data_check,{key => 'mediating_factors', 
		value => $query->param('mediating_factors')};

	$doc->{heTrafficTransReview}->{$xml_ref}
		{'notes'} = [$query->param('notes')];
	push @data_check,{key => 'notes', 
		value => $query->param('notes')};

#Save record to a temporary file

	open (fHandle, '>data/temp_file.xml') || die;

	print fHandle $newdoc->XMLout($doc);

	close fHandle;

# SEND DATA TO HTML
		
	$template->param(record_keys => \@data_check);
	print $template->output();

}

sub save_record
{
	print header;

	my $userinfo;

	my $template = HTML::Template->new
	(
		filename => 'dB_add.tpl',
		die_on_bad_params => 0,
		#loop_context_vars => 1,
		path => [ 'templates' ]
	);

# UPDATE KEYWORD FILES

	#Start with just thealthKw.xml

	#my $doc3 = XMLin('data/thealthKw.xml');
	
	if (validate_user($query->param("username"),$query->param("password"))) 
	{
		#system("XMLmerge.bat");
		XML_append("data/test_xml_data.xml", "data/temp_file.xml");
		$userinfo = "The record has been added to the database";
	}
	else
	{
		$userinfo = "Unable to add record - Bad password?";
	}
	
	$template->param(hia_info => $userinfo);
	print $template->output();
}

sub validate_user 
{
  my ($user,$passwd) = @_;
  my $file = 'data/users.xml';
  my $xs1 = XML::Simple->new();
  my $doc = $xs1->XMLin($file);

  if ($user ne "" && $passwd ne "") 
  {
	if ($doc->{user}->{$user}->{password} eq $passwd) 
	{
	  # this matches
	  return 1;
	} 
	else 
	{
	  #incorrect password
	  return 0;
	}
  } 
  else 
  {
	   # fields are empty
  }

  # For test - always validate password
  return 1;
}
  
sub XML_append
{
	my($file1, $file2) = @_;

	my @alldata = ();
	my $currentdata = ();
	my $dataitem = ();

	# Strip off top level header

    open(FILE, $file1) || die "Can't open file 1";

	print "Opening file 1";

    while(<FILE>) # special case of 'while(defined($a = <FILE>))'
					# works line by line
	{
		if(/<records>/) 
		{
			$currentdata = "";
		}

		elsif(/<\/records>/) 
		{
			push(@alldata, ($currentdata));
		}

		else 
		{	    
			$currentdata .= $_;	# .= concatenate string
		}
    }
    close(FILE);

	open(FILE, $file2) || die "Can't open file 2";

    while(<FILE>) # special case of 'while(defined($a = <FILE>))'
					# works line by line
	{
		if(/<records>/) 
		{
			$currentdata = "";
		}

		elsif(/<\/records>/) 
		{
			push(@alldata, ($currentdata));
		}

		else 
		{	    
			$currentdata .= $_;	# .= concatenate string
		}
    }
    close(FILE);

	open(FILE, ">".$file1);

	print FILE "<records>\n";

	foreach $dataitem (@alldata) 
	{
		print FILE $dataitem;
	}

	print FILE "</records>\n";

	close(FILE);
}
