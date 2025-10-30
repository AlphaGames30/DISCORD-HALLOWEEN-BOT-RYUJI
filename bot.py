import discord
import requests 
from discord.ext import commands
import json
import random
import os
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
import threading
from flask import Flask

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

DATA_FILE = Path(__file__).parent / 'data.json'

HALLOWEEN_EMOJIS = [
    {'emoji': '👻', 'probability': 0.4000, 'points': 4, 'name': 'fantôme'},
    {'emoji': '🧟', 'probability': 0.3500, 'points': 7, 'name': 'zombie'},
    {'emoji': '💀', 'probability': 0.1500, 'points': 10, 'name': 'crâne'},
    {'emoji': '🔪', 'probability': 0.0909, 'points': 12, 'name': 'couteau'},
    {'emoji': '🐺', 'probability': 0.0082, 'points': 17, 'name': 'loup'},
    {'emoji': '🎃', 'probability': 0.0008, 'points': 31, 'name': 'citrouille'},
    {'emoji': '🍬', 'probability': 0.0001, 'points': 50, 'name':'bonbon'}
]

message_count = 1
next_reaction_at = random.randint(15, 30)
user_data = {}
health_boost_active = False

def select_random_emoji():
    random_value = random.random()
    cumulative_probability = 0
    
    for emoji_data in HALLOWEEN_EMOJIS:
        cumulative_probability += emoji_data['probability']
        if random_value < cumulative_probability:
            return emoji_data
    
    return HALLOWEEN_EMOJIS[-1]

import requests

GIST_ID = os.getenv("GIST_ID")
GITHUB_GIST_TOKEN = os.getenv("GITHUB_GIST_TOKEN")

def load_data():
    """Charge les données du Gist GitHub"""
    global user_data, health_boost_active
    if not GIST_ID or not GITHUB_GIST_TOKEN:
        print("⚠️ Variables d'environnement GIST_ID ou GITHUB_GIST_TOKEN manquantes — impossible de charger depuis GitHub.")
        user_data = {}
        health_boost_active = False
        return

    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {"Authorization": f"token {GITHUB_GIST_TOKEN}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        gist_data = response.json()
        content = list(gist_data["files"].values())[0]["content"]
        data = json.loads(content)

        if isinstance(data, dict) and "_system" in data:
            health_boost_active = data["_system"].get("health_boost_active", False)
            user_data = {k: v for k, v in data.items() if k != "_system"}
        else:
            user_data = data
            health_boost_active = False

        print("✅ Données chargées depuis le Gist GitHub")
    except Exception as e:
        print(f"❌ Erreur lors du chargement du Gist : {e}")
        user_data = {}
        health_boost_active = False

@bot.event
async def on_ready():
    print(f'🎃 Bot connecté en tant que {bot.user}')
    print(f'👻 Prêt à réagir tous les {next_reaction_at} messages')
    load_data()

@bot.event
async def on_message(message):
    global message_count, next_reaction_at, health_boost_active
    
    if message.author.bot:
        return
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict) and '_system' in data:
                health_boost_active = data['_system'].get('health_boost_active', False)
    except:
        pass
    
    message_count += 1
    
    if message_count >= next_reaction_at:
        selected_emoji = select_random_emoji()
        
        try:
            await message.add_reaction(selected_emoji['emoji'])
            
            user = get_user_data(message.author.id)
            points_earned = selected_emoji['points']
            
            if health_boost_active:
                points_earned = int(points_earned * 1.5)
                user['healthBoost'] += points_earned - selected_emoji['points']
            
            user['points'] += points_earned
            
            if selected_emoji['name'] not in user['reactions']:
                user['reactions'][selected_emoji['name']] = 0
            user['reactions'][selected_emoji['name']] += 1
           
def save_data():
    """Sauvegarde les données dans DATA_FILE (data.json)."""
    global user_data, health_boost_active

    data_to_save = {"_system": {"health_boost_active": health_boost_active}}
    data_to_save.update(user_data)

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        print("💾 Données sauvegardées avec succès dans data.json")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde des données : {e}")

            
            boost_msg = ' (Health Boost x1.5 actif!)' if health_boost_active else ''
            await message.reply(
                f"{selected_emoji['emoji']} Tu as gagné **{points_earned} points** avec {selected_emoji['name']}!{boost_msg} "
                f"Total: **{user['points']} points**"
            )
            
            print(f"🎃 Réaction {selected_emoji['emoji']} ({selected_emoji['points']}pts) sur message de {message.author}")
        except Exception as e:
            print(f'❌ Erreur lors de la réaction: {e}')
        
        message_count = 0
        next_reaction_at = random.randint(15, 30)
        print(f'⏳ Prochaine réaction dans {next_reaction_at} messages')
    
    await bot.process_commands(message)

