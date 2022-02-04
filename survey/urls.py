from django.urls import path, include
from .import views

urlpatterns = [

    path('createSurvey/', views.createSurvey, name ="Create_Survey"),



    
]