"""
SetPieceThreatEvaluator - Module d'analyse du danger sur coups de pied arrêtés.
Évalue la menace et l'efficacité des équipes sur les phases arrêtées offensives et défensives.
"""

import numpy as np
import random
from datetime import datetime, timedelta
import json
import os
from collections import deque

class SetPieceThreatEvaluator:
    """
    SetPieceThreatEvaluator - Analyse le danger et l'efficacité sur coups de pied arrêtés.
    Évalue la performance offensive et défensive des équipes sur les phases arrêtées.
    """
    
    def __init__(self):
        """Initialise le module SetPieceThreatEvaluator."""
        # Types de coups de pied arrêtés
        self.set_piece_types = {
            'corner': {
                'weight': 0.3,        # Importance relative dans l'analyse
                'avg_conversion': 0.03  # Taux de conversion moyen (référence)
            },
            'free_kick_direct': {
                'weight': 0.25,
                'avg_conversion': 0.07
            },
            'free_kick_indirect': {
                'weight': 0.15,
                'avg_conversion': 0.02
            },
            'penalty': {
                'weight': 0.3,
                'avg_conversion': 0.76
            }
        }
        
        # Facteurs d'efficacité offensive
        self.offensive_factors = {
            'delivery_quality': 0.25,     # Qualité des centres/frappes
            'aerial_threat': 0.2,         # Menace aérienne
            'routine_complexity': 0.15,   # Complexité des combinaisons
            'shooter_quality': 0.2,       # Qualité des tireurs
            'positioning': 0.2            # Positionnement des joueurs
        }
        
        # Facteurs d'efficacité défensive
        self.defensive_factors = {
            'aerial_defense': 0.25,       # Défense aérienne
            'organization': 0.25,         # Organisation défensive
            'concentration': 0.2,         # Concentration
            'goalkeeper_command': 0.15,   # Autorité du gardien
            'man_marking': 0.15           # Marquage individuel
        }
        
        # Zones de menace (pour l'analyse spatiale)
        self.threat_zones = {
            'near_post': {
                'corners': 0.35,          # Importance au premier poteau sur corner
                'free_kicks': 0.25        # Importance au premier poteau sur coup franc
            },
            'far_post': {
                'corners': 0.3,
                'free_kicks': 0.25
            },
            'central': {
                'corners': 0.25,
                'free_kicks': 0.4
            },
            'edge_of_box': {
                'corners': 0.1,
                'free_kicks': 0.1
            }
        }
        
        # Modèles de vulnérabilité défensive
        self.vulnerability_patterns = {
            'zonal_marking_gaps': {
                'description': 'Espaces entre les zones de marquage',
                'detection_threshold': 0.65,
                'exploit_difficulty': 0.7
            },
            'near_post_weakness': {
                'description': 'Faiblesse au premier poteau',
                'detection_threshold': 0.7,
                'exploit_difficulty': 0.5
            },
            'far_post_overload': {
                'description': 'Surcharge au second poteau',
                'detection_threshold': 0.6,
                'exploit_difficulty': 0.6
            },
            'goalkeeper_hesitation': {
                'description': 'Hésitation du gardien sur les sorties',
                'detection_threshold': 0.7,
                'exploit_difficulty': 0.7
            },
            'poor_defensive_coordination': {
                'description': 'Manque de coordination défensive',
                'detection_threshold': 0.6,
                'exploit_difficulty': 0.6
            }
        }
        
        # Historique des analyses
        self.analysis_history = []
        
        # Suivi des équipes
        self.team_set_piece_profiles = {}  # team_id -> profil
    
    def analyze_team_set_pieces(self, team_data, match_history=None):
        """
        Analyser la performance d'une équipe sur coups de pied arrêtés.
        
        Args:
            team_data (dict): Données de l'équipe et des joueurs
            match_history (list, optional): Historique récent des matchs
            
        Returns:
            dict: Analyse complète des coups de pied arrêtés
        """
        # Extraire les informations pertinentes
        team_id = team_data.get('id', '')
        team_name = team_data.get('name', '')
        squad = team_data.get('squad', [])
        
        # Analyser les capacités offensives
        offensive_rating = self._analyze_offensive_capabilities(team_data, squad)
        
        # Analyser les capacités défensives
        defensive_rating = self._analyze_defensive_capabilities(team_data, squad)
        
        # Analyser les données historiques si disponibles
        historical_performance = None
        if match_history:
            historical_performance = self._analyze_historical_performance(team_id, match_history)
        
        # Identifier les spécialistes
        specialists = self._identify_specialists(squad)
        
        # Analyser les zones de menace
        threat_zones = self._analyze_threat_zones(team_data, specialists)
        
        # Déterminer les routines notables
        notable_routines = self._identify_notable_routines(team_data, match_history)
        
        # Calculer l'efficacité globale
        overall_offensive = offensive_rating['overall']
        overall_defensive = defensive_rating['overall']
        
        # Ajuster avec les données historiques si disponibles
        if historical_performance:
            overall_offensive = (overall_offensive * 0.6) + (historical_performance['offensive_efficiency'] * 0.4)
            overall_defensive = (overall_defensive * 0.6) + (historical_performance['defensive_efficiency'] * 0.4)
        
        # Enregistrer le profil de l'équipe
        self.team_set_piece_profiles[team_id] = {
            'timestamp': datetime.now().isoformat(),
            'offensive_rating': overall_offensive,
            'defensive_rating': overall_defensive,
            'specialists': specialists,
            'threat_zones': threat_zones
        }
        
        # Préparer le résultat
        result = {
            'team_name': team_name,
            'offensive_analysis': {
                'overall_rating': overall_offensive,
                'category': self._categorize_rating(overall_offensive),
                'breakdown': offensive_rating['breakdown'],
                'specialists': specialists['offensive'],
                'threat_zones': threat_zones['offensive'],
                'historical_performance': historical_performance['offensive'] if historical_performance else None
            },
            'defensive_analysis': {
                'overall_rating': overall_defensive,
                'category': self._categorize_rating(overall_defensive),
                'breakdown': defensive_rating['breakdown'],
                'vulnerabilities': self._identify_vulnerabilities(team_data, defensive_rating, historical_performance),
                'historical_performance': historical_performance['defensive'] if historical_performance else None
            },
            'notable_routines': notable_routines,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        # Enregistrer l'analyse dans l'historique
        self.analysis_history.append({
            'team_id': team_id,
            'timestamp': datetime.now().isoformat(),
            'offensive_rating': overall_offensive,
            'defensive_rating': overall_defensive
        })
        
        return result
    
    def predict_set_piece_matchup(self, team_data, opponent_data, match_context=None):
        """
        Prédire l'issue probable des coups de pied arrêtés dans un match spécifique.
        
        Args:
            team_data (dict): Données de l'équipe
            opponent_data (dict): Données de l'adversaire
            match_context (dict, optional): Contexte du match
            
        Returns:
            dict: Prédiction des performances sur coups de pied arrêtés
        """
        # Extraire les IDs des équipes
        team_id = team_data.get('id', '')
        opponent_id = opponent_data.get('id', '')
        
        # Obtenir ou créer les profils de set-pieces
        team_profile = self.team_set_piece_profiles.get(team_id, None)
        opponent_profile = self.team_set_piece_profiles.get(opponent_id, None)
        
        # Si les profils n'existent pas, les créer
        if not team_profile:
            team_analysis = self.analyze_team_set_pieces(team_data)
            team_profile = self.team_set_piece_profiles.get(team_id, {
                'offensive_rating': team_analysis['offensive_analysis']['overall_rating'],
                'defensive_rating': team_analysis['defensive_analysis']['overall_rating']
            })
        
        if not opponent_profile:
            opponent_analysis = self.analyze_team_set_pieces(opponent_data)
            opponent_profile = self.team_set_piece_profiles.get(opponent_id, {
                'offensive_rating': opponent_analysis['offensive_analysis']['overall_rating'],
                'defensive_rating': opponent_analysis['defensive_analysis']['overall_rating']
            })
        
        # Calculer les probabilités de base
        team_offensive_strength = team_profile.get('offensive_rating', 0.5)
        opponent_defensive_strength = opponent_profile.get('defensive_rating', 0.5)
        
        opponent_offensive_strength = opponent_profile.get('offensive_rating', 0.5)
        team_defensive_strength = team_profile.get('defensive_rating', 0.5)
        
        # Calculer les avantages relatifs
        team_offensive_advantage = team_offensive_strength - opponent_defensive_strength
        opponent_offensive_advantage = opponent_offensive_strength - team_defensive_strength
        
        # Ajuster selon le contexte du match
        context_factors = {}
        if match_context:
            # Facteurs qui peuvent influencer les coups de pied arrêtés
            weather = match_context.get('weather', 'normal')
            pitch_condition = match_context.get('pitch_condition', 'good')
            crowd_factor = match_context.get('crowd_factor', 0.5)
            
            # Calculer les ajustements de contexte
            context_adjustment = 0.0
            
            if weather in ['rain', 'snow', 'wind']:
                context_adjustment -= 0.05  # Conditions difficiles réduisent l'efficacité
                context_factors['weather'] = {
                    'factor': weather,
                    'impact': -0.05,
                    'description': 'Conditions météorologiques défavorables'
                }
            
            if pitch_condition in ['poor', 'very_poor']:
                context_adjustment -= 0.07
                context_factors['pitch'] = {
                    'factor': pitch_condition,
                    'impact': -0.07,
                    'description': 'Terrain en mauvais état'
                }
            
            # Avantage du public pour l'équipe à domicile
            is_home = match_context.get('is_home', True)
            if is_home:
                crowd_boost = crowd_factor * 0.05
                context_adjustment += crowd_boost
                context_factors['crowd'] = {
                    'factor': 'home_advantage',
                    'impact': crowd_boost,
                    'description': 'Soutien du public domicile'
                }
            
            # Appliquer les ajustements
            team_offensive_advantage += context_adjustment
            team_defensive_strength += context_adjustment * 0.5
        
        # Calculer les probabilités de but sur coup de pied arrêté
        expected_team_goals = self._calculate_expected_set_piece_goals(team_offensive_advantage)
        expected_opponent_goals = self._calculate_expected_set_piece_goals(opponent_offensive_advantage)
        
        # Identifier les matchups clés
        key_matchups = self._identify_key_set_piece_matchups(team_data, opponent_data)
        
        # Calculer le différentiel global
        overall_advantage = team_offensive_advantage - opponent_offensive_advantage
        
        # Déterminer qui a l'avantage
        advantage_team = None
        if overall_advantage > 0.15:
            advantage_team = team_data.get('name', 'Home')
        elif overall_advantage < -0.15:
            advantage_team = opponent_data.get('name', 'Away')
        
        # Générer des recommandations tactiques
        tactical_recommendations = self._generate_set_piece_recommendations(
            team_data, opponent_data, team_profile, opponent_profile
        )
        
        # Préparer le résultat
        result = {
            'team_name': team_data.get('name', 'Home'),
            'opponent_name': opponent_data.get('name', 'Away'),
            'team_offensive_advantage': team_offensive_advantage,
            'opponent_offensive_advantage': opponent_offensive_advantage,
            'expected_team_set_piece_goals': expected_team_goals,
            'expected_opponent_set_piece_goals': expected_opponent_goals,
            'overall_set_piece_advantage': overall_advantage,
            'advantage_team': advantage_team,
            'key_matchups': key_matchups,
            'context_factors': context_factors,
            'tactical_recommendations': tactical_recommendations,
            'prediction_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def analyze_set_piece_event(self, event_data, team_data, opponent_data):
        """
        Analyser un événement spécifique de coup de pied arrêté.
        
        Args:
            event_data (dict): Données de l'événement
            team_data (dict): Données de l'équipe attaquante
            opponent_data (dict): Données de l'équipe défensive
            
        Returns:
            dict: Analyse détaillée de l'événement
        """
        # Extraire les informations pertinentes
        event_type = event_data.get('type', 'corner')  # corner, free_kick, penalty
        minute = event_data.get('minute', 0)
        result = event_data.get('result', 'no_goal')  # goal, no_goal, saved, missed, etc.
        location = event_data.get('location', {})
        players_involved = event_data.get('players_involved', [])
        
        # Récupérer des informations supplémentaires
        set_piece_taker = event_data.get('taker', {})
        delivery_type = event_data.get('delivery_type', 'inswinger')
        zone_targeted = event_data.get('zone_targeted', 'near_post')
        defensive_setup = event_data.get('defensive_setup', 'zonal')
        
        # Évaluer la qualité de l'exécution
        execution_quality = self._evaluate_set_piece_execution(
            event_data, set_piece_taker, team_data
        )
        
        # Évaluer la qualité de la défense
        defense_quality = self._evaluate_set_piece_defense(
            event_data, defensive_setup, opponent_data
        )
        
        # Analyser les facteurs clés qui ont influencé le résultat
        key_factors = self._identify_set_piece_key_factors(
            event_data, execution_quality, defense_quality
        )
        
        # Évaluer l'impact de l'événement sur le match
        match_impact = self._evaluate_set_piece_match_impact(
            event_data, minute, result
        )
        
        # Préparer le résultat
        result = {
            'event_type': event_type,
            'minute': minute,
            'outcome': result,
            'execution_quality': execution_quality,
            'defense_quality': defense_quality,
            'key_factors': key_factors,
            'match_impact': match_impact,
            'technical_details': {
                'taker': set_piece_taker.get('name', ''),
                'delivery_type': delivery_type,
                'zone_targeted': zone_targeted,
                'defensive_setup': defensive_setup
            },
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def generate_set_piece_strategy(self, team_data, opponent_data=None):
        """
        Générer une stratégie optimale de coups de pied arrêtés pour une équipe.
        
        Args:
            team_data (dict): Données de l'équipe
            opponent_data (dict, optional): Données de l'adversaire pour adaptation spécifique
            
        Returns:
            dict: Stratégie recommandée
        """
        # Extraire les informations pertinentes
        team_name = team_data.get('name', '')
        squad = team_data.get('squad', [])
        
        # Analyser l'équipe si ce n'est pas déjà fait
        team_id = team_data.get('id', '')
        if team_id not in self.team_set_piece_profiles:
            self.analyze_team_set_pieces(team_data)
        
        team_profile = self.team_set_piece_profiles.get(team_id, {})
        
        # Identifier les spécialistes
        specialists = self._identify_specialists(squad)
        
        # Générer des stratégies par type de coup de pied arrêté
        corner_strategy = self._generate_corner_strategy(team_data, specialists, opponent_data)
        direct_free_kick_strategy = self._generate_direct_free_kick_strategy(team_data, specialists, opponent_data)
        indirect_free_kick_strategy = self._generate_indirect_free_kick_strategy(team_data, specialists, opponent_data)
        penalty_strategy = self._generate_penalty_strategy(team_data, specialists)
        
        # Générer des stratégies défensives
        defensive_strategies = self._generate_defensive_strategies(team_data, opponent_data)
        
        # Préparer le résultat
        result = {
            'team_name': team_name,
            'offensive_strategies': {
                'corners': corner_strategy,
                'direct_free_kicks': direct_free_kick_strategy,
                'indirect_free_kicks': indirect_free_kick_strategy,
                'penalties': penalty_strategy
            },
            'defensive_strategies': defensive_strategies,
            'key_personnel': {
                'corner_takers': [specialist['name'] for specialist in specialists['offensive']['corner_specialists'][:2]],
                'free_kick_takers': [specialist['name'] for specialist in specialists['offensive']['free_kick_specialists'][:2]],
                'penalty_takers': [specialist['name'] for specialist in specialists['offensive']['penalty_specialists'][:2]],
                'aerial_threats': [specialist['name'] for specialist in specialists['offensive']['aerial_specialists'][:3]]
            },
            'strategy_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def _analyze_offensive_capabilities(self, team_data, squad):
        """Analyser les capacités offensives sur coups de pied arrêtés."""
        # Initialiser les scores par facteur
        factor_scores = {
            'delivery_quality': 0.0,
            'aerial_threat': 0.0,
            'routine_complexity': 0.0,
            'shooter_quality': 0.0,
            'positioning': 0.0
        }
        
        # Analyser la qualité de centre/frappe
        delivery_specialists = []
        for player in squad:
            if 'attributes' in player:
                delivery_rating = (
                    player['attributes'].get('crossing', 0.5) * 0.6 +
                    player['attributes'].get('technique', 0.5) * 0.4
                )
                if delivery_rating > 0.7:
                    delivery_specialists.append({
                        'id': player.get('id', ''),
                        'name': player.get('name', ''),
                        'rating': delivery_rating
                    })
        
        # Trier et prendre les meilleurs
        delivery_specialists.sort(key=lambda x: x['rating'], reverse=True)
        top_delivery = delivery_specialists[:3]
        
        if top_delivery:
            factor_scores['delivery_quality'] = sum(s['rating'] for s in top_delivery) / len(top_delivery)
        
        # Analyser la menace aérienne
        aerial_specialists = []
        for player in squad:
            if 'attributes' in player:
                aerial_rating = (
                    player['attributes'].get('jumping', 0.5) * 0.4 +
                    player['attributes'].get('heading', 0.5) * 0.4 +
                    player['attributes'].get('height', 0.5) * 0.2
                )
                if aerial_rating > 0.65:
                    aerial_specialists.append({
                        'id': player.get('id', ''),
                        'name': player.get('name', ''),
                        'rating': aerial_rating
                    })
        
        # Trier et prendre les meilleurs
        aerial_specialists.sort(key=lambda x: x['rating'], reverse=True)
        top_aerial = aerial_specialists[:4]
        
        if top_aerial:
            factor_scores['aerial_threat'] = sum(s['rating'] for s in top_aerial) / len(top_aerial)
        
        # Évaluer la complexité des routines (basée sur les tactiques de l'équipe)
        tactical_creativity = team_data.get('tactical_creativity', 0.5)
        set_piece_innovation = team_data.get('set_piece_innovation', 0.5)
        
        factor_scores['routine_complexity'] = (tactical_creativity * 0.6) + (set_piece_innovation * 0.4)
        
        # Évaluer la qualité des tireurs (coups francs directs, penalties)
        shooter_specialists = []
        for player in squad:
            if 'attributes' in player:
                shooting_rating = (
                    player['attributes'].get('shooting', 0.5) * 0.4 +
                    player['attributes'].get('technique', 0.5) * 0.4 +
                    player['attributes'].get('composure', 0.5) * 0.2
                )
                if shooting_rating > 0.7:
                    shooter_specialists.append({
                        'id': player.get('id', ''),
                        'name': player.get('name', ''),
                        'rating': shooting_rating
                    })
        
        # Trier et prendre les meilleurs
        shooter_specialists.sort(key=lambda x: x['rating'], reverse=True)
        top_shooters = shooter_specialists[:2]
        
        if top_shooters:
            factor_scores['shooter_quality'] = sum(s['rating'] for s in top_shooters) / len(top_shooters)
        
        # Évaluer le positionnement
        set_piece_organization = team_data.get('set_piece_organization', 0.5)
        positional_awareness = team_data.get('positional_awareness', 0.5)
        
        factor_scores['positioning'] = (set_piece_organization * 0.7) + (positional_awareness * 0.3)
        
        # Calculer le score global pondéré
        overall_score = 0.0
        for factor, score in factor_scores.items():
            overall_score += score * self.offensive_factors[factor]
        
        return {
            'overall': overall_score,
            'breakdown': factor_scores
        }
    
    def _analyze_defensive_capabilities(self, team_data, squad):
        """Analyser les capacités défensives sur coups de pied arrêtés."""
        # Initialiser les scores par facteur
        factor_scores = {
            'aerial_defense': 0.0,
            'organization': 0.0,
            'concentration': 0.0,
            'goalkeeper_command': 0.0,
            'man_marking': 0.0
        }
        
        # Analyser la défense aérienne
        aerial_defenders = []
        for player in squad:
            position = player.get('position', '')
            if position in ['CB', 'LB', 'RB', 'DM'] and 'attributes' in player:
                aerial_rating = (
                    player['attributes'].get('jumping', 0.5) * 0.3 +
                    player['attributes'].get('heading', 0.5) * 0.3 +
                    player['attributes'].get('defensive_positioning', 0.5) * 0.2 +
                    player['attributes'].get('height', 0.5) * 0.2
                )
                if aerial_rating > 0.65:
                    aerial_defenders.append({
                        'id': player.get('id', ''),
                        'name': player.get('name', ''),
                        'rating': aerial_rating
                    })
        
        # Trier et prendre les meilleurs
        aerial_defenders.sort(key=lambda x: x['rating'], reverse=True)
        top_aerial_defenders = aerial_defenders[:4]
        
        if top_aerial_defenders:
            factor_scores['aerial_defense'] = sum(s['rating'] for s in top_aerial_defenders) / len(top_aerial_defenders)
        
        # Évaluer l'organisation défensive
        defensive_organization = team_data.get('defensive_organization', 0.5)
        set_piece_defensive_drilling = team_data.get('set_piece_defensive_drilling', 0.5)
        
        factor_scores['organization'] = (defensive_organization * 0.5) + (set_piece_defensive_drilling * 0.5)
        
        # Évaluer la concentration
        team_concentration = team_data.get('concentration', 0.5)
        mental_resilience = team_data.get('mental_resilience', 0.5)
        
        factor_scores['concentration'] = (team_concentration * 0.6) + (mental_resilience * 0.4)
        
        # Évaluer l'autorité du gardien
        goalkeeper = None
        for player in squad:
            if player.get('position', '') == 'GK':
                goalkeeper = player
                break
        
        if goalkeeper and 'attributes' in goalkeeper:
            goalkeeper_rating = (
                goalkeeper['attributes'].get('commanding_area', 0.5) * 0.4 +
                goalkeeper['attributes'].get('aerial_ability', 0.5) * 0.4 +
                goalkeeper['attributes'].get('communication', 0.5) * 0.2
            )
            factor_scores['goalkeeper_command'] = goalkeeper_rating
        
        # Évaluer le marquage individuel
        marking_quality = team_data.get('marking_quality', 0.5)
        defensive_awareness = team_data.get('defensive_awareness', 0.5)
        
        factor_scores['man_marking'] = (marking_quality * 0.6) + (defensive_awareness * 0.4)
        
        # Calculer le score global pondéré
        overall_score = 0.0
        for factor, score in factor_scores.items():
            overall_score += score * self.defensive_factors[factor]
        
        return {
            'overall': overall_score,
            'breakdown': factor_scores
        }
    
    def _analyze_historical_performance(self, team_id, match_history):
        """Analyser la performance historique sur coups de pied arrêtés."""
        # Compteurs pour les statistiques
        total_matches = len(match_history)
        if total_matches == 0:
            return None
        
        # Statistiques offensives
        corner_count = 0
        corners_converted = 0
        direct_fk_count = 0
        direct_fk_converted = 0
        indirect_fk_count = 0
        indirect_fk_converted = 0
        penalties_count = 0
        penalties_converted = 0
        
        # Statistiques défensives
        corners_against = 0
        corners_conceded = 0
        direct_fk_against = 0
        direct_fk_conceded = 0
        indirect_fk_against = 0
        indirect_fk_conceded = 0
        penalties_against = 0
        penalties_conceded = 0
        
        # Traiter chaque match
        for match in match_history:
            set_pieces = match.get('set_pieces', {})
            
            # Statistiques offensives
            offensive_stats = set_pieces.get('offensive', {})
            corner_count += offensive_stats.get('corners', {}).get('count', 0)
            corners_converted += offensive_stats.get('corners', {}).get('converted', 0)
            direct_fk_count += offensive_stats.get('direct_free_kicks', {}).get('count', 0)
            direct_fk_converted += offensive_stats.get('direct_free_kicks', {}).get('converted', 0)
            indirect_fk_count += offensive_stats.get('indirect_free_kicks', {}).get('count', 0)
            indirect_fk_converted += offensive_stats.get('indirect_free_kicks', {}).get('converted', 0)
            penalties_count += offensive_stats.get('penalties', {}).get('count', 0)
            penalties_converted += offensive_stats.get('penalties', {}).get('converted', 0)
            
            # Statistiques défensives
            defensive_stats = set_pieces.get('defensive', {})
            corners_against += defensive_stats.get('corners', {}).get('count', 0)
            corners_conceded += defensive_stats.get('corners', {}).get('conceded', 0)
            direct_fk_against += defensive_stats.get('direct_free_kicks', {}).get('count', 0)
            direct_fk_conceded += defensive_stats.get('direct_free_kicks', {}).get('conceded', 0)
            indirect_fk_against += defensive_stats.get('indirect_free_kicks', {}).get('count', 0)
            indirect_fk_conceded += defensive_stats.get('indirect_free_kicks', {}).get('conceded', 0)
            penalties_against += defensive_stats.get('penalties', {}).get('count', 0)
            penalties_conceded += defensive_stats.get('penalties', {}).get('conceded', 0)
        
        # Calculer les taux de conversion offensifs
        corner_conversion = corners_converted / corner_count if corner_count > 0 else 0
        direct_fk_conversion = direct_fk_converted / direct_fk_count if direct_fk_count > 0 else 0
        indirect_fk_conversion = indirect_fk_converted / indirect_fk_count if indirect_fk_count > 0 else 0
        penalty_conversion = penalties_converted / penalties_count if penalties_count > 0 else 0
        
        # Calculer les taux de concession défensifs
        corner_concession = corners_conceded / corners_against if corners_against > 0 else 0
        direct_fk_concession = direct_fk_conceded / direct_fk_against if direct_fk_against > 0 else 0
        indirect_fk_concession = indirect_fk_conceded / indirect_fk_against if indirect_fk_against > 0 else 0
        penalty_concession = penalties_conceded / penalties_against if penalties_against > 0 else 0
        
        # Calculer l'efficacité offensive globale
        offensive_efficiency = 0.0
        offensive_weights = 0.0
        
        if corner_count > 0:
            corner_relative = corner_conversion / self.set_piece_types['corner']['avg_conversion']
            offensive_efficiency += corner_relative * self.set_piece_types['corner']['weight']
            offensive_weights += self.set_piece_types['corner']['weight']
        
        if direct_fk_count > 0:
            direct_fk_relative = direct_fk_conversion / self.set_piece_types['free_kick_direct']['avg_conversion']
            offensive_efficiency += direct_fk_relative * self.set_piece_types['free_kick_direct']['weight']
            offensive_weights += self.set_piece_types['free_kick_direct']['weight']
        
        if indirect_fk_count > 0:
            indirect_fk_relative = indirect_fk_conversion / self.set_piece_types['free_kick_indirect']['avg_conversion']
            offensive_efficiency += indirect_fk_relative * self.set_piece_types['free_kick_indirect']['weight']
            offensive_weights += self.set_piece_types['free_kick_indirect']['weight']
        
        if penalties_count > 0:
            penalty_relative = penalty_conversion / self.set_piece_types['penalty']['avg_conversion']
            offensive_efficiency += penalty_relative * self.set_piece_types['penalty']['weight']
            offensive_weights += self.set_piece_types['penalty']['weight']
        
        # Normaliser l'efficacité offensive
        if offensive_weights > 0:
            offensive_efficiency /= offensive_weights
        else:
            offensive_efficiency = 0.5  # Valeur par défaut
        
        # Calculer l'efficacité défensive globale (inversée - plus petit est meilleur)
        defensive_efficiency = 0.0
        defensive_weights = 0.0
        
        if corners_against > 0:
            corner_def_relative = 1 - (corner_concession / self.set_piece_types['corner']['avg_conversion'])
            defensive_efficiency += corner_def_relative * self.set_piece_types['corner']['weight']
            defensive_weights += self.set_piece_types['corner']['weight']
        
        if direct_fk_against > 0:
            direct_fk_def_relative = 1 - (direct_fk_concession / self.set_piece_types['free_kick_direct']['avg_conversion'])
            defensive_efficiency += direct_fk_def_relative * self.set_piece_types['free_kick_direct']['weight']
            defensive_weights += self.set_piece_types['free_kick_direct']['weight']
        
        if indirect_fk_against > 0:
            indirect_fk_def_relative = 1 - (indirect_fk_concession / self.set_piece_types['free_kick_indirect']['avg_conversion'])
            defensive_efficiency += indirect_fk_def_relative * self.set_piece_types['free_kick_indirect']['weight']
            defensive_weights += self.set_piece_types['free_kick_indirect']['weight']
        
        if penalties_against > 0:
            penalty_def_relative = 1 - (penalty_concession / self.set_piece_types['penalty']['avg_conversion'])
            defensive_efficiency += penalty_def_relative * self.set_piece_types['penalty']['weight']
            defensive_weights += self.set_piece_types['penalty']['weight']
        
        # Normaliser l'efficacité défensive
        if defensive_weights > 0:
            defensive_efficiency /= defensive_weights
        else:
            defensive_efficiency = 0.5  # Valeur par défaut
        
        # Limiter les valeurs à des plages raisonnables
        offensive_efficiency = max(0.1, min(2.0, offensive_efficiency))
        defensive_efficiency = max(0.1, min(2.0, defensive_efficiency))
        
        # Préparer les statistiques offensives
        offensive_stats = {
            'corners': {
                'count': corner_count,
                'converted': corners_converted,
                'conversion_rate': corner_conversion,
                'vs_average': corner_conversion / self.set_piece_types['corner']['avg_conversion'] if corner_count > 0 else 1.0
            },
            'direct_free_kicks': {
                'count': direct_fk_count,
                'converted': direct_fk_converted,
                'conversion_rate': direct_fk_conversion,
                'vs_average': direct_fk_conversion / self.set_piece_types['free_kick_direct']['avg_conversion'] if direct_fk_count > 0 else 1.0
            },
            'indirect_free_kicks': {
                'count': indirect_fk_count,
                'converted': indirect_fk_converted,
                'conversion_rate': indirect_fk_conversion,
                'vs_average': indirect_fk_conversion / self.set_piece_types['free_kick_indirect']['avg_conversion'] if indirect_fk_count > 0 else 1.0
            },
            'penalties': {
                'count': penalties_count,
                'converted': penalties_converted,
                'conversion_rate': penalty_conversion,
                'vs_average': penalty_conversion / self.set_piece_types['penalty']['avg_conversion'] if penalties_count > 0 else 1.0
            }
        }
        
        # Préparer les statistiques défensives
        defensive_stats = {
            'corners': {
                'count': corners_against,
                'conceded': corners_conceded,
                'concession_rate': corner_concession,
                'vs_average': corner_concession / self.set_piece_types['corner']['avg_conversion'] if corners_against > 0 else 1.0
            },
            'direct_free_kicks': {
                'count': direct_fk_against,
                'conceded': direct_fk_conceded,
                'concession_rate': direct_fk_concession,
                'vs_average': direct_fk_concession / self.set_piece_types['free_kick_direct']['avg_conversion'] if direct_fk_against > 0 else 1.0
            },
            'indirect_free_kicks': {
                'count': indirect_fk_against,
                'conceded': indirect_fk_conceded,
                'concession_rate': indirect_fk_concession,
                'vs_average': indirect_fk_concession / self.set_piece_types['free_kick_indirect']['avg_conversion'] if indirect_fk_against > 0 else 1.0
            },
            'penalties': {
                'count': penalties_against,
                'conceded': penalties_conceded,
                'concession_rate': penalty_concession,
                'vs_average': penalty_concession / self.set_piece_types['penalty']['avg_conversion'] if penalties_against > 0 else 1.0
            }
        }
        
        return {
            'offensive': offensive_stats,
            'defensive': defensive_stats,
            'offensive_efficiency': offensive_efficiency,
            'defensive_efficiency': defensive_efficiency,
            'matches_analyzed': total_matches
        }
    
    def _identify_specialists(self, squad):
        """Identifier les spécialistes de coups de pied arrêtés dans l'équipe."""
        # Spécialistes offensifs
        corner_specialists = []
        free_kick_specialists = []
        penalty_specialists = []
        aerial_specialists = []
        
        for player in squad:
            attributes = player.get('attributes', {})
            
            # Évaluer les capacités de corner
            if 'crossing' in attributes:
                corner_rating = (
                    attributes.get('crossing', 0.5) * 0.6 +
                    attributes.get('technique', 0.5) * 0.3 +
                    attributes.get('composure', 0.5) * 0.1
                )
                if corner_rating > 0.7:
                    corner_specialists.append({
                        'id': player.get('id', ''),
                        'name': player.get('name', ''),
                        'position': player.get('position', ''),
                        'rating': corner_rating
                    })
            
            # Évaluer les capacités de coup franc
            if 'free_kick' in attributes or 'shooting' in attributes:
                free_kick_rating = (
                    attributes.get('free_kick', attributes.get('shooting', 0.5)) * 0.5 +
                    attributes.get('technique', 0.5) * 0.3 +
                    attributes.get('composure', 0.5) * 0.2
                )
                if free_kick_rating > 0.7:
                    free_kick_specialists.append({
                        'id': player.get('id', ''),
                        'name': player.get('name', ''),
                        'position': player.get('position', ''),
                        'rating': free_kick_rating
                    })
            
            # Évaluer les capacités de penalty
            if 'penalty' in attributes or 'composure' in attributes:
                penalty_rating = (
                    attributes.get('penalty', attributes.get('composure', 0.5)) * 0.6 +
                    attributes.get('technique', 0.5) * 0.2 +
                    attributes.get('mental_strength', 0.5) * 0.2
                )
                if penalty_rating > 0.7:
                    penalty_specialists.append({
                        'id': player.get('id', ''),
                        'name': player.get('name', ''),
                        'position': player.get('position', ''),
                        'rating': penalty_rating
                    })
            
            # Évaluer les capacités aériennes
            if 'heading' in attributes or 'jumping' in attributes:
                aerial_rating = (
                    attributes.get('heading', 0.5) * 0.4 +
                    attributes.get('jumping', 0.5) * 0.3 +
                    attributes.get('height', 0.5) * 0.2 +
                    attributes.get('strength', 0.5) * 0.1
                )
                if aerial_rating > 0.7:
                    aerial_specialists.append({
                        'id': player.get('id', ''),
                        'name': player.get('name', ''),
                        'position': player.get('position', ''),
                        'rating': aerial_rating
                    })
        
        # Trier chaque liste par score
        corner_specialists.sort(key=lambda x: x['rating'], reverse=True)
        free_kick_specialists.sort(key=lambda x: x['rating'], reverse=True)
        penalty_specialists.sort(key=lambda x: x['rating'], reverse=True)
        aerial_specialists.sort(key=lambda x: x['rating'], reverse=True)
        
        # Spécialistes défensifs
        defensive_aerial_specialists = []
        gk_set_piece_specialists = []
        
        for player in squad:
            attributes = player.get('attributes', {})
            position = player.get('position', '')
            
            # Évaluer les capacités défensives aériennes
            if position in ['CB', 'LB', 'RB', 'DM'] and ('heading' in attributes or 'jumping' in attributes):
                def_aerial_rating = (
                    attributes.get('heading', 0.5) * 0.3 +
                    attributes.get('jumping', 0.5) * 0.3 +
                    attributes.get('height', 0.5) * 0.2 +
                    attributes.get('defensive_positioning', 0.5) * 0.2
                )
                if def_aerial_rating > 0.7:
                    defensive_aerial_specialists.append({
                        'id': player.get('id', ''),
                        'name': player.get('name', ''),
                        'position': position,
                        'rating': def_aerial_rating
                    })
            
            # Évaluer les capacités du gardien sur coups de pied arrêtés
            if position == 'GK':
                gk_rating = (
                    attributes.get('commanding_area', 0.5) * 0.4 +
                    attributes.get('aerial_ability', 0.5) * 0.4 +
                    attributes.get('reflexes', 0.5) * 0.1 +
                    attributes.get('positioning', 0.5) * 0.1
                )
                gk_set_piece_specialists.append({
                    'id': player.get('id', ''),
                    'name': player.get('name', ''),
                    'position': 'GK',
                    'rating': gk_rating
                })
        
        # Trier chaque liste par score
        defensive_aerial_specialists.sort(key=lambda x: x['rating'], reverse=True)
        gk_set_piece_specialists.sort(key=lambda x: x['rating'], reverse=True)
        
        return {
            'offensive': {
                'corner_specialists': corner_specialists,
                'free_kick_specialists': free_kick_specialists,
                'penalty_specialists': penalty_specialists,
                'aerial_specialists': aerial_specialists
            },
            'defensive': {
                'aerial_defenders': defensive_aerial_specialists,
                'goalkeepers': gk_set_piece_specialists
            }
        }
    
    def _analyze_threat_zones(self, team_data, specialists):
        """Analyser les zones de menace sur coups de pied arrêtés."""
        # Zones de menace offensive
        offensive_threat_zones = {
            'near_post': 0.0,
            'far_post': 0.0,
            'central': 0.0,
            'edge_of_box': 0.0
        }
        
        # Évaluer la menace par zone basée sur les spécialistes
        aerial_specialists = specialists['offensive']['aerial_specialists']
        tall_players = [s for s in aerial_specialists if s.get('rating', 0) > 0.75]
        
        corner_takers = specialists['offensive']['corner_specialists']
        if corner_takers:
            # Qualité de centre/frappe
            delivery_quality = corner_takers[0]['rating'] if corner_takers else 0.5
            
            # Ajuster les zones de menace selon la qualité de livraison et les spécialistes aériens
            if tall_players:
                offensive_threat_zones['far_post'] = (delivery_quality * 0.6) + (tall_players[0]['rating'] * 0.4)
                offensive_threat_zones['near_post'] = (delivery_quality * 0.7) + (tall_players[0]['rating'] * 0.3)
            
            # Central et edge of box
            tactical_quality = team_data.get('tactical_quality', 0.5)
            set_piece_innovation = team_data.get('set_piece_innovation', 0.5)
            
            offensive_threat_zones['central'] = (delivery_quality * 0.5) + (tactical_quality * 0.3) + (len(tall_players) * 0.1)
            offensive_threat_zones['edge_of_box'] = (set_piece_innovation * 0.7) + (tactical_quality * 0.3)
        
        # Normaliser les zones
        total_threat = sum(offensive_threat_zones.values())
        if total_threat > 0:
            for zone in offensive_threat_zones:
                offensive_threat_zones[zone] /= total_threat
        
        # Zones de vulnérabilité défensive
        defensive_vulnerability_zones = {
            'near_post': 0.0,
            'far_post': 0.0,
            'central': 0.0,
            'edge_of_box': 0.0
        }
        
        # Évaluer la vulnérabilité par zone
        defensive_aerial = specialists['defensive']['aerial_defenders']
        goalkeeper = specialists['defensive']['goalkeepers'][0] if specialists['defensive']['goalkeepers'] else None
        
        # Vulnérabilité au premier poteau
        if goalkeeper:
            near_post_defense = (goalkeeper['rating'] * 0.6)
            if defensive_aerial:
                near_post_defense += (defensive_aerial[0]['rating'] * 0.4)
            defensive_vulnerability_zones['near_post'] = 1 - near_post_defense
        
        # Vulnérabilité au second poteau
        far_post_defense = 0.0
        far_post_defenders = [d for d in defensive_aerial if d['position'] in ['CB']]
        if far_post_defenders:
            far_post_defense = sum(d['rating'] for d in far_post_defenders[:2]) / len(far_post_defenders[:2])
        defensive_vulnerability_zones['far_post'] = 1 - far_post_defense
        
        # Vulnérabilité centrale
        central_defense = 0.5  # Défense moyenne par défaut
        if defensive_aerial:
            central_defenders = [d for d in defensive_aerial if d['position'] in ['CB', 'DM']]
            if central_defenders:
                central_defense = sum(d['rating'] for d in central_defenders[:3]) / len(central_defenders[:3])
        defensive_vulnerability_zones['central'] = 1 - central_defense
        
        # Vulnérabilité à l'extérieur de la surface
        edge_defense = team_data.get('defensive_organization', 0.5)
        defensive_vulnerability_zones['edge_of_box'] = 1 - edge_defense
        
        # Normaliser les vulnérabilités
        total_vuln = sum(defensive_vulnerability_zones.values())
        if total_vuln > 0:
            for zone in defensive_vulnerability_zones:
                defensive_vulnerability_zones[zone] /= total_vuln
        
        return {
            'offensive': offensive_threat_zones,
            'defensive': defensive_vulnerability_zones
        }
    
    def _identify_notable_routines(self, team_data, match_history):
        """Identifier les routines notables sur coups de pied arrêtés."""
        notable_routines = []
        
        # Vérifier s'il y a des données historiques
        if not match_history:
            return notable_routines
        
        # Compteurs pour détecter les motifs
        corner_patterns = {}
        free_kick_patterns = {}
        
        # Analyser les matchs pour trouver des routines récurrentes
        for match in match_history:
            set_pieces = match.get('set_pieces', {})
            offensive_events = set_pieces.get('offensive_events', [])
            
            for event in offensive_events:
                event_type = event.get('type', '')
                pattern_key = None
                
                if event_type == 'corner':
                    delivery = event.get('delivery_type', 'unknown')
                    target_zone = event.get('zone_targeted', 'unknown')
                    player_movement = event.get('player_movement', 'unknown')
                    
                    pattern_key = f"{delivery}_{target_zone}_{player_movement}"
                    if pattern_key in corner_patterns:
                        corner_patterns[pattern_key]['count'] += 1
                        if event.get('result', '') == 'goal':
                            corner_patterns[pattern_key]['goals'] += 1
                    else:
                        corner_patterns[pattern_key] = {
                            'count': 1,
                            'goals': 1 if event.get('result', '') == 'goal' else 0,
                            'delivery': delivery,
                            'target_zone': target_zone,
                            'player_movement': player_movement
                        }
                
                elif event_type == 'free_kick':
                    direct = event.get('direct', False)
                    technique = event.get('technique', 'unknown')
                    players_involved = len(event.get('players_involved', []))
                    
                    pattern_key = f"{'direct' if direct else 'indirect'}_{technique}_{players_involved}"
                    if pattern_key in free_kick_patterns:
                        free_kick_patterns[pattern_key]['count'] += 1
                        if event.get('result', '') == 'goal':
                            free_kick_patterns[pattern_key]['goals'] += 1
                    else:
                        free_kick_patterns[pattern_key] = {
                            'count': 1,
                            'goals': 1 if event.get('result', '') == 'goal' else 0,
                            'direct': direct,
                            'technique': technique,
                            'players_involved': players_involved
                        }
        
        # Identifier les coins notables (plus fréquents ou efficaces)
        for pattern_key, data in corner_patterns.items():
            if data['count'] >= 3 or data['goals'] >= 2:
                conversion_rate = data['goals'] / data['count'] if data['count'] > 0 else 0
                
                # Si le taux de conversion est significativement supérieur à la moyenne
                if conversion_rate > self.set_piece_types['corner']['avg_conversion'] * 1.5 or data['goals'] >= 2:
                    notable_routines.append({
                        'type': 'corner',
                        'name': f"Corner {'in' if data['delivery'] == 'inswinger' else 'out'}swinging {data['target_zone']}",
                        'description': f"Corner {'in' if data['delivery'] == 'inswinger' else 'out'}swinging vers {data['target_zone']} avec {data['player_movement']}",
                        'frequency': data['count'],
                        'goals': data['goals'],
                        'conversion_rate': conversion_rate,
                        'vs_average': conversion_rate / self.set_piece_types['corner']['avg_conversion'] if conversion_rate > 0 else 0
                    })
        
        # Identifier les coups francs notables
        for pattern_key, data in free_kick_patterns.items():
            if data['count'] >= 2 or data['goals'] >= 1:
                conversion_rate = data['goals'] / data['count'] if data['count'] > 0 else 0
                
                # Type de coup franc
                fk_type = 'free_kick_direct' if data['direct'] else 'free_kick_indirect'
                
                # Si le taux de conversion est significativement supérieur à la moyenne
                if conversion_rate > self.set_piece_types[fk_type]['avg_conversion'] * 1.5 or data['goals'] >= 1:
                    notable_routines.append({
                        'type': 'free_kick',
                        'name': f"{'Direct' if data['direct'] else 'Indirect'} free kick {data['technique']}",
                        'description': f"{'Coup franc direct' if data['direct'] else 'Coup franc indirect'} utilisant {data['technique']} avec {data['players_involved']} joueurs impliqués",
                        'frequency': data['count'],
                        'goals': data['goals'],
                        'conversion_rate': conversion_rate,
                        'vs_average': conversion_rate / self.set_piece_types[fk_type]['avg_conversion'] if conversion_rate > 0 else 0
                    })
        
        # Trier par efficacité
        notable_routines.sort(key=lambda x: x['conversion_rate'], reverse=True)
        
        return notable_routines
    
    def _identify_vulnerabilities(self, team_data, defensive_rating, historical_performance=None):
        """Identifier les vulnérabilités sur coups de pied arrêtés."""
        vulnerabilities = []
        
        # Analyser les scores défensifs pour identifier les faiblesses
        factor_scores = defensive_rating['breakdown']
        
        for factor, score in factor_scores.items():
            if score < 0.5:
                vulnerability = {
                    'factor': factor,
                    'score': score,
                    'severity': 'high' if score < 0.4 else 'medium',
                    'description': self._get_vulnerability_description(factor, score)
                }
                vulnerabilities.append(vulnerability)
        
        # Analyser les données historiques si disponibles
        if historical_performance:
            defensive_stats = historical_performance['defensive']
            
            # Vérifier les taux de concession élevés
            for set_piece_type, stats in defensive_stats.items():
                if stats['vs_average'] > 1.2 and stats['count'] >= 3:
                    vulnerabilities.append({
                        'factor': f"{set_piece_type}_concession",
                        'score': stats['concession_rate'],
                        'severity': 'high' if stats['vs_average'] > 1.5 else 'medium',
                        'description': f"Taux de concession élevé sur {self._translate_set_piece_type(set_piece_type)} ({stats['concession_rate']:.1%}, {stats['vs_average']:.1f}x la moyenne)",
                        'data_points': stats['count']
                    })
        
        # Identifier les modèles de vulnérabilité potentiels
        squad = team_data.get('squad', [])
        
        # Vérifier la faiblesse au premier poteau
        goalkeeper = None
        for player in squad:
            if player.get('position', '') == 'GK':
                goalkeeper = player
                break
        
        if goalkeeper and 'attributes' in goalkeeper:
            near_post_command = goalkeeper['attributes'].get('commanding_area', 0.5)
            if near_post_command < 0.5:
                vulnerabilities.append({
                    'factor': 'near_post_weakness',
                    'score': near_post_command,
                    'severity': 'high' if near_post_command < 0.4 else 'medium',
                    'description': f"Faiblesse potentielle au premier poteau due à une autorité limitée du gardien sur sa surface",
                    'pattern': self.vulnerability_patterns['near_post_weakness']
                })
        
        # Vérifier le manque de taille défensive
        tall_defenders = 0
        for player in squad:
            if player.get('position', '') in ['CB', 'GK'] and player.get('attributes', {}).get('height', 0.5) > 0.7:
                tall_defenders += 1
        
        if tall_defenders < 3:
            vulnerabilities.append({
                'factor': 'aerial_weakness',
                'score': 0.4,
                'severity': 'medium',
                'description': f"Manque potentiel de taille défensive avec seulement {tall_defenders} grands défenseurs",
                'pattern': {
                    'description': 'Manque de taille défensive',
                    'detection_threshold': 0.6,
                    'exploit_difficulty': 0.6
                }
            })
        
        # Vérifier les problèmes d'organisation
        if factor_scores.get('organization', 0.5) < 0.45 and factor_scores.get('concentration', 0.5) < 0.5:
            vulnerabilities.append({
                'factor': 'poor_defensive_coordination',
                'score': (factor_scores.get('organization', 0.5) + factor_scores.get('concentration', 0.5)) / 2,
                'severity': 'high',
                'description': "Manque de coordination défensive, combinant des problèmes d'organisation et de concentration",
                'pattern': self.vulnerability_patterns['poor_defensive_coordination']
            })
        
        # Limiter aux 3 vulnérabilités les plus critiques
        vulnerabilities.sort(key=lambda x: x['score'])
        return vulnerabilities[:3]
    
    def _get_vulnerability_description(self, factor, score):
        """Obtenir une description textuelle d'une vulnérabilité."""
        if factor == 'aerial_defense':
            return "Faiblesse dans les duels aériens défensifs"
        elif factor == 'organization':
            return "Manque d'organisation défensive sur les phases arrêtées"
        elif factor == 'concentration':
            return "Manque de concentration dans les moments clés"
        elif factor == 'goalkeeper_command':
            return "Autorité limitée du gardien sur sa surface"
        elif factor == 'man_marking':
            return "Déficiences dans le marquage individuel"
        else:
            return f"Faiblesse identifiée dans {factor} (score: {score:.2f})"
    
    def _translate_set_piece_type(self, set_piece_type):
        """Traduire le type de coup de pied arrêté en description lisible."""
        translations = {
            'corners': 'corners',
            'direct_free_kicks': 'coups francs directs',
            'indirect_free_kicks': 'coups francs indirects',
            'penalties': 'penalties'
        }
        return translations.get(set_piece_type, set_piece_type)
    
    def _calculate_expected_set_piece_goals(self, advantage):
        """Calculer le nombre attendu de buts sur coups de pied arrêtés."""
        # Base: ~0.3 buts par match sur coups de pied arrêtés (hors penalties)
        base_rate = 0.3
        
        # Ajuster selon l'avantage relatif (différence entre attaque et défense)
        adjusted_rate = base_rate * (1 + advantage)
        
        # Limiter à des valeurs raisonnables
        return max(0.05, min(1.0, adjusted_rate))
    
    def _identify_key_set_piece_matchups(self, team_data, opponent_data):
        """Identifier les confrontations clés sur coups de pied arrêtés."""
        key_matchups = []
        
        # Extraire les spécialistes des deux équipes
        team_specialists = self._identify_specialists(team_data.get('squad', []))
        opponent_specialists = self._identify_specialists(opponent_data.get('squad', []))
        
        # Identifier les confrontations offensives
        team_aerial = team_specialists['offensive']['aerial_specialists']
        opponent_defensive_aerial = opponent_specialists['defensive']['aerial_defenders']
        
        # Confrontations aériennes
        if team_aerial and opponent_defensive_aerial:
            # Trouver les meilleurs attaquants aériens
            for aerial_attacker in team_aerial[:2]:
                best_defender = None
                for defender in opponent_defensive_aerial:
                    if not best_defender or defender['rating'] > best_defender['rating']:
                        best_defender = defender
                
                if best_defender:
                    advantage = aerial_attacker['rating'] - best_defender['rating']
                    key_matchups.append({
                        'type': 'aerial',
                        'team_player': aerial_attacker['name'],
                        'opponent_player': best_defender['name'],
                        'advantage': advantage,
                        'description': f"Duel aérien entre {aerial_attacker['name']} et {best_defender['name']}",
                        'advantage_team': 'team' if advantage > 0 else 'opponent'
                    })
        
        # Confrontation tireur de coup franc vs mur/gardien
        team_fk = team_specialists['offensive']['free_kick_specialists']
        opponent_gk = opponent_specialists['defensive']['goalkeepers']
        
        if team_fk and opponent_gk:
            best_fk = team_fk[0]
            gk = opponent_gk[0]
            
            advantage = best_fk['rating'] - gk['rating']
            key_matchups.append({
                'type': 'free_kick',
                'team_player': best_fk['name'],
                'opponent_player': gk['name'],
                'advantage': advantage,
                'description': f"Coup franc de {best_fk['name']} face à {gk['name']}",
                'advantage_team': 'team' if advantage > 0 else 'opponent'
            })
        
        # Confrontation corner vs défense au premier poteau
        team_corner = team_specialists['offensive']['corner_specialists']
        
        if team_corner and opponent_gk:
            best_corner = team_corner[0]
            advantage = best_corner['rating'] - (opponent_gk[0]['rating'] * 0.7)
            key_matchups.append({
                'type': 'corner_delivery',
                'team_player': best_corner['name'],
                'opponent_player': opponent_gk[0]['name'],
                'advantage': advantage,
                'description': f"Centres de {best_corner['name']} vs. autorité de {opponent_gk[0]['name']}",
                'advantage_team': 'team' if advantage > 0 else 'opponent'
            })
        
        # Tri par avantage absolu
        key_matchups.sort(key=lambda x: abs(x['advantage']), reverse=True)
        
        return key_matchups
    
    def _generate_set_piece_recommendations(self, team_data, opponent_data, team_profile, opponent_profile):
        """Générer des recommandations tactiques pour les coups de pied arrêtés."""
        recommendations = []
        
        # Extraire les forces et faiblesses
        team_offensive = team_profile.get('offensive_rating', 0.5)
        team_defensive = team_profile.get('defensive_rating', 0.5)
        opponent_offensive = opponent_profile.get('offensive_rating', 0.5)
        opponent_defensive = opponent_profile.get('defensive_rating', 0.5)
        
        # Évaluer les spécialistes
        team_specialists = self._identify_specialists(team_data.get('squad', []))
        opponent_specialists = self._identify_specialists(opponent_data.get('squad', []))
        
        # Recommandations offensives
        if team_offensive > opponent_defensive + 0.15:
            # Avantage offensif significatif
            recommendations.append({
                'type': 'offensive',
                'description': "Maximiser les occasions de coups de pied arrêtés - avantage offensif significatif",
                'priority': 'high',
                'specific_actions': [
                    "Chercher à obtenir des corners et coups francs dans le dernier tiers",
                    "Utiliser les schémas les plus efficaces sans retenue"
                ]
            })
        
        # Recommandations défensives
        if opponent_offensive > team_defensive + 0.15:
            # Désavantage défensif significatif
            recommendations.append({
                'type': 'defensive',
                'description': "Renforcer la vigilance défensive sur coups de pied arrêtés - vulnérabilité significative",
                'priority': 'high',
                'specific_actions': [
                    "Éviter les fautes non nécessaires dans le dernier tiers",
                    "Renforcer le marquage sur les spécialistes adverses"
                ]
            })
        
        # Recommandations spécifiques basées sur les spécialistes
        team_aerial = team_specialists['offensive']['aerial_specialists']
        if team_aerial and len(team_aerial) >= 2 and team_aerial[0]['rating'] > 0.75:
            # Force aérienne significative
            recommendations.append({
                'type': 'targeting',
                'description': f"Exploiter la force aérienne en ciblant {team_aerial[0]['name']} et {team_aerial[1]['name']}",
                'priority': 'medium',
                'specific_actions': [
                    f"Centres précis vers {team_aerial[0]['name']} au second poteau",
                    "Utiliser des combinaisons pour créer de l'espace pour les cibles aériennes"
                ]
            })
        
        # Recommandation sur les zones vulnérables de l'adversaire
        opponent_gk = opponent_specialists['defensive']['goalkeepers']
        if opponent_gk and opponent_gk[0]['rating'] < 0.6:
            # Gardien adverse faible dans les airs
            recommendations.append({
                'type': 'exploitation',
                'description': f"Cibler le gardien adverse {opponent_gk[0]['name']} qui présente des faiblesses aériennes",
                'priority': 'high',
                'specific_actions': [
                    "Corners et coups francs dans la zone du gardien pour le mettre sous pression",
                    "Créer du trafic devant le gardien pour limiter sa capacité à sortir"
                ]
            })
        
        # Recommandation sur les routines spécifiques
        team_free_kick_specialists = team_specialists['offensive']['free_kick_specialists']
        if team_free_kick_specialists and team_free_kick_specialists[0]['rating'] > 0.8:
            # Excellent tireur de coups francs
            recommendations.append({
                'type': 'free_kicks',
                'description': f"Maximiser les opportunités de tir pour {team_free_kick_specialists[0]['name']}",
                'priority': 'medium',
                'specific_actions': [
                    f"Rechercher les fautes dans la zone de tir de {team_free_kick_specialists[0]['name']}",
                    "Utiliser des combinaisons pour créer des angles de tir favorables"
                ]
            })
        
        return recommendations
    
    def _generate_corner_strategy(self, team_data, specialists, opponent_data=None):
        """Générer une stratégie optimale pour les corners."""
        # Extraire les informations pertinentes
        offensive_specialists = specialists['offensive']
        corner_takers = offensive_specialists['corner_specialists']
        aerial_threats = offensive_specialists['aerial_specialists']
        
        # Déterminer les tireurs de corner
        recommended_takers = []
        if corner_takers:
            for taker in corner_takers[:2]:
                recommended_takers.append({
                    'name': taker['name'],
                    'side': 'both' if taker['rating'] > 0.8 else ('right' if taker['position'] in ['LM', 'LW', 'LB'] else 'left'),
                    'rating': taker['rating']
                })
        
        # Déterminer les cibles principales
        priority_targets = []
        if aerial_threats:
            for threat in aerial_threats[:3]:
                priority_targets.append({
                    'name': threat['name'],
                    'role': 'target',
                    'zone': 'far_post' if threat['rating'] > 0.8 else 'near_post'
                })
        
        # Déterminer les zones à cibler
        target_zones = []
        if aerial_threats and len(aerial_threats) >= 2:
            # Si bonnes menaces aériennes, privilégier les zones centrales et second poteau
            target_zones = [
                {'zone': 'far_post', 'priority': 'high'},
                {'zone': 'central', 'priority': 'medium'},
                {'zone': 'near_post', 'priority': 'low'}
            ]
        else:
            # Sinon, mixer les approches
            target_zones = [
                {'zone': 'near_post', 'priority': 'high'},
                {'zone': 'edge_of_box', 'priority': 'medium'},
                {'zone': 'far_post', 'priority': 'low'}
            ]
        
        # Déterminer les routines recommandées
        recommended_routines = []
        
        # Routine 1: Classique
        recommended_routines.append({
            'name': 'Classique',
            'description': 'Centre vers le point de penalty avec 3-4 attaquants dans la surface',
            'complexity': 'low',
            'suitability': 'high'
        })
        
        # Routine 2: Blocage
        if aerial_threats and len(aerial_threats) >= 3:
            recommended_routines.append({
                'name': 'Blocage pour cible principale',
                'description': f"Blocage pour libérer {aerial_threats[0]['name']} au second poteau",
                'complexity': 'medium',
                'suitability': 'high'
            })
        
        # Routine 3: Corner court
        if corner_takers and corner_takers[0]['rating'] > 0.75:
            recommended_routines.append({
                'name': 'Corner court',
                'description': 'Combinaison courte suivie d\'un centre ou d\'une frappe',
                'complexity': 'medium',
                'suitability': 'medium'
            })
        
        # Adapter selon l'adversaire si disponible
        if opponent_data:
            opponent_specialists = self._identify_specialists(opponent_data.get('squad', []))
            opponent_gk = opponent_specialists['defensive']['goalkeepers'][0] if opponent_specialists['defensive']['goalkeepers'] else None
            
            if opponent_gk:
                if opponent_gk['rating'] < 0.6:
                    # Gardien faible - cibler sa zone
                    target_zones.insert(0, {'zone': 'goalkeeper_area', 'priority': 'very_high'})
                    recommended_routines.insert(0, {
                        'name': 'Pression sur le gardien',
                        'description': f"Centre en cloche dans la zone du gardien {opponent_gk['name']} pour le mettre sous pression",
                        'complexity': 'low',
                        'suitability': 'very_high'
                    })
        
        return {
            'recommended_takers': recommended_takers,
            'priority_targets': priority_targets,
            'target_zones': target_zones,
            'recommended_routines': recommended_routines
        }
    
    def _generate_direct_free_kick_strategy(self, team_data, specialists, opponent_data=None):
        """Générer une stratégie optimale pour les coups francs directs."""
        # Extraire les informations pertinentes
        offensive_specialists = specialists['offensive']
        free_kick_takers = offensive_specialists['free_kick_specialists']
        
        # Déterminer les tireurs de coups francs
        recommended_takers = []
        if free_kick_takers:
            for taker in free_kick_takers[:2]:
                recommended_takers.append({
                    'name': taker['name'],
                    'side': 'both' if taker['rating'] > 0.8 else ('right' if taker['position'] in ['LM', 'LW', 'LB'] else 'left'),
                    'distance': 'medium' if taker['rating'] > 0.8 else 'close',
                    'technique': 'curl' if taker['rating'] > 0.75 else 'power',
                    'rating': taker['rating']
                })
        
        # Déterminer les techniques recommandées par distance
        technique_by_distance = {
            'close': [],
            'medium': [],
            'long': []
        }
        
        if free_kick_takers:
            best_taker = free_kick_takers[0]
            
            # Techniques à courte distance
            technique_by_distance['close'] = [
                {'technique': 'curl', 'suitability': 'high' if best_taker['rating'] > 0.7 else 'medium'},
                {'technique': 'power', 'suitability': 'medium'}
            ]
            
            # Techniques à moyenne distance
            technique_by_distance['medium'] = [
                {'technique': 'curl', 'suitability': 'high' if best_taker['rating'] > 0.8 else 'medium'},
                {'technique': 'dipping', 'suitability': 'medium' if best_taker['rating'] > 0.75 else 'low'}
            ]
            
            # Techniques à longue distance
            technique_by_distance['long'] = [
                {'technique': 'knuckleball', 'suitability': 'medium' if best_taker['rating'] > 0.85 else 'low'},
                {'technique': 'crossed', 'suitability': 'high'}
            ]
        
        # Déterminer les zones cibles par côté
        target_zones = {
            'left_side': [
                {'zone': 'far_top_corner', 'priority': 'high'},
                {'zone': 'near_bottom_corner', 'priority': 'medium'}
            ],
            'right_side': [
                {'zone': 'far_top_corner', 'priority': 'high'},
                {'zone': 'near_bottom_corner', 'priority': 'medium'}
            ],
            'central': [
                {'zone': 'top_corner', 'priority': 'high'},
                {'zone': 'bottom_corner', 'priority': 'medium'}
            ]
        }
        
        # Adapter selon l'adversaire si disponible
        if opponent_data:
            opponent_specialists = self._identify_specialists(opponent_data.get('squad', []))
            opponent_gk = opponent_specialists['defensive']['goalkeepers'][0] if opponent_specialists['defensive']['goalkeepers'] else None
            
            if opponent_gk:
                gk_rating = opponent_gk['rating']
                gk_weakness = 'height' if opponent_gk.get('attributes', {}).get('height', 0.5) < 0.7 else (
                    'agility' if opponent_gk.get('attributes', {}).get('agility', 0.5) < 0.7 else None
                )
                
                if gk_weakness == 'height':
                    # Gardien petit - cibler les angles supérieurs
                    for side in target_zones:
                        for zone in target_zones[side]:
                            if 'top' in zone['zone']:
                                zone['priority'] = 'very_high'
                elif gk_weakness == 'agility':
                    # Gardien peu agile - varier les techniques
                    for distance in technique_by_distance:
                        technique_by_distance[distance].append({
                            'technique': 'unpredictable', 
                            'suitability': 'high'
                        })
        
        return {
            'recommended_takers': recommended_takers,
            'technique_by_distance': technique_by_distance,
            'target_zones': target_zones
        }
    
    def _generate_indirect_free_kick_strategy(self, team_data, specialists, opponent_data=None):
        """Générer une stratégie optimale pour les coups francs indirects."""
        # Extraire les informations pertinentes
        offensive_specialists = specialists['offensive']
        free_kick_takers = offensive_specialists['free_kick_specialists']
        aerial_threats = offensive_specialists['aerial_specialists']
        
        # Stratégie similaire aux corners mais adaptée
        recommended_takers = []
        if free_kick_takers:
            for taker in free_kick_takers[:2]:
                recommended_takers.append({
                    'name': taker['name'],
                    'position': taker['position'],
                    'rating': taker['rating']
                })
        
        # Déterminer les cibles principales
        priority_targets = []
        if aerial_threats:
            for threat in aerial_threats[:3]:
                priority_targets.append({
                    'name': threat['name'],
                    'role': 'target',
                    'zone': 'central' if threat['rating'] > 0.8 else 'near_post'
                })
        
        # Déterminer les routines recommandées
        recommended_routines = []
        
        # Routine 1: Centre classique
        recommended_routines.append({
            'name': 'Centre classique',
            'description': 'Centre direct vers le point de penalty avec course d\'appel',
            'complexity': 'low',
            'suitability': 'high'
        })
        
        # Routine 2: Combinaison
        recommended_routines.append({
            'name': 'Combinaison courte',
            'description': 'Passe courte puis centre en profondeur',
            'complexity': 'medium',
            'suitability': 'medium'
        })
        
        # Routine 3: Décalage
        if free_kick_takers and len(free_kick_takers) >= 2:
            recommended_routines.append({
                'name': 'Décalage pour tireur',
                'description': f"Décalage pour {free_kick_takers[0]['name']} ou {free_kick_takers[1]['name']}",
                'complexity': 'medium',
                'suitability': 'medium'
            })
        
        # Déterminer les zones à cibler
        target_zones = [
            {'zone': 'central', 'priority': 'high'},
            {'zone': 'far_post', 'priority': 'medium'},
            {'zone': 'near_post', 'priority': 'low'}
        ]
        
        # Adapter selon l'adversaire si disponible
        if opponent_data:
            opponent_specialists = self._identify_specialists(opponent_data.get('squad', []))
            opponent_defensive_aerial = opponent_specialists['defensive']['aerial_defenders']
            
            if opponent_defensive_aerial and len(opponent_defensive_aerial) < 3:
                # Adversaire faible dans les airs - privilégier les centres
                target_zones[0]['priority'] = 'very_high'
                recommended_routines.insert(0, {
                    'name': 'Surcharge aérienne',
                    'description': 'Concentrer les cibles aériennes dans la surface pour dominer en l\'air',
                    'complexity': 'low',
                    'suitability': 'very_high'
                })
        
        return {
            'recommended_takers': recommended_takers,
            'priority_targets': priority_targets,
            'target_zones': target_zones,
            'recommended_routines': recommended_routines
        }
    
    def _generate_penalty_strategy(self, team_data, specialists):
        """Générer une stratégie optimale pour les penalties."""
        # Extraire les informations pertinentes
        offensive_specialists = specialists['offensive']
        penalty_takers = offensive_specialists['penalty_specialists']
        
        # Déterminer les tireurs de penalty
        recommended_takers = []
        if penalty_takers:
            for taker in penalty_takers[:3]:
                technique = 'placement'
                if taker['rating'] > 0.85:
                    technique = 'unpredictable'
                elif taker['rating'] > 0.75:
                    technique = 'power'
                
                recommended_takers.append({
                    'name': taker['name'],
                    'technique': technique,
                    'preferred_side': 'right' if random.random() > 0.5 else 'left',  # Simplifié
                    'rating': taker['rating']
                })
        
        # Recommandations générales
        recommendations = [
            {
                'description': 'Soyez imprévisible, variez les côtés et techniques',
                'priority': 'high'
            },
            {
                'description': 'Surveillez les tendances du gardien lors de l\'échauffement',
                'priority': 'medium'
            }
        ]
        
        # Ordre de priorité des tireurs
        taker_order = [taker['name'] for taker in recommended_takers]
        
        return {
            'recommended_takers': recommended_takers,
            'taker_order': taker_order,
            'recommendations': recommendations
        }
    
    def _generate_defensive_strategies(self, team_data, opponent_data=None):
        """Générer des stratégies défensives sur coups de pied arrêtés."""
        # Extraire les informations pertinentes
        squad = team_data.get('squad', [])
        gk = None
        for player in squad:
            if player.get('position', '') == 'GK':
                gk = player
                break
        
        # Stratégies défensives par type
        corners_strategy = {}
        free_kicks_strategy = {}
        penalties_strategy = {}
        
        # Stratégie sur corners
        marking_approach = 'mixed'  # Par défaut
        
        # Déterminer l'approche de marquage optimale
        aerial_defenders = []
        for player in squad:
            if player.get('position', '') in ['CB', 'LB', 'RB', 'DM'] and 'attributes' in player:
                aerial_rating = (
                    player['attributes'].get('jumping', 0.5) * 0.3 +
                    player['attributes'].get('heading', 0.5) * 0.3 +
                    player['attributes'].get('defensive_positioning', 0.5) * 0.2 +
                    player['attributes'].get('height', 0.5) * 0.2
                )
                if aerial_rating > 0.65:
                    aerial_defenders.append({
                        'id': player.get('id', ''),
                        'name': player.get('name', ''),
                        'position': player.get('position', ''),
                        'rating': aerial_rating
                    })
        
        # Trier et déterminer l'approche optimale
        aerial_defenders.sort(key=lambda x: x['rating'], reverse=True)
        
        if len(aerial_defenders) >= 4 and aerial_defenders[0]['rating'] > 0.8:
            marking_approach = 'zonal'  # Bons défenseurs = marquage de zone
        elif len(aerial_defenders) < 3:
            marking_approach = 'man_to_man'  # Peu de bons défenseurs = marquage individuel
        
        # Configuration défensive sur corners
        corners_strategy = {
            'marking_approach': marking_approach,
            'key_defenders': [d['name'] for d in aerial_defenders[:3]],
            'posts_coverage': 'near_post' if gk and gk.get('attributes', {}).get('commanding_area', 0.5) > 0.7 else 'both_posts',
            'recommended_setup': {
                'zonal_structure': '5+3+2' if marking_approach == 'zonal' else '4+4+2',
                'player_positioning': [
                    {'position': 'near_post', 'player_type': 'quick_defender'},
                    {'position': 'six_yard_line', 'player_type': 'tall_defenders'},
                    {'position': 'edge_of_box', 'player_type': 'technical_midfielder'}
                ]
            }
        }
        
        # Configuration défensive sur coups francs
        free_kicks_strategy = {
            'wall_setup': {
                'size': 4,
                'positioning': 'standard',
                'jumpers': True
            },
            'marking_approach': 'man_to_man',
            'offside_trap': team_data.get('defensive_discipline', 0.5) > 0.7
        }
        
        # Configuration défensive sur penalties
        penalties_strategy = {
            'goalkeeper_approach': 'read_and_react' if gk and gk.get('attributes', {}).get('reflexes', 0.5) > 0.75 else 'commit_early',
            'psychological_tactics': 'minimal' if team_data.get('sportsmanship', 0.7) > 0.8 else 'moderate'
        }
        
        # Adapter selon l'adversaire si disponible
        if opponent_data:
            opponent_specialists = self._identify_specialists(opponent_data.get('squad', []))
            opponent_aerial = opponent_specialists['offensive']['aerial_specialists']
            opponent_fk = opponent_specialists['offensive']['free_kick_specialists']
            
            if opponent_aerial and len(opponent_aerial) >= 3:
                # Adversaire fort dans les airs
                corners_strategy['key_threats'] = [o['name'] for o in opponent_aerial[:2]]
                corners_strategy['special_attention'] = "Attention particulière aux menaces aériennes adverses"
                
                if marking_approach == 'mixed':
                    corners_strategy['marking_approach'] = 'man_to_man'  # Privilégier le marquage individuel contre les équipes fortes dans les airs
            
            if opponent_fk and opponent_fk[0]['rating'] > 0.8:
                # Excellent tireur adverse
                free_kicks_strategy['wall_setup']['size'] = 5
                free_kicks_strategy['special_attention'] = f"Attention particulière à {opponent_fk[0]['name']} sur coups francs"
        
        return {
            'corners': corners_strategy,
            'free_kicks': free_kicks_strategy,
            'penalties': penalties_strategy
        }
    
    def _evaluate_set_piece_execution(self, event_data, set_piece_taker, team_data):
        """Évaluer la qualité d'exécution d'un coup de pied arrêté."""
        event_type = event_data.get('type', 'corner')
        delivery_quality = 0.5  # Qualité moyenne par défaut
        
        # Évaluer selon le type
        if event_type == 'corner':
            # Qualité de centre
            delivery_type = event_data.get('delivery_type', 'inswinger')
            target_zone = event_data.get('zone_targeted', 'near_post')
            
            # Base: qualité du tireur
            if 'attributes' in set_piece_taker:
                delivery_quality = (
                    set_piece_taker['attributes'].get('crossing', 0.5) * 0.7 +
                    set_piece_taker['attributes'].get('technique', 0.5) * 0.3
                )
            
            # Ajuster selon la difficulté du centre
            if delivery_type == 'inswinger' and target_zone == 'far_post':
                delivery_quality *= 0.9  # Plus difficile
            elif delivery_type == 'outswinger' and target_zone == 'near_post':
                delivery_quality *= 0.9  # Plus difficile
            
            # Ajuster selon la position des joueurs
            player_positioning = event_data.get('player_positioning', 0.5)
            delivery_quality = (delivery_quality * 0.7) + (player_positioning * 0.3)
        
        elif event_type == 'free_kick_direct':
            # Qualité de frappe
            technique = event_data.get('technique', 'curl')
            distance = event_data.get('distance', 'medium')
            
            # Base: qualité du tireur
            if 'attributes' in set_piece_taker:
                delivery_quality = (
                    set_piece_taker['attributes'].get('free_kick', set_piece_taker['attributes'].get('shooting', 0.5)) * 0.6 +
                    set_piece_taker['attributes'].get('technique', 0.5) * 0.2 +
                    set_piece_taker['attributes'].get('composure', 0.5) * 0.2
                )
            
            # Ajuster selon la difficulté
            if distance == 'long':
                delivery_quality *= 0.85  # Plus difficile
            elif distance == 'close' and technique == 'power':
                delivery_quality *= 0.9  # Moins adapté
        
        elif event_type == 'free_kick_indirect':
            # Similaire aux corners
            delivery_type = event_data.get('delivery_type', 'lofted')
            
            # Base: qualité du tireur
            if 'attributes' in set_piece_taker:
                delivery_quality = (
                    set_piece_taker['attributes'].get('passing', 0.5) * 0.5 +
                    set_piece_taker['attributes'].get('technique', 0.5) * 0.3 +
                    set_piece_taker['attributes'].get('vision', 0.5) * 0.2
                )
            
            # Ajuster selon la complexité
            routine_complexity = event_data.get('routine_complexity', 0.5)
            if routine_complexity > 0.7:
                delivery_quality = (delivery_quality * 0.7) + (routine_complexity * 0.1)
            
            # Ajuster selon la coordination
            coordination = event_data.get('coordination', 0.5)
            delivery_quality = (delivery_quality * 0.8) + (coordination * 0.2)
        
        elif event_type == 'penalty':
            # Qualité de penalty
            technique = event_data.get('technique', 'placement')
            
            # Base: qualité du tireur
            if 'attributes' in set_piece_taker:
                delivery_quality = (
                    set_piece_taker['attributes'].get('penalty', 0.5) * 0.5 +
                    set_piece_taker['attributes'].get('composure', 0.5) * 0.3 +
                    set_piece_taker['attributes'].get('technique', 0.5) * 0.2
                )
            
            # Ajuster selon la technique
            if technique == 'power':
                delivery_quality = (delivery_quality * 0.9) + 0.05  # Plus risqué
            elif technique == 'panenka':
                delivery_quality = (delivery_quality * 0.8) + 0.1  # Très risqué mais gros impact
        
        # Limiter à des valeurs raisonnables
        delivery_quality = max(0.1, min(1.0, delivery_quality))
        
        # Classifier la qualité
        quality_category = 'average'
        if delivery_quality > 0.8:
            quality_category = 'excellent'
        elif delivery_quality > 0.65:
            quality_category = 'good'
        elif delivery_quality < 0.4:
            quality_category = 'poor'
        
        return {
            'score': delivery_quality,
            'category': quality_category,
            'type': event_type,
            'execution_details': {
                'taker': set_piece_taker.get('name', 'Unknown'),
                'technique': event_data.get('technique', ''),
                'target_zone': event_data.get('zone_targeted', '')
            }
        }
    
    def _evaluate_set_piece_defense(self, event_data, defensive_setup, opponent_data):
        """Évaluer la qualité de la défense sur un coup de pied arrêté."""
        event_type = event_data.get('type', 'corner')
        defense_quality = 0.5  # Qualité moyenne par défaut
        
        # Évaluer selon le type
        if event_type == 'corner':
            # Organisation défensive
            marking_type = defensive_setup.get('marking_type', 'zonal')
            organization = defensive_setup.get('organization', 0.5)
            
            # Base: qualité défensive
            defense_quality = organization
            
            # Ajuster selon le marquage et la coordination
            if marking_type == 'zonal':
                zone_integrity = defensive_setup.get('zone_integrity', 0.5)
                defense_quality = (defense_quality * 0.6) + (zone_integrity * 0.4)
            else:  # man_to_man ou mixed
                marking_tightness = defensive_setup.get('marking_tightness', 0.5)
                defense_quality = (defense_quality * 0.6) + (marking_tightness * 0.4)
            
            # Ajuster selon la position du gardien
            goalkeeper_positioning = defensive_setup.get('goalkeeper_positioning', 0.5)
            defense_quality = (defense_quality * 0.7) + (goalkeeper_positioning * 0.3)
        
        elif event_type == 'free_kick_direct':
            # Organisation du mur et du gardien
            wall_positioning = defensive_setup.get('wall_positioning', 0.5)
            goalkeeper_positioning = defensive_setup.get('goalkeeper_positioning', 0.5)
            
            # Base: positionnement du mur
            defense_quality = wall_positioning
            
            # Ajuster selon le gardien
            defense_quality = (defense_quality * 0.5) + (goalkeeper_positioning * 0.5)
            
            # Ajuster selon la distance
            distance = event_data.get('distance', 'medium')
            if distance == 'close':
                defense_quality *= 0.9  # Plus difficile à défendre
        
        elif event_type == 'free_kick_indirect':
            # Organisation défensive
            marking_type = defensive_setup.get('marking_type', 'man_to_man')
            organization = defensive_setup.get('organization', 0.5)
            
            # Base: qualité défensive
            defense_quality = organization
            
            # Ajuster selon le type de marquage
            if marking_type == 'zonal':
                zone_integrity = defensive_setup.get('zone_integrity', 0.5)
                defense_quality = (defense_quality * 0.6) + (zone_integrity * 0.4)
            else:  # man_to_man ou mixed
                marking_tightness = defensive_setup.get('marking_tightness', 0.5)
                defense_quality = (defense_quality * 0.6) + (marking_tightness * 0.4)
            
            # Ajuster selon les joueurs impliqués
            aerial_ability = defensive_setup.get('aerial_ability', 0.5)
            defense_quality = (defense_quality * 0.7) + (aerial_ability * 0.3)
        
        elif event_type == 'penalty':
            # Performance du gardien
            goalkeeper_technique = defensive_setup.get('goalkeeper_technique', 'read_and_react')
            goalkeeper_quality = defensive_setup.get('goalkeeper_quality', 0.5)
            
            # Base: qualité du gardien
            defense_quality = goalkeeper_quality
            
            # Ajuster selon la technique
            if goalkeeper_technique == 'commit_early':
                defense_quality = (defense_quality * 0.8) + 0.1  # Plus risqué mais peut déstabiliser
            
            # Ajuster selon la préparation
            preparation = defensive_setup.get('preparation', 0.5)
            defense_quality = (defense_quality * 0.8) + (preparation * 0.2)
        
        # Limiter à des valeurs raisonnables
        defense_quality = max(0.1, min(1.0, defense_quality))
        
        # Classifier la qualité
        quality_category = 'average'
        if defense_quality > 0.8:
            quality_category = 'excellent'
        elif defense_quality > 0.65:
            quality_category = 'good'
        elif defense_quality < 0.4:
            quality_category = 'poor'
        
        return {
            'score': defense_quality,
            'category': quality_category,
            'type': event_type,
            'defense_details': {
                'setup': defensive_setup.get('marking_type', ''),
                'key_defenders': defensive_setup.get('key_defenders', []),
                'organization_level': organization if 'organization' in locals() else 0.5
            }
        }
    
    def _identify_set_piece_key_factors(self, event_data, execution_quality, defense_quality):
        """Identifier les facteurs clés qui ont influencé le résultat d'un coup de pied arrêté."""
        result = event_data.get('result', 'no_goal')
        event_type = event_data.get('type', 'corner')
        
        key_factors = []
        
        # Facteur 1: Qualité d'exécution
        execution_factor = {
            'factor': 'execution_quality',
            'influence': 'positive' if execution_quality['score'] > 0.6 else ('negative' if execution_quality['score'] < 0.4 else 'neutral'),
            'description': f"Exécution {execution_quality['category']} du coup de pied arrêté"
        }
        key_factors.append(execution_factor)
        
        # Facteur 2: Qualité défensive
        defense_factor = {
            'factor': 'defense_quality',
            'influence': 'positive' if defense_quality['score'] > 0.6 else ('negative' if defense_quality['score'] < 0.4 else 'neutral'),
            'description': f"Défense {defense_quality['category']} sur le coup de pied arrêté"
        }
        key_factors.append(defense_factor)
        
        # Facteur 3: Facteurs spécifiques selon le type
        if event_type == 'corner':
            target_zone = event_data.get('zone_targeted', '')
            if 'zone_targeted' in event_data:
                zone_factor = {
                    'factor': 'targeted_zone',
                    'influence': 'neutral',
                    'description': f"Centre vers la zone {target_zone}"
                }
                
                # Déterminer l'influence selon le résultat
                if result == 'goal' and execution_quality['score'] > 0.6:
                    zone_factor['influence'] = 'positive'
                
                key_factors.append(zone_factor)
        
        elif event_type == 'free_kick_direct':
            technique = event_data.get('technique', '')
            if 'technique' in event_data:
                technique_factor = {
                    'factor': 'technique',
                    'influence': 'neutral',
                    'description': f"Utilisation de la technique '{technique}'"
                }
                
                # Déterminer l'influence selon le résultat
                if result == 'goal' and execution_quality['score'] > 0.6:
                    technique_factor['influence'] = 'positive'
                elif result == 'saved' and defense_quality['score'] > 0.6:
                    technique_factor['influence'] = 'negative'
                
                key_factors.append(technique_factor)
        
        elif event_type == 'penalty':
            placement = event_data.get('placement', '')
            if 'placement' in event_data:
                placement_factor = {
                    'factor': 'placement',
                    'influence': 'neutral',
                    'description': f"Penalty placé {placement}"
                }
                
                # Déterminer l'influence selon le résultat
                if result == 'goal':
                    placement_factor['influence'] = 'positive'
                elif result in ['saved', 'missed']:
                    placement_factor['influence'] = 'negative'
                
                key_factors.append(placement_factor)
        
        # Facteur 4: Évaluations supplémentaires basées sur le résultat
        if result == 'goal':
            # Cas de but: quel facteur a été décisif?
            if execution_quality['score'] > defense_quality['score'] + 0.2:
                key_factors.append({
                    'factor': 'decisive_quality',
                    'influence': 'positive',
                    'description': "Qualité d'exécution supérieure à la défense"
                })
            elif defense_quality['score'] < 0.4:
                key_factors.append({
                    'factor': 'defensive_error',
                    'influence': 'negative',
                    'description': "Erreur défensive significative"
                })
        elif result in ['saved', 'blocked', 'no_goal']:
            # Cas d'échec: quel facteur a été décisif?
            if defense_quality['score'] > execution_quality['score'] + 0.2:
                key_factors.append({
                    'factor': 'decisive_defense',
                    'influence': 'positive',
                    'description': "Qualité défensive supérieure à l'exécution"
                })
            elif execution_quality['score'] < 0.4:
                key_factors.append({
                    'factor': 'poor_execution',
                    'influence': 'negative',
                    'description': "Exécution significativement déficiente"
                })
        
        return key_factors
    
    def _evaluate_set_piece_match_impact(self, event_data, minute, result):
        """Évaluer l'impact de l'événement sur le match."""
        # Impact de base selon le résultat
        base_impact = 0.0
        if result == 'goal':
            base_impact = 0.8  # Impact élevé
        elif result in ['saved', 'blocked']:
            base_impact = 0.5  # Impact moyen
        elif result == 'missed':
            base_impact = 0.4  # Impact modéré
        else:
            base_impact = 0.2  # Impact faible
        
        # Ajuster selon le moment du match
        time_factor = 1.0
        if minute > 80:
            time_factor = 1.5  # Impact amplifié en fin de match
        elif minute > 70:
            time_factor = 1.3
        elif minute > 40 and minute <= 45:
            time_factor = 1.2  # Impact important juste avant la mi-temps
        
        # Ajuster selon le score avant l'événement
        score_state = event_data.get('score_state', 'tied')
        score_factor = 1.0
        
        if score_state == 'tied' and result == 'goal':
            score_factor = 1.3  # But qui débloque un match nul
        elif score_state == 'trailing_by_one' and result == 'goal':
            score_factor = 1.4  # But égalisateur
        elif score_state == 'tied' and minute > 80 and result == 'goal':
            score_factor = 1.5  # But décisif en fin de match
        
        # Calculer l'impact final
        match_impact = base_impact * time_factor * score_factor
        
        # Limiter à des valeurs raisonnables
        match_impact = min(1.0, match_impact)
        
        # Classifier l'impact
        impact_category = 'moderate'
        if match_impact > 0.8:
            impact_category = 'game_changing'
        elif match_impact > 0.6:
            impact_category = 'significant'
        elif match_impact < 0.3:
            impact_category = 'minimal'
        
        return {
            'impact_score': match_impact,
            'category': impact_category,
            'time_context': 'late_game' if minute > 75 else ('mid_game' if minute > 30 else 'early_game'),
            'score_context': score_state
        }
    
    def _categorize_rating(self, rating):
        """Classifier une note en catégorie."""
        if rating > 0.8:
            return 'excellent'
        elif rating > 0.7:
            return 'very_good'
        elif rating > 0.6:
            return 'good'
        elif rating > 0.45:
            return 'average'
        elif rating > 0.3:
            return 'below_average'
        else:
            return 'poor'