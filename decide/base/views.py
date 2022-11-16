from django.shortcuts import render
from voting import models as voting_models
from census import models as census_models

def main_page(request):
    is_anonymous = request.user.is_anonymous
    allowed_votings = census_models.Census.objects.filter(voter_id=request.user.pk).values('voting_id')
    votings = voting_models.Voting.objects.filter(end_date__isnull=True,pk__in=allowed_votings)
    return render(request,'mainpage.html',{'votings':votings,'is_anonymous':is_anonymous})