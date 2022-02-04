from django.db import models

# Create your models here.

class Survey(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    created_by = models.IntegerField(blank=False, default=-1)
    is_active = models.BooleanField( default=True)
    date_created = models.DateTimeField( auto_now_add=True)


class Question(models.Model):
    answer_types =(
    ("Text Field", "Text Field"),
    ("Number Field", "Number Field"),
    ("Dropdown", "Dropdown"),
    ("Check Box", "Check Box"),
    ("Radio Button", "Radio Button"),
    )
    question = models.CharField(max_length=255,null=False,blank=False,default='')
    survey_id = models.IntegerField(blank=False, default=-1)
    is_active = models.BooleanField( default=True)
    date_created = models.DateTimeField( auto_now_add=True)
    created_by = models.IntegerField(blank=False, default=-1)
    answer_type = models.CharField(choices=answer_types, max_length=30, default="Text Field",blank=True)


class AnswerChoices(models.Model):
    content = models.CharField(max_length=255,null=True,blank=True,default='')
    question_id = models.IntegerField(blank=False, default=-1)

    
