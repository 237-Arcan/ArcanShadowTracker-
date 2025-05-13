"""
LateSurgeDetector - Module de détection des remontées tardives.
Analyse les patterns de remontées et les conditions favorisant les comebacks en fin de match.
"""

import random
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict

class LateSurgeDetector:
    """
    LateSurgeDetector - Système de détection des remontées tardives.
    Identifie le potentiel et les conditions propices aux comebacks en fin de match.
    """
    
    def __init__(self):
        """Initialise le module LateSurgeDetector"""
        # Paramètres de détection
        self.detection_parameters = {
            'late_threshold': 75,         # Minute à partir de laquelle on considère "tard" dans le match
            'very_late_threshold': 85,    # Minute à partir de laquelle on considère "très tard"
            'critical_deficit': 2,        # Déficit considéré comme critique (difficile à remonter)
            'moderate_deficit': 1,        # Déficit considéré comme modéré
            'surge_minute_window': 15,    # Fenêtre de temps pour observer une remontée
            'significant_momentum_shift': 0.6  # Seuil pour un changement significatif de momentum
        }
        
        # Facteurs de remontée tardive
        self.surge_factors = {
            'tactical_change': {
                'weight': 0.25,
                'indicators': ['formation_change', 'high_pressing', 'all_out_attack', 'risk_taking']
            },
            'psychological_state': {
                'weight': 0.2,
                'indicators': ['desperation', 'determination', 'belief', 'home_crowd_support']
            },
            'physical_condition': {
                'weight': 0.15,
                'indicators': ['stamina_advantage', 'fitness_levels', 'bench_impact', 'opposition_fatigue']
            },
            'game_state': {
                'weight': 0.2,
                'indicators': ['set_piece_opportunities', 'possession_dominance', 'territory_control', 'opposition_sitting_deep']
            },
            'individual_quality': {
                'weight': 0.2,
                'indicators': ['clutch_performers', 'technical_superiority', 'individual_brilliance', 'leadership']
            }
        }
        
        # Patterns historiques de remontée
        self.surge_patterns = {
            'blitz': {
                'description': "Séquence rapide de buts en rafale",
                'time_requirement': 10,  # Minutes max entre les buts
                'typical_formation': "3-4-3 or 4-2-4",
                'detection_weight': 0.3
            },
            'sustained_pressure': {
                'description': "Pression constante menant à des buts",
                'time_requirement': 15,  # Minutes de domination
                'typical_formation': "4-3-3 or 4-2-3-1",
                'detection_weight': 0.25
            },
            'counter_surge': {
                'description': "Remontée basée sur des contres rapides",
                'time_requirement': 20,  # Fenêtre de temps
                'typical_formation': "3-5-2 or 4-4-2",
                'detection_weight': 0.2
            },
            'set_piece_exploitation': {
                'description': "Exploitation de coups de pied arrêtés multiples",
                'time_requirement': 25,  # Fenêtre de temps
                'typical_formation': "variable",
                'detection_weight': 0.15
            },
            'individual_brilliance': {
                'description': "Performance exceptionnelle d'un joueur clé",
                'time_requirement': 30,  # Fenêtre de temps
                'typical_formation': "any",
                'detection_weight': 0.1
            }
        }
        
        # Historique des analyses
        self.analysis_history = []
        
    def analyze_comeback_potential(self, match_data, current_minute, team1_score, team2_score, team_to_analyze=None):
        """
        Analyser le potentiel de remontée pour une ou les deux équipes.
        
        Args:
            match_data (dict): Données du match
            current_minute (int): Minute actuelle du match
            team1_score (int): Score actuel de l'équipe 1
            team2_score (int): Score actuel de l'équipe 2
            team_to_analyze (str, optional): Équipe spécifique à analyser (sinon les deux)
            
        Returns:
            dict: Analyse du potentiel de remontée
        """
        # Extraire les noms des équipes
        team1_name = match_data.get('home_team', 'Équipe 1')
        team2_name = match_data.get('away_team', 'Équipe 2')
        
        # Vérifier si on est en fin de match
        is_late_game = current_minute >= self.detection_parameters['late_threshold']
        is_very_late_game = current_minute >= self.detection_parameters['very_late_threshold']
        
        # Déterminer si une ou les deux équipes sont menées
        team1_deficit = team2_score - team1_score
        team2_deficit = team1_score - team2_score
        
        team1_trailing = team1_deficit > 0
        team2_trailing = team2_deficit > 0
        
        # Déterminer quelles équipes analyser
        teams_to_analyze = []
        if team_to_analyze:
            if team_to_analyze == team1_name and team1_trailing:
                teams_to_analyze.append((team1_name, team1_deficit))
            elif team_to_analyze == team2_name and team2_trailing:
                teams_to_analyze.append((team2_name, team2_deficit))
        else:
            if team1_trailing:
                teams_to_analyze.append((team1_name, team1_deficit))
            if team2_trailing:
                teams_to_analyze.append((team2_name, team2_deficit))
        
        # Si aucune équipe n'est menée, retourner une analyse vide
        if not teams_to_analyze:
            return {
                'match_minute': current_minute,
                'is_late_game': is_late_game,
                'is_very_late_game': is_very_late_game,
                'teams_analyzed': [],
                'overall_comeback_likelihood': 0.0,
                'message': "Aucune équipe n'est actuellement menée"
            }
        
        # Analyser chaque équipe menée
        team_analyses = {}
        for team_name, deficit in teams_to_analyze:
            team_analyses[team_name] = self._analyze_team_comeback_potential(
                team_name, deficit, match_data, current_minute, is_late_game, is_very_late_game
            )
        
        # Calculer la probabilité globale de remontée
        overall_likelihood = 0.0
        if team_analyses:
            max_likelihood = max(analysis.get('comeback_likelihood', 0) 
                              for analysis in team_analyses.values())
            overall_likelihood = max_likelihood
        
        # Compiler l'analyse complète
        analysis = {
            'match_minute': current_minute,
            'score': f"{team1_score}-{team2_score}",
            'is_late_game': is_late_game,
            'is_very_late_game': is_very_late_game,
            'teams_analyzed': list(team_analyses.keys()),
            'team_analyses': team_analyses,
            'overall_comeback_likelihood': overall_likelihood,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'comeback_potential_analysis',
            'timestamp': datetime.now().isoformat(),
            'match': f"{team1_name} vs {team2_name}",
            'minute': current_minute,
            'score': f"{team1_score}-{team2_score}",
            'teams_analyzed': list(team_analyses.keys()),
            'overall_likelihood': overall_likelihood
        })
        
        return analysis
    
    def detect_surge_patterns(self, match_data, match_timeline=None):
        """
        Détecter les patterns spécifiques de remontée tardive dans le match.
        
        Args:
            match_data (dict): Données du match
            match_timeline (list, optional): Timeline des événements du match
            
        Returns:
            dict: Analyse des patterns de remontée détectés
        """
        team1_name = match_data.get('home_team', 'Équipe 1')
        team2_name = match_data.get('away_team', 'Équipe 2')
        
        # Si aucune timeline n'est fournie, utiliser des données simulées
        if match_timeline is None:
            match_timeline = self._generate_match_timeline(team1_name, team2_name)
        
        # Détecter les périodes de remontée potentielles
        surge_periods = self._detect_surge_periods(match_timeline)
        
        # Analyser chaque période de remontée
        surge_analyses = []
        for period in surge_periods:
            period_analysis = self._analyze_surge_period(period, match_timeline, match_data)
            surge_analyses.append(period_analysis)
        
        # Identifier le pattern le plus probable pour chaque remontée
        for analysis in surge_analyses:
            analysis['detected_pattern'] = self._identify_surge_pattern(analysis, match_timeline)
        
        # Compiler l'analyse complète
        analysis = {
            'match': f"{team1_name} vs {team2_name}",
            'surges_detected': len(surge_analyses),
            'surge_analyses': surge_analyses,
            'match_has_remarkable_surge': any(a.get('significance', 0) > 0.7 for a in surge_analyses),
            'most_significant_surge': max(surge_analyses, key=lambda a: a.get('significance', 0)) if surge_analyses else None,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'surge_pattern_detection',
            'timestamp': datetime.now().isoformat(),
            'match': f"{team1_name} vs {team2_name}",
            'surges_detected': len(surge_analyses),
            'has_remarkable_surge': analysis['match_has_remarkable_surge']
        })
        
        return analysis
    
    def evaluate_team_surge_profile(self, team_name, historical_matches=None):
        """
        Évaluer le profil de remontée tardive d'une équipe basé sur son historique.
        
        Args:
            team_name (str): Nom de l'équipe
            historical_matches (list, optional): Historique des matchs de l'équipe
            
        Returns:
            dict: Profil de remontée de l'équipe
        """
        # Si aucun historique n'est fourni, utiliser des données simulées
        if historical_matches is None:
            historical_matches = self._generate_team_history(team_name)
        
        # Analyser l'historique des remontées
        comeback_history = self._analyze_comeback_history(team_name, historical_matches)
        
        # Analyser les patterns favoris de remontée
        favorite_patterns = self._analyze_favorite_patterns(team_name, historical_matches)
        
        # Analyser les facteurs clés de remontée
        key_factors = self._analyze_key_surge_factors(team_name, historical_matches)
        
        # Calculer le score de résilience
        resilience_score = self._calculate_resilience_score(
            comeback_history, favorite_patterns, key_factors
        )
        
        # Analyser les conditions optimales
        optimal_conditions = self._analyze_optimal_surge_conditions(team_name, historical_matches)
        
        # Compiler le profil complet
        profile = {
            'team_name': team_name,
            'comeback_history': comeback_history,
            'favorite_patterns': favorite_patterns,
            'key_factors': key_factors,
            'resilience_score': resilience_score,
            'optimal_conditions': optimal_conditions,
            'profile_timestamp': datetime.now().isoformat()
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'team_surge_profile',
            'timestamp': datetime.now().isoformat(),
            'team': team_name,
            'resilience_score': resilience_score,
            'favorite_pattern': favorite_patterns[0]['pattern_type'] if favorite_patterns else None,
            'key_factor': key_factors[0]['factor_type'] if key_factors else None
        })
        
        return profile
    
    def predict_surge_dynamics(self, match_data, team1_profile=None, team2_profile=None):
        """
        Prédire les dynamiques de remontée potentielles pour un match.
        
        Args:
            match_data (dict): Données du match
            team1_profile (dict, optional): Profil de remontée de l'équipe 1
            team2_profile (dict, optional): Profil de remontée de l'équipe 2
            
        Returns:
            dict: Prédiction des dynamiques de remontée
        """
        team1_name = match_data.get('home_team', 'Équipe 1')
        team2_name = match_data.get('away_team', 'Équipe 2')
        
        # Générer des profils si non fournis
        if team1_profile is None:
            team1_profile = self.evaluate_team_surge_profile(team1_name)
        
        if team2_profile is None:
            team2_profile = self.evaluate_team_surge_profile(team2_name)
        
        # Analyser le match actuel pour les facteurs de contexte
        context_factors = self._analyze_match_context_factors(match_data)
        
        # Calculer les probabilités de remontée pour chaque équipe
        team1_surge_probability = self._calculate_surge_probability(team1_profile, context_factors, is_home=True)
        team2_surge_probability = self._calculate_surge_probability(team2_profile, context_factors, is_home=False)
        
        # Générer des scénarios de remontée pour chaque équipe
        team1_scenarios = self._generate_surge_scenarios(team1_name, team1_profile, team1_surge_probability)
        team2_scenarios = self._generate_surge_scenarios(team2_name, team2_profile, team2_surge_probability)
        
        # Analyser l'interaction des styles de remontée
        style_interaction = self._analyze_surge_style_interaction(team1_profile, team2_profile)
        
        # Déterminer les minutes clés pour les remontées potentielles
        key_minutes = self._determine_key_surge_minutes(team1_profile, team2_profile, match_data)
        
        # Compiler la prédiction complète
        prediction = {
            'match': f"{team1_name} vs {team2_name}",
            'team1_name': team1_name,
            'team2_name': team2_name,
            'team1_surge_probability': team1_surge_probability,
            'team2_surge_probability': team2_surge_probability,
            'team1_scenarios': team1_scenarios,
            'team2_scenarios': team2_scenarios,
            'style_interaction': style_interaction,
            'key_minutes': key_minutes,
            'most_likely_surge_team': team1_name if team1_surge_probability > team2_surge_probability else team2_name,
            'prediction_timestamp': datetime.now().isoformat()
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'surge_dynamics_prediction',
            'timestamp': datetime.now().isoformat(),
            'match': f"{team1_name} vs {team2_name}",
            'team1_probability': team1_surge_probability,
            'team2_probability': team2_surge_probability,
            'most_likely_team': prediction['most_likely_surge_team']
        })
        
        return prediction
    
    def analyze_in_progress_surge(self, match_data, current_minute, team1_score, team2_score, recent_events):
        """
        Analyser une remontée en cours et prédire son évolution.
        
        Args:
            match_data (dict): Données du match
            current_minute (int): Minute actuelle du match
            team1_score (int): Score actuel de l'équipe 1
            team2_score (int): Score actuel de l'équipe 2
            recent_events (list): Événements récents du match
            
        Returns:
            dict: Analyse de la remontée en cours
        """
        team1_name = match_data.get('home_team', 'Équipe 1')
        team2_name = match_data.get('away_team', 'Équipe 2')
        
        # Détecter si une remontée est en cours
        surge_data = self._detect_active_surge(team1_name, team2_name, current_minute, team1_score, team2_score, recent_events)
        
        if not surge_data['surge_detected']:
            return {
                'match': f"{team1_name} vs {team2_name}",
                'minute': current_minute,
                'score': f"{team1_score}-{team2_score}",
                'surge_detected': False,
                'message': "Aucune remontée en cours détectée",
                'analysis_timestamp': datetime.now().isoformat()
            }
        
        # Analyser la dynamique de la remontée
        surge_team = surge_data['surge_team']
        surge_start_minute = surge_data['start_minute']
        surge_deficit = surge_data['initial_deficit']
        current_deficit = surge_data['current_deficit']
        
        # Calculer le momentum actuel
        current_momentum = self._calculate_surge_momentum(surge_team, surge_start_minute, current_minute, surge_deficit, current_deficit, recent_events)
        
        # Calculer la probabilité de compléter la remontée
        completion_probability = self._calculate_completion_probability(surge_team, current_minute, current_deficit, current_momentum)
        
        # Identifier les facteurs critiques pour compléter la remontée
        critical_factors = self._identify_critical_factors(surge_team, current_minute, current_deficit, match_data)
        
        # Prédire l'évolution de la remontée
        surge_trajectory = self._predict_surge_trajectory(surge_team, current_minute, current_deficit, current_momentum, critical_factors)
        
        # Compiler l'analyse complète
        analysis = {
            'match': f"{team1_name} vs {team2_name}",
            'minute': current_minute,
            'score': f"{team1_score}-{team2_score}",
            'surge_detected': True,
            'surge_team': surge_team,
            'start_minute': surge_start_minute,
            'initial_deficit': surge_deficit,
            'current_deficit': current_deficit,
            'deficit_reduced': surge_deficit - current_deficit,
            'current_momentum': current_momentum,
            'completion_probability': completion_probability,
            'critical_factors': critical_factors,
            'surge_trajectory': surge_trajectory,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'in_progress_surge_analysis',
            'timestamp': datetime.now().isoformat(),
            'match': f"{team1_name} vs {team2_name}",
            'minute': current_minute,
            'surge_team': surge_team,
            'completion_probability': completion_probability
        })
        
        return analysis
    
    def _analyze_team_comeback_potential(self, team_name, deficit, match_data, current_minute, is_late_game, is_very_late_game):
        """Analyser le potentiel de remontée pour une équipe spécifique."""
        # Base de l'analyse
        analysis = {
            'team_name': team_name,
            'deficit': deficit,
            'time_remaining': 90 - current_minute,
            'comeback_likelihood': 0.0,
            'key_factors': [],
            'recommended_tactics': []
        }
        
        # Déterminer la sévérité du déficit
        if deficit >= self.detection_parameters['critical_deficit']:
            deficit_severity = 'critical'
        elif deficit >= self.detection_parameters['moderate_deficit']:
            deficit_severity = 'moderate'
        else:
            deficit_severity = 'minimal'
        
        analysis['deficit_severity'] = deficit_severity
        
        # Calculer la probabilité de base en fonction du temps et du déficit
        base_probability = self._calculate_base_comeback_probability(deficit, current_minute)
        
        # Analyser les facteurs favorables/défavorables
        factor_analysis = self._analyze_team_surge_factors(team_name, match_data, current_minute)
        factor_score = factor_analysis['factor_score']
        
        # Calculer la probabilité ajustée
        adjusted_probability = base_probability * (1 + factor_score)
        
        # Limiter à une valeur entre 0 et 1
        analysis['comeback_likelihood'] = max(0.0, min(1.0, adjusted_probability))
        
        # Ajouter les facteurs clés
        analysis['key_factors'] = factor_analysis['key_factors']
        
        # Générer des recommandations tactiques
        analysis['recommended_tactics'] = self._generate_tactical_recommendations(
            team_name, deficit, current_minute, factor_analysis
        )
        
        # Catégoriser la probabilité
        if analysis['comeback_likelihood'] < 0.2:
            analysis['probability_category'] = 'très faible'
        elif analysis['comeback_likelihood'] < 0.4:
            analysis['probability_category'] = 'faible'
        elif analysis['comeback_likelihood'] < 0.6:
            analysis['probability_category'] = 'modérée'
        elif analysis['comeback_likelihood'] < 0.8:
            analysis['probability_category'] = 'bonne'
        else:
            analysis['probability_category'] = 'très bonne'
        
        return analysis
    
    def _calculate_base_comeback_probability(self, deficit, current_minute):
        """Calculer la probabilité de base de remontée en fonction du déficit et du temps."""
        # Calculer le temps restant
        time_remaining = 90 - current_minute
        
        # Définir un seuil de temps minimum pour chaque déficit
        if deficit >= 3:
            # Pour un déficit de 3+ buts, il faut généralement au moins 30 minutes
            if time_remaining < 30:
                return 0.05  # Très improbable mais pas impossible
            else:
                return 0.1 * (time_remaining / 30)  # 0.1 à 0.3
        
        elif deficit == 2:
            # Pour un déficit de 2 buts, il faut généralement au moins 20 minutes
            if time_remaining < 20:
                return 0.1  # Peu probable mais possible
            else:
                return 0.2 * (time_remaining / 20)  # 0.2 à 0.9
        
        elif deficit == 1:
            # Pour un déficit de 1 but, même 5 minutes peuvent suffire
            if time_remaining < 5:
                return 0.2  # Encore possible
            else:
                return 0.3 * (time_remaining / 10)  # 0.3 à 0.9+
        
        return 0.0  # Déficit nul ou négatif
    
    def _analyze_team_surge_factors(self, team_name, match_data, current_minute):
        """Analyser les facteurs favorisant ou limitant la remontée d'une équipe."""
        # Base de l'analyse
        analysis = {
            'factor_score': 0.0,  # Score global (-1 à 1)
            'key_factors': []     # Facteurs les plus significatifs
        }
        
        # Évaluer chaque catégorie de facteurs
        factor_scores = {}
        
        # Facteur 1: Changements tactiques
        tactical_score = self._evaluate_tactical_factors(team_name, match_data, current_minute)
        factor_scores['tactical_change'] = tactical_score
        
        # Facteur 2: État psychologique
        psychological_score = self._evaluate_psychological_factors(team_name, match_data, current_minute)
        factor_scores['psychological_state'] = psychological_score
        
        # Facteur 3: Condition physique
        physical_score = self._evaluate_physical_factors(team_name, match_data, current_minute)
        factor_scores['physical_condition'] = physical_score
        
        # Facteur 4: État du jeu
        game_state_score = self._evaluate_game_state_factors(team_name, match_data, current_minute)
        factor_scores['game_state'] = game_state_score
        
        # Facteur 5: Qualité individuelle
        individual_score = self._evaluate_individual_factors(team_name, match_data, current_minute)
        factor_scores['individual_quality'] = individual_score
        
        # Calculer le score global pondéré
        total_score = 0.0
        for factor_type, score in factor_scores.items():
            weight = self.surge_factors.get(factor_type, {}).get('weight', 0.2)
            total_score += score * weight
        
        analysis['factor_score'] = total_score
        
        # Déterminer les facteurs clés (les plus significatifs, positifs ou négatifs)
        sorted_factors = sorted(
            [(factor_type, score) for factor_type, score in factor_scores.items()],
            key=lambda x: abs(x[1]),
            reverse=True
        )
        
        # Prendre les 3 facteurs les plus significatifs
        for factor_type, score in sorted_factors[:3]:
            impact = 'positif' if score > 0 else 'négatif'
            factor_description = self._generate_factor_description(factor_type, score)
            
            analysis['key_factors'].append({
                'factor_type': factor_type,
                'impact': impact,
                'score': score,
                'description': factor_description
            })
        
        return analysis
    
    def _evaluate_tactical_factors(self, team_name, match_data, current_minute):
        """Évaluer les facteurs tactiques pour une remontée."""
        # Cette fonction simule l'évaluation des facteurs tactiques
        # Dans une implémentation réelle, elle analyserait des données tactiques réelles
        
        # Simuler un score entre -0.5 et 0.5
        return random.uniform(-0.5, 0.5)
    
    def _evaluate_psychological_factors(self, team_name, match_data, current_minute):
        """Évaluer les facteurs psychologiques pour une remontée."""
        # Cette fonction simule l'évaluation des facteurs psychologiques
        # Dans une implémentation réelle, elle analyserait des indicateurs psychologiques
        
        # Simuler un score entre -0.5 et 0.5
        return random.uniform(-0.5, 0.5)
    
    def _evaluate_physical_factors(self, team_name, match_data, current_minute):
        """Évaluer les facteurs physiques pour une remontée."""
        # Cette fonction simule l'évaluation des facteurs physiques
        # Dans une implémentation réelle, elle analyserait des données de condition physique
        
        # Simuler un score entre -0.5 et 0.5
        return random.uniform(-0.5, 0.5)
    
    def _evaluate_game_state_factors(self, team_name, match_data, current_minute):
        """Évaluer les facteurs d'état du jeu pour une remontée."""
        # Cette fonction simule l'évaluation des facteurs d'état du jeu
        # Dans une implémentation réelle, elle analyserait des statistiques de match
        
        # Simuler un score entre -0.5 et 0.5
        return random.uniform(-0.5, 0.5)
    
    def _evaluate_individual_factors(self, team_name, match_data, current_minute):
        """Évaluer les facteurs de qualité individuelle pour une remontée."""
        # Cette fonction simule l'évaluation des facteurs individuels
        # Dans une implémentation réelle, elle analyserait les performances individuelles
        
        # Simuler un score entre -0.5 et 0.5
        return random.uniform(-0.5, 0.5)
    
    def _generate_factor_description(self, factor_type, score):
        """Générer une description textuelle pour un facteur."""
        # Descriptions positives
        positive_descriptions = {
            'tactical_change': "Flexibilité tactique permettant des ajustements efficaces",
            'psychological_state': "Forte résilience mentale et conviction",
            'physical_condition': "Bonne condition physique et options de banc impactantes",
            'game_state': "Contrôle croissant du jeu et occasions créées",
            'individual_quality': "Joueurs clés capables de moments décisifs"
        }
        
        # Descriptions négatives
        negative_descriptions = {
            'tactical_change': "Manque de flexibilité tactique et d'options",
            'psychological_state': "Signes de résignation et de frustration",
            'physical_condition': "Fatigue visible et manque de fraîcheur",
            'game_state': "Difficultés à créer des occasions claires",
            'individual_quality': "Absence d'individualités capables de faire la différence"
        }
        
        if score > 0:
            return positive_descriptions.get(factor_type, "Facteur positif")
        else:
            return negative_descriptions.get(factor_type, "Facteur négatif")
    
    def _generate_tactical_recommendations(self, team_name, deficit, current_minute, factor_analysis):
        """Générer des recommandations tactiques pour une remontée."""
        recommendations = []
        
        # Facteurs clés de l'analyse
        key_factors = factor_analysis['key_factors']
        
        # Recommandations basées sur le déficit
        if deficit >= 3:
            recommendations.append({
                'type': 'formation',
                'description': "Passer à une formation ultra-offensive (3-4-3 ou similaire)",
                'urgency': 'haute'
            })
        elif deficit == 2:
            recommendations.append({
                'type': 'formation',
                'description': "Adopter une formation plus offensive (4-3-3 ou 4-2-3-1)",
                'urgency': 'moyenne'
            })
        else:  # déficit = 1
            recommendations.append({
                'type': 'formation',
                'description': "Ajuster légèrement vers l'offensive sans déséquilibrer",
                'urgency': 'basse'
            })
        
        # Recommandations basées sur le temps restant
        time_remaining = 90 - current_minute
        if time_remaining < 10:
            recommendations.append({
                'type': 'risque',
                'description': "Risque maximal - tous les joueurs en phase offensive y compris le gardien sur coups de pied arrêtés",
                'urgency': 'très haute'
            })
        elif time_remaining < 20:
            recommendations.append({
                'type': 'pressing',
                'description': "Pressing haut et agressif pour récupérer rapidement le ballon",
                'urgency': 'haute'
            })
        
        # Recommandations basées sur les facteurs clés
        for factor in key_factors:
            if factor['factor_type'] == 'physical_condition' and factor['score'] < 0:
                recommendations.append({
                    'type': 'substitutions',
                    'description': "Utiliser des remplaçants frais pour injecter de l'énergie",
                    'urgency': 'moyenne'
                })
            
            elif factor['factor_type'] == 'individual_quality' and factor['score'] > 0:
                recommendations.append({
                    'type': 'stratégie',
                    'description': "Centraliser le jeu sur les joueurs les plus décisifs",
                    'urgency': 'moyenne'
                })
        
        # Garantir au moins 3 recommandations
        generic_recommendations = [
            {
                'type': 'tempo',
                'description': "Augmenter le tempo et jouer direct vers l'avant",
                'urgency': 'moyenne'
            },
            {
                'type': 'coups de pied arrêtés',
                'description': "Maximiser l'exploitation des coups de pied arrêtés",
                'urgency': 'moyenne'
            },
            {
                'type': 'risque',
                'description': "Prises de risque accrues avec les défenseurs",
                'urgency': 'basse'
            }
        ]
        
        while len(recommendations) < 3:
            if generic_recommendations:
                recommendations.append(generic_recommendations.pop(0))
            else:
                break
        
        return recommendations
    
    def _detect_surge_periods(self, match_timeline):
        """Détecter les périodes de remontée dans la timeline du match."""
        # Base de l'analyse
        surge_periods = []
        
        # Vérifier les données
        if not match_timeline:
            return surge_periods
        
        # Trier la timeline par minute
        sorted_timeline = sorted(match_timeline, key=lambda e: e.get('minute', 0))
        
        # Suivre le score tout au long du match
        team1_score = 0
        team2_score = 0
        team1_deficits = []  # Pour suivre les déficits de l'équipe 1
        team2_deficits = []  # Pour suivre les déficits de l'équipe 2
        
        for event in sorted_timeline:
            minute = event.get('minute', 0)
            event_type = event.get('type', '')
            
            # Mettre à jour le score si c'est un but
            if event_type == 'goal':
                team = event.get('team', '')
                if team == 'team1':
                    team1_score += 1
                elif team == 'team2':
                    team2_score += 1
            
            # Calculer les déficits actuels
            team1_deficit = max(0, team2_score - team1_score)
            team2_deficit = max(0, team1_score - team2_score)
            
            # Enregistrer les déficits
            team1_deficits.append((minute, team1_deficit))
            team2_deficits.append((minute, team2_deficit))
        
        # Analyser les déficits pour détecter les périodes de remontée
        for team_name, deficits in [('team1', team1_deficits), ('team2', team2_deficits)]:
            i = 0
            while i < len(deficits):
                # Si l'équipe est menée à ce moment
                if deficits[i][1] > 0:
                    start_minute = deficits[i][0]
                    start_deficit = deficits[i][1]
                    
                    # Chercher le prochain changement de déficit
                    j = i + 1
                    while j < len(deficits) and deficits[j][1] == start_deficit:
                        j += 1
                    
                    # Si le déficit a diminué après cela
                    if j < len(deficits) and deficits[j][1] < start_deficit:
                        surge_start = j
                        current_deficit = deficits[j][1]
                        
                        # Continuer tant que le déficit diminue ou reste stable
                        while j + 1 < len(deficits) and deficits[j + 1][1] <= current_deficit:
                            current_deficit = deficits[j + 1][1]
                            j += 1
                        
                        end_minute = deficits[j][0]
                        end_deficit = deficits[j][1]
                        
                        # S'assurer que c'est une remontée significative
                        if start_deficit - end_deficit >= 1 or end_deficit == 0:
                            surge_periods.append({
                                'team': team_name,
                                'start_minute': start_minute,
                                'end_minute': end_minute,
                                'duration': end_minute - start_minute,
                                'initial_deficit': start_deficit,
                                'final_deficit': end_deficit,
                                'deficit_reduced': start_deficit - end_deficit,
                                'completed': end_deficit == 0  # Remontée complète si le déficit est éliminé
                            })
                    
                    i = j
                else:
                    i += 1
        
        return surge_periods
    
    def _analyze_surge_period(self, surge_period, match_timeline, match_data):
        """Analyser une période de remontée spécifique."""
        # Base de l'analyse
        analysis = {
            'team': surge_period['team'],
            'period': f"{surge_period['start_minute']}-{surge_period['end_minute']}",
            'duration': surge_period['duration'],
            'deficit_change': f"{surge_period['initial_deficit']}-{surge_period['final_deficit']}",
            'completed': surge_period['completed'],
            'key_events': [],
            'significance': 0.0
        }
        
        # Extraire les événements pertinents de la timeline
        relevant_events = []
        for event in match_timeline:
            minute = event.get('minute', 0)
            if (surge_period['start_minute'] <= minute <= surge_period['end_minute'] and 
                (event.get('team', '') == surge_period['team'] or event.get('type', '') in ['red_card', 'substitution'])):
                relevant_events.append(event)
        
        # Identifier les événements clés
        for event in relevant_events:
            if event.get('type') == 'goal' and event.get('team') == surge_period['team']:
                analysis['key_events'].append({
                    'minute': event.get('minute'),
                    'type': 'goal',
                    'description': event.get('description', 'But marqué'),
                    'importance': 'haute'
                })
            elif event.get('type') == 'red_card' and event.get('team') != surge_period['team']:
                analysis['key_events'].append({
                    'minute': event.get('minute'),
                    'type': 'red_card',
                    'description': "Carton rouge pour l'adversaire",
                    'importance': 'haute'
                })
            elif event.get('type') == 'substitution' and event.get('team') == surge_period['team']:
                analysis['key_events'].append({
                    'minute': event.get('minute'),
                    'type': 'substitution',
                    'description': event.get('description', 'Changement tactique'),
                    'importance': 'moyenne'
                })
            elif event.get('type') == 'tactical_change' and event.get('team') == surge_period['team']:
                analysis['key_events'].append({
                    'minute': event.get('minute'),
                    'type': 'tactical_change',
                    'description': event.get('description', 'Changement de formation'),
                    'importance': 'moyenne'
                })
        
        # Calculer la significance de la remontée
        significance = self._calculate_surge_significance(surge_period, analysis['key_events'])
        analysis['significance'] = significance
        
        # Catégoriser la remontée
        if significance < 0.3:
            analysis['category'] = 'mineure'
        elif significance < 0.6:
            analysis['category'] = 'notable'
        elif significance < 0.8:
            analysis['category'] = 'majeure'
        else:
            analysis['category'] = 'historique'
        
        # Identifier les facteurs clés de la remontée
        analysis['key_factors'] = self._identify_surge_key_factors(
            surge_period, analysis['key_events'], match_data
        )
        
        return analysis
    
    def _identify_surge_pattern(self, surge_analysis, match_timeline):
        """Identifier le pattern de remontée le plus probable."""
        # Base de l'analyse
        pattern_analysis = {
            'pattern_type': '',
            'confidence': 0.0,
            'characteristics': []
        }
        
        # Extraire les points clés
        team = surge_analysis['team']
        start_minute = surge_analysis['period'].split('-')[0]
        end_minute = surge_analysis['period'].split('-')[1]
        key_events = surge_analysis['key_events']
        
        # Calculer les scores pour chaque pattern
        pattern_scores = {}
        
        # Pattern 1: Blitz
        blitz_score = self._evaluate_blitz_pattern(key_events)
        pattern_scores['blitz'] = blitz_score
        
        # Pattern 2: Sustained Pressure
        pressure_score = self._evaluate_sustained_pressure_pattern(team, start_minute, end_minute, match_timeline)
        pattern_scores['sustained_pressure'] = pressure_score
        
        # Pattern 3: Counter Surge
        counter_score = self._evaluate_counter_surge_pattern(team, start_minute, end_minute, match_timeline)
        pattern_scores['counter_surge'] = counter_score
        
        # Pattern 4: Set Piece Exploitation
        set_piece_score = self._evaluate_set_piece_pattern(key_events)
        pattern_scores['set_piece_exploitation'] = set_piece_score
        
        # Pattern 5: Individual Brilliance
        individual_score = self._evaluate_individual_brilliance_pattern(key_events)
        pattern_scores['individual_brilliance'] = individual_score
        
        # Trouver le pattern le plus probable
        best_pattern = max(pattern_scores.items(), key=lambda x: x[1])
        pattern_type = best_pattern[0]
        confidence = best_pattern[1]
        
        pattern_analysis['pattern_type'] = pattern_type
        pattern_analysis['confidence'] = confidence
        
        # Ajouter des caractéristiques spécifiques au pattern
        if pattern_type == 'blitz':
            pattern_analysis['characteristics'] = [
                "Séquence rapide de buts en peu de temps",
                "Attaque intense et directe",
                "Pressing agressif pour récupérer rapidement le ballon"
            ]
        elif pattern_type == 'sustained_pressure':
            pattern_analysis['characteristics'] = [
                "Domination progressive du jeu",
                "Accumulation de occasions et de corners",
                "Usure de la défense adverse par la possession"
            ]
        elif pattern_type == 'counter_surge':
            pattern_analysis['characteristics'] = [
                "Exploitation rapide des espaces en contre-attaque",
                "Efficacité offensive maximale",
                "Organisation défensive permettant des transitions rapides"
            ]
        elif pattern_type == 'set_piece_exploitation':
            pattern_analysis['characteristics'] = [
                "Exploitation efficace des coups de pied arrêtés",
                "Préparations tactiques spécifiques",
                "Présence de spécialistes décisifs"
            ]
        elif pattern_type == 'individual_brilliance':
            pattern_analysis['characteristics'] = [
                "Performance exceptionnelle d'un joueur clé",
                "Moments de génie individuel",
                "Capacité à transcender le jeu collectif"
            ]
        
        return pattern_analysis
    
    def _calculate_surge_significance(self, surge_period, key_events):
        """Calculer la significance d'une remontée."""
        # Facteurs de base
        base_score = 0.5
        
        # Facteur 1: Ampleur de la remontée
        deficit_reduced = surge_period['deficit_reduced']
        deficit_factor = min(0.3, deficit_reduced * 0.15)
        
        # Facteur 2: Remontée complétée ou non
        completion_factor = 0.2 if surge_period['completed'] else 0.0
        
        # Facteur 3: Durée de la remontée (plus c'est court, plus c'est impressionnant)
        duration = max(1, surge_period['duration'])
        duration_factor = min(0.2, (30 / duration) * 0.1)
        
        # Facteur 4: Timing de la remontée (plus c'est tard, plus c'est significatif)
        timing_factor = min(0.2, (surge_period['start_minute'] / 90) * 0.2)
        
        # Facteur 5: Événements clés
        event_factor = min(0.1, len(key_events) * 0.02)
        
        # Calculer le score total
        total_score = base_score + deficit_factor + completion_factor + duration_factor + timing_factor + event_factor
        
        # Limiter entre 0 et 1
        return min(1.0, total_score)
    
    def _identify_surge_key_factors(self, surge_period, key_events, match_data):
        """Identifier les facteurs clés d'une remontée."""
        # Base de l'analyse
        key_factors = []
        
        # Facteur 1: Changements tactiques
        tactical_changes = [e for e in key_events if e.get('type') in ['substitution', 'tactical_change']]
        if tactical_changes:
            key_factors.append({
                'factor_type': 'tactical_change',
                'strength': min(1.0, len(tactical_changes) * 0.3),
                'description': "Ajustements tactiques décisifs"
            })
        
        # Facteur 2: Momentum émotionnel (simulé)
        # Dans une implémentation réelle, cela serait basé sur des indicateurs réels
        if surge_period['completed'] or surge_period['deficit_reduced'] >= 2:
            key_factors.append({
                'factor_type': 'psychological_state',
                'strength': random.uniform(0.7, 0.9),
                'description': "Forte dynamique émotionnelle positive"
            })
        
        # Facteur 3: Qualité individuelle
        crucial_goals = [e for e in key_events if e.get('type') == 'goal' and e.get('importance') == 'haute']
        if crucial_goals:
            key_factors.append({
                'factor_type': 'individual_quality',
                'strength': min(1.0, len(crucial_goals) * 0.4),
                'description': "Moments de qualité individuelle décisifs"
            })
        
        # Facteur 4: Avantage numérique
        red_cards = [e for e in key_events if e.get('type') == 'red_card']
        if red_cards:
            key_factors.append({
                'factor_type': 'game_state',
                'strength': 0.8,
                'description': "Supériorité numérique exploitée efficacement"
            })
        
        # Facteur 5: Condition physique (simulé)
        if surge_period['start_minute'] > 60:
            key_factors.append({
                'factor_type': 'physical_condition',
                'strength': random.uniform(0.6, 0.8),
                'description': "Meilleure condition physique en fin de match"
            })
        
        # Trier par force
        key_factors.sort(key=lambda f: f.get('strength', 0), reverse=True)
        
        # Limiter à 3 facteurs maximum
        return key_factors[:3]
    
    def _evaluate_blitz_pattern(self, key_events):
        """Évaluer la probabilité d'un pattern de blitz."""
        # Compter les buts et leur timing
        goals = [e for e in key_events if e.get('type') == 'goal']
        
        if len(goals) < 2:
            return 0.3  # Peu probable si moins de 2 buts
        
        # Vérifier si les buts ont été marqués rapidement
        goal_minutes = [g.get('minute') for g in goals]
        goal_minutes.sort()
        
        for i in range(len(goal_minutes) - 1):
            if goal_minutes[i+1] - goal_minutes[i] <= self.surge_patterns['blitz']['time_requirement']:
                return 0.8  # Haute probabilité si au moins 2 buts rapprochés
        
        return 0.5  # Probabilité moyenne sinon
    
    def _evaluate_sustained_pressure_pattern(self, team, start_minute, end_minute, match_timeline):
        """Évaluer la probabilité d'un pattern de pression soutenue."""
        # Cette fonction simule l'évaluation
        # Dans une implémentation réelle, elle analyserait des indicateurs de domination
        
        # Simuler une probabilité entre 0.3 et 0.9
        return random.uniform(0.3, 0.9)
    
    def _evaluate_counter_surge_pattern(self, team, start_minute, end_minute, match_timeline):
        """Évaluer la probabilité d'un pattern de contre-attaques."""
        # Cette fonction simule l'évaluation
        # Dans une implémentation réelle, elle analyserait des indicateurs de contre-attaque
        
        # Simuler une probabilité entre 0.3 et 0.9
        return random.uniform(0.3, 0.9)
    
    def _evaluate_set_piece_pattern(self, key_events):
        """Évaluer la probabilité d'un pattern d'exploitation de coups de pied arrêtés."""
        # Compter les buts sur coups de pied arrêtés
        set_piece_goals = [
            e for e in key_events 
            if e.get('type') == 'goal' and 'corner' in e.get('description', '').lower() or 'free kick' in e.get('description', '').lower() or 'penalty' in e.get('description', '').lower()
        ]
        
        if len(set_piece_goals) >= 2:
            return 0.9  # Très probable si au moins 2 buts sur coup de pied arrêté
        elif len(set_piece_goals) == 1:
            return 0.6  # Assez probable si 1 but sur coup de pied arrêté
        else:
            return 0.3  # Peu probable sinon
    
    def _evaluate_individual_brilliance_pattern(self, key_events):
        """Évaluer la probabilité d'un pattern de brillance individuelle."""
        # Chercher des indications de performances individuelles exceptionnelles
        individual_brilliance = [
            e for e in key_events 
            if (e.get('type') == 'goal' and ('solo' in e.get('description', '').lower() or 'spectacular' in e.get('description', '').lower())) or
               ('hat-trick' in e.get('description', '').lower())
        ]
        
        if individual_brilliance:
            return 0.9  # Très probable si des actions individuelles exceptionnelles
        else:
            return 0.4  # Probabilité moyenne sinon
    
    def _analyze_comeback_history(self, team_name, historical_matches):
        """Analyser l'historique des remontées d'une équipe."""
        # Base de l'analyse
        history = {
            'total_matches': len(historical_matches),
            'deficit_situations': 0,
            'comeback_attempts': 0,
            'successful_comebacks': 0,
            'comeback_rate': 0.0,
            'average_deficit_overcome': 0.0,
            'remarkable_comebacks': []
        }
        
        # Compter les situations et remontées
        total_deficit = 0
        total_overcome = 0
        
        for match in historical_matches:
            # Vérifier si l'équipe a été menée
            max_deficit = match.get('max_deficit', 0)
            final_deficit = match.get('final_deficit', 0)
            
            if max_deficit > 0:
                history['deficit_situations'] += 1
                total_deficit += max_deficit
                
                # Vérifier si une remontée a été tentée (réduction du déficit)
                if max_deficit > final_deficit:
                    history['comeback_attempts'] += 1
                    deficit_overcome = max_deficit - final_deficit
                    total_overcome += deficit_overcome
                    
                    # Vérifier si la remontée a été réussie (déficit éliminé)
                    if final_deficit == 0 and match.get('result', '') != 'loss':
                        history['successful_comebacks'] += 1
                        
                        # Vérifier si la remontée est remarquable
                        if max_deficit >= 2 or (max_deficit == 1 and match.get('match_minute_deficit', 0) >= 80):
                            history['remarkable_comebacks'].append({
                                'match': match.get('opponent', 'Équipe inconnue'),
                                'deficit': max_deficit,
                                'minute': match.get('match_minute_deficit', 0),
                                'result': match.get('result', '')
                            })
        
        # Calculer les statistiques
        if history['deficit_situations'] > 0:
            history['comeback_attempt_rate'] = history['comeback_attempts'] / history['deficit_situations']
            
            if history['comeback_attempts'] > 0:
                history['comeback_rate'] = history['successful_comebacks'] / history['comeback_attempts']
                history['average_deficit_overcome'] = total_overcome / history['comeback_attempts']
        
        # Trier les remontées remarquables par importance
        history['remarkable_comebacks'].sort(key=lambda c: c.get('deficit', 0) * 10 + c.get('minute', 0) / 10, reverse=True)
        
        return history
    
    def _analyze_favorite_patterns(self, team_name, historical_matches):
        """Analyser les patterns de remontée favoris d'une équipe."""
        # Base de l'analyse
        patterns = []
        
        # Compter l'utilisation de chaque pattern
        pattern_counts = defaultdict(int)
        pattern_success = defaultdict(int)
        
        for match in historical_matches:
            comeback_data = match.get('comeback_data', {})
            pattern = comeback_data.get('pattern', '')
            
            if pattern and pattern in self.surge_patterns:
                pattern_counts[pattern] += 1
                
                if comeback_data.get('successful', False):
                    pattern_success[pattern] += 1
        
        # Calculer les taux de succès et générer l'analyse
        for pattern, count in pattern_counts.items():
            success_rate = pattern_success[pattern] / count if count > 0 else 0
            
            patterns.append({
                'pattern_type': pattern,
                'usage_count': count,
                'success_count': pattern_success[pattern],
                'success_rate': success_rate,
                'description': self.surge_patterns[pattern]['description'],
                'typical_formation': self.surge_patterns[pattern]['typical_formation']
            })
        
        # Trier par utilisation et taux de succès
        patterns.sort(key=lambda p: (p.get('usage_count', 0), p.get('success_rate', 0)), reverse=True)
        
        return patterns
    
    def _analyze_key_surge_factors(self, team_name, historical_matches):
        """Analyser les facteurs clés de remontée pour une équipe."""
        # Base de l'analyse
        factors = []
        
        # Compter l'importance de chaque facteur
        factor_importance = defaultdict(float)
        factor_frequency = defaultdict(int)
        
        for match in historical_matches:
            comeback_data = match.get('comeback_data', {})
            key_factors = comeback_data.get('key_factors', [])
            
            for factor in key_factors:
                factor_type = factor.get('factor_type', '')
                strength = factor.get('strength', 0.5)
                
                if factor_type in self.surge_factors:
                    factor_importance[factor_type] += strength
                    factor_frequency[factor_type] += 1
        
        # Calculer l'importance moyenne et générer l'analyse
        for factor_type, total_importance in factor_importance.items():
            frequency = factor_frequency[factor_type]
            average_importance = total_importance / frequency if frequency > 0 else 0
            
            factors.append({
                'factor_type': factor_type,
                'frequency': frequency,
                'average_importance': average_importance,
                'weight': self.surge_factors[factor_type]['weight'],
                'indicators': self.surge_factors[factor_type]['indicators']
            })
        
        # Trier par importance moyenne
        factors.sort(key=lambda f: f.get('average_importance', 0), reverse=True)
        
        return factors
    
    def _calculate_resilience_score(self, comeback_history, favorite_patterns, key_factors):
        """Calculer le score de résilience globale d'une équipe."""
        # Base du calcul
        resilience = {
            'overall_score': 0.5,  # Valeur neutre par défaut
            'components': {},
            'interpretation': ''
        }
        
        # Composante 1: Historique de remontées
        history_score = 0.5  # Valeur par défaut
        if comeback_history['deficit_situations'] > 0:
            comeback_rate = comeback_history['successful_comebacks'] / comeback_history['deficit_situations']
            # Ajuster pour donner un score entre 0.2 et 0.8
            history_score = 0.2 + (comeback_rate * 0.6)
        
        resilience['components']['history'] = history_score
        
        # Composante 2: Diversité et efficacité des patterns
        pattern_score = 0.5  # Valeur par défaut
        if favorite_patterns:
            # Nombre de patterns utilisés avec succès
            successful_patterns = len([p for p in favorite_patterns if p.get('success_rate', 0) > 0.3])
            # Taux de succès moyen des patterns principaux
            avg_success_rate = sum(p.get('success_rate', 0) for p in favorite_patterns[:3]) / min(3, len(favorite_patterns))
            
            pattern_score = 0.3 + (successful_patterns * 0.1) + (avg_success_rate * 0.3)
            pattern_score = min(0.9, pattern_score)  # Plafonner à 0.9
        
        resilience['components']['patterns'] = pattern_score
        
        # Composante 3: Diversité et importance des facteurs
        factor_score = 0.5  # Valeur par défaut
        if key_factors:
            # Nombre de facteurs significatifs
            significant_factors = len([f for f in key_factors if f.get('average_importance', 0) > 0.5])
            # Importance moyenne des principaux facteurs
            avg_importance = sum(f.get('average_importance', 0) for f in key_factors[:3]) / min(3, len(key_factors))
            
            factor_score = 0.3 + (significant_factors * 0.1) + (avg_importance * 0.3)
            factor_score = min(0.9, factor_score)  # Plafonner à 0.9
        
        resilience['components']['factors'] = factor_score
        
        # Calculer le score global pondéré
        overall_score = (
            history_score * 0.4 +
            pattern_score * 0.3 +
            factor_score * 0.3
        )
        
        resilience['overall_score'] = overall_score
        
        # Interpréter le score
        if overall_score < 0.3:
            resilience['interpretation'] = "Faible résilience - l'équipe a du mal à revenir lorsqu'elle est menée"
        elif overall_score < 0.5:
            resilience['interpretation'] = "Résilience modérée - capacité inconsistante à effectuer des remontées"
        elif overall_score < 0.7:
            resilience['interpretation'] = "Bonne résilience - capable de remontées régulières dans les bonnes conditions"
        else:
            resilience['interpretation'] = "Excellente résilience - équipe spécialiste des remontées, mentalement forte"
        
        return resilience
    
    def _analyze_optimal_surge_conditions(self, team_name, historical_matches):
        """Analyser les conditions optimales pour les remontées d'une équipe."""
        # Base de l'analyse
        conditions = {
            'optimal_deficit': 0,
            'optimal_timing': 0,
            'favorable_situations': [],
            'unfavorable_situations': []
        }
        
        # Collecter les informations sur les remontées réussies
        successful_deficits = []
        successful_timings = []
        
        for match in historical_matches:
            comeback_data = match.get('comeback_data', {})
            if comeback_data.get('successful', False):
                deficit = comeback_data.get('deficit', 0)
                timing = comeback_data.get('timing', 0)  # Minute où la remontée a commencé
                
                if deficit > 0:
                    successful_deficits.append(deficit)
                
                if timing > 0:
                    successful_timings.append(timing)
        
        # Déterminer le déficit optimal
        if successful_deficits:
            # Le déficit le plus fréquent dans les remontées réussies
            deficit_counts = defaultdict(int)
            for deficit in successful_deficits:
                deficit_counts[deficit] += 1
            
            conditions['optimal_deficit'] = max(deficit_counts.items(), key=lambda x: x[1])[0]
        
        # Déterminer le timing optimal
        if successful_timings:
            # Regrouper les timings par tranches de 15 minutes
            timing_groups = defaultdict(int)
            for timing in successful_timings:
                group = (timing // 15) * 15  # 0-14 → 0, 15-29 → 15, etc.
                timing_groups[group] += 1
            
            optimal_group = max(timing_groups.items(), key=lambda x: x[1])[0]
            conditions['optimal_timing'] = f"{optimal_group}-{optimal_group + 14}"
        
        # Identifier les situations favorables
        conditions['favorable_situations'] = [
            "Déficit d'un but avec plus de 30 minutes à jouer",
            "Domicile avec soutien du public",
            "Adversaire qui recule trop pour défendre son avance",
            "Dynamique positive après un changement tactique"
        ]
        
        # Identifier les situations défavorables
        conditions['unfavorable_situations'] = [
            "Déficit de trois buts ou plus après la 60e minute",
            "Adversaire avec forte capacité de contrôle du ballon",
            "Fatigue visible en fin de match",
            "Démoralisation après un but refusé ou un penalty manqué"
        ]
        
        return conditions
    
    def _analyze_match_context_factors(self, match_data):
        """Analyser les facteurs contextuels d'un match pour les remontées."""
        # Base de l'analyse
        context_factors = {
            'match_importance': 0.5,  # Importance neutre par défaut
            'crowd_factor': 0.5,      # Influence neutre par défaut
            'referee_factor': 0.5,    # Influence neutre par défaut
            'weather_factor': 0.5,    # Influence neutre par défaut
            'pitch_factor': 0.5       # Influence neutre par défaut
        }
        
        # Facteur 1: Importance du match
        match_type = match_data.get('match_type', 'league')
        if match_type == 'final' or match_type == 'semifinal':
            context_factors['match_importance'] = 0.9
        elif match_type == 'important_league' or match_type == 'derby':
            context_factors['match_importance'] = 0.7
        
        # Facteur 2: Influence du public
        attendance = match_data.get('attendance', 0)
        capacity = match_data.get('stadium_capacity', 10000)
        
        if capacity > 0:
            attendance_percentage = min(1.0, attendance / capacity)
            context_factors['crowd_factor'] = 0.3 + (attendance_percentage * 0.5)
        
        # Facteur 3: Influence de l'arbitre (simulé)
        # Dans une implémentation réelle, cela serait basé sur le style d'arbitrage
        context_factors['referee_factor'] = random.uniform(0.4, 0.6)
        
        # Facteur 4: Influence de la météo
        weather = match_data.get('weather', 'clear')
        if weather in ['rain', 'snow', 'strong_wind']:
            context_factors['weather_factor'] = 0.4  # Météo difficile peut réduire les chances de remontée
        else:
            context_factors['weather_factor'] = 0.5  # Météo neutre
        
        # Facteur 5: Influence du terrain
        pitch_condition = match_data.get('pitch_condition', 'good')
        if pitch_condition == 'poor':
            context_factors['pitch_factor'] = 0.4  # Mauvais terrain peut réduire les chances de remontée
        elif pitch_condition == 'excellent':
            context_factors['pitch_factor'] = 0.6  # Excellent terrain peut favoriser les remontées
        
        return context_factors
    
    def _calculate_surge_probability(self, team_profile, context_factors, is_home):
        """Calculer la probabilité de remontée pour une équipe dans un match."""
        # Extraire les composantes clés
        resilience_score = team_profile.get('resilience_score', {}).get('overall_score', 0.5)
        
        # Facteurs additionnels
        home_advantage = 0.1 if is_home else 0.0
        
        # Combiner les facteurs contextuels
        context_score = (
            context_factors['match_importance'] * 0.3 +
            context_factors['crowd_factor'] * 0.3 +
            context_factors['referee_factor'] * 0.1 +
            context_factors['weather_factor'] * 0.1 +
            context_factors['pitch_factor'] * 0.2
        )
        
        # Calculer la probabilité globale
        probability = (
            resilience_score * 0.6 +
            context_score * 0.3 +
            home_advantage
        )
        
        # Limiter entre 0.1 et 0.9
        return max(0.1, min(0.9, probability))
    
    def _generate_surge_scenarios(self, team_name, team_profile, surge_probability):
        """Générer des scénarios de remontée pour une équipe."""
        # Base des scénarios
        scenarios = []
        
        # Extraire les patterns favoris
        favorite_patterns = team_profile.get('favorite_patterns', [])
        
        # Extraire les facteurs clés
        key_factors = team_profile.get('key_factors', [])
        
        # Scénario 1: Remontée basée sur le pattern favori
        if favorite_patterns:
            favorite_pattern = favorite_patterns[0]
            pattern_type = favorite_pattern.get('pattern_type', '')
            
            if pattern_type in self.surge_patterns:
                pattern_prob = surge_probability * 0.8  # Légèrement réduit pour être réaliste
                
                scenarios.append({
                    'scenario_type': 'pattern_based',
                    'pattern': pattern_type,
                    'description': f"Remontée utilisant le pattern favori de l'équipe: {self.surge_patterns[pattern_type]['description']}",
                    'probability': pattern_prob,
                    'key_elements': [
                        f"Formation typique: {favorite_pattern.get('typical_formation', 'variable')}",
                        f"Taux de réussite historique: {favorite_pattern.get('success_rate', 0):.1%}",
                        "Exploitation des forces établies de l'équipe"
                    ]
                })
        
        # Scénario 2: Remontée basée sur les facteurs clés
        if key_factors:
            key_factor = key_factors[0]
            factor_type = key_factor.get('factor_type', '')
            
            if factor_type in self.surge_factors:
                factor_prob = surge_probability * 0.7  # Plus réduit car plus spécifique
                
                indicators = self.surge_factors[factor_type]['indicators']
                key_indicator = indicators[0] if indicators else "variable"
                
                scenarios.append({
                    'scenario_type': 'factor_based',
                    'factor': factor_type,
                    'description': f"Remontée exploitant le facteur clé: {factor_type}",
                    'probability': factor_prob,
                    'key_elements': [
                        f"Indicateur principal: {key_indicator}",
                        f"Importance moyenne: {key_factor.get('average_importance', 0):.2f}",
                        "Adaptation tactique spécifique à ce facteur"
                    ]
                })
        
        # Scénario 3: Remontée opportuniste (toujours inclus)
        opportunity_prob = surge_probability * 0.6  # Encore plus réduit car plus aléatoire
        
        scenarios.append({
            'scenario_type': 'opportunistic',
            'description': "Remontée opportuniste exploitant les erreurs adverses ou circonstances favorables",
            'probability': opportunity_prob,
            'key_elements': [
                "Réaction rapide aux opportunités",
                "Exploitation des faiblesses adverses",
                "Adaptabilité à l'évolution du match"
            ]
        })
        
        # Scénario 4: Non-remontée (échec)
        failure_prob = 1.0 - surge_probability
        
        scenarios.append({
            'scenario_type': 'failure',
            'description': "Tentative de remontée infructueuse",
            'probability': failure_prob,
            'key_elements': [
                "Défense adverse solide",
                "Manque d'efficacité offensive",
                "Temps insuffisant pour renverser le score"
            ]
        })
        
        # Trier par probabilité
        scenarios.sort(key=lambda s: s.get('probability', 0), reverse=True)
        
        return scenarios
    
    def _analyze_surge_style_interaction(self, team1_profile, team2_profile):
        """Analyser l'interaction des styles de remontée des deux équipes."""
        # Base de l'analyse
        interaction = {
            'compatibility': 0.5,  # Valeur neutre par défaut
            'favored_team': None,
            'dynamics': []
        }
        
        # Extraire les patterns favoris
        team1_patterns = team1_profile.get('favorite_patterns', [])
        team2_patterns = team2_profile.get('favorite_patterns', [])
        
        # Extraire les facteurs clés
        team1_factors = team1_profile.get('key_factors', [])
        team2_factors = team2_profile.get('key_factors', [])
        
        # Comparer les styles si les données sont disponibles
        if team1_patterns and team2_patterns:
            team1_pattern = team1_patterns[0].get('pattern_type', '')
            team2_pattern = team2_patterns[0].get('pattern_type', '')
            
            # Dynamiques favorables/défavorables selon les patterns
            favorable_interactions = [
                ('blitz', 'sustained_pressure'),
                ('counter_surge', 'sustained_pressure'),
                ('individual_brilliance', 'set_piece_exploitation')
            ]
            
            unfavorable_interactions = [
                ('blitz', 'counter_surge'),
                ('sustained_pressure', 'set_piece_exploitation'),
                ('individual_brilliance', 'counter_surge')
            ]
            
            if (team1_pattern, team2_pattern) in favorable_interactions or (team2_pattern, team1_pattern) in favorable_interactions:
                interaction['compatibility'] = 0.7
                
                if (team1_pattern, team2_pattern) in favorable_interactions:
                    interaction['favored_team'] = 'team1'
                else:
                    interaction['favored_team'] = 'team2'
                
                interaction['dynamics'].append(
                    f"Le style {team1_pattern if interaction['favored_team'] == 'team1' else team2_pattern} a un avantage naturel contre {team2_pattern if interaction['favored_team'] == 'team1' else team1_pattern}"
                )
            
            elif (team1_pattern, team2_pattern) in unfavorable_interactions or (team2_pattern, team1_pattern) in unfavorable_interactions:
                interaction['compatibility'] = 0.3
                
                if (team2_pattern, team1_pattern) in unfavorable_interactions:
                    interaction['favored_team'] = 'team1'
                else:
                    interaction['favored_team'] = 'team2'
                
                interaction['dynamics'].append(
                    f"Le style {team1_pattern if interaction['favored_team'] == 'team1' else team2_pattern} neutralise efficacement {team2_pattern if interaction['favored_team'] == 'team1' else team1_pattern}"
                )
            
            else:
                interaction['dynamics'].append(
                    f"Les styles {team1_pattern} et {team2_pattern} s'opposent sans avantage clair"
                )
        
        # Comparer les facteurs si disponibles
        if team1_factors and team2_factors:
            team1_factor = team1_factors[0].get('factor_type', '')
            team2_factor = team2_factors[0].get('factor_type', '')
            
            if team1_factor == team2_factor:
                interaction['dynamics'].append(
                    f"Les deux équipes s'appuient sur le même facteur clé ({team1_factor}), créant une confrontation directe"
                )
            else:
                interaction['dynamics'].append(
                    f"L'équipe 1 s'appuie sur {team1_factor} tandis que l'équipe 2 mise sur {team2_factor}"
                )
        
        return interaction
    
    def _determine_key_surge_minutes(self, team1_profile, team2_profile, match_data):
        """Déterminer les minutes clés pour les remontées potentielles."""
        # Base de l'analyse
        key_minutes = []
        
        # Extraire les informations des profils
        team1_optimal = team1_profile.get('optimal_conditions', {}).get('optimal_timing', '')
        team2_optimal = team2_profile.get('optimal_conditions', {}).get('optimal_timing', '')
        
        # Convertir en minutes spécifiques si disponible
        if team1_optimal:
            try:
                start, end = team1_optimal.split('-')
                mid_point = (int(start) + int(end)) // 2
                
                key_minutes.append({
                    'minute': mid_point,
                    'team': 'team1',
                    'description': f"Fenêtre optimale historique pour l'équipe 1",
                    'importance': 'haute'
                })
            except:
                pass
        
        if team2_optimal:
            try:
                start, end = team2_optimal.split('-')
                mid_point = (int(start) + int(end)) // 2
                
                key_minutes.append({
                    'minute': mid_point,
                    'team': 'team2',
                    'description': f"Fenêtre optimale historique pour l'équipe 2",
                    'importance': 'haute'
                })
            except:
                pass
        
        # Ajouter des minutes génériques importantes
        key_minutes.extend([
            {
                'minute': 75,
                'team': 'both',
                'description': "Début de la phase critique en fin de match",
                'importance': 'moyenne'
            },
            {
                'minute': 60,
                'team': 'both',
                'description': "Fenêtre idéale pour les changements tactiques majeurs",
                'importance': 'moyenne'
            },
            {
                'minute': 85,
                'team': 'both',
                'description': "Dernière opportunité pour une remontée désespérée",
                'importance': 'très haute'
            }
        ])
        
        # Trier par minute
        key_minutes.sort(key=lambda m: m.get('minute', 0))
        
        return key_minutes
    
    def _detect_active_surge(self, team1_name, team2_name, current_minute, team1_score, team2_score, recent_events):
        """Détecter si une remontée est actuellement en cours."""
        # Base de l'analyse
        surge_data = {
            'surge_detected': False,
            'surge_team': None,
            'start_minute': 0,
            'initial_deficit': 0,
            'current_deficit': 0
        }
        
        # Vérifier les événements récents pour détecter une remontée
        if not recent_events:
            return surge_data
        
        # Trier les événements par minute
        sorted_events = sorted(recent_events, key=lambda e: e.get('minute', 0))
        
        # Suivre le score au cours des événements récents
        team1_history = []
        team2_history = []
        
        current_team1_score = team1_score
        current_team2_score = team2_score
        
        # Remonter le temps pour reconstruire l'historique des scores
        for event in reversed(sorted_events):
            minute = event.get('minute', 0)
            event_type = event.get('type', '')
            
            if event_type == 'goal':
                team = event.get('team', '')
                if team == 'team1':
                    current_team1_score -= 1
                elif team == 'team2':
                    current_team2_score -= 1
            
            team1_history.insert(0, (minute, current_team1_score, current_team2_score))
            team2_history.insert(0, (minute, current_team1_score, current_team2_score))
        
        # Ajouter le score actuel
        team1_history.append((current_minute, team1_score, team2_score))
        team2_history.append((current_minute, team1_score, team2_score))
        
        # Analyser les histoires de score pour détecter une remontée
        team1_surge = self._detect_team_surge(team1_history)
        team2_surge = self._detect_team_surge(team2_history, is_team1=False)
        
        # Déterminer si une remontée est en cours
        if team1_surge['detected']:
            surge_data['surge_detected'] = True
            surge_data['surge_team'] = team1_name
            surge_data['start_minute'] = team1_surge['start_minute']
            surge_data['initial_deficit'] = team1_surge['initial_deficit']
            surge_data['current_deficit'] = team1_surge['current_deficit']
        elif team2_surge['detected']:
            surge_data['surge_detected'] = True
            surge_data['surge_team'] = team2_name
            surge_data['start_minute'] = team2_surge['start_minute']
            surge_data['initial_deficit'] = team2_surge['initial_deficit']
            surge_data['current_deficit'] = team2_surge['current_deficit']
        
        return surge_data
    
    def _detect_team_surge(self, score_history, is_team1=True):
        """Détecter une remontée pour une équipe à partir de l'historique des scores."""
        # Base de l'analyse
        surge = {
            'detected': False,
            'start_minute': 0,
            'initial_deficit': 0,
            'current_deficit': 0
        }
        
        if len(score_history) < 2:
            return surge
        
        # Calculer les déficits à chaque point
        deficits = []
        for minute, team1_score, team2_score in score_history:
            if is_team1:
                deficit = max(0, team2_score - team1_score)
            else:
                deficit = max(0, team1_score - team2_score)
            
            deficits.append((minute, deficit))
        
        # Chercher un pattern de réduction du déficit
        max_deficit = max(deficits, key=lambda d: d[1])
        max_deficit_minute, max_deficit_value = max_deficit
        
        # Si le déficit maximum est 0, pas de remontée possible
        if max_deficit_value == 0:
            return surge
        
        # Vérifier si le déficit a diminué depuis son maximum
        current_deficit = deficits[-1][1]
        if current_deficit < max_deficit_value:
            # Une remontée est en cours
            surge['detected'] = True
            surge['start_minute'] = max_deficit_minute
            surge['initial_deficit'] = max_deficit_value
            surge['current_deficit'] = current_deficit
        
        return surge
    
    def _calculate_surge_momentum(self, surge_team, surge_start_minute, current_minute, initial_deficit, current_deficit, recent_events):
        """Calculer le momentum actuel d'une remontée en cours."""
        # Base du calcul
        momentum = {
            'value': 0.5,  # Valeur neutre par défaut
            'trend': 'stable',
            'key_indicators': []
        }
        
        # Filtrer les événements pertinents pour la remontée
        relevant_events = [
            e for e in recent_events 
            if e.get('minute', 0) >= surge_start_minute and 
               (e.get('team', '') == surge_team or e.get('type', '') in ['red_card', 'yellow_card', 'penalty'])
        ]
        
        # Facteur 1: Progression de la remontée
        deficit_reduced = initial_deficit - current_deficit
        deficit_progression = deficit_reduced / initial_deficit if initial_deficit > 0 else 0
        
        # Facteur 2: Rapidité de la remontée
        time_elapsed = max(1, current_minute - surge_start_minute)
        reduction_rate = deficit_reduced / time_elapsed
        
        # Facteur 3: Événements récents favorables
        positive_events = 0
        negative_events = 0
        
        for event in relevant_events:
            event_type = event.get('type', '')
            event_team = event.get('team', '')
            
            if event_type == 'goal' and event_team == surge_team:
                positive_events += 1
            elif event_type == 'red_card' and event_team != surge_team:
                positive_events += 1
            elif event_type == 'yellow_card' and event_team != surge_team:
                positive_events += 0.5
            elif event_type == 'penalty' and event_team == surge_team:
                positive_events += 0.5
            elif event_type == 'missed_chance' and event_team == surge_team:
                negative_events += 0.5
            elif event_type == 'yellow_card' and event_team == surge_team:
                negative_events += 0.5
        
        event_factor = (positive_events - negative_events) * 0.1
        
        # Calculer le momentum global
        momentum_value = 0.5 + (deficit_progression * 0.3) + (min(0.3, reduction_rate * 5)) + event_factor
        
        # Limiter entre 0 et 1
        momentum_value = max(0.1, min(0.9, momentum_value))
        momentum['value'] = momentum_value
        
        # Déterminer la tendance
        if deficit_reduced > 0 and positive_events > negative_events:
            momentum['trend'] = 'increasing'
        elif deficit_reduced == 0 or positive_events == negative_events:
            momentum['trend'] = 'stable'
        else:
            momentum['trend'] = 'decreasing'
        
        # Générer des indicateurs clés
        if deficit_progression > 0.5:
            momentum['key_indicators'].append(
                f"Plus de la moitié du déficit déjà comblé"
            )
        
        if reduction_rate > 0.1:
            momentum['key_indicators'].append(
                f"Rythme de remontée rapide ({reduction_rate:.2f} buts par minute)"
            )
        
        if positive_events > negative_events + 1:
            momentum['key_indicators'].append(
                f"Accumulation d'événements positifs récents"
            )
        
        return momentum
    
    def _calculate_completion_probability(self, surge_team, current_minute, current_deficit, current_momentum):
        """Calculer la probabilité de compléter une remontée en cours."""
        # Base du calcul
        time_remaining = 90 - current_minute
        momentum_value = current_momentum.get('value', 0.5)
        
        # Facteur 1: Temps nécessaire par but
        minutes_per_goal_needed = time_remaining / max(1, current_deficit)
        
        # Probabilité de base selon le temps disponible
        if minutes_per_goal_needed < 5:
            time_factor = 0.2  # Très peu probable
        elif minutes_per_goal_needed < 10:
            time_factor = 0.4  # Difficile mais possible
        elif minutes_per_goal_needed < 20:
            time_factor = 0.6  # Plausible
        else:
            time_factor = 0.8  # Très plausible
        
        # Facteur 2: Momentum
        momentum_factor = momentum_value
        
        # Facteur 3: Ampleur du déficit restant
        if current_deficit >= 3:
            deficit_factor = 0.2  # Très difficile
        elif current_deficit == 2:
            deficit_factor = 0.4  # Difficile
        else:  # current_deficit == 1
            deficit_factor = 0.7  # Tout à fait possible
        
        # Calculer la probabilité globale
        probability = (time_factor * 0.4) + (momentum_factor * 0.4) + (deficit_factor * 0.2)
        
        # Limiter entre 0.05 et 0.95
        return max(0.05, min(0.95, probability))
    
    def _identify_critical_factors(self, surge_team, current_minute, current_deficit, match_data):
        """Identifier les facteurs critiques pour compléter une remontée en cours."""
        # Base de l'analyse
        critical_factors = []
        
        # Facteur 1: Gestion du temps
        time_remaining = 90 - current_minute
        if time_remaining < 10:
            critical_factors.append({
                'factor_type': 'time_management',
                'criticality': 'très haute',
                'recommendation': "Maximiser chaque possession et forcer des coups de pied arrêtés"
            })
        elif time_remaining < 20:
            critical_factors.append({
                'factor_type': 'time_management',
                'criticality': 'haute',
                'recommendation': "Augmenter le tempo et créer un sentiment d'urgence"
            })
        
        # Facteur 2: Pression psychologique
        if current_deficit > 1:
            critical_factors.append({
                'factor_type': 'psychological_management',
                'criticality': 'haute',
                'recommendation': "Maintenir la croyance et éviter la précipitation malgré le déficit multiple"
            })
        else:
            critical_factors.append({
                'factor_type': 'psychological_management',
                'criticality': 'moyenne',
                'recommendation': "Équilibrer la patience et l'urgence avec un seul but à marquer"
            })
        
        # Facteur 3: Stratégie offensive
        if current_minute > 80:
            critical_factors.append({
                'factor_type': 'offensive_approach',
                'criticality': 'très haute',
                'recommendation': "Risque maximal - faire monter les défenseurs et le gardien sur coups de pied arrêtés"
            })
        elif current_deficit > 1:
            critical_factors.append({
                'factor_type': 'offensive_approach',
                'criticality': 'haute',
                'recommendation': "Tactique très offensive avec augmentation du nombre d'attaquants"
            })
        else:
            critical_factors.append({
                'factor_type': 'offensive_approach',
                'criticality': 'moyenne',
                'recommendation': "Augmenter la pression sans compromettre complètement l'équilibre défensif"
            })
        
        # Trier par criticité
        criticality_order = {
            'très haute': 0,
            'haute': 1,
            'moyenne': 2,
            'basse': 3
        }
        
        critical_factors.sort(key=lambda f: criticality_order.get(f.get('criticality'), 99))
        
        return critical_factors
    
    def _predict_surge_trajectory(self, surge_team, current_minute, current_deficit, current_momentum, critical_factors):
        """Prédire la trajectoire d'une remontée en cours."""
        # Base de la prédiction
        trajectory = {
            'completion_minute': None,
            'expected_outcome': '',
            'key_phases': [],
            'recommendations': []
        }
        
        # Extraire les paramètres clés
        time_remaining = 90 - current_minute
        momentum_value = current_momentum.get('value', 0.5)
        momentum_trend = current_momentum.get('trend', 'stable')
        
        # Calculer le temps estimé pour combler le déficit
        goal_rate = 0.0
        if momentum_value < 0.3:
            goal_rate = 0.01  # 1 but toutes les 100 minutes (très lent)
        elif momentum_value < 0.5:
            goal_rate = 0.05  # 1 but toutes les 20 minutes
        elif momentum_value < 0.7:
            goal_rate = 0.08  # 1 but toutes les 12-13 minutes
        else:
            goal_rate = 0.12  # 1 but toutes les 8-9 minutes
        
        # Ajuster selon la tendance
        if momentum_trend == 'increasing':
            goal_rate *= 1.2
        elif momentum_trend == 'decreasing':
            goal_rate *= 0.8
        
        # Temps estimé pour combler le déficit
        estimated_minutes_needed = current_deficit / goal_rate
        
        # Déterminer si la remontée est probable
        if estimated_minutes_needed <= time_remaining:
            estimated_completion = current_minute + estimated_minutes_needed
            trajectory['completion_minute'] = round(estimated_completion)
            
            if current_deficit == 1:
                trajectory['expected_outcome'] = "Égalisation probable"
            else:
                trajectory['expected_outcome'] = "Remontée complète probable"
        else:
            deficit_at_end = current_deficit - (time_remaining * goal_rate)
            rounded_deficit = round(deficit_at_end)
            
            if rounded_deficit == 0:
                trajectory['expected_outcome'] = "Égalisation dans les derniers instants"
            else:
                trajectory['expected_outcome'] = f"Remontée partielle probable (déficit final estimé: {rounded_deficit})"
        
        # Générer les phases clés
        third_remaining = time_remaining / 3
        
        trajectory['key_phases'].append({
            'minute': round(current_minute + third_remaining),
            'description': "Phase critique pour maintenir le momentum de remontée",
            'expected_deficit': max(0, current_deficit - (third_remaining * goal_rate))
        })
        
        trajectory['key_phases'].append({
            'minute': round(current_minute + 2 * third_remaining),
            'description': "Dernière opportunité pour des changements tactiques majeurs",
            'expected_deficit': max(0, current_deficit - (2 * third_remaining * goal_rate))
        })
        
        # Générer des recommandations basées sur les facteurs critiques
        for factor in critical_factors:
            trajectory['recommendations'].append(factor.get('recommendation', ''))
        
        return trajectory
    
    def _generate_match_timeline(self, team1_name, team2_name):
        """Générer une timeline simulée pour un match."""
        # Cette fonction simule une timeline de match
        # Dans une implémentation réelle, elle utiliserait des données réelles
        
        timeline = []
        
        # Simuler un score final
        team1_score = random.randint(0, 3)
        team2_score = random.randint(0, 3)
        
        # Générer des événements pour chaque but
        for i in range(team1_score):
            minute = random.randint(1, 90)
            timeline.append({
                'type': 'goal',
                'team': 'team1',
                'minute': minute,
                'description': f"But pour {team1_name}"
            })
        
        for i in range(team2_score):
            minute = random.randint(1, 90)
            timeline.append({
                'type': 'goal',
                'team': 'team2',
                'minute': minute,
                'description': f"But pour {team2_name}"
            })
        
        # Ajouter quelques événements supplémentaires
        event_types = ['yellow_card', 'red_card', 'substitution', 'missed_chance', 'tactical_change']
        num_events = random.randint(5, 15)
        
        for i in range(num_events):
            event_type = random.choice(event_types)
            minute = random.randint(1, 90)
            team = 'team1' if random.random() > 0.5 else 'team2'
            
            timeline.append({
                'type': event_type,
                'team': team,
                'minute': minute,
                'description': f"{event_type} pour {'team1' if team == 'team1' else 'team2'}"
            })
        
        # Trier la timeline par minute
        timeline.sort(key=lambda e: e.get('minute', 0))
        
        return timeline
    
    def _generate_team_history(self, team_name):
        """Générer un historique simulé pour une équipe."""
        # Cette fonction simule un historique d'équipe
        # Dans une implémentation réelle, elle utiliserait des données historiques
        
        history = []
        
        # Générer plusieurs matchs
        for i in range(30):
            # Simuler un match
            match = {
                'opponent': f"Adversaire {random.randint(1, 20)}",
                'date': (datetime.now() - timedelta(days=i*7)).isoformat(),
                'result': random.choice(['win', 'draw', 'loss']),
                'max_deficit': random.randint(0, 3),
                'final_deficit': 0,
                'match_minute_deficit': random.randint(15, 75)
            }
            
            # Si l'équipe a été menée, simuler le déficit final
            if match['max_deficit'] > 0:
                if match['result'] == 'win':
                    match['final_deficit'] = 0
                elif match['result'] == 'draw':
                    match['final_deficit'] = 0
                else:
                    match['final_deficit'] = random.randint(1, match['max_deficit'])
            
            # Ajouter des données de remontée si applicable
            if match['max_deficit'] > 0 and match['max_deficit'] > match['final_deficit']:
                match['comeback_data'] = {
                    'deficit': match['max_deficit'],
                    'timing': match['match_minute_deficit'],
                    'successful': match['final_deficit'] == 0,
                    'pattern': random.choice(list(self.surge_patterns.keys())),
                    'key_factors': [
                        {
                            'factor_type': random.choice(list(self.surge_factors.keys())),
                            'strength': random.uniform(0.5, 0.9)
                        },
                        {
                            'factor_type': random.choice(list(self.surge_factors.keys())),
                            'strength': random.uniform(0.5, 0.9)
                        }
                    ]
                }
            
            history.append(match)
        
        return history