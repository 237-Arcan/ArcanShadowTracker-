"""
MomentumShiftTracker - Module de suivi des changements d'élan dans un match.
Analyse les basculements psychologiques et dynamiques pour détecter les shifts de momentum.
"""

import numpy as np
import random
from datetime import datetime, timedelta
import json
import os
from collections import deque

class MomentumShiftTracker:
    """
    MomentumShiftTracker - Détection et analyse des changements d'élan pendant un match.
    Identifie les moments où la dynamique du match change et quantifie ces basculements.
    """
    
    def __init__(self):
        """Initialise le module MomentumShiftTracker."""
        # Facteurs qui influencent le momentum
        self.momentum_factors = {
            'goal': 0.5,                  # Impact d'un but
            'red_card': 0.4,              # Impact d'un carton rouge
            'penalty_awarded': 0.35,      # Impact d'un penalty accordé
            'penalty_missed': -0.3,       # Impact d'un penalty raté
            'big_save': 0.25,             # Impact d'un arrêt important
            'dangerous_attack': 0.15,     # Impact d'une attaque dangereuse
            'yellow_card': 0.1,           # Impact d'un carton jaune
            'possession_dominance': 0.2,  # Impact d'une domination de possession
            'substitution': 0.15,         # Impact d'un changement tactique
            'missed_chance': -0.15        # Impact d'une occasion manquée
        }
        
        # Paramètres du modèle de momentum
        self.momentum_params = {
            'decay_rate': 0.95,           # Taux de décroissance du momentum
            'accumulation_threshold': 0.3,  # Seuil d'accumulation pour un shift
            'equilibrium_value': 0.0,     # Valeur d'équilibre (neutre)
            'max_value': 1.0,             # Valeur maximale de momentum
            'min_value': -1.0             # Valeur minimale de momentum
        }
        
        # État actuel du momentum
        self.current_momentum = {
            'home_team': 0.0,             # Momentum de l'équipe à domicile
            'away_team': 0.0,             # Momentum de l'équipe extérieure
            'dominant_team': None,        # Équipe dominante actuellement
            'shift_in_progress': False,   # Indicateur de shift en cours
            'last_update': None           # Timestamp de la dernière mise à jour
        }
        
        # Historique du momentum
        self.momentum_history = []
        
        # Historique des shifts détectés
        self.shift_history = []
        
        # Buffer d'événements récents pour analyser les tendances
        self.recent_events_buffer = deque(maxlen=15)
        
        # Compteurs d'événements positifs/négatifs récents par équipe
        self.recent_positive_events = {'home': 0, 'away': 0}
        self.recent_negative_events = {'home': 0, 'away': 0}
    
    def track_live_momentum(self, match_data, live_events=None):
        """
        Suivre et analyser le momentum en temps réel pendant un match.
        
        Args:
            match_data (dict): Informations générales sur le match
            live_events (list, optional): Événements live du match
            
        Returns:
            dict: Analyse du momentum actuel et des shifts détectés
        """
        # Extraire les informations pertinentes
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        current_minute = self._get_match_minute(match_data, live_events)
        
        # Initialiser le timestamp de la dernière mise à jour si nécessaire
        if self.current_momentum['last_update'] is None:
            self.current_momentum['last_update'] = datetime.now()
        
        # Traiter les événements récents pour mettre à jour le momentum
        momentum_changes = {'home': 0.0, 'away': 0.0}
        detected_shifts = []
        
        if live_events:
            # Filtrer les événements récents (depuis la dernière mise à jour)
            last_momentum_update = self.current_momentum['last_update']
            if isinstance(last_momentum_update, str):
                last_momentum_update = datetime.fromisoformat(last_momentum_update)
            
            recent_events = []
            for event in live_events:
                event_time = event.get('timestamp', None)
                if event_time:
                    if isinstance(event_time, str):
                        event_time = datetime.fromisoformat(event_time)
                    if event_time > last_momentum_update:
                        recent_events.append(event)
                
                # Si pas de timestamp, se baser sur la minute de jeu
                event_minute = event.get('minute', 0)
                last_processed_minute = self.momentum_history[-1]['minute'] if self.momentum_history else 0
                if event_minute > last_processed_minute:
                    recent_events.append(event)
            
            # Ajouter les événements au buffer et calculer les changements de momentum
            for event in recent_events:
                self.recent_events_buffer.append(event)
                
                event_type = event.get('type', '')
                team = event.get('team', 'home')  # Par défaut, considérer l'équipe à domicile
                impact = self._calculate_event_impact(event, match_data)
                
                # Appliquer l'impact au momentum
                if team == 'home':
                    momentum_changes['home'] += impact
                    if impact > 0:
                        self.recent_positive_events['home'] += 1
                    elif impact < 0:
                        self.recent_negative_events['home'] += 1
                else:
                    momentum_changes['away'] += impact
                    if impact > 0:
                        self.recent_positive_events['away'] += 1
                    elif impact < 0:
                        self.recent_negative_events['away'] += 1
        
        # Appliquer la décroissance naturelle du momentum
        time_delta = (datetime.now() - last_momentum_update).total_seconds() / 60  # En minutes
        decay_factor = self.momentum_params['decay_rate'] ** time_delta
        
        old_home_momentum = self.current_momentum['home_team']
        old_away_momentum = self.current_momentum['away_team']
        
        # Calculer le nouveau momentum
        new_home_momentum = old_home_momentum * decay_factor + momentum_changes['home']
        new_away_momentum = old_away_momentum * decay_factor + momentum_changes['away']
        
        # Limiter aux valeurs min/max
        new_home_momentum = max(self.momentum_params['min_value'], 
                               min(self.momentum_params['max_value'], new_home_momentum))
        new_away_momentum = max(self.momentum_params['min_value'], 
                               min(self.momentum_params['max_value'], new_away_momentum))
        
        # Détecter les shifts de momentum
        old_dominant = self.current_momentum['dominant_team']
        new_dominant = 'home' if new_home_momentum > new_away_momentum else 'away'
        
        # Détecter un changement de team dominante
        if old_dominant != new_dominant and old_dominant is not None:
            # Vérifier si c'est un shift significatif
            momentum_diff = abs(new_home_momentum - new_away_momentum)
            if momentum_diff > self.momentum_params['accumulation_threshold']:
                shift = {
                    'minute': current_minute,
                    'timestamp': datetime.now().isoformat(),
                    'from_team': old_dominant,
                    'to_team': new_dominant,
                    'shift_strength': momentum_diff,
                    'trigger_events': list(self.recent_events_buffer)[-3:],  # 3 derniers événements
                    'match_id': match_data.get('id', '')
                }
                detected_shifts.append(shift)
                self.shift_history.append(shift)
        
        # Mettre à jour l'état actuel du momentum
        self.current_momentum['home_team'] = new_home_momentum
        self.current_momentum['away_team'] = new_away_momentum
        self.current_momentum['dominant_team'] = new_dominant
        self.current_momentum['shift_in_progress'] = (len(detected_shifts) > 0)
        self.current_momentum['last_update'] = datetime.now().isoformat()
        
        # Enregistrer dans l'historique
        self.momentum_history.append({
            'timestamp': datetime.now().isoformat(),
            'minute': current_minute,
            'home_momentum': new_home_momentum,
            'away_momentum': new_away_momentum,
            'dominant_team': new_dominant,
            'recent_events': len(recent_events) if 'recent_events' in locals() else 0
        })
        
        # Calculer les métriques d'élan
        momentum_metrics = self._calculate_momentum_metrics()
        
        # Réinitialiser les compteurs d'événements si nécessaire
        if self.momentum_history and len(self.momentum_history) % 5 == 0:  # Tous les 5 enregistrements
            self.recent_positive_events = {'home': 0, 'away': 0}
            self.recent_negative_events = {'home': 0, 'away': 0}
        
        # Préparer le résultat
        result = {
            'match_time': current_minute,
            'current_momentum': {
                'home_team': {
                    'name': home_team,
                    'value': new_home_momentum,
                    'trend': 'rising' if new_home_momentum > old_home_momentum else 'falling',
                    'recent_positive_events': self.recent_positive_events['home'],
                    'recent_negative_events': self.recent_negative_events['home']
                },
                'away_team': {
                    'name': away_team,
                    'value': new_away_momentum,
                    'trend': 'rising' if new_away_momentum > old_away_momentum else 'falling',
                    'recent_positive_events': self.recent_positive_events['away'],
                    'recent_negative_events': self.recent_negative_events['away']
                }
            },
            'dominant_team': {
                'name': home_team if new_dominant == 'home' else away_team,
                'side': new_dominant,
                'dominance_margin': abs(new_home_momentum - new_away_momentum)
            },
            'detected_shifts': detected_shifts,
            'momentum_metrics': momentum_metrics,
            'momentum_stability': self._calculate_momentum_stability()
        }
        
        return result
    
    def predict_momentum_pattern(self, team_data, opponent_data=None):
        """
        Prédire les patterns de momentum typiques pour une équipe.
        
        Args:
            team_data (dict): Données historiques de l'équipe
            opponent_data (dict, optional): Données de l'adversaire
            
        Returns:
            dict: Patterns de momentum prédits
        """
        # Extraire les informations pertinentes
        team_name = team_data.get('name', '')
        team_style = team_data.get('playing_style', 'balanced')
        fast_starter = team_data.get('fast_starter', False)
        strong_finisher = team_data.get('strong_finisher', False)
        momentum_sensitivity = team_data.get('momentum_sensitivity', 0.5)  # 0-1, réactivité au momentum
        
        # Patterns de momentum typiques selon le style de jeu
        momentum_patterns = {
            'attacking': {
                'initial_momentum': 0.3,
                'midgame_dip': True,
                'strong_start': True,
                'momentum_consistency': 0.4
            },
            'defensive': {
                'initial_momentum': -0.1,
                'midgame_dip': False,
                'strong_start': False,
                'momentum_consistency': 0.7
            },
            'possession': {
                'initial_momentum': 0.2,
                'midgame_dip': False,
                'strong_start': False,
                'momentum_consistency': 0.6
            },
            'counter': {
                'initial_momentum': -0.2,
                'midgame_dip': True,
                'strong_start': False,
                'momentum_consistency': 0.3
            },
            'balanced': {
                'initial_momentum': 0.0,
                'midgame_dip': False,
                'strong_start': False,
                'momentum_consistency': 0.5
            }
        }
        
        # Obtenir le pattern de base selon le style
        base_pattern = momentum_patterns.get(team_style, momentum_patterns['balanced'])
        
        # Ajuster selon les caractéristiques de l'équipe
        if fast_starter:
            base_pattern['initial_momentum'] += 0.2
            base_pattern['strong_start'] = True
        
        if strong_finisher:
            base_pattern['midgame_dip'] = True
        
        # Prédire les périodes de fort momentum
        high_momentum_periods = []
        
        if base_pattern['strong_start']:
            high_momentum_periods.append({
                'start_minute': 1,
                'end_minute': 15,
                'expected_strength': base_pattern['initial_momentum'] + 0.2,
                'description': 'Forte entame de match'
            })
        
        if strong_finisher:
            high_momentum_periods.append({
                'start_minute': 75,
                'end_minute': 90,
                'expected_strength': 0.4,
                'description': 'Fort finish en fin de match'
            })
        
        # Moment de vulnérabilité si midgame_dip
        vulnerable_periods = []
        if base_pattern['midgame_dip']:
            vulnerable_periods.append({
                'start_minute': 30,
                'end_minute': 45,
                'vulnerability_level': 0.3,
                'description': 'Baisse d\'intensité avant la mi-temps'
            })
        
        # Impact des événements critiques
        event_impact = {
            'goal_conceded': momentum_sensitivity * 0.7,  # Baisse de momentum en cas de but encaissé
            'red_card': momentum_sensitivity * 0.9,       # Baisse en cas de carton rouge
            'comeback_potential': self._calculate_comeback_potential(team_data)
        }
        
        # Considérer l'adversaire si fourni
        opponent_factor = None
        if opponent_data:
            opponent_style = opponent_data.get('playing_style', 'balanced')
            opponent_momentum_sensitivity = opponent_data.get('momentum_sensitivity', 0.5)
            
            # Analyser la compatibilité/conflit des styles
            style_match = self._analyze_style_compatibility(team_style, opponent_style)
            
            opponent_factor = {
                'name': opponent_data.get('name', ''),
                'style_compatibility': style_match,
                'relative_momentum_sensitivity': momentum_sensitivity / max(0.1, opponent_momentum_sensitivity),
                'predicted_momentum_battle': style_match['predicted_momentum_pattern']
            }
        
        return {
            'team_name': team_name,
            'predicted_pattern': base_pattern,
            'high_momentum_periods': high_momentum_periods,
            'vulnerable_periods': vulnerable_periods,
            'event_impact_factors': event_impact,
            'opponent_analysis': opponent_factor,
            'overall_momentum_consistency': base_pattern['momentum_consistency']
        }
    
    def analyze_momentum_trends(self, match_history):
        """
        Analyser les tendances de momentum à partir de l'historique des matchs.
        
        Args:
            match_history (list): Historique des matchs avec données de momentum
            
        Returns:
            dict: Analyse des tendances de momentum
        """
        if not match_history or len(match_history) == 0:
            return {
                'status': 'error',
                'message': 'Historique de matchs vide'
            }
        
        # Extraire les patterns de momentum de l'historique
        momentum_patterns = []
        shifts_by_period = {'0-15': 0, '16-30': 0, '31-45': 0, 
                          '46-60': 0, '61-75': 0, '76-90': 0}
        
        total_shifts = 0
        comeback_matches = 0
        consistent_momentum_matches = 0
        
        for match in match_history:
            match_shifts = match.get('momentum_shifts', [])
            total_shifts += len(match_shifts)
            
            # Classer les shifts par période
            for shift in match_shifts:
                minute = shift.get('minute', 0)
                period = self._get_period_for_minute(minute)
                if period in shifts_by_period:
                    shifts_by_period[period] += 1
            
            # Vérifier s'il y a eu un comeback
            if self._has_comeback(match):
                comeback_matches += 1
            
            # Vérifier la consistance du momentum
            if self._has_consistent_momentum(match):
                consistent_momentum_matches += 1
            
            # Extraire le pattern de momentum
            momentum_pattern = self._extract_momentum_pattern(match)
            if momentum_pattern:
                momentum_patterns.append(momentum_pattern)
        
        # Calculer les statistiques
        avg_shifts_per_match = total_shifts / len(match_history)
        comeback_ratio = comeback_matches / len(match_history)
        consistency_ratio = consistent_momentum_matches / len(match_history)
        
        # Identifier les périodes critiques
        critical_periods = []
        for period, count in shifts_by_period.items():
            if count > avg_shifts_per_match:
                critical_periods.append({
                    'period': period,
                    'shift_count': count,
                    'shift_percentage': count / total_shifts if total_shifts > 0 else 0
                })
        
        # Analyser les patterns communs
        common_patterns = self._identify_common_patterns(momentum_patterns)
        
        return {
            'match_count': len(match_history),
            'total_momentum_shifts': total_shifts,
            'avg_shifts_per_match': avg_shifts_per_match,
            'shifts_by_period': shifts_by_period,
            'critical_periods': critical_periods,
            'comeback_stats': {
                'comeback_matches': comeback_matches,
                'comeback_ratio': comeback_ratio
            },
            'momentum_consistency': {
                'consistent_matches': consistent_momentum_matches,
                'consistency_ratio': consistency_ratio
            },
            'common_momentum_patterns': common_patterns
        }
    
    def _calculate_event_impact(self, event, match_data):
        """Calculer l'impact d'un événement sur le momentum."""
        event_type = event.get('type', '')
        team = event.get('team', 'home')
        minute = event.get('minute', 0)
        
        # Impact de base selon le type d'événement
        base_impact = self.momentum_factors.get(event_type, 0.0)
        
        # Ajuster l'impact selon le moment du match
        time_factor = 1.0
        if minute < 10:  # Début de match
            time_factor = 1.2
        elif minute > 80:  # Fin de match
            time_factor = 1.5
        elif 40 <= minute <= 45 or 85 <= minute <= 90:  # Fin de mi-temps
            time_factor = 1.3
        
        # Ajuster l'impact selon le score actuel
        score_factor = 1.0
        home_score = match_data.get('home_score', 0)
        away_score = match_data.get('away_score', 0)
        
        score_diff = home_score - away_score if team == 'home' else away_score - home_score
        if score_diff < 0:  # L'équipe est menée
            score_factor = 1.3
        elif score_diff > 1:  # L'équipe mène par plus d'un but
            score_factor = 0.8
        
        # Calculer l'impact final
        impact = base_impact * time_factor * score_factor
        
        # Inverser l'impact pour l'équipe adverse
        if team != 'home' and event_type in self.momentum_factors:
            impact = -impact
        
        return impact
    
    def _calculate_momentum_metrics(self):
        """Calculer des métriques basées sur l'historique du momentum."""
        if not self.momentum_history or len(self.momentum_history) < 2:
            return {
                'volatility': 0.0,
                'trend_strength': 0.0,
                'momentum_balance': 0.0
            }
        
        # Calculer la volatilité du momentum
        momentum_changes = []
        for i in range(1, len(self.momentum_history)):
            prev = self.momentum_history[i-1]
            curr = self.momentum_history[i]
            
            home_change = abs(curr['home_momentum'] - prev['home_momentum'])
            away_change = abs(curr['away_momentum'] - prev['away_momentum'])
            
            momentum_changes.append(max(home_change, away_change))
        
        volatility = sum(momentum_changes) / len(momentum_changes) if momentum_changes else 0.0
        
        # Calculer la force de la tendance actuelle
        recent_history = self.momentum_history[-5:] if len(self.momentum_history) >= 5 else self.momentum_history
        
        home_values = [entry['home_momentum'] for entry in recent_history]
        away_values = [entry['away_momentum'] for entry in recent_history]
        
        home_trend = self._calculate_trend_strength(home_values)
        away_trend = self._calculate_trend_strength(away_values)
        
        trend_strength = max(abs(home_trend), abs(away_trend))
        
        # Calculer l'équilibre global du momentum
        latest = self.momentum_history[-1]
        momentum_balance = latest['home_momentum'] - latest['away_momentum']
        
        return {
            'volatility': volatility,
            'trend_strength': trend_strength,
            'momentum_balance': momentum_balance,
            'home_trend': home_trend,
            'away_trend': away_trend
        }
    
    def _calculate_trend_strength(self, values):
        """Calculer la force d'une tendance à partir d'une série de valeurs."""
        if len(values) < 2:
            return 0.0
        
        # Régression linéaire simple
        x = list(range(len(values)))
        x_mean = sum(x) / len(x)
        y_mean = sum(values) / len(values)
        
        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(len(values)))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(len(values)))
        
        slope = numerator / denominator if denominator != 0 else 0
        
        return slope
    
    def _calculate_momentum_stability(self):
        """Calculer la stabilité du momentum actuel."""
        if not self.momentum_history or len(self.momentum_history) < 3:
            return 0.5  # Valeur par défaut si pas assez d'historique
        
        # Utiliser les données récentes
        recent_history = self.momentum_history[-5:] if len(self.momentum_history) >= 5 else self.momentum_history
        
        # Calculer la variance du momentum
        home_variance = np.var([entry['home_momentum'] for entry in recent_history])
        away_variance = np.var([entry['away_momentum'] for entry in recent_history])
        
        # Une faible variance indique une plus grande stabilité
        combined_variance = (home_variance + away_variance) / 2
        
        # Convertir en score de stabilité (inverse de la variance, normalisé)
        stability = 1 / (1 + 5 * combined_variance)  # Le facteur 5 est arbitraire pour normaliser
        
        return stability
    
    def _get_period_for_minute(self, minute):
        """Convertir une minute en période de match."""
        if 0 <= minute <= 15:
            return '0-15'
        elif 16 <= minute <= 30:
            return '16-30'
        elif 31 <= minute <= 45:
            return '31-45'
        elif 46 <= minute <= 60:
            return '46-60'
        elif 61 <= minute <= 75:
            return '61-75'
        elif 76 <= minute <= 90:
            return '76-90'
        else:
            return 'extra_time'
    
    def _has_comeback(self, match):
        """Vérifier si un match a eu un comeback."""
        # Un comeback est généralement défini comme une équipe qui était menée
        # et qui a finalement gagné ou fait match nul
        
        # Logique simplifiée ici - dans un système réel, nous examinerions le déroulement
        # complet du match et des buts
        
        return match.get('had_comeback', False)
    
    def _has_consistent_momentum(self, match):
        """Vérifier si le momentum était consistent pendant le match."""
        # Un momentum consistent signifie qu'une équipe a gardé le momentum
        # pendant la majeure partie du match
        
        momentum_shifts = match.get('momentum_shifts', [])
        
        # Peu de shifts indique un momentum consistent
        return len(momentum_shifts) <= 2  # Seuil arbitraire
    
    def _extract_momentum_pattern(self, match):
        """Extraire le pattern de momentum d'un match."""
        # Pattern = comment le momentum a évolué pendant les différentes phases du match
        
        momentum_data = match.get('momentum_data', {})
        if not momentum_data:
            return None
        
        # Simplification - dans un système réel, nous aurions des données plus détaillées
        return {
            'match_id': match.get('id', ''),
            'early_game': momentum_data.get('early_game', 0),
            'mid_game': momentum_data.get('mid_game', 0),
            'late_game': momentum_data.get('late_game', 0),
            'dominant_team': momentum_data.get('dominant_team', None),
            'pattern_type': momentum_data.get('pattern_type', 'unknown')
        }
    
    def _identify_common_patterns(self, patterns):
        """Identifier les patterns de momentum communs."""
        if not patterns:
            return []
        
        # Compteur simplifié des types de patterns
        pattern_counts = {}
        
        for pattern in patterns:
            pattern_type = pattern.get('pattern_type', 'unknown')
            if pattern_type in pattern_counts:
                pattern_counts[pattern_type] += 1
            else:
                pattern_counts[pattern_type] = 1
        
        # Trier par fréquence
        sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {'pattern_type': p_type, 'frequency': count, 'percentage': count / len(patterns)}
            for p_type, count in sorted_patterns
        ]
    
    def _calculate_comeback_potential(self, team_data):
        """Calculer le potentiel de comeback d'une équipe."""
        comebacks_made = team_data.get('comebacks_made', 0)
        matches_losing = team_data.get('matches_when_losing', 1)  # Éviter division par zéro
        
        comeback_ratio = comebacks_made / matches_losing if matches_losing > 0 else 0
        
        mental_strength = team_data.get('mental_strength', 0.5)  # 0-1
        
        return (comeback_ratio * 0.7) + (mental_strength * 0.3)
    
    def _analyze_style_compatibility(self, team_style, opponent_style):
        """Analyser la compatibilité des styles de jeu pour le momentum."""
        # Table de compatibilité des styles
        style_compatibility = {
            'attacking': {
                'attacking': {'momentum_swings': 'high', 'predicted_momentum_pattern': 'volatile'},
                'defensive': {'momentum_swings': 'low', 'predicted_momentum_pattern': 'grinding'},
                'possession': {'momentum_swings': 'medium', 'predicted_momentum_pattern': 'contested'},
                'counter': {'momentum_swings': 'high', 'predicted_momentum_pattern': 'end-to-end'},
                'balanced': {'momentum_swings': 'medium', 'predicted_momentum_pattern': 'balanced'}
            },
            'defensive': {
                'attacking': {'momentum_swings': 'low', 'predicted_momentum_pattern': 'tactical'},
                'defensive': {'momentum_swings': 'very_low', 'predicted_momentum_pattern': 'stalemate'},
                'possession': {'momentum_swings': 'low', 'predicted_momentum_pattern': 'cautious'},
                'counter': {'momentum_swings': 'medium', 'predicted_momentum_pattern': 'defensive_battle'},
                'balanced': {'momentum_swings': 'low', 'predicted_momentum_pattern': 'contain'}
            },
            'possession': {
                'attacking': {'momentum_swings': 'medium', 'predicted_momentum_pattern': 'technical'},
                'defensive': {'momentum_swings': 'low', 'predicted_momentum_pattern': 'methodical'},
                'possession': {'momentum_swings': 'low', 'predicted_momentum_pattern': 'chess_match'},
                'counter': {'momentum_swings': 'medium', 'predicted_momentum_pattern': 'tactical_battle'},
                'balanced': {'momentum_swings': 'low', 'predicted_momentum_pattern': 'controlled'}
            },
            'counter': {
                'attacking': {'momentum_swings': 'high', 'predicted_momentum_pattern': 'counter_punch'},
                'defensive': {'momentum_swings': 'medium', 'predicted_momentum_pattern': 'cagey'},
                'possession': {'momentum_swings': 'medium', 'predicted_momentum_pattern': 'break_and_build'},
                'counter': {'momentum_swings': 'high', 'predicted_momentum_pattern': 'waiting_game'},
                'balanced': {'momentum_swings': 'medium', 'predicted_momentum_pattern': 'opportunistic'}
            },
            'balanced': {
                'attacking': {'momentum_swings': 'medium', 'predicted_momentum_pattern': 'adaptable'},
                'defensive': {'momentum_swings': 'low', 'predicted_momentum_pattern': 'strategic'},
                'possession': {'momentum_swings': 'low', 'predicted_momentum_pattern': 'calculated'},
                'counter': {'momentum_swings': 'medium', 'predicted_momentum_pattern': 'flexible'},
                'balanced': {'momentum_swings': 'medium', 'predicted_momentum_pattern': 'even_contest'}
            }
        }
        
        # Obtenir la compatibilité selon les styles
        if team_style in style_compatibility and opponent_style in style_compatibility[team_style]:
            return style_compatibility[team_style][opponent_style]
        
        # Par défaut
        return {'momentum_swings': 'medium', 'predicted_momentum_pattern': 'standard'}
    
    def _get_match_minute(self, match_data, live_events=None):
        """Déterminer la minute actuelle du match."""
        if live_events and len(live_events) > 0:
            latest_event = max(live_events, key=lambda e: e.get('minute', 0))
            return latest_event.get('minute', 0)
        
        # Si pas d'événements, utiliser le temps de match fourni
        return match_data.get('current_minute', 0)