"""
Module d'intégration soccerdata pour ArcanShadow.
Ce module sert de point central pour l'accès aux 9 sources de données de soccerdata
par tous les onglets et méta-systèmes de l'application.

Sources disponibles:
- Club Elo
- ESPN
- FBref
- Football-Data.co.uk
- FotMob
- Sofascore
- SoFIFA
- Understat
- WhoScored
"""

import logging
import pandas as pd
import os
from datetime import datetime

# Importer soccerdata
try:
    import soccerdata as sd
    SOCCERDATA_AVAILABLE = True
except ImportError:
    SOCCERDATA_AVAILABLE = False

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mapping des codes de compétitions standardisés
COMPETITION_MAPPING = {
    "PL": "EPL",  # Premier League
    "BL1": "1. Bundesliga",  # Bundesliga
    "FL1": "Ligue 1",  # Ligue 1
    "SA": "Serie A",  # Serie A
    "PD": "La Liga",  # La Liga
    "PPL": "Liga Portugal",  # Primeira Liga
    "DED": "Eredivisie",  # Eredivisie
    "ELC": "Championship",  # EFL Championship
}

# Instances singleton des scrappers
_scrapers = {
    'fbref': None,
    'espn': None,
    'fotmob': None,
    'sofascore': None,
    'understat': None,
    'whoscored': None,
    'clubelo': None,
    'sofifa': None,
    'footballdata': None
}

