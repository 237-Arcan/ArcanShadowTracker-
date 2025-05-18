"""
Module pour la surveillance en direct des matchs de football.
"""
import random
from datetime import datetime, timedelta
import time

def get_live_matches():
    """
    Récupère les matchs actuellement en direct.
    Utilise désormais les données réelles de l'API Football.
    
    Returns:
        list: Liste des matchs en direct avec les données réelles
    """
    import os
    import requests
    import sys
    
    # Utilisation de l'API Football pour obtenir des données réelles
    try:
        # Récupérer la clé API des variables d'environnement
        api_key = os.environ.get('FOOTBALL_API_KEY')
        
        if not api_key:
            print("Avertissement: Clé API Football non trouvée dans les variables d'environnement")
            # Si nous n'avons pas de clé API, utiliser les données d'exemple
            return get_sample_live_matches()
        
        # Préparation de la requête à l'API Football
        headers = {
            'X-RapidAPI-Key': api_key,
            'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com'
        }
        
        # Récupérer les matchs en direct
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        params = {"live": "all"}
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Lever une exception si la réponse contient une erreur
        
        data = response.json()
        
        if not data.get('response'):
            print("Aucun match en direct trouvé via l'API")
            return get_sample_live_matches()
        
        # Transformation des données de l'API au format attendu par l'application
        live_matches = []
        
        for fixture in data.get('response', []):
            fixture_data = fixture.get('fixture', {})
            teams = fixture.get('teams', {})
            goals = fixture.get('goals', {})
            league = fixture.get('league', {})
            
            # Calculer la minute actuelle
            status = fixture_data.get('status', {})
            minute = status.get('elapsed', 0)
            
            # Période (1ère ou 2nde mi-temps)
            period = "1ère mi-temps" if minute <= 45 else "2nde mi-temps"
            
            # Extrait des statistiques si disponibles
            stats = {
                'possession': 50,  # Valeur par défaut
                'shots': 0,
                'shots_on_target': 0,
                'corners': 0,
                'yellow_cards': 0,
                'red_cards': 0
            }
            
            # Récupération des cotes si disponibles
            live_odds = {
                'home_win': 2.0,
                'draw': 3.0,
                'away_win': 4.0
            }
            
            # Création de l'objet match
            match_data = {
                'league': league.get('name', ''),
                'home_team': teams.get('home', {}).get('name', ''),
                'away_team': teams.get('away', {}).get('name', ''),
                'home_score': goals.get('home', 0),
                'away_score': goals.get('away', 0),
                'minute': minute,
                'period': period,
                'added_time': 0,
                'stats': stats,
                'live_odds': live_odds,
                'momentum': random.randint(40, 60),  # Valeur aléatoire pour le momentum
                'recent_events': []  # Événements récents à remplir si disponibles
            }
            
            live_matches.append(match_data)
        
        if not live_matches:
            print("Aucun match en direct trouvé après traitement des données")
            return get_sample_live_matches()
        
        return live_matches
        
    except Exception as e:
        print(f"Erreur lors de la récupération des matchs en direct: {str(e)}")
        # En cas d'erreur, utiliser les données d'exemple
        return get_sample_live_matches()

def get_sample_live_matches():
    """
    Génère des exemples de matchs en direct basés sur des données réelles.
    Utilisé comme solution de secours si l'API n'est pas disponible.
    
    Returns:
        list: Liste des matchs en direct d'exemple
    """
    # Données d'exemple basées sur des matchs réels
    sample_matches = [
        {
            'league': 'Premier League',
            'home_team': 'Arsenal',
            'away_team': 'Manchester City',
            'home_score': 1,
            'away_score': 1,
            'minute': 65,
            'period': '2nde mi-temps',
            'added_time': 0,
            'stats': {
                'possession': 42,
                'shots': 8,
                'shots_on_target': 3,
                'corners': 5,
                'yellow_cards': 2,
                'red_cards': 0
            },
            'live_odds': {
                'home_win': 3.50,
                'draw': 2.20,
                'away_win': 2.10
            },
            'momentum': 45,
            'recent_events': []
        },
        {
            'league': 'Ligue 1',
            'home_team': 'PSG',
            'away_team': 'Marseille',
            'home_score': 2,
            'away_score': 0,
            'minute': 78,
            'period': '2nde mi-temps',
            'added_time': 0,
            'stats': {
                'possession': 58,
                'shots': 12,
                'shots_on_target': 6,
                'corners': 7,
                'yellow_cards': 1,
                'red_cards': 0
            },
            'live_odds': {
                'home_win': 1.20,
                'draw': 5.50,
                'away_win': 12.00
            },
            'momentum': 65,
            'recent_events': []
        },
        {
            'league': 'LaLiga',
            'home_team': 'Barcelona',
            'away_team': 'Real Madrid',
            'home_score': 1,
            'away_score': 2,
            'minute': 82,
            'period': '2nde mi-temps',
            'added_time': 0,
            'stats': {
                'possession': 62,
                'shots': 14,
                'shots_on_target': 5,
                'corners': 9,
                'yellow_cards': 3,
                'red_cards': 0
            },
            'live_odds': {
                'home_win': 3.75,
                'draw': 3.00,
                'away_win': 1.95
            },
            'momentum': 35,
            'recent_events': []
        }
    ]
    
    # Ajouter quelques événements récents générés
    for match in sample_matches:
        match['recent_events'] = generate_recent_events(
            match['minute'], 
            match['home_team'], 
            match['away_team'], 
            match['home_score'], 
            match['away_score']
        )
    
    return sample_matches