@bot.command(name='points')
async def points_command(ctx):
    await leaderboard_command(ctx)

@bot.command(name='leaderboard')
async def leaderboard_command(ctx):
    if not user_data:
        await ctx.reply('🎃 Aucun joueur n\'a encore de points!')
        return
    
    sorted_users = sorted(
        [(user_id, data) for user_id, data in user_data.items()],
        key=lambda x: x[1]['points'],
        reverse=True
    )[:10]
    
    leaderboard = '🎃 **CLASSEMENT HALLOWEEN** 🎃\n\n'
    
    for i, (user_id, data) in enumerate(sorted_users):
        try:
            user = await bot.fetch_user(int(user_id))
            medal = '🥇' if i == 0 else '🥈' if i == 1 else '🥉' if i == 2 else f'{i + 1}.'
            leaderboard += f'{medal} **{user.name}**: {data["points"]} points\n'
        except:
            leaderboard += f'{i + 1}. Utilisateur inconnu: {data["points"]} points\n'
    
    await ctx.reply(leaderboard)

@bot.command()
async def backup(ctx):
    """Force la sauvegarde des données et envoie un résumé en MP."""
    global user_data, health_boost_active

    # Vérifie que la fonction save_data existe
    try:
        save_data()
    except NameError:
        await ctx.send("⚠️ La fonction `save_data()` n'est pas définie. Impossible de sauvegarder.")
        return

    # Crée un résumé des données utilisateurs
    summary_lines = []
    for user_id, user_info in user_data.items():
        points = user_info.get("points", 0)
        health = user_info.get("healthBoost", 0)
        reactions = user_info.get("reactions", {})
        reactions_str = ", ".join(f"{k}: {v}" for k, v in reactions.items()) if reactions else "aucune"
        summary_lines.append(f"<@{user_id}> - Points: {points}, HealthBoost: {health}, Reactions: {reactions_str}")

    summary = "\n".join(summary_lines) if summary_lines else "Aucun utilisateur à afficher."

    # Envoi du résumé en MP à l'auteur
    try:
        await ctx.author.send(f"💾 Sauvegarde effectuée !\nRésumé des données :\n{summary}")
        await ctx.send("✅ Je t'ai envoyé un MP avec le résumé de la sauvegarde.")
    except:
        await ctx.send("⚠️ Impossible de t'envoyer un MP. Assure-toi que tes messages privés sont ouverts.")

@bot.command(name='serverreactions')
async def serverreactions_command(ctx):
    if not user_data:
        await ctx.reply('🎃 Aucune réaction enregistrée pour le moment!')
        return
    
    total_reactions = {}
    total_points = 0
    total_users = len(user_data)
    
    for user_id, data in user_data.items():
        total_points += data['points']
        for emoji_name, count in data.get('reactions', {}).items():
            if emoji_name not in total_reactions:
                total_reactions[emoji_name] = 0
            total_reactions[emoji_name] += count
    
    stats_msg = '🎃 **STATISTIQUES GLOBALES DU SERVEUR** 🎃\n\n'
    stats_msg += f'👥 Joueurs actifs: **{total_users}**\n'
    stats_msg += f'💰 Points totaux distribués: **{total_points}**\n\n'
    stats_msg += f'📊 **Réactions totales par emoji:**\n'
    
    if total_reactions:
        sorted_reactions = sorted(total_reactions.items(), key=lambda x: x[1], reverse=True)
        for emoji_name, count in sorted_reactions:
            emoji_data = next((e for e in HALLOWEEN_EMOJIS if e['name'] == emoji_name), None)
            emoji_icon = emoji_data['emoji'] if emoji_data else '❓'
            stats_msg += f'{emoji_icon} **{emoji_name}**: {count}x ({emoji_data["points"] if emoji_data else "?"} pts chacun)\n'
    else:
        stats_msg += 'Aucune réaction pour le moment!\n'
    
    await ctx.reply(stats_msg)

