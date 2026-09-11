"""
TP4, partie 2 — Test système (chapitre 4).

Un test système exerce l'application ENTIÈRE, de bout en bout, comme le
ferait un utilisateur : formulaire -> soumission -> facture. Contrairement
aux tests unitaires (TP1/TP2) ou aux tests d'intégration vue par vue
(TP3), on ne teste pas ici un composant isolé, mais l'enchaînement complet
à travers plusieurs apps (patients + rendezvous).

TODO (TP4) : écrivez un test qui, dans une seule méthode :
1. crée un patient (Patient.objects.create)
2. affiche le formulaire de prise de rendez-vous (GET /rendezvous/) et
   vérifie que le patient y apparaît
3. soumet une prise de rendez-vous (POST /rendezvous/)
4. consulte la facture du patient (GET /rendezvous/facture/<id>/) et
   vérifie que le total affiché correspond au tarif attendu

Comparez avec solution/rendezvous/tests_systeme.py une fois terminé.
"""
from django.test import TestCase

# TODO (TP4) : importez Patient (patients.models) une fois que vous en
# avez besoin dans le test ci-dessous.


class ParcoursCompletRendezVousTest(TestCase):
    def test_parcours_complet_de_la_prise_de_rendez_vous_a_la_facture(self):
        self.skipTest("TODO (TP4) : à implémenter, voir la consigne ci-dessus")
