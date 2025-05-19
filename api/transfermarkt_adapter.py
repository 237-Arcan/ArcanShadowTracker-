"""
Module d'adaptation pour l'API Transfermarkt.
Ce module connecte ArcanShadow aux données de Transfermarkt pour améliorer
la qualité des analyses, en particulier pour YouthImpactAnalyzer et autres modules connexes.
"""

import os
import requests
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransfermarktAdapter:
    """
    Adaptateur pour l'API Transfermarkt.
    Cet adaptateur permet d'accéder aux informations sur les équipes, joueurs et compétitions
    depuis Transfermarkt.
    """
    
    def __init__(self):
        """Initialise l'adaptateur Transfermarkt."""
        self.base_url = "https://transfermarkt-api.fly.dev"
        self.api_online = self._check_api_connection()
        # Mise en cache pour éviter les appels répétés à l'API
        self.cache = {
            'clubs': {},
            'players': {},
            'competitions': {},
            'cache_time': {}
        }
        self.cache_expiration = 3600  # 1 heure en secondes
    
    def _check_api_connection(self):
        """
        Vérifie si l'API Transfermarkt est accessible.
        
        Returns:
            bool: True si l'API est accessible, False sinon
        """
        try:
            response = requests.get(f"{self.base_url}/docs")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Erreur de connexion à l'API Transfermarkt: {e}")
            return False
    
    def _get_from_cache(self, cache_type, item_id):
        """
        Récupère un élément du cache s'il existe et n'est pas expiré.
        
        Args:
            cache_type (str): Type de cache ('clubs', 'players', 'competitions')
            item_id (str): Identifiant de l'élément
            
        Returns:
            dict: Élément du cache ou None s'il n'existe pas ou est expiré
        """
        cache_key = f"{cache_type}_{item_id}"
        
        if cache_key in self.cache[cache_type]:
            # Vérifier l'expiration du cache
            if cache_key in self.cache['cache_time']:
                cache_time = self.cache['cache_time'][cache_key]
                current_time = datetime.now().timestamp()
                
                if current_time - cache_time < self.cache_expiration:
                    logger.info(f"Récupération de {cache_type} {item_id} depuis le cache")
                    return self.cache[cache_type][cache_key]
        
        return None
    
    def _save_to_cache(self, cache_type, item_id, data):
        """
        Sauvegarde un élément dans le cache.
        
        Args:
            cache_type (str): Type de cache ('clubs', 'players', 'competitions')
            item_id (str): Identifiant de l'élément
            data (dict): Données à mettre en cache
        """
        cache_key = f"{cache_type}_{item_id}"
        self.cache[cache_type][cache_key] = data
        self.cache['cache_time'][cache_key] = datetime.now().timestamp()
    
    def search_club(self, club_name):
        """
        Recherche un club par son nom.
        
        Args:
            club_name (str): Nom du club à rechercher
            
        Returns:
            dict: Résultats de la recherche
        """
        if not self.api_online:
            logger.warning("API Transfermarkt non disponible pour la recherche de club")
            return {'status': 'error', 'message': 'API non disponible'}
        
        try:
            # Vérifier dans le cache
            cache_result = self._get_from_cache('clubs', f"search_{club_name}")
            if cache_result:
                return cache_result
            
            # Appel à l'API
            response = requests.get(f"{self.base_url}/clubs/search/{club_name}")
            
            if response.status_code == 200:
                data = response.json()
                # Mettre en cache
                self._save_to_cache('clubs', f"search_{club_name}", data)
                return data
            else:
                logger.error(f"Erreur lors de la recherche du club {club_name}: {response.status_code}")
                return {'status': 'error', 'message': f"Erreur {response.status_code}"}
        
        except Exception as e:
            logger.error(f"Exception lors de la recherche du club {club_name}: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_club_profile(self, club_id):
        """
        Récupère le profil d'un club par son ID.
        
        Args:
            club_id (str): ID du club
            
        Returns:
            dict: Profil du club
        """
        if not self.api_online:
            logger.warning("API Transfermarkt non disponible pour le profil de club")
            return {'status': 'error', 'message': 'API non disponible'}
        
        try:
            # Vérifier dans le cache
            cache_result = self._get_from_cache('clubs', f"profile_{club_id}")
            if cache_result:
                return cache_result
            
            # Appel à l'API
            response = requests.get(f"{self.base_url}/clubs/{club_id}/profile")
            
            if response.status_code == 200:
                data = response.json()
                # Mettre en cache
                self._save_to_cache('clubs', f"profile_{club_id}", data)
                return data
            else:
                logger.error(f"Erreur lors de la récupération du profil du club {club_id}: {response.status_code}")
                return {'status': 'error', 'message': f"Erreur {response.status_code}"}
        
        except Exception as e:
            logger.error(f"Exception lors de la récupération du profil du club {club_id}: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_club_players(self, club_id, season_id=None):
        """
        Récupère les joueurs d'un club.
        
        Args:
            club_id (str): ID du club
            season_id (str, optional): ID de la saison. Par défaut None (saison actuelle).
            
        Returns:
            dict: Liste des joueurs du club
        """
        if not self.api_online:
            logger.warning("API Transfermarkt non disponible pour les joueurs du club")
            return {'status': 'error', 'message': 'API non disponible'}
        
        try:
            # Créer un identifiant unique pour le cache
            cache_id = f"players_{club_id}"
            if season_id:
                cache_id += f"_{season_id}"
            
            # Vérifier dans le cache
            cache_result = self._get_from_cache('clubs', cache_id)
            if cache_result:
                return cache_result
            
            # Construire l'URL
            url = f"{self.base_url}/clubs/{club_id}/players"
            if season_id:
                url += f"?season_id={season_id}"
            
            # Appel à l'API
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                # Mettre en cache
                self._save_to_cache('clubs', cache_id, data)
                return data
            else:
                logger.error(f"Erreur lors de la récupération des joueurs du club {club_id}: {response.status_code}")
                return {'status': 'error', 'message': f"Erreur {response.status_code}"}
        
        except Exception as e:
            logger.error(f"Exception lors de la récupération des joueurs du club {club_id}: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def search_player(self, player_name):
        """
        Recherche un joueur par son nom.
        
        Args:
            player_name (str): Nom du joueur à rechercher
            
        Returns:
            dict: Résultats de la recherche
        """
        if not self.api_online:
            logger.warning("API Transfermarkt non disponible pour la recherche de joueur")
            return {'status': 'error', 'message': 'API non disponible'}
        
        try:
            # Vérifier dans le cache
            cache_result = self._get_from_cache('players', f"search_{player_name}")
            if cache_result:
                return cache_result
            
            # Appel à l'API
            response = requests.get(f"{self.base_url}/players/search/{player_name}")
            
            if response.status_code == 200:
                data = response.json()
                # Mettre en cache
                self._save_to_cache('players', f"search_{player_name}", data)
                return data
            else:
                logger.error(f"Erreur lors de la recherche du joueur {player_name}: {response.status_code}")
                return {'status': 'error', 'message': f"Erreur {response.status_code}"}
        
        except Exception as e:
            logger.error(f"Exception lors de la recherche du joueur {player_name}: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_player_profile(self, player_id):
        """
        Récupère le profil d'un joueur par son ID.
        
        Args:
            player_id (str): ID du joueur
            
        Returns:
            dict: Profil du joueur
        """
        if not self.api_online:
            logger.warning("API Transfermarkt non disponible pour le profil de joueur")
            return {'status': 'error', 'message': 'API non disponible'}
        
        try:
            # Vérifier dans le cache
            cache_result = self._get_from_cache('players', f"profile_{player_id}")
            if cache_result:
                return cache_result
            
            # Appel à l'API
            response = requests.get(f"{self.base_url}/players/{player_id}/profile")
            
            if response.status_code == 200:
                data = response.json()
                # Mettre en cache
                self._save_to_cache('players', f"profile_{player_id}", data)
                return data
            else:
                logger.error(f"Erreur lors de la récupération du profil du joueur {player_id}: {response.status_code}")
                return {'status': 'error', 'message': f"Erreur {response.status_code}"}
        
        except Exception as e:
            logger.error(f"Exception lors de la récupération du profil du joueur {player_id}: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_competition_clubs(self, competition_id, season_id=None):
        """
        Récupère les clubs d'une compétition.
        
        Args:
            competition_id (str): ID de la compétition
            season_id (str, optional): ID de la saison. Par défaut None (saison actuelle).
            
        Returns:
            dict: Liste des clubs de la compétition
        """
        if not self.api_online:
            logger.warning("API Transfermarkt non disponible pour les clubs de la compétition")
            return {'status': 'error', 'message': 'API non disponible'}
        
        try:
            # Créer un identifiant unique pour le cache
            cache_id = f"clubs_{competition_id}"
            if season_id:
                cache_id += f"_{season_id}"
            
            # Vérifier dans le cache
            cache_result = self._get_from_cache('competitions', cache_id)
            if cache_result:
                return cache_result
            
            # Construire l'URL
            url = f"{self.base_url}/competitions/{competition_id}/clubs"
            if season_id:
                url += f"?season_id={season_id}"
            
            # Appel à l'API
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                # Mettre en cache
                self._save_to_cache('competitions', cache_id, data)
                return data
            else:
                logger.error(f"Erreur lors de la récupération des clubs de la compétition {competition_id}: {response.status_code}")
                return {'status': 'error', 'message': f"Erreur {response.status_code}"}
        
        except Exception as e:
            logger.error(f"Exception lors de la récupération des clubs de la compétition {competition_id}: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_competition_table(self, competition_id, season_id=None):
        """
        Récupère le classement d'une compétition.
        
        Args:
            competition_id (str): ID de la compétition
            season_id (str, optional): ID de la saison. Par défaut None (saison actuelle).
            
        Returns:
            dict: Classement de la compétition
        """
        if not self.api_online:
            logger.warning("API Transfermarkt non disponible pour le classement de la compétition")
            return {'status': 'error', 'message': 'API non disponible'}
        
        try:
            # Créer un identifiant unique pour le cache
            cache_id = f"table_{competition_id}"
            if season_id:
                cache_id += f"_{season_id}"
            
            # Vérifier dans le cache
            cache_result = self._get_from_cache('competitions', cache_id)
            if cache_result:
                return cache_result
            
            # Construire l'URL
            url = f"{self.base_url}/competitions/{competition_id}/table"
            if season_id:
                url += f"?season_id={season_id}"
            
            # Appel à l'API
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                # Mettre en cache
                self._save_to_cache('competitions', cache_id, data)
                return data
            else:
                logger.error(f"Erreur lors de la récupération du classement de la compétition {competition_id}: {response.status_code}")
                return {'status': 'error', 'message': f"Erreur {response.status_code}"}
        
        except Exception as e:
            logger.error(f"Exception lors de la récupération du classement de la compétition {competition_id}: {e}")
            return {'status': 'error', 'message': str(e)}

# Exemple d'utilisation:
# transfermarkt = TransfermarktAdapter()
# club_data = transfermarkt.search_club("Paris Saint-Germain")
# print(club_data)