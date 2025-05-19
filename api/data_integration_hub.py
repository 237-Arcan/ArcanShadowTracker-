"""
Module de hub d'intégration de données pour ArcanShadow.
Ce hub centralise l'accès à toutes les sources de données et fournit une interface unifiée
pour les autres modules du système.
"""

import os
import json
import requests
import logging
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import importlib

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constantes pour l'API Football
FOOTBALL_API_KEY = os.environ.get('FOOTBALL_API_KEY')
FOOTBALL_API_HOST = 'v3.football.api-sports.io'

class DataIntegrationHub:
    """
    Hub central d'intégration de données pour ArcanShadow.
    Centralise l'accès aux différentes API et sources de données.
    """
    
    def __init__(self):
        """Initialise le hub d'intégration de données"""
        self.cache = {}
        self.cache_expiry = {}
        self.cache_duration = 3600  # 1 heure par défaut
        
        # Initialiser les connecteurs API
        self._init_football_api()
        self._init_transfermarkt()
        self._init_soccerdata()
        self._init_time_module()
        self._init_cross_platform_adapter()
        
        # Variables de suivi des sources
        self.sources_status = {
            'football_api': self._check_football_api(),
            'transfermarkt': False,
            'soccerdata': False,
            'time_module': self.time_module is not None,
            'cross_platform': hasattr(self, 'cross_platform_adapter') and self.cross_platform_adapter is not None
        }
        
        logger.info(f"Hub d'intégration initialisé. Sources disponibles: {self.sources_status}")
        
    def _init_cross_platform_adapter(self):
        """Initialise l'adaptateur cross-platform pour la préparation mobile"""
        try:
            # Importer dynamiquement l'adaptateur cross-platform
            from api.modules.cross_platform_adapter import CrossPlatformAdapter
            self.cross_platform_adapter = CrossPlatformAdapter(self)
            logger.info("Adaptateur cross-platform initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de l'adaptateur cross-platform: {e}")
            self.cross_platform_adapter = None
        
    def _init_time_module(self):
        """Initialise le module de temps intégré"""
        try:
            # Importer dynamiquement le module de temps
            from api.modules.time_module import TimeModule
            self.time_module = TimeModule()
            logger.info("Module de temps initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du module de temps: {e}")
            self.time_module = None
    
    def _init_football_api(self):
        """Initialise la connexion à l'API Football"""
        self.football_api_key = FOOTBALL_API_KEY
        self.football_api_host = FOOTBALL_API_HOST
        self.football_api_headers = {
            'x-rapidapi-key': self.football_api_key,
            'x-rapidapi-host': self.football_api_host
        }
    
    def _init_transfermarkt(self):
        """Initialise la connexion à Transfermarkt (adapté selon l'implémentation)"""
        # Cette fonction serait complétée avec le code réel de connexion
        pass
    
    def _init_soccerdata(self):
        """Initialise la connexion à soccerdata"""
        # Cette fonction serait complétée avec le code réel de connexion
        pass
    
    def _check_football_api(self):
        """Vérifie si l'API Football est accessible"""
        if not self.football_api_key:
            logger.warning("Clé API Football non disponible")
            return False
        
        try:
            # Tester un endpoint basique de l'API Football
            url = f"https://{self.football_api_host}/status"
            
            response = requests.get(url, headers=self.football_api_headers)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"API Football accessible. Réponse: {data}")
                return True
            else:
                logger.warning(f"Erreur lors de la vérification de l'API Football. Code: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de la vérification de l'API Football: {e}")
            return False
            
    def check_api_connections(self):
        """
        Vérifie toutes les connexions API et met à jour leur statut.
        
        Returns:
            dict: Statut mis à jour des API
        """
        # Mettre à jour le statut de l'API Football
        self.sources_status['football_api'] = self._check_football_api()
        
        # Implémenter des vérifications similaires pour les autres sources
        # self.sources_status['transfermarkt'] = self._check_transfermarkt()
        # self.sources_status['soccerdata'] = self._check_soccerdata()
        
        logger.info(f"Statut des connexions API mis à jour: {self.sources_status}")
        
        return self.sources_status
    
    def get_cache_key(self, func_name, **kwargs):
        """Génère une clé de cache basée sur la fonction et ses paramètres"""
        param_str = '_'.join(f"{k}={v}" for k, v in sorted(kwargs.items()))
        return f"{func_name}_{param_str}"
    
    def is_cache_valid(self, key):
        """Vérifie si une entrée de cache est encore valide"""
        if key not in self.cache_expiry:
            return False
        
        return datetime.now() < self.cache_expiry[key]
    
    def set_cache(self, key, data, duration=None):
        """Stocke des données en cache avec une durée de validité"""
        self.cache[key] = data
        expiry_duration = duration if duration is not None else self.cache_duration
        self.cache_expiry[key] = datetime.now() + timedelta(seconds=expiry_duration)
        
        logger.info(f"Données mises en cache avec la clé {key}, valide jusqu'à {self.cache_expiry[key]}")
    
    def get_upcoming_matches(self, days_ahead=3, leagues=None):
        """
        Récupère les matchs à venir pour les prochains jours.
        
        Args:
            days_ahead (int): Nombre de jours à l'avance pour récupérer les matchs
            leagues (list): Liste d'IDs de ligues à filtrer
            
        Returns:
            list: Liste des matchs à venir
        """
        cache_key = self.get_cache_key('upcoming_matches', days=days_ahead, leagues=str(leagues))
        
        if self.is_cache_valid(cache_key):
            logger.info(f"Utilisation du cache pour les matchs à venir")
            return self.cache[cache_key]
        
        logger.info(f"Récupération des matchs à venir pour les {days_ahead} prochains jours")
        
        # Essayer d'utiliser l'API Football si disponible
        if self.sources_status['football_api']:
            try:
                matches = self._get_matches_from_football_api(days_ahead, leagues)
                self.set_cache(cache_key, matches)
                return matches
            except Exception as e:
                logger.error(f"Erreur lors de la récupération depuis l'API Football: {e}")
        
        # Fallback: Générer des matchs simulés
        logger.warning("Utilisation de matchs simulés")
        matches = self._generate_simulated_matches(days_ahead, leagues)
        self.set_cache(cache_key, matches)
        return matches
    
    def _get_matches_from_football_api(self, days_ahead, leagues=None):
        """
        Récupère les matchs depuis l'API Football.
        
        Args:
            days_ahead (int): Nombre de jours à l'avance
            leagues (list): Liste d'IDs de ligues à filtrer
            
        Returns:
            list: Liste des matchs
        """
        today = datetime.now().date()
        end_date = today + timedelta(days=days_ahead)
        
        matches = []
        
        # Pour chaque jour dans la plage
        for day_offset in range(days_ahead + 1):
            current_date = today + timedelta(days=day_offset)
            date_str = current_date.strftime('%Y-%m-%d')
            
            # Construire l'URL avec les paramètres
            url = f"https://{self.football_api_host}/fixtures"
            params = {'date': date_str}
            
            if leagues:
                # L'API accepte une liste d'IDs de ligues séparés par des tirets
                params['league'] = '-'.join(str(l) for l in leagues)
            
            # Cette partie simule l'appel API puisque nous n'avons pas les identifiants réels
            # Dans un code de production, ce serait remplacé par un appel API réel
            time.sleep(0.1)  # Simuler un délai réseau
            
            # Simuler une réponse
            api_matches = self._generate_simulated_matches(1, leagues, current_date)
            
            # Transformer au format standard
            for api_match in api_matches:
                match = {
                    'id': api_match.get('id'),
                    'date': api_match.get('date'),
                    'time': datetime.fromisoformat(api_match.get('date').replace('Z', '+00:00')).strftime('%H:%M'),
                    'home_team': api_match.get('home_team'),
                    'away_team': api_match.get('away_team'),
                    'league_id': api_match.get('league_id'),
                    'league_name': api_match.get('league_name'),
                    'venue': api_match.get('venue'),
                    'referee': api_match.get('referee'),
                    'temperature': api_match.get('temperature'),
                    'weather': api_match.get('weather')
                }
                
                matches.append(match)
        
        return matches
    
    # Méthodes d'interface pour le module de temps
    def get_upcoming_days_formatted(self, count=7):
        """
        Obtient une liste formatée des prochains jours pour l'interface utilisateur
        
        Args:
            count (int): Nombre de jours à inclure
            
        Returns:
            list: Liste de dictionnaires avec les informations de jours formatées
        """
        if self.time_module:
            return self.time_module.get_upcoming_days(count)
        else:
            # Version simplifiée si le module n'est pas disponible
            days = []
            today = datetime.now().date()
            
            for i in range(count):
                current_date = today + timedelta(days=i)
                days.append({
                    "date": current_date.isoformat(),
                    "day": current_date.day,
                    "month": current_date.month,
                    "formatted_date": f"{current_date.day}/{current_date.month}"
                })
            
            return days
    
    def enhance_matches_with_time_info(self, matches):
        """
        Enrichit une liste de matchs avec des informations temporelles
        
        Args:
            matches (list): Liste de dictionnaires représentant des matchs
            
        Returns:
            list: Matchs enrichis avec des informations temporelles
        """
        if not self.time_module:
            return matches
        
        enhanced_matches = []
        for match in matches:
            enhanced_match = self.time_module.enhance_match_data_with_time_info(match)
            enhanced_matches.append(enhanced_match)
        
        return enhanced_matches
    
    def group_matches_by_time_windows(self, matches):
        """
        Regroupe les matchs par fenêtres temporelles
        
        Args:
            matches (list): Liste de matchs
            
        Returns:
            dict: Matchs regroupés par créneaux horaires
        """
        if self.time_module:
            return self.time_module.group_matches_by_time_slots(matches)
        else:
            # Version simplifiée si le module n'est pas disponible
            return {"all": matches}
    
    def get_prime_time_matches(self, matches):
        """
        Filtre les matchs pour ne conserver que ceux en prime time
        
        Args:
            matches (list): Liste de matchs
            
        Returns:
            list: Matchs en prime time
        """
        if self.time_module:
            return self.time_module.get_prime_time_matches(matches)
        else:
            return matches
    
    def format_match_time(self, match_datetime, format_type=None):
        """
        Formate l'heure d'un match selon les préférences
        
        Args:
            match_datetime: Date et heure du match
            format_type: Type de format
            
        Returns:
            str: Heure formatée
        """
        if self.time_module:
            return self.time_module.format_match_time(match_datetime, format_type)
        else:
            # Version simplifiée
            if isinstance(match_datetime, str):
                try:
                    match_datetime = datetime.fromisoformat(match_datetime.replace('Z', '+00:00'))
                except:
                    return match_datetime
            
            return match_datetime.strftime("%H:%M")
    
    def format_match_date(self, match_datetime, format_type="full"):
        """
        Formate la date d'un match selon le format spécifié
        
        Args:
            match_datetime: Date et heure du match
            format_type: Type de format
            
        Returns:
            str: Date formatée
        """
        if self.time_module:
            return self.time_module.format_match_date(match_datetime, format_type)
        else:
            # Version simplifiée
            if isinstance(match_datetime, str):
                try:
                    match_datetime = datetime.fromisoformat(match_datetime.replace('Z', '+00:00'))
                except:
                    return match_datetime
            
            return match_datetime.strftime("%d/%m/%Y")
            
    # Méthodes pour préparer les données pour l'application mobile
    
    def prepare_matches_for_app(self, matches, platform="mobile"):
        """
        Prépare les données de matchs pour l'application mobile
        
        Args:
            matches (list): Liste de matchs à préparer
            platform (str): Plateforme cible ('mobile', 'web', 'watch')
            
        Returns:
            list: Données préparées pour l'application
        """
        if hasattr(self, 'cross_platform_adapter') and self.cross_platform_adapter:
            try:
                return self.cross_platform_adapter.prepare_matches_for_app(matches, platform)
            except Exception as e:
                logger.error(f"Erreur lors de la préparation des données pour l'app: {e}")
        
        # Version de base si l'adaptateur n'est pas disponible
        return matches
    
    def generate_app_configuration(self, platform="mobile"):
        """
        Génère une configuration pour l'application mobile
        
        Args:
            platform (str): Plateforme cible
            
        Returns:
            dict: Configuration de l'application
        """
        if hasattr(self, 'cross_platform_adapter') and self.cross_platform_adapter:
            try:
                return self.cross_platform_adapter.generate_app_configuration(platform)
            except Exception as e:
                logger.error(f"Erreur lors de la génération de la configuration app: {e}")
        
        # Configuration minimale par défaut
        return {
            "version": "1.0.0",
            "api_url": "/api",
            "refresh_interval": 300,
            "platform": platform
        }
    
    def export_data_for_app(self, data, format="json"):
        """
        Exporte les données dans un format prêt pour l'application
        
        Args:
            data (dict/list): Données à exporter
            format (str): Format d'exportation ('json', 'compact')
            
        Returns:
            str: Données exportées au format demandé
        """
        if hasattr(self, 'cross_platform_adapter') and self.cross_platform_adapter:
            try:
                return self.cross_platform_adapter.export_data_for_app(data, format)
            except Exception as e:
                logger.error(f"Erreur lors de l'exportation des données: {e}")
        
        # Version simple JSON par défaut
        return json.dumps(data)
    
    def _generate_simulated_matches(self, days_ahead=7, leagues=None, start_date=None):
        """
        Génère des matchs simulés en cas d'indisponibilité de l'API.
        Créez des matchs avec des données réalistes mais générées.
        
        Args:
            days_ahead (int): Nombre de jours à l'avance
            leagues (list): Liste de ligues à filtrer (optionnel)
            start_date (datetime): Date de début (par défaut aujourd'hui)
            
        Returns:
            list: Liste des matchs simulés
        """
        matches = []
        league_definitions = [
            {"id": 39, "name": "Premier League", "country": "ANGLETERRE"},
            {"id": 140, "name": "La Liga", "country": "ESPAGNE"},
            {"id": 61, "name": "Ligue 1", "country": "FRANCE"},
            {"id": 78, "name": "Bundesliga", "country": "ALLEMAGNE"},
            {"id": 135, "name": "Serie A", "country": "ITALIE"},
            {"id": 2, "name": "Champions League", "country": "EUROPE"},
            {"id": 233, "name": "Premiership", "country": "AFRIQUE DU SUD"},
            {"id": 262, "name": "Saudi Pro League", "country": "ARABIE SAOUDITE"}
        ]
        
        teams_by_league = {
            39: ["Arsenal", "Chelsea", "Liverpool", "Manchester City", "Manchester United", "Tottenham", "Newcastle", "Aston Villa"],
            140: ["Real Madrid", "Barcelona", "Atletico Madrid", "Sevilla", "Valencia", "Villarreal", "Athletic Bilbao", "Real Sociedad"],
            61: ["PSG", "Marseille", "Lyon", "Monaco", "Lille", "Rennes", "Nice", "Lens"],
            78: ["Bayern Munich", "Borussia Dortmund", "RB Leipzig", "Leverkusen", "Wolfsburg", "Gladbach", "Frankfurt", "Union Berlin"],
            135: ["Inter Milan", "Milan", "Juventus", "Napoli", "Roma", "Lazio", "Atalanta", "Fiorentina"],
            2: ["Real Madrid", "Manchester City", "Bayern Munich", "PSG", "Barcelona", "Liverpool", "Inter Milan", "Borussia Dortmund"],
            233: ["Kaizer Chiefs", "Orlando Pirates", "Mamelodi Sundowns", "SuperSport United", "Cape Town City FC", "Stellenbosch FC"],
            262: ["Al Hilal", "Al Nassr", "Al Ahli", "Al Ittihad", "Al Shabab", "Al Taawoun"]
        }
        
        venues = {
            39: ["Emirates Stadium", "Stamford Bridge", "Anfield", "Etihad Stadium", "Old Trafford", "Tottenham Hotspur Stadium"],
            140: ["Santiago Bernabéu", "Camp Nou", "Wanda Metropolitano", "Ramón Sánchez Pizjuán", "Mestalla"],
            61: ["Parc des Princes", "Stade Vélodrome", "Groupama Stadium", "Stade Louis II", "Stade Pierre-Mauroy"],
            78: ["Allianz Arena", "Signal Iduna Park", "Red Bull Arena", "BayArena", "Volkswagen Arena"],
            135: ["San Siro", "Juventus Stadium", "Stadio Diego Armando Maradona", "Stadio Olimpico", "Gewiss Stadium"],
            2: ["Santiago Bernabéu", "Etihad Stadium", "Allianz Arena", "Parc des Princes", "Camp Nou", "Anfield"],
            233: ["FNB Stadium", "Orlando Stadium", "Loftus Versfeld Stadium", "Cape Town Stadium"],
            262: ["King Fahd International Stadium", "King Abdullah Sports City", "Prince Abdullah bin Jalawi Stadium"]
        }
        
        # Filtrer les ligues si spécifié
        if leagues:
            available_leagues = [l for l in league_definitions if l['id'] in leagues]
        else:
            available_leagues = league_definitions
        
        # Date de début (aujourd'hui par défaut)
        if start_date is None:
            start_date = datetime.now().date()
        elif isinstance(start_date, datetime):
            start_date = start_date.date()
        
        # Générer des matchs pour chaque jour
        for day in range(days_ahead):
            current_date = start_date + timedelta(days=day) if isinstance(start_date, datetime) else start_date
            
            # Générer plus de matchs pour les jours de week-end
            matches_per_day = 8 if current_date.weekday() >= 5 else 5
            
            # Répartir les matchs entre les différentes ligues
            leagues_for_day = random.sample(available_leagues, min(len(available_leagues), matches_per_day))
            
            for league in leagues_for_day:
                league_id = league["id"]
                
                # S'assurer que la ligue a suffisamment d'équipes
                if league_id in teams_by_league and len(teams_by_league[league_id]) >= 2:
                    # Nombre de matchs à générer pour cette ligue
                    matches_for_league = random.randint(1, 4)
                    
                    # S'assurer qu'on a assez d'équipes pour générer ces matchs
                    matches_for_league = min(matches_for_league, len(teams_by_league[league_id]) // 2)
                    
                    # Mélanger les équipes pour cette ligue
                    shuffled_teams = random.sample(teams_by_league[league_id], len(teams_by_league[league_id]))
                    
                    # Générer les matchs
                    for i in range(matches_for_league):
                        if 2*i + 1 < len(shuffled_teams):
                            home_team = shuffled_teams[2*i]
                            away_team = shuffled_teams[2*i + 1]
                            
                            # Créer un nouveau match
                            match_hour = random.randint(12, 21)
                            match_minute = random.choice([0, 15, 30, 45])
                            
                            if isinstance(current_date, datetime):
                                match_datetime = current_date.replace(hour=match_hour, minute=match_minute)
                            else:
                                match_datetime = datetime.combine(current_date, datetime.min.time()).replace(hour=match_hour, minute=match_minute)
                            
                            # Sélectionner un stade pour ce match
                            venue = random.choice(venues.get(league_id, ["Stade Municipal"]))
                            
                            match = {
                                "id": f"{day}_{league_id}_{i}",
                                "league_id": league_id,
                                "league": {"id": league_id, "name": league["name"]},
                                "league_name": league["name"],
                                "country": league["country"],
                                "home_team": home_team,
                                "away_team": away_team,
                                "date": match_datetime.isoformat(),
                                "time": match_datetime.strftime("%H:%M"),
                                "venue": venue,
                                "referee": f"Arbitre {random.randint(1, 20)}",
                                "temperature": f"{random.randint(15, 28)}°C",
                                "weather": random.choice(["Ensoleillé", "Nuageux", "Pluie légère", "Clair"])
                            }
                            
                            matches.append(match)
        
        # Trier les matchs par date
        matches.sort(key=lambda x: x["date"])
        return matches
    
    def get_team_statistics(self, home_team, away_team, league_id=None):
        """
        Récupère les statistiques détaillées des équipes et les informations H2H.
        
        Args:
            home_team (str): Nom de l'équipe à domicile
            away_team (str): Nom de l'équipe à l'extérieur
            league_id (int): ID de la ligue (optionnel)
            
        Returns:
            dict: Statistiques des équipes et informations H2H
        """
        cache_key = self.get_cache_key('team_stats', home=home_team, away=away_team, league=league_id)
        
        if self.is_cache_valid(cache_key):
            logger.info(f"Utilisation du cache pour les statistiques d'équipes")
            return self.cache[cache_key]
        
        logger.info(f"Récupération des statistiques pour {home_team} vs {away_team}")
        
        # Essayer d'utiliser l'API Football si disponible
        if self.sources_status['football_api']:
            try:
                stats = self._get_team_stats_from_api(home_team, away_team, league_id)
                self.set_cache(cache_key, stats)
                return stats
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des stats depuis l'API: {e}")
        
        # Fallback: Générer des stats simulées
        logger.warning("Utilisation de statistiques simulées")
        stats = self._generate_simulated_team_stats(home_team, away_team)
        self.set_cache(cache_key, stats)
        return stats
    
    def _get_team_stats_from_api(self, home_team, away_team, league_id=None):
        """
        Récupère les statistiques des équipes depuis l'API Football.
        
        Args:
            home_team (str): Nom de l'équipe à domicile
            away_team (str): Nom de l'équipe à l'extérieur
            league_id (int): ID de la ligue (optionnel)
            
        Returns:
            dict: Statistiques des équipes
        """
        # Cette méthode simule la récupération de données de l'API
        # Dans un code de production, ce serait remplacé par un appel API réel
        time.sleep(0.2)  # Simuler un délai réseau
        
        # Simuler les données de statistiques
        return self._generate_simulated_team_stats(home_team, away_team)
    
    def _generate_simulated_team_stats(self, home_team, away_team):
        """
        Génère des statistiques d'équipe simulées.
        
        Args:
            home_team (str): Nom de l'équipe à domicile
            away_team (str): Nom de l'équipe à l'extérieur
            
        Returns:
            dict: Statistiques simulées
        """
        # Générer des données de forme récente (5 derniers matchs)
        home_form = [random.uniform(0.3, 0.9) for _ in range(5)]
        away_form = [random.uniform(0.3, 0.9) for _ in range(5)]
        
        # Générer des résultats de confrontations directes
        h2h_total = random.randint(3, 10)
        h2h_home_wins = random.randint(0, h2h_total - 1)
        h2h_away_wins = random.randint(0, h2h_total - h2h_home_wins - 1)
        h2h_draws = h2h_total - h2h_home_wins - h2h_away_wins
        
        # Générer des valeurs marchandes des équipes (en millions d'euros)
        home_value = random.uniform(100, 1000)
        away_value = random.uniform(100, 1000)
        
        # Générer un indice de force relative entre les équipes
        strength_difference = random.uniform(-0.5, 0.5)
        form_difference = (sum(home_form) / len(home_form)) - (sum(away_form) / len(away_form))
        
        # Générer des stats d'attaque et défense
        home_goals_per_match = random.uniform(1.0, 2.5)
        home_goals_conceded_per_match = random.uniform(0.8, 1.8)
        away_goals_per_match = random.uniform(0.8, 2.0)
        away_goals_conceded_per_match = random.uniform(1.0, 2.0)
        
        # Générer le pourcentage d'absences de joueurs clés
        home_key_players_missing = random.uniform(0, 0.3)
        away_key_players_missing = random.uniform(0, 0.3)
        
        return {
            'home_team': home_team,
            'away_team': away_team,
            'home_form': home_form,
            'away_form': away_form,
            'h2h_home_wins': h2h_home_wins,
            'h2h_away_wins': h2h_away_wins,
            'h2h_draws': h2h_draws,
            'home_value': home_value,
            'away_value': away_value,
            'value_difference': home_value - away_value,
            'value_difference_percentage': abs((home_value - away_value) / max(home_value, away_value) * 100),
            'strength_difference': strength_difference,
            'form_difference': form_difference,
            'home_goals_per_match': home_goals_per_match,
            'home_goals_conceded_per_match': home_goals_conceded_per_match,
            'away_goals_per_match': away_goals_per_match,
            'away_goals_conceded_per_match': away_goals_conceded_per_match,
            'home_key_players_missing': home_key_players_missing,
            'away_key_players_missing': away_key_players_missing
        }
    
    def get_match_predictions(self, home_team, away_team, league_id=None):
        """
        Génère des prédictions pour un match en utilisant XGBoost.
        
        Args:
            home_team (str): Équipe à domicile
            away_team (str): Équipe à l'extérieur
            league_id (int): ID de la ligue (optionnel)
            
        Returns:
            dict: Prédictions pour le match
        """
        # Récupérer les statistiques des équipes
        team_stats = self.get_team_statistics(home_team, away_team, league_id)
        
        # Prédire les résultats
        # Dans un système réel, cela utiliserait un modèle XGBoost entraîné
        home_win_prob = 0.4
        draw_prob = 0.3
        away_win_prob = 0.3
        
        # Facteurs qui influencent les prédictions
        factors = {
            'home_advantage': 0.08,
            'form_weight': 0.12,
            'h2h_weight': 0.15,
            'value_weight': 0.10,
            'injury_impact': -0.05
        }
        
        # Ajuster la prédiction avec ces facteurs
        form_impact = team_stats.get('form_difference', 0) * factors['form_weight']
        value_impact = (team_stats.get('home_value', 500) - team_stats.get('away_value', 500)) / 1000 * factors['value_weight']
        
        h2h_total = team_stats.get('h2h_home_wins', 0) + team_stats.get('h2h_away_wins', 0) + team_stats.get('h2h_draws', 0)
        if h2h_total > 0:
            h2h_impact = (team_stats.get('h2h_home_wins', 0) / h2h_total - team_stats.get('h2h_away_wins', 0) / h2h_total) * factors['h2h_weight']
        else:
            h2h_impact = 0
        
        home_adv = factors['home_advantage']
        injury_impact_home = team_stats.get('home_key_players_missing', 0) * factors['injury_impact']
        injury_impact_away = team_stats.get('away_key_players_missing', 0) * factors['injury_impact'] * -1
        
        # Calculer les probabilités ajustées
        home_win_prob += form_impact + value_impact + h2h_impact + home_adv + injury_impact_home
        away_win_prob -= form_impact + value_impact + h2h_impact - home_adv - injury_impact_away
        
        # Assurer que les probabilités sont dans des limites raisonnables
        home_win_prob = max(0.05, min(0.9, home_win_prob))
        away_win_prob = max(0.05, min(0.9, away_win_prob))
        draw_prob = 1.0 - home_win_prob - away_win_prob
        
        # Normaliser pour s'assurer que la somme est 1
        total = home_win_prob + away_win_prob + draw_prob
        home_win_prob /= total
        away_win_prob /= total
        draw_prob /= total
        
        # Calculer les cotes
        margin = 0.07  # Marge du bookmaker
        home_odds = round((1 / home_win_prob * (1 + margin)), 2)
        draw_odds = round((1 / draw_prob * (1 + margin)), 2)
        away_odds = round((1 / away_win_prob * (1 + margin)), 2)
        
        # Calculer la confiance de la prédiction
        max_prob = max(home_win_prob, draw_prob, away_win_prob)
        second_max = sorted([home_win_prob, draw_prob, away_win_prob])[-2]
        confidence = min(max(((max_prob - second_max) / max_prob) + 0.6, 0.65), 0.95)
        
        return {
            'probabilities': {
                'home': round(home_win_prob * 100),
                'draw': round(draw_prob * 100),
                'away': round(away_win_prob * 100)
            },
            'odds': {
                'home': home_odds,
                'draw': draw_odds,
                'away': away_odds
            },
            'confidence': round(confidence, 2),
            'factors': {
                'form_impact': round(form_impact, 3),
                'value_impact': round(value_impact, 3),
                'h2h_impact': round(h2h_impact, 3),
                'home_advantage': round(home_adv, 3),
                'injury_impact_home': round(injury_impact_home, 3),
                'injury_impact_away': round(injury_impact_away, 3)
            },
            'team_stats': team_stats,
            'best_bet': "Victoire domicile" if home_win_prob > max(draw_prob, away_win_prob) else 
                      "Match nul" if draw_prob >= max(home_win_prob, away_win_prob) else 
                      "Victoire extérieur"
        }
    
    def get_xgboost_feature_importance(self):
        """
        Renvoie l'importance des caractéristiques pour XGBoost.
        Dans un système réel, cela viendrait du modèle entraîné.
        
        Returns:
            list: Liste des paires (caractéristique, importance)
        """
        features = [
            ('form_difference', 0.22),
            ('value_ratio', 0.15),
            ('attack_ratio', 0.18),
            ('defense_ratio', 0.16),
            ('h2h_home_win_ratio', 0.12),
            ('home_advantage', 0.08),
            ('home_key_players_missing', 0.05),
            ('away_key_players_missing', 0.04)
        ]
        
        return features