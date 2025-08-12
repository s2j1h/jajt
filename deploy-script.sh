#!/bin/bash

# Script de déploiement pour JAJT Bot
# Usage: ./deploy.sh [start|stop|restart|logs|status]

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonctions utilitaires
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérification des prérequis
check_requirements() {
    log_info "Vérification des prérequis..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker n'est pas installé. Installez Docker et réessayez."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose n'est pas installé. Installez Docker Compose et réessayez."
        exit 1
    fi
    
    if [ ! -f ".env" ]; then
        log_error "Fichier .env non trouvé. Créez-le avec vos variables d'environnement."
        echo "Exemple de contenu .env :"
        echo "TELEGRAM_BOT_TOKEN=your_token_here"
        echo "GITHUB_TOKEN=your_github_token"
        echo "GITHUB_REPO=username/repo"
        echo "AUTHORIZED_USERS=123456789"
        exit 1
    fi
    
    log_success "Prérequis validés ✓"
}

# Fonction de démarrage
start_bot() {
    log_info "Démarrage du bot JAJT..."
    check_requirements
    
    # Créer le dossier logs s'il n'existe pas
    mkdir -p logs
    
    # Build et démarrage
    docker-compose up -d --build
    
    log_success "Bot démarré avec succès ! 🚀"
    log_info "Utilisez './deploy.sh logs' pour voir les logs"
    log_info "Utilisez './deploy.sh status' pour voir le statut"
}

# Fonction d'arrêt
stop_bot() {
    log_info "Arrêt du bot JAJT..."
    docker-compose down
    log_success "Bot arrêté"
}

# Fonction de redémarrage
restart_bot() {
    log_info "Redémarrage du bot JAJT..."
    stop_bot
    start_bot
}

# Affichage des logs
show_logs() {
    log_info "Affichage des logs (Ctrl+C pour quitter)..."
    docker-compose logs -f journal-bot
}

# Statut du bot
show_status() {
    log_info "Statut du bot JAJT..."
    echo
    docker-compose ps
    echo
    
    # Vérifier si le container tourne
    if docker-compose ps | grep -q "Up"; then
        log_success "Le bot est en cours d'exécution ✓"
        
        # Afficher les dernières lignes de log
        log_info "Dernières activités :"
        docker-compose logs --tail=5 journal-bot
    else
        log_warning "Le bot n'est pas en cours d'exécution"
    fi
}

# Fonction de mise à jour
update_bot() {
    log_info "Mise à jour du bot..."
    docker-compose down
    docker-compose pull
    docker-compose up -d --build
    log_success "Bot mis à jour et redémarré"
}

# Fonction de nettoyage
cleanup() {
    log_info "Nettoyage des images Docker inutilisées..."
    docker-compose down
    docker system prune -f
    log_success "Nettoyage terminé"
}

# Menu principal
case "$1" in
    start)
        start_bot
        ;;
    stop)
        stop_bot
        ;;
    restart)
        restart_bot
        ;;
    logs)
        show_logs
        ;;
    status)
        show_status
        ;;
    update)
        update_bot
        ;;
    cleanup)
        cleanup
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|logs|status|update|cleanup}"
        echo
        echo "Commandes disponibles :"
        echo "  start    - Démarrer le bot"
        echo "  stop     - Arrêter le bot"
        echo "  restart  - Redémarrer le bot"
        echo "  logs     - Afficher les logs en temps réel"
        echo "  status   - Afficher le statut du bot"
        echo "  update   - Mettre à jour et redémarrer le bot"
        echo "  cleanup  - Nettoyer les images Docker inutilisées"
        exit 1
        ;;
esac