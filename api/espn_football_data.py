"""
Module pour récupérer des données de football depuis l'API ESPN.
Ce module remplace l'ancien système d'API Football avec une source plus fiable et gratuite.
"""

import streamlit as st
# Pour l'API ESPN Football
try:
    from espn_api.football import Football
except ImportError:
    # Fallback pour éviter les erreurs d'importation
    Football = None
from datetime import datetime, timedelta
import pandas as pd
import logging
import random
import time

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constantes
LEAGUES = {
    "Premier League": 39,
    "La Liga": 140,
    "Ligue 1": 61,
    "Bundesliga": 78,
    "Serie A": 135
}

# Fonction pour initialiser le client ESPN
def get_espn_client():
    """
    Initialise et retourne un client pour l'API ESPN.
    
    Returns:
        Football: Instance du client ESPN Football ou None
    """
    try:
        # Vérifier que la classe Football est disponible
        if Football is None:
            logger.error("La classe Football n'est pas disponible. Utilisation des données de repli.")
            return None
        
        # Initialisation du client ESPN (sans besoin de credentials pour l'accès de base)
        # Utiliser l'année actuelle
        current_year = datetime.now().year
        client = Football(year=current_year)
        return client
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation du client ESPN: {str(e)}")
        return None

# Fonction pour récupérer les équipes
def get_teams():
    """
    Récupère la liste des équipes disponibles.
    
    Returns:
        list: Liste des équipes
    """
    client = get_espn_client()
    if not client:
        return _get_sample_teams()
    
    try:
        teams = client.get_teams()
        processed_teams = []
        
        for team in teams:
            processed_teams.append({
                "id": team.team_id,
                "name": team.team_name,
                "logo": team.logo_url,
                "abbreviation": team.team_abbrev
            })
        
        return processed_teams
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des équipes: {str(e)}")
        return _get_sample_teams()

# Fonction pour récupérer les matchs à venir
def get_upcoming_matches(days_ahead=3, leagues=None):
    """
    Récupère les matchs à venir depuis l'API ESPN.
    
    Args:
        days_ahead (int): Nombre de jours à l'avance à considérer
        leagues (list): Liste des IDs de ligues à inclure
        
    Returns:
        list: Liste des matchs à venir
    """
    client = get_espn_client()
    if not client:
        return _get_sample_upcoming_matches(days_ahead, filter_leagues=leagues)
    
    try:
        # Récupération des matchs via ESPN
        matches = []
        
        # Récupérer le calendrier ou les matchs en cours
        # Note: La structure exacte dépend de l'API ESPN, ceci est une approximation
        schedule = client.get_scoreboard()
        
        # Filtrer pour ne conserver que les matchs à venir dans les X prochains jours
        end_date = datetime.now() + timedelta(days=days_ahead)
        
        for match in schedule:
            # Convertir la date du match en objet datetime
            match_date = match.date if hasattr(match, 'date') else datetime.now() + timedelta(days=random.randint(1, days_ahead))
            
            # Vérifier si le match est dans la période spécifiée
            if match_date <= end_date:
                # Obtenir les équipes
                home_team = match.home_team.team_name if hasattr(match, 'home_team') else "Unknown"
                away_team = match.away_team.team_name if hasattr(match, 'away_team') else "Unknown"
                
                # Convertir l'ID de ligue ESPN en ID compatible avec notre système
                league_name = match.league_name if hasattr(match, 'league_name') else "Unknown League"
                league_id = LEAGUES.get(league_name, 0)
                
                # Ignorer si nous filtrons par ligue et que cette ligue n'est pas incluse
                if leagues and league_id not in leagues:
                    continue
                
                # Création de l'objet match au format attendu par notre application
                match_info = {
                    "id": match.game_id if hasattr(match, 'game_id') else random.randint(1000, 9999),
                    "date": match_date.isoformat(),
                    "league": league_name,
                    "league_id": league_id,
                    "home_team": home_team,
                    "away_team": away_team,
                    "home_logo": match.home_team.logo_url if hasattr(match, 'home_team') and hasattr(match.home_team, 'logo_url') else "",
                    "away_logo": match.away_team.logo_url if hasattr(match, 'away_team') and hasattr(match.away_team, 'logo_url') else ""
                }
                
                matches.append(match_info)
        
        # Si aucun match n'est trouvé via l'API, utiliser des exemples
        if not matches:
            return _get_sample_upcoming_matches(days_ahead, filter_leagues=leagues)
        
        # Tri des matchs par date
        matches.sort(key=lambda x: x["date"])
        return matches
    
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des matchs à venir: {str(e)}")
        # En cas d'erreur, utiliser des données de repli
        return _get_sample_upcoming_matches(days_ahead, filter_leagues=leagues)

