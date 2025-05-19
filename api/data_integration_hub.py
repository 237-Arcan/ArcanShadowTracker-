"""
Module hub d'intégration de données pour ArcanShadow.
Ce module centralise l'accès aux différentes sources de données
(Transfermarkt, soccerdata, et enrichissements détaillés)
pour toutes les composantes du système.
"""

import logging
import pandas as pd
from datetime import datetime
import os

# Importer nos sources de données
from api.transfermarkt_integration import (
    is_transfermarkt_available,
    enhance_match_data_with_transfermarkt,
    get_team_players,
    get_team_profile,
    search_club_by_name,
    get_player_profile,
    search_player_by_name
)

# Importer nos nouvelles intégrations
try:
    from api.soccerdata_integration import (
        is_soccerdata_available,
        get_soccer_data_integration,
        enhance_match_data_with_soccerdata,
        get_available_sources
    )
    SOCCERDATA_IMPORTED = True
except ImportError:
    SOCCERDATA_IMPORTED = False

try:
    from api.player_data_enrichment import (
        get_detailed_player_data,
        get_detailed_manager_data,
        enrich_team_with_player_data,
        get_player_data_enrichment
    )
    PLAYER_ENRICHMENT_IMPORTED = True
except ImportError:
    PLAYER_ENRICHMENT_IMPORTED = False

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataIntegrationHub:
    """
    Classe centrale pour l'intégration de données dans ArcanShadow.
    Ce hub fournit une interface unifiée pour accéder à toutes les sources de données,
    en privilégiant les données les plus complètes et en dégradant gracieusement
    en cas d'indisponibilité de certaines sources.
    """
    
    def __init__(self):
        """Initialise le hub d'intégration de données."""
        self.sources_available = self._check_sources_availability()
        logger.info(f"Hub d'intégration de données initialisé. Sources disponibles: {self.sources_available}")
    
    def _check_sources_availability(self):
        """
        Vérifie la disponibilité des différentes sources de données.
        
        Returns:
            dict: Dictionnaire indiquant la disponibilité de chaque source
        """
        sources = {
            'transfermarkt': is_transfermarkt_available()
        }
        
        # Vérifier soccerdata si importé
        if SOCCERDATA_IMPORTED:
            sources['soccerdata'] = is_soccerdata_available()
            
            # Si soccerdata est disponible, vérifier quelles sources spécifiques sont disponibles
            if sources['soccerdata']:
                available_sources = get_available_sources()
                for source, available in available_sources.items():
                    sources[f'soccerdata_{source}'] = available
        else:
            sources['soccerdata'] = False
        
        # Vérifier l'enrichissement de données joueur si importé
        if PLAYER_ENRICHMENT_IMPORTED:
            sources['player_enrichment'] = True
            
            # Récupérer les sources disponibles pour l'enrichissement
            try:
                enrichment = get_player_data_enrichment()
                enrichment_sources = enrichment.sources_available
                for source, available in enrichment_sources.items():
                    if source not in sources:
                        sources[source] = available
            except Exception as e:
                logger.error(f"Erreur lors de la vérification des sources d'enrichissement: {e}")
                sources['player_enrichment'] = False
        else:
            sources['player_enrichment'] = False
        
        return sources
    
    def get_upcoming_matches(self, days_ahead=3, leagues=None):
        """
        Récupère les matchs à venir depuis l'API Football.
        Cette méthode redirige vers la fonction dans le module football_data.
        
        Args:
            days_ahead (int): Nombre de jours à l'avance à considérer
            leagues (list): Liste des IDs de ligues à inclure
            
        Returns:
            list: Liste des matchs à venir
        """
        # Importer ici pour éviter les imports circulaires
        from api.football_data import get_upcoming_matches as get_matches
        return get_matches(days_ahead=days_ahead, leagues=leagues)
    
    def enhance_match_data(self, match_data):
        """
        Enrichit les données d'un match avec toutes les sources disponibles.
        
        Args:
            match_data (dict): Données du match à enrichir
            
        Returns:
            dict: Données du match enrichies
        """
        enhanced_data = match_data.copy()
        
        # 1. Transfermarkt (base)
        if self.sources_available['transfermarkt']:
            try:
                enhanced_data = enhance_match_data_with_transfermarkt(enhanced_data)
            except Exception as e:
                logger.error(f"Erreur lors de l'enrichissement avec Transfermarkt: {e}")
        
        # 2. soccerdata (si disponible)
        if self.sources_available.get('soccerdata', False) and SOCCERDATA_IMPORTED:
            try:
                enhanced_data = enhance_match_data_with_soccerdata(enhanced_data)
            except Exception as e:
                logger.error(f"Erreur lors de l'enrichissement avec soccerdata: {e}")
        
        # 3. Enrichissement détaillé des équipes et joueurs (si disponible)
        if self.sources_available.get('player_enrichment', False) and PLAYER_ENRICHMENT_IMPORTED:
            try:
                # Enrichir les données de l'équipe à domicile avec les détails des joueurs
                if 'home_team' in enhanced_data:
                    home_team_data = {
                        'team_name': enhanced_data['home_team']
                    }
                    
                    # Utiliser les données Transfermarkt si disponibles
                    if 'home_team_transfermarkt_data' in enhanced_data:
                        home_team_data['transfermarkt_data'] = enhanced_data['home_team_transfermarkt_data']
                    
                    # Utiliser les données soccerdata si disponibles
                    if 'home_team_form' in enhanced_data:
                        home_team_data['form'] = enhanced_data['home_team_form']
                    
                    if 'home_team_elo' in enhanced_data:
                        home_team_data['elo_rating'] = enhanced_data['home_team_elo']
                    
                    # Enrichir avec les détails des joueurs
                    home_team_data = enrich_team_with_player_data(home_team_data)
                    
                    # Ajouter aux données du match
                    enhanced_data['home_team_detailed'] = home_team_data
                
                # Enrichir les données de l'équipe à l'extérieur avec les détails des joueurs
                if 'away_team' in enhanced_data:
                    away_team_data = {
                        'team_name': enhanced_data['away_team']
                    }
                    
                    # Utiliser les données Transfermarkt si disponibles
                    if 'away_team_transfermarkt_data' in enhanced_data:
                        away_team_data['transfermarkt_data'] = enhanced_data['away_team_transfermarkt_data']
                    
                    # Utiliser les données soccerdata si disponibles
                    if 'away_team_form' in enhanced_data:
                        away_team_data['form'] = enhanced_data['away_team_form']
                    
                    if 'away_team_elo' in enhanced_data:
                        away_team_data['elo_rating'] = enhanced_data['away_team_elo']
                    
                    # Enrichir avec les détails des joueurs
                    away_team_data = enrich_team_with_player_data(away_team_data)
                    
                    # Ajouter aux données du match
                    enhanced_data['away_team_detailed'] = away_team_data
            except Exception as e:
                logger.error(f"Erreur lors de l'enrichissement détaillé des équipes: {e}")
        
        return enhanced_data
    
    def get_player_details(self, player_name, team_name=None):
        """
        Récupère des détails complets sur un joueur en combinant toutes les sources disponibles.
        
        Args:
            player_name (str): Nom du joueur
            team_name (str, optional): Nom de l'équipe pour faciliter l'identification
            
        Returns:
            dict: Détails complets sur le joueur
        """
        player_data = {}
        
        # Utiliser l'enrichissement détaillé si disponible
        if self.sources_available.get('player_enrichment', False) and PLAYER_ENRICHMENT_IMPORTED:
            try:
                player_data = get_detailed_player_data(player_name, team_name)
                if player_data:
                    return player_data
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des détails du joueur avec l'enrichissement: {e}")
        
        # Sinon, essayer avec Transfermarkt
        if self.sources_available['transfermarkt']:
            try:
                # Rechercher le joueur
                search_results = search_player_by_name(player_name)
                
                if search_results and 'items' in search_results and search_results['items']:
                    # Filtrer par équipe si spécifiée
                    player_items = search_results['items']
                    
                    if team_name:
                        filtered_items = [item for item in player_items if team_name.lower() in item.get('clubName', '').lower()]
                        if filtered_items:
                            player_items = filtered_items
                    
                    # Utiliser le premier résultat
                    player_id = player_items[0]['id']
                    tm_player_data = get_player_profile(player_id)
                    
                    if tm_player_data and 'status' not in tm_player_data:
                        player_data = {
                            'name': tm_player_data.get('name', player_name),
                            'team': tm_player_data.get('club', {}).get('name', team_name) if team_name else tm_player_data.get('club', {}).get('name', ''),
                            'position': tm_player_data.get('positions', [{}])[0].get('name', '') if tm_player_data.get('positions') else '',
                            'nationality': tm_player_data.get('citizenship', {}).get('name', ''),
                            'birth_date': tm_player_data.get('dateOfBirth', ''),
                            'height': tm_player_data.get('height', ''),
                            'market_value': tm_player_data.get('marketValue', {}).get('value', ''),
                            'data_source': 'transfermarkt'
                        }
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des détails du joueur avec Transfermarkt: {e}")
        
        # Si aucun résultat, essayer avec soccerdata
        if not player_data and self.sources_available.get('soccerdata', False) and SOCCERDATA_IMPORTED:
            try:
                soccer_data = get_soccer_data_integration()
                
                # Essayer d'abord avec FBref
                if self.sources_available.get('soccerdata_fbref', False):
                    player_stats = soccer_data.get_player_detailed_stats(
                        player_name=player_name,
                        team_name=team_name,
                        source='fbref'
                    )
                    
                    if not player_stats.empty:
                        # Convertir en dictionnaire
                        stats = player_stats.iloc[0].to_dict()
                        
                        player_data = {
                            'name': stats.get('player', player_name),
                            'team': stats.get('team', team_name) if team_name else stats.get('team', ''),
                            'position': stats.get('position', ''),
                            'nationality': stats.get('nationality', ''),
                            'age': stats.get('age', ''),
                            'data_source': 'soccerdata_fbref'
                        }
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des détails du joueur avec soccerdata: {e}")
        
        return player_data
    
    def get_team_details(self, team_name):
        """
        Récupère des détails complets sur une équipe en combinant toutes les sources disponibles.
        
        Args:
            team_name (str): Nom de l'équipe
            
        Returns:
            dict: Détails complets sur l'équipe
        """
        team_data = {'team_name': team_name}
        
        # Commencer avec Transfermarkt (base)
        if self.sources_available['transfermarkt']:
            try:
                # Rechercher l'équipe
                search_results = search_club_by_name(team_name)
                
                if search_results and 'items' in search_results and search_results['items']:
                    team_id = search_results['items'][0]['id']
                    tm_team_data = get_team_profile(team_id)
                    
                    if tm_team_data and 'status' not in tm_team_data:
                        team_data['transfermarkt_data'] = tm_team_data
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des détails de l'équipe avec Transfermarkt: {e}")
        
        # Ajouter les informations de soccerdata (si disponible)
        if self.sources_available.get('soccerdata', False) and SOCCERDATA_IMPORTED:
            try:
                soccer_data = get_soccer_data_integration()
                
                # Essayer de récupérer la forme récente de l'équipe
                team_form = soccer_data.get_team_form(team_name)
                if not team_form.empty:
                    team_data['form'] = team_form.to_dict()
                
                # Essayer de récupérer les statistiques de l'équipe
                team_stats = soccer_data.get_team_stats(team_name)
                if not team_stats.empty:
                    team_data['stats'] = team_stats.to_dict()
                
                # Essayer de récupérer le classement Elo
                if self.sources_available.get('soccerdata_clubelo', False):
                    elo_rating = soccer_data.get_team_elo_rating(team_name)
                    if elo_rating is not None:
                        team_data['elo_rating'] = elo_rating
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des détails de l'équipe avec soccerdata: {e}")
        
        # Enrichir avec les détails des joueurs (si disponible)
        if self.sources_available.get('player_enrichment', False) and PLAYER_ENRICHMENT_IMPORTED:
            try:
                team_data = enrich_team_with_player_data(team_data)
            except Exception as e:
                logger.error(f"Erreur lors de l'enrichissement de l'équipe avec les détails des joueurs: {e}")
        
        return team_data
    
    def get_league_standings(self, league_code, season=None):
        """
        Récupère le classement d'une ligue en utilisant la meilleure source disponible.
        
        Args:
            league_code (str): Code de la ligue
            season (str, optional): Saison (ex: "2023/2024")
            
        Returns:
            pd.DataFrame: Classement de la ligue
        """
        standings = pd.DataFrame()
        
        # Essayer avec soccerdata (meilleures données de classement)
        if self.sources_available.get('soccerdata', False) and SOCCERDATA_IMPORTED:
            try:
                soccer_data = get_soccer_data_integration()
                
                # Essayer différentes sources dans l'ordre de préférence
                for source in ['fbref', 'espn', 'fotmob', 'sofascore']:
                    if self.sources_available.get(f'soccerdata_{source}', False):
                        standings = soccer_data.get_league_standings(
                            league_code=league_code,
                            season=season,
                            source=source
                        )
                        
                        if not standings.empty:
                            break
            except Exception as e:
                logger.error(f"Erreur lors de la récupération du classement avec soccerdata: {e}")
        
        # Si aucun résultat, essayer avec Transfermarkt ou d'autres sources
        # Note: Transfermarkt API ne fournit pas directement un classement de ligue
        
        return standings
    
    def get_match_statistics(self, home_team, away_team, date=None, league_code=None):
        """
        Récupère les statistiques d'un match en utilisant la meilleure source disponible.
        
        Args:
            home_team (str): Nom de l'équipe à domicile
            away_team (str): Nom de l'équipe à l'extérieur
            date (str, optional): Date du match (format YYYY-MM-DD)
            league_code (str, optional): Code de la ligue
            
        Returns:
            dict: Statistiques du match
        """
        match_stats = {}
        
        # Essayer avec soccerdata (meilleures données de statistiques de match)
        if self.sources_available.get('soccerdata', False) and SOCCERDATA_IMPORTED:
            try:
                soccer_data = get_soccer_data_integration()
                
                # Essayer différentes sources dans l'ordre de préférence
                for source in ['fotmob', 'sofascore', 'whoscored', 'fbref']:
                    if self.sources_available.get(f'soccerdata_{source}', False):
                        stats = soccer_data.get_match_statistics(
                            home_team=home_team,
                            away_team=away_team,
                            date=date,
                            league_code=league_code,
                            source=source
                        )
                        
                        if stats:
                            match_stats = stats
                            break
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des statistiques de match avec soccerdata: {e}")
        
        return match_stats
    
    def is_source_available(self, source):
        """
        Vérifie si une source spécifique est disponible.
        
        Args:
            source (str): Nom de la source à vérifier
            
        Returns:
            bool: True si la source est disponible, False sinon
        """
        return self.sources_available.get(source, False)
    
    def get_available_sources(self):
        """
        Récupère la liste des sources disponibles.
        
        Returns:
            dict: Dictionnaire des sources et leur disponibilité
        """
        return self.sources_available

