"""
Module pour gérer la surveillance en direct des matchs de football
avec des données réelles provenant de football.json.
"""
import random
from datetime import datetime, timedelta

def get_live_matches(all_matches):
    """
    Identifie et retourne les matchs qui sont actuellement en cours.
    
    Args:
        all_matches (list): Liste de tous les matchs disponibles
        
    Returns:
        list: Matchs actuellement en cours (simulés)
    """
    # En réalité, nous n'avons pas de données de matchs en direct en temps réel
    # Nous allons donc simuler des matchs en direct à partir des matchs récents
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_matches = [m for m in all_matches if isinstance(m, dict) and m.get('date', '') == today]
    
    # Si nous n'avons pas de matchs aujourd'hui, prendre des matchs récents et les montrer comme en direct
    if not today_matches:
        # Trier les matchs par date
        sorted_matches = sorted(
            [m for m in all_matches if isinstance(m, dict) and 'date' in m],
            key=lambda x: x.get('date', ''),
            reverse=True
        )
        
        # Prendre les 5 premiers matchs
        today_matches = sorted_matches[:5] if sorted_matches else []
    
    # Pour la simulation, nous allons transformer ces matchs en matchs en direct
    live_matches = []
    for i, match in enumerate(today_matches):
        if not isinstance(match, dict):
            continue
            
        # Dupliquer le match pour ne pas modifier l'original
        live_match = dict(match)
        
        # Ajouter des informations de match en direct
        live_match['status'] = 'En cours'
        live_match['minute'] = random.randint(1, 90)
        
        # Générer un score aléatoire réaliste
        home_score = random.randint(0, 3)
        away_score = random.randint(0, 2)
        live_match['score'] = f"{home_score}-{away_score}"
        live_match['home_score'] = home_score
        live_match['away_score'] = away_score
        
        # Générer des statistiques de match
        live_match['stats'] = {
            'possession': {
                'home': random.randint(40, 60),
                'away': 0  # Sera calculé
            },
            'shots': {
                'home': random.randint(5, 15),
                'away': random.randint(3, 12)
            },
            'shots_on_target': {
                'home': random.randint(2, 8),
                'away': random.randint(1, 6)
            },
            'corners': {
                'home': random.randint(2, 8),
                'away': random.randint(1, 7)
            },
            'fouls': {
                'home': random.randint(5, 12),
                'away': random.randint(5, 12)
            },
            'yellow_cards': {
                'home': random.randint(0, 3),
                'away': random.randint(0, 3)
            },
            'red_cards': {
                'home': 1 if random.random() < 0.1 else 0,
                'away': 1 if random.random() < 0.1 else 0
            }
        }
        
        # Calculer la possession de l'équipe extérieure
        live_match['stats']['possession']['away'] = 100 - live_match['stats']['possession']['home']
        
        # Simuler des tendances du match
        live_match['momentum'] = 'home' if random.random() < 0.6 else 'away'
        live_match['intensity'] = random.choice(['high', 'medium', 'low'])
        live_match['pressure'] = {
            'home': random.randint(1, 5),
            'away': random.randint(1, 5)
        }
        
        # Ajouter au tableau des matchs en direct
        live_matches.append(live_match)
    
    return live_matches

def get_recent_events(live_matches):
    """
    Génère des événements récents pour les matchs en direct.
    
    Args:
        live_matches (list): Liste des matchs en direct
        
    Returns:
        list: Événements récents survenus dans les matchs
    """
    event_types = [
        {"type": "shot", "description": "Tir", "probability": 0.3},
        {"type": "goal", "description": "BUT!", "probability": 0.1},
        {"type": "corner", "description": "Corner", "probability": 0.2},
        {"type": "foul", "description": "Faute", "probability": 0.25},
        {"type": "yellow_card", "description": "Carton jaune", "probability": 0.15},
        {"type": "red_card", "description": "Carton rouge", "probability": 0.02},
        {"type": "shot_on_target", "description": "Tir cadré", "probability": 0.2},
        {"type": "substitution", "description": "Remplacement", "probability": 0.15},
        {"type": "offside", "description": "Hors-jeu", "probability": 0.18},
        {"type": "free_kick", "description": "Coup franc", "probability": 0.22},
        {"type": "penalty", "description": "Penalty", "probability": 0.05},
    ]
    
    recent_events = []
    
    for match in live_matches:
        if not isinstance(match, dict):
            continue
            
        # Générer 3 à 8 événements par match
        num_events = random.randint(3, 8)
        
        for _ in range(num_events):
            # Sélectionner un type d'événement basé sur sa probabilité
            event = random.choices(
                event_types, 
                weights=[e["probability"] for e in event_types], 
                k=1
            )[0]
            
            # Déterminer quelle équipe est concernée
            team_side = random.choice(["home", "away"])
            team_name = match.get('home_team' if team_side == "home" else 'away_team', 
                                 match.get('home' if team_side == "home" else 'away', '?'))
            
            # Déterminer la minute de l'événement
            minute = random.randint(1, match.get('minute', 45))
            
            # Générer un joueur fictif
            player_number = random.randint(1, 11)
            player_name = f"Joueur #{player_number}"
            
            # Construire la description de l'événement
            description = f"{event['description']} - {team_name} ({minute}')"
            if event['type'] not in ['corner', 'offside']:
                description += f" - {player_name}"
            
            # Ajouter des détails spécifiques à certains événements
            if event['type'] == 'goal':
                description = f"⚽ BUT! - {team_name} ({minute}') - {player_name}"
                # Mettre à jour le score du match
                if team_side == "home":
                    match['home_score'] = match.get('home_score', 0) + 1
                else:
                    match['away_score'] = match.get('away_score', 0) + 1
                match['score'] = f"{match.get('home_score', 0)}-{match.get('away_score', 0)}"
            elif event['type'] == 'yellow_card':
                description = f"🟨 Carton jaune - {team_name} ({minute}') - {player_name}"
            elif event['type'] == 'red_card':
                description = f"🟥 Carton rouge - {team_name} ({minute}') - {player_name}"
            elif event['type'] == 'penalty':
                description = f"⚠️ Penalty pour {team_name} ({minute}') - {player_name}"
            
            # Calculer un timestamp pour l'événement
            event_time = datetime.now() - timedelta(seconds=random.randint(10, 600))
            
            # Ajouter l'événement à la liste
            recent_events.append({
                'match': f"{match.get('home_team', match.get('home', '?'))} vs {match.get('away_team', match.get('away', '?'))}",
                'match_id': id(match),  # Utiliser l'ID de l'objet comme identifiant unique
                'type': event['type'],
                'description': description,
                'minute': minute,
                'team_side': team_side,
                'team_name': team_name,
                'player_name': player_name,
                'timestamp': event_time.strftime("%H:%M:%S")
            })
    
    # Trier les événements par timestamp
    recent_events.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return recent_events

