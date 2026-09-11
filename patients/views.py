"""
TP3 - Corrigé.

La recherche passe par l'ORM Django (QuerySet + Q), qui paramètre
automatiquement la requête SQL générée : impossible d'injecter du SQL via
le champ `q`, quel que soit son contenu.
"""
from django.db.models import Q
from django.shortcuts import render

from .models import Patient


def rechercher_patient(request):
    q = request.GET.get("q", "")
    resultats = []

    if q:
        resultats = Patient.objects.filter(Q(nom__icontains=q) | Q(prenom__icontains=q))

    return render(request, "patients/recherche.html", {"q": q, "resultats": resultats})
