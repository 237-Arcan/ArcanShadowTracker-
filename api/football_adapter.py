"""
Module adaptateur pour assurer la compatibilité entre l'API ESPN et l'interface existante.
Ce module permet une transition en douceur de l'ancienne API Football vers l'API ESPN.
"""

import os
import logging
from api import espn_football_data

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fonction pour récupérer une clé API
def get_api_key():
    """
    Fonction de compatibilité pour la transition vers ESPN.
    
    Returns:
        str: Toujours une valeur non vide
    """
    return "ESPN_ADAPTER"  # Valeur fictive pour assurer le bon fonctionnement

# Fonction pour récupérer les matchs à venir
def get_upcoming_matches(days_ahead=3, leagues=None):
    """
    Récupère les matchs à venir via l'API ESPN.
    
    Args:
        days_ahead (int): Nombre de jours à l'avance à considérer
        leagues (list): Liste des IDs de ligues à inclure
        
    Returns:
        list: Liste des matchs à venir
    """
    logger.info(f"Récupération des matchs à venir pour les {days_ahead} prochains jours")
    return espn_football_data.get_upcoming_matches(days_ahead, leagues)

# Fonction pour récupérer les matchs en direct
def get_live_matches(leagues=None):
    """
    Récupère les matchs en direct via l'API ESPN.
    
    Args:
        leagues (list): Liste des IDs de ligues à inclure
        
    Returns:
        list: Liste des matchs en direct
    """
    logger.info("Récupération des matchs en direct")
    return espn_football_data.get_live_matches(leagues)

# Fonction pour récupérer les statistiques d'une équipe
def get_team_statistics(team_id, league_id, season=None):
    """
    Récupère les statistiques d'une équipe via l'API ESPN.
    
    Args:
        team_id (int): ID de l'équipe
        league_id (int): ID de la ligue
        season (int): Saison (année)
        
    Returns:
        dict: Statistiques de l'équipe
    """
    logger.info(f"Récupération des statistiques pour l'équipe {team_id}")
    return espn_football_data.get_team_statistics(team_id, league_id, season)

# Fonction pour récupérer les confrontations directes
def get_h2h_matches(team1_id, team2_id, limit=10):
    """
    Récupère les confrontations directes entre deux équipes via l'API ESPN.
    
    Args:
        team1_id (int): ID de la première équipe
        team2_id (int): ID de la deuxième équipe
        limit (int): Nombre de matchs à récupérer
        
    Returns:
        list: Liste des confrontations directes
    """
    logger.info(f"Récupération des confrontations directes entre {team1_id} et {team2_id}")
    return espn_football_data.get_h2h_matches(team1_id, team2_id, limit)

# Fonction pour récupérer les derniers matchs d'une équipe
def get_team_last_matches(team_id, limit=10):
    """
    Récupère les derniers matchs d'une équipe via l'API ESPN.
    
    Args:
        team_id (int): ID de l'équipe
        limit (int): Nombre de matchs à récupérer
        
    Returns:
        list: Liste des derniers matchs
    """
    logger.info(f"Récupération des derniers matchs pour l'équipe {team_id}")
    return espn_football_data.get_team_last_matches(team_id, limit)

# Fonction pour récupérer les ligues disponibles
def get_available_leagues():
    """
    Récupère la liste des ligues disponibles via l'API ESPN.
    
    Returns:
        list: Liste des ligues disponibles
    """
    logger.info("Récupération des ligues disponibles")
    return espn_football_data.get_available_leagues()