# 🎃 Halloween Discord Bot

Un bot Discord interactif pour Halloween avec système de points, réactions automatiques et interface web de monitoring.

## 🌟 Fonctionnalités

### Bot Discord
- **Réactions automatiques**: Le bot réagit tous les 15-30 messages avec des emojis Halloween
- **Système de points**: Gagnez des points basés sur la rareté des emojis
- **Claim quotidien**: Réclamez des points chaque jour avec la commande `!claim`
- **Statistiques globales**: Visualisez les stats du serveur entier avec `!serverreactions`
- **Commandes admin**: Ajoutez ou retirez des points manuellement
- **Health Boost**: Multiplicateur x1.5 pour tous les points

### Interface Web
- **Dashboard en temps réel**: Visualisez les statistiques en direct
- **Leaderboard Top 10**: Classement des meilleurs joueurs
- **Contrôle Health Boost**: Activez/désactivez le multiplicateur depuis le web
- **Statistiques serveur**: Vue d'ensemble de toutes les réactions

## 🎮 Commandes Discord

### Commandes Utilisateur
- `!claim` - Réclame des points quotidiens (cooldown 24h)
- `!points` ou `!leaderboard` - Affiche le classement
- `!serverreactions` - Statistiques globales du serveur
- `!stats` - Affiche tes statistiques personnelles
- `!healthboost` - Active/désactive le multiplicateur x1.5
- `!help` - Affiche l'aide

### Commandes Admin
- `!pointadd @user <points>` - Ajoute des points à un utilisateur
- `!pointremove @user <points>` - Retire des points à un utilisateur

## 🎯 Emojis et Probabilités

| Emoji | Nom | Points | Probabilité |
|-------|-----|--------|-------------|
| 👻 | Fantôme | 4 | 40% |
| 🧟 | Zombie | 7 | 35% |
| 💀 | Crâne | 10 | 15% |
| 🔪 | Couteau | 12 | 9% |
| 🐺 | Loup | 17 | 1% |
| 🎃 | Citrouille | 31 | 0.09% |

## 🚀 Installation Locale (Replit)

1. **Ajoutez votre token Discord**:
   - Cliquez sur l'icône 🔒 (Secrets)
   - Ajoutez: `DISCORD_TOKEN` = votre token

2. **Lancez le bot**:
   - Cliquez sur "Run"
   - Le bot et l'interface web démarreront automatiquement

3. **Accédez au dashboard**:
   - Ouvrez l'interface web depuis le webview Replit

## 📦 Déploiement sur Render

### Méthode automatique avec render.yaml

1. **Push sur GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <votre-repo>
   git push -u origin main
   ```

2. **Connectez à Render**:
   - Allez sur [render.com](https://render.com)
   - Créez un nouveau "Blueprint"
   - Connectez votre repo GitHub
   - Render détectera automatiquement `render.yaml`

3. **Configurez les variables**:
   - Ajoutez `DISCORD_TOKEN` dans les variables d'environnement

Le fichier `render.yaml` configure automatiquement:
- ✅ Un service web unique qui exécute le bot Discord ET le dashboard
- ✅ Partage de données entre le bot et l'interface web
- ✅ Toutes les variables d'environnement nécessaires

**Note**: Le bot et l'interface web tournent dans le même processus sur Render (via `main.py`) pour partager l'état et les données en temps réel.

## 📁 Structure du Projet

```
.
├── bot.py                  # Bot Discord principal
├── web_app.py             # Interface web Flask
├── main.py                # Lanceur combiné (bot + web)
├── templates/
│   └── index.html         # Dashboard HTML
├── requirements.txt       # Dépendances Python
├── render.yaml           # Configuration Render
├── data.json             # Données des utilisateurs (auto-généré)
└── README.md             # Ce fichier
```

## 🔧 Configuration

### Variables d'Environnement

| Variable | Description | Obligatoire |
|----------|-------------|-------------|
| `DISCORD_TOKEN` | Token du bot Discord | ✅ Oui |
| `SESSION_SECRET` | Clé secrète Flask | ❌ Non (auto-généré) |
| `PORT` | Port du serveur web | ❌ Non (5000 par défaut) |

## 🛠️ Développement

### Fichiers modifiables

- **bot.py**: Logique du bot, commandes, événements
- **web_app.py**: API et routes Flask
- **templates/index.html**: Interface utilisateur

### Ajouter une nouvelle commande

```python
@bot.command(name='macommande')
async def ma_commande(ctx):
    await ctx.reply('Réponse de ma commande!')
```

## 📊 Données

Les données sont stockées dans `data.json`:
```json
{
  "user_id": {
    "points": 100,
    "healthBoost": 20,
    "reactions": {
      "fantôme": 10,
      "zombie": 5
    },
    "lastClaim": "2024-10-28T12:00:00"
  }
}
```

## 🐛 Dépannage

### Le bot ne démarre pas
- Vérifiez que `DISCORD_TOKEN` est défini
- Vérifiez les permissions du bot Discord (Members Intent, Message Content Intent)

### L'interface web ne s'affiche pas
- Vérifiez que le port 5000 est disponible
- Vérifiez les logs dans la console

### Les données ne se sauvegardent pas
- Vérifiez les permissions d'écriture du fichier `data.json`
- Consultez les logs pour les erreurs de sauvegarde

## 📝 Licence

Projet libre d'utilisation pour des fins personnelles et éducatives.

## 👥 Support

Pour toute question ou problème:
1. Consultez les logs du bot
2. Vérifiez que toutes les dépendances sont installées
3. Assurez-vous que le token Discord est valide

---

Fait avec 🎃 pour Halloween
