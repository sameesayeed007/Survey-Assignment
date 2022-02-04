from django.contrib import admin
from survey.models import Survey,Question,AnswerChoices

# Register your models here.
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(AnswerChoices)

