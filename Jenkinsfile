// Pipeline Jenkins pour SunuSanté (chapitre 4).
//
// Chaque stage correspond à une étape du workflow vu en cours :
// Récupération du code -> Build -> Standard de code -> Tests -> Sécurité.
// Un stage rouge arrête le pipeline : c'est le "feedback" du serveur CI au
// dépôt, en quelques minutes plutôt qu'en semaines (cf. chapitre 4, partie 1).
//
// Portabilité (voir INSTALLATION_JENKINS.md) : avec l'agent Docker
// (recommandé), tous les stages tournent dans un conteneur Linux, quel
// que soit le système d'exploitation qui héberge Jenkins.

def runCmd(String commande) {
    if (isUnix()) {
        sh commande
    } else {
        bat commande
    }
}

pipeline {
    agent {
        docker { image 'python:3.11-slim' }
    }

    environment {
        // L'agent tourne avec l'UID de Jenkins (1000), sans home accessible
        // dans python:3.11-slim. On redirige HOME et le cache pip vers le
        // workspace, où l'UID a les droits en écriture.
        HOME = "${WORKSPACE}"
        PIP_CACHE_DIR = "${WORKSPACE}/.pip-cache"
    }

    stages {
        stage('Récupération du code') {
            steps {
                checkout scm
            }
        }

        stage('Installation des dépendances') {
            // --user installe dans $HOME/.local ; on exporte ensuite
            // $HOME/.local/bin dans le PATH pour que flake8, semgrep et
            // pip-audit soient trouvés par les stages suivants. Le PATH est
            // exporté dans chaque stage shell car chaque `sh` ouvre un shell
            // neuf (l'export ne persiste pas d'un stage à l'autre).
            steps {
                runCmd 'python -m pip install --user --upgrade pip'
                runCmd 'pip install --user -r requirements-dev.txt'
            }
        }

        stage('Build') {
            steps {
                runCmd 'python manage.py check'
                runCmd 'python manage.py collectstatic --noinput --dry-run'
            }
        }

        stage('Standard de code (lint)') {
            // Prérequis d'une bonne CI, chapitre 4 partie 3 : le style est
            // vérifié par la machine, la revue de code se concentre sur le fond.
            steps {
                runCmd 'export PATH=$HOME/.local/bin:$PATH && flake8 .'
            }
        }

        stage('Tests') {
            // Unitaires, intégration et système (TP1-TP4) sont tous exécutés
            // ici par le même appel : manage.py les découvre automatiquement.
            steps {
                runCmd 'python manage.py test'
            }
        }

        stage('Sécurité - SAST') {
            // cf. chapitre 3 et chapitre 4 partie 2 : "tests de sécurité,
            // cf. SAST/DAST/SCA au chapitre 3".
            steps {
                runCmd 'export PATH=$HOME/.local/bin:$PATH && semgrep --config p/security-audit --config p/django --config p/python --error .'
            }
        }

        stage('Sécurité - SCA') {
            steps {
                runCmd 'export PATH=$HOME/.local/bin:$PATH && pip-audit -r requirements.txt'
            }
        }
    }

    post {
        success {
            echo 'Pipeline vert : build, lint, tests et sécurité tous OK.'
        }
        failure {
            echo 'Pipeline rouge : consultez le premier stage en échec ci-dessus.'
        }
    }
}
