"""
MultidimensionalAnalyzer - Module d'analyse combinant approches statistiques, ésotériques et comportementales.
Intègre les données des différentes dimensions d'analyse pour une prédiction holistique.
"""

import numpy as np
import random
from datetime import datetime, timedelta
from collections import defaultdict

class MultidimensionalAnalyzer:
    """
    MultidimensionalAnalyzer - Système d'analyse multidimensionnelle.
    Combine les données provenant de différentes dimensions d'analyse (statistique, ésotérique, comportementale)
    pour générer une prédiction holistique tenant compte de toutes les perspectives.
    """
    
    def __init__(self):
        """Initialise le module MultidimensionalAnalyzer"""
        # Paramètres de l'analyse
        self.analysis_params = {
            'statistical_weight': 0.4,       # Poids de la dimension statistique
            'esoteric_weight': 0.3,          # Poids de la dimension ésotérique
            'behavioral_weight': 0.3,        # Poids de la dimension comportementale
            'convergence_threshold': 0.7,    # Seuil pour considérer une convergence significative
            'divergence_threshold': 0.5,     # Seuil pour considérer une divergence significative
            'minimum_confidence': 0.6,       # Confiance minimale pour une prédiction
            'dimension_reliability': {        # Fiabilité relative de chaque dimension
                'statistical': 0.85,
                'esoteric': 0.75, 
                'behavioral': 0.8
            }
        }
        
        # Sources de données par dimension
        self.data_sources = {
            'statistical': [
                'match_history',
                'current_form',
                'head_to_head',
                'league_position',
                'goal_statistics',
                'player_stats',
                'team_xG'
            ],
            'esoteric': [
                'numerological_analysis',
                'tarot_insights',
                'astrological_influences',
                'karmic_patterns',
                'cyclical_echoes',
                'geometric_patterns'
            ],
            'behavioral': [
                'team_psychology',
                'crowd_pressure',
                'momentum_shifts',
                'clutch_performance',
                'collapse_tendency',
                'fan_sentiment',
                'media_pressure'
            ]
        }
        
        # Historique des analyses
        self.analysis_history = []
        
    def perform_multidimensional_analysis(self, match_data, statistical_data=None, esoteric_data=None, behavioral_data=None):
        """
        Effectuer une analyse multidimensionnelle complète pour un match.
        
        Args:
            match_data (dict): Données du match
            statistical_data (dict, optional): Données statistiques disponibles
            esoteric_data (dict, optional): Données ésotériques disponibles
            behavioral_data (dict, optional): Données comportementales disponibles
            
        Returns:
            dict: Analyse multidimensionnelle complète
        """
        # Extraire les noms des équipes
        team1_name = match_data.get('home_team', 'Équipe 1')
        team2_name = match_data.get('away_team', 'Équipe 2')
        
        # Obtenir ou générer les données statistiques
        statistical_analysis = self._analyze_statistical_dimension(
            team1_name, team2_name, match_data, statistical_data
        )
        
        # Obtenir ou générer les données ésotériques
        esoteric_analysis = self._analyze_esoteric_dimension(
            team1_name, team2_name, match_data, esoteric_data
        )
        
        # Obtenir ou générer les données comportementales
        behavioral_analysis = self._analyze_behavioral_dimension(
            team1_name, team2_name, match_data, behavioral_data
        )
        
        # Analyser les convergences et divergences
        convergence_analysis = self._analyze_dimensional_convergence(
            statistical_analysis, esoteric_analysis, behavioral_analysis
        )
        
        # Générer la prédiction multidimensionnelle
        multidimensional_prediction = self._generate_multidimensional_prediction(
            statistical_analysis, esoteric_analysis, behavioral_analysis, convergence_analysis
        )
        
        # Évaluer les indices de confiance
        confidence_analysis = self._evaluate_confidence_metrics(
            statistical_analysis, esoteric_analysis, behavioral_analysis, convergence_analysis
        )
        
        # Identifier les signaux contradictoires
        contradictory_signals = self._identify_contradictory_signals(
            statistical_analysis, esoteric_analysis, behavioral_analysis
        )
        
        # Compiler l'analyse complète
        analysis = {
            'match': f"{team1_name} vs {team2_name}",
            'analysis_timestamp': datetime.now().isoformat(),
            'match_date': match_data.get('date', datetime.now().isoformat()),
            'statistical_analysis': statistical_analysis,
            'esoteric_analysis': esoteric_analysis,
            'behavioral_analysis': behavioral_analysis,
            'convergence_analysis': convergence_analysis,
            'multidimensional_prediction': multidimensional_prediction,
            'confidence_metrics': confidence_analysis,
            'contradictory_signals': contradictory_signals
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'multidimensional_analysis',
            'timestamp': datetime.now().isoformat(),
            'match': f"{team1_name} vs {team2_name}",
            'prediction': multidimensional_prediction.get('prediction'),
            'confidence': confidence_analysis.get('overall_confidence', 0)
        })
        
        return analysis
    
    def analyze_dimensional_alignment(self, team_name, timeframe='recent', specific_event=None):
        """
        Analyser l'alignement des différentes dimensions pour une équipe sur une période donnée.
        
        Args:
            team_name (str): Nom de l'équipe
            timeframe (str): Période d'analyse ('recent', 'season', 'historical')
            specific_event (dict, optional): Événement spécifique à analyser
            
        Returns:
            dict: Analyse de l'alignement dimensionnel
        """
        # Base de l'analyse
        alignment_analysis = {
            'team_name': team_name,
            'timeframe': timeframe,
            'analysis_timestamp': datetime.now().isoformat(),
            'dimensional_alignments': [],
            'overall_alignment': 0.0,
            'alignment_stability': 0.0,
            'significant_patterns': []
        }
        
        # Générer des données historiques d'alignement
        historical_alignments = self._generate_historical_alignments(team_name, timeframe, specific_event)
        
        # Calculer l'alignement global
        overall_alignment = self._calculate_overall_alignment(historical_alignments)
        alignment_analysis['overall_alignment'] = overall_alignment
        
        # Calculer la stabilité de l'alignement
        alignment_stability = self._calculate_alignment_stability(historical_alignments)
        alignment_analysis['alignment_stability'] = alignment_stability
        
        # Identifier les patterns significatifs
        significant_patterns = self._identify_alignment_patterns(historical_alignments, team_name)
        alignment_analysis['significant_patterns'] = significant_patterns
        
        # Évaluer l'impact sur les performances
        performance_impact = self._evaluate_alignment_performance_impact(
            overall_alignment, alignment_stability, historical_alignments
        )
        alignment_analysis['performance_impact'] = performance_impact
        
        # Prédire les tendances futures
        future_trends = self._predict_alignment_trends(
            historical_alignments, overall_alignment, alignment_stability
        )
        alignment_analysis['future_trends'] = future_trends
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'dimensional_alignment_analysis',
            'timestamp': datetime.now().isoformat(),
            'team': team_name,
            'overall_alignment': overall_alignment,
            'alignment_stability': alignment_stability
        })
        
        return alignment_analysis
    
    def detect_dimensional_anomalies(self, match_data, analysis_window=5):
        """
        Détecter les anomalies dans l'alignement dimensionnel.
        
        Args:
            match_data (dict): Données du match
            analysis_window (int): Fenêtre d'analyse (nombre d'événements)
            
        Returns:
            dict: Analyse des anomalies dimensionnelles
        """
        # Extraire les noms des équipes
        team1_name = match_data.get('home_team', 'Équipe 1')
        team2_name = match_data.get('away_team', 'Équipe 2')
        
        # Base de l'analyse
        anomaly_analysis = {
            'match': f"{team1_name} vs {team2_name}",
            'analysis_timestamp': datetime.now().isoformat(),
            'match_date': match_data.get('date', datetime.now().isoformat()),
            'anomalies_detected': False,
            'anomalies': [],
            'anomaly_significance': 0.0,
            'potential_impact': {}
        }
        
        # Générer des données récentes
        recent_team1_data = self._generate_recent_dimensional_data(team1_name, analysis_window)
        recent_team2_data = self._generate_recent_dimensional_data(team2_name, analysis_window)
        
        # Détecter les anomalies pour chaque équipe
        team1_anomalies = self._detect_team_anomalies(team1_name, recent_team1_data)
        team2_anomalies = self._detect_team_anomalies(team2_name, recent_team2_data)
        
        # Compiler les anomalies
        all_anomalies = team1_anomalies + team2_anomalies
        
        # Mettre à jour l'analyse
        if all_anomalies:
            anomaly_analysis['anomalies_detected'] = True
            anomaly_analysis['anomalies'] = all_anomalies
            
            # Calculer la signification globale
            significance_scores = [a.get('significance', 0) for a in all_anomalies]
            if significance_scores:
                anomaly_analysis['anomaly_significance'] = sum(significance_scores) / len(significance_scores)
        
            # Évaluer l'impact potentiel
            anomaly_analysis['potential_impact'] = self._evaluate_anomaly_impact(
                all_anomalies, team1_name, team2_name, match_data
            )
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'dimensional_anomaly_detection',
            'timestamp': datetime.now().isoformat(),
            'match': f"{team1_name} vs {team2_name}",
            'anomalies_detected': anomaly_analysis['anomalies_detected'],
            'anomaly_significance': anomaly_analysis['anomaly_significance']
        })
        
        return anomaly_analysis
    
    def evaluate_cross_dimensional_synergy(self, team1_name, team2_name, match_context=None):
        """
        Évaluer les synergies entre dimensions pour deux équipes.
        
        Args:
            team1_name (str): Nom de la première équipe
            team2_name (str): Nom de la deuxième équipe
            match_context (dict, optional): Contexte du match
            
        Returns:
            dict: Analyse des synergies dimensionnelles
        """
        # Base de l'analyse
        synergy_analysis = {
            'teams': f"{team1_name} vs {team2_name}",
            'analysis_timestamp': datetime.now().isoformat(),
            'team1_synergies': {},
            'team2_synergies': {},
            'comparative_advantage': None,
            'synergy_patterns': []
        }
        
        # Analyser les synergies pour chaque équipe
        team1_synergies = self._analyze_team_synergies(team1_name)
        team2_synergies = self._analyze_team_synergies(team2_name)
        
        synergy_analysis['team1_synergies'] = team1_synergies
        synergy_analysis['team2_synergies'] = team2_synergies
        
        # Déterminer l'avantage comparatif
        synergy_analysis['comparative_advantage'] = self._determine_synergy_advantage(
            team1_name, team2_name, team1_synergies, team2_synergies, match_context
        )
        
        # Identifier les patterns de synergie
        synergy_analysis['synergy_patterns'] = self._identify_synergy_patterns(
            team1_synergies, team2_synergies, match_context
        )
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'cross_dimensional_synergy',
            'timestamp': datetime.now().isoformat(),
            'teams': f"{team1_name} vs {team2_name}",
            'comparative_advantage': synergy_analysis['comparative_advantage'].get('team') if synergy_analysis['comparative_advantage'] else None
        })
        
        return synergy_analysis
    
    def _analyze_statistical_dimension(self, team1_name, team2_name, match_data, statistical_data=None):
        """Analyser la dimension statistique."""
        # Si des données sont fournies, les utiliser
        if statistical_data:
            return statistical_data
        
        # Générer des données simulées pour la dimension statistique
        return {
            'dimension': 'statistical',
            'sources_analyzed': self.data_sources['statistical'],
            'team1_analysis': {
                'form': random.uniform(0.3, 0.9),
                'expected_goals': random.uniform(0.8, 2.5),
                'defense_rating': random.uniform(0.4, 0.9),
                'attack_rating': random.uniform(0.4, 0.9),
                'home_advantage': random.uniform(0.1, 0.3) if match_data.get('home_team') == team1_name else 0,
                'key_player_impact': random.uniform(0.5, 0.9)
            },
            'team2_analysis': {
                'form': random.uniform(0.3, 0.9),
                'expected_goals': random.uniform(0.8, 2.5),
                'defense_rating': random.uniform(0.4, 0.9),
                'attack_rating': random.uniform(0.4, 0.9),
                'home_advantage': random.uniform(0.1, 0.3) if match_data.get('home_team') == team2_name else 0,
                'key_player_impact': random.uniform(0.5, 0.9)
            },
            'head_to_head': {
                'historical_advantage': random.choice(['team1', 'team2', 'neutral']),
                'average_goals': random.uniform(1.5, 3.5),
                'similarity_to_previous': random.uniform(0.3, 0.8)
            },
            'prediction': {
                'win_probability': {
                    'team1': random.uniform(0.2, 0.7),
                    'team2': random.uniform(0.2, 0.7),
                    'draw': random.uniform(0.1, 0.3)
                },
                'expected_score': {
                    'team1': random.uniform(0.5, 2.5),
                    'team2': random.uniform(0.5, 2.5)
                },
                'confidence': random.uniform(0.6, 0.9)
            }
        }
    
    def _analyze_esoteric_dimension(self, team1_name, team2_name, match_data, esoteric_data=None):
        """Analyser la dimension ésotérique."""
        # Si des données sont fournies, les utiliser
        if esoteric_data:
            return esoteric_data
        
        # Générer des données simulées pour la dimension ésotérique
        return {
            'dimension': 'esoteric',
            'sources_analyzed': self.data_sources['esoteric'],
            'numerological_analysis': {
                'team1_number': random.randint(1, 9),
                'team2_number': random.randint(1, 9),
                'match_day_vibration': random.randint(1, 9),
                'compatibility': random.uniform(0.3, 0.9)
            },
            'astrological_influences': {
                'favorable_team': random.choice(['team1', 'team2', 'neutral']),
                'planetary_positions': random.choice(['supportive', 'challenging', 'neutral']),
                'influence_strength': random.uniform(0.3, 0.8)
            },
            'karmic_patterns': {
                'team1_karma': random.uniform(-0.5, 0.5),
                'team2_karma': random.uniform(-0.5, 0.5),
                'karmic_balance': random.choice(['team1_debt', 'team2_debt', 'balanced']),
                'cycle_position': random.choice(['ascending', 'peak', 'descending', 'trough'])
            },
            'cyclical_echoes': {
                'historical_resonance': random.uniform(0.3, 0.9),
                'pattern_strength': random.uniform(0.4, 0.8),
                'echo_significance': random.uniform(0.5, 0.9)
            },
            'prediction': {
                'favored_outcome': random.choice(['team1_win', 'team2_win', 'draw', 'unpredictable']),
                'alignment_score': {
                    'team1': random.uniform(0.3, 0.9),
                    'team2': random.uniform(0.3, 0.9)
                },
                'confidence': random.uniform(0.5, 0.85)
            }
        }
    
    def _analyze_behavioral_dimension(self, team1_name, team2_name, match_data, behavioral_data=None):
        """Analyser la dimension comportementale."""
        # Si des données sont fournies, les utiliser
        if behavioral_data:
            return behavioral_data
        
        # Générer des données simulées pour la dimension comportementale
        return {
            'dimension': 'behavioral',
            'sources_analyzed': self.data_sources['behavioral'],
            'team_psychology': {
                'team1_mental_state': random.choice(['confident', 'anxious', 'determined', 'pressured', 'relaxed']),
                'team2_mental_state': random.choice(['confident', 'anxious', 'determined', 'pressured', 'relaxed']),
                'psychological_advantage': random.choice(['team1', 'team2', 'neutral'])
            },
            'pressure_factors': {
                'team1_pressure': random.uniform(0.2, 0.9),
                'team2_pressure': random.uniform(0.2, 0.9),
                'crowd_influence': random.uniform(0.1, 0.4) if match_data.get('attendance', 0) > 10000 else random.uniform(0, 0.2),
                'media_pressure': random.uniform(0.2, 0.7)
            },
            'momentum_analysis': {
                'current_momentum': random.choice(['team1', 'team2', 'neutral']),
                'momentum_strength': random.uniform(0.3, 0.8),
                'momentum_stability': random.uniform(0.4, 0.9)
            },
            'fan_sentiment': {
                'team1_fan_optimism': random.uniform(0.3, 0.9),
                'team2_fan_optimism': random.uniform(0.3, 0.9),
                'sentiment_impact': random.uniform(0.1, 0.4)
            },
            'prediction': {
                'behavioral_edge': random.choice(['team1', 'team2', 'neutral']),
                'performance_under_pressure': {
                    'team1': random.uniform(0.4, 0.9),
                    'team2': random.uniform(0.4, 0.9)
                },
                'confidence': random.uniform(0.6, 0.85)
            }
        }
    
    def _analyze_dimensional_convergence(self, statistical_analysis, esoteric_analysis, behavioral_analysis):
        """Analyser les convergences et divergences entre dimensions."""
        # Base de l'analyse
        convergence_analysis = {
            'convergence_detected': False,
            'overall_convergence': 0.0,
            'converging_dimensions': [],
            'divergent_dimensions': [],
            'neutral_dimensions': [],
            'strongest_signal': None
        }
        
        # Extraire les prédictions de chaque dimension
        statistical_prediction = self._extract_dimension_prediction(statistical_analysis)
        esoteric_prediction = self._extract_dimension_prediction(esoteric_analysis)
        behavioral_prediction = self._extract_dimension_prediction(behavioral_analysis)
        
        # Calculer les scores de convergence entre dimensions
        stat_eso_convergence = self._calculate_prediction_convergence(
            statistical_prediction, esoteric_prediction
        )
        
        stat_behav_convergence = self._calculate_prediction_convergence(
            statistical_prediction, behavioral_prediction
        )
        
        eso_behav_convergence = self._calculate_prediction_convergence(
            esoteric_prediction, behavioral_prediction
        )
        
        # Déterminer les dimensions convergentes
        if stat_eso_convergence > self.analysis_params['convergence_threshold']:
            convergence_analysis['converging_dimensions'].append({
                'dimensions': ['statistical', 'esoteric'],
                'convergence_score': stat_eso_convergence,
                'prediction': self._determine_combined_prediction(statistical_prediction, esoteric_prediction)
            })
        elif stat_eso_convergence < self.analysis_params['divergence_threshold']:
            convergence_analysis['divergent_dimensions'].append({
                'dimensions': ['statistical', 'esoteric'],
                'divergence_score': 1 - stat_eso_convergence
            })
        else:
            convergence_analysis['neutral_dimensions'].append({
                'dimensions': ['statistical', 'esoteric'],
                'relation_score': stat_eso_convergence
            })
        
        if stat_behav_convergence > self.analysis_params['convergence_threshold']:
            convergence_analysis['converging_dimensions'].append({
                'dimensions': ['statistical', 'behavioral'],
                'convergence_score': stat_behav_convergence,
                'prediction': self._determine_combined_prediction(statistical_prediction, behavioral_prediction)
            })
        elif stat_behav_convergence < self.analysis_params['divergence_threshold']:
            convergence_analysis['divergent_dimensions'].append({
                'dimensions': ['statistical', 'behavioral'],
                'divergence_score': 1 - stat_behav_convergence
            })
        else:
            convergence_analysis['neutral_dimensions'].append({
                'dimensions': ['statistical', 'behavioral'],
                'relation_score': stat_behav_convergence
            })
        
        if eso_behav_convergence > self.analysis_params['convergence_threshold']:
            convergence_analysis['converging_dimensions'].append({
                'dimensions': ['esoteric', 'behavioral'],
                'convergence_score': eso_behav_convergence,
                'prediction': self._determine_combined_prediction(esoteric_prediction, behavioral_prediction)
            })
        elif eso_behav_convergence < self.analysis_params['divergence_threshold']:
            convergence_analysis['divergent_dimensions'].append({
                'dimensions': ['esoteric', 'behavioral'],
                'divergence_score': 1 - eso_behav_convergence
            })
        else:
            convergence_analysis['neutral_dimensions'].append({
                'dimensions': ['esoteric', 'behavioral'],
                'relation_score': eso_behav_convergence
            })
        
        # Calculer la convergence globale
        all_convergences = [stat_eso_convergence, stat_behav_convergence, eso_behav_convergence]
        convergence_analysis['overall_convergence'] = sum(all_convergences) / len(all_convergences)
        
        # Déterminer si une convergence est détectée
        convergence_analysis['convergence_detected'] = len(convergence_analysis['converging_dimensions']) > 0
        
        # Déterminer le signal le plus fort
        if convergence_analysis['converging_dimensions']:
            strongest_convergence = max(convergence_analysis['converging_dimensions'], 
                                        key=lambda x: x.get('convergence_score', 0))
            strongest_signal = {
                'type': 'convergence',
                'dimensions': strongest_convergence['dimensions'],
                'strength': strongest_convergence['convergence_score'],
                'prediction': strongest_convergence['prediction']
            }
        elif convergence_analysis['divergent_dimensions']:
            strongest_divergence = max(convergence_analysis['divergent_dimensions'], 
                                     key=lambda x: x.get('divergence_score', 0))
            strongest_signal = {
                'type': 'divergence',
                'dimensions': strongest_divergence['dimensions'],
                'strength': strongest_divergence['divergence_score'],
                'message': "Signaux contradictoires entre dimensions"
            }
        else:
            strongest_signal = {
                'type': 'neutral',
                'dimensions': ['statistical', 'esoteric', 'behavioral'],
                'strength': max(all_convergences),
                'message': "Pas de signal fort détecté entre les dimensions"
            }
        
        convergence_analysis['strongest_signal'] = strongest_signal
        
        return convergence_analysis
    
    def _generate_multidimensional_prediction(self, statistical_analysis, esoteric_analysis, behavioral_analysis, convergence_analysis):
        """Générer une prédiction en combinant les différentes dimensions."""
        # Base de la prédiction
        multidim_prediction = {
            'prediction': None,
            'win_probability': {
                'team1': 0.0,
                'draw': 0.0,
                'team2': 0.0
            },
            'confidence': 0.0,
            'key_factors': [],
            'dimension_contributions': {}
        }
        
        # Extraire les prédictions de chaque dimension
        statistical_prediction = self._extract_dimension_prediction(statistical_analysis)
        esoteric_prediction = self._extract_dimension_prediction(esoteric_analysis)
        behavioral_prediction = self._extract_dimension_prediction(behavioral_analysis)
        
        # Calculer les poids relatifs basés sur la fiabilité et la convergence
        stat_reliability = self.analysis_params['dimension_reliability']['statistical']
        eso_reliability = self.analysis_params['dimension_reliability']['esoteric']
        behav_reliability = self.analysis_params['dimension_reliability']['behavioral']
        
        # Ajuster les poids en fonction de la convergence
        if convergence_analysis['converging_dimensions']:
            for conv in convergence_analysis['converging_dimensions']:
                if 'statistical' in conv['dimensions']:
                    stat_reliability *= (1 + 0.2 * conv['convergence_score'])
                if 'esoteric' in conv['dimensions']:
                    eso_reliability *= (1 + 0.2 * conv['convergence_score'])
                if 'behavioral' in conv['dimensions']:
                    behav_reliability *= (1 + 0.2 * conv['convergence_score'])
        
        # Normaliser les poids
        total_reliability = stat_reliability + eso_reliability + behav_reliability
        stat_weight = stat_reliability / total_reliability * self.analysis_params['statistical_weight']
        eso_weight = eso_reliability / total_reliability * self.analysis_params['esoteric_weight']
        behav_weight = behav_reliability / total_reliability * self.analysis_params['behavioral_weight']
        
        # Enregistrer les contributions de chaque dimension
        multidim_prediction['dimension_contributions'] = {
            'statistical': stat_weight,
            'esoteric': eso_weight,
            'behavioral': behav_weight
        }
        
        # Calculer les probabilités pondérées
        team1_win_prob = (
            statistical_prediction['win_probability']['team1'] * stat_weight +
            esoteric_prediction['win_probability']['team1'] * eso_weight +
            behavioral_prediction['win_probability']['team1'] * behav_weight
        )
        
        team2_win_prob = (
            statistical_prediction['win_probability']['team2'] * stat_weight +
            esoteric_prediction['win_probability']['team2'] * eso_weight +
            behavioral_prediction['win_probability']['team2'] * behav_weight
        )
        
        draw_prob = (
            statistical_prediction['win_probability']['draw'] * stat_weight +
            esoteric_prediction['win_probability']['draw'] * eso_weight +
            behavioral_prediction['win_probability']['draw'] * behav_weight
        )
        
        # Normaliser les probabilités
        total_prob = team1_win_prob + team2_win_prob + draw_prob
        team1_win_prob /= total_prob
        team2_win_prob /= total_prob
        draw_prob /= total_prob
        
        multidim_prediction['win_probability'] = {
            'team1': team1_win_prob,
            'draw': draw_prob,
            'team2': team2_win_prob
        }
        
        # Déterminer la prédiction
        if team1_win_prob > team2_win_prob and team1_win_prob > draw_prob:
            multidim_prediction['prediction'] = 'team1_win'
        elif team2_win_prob > team1_win_prob and team2_win_prob > draw_prob:
            multidim_prediction['prediction'] = 'team2_win'
        else:
            multidim_prediction['prediction'] = 'draw'
        
        # Calculer la confiance
        if convergence_analysis['convergence_detected']:
            # Haute confiance si convergence
            top_convergence = max(convergence_analysis['converging_dimensions'], 
                                key=lambda x: x.get('convergence_score', 0))
            
            confidence_boost = top_convergence['convergence_score'] * 0.2
            base_confidence = max(
                statistical_prediction['confidence'],
                esoteric_prediction['confidence'],
                behavioral_prediction['confidence']
            )
            
            multidim_prediction['confidence'] = min(0.99, base_confidence + confidence_boost)
        else:
            # Confiance moyenne pondérée si pas de convergence claire
            multidim_prediction['confidence'] = (
                statistical_prediction['confidence'] * stat_weight +
                esoteric_prediction['confidence'] * eso_weight +
                behavioral_prediction['confidence'] * behav_weight
            )
        
        # Identifier les facteurs clés
        if convergence_analysis['strongest_signal']['type'] == 'convergence':
            dimensions = convergence_analysis['strongest_signal']['dimensions']
            multidim_prediction['key_factors'].append({
                'type': 'convergence',
                'description': f"Forte convergence entre les dimensions {' et '.join(dimensions)}",
                'strength': convergence_analysis['strongest_signal']['strength']
            })
        
        # Ajouter les facteurs spécifiques à chaque dimension
        self._add_dimension_key_factors(multidim_prediction['key_factors'], statistical_analysis, 'statistical')
        self._add_dimension_key_factors(multidim_prediction['key_factors'], esoteric_analysis, 'esoteric')
        self._add_dimension_key_factors(multidim_prediction['key_factors'], behavioral_analysis, 'behavioral')
        
        # Trier par importance
        multidim_prediction['key_factors'].sort(key=lambda x: x.get('strength', 0), reverse=True)
        
        return multidim_prediction
    
    def _evaluate_confidence_metrics(self, statistical_analysis, esoteric_analysis, behavioral_analysis, convergence_analysis):
        """Évaluer les indices de confiance de l'analyse."""
        # Base de l'évaluation
        confidence_metrics = {
            'overall_confidence': 0.0,
            'dimension_confidence': {
                'statistical': statistical_analysis.get('prediction', {}).get('confidence', 0.5),
                'esoteric': esoteric_analysis.get('prediction', {}).get('confidence', 0.5),
                'behavioral': behavioral_analysis.get('prediction', {}).get('confidence', 0.5)
            },
            'convergence_confidence': convergence_analysis.get('overall_convergence', 0.5),
            'reliability_metrics': {},
            'confidence_adjustments': []
        }
        
        # Calculer la confiance globale
        base_confidence = (
            confidence_metrics['dimension_confidence']['statistical'] * self.analysis_params['statistical_weight'] +
            confidence_metrics['dimension_confidence']['esoteric'] * self.analysis_params['esoteric_weight'] +
            confidence_metrics['dimension_confidence']['behavioral'] * self.analysis_params['behavioral_weight']
        )
        
        # Ajuster en fonction de la convergence
        convergence_adjustment = 0.0
        if convergence_analysis['convergence_detected']:
            convergence_adjustment = (convergence_analysis['overall_convergence'] - 0.5) * 0.4
        
        # Appliquer l'ajustement
        confidence_metrics['overall_confidence'] = min(0.99, max(0.1, base_confidence + convergence_adjustment))
        
        if convergence_adjustment != 0:
            confidence_metrics['confidence_adjustments'].append({
                'type': 'convergence_adjustment',
                'value': convergence_adjustment,
                'description': "Ajustement basé sur la convergence entre dimensions"
            })
        
        # Calculer des métriques de fiabilité
        confidence_metrics['reliability_metrics'] = {
            'dimension_consistency': self._calculate_dimension_consistency(
                statistical_analysis, esoteric_analysis, behavioral_analysis
            ),
            'historical_accuracy': random.uniform(0.6, 0.9),  # Simulé
            'data_completeness': self._calculate_data_completeness(
                statistical_analysis, esoteric_analysis, behavioral_analysis
            )
        }
        
        # Ajuster la confiance si nécessaire en fonction des métriques de fiabilité
        if confidence_metrics['reliability_metrics']['dimension_consistency'] < 0.4:
            consistency_penalty = -0.1
            confidence_metrics['overall_confidence'] = max(0.1, confidence_metrics['overall_confidence'] + consistency_penalty)
            confidence_metrics['confidence_adjustments'].append({
                'type': 'consistency_penalty',
                'value': consistency_penalty,
                'description': "Pénalité due à la faible cohérence entre dimensions"
            })
        
        if confidence_metrics['reliability_metrics']['data_completeness'] < 0.7:
            completeness_penalty = -0.15
            confidence_metrics['overall_confidence'] = max(0.1, confidence_metrics['overall_confidence'] + completeness_penalty)
            confidence_metrics['confidence_adjustments'].append({
                'type': 'completeness_penalty',
                'value': completeness_penalty,
                'description': "Pénalité due à des données incomplètes"
            })
        
        return confidence_metrics
    
    def _identify_contradictory_signals(self, statistical_analysis, esoteric_analysis, behavioral_analysis):
        """Identifier les signaux contradictoires entre les dimensions."""
        # Base de l'analyse
        contradictions = []
        
        # Extraire les prédictions
        stat_pred = statistical_analysis.get('prediction', {}).get('win_probability', {})
        eso_pred = esoteric_analysis.get('prediction', {}).get('win_probability', {})
        behav_pred = behavioral_analysis.get('prediction', {}).get('win_probability', {})
        
        # Extraire les prédictions de résultat
        stat_result = self._get_predicted_result(stat_pred)
        eso_result = self._get_predicted_result(eso_pred)
        behav_result = self._get_predicted_result(behav_pred)
        
        # Comparer les résultats entre dimensions
        if stat_result != eso_result:
            contradictions.append({
                'dimensions': ['statistical', 'esoteric'],
                'contradiction_type': 'result',
                'values': [stat_result, eso_result],
                'significance': min(
                    statistical_analysis.get('prediction', {}).get('confidence', 0.5),
                    esoteric_analysis.get('prediction', {}).get('confidence', 0.5)
                )
            })
        
        if stat_result != behav_result:
            contradictions.append({
                'dimensions': ['statistical', 'behavioral'],
                'contradiction_type': 'result',
                'values': [stat_result, behav_result],
                'significance': min(
                    statistical_analysis.get('prediction', {}).get('confidence', 0.5),
                    behavioral_analysis.get('prediction', {}).get('confidence', 0.5)
                )
            })
        
        if eso_result != behav_result:
            contradictions.append({
                'dimensions': ['esoteric', 'behavioral'],
                'contradiction_type': 'result',
                'values': [eso_result, behav_result],
                'significance': min(
                    esoteric_analysis.get('prediction', {}).get('confidence', 0.5),
                    behavioral_analysis.get('prediction', {}).get('confidence', 0.5)
                )
            })
        
        # Comparer des facteurs spécifiques
        # Exemple: Momentum
        stat_momentum = statistical_analysis.get('team1_analysis', {}).get('form', 0) > statistical_analysis.get('team2_analysis', {}).get('form', 0)
        behav_momentum = behavioral_analysis.get('momentum_analysis', {}).get('current_momentum', 'neutral') == 'team1'
        
        if stat_momentum != behav_momentum:
            contradictions.append({
                'dimensions': ['statistical', 'behavioral'],
                'contradiction_type': 'momentum',
                'description': "Contradiction sur l'équipe ayant le momentum",
                'significance': 0.7
            })
        
        return contradictions
    
    def _generate_historical_alignments(self, team_name, timeframe, specific_event=None):
        """Générer des données historiques d'alignement dimensionnel."""
        # Déterminer le nombre de points selon la période
        if timeframe == 'recent':
            num_points = 10
        elif timeframe == 'season':
            num_points = 30
        else:  # historical
            num_points = 50
        
        # Générer des données simulées
        alignments = []
        
        base_date = datetime.now() - timedelta(days=num_points * 7)
        
        for i in range(num_points):
            point_date = (base_date + timedelta(days=i * 7)).isoformat()
            
            # Générer des valeurs d'alignement
            stat_eso_alignment = random.uniform(0.3, 0.9)
            stat_behav_alignment = random.uniform(0.3, 0.9)
            eso_behav_alignment = random.uniform(0.3, 0.9)
            
            # Calculer l'alignement global
            overall_alignment = (stat_eso_alignment + stat_behav_alignment + eso_behav_alignment) / 3
            
            alignments.append({
                'date': point_date,
                'match_context': {
                    'opponent': f"Équipe {random.randint(1, 20)}",
                    'result': random.choice(['win', 'draw', 'loss']),
                    'score': [random.randint(0, 3), random.randint(0, 3)]
                },
                'dimensional_alignments': {
                    'statistical_esoteric': stat_eso_alignment,
                    'statistical_behavioral': stat_behav_alignment,
                    'esoteric_behavioral': eso_behav_alignment
                },
                'overall_alignment': overall_alignment,
                'performance_correlation': random.uniform(-0.3, 0.9)
            })
        
        # Trier par date
        alignments.sort(key=lambda a: a.get('date', ''))
        
        return alignments
    
    def _calculate_overall_alignment(self, historical_alignments):
        """Calculer l'alignement global des dimensions."""
        if not historical_alignments:
            return 0.5
        
        # Calculer la moyenne des alignements récents avec une pondération plus forte pour les plus récents
        recent_alignments = historical_alignments[-5:]  # 5 derniers points
        
        if not recent_alignments:
            return 0.5
        
        total_weight = 0
        weighted_sum = 0
        
        for i, alignment in enumerate(recent_alignments):
            weight = i + 1  # Plus récent = plus de poids
            weighted_sum += alignment.get('overall_alignment', 0.5) * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.5
    
    def _calculate_alignment_stability(self, historical_alignments):
        """Calculer la stabilité de l'alignement."""
        if not historical_alignments or len(historical_alignments) < 3:
            return 0.5
        
        # Extraire les valeurs d'alignement global
        alignment_values = [a.get('overall_alignment', 0.5) for a in historical_alignments]
        
        # Calculer la variance
        variance = np.var(alignment_values)
        
        # Convertir en score de stabilité (inversement proportionnel à la variance)
        stability = max(0.1, min(1.0, 1.0 - variance * 2))
        
        return stability
    
    def _identify_alignment_patterns(self, historical_alignments, team_name):
        """Identifier des patterns significatifs dans l'alignement dimensionnel."""
        if not historical_alignments or len(historical_alignments) < 5:
            return []
        
        patterns = []
        
        # Pattern 1: Tendance récente
        recent_alignments = historical_alignments[-5:]
        first_value = recent_alignments[0].get('overall_alignment', 0.5)
        last_value = recent_alignments[-1].get('overall_alignment', 0.5)
        
        if abs(last_value - first_value) > 0.2:
            trend_direction = 'improving' if last_value > first_value else 'deteriorating'
            patterns.append({
                'pattern_type': 'recent_trend',
                'direction': trend_direction,
                'magnitude': abs(last_value - first_value),
                'description': f"Tendance {trend_direction} de l'alignement dimensionnel"
            })
        
        # Pattern 2: Corrélation avec les performances
        performance_correlations = [a.get('performance_correlation', 0) for a in historical_alignments]
        avg_correlation = sum(performance_correlations) / len(performance_correlations)
        
        if abs(avg_correlation) > 0.3:
            correlation_type = 'positive' if avg_correlation > 0 else 'negative'
            patterns.append({
                'pattern_type': 'performance_correlation',
                'correlation_type': correlation_type,
                'strength': abs(avg_correlation),
                'description': f"Corrélation {correlation_type} entre alignement et performance"
            })
        
        # Pattern 3: Cycles d'alignement
        # Analyse simplifiée pour détecter des patterns cycliques
        alignment_values = [a.get('overall_alignment', 0.5) for a in historical_alignments]
        cycle_detected = False
        cycle_length = 0
        
        # Recherche simplifiée de cycles
        for cycle_size in range(3, min(10, len(alignment_values) // 2)):
            if self._detect_cycle(alignment_values, cycle_size):
                cycle_detected = True
                cycle_length = cycle_size
                break
        
        if cycle_detected:
            patterns.append({
                'pattern_type': 'alignment_cycle',
                'cycle_length': cycle_length,
                'description': f"Cycle d'alignement dimensionnel de période {cycle_length}",
                'current_phase': len(alignment_values) % cycle_length
            })
        
        # Trier par importance
        patterns.sort(key=lambda p: p.get('magnitude', p.get('strength', 0)), reverse=True)
        
        return patterns
    
    def _evaluate_alignment_performance_impact(self, overall_alignment, alignment_stability, historical_alignments):
        """Évaluer l'impact de l'alignement sur les performances."""
        # Base de l'évaluation
        impact = {
            'impact_score': 0.0,
            'impact_type': 'neutral',
            'key_factors': [],
            'recommendations': []
        }
        
        # Calculer le score d'impact
        impact_score = (overall_alignment - 0.5) * 2  # -1 à 1
        
        # Ajuster en fonction de la stabilité
        if alignment_stability < 0.4:
            impact_score *= 0.7  # Réduire l'impact si instable
            impact['key_factors'].append({
                'factor_type': 'alignment_instability',
                'description': "L'instabilité de l'alignement réduit son impact prédictif",
                'adjustment': -0.3
            })
        elif alignment_stability > 0.7:
            impact_score *= 1.2  # Augmenter l'impact si stable
            impact['key_factors'].append({
                'factor_type': 'alignment_stability',
                'description': "La stabilité de l'alignement renforce son impact prédictif",
                'adjustment': 0.2
            })
        
        # Déterminer le type d'impact
        if impact_score > 0.3:
            impact['impact_type'] = 'strongly_positive'
        elif impact_score > 0.1:
            impact['impact_type'] = 'moderately_positive'
        elif impact_score < -0.3:
            impact['impact_type'] = 'strongly_negative'
        elif impact_score < -0.1:
            impact['impact_type'] = 'moderately_negative'
        else:
            impact['impact_type'] = 'neutral'
        
        impact['impact_score'] = impact_score
        
        # Générer des recommandations
        if impact['impact_type'] in ['strongly_positive', 'moderately_positive']:
            impact['recommendations'].append(
                "Maintenir les approches actuelles qui favorisent l'alignement dimensionnel"
            )
        elif impact['impact_type'] in ['strongly_negative', 'moderately_negative']:
            impact['recommendations'].append(
                "Réévaluer les approches tactiques et psychologiques pour améliorer l'alignement"
            )
        
        if alignment_stability < 0.5:
            impact['recommendations'].append(
                "Travailler sur la consistance pour stabiliser l'alignement dimensionnel"
            )
        
        return impact
    
    def _predict_alignment_trends(self, historical_alignments, overall_alignment, alignment_stability):
        """Prédire les tendances futures de l'alignement dimensionnel."""
        # Base de la prédiction
        trends = {
            'short_term_trend': 'stable',
            'medium_term_trend': 'stable',
            'prediction_confidence': 0.6,
            'key_influences': []
        }
        
        # Analyser la tendance récente
        if len(historical_alignments) >= 5:
            recent_values = [a.get('overall_alignment', 0.5) for a in historical_alignments[-5:]]
            
            # Tendance à court terme
            first_recent = recent_values[0]
            last_recent = recent_values[-1]
            
            if last_recent > first_recent + 0.1:
                trends['short_term_trend'] = 'improving'
            elif last_recent < first_recent - 0.1:
                trends['short_term_trend'] = 'deteriorating'
            
            # Tendance à moyen terme (extrapolation simple)
            slope = (last_recent - first_recent) / 4  # Changement par période
            projected_value = last_recent + slope * 5  # Projection sur 5 périodes
            
            if projected_value > last_recent + 0.15:
                trends['medium_term_trend'] = 'improving'
            elif projected_value < last_recent - 0.15:
                trends['medium_term_trend'] = 'deteriorating'
        
        # Ajuster la confiance en fonction de la stabilité
        if alignment_stability < 0.4:
            trends['prediction_confidence'] = 0.4  # Faible confiance si instable
        elif alignment_stability > 0.7:
            trends['prediction_confidence'] = 0.8  # Haute confiance si stable
        
        # Identifier les influences clés
        influences = [
            {
                'factor': 'performance_feedback',
                'description': "Les résultats récents influencent la cohérence dimensionnelle",
                'impact': random.uniform(0.3, 0.7)
            },
            {
                'factor': 'tactical_approach',
                'description': "La cohérence tactique renforce l'alignement des dimensions",
                'impact': random.uniform(0.2, 0.6)
            },
            {
                'factor': 'external_context',
                'description': "Facteurs externes (médias, supporters) affectant l'alignement",
                'impact': random.uniform(0.1, 0.5)
            }
        ]
        
        # Trier par impact
        influences.sort(key=lambda i: i.get('impact', 0), reverse=True)
        trends['key_influences'] = influences
        
        return trends
    
    def _generate_recent_dimensional_data(self, team_name, num_points):
        """Générer des données dimensionnelles récentes pour une équipe."""
        data_points = []
        
        base_date = datetime.now() - timedelta(days=num_points * 7)
        
        for i in range(num_points):
            point_date = (base_date + timedelta(days=i * 7)).isoformat()
            
            # Générer des valeurs pour chaque dimension
            statistical_values = {
                'form': random.uniform(0.3, 0.8),
                'expected_goals': random.uniform(0.8, 2.2),
                'defense_rating': random.uniform(0.4, 0.9)
            }
            
            esoteric_values = {
                'karmic_balance': random.uniform(-0.5, 0.5),
                'cycle_position': random.choice(['ascending', 'peak', 'descending', 'trough']),
                'numerological_alignment': random.uniform(0.3, 0.9)
            }
            
            behavioral_values = {
                'team_psychology': random.choice(['confident', 'anxious', 'determined', 'pressured']),
                'momentum': random.uniform(0.3, 0.8),
                'pressure_handling': random.uniform(0.4, 0.9)
            }
            
            # Calculer l'alignement entre dimensions
            dimensional_alignment = random.uniform(0.3, 0.9)
            
            data_points.append({
                'date': point_date,
                'match_context': {
                    'opponent': f"Équipe {random.randint(1, 20)}",
                    'result': random.choice(['win', 'draw', 'loss'])
                },
                'statistical_values': statistical_values,
                'esoteric_values': esoteric_values,
                'behavioral_values': behavioral_values,
                'dimensional_alignment': dimensional_alignment
            })
        
        # Trier par date
        data_points.sort(key=lambda d: d.get('date', ''))
        
        return data_points
    
    def _detect_team_anomalies(self, team_name, recent_data):
        """Détecter les anomalies dimensionnelles pour une équipe."""
        if not recent_data or len(recent_data) < 3:
            return []
        
        anomalies = []
        
        # Valeurs récentes pour la référence
        recent_alignments = [d.get('dimensional_alignment', 0.5) for d in recent_data[-3:]]
        avg_recent_alignment = sum(recent_alignments) / len(recent_alignments)
        
        # Chercher les anomalies d'alignement
        for i, data_point in enumerate(recent_data):
            alignment = data_point.get('dimensional_alignment', 0.5)
            
            # Détecter une anomalie d'alignement
            if abs(alignment - avg_recent_alignment) > 0.25:
                anomalies.append({
                    'type': 'alignment_anomaly',
                    'date': data_point.get('date', ''),
                    'value': alignment,
                    'expected_range': [avg_recent_alignment - 0.15, avg_recent_alignment + 0.15],
                    'deviation': abs(alignment - avg_recent_alignment),
                    'significance': min(1.0, abs(alignment - avg_recent_alignment) * 2),
                    'description': "Anomalie d'alignement dimensionnel significative"
                })
        
        # Chercher les anomalies de dimension spécifique
        dimensions = ['statistical_values', 'esoteric_values', 'behavioral_values']
        
        for dimension in dimensions:
            # Extraire un indicateur clé pour chaque dimension
            if dimension == 'statistical_values':
                key_indicator = 'form'
            elif dimension == 'esoteric_values':
                key_indicator = 'karmic_balance'
            else:  # behavioral_values
                key_indicator = 'momentum'
            
            # Collecter les valeurs récentes
            recent_values = []
            for data_point in recent_data[-3:]:
                dimension_data = data_point.get(dimension, {})
                if isinstance(dimension_data, dict) and key_indicator in dimension_data:
                    recent_values.append(dimension_data[key_indicator])
            
            if not recent_values:
                continue
                
            avg_value = sum(recent_values) / len(recent_values)
            
            # Chercher les anomalies
            for i, data_point in enumerate(recent_data):
                dimension_data = data_point.get(dimension, {})
                if not isinstance(dimension_data, dict) or key_indicator not in dimension_data:
                    continue
                    
                value = dimension_data[key_indicator]
                
                if isinstance(value, (int, float)) and abs(value - avg_value) > 0.3:
                    anomalies.append({
                        'type': f'{dimension}_anomaly',
                        'date': data_point.get('date', ''),
                        'indicator': key_indicator,
                        'value': value,
                        'expected_range': [avg_value - 0.2, avg_value + 0.2],
                        'deviation': abs(value - avg_value),
                        'significance': min(1.0, abs(value - avg_value) * 1.5),
                        'description': f"Anomalie détectée dans la dimension {dimension.split('_')[0]}"
                    })
        
        # Trier par significance
        anomalies.sort(key=lambda a: a.get('significance', 0), reverse=True)
        
        return anomalies
    
    def _evaluate_anomaly_impact(self, all_anomalies, team1_name, team2_name, match_data):
        """Évaluer l'impact potentiel des anomalies détectées."""
        # Base de l'évaluation
        impact = {
            'overall_impact': 'neutral',
            'favored_team': None,
            'impact_description': '',
            'key_anomalies': []
        }
        
        if not all_anomalies:
            return impact
        
        # Séparer les anomalies par équipe
        team1_anomalies = [a for a in all_anomalies if a.get('team', '') == team1_name]
        team2_anomalies = [a for a in all_anomalies if a.get('team', '') == team2_name]
        
        # Calculer l'impact moyen par équipe
        team1_impact = 0.0
        team2_impact = 0.0
        
        for anomaly in team1_anomalies:
            # Déterminer si l'anomalie est positive ou négative
            if 'alignment_anomaly' in anomaly.get('type', ''):
                # Une anomalie positive d'alignement est favorable
                if anomaly.get('value', 0.5) > 0.7:
                    team1_impact += anomaly.get('significance', 0.5) * 0.5
                else:
                    team1_impact -= anomaly.get('significance', 0.5) * 0.5
            elif any(dim in anomaly.get('type', '') for dim in ['statistical', 'esoteric', 'behavioral']):
                # Pour les autres dimensions, dépend de l'indicateur
                indicator = anomaly.get('indicator', '')
                value = anomaly.get('value', 0)
                
                if indicator in ['form', 'momentum', 'karmic_balance'] and value > 0.7:
                    team1_impact += anomaly.get('significance', 0.5) * 0.3
                elif value < 0.3:
                    team1_impact -= anomaly.get('significance', 0.5) * 0.3
        
        for anomaly in team2_anomalies:
            # Même logique pour l'équipe 2
            if 'alignment_anomaly' in anomaly.get('type', ''):
                if anomaly.get('value', 0.5) > 0.7:
                    team2_impact += anomaly.get('significance', 0.5) * 0.5
                else:
                    team2_impact -= anomaly.get('significance', 0.5) * 0.5
            elif any(dim in anomaly.get('type', '') for dim in ['statistical', 'esoteric', 'behavioral']):
                indicator = anomaly.get('indicator', '')
                value = anomaly.get('value', 0)
                
                if indicator in ['form', 'momentum', 'karmic_balance'] and value > 0.7:
                    team2_impact += anomaly.get('significance', 0.5) * 0.3
                elif value < 0.3:
                    team2_impact -= anomaly.get('significance', 0.5) * 0.3
        
        # Déterminer l'équipe favorisée
        if team1_impact > team2_impact + 0.2:
            impact['favored_team'] = team1_name
            impact['overall_impact'] = 'positive_for_team1'
            impact['impact_description'] = f"Les anomalies dimensionnelles favorisent {team1_name}"
        elif team2_impact > team1_impact + 0.2:
            impact['favored_team'] = team2_name
            impact['overall_impact'] = 'positive_for_team2'
            impact['impact_description'] = f"Les anomalies dimensionnelles favorisent {team2_name}"
        else:
            impact['overall_impact'] = 'neutral'
            impact['impact_description'] = "Les anomalies dimensionnelles n'offrent pas d'avantage clair"
        
        # Identifier les anomalies clés
        all_anomalies.sort(key=lambda a: a.get('significance', 0), reverse=True)
        impact['key_anomalies'] = all_anomalies[:3] if len(all_anomalies) > 3 else all_anomalies
        
        return impact
    
    def _analyze_team_synergies(self, team_name):
        """Analyser les synergies dimensionnelles pour une équipe."""
        # Générer des synergies simulées
        synergies = {
            'overall_synergy': random.uniform(0.4, 0.9),
            'dimension_pairs': {
                'statistical_esoteric': random.uniform(0.3, 0.9),
                'statistical_behavioral': random.uniform(0.3, 0.9),
                'esoteric_behavioral': random.uniform(0.3, 0.9)
            },
            'key_synergy_factors': [],
            'synergy_stability': random.uniform(0.5, 0.9)
        }
        
        # Générer des facteurs de synergie
        num_factors = random.randint(2, 4)
        potential_factors = [
            {
                'factor_type': 'tactical_consistency',
                'description': "Cohérence entre approche tactique et cycle karmique",
                'strength': random.uniform(0.6, 0.9),
                'dimensions': ['statistical', 'esoteric']
            },
            {
                'factor_type': 'psychological_alignment',
                'description': "Alignement entre état psychologique et moment du cycle",
                'strength': random.uniform(0.5, 0.8),
                'dimensions': ['behavioral', 'esoteric']
            },
            {
                'factor_type': 'momentum_reinforcement',
                'description': "Momentum statistique amplifié par l'état mental collectif",
                'strength': random.uniform(0.6, 0.9),
                'dimensions': ['statistical', 'behavioral']
            },
            {
                'factor_type': 'temporal_harmony',
                'description': "Harmonie entre timing des performances et cycles temporels",
                'strength': random.uniform(0.5, 0.9),
                'dimensions': ['statistical', 'esoteric']
            },
            {
                'factor_type': 'collective_consciousness',
                'description': "Renforcement mutuel entre conscience collective et traces karmiques",
                'strength': random.uniform(0.4, 0.8),
                'dimensions': ['behavioral', 'esoteric']
            }
        ]
        
        # Choisir quelques facteurs aléatoires
        selected_factors = random.sample(potential_factors, min(num_factors, len(potential_factors)))
        selected_factors.sort(key=lambda f: f.get('strength', 0), reverse=True)
        
        synergies['key_synergy_factors'] = selected_factors
        
        return synergies
    
    def _determine_synergy_advantage(self, team1_name, team2_name, team1_synergies, team2_synergies, match_context=None):
        """Déterminer l'avantage synergique entre deux équipes."""
        # Base de l'analyse
        advantage = {
            'team': None,
            'advantage_score': 0.0,
            'key_factors': [],
            'description': ''
        }
        
        # Calculer l'avantage brut
        team1_overall = team1_synergies.get('overall_synergy', 0.5)
        team2_overall = team2_synergies.get('overall_synergy', 0.5)
        
        raw_advantage = team1_overall - team2_overall
        
        # Ajuster en fonction du contexte
        context_adjustment = 0.0
        if match_context:
            # Avantage à domicile
            if match_context.get('home_team') == team1_name:
                context_adjustment += 0.1
                advantage['key_factors'].append({
                    'factor_type': 'home_advantage',
                    'description': f"Avantage du domicile pour {team1_name}",
                    'impact': 0.1
                })
            elif match_context.get('home_team') == team2_name:
                context_adjustment -= 0.1
                advantage['key_factors'].append({
                    'factor_type': 'home_advantage',
                    'description': f"Avantage du domicile pour {team2_name}",
                    'impact': -0.1
                })
            
            # Importance du match
            match_importance = match_context.get('importance', 'regular')
            if match_importance in ['high', 'critical', 'derby']:
                # Favoriser l'équipe avec une meilleure stabilité de synergie
                team1_stability = team1_synergies.get('synergy_stability', 0.5)
                team2_stability = team2_synergies.get('synergy_stability', 0.5)
                
                stability_diff = team1_stability - team2_stability
                context_adjustment += stability_diff * 0.15
                
                advantage['key_factors'].append({
                    'factor_type': 'stability_in_pressure',
                    'description': f"{'Avantage' if stability_diff > 0 else 'Désavantage'} de stabilité sous pression",
                    'impact': stability_diff * 0.15
                })
        
        # Calculer l'avantage final
        adjusted_advantage = raw_advantage + context_adjustment
        advantage['advantage_score'] = adjusted_advantage
        
        # Déterminer l'équipe avantagée
        if adjusted_advantage > 0.1:
            advantage['team'] = team1_name
            advantage['description'] = f"Avantage synergique pour {team1_name}"
        elif adjusted_advantage < -0.1:
            advantage['team'] = team2_name
            advantage['advantage_score'] = abs(adjusted_advantage)  # Rendre positif
            advantage['description'] = f"Avantage synergique pour {team2_name}"
        else:
            advantage['team'] = 'neutral'
            advantage['advantage_score'] = abs(adjusted_advantage)  # Rendre positif
            advantage['description'] = "Aucun avantage synergique significatif"
        
        # Ajouter des facteurs de synergie clés
        self._add_key_synergy_factors(advantage['key_factors'], team1_synergies, team2_synergies, advantage['team'])
        
        return advantage
    
    def _identify_synergy_patterns(self, team1_synergies, team2_synergies, match_context=None):
        """Identifier les patterns de synergie significatifs."""
        patterns = []
        
        # Pattern 1: Complémentarité dimensionnelle
        team1_dimension_pairs = team1_synergies.get('dimension_pairs', {})
        team2_dimension_pairs = team2_synergies.get('dimension_pairs', {})
        
        # Vérifier si une équipe a une forte synergie dans une dimension où l'autre est faible
        for pair in ['statistical_esoteric', 'statistical_behavioral', 'esoteric_behavioral']:
            team1_value = team1_dimension_pairs.get(pair, 0.5)
            team2_value = team2_dimension_pairs.get(pair, 0.5)
            
            if team1_value > 0.7 and team2_value < 0.4:
                patterns.append({
                    'pattern_type': 'dimensional_advantage',
                    'team': 'team1',
                    'dimension_pair': pair,
                    'description': f"Avantage significatif pour l'équipe 1 dans la synergie {pair}",
                    'significance': team1_value - team2_value
                })
            elif team2_value > 0.7 and team1_value < 0.4:
                patterns.append({
                    'pattern_type': 'dimensional_advantage',
                    'team': 'team2',
                    'dimension_pair': pair,
                    'description': f"Avantage significatif pour l'équipe 2 dans la synergie {pair}",
                    'significance': team2_value - team1_value
                })
        
        # Pattern 2: Stabilité contrastée
        team1_stability = team1_synergies.get('synergy_stability', 0.5)
        team2_stability = team2_synergies.get('synergy_stability', 0.5)
        
        if abs(team1_stability - team2_stability) > 0.3:
            stable_team = 'team1' if team1_stability > team2_stability else 'team2'
            patterns.append({
                'pattern_type': 'stability_contrast',
                'stable_team': stable_team,
                'stability_gap': abs(team1_stability - team2_stability),
                'description': f"Contraste significatif de stabilité synergique en faveur de {'l'équipe 1' if stable_team == 'team1' else 'l'équipe 2'}",
                'significance': abs(team1_stability - team2_stability)
            })
        
        # Pattern 3: Facteurs synergiques communs
        team1_factors = [f.get('factor_type') for f in team1_synergies.get('key_synergy_factors', [])]
        team2_factors = [f.get('factor_type') for f in team2_synergies.get('key_synergy_factors', [])]
        
        common_factors = set(team1_factors).intersection(set(team2_factors))
        if common_factors:
            patterns.append({
                'pattern_type': 'common_synergy_factors',
                'factors': list(common_factors),
                'description': f"Facteurs synergiques communs: {', '.join(common_factors)}",
                'significance': 0.6
            })
        
        # Trier par significance
        patterns.sort(key=lambda p: p.get('significance', 0), reverse=True)
        
        return patterns
    
    def _extract_dimension_prediction(self, dimension_analysis):
        """Extraire la prédiction d'une analyse dimensionnelle."""
        # Base de la prédiction
        prediction = {
            'win_probability': {
                'team1': 0.33,
                'draw': 0.34,
                'team2': 0.33
            },
            'confidence': 0.5
        }
        
        # Extraire les informations disponibles
        if 'prediction' in dimension_analysis:
            pred = dimension_analysis['prediction']
            
            if 'win_probability' in pred:
                wp = pred['win_probability']
                
                if isinstance(wp, dict):
                    # Format {team1: x, draw: y, team2: z}
                    if 'team1' in wp and 'team2' in wp and 'draw' in wp:
                        prediction['win_probability'] = wp
                    # Format {home: x, draw: y, away: z}
                    elif 'home' in wp and 'away' in wp and 'draw' in wp:
                        prediction['win_probability'] = {
                            'team1': wp['home'],
                            'draw': wp['draw'],
                            'team2': wp['away']
                        }
            
            # Si un résultat favori est spécifié
            if 'favored_outcome' in pred:
                outcome = pred['favored_outcome']
                
                if outcome == 'team1_win':
                    prediction['win_probability'] = {
                        'team1': 0.6,
                        'draw': 0.2,
                        'team2': 0.2
                    }
                elif outcome == 'team2_win':
                    prediction['win_probability'] = {
                        'team1': 0.2,
                        'draw': 0.2,
                        'team2': 0.6
                    }
                elif outcome == 'draw':
                    prediction['win_probability'] = {
                        'team1': 0.25,
                        'draw': 0.5,
                        'team2': 0.25
                    }
            
            # Extraire la confiance
            if 'confidence' in pred:
                prediction['confidence'] = pred['confidence']
        
        return prediction
    
    def _calculate_prediction_convergence(self, prediction1, prediction2):
        """Calculer la convergence entre deux prédictions."""
        # Extraire les probabilités
        p1_team1 = prediction1['win_probability']['team1']
        p1_draw = prediction1['win_probability']['draw']
        p1_team2 = prediction1['win_probability']['team2']
        
        p2_team1 = prediction2['win_probability']['team1']
        p2_draw = prediction2['win_probability']['draw']
        p2_team2 = prediction2['win_probability']['team2']
        
        # Calculer la distance euclidienne normalisée
        distance = np.sqrt(
            (p1_team1 - p2_team1)**2 +
            (p1_draw - p2_draw)**2 +
            (p1_team2 - p2_team2)**2
        ) / np.sqrt(2)  # Normaliser pour avoir une valeur entre 0 et 1
        
        # Convertir en score de convergence
        convergence = 1.0 - distance
        
        return convergence
    
    def _determine_combined_prediction(self, prediction1, prediction2):
        """Déterminer une prédiction combinée à partir de deux prédictions."""
        # Calculer la moyenne pondérée
        combined_team1 = (prediction1['win_probability']['team1'] + prediction2['win_probability']['team1']) / 2
        combined_draw = (prediction1['win_probability']['draw'] + prediction2['win_probability']['draw']) / 2
        combined_team2 = (prediction1['win_probability']['team2'] + prediction2['win_probability']['team2']) / 2
        
        # Normaliser
        total = combined_team1 + combined_draw + combined_team2
        combined_team1 /= total
        combined_draw /= total
        combined_team2 /= total
        
        # Déterminer le résultat prédit
        if combined_team1 > combined_team2 and combined_team1 > combined_draw:
            prediction = 'team1_win'
        elif combined_team2 > combined_team1 and combined_team2 > combined_draw:
            prediction = 'team2_win'
        else:
            prediction = 'draw'
        
        return prediction
    
    def _add_dimension_key_factors(self, key_factors, dimension_analysis, dimension_name):
        """Ajouter des facteurs clés spécifiques à une dimension."""
        if dimension_name == 'statistical':
            # Ajouter un facteur basé sur la forme
            team1_form = dimension_analysis.get('team1_analysis', {}).get('form', 0)
            team2_form = dimension_analysis.get('team2_analysis', {}).get('form', 0)
            
            if abs(team1_form - team2_form) > 0.2:
                better_team = 'team1' if team1_form > team2_form else 'team2'
                key_factors.append({
                    'type': 'statistical_form',
                    'description': f"Meilleure forme statistique pour {'l\'équipe 1' if better_team == 'team1' else 'l\'équipe 2'}",
                    'strength': abs(team1_form - team2_form)
                })
        
        elif dimension_name == 'esoteric':
            # Ajouter un facteur basé sur l'alignement karmique
            karmic_balance = dimension_analysis.get('karmic_patterns', {}).get('karmic_balance', 'balanced')
            
            if karmic_balance in ['team1_debt', 'team2_debt']:
                favored_team = 'team2' if karmic_balance == 'team1_debt' else 'team1'
                key_factors.append({
                    'type': 'esoteric_karma',
                    'description': f"Balance karmique favorable à {'l\'équipe 1' if favored_team == 'team1' else 'l\'équipe 2'}",
                    'strength': 0.7
                })
        
        elif dimension_name == 'behavioral':
            # Ajouter un facteur basé sur le momentum
            momentum = dimension_analysis.get('momentum_analysis', {}).get('current_momentum', 'neutral')
            momentum_strength = dimension_analysis.get('momentum_analysis', {}).get('momentum_strength', 0.5)
            
            if momentum in ['team1', 'team2'] and momentum_strength > 0.6:
                key_factors.append({
                    'type': 'behavioral_momentum',
                    'description': f"Momentum comportemental fort pour {'l\'équipe 1' if momentum == 'team1' else 'l\'équipe 2'}",
                    'strength': momentum_strength
                })
    
    def _calculate_dimension_consistency(self, statistical_analysis, esoteric_analysis, behavioral_analysis):
        """Calculer la cohérence entre les différentes dimensions."""
        # Extraire les prédictions
        stat_pred = self._get_predicted_result(statistical_analysis.get('prediction', {}).get('win_probability', {}))
        eso_pred = self._get_predicted_result(esoteric_analysis.get('prediction', {}).get('win_probability', {}))
        behav_pred = self._get_predicted_result(behavioral_analysis.get('prediction', {}).get('win_probability', {}))
        
        # Compter les prédictions uniques
        predictions = [stat_pred, eso_pred, behav_pred]
        unique_predictions = set(predictions)
        
        # Calculer la cohérence
        if len(unique_predictions) == 1:
            # Toutes les dimensions prédisent le même résultat
            return 1.0
        elif len(unique_predictions) == 2:
            # Deux dimensions prédisent le même résultat
            return 0.5
        else:
            # Toutes les dimensions prédisent des résultats différents
            return 0.0
    
    def _calculate_data_completeness(self, statistical_analysis, esoteric_analysis, behavioral_analysis):
        """Calculer la complétude des données."""
        # Vérifier la présence des analyses clés
        completeness = 0.0
        
        # Dimension statistique
        stat_completeness = 0.0
        if 'team1_analysis' in statistical_analysis and 'team2_analysis' in statistical_analysis:
            stat_completeness += 0.5
        if 'head_to_head' in statistical_analysis:
            stat_completeness += 0.2
        if 'prediction' in statistical_analysis:
            stat_completeness += 0.3
        
        # Dimension ésotérique
        eso_completeness = 0.0
        if 'numerological_analysis' in esoteric_analysis:
            eso_completeness += 0.2
        if 'astrological_influences' in esoteric_analysis:
            eso_completeness += 0.2
        if 'karmic_patterns' in esoteric_analysis:
            eso_completeness += 0.3
        if 'prediction' in esoteric_analysis:
            eso_completeness += 0.3
        
        # Dimension comportementale
        behav_completeness = 0.0
        if 'team_psychology' in behavioral_analysis:
            behav_completeness += 0.3
        if 'pressure_factors' in behavioral_analysis:
            behav_completeness += 0.3
        if 'momentum_analysis' in behavioral_analysis:
            behav_completeness += 0.2
        if 'prediction' in behavioral_analysis:
            behav_completeness += 0.2
        
        # Calculer la complétude globale
        completeness = (
            stat_completeness * self.analysis_params['statistical_weight'] +
            eso_completeness * self.analysis_params['esoteric_weight'] +
            behav_completeness * self.analysis_params['behavioral_weight']
        )
        
        return completeness
    
    def _get_predicted_result(self, win_probability):
        """Obtenir le résultat prédit à partir des probabilités."""
        if not win_probability:
            return 'unknown'
        
        team1_prob = win_probability.get('team1', 0)
        team2_prob = win_probability.get('team2', 0)
        draw_prob = win_probability.get('draw', 0)
        
        if team1_prob > team2_prob and team1_prob > draw_prob:
            return 'team1_win'
        elif team2_prob > team1_prob and team2_prob > draw_prob:
            return 'team2_win'
        else:
            return 'draw'
    
    def _detect_cycle(self, values, cycle_size):
        """Détecter un cycle dans une série de valeurs."""
        # Méthode simplifiée pour détecter des cycles
        if len(values) < cycle_size * 2:
            return False
        
        # Comparer différentes sections de la séquence
        similarity_sum = 0
        comparisons = 0
        
        for i in range(len(values) - cycle_size):
            if i + cycle_size * 2 <= len(values):
                segment1 = values[i:i+cycle_size]
                segment2 = values[i+cycle_size:i+cycle_size*2]
                
                # Calculer la similarité (corrélation)
                correlation = np.corrcoef(segment1, segment2)[0, 1]
                
                if not np.isnan(correlation):
                    similarity_sum += correlation
                    comparisons += 1
        
        if comparisons > 0:
            avg_similarity = similarity_sum / comparisons
            return avg_similarity > 0.7
        
        return False
    
    def _add_key_synergy_factors(self, key_factors, team1_synergies, team2_synergies, advantaged_team):
        """Ajouter des facteurs de synergie clés à l'analyse d'avantage."""
        if advantaged_team == 'team1':
            # Ajouter les facteurs clés de l'équipe 1
            factors = team1_synergies.get('key_synergy_factors', [])
            if factors:
                top_factor = max(factors, key=lambda f: f.get('strength', 0))
                key_factors.append({
                    'factor_type': 'synergy_strength',
                    'description': top_factor.get('description', 'Forte synergie dimensionnelle'),
                    'impact': top_factor.get('strength', 0.7) * 0.3
                })
        
        elif advantaged_team == 'team2':
            # Ajouter les facteurs clés de l'équipe 2
            factors = team2_synergies.get('key_synergy_factors', [])
            if factors:
                top_factor = max(factors, key=lambda f: f.get('strength', 0))
                key_factors.append({
                    'factor_type': 'synergy_strength',
                    'description': top_factor.get('description', 'Forte synergie dimensionnelle'),
                    'impact': top_factor.get('strength', 0.7) * 0.3
                })
        
        # Si une dimension spécifique est particulièrement forte
        if advantaged_team in ['team1', 'team2']:
            synergies = team1_synergies if advantaged_team == 'team1' else team2_synergies
            dimension_pairs = synergies.get('dimension_pairs', {})
            
            if dimension_pairs:
                top_pair = max(dimension_pairs.items(), key=lambda x: x[1])
                if top_pair[1] > 0.8:
                    key_factors.append({
                        'factor_type': 'dimension_synergy',
                        'description': f"Synergie exceptionnelle entre dimensions {top_pair[0].replace('_', '-')}",
                        'impact': (top_pair[1] - 0.5) * 0.4
                    })