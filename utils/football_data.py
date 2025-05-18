"""
Module pour charger et traiter les données de football depuis le dépôt football.json
"""
import os
import json
import random
from datetime import datetime, timedelta

# Mappings pour les noms des ligues et codes de pays
LEAGUE_NAMES = {
    'en.1': 'Premier League',
    'en.2': 'Championship',
    'es.1': 'LaLiga',
    'it.1': 'Serie A',
    'de.1': 'Bundesliga',
    'fr.1': 'Ligue 1',
    'nl.1': 'Eredivisie',
    'pt.1': 'Primeira Liga',
    'uefa.cl': 'Champions League'
}

COUNTRY_CODES = {
    'en': 'gb',
    'es': 'es',
    'it': 'it',
    'de': 'de',
    'fr': 'fr',
    'nl': 'nl',
    'pt': 'pt',
    'uefa': 'eu'
}

def get_league_data(season="2024-25", league_ids=None):
    """
    Charge les données des ligues spécifiées pour une saison donnée.
    
    Args:
        season (str): La saison à charger (format: "YYYY-YY")
        league_ids (list): Liste des identifiants de ligues à charger (ex: ['fr.1', 'en.1'])
                          Si None, charge toutes les ligues principales.
    
    Returns:
        dict: Dictionnaire avec les données des ligues
    """
    if league_ids is None:
        league_ids = ['en.1', 'es.1', 'it.1', 'de.1', 'fr.1']
    
    leagues_data = {}
    
    data_dir = os.path.join('data', 'football', season)
    if not os.path.exists(data_dir):
        return {}
    
    for league_id in league_ids:
        file_path = os.path.join(data_dir, f"{league_id}.json")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    league_data = json.load(f)
                leagues_data[league_id] = league_data
            except Exception as e:
                print(f"Erreur lors du chargement de {file_path}: {e}")
    
    return leagues_data

def get_matches_for_date(date=None, days_range=3, league_ids=None, season="2024-25"):
    """
    Récupère les matchs pour une date donnée ou autour de cette date.
    
    Args:
        date (str): Date au format YYYY-MM-DD. Si None, utilise la date du jour.
        days_range (int): Nombre de jours avant/après pour inclure les matchs
        league_ids (list): Liste des IDs de ligues à inclure
        season (str): Saison à utiliser
    
    Returns:
        tuple: (featured_matches, today_matches) - (Matchs à la une, Tous les matchs)
    """
    # Date par défaut = aujourd'hui
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    target_date = datetime.strptime(date, "%Y-%m-%d")
    min_date = (target_date - timedelta(days=days_range)).strftime("%Y-%m-%d")
    max_date = (target_date + timedelta(days=days_range)).strftime("%Y-%m-%d")
    
    # Charger les données des ligues
    leagues_data = get_league_data(season, league_ids)
    
    # Récupérer tous les matchs dans la plage de dates
    all_matches = []
    for league_id, league in leagues_data.items():
        country_code = league_id.split('.')[0]
        league_name = LEAGUE_NAMES.get(league_id, league.get('name', league_id))
        
        for match in league.get('matches', []):
            match_date = match.get('date')
            
            if min_date <= match_date <= max_date:
                # Convertir les données au format utilisé par ArcanShadow
                home_team = match.get('team1')
                away_team = match.get('team2')
                
                # Générer des cotes/probs simulées basées sur le score si disponible
                score = match.get('score', {}).get('ft', [])
                if len(score) == 2:
                    home_score, away_score = score
                    total_goals = home_score + away_score
                    
                    # Base les probabilités sur le score
                    if home_score > away_score:
                        home_prob = random.uniform(0.55, 0.75)
                        away_prob = random.uniform(0.15, 0.25)
                    elif away_score > home_score:
                        home_prob = random.uniform(0.15, 0.25)
                        away_prob = random.uniform(0.55, 0.75)
                    else:  # Match nul
                        home_prob = random.uniform(0.35, 0.45)
                        away_prob = random.uniform(0.35, 0.45)
                    
                    draw_prob = 1.0 - home_prob - away_prob
                else:
                    # Probs par défaut si pas de score
                    home_prob = random.uniform(0.35, 0.45)
                    draw_prob = random.uniform(0.25, 0.35)
                    away_prob = 1.0 - home_prob - draw_prob
                
                # Arrondir les probs
                home_prob = round(home_prob, 2)
                draw_prob = round(draw_prob, 2)
                away_prob = round(away_prob, 2)
                
                # Calculer les cotes (éviter les divisions par zéro)
                home_odds = round(1 / max(home_prob, 0.01), 2)
                draw_odds = round(1 / max(draw_prob, 0.01), 2)
                away_odds = round(1 / max(away_prob, 0.01), 2)
                
                # Obtenir et formater l'heure du match
                match_time = match.get('time', '??:??')
                
                # Formater la date et l'heure pour un affichage clair et fiable
                formatted_date = datetime.strptime(match_date, "%Y-%m-%d").strftime("%d/%m/%Y")
                
                # Créer l'objet match compatible avec ArcanShadow
                arcan_match = {
                    "league": league_name,
                    "country_code": COUNTRY_CODES.get(country_code, country_code),
                    "home_team": home_team,
                    "away_team": away_team,
                    "home": home_team,  # Alias pour compatibilité
                    "away": away_team,  # Alias pour compatibilité
                    "time": match_time,
                    "kickoff_time": match_time,
                    "date": match_date,
                    "formatted_date": formatted_date,
                    "full_date_time": f"{formatted_date} à {match_time}",
                    "home_odds": home_odds,
                    "draw_odds": draw_odds,
                    "away_odds": away_odds,
                    "home_prob": home_prob,
                    "draw_prob": draw_prob,
                    "away_prob": away_prob
                }
                
                # Ajouter le score si disponible
                if len(score) == 2:
                    arcan_match["score"] = f"{score[0]}-{score[1]}"
                
                all_matches.append(arcan_match)
    
    # Trier par date et heure
    all_matches.sort(key=lambda x: (x.get('date', ''), x.get('time', '')))
    
    # Sélectionner quelques matchs à la une
    featured_count = min(3, len(all_matches))
    featured_indices = random.sample(range(len(all_matches)), featured_count) if all_matches else []
    featured_matches = [all_matches[i] for i in featured_indices]
    
    # Retourner les listes de matchs
    today_matches = [match for i, match in enumerate(all_matches) if i not in featured_indices]
    
    return featured_matches, today_matches

def get_future_matches(days_ahead=7, league_ids=None, season="2024-25"):
    """
    Récupère les matchs à venir dans les prochains jours.
    
    Args:
        days_ahead (int): Nombre de jours à l'avance pour chercher des matchs
        league_ids (list): Liste des IDs de ligues à inclure
        season (str): Saison à utiliser
    
    Returns:
        tuple: (featured_matches, today_matches)
    """
    today = datetime.now().strftime("%Y-%m-%d")
    return get_matches_for_date(today, days_ahead, league_ids, season)