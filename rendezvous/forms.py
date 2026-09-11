from django import forms

from patients.models import Patient

from .models import TypeConsultation


class RendezVousForm(forms.Form):
    """La validation (patient obligatoire, date obligatoire, type valide)
    n'est plus recopiée à la main dans la vue : Django la fait une seule
    fois, ici (DRY)."""

    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        error_messages={"required": "Le patient est obligatoire"},
    )
    type_consultation = forms.ChoiceField(choices=TypeConsultation.choices)
    date = forms.DateField(error_messages={"required": "La date est obligatoire"})
    notes = forms.CharField(required=False, widget=forms.Textarea)
