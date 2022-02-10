#!/usr/bin/perl -w 

######################################################################
#
#  HIA Evidence Search 
#
#  Ver. 1.00 by Ella Rice & Tom King
#  Ver. 2.00 by Mike Riley (mcriley@supanet.com)
#  
######################################################################

use CGI qw(:standard);
use CGI qw/-debug/;
use HTML::Template;
use Text::Soundex;
use XML::Simple;
use Data::Dumper;


$query = new CGI;

print STDERR $query->param('mode');

if ($query->param('mode') eq "") 
{
  start_page($query);
}
 
elsif ($query->param('mode') eq "showref") 
{
  show_reference($query);
} 

elsif ($query->param('mode') eq "fullrecord")
{
  show_full_record($query);
} 

elsif ($query->param('mode') eq "fullrecordedit")
{
  show_full_record_edit($query);
} 

elsif ($query->param('mode') eq "submitedit")
{
  full_record_save($query);
} 

elsif ($query->param('mode') eq "addrecord") 
{
  enter_record($query);
} 

elsif ($query->param('mode') eq "completed_form") 
{
  display_record($query);
}

elsif ($query->param('mode') eq "display_data") 
{
  save_record($query);
}

elsif ($query->param('mode') eq "newrecordtype") 
{
  new_full_record($query);
} 

else 
{
  print $query->header;
  do_work($query);
}

#close(dump);

sub start_page
{
print $query->header;

  my $template = HTML::Template->new( filename => 'form.tpl',
				      die_on_bad_params => 0,
				      path => [ 'templates' ]);

  #my $doc = XMLin('data/healthKw.xml');

  my $file = 'data/healthKw.xml';
  my $xs1 = XML::Simple->new();
  my $doc = $xs1->XMLin($file);

  foreach $key (keys (%{$doc->{health_keywords}})) 
  {
      $doc->{health_keywords}->{$key}{ref}=$key;
      push @health_keywords, $doc->{health_keywords}->{$key};
  }

  @health_keywords = sort { $a->{keyword} cmp $b->{keyword} } @health_keywords;
  $template->param(health_keywords_loop=>\@health_keywords);

  my $file2 = 'data/regenerationKw.xml';
  my $xs2 = XML::Simple->new();
  my $doc2 = $xs2->XMLin($file2);

#  my $doc2 = XMLin('data/regenerationKw.xml');

  foreach $key2 (keys (%{$doc2->{regeneration_keywords}})) 
  {
      $doc2->{regeneration_keywords}->{$key2}{ref}=$key2;
      push @regeneration_keywords, $doc2->{regeneration_keywords}->{$key2};
  }

  @regeneration_keywords = sort { $a->{keyword} cmp $b->{keyword} } @regeneration_keywords;
  $template->param(regeneration_keywords_loop=>\@regeneration_keywords);

  #print Dumper(\@regeneration_keywords);

#  my $doc3 = XMLin('data/all_xml_data.xml');
  
#  foreach $key3 (keys (%{$doc3->{heTrafficTransReview}})) 
 # {
#      $doc3->{heTrafficTransReview}->{$key3}{ref}=$key3;
#      push @author_keywords,  $doc3->{heTrafficTransReview}->{$key3};
#  }

#  @author_keywords = sort { $a->{author} cmp $b->{author} }@author_keywords;

#  $template->param(author_keywords_loop=>\@author_keywords);

  #print Dumper($doc3);

  my $file4 = 'data/authorName.xml';
  my $xs4 = XML::Simple->new();
  my $doc4 = $xs4->XMLin($file4);

  foreach $key4 (keys (%{$doc4->{author_keyword}})) 
  {
      $doc4->{author_keyword}->{$key4}{ref}=$key4;
      push @author_keywords,  $doc4->{author_keyword}->{$key4};
  }

  @author_keywords = sort { $a->{author} cmp $b->{author} }@author_keywords;

  $template->param(author_keywords_loop=>\@author_keywords);

#   $author = $doc->{heTrafficTransReview}->{$key}->{author};

  print $template->output();
}

