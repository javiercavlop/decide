import json
import os
from rest_framework import generics
from django.contrib.auth import get_user_model

from django.http import HttpResponse, Http404, FileResponse
import datetime
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.generic import TemplateView
from dashboard.models import DashBoard, Percentages,Surveys
from voting.models import Voting
from census.models import Census
from rest_framework.decorators import api_view
import weasyprint
from wsgiref.util import FileWrapper
from voting.models import Voting
from census.models import Census

from voting import models as voting_models
from census import models as census_models
from django.utils.translation import ugettext_lazy as _

def vista(request,voting_id):
    data = get_object_or_404(Voting,id=voting_id)

    data = Voting.objects.filter(id=voting_id)
    numberOfPeople = len(Census.objects.filter(voting_id = voting_id))
    duracion = ""
    if not data[0].start_date:
        duracion = _("Aún no ha comenzado")
    elif not data[0].end_date:
        duracion = _("Aún no ha terminado")
    else:
        time = data[0].end_date-data[0].start_date
        duracion = str(time - datetime.timedelta(microseconds=time.microseconds))

    data[0].do_postproc()

    if data[0].desc != "" and data[0].desc is not None:
        description = data[0].desc
    elif data[0].question.desc != "" and data[0].question.desc is not None:
        description = data[0].question.desc
    else:
        description = _("No hay una descripción asociada a esta votación ni a esta pregunta")


    postpro = data[0].postproc
    numberOfVotesAux = 0
    numberOfVotes = 0
    options = []
    values = []
    questionType = data[0].question.questionType

    if(questionType=='borda'):
        for vote in postpro:
            options.append(vote['option'])
            values.append(vote['postproc'])
            numberOfVotesAux=numberOfVotesAux + vote['votes']
        numberOfVotes = numberOfVotesAux/len(options)

    elif(questionType == 'normal'):
        for vote in postpro:
            options.append(vote['option'])
            values.append(vote['votes'])
            numberOfVotes = numberOfVotes+ vote['votes']

    elif(questionType == 'dhondt'):
        for vote in postpro:
            options.append(vote['option'])
            values.append(vote['postproc'])
            numberOfVotes = numberOfVotes + vote['votes']
    
    
    labels2 = ["Votaron","No votaron"]
    values2 = [int(numberOfVotes), int(numberOfPeople-numberOfVotes)]

    aux = {}
    aux['Hombre'] = data[0].num_votes_M
    aux['Mujer'] = data[0].num_votes_W
    aux['Otros'] = numberOfVotes - (aux['Hombre'] + aux['Mujer'])
    labels3 = aux.keys()
    values3 = []
    for label in labels3:
        values3.append(aux[label])
    
    parity = False
    mayor = ''
    menor = ''
    numDif = abs(aux['Hombre'] - aux['Mujer'])
    if(aux['Hombre'] == aux['Mujer']):
        parity = True
    elif(aux['Hombre'] > aux['Mujer']):
        mayor = 'hombres'
        menor = 'mujeres'
    else:
        mayor = 'mujeres'
        menor = 'hombres'


    context = {
        "voting" : data[0],
        "description" : description,
        "parity" : parity,
        "mayor" : mayor,
        "menor" : menor,
        "numDif" : numDif,
        "people" : numberOfPeople,
        "time" : duracion,
        "numberOfVotes" : int(numberOfVotes),
        "questionType" :questionType,
        "labels" : options,
        "values" : values,
        "labels2" : labels2,
        "values2" : values2,
        "labels3" : labels3,
        "values3" : values3,
    }

    return render(request,"dashboard_with_pv.html",context)


class DashboardView(TemplateView):
    def as_view(request):
        template_name = 'dashboard/dashboard.html'

        percentages=list(Percentages.objects.all().values())
        pools=[p['voting'] for p in percentages]

        User = get_user_model()
        users = User.objects.values()
        us = list(users.all())
        usern_id = {}
        for u in us:
            usern_id[u['id']] = u['username']

        lista = []
        for i in us:
            lista.append(i['username'])

        surveys=list(Surveys.objects.all().values())
        votings=Voting.objects.all().values()


        for v in votings:
            dict={}
            if v['id'] not in pools:
                dict['id'] = '-'
                dict['voting']=v['id']
                dict['percen']=  0.0
                percentages.append(dict)
                

        context = {
            "percentages": percentages,
            "users": lista,
            "new_votes": surveys,

        }

        return render(request,template_name,context)

