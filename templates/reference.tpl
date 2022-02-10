<TMPL_INCLUDE header.tpl>
<h2>Record of reference</h2>
<p>

<TABLE>
<TR>
<TD>
<i>Detailed Reference/s</i>
</TD>
</TR>

</table>

<TMPL_LOOP ref_array>
  <table>
  <tr>
  <td>
  <TMPL_VAR details>

  </td>
  </tr>
  </TABLE>
  <FORM method=POST>

  <INPUT TYPE="HIDDEN" NAME="mode" VALUE="addrecord">
  <INPUT TYPE="HIDDEN" NAME="ref" VALUE=<TMPL_VAR ref>>
  <INPUT TYPE="SUBMIT" NAME="New record for this reference" VALUE="Add a new record for this reference">
  </FORM>
</TMPL_LOOP>
<i>(Adding records requires a username and password)</i>
<p>
<TMPL_INCLUDE footer.tpl>
