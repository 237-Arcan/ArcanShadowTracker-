"""
Module pour récupérer des données de matchs de football depuis l'API Football.
Ce module centralise toutes les requêtes à l'API pour éviter la duplication de code.
"""

import os
import requests
from datetime import datetime, timedelta
import streamlit as st

def get_api_key():
    """
    Récupère la clé API Football depuis les variables d'environnement.
    
    Returns:
        str: Clé API Football, None si non disponible
    """
    api_key = os.environ.get("FOOTBALL_API_KEY")
    if not api_key:
        st.error("Clé API Football manquante. Certaines fonctionnalités seront limitées.")
    return api_key

def get_upcoming_matches(days_ahead=3, leagues=None):
    """
    Récupère les matchs à venir depuis l'API Football.
    
    Args:
        days_ahead (int): Nombre de jours à l'avance à considérer
        leagues (list): Liste des IDs de ligues à inclure
        
    Returns:
        list: Liste des matchs à venir
    """
    api_key = get_api_key()
    if not api_key:
        return []
        
    # Date de début (aujourd'hui) et date de fin
    today = datetime.today().strftime('%Y-%m-%d')
    end_date = (datetime.today() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
    
    # Si aucune ligue n'est spécifiée, utiliser les grandes ligues européennes
    if not leagues:
        leagues = [39, 140, 61, 78, 135]  # Premier League, La Liga, Ligue 1, Bundesliga, Serie A
        
    # Initialisation de la liste des matchs
    all_matches = []
    
    try:
        # Récupération des matchs pour chaque ligue
        for league_id in leagues:
            url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures"
            headers = {
                "X-RapidAPI-Key": api_key,
                "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
            }
            params = {
                "league": league_id,
                "from": today,
                "to": end_date,
                "timezone": "Europe/Paris"
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data["results"] > 0:
                    for match in data["response"]:
                        # Extraction des informations pertinentes
                        match_info = {
                            "id": match["fixture"]["id"],
                            "date": match["fixture"]["date"],
                            "league": match["league"]["name"],
                            "league_id": match["league"]["id"],
                            "home_team": match["teams"]["home"]["name"],
                            "away_team": match["teams"]["away"]["name"],
                            "home_logo": match["teams"]["home"]["logo"],
                            "away_logo": match["teams"]["away"]["logo"]
                        }
                        all_matches.append(match_info)
            else:
                st.warning(f"Erreur lors de la récupération des matchs pour la ligue {league_id}: {response.status_code}")
        
        # Tri des matchs par date
        all_matches.sort(key=lambda x: x["date"])
        return all_matches
    
    except Exception as e:
        st.error(f"Erreur lors de la récupération des matchs: {str(e)}")
        return []

def get_live_matches(leagues=None):
    """
    Récupère les matchs en direct depuis l'API Football.
    
    Args:
        leagues (list): Liste des IDs de ligues à inclure
        
    Returns:
        list: Liste des matchs en direct
    """
    api_key = get_api_key()
    if not api_key:
        return []
    
    # Si aucune ligue n'est spécifiée, utiliser les grandes ligues européennes
    if not leagues:
        leagues = [39, 140, 61, 78, 135]  # Premier League, La Liga, Ligue 1, Bundesliga, Serie A
    
    # Initialisation de la liste des matchs
    live_matches = []
    
    try:
        url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures"
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        params = {
            "live": "all"
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data["results"] > 0:
                for match in data["response"]:
                    # Vérifier si le match appartient à une des ligues spécifiées
                    if leagues and match["league"]["id"] not in leagues:
                        continue
                        
                    # Extraction des informations pertinentes
                    match_info = {
                        "id": match["fixture"]["id"],
                        "date": match["fixture"]["date"],
                        "status": match["fixture"]["status"]["short"],
                        "elapsed": match["fixture"]["status"]["elapsed"],
                        "league": match["league"]["name"],
                        "league_id": match["league"]["id"],
                        "home_team": match["teams"]["home"]["name"],
                        "away_team": match["teams"]["away"]["name"],
                        "home_logo": match["teams"]["home"]["logo"],
                        "away_logo": match["teams"]["away"]["logo"],
                        "home_score": match["goals"]["home"],
                        "away_score": match["goals"]["away"]
                    }
                    live_matches.append(match_info)
            return live_matches
        else:
            st.warning(f"Erreur lors de la récupération des matchs en direct: {response.status_code}")
            return []
            
    except Exception as e:
        st.error(f"Erreur lors de la récupération des matchs en direct: {str(e)}")
        return []

def get_team_statistics(team_id, league_id, season=None):
    """
    Récupère les statistiques d'une équipe dans une ligue spécifique.
    
    Args:
        team_id (int): ID de l'équipe
        league_id (int): ID de la ligue
        season (int): Saison (année de début), None pour la saison actuelle
        
    Returns:
        dict: Statistiques de l'équipe
    """
    api_key = get_api_key()
    if not api_key:
        return {}
    
    # Si aucune saison n'est spécifiée, utiliser l'année actuelle
    if not season:
        current_year = datetime.now().year
        # Si nous sommes après juin, utiliser l'année actuelle, sinon l'année précédente
        season = current_year if datetime.now().month > 6 else current_year - 1
    
    try:
        url = f"https://api-football-v1.p.rapidapi.com/v3/teams/statistics"
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        params = {
            "team": team_id,
            "league": league_id,
            "season": season
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if "response" in data:
                return data["response"]
            else:
                return {}
        else:
            st.warning(f"Erreur lors de la récupération des statistiques: {response.status_code}")
            return {}
            
    except Exception as e:
        st.error(f"Erreur lors de la récupération des statistiques: {str(e)}")
        return {}

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
    api_key = get_api_key()
    if not api_key:
        return []
    
    try:
        url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures/headtohead"
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        params = {
            "h2h": f"{team1_id}-{team2_id}",
            "last": limit
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data["results"] > 0:
                h2h_matches = []
                for match in data["response"]:
                    match_info = {
                        "id": match["fixture"]["id"],
                        "date": match["fixture"]["date"],
                        "league": match["league"]["name"],
                        "home_team": match["teams"]["home"]["name"],
                        "away_team": match["teams"]["away"]["name"],
                        "home_score": match["goals"]["home"],
                        "away_score": match["goals"]["away"],
                        "winner": match["teams"]["home"]["winner"] and "home" or match["teams"]["away"]["winner"] and "away" or "draw"
                    }
                    h2h_matches.append(match_info)
                return h2h_matches
            else:
                return []
        else:
            st.warning(f"Erreur lors de la récupération des confrontations directes: {response.status_code}")
            return []
            
    except Exception as e:
        st.error(f"Erreur lors de la récupération des confrontations directes: {str(e)}")
        return []

def get_team_last_matches(team_id, limit=10):
    """
    Récupère les derniers matchs d'une équipe.
    
    Args:
        team_id (int): ID de l'équipe
        limit (int): Nombre de matchs à récupérer
        
    Returns:
        list: Liste des derniers matchs
    """
    api_key = get_api_key()
    if not api_key:
        return []
    
    try:
        url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures"
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        params = {
            "team": team_id,
            "last": limit
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data["results"] > 0:
                matches = []
                for match in data["response"]:
                    match_info = {
                        "id": match["fixture"]["id"],
                        "date": match["fixture"]["date"],
                        "league": match["league"]["name"],
                        "home_team": match["teams"]["home"]["name"],
                        "away_team": match["teams"]["away"]["name"],
                        "home_score": match["goals"]["home"],
                        "away_score": match["goals"]["away"],
                        "is_home": match["teams"]["home"]["id"] == team_id,
                        "winner": match["teams"]["home"]["winner"] and "home" or match["teams"]["away"]["winner"] and "away" or "draw"
                    }
                    matches.append(match_info)
                return matches
            else:
                return []
        else:
            st.warning(f"Erreur lors de la récupération des derniers matchs: {response.status_code}")
            return []
            
    except Exception as e:
        st.error(f"Erreur lors de la récupération des derniers matchs: {str(e)}")
        return []

def get_available_leagues():
    """
    Récupère la liste des ligues disponibles dans l'API Football.
    
    Returns:
        list: Liste des ligues disponibles
    """
    # Pour l'instant, nous utilisons une liste prédéfinie des grandes ligues
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