#do_work method

sub do_work 
{
  my($query) = @_;

#Global array - @results
 @results = ();

  my $template = HTML::Template->new
  (
    filename => 'results.tpl',
    die_on_bad_params => 0,
	loop_context_vars => 1,
    path => [ 'templates' ]
  );

  my $file = 'data/all_xml_data.xml';
  my $xs1 = XML::Simple->new();
  my $doc = $xs1->XMLin($file);

#  print keys %{$doc->{heTrafficTransReview}};

  my @result_set = ();

## this is where we check our criteria
# this needs some rethinking to cope with the "AND" nature
# of filling in multiple boxes on the form, i think these ifs
# should all be nested but it ugly to read

  print STDERR $query->param("author"), "\n";



  $author_cgi = $query->param("author");
  $author_soundex = soundex($query->param("author"));


  $aspectofh_cgi = $query->param('aspectofh');
  $aspectofh_soundex = soundex($query->param('aspectofh'));

  $aspectofr_cgi = $query->param("aspectofr");
  $aspectofr_soundex = soundex($query->param("aspectofr"));



  foreach $key (keys (%{$doc->{heTrafficTransReview}})) 
  {
    $score = 0;
    $author = $doc->{heTrafficTransReview}->{$key}->{author};
    $aspectofh = $doc->{heTrafficTransReview}->{$key}->{aspect_of_health};
    $aspectofr = $doc->{heTrafficTransReview}->{$key}->{aspect_of_regeneration};

    #$score++ if (( (soundex($author) eq soundex ($query->param("author"))
     #   && $query->param("author") ne "" )));

    if ($author_cgi ne "") 
    {
      $score++ if (soundex($author) eq $author_soundex);

      foreach $part (split / /, $author) 
      {
	    $score++ if (soundex($part) eq $author_soundex);
      }
    }

    if (($aspectofr_cgi ne "") && ($aspectofh_cgi ne ""))
    {
      $score++ if ((soundex($aspectofr) eq $aspectofr_soundex) && (soundex($aspectofh) eq $aspectofh_soundex));
    }

    elsif (($aspectofr_cgi ne "") && ($aspectofh_cgi eq ""))
    {
      $score++ if (soundex($aspectofr) eq $aspectofr_soundex);

      foreach $reg_Key_part (split / /, $aspectofr) 
      {
	    $score++ if (soundex($reg_Key_part) eq $aspectofr_soundex);
      }
    }
 
    elsif (($aspectofh_cgi ne "") && ($aspectofr_cgi ne ""))
    {
      $score++ if (soundex($aspectofh) eq $aspectofh_soundex);

      foreach $health_Key_part (split / /, $aspectofh) 
      {
	    $score++ if (soundex($health_Key_part) eq $aspectofh_soundex);
      }
    }

    $score++ if (($query->param('freetextsearch') ne "") && text_match($query->param('freetextsearch'),$query->param('textsearchtype'), %{$doc->{heTrafficTransReview}->{$key}} ))  ;

    $aspectofh_form = $query->param('aspectofh');
    $aspectofr_form = $query->param('aspectofr');

    if(($aspectofh_form ne "") && ($aspectofr_form ne ""))
    {
      $score++ if (($aspectofh =~ /^.*($aspectofh_form).*$/i ) && ($aspectofr =~ /^.*($aspectofr_form).*$/i ));
    }

    elsif ($aspectofh_form ne "")
    {
      $score++ if ($aspectofh =~ /^.*($aspectofh_form).*$/i );
    }

    elsif ($aspectofr_form ne "")
    {
      $score++ if ($aspectofr =~ /^.*($aspectofr_form).*$/i );
    }

#print Dumper($score);

    if ($score >= 1) 
    {
      # this is a hit
      $count++; 

      $doc->{heTrafficTransReview}->{$key}{ref}=$key;
      push @result_set, $doc->{heTrafficTransReview}->{$key};
    } 
    else 
    {
      # this is a miss
      $score = 0;
    }
  }

#print Dumper("\nThis is the result set");
#print Dumper(@result_set);

#  foreach $entry (@result_set) 
#  {
#    foreach $subkey (keys %{$entry}) 
#    {
#      print STDERR "$subkey=>$entry->{$subkey}\n";
#
#      if ($entry->{$subkey} =~ /HASH/) 
#      {
#        $entry->{$subkey} = "";
#      }
#    }
#  }
 
  $template->param(number_returned =>$count);
  $template->param(result_set=>\@result_set);

  print $template->output();
}

