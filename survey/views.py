from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.views import APIView
from user.models import User
from survey.models import Survey,Question,AnswerChoices,Submission,Answers
from rest_framework import permissions, status
from survey.serializers import SurveySerializer,SurveyInfoSerializer,SubmissionSerializer,SubmissionInfoSerializer


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



#This will add a question to a specific survey
@api_view(["POST"])
def createQuestion(request):
    try:

        # data = {
        # "admin_id" : 11,
        # "survey_id" : 1,
        # "question" : "What is your gender?",
        # "answer_type": "Check Box",
        # "answer_choices" : ["male","female","others"]
        # }
        data = request.data

        admin_id = data["admin_id"]
        survey_id = data["survey_id"]
        question = data["question"]
        answer_type = data["answer_type"]
        answer_choices = data["answer_choices"]
        
        try:
            specificUser = User.objects.get(id=admin_id)
        except:
            specificUser = None

        if specificUser:
            if specificUser.is_staff == True:
                if specificUser.is_active == True:
                    #Create a question
                    specificQuestion = Question.objects.create(created_by = admin_id,survey_id = survey_id,question =question,answer_type = answer_type )
                    specificQuestion.save()
                    question_id = specificQuestion.id
                    if specificQuestion.answer_type == "Dropdown":
                        #Create a Answer Choice fields
                        for k in range(len(answer_choices)):
                            answer_choice = AnswerChoices.objects.create(content = answer_choices[k],question_id = question_id)
                            answer_choice.save()
                    elif specificQuestion.answer_type == "Check Box":
                        #Create a Answer Choice fields
                        for k in range(len(answer_choices)):
                            answer_choice = AnswerChoices.objects.create(content = answer_choices[k],question_id = question_id)
                            answer_choice.save()
                    elif specificQuestion.answer_type == "Radio Button":
                        #Create a Answer Choice fields
                        for k in range(len(answer_choices)):
                            answer_choice = AnswerChoices.objects.create(content = answer_choices[k],question_id = question_id)
                            answer_choice.save()
                    elif specificQuestion.answer_type == "Text Field":
                        pass 
                    elif specificQuestion.answer_type == "Number Field":
                        pass 
                    else:
                        #Delete the question 
                        specificQuestion.delete()
                        return JsonResponse({'success':False, 'message': 'The question type is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
 
                    answerObj = {"id":specificQuestion.id, "question":specificQuestion.question,"survey_id":specificQuestion.survey_id, "admin_id":specificQuestion.created_by,"date_created":specificQuestion.date_created,"answer_type":specificQuestion.answer_type,"answer_choices":answer_choices}
                    return JsonResponse({'success':True, 'message': 'A survey has been created.',"data":answerObj}, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse({'success':False, 'message': 'This admin is not an active user.'}, status=status.HTTP_400_BAD_REQUEST)

                 
            else:
                return JsonResponse({'success':False, 'message': 'This user is not an admin.'}, status=status.HTTP_400_BAD_REQUEST)

        
        else:
            return JsonResponse({'success':False, 'message': 'This admin does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    
    except Exception as e:

        errors = str(e)
        return JsonResponse({'success':False, 'message': 'Some error occurred.','errors': errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#This API will display the list of all the active surveys
@api_view(["GET"])
def showSurveyList(request):
    try:
        try:
            surveys = Survey.objects.filter(is_active= True)
        except:
            surveys = None

        if surveys:
            
            survey_serializer = SurveySerializer(surveys,many=True)
            return JsonResponse({'success':True,'message':'Survey data is shown.','data':survey_serializer.data},status=status.HTTP_200_OK)
        else:
            return JsonResponse({'success':False,'message':'Survey data not found.'},status=status.HTTP_404_NOT_FOUND)

    except Exception as e:

        errors = str(e)
        return JsonResponse({'success':False, 'message': 'Some error occurred.','errors': errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#This API will display a specific survey with its questions 
@api_view(["GET"])
def showSpecificSurvey(request,survey_id):
    try:
        try:
            surveys = Survey.objects.get(id= survey_id)
        except:
            surveys = None


        if surveys:
            
            survey_serializer = SurveyInfoSerializer(surveys,many=False)
            return JsonResponse({'success':True,'message':'Survey data is shown.','data':survey_serializer.data},status=status.HTTP_200_OK)

        else:
            return JsonResponse({'success':False,'message':'Survey data not found.'},status=status.HTTP_404_NOT_FOUND)


    except Exception as e:

        errors = str(e)
        return JsonResponse({'success':False, 'message': 'Some error occurred.','errors': errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#This will be done by the end user. Answers to questions will be created and and submission to a form will be made
@api_view(["POST"])
def createSubmission(request):
    try:


        # data = {
        # "user_id" : 10,
        # "survey_id" : 1,
        # "answers": [{"question_id":1,"answer":["male"]},
        #             {"question_id":2,"answer":["Cricket","Football"]},
        #             {"question_id":3,"answer":["Ruhul"]},
        #             {"question_id":4,"answer":["22"]},
        #             {"question_id":5,"answer":["3"]}]
        # }
        data = request.data

        user_id = data["user_id"]
        survey_id = data["survey_id"]
        answers = data["answers"]


        try:
            specificUser = User.objects.get(id=user_id)
        except:
            specificUser = None

        if specificUser:
            if specificUser.is_staff == False:
                if specificUser.is_active == True:
                    #Create a submission
                    specificSubmission = Submission.objects.create(survey_id = survey_id, user_id = user_id )
                    specificSubmission.save() 
                    submission_id = specificSubmission.id
                    #Create the answers 
                    for k in range(len(answers)):
                        for m in range(len(answers[k]["answer"])):
                            #Create an an answer 
                            specificAnswer = Answers.objects.create(submission_id = submission_id, user_id = user_id, question_id = answers[k]["question_id"],answer =answers[k]["answer"][m])
                            specificAnswer.save()

                    return JsonResponse({'success':True, 'message': 'Form has been submitted and answers have been recorded.'}, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse({'success':False, 'message': 'This user is not an active user.'}, status=status.HTTP_400_BAD_REQUEST)

                 
            else:
                return JsonResponse({'success':False, 'message': 'This user is not a regular user.'}, status=status.HTTP_400_BAD_REQUEST)

        
        else:
            return JsonResponse({'success':False, 'message': 'This user does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        

    except Exception as e:

        errors = str(e)
        return JsonResponse({'success':False, 'message': 'Some error occurred.','errors': errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#This API will display the list of all the submissions. This will be used in admin's reports section
@api_view(["GET"])
def showSubmissionList(request):
    try:
        try:
            submissions = Submission.objects.all()
        except:
            submissions = None

        if submissions:
            
            submission_serializer = SubmissionSerializer(submissions,many=True)
            return JsonResponse({'success':True,'message':'Submission data is shown.','data':submission_serializer.data},status=status.HTTP_200_OK)
        else:
            return JsonResponse({'success':False,'message':'Submission data not found.'},status=status.HTTP_404_NOT_FOUND)

    except Exception as e:

        errors = str(e)
        return JsonResponse({'success':False, 'message': 'Some error occurred.','errors': errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#This API will display the list of all the submissions made by a specific end user. This will be used in admin's reports section
@api_view(["GET"])
def showSubmissionListSpecificUser(request,user_id):
    try:
        try:
            submissions = Submission.objects.filter(user_id = user_id)
        except:
            submissions = None

        if submissions:
            
            submission_serializer = SubmissionSerializer(submissions,many=True)
            return JsonResponse({'success':True,'message':'Submission data is shown.','data':submission_serializer.data},status=status.HTTP_200_OK)
        else:
            return JsonResponse({'success':False,'message':'Submission data not found.'},status=status.HTTP_404_NOT_FOUND)

    except Exception as e:

        errors = str(e)
        return JsonResponse({'success':False, 'message': 'Some error occurred.','errors': errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#This API will display the list of all the submissions of a specific survey. This will be used in admin's reports section
@api_view(["GET"])
def showSubmissionListSpecificSurvery(request,survey_id):
    try:
        try:
            submissions = Submission.objects.filter(survey_id = survey_id)
        except:
            submissions = None

        if submissions:
            
            submission_serializer = SubmissionSerializer(submissions,many=True)
            return JsonResponse({'success':True,'message':'Submission data is shown.','data':submission_serializer.data},status=status.HTTP_200_OK)
        else:
            return JsonResponse({'success':False,'message':'Submission data not found.'},status=status.HTTP_404_NOT_FOUND)

    except Exception as e:

        errors = str(e)
        return JsonResponse({'success':False, 'message': 'Some error occurred.','errors': errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#This will show the submission details of a specific submission (questions and answers of a specific survey). This will be used in the admin's report section
@api_view(["GET"])
def showSubmissionDetails(request,submission_id):
    try:
        try:
            submission = Submission.objects.get(id = submission_id)
        except:
            submission = None

        if submission:
            
            submission_serializer = SubmissionInfoSerializer(submission,many=False)
            return JsonResponse({'success':True,'message':'Submission data is shown.','data':submission_serializer.data},status=status.HTTP_200_OK)
        else:
            return JsonResponse({'success':False,'message':'Submission data not found.'},status=status.HTTP_404_NOT_FOUND)

    except Exception as e:

        errors = str(e)
        return JsonResponse({'success':False, 'message': 'Some error occurred.','errors': errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)