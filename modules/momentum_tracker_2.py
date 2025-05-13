"""
MomentumTracker 2.0 - Module avancé de suivi et analyse des dynamiques de momentum.
Détecte, quantifie et modélise les changements de momentum avec une précision accrue.
"""

import numpy as np
import random
from datetime import datetime, timedelta
import json
import os
from collections import deque
import math

class MomentumTracker2:
    """
    MomentumTracker 2.0 - Version avancée du MomentumShiftTracker avec modélisation multidimensionnelle.
    Analyse les changements de momentum avec méthodologie améliorée et détection de patterns complexes.
    """
    
    def __init__(self):
        """Initialise le module MomentumTracker 2.0."""
        # Dimensions du momentum (extension significative par rapport à la v1)
        self.momentum_dimensions = {
            'psychological': {
                'weight': 0.25,
                'description': 'État mental et confiance des équipes',
                'decay_rate': 0.9,
                'volatility': 0.3,
                'transfer_rate': 0.4  # Transfert entre équipes
            },
            'tactical': {
                'weight': 0.2,
                'description': 'Avantage tactique et contrôle du jeu',
                'decay_rate': 0.95,
                'volatility': 0.2,
                'transfer_rate': 0.3
            },
            'physical': {
                'weight': 0.2,
                'description': 'Énergie physique et dominance athlétique',
                'decay_rate': 0.85,
                'volatility': 0.25,
                'transfer_rate': 0.3
            },
            'technical': {
                'weight': 0.15,
                'description': 'Qualité technique des actions',
                'decay_rate': 0.92,
                'volatility': 0.15,
                'transfer_rate': 0.2
            },
            'environmental': {
                'weight': 0.1,
                'description': 'Influence du public et facteurs externes',
                'decay_rate': 0.93,
                'volatility': 0.4,
                'transfer_rate': 0.5
            },
            'strategic': {
                'weight': 0.1,
                'description': 'Adaptations stratégiques et changements',
                'decay_rate': 0.97,
                'volatility': 0.2,
                'transfer_rate': 0.25
            }
        }
        
        # Modèles de momentum (patterns reconnaissables)
        self.momentum_patterns = {
            'crescendo': {
                'description': 'Augmentation progressive et soutenue',
                'recognition_threshold': 0.7,
                'detection_window': 10,  # minutes
                'significance': 0.8
            },
            'sudden_shift': {
                'description': 'Changement brusque et significatif',
                'recognition_threshold': 0.8,
                'detection_window': 5,
                'significance': 0.85
            },
            'oscillation': {
                'description': 'Alternance régulière entre équipes',
                'recognition_threshold': 0.75,
                'detection_window': 15,
                'significance': 0.7
            },
            'plateau': {
                'description': 'Stabilisation du momentum pour une équipe',
                'recognition_threshold': 0.65,
                'detection_window': 8,
                'significance': 0.6
            },
            'snowball': {
                'description': 'Effet boule de neige auto-renforçant',
                'recognition_threshold': 0.75,
                'detection_window': 12,
                'significance': 0.9
            },
            'resilient_response': {
                'description': 'Réponse après un momentum adverse',
                'recognition_threshold': 0.8,
                'detection_window': 7,
                'significance': 0.85
            }
        }
        
        # Types d'événements et leur impact sur le momentum (étendu)
        self.momentum_events = {
            # Événements standard
            'goal': {
                'base_impact': 0.5,
                'dimension_impacts': {
                    'psychological': 0.7,
                    'tactical': 0.3,
                    'physical': 0.1,
                    'technical': 0.2,
                    'environmental': 0.6,
                    'strategic': 0.2
                }
            },
            'shot_on_target': {
                'base_impact': 0.1,
                'dimension_impacts': {
                    'psychological': 0.15,
                    'tactical': 0.1,
                    'physical': 0.05,
                    'technical': 0.15,
                    'environmental': 0.1,
                    'strategic': 0.05
                }
            },
            'missed_chance': {
                'base_impact': -0.15,
                'dimension_impacts': {
                    'psychological': -0.25,
                    'tactical': -0.1,
                    'physical': 0.0,
                    'technical': -0.2,
                    'environmental': -0.15,
                    'strategic': -0.05
                }
            },
            'save': {
                'base_impact': 0.15,
                'dimension_impacts': {
                    'psychological': 0.2,
                    'tactical': 0.1,
                    'physical': 0.1,
                    'technical': 0.2,
                    'environmental': 0.15,
                    'strategic': 0.05
                }
            },
            'yellow_card': {
                'base_impact': -0.1,
                'dimension_impacts': {
                    'psychological': -0.15,
                    'tactical': -0.1,
                    'physical': -0.05,
                    'technical': 0.0,
                    'environmental': -0.05,
                    'strategic': -0.2
                }
            },
            'red_card': {
                'base_impact': -0.4,
                'dimension_impacts': {
                    'psychological': -0.5,
                    'tactical': -0.6,
                    'physical': -0.3,
                    'technical': -0.1,
                    'environmental': -0.3,
                    'strategic': -0.7
                }
            },
            'successful_dribble': {
                'base_impact': 0.08,
                'dimension_impacts': {
                    'psychological': 0.1,
                    'tactical': 0.05,
                    'physical': 0.1,
                    'technical': 0.2,
                    'environmental': 0.05,
                    'strategic': 0.0
                }
            },
            'tackle': {
                'base_impact': 0.05,
                'dimension_impacts': {
                    'psychological': 0.05,
                    'tactical': 0.05,
                    'physical': 0.15,
                    'technical': 0.1,
                    'environmental': 0.0,
                    'strategic': 0.0
                }
            },
            'interception': {
                'base_impact': 0.07,
                'dimension_impacts': {
                    'psychological': 0.05,
                    'tactical': 0.1,
                    'physical': 0.1,
                    'technical': 0.1,
                    'environmental': 0.0,
                    'strategic': 0.05
                }
            },
            'corner': {
                'base_impact': 0.05,
                'dimension_impacts': {
                    'psychological': 0.05,
                    'tactical': 0.1,
                    'physical': 0.0,
                    'technical': 0.0,
                    'environmental': 0.15,
                    'strategic': 0.05
                }
            },
            
            # Événements avancés supplémentaires dans la v2
            'key_pass': {
                'base_impact': 0.12,
                'dimension_impacts': {
                    'psychological': 0.1,
                    'tactical': 0.15,
                    'physical': 0.0,
                    'technical': 0.25,
                    'environmental': 0.05,
                    'strategic': 0.1
                }
            },
            'counter_attack': {
                'base_impact': 0.15,
                'dimension_impacts': {
                    'psychological': 0.15,
                    'tactical': 0.2,
                    'physical': 0.2,
                    'technical': 0.1,
                    'environmental': 0.1,
                    'strategic': 0.15
                }
            },
            'high_press_sequence': {
                'base_impact': 0.1,
                'dimension_impacts': {
                    'psychological': 0.1,
                    'tactical': 0.15,
                    'physical': 0.25,
                    'technical': 0.05,
                    'environmental': 0.05,
                    'strategic': 0.15
                }
            },
            'possession_sequence': {
                'base_impact': 0.08,
                'dimension_impacts': {
                    'psychological': 0.05,
                    'tactical': 0.15,
                    'physical': 0.05,
                    'technical': 0.15,
                    'environmental': 0.0,
                    'strategic': 0.1
                }
            },
            'tactical_substitution': {
                'base_impact': 0.15,
                'dimension_impacts': {
                    'psychological': 0.1,
                    'tactical': 0.2,
                    'physical': 0.15,
                    'technical': 0.0,
                    'environmental': 0.05,
                    'strategic': 0.35
                }
            },
            'formation_change': {
                'base_impact': 0.2,
                'dimension_impacts': {
                    'psychological': 0.1,
                    'tactical': 0.3,
                    'physical': 0.0,
                    'technical': 0.0,
                    'environmental': 0.0,
                    'strategic': 0.4
                }
            },
            'crowd_surge': {
                'base_impact': 0.15,
                'dimension_impacts': {
                    'psychological': 0.2,
                    'tactical': 0.0,
                    'physical': 0.05,
                    'technical': 0.0,
                    'environmental': 0.5,
                    'strategic': 0.0
                }
            },
            'injury': {
                'base_impact': -0.25,
                'dimension_impacts': {
                    'psychological': -0.25,
                    'tactical': -0.2,
                    'physical': -0.3,
                    'technical': -0.1,
                    'environmental': -0.1,
                    'strategic': -0.2
                }
            },
            'var_review': {
                'base_impact': 0.0,  # Neutre jusqu'à la décision
                'dimension_impacts': {
                    'psychological': -0.1,  # Incertitude
                    'tactical': 0.0,
                    'physical': 0.0,
                    'technical': 0.0,
                    'environmental': 0.3,
                    'strategic': 0.0
                }
            },
            'referee_decision': {
                'base_impact': 0.0,  # Dépend de la décision
                'dimension_impacts': {
                    'psychological': 0.0,
                    'tactical': 0.0,
                    'physical': 0.0,
                    'technical': 0.0,
                    'environmental': 0.2,
                    'strategic': 0.0
                }
            }
        }
        
        # Phases de match et leur impact sur la dynamique du momentum
        self.match_phases = {
            'kickoff': {
                'start': 0,
                'end': 15,
                'momentum_sensitivity': 1.2,  # Plus sensible au début
                'momentum_volatility': 1.3
            },
            'early_first_half': {
                'start': 16,
                'end': 30,
                'momentum_sensitivity': 1.1,
                'momentum_volatility': 1.1
            },
            'late_first_half': {
                'start': 31,
                'end': 45,
                'momentum_sensitivity': 1.3,  # Plus d'impact avant la mi-temps
                'momentum_volatility': 1.0
            },
            'second_half_start': {
                'start': 46,
                'end': 60,
                'momentum_sensitivity': 1.2,
                'momentum_volatility': 1.1
            },
            'mid_second_half': {
                'start': 61,
                'end': 75,
                'momentum_sensitivity': 1.0,
                'momentum_volatility': 1.0
            },
            'late_game': {
                'start': 76,
                'end': 90,
                'momentum_sensitivity': 1.4,  # Très sensible en fin de match
                'momentum_volatility': 1.5
            },
            'injury_time': {
                'start': 91,
                'end': 100,
                'momentum_sensitivity': 1.5,  # Extrêmement sensible
                'momentum_volatility': 1.7
            }
        }
        
        # Historique du momentum multidimensionnel
        self.momentum_history = []
        
        # État actuel du momentum par dimension
        self.current_momentum = {
            'home': {dim: 0.0 for dim in self.momentum_dimensions},
            'away': {dim: 0.0 for dim in self.momentum_dimensions}
        }
        
        # Valeurs globales actuelles du momentum
        self.current_global_momentum = {'home': 0.0, 'away': 0.0}
        
        # Patterns de momentum détectés
        self.detected_patterns = []
        
        # Facteurs de contexte du match
        self.match_context = {
            'score': {'home': 0, 'away': 0},
            'red_cards': {'home': 0, 'away': 0},
            'current_minute': 0,
            'current_phase': 'kickoff',
            'home_team_strength': 0.5,
            'away_team_strength': 0.5,
            'match_importance': 0.5,
            'crowd_factor': 0.5,
            'weather_factor': 0.0
        }
        
        # Buffer des événements récents
        self.recent_events = deque(maxlen=50)
        
        # Historique des changements significatifs
        self.momentum_shifts = []
        
        # Métriques d'influence du momentum sur le match
        self.momentum_match_influence = {
            'momentum_goals': 0,  # Buts marqués durant un momentum fort
            'comeback_potential': 0.0,
            'momentum_efficiency': 0.0,
            'critical_moments': []
        }
        
        # État d'initialisation
        self.initialized = False
    
    def initialize_match(self, match_data):
        """
        Initialiser les paramètres pour un nouveau match.
        
        Args:
            match_data (dict): Données du match (équipes, importance, etc.)
            
        Returns:
            dict: État initial du momentum
        """
        # Réinitialiser les structures
        self.momentum_history = []
        self.current_momentum = {
            'home': {dim: 0.0 for dim in self.momentum_dimensions},
            'away': {dim: 0.0 for dim in self.momentum_dimensions}
        }
        self.current_global_momentum = {'home': 0.0, 'away': 0.0}
        self.detected_patterns = []
        self.recent_events = deque(maxlen=50)
        self.momentum_shifts = []
        self.momentum_match_influence = {
            'momentum_goals': 0,
            'comeback_potential': 0.0,
            'momentum_efficiency': 0.0,
            'critical_moments': []
        }
        
        # Initialiser le contexte du match
        self.match_context = {
            'score': {'home': 0, 'away': 0},
            'red_cards': {'home': 0, 'away': 0},
            'current_minute': 0,
            'current_phase': 'kickoff',
            'home_team_strength': match_data.get('home_team', {}).get('strength', 0.5),
            'away_team_strength': match_data.get('away_team', {}).get('strength', 0.5),
            'match_importance': match_data.get('importance', 0.5),
            'crowd_factor': match_data.get('crowd_factor', 0.5),
            'weather_factor': match_data.get('weather_factor', 0.0)
        }
        
        # Calculer l'avantage initial
        home_advantage = 0.1 * self.match_context['crowd_factor']
        initial_momentum = self._calculate_initial_momentum(match_data)
        
        # Appliquer l'avantage initial
        for dim in self.momentum_dimensions:
            self.current_momentum['home'][dim] = initial_momentum['home'][dim]
            self.current_momentum['away'][dim] = initial_momentum['away'][dim]
        
        # Calculer le momentum global
        self._update_global_momentum()
        
        # Enregistrer l'état initial dans l'historique
        self._record_momentum_state(0)
        
        self.initialized = True
        
        # Retourner l'état initial
        return {
            'home_team': match_data.get('home_team', {}).get('name', 'Home'),
            'away_team': match_data.get('away_team', {}).get('name', 'Away'),
            'initial_momentum': {
                'home': self.current_global_momentum['home'],
                'away': self.current_global_momentum['away']
            },
            'momentum_by_dimension': {
                'home': self.current_momentum['home'],
                'away': self.current_momentum['away']
            },
            'advantage': 'home' if self.current_global_momentum['home'] > self.current_global_momentum['away'] else 'away',
            'initialization_time': datetime.now().isoformat()
        }
    
    def process_match_event(self, event_data):
        """
        Traiter un événement de match et mettre à jour le momentum.
        
        Args:
            event_data (dict): Données de l'événement
            
        Returns:
            dict: Impact de l'événement sur le momentum
        """
        if not self.initialized:
            return {
                'status': 'error',
                'message': 'Match non initialisé. Appelez initialize_match() d\'abord.'
            }
        
        # Extraire les informations de l'événement
        event_type = event_data.get('type', '')
        team = event_data.get('team', 'home')  # 'home' ou 'away'
        minute = event_data.get('minute', 0)
        
        # Mettre à jour le contexte du match
        self._update_match_context(event_data)
        
        # Vérifier si l'événement est reconnu
        if event_type not in self.momentum_events:
            return {
                'status': 'warning',
                'message': f'Type d\'événement "{event_type}" non reconnu. Momentum inchangé.'
            }
        
        # Calculer l'impact de l'événement sur le momentum
        impact = self._calculate_event_impact(event_data)
        
        # Appliquer l'impact sur chaque dimension du momentum
        self._apply_momentum_impact(impact, team)
        
        # Mettre à jour le momentum global
        self._update_global_momentum()
        
        # Appliquer la dégradation naturelle du momentum
        self._apply_momentum_decay()
        
        # Vérifier les transferts de momentum entre équipes
        self._process_momentum_transfer()
        
        # Détecter les patterns de momentum
        detected_pattern = self._detect_momentum_patterns()
        
        # Enregistrer l'événement et l'état actuel
        self.recent_events.append(event_data)
        self._record_momentum_state(minute)
        
        # Détecter les changements significatifs de momentum
        momentum_shift = self._detect_momentum_shift(event_data)
        
        # Analyser l'impact du momentum sur le match
        self._analyze_momentum_match_influence(event_data)
        
        # Préparer le résultat
        result = {
            'status': 'success',
            'event': event_type,
            'team': team,
            'minute': minute,
            'momentum_impact': impact,
            'current_momentum': {
                'home': self.current_global_momentum['home'],
                'away': self.current_global_momentum['away']
            },
            'momentum_by_dimension': {
                'home': self.current_momentum['home'],
                'away': self.current_momentum['away']
            },
            'dominant_team': 'home' if self.current_global_momentum['home'] > self.current_global_momentum['away'] else 'away',
            'momentum_advantage': abs(self.current_global_momentum['home'] - self.current_global_momentum['away']),
            'detected_pattern': detected_pattern,
            'momentum_shift': momentum_shift
        }
        
        return result
    
    def analyze_momentum_state(self, minute=None):
        """
        Analyser l'état actuel du momentum ou à un moment spécifique.
        
        Args:
            minute (int, optional): Minute spécifique à analyser
            
        Returns:
            dict: Analyse détaillée du momentum
        """
        if not self.initialized:
            return {
                'status': 'error',
                'message': 'Match non initialisé. Appelez initialize_match() d\'abord.'
            }
        
        # Si une minute spécifique est demandée, chercher dans l'historique
        momentum_state = None
        if minute is not None:
            for state in self.momentum_history:
                if state['minute'] == minute:
                    momentum_state = state
                    break
            
            if not momentum_state:
                return {
                    'status': 'error',
                    'message': f'Aucune donnée de momentum pour la minute {minute}'
                }
        
        # Sinon, utiliser l'état actuel
        else:
            minute = self.match_context['current_minute']
            momentum_state = {
                'minute': minute,
                'global': {
                    'home': self.current_global_momentum['home'],
                    'away': self.current_global_momentum['away']
                },
                'dimensions': {
                    'home': self.current_momentum['home'],
                    'away': self.current_momentum['away']
                }
            }
        
        # Calculer des métriques d'analyse
        dominant_dimensions = self._identify_dominant_dimensions(momentum_state['dimensions'])
        momentum_trend = self._calculate_momentum_trend(minute)
        current_patterns = self._get_active_patterns(minute)
        
        # Calculer la probabilité d'impact sur le match
        match_impact_probability = self._calculate_match_impact_probability(momentum_state)
        
        # Récupérer le contexte de match pour cette minute
        match_phase = self._determine_match_phase(minute)
        
        # Analyse des forces et faiblesses par dimension
        dimensional_analysis = self._analyze_dimensional_strengths(momentum_state['dimensions'])
        
        # Préparer le résultat
        result = {
            'minute': minute,
            'current_momentum': {
                'home': momentum_state['global']['home'],
                'away': momentum_state['global']['away'],
                'advantage': 'home' if momentum_state['global']['home'] > momentum_state['global']['away'] else 'away',
                'advantage_magnitude': abs(momentum_state['global']['home'] - momentum_state['global']['away'])
            },
            'dimensional_momentum': momentum_state['dimensions'],
            'dominant_dimensions': dominant_dimensions,
            'momentum_trend': momentum_trend,
            'active_patterns': current_patterns,
            'match_phase': match_phase,
            'match_impact': {
                'probability': match_impact_probability,
                'potential_effect': self._describe_potential_effect(match_impact_probability, momentum_state)
            },
            'dimensional_analysis': dimensional_analysis,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def forecast_momentum(self, projection_minutes=15):
        """
        Prévoir l'évolution du momentum dans les prochaines minutes.
        
        Args:
            projection_minutes (int): Nombre de minutes à projeter
            
        Returns:
            dict: Prévision de l'évolution du momentum
        """
        if not self.initialized:
            return {
                'status': 'error',
                'message': 'Match non initialisé. Appelez initialize_match() d\'abord.'
            }
        
        # Récupérer l'état actuel
        current_minute = self.match_context['current_minute']
        
        # Extraire les tendances récentes
        recent_history = [state for state in self.momentum_history 
                         if state['minute'] > current_minute - 15]
        
        if not recent_history:
            return {
                'status': 'warning',
                'message': 'Historique insuffisant pour une prévision fiable',
                'forecast': {
                    'home': self.current_global_momentum['home'],
                    'away': self.current_global_momentum['away']
                }
            }
        
        # Calculer les paramètres de tendance
        momentum_trend = self._calculate_momentum_trend(current_minute)
        
        # Initialiser les projections
        projected_momentum = {
            'minutes': [],
            'home': [],
            'away': []
        }
        
        # État actuel
        current_home = self.current_global_momentum['home']
        current_away = self.current_global_momentum['away']
        
        # Projeter l'évolution par minute
        for i in range(1, projection_minutes + 1):
            projected_minute = current_minute + i
            
            # Identifier la phase de match pour cette minute
            match_phase = self._determine_match_phase(projected_minute)
            phase_volatility = self.match_phases[match_phase]['momentum_volatility']
            
            # Calculer les facteurs de tendance
            home_trend_factor = momentum_trend['home']['rate'] * i * phase_volatility
            away_trend_factor = momentum_trend['away']['rate'] * i * phase_volatility
            
            # Ajouter de l'incertitude (volatilité)
            volatility = 0.02 * i  # Augmente avec le temps
            home_noise = random.uniform(-volatility, volatility)
            away_noise = random.uniform(-volatility, volatility)
            
            # Calculer les valeurs projetées
            projected_home = max(0.0, min(1.0, current_home + home_trend_factor + home_noise))
            projected_away = max(0.0, min(1.0, current_away + away_trend_factor + away_noise))
            
            # Enregistrer les projections
            projected_momentum['minutes'].append(projected_minute)
            projected_momentum['home'].append(projected_home)
            projected_momentum['away'].append(projected_away)
        
        # Analyser les points critiques dans la projection
        critical_points = self._identify_critical_points(projected_momentum)
        
        # Évaluer le potentiel de changement significatif
        shift_potential = self._evaluate_shift_potential(projected_momentum)
        
        # Préparer le résultat
        result = {
            'projected_momentum': projected_momentum,
            'critical_points': critical_points,
            'shift_potential': shift_potential,
            'base_trends': momentum_trend,
            'confidence': max(0.2, min(0.9, 0.8 - (0.02 * projection_minutes))),  # Diminue avec la longueur de projection
            'forecast_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def identify_momentum_triggers(self, team='both'):
        """
        Identifier les déclencheurs de momentum pour une équipe.
        
        Args:
            team (str): Équipe à analyser ('home', 'away', 'both')
            
        Returns:
            dict: Analyse des déclencheurs de momentum
        """
        if not self.initialized:
            return {
                'status': 'error',
                'message': 'Match non initialisé. Appelez initialize_match() d\'abord.'
            }
        
        # Vérifier si nous avons assez d'événements
        if len(self.recent_events) < 5:
            return {
                'status': 'warning',
                'message': 'Pas assez d\'événements pour identifier des déclencheurs de momentum',
                'triggers': {}
            }
        
        # Identifier les équipes à analyser
        teams_to_analyze = []
        if team == 'both':
            teams_to_analyze = ['home', 'away']
        else:
            teams_to_analyze = [team]
        
        # Résultats par équipe
        triggers_by_team = {}
        
        for t in teams_to_analyze:
            # Chercher les événements qui ont précédé des hausses significatives de momentum
            momentum_increases = []
            
            for i in range(1, len(self.momentum_history)):
                prev_state = self.momentum_history[i-1]
                curr_state = self.momentum_history[i]
                
                # Détecter une hausse significative du momentum
                momentum_diff = curr_state['global'][t] - prev_state['global'][t]
                if momentum_diff > 0.15:  # Seuil de hausse significative
                    # Rechercher les événements juste avant cette hausse
                    preceding_events = [
                        e for e in self.recent_events
                        if e.get('minute', 0) <= curr_state['minute'] and 
                        e.get('minute', 0) > prev_state['minute'] and
                        e.get('team', '') == t
                    ]
                    
                    for event in preceding_events:
                        momentum_increases.append({
                            'event_type': event.get('type', ''),
                            'minute': event.get('minute', 0),
                            'momentum_increase': momentum_diff
                        })
            
            # Regrouper par type d'événement
            event_type_impacts = {}
            for increase in momentum_increases:
                event_type = increase['event_type']
                if event_type not in event_type_impacts:
                    event_type_impacts[event_type] = []
                
                event_type_impacts[event_type].append(increase['momentum_increase'])
            
            # Calculer l'efficacité moyenne de chaque type d'événement
            triggers = []
            for event_type, impacts in event_type_impacts.items():
                if len(impacts) > 0:
                    avg_impact = sum(impacts) / len(impacts)
                    frequency = len(impacts)
                    
                    triggers.append({
                        'event_type': event_type,
                        'average_impact': avg_impact,
                        'frequency': frequency,
                        'effectiveness': avg_impact * min(1.0, frequency / 3)  # Pondéré par la fréquence, plafonné à 3+ occurrences
                    })
            
            # Trier par efficacité
            triggers.sort(key=lambda x: x['effectiveness'], reverse=True)
            
            # Stocker les résultats pour cette équipe
            triggers_by_team[t] = triggers
        
        # Préparer le résultat
        result = {
            'status': 'success',
            'team_analyzed': team,
            'triggers': triggers_by_team,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def analyze_critical_moments(self):
        """
        Analyser les moments critiques du match en termes de momentum.
        
        Returns:
            dict: Analyse des moments critiques du match
        """
        if not self.initialized:
            return {
                'status': 'error',
                'message': 'Match non initialisé. Appelez initialize_match() d\'abord.'
            }
        
        # Vérifier si nous avons assez de données
        if len(self.momentum_history) < 5:
            return {
                'status': 'warning',
                'message': 'Pas assez de données pour identifier les moments critiques',
                'critical_moments': []
            }
        
        # Identifier les changements significatifs de momentum
        significant_shifts = [shift for shift in self.momentum_shifts 
                             if shift['magnitude'] > 0.25]
        
        # Identifier les périodes de momentum dominant
        dominant_periods = self._identify_dominant_periods()
        
        # Identifier les moments où le momentum a directement influencé le score
        influential_moments = self.momentum_match_influence['critical_moments']
        
        # Identifier les périodes cruciales du match
        crucial_phases = self._identify_crucial_match_phases()
        
        # Consolider les moments critiques
        critical_moments = []
        
        # Ajouter les changements significatifs
        for shift in significant_shifts:
            critical_moments.append({
                'type': 'momentum_shift',
                'minute': shift['minute'],
                'description': f"Changement majeur de momentum en faveur de l'équipe {shift['to_team']}",
                'magnitude': shift['magnitude'],
                'triggered_by': shift.get('triggered_by', 'multiple_events'),
                'significance': min(1.0, shift['magnitude'] * 1.5)
            })
        
        # Ajouter les périodes dominantes
        for period in dominant_periods:
            critical_moments.append({
                'type': 'dominant_period',
                'start_minute': period['start_minute'],
                'end_minute': period['end_minute'],
                'team': period['team'],
                'description': f"Période de momentum dominant pour l'équipe {period['team']}",
                'average_advantage': period['average_advantage'],
                'significance': min(1.0, period['average_advantage'] * period['duration'] / 20)  # Normaliser
            })
        
        # Ajouter les moments d'influence
        for moment in influential_moments:
            critical_moments.append({
                'type': 'momentum_influence',
                'minute': moment['minute'],
                'description': moment['description'],
                'team': moment['team'],
                'event_type': moment['event_type'],
                'significance': moment['significance']
            })
        
        # Ajouter les phases cruciales
        for phase in crucial_phases:
            critical_moments.append({
                'type': 'crucial_phase',
                'start_minute': phase['start_minute'],
                'end_minute': phase['end_minute'],
                'description': phase['description'],
                'significance': phase['significance']
            })
        
        # Trier par minute et éliminer les doublons proches
        critical_moments.sort(key=lambda x: x.get('minute', x.get('start_minute', 0)))
        
        # Filtrer les moments trop proches (à moins de 3 minutes d'écart)
        filtered_moments = []
        last_minute = -5
        
        for moment in critical_moments:
            moment_minute = moment.get('minute', moment.get('start_minute', 0))
            if moment_minute > last_minute + 3:
                filtered_moments.append(moment)
                last_minute = moment_minute
        
        # Identifier le moment le plus critique du match
        most_critical = None
        if filtered_moments:
            most_critical = max(filtered_moments, key=lambda x: x.get('significance', 0))
        
        # Préparer le résultat
        result = {
            'status': 'success',
            'critical_moments': filtered_moments,
            'most_critical_moment': most_critical,
            'total_moments_identified': len(filtered_moments),
            'match_momentum_volatility': self._calculate_match_volatility(),
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def generate_match_momentum_report(self):
        """
        Générer un rapport complet sur le momentum du match.
        
        Returns:
            dict: Rapport détaillé sur le momentum du match
        """
        if not self.initialized:
            return {
                'status': 'error',
                'message': 'Match non initialisé. Appelez initialize_match() d\'abord.'
            }
        
        # Vérifier si nous avons assez de données
        if len(self.momentum_history) < 10:
            return {
                'status': 'warning',
                'message': 'Données insuffisantes pour un rapport complet',
                'limited_report': {
                    'current_momentum': {
                        'home': self.current_global_momentum['home'],
                        'away': self.current_global_momentum['away']
                    },
                    'momentum_shifts': len(self.momentum_shifts)
                }
            }
        
        # Récupérer les statistiques générales du momentum
        momentum_stats = self._calculate_momentum_statistics()
        
        # Analyser les moments critiques
        critical_moments_analysis = self.analyze_critical_moments()
        
        # Analyser les déclencheurs pour les deux équipes
        triggers_analysis = self.identify_momentum_triggers('both')
        
        # Évaluer l'efficacité du momentum
        momentum_efficiency = self._evaluate_momentum_efficiency()
        
        # Identifier les patterns dominants
        dominant_patterns = self._identify_dominant_patterns()
        
        # Analyser la distribution dimensionnelle du momentum
        dimensional_distribution = self._analyze_dimensional_distribution()
        
        # Construire le résumé narratif
        momentum_narrative = self._generate_momentum_narrative()
        
        # Préparer le résultat
        result = {
            'status': 'success',
            'match_summary': {
                'current_minute': self.match_context['current_minute'],
                'score': self.match_context['score'],
                'current_momentum': {
                    'home': self.current_global_momentum['home'],
                    'away': self.current_global_momentum['away']
                }
            },
            'momentum_statistics': momentum_stats,
            'critical_moments': critical_moments_analysis.get('critical_moments', []),
            'momentum_triggers': triggers_analysis.get('triggers', {}),
            'momentum_efficiency': momentum_efficiency,
            'dominant_patterns': dominant_patterns,
            'dimensional_distribution': dimensional_distribution,
            'momentum_narrative': momentum_narrative,
            'report_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def _calculate_initial_momentum(self, match_data):
        """Calculer le momentum initial basé sur les données du match."""
        # Récupérer les forces des équipes
        home_strength = match_data.get('home_team', {}).get('strength', 0.5)
        away_strength = match_data.get('away_team', {}).get('strength', 0.5)
        
        # Facteur d'avantage à domicile
        home_advantage = 0.1 * self.match_context['crowd_factor']
        
        # Initialiser le momentum par dimension
        initial_momentum = {
            'home': {},
            'away': {}
        }
        
        # Calculer pour chaque dimension
        for dim, dim_data in self.momentum_dimensions.items():
            # Base: force relative des équipes
            home_base = home_strength
            away_base = away_strength
            
            # Appliquer l'avantage à domicile, adapté à chaque dimension
            if dim == 'psychological':
                home_base += home_advantage * 1.5
            elif dim == 'environmental':
                home_base += home_advantage * 2.0
            else:
                home_base += home_advantage
            
            # Ajouter une légère variation aléatoire pour éviter le déterminisme
            home_variation = random.uniform(-0.05, 0.05)
            away_variation = random.uniform(-0.05, 0.05)
            
            # Calculer le momentum initial dans cette dimension
            initial_momentum['home'][dim] = max(0.0, min(1.0, home_base + home_variation))
            initial_momentum['away'][dim] = max(0.0, min(1.0, away_base + away_variation))
        
        return initial_momentum
    
    def _update_match_context(self, event_data):
        """Mettre à jour le contexte du match en fonction de l'événement."""
        event_type = event_data.get('type', '')
        team = event_data.get('team', 'home')
        minute = event_data.get('minute', self.match_context['current_minute'])
        
        # Mettre à jour la minute courante
        if minute > self.match_context['current_minute']:
            self.match_context['current_minute'] = minute
            
            # Mettre à jour la phase du match
            self.match_context['current_phase'] = self._determine_match_phase(minute)
        
        # Mettre à jour le score
        if event_type == 'goal':
            self.match_context['score'][team] += 1
        
        # Mettre à jour les cartons rouges
        if event_type == 'red_card':
            self.match_context['red_cards'][team] += 1
    
    def _calculate_event_impact(self, event_data):
        """Calculer l'impact d'un événement sur le momentum."""
        event_type = event_data.get('type', '')
        team = event_data.get('team', 'home')
        minute = event_data.get('minute', 0)
        
        # Si l'événement n'est pas reconnu, pas d'impact
        if event_type not in self.momentum_events:
            return {dim: 0.0 for dim in self.momentum_dimensions}
        
        # Récupérer les impacts de base par dimension
        event_info = self.momentum_events[event_type]
        base_impacts = event_info['dimension_impacts']
        
        # Ajuster selon la phase du match
        match_phase = self._determine_match_phase(minute)
        phase_sensitivity = self.match_phases[match_phase]['momentum_sensitivity']
        
        # Ajuster selon le score
        score_factor = self._calculate_score_factor(team)
        
        # Ajuster selon l'importance du match
        importance_factor = 1.0 + (self.match_context['match_importance'] - 0.5)
        
        # Calculer l'impact final pour chaque dimension
        final_impacts = {}
        for dim in self.momentum_dimensions:
            base_impact = base_impacts.get(dim, 0.0)
            
            # Appliquer les facteurs d'ajustement
            adjusted_impact = base_impact * phase_sensitivity * score_factor * importance_factor
            
            # Limiter à une plage raisonnable
            final_impacts[dim] = max(-0.5, min(0.5, adjusted_impact))
        
        return final_impacts
    
    def _apply_momentum_impact(self, impact, team):
        """Appliquer l'impact sur le momentum."""
        # Appliquer l'impact pour chaque dimension
        for dim, value in impact.items():
            # Équipe bénéficiaire
            self.current_momentum[team][dim] += value
            
            # Limiter à la plage [0, 1]
            self.current_momentum[team][dim] = max(0.0, min(1.0, self.current_momentum[team][dim]))
    
    def _update_global_momentum(self):
        """Mettre à jour le momentum global à partir des dimensions."""
        # Calculer pour chaque équipe
        for team in ['home', 'away']:
            weighted_sum = 0.0
            total_weight = 0.0
            
            for dim, value in self.current_momentum[team].items():
                weight = self.momentum_dimensions[dim]['weight']
                weighted_sum += value * weight
                total_weight += weight
            
            # Normaliser
            if total_weight > 0:
                self.current_global_momentum[team] = weighted_sum / total_weight
            else:
                self.current_global_momentum[team] = 0.5  # Valeur par défaut
    
    def _apply_momentum_decay(self):
        """Appliquer la dégradation naturelle du momentum."""
        for team in ['home', 'away']:
            for dim, value in self.current_momentum[team].items():
                # Récupérer le taux de dégradation pour cette dimension
                decay_rate = self.momentum_dimensions[dim]['decay_rate']
                
                # Appliquer la dégradation
                # Plus la valeur est éloignée de 0.5, plus forte est la dégradation
                decay_amount = (value - 0.5) * (1.0 - decay_rate)
                self.current_momentum[team][dim] -= decay_amount
                
                # Limiter à la plage [0, 1]
                self.current_momentum[team][dim] = max(0.0, min(1.0, self.current_momentum[team][dim]))
    
    def _process_momentum_transfer(self):
        """Traiter le transfert de momentum entre les équipes."""
        # Pour chaque dimension
        for dim in self.momentum_dimensions:
            # Calculer la différence de momentum dans cette dimension
            home_value = self.current_momentum['home'][dim]
            away_value = self.current_momentum['away'][dim]
            
            # Si la différence est significative, il y a un transfert potentiel
            if abs(home_value - away_value) > 0.3:
                # Récupérer le taux de transfert pour cette dimension
                transfer_rate = self.momentum_dimensions[dim]['transfer_rate']
                
                # Calculer le montant du transfert
                transfer_amount = (abs(home_value - away_value) - 0.3) * transfer_rate
                
                # Appliquer le transfert (depuis l'équipe forte vers la faible)
                if home_value > away_value:
                    self.current_momentum['home'][dim] -= transfer_amount
                    self.current_momentum['away'][dim] += transfer_amount
                else:
                    self.current_momentum['home'][dim] += transfer_amount
                    self.current_momentum['away'][dim] -= transfer_amount
                
                # Limiter à la plage [0, 1]
                self.current_momentum['home'][dim] = max(0.0, min(1.0, self.current_momentum['home'][dim]))
                self.current_momentum['away'][dim] = max(0.0, min(1.0, self.current_momentum['away'][dim]))
    
    def _detect_momentum_patterns(self):
        """Détecter les patterns de momentum dans l'historique récent."""
        # Vérifier si nous avons assez de données
        if len(self.momentum_history) < 5:
            return None
        
        # Extraire l'historique récent
        recent_history = self.momentum_history[-15:]  # Dernières 15 entrées
        
        # Vérifier chaque pattern
        detected_patterns = []
        
        for pattern_name, pattern_data in self.momentum_patterns.items():
            detected = self._check_pattern(pattern_name, recent_history)
            if detected:
                detected_patterns.append({
                    'pattern': pattern_name,
                    'description': pattern_data['description'],
                    'confidence': detected['confidence'],
                    'team': detected['team'],
                    'start_minute': detected['start_minute'],
                    'end_minute': detected['end_minute']
                })
        
        # Enregistrer les patterns détectés
        if detected_patterns:
            best_pattern = max(detected_patterns, key=lambda x: x['confidence'])
            self.detected_patterns.append({
                'minute': self.match_context['current_minute'],
                'pattern': best_pattern['pattern'],
                'team': best_pattern['team'],
                'confidence': best_pattern['confidence']
            })
            
            return best_pattern
        
        return None
    
    def _check_pattern(self, pattern_name, history):
        """Vérifier si un pattern spécifique est présent dans l'historique."""
        pattern_data = self.momentum_patterns[pattern_name]
        detection_window = pattern_data['detection_window']
        threshold = pattern_data['recognition_threshold']
        
        # Vérifier si l'historique est suffisamment long
        if len(history) < detection_window:
            return None
        
        # Différentes logiques de détection selon le pattern
        if pattern_name == 'crescendo':
            # Rechercher une augmentation progressive
            for team in ['home', 'away']:
                start_value = history[-detection_window]['global'][team]
                end_value = history[-1]['global'][team]
                
                # Vérifier que l'augmentation est significative et progressive
                if end_value - start_value > 0.2:
                    # Vérifier la progressivité
                    is_progressive = True
                    for i in range(1, detection_window):
                        if history[-i]['global'][team] < history[-(i+1)]['global'][team]:
                            is_progressive = False
                            break
                    
                    if is_progressive:
                        confidence = min(1.0, (end_value - start_value) * 2)
                        if confidence > threshold:
                            return {
                                'team': team,
                                'confidence': confidence,
                                'start_minute': history[-detection_window]['minute'],
                                'end_minute': history[-1]['minute']
                            }
        
        elif pattern_name == 'sudden_shift':
            # Rechercher un changement brusque
            for i in range(1, len(history)):
                for team in ['home', 'away']:
                    momentum_diff = history[i]['global'][team] - history[i-1]['global'][team]
                    
                    # Changement supérieur à 20% en une seule itération
                    if momentum_diff > 0.2:
                        confidence = min(1.0, momentum_diff * 2.5)
                        if confidence > threshold:
                            return {
                                'team': team,
                                'confidence': confidence,
                                'start_minute': history[i-1]['minute'],
                                'end_minute': history[i]['minute']
                            }
        
        elif pattern_name == 'oscillation':
            # Rechercher des alternances
            oscillations = 0
            dominant_team = 'home' if history[0]['global']['home'] > history[0]['global']['away'] else 'away'
            
            for i in range(1, len(history)):
                current_dominant = 'home' if history[i]['global']['home'] > history[i]['global']['away'] else 'away'
                
                if current_dominant != dominant_team:
                    oscillations += 1
                    dominant_team = current_dominant
            
            # Vérifier si les oscillations sont significatives
            if oscillations >= 3:  # Au moins 3 changements
                confidence = min(1.0, oscillations / 5)  # 5 oscillations donnent une confiance de 1.0
                if confidence > threshold:
                    return {
                        'team': 'both',  # Ce pattern concerne les deux équipes
                        'confidence': confidence,
                        'start_minute': history[0]['minute'],
                        'end_minute': history[-1]['minute']
                    }
        
        elif pattern_name == 'plateau':
            # Rechercher une stabilisation
            for team in ['home', 'away']:
                if len(history) >= detection_window:
                    recent_values = [state['global'][team] for state in history[-detection_window:]]
                    
                    # Calculer la stabilité (écart-type faible)
                    std_dev = np.std(recent_values)
                    mean_value = np.mean(recent_values)
                    
                    # Vérifier si la valeur est significative et stable
                    if mean_value > 0.6 and std_dev < 0.05:
                        confidence = min(1.0, (1.0 - std_dev * 10) * mean_value)
                        if confidence > threshold:
                            return {
                                'team': team,
                                'confidence': confidence,
                                'start_minute': history[-detection_window]['minute'],
                                'end_minute': history[-1]['minute']
                            }
        
        elif pattern_name == 'snowball':
            # Rechercher un effet d'auto-renforcement
            for team in ['home', 'away']:
                if len(history) >= detection_window:
                    # Vérifier si le momentum s'accélère
                    values = [state['global'][team] for state in history[-detection_window:]]
                    
                    # Calculer les différences de premier ordre (vitesse)
                    first_derivatives = [values[i] - values[i-1] for i in range(1, len(values))]
                    
                    # Calculer les différences de second ordre (accélération)
                    second_derivatives = [first_derivatives[i] - first_derivatives[i-1] for i in range(1, len(first_derivatives))]
                    
                    # Vérifier si l'accélération est positive
                    if sum(second_derivatives) > 0 and values[-1] > 0.6:
                        confidence = min(1.0, values[-1] * (1.0 + sum(second_derivatives) * 5))
                        if confidence > threshold:
                            return {
                                'team': team,
                                'confidence': confidence,
                                'start_minute': history[-detection_window]['minute'],
                                'end_minute': history[-1]['minute']
                            }
        
        elif pattern_name == 'resilient_response':
            # Rechercher une réponse après un momentum adverse
            for team in ['home', 'away']:
                opponent = 'away' if team == 'home' else 'home'
                
                for i in range(detection_window, len(history)):
                    # Vérifier si l'adversaire avait un momentum fort
                    previous_opponent_momentum = max([history[j]['global'][opponent] for j in range(i-detection_window, i)])
                    
                    if previous_opponent_momentum > 0.6:
                        # Vérifier si l'équipe a répondu
                        current_momentum = history[i]['global'][team]
                        previous_momentum = history[i-detection_window]['global'][team]
                        
                        if current_momentum > previous_momentum + 0.2:
                            confidence = min(1.0, (current_momentum - previous_momentum) * 2)
                            if confidence > threshold:
                                return {
                                    'team': team,
                                    'confidence': confidence,
                                    'start_minute': history[i-detection_window]['minute'],
                                    'end_minute': history[i]['minute']
                                }
        
        return None
    
    def _record_momentum_state(self, minute):
        """Enregistrer l'état actuel du momentum dans l'historique."""
        state = {
            'minute': minute,
            'global': {
                'home': self.current_global_momentum['home'],
                'away': self.current_global_momentum['away']
            },
            'dimensions': {
                'home': self.current_momentum['home'].copy(),
                'away': self.current_momentum['away'].copy()
            },
            'match_context': {
                'score': self.match_context['score'].copy(),
                'red_cards': self.match_context['red_cards'].copy(),
                'phase': self.match_context['current_phase']
            },
            'timestamp': datetime.now().isoformat()
        }
        
        self.momentum_history.append(state)
    
    def _detect_momentum_shift(self, event_data):
        """Détecter un changement significatif de momentum."""
        # Vérifier si nous avons assez d'historique
        if len(self.momentum_history) < 2:
            return None
        
        # Récupérer les états avant et après
        previous_state = self.momentum_history[-2] if len(self.momentum_history) > 1 else None
        current_state = self.momentum_history[-1]
        
        if not previous_state:
            return None
        
        # Vérifier s'il y a un changement d'équipe dominante
        previous_dominant = 'home' if previous_state['global']['home'] > previous_state['global']['away'] else 'away'
        current_dominant = 'home' if current_state['global']['home'] > current_state['global']['away'] else 'away'
        
        # Si pas de changement d'équipe dominante, vérifier un changement d'amplitude
        if previous_dominant == current_dominant:
            previous_advantage = abs(previous_state['global']['home'] - previous_state['global']['away'])
            current_advantage = abs(current_state['global']['home'] - current_state['global']['away'])
            
            # Si l'avantage a augmenté significativement
            if current_advantage > previous_advantage + 0.2:
                shift = {
                    'type': 'amplification',
                    'minute': current_state['minute'],
                    'team': current_dominant,
                    'from_value': previous_advantage,
                    'to_value': current_advantage,
                    'magnitude': current_advantage - previous_advantage,
                    'triggered_by': event_data.get('type', '')
                }
                
                self.momentum_shifts.append(shift)
                return shift
        
        # Si changement d'équipe dominante
        elif previous_dominant != current_dominant:
            previous_advantage = previous_state['global'][previous_dominant] - previous_state['global'][current_dominant]
            current_advantage = current_state['global'][current_dominant] - current_state['global'][previous_dominant]
            
            # Calculer la magnitude du changement
            magnitude = previous_advantage + current_advantage
            
            shift = {
                'type': 'switch',
                'minute': current_state['minute'],
                'from_team': previous_dominant,
                'to_team': current_dominant,
                'magnitude': magnitude,
                'triggered_by': event_data.get('type', '')
            }
            
            self.momentum_shifts.append(shift)
            return shift
        
        return None
    
    def _analyze_momentum_match_influence(self, event_data):
        """Analyser l'influence du momentum sur le match."""
        event_type = event_data.get('type', '')
        team = event_data.get('team', 'home')
        minute = event_data.get('minute', 0)
        
        # Si l'événement est un but, vérifier s'il a été marqué durant un momentum fort
        if event_type == 'goal':
            team_momentum = self.current_global_momentum[team]
            
            # Si le momentum est fort (> 0.7)
            if team_momentum > 0.7:
                self.momentum_match_influence['momentum_goals'] += 1
                
                # Enregistrer comme moment critique
                self.momentum_match_influence['critical_moments'].append({
                    'minute': minute,
                    'team': team,
                    'event_type': 'goal',
                    'description': f"But marqué par l'équipe {team} durant un fort momentum ({team_momentum:.2f})",
                    'significance': team_momentum
                })
        
        # Mettre à jour le potentiel de comeback
        self._update_comeback_potential()
        
        # Mettre à jour l'efficacité du momentum
        self._update_momentum_efficiency()
    
    def _update_comeback_potential(self):
        """Mettre à jour le potentiel de comeback basé sur le momentum actuel."""
        # Vérifier quelle équipe est menée
        home_score = self.match_context['score']['home']
        away_score = self.match_context['score']['away']
        
        if home_score == away_score:
            # Match nul, pas de comeback possible
            self.momentum_match_influence['comeback_potential'] = 0.0
            return
        
        # Déterminer l'équipe menée et son adversaire
        trailing_team = 'home' if home_score < away_score else 'away'
        leading_team = 'away' if trailing_team == 'home' else 'home'
        
        # Calculer l'écart de score
        score_difference = abs(home_score - away_score)
        
        # Calculer le potentiel de comeback
        # Facteurs: momentum de l'équipe menée, temps restant, écart de score
        trailing_momentum = self.current_global_momentum[trailing_team]
        minutes_remaining = max(0, 90 - self.match_context['current_minute'])
        time_factor = minutes_remaining / 90
        
        # Formule: plus le momentum est élevé, plus le temps restant est important, moins l'écart est grand
        comeback_potential = trailing_momentum * time_factor / (score_difference * 0.5 + 0.5)
        
        # Limiter à [0, 1]
        comeback_potential = max(0.0, min(1.0, comeback_potential))
        
        self.momentum_match_influence['comeback_potential'] = comeback_potential
    
    def _update_momentum_efficiency(self):
        """Mettre à jour l'efficacité du momentum."""
        # Calculer l'efficacité: ratio entre les buts marqués durant un momentum fort et les périodes de momentum fort
        strong_momentum_periods = 0
        
        for state in self.momentum_history:
            if state['global']['home'] > 0.7 or state['global']['away'] > 0.7:
                strong_momentum_periods += 1
        
        # Éviter la division par zéro
        if strong_momentum_periods > 0:
            efficiency = self.momentum_match_influence['momentum_goals'] / strong_momentum_periods
        else:
            efficiency = 0.0
        
        # Normaliser l'efficacité
        normalized_efficiency = min(1.0, efficiency * 5)  # 5 est un facteur arbitraire
        
        self.momentum_match_influence['momentum_efficiency'] = normalized_efficiency
    
    def _calculate_score_factor(self, team):
        """Calculer un facteur d'ajustement basé sur le score."""
        home_score = self.match_context['score']['home']
        away_score = self.match_context['score']['away']
        
        # Déterminer si l'équipe est en avance, à égalité ou en retard
        if team == 'home':
            if home_score > away_score:
                score_state = 'leading'
            elif home_score < away_score:
                score_state = 'trailing'
            else:
                score_state = 'tied'
        else:  # away
            if away_score > home_score:
                score_state = 'leading'
            elif away_score < home_score:
                score_state = 'trailing'
            else:
                score_state = 'tied'
        
        # Calculer le facteur selon l'état du score
        if score_state == 'leading':
            return 0.9  # Légèrement réduit car déjà en avance
        elif score_state == 'trailing':
            return 1.2  # Amplifié pour permettre le retour
        else:  # tied
            return 1.0  # Neutre
    
    def _determine_match_phase(self, minute):
        """Déterminer la phase actuelle du match en fonction de la minute."""
        for phase, data in self.match_phases.items():
            if data['start'] <= minute <= data['end']:
                return phase
        
        # Par défaut, retourner la dernière phase
        return 'injury_time'
    
    def _identify_dominant_dimensions(self, dimensions):
        """Identifier les dimensions dominantes pour chaque équipe."""
        dominant_dimensions = {'home': [], 'away': []}
        
        for team in ['home', 'away']:
            # Trier les dimensions par valeur
            sorted_dims = sorted(dimensions[team].items(), key=lambda x: x[1], reverse=True)
            
            # Filtrer celles au-dessus d'un seuil
            strong_dims = [dim for dim, value in sorted_dims if value > 0.65]
            
            # Prendre les 3 meilleures dimensions
            top_dims = sorted_dims[:3]
            
            # Stocker les dimensions dominantes avec leurs valeurs
            for dim, value in top_dims:
                dominant_dimensions[team].append({
                    'dimension': dim,
                    'value': value,
                    'is_strong': value > 0.65,
                    'description': self.momentum_dimensions[dim]['description']
                })
        
        return dominant_dimensions
    
    def _calculate_momentum_trend(self, current_minute):
        """Calculer la tendance récente du momentum."""
        # Récupérer l'historique récent
        recent_history = [state for state in self.momentum_history 
                         if state['minute'] >= current_minute - 15]
        
        if len(recent_history) < 3:
            return {
                'home': {'direction': 'stable', 'rate': 0.0},
                'away': {'direction': 'stable', 'rate': 0.0}
            }
        
        # Extraire les valeurs de momentum
        home_values = [state['global']['home'] for state in recent_history]
        away_values = [state['global']['away'] for state in recent_history]
        
        # Calculer la pente de la tendance (régression linéaire simple)
        x = list(range(len(home_values)))
        
        # Fonction pour calculer la pente
        def calculate_slope(y_values):
            n = len(y_values)
            if n < 2:
                return 0.0
            
            mean_x = sum(x) / n
            mean_y = sum(y_values) / n
            
            numerator = sum((x[i] - mean_x) * (y_values[i] - mean_y) for i in range(n))
            denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
            
            if denominator == 0:
                return 0.0
            
            return numerator / denominator
        
        # Calculer les pentes
        home_slope = calculate_slope(home_values)
        away_slope = calculate_slope(away_values)
        
        # Déterminer la direction de la tendance
        def get_direction(slope):
            if slope > 0.01:
                return 'rising'
            elif slope < -0.01:
                return 'falling'
            else:
                return 'stable'
        
        return {
            'home': {
                'direction': get_direction(home_slope),
                'rate': home_slope
            },
            'away': {
                'direction': get_direction(away_slope),
                'rate': away_slope
            }
        }
    
    def _get_active_patterns(self, minute):
        """Récupérer les patterns actifs à un moment donné."""
        # Filtrer les patterns récents
        active_patterns = [pattern for pattern in self.detected_patterns 
                          if abs(pattern['minute'] - minute) <= 5]
        
        # Trier par confiance
        active_patterns.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Limiter aux 3 plus pertinents
        return active_patterns[:3]
    
    def _calculate_match_impact_probability(self, momentum_state):
        """Calculer la probabilité d'impact sur le match."""
        # Facteurs: amplitude du momentum, phase du match, différence de score
        home_momentum = momentum_state['global']['home']
        away_momentum = momentum_state['global']['away']
        momentum_diff = abs(home_momentum - away_momentum)
        
        # Plus la différence est grande, plus l'impact est probable
        base_probability = momentum_diff * 0.7
        
        # Ajuster selon la phase du match
        match_phase = self._determine_match_phase(momentum_state['minute'])
        phase_factor = self.match_phases[match_phase]['momentum_sensitivity']
        
        # Ajuster selon le score
        score_diff = abs(self.match_context['score']['home'] - self.match_context['score']['away'])
        score_factor = 1.0 if score_diff <= 1 else (1.0 / score_diff)
        
        # Calculer la probabilité finale
        impact_probability = base_probability * phase_factor * score_factor
        
        # Limiter à [0, 1]
        return max(0.0, min(1.0, impact_probability))
    
    def _describe_potential_effect(self, probability, momentum_state):
        """Décrire l'effet potentiel du momentum sur le match."""
        if probability < 0.3:
            return "Influence limitée sur le cours du match"
        
        # Déterminer l'équipe avec l'avantage
        dominant_team = 'home' if momentum_state['global']['home'] > momentum_state['global']['away'] else 'away'
        advantage = abs(momentum_state['global']['home'] - momentum_state['global']['away'])
        
        if probability >= 0.7:
            if advantage > 0.4:
                return f"Fort potentiel d'influencer le résultat en faveur de l'équipe {dominant_team}"
            else:
                return "Potentiel significatif d'influencer la dynamique du match"
        elif probability >= 0.5:
            return f"Peut créer des opportunités favorables pour l'équipe {dominant_team}"
        else:
            return "Peut influencer des situations spécifiques du match"
    
    def _analyze_dimensional_strengths(self, dimensions):
        """Analyser les forces et faiblesses dimensionnelles."""
        strengths = {'home': [], 'away': []}
        weaknesses = {'home': [], 'away': []}
        
        for team in ['home', 'away']:
            # Identifier les dimensions fortes
            for dim, value in dimensions[team].items():
                if value > 0.7:
                    strengths[team].append({
                        'dimension': dim,
                        'value': value,
                        'description': f"Fort momentum {self.momentum_dimensions[dim]['description'].lower()}"
                    })
                elif value < 0.4:
                    weaknesses[team].append({
                        'dimension': dim,
                        'value': value,
                        'description': f"Faible momentum {self.momentum_dimensions[dim]['description'].lower()}"
                    })
        
        # Calculer les avantages dimensionnels
        dimensional_advantages = []
        
        for dim in self.momentum_dimensions:
            home_value = dimensions['home'][dim]
            away_value = dimensions['away'][dim]
            
            if abs(home_value - away_value) > 0.2:
                advantaged_team = 'home' if home_value > away_value else 'away'
                advantage = abs(home_value - away_value)
                
                dimensional_advantages.append({
                    'dimension': dim,
                    'team': advantaged_team,
                    'advantage': advantage,
                    'description': f"Avantage {self.momentum_dimensions[dim]['description'].lower()} pour l'équipe {advantaged_team}"
                })
        
        # Trier par amplitude d'avantage
        dimensional_advantages.sort(key=lambda x: x['advantage'], reverse=True)
        
        return {
            'strengths': strengths,
            'weaknesses': weaknesses,
            'dimensional_advantages': dimensional_advantages
        }
    
    def _identify_critical_points(self, projected_momentum):
        """Identifier les points critiques dans une projection de momentum."""
        critical_points = []
        
        # Extraire les séries
        minutes = projected_momentum['minutes']
        home_values = projected_momentum['home']
        away_values = projected_momentum['away']
        
        # Vérifier les croisements (changements d'équipe dominante)
        for i in range(1, len(minutes)):
            prev_dominant = 'home' if home_values[i-1] > away_values[i-1] else 'away'
            curr_dominant = 'home' if home_values[i] > away_values[i] else 'away'
            
            if prev_dominant != curr_dominant:
                critical_points.append({
                    'type': 'dominance_switch',
                    'minute': minutes[i],
                    'from_team': prev_dominant,
                    'to_team': curr_dominant,
                    'home_momentum': home_values[i],
                    'away_momentum': away_values[i],
                    'description': f"Changement prévu d'équipe dominante à la minute {minutes[i]}"
                })
        
        # Vérifier les pics et les creux
        for team, values in [('home', home_values), ('away', away_values)]:
            for i in range(1, len(values) - 1):
                # Détecter un pic
                if values[i] > values[i-1] and values[i] > values[i+1] and values[i] > 0.65:
                    critical_points.append({
                        'type': 'momentum_peak',
                        'minute': minutes[i],
                        'team': team,
                        'value': values[i],
                        'description': f"Pic de momentum prévu pour l'équipe {team} à la minute {minutes[i]}"
                    })
                
                # Détecter un creux
                if values[i] < values[i-1] and values[i] < values[i+1] and values[i] < 0.35:
                    critical_points.append({
                        'type': 'momentum_trough',
                        'minute': minutes[i],
                        'team': team,
                        'value': values[i],
                        'description': f"Creux de momentum prévu pour l'équipe {team} à la minute {minutes[i]}"
                    })
        
        # Trier par minute
        critical_points.sort(key=lambda x: x['minute'])
        
        return critical_points
    
    def _evaluate_shift_potential(self, projected_momentum):
        """Évaluer le potentiel de changement significatif dans une projection."""
        # Calculer la différence maximale pour chaque équipe
        home_values = projected_momentum['home']
        away_values = projected_momentum['away']
        
        home_current = home_values[0]
        away_current = away_values[0]
        
        home_max_change = max(abs(v - home_current) for v in home_values)
        away_max_change = max(abs(v - away_current) for v in away_values)
        
        # Vérifier les croisements
        crossovers = 0
        dominant_team = 'home' if home_current > away_current else 'away'
        
        for i in range(1, len(home_values)):
            current_dominant = 'home' if home_values[i] > away_values[i] else 'away'
            if current_dominant != dominant_team:
                crossovers += 1
                dominant_team = current_dominant
        
        # Calculer le potentiel de changement
        shift_potential = max(home_max_change, away_max_change) * 0.7 + (crossovers * 0.1)
        
        # Classifier le potentiel
        category = 'low'
        if shift_potential > 0.4:
            category = 'high'
        elif shift_potential > 0.2:
            category = 'medium'
        
        return {
            'value': shift_potential,
            'category': category,
            'max_home_change': home_max_change,
            'max_away_change': away_max_change,
            'expected_crossovers': crossovers
        }
    
    def _identify_dominant_periods(self):
        """Identifier les périodes de momentum dominant."""
        # Vérifier si nous avons assez de données
        if len(self.momentum_history) < 5:
            return []
        
        dominant_periods = []
        
        # Trier par minute
        sorted_history = sorted(self.momentum_history, key=lambda x: x['minute'])
        
        # Parcourir l'historique
        current_period = None
        
        for i, state in enumerate(sorted_history):
            home_momentum = state['global']['home']
            away_momentum = state['global']['away']
            
            # Déterminer l'équipe dominante
            dominant = 'home' if home_momentum > away_momentum else 'away'
            advantage = abs(home_momentum - away_momentum)
            
            # Si avantage significatif
            if advantage > 0.25:
                # Si pas de période en cours ou changement d'équipe dominante
                if current_period is None or current_period['team'] != dominant:
                    # Terminer la période précédente si elle existe
                    if current_period:
                        current_period['end_minute'] = state['minute'] - 1
                        current_period['duration'] = current_period['end_minute'] - current_period['start_minute'] + 1
                        
                        # Ajouter si la durée est suffisante
                        if current_period['duration'] >= 5:
                            dominant_periods.append(current_period)
                    
                    # Commencer une nouvelle période
                    current_period = {
                        'team': dominant,
                        'start_minute': state['minute'],
                        'end_minute': None,
                        'average_advantage': advantage,
                        'advantages': [advantage],
                        'duration': None
                    }
                else:
                    # Continuer la période en cours
                    current_period['advantages'].append(advantage)
                    current_period['average_advantage'] = sum(current_period['advantages']) / len(current_period['advantages'])
            else:
                # Avantage non significatif, terminer la période en cours si elle existe
                if current_period:
                    current_period['end_minute'] = state['minute'] - 1
                    current_period['duration'] = current_period['end_minute'] - current_period['start_minute'] + 1
                    
                    # Ajouter si la durée est suffisante
                    if current_period['duration'] >= 5:
                        dominant_periods.append(current_period)
                    
                    current_period = None
        
        # Gérer la dernière période si non terminée
        if current_period:
            current_period['end_minute'] = sorted_history[-1]['minute']
            current_period['duration'] = current_period['end_minute'] - current_period['start_minute'] + 1
            
            # Ajouter si la durée est suffisante
            if current_period['duration'] >= 5:
                dominant_periods.append(current_period)
        
        return dominant_periods
    
    def _identify_crucial_match_phases(self):
        """Identifier les phases cruciales du match en termes de momentum."""
        # Vérifier si nous avons assez de données
        if len(self.momentum_history) < 10:
            return []
        
        crucial_phases = []
        
        # Identifier les phases de haute volatilité du momentum
        volatility_windows = []
        window_size = 5  # Minutes
        
        for i in range(len(self.momentum_history) - window_size + 1):
            window = self.momentum_history[i:i+window_size]
            
            # Calculer la volatilité dans cette fenêtre
            home_values = [state['global']['home'] for state in window]
            away_values = [state['global']['away'] for state in window]
            
            home_volatility = np.std(home_values)
            away_volatility = np.std(away_values)
            
            total_volatility = home_volatility + away_volatility
            
            if total_volatility > 0.2:  # Seuil de volatilité significative
                volatility_windows.append({
                    'start_minute': window[0]['minute'],
                    'end_minute': window[-1]['minute'],
                    'volatility': total_volatility,
                    'description': f"Phase de forte volatilité du momentum (minutes {window[0]['minute']}-{window[-1]['minute']})",
                    'significance': min(1.0, total_volatility * 2)
                })
        
        # Fusionner les fenêtres qui se chevauchent
        merged_windows = []
        
        if volatility_windows:
            current_window = volatility_windows[0]
            
            for i in range(1, len(volatility_windows)):
                if volatility_windows[i]['start_minute'] <= current_window['end_minute'] + 2:
                    # Fusionner les fenêtres
                    current_window['end_minute'] = volatility_windows[i]['end_minute']
                    current_window['volatility'] = max(current_window['volatility'], volatility_windows[i]['volatility'])
                    current_window['significance'] = max(current_window['significance'], volatility_windows[i]['significance'])
                else:
                    # Ajouter la fenêtre actuelle et commencer une nouvelle
                    merged_windows.append(current_window)
                    current_window = volatility_windows[i]
            
            # Ajouter la dernière fenêtre
            merged_windows.append(current_window)
        
        # Ajouter aux phases cruciales
        crucial_phases.extend(merged_windows)
        
        # Ajouter les périodes avec des transitions significatives
        significant_transitions = []
        
        for shift in self.momentum_shifts:
            if shift.get('magnitude', 0) > 0.35:
                minute = shift.get('minute', 0)
                significant_transitions.append({
                    'start_minute': max(0, minute - 2),
                    'end_minute': minute + 2,
                    'description': f"Transition majeure du momentum à la minute {minute}",
                    'significance': min(1.0, shift.get('magnitude', 0) * 1.5)
                })
        
        # Ajouter aux phases cruciales
        crucial_phases.extend(significant_transitions)
        
        # Trier par minute de début
        crucial_phases.sort(key=lambda x: x['start_minute'])
        
        return crucial_phases
    
    def _calculate_match_volatility(self):
        """Calculer la volatilité globale du momentum pendant le match."""
        # Vérifier si nous avons assez de données
        if len(self.momentum_history) < 5:
            return 0.5  # Valeur par défaut
        
        # Extraire les séries de momentum
        home_values = [state['global']['home'] for state in self.momentum_history]
        away_values = [state['global']['away'] for state in self.momentum_history]
        
        # Calculer les différences d'un état à l'autre
        home_diffs = [abs(home_values[i] - home_values[i-1]) for i in range(1, len(home_values))]
        away_diffs = [abs(away_values[i] - away_values[i-1]) for i in range(1, len(away_values))]
        
        # Calculer la volatilité moyenne
        avg_volatility = (sum(home_diffs) + sum(away_diffs)) / (len(home_diffs) + len(away_diffs))
        
        # Normaliser sur une échelle 0-1
        normalized_volatility = min(1.0, avg_volatility * 10)  # Facteur arbitraire
        
        return normalized_volatility
    
    def _calculate_momentum_statistics(self):
        """Calculer les statistiques générales du momentum."""
        # Vérifier si nous avons assez de données
        if len(self.momentum_history) < 5:
            return {
                'average_momentum': {'home': 0.5, 'away': 0.5},
                'volatility': 0.5,
                'momentum_shifts': 0,
                'dominant_team': 'none'
            }
        
        # Extraire les séries de momentum
        home_values = [state['global']['home'] for state in self.momentum_history]
        away_values = [state['global']['away'] for state in self.momentum_history]
        
        # Calculer les moyennes
        avg_home = sum(home_values) / len(home_values)
        avg_away = sum(away_values) / len(away_values)
        
        # Calculer la volatilité
        volatility = self._calculate_match_volatility()
        
        # Déterminer l'équipe dominante globale
        dominant_team = 'home' if avg_home > avg_away else 'away'
        dominance_percentage = max(avg_home, avg_away) / (avg_home + avg_away) * 100 if (avg_home + avg_away) > 0 else 50
        
        # Compter les périodes de momentum fort
        strong_momentum_periods = {
            'home': sum(1 for v in home_values if v > 0.7),
            'away': sum(1 for v in away_values if v > 0.7)
        }
        
        # Calculer le temps passé en avantage
        dominant_minutes = {
            'home': sum(1 for i in range(len(home_values)) if home_values[i] > away_values[i]),
            'away': sum(1 for i in range(len(away_values)) if away_values[i] > home_values[i])
        }
        
        # Calculer le pourcentage de temps dominant
        total_minutes = len(home_values)
        dominance_time_percentage = {
            'home': (dominant_minutes['home'] / total_minutes) * 100 if total_minutes > 0 else 0,
            'away': (dominant_minutes['away'] / total_minutes) * 100 if total_minutes > 0 else 0
        }
        
        return {
            'average_momentum': {
                'home': avg_home,
                'away': avg_away
            },
            'volatility': volatility,
            'momentum_shifts': len(self.momentum_shifts),
            'dominant_team': dominant_team,
            'dominance_percentage': dominance_percentage,
            'strong_momentum_periods': strong_momentum_periods,
            'dominance_minutes': dominant_minutes,
            'dominance_time_percentage': dominance_time_percentage
        }
    
    def _evaluate_momentum_efficiency(self):
        """Évaluer l'efficacité globale du momentum."""
        # Récupérer les données pertinentes
        momentum_goals = self.momentum_match_influence['momentum_goals']
        strong_momentum_periods = 0
        
        for state in self.momentum_history:
            if state['global']['home'] > 0.7 or state['global']['away'] > 0.7:
                strong_momentum_periods += 1
        
        # Calculer l'efficacité de base (buts / périodes)
        base_efficiency = momentum_goals / max(1, strong_momentum_periods // 5)  # Grouper par 5 minutes
        
        # Ajuster selon le nombre de shifts
        shift_factor = min(1.0, len(self.momentum_shifts) / 10)  # 10 shifts est considéré comme beaucoup
        
        # Calculer l'efficacité ajustée
        adjusted_efficiency = base_efficiency * (1.0 - (shift_factor * 0.5))
        
        # Limiter à une plage raisonnable
        normalized_efficiency = min(1.0, adjusted_efficiency * 2)  # Facteur arbitraire
        
        # Classifier l'efficacité
        if normalized_efficiency > 0.7:
            efficiency_category = 'high'
        elif normalized_efficiency > 0.4:
            efficiency_category = 'medium'
        else:
            efficiency_category = 'low'
        
        return {
            'value': normalized_efficiency,
            'category': efficiency_category,
            'momentum_goals': momentum_goals,
            'strong_momentum_periods': strong_momentum_periods // 5,
            'raw_efficiency': base_efficiency
        }
    
    def _identify_dominant_patterns(self):
        """Identifier les patterns de momentum dominants du match."""
        # Vérifier si nous avons détecté des patterns
        if not self.detected_patterns:
            return []
        
        # Compter les occurrences de chaque type de pattern
        pattern_counts = {}
        
        for pattern in self.detected_patterns:
            pattern_type = pattern['pattern']
            team = pattern['team']
            
            key = f"{pattern_type}_{team}"
            
            if key not in pattern_counts:
                pattern_counts[key] = {
                    'pattern': pattern_type,
                    'team': team,
                    'count': 0,
                    'avg_confidence': 0.0,
                    'confidences': []
                }
            
            pattern_counts[key]['count'] += 1
            pattern_counts[key]['confidences'].append(pattern['confidence'])
        
        # Calculer la confiance moyenne
        for key, data in pattern_counts.items():
            if data['confidences']:
                data['avg_confidence'] = sum(data['confidences']) / len(data['confidences'])
        
        # Convertir en liste et trier
        dominant_patterns = list(pattern_counts.values())
        dominant_patterns.sort(key=lambda x: (x['count'], x['avg_confidence']), reverse=True)
        
        # Limiter aux 5 plus dominants
        return dominant_patterns[:5]
    
    def _analyze_dimensional_distribution(self):
        """Analyser la distribution dimensionnelle du momentum."""
        # Initialiser les statistiques par dimension
        dimensional_stats = {dim: {'home': 0.0, 'away': 0.0, 'dominance': 'none'} 
                            for dim in self.momentum_dimensions}
        
        # Vérifier si nous avons assez de données
        if len(self.momentum_history) < 3:
            return dimensional_stats
        
        # Calculer les moyennes par dimension
        for dim in self.momentum_dimensions:
            home_values = [state['dimensions']['home'][dim] for state in self.momentum_history]
            away_values = [state['dimensions']['away'][dim] for state in self.momentum_history]
            
            avg_home = sum(home_values) / len(home_values)
            avg_away = sum(away_values) / len(away_values)
            
            dimensional_stats[dim]['home'] = avg_home
            dimensional_stats[dim]['away'] = avg_away
            dimensional_stats[dim]['dominance'] = 'home' if avg_home > avg_away else 'away'
            dimensional_stats[dim]['dominance_margin'] = abs(avg_home - avg_away)
        
        # Trier les dimensions par marge de dominance
        dimensional_ranking = [(dim, data['dominance_margin']) 
                              for dim, data in dimensional_stats.items()]
        dimensional_ranking.sort(key=lambda x: x[1], reverse=True)
        
        # Ajouter le classement à la distribution
        for i, (dim, _) in enumerate(dimensional_ranking):
            dimensional_stats[dim]['rank'] = i + 1
        
        return dimensional_stats
    
    def _generate_momentum_narrative(self):
        """Générer un résumé narratif de l'évolution du momentum."""
        # Vérifier si nous avons assez de données
        if len(self.momentum_history) < 10:
            return {
                'summary': "Données insuffisantes pour générer une narration complète du momentum",
                'key_moments': []
            }
        
        # Récupérer les statistiques générales
        momentum_stats = self._calculate_momentum_statistics()
        
        # Récupérer les phases cruciales
        crucial_phases = self._identify_crucial_match_phases()
        
        # Récupérer les moments critiques
        critical_moments = self.analyze_critical_moments()['critical_moments']
        
        # Construire un résumé général
        dominant_team = momentum_stats['dominant_team']
        dominance_percentage = momentum_stats['dominance_percentage']
        
        if dominant_team != 'none':
            summary = f"Le match a été globalement dominé en termes de momentum par l'équipe {dominant_team} "
            summary += f"({dominance_percentage:.1f}% du temps), "
        else:
            summary = "Le match a été équilibré en termes de momentum, "
        
        summary += f"avec {len(self.momentum_shifts)} changements significatifs de dynamique"
        
        if momentum_stats['volatility'] > 0.7:
            summary += " et une volatilité très élevée."
        elif momentum_stats['volatility'] > 0.4:
            summary += " et une volatilité modérée."
        else:
            summary += " et une volatilité relativement faible."
        
        # Ajouter des informations sur l'efficacité
        momentum_efficiency = self._evaluate_momentum_efficiency()
        
        if momentum_efficiency['value'] > 0.6:
            summary += f" Le momentum s'est traduit de manière efficace en résultats concrets, avec {momentum_efficiency['momentum_goals']} buts marqués durant des périodes de fort momentum."
        elif momentum_efficiency['value'] > 0.3:
            summary += f" Le momentum a eu une influence modérée sur le résultat, avec {momentum_efficiency['momentum_goals']} buts marqués durant des périodes de fort momentum."
        else:
            summary += f" Malgré les variations de momentum, celles-ci ont eu peu d'influence directe sur le résultat, avec seulement {momentum_efficiency['momentum_goals']} buts marqués durant des périodes de fort momentum."
        
        # Préparer le résultat
        narrative = {
            'summary': summary,
            'key_moments': []
        }
        
        # Ajouter les moments clés
        for moment in critical_moments[:5]:  # Limiter aux 5 plus importants
            narrative['key_moments'].append({
                'minute': moment.get('minute', moment.get('start_minute', 0)),
                'description': moment['description'],
                'significance': moment.get('significance', 0.5)
            })
        
        return narrative