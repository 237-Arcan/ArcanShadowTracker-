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
            
        url = f"{self.base_url}/{sport}/{date}/"
        
        try:
            html_content = fetch_url(url, headers=self.headers)
            if not html_content:
                return []
                
            # Extraction du contenu principal
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Recherche des éléments de matchs
            matches = []
            match_elements = soup.select('div.event__match')
            
            for match in match_elements:
                try:
                    match_id = match.get('id', '').replace('g_1_', '')
                    
                    # Équipes
                    home_team = match.select_one('div.event__participant--home').text.strip()
                    away_team = match.select_one('div.event__participant--away').text.strip()
                    
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
                        'url': f"{self.base_url}/match/{match_id}/"
                    })
                except Exception as e:
                    print(f"Erreur lors de l'extraction d'un match: {e}")
                    continue
                    
            return matches
            
        except Exception as e:
            print(f"Erreur lors de la récupération des matchs: {e}")
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
        url = f"{self.base_url}/match/{match_id}/"
        
        try:
            html_content = fetch_url(url, headers=self.headers)
            if not html_content:
                return {}
                
            # Extraction avec trafilatura pour le contenu principal
            text_content = extract(html_content)
            
            # Parsing avec BeautifulSoup pour la structure
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Récupération des informations de base
            home_team = soup.select_one('div.participant__participantName--home').text.strip()
            away_team = soup.select_one('div.participant__participantName--away').text.strip()
            
            # Score actuel ou final
            score_element = soup.select_one('div.detailScore__wrapper')
            home_score = score_element.select_one('span.detailScore__wrapper span:nth-child(1)').text.strip() if score_element else "0"
            away_score = score_element.select_one('span.detailScore__wrapper span:nth-child(3)').text.strip() if score_element else "0"
            
            # Événements de match (buts, cartons)
            events = []
            event_elements = soup.select('div.detailMS__incidentRow')
            
            for event in event_elements:
                event_type_element = event.select_one('div.detailMS__incidentType')
                event_type = event_type_element.get('class', [''])[0] if event_type_element else ""
                
                time_element = event.select_one('div.detailMS__incidentTime')
                event_time = time_element.text.strip() if time_element else ""
                
                player_element = event.select_one('div.detailMS__incidentName')
                player = player_element.text.strip() if player_element else ""
                
                team_side = "home" if "incidentRow--home" in event.get('class', []) else "away"
                
                events.append({
                    'type': event_type,
                    'time': event_time,
                    'player': player,
                    'team': team_side
                })
            
            # Statistiques
            stats = {}
            stat_elements = soup.select('div.stat__row')
            
            for stat in stat_elements:
                category_element = stat.select_one('div.stat__categoryName')
                category = category_element.text.strip() if category_element else ""
                
                home_value_element = stat.select_one('div.stat__homeValue')
                home_value = home_value_element.text.strip() if home_value_element else ""
                
                away_value_element = stat.select_one('div.stat__awayValue')
                away_value = away_value_element.text.strip() if away_value_element else ""
                
                stats[category] = {
                    'home': home_value,
                    'away': away_value
                }
            
            # Cotes
            odds = {}
            odds_elements = soup.select('div.oddsValueInner')
            
            if odds_elements:
                if len(odds_elements) >= 3:
                    odds['1'] = odds_elements[0].text.strip()
                    odds['X'] = odds_elements[1].text.strip()
                    odds['2'] = odds_elements[2].text.strip()
            
            match_details = {
                'id': match_id,
                'home_team': home_team,
                'away_team': away_team,
                'home_score': home_score,
                'away_score': away_score,
                'events': events,
                'stats': stats,
                'odds': odds,
                'url': url
            }
            
            return match_details
            
        except Exception as e:
            print(f"Erreur lors de la récupération des détails du match: {e}")
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
            html_content = fetch_url(url, headers=self.headers)
            if not html_content:
                return []
                
            # Parsing avec BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Récupération des matchs récents
            recent_matches = []
            match_elements = soup.select('div.event__match')[:num_matches]
            
            for match in match_elements:
                try:
                    match_id = match.get('id', '').replace('g_1_', '')
                    
                    # Équipes
                    home_team = match.select_one('div.event__participant--home').text.strip()
                    away_team = match.select_one('div.event__participant--away').text.strip()
                    
                    # Score
                    score_element = match.select_one('div.event__scores')
                    score = score_element.text.strip() if score_element else "N/A"
                    
                    # Date
                    date_element = match.select_one('div.event__time')
                    date = date_element.text.strip() if date_element else "N/A"
                    
                    # Résultat (W/D/L) du point de vue de l'équipe
                    result = "N/A"
                    if score_element:
                        scores = score_element.text.split('-')
                        if len(scores) == 2:
                            home_score = int(scores[0].strip())
                            away_score = int(scores[1].strip())
                            
                            if home_team == team_id:
                                if home_score > away_score:
                                    result = "W"
                                elif home_score < away_score:
                                    result = "L"
                                else:
                                    result = "D"
                            else:
                                if home_score < away_score:
                                    result = "W"
                                elif home_score > away_score:
                                    result = "L"
                                else:
                                    result = "D"
                    
                    recent_matches.append({
                        'id': match_id,
                        'home_team': home_team,
                        'away_team': away_team,
                        'score': score,
                        'date': date,
                        'result': result
                    })
                except Exception as e:
                    print(f"Erreur lors de l'extraction d'un match récent: {e}")
                    continue
                    
            return recent_matches
            
        except Exception as e:
            print(f"Erreur lors de la récupération de la forme de l'équipe: {e}")
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
            html_content = fetch_url(url, headers=self.headers)
            if not html_content:
                return {}
                
            # Parsing avec BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Récupération des mouvements de cotes
            odds_movement = {}
            
            # Pour chaque type de marché (1X2, Over/Under, etc.)
            market_elements = soup.select('div.oddsTab__tableWrapper')
            
            for market_element in market_elements:
                market_name_element = market_element.select_one('div.oddsTab__tableHeader')
                market_name = market_name_element.text.strip() if market_name_element else "Unknown"
                
                rows = market_element.select('div.ui-table__row')
                market_data = []
                
                for row in rows:
                    time_element = row.select_one('div.ui-table__cell--time')
                    time = time_element.text.strip() if time_element else ""
                    
                    odds_cells = row.select('div.ui-table__cell:not(.ui-table__cell--time)')
                    odds_values = [cell.text.strip() for cell in odds_cells]
                    
                    row_data = {
                        'time': time,
                        'values': odds_values
                    }
                    
                    market_data.append(row_data)
                
                odds_movement[market_name] = market_data
            
            return odds_movement
            
        except Exception as e:
            print(f"Erreur lors de la récupération des mouvements de cotes: {e}")
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
        url = f"{self.base_url}/match/h2h/{team1_id}-{team2_id}/previous-meetings/"
        
        try:
            html_content = fetch_url(url, headers=self.headers)
            if not html_content:
                return []
                
            # Parsing avec BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Récupération des confrontations directes
            h2h_matches = []
            match_elements = soup.select('div.h2h__section div.event__match')[:num_matches]
            
            for match in match_elements:
                try:
                    match_id = match.get('id', '').replace('g_1_', '')
                    
                    # Équipes
                    home_team = match.select_one('div.event__participant--home').text.strip()
                    away_team = match.select_one('div.event__participant--away').text.strip()
                    
                    # Score
                    score_element = match.select_one('div.event__scores')
                    score = score_element.text.strip() if score_element else "N/A"
                    
                    # Date
                    date_element = match.select_one('div.event__time')
                    date = date_element.text.strip() if date_element else "N/A"
                    
                    h2h_matches.append({
                        'id': match_id,
                        'home_team': home_team,
                        'away_team': away_team,
                        'score': score,
                        'date': date
                    })
                except Exception as e:
                    print(f"Erreur lors de l'extraction d'une confrontation directe: {e}")
                    continue
                    
            return h2h_matches
            
        except Exception as e:
            print(f"Erreur lors de la récupération des confrontations directes: {e}")
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
        url = f"{self.base_url}/league/{league_id}/standings/"
        
        try:
            html_content = fetch_url(url, headers=self.headers)
            if not html_content:
                return []
                
            # Parsing avec BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Récupération du classement
            standings = []
            team_elements = soup.select('div.ui-table__row')
            
            for team in team_elements:
                try:
                    # Position
                    position_element = team.select_one('div.tableCellRank')
                    position = position_element.text.strip() if position_element else "N/A"
                    
                    # Équipe
                    team_name_element = team.select_one('div.tableCellParticipant__name')
                    team_name = team_name_element.text.strip() if team_name_element else "N/A"
                    
                    # Nombre de matchs joués
                    matches_played_element = team.select_one('div.table__cell--value')
                    matches_played = matches_played_element.text.strip() if matches_played_element else "0"
                    
                    # Points
                    points_element = team.select('div.table__cell--value')[9] if len(team.select('div.table__cell--value')) > 9 else None
                    points = points_element.text.strip() if points_element else "0"
                    
                    # Victoires
                    wins_element = team.select('div.table__cell--value')[1] if len(team.select('div.table__cell--value')) > 1 else None
                    wins = wins_element.text.strip() if wins_element else "0"
                    
                    # Nuls
                    draws_element = team.select('div.table__cell--value')[2] if len(team.select('div.table__cell--value')) > 2 else None
                    draws = draws_element.text.strip() if draws_element else "0"
                    
                    # Défaites
                    losses_element = team.select('div.table__cell--value')[3] if len(team.select('div.table__cell--value')) > 3 else None
                    losses = losses_element.text.strip() if losses_element else "0"
                    
                    # Buts marqués/encaissés
                    goals_for_element = team.select('div.table__cell--value')[4] if len(team.select('div.table__cell--value')) > 4 else None
                    goals_for = goals_for_element.text.strip() if goals_for_element else "0"
                    
                    goals_against_element = team.select('div.table__cell--value')[5] if len(team.select('div.table__cell--value')) > 5 else None
                    goals_against = goals_against_element.text.strip() if goals_against_element else "0"
                    
                    standings.append({
                        'position': position,
                        'team': team_name,
                        'matches_played': matches_played,
                        'wins': wins,
                        'draws': draws,
                        'losses': losses,
                        'goals_for': goals_for,
                        'goals_against': goals_against,
                        'points': points
                    })
                except Exception as e:
                    print(f"Erreur lors de l'extraction d'une équipe du classement: {e}")
                    continue
                    
            return standings
            
        except Exception as e:
            print(f"Erreur lors de la récupération du classement: {e}")
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
        query = query.replace(' ', '+')
        url = f"{self.base_url}/search/{query}/"
        
        try:
            html_content = fetch_url(url, headers=self.headers)
            if not html_content:
                return {}
                
            # Parsing avec BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            results = {
                'teams': [],
                'leagues': []
            }
            
            # Recherche d'équipes
            team_elements = soup.select('div.searchTeam')
            
            for team in team_elements:
                try:
                    # Nom de l'équipe
                    name_element = team.select_one('span.searchTeam__name')
                    name = name_element.text.strip() if name_element else "N/A"
                    
                    # Lien de l'équipe
                    link_element = team.select_one('a')
                    link = link_element.get('href', '') if link_element else ""
                    
                    # Extraction de l'ID de l'équipe
                    team_id = ""
                    if link:
                        # Format attendu: "/team/team-name/abcdef/"
                        parts = link.split('/')
                        if len(parts) > 2:
                            team_id = parts[-2]
                    
                    # Pays/Ligue de l'équipe
                    country_element = team.select_one('span.searchTeam__country')
                    country = country_element.text.strip() if country_element else "N/A"
                    
                    results['teams'].append({
                        'id': team_id,
                        'name': name,
                        'country': country,
                        'url': f"{self.base_url}{link}"
                    })
                except Exception as e:
                    print(f"Erreur lors de l'extraction d'une équipe: {e}")
                    continue
            
            # Recherche de ligues
            league_elements = soup.select('div.searchCompetition')
            
            for league in league_elements:
                try:
                    # Nom de la ligue
                    name_element = league.select_one('span.searchCompetition__name')
                    name = name_element.text.strip() if name_element else "N/A"
                    
                    # Lien de la ligue
                    link_element = league.select_one('a')
                    link = link_element.get('href', '') if link_element else ""
                    
                    # Extraction de l'ID de la ligue
                    league_id = ""
                    if link:
                        # Format attendu: "/league/country/league-name/abcdef/"
                        parts = link.split('/')
                        if len(parts) > 2:
                            league_id = parts[-2]
                    
                    # Pays de la ligue
                    country_element = league.select_one('span.searchCompetition__country')
                    country = country_element.text.strip() if country_element else "N/A"
                    
                    results['leagues'].append({
                        'id': league_id,
                        'name': name,
                        'country': country,
                        'url': f"{self.base_url}{link}"
                    })
                except Exception as e:
                    print(f"Erreur lors de l'extraction d'une ligue: {e}")
                    continue
                    
            return results
            
        except Exception as e:
            print(f"Erreur lors de la recherche: {e}")
            return {}
            
        finally:
            self._random_delay()

    def enrich_match_data(self, basic_match):
        """
        Enrichit les données d'un match avec des détails complémentaires.
        
        Args:
            basic_match (dict): Données de base du match
            
        Returns:
            dict: Données enrichies du match
        """
        match_id = basic_match.get('id')
        if not match_id:
            return basic_match
            
        # Récupérer les détails complets du match
        match_details = self.get_match_details(match_id)
        
        # Fusionner les données
        enriched_match = {**basic_match, **match_details}
        
        # Rechercher les équipes pour obtenir leurs IDs
        home_team = basic_match.get('home_team', '')
        away_team = basic_match.get('away_team', '')
        
        if home_team and away_team:
            # Rechercher la première équipe
            home_results = self.search_teams_or_leagues(home_team)
            home_id = ""
            
            if home_results.get('teams'):
                for team in home_results.get('teams', []):
                    if team.get('name').lower() == home_team.lower():
                        home_id = team.get('id')
                        break
            
            # Rechercher la deuxième équipe
            away_results = self.search_teams_or_leagues(away_team)
            away_id = ""
            
            if away_results.get('teams'):
                for team in away_results.get('teams', []):
                    if team.get('name').lower() == away_team.lower():
                        away_id = team.get('id')
                        break
            
            # Si on a trouvé les deux équipes, récupérer les historiques
            if home_id and away_id:
                # Forme récente
                home_form = self.get_team_form(home_id)
                away_form = self.get_team_form(away_id)
                
                # Confrontations directes
                h2h = self.get_head_to_head(home_id, away_id)
                
                enriched_match['home_form'] = home_form
                enriched_match['away_form'] = away_form
                enriched_match['head_to_head'] = h2h
        
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
            html_content = fetch_url(url, user_agent=self.headers['User-Agent'])
            if not html_content:
                logger.warning(f"Aucun contenu HTML récupéré pour les compositions du match {match_id}")
                return {'home': {'starting': [], 'substitutes': []}, 'away': {'starting': [], 'substitutes': []}}
                
            soup = BeautifulSoup(html_content, 'html.parser')
            
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
            html_content = fetch_url(url, user_agent=self.headers['User-Agent'])
            if not html_content:
                logger.warning(f"Aucun contenu HTML récupéré pour les statistiques du match {match_id}")
                return {}
                
            soup = BeautifulSoup(html_content, 'html.parser')
            
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