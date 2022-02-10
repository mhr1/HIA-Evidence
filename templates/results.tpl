<TMPL_INCLUDE header.tpl>
<h2>Results</h2>
Your search returned the following <strong><TMPL_VAR number_returned></strong> record/s.
Please click on a record to its contents.
<p>

<TABLE border=0>
<TR>
<TD>
<i>Report Authors</i>&nbsp;
</TD>
<TD>
<i>Aspect of Health</i>&nbsp;
</TD>
<TD>
<i>Aspect of Regeneration</i>&nbsp;

</TD>
</TR>

<TMPL_LOOP name=result_set>
<TR>
<TD <TMPL_IF NAME="__ODD__">bgcolor="#eeeeee"<TMPL_ELSE>bgcolor="#ccccff"</TMPL_IF>>
<a href="ella_search.cgi?mode=showref&ref=<TMPL_VAR reference_no>">
<TMPL_VAR author>
</a>
</TD>
<TD <TMPL_IF NAME="__ODD__">bgcolor="#eeeeee"<TMPL_ELSE>bgcolor="#ccccff"</TMPL_IF>>
<TMPL_VAR aspect_of_health>
</TD>
<TD <TMPL_IF NAME="__ODD__">bgcolor="#eeeeee"<TMPL_ELSE>bgcolor="#ccccff"</TMPL_IF>>
<TMPL_VAR aspect_of_regeneration>

</TD>
<TD <TMPL_IF NAME="__ODD__">bgcolor="#eeeeee"<TMPL_ELSE>bgcolor="#ccccff"</TMPL_IF>>
<a href="ella_search.cgi?mode=fullrecord&ref=<TMPL_VAR ref>">
Show Full Record
</a>

</TD>
</TR>
</TMPL_LOOP>
</TABLE>

<p>
</p>

<TMPL_INCLUDE footer.tpl>