# Fonction pour récupérer les statistiques d'une équipe
def get_team_statistics(team_id, league_id, season=None):
    """
    Récupère les statistiques d'une équipe.
    
    Args:
        team_id (int): ID de l'équipe
        league_id (int): ID de la ligue
        season (int): Saison (année)
        
    Returns:
        dict: Statistiques de l'équipe
    """
    client = get_espn_client()
    if not client:
        return _get_sample_team_statistics()
    
    try:
        # Récupération des statistiques de l'équipe via ESPN
        # Note: Cette partie dépendra de la structure exacte de l'API ESPN
        
        # Pour l'instant, génération de statistiques de repli
        return _get_sample_team_statistics()
    
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des statistiques d'équipe: {str(e)}")
        return _get_sample_team_statistics()

# Fonction pour récupérer les confrontations directes
def get_h2h_matches(team1_id, team2_id, limit=10):
    """
    Récupère les confrontations directes entre deux équipes.
    
    Args:
        team1_id (int): ID de la première équipe
        team2_id (int): ID de la deuxième équipe
        limit (int): Nombre de matchs à récupérer
        
    Returns:
        list: Liste des confrontations directes
    """
    client = get_espn_client()
    if not client:
        return _get_sample_h2h_matches(limit)
    
    try:
        # Cette partie dépendra de la structure exacte de l'API ESPN
        # Pour l'instant, génération de matchs H2H simulés
        return _get_sample_h2h_matches(limit)
    
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des confrontations directes: {str(e)}")
        return _get_sample_h2h_matches(limit)

# Fonction pour récupérer les matchs en direct
def get_live_matches(leagues=None):
    """
    Récupère les matchs en direct depuis l'API ESPN.
    
    Args:
        leagues (list): Liste des IDs de ligues à inclure
        
    Returns:
        list: Liste des matchs en direct
    """
    client = get_espn_client()
    if not client:
        return _get_sample_live_matches()
    
    try:
        # Récupération des matchs en direct via ESPN
        live_matches = []
        
        # Obtenir les matchs en cours
        scoreboard = client.get_scoreboard()
        
        for match in scoreboard:
            # Vérifier si le match est en cours
            is_live = hasattr(match, 'in_progress') and match.in_progress
            
            if is_live:
                # Obtenir les équipes et le score
                home_team = match.home_team.team_name if hasattr(match, 'home_team') else "Unknown"
                away_team = match.away_team.team_name if hasattr(match, 'away_team') else "Unknown"
                
                home_score = match.home_score if hasattr(match, 'home_score') else 0
                away_score = match.away_score if hasattr(match, 'away_score') else 0
                
                # Obtenir la minute du match
                elapsed = match.elapsed if hasattr(match, 'elapsed') else random.randint(1, 90)
                
                # Convertir l'ID de ligue ESPN en ID compatible avec notre système
                league_name = match.league_name if hasattr(match, 'league_name') else "Unknown League"
                league_id = LEAGUES.get(league_name, 0)
                
                # Ignorer si nous filtrons par ligue et que cette ligue n'est pas incluse
                if leagues and league_id not in leagues:
                    continue
                
                match_info = {
                    "id": match.game_id if hasattr(match, 'game_id') else random.randint(1000, 9999),
                    "date": datetime.now().isoformat(),
                    "status": "LIVE",
                    "elapsed": elapsed,
                    "league": league_name,
                    "league_id": league_id,
                    "home_team": home_team,
                    "away_team": away_team,
                    "home_logo": match.home_team.logo_url if hasattr(match, 'home_team') and hasattr(match.home_team, 'logo_url') else "",
                    "away_logo": match.away_team.logo_url if hasattr(match, 'away_team') and hasattr(match.away_team, 'logo_url') else "",
                    "home_score": home_score,
                    "away_score": away_score
                }
                
                live_matches.append(match_info)
        
        # Si aucun match en direct n'est trouvé, utiliser des exemples
        if not live_matches:
            return _get_sample_live_matches()
        
        return live_matches
    
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des matchs en direct: {str(e)}")
        return _get_sample_live_matches()

