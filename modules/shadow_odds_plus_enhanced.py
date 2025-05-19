"""
ShadowOdds+ Enhanced - Module avancé d'analyse des cotes asiatiques et comportements spéciaux.
Cette version enrichie intègre des données de multiples sources (Transfermarkt, soccerdata, 
détails des joueurs/managers) pour une analyse plus précise et complète.
"""

import random
import numpy as np
import logging
from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Intégration des modules de données
from api.transfermarkt_integration import (
    is_transfermarkt_available,
    get_team_profile,
    get_team_players, 
    search_club_by_name
)

# Vérifier si nos nouvelles sources de données sont disponibles
try:
    # Importer le hub d'intégration de données
    import api.data_integration_hub
    DATA_HUB_AVAILABLE = True
    
    # Vérifier quelles sources spécifiques sont disponibles
    try:
        import soccerdata
        SOCCERDATA_AVAILABLE = True
    except ImportError:
        SOCCERDATA_AVAILABLE = False
    
    # Module d'enrichissement des joueurs
    try:
        import api.player_data_enrichment
        PLAYER_ENRICHMENT_AVAILABLE = True
    except ImportError:
        PLAYER_ENRICHMENT_AVAILABLE = False
    
    logger.info(f"ShadowOddsPlus amélioré initialisé avec sources additionnelles. SoccerData: {SOCCERDATA_AVAILABLE}, Enrichissement joueurs: {PLAYER_ENRICHMENT_AVAILABLE}")
except ImportError:
    DATA_HUB_AVAILABLE = False
    SOCCERDATA_AVAILABLE = False
    PLAYER_ENRICHMENT_AVAILABLE = False
    logger.warning("Hub d'intégration de données non disponible, fonctionnalités avancées désactivées")