class SoccerDataIntegration:
    """
    Classe principale pour l'intégration de soccerdata dans ArcanShadow.
    Cette classe fournit des méthodes pour accéder aux différentes sources
    et normaliser leurs données vers un format commun utilisable par ArcanShadow.
    """
    
    def __init__(self):
        """Initialise l'intégration soccerdata."""
        self.sources_available = self._check_sources_availability()
        # Chemin de mise en cache des données
        self.cache_dir = os.path.join(os.getcwd(), 'data', 'soccerdata_cache')
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _check_sources_availability(self):
        """
        Vérifie la disponibilité des différentes sources de soccerdata.
        
        Returns:
            dict: Dictionnaire indiquant la disponibilité de chaque source
        """
        sources_status = {}
        
        if not SOCCERDATA_AVAILABLE:
            logger.warning("Bibliothèque soccerdata non disponible")
            return {source: False for source in _scrapers.keys()}
        
        try:
            # Tester FBref (généralement la source la plus fiable)
            _scrapers['fbref'] = sd.FBref(leagues=["EPL"], seasons=["2024"])
            sources_status['fbref'] = True
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de FBref: {e}")
            sources_status['fbref'] = False
        
        try:
            # Tester ESPN
            _scrapers['espn'] = sd.ESPN(leagues=["EPL"], seasons=["2024"])
            sources_status['espn'] = True
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation d'ESPN: {e}")
            sources_status['espn'] = False
        
        try:
            # Tester FotMob
            _scrapers['fotmob'] = sd.FotMob(leagues=["EPL"], seasons=["2024"])
            sources_status['fotmob'] = True
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de FotMob: {e}")
            sources_status['fotmob'] = False
        
        try:
            # Tester Sofascore
            _scrapers['sofascore'] = sd.SofaScore(leagues=["EPL"], seasons=["2024"])
            sources_status['sofascore'] = True
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de Sofascore: {e}")
            sources_status['sofascore'] = False
        
        try:
            # Tester Understat
            _scrapers['understat'] = sd.Understat(leagues=["EPL"], seasons=["2024"])
            sources_status['understat'] = True
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation d'Understat: {e}")
            sources_status['understat'] = False
        
        try:
            # Tester WhoScored
            _scrapers['whoscored'] = sd.WhoScored(leagues=["EPL"], seasons=["2024"])
            sources_status['whoscored'] = True
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de WhoScored: {e}")
            sources_status['whoscored'] = False
        
        try:
            # Tester ClubElo
            _scrapers['clubelo'] = sd.ClubElo()
            sources_status['clubelo'] = True
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de ClubElo: {e}")
            sources_status['clubelo'] = False
        
        try:
            # Tester SoFIFA
            _scrapers['sofifa'] = sd.SoFIFA(leagues=["EPL"], seasons=["2024"])
            sources_status['sofifa'] = True
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de SoFIFA: {e}")
            sources_status['sofifa'] = False
        
        try:
            # Tester FootballData
            _scrapers['footballdata'] = sd.FootballData(leagues=["EPL"], seasons=["2023/2024"])
            sources_status['footballdata'] = True
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de FootballData: {e}")
            sources_status['footballdata'] = False
        
        return sources_status
    
    def get_scraper(self, source):
        """
        Récupère l'instance du scraper pour une source spécifique.
        
        Args:
            source (str): Nom de la source ('fbref', 'espn', etc.)
            
        Returns:
            object: Instance du scraper ou None si non disponible
        """
        if not SOCCERDATA_AVAILABLE:
            logger.warning(f"Bibliothèque soccerdata non disponible pour {source}")
            return None
        
        if not self.sources_available.get(source, False):
            logger.warning(f"Source {source} non disponible")
            return None
        
        return _scrapers.get(source)
    
    def get_league_standings(self, league_code, season=None, source='fbref'):
        """
        Récupère le classement d'une ligue spécifique.
        
        Args:
            league_code (str): Code de la ligue (format ArcanShadow)
            season (str, optional): Saison (ex: "2023/2024"). Par défaut, saison actuelle.
            source (str, optional): Source de données. Par défaut, 'fbref'.
            
        Returns:
            pd.DataFrame: Classement de la ligue
        """
        if not SOCCERDATA_AVAILABLE:
            logger.warning("Bibliothèque soccerdata non disponible")
            return pd.DataFrame()
        
        if not self.sources_available.get(source, False):
            logger.warning(f"Source {source} non disponible, tentative avec une autre source")
            # Essayer avec une autre source disponible
            for alt_source in ['fbref', 'espn', 'fotmob', 'sofascore']:
                if self.sources_available.get(alt_source, False):
                    source = alt_source
                    break
            else:
                logger.error("Aucune source alternative disponible")
                return pd.DataFrame()
        
        try:
            # Convertir le code de ligue ArcanShadow vers soccerdata
            sd_league = COMPETITION_MAPPING.get(league_code, league_code)
            
            # Déterminer la saison
            if not season:
                current_year = datetime.now().year
                if datetime.now().month >= 7:  # Après juillet, on considère la nouvelle saison
                    season = f"{current_year}/{current_year+1}"
                else:
                    season = f"{current_year-1}/{current_year}"
            
            # Adapter le format de saison selon la source
            if source in ['footballdata']:
                sd_season = season
            else:
                # La plupart des sources utilisent juste l'année de fin
                sd_season = season.split('/')[1]
            
            # Récupérer ou créer le scraper
            if _scrapers[source] is None or sd_league not in _scrapers[source].leagues or sd_season not in _scrapers[source].seasons:
                if source == 'footballdata':
                    _scrapers[source] = sd.FootballData(leagues=[sd_league], seasons=[sd_season])
                elif source == 'clubelo':
                    _scrapers[source] = sd.ClubElo()
                else:
                    scraper_class = getattr(sd, source.capitalize())
                    _scrapers[source] = scraper_class(leagues=[sd_league], seasons=[sd_season])
            
            # Récupérer les données
            if source in ['fbref', 'espn', 'fotmob', 'sofascore', 'understat', 'whoscored']:
                standings = _scrapers[source].read_league_table()
                
                # Normaliser les colonnes pour ArcanShadow
                if not standings.empty:
                    # Renommer les colonnes selon un format standard pour ArcanShadow
                    col_mapping = {
                        'team': 'team_name',
                        'position': 'position',
                        'games': 'played',
                        'points': 'points',
                        'wins': 'wins',
                        'draws': 'draws',
                        'losses': 'losses',
                        'goals_for': 'goals_scored',
                        'goals_against': 'goals_conceded'
                    }
                    
                    # Appliquer le mapping des colonnes disponibles
                    rename_dict = {col: col_mapping[col] for col in col_mapping if col in standings.columns}
                    if rename_dict:
                        standings = standings.rename(columns=rename_dict)
                    
                    # Ajouter des colonnes dérivées si nécessaires
                    if 'goal_diff' not in standings.columns and 'goals_scored' in standings.columns and 'goals_conceded' in standings.columns:
                        standings['goal_diff'] = standings['goals_scored'] - standings['goals_conceded']
                    
                    # Ajouter des métadonnées
                    standings['source'] = source
                    standings['league'] = league_code
                    standings['season'] = season
                
                return standings
            
            logger.warning(f"Fonction non implémentée pour la source {source}")
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du classement pour {league_code} via {source}: {e}")
            return pd.DataFrame()
    
    def get_team_players(self, team_name, season=None, source='fbref'):
        """
        Récupère les joueurs d'une équipe spécifique.
        
        Args:
            team_name (str): Nom de l'équipe
            season (str, optional): Saison (ex: "2023/2024"). Par défaut, saison actuelle.
            source (str, optional): Source de données. Par défaut, 'fbref'.
            
        Returns:
            pd.DataFrame: Liste des joueurs de l'équipe
        """
        if not SOCCERDATA_AVAILABLE:
            logger.warning("Bibliothèque soccerdata non disponible")
            return pd.DataFrame()
        
        if not self.sources_available.get(source, False):
            logger.warning(f"Source {source} non disponible, tentative avec une autre source")
            # Essayer avec une autre source disponible
            for alt_source in ['fbref', 'sofifa', 'sofascore', 'fotmob']:
                if self.sources_available.get(alt_source, False):
                    source = alt_source
                    break
            else:
                logger.error("Aucune source alternative disponible")
                return pd.DataFrame()
        
        try:
            # Déterminer la saison
            if not season:
                current_year = datetime.now().year
                if datetime.now().month >= 7:  # Après juillet, on considère la nouvelle saison
                    season = f"{current_year}/{current_year+1}"
                else:
                    season = f"{current_year-1}/{current_year}"
            
            # Adapter le format de saison selon la source
            if source in ['footballdata']:
                sd_season = season
            else:
                # La plupart des sources utilisent juste l'année de fin
                sd_season = season.split('/')[1]
            
            # Pour cette fonction, nous devons d'abord trouver la ligue de l'équipe
            # Parcourir les ligues principales
            leagues = ["EPL", "1. Bundesliga", "La Liga", "Serie A", "Ligue 1"]
            
            players_df = pd.DataFrame()
            
            for league in leagues:
                try:
                    # Créer un scraper pour cette ligue
                    if source == 'footballdata':
                        scraper = sd.FootballData(leagues=[league], seasons=[sd_season])
                    elif source == 'clubelo':
                        continue  # ClubElo n'a pas d'informations sur les joueurs
                    else:
                        scraper_class = getattr(sd, source.capitalize())
                        scraper = scraper_class(leagues=[league], seasons=[sd_season])
                    
                    # Vérifier si l'équipe est dans cette ligue
                    if source in ['fbref', 'sofifa', 'sofascore', 'fotmob']:
                        # Récupérer les informations des joueurs selon la source
                        if source == 'fbref':
                            try:
                                players = scraper.read_player_season_stats(stat_type='standard')
                                if not players.empty and 'team' in players.columns:
                                    # Filtrer par équipe (avec correspondance partielle)
                                    players = players[players['team'].str.contains(team_name, case=False, na=False)]
                                    if not players.empty:
                                        players_df = players
                                        break
                            except Exception as e:
                                logger.error(f"Erreur lors de la récupération des joueurs FBref pour {team_name}: {e}")
                        
                        elif source == 'sofifa':
                            try:
                                # SoFIFA a une structure différente
                                teams = scraper.read_teams()
                                if not teams.empty:
                                    team_id = teams[teams['name'].str.contains(team_name, case=False, na=False)]['team_id'].iloc[0]
                                    players = scraper.read_team_players(team_id)
                                    if not players.empty:
                                        players_df = players
                                        break
                            except Exception as e:
                                logger.error(f"Erreur lors de la récupération des joueurs SoFIFA pour {team_name}: {e}")
                except Exception as e:
                    logger.error(f"Erreur lors de la recherche de {team_name} dans {league} via {source}: {e}")
                    continue
            
            # Normaliser les colonnes pour ArcanShadow
            if not players_df.empty:
                # Renommer les colonnes selon un format standard pour ArcanShadow
                col_mapping = {
                    'name': 'player_name',
                    'full_name': 'player_name',
                    'player_name': 'player_name',
                    'age': 'age',
                    'nationality': 'nationality',
                    'position': 'position',
                    'foot': 'preferred_foot',
                    'height': 'height',
                    'weight': 'weight',
                    'shirt_number': 'shirt_number',
                    'jersey_number': 'shirt_number',
                    'value': 'market_value',
                    'team': 'team_name'
                }
                
                # Appliquer le mapping des colonnes disponibles
                rename_dict = {col: col_mapping[col] for col in col_mapping if col in players_df.columns}
                if rename_dict:
                    players_df = players_df.rename(columns=rename_dict)
                
                # Ajouter des métadonnées
                players_df['source'] = source
                players_df['team'] = team_name
                players_df['season'] = season
            
            return players_df
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des joueurs pour {team_name} via {source}: {e}")
            return pd.DataFrame()
    
    def get_match_statistics(self, home_team, away_team, date=None, league_code=None, season=None, source='fotmob'):
        """
        Récupère les statistiques d'un match spécifique.
        
        Args:
            home_team (str): Nom de l'équipe à domicile
            away_team (str): Nom de l'équipe à l'extérieur
            date (str, optional): Date du match (format YYYY-MM-DD). Si None, cherche les matchs récents.
            league_code (str, optional): Code de la ligue
            season (str, optional): Saison (ex: "2023/2024"). Par défaut, saison actuelle.
            source (str, optional): Source de données. Par défaut, 'fotmob'.
            
        Returns:
            dict: Statistiques du match
        """
        if not SOCCERDATA_AVAILABLE:
            logger.warning("Bibliothèque soccerdata non disponible")
            return {}
        
        if not self.sources_available.get(source, False):
            logger.warning(f"Source {source} non disponible, tentative avec une autre source")
            # Essayer avec une autre source disponible
            for alt_source in ['fotmob', 'sofascore', 'whoscored', 'fbref']:
                if self.sources_available.get(alt_source, False):
                    source = alt_source
                    break
            else:
                logger.error("Aucune source alternative disponible")
                return {}
        
        try:
            # Déterminer la saison
            if not season:
                current_year = datetime.now().year
                if datetime.now().month >= 7:  # Après juillet, on considère la nouvelle saison
                    season = f"{current_year}/{current_year+1}"
                else:
                    season = f"{current_year-1}/{current_year}"
            
            # Adapter le format de saison selon la source
            if source in ['footballdata']:
                sd_season = season
            else:
                # La plupart des sources utilisent juste l'année de fin
                sd_season = season.split('/')[1]
            
            # Déterminer la ligue si non spécifiée
            leagues_to_check = []
            if league_code:
                sd_league = COMPETITION_MAPPING.get(league_code, league_code)
                leagues_to_check = [sd_league]
            else:
                leagues_to_check = ["EPL", "1. Bundesliga", "La Liga", "Serie A", "Ligue 1"]
            
            match_stats = {}
            
            for league in leagues_to_check:
                try:
                    # Créer un scraper pour cette ligue
                    if source == 'footballdata':
                        continue  # FootballData n'a pas d'informations détaillées sur les matchs
                    elif source == 'clubelo':
                        continue  # ClubElo n'a pas d'informations sur les matchs
                    else:
                        scraper_class = getattr(sd, source.capitalize())
                        scraper = scraper_class(leagues=[league], seasons=[sd_season])
                    
                    # Récupérer les statistiques de match selon la source
                    if source in ['fotmob', 'sofascore', 'whoscored', 'fbref']:
                        try:
                            if source == 'fbref':
                                matches = scraper.read_schedule()
                                if not matches.empty:
                                    # Filtrer pour trouver le match spécifique
                                    match_filter = (
                                        (matches['home_team'].str.contains(home_team, case=False, na=False)) & 
                                        (matches['away_team'].str.contains(away_team, case=False, na=False))
                                    )
                                    if date:
                                        match_filter &= (matches['date'] == date)
                                    
                                    match_row = matches[match_filter]
                                    
                                    if not match_row.empty:
                                        match_id = match_row.iloc[0]['match_id']
                                        
                                        # Récupérer les stats du match
                                        try:
                                            stats = scraper.read_match_report(match_id)
                                            lineups = scraper.read_match_lineups(match_id)
                                            events = scraper.read_match_events(match_id)
                                            
                                            # Construire un dictionnaire normalisé pour ArcanShadow
                                            match_stats = {
                                                'match_id': match_id,
                                                'home_team': match_row.iloc[0]['home_team'],
                                                'away_team': match_row.iloc[0]['away_team'],
                                                'date': match_row.iloc[0]['date'],
                                                'league': league,
                                                'source': source,
                                                'statistics': stats.to_dict() if not stats.empty else {},
                                                'lineups': lineups.to_dict() if not lineups.empty else {},
                                                'events': events.to_dict() if not events.empty else {}
                                            }
                                            return match_stats
                                        except Exception as e:
                                            logger.error(f"Erreur lors de la récupération des détails du match {match_id}: {e}")
                            
                            elif source in ['fotmob', 'sofascore', 'whoscored']:
                                # Ces sources ont des fonctionnalités similaires
                                try:
                                    matches = scraper.read_schedule()
                                    if not matches.empty:
                                        match_filter = (
                                            (matches['home_team'].str.contains(home_team, case=False, na=False)) & 
                                            (matches['away_team'].str.contains(away_team, case=False, na=False))
                                        )
                                        if date:
                                            match_filter &= (matches['date'] == date)
                                        
                                        match_row = matches[match_filter]
                                        
                                        if not match_row.empty:
                                            match_id = match_row.iloc[0]['match_id']
                                            
                                            # Le format des stats varie selon la source
                                            match_data = {}
                                            
                                            if source == 'fotmob':
                                                match_data = scraper.read_match_facts(match_id)
                                            elif source == 'sofascore':
                                                match_data = scraper.read_match_report(match_id)
                                            elif source == 'whoscored':
                                                match_data = scraper.read_match_report(match_id)
                                            
                                            # Construire un dictionnaire normalisé
                                            match_stats = {
                                                'match_id': match_id,
                                                'home_team': match_row.iloc[0]['home_team'],
                                                'away_team': match_row.iloc[0]['away_team'],
                                                'date': match_row.iloc[0]['date'],
                                                'league': league,
                                                'source': source,
                                                'data': match_data.to_dict() if not match_data.empty else {}
                                            }
                                            return match_stats
                                except Exception as e:
                                    logger.error(f"Erreur lors de la récupération des matchs via {source}: {e}")
                        except Exception as e:
                            logger.error(f"Erreur lors de l'accès aux données de match {home_team} vs {away_team} via {source}: {e}")
                except Exception as e:
                    logger.error(f"Erreur lors de l'initialisation du scraper {source} pour {league}: {e}")
                    continue
            
            return match_stats
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats du match {home_team} vs {away_team}: {e}")
            return {}
    
    def get_team_form(self, team_name, last_n_matches=5, league_code=None, season=None, source='fbref'):
        """
        Récupère la forme récente d'une équipe (résultats des derniers matchs).
        
        Args:
            team_name (str): Nom de l'équipe
            last_n_matches (int, optional): Nombre de derniers matchs à considérer. Par défaut, 5.
            league_code (str, optional): Code de la ligue
            season (str, optional): Saison (ex: "2023/2024"). Par défaut, saison actuelle.
            source (str, optional): Source de données. Par défaut, 'fbref'.
            
        Returns:
            pd.DataFrame: Données de forme de l'équipe
        """
        if not SOCCERDATA_AVAILABLE:
            logger.warning("Bibliothèque soccerdata non disponible")
            return pd.DataFrame()
        
        if not self.sources_available.get(source, False):
            logger.warning(f"Source {source} non disponible, tentative avec une autre source")
            # Essayer avec une autre source disponible
            for alt_source in ['fbref', 'fotmob', 'sofascore']:
                if self.sources_available.get(alt_source, False):
                    source = alt_source
                    break
            else:
                logger.error("Aucune source alternative disponible")
                return pd.DataFrame()
        
        try:
            # Déterminer la saison
            if not season:
                current_year = datetime.now().year
                if datetime.now().month >= 7:  # Après juillet, on considère la nouvelle saison
                    season = f"{current_year}/{current_year+1}"
                else:
                    season = f"{current_year-1}/{current_year}"
            
            # Adapter le format de saison selon la source
            if source in ['footballdata']:
                sd_season = season
            else:
                # La plupart des sources utilisent juste l'année de fin
                sd_season = season.split('/')[1]
            
            # Déterminer la ligue si non spécifiée
            leagues_to_check = []
            if league_code:
                sd_league = COMPETITION_MAPPING.get(league_code, league_code)
                leagues_to_check = [sd_league]
            else:
                leagues_to_check = ["EPL", "1. Bundesliga", "La Liga", "Serie A", "Ligue 1"]
            
            for league in leagues_to_check:
                try:
                    # Créer un scraper pour cette ligue
                    if source == 'footballdata':
                        scraper = sd.FootballData(leagues=[league], seasons=[sd_season])
                    elif source == 'clubelo':
                        continue  # ClubElo n'a pas d'informations sur les matchs
                    else:
                        scraper_class = getattr(sd, source.capitalize())
                        scraper = scraper_class(leagues=[league], seasons=[sd_season])
                    
                    # Récupérer le calendrier des matchs
                    if source in ['fbref', 'fotmob', 'sofascore']:
                        try:
                            matches = scraper.read_schedule()
                            if not matches.empty:
                                # Filtrer les matchs de cette équipe
                                team_matches = matches[
                                    (matches['home_team'].str.contains(team_name, case=False, na=False)) | 
                                    (matches['away_team'].str.contains(team_name, case=False, na=False))
                                ]
                                
                                if not team_matches.empty:
                                    # Trier par date (du plus récent au plus ancien)
                                    team_matches = team_matches.sort_values(by='date', ascending=False)
                                    
                                    # Limiter au nombre de matchs demandés
                                    team_matches = team_matches.head(last_n_matches)
                                    
                                    # Ajouter une colonne pour le résultat du point de vue de l'équipe
                                    def determine_result(row):
                                        if row['home_team'].lower() in team_name.lower() or team_name.lower() in row['home_team'].lower():
                                            # L'équipe joue à domicile
                                            if row['home_score'] > row['away_score']:
                                                return 'W'  # Victoire
                                            elif row['home_score'] < row['away_score']:
                                                return 'L'  # Défaite
                                            else:
                                                return 'D'  # Match nul
                                        else:
                                            # L'équipe joue à l'extérieur
                                            if row['away_score'] > row['home_score']:
                                                return 'W'  # Victoire
                                            elif row['away_score'] < row['home_score']:
                                                return 'L'  # Défaite
                                            else:
                                                return 'D'  # Match nul
                                    
                                    # Appliquer la fonction pour déterminer le résultat
                                    if 'home_score' in team_matches.columns and 'away_score' in team_matches.columns:
                                        team_matches['result'] = team_matches.apply(determine_result, axis=1)
                                    
                                    # Ajouter des métadonnées
                                    team_matches['source'] = source
                                    team_matches['team'] = team_name
                                    
                                    return team_matches
                        except Exception as e:
                            logger.error(f"Erreur lors de la récupération de la forme de {team_name} via {source}: {e}")
                except Exception as e:
                    logger.error(f"Erreur lors de l'initialisation du scraper {source} pour {league}: {e}")
                    continue
            
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la forme de {team_name}: {e}")
            return pd.DataFrame()
    
    def get_team_elo_rating(self, team_name):
        """
        Récupère le classement Elo d'une équipe spécifique.
        
        Args:
            team_name (str): Nom de l'équipe
            
        Returns:
            float: Classement Elo de l'équipe ou None si non disponible
        """
        if not SOCCERDATA_AVAILABLE:
            logger.warning("Bibliothèque soccerdata non disponible")
            return None
        
        if not self.sources_available.get('clubelo', False):
            logger.warning("Source ClubElo non disponible")
            return None
        
        try:
            scraper = self.get_scraper('clubelo')
            
            # Récupérer les données Elo complètes
            elo_data = scraper.read_by_date()
            
            if not elo_data.empty and 'Club' in elo_data.columns:
                # Chercher l'équipe (match partiel)
                team_data = elo_data[elo_data['Club'].str.contains(team_name, case=False, na=False)]
                
                if not team_data.empty:
                    # Récupérer le classement Elo le plus récent
                    latest_elo = team_data.iloc[0]['Elo']
                    return latest_elo
            
            return None
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du classement Elo pour {team_name}: {e}")
            return None
    
    def get_team_stats(self, team_name, stat_type='standard', league_code=None, season=None, source='fbref'):
        """
        Récupère les statistiques d'équipe pour une saison spécifique.
        
        Args:
            team_name (str): Nom de l'équipe
            stat_type (str, optional): Type de statistiques ('standard', 'shooting', 'passing', etc.). Par défaut, 'standard'.
            league_code (str, optional): Code de la ligue
            season (str, optional): Saison (ex: "2023/2024"). Par défaut, saison actuelle.
            source (str, optional): Source de données. Par défaut, 'fbref'.
            
        Returns:
            pd.DataFrame: Statistiques de l'équipe
        """
        if not SOCCERDATA_AVAILABLE:
            logger.warning("Bibliothèque soccerdata non disponible")
            return pd.DataFrame()
        
        if not self.sources_available.get(source, False):
            logger.warning(f"Source {source} non disponible, tentative avec une autre source")
            # Essayer avec une autre source disponible
            for alt_source in ['fbref', 'fotmob', 'sofascore', 'whoscored']:
                if self.sources_available.get(alt_source, False):
                    source = alt_source
                    break
            else:
                logger.error("Aucune source alternative disponible")
                return pd.DataFrame()
        
        try:
            # Déterminer la saison
            if not season:
                current_year = datetime.now().year
                if datetime.now().month >= 7:  # Après juillet, on considère la nouvelle saison
                    season = f"{current_year}/{current_year+1}"
                else:
                    season = f"{current_year-1}/{current_year}"
            
            # Adapter le format de saison selon la source
            if source in ['footballdata']:
                sd_season = season
            else:
                # La plupart des sources utilisent juste l'année de fin
                sd_season = season.split('/')[1]
            
            # Déterminer la ligue si non spécifiée
            leagues_to_check = []
            if league_code:
                sd_league = COMPETITION_MAPPING.get(league_code, league_code)
                leagues_to_check = [sd_league]
            else:
                leagues_to_check = ["EPL", "1. Bundesliga", "La Liga", "Serie A", "Ligue 1"]
            
            for league in leagues_to_check:
                try:
                    # Créer un scraper pour cette ligue
                    if source == 'footballdata':
                        continue  # FootballData n'a pas d'informations détaillées sur les équipes
                    elif source == 'clubelo':
                        continue  # ClubElo n'a pas d'informations détaillées sur les équipes
                    else:
                        scraper_class = getattr(sd, source.capitalize())
                        scraper = scraper_class(leagues=[league], seasons=[sd_season])
                    
                    # Récupérer les statistiques d'équipe selon la source
                    if source == 'fbref':
                        try:
                            # FBref a différents types de statistiques
                            if stat_type == 'standard':
                                stats = scraper.read_team_season_stats(stat_type='standard')
                            elif stat_type == 'shooting':
                                stats = scraper.read_team_season_stats(stat_type='shooting')
                            elif stat_type == 'passing':
                                stats = scraper.read_team_season_stats(stat_type='passing')
                            elif stat_type == 'defense':
                                stats = scraper.read_team_season_stats(stat_type='defense')
                            elif stat_type == 'possession':
                                stats = scraper.read_team_season_stats(stat_type='possession')
                            else:
                                stats = scraper.read_team_season_stats(stat_type='standard')
                            
                            if not stats.empty and 'team' in stats.columns:
                                # Filtrer pour l'équipe spécifique
                                team_stats = stats[stats['team'].str.contains(team_name, case=False, na=False)]
                                
                                if not team_stats.empty:
                                    # Ajouter des métadonnées
                                    team_stats['source'] = source
                                    team_stats['league'] = league
                                    team_stats['season'] = season
                                    
                                    return team_stats
                        except Exception as e:
                            logger.error(f"Erreur lors de la récupération des stats {stat_type} pour {team_name} via FBref: {e}")
                    
                    elif source in ['fotmob', 'sofascore', 'whoscored']:
                        try:
                            # Ces sources ont des fonctionnalités différentes pour les stats d'équipe
                            if source == 'fotmob':
                                # Pour FotMob, on doit d'abord trouver l'ID de l'équipe
                                teams = scraper.read_league_table()
                                if not teams.empty and 'team' in teams.columns:
                                    team_row = teams[teams['team'].str.contains(team_name, case=False, na=False)]
                                    if not team_row.empty and 'team_id' in team_row.columns:
                                        team_id = team_row.iloc[0]['team_id']
                                        # Récupérer les stats de l'équipe (si disponible dans la source)
                                        # FotMob peut ne pas avoir cette fonctionnalité directement
                                        pass
                            
                            elif source == 'sofascore':
                                # Pour Sofascore, approche similaire
                                teams = scraper.read_league_table()
                                if not teams.empty and 'team' in teams.columns:
                                    team_row = teams[teams['team'].str.contains(team_name, case=False, na=False)]
                                    if not team_row.empty and 'team_id' in team_row.columns:
                                        team_id = team_row.iloc[0]['team_id']
                                        # Récupérer les stats de l'équipe (si disponible)
                                        pass
                            
                            elif source == 'whoscored':
                                # WhoScored a plus de détails
                                teams = scraper.read_teams()
                                if not teams.empty and 'name' in teams.columns:
                                    team_row = teams[teams['name'].str.contains(team_name, case=False, na=False)]
                                    if not team_row.empty and 'team_id' in team_row.columns:
                                        team_id = team_row.iloc[0]['team_id']
                                        # WhoScored peut avoir des stats d'équipe plus détaillées
                                        # mais cela dépend de l'implémentation actuelle de soccerdata
                                        pass
                        except Exception as e:
                            logger.error(f"Erreur lors de la récupération des stats d'équipe pour {team_name} via {source}: {e}")
                except Exception as e:
                    logger.error(f"Erreur lors de l'initialisation du scraper {source} pour {league}: {e}")
                    continue
            
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats d'équipe pour {team_name}: {e}")
            return pd.DataFrame()
    
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
    
    def get_available_leagues(self, source='fbref'):
        """
        Récupère la liste des ligues disponibles pour une source.
        
        Args:
            source (str, optional): Source de données. Par défaut, 'fbref'.
            
        Returns:
            list: Liste des ligues disponibles
        """
        if not SOCCERDATA_AVAILABLE:
            logger.warning("Bibliothèque soccerdata non disponible")
            return []
        
        if not self.sources_available.get(source, False):
            logger.warning(f"Source {source} non disponible")
            return []
        
        try:
            if source == 'fbref':
                return ["EPL", "1. Bundesliga", "La Liga", "Serie A", "Ligue 1", "Eredivisie", "Liga Portugal", "Championship"]
            elif source == 'espn':
                return ["EPL", "1. Bundesliga", "La Liga", "Serie A", "Ligue 1", "Eredivisie", "Liga MX"]
            elif source == 'fotmob':
                return ["EPL", "1. Bundesliga", "La Liga", "Serie A", "Ligue 1", "Eredivisie", "Liga Portugal", "Championship"]
            elif source == 'sofascore':
                return ["EPL", "1. Bundesliga", "La Liga", "Serie A", "Ligue 1", "Eredivisie", "Liga Portugal", "Championship"]
            elif source == 'understat':
                return ["EPL", "1. Bundesliga", "La Liga", "Serie A", "Ligue 1", "RFPL"]
            elif source == 'whoscored':
                return ["EPL", "1. Bundesliga", "La Liga", "Serie A", "Ligue 1", "Eredivisie", "Liga Portugal", "Championship"]
            elif source == 'sofifa':
                return ["EPL", "1. Bundesliga", "La Liga", "Serie A", "Ligue 1", "Eredivisie", "Liga Portugal", "Championship"]
            elif source == 'footballdata':
                return ["E0", "D1", "I1", "SP1", "F1", "N1", "P1", "E1"]
            else:
                return []
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des ligues disponibles pour {source}: {e}")
            return []
    
    def get_player_detailed_stats(self, player_name, team_name=None, league_code=None, season=None, source='fbref'):
        """
        Récupère les statistiques détaillées d'un joueur spécifique.
        
        Args:
            player_name (str): Nom du joueur
            team_name (str, optional): Nom de l'équipe pour aider à identifier le joueur
            league_code (str, optional): Code de la ligue
            season (str, optional): Saison (ex: "2023/2024"). Par défaut, saison actuelle.
            source (str, optional): Source de données. Par défaut, 'fbref'.
            
        Returns:
            pd.DataFrame: Statistiques détaillées du joueur
        """
        if not SOCCERDATA_AVAILABLE:
            logger.warning("Bibliothèque soccerdata non disponible")
            return pd.DataFrame()
        
        if not self.sources_available.get(source, False):
            logger.warning(f"Source {source} non disponible, tentative avec une autre source")
            # Essayer avec une autre source disponible
            for alt_source in ['fbref', 'sofifa', 'sofascore', 'whoscored']:
                if self.sources_available.get(alt_source, False):
                    source = alt_source
                    break
            else:
                logger.error("Aucune source alternative disponible")
                return pd.DataFrame()
        
        try:
            # Déterminer la saison
            if not season:
                current_year = datetime.now().year
                if datetime.now().month >= 7:  # Après juillet, on considère la nouvelle saison
                    season = f"{current_year}/{current_year+1}"
                else:
                    season = f"{current_year-1}/{current_year}"
            
            # Adapter le format de saison selon la source
            if source in ['footballdata']:
                sd_season = season
            else:
                # La plupart des sources utilisent juste l'année de fin
                sd_season = season.split('/')[1]
            
            # Déterminer la ligue si non spécifiée
            leagues_to_check = []
            if league_code:
                sd_league = COMPETITION_MAPPING.get(league_code, league_code)
                leagues_to_check = [sd_league]
            else:
                leagues_to_check = ["EPL", "1. Bundesliga", "La Liga", "Serie A", "Ligue 1"]
            
            for league in leagues_to_check:
                try:
                    # Créer un scraper pour cette ligue
                    if source == 'footballdata':
                        continue  # FootballData n'a pas d'informations sur les joueurs
                    elif source == 'clubelo':
                        continue  # ClubElo n'a pas d'informations sur les joueurs
                    else:
                        scraper_class = getattr(sd, source.capitalize())
                        scraper = scraper_class(leagues=[league], seasons=[sd_season])
                    
                    # Récupérer les statistiques du joueur selon la source
                    if source == 'fbref':
                        try:
                            # FBref a différents types de statistiques pour les joueurs
                            # Commencer par les statistiques standard
                            stats_standard = scraper.read_player_season_stats(stat_type='standard')
                            
                            if not stats_standard.empty and 'player' in stats_standard.columns:
                                # Filtrer pour le joueur spécifique
                                player_filter = stats_standard['player'].str.contains(player_name, case=False, na=False)
                                
                                # Ajouter un filtre d'équipe si spécifié
                                if team_name and 'team' in stats_standard.columns:
                                    player_filter &= stats_standard['team'].str.contains(team_name, case=False, na=False)
                                
                                player_stats = stats_standard[player_filter]
                                
                                if not player_stats.empty:
                                    # Récupérer des statistiques supplémentaires pour enrichir les données
                                    try:
                                        # Statistiques de tir
                                        stats_shooting = scraper.read_player_season_stats(stat_type='shooting')
                                        if not stats_shooting.empty:
                                            player_shooting = stats_shooting[player_filter]
                                            if not player_shooting.empty:
                                                # Fusionner les statistiques
                                                for col in player_shooting.columns:
                                                    if col not in player_stats.columns:
                                                        player_stats[col] = player_shooting[col].values
                                    except Exception:
                                        pass
                                    
                                    try:
                                        # Statistiques de passes
                                        stats_passing = scraper.read_player_season_stats(stat_type='passing')
                                        if not stats_passing.empty:
                                            player_passing = stats_passing[player_filter]
                                            if not player_passing.empty:
                                                # Fusionner les statistiques
                                                for col in player_passing.columns:
                                                    if col not in player_stats.columns:
                                                        player_stats[col] = player_passing[col].values
                                    except Exception:
                                        pass
                                    
                                    # Ajouter des métadonnées
                                    player_stats['source'] = source
                                    player_stats['league'] = league
                                    player_stats['season'] = season
                                    
                                    return player_stats
                        except Exception as e:
                            logger.error(f"Erreur lors de la récupération des stats du joueur {player_name} via FBref: {e}")
                    
                    elif source == 'sofifa':
                        try:
                            # Pour SoFIFA, nous devons d'abord trouver l'équipe, puis le joueur
                            if team_name:
                                teams = scraper.read_teams()
                                if not teams.empty and 'name' in teams.columns:
                                    team_row = teams[teams['name'].str.contains(team_name, case=False, na=False)]
                                    if not team_row.empty and 'team_id' in team_row.columns:
                                        team_id = team_row.iloc[0]['team_id']
                                        # Récupérer les joueurs de l'équipe
                                        players = scraper.read_team_players(team_id)
                                        if not players.empty and 'name' in players.columns:
                                            player_row = players[players['name'].str.contains(player_name, case=False, na=False)]
                                            if not player_row.empty:
                                                # Ajouter des métadonnées
                                                player_row['source'] = source
                                                player_row['league'] = league
                                                player_row['season'] = season
                                                player_row['team'] = team_name
                                                
                                                return player_row
                        except Exception as e:
                            logger.error(f"Erreur lors de la récupération des stats du joueur {player_name} via SoFIFA: {e}")
                    
                    # D'autres sources pourraient nécessiter des implémentations spécifiques
                    # WhoScored et Sofascore ont des données riches sur les joueurs
                    
                except Exception as e:
                    logger.error(f"Erreur lors de l'initialisation du scraper {source} pour {league}: {e}")
                    continue
            
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats détaillées pour {player_name}: {e}")
            return pd.DataFrame()

