"""
TP4, partie 2 — Test système (chapitre 4).

Un test système exerce l'application ENTIÈRE, de bout en bout, comme le
ferait un utilisateur : formulaire -> soumission -> facture. Contrairement
aux tests unitaires (TP1/TP2) ou aux tests d'intégration vue par vue
(TP3), on ne teste pas ici un composant isolé, mais l'enchaînement complet
à travers plusieurs apps (patients + rendezvous).
"""
from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from patients.models import Patient
from rendezvous.models import RendezVous, TypeConsultation

# Le service refuse les dates passées (règle métier du TP2) : on vise donc
# un mardi futur, calculé dynamiquement pour que le test ne pourrisse pas
# avec le temps. weekday() : 0 = lundi, 1 = mardi.
_BASE = date.today() + timedelta(days=30)
FUTUR_MARDI = _BASE + timedelta(days=(1 - _BASE.weekday()) % 7)


class ParcoursCompletRendezVousTest(TestCase):
    def test_parcours_complet_de_la_prise_de_rendez_vous_a_la_facture(self):
        # 1. Un patient existe dans le système.
        patient = Patient.objects.create(
            nom="Ndiaye", prenom="Awa", email="awa@example.sn", est_vip=False
        )

        # 2. Le formulaire de prise de rendez-vous s'affiche et présente
        #    le patient (GET traversant patients + rendezvous).
        reponse_formulaire = self.client.get(reverse("rendezvous:prendre"))
        self.assertEqual(reponse_formulaire.status_code, 200)
        self.assertContains(reponse_formulaire, "Awa")

        # 3. On soumet une prise de rendez-vous (POST -> service -> base).
        reponse_post = self.client.post(
            reverse("rendezvous:prendre"),
            {
                "patient": patient.id,
                "type_consultation": TypeConsultation.GENERALISTE,
                "date": FUTUR_MARDI.isoformat(),
                "notes": "",
            },
        )
        # POST-Redirect-Get : succès => redirection.
        self.assertEqual(reponse_post.status_code, 302)
        # Le rendez-vous a bien été enregistré, au bon tarif.
        rdv = RendezVous.objects.get(patient=patient)
        self.assertEqual(rdv.prix, Decimal("5000"))

        # 4. La facture du patient affiche le total attendu.
        reponse_facture = self.client.get(
            reverse("rendezvous:facture", args=[patient.id])
        )
        self.assertEqual(reponse_facture.status_code, 200)
        self.assertEqual(reponse_facture.context["total"], Decimal("5000"))
