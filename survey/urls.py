from django.urls import path, include
from .import views

urlpatterns = [

    path('createSurvey/', views.createSurvey, name ="Create_Survey"),
    path('createQuestion/', views.createQuestion, name ="Create_Question"),
    path('showSurveyList/', views.showSurveyList, name ="Show_Survey_List"),
    path('showSpecificSurvey/<int:survey_id>/', views.showSpecificSurvey, name ="Show_Specific_Survey"),
    path('createSubmission/', views.createSubmission, name ="Create_Submission"),
    path('showSubmissionList/', views.showSubmissionList, name ="Show_Submission_List"),
    path('showSubmissionListSpecificSurvery/<int:survey_id>/', views.showSubmissionListSpecificSurvery, name ="Show_Submission_List_Specific_Survey"),
    path('showSubmissionListSpecificUser/<int:user_id>/', views.showSubmissionListSpecificUser, name ="Show_Submission_List_Specific_User"),
    path('showSubmissionDetails/<int:submission_id>/', views.showSubmissionDetails, name ="Show_Submission_Details"),
    
    




    
]