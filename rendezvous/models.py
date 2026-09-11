from django.db import models

from patients.models import Patient


class TypeConsultation(models.TextChoices):
    GENERALISTE = "GENERALISTE", "Généraliste"
    SPECIALISTE = "SPECIALISTE", "Spécialiste"
    URGENCE = "URGENCE", "Urgence"


class RendezVous(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="rendez_vous")
    type_consultation = models.CharField(max_length=20, choices=TypeConsultation.choices)
    date = models.DateField()
    prix = models.DecimalField(max_digits=8, decimal_places=0)
    notes = models.TextField(blank=True, default="")
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.type_consultation} - {self.date}"
