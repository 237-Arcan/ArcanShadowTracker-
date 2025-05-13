"""
CollapseDetector - Module de détection des risques d'effondrement d'une équipe.
Analyse les patterns de fragilité mentale et d'effondrements historiques.
"""

import random
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict

class CollapseDetector:
    """
    CollapseDetector - Système de détection des risques d'effondrement mental et de performance.
    Identifie les moments clés où une équipe est susceptible de s'effondrer pendant un match.
    """
    
    def __init__(self):
        """Initialise le module CollapseDetector"""
        self.collapse_patterns = {
            'after_conceding': {
                'description': 'Effondrement après avoir encaissé un but',
                'importance': 0.85,
                'time_window': 10,  # minutes
                'indicators': [
                    'but encaissé dans les 10 dernières minutes',
                    'domination adverse après le but',
                    'changements tactiques désordonnés'
                ]
            },
            'late_game_pressure': {
                'description': 'Effondrement sous pression en fin de match',
                'importance': 0.9,
                'time_window': 15,  # dernières minutes
                'indicators': [
                    'minute > 75',
                    'lead < 2 buts',
                    'domination adverse croissante',
                    'fatigue visible'
                ]
            },
            'momentum_shift': {
                'description': 'Effondrement suite à un changement de momentum',
                'importance': 0.8,
                'time_window': 15,  # minutes
                'indicators': [
                    'occasions manquées suivies par contre rapide',
                    'carton rouge ou pénalty controversé',
                    'changement tactique adverse efficace'
                ]
            },
            'key_player_impact': {
                'description': "Effondrement suite à la perte d'un joueur clé",
                'importance': 0.75,
                'time_window': 20,  # minutes
                'indicators': [
                    "blessure ou remplacement d'un joueur clé",
                    'désorganisation défensive après le changement',
                    'absence de leadership sur le terrain'
                ]
            }
        }
        
        # Historique des analyses
        self.analysis_history = []
        
        # Indicateurs psychologiques potentiels d'effondrement
        self.psychological_indicators = {
            'frustration_visible': 0.8,
            'communication_breakdown': 0.85,
            'body_language_negative': 0.7,
            'blame_shifting': 0.75,
            'tactical_confusion': 0.9,
            'excessive_complaints': 0.6,
            'time_wasting_desperate': 0.65,
            'defensive_disorganization': 0.95
        }
        
        # Facteurs historiques de résilience
        self.resilience_factors = {
            'strong_leadership': -0.8,  # Facteurs réduisant le risque
            'comeback_history': -0.7,
            'experienced_squad': -0.65,
            'tactical_flexibility': -0.75,
            'strong_bench_options': -0.6,
            'positive_momentum': -0.7,
            'good_fitness_levels': -0.65,
            'psychological_preparation': -0.8
        }
    
    def analyze_match_state(self, match_data, current_minute, team1_score, team2_score, recent_events=None):
        """
        Analyser l'état actuel du match et détecter les risques d'effondrement.
        
        Args:
            match_data (dict): Données du match
            current_minute (int): Minute actuelle du match
            team1_score (int): Score actuel de l'équipe 1
            team2_score (int): Score actuel de l'équipe 2
            recent_events (list, optional): Liste des événements récents du match
            
