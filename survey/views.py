from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.views import APIView
from user.models import User
from survey.models import Survey,Question,AnswerChoices
from rest_framework import permissions, status

# Create your views here.

#This will be used to create a survey 
@api_view(["POST"])
def createSurvey(request):
    try:
        
        survey_name = request.data.get('survey_name')
        admin_id = request.data.get('admin_id')
        
        try:
            specificUser = User.objects.get(id=admin_id)
        except:
            specificUser = None

        if specificUser:
            if specificUser.is_staff == True:
                if specificUser.is_active == True:
                    #Create a survery
                    survey_object = Survey.objects.create(name = survey_name, created_by =admin_id )
                    survey_object.save()
                    surveyObj = {"id":survey_object.id, "name":survey_object.name, "admin_id":survey_object.created_by,"date_created":survey_object.date_created}
                    return JsonResponse({'success':True, 'message': 'A survey has been created.',"data":surveyObj}, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse({'success':False, 'message': 'This admin is not an active user.'}, status=status.HTTP_400_BAD_REQUEST)

                 
            else:
                return JsonResponse({'success':False, 'message': 'This user is not an admin.'}, status=status.HTTP_400_BAD_REQUEST)

        
        else:
            return JsonResponse({'success':False, 'message': 'This admin does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    
    except Exception as e:

        errors = str(e)
        return JsonResponse({'success':False, 'message': 'Some error occurred.','errors': errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

