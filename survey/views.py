from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.views import APIView
from user.models import User
from survey.models import Survey,Question,AnswerChoices

# Create your views here.
