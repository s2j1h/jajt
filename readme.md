# 📔 JAJT - Just Another Journaling Tool

Un bot Telegram simple pour créer un journal personnel avec versioning automatique sur GitHub.

## 🚀 Installation rapide

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

Modifiez directement dans `journal_bot.py` :
```python
TELEGRAM_BOT_TOKEN = "VOTRE_TOKEN_TELEGRAM"
GITHUB_TOKEN = "VOTRE_TOKEN_GITHUB"
GITHUB_REPO = "votre-username/votre-repo"
TIMEZONE = "Europe/Paris"  # Votre timezone
```

**OU** utilisez des variables d'environnement (recommandé) :
```bash
export TELEGRAM_BOT_TOKEN="votre_token"
export GITHUB_TOKEN="votre_token"
export GITHUB_REPO="username/repo"
```

### 5. Sécuriser le bot (optionnel mais recommandé)

Pour que seul vous puissiez utiliser le bot :

1. Trouvez votre ID Telegram :
   - Cherchez **@userinfobot** sur Telegram
   - Envoyez `/start`
   - Notez votre ID (nombre comme `123456789`)

2. Ajoutez votre ID dans le code :
```python
AUTHORIZED_USERS = [123456789]  # Remplacez par votre ID
```

## 🎯 Utilisation

### Démarrer le bot

```bash
python journal_bot.py
```

### Commandes disponibles

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

## 📝 Format du journal

Le journal est sauvegardé en Markdown avec ce format :

```markdown
# 📔 Mon Journal Personnel

---

## 📝 2024-01-15 - 14:30
*Par: Jean*

Aujourd'hui j'ai appris à créer un bot Telegram...

---

## 📝 2024-01-15 - 16:45
*Par: Jean*

Deuxième entrée de la journée...

---
```

## 🚀 Déploiement

### Option 1 : Sur votre ordinateur

Laissez simplement le script tourner :
```bash
python journal_bot.py
```

### Option 2 : Sur un VPS (Serveur)

1. Connectez-vous à votre VPS
2. Installez Python 3.8+
3. Clonez le projet
4. Utilisez `screen` ou `systemd` pour le faire tourner en arrière-plan

Avec screen :
```bash
screen -S journal-bot
python journal_bot.py
# Ctrl+A puis D pour détacher
```

### Option 3 : Sur un Raspberry Pi

Parfait pour un bot personnel qui tourne 24/7 !

1. Installez Python et pip
2. Clonez le projet
3. Créez un service systemd :

```bash
sudo nano /etc/systemd/system/journal-bot.service
```

Contenu :
```ini
[Unit]
Description=Journal Telegram Bot
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/journal-bot
ExecStart=/usr/bin/python3 /home/pi/journal-bot/journal_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Puis :
```bash
sudo systemctl enable journal-bot
sudo systemctl start journal-bot
```

### Option 4 : Hébergement gratuit

**Railway.app** (gratuit avec limites) :
1. Créez un compte sur [Railway](https://railway.app)
2. Connectez votre GitHub
3. Déployez depuis votre repo
4. Ajoutez les variables d'environnement

**Render.com** (gratuit avec limites) :
1. Créez un compte sur [Render](https://render.com)
2. Créez un nouveau "Background Worker"
3. Connectez votre repo GitHub
4. Ajoutez les variables d'environnement

## 🔒 Sécurité

- **Ne partagez jamais vos tokens**
- Utilisez un repo privé si votre journal est personnel
- Activez `AUTHORIZED_USERS` pour limiter l'accès
- Utilisez des variables d'environnement plutôt que d'écrire les tokens dans le code

## 🐛 Dépannage

### Le bot ne répond pas
- Vérifiez que le token Telegram est correct
- Vérifiez que le bot est bien démarré (`python journal_bot.py`)
- Regardez les logs dans le terminal

### Erreur GitHub
- Vérifiez le token GitHub et les permissions
- Vérifiez que le nom du repo est correct (format: `username/repo`)
- Vérifiez que le repo existe

### Erreur d'autorisation
- Vérifiez votre ID Telegram avec @userinfobot
- Assurez-vous que votre ID est dans `AUTHORIZED_USERS`

## 📚 Personnalisation

### Changer le format des entrées

Modifiez la fonction `format_entry()` :
```python
def format_entry(self, text, user_name):
    # Personnalisez le format ici
    entry = f"\n### {date_str}\n"
    entry += f"{text}\n"
    return entry
```

### Ajouter des tags

Vous pouvez analyser les messages pour ajouter des tags automatiques :
```python
if "#important" in text:
    entry = f"\n## 📝 {date_str} - {time_str} 🔴 IMPORTANT\n"
```

### Notifications

Ajoutez des rappels quotidiens :
```python
from telegram.ext import JobQueue

async def daily_reminder(context):
    await context.bot.send_message(
        chat_id=YOUR_CHAT_ID,
        text="📝 N'oubliez pas d'écrire dans votre journal aujourd'hui !"
    )

# Dans main()
application.job_queue.run_daily(
    daily_reminder, 
    time=datetime.time(20, 0, 0)  # 20h00
)
```

## 💡 Idées d'amélioration

- Ajouter le support des photos
- Créer des résumés hebdomadaires/mensuels
- Ajouter une recherche dans le journal
- Exporter en PDF
- Ajouter des graphiques de statistiques
- Support multi-utilisateurs avec fichiers séparés

## 📄 License

MIT - Utilisez ce code comme vous voulez !

## 🤝 Support

Des questions ? Créez une issue sur GitHub ou améliorez ce README !