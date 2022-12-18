from django import forms
from .models import Census,CensusGroup
from django.contrib.auth.models import User
from voting.models import Voting

class CensusReuseForm(forms.Form):
    voting_id = forms.IntegerField(label="voting_id")
    new_voting = forms.IntegerField(label="new_voting")

class CensusGroupingForm(forms.Form):
    group = forms.CharField(label="group", required = False)
    choices = forms.ModelMultipleChoiceField(
    queryset= Census.objects.all(),
    widget  = forms.CheckboxSelectMultiple,
    )

class CensusForm(forms.Form):
    voting_id=forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}),
        choices=list(),
        label="Elige votación")
    voter_name=forms.ChoiceField(
        widget=forms.Select(attrs={'class': "form-control"}),
        choices=list(),
        label="Elige votante")
    group_name=forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"}),
        label='Escribe el nombre del grupo',
        required=False)

    def __init__(self, *args, **kwargs):
        super(CensusForm,self).__init__(*args,**kwargs)
        self.fields['voting_id'].choices = [(v.pk, "{} - {}".format(v.pk,v.name)) for v in Voting.objects.all()]
        self.fields['voter_name'].choices = [(u.pk, u.username) for u in User.objects.all()]