sub text_match 
{
  my($terms,$type,%hash) = @_;
  @terms = split / /, $terms; 

  foreach $key (keys %hash) 
  {
    my $count=0;

    foreach $term (@terms) 
    {
      if ($hash{$key} =~ /$term/i) 
      {
        $count++;
 
        #print "$hash{$key} <b>contains</b> $term <b>count=$count</b><p>";
      }
    } 

    if ($type eq "Any" && $count>0) 
    {
      return 1;
    } 
    elsif ($type eq "All" && $count == length @terms) 
    {
      return 1;
    }  
    else 
    {

    }
  }
  return 0;
}

sub show_reference 
{
  my($query) = @_;
  my $template = HTML::Template->new
  (
         filename => 'reference.tpl',
         die_on_bad_params => 0,
	     loop_context_vars => 1,
         path => [ 'templates' ]
  );

  my $file = 'data/refs.xml';
  my $xs1 = XML::Simple->new();
  my $doc = $xs1->XMLin($file);

  (@refs) = split /,/, $query->param('ref');
  @ref_array = ();

  foreach $ref (@refs) 
  {
    $ref =~ s/\.00//;
    %foo = %{$doc->{reference}->{$ref}};
    $foo{ref}=$ref;
#    push @ref_array, \%foo;
    push @ref_array, {details => $foo{details}, ref=>$ref};
  }

print STDERR Dumper(\@ref_array);
  $template->param(ref_array=>\@ref_array);  
#  $template->param(ref=> $feck);

  print $query->header;
  print $template->output();

}

sub show_full_record 
{
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

  my %key_transform = 
  (
    "author" => "Author",
    "aspect_of_regeneration" => "Aspect of Regeneration", 
	"aspect_of_health" => "Aspect of Health", 
	"reference_no" => "Reference No",
	"study_design_and_sample" => "Study design and sample",
	"health_outcomes" => "Health outcome/effects",
	"health_outcome_effects" => "Health outcome/effects",
	"process" => "Process", 
	"mediating_factors" => "Mediating Factors",
	"notes" => "Notes",
	"study_details" => "Study Details",
	"process_used" => "Process",
	"causal_pathways" => "Causal pathways discussed",
	"outcomes_rel_unemployment" => "Key health outcomes related to unemployment",
	"field_4" => "Social capital defined as...",
	"conclusion" => "Overall results/Conclusion",
	"key_issues_rel_he" => "Key issues related to health",
	"measure_social_cap" => "Measure of social capital",
	"ref_long_study" => "Refs to longitudinal studies?"
  );

  my($query) = @_;
  my $template = HTML::Template->new
  (
		 filename => 'fullrecord.tpl',
		 die_on_bad_params => 0,
		 loop_context_vars => 1,
		 path => [ 'templates' ]
  );
	  
  $record_key = $query->param('ref');

  my $file = 'data/all_xml_data.xml';
  my $xs1 = XML::Simple->new();
  my $doc = $xs1->XMLin($file);

  @record_keys = ();

  foreach $heading (@order_of_headings)
  {
	  foreach $key (keys %{$doc->{heTrafficTransReview}->{$record_key}}) 
	  {
	    if($key eq $heading)
		{
			$keynice = $key_transform{$key};

			if ($doc->{heTrafficTransReview}->{$record_key}{$key} =~ /HASH/) 
			{
			  push @record_keys, {key=>$keynice,  value=>"", key_orig=>$key};
			} 
			else 
			{
			  push @record_keys, {key=>$keynice,  value=>$doc->{heTrafficTransReview}->{$record_key}{$key}, key_orig=>$key};
			}
		}
	  }
  }

  $template->param(record_keys=>\@record_keys);
  print $query->header;
  $template->param(ref=>$record_key);
  print $template->output();
	  
}

	
sub show_full_record_edit 
{
  my($query) = @_;
  my $template = HTML::Template->new
  (
    filename => 'fullrecordedit.tpl',
	die_on_bad_params => 0,
	loop_context_vars => 1,
	path => [ 'templates' ]
  );
	  
  $record_key = $query->param('ref');

  my $file = 'data/all_xml_data.xml';
  my $xs1 = XML::Simple->new();
  my $doc = $xs1->XMLin($file);

  @record_keys = ();

  foreach $key (sort keys %{$doc->{heTrafficTransReview}->{$record_key}}) 
  {
	$keynice = $key;
	$keynice =~ s/_/ /g;

	if ($doc->{heTrafficTransReview}->{$record_key}{$key} =~ /HASH/) 
	{
	  push @record_keys, {key=>$keynice,  value=>"", key_orig=>$key};
	} 
	else 
	{
	  push @record_keys, {key=>$keynice,  value=>$doc->{heTrafficTransReview}->{$record_key}{$key}, key_orig=>$key};
	}
  }

  $template->param(record_keys=>\@record_keys);
  $template->param(ref=>$record_key);
  print $query->header;
  print $template->output();
}