def get_arcan_sentinel_activities(live_matches, events):
    """
    Génère des activités d'ArcanSentinel basées sur les matchs en direct.
    
    Args:
        live_matches (list): Liste des matchs en direct
        events (list): Liste des événements récents
        
    Returns:
        list: Activités d'ArcanSentinel
    """
    # Types d'activités que peut détecter ArcanSentinel
    activity_types = [
        "Momentum shift détecté",
        "Séquence de jeu intense détectée",
        "Changement tactique identifié",
        "Blessure potentielle détectée",
        "Pression défensive accrue",
        "Opportunité de but imminente",
        "Fatigue critique détectée",
        "Adaptation tactique recommandée",
        "Déséquilibre formation adverse",
        "Sur-engagement offensif identifié"
    ]
    
    # Simuler des activités détectées par ArcanSentinel
    activities = []
    
    for match in live_matches:
        if not isinstance(match, dict):
            continue
            
        # Générer 2 à 4 activités par match
        num_activities = random.randint(2, 4)
        
        for _ in range(num_activities):
            # Choisir un type d'activité
            activity_type = random.choice(activity_types)
            
            # Déterminer quelle équipe est concernée
            team_side = random.choice(["home", "away"])
            team_name = match.get('home_team' if team_side == "home" else 'away_team', 
                                 match.get('home' if team_side == "home" else 'away', '?'))
            
            # Générer des détails spécifiques à certains types d'activités
            details = ""
            impact = random.choice(["high", "medium", "low"])
            
            if "Momentum shift" in activity_type:
                percentage = random.randint(15, 40)
                details = f"{activity_type} pour {team_name} (+{percentage}%)"
            elif "tactique" in activity_type:
                formations = ["4-3-3", "4-4-2", "3-5-2", "4-2-3-1", "5-3-2"]
                old_formation = random.choice(formations)
                new_formation = random.choice([f for f in formations if f != old_formation])
                details = f"{activity_type}: {team_name} {old_formation} → {new_formation}"
            elif "Blessure" in activity_type:
                player_number = random.randint(1, 11)
                details = f"{activity_type}: joueur #{player_number} de {team_name}"
            elif "Pression" in activity_type:
                percentage = random.randint(20, 50)
                details = f"{activity_type} de {team_name} (+{percentage}% d'intensité)"
            elif "Opportunité" in activity_type:
                probability = random.randint(60, 90)
                details = f"{activity_type} pour {team_name} ({probability}% probabilité)"
            elif "Fatigue" in activity_type:
                player_number = random.randint(1, 11)
                percentage = random.randint(75, 95)
                details = f"{activity_type}: joueur #{player_number} de {team_name} ({percentage}%)"
            elif "Adaptation" in activity_type:
                tactic = random.choice(["pressing haut", "bloc bas", "jeu direct", "possession"])
                details = f"{activity_type} pour {team_name}: {tactic}"
            elif "Déséquilibre" in activity_type:
                zone = random.choice(["axe central", "côté gauche", "côté droit"])
                details = f"{activity_type} sur {zone} chez {team_name}"
            elif "Sur-engagement" in activity_type:
                risk = random.randint(60, 90)
                details = f"{activity_type} chez {team_name} (risque contre-attaque {risk}%)"
            else:
                details = f"{activity_type} dans le match de {team_name}"
            
            # Calculer un timestamp pour l'activité
            activity_time = datetime.now() - timedelta(seconds=random.randint(10, 300))
            
            # Ajouter l'activité à la liste
            activities.append({
                'time': activity_time.strftime("%H:%M:%S"),
                'match': f"{match.get('home_team', match.get('home', '?'))} vs {match.get('away_team', match.get('away', '?'))}",
                'event': details,
                'impact': impact
            })
    
    # Trier les activités par timestamp
    activities.sort(key=lambda x: x['time'], reverse=True)
    
    return activities

def get_sentinel_metrics():
    """
    Génère des métriques pour ArcanSentinel.
    
    Returns:
        dict: Métriques d'ArcanSentinel
    """
    return {
        'matchs_analysés': random.randint(15, 40),
        'anomalies_détectées': random.randint(5, 15),
        'précision_alertes': round(random.uniform(88, 96), 1),
        'temps_réponse': round(random.uniform(1.0, 1.8), 1)
    }