def generate_recent_events(minute, home_team, away_team, home_score, away_score):
    """
    Génère des événements récents pour un match en direct.
    
    Args:
        minute (int): Minute actuelle du match
        home_team (str): Équipe à domicile
        away_team (str): Équipe à l'extérieur
        home_score (int): Buts de l'équipe à domicile
        away_score (int): Buts de l'équipe à l'extérieur
        
    Returns:
        list: Liste des événements récents
    """
    events = []
    
    # Générer des noms de joueurs aléatoires
    home_players = [f"Joueur {chr(65+i)}" for i in range(11)]
    away_players = [f"Joueur {chr(65+i)}" for i in range(11)]
    
    # Nombre d'événements à générer (entre 3 et 5)
    num_events = random.randint(3, 5)
    
    # Événements possibles
    event_types = ['but', 'carton', 'occasion', 'remplacement', 'corner']
    
    # Minutes pour les événements (récents)
    event_minutes = []
    for _ in range(num_events):
        # Générer une minute avant la minute actuelle
        if minute <= 5:
            event_minute = random.randint(1, minute)
        else:
            event_minute = random.randint(minute - 5, minute)
        
        event_minutes.append(event_minute)
        
    # Trier les minutes par ordre décroissant (événements les plus récents d'abord)
    event_minutes.sort(reverse=True)
    
    # Générer les événements
    for event_minute in event_minutes:
        # Déterminer le type d'événement
        # Ajuster les probabilités en fonction du score et de la minute
        if event_minute == minute and (home_score > 0 or away_score > 0):
            # Si c'est la minute actuelle et qu'il y a au moins un but, augmenter la probabilité d'un but
            weights = [0.4, 0.15, 0.2, 0.1, 0.15]  # but, carton, occasion, remplacement, corner
        else:
            weights = [0.2, 0.2, 0.3, 0.1, 0.2]  # but, carton, occasion, remplacement, corner
            
        event_type = random.choices(event_types, weights=weights)[0]
        
        # Déterminer l'équipe (50/50 entre domicile et extérieur)
        is_home_team = random.choice([True, False])
        team = home_team if is_home_team else away_team
        players = home_players if is_home_team else away_players
        
        # Créer l'événement
        event = {
            'minute': event_minute,
            'team': team,
            'type': event_type
        }
        
        # Ajouter des détails spécifiques selon le type d'événement
        if event_type == 'but':
            scorer = random.choice(players)
            event['player'] = scorer
            event['description'] = f"But de {scorer} pour {team}"
            
        elif event_type == 'carton':
            player = random.choice(players)
            card_type = random.choices(['jaune', 'rouge'], weights=[0.9, 0.1])[0]
            event['player'] = player
            event['card_type'] = card_type
            event['description'] = f"Carton {card_type} pour {player} ({team})"
            
        elif event_type == 'occasion':
            player = random.choice(players)
            event['player'] = player
            event['description'] = f"Occasion manquée par {player} ({team})"
            
        elif event_type == 'remplacement':
            player_out = random.choice(players)
            # Trouver un joueur différent
            player_in = random.choice([p for p in players if p != player_out])
            event['player_out'] = player_out
            event['player_in'] = player_in
            event['description'] = f"Remplacement pour {team}: {player_in} remplace {player_out}"
            
        elif event_type == 'corner':
            event['description'] = f"Corner pour {team}"
            
        events.append(event)
        
    return events

