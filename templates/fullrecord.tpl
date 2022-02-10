<TMPL_INCLUDE header.tpl>
<h2>Complete Record</h2>
<p>

<TABLE>
<TR>
<TD colspan=2>
<i>Detailed Record</i>
</TD>
</TR>
<p>
<TMPL_VAR error>
</p>
<TMPL_LOOP record_keys>
<tr>
<td <TMPL_IF NAME="__ODD__">bgcolor="#eeeeee"<TMPL_ELSE>bgcolor="#ccccff"</TMPL_IF>>
<TMPL_VAR key>
</td>
<td <TMPL_IF NAME="__ODD__">bgcolor="#eeeeee"<TMPL_ELSE>bgcolor="#ccccff"</TMPL_IF>>
<TMPL_VAR value>
</td>
</tr>
</TMPL_LOOP>
</TABLE>


<FORM method=post>
<input type=hidden name="ref" value="<TMPL_VAR ref>">
<input type=hidden name="mode" value="fullrecordedit">
<input type=submit name="Edit" value="Edit this record"> (requires admin password)
</form>
<TMPL_INCLUDE footer.tpl>
