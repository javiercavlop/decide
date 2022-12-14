from modeltranslation.translator import translator, TranslationOptions
from .models import Voting

class VotingTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Voting, VotingTranslationOptions)