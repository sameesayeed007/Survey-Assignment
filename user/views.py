from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.views import APIView
from user.models import User
from rest_framework import permissions, status
from django.contrib.auth import authenticate


# Create your views here.

#Admins will register through this API 
@api_view(["POST"])
def register(request):

    try:

        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')
        isAdmin = request.data.get('isAdmin')

        if isAdmin == "True": 
            #The new user created will be an admin
            
            newUser = User.objects.create(email = email, name = name, is_staff = True, is_active = True) 
            newUser.set_password(password)
            newUser.save()
            return JsonResponse({'success':True, 'message': 'Registration is successful. An admin has been created.'}, status=status.HTTP_201_CREATED)
        else:
            #The new user created will be a user
            newUser = User.objects.create(email = email,name = name, is_staff = False, is_active = True)
            newUser.set_password(password) 
            newUser.save()
            return JsonResponse({'success':True, 'message': 'Registration is successful. A user has been created.'}, status=status.HTTP_201_CREATED)

    except Exception as e:

        errors = str(e)
        return JsonResponse({'success':False, 'message': 'Some error occurred.','errors': errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(["POST"])
def login(request):

    try:

        email = request.POST['email']
        password = request.POST['password']
        isAdmin = request.data.get('isAdmin')
        # print(email)
        # print(password)

        if isAdmin == "True": 
            #authenticate user
            specificUser = authenticate(email= email, password= password)

            if specificUser: 
                if specificUser.is_staff == True:
                    specUser = {'userId':specificUser.id, 'email':specificUser.email}
                    return JsonResponse({'success':True, 'message': 'Login is successful','data':specUser}, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'success':False,'message':'The user here is not an admin.'})
            else:
                return JsonResponse({'success':False,'message':'Please enter the correct admin credentials'},status=status.HTTP_400_BAD_REQUEST)

        else:
            #authenticate user
            specificUser = authenticate(email=email, password=password)

            if specificUser: 
                if specificUser.is_staff == False:
                    specUser = {'userId':specificUser.id, 'email':specificUser.email}
                    return JsonResponse({'success':True, 'message': 'Login is successful','data':specUser}, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'success':False,'message':'The user here is not a regular user.'})
            else:
                return JsonResponse({'success':False,'message':'Please enter the correct user credentials'},status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:

        errors = str(e)
        return JsonResponse({'success':False, 'message': 'Some error occurred.','errors': errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


