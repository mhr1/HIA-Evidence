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
Please enter your username here:- <input type=text name="username" length=10>
<br>
Please enter your password here:- <input type=password name="password" length=10>
<br>
<input type=hidden name="ref" value="<TMPL_VAR ref>">
<input type=hidden name="mode" value="display_data">
<input type=submit name="Save" value="Save this record"> (requires admin password)
</form>
<TMPL_INCLUDE footer.tpl>
