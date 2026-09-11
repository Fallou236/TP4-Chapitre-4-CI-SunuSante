# Installer Jenkins en local

Jenkins est un serveur : il tourne en tâche de fond et expose une interface
web sur `http://localhost:8080`. Choisissez **une seule** méthode
d'installation ci-dessous, selon votre système d'exploitation et vos
préférences. Java 17 (ou plus) est nécessaire dans tous les cas, sauf si
vous choisissez l'option Docker (le conteneur l'embarque déjà). Docker
n'est **pas obligatoire** pour ce TP : ce n'est qu'une des méthodes
possibles, à choisir si vous préférez éviter d'installer Java/Jenkins
directement sur votre machine.

## Option Docker - si vous préférez cette approche (Windows, macOS, Linux)

Jenkins tourne dans un conteneur, ce qui évite d'installer Java et Jenkins
directement sur votre machine, et donne un environnement identique quel
que soit votre système d'exploitation.

### Installer Docker lui-même

Si Docker n'est pas déjà sur votre machine :

- **Windows** : téléchargez et installez
  [Docker Desktop](https://www.docker.com/products/docker-desktop/).
  Nécessite WSL2 (l'installeur propose de l'activer automatiquement si
  besoin) ; un redémarrage est généralement demandé.
- **macOS** : téléchargez
  [Docker Desktop](https://www.docker.com/products/docker-desktop/)
  (choisissez la version Apple Silicon ou Intel selon votre Mac), ou via
  Homebrew : `brew install --cask docker` puis lancez l'application une
  fois pour terminer l'installation.
- **Linux (Debian/Ubuntu)** : script officiel, le plus simple :
  ```bash
  curl -fsSL https://get.docker.com | sudo sh
  sudo usermod -aG docker $USER
  ```
  Déconnectez-vous/reconnectez-vous (ou `newgrp docker`) pour que
  l'appartenance au groupe `docker` prenne effet sans `sudo`.
- **Linux (Fedora/RHEL)** :
  ```bash
  sudo dnf install -y dnf-plugins-core
  sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
  sudo dnf install -y docker-ce docker-ce-cli containerd.io
  sudo systemctl enable --now docker
  sudo usermod -aG docker $USER
  ```

Vérifiez ensuite que Docker fonctionne :

```bash
docker run hello-world
```

Si ce test affiche un message de bienvenue, Docker est prêt et vous
pouvez passer à la suite.

### Lancer Jenkins dans Docker

```bash
docker volume create jenkins_home

docker run -d --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts-jdk17
```

Sous **Windows (PowerShell)**, adaptez les retours à la ligne :

```powershell
docker volume create jenkins_home

docker run -d --name jenkins `
  -p 8080:8080 -p 50000:50000 `
  -v jenkins_home:/var/jenkins_home `
  jenkins/jenkins:lts-jdk17
```

Le montage de `/var/run/docker.sock` (Linux/macOS) permet à Jenkins de
lancer des conteneurs Docker pour exécuter le pipeline (voir plus bas,
l'agent Python du `Jenkinsfile`). Sous Windows avec Docker Desktop, si ce
montage pose problème, vous pouvez l'omettre et installer Python
directement sur l'agent Jenkins (voir la note en fin de fichier).

## Windows - installeur natif

1. Téléchargez le fichier `.msi` depuis [jenkins.io/download](https://www.jenkins.io/download/)
   (section Windows).
2. Lancez l'installeur : il installe Jenkins comme service Windows et
   installe un JDK si nécessaire.
3. Jenkins démarre automatiquement et est accessible sur
   `http://localhost:8080`.

## macOS - Homebrew

```bash
brew install openjdk@17
brew install jenkins-lts
brew services start jenkins-lts
```

## Linux (Debian/Ubuntu) - dépôt officiel

```bash
sudo apt update && sudo apt install -y openjdk-17-jre

curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key \
  | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/" \
  | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update && sudo apt install -y jenkins
sudo systemctl enable --now jenkins
```

## Linux (Fedora/RHEL) - dépôt officiel

```bash
sudo dnf install -y java-17-openjdk

sudo wget -O /etc/yum.repos.d/jenkins.repo \
  https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key

sudo dnf install -y jenkins
sudo systemctl enable --now jenkins
```

---

## Configuration initiale (identique quelle que soit la méthode)

1. Ouvrez `http://localhost:8080`.
2. Jenkins demande un **mot de passe administrateur initial**. Récupérez-le :
   - Docker : `docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword`
   - Windows/macOS/Linux natif : ouvrez le fichier indiqué à l'écran
     (généralement `.../secrets/initialAdminPassword`)
3. Cliquez sur **Installer les plugins suggérés** (inclut Git, Pipeline -
   nécessaires pour ce TP).
4. Créez votre compte administrateur.
5. Gardez l'URL par défaut (`http://localhost:8080/`).

## Créer le pipeline SunuSanté

1. Sur le tableau de bord Jenkins : **Nouveau Item** → nom `sunusante-ci`
   → type **Pipeline** → OK.
2. Dans la section **Pipeline**, choisissez :
   - **Definition** : `Pipeline script from SCM`
   - **SCM** : `Git`, renseignez le chemin de votre dépôt local
     (ex. `file:///C:/chemin/vers/votre/depot` sous Windows, ou
     `file:///home/vous/sunusante` sous Linux/macOS) - ou l'URL de votre
     dépôt GitHub si vous l'avez poussé en ligne.
   - **Script Path** : `Jenkinsfile` (déjà fourni à la racine du projet)
3. Cliquez sur **Save**, puis **Build Now** pour lancer une première
   exécution.

## Note sur l'agent Python

Attention à ne pas confondre deux choix indépendants :

- **Comment Jenkins lui-même est installé** - Docker ou natif, c'est la
  question traitée plus haut dans ce fichier.
- **Comment le pipeline exécute ses étapes** (le "agent" du
  `Jenkinsfile`) - c'est ce dont parle cette section.

Vous pouvez tout à fait installer Jenkins nativement (Windows/macOS/Linux)
et quand même utiliser un agent Docker pour le pipeline si Docker est
disponible sur cette machine - ou inversement, installer Jenkins via
Docker et faire tourner le pipeline avec `agent any`. Les deux réglages
sont indépendants.

Le `Jenkinsfile` fourni utilise par défaut un agent Docker (`agent {
docker { image 'python:3.11-slim' } }`) : chaque étape tourne dans un
conteneur Python jetable, sans rien installer sur la machine qui exécute
le pipeline. Cela nécessite le plugin **Docker Pipeline** (proposez son
installation si Jenkins vous le signale en rouge à la première exécution :
**Manage Jenkins → Plugins → Available**) et que Docker soit accessible
depuis l'agent Jenkins qui exécute le pipeline.

Si vous ne pouvez pas utiliser Docker comme agent (ex. Jenkins installé
nativement sans accès à un démon Docker), remplacez dans `Jenkinsfile` :

```groovy
agent { docker { image 'python:3.11-slim' } }
```

par :

```groovy
agent any
```

et installez Python 3.11+ directement sur la machine qui héberge
l'agent Jenkins (vérifiez que `python` et `pip` sont bien dans le PATH).

Aucune autre ligne du `Jenkinsfile` n'a besoin de changer : les stages
appellent toutes la fonction `runCmd()` définie en haut du fichier, qui
teste `isUnix()` et bascule automatiquement entre `sh` (Linux/macOS) et
`bat` (Windows). Avec l'agent Docker, `isUnix()` renvoie toujours vrai
(le conteneur est Linux) ; avec `agent any` sur un poste Windows natif,
`isUnix()` renvoie faux et les mêmes commandes sont exécutées via `bat` -
sans rien à adapter vous-même.
