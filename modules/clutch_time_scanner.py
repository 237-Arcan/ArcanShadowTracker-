"""
ClutchTimeScanner - Module de détection des moments décisifs dans un match.
Identifie et analyse les périodes de jeu cruciales où le résultat peut basculer.
"""

import numpy as np
import random
from datetime import datetime, timedelta
import json
import os

class ClutchTimeScanner:
    """
    ClutchTimeScanner - Analyse des moments décisifs dans un match.
    Détecte les périodes critiques où la pression est maximale et où les actions
    peuvent avoir un impact disproportionné sur le résultat final.
    """
    
    def __init__(self):
        """Initialise le module ClutchTimeScanner."""
        # Fenêtres de temps classiques pour les moments décisifs
        self.clutch_windows = {
            'end_first_half': {'start': 40, 'end': 45},     # Fin de première mi-temps
            'start_second_half': {'start': 45, 'end': 50},  # Début de seconde mi-temps
            'final_minutes': {'start': 85, 'end': 90},      # Dernières minutes
            'extra_time': {'start': 90, 'end': 95}          # Temps additionnel
        }
        
        # Facteurs qui amplifient l'importance d'un moment
        self.clutch_amplifiers = {
            'score_difference': {
                0: 1.0,    # Match nul - tension maximale
                1: 0.8,    # Différence d'un but - haute tension
                2: 0.5,    # Différence de deux buts - tension modérée
                3: 0.3     # Différence de trois buts ou plus - tension faible
            },
            'player_status': {
                'star_player': 0.3,       # Impact d'un joueur star
                'captain': 0.25,          # Impact du capitaine
                'super_sub': 0.2,         # Impact d'un super-sub
                'in_form_player': 0.15    # Impact d'un joueur en forme
            },
            'match_context': {
                'derby': 0.3,             # Contexte de derby
                'title_race': 0.35,       # Impact sur le titre
                'relegation_battle': 0.3, # Lutte pour le maintien
                'cup_elimination': 0.4    # Match à élimination directe
            }
        }
        
        # Évaluation des actions pendant les moments décisifs
        self.clutch_actions = {
            'goal': 1.0,                 # But
            'penalty_awarded': 0.9,      # Penalty accordé
            'penalty_saved': 0.95,       # Penalty arrêté
            'red_card': 0.85,            # Carton rouge
            'big_save': 0.8,             # Arrêt décisif
            'key_pass': 0.7,             # Passe décisive
            'counter_attack': 0.65,      # Contre-attaque
            'set_piece': 0.6,            # Coup de pied arrêté
            'defensive_error': 0.75,     # Erreur défensive
            'tactical_substitution': 0.5 # Changement tactique
        }
        
        # Historique des moments décisifs détectés
        self.clutch_moments_history = []
        
        # État actuel de l'analyse
        self.current_state = {
            'match_time': 0,
            'current_score': [0, 0],
            'active_clutch_period': False,
            'clutch_intensity': 0.0,
            'detected_moments': []
        }
    
    def analyze_match_state(self, match_data, live_events=None):
        """
        Analyser l'état actuel du match pour détecter les moments décisifs.
        
        Args:
            match_data (dict): Informations générales sur le match
            live_events (list, optional): Événements live du match
            
        Returns:
            dict: Analyse des moments décisifs détectés
        """
        # Extraire les informations pertinentes
        current_minute = self._get_match_minute(match_data, live_events)
        home_score = match_data.get('home_score', 0)
        away_score = match_data.get('away_score', 0)
        match_type = match_data.get('match_type', 'league')
        match_context = self._determine_match_context(match_data)
        
        # Mettre à jour l'état actuel
        self.current_state['match_time'] = current_minute
        self.current_state['current_score'] = [home_score, away_score]
        
        # Vérifier si nous sommes dans une fenêtre de temps décisive
        in_clutch_window, window_type = self._check_clutch_window(current_minute)
        
        # Calculer la différence de score
        score_diff = abs(home_score - away_score)
        
        # Déterminer l'intensité de base du moment
        base_intensity = 0.0
        if in_clutch_window:
            base_intensity = 0.6  # Valeur de base pour un moment dans une fenêtre décisive
            # Ajuster selon la différence de score
            if score_diff in self.clutch_amplifiers['score_difference']:
                base_intensity *= self.clutch_amplifiers['score_difference'][score_diff]
            else:
                base_intensity *= self.clutch_amplifiers['score_difference'][3]  # Différence de 3+ buts
            
            # Ajuster selon le contexte du match
            for context_type, context_value in match_context.items():
                if context_value and context_type in self.clutch_amplifiers['match_context']:
                    base_intensity += self.clutch_amplifiers['match_context'][context_type]
        
        # Vérifier les événements récents pour identifier des moments décisifs
        detected_moments = []
        if live_events:
            recent_events = [e for e in live_events if e.get('minute', 0) > current_minute - 5]
            for event in recent_events:
                event_type = event.get('type', '')
                minute = event.get('minute', 0)
                
                # Vérifier si l'action est décisive
                if event_type in self.clutch_actions:
                    action_value = self.clutch_actions[event_type]
                    
                    # Calculer l'intensité du moment décisif
                    moment_intensity = base_intensity * action_value
                    
                    # Amplifier selon les joueurs impliqués
                    player_info = event.get('player_info', {})
                    for status, amplifier in self.clutch_amplifiers['player_status'].items():
                        if player_info.get(status, False):
                            moment_intensity += amplifier
                    
                    # Si l'intensité est suffisante, c'est un moment décisif
                    if moment_intensity > 0.5:
                        detected_moment = {
                            'minute': minute,
                            'event_type': event_type,
                            'intensity': moment_intensity,
                            'players_involved': event.get('players_involved', []),
                            'description': event.get('description', ''),
                            'window_type': window_type if in_clutch_window else 'regular_play'
                        }
                        detected_moments.append(detected_moment)
                        
                        # Ajouter à l'historique
                        self.clutch_moments_history.append({
                            'timestamp': datetime.now().isoformat(),
                            'match_minute': minute,
                            'event_type': event_type,
                            'intensity': moment_intensity,
                            'match_id': match_data.get('id', '')
                        })
        
        # Mettre à jour l'état actuel
        self.current_state['active_clutch_period'] = in_clutch_window
        self.current_state['clutch_intensity'] = base_intensity
        self.current_state['detected_moments'] = detected_moments
        
        # Préparer le résultat
        result = {
            'match_time': current_minute,
            'in_clutch_period': in_clutch_window,
            'clutch_window_type': window_type if in_clutch_window else None,
            'clutch_intensity': base_intensity,
            'detected_moments': detected_moments,
            'score_state': {
                'home_score': home_score,
                'away_score': away_score,
                'score_difference': score_diff,
                'score_impact_factor': self.clutch_amplifiers['score_difference'].get(score_diff, 0.3)
            },
            'match_context_analysis': match_context
        }
        
        return result
    
    def predict_clutch_moments(self, match_data):
        """
        Prédire les moments potentiellement décisifs dans un match à venir.
        
        Args:
            match_data (dict): Informations sur le match
            
        Returns:
            dict: Prédiction des moments potentiellement décisifs
        """
        # Extraire les informations pertinentes
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        match_type = match_data.get('match_type', 'league')
        match_context = self._determine_match_context(match_data)
        
        # Déterminer les fenêtres de base
        predicted_windows = []
        for window_name, window_data in self.clutch_windows.items():
            # Probabilité de base que cette fenêtre contienne un moment décisif
            base_probability = 0.6
            
            # Ajuster selon le contexte
            for context_type, context_value in match_context.items():
                if context_value and context_type in self.clutch_amplifiers['match_context']:
                    base_probability += self.clutch_amplifiers['match_context'][context_type] * 0.5
            
            predicted_windows.append({
                'window_name': window_name,
                'start_minute': window_data['start'],
                'end_minute': window_data['end'],
                'probability': min(0.95, base_probability)  # Plafond à 95%
            })
        
        # Prédire les types d'actions potentiellement décisives
        predicted_actions = []
        for action_type, action_value in self.clutch_actions.items():
            if action_value > 0.7:  # Se concentrer sur les actions à haut impact
                predicted_actions.append({
                    'action_type': action_type,
                    'impact_factor': action_value,
                    'probability': action_value * 0.5  # Probabilité simplifiée
                })
        
        # Prédire l'impact des joueurs clés
        key_players_impact = []
        home_stars = match_data.get('home_team_key_players', [])
        away_stars = match_data.get('away_team_key_players', [])
        
        for player in home_stars + away_stars:
            player_status = self._determine_player_status(player)
            impact_factor = 0.0
            for status, amplifier in self.clutch_amplifiers['player_status'].items():
                if player_status.get(status, False):
                    impact_factor += amplifier
            
            if impact_factor > 0:
                key_players_impact.append({
                    'player_name': player.get('name', ''),
                    'team': player.get('team', ''),
                    'status': player_status,
                    'clutch_impact_factor': impact_factor
                })
        
        # Résultat final
        return {
            'predicted_clutch_windows': predicted_windows,
            'high_impact_actions': predicted_actions,
            'key_players_impact': key_players_impact,
            'match_context': match_context,
            'overall_clutch_probability': self._calculate_overall_clutch_probability(match_context)
        }
    
    def get_team_clutch_performance(self, team_data, recent_matches=10):
        """
        Analyser la performance d'une équipe dans les moments décisifs.
        
        Args:
            team_data (dict): Données historiques de l'équipe
            recent_matches (int): Nombre de matchs récents à considérer
            
        Returns:
            dict: Analyse de la performance dans les moments décisifs
        """
        # Extraire les informations pertinentes
        team_name = team_data.get('name', '')
        clutch_goals_scored = team_data.get('clutch_goals_scored', 0)
        clutch_goals_conceded = team_data.get('clutch_goals_conceded', 0)
        late_wins = team_data.get('late_wins', 0)
        late_draws = team_data.get('late_draws', 0)
        late_losses = team_data.get('late_losses', 0)
        comeback_wins = team_data.get('comeback_wins', 0)
        
        # Calculer les indicateurs de performance
        total_late_game_changes = late_wins + late_draws + late_losses
        
        if total_late_game_changes > 0:
            clutch_win_ratio = late_wins / total_late_game_changes
            clutch_points_secured = (late_wins * 3 + late_draws * 1) / (total_late_game_changes * 3)
        else:
            clutch_win_ratio = 0
            clutch_points_secured = 0
        
        # Différentiel de buts dans les moments décisifs
        clutch_goal_difference = clutch_goals_scored - clutch_goals_conceded
        
        # Calculer la note globale de "clutch performance"
        clutch_rating = 0.0
        if total_late_game_changes > 0:
            clutch_components = [
                clutch_win_ratio * 0.3,
                clutch_points_secured * 0.3,
                (clutch_goal_difference / total_late_game_changes * 0.1 + 0.5) * 0.2,  # Normaliser autour de 0.5
                (comeback_wins / max(1, total_late_game_changes / 2)) * 0.2  # Max pour éviter division par zéro
            ]
            clutch_rating = sum(clutch_components)
        
        # Classifier la performance
        clutch_category = 'average'
        if clutch_rating > 0.7:
            clutch_category = 'excellent'
        elif clutch_rating > 0.6:
            clutch_category = 'good'
        elif clutch_rating < 0.4:
            clutch_category = 'poor'
        
        return {
            'team_name': team_name,
            'clutch_rating': clutch_rating,
            'category': clutch_category,
            'clutch_win_ratio': clutch_win_ratio,
            'clutch_points_secured_ratio': clutch_points_secured,
            'clutch_goal_difference': clutch_goal_difference,
            'comeback_factor': comeback_wins / max(1, total_late_game_changes),
            'raw_stats': {
                'clutch_goals_scored': clutch_goals_scored,
                'clutch_goals_conceded': clutch_goals_conceded,
                'late_wins': late_wins,
                'late_draws': late_draws,
                'late_losses': late_losses,
                'comeback_wins': comeback_wins
            }
        }
    
    def _check_clutch_window(self, minute):
        """Vérifier si la minute actuelle est dans une fenêtre de temps décisive."""
        for window_name, window_data in self.clutch_windows.items():
            if window_data['start'] <= minute <= window_data['end']:
                return True, window_name
        return False, None
    
    def _determine_match_context(self, match_data):
        """Déterminer le contexte du match pour ajuster l'analyse."""
        context = {
            'derby': False,
            'title_race': False,
            'relegation_battle': False,
            'cup_elimination': False
        }
        
        # Vérifier le type de match
        match_type = match_data.get('match_type', 'league')
        if match_type == 'cup' or match_type == 'knockout':
            context['cup_elimination'] = True
        
        # Vérifier les enjeux spécifiques
        context['title_race'] = match_data.get('title_race', False)
        context['relegation_battle'] = match_data.get('relegation_battle', False)
        
        # Vérifier si c'est un derby
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        context['derby'] = self._is_derby(home_team, away_team)
        
        return context
    
    def _determine_player_status(self, player):
        """Déterminer le statut d'un joueur pour l'analyse de son impact potentiel."""
        status = {
            'star_player': False,
            'captain': False,
            'super_sub': False,
            'in_form_player': False
        }
        
        # Vérifier les attributs du joueur
        if player.get('is_star', False) or player.get('rating', 0) > 85:
            status['star_player'] = True
        
        if player.get('is_captain', False):
            status['captain'] = True
        
        if player.get('super_sub', False) or player.get('goals_as_sub', 0) > 2:
            status['super_sub'] = True
        
        if player.get('current_form', 0) > 7.5 or player.get('goals_last_5', 0) > 2:
            status['in_form_player'] = True
        
        return status
    
    def _is_derby(self, home_team, away_team):
        """Déterminer si le match est un derby."""
        # Liste simplifiée de derbies connus
        known_derbies = [
            ('Manchester United', 'Manchester City'),
            ('Liverpool', 'Everton'),
            ('Arsenal', 'Tottenham'),
            ('AC Milan', 'Inter Milan'),
            ('Real Madrid', 'Atletico Madrid'),
            ('Barcelona', 'Espanyol'),
            ('Boca Juniors', 'River Plate')
        ]
        
        # Vérifier les derbies connus
        for team1, team2 in known_derbies:
            if (home_team == team1 and away_team == team2) or (home_team == team2 and away_team == team1):
                return True
        
        # Vérifier si les équipes partagent la même ville (analyse simplifiée)
        home_city = home_team.split()[0]  # Première partie du nom
        if len(home_city) > 3 and home_city in away_team:
            return True
        
        return False
    
    def _calculate_overall_clutch_probability(self, match_context):
        """Calculer la probabilité globale d'avoir des moments décisifs dans le match."""
        base_probability = 0.6  # Probabilité de base
        
        # Ajuster selon le contexte
        context_factor = 0.0
        for context_type, context_value in match_context.items():
            if context_value and context_type in self.clutch_amplifiers['match_context']:
                context_factor += self.clutch_amplifiers['match_context'][context_type]
        
        overall_probability = base_probability + (context_factor * 0.3)
        return min(0.95, overall_probability)  # Plafond à 95%
    
    def _get_match_minute(self, match_data, live_events=None):
        """Déterminer la minute actuelle du match."""
        if live_events and len(live_events) > 0:
            latest_event = max(live_events, key=lambda e: e.get('minute', 0))
            return latest_event.get('minute', 0)
        
        # Si pas d'événements, utiliser le temps de match fourni
        return match_data.get('current_minute', 0)