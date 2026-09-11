"""
TP3 - Corrigé.

LoginThrottle (services.py) compte les tentatives échouées par identifiant
et bloque temporairement après MAX_TENTATIVES échecs : un script de force
brute se heurte à un mur au bout de quelques essais, même s'il finit par
tomber sur le bon mot de passe.
"""
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from .services import LoginThrottle

_throttle = LoginThrottle()


def connexion(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        if _throttle.est_bloque(username):
            return HttpResponseForbidden(
                "Trop de tentatives échouées pour ce compte. Réessayez dans quelques minutes."
            )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            _throttle.reinitialiser(username)
            login(request, user)
            messages.success(request, f"Bienvenue, {user.username}")
            return redirect("personnel:connexion")

        _throttle.enregistrer_echec(username)
        messages.error(request, "Identifiants incorrects")
        return redirect("personnel:connexion")

    return render(request, "personnel/connexion.html")
