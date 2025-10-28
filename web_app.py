from flask import Flask, render_template, jsonify, request
import json
import os
from pathlib import Path
from threading import Thread
import importlib.util

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET', 'halloween-secret-key-2024')

DATA_FILE = Path(__file__).parent / 'data.json'

def load_user_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict) and '_system' in data:
                return {k: v for k, v in data.items() if k != '_system'}
            return data
    except FileNotFoundError:
        return {}

def load_system_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict) and '_system' in data:
                return data['_system']
            return {}
    except FileNotFoundError:
        return {}

def save_system_data(system_data):
    try:
        user_data = load_user_data()
        data_to_save = {'_system': system_data}
        data_to_save.update(user_data)
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f'❌ Erreur lors de la sauvegarde: {e}')

def get_bot_module():
    try:
        spec = importlib.util.spec_from_file_location("bot", "bot.py")
        bot_module = importlib.util.module_from_spec(spec)
        return bot_module
    except:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/leaderboard')
def api_leaderboard():
    user_data = load_user_data()
    
    if not user_data:
        return jsonify([])
    
    sorted_users = sorted(
        [(user_id, data) for user_id, data in user_data.items()],
        key=lambda x: x[1]['points'],
        reverse=True
    )[:10]
    
    leaderboard = []
    for i, (user_id, data) in enumerate(sorted_users):
        leaderboard.append({
            'rank': i + 1,
            'user_id': user_id,
            'points': data['points'],
            'healthBoost': data.get('healthBoost', 0),
            'reactions': data.get('reactions', {})
        })
    
    return jsonify(leaderboard)

@app.route('/api/stats')
def api_stats():
    user_data = load_user_data()
    
    total_reactions = {}
    total_points = 0
    total_users = len(user_data)
    total_health_boost = 0
    
    for user_id, data in user_data.items():
        total_points += data['points']
        total_health_boost += data.get('healthBoost', 0)
        for emoji_name, count in data.get('reactions', {}).items():
            if emoji_name not in total_reactions:
                total_reactions[emoji_name] = 0
            total_reactions[emoji_name] += count
    
    return jsonify({
        'total_users': total_users,
        'total_points': total_points,
        'total_health_boost': total_health_boost,
        'total_reactions': total_reactions
    })

@app.route('/api/healthboost/status')
def api_healthboost_status():
    system_data = load_system_data()
    status = system_data.get('health_boost_active', False)
    return jsonify({'active': status})

@app.route('/api/healthboost/toggle', methods=['POST'])
def api_healthboost_toggle():
    try:
        system_data = load_system_data()
        current_status = system_data.get('health_boost_active', False)
        new_status = not current_status
        
        system_data['health_boost_active'] = new_status
        save_system_data(system_data)
        
        return jsonify({
            'success': True,
            'active': new_status,
            'message': f'Health Boost {"activé" if new_status else "désactivé"}!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur: {str(e)}'
        }), 500

@app.route('/api/bot/status')
def api_bot_status():
    try:
        import bot as bot_instance
        is_ready = bot_instance.bot.is_ready() if hasattr(bot_instance, 'bot') else False
        return jsonify({
            'online': is_ready,
            'status': 'En ligne' if is_ready else 'Hors ligne'
        })
    except:
        return jsonify({
            'online': False,
            'status': 'Hors ligne'
        })

def run_flask():
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    run_flask()