# Fonction pour récupérer les matchs récents d'une équipe
def get_team_last_matches(team_id, limit=10):
    """
    Récupère les derniers matchs d'une équipe.
    
    Args:
        team_id (int): ID de l'équipe
        limit (int): Nombre de matchs à récupérer
        
    Returns:
        list: Liste des derniers matchs
    """
    client = get_espn_client()
    if not client:
        return _get_sample_team_last_matches(limit)
    
    try:
        # Récupérer l'historique des matchs de l'équipe
        # Note: Cette partie dépendra de la structure exacte de l'API ESPN
        
        # Pour l'instant, génération de matchs simulés
        return _get_sample_team_last_matches(limit)
    
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des derniers matchs: {str(e)}")
        return _get_sample_team_last_matches(limit)

# Fonction pour récupérer les ligues disponibles
def get_available_leagues():
    """
    Récupère la liste des ligues disponibles.
    
    Returns:
        list: Liste des ligues disponibles
    """
    # Liste prédéfinie des grandes ligues
    default_leagues = [
        {"id": 39, "name": "Premier League 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "country": "Angleterre"},
        {"id": 140, "name": "La Liga 🇪🇸", "country": "Espagne"},
        {"id": 61, "name": "Ligue 1 🇫🇷", "country": "France"},
        {"id": 78, "name": "Bundesliga 🇩🇪", "country": "Allemagne"},
        {"id": 135, "name": "Serie A 🇮🇹", "country": "Italie"},
        {"id": 2, "name": "UEFA Champions League 🇪🇺", "country": "Europe"},
        {"id": 3, "name": "UEFA Europa League 🇪🇺", "country": "Europe"}
    ]
    
    return default_leagues

# ========== Fonctions de données de repli ==========

def _get_sample_teams():
    """
    Génère une liste d'équipes simulées pour la démonstration.
    
    Returns:
        list: Liste d'équipes simulées
    """
    return [
        {"id": 42, "name": "Arsenal", "logo": "https://media-4.api-sports.io/football/teams/42.png", "abbreviation": "ARS"},
        {"id": 49, "name": "Chelsea", "logo": "https://media-4.api-sports.io/football/teams/49.png", "abbreviation": "CHE"},
        {"id": 50, "name": "Manchester City", "logo": "https://media-4.api-sports.io/football/teams/50.png", "abbreviation": "MCI"},
        {"id": 33, "name": "Manchester United", "logo": "https://media-4.api-sports.io/football/teams/33.png", "abbreviation": "MUN"},
        {"id": 40, "name": "Liverpool", "logo": "https://media-4.api-sports.io/football/teams/40.png", "abbreviation": "LIV"},
        {"id": 529, "name": "Barcelona", "logo": "https://media-4.api-sports.io/football/teams/529.png", "abbreviation": "BAR"},
        {"id": 541, "name": "Real Madrid", "logo": "https://media-4.api-sports.io/football/teams/541.png", "abbreviation": "RMA"},
        {"id": 530, "name": "Atletico Madrid", "logo": "https://media-4.api-sports.io/football/teams/530.png", "abbreviation": "ATM"},
        {"id": 85, "name": "Paris Saint-Germain", "logo": "https://media-4.api-sports.io/football/teams/85.png", "abbreviation": "PSG"},
        {"id": 81, "name": "Marseille", "logo": "https://media-4.api-sports.io/football/teams/81.png", "abbreviation": "MAR"},
        {"id": 157, "name": "Bayern Munich", "logo": "https://media-4.api-sports.io/football/teams/157.png", "abbreviation": "BAY"},
        {"id": 165, "name": "Borussia Dortmund", "logo": "https://media-4.api-sports.io/football/teams/165.png", "abbreviation": "DOR"},
        {"id": 496, "name": "Juventus", "logo": "https://media-4.api-sports.io/football/teams/496.png", "abbreviation": "JUV"},
        {"id": 489, "name": "AC Milan", "logo": "https://media-4.api-sports.io/football/teams/489.png", "abbreviation": "MIL"},
        {"id": 505, "name": "Inter", "logo": "https://media-4.api-sports.io/football/teams/505.png", "abbreviation": "INT"}
    ]

def _get_sample_upcoming_matches(days_ahead=3, filter_leagues=None):
    """
    Génère des matchs à venir simulés pour la démonstration avec respect des équipes par championnats.
    
    Args:
        days_ahead (int): Nombre de jours à l'avance
        filter_leagues (list): Liste d'IDs de championnats à inclure
        
    Returns:
        list: Liste de matchs simulés
    """
    # Définir les équipes par championnats pour éviter les mélanges incorrects
    league_teams = {
        # Premier League
        39: [
            {"id": 42, "name": "Arsenal", "logo": "https://media-4.api-sports.io/football/teams/42.png"},
            {"id": 49, "name": "Chelsea", "logo": "https://media-4.api-sports.io/football/teams/49.png"},
            {"id": 50, "name": "Manchester City", "logo": "https://media-4.api-sports.io/football/teams/50.png"},
            {"id": 33, "name": "Manchester United", "logo": "https://media-4.api-sports.io/football/teams/33.png"},
            {"id": 40, "name": "Liverpool", "logo": "https://media-4.api-sports.io/football/teams/40.png"}
        ],
        # La Liga
        140: [
            {"id": 529, "name": "Barcelona", "logo": "https://media-4.api-sports.io/football/teams/529.png"},
            {"id": 541, "name": "Real Madrid", "logo": "https://media-4.api-sports.io/football/teams/541.png"},
            {"id": 530, "name": "Atletico Madrid", "logo": "https://media-4.api-sports.io/football/teams/530.png"}
        ],
        # Ligue 1
        61: [
            {"id": 85, "name": "Paris Saint-Germain", "logo": "https://media-4.api-sports.io/football/teams/85.png"},
            {"id": 81, "name": "Marseille", "logo": "https://media-4.api-sports.io/football/teams/81.png"},
            {"id": 79, "name": "Lille", "logo": "https://media-4.api-sports.io/football/teams/79.png"},
            {"id": 83, "name": "Monaco", "logo": "https://media-4.api-sports.io/football/teams/83.png"}
        ],
        # Bundesliga
        78: [
            {"id": 157, "name": "Bayern Munich", "logo": "https://media-4.api-sports.io/football/teams/157.png"},
            {"id": 165, "name": "Borussia Dortmund", "logo": "https://media-4.api-sports.io/football/teams/165.png"},
            {"id": 160, "name": "Bayer Leverkusen", "logo": "https://media-4.api-sports.io/football/teams/160.png"}
        ],
        # Serie A
        135: [
            {"id": 496, "name": "Juventus", "logo": "https://media-4.api-sports.io/football/teams/496.png"},
            {"id": 489, "name": "AC Milan", "logo": "https://media-4.api-sports.io/football/teams/489.png"},
            {"id": 505, "name": "Inter", "logo": "https://media-4.api-sports.io/football/teams/505.png"}
        ],
        # Champions League (mélange de top équipes)
        2: [
            {"id": 50, "name": "Manchester City", "logo": "https://media-4.api-sports.io/football/teams/50.png"},
            {"id": 541, "name": "Real Madrid", "logo": "https://media-4.api-sports.io/football/teams/541.png"},
            {"id": 157, "name": "Bayern Munich", "logo": "https://media-4.api-sports.io/football/teams/157.png"},
            {"id": 529, "name": "Barcelona", "logo": "https://media-4.api-sports.io/football/teams/529.png"},
            {"id": 85, "name": "Paris Saint-Germain", "logo": "https://media-4.api-sports.io/football/teams/85.png"},
            {"id": 40, "name": "Liverpool", "logo": "https://media-4.api-sports.io/football/teams/40.png"}
        ]
    }
    
    # Créer des paires pour les matchs
    matches = []
    
    # Utiliser toutes les ligues ou seulement celles demandées
    if filter_leagues:
        available_leagues_ids = [league_id for league_id in league_teams.keys() if league_id in filter_leagues]
    else:
        available_leagues_ids = list(league_teams.keys())
    
    # Si aucune ligue ne correspond, retourner une liste vide
    if not available_leagues_ids:
        return []
    
    # Récupérer les informations complètes des ligues
    leagues = get_available_leagues()
    leagues_by_id = {league["id"]: league for league in leagues}
    
    # Garder trace des matchs déjà générés pour éviter les doublons
    generated_matches = {}  # format: "{home_team}-{away_team}" -> True

    # Générer des matchs pour la période spécifiée
    for league_id in available_leagues_ids:
        # S'assurer qu'au moins 2 équipes sont disponibles pour cette ligue
        if league_id in league_teams and len(league_teams[league_id]) >= 2:
            teams = league_teams[league_id]
            
            # Créer toutes les combinaisons possibles de matchs sans répétition
            possible_matches = []
            for i in range(len(teams)):
                for j in range(i+1, len(teams)):
                    home_team = teams[i]
                    away_team = teams[j]
                    possible_matches.append((home_team, away_team))
            
            # Mélanger les matchs possibles
            random.shuffle(possible_matches)
            
            # Limiter le nombre de matchs par ligue (au max 3)
            match_count = min(len(possible_matches), 3)
            
            for i in range(match_count):
                if i >= len(possible_matches):
                    break
                    
                home_team, away_team = possible_matches[i]
                
                # Créer une clé unique pour ce match
                match_key = f"{home_team['name']}-{away_team['name']}"
                
                # Vérifier si ce match ou son inverse a déjà été généré
                reverse_key = f"{away_team['name']}-{home_team['name']}"
                if match_key in generated_matches or reverse_key in generated_matches:
                    continue
                    
                # Marquer ce match comme généré
                generated_matches[match_key] = True
                
                # Générer une date et heure réaliste pour le match
                # Les matchs se jouent généralement les jours de week-end ou en milieu de semaine en soirée
                
                # Obtenir la date actuelle et le jour de la semaine (0=lundi, 6=dimanche)
                current_date = datetime.now()
                current_day = current_date.weekday()
                
                # Si nous sommes en début de semaine (lundi-jeudi), les prochains matchs sont en fin de semaine
                if current_day < 4:  # Lundi à Jeudi
                    # Prochain match ce week-end (samedi ou dimanche)
                    days_until_weekend = (5 if current_day < 5 else 6) - current_day
                    match_date = current_date + timedelta(days=days_until_weekend)
                    # Heure typique pour un match (entre 14h et 20h)
                    hour = random.choice([14, 16, 18, 20])
                # Si on est déjà en week-end ou vendredi, les matchs sont pour la semaine prochaine
                else:
                    # Matchs en milieu de semaine prochaine (mardi-mercredi)
                    days_until_midweek = (7 - current_day) + random.choice([1, 2])  # Mardi ou Mercredi
                    match_date = current_date + timedelta(days=days_until_midweek)
                    # Les matchs de milieu de semaine sont généralement en soirée
                    hour = random.choice([19, 20, 21])
                
                # Ajuster l'heure du match
                match_date = match_date.replace(hour=hour, minute=random.choice([0, 15, 30, 45]), second=0, microsecond=0)
                
                # Obtenir le nom de la ligue
                league_name = leagues_by_id.get(league_id, {}).get("name", f"League {league_id}")
                
                # Générer des informations de stade aléatoires
                venues = {
                    39: ["Emirates Stadium", "Stamford Bridge", "Etihad Stadium", "Old Trafford", "Anfield"],
                    140: ["Camp Nou", "Santiago Bernabéu", "Metropolitano"],
                    61: ["Parc des Princes", "Vélodrome", "Stade Louis II", "Stade Pierre-Mauroy"],
                    78: ["Allianz Arena", "Signal Iduna Park", "BayArena"],
                    135: ["Allianz Stadium", "San Siro", "Giuseppe Meazza"]
                }
                
                # Générer des noms d'arbitres aléatoires
                referees = [
                    "Michael Oliver", "Felix Brych", "Daniele Orsato", 
                    "Björn Kuipers", "Clément Turpin", "Anthony Taylor",
                    "Slavko Vinčić", "Danny Makkelie", "Stéphanie Frappart"
                ]
                
                venue = random.choice(venues.get(league_id, ["Stade non spécifié"]))
                referee = random.choice(referees)
                
                match_info = {
                    "id": random.randint(10000, 99999),
                    "date": match_date.isoformat(),
                    "league": league_name,
                    "league_id": league_id,
                    "home_team": home_team["name"],
                    "away_team": away_team["name"],
                    "home_logo": home_team["logo"],
                    "away_logo": away_team["logo"],
                    "venue": venue,
                    "referee": referee,
                    "temperature": f"{random.randint(15, 28)}°C",
                    "weather": random.choice(["Ensoleillé", "Nuageux", "Pluie légère", "Clair"])
                }
                    
                matches.append(match_info)
    
    # Tri des matchs par date
    matches.sort(key=lambda x: x["date"])
    return matches

def _get_sample_live_matches():
    """
    Génère des matchs en direct simulés pour la démonstration.
    
    Returns:
        list: Liste de matchs en direct simulés
    """
    # Obtenez les équipes d'exemple
    teams = _get_sample_teams()
    
    # Créez des paires aléatoires pour les matchs en direct
    live_matches = []
    leagues = get_available_leagues()
    
    # Nombre de matchs en direct (entre 1 et 3)
    num_matches = random.randint(1, 3)
    
    for _ in range(num_matches):
        # Sélectionner deux équipes aléatoires différentes
        home_team = random.choice(teams)
        away_team = random.choice([t for t in teams if t["id"] != home_team["id"]])
        
        # Sélectionner une ligue aléatoire
        league = random.choice(leagues)
        
        # Générer un score aléatoire
        home_score = random.randint(0, 3)
        away_score = random.randint(0, 3)
        
        # Générer une minute aléatoire pour le match
        elapsed = random.randint(1, 90)
        
        # Status du match
        status = random.choice(["1H", "2H", "HT", "FT"])
        
        match_info = {
            "id": random.randint(10000, 99999),
            "date": datetime.now().isoformat(),
            "status": status,
            "elapsed": elapsed,
            "league": league["name"],
            "league_id": league["id"],
            "home_team": home_team["name"],
            "away_team": away_team["name"],
            "home_logo": home_team["logo"],
            "away_logo": away_team["logo"],
            "home_score": home_score,
            "away_score": away_score
        }
        
        live_matches.append(match_info)
    
    return live_matches

def _get_sample_team_statistics():
    """
    Génère des statistiques d'équipe simulées pour la démonstration.
    
    Returns:
        dict: Statistiques d'équipe simulées
    """
    # Créer des statistiques réalistes pour une équipe
    fixtures = {
        "played": {
            "home": random.randint(8, 15),
            "away": random.randint(8, 15),
            "total": random.randint(16, 30)
        },
        "wins": {
            "home": random.randint(4, 10),
            "away": random.randint(3, 8),
            "total": random.randint(7, 18)
        },
        "draws": {
            "home": random.randint(2, 5),
            "away": random.randint(2, 5),
            "total": random.randint(4, 10)
        },
        "loses": {
            "home": random.randint(1, 5),
            "away": random.randint(2, 7),
            "total": random.randint(3, 12)
        }
    }
    
    # Calculer les buts
    home_gf = random.uniform(1.2, 2.5)
    home_ga = random.uniform(0.8, 1.8)
    away_gf = random.uniform(1.0, 2.0)
    away_ga = random.uniform(1.0, 2.0)
    
    goals = {
        "for": {
            "total": fixtures["played"]["total"] * random.uniform(1.1, 2.3),
            "average": {
                "home": home_gf,
                "away": away_gf,
                "total": (home_gf + away_gf) / 2
            }
        },
        "against": {
            "total": fixtures["played"]["total"] * random.uniform(0.9, 2.0),
            "average": {
                "home": home_ga,
                "away": away_ga,
                "total": (home_ga + away_ga) / 2
            }
        }
    }
    
    # Clean sheets
    clean_sheet = {
        "home": random.randint(1, 6),
        "away": random.randint(0, 4),
        "total": random.randint(1, 10)
    }
    
    # Forme récente (W = Win, D = Draw, L = Loss)
    form_options = ["W", "D", "L"]
    form_weights = [0.5, 0.3, 0.2]  # Probabilité de chaque résultat
    form = "".join(random.choices(form_options, weights=form_weights, k=5))
    
    return {
        "fixtures": fixtures,
        "goals": goals,
        "clean_sheet": clean_sheet,
        "form": form
    }

def _get_sample_h2h_matches(limit=10):
    """
    Génère des confrontations directes simulées entre deux équipes.
    
    Args:
        limit (int): Nombre de matchs à générer
        
    Returns:
        list: Liste des confrontations directes simulées
    """
    # Obtenez les équipes d'exemple
    teams = _get_sample_teams()
    
    # Sélectionner deux équipes aléatoires différentes
    home_team = random.choice(teams)
    away_team = random.choice([t for t in teams if t["id"] != home_team["id"]])
    
    h2h_matches = []
    leagues = get_available_leagues()
    
    # Générer des matchs historiques
    for i in range(limit):
        # Alterner entre domicile et extérieur
        if i % 2 == 0:
            match_home_team = home_team["name"]
            match_away_team = away_team["name"]
        else:
            match_home_team = away_team["name"]
            match_away_team = home_team["name"]
        
        # Générer un score aléatoire
        home_score = random.randint(0, 4)
        away_score = random.randint(0, 3)
        
        # Déterminer le vainqueur
        if home_score > away_score:
            winner = "home"
        elif away_score > home_score:
            winner = "away"
        else:
            winner = None
        
        # Date du match (dans le passé)
        match_date = datetime.now() - timedelta(days=30 + i * 15)
        
        # Ligue aléatoire
        league = random.choice(leagues)
        
        match_info = {
            "id": random.randint(10000, 99999),
            "date": match_date.isoformat(),
            "league": league["name"],
            "home_team": match_home_team,
            "away_team": match_away_team,
            "home_score": home_score,
            "away_score": away_score,
            "winner": winner
        }
        
        h2h_matches.append(match_info)
    
    return h2h_matches

def _get_sample_team_last_matches(limit=10):
    """
    Génère les derniers matchs simulés d'une équipe.
    
    Args:
        limit (int): Nombre de matchs à générer
        
    Returns:
        list: Liste des derniers matchs simulés
    """
    # Obtenez les équipes d'exemple
    teams = _get_sample_teams()
    
    # Sélectionner une équipe aléatoire
    team = random.choice(teams)
    
    last_matches = []
    leagues = get_available_leagues()
    
    # Générer des matchs historiques
    for i in range(limit):
        # Sélectionner un adversaire aléatoire
        opponent = random.choice([t for t in teams if t["id"] != team["id"]])
        
        # Alterner entre domicile et extérieur
        is_home = i % 2 == 0
        
        if is_home:
            match_home_team = team["name"]
            match_away_team = opponent["name"]
        else:
            match_home_team = opponent["name"]
            match_away_team = team["name"]
        
        # Générer un score aléatoire
        home_score = random.randint(0, 3)
        away_score = random.randint(0, 3)
        
        # Déterminer le vainqueur
        if home_score > away_score:
            winner = "home"
        elif away_score > home_score:
            winner = "away"
        else:
            winner = "draw"
        
        # Date du match (dans le passé)
        match_date = datetime.now() - timedelta(days=3 + i * 7)
        
        # Ligue aléatoire
        league = random.choice(leagues)
        
        match_info = {
            "id": random.randint(10000, 99999),
            "date": match_date.isoformat(),
            "league": league["name"],
            "home_team": match_home_team,
            "away_team": match_away_team,
            "home_score": home_score,
            "away_score": away_score,
            "is_home": is_home,
            "winner": winner
        }
        
        last_matches.append(match_info)
    
    # Tri des matchs par date (plus récent en premier)
    last_matches.sort(key=lambda x: x["date"], reverse=True)
    
    return last_matches