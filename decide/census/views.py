from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)
from rest_framework.permissions import IsAdminUser
from base.perms import UserIsStaff
from .models import Census,CensusGroup
from .serializers import CensusGroupSerializer,CensusSerializer

from django.conf import settings
import pandas as pd
from rest_framework.decorators import api_view
from django.db import transaction
import math
from django.http import HttpResponse
import csv
from django.contrib import messages


class CensusCreate(generics.ListCreateAPIView):
    serializer_class = CensusSerializer
    permission_classes = (IsAdminUser,)

    def create(self, request, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        group_name = request.data.get('group')
        if group_name:
            group_name = group_name.get('name')
        try:
            group = None
            if group_name and len(group_name) > 0:
                group = CensusGroup.objects.get(name=group_name)
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter, group=group)
                census.save()
        except CensusGroup.DoesNotExist:
            return Response('The input Census Group does not exist', status=ST_400)
        except IntegrityError:
            return Response('Error trying to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})



@transaction.atomic
def import_excel(request):
    cont=2
    try: 
        if request.method == 'POST':
            census_from_excel=[]
        
            myfile = request.FILES['myfile'] 
            df=pd.read_excel(myfile)

            for d in df.values:
                try:
                    group = None
                    if not math.isnan(d[2]):
                        group = CensusGroup.objects.get(id=d[2])

                    census = Census(voting_id=d[0], voter_id=d[1],group=group)
                    census_from_excel.append(census)
                    cont+=1
                except CensusGroup.DoesNotExist:
                    messages.error(request,'The input Census Group does not exist, in row {}'.format(cont-1))
                    return render(request,"census/import.html")

            cont=0
            for c in census_from_excel:
                try:
                    cont+=1
                    c.save()
                except IntegrityError:
                    messages.error(request, 'Error trying to import excel, in row {}. A census cannot be repeated.'.format(cont))
                    return render(request,"census/import.html")

            messages.success(request, 'Census Created')
            return render(request,"census/import.html")

    except:
        messages.error(request, 'Error in excel data. There are wrong data in row {}'.format(cont+1)) 
        return render(request,"census/import.html")

    return render(request,"census/import.html")

@transaction.atomic
def import_json(request):
    cont=2
    try: 
        if request.method == 'POST':
            census_from_json=[]
        
            myfile = request.FILES['myfile'] 
            df=pd.read_json(myfile)

            for d in df.values:
                try:
                    group= None
                    if d[2]:
                        if d[2] == "":
                            group = None
                        else: 
                            group = CensusGroup.objects.get(id=d[2])

                    census = Census(voting_id=d[0], voter_id=d[1],group=group)
                    census_from_json.append(census)
                except CensusGroup.DoesNotExist:
                    messages.error(request,'The input Census Group does not exist')
                    return render(request,"json.html")
            for c in census_from_json:
                try:
                    c.save()
                except IntegrityError:
                    messages.error(request, 'Error trying to import JSON. A census cannot be repeated.')
                    return render(request,"json.html")
            messages.success(request, 'Census created')
    except:
        messages.error(request, 'Error in JSON data.') 
        return render(request,"json.html")
    return render(request,"json.html")

@transaction.atomic
def import_csv(request):
    cont=2
    try: 
        if request.method == 'POST':
            census_from_csv=[]
        
            myfile = request.FILES['myfile'] 
            df=pd.read_csv(myfile)

            for d in df.values:
                try:
                    group = None
                    if not math.isnan(d[2]):
                        group = CensusGroup.objects.get(id=d[2])

                    census = Census(voting_id=d[0], voter_id=d[1],group=group)
                    census_from_csv.append(census)
                    cont+=1
                except CensusGroup.DoesNotExist:
                    messages.error(request, 'The input Census Group does not exist, in row {}'.format(cont-1))
                    return render(request, "csv.html")
            cont=0
            for c in census_from_csv:
                try:
                    cont+=1
                    c.save()
                except IntegrityError:
                    messages.error(request, 'Error trying to import CSV, in row {}. A census cannot be repeated.'.format(cont))
                    return render(request,"csv.html")
            messages.success(request, 'Census Created')
            return render(request,"csv.html")
    except:
        messages.error(request, 'Error in CSV data. There are wrong data in row {}'.format(cont+1)) 
        return render(request,"csv.html")
    return render(request,"csv.html")

<<<<<<< HEAD
=======
@transaction.atomic
def import_excel(request):
    cont=2
    try: 
        if request.method == 'POST':
            census_from_excel=[]
        
            myfile = request.FILES['myfile'] 
            df=pd.read_excel(myfile)

            for d in df.values:
                try:
                    group = None
                    if not math.isnan(d[2]):
                        group = CensusGroup.objects.get(id=d[2])

                    census = Census(voting_id=d[0], voter_id=d[1],group=group)
                    census_from_excel.append(census)
                    cont+=1
                except CensusGroup.DoesNotExist:
                    messages.error(request,'The input Census Group does not exist, in row {}'.format(cont-1))
                    return render(request,"census/import.html")

            cont=0
            for c in census_from_excel:
                try:
                    cont+=1
                    c.save()
                except IntegrityError:
                    messages.error(request, 'Error trying to import excel, in row {}. A census cannot be repeated.'.format(cont))
                    return render(request,"census/import.html")
                    
            messages.success(request, 'Census Created')
            return render(request,"census/import.html")

    except:
        messages.error(request, 'Error in excel data. There are wrong data in row {}'.format(cont+1)) 
        return render(request,"census/import.html")

    return render(request,"census/import.html")


>>>>>>> ffdaec2f5671f6a9f755a0922ed07bf1461ccc97

def export_excel(request):
    try:           
        if request.method == 'POST':
            census=Census.objects.all()
            response=HttpResponse()
            response['Content-Disposition']= 'attachment; filename=census.xlsx'
            writer=csv.writer(response)
            writer.writerow(['voting_id','voter_id','group'])
            census_fields=census.values_list('voting_id','voter_id','group')
            for c in census_fields:
                writer.writerow(c)
            messages.success(request,"Exportado correctamente")
            return response
    except:
            messages.error(request,'Error in exporting data. There are null data in rows')
            return render(request, "census/export.html")
    return render(request,"census/export.html")





class CensusDetail(generics.RetrieveDestroyAPIView):
    serializer_class = CensusSerializer

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        census = Census.objects.filter(voting_id=voting_id, voter_id__in=voters)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')

class CensusGroupCreate(generics.ListCreateAPIView):
    serializer_class = CensusGroupSerializer
    permission_classes = (IsAdminUser,)
    queryset = CensusGroup.objects.all()

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        try:
            census_group = CensusGroup(name=name)
            census_group.save()
        except IntegrityError:
            return Response('Error trying to create census', status=ST_409)
        return Response('Census group created', status=ST_201)
  
class CensusGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CensusGroupSerializer
    queryset = CensusGroup.objects.all()

    def destroy(self, request, pk, *args, **kwargs):
        census_group = CensusGroup.objects.filter(id=pk)
        census_group.delete()
        return Response('Census Group deleted from census', status=ST_204)

    def retrieve(self, request, pk, *args, **kwargs):
        try:
            CensusGroup.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response('Non-existent group', status=ST_401)
        return Response('Valid group')