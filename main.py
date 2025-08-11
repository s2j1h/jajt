import os
import logging
from datetime import datetime
import pytz
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from github import Github
from dotenv import load_dotenv



# Configuration depuis les variables d'environnement
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "")
JOURNAL_FILE = os.getenv("JOURNAL_FILE", "journal.md")
TIMEZONE = os.getenv("TIMEZONE", "Europe/Paris")

# ID Telegram autorisés (optionnel - pour sécuriser le bot)
# Format: "123456789,987654321" dans la variable d'environnement
AUTHORIZED_USERS_STR = os.getenv("AUTHORIZED_USERS", "0")
AUTHORIZED_USERS = [int(id.strip()) for id in AUTHORIZED_USERS_STR.split(",") if id.strip()]

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class JournalBot:
    def __init__(self):
        self.github = Github(GITHUB_TOKEN)
        self.repo = self.github.get_repo(GITHUB_REPO)
        self.tz = pytz.timezone(TIMEZONE)
        
    def get_current_content(self):
        """Récupère le contenu actuel du fichier journal"""
        try:
            file_contents = self.repo.get_contents(JOURNAL_FILE)
            return file_contents.decoded_content.decode('utf-8'), file_contents
        except:
            # Le fichier n'existe pas encore
            return "", None
    
    def format_entry(self, text):
        """Formate une entrée de journal"""
        now = datetime.now(self.tz)
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M")
        
        # Format Markdown pour une belle présentation
        entry = f"\n## 📝 {date_str} - {time_str}\n"
        entry += f"{text}\n"
        entry += f"\n---\n"
        
        return entry
    
    def save_to_github(self, new_entry, user_name):
        """Sauvegarde l'entrée dans GitHub"""
        try:
            # Récupérer le contenu actuel
            current_content, file_obj = self.get_current_content()
            
            # Si le fichier n'existe pas, créer un header
            if not current_content:
                current_content = "# 📔 Mon Journal Personnel\n\n"
                current_content += f"*Créé le {datetime.now(self.tz).strftime('%Y-%m-%d')}*\n"
                current_content += "\n---\n"
            
            # Ajouter la nouvelle entrée
            updated_content = current_content + new_entry
            
            # Créer le message de commit
            commit_message = f"✏️ Nouvelle entrée - {datetime.now(self.tz).strftime('%Y-%m-%d %H:%M')}"
            
            # Mettre à jour ou créer le fichier
            if file_obj:
                self.repo.update_file(
                    JOURNAL_FILE,
                    commit_message,
                    updated_content,
                    file_obj.sha
                )
            else:
                self.repo.create_file(
                    JOURNAL_FILE,
                    commit_message,
                    updated_content
                )
            
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde: {e}")
            return False

# Gestionnaires de commandes
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /start"""
    user = update.effective_user
    
    # Vérifier l'autorisation si configurée
    if AUTHORIZED_USERS and user.id not in AUTHORIZED_USERS:
        await update.message.reply_text(
            "❌ Désolé, vous n'êtes pas autorisé à utiliser ce bot."
        )
        return
    
    welcome_message = """
🎉 Bienvenue dans votre Journal Personnel !

📝 **Comment utiliser ce bot :**
• Envoyez simplement un message pour créer une entrée
• Utilisez /stats pour voir vos statistiques
• Utilisez /last pour voir votre dernière entrée
• Utilisez /help pour revoir ces instructions

Tous vos messages sont sauvegardés sur GitHub avec versioning complet !

