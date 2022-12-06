from django import forms
from .models import Census,CensusGroup

class CensusReuseForm(forms.Form):
    voting_id = forms.IntegerField(label="voting_id")
    new_voting = forms.IntegerField(label="new_voting")

class CensusGroupingForm(forms.Form):
    group = forms.CharField(label="group")
    choices = forms.ModelMultipleChoiceField(
    queryset= Census.objects.all(),
    widget  = forms.CheckboxSelectMultiple,
    )