from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)

from rest_framework.permissions import IsAdminUser,IsAuthenticated
from base.perms import UserIsStaff
from .models import Census,CensusGroup
from .forms import CensusReuseForm
from .serializers import CensusGroupSerializer,CensusSerializer
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes 


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
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

@api_view(['GET','POST'])
def censusReuse(request):
    if request.method == 'POST':
            form = CensusReuseForm(request.POST)
            print(form)
            if form.is_valid():
                cd = form.cleaned_data
                voting_id = cd['voting_id']
                new_voting = cd['new_voting']
                censos = Census.objects.all().values()
                for c in censos:
                    if(c['voting_id'] == voting_id):
                            try:
                                census = Census(voting_id=new_voting, voter_id=c['voter_id'], group_id=c['group_id'])
                                census.save()
                            except:
                                pass
                return HttpResponseRedirect('/census')
            else:
                return Response('Error try to create census', status=ST_400)
    else:
        form = CensusReuseForm()
    return render(request,'census/census_reuse_form.html',{'form':form})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def censusList(request):
    censos = Census.objects.all().values()
    res = []
    options = []
    for c in censos:
        try:
            votante = User.objects.get(pk=c['voter_id'])
        except:
            votante = "El votante todavía no ha sido añadido"
        if(votante not in options):
            options.append(votante)
        censo = c['voting_id']
        try:
            grupo = CensusGroup.objects.get(id=c['group_id'])
            if(grupo not in options):
                options.append(grupo.name)
        except:
            ###    <!-- TRADUCCIÓN -->
            grupo = "No tiene grupo asignado"
            if(grupo not in options):
                options.append(grupo)
        res.append({'voting_id':censo,'voter':votante,'group':grupo})
    return render(request,'census/census.html',{'censos':res, 'options':options})


class CensusGroupDetail(generics.RetrieveDestroyAPIView):
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