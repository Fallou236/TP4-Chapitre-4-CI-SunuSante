from django.contrib import admin

from .models import RendezVous


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ("patient", "type_consultation", "date", "prix")
    list_filter = ("type_consultation",)
