# Démarrage Rapide avec Docker

Guide ultra-rapide pour faire tourner JAJT avec Docker en 5 minutes.

## Prérequis

✅ **Docker** installé ([Guide d'installation](https://docs.docker.com/get-docker/))  
✅ **Docker Compose** installé (inclus avec Docker Desktop)

## Installation en 5 étapes

### 1. Cloner le projet
```bash
git clone [votre-repo]
cd jajt
```

### 2. Configurer l'environnement
```bash
# Copier le fichier d'exemple
cp .env-example .env

# Éditer avec vos tokens
nano .env  # ou votre éditeur préféré
```

Remplissez au minimum :
- `TELEGRAM_BOT_TOKEN` (via @BotFather)
- `GITHUB_TOKEN` (GitHub Settings > Developer settings)
- `GITHUB_REPO` (votre-username/votre-repo)
- `AUTHORIZED_USERS`(la liste des utilisateurs autorisés)


### 3. Démarrer le bot
```bash
# Rendre le script exécutable
chmod +x deploy.sh

# Démarrer (build + run)
./deploy.sh start
```

### 4. Vérifier que cela fonctionne
```bash
# Voir le statut
./deploy.sh status

# Voir les logs
./deploy.sh logs
```

### 5. Tester sur Telegram
- Cherchez votre bot sur Telegram
- Envoyez `/start`
- Écrivez votre première entrée !

## Commandes utiles

```bash
# Gestion du bot
./deploy.sh start    # Démarrer
./deploy.sh stop     # Arrêter  
./deploy.sh restart  # Redémarrer
./deploy.sh status   # Statut

# Monitoring
./deploy.sh logs     # Logs temps réel (Ctrl+C pour quitter)

# Maintenance
./deploy.sh update   # Mettre à jour
./deploy.sh cleanup  # Nettoyer Docker
```

## Résolution rapide des problèmes

### Le bot ne répond pas ?
```bash
# 1. Vérifier les logs
./deploy.sh logs

# 2. Vérifier le statut
./deploy.sh status

# 3. Redémarrer si besoin
./deploy.sh restart
```

### Variables d'environnement incorrectes ?
```bash
# Éditer la config
nano .env

# Redémarrer pour prendre en compte
./deploy.sh restart
```

### Problème de permissions ?
```bash
# Reconstruire complètement
docker-compose down
docker-compose up -d --build --force-recreate
```

## Structure des fichiers créés

Après installation, vous aurez :

```
jajt/
├── main.py              # Code principal
├── requirements.txt     # Dépendances Python
├── Dockerfile          # Configuration Docker
├── docker-compose.yml  # Orchestration
├── deploy.sh           # Script de gestion
├── .env                # Vos variables (à créer)
├── .env.example        # Exemple de config
├── logs/               # Logs du bot (créé auto)
├── README.md           # Documentation
└── quick-start-docker.md # Ce fichier
```

## Monitoring simple

```bash
# Ressources utilisées
docker stats jajt-bot

# Santé du container
docker inspect jajt-bot --format='{{.State.Health.Status}}'

# Logs des dernières 24h
docker logs jajt-bot --since 24h
```

---

Consultez le README.md complet pour plus d'options et de fonctionnalités.