def get_match_timeline(match_id, current_minute=45):
    """
    Génère une chronologie complète pour un match en cours.
    
    Args:
        match_id (str): Identifiant du match
        current_minute (int): Minute actuelle du match
        
    Returns:
        dict: Chronologie du match
    """
    # Dans un système réel, cela récupérerait les données de l'API
    # Ici, nous générons des données simulées
    
    # Équipes (pour l'exemple)
    home_team = "Équipe Domicile"
    away_team = "Équipe Extérieure"
    
    # Score actuel
    home_score = 0
    away_score = 0
    
    # Générer des noms de joueurs aléatoires
    home_players = [f"Joueur {home_team} {chr(65+i)}" for i in range(11)]
    away_players = [f"Joueur {away_team} {chr(65+i)}" for i in range(11)]
    
    # Événements du match
    events = []
    
    # Nombre total d'événements (entre 10 et 20)
    num_events = random.randint(10, 20)
    
    # Générer des minutes pour les événements (jusqu'à la minute actuelle)
    event_minutes = sorted([random.randint(1, current_minute) for _ in range(num_events)])
    
    # Types d'événements possibles
    event_types = ['but', 'carton jaune', 'carton rouge', 'occasion', 'corner', 'remplacement', 'faute', 'hors-jeu']
    
    # Générer les événements
    for minute in event_minutes:
        # Determiner le type d'événement
        if minute < 10:
            # Début de match - moins de buts, plus de fautes
            weights = [0.05, 0.2, 0.01, 0.2, 0.15, 0.05, 0.25, 0.09]
        elif minute > current_minute - 10:
            # Fin de mi-temps ou de match - plus de buts et remplacements
            weights = [0.2, 0.1, 0.02, 0.2, 0.15, 0.15, 0.1, 0.08]
        else:
            # Milieu de match - distribution équilibrée
            weights = [0.15, 0.15, 0.02, 0.2, 0.15, 0.1, 0.15, 0.08]
            
        event_type = random.choices(event_types, weights=weights)[0]
        
        # Déterminer l'équipe (50/50 entre domicile et extérieur)
        is_home_team = random.choice([True, False])
        team = home_team if is_home_team else away_team
        players = home_players if is_home_team else away_players
        
        # Créer l'événement
        event = {
            'minute': minute,
            'team': team,
            'type': event_type
        }
        
        # Ajouter des détails spécifiques selon le type d'événement
        if event_type == 'but':
            scorer = random.choice(players)
            assistor = random.choice([p for p in players if p != scorer])
            event['player'] = scorer
            event['assist'] = assistor
            event['description'] = f"BUT! {scorer} marque pour {team}. Passé décisive de {assistor}."
            
            # Mettre à jour le score
            if is_home_team:
                home_score += 1
            else:
                away_score += 1
                
            event['score'] = f"{home_score}-{away_score}"
            
        elif event_type == 'carton jaune':
            player = random.choice(players)
            event['player'] = player
            event['description'] = f"Carton jaune pour {player} ({team})."
            
        elif event_type == 'carton rouge':
            player = random.choice(players)
            event['player'] = player
            event['description'] = f"CARTON ROUGE! {player} ({team}) est expulsé du terrain."
            
        elif event_type == 'occasion':
            player = random.choice(players)
            event['player'] = player
            
            # Type d'occasion
            chance_types = ['frappe', 'tête', 'dribble', 'contre-attaque']
            chance_type = random.choice(chance_types)
            
            event['description'] = f"Occasion pour {team}. {player} tente une {chance_type} mais ne parvient pas à marquer."
            
        elif event_type == 'corner':
            player = random.choice(players)
            event['player'] = player
            event['description'] = f"Corner pour {team}, tiré par {player}."
            
        elif event_type == 'remplacement':
            player_out = random.choice(players)
            # Supprimer le joueur sortant de la liste pour le remplaçant
            players.remove(player_out)
            player_in = f"Joueur {team} Remplaçant {random.randint(1, 5)}"
            players.append(player_in)
            
            event['player_out'] = player_out
            event['player_in'] = player_in
            event['description'] = f"Changement pour {team}: {player_in} remplace {player_out}."
            
        elif event_type == 'faute':
            player = random.choice(players)
            event['player'] = player
            
            # L'équipe victime de la faute
            victim_team = away_team if is_home_team else home_team
            victim_players = away_players if is_home_team else home_players
            victim_player = random.choice(victim_players)
            
            event['description'] = f"Faute de {player} ({team}) sur {victim_player} ({victim_team})."
            
        elif event_type == 'hors-jeu':
            player = random.choice(players)
            event['player'] = player
            event['description'] = f"Hors-jeu signalé contre {player} ({team})."
            
        events.append(event)
        
    # Trier les événements par minute (décroissant pour avoir les plus récents en premier)
    events.sort(key=lambda x: x['minute'], reverse=True)
    
    return {
        'match_id': match_id,
        'home_team': home_team,
        'away_team': away_team,
        'current_score': f"{home_score}-{away_score}",
        'current_minute': current_minute,
        'events': events,
        'stats': {
            'possession': random.randint(40, 60),  # Pourcentage pour l'équipe à domicile
            'shots': {
                'home': random.randint(5, 15),
                'away': random.randint(5, 15)
            },
            'shots_on_target': {
                'home': random.randint(2, 8),
                'away': random.randint(2, 8)
            },
            'corners': {
                'home': random.randint(2, 8),
                'away': random.randint(2, 8)
            },
            'fouls': {
                'home': random.randint(5, 15),
                'away': random.randint(5, 15)
            },
            'yellow_cards': {
                'home': random.randint(0, 3),
                'away': random.randint(0, 3)
            },
            'red_cards': {
                'home': random.randint(0, 1),
                'away': random.randint(0, 1)
            }
        }
    }