sub full_record_save 
{
  my($query) = @_;
  my $template = HTML::Template->new
  (
	filename => 'fullrecord.tpl',
	die_on_bad_params => 0,
	loop_context_vars => 1,
	path => [ 'templates' ]
  );

  $record_key = $query->param('ref');

  my $file = 'data/all_xml_data.xml';
  my $xs1 = XML::Simple->new(forcearray=>1);
# my $xs2 = XML::Simple->new( noattr=>1, rootname=>"records", keyattr=>["key"]);
  my $xs2 = XML::Simple->new( noattr=>0, rootname=>"records", keeproot=>0, keyattr=>{"heTrafficTransReview"=>"key"});
  my $doc = $xs1->XMLin($file);

  @record_keys = ();
	  
  foreach $key (sort keys %{$doc->{heTrafficTransReview}->{$record_key}}) 
  {
	$keynice = $key;
	$keynice =~ s/_/ /g;
	$data = $query->param($key);

	# Strip out all whitespace
	$data =~ s/\s/ /g;

	# Truncate trailing space
	$data =~ s/\s*$//g;
	$doc->{heTrafficTransReview}->{$record_key}{$key}=[$data];

	# First element of array, (all array only have one element!)
	push @record_keys, {key=>$keynice,  value=>$doc->{heTrafficTransReview}->{$record_key}{$key}[0]};
  }

  print $query->header;

  if (validate_user($query->param("username"),$query->param("password"))) 
  {
	open OUT, ">data/all_xml_data.xml" or die "Failed to open file";
#   open OUT, ">/tmp/modified.xml";

	print OUT $xs2->XMLout($doc);
	close OUT;
	open DEBUG, ">/tmp/debug";
	print DEBUG Dumper($doc, "doc");
	close DEBUG;

	$template->param(error=>"Record saved.");
  } 
  else 
  {
	# wrong password don't save it
	$template->param(error=>"Incorrect username or password. Record not saved.");
  }

  $template->param(record_keys=>\@record_keys);
  $template->param(ref=>$record_key);
  print $template->output();
  
}

sub validate_user 
{
  my ($user,$passwd) = @_;
  my $file = 'data/users.xml';
  my $xs1 = XML::Simple->new();
  my $doc = $xs1->XMLin($file);

	#print STDERR "passsword should be...".$doc->{user}->{$user}->{password}."\n";
	#print STDERR "passsword is...".$query->param(password)."\n";
	#print STDERR Dumper($doc);

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
}


