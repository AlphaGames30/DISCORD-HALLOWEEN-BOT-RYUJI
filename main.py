import os
import sys
from threading import Thread
import time

def run_bot():
    print("🎃 Démarrage du bot Discord...")
    try:
        from bot import start_bot
        start_bot()
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du bot: {e}")
        sys.exit(1)

def run_web():
    print("🌐 Démarrage de l'interface web...")
    time.sleep(2)
    try:
        from web_app import run_flask
        run_flask()
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur web: {e}")
        sys.exit(1)

if __name__ == '__main__':
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        print('❌ ERREUR: DISCORD_TOKEN non défini dans les variables d\'environnement!')
        print('📝 Veuillez ajouter votre token Discord dans les Secrets')
        print('\n💡 Pour ajouter votre token:')
        print('   1. Cliquez sur l\'icône de cadenas (Secrets) dans la barre latérale')
        print('   2. Ajoutez une nouvelle variable: DISCORD_TOKEN')
        print('   3. Collez votre token Discord')
        sys.exit(1)
    
    print('=' * 50)
    print('🎃 HALLOWEEN DISCORD BOT - Démarrage')
    print('=' * 50)
    
    web_thread = Thread(target=run_web, daemon=True)
    web_thread.start()
    
    run_bot()
