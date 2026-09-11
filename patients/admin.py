from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("prenom", "nom", "email", "est_vip")
    search_fields = ("nom", "prenom", "email")
