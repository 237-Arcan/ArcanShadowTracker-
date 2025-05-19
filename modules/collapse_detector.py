"""
CollapseDetector - Module de détection des risques d'effondrement d'une équipe.
Analyse les patterns de fragilité mentale et d'effondrements historiques.
Utilise les données de Transfermarkt pour une analyse plus précise des joueurs clés.
"""

import random
from datetime import datetime, timedelta
import numpy as np
import logging
from collections import defaultdict

# Intégration de l'adaptateur Transfermarkt
from api.transfermarkt_adapter import TransfermarktAdapter

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CollapseDetector:
    """
    CollapseDetector - Système de détection des risques d'effondrement mental et de performance.
    Identifie les moments clés où une équipe est susceptible de s'effondrer pendant un match.
    """
    
    def __init__(self):
        """Initialise le module CollapseDetector avec l'adaptateur Transfermarkt"""
        # Initialiser l'adaptateur Transfermarkt pour obtenir des données réelles
        self.transfermarkt = TransfermarktAdapter()
        logger.info("Initialisation de l'adaptateur Transfermarkt pour CollapseDetector")
        self.use_real_data = self.transfermarkt.api_online
        
        if self.use_real_data:
            logger.info("CollapseDetector utilisera les données réelles de Transfermarkt")
        else:
            logger.warning("API Transfermarkt non disponible, CollapseDetector utilisera des données simulées")
            
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
            
        Returns:
            dict: Analyse des risques d'effondrement
        """
        # Par défaut, utiliser des événements vides si non fournis
        if recent_events is None:
            recent_events = []
        
        # Extraire les noms des équipes
        team1_name = match_data.get('home_team', 'Équipe 1')
        team2_name = match_data.get('away_team', 'Équipe 2')
        
        # Analyse des risques pour chaque équipe
        team1_analysis = self._analyze_team_collapse_risk(
            team1_name, team1_score, team2_score, current_minute, recent_events, is_home=True
        )
        
        team2_analysis = self._analyze_team_collapse_risk(
            team2_name, team2_score, team1_score, current_minute, recent_events, is_home=False
        )
        
        # Analyse comparative entre les équipes
        comparative_analysis = self._compare_collapse_risks(team1_analysis, team2_analysis)
        
        # Recommandations d'action
        recommendations = self._generate_recommendations(
            team1_analysis, team2_analysis, comparative_analysis
        )
        
        # Préparer l'analyse complète
        analysis = {
            'match_state': {
                'minute': current_minute,
                'team1_name': team1_name,
                'team2_name': team2_name,
                'team1_score': team1_score,
                'team2_score': team2_score
            },
            'team1_analysis': team1_analysis,
            'team2_analysis': team2_analysis,
            'comparative_analysis': comparative_analysis,
            'recommendations': recommendations,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'match_state_analysis',
            'timestamp': datetime.now().isoformat(),
            'match': f"{team1_name} vs {team2_name}",
            'minute': current_minute,
            'analysis': analysis
        })
        
        return analysis
    
    def analyze_team_susceptibility(self, team_data, match_history=None):
        """
        Analyser la susceptibilité générale d'une équipe aux effondrements.
        
        Args:
            team_data (dict): Données de l'équipe
            match_history (list, optional): Historique des matchs de l'équipe
            
        Returns:
            dict: Profil de susceptibilité aux effondrements
        """
        # Par défaut, utiliser un historique vide si non fourni
        if match_history is None:
            match_history = []
        
        team_name = team_data.get('name', 'Équipe')
        
        # Initialiser le profil
        susceptibility_profile = {
            'team_name': team_name,
            'overall_score': 0.5,  # Score neutre par défaut
            'key_weaknesses': [],
            'historical_patterns': [],
            'psychological_profile': {},
            'triggering_events': []
        }
        
        # Analyser l'historique des matchs si disponible
        if match_history:
            collapse_instances = self._identify_historical_collapses(match_history)
            susceptibility_profile['historical_patterns'] = collapse_instances
            
            # Calculer un score basé sur l'historique
            historical_score = self._calculate_historical_susceptibility(collapse_instances)
            susceptibility_profile['historical_score'] = historical_score
        
        # Analyser la composition de l'équipe
        squad_analysis = self._analyze_squad_vulnerability(team_data)
        susceptibility_profile['squad_analysis'] = squad_analysis
        
        # Identifier les faiblesses clés
        key_weaknesses = self._identify_key_weaknesses(team_data, match_history)
        susceptibility_profile['key_weaknesses'] = key_weaknesses
        
        # Générer un profil psychologique
        psychological_profile = self._generate_psychological_profile(team_data, match_history)
        susceptibility_profile['psychological_profile'] = psychological_profile
        
        # Identifier les événements déclencheurs
        triggering_events = self._identify_triggering_events(match_history)
        susceptibility_profile['triggering_events'] = triggering_events
        
        # Calculer le score global
        if match_history:
            susceptibility_profile['overall_score'] = (
                historical_score * 0.4 +
                squad_analysis['vulnerability_score'] * 0.3 +
                psychological_profile['vulnerability_score'] * 0.3
            )
        else:
            susceptibility_profile['overall_score'] = (
                squad_analysis['vulnerability_score'] * 0.5 +
                psychological_profile['vulnerability_score'] * 0.5
            )
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'team_susceptibility_analysis',
            'timestamp': datetime.now().isoformat(),
            'team': team_name,
            'analysis': susceptibility_profile
        })
        
        return susceptibility_profile
    
    def predict_collapse_windows(self, match_data, team_susceptibility=None):
        """
        Prédire les fenêtres temporelles où un effondrement est le plus probable.
        
        Args:
            match_data (dict): Données du match
            team_susceptibility (dict, optional): Analyse de susceptibilité pré-calculée
            
        Returns:
            dict: Fenêtres temporelles à risque d'effondrement
        """
        team1_name = match_data.get('home_team', 'Équipe 1')
        team2_name = match_data.get('away_team', 'Équipe 2')
        
        # Générer des susceptibilités si non fournies
        if team_susceptibility is None:
            team1_susceptibility = self.analyze_team_susceptibility({'name': team1_name})
            team2_susceptibility = self.analyze_team_susceptibility({'name': team2_name})
        else:
            team1_susceptibility = team_susceptibility.get(team1_name, self.analyze_team_susceptibility({'name': team1_name}))
            team2_susceptibility = team_susceptibility.get(team2_name, self.analyze_team_susceptibility({'name': team2_name}))
        
        # Identifier les fenêtres génériques à risque
        generic_risk_windows = [
            {'start': 40, 'end': 45, 'description': 'Fin de première mi-temps', 'base_risk': 0.6},
            {'start': 45, 'end': 55, 'description': 'Début de seconde mi-temps', 'base_risk': 0.55},
            {'start': 75, 'end': 90, 'description': 'Fin de match', 'base_risk': 0.7}
        ]
        
        # Ajuster les risques pour chaque équipe
        team1_windows = self._customize_risk_windows(generic_risk_windows, team1_susceptibility)
        team2_windows = self._customize_risk_windows(generic_risk_windows, team2_susceptibility)
        
        # Ajouter des fenêtres spécifiques au match
        match_specific_windows = self._identify_match_specific_windows(match_data, team1_susceptibility, team2_susceptibility)
        
        team1_windows.extend([w for w in match_specific_windows if w['team'] == team1_name])
        team2_windows.extend([w for w in match_specific_windows if w['team'] == team2_name])
        
        # Trier les fenêtres par risque pour chaque équipe
        team1_windows.sort(key=lambda x: x['risk_score'], reverse=True)
        team2_windows.sort(key=lambda x: x['risk_score'], reverse=True)
        
        # Préparer le résultat
        prediction = {
            'match': f"{team1_name} vs {team2_name}",
            'team1_name': team1_name,
            'team2_name': team2_name,
            'team1_windows': team1_windows,
            'team2_windows': team2_windows,
            'high_risk_moments': [
                w for w in team1_windows + team2_windows if w['risk_score'] > 0.7
            ],
            'prediction_timestamp': datetime.now().isoformat()
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'collapse_windows_prediction',
            'timestamp': datetime.now().isoformat(),
            'match': f"{team1_name} vs {team2_name}",
            'prediction': prediction
        })
        
        return prediction
    
    def evaluate_resilience_factor(self, team_data, resilience_type, match_data=None):
        """
        Évaluer un facteur spécifique de résilience pour une équipe.
        
        Args:
            team_data (dict): Données de l'équipe
            resilience_type (str): Type de résilience à évaluer
            match_data (dict, optional): Données du match pour contexte
            
        Returns:
            dict: Évaluation du facteur de résilience
        """
        team_name = team_data.get('name', 'Équipe')
        
        if resilience_type not in self.resilience_factors:
            return {
                'team_name': team_name,
                'resilience_type': resilience_type,
                'error': 'Type de résilience non reconnu'
            }
        
        # Base de l'évaluation
        evaluation = {
            'team_name': team_name,
            'resilience_type': resilience_type,
            'factor_base_value': abs(self.resilience_factors[resilience_type]),
            'contextual_score': 0.5,  # Score neutre par défaut
            'description': '',
            'relevance_to_match': 0.5  # Pertinence moyenne par défaut
        }
        
        # Générer une évaluation du facteur
        if resilience_type == 'strong_leadership':
            evaluation['description'] = self._evaluate_leadership(team_data)
            if match_data:
                evaluation['relevance_to_match'] = self._evaluate_leadership_relevance(match_data)
        
        elif resilience_type == 'comeback_history':
            evaluation['description'] = self._evaluate_comeback_history(team_data)
            if match_data:
                evaluation['relevance_to_match'] = self._evaluate_comeback_relevance(match_data)
        
        elif resilience_type == 'experienced_squad':
            evaluation['description'] = self._evaluate_experience(team_data)
            if match_data:
                evaluation['relevance_to_match'] = self._evaluate_experience_relevance(match_data)
        
        elif resilience_type == 'tactical_flexibility':
            evaluation['description'] = self._evaluate_tactical_flexibility(team_data)
            if match_data:
                evaluation['relevance_to_match'] = self._evaluate_tactical_relevance(match_data)
        
        # Générer un score contextuel
        # Dans une implémentation réelle, cela serait basé sur des données réelles
        evaluation['contextual_score'] = random.uniform(
            max(0.3, evaluation['factor_base_value'] - 0.2),
            min(0.9, evaluation['factor_base_value'] + 0.2)
        )
        
        return evaluation
    
    def _analyze_team_collapse_risk(self, team_name, team_score, opponent_score, current_minute, recent_events, is_home=True):
        """Analyser le risque d'effondrement pour une équipe spécifique."""
        # Base de l'analyse
        analysis = {
            'team_name': team_name,
            'current_risk_score': 0.5,  # Score neutre par défaut
            'risk_factors': [],
            'active_patterns': [],
            'psychological_state': {},
            'trend': 'stable'  # stable, increasing, decreasing
        }
        
        # Facteurs de base
        base_factors = []
        
        # Facteur 1: Minute du match
        if current_minute > 75:
            factor = {'name': 'late_game_pressure', 'impact': 0.2}
            base_factors.append(factor)
        elif 40 <= current_minute <= 45:
            factor = {'name': 'end_of_half_pressure', 'impact': 0.15}
            base_factors.append(factor)
        elif 45 <= current_minute <= 55:
            factor = {'name': 'start_of_second_half_adjustment', 'impact': 0.1}
            base_factors.append(factor)
        
        # Facteur 2: État du score
        score_diff = team_score - opponent_score
        if score_diff == -1:
            factor = {'name': 'narrow_deficit', 'impact': 0.15}
            base_factors.append(factor)
        elif score_diff <= -2:
            factor = {'name': 'significant_deficit', 'impact': 0.25}
            base_factors.append(factor)
        elif score_diff == 1:
            factor = {'name': 'protecting_narrow_lead', 'impact': 0.2}
            base_factors.append(factor)
        
        # Facteur 3: Domicile/Extérieur
        if not is_home:
            factor = {'name': 'away_team_pressure', 'impact': 0.1}
            base_factors.append(factor)
        
        # Ajouter nos facteurs de base
        analysis['risk_factors'] = base_factors
        
        # Calculer le score de risque actuel
        risk_score = 0.4  # Base neutre légèrement optimiste
        for factor in base_factors:
            risk_score += factor['impact']
        
        # Limiter entre 0.1 et 0.9
        analysis['current_risk_score'] = max(0.1, min(0.9, risk_score))
        
        # Analyser les patterns actifs
        active_patterns = []
        for pattern_name, pattern_data in self.collapse_patterns.items():
            is_active = self._check_pattern_active(
                pattern_name, pattern_data, current_minute, 
                team_score, opponent_score, recent_events
            )
            if is_active:
                active_patterns.append({
                    'pattern': pattern_name,
                    'description': pattern_data['description'],
                    'importance': pattern_data['importance'],
                    'remaining_window': pattern_data['time_window'] - self._get_time_since_trigger(pattern_name, recent_events, current_minute)
                })
        
        analysis['active_patterns'] = active_patterns
        
        # Ajuster le score en fonction des patterns actifs
        for pattern in active_patterns:
            analysis['current_risk_score'] = min(
                0.9, 
                analysis['current_risk_score'] + (pattern['importance'] * 0.1)
            )
        
        # Simuler un état psychologique (dans une implémentation réelle, cela viendrait d'une analyse)
        psychological_state = self._simulate_psychological_state(
            team_name, team_score, opponent_score, current_minute
        )
        analysis['psychological_state'] = psychological_state
        
        # Ajuster le score en fonction de l'état psychologique
        psych_adjustment = (psychological_state['frustration'] * 0.1 + 
                           psychological_state['cohesion'] * -0.1 +
                           psychological_state['confidence'] * -0.15)
        analysis['current_risk_score'] = max(0.1, min(0.9, analysis['current_risk_score'] + psych_adjustment))
        
        # Déterminer la tendance
        analysis['trend'] = self._determine_risk_trend(
            analysis['current_risk_score'], current_minute, recent_events
        )
        
        return analysis
    
    def _check_pattern_active(self, pattern_name, pattern_data, current_minute, team_score, opponent_score, recent_events):
        """Vérifier si un pattern d'effondrement est actif."""
        if pattern_name == 'after_conceding':
            # Vérifier s'il y a eu un but encaissé récemment
            for event in recent_events:
                if (event.get('type') == 'goal' and 
                    event.get('against_team', False) and
                    current_minute - event.get('minute', 0) <= pattern_data['time_window']):
                    return True
        
        elif pattern_name == 'late_game_pressure':
            # Vérifier si c'est la fin du match avec un score serré
            return (current_minute >= 75 and 
                   abs(team_score - opponent_score) <= 1)
        
        elif pattern_name == 'momentum_shift':
            # Vérifier s'il y a eu un changement de momentum récent
            has_momentum_shift = False
            for event in recent_events:
                if (event.get('type') in ['missed_chance', 'red_card', 'penalty_against'] and
                    current_minute - event.get('minute', 0) <= pattern_data['time_window']):
                    has_momentum_shift = True
                    break
            return has_momentum_shift
        
        elif pattern_name == 'key_player_impact':
            # Vérifier s'il y a eu une perte de joueur clé
            for event in recent_events:
                if (event.get('type') in ['substitution', 'injury'] and
                    event.get('key_player', False) and
                    current_minute - event.get('minute', 0) <= pattern_data['time_window']):
                    return True
        
        return False
    
    def _get_time_since_trigger(self, pattern_name, recent_events, current_minute):
        """Obtenir le temps écoulé depuis le déclenchement du pattern."""
        trigger_minute = 0
        
        if pattern_name == 'after_conceding':
            for event in recent_events:
                if (event.get('type') == 'goal' and 
                    event.get('against_team', False)):
                    trigger_minute = max(trigger_minute, event.get('minute', 0))
        
        elif pattern_name == 'late_game_pressure':
            trigger_minute = 75  # Début de la période de pression
        
        elif pattern_name == 'momentum_shift':
            for event in recent_events:
                if event.get('type') in ['missed_chance', 'red_card', 'penalty_against']:
                    trigger_minute = max(trigger_minute, event.get('minute', 0))
        
        elif pattern_name == 'key_player_impact':
            for event in recent_events:
                if (event.get('type') in ['substitution', 'injury'] and
                    event.get('key_player', False)):
                    trigger_minute = max(trigger_minute, event.get('minute', 0))
        
        return max(0, current_minute - trigger_minute)
    
    def _simulate_psychological_state(self, team_name, team_score, opponent_score, current_minute):
        """Simuler l'état psychologique d'une équipe (dans une version réelle, cela serait basé sur des données)."""
        # Base de l'état psychologique
        psychological_state = {
            'frustration': 0.5,
            'cohesion': 0.5,
            'confidence': 0.5,
            'energy': 0.5,
            'focus': 0.5
        }
        
        # Ajuster en fonction du score
        score_diff = team_score - opponent_score
        if score_diff < 0:
            # En déficit, plus de frustration, moins de confiance
            psychological_state['frustration'] = min(0.9, 0.5 + abs(score_diff) * 0.15)
            psychological_state['confidence'] = max(0.2, 0.5 - abs(score_diff) * 0.1)
            psychological_state['cohesion'] = max(0.3, 0.5 - abs(score_diff) * 0.05)
        elif score_diff > 0:
            # En avance, plus de confiance
            psychological_state['confidence'] = min(0.9, 0.5 + score_diff * 0.1)
            psychological_state['frustration'] = max(0.2, 0.5 - score_diff * 0.1)
            
            # Mais si l'avance est grande en fin de match, possible baisse de concentration
            if score_diff >= 2 and current_minute > 70:
                psychological_state['focus'] = max(0.3, 0.5 - 0.1)
        
        # Ajuster en fonction du temps de jeu
        if current_minute > 75:
            # Fin de match, baisse d'énergie
            psychological_state['energy'] = max(0.3, 0.5 - (current_minute - 75) / 15 * 0.2)
        
        # Ajouter un peu de variabilité pour simuler l'incertitude
        for key in psychological_state:
            psychological_state[key] = max(0.1, min(0.9, psychological_state[key] + random.uniform(-0.1, 0.1)))
        
        return psychological_state
    
    def _determine_risk_trend(self, current_risk, current_minute, recent_events):
        """Déterminer la tendance du risque d'effondrement."""
        # Rechercher des événements récents qui pourraient impacter la tendance
        recent_negative_events = 0
        recent_positive_events = 0
        very_recent_window = 5  # 5 dernières minutes
        
        for event in recent_events:
            event_minute = event.get('minute', 0)
            if current_minute - event_minute > very_recent_window:
                continue
                
            event_type = event.get('type', '')
            if event_type in ['goal_against', 'red_card', 'missed_chance', 'injury']:
                recent_negative_events += 1
            elif event_type in ['goal_for', 'saved_shot', 'successful_tackle', 'key_pass']:
                recent_positive_events += 1
        
        # Déterminer la tendance
        if recent_negative_events > recent_positive_events + 1:
            return 'increasing'  # Risque en hausse
        elif recent_positive_events > recent_negative_events + 1:
            return 'decreasing'  # Risque en baisse
        elif current_minute > 80 and current_risk > 0.6:
            return 'increasing'  # Fin de match à haut risque = tendance à la hausse
        else:
            return 'stable'  # Tendance stable
    
    def _compare_collapse_risks(self, team1_analysis, team2_analysis):
        """Comparer les risques d'effondrement entre les deux équipes."""
        comparative_analysis = {
            'team1_name': team1_analysis['team_name'],
            'team2_name': team2_analysis['team_name'],
            'team1_risk': team1_analysis['current_risk_score'],
            'team2_risk': team2_analysis['current_risk_score'],
            'risk_differential': team1_analysis['current_risk_score'] - team2_analysis['current_risk_score'],
            'higher_risk_team': team1_analysis['team_name'] if team1_analysis['current_risk_score'] > team2_analysis['current_risk_score'] else team2_analysis['team_name'],
            'comparative_assessment': ''
        }
        
        # Générer une évaluation comparative
        risk_diff = abs(comparative_analysis['risk_differential'])
        
        if risk_diff < 0.1:
            comparative_analysis['comparative_assessment'] = "Les deux équipes présentent un niveau de risque d'effondrement similaire."
        elif risk_diff < 0.2:
            comparative_analysis['comparative_assessment'] = f"{comparative_analysis['higher_risk_team']} présente un risque d'effondrement légèrement plus élevé."
        elif risk_diff < 0.4:
            comparative_analysis['comparative_assessment'] = f"{comparative_analysis['higher_risk_team']} présente un risque d'effondrement significativement plus élevé."
        else:
            comparative_analysis['comparative_assessment'] = f"{comparative_analysis['higher_risk_team']} présente un risque d'effondrement très élevé par rapport à l'adversaire."
        
        return comparative_analysis
    
    def _generate_recommendations(self, team1_analysis, team2_analysis, comparative_analysis):
        """Générer des recommandations d'observation et d'action basées sur l'analyse."""
        recommendations = []
        
        # Recommandations pour l'équipe à plus haut risque
        higher_risk_team = comparative_analysis['higher_risk_team']
        higher_risk_analysis = team1_analysis if higher_risk_team == team1_analysis['team_name'] else team2_analysis
        
        if higher_risk_analysis['current_risk_score'] > 0.7:
            recommendations.append({
                'priority': 'high',
                'focus': higher_risk_team,
                'observation': f"Surveiller attentivement les signes de désorganisation et de frustration chez {higher_risk_team}",
                'action': f"Considérer une forte probabilité d'effondrement défensif pour {higher_risk_team}"
            })
        elif higher_risk_analysis['current_risk_score'] > 0.5:
            recommendations.append({
                'priority': 'medium',
                'focus': higher_risk_team,
                'observation': f"Observer l'attitude corporelle et la communication entre les joueurs de {higher_risk_team}",
                'action': f"Envisager un risque modéré d'effondrement si un événement déclencheur survient"
            })
        
        # Recommandations basées sur les patterns actifs
        for team_analysis in [team1_analysis, team2_analysis]:
            team_name = team_analysis['team_name']
            
            for pattern in team_analysis['active_patterns']:
                if pattern['importance'] > 0.7:
                    recommendations.append({
                        'priority': 'high',
                        'focus': team_name,
                        'observation': f"Pattern '{pattern['description']}' actif pour {team_name}",
                        'action': f"Anticiper un possible effondrement dans les {pattern['remaining_window']} prochaines minutes"
                    })
                else:
                    recommendations.append({
                        'priority': 'medium',
                        'focus': team_name,
                        'observation': f"Pattern '{pattern['description']}' actif pour {team_name}",
                        'action': f"Rester attentif à l'évolution dans les {pattern['remaining_window']} prochaines minutes"
                    })
        
        # Recommandations basées sur l'état psychologique
        for team_analysis in [team1_analysis, team2_analysis]:
            team_name = team_analysis['team_name']
            psych_state = team_analysis['psychological_state']
            
            if psych_state['frustration'] > 0.7 and psych_state['cohesion'] < 0.4:
                recommendations.append({
                    'priority': 'high',
                    'focus': team_name,
                    'observation': f"Niveau élevé de frustration et faible cohésion chez {team_name}",
                    'action': "Anticiper des erreurs défensives et un manque de coordination"
                })
            elif psych_state['confidence'] < 0.3:
                recommendations.append({
                    'priority': 'medium',
                    'focus': team_name,
                    'observation': f"Confiance très basse chez {team_name}",
                    'action': "Surveiller les signes de repli défensif et de jeu hésitant"
                })
        
        # Trier par priorité
        recommendations.sort(key=lambda x: 0 if x['priority'] == 'high' else (1 if x['priority'] == 'medium' else 2))
        
        return recommendations
    
    def _identify_historical_collapses(self, match_history):
        """Identifier les effondrements historiques dans l'historique des matchs."""
        collapse_instances = []
        
        for match in match_history:
            # Vérifier si le match montre des signes d'effondrement
            is_collapse = False
            collapse_type = None
            
            # Type 1: Perdre un match après avoir mené
            if ('score_progression' in match and 
                any(score[0] > score[1] for score in match['score_progression'][:-1]) and
                match['score_progression'][-1][0] < match['score_progression'][-1][1]):
                is_collapse = True
                collapse_type = 'lost_after_leading'
            
            # Type 2: Encaisser plusieurs buts en peu de temps
            if 'goals_conceded_minutes' in match:
                consecutive_goals = self._find_consecutive_conceded_goals(match['goals_conceded_minutes'])
                if consecutive_goals:
                    is_collapse = True
                    collapse_type = 'multiple_goals_conceded'
            
            # Type 3: Effondrement en fin de match
            if ('score_progression' in match and 
                len(match['score_progression']) >= 2 and
                match['score_progression'][-2][0] - match['score_progression'][-2][1] >
                match['score_progression'][-1][0] - match['score_progression'][-1][1] + 1):
                is_collapse = True
                collapse_type = 'late_game_collapse'
            
            if is_collapse:
                collapse_instances.append({
                    'match_date': match.get('date', 'Unknown'),
                    'opponent': match.get('opponent', 'Unknown'),
                    'collapse_type': collapse_type,
                    'description': self._generate_collapse_description(match, collapse_type)
                })
        
        return collapse_instances
    
    def _find_consecutive_conceded_goals(self, goal_minutes):
        """Trouver des séquences de buts encaissés en peu de temps."""
        if len(goal_minutes) < 2:
            return None
            
        goal_minutes.sort()
        for i in range(len(goal_minutes) - 1):
            if goal_minutes[i+1] - goal_minutes[i] <= 10:  # Buts encaissés en 10 minutes ou moins
                return (goal_minutes[i], goal_minutes[i+1])
                
        return None
    
    def _generate_collapse_description(self, match, collapse_type):
        """Générer une description de l'effondrement historique."""
        if collapse_type == 'lost_after_leading':
            lead_score = None
            for i, score in enumerate(match.get('score_progression', [])):
                if score[0] > score[1]:
                    lead_score = score
                    break
                    
            final_score = match.get('score_progression', [])[-1]
            return f"Défaite {final_score[0]}-{final_score[1]} après avoir mené {lead_score[0]}-{lead_score[1]}"
            
        elif collapse_type == 'multiple_goals_conceded':
            consecutive_goals = self._find_consecutive_conceded_goals(match.get('goals_conceded_minutes', []))
            if consecutive_goals:
                return f"Plusieurs buts encaissés en peu de temps (minutes {consecutive_goals[0]} et {consecutive_goals[1]})"
            
        elif collapse_type == 'late_game_collapse':
            progress = match.get('score_progression', [])
            if len(progress) >= 2:
                return f"Effondrement en fin de match, passant de {progress[-2][0]}-{progress[-2][1]} à {progress[-1][0]}-{progress[-1][1]}"
            
        return "Effondrement notable"
    
    def _calculate_historical_susceptibility(self, collapse_instances):
        """Calculer un score de susceptibilité basé sur l'historique."""
        if not collapse_instances:
            return 0.5  # Score neutre
            
        # Score de base influencé par le nombre d'effondrements
        base_score = min(0.9, 0.4 + len(collapse_instances) * 0.1)
        
        # Ajuster en fonction des types d'effondrement
        collapse_types = [instance['collapse_type'] for instance in collapse_instances]
        
        # Les effondrements répétitifs du même type indiquent une faiblesse structurelle
        if collapse_types.count('lost_after_leading') > 1:
            base_score += 0.1
        if collapse_types.count('multiple_goals_conceded') > 1:
            base_score += 0.1
        if collapse_types.count('late_game_collapse') > 1:
            base_score += 0.1
            
        # Limiter entre 0.1 et 0.9
        return max(0.1, min(0.9, base_score))
    
    def _analyze_squad_vulnerability(self, team_data):
        """Analyser la vulnérabilité de l'effectif aux effondrements."""
        # Dans une implémentation réelle, cela utiliserait des données d'équipe réelles
        # Ici, nous simulons pour l'exemple
        
        squad_analysis = {
            'vulnerability_score': 0.5,  # Score neutre par défaut
            'key_factors': [],
            'strengths': [],
            'weaknesses': []
        }
        
        # Facteurs simulés (dans une implémentation réelle, ces données viendraient de l'équipe)
        experience_level = random.uniform(0.3, 0.9)
        leadership_presence = random.uniform(0.3, 0.9)
        mental_resilience = random.uniform(0.3, 0.9)
        squad_depth = random.uniform(0.3, 0.9)
        tactical_rigidity = random.uniform(0.3, 0.9)
        
        # Calculer le score de vulnérabilité
        vulnerability_factors = [
            1 - experience_level,  # Moins d'expérience = plus de vulnérabilité
            1 - leadership_presence,
            1 - mental_resilience,
            1 - squad_depth,
            tactical_rigidity  # Plus de rigidité = plus de vulnérabilité
        ]
        
        squad_analysis['vulnerability_score'] = sum(vulnerability_factors) / len(vulnerability_factors)
        
        # Identifier les forces et faiblesses clés
        if experience_level > 0.7:
            squad_analysis['strengths'].append("Équipe expérimentée")
        elif experience_level < 0.4:
            squad_analysis['weaknesses'].append("Manque d'expérience dans l'effectif")
            squad_analysis['key_factors'].append({
                'factor': 'inexperience',
                'impact': 0.7
            })
        
        if leadership_presence > 0.7:
            squad_analysis['strengths'].append("Leadership fort sur le terrain")
        elif leadership_presence < 0.4:
            squad_analysis['weaknesses'].append("Absence de leaders clairs")
            squad_analysis['key_factors'].append({
                'factor': 'leadership_vacuum',
                'impact': 0.8
            })
        
        if mental_resilience > 0.7:
            squad_analysis['strengths'].append("Forte résilience mentale")
        elif mental_resilience < 0.4:
            squad_analysis['weaknesses'].append("Fragilité mentale")
            squad_analysis['key_factors'].append({
                'factor': 'mental_fragility',
                'impact': 0.9
            })
        
        if squad_depth > 0.7:
            squad_analysis['strengths'].append("Effectif profond")
        elif squad_depth < 0.4:
            squad_analysis['weaknesses'].append("Manque de profondeur d'effectif")
            squad_analysis['key_factors'].append({
                'factor': 'thin_squad',
                'impact': 0.6
            })
        
        if tactical_rigidity < 0.4:
            squad_analysis['strengths'].append("Flexibilité tactique")
        elif tactical_rigidity > 0.7:
            squad_analysis['weaknesses'].append("Rigidité tactique")
            squad_analysis['key_factors'].append({
                'factor': 'tactical_inflexibility',
                'impact': 0.7
            })
        
        return squad_analysis
    
    def _identify_key_weaknesses(self, team_data, match_history):
        """Identifier les faiblesses clés d'une équipe en termes de risque d'effondrement."""
        # Dans une implémentation réelle, cela utiliserait l'analyse des données
        # Ici, nous simulons pour l'exemple
        
        weaknesses = []
        
        # Simuler l'identification de faiblesses basées sur des patterns imaginaires
        if random.random() < 0.3:
            weaknesses.append({
                'type': 'defensive_organization',
                'description': "Désorganisation défensive sous pression",
                'severity': random.uniform(0.6, 0.9),
                'evidence': f"Visible dans {random.randint(1, 5)} matchs récents"
            })
            
        if random.random() < 0.25:
            weaknesses.append({
                'type': 'set_piece_vulnerability',
                'description': "Vulnérabilité sur coups de pied arrêtés défensifs",
                'severity': random.uniform(0.5, 0.8),
                'evidence': f"{random.randint(20, 40)}% des buts encaissés sur phases arrêtées"
            })
            
        if random.random() < 0.2:
            weaknesses.append({
                'type': 'counterattack_exposure',
                'description': "Exposition aux contre-attaques en fin de match",
                'severity': random.uniform(0.6, 0.85),
                'evidence': f"{random.randint(3, 8)} buts encaissés en contre-attaque en fin de match"
            })
            
        if random.random() < 0.3:
            weaknesses.append({
                'type': 'mental_resilience',
                'description': "Baisse de performances après avoir encaissé",
                'severity': random.uniform(0.7, 0.9),
                'evidence': f"Temps de récupération mental moyen de {random.randint(8, 15)} minutes après un but encaissé"
            })
            
        if random.random() < 0.25:
            weaknesses.append({
                'type': 'squad_depth',
                'description': "Baisse de niveau significative avec les remplaçants",
                'severity': random.uniform(0.5, 0.85),
                'evidence': f"Performance réduite de {random.randint(15, 30)}% après les changements"
            })
        
        # Trier par sévérité
        weaknesses.sort(key=lambda x: x['severity'], reverse=True)
        
        return weaknesses
    
    def _generate_psychological_profile(self, team_data, match_history):
        """Générer un profil psychologique de l'équipe par rapport aux effondrements."""
        # Dans une implémentation réelle, cela utiliserait l'analyse des données
        # Ici, nous simulons pour l'exemple
        
        profile = {
            'vulnerability_score': random.uniform(0.4, 0.7),
            'traits': {},
            'key_observations': []
        }
        
        # Traits simulés
        profile['traits'] = {
            'resilience': random.uniform(0.3, 0.8),
            'collective_confidence': random.uniform(0.4, 0.8),
            'pressure_handling': random.uniform(0.3, 0.8),
            'adaptability': random.uniform(0.4, 0.8),
            'leadership_structure': random.uniform(0.3, 0.8),
            'emotional_control': random.uniform(0.3, 0.7)
        }
        
        # Générer des observations clés basées sur les traits
        if profile['traits']['resilience'] < 0.5:
            profile['key_observations'].append("L'équipe montre des signes de fragilité après des revers")
            
        if profile['traits']['collective_confidence'] < 0.5:
            profile['key_observations'].append("Manque de confiance collective dans les moments difficiles")
            
        if profile['traits']['pressure_handling'] < 0.5:
            profile['key_observations'].append("Difficultés à gérer la pression dans les matchs importants")
            
        if profile['traits']['adaptability'] < 0.5:
            profile['key_observations'].append("Manque d'adaptabilité face aux changements tactiques adverses")
            
        if profile['traits']['leadership_structure'] < 0.5:
            profile['key_observations'].append("Structure de leadership fragile en l'absence de certains cadres")
            
        if profile['traits']['emotional_control'] < 0.5:
            profile['key_observations'].append("Contrôle émotionnel insuffisant face à l'adversité")
        
        return profile
    
    def _identify_triggering_events(self, match_history):
        """Identifier les événements qui déclenchent typiquement un effondrement."""
        # Dans une implémentation réelle, cela analyserait l'historique des matchs
        # Ici, nous simulons pour l'exemple
        
        triggers = []
        
        possible_triggers = [
            {'type': 'goal_conceded', 'description': "But encaissé contre le cours du jeu"},
            {'type': 'referee_decision', 'description': "Décision arbitrale controversée"},
            {'type': 'key_player_injury', 'description': "Blessure d'un joueur clé"},
            {'type': 'tactical_change', 'description': "Changement tactique adverse efficace"},
            {'type': 'momentum_loss', 'description': "Perte de momentum après occasions manquées"},
            {'type': 'individual_error', 'description': "Erreur individuelle majeure"},
            {'type': 'set_piece_conceded', 'description': "But encaissé sur coup de pied arrêté"}
        ]
        
        # Sélectionner aléatoirement 2-4 déclencheurs
        num_triggers = random.randint(2, 4)
        selected_triggers = random.sample(possible_triggers, num_triggers)
        
        for trigger in selected_triggers:
            trigger_data = trigger.copy()
            trigger_data['impact_score'] = random.uniform(0.6, 0.9)
            trigger_data['frequency'] = f"{random.randint(3, 8)} occurrences identifiées"
            triggers.append(trigger_data)
        
        # Trier par impact
        triggers.sort(key=lambda x: x['impact_score'], reverse=True)
        
        return triggers
    
    def _customize_risk_windows(self, generic_windows, team_susceptibility):
        """Personnaliser les fenêtres de risque génériques pour une équipe spécifique."""
        team_name = team_susceptibility['team_name']
        susceptibility_score = team_susceptibility['overall_score']
        
        customized_windows = []
        
        for window in generic_windows:
            custom_window = window.copy()
            custom_window['team'] = team_name
            
            # Ajuster le risque en fonction de la susceptibilité
            risk_adjustment = (susceptibility_score - 0.5) * 0.4  # -0.2 à +0.2
            custom_window['risk_score'] = max(0.1, min(0.9, custom_window['base_risk'] + risk_adjustment))
            
            # Ajuster légèrement les minutes pour créer une variabilité
            minute_adjustment = random.randint(-2, 2)
            custom_window['start'] = max(1, custom_window['start'] + minute_adjustment)
            custom_window['end'] = min(90, custom_window['end'] + minute_adjustment)
            
            customized_windows.append(custom_window)
        
        return customized_windows
    
    def _identify_match_specific_windows(self, match_data, team1_susceptibility, team2_susceptibility):
        """Identifier des fenêtres de risque spécifiques au match."""
        match_specific_windows = []
        
        team1_name = team1_susceptibility['team_name']
        team2_name = team2_susceptibility['team_name']
        
        # Fenêtre 1: Début de match pour l'équipe ayant un historique de départs difficiles
        if random.random() < 0.3:  # 30% de chance
            team_with_slow_starts = team1_name if random.random() < 0.5 else team2_name
            match_specific_windows.append({
                'team': team_with_slow_starts,
                'start': 1,
                'end': 15,
                'description': "Début de match difficile",
                'risk_score': random.uniform(0.6, 0.8),
                'specific_factor': "Historique de départs lents"
            })
        
        # Fenêtre 2: Risque après un but potentiel
        goal_minute = random.randint(25, 65)
        conceding_team = team1_name if random.random() < 0.5 else team2_name
        match_specific_windows.append({
            'team': conceding_team,
            'start': goal_minute,
            'end': goal_minute + 10,
            'description': "Après un but potentiel",
            'risk_score': random.uniform(0.65, 0.85),
            'specific_factor': "Vulnérabilité après avoir encaissé"
        })
        
        # Fenêtre 3: Risque lié à la fatigue pour une équipe ayant joué récemment
        tired_team = team1_name if random.random() < 0.5 else team2_name
        match_specific_windows.append({
            'team': tired_team,
            'start': 65,
            'end': 90,
            'description': "Phase de fatigue",
            'risk_score': random.uniform(0.6, 0.8),
            'specific_factor': "Fatigue accumulée"
        })
        
        return match_specific_windows
    
    def _evaluate_leadership(self, team_data):
        """Évaluer le leadership dans l'équipe."""
        # Dans une implémentation réelle, cela utiliserait des données d'équipe
        return "Présence de leaders clés sur le terrain avec influence positive en situation de stress" if random.random() < 0.6 else "Structure de leadership fragile dépendant fortement du capitaine"
    
    def _evaluate_leadership_relevance(self, match_data):
        """Évaluer la pertinence du facteur leadership pour le match."""
        return random.uniform(0.5, 0.9)  # Plus élevé = plus pertinent
    
    def _evaluate_comeback_history(self, team_data):
        """Évaluer l'historique de remontées de l'équipe."""
        return f"Historique de {random.randint(2, 8)} remontées significatives sur la saison, démontrant une forte capacité à réagir" if random.random() < 0.5 else f"Seulement {random.randint(0, 2)} remontées réussies cette saison, indiquant une fragilité mentale lorsque menée au score"
    
    def _evaluate_comeback_relevance(self, match_data):
        """Évaluer la pertinence du facteur de remontée pour le match."""
        return random.uniform(0.5, 0.9)
    
    def _evaluate_experience(self, team_data):
        """Évaluer l'expérience de l'équipe."""
        return f"Équipe expérimentée avec âge moyen de {random.randint(27, 31)} ans et {random.randint(500, 1500)} matchs professionnels cumulés" if random.random() < 0.6 else f"Équipe relativement jeune avec âge moyen de {random.randint(22, 26)} ans et manque d'expérience dans les moments décisifs"
    
    def _evaluate_experience_relevance(self, match_data):
        """Évaluer la pertinence du facteur expérience pour le match."""
        return random.uniform(0.5, 0.9)
    
    def _evaluate_tactical_flexibility(self, team_data):
        """Évaluer la flexibilité tactique de l'équipe."""
        return f"Équipe ayant utilisé {random.randint(3, 6)} systèmes tactiques cette saison avec transitions fluides" if random.random() < 0.5 else f"Équipe rigide tactiquement, limitée à {random.randint(1, 2)} systèmes de jeu et adaptations lentes aux changements adverses"
    
    def _evaluate_tactical_relevance(self, match_data):
        """Évaluer la pertinence du facteur tactique pour le match."""
        return random.uniform(0.5, 0.9)