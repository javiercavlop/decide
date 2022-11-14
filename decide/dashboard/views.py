
import json

from django.contrib.auth import get_user_model

# Create your views here.
from django.http import HttpResponse, Http404
from django.conf import settings
from django.views.generic import TemplateView
from voting.models import Voting
from census.models import Census
from dashboard.models import DashBoard

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voting = list(Voting.objects.values())
        total_votes=[]
        new_votes=list(DashBoard.objects.all().values())

        for v in list(voting):
            sum=0
            if v['postproc']!=None:
                for p in v['postproc']:
                    sum += int(p['votes'])

                tuple=(v['id'],sum)
                total_votes.append(tuple)

        add_votes=[n['voting'] for n in new_votes]
        set_add=set(add_votes)
        add_dict = {item: add_votes.count(item) for item in set_add}
        for key in add_dict.keys():

            tuple=(key,add_dict[key])
            total_votes.append(tuple)
        total_votes = sorted(total_votes, key=lambda x: x[0], reverse=False)
        census = list(Census.objects.values())
        print("total",total_votes)
        dic_census={}
        for c in census:
            if c['voting_id'] in dic_census.keys():
                dic_census[c['voting_id']]+=1
            else:
                dic_census[c['voting_id']]=1
        list_census=list(dic_census.items())
        list_census=sorted(list_census, key=lambda x: x[0], reverse=False)
        votings_ids=[x[0] for x in total_votes]
        list_dict_census=[]
        for it in list_census:
            dic_percen = {}
            if it[0] in votings_ids:
                dic_percen['votingid']=it[0]
                dic_percen['porc']=total_votes[votings_ids.index(it[0])][1]/it[1]
                list_dict_census.append(dic_percen)
            else:
                dic_percen['votingid'] = it[0]
                dic_percen['porc']=0
                list_dict_census.append(dic_percen)

        context['porcentages'] = json.dumps(list_dict_census)

        User = get_user_model()
        users = User.objects.values()
        us=list(users.all())
        print("users",us)
        usern_id={}
        for u in us:
            usern_id[u['id']]=u['username']

        lista=[]
        for i in us:

            lista.append(i['username'])

        context['users'] = json.dumps(lista)
        context['KEYBITS'] = settings.KEYBITS

        #número de encuestas votadas por perfiles
        votes_user={}
        for  vote in new_votes:
            if vote['voter'] in votes_user.keys():
                votes_user['voter']=vote['voter']
            else:
                votes_user[vote['voter']]=1
        form_vu=[]
        for it in votes_user.keys():
            dict={}
            dict['voter']=usern_id[it]
            dict['number']=votes_user[it]
            form_vu.append(dict)



        context['new_votes'] = json.dumps(form_vu)


        return context

