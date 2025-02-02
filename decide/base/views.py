from django.shortcuts import render
from rest_framework.authtoken.models import Token
from voting import models as voting_models
from census import models as census_models
from authentication.views import SignUpView

from postproc.models import UserProfile
from rest_framework.authtoken.models import Token

def main_page(request):
    is_anonymous = request.user.is_anonymous
    allowed_votings = census_models.Census.objects.filter(voter_id=request.user.pk).values('voting_id')

    voting_votings = voting_models.Voting.objects.filter(end_date__isnull=True,start_date__isnull=False,pk__in=allowed_votings)
    visualize_votings = voting_models.Voting.objects.filter(end_date__isnull=False,tally__isnull=False,pk__in=allowed_votings)

    if is_anonymous:
        return SignUpView.register(request)
    else:

        UserProfile.objects.get_or_create(user=request.user)
        Token.objects.get_or_create(user=request.user)
        return render(request,'mainpage.html',{
                                                'voting_votings':voting_votings,
                                                'visualize_votings':visualize_votings,
                                                })