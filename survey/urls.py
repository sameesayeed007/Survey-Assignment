from django.urls import path, include
from .import views

urlpatterns = [

    path('createSurvey/', views.createSurvey, name ="Create_Survey"),
    path('createQuestion/', views.createQuestion, name ="Create_Question"),
    path('showSurveyList/', views.showSurveyList, name ="Show_Survey_List"),
    path('showSpecificSurvey/<int:survey_id>/', views.showSpecificSurvey, name ="Show_Specific_Survey"),
    path('createSubmission/', views.createSubmission, name ="Create_Submission"),






    
]