# Créer une instance singleton pour l'accès global
_data_integration_hub = None

def get_data_integration_hub():
    """
    Récupère l'instance singleton du hub d'intégration de données.
    
    Returns:
        DataIntegrationHub: Instance du hub d'intégration de données
    """
    global _data_integration_hub
    
    if _data_integration_hub is None:
        logger.info("Initialisation du hub d'intégration de données global")
        _data_integration_hub = DataIntegrationHub()
        
    return _data_integration_hub

def enhance_match_data(match_data):
    """
    Enrichit les données d'un match avec toutes les sources disponibles.
    
    Args:
        match_data (dict): Données du match à enrichir
        
    Returns:
        dict: Données du match enrichies
    """
    hub = get_data_integration_hub()
    return hub.enhance_match_data(match_data)

def get_player_details(player_name, team_name=None):
    """
    Récupère des détails complets sur un joueur.
    
    Args:
        player_name (str): Nom du joueur
        team_name (str, optional): Nom de l'équipe pour faciliter l'identification
        
    Returns:
        dict: Détails complets sur le joueur
    """
    hub = get_data_integration_hub()
    return hub.get_player_details(player_name, team_name)

def get_team_details(team_name):
    """
    Récupère des détails complets sur une équipe.
    
    Args:
        team_name (str): Nom de l'équipe
        
    Returns:
        dict: Détails complets sur l'équipe
    """
    hub = get_data_integration_hub()
    return hub.get_team_details(team_name)

