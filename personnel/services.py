"""
Protège la connexion du personnel contre la force brute (chapitre 3).

Utilise le cache Django (LocMemCache par défaut en développement, Redis ou
Memcached en production) pour compter les tentatives échouées par
identifiant, sans dépendance externe ni nouvelle table en base.
"""
from django.core.cache import cache

MAX_TENTATIVES = 5
DUREE_BLOCAGE_SECONDES = 15 * 60  # 15 minutes


class LoginThrottle:
    """Une seule responsabilité : décider si un identifiant est
    temporairement bloqué après trop d'échecs (SRP, chapitre 2)."""

    def _cle(self, identifiant: str) -> str:
        return f"login_tentatives:{identifiant}"

    def est_bloque(self, identifiant: str) -> bool:
        return cache.get(self._cle(identifiant), 0) >= MAX_TENTATIVES

    def enregistrer_echec(self, identifiant: str) -> None:
        cle = self._cle(identifiant)
        tentatives = cache.get(cle, 0) + 1
        cache.set(cle, tentatives, timeout=DUREE_BLOCAGE_SECONDES)

    def reinitialiser(self, identifiant: str) -> None:
        cache.delete(self._cle(identifiant))
