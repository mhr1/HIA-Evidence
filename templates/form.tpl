<TMPL_INCLUDE header.tpl>
<h2>Search Form</h2>
<p>
This database is separated into 9 different tables. Please select your search criteria from the list below. You can limit your search to any of the following criteria.
</p>
<p>
All modifications/additions to this information should be passed to Ella Rice

<a href="mailto:ellabug@odl.qmul.ac.uk">ellabug@odl.qmul.ac.uk</a>
</p>
<p>
<form name=myform method=post>
<table>
<tr>
<td>
Author's name 
</td>
<td>
<select name=author>
<option></option>
<TMPL_LOOP name=author_keywords_loop>
<option><TMPL_VAR author></option>
</TMPL_LOOP>
</select>

<tr>
<td>
Specific aspects of health
</td>
<td>
<select name=aspectofh>
<option></option>
<TMPL_LOOP name=health_keywords_loop>
<option><TMPL_VAR keyword></option>
</TMPL_LOOP>
</select>
</td>
</tr>
<tr>
<td>
Specific aspects of regeneration
</td>
<td>
<select name=aspectofr>
<option></option>
<TMPL_LOOP name=regeneration_keywords_loop>
<option><TMPL_VAR keyword></option>
</TMPL_LOOP>
</select>
</td>
</tr>
<tr>
<td>
Free text search 
</td>
<td>
<input type=text name=freetextsearch size=25 maxlength=50 value="<TMPL_VAR free_text>">
<input type=radio name=textsearchtype value="Any" checked>Match any of these terms
<input type=radio name=textsearchtype value="All">Match all of these terms
</input>
</td>
</tr>
</table>
<input type=hidden name=mode value="search">
<input type=submit name=Action value="Submit">
</form>

<TMPL_INCLUDE footer.tpl>
