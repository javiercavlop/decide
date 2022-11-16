from django.shortcuts import render
from voting import models

def main_page(request):
    votings = models.Voting.objects.filter(end_date__isnull=True)
    return render(request,'mainpage.html',{'votings':votings})