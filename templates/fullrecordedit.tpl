<TMPL_INCLUDE header.tpl>
<h2>Complete Record</h2>
<p>

<TABLE>
<TR>
<TD colspan=2>
<i>Detailed Record</i>
</TD>
</TR>

<FORM name=myform method=post>
<TMPL_LOOP record_keys>
<tr>
<td <TMPL_IF NAME="__ODD__">bgcolor="#eeeeee"<TMPL_ELSE>bgcolor="#ccccff"</TMPL_IF>>
<TMPL_VAR key>
</td>
<td <TMPL_IF NAME="__ODD__">bgcolor="#eeeeee"<TMPL_ELSE>bgcolor="#ccccff"</TMPL_IF>>
<textarea cols=50 rows=5 wrap="virtual" name="<TMPL_VAR key_orig>">
<TMPL_VAR value>
</textarea>
</td>
</tr>
</TMPL_LOOP>
</TABLE>
<p>
Please enter your username here:- <input type=text name="username" length=10>
<br>
Please enter your password here:- <input type=password name="password" length=10>
<br>
and then <input type=hidden name="mode" value="submitedit">
<input type=hidden name="ref" value="<TMPL_VAR ref>">
<input type=submit name="Submit" value="Save Changes">
</p>
<TMPL_INCLUDE footer.tpl>
