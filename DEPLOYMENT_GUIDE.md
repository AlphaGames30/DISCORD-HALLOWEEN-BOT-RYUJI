# 🚀 Guide de Déploiement - Halloween Discord Bot

## ✅ Ce qui a été créé

Votre bot Discord Halloween est maintenant **complet et prêt pour le déploiement** avec toutes les fonctionnalités demandées !

### 🎮 Nouvelles Commandes Discord

#### Commandes Utilisateur
- **!claim** - Réclamer des points quotidiens (cooldown 24h)
- **!serverreactions** - Voir toutes les réactions totales du serveur entier
- **!leaderboard** - Classement des joueurs
- **!stats** - Statistiques personnelles avec countdown prochain claim
- **!healthboost** - Toggle multiplicateur x1.5
- **!help** - Aide complète

#### Commandes Admin (Administrateurs uniquement)
- **!pointadd @utilisateur <points>** - Ajouter des points manuellement
- **!pointremove @utilisateur <points>** - Retirer des points manuellement

### 🌐 Interface Web Dashboard

Une magnifique interface web est accessible qui affiche :
- 📊 Statistiques en temps réel (joueurs actifs, points totaux, Health Boost)
- 🏆 Leaderboard Top 10 
- 🏥 Contrôle Health Boost (toggle x1.5)
- 📈 Réactions globales du serveur
- 🤖 Statut du bot (En ligne / Hors ligne)
- 🔄 Auto-refresh toutes les 10 secondes

## 🏃 Utilisation sur Replit

### Le bot est déjà en cours d'exécution ! 

1. **Accéder au dashboard** : Cliquez sur l'onglet "Webview" pour voir l'interface
2. **Inviter le bot sur votre serveur Discord** :
   - Allez sur https://discord.com/developers/applications
   - Sélectionnez votre application bot
   - Onglet "OAuth2" > "URL Generator"
   - Cochez : `bot`, `applications.commands`
   - Permissions : "Administrator" ou les permissions spécifiques nécessaires
   - Copiez l'URL générée et ouvrez-la dans votre navigateur
   - Sélectionnez votre serveur et autorisez le bot

3. **Tester le bot** :
   - Envoyez des messages dans votre serveur Discord
   - Le bot réagira automatiquement tous les 15-30 messages
   - Testez les commandes : `!claim`, `!serverreactions`, `!stats`, etc.

## 🚀 Déploiement sur Render

### Préparation

1. **Créer un compte sur Render** : https://render.com
2. **Push votre code sur GitHub** :
   ```bash
   git init
   git add .
   git commit -m "Halloween Discord Bot - Ready for deployment"
   git branch -M main
   git remote add origin <votre-url-github>
   git push -u origin main
   ```

### Déploiement Automatique

3. **Sur Render** :
   - Cliquez sur "New +" > "Blueprint"
   - Connectez votre repository GitHub
   - Render détectera automatiquement le fichier `render.yaml`
   - Cliquez sur "Apply"

4. **Configurer les variables d'environnement** :
   - `DISCORD_TOKEN` : Votre token Discord (déjà configuré sur Replit)
   - `SESSION_SECRET` : Sera généré automatiquement
   - `PORT` : 5000 (déjà configuré)

5. **Le déploiement démarre automatiquement !**
   - Le service web unique lance le bot ET le dashboard
   - Tout fonctionne dans le même processus
   - Les données sont partagées via `data.json`

## 🎯 Architecture Technique

### Fichiers Principaux
- **bot.py** : Bot Discord avec toutes les commandes
- **web_app.py** : API Flask et serveur web
- **main.py** : Lance bot + web simultanément
- **templates/index.html** : Interface web
- **data.json** : Base de données (auto-créé)
- **render.yaml** : Configuration Render

### Système de Données

Le fichier `data.json` stocke :
```json
{
  "_system": {
    "health_boost_active": true/false
  },
  "user_id": {
    "points": 100,
    "healthBoost": 20,
    "reactions": {"fantôme": 10, "zombie": 5},
    "lastClaim": "2024-10-28T12:00:00"
  }
}
```

### Points Clés
- ✅ Le bot et l'interface web partagent le même processus
- ✅ Health Boost synchronisé entre Discord et interface web
- ✅ Cooldown 24h pour les claims persisté dans le fichier
- ✅ Commandes admin avec vérification des permissions
- ✅ Statistiques globales du serveur en temps réel

## 🎃 Emojis et Probabilités

| Emoji | Nom | Points | Probabilité | Commande !claim |
|-------|-----|--------|-------------|-----------------|
| 👻 | Fantôme | 4 | 40% | Haute chance |
| 🧟 | Zombie | 7 | 35% | Bonne chance |
| 💀 | Crâne | 10 | 15% | Moyenne |
| 🔪 | Couteau | 12 | 9% | Faible |
| 🐺 | Loup | 17 | 1% | Rare |
| 🎃 | Citrouille | 31 | 0.09% | Ultra rare |

## 🔧 Maintenance

### Sauvegarder les données
Le fichier `data.json` est automatiquement sauvegardé après chaque action.
**Important** : Sur Render, les fichiers peuvent être perdus lors des redémarrages. 
Pour une solution permanente, envisagez d'utiliser une base de données PostgreSQL.

### Logs et Monitoring
- Sur Replit : Consultez la console
- Sur Render : Onglet "Logs" du service

### Mise à jour du code
1. Modifiez le code sur Replit ou localement
2. Commit et push sur GitHub
3. Render redéploie automatiquement

## 🎊 Fonctionnalités Bonus

### Health Boost Multiplié
Quand le Health Boost est activé (x1.5) :
- Via commande Discord `!healthboost`
- Via le bouton dans l'interface web
- Les deux sont synchronisés en temps réel !

### Claims Quotidiens
- Chaque utilisateur peut claim une fois par 24h
- Utilise le même système de probabilités que les réactions automatiques
- Le cooldown est affiché dans `!stats`

### Statistiques Complètes
- **Personnelles** : `!stats`
- **Globales** : `!serverreactions`
- **Leaderboard** : `!leaderboard`
- **Dashboard web** : Vue d'ensemble en temps réel

## 🐛 Dépannage

### Le bot ne répond pas
- Vérifiez que le workflow "Halloween Bot" est en cours d'exécution
- Vérifiez que le token Discord est valide
- Assurez-vous que les "Message Content Intent" et "Server Members Intent" sont activés

### L'interface web ne charge pas
- Vérifiez que le port 5000 est accessible
- Consultez les logs pour les erreurs Flask

### Les données ne se sauvegardent pas
- Vérifiez les permissions du fichier `data.json`
- Consultez les logs pour les erreurs de sauvegarde

## 📞 Support

Pour toute question :
1. Consultez les logs du bot (Console Replit ou Logs Render)
2. Vérifiez le fichier `README.md` pour plus de détails
3. Assurez-vous que toutes les dépendances sont installées

---

**Fait avec 🎃 pour Halloween**

**Statut** : ✅ Production Ready - Déploiement possible immédiatement !
