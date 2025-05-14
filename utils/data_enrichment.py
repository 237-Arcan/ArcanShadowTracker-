"""
Data Enrichment - Module d'enrichissement des données pour ArcanShadow
Ce module utilise FlashScraper pour enrichir les données des matchs et améliorer
les prédictions et la sélection du combiné du jour.
"""

import os
import json
import pandas as pd
from datetime import datetime, timedelta
import time
import threading
import logging
from .flash_scraper import FlashScraper

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('data_enrichment')

class DataEnrichment:
    """
    Module d'enrichissement des données pour ArcanShadow.
    Enrichit les données des matchs avec des informations provenant de Flashscore.
    """
    def __init__(self, cache_dir='data/cache', refresh_interval=3600):
        """
        Initialise le module d'enrichissement.
        
        Args:
            cache_dir (str): Répertoire pour le cache des données
            refresh_interval (int): Intervalle de rafraîchissement en secondes
        """
        self.scraper = FlashScraper()
        self.cache_dir = cache_dir
        self.refresh_interval = refresh_interval
        self.sport = "football"  # Par défaut
        
        # Créer le répertoire de cache s'il n'existe pas
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Démarrer le thread de mise à jour en arrière-plan
        self.stop_thread = threading.Event()
        self.update_thread = threading.Thread(target=self._background_update)
        self.update_thread.daemon = True
        self.update_thread.start()
        
    def _background_update(self):
        """Fonction de mise à jour en arrière-plan"""
        while not self.stop_thread.is_set():
            try:
                # Mettre à jour les données du jour
                self.refresh_daily_matches()
                
                # Mettre à jour les données des équipes populaires
                self.refresh_popular_teams()
                
                # Mettre à jour les données des ligues populaires
                self.refresh_popular_leagues()
                
                # Attendre l'intervalle de rafraîchissement
                self.stop_thread.wait(timeout=self.refresh_interval)
            except Exception as e:
                logger.error(f"Erreur lors de la mise à jour en arrière-plan: {e}")
                # Attendre avant de réessayer en cas d'erreur
                self.stop_thread.wait(timeout=60)
    
    def stop(self):
        """Arrête le thread de mise à jour en arrière-plan"""
        self.stop_thread.set()
        self.update_thread.join(timeout=5)
    
    def _get_cache_path(self, name, date=None):
        """
        Obtient le chemin du fichier de cache.
        
        Args:
            name (str): Nom du fichier de cache
            date (str, optional): Date au format YYYYMMDD
            
        Returns:
            str: Chemin complet du fichier de cache
        """
        if date:
            return os.path.join(self.cache_dir, f"{name}_{date}.json")
        return os.path.join(self.cache_dir, f"{name}.json")
    
    def _save_to_cache(self, data, name, date=None):
        """
        Sauvegarde des données dans le cache.
        
        Args:
            data: Données à sauvegarder
            name (str): Nom du fichier de cache
            date (str, optional): Date au format YYYYMMDD
        """
        try:
            cache_path = self._get_cache_path(name, date)
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde dans le cache: {e}")
    
    def _load_from_cache(self, name, date=None, max_age=None):
        """
        Charge des données depuis le cache.
        
        Args:
            name (str): Nom du fichier de cache
            date (str, optional): Date au format YYYYMMDD
            max_age (int, optional): Âge maximum du cache en secondes
            
        Returns:
            dict/list: Données du cache ou None si pas disponible/périmé
        """
        try:
            cache_path = self._get_cache_path(name, date)
            
            # Vérifier si le fichier existe
            if not os.path.exists(cache_path):
                return None
                
            # Vérifier l'âge du fichier si max_age est spécifié
            if max_age:
                file_age = time.time() - os.path.getmtime(cache_path)
                if file_age > max_age:
                    return None
            
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erreur lors du chargement depuis le cache: {e}")
            return None
    
    def refresh_daily_matches(self, date=None):
        """
        Rafraîchit les matchs du jour et les sauvegarde dans le cache.
        
        Args:
            date (str, optional): Date au format YYYYMMDD
            
        Returns:
            list: Liste des matchs du jour
        """
        if date is None:
            date = datetime.now().strftime('%Y%m%d')
        
        try:
            logger.info(f"Rafraîchissement des matchs pour la date {date}")
            
            # Récupérer les matchs du jour
            matches = self.scraper.get_matches_of_day(sport=self.sport, date=date)
            
            # Sauvegarder dans le cache
            self._save_to_cache(matches, "daily_matches", date)
            
            return matches
        except Exception as e:
            logger.error(f"Erreur lors du rafraîchissement des matchs du jour: {e}")
            return []
    
    def refresh_popular_teams(self):
        """
        Rafraîchit les données des équipes populaires.
        """
        try:
            # Liste des équipes populaires (à personnaliser)
            popular_teams = [
                # Format: [nom_équipe, id_équipe]
                ["Paris Saint-Germain", "3kq24huf"],
                ["Real Madrid", "2b23qvpp"],
                ["Barcelona", "hxvbo9br"],
                ["Manchester City", "sh8x82qw"],
                ["Liverpool", "c8h9bw1l"],
                ["Bayern Munich", "oumd2gub"],
                # Ajouter d'autres équipes populaires
            ]
            
            for team_name, team_id in popular_teams:
                try:
                    # Récupérer la forme de l'équipe
                    team_form = self.scraper.get_team_form(team_id, num_matches=10)
                    
                    # Sauvegarder dans le cache
                    self._save_to_cache(team_form, f"team_form_{team_id}")
                    
                    logger.info(f"Forme de l'équipe {team_name} mise à jour")
                except Exception as e:
                    logger.error(f"Erreur lors de la mise à jour de la forme de l'équipe {team_name}: {e}")
        except Exception as e:
            logger.error(f"Erreur lors du rafraîchissement des équipes populaires: {e}")
    
    def refresh_popular_leagues(self):
        """
        Rafraîchit les données des ligues populaires.
        """
        try:
            # Liste des ligues populaires (à personnaliser)
            popular_leagues = [
                # Format: [nom_ligue, id_ligue]
                ["Premier League", "xcd0rhjs"],
                ["La Liga", "pnvbqtve"],
                ["Bundesliga", "psg9hb1f"],
                ["Serie A", "f8n3715w"],
                ["Ligue 1", "qvupycj5"],
                ["Champions League", "8m5yq1l0"],
                # Ajouter d'autres ligues populaires
            ]
            
            for league_name, league_id in popular_leagues:
                try:
                    # Récupérer le classement de la ligue
                    league_table = self.scraper.get_league_table(league_id)
                    
                    # Sauvegarder dans le cache
                    self._save_to_cache(league_table, f"league_table_{league_id}")
                    
                    logger.info(f"Classement de la ligue {league_name} mis à jour")
                except Exception as e:
                    logger.error(f"Erreur lors de la mise à jour du classement de la ligue {league_name}: {e}")
        except Exception as e:
            logger.error(f"Erreur lors du rafraîchissement des ligues populaires: {e}")
    
    def get_daily_matches(self, date=None, refresh=False, max_age=3600):
        """
        Récupère les matchs du jour, depuis le cache ou en les rafraîchissant.
        
        Args:
            date (str, optional): Date au format YYYYMMDD
            refresh (bool): Forcer le rafraîchissement
            max_age (int): Âge maximum du cache en secondes
            
        Returns:
            list: Liste des matchs du jour
        """
        if date is None:
            date = datetime.now().strftime('%Y%m%d')
        
        # Essayer de charger depuis le cache si refresh n'est pas forcé
        if not refresh:
            cached_matches = self._load_from_cache("daily_matches", date, max_age)
            if cached_matches is not None:
                return cached_matches
        
        # Sinon, rafraîchir les données
        return self.refresh_daily_matches(date)
    
    def get_enriched_match(self, match_id, refresh=False, max_age=3600):
        """
        Récupère les données enrichies d'un match.
        
        Args:
            match_id (str): ID du match
            refresh (bool): Forcer le rafraîchissement
            max_age (int): Âge maximum du cache en secondes
            
        Returns:
            dict: Données enrichies du match
        """
        # Essayer de charger depuis le cache si refresh n'est pas forcé
        if not refresh:
            cached_match = self._load_from_cache(f"match_{match_id}", max_age=max_age)
            if cached_match is not None:
                return cached_match
        
        try:
            # Récupérer les détails du match
            match_details = self.scraper.get_match_details(match_id)
            
            # Enrichir avec d'autres données
            enriched_match = self.scraper.enrich_match_data(match_details)
            
            # Sauvegarder dans le cache
            self._save_to_cache(enriched_match, f"match_{match_id}")
            
            return enriched_match
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des données enrichies du match {match_id}: {e}")
            return {}
    
    def get_team_form(self, team_id, refresh=False, max_age=3600):
        """
        Récupère la forme d'une équipe.
        
        Args:
            team_id (str): ID de l'équipe
            refresh (bool): Forcer le rafraîchissement
            max_age (int): Âge maximum du cache en secondes
            
        Returns:
            list: Forme de l'équipe
        """
        # Essayer de charger depuis le cache si refresh n'est pas forcé
        if not refresh:
            cached_form = self._load_from_cache(f"team_form_{team_id}", max_age=max_age)
            if cached_form is not None:
                return cached_form
        
        try:
            # Récupérer la forme de l'équipe
            team_form = self.scraper.get_team_form(team_id)
            
            # Sauvegarder dans le cache
            self._save_to_cache(team_form, f"team_form_{team_id}")
            
            return team_form
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la forme de l'équipe {team_id}: {e}")
            return []
    
    def get_head_to_head(self, team1_id, team2_id, refresh=False, max_age=86400):
        """
        Récupère l'historique des confrontations directes entre deux équipes.
        
        Args:
            team1_id (str): ID de la première équipe
            team2_id (str): ID de la deuxième équipe
            refresh (bool): Forcer le rafraîchissement
            max_age (int): Âge maximum du cache en secondes
            
        Returns:
            list: Historique des confrontations
        """
        cache_name = f"h2h_{team1_id}_{team2_id}"
        
        # Essayer de charger depuis le cache si refresh n'est pas forcé
        if not refresh:
            cached_h2h = self._load_from_cache(cache_name, max_age=max_age)
            if cached_h2h is not None:
                return cached_h2h
        
        try:
            # Récupérer les confrontations directes
            h2h = self.scraper.get_head_to_head(team1_id, team2_id)
            
            # Sauvegarder dans le cache
            self._save_to_cache(h2h, cache_name)
            
            return h2h
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des confrontations directes entre {team1_id} et {team2_id}: {e}")
            return []
    
    def get_league_table(self, league_id, refresh=False, max_age=43200):
        """
        Récupère le classement d'une ligue.
        
        Args:
            league_id (str): ID de la ligue
            refresh (bool): Forcer le rafraîchissement
            max_age (int): Âge maximum du cache en secondes
            
        Returns:
            list: Classement de la ligue
        """
        # Essayer de charger depuis le cache si refresh n'est pas forcé
        if not refresh:
            cached_table = self._load_from_cache(f"league_table_{league_id}", max_age=max_age)
            if cached_table is not None:
                return cached_table
        
        try:
            # Récupérer le classement de la ligue
            league_table = self.scraper.get_league_table(league_id)
            
            # Sauvegarder dans le cache
            self._save_to_cache(league_table, f"league_table_{league_id}")
            
            return league_table
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du classement de la ligue {league_id}: {e}")
            return []
    
    def get_matches_with_betting_value(self, date=None, min_confidence=0.6):
        """
        Récupère les matchs du jour avec une analyse de la valeur de paris.
        
        Args:
            date (str, optional): Date au format YYYYMMDD
            min_confidence (float): Confiance minimale pour les paris
            
        Returns:
            list: Liste des paris à valeur
        """
        try:
            # Récupérer les matchs du jour
            matches = self.get_daily_matches(date)
            value_bets = []
            
            for match in matches:
                try:
                    match_id = match.get('id')
                    
                    # Récupérer les données enrichies du match
                    enriched_match = self.get_enriched_match(match_id)
                    
                    # Extraire les cotes
                    odds = enriched_match.get('odds', {})
                    
                    # Analyser la valeur potentielle
                    if odds:
                        home_odds = float(odds.get('1', 0)) if odds.get('1') else 0
                        draw_odds = float(odds.get('X', 0)) if odds.get('X') else 0
                        away_odds = float(odds.get('2', 0)) if odds.get('2') else 0
                        
                        # Analyser la forme et l'historique
                        home_form = enriched_match.get('home_form', [])
                        away_form = enriched_match.get('away_form', [])
                        h2h = enriched_match.get('head_to_head', [])
                        
                        # Calculer la forme récente (% de victoires)
                        home_wins = sum(1 for m in home_form if m.get('result') == 'W')
                        home_form_rating = home_wins / len(home_form) if home_form else 0.5
                        
                        away_wins = sum(1 for m in away_form if m.get('result') == 'W')
                        away_form_rating = away_wins / len(away_form) if away_form else 0.5
                        
                        # Analyser les H2H
                        h2h_home_wins = 0
                        h2h_away_wins = 0
                        h2h_draws = 0
                        
                        for h2h_match in h2h:
                            home_team = h2h_match.get('home_team')
                            score = h2h_match.get('score', '').split('-')
                            
                            if len(score) == 2:
                                home_score = int(score[0])
                                away_score = int(score[1])
                                
                                if home_score > away_score:
                                    if home_team == enriched_match.get('home_team'):
                                        h2h_home_wins += 1
                                    else:
                                        h2h_away_wins += 1
                                elif home_score < away_score:
                                    if home_team == enriched_match.get('home_team'):
                                        h2h_away_wins += 1
                                    else:
                                        h2h_home_wins += 1
                                else:
                                    h2h_draws += 1
                        
                        h2h_total = h2h_home_wins + h2h_away_wins + h2h_draws
                        h2h_home_ratio = h2h_home_wins / h2h_total if h2h_total > 0 else 0.33
                        h2h_away_ratio = h2h_away_wins / h2h_total if h2h_total > 0 else 0.33
                        h2h_draw_ratio = h2h_draws / h2h_total if h2h_total > 0 else 0.33
                        
                        # Calculer les probabilités estimées
                        home_probability = (home_form_rating * 0.4) + (h2h_home_ratio * 0.4) + 0.2  # Avantage à domicile
                        away_probability = (away_form_rating * 0.4) + (h2h_away_ratio * 0.4)
                        draw_probability = (h2h_draw_ratio * 0.5) + 0.15  # Base de probabilité pour le nul
                        
                        # Normaliser
                        total_prob = home_probability + away_probability + draw_probability
                        if total_prob > 0:
                            home_probability /= total_prob
                            away_probability /= total_prob
                            draw_probability /= total_prob
                        
                        # Calculer les valeurs attendues
                        home_ev = (home_probability * home_odds) - 1
                        away_ev = (away_probability * away_odds) - 1
                        draw_ev = (draw_probability * draw_odds) - 1
                        
                        # Filtrer par confiance minimale
                        if home_probability >= min_confidence:
                            value_bets.append({
                                'match': enriched_match,
                                'selection': 'home',
                                'odds': home_odds,
                                'probability': home_probability,
                                'ev': home_ev
                            })
                        
                        if away_probability >= min_confidence:
                            value_bets.append({
                                'match': enriched_match,
                                'selection': 'away',
                                'odds': away_odds,
                                'probability': away_probability,
                                'ev': away_ev
                            })
                        
                        if draw_probability >= min_confidence:
                            value_bets.append({
                                'match': enriched_match,
                                'selection': 'draw',
                                'odds': draw_odds,
                                'probability': draw_probability,
                                'ev': draw_ev
                            })
                
                except Exception as e:
                    logger.error(f"Erreur lors de l'analyse du match {match.get('id')}: {e}")
                    continue
            
            # Trier par valeur espérée décroissante
            value_bets.sort(key=lambda x: x.get('ev', 0), reverse=True)
            
            return value_bets
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des matchs avec valeur de paris: {e}")
            return []
    
    def search_team(self, team_name):
        """
        Recherche une équipe par son nom.
        
        Args:
            team_name (str): Nom de l'équipe
            
        Returns:
            dict: Informations sur l'équipe
        """
        try:
            # Rechercher l'équipe
            results = self.scraper.search_teams_or_leagues(team_name)
            
            # Retourner la première équipe correspondante
            if results.get('teams'):
                return results['teams'][0]
            
            return None
        except Exception as e:
            logger.error(f"Erreur lors de la recherche de l'équipe {team_name}: {e}")
            return None
    
    def get_team_id(self, team_name):
        """
        Récupère l'ID d'une équipe à partir de son nom.
        
        Args:
            team_name (str): Nom de l'équipe
            
        Returns:
            str: ID de l'équipe
        """
        team = self.search_team(team_name)
        if team:
            return team.get('id')
        return None
    
    def enrich_matches_data(self, matches):
        """
        Enrichit les données de plusieurs matchs.
        
        Args:
            matches (list): Liste des matchs à enrichir
            
        Returns:
            list: Liste des matchs enrichis
        """
        enriched_matches = []
        
        for match in matches:
            try:
                match_id = match.get('id')
                if match_id:
                    enriched_match = self.get_enriched_match(match_id)
                    enriched_matches.append(enriched_match)
                else:
                    # Essayer de trouver l'ID du match
                    home_team = match.get('home_team')
                    away_team = match.get('away_team')
                    
                    if home_team and away_team:
                        # Rechercher les équipes
                        home_id = self.get_team_id(home_team)
                        away_id = self.get_team_id(away_team)
                        
                        if home_id and away_id:
                            # Enrichir avec les données disponibles
                            match_with_ids = {
                                **match,
                                'home_id': home_id,
                                'away_id': away_id
                            }
                            
                            # Ajouter la forme et les H2H
                            home_form = self.get_team_form(home_id)
                            away_form = self.get_team_form(away_id)
                            h2h = self.get_head_to_head(home_id, away_id)
                            
                            enriched_match = {
                                **match_with_ids,
                                'home_form': home_form,
                                'away_form': away_form,
                                'head_to_head': h2h
                            }
                            
                            enriched_matches.append(enriched_match)
                        else:
                            # Si on ne peut pas enrichir, ajouter le match original
                            enriched_matches.append(match)
                    else:
                        # Si pas d'équipes, ajouter le match original
                        enriched_matches.append(match)
            except Exception as e:
                logger.error(f"Erreur lors de l'enrichissement du match: {e}")
                # Ajouter le match original en cas d'erreur
                enriched_matches.append(match)
        
        return enriched_matches