sub add_record_given_reference 
{
  my ($query) = @_;
  print $query->header;
  my $template = HTML::Template->new
  (
	filename => 'newrecordtype.tpl',
	die_on_bad_params => 0,
	loop_context_vars => 1,
	path => [ 'templates' ]
  );
	  
  $record_key = $query->param('ref');

  my $file = 'data/all_xml_data.xml';
  my $xs1 = XML::Simple->new();
  my $doc = $xs1->XMLin($file);

  @record_types = ();

  foreach $key (sort keys %{$doc} ) 
  {
    %row = ( type => $key, ref => $query->param("ref"));
    push @record_types, \%row;
  }

  $template->param(ref=>$query->param("ref"));
  $template->param(record_types=>\@record_types);
  print $template->output();
  
}

sub new_full_record 
{
  my($query) = @_;
  my $template = HTML::Template->new
  (
    filename => 'fullrecordedit.tpl',
    die_on_bad_params => 0,
	loop_context_vars => 1,
    path => [ 'templates' ]
  );

  $reference_key = $query->param('ref');

  my $file = 'data/all_xml_data.xml';
  my $xs1 = XML::Simple->new();
  my $doc = $xs1->XMLin($file);

  @record_numbers = ();
  @record_keys = ();
  $keyhighest = 0;

  foreach $key (sort {$a<=>$b} keys %{$doc->{heTrafficTransReview}}) 
  {
    if ($key > $keyhighest) {$keyhighest = $key;}
  }

  $keyhighest++;
#  foreach $key (sort keys %{$doc->{heTrafficTransReview}->{1}}) {
#    $keynice = $key;
#    $keynice =~ s/_/ /g;
#    if ($key eq "reference_no") {
#      push @record_keys, {key=>$keynice,  value=>$reference_key.".00", key_orig=>$key};
#    }  {
#      push @record_keys, {key=>$keynice,  value=>"", key_orig=>$key};
#    }
#  }
#print STDERR $query-param("recordtype")."\n";

  if ($query->param("recordtype") eq "housing") 
  {
    @record_keys = 
	( 
      {key=>"Aspect of Health", value=>"", key_orig=>"aspect_of_health"},
      {key=>"Aspect of Regeneration", value=>"", key_orig=>"aspect_of_regeneration"},
      {key=>"Author", value=>"", key_orig=>"author"},
      {key=>"Mediating Factors", value=>"", key_orig=>"mediating_factors"},
      {key=>"Process used", value=>"", key_orig=>"process_used"},
      {key=>"Reference", value=>$query->param("ref"), key_orig=>"reference_no"},
      {key=>"Study design and sample", value=>"", key_orig=>"study_design_and_sample"},
      {key=>"Health outcome/effects", value=>"", key_orig=>"health_outcome_effects"},
      {key=>"Record Number (don't change)", value=>"$keyhighest", key_orig=>"key"},
      {key=>"Causal pathways discussed", value=>"", key_orig=>"causal_pathways"},
      {key=>"Key health outcomes related to unemployment", value=>"", key_orig=>"outcomes_rel_unemployment"},
      {key=>"Notes", value=>"", key_orig=>"notes"}
    );
  } 
  elsif ($query->param("recordtype") eq "traffic") 
  {
    @record_keys = 
	( 
     {key=>"Aspect of Health", value=>"", key_orig=>"aspect_of_health"},
     {key=>"Aspect of Regeneration", value=>"", key_orig=>"aspect_of_regeneration"},
     {key=>"Author", value=>"", key_orig=>"author"},
     {key=>"Mediating Factors", value=>"", key_orig=>"mediating_factors"},
     {key=>"Process used", value=>"", key_orig=>"process_used"},
     {key=>"Reference", value=>$query->param("ref"), key_orig=>"reference_no"},
     {key=>"Study design and sample", value=>"", key_orig=>"study_design_and_sample"},
     {key=>"Health outcome/effects", value=>"", key_orig=>"health_outcome_effects"},
     {key=>"Record Number (don't change)", value=>"$keyhighest", key_orig=>"key"},
     {key=>"Causal pathways discussed", value=>"", key_orig=>"causal_pathways"},
     {key=>"Key health outcomes related to unemployment", value=>"", key_orig=>"outcomes_rel_unemployment"},
     {key=>"Notes", value=>"", key_orig=>"notes"}
    );

  } 
  elsif ($query->param("recordtype") eq "Employment") 
  {
    @record_keys = 
	( 
     {key=>"Aspect of Health", value=>"", key_orig=>"aspect_of_health"},
     {key=>"Aspect of Regeneration", value=>"", key_orig=>"aspect_of_regeneration"},
     {key=>"Author", value=>"", key_orig=>"author"},
     {key=>"Mediating Factors", value=>"", key_orig=>"mediating_factors"},
     {key=>"Process used", value=>"", key_orig=>"process_used"},
     {key=>"Reference", value=>$query->param("ref"), key_orig=>"reference_no"},
     {key=>"Study design and sample", value=>"", key_orig=>"study_design_and_sample"},
     {key=>"Health outcome/effects", value=>"", key_orig=>"health_outcome_effects"},
     {key=>"Record Number (don't change)", value=>"$keyhighest", key_orig=>"key"},
     {key=>"Causal pathways discussed", value=>"", key_orig=>"causal_pathways"},
     {key=>"Key health outcomes related to unemployment", value=>"", key_orig=>"outcomes_rel_unemployment"},
     {key=>"Notes", value=>"", key_orig=>"notes"}
    );
  } 

  $template->param(record_keys=>\@record_keys);
  $template->param(ref=>$keyhighest);
  print $query->header;
  print $template->output();
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

	my $doc2 = XMLin('data/all_xml_data.xml');
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


	
	if (validate_user($query->param("username"),$query->param("password"))) 
	{
		#system("XMLmerge.bat");
		XML_append("data/all_xml_data.xml", "data/temp_file.xml");
		update_keyword_files();
		$userinfo = "The record has been added to the database";
	}
	else
	{
		$userinfo = "Unable to add record - Bad password?";
	}

	# UPDATE KEYWORD FILES

	#Start with just thealthKw.xml

	#my $doc3 = XMLin('data/thealthKw.xml');
	
	$template->param(hia_info => $userinfo);
	print $template->output();
}


  
sub XML_append
{
	my($file1, $file2) = @_;

	my @alldata = ();
	my $currentdata = ();
	my $dataitem = ();

	# Strip off top level header

    open(FILE, $file1) || die "Can't open file 1";

	#print "Opening file 1";

    while(<FILE>) 
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

    while(<FILE>) 
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

sub update_keyword_files
{
# GET KEYWORDS

	my $healthKw = get_keyword("data/temp_file.xml", "aspect_of_health");
	my $regenKw = get_keyword("data/temp_file.xml", "aspect_of_regeneration");
	my $authorKw = get_keyword("data/temp_file.xml", "author");

# CHECK IF THEY EXIST AND ADD TO LISTS IF NOT

	my @list_healthKw = split(/, /, $healthKw);

	foreach $separate_healthKw(@list_healthKw)
	{
		#print $separate_healthKw."\n";

		if(!xml_keyword_exists("data/healthKw.xml", "health_keywords", $separate_healthKw) )
		{
			add_keyword("data/healthKw.xml", "health_keywords", $separate_healthKw);
		}
	}

	my @list_regenKw = split(/, /, $regenKw);

	foreach $separate_regenKw(@list_regenKw)
	{

		if(!xml_keyword_exists("data/regenerationKw.xml", "regeneration_keywords", $separate_regenKw) )
		{
			add_keyword("data/regenerationKw.xml", "regeneration_keywords", $separate_regenKw);
		}
	}	

	if(!xml_author_exists("data/authorName.xml", "author_keyword", $authorKw) )
	{
		add_author("data/authorName.xml", "author_keyword", $authorKw);
	}
}

sub xml_keyword_exists
{
   my($file, $keyKw, $keyword) = @_;

   my $xml_file = XML::Simple->new();
   my $doc = $xml_file->XMLin($file);

   foreach $key (keys (%{$doc->{$keyKw}}))
   {
      if($doc->{$keyKw}->{$key}{keyword} eq $keyword)
      {
         #print $doc->{$keyKw}->{$key}{keyword}."\n";
		 #print $key;
         return 1;
      }
      else
      {
		  
      }
   }
   return 0;
}

sub xml_author_exists
{
   my($file, $keyKw, $keyword) = @_;

   my $xml_file = XML::Simple->new();
   my $doc = $xml_file->XMLin($file);

   foreach $key (keys (%{$doc->{$keyKw}}))
   {
      if($doc->{$keyKw}->{$key}{author} eq $keyword)
      {
         #print $doc->{$keyKw}->{$key}{author}."\n";
         #print "\n";
		 #print $key;
         return 1;
      }

	#print $doc->{$keyKw}->{$key}{author}."\n";
   }
   return 0;
}

sub get_keyword
{
	my($file, $key_keyword) = @_;
	
	my $xml_tempfile = XML::Simple -> new();
	my $doc = $xml_tempfile -> XMLin($file);

	my $sub_keyword = $doc->{heTrafficTransReview}->{$key_keyword};

	return ($sub_keyword);
}


sub add_keyword
{
	my($file, $keyKw, $keyword) = @_;

	my $xml_tempfile = XML::Simple->new();
	my $doc = $xml_tempfile->XMLin($file);

	my $highest_ref = 0;
	my $ref_no = 0;

	my @all_data = ();
	my $current_data = ();
	my $data_item = ();

	# Find highest ref

	foreach $ref_no(keys %{$doc->{$keyKw}})
	{
		if($ref_no > $highest_ref)
		{
			$highest_ref = $ref_no;
		}
	}

	# Next available empty ref

	$highest_ref++;

	#print "\n\n";
	#print $highest_ref;

	#$doc->{$keyKw}->{$highest_ref}{'keyword'} = $keyword;

	open (fHandle, $file) || warn;

	while(<fHandle>)
	{
		if(/<\/records>/)
		{
			push(@all_data, ($current_data));
		}
		else
		{
			$current_data .= $_;
		}
	}

	#print Dumper (@all_data);
	
	close(fHandle);
	
	# Open for writing
	
	open(fHandle, ">".$file) || die "can't open file";
	
	foreach $data_item (@all_data)
	{
		print fHandle $data_item;
	}

	print fHandle "<".$keyKw." key=\"".$highest_ref."\">\n";
	print fHandle "<keyword>".$keyword."</keyword>\n";
	print fHandle "</".$keyKw.">\n";
	print fHandle "</records>\n";
	
	#print fHandle "\n";
	
	close(fHandle);			

}


sub add_author
{
	my($file, $keyKw, $keyword) = @_;

	my $xml_tempfile = XML::Simple->new();
	my $doc = $xml_tempfile->XMLin($file);

	my $highest_ref = 0;
	my $ref_no = 0;

	my @all_data = ();
	my $current_data = ();
	my $data_item = ();

	# Find highest ref

	foreach $ref_no(keys %{$doc->{$keyKw}})
	{
		if($ref_no > $highest_ref)
		{
			$highest_ref = $ref_no;
		}
	}

	# Next available empty ref

	$highest_ref++;

	#print "\n\n";
	#print $highest_ref;

	#$doc->{$keyKw}->{$highest_ref}{'keyword'} = $keyword;

	open (fHandle, $file) || warn;

	while(<fHandle>)
	{
		if(/<\/records>/)
		{
			push(@all_data, ($current_data));
		}
		else
		{
			$current_data .= $_;
		}
	}

	#print Dumper (@all_data);
	
	close(fHandle);
	
	# Open for writing
	
	open(fHandle, ">".$file) || die "can't open file";
	
	foreach $data_item (@all_data)
	{
		print fHandle $data_item;
	}

	print fHandle "<".$keyKw." key=\"".$highest_ref."\">\n";
	print fHandle "<author>".$keyword."</author>\n";
	print fHandle "</".$keyKw.">\n";
	print fHandle "</records>\n";
	
	#print fHandle "\n";
	
	close(fHandle);			

}	
