"""
DataEnrichment - Module d'enrichissement des données sportives pour ArcanShadow
Ce module utilise le scraping et d'autres sources pour enrichir les données de matchs
avec des statistiques avancées, compositions d'équipes et analyses historiques.
"""

import logging
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from .flash_scraper import FlashScraper

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('data_enrichment')

class DataEnrichment:
    """
    Module d'enrichissement de données pour ArcanShadow.
    Récupère et combine des données de plusieurs sources pour améliorer la qualité
    des prédictions et des analyses.
    """
    def __init__(self):
        """
        Initialise le module d'enrichissement de données.
        """
        self.flash_scraper = FlashScraper()
        
    def get_daily_matches(self, sport="football", date=None):
        """
        Récupère les matchs du jour avec des données de base.
        
        Args:
            sport (str): Le sport à récupérer (default: football)
            date (str): Date au format YYYYMMDD (default: aujourd'hui)
            
        Returns:
            list: Liste des matchs du jour avec leurs infos de base
        """
        try:
            logger.info(f"Récupération des matchs du jour pour {sport}")
            
            # Récupérer les matchs via le scraper
            matches = self.flash_scraper.get_matches_of_day(sport=sport, date=date)
            
            return matches
        
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des matchs du jour: {e}")
            
            # En cas d'erreur, générer quelques matchs d'exemple
            return self._generate_sample_matches()
    
    def _generate_sample_matches(self, count=10):
        """
        Génère des matchs d'exemple pour les tests ou en cas d'erreur.
        
        Args:
            count (int): Nombre de matchs à générer
            
        Returns:
            list: Liste de matchs générés
        """
        teams = {
            "English Premier League": [
                "Manchester City", "Liverpool", "Arsenal", "Manchester United",
                "Tottenham", "Chelsea", "Newcastle", "Aston Villa",
                "Brighton", "West Ham", "Crystal Palace", "Brentford"
            ],
            "Spanish La Liga": [
                "Real Madrid", "Barcelona", "Atletico Madrid", "Real Sociedad",
                "Villarreal", "Athletic Bilbao", "Real Betis", "Valencia",
                "Sevilla", "Celta Vigo", "Getafe", "Espanyol"
            ],
            "Italian Serie A": [
                "Inter Milan", "AC Milan", "Juventus", "Napoli",
                "Roma", "Lazio", "Atalanta", "Fiorentina",
                "Bologna", "Torino", "Udinese", "Sassuolo"
            ],
            "German Bundesliga": [
                "Bayern Munich", "Borussia Dortmund", "RB Leipzig", "Bayer Leverkusen",
                "Eintracht Frankfurt", "Wolfsburg", "Borussia Monchengladbach", "Hoffenheim",
                "Freiburg", "Mainz", "FC Koln", "Union Berlin"
            ],
            "French Ligue 1": [
                "Paris Saint-Germain", "Marseille", "Monaco", "Lyon",
                "Lille", "Rennes", "Nice", "Lens",
                "Strasbourg", "Montpellier", "Nantes", "Brest"
            ]
        }
        
        matches = []
        match_time = datetime.now().replace(hour=12, minute=0, second=0)
        
        for i in range(count):
            # Choisir une ligue aléatoire
            league = random.choice(list(teams.keys()))
            league_teams = teams[league]
            
            # Choisir deux équipes différentes
            home_team = random.choice(league_teams)
            away_team = random.choice([team for team in league_teams if team != home_team])
            
            # Générer un identifiant unique
            match_id = f"sample_{league.replace(' ', '_')}_{i}_{int(datetime.now().timestamp())}"
            
            # Incrémenter l'heure de match
            match_time += timedelta(minutes=15)
            
            matches.append({
                'id': match_id,
                'home_team': home_team,
                'away_team': away_team,
                'league': league,
                'date': match_time.strftime('%Y-%m-%d'),
                'time': match_time.strftime('%H:%M'),
                'status': 'NS'  # Non commencé
            })
        
        return matches
    
    def enrich_match_data(self, match):
        """
        Enrichit les données d'un match avec des informations supplémentaires.
        
        Args:
            match (dict): Données de base du match
            
        Returns:
            dict: Données enrichies du match
        """
        try:
            logger.info(f"Enrichissement des données pour le match {match.get('id')}")
            
            match_id = match.get('id')
            
            if not match_id:
                logger.warning("Impossible d'enrichir un match sans identifiant")
                return match
            
            # Si c'est un match d'exemple (généré), on génère des données d'exemple
            if str(match_id).startswith('sample_'):
                return self._enrich_sample_match(match)
            
            # Enrichir avec le scraper
            enriched_match = self.flash_scraper.enrich_match_data(match)
            
            # Récupérer les compositions d'équipes si disponibles
            lineups = self.flash_scraper.get_match_lineups(match_id)
            if lineups and (lineups.get('home', {}).get('starting') or lineups.get('away', {}).get('starting')):
                enriched_match['lineups'] = lineups
            
            # Récupérer les statistiques avancées si disponibles
            advanced_stats = self.flash_scraper.get_advanced_stats(match_id)
            if advanced_stats and advanced_stats.get('categories'):
                enriched_match['advanced_stats'] = advanced_stats
            
            return enriched_match
        
        except Exception as e:
            logger.error(f"Erreur lors de l'enrichissement des données du match: {e}")
            return match
    
    def _enrich_sample_match(self, match):
        """
        Enrichit un match d'exemple avec des données simulées.
        
        Args:
            match (dict): Données de base du match d'exemple
            
        Returns:
            dict: Données enrichies du match d'exemple
        """
        enriched_match = match.copy()
        
        # Ajouter des cotes simulées
        home_strength = random.uniform(0.3, 0.7)
        away_strength = random.uniform(0.3, 0.7)
        draw_factor = random.uniform(0.2, 0.4)
        
        home_odds = round(1 / (home_strength + 0.05), 2)
        away_odds = round(1 / (away_strength + 0.05), 2)
        draw_odds = round(1 / draw_factor, 2)
        
        enriched_match['odds'] = {
            '1': home_odds,
            'X': draw_odds,
            '2': away_odds,
            'Over 2.5': round(random.uniform(1.7, 2.2), 2),
            'Under 2.5': round(random.uniform(1.6, 2.1), 2),
            'BTTS Yes': round(random.uniform(1.7, 2.1), 2),
            'BTTS No': round(random.uniform(1.7, 2.1), 2)
        }
        
        # Simuler la forme récente
        home_form = []
        away_form = []
        
        for i in range(5):
            # Forme à domicile
            home_result = random.choices(['W', 'D', 'L'], weights=[home_strength, draw_factor, away_strength])[0]
            home_goals_for = random.choices(range(4), weights=[0.2, 0.5, 0.2, 0.1])[0]
            home_goals_against = random.choices(range(4), weights=[0.3, 0.4, 0.2, 0.1])[0]
            
            if home_result == 'W':
                home_goals_for = max(home_goals_against + 1, home_goals_for)
            elif home_result == 'L':
                home_goals_against = max(home_goals_for + 1, home_goals_against)
            
            # Forme à l'extérieur
            away_result = random.choices(['W', 'D', 'L'], weights=[away_strength, draw_factor, home_strength])[0]
            away_goals_for = random.choices(range(4), weights=[0.3, 0.4, 0.2, 0.1])[0]
            away_goals_against = random.choices(range(4), weights=[0.2, 0.5, 0.2, 0.1])[0]
            
            if away_result == 'W':
                away_goals_for = max(away_goals_against + 1, away_goals_for)
            elif away_result == 'L':
                away_goals_against = max(away_goals_for + 1, away_goals_against)
            
            # Date du match récent
            past_date = (datetime.now() - timedelta(days=i*7 + 3)).strftime('%Y-%m-%d')
            
            home_form.append({
                'date': past_date,
                'home_team': match['home_team'] if i % 2 == 0 else f"Team H{i}",
                'away_team': f"Team H{i}" if i % 2 == 0 else match['home_team'],
                'score': f"{home_goals_for}-{home_goals_against}" if i % 2 == 0 else f"{home_goals_against}-{home_goals_for}",
                'result': home_result,
                'league': match['league']
            })
            
            away_form.append({
                'date': past_date,
                'home_team': match['away_team'] if i % 2 == 0 else f"Team A{i}",
                'away_team': f"Team A{i}" if i % 2 == 0 else match['away_team'],
                'score': f"{away_goals_for}-{away_goals_against}" if i % 2 == 0 else f"{away_goals_against}-{away_goals_for}",
                'result': away_result,
                'league': match['league']
            })
        
        # Simuler les confrontations directes
        h2h = []
        for i in range(3):
            # Date du match récent
            past_date = (datetime.now() - timedelta(days=i*90 + 30)).strftime('%Y-%m-%d')
            
            # Résultat du match
            home_goals = random.choices(range(4), weights=[0.3, 0.4, 0.2, 0.1])[0]
            away_goals = random.choices(range(4), weights=[0.3, 0.4, 0.2, 0.1])[0]
            
            home_team_h2h = match['home_team'] if i % 2 == 0 else match['away_team']
            away_team_h2h = match['away_team'] if i % 2 == 0 else match['home_team']
            
            h2h.append({
                'date': past_date,
                'home_team': home_team_h2h,
                'away_team': away_team_h2h,
                'score': f"{home_goals}-{away_goals}",
                'league': match['league']
            })
        
        enriched_match['home_form'] = home_form
        enriched_match['away_form'] = away_form
        enriched_match['head_to_head'] = h2h
        
        # Simuler des compositions d'équipes
        positions = {
            'G': 'Goalkeeper',
            'D': 'Defender',
            'M': 'Midfielder',
            'F': 'Forward'
        }
        
        first_names = ["John", "James", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
                     "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Kenneth", "George"]
        
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
                    "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson"]
        
        lineups = {
            'home': {
                'team_name': match['home_team'],
                'formation': random.choice(['4-4-2', '4-3-3', '4-2-3-1', '3-5-2']),
                'coach': f"{random.choice(first_names)} {random.choice(last_names)}",
                'starting': [],
                'substitutes': []
            },
            'away': {
                'team_name': match['away_team'],
                'formation': random.choice(['4-4-2', '4-3-3', '4-2-3-1', '3-5-2']),
                'coach': f"{random.choice(first_names)} {random.choice(last_names)}",
                'starting': [],
                'substitutes': []
            },
            'status': random.choice(['official', 'probable'])
        }
        
        # Générer 11 titulaires et 7 remplaçants pour chaque équipe
        for side in ['home', 'away']:
            # Titulaires
            for i in range(11):
                pos_code = 'G' if i == 0 else ('D' if i < 5 else ('M' if i < 9 else 'F'))
                lineups[side]['starting'].append({
                    'name': f"{random.choice(first_names)} {random.choice(last_names)}",
                    'number': str(i + 1),
                    'position': positions[pos_code]
                })
            
            # Remplaçants
            for i in range(7):
                pos_code = random.choice(['G', 'D', 'M', 'F'])
                lineups[side]['substitutes'].append({
                    'name': f"{random.choice(first_names)} {random.choice(last_names)}",
                    'number': str(i + 12),
                    'position': positions[pos_code]
                })
        
        enriched_match['lineups'] = lineups
        
        # Simuler des statistiques avancées
        advanced_stats = {
            'home_team': match['home_team'],
            'away_team': match['away_team'],
            'home': {},
            'away': {},
            'categories': ['Attack', 'Ball Possession', 'Discipline', 'Passing']
        }
        
        # Statistiques d'attaque
        advanced_stats['home']['Attack'] = {
            'Goal Attempts': random.randint(8, 20),
            'Shots on Goal': random.randint(3, 10),
            'Corner Kicks': random.randint(2, 10),
            'Offsides': random.randint(0, 5)
        }
        
        advanced_stats['away']['Attack'] = {
            'Goal Attempts': random.randint(6, 18),
            'Shots on Goal': random.randint(2, 9),
            'Corner Kicks': random.randint(2, 8),
            'Offsides': random.randint(0, 6)
        }
        
        # Possession
        home_possession = random.uniform(0.35, 0.65)
        away_possession = 1 - home_possession
        
        advanced_stats['home']['Ball Possession'] = {
            'Ball Possession': home_possession
        }
        
        advanced_stats['away']['Ball Possession'] = {
            'Ball Possession': away_possession
        }
        
        # Discipline
        advanced_stats['home']['Discipline'] = {
            'Yellow Cards': random.randint(0, 5),
            'Red Cards': random.randint(0, 1),
            'Fouls': random.randint(5, 15)
        }
        
        advanced_stats['away']['Discipline'] = {
            'Yellow Cards': random.randint(0, 5),
            'Red Cards': random.randint(0, 1),
            'Fouls': random.randint(5, 15)
        }
        
        # Passes
        home_total_passes = random.randint(300, 700)
        home_accurate_passes = int(home_total_passes * random.uniform(0.7, 0.9))
        
        away_total_passes = random.randint(250, 650)
        away_accurate_passes = int(away_total_passes * random.uniform(0.7, 0.9))
        
        advanced_stats['home']['Passing'] = {
            'Total Passes': home_total_passes,
            'Accurate Passes': home_accurate_passes
        }
        
        advanced_stats['away']['Passing'] = {
            'Total Passes': away_total_passes,
            'Accurate Passes': away_accurate_passes
        }
        
        # Statistiques dérivées
        advanced_stats['home']['Derived'] = {
            'Conversion Rate': advanced_stats['home']['Attack']['Shots on Goal'] / advanced_stats['home']['Attack']['Goal Attempts'],
            'Pass Efficiency': home_accurate_passes / home_total_passes
        }
        
        advanced_stats['away']['Derived'] = {
            'Conversion Rate': advanced_stats['away']['Attack']['Shots on Goal'] / advanced_stats['away']['Attack']['Goal Attempts'],
            'Pass Efficiency': away_accurate_passes / away_total_passes
        }
        
        advanced_stats['categories'].append('Derived')
        
        enriched_match['advanced_stats'] = advanced_stats
        
        return enriched_match
    
    def enrich_matches_data(self, matches):
        """
        Enrichit les données d'une liste de matchs.
        
        Args:
            matches (list): Liste de matchs à enrichir
            
        Returns:
            list: Liste des matchs avec données enrichies
        """
        enriched_matches = []
        
        for match in matches:
            try:
                enriched_match = self.enrich_match_data(match)
                enriched_matches.append(enriched_match)
            except Exception as e:
                logger.error(f"Erreur lors de l'enrichissement du match {match.get('id')}: {e}")
                enriched_matches.append(match)
        
        return enriched_matches
    
    def get_comparative_analysis(self, match_id):
        """
        Génère une analyse comparative approfondie pour un match spécifique.
        
        Args:
            match_id (str): Identifiant du match à analyser
            
        Returns:
            dict: Analyse comparative détaillée
        """
        try:
            logger.info(f"Génération d'une analyse comparative pour le match {match_id}")
            
            # Si c'est un match d'exemple, générer une analyse d'exemple
            if str(match_id).startswith('sample_'):
                return self._generate_sample_comparative_analysis(match_id)
            
            # Récupérer les données du match
            match_details = self.flash_scraper.get_match_details(match_id)
            
            if not match_details:
                logger.warning(f"Aucune donnée trouvée pour le match {match_id}")
                return {}
            
            # Enrichir le match
            enriched_match = self.enrich_match_data(match_details)
            
            # Récupérer les compositions d'équipes
            lineups = enriched_match.get('lineups', {})
            
            # Récupérer les statistiques avancées
            advanced_stats = enriched_match.get('advanced_stats', {})
            
            # Structure de l'analyse comparative
            comparative_analysis = {
                'match_info': {
                    'id': match_id,
                    'home_team': enriched_match.get('home_team', ''),
                    'away_team': enriched_match.get('away_team', ''),
                    'league': enriched_match.get('league', ''),
                    'date': enriched_match.get('date', ''),
                    'time': enriched_match.get('time', '')
                },
                'form_comparison': self._analyze_form_comparison(enriched_match),
                'statistical_comparison': self._analyze_statistical_comparison(advanced_stats),
                'tactical_comparison': self._analyze_tactical_comparison(lineups),
                'h2h_analysis': self._analyze_h2h(enriched_match.get('head_to_head', [])),
                'key_player_comparison': self._analyze_key_players(lineups),
                'betting_patterns': self._analyze_betting_patterns(enriched_match)
            }
            
            return comparative_analysis
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de l'analyse comparative: {e}")
            return {}
    
    def _analyze_form_comparison(self, match_data):
        """
        Analyse la forme récente des deux équipes.
        
        Args:
            match_data (dict): Données enrichies du match
            
        Returns:
            dict: Analyse comparative de la forme
        """
        home_form = match_data.get('home_form', [])
        away_form = match_data.get('away_form', [])
        
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # Calculer les stats de forme
        home_wins = sum(1 for m in home_form if m.get('result') == 'W')
        home_draws = sum(1 for m in home_form if m.get('result') == 'D')
        home_losses = sum(1 for m in home_form if m.get('result') == 'L')
        
        away_wins = sum(1 for m in away_form if m.get('result') == 'W')
        away_draws = sum(1 for m in away_form if m.get('result') == 'D')
        away_losses = sum(1 for m in away_form if m.get('result') == 'L')
        
        # Calculer les buts marqués/encaissés
        home_goals_for = 0
        home_goals_against = 0
        
        for m in home_form:
            try:
                score = m.get('score', '0-0').split('-')
                if len(score) == 2:
                    if m.get('home_team') == home_team:
                        home_goals_for += int(score[0])
                        home_goals_against += int(score[1])
                    else:
                        home_goals_for += int(score[1])
                        home_goals_against += int(score[0])
            except:
                pass
        
        away_goals_for = 0
        away_goals_against = 0
        
        for m in away_form:
            try:
                score = m.get('score', '0-0').split('-')
                if len(score) == 2:
                    if m.get('home_team') == away_team:
                        away_goals_for += int(score[0])
                        away_goals_against += int(score[1])
                    else:
                        away_goals_for += int(score[1])
                        away_goals_against += int(score[0])
            except:
                pass
        
        # Calculer les points
        home_points = home_wins * 3 + home_draws
        away_points = away_wins * 3 + away_draws
        
        # Calculer les moyennes
        home_matches = len(home_form)
        away_matches = len(away_form)
        
        home_avg_goals_for = home_goals_for / home_matches if home_matches > 0 else 0
        home_avg_goals_against = home_goals_against / home_matches if home_matches > 0 else 0
        
        away_avg_goals_for = away_goals_for / away_matches if away_matches > 0 else 0
        away_avg_goals_against = away_goals_against / away_matches if away_matches > 0 else 0
        
        # Tendance (points des 3 derniers matchs vs points des 2 matchs précédents)
        home_recent_points = sum(3 if m.get('result') == 'W' else 1 if m.get('result') == 'D' else 0 for m in home_form[:3])
        home_earlier_points = sum(3 if m.get('result') == 'W' else 1 if m.get('result') == 'D' else 0 for m in home_form[3:5] if len(home_form) > 3)
        
        away_recent_points = sum(3 if m.get('result') == 'W' else 1 if m.get('result') == 'D' else 0 for m in away_form[:3])
        away_earlier_points = sum(3 if m.get('result') == 'W' else 1 if m.get('result') == 'D' else 0 for m in away_form[3:5] if len(away_form) > 3)
        
        home_trend = 'stable'
        if home_recent_points > home_earlier_points * (3/2) and home_earlier_points > 0:
            home_trend = 'improving'
        elif home_recent_points * (3/2) < home_earlier_points and home_recent_points > 0:
            home_trend = 'declining'
        
        away_trend = 'stable'
        if away_recent_points > away_earlier_points * (3/2) and away_earlier_points > 0:
            away_trend = 'improving'
        elif away_recent_points * (3/2) < away_earlier_points and away_recent_points > 0:
            away_trend = 'declining'
        
        return {
            'home': {
                'team': home_team,
                'wins': home_wins,
                'draws': home_draws,
                'losses': home_losses,
                'goals_for': home_goals_for,
                'goals_against': home_goals_against,
                'points': home_points,
                'form_string': ''.join(['W' if m.get('result') == 'W' else 'D' if m.get('result') == 'D' else 'L' for m in home_form]),
                'avg_goals_for': home_avg_goals_for,
                'avg_goals_against': home_avg_goals_against,
                'trend': home_trend
            },
            'away': {
                'team': away_team,
                'wins': away_wins,
                'draws': away_draws,
                'losses': away_losses,
                'goals_for': away_goals_for,
                'goals_against': away_goals_against,
                'points': away_points,
                'form_string': ''.join(['W' if m.get('result') == 'W' else 'D' if m.get('result') == 'D' else 'L' for m in away_form]),
                'avg_goals_for': away_avg_goals_for,
                'avg_goals_against': away_avg_goals_against,
                'trend': away_trend
            },
            'advantage': 'home' if home_points > away_points else 'away' if away_points > home_points else 'neutral',
            'form_difference': home_points - away_points
        }
    
    def _analyze_statistical_comparison(self, advanced_stats):
        """
        Analyse les statistiques avancées des deux équipes.
        
        Args:
            advanced_stats (dict): Statistiques avancées du match
            
        Returns:
            dict: Analyse comparative des statistiques
        """
        if not advanced_stats or 'home' not in advanced_stats or 'away' not in advanced_stats:
            return {}
        
        comparison = {}
        
        for category in advanced_stats.get('categories', []):
            home_category = advanced_stats['home'].get(category, {})
            away_category = advanced_stats['away'].get(category, {})
            
            comparison[category] = {}
            
            for stat_name in set(list(home_category.keys()) + list(away_category.keys())):
                home_value = home_category.get(stat_name, 0)
                away_value = away_category.get(stat_name, 0)
                
                # Déterminer l'avantage
                advantage = 'neutral'
                
                # Pour la possession, les passes et les tirs, plus c'est mieux
                if category in ['Ball Possession', 'Attack', 'Passing'] and stat_name not in ['Offsides']:
                    advantage = 'home' if home_value > away_value else 'away' if away_value > home_value else 'neutral'
                
                # Pour la discipline, moins c'est mieux
                elif category == 'Discipline':
                    advantage = 'home' if home_value < away_value else 'away' if away_value < home_value else 'neutral'
                
                # Pour le taux de conversion et l'efficacité des passes, plus c'est mieux
                elif category == 'Derived':
                    advantage = 'home' if home_value > away_value else 'away' if away_value > home_value else 'neutral'
                
                # Calculer la différence
                difference = None
                try:
                    if isinstance(home_value, (int, float)) and isinstance(away_value, (int, float)):
                        difference = home_value - away_value
                except:
                    pass
                
                comparison[category][stat_name] = {
                    'home': home_value,
                    'away': away_value,
                    'advantage': advantage,
                    'difference': difference
                }
        
        # Calculer l'avantage statistique global
        attacking_advantage = 'neutral'
        possession_advantage = 'neutral'
        discipline_advantage = 'neutral'
        passing_advantage = 'neutral'
        
        # Avantage offensif
        if 'Attack' in comparison:
            home_attack_points = 0
            away_attack_points = 0
            
            for stat in comparison['Attack'].values():
                if stat['advantage'] == 'home':
                    home_attack_points += 1
                elif stat['advantage'] == 'away':
                    away_attack_points += 1
            
            attacking_advantage = 'home' if home_attack_points > away_attack_points else 'away' if away_attack_points > home_attack_points else 'neutral'
        
        # Avantage possession
        if 'Ball Possession' in comparison and 'Ball Possession' in comparison['Ball Possession']:
            possession_advantage = comparison['Ball Possession']['Ball Possession']['advantage']
        
        # Avantage discipline
        if 'Discipline' in comparison:
            home_discipline_points = 0
            away_discipline_points = 0
            
            for stat in comparison['Discipline'].values():
                if stat['advantage'] == 'home':
                    home_discipline_points += 1
                elif stat['advantage'] == 'away':
                    away_discipline_points += 1
            
            discipline_advantage = 'home' if home_discipline_points > away_discipline_points else 'away' if away_discipline_points > home_discipline_points else 'neutral'
        
        # Avantage passes
        if 'Passing' in comparison:
            home_passing_points = 0
            away_passing_points = 0
            
            for stat in comparison['Passing'].values():
                if stat['advantage'] == 'home':
                    home_passing_points += 1
                elif stat['advantage'] == 'away':
                    away_passing_points += 1
            
            passing_advantage = 'home' if home_passing_points > away_passing_points else 'away' if away_passing_points > home_passing_points else 'neutral'
        
        # Avantage global
        advantages = {
            'home': sum(1 for adv in [attacking_advantage, possession_advantage, discipline_advantage, passing_advantage] if adv == 'home'),
            'away': sum(1 for adv in [attacking_advantage, possession_advantage, discipline_advantage, passing_advantage] if adv == 'away'),
            'neutral': sum(1 for adv in [attacking_advantage, possession_advantage, discipline_advantage, passing_advantage] if adv == 'neutral')
        }
        
        overall_advantage = 'home' if advantages['home'] > advantages['away'] else 'away' if advantages['away'] > advantages['home'] else 'neutral'
        
        comparison['overall'] = {
            'attacking_advantage': attacking_advantage,
            'possession_advantage': possession_advantage,
            'discipline_advantage': discipline_advantage,
            'passing_advantage': passing_advantage,
            'overall_advantage': overall_advantage
        }
        
        return comparison
    
    def _analyze_tactical_comparison(self, lineups):
        """
        Analyse les aspects tactiques basés sur les compositions d'équipes.
        
        Args:
            lineups (dict): Compositions d'équipes
            
        Returns:
            dict: Analyse comparative tactique
        """
        if not lineups or 'home' not in lineups or 'away' not in lineups:
            return {}
        
        home_formation = lineups['home'].get('formation', '')
        away_formation = lineups['away'].get('formation', '')
        
        # Analyser les formations
        home_formation_parts = home_formation.split('-') if home_formation else []
        away_formation_parts = away_formation.split('-') if away_formation else []
        
        home_defenders = int(home_formation_parts[0]) if len(home_formation_parts) > 0 else 0
        home_midfielders = sum(int(p) for p in home_formation_parts[1:-1]) if len(home_formation_parts) > 2 else 0
        home_forwards = int(home_formation_parts[-1]) if len(home_formation_parts) > 0 else 0
        
        away_defenders = int(away_formation_parts[0]) if len(away_formation_parts) > 0 else 0
        away_midfielders = sum(int(p) for p in away_formation_parts[1:-1]) if len(away_formation_parts) > 2 else 0
        away_forwards = int(away_formation_parts[-1]) if len(away_formation_parts) > 0 else 0
        
        # Déterminer le style de jeu probable
        home_style = 'balanced'
        if home_defenders > 4 and home_forwards < 2:
            home_style = 'defensive'
        elif home_defenders < 4 and home_forwards > 2:
            home_style = 'attacking'
        elif home_midfielders > 5:
            home_style = 'possession'
        
        away_style = 'balanced'
        if away_defenders > 4 and away_forwards < 2:
            away_style = 'defensive'
        elif away_defenders < 4 and away_forwards > 2:
            away_style = 'attacking'
        elif away_midfielders > 5:
            away_style = 'possession'
        
        # Compter les joueurs par position
        home_positions = {'Goalkeeper': 0, 'Defender': 0, 'Midfielder': 0, 'Forward': 0}
        away_positions = {'Goalkeeper': 0, 'Defender': 0, 'Midfielder': 0, 'Forward': 0}
        
        for player in lineups['home'].get('starting', []):
            position = player.get('position', '')
            if position in home_positions:
                home_positions[position] += 1
        
        for player in lineups['away'].get('starting', []):
            position = player.get('position', '')
            if position in away_positions:
                away_positions[position] += 1
        
        return {
            'home': {
                'formation': home_formation,
                'defenders': home_defenders,
                'midfielders': home_midfielders,
                'forwards': home_forwards,
                'style': home_style,
                'positions': home_positions
            },
            'away': {
                'formation': away_formation,
                'defenders': away_defenders,
                'midfielders': away_midfielders,
                'forwards': away_forwards,
                'style': away_style,
                'positions': away_positions
            },
            'tactical_matchup': {
                'home_attacking_advantage': home_forwards > away_defenders,
                'away_attacking_advantage': away_forwards > home_defenders,
                'midfield_control': 'home' if home_midfielders > away_midfielders else 'away' if away_midfielders > home_midfielders else 'neutral',
                'style_matchup': f"{home_style} vs {away_style}"
            }
        }
    
    def _analyze_h2h(self, h2h_matches):
        """
        Analyse l'historique des confrontations directes.
        
        Args:
            h2h_matches (list): Liste des confrontations directes
            
        Returns:
            dict: Analyse des confrontations directes
        """
        if not h2h_matches:
            return {}
        
        home_wins = 0
        away_wins = 0
        draws = 0
        
        total_goals = 0
        home_team_goals = 0
        away_team_goals = 0
        
        both_teams_scored_count = 0
        over_2_5_count = 0
        
        # Analyser chaque match H2H
        for match in h2h_matches:
            try:
                score = match.get('score', '0-0').split('-')
                if len(score) == 2:
                    home_score = int(score[0])
                    away_score = int(score[1])
                    
                    total_goals += home_score + away_score
                    
                    if match.get('home_team') == h2h_matches[0].get('home_team'):
                        home_team_goals += home_score
                        away_team_goals += away_score
                    else:
                        home_team_goals += away_score
                        away_team_goals += home_score
                    
                    if home_score > away_score:
                        if match.get('home_team') == h2h_matches[0].get('home_team'):
                            home_wins += 1
                        else:
                            away_wins += 1
                    elif away_score > home_score:
                        if match.get('home_team') == h2h_matches[0].get('home_team'):
                            away_wins += 1
                        else:
                            home_wins += 1
                    else:
                        draws += 1
                    
                    # BTTS
                    if home_score > 0 and away_score > 0:
                        both_teams_scored_count += 1
                    
                    # Over 2.5
                    if home_score + away_score > 2:
                        over_2_5_count += 1
            except:
                pass
        
        total_matches = len(h2h_matches)
        
        # Calculer les moyennes et pourcentages
        avg_goals = total_goals / total_matches if total_matches > 0 else 0
        btts_rate = both_teams_scored_count / total_matches if total_matches > 0 else 0
        over_2_5_rate = over_2_5_count / total_matches if total_matches > 0 else 0
        
        home_win_rate = home_wins / total_matches if total_matches > 0 else 0
        away_win_rate = away_wins / total_matches if total_matches > 0 else 0
        draw_rate = draws / total_matches if total_matches > 0 else 0
        
        return {
            'matches_count': total_matches,
            'home_wins': home_wins,
            'away_wins': away_wins,
            'draws': draws,
            'home_win_rate': home_win_rate,
            'away_win_rate': away_win_rate,
            'draw_rate': draw_rate,
            'total_goals': total_goals,
            'avg_goals': avg_goals,
            'home_team_goals': home_team_goals,
            'away_team_goals': away_team_goals,
            'both_teams_scored_count': both_teams_scored_count,
            'btts_rate': btts_rate,
            'over_2_5_count': over_2_5_count,
            'over_2_5_rate': over_2_5_rate,
            'h2h_advantage': 'home' if home_wins > away_wins else 'away' if away_wins > home_wins else 'neutral'
        }
    
    def _analyze_key_players(self, lineups):
        """
        Analyse les joueurs clés dans les compositions.
        
        Args:
            lineups (dict): Compositions d'équipes
            
        Returns:
            dict: Analyse des joueurs clés
        """
        if not lineups or 'home' not in lineups or 'away' not in lineups:
            return {}
        
        # Pour une analyse réelle, nous aurions besoin de données sur les joueurs
        # Pour l'instant, nous simulons quelques analyses de base
        
        home_players = lineups['home'].get('starting', [])
        away_players = lineups['away'].get('starting', [])
        
        # Identifier quelques joueurs "clés" (dans un cas réel, on utiliserait des statistiques)
        home_key_players = []
        away_key_players = []
        
        # Sélectionner quelques joueurs par poste
        for player in home_players:
            position = player.get('position', '')
            if position == 'Goalkeeper' or position == 'Forward' or (position == 'Midfielder' and random.random() > 0.7):
                home_key_players.append(player)
        
        for player in away_players:
            position = player.get('position', '')
            if position == 'Goalkeeper' or position == 'Forward' or (position == 'Midfielder' and random.random() > 0.7):
                away_key_players.append(player)
        
        return {
            'home_key_players': home_key_players,
            'away_key_players': away_key_players,
            'home_coach': lineups['home'].get('coach', 'Unknown'),
            'away_coach': lineups['away'].get('coach', 'Unknown')
        }
    
    def _analyze_betting_patterns(self, match_data):
        """
        Analyse les tendances de paris pour le match.
        
        Args:
            match_data (dict): Données enrichies du match
            
        Returns:
            dict: Analyse des tendances de paris
        """
        odds = match_data.get('odds', {})
        
        if not odds:
            return {}
        
        # Calculer quelques indicateurs basés sur les cotes
        home_odds = float(odds.get('1', 0))
        draw_odds = float(odds.get('X', 0))
        away_odds = float(odds.get('2', 0))
        
        if home_odds <= 0 or draw_odds <= 0 or away_odds <= 0:
            return {}
        
        # Calculer les probabilités implicites
        home_prob = 1 / home_odds
        draw_prob = 1 / draw_odds
        away_prob = 1 / away_odds
        
        # Normaliser les probabilités (retirer la marge du bookmaker)
        total_prob = home_prob + draw_prob + away_prob
        home_prob_normalized = home_prob / total_prob
        draw_prob_normalized = draw_prob / total_prob
        away_prob_normalized = away_prob / total_prob
        
        # Déterminer la tendance du marché
        market_favorite = 'home' if home_prob_normalized > away_prob_normalized else 'away' if away_prob_normalized > home_prob_normalized else 'neutral'
        
        # Classer la confiance du marché
        market_confidence = 'low'
        if max(home_prob_normalized, away_prob_normalized) > 0.6:
            market_confidence = 'high'
        elif max(home_prob_normalized, away_prob_normalized) > 0.45:
            market_confidence = 'medium'
        
        # Autres marchés
        over_under_bias = 'neutral'
        if 'Over 2.5' in odds and 'Under 2.5' in odds:
            over_odds = float(odds.get('Over 2.5', 0))
            under_odds = float(odds.get('Under 2.5', 0))
            
            if over_odds > 0 and under_odds > 0:
                over_prob = 1 / over_odds
                under_prob = 1 / under_odds
                
                total_ou_prob = over_prob + under_prob
                over_prob_normalized = over_prob / total_ou_prob
                
                over_under_bias = 'over' if over_prob_normalized > 0.52 else 'under' if over_prob_normalized < 0.48 else 'neutral'
        
        btts_bias = 'neutral'
        if 'BTTS Yes' in odds and 'BTTS No' in odds:
            btts_yes_odds = float(odds.get('BTTS Yes', 0))
            btts_no_odds = float(odds.get('BTTS No', 0))
            
            if btts_yes_odds > 0 and btts_no_odds > 0:
                btts_yes_prob = 1 / btts_yes_odds
                btts_no_prob = 1 / btts_no_odds
                
                total_btts_prob = btts_yes_prob + btts_no_prob
                btts_yes_prob_normalized = btts_yes_prob / total_btts_prob
                
                btts_bias = 'yes' if btts_yes_prob_normalized > 0.52 else 'no' if btts_yes_prob_normalized < 0.48 else 'neutral'
        
        return {
            'odds': {
                'home': home_odds,
                'draw': draw_odds,
                'away': away_odds,
                'over_2_5': odds.get('Over 2.5', 0),
                'under_2_5': odds.get('Under 2.5', 0),
                'btts_yes': odds.get('BTTS Yes', 0),
                'btts_no': odds.get('BTTS No', 0)
            },
            'implied_probabilities': {
                'home': home_prob_normalized,
                'draw': draw_prob_normalized,
                'away': away_prob_normalized
            },
            'market_trends': {
                'favorite': market_favorite,
                'confidence': market_confidence,
                'over_under_bias': over_under_bias,
                'btts_bias': btts_bias
            }
        }
    
    def _generate_sample_comparative_analysis(self, match_id):
        """
        Génère une analyse comparative d'exemple pour un match.
        
        Args:
            match_id (str): Identifiant du match
            
        Returns:
            dict: Analyse comparative d'exemple
        """
        # Extraire les infos de base à partir de l'identifiant
        parts = match_id.split('_')
        league = parts[1].replace('_', ' ') if len(parts) > 1 else "Sample League"
        
        # Générer un match d'exemple
        teams = {
            "English Premier League": [
                "Manchester City", "Liverpool", "Arsenal", "Manchester United",
                "Tottenham", "Chelsea", "Newcastle", "Aston Villa"
            ],
            "Spanish La Liga": [
                "Real Madrid", "Barcelona", "Atletico Madrid", "Real Sociedad",
                "Villarreal", "Athletic Bilbao", "Real Betis", "Valencia"
            ],
            "Italian Serie A": [
                "Inter Milan", "AC Milan", "Juventus", "Napoli",
                "Roma", "Lazio", "Atalanta", "Fiorentina"
            ],
            "German Bundesliga": [
                "Bayern Munich", "Borussia Dortmund", "RB Leipzig", "Bayer Leverkusen",
                "Eintracht Frankfurt", "Wolfsburg", "Borussia Monchengladbach", "Hoffenheim"
            ],
            "French Ligue 1": [
                "Paris Saint-Germain", "Marseille", "Monaco", "Lyon",
                "Lille", "Rennes", "Nice", "Lens"
            ]
        }
        
        # Choisir deux équipes
        league_teams = teams.get(league, teams["English Premier League"])
        home_team = random.choice(league_teams)
        away_team = random.choice([team for team in league_teams if team != home_team])
        
        # Créer un match d'exemple
        match = {
            'id': match_id,
            'home_team': home_team,
            'away_team': away_team,
            'league': league,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M')
        }
        
        # Enrichir le match
        enriched_match = self._enrich_sample_match(match)
        
        # Créer l'analyse comparative
        comparative_analysis = {
            'match_info': {
                'id': match_id,
                'home_team': home_team,
                'away_team': away_team,
                'league': league,
                'date': match['date'],
                'time': match['time']
            },
            'form_comparison': self._analyze_form_comparison(enriched_match),
            'statistical_comparison': self._analyze_statistical_comparison(enriched_match.get('advanced_stats', {})),
            'tactical_comparison': self._analyze_tactical_comparison(enriched_match.get('lineups', {})),
            'h2h_analysis': self._analyze_h2h(enriched_match.get('head_to_head', [])),
            'key_player_comparison': self._analyze_key_players(enriched_match.get('lineups', {})),
            'betting_patterns': self._analyze_betting_patterns(enriched_match)
        }
        
        return comparative_analysis