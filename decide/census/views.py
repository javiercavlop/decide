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


 


class CensusImport(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)
    
    @transaction.atomic
    @api_view(['GET','POST'])
    def import_csv(request):
        try: 
            if request.method == 'POST':
                census_from_csv=[]
            
                myfile = request.FILES['myfile'] 
                df=pd.read_csv(myfile)
                cont=2
                for d in df.values:
                    try:
                        group = None
                        if not math.isnan(d[2]):
                            group = CensusGroup.objects.get(id=d[2])

                        census = Census(voting_id=d[0], voter_id=d[1],group=group)
                        census_from_csv.append(census)
                        cont+=1
                    except CensusGroup.DoesNotExist:
                        return Response('The input Census Group does not exist, in row {}'.format(cont-1), status=ST_400)
                    except IntegrityError:
                        return Response('Error trying to import CSV, in row {}. All previous census has been dissmised'.format(cont), status=ST_409)
                for c in census_from_csv:
                    c.save()
                return Response('Census created', status=ST_201)
        except:
            return Response('Error in CSV data.', status=ST_409)
        return render(request,"csv.html")

    @transaction.atomic
    @api_view(['GET','POST'])
    def import_json(request):
        try: 
            if request.method == 'POST':
                census_from_json=[]
            
                myfile = request.FILES['myfile'] 
                df=pd.read_json(myfile)
                cont=2
                for d in df.values:
                    try:
                        group = None
                        if not math.isnan(d[2]):
                            group = CensusGroup.objects.get(id=d[2])

                        census = Census(voting_id=d[0], voter_id=d[1],group=group)
                        census_from_json.append(census)
                        cont+=1
                    except CensusGroup.DoesNotExist:
                        return Response('The input Census Group does not exist, in row {}'.format(cont-1), status=ST_400)
                    except IntegrityError:
                        return Response('Error trying to import JSON, in row {}. All previous census has been dissmised'.format(cont), status=ST_409)
                for c in census_from_json:
                    c.save()
                return Response('Census created', status=ST_201)
        except:
            return Response('Error in JSON data. There are null data in rows', status=ST_409)
        return render(request,"json.html")
    
    @transaction.atomic
    @api_view(['GET','POST'])
    def import_excel(request):
        try: 
            if request.method == 'POST':
                census_from_excel=[]
            
                myfile = request.FILES['myfile'] 
                df=pd.read_excel(myfile)
                cont=2
                for d in df.values:
                    try:
                        group = None
                        if not math.isnan(d[2]):
                            group = CensusGroup.objects.get(id=d[2])

                        census = Census(voting_id=d[0], voter_id=d[1],group=group)
                        census_from_excel.append(census)
                        cont+=1
                    except CensusGroup.DoesNotExist:
                        return Response('The input Census Group does not exist, in row {}'.format(cont-1), status=ST_400)
                    except IntegrityError:
                        return Response('Error trying to import excel, in row {}. All previous census has been dissmised'.format(cont), status=ST_409)
                for c in census_from_excel:
                    c.save()
                return Response('Census created', status=ST_201)
        except:
            return Response('Error in excel data. There are null data in rows', status=ST_409)
        return render(request,"excel.html")



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