from django.http import JsonResponse
from django.shortcuts import render
from voting.models import Voting
from django.core import serializers

# Create your views here.
#Aquí se redirige a las vistas
def dashboard_pv(request):
    return render(request, 'dashboard_with_pv.html',{})

def pivot_data(request):
    #Aquí está al función del model del que sacaremos los datos
    filter_fields = ('id', )
    dataset = Voting.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe = False)