class DashBoardFile(generics.ListCreateAPIView):
    @api_view(['GET',])
    def write_doc(request):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        with open(dir_path+'/files/record','w') as file:


            file.write("<!DOCTYPE html>\n")
            file.write("<html>\n")
            file.write(("<head>\n"))
            file.write("<style>\n")
            file.write("table{\n")
            file.write("    font-family: arial, sans-serif;\n")
            file.write("    border-collapse: collapse;\n")
            file.write("    width: 100 %;\n")
            file.write("}\n")
            file.write("td, th{\n")
            file.write("    border: 1px solid  #dddddd;\n")
            file.write("    text-align: left;\n")
            file.write("    padding: 8px;\n")
            file.write("}\n")

            file.write("tr:nth-child(even){\n")
            file.write("    background-color:  #dddddd;\n")
            file.write("}\n")

            file.write("</style>\n")
            file.write(("</head>\n"))
            file.write("<body>\n")
            file.write("<h1>Informe detallado de las estadísticas recogidas</h1>\n")
            file.write(("<h2>Usuarios de la aplicación</h2>\n"))
            file.write('<table>\n')
            file.write('    <tr>\n')
            file.write('    <th>Usuario</th>\n')
            file.write(('   </tr>\n'))
            file.write('    <tr>\n')

            User = get_user_model()
            users = User.objects.values()
            us = list(users.all())
            for i in us:
                file.write('    <tr>\n')

                file.write('    <td>'+i['username']+'</td>\n')
                file.write('    </tr>\n')

            file.write('</table>\n')

            file.write(("<h2>Porcentaje del censo</h2>\n"))

            file.write("<p>Se tomaron estadísticas para el porcentaje de personas que habían votado del total del censo disponible, no sólo se cuenta con con"
                       "los datos recogidos de encuestas ya cerradas si no tambíen con aquellas que siguen abiertas. Es por esto que el grado de sensibilidad de estos datos es alto y "
                       "no deberán ser tranferidos a nadie.\n<p>")
            file.write(
                "<p> En la tabla adjuntada a continuación se visualizan en la primera columna los identificadores de las votaciones y en otra el porcentaje "
                "total del censo que ha votado.\n<p>")
            file.write('<table>\n')
            file.write('    <tr>\n')
            file.write('    <th>Id de Votación</th>\n')
            file.write('    <th>Porcentaje del censo</th>\n')
            file.write(('   </tr>\n'))
            file.write('    <tr>\n')
            percen=list(Percentages.objects.all().values())
            for p in percen:
                file.write('    <tr>\n')
                file.write('    <td>' + str(p['voting']) + '</td>\n')
                file.write('    <td>' + str(p['percen']*100) + '%</td>\n')

                file.write('    </tr>\n')
            file.write('</table>\n')


            file.write(("<h2>Encuestas votadas</h2>\n"))
            file.write("<p>También se han recogido datos sobre las encuestas contestadas por usuario. Cabe recalcar que este datos se toma a partir de la implementación"
                       " de este módulo en el sistema, las encuestas votadas previas a la misma estaŕan reflejadas en las estadísticas.\n<p>")

            file.write('<table>\n')
            file.write('    <tr>\n')
            file.write('    <th>Votante</th>\n')
            file.write('    <th>Encuestas</th>\n')
            file.write(('   </tr>\n'))
            file.write('    <tr>\n')


            surveys=list(Surveys.objects.all().values())
            for s in surveys:
                file.write('    <tr>\n')
                file.write('    <td>' + str(s['voter']) + '</td>\n')
                file.write('    <td>' + str(s['number'] ) + '</td>\n')

                file.write('    </tr>\n')
            file.write('</table>\n')


            file.write("</body>\n")

            file.write("</html>\n")
            file.close()


            with open(dir_path + '/files/record', 'r') as file:
                # Define text file name
                filename = 'record.pdf'
                # Define the full file path
                dir_path = os.path.dirname(os.path.realpath(__file__))


                pdf = weasyprint.HTML(dir_path + '/files/record').write_pdf()
                open(dir_path+'/files/record.pdf', 'wb').write(pdf)
                filepath = dir_path + '/files/record.pdf'
                content = FileWrapper(open(dir_path+'/files/record.pdf','rb'))
                response = FileResponse(content, content_type='application/pdf')
                filename = 'record'

                response['Content-Length'] = os.path.getsize(dir_path+'/files/record.pdf')
                response['Content-Disposition'] = "attachment; filename=%s" % 'record.pdf'

            return response

def main_page(request):
    is_anonymous = request.user.is_anonymous
    is_staff = request.user.is_staff
    allowed_votings = census_models.Census.objects.filter(voter_id=request.user.pk).values('voting_id')

    voting_votings = voting_models.Voting.objects.filter(end_date__isnull=True,start_date__isnull=False,pk__in=allowed_votings)
    visualize_votings = voting_models.Voting.objects.filter(end_date__isnull=False,tally__isnull=False,pk__in=allowed_votings)

    if is_anonymous:
        return render(request,'register.html')
    else:
        return render(request,'dashboard/mainpage_dashboard.html',{
                                                'voting_votings':voting_votings,
                                                'visualize_votings':visualize_votings,
                                                'is_anonymous':is_anonymous,
                                                'is_staff':is_staff
                                                })
