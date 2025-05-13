"""
CrowdPressureIndex - Module d'analyse de l'influence du public et de l'ambiance.
Quantifie l'impact de la pression du public sur la performance des équipes.
"""

import numpy as np
import random
from datetime import datetime, timedelta
import json
import os

class CrowdPressureIndex:
    """
    CrowdPressureIndex - Analyse la pression du public et l'ambiance du stade.
    Mesure quantitativement l'influence des supporters sur les joueurs et l'arbitre.
    """
    
    def __init__(self):
        """Initialise le module CrowdPressureIndex."""
        # Facteurs d'impact du public
        self.pressure_factors = {
            'home_advantage': 0.65,  # Impact de l'avantage du terrain
            'crowd_size': 0.4,       # Impact du nombre de spectateurs
            'fan_intensity': 0.55,   # Impact de l'intensité des supporters
            'stadium_acoustics': 0.3,  # Impact de l'acoustique du stade
            'rivalry_boost': 0.7,    # Amplification lors des derbies
            'historical_impact': 0.35  # Impact historique du public sur ce terrain
        }
        
        # Courbes de pression selon le contexte de match
        self.pressure_curves = {
            'normal_match': [0.3, 0.4, 0.5, 0.6, 0.7, 0.65, 0.6, 0.7, 0.8],  # Évolution standard
            'high_stakes': [0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0],  # Enjeu important
            'derby': [0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.95, 0.98, 1.0]  # Derby local
        }
        
        # Zones du terrain plus sensibles à la pression
        self.pressure_sensitive_zones = {
            'penalty_area': 0.9,     # Surface de réparation
            'goalmouth': 1.0,        # Devant le but
            'referee_proximity': 0.8  # Proximité de l'arbitre
        }
        
        # Effets mesurables de la pression
        self.pressure_effects = {
            'referee_bias': 0.0,       # Biais arbitral (initialisé à 0)
            'home_boost': 0.0,         # Boost pour l'équipe à domicile
            'away_stress': 0.0,        # Stress pour l'équipe extérieure
            'momentum_amplifier': 0.0  # Amplification du momentum
        }
        
        # Historique des mesures de pression
        self.pressure_history = []
        
        # État actuel de l'analyse
        self.current_state = {
            'match_time': 0,           # Minute de jeu
            'crowd_intensity': 0.5,    # Intensité actuelle du public
            'critical_moments': [],    # Moments critiques identifiés
            'pressure_index': 0.0      # Indice de pression actuel
        }
    
    def analyze_crowd_pressure(self, match_data, live_events=None):
        """
        Analyse la pression du public et son influence sur le match.
        
        Args:
            match_data (dict): Informations générales sur le match
            live_events (list, optional): Événements live du match
            
        Returns:
            dict: Analyse de la pression du public et son impact
        """
        # Extraire les informations pertinentes
        stadium = match_data.get('stadium', '')
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        attendance = match_data.get('attendance', 0)
        stadium_capacity = match_data.get('stadium_capacity', 0)
        match_type = match_data.get('match_type', 'league')
        
        # Calculer les coefficients de base
        attendance_ratio = attendance / stadium_capacity if stadium_capacity > 0 else 0.5
        is_derby = self._is_derby(home_team, away_team)
        match_importance = self._calculate_match_importance(match_data)
        
        # Déterminer la courbe de pression applicable
        pressure_curve = 'normal_match'
        if match_importance > 0.7:
            pressure_curve = 'high_stakes'
        if is_derby:
            pressure_curve = 'derby'
        
        # Mise à jour de l'état actuel
        current_minute = self._get_match_minute(match_data, live_events)
        self.current_state['match_time'] = current_minute
        
        # Calculer l'intensité du public
        crowd_intensity = self._calculate_crowd_intensity(
            current_minute, 
            attendance_ratio, 
            is_derby, 
            match_importance,
            live_events
        )
        self.current_state['crowd_intensity'] = crowd_intensity
        
        # Calculer l'indice de pression global
        pressure_index = self._calculate_pressure_index(
            crowd_intensity,
            self.pressure_curves[pressure_curve],
            current_minute
        )
        self.current_state['pressure_index'] = pressure_index
        
        # Calculer les effets de la pression
        self._calculate_pressure_effects(
            pressure_index,
            is_derby,
            match_importance,
            current_minute
        )
        
        # Identifier les moments critiques
        if live_events:
            critical_moments = self._identify_critical_moments(live_events, pressure_index)
            self.current_state['critical_moments'] = critical_moments
        
        # Enregistrer l'analyse dans l'historique
        self.pressure_history.append({
            'timestamp': datetime.now().isoformat(),
            'minute': current_minute,
            'pressure_index': pressure_index,
            'crowd_intensity': crowd_intensity,
            'effects': self.pressure_effects.copy()
        })
        
        # Préparer le résultat
        result = {
            'pressure_index': pressure_index,
            'crowd_intensity': crowd_intensity,
            'pressure_effects': self.pressure_effects.copy(),
            'critical_moments': self.current_state['critical_moments'],
            'home_advantage_factor': self.pressure_effects['home_boost'],
            'referee_bias_factor': self.pressure_effects['referee_bias'],
            'momentum_amplification': self.pressure_effects['momentum_amplifier'],
            'match_time': current_minute
        }
        
        return result
    
    def get_crowd_impact_prediction(self, match_data):
        """
        Prédire l'impact potentiel du public sur un match à venir.
        
        Args:
            match_data (dict): Informations sur le match
            
        Returns:
            dict: Prédiction de l'impact du public
        """
        # Extraire les informations pertinentes
        stadium = match_data.get('stadium', '')
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        expected_attendance = match_data.get('expected_attendance', 0)
        stadium_capacity = match_data.get('stadium_capacity', 0)
        match_type = match_data.get('match_type', 'league')
        
        # Calculer les coefficients de base
        attendance_ratio = expected_attendance / stadium_capacity if stadium_capacity > 0 else 0.5
        is_derby = self._is_derby(home_team, away_team)
        match_importance = self._calculate_match_importance(match_data)
        
        # Prédire l'intensité du public
        predicted_intensity = attendance_ratio * 0.5 + match_importance * 0.3
        if is_derby:
            predicted_intensity += 0.2
        predicted_intensity = min(1.0, predicted_intensity)
        
        # Prédire les facteurs d'impact
        home_advantage = self.pressure_factors['home_advantage'] * predicted_intensity
        referee_bias = self.pressure_factors['home_advantage'] * predicted_intensity * 0.3
        away_stress = predicted_intensity * 0.4
        
        # Prédire les moments potentiels de haute pression
        high_pressure_moments = []
        for minute in [2, 45, 46, 75, 85, 90]:  # Moments typiques de haute pression
            factor = 0.7
            if minute in [45, 90]:  # Fin de mi-temps
                factor = 0.9
            high_pressure_moments.append({
                'minute': minute,
                'intensity': predicted_intensity * factor
            })
        
        return {
            'predicted_intensity': predicted_intensity,
            'home_advantage_boost': home_advantage,
            'potential_referee_bias': referee_bias,
            'away_team_stress': away_stress,
            'high_pressure_moments': high_pressure_moments,
            'is_derby': is_derby,
            'match_importance': match_importance
        }
    
    def evaluate_home_advantage(self, team_data):
        """
        Évaluer la force de l'avantage du terrain pour une équipe spécifique.
        
        Args:
            team_data (dict): Données historiques de l'équipe
            
        Returns:
            dict: Évaluation de l'avantage du terrain
        """
        # Extraire les données historiques
        home_wins = team_data.get('home_wins', 0)
        home_matches = team_data.get('home_matches', 0)
        away_wins = team_data.get('away_wins', 0)
        away_matches = team_data.get('away_matches', 0)
        crowd_support = team_data.get('crowd_support', 0.5)  # 0-1 indicateur du support des fans
        
        # Calculer les ratios
        home_win_ratio = home_wins / home_matches if home_matches > 0 else 0.5
        away_win_ratio = away_wins / away_matches if away_matches > 0 else 0.3
        
        # Calculer l'avantage du terrain
        home_advantage = home_win_ratio - away_win_ratio
        
        # Ajuster en fonction du support des fans
        adjusted_advantage = home_advantage * (0.8 + (crowd_support * 0.4))
        
        # Classifier l'avantage
        advantage_category = 'moderate'
        if adjusted_advantage > 0.3:
            advantage_category = 'strong'
        elif adjusted_advantage > 0.15:
            advantage_category = 'significant'
        elif adjusted_advantage < 0.05:
            advantage_category = 'weak'
        
        return {
            'home_advantage_raw': home_advantage,
            'home_advantage_adjusted': adjusted_advantage,
            'category': advantage_category,
            'crowd_factor': crowd_support,
            'home_win_ratio': home_win_ratio,
            'away_win_ratio': away_win_ratio
        }
    
    def _calculate_crowd_intensity(self, minute, attendance_ratio, is_derby, match_importance, live_events=None):
        """Calculer l'intensité actuelle du public."""
        # Intensité de base selon le taux de remplissage et l'importance
        base_intensity = (attendance_ratio * 0.6) + (match_importance * 0.4)
        
        # Bonus pour les derbies
        if is_derby:
            base_intensity = min(1.0, base_intensity + 0.2)
        
        # Ajustement selon le moment du match
        time_factor = 1.0
        if minute < 10:  # Début de match
            time_factor = 0.8
        elif minute > 80:  # Fin de match
            time_factor = 1.2
        elif 40 <= minute <= 45 or 85 <= minute <= 90:  # Fin de mi-temps
            time_factor = 1.1
        
        # Ajustement selon les événements récents
        event_factor = 1.0
        if live_events:
            recent_events = [e for e in live_events if e.get('minute', 0) > minute - 5]
            for event in recent_events:
                event_type = event.get('type', '')
                if event_type == 'goal':
                    event_factor += 0.3
                elif event_type == 'missed_penalty':
                    event_factor += 0.25
                elif event_type == 'red_card':
                    event_factor += 0.2
                elif event_type == 'penalty_awarded':
                    event_factor += 0.15
        
        # Calculer l'intensité finale
        intensity = base_intensity * time_factor * event_factor
        
        # Plafonner à 1.0
        return min(1.0, intensity)
    
    def _calculate_pressure_index(self, crowd_intensity, pressure_curve, minute):
        """Calculer l'indice de pression global."""
        # Déterminer la phase du match (0-8 pour un match de 90 minutes)
        match_phase = min(8, int(minute / 10))
        
        # Obtenir le facteur de courbe pour cette phase
        curve_factor = pressure_curve[match_phase]
        
        # Calculer l'indice de pression
        pressure_index = crowd_intensity * curve_factor
        
        return pressure_index
    
    def _calculate_pressure_effects(self, pressure_index, is_derby, match_importance, minute):
        """Calculer les effets spécifiques de la pression."""
        # Impact sur l'arbitre
        referee_susceptibility = 0.3  # Susceptibilité de base
        if is_derby:
            referee_susceptibility += 0.1
        if minute > 80:  # Fin de match
            referee_susceptibility += 0.15
        
        self.pressure_effects['referee_bias'] = pressure_index * referee_susceptibility
        
        # Boost pour l'équipe à domicile
        home_team_boost = pressure_index * self.pressure_factors['home_advantage']
        self.pressure_effects['home_boost'] = home_team_boost
        
        # Stress pour l'équipe extérieure
        away_team_stress = pressure_index * 0.4
        if is_derby:
            away_team_stress *= 1.3  # Plus de stress dans les derbies
        self.pressure_effects['away_stress'] = away_team_stress
        
        # Amplification du momentum
        momentum_amplifier = pressure_index * 0.5
        if match_importance > 0.7:  # Matchs importants
            momentum_amplifier *= 1.2
        self.pressure_effects['momentum_amplifier'] = momentum_amplifier
    
    def _identify_critical_moments(self, live_events, pressure_index):
        """Identifier les moments critiques où la pression du public est déterminante."""
        critical_moments = []
        
        for event in live_events:
            event_type = event.get('type', '')
            minute = event.get('minute', 0)
            
            # Facteurs qui rendent un moment critique
            is_critical = False
            pressure_impact = 0.0
            
            if event_type == 'penalty_awarded':
                is_critical = True
                pressure_impact = pressure_index * 0.8
            elif event_type == 'red_card' and pressure_index > 0.7:
                is_critical = True
                pressure_impact = pressure_index * 0.6
            elif event_type == 'goal' and minute > 85:
                is_critical = True
                pressure_impact = pressure_index * 0.7
            elif event_type == 'var_review' and pressure_index > 0.6:
                is_critical = True
                pressure_impact = pressure_index * 0.9
            
            if is_critical:
                critical_moments.append({
                    'minute': minute,
                    'event_type': event_type,
                    'pressure_impact': pressure_impact,
                    'pressure_index': pressure_index
                })
        
        return critical_moments
    
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
    
    def _calculate_match_importance(self, match_data):
        """Calculer l'importance du match."""
        competition_type = match_data.get('competition_type', 'league')
        round_info = match_data.get('round', '')
        
        # Importance de base selon le type de compétition
        importance = 0.5  # Valeur par défaut pour les matches de championnat
        
        if competition_type == 'cup':
            importance = 0.7
        elif competition_type == 'continental':
            importance = 0.8
        elif competition_type == 'international':
            importance = 0.9
        
        # Ajustement selon la phase de la compétition
        if 'final' in round_info.lower():
            importance = min(1.0, importance + 0.3)
        elif 'semi' in round_info.lower():
            importance = min(1.0, importance + 0.2)
        elif 'quarter' in round_info.lower():
            importance = min(1.0, importance + 0.1)
        
        # Prendre en compte les enjeux spécifiques
        title_decider = match_data.get('title_decider', False)
        relegation_battle = match_data.get('relegation_battle', False)
        
        if title_decider:
            importance = min(1.0, importance + 0.2)
        if relegation_battle:
            importance = min(1.0, importance + 0.15)
        
        return importance
    
    def _get_match_minute(self, match_data, live_events=None):
        """Déterminer la minute actuelle du match."""
        if live_events and len(live_events) > 0:
            latest_event = max(live_events, key=lambda e: e.get('minute', 0))
            return latest_event.get('minute', 0)
        
        # Si pas d'événements, utiliser le temps de match fourni
        return match_data.get('current_minute', 0)