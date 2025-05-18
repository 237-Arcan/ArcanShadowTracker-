"""
Module pour gérer les données réelles de football.
"""
import os
import json
import requests
from datetime import datetime, timedelta
import random

# URL de base pour les données de football
FOOTBALL_DATA_API_URL = "https://api.football-data.org/v4"

def get_football_api_key():
    """Récupère la clé API pour football-data.org"""
    return os.environ.get("FOOTBALL_API_KEY", "")

def get_future_matches(days_ahead=7, league_ids=None, season="2024-25"):
    """
    Récupère les matchs à venir pour les ligues spécifiées.
    
    Args:
        days_ahead (int): Nombre de jours à considérer
        league_ids (list): Liste des identifiants de ligues
        season (str): Saison de football
        
    Returns:
        tuple: (featured_matches, all_matches)
    """
    if league_ids is None:
        league_ids = ['en.1', 'es.1', 'it.1', 'de.1', 'fr.1', 'uefa.cl']
        
    api_key = get_football_api_key()
    
    # Liste pour stocker les matchs
    featured_matches = []
    all_matches = []
    
    # Date actuelle et date future
    today = datetime.now()
    end_date = today + timedelta(days=days_ahead)
    
    if api_key:
        # Utiliser l'API football-data.org pour obtenir les matchs réels
        try:
            # Configuration pour la requête API
            headers = {"X-Auth-Token": api_key}
            
            # Liste des compétitions à utiliser
            competition_map = {
                'en.1': 2021,  # Premier League
                'es.1': 2014,  # LaLiga
                'it.1': 2019,  # Serie A
                'de.1': 2002,  # Bundesliga
                'fr.1': 2015,  # Ligue 1
                'uefa.cl': 2001  # UEFA Champions League
            }
            
            # Pour chaque ligue, récupérer les matchs à venir
            for league_id in league_ids:
                if league_id not in competition_map:
                    continue
                    
                competition_id = competition_map[league_id]
                
                # Formatage des dates pour l'API
                from_date = today.strftime("%Y-%m-%d")
                to_date = end_date.strftime("%Y-%m-%d")
                
                # Endpoint pour les matchs d'une compétition
                url = f"{FOOTBALL_DATA_API_URL}/competitions/{competition_id}/matches"
                params = {
                    "dateFrom": from_date,
                    "dateTo": to_date,
                    "status": "SCHEDULED"
                }
                
                response = requests.get(url, headers=headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for match in data.get('matches', []):
                        match_data = {
                            'league': match.get('competition', {}).get('name', ''),
                            'home_team': match.get('homeTeam', {}).get('name', ''),
                            'away_team': match.get('awayTeam', {}).get('name', ''),
                            'date': match.get('utcDate', '').split('T')[0],
                            'time': match.get('utcDate', '').split('T')[1][:5],
                            'status': match.get('status', ''),
                            'matchday': match.get('matchday', 0),
                            'home_odds': round(2.5 + random.random() * 2, 2),  # Simulation des cotes
                            'draw_odds': round(2.8 + random.random() * 1.5, 2),
                            'away_odds': round(2.5 + random.random() * 2, 2),
                            'home_prob': random.randint(30, 70),
                            'draw_prob': random.randint(15, 40),
                            'away_prob': random.randint(30, 70),
                        }
                        
                        # Corriger les probabilités pour qu'elles totalisent 100%
                        total_prob = match_data['home_prob'] + match_data['draw_prob'] + match_data['away_prob']
                        if total_prob != 100:
                            factor = 100 / total_prob
                            match_data['home_prob'] = int(match_data['home_prob'] * factor)
                            match_data['draw_prob'] = int(match_data['draw_prob'] * factor)
                            match_data['away_prob'] = 100 - match_data['home_prob'] - match_data['draw_prob']
                            
                        # Ajouter à la liste des matchs
                        all_matches.append(match_data)
                        
                        # Ajouter aux matchs mis en avant si c'est un match important
                        if match_data['matchday'] > 30 or random.random() > 0.7:
                            featured_matches.append(match_data)
                            
        except Exception as e:
            print(f"Erreur lors de la récupération des données: {str(e)}")
            # Générer des données de secours en cas d'erreur
            return _generate_fallback_matches(days_ahead)
    else:
        # Si pas de clé API, générer des données de secours
        return _generate_fallback_matches(days_ahead)
        
    # Si aucun match n'a été trouvé, générer des données de secours
    if not all_matches:
        return _generate_fallback_matches(days_ahead)
        
    return featured_matches, all_matches

def _generate_fallback_matches(days_ahead=7):
    """
    Génère des données de match de secours en cas d'erreur ou d'absence de clé API.
    
    Args:
        days_ahead (int): Nombre de jours à considérer
        
    Returns:
        tuple: (featured_matches, all_matches)
    """
    # Liste des équipes par ligue
    teams = {
        'Premier League': ['Arsenal', 'Manchester City', 'Liverpool', 'Manchester United', 
                        'Chelsea', 'Tottenham', 'Newcastle', 'Aston Villa'],
        'LaLiga': ['Real Madrid', 'Barcelona', 'Atletico Madrid', 'Sevilla', 
                 'Villarreal', 'Real Betis', 'Real Sociedad', 'Athletic Bilbao'],
        'Serie A': ['Inter Milan', 'AC Milan', 'Juventus', 'Napoli',
                  'Roma', 'Lazio', 'Atalanta', 'Fiorentina'],
        'Bundesliga': ['Bayern Munich', 'Borussia Dortmund', 'RB Leipzig', 'Bayer Leverkusen',
                      'Wolfsburg', 'Borussia Mönchengladbach', 'Eintracht Frankfurt', 'Union Berlin'],
        'Ligue 1': ['PSG', 'Marseille', 'Lyon', 'Lille', 
                   'Monaco', 'Rennes', 'Nice', 'Lens'],
        'UEFA Champions League': ['Real Madrid', 'Manchester City', 'Bayern Munich', 'PSG',
                                'Liverpool', 'Barcelona', 'Inter Milan', 'Borussia Dortmund']
    }
    
    # Date actuelle
    today = datetime.now()
    
    # Générer les matchs pour chaque ligue
    all_matches = []
    featured_matches = []
    
    for league, league_teams in teams.items():
        # Mélanger les équipes
        shuffled_teams = league_teams.copy()
        random.shuffle(shuffled_teams)
        
        # Créer des paires pour les matchs
        pairs = [(shuffled_teams[i], shuffled_teams[i+1]) for i in range(0, len(shuffled_teams), 2)]
        
        # Générer des matchs pour les jours à venir
        for i, (home, away) in enumerate(pairs):
            # Distribuer les matchs sur les jours à venir
            match_date = today + timedelta(days=i % days_ahead)
            
            # Générer une heure aléatoire entre 12h et 21h
            hour = random.randint(12, 21)
            minute = random.choice([0, 15, 30, 45])
            
            # Formater la date et l'heure
            date_str = match_date.strftime("%Y-%m-%d")
            time_str = f"{hour:02d}:{minute:02d}"
            
            # Générer des cotes aléatoires
            home_odds = round(1.5 + random.random() * 3, 2)
            draw_odds = round(2.5 + random.random() * 2, 2)
            away_odds = round(1.5 + random.random() * 3, 2)
            
            # Calculer les probabilités inversement proportionnelles aux cotes
            total_inverse = (1/home_odds) + (1/draw_odds) + (1/away_odds)
            home_prob = int(100 * (1/home_odds) / total_inverse)
            draw_prob = int(100 * (1/draw_odds) / total_inverse)
            away_prob = 100 - home_prob - draw_prob
            
            # Créer l'objet match
            match_data = {
                'league': league,
                'home_team': home,
                'away_team': away,
                'date': date_str,
                'time': time_str,
                'status': 'SCHEDULED',
                'matchday': random.randint(20, 38),
                'home_odds': home_odds,
                'draw_odds': draw_odds,
                'away_odds': away_odds,
                'home_prob': home_prob,
                'draw_prob': draw_prob,
                'away_prob': away_prob,
            }
            
            # Ajouter à la liste des matchs
            all_matches.append(match_data)
            
            # Ajouter aux matchs mis en avant si c'est un match important
            if home in ['Real Madrid', 'Barcelona', 'Manchester City', 'Liverpool', 'Bayern Munich', 'PSG'] or \
               away in ['Real Madrid', 'Barcelona', 'Manchester City', 'Liverpool', 'Bayern Munich', 'PSG'] or \
               random.random() > 0.7:
                featured_matches.append(match_data)
    
    return featured_matches, all_matches

def get_team_form(team_name, num_matches=5):
    """
    Récupère la forme récente d'une équipe (résultats des derniers matchs).
    
    Args:
        team_name (str): Nom de l'équipe
        num_matches (int): Nombre de matchs à considérer
        
    Returns:
        dict: Informations sur la forme de l'équipe
    """
    # Dans un système réel, cela récupérerait les données de l'API
    # Ici, nous générons des données aléatoires
    
    # Génère une séquence aléatoire de résultats (W = victoire, D = match nul, L = défaite)
    results = random.choices(['W', 'D', 'L'], weights=[0.5, 0.25, 0.25], k=num_matches)
    
    # Calculer les statistiques
    wins = results.count('W')
    draws = results.count('D')
    losses = results.count('L')
    
    # Générer des scores pour chaque résultat
    scores = []
    for result in results:
        if result == 'W':
            scores.append(f"{random.randint(1, 4)}-{random.randint(0, 1)}")
        elif result == 'D':
            draw_score = random.randint(0, 3)
            scores.append(f"{draw_score}-{draw_score}")
        else:  # 'L'
            scores.append(f"{random.randint(0, 1)}-{random.randint(1, 4)}")
    
    # Calculer le pourcentage de victoires
    win_percentage = (wins / num_matches) * 100
    
    # Calculer la dynamique (positive, neutre, négative)
    form_trend = "positive" if results[0:3].count('W') >= 2 else "negative" if results[0:3].count('L') >= 2 else "neutre"
    
    return {
        'team': team_name,
        'results': results,
        'scores': scores,
        'wins': wins,
        'draws': draws,
        'losses': losses,
        'win_percentage': win_percentage,
        'form_trend': form_trend
    }

def get_head_to_head(team1, team2, num_matches=5):
    """
    Récupère les résultats des confrontations directes entre deux équipes.
    
    Args:
        team1 (str): Première équipe
        team2 (str): Deuxième équipe
        num_matches (int): Nombre de matchs à considérer
        
    Returns:
        list: Liste des résultats des confrontations
    """
    # Dans un système réel, cela récupérerait les données de l'API
    # Ici, nous générons des données aléatoires
    
    # Déterminer quel type d'historique simuler (domination équipe1, équipe2 ou équilibre)
    h2h_type = random.choice(['balanced', 'team1_dominance', 'team2_dominance'])
    
    results = []
    for i in range(num_matches):
        # Date du match (de plus récent à plus ancien)
        match_date = (datetime.now() - timedelta(days=90*i)).strftime("%d/%m/%Y")
        
        # Déterminer le résultat en fonction du type d'historique
        if h2h_type == 'balanced':
            result_type = random.choice(['team1_win', 'draw', 'team2_win'])
        elif h2h_type == 'team1_dominance':
            result_type = random.choices(
                ['team1_win', 'draw', 'team2_win'], 
                weights=[0.6, 0.3, 0.1], 
                k=1
            )[0]
        else:  # team2_dominance
            result_type = random.choices(
                ['team1_win', 'draw', 'team2_win'], 
                weights=[0.1, 0.3, 0.6], 
                k=1
            )[0]
        
        # Générer le score en fonction du résultat
        if result_type == 'team1_win':
            score = f"{random.randint(1, 4)}-{random.randint(0, 1)}"
        elif result_type == 'draw':
            draw_score = random.randint(0, 3)
            score = f"{draw_score}-{draw_score}"
        else:  # team2_win
            score = f"{random.randint(0, 1)}-{random.randint(1, 4)}"
        
        # Ajouter le résultat à la liste
        results.append({
            'date': match_date,
            'score': score,
            'result': result_type
        })
    
    return results

def get_team_stats(team_name):
    """
    Récupère les statistiques d'une équipe.
    
    Args:
        team_name (str): Nom de l'équipe
        
    Returns:
        dict: Statistiques de l'équipe
    """
    # Dans un système réel, cela récupérerait les données de l'API
    # Ici, nous générons des données aléatoires
    
    return {
        'team': team_name,
        'goals_scored': random.randint(20, 60),
        'goals_conceded': random.randint(15, 50),
        'clean_sheets': random.randint(5, 15),
        'shots_per_game': round(random.uniform(8.0, 18.0), 1),
        'pass_completion': random.randint(75, 90),
        'possession': random.randint(45, 65),
        'cards': {
            'yellow': random.randint(30, 80),
            'red': random.randint(1, 5)
        },
        'home_record': {
            'wins': random.randint(5, 15),
            'draws': random.randint(2, 8),
            'losses': random.randint(1, 8)
        },
        'away_record': {
            'wins': random.randint(5, 12),
            'draws': random.randint(2, 8),
            'losses': random.randint(2, 10)
        }
    }