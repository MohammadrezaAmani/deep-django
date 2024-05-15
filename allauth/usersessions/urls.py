from allauth.usersessions import views
from django.urls import path

urlpatterns = [
    path("", views.list_usersessions, name="usersessions_list"),
]