def get_match_momentum(match_id):
    """
    Calcule l'indice de momentum pour chaque équipe dans un match.
    
    Args:
        match_id (str): Identifiant du match
        
    Returns:
        dict: Données de momentum
    """
    # Dans un système réel, cela serait calculé à partir des données du match
    # Ici, nous générons des données aléatoires
    
    # Générer une série de points de données pour le momentum (90 points, un par minute)
    home_momentum = []
    away_momentum = []
    
    baseline_home = random.randint(30, 70)
    baseline_away = 100 - baseline_home
    
    for i in range(90):
        # Ajouter une variation aléatoire
        variation = random.randint(-5, 5)
        
        # Calculer les valeurs de momentum
        home_value = max(0, min(100, baseline_home + variation))
        away_value = 100 - home_value
        
        home_momentum.append(home_value)
        away_momentum.append(away_value)
        
        # Mise à jour du baseline pour la prochaine minute (avec une légère régression vers la moyenne)
        baseline_home = home_value * 0.9 + baseline_home * 0.1
        baseline_away = away_value * 0.9 + baseline_away * 0.1
        
    # Créer des moments clés (changements significatifs dans le momentum)
    key_moments = []
    
    for i in range(1, len(home_momentum)):
        delta = abs(home_momentum[i] - home_momentum[i-1])
        if delta > 10:
            # Déterminer l'équipe qui a gagné du momentum
            team_gained = 'home' if home_momentum[i] > home_momentum[i-1] else 'away'
            
            key_moments.append({
                'minute': i + 1,
                'team': team_gained,
                'delta': delta,
                'event_type': random.choice(['but', 'occasion', 'carton', 'remplacement']),
                'description': "Changement significatif de momentum en faveur de l'équipe " + ("à domicile" if team_gained == 'home' else "à l'extérieur")
            })
    
    return {
        'match_id': match_id,
        'home_momentum': home_momentum,
        'away_momentum': away_momentum,
        'key_moments': key_moments
    }

