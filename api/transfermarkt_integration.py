"""
Module d'intégration Transfermarkt pour ArcanShadow.
Ce module sert de point central pour l'accès aux données Transfermarkt
par tous les onglets et méta-systèmes de l'application.
"""

import logging
from api.transfermarkt_adapter import TransfermarktAdapter

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instance singleton de l'adaptateur Transfermarkt
_transfermarkt_adapter = None

def get_transfermarkt_adapter():
    """
    Récupère l'instance singleton de l'adaptateur Transfermarkt.
    
    Returns:
        TransfermarktAdapter: Instance de l'adaptateur Transfermarkt
    """
    global _transfermarkt_adapter
    
    if _transfermarkt_adapter is None:
        logger.info("Initialisation de l'adaptateur Transfermarkt global")
        _transfermarkt_adapter = TransfermarktAdapter()
        
    return _transfermarkt_adapter

def is_transfermarkt_available():
    """
    Vérifie si l'API Transfermarkt est disponible.
    
    Returns:
        bool: True si l'API est disponible, False sinon
    """
    adapter = get_transfermarkt_adapter()
    return adapter.api_online

def enhance_match_data_with_transfermarkt(match_data):
    """
    Enrichit les données d'un match avec des informations de Transfermarkt.
    
    Args:
        match_data (dict): Données du match à enrichir
        
    Returns:
        dict: Données du match enrichies
    """
    if not is_transfermarkt_available():
        logger.warning("API Transfermarkt non disponible pour l'enrichissement des données de match")
        return match_data
    
    # Créer une copie des données pour éviter de modifier l'original
    enhanced_data = match_data.copy()
    adapter = get_transfermarkt_adapter()
    
    try:
        # Récupérer les IDs des équipes si disponibles
        home_team_id = match_data.get('home_team_id')
        away_team_id = match_data.get('away_team_id')
        
        # Si les IDs ne sont pas disponibles, essayer de rechercher les équipes par nom
        if not home_team_id and 'home_team' in match_data:
            home_team_search = adapter.search_club(match_data['home_team'])
            if home_team_search and 'items' in home_team_search and home_team_search['items']:
                home_team_id = home_team_search['items'][0]['id']
                enhanced_data['home_team_id'] = home_team_id
                logger.info(f"ID Transfermarkt trouvé pour {match_data['home_team']}: {home_team_id}")
        
        if not away_team_id and 'away_team' in match_data:
            away_team_search = adapter.search_club(match_data['away_team'])
            if away_team_search and 'items' in away_team_search and away_team_search['items']:
                away_team_id = away_team_search['items'][0]['id']
                enhanced_data['away_team_id'] = away_team_id
                logger.info(f"ID Transfermarkt trouvé pour {match_data['away_team']}: {away_team_id}")
        
        # Enrichir avec les données de Transfermarkt si les IDs sont disponibles
        if home_team_id:
            home_team_data = adapter.get_club_profile(home_team_id)
            if home_team_data and 'status' not in home_team_data:
                enhanced_data['home_team_transfermarkt_data'] = home_team_data
                logger.info(f"Données Transfermarkt récupérées pour l'équipe domicile: {match_data.get('home_team')}")
        
        if away_team_id:
            away_team_data = adapter.get_club_profile(away_team_id)
            if away_team_data and 'status' not in away_team_data:
                enhanced_data['away_team_transfermarkt_data'] = away_team_data
                logger.info(f"Données Transfermarkt récupérées pour l'équipe extérieure: {match_data.get('away_team')}")
    
    except Exception as e:
        logger.error(f"Erreur lors de l'enrichissement des données avec Transfermarkt: {e}")
    
    return enhanced_data

def get_team_players(team_id):
    """
    Récupère les joueurs d'une équipe depuis Transfermarkt.
    
    Args:
        team_id (str): ID de l'équipe dans Transfermarkt
        
    Returns:
        dict: Données des joueurs de l'équipe
    """
    if not is_transfermarkt_available():
        logger.warning("API Transfermarkt non disponible pour la récupération des joueurs")
        return {'status': 'error', 'message': 'API non disponible'}
    
    adapter = get_transfermarkt_adapter()
    return adapter.get_club_players(team_id)

def get_team_profile(team_id):
    """
    Récupère le profil d'une équipe depuis Transfermarkt.
    
    Args:
        team_id (str): ID de l'équipe dans Transfermarkt
        
    Returns:
        dict: Profil de l'équipe
    """
    if not is_transfermarkt_available():
        logger.warning("API Transfermarkt non disponible pour la récupération du profil d'équipe")
        return {'status': 'error', 'message': 'API non disponible'}
    
    adapter = get_transfermarkt_adapter()
    return adapter.get_club_profile(team_id)

def search_club_by_name(club_name):
    """
    Recherche un club par son nom dans Transfermarkt.
    
    Args:
        club_name (str): Nom du club à rechercher
        
    Returns:
        dict: Résultats de la recherche
    """
    if not is_transfermarkt_available():
        logger.warning("API Transfermarkt non disponible pour la recherche de club")
        return {'status': 'error', 'message': 'API non disponible'}
    
    adapter = get_transfermarkt_adapter()
    return adapter.search_club(club_name)

def get_player_profile(player_id):
    """
    Récupère le profil d'un joueur depuis Transfermarkt.
    
    Args:
        player_id (str): ID du joueur dans Transfermarkt
        
    Returns:
        dict: Profil du joueur
    """
    if not is_transfermarkt_available():
        logger.warning("API Transfermarkt non disponible pour la récupération du profil de joueur")
        return {'status': 'error', 'message': 'API non disponible'}
    
    adapter = get_transfermarkt_adapter()
    return adapter.get_player_profile(player_id)

def search_player_by_name(player_name):
    """
    Recherche un joueur par son nom dans Transfermarkt.
    
    Args:
        player_name (str): Nom du joueur à rechercher
        
    Returns:
        dict: Résultats de la recherche
    """
    if not is_transfermarkt_available():
        logger.warning("API Transfermarkt non disponible pour la recherche de joueur")
        return {'status': 'error', 'message': 'API non disponible'}
    
    adapter = get_transfermarkt_adapter()
    return adapter.search_player(player_name)