Commencez dès maintenant en envoyant votre premier message 📖
    """
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /help"""
    help_text = """
📚 **Just Another Journaling Tool - Jalt**

**Commandes disponibles :**
• /start - Démarrer le bot
• /help - Afficher cette aide
• /stats - Voir vos statistiques
• /last - Voir votre dernière entrée
• /github - Obtenir le lien vers votre journal

**Formats supportés :**
• Texte simple
• Emojis 😊
• Liens
• **Markdown** basique

Envoyez simplement un message pour créer une entrée !
    """
    await update.message.reply_text(help_text)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /stats - Affiche les statistiques du journal"""
    user = update.effective_user
    
    if AUTHORIZED_USERS and user.id not in AUTHORIZED_USERS:
        return
    
    try:
        bot = JournalBot()
        content, _ = bot.get_current_content()
        
        if content:
            # Compter les entrées (chaque entrée commence par ##)
            entries_count = content.count("\n## 📝")
            words_count = len(content.split())
            
            stats_message = f"""
📊 **Statistiques de votre journal**

• 📝 Nombre d'entrées : {entries_count}
• 📖 Nombre de mots total : {words_count}
• 📅 Première entrée : {datetime.now(bot.tz).strftime('%Y-%m-%d')}
            """
        else:
            stats_message = "📊 Aucune entrée pour le moment. Commencez à écrire !"
        
        await update.message.reply_text(stats_message)
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur lors de la récupération des stats: {e}")

async def last_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /last - Affiche la dernière entrée"""
    user = update.effective_user
    
    if AUTHORIZED_USERS and user.id not in AUTHORIZED_USERS:
        return
    
    try:
        bot = JournalBot()
        content, _ = bot.get_current_content()
        
        if content and "## 📝" in content:
            # Extraire la dernière entrée
            entries = content.split("\n## 📝")
            if len(entries) > 1:
                last = "## 📝" + entries[-1].split("\n---")[0]
                await update.message.reply_text(f"**Votre dernière entrée :**\n\n{last}")
            else:
                await update.message.reply_text("Aucune entrée trouvée.")
        else:
            await update.message.reply_text("📖 Votre journal est vide pour le moment.")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur: {e}")

async def github_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /github - Donne le lien vers le journal"""
    user = update.effective_user
    
    if AUTHORIZED_USERS and user.id not in AUTHORIZED_USERS:
        return
    
    github_url = f"https://github.com/{GITHUB_REPO}/blob/main/{JOURNAL_FILE}"
    await update.message.reply_text(
        f"🔗 **Votre journal sur GitHub :**\n{github_url}"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestionnaire principal pour tous les messages texte"""
    user = update.effective_user
    
    # Vérifier l'autorisation
    if AUTHORIZED_USERS and user.id not in AUTHORIZED_USERS:
        await update.message.reply_text(
            "❌ Vous n'êtes pas autorisé à utiliser ce bot."
        )
        return
    
    text = update.message.text
    user_name = user.first_name or "Anonyme"
    
    # Feedback immédiat
    processing_msg = await update.message.reply_text("✍️ Enregistrement en cours...")
    
    try:
        # Créer et sauvegarder l'entrée
        bot = JournalBot()
        entry = bot.format_entry(text)
        
        if bot.save_to_github(entry, user_name):
            # Succès
            await processing_msg.edit_text(
                "✅ **Entrée sauvegardée !**\n\n"
                f"📅 {datetime.now(bot.tz).strftime('%H:%M')} - "
                f"{len(text.split())} mots ajoutés à votre journal."
            )
            
            # Log pour debug
            logger.info(f"Entrée sauvegardée pour {user_name}: {text[:50]}...")
        else:
            await processing_msg.edit_text(
                "❌ Erreur lors de la sauvegarde. Veuillez réessayer."
            )
    except Exception as e:
        logger.error(f"Erreur: {e}")
        await processing_msg.edit_text(
            f"❌ Une erreur s'est produite: {str(e)}"
        )

def main():
    """Fonction principale"""
    # Créer l'application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Ajouter les gestionnaires de commandes
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("last", last_entry))
    application.add_handler(CommandHandler("github", github_link))
    
    # Gestionnaire pour tous les messages texte
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Démarrer le bot
    logger.info("🚀 Bot démarré !")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()