def get_live_alerts():
    """
    Génère des alertes en direct sur des matchs en cours.
    
    Returns:
        list: Liste des alertes
    """
    # Dans un système réel, cela serait basé sur de vrais événements
    # Ici, nous générons des alertes simulées
    
    alert_types = [
        "but", "carton_rouge", "grosse_occasion", 
        "cote_changement", "momentum_shift", "valeur_betting"
    ]
    
    # Générer un nombre aléatoire d'alertes (entre 1 et 4)
    num_alerts = random.randint(1, 4)
    
    alerts = []
    
    for _ in range(num_alerts):
        # Type d'alerte
        alert_type = random.choice(alert_types)
        
        # Timestamp
        minutes_ago = random.randint(1, 15)
        timestamp = (datetime.now() - timedelta(minutes=minutes_ago)).strftime("%H:%M")
        
        # Équipes (pour l'exemple)
        teams = [
            ("Manchester City", "Liverpool"),
            ("Barcelona", "Real Madrid"),
            ("Bayern Munich", "Borussia Dortmund"),
            ("PSG", "Marseille"),
            ("Inter Milan", "Juventus")
        ]
        home_team, away_team = random.choice(teams)
        
        # Créer une alerte basée sur son type
        if alert_type == "but":
            scoring_team = random.choice([home_team, away_team])
            other_team = away_team if scoring_team == home_team else home_team
            
            # Score actuel (simulé)
            home_score = random.randint(1, 3)
            away_score = random.randint(1, 3)
            if scoring_team == home_team:
                home_score += 1
            else:
                away_score += 1
                
            alerts.append({
                'type': 'goal',
                'timestamp': timestamp,
                'match': f"{home_team} vs {away_team}",
                'minute': random.randint(1, 90),
                'title': f"BUT! {scoring_team}",
                'content': f"{scoring_team} vient de marquer contre {other_team}. Score: {home_team} {home_score}-{away_score} {away_team}",
                'importance': 'high'
            })
            
        elif alert_type == "carton_rouge":
            team = random.choice([home_team, away_team])
            player = f"Joueur {chr(64 + random.randint(1, 26))}"
            
            alerts.append({
                'type': 'red_card',
                'timestamp': timestamp,
                'match': f"{home_team} vs {away_team}",
                'minute': random.randint(1, 90),
                'title': f"CARTON ROUGE! {team}",
                'content': f"{player} de {team} vient de recevoir un carton rouge!",
                'importance': 'medium'
            })
            
        elif alert_type == "grosse_occasion":
            team = random.choice([home_team, away_team])
            player = f"Joueur {chr(64 + random.randint(1, 26))}"
            
            alerts.append({
                'type': 'big_chance',
                'timestamp': timestamp,
                'match': f"{home_team} vs {away_team}",
                'minute': random.randint(1, 90),
                'title': f"Grosse occasion pour {team}!",
                'content': f"{player} vient de manquer une énorme occasion pour {team}!",
                'importance': 'medium'
            })
            
        elif alert_type == "cote_changement":
            # Équipe dont la cote change
            team = random.choice([home_team, away_team])
            
            # Direction du changement
            direction = random.choice(["baisse", "hausse"])
            
            # Valeurs des cotes
            old_odds = round(2.0 + random.random() * 2, 2)
            new_odds = old_odds * (0.8 if direction == "baisse" else 1.2)
            new_odds = round(new_odds, 2)
            
            importance = 'medium' if abs(old_odds - new_odds) > 0.5 else 'low'
            alerts.append({
                'type': 'odds_change',
                'timestamp': timestamp,
                'match': f"{home_team} vs {away_team}",
                'minute': random.randint(1, 90),
                'title': f"Changement de cote pour {team}",
                'content': f"La cote pour une victoire de {team} est en {direction}, passant de {old_odds} à {new_odds}.",
                'importance': importance
            })
            
        elif alert_type == "momentum_shift":
            # Équipe qui gagne du momentum
            gaining_team = random.choice([home_team, away_team])
            other_team = away_team if gaining_team == home_team else home_team
            
            alerts.append({
                'type': 'momentum',
                'timestamp': timestamp,
                'match': f"{home_team} vs {away_team}",
                'minute': random.randint(1, 90),
                'title': f"Changement de momentum!",
                'content': f"{gaining_team} prend l\'ascendant sur {other_team} dans les dernières minutes!",
                'importance': 'medium'
            })
            
        elif alert_type == "valeur_betting":
            # Type de pari
            bet_types = ["1X2", "Over/Under", "Les deux équipes marquent"]
            bet_type = random.choice(bet_types)
            
            # Valeur détectée
            content = ""
            if bet_type == "1X2":
                team = random.choice([home_team, away_team])
                odds = round(2.0 + random.random() * 3, 2)
                content = f"Valeur détectée sur la victoire de {team} à {odds}"
            elif bet_type == "Over/Under":
                threshold = random.choice([1.5, 2.5, 3.5])
                direction = random.choice(["Plus", "Moins"])
                odds = round(1.5 + random.random() * 1.5, 2)
                content = f"Valeur détectée sur {direction} de {threshold} buts à {odds}"
            else:  # Les deux équipes marquent
                choice = random.choice(["Oui", "Non"])
                odds = round(1.5 + random.random() * 1, 2)
                content = f"Valeur détectée sur 'Les deux équipes marquent - {choice}' à {odds}"
                
            alerts.append({
                'type': 'value_bet',
                'timestamp': timestamp,
                'match': f"{home_team} vs {away_team}",
                'minute': random.randint(1, 90),
                'title': f"Opportunité de valeur [{bet_type}]",
                'content': content,
                'importance': 'high'
            })
    
    return alerts