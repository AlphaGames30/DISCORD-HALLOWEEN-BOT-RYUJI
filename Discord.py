import discord
import json
import os

intents = discord.Intents.default()
intents.reactions = True
intents.messages = True
client = discord.Client(intents=intents)

POINTS_FILE = "points.json"

# --- Charger les points au démarrage ---
if os.path.exists(POINTS_FILE):
    with open(POINTS_FILE, "r") as f:
        user_points = json.load(f)
else:
    user_points = {}

def save_points():
    """Sauvegarde les points dans le fichier JSON"""
    with open(POINTS_FILE, "w") as f:
        json.dump(user_points, f, indent=4)

@client.event
async def on_ready():
    print(f"✅ Connecté en tant que {client.user}")

@client.event
async def on_reaction_add(reaction, user):
    """Quand quelqu'un réagit à un message"""
    if user.bot:
        return  # on ignore les bots

    user_id = str(user.id)
    user_points[user_id] = user_points.get(user_id, 0) + 1
    save_points()
    print(f"{user} a maintenant {user_points[user_id]} points")

@client.event
async def on_message(message):
    """Commande pour voir ses points"""
    if message.content.startswith("!points"):
        user_id = str(message.author.id)
        points = user_points.get(user_id, 0)
        await message.channel.send(f"Tu as **{points} points** 🎯")

@client.event
async def on_disconnect():
    """Sauvegarde automatique avant déconnexion"""
    save_points()
    print("💾 Points sauvegardés avant la déconnexion")

client.run("DISCORD_TOKEN")
