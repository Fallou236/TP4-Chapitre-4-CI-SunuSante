// Pipeline Jenkins pour SunuSanté (chapitre 4).
//
// Chaque stage correspond à une étape du workflow vu en cours :
// Récupération du code -> Build -> Standard de code -> Tests -> Sécurité.
// Un stage rouge arrête le pipeline : c'est le "feedback" du serveur CI au
// dépôt, en quelques minutes plutôt qu'en semaines (cf. chapitre 4, partie 1).

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
        // HOME hors du workspace : les dépendances installées avec --user
        // vont dans /tmp/.local et non dans le dépôt, donc flake8 ne les
        // analyse pas.
        HOME = "/tmp/jenkins-home"
        PIP_CACHE_DIR = "/tmp/jenkins-home/.pip-cache"
    }

    stages {
        stage('Récupération du code') {
            steps {
                checkout scm
                // Nettoie tout résidu d'un build antérieur avant analyse.
                runCmd 'rm -rf .local .pip-cache staticfiles'
            }
        }

        stage('Installation des dépendances') {
            steps {
                runCmd 'mkdir -p $HOME'
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
            // flake8 lit sa configuration depuis le fichier .flake8 versionné
            // avec le code (max-line-length, dossiers exclus).
            steps {
                runCmd 'export PATH=$HOME/.local/bin:$PATH && flake8 .'
            }
        }

        stage('Tests') {
            steps {
                runCmd 'python manage.py test'
            }
        }

        stage('Sécurité - SAST') {
            steps {
                runCmd 'export PATH=$HOME/.local/bin:$PATH && semgrep --config p/security-audit --config p/django --config p/python --error patients rendezvous personnel sunusante'
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
