"""
CollapseDetector - Module d'analyse des effondrements probables d'équipes favorites.
Détecte les équipes à risque d'effondrement psychologique ou tactique à partir de modèles statistiques et psychologiques.
"""

import numpy as np
import random
from datetime import datetime, timedelta
import json
import os
from collections import deque

class CollapseDetector:
    """
    CollapseDetector - Analyse les risques d'effondrement des équipes favorites.
    Évalue les facteurs de risque d'une équipe à s'effondrer malgré un statut de favori.
    """
    
    def __init__(self):
        """Initialise le module CollapseDetector."""
        # Facteurs de risque d'effondrement
        self.collapse_factors = {
            'psychological': {
                'pressure_threshold': 0.7,      # Seuil de pression mentale
                'ego_factor': 0.6,              # Impact de l'ego/arrogance
                'complacency_risk': 0.5,        # Risque de complaisance
                'fan_expectation_weight': 0.45, # Poids des attentes des supporters
                'media_pressure_factor': 0.4    # Facteur de pression médiatique
            },
            'tactical': {
                'substitution_impact': 0.55,    # Impact des changements tactiques
                'formation_rigidity': 0.5,      # Rigidité tactique
                'plan_b_availability': 0.65,    # Disponibilité d'un plan B
                'adaptability_factor': 0.6      # Facteur d'adaptabilité tactique
            },
            'physical': {
                'fatigue_threshold': 0.7,       # Seuil de fatigue
                'injury_impact': 0.8,           # Impact des blessures
                'fixture_congestion': 0.6,      # Congestion du calendrier
                'travel_burden': 0.4,           # Charge liée aux déplacements
                'weather_adaptation': 0.3       # Adaptation aux conditions météo
            },
            'historical': {
                'bottling_history': 0.75,       # Historique d'effondrements
                'revenge_factor': 0.5,          # Facteur de revanche
                'psychological_scars': 0.65,    # Cicatrices psychologiques
                'underdog_success': 0.55        # Succès précédents contre cette équipe
            }
        }
        
        # Modèles d'effondrement typiques
        self.collapse_patterns = {
            'gradual_fade': {
                'description': 'Effondrement progressif sur plusieurs matchs',
                'detection_window': 5,          # Fenêtre de matchs pour détection
                'confidence_threshold': 0.7,    # Seuil de confiance
                'key_indicators': ['declining_form', 'increasing_goals_conceded', 'decreasing_xG']
            },
            'sudden_collapse': {
                'description': 'Effondrement brutal sur un match',
                'detection_window': 1,
                'confidence_threshold': 0.8,
                'key_indicators': ['red_card', 'early_conceded_goal', 'key_injury', 'tactical_mismatch']
            },
            'psychological_meltdown': {
                'description': 'Effondrement psychologique après un événement traumatique',
                'detection_window': 3,
                'confidence_threshold': 0.75,
                'key_indicators': ['critical_mistake', 'missed_opportunity', 'public_criticism', 'internal_conflict']
            },
            'strategic_exposure': {
                'description': 'Vulnérabilités stratégiques exposées par un adversaire',
                'detection_window': 2,
                'confidence_threshold': 0.65,
                'key_indicators': ['tactical_vulnerability', 'repeated_mistake', 'failed_adjustment', 'overconfidence']
            }
        }
        
        # Seuils de détection d'effondrement
        self.detection_thresholds = {
            'high_risk': 0.7,      # Risque élevé d'effondrement
            'medium_risk': 0.5,    # Risque moyen d'effondrement
            'low_risk': 0.3        # Risque faible d'effondrement
        }
        
        # Historique des analyses d'effondrement
        self.collapse_analysis_history = []
        
        # Buffer pour le suivi de la forme récente
        self.form_tracker = {}  # team_id -> [résultats récents]
        
        # État actuel de l'analyse
        self.current_state = {
            'teams_at_risk': [],
            'ongoing_collapses': [],
            'last_update': None
        }
    
    def analyze_collapse_risk(self, team_data, match_data=None, form_data=None):
        """
        Analyser le risque d'effondrement d'une équipe.
        
        Args:
            team_data (dict): Données de l'équipe à analyser
            match_data (dict, optional): Données du match à venir
            form_data (dict, optional): Données de forme récente
            
        Returns:
            dict: Analyse du risque d'effondrement avec scores
        """
        # Extraire les informations pertinentes
        team_id = team_data.get('id', '')
        team_name = team_data.get('name', '')
        
        # Initialiser les scores de risque par catégorie
        risk_scores = {
            'psychological': 0.0,
            'tactical': 0.0,
            'physical': 0.0,
            'historical': 0.0
        }
        
        # 1. Évaluer les facteurs psychologiques
        psychological_risk = self._evaluate_psychological_factors(team_data, match_data)
        risk_scores['psychological'] = psychological_risk
        
        # 2. Évaluer les facteurs tactiques
        tactical_risk = self._evaluate_tactical_factors(team_data, match_data)
        risk_scores['tactical'] = tactical_risk
        
        # 3. Évaluer les facteurs physiques
        physical_risk = self._evaluate_physical_factors(team_data, match_data)
        risk_scores['physical'] = physical_risk
        
        # 4. Évaluer les facteurs historiques
        historical_risk = self._evaluate_historical_factors(team_data, match_data)
        risk_scores['historical'] = historical_risk
        
        # 5. Analyser la forme récente si disponible
        form_analysis = None
        if form_data:
            form_analysis = self._analyze_recent_form(team_id, form_data)
            
            # Mettre à jour le tracker de forme
            if team_id not in self.form_tracker:
                self.form_tracker[team_id] = deque(maxlen=10)  # Suivre les 10 derniers résultats
            
            # Ajouter le résultat le plus récent
            latest_result = form_data.get('latest_result', None)
            if latest_result:
                self.form_tracker[team_id].append(latest_result)
        
        # 6. Détecter les patterns d'effondrement
        detected_patterns = self._detect_collapse_patterns(team_data, risk_scores, form_analysis)
        
        # 7. Calculer le score de risque global
        overall_risk = (
            risk_scores['psychological'] * 0.3 +
            risk_scores['tactical'] * 0.25 +
            risk_scores['physical'] * 0.2 +
            risk_scores['historical'] * 0.25
        )
        
        # Déterminer le niveau de risque
        risk_level = 'low'
        if overall_risk >= self.detection_thresholds['high_risk']:
            risk_level = 'high'
        elif overall_risk >= self.detection_thresholds['medium_risk']:
            risk_level = 'medium'
        
        # 8. Générer les points faibles spécifiques
        weaknesses = self._identify_specific_weaknesses(risk_scores, form_analysis, team_data)
        
        # 9. Préparer les recommandations pour éviter l'effondrement
        recommendations = self._generate_recommendations(risk_scores, detected_patterns, weaknesses)
        
        # Mettre à jour l'état actuel
        is_at_risk = overall_risk >= self.detection_thresholds['medium_risk']
        if is_at_risk:
            self.current_state['teams_at_risk'].append({
                'team_id': team_id,
                'team_name': team_name,
                'risk_score': overall_risk,
                'risk_level': risk_level,
                'timestamp': datetime.now().isoformat()
            })
        
        # Nettoyer la liste des équipes à risque (garder uniquement les entrées récentes)
        now = datetime.now()
        self.current_state['teams_at_risk'] = [
            team for team in self.current_state['teams_at_risk']
            if datetime.fromisoformat(team['timestamp']) > now - timedelta(days=7)
        ]
        
        # Enregistrer l'analyse dans l'historique
        analysis_record = {
            'team_id': team_id,
            'team_name': team_name,
            'timestamp': datetime.now().isoformat(),
            'risk_scores': risk_scores,
            'overall_risk': overall_risk,
            'risk_level': risk_level,
            'detected_patterns': detected_patterns,
            'match_id': match_data.get('id', '') if match_data else ''
        }
        
        self.collapse_analysis_history.append(analysis_record)
        
        # Limiter la taille de l'historique
        if len(self.collapse_analysis_history) > 100:
            self.collapse_analysis_history = self.collapse_analysis_history[-100:]
        
        # Préparer le résultat
        result = {
            'team_name': team_name,
            'overall_collapse_risk': overall_risk,
            'risk_level': risk_level,
            'risk_breakdown': risk_scores,
            'detected_patterns': detected_patterns,
            'specific_weaknesses': weaknesses,
            'recommendations': recommendations,
            'form_analysis': form_analysis,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def predict_collapse_potential(self, season_data, team_id):
        """
        Prédire le potentiel d'effondrement d'une équipe sur une saison entière.
        
        Args:
            season_data (dict): Données de la saison actuelle
            team_id (str): Identifiant de l'équipe à analyser
            
        Returns:
            dict: Prédiction du potentiel d'effondrement
        """
        # Extraire les données de l'équipe
        team_info = None
        for team in season_data.get('teams', []):
            if team.get('id', '') == team_id:
                team_info = team
                break
        
        if not team_info:
            return {
                'status': 'error',
                'message': 'Équipe non trouvée dans les données de la saison'
            }
        
        # Analyser les périodes critiques de la saison
        season_timeline = season_data.get('timeline', {})
        critical_periods = self._identify_critical_periods(season_timeline, team_info)
        
        # Évaluer les facteurs de risque structurels
        structural_risks = self._evaluate_structural_risks(team_info)
        
        # Analyser l'historique d'effondrements
        collapse_history = self._analyze_historical_collapses(team_info)
        
        # Calculer la résilience de l'équipe
        resilience_score = self._calculate_team_resilience(team_info)
        
        # Calculer le potentiel d'effondrement
        collapse_potential = (
            structural_risks['overall'] * 0.4 +
            (1 - resilience_score) * 0.3 +
            collapse_history['collapse_frequency'] * 0.3
        )
        
        # Classification du potentiel
        potential_category = 'average'
        if collapse_potential >= 0.7:
            potential_category = 'high'
        elif collapse_potential >= 0.5:
            potential_category = 'above_average'
        elif collapse_potential <= 0.3:
            potential_category = 'low'
        
        # Générer la prédiction
        most_vulnerable_period = max(critical_periods, key=lambda x: x['risk_score']) if critical_periods else None
        
        prediction = {
            'team_name': team_info.get('name', ''),
            'collapse_potential': collapse_potential,
            'potential_category': potential_category,
            'structural_risks': structural_risks,
            'resilience_score': resilience_score,
            'historical_collapse_rate': collapse_history['collapse_frequency'],
            'critical_periods': critical_periods,
            'most_vulnerable_period': most_vulnerable_period,
            'key_risk_factors': structural_risks['key_factors'],
            'conditional_factors': self._identify_conditional_factors(team_info)
        }
        
        return prediction
    
    def detect_ongoing_collapse(self, team_data, recent_results, competition_data=None):
        """
        Détecter si une équipe est actuellement en train de s'effondrer.
        
        Args:
            team_data (dict): Données de l'équipe
            recent_results (list): Résultats récents de l'équipe
            competition_data (dict, optional): Données de la compétition
            
        Returns:
            dict: Analyse d'un effondrement en cours
        """
        # Minimum de résultats pour une analyse valide
        if not recent_results or len(recent_results) < 3:
            return {
                'status': 'insufficient_data',
                'message': 'Pas assez de résultats récents pour analyser'
            }
        
        # Extraire les informations pertinentes
        team_name = team_data.get('name', '')
        expected_performance = team_data.get('expected_performance', 0.6)  # Performance attendue (0-1)
        
        # Calculer les indicateurs d'effondrement
        indicators = self._calculate_collapse_indicators(recent_results, expected_performance)
        
        # Vérifier si les critères d'effondrement sont remplis
        is_collapsing = False
        confidence = 0.0
        collapse_pattern = None
        
        # Critère 1: Baisse significative de la performance
        if indicators['performance_drop'] > 0.3:
            is_collapsing = True
            confidence += 0.4
            collapse_pattern = 'performance_drop'
        
        # Critère 2: Séquence de défaites
        if indicators['consecutive_losses'] >= 3:
            is_collapsing = True
            confidence += 0.3 + (min(indicators['consecutive_losses'] - 3, 2) * 0.1)  # +0.1 par défaite supplémentaire, max +0.2
            collapse_pattern = collapse_pattern or 'losing_streak'
        
        # Critère 3: Détérioration défensive
        if indicators['defensive_collapse']:
            is_collapsing = True
            confidence += 0.25
            collapse_pattern = collapse_pattern or 'defensive_collapse'
        
        # Critère 4: Chute dans le classement
        if indicators['ranking_drop'] >= 3:
            confidence += 0.2
            collapse_pattern = collapse_pattern or 'ranking_collapse'
        
        # Limiter la confiance à 1.0
        confidence = min(1.0, confidence)
        
        # Identifier le type d'effondrement
        collapse_type = self._identify_collapse_type(indicators, recent_results)
        
        # Enregistrer l'effondrement s'il est détecté avec une confiance suffisante
        if is_collapsing and confidence > 0.6:
            # Vérifier si cet effondrement est déjà suivi
            team_id = team_data.get('id', '')
            already_tracked = False
            
            for collapse in self.current_state['ongoing_collapses']:
                if collapse['team_id'] == team_id:
                    # Mettre à jour l'effondrement existant
                    collapse['confidence'] = confidence
                    collapse['intensity'] = indicators['performance_drop']
                    collapse['last_update'] = datetime.now().isoformat()
                    already_tracked = True
                    break
            
            if not already_tracked:
                # Ajouter un nouvel effondrement
                self.current_state['ongoing_collapses'].append({
                    'team_id': team_id,
                    'team_name': team_name,
                    'start_date': recent_results[0].get('date', datetime.now().isoformat()),
                    'confidence': confidence,
                    'pattern': collapse_pattern,
                    'type': collapse_type,
                    'intensity': indicators['performance_drop'],
                    'last_update': datetime.now().isoformat()
                })
        
        # Nettoyer la liste des effondrements en cours (supprimer ceux qui sont résolus)
        now = datetime.now()
        self.current_state['ongoing_collapses'] = [
            collapse for collapse in self.current_state['ongoing_collapses']
            if datetime.fromisoformat(collapse['last_update']) > now - timedelta(days=14)
        ]
        
        # Prédire la durée et la sévérité de l'effondrement
        recovery_prediction = None
        if is_collapsing and confidence > 0.5:
            recovery_prediction = self._predict_collapse_recovery(team_data, indicators, collapse_type)
        
        # Préparer le résultat
        result = {
            'team_name': team_name,
            'is_collapsing': is_collapsing,
            'confidence': confidence,
            'collapse_pattern': collapse_pattern,
            'collapse_type': collapse_type,
            'indicators': indicators,
            'recovery_prediction': recovery_prediction,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def _evaluate_psychological_factors(self, team_data, match_data=None):
        """Évaluer les facteurs de risque psychologiques d'effondrement."""
        # Extraction des données pertinentes
        pressure_level = team_data.get('pressure_level', 0.5)
        ego_level = team_data.get('ego_level', 0.5)
        experience_rating = team_data.get('experience_rating', 0.5)
        fan_expectation = team_data.get('fan_expectation', 0.5)
        media_scrutiny = team_data.get('media_scrutiny', 0.5)
        
        # Ajuster selon le match à venir si disponible
        if match_data:
            match_importance = match_data.get('importance', 0.5)
            is_derby = match_data.get('is_derby', False)
            
            # Augmenter la pression pour les matchs importants
            pressure_level = min(1.0, pressure_level + (match_importance * 0.2))
            
            # Augmenter la pression médiatique pour les derbies
            if is_derby:
                media_scrutiny = min(1.0, media_scrutiny + 0.15)
                fan_expectation = min(1.0, fan_expectation + 0.1)
        
        # Calcul des facteurs de risque
        pressure_risk = pressure_level * self.collapse_factors['psychological']['pressure_threshold']
        ego_risk = ego_level * self.collapse_factors['psychological']['ego_factor']
        
        # Facteur d'expérience (inverse - plus d'expérience = moins de risque)
        experience_factor = (1 - experience_rating) * 0.5
        
        # Attentes des supporters et pression médiatique
        expectation_risk = fan_expectation * self.collapse_factors['psychological']['fan_expectation_weight']
        media_risk = media_scrutiny * self.collapse_factors['psychological']['media_pressure_factor']
        
        # Risque psychologique global
        psychological_risk = (
            pressure_risk * 0.3 +
            ego_risk * 0.2 +
            experience_factor * 0.2 +
            expectation_risk * 0.15 +
            media_risk * 0.15
        )
        
        return min(1.0, psychological_risk)
    
    def _evaluate_tactical_factors(self, team_data, match_data=None):
        """Évaluer les facteurs de risque tactiques d'effondrement."""
        # Extraction des données
        formation_rigidity = team_data.get('formation_rigidity', 0.5)
        tactical_adaptability = team_data.get('tactical_adaptability', 0.5)
        substitution_impact = team_data.get('substitution_impact', 0.5)
        has_plan_b = team_data.get('has_plan_b', True)
        
        # Ajuster selon le match à venir si disponible
        if match_data:
            opponent_style = match_data.get('opponent_style', 'balanced')
            team_style = team_data.get('playing_style', 'balanced')
            
            # Évaluer la compatibilité des styles
            style_compatibility = self._evaluate_style_compatibility(team_style, opponent_style)
            
            # Augmenter la rigidité si le style est incompatible
            if style_compatibility < 0.4:
                formation_rigidity = min(1.0, formation_rigidity + 0.15)
        
        # Calcul des facteurs de risque
        rigidity_risk = formation_rigidity * self.collapse_factors['tactical']['formation_rigidity']
        adaptability_risk = (1 - tactical_adaptability) * self.collapse_factors['tactical']['adaptability_factor']
        substitution_risk = (1 - substitution_impact) * self.collapse_factors['tactical']['substitution_impact']
        plan_b_risk = 0.0 if has_plan_b else self.collapse_factors['tactical']['plan_b_availability']
        
        # Risque tactique global
        tactical_risk = (
            rigidity_risk * 0.3 +
            adaptability_risk * 0.3 +
            substitution_risk * 0.2 +
            plan_b_risk * 0.2
        )
        
        return min(1.0, tactical_risk)
    
    def _evaluate_physical_factors(self, team_data, match_data=None):
        """Évaluer les facteurs de risque physiques d'effondrement."""
        # Extraction des données
        fatigue_level = team_data.get('fatigue_level', 0.5)
        injury_concerns = team_data.get('injury_concerns', 0.3)
        fixture_congestion = team_data.get('fixture_congestion', 0.3)
        travel_distance = team_data.get('travel_distance', 0)  # En km
        
        # Normaliser la distance de voyage
        normalized_travel = min(1.0, travel_distance / 1000)  # 1000km comme référence max
        
        # Ajuster selon le match à venir si disponible
        if match_data:
            is_away = match_data.get('is_away', False)
            weather_condition = match_data.get('weather_condition', 'normal')
            days_since_last_match = match_data.get('days_since_last_match', 4)
            
            # Augmenter la fatigue pour les matchs à l'extérieur
            if is_away:
                fatigue_level = min(1.0, fatigue_level + 0.1)
            
            # Ajuster selon les conditions météo
            if weather_condition in ['extreme_heat', 'extreme_cold', 'heavy_rain', 'snow']:
                fatigue_level = min(1.0, fatigue_level + 0.15)
            
            # Facteur de récupération
            if days_since_last_match < 3:
                fatigue_level = min(1.0, fatigue_level + (3 - days_since_last_match) * 0.05)
                fixture_congestion = min(1.0, fixture_congestion + 0.2)
        
        # Calcul des facteurs de risque
        fatigue_risk = fatigue_level * self.collapse_factors['physical']['fatigue_threshold']
        injury_risk = injury_concerns * self.collapse_factors['physical']['injury_impact']
        congestion_risk = fixture_congestion * self.collapse_factors['physical']['fixture_congestion']
        travel_risk = normalized_travel * self.collapse_factors['physical']['travel_burden']
        
        # Risque physique global
        physical_risk = (
            fatigue_risk * 0.35 +
            injury_risk * 0.3 +
            congestion_risk * 0.25 +
            travel_risk * 0.1
        )
        
        return min(1.0, physical_risk)
    
    def _evaluate_historical_factors(self, team_data, match_data=None):
        """Évaluer les facteurs de risque historiques d'effondrement."""
        # Extraction des données
        previous_collapses = team_data.get('previous_collapses', 0)  # Nombre d'effondrements précédents
        similar_situation_success = team_data.get('similar_situation_success', 0.5)
        psychological_fragility = team_data.get('psychological_fragility', 0.3)
        
        # Normaliser le nombre d'effondrements précédents
        normalized_collapses = min(1.0, previous_collapses / 5)  # 5 collapses comme référence max
        
        # Ajuster selon le match à venir si disponible
        if match_data:
            opponent_id = match_data.get('opponent_id', '')
            is_revenge_match = match_data.get('is_revenge_match', False)
            previous_trauma = match_data.get('previous_trauma', False)
            
            # Chercher les effets psychologiques spécifiques contre cet adversaire
            historical_record = team_data.get('opponent_record', {}).get(opponent_id, {})
            underdog_victories = historical_record.get('underdog_victories', 0)
            
            # Normaliser les victoires surprises
            normalized_underdog_wins = min(1.0, underdog_victories / 3)
            
            # Facteurs de revanche et trauma psychologique
            if is_revenge_match:
                psychological_fragility = min(1.0, psychological_fragility + 0.2)
            
            if previous_trauma:
                psychological_fragility = min(1.0, psychological_fragility + 0.25)
        else:
            normalized_underdog_wins = 0.0
        
        # Calcul des facteurs de risque
        bottling_risk = normalized_collapses * self.collapse_factors['historical']['bottling_history']
        success_risk = (1 - similar_situation_success) * 0.5  # Facteur inverse
        psychological_risk = psychological_fragility * self.collapse_factors['historical']['psychological_scars']
        underdog_risk = normalized_underdog_wins * self.collapse_factors['historical']['underdog_success']
        
        # Risque historique global
        historical_risk = (
            bottling_risk * 0.4 +
            success_risk * 0.2 +
            psychological_risk * 0.3 +
            underdog_risk * 0.1
        )
        
        return min(1.0, historical_risk)
    
    def _analyze_recent_form(self, team_id, form_data):
        """Analyser la forme récente d'une équipe pour détecter des signes d'effondrement."""
        # Extraction des données
        results = form_data.get('results', [])
        expected_results = form_data.get('expected_results', [])
        
        if not results:
            return None
        
        # Calculer les tendances
        win_percentage = form_data.get('win_percentage', 0.0)
        expected_win_percentage = form_data.get('expected_win_percentage', 0.0)
        form_trend = form_data.get('form_trend', 'stable')
        
        # Performance par rapport aux attentes
        performance_vs_expectation = win_percentage - expected_win_percentage
        
        # Analyser la tendance défensive
        defensive_trend = form_data.get('defensive_trend', 'stable')
        goals_conceded_trend = form_data.get('goals_conceded_trend', 'stable')
        
        # Résultats récents (derniers matchs)
        recent_results_trend = self._calculate_results_trend(results[:5])
        
        # Obtenir l'historique de forme pour ce team_id
        previous_form = None
        if team_id in self.form_tracker:
            previous_form = list(self.form_tracker[team_id])
        
        # Analyser l'évolution par rapport à la forme précédente
        form_evolution = None
        if previous_form:
            form_evolution = self._compare_form_periods(previous_form, results[:len(previous_form)])
        
        return {
            'win_percentage': win_percentage,
            'performance_vs_expectation': performance_vs_expectation,
            'form_trend': form_trend,
            'defensive_trend': defensive_trend,
            'goals_conceded_trend': goals_conceded_trend,
            'recent_results_trend': recent_results_trend,
            'form_evolution': form_evolution,
            'collapse_warning': performance_vs_expectation < -0.2,
            'expected_correction': performance_vs_expectation < -0.3,
            'recovery_signs': recent_results_trend == 'improving' and defensive_trend == 'improving'
        }
    
    def _detect_collapse_patterns(self, team_data, risk_scores, form_analysis=None):
        """Détecter des patterns d'effondrement spécifiques."""
        detected_patterns = []
        
        # Pattern 1: Fatigue psychologique
        if risk_scores['psychological'] > 0.7 and risk_scores['physical'] > 0.6:
            detected_patterns.append({
                'pattern': 'psychological_fatigue',
                'confidence': (risk_scores['psychological'] * 0.7 + risk_scores['physical'] * 0.3),
                'description': 'Signes de fatigue psychologique et physique combinées',
                'risk_level': 'high'
            })
        
        # Pattern 2: Rigidité tactique
        if risk_scores['tactical'] > 0.75:
            detected_patterns.append({
                'pattern': 'tactical_rigidity',
                'confidence': risk_scores['tactical'],
                'description': 'Manque d\'adaptabilité tactique face à l\'adversité',
                'risk_level': 'high' if risk_scores['tactical'] > 0.8 else 'medium'
            })
        
        # Pattern 3: Cicatrices historiques
        if risk_scores['historical'] > 0.7 and risk_scores['psychological'] > 0.6:
            detected_patterns.append({
                'pattern': 'historical_scars',
                'confidence': (risk_scores['historical'] * 0.6 + risk_scores['psychological'] * 0.4),
                'description': 'Traumatismes historiques affectant la performance actuelle',
                'risk_level': 'high'
            })
        
        # Pattern 4: Arrogance et complaisance
        if risk_scores['psychological'] > 0.65 and team_data.get('ego_level', 0) > 0.7:
            detected_patterns.append({
                'pattern': 'complacency',
                'confidence': risk_scores['psychological'] * 0.8,
                'description': 'Excès de confiance et sous-estimation de l\'adversaire',
                'risk_level': 'medium'
            })
        
        # Pattern 5: Pression externe
        media_pressure = team_data.get('media_scrutiny', 0.5)
        fan_expectation = team_data.get('fan_expectation', 0.5)
        if media_pressure > 0.7 and fan_expectation > 0.7 and risk_scores['psychological'] > 0.6:
            detected_patterns.append({
                'pattern': 'external_pressure',
                'confidence': (media_pressure * 0.3 + fan_expectation * 0.3 + risk_scores['psychological'] * 0.4),
                'description': 'Forte pression médiatique et attentes des supporters',
                'risk_level': 'medium'
            })
        
        # Intégrer l'analyse de forme si disponible
        if form_analysis:
            if form_analysis.get('performance_vs_expectation', 0) < -0.25 and form_analysis.get('form_trend', '') == 'declining':
                detected_patterns.append({
                    'pattern': 'form_collapse',
                    'confidence': min(1.0, abs(form_analysis['performance_vs_expectation']) * 2),
                    'description': 'Baisse marquée de forme par rapport aux attentes',
                    'risk_level': 'high' if form_analysis['performance_vs_expectation'] < -0.35 else 'medium'
                })
            
            if form_analysis.get('defensive_trend', '') == 'declining' and form_analysis.get('goals_conceded_trend', '') == 'increasing':
                detected_patterns.append({
                    'pattern': 'defensive_vulnerability',
                    'confidence': 0.7,
                    'description': 'Fragilité défensive croissante, susceptible d\'impacter le moral',
                    'risk_level': 'medium'
                })
        
        return detected_patterns
    
    def _identify_specific_weaknesses(self, risk_scores, form_analysis, team_data):
        """Identifier les faiblesses spécifiques susceptibles de provoquer un effondrement."""
        weaknesses = []
        
        # Identifier les catégories de risque élevé
        high_risk_categories = []
        for category, score in risk_scores.items():
            if score > 0.7:
                high_risk_categories.append(category)
        
        # Faiblesses psychologiques
        if 'psychological' in high_risk_categories:
            if team_data.get('ego_level', 0) > 0.7:
                weaknesses.append({
                    'type': 'psychological',
                    'weakness': 'ego_management',
                    'description': 'Excès de confiance des joueurs clés',
                    'severity': 'high'
                })
            
            if team_data.get('pressure_level', 0) > 0.75:
                weaknesses.append({
                    'type': 'psychological',
                    'weakness': 'pressure_handling',
                    'description': 'Gestion déficiente de la pression dans les moments clés',
                    'severity': 'high'
                })
        
        # Faiblesses tactiques
        if 'tactical' in high_risk_categories:
            if team_data.get('formation_rigidity', 0) > 0.7:
                weaknesses.append({
                    'type': 'tactical',
                    'weakness': 'tactical_flexibility',
                    'description': 'Manque de flexibilité dans l\'approche tactique',
                    'severity': 'high'
                })
            
            if not team_data.get('has_plan_b', True):
                weaknesses.append({
                    'type': 'tactical',
                    'weakness': 'plan_b',
                    'description': 'Absence de plan alternatif en cas de difficulté',
                    'severity': 'high'
                })
        
        # Faiblesses physiques
        if 'physical' in high_risk_categories:
            if team_data.get('fatigue_level', 0) > 0.7:
                weaknesses.append({
                    'type': 'physical',
                    'weakness': 'fatigue_management',
                    'description': 'Niveaux de fatigue élevés affectant la performance',
                    'severity': 'high'
                })
            
            if team_data.get('injury_concerns', 0) > 0.6:
                weaknesses.append({
                    'type': 'physical',
                    'weakness': 'injury_problems',
                    'description': 'Problèmes de blessures impactant la stabilité de l\'équipe',
                    'severity': 'medium'
                })
        
        # Faiblesses historiques
        if 'historical' in high_risk_categories:
            if team_data.get('previous_collapses', 0) > 2:
                weaknesses.append({
                    'type': 'historical',
                    'weakness': 'psychological_scars',
                    'description': 'Historique d\'effondrements affectant la confiance actuelle',
                    'severity': 'high'
                })
        
        # Intégrer l'analyse de forme si disponible
        if form_analysis:
            if form_analysis.get('defensive_trend', '') == 'declining':
                weaknesses.append({
                    'type': 'form',
                    'weakness': 'defensive_frailty',
                    'description': 'Tendance défensive en déclin',
                    'severity': 'medium'
                })
            
            if form_analysis.get('performance_vs_expectation', 0) < -0.3:
                weaknesses.append({
                    'type': 'form',
                    'weakness': 'performance_gap',
                    'description': 'Performance nettement en-dessous des attentes',
                    'severity': 'high'
                })
        
        return weaknesses
    
    def _generate_recommendations(self, risk_scores, detected_patterns, weaknesses):
        """Générer des recommandations pour éviter l'effondrement."""
        recommendations = []
        
        # Identifier les catégories à risque
        high_risk_categories = []
        for category, score in risk_scores.items():
            if score > 0.6:
                high_risk_categories.append(category)
        
        # Recommandations psychologiques
        if 'psychological' in high_risk_categories:
            recommendations.append({
                'area': 'psychological',
                'recommendation': 'Intervention psychologique ciblée',
                'description': 'Séances spécifiques de gestion du stress et de la pression',
                'priority': 'high' if risk_scores['psychological'] > 0.7 else 'medium'
            })
            
            recommendations.append({
                'area': 'psychological',
                'recommendation': 'Gestion de la communication',
                'description': 'Réduire l\'exposition médiatique des joueurs clés',
                'priority': 'medium'
            })
        
        # Recommandations tactiques
        if 'tactical' in high_risk_categories:
            recommendations.append({
                'area': 'tactical',
                'recommendation': 'Développement d\'un plan B',
                'description': 'Préparer une approche tactique alternative',
                'priority': 'high' if risk_scores['tactical'] > 0.75 else 'medium'
            })
            
            recommendations.append({
                'area': 'tactical',
                'recommendation': 'Entraînement d\'adaptabilité',
                'description': 'Exercices visant à améliorer la réponse aux changements tactiques',
                'priority': 'medium'
            })
        
        # Recommandations physiques
        if 'physical' in high_risk_categories:
            recommendations.append({
                'area': 'physical',
                'recommendation': 'Gestion optimisée de la charge',
                'description': 'Ajuster l\'intensité des entraînements pour maximiser la récupération',
                'priority': 'high' if risk_scores['physical'] > 0.7 else 'medium'
            })
        
        # Recommandations historiques
        if 'historical' in high_risk_categories:
            recommendations.append({
                'area': 'historical',
                'recommendation': 'Travail sur le narratif',
                'description': 'Recadrer les expériences passées comme des apprentissages plutôt que des échecs',
                'priority': 'medium'
            })
        
        # Recommandations basées sur les patterns détectés
        for pattern in detected_patterns:
            if pattern['pattern'] == 'complacency':
                recommendations.append({
                    'area': 'mentality',
                    'recommendation': 'Rappel des difficultés potentielles',
                    'description': 'Séances vidéo spécifiques sur les forces de l\'adversaire',
                    'priority': 'high'
                })
            
            elif pattern['pattern'] == 'form_collapse':
                recommendations.append({
                    'area': 'training',
                    'recommendation': 'Retour aux fondamentaux',
                    'description': 'Session d\'entraînement axée sur les bases et la confiance',
                    'priority': 'high'
                })
        
        # Recommandations basées sur les faiblesses identifiées
        for weakness in weaknesses:
            if weakness['weakness'] == 'defensive_frailty':
                recommendations.append({
                    'area': 'defensive',
                    'recommendation': 'Travail défensif intensif',
                    'description': 'Sessions dédiées à l\'organisation défensive et la communication',
                    'priority': 'high'
                })
        
        return recommendations
    
    def _calculate_results_trend(self, results):
        """Calculer la tendance des résultats récents."""
        if not results or len(results) < 3:
            return 'stable'
        
        # Convertir les résultats en scores numériques
        scores = []
        for result in results:
            result_type = result.get('result', 'D')
            if result_type == 'W':
                scores.append(3)
            elif result_type == 'D':
                scores.append(1)
            else:  # 'L'
                scores.append(0)
        
        # Calculer la tendance (linéaire simplifiée)
        n = len(scores)
        avg_score = sum(scores) / n
        
        if n >= 3:
            first_half = sum(scores[:n//2]) / (n//2)
            second_half = sum(scores[n//2:]) / (n - n//2)
            
            if second_half > first_half + 0.5:
                return 'improving'
            elif first_half > second_half + 0.5:
                return 'declining'
        
        return 'stable'
    
    def _compare_form_periods(self, previous_form, current_form):
        """Comparer deux périodes de forme."""
        if not previous_form or not current_form or len(previous_form) != len(current_form):
            return None
        
        # Convertir les résultats en scores
        previous_scores = []
        current_scores = []
        
        for result in previous_form:
            result_type = result.get('result', 'D')
            if result_type == 'W':
                previous_scores.append(3)
            elif result_type == 'D':
                previous_scores.append(1)
            else:  # 'L'
                previous_scores.append(0)
        
        for result in current_form:
            result_type = result.get('result', 'D')
            if result_type == 'W':
                current_scores.append(3)
            elif result_type == 'D':
                current_scores.append(1)
            else:  # 'L'
                current_scores.append(0)
        
        # Calculer les moyennes
        prev_avg = sum(previous_scores) / len(previous_scores)
        curr_avg = sum(current_scores) / len(current_scores)
        
        # Déterminer l'évolution
        if curr_avg > prev_avg + 0.5:
            return 'improved'
        elif prev_avg > curr_avg + 0.5:
            return 'deteriorated'
        else:
            return 'similar'
    
    def _evaluate_style_compatibility(self, team_style, opponent_style):
        """Évaluer la compatibilité des styles de jeu."""
        # Table simplifiée de compatibilité des styles
        compatibility_matrix = {
            'attacking': {
                'attacking': 0.6,   # Compatible (ouvert)
                'defensive': 0.3,   # Peu compatible (fermé)
                'possession': 0.5,  # Modérément compatible
                'counter': 0.4,     # Modérément compatible
                'balanced': 0.6     # Compatible
            },
            'defensive': {
                'attacking': 0.3,   # Peu compatible
                'defensive': 0.2,   # Très peu compatible (fermé)
                'possession': 0.4,  # Modérément compatible
                'counter': 0.3,     # Peu compatible
                'balanced': 0.5     # Modérément compatible
            },
            'possession': {
                'attacking': 0.5,   # Modérément compatible
                'defensive': 0.4,   # Modérément compatible
                'possession': 0.6,  # Compatible
                'counter': 0.3,     # Peu compatible
                'balanced': 0.6     # Compatible
            },
            'counter': {
                'attacking': 0.4,   # Modérément compatible
                'defensive': 0.3,   # Peu compatible
                'possession': 0.3,  # Peu compatible
                'counter': 0.5,     # Modérément compatible
                'balanced': 0.5     # Modérément compatible
            },
            'balanced': {
                'attacking': 0.6,   # Compatible
                'defensive': 0.5,   # Modérément compatible
                'possession': 0.6,  # Compatible
                'counter': 0.5,     # Modérément compatible
                'balanced': 0.7     # Très compatible
            }
        }
        
        # Obtenir la compatibilité de la matrice
        if team_style in compatibility_matrix and opponent_style in compatibility_matrix[team_style]:
            return compatibility_matrix[team_style][opponent_style]
        
        # Valeur par défaut si styles non trouvés
        return 0.5
    
    def _identify_critical_periods(self, season_timeline, team_info):
        """Identifier les périodes critiques pour une équipe au cours d'une saison."""
        critical_periods = []
        
        # Périodes traditionnellement difficiles
        traditional_periods = [
            {'name': 'holiday_fixtures', 'start_month': 12, 'end_month': 1, 'description': 'Période chargée des fêtes'},
            {'name': 'season_end', 'start_month': 4, 'end_month': 5, 'description': 'Fin de saison sous pression'},
            {'name': 'champions_league_ko', 'start_month': 2, 'end_month': 3, 'description': 'Phase à élimination directe en compétition européenne'}
        ]
        
        # Forces et faiblesses de l'équipe
        squad_depth = team_info.get('squad_depth', 0.5)
        experience_level = team_info.get('experience_level', 0.5)
        historical_endurance = team_info.get('historical_endurance', 0.5)
        
        # Évaluer chaque période traditionnelle
        for period in traditional_periods:
            # Calculer le facteur de risque pour cette période
            risk_score = 0.5  # Base
            
            if period['name'] == 'holiday_fixtures':
                risk_score += (1 - squad_depth) * 0.3  # Manque de profondeur = plus de risque
                
                # Vérifier si des matchs difficiles sont prévus
                has_difficult_fixtures = False
                for fixture in season_timeline.get('fixtures', []):
                    if fixture.get('month') in [period['start_month'], period['end_month']] and fixture.get('difficulty', 0) > 0.7:
                        has_difficult_fixtures = True
                        break
                
                if has_difficult_fixtures:
                    risk_score += 0.15
            
            elif period['name'] == 'season_end':
                risk_score += (1 - experience_level) * 0.25  # Manque d'expérience = plus de risque
                risk_score += (1 - historical_endurance) * 0.25  # Faible endurance historique = plus de risque
                
                # Vérifier si l'équipe joue pour un enjeu important
                if team_info.get('title_race', False) or team_info.get('relegation_battle', False):
                    risk_score += 0.2
            
            elif period['name'] == 'champions_league_ko' and team_info.get('in_champions_league', False):
                risk_score += (1 - experience_level) * 0.3  # L'expérience est cruciale en Europe
                
                # Pression supplémentaire si haute attente européenne
                if team_info.get('european_expectations', 0) > 0.7:
                    risk_score += 0.15
            
            # Ajouter la période si le score de risque est significatif
            if risk_score > 0.6:
                critical_periods.append({
                    'period_name': period['name'],
                    'description': period['description'],
                    'risk_score': risk_score,
                    'risk_level': 'high' if risk_score > 0.75 else 'medium',
                    'start_month': period['start_month'],
                    'end_month': period['end_month']
                })
        
        # Ajouter des périodes spécifiques selon le calendrier
        fixture_clusters = self._identify_fixture_clusters(season_timeline)
        for cluster in fixture_clusters:
            risk_score = 0.5 + (cluster['difficulty'] * 0.3) + ((1 - squad_depth) * 0.2)
            
            if risk_score > 0.65:
                critical_periods.append({
                    'period_name': 'fixture_congestion',
                    'description': f"Séquence intense de {cluster['count']} matchs en {cluster['days']} jours",
                    'risk_score': risk_score,
                    'risk_level': 'high' if risk_score > 0.75 else 'medium',
                    'start_date': cluster['start_date'],
                    'end_date': cluster['end_date']
                })
        
        return critical_periods
    
    def _identify_fixture_clusters(self, season_timeline):
        """Identifier les périodes de congestion de matchs."""
        fixtures = season_timeline.get('fixtures', [])
        
        # Trier les matchs par date
        fixtures = sorted(fixtures, key=lambda x: x.get('date', ''))
        
        clusters = []
        current_start = None
        current_fixtures = []
        
        # Identifier les séquences de matchs rapprochés
        for i in range(len(fixtures) - 1):
            current = fixtures[i]
            next_match = fixtures[i + 1]
            
            # Calculer le nombre de jours entre les matchs
            current_date = datetime.fromisoformat(current.get('date', '')) if isinstance(current.get('date', ''), str) else current.get('date')
            next_date = datetime.fromisoformat(next_match.get('date', '')) if isinstance(next_match.get('date', ''), str) else next_match.get('date')
            
            days_between = (next_date - current_date).days
            
            # Si les matchs sont rapprochés (moins de 4 jours)
            if days_between < 4:
                if not current_start:
                    current_start = current_date
                    current_fixtures = [current]
                
                current_fixtures.append(next_match)
            else:
                # Fin d'un cluster potentiel
                if current_start and len(current_fixtures) >= 3:
                    # Calculer la difficulté moyenne
                    avg_difficulty = sum(match.get('difficulty', 0.5) for match in current_fixtures) / len(current_fixtures)
                    
                    clusters.append({
                        'start_date': current_start,
                        'end_date': next_date,
                        'count': len(current_fixtures),
                        'days': (next_date - current_start).days,
                        'difficulty': avg_difficulty,
                        'fixtures': current_fixtures
                    })
                
                # Réinitialiser
                current_start = None
                current_fixtures = []
        
        # Vérifier le dernier cluster potentiel
        if current_start and len(current_fixtures) >= 3:
            avg_difficulty = sum(match.get('difficulty', 0.5) for match in current_fixtures) / len(current_fixtures)
            
            clusters.append({
                'start_date': current_start,
                'end_date': current_fixtures[-1].get('date'),
                'count': len(current_fixtures),
                'days': (current_fixtures[-1].get('date') - current_start).days,
                'difficulty': avg_difficulty,
                'fixtures': current_fixtures
            })
        
        return clusters
    
    def _evaluate_structural_risks(self, team_info):
        """Évaluer les risques structurels d'effondrement."""
        # Extraire les facteurs de risque structurels
        squad_depth = team_info.get('squad_depth', 0.5)
        experience_level = team_info.get('experience_level', 0.5)
        tactical_rigidity = team_info.get('tactical_rigidity', 0.5)
        leadership_quality = team_info.get('leadership_quality', 0.5)
        psychological_resilience = team_info.get('psychological_resilience', 0.5)
        
        # Calculer les scores de risque
        depth_risk = (1 - squad_depth) * 0.8
        experience_risk = (1 - experience_level) * 0.7
        tactical_risk = tactical_rigidity * 0.6
        leadership_risk = (1 - leadership_quality) * 0.7
        psychological_risk = (1 - psychological_resilience) * 0.9
        
        # Calculer le risque structurel global
        overall_risk = (
            depth_risk * 0.2 +
            experience_risk * 0.2 +
            tactical_risk * 0.15 +
            leadership_risk * 0.2 +
            psychological_risk * 0.25
        )
        
        # Identifier les facteurs de risque clés (top 2)
        risk_factors = [
            {'factor': 'squad_depth', 'risk': depth_risk},
            {'factor': 'experience', 'risk': experience_risk},
            {'factor': 'tactical_rigidity', 'risk': tactical_risk},
            {'factor': 'leadership', 'risk': leadership_risk},
            {'factor': 'psychological_resilience', 'risk': psychological_risk}
        ]
        
        sorted_factors = sorted(risk_factors, key=lambda x: x['risk'], reverse=True)
        key_factors = sorted_factors[:2]
        
        return {
            'overall': overall_risk,
            'depth_risk': depth_risk,
            'experience_risk': experience_risk,
            'tactical_risk': tactical_risk,
            'leadership_risk': leadership_risk,
            'psychological_risk': psychological_risk,
            'key_factors': key_factors,
            'risk_level': 'high' if overall_risk > 0.7 else 'medium' if overall_risk > 0.5 else 'low'
        }
    
    def _analyze_historical_collapses(self, team_info):
        """Analyser l'historique d'effondrement d'une équipe."""
        # Extraire les données historiques
        previous_collapses = team_info.get('previous_collapses', 0)
        seasons_analyzed = team_info.get('seasons_analyzed', 5)
        complete_collapses = team_info.get('complete_collapses', 0)
        partial_recoveries = team_info.get('partial_recoveries', 0)
        
        # Éviter la division par zéro
        if seasons_analyzed == 0:
            seasons_analyzed = 1
        
        # Calculer les métriques
        collapse_frequency = previous_collapses / seasons_analyzed
        recovery_rate = partial_recoveries / max(1, previous_collapses)
        complete_collapse_rate = complete_collapses / max(1, previous_collapses)
        
        # Analyser les types d'effondrement historiques
        collapse_types = team_info.get('collapse_types', {})
        dominant_type = max(collapse_types.items(), key=lambda x: x[1])[0] if collapse_types else None
        
        return {
            'collapse_frequency': collapse_frequency,
            'recovery_rate': recovery_rate,
            'complete_collapse_rate': complete_collapse_rate,
            'dominant_type': dominant_type,
            'collapses_per_season': collapse_frequency,
            'recovery_potential': recovery_rate,
            'collapse_severity': complete_collapse_rate,
            'historical_risk': 'high' if collapse_frequency > 0.5 else 'medium' if collapse_frequency > 0.2 else 'low'
        }
    
    def _calculate_team_resilience(self, team_info):
        """Calculer la résilience d'une équipe face à l'adversité."""
        # Extraire les métriques de résilience
        comeback_rate = team_info.get('comeback_rate', 0.5)
        recovery_after_loss = team_info.get('recovery_after_loss', 0.5)
        psychological_resilience = team_info.get('psychological_resilience', 0.5)
        leadership_quality = team_info.get('leadership_quality', 0.5)
        manager_experience = team_info.get('manager_experience', 0.5)
        
        # Facteurs supplémentaires
        strong_dressing_room = team_info.get('strong_dressing_room', False)
        experienced_core = team_info.get('experienced_core', False)
        
        # Calculer le score de résilience
        resilience_score = (
            comeback_rate * 0.2 +
            recovery_after_loss * 0.2 +
            psychological_resilience * 0.2 +
            leadership_quality * 0.2 +
            manager_experience * 0.2
        )
        
        # Ajustements pour facteurs supplémentaires
        if strong_dressing_room:
            resilience_score = min(1.0, resilience_score + 0.1)
        
        if experienced_core:
            resilience_score = min(1.0, resilience_score + 0.1)
        
        return resilience_score
    
    def _identify_conditional_factors(self, team_info):
        """Identifier les facteurs conditionnels qui peuvent influencer le potentiel d'effondrement."""
        conditional_factors = []
        
        # Facteur 1: Dépendance à un joueur clé
        key_player_dependency = team_info.get('key_player_dependency', 0.0)
        if key_player_dependency > 0.7:
            conditional_factors.append({
                'factor': 'key_player_dependency',
                'description': 'Forte dépendance à un joueur clé - risque d\'effondrement en cas de blessure/suspension',
                'impact': 'high',
                'trigger_condition': 'absence du joueur clé'
            })
        
        # Facteur 2: Vulnérabilité aux matchs à l'extérieur
        away_form_differential = team_info.get('away_form_differential', 0.0)
        if away_form_differential > 0.3:  # Grande différence entre domicile et extérieur
            conditional_factors.append({
                'factor': 'away_vulnerability',
                'description': 'Performance nettement inférieure à l\'extérieur',
                'impact': 'medium',
                'trigger_condition': 'série de matchs à l\'extérieur'
            })
        
        # Facteur 3: Vulnérabilité aux blessures
        injury_impact = team_info.get('injury_impact', 0.0)
        if injury_impact > 0.6:
            conditional_factors.append({
                'factor': 'injury_cascade',
                'description': 'Risque d\'effondrement si plusieurs blessures surviennent',
                'impact': 'high',
                'trigger_condition': 'accumulation de blessures'
            })
        
        # Facteur 4: Réaction aux changements de manager
        manager_change_sensitivity = team_info.get('manager_change_sensitivity', 0.0)
        if manager_change_sensitivity > 0.7:
            conditional_factors.append({
                'factor': 'manager_change',
                'description': 'Forte sensibilité aux changements d\'entraîneur',
                'impact': 'high',
                'trigger_condition': 'spéculation sur l\'avenir du manager'
            })
        
        # Facteur 5: Vulnérabilité face à certains styles de jeu
        style_vulnerabilities = team_info.get('style_vulnerabilities', {})
        for style, vulnerability in style_vulnerabilities.items():
            if vulnerability > 0.7:
                conditional_factors.append({
                    'factor': f'vulnerability_{style}',
                    'description': f'Faiblesse face au style de jeu "{style}"',
                    'impact': 'medium',
                    'trigger_condition': f'affronter une équipe jouant en "{style}"'
                })
        
        return conditional_factors
    
    def _calculate_collapse_indicators(self, recent_results, expected_performance):
        """Calculer les indicateurs d'effondrement à partir des résultats récents."""
        # Initialiser les indicateurs
        indicators = {
            'performance_drop': 0.0,
            'consecutive_losses': 0,
            'defensive_collapse': False,
            'ranking_drop': 0
        }
        
        # Calculer la performance actuelle
        n_results = len(recent_results)
        win_count = sum(1 for result in recent_results if result.get('result', '') == 'W')
        actual_performance = win_count / n_results if n_results > 0 else 0
        
        # Baisse de performance par rapport à l'attendu
        indicators['performance_drop'] = max(0, expected_performance - actual_performance)
        
        # Séquence de défaites
        consecutive_losses = 0
        for result in recent_results:
            if result.get('result', '') == 'L':
                consecutive_losses += 1
            else:
                break
        indicators['consecutive_losses'] = consecutive_losses
        
        # Effondrement défensif (si l'équipe concède beaucoup plus de buts que d'habitude)
        recent_conceded = [result.get('goals_conceded', 0) for result in recent_results]
        avg_conceded = sum(recent_conceded) / len(recent_conceded) if recent_conceded else 0
        expected_conceded = recent_results[0].get('expected_conceded', 1.0) if recent_results else 1.0
        
        indicators['defensive_collapse'] = avg_conceded > (expected_conceded * 1.5)
        
        # Chute au classement (si disponible)
        if len(recent_results) >= 2:
            first_ranking = recent_results[-1].get('ranking', 0)
            latest_ranking = recent_results[0].get('ranking', 0)
            indicators['ranking_drop'] = max(0, latest_ranking - first_ranking)
        
        return indicators
    
    def _identify_collapse_type(self, indicators, recent_results):
        """Identifier le type d'effondrement en cours."""
        # Types d'effondrement
        collapse_types = {
            'defensive': 0,
            'offensive': 0,
            'psychological': 0,
            'physical': 0,
            'tactical': 0
        }
        
        # Analyser les indicateurs et les résultats
        
        # Signes d'effondrement défensif
        if indicators['defensive_collapse']:
            collapse_types['defensive'] += 2
        
        # Analyser les buts marqués récemment
        recent_scored = [result.get('goals_scored', 0) for result in recent_results]
        avg_scored = sum(recent_scored) / len(recent_scored) if recent_scored else 0
        expected_scored = recent_results[0].get('expected_scored', 1.0) if recent_results else 1.0
        
        if avg_scored < (expected_scored * 0.7):
            collapse_types['offensive'] += 2
        
        # Signes d'effondrement psychologique
        if indicators['consecutive_losses'] >= 3:
            collapse_types['psychological'] += 1
        
        # Défaites lourdes
        heavy_defeats = sum(1 for result in recent_results if result.get('result', '') == 'L' and 
                          result.get('goals_conceded', 0) - result.get('goals_scored', 0) >= 3)
        if heavy_defeats > 0:
            collapse_types['psychological'] += 1
            collapse_types['tactical'] += 1
        
        # Signes de fatigue physique
        late_goals_conceded = sum(1 for result in recent_results if result.get('late_goals_conceded', 0) > 0)
        if late_goals_conceded >= 2:
            collapse_types['physical'] += 2
        
        # Analyser la distance parcourue (si disponible)
        recent_distance = [result.get('distance_covered', 110) for result in recent_results if 'distance_covered' in result]
        if recent_distance:
            avg_distance = sum(recent_distance) / len(recent_distance)
            expected_distance = 110  # Valeur par défaut
            if avg_distance < (expected_distance * 0.9):
                collapse_types['physical'] += 1
        
        # Signes d'effondrement tactique
        tactical_issues = sum(1 for result in recent_results if result.get('tactical_issues', False))
        if tactical_issues >= 2:
            collapse_types['tactical'] += 2
        
        # Déterminer le type dominant
        dominant_type = max(collapse_types.items(), key=lambda x: x[1])[0]
        
        return dominant_type
    
    def _predict_collapse_recovery(self, team_data, indicators, collapse_type):
        """Prédire la durée et la sévérité de l'effondrement."""
        # Facteurs de récupération
        recovery_factors = {
            'manager_quality': team_data.get('manager_quality', 0.5),
            'squad_depth': team_data.get('squad_depth', 0.5),
            'leadership_quality': team_data.get('leadership_quality', 0.5),
            'financial_resources': team_data.get('financial_resources', 0.5),
            'fixture_difficulty': team_data.get('upcoming_fixture_difficulty', 0.5)
        }
        
        # Calculer le potentiel de récupération
        recovery_potential = (
            recovery_factors['manager_quality'] * 0.25 +
            recovery_factors['squad_depth'] * 0.2 +
            recovery_factors['leadership_quality'] * 0.25 +
            recovery_factors['financial_resources'] * 0.1 -
            recovery_factors['fixture_difficulty'] * 0.2
        )
        
        # Ajuster selon le type d'effondrement
        if collapse_type == 'physical':
            # Plus facile à récupérer avec une bonne profondeur d'effectif
            recovery_duration = 3 - round(recovery_factors['squad_depth'] * 2)
        elif collapse_type == 'psychological':
            # Plus difficile à récupérer, dépend fortement du leadership
            recovery_duration = 5 - round(recovery_factors['leadership_quality'] * 3)
        elif collapse_type == 'tactical':
            # Dépend fortement de la qualité du manager
            recovery_duration = 4 - round(recovery_factors['manager_quality'] * 3)
        else:  # defensive ou offensive
            recovery_duration = 4 - round(recovery_potential * 3)
        
        # Limiter à des valeurs raisonnables
        recovery_duration = max(1, min(6, recovery_duration))
        
        # Prédire la sévérité finale
        severity = indicators['performance_drop'] * (1 - recovery_potential)
        
        # Classification de la sévérité
        severity_level = 'moderate'
        if severity > 0.3:
            severity_level = 'severe'
        elif severity < 0.15:
            severity_level = 'mild'
        
        # Préparer la prédiction
        return {
            'expected_duration': recovery_duration,
            'severity': severity,
            'severity_level': severity_level,
            'recovery_potential': recovery_potential,
            'recovery_plan': self._generate_recovery_plan(collapse_type, recovery_factors),
            'key_recovery_factor': max(recovery_factors.items(), key=lambda x: x[1])[0]
        }
    
    def _generate_recovery_plan(self, collapse_type, recovery_factors):
        """Générer un plan de récupération adapté au type d'effondrement."""
        recovery_plan = []
        
        if collapse_type == 'defensive':
            recovery_plan.append({
                'action': 'session_défensive_intensive',
                'description': 'Sessions d\'entraînement axées sur l\'organisation défensive et la communication',
                'priority': 'high'
            })
            recovery_plan.append({
                'action': 'analyse_vidéo_défensive',
                'description': 'Analyse approfondie des erreurs défensives récentes',
                'priority': 'high'
            })
        
        elif collapse_type == 'offensive':
            recovery_plan.append({
                'action': 'session_finition',
                'description': 'Entraînement intensif de finition et création d\'occasions',
                'priority': 'high'
            })
            recovery_plan.append({
                'action': 'simplification_offensive',
                'description': 'Simplifier temporairement le schéma offensif pour restaurer la confiance',
                'priority': 'medium'
            })
        
        elif collapse_type == 'psychological':
            recovery_plan.append({
                'action': 'intervention_psychologique',
                'description': 'Sessions avec un psychologue sportif pour restaurer la confiance',
                'priority': 'high'
            })
            recovery_plan.append({
                'action': 'activités_de_cohésion',
                'description': 'Activités extra-sportives pour renforcer la cohésion du groupe',
                'priority': 'medium'
            })
        
        elif collapse_type == 'physical':
            recovery_plan.append({
                'action': 'allègement_charge',
                'description': 'Réduction temporaire de l\'intensité des entraînements',
                'priority': 'high'
            })
            recovery_plan.append({
                'action': 'rotation_effectif',
                'description': 'Utilisation plus large de l\'effectif pour les prochains matchs',
                'priority': 'high'
            })
        
        elif collapse_type == 'tactical':
            recovery_plan.append({
                'action': 'revue_tactique',
                'description': 'Révision complète de l\'approche tactique',
                'priority': 'high'
            })
            recovery_plan.append({
                'action': 'retour_aux_fondamentaux',
                'description': 'Se concentrer sur les principes de jeu de base',
                'priority': 'medium'
            })
        
        # Ajouter des actions génériques
        recovery_plan.append({
            'action': 'communication_claire',
            'description': 'Communication transparente sur les objectifs à court terme',
            'priority': 'medium'
        })
        
        # Ajuster selon les facteurs de récupération
        if recovery_factors['leadership_quality'] < 0.4:
            recovery_plan.append({
                'action': 'responsabilisation_leaders',
                'description': 'Impliquer davantage les leaders naturels du vestiaire',
                'priority': 'high'
            })
        
        if recovery_factors['fixture_difficulty'] > 0.7:
            recovery_plan.append({
                'action': 'approche_match_par_match',
                'description': 'Se concentrer uniquement sur le prochain match, sans projection',
                'priority': 'high'
            })
        
        return recovery_plan