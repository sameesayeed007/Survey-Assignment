from django.contrib import admin
from survey.models import Survey,Question,AnswerChoices,Submission,Answers
# Register your models here.
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(AnswerChoices)
admin.site.register(Submission)
admin.site.register(Answers)

