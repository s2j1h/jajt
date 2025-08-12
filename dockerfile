# Utiliser Python 3.11 slim pour une image plus légère
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY main.py .

# Créer un utilisateur non-root pour la sécurité
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Variables d'environnement par défaut
ENV PYTHONUNBUFFERED=1
ENV JOURNAL_FILE=journal.md
ENV TIMEZONE=Europe/Paris

# Port expose (optionnel, le bot Telegram n'en a pas besoin)
# EXPOSE 8080

# Commande de santé pour Docker
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('https://api.telegram.org', timeout=5)" || exit 1

# Commande pour démarrer l'application
CMD ["python", "main.py"]