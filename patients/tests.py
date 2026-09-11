from django.test import TestCase

from .models import Patient


class RechercherPatientTest(TestCase):
    def setUp(self):
        Patient.objects.create(nom="Ndiaye", prenom="Awa", email="awa@example.com")
        Patient.objects.create(nom="Diop", prenom="Moussa", email="moussa@example.com")

    def test_recherche_normale_filtre_correctement(self):
        resp = self.client.get("/patients/recherche/", {"q": "Ndiaye"})
        self.assertEqual(len(resp.context["resultats"]), 1)

    def test_tentative_injection_sql_ne_contourne_pas_le_filtre(self):
        # Avant le correctif, ce payload renvoyait TOUS les patients.
        payload = "' OR '1'='1"
        resp = self.client.get("/patients/recherche/", {"q": payload})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context["resultats"]), 0)