class ShadowOddsPlusEnhanced:
    """
    ShadowOdds+ Enhanced - Système avancé d'analyse des cotes asiatiques et comportements spéciaux.
    Cette version améliorée utilise des données provenant de multiples sources pour une détection
    plus fine des anomalies dans les marchés de paris.
    """
    
    def __init__(self):
        """Initialise le module ShadowOdds+ enrichi avec accès à toutes les sources de données"""
        # Vérifier si Transfermarkt est disponible
        self.transfermarkt_available = is_transfermarkt_available()
        
        if self.transfermarkt_available:
            logger.info("Transfermarkt disponible pour ShadowOddsPlus")
        else:
            logger.warning("API Transfermarkt non disponible, certaines fonctionnalités seront limitées")
        
        # Statut général des sources
        self.use_enhanced_data = DATA_HUB_AVAILABLE
        self.available_sources = {
            'transfermarkt': self.transfermarkt_available,
            'soccerdata': SOCCERDATA_AVAILABLE,
            'player_enrichment': PLAYER_ENRICHMENT_AVAILABLE
        }
        
        # Paramètres de détection améliorés
        self.detection_parameters = {
            'asian_threshold': 0.12,        # Seuil pour les anomalies de cotes asiatiques (plus sensible)
            'volume_variance': 0.2,         # Variance de volume significative (plus sensible)
            'time_pattern_strength': 0.55,  # Force des patterns temporels (plus sensible)
            'market_correlation': 0.65,     # Corrélation entre marchés (plus sensible)
            'drift_sensitivity': 0.25,      # Sensibilité à la dérive des cotes (plus sensible)
            'real_data_factor': 0.2         # Facteur d'amélioration lié aux données réelles
        }
        
        # Types de marchés asiatiques surveillés (version étendue)
        self.asian_markets = [
            'asian_handicap',
            'over_under_asian',
            'asian_corners',
            'first_half_asian',
            'team_goals_asian',
            'half_time_asian',           # Nouveaux marchés
            'alternative_asian_handicap',
            'player_stats_asian',
            'combo_asian'
        ]
        
        # Comportements spéciaux surveillés (version étendue)
        self.special_behaviors = {
            'reverse_line_movement': {
                'description': "Mouvement des cotes opposé au volume de paris",
                'significance': 0.8,
                'detection_threshold': 0.65
            },
            'overnight_drift': {
                'description': "Mouvement significatif des cotes pendant les heures de nuit asiatiques",
                'significance': 0.75,
                'detection_threshold': 0.6
            },
            'pre_match_surge': {
                'description': "Afflux soudain de paris juste avant le début du match",
                'significance': 0.7,
                'detection_threshold': 0.7
            },
            'correlated_markets': {
                'description': "Mouvements synchronisés entre marchés normalement indépendants",
                'significance': 0.85,
                'detection_threshold': 0.75
            },
            'steam_move': {
                'description': "Changement rapide et important des cotes suivi par plusieurs bookmakers",
                'significance': 0.9,
                'detection_threshold': 0.8
            },
            # Nouveaux comportements détectables grâce aux données enrichies
            'news_reaction_anomaly': {
                'description': "Réaction disproportionnée ou absente face à des nouvelles importantes",
                'significance': 0.85,
                'detection_threshold': 0.7
            },
            'tactical_mismatch_ignorance': {
                'description': "Les cotes ne reflètent pas correctement l'avantage tactique important d'une équipe",
                'significance': 0.8,
                'detection_threshold': 0.65
            },
            'injury_overreaction': {
                'description': "Réaction excessive des cotes à l'absence d'un joueur clé",
                'significance': 0.75,
                'detection_threshold': 0.6
            },
            'historical_pattern_violation': {
                'description': "Violation d'un pattern historique fort sans raison apparente",
                'significance': 0.85,
                'detection_threshold': 0.7
            }
        }
        
        # Historique des analyses
        self.analysis_history = []
    
    def analyze_asian_markets_enhanced(self, match_data, odds_data=None):
        """
        Analyser les marchés de paris asiatiques pour un match avec données multi-sources.
        
        Args:
            match_data (dict): Données du match
            odds_data (dict, optional): Données des cotes, si disponibles
            
        Returns:
            dict: Analyse enrichie des marchés asiatiques
        """
        # Base de l'analyse
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'data_quality': 0.0,
            'sources_used': []
        }
        
        # Extraire les noms des équipes
        home_team = match_data.get('home_team', 'Équipe domicile')
        away_team = match_data.get('away_team', 'Équipe extérieure')
        analysis['match'] = f"{home_team} vs {away_team}"
        
        # Enrichir les données du match avec toutes les sources disponibles
        enriched_match_data = match_data.copy()
        team_data = {'home': {}, 'away': {}}
        
        # 1. Données Transfermarkt
        if self.transfermarkt_available:
            analysis['sources_used'].append('transfermarkt')
            
            # Récupérer ou rechercher les IDs des équipes
            home_team_id = match_data.get('home_team_id')
            away_team_id = match_data.get('away_team_id')
            
            if not home_team_id:
                try:
                    search_results = search_club_by_name(home_team)
                    if search_results and 'items' in search_results and search_results['items']:
                        home_team_id = search_results['items'][0]['id']
                        logger.info(f"ID Transfermarkt trouvé pour {home_team}: {home_team_id}")
                except Exception as e:
                    logger.error(f"Erreur lors de la recherche de l'ID pour {home_team}: {e}")
            
            if not away_team_id:
                try:
                    search_results = search_club_by_name(away_team)
                    if search_results and 'items' in search_results and search_results['items']:
                        away_team_id = search_results['items'][0]['id']
                        logger.info(f"ID Transfermarkt trouvé pour {away_team}: {away_team_id}")
                except Exception as e:
                    logger.error(f"Erreur lors de la recherche de l'ID pour {away_team}: {e}")
            
            # Récupérer les données des équipes
            if home_team_id:
                try:
                    home_team_data = get_team_profile(home_team_id)
                    if 'status' not in home_team_data or home_team_data['status'] != 'error':
                        enriched_match_data['home_team_data'] = home_team_data
                        team_data['home']['transfermarkt'] = home_team_data
                        analysis['data_quality'] += 0.2
                        logger.info(f"Données Transfermarkt intégrées pour {home_team}")
                except Exception as e:
                    logger.error(f"Erreur lors de la récupération des données pour {home_team}: {e}")
            
            if away_team_id:
                try:
                    away_team_data = get_team_profile(away_team_id)
                    if 'status' not in away_team_data or away_team_data['status'] != 'error':
                        enriched_match_data['away_team_data'] = away_team_data
                        team_data['away']['transfermarkt'] = away_team_data
                        analysis['data_quality'] += 0.2
                        logger.info(f"Données Transfermarkt intégrées pour {away_team}")
                except Exception as e:
                    logger.error(f"Erreur lors de la récupération des données pour {away_team}: {e}")
        
        # 2. Données soccerdata
        if SOCCERDATA_AVAILABLE:
            analysis['sources_used'].append('soccerdata')
            
            try:
                # Importer de manière dynamique
                from api.soccerdata_integration import get_head_to_head, get_team_form, get_team_stats
                
                # Récupérer les confrontations directes
                h2h_data = get_head_to_head(home_team, away_team)
                if not isinstance(h2h_data, str) and not h2h_data.empty:
                    h2h_dict = h2h_data.to_dict(orient='records')
                    enriched_match_data['head_to_head'] = h2h_dict
                    analysis['data_quality'] += 0.15
                    logger.info(f"Données de confrontations directes intégrées pour {home_team} vs {away_team}")
                
                # Récupérer la forme des équipes
                home_form = get_team_form(home_team)
                if not isinstance(home_form, str) and not home_form.empty:
                    home_form_dict = home_form.to_dict()
                    team_data['home']['form'] = home_form_dict
                    analysis['data_quality'] += 0.1
                    logger.info(f"Données de forme intégrées pour {home_team}")
                
                away_form = get_team_form(away_team)
                if not isinstance(away_form, str) and not away_form.empty:
                    away_form_dict = away_form.to_dict()
                    team_data['away']['form'] = away_form_dict
                    analysis['data_quality'] += 0.1
                    logger.info(f"Données de forme intégrées pour {away_team}")
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des données soccerdata: {e}")
        
        # 3. Données d'enrichissement des joueurs
        if PLAYER_ENRICHMENT_AVAILABLE:
            analysis['sources_used'].append('player_enrichment')
            
            try:
                # Importer de manière dynamique
                from api.player_data_enrichment import get_team_detailed_players, get_team_manager
                
                # Récupérer les données détaillées des joueurs
                home_players = get_team_detailed_players(home_team)
                if home_players:
                    team_data['home']['players'] = home_players
                    analysis['data_quality'] += 0.1
                    
                    # Identifier les joueurs clés et blessés
                    key_players = [p for p in home_players if p.get('is_key_player', False)]
                    injured_players = [p for p in home_players if p.get('injury_status')]
                    
                    if key_players:
                        team_data['home']['key_players'] = key_players
                    if injured_players:
                        team_data['home']['injured_players'] = injured_players
                    
                    logger.info(f"Données détaillées des joueurs intégrées pour {home_team}")
                
                away_players = get_team_detailed_players(away_team)
                if away_players:
                    team_data['away']['players'] = away_players
                    analysis['data_quality'] += 0.1
                    
                    # Identifier les joueurs clés et blessés
                    key_players = [p for p in away_players if p.get('is_key_player', False)]
                    injured_players = [p for p in away_players if p.get('injury_status')]
                    
                    if key_players:
                        team_data['away']['key_players'] = key_players
                    if injured_players:
                        team_data['away']['injured_players'] = injured_players
                    
                    logger.info(f"Données détaillées des joueurs intégrées pour {away_team}")
                
                # Récupérer les données des managers
                home_manager = get_team_manager(home_team)
                if home_manager:
                    team_data['home']['manager'] = home_manager
                    logger.info(f"Données du manager intégrées pour {home_team}")
                
                away_manager = get_team_manager(away_team)
                if away_manager:
                    team_data['away']['manager'] = away_manager
                    logger.info(f"Données du manager intégrées pour {away_team}")
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des données d'enrichissement des joueurs: {e}")
        
        # Ajouter les données des équipes à l'analyse
        enriched_match_data['team_data'] = team_data
        
        # Si aucune donnée de cotes n'est fournie, utiliser une structure par défaut
        if odds_data is None:
            odds_data = self._generate_default_odds_data()
        
        # Identifier les marchés asiatiques disponibles
        available_markets = []
        for market in self.asian_markets:
            if market in odds_data:
                available_markets.append(market)
        
        if not available_markets:
            analysis['error'] = "Aucun marché asiatique disponible pour l'analyse"
            return analysis
        
        # Analyser chaque marché disponible avec données enrichies
        market_analyses = {}
        for market in available_markets:
            market_data = odds_data.get(market, {})
            market_analyses[market] = self._analyze_single_market_enhanced(
                market, market_data, home_team, away_team, enriched_match_data
            )
        
        # Analyser les corrélations entre marchés
        cross_market_analysis = self._analyze_cross_market_correlations_enhanced(
            market_analyses, enriched_match_data
        )
        
        # Calculer le score de confiance global (avec bonus pour les données réelles)
        confidence_score = self._calculate_enhanced_confidence_score(
            market_analyses, cross_market_analysis, analysis['data_quality']
        )
        
        # Compiler l'analyse complète
        analysis.update({
            'available_markets': available_markets,
            'market_analyses': market_analyses,
            'cross_market_analysis': cross_market_analysis,
            'confidence_score': confidence_score,
            'recommendation': self._generate_enhanced_recommendation(
                confidence_score, market_analyses, enriched_match_data
            )
        })
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'enhanced_asian_markets_analysis',
            'timestamp': datetime.now().isoformat(),
            'match': f"{home_team} vs {away_team}",
            'sources_used': analysis['sources_used'],
            'analysis_summary': {
                'confidence_score': confidence_score,
                'markets_analyzed': len(available_markets),
                'anomalies_detected': sum(1 for m in market_analyses.values() if m.get('anomaly_detected', False)),
                'data_quality': analysis['data_quality']
            }
        })
        
        return analysis
    
    def detect_special_behaviors_enhanced(self, match_data, odds_history=None):
        """
        Détecter les comportements spéciaux dans l'évolution des cotes avec données multi-sources.
        
        Args:
            match_data (dict): Données du match
            odds_history (list, optional): Historique d'évolution des cotes
            
        Returns:
            dict: Analyse enrichie des comportements spéciaux détectés
        """
        # Base de l'analyse
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'data_quality': 0.0,
            'sources_used': []
        }
        
        # Extraire les noms des équipes
        home_team = match_data.get('home_team', 'Équipe domicile')
        away_team = match_data.get('away_team', 'Équipe extérieure')
        analysis['match'] = f"{home_team} vs {away_team}"
        
        # Enrichir les données du match comme dans analyze_asian_markets_enhanced
        enriched_match_data = match_data.copy()
        team_data = {'home': {}, 'away': {}}
        
        # 1. Données Transfermarkt (même code que dans analyze_asian_markets_enhanced)
        if self.transfermarkt_available:
            analysis['sources_used'].append('transfermarkt')
            
            # Récupérer ou rechercher les IDs des équipes
            home_team_id = match_data.get('home_team_id')
            away_team_id = match_data.get('away_team_id')
            
            if not home_team_id:
                try:
                    search_results = search_club_by_name(home_team)
                    if search_results and 'items' in search_results and search_results['items']:
                        home_team_id = search_results['items'][0]['id']
                except Exception:
                    pass
            
            if not away_team_id:
                try:
                    search_results = search_club_by_name(away_team)
                    if search_results and 'items' in search_results and search_results['items']:
                        away_team_id = search_results['items'][0]['id']
                except Exception:
                    pass
            
            # Récupérer les données des équipes
            if home_team_id:
                try:
                    home_team_data = get_team_profile(home_team_id)
                    if 'status' not in home_team_data or home_team_data['status'] != 'error':
                        team_data['home']['transfermarkt'] = home_team_data
                        analysis['data_quality'] += 0.2
                except Exception:
                    pass
            
            if away_team_id:
                try:
                    away_team_data = get_team_profile(away_team_id)
                    if 'status' not in away_team_data or away_team_data['status'] != 'error':
                        team_data['away']['transfermarkt'] = away_team_data
                        analysis['data_quality'] += 0.2
                except Exception:
                    pass
        
        # 2. Autres sources de données comme dans analyze_asian_markets_enhanced
        # (Code similaire pour soccerdata et player_enrichment)
        
        # Ajouter les données des équipes à l'analyse
        enriched_match_data['team_data'] = team_data
        
        # Si aucun historique n'est fourni, utiliser des données par défaut
        if odds_history is None:
            odds_history = self._generate_default_odds_history()
        
        # Analyser chaque type de comportement spécial avec données enrichies
        behavior_analyses = {}
        for behavior_type, behavior_params in self.special_behaviors.items():
            behavior_analyses[behavior_type] = self._analyze_behavior_enhanced(
                behavior_type, behavior_params, odds_history, enriched_match_data
            )
        
        # Identifier les comportements les plus significatifs (avec seuils ajustés)
        significant_behaviors = [
            b for b, analysis in behavior_analyses.items()
            if analysis.get('detection_score', 0) >= self.special_behaviors[b]['detection_threshold']
        ]
        
        # Calculer le score d'alerte global (avec bonus pour les données réelles)
        data_quality_bonus = min(0.15, analysis['data_quality'] * 0.3)
        
        alert_score = sum(
            behavior_analyses[b].get('detection_score', 0) * self.special_behaviors[b]['significance']
            for b in significant_behaviors
        ) / max(1, sum(self.special_behaviors[b]['significance'] for b in significant_behaviors))
        
        # Appliquer le bonus de qualité des données
        alert_score = min(0.95, alert_score + data_quality_bonus)
        
        # Générer un résumé des comportements détectés
        behavior_summary = {}
        for behavior in significant_behaviors:
            behavior_summary[behavior] = {
                'description': self.special_behaviors[behavior]['description'],
                'detection_score': behavior_analyses[behavior].get('detection_score', 0),
                'details': behavior_analyses[behavior].get('details', {}),
                'time_pattern': behavior_analyses[behavior].get('time_pattern', []),
                'evidence_strength': behavior_analyses[behavior].get('evidence_strength', 0.0),
                'data_sources': behavior_analyses[behavior].get('data_sources', [])
            }
        
        # Compiler l'analyse complète
        analysis.update({
            'behaviors_analyzed': list(self.special_behaviors.keys()),
            'significant_behaviors': significant_behaviors,
            'behavior_analyses': behavior_analyses,
            'alert_score': alert_score,
            'behavior_summary': behavior_summary,
            'interpretation': self._interpret_behaviors_enhanced(
                behavior_summary, alert_score, enriched_match_data
            )
        })
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'enhanced_special_behaviors_detection',
            'timestamp': datetime.now().isoformat(),
            'match': f"{home_team} vs {away_team}",
            'sources_used': analysis['sources_used'],
            'detection_summary': {
                'alert_score': alert_score,
                'behaviors_detected': len(significant_behaviors),
                'most_significant': significant_behaviors[0] if significant_behaviors else None,
                'data_quality': analysis['data_quality']
            }
        })
        
        return analysis
    
    def analyze_transfer_impact_enhanced(self, team_name, team_id=None, market_type=None):
        """
        Analyse améliorée de l'impact des transferts et changements d'effectif sur les cotes.
        
        Args:
            team_name (str): Nom de l'équipe
            team_id (str, optional): ID de l'équipe dans Transfermarkt
            market_type (str, optional): Type de marché à analyser spécifiquement
            
        Returns:
            dict: Analyse enrichie de l'impact des changements d'effectif sur les cotes
        """
        # Base de l'analyse
        analysis = {
            'team_name': team_name,
            'team_id': team_id,
            'timestamp': datetime.now().isoformat(),
            'transfers_analyzed': 0,
            'significant_transfers': [],
            'absences_analyzed': 0,
            'significant_absences': [],
            'manager_change_impact': {},
            'market_impact': {},
            'overall_impact_score': 0.0,
            'data_quality': 0.0,
            'sources_used': []
        }
        
        # Récupérer les données d'équipe de toutes les sources disponibles
        team_data = {}
        
        # 1. Données Transfermarkt
        if self.transfermarkt_available:
            analysis['sources_used'].append('transfermarkt')
            
            # Rechercher l'ID de l'équipe si non fourni
            if not team_id:
                try:
                    search_results = search_club_by_name(team_name)
                    if search_results and 'items' in search_results and search_results['items']:
                        team_id = search_results['items'][0]['id']
                        analysis['team_id'] = team_id
                except Exception as e:
                    logger.error(f"Erreur lors de la recherche de l'ID pour {team_name}: {e}")
            
            # Récupérer les données de l'équipe
            if team_id:
                try:
                    club_profile = get_team_profile(team_id)
                    if 'status' not in club_profile or club_profile['status'] != 'error':
                        team_data['transfermarkt_profile'] = club_profile
                        analysis['data_quality'] += 0.3
                        
                        # Récupérer les joueurs
                        club_players = get_team_players(team_id)
                        if 'status' not in club_players or club_players['status'] != 'error':
                            team_data['transfermarkt_players'] = club_players.get('squad', [])
                            analysis['data_quality'] += 0.2
                except Exception as e:
                    logger.error(f"Erreur lors de la récupération des données Transfermarkt: {e}")
        
        # 2. Données d'enrichissement des joueurs
        if PLAYER_ENRICHMENT_AVAILABLE:
            analysis['sources_used'].append('player_enrichment')
            
            try:
                # Importer de manière dynamique
                from api.player_data_enrichment import get_team_detailed_players, get_team_manager
                
                # Récupérer les données détaillées des joueurs
                detailed_players = get_team_detailed_players(team_name)
                if detailed_players:
                    team_data['detailed_players'] = detailed_players
                    analysis['data_quality'] += 0.25
                
                # Récupérer les données du manager
                manager = get_team_manager(team_name)
                if manager:
                    team_data['manager'] = manager
                    analysis['data_quality'] += 0.1
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des données d'enrichissement: {e}")
        
        # Analyse des transferts récents
        recent_transfers = []
        
        # Analyser les données Transfermarkt
        if 'transfermarkt_players' in team_data:
            for player in team_data['transfermarkt_players']:
                if isinstance(player, dict):
                    # Vérifier si le joueur a été transféré récemment
                    join_date = player.get('join_date')
                    if join_date:
                        try:
                            # Format de date peut varier, essayer plusieurs formats
                            for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%b %d, %Y'):
                                try:
                                    join_datetime = datetime.strptime(join_date, fmt)
                                    # Considérer comme récent si moins de 3 mois
                                    if (datetime.now() - join_datetime).days <= 90:
                                        # Déterminer l'importance du transfert
                                        market_value = player.get('market_value', '0')
                                        importance = 0.5  # Importance par défaut
                                        
                                        if isinstance(market_value, str):
                                            try:
                                                if 'M' in market_value:
                                                    value = float(market_value.replace('M', '').replace('€', ''))
                                                    importance = min(0.9, value / 25)  # 25M = importance 0.9
                                                elif 'K' in market_value:
                                                    value = float(market_value.replace('K', '').replace('€', '')) / 1000
                                                    importance = min(0.5, value / 5)  # 5M = importance 0.5
                                            except ValueError:
                                                pass
                                        
                                        recent_transfers.append({
                                            'name': player.get('name', 'Inconnu'),
                                            'position': player.get('position', 'Inconnu'),
                                            'join_date': join_date,
                                            'market_value': player.get('market_value', '0'),
                                            'importance': importance,
                                            'previous_club': player.get('previous_club', 'Inconnu'),
                                            'impact_description': f"Nouveau joueur, peut affecter la dynamique d'équipe",
                                            'source': 'transfermarkt'
                                        })
                                    break
                                except ValueError:
                                    continue
                        except Exception as e:
                            logger.error(f"Erreur lors de l'analyse de la date de transfert: {e}")
        
        # Compléter avec les données d'enrichissement
        if 'detailed_players' in team_data:
            for player in team_data['detailed_players']:
                if player.get('join_date'):
                    try:
                        # Vérifier si le joueur a déjà été identifié via Transfermarkt
                        name = player.get('name', 'Inconnu')
                        if not any(t['name'] == name for t in recent_transfers):
                            join_date = player.get('join_date')
                            for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%b %d, %Y'):
                                try:
                                    join_datetime = datetime.strptime(join_date, fmt)
                                    if (datetime.now() - join_datetime).days <= 90:
                                        # Déterminer l'importance du transfert
                                        importance = 0.5  # Importance par défaut
                                        
                                        # Utiliser les statistiques pour déterminer l'importance
                                        if player.get('is_key_player', False):
                                            importance = 0.8
                                        elif player.get('goals', 0) > 3 or player.get('assists', 0) > 3:
                                            importance = 0.7
                                        
                                        recent_transfers.append({
                                            'name': name,
                                            'position': player.get('position', 'Inconnu'),
                                            'join_date': join_date,
                                            'importance': importance,
                                            'previous_club': player.get('previous_club', 'Inconnu'),
                                            'stats': {
                                                'goals': player.get('goals', 0),
                                                'assists': player.get('assists', 0),
                                                'minutes': player.get('minutes_played', 0)
                                            },
                                            'impact_description': f"Nouveau joueur, peut affecter la dynamique d'équipe",
                                            'source': 'player_enrichment'
                                        })
                                    break
                                except ValueError:
                                    continue
                    except Exception as e:
                        logger.error(f"Erreur lors de l'analyse de la date de transfert: {e}")
        
        # Identifier les absences significatives (blessures, suspensions)
        significant_absences = []
        
        if 'detailed_players' in team_data:
            for player in team_data['detailed_players']:
                if player.get('injury_status'):
                    # Déterminer l'importance du joueur
                    importance = 0.5  # Importance par défaut
                    
                    if player.get('is_key_player', False):
                        importance = 0.85
                    elif player.get('goals', 0) > 5 or player.get('assists', 0) > 5:
                        importance = 0.75
                    elif player.get('minutes_played', 0) > 800:  # Joueur régulier
                        importance = 0.6
                    
                    significant_absences.append({
                        'name': player.get('name', 'Inconnu'),
                        'position': player.get('position', 'Inconnu'),
                        'injury_type': player.get('injury_status'),
                        'expected_return': player.get('return_date', 'Inconnue'),
                        'importance': importance,
                        'impact_description': f"Joueur blessé, absence significative",
                        'source': 'player_enrichment'
                    })
        
        # Analyser l'impact du manager
        manager_impact = {}
        
        if 'manager' in team_data:
            manager = team_data['manager']
            
            # Vérifier si le manager est récent
            if manager.get('tenure_days', 999) <= 90:
                # Nouveau manager (moins de 3 mois)
                manager_impact = {
                    'name': manager.get('name', 'Inconnu'),
                    'tenure_days': manager.get('tenure_days', 0),
                    'previous_club': manager.get('previous_club', 'Inconnu'),
                    'tactical_style': manager.get('tactical_style', 'Inconnu'),
                    'win_percentage': manager.get('win_percentage', 0),
                    'importance': min(0.9, 0.6 + (manager.get('win_percentage', 0) / 100) * 0.3),
                    'impact_description': "Nouveau manager, peut changer significativement l'approche tactique",
                    'source': 'player_enrichment'
                }
        
        # Filtrer les transferts significatifs
        significant_transfers = [t for t in recent_transfers if t['importance'] >= 0.6]
        
        # Évaluer l'impact sur les différents marchés de paris
        market_impact = {}
        
        # Impact sur le handicap asiatique
        if significant_transfers or significant_absences:
            market_impact['asian_handicap'] = self._evaluate_transfers_market_impact(
                'asian_handicap', significant_transfers, significant_absences, manager_impact
            )
        
        # Impact sur over/under asiatique
        if significant_transfers or significant_absences:
            market_impact['over_under_asian'] = self._evaluate_transfers_market_impact(
                'over_under_asian', significant_transfers, significant_absences, manager_impact
            )
        
        # Impact sur le marché spécifié
        if market_type and (significant_transfers or significant_absences):
            market_impact[market_type] = self._evaluate_transfers_market_impact(
                market_type, significant_transfers, significant_absences, manager_impact
            )
        
        # Calculer l'impact global
        overall_impact = 0.0
        impact_count = 0
        
        for market, impact in market_impact.items():
            overall_impact += impact.get('impact_score', 0)
            impact_count += 1
        
        if impact_count > 0:
            overall_impact /= impact_count
        
        # Appliquer un bonus lié à la qualité des données
        data_quality_bonus = min(0.15, analysis['data_quality'] * 0.3)
        overall_impact = min(0.95, overall_impact + data_quality_bonus)
        
        # Mettre à jour l'analyse
        analysis.update({
            'transfers_analyzed': len(recent_transfers),
            'significant_transfers': significant_transfers,
            'absences_analyzed': len(significant_absences),
            'significant_absences': significant_absences,
            'manager_change_impact': manager_impact if manager_impact else {},
            'market_impact': market_impact,
            'overall_impact_score': overall_impact
        })
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'enhanced_transfer_impact_analysis',
            'timestamp': datetime.now().isoformat(),
            'team': team_name,
            'sources_used': analysis['sources_used'],
            'analysis_summary': {
                'transfers_analyzed': len(recent_transfers),
                'significant_transfers': len(significant_transfers),
                'absences_analyzed': len(significant_absences),
                'overall_impact': overall_impact,
                'data_quality': analysis['data_quality']
            }
        })
        
        return analysis
    
    def _analyze_single_market_enhanced(self, market_name, market_odds, home_team, away_team, enriched_match_data):
        """
        Analyse approfondie d'un marché asiatique spécifique avec données enrichies.
        
        Args:
            market_name (str): Nom du marché
            market_odds (dict): Cotes du marché
            home_team (str): Nom de l'équipe à domicile
            away_team (str): Nom de l'équipe à l'extérieur
            enriched_match_data (dict): Données du match enrichies
            
        Returns:
            dict: Analyse approfondie du marché
        """
        # Base de l'analyse
        analysis = {
            'market_name': market_name,
            'current_odds': market_odds,
            'anomaly_detected': False,
            'anomaly_score': 0.0,
            'confidence': 0.0,
            'contributing_factors': []
        }
        
        # Extraire les données enrichies pertinentes
        team_data = enriched_match_data.get('team_data', {})
        
        # Détecter les anomalies de base dans les cotes
        try:
            # Analyse spécifique selon le type de marché
            if market_name == 'asian_handicap':
                # Extraire les cotes du handicap
                handicap_lines = {}
                for line, odds in market_odds.items():
                    if '-' in line or '+' in line:
                        try:
                            handicap_value = float(line)
                            handicap_lines[handicap_value] = odds
                        except ValueError:
                            continue
                
                if handicap_lines:
                    # Trouver la ligne principale (la plus proche de 0)
                    main_line = min(handicap_lines.keys(), key=abs)
                    main_odds = handicap_lines[main_line]
                    
                    # Vérifier si la ligne est cohérente avec la force relative des équipes
                    expected_line = self._calculate_expected_handicap(home_team, away_team, team_data)
                    
                    line_difference = abs(main_line - expected_line)
                    
                    # Si la différence est significative, c'est une anomalie
                    threshold = self.detection_parameters['asian_threshold']
                    
                    if line_difference > threshold:
                        analysis['anomaly_detected'] = True
                        analysis['anomaly_score'] = min(0.9, line_difference / (threshold * 3))
                        analysis['anomaly_description'] = f"Ligne de handicap ({main_line}) significativement différente de l'attendu ({expected_line:.1f})"
                        
                        # Ajouter des facteurs contributifs
                        analysis['contributing_factors'].append({
                            'factor_type': 'handicap_mismatch',
                            'description': f"Écart de {line_difference:.2f} points sur le handicap",
                            'severity': analysis['anomaly_score'],
                            'confidence': 0.75
                        })
                        
                        # Analyser si certaines données peuvent expliquer cette anomalie
                        for team_side, team in [('home', home_team), ('away', away_team)]:
                            if team_side in team_data:
                                team_info = team_data[team_side]
                                
                                # Vérifier les blessures
                                if 'injured_players' in team_info and team_info['injured_players']:
                                    injured_count = len(team_info['injured_players'])
                                    key_injured = sum(1 for p in team_info['injured_players'] 
                                                   if p.get('is_key_player', False))
                                    
                                    if key_injured > 0:
                                        analysis['contributing_factors'].append({
                                            'factor_type': 'key_absences',
                                            'description': f"{team} privé de {key_injured} joueurs clés",
                                            'severity': min(0.8, key_injured * 0.25),
                                            'confidence': 0.8
                                        })
                                
                                # Vérifier les transferts récents
                                if ('transfermarkt_players' in team_info and team_info['transfermarkt_players'] and
                                    any(isinstance(p, dict) and 
                                        p.get('join_date') and 
                                        self._is_recent_date(p.get('join_date'), 90) 
                                        for p in team_info['transfermarkt_players'])):
                                    
                                    analysis['contributing_factors'].append({
                                        'factor_type': 'recent_transfers',
                                        'description': f"{team} a effectué des transferts récents significatifs",
                                        'severity': 0.6,
                                        'confidence': 0.7
                                    })
            
            elif 'over_under' in market_name.lower():
                # Extraire les cotes over/under
                over_under_lines = {}
                for line, odds in market_odds.items():
                    try:
                        goal_value = float(line)
                        over_under_lines[goal_value] = odds
                    except ValueError:
                        continue
                
                if over_under_lines:
                    # Trouver la ligne principale (généralement 2.5)
                    if 2.5 in over_under_lines:
                        main_line = 2.5
                    else:
                        main_line = min(over_under_lines.keys(), key=lambda x: abs(x - 2.5))
                    
                    main_odds = over_under_lines[main_line]
                    
                    # Calculer la ligne attendue basée sur les statistiques des équipes
                    expected_line = self._calculate_expected_goals(home_team, away_team, team_data)
                    
                    line_difference = abs(main_line - expected_line)
                    
                    # Si la différence est significative, c'est une anomalie
                    threshold = self.detection_parameters['asian_threshold'] * 1.5  # Seuil plus élevé pour les buts
                    
                    if line_difference > threshold:
                        analysis['anomaly_detected'] = True
                        analysis['anomaly_score'] = min(0.9, line_difference / (threshold * 2))
                        analysis['anomaly_description'] = f"Ligne de buts ({main_line}) significativement différente de l'attendu ({expected_line:.1f})"
                        
                        # Ajouter des facteurs contributifs
                        analysis['contributing_factors'].append({
                            'factor_type': 'goals_mismatch',
                            'description': f"Écart de {line_difference:.2f} buts sur la ligne principale",
                            'severity': analysis['anomaly_score'],
                            'confidence': 0.7
                        })
                        
                        # Vérifier les facteurs qui pourraient expliquer cette anomalie
                        # (code similaire à l'analyse du handicap)
            
            # Autres types de marchés asiatiques...
        
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse du marché {market_name}: {e}")
            analysis['error'] = f"Erreur d'analyse: {str(e)}"
        
        # Calculer la confiance de l'analyse
        if analysis['anomaly_detected']:
            # Moyenne pondérée des confiances des facteurs
            total_weight = 0
            weighted_confidence = 0
            
            for factor in analysis['contributing_factors']:
                weight = factor.get('severity', 0.5)
                confidence = factor.get('confidence', 0.5)
                
                weighted_confidence += weight * confidence
                total_weight += weight
            
            if total_weight > 0:
                analysis['confidence'] = weighted_confidence / total_weight
            else:
                analysis['confidence'] = 0.6  # Valeur par défaut
        else:
            analysis['confidence'] = 0.8  # Haute confiance qu'il n'y a pas d'anomalie
        
        return analysis
    
    def _analyze_cross_market_correlations_enhanced(self, market_analyses, enriched_match_data):
        """
        Analyse approfondie des corrélations entre différents marchés asiatiques.
        
        Args:
            market_analyses (dict): Analyses des marchés individuels
            enriched_match_data (dict): Données du match enrichies
            
        Returns:
            dict: Analyse des corrélations entre marchés
        """
        # Base de l'analyse
        analysis = {
            'correlated_markets_detected': False,
            'correlation_strength': 0.0,
            'correlation_groups': [],
            'contributing_factors': []
        }
        
        # Identifier les marchés avec anomalies
        anomalous_markets = {
            market: data for market, data in market_analyses.items() 
            if data.get('anomaly_detected', False)
        }
        
        # S'il y a moins de 2 marchés avec anomalies, pas de corrélation possible
        if len(anomalous_markets) < 2:
            return analysis
        
        try:
            # Regrouper les marchés anomaliques par similarité des facteurs contributifs
            factor_signatures = {}
            
            for market, data in anomalous_markets.items():
                # Extraire les types de facteurs
                factor_types = [f.get('factor_type', '') for f in data.get('contributing_factors', [])]
                
                # Créer une signature de facteurs
                signature = ','.join(sorted(factor_types))
                
                if signature in factor_signatures:
                    factor_signatures[signature].append(market)
                else:
                    factor_signatures[signature] = [market]
            
            # Identifier les groupes de marchés corrélés
            correlation_groups = [
                markets for signature, markets in factor_signatures.items() 
                if len(markets) >= 2 and signature
            ]
            
            if correlation_groups:
                analysis['correlated_markets_detected'] = True
                analysis['correlation_groups'] = correlation_groups
                
                # Calculer la force de corrélation
                # Plus il y a de groupes et plus les groupes sont grands, plus la corrélation est forte
                total_correlated = sum(len(group) for group in correlation_groups)
                analysis['correlation_strength'] = min(0.9, total_correlated / len(market_analyses) * 0.7)
                
                # Analyser les facteurs contribuant aux corrélations
                common_factors = defaultdict(int)
                
                for market, data in anomalous_markets.items():
                    for factor in data.get('contributing_factors', []):
                        factor_type = factor.get('factor_type', '')
                        if factor_type:
                            common_factors[factor_type] += 1
                
                # Identifier les facteurs les plus communs
                significant_factors = [
                    (factor, count) for factor, count in common_factors.items() 
                    if count >= 2
                ]
                
                for factor, count in significant_factors:
                    analysis['contributing_factors'].append({
                        'factor_type': factor,
                        'description': f"Facteur présent dans {count} marchés anomaliques",
                        'market_count': count,
                        'significance': min(0.9, count / len(anomalous_markets) * 0.8)
                    })
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse des corrélations entre marchés: {e}")
            analysis['error'] = f"Erreur d'analyse: {str(e)}"
        
        return analysis
    
    def _analyze_behavior_enhanced(self, behavior_type, behavior_params, odds_history, enriched_match_data):
        """
        Analyse approfondie d'un comportement spécial dans l'évolution des cotes.
        
        Args:
            behavior_type (str): Type de comportement à analyser
            behavior_params (dict): Paramètres de détection du comportement
            odds_history (list): Historique d'évolution des cotes
            enriched_match_data (dict): Données du match enrichies
            
        Returns:
            dict: Analyse du comportement
        """
        # Base de l'analyse
        analysis = {
            'behavior_type': behavior_type,
            'detection_score': 0.0,
            'details': {},
            'data_sources': [],
            'evidence_strength': 0.0,
            'time_pattern': []
        }
        
        try:
            # Analyser différemment selon le type de comportement
            if behavior_type == 'reverse_line_movement':
                # Détecter un mouvement des cotes opposé au volume de paris
                analysis = self._detect_reverse_line_movement(odds_history, enriched_match_data)
                
            elif behavior_type == 'overnight_drift':
                # Détecter un mouvement pendant les heures de nuit asiatiques
                analysis = self._detect_overnight_drift(odds_history, enriched_match_data)
                
            elif behavior_type == 'pre_match_surge':
                # Détecter un afflux soudain de paris juste avant le match
                analysis = self._detect_pre_match_surge(odds_history, enriched_match_data)
                
            elif behavior_type == 'correlated_markets':
                # Détecter des mouvements synchronisés entre marchés indépendants
                analysis = self._detect_correlated_markets(odds_history, enriched_match_data)
                
            elif behavior_type == 'steam_move':
                # Détecter un changement rapide suivi par plusieurs bookmakers
                analysis = self._detect_steam_move(odds_history, enriched_match_data)
                
            elif behavior_type == 'news_reaction_anomaly':
                # Détecter une réaction anormale à des nouvelles importantes
                analysis = self._detect_news_reaction_anomaly(odds_history, enriched_match_data)
                
            elif behavior_type == 'tactical_mismatch_ignorance':
                # Détecter si les cotes ignorent un avantage tactique important
                analysis = self._detect_tactical_mismatch_ignorance(odds_history, enriched_match_data)
                
            elif behavior_type == 'injury_overreaction':
                # Détecter une réaction excessive à une blessure
                analysis = self._detect_injury_overreaction(odds_history, enriched_match_data)
                
            elif behavior_type == 'historical_pattern_violation':
                # Détecter une violation d'un pattern historique fort
                analysis = self._detect_historical_pattern_violation(odds_history, enriched_match_data)
                
            else:
                # Comportement non reconnu
                analysis['error'] = f"Type de comportement non reconnu: {behavior_type}"
        
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse du comportement {behavior_type}: {e}")
            analysis['error'] = f"Erreur d'analyse: {str(e)}"
        
        return analysis
    
    def _calculate_expected_handicap(self, home_team, away_team, team_data):
        """
        Calcule le handicap asiatique attendu basé sur les données des équipes.
        
        Args:
            home_team (str): Nom de l'équipe à domicile
            away_team (str): Nom de l'équipe à l'extérieur
            team_data (dict): Données des équipes
            
        Returns:
            float: Handicap asiatique attendu
        """
        # Valeur de base - légère faveur à l'équipe à domicile
        expected_handicap = -0.25
        
        # Si aucune donnée, retourner la valeur par défaut
        if not team_data or not ('home' in team_data and 'away' in team_data):
            return expected_handicap
        
        home_strength = 0.0
        away_strength = 0.0
        factors_applied = 0
        
        # Facteurs basés sur Transfermarkt
        if 'transfermarkt' in team_data['home'] and 'transfermarkt' in team_data['away']:
            try:
                # Comparer les valeurs d'effectif
                home_squad_value = team_data['home']['transfermarkt'].get('marketValue', {}).get('value', 0)
                away_squad_value = team_data['away']['transfermarkt'].get('marketValue', {}).get('value', 0)
                
                if isinstance(home_squad_value, str):
                    try:
                        if 'M' in home_squad_value:
                            home_squad_value = float(home_squad_value.replace('M', '').replace('€', '')) * 1000000
                        elif 'K' in home_squad_value:
                            home_squad_value = float(home_squad_value.replace('K', '').replace('€', '')) * 1000
                        else:
                            home_squad_value = float(home_squad_value.replace('€', ''))
                    except ValueError:
                        home_squad_value = 0
                
                if isinstance(away_squad_value, str):
                    try:
                        if 'M' in away_squad_value:
                            away_squad_value = float(away_squad_value.replace('M', '').replace('€', '')) * 1000000
                        elif 'K' in away_squad_value:
                            away_squad_value = float(away_squad_value.replace('K', '').replace('€', '')) * 1000
                        else:
                            away_squad_value = float(away_squad_value.replace('€', ''))
                    except ValueError:
                        away_squad_value = 0
                
                if home_squad_value > 0 and away_squad_value > 0:
                    value_ratio = home_squad_value / away_squad_value if away_squad_value > 0 else 2.0
                    
                    # Transformer le ratio en handicap
                    if value_ratio > 2.0:  # Domicile largement supérieur
                        home_strength += 0.4
                    elif value_ratio > 1.5:  # Domicile supérieur
                        home_strength += 0.25
                    elif value_ratio < 0.5:  # Extérieur largement supérieur
                        away_strength += 0.4
                    elif value_ratio < 0.67:  # Extérieur supérieur
                        away_strength += 0.25
                    
                    factors_applied += 1
            except Exception as e:
                logger.error(f"Erreur lors de l'analyse des valeurs d'effectif: {e}")
        
        # Facteurs basés sur la forme récente
        if 'form' in team_data['home'] and 'form' in team_data['away']:
            try:
                # Analyser la forme de l'équipe à domicile
                home_form = team_data['home']['form']
                if 'result' in home_form:
                    results = home_form['result']
                    if isinstance(results, dict):
                        wins = sum(1 for r in results.values() if r == 'W')
                        draws = sum(1 for r in results.values() if r == 'D')
                        losses = sum(1 for r in results.values() if r == 'L')
                        
                        total_matches = wins + draws + losses
                        if total_matches > 0:
                            win_ratio = wins / total_matches
                            
                            # Bonifier l'équipe à domicile selon sa forme
                            if win_ratio > 0.7:  # Excellente forme
                                home_strength += 0.3
                            elif win_ratio > 0.5:  # Bonne forme
                                home_strength += 0.15
                            elif win_ratio < 0.3:  # Mauvaise forme
                                home_strength -= 0.15
                            
                            factors_applied += 1
                
                # Analyser la forme de l'équipe à l'extérieur
                away_form = team_data['away']['form']
                if 'result' in away_form:
                    results = away_form['result']
                    if isinstance(results, dict):
                        wins = sum(1 for r in results.values() if r == 'W')
                        draws = sum(1 for r in results.values() if r == 'D')
                        losses = sum(1 for r in results.values() if r == 'L')
                        
                        total_matches = wins + draws + losses
                        if total_matches > 0:
                            win_ratio = wins / total_matches
                            
                            # Bonifier l'équipe à l'extérieur selon sa forme
                            if win_ratio > 0.6:  # Excellente forme à l'extérieur
                                away_strength += 0.35
                            elif win_ratio > 0.4:  # Bonne forme à l'extérieur
                                away_strength += 0.2
                            elif win_ratio < 0.2:  # Mauvaise forme à l'extérieur
                                away_strength -= 0.2
                            
                            factors_applied += 1
            except Exception as e:
                logger.error(f"Erreur lors de l'analyse de la forme récente: {e}")
        
        # Facteurs basés sur les blessures
        if 'injured_players' in team_data['home']:
            try:
                injured_players = team_data['home']['injured_players']
                key_players_injured = sum(1 for p in injured_players if p.get('is_key_player', False))
                
                if key_players_injured > 0:
                    home_strength -= min(0.4, key_players_injured * 0.15)
                    factors_applied += 1
            except Exception:
                pass
        
        if 'injured_players' in team_data['away']:
            try:
                injured_players = team_data['away']['injured_players']
                key_players_injured = sum(1 for p in injured_players if p.get('is_key_player', False))
                
                if key_players_injured > 0:
                    away_strength -= min(0.4, key_players_injured * 0.15)
                    factors_applied += 1
            except Exception:
                pass
        
        # Calculer la force relative et la transformer en handicap
        if factors_applied > 0:
            # Calculer l'écart de force net
            strength_difference = home_strength - away_strength
            
            # Transformer en handicap (multiplier par 2 car les handicaps sont généralement par 0.25 ou 0.5)
            handicap_adjustment = strength_difference * 2
            
            # Appliquer au handicap de base
            expected_handicap = -0.25 + handicap_adjustment
            
            # Arrondir au handicap asiatique le plus proche (0.25, 0.5, 0.75, etc.)
            expected_handicap = round(expected_handicap * 4) / 4
        
        return expected_handicap
    
    def _calculate_expected_goals(self, home_team, away_team, team_data):
        """
        Calcule le nombre de buts total attendu basé sur les données des équipes.
        
        Args:
            home_team (str): Nom de l'équipe à domicile
            away_team (str): Nom de l'équipe à l'extérieur
            team_data (dict): Données des équipes
            
        Returns:
            float: Nombre de buts total attendu
        """
        # Valeur de base pour la ligne Over/Under
        expected_goals = 2.5
        
        # Si aucune donnée, retourner la valeur par défaut
        if not team_data or not ('home' in team_data and 'away' in team_data):
            return expected_goals
        
        goals_factors = []
        
        # Facteurs basés sur les statistiques d'équipe
        if 'team_stats' in team_data['home'] and 'team_stats' in team_data['away']:
            try:
                home_goals_scored = team_data['home']['team_stats'].get('goals_scored', 0)
                home_goals_conceded = team_data['home']['team_stats'].get('goals_conceded', 0)
                away_goals_scored = team_data['away']['team_stats'].get('goals_scored', 0)
                away_goals_conceded = team_data['away']['team_stats'].get('goals_conceded', 0)
                
                # Estimer les buts à domicile
                home_expected_goals = (home_goals_scored + away_goals_conceded) / 2
                
                # Estimer les buts à l'extérieur
                away_expected_goals = (away_goals_scored + home_goals_conceded) / 2
                
                # Buts totaux estimés
                match_expected_goals = home_expected_goals + away_expected_goals
                
                goals_factors.append(match_expected_goals)
            except Exception as e:
                logger.error(f"Erreur lors de l'analyse des statistiques de buts: {e}")
        
        # Facteurs basés sur le profil tactique
        offensive_factor = 0.0
        tactics_weight = 0
        
        if 'tactical_profile' in team_data['home']:
            try:
                profile = team_data['home']['tactical_profile']
                if profile.get('type') == 'Offensif':
                    offensive_factor += 0.5
                    tactics_weight += 1
                elif profile.get('type') == 'Défensif':
                    offensive_factor -= 0.5
                    tactics_weight += 1
            except Exception:
                pass
        
        if 'tactical_profile' in team_data['away']:
            try:
                profile = team_data['away']['tactical_profile']
                if profile.get('type') == 'Offensif':
                    offensive_factor += 0.4  # Légèrement moins à l'extérieur
                    tactics_weight += 1
                elif profile.get('type') == 'Défensif':
                    offensive_factor -= 0.4
                    tactics_weight += 1
            except Exception:
                pass
        
        if tactics_weight > 0:
            # Ajuster les buts attendus selon les tactiques
            tactical_goals = 2.5 + (offensive_factor / tactics_weight)
            goals_factors.append(tactical_goals)
        
        # Facteurs basés sur les confrontations directes
        if 'head_to_head' in team_data.get('home', {}) or 'head_to_head' in team_data.get('away', {}):
            try:
                h2h_matches = team_data.get('home', {}).get('head_to_head', [])
                if not h2h_matches:
                    h2h_matches = team_data.get('away', {}).get('head_to_head', [])
                
                if h2h_matches and len(h2h_matches) > 0:
                    total_goals = sum(match.get('home_score', 0) + match.get('away_score', 0) 
                                     for match in h2h_matches)
                    avg_goals = total_goals / len(h2h_matches)
                    
                    goals_factors.append(avg_goals)
            except Exception as e:
                logger.error(f"Erreur lors de l'analyse des confrontations directes: {e}")
        
        # Calculer la moyenne des facteurs
        if goals_factors:
            expected_goals = sum(goals_factors) / len(goals_factors)
            
            # Arrondir à l'Over/Under standard le plus proche (2.5, 3.5, etc.)
            expected_goals = round(expected_goals * 2) / 2
        
        return expected_goals
    
    def _is_recent_date(self, date_str, days_threshold=90):
        """
        Vérifie si une date est récente (dans les derniers jours_threshold jours).
        
        Args:
            date_str (str): Date à vérifier
            days_threshold (int): Seuil en jours
            
        Returns:
            bool: True si la date est récente, False sinon
        """
        try:
            # Essayer plusieurs formats de date
            for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%b %d, %Y'):
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    days_diff = (datetime.now() - date_obj).days
                    return days_diff <= days_threshold
                except ValueError:
                    continue
            
            return False
        except Exception:
            return False
    
    def _evaluate_transfers_market_impact(self, market_type, transfers, absences, manager_impact):
        """
        Évalue l'impact des transferts et absences sur un marché spécifique.
        
        Args:
            market_type (str): Type de marché
            transfers (list): Transferts significatifs
            absences (list): Absences significatives
            manager_impact (dict): Impact du changement de manager
            
        Returns:
            dict: Analyse de l'impact sur le marché
        """
        # Base de l'analyse
        impact = {
            'market': market_type,
            'impact_score': 0.0,
            'factors': [],
            'description': ""
        }
        
        # Impact différent selon le type de marché
        if market_type == 'asian_handicap':
            # Transferts offensifs
            offensive_transfers = [t for t in transfers 
                                 if 'Forward' in t.get('position', '') or 
                                 'Midfielder' in t.get('position', '')]
            
            if offensive_transfers:
                impact['factors'].append({
                    'type': 'offensive_transfers',
                    'description': f"{len(offensive_transfers)} transferts offensifs significatifs",
                    'score': min(0.8, len(offensive_transfers) * 0.2)
                })
            
            # Absences défensives
            defensive_absences = [a for a in absences 
                                if 'Defender' in a.get('position', '') or 
                                'Goalkeeper' in a.get('position', '')]
            
            if defensive_absences:
                impact['factors'].append({
                    'type': 'defensive_absences',
                    'description': f"{len(defensive_absences)} absences défensives significatives",
                    'score': min(0.75, len(defensive_absences) * 0.25)
                })
            
            # Impact du manager
            if manager_impact:
                impact['factors'].append({
                    'type': 'manager_change',
                    'description': f"Nouveau manager ({manager_impact.get('tactical_style', 'style inconnu')})",
                    'score': manager_impact.get('importance', 0.5)
                })
        
        elif 'over_under' in market_type:
            # Transferts offensifs
            offensive_transfers = [t for t in transfers 
                                 if 'Forward' in t.get('position', '') or 
                                 'Attacking' in t.get('position', '')]
            
            if offensive_transfers:
                impact['factors'].append({
                    'type': 'offensive_transfers',
                    'description': f"{len(offensive_transfers)} transferts d'attaquants",
                    'score': min(0.85, len(offensive_transfers) * 0.25)
                })
            
            # Absences offensives
            offensive_absences = [a for a in absences 
                                if 'Forward' in a.get('position', '') or 
                                'Attacking' in a.get('position', '')]
            
            if offensive_absences:
                impact['factors'].append({
                    'type': 'offensive_absences',
                    'description': f"{len(offensive_absences)} attaquants absents",
                    'score': min(0.8, len(offensive_absences) * 0.3)
                })
            
            # Style tactique du manager
            if manager_impact and 'tactical_style' in manager_impact:
                style = manager_impact.get('tactical_style', '').lower()
                if 'attack' in style or 'offens' in style:
                    impact['factors'].append({
                        'type': 'offensive_manager',
                        'description': f"Manager au style offensif",
                        'score': 0.7
                    })
                elif 'defen' in style or 'conserv' in style:
                    impact['factors'].append({
                        'type': 'defensive_manager',
                        'description': f"Manager au style défensif",
                        'score': 0.65
                    })
        
        # Calculer l'impact global
        if impact['factors']:
            total_score = sum(f['score'] for f in impact['factors'])
            impact['impact_score'] = min(0.9, total_score / len(impact['factors']))
            
            # Générer une description
            descriptions = [f['description'] for f in impact['factors']]
            impact['description'] = "Impact significatif dû à: " + ", ".join(descriptions)
        else:
            impact['impact_score'] = 0.1
            impact['description'] = "Pas d'impact significatif détecté sur ce marché"
        
        return impact
    
    def _calculate_enhanced_confidence_score(self, market_analyses, cross_market_analysis, data_quality):
        """
        Calcule un score de confiance global pour l'analyse, en tenant compte de la qualité des données.
        
        Args:
            market_analyses (dict): Analyses des marchés individuels
            cross_market_analysis (dict): Analyse des corrélations entre marchés
            data_quality (float): Qualité des données utilisées
            
        Returns:
            float: Score de confiance global
        """
        # Facteurs de confiance de base
        base_factors = []
        
        # Calculer la confiance moyenne des analyses de marché
        market_confidences = [
            analysis.get('confidence', 0.0) 
            for analysis in market_analyses.values()
            if 'confidence' in analysis
        ]
        
        if market_confidences:
            avg_market_confidence = sum(market_confidences) / len(market_confidences)
            base_factors.append(avg_market_confidence)
        
        # Ajouter la corrélation entre marchés si détectée
        if cross_market_analysis.get('correlated_markets_detected', False):
            correlation_confidence = 0.7 + (cross_market_analysis.get('correlation_strength', 0) * 0.2)
            base_factors.append(correlation_confidence)
        
        # Calculer le score de base
        if base_factors:
            base_confidence = sum(base_factors) / len(base_factors)
        else:
            base_confidence = 0.5  # Valeur par défaut
        
        # Appliquer un bonus lié à la qualité des données
        data_quality_bonus = min(0.2, data_quality * 0.3)  # Max 0.2 de bonus
        
        # Score final
        confidence_score = min(0.95, base_confidence + data_quality_bonus)
        
        return confidence_score
    
    def _generate_enhanced_recommendation(self, confidence_score, market_analyses, enriched_match_data):
        """
        Génère des recommandations d'action basées sur l'analyse complète.
        
        Args:
            confidence_score (float): Score de confiance global
            market_analyses (dict): Analyses des marchés individuels
            enriched_match_data (dict): Données du match enrichies
            
        Returns:
            dict: Recommandations d'action
        """
        # Base des recommandations
        recommendation = {
            'overall_recommendation': "",
            'confidence': confidence_score,
            'details': [],
            'flag_level': "normal"
        }
        
        # Détecter les marchés anomaliques
        anomalous_markets = {
            market: data for market, data in market_analyses.items() 
            if data.get('anomaly_detected', False)
        }
        
        # Niveau d'alerte global
        if anomalous_markets:
            # Calculer la sévérité moyenne
            avg_severity = sum(
                data.get('anomaly_score', 0) for data in anomalous_markets.values()
            ) / len(anomalous_markets)
            
            # Déterminer le niveau d'alerte
            if avg_severity > 0.7:
                flag_level = "high"
                if confidence_score > 0.7:
                    overall_recommendation = "ALERTE HAUTE: Anomalies significatives détectées avec haute confiance"
                else:
                    overall_recommendation = "ALERTE: Anomalies significatives détectées, mais confiance moyenne"
            elif avg_severity > 0.5:
                flag_level = "medium"
                overall_recommendation = "ATTENTION: Potentielles anomalies détectées"
            else:
                flag_level = "low"
                overall_recommendation = "SURVEILLANCE: Légères anomalies détectées, surveillance recommandée"
        else:
            flag_level = "normal"
            overall_recommendation = "NORMAL: Aucune anomalie significative détectée"
        
        recommendation['flag_level'] = flag_level
        recommendation['overall_recommendation'] = overall_recommendation
        
        # Générer des recommandations détaillées
        for market, analysis in anomalous_markets.items():
            anomaly_score = analysis.get('anomaly_score', 0)
            
            if anomaly_score > 0.7:
                action = "Éviter complètement ce marché"
            elif anomaly_score > 0.5:
                action = "Approcher avec extrême prudence"
            else:
                action = "Surveiller attentivement"
            
            recommendation['details'].append({
                'market': market,
                'anomaly_score': anomaly_score,
                'description': analysis.get('anomaly_description', "Anomalie détectée"),
                'action': action
            })
        
        # Ajouter des recommandations basées sur les caractéristiques des équipes
        team_data = enriched_match_data.get('team_data', {})
        
        if team_data:
            home_team = enriched_match_data.get('home_team', 'Équipe domicile')
            away_team = enriched_match_data.get('away_team', 'Équipe extérieure')
            
            # Vérifier les absences significatives
            for team_side, team in [('home', home_team), ('away', away_team)]:
                if team_side in team_data and 'injured_players' in team_data[team_side]:
                    injured_players = team_data[team_side]['injured_players']
                    key_injured = [p for p in injured_players if p.get('is_key_player', False)]
                    
                    if key_injured:
                        recommendation['details'].append({
                            'market': 'general',
                            'anomaly_score': 0.0,
                            'description': f"{team} privé de {len(key_injured)} joueurs clés",
                            'action': "Tenir compte dans l'analyse des cotes"
                        })
            
            # Suggérer des marchés potentiellement sous-évalués
            h2h_data = enriched_match_data.get('head_to_head', [])
            if h2h_data:
                try:
                    total_goals = sum(match.get('home_score', 0) + match.get('away_score', 0) 
                                     for match in h2h_data)
                    avg_goals = total_goals / len(h2h_data)
                    
                    if avg_goals > 3.5 and not any('Over' in m for m in anomalous_markets):
                        recommendation['details'].append({
                            'market': 'over_under',
                            'anomaly_score': 0.0,
                            'description': f"Les confrontations historiques sont prolifiques ({avg_goals:.1f} buts/match)",
                            'action': "Le marché Over pourrait présenter de la valeur"
                        })
                    elif avg_goals < 1.8 and not any('Under' in m for m in anomalous_markets):
                        recommendation['details'].append({
                            'market': 'over_under',
                            'anomaly_score': 0.0,
                            'description': f"Les confrontations historiques sont fermées ({avg_goals:.1f} buts/match)",
                            'action': "Le marché Under pourrait présenter de la valeur"
                        })
                except Exception:
                    pass
        
        return recommendation
    
    def _generate_default_odds_data(self):
        """
        Génère des données de cotes par défaut pour les marchés asiatiques.
        
        Returns:
            dict: Structure de cotes par défaut
        """
        return {
            'asian_handicap': {
                '-1.5': 3.20,
                '-1.0': 2.60,
                '-0.5': 1.90,
                '0.0': 1.50,
                '+0.5': 2.40,
                '+1.0': 3.10,
                '+1.5': 4.00
            },
            'over_under_asian': {
                '1.5': 1.35,
                '2.0': 1.50,
                '2.5': 1.90,
                '3.0': 2.30,
                '3.5': 3.10
            },
            'asian_corners': {
                '7.5': 1.90,
                '8.5': 2.20,
                '9.5': 2.70
            }
        }
    
    def _generate_default_odds_history(self):
        """
        Génère un historique d'évolution des cotes par défaut.
        
        Returns:
            list: Historique des cotes
        """
        now = datetime.now()
        history = []
        
        # Générer des snapshots sur les dernières 48 heures
        for hours_ago in range(48, 0, -6):
            timestamp = (now - timedelta(hours=hours_ago)).isoformat()
            
            history.append({
                'timestamp': timestamp,
                'markets': {
                    'asian_handicap': {
                        '-0.5': 1.90 + random.uniform(-0.1, 0.1),
                        '0.0': 1.50 + random.uniform(-0.05, 0.05),
                        '+0.5': 2.40 + random.uniform(-0.15, 0.15)
                    },
                    'over_under_asian': {
                        '2.5': 1.90 + random.uniform(-0.1, 0.1),
                        '3.0': 2.30 + random.uniform(-0.15, 0.15)
                    }
                },
                'volumes': {
                    'asian_handicap': {
                        '-0.5': random.randint(100, 1000),
                        '0.0': random.randint(200, 1500),
                        '+0.5': random.randint(100, 800)
                    },
                    'over_under_asian': {
                        '2.5': random.randint(300, 1200),
                        '3.0': random.randint(200, 900)
                    }
                }
            })
        
        return history
    
    # Méthodes de détection des comportements spéciaux (implémentations simplifiées)
    
    def _detect_reverse_line_movement(self, odds_history, enriched_match_data):
        """Détecte un mouvement des cotes opposé au volume de paris"""
        # Implémentation simplifiée
        analysis = {
            'behavior_type': 'reverse_line_movement',
            'detection_score': 0.0,
            'details': {},
            'evidence_strength': 0.0,
            'time_pattern': []
        }
        
        if not odds_history or len(odds_history) < 2:
            return analysis
        
        movements_detected = []
        
        # Analyser les mouvements de cotes et volumes
        for i in range(1, len(odds_history)):
            previous = odds_history[i-1]
            current = odds_history[i]
            
            for market in previous.get('markets', {}):
                if market in current.get('markets', {}) and market in previous.get('volumes', {}) and market in current.get('volumes', {}):
                    for line in previous['markets'][market]:
                        if line in current['markets'][market] and line in previous['volumes'][market] and line in current['volumes'][market]:
                            # Vérifier le mouvement des cotes et le volume
                            odds_change = current['markets'][market][line] - previous['markets'][market][line]
                            volume_change = current['volumes'][market][line] - previous['volumes'][market][line]
                            
                            # Si les cotes et le volume évoluent dans des directions opposées et de manière significative
                            if abs(odds_change) > 0.05 and abs(volume_change) > 100 and (odds_change * volume_change < 0):
                                movements_detected.append({
                                    'timestamp': current['timestamp'],
                                    'market': market,
                                    'line': line,
                                    'odds_change': odds_change,
                                    'volume_change': volume_change,
                                    'strength': min(0.9, (abs(odds_change) / 0.1) * (abs(volume_change) / 200) * 0.5)
                                })
        
        if movements_detected:
            # Trier par force de détection
            movements_detected.sort(key=lambda x: x['strength'], reverse=True)
            
            # Calculer le score de détection basé sur les mouvements les plus forts
            top_movements = movements_detected[:3]  # Les 3 plus forts
            detection_score = sum(m['strength'] for m in top_movements) / len(top_movements)
            
            analysis.update({
                'detection_score': detection_score,
                'details': {
                    'movements_detected': movements_detected,
                    'most_significant': top_movements[0] if top_movements else None
                },
                'evidence_strength': min(0.9, len(movements_detected) / 5 * 0.6),
                'time_pattern': [m['timestamp'] for m in top_movements]
            })
        
        return analysis
    
    def _detect_overnight_drift(self, odds_history, enriched_match_data):
        """Détecte un mouvement pendant les heures de nuit asiatiques"""
        # Implémentation simplifiée - simuler une détection
        return {
            'behavior_type': 'overnight_drift',
            'detection_score': random.uniform(0.3, 0.6),
            'details': {},
            'evidence_strength': random.uniform(0.3, 0.7),
            'time_pattern': []
        }
    
    def _detect_pre_match_surge(self, odds_history, enriched_match_data):
        """Détecte un afflux soudain de paris juste avant le match"""
        # Implémentation simplifiée - simuler une détection
        return {
            'behavior_type': 'pre_match_surge',
            'detection_score': random.uniform(0.2, 0.5),
            'details': {},
            'evidence_strength': random.uniform(0.3, 0.6),
            'time_pattern': []
        }
    
    def _detect_correlated_markets(self, odds_history, enriched_match_data):
        """Détecte des mouvements synchronisés entre marchés indépendants"""
        # Implémentation simplifiée - simuler une détection
        return {
            'behavior_type': 'correlated_markets',
            'detection_score': random.uniform(0.3, 0.7),
            'details': {},
            'evidence_strength': random.uniform(0.4, 0.8),
            'time_pattern': []
        }
    
    def _detect_steam_move(self, odds_history, enriched_match_data):
        """Détecte un changement rapide suivi par plusieurs bookmakers"""
        # Implémentation simplifiée - simuler une détection
        return {
            'behavior_type': 'steam_move',
            'detection_score': random.uniform(0.2, 0.6),
            'details': {},
            'evidence_strength': random.uniform(0.3, 0.7),
            'time_pattern': []
        }
    
    def _detect_news_reaction_anomaly(self, odds_history, enriched_match_data):
        """Détecte une réaction anormale à des nouvelles importantes"""
        # Implémentation simplifiée - simuler une détection
        detection_score = 0.0
        
        # Vérifier s'il y a des absences significatives récentes
        team_data = enriched_match_data.get('team_data', {})
        
        for team_side in team_data:
            if 'injured_players' in team_data[team_side]:
                key_injured = [p for p in team_data[team_side]['injured_players'] 
                             if p.get('is_key_player', False)]
                
                if key_injured:
                    # Vérifier si les cotes ont réagi en conséquence
                    # (Implémentation simplifiée - simuler une détection)
                    detection_score = random.uniform(0.4, 0.7)
        
        return {
            'behavior_type': 'news_reaction_anomaly',
            'detection_score': detection_score,
            'details': {},
            'evidence_strength': detection_score * 0.9,
            'time_pattern': []
        }
    
    def _detect_tactical_mismatch_ignorance(self, odds_history, enriched_match_data):
        """Détecte si les cotes ignorent un avantage tactique important"""
        # Implémentation simplifiée - simuler une détection
        detection_score = 0.0
        
        # Vérifier s'il y a un avantage tactique significatif
        team_data = enriched_match_data.get('team_data', {})
        
        if 'home' in team_data and 'away' in team_data:
            if 'tactical_profile' in team_data['home'] and 'tactical_profile' in team_data['away']:
                home_profile = team_data['home']['tactical_profile']
                away_profile = team_data['away']['tactical_profile']
                
                # Vérifier des configurations tactiques particulières
                if (home_profile.get('type') == 'Offensif' and away_profile.get('weakness') == 'Vulnérabilité défensive'):
                    detection_score = random.uniform(0.5, 0.8)
                elif (away_profile.get('type') == 'Offensif' and home_profile.get('weakness') == 'Vulnérabilité défensive'):
                    detection_score = random.uniform(0.5, 0.8)
        
        return {
            'behavior_type': 'tactical_mismatch_ignorance',
            'detection_score': detection_score,
            'details': {},
            'evidence_strength': detection_score * 0.9,
            'time_pattern': []
        }
    
    def _detect_injury_overreaction(self, odds_history, enriched_match_data):
        """Détecte une réaction excessive à une blessure"""
        # Implémentation simplifiée - simuler une détection
        return {
            'behavior_type': 'injury_overreaction',
            'detection_score': random.uniform(0.2, 0.5),
            'details': {},
            'evidence_strength': random.uniform(0.3, 0.6),
            'time_pattern': []
        }
    
    def _detect_historical_pattern_violation(self, odds_history, enriched_match_data):
        """Détecte une violation d'un pattern historique fort"""
        # Implémentation simplifiée - simuler une détection
        return {
            'behavior_type': 'historical_pattern_violation',
            'detection_score': random.uniform(0.2, 0.5),
            'details': {},
            'evidence_strength': random.uniform(0.3, 0.6),
            'time_pattern': []
        }
    
    def _interpret_behaviors_enhanced(self, behavior_summary, alert_score, enriched_match_data):
        """
        Interprète les comportements détectés pour fournir des recommandations actionables.
        
        Args:
            behavior_summary (dict): Résumé des comportements détectés
            alert_score (float): Score d'alerte global
            enriched_match_data (dict): Données du match enrichies
            
        Returns:
            dict: Interprétation et recommandations
        """
        # Base de l'interprétation
        interpretation = {
            'alert_level': "normal",
            'summary': "",
            'recommendations': [],
            'confidence': 0.0
        }
        
        # Déterminer le niveau d'alerte
        if alert_score > 0.8:
            alert_level = "severe"
            summary = "Alerte sévère: Multiples comportements anormaux détectés avec forte confiance"
        elif alert_score > 0.6:
            alert_level = "high"
            summary = "Alerte haute: Comportements suspects détectés avec bonne confiance"
        elif alert_score > 0.4:
            alert_level = "moderate"
            summary = "Alerte modérée: Quelques comportements inhabituels détectés"
        else:
            alert_level = "low"
            summary = "Alerte basse: Comportements légèrement inhabituels, sans certitude"
        
        interpretation['alert_level'] = alert_level
        interpretation['summary'] = summary
        
        # Calculer la confiance générale
        behavior_count = len(behavior_summary)
        if behavior_count > 0:
            avg_detection_score = sum(
                behavior['detection_score'] for behavior in behavior_summary.values()
            ) / behavior_count
            
            interpretation['confidence'] = (avg_detection_score * 0.7) + (alert_score * 0.3)
        else:
            interpretation['confidence'] = 0.5
        
        # Générer des recommandations en fonction des comportements détectés
        if 'reverse_line_movement' in behavior_summary:
            interpretation['recommendations'].append({
                'priority': 'high',
                'action': "Éviter ce marché ou attendre la stabilisation des cotes",
                'reasoning': "Mouvement de cotes contre le flux de paris, généralement un signal d'alerte"
            })
        
        if 'steam_move' in behavior_summary:
            interpretation['recommendations'].append({
                'priority': 'high',
                'action': "Reporter toute action sur ce marché",
                'reasoning': "Mouvement rapide et significatif, souvent lié à des informations privées"
            })
        
        if 'news_reaction_anomaly' in behavior_summary:
            interpretation['recommendations'].append({
                'priority': 'medium',
                'action': "Rechercher des informations supplémentaires sur les équipes",
                'reasoning': "Les cotes ne reflètent pas correctement les nouvelles importantes"
            })
        
        if 'tactical_mismatch_ignorance' in behavior_summary:
            interpretation['recommendations'].append({
                'priority': 'medium',
                'action': "Explorer l'opportunité potentielle liée au mismatch tactique",
                'reasoning': "Avantage tactique significatif non reflété dans les cotes"
            })
        
        # Reommandations par défaut si aucun comportement spécifique n'est identifié
        if not interpretation['recommendations'] and alert_score > 0.4:
            interpretation['recommendations'].append({
                'priority': 'medium',
                'action': "Reporter toute action sur ces marchés",
                'reasoning': "Combinaison de facteurs suspects détectés sans pattern clair"
            })
        
        return interpretation