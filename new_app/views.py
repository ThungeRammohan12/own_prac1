from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .serializers import UserSerializer
import json


# Create your views here.

def hello(req):
    return JsonResponse({"msg":"welcome to django"})

@csrf_exempt
def users_list(request):
    if request.method=="GET":
            users=User.objects.all()
            serializer=UserSerializer(users,many=True)
            return JsonResponse(serializer.data,safe=False)
    if request.method=='POST':
         data=json.loads(request.body.decode("utf-8"))
         serializer=UserSerializer(data=data)

         if serializer.is_valid():
              serializer.save()
              return JsonResponse(serializer.data,status=201)
         return JsonResponse(serializer.errors,status=400)

@csrf_exempt
def user_details(request,id):
     try:
          user=User.objects.get(id=id)
     except User.DoesNotExist:
          return JsonResponse({"error":"User not found"},status=404)
     
     #get single user
     if request.method=="GET":
          serializer=UserSerializer(user)
          return JsonResponse(serializer.data)
     
     # UPDATE USER
     if request.method == "PUT":
        data = json.loads(request.body.decode("utf-8"))
        serializer = UserSerializer(user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

        return JsonResponse(serializer.errors, status=400)
     # DELETE USER
     if request.method == "DELETE":
        user.delete()
        return JsonResponse({"message": "User deleted"})

        
          
    