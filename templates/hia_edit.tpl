<h2>HIA Edit</h2>
<p>

<TABLE>

<FORM name=myform method=post>
<TMPL_LOOP record_keys>
<tr>
<td <TMPL_IF NAME="__ODD__">bgcolor="#eeeeee"<TMPL_ELSE>bgcolor="#cccc00"</TMPL_IF>>
<TMPL_VAR key>
</td>
<td <TMPL_IF NAME="__ODD__">bgcolor="#eeeeee"<TMPL_ELSE>bgcolor="#55aacc"</TMPL_IF>>
<textarea cols=70 rows=3 wrap="virtual" name="<TMPL_VAR key_orig>">
<TMPL_VAR value>
</textarea>
</td>
</tr>
</TMPL_LOOP>
</TABLE>
Record ref:- <input type=text name="ref" length=10>
<input type=hidden name="info" value="<TMPL_VAR ref>">
<input type=submit name="Submit" value="fetch">
</p>
