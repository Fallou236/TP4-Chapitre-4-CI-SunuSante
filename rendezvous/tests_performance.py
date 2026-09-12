"""
TP4, partie 2 — Test non fonctionnel de performance (chapitre 4).

"Est-ce que c'est rapide ?" On ne fait pas ici un vrai test de charge
(outils dédiés : Locust, k6 — hors scope de ce TP), mais un test de
performance minimal ("smoke test") qui échoue si une régression grossière
rend une page anormalement lente.

Le seuil est volontairement généreux (1 seconde) : le but n'est pas de
mesurer une performance fine, mais de détecter une dégradation majeure
(requête N+1, boucle coûteuse, etc.) tout en restant fiable même sur une
machine chargée comme un agent CI.
"""
import time

from django.test import TestCase
from django.urls import reverse

SEUIL_SECONDES = 1.0


class PerformanceFormulaireTest(TestCase):
    def test_formulaire_repond_rapidement(self):
        debut = time.perf_counter()
        reponse = self.client.get(reverse("rendezvous:prendre"))
        duree = time.perf_counter() - debut

        # La page doit d'abord répondre correctement...
        self.assertEqual(reponse.status_code, 200)
        # ...et le faire sous le seuil.
        self.assertLess(
            duree,
            SEUIL_SECONDES,
            f"GET /rendezvous/ a mis {duree:.3f}s (seuil {SEUIL_SECONDES}s)",
        )
