# SunuSanté - TP4 : Tests et intégration continue (Jenkins)

## Contexte

SunuSanté est maintenant sécurisée (TP3). Reste à automatiser tout ce que
vous avez fait à la main jusqu'ici : lancer les tests, vérifier le style,
scanner les vulnérabilités - à chaque commit, sans y penser.

## Installation locale (avant Jenkins)

```bash
python -m venv venv
# Windows : venv\Scripts\activate   |   macOS/Linux : source venv/bin/activate
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py test
```

`requirements-dev.txt` installe l'application (via `-r requirements.txt`)
**et** les outils utilisés par le pipeline : flake8, pip-audit, semgrep.

---

## Partie 1 - Installer Jenkins et lancer un premier pipeline

Suivez `INSTALLATION_JENKINS.md` (choisissez la méthode adaptée à votre
système d'exploitation - Docker est recommandé). À la fin de cette
partie, vous devez avoir un job Jenkins `sunusante-ci` qui exécute le
`Jenkinsfile` fourni.

**Votre première exécution va échouer** : le stage *Standard de code
(lint)* est rouge, volontairement (voir partie 3). C'est normal - c'est
le "feedback build/tests" en quelques minutes dont parle le cours, pas en
semaines.

Complétez ensuite la partie 1 de `CI_TEMPLATE.md`.

## Partie 2 - Compléter la pyramide de tests

Le chapitre 4 distingue tests fonctionnels (unitaires, API, intégration,
système) et non fonctionnels (performance, sécurité, capacitaires,
compatibilité). Les tests unitaires et d'intégration existent déjà
(TP1-TP3). Il manque :

1. **Test système** (`rendezvous/tests_systeme.py`) : un parcours complet
   patient → formulaire → rendez-vous → facture, à travers plusieurs apps
   à la fois. Le TODO dans le fichier détaille les 4 étapes attendues.
2. **Test de performance** (`rendezvous/tests_performance.py`) : un
   "smoke test" qui échoue si `GET /rendezvous/` devient anormalement
   lent. Le TODO dans le fichier explique le seuil attendu.

Les tests de **sécurité** (SAST/SCA) sont déjà couverts par le pipeline
(stages dédiés) - c'est directement la reprise du TP3. Les tests
**capacitaires** et de **compatibilité** ne sont pas traités dans ce TP :
vous justifierez ce choix dans `CI_TEMPLATE.md`, partie 5.

Une fois vos deux tests écrits, `python manage.py test` doit passer à 18
tests, tous verts (aucun `skipped`).

## Partie 3 - Le standard de code casse le build

Le stage *Standard de code (lint)* de votre premier pipeline est rouge.

1. Lancez `flake8 .` en local pour voir l'erreur.
2. Corrigez-la dans `rendezvous/views.py`.
3. Relancez `flake8 .` : il doit être silencieux (aucune sortie, code de
   sortie 0).
4. Relancez le pipeline Jenkins (**Build Now**) : le stage doit passer au
   vert.

Complétez la partie 2 de `CI_TEMPLATE.md`.

## Partie 4 - CI, Continuous Delivery, déploiement continu

Complétez les parties 3 et 4 de `CI_TEMPLATE.md` : comparatif des outils
CI/CD vu en cours, et positionnement de votre pipeline actuel sur les 3
périmètres (CI / Continuous Delivery / déploiement continu).

## Rendu attendu

- `CI_TEMPLATE.md` complété
- `Jenkinsfile` fonctionnel, capture d'écran (ou export) d'un pipeline
  entièrement vert dans Jenkins
- `rendezvous/tests_systeme.py` et `rendezvous/tests_performance.py`
  implémentés
- `rendezvous/views.py` corrigé (plus d'erreur flake8)
- `python manage.py test` : 18 tests, tous verts
