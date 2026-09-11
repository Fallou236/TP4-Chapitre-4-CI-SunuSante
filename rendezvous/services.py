"""
Centralise TOUTE la logique de tarification (principe DRY, chapitre 2).

Dans la version de départ, cette logique était recopiée entre
prendre_rendez_vous() et facture_patient() dans views.py. Ici elle n'existe
qu'à un seul endroit (TarifCalculator), appelée une seule fois au moment de
la création du rendez-vous : le prix est ensuite simplement stocké et lu,
jamais recalculé.

RendezVousService orchestre validation métier + tarification + persistance,
sans rien savoir de HTTP ni d'affichage (SRP) : les vues n'ont plus qu'à
transmettre des données déjà validées par un Form.
"""
from datetime import date

from django.db.models import Sum

from .models import RendezVous, TypeConsultation

MAJORATION_WEEKEND = 0.20
REDUCTION_VIP = 0.10

TARIFS_BASE = {
    TypeConsultation.GENERALISTE: 5000,
    TypeConsultation.SPECIALISTE: 10000,
    TypeConsultation.URGENCE: 15000,
}


class TarifCalculator:
    """Chaque règle est isolée dans sa propre méthode : une seule décision
    par méthode, contre plus de 15 décisions imbriquées dans la version de
    départ (cf. mesure de complexité cyclomatique du TP1)."""

    def calculer(self, type_consultation: str, date_rdv: date, est_vip: bool) -> float:
        prix = self._tarif_base(type_consultation)
        prix = self._appliquer_majoration_weekend(prix, date_rdv)
        prix = self._appliquer_reduction_vip(prix, est_vip)
        return prix

    def _tarif_base(self, type_consultation: str) -> float:
        try:
            return TARIFS_BASE[type_consultation]
        except KeyError as exc:
            raise ValueError(f"Type de consultation inconnu: {type_consultation}") from exc

    def _appliquer_majoration_weekend(self, prix: float, date_rdv: date) -> float:
        return prix * (1 + MAJORATION_WEEKEND) if self._est_weekend(date_rdv) else prix

    def _appliquer_reduction_vip(self, prix: float, est_vip: bool) -> float:
        return prix * (1 - REDUCTION_VIP) if est_vip else prix

    def _est_weekend(self, date_rdv: date) -> bool:
        return date_rdv.weekday() >= 5  # 5 = samedi, 6 = dimanche


class RendezVousService:
    def __init__(self, tarif_calculator: TarifCalculator | None = None):
        self.tarif_calculator = tarif_calculator or TarifCalculator()

    def creer_rendez_vous(
        self, patient, type_consultation: str, date_rdv: date, notes: str = ""
    ) -> RendezVous:
        prix = self.tarif_calculator.calculer(type_consultation, date_rdv, patient.est_vip)
        return RendezVous.objects.create(
            patient=patient,
            type_consultation=type_consultation,
            date=date_rdv,
            prix=prix,
            notes=notes,
        )

    def facturer_patient(self, patient) -> float:
        total = RendezVous.objects.filter(patient=patient).aggregate(total=Sum("prix"))["total"]
        return total or 0
