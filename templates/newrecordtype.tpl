<TMPL_INCLUDE header.tpl>
<h2>Record type</h2>
<p>
Please select which type of record you would like to create.
</p>
<TABLE>
<TR>
<TD>
<i></i>
</TD>
</TR>
 <tr>
  <td>
   <FORM method=post>
    <INPUT TYPE="HIDDEN" NAME="mode" VALUE="newrecordtype">
    <INPUT TYPE="HIDDEN" NAME="ref" VALUE="<TMPL_VAR ref>">
    <INPUT TYPE="HIDDEN" NAME="recordtype" VALUE="traffic">
    <INPUT TYPE="SUBMIT" NAME="submit" VALUE="New Traffic/Transport record">
   </FORM>
  </td>
 </tr>
 <tr>
  <td>
   <FORM method=post>
    <INPUT TYPE="HIDDEN" NAME="mode" VALUE="newrecordtype">
    <INPUT TYPE="HIDDEN" NAME="ref" VALUE="<TMPL_VAR ref>">
    <INPUT TYPE="HIDDEN" NAME="recordtype" VALUE="housing">
    <INPUT TYPE="SUBMIT" NAME="submit" VALUE="New Housing record">
   </FORM>
  </td>
 </tr>
 <tr>
  <td>
   <FORM method=post>
    <INPUT TYPE="HIDDEN" NAME="mode" VALUE="newrecordtype">
    <INPUT TYPE="HIDDEN" NAME="ref" VALUE="<TMPL_VAR ref>">
    <INPUT TYPE="HIDDEN" NAME="recordtype" VALUE="Employment">
    <INPUT TYPE="SUBMIT" NAME="submit" VALUE="New Employment record">
   </FORM>
  </td>
 </tr>
</TABLE>

<TMPL_INCLUDE footer.tpl>