@bot.command(name='claim')
async def claim_command(ctx):
    user = get_user_data(ctx.author.id)
    now = datetime.now()
    
    if user['lastClaim']:
        last_claim = datetime.fromisoformat(user['lastClaim'])
        time_diff = now - last_claim
        
        if time_diff < timedelta(hours=24):
            remaining = timedelta(hours=24) - time_diff
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            await ctx.reply(f'⏰ Tu as déjà réclamé tes points aujourd\'hui! Reviens dans **{hours}h {minutes}m**.')
            return
    
    selected_emoji = select_random_emoji()
    points_earned = selected_emoji['points']
    
    if health_boost_active:
        points_earned = int(points_earned * 1.5)
        user['healthBoost'] += points_earned - selected_emoji['points']
    
    user['points'] += points_earned
    
    if selected_emoji['name'] not in user['reactions']:
        user['reactions'][selected_emoji['name']] = 0
    user['reactions'][selected_emoji['name']] += 1
    
    user['lastClaim'] = now.isoformat()
    
    save_data()
    
    boost_msg = ' (Health Boost x1.5 actif!)' if health_boost_active else ''
    await ctx.reply(
        f"🎁 {selected_emoji['emoji']} Claim réussi! Tu as gagné **{points_earned} points** avec {selected_emoji['name']}!{boost_msg}\n"
        f"Total: **{user['points']} points**\n"
        f"Reviens dans 24h pour ton prochain claim!"
    )
    print(f"🎁 Claim de {ctx.author}: {selected_emoji['emoji']} ({points_earned}pts)")

@bot.command(name='pointadd')
@commands.has_permissions(administrator=True)
async def pointadd_command(ctx, member: discord.Member, points: int):
    if points < 0:
        await ctx.reply('❌ Le nombre de points doit être positif!')
        return
    
    user = get_user_data(member.id)
    user['points'] += points
    save_data()
    
    await ctx.reply(f'✅ **{points} points** ajoutés à {member.mention}! Nouveau total: **{user["points"]} points**')
    print(f'➕ Admin {ctx.author} a ajouté {points}pts à {member}')

@bot.command(name='pointremove')
@commands.has_permissions(administrator=True)
async def pointremove_command(ctx, member: discord.Member, points: int):
    if points < 0:
        await ctx.reply('❌ Le nombre de points doit être positif!')
        return
    
    user = get_user_data(member.id)
    user['points'] = max(0, user['points'] - points)
    save_data()
    
    await ctx.reply(f'✅ **{points} points** retirés de {member.mention}! Nouveau total: **{user["points"]} points**')
    print(f'➖ Admin {ctx.author} a retiré {points}pts à {member}')

@bot.command(name='healthboost')
async def healthboost_command(ctx):
    global health_boost_active
    health_boost_active = not health_boost_active
    save_data()
    status = 'activé ✅' if health_boost_active else 'désactivé ❌'
    extra_msg = ' Les points sont multipliés par 1.5!' if health_boost_active else ''
    await ctx.reply(f'🏥 Health Boost {status}!{extra_msg}')
    print(f'🏥 Health Boost {status}')

@bot.command(name='stats')
async def stats_command(ctx):
    user = get_user_data(ctx.author.id)
    stats_msg = f'📊 **Tes statistiques Halloween** 📊\n\n'
    stats_msg += f'💰 Points totaux: **{user["points"]}**\n'
    stats_msg += f'🏥 Points de Health Boost: **{user["healthBoost"]}**\n\n'
    
    if user['lastClaim']:
        last_claim = datetime.fromisoformat(user['lastClaim'])
        now = datetime.now()
        time_diff = now - last_claim
        if time_diff < timedelta(hours=24):
            remaining = timedelta(hours=24) - time_diff
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            stats_msg += f'⏰ Prochain claim dans: **{hours}h {minutes}m**\n\n'
        else:
            stats_msg += f'✅ Claim disponible maintenant!\n\n'
    else:
        stats_msg += f'🎁 Claim disponible! Utilise `!claim`\n\n'
    
    stats_msg += f'🎃 **Réactions reçues:**\n'
    
    if user['reactions']:
        for emoji_name, count in user['reactions'].items():
            emoji_data = next((e for e in HALLOWEEN_EMOJIS if e['name'] == emoji_name), None)
            emoji_icon = emoji_data['emoji'] if emoji_data else '❓'
            stats_msg += f'{emoji_icon} {emoji_name}: {count}x\n'
    else:
        stats_msg += 'Aucune réaction pour le moment!\n'
    
    await ctx.reply(stats_msg)

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    print(f"🔥 Réaction détectée : {reaction.emoji} par {user}")

