<TMPL_INCLUDE header.tpl>
<h2>HIA data add</h2>
<p>

<TABLE>

<FORM name=myform method=post>
Aspect of health<br/>
<textarea name="<TMPL_VAR aspect_of_health>" rows="3" cols="80">
<TMPL_VAR NAME=aspect_of_health>
</textarea>
<br/>
<input type=hidden name="mode" value="completed_form">
<input type="submit" value="Send"/><input type="Reset"/>
</FORM>

</TABLE>
</p>

<TMPL_INCLUDE footer.tpl>
