from django import forms

class CensusReuseForm(forms.Form):
    voting_id = forms.IntegerField(label="voting_id")
    new_voting = forms.IntegerField(label="new_voting")

class CensusGroupingForm(forms.Form):
    voting_id = forms.IntegerField(label="voting_id")
    voter_id = forms.IntegerField(label="voter_id")
    group = forms.CharField(label="group")