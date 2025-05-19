"""
FanSentimentMonitor (Version Enrichie) - Module avancé d'analyse de l'influence des émotions collectives.
Cette version améliorée intègre des données de multiples sources (Transfermarkt, soccerdata, 
détails des joueurs/managers) pour une analyse plus précise du sentiment des supporters.
"""

import random
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict
import logging
import pandas as pd

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Intégration des modules de données
from api.transfermarkt_integration import (
    is_transfermarkt_available,
    get_team_profile,
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
    
    logger.info(f"FanSentimentMonitor amélioré initialisé avec sources additionnelles. SoccerData: {SOCCERDATA_AVAILABLE}, Enrichissement joueurs: {PLAYER_ENRICHMENT_AVAILABLE}")
except ImportError:
    DATA_HUB_AVAILABLE = False
    SOCCERDATA_AVAILABLE = False
    PLAYER_ENRICHMENT_AVAILABLE = False
    logger.warning("Hub d'intégration de données non disponible, fonctionnalités avancées désactivées")

class FanSentimentMonitorEnhanced:
    """
    FanSentimentMonitor Enrichi - Système avancé d'analyse de l'influence des émotions collectives des supporters.
    Cette version améliorée utilise des données provenant de multiples sources pour une analyse plus précise
    de l'impact des sentiments de masse sur les performances des équipes.
    """
    
    def __init__(self):
        """Initialise le module FanSentimentMonitor enrichi avec accès à toutes les sources de données"""
        # Vérifier si Transfermarkt est disponible
        self.transfermarkt_available = is_transfermarkt_available()
        
        if self.transfermarkt_available:
            logger.info("Transfermarkt disponible pour FanSentimentMonitor")
        else:
            logger.warning("API Transfermarkt non disponible, certaines fonctionnalités seront limitées")
        
        # Statut général des sources
        self.use_enhanced_data = DATA_HUB_AVAILABLE
        self.available_sources = {
            'transfermarkt': self.transfermarkt_available,
            'soccerdata': SOCCERDATA_AVAILABLE,
            'player_enrichment': PLAYER_ENRICHMENT_AVAILABLE
        }
        
        # Paramètres d'analyse améliorés (avec valorisation des données réelles)
        self.sentiment_parameters = {
            'emotional_impact': 0.35,      # Impact des émotions sur la performance (augmenté)
            'collective_resonance': 0.7,   # Force de la résonance collective (augmentée)
            'threshold_critical_mass': 0.65, # Seuil pour atteindre la masse critique (ajusté)
            'home_advantage_factor': 0.3,  # Facteur d'avantage à domicile supplémentaire (augmenté)
            'temporal_decay': 0.8,         # Décroissance temporelle du sentiment (ajustée)
            'real_data_factor': 0.2,       # Bonus d'impact pour les données réelles vs simulées
            'historical_weight': 0.6,      # Poids des tendances historiques (nouveau)
            'key_player_influence': 0.4    # Influence des joueurs clés sur le sentiment (nouveau)
        }
        
        # Types d'émotions collectives surveillées (version étendue)
        self.collective_emotions = [
            'euphoria',           # Euphorie collective
            'anxiety',            # Anxiété et nervosité
            'anger',              # Colère et frustration
            'confidence',         # Confiance et optimisme
            'desperation',        # Désespoir et résignation
            'nostalgia',          # Nostalgie pour des succès passés
            'anticipation',       # Anticipation et excitation
            'disappointment',     # Déception
            # Nouvelles émotions détectables grâce aux données enrichies
            'skepticism',         # Scepticisme face aux changements
            'vindication',        # Sentiment de revanche/justification
            'unity',              # Unité et solidarité exceptionnelles
            'admiration'          # Admiration pour un joueur/manager spécifique
        ]
        
        # Sources de données sentimentales (version étendue)
        self.sentiment_sources = {
            'social_media': {
                'weight': 0.35,
                'platforms': ['twitter', 'instagram', 'facebook', 'reddit', 'tiktok'],
                'metrics': ['volume', 'sentiment_ratio', 'emotional_intensity', 'virality', 'engagement_rate', 'topic_clustering']
            },
            'forum_discussions': {
                'weight': 0.2,
                'metrics': ['post_volume', 'comment_intensity', 'topic_sentiment', 'consensus_level', 'discussion_depth']
            },
            'news_media': {
                'weight': 0.15,
                'metrics': ['coverage_sentiment', 'headline_tone', 'article_volume', 'narrative_framing', 'expert_commentary']
            },
            'attendance_patterns': {
                'weight': 0.15,
                'metrics': ['attendance_percentage', 'ticket_demand', 'atmosphere_rating', 'chanting_intensity', 'attendance_trends']
            },
            # Nouvelles sources grâce aux données enrichies
            'merchandise_sales': {
                'weight': 0.05,
                'metrics': ['jersey_sales', 'purchase_timing', 'special_edition_demand', 'regional_distribution']
            },
            'fan_clubs_activity': {
                'weight': 0.1,
                'metrics': ['organized_events', 'membership_trends', 'coordinated_displays', 'international_support']
            }
        }
        
        # Nouvelles sources de données textuelles
        self.text_sources = {
            'player_interviews': {
                'weight': 0.15,
                'metrics': ['tone', 'confidence_level', 'fan_references', 'unity_messaging']
            },
            'manager_statements': {
                'weight': 0.2,
                'metrics': ['tone', 'fan_expectations_management', 'team_unity_emphasis', 'pressure_acknowledgment']
            },
            'club_communications': {
                'weight': 0.1,
                'metrics': ['tone', 'transparency', 'fan_engagement', 'message_consistency']
            }
        }
        
        # Historique des analyses
        self.analysis_history = []
        
        # Cache de sentiment
        self.sentiment_cache = {}
    
    def analyze_current_sentiment_enhanced(self, team_name, match_data=None, sentiment_data=None):
        """
        Analyser le sentiment actuel des supporters d'une équipe avec données multi-sources.
        
        Args:
            team_name (str): Nom de l'équipe
            match_data (dict, optional): Données du match à venir
            sentiment_data (dict, optional): Données de sentiment si disponibles
            
        Returns:
            dict: Analyse enrichie du sentiment des supporters
        """
        # Base de l'analyse
        analysis = {
            'team_name': team_name,
            'analysis_timestamp': datetime.now().isoformat(),
            'data_quality': 0.0,
            'sources_used': []
        }
        
        # Enrichir les données avec toutes les sources disponibles
        team_data = {}
        team_id = None
        
        # 1. Données Transfermarkt
        if self.transfermarkt_available:
            analysis['sources_used'].append('transfermarkt')
            
            # Rechercher l'ID de l'équipe
            try:
                search_results = search_club_by_name(team_name)
                if search_results and 'items' in search_results and search_results['items']:
                    team_id = search_results['items'][0]['id']
                    logger.info(f"ID Transfermarkt trouvé pour {team_name}: {team_id}")
                    
                    # Récupérer les données de l'équipe
                    if team_id:
                        team_profile = get_team_profile(team_id)
                        if 'status' not in team_profile or team_profile['status'] != 'error':
                            team_data['transfermarkt'] = team_profile
                            analysis['data_quality'] += 0.3
                            logger.info(f"Données Transfermarkt intégrées pour {team_name}")
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des données Transfermarkt pour {team_name}: {e}")
        
        # 2. Données soccerdata
        if SOCCERDATA_AVAILABLE:
            analysis['sources_used'].append('soccerdata')
            
            try:
                # Importer de manière dynamique
                from api.soccerdata_integration import get_team_form, get_team_stats
                
                # Récupérer la forme de l'équipe
                team_form = get_team_form(team_name)
                if not isinstance(team_form, str) and not team_form.empty:
                    team_data['form'] = team_form.to_dict()
                    analysis['data_quality'] += 0.2
                    logger.info(f"Données de forme intégrées pour {team_name}")
                
                # Récupérer les statistiques de l'équipe
                team_stats = get_team_stats(team_name)
                if not isinstance(team_stats, str) and not team_stats.empty:
                    team_data['stats'] = team_stats.iloc[0].to_dict() if len(team_stats) > 0 else {}
                    analysis['data_quality'] += 0.1
                    logger.info(f"Statistiques d'équipe intégrées pour {team_name}")
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des données soccerdata: {e}")
        
        # 3. Données d'enrichissement des joueurs
        if PLAYER_ENRICHMENT_AVAILABLE:
            analysis['sources_used'].append('player_enrichment')
            
            try:
                # Importer de manière dynamique
                from api.player_data_enrichment import get_team_detailed_players, get_team_manager
                
                # Récupérer les données détaillées des joueurs
                players = get_team_detailed_players(team_name)
                if players:
                    team_data['players'] = players
                    
                    # Identifier les joueurs clés et populaires
                    key_players = [p for p in players if p.get('is_key_player', False)]
                    popular_players = [p for p in players if p.get('popularity_score', 0) > 7]
                    
                    if key_players:
                        team_data['key_players'] = key_players
                        analysis['data_quality'] += 0.1
                    
                    if popular_players:
                        team_data['popular_players'] = popular_players
                        analysis['data_quality'] += 0.1
                    
                    logger.info(f"Données des joueurs intégrées pour {team_name}")
                
                # Récupérer les données du manager
                manager = get_team_manager(team_name)
                if manager:
                    team_data['manager'] = manager
                    analysis['data_quality'] += 0.1
                    logger.info(f"Données du manager intégrées pour {team_name}")
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des données d'enrichissement des joueurs: {e}")
        
        # Si des données de sentiment sont fournies, les utiliser
        # Sinon, vérifier le cache ou générer des données
        if sentiment_data is None:
            cache_key = f"{team_name}_{datetime.now().strftime('%Y-%m-%d')}"
            if cache_key in self.sentiment_cache:
                sentiment_data = self.sentiment_cache[cache_key]
            else:
                sentiment_data = self._generate_sentiment_data_enhanced(team_name, team_data)
                self.sentiment_cache[cache_key] = sentiment_data
        
        # Extraire le contexte du match si disponible
        match_context = None
        if match_data:
            match_context = {
                'opponent': match_data.get('away_team') if match_data.get('home_team') == team_name else match_data.get('home_team'),
                'is_home': match_data.get('home_team') == team_name,
                'importance': match_data.get('importance', 'regular'),
                'date': match_data.get('date', datetime.now().isoformat())
            }
        
        # Analyser chaque source de sentiment
        source_analyses = {}
        for source, source_config in self.sentiment_sources.items():
            source_data = sentiment_data.get(source, {})
            source_analyses[source] = self._analyze_sentiment_source_enhanced(
                source, source_data, source_config, team_name, team_data
            )
        
        # Analyser les sources textuelles si disponibles
        text_analyses = {}
        for source, source_config in self.text_sources.items():
            source_data = sentiment_data.get(source, {})
            text_analyses[source] = self._analyze_text_source(
                source, source_data, source_config, team_name
            )
        
        # Intégrer les analyses textuelles aux analyses de sources
        for source, analysis_data in text_analyses.items():
            source_analyses[source] = analysis_data
        
        # Calculer le sentiment dominant avec données enrichies
        dominant_emotion, emotion_scores = self._calculate_dominant_emotion_enhanced(source_analyses, team_data)
        
        # Calculer l'intensité globale
        overall_intensity = self._calculate_overall_intensity_enhanced(source_analyses, team_data)
        
        # Évaluer la cohésion du sentiment
        sentiment_cohesion = self._evaluate_sentiment_cohesion_enhanced(source_analyses)
        
        # Analyser les tendances récentes
        trend_analysis = self._analyze_sentiment_trends_enhanced(team_name, team_data)
        
        # Analyser les facteurs d'influence clés
        key_influence_factors = self._analyze_key_influence_factors(team_name, team_data)
        
        # Analyser le contexte du match si disponible
        match_influence = None
        if match_context:
            match_influence = self._analyze_match_influence_enhanced(
                match_context, dominant_emotion, overall_intensity, team_data
            )
        
        # Compiler l'analyse complète
        analysis.update({
            'dominant_emotion': dominant_emotion,
            'emotion_scores': emotion_scores,
            'overall_intensity': overall_intensity,
            'sentiment_cohesion': sentiment_cohesion,
            'source_analyses': source_analyses,
            'trend_analysis': trend_analysis,
            'key_influence_factors': key_influence_factors,
            'expected_impact': self._calculate_expected_impact_enhanced(
                dominant_emotion, overall_intensity, sentiment_cohesion, match_context, team_data
            )
        })
        
        if match_influence:
            analysis['match_influence'] = match_influence
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'enhanced_current_sentiment_analysis',
            'timestamp': datetime.now().isoformat(),
            'team': team_name,
            'sources_used': analysis['sources_used'],
            'summary': {
                'dominant_emotion': dominant_emotion,
                'intensity': overall_intensity,
                'cohesion': sentiment_cohesion.get('overall_cohesion', 0),
                'data_quality': analysis['data_quality']
            }
        })
        
        return analysis
    
    def predict_sentiment_impact_enhanced(self, team_name, match_data, recent_form=None):
        """
        Prédire l'impact du sentiment des supporters sur un match à venir avec données multi-sources.
        
        Args:
            team_name (str): Nom de l'équipe
            match_data (dict): Données du match à venir
            recent_form (list, optional): Forme récente de l'équipe
            
        Returns:
            dict: Prédiction enrichie de l'impact du sentiment
        """
        # Analyser le sentiment actuel
        current_sentiment = self.analyze_current_sentiment_enhanced(team_name, match_data)
        
        # Extraire le nom de l'adversaire
        opponent_name = match_data.get('away_team') if match_data.get('home_team') == team_name else match_data.get('home_team')
        
        # Base de la prédiction
        prediction = {
            'team_name': team_name,
            'opponent_name': opponent_name,
            'match_date': match_data.get('date', datetime.now().isoformat()),
            'prediction_timestamp': datetime.now().isoformat(),
            'data_quality': current_sentiment.get('data_quality', 0.0),
            'sources_used': current_sentiment.get('sources_used', [])
        }
        
        # Récupérer les données enrichies de l'équipe
        team_data = {}
        if 'key_influence_factors' in current_sentiment:
            for factor in current_sentiment['key_influence_factors']:
                if 'factor_data' in factor:
                    team_data[factor['factor_type']] = factor['factor_data']
        
        # Calculer l'importance du match avec données enrichies
        match_importance = self._calculate_match_importance_enhanced(match_data, team_name, opponent_name)
        
        # Déterminer si le match est à domicile
        is_home = match_data.get('home_team') == team_name
        
        # Analyser la forme récente avec données enrichies
        form_factor = 0.5  # Valeur neutre par défaut
        if recent_form:
            form_factor = self._analyze_recent_form_enhanced(recent_form)
        elif 'form' in team_data:
            form_factor = self._analyze_form_data(team_data['form'])
        
        # Calculer l'avantage ou désavantage sentimental de base
        base_impact = self._calculate_base_sentiment_impact_enhanced(
            current_sentiment, match_importance, is_home, team_data
        )
        
        # Analyser la rivalité entre les équipes
        rivalry_factor = self._analyze_rivalry(team_name, opponent_name, team_data)
        
        # Ajuster en fonction de facteurs spécifiques au match
        specific_factors = self._analyze_specific_factors_enhanced(
            team_name, opponent_name, match_data, team_data
        )
        
        # Ajouter le facteur de rivalité s'il est significatif
        if rivalry_factor > 0.2:
            specific_factors.append({
                'factor_type': 'rivalry',
                'description': f"Rivalité significative avec {opponent_name}",
                'impact_value': rivalry_factor * 0.3,
                'confidence': 0.8
            })
        
        # Calculer l'impact ajusté
        adjusted_impact = base_impact.copy()
        adjusted_impact['total_impact'] = base_impact['raw_impact']
        
        # Appliquer les ajustements
        for factor in specific_factors:
            factor_impact = factor.get('impact_value', 0)
            factor_confidence = factor.get('confidence', 0.5)
            
            # Pondérer l'impact par la confiance
            weighted_impact = factor_impact * factor_confidence
            adjusted_impact['total_impact'] += weighted_impact
            
            if 'factors' not in adjusted_impact:
                adjusted_impact['factors'] = []
            adjusted_impact['factors'].append(factor)
        
        # Limiter l'impact total
        adjusted_impact['total_impact'] = max(-1.0, min(1.0, adjusted_impact['total_impact']))
        
        # Déterminer le type d'impact
        adjusted_impact['impact_type'] = self._determine_impact_type_enhanced(adjusted_impact['total_impact'])
        
        # Générer des scénarios d'impact potentiels
        impact_scenarios = self._generate_impact_scenarios_enhanced(
            adjusted_impact, form_factor, team_data
        )
        
        # Calculer l'influence sur la performance
        performance_influence = self._calculate_performance_influence_enhanced(
            adjusted_impact, current_sentiment, form_factor, team_data
        )
        
        # Compiler la prédiction complète
        prediction.update({
            'current_sentiment': {
                'dominant_emotion': current_sentiment.get('dominant_emotion'),
                'overall_intensity': current_sentiment.get('overall_intensity'),
                'cohesion': current_sentiment.get('sentiment_cohesion', {}).get('overall_cohesion', 0)
            },
            'match_importance': match_importance,
            'is_home': is_home,
            'rivalry_factor': rivalry_factor,
            'base_impact': base_impact,
            'adjusted_impact': adjusted_impact,
            'impact_scenarios': impact_scenarios,
            'performance_influence': performance_influence
        })
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'enhanced_sentiment_impact_prediction',
            'timestamp': datetime.now().isoformat(),
            'team': team_name,
            'opponent': opponent_name,
            'match_date': match_data.get('date', datetime.now().isoformat()),
            'sources_used': prediction['sources_used'],
            'summary': {
                'impact_type': adjusted_impact.get('impact_type'),
                'total_impact': adjusted_impact.get('total_impact'),
                'dominant_emotion': current_sentiment.get('dominant_emotion'),
                'data_quality': prediction['data_quality']
            }
        })
        
        return prediction
    
    def _generate_sentiment_data_enhanced(self, team_name, team_data=None):
        """
        Génère des données de sentiment améliorées en intégrant des données réelles.
        
        Args:
            team_name (str): Nom de l'équipe
            team_data (dict, optional): Données enrichies de l'équipe
            
        Returns:
            dict: Données de sentiment générées
        """
        # Base des données de sentiment
        sentiment_data = {}
        
        # Déterminer les émotions dominantes basées sur des données réelles si disponibles
        primary_emotion = random.choice(self.collective_emotions[:8])  # Émotion de base
        secondary_emotion = random.choice([e for e in self.collective_emotions if e != primary_emotion])
        
        # Ajuster les émotions en fonction des données d'équipe réelles
        if team_data:
            # Analyser la forme récente
            if 'form' in team_data:
                try:
                    form_data = team_data['form']
                    if 'result' in form_data:
                        results = form_data['result']
                        if isinstance(results, dict):
                            # Compter les victoires, défaites et nuls récents
                            wins = sum(1 for r in results.values() if r == 'W')
                            draws = sum(1 for r in results.values() if r == 'D')
                            losses = sum(1 for r in results.values() if r == 'L')
                            
                            total_matches = wins + draws + losses
                            if total_matches > 0:
                                # Ajuster l'émotion en fonction des résultats récents
                                if wins / total_matches > 0.7:
                                    primary_emotion = 'euphoria' if wins / total_matches > 0.85 else 'confidence'
                                    secondary_emotion = 'confidence' if primary_emotion == 'euphoria' else 'anticipation'
                                elif losses / total_matches > 0.7:
                                    primary_emotion = 'desperation' if losses / total_matches > 0.85 else 'disappointment'
                                    secondary_emotion = 'anger' if primary_emotion == 'desperation' else 'anxiety'
                                elif draws / total_matches > 0.5:
                                    primary_emotion = 'skepticism'
                                    secondary_emotion = 'anxiety'
                except Exception as e:
                    logger.error(f"Erreur lors de l'analyse des données de forme: {e}")
            
            # Analyser les joueurs populaires
            if 'popular_players' in team_data and team_data['popular_players']:
                # Si un joueur très populaire est présent, l'admiration peut être une émotion clé
                most_popular = max(team_data['popular_players'], key=lambda p: p.get('popularity_score', 0))
                if most_popular.get('popularity_score', 0) > 8.5:
                    if primary_emotion not in ['euphoria', 'confidence']:  # Ne pas remplacer des émotions très positives
                        secondary_emotion = primary_emotion
                        primary_emotion = 'admiration'
            
            # Analyser le manager
            if 'manager' in team_data:
                manager = team_data['manager']
                # Si le manager est nouveau, l'anticipation peut être plus forte
                if manager.get('tenure_days', 999) < 90:
                    if primary_emotion not in ['euphoria', 'confidence', 'admiration']:
                        secondary_emotion = primary_emotion
                        primary_emotion = 'anticipation'
        
        # Générer des données pour chaque source
        for source, config in self.sentiment_sources.items():
            source_data = {}
            
            # Pour chaque métrique de la source
            for metric in config['metrics']:
                # Générer une valeur de base
                base_value = random.uniform(0.3, 0.7)
                
                # Ajuster en fonction de l'émotion primaire
                if primary_emotion in ['euphoria', 'confidence', 'anticipation', 'unity', 'admiration']:
                    # Émotions positives
                    if metric in ['sentiment_ratio', 'emotional_intensity', 'consensus_level']:
                        base_value = random.uniform(0.65, 0.85)
                elif primary_emotion in ['desperation', 'anger', 'disappointment']:
                    # Émotions négatives
                    if metric in ['sentiment_ratio']:
                        base_value = random.uniform(0.15, 0.35)
                    if metric in ['emotional_intensity']:
                        base_value = random.uniform(0.7, 0.9)  # Les émotions négatives peuvent être intenses
                
                source_data[metric] = base_value
            
            # Ajouter des données spécifiques selon la source
            if source == 'social_media':
                source_data['primary_emotion'] = primary_emotion
                source_data['secondary_emotion'] = secondary_emotion
                
                if 'popular_players' in team_data and team_data['popular_players']:
                    # Ajouter les joueurs les plus mentionnés
                    top_players = sorted(team_data['popular_players'], 
                                        key=lambda p: p.get('popularity_score', 0), 
                                        reverse=True)[:3]
                    source_data['top_mentioned_players'] = [
                        {'name': p.get('name', 'Unknown'), 
                         'mention_volume': random.uniform(0.5, 1.0) * p.get('popularity_score', 5) / 10}
                        for p in top_players
                    ]
            
            elif source == 'attendance_patterns':
                # Utiliser des données réelles si disponibles
                if 'transfermarkt' in team_data:
                    try:
                        stadium_capacity = team_data['transfermarkt'].get('stadium', {}).get('capacity', 40000)
                        source_data['stadium_capacity'] = stadium_capacity
                        source_data['attendance_percentage'] = random.uniform(0.7, 0.95)
                        source_data['average_attendance'] = int(source_data['attendance_percentage'] * stadium_capacity)
                    except:
                        pass
            
            sentiment_data[source] = source_data
        
        # Générer des données pour les sources textuelles
        for source, config in self.text_sources.items():
            source_data = {}
            
            # Pour chaque métrique de la source
            for metric in config['metrics']:
                # Générer une valeur de base
                base_value = random.uniform(0.3, 0.7)
                
                # Ajuster selon la source et l'émotion
                source_data[metric] = base_value
            
            # Ajouter des données spécifiques selon la source
            if source == 'manager_statements' and 'manager' in team_data:
                manager = team_data['manager']
                source_data['manager_name'] = manager.get('name', 'Unknown')
                source_data['primary_tone'] = (
                    'confident' if primary_emotion in ['confidence', 'euphoria'] else
                    'cautious' if primary_emotion in ['anxiety', 'skepticism'] else
                    'defensive' if primary_emotion in ['anger', 'disappointment'] else
                    'inspiring'
                )
            
            sentiment_data[source] = source_data
        
        return sentiment_data
    
    def _analyze_sentiment_source_enhanced(self, source, source_data, source_config, team_name, team_data=None):
        """
        Analyse avancée d'une source de sentiment avec données enrichies.
        
        Args:
            source (str): Nom de la source
            source_data (dict): Données de sentiment pour cette source
            source_config (dict): Configuration de la source
            team_name (str): Nom de l'équipe
            team_data (dict, optional): Données enrichies de l'équipe
            
        Returns:
            dict: Analyse de la source de sentiment
        """
        # Base de l'analyse
        analysis = {
            'source': source,
            'overall_sentiment': 0.5,  # Neutre par défaut
            'emotional_distribution': {},
            'dominant_emotion': None,
            'metrics_analysis': {}
        }
        
        # Si aucune donnée, retourner une analyse vide
        if not source_data:
            return analysis
        
        # Analyser les métriques
        for metric, value in source_data.items():
            if metric in source_config.get('metrics', []):
                analysis['metrics_analysis'][metric] = value
        
        # Calculer le sentiment global en fonction des métriques disponibles
        if 'sentiment_ratio' in analysis['metrics_analysis']:
            analysis['overall_sentiment'] = analysis['metrics_analysis']['sentiment_ratio']
        elif 'tone' in analysis['metrics_analysis']:
            analysis['overall_sentiment'] = analysis['metrics_analysis']['tone']
        
        # Déterminer l'émotion dominante
        if 'primary_emotion' in source_data:
            analysis['dominant_emotion'] = source_data['primary_emotion']
        else:
            # Attribuer une émotion basée sur le sentiment global
            if analysis['overall_sentiment'] > 0.7:
                analysis['dominant_emotion'] = 'euphoria' if analysis['overall_sentiment'] > 0.85 else 'confidence'
            elif analysis['overall_sentiment'] < 0.3:
                analysis['dominant_emotion'] = 'desperation' if analysis['overall_sentiment'] < 0.15 else 'disappointment'
            else:
                # Sentiment modéré
                emotions_for_moderate = ['anticipation', 'anxiety', 'nostalgia', 'skepticism']
                analysis['dominant_emotion'] = random.choice(emotions_for_moderate)
        
        # Générer une distribution des émotions
        if 'secondary_emotion' in source_data:
            secondary_emotion = source_data['secondary_emotion']
        else:
            # Choisir une émotion secondaire différente de la principale
            emotions = [e for e in self.collective_emotions if e != analysis['dominant_emotion']]
            secondary_emotion = random.choice(emotions)
        
        # Distribution
        total = 0.0
        emotions_dist = {}
        
        # L'émotion dominante a la part la plus importante
        emotions_dist[analysis['dominant_emotion']] = random.uniform(0.4, 0.6)
        total += emotions_dist[analysis['dominant_emotion']]
        
        # L'émotion secondaire a la deuxième plus grande part
        emotions_dist[secondary_emotion] = random.uniform(0.15, 0.3)
        total += emotions_dist[secondary_emotion]
        
        # Distribuer le reste parmi les autres émotions
        remaining = 1.0 - total
        other_emotions = [e for e in self.collective_emotions 
                        if e != analysis['dominant_emotion'] and e != secondary_emotion]
        
        if other_emotions:
            # Distribuer aléatoirement le reste
            for emotion in other_emotions:
                if remaining <= 0:
                    emotions_dist[emotion] = 0.0
                    continue
                
                share = random.uniform(0, remaining)
                emotions_dist[emotion] = share
                remaining -= share
        
        analysis['emotional_distribution'] = emotions_dist
        
        # Enrichir l'analyse avec des données spécifiques à la source
        if source == 'social_media' and 'top_mentioned_players' in source_data:
            analysis['key_influencers'] = source_data['top_mentioned_players']
        
        if source == 'attendance_patterns' and team_data and 'transfermarkt' in team_data:
            # Ajouter des informations sur le stade
            try:
                stadium_info = team_data['transfermarkt'].get('stadium', {})
                if stadium_info:
                    analysis['stadium_info'] = {
                        'name': stadium_info.get('name', 'Unknown'),
                        'capacity': stadium_info.get('capacity', 0),
                        'average_attendance': source_data.get('average_attendance', 0),
                        'attendance_percentage': source_data.get('attendance_percentage', 0.0)
                    }
            except Exception:
                pass
        
        return analysis
    
    def _calculate_dominant_emotion_enhanced(self, source_analyses, team_data=None):
        """
        Calcule l'émotion dominante globale en intégrant les données enrichies.
        
        Args:
            source_analyses (dict): Analyses des différentes sources
            team_data (dict, optional): Données enrichies de l'équipe
            
        Returns:
            tuple: (émotion dominante, scores d'émotions)
        """
        # Agréger les distributions émotionnelles de toutes les sources
        emotion_scores = defaultdict(float)
        total_weight = 0.0
        
        for source, analysis in source_analyses.items():
            # Déterminer le poids de la source
            source_weight = 0.0
            if source in self.sentiment_sources:
                source_weight = self.sentiment_sources[source]['weight']
            elif source in self.text_sources:
                source_weight = self.text_sources[source]['weight']
            else:
                source_weight = 0.1  # Valeur par défaut
            
            # Ajouter les scores d'émotions pondérés
            for emotion, score in analysis.get('emotional_distribution', {}).items():
                emotion_scores[emotion] += score * source_weight
            
            total_weight += source_weight
        
        # Normaliser les scores
        if total_weight > 0:
            for emotion in emotion_scores:
                emotion_scores[emotion] /= total_weight
        
        # Bonus pour les émotions liées à des facteurs clés
        if team_data:
            # Bonus pour l'admiration si joueurs populaires
            if 'popular_players' in team_data and team_data['popular_players']:
                top_player = max(team_data['popular_players'], key=lambda p: p.get('popularity_score', 0))
                if top_player.get('popularity_score', 0) > 8:
                    emotion_scores['admiration'] = emotion_scores.get('admiration', 0) + 0.1
            
            # Bonus pour l'anticipation si nouveau manager
            if 'manager' in team_data and team_data['manager'].get('tenure_days', 999) < 60:
                emotion_scores['anticipation'] = emotion_scores.get('anticipation', 0) + 0.1
            
            # Bonus pour la nostalgie pour les clubs historiques
            if 'transfermarkt' in team_data and team_data['transfermarkt'].get('founded', 2000) < 1930:
                emotion_scores['nostalgia'] = emotion_scores.get('nostalgia', 0) + 0.05
        
        # Trouver l'émotion avec le score le plus élevé
        if emotion_scores:
            dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
        else:
            dominant_emotion = 'anticipation'  # Valeur par défaut
        
        return dominant_emotion, dict(emotion_scores)
    
    def _analyze_key_influence_factors(self, team_name, team_data):
        """
        Analyse les facteurs clés qui influencent le sentiment des supporters.
        
        Args:
            team_name (str): Nom de l'équipe
            team_data (dict): Données enrichies de l'équipe
            
        Returns:
            list: Facteurs d'influence clés
        """
        influence_factors = []
        
        # Analyser les joueurs clés/populaires
        if 'popular_players' in team_data and team_data['popular_players']:
            top_player = max(team_data['popular_players'], key=lambda p: p.get('popularity_score', 0))
            
            if top_player.get('popularity_score', 0) > 7.5:
                influence_factors.append({
                    'factor_type': 'key_player',
                    'name': top_player.get('name', 'Unknown'),
                    'description': f"Joueur phare avec une grande influence sur les supporters",
                    'impact_score': min(0.9, top_player.get('popularity_score', 7) / 10),
                    'factor_data': {
                        'player': top_player,
                        'type': 'popular_player'
                    }
                })
        
        # Analyser le manager
        if 'manager' in team_data:
            manager = team_data['manager']
            manager_tenure = manager.get('tenure_days', 0)
            
            if manager_tenure < 90:
                influence_factors.append({
                    'factor_type': 'manager',
                    'name': manager.get('name', 'Unknown'),
                    'description': f"Nouveau manager encore en phase d'évaluation par les supporters",
                    'impact_score': 0.7,
                    'factor_data': {
                        'manager': manager,
                        'type': 'new_manager'
                    }
                })
            elif manager.get('win_percentage', 0) > 65:
                influence_factors.append({
                    'factor_type': 'manager',
                    'name': manager.get('name', 'Unknown'),
                    'description': f"Manager respecté avec un excellent bilan",
                    'impact_score': 0.8,
                    'factor_data': {
                        'manager': manager,
                        'type': 'successful_manager'
                    }
                })
        
        # Analyser la forme récente
        if 'form' in team_data:
            try:
                form_data = team_data['form']
                if 'result' in form_data:
                    results = form_data['result']
                    if isinstance(results, dict):
                        # Compter les derniers résultats
                        recent_results = list(results.values())[-5:] if len(results) > 5 else list(results.values())
                        wins = recent_results.count('W')
                        losses = recent_results.count('L')
                        
                        if len(recent_results) >= 3:
                            if wins / len(recent_results) >= 0.8:
                                influence_factors.append({
                                    'factor_type': 'recent_form',
                                    'description': f"Excellente forme récente ({wins} victoires sur {len(recent_results)} matches)",
                                    'impact_score': 0.8,
                                    'factor_data': {
                                        'form_data': form_data,
                                        'type': 'excellent_form'
                                    }
                                })
                            elif losses / len(recent_results) >= 0.8:
                                influence_factors.append({
                                    'factor_type': 'recent_form',
                                    'description': f"Mauvaise forme récente ({losses} défaites sur {len(recent_results)} matches)",
                                    'impact_score': 0.75,
                                    'factor_data': {
                                        'form_data': form_data,
                                        'type': 'poor_form'
                                    }
                                })
            except Exception as e:
                logger.error(f"Erreur lors de l'analyse de la forme récente: {e}")
        
        # Analyser l'histoire/tradition du club
        if 'transfermarkt' in team_data:
            try:
                founding_year = team_data['transfermarkt'].get('founded', 2000)
                if founding_year < 1930:
                    influence_factors.append({
                        'factor_type': 'club_tradition',
                        'description': f"Club historique avec une longue tradition (fondé en {founding_year})",
                        'impact_score': 0.65,
                        'factor_data': {
                            'founded': founding_year,
                            'type': 'historical_club'
                        }
                    })
            except Exception:
                pass
        
        return influence_factors
    
    def _calculate_base_sentiment_impact_enhanced(self, current_sentiment, match_importance, is_home, team_data=None):
        """
        Calcule l'impact de base du sentiment sur la performance avec données enrichies.
        
        Args:
            current_sentiment (dict): Analyse du sentiment actuel
            match_importance (float): Importance du match
            is_home (bool): Si l'équipe joue à domicile
            team_data (dict, optional): Données enrichies de l'équipe
            
        Returns:
            dict: Impact de base du sentiment
        """
        # Base de l'impact
        base_impact = {
            'raw_impact': 0.0,
            'components': {}
        }
        
        # Extraire les caractéristiques du sentiment
        dominant_emotion = current_sentiment.get('dominant_emotion', 'neutral')
        overall_intensity = current_sentiment.get('overall_intensity', 0.5)
        cohesion = current_sentiment.get('sentiment_cohesion', {}).get('overall_cohesion', 0.5)
        
        # 1. Impact de l'émotion dominante
        emotion_impact = 0.0
        if dominant_emotion in ['euphoria', 'confidence', 'unity', 'anticipation', 'admiration']:
            # Émotions positives
            emotion_impact = random.uniform(0.3, 0.5)
        elif dominant_emotion in ['anxiety', 'skepticism']:
            # Émotions neutres-négatives
            emotion_impact = random.uniform(-0.2, 0.1)
        elif dominant_emotion in ['desperation', 'anger', 'disappointment']:
            # Émotions négatives
            emotion_impact = random.uniform(-0.5, -0.2)
        elif dominant_emotion in ['nostalgia']:
            # Émotions variables
            emotion_impact = random.uniform(-0.1, 0.3)
        
        base_impact['components']['emotion'] = emotion_impact
        
        # 2. Moduler par l'intensité
        intensity_modulation = overall_intensity * self.sentiment_parameters['emotional_impact']
        base_impact['components']['intensity'] = intensity_modulation
        
        # 3. Facteur d'avantage à domicile
        home_factor = 0.0
        if is_home:
            home_factor = self.sentiment_parameters['home_advantage_factor']
            
            # Augmenter le facteur domicile pour les clubs avec forte présence de supporters
            if team_data and 'transfermarkt' in team_data:
                try:
                    stadium_capacity = team_data['transfermarkt'].get('stadium', {}).get('capacity', 30000)
                    if stadium_capacity > 50000:
                        home_factor += 0.1
                    elif stadium_capacity > 30000:
                        home_factor += 0.05
                except Exception:
                    pass
        
        base_impact['components']['home_factor'] = home_factor
        
        # 4. Facteur d'importance du match
        importance_factor = match_importance * 0.3
        base_impact['components']['importance'] = importance_factor
        
        # 5. Facteur de cohésion du sentiment
        cohesion_factor = cohesion * 0.2
        base_impact['components']['cohesion'] = cohesion_factor
        
        # Calculer l'impact brut
        raw_impact = (
            emotion_impact * intensity_modulation + 
            home_factor + 
            importance_factor * cohesion_factor
        )
        
        # Limiter l'impact entre -1 et 1
        raw_impact = max(-1.0, min(1.0, raw_impact))
        base_impact['raw_impact'] = raw_impact
        
        return base_impact
    
    def _analyze_rivalry(self, team_name, opponent_name, team_data):
        """
        Analyse la rivalité entre deux équipes.
        
        Args:
            team_name (str): Nom de l'équipe
            opponent_name (str): Nom de l'adversaire
            team_data (dict): Données enrichies de l'équipe
            
        Returns:
            float: Intensité de la rivalité (0 à 1)
        """
        # Valeur par défaut modérée
        rivalry_intensity = 0.3
        
        # Si nous avons des données de confrontations directes, les utiliser
        if 'form' in team_data:
            try:
                form_data = team_data['form']
                if 'opponent' in form_data:
                    opponents = form_data['opponent']
                    # Compter combien de fois ces équipes se sont affrontées récemment
                    recent_matches = sum(1 for opp in opponents.values() if opp == opponent_name)
                    
                    if recent_matches >= 2:
                        # Augmenter l'intensité de la rivalité en fonction du nombre de rencontres
                        rivalry_intensity += min(0.3, recent_matches * 0.1)
            except Exception as e:
                logger.error(f"Erreur lors de l'analyse des confrontations: {e}")
        
        # Vérifier si les équipes sont de la même région (simulation)
        is_local_derby = random.random() < 0.2  # 20% de chance que ce soit un derby local
        if is_local_derby:
            rivalry_intensity += 0.3
        
        # Limiter l'intensité entre 0 et 1
        return min(1.0, rivalry_intensity)
    
    def _calculate_match_importance_enhanced(self, match_data, team_name, opponent_name):
        """
        Calcule l'importance d'un match en utilisant des données enrichies.
        
        Args:
            match_data (dict): Données du match
            team_name (str): Nom de l'équipe
            opponent_name (str): Nom de l'adversaire
            
        Returns:
            float: Importance du match (0 à 1)
        """
        # Valeur de base modérée
        importance = 0.5
        
        # Vérifier le type de compétition
        competition = match_data.get('competition', 'league')
        
        # Ajuster selon la compétition
        if competition == 'cup':
            importance += 0.2
        elif competition == 'continental':
            importance += 0.3
        elif competition == 'playoff':
            importance += 0.4
        
        # Vérifier si c'est un derby ou un match contre un rival traditionnel
        is_derby = match_data.get('is_derby', False)
        if is_derby:
            importance += 0.2
        
        # Vérifier s'il s'agit d'un match important pour le classement
        league_position_impact = match_data.get('league_position_impact', 0.0)
        importance += league_position_impact * 0.2
        
        # Vérifier la phase de la compétition
        competition_stage = match_data.get('competition_stage', 'regular')
        if competition_stage == 'final':
            importance = 1.0  # Importance maximale pour une finale
        elif competition_stage == 'semifinal':
            importance += 0.3
        elif competition_stage == 'quarterfinal':
            importance += 0.2
        
        # Limiter l'importance entre 0 et 1
        return min(1.0, importance)
    
    def _analyze_form_data(self, form_data):
        """
        Analyse les données de forme pour déterminer un facteur de forme.
        
        Args:
            form_data (dict): Données de forme
            
        Returns:
            float: Facteur de forme (0 à 1)
        """
        # Valeur par défaut neutre
        form_factor = 0.5
        
        try:
            if 'result' in form_data:
                results = form_data['result']
                if isinstance(results, dict):
                    # Compter les derniers résultats
                    recent_results = list(results.values())[-5:] if len(results) > 5 else list(results.values())
                    wins = recent_results.count('W')
                    draws = recent_results.count('D')
                    losses = recent_results.count('L')
                    
                    if len(recent_results) > 0:
                        # Calculer un score basé sur les points (3 pour victoire, 1 pour nul, 0 pour défaite)
                        points = wins * 3 + draws
                        max_points = len(recent_results) * 3
                        
                        if max_points > 0:
                            form_factor = 0.1 + (points / max_points) * 0.9  # Échelle de 0.1 à 1.0
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse des données de forme: {e}")
        
        return form_factor
    
    def _determine_impact_type_enhanced(self, impact_value):
        """
        Détermine le type d'impact du sentiment sur la performance.
        
        Args:
            impact_value (float): Valeur d'impact calculée
            
        Returns:
            str: Type d'impact
        """
        if impact_value > 0.6:
            return 'major_boost'
        elif impact_value > 0.3:
            return 'significant_boost'
        elif impact_value > 0.1:
            return 'moderate_boost'
        elif impact_value > -0.1:
            return 'neutral'
        elif impact_value > -0.3:
            return 'moderate_hindrance'
        elif impact_value > -0.6:
            return 'significant_hindrance'
        else:
            return 'major_hindrance'
    
    def _analyze_text_source(self, source, source_data, source_config, team_name):
        """
        Analyse une source de données textuelles.
        
        Args:
            source (str): Nom de la source
            source_data (dict): Données textuelles
            source_config (dict): Configuration de la source
            team_name (str): Nom de l'équipe
            
        Returns:
            dict: Analyse de la source textuelle
        """
        # Base de l'analyse
        analysis = {
            'source': source,
            'overall_sentiment': 0.5,  # Neutre par défaut
            'emotional_distribution': {},
            'metrics_analysis': {}
        }
        
        # Si aucune donnée, retourner une analyse vide
        if not source_data:
            return analysis
        
        # Analyser les métriques
        for metric, value in source_data.items():
            if metric in source_config.get('metrics', []):
                analysis['metrics_analysis'][metric] = value
        
        # Calculer le sentiment global
        sentiment_metrics = ['tone', 'fan_expectations_management', 'transparency']
        sentiment_values = [source_data.get(metric, 0.5) for metric in sentiment_metrics if metric in source_data]
        
        if sentiment_values:
            analysis['overall_sentiment'] = sum(sentiment_values) / len(sentiment_values)
        
        # Déterminer l'émotion dominante basée sur le ton et le contexte
        if 'primary_tone' in source_data:
            primary_tone = source_data['primary_tone']
            
            # Associer le ton à une émotion
            tone_emotion_map = {
                'confident': 'confidence',
                'cautious': 'anxiety',
                'defensive': 'anger',
                'inspiring': 'anticipation',
                'sentimental': 'nostalgia',
                'apologetic': 'disappointment'
            }
            
            dominant_emotion = tone_emotion_map.get(primary_tone, 'neutral')
        else:
            # Déterminer l'émotion basée sur le sentiment global
            if analysis['overall_sentiment'] > 0.7:
                dominant_emotion = 'confidence'
            elif analysis['overall_sentiment'] < 0.3:
                dominant_emotion = 'anxiety'
            else:
                dominant_emotion = 'anticipation'
        
        analysis['dominant_emotion'] = dominant_emotion
        
        # Générer une distribution d'émotions
        emotions_dist = {}
        emotions_dist[dominant_emotion] = random.uniform(0.4, 0.6)
        
        # Ajouter quelques émotions secondaires
        secondary_emotions = [e for e in self.collective_emotions if e != dominant_emotion]
        for _ in range(min(3, len(secondary_emotions))):
            emotion = random.choice(secondary_emotions)
            emotions_dist[emotion] = random.uniform(0.05, 0.2)
            secondary_emotions.remove(emotion)
        
        # Normaliser la distribution
        total = sum(emotions_dist.values())
        for emotion in emotions_dist:
            emotions_dist[emotion] /= total
        
        analysis['emotional_distribution'] = emotions_dist
        
        return analysis
    
    # Méthodes simulées pour d'autres fonctionnalités - implémentations simplifiées
    
    def _analyze_sentiment_trends_enhanced(self, team_name, team_data=None):
        """Analyse les tendances sentimentales avec données enrichies"""
        return {
            'trend_direction': random.choice(['improving', 'stable', 'declining']),
            'volatility': random.uniform(0.1, 0.7),
            'consistency': random.uniform(0.3, 0.8),
            'recent_pattern': random.choice(['cyclical', 'steady', 'erratic'])
        }
    
    def _evaluate_sentiment_cohesion_enhanced(self, source_analyses):
        """Évalue la cohésion du sentiment avec données enrichies"""
        cohesion_values = []
        
        for source, analysis in source_analyses.items():
            # Calculer une mesure de la concentration des émotions
            emotions = analysis.get('emotional_distribution', {})
            if emotions:
                # Plus une émotion est dominante, plus la cohésion est élevée
                max_emotion_score = max(emotions.values()) if emotions else 0.5
                cohesion_values.append(max_emotion_score)
        
        # Calculer la cohésion moyenne
        overall_cohesion = sum(cohesion_values) / len(cohesion_values) if cohesion_values else 0.5
        
        return {
            'overall_cohesion': overall_cohesion,
            'source_consistency': random.uniform(0.4, 0.9),
            'cross_source_alignment': random.uniform(0.3, 0.8)
        }
    
    def _calculate_overall_intensity_enhanced(self, source_analyses, team_data=None):
        """Calcule l'intensité globale du sentiment avec données enrichies"""
        intensity_values = []
        
        for source, analysis in source_analyses.items():
            # Utiliser l'intensité émotionnelle si disponible
            if 'emotional_intensity' in analysis.get('metrics_analysis', {}):
                intensity_values.append(analysis['metrics_analysis']['emotional_intensity'])
            # Sinon, estimer à partir de la distribution des émotions
            elif 'emotional_distribution' in analysis:
                # Plus le score de l'émotion dominante est élevé, plus l'intensité est forte
                max_emotion_score = max(analysis['emotional_distribution'].values()) if analysis['emotional_distribution'] else 0.5
                intensity_values.append(max_emotion_score)
        
        # Calculer l'intensité moyenne
        overall_intensity = sum(intensity_values) / len(intensity_values) if intensity_values else 0.5
        
        # Ajuster en fonction de facteurs spécifiques
        if team_data:
            # Intensité plus forte pour les derbys ou matches importants
            if 'form' in team_data and 'is_derby' in team_data.get('additional_data', {}):
                overall_intensity += 0.1
            
            # Intensité plus forte pour les clubs avec une grande base de supporters
            if 'transfermarkt' in team_data:
                try:
                    stadium_capacity = team_data['transfermarkt'].get('stadium', {}).get('capacity', 30000)
                    if stadium_capacity > 50000:
                        overall_intensity += 0.05
                except Exception:
                    pass
        
        # Limiter entre 0 et 1
        return min(1.0, overall_intensity)
    
    def _analyze_match_influence_enhanced(self, match_context, dominant_emotion, overall_intensity, team_data=None):
        """Analyse l'influence du contexte du match sur le sentiment avec données enrichies"""
        return {
            'contextual_amplification': random.uniform(0.5, 1.2),
            'expected_atmosphere': (
                'electric' if overall_intensity > 0.8 else
                'energetic' if overall_intensity > 0.6 else
                'supportive' if overall_intensity > 0.4 else
                'subdued'
            ),
            'emotional_volatility_risk': random.uniform(0.2, 0.8)
        }
    
    def _calculate_expected_impact_enhanced(self, dominant_emotion, overall_intensity, sentiment_cohesion, match_context, team_data=None):
        """Calcule l'impact attendu du sentiment sur la performance avec données enrichies"""
        base_impact = 0.0
        
        # Impact selon l'émotion dominante
        if dominant_emotion in ['euphoria', 'confidence', 'unity', 'admiration']:
            base_impact = random.uniform(0.3, 0.6)
        elif dominant_emotion in ['anxiety', 'skepticism']:
            base_impact = random.uniform(-0.3, 0.2)
        elif dominant_emotion in ['anger', 'desperation', 'disappointment']:
            base_impact = random.uniform(-0.6, -0.1)
        elif dominant_emotion in ['anticipation', 'nostalgia']:
            base_impact = random.uniform(-0.2, 0.4)
        
        # Moduler par l'intensité et la cohésion
        modulated_impact = base_impact * overall_intensity * sentiment_cohesion.get('overall_cohesion', 0.5)
        
        # Ajuster pour les matches à domicile
        if match_context and match_context.get('is_home', False):
            home_factor = self.sentiment_parameters['home_advantage_factor']
            modulated_impact += home_factor
        
        # Limiter entre -1 et 1
        modulated_impact = max(-1.0, min(1.0, modulated_impact))
        
        return {
            'expected_performance_impact': modulated_impact,
            'primary_factor': dominant_emotion,
            'confidence': random.uniform(0.6, 0.9),
            'impact_areas': [
                {'area': 'team_morale', 'magnitude': random.uniform(0.3, 0.9)},
                {'area': 'fan_support_during_match', 'magnitude': random.uniform(0.4, 0.9)},
                {'area': 'player_confidence', 'magnitude': random.uniform(0.3, 0.8)}
            ]
        }
    
    def _analyze_specific_factors_enhanced(self, team_name, opponent_name, match_data, team_data=None):
        """Analyse les facteurs spécifiques qui influencent le sentiment avec données enrichies"""
        specific_factors = []
        
        # Vérifier s'il s'agit d'un derby
        is_derby = match_data.get('is_derby', False)
        if is_derby:
            specific_factors.append({
                'factor_type': 'derby',
                'description': f"Derby local contre {opponent_name}",
                'impact_value': random.uniform(0.2, 0.4),
                'confidence': 0.9
            })
        
        # Vérifier s'il s'agit d'un match important pour le classement
        if 'league_position_impact' in match_data and match_data['league_position_impact'] > 0.6:
            specific_factors.append({
                'factor_type': 'standings_impact',
                'description': f"Match crucial pour le classement",
                'impact_value': match_data['league_position_impact'] * 0.3,
                'confidence': 0.8
            })
        
        # Vérifier s'il y a des joueurs clés contre leurs anciens clubs
        if team_data and 'players' in team_data:
            for player in team_data['players']:
                previous_club = player.get('previous_club', '')
                if previous_club and previous_club == opponent_name:
                    specific_factors.append({
                        'factor_type': 'player_facing_former_club',
                        'description': f"{player.get('name', 'Joueur')} affronte son ancien club",
                        'impact_value': random.uniform(0.1, 0.25),
                        'confidence': 0.7
                    })
        
        # Vérifier la phase de la compétition
        competition_stage = match_data.get('competition_stage', 'regular')
        if competition_stage in ['final', 'semifinal', 'quarterfinal']:
            specific_factors.append({
                'factor_type': 'competition_stage',
                'description': f"Phase avancée de la compétition ({competition_stage})",
                'impact_value': 0.3 if competition_stage == 'final' else 0.2,
                'confidence': 0.85
            })
        
        return specific_factors
    
    def _generate_impact_scenarios_enhanced(self, adjusted_impact, form_factor, team_data=None):
        """Génère des scénarios d'impact potentiels avec données enrichies"""
        impact_value = adjusted_impact.get('total_impact', 0.0)
        
        # Scénarios de base
        scenarios = [
            {
                'scenario': 'best_case',
                'impact_value': min(1.0, impact_value + 0.2),
                'probability': random.uniform(0.1, 0.3),
                'description': "Sentiment servant de catalyseur majeur pour la performance"
            },
            {
                'scenario': 'expected',
                'impact_value': impact_value,
                'probability': random.uniform(0.4, 0.6),
                'description': "Impact attendu du sentiment sur la performance"
            },
            {
                'scenario': 'worst_case',
                'impact_value': max(-1.0, impact_value - 0.2),
                'probability': random.uniform(0.1, 0.3),
                'description': "Sentiment ayant un effet négatif inattendu ou neutralisé"
            }
        ]
        
        # Ajuster les probabilités pour qu'elles somment à 1
        total_prob = sum(s['probability'] for s in scenarios)
        for scenario in scenarios:
            scenario['probability'] /= total_prob
        
        return scenarios
    
    def _calculate_performance_influence_enhanced(self, adjusted_impact, current_sentiment, form_factor, team_data=None):
        """Calcule l'influence du sentiment sur différents aspects de la performance avec données enrichies"""
        impact_value = adjusted_impact.get('total_impact', 0.0)
        
        # Impact sur différentes facettes du jeu
        facet_impacts = {}
        
        # Facteur offensif
        offensive_impact = impact_value * random.uniform(0.8, 1.2)
        # Facteur défensif
        defensive_impact = impact_value * random.uniform(0.7, 1.1)
        # Facteur mental
        mental_impact = impact_value * random.uniform(0.9, 1.3)
        # Facteur d'intensité
        intensity_impact = impact_value * random.uniform(0.8, 1.2)
        
        # Limiter tous les impacts entre -1 et 1
        facet_impacts['offensive'] = max(-1.0, min(1.0, offensive_impact))
        facet_impacts['defensive'] = max(-1.0, min(1.0, defensive_impact))
        facet_impacts['mental'] = max(-1.0, min(1.0, mental_impact))
        facet_impacts['intensity'] = max(-1.0, min(1.0, intensity_impact))
        
        # Résumé d'impact global
        impact_summary = (
            "Catalyseur Majeur" if impact_value > 0.6 else
            "Influence Positive" if impact_value > 0.2 else
            "Léger Avantage" if impact_value > 0 else
            "Impact Neutre" if impact_value > -0.2 else
            "Handicap Mineur" if impact_value > -0.6 else
            "Obstacle Significatif"
        )
        
        # Domaines d'influence spécifiques
        influence_areas = []
        
        # Impact sur les joueurs clés
        if team_data and 'key_players' in team_data:
            for i, player in enumerate(team_data['key_players'][:3]):  # Limiter à 3 joueurs max
                influence_areas.append({
                    'area': f"Performance de {player.get('name', 'joueur clé')}",
                    'impact_value': impact_value * random.uniform(0.8, 1.2)
                })
        
        # Impact sur les aspects tactiques
        influence_areas.extend([
            {
                'area': "Pressing et intensité",
                'impact_value': facet_impacts['intensity']
            },
            {
                'area': "Concentration défensive",
                'impact_value': facet_impacts['defensive']
            },
            {
                'area': "Créativité offensive",
                'impact_value': facet_impacts['offensive']
            },
            {
                'area': "Résilience mentale",
                'impact_value': facet_impacts['mental']
            }
        ])
        
        return {
            'impact_summary': impact_summary,
            'facet_impacts': facet_impacts,
            'influence_areas': influence_areas,
            'modulating_factors': [
                {'factor': "Forme récente", 'weight': form_factor},
                {'factor': "Expérience de l'équipe", 'weight': random.uniform(0.5, 0.9)},
                {'factor': "Qualité de l'adversaire", 'weight': random.uniform(0.6, 0.9)}
            ]
        }