from rest_framework import serializers
from user.models import User
from survey.models import Survey,Question,AnswerChoices,Submission,Answers




class SurveySerializer(serializers.ModelSerializer):
    admin_information = serializers.SerializerMethodField(method_name='get_admin_info')
    class Meta:
        model = Survey
        fields = "__all__"

    def get_admin_info(self,instance):
        try:
            specificUser = User.objects.get(id= instance.created_by)
        except:
            specificUser = None
        print(specificUser)

        if specificUser:
            admin_name = specificUser.name
            admin_email = specificUser.email
            adminObj = {"admin_name":admin_name, "admin_email":admin_email}
            return adminObj

        else:
            return {}


class QuestionSerializer(serializers.ModelSerializer):
    answer_choices = serializers.SerializerMethodField(method_name='get_answer_choices')
    class Meta:
        model = Question
        fields = "__all__"

    def get_answer_choices(self,instance):
        try:
            specific_choices = AnswerChoices.objects.filter(question_id= instance.id)
        except:
            specific_choices = None
       

        if specific_choices:
            all_choices = list(specific_choices.values_list('content',flat=True))
            return all_choices


        else:
            return []


class SurveyInfoSerializer(serializers.ModelSerializer):
    admin_information = serializers.SerializerMethodField(method_name='get_admin_info')
    questions = serializers.SerializerMethodField(method_name='get_questions')
    class Meta:
        model = Survey
        fields = "__all__"

    def get_admin_info(self,instance):
        try:
            specificUser = User.objects.get(id= instance.created_by)
        except:
            specificUser = None
        print(specificUser)

        if specificUser:
            admin_name = specificUser.name
            admin_email = specificUser.email
            adminObj = {"admin_name":admin_name, "admin_email":admin_email}
            return adminObj

        else:
            return {}

    def get_questions(self,instance):
        try:
            questions = Question.objects.filter(survey_id= instance.id)
        except:
            questions = None

        if questions:
            question_serializer = QuestionSerializer(questions,many=True)
            return question_serializer.data

        else:
            return []