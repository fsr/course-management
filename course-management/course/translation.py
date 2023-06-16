from modeltranslation.translator import translator, TranslationOptions
from .models import subject

class SubjectTranslationOptions(TranslationOptions):
    fields = ('description',)

translator.register(subject.Subject, SubjectTranslationOptions)
