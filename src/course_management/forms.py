from django import forms



class EditCourseForm(forms.Form):
    active = forms.BooleanField(initial=False)
    description = forms.CharField(widget=forms.Textarea)
    max_participants = forms.DecimalField(min_value=1, label="Maximum number of allowed participants")
