# JAJT - Just Another Journaling Tool

Un bot Telegram simple pour créer un journal personnel avec versioning automatique sur GitHub.

## Fonctionnalités

### v1
- Création d'une entrée
- Visualisation de la dernière entrée enregistrée
- Statistiques
- Accès au journal complet via son lien sur github

### v1.1
- ajout d'un job qui demandera à l'utilisateur 1/jour pour écrire une entrée (à 20h00)

### v1.2
- Possibilité de mettre le script dans un container docker


## Installation rapide

### 1. Créer un bot Telegram

1. Ouvrez Telegram et cherchez **@BotFather**
2. Envoyez `/newbot`
3. Choisissez un nom pour votre bot (ex: "Mon Journal Personnel")
4. Choisissez un username unique finissant par `bot` (ex: `mon_journal_perso_bot`)
5. **Gardez le token** que BotFather vous donne (format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Créer un token GitHub

1. Allez sur GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Cliquez sur "Generate new token (classic)"
3. Nom: "Journal Bot"
4. Cochez les permissions :
   - ✅ `repo` (toutes les sous-options)
5. Générez et **copiez le token**

### 3. Créer un repository GitHub

1. Créez un nouveau repository sur GitHub (public ou privé)
2. Nom suggéré : `mon-journal` ou `personal-journal`
3. Initialisez avec un README si vous voulez

### 4. Configuration du bot

1. **Clonez ce projet** :
```bash
git clone [votre-repo]
cd [votre-repo]
```

2. **Installez les dépendances** :
```bash
pip install -r requirements.txt
```

3. **Configurez les variables** :

Créez un fichier .env qui contiendra les différentes variables (ou utiliser l'exemple dans  `.env-example`)
```bash
TELEGRAM_BOT_TOKEN = "VOTRE_TOKEN_TELEGRAM"
GITHUB_TOKEN = "VOTRE_TOKEN_GITHUB"
GITHUB_REPO = "votre-username/votre-repo"
JOURNAL_FILE = "journal.md"  # Nom du fichier dans le repo
TIMEZONE = "Europe/Paris"  # Votre timezone
AUTHORIZED_USERS = "" #la liste des utilisateurs autorisés à utiliser le bot, à récupérer via @userinfobot
```

## Utilisation

### Démarrer le bot

#### en mode simple
```bash
python journal_bot.py
```

#### via docker
cf. `quick-start-docker.md`

### Commandes disponibles dans Telegram

- `/start` - Initialiser le bot
- `/help` - Afficher l'aide
- `/stats` - Voir vos statistiques
- `/last` - Voir votre dernière entrée
- `/github` - Obtenir le lien vers votre journal

### Créer une entrée

Envoyez simplement un message texte au bot !

Exemple :
```
Aujourd'hui j'ai appris à créer un bot Telegram. 
C'est fascinant de voir comment on peut automatiser 
la création d'un journal personnel ! 🚀
```

## Format du journal

Le journal est sauvegardé en Markdown avec ce format :

```markdown
# 📔 Mon Journal Personnel

---

## 📝 2024-01-15 - 14:30

Aujourd'hui j'ai appris à créer un bot Telegram...

---

## 📝 2024-01-15 - 16:45

Deuxième entrée de la journée...

---
```

## Déploiement

### Option 1 : Sur votre ordinateur

Laissez simplement le script tourner :
```bash
python journal_bot.py
```

### Option 2 : via un container



## Sécurité

- **Ne partagez jamais vos tokens**
- Utilisez un repo privé si votre journal est personnel

## Dépannage

### Le bot ne répond pas
- Vérifiez que le token Telegram est correct
- Vérifiez que le bot est bien démarré (`python main.py`)
- Regardez les logs dans le terminal

### Erreur GitHub
- Vérifiez le token GitHub et les permissions
- Vérifiez que le nom du repo est correct (format: `username/repo`)
- Vérifiez que le repo existe

### Erreur d'autorisation
- Vérifiez votre ID Telegram avec @userinfobot
- Assurez-vous que votre ID est dans `AUTHORIZED_USERS`

## Idées d'amélioration

- Ajouter le support des photos
- Créer des résumés hebdomadaires/mensuels
- Ajouter une recherche dans le journal
- Exporter en PDF
- Ajouter des graphiques de statistiques
- Support multi-utilisateurs avec fichiers séparés
- gestion de tags

## License

MIT - Utilisez ce code comme vous voulez !

## Support

Des questions ? Créez une issue sur GitHub ou améliorez ce README !