from django import forms

class GroupADD(forms.Form):
	name = forms.CharField(max_length=80)

class GroupDelete(forms.Form):
	name = forms.CharField(max_length=80)
