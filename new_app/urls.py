from django.urls import path
from .views import hello,users_list,user_details

urlpatterns=[
    path("hello/",hello),
    path("users/",users_list),
    path("users/<int:id>/",user_details),
]