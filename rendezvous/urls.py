from django.urls import path

from . import views

app_name = "rendezvous"

urlpatterns = [
    path("", views.prendre_rendez_vous, name="prendre"),
    path("facture/<int:patient_id>/", views.facture_patient, name="facture"),
]
