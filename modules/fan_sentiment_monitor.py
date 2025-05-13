"""
FanSentimentMonitor - Module d'analyse de l'influence des émotions collectives.
Surveille et analyse le sentiment des supporters pour prédire son impact sur les performances.
"""

import random
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict

class FanSentimentMonitor:
    """
    FanSentimentMonitor - Système d'analyse de l'influence des émotions collectives des supporters.
    Mesure l'impact des sentiments de masse sur les performances des équipes.
    """
    
    def __init__(self):
        """Initialise le module FanSentimentMonitor"""
        # Paramètres d'analyse
        self.sentiment_parameters = {
            'emotional_impact': 0.3,      # Impact des émotions sur la performance
            'collective_resonance': 0.65,  # Force de la résonance collective
            'threshold_critical_mass': 0.7, # Seuil pour atteindre la masse critique
            'home_advantage_factor': 0.25, # Facteur d'avantage à domicile supplémentaire
            'temporal_decay': 0.85         # Décroissance temporelle du sentiment
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
        
        # Historique des analyses
        self.analysis_history = []
        
        # Cache de sentiment
        self.sentiment_cache = {}
        
    def analyze_current_sentiment(self, team_name, match_data=None, sentiment_data=None):
        """
        Analyser le sentiment actuel des supporters d'une équipe.
        
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
                sentiment_data = self._generate_sentiment_data(team_name)
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
            source_analyses[source] = self._analyze_sentiment_source(
                source, source_data, source_config, team_name
            )
        
        # Calculer le sentiment dominant
        dominant_emotion, emotion_scores = self._calculate_dominant_emotion(source_analyses)
        
        # Calculer l'intensité globale
        overall_intensity = self._calculate_overall_intensity(source_analyses)
        
        # Évaluer la cohésion du sentiment
        sentiment_cohesion = self._evaluate_sentiment_cohesion(source_analyses)
        
        # Analyser les tendances récentes
        trend_analysis = self._analyze_sentiment_trends(team_name)
        
        # Analyser le contexte du match si disponible
        match_influence = None
        if match_context:
            match_influence = self._analyze_match_influence(match_context, dominant_emotion, overall_intensity)
        
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
                dominant_emotion, overall_intensity, sentiment_cohesion, match_context
            )
        }
        
        if match_influence:
            analysis['match_influence'] = match_influence
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'current_sentiment_analysis',
            'timestamp': datetime.now().isoformat(),
            'team': team_name,
            'summary': {
                'dominant_emotion': dominant_emotion,
                'intensity': overall_intensity,
                'cohesion': sentiment_cohesion.get('overall_cohesion', 0)
            }
        })
        
        return analysis
    
    def predict_sentiment_impact(self, team_name, match_data, recent_form=None):
        """
        Prédire l'impact du sentiment des supporters sur un match à venir.
        
        Args:
            team_name (str): Nom de l'équipe
            match_data (dict): Données du match à venir
            recent_form (list, optional): Forme récente de l'équipe
            
        Returns:
            dict: Prédiction de l'impact du sentiment
        """
        # Analyser le sentiment actuel
        current_sentiment = self.analyze_current_sentiment(team_name, match_data)
        
        # Extraire le nom de l'adversaire
        opponent_name = match_data.get('away_team') if match_data.get('home_team') == team_name else match_data.get('home_team')
        
        # Calculer l'importance du match
        match_importance = self._calculate_match_importance(match_data)
        
        # Déterminer si le match est à domicile
        is_home = match_data.get('home_team') == team_name
        
        # Analyser la forme récente si fournie
        form_factor = 0.5  # Valeur neutre par défaut
        if recent_form:
            form_factor = self._analyze_recent_form(recent_form)
        
        # Calculer l'avantage ou désavantage sentimental de base
        base_impact = self._calculate_base_sentiment_impact(
            current_sentiment, match_importance, is_home
        )
        
        # Ajuster en fonction de facteurs spécifiques au match
        specific_factors = self._analyze_specific_factors(team_name, opponent_name, match_data)
        
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
        impact_scenarios = self._generate_impact_scenarios(adjusted_impact, form_factor)
        
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
            'performance_influence': self._calculate_performance_influence(
                adjusted_impact, current_sentiment, form_factor
            )
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'sentiment_impact_prediction',
            'timestamp': datetime.now().isoformat(),
            'team': team_name,
            'opponent': opponent_name,
            'match_date': match_data.get('date', datetime.now().isoformat()),
            'summary': {
                'impact_type': adjusted_impact.get('impact_type'),
                'total_impact': adjusted_impact.get('total_impact'),
                'dominant_emotion': current_sentiment.get('dominant_emotion')
            }
        })
        
        return prediction
    
    def analyze_sentiment_response(self, team_name, match_data, result_data, pre_match_sentiment=None):
        """
        Analyser la réponse sentimentale à un résultat de match.
        
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
                if (analysis.get('type') == 'sentiment_impact_prediction' and 
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
        
        # Générer les données de réponse sentimentale
        response_data = self._generate_response_data(team_name, match_result, pre_match_sentiment)
        
        # Analyser chaque source de sentiment
        source_analyses = {}
        for source, source_config in self.sentiment_sources.items():
            source_data = response_data.get(source, {})
            source_analyses[source] = self._analyze_sentiment_source(
                source, source_data, source_config, team_name, is_response=True
            )
        
        # Calculer le sentiment dominant après le match
        post_match_emotion, emotion_scores = self._calculate_dominant_emotion(source_analyses)
        
        # Calculer l'intensité globale
        post_match_intensity = self._calculate_overall_intensity(source_analyses)
        
        # Analyser le changement par rapport au sentiment pré-match
        sentiment_shift = self._analyze_sentiment_shift(
            pre_match_sentiment.get('dominant_emotion'),
            post_match_emotion,
            pre_match_sentiment.get('overall_intensity', 0.7),
            post_match_intensity
        )
        
        # Analyser la volatilité du sentiment
        sentiment_volatility = self._analyze_sentiment_volatility(source_analyses)
        
        # Calculer la durée prévue de l'effet
        expected_duration = self._calculate_sentiment_effect_duration(
            post_match_emotion, post_match_intensity, match_result, match_data
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
            'future_impact': self._predict_future_impact(
                team_name, post_match_emotion, post_match_intensity, sentiment_shift, match_result
            )
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'sentiment_response_analysis',
            'timestamp': datetime.now().isoformat(),
            'team': team_name,
            'match_date': match_data.get('date'),
            'match_result': match_result,
            'summary': {
                'post_match_emotion': post_match_emotion,
                'intensity': post_match_intensity,
                'shift_magnitude': sentiment_shift.get('magnitude')
            }
        })
        
        return analysis
    
    def analyze_long_term_sentiment(self, team_name, timeframe='season', historical_data=None):
        """
        Analyser le sentiment à long terme pour une équipe.
        
        Args:
            team_name (str): Nom de l'équipe
            timeframe (str): Période d'analyse ('season', 'year', 'multi_year')
            historical_data (dict, optional): Données historiques si disponibles
            
        Returns:
            dict: Analyse du sentiment à long terme
        """
        # Générer ou utiliser des données historiques
        if historical_data is None:
            historical_data = self._generate_historical_data(team_name, timeframe)
        
        # Analyser les cycles de sentiment
        sentiment_cycles = self._analyze_sentiment_cycles(historical_data)
        
        # Analyser la stabilité du sentiment
        sentiment_stability = self._analyze_sentiment_stability(historical_data)
        
        # Analyser les corrélations avec la performance
        performance_correlations = self._analyze_performance_correlations(historical_data)
        
        # Identifier les points de bascule
        tipping_points = self._identify_sentiment_tipping_points(historical_data)
        
        # Analyser les facteurs externes d'influence
        external_factors = self._analyze_external_influence_factors(historical_data)
        
        # Calculer le sentiment de base
        baseline_sentiment = self._calculate_baseline_sentiment(historical_data)
        
        # Compiler l'analyse complète
        analysis = {
            'team_name': team_name,
            'timeframe': timeframe,
            'analysis_timestamp': datetime.now().isoformat(),
            'sentiment_cycles': sentiment_cycles,
            'sentiment_stability': sentiment_stability,
            'performance_correlations': performance_correlations,
            'tipping_points': tipping_points,
            'external_factors': external_factors,
            'baseline_sentiment': baseline_sentiment,
            'long_term_projection': self._generate_long_term_projection(
                team_name, historical_data, sentiment_cycles, sentiment_stability
            )
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'long_term_sentiment_analysis',
            'timestamp': datetime.now().isoformat(),
            'team': team_name,
            'timeframe': timeframe,
            'summary': {
                'baseline_emotion': baseline_sentiment.get('dominant_emotion'),
                'stability_score': sentiment_stability.get('overall_stability'),
                'cycle_count': len(sentiment_cycles.get('identified_cycles', []))
            }
        })
        
        return analysis
    
    def compare_team_sentiments(self, team1_name, team2_name, context=None):
        """
        Comparer le sentiment des supporters de deux équipes.
        
        Args:
            team1_name (str): Nom de la première équipe
            team2_name (str): Nom de la deuxième équipe
            context (dict, optional): Contexte de la comparaison (ex: match à venir)
            
        Returns:
            dict: Analyse comparative des sentiments
        """
        # Analyser le sentiment actuel de chaque équipe
        team1_sentiment = self.analyze_current_sentiment(team1_name, context)
        team2_sentiment = self.analyze_current_sentiment(team2_name, context)
        
        # Comparer les émotions dominantes
        emotion_comparison = self._compare_dominant_emotions(
            team1_sentiment.get('dominant_emotion'),
            team2_sentiment.get('dominant_emotion'),
            team1_sentiment.get('emotion_scores', {}),
            team2_sentiment.get('emotion_scores', {})
        )
        
        # Comparer les intensités
        intensity_comparison = self._compare_intensities(
            team1_sentiment.get('overall_intensity', 0),
            team2_sentiment.get('overall_intensity', 0)
        )
        
        # Comparer les cohésions de sentiment
        cohesion_comparison = self._compare_cohesions(
            team1_sentiment.get('sentiment_cohesion', {}).get('overall_cohesion', 0),
            team2_sentiment.get('sentiment_cohesion', {}).get('overall_cohesion', 0)
        )
        
        # Analyser l'interaction des sentiments
        sentiment_interaction = self._analyze_sentiment_interaction(
            team1_sentiment, team2_sentiment
        )
        
        # Déterminer l'avantage sentimental
        sentiment_advantage = self._determine_sentiment_advantage(
            team1_name, team2_name, team1_sentiment, team2_sentiment, context
        )
        
        # Compiler l'analyse comparative
        comparison = {
            'team1': {
                'name': team1_name,
                'dominant_emotion': team1_sentiment.get('dominant_emotion'),
                'overall_intensity': team1_sentiment.get('overall_intensity'),
                'cohesion': team1_sentiment.get('sentiment_cohesion', {}).get('overall_cohesion', 0)
            },
            'team2': {
                'name': team2_name,
                'dominant_emotion': team2_sentiment.get('dominant_emotion'),
                'overall_intensity': team2_sentiment.get('overall_intensity'),
                'cohesion': team2_sentiment.get('sentiment_cohesion', {}).get('overall_cohesion', 0)
            },
            'emotion_comparison': emotion_comparison,
            'intensity_comparison': intensity_comparison,
            'cohesion_comparison': cohesion_comparison,
            'sentiment_interaction': sentiment_interaction,
            'sentiment_advantage': sentiment_advantage,
            'comparison_timestamp': datetime.now().isoformat()
        }
        
        # Ajouter des informations de contexte si disponibles
        if context:
            comparison['context'] = {
                'type': context.get('type', 'general'),
                'match_date': context.get('date', ''),
                'importance': context.get('importance', 'regular')
            }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'team_sentiment_comparison',
            'timestamp': datetime.now().isoformat(),
            'teams': [team1_name, team2_name],
            'summary': {
                'advantage_team': sentiment_advantage.get('team'),
                'advantage_magnitude': sentiment_advantage.get('magnitude'),
                'interaction_type': sentiment_interaction.get('type')
            }
        })
        
        return comparison
    
    def _analyze_sentiment_source(self, source_name, source_data, source_config, team_name, is_response=False):
        """Analyser une source spécifique de sentiment."""
        # Base de l'analyse
        analysis = {
            'source_name': source_name,
            'sentiment_by_emotion': {},
            'overall_sentiment': 0.0,
            'reliability': 0.7,  # Valeur par défaut
            'metrics': {}
        }
        
        # Analyser les métriques disponibles pour cette source
        for metric in source_config.get('metrics', []):
            if metric in source_data:
                metric_value = source_data[metric]
                analysis['metrics'][metric] = metric_value
        
        # Analyser le sentiment pour chaque émotion
        emotion_data = source_data.get('emotions', {})
        for emotion in self.collective_emotions:
            if emotion in emotion_data:
                analysis['sentiment_by_emotion'][emotion] = emotion_data[emotion]
        
        # Si aucune donnée d'émotion n'est disponible, utiliser des valeurs par défaut
        if not analysis['sentiment_by_emotion']:
            if is_response:
                # Pour les analyses de réponse, simuler des sentiments plus prononcés
                primary_emotion = random.choice(self.collective_emotions)
                analysis['sentiment_by_emotion'] = {
                    emotion: 0.2 + (0.6 if emotion == primary_emotion else 0.0) + random.uniform(0, 0.2)
                    for emotion in self.collective_emotions
                }
            else:
                # Pour les analyses normales, utiliser une distribution plus équilibrée
                analysis['sentiment_by_emotion'] = {
                    emotion: random.uniform(0.2, 0.8)
                    for emotion in self.collective_emotions
                }
        
        # Calculer le sentiment global
        if analysis['sentiment_by_emotion']:
            analysis['overall_sentiment'] = sum(analysis['sentiment_by_emotion'].values()) / len(analysis['sentiment_by_emotion'])
        
        # Calculer la fiabilité
        analysis['reliability'] = self._calculate_source_reliability(source_name, analysis['metrics'])
        
        return analysis
    
    def _calculate_dominant_emotion(self, source_analyses):
        """Calculer l'émotion dominante à partir des analyses de sources."""
        # Initialiser les scores pour chaque émotion
        emotion_scores = {emotion: 0.0 for emotion in self.collective_emotions}
        
        # Agréger les scores de toutes les sources
        total_weight = 0.0
        for source, analysis in source_analyses.items():
            source_weight = self.sentiment_sources.get(source, {}).get('weight', 0.25)
            source_reliability = analysis.get('reliability', 0.7)
            
            # Ajuster le poids par la fiabilité
            adjusted_weight = source_weight * source_reliability
            total_weight += adjusted_weight
            
            # Ajouter les scores d'émotions
            for emotion, score in analysis.get('sentiment_by_emotion', {}).items():
                if emotion in emotion_scores:
                    emotion_scores[emotion] += score * adjusted_weight
        
        # Normaliser les scores
        if total_weight > 0:
            for emotion in emotion_scores:
                emotion_scores[emotion] /= total_weight
        
        # Trouver l'émotion dominante
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        
        return dominant_emotion, emotion_scores
    
    def _calculate_overall_intensity(self, source_analyses):
        """Calculer l'intensité globale du sentiment."""
        # Calculer une moyenne pondérée des intensités
        total_intensity = 0.0
        total_weight = 0.0
        
        for source, analysis in source_analyses.items():
            source_weight = self.sentiment_sources.get(source, {}).get('weight', 0.25)
            source_reliability = analysis.get('reliability', 0.7)
            
            # Ajuster le poids par la fiabilité
            adjusted_weight = source_weight * source_reliability
            total_weight += adjusted_weight
            
            # Utiliser l'intensité moyenne des émotions comme intensité de la source
            source_intensity = sum(analysis.get('sentiment_by_emotion', {}).values()) / max(1, len(analysis.get('sentiment_by_emotion', {})))
            
            total_intensity += source_intensity * adjusted_weight
        
        # Normaliser l'intensité
        if total_weight > 0:
            overall_intensity = total_intensity / total_weight
        else:
            overall_intensity = 0.5  # Valeur par défaut
        
        return overall_intensity
    
    def _evaluate_sentiment_cohesion(self, source_analyses):
        """Évaluer la cohésion du sentiment entre les différentes sources."""
        # Base de l'évaluation
        evaluation = {
            'overall_cohesion': 0.0,
            'source_alignment': {},
            'emotion_variance': {}
        }
        
        # Calculer la variance des émotions entre les sources
        for emotion in self.collective_emotions:
            emotion_scores = []
            for source, analysis in source_analyses.items():
                if emotion in analysis.get('sentiment_by_emotion', {}):
                    emotion_scores.append(analysis['sentiment_by_emotion'][emotion])
            
            if emotion_scores:
                evaluation['emotion_variance'][emotion] = np.var(emotion_scores)
        
        # Calculer l'alignement entre les sources
        sources = list(source_analyses.keys())
        for i in range(len(sources)):
            for j in range(i+1, len(sources)):
                source1, source2 = sources[i], sources[j]
                
                alignment = self._calculate_source_alignment(
                    source_analyses[source1], source_analyses[source2]
                )
                
                alignment_key = f"{source1}_vs_{source2}"
                evaluation['source_alignment'][alignment_key] = alignment
        
        # Calculer la cohésion globale
        if evaluation['emotion_variance']:
            avg_variance = sum(evaluation['emotion_variance'].values()) / len(evaluation['emotion_variance'])
            evaluation['overall_cohesion'] = 1.0 - min(1.0, avg_variance * 2)
        else:
            evaluation['overall_cohesion'] = 0.5  # Valeur par défaut
        
        return evaluation
    
    def _analyze_sentiment_trends(self, team_name):
        """Analyser les tendances récentes du sentiment."""
        # Base de l'analyse
        trend_analysis = {
            'recent_direction': 'stable',
            'trend_strength': 0.0,
            'significant_shifts': [],
            'prediction': {}
        }
        
        # Récupérer les analyses récentes pour cette équipe
        recent_analyses = []
        for analysis in self.analysis_history:
            if analysis.get('team') == team_name and analysis.get('type') in ['current_sentiment_analysis', 'sentiment_response_analysis']:
                recent_analyses.append(analysis)
        
        # Trier par date
        recent_analyses.sort(key=lambda a: a.get('timestamp', ''))
        
        # Si peu d'analyses sont disponibles, retourner une analyse limitée
        if len(recent_analyses) < 3:
            trend_analysis['prediction'] = {
                'confidence': 'low',
                'next_direction': 'uncertain',
                'explanation': "Données historiques insuffisantes pour une prédiction fiable"
            }
            return trend_analysis
        
        # Analyser la direction récente
        recent_intensities = [a.get('summary', {}).get('intensity', 0.5) for a in recent_analyses[-3:]]
        if len(recent_intensities) >= 2:
            if recent_intensities[-1] > recent_intensities[-2] * 1.1:
                trend_analysis['recent_direction'] = 'increasing'
                trend_analysis['trend_strength'] = (recent_intensities[-1] - recent_intensities[-2]) / recent_intensities[-2]
            elif recent_intensities[-1] < recent_intensities[-2] * 0.9:
                trend_analysis['recent_direction'] = 'decreasing'
                trend_analysis['trend_strength'] = (recent_intensities[-2] - recent_intensities[-1]) / recent_intensities[-2]
            else:
                trend_analysis['recent_direction'] = 'stable'
                trend_analysis['trend_strength'] = 0.1
        
        # Identifier les changements significatifs
        for i in range(1, len(recent_analyses)):
            prev = recent_analyses[i-1].get('summary', {})
            curr = recent_analyses[i].get('summary', {})
            
            prev_emotion = prev.get('dominant_emotion', '')
            curr_emotion = curr.get('dominant_emotion', '')
            
            prev_intensity = prev.get('intensity', 0.5)
            curr_intensity = curr.get('intensity', 0.5)
            
            # Si l'émotion a changé ou l'intensité a beaucoup varié
            if prev_emotion != curr_emotion or abs(curr_intensity - prev_intensity) > 0.2:
                trend_analysis['significant_shifts'].append({
                    'timestamp': recent_analyses[i].get('timestamp', ''),
                    'from_emotion': prev_emotion,
                    'to_emotion': curr_emotion,
                    'intensity_change': curr_intensity - prev_intensity,
                    'trigger': self._identify_shift_trigger(recent_analyses[i])
                })
        
        # Générer une prédiction
        trend_analysis['prediction'] = self._predict_sentiment_trend(
            recent_analyses, trend_analysis['recent_direction'], trend_analysis['trend_strength']
        )
        
        return trend_analysis
    
    def _analyze_match_influence(self, match_context, dominant_emotion, overall_intensity):
        """Analyser l'influence du contexte du match sur le sentiment."""
        # Base de l'analyse
        influence = {
            'match_magnifier': 1.0,
            'home_advantage': 0.0,
            'rivalry_factor': 0.0,
            'importance_effect': 0.0,
            'total_influence': 0.0
        }
        
        # Ajuster pour les matchs à domicile
        if match_context.get('is_home', False):
            influence['home_advantage'] = self.sentiment_parameters['home_advantage_factor']
        
        # Ajuster pour l'importance du match
        importance = match_context.get('importance', 'regular')
        if importance == 'critical':
            influence['importance_effect'] = 0.3
        elif importance == 'high':
            influence['importance_effect'] = 0.2
        elif importance == 'derby':
            influence['importance_effect'] = 0.25
            influence['rivalry_factor'] = 0.2
        
        # Calculer le magnifieur global
        influence['match_magnifier'] = 1.0 + influence['home_advantage'] + influence['importance_effect'] + influence['rivalry_factor']
        
        # Déterminer l'influence totale
        influence['total_influence'] = (
            influence['match_magnifier'] * overall_intensity - 0.5
        ) * 2  # Normaliser entre -1 et 1
        
        # Limiter l'influence totale
        influence['total_influence'] = max(-1.0, min(1.0, influence['total_influence']))
        
        return influence
    
    def _calculate_expected_impact(self, dominant_emotion, overall_intensity, sentiment_cohesion, match_context=None):
        """Calculer l'impact attendu sur la performance."""
        # Base du calcul
        impact = {
            'performance_factor': 0.0,
            'psychological_effect': '',
            'probability': 0.5,
            'confidence': 'medium'
        }
        
        # Facteur de base selon l'émotion
        base_factor = 0.0
        if dominant_emotion == 'euphoria':
            base_factor = 0.3
            impact['psychological_effect'] = 'boost_confidence'
        elif dominant_emotion == 'anxiety':
            base_factor = -0.2
            impact['psychological_effect'] = 'increase_pressure'
        elif dominant_emotion == 'anger':
            base_factor = 0.1  # Peut être positif ou négatif
            impact['psychological_effect'] = 'heighten_aggression'
        elif dominant_emotion == 'confidence':
            base_factor = 0.25
            impact['psychological_effect'] = 'enhance_composure'
        elif dominant_emotion == 'desperation':
            base_factor = -0.15
            impact['psychological_effect'] = 'create_urgency'
        elif dominant_emotion == 'nostalgia':
            base_factor = 0.05
            impact['psychological_effect'] = 'inspire_connection'
        elif dominant_emotion == 'anticipation':
            base_factor = 0.15
            impact['psychological_effect'] = 'increase_focus'
        elif dominant_emotion == 'disappointment':
            base_factor = -0.25
            impact['psychological_effect'] = 'undermine_motivation'
        
        # Ajuster par l'intensité
        intensity_factor = overall_intensity - 0.5  # -0.5 à 0.5
        
        # Ajuster par la cohésion
        cohesion_factor = sentiment_cohesion.get('overall_cohesion', 0.5) - 0.5  # -0.5 à 0.5
        
        # Calculer le facteur de performance
        impact['performance_factor'] = base_factor + (intensity_factor * 0.4) + (cohesion_factor * 0.3)
        
        # Ajuster pour le contexte du match si disponible
        if match_context:
            if match_context.get('is_home', False):
                impact['performance_factor'] += 0.1
            
            importance = match_context.get('importance', 'regular')
            if importance in ['high', 'critical', 'derby']:
                impact['performance_factor'] += 0.1
        
        # Limiter le facteur de performance
        impact['performance_factor'] = max(-0.5, min(0.5, impact['performance_factor']))
        
        # Déterminer la probabilité et la confiance
        impact['probability'] = 0.5 + (abs(impact['performance_factor']) * 0.5)
        
        cohesion = sentiment_cohesion.get('overall_cohesion', 0.5)
        if cohesion > 0.7:
            impact['confidence'] = 'high'
        elif cohesion < 0.4:
            impact['confidence'] = 'low'
        else:
            impact['confidence'] = 'medium'
        
        return impact
    
    def _calculate_base_sentiment_impact(self, current_sentiment, match_importance, is_home):
        """Calculer l'impact sentimental de base pour un match."""
        # Base du calcul
        impact = {
            'raw_impact': 0.0,
            'emotional_component': 0.0,
            'intensity_component': 0.0,
            'cohesion_component': 0.0
        }
        
        # Extraire les composantes du sentiment
        dominant_emotion = current_sentiment.get('dominant_emotion', 'neutral')
        overall_intensity = current_sentiment.get('overall_intensity', 0.5)
        cohesion = current_sentiment.get('sentiment_cohesion', {}).get('overall_cohesion', 0.5)
        
        # Calculer la composante émotionnelle
        if dominant_emotion == 'euphoria':
            impact['emotional_component'] = 0.3
        elif dominant_emotion == 'anxiety':
            impact['emotional_component'] = -0.2
        elif dominant_emotion == 'anger':
            impact['emotional_component'] = 0.1
        elif dominant_emotion == 'confidence':
            impact['emotional_component'] = 0.25
        elif dominant_emotion == 'desperation':
            impact['emotional_component'] = -0.15
        elif dominant_emotion == 'nostalgia':
            impact['emotional_component'] = 0.05
        elif dominant_emotion == 'anticipation':
            impact['emotional_component'] = 0.15
        elif dominant_emotion == 'disappointment':
            impact['emotional_component'] = -0.25
        
        # Ajuster par l'intensité
        impact['intensity_component'] = (overall_intensity - 0.5) * 0.4
        
        # Ajuster par la cohésion
        impact['cohesion_component'] = (cohesion - 0.5) * 0.3
        
        # Calculer l'impact brut
        impact['raw_impact'] = (
            impact['emotional_component'] + 
            impact['intensity_component'] + 
            impact['cohesion_component']
        )
        
        # Ajuster pour les matchs à domicile
        if is_home:
            impact['raw_impact'] *= (1 + self.sentiment_parameters['home_advantage_factor'])
        
        # Ajuster pour l'importance du match
        importance_factor = 1.0
        if match_importance == 'critical':
            importance_factor = 1.3
        elif match_importance == 'high':
            importance_factor = 1.2
        elif match_importance == 'derby':
            importance_factor = 1.25
        
        impact['raw_impact'] *= importance_factor
        
        # Limiter l'impact brut
        impact['raw_impact'] = max(-0.5, min(0.5, impact['raw_impact']))
        
        return impact
    
    def _analyze_specific_factors(self, team_name, opponent_name, match_data):
        """Analyser les facteurs spécifiques au match qui influencent le sentiment."""
        factors = []
        
        # Facteur 1: Historique récent contre cet adversaire
        recent_history = self._get_recent_history(team_name, opponent_name)
        if recent_history.get('favorable', False):
            factors.append({
                'name': 'favorable_history',
                'description': "Historique récent favorable contre cet adversaire",
                'impact_value': 0.1
            })
        elif recent_history.get('unfavorable', False):
            factors.append({
                'name': 'unfavorable_history',
                'description': "Historique récent défavorable contre cet adversaire",
                'impact_value': -0.1
            })
        
        # Facteur 2: Contexte de derby
        if match_data.get('is_derby', False) or match_data.get('importance') == 'derby':
            factors.append({
                'name': 'derby_intensity',
                'description': "Intensité émotionnelle accrue d'un derby",
                'impact_value': 0.15
            })
        
        # Facteur 3: Contexte de fin de saison
        if match_data.get('season_context') == 'end_season':
            if match_data.get('stakes') == 'high':
                factors.append({
                    'name': 'high_stakes_end_season',
                    'description': "Enjeux élevés en fin de saison",
                    'impact_value': 0.2
                })
        
        # Facteur 4: Retour d'un joueur clé
        if match_data.get('key_player_return', False):
            factors.append({
                'name': 'key_player_return',
                'description': "Retour d'un joueur clé boostant le moral",
                'impact_value': 0.1
            })
        
        # Facteur 5: Perte d'un joueur clé
        if match_data.get('key_player_loss', False):
            factors.append({
                'name': 'key_player_loss',
                'description': "Perte d'un joueur clé affectant le moral",
                'impact_value': -0.1
            })
        
        # Facteur 6: Contexte de revanche
        if match_data.get('revenge_context', False):
            factors.append({
                'name': 'revenge_motivation',
                'description': "Motivation de revanche d'une défaite précédente",
                'impact_value': 0.12
            })
        
        return factors
    
    def _determine_impact_type(self, total_impact):
        """Déterminer le type d'impact basé sur la valeur totale."""
        if total_impact > 0.3:
            return "major_positive"
        elif total_impact > 0.1:
            return "moderate_positive"
        elif total_impact > -0.1:
            return "neutral"
        elif total_impact > -0.3:
            return "moderate_negative"
        else:
            return "major_negative"
    
    def _generate_impact_scenarios(self, adjusted_impact, form_factor):
        """Générer des scénarios d'impact potentiels."""
        scenarios = []
        
        impact_type = adjusted_impact.get('impact_type', 'neutral')
        total_impact = adjusted_impact.get('total_impact', 0)
        
        # Scénario 1: Impact optimal
        if impact_type in ['moderate_positive', 'major_positive']:
            probability = 0.3 + (total_impact * 0.5)
            scenarios.append({
                'scenario_type': 'optimal',
                'description': "Supporters galvanisant l'équipe vers une performance exceptionnelle",
                'probability': probability,
                'performance_effect': "Augmentation significative de l'intensité et de la précision"
            })
        
        # Scénario 2: Impact standard positif
        if impact_type in ['moderate_positive', 'major_positive', 'neutral']:
            probability = 0.4 + (max(0, total_impact) * 0.3)
            scenarios.append({
                'scenario_type': 'standard_positive',
                'description': "Énergie positive améliorant la confiance et la cohésion",
                'probability': probability,
                'performance_effect': "Légère augmentation d'efficacité collective"
            })
        
        # Scénario 3: Impact neutre
        probability = 0.5 - (abs(total_impact) * 0.5)
        scenarios.append({
            'scenario_type': 'neutral',
            'description': "Influence émotionnelle équilibrée sans effet significatif",
            'probability': probability,
            'performance_effect': "Performances conformes au niveau habituel"
        })
        
        # Scénario 4: Impact standard négatif
        if impact_type in ['moderate_negative', 'major_negative', 'neutral']:
            probability = 0.4 + (min(0, total_impact) * -0.3)
            scenarios.append({
                'scenario_type': 'standard_negative',
                'description': "Pression excessive créant de la tension et de l'hésitation",
                'probability': probability,
                'performance_effect': "Légère diminution d'efficacité individuelle"
            })
        
        # Scénario 5: Impact pessimal
        if impact_type in ['moderate_negative', 'major_negative']:
            probability = 0.3 + (total_impact * -0.5)
            scenarios.append({
                'scenario_type': 'pessimal',
                'description': "Sentiment négatif paralysant créant un effondrement collectif",
                'probability': probability,
                'performance_effect': "Diminution significative de la concentration et coordination"
            })
        
        # Ajuster les probabilités en fonction de la forme
        for scenario in scenarios:
            if form_factor > 0.7 and scenario['scenario_type'] in ['optimal', 'standard_positive']:
                scenario['probability'] = min(0.95, scenario['probability'] * 1.2)
            elif form_factor < 0.3 and scenario['scenario_type'] in ['pessimal', 'standard_negative']:
                scenario['probability'] = min(0.95, scenario['probability'] * 1.2)
        
        # Normaliser les probabilités
        total_prob = sum(s['probability'] for s in scenarios)
        if total_prob > 0:
            for scenario in scenarios:
                scenario['probability'] = scenario['probability'] / total_prob
        
        # Trier par probabilité
        scenarios.sort(key=lambda s: s['probability'], reverse=True)
        
        return scenarios
    
    def _calculate_performance_influence(self, adjusted_impact, current_sentiment, form_factor):
        """Calculer l'influence sur la performance spécifique."""
        # Base du calcul
        influence = {
            'motivation_impact': 0.0,
            'pressure_impact': 0.0,
            'energy_impact': 0.0,
            'focus_impact': 0.0,
            'overall_impact': 0.0,
            'critical_moments': {}
        }
        
        # Extraire les paramètres nécessaires
        impact_type = adjusted_impact.get('impact_type', 'neutral')
        total_impact = adjusted_impact.get('total_impact', 0)
        dominant_emotion = current_sentiment.get('dominant_emotion', 'neutral')
        intensity = current_sentiment.get('overall_intensity', 0.5)
        
        # Calculer l'impact sur la motivation
        if dominant_emotion in ['euphoria', 'confidence', 'anticipation']:
            influence['motivation_impact'] = 0.2 * intensity
        elif dominant_emotion in ['desperation', 'disappointment']:
            influence['motivation_impact'] = -0.2 * intensity
        else:
            influence['motivation_impact'] = 0.1 * (2 * intensity - 1)  # -0.1 à 0.1
        
        # Calculer l'impact sur la pression
        if dominant_emotion in ['anxiety', 'desperation']:
            influence['pressure_impact'] = -0.2 * intensity
        elif dominant_emotion in ['confidence']:
            influence['pressure_impact'] = 0.15 * intensity
        else:
            influence['pressure_impact'] = 0.0
        
        # Calculer l'impact sur l'énergie
        if dominant_emotion in ['euphoria', 'anger', 'anticipation']:
            influence['energy_impact'] = 0.25 * intensity
        elif dominant_emotion in ['disappointment', 'nostalgia']:
            influence['energy_impact'] = -0.1 * intensity
        else:
            influence['energy_impact'] = 0.0
        
        # Calculer l'impact sur la concentration
        if dominant_emotion in ['confidence', 'anticipation']:
            influence['focus_impact'] = 0.2 * intensity
        elif dominant_emotion in ['anxiety', 'anger']:
            influence['focus_impact'] = -0.15 * intensity
        else:
            influence['focus_impact'] = 0.0
        
        # Ajuster en fonction de la forme
        form_adjustment = (form_factor - 0.5) * 0.2
        influence['motivation_impact'] += form_adjustment
        influence['energy_impact'] += form_adjustment
        
        # Calculer l'impact global
        influence['overall_impact'] = (
            influence['motivation_impact'] * 0.3 +
            influence['pressure_impact'] * 0.25 +
            influence['energy_impact'] * 0.25 +
            influence['focus_impact'] * 0.2
        )
        
        # Déterminer les effets sur les moments critiques
        influence['critical_moments'] = {
            'start_of_match': self._calculate_period_effect('start', dominant_emotion, intensity),
            'after_conceding': self._calculate_period_effect('after_conceding', dominant_emotion, intensity),
            'late_game': self._calculate_period_effect('late_game', dominant_emotion, intensity)
        }
        
        return influence
    
    def _analyze_sentiment_shift(self, pre_emotion, post_emotion, pre_intensity, post_intensity):
        """Analyser le changement de sentiment avant et après un match."""
        # Base de l'analyse
        shift = {
            'emotion_shift': pre_emotion != post_emotion,
            'intensity_change': post_intensity - pre_intensity,
            'magnitude': 0.0,
            'direction': 'neutral',
            'interpretation': ''
        }
        
        # Calculer la magnitude du changement
        emotion_change_value = 0.5 if shift['emotion_shift'] else 0.0
        intensity_change_value = abs(shift['intensity_change'])
        
        shift['magnitude'] = max(emotion_change_value, intensity_change_value)
        
        # Déterminer la direction
        if not shift['emotion_shift'] and abs(shift['intensity_change']) < 0.1:
            shift['direction'] = 'neutral'
            shift['interpretation'] = "Peu de changement émotionnel, sentiment stable"
        elif self._is_positive_emotion(post_emotion) and shift['intensity_change'] > 0:
            shift['direction'] = 'strongly_positive'
            shift['interpretation'] = "Renforcement significatif du sentiment positif"
        elif self._is_positive_emotion(post_emotion):
            shift['direction'] = 'mildly_positive'
            shift['interpretation'] = "Évolution vers un sentiment plus positif"
        elif self._is_negative_emotion(post_emotion) and shift['intensity_change'] > 0:
            shift['direction'] = 'strongly_negative'
            shift['interpretation'] = "Intensification du sentiment négatif"
        elif self._is_negative_emotion(post_emotion):
            shift['direction'] = 'mildly_negative'
            shift['interpretation'] = "Glissement vers un sentiment plus négatif"
        else:
            shift['direction'] = 'mixed'
            shift['interpretation'] = "Évolution complexe du sentiment avec éléments mixtes"
        
        # Ajouter des détails sur le changement spécifique
        if shift['emotion_shift']:
            shift['emotion_transition'] = f"De {pre_emotion} à {post_emotion}"
            shift['transition_significance'] = self._evaluate_transition_significance(pre_emotion, post_emotion)
        
        return shift
    
    def _analyze_sentiment_volatility(self, source_analyses):
        """Analyser la volatilité du sentiment à travers les sources."""
        # Base de l'analyse
        volatility = {
            'overall_volatility': 0.0,
            'source_volatility': {},
            'emotion_stability': {}
        }
        
        # Calculer la volatilité par source
        for source, analysis in source_analyses.items():
            emotion_scores = analysis.get('sentiment_by_emotion', {})
            if emotion_scores:
                # Calculer l'écart-type des scores
                std_dev = np.std(list(emotion_scores.values()))
                volatility['source_volatility'][source] = std_dev
        
        # Calculer la stabilité par émotion
        for emotion in self.collective_emotions:
            emotion_scores = []
            for source, analysis in source_analyses.items():
                if emotion in analysis.get('sentiment_by_emotion', {}):
                    emotion_scores.append(analysis['sentiment_by_emotion'][emotion])
            
            if emotion_scores:
                # Calculer l'écart-type des scores
                std_dev = np.std(emotion_scores)
                volatility['emotion_stability'][emotion] = 1.0 - min(1.0, std_dev * 2)
        
        # Calculer la volatilité globale
        if volatility['source_volatility']:
            volatility['overall_volatility'] = sum(volatility['source_volatility'].values()) / len(volatility['source_volatility'])
        
        return volatility
    
    def _calculate_sentiment_effect_duration(self, emotion, intensity, match_result, match_data):
        """Calculer la durée prévue de l'effet du sentiment."""
        # Base du calcul
        duration = {
            'expected_days': 0,
            'confidence': 'medium',
            'decay_pattern': 'linear'
        }
        
        # Durée de base selon l'émotion et l'intensité
        base_days = 0
        if emotion == 'euphoria':
            base_days = 5
        elif emotion == 'disappointment':
            base_days = 4
        elif emotion == 'anger':
            base_days = 3
        elif emotion == 'confidence':
            base_days = 7
        elif emotion == 'anxiety':
            base_days = 2
        elif emotion == 'desperation':
            base_days = 3
        elif emotion == 'nostalgia':
            base_days = 6
        elif emotion == 'anticipation':
            base_days = 2
        
        # Ajuster par l'intensité
        intensity_multiplier = 0.5 + intensity
        base_days *= intensity_multiplier
        
        # Ajuster par le résultat
        if emotion in ['euphoria', 'confidence'] and match_result == 'win':
            base_days *= 1.3
        elif emotion in ['disappointment', 'anger'] and match_result == 'loss':
            base_days *= 1.3
        
        # Ajuster par l'importance du match
        importance = match_data.get('importance', 'regular')
        if importance == 'critical':
            base_days *= 1.5
        elif importance == 'high':
            base_days *= 1.3
        elif importance == 'derby':
            base_days *= 1.4
        
        # Calculer la durée finale
        duration['expected_days'] = round(base_days)
        
        # Déterminer le pattern de décroissance
        if emotion in ['euphoria', 'anger']:
            duration['decay_pattern'] = 'exponential'
        elif emotion in ['nostalgia', 'confidence']:
            duration['decay_pattern'] = 'plateau_then_drop'
        else:
            duration['decay_pattern'] = 'linear'
        
        # Déterminer la confiance
        if intensity > 0.8:
            duration['confidence'] = 'high'
        elif intensity < 0.4:
            duration['confidence'] = 'low'
        else:
            duration['confidence'] = 'medium'
        
        return duration
    
    def _predict_future_impact(self, team_name, emotion, intensity, sentiment_shift, match_result):
        """Prédire l'impact futur sur les performances."""
        # Base de la prédiction
        prediction = {
            'next_match_impact': 0.0,
            'impact_duration': 0,
            'confidence': 'medium',
            'specific_effects': []
        }
        
        # Calculer l'impact sur le prochain match
        base_impact = 0.0
        if emotion == 'euphoria' and match_result == 'win':
            base_impact = 0.15
        elif emotion == 'confidence' and match_result == 'win':
            base_impact = 0.1
        elif emotion == 'disappointment' and match_result == 'loss':
            base_impact = -0.1
        elif emotion == 'anger' and match_result == 'loss':
            base_impact = -0.05  # Peut être motivant dans certains cas
        elif emotion == 'anxiety':
            base_impact = -0.1
        elif emotion == 'desperation':
            base_impact = -0.15 if match_result == 'loss' else 0.05
        
        # Ajuster par l'intensité
        intensity_factor = intensity - 0.5  # -0.5 à 0.5
        prediction['next_match_impact'] = base_impact + (intensity_factor * 0.1)
        
        # Ajuster par la magnitude du changement
        if sentiment_shift.get('magnitude', 0) > 0.5:
            if sentiment_shift.get('direction') in ['strongly_positive', 'mildly_positive']:
                prediction['next_match_impact'] += 0.05
            elif sentiment_shift.get('direction') in ['strongly_negative', 'mildly_negative']:
                prediction['next_match_impact'] -= 0.05
        
        # Calculer la durée d'impact
        if abs(prediction['next_match_impact']) < 0.05:
            prediction['impact_duration'] = 1
        elif abs(prediction['next_match_impact']) < 0.1:
            prediction['impact_duration'] = 2
        else:
            prediction['impact_duration'] = 3
        
        # Déterminer la confiance
        prediction['confidence'] = sentiment_shift.get('magnitude', 0) > 0.3 and intensity > 0.6 ? 'high' : 'medium'
        
        # Ajouter des effets spécifiques
        if prediction['next_match_impact'] > 0.1:
            prediction['specific_effects'].append(
                "Augmentation de l'énergie au début du match"
            )
        elif prediction['next_match_impact'] < -0.1:
            prediction['specific_effects'].append(
                "Augmentation de la pression et réduction de la prise de risque"
            )
        
        if emotion == 'anger':
            prediction['specific_effects'].append(
                "Possible augmentation de l'agressivité (cartes)"
            )
        elif emotion == 'desperation':
            prediction['specific_effects'].append(
                "Approche plus directe et offensive en cas de score défavorable"
            )
        
        return prediction
    
    def _analyze_sentiment_cycles(self, historical_data):
        """Analyser les cycles de sentiment dans les données historiques."""
        # Base de l'analyse
        cycles = {
            'identified_cycles': [],
            'dominant_pattern': None,
            'cycle_quality': 0.0
        }
        
        # Vérifier les données
        sentiment_timeline = historical_data.get('sentiment_timeline', [])
        if not sentiment_timeline or len(sentiment_timeline) < 10:
            return cycles
        
        # Rechercher différentes longueurs de cycle
        for cycle_length in range(3, min(15, len(sentiment_timeline) // 2)):
            cycle_strength = self._detect_cycle_pattern(sentiment_timeline, cycle_length)
            if cycle_strength > 0.6:
                cycles['identified_cycles'].append({
                    'length': cycle_length,
                    'strength': cycle_strength,
                    'description': self._describe_sentiment_cycle(sentiment_timeline, cycle_length),
                    'current_phase': self._determine_cycle_phase(sentiment_timeline, cycle_length)
                })
        
        # Trier par force
        cycles['identified_cycles'].sort(key=lambda c: c.get('strength', 0), reverse=True)
        
        # Définir le cycle dominant
        if cycles['identified_cycles']:
            cycles['dominant_pattern'] = cycles['identified_cycles'][0]
            cycles['cycle_quality'] = cycles['identified_cycles'][0].get('strength', 0)
        
        return cycles
    
    def _analyze_sentiment_stability(self, historical_data):
        """Analyser la stabilité du sentiment au fil du temps."""
        # Base de l'analyse
        stability = {
            'overall_stability': 0.0,
            'emotion_stability': {},
            'volatility_periods': [],
            'stability_trend': 'stable'
        }
        
        # Vérifier les données
        sentiment_timeline = historical_data.get('sentiment_timeline', [])
        if not sentiment_timeline or len(sentiment_timeline) < 5:
            return stability
        
        # Calculer la stabilité pour chaque émotion
        emotions_over_time = defaultdict(list)
        for point in sentiment_timeline:
            emotion_scores = point.get('emotion_scores', {})
            for emotion, score in emotion_scores.items():
                emotions_over_time[emotion].append(score)
        
        for emotion, scores in emotions_over_time.items():
            if scores:
                stability['emotion_stability'][emotion] = 1.0 - min(1.0, np.std(scores))
        
        # Calculer la stabilité globale
        if stability['emotion_stability']:
            stability['overall_stability'] = sum(stability['emotion_stability'].values()) / len(stability['emotion_stability'])
        
        # Identifier les périodes de volatilité
        volatility_window = 5
        for i in range(len(sentiment_timeline) - volatility_window):
            window = sentiment_timeline[i:i+volatility_window]
            dominant_emotions = [point.get('dominant_emotion') for point in window]
            unique_emotions = len(set(dominant_emotions))
            
            if unique_emotions >= 3:
                start_date = window[0].get('date', '')
                end_date = window[-1].get('date', '')
                
                stability['volatility_periods'].append({
                    'start_date': start_date,
                    'end_date': end_date,
                    'unique_emotions': unique_emotions,
                    'volatility_score': unique_emotions / volatility_window
                })
        
        # Déterminer la tendance de stabilité
        if len(sentiment_timeline) >= 10:
            first_half = sentiment_timeline[:len(sentiment_timeline)//2]
            second_half = sentiment_timeline[len(sentiment_timeline)//2:]
            
            first_emotions = [point.get('dominant_emotion') for point in first_half]
            second_emotions = [point.get('dominant_emotion') for point in second_half]
            
            first_unique = len(set(first_emotions))
            second_unique = len(set(second_emotions))
            
            if second_unique < first_unique * 0.8:
                stability['stability_trend'] = 'increasing'
            elif second_unique > first_unique * 1.2:
                stability['stability_trend'] = 'decreasing'
            else:
                stability['stability_trend'] = 'stable'
        
        return stability
    
    def _analyze_performance_correlations(self, historical_data):
        """Analyser les corrélations entre sentiment et performance."""
        # Base de l'analyse
        correlations = {
            'overall_correlation': 0.0,
            'emotion_correlations': {},
            'strongest_correlation': None,
            'performance_lag': 0
        }
        
        # Vérifier les données
        sentiment_timeline = historical_data.get('sentiment_timeline', [])
        performance_data = historical_data.get('performance_data', [])
        
        if not sentiment_timeline or not performance_data or len(sentiment_timeline) < 5 or len(performance_data) < 5:
            return correlations
        
        # Calculer les corrélations pour chaque émotion
        for emotion in self.collective_emotions:
            emotion_scores = []
            performance_scores = []
            
            # Collecter les paires de données
            for i, sentiment_point in enumerate(sentiment_timeline):
                if i < len(performance_data):
                    emotion_score = sentiment_point.get('emotion_scores', {}).get(emotion, 0)
                    performance_score = performance_data[i].get('performance_score', 0)
                    
                    emotion_scores.append(emotion_score)
                    performance_scores.append(performance_score)
            
            # Calculer la corrélation
            if emotion_scores and len(emotion_scores) > 1:
                try:
                    correlation = np.corrcoef(emotion_scores, performance_scores)[0, 1]
                    correlations['emotion_correlations'][emotion] = correlation
                except:
                    # En cas d'erreur de calcul, utiliser une valeur par défaut
                    correlations['emotion_correlations'][emotion] = 0.0
        
        # Trouver la corrélation la plus forte
        if correlations['emotion_correlations']:
            strongest_emotion = max(correlations['emotion_correlations'].items(), key=lambda x: abs(x[1]))
            correlations['strongest_correlation'] = {
                'emotion': strongest_emotion[0],
                'correlation': strongest_emotion[1],
                'direction': 'positive' if strongest_emotion[1] > 0 else 'negative'
            }
        
        # Calculer la corrélation globale
        if correlations['emotion_correlations']:
            correlations['overall_correlation'] = sum(abs(c) for c in correlations['emotion_correlations'].values()) / len(correlations['emotion_correlations'])
        
        # Analyser le décalage de performance
        correlations['performance_lag'] = self._detect_performance_lag(sentiment_timeline, performance_data)
        
        return correlations
    
    def _identify_sentiment_tipping_points(self, historical_data):
        """Identifier les points de bascule du sentiment."""
        # Base de l'analyse
        tipping_points = []
        
        # Vérifier les données
        sentiment_timeline = historical_data.get('sentiment_timeline', [])
        if not sentiment_timeline or len(sentiment_timeline) < 5:
            return tipping_points
        
        # Trier par date
        sorted_timeline = sorted(sentiment_timeline, key=lambda x: x.get('date', ''))
        
        # Identifier les changements significatifs
        for i in range(1, len(sorted_timeline)):
            prev = sorted_timeline[i-1]
            curr = sorted_timeline[i]
            
            prev_emotion = prev.get('dominant_emotion', '')
            curr_emotion = curr.get('dominant_emotion', '')
            
            prev_intensity = prev.get('overall_intensity', 0.5)
            curr_intensity = curr.get('overall_intensity', 0.5)
            
            # Si l'émotion a changé ou l'intensité a beaucoup varié
            if prev_emotion != curr_emotion or abs(curr_intensity - prev_intensity) > 0.25:
                tipping_point = {
                    'date': curr.get('date', ''),
                    'previous_emotion': prev_emotion,
                    'new_emotion': curr_emotion,
                    'intensity_change': curr_intensity - prev_intensity,
                    'significance': 0.0,
                    'trigger_events': []
                }
                
                # Calculer la significance
                emotion_change_value = 0.5 if prev_emotion != curr_emotion else 0.0
                intensity_change_value = abs(curr_intensity - prev_intensity)
                tipping_point['significance'] = max(emotion_change_value, intensity_change_value)
                
                # Identifier les déclencheurs potentiels
                trigger_events = historical_data.get('key_events', [])
                for event in trigger_events:
                    event_date = event.get('date', '')
                    tipping_date = tipping_point['date']
                    
                    # Si l'événement est proche dans le temps (à adapter selon le format de date)
                    if abs((datetime.fromisoformat(event_date) - datetime.fromisoformat(tipping_date)).days) <= 7:
                        tipping_point['trigger_events'].append(event)
                
                tipping_points.append(tipping_point)
        
        # Trier par significance
        tipping_points.sort(key=lambda tp: tp.get('significance', 0), reverse=True)
        
        return tipping_points
    
    def _analyze_external_influence_factors(self, historical_data):
        """Analyser les facteurs externes influençant le sentiment."""
        # Base de l'analyse
        factors = []
        
        # Vérifier les données
        external_events = historical_data.get('external_events', [])
        sentiment_timeline = historical_data.get('sentiment_timeline', [])
        
        if not external_events or not sentiment_timeline:
            return factors
        
        # Analyser l'impact de chaque type d'événement externe
        event_types = set(event.get('type', '') for event in external_events)
        
        for event_type in event_types:
            events_of_type = [e for e in external_events if e.get('type') == event_type]
            if not events_of_type:
                continue
            
            # Mesurer l'impact moyen
            impact_scores = []
            for event in events_of_type:
                impact = self._measure_event_impact(event, sentiment_timeline)
                if impact['detected']:
                    impact_scores.append(impact['magnitude'])
            
            if impact_scores:
                average_impact = sum(impact_scores) / len(impact_scores)
                factors.append({
                    'factor_type': event_type,
                    'average_impact': average_impact,
                    'occurrence_count': len(events_of_type),
                    'consistency': 1.0 - min(1.0, np.std(impact_scores)) if len(impact_scores) > 1 else 0.5,
                    'example_events': events_of_type[:2]  # Quelques exemples
                })
        
        # Trier par impact moyen
        factors.sort(key=lambda f: abs(f.get('average_impact', 0)), reverse=True)
        
        return factors
    
    def _calculate_baseline_sentiment(self, historical_data):
        """Calculer le sentiment de base sur la période historique."""
        # Base du calcul
        baseline = {
            'dominant_emotion': '',
            'emotion_distribution': {},
            'average_intensity': 0.0,
            'stability_score': 0.0
        }
        
        # Vérifier les données
        sentiment_timeline = historical_data.get('sentiment_timeline', [])
        if not sentiment_timeline:
            return baseline
        
        # Calculer la distribution des émotions
        emotion_counts = defaultdict(int)
        total_intensity = 0.0
        total_points = len(sentiment_timeline)
        
        for point in sentiment_timeline:
            emotion = point.get('dominant_emotion', '')
            if emotion:
                emotion_counts[emotion] += 1
            
            intensity = point.get('overall_intensity', 0.5)
            total_intensity += intensity
        
        # Calculer la distribution
        if emotion_counts:
            for emotion, count in emotion_counts.items():
                baseline['emotion_distribution'][emotion] = count / total_points
            
            # Déterminer l'émotion dominante
            baseline['dominant_emotion'] = max(emotion_counts, key=emotion_counts.get)
        
        # Calculer l'intensité moyenne
        if total_points > 0:
            baseline['average_intensity'] = total_intensity / total_points
        
        # Calculer le score de stabilité
        if baseline['emotion_distribution']:
            # Un score élevé si une émotion est clairement dominante
            max_percentage = max(baseline['emotion_distribution'].values())
            baseline['stability_score'] = max_percentage
        
        return baseline
    
    def _generate_long_term_projection(self, team_name, historical_data, sentiment_cycles, sentiment_stability):
        """Générer une projection à long terme du sentiment."""
        # Base de la projection
        projection = {
            'timeframe': 'season',
            'expected_baseline': {},
            'potential_shifts': [],
            'risk_factors': [],
            'confidence': 'medium'
        }
        
        # Calculer le sentiment de base
        baseline_sentiment = self._calculate_baseline_sentiment(historical_data)
        
        # Utiliser comme point de départ pour la projection
        projection['expected_baseline'] = {
            'dominant_emotion': baseline_sentiment.get('dominant_emotion', ''),
            'intensity': baseline_sentiment.get('average_intensity', 0.5),
            'stability': baseline_sentiment.get('stability_score', 0.5)
        }
        
        # Identifier les changements potentiels basés sur les cycles
        dominant_cycle = sentiment_cycles.get('dominant_pattern')
        if dominant_cycle:
            cycle_length = dominant_cycle.get('length', 0)
            current_phase = dominant_cycle.get('current_phase', 0)
            
            if cycle_length > 0:
                # Calculer à quelle distance on est du prochain changement
                next_phase = (current_phase + 1) % cycle_length
                steps_to_change = (next_phase - current_phase) % cycle_length
                
                # Convertir les étapes en date approximative
                approx_date = (datetime.now() + timedelta(days=steps_to_change * 30)).isoformat()  # Estimation grossière
                
                projection['potential_shifts'].append({
                    'estimated_date': approx_date,
                    'cycle_based': True,
                    'description': f"Changement cyclique attendu basé sur le pattern de {cycle_length} unités",
                    'confidence': dominant_cycle.get('strength', 0.5)
                })
        
        # Identifier les facteurs de risque
        stability_score = sentiment_stability.get('overall_stability', 0.5)
        if stability_score < 0.4:
            projection['risk_factors'].append({
                'type': 'high_volatility',
                'description': "Forte volatilité historique suggérant des changements imprévisibles",
                'severity': 0.8
            })
        
        volatility_periods = sentiment_stability.get('volatility_periods', [])
        if volatility_periods and len(volatility_periods) >= 3:
            projection['risk_factors'].append({
                'type': 'recurring_volatility',
                'description': "Périodes de volatilité récurrentes indiquant une instabilité structurelle",
                'severity': 0.7
            })
        
        # Déterminer la confiance dans la projection
        if stability_score > 0.7 and baseline_sentiment.get('stability_score', 0) > 0.6:
            projection['confidence'] = 'high'
        elif stability_score < 0.4 or baseline_sentiment.get('stability_score', 0) < 0.3:
            projection['confidence'] = 'low'
        else:
            projection['confidence'] = 'medium'
        
        return projection
    
    def _compare_dominant_emotions(self, emotion1, emotion2, scores1, scores2):
        """Comparer les émotions dominantes de deux équipes."""
        # Base de la comparaison
        comparison = {
            'are_identical': emotion1 == emotion2,
            'are_complementary': False,
            'are_conflicting': False,
            'relative_intensity': {}
        }
        
        # Vérifier si elles sont complémentaires ou conflictuelles
        if emotion1 != emotion2:
            complementary_pairs = [
                ('confidence', 'anxiety'),
                ('euphoria', 'disappointment'),
                ('anticipation', 'nostalgia')
            ]
            
            for e1, e2 in complementary_pairs:
                if (emotion1 == e1 and emotion2 == e2) or (emotion1 == e2 and emotion2 == e1):
                    comparison['are_complementary'] = True
                    break
            
            conflicting_pairs = [
                ('confidence', 'desperation'),
                ('euphoria', 'anger'),
                ('anticipation', 'disappointment')
            ]
            
            for e1, e2 in conflicting_pairs:
                if (emotion1 == e1 and emotion2 == e2) or (emotion1 == e2 and emotion2 == e1):
                    comparison['are_conflicting'] = True
                    break
        
        # Comparer les intensités relatives
        for emotion in set(scores1.keys()) | set(scores2.keys()):
            score1 = scores1.get(emotion, 0)
            score2 = scores2.get(emotion, 0)
            
            if score1 > 0 or score2 > 0:
                comparison['relative_intensity'][emotion] = {
                    'team1_score': score1,
                    'team2_score': score2,
                    'difference': score1 - score2
                }
        
        return comparison
    
    def _compare_intensities(self, intensity1, intensity2):
        """Comparer les intensités de sentiment."""
        # Base de la comparaison
        comparison = {
            'intensity_gap': abs(intensity1 - intensity2),
            'higher_intensity': 'team1' if intensity1 > intensity2 else 'team2' if intensity2 > intensity1 else 'equal',
            'significance': 0.0
        }
        
        # Calculer la significance
        comparison['significance'] = min(1.0, comparison['intensity_gap'] * 2)
        
        return comparison
    
    def _compare_cohesions(self, cohesion1, cohesion2):
        """Comparer les cohésions de sentiment."""
        # Base de la comparaison
        comparison = {
            'cohesion_gap': abs(cohesion1 - cohesion2),
            'higher_cohesion': 'team1' if cohesion1 > cohesion2 else 'team2' if cohesion2 > cohesion1 else 'equal',
            'significance': 0.0
        }
        
        # Calculer la significance
        comparison['significance'] = min(1.0, comparison['cohesion_gap'] * 2)
        
        return comparison
    
    def _analyze_sentiment_interaction(self, sentiment1, sentiment2):
        """Analyser l'interaction entre les sentiments de deux équipes."""
        # Base de l'analyse
        interaction = {
            'type': 'neutral',
            'intensity': 0.0,
            'dynamic': '',
            'expected_effect': ''
        }
        
        # Extraire les composantes
        emotion1 = sentiment1.get('dominant_emotion', '')
        emotion2 = sentiment2.get('dominant_emotion', '')
        intensity1 = sentiment1.get('overall_intensity', 0.5)
        intensity2 = sentiment2.get('overall_intensity', 0.5)
        
        # Déterminer le type d'interaction
        if emotion1 == emotion2:
            interaction['type'] = 'mirror'
            interaction['dynamic'] = "Reflet émotionnel créant une résonance amplificatrice"
            interaction['intensity'] = (intensity1 + intensity2) / 2
        elif self._are_complementary_emotions(emotion1, emotion2):
            interaction['type'] = 'complementary'
            interaction['dynamic'] = "Émotions complémentaires créant une dynamique équilibrante"
            interaction['intensity'] = max(intensity1, intensity2) * 0.8
        elif self._are_conflicting_emotions(emotion1, emotion2):
            interaction['type'] = 'conflicting'
            interaction['dynamic'] = "Émotions conflictuelles créant une tension importante"
            interaction['intensity'] = max(intensity1, intensity2) * 1.2
        else:
            interaction['type'] = 'independent'
            interaction['dynamic'] = "Émotions indépendantes sans interaction significative"
            interaction['intensity'] = (intensity1 + intensity2) / 4
        
        # Déterminer l'effet attendu
        if interaction['type'] == 'mirror' and (emotion1 in ['euphoria', 'confidence', 'anticipation']):
            interaction['expected_effect'] = "Amplification positive de l'atmosphère"
        elif interaction['type'] == 'mirror' and (emotion1 in ['anxiety', 'disappointment', 'desperation']):
            interaction['expected_effect'] = "Amplification négative de la tension"
        elif interaction['type'] == 'complementary':
            interaction['expected_effect'] = "Équilibre des forces émotionnelles"
        elif interaction['type'] == 'conflicting' and intensity1 > intensity2:
            interaction['expected_effect'] = f"Domination probable de l'émotion de l'équipe 1 ({emotion1})"
        elif interaction['type'] == 'conflicting':
            interaction['expected_effect'] = f"Domination probable de l'émotion de l'équipe 2 ({emotion2})"
        else:
            interaction['expected_effect'] = "Peu d'effet d'interaction notable"
        
        return interaction
    
    def _determine_sentiment_advantage(self, team1_name, team2_name, sentiment1, sentiment2, context=None):
        """Déterminer quel équipe a un avantage sentimental."""
        # Base de l'analyse
        advantage = {
            'team': None,
            'magnitude': 0.0,
            'factors': [],
            'confidence': 'medium'
        }
        
        # Extraire les composantes
        emotion1 = sentiment1.get('dominant_emotion', '')
        emotion2 = sentiment2.get('dominant_emotion', '')
        intensity1 = sentiment1.get('overall_intensity', 0.5)
        intensity2 = sentiment2.get('overall_intensity', 0.5)
        cohesion1 = sentiment1.get('sentiment_cohesion', {}).get('overall_cohesion', 0.5)
        cohesion2 = sentiment2.get('sentiment_cohesion', {}).get('overall_cohesion', 0.5)
        
        # Facteur 1: Type d'émotion
        emotion1_factor = self._calculate_emotion_value(emotion1)
        emotion2_factor = self._calculate_emotion_value(emotion2)
        emotion_diff = emotion1_factor - emotion2_factor
        
        if abs(emotion_diff) > 0.1:
            advantage['factors'].append({
                'type': 'emotion_type',
                'value': emotion_diff,
                'description': f"{'L'équipe 1' if emotion_diff > 0 else 'L'équipe 2'} bénéficie d'une émotion plus favorable"
            })
        
        # Facteur 2: Intensité
        intensity_diff = intensity1 - intensity2
        if abs(intensity_diff) > 0.1:
            advantage['factors'].append({
                'type': 'emotional_intensity',
                'value': intensity_diff * 0.5,  # Pondéré à 50%
                'description': f"{'L'équipe 1' if intensity_diff > 0 else 'L'équipe 2'} a une intensité émotionnelle plus forte"
            })
        
        # Facteur 3: Cohésion
        cohesion_diff = cohesion1 - cohesion2
        if abs(cohesion_diff) > 0.1:
            advantage['factors'].append({
                'type': 'sentiment_cohesion',
                'value': cohesion_diff * 0.3,  # Pondéré à 30%
                'description': f"{'L'équipe 1' if cohesion_diff > 0 else 'L'équipe 2'} a une cohésion émotionnelle plus forte"
            })
        
        # Facteur 4: Contexte du match
        if context and 'type' in context:
            context_factor = 0.0
            
            if context['type'] == 'home_match' and context.get('home_team') == team1_name:
                context_factor = 0.15
            elif context['type'] == 'home_match' and context.get('home_team') == team2_name:
                context_factor = -0.15
            elif context['type'] == 'derby':
                # Dans un derby, l'avantage va à l'équipe avec plus de "fire" émotionnel
                if emotion1 in ['euphoria', 'anger', 'anticipation'] and emotion2 not in ['euphoria', 'anger', 'anticipation']:
                    context_factor = 0.1
                elif emotion2 in ['euphoria', 'anger', 'anticipation'] and emotion1 not in ['euphoria', 'anger', 'anticipation']:
                    context_factor = -0.1
            
            if context_factor != 0:
                advantage['factors'].append({
                    'type': 'match_context',
                    'value': context_factor,
                    'description': f"{'L'équipe 1' if context_factor > 0 else 'L'équipe 2'} est favorisée par le contexte du match"
                })
        
        # Calculer la magnitude globale
        total_advantage = sum(factor.get('value', 0) for factor in advantage['factors'])
        advantage['magnitude'] = total_advantage
        
        # Déterminer l'équipe avantagée
        if total_advantage > 0.05:
            advantage['team'] = team1_name
        elif total_advantage < -0.05:
            advantage['team'] = team2_name
            advantage['magnitude'] = abs(advantage['magnitude'])  # Rendre la magnitude positive
        else:
            advantage['team'] = 'neutral'
            advantage['magnitude'] = abs(advantage['magnitude'])  # Rendre la magnitude positive
        
        # Déterminer la confiance
        if len(advantage['factors']) >= 3 and advantage['magnitude'] > 0.2:
            advantage['confidence'] = 'high'
        elif len(advantage['factors']) <= 1 or advantage['magnitude'] < 0.1:
            advantage['confidence'] = 'low'
        else:
            advantage['confidence'] = 'medium'
        
        return advantage
    
    def _calculate_source_reliability(self, source_name, metrics):
        """Calculer la fiabilité d'une source de sentiment."""
        # Cette fonction simule le calcul de fiabilité
        # Dans une implémentation réelle, elle utiliserait des métriques spécifiques
        
        # Simuler une fiabilité entre 0.5 et 0.9
        return random.uniform(0.5, 0.9)
    
    def _calculate_source_alignment(self, source1_analysis, source2_analysis):
        """Calculer l'alignement entre deux sources."""
        # Cette fonction calcule l'alignement entre deux sources
        
        # Extraire les scores d'émotions
        emotions1 = source1_analysis.get('sentiment_by_emotion', {})
        emotions2 = source2_analysis.get('sentiment_by_emotion', {})
        
        # Calculer la distance
        common_emotions = set(emotions1.keys()) & set(emotions2.keys())
        if not common_emotions:
            return 0.0
        
        total_diff = 0.0
        for emotion in common_emotions:
            total_diff += abs(emotions1[emotion] - emotions2[emotion])
        
        # Convertir en score d'alignement
        if len(common_emotions) > 0:
            avg_diff = total_diff / len(common_emotions)
            alignment = 1.0 - min(1.0, avg_diff)
            return alignment
        
        return 0.0
    
    def _identify_shift_trigger(self, analysis):
        """Identifier le déclencheur potentiel d'un changement de sentiment."""
        # Cette fonction simule l'identification de déclencheur
        # Dans une implémentation réelle, elle analyserait des événements
        
        return random.choice([
            "Résultat de match",
            "Déclaration de l'entraîneur",
            "Transfert de joueur",
            "Controverse arbitrale",
            "Blessure d'un joueur clé",
            "Performance exceptionnelle"
        ])
    
    def _predict_sentiment_trend(self, recent_analyses, recent_direction, trend_strength):
        """Prédire la tendance future du sentiment."""
        # Cette fonction simule la prédiction de tendance
        # Dans une implémentation réelle, elle utiliserait des modèles plus sophistiqués
        
        # Base de la prédiction
        prediction = {
            'confidence': 'medium',
            'next_direction': recent_direction,
            'explanation': ""
        }
        
        # Simuler une prédiction basée sur la direction récente
        if recent_direction == 'increasing':
            if trend_strength > 0.3:
                prediction['explanation'] = "La forte augmentation récente devrait se poursuivre à court terme"
                prediction['confidence'] = 'high'
            else:
                prediction['explanation'] = "La tendance à la hausse modérée devrait continuer, mais pourrait se stabiliser"
        elif recent_direction == 'decreasing':
            if trend_strength > 0.3:
                prediction['explanation'] = "La baisse significative pourrait s'inverser prochainement par effet rebond"
                prediction['next_direction'] = 'stabilizing'
            else:
                prediction['explanation'] = "La tendance baissière modérée devrait se poursuivre"
        else:  # stable
            prediction['explanation'] = "La stabilité actuelle devrait se maintenir, avec de légères fluctuations possibles"
            prediction['confidence'] = 'high'
        
        return prediction
    
    def _calculate_match_importance(self, match_data):
        """Calculer l'importance d'un match."""
        # Cette fonction détermine l'importance d'un match
        
        # Valeur par défaut
        importance = 'regular'
        
        # Détecter les facteurs d'importance
        if match_data.get('is_derby', False):
            importance = 'derby'
        elif match_data.get('is_final', False) or match_data.get('is_semifinal', False):
            importance = 'critical'
        elif match_data.get('stakes') == 'high' or match_data.get('importance') == 'high':
            importance = 'high'
        
        return importance
    
    def _analyze_recent_form(self, recent_form):
        """Analyser la forme récente d'une équipe."""
        # Cette fonction calcule un facteur basé sur la forme récente
        
        if not recent_form:
            return 0.5  # Valeur neutre
        
        # Compter les résultats
        wins = recent_form.count('W')
        draws = recent_form.count('D')
        losses = recent_form.count('L')
        
        total_matches = len(recent_form)
        
        # Calculer le facteur
        form_factor = (wins + 0.5 * draws) / total_matches
        
        return form_factor
    
    def _get_recent_history(self, team_name, opponent_name):
        """Obtenir l'historique récent entre deux équipes."""
        # Cette fonction simule la récupération d'historique
        # Dans une implémentation réelle, elle interrogerait une base de données
        
        return {
            'favorable': random.choice([True, False]),
            'unfavorable': random.choice([True, False]),
            'recent_matches': []
        }
    
    def _calculate_period_effect(self, period, emotion, intensity):
        """Calculer l'effet du sentiment sur une période spécifique du match."""
        # Cette fonction calcule l'effet pour différentes périodes
        
        effect = {
            'impact': 0.0,
            'description': ""
        }
        
        # Effets spécifiques selon la période et l'émotion
        if period == 'start':
            if emotion == 'euphoria':
                effect['impact'] = 0.3 * intensity
                effect['description'] = "Départ énergique et offensif"
            elif emotion == 'anxiety':
                effect['impact'] = -0.3 * intensity
                effect['description'] = "Départ nerveux et hésitant"
            elif emotion == 'confidence':
                effect['impact'] = 0.25 * intensity
                effect['description'] = "Départ composé et méthodique"
            else:
                effect['impact'] = 0.1 * intensity
                effect['description'] = "Départ standard sans effet notable"
        
        elif period == 'after_conceding':
            if emotion == 'desperation':
                effect['impact'] = -0.2 * intensity
                effect['description'] = "Effondrement possible après avoir encaissé"
            elif emotion == 'anger':
                effect['impact'] = 0.15 * intensity
                effect['description'] = "Réaction combative après avoir encaissé"
            elif emotion == 'confidence':
                effect['impact'] = 0.2 * intensity
                effect['description'] = "Résilience après avoir encaissé"
            else:
                effect['impact'] = 0.0
                effect['description'] = "Réaction standard après avoir encaissé"
        
        elif period == 'late_game':
            if emotion == 'desperation':
                effect['impact'] = 0.1 * intensity
                effect['description'] = "Pression offensive désordonnée en fin de match"
            elif emotion == 'confidence':
                effect['impact'] = 0.25 * intensity
                effect['description'] = "Gestion efficace des dernières minutes"
            elif emotion == 'anxiety':
                effect['impact'] = -0.25 * intensity
                effect['description'] = "Crispation défensive en fin de match"
            else:
                effect['impact'] = 0.0
                effect['description'] = "Approche standard de fin de match"
        
        return effect
    
    def _generate_response_data(self, team_name, match_result, pre_match_sentiment):
        """Générer des données de réponse sentimentale après un match."""
        # Cette fonction simule la génération de données
        # Dans une implémentation réelle, elle utiliserait des données réelles
        
        response_data = {}
        
        # Déterminer l'émotion probable après le match
        pre_emotion = pre_match_sentiment.get('dominant_emotion', 'anticipation')
        pre_intensity = pre_match_sentiment.get('overall_intensity', 0.7)
        
        # Déterminer l'émotion post-match basée sur le résultat et l'émotion pré-match
        post_emotion = self._determine_post_match_emotion(pre_emotion, match_result)
        
        # Déterminer l'intensité post-match
        post_intensity = self._determine_post_match_intensity(pre_intensity, match_result)
        
        # Générer des données pour chaque source
        for source, source_config in self.sentiment_sources.items():
            source_data = {
                'emotions': {}
            }
            
            # Générer des scores pour chaque émotion
            for emotion in self.collective_emotions:
                if emotion == post_emotion:
                    # L'émotion dominante a un score élevé
                    source_data['emotions'][emotion] = max(0.7, post_intensity) + random.uniform(-0.1, 0.1)
                else:
                    # Les autres émotions ont des scores plus bas
                    base_score = random.uniform(0.1, 0.4)
                    if self._are_complementary_emotions(emotion, post_emotion):
                        base_score += 0.2  # Les émotions complémentaires sont légèrement plus élevées
                    
                    source_data['emotions'][emotion] = min(1.0, base_score)
            
            # Ajouter des métriques spécifiques à la source
            for metric in source_config.get('metrics', []):
                source_data[metric] = random.uniform(0.3, 0.9)
            
            response_data[source] = source_data
        
        return response_data
    
    def _determine_post_match_emotion(self, pre_emotion, match_result):
        """Déterminer l'émotion probable après un match selon le résultat."""
        # Mapping des émotions post-match pour chaque résultat
        post_match_emotions = {
            'win': ['euphoria', 'confidence', 'anticipation'],
            'loss': ['disappointment', 'anger', 'desperation'],
            'draw': ['nostalgia', 'anxiety', 'anticipation']
        }
        
        # Si le résultat n'est pas connu, utiliser une distribution plus équilibrée
        if match_result not in post_match_emotions:
            return random.choice(self.collective_emotions)
        
        # Choisir parmi les émotions probables pour ce résultat
        return random.choice(post_match_emotions[match_result])
    
    def _determine_post_match_intensity(self, pre_intensity, match_result):
        """Déterminer l'intensité probable après un match selon le résultat."""
        # Les victoires et défaites génèrent généralement plus d'intensité que les nuls
        if match_result == 'win':
            return min(1.0, pre_intensity * 1.3)
        elif match_result == 'loss':
            return min(1.0, pre_intensity * 1.2)
        elif match_result == 'draw':
            return pre_intensity * 0.9
        else:
            return pre_intensity
    
    def _detect_cycle_pattern(self, timeline, cycle_length):
        """Détecter un pattern cyclique dans une timeline."""
        # Cette fonction simule la détection de cycles
        # Dans une implémentation réelle, elle utiliserait des algorithmes plus sophistiqués
        
        # Simuler une force de cycle entre 0.5 et 0.9
        cycle_strength = random.uniform(0.5, 0.9)
        
        return cycle_strength
    
    def _describe_sentiment_cycle(self, timeline, cycle_length):
        """Décrire un cycle de sentiment détecté."""
        # Cette fonction simule la description de cycles
        # Dans une implémentation réelle, elle analyserait les patterns
        
        return random.choice([
            f"Cycle de {cycle_length} alternant optimisme et pessimisme",
            f"Oscillation de {cycle_length} entre euphorie et déception",
            f"Séquence de {cycle_length} avec montée progressive puis chute",
            f"Pattern de {cycle_length} avec phases stables et transitions rapides"
        ])
    
    def _determine_cycle_phase(self, timeline, cycle_length):
        """Déterminer la phase actuelle dans un cycle."""
        # Cette fonction simule la détermination de phase
        # Dans une implémentation réelle, elle calculerait la position
        
        # Simuler une phase aléatoire dans le cycle
        return random.randint(0, cycle_length - 1)
    
    def _detect_performance_lag(self, sentiment_timeline, performance_data):
        """Détecter le décalage entre sentiment et performance."""
        # Cette fonction simule la détection de décalage
        # Dans une implémentation réelle, elle utiliserait des analyses de séries temporelles
        
        # Simuler un décalage entre 0 et 3
        return random.randint(0, 3)
    
    def _measure_event_impact(self, event, sentiment_timeline):
        """Mesurer l'impact d'un événement externe sur le sentiment."""
        # Cette fonction simule la mesure d'impact
        # Dans une implémentation réelle, elle comparerait les séries temporelles
        
        return {
            'detected': random.choice([True, False]),
            'magnitude': random.uniform(0.1, 0.8),
            'latency': random.randint(1, 7)
        }
    
    def _is_positive_emotion(self, emotion):
        """Vérifier si une émotion est généralement positive."""
        return emotion in ['euphoria', 'confidence', 'anticipation']
    
    def _is_negative_emotion(self, emotion):
        """Vérifier si une émotion est généralement négative."""
        return emotion in ['anxiety', 'disappointment', 'desperation', 'anger']
    
    def _evaluate_transition_significance(self, emotion1, emotion2):
        """Évaluer la signification d'une transition entre émotions."""
        # Cette fonction évalue l'importance d'un changement d'émotion
        
        # Transitions majeures
        major_transitions = [
            ('euphoria', 'disappointment'),
            ('confidence', 'anxiety'),
            ('anticipation', 'desperation'),
            ('disappointment', 'euphoria'),
            ('anxiety', 'confidence')
        ]
        
        if (emotion1, emotion2) in major_transitions:
            return 'major_shift'
        elif self._is_positive_emotion(emotion1) and self._is_negative_emotion(emotion2):
            return 'negative_shift'
        elif self._is_negative_emotion(emotion1) and self._is_positive_emotion(emotion2):
            return 'positive_shift'
        else:
            return 'minor_shift'
    
    def _are_complementary_emotions(self, emotion1, emotion2):
        """Vérifier si deux émotions sont complémentaires."""
        complementary_pairs = [
            ('confidence', 'anxiety'),
            ('euphoria', 'disappointment'),
            ('anticipation', 'nostalgia'),
            ('anger', 'desperation')
        ]
        
        return (emotion1, emotion2) in complementary_pairs or (emotion2, emotion1) in complementary_pairs
    
    def _are_conflicting_emotions(self, emotion1, emotion2):
        """Vérifier si deux émotions sont conflictuelles."""
        conflicting_pairs = [
            ('confidence', 'desperation'),
            ('euphoria', 'anger'),
            ('anticipation', 'disappointment'),
            ('nostalgia', 'anxiety')
        ]
        
        return (emotion1, emotion2) in conflicting_pairs or (emotion2, emotion1) in conflicting_pairs
    
    def _calculate_emotion_value(self, emotion):
        """Calculer la valeur stratégique d'une émotion."""
        # Cette fonction attribue une valeur à chaque type d'émotion
        # pour déterminer son impact probable sur la performance
        
        emotion_values = {
            'confidence': 0.3,
            'euphoria': 0.25,
            'anticipation': 0.2,
            'nostalgia': 0.1,
            'anxiety': -0.15,
            'anger': -0.05,  # Peut être positive ou négative
            'disappointment': -0.2,
            'desperation': -0.25
        }
        
        return emotion_values.get(emotion, 0.0)
    
    def _generate_sentiment_data(self, team_name):
        """Générer des données de sentiment simulées."""
        # Cette fonction simule la génération de données
        # Dans une implémentation réelle, elle récupérerait des données de sources externes
        
        sentiment_data = {}
        
        # Générer une émotion dominante
        dominant_emotion = random.choice(self.collective_emotions)
        dominant_intensity = random.uniform(0.6, 0.9)
        
        # Générer des données pour chaque source
        for source, source_config in self.sentiment_sources.items():
            source_data = {
                'emotions': {}
            }
            
            # Générer des scores pour chaque émotion
            for emotion in self.collective_emotions:
                if emotion == dominant_emotion:
                    # L'émotion dominante a un score élevé
                    source_data['emotions'][emotion] = dominant_intensity + random.uniform(-0.1, 0.1)
                else:
                    # Les autres émotions ont des scores plus bas
                    base_score = random.uniform(0.1, 0.4)
                    if self._are_complementary_emotions(emotion, dominant_emotion):
                        base_score += 0.2  # Les émotions complémentaires sont légèrement plus élevées
                    
                    source_data['emotions'][emotion] = min(1.0, base_score)
            
            # Ajouter des métriques spécifiques à la source
            for metric in source_config.get('metrics', []):
                source_data[metric] = random.uniform(0.3, 0.9)
            
            sentiment_data[source] = source_data
        
        return sentiment_data
    
    def _generate_historical_data(self, team_name, timeframe):
        """Générer des données historiques simulées."""
        # Cette fonction simule la génération de données historiques
        # Dans une implémentation réelle, elle récupérerait des données archivées
        
        # Déterminer le nombre de points selon la période
        if timeframe == 'season':
            num_points = 30
        elif timeframe == 'year':
            num_points = 50
        else:  # multi_year
            num_points = 100
        
        # Générer une timeline de sentiment
        sentiment_timeline = []
        base_date = datetime.now() - timedelta(days=num_points * 7)
        
        for i in range(num_points):
            point_date = (base_date + timedelta(days=i * 7)).isoformat()
            
            # Simuler une émotion dominante
            dominant_emotion = random.choice(self.collective_emotions)
            
            # Simuler des scores pour toutes les émotions
            emotion_scores = {}
            for emotion in self.collective_emotions:
                if emotion == dominant_emotion:
                    emotion_scores[emotion] = random.uniform(0.6, 0.9)
                else:
                    emotion_scores[emotion] = random.uniform(0.1, 0.5)
            
            sentiment_timeline.append({
                'date': point_date,
                'dominant_emotion': dominant_emotion,
                'overall_intensity': random.uniform(0.4, 0.9),
                'emotion_scores': emotion_scores
            })
        
        # Générer des données de performance correspondantes
        performance_data = []
        for i in range(num_points):
            point_date = (base_date + timedelta(days=i * 7)).isoformat()
            
            performance_data.append({
                'date': point_date,
                'performance_score': random.uniform(0.2, 0.8),
                'match_result': random.choice(['win', 'draw', 'loss'])
            })
        
        # Générer des événements externes
        external_events = []
        num_events = num_points // 5
        
        for i in range(num_events):
            event_day = random.randint(0, num_points * 7)
            event_date = (base_date + timedelta(days=event_day)).isoformat()
            
            external_events.append({
                'date': event_date,
                'type': random.choice([
                    'management_change', 'key_signing', 'player_departure',
                    'fan_protest', 'financial_news', 'controversy', 'milestone'
                ]),
                'description': f"Événement {i+1}",
                'significance': random.uniform(0.3, 0.9)
            })
        
        # Compiler les données historiques
        historical_data = {
            'team_name': team_name,
            'timeframe': timeframe,
            'sentiment_timeline': sentiment_timeline,
            'performance_data': performance_data,
            'external_events': external_events,
            'key_events': self._generate_key_events(base_date, num_points)
        }
        
        return historical_data
    
    def _generate_key_events(self, base_date, num_points):
        """Générer des événements clés simulés."""
        # Cette fonction simule la génération d'événements clés
        # Dans une implémentation réelle, elle utiliserait des données historiques
        
        key_events = []
        num_events = min(10, num_points // 10)
        
        for i in range(num_events):
            event_day = random.randint(0, num_points * 7)
            event_date = (base_date + timedelta(days=event_day)).isoformat()
            
            key_events.append({
                'date': event_date,
                'type': random.choice([
                    'critical_win', 'major_loss', 'derby_result',
                    'championship_game', 'relegation_battle', 'record_breaking_performance'
                ]),
                'description': f"Événement clé {i+1}",
                'significance': random.uniform(0.7, 1.0)
            })
        
        return key_events