def get_league_standings(league_code, season=None):
    """
    Récupère le classement d'une ligue.
    
    Args:
        league_code (str): Code de la ligue
        season (str, optional): Saison (ex: "2023/2024")
        
    Returns:
        pd.DataFrame: Classement de la ligue
    """
    hub = get_data_integration_hub()
    return hub.get_league_standings(league_code, season)

def get_match_statistics(home_team, away_team, date=None, league_code=None):
    """
    Récupère les statistiques d'un match.
    
    Args:
        home_team (str): Nom de l'équipe à domicile
        away_team (str): Nom de l'équipe à l'extérieur
        date (str, optional): Date du match (format YYYY-MM-DD)
        league_code (str, optional): Code de la ligue
        
    Returns:
        dict: Statistiques du match
    """
    hub = get_data_integration_hub()
    return hub.get_match_statistics(home_team, away_team, date, league_code)

def is_source_available(source):
    """
    Vérifie si une source spécifique est disponible.
    
    Args:
        source (str): Nom de la source à vérifier
        
    Returns:
        bool: True si la source est disponible, False sinon
    """
    hub = get_data_integration_hub()
    return hub.is_source_available(source)

def get_available_sources():
    """
    Récupère la liste des sources disponibles.
    
    Returns:
        dict: Dictionnaire des sources et leur disponibilité
    """
    # Vérification simple des sources sans utiliser le hub (pour éviter la récursion)
    sources = {
        'transfermarkt': is_transfermarkt_available()
    }
    
    # Vérifier soccerdata si importé
    if SOCCERDATA_IMPORTED:
        try:
            import soccerdata
            sources['soccerdata'] = True
            # Ajouter des sources soccerdata basiques
            sources['soccerdata_fbref'] = True
            sources['soccerdata_espn'] = True
            sources['soccerdata_fotmob'] = True
        except ImportError:
            sources['soccerdata'] = False
    else:
        sources['soccerdata'] = False
    
    # Vérifier l'enrichissement de données joueur si importé
    if PLAYER_ENRICHMENT_IMPORTED:
        sources['player_enrichment'] = True
    else:
        sources['player_enrichment'] = False
    
    return sources