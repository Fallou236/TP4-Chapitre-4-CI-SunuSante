# Pipeline CI - SunuSanté

Nom / Groupe :

## 1. Le workflow d'intégration continue (chapitre 4, partie 1)

Le cours décrit 6 étapes, du commit au feedback. Remplissez la colonne de
droite avec le nom exact du stage Jenkins qui correspond, tel qu'il
apparaît dans votre `Jenkinsfile` et dans la Stage View de Jenkins.

| Étape du cours | Stage Jenkins correspondant |
|---|---|
| 1. Commit & push | |
| 2. Notification (Jenkins est prévenu) | |
| 3. Build | |
| 4. Feedback build | |
| 5. Tests automatiques | |
| 6. Feedback tests | |

Comment Jenkins est-il informé qu'un nouveau commit existe, dans votre
configuration (polling SCM, webhook, déclenchement manuel) ?

## 2. Les prérequis d'une bonne CI (chapitre 4, partie 3)

| Prérequis | Statut sur SunuSanté | Détail |
|---|---|---|
| Dépôt avec versioning | | (Git local ? distant ? lequel ?) |
| Standard de code vérifié | | (outil, fichier de config) |
| Serveur d'intégration continue | | (Jenkins, où est-il installé, quel agent ?) |

## 3. Pourquoi Jenkins, ici (chapitre 4, partie 4)

Le cours compare GitLab CI/CD, Jenkins et GitHub Actions. Remplissez ce
comparatif avec vos propres mots, puis justifiez en 2-3 phrases pourquoi
Jenkins convient (ou pas) à ce projet précis.

| Outil | Avantage principal | Inconvénient principal |
|---|---|---|
| GitLab CI/CD | | |
| Jenkins | | |
| GitHub Actions | | |

**Justification du choix pour SunuSanté :**

## 4. CI, Continuous Delivery, déploiement continu

Sur les 3 périmètres vus en cours (CI : code source + tests + build ·
Continuous Delivery : + qualité + release manuelle · déploiement continu :
tout automatisé), lequel votre `Jenkinsfile` couvre-t-il aujourd'hui ?
Qu'est-ce qui manquerait pour passer au périmètre suivant ?

**Périmètre couvert :**

**Ce qui manquerait pour aller plus loin :**

## 5. Tests non fonctionnels hors scope

Le chapitre 4 liste aussi les tests capacitaires et de compatibilité,
absents de ce pipeline. Pourquoi, à l'échelle de ce TP, est-ce un choix
raisonnable plutôt qu'un oubli (indice : YAGNI, chapitre 2) ? Que
faudrait-il ajouter si SunuSanté grandissait réellement ?
