"""
FanSentimentMonitor (Version Enrichie) - Module d'analyse de l'influence des émotions collectives.
Cette version améliorée intègre des données réelles provenant de multiples sources 
(Transfermarkt, soccerdata, détails des joueurs et managers) pour une analyse plus précise.
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

# Import de l'adaptateur Transfermarkt (existant)
from api.transfermarkt_integration import (
    is_transfermarkt_available,
    get_team_profile,
    search_club_by_name
)

# Imports de nos NOUVEAUX modules de données avancées
try:
    # Import du hub central d'intégration des données
    from api.data_integration_hub import (
        get_data_integration_hub,
        get_team_details,
        is_source_available
    )
    DATA_HUB_AVAILABLE = True
except ImportError:
    logger.warning("Hub d'intégration de données non disponible, fonctionnalités avancées désactivées")
    DATA_HUB_AVAILABLE = False

# Import du module d'analyse avancée
try:
    from modules.advanced_data_insights import generate_team_insights
    ADVANCED_INSIGHTS_AVAILABLE = True
except ImportError:
    logger.warning("Module d'analyse avancée non disponible, insights avancés désactivés")
    ADVANCED_INSIGHTS_AVAILABLE = False

class FanSentimentMonitorEnhanced:
    """
    FanSentimentMonitor (Version Enrichie) - Système d'analyse de l'influence des émotions collectives des supporters.
    Cette version enrichie utilise des données réelles provenant de toutes les sources disponibles pour 
    offrir une analyse plus précise de l'impact du sentiment des supporters sur les performances.
    """
    
    def __init__(self):
        """Initialise le module FanSentimentMonitor enrichi avec accès à toutes les sources de données"""
        # Vérifier la disponibilité du hub d'intégration de données
        self.use_data_hub = DATA_HUB_AVAILABLE
        self.use_advanced_insights = ADVANCED_INSIGHTS_AVAILABLE
        
        if self.use_data_hub:
            try:
                self.data_hub = get_data_integration_hub()
                available_sources = self.data_hub.get_available_sources()
                logger.info(f"Hub d'intégration de données disponible pour FanSentimentMonitor. Sources: {available_sources}")
            except Exception as e:
                logger.error(f"Erreur lors de l'initialisation du hub d'intégration: {e}")
                self.use_data_hub = False
        
        # Paramètres d'analyse
        self.sentiment_parameters = {
            'emotional_impact': 0.3,       # Impact des émotions sur la performance
            'collective_resonance': 0.65,  # Force de la résonance collective
            'threshold_critical_mass': 0.7, # Seuil pour atteindre la masse critique
            'home_advantage_factor': 0.25,  # Facteur d'avantage à domicile supplémentaire
            'temporal_decay': 0.85,         # Décroissance temporelle du sentiment
            'social_media_weight': 0.35,    # Poids des réseaux sociaux (ajusté)
            'real_data_bonus': 0.15         # Bonus pour les données réelles
        }
        
        # Types d'émotions collectives surveillées
        self.collective_emotions = [
            'euphoria',           # Euphorie collective
            'anxiety',            # Anxiété et nervosité
            'anger',              # Colère et frustration
            'confidence',         # Confiance et optimisme
            'desperation',        # Désespoir et résignation
            'nostalgia',          # Nostalgie pour des succès passés
            'anticipation',       # Anticipation et excitation
            'disappointment'      # Déception
        ]
        
        # Sources de données sentimentales
        self.sentiment_sources = {
            'social_media': {
                'weight': 0.4,
                'platforms': ['twitter', 'instagram', 'facebook', 'reddit'],
                'metrics': ['volume', 'sentiment_ratio', 'emotional_intensity', 'virality']
            },
            'forum_discussions': {
                'weight': 0.25,
                'metrics': ['post_volume', 'comment_intensity', 'topic_sentiment', 'consensus_level']
            },
            'news_media': {
                'weight': 0.15,
                'metrics': ['coverage_sentiment', 'headline_tone', 'article_volume', 'narrative_framing']
            },
            'attendance_patterns': {
                'weight': 0.2,
                'metrics': ['attendance_percentage', 'ticket_demand', 'atmosphere_rating', 'chanting_intensity']
            }
        }
        
        # Nouvelles sources de données réelles
        if self.use_data_hub:
            self.real_data_sources = {
                'transfermarkt': {
                    'weight': 0.3,
                    'available': is_transfermarkt_available(),
                    'metrics': ['club_popularity', 'fans_intensity', 'social_media_followers', 'team_reputation']
                },
                'soccerdata': {
                    'weight': 0.25,
                    'available': is_source_available('soccerdata') if self.use_data_hub else False,
                    'metrics': ['fan_attendance', 'social_media_sentiment', 'news_coverage']
                },
                'player_data': {
                    'weight': 0.25,
                    'available': is_source_available('player_enrichment') if self.use_data_hub else False,
                    'metrics': ['star_player_popularity', 'manager_reputation', 'team_chemistry']
                },
                'historical_performance': {
                    'weight': 0.2,
                    'available': True,  # Toujours disponible via des simulations au minimum
                    'metrics': ['recent_results', 'historical_rivalry', 'trophy_history']
                }
            }
        else:
            self.real_data_sources = {}
        
        # Historique des analyses
        self.analysis_history = []
        
        # Cache de sentiment
        self.sentiment_cache = {}
    
    def analyze_current_sentiment(self, team_name, match_data=None, sentiment_data=None):
        """
        Analyser le sentiment actuel des supporters d'une équipe en utilisant toutes les sources disponibles.
        
        Args:
            team_name (str): Nom de l'équipe
            match_data (dict, optional): Données du match à venir
            sentiment_data (dict, optional): Données de sentiment si disponibles
            
        Returns:
            dict: Analyse du sentiment des supporters
        """
        # Si des données de sentiment sont fournies, les utiliser
        # Sinon, vérifier le cache ou générer des données
        if sentiment_data is None:
            cache_key = f"{team_name}_{datetime.now().strftime('%Y-%m-%d')}"
            if cache_key in self.sentiment_cache:
                sentiment_data = self.sentiment_cache[cache_key]
            else:
                sentiment_data = self._generate_enhanced_sentiment_data(team_name)
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
        
        # Analyser chaque source de sentiment traditionnelle
        source_analyses = {}
        for source, source_config in self.sentiment_sources.items():
            source_data = sentiment_data.get(source, {})
            source_analyses[source] = self._analyze_sentiment_source(
                source, source_data, source_config, team_name
            )
        
        # Analyser les nouvelles sources de données réelles si disponibles
        real_data_analyses = {}
        team_details = None
        
        if self.use_data_hub:
            try:
                # Récupérer les détails complets de l'équipe
                team_details = get_team_details(team_name)
                
                # Analyser chaque source de données réelles
                for source, source_config in self.real_data_sources.items():
                    if source_config['available']:
                        if source == 'transfermarkt' and 'transfermarkt_data' in team_details:
                            source_data = team_details['transfermarkt_data']
                        elif source == 'soccerdata' and 'form' in team_details:
                            source_data = team_details['form']
                        elif source == 'player_data' and 'detailed_players' in team_details:
                            source_data = {'players': team_details['detailed_players']}
                            if 'detailed_manager' in team_details:
                                source_data['manager'] = team_details['detailed_manager']
                        elif source == 'historical_performance':
                            # Utiliser les performances historiques disponibles
                            source_data = {'team_name': team_name}
                            if 'form' in team_details:
                                source_data['form'] = team_details['form']
                        else:
                            source_data = {}
                        
                        real_data_analyses[source] = self._analyze_real_data_source(
                            source, source_data, source_config, team_name
                        )
            except Exception as e:
                logger.error(f"Erreur lors de l'analyse des données réelles pour {team_name}: {e}")
        
        # Utiliser les insights avancés si disponibles
        advanced_insights = None
        if self.use_advanced_insights and team_details:
            try:
                advanced_insights = generate_team_insights(team_name)
                logger.info(f"Insights avancés générés pour {team_name}")
            except Exception as e:
                logger.error(f"Erreur lors de la génération d'insights avancés pour {team_name}: {e}")
        
        # Calculer le sentiment dominant en intégrant toutes les sources
        if real_data_analyses:
            # Combiner les analyses traditionnelles et réelles
            combined_analyses = {**source_analyses, **real_data_analyses}
            dominant_emotion, emotion_scores = self._calculate_enhanced_dominant_emotion(
                combined_analyses, real_data_analyses
            )
            
            # Calculer l'intensité globale avec un bonus pour les données réelles
            overall_intensity = self._calculate_enhanced_overall_intensity(
                combined_analyses, real_data_analyses
            )
            
            # Évaluer la cohésion du sentiment avec toutes les sources
            sentiment_cohesion = self._evaluate_enhanced_sentiment_cohesion(
                combined_analyses, real_data_analyses
            )
        else:
            # Utiliser uniquement les analyses traditionnelles
            dominant_emotion, emotion_scores = self._calculate_dominant_emotion(source_analyses)
            overall_intensity = self._calculate_overall_intensity(source_analyses)
            sentiment_cohesion = self._evaluate_sentiment_cohesion(source_analyses)
        
        # Analyser les tendances récentes
        trend_analysis = self._analyze_sentiment_trends(team_name)
        
        # Analyser le contexte du match si disponible
        match_influence = None
        if match_context:
            match_influence = self._analyze_match_influence(
                match_context, dominant_emotion, overall_intensity,
                team_details if self.use_data_hub else None
            )
        
        # Compiler l'analyse complète
        analysis = {
            'team_name': team_name,
            'analysis_timestamp': datetime.now().isoformat(),
            'dominant_emotion': dominant_emotion,
            'emotion_scores': emotion_scores,
            'overall_intensity': overall_intensity,
            'sentiment_cohesion': sentiment_cohesion,
            'source_analyses': source_analyses,
            'trend_analysis': trend_analysis,
            'expected_impact': self._calculate_expected_impact(
                dominant_emotion, overall_intensity, sentiment_cohesion, match_context,
                team_details if self.use_data_hub else None
            ),
            'data_quality': 0.5 + (0.3 if self.use_data_hub else 0)  # Base + bonus pour les données réelles
        }
        
        # Ajouter les analyses de données réelles si disponibles
        if real_data_analyses:
            analysis['real_data_analyses'] = real_data_analyses
        
        # Ajouter les insights avancés si disponibles
        if advanced_insights:
            analysis['advanced_insights'] = advanced_insights
        
        if match_influence:
            analysis['match_influence'] = match_influence
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'enhanced_sentiment_analysis',
            'timestamp': datetime.now().isoformat(),
            'team': team_name,
            'summary': {
                'dominant_emotion': dominant_emotion,
                'intensity': overall_intensity,
                'cohesion': sentiment_cohesion.get('overall_cohesion', 0),
                'data_quality': analysis['data_quality']
            }
        })
        
        return analysis
    
    def predict_sentiment_impact(self, team_name, match_data, recent_form=None):
        """
        Prédire l'impact du sentiment des supporters sur un match à venir,
        en utilisant toutes les sources de données disponibles.
        
        Args:
            team_name (str): Nom de l'équipe
            match_data (dict): Données du match à venir
            recent_form (list, optional): Forme récente de l'équipe
            
        Returns:
            dict: Prédiction de l'impact du sentiment
        """
        # Analyser le sentiment actuel avec méthode enrichie
        current_sentiment = self.analyze_current_sentiment(team_name, match_data)
        
        # Extraire le nom de l'adversaire
        opponent_name = match_data.get('away_team') if match_data.get('home_team') == team_name else match_data.get('home_team')
        
        # Récupérer les détails des équipes si le hub est disponible
        team_details = None
        opponent_details = None
        if self.use_data_hub:
            try:
                team_details = get_team_details(team_name)
                opponent_details = get_team_details(opponent_name)
                
                # Utiliser les données de forme récente si non fournies
                if recent_form is None and 'form' in team_details and isinstance(team_details['form'], dict) and 'data' in team_details['form']:
                    recent_form = team_details['form']['data']
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des détails d'équipe: {e}")
        
        # Calculer l'importance du match
        match_importance = self._calculate_enhanced_match_importance(
            match_data, team_details, opponent_details
        )
        
        # Déterminer si le match est à domicile
        is_home = match_data.get('home_team') == team_name
        
        # Analyser la forme récente si fournie
        form_factor = 0.5  # Valeur neutre par défaut
        if recent_form:
            form_factor = self._analyze_recent_form(recent_form)
        
        # Calculer l'avantage ou désavantage sentimental de base
        base_impact = self._calculate_enhanced_base_sentiment_impact(
            current_sentiment, match_importance, is_home,
            team_details if self.use_data_hub else None
        )
        
        # Ajuster en fonction de facteurs spécifiques au match
        specific_factors = self._analyze_specific_factors(
            team_name, opponent_name, match_data,
            team_details, opponent_details
        )
        
        # Calculer l'impact ajusté
        adjusted_impact = base_impact.copy()
        adjusted_impact['total_impact'] = base_impact['raw_impact']
        
        # Appliquer les ajustements
        for factor in specific_factors:
            adjusted_impact['total_impact'] += factor.get('impact_value', 0)
            adjusted_impact['factors'] = adjusted_impact.get('factors', []) + [factor]
        
        # Limiter l'impact total
        adjusted_impact['total_impact'] = max(-1.0, min(1.0, adjusted_impact['total_impact']))
        
        # Déterminer le type d'impact
        adjusted_impact['impact_type'] = self._determine_impact_type(adjusted_impact['total_impact'])
        
        # Générer des scénarios d'impact potentiels
        impact_scenarios = self._generate_enhanced_impact_scenarios(
            adjusted_impact, form_factor, 
            team_details if self.use_data_hub else None
        )
        
        # Compiler la prédiction complète
        prediction = {
            'team_name': team_name,
            'opponent_name': opponent_name,
            'match_date': match_data.get('date', datetime.now().isoformat()),
            'prediction_timestamp': datetime.now().isoformat(),
            'current_sentiment': {
                'dominant_emotion': current_sentiment.get('dominant_emotion'),
                'overall_intensity': current_sentiment.get('overall_intensity'),
                'cohesion': current_sentiment.get('sentiment_cohesion', {}).get('overall_cohesion', 0)
            },
            'match_importance': match_importance,
            'is_home': is_home,
            'base_impact': base_impact,
            'adjusted_impact': adjusted_impact,
            'impact_scenarios': impact_scenarios,
            'performance_influence': self._calculate_enhanced_performance_influence(
                adjusted_impact, current_sentiment, form_factor,
                team_details if self.use_data_hub else None
            ),
            'data_quality': current_sentiment.get('data_quality', 0.5)
        }
        
        # Ajouter des insights issus des données réelles si disponibles
        if self.use_data_hub and team_details and 'advanced_insights' in current_sentiment:
            prediction['sentiment_insights'] = self._extract_sentiment_insights(
                current_sentiment['advanced_insights']
            )
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'enhanced_sentiment_impact_prediction',
            'timestamp': datetime.now().isoformat(),
            'team': team_name,
            'opponent': opponent_name,
            'match_date': match_data.get('date', datetime.now().isoformat()),
            'summary': {
                'impact_type': adjusted_impact.get('impact_type'),
                'total_impact': adjusted_impact.get('total_impact'),
                'dominant_emotion': current_sentiment.get('dominant_emotion'),
                'data_quality': prediction.get('data_quality', 0.5)
            }
        })
        
        return prediction
    
    def analyze_sentiment_response(self, team_name, match_data, result_data, pre_match_sentiment=None):
        """
        Analyser la réponse sentimentale à un résultat de match en utilisant 
        toutes les sources de données disponibles.
        
        Args:
            team_name (str): Nom de l'équipe
            match_data (dict): Données du match
            result_data (dict): Données du résultat
            pre_match_sentiment (dict, optional): Analyse du sentiment avant le match
            
        Returns:
            dict: Analyse de la réponse sentimentale
        """
        # Si l'analyse pré-match n'est pas fournie, essayer de la récupérer
        if pre_match_sentiment is None:
            for analysis in reversed(self.analysis_history):
                if (analysis.get('type') in ['enhanced_sentiment_impact_prediction', 'sentiment_impact_prediction'] and 
                    analysis.get('team') == team_name and
                    analysis.get('match_date') == match_data.get('date')):
                    pre_match_sentiment = {
                        'dominant_emotion': analysis.get('summary', {}).get('dominant_emotion'),
                        'overall_intensity': 0.7,  # Valeur par défaut
                        'cohesion': 0.6  # Valeur par défaut
                    }
                    break
        
        # Si toujours pas disponible, utiliser des valeurs par défaut
        if pre_match_sentiment is None:
            pre_match_sentiment = {
                'dominant_emotion': 'anticipation',
                'overall_intensity': 0.7,
                'cohesion': 0.6
            }
        
        # Déterminer le résultat du match
        match_result = 'unknown'
        if 'score' in result_data:
            score = result_data['score']
            if isinstance(score, list) and len(score) == 2:
                team_score_index = 0 if match_data.get('home_team') == team_name else 1
                opponent_score_index = 1 - team_score_index
                if score[team_score_index] > score[opponent_score_index]:
                    match_result = 'win'
                elif score[team_score_index] < score[opponent_score_index]:
                    match_result = 'loss'
                else:
                    match_result = 'draw'
        
        # Récupérer les détails de l'équipe si le hub est disponible
        team_details = None
        if self.use_data_hub:
            try:
                team_details = get_team_details(team_name)
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des détails d'équipe: {e}")
        
        # Générer les données de réponse sentimentale enrichies
        response_data = self._generate_enhanced_response_data(
            team_name, match_result, pre_match_sentiment,
            team_details if self.use_data_hub else None
        )
        
        # Analyser chaque source de sentiment traditionnelle
        source_analyses = {}
        for source, source_config in self.sentiment_sources.items():
            source_data = response_data.get(source, {})
            source_analyses[source] = self._analyze_sentiment_source(
                source, source_data, source_config, team_name, is_response=True
            )
        
        # Analyser les sources de données réelles si disponibles
        real_data_analyses = {}
        if self.use_data_hub and team_details:
            try:
                # Analyser chaque source de données réelles
                for source, source_config in self.real_data_sources.items():
                    if source_config['available']:
                        if source == 'transfermarkt' and 'transfermarkt_data' in team_details:
                            source_data = team_details['transfermarkt_data']
                        elif source == 'soccerdata' and 'form' in team_details:
                            source_data = team_details['form']
                        elif source == 'player_data' and 'detailed_players' in team_details:
                            source_data = {'players': team_details['detailed_players']}
                            if 'detailed_manager' in team_details:
                                source_data['manager'] = team_details['detailed_manager']
                        elif source == 'historical_performance':
                            # Utiliser les performances historiques disponibles
                            source_data = {'team_name': team_name}
                            if 'form' in team_details:
                                source_data['form'] = team_details['form']
                        else:
                            source_data = {}
                        
                        # Ajouter le résultat du match pour l'analyse
                        if isinstance(source_data, dict):
                            source_data['match_result'] = match_result
                        
                        real_data_analyses[source] = self._analyze_real_data_source(
                            source, source_data, source_config, team_name, is_response=True
                        )
            except Exception as e:
                logger.error(f"Erreur lors de l'analyse des données réelles post-match pour {team_name}: {e}")
        
        # Calculer le sentiment dominant après le match
        if real_data_analyses:
            # Combiner les analyses traditionnelles et réelles
            combined_analyses = {**source_analyses, **real_data_analyses}
            post_match_emotion, emotion_scores = self._calculate_enhanced_dominant_emotion(
                combined_analyses, real_data_analyses
            )
            
            # Calculer l'intensité globale avec un bonus pour les données réelles
            post_match_intensity = self._calculate_enhanced_overall_intensity(
                combined_analyses, real_data_analyses
            )
        else:
            # Utiliser uniquement les analyses traditionnelles
            post_match_emotion, emotion_scores = self._calculate_dominant_emotion(source_analyses)
            post_match_intensity = self._calculate_overall_intensity(source_analyses)
        
        # Analyser le changement par rapport au sentiment pré-match
        sentiment_shift = self._analyze_sentiment_shift(
            pre_match_sentiment.get('dominant_emotion'),
            post_match_emotion,
            pre_match_sentiment.get('overall_intensity', 0.7),
            post_match_intensity
        )
        
        # Analyser la volatilité du sentiment
        sentiment_volatility = self._analyze_sentiment_volatility(
            source_analyses if not real_data_analyses else combined_analyses
        )
        
        # Calculer la durée prévue de l'effet
        expected_duration = self._calculate_enhanced_sentiment_effect_duration(
            post_match_emotion, post_match_intensity, match_result, match_data,
            team_details if self.use_data_hub else None
        )
        
        # Compiler l'analyse complète
        analysis = {
            'team_name': team_name,
            'match_date': match_data.get('date', datetime.now().isoformat()),
            'match_result': match_result,
            'analysis_timestamp': datetime.now().isoformat(),
            'pre_match_sentiment': pre_match_sentiment,
            'post_match_emotion': post_match_emotion,
            'emotion_scores': emotion_scores,
            'post_match_intensity': post_match_intensity,
            'sentiment_shift': sentiment_shift,
            'sentiment_volatility': sentiment_volatility,
            'source_analyses': source_analyses,
            'expected_duration': expected_duration,
            'future_impact': self._predict_enhanced_future_impact(
                team_name, post_match_emotion, post_match_intensity, 
                sentiment_shift, match_result,
                team_details if self.use_data_hub else None
            ),
            'data_quality': 0.5 + (0.3 if self.use_data_hub else 0)  # Base + bonus pour les données réelles
        }
        
        # Ajouter les analyses de données réelles si disponibles
        if real_data_analyses:
            analysis['real_data_analyses'] = real_data_analyses
        
        # Générer des insights avancés post-match si disponibles
        if self.use_advanced_insights and team_details:
            try:
                post_match_insights = generate_team_insights(team_name)
                analysis['post_match_insights'] = post_match_insights
            except Exception as e:
                logger.error(f"Erreur lors de la génération d'insights post-match pour {team_name}: {e}")
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'enhanced_sentiment_response_analysis',
            'timestamp': datetime.now().isoformat(),
            'team': team_name,
            'match_date': match_data.get('date'),
            'match_result': match_result,
            'summary': {
                'post_match_emotion': post_match_emotion,
                'intensity': post_match_intensity,
                'shift_magnitude': sentiment_shift.get('magnitude'),
                'data_quality': analysis.get('data_quality', 0.5)
            }
        })
        
        return analysis
    
    # Méthodes originales de la classe FanSentimentMonitor
    # ...
    
    # Nouvelles méthodes améliorées
    
    def _generate_enhanced_sentiment_data(self, team_name):
        """
        Génère des données de sentiment pour une équipe, enrichies avec des données réelles
        lorsque disponibles.
        
        Args:
            team_name (str): Nom de l'équipe
            
        Returns:
            dict: Données de sentiment générées
        """
        sentiment_data = {}
        
        # Générer des données pour chaque source traditionnelle
        for source, source_config in self.sentiment_sources.items():
            source_data = {}
            
            # Générer des métriques pour cette source
            for metric in source_config.get('metrics', []):
                source_data[metric] = random.uniform(0.3, 0.9)
            
            # Pour les réseaux sociaux, générer des données par plateforme
            if source == 'social_media':
                platform_data = {}
                for platform in source_config.get('platforms', []):
                    platform_data[platform] = {
                        'volume': random.randint(1000, 10000),
                        'sentiment_ratio': random.uniform(0.2, 0.8),
                        'emotional_intensity': random.uniform(0.4, 0.9),
                        'dominant_emotions': [
                            {
                                'emotion': random.choice(self.collective_emotions),
                                'strength': random.uniform(0.3, 0.9)
                            }
                            for _ in range(3)
                        ]
                    }
                source_data['platforms'] = platform_data
            
            # Ajouter des valeurs pour chaque émotion
            emotions_data = {}
            for emotion in self.collective_emotions:
                emotions_data[emotion] = random.uniform(0.1, 0.9)
            source_data['emotions'] = emotions_data
            
            sentiment_data[source] = source_data
        
        # Enrichir avec des données réelles si disponibles
        if self.use_data_hub:
            try:
                team_details = get_team_details(team_name)
                
                # Enrichir les données sociales avec des informations réelles
                if 'transfermarkt_data' in team_details and isinstance(team_details['transfermarkt_data'], dict):
                    # Extraire les statistiques sociales si disponibles
                    tm_data = team_details['transfermarkt_data']
                    social_stats = tm_data.get('social', {})
                    
                    if social_stats and 'social_media' in sentiment_data and 'platforms' in sentiment_data['social_media']:
                        platforms = sentiment_data['social_media']['platforms']
                        
                        # Twitter/X
                        if 'twitter' in platforms and 'twitter_followers' in social_stats:
                            platforms['twitter']['volume'] = social_stats['twitter_followers']
                        
                        # Facebook
                        if 'facebook' in platforms and 'facebook_likes' in social_stats:
                            platforms['facebook']['volume'] = social_stats['facebook_likes']
                        
                        # Instagram
                        if 'instagram' in platforms and 'instagram_followers' in social_stats:
                            platforms['instagram']['volume'] = social_stats['instagram_followers']
                
                # Enrichir les données de fréquentation
                if 'attendance_patterns' in sentiment_data:
                    if 'stats' in team_details and isinstance(team_details['stats'], dict):
                        stats = team_details['stats']
                        if 'average_attendance' in stats:
                            sentiment_data['attendance_patterns']['attendance_percentage'] = stats['average_attendance'] / stats.get('stadium_capacity', 100000)
                    
                    if 'transfermarkt_data' in team_details and isinstance(team_details['transfermarkt_data'], dict):
                        tm_data = team_details['transfermarkt_data']
                        if 'stadium' in tm_data and 'capacity' in tm_data['stadium']:
                            capacity = tm_data['stadium']['capacity']
                            if capacity > 0:
                                sentiment_data['attendance_patterns']['ticket_demand'] = min(0.9, random.uniform(0.5, 0.8) * 40000 / capacity)
                
                # Ajuster l'intensité émotionnelle en fonction des résultats récents
                if 'form' in team_details and isinstance(team_details['form'], dict) and 'data' in team_details['form']:
                    form_data = team_details['form']['data']
                    recent_results = []
                    
                    # Extraire les résultats récents
                    if isinstance(form_data, list):
                        for match in form_data[:5]:  # 5 derniers matchs
                            if 'result' in match:
                                recent_results.append(match['result'])
                    
                    # Calculer un facteur de forme
                    form_factor = 0.5  # Valeur neutre par défaut
                    if recent_results:
                        wins = recent_results.count('W')
                        draws = recent_results.count('D')
                        losses = recent_results.count('L')
                        form_factor = (wins * 0.2 + draws * 0.1 - losses * 0.1) + 0.5
                        form_factor = max(0.2, min(0.8, form_factor))
                    
                    # Ajuster les émotions en fonction de la forme
                    if form_factor > 0.6:  # Bonne forme
                        for source in sentiment_data.values():
                            if 'emotions' in source:
                                source['emotions']['confidence'] = random.uniform(0.7, 0.9)
                                source['emotions']['euphoria'] = random.uniform(0.6, 0.8)
                                source['emotions']['anxiety'] = random.uniform(0.2, 0.4)
                    elif form_factor < 0.4:  # Mauvaise forme
                        for source in sentiment_data.values():
                            if 'emotions' in source:
                                source['emotions']['anxiety'] = random.uniform(0.7, 0.9)
                                source['emotions']['desperation'] = random.uniform(0.6, 0.8)
                                source['emotions']['confidence'] = random.uniform(0.2, 0.4)
            except Exception as e:
                logger.error(f"Erreur lors de l'enrichissement des données de sentiment pour {team_name}: {e}")
        
        return sentiment_data
    
    def _analyze_real_data_source(self, source_name, source_data, source_config, team_name, is_response=False):
        """
        Analyse une source de données réelles pour en extraire le sentiment des supporters.
        
        Args:
            source_name (str): Nom de la source
            source_data (dict): Données de la source
            source_config (dict): Configuration de la source
            team_name (str): Nom de l'équipe
            is_response (bool, optional): Indique si l'analyse concerne une réponse post-match
            
        Returns:
            dict: Analyse de la source
        """
        analysis = {
            'source_name': source_name,
            'emotional_profile': {},
            'intensity': 0.0,
            'confidence': 0.0,
            'dominant_emotion': None,
            'metrics_analysis': {}
        }
        
        try:
            if not source_data:
                analysis['error'] = "Données source non disponibles"
                analysis['confidence'] = 0.3
                return analysis
            
            # Analyse spécifique selon la source
            if source_name == 'transfermarkt':
                analysis = self._analyze_transfermarkt_data(source_data, team_name, is_response)
            elif source_name == 'soccerdata':
                analysis = self._analyze_soccerdata(source_data, team_name, is_response)
            elif source_name == 'player_data':
                analysis = self._analyze_player_data(source_data, team_name, is_response)
            elif source_name == 'historical_performance':
                analysis = self._analyze_historical_performance(source_data, team_name, is_response)
            
            # Appliquer le poids de la source
            analysis['source_weight'] = source_config.get('weight', 0.25)
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse de la source {source_name}: {e}")
            analysis['error'] = str(e)
            analysis['confidence'] = 0.3
        
        return analysis
    
    def _analyze_transfermarkt_data(self, tm_data, team_name, is_response=False):
        """
        Analyse les données Transfermarkt pour en extraire le sentiment des supporters.
        
        Args:
            tm_data (dict): Données Transfermarkt
            team_name (str): Nom de l'équipe
            is_response (bool): Indique si l'analyse concerne une réponse post-match
            
        Returns:
            dict: Analyse des données Transfermarkt
        """
        analysis = {
            'source_name': 'transfermarkt',
            'emotional_profile': {},
            'intensity': 0.0,
            'confidence': 0.7,  # Confiance élevée pour les données réelles
            'dominant_emotion': None,
            'metrics_analysis': {}
        }
        
        # Vérifier que les données sont valides
        if not tm_data or not isinstance(tm_data, dict):
            analysis['error'] = "Données Transfermarkt non disponibles ou invalides"
            analysis['confidence'] = 0.3
            return analysis
        
        try:
            # Extraire les métriques pertinentes
            club_popularity = 0.5  # Valeur neutre par défaut
            social_media_followers = 0
            team_reputation = 0.5  # Valeur neutre par défaut
            
            # Popularité du club (basée sur la valeur du club)
            if 'marketValue' in tm_data:
                try:
                    market_value = tm_data['marketValue'].get('value', 0)
                    if isinstance(market_value, str):
                        if 'm' in market_value.lower():
                            market_value = float(market_value.lower().replace('m', '').replace('€', '')) * 1000000
                        elif 'k' in market_value.lower():
                            market_value = float(market_value.lower().replace('k', '').replace('€', '')) * 1000
                        else:
                            market_value = float(market_value.replace('€', ''))
                    
                    # Normaliser la valeur marchande entre 0 et 1
                    # Considérer 500M€ comme valeur maximale théorique
                    club_popularity = min(1.0, market_value / 500000000)
                    analysis['metrics_analysis']['club_value'] = market_value
                except (ValueError, TypeError, AttributeError) as e:
                    logger.warning(f"Erreur lors de l'extraction de la valeur marchande: {e}")
            
            # Extraire les followers sur les réseaux sociaux
            if 'social' in tm_data:
                social = tm_data['social']
                twitter = social.get('twitter_followers', 0)
                facebook = social.get('facebook_likes', 0)
                instagram = social.get('instagram_followers', 0)
                
                social_media_followers = twitter + facebook + instagram
                
                # Normaliser le nombre de followers entre 0 et 1
                # Considérer 50M comme nombre maximal théorique
                social_media_factor = min(1.0, social_media_followers / 50000000)
                analysis['metrics_analysis']['social_media_followers'] = social_media_followers
                analysis['metrics_analysis']['social_media_factor'] = social_media_factor
                
                # Utiliser le facteur social pour influencer l'intensité
                analysis['intensity'] = 0.4 + (social_media_factor * 0.6)
            
            # Extraire la réputation de l'équipe (stade, histoire, etc.)
            if 'founded' in tm_data and 'stadium' in tm_data:
                # Clubs plus anciens tendent à avoir une base de supporters plus fidèle
                try:
                    founded_year = int(tm_data['founded'])
                    years_existing = datetime.now().year - founded_year
                    # Normaliser l'âge du club (max théorique: 150 ans)
                    age_factor = min(1.0, years_existing / 150)
                    
                    # Capacité du stade comme indicateur de la taille du club
                    stadium_capacity = tm_data['stadium'].get('capacity', 0)
                    # Normaliser la capacité (max théorique: 100,000)
                    capacity_factor = min(1.0, stadium_capacity / 100000)
                    
                    # Combiner les facteurs
                    team_reputation = (age_factor * 0.4) + (capacity_factor * 0.6)
                    analysis['metrics_analysis']['club_age'] = years_existing
                    analysis['metrics_analysis']['stadium_capacity'] = stadium_capacity
                except (ValueError, TypeError, AttributeError) as e:
                    logger.warning(f"Erreur lors de l'extraction de la réputation: {e}")
            
            # Déterminer le profil émotionnel
            emotional_profile = {}
            
            # La popularité influence confiance et fierté
            emotional_profile['confidence'] = 0.4 + (club_popularity * 0.5)
            
            # Le nombre de followers influence l'intensité des émotions
            intensity_factor = 0.4 + (social_media_factor * 0.6)
            
            # La réputation historique influence la nostalgie et l'attachement
            emotional_profile['nostalgia'] = 0.3 + (team_reputation * 0.6)
            
            # Pour une réponse post-match, ajuster en fonction du résultat
            if is_response and 'match_result' in tm_data:
                match_result = tm_data['match_result']
                if match_result == 'win':
                    emotional_profile['euphoria'] = 0.7 + (intensity_factor * 0.3)
                    emotional_profile['confidence'] += 0.2
                elif match_result == 'loss':
                    emotional_profile['disappointment'] = 0.7 + (intensity_factor * 0.3)
                    emotional_profile['anxiety'] = 0.6 + (intensity_factor * 0.3)
                    emotional_profile['confidence'] -= 0.2
                else:  # draw
                    emotional_profile['anxiety'] = 0.5 + (intensity_factor * 0.2)
            else:
                # Sentiment par défaut pour l'analyse pré-match
                emotional_profile['anticipation'] = 0.5 + (intensity_factor * 0.3)
                emotional_profile['anxiety'] = 0.4 + ((1 - team_reputation) * 0.4)
            
            # S'assurer que toutes les émotions ont une valeur
            for emotion in self.collective_emotions:
                if emotion not in emotional_profile:
                    emotional_profile[emotion] = 0.3 + (random.random() * 0.3)
            
            # Normaliser le profil émotionnel pour qu'il somme à 1
            total = sum(emotional_profile.values())
            if total > 0:
                emotional_profile = {k: v / total for k, v in emotional_profile.items()}
            
            # Trouver l'émotion dominante
            dominant_emotion = max(emotional_profile.items(), key=lambda x: x[1])[0]
            
            analysis['emotional_profile'] = emotional_profile
            analysis['dominant_emotion'] = dominant_emotion
            
            # Mise à jour de l'intensité si non déjà calculée
            if analysis['intensity'] == 0.0:
                analysis['intensity'] = intensity_factor
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse des données Transfermarkt: {e}")
            analysis['error'] = str(e)
            analysis['confidence'] = 0.3
            return analysis
    
    def _analyze_soccerdata(self, data, team_name, is_response=False):
        """
        Analyse les données soccerdata pour en extraire le sentiment des supporters.
        
        Args:
            data (dict): Données soccerdata
            team_name (str): Nom de l'équipe
            is_response (bool): Indique si l'analyse concerne une réponse post-match
            
        Returns:
            dict: Analyse des données soccerdata
        """
        analysis = {
            'source_name': 'soccerdata',
            'emotional_profile': {},
            'intensity': 0.0,
            'confidence': 0.7,  # Confiance élevée pour les données réelles
            'dominant_emotion': None,
            'metrics_analysis': {}
        }
        
        # Vérifier que les données sont valides
        if not data or not isinstance(data, dict):
            analysis['error'] = "Données soccerdata non disponibles ou invalides"
            analysis['confidence'] = 0.3
            return analysis
        
        try:
            # Extraire les données de forme si disponibles
            form_data = None
            if 'data' in data:
                form_data = data['data']
            
            # Initialiser le profil émotionnel
            emotional_profile = {emotion: 0.0 for emotion in self.collective_emotions}
            
            if form_data and isinstance(form_data, list) and len(form_data) > 0:
                # Analyser les résultats récents
                recent_results = []
                for match in form_data[:5]:  # 5 derniers matchs
                    if 'result' in match:
                        recent_results.append(match['result'])
                
                if recent_results:
                    wins = recent_results.count('W')
                    draws = recent_results.count('D')
                    losses = recent_results.count('L')
                    
                    # Calculer un facteur de forme
                    form_factor = (wins * 0.2 + draws * 0.05 - losses * 0.1) + 0.5
                    form_factor = max(0.2, min(0.8, form_factor))
                    
                    analysis['metrics_analysis']['recent_form'] = {
                        'wins': wins,
                        'draws': draws,
                        'losses': losses,
                        'form_factor': form_factor
                    }
                    
                    # Ajuster le profil émotionnel en fonction de la forme
                    if form_factor > 0.65:  # Très bonne forme
                        emotional_profile['confidence'] = 0.7 + (random.random() * 0.2)
                        emotional_profile['euphoria'] = 0.6 + (random.random() * 0.2)
                        emotional_profile['anticipation'] = 0.6 + (random.random() * 0.2)
                    elif form_factor > 0.5:  # Bonne forme
                        emotional_profile['confidence'] = 0.6 + (random.random() * 0.2)
                        emotional_profile['anticipation'] = 0.5 + (random.random() * 0.2)
                    elif form_factor > 0.35:  # Forme moyenne
                        emotional_profile['anxiety'] = 0.5 + (random.random() * 0.2)
                        emotional_profile['anticipation'] = 0.4 + (random.random() * 0.2)
                    else:  # Mauvaise forme
                        emotional_profile['anxiety'] = 0.6 + (random.random() * 0.2)
                        emotional_profile['desperation'] = 0.5 + (random.random() * 0.2)
                        emotional_profile['disappointment'] = 0.6 + (random.random() * 0.2)
                    
                    # Calculer l'intensité en fonction de la volatilité des résultats
                    volatility = len(set(recent_results)) / len(recent_results)
                    analysis['intensity'] = 0.5 + (volatility * 0.3) + (form_factor * 0.2)
                else:
                    # Pas de résultats récents
                    emotional_profile = {e: 0.3 + (random.random() * 0.4) for e in emotional_profile}
                    analysis['intensity'] = 0.5
            else:
                # Pas de données de forme
                emotional_profile = {e: 0.3 + (random.random() * 0.4) for e in emotional_profile}
                analysis['intensity'] = 0.5
            
            # Pour une réponse post-match, ajuster en fonction du résultat
            if is_response and 'match_result' in data:
                match_result = data['match_result']
                if match_result == 'win':
                    emotional_profile['euphoria'] = 0.7 + (random.random() * 0.2)
                    emotional_profile['confidence'] += 0.2
                elif match_result == 'loss':
                    emotional_profile['disappointment'] = 0.7 + (random.random() * 0.2)
                    emotional_profile['anxiety'] = 0.6 + (random.random() * 0.2)
                else:  # draw
                    emotional_profile['anxiety'] = 0.5 + (random.random() * 0.2)
                    emotional_profile['anticipation'] = 0.4 + (random.random() * 0.2)
            
            # Normaliser le profil émotionnel pour qu'il somme à 1
            total = sum(emotional_profile.values())
            if total > 0:
                emotional_profile = {k: v / total for k, v in emotional_profile.items()}
            
            # Trouver l'émotion dominante
            dominant_emotion = max(emotional_profile.items(), key=lambda x: x[1])[0]
            
            analysis['emotional_profile'] = emotional_profile
            analysis['dominant_emotion'] = dominant_emotion
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse des données soccerdata: {e}")
            analysis['error'] = str(e)
            analysis['confidence'] = 0.3
            return analysis
    
    def _analyze_player_data(self, data, team_name, is_response=False):
        """
        Analyse les données des joueurs pour en extraire le sentiment des supporters.
        
        Args:
            data (dict): Données des joueurs et du manager
            team_name (str): Nom de l'équipe
            is_response (bool): Indique si l'analyse concerne une réponse post-match
            
        Returns:
            dict: Analyse des données des joueurs
        """
        analysis = {
            'source_name': 'player_data',
            'emotional_profile': {},
            'intensity': 0.0,
            'confidence': 0.7,  # Confiance élevée pour les données réelles
            'dominant_emotion': None,
            'metrics_analysis': {}
        }
        
        # Vérifier que les données sont valides
        if not data or not isinstance(data, dict):
            analysis['error'] = "Données des joueurs non disponibles ou invalides"
            analysis['confidence'] = 0.3
            return analysis
        
        try:
            # Extraire les données des joueurs et du manager
            players_data = data.get('players', [])
            manager_data = data.get('manager', {})
            
            # Initialiser le profil émotionnel
            emotional_profile = {emotion: 0.0 for emotion in self.collective_emotions}
            
            # Analyser les joueurs
            if players_data and isinstance(players_data, list) and len(players_data) > 0:
                # Calculer la valeur totale des joueurs
                total_value = 0
                star_players = []
                injured_key_players = []
                
                for player in players_data:
                    # Vérifier si c'est un joueur clé (valeur marchande élevée ou stats)
                    is_key_player = False
                    
                    # Vérifier la valeur marchande
                    market_value = 0
                    if 'market_value' in player:
                        try:
                            if isinstance(player['market_value'], str):
                                if 'M' in player['market_value']:
                                    market_value = float(player['market_value'].replace('M', '').replace('€', '')) * 1000000
                                elif 'K' in player['market_value']:
                                    market_value = float(player['market_value'].replace('K', '').replace('€', '')) * 1000
                                else:
                                    market_value = float(player['market_value'].replace('€', ''))
                            else:
                                market_value = player['market_value']
                                
                            total_value += market_value
                            
                            # Joueur de valeur élevée
                            if market_value > 20000000:
                                is_key_player = True
                        except (ValueError, TypeError):
                            pass
                    
                    # Vérifier les statistiques (buts, passes)
                    if player.get('goals', 0) > 5 or player.get('assists', 0) > 5:
                        is_key_player = True
                    
                    # Ajouter aux joueurs stars si c'est un joueur clé
                    if is_key_player:
                        star_players.append({
                            'name': player.get('name', 'Inconnu'),
                            'value': market_value,
                            'goals': player.get('goals', 0),
                            'assists': player.get('assists', 0)
                        })
                        
                        # Vérifier s'il est blessé
                        if player.get('injury_status'):
                            injured_key_players.append(player.get('name', 'Inconnu'))
                
                # Analyser les joueurs stars
                star_player_count = len(star_players)
                injured_count = len(injured_key_players)
                
                analysis['metrics_analysis']['star_players'] = {
                    'count': star_player_count,
                    'details': star_players,
                    'injured_count': injured_count,
                    'injured_players': injured_key_players
                }
                
                # Ajuster le profil émotionnel en fonction des joueurs stars
                if star_player_count > 3:
                    emotional_profile['confidence'] = 0.6 + (random.random() * 0.2)
                    emotional_profile['anticipation'] = 0.5 + (random.random() * 0.2)
                elif star_player_count > 0:
                    emotional_profile['confidence'] = 0.5 + (random.random() * 0.2)
                    emotional_profile['anticipation'] = 0.4 + (random.random() * 0.2)
                
                # Ajuster en fonction des blessures
                if injured_count > 0:
                    if injured_count > 2:
                        emotional_profile['anxiety'] = 0.7 + (random.random() * 0.2)
                        emotional_profile['desperation'] = 0.5 + (random.random() * 0.2)
                    else:
                        emotional_profile['anxiety'] = 0.5 + (random.random() * 0.2)
                
                # Normaliser la valeur totale (MAX_VALUE = 1B€)
                normalized_value = min(1.0, total_value / 1000000000)
                analysis['metrics_analysis']['total_squad_value'] = total_value
                analysis['metrics_analysis']['normalized_value'] = normalized_value
                
                # Ajuster l'intensité en fonction de la valeur de l'équipe et des joueurs stars
                analysis['intensity'] = 0.4 + (normalized_value * 0.3) + (min(1.0, star_player_count / 5) * 0.3)
            
            # Analyser le manager
            if manager_data and isinstance(manager_data, dict):
                manager_reputation = 0.5  # Par défaut
                
                # Calculer une réputation basée sur les statistiques
                if 'games_total' in manager_data and manager_data['games_total'] > 0:
                    wins = manager_data.get('games_won', 0)
                    total = manager_data['games_total']
                    win_ratio = wins / total if total > 0 else 0
                    
                    manager_reputation = 0.3 + (win_ratio * 0.7)
                
                # Vérifier les trophées
                trophy_count = len(manager_data.get('trophies', []))
                if trophy_count > 0:
                    trophy_factor = min(1.0, trophy_count / 10)  # Normaliser (max 10 trophées)
                    manager_reputation = max(manager_reputation, 0.5 + (trophy_factor * 0.5))
                
                analysis['metrics_analysis']['manager'] = {
                    'name': manager_data.get('name', 'Inconnu'),
                    'reputation': manager_reputation,
                    'trophies': trophy_count
                }
                
                # Ajuster le profil émotionnel en fonction du manager
                if manager_reputation > 0.7:
                    emotional_profile['confidence'] = max(emotional_profile.get('confidence', 0), 0.6 + (random.random() * 0.2))
                    emotional_profile['anticipation'] = max(emotional_profile.get('anticipation', 0), 0.5 + (random.random() * 0.2))
                elif manager_reputation > 0.4:
                    emotional_profile['confidence'] = max(emotional_profile.get('confidence', 0), 0.5 + (random.random() * 0.2))
                else:
                    emotional_profile['anxiety'] = max(emotional_profile.get('anxiety', 0), 0.5 + (random.random() * 0.2))
                    emotional_profile['desperation'] = max(emotional_profile.get('desperation', 0), 0.4 + (random.random() * 0.2))
            
            # Pour une réponse post-match, ajuster en fonction du résultat
            if is_response and 'match_result' in data:
                match_result = data['match_result']
                if match_result == 'win':
                    emotional_profile['euphoria'] = max(emotional_profile.get('euphoria', 0), 0.7 + (random.random() * 0.2))
                    emotional_profile['confidence'] += 0.2
                elif match_result == 'loss':
                    emotional_profile['disappointment'] = max(emotional_profile.get('disappointment', 0), 0.7 + (random.random() * 0.2))
                    emotional_profile['anxiety'] = max(emotional_profile.get('anxiety', 0), 0.6 + (random.random() * 0.2))
                else:  # draw
                    emotional_profile['anxiety'] = max(emotional_profile.get('anxiety', 0), 0.5 + (random.random() * 0.2))
            
            # S'assurer que toutes les émotions ont une valeur
            for emotion in self.collective_emotions:
                if emotion not in emotional_profile or emotional_profile[emotion] <= 0:
                    emotional_profile[emotion] = 0.3 + (random.random() * 0.3)
            
            # Normaliser le profil émotionnel pour qu'il somme à 1
            total = sum(emotional_profile.values())
            if total > 0:
                emotional_profile = {k: v / total for k, v in emotional_profile.items()}
            
            # Trouver l'émotion dominante
            dominant_emotion = max(emotional_profile.items(), key=lambda x: x[1])[0]
            
            analysis['emotional_profile'] = emotional_profile
            analysis['dominant_emotion'] = dominant_emotion
            
            # Mise à jour de l'intensité si non déjà calculée
            if analysis['intensity'] == 0.0:
                analysis['intensity'] = 0.5  # Valeur par défaut
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse des données des joueurs: {e}")
            analysis['error'] = str(e)
            analysis['confidence'] = 0.3
            return analysis
    
    def _analyze_historical_performance(self, data, team_name, is_response=False):
        """
        Analyse les performances historiques pour en extraire le sentiment des supporters.
        
        Args:
            data (dict): Données des performances historiques
            team_name (str): Nom de l'équipe
            is_response (bool): Indique si l'analyse concerne une réponse post-match
            
        Returns:
            dict: Analyse des performances historiques
        """
        analysis = {
            'source_name': 'historical_performance',
            'emotional_profile': {},
            'intensity': 0.0,
            'confidence': 0.6,  # Confiance moyenne
            'dominant_emotion': None,
            'metrics_analysis': {}
        }
        
        # Vérifier que les données sont valides
        if not data or not isinstance(data, dict):
            analysis['error'] = "Données historiques non disponibles ou invalides"
            analysis['confidence'] = 0.3
            return analysis
        
        try:
            # Extraire les données de forme si disponibles
            form_data = None
            if 'form' in data and isinstance(data['form'], dict) and 'data' in data['form']:
                form_data = data['form']['data']
            
            # Initialiser le profil émotionnel
            emotional_profile = {emotion: 0.0 for emotion in self.collective_emotions}
            
            # Simuler des données historiques de base
            trophy_history = {
                'league_titles': random.randint(0, 10),
                'cup_titles': random.randint(0, 8),
                'continental_titles': random.randint(0, 3),
                'last_trophy_years_ago': random.randint(1, 20)
            }
            
            analysis['metrics_analysis']['trophy_history'] = trophy_history
            
            # Ajuster le profil émotionnel en fonction de l'historique des trophées
            total_trophies = sum(trophy_history.values()) - trophy_history['last_trophy_years_ago']
            if total_trophies > 10:
                # Club historiquement grand
                emotional_profile['nostalgia'] = 0.7 + (random.random() * 0.2)
                emotional_profile['confidence'] = 0.6 + (random.random() * 0.2)
            elif total_trophies > 5:
                # Club établi
                emotional_profile['nostalgia'] = 0.5 + (random.random() * 0.2)
                emotional_profile['confidence'] = 0.5 + (random.random() * 0.2)
            else:
                # Club moins prestigieux
                emotional_profile['anxiety'] = 0.5 + (random.random() * 0.2)
            
            # Ajuster en fonction du temps écoulé depuis le dernier trophée
            if trophy_history['last_trophy_years_ago'] > 10:
                emotional_profile['desperation'] = 0.6 + (random.random() * 0.2)
            elif trophy_history['last_trophy_years_ago'] <= 3:
                emotional_profile['euphoria'] = 0.5 + (random.random() * 0.2)
                emotional_profile['confidence'] += 0.1
            
            # Analyser les résultats récents si disponibles
            if form_data and isinstance(form_data, list) and len(form_data) > 0:
                recent_results = []
                for match in form_data[:10]:  # 10 derniers matchs
                    if 'result' in match:
                        recent_results.append(match['result'])
                
                if recent_results:
                    wins = recent_results.count('W')
                    draws = recent_results.count('D')
                    losses = recent_results.count('L')
                    
                    # Calculer un facteur de forme
                    form_factor = (wins * 0.2 + draws * 0.05 - losses * 0.1) + 0.5
                    form_factor = max(0.2, min(0.8, form_factor))
                    
                    analysis['metrics_analysis']['recent_form'] = {
                        'wins': wins,
                        'draws': draws,
                        'losses': losses,
                        'form_factor': form_factor
                    }
                    
                    # Ajuster l'intensité en fonction de la volatilité des résultats
                    volatility = len(set(recent_results)) / len(recent_results)
                    analysis['intensity'] = 0.4 + (volatility * 0.3) + (form_factor * 0.3)
            else:
                analysis['intensity'] = 0.5  # Valeur par défaut
            
            # Pour une réponse post-match, ajuster en fonction du résultat
            if is_response and 'match_result' in data:
                match_result = data['match_result']
                if match_result == 'win':
                    emotional_profile['euphoria'] = 0.7 + (random.random() * 0.2)
                    emotional_profile['confidence'] += 0.2
                elif match_result == 'loss':
                    emotional_profile['disappointment'] = 0.7 + (random.random() * 0.2)
                    emotional_profile['anxiety'] = 0.6 + (random.random() * 0.2)
                else:  # draw
                    emotional_profile['anxiety'] = 0.5 + (random.random() * 0.2)
            
            # S'assurer que toutes les émotions ont une valeur
            for emotion in self.collective_emotions:
                if emotion not in emotional_profile or emotional_profile[emotion] <= 0:
                    emotional_profile[emotion] = 0.3 + (random.random() * 0.3)
            
            # Normaliser le profil émotionnel pour qu'il somme à 1
            total = sum(emotional_profile.values())
            if total > 0:
                emotional_profile = {k: v / total for k, v in emotional_profile.items()}
            
            # Trouver l'émotion dominante
            dominant_emotion = max(emotional_profile.items(), key=lambda x: x[1])[0]
            
            analysis['emotional_profile'] = emotional_profile
            analysis['dominant_emotion'] = dominant_emotion
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse des performances historiques: {e}")
            analysis['error'] = str(e)
            analysis['confidence'] = 0.3
            return analysis
    
    def _calculate_enhanced_dominant_emotion(self, combined_analyses, real_data_analyses):
        """
        Calcule l'émotion dominante en prenant en compte toutes les sources,
        mais en donnant plus de poids aux données réelles.
        
        Args:
            combined_analyses (dict): Analyses combinées (traditionnelles + réelles)
            real_data_analyses (dict): Analyses des données réelles
            
        Returns:
            tuple: Émotion dominante et scores pour toutes les émotions
        """
        # Initialiser les scores
        emotion_scores = {emotion: 0.0 for emotion in self.collective_emotions}
        
        # Facteur de pondération pour les données réelles
        real_data_weight_factor = 1.5
        
        # Compiler les scores émotionnels de toutes les sources
        for source, analysis in combined_analyses.items():
            # Vérifier si c'est une source de données réelles
            is_real_data = source in real_data_analyses
            
            # Récupérer le profil émotionnel
            emotional_profile = analysis.get('emotional_profile', {})
            
            # Récupérer le poids de la source
            source_weight = analysis.get('source_weight', 0.25)
            
            # Appliquer le facteur de pondération pour les données réelles
            if is_real_data:
                source_weight *= real_data_weight_factor
            
            # Ajouter les scores de cette source pour chaque émotion
            for emotion, score in emotional_profile.items():
                if emotion in emotion_scores:
                    emotion_scores[emotion] += score * source_weight
        
        # Normaliser les scores
        total_score = sum(emotion_scores.values())
        if total_score > 0:
            emotion_scores = {emotion: score / total_score for emotion, score in emotion_scores.items()}
        
        # Déterminer l'émotion dominante
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
        
        return dominant_emotion, emotion_scores
    
    def _calculate_enhanced_overall_intensity(self, combined_analyses, real_data_analyses):
        """
        Calcule l'intensité globale en prenant en compte toutes les sources,
        mais en donnant plus de poids aux données réelles.
        
        Args:
            combined_analyses (dict): Analyses combinées (traditionnelles + réelles)
            real_data_analyses (dict): Analyses des données réelles
            
        Returns:
            float: Intensité globale
        """
        # Facteur de pondération pour les données réelles
        real_data_weight_factor = 1.5
        
        # Initialiser les variables pour la moyenne pondérée
        weighted_sum = 0.0
        total_weight = 0.0
        
        # Calculer la moyenne pondérée des intensités
        for source, analysis in combined_analyses.items():
            # Vérifier si c'est une source de données réelles
            is_real_data = source in real_data_analyses
            
            # Récupérer l'intensité
            intensity = analysis.get('intensity', 0.5)
            
            # Récupérer le poids de la source
            source_weight = analysis.get('source_weight', 0.25)
            
            # Appliquer le facteur de pondération pour les données réelles
            if is_real_data:
                source_weight *= real_data_weight_factor
            
            # Ajouter à la somme pondérée
            weighted_sum += intensity * source_weight
            total_weight += source_weight
        
        # Calculer l'intensité globale
        if total_weight > 0:
            overall_intensity = weighted_sum / total_weight
        else:
            overall_intensity = 0.5  # Valeur par défaut
        
        return overall_intensity
    
    def _evaluate_enhanced_sentiment_cohesion(self, combined_analyses, real_data_analyses):
        """
        Évalue la cohésion du sentiment en prenant en compte toutes les sources,
        mais en donnant plus de poids aux données réelles.
        
        Args:
            combined_analyses (dict): Analyses combinées (traditionnelles + réelles)
            real_data_analyses (dict): Analyses des données réelles
            
        Returns:
            dict: Analyse de la cohésion du sentiment
        """
        # Facteur de pondération pour les données réelles
        real_data_weight_factor = 1.5
        
        # Extraire les émotions dominantes de chaque source
        dominant_emotions = {}
        for source, analysis in combined_analyses.items():
            # Récupérer l'émotion dominante
            dominant_emotion = analysis.get('dominant_emotion')
            
            if dominant_emotion:
                # Récupérer le poids de la source
                source_weight = analysis.get('source_weight', 0.25)
                
                # Appliquer le facteur de pondération pour les données réelles
                if source in real_data_analyses:
                    source_weight *= real_data_weight_factor
                
                if dominant_emotion in dominant_emotions:
                    dominant_emotions[dominant_emotion] += source_weight
                else:
                    dominant_emotions[dominant_emotion] = source_weight
        
        # Calculer la cohésion globale
        total_weight = sum(dominant_emotions.values())
        if total_weight > 0:
            max_emotion_weight = max(dominant_emotions.values())
            overall_cohesion = max_emotion_weight / total_weight
        else:
            overall_cohesion = 0.5  # Valeur par défaut
        
        # Identifier les sources de discorde
        discord_sources = []
        if len(dominant_emotions) > 1:
            # Trouver l'émotion dominante globale
            global_dominant = max(dominant_emotions.items(), key=lambda x: x[1])[0]
            
            # Identifier les sources qui ont une émotion dominante différente
            for source, analysis in combined_analyses.items():
                if analysis.get('dominant_emotion') != global_dominant:
                    discord_sources.append({
                        'source': source,
                        'emotion': analysis.get('dominant_emotion'),
                        'intensity': analysis.get('intensity', 0.5)
                    })
        
        return {
            'overall_cohesion': overall_cohesion,
            'emotion_distribution': dominant_emotions,
            'discord_sources': discord_sources
        }
    
    def _calculate_enhanced_match_importance(self, match_data, team_details=None, opponent_details=None):
        """
        Calcule l'importance d'un match en utilisant toutes les données disponibles.
        
        Args:
            match_data (dict): Données du match
            team_details (dict, optional): Détails de l'équipe
            opponent_details (dict, optional): Détails de l'équipe adverse
            
        Returns:
            dict: Importance du match
        """
        # Base d'importance
        importance = {
            'level': 'regular',
            'value': 0.5,
            'factors': []
        }
        
        # Vérifier si des informations sur le type de compétition sont disponibles
        competition_type = match_data.get('competition_type', '').lower()
        
        if competition_type in ['final', 'finale', 'championship final']:
            importance['level'] = 'final'
            importance['value'] = 0.9
            importance['factors'].append({'type': 'competition', 'description': 'Finale', 'value': 0.4})
        elif competition_type in ['semifinal', 'demi-finale', 'semi-final']:
            importance['level'] = 'semifinal'
            importance['value'] = 0.8
            importance['factors'].append({'type': 'competition', 'description': 'Demi-finale', 'value': 0.3})
        elif competition_type in ['quarterfinal', 'quart-finale', 'quarter-final']:
            importance['level'] = 'quarterfinal'
            importance['value'] = 0.7
            importance['factors'].append({'type': 'competition', 'description': 'Quart de finale', 'value': 0.2})
        elif 'cup' in competition_type or 'knockout' in competition_type:
            importance['level'] = 'cup_match'
            importance['value'] = 0.65
            importance['factors'].append({'type': 'competition', 'description': 'Match de coupe', 'value': 0.15})
        elif 'derby' in competition_type or 'rivalry' in competition_type:
            importance['level'] = 'derby'
            importance['value'] = 0.75
            importance['factors'].append({'type': 'rivalry', 'description': 'Derby', 'value': 0.25})
        elif 'playoff' in competition_type:
            importance['level'] = 'playoff'
            importance['value'] = 0.8
            importance['factors'].append({'type': 'competition', 'description': 'Playoff', 'value': 0.3})
        
        # Si des données d'équipes sont disponibles, enrichir l'analyse
        if team_details and opponent_details and self.use_data_hub:
            # Vérifier s'il s'agit d'un derby ou d'une rivalité historique
            try:
                # Analyser les données de transfermarkt si disponibles
                if ('transfermarkt_data' in team_details and 'transfermarkt_data' in opponent_details and
                    'name' in team_details['transfermarkt_data'] and 'name' in opponent_details['transfermarkt_data']):
                    tm_team = team_details['transfermarkt_data']['name']
                    tm_opponent = opponent_details['transfermarkt_data']['name']
                    
                    # Liste de derbies connus (pourrait être étendue)
                    derbies = [
                        ('Real Madrid', 'Barcelona'),
                        ('Manchester United', 'Manchester City'),
                        ('Liverpool', 'Everton'),
                        ('Arsenal', 'Tottenham'),
                        ('Inter', 'Milan'),
                        ('Roma', 'Lazio'),
                        ('Boca Juniors', 'River Plate'),
                        ('Celtic', 'Rangers'),
                        ('Marseille', 'Paris Saint-Germain')
                    ]
                    
                    # Vérifier si les équipes forment un derby connu
                    is_derby = any((tm_team in pair and tm_opponent in pair) for pair in derbies)
                    
                    if is_derby and 'derby' not in importance['level']:
                        importance['level'] = 'derby'
                        importance['value'] = max(importance['value'], 0.75)
                        importance['factors'].append({'type': 'rivalry', 'description': 'Derby historique', 'value': 0.25})
            except Exception as e:
                logger.warning(f"Erreur lors de l'analyse de rivalité: {e}")
            
            # Vérifier l'enjeu au classement
            try:
                if ('transfermarkt_data' in team_details and 'transfermarkt_data' in opponent_details and
                    'league' in team_details['transfermarkt_data'] and 'league' in opponent_details['transfermarkt_data']):
                    team_position = team_details['transfermarkt_data']['league'].get('position', 0)
                    opponent_position = opponent_details['transfermarkt_data']['league'].get('position', 0)
                    
                    # Si les positions sont proches, l'enjeu est plus important
                    if team_position > 0 and opponent_position > 0:
                        position_difference = abs(team_position - opponent_position)
                        if position_difference <= 2:
                            importance['factors'].append({'type': 'standings', 'description': 'Positions proches au classement', 'value': 0.15})
                            importance['value'] = max(importance['value'], 0.65)
                        
                        # Match pour le titre (entre équipes du haut de tableau)
                        if team_position <= 4 and opponent_position <= 4:
                            importance['factors'].append({'type': 'standings', 'description': 'Match entre prétendants au titre', 'value': 0.2})
                            importance['value'] = max(importance['value'], 0.7)
                        
                        # Match pour le maintien (entre équipes du bas de tableau)
                        relegation_zone = 18  # Adapter selon le championnat
                        if team_position >= relegation_zone - 3 and opponent_position >= relegation_zone - 3:
                            importance['factors'].append({'type': 'standings', 'description': 'Match pour le maintien', 'value': 0.2})
                            importance['value'] = max(importance['value'], 0.7)
            except Exception as e:
                logger.warning(f"Erreur lors de l'analyse de l'enjeu au classement: {e}")
        
        return importance
    
    def _calculate_enhanced_base_sentiment_impact(self, current_sentiment, match_importance, is_home, team_details=None):
        """
        Calcule l'impact de base du sentiment sur la performance, en utilisant toutes les données disponibles.
        
        Args:
            current_sentiment (dict): Analyse du sentiment actuel
            match_importance (dict): Importance du match
            is_home (bool): Indique si le match est à domicile
            team_details (dict, optional): Détails de l'équipe
            
        Returns:
            dict: Impact de base du sentiment
        """
        # Extraire les informations clés du sentiment actuel
        dominant_emotion = current_sentiment.get('dominant_emotion', 'neutral')
        intensity = current_sentiment.get('overall_intensity', 0.5)
        cohesion = current_sentiment.get('sentiment_cohesion', {}).get('overall_cohesion', 0.5)
        
        # Extraire l'importance du match
        importance_value = match_importance.get('value', 0.5)
        
        # Calculer l'impact émotionnel de base
        emotional_impact = self._calculate_emotion_impact(dominant_emotion, intensity)
        
        # Appliquer le facteur de cohésion
        # Une plus grande cohésion amplifie l'impact (positif ou négatif)
        cohesion_factor = 0.7 + (cohesion * 0.6)  # Entre 0.7 et 1.3
        adjusted_emotion_impact = emotional_impact * cohesion_factor
        
        # Appliquer le facteur d'avantage à domicile
        home_advantage = 0.0
        if is_home:
            home_advantage = self.sentiment_parameters['home_advantage_factor']
            
            # Si des données d'équipe sont disponibles, affiner l'avantage du domicile
            if team_details and self.use_data_hub:
                try:
                    # Analyser les performances à domicile si disponibles
                    if 'form' in team_details and isinstance(team_details['form'], dict) and 'data' in team_details['form']:
                        form_data = team_details['form']['data']
                        
                        if isinstance(form_data, list):
                            # Filtrer les matchs à domicile
                            home_matches = [m for m in form_data if m.get('home_team') == team_details.get('team_name')]
                            
                            if home_matches:
                                # Calculer la performance à domicile
                                home_wins = sum(1 for m in home_matches if m.get('result') == 'W')
                                home_ratio = home_wins / len(home_matches)
                                
                                # Ajuster l'avantage à domicile
                                if home_ratio > 0.6:
                                    home_advantage += 0.1  # Bonus pour les équipes fortes à domicile
                                elif home_ratio < 0.3:
                                    home_advantage -= 0.05  # Malus pour les équipes faibles à domicile
                except Exception as e:
                    logger.warning(f"Erreur lors de l'analyse de l'avantage à domicile: {e}")
        
        # Appliquer le facteur d'importance du match
        # Les matchs plus importants amplifient l'impact du sentiment
        importance_factor = 0.7 + (importance_value * 0.6)  # Entre 0.7 et 1.3
        
        # Calculer l'impact total
        raw_impact = (adjusted_emotion_impact + home_advantage) * importance_factor
        
        # Limiter l'impact dans une plage raisonnable
        raw_impact = max(-1.0, min(1.0, raw_impact))
        
        # Compiler l'impact de base
        base_impact = {
            'dominant_emotion': dominant_emotion,
            'emotional_impact': emotional_impact,
            'cohesion_factor': cohesion_factor,
            'home_advantage': home_advantage,
            'importance_factor': importance_factor,
            'raw_impact': raw_impact
        }
        
        return base_impact
    
    def _generate_enhanced_impact_scenarios(self, adjusted_impact, form_factor, team_details=None):
        """
        Génère des scénarios d'impact potentiels en utilisant toutes les données disponibles.
        
        Args:
            adjusted_impact (dict): Impact ajusté du sentiment
            form_factor (float): Facteur de forme de l'équipe
            team_details (dict, optional): Détails de l'équipe
            
        Returns:
            list: Scénarios d'impact potentiels
        """
        impact_scenarios = []
        
        # Extraire les informations clés
        impact_value = adjusted_impact.get('total_impact', 0.0)
        impact_type = adjusted_impact.get('impact_type', 'neutral')
        dominant_emotion = adjusted_impact.get('dominant_emotion', 'neutral')
        
        # Déterminer les scénarios en fonction du type d'impact
        if impact_type == 'strong_positive':
            # Impact très positif
            impact_scenarios.append({
                'scenario': 'optimal',
                'description': "Les supporters galvanisent l'équipe qui réalise une performance exceptionnelle",
                'probability': 0.6 + (0.2 * form_factor),
                'impact_modifier': 0.2
            })
            
            impact_scenarios.append({
                'scenario': 'positive',
                'description': "L'équipe performe bien, portée par le soutien des supporters",
                'probability': 0.3 - (0.1 * form_factor),
                'impact_modifier': 0.1
            })
            
            impact_scenarios.append({
                'scenario': 'pressure',
                'description': "La pression des attentes affecte négativement certains joueurs",
                'probability': 0.1 - (0.05 * form_factor),
                'impact_modifier': -0.1
            })
            
        elif impact_type == 'positive':
            # Impact positif
            impact_scenarios.append({
                'scenario': 'positive',
                'description': "L'équipe est bien soutenue et performe au-dessus de son niveau habituel",
                'probability': 0.5 + (0.1 * form_factor),
                'impact_modifier': 0.1
            })
            
            impact_scenarios.append({
                'scenario': 'neutral',
                'description': "L'équipe joue normalement, avec un léger boost d'énergie",
                'probability': 0.4 - (0.1 * form_factor),
                'impact_modifier': 0.0
            })
            
            impact_scenarios.append({
                'scenario': 'inconsistent',
                'description': "L'équipe alterne entre des moments forts et des passages à vide",
                'probability': 0.1,
                'impact_modifier': -0.05
            })
            
        elif impact_type == 'neutral':
            # Impact neutre
            impact_scenarios.append({
                'scenario': 'standard',
                'description': "L'équipe joue à son niveau habituel, sans influence particulière des supporters",
                'probability': 0.6,
                'impact_modifier': 0.0
            })
            
            impact_scenarios.append({
                'scenario': 'slight_positive',
                'description': "L'équipe trouve un peu d'énergie supplémentaire en cours de match",
                'probability': 0.2 + (0.1 * form_factor),
                'impact_modifier': 0.05
            })
            
            impact_scenarios.append({
                'scenario': 'slight_negative',
                'description': "L'équipe manque légèrement d'inspiration ou de soutien à des moments clés",
                'probability': 0.2 - (0.1 * form_factor),
                'impact_modifier': -0.05
            })
            
        elif impact_type == 'negative':
            # Impact négatif
            impact_scenarios.append({
                'scenario': 'nervous',
                'description': "L'équipe semble tendue et commet des erreurs inhabituelles",
                'probability': 0.5 - (0.1 * form_factor),
                'impact_modifier': -0.1
            })
            
            impact_scenarios.append({
                'scenario': 'flat',
                'description': "L'équipe manque d'énergie et joue sans inspiration",
                'probability': 0.3,
                'impact_modifier': -0.05
            })
            
            impact_scenarios.append({
                'scenario': 'resilient',
                'description': "L'équipe fait preuve de caractère malgré l'ambiance négative",
                'probability': 0.2 + (0.1 * form_factor),
                'impact_modifier': 0.1
            })
            
        elif impact_type == 'strong_negative':
            # Impact très négatif
            impact_scenarios.append({
                'scenario': 'collapse',
                'description': "L'équipe s'effondre sous la pression négative des supporters",
                'probability': 0.6 - (0.2 * form_factor),
                'impact_modifier': -0.2
            })
            
            impact_scenarios.append({
                'scenario': 'struggle',
                'description': "L'équipe lutte mais n'arrive pas à se libérer du poids de l'ambiance négative",
                'probability': 0.3 + (0.1 * form_factor),
                'impact_modifier': -0.1
            })
            
            impact_scenarios.append({
                'scenario': 'defiance',
                'description': "L'équipe se révolte contre l'ambiance négative et trouve des ressources inattendues",
                'probability': 0.1 + (0.1 * form_factor),
                'impact_modifier': 0.15
            })
        
        # Enrichir les scénarios si des données détaillées sont disponibles
        if team_details and self.use_data_hub:
            try:
                # Ajouter des scénarios spécifiques basés sur les joueurs clés
                if 'detailed_players' in team_details:
                    players = team_details['detailed_players']
                    
                    # Vérifier les joueurs stars
                    star_players = [p for p in players if (
                        p.get('goals', 0) > 5 or
                        p.get('assists', 0) > 5 or
                        (isinstance(p.get('market_value'), (int, float)) and p.get('market_value', 0) > 20000000) or
                        (isinstance(p.get('market_value'), str) and 'M' in p.get('market_value', ''))
                    )]
                    
                    if star_players and dominant_emotion in ['confidence', 'euphoria']:
                        # Scénario de performance exceptionnelle d'un joueur star
                        star_player = star_players[0]['name'] if len(star_players) > 0 else "Un joueur clé"
                        star_scenario = {
                            'scenario': 'star_performance',
                            'description': f"{star_player} brille particulièrement, porté par la confiance des supporters",
                            'probability': 0.3 + (0.1 * form_factor),
                            'impact_modifier': 0.15
                        }
                        impact_scenarios.append(star_scenario)
                    
                    # Vérifier les joueurs blessés ou revenant de blessure
                    injured_players = [p for p in players if p.get('injury_status')]
                    
                    if injured_players and dominant_emotion in ['anxiety', 'desperation']:
                        # Scénario de rechute ou difficulté d'un joueur revenant de blessure
                        injured_player = injured_players[0]['name'] if len(injured_players) > 0 else "Un joueur fragile"
                        injury_scenario = {
                            'scenario': 'injury_concern',
                            'description': f"La pression affecte la confiance de {injured_player}, limitant son impact",
                            'probability': 0.2,
                            'impact_modifier': -0.1
                        }
                        impact_scenarios.append(injury_scenario)
            except Exception as e:
                logger.warning(f"Erreur lors de l'enrichissement des scénarios: {e}")
        
        # Normaliser les probabilités
        total_probability = sum(scenario['probability'] for scenario in impact_scenarios)
        if total_probability > 0:
            for scenario in impact_scenarios:
                scenario['probability'] = scenario['probability'] / total_probability
        
        return impact_scenarios
    
    def _calculate_enhanced_performance_influence(self, adjusted_impact, current_sentiment, form_factor, team_details=None):
        """
        Calcule l'influence sur la performance en utilisant toutes les données disponibles.
        
        Args:
            adjusted_impact (dict): Impact ajusté du sentiment
            current_sentiment (dict): Analyse du sentiment actuel
            form_factor (float): Facteur de forme de l'équipe
            team_details (dict, optional): Détails de l'équipe
            
        Returns:
            dict: Influence sur la performance
        """
        # Extraire les informations clés
        impact_value = adjusted_impact.get('total_impact', 0.0)
        impact_type = adjusted_impact.get('impact_type', 'neutral')
        
        # Initialiser l'influence sur la performance
        performance_influence = {
            'overall_modifier': impact_value,
            'specific_effects': []
        }
        
        # Déterminer les effets spécifiques en fonction du type d'impact
        if impact_type in ['strong_positive', 'positive']:
            # Effets positifs
            performance_influence['specific_effects'].extend([
                {
                    'aspect': 'energy',
                    'description': "Niveau d'énergie et d'intensité augmenté",
                    'modifier': 0.15 + (impact_value * 0.1)
                },
                {
                    'aspect': 'confidence',
                    'description': "Confiance et prise de risque accrues",
                    'modifier': 0.1 + (impact_value * 0.15)
                },
                {
                    'aspect': 'home_advantage',
                    'description': "Renforcement de l'avantage du terrain",
                    'modifier': 0.1 + (impact_value * 0.1)
                }
            ])
            
        elif impact_type == 'neutral':
            # Effets neutres
            performance_influence['specific_effects'].extend([
                {
                    'aspect': 'standard_performance',
                    'description': "Performance standard, proche du niveau habituel",
                    'modifier': 0.0
                }
            ])
            
        elif impact_type in ['negative', 'strong_negative']:
            # Effets négatifs
            performance_influence['specific_effects'].extend([
                {
                    'aspect': 'pressure',
                    'description': "Pression accrue sur les joueurs",
                    'modifier': -0.1 + (impact_value * 0.1)
                },
                {
                    'aspect': 'decision_making',
                    'description': "Prises de décision plus conservatrices ou précipitées",
                    'modifier': -0.15 + (impact_value * 0.1)
                },
                {
                    'aspect': 'cohesion',
                    'description': "Cohésion d'équipe diminuée",
                    'modifier': -0.1 + (impact_value * 0.1)
                }
            ])
        
        # Ajuster en fonction du facteur de forme
        form_adjustment = (form_factor - 0.5) * 0.2  # Entre -0.1 et +0.1
        performance_influence['form_adjustment'] = form_adjustment
        performance_influence['overall_modifier'] += form_adjustment
        
        # Enrichir avec des effets spécifiques si des données détaillées sont disponibles
        if team_details and self.use_data_hub:
            try:
                # Ajouter des effets spécifiques basés sur les joueurs clés
                if 'detailed_players' in team_details:
                    players = team_details['detailed_players']
                    
                    # Vérifier les joueurs expérimentés
                    experienced_players = [p for p in players if p.get('age', 0) >= 30]
                    young_players = [p for p in players if p.get('age', 0) <= 23]
                    
                    # Les joueurs expérimentés sont moins affectés par le sentiment négatif
                    if experienced_players and len(experienced_players) >= 3 and impact_type in ['negative', 'strong_negative']:
                        performance_influence['specific_effects'].append({
                            'aspect': 'experience',
                            'description': "Les joueurs expérimentés maintiennent leur niveau malgré la pression",
                            'modifier': 0.1
                        })
                    
                    # Les jeunes joueurs sont plus affectés par le sentiment négatif mais aussi plus galvanisés par le positif
                    if young_players and len(young_players) >= 3:
                        if impact_type in ['negative', 'strong_negative']:
                            performance_influence['specific_effects'].append({
                                'aspect': 'youth_pressure',
                                'description': "Les jeunes joueurs ressentent davantage la pression",
                                'modifier': -0.1
                            })
                        elif impact_type in ['positive', 'strong_positive']:
                            performance_influence['specific_effects'].append({
                                'aspect': 'youth_energy',
                                'description': "Les jeunes joueurs sont particulièrement galvanisés par l'ambiance positive",
                                'modifier': 0.15
                            })
                
                # Ajouter des effets basés sur le manager
                if 'detailed_manager' in team_details:
                    manager = team_details['detailed_manager']
                    
                    # Les managers expérimentés gèrent mieux la pression
                    if manager.get('games_total', 0) > 100 and impact_type in ['negative', 'strong_negative']:
                        performance_influence['specific_effects'].append({
                            'aspect': 'manager_experience',
                            'description': "Le manager expérimenté aide l'équipe à gérer la pression",
                            'modifier': 0.1
                        })
            except Exception as e:
                logger.warning(f"Erreur lors de l'enrichissement des effets de performance: {e}")
        
        # Calculer l'effet global final
        total_modifier = performance_influence['overall_modifier']
        for effect in performance_influence['specific_effects']:
            total_modifier += effect.get('modifier', 0)
        
        # Limiter le modificateur global
        performance_influence['final_modifier'] = max(-0.5, min(0.5, total_modifier))
        
        return performance_influence
    
    def _calculate_enhanced_sentiment_effect_duration(self, emotion, intensity, match_result, match_data, team_details=None):
        """
        Calcule la durée prévue de l'effet du sentiment après un match,
        en utilisant toutes les données disponibles.
        
        Args:
            emotion (str): Émotion dominante post-match
            intensity (float): Intensité du sentiment post-match
            match_result (str): Résultat du match ('win', 'loss', 'draw')
            match_data (dict): Données du match
            team_details (dict, optional): Détails de l'équipe
            
        Returns:
            dict: Durée prévue de l'effet
        """
        # Durée de base en jours
        base_duration = 3.0  # Durée par défaut
        
        # Ajuster en fonction de l'émotion
        emotion_factor = 1.0  # Facteur neutre par défaut
        if emotion == 'euphoria':
            emotion_factor = 1.5
        elif emotion == 'disappointment':
            emotion_factor = 1.2
        elif emotion == 'anger':
            emotion_factor = 0.8
        elif emotion == 'anxiety':
            emotion_factor = 1.0
        
        # Ajuster en fonction de l'intensité
        intensity_factor = 0.5 + intensity
        
        # Ajuster en fonction du résultat
        result_factor = 1.0  # Facteur neutre par défaut
        if match_result == 'win':
            result_factor = 1.2
        elif match_result == 'loss':
            result_factor = 1.1
        
        # Calculer la durée ajustée
        adjusted_duration = base_duration * emotion_factor * intensity_factor * result_factor
        
        # Enrichir l'analyse si des données détaillées sont disponibles
        if team_details and self.use_data_hub:
            try:
                # La fidélité des supporters peut prolonger l'effet
                if 'transfermarkt_data' in team_details:
                    tm_data = team_details['transfermarkt_data']
                    
                    # Un club plus ancien a généralement des supporters plus fidèles
                    if 'founded' in tm_data:
                        try:
                            founded_year = int(tm_data['founded'])
                            years_existing = datetime.now().year - founded_year
                            
                            # Plus le club est ancien, plus l'effet dure
                            if years_existing > 100:
                                adjusted_duration *= 1.2
                            elif years_existing > 50:
                                adjusted_duration *= 1.1
                        except (ValueError, TypeError):
                            pass
                    
                    # Un stade plus grand signifie une base de supporters plus large
                    if 'stadium' in tm_data and 'capacity' in tm_data['stadium']:
                        capacity = tm_data['stadium']['capacity']
                        
                        # Plus le stade est grand, plus l'effet peut être durable
                        if capacity > 60000:
                            adjusted_duration *= 1.15
                        elif capacity > 40000:
                            adjusted_duration *= 1.1
                
                # La présence sur les réseaux sociaux amplifie et prolonge les réactions
                if 'transfermarkt_data' in team_details and 'social' in team_details['transfermarkt_data']:
                    social = team_details['transfermarkt_data']['social']
                    total_followers = (
                        social.get('twitter_followers', 0) +
                        social.get('facebook_likes', 0) +
                        social.get('instagram_followers', 0)
                    )
                    
                    # Plus il y a de followers, plus l'effet dure
                    if total_followers > 10000000:  # 10M+
                        adjusted_duration *= 1.3
                    elif total_followers > 5000000:  # 5M+
                        adjusted_duration *= 1.2
                    elif total_followers > 1000000:  # 1M+
                        adjusted_duration *= 1.1
                
                # Les résultats récents peuvent atténuer ou amplifier l'effet
                if 'form' in team_details and isinstance(team_details['form'], dict) and 'data' in team_details['form']:
                    form_data = team_details['form']['data']
                    
                    if isinstance(form_data, list) and len(form_data) > 0:
                        recent_results = []
                        for match in form_data[:5]:  # 5 derniers matchs
                            if 'result' in match:
                                recent_results.append(match['result'])
                        
                        if recent_results:
                            wins = recent_results.count('W')
                            losses = recent_results.count('L')
                            
                            # Une série de résultats identiques renforce l'effet
                            if match_result == 'win' and wins >= 3:
                                adjusted_duration *= 1.1  # Série de victoires renforce l'euphorie
                            elif match_result == 'loss' and losses >= 3:
                                adjusted_duration *= 1.2  # Série de défaites renforce la déception
                            # Un résultat qui rompt une série a un effet plus fort
                            elif match_result == 'win' and losses >= 3:
                                adjusted_duration *= 1.3  # Victoire qui rompt une série de défaites
                            elif match_result == 'loss' and wins >= 3:
                                adjusted_duration *= 1.4  # Défaite qui rompt une série de victoires
            except Exception as e:
                logger.warning(f"Erreur lors de l'enrichissement de la durée de l'effet: {e}")
        
        # Déterminer les facteurs qui affectent la durée
        affecting_factors = []
        
        # Facteur émotionnel
        if emotion_factor > 1.1:
            affecting_factors.append({
                'factor': 'emotion',
                'description': f"L'émotion de {emotion} tend à persister",
                'impact': 'increase',
                'magnitude': emotion_factor
            })
        elif emotion_factor < 0.9:
            affecting_factors.append({
                'factor': 'emotion',
                'description': f"L'émotion de {emotion} tend à se dissiper rapidement",
                'impact': 'decrease',
                'magnitude': emotion_factor
            })
        
        # Facteur d'intensité
        if intensity > 0.7:
            affecting_factors.append({
                'factor': 'intensity',
                'description': "Forte intensité émotionnelle",
                'impact': 'increase',
                'magnitude': intensity_factor
            })
        elif intensity < 0.4:
            affecting_factors.append({
                'factor': 'intensity',
                'description': "Faible intensité émotionnelle",
                'impact': 'decrease',
                'magnitude': intensity_factor
            })
        
        # Facteur de résultat
        if result_factor > 1.1:
            affecting_factors.append({
                'factor': 'result',
                'description': f"L'impact d'une {match_result} tend à persister",
                'impact': 'increase',
                'magnitude': result_factor
            })
        
        # Compiler la durée prévue
        expected_duration = {
            'days': round(adjusted_duration, 1),
            'intensity_decay': {
                'initial': intensity,
                'after_1_day': intensity * 0.8,
                'after_3_days': intensity * 0.5,
                'after_7_days': intensity * 0.2
            },
            'affecting_factors': affecting_factors
        }
        
        return expected_duration
    
    def _predict_enhanced_future_impact(self, team_name, post_match_emotion, post_match_intensity, sentiment_shift, match_result, team_details=None):
        """
        Prédit l'impact futur du sentiment post-match, en utilisant toutes les données disponibles.
        
        Args:
            team_name (str): Nom de l'équipe
            post_match_emotion (str): Émotion dominante post-match
            post_match_intensity (float): Intensité du sentiment post-match
            sentiment_shift (dict): Analyse du changement de sentiment
            match_result (str): Résultat du match ('win', 'loss', 'draw')
            team_details (dict, optional): Détails de l'équipe
            
        Returns:
            dict: Prédiction de l'impact futur
        """
        # Calculer l'impact de base sur le prochain match
        next_match_impact = 0.0
        
        # Ajuster en fonction de l'émotion post-match
        if post_match_emotion == 'euphoria':
            next_match_impact = 0.15
        elif post_match_emotion == 'confidence':
            next_match_impact = 0.1
        elif post_match_emotion == 'disappointment':
            next_match_impact = -0.1
        elif post_match_emotion == 'anger':
            next_match_impact = -0.15
        elif post_match_emotion == 'anxiety':
            next_match_impact = -0.1
        
        # Ajuster en fonction de l'intensité
        next_match_impact *= post_match_intensity
        
        # Ajuster en fonction de l'ampleur du changement de sentiment
        shift_magnitude = sentiment_shift.get('magnitude', 0.0)
        if shift_magnitude > 0.5:
            # Un grand changement a un impact plus fort
            next_match_impact *= 1.2
        
        # Enrichir l'analyse si des données détaillées sont disponibles
        upcoming_matches = []
        if team_details and self.use_data_hub:
            try:
                # Récupérer les matchs à venir si disponibles
                if 'transfermarkt_data' in team_details and 'fixtures' in team_details['transfermarkt_data']:
                    fixtures = team_details['transfermarkt_data']['fixtures']
                    
                    if isinstance(fixtures, list) and len(fixtures) > 0:
                        for fixture in fixtures[:3]:  # 3 prochains matchs
                            upcoming_matches.append({
                                'opponent': fixture.get('opponent', {}).get('name', 'Inconnu'),
                                'date': fixture.get('date', ''),
                                'is_home': fixture.get('isHome', False),
                                'competition': fixture.get('competition', {}).get('name', 'Inconnu')
                            })
                
                # La résilience de l'équipe peut affecter l'impact futur
                if match_result == 'loss' and 'form' in team_details and isinstance(team_details['form'], dict) and 'data' in team_details['form']:
                    form_data = team_details['form']['data']
                    
                    if isinstance(form_data, list) and len(form_data) > 1:
                        # Vérifier comment l'équipe rebondit habituellement après une défaite
                        bounce_back_wins = 0
                        total_after_loss = 0
                        
                        for i in range(1, len(form_data)):
                            prev_match = form_data[i-1]
                            current_match = form_data[i]
                            
                            if prev_match.get('result') == 'L' and current_match.get('result') == 'W':
                                bounce_back_wins += 1
                                total_after_loss += 1
                            elif prev_match.get('result') == 'L':
                                total_after_loss += 1
                        
                        if total_after_loss > 0:
                            bounce_back_ratio = bounce_back_wins / total_after_loss
                            
                            # Si l'équipe rebondit bien après les défaites, l'impact négatif est réduit
                            if bounce_back_ratio > 0.6:
                                next_match_impact *= 0.7  # Réduction de l'impact négatif
                                
                                # Ajouter un facteur de résilience
                                resilience_factor = {
                                    'factor': 'team_resilience',
                                    'description': f"{team_name} rebondit généralement bien après une défaite",
                                    'bounce_back_ratio': bounce_back_ratio,
                                    'impact': 'positive',
                                    'magnitude': 0.3
                                }
            except Exception as e:
                logger.warning(f"Erreur lors de l'enrichissement de l'impact futur: {e}")
        
        # Déterminer les facteurs qui affectent l'impact futur
        impact_factors = []
        
        # Facteur émotionnel
        impact_factors.append({
            'factor': 'post_match_emotion',
            'description': f"L'émotion dominante de {post_match_emotion} après le match",
            'impact': 'positive' if next_match_impact > 0 else 'negative',
            'magnitude': abs(next_match_impact / post_match_intensity)
        })
        
        # Facteur d'intensité
        impact_factors.append({
            'factor': 'emotional_intensity',
            'description': f"Intensité émotionnelle post-match: {post_match_intensity:.2f}",
            'impact': 'amplifier',
            'magnitude': post_match_intensity
        })
        
        # Facteur de changement de sentiment
        if shift_magnitude > 0.3:
            impact_factors.append({
                'factor': 'sentiment_shift',
                'description': f"Changement important du sentiment (magnitude: {shift_magnitude:.2f})",
                'impact': 'amplifier',
                'magnitude': shift_magnitude
            })
        
        # Compiler la prédiction d'impact futur
        future_impact = {
            'next_match_impact': next_match_impact,
            'impact_factors': impact_factors,
            'upcoming_matches': upcoming_matches,
            'recovery_trajectory': {
                'initial': next_match_impact,
                'after_1_match': next_match_impact * 0.7,
                'after_2_matches': next_match_impact * 0.4,
                'after_3_matches': next_match_impact * 0.2
            }
        }
        
        # Ajouter le facteur de résilience si présent
        if 'resilience_factor' in locals():
            future_impact['impact_factors'].append(resilience_factor)
        
        return future_impact
    
    def _extract_sentiment_insights(self, advanced_insights):
        """
        Extrait des insights pertinents pour l'analyse de sentiment à partir des insights avancés.
        
        Args:
            advanced_insights (dict): Insights avancés générés par le module d'analyse avancée
            
        Returns:
            list: Insights pertinents pour l'analyse de sentiment
        """
        sentiment_insights = []
        
        try:
            # Extraire les forces de l'équipe qui peuvent influencer le sentiment
            team_strengths = advanced_insights.get('team_strengths', [])
            for strength in team_strengths:
                if strength.get('type') in ['attacking', 'set_pieces', 'possession'] and strength.get('confidence', 0) > 0.6:
                    sentiment_insights.append({
                        'type': 'team_strength',
                        'title': strength.get('title', 'Force'),
                        'description': strength.get('description', ''),
                        'impact': 'positive',
                        'confidence': strength.get('confidence', 0.5)
                    })
            
            # Extraire les faiblesses de l'équipe qui peuvent influencer le sentiment
            team_weaknesses = advanced_insights.get('team_weaknesses', [])
            for weakness in team_weaknesses:
                if weakness.get('type') in ['defending', 'injuries', 'discipline'] and weakness.get('confidence', 0) > 0.6:
                    sentiment_insights.append({
                        'type': 'team_weakness',
                        'title': weakness.get('title', 'Faiblesse'),
                        'description': weakness.get('description', ''),
                        'impact': 'negative',
                        'confidence': weakness.get('confidence', 0.5)
                    })
            
            # Extraire les tendances historiques qui peuvent influencer le sentiment
            historical_trends = advanced_insights.get('historical_trends', [])
            for trend in historical_trends:
                if trend.get('type') in ['recent_form', 'home_form', 'away_form'] and trend.get('confidence', 0) > 0.6:
                    sentiment_insights.append({
                        'type': 'historical_trend',
                        'title': trend.get('title', 'Tendance'),
                        'description': trend.get('description', ''),
                        'impact': 'positive' if 'bonne' in trend.get('description', '').lower() or 'force' in trend.get('description', '').lower() else 'negative',
                        'confidence': trend.get('confidence', 0.5)
                    })
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction des insights de sentiment: {e}")
        
        return sentiment_insights
    
    # Méthodes d'helpers originales et autres méthodes d'analyse
    # À implémenter selon les besoins
    
    # Méthode fallback pour la compatibilité, utilise la nouvelle méthode améliorée
    def analyze_current_sentiment_legacy(self, team_name, match_data=None, sentiment_data=None):
        """Méthode de compatibilité avec l'ancienne API"""
        return self.analyze_current_sentiment(team_name, match_data, sentiment_data)
    
    def predict_sentiment_impact_legacy(self, team_name, match_data, recent_form=None):
        """Méthode de compatibilité avec l'ancienne API"""
        return self.predict_sentiment_impact(team_name, match_data, recent_form)
    
    def analyze_sentiment_response_legacy(self, team_name, match_data, result_data, pre_match_sentiment=None):
        """Méthode de compatibilité avec l'ancienne API"""
        return self.analyze_sentiment_response(team_name, match_data, result_data, pre_match_sentiment)