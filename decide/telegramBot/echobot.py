import json
import logging
import datetime
from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from django.contrib.auth import get_user_model


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "decide.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from dashboard.models import DashBoard, Percentages, Surveys
from census.models import Census
from voting.models import Voting

def echo(update: Update, _: CallbackContext) -> None:
    query = update.message.text
    User = get_user_model()
    users = User.objects.values()
    us=list(users.all())


    new_votes=list(Surveys.objects.all().values())
    votes_user={}
    for  vote in new_votes:
        if vote['voter'] in votes_user.keys():
            votes_user['voter']=vote['voter']
        else:
            votes_user[vote['voter']]=1
    
    text=""
    reply_keyboard = [["start"],["help"],["profiles"],["voting"],["votings"],["percentages"]]
    #queries
    if query in ['start','Start'] :
        user = update.effective_user
        text = fr"Hola {user.first_name}! Escribe help para saber que comandos puedes usar"

    elif query in ['help','Help'] :
        text = "LOS COMANDOS QUE SE PUEDEN PROBAR SON:  \n start  \n profiles  "
        text = text + f"\n voting \n votings \n voting-<voting_id>\n percentages"

    elif query in ['profiles','Profiles'] :
        text = 'Perfiles:\n'
        for i in us:
            username = i['username']
            text = text + f"{username}\n"

    elif query in ['percentages','Percentages'] :
        percentages=list(Percentages.objects.all().values())
        text = 'PORCENTAJES DE VOTACIONES SEGÚN CENSO\n';
        for p in percentages:
            voting = p['voting']
            perc = p['percen']*100
            text = text + f'Encuesta: {voting}  // Porcentage: {perc}%\n'
    
    elif query in ['voting','Voting'] :
        for it in new_votes:
            voter = it['voter']
            number = it['number']
            text = f"NÚMEROS DE ENCUESTAS VOTADAS EN TIEMPO REAL \nVotante: {voter}  //  Encuestas: {number}\n"

    
    elif query in ['votings', 'Votings']:
        i = 1
        for v in list(Voting.objects.order_by('id')):
            text = text + f'Id: {i}  //  Nombre: {v}\n'
            i = i+1

    elif ('voting-' in query) or ('Voting-' in query ):
        try:
            split = query.index('-')+1
            voting_id = query[split:]
            data = Voting.objects.filter(id=voting_id)
            numberOfPeople = len(Census.objects.filter(voting_id = voting_id))
            duration = ""
            if not data[0].start_date:
                duration = "Aún no ha comenzado"
            elif not data[0].end_date:
                duration = "Aún no ha terminado"
            else:
                time = data[0].end_date-data[0].start_date
                duration = str(time - datetime.timedelta(microseconds=time.microseconds))

            data[0].do_postproc()
            postpro = data[0].postproc
            numberOfVotes = 0
            options = []
            votes = []
            for vote in postpro:
                options.append(vote['option'])
                votes.append(vote['votes'])
                numberOfVotes = numberOfVotes+ vote['votes']
            labels2 = ["Votaron","No votaron"]
            values2 = [numberOfVotes, numberOfPeople-numberOfVotes]
            text = f'Nombre de la votación: {data[0].name}\n'
            text = text + f'Descripción de la votación: \n {data[0].desc}\n'
            text = text + f'Número de personas en el censo: {numberOfPeople}\n'
            text = text + f'Número de votos: {numberOfVotes}\n'
            text = text + f'Duración de la votación: {duration}'
        except:
            text = f'La aplicación web debe estar arrancada para poder proporcionar datos sobre Voting-{voting_id}'

    else: 
        text = f"Comando '{query}' erroneo, prueba con:  \n start \n help \n profiles "
        text = text + f"\n voting \n votings \n voting-<voting_id>"

    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard,));    


def main() -> None:
    """Start the bot."""

    updater = Updater("5699779008:AAGmJq26fV43EuwY4rFRNtx-1h1oo26TumE")


    dispatcher = updater.dispatcher

    # echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
   
   # Start the Bot
    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()