from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .serializers import UserSerializer
import json
import jwt
import datetime
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

def hello(req):
    return JsonResponse({"msg": "welcome to django"})


# Helper: create JWT
def create_jwt(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


# ---------------- REGISTER ----------------
@csrf_exempt
def users_list(request):
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        # 1) Hash password
        hashed_password = make_password(data["password"])

        # 2) Create user
        user = User.objects.create(
            name=data["name"],
            email=data["email"],
            password=hashed_password
        )

        # 3) Create JWT
        token = create_jwt(user)

        serializer = UserSerializer(user)

        # 4) Return response + cookie
        response = JsonResponse({
            "message": "Registration successful",
            "user": serializer.data,
            "token": token   # for debugging
        }, status=201)

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            samesite="Lax",
            max_age=60 * 60 * 24
        )

        return response


# ---------------- GET / UPDATE / DELETE USER ----------------
@csrf_exempt
def user_details(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    if request.method == "GET":
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    if request.method == "PUT":
        data = json.loads(request.body.decode("utf-8"))
        serializer = UserSerializer(user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

        return JsonResponse(serializer.errors, status=400)

    if request.method == "DELETE":
        user.delete()
        return JsonResponse({"message": "User deleted"})


# ---------------- LOGIN ----------------
@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        email = data.get("email")
        password = data.get("password")

        # 1) Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"error": "Invalid email"}, status=400)

        # 2) Validate password
        if not check_password(password, user.password):
            return JsonResponse({"error": "Invalid password"}, status=400)

        # 3) Create JWT
        token = create_jwt(user)

        # 4) Send token in cookie
        response = JsonResponse({
            "message": "Login successful",
            "token": token
        })

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            samesite="Lax",
            max_age=60 * 60  # 1 hour
        )

        return response
