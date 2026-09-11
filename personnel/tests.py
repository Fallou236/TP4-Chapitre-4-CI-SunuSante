from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase

from .services import LoginThrottle


class LoginThrottleTest(TestCase):
    def setUp(self):
        cache.clear()
        self.throttle = LoginThrottle()

    def test_pas_bloque_avant_le_seuil(self):
        for _ in range(4):
            self.throttle.enregistrer_echec("secretaire")
        self.assertFalse(self.throttle.est_bloque("secretaire"))

    def test_bloque_apres_le_seuil(self):
        for _ in range(5):
            self.throttle.enregistrer_echec("secretaire")
        self.assertTrue(self.throttle.est_bloque("secretaire"))

    def test_reinitialiser_debloque(self):
        for _ in range(5):
            self.throttle.enregistrer_echec("secretaire")
        self.throttle.reinitialiser("secretaire")
        self.assertFalse(self.throttle.est_bloque("secretaire"))


class ConnexionViewTest(TestCase):
    def setUp(self):
        cache.clear()
        User.objects.create_user(username="secretaire", password="motdepasse-correct")

    def test_brute_force_est_bloque_apres_5_echecs(self):
        for _ in range(5):
            resp = self.client.post(
                "/personnel/connexion/",
                {"username": "secretaire", "password": "mauvais-mdp"},
            )
            self.assertEqual(resp.status_code, 302)

        # La 6e tentative est bloquée, MÊME avec le bon mot de passe.
        resp_bloque = self.client.post(
            "/personnel/connexion/",
            {"username": "secretaire", "password": "motdepasse-correct"},
        )
        self.assertEqual(resp_bloque.status_code, 403)

    def test_connexion_reussie_avant_le_seuil_fonctionne(self):
        for _ in range(3):
            self.client.post(
                "/personnel/connexion/",
                {"username": "secretaire", "password": "mauvais-mdp"},
            )

        resp = self.client.post(
            "/personnel/connexion/",
            {"username": "secretaire", "password": "motdepasse-correct"},
            follow=True,
        )
        self.assertContains(resp, "Bienvenue")
