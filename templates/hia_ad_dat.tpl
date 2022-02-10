<TMPL_INCLUDE header.tpl>
<h2>HIA data add</h2>
<p>

<TABLE>

<FORM name="myform" method="post">
Aspect of health<br/>
<textarea name="aspect_of_health" rows="3" cols="80">
</textarea>
<br/>
Aspect of regeneration<br/>
<textarea name="aspect_of_regeneration" rows="3" cols="80">
</textarea>
<br/>
Author<br/>
<textarea name="author" rows="3" cols="80">
</textarea>
<br/>
Reference<br/>
<textarea name="reference_no" rows="1" cols="80">
</textarea>
<br/>
Study details<br/>
<textarea name="study_details" rows="3" cols="80">
</textarea>
<br/>
Process<br/>
<textarea name="process" rows="3" cols="80">
</textarea>
<br/>
Health outcome/effects<br/>
<textarea name="health_outcome_effects" rows="3" cols="80">
</textarea>
<br/>
Mediating factors<br/>
<textarea name="mediating_factors" rows="3" cols="80">
</textarea>
<br/>
Notes<br/>
<textarea name="notes" rows="3" cols="80">
</textarea>
<br/>
<input type=hidden name="mode" value="completed_form">
<input type="submit" value="Send"/>
</FORM>

</TABLE>
</p>

<TMPL_INCLUDE footer.tpl>
