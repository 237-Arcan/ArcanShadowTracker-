"""
FlashScraper - Module de récupération de données depuis Flashscore
Ce module permet de collecter des statistiques détaillées, des cotes, des tendances,
des compositions d'équipes et des statistiques avancées pour alimenter le système
de prédiction ArcanShadow.
"""

import time
import random
import json
import re
import pandas as pd
from datetime import datetime, timedelta
import requests
from trafilatura import fetch_url, extract
from bs4 import BeautifulSoup
import logging
from .cache_manager import CacheManager

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('flash_scraper')

class FlashScraper:
    """
    Module de scraping spécialisé pour Flashscore.
    Collecte les matchs, statistiques, cotes et tendances.
    """
    def __init__(self, delay_range=(1, 3)):
        """
        Initialise le scraper avec des paramètres de base.
        
        Args:
            delay_range (tuple): Plage de délai entre les requêtes (min, max) en secondes
        """
        self.base_url = "https://www.flashscore.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        self.delay_range = delay_range
        
        # Initialiser le gestionnaire de cache
        self.cache_manager = CacheManager()
        
        # Durées de cache par défaut (en secondes)
        self.cache_durations = {
            'matches_of_day': 3 * 60 * 60,      # 3 heures pour les matchs du jour
            'match_details': 12 * 60 * 60,      # 12 heures pour les détails d'un match
            'team_form': 6 * 60 * 60,           # 6 heures pour la forme d'une équipe
            'odds_movement': 30 * 60,           # 30 minutes pour les mouvements de cotes
            'match_stats': 24 * 60 * 60,        # 24 heures pour les statistiques d'un match
            'match_lineups': 12 * 60 * 60       # 12 heures pour les compositions d'équipes
        }
        
    def _random_delay(self):
        """Introduit un délai aléatoire pour éviter la détection"""
        time.sleep(random.uniform(*self.delay_range))
        
    def get_matches_of_day(self, sport="football", date=None):
        """
        Récupère tous les matchs du jour pour un sport donné.
        
        Args:
            sport (str): Le sport à scraper (default: football)
            date (str): Date au format YYYYMMDD (default: aujourd'hui)
            
        Returns:
            list: Liste des matchs avec leurs détails de base
        """
        if date is None:
            date = datetime.now().strftime('%Y%m%d')
        elif isinstance(date, datetime) or hasattr(date, 'strftime'):
            date = date.strftime('%Y%m%d')
            
        # Clé de cache
        cache_key = f"flash_matches_{sport}_{date}"
        
        # Essaie de récupérer les données du cache
        cached_data = self.cache_manager.get(cache_key, 'flash_scraper')
        if cached_data:
            logger.info(f"Utilisation des données en cache pour les matchs de {sport} du {date}")
            return cached_data
            
        url = f"{self.base_url}/{sport}/{date}/"
        
        try:
            # Utiliser requests à la place de fetch_url pour avoir plus de contrôle sur les headers
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                logger.warning(f"Impossible de récupérer les matchs du jour. Code: {response.status_code}")
                return []
                
            # Extraction du contenu principal
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Recherche des éléments de matchs
            matches = []
            match_elements = soup.select('div.event__match')
            
            for match in match_elements:
                try:
                    match_id = match.get('id', '')
                    if match_id:
                        match_id = match_id.replace('g_1_', '')
                    
                    # Équipes
                    home_team_elem = match.select_one('div.event__participant--home')
                    away_team_elem = match.select_one('div.event__participant--away')
                    
                    home_team = home_team_elem.text.strip() if home_team_elem else "Unknown"
                    away_team = away_team_elem.text.strip() if away_team_elem else "Unknown"
                    
                    # Heure du match
                    time_element = match.select_one('div.event__time')
                    match_time = time_element.text.strip() if time_element else "N/A"
                    
                    # Statut du match (à venir, en cours, terminé)
                    status_element = match.select_one('div.event__stage')
                    status = status_element.text.strip() if status_element else "N/A"
                    
                    # Compétition
                    league_element = match.select_one('span.event__title--name')
                    league = league_element.text.strip() if league_element else "N/A"
                    
                    matches.append({
                        'id': match_id,
                        'home_team': home_team,
                        'away_team': away_team,
                        'time': match_time,
                        'status': status,
                        'league': league,
                        'date': date
                    })
                except Exception as e:
                    logger.error(f"Erreur lors de l'extraction du match: {e}")
                    continue
            
            # Mettre en cache les résultats si des matchs sont trouvés
            if matches:
                self.cache_manager.set(
                    cache_key, 
                    matches, 
                    'flash_scraper', 
                    self.cache_durations.get('matches_of_day')
                )
                logger.info(f"Mise en cache des données pour les matchs de {sport} du {date}")
            
            return matches
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des matchs: {e}")
            return []
            
        finally:
            self._random_delay()
    
    def get_match_details(self, match_id):
        """
        Récupère les détails complets d'un match spécifique.
        
        Args:
            match_id (str): Identifiant unique du match
            
        Returns:
            dict: Détails complets du match
        """
        # Clé de cache
        cache_key = f"match_details_{match_id}"
        
        # Essaie de récupérer les données du cache
        cached_data = self.cache_manager.get(cache_key, 'flash_scraper')
        if cached_data:
            logger.info(f"Utilisation des données en cache pour les détails du match {match_id}")
            return cached_data
        
        url = f"{self.base_url}/match/{match_id}/"
        
        try:
            # Utiliser requests à la place de fetch_url
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                logger.warning(f"Impossible de récupérer les détails du match {match_id}. Code: {response.status_code}")
                return {}
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraire les informations de base
            match_details = {}
            
            # Récupérer les équipes
            home_team_elem = soup.select_one('div.participant__participantName--home')
            away_team_elem = soup.select_one('div.participant__participantName--away')
            
            match_details['home_team'] = home_team_elem.text.strip() if home_team_elem else "Unknown"
            match_details['away_team'] = away_team_elem.text.strip() if away_team_elem else "Unknown"
            
            # Récupérer le score (si le match est terminé ou en cours)
            score_elem = soup.select_one('div.detailScore__wrapper')
            if score_elem:
                home_score_elem = score_elem.select_one('span.detailScore__home')
                away_score_elem = score_elem.select_one('span.detailScore__away')
                
                home_score = home_score_elem.text.strip() if home_score_elem else "0"
                away_score = away_score_elem.text.strip() if away_score_elem else "0"
                
                match_details['score'] = f"{home_score}-{away_score}"
            
            # Récupérer la date et l'heure
            date_elem = soup.select_one('div.duelParticipant__startTime')
            if date_elem:
                date_text = date_elem.text.strip()
                match_details['date_time'] = date_text
                
                # Séparer la date et l'heure
                try:
                    date_parts = date_text.split(' ')
                    if len(date_parts) >= 2:
                        match_details['date'] = date_parts[0]
                        match_details['time'] = date_parts[1]
                except:
                    pass
            
            # Récupérer la ligue
            league_elem = soup.select_one('span.tournamentHeader__country')
            if league_elem:
                match_details['league'] = league_elem.text.strip()
            
            # Récupérer le statut
            status_elem = soup.select_one('div.detailScore__status')
            if status_elem:
                match_details['status'] = status_elem.text.strip()
            
            # Ajouter l'ID du match
            match_details['id'] = match_id
            
            # Mettre en cache les résultats si des détails sont trouvés
            if match_details:
                self.cache_manager.set(
                    cache_key, 
                    match_details, 
                    'flash_scraper', 
                    self.cache_durations.get('match_details')
                )
                logger.info(f"Mise en cache des détails du match {match_id}")
            
            return match_details
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des détails du match: {e}")
            return {}
            
        finally:
            self._random_delay()
    
    def get_team_form(self, team_id, num_matches=5):
        """
        Récupère la forme récente d'une équipe.
        
        Args:
            team_id (str): Identifiant de l'équipe
            num_matches (int): Nombre de matchs récents à récupérer
            
        Returns:
            list: Liste des matchs récents
        """
        url = f"{self.base_url}/team/{team_id}/results/"
        
        try:
            # Utiliser requests à la place de fetch_url
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                logger.warning(f"Impossible de récupérer la forme de l'équipe {team_id}. Code: {response.status_code}")
                return []
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Récupérer le nom de l'équipe
            team_name_elem = soup.select_one('div.heading__name')
            team_name = team_name_elem.text.strip() if team_name_elem else "Unknown"
            
            # Récupérer les matchs récents
            recent_matches = []
            match_elems = soup.select('div.event__match')
            
            for i, match_elem in enumerate(match_elems):
                if i >= num_matches:
                    break
                
                try:
                    # ID du match
                    match_id = match_elem.get('id', '')
                    if match_id:
                        match_id = match_id.replace('g_1_', '')
                    
                    # Équipes
                    home_team_elem = match_elem.select_one('div.event__participant--home')
                    away_team_elem = match_elem.select_one('div.event__participant--away')
                    
                    home_team = home_team_elem.text.strip() if home_team_elem else "Unknown"
                    away_team = away_team_elem.text.strip() if away_team_elem else "Unknown"
                    
                    # Score
                    score_elem = match_elem.select_one('div.event__scores')
                    score = score_elem.text.strip().replace(' ', '') if score_elem else "0-0"
                    
                    # Date
                    date_elem = match_elem.select_one('div.event__time')
                    date = date_elem.text.strip() if date_elem else "Unknown"
                    
                    # Ligue
                    league_elem = match_elem.select_one('div.event__title--name')
                    league = league_elem.text.strip() if league_elem else "Unknown"
                    
                    # Déterminer le résultat du point de vue de l'équipe
                    result = ''
                    if '-' in score:
                        try:
                            home_score, away_score = score.split('-')
                            home_score = int(home_score)
                            away_score = int(away_score)
                            
                            if home_team == team_name:
                                if home_score > away_score:
                                    result = 'W'
                                elif home_score < away_score:
                                    result = 'L'
                                else:
                                    result = 'D'
                            else:
                                if away_score > home_score:
                                    result = 'W'
                                elif away_score < home_score:
                                    result = 'L'
                                else:
                                    result = 'D'
                        except:
                            result = '?'
                    
                    recent_matches.append({
                        'id': match_id,
                        'home_team': home_team,
                        'away_team': away_team,
                        'score': score,
                        'date': date,
                        'league': league,
                        'result': result
                    })
                    
                except Exception as e:
                    logger.error(f"Erreur lors de l'extraction d'un match récent: {e}")
                    continue
            
            return recent_matches
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la forme de l'équipe: {e}")
            return []
            
        finally:
            self._random_delay()
    
    def get_odds_movement(self, match_id):
        """
        Récupère l'évolution des cotes pour un match.
        
        Args:
            match_id (str): Identifiant unique du match
            
        Returns:
            dict: Historique des cotes par marché
        """
        url = f"{self.base_url}/match/{match_id}/odds-movement/"
        
        try:
            # Utiliser requests à la place de fetch_url
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                logger.warning(f"Impossible de récupérer l'évolution des cotes pour le match {match_id}. Code: {response.status_code}")
                return {}
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Structure pour les cotes
            odds_movement = {
                '1X2': {
                    'home': [],
                    'draw': [],
                    'away': []
                },
                'Over/Under': {},
                'Asian Handicap': {},
                'Both Teams to Score': {}
            }
            
            # Récupérer les cotes 1X2
            home_odds_elem = soup.select('div.oddsTab__tableWrapper--home tr.oddsCell__odd')
            draw_odds_elem = soup.select('div.oddsTab__tableWrapper--draw tr.oddsCell__odd')
            away_odds_elem = soup.select('div.oddsTab__tableWrapper--away tr.oddsCell__odd')
            
            # Extraire l'historique des cotes pour le marché 1X2
            for odds_elem in home_odds_elem:
                try:
                    value_elem = odds_elem.select_one('span.oddsCell__odd')
                    time_elem = odds_elem.select_one('span.oddsCell__time')
                    
                    if value_elem and time_elem:
                        odds_movement['1X2']['home'].append({
                            'value': value_elem.text.strip(),
                            'time': time_elem.text.strip()
                        })
                except:
                    continue
            
            for odds_elem in draw_odds_elem:
                try:
                    value_elem = odds_elem.select_one('span.oddsCell__odd')
                    time_elem = odds_elem.select_one('span.oddsCell__time')
                    
                    if value_elem and time_elem:
                        odds_movement['1X2']['draw'].append({
                            'value': value_elem.text.strip(),
                            'time': time_elem.text.strip()
                        })
                except:
                    continue
            
            for odds_elem in away_odds_elem:
                try:
                    value_elem = odds_elem.select_one('span.oddsCell__odd')
                    time_elem = odds_elem.select_one('span.oddsCell__time')
                    
                    if value_elem and time_elem:
                        odds_movement['1X2']['away'].append({
                            'value': value_elem.text.strip(),
                            'time': time_elem.text.strip()
                        })
                except:
                    continue
            
            return odds_movement
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'évolution des cotes: {e}")
            return {}
            
        finally:
            self._random_delay()
    
    def get_head_to_head(self, team1_id, team2_id, num_matches=10):
        """
        Récupère l'historique des confrontations directes entre deux équipes.
        
        Args:
            team1_id (str): Identifiant de la première équipe
            team2_id (str): Identifiant de la deuxième équipe
            num_matches (int): Nombre de confrontations à récupérer
            
        Returns:
            list: Liste des confrontations directes
        """
        # Construire l'URL des confrontations H2H
        url = f"{self.base_url}/match/{'N/A'}/h2h/" # Ceci est un exemple - nécessite un match_id réel
        
        try:
            # Utiliser requests à la place de fetch_url
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                logger.warning(f"Impossible de récupérer les H2H entre {team1_id} et {team2_id}. Code: {response.status_code}")
                return []
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Récupérer les noms des équipes
            team1_name_elem = soup.select_one('div.h2h__participantName--home')
            team2_name_elem = soup.select_one('div.h2h__participantName--away')
            
            team1_name = team1_name_elem.text.strip() if team1_name_elem else "Team 1"
            team2_name = team2_name_elem.text.strip() if team2_name_elem else "Team 2"
            
            # Récupérer les matchs H2H
            h2h_matches = []
            h2h_section = soup.select_one('div.h2h__section--mutual')
            
            if h2h_section:
                match_elems = h2h_section.select('div.event__match')
                
                for i, match_elem in enumerate(match_elems):
                    if i >= num_matches:
                        break
                    
                    try:
                        # ID du match
                        match_id = match_elem.get('id', '')
                        if match_id:
                            match_id = match_id.replace('g_1_', '')
                        
                        # Équipes
                        home_team_elem = match_elem.select_one('div.event__participant--home')
                        away_team_elem = match_elem.select_one('div.event__participant--away')
                        
                        home_team = home_team_elem.text.strip() if home_team_elem else "Unknown"
                        away_team = away_team_elem.text.strip() if away_team_elem else "Unknown"
                        
                        # Score
                        score_elem = match_elem.select_one('div.event__scores')
                        score = score_elem.text.strip().replace(' ', '') if score_elem else "0-0"
                        
                        # Date
                        date_elem = match_elem.select_one('div.event__time')
                        date = date_elem.text.strip() if date_elem else "Unknown"
                        
                        # Ligue
                        league_elem = match_elem.select_one('div.event__title--name')
                        league = league_elem.text.strip() if league_elem else "Unknown"
                        
                        h2h_matches.append({
                            'id': match_id,
                            'home_team': home_team,
                            'away_team': away_team,
                            'score': score,
                            'date': date,
                            'league': league
                        })
                        
                    except Exception as e:
                        logger.error(f"Erreur lors de l'extraction d'un match H2H: {e}")
                        continue
            
            return h2h_matches
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des H2H: {e}")
            return []
            
        finally:
            self._random_delay()
    
    def get_league_table(self, league_id):
        """
        Récupère le classement d'une ligue.
        
        Args:
            league_id (str): Identifiant de la ligue
            
        Returns:
            list: Classement de la ligue
        """
        url = f"{self.base_url}/tournament/{league_id}/standings/"
        
        try:
            # Utiliser requests à la place de fetch_url
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                logger.warning(f"Impossible de récupérer le classement de la ligue {league_id}. Code: {response.status_code}")
                return []
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            standings = []
            team_rows = soup.select('div.ui-table__row')
            
            for row in team_rows:
                try:
                    # Position
                    position_elem = row.select_one('div.tableCellRank')
                    position = position_elem.text.strip() if position_elem else "0"
                    
                    # Nom de l'équipe
                    team_name_elem = row.select_one('a.tableCellParticipant__name')
                    team_name = team_name_elem.text.strip() if team_name_elem else "Unknown"
                    
                    # Nombre de matchs joués
                    played_elem = row.select_one('div.table__cell--value')
                    played = played_elem.text.strip() if played_elem else "0"
                    
                    # Victoires, nuls, défaites
                    results_elems = row.select('div.table__cell--value')
                    wins = results_elems[1].text.strip() if len(results_elems) > 1 else "0"
                    draws = results_elems[2].text.strip() if len(results_elems) > 2 else "0"
                    losses = results_elems[3].text.strip() if len(results_elems) > 3 else "0"
                    
                    # Buts marqués et encaissés
                    goals_for = results_elems[4].text.strip() if len(results_elems) > 4 else "0"
                    goals_against = results_elems[5].text.strip() if len(results_elems) > 5 else "0"
                    
                    # Différence de buts
                    goal_diff = results_elems[6].text.strip() if len(results_elems) > 6 else "0"
                    
                    # Points
                    points_elem = row.select_one('div.table__cell--points')
                    points = points_elem.text.strip() if points_elem else "0"
                    
                    standings.append({
                        'position': position,
                        'team': team_name,
                        'played': played,
                        'wins': wins,
                        'draws': draws,
                        'losses': losses,
                        'goals_for': goals_for,
                        'goals_against': goals_against,
                        'goal_diff': goal_diff,
                        'points': points
                    })
                    
                except Exception as e:
                    logger.error(f"Erreur lors de l'extraction d'une ligne du classement: {e}")
                    continue
            
            return standings
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du classement: {e}")
            return []
            
        finally:
            self._random_delay()
    
    def search_teams_or_leagues(self, query):
        """
        Recherche des équipes ou ligues à partir d'un terme de recherche.
        
        Args:
            query (str): Terme de recherche
            
        Returns:
            dict: Résultats de recherche
        """
        # Implémenter plus tard si nécessaire
        return {'teams': [], 'leagues': []}
    
    def enrich_match_data(self, basic_match):
        """
        Enrichit les données d'un match avec des détails complémentaires.
        
        Args:
            basic_match (dict): Données de base du match
            
        Returns:
            dict: Données enrichies du match
        """
        enriched_match = basic_match.copy()
        match_id = basic_match.get('id')
        
        if not match_id:
            return enriched_match
        
        try:
            # Récupérer les cotes
            odds_movement = self.get_odds_movement(match_id)
            if odds_movement and '1X2' in odds_movement:
                latest_odds = {
                    '1': odds_movement['1X2']['home'][0]['value'] if odds_movement['1X2']['home'] else None,
                    'X': odds_movement['1X2']['draw'][0]['value'] if odds_movement['1X2']['draw'] else None,
                    '2': odds_movement['1X2']['away'][0]['value'] if odds_movement['1X2']['away'] else None
                }
                enriched_match['odds'] = latest_odds
            
            # Récupérer les formes des équipes
            home_team_id = "team1"  # Ceci est un exemple - nécessite un ID réel
            away_team_id = "team2"  # Ceci est un exemple - nécessite un ID réel
            
            home_form = self.get_team_form(home_team_id)
            away_form = self.get_team_form(away_team_id)
            
            # Récupérer les H2H
            h2h = self.get_head_to_head(home_team_id, away_team_id)
            
            # Ajouter les données enrichies
            if home_form:
                enriched_match['home_form'] = home_form
            if away_form:
                enriched_match['away_form'] = away_form
            if h2h:
                enriched_match['head_to_head'] = h2h
        
        except Exception as e:
            logger.error(f"Erreur lors de l'enrichissement des données du match: {e}")
        
        return enriched_match
        
    def get_match_lineups(self, match_id):
        """
        Récupère les compositions d'équipes pour un match.
        
        Args:
            match_id (str): Identifiant unique du match
            
        Returns:
            dict: Compositions d'équipes (titulaires et remplaçants)
        """
        url = f"{self.base_url}/match/{match_id}/lineups/"
        
        try:
            logger.info(f"Récupération des compositions pour le match {match_id}")
            # Utiliser requests à la place de fetch_url pour avoir plus de contrôle sur les headers
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                logger.warning(f"Aucun contenu HTML récupéré pour les compositions du match {match_id}. Code: {response.status_code}")
                return {'home': {'starting': [], 'substitutes': []}, 'away': {'starting': [], 'substitutes': []}}
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Structure de données pour les compositions
            lineups = {
                'home': {'starting': [], 'substitutes': []},
                'away': {'starting': [], 'substitutes': []}
            }
            
            # Récupérer le nom des équipes
            home_team_elem = soup.select_one('div.participant__participantName--home')
            away_team_elem = soup.select_one('div.participant__participantName--away')
            
            if home_team_elem and away_team_elem:
                lineups['home']['team_name'] = home_team_elem.text.strip()
                lineups['away']['team_name'] = away_team_elem.text.strip()
            
            # Récupérer la formation (système de jeu)
            formation_elems = soup.select('div.lineup__formation')
            if len(formation_elems) >= 2:
                lineups['home']['formation'] = formation_elems[0].text.strip()
                lineups['away']['formation'] = formation_elems[1].text.strip()
            
            # Récupérer les titulaires
            for side in ['home', 'away']:
                side_class = 'lineup__sector--home' if side == 'home' else 'lineup__sector--away'
                
                # Titulaires
                starting_elems = soup.select(f'div.{side_class} div.lineup__player')
                for player_elem in starting_elems:
                    try:
                        # Numéro de maillot
                        shirt_elem = player_elem.select_one('div.lineup__playerShirt')
                        shirt_number = shirt_elem.text.strip() if shirt_elem else ""
                        
                        # Nom du joueur
                        name_elem = player_elem.select_one('a.lineup__playerName')
                        name = name_elem.text.strip() if name_elem else ""
                        
                        # Position
                        position_elem = player_elem.select_one('span.lineup__playerPosition')
                        position = position_elem.text.strip() if position_elem else ""
                        
                        if name:
                            lineups[side]['starting'].append({
                                'name': name,
                                'number': shirt_number,
                                'position': position
                            })
                    except Exception as e:
                        logger.error(f"Erreur lors de l'extraction d'un joueur titulaire: {e}")
                        continue
                
                # Remplaçants
                side_bench_class = 'lineup__bench--home' if side == 'home' else 'lineup__bench--away'
                bench_elems = soup.select(f'div.{side_bench_class} div.lineup__benchRow')
                
                for player_elem in bench_elems:
                    try:
                        # Numéro de maillot
                        shirt_elem = player_elem.select_one('div.lineup__playerShirt')
                        shirt_number = shirt_elem.text.strip() if shirt_elem else ""
                        
                        # Nom du joueur
                        name_elem = player_elem.select_one('a.lineup__playerName')
                        name = name_elem.text.strip() if name_elem else ""
                        
                        # Position
                        position_elem = player_elem.select_one('span.lineup__playerPosition')
                        position = position_elem.text.strip() if position_elem else ""
                        
                        if name:
                            lineups[side]['substitutes'].append({
                                'name': name,
                                'number': shirt_number,
                                'position': position
                            })
                    except Exception as e:
                        logger.error(f"Erreur lors de l'extraction d'un joueur remplaçant: {e}")
                        continue
            
            # Récupérer les entraîneurs
            coach_elems = soup.select('div.lineup__coachName')
            if len(coach_elems) >= 2:
                lineups['home']['coach'] = coach_elems[0].text.strip() if coach_elems[0] else "Unknown"
                lineups['away']['coach'] = coach_elems[1].text.strip() if coach_elems[1] else "Unknown"
            
            # Vérifier si c'est une composition officielle ou probable
            lineup_status_elem = soup.select_one('div.lineup__title')
            if lineup_status_elem:
                status_text = lineup_status_elem.text.strip().lower()
                if "probable" in status_text or "predicted" in status_text:
                    lineups['status'] = "probable"
                else:
                    lineups['status'] = "official"
            else:
                lineups['status'] = "unknown"
            
            return lineups
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des compositions d'équipes: {e}")
            return {'home': {'starting': [], 'substitutes': []}, 'away': {'starting': [], 'substitutes': []}}
            
        finally:
            self._random_delay()

    def get_advanced_stats(self, match_id):
        """
        Récupère les statistiques avancées pour un match.
        
        Args:
            match_id (str): Identifiant unique du match
            
        Returns:
            dict: Statistiques avancées du match
        """
        url = f"{self.base_url}/match/{match_id}/match-statistics/"
        
        try:
            logger.info(f"Récupération des statistiques avancées pour le match {match_id}")
            # Utiliser requests à la place de fetch_url pour avoir plus de contrôle sur les headers
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                logger.warning(f"Aucun contenu HTML récupéré pour les statistiques du match {match_id}. Code: {response.status_code}")
                return {}
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Structure de données pour les statistiques
            stats = {
                'home': {},
                'away': {},
                'categories': []
            }
            
            # Récupérer les noms des équipes
            home_team_elem = soup.select_one('div.participant__participantName--home')
            away_team_elem = soup.select_one('div.participant__participantName--away')
            
            if home_team_elem and away_team_elem:
                stats['home_team'] = home_team_elem.text.strip()
                stats['away_team'] = away_team_elem.text.strip()
            
            # Récupérer les catégories de statistiques
            stat_sections = soup.select('div.stat-category')
            
            for section in stat_sections:
                try:
                    # Titre de la catégorie
                    title_elem = section.select_one('div.stat-category__title')
                    if not title_elem:
                        continue
                        
                    category = title_elem.text.strip()
                    stats['categories'].append(category)
                    
                    stats['home'][category] = {}
                    stats['away'][category] = {}
                    
                    # Statistiques individuelles dans cette catégorie
                    stat_rows = section.select('div.stat-category__item')
                    
                    for stat_row in stat_rows:
                        try:
                            # Nom de la statistique
                            name_elem = stat_row.select_one('div.stat-category__name')
                            if not name_elem:
                                continue
                                
                            stat_name = name_elem.text.strip()
                            
                            # Valeurs pour l'équipe à domicile
                            home_value_elem = stat_row.select_one('div.stat-category__value--home')
                            home_value = home_value_elem.text.strip() if home_value_elem else "0"
                            
                            # Valeurs pour l'équipe à l'extérieur
                            away_value_elem = stat_row.select_one('div.stat-category__value--away')
                            away_value = away_value_elem.text.strip() if away_value_elem else "0"
                            
                            # Convertir en nombres si possible
                            try:
                                if '%' in home_value:
                                    home_value = float(home_value.replace('%', '')) / 100
                                else:
                                    home_value = int(home_value) if home_value.isdigit() else home_value
                            except:
                                pass
                                
                            try:
                                if '%' in away_value:
                                    away_value = float(away_value.replace('%', '')) / 100
                                else:
                                    away_value = int(away_value) if away_value.isdigit() else away_value
                            except:
                                pass
                            
                            stats['home'][category][stat_name] = home_value
                            stats['away'][category][stat_name] = away_value
                        
                        except Exception as e:
                            logger.error(f"Erreur lors de l'extraction d'une statistique: {e}")
                            continue
                
                except Exception as e:
                    logger.error(f"Erreur lors de l'extraction d'une catégorie de statistiques: {e}")
                    continue
            
            # Calculer des indicateurs dérivés utiles pour les prédictions
            
            # 1. Taux de conversion (buts / tirs)
            if 'Attack' in stats['home'] and 'Shots on Goal' in stats['home']['Attack'] and 'Goal Attempts' in stats['home']['Attack']:
                try:
                    home_conversion = stats['home']['Attack']['Shots on Goal'] / stats['home']['Attack']['Goal Attempts'] if stats['home']['Attack']['Goal Attempts'] > 0 else 0
                    away_conversion = stats['away']['Attack']['Shots on Goal'] / stats['away']['Attack']['Goal Attempts'] if stats['away']['Attack']['Goal Attempts'] > 0 else 0
                    
                    if 'Derived' not in stats['home']:
                        stats['home']['Derived'] = {}
                        stats['away']['Derived'] = {}
                        stats['categories'].append('Derived')
                    
                    stats['home']['Derived']['Conversion Rate'] = home_conversion
                    stats['away']['Derived']['Conversion Rate'] = away_conversion
                except:
                    pass
            
            # 2. Efficacité des passes
            if 'Passing' in stats['home'] and 'Accurate Passes' in stats['home']['Passing'] and 'Total Passes' in stats['home']['Passing']:
                try:
                    home_pass_efficiency = stats['home']['Passing']['Accurate Passes'] / stats['home']['Passing']['Total Passes'] if stats['home']['Passing']['Total Passes'] > 0 else 0
                    away_pass_efficiency = stats['away']['Passing']['Accurate Passes'] / stats['away']['Passing']['Total Passes'] if stats['away']['Passing']['Total Passes'] > 0 else 0
                    
                    if 'Derived' not in stats['home']:
                        stats['home']['Derived'] = {}
                        stats['away']['Derived'] = {}
                        stats['categories'].append('Derived')
                    
                    stats['home']['Derived']['Pass Efficiency'] = home_pass_efficiency
                    stats['away']['Derived']['Pass Efficiency'] = away_pass_efficiency
                except:
                    pass
            
            return stats
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des statistiques avancées: {e}")
            return {}
            
        finally:
            self._random_delay()
    
    def get_team_recent_stats(self, team_id, num_matches=5):
        """
        Récupère les statistiques récentes d'une équipe.
        
        Args:
            team_id (str): Identifiant de l'équipe
            num_matches (int): Nombre de matchs récents à analyser
            
        Returns:
            dict: Statistiques moyennes de l'équipe
        """
        try:
            logger.info(f"Récupération des statistiques récentes pour l'équipe {team_id}")
            
            # Récupérer les matchs récents
            recent_matches = self.get_team_form(team_id, num_matches)
            
            # Statistiques à collecter
            stats = {
                'goals_scored': [],
                'goals_conceded': [],
                'shots': [],
                'shots_on_target': [],
                'corners': [],
                'possession': [],
                'fouls': [],
                'yellow_cards': [],
                'red_cards': [],
                'win_rate': 0,
                'draw_rate': 0,
                'loss_rate': 0
            }
            
            win_count = 0
            draw_count = 0
            loss_count = 0
            
            # Analyser chaque match récent
            for match in recent_matches:
                match_id = match.get('id')
                if not match_id:
                    continue
                
                # Récupérer les statistiques du match
                match_stats = self.get_advanced_stats(match_id)
                if not match_stats:
                    continue
                
                # Déterminer si l'équipe était à domicile ou à l'extérieur
                is_home = match_stats.get('home_team') == team_id
                team_side = 'home' if is_home else 'away'
                opponent_side = 'away' if is_home else 'home'
                
                # Récupérer le score et déterminer le résultat
                score = match.get('score', '0-0').split('-')
                if len(score) == 2:
                    try:
                        home_score = int(score[0].strip())
                        away_score = int(score[1].strip())
                        
                        if is_home:
                            if home_score > away_score:
                                win_count += 1
                            elif home_score == away_score:
                                draw_count += 1
                            else:
                                loss_count += 1
                                
                            stats['goals_scored'].append(home_score)
                            stats['goals_conceded'].append(away_score)
                        else:
                            if away_score > home_score:
                                win_count += 1
                            elif away_score == home_score:
                                draw_count += 1
                            else:
                                loss_count += 1
                                
                            stats['goals_scored'].append(away_score)
                            stats['goals_conceded'].append(home_score)
                    except:
                        pass
                
                # Collecter les statistiques de match
                for category in match_stats.get('categories', []):
                    category_stats = match_stats.get(team_side, {}).get(category, {})
                    
                    # Tirs
                    if category == 'Attack' and 'Goal Attempts' in category_stats:
                        stats['shots'].append(category_stats['Goal Attempts'])
                    
                    # Tirs cadrés
                    if category == 'Attack' and 'Shots on Goal' in category_stats:
                        stats['shots_on_target'].append(category_stats['Shots on Goal'])
                    
                    # Corners
                    if category == 'Attack' and 'Corner Kicks' in category_stats:
                        stats['corners'].append(category_stats['Corner Kicks'])
                    
                    # Possession
                    if category == 'Ball Possession' and 'Ball Possession' in category_stats:
                        possession_value = category_stats['Ball Possession']
                        if isinstance(possession_value, float):
                            stats['possession'].append(possession_value)
                        elif isinstance(possession_value, str) and '%' in possession_value:
                            try:
                                stats['possession'].append(float(possession_value.replace('%', '')) / 100)
                            except:
                                pass
                    
                    # Fautes
                    if category == 'Discipline' and 'Fouls' in category_stats:
                        stats['fouls'].append(category_stats['Fouls'])
                    
                    # Cartons
                    if category == 'Discipline' and 'Yellow Cards' in category_stats:
                        stats['yellow_cards'].append(category_stats['Yellow Cards'])
                    
                    if category == 'Discipline' and 'Red Cards' in category_stats:
                        stats['red_cards'].append(category_stats['Red Cards'])
            
            # Calculer les moyennes
            total_matches = len(recent_matches)
            if total_matches > 0:
                stats['win_rate'] = win_count / total_matches
                stats['draw_rate'] = draw_count / total_matches
                stats['loss_rate'] = loss_count / total_matches
                
                stats['avg_goals_scored'] = sum(stats['goals_scored']) / len(stats['goals_scored']) if stats['goals_scored'] else 0
                stats['avg_goals_conceded'] = sum(stats['goals_conceded']) / len(stats['goals_conceded']) if stats['goals_conceded'] else 0
                stats['avg_shots'] = sum(stats['shots']) / len(stats['shots']) if stats['shots'] else 0
                stats['avg_shots_on_target'] = sum(stats['shots_on_target']) / len(stats['shots_on_target']) if stats['shots_on_target'] else 0
                stats['avg_corners'] = sum(stats['corners']) / len(stats['corners']) if stats['corners'] else 0
                stats['avg_possession'] = sum(stats['possession']) / len(stats['possession']) if stats['possession'] else 0
                stats['avg_fouls'] = sum(stats['fouls']) / len(stats['fouls']) if stats['fouls'] else 0
                stats['avg_yellow_cards'] = sum(stats['yellow_cards']) / len(stats['yellow_cards']) if stats['yellow_cards'] else 0
                stats['avg_red_cards'] = sum(stats['red_cards']) / len(stats['red_cards']) if stats['red_cards'] else 0
            
            return stats
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des statistiques récentes de l'équipe: {e}")
            return {}
            
        finally:
            self._random_delay()