from django.urls import path

from . import views

app_name = "personnel"

urlpatterns = [
    path("connexion/", views.connexion, name="connexion"),
]
