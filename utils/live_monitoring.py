"""
Module pour la surveillance en direct des matchs de football.
"""
import random
from datetime import datetime, timedelta
import time

def get_live_matches():
    """
    Récupère les matchs actuellement en direct.
    
    Returns:
        list: Liste des matchs en direct
    """
    # Dans un système réel, cela récupérerait les données de l'API
    # Ici, nous générons des données simulées
    
    # Liste des équipes par ligue pour les matchs en direct
    teams = {
        'Premier League': ['Arsenal', 'Manchester City', 'Liverpool', 'Manchester United', 
                        'Chelsea', 'Tottenham'],
        'LaLiga': ['Real Madrid', 'Barcelona', 'Atletico Madrid', 'Sevilla', 
                 'Villarreal', 'Real Betis'],
        'Serie A': ['Inter Milan', 'AC Milan', 'Juventus', 'Napoli',
                  'Roma', 'Lazio'],
        'Bundesliga': ['Bayern Munich', 'Borussia Dortmund', 'RB Leipzig', 'Bayer Leverkusen',
                      'Wolfsburg', 'Borussia Mönchengladbach'],
        'Ligue 1': ['PSG', 'Marseille', 'Lyon', 'Lille', 
                   'Monaco', 'Rennes'],
        'UEFA Champions League': ['Real Madrid', 'Manchester City', 'Bayern Munich', 'PSG']
    }
    
    live_matches = []
    
    # Générer un nombre aléatoire de matchs en direct (entre 2 et 5)
    num_live_matches = random.randint(2, 5)
    
    # Sélectionner des ligues aléatoires
    leagues = random.sample(list(teams.keys()), min(num_live_matches, len(teams)))
    
    # Pour chaque ligue, créer un match en direct
    for league in leagues:
        # Sélectionner deux équipes aléatoires
        home, away = random.sample(teams[league], 2)
        
        # Déterminer la minute du match (entre 1 et 90)
        minute = random.randint(1, 90)
        
        # Temps ajouté si nous sommes en fin de mi-temps
        added_time = 0
        if 43 <= minute <= 45 or 88 <= minute <= 90:
            added_time = random.randint(1, 5)
            
        # Déterminer la mi-temps
        if minute <= 45 + added_time:
            period = "1ère mi-temps"
            display_minute = minute
        else:
            period = "2nde mi-temps"
            display_minute = minute - 45
            
        # Générer le score
        if minute < 15:
            # Début de match, probabilité plus élevée de 0-0
            home_goals = random.choices([0, 1], weights=[0.8, 0.2])[0]
            away_goals = random.choices([0, 1], weights=[0.8, 0.2])[0]
        elif minute < 45:
            # Première mi-temps
            home_goals = random.choices([0, 1, 2], weights=[0.4, 0.4, 0.2])[0]
            away_goals = random.choices([0, 1, 2], weights=[0.4, 0.4, 0.2])[0]
        else:
            # Deuxième mi-temps
            home_goals = random.choices([0, 1, 2, 3], weights=[0.2, 0.4, 0.3, 0.1])[0]
            away_goals = random.choices([0, 1, 2, 3], weights=[0.2, 0.4, 0.3, 0.1])[0]
            
        # Générer des statistiques de match
        possession = random.randint(40, 60)
        shots = random.randint(5, 15)
        shots_on_target = random.randint(1, shots)
        corners = random.randint(1, 8)
        yellow_cards = random.randint(0, 5)
        red_cards = random.randint(0, 1)
        
        # Créer l'objet match
        match_data = {
            'league': league,
            'home_team': home,
            'away_team': away,
            'home_score': home_goals,
            'away_score': away_goals,
            'minute': display_minute,
            'period': period,
            'added_time': added_time,
            'stats': {
                'possession': possession,
                'shots': shots,
                'shots_on_target': shots_on_target,
                'corners': corners,
                'yellow_cards': yellow_cards,
                'red_cards': red_cards
            },
            'live_odds': {
                'home_win': round(2.0 + random.random() * 2, 2),
                'draw': round(2.5 + random.random() * 1.5, 2),
                'away_win': round(2.0 + random.random() * 2, 2)
            },
            'momentum': random.randint(1, 100),
            'recent_events': generate_recent_events(minute, home, away, home_goals, away_goals)
        }
        
        live_matches.append(match_data)
        
    return live_matches

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
                'description': f"Changement significatif de momentum en faveur de l'équipe {'à domicile' if team_gained == 'home' else 'à l'extérieur'}"
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
                'content': f"{gaining_team} prend l'ascendant sur {other_team} dans les dernières minutes!",
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