@bot.command(name="reactionselect")
@commands.has_permissions(administrator=True)
async def reactionselect(ctx, emoji: str):
    valeurs = {
        "👻": 3,
        "☠️": 7,
        "🧟": 7,
        "🔪": 12,
        "🐺": 17,
        "🎃": 31,
        "🍬": 50
    }

    if emoji not in valeurs:
        await ctx.send("❌ Réaction invalide. Choisis parmi 👻 🧟 🔪 🐺 🎃 ☠️ 🍬 ☠️")
        return

    message = await ctx.send(
        f"👀 Réagissez vite avec {emoji} ! "
        f"Le premier à le faire gagne **{valeurs[emoji]} points !** "
        f"Vous avez 60 secondes ⏱️"
    )
    await message.add_reaction(emoji)
    print(f"🕒 En attente d'une réaction {emoji} sur le message ID {message.id}")

    def check(reaction, user):
        return (
            str(reaction.emoji) == emoji
            and reaction.message.id == message.id
            and not user.bot
        )

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
        user_data_entry = get_user_data(user.id)
        user_data_entry["points"] += valeurs[emoji]
        save_data()

        print(f"✅ Réaction détectée de {user} — {valeurs[emoji]} points ajoutés")
        await ctx.send(f"🏆 {user.mention} a été le plus rapide et gagne **{valeurs[emoji]} points !** 🎉")

    except asyncio.TimeoutError:
        print("⏰ Personne n’a réagi à temps — giveaway terminé sans gagnant")
        await ctx.send("⏰ Personne n’a réagi à temps — giveaway terminé sans gagnant.")


@bot.command(name='help')
async def help_command(ctx):
    help_msg = """🎃 **BOT HALLOWEEN - AIDE** 🎃

**Fonctionnement:**
Le bot réagit automatiquement tous les 15-30 messages avec un emoji Halloween!

**Emojis et Points:**
👻 Fantôme: 4 points (40% de chance)
🧟 Zombie: 7 points (35% de chance)
💀 Crâne: 10 points (15% de chance)
🔪 Couteau: 12 points (9% de chance)
🐺 Loup: 17 points (1% de chance)
🎃 Citrouille: 31 points (0.08% de chance)
🍬 Bonbon: 50 points (0.01% de chance)

**Commandes:**
`!points` ou `!leaderboard` - Affiche le classement
`!serverreactions` - Statistiques globales du serveur
`!claim` - Réclame des points quotidiens (24h cooldown)
`!stats` - Affiche tes statistiques
`!healthboost` - Active/désactive le multiplicateur x1.5
`!help` - Affiche cette aide

**Commandes Admin:**
`!pointadd @user <points>` - Ajoute des points
`!pointremove @user <points>` - Retire des points"""
    
    await ctx.reply(help_msg)

@pointadd_command.error
@pointremove_command.error
async def admin_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply('❌ Cette commande est réservée aux administrateurs!')
    elif isinstance(error, commands.MemberNotFound):
        await ctx.reply('❌ Membre introuvable!')
    elif isinstance(error, commands.BadArgument):
        await ctx.reply('❌ Utilisation: `!pointadd @user <points>` ou `!pointremove @user <points>`')

def start_bot():
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        print('❌ ERREUR: DISCORD_TOKEN non défini dans les variables d\'environnement!')
        print('📝 Veuillez ajouter votre token Discord dans les Secrets')
        exit(1)

# --- Mini serveur Flask pour Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Discord en ligne ✅"

@app.route('/health')
def health():
    return "OK"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run(os.getenv("DISCORD_TOKEN"))    
  
    try:
        bot.run(token)
    except Exception as e:
        print(f'❌ Erreur de connexion: {e}')
        exit(1)

if __name__ == '__main__':
    start_bot()