# Créer une instance singleton pour l'accès global
_soccer_data_integration = None

def get_soccer_data_integration():
    """
    Récupère l'instance singleton d'intégration soccerdata.
    
    Returns:
        SoccerDataIntegration: Instance d'intégration soccerdata
    """
    global _soccer_data_integration
    
    if _soccer_data_integration is None:
        logger.info("Initialisation de l'intégration soccerdata globale")
        _soccer_data_integration = SoccerDataIntegration()
        
    return _soccer_data_integration

def is_soccerdata_available():
    """
    Vérifie si soccerdata est disponible.
    
    Returns:
        bool: True si soccerdata est disponible, False sinon
    """
    return SOCCERDATA_AVAILABLE

def get_available_sources():
    """
    Récupère la liste des sources disponibles dans soccerdata.
    
    Returns:
        dict: Dictionnaire des sources et leur disponibilité
    """
    integration = get_soccer_data_integration()
    return integration.get_available_sources()

def enhance_match_data_with_soccerdata(match_data):
    """
    Enrichit les données d'un match avec des informations de soccerdata.
    
    Args:
        match_data (dict): Données du match à enrichir
        
    Returns:
        dict: Données du match enrichies
    """
    if not is_soccerdata_available():
        logger.warning("Bibliothèque soccerdata non disponible pour l'enrichissement des données de match")
        return match_data
    
    # Créer une copie des données pour éviter de modifier l'original
    enhanced_data = match_data.copy()
    integration = get_soccer_data_integration()
    
    try:
        # Extraire les informations clés du match
        home_team = match_data.get('home_team')
        away_team = match_data.get('away_team')
        match_date = match_data.get('date')
        league_code = match_data.get('league_code')
        
        if home_team and away_team:
            # Essayer de récupérer des statistiques de match via soccerdata
            sources_to_try = ['fotmob', 'sofascore', 'fbref', 'whoscored']
            match_stats = {}
            
            for source in sources_to_try:
                if integration.is_source_available(source):
                    match_stats = integration.get_match_statistics(
                        home_team=home_team,
                        away_team=away_team,
                        date=match_date,
                        league_code=league_code,
                        source=source
                    )
                    
                    if match_stats:
                        logger.info(f"Données de match récupérées via {source} pour {home_team} vs {away_team}")
                        break
            
            if match_stats:
                enhanced_data['soccerdata_match_stats'] = match_stats
            
            # Essayer de récupérer la forme récente des équipes
            home_form = integration.get_team_form(home_team, league_code=league_code)
            if not home_form.empty:
                enhanced_data['home_team_form'] = home_form.to_dict()
                logger.info(f"Forme récente récupérée pour {home_team}")
            
            away_form = integration.get_team_form(away_team, league_code=league_code)
            if not away_form.empty:
                enhanced_data['away_team_form'] = away_form.to_dict()
                logger.info(f"Forme récente récupérée pour {away_team}")
            
            # Essayer de récupérer le classement Elo des équipes
            if integration.is_source_available('clubelo'):
                home_elo = integration.get_team_elo_rating(home_team)
                if home_elo:
                    enhanced_data['home_team_elo'] = home_elo
                    logger.info(f"Classement Elo récupéré pour {home_team}: {home_elo}")
                
                away_elo = integration.get_team_elo_rating(away_team)
                if away_elo:
                    enhanced_data['away_team_elo'] = away_elo
                    logger.info(f"Classement Elo récupéré pour {away_team}: {away_elo}")
    
    except Exception as e:
        logger.error(f"Erreur lors de l'enrichissement des données avec soccerdata: {e}")
    
    return enhanced_data