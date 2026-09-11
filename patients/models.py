from django.db import models


class Patient(models.Model):
    """
    Un patient de la clinique SunuSanté.

    Donnée sensible (chapitre 2, gestion des risques) : ce modèle est lié à
    des informations de santé via ses rendez-vous. Classez ce risque dans
    RISQUES_TEMPLATE.md (important / modéré / faible).
    """

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    est_vip = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
