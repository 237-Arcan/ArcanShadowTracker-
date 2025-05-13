"""
KarmicFlow+ - Module d'analyse des flux karmiques dans le sport.
Détecte et quantifie les patterns de "justice poétique" et les retours de fortune dans le football.
"""

import numpy as np
import random
from datetime import datetime, timedelta
import json
import os
from collections import deque
import math

class KarmicFlowPlus:
    """
    KarmicFlow+ - Analyse des retours karmiques et de la justice poétique dans le football.
    Détecte les séquences où la fortune semble "équilibrer les comptes" pour les équipes et joueurs.
    """
    
    def __init__(self):
        """Initialise le module KarmicFlow+."""
        # Types de phénomènes karmiques reconnus
        self.karmic_patterns = {
            'revenge': {
                'description': 'Revanche sur une défaite ou humiliation précédente',
                'detection_threshold': 0.7,
                'narrative_power': 0.8,
                'emotional_impact': 0.85
            },
            'redemption': {
                'description': 'Rédemption après une erreur ou un échec',
                'detection_threshold': 0.75,
                'narrative_power': 0.9,
                'emotional_impact': 0.9
            },
            'poetic_justice': {
                'description': 'Justice poétique - destin ironique',
                'detection_threshold': 0.8,
                'narrative_power': 0.85,
                'emotional_impact': 0.8
            },
            'long_awaited': {
                'description': 'Accomplissement longtemps attendu',
                'detection_threshold': 0.65,
                'narrative_power': 0.75,
                'emotional_impact': 0.85
            },
            'reversal_of_fortune': {
                'description': 'Renversement dramatique de fortune',
                'detection_threshold': 0.7,
                'narrative_power': 0.8,
                'emotional_impact': 0.75
            },
            'nemesis': {
                'description': 'Adversaire récurrent qui pose des problèmes spécifiques',
                'detection_threshold': 0.65,
                'narrative_power': 0.7,
                'emotional_impact': 0.75
            }
        }
        
        # Paramètres d'analyse karmique
        self.karmic_parameters = {
            'time_threshold': 5,           # Années pour connexion karmique longue durée
            'match_threshold': 3,          # Matchs pour connexion karmique courte durée
            'emotional_threshold': 0.7,    # Seuil d'impact émotionnel
            'narrative_threshold': 0.65,   # Seuil d'impact narratif
            'minimum_karma_score': 0.6,    # Score karmique minimum pour validation
            'individual_weight': 0.7,      # Poids des histoires individuelles
            'team_weight': 0.8             # Poids des histoires d'équipe
        }
        
        # Facteurs d'amplification karmique
        self.amplification_factors = {
            'media_coverage': 0.3,         # Amplification par la couverture médiatique
            'fan_sentiment': 0.25,         # Amplification par le sentiment des fans
            'historical_rivalry': 0.35,    # Amplification par la rivalité historique
            'competition_prestige': 0.4,   # Amplification par le prestige de la compétition
            'drama_level': 0.2,            # Amplification par le niveau de drame/controverse
            'milestone': 0.3               # Amplification par caractère historique/record
        }
        
        # Historique des analyses karmiques
        self.karmic_analysis_history = []
        
        # État karmique actuel pour les entités suivies
        self.entity_karmic_states = {}
        
        # Base de données des histoires karmiques notables
        self.karmic_stories_db = []
        
        # Compteurs pour l'analyse statistique
        self.pattern_counters = {p: 0 for p in self.karmic_patterns}
    
    def analyze_karmic_potential(self, event_data, historical_context=None):
        """
        Analyser le potentiel karmique d'un événement sportif.
        
        Args:
            event_data (dict): Données sur l'événement à analyser
            historical_context (dict, optional): Contexte historique supplémentaire
            
        Returns:
            dict: Analyse du potentiel karmique
        """
        # Extraire les informations de base
        event_type = event_data.get('type', '')
        entity_id = event_data.get('entity_id', '')
        entity_name = event_data.get('entity_name', '')
        entity_type = event_data.get('entity_type', 'team')  # 'team' ou 'player'
        
        # Vérifier si nous avons un type d'événement valide
        if not event_type:
            return {
                'status': 'invalid_event',
                'message': 'Type d\'événement manquant ou invalide'
            }
        
        # Extraire le contexte historique si non fourni
        if not historical_context:
            historical_context = self._retrieve_historical_context(entity_id, entity_type)
        
        # Évaluer le potentiel karmique pour chaque pattern reconnu
        karmic_evaluations = []
        
        for pattern_name, pattern_data in self.karmic_patterns.items():
            evaluation = self._evaluate_karmic_pattern(
                pattern_name, event_data, historical_context
            )
            
            if evaluation['match_score'] >= pattern_data['detection_threshold']:
                karmic_evaluations.append(evaluation)
                self.pattern_counters[pattern_name] += 1
        
        # Si aucun pattern n'est détecté, retourner une analyse minimale
        if not karmic_evaluations:
            return {
                'entity_name': entity_name,
                'entity_type': entity_type,
                'event_type': event_type,
                'karmic_potential': 0.0,
                'detected_patterns': [],
                'narrative_power': 0.0,
                'has_karmic_significance': False,
                'analysis_timestamp': datetime.now().isoformat()
            }
        
        # Trier les évaluations par score de correspondance
        karmic_evaluations.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Calculer le potentiel karmique global
        best_evaluation = karmic_evaluations[0]
        karmic_potential = best_evaluation['match_score'] * self.karmic_patterns[best_evaluation['pattern']]['narrative_power']
        
        # Amplifier selon les facteurs contextuels
        amplification = self._calculate_amplification_factors(event_data, historical_context)
        amplified_potential = karmic_potential * (1 + amplification)
        
        # Déterminer si l'événement a une signification karmique
        has_significance = amplified_potential > self.karmic_parameters['minimum_karma_score']
        
        # Préparer la narration karmique
        karmic_narrative = self._generate_karmic_narrative(
            best_evaluation, event_data, historical_context
        ) if has_significance else None
        
        # Mettre à jour l'état karmique de l'entité
        self._update_entity_karmic_state(entity_id, entity_name, entity_type, amplified_potential, best_evaluation['pattern'])
        
        # Enregistrer l'analyse dans l'historique
        analysis_record = {
            'entity_id': entity_id,
            'entity_name': entity_name,
            'entity_type': entity_type,
            'event_type': event_type,
            'karmic_potential': amplified_potential,
            'primary_pattern': best_evaluation['pattern'],
            'timestamp': datetime.now().isoformat()
        }
        
        self.karmic_analysis_history.append(analysis_record)
        
        # Si l'événement est significatif, l'ajouter à la base de données d'histoires
        if has_significance:
            self.karmic_stories_db.append({
                'entity_id': entity_id,
                'entity_name': entity_name,
                'entity_type': entity_type,
                'pattern': best_evaluation['pattern'],
                'karmic_score': amplified_potential,
                'narrative': karmic_narrative,
                'timestamp': datetime.now().isoformat()
            })
        
        # Préparer le résultat
        result = {
            'entity_name': entity_name,
            'entity_type': entity_type,
            'event_type': event_type,
            'karmic_potential': amplified_potential,
            'base_potential': karmic_potential,
            'amplification_score': amplification,
            'detected_patterns': karmic_evaluations,
            'primary_pattern': best_evaluation['pattern'],
            'narrative_power': self.karmic_patterns[best_evaluation['pattern']]['narrative_power'],
            'emotional_impact': self.karmic_patterns[best_evaluation['pattern']]['emotional_impact'],
            'has_karmic_significance': has_significance,
            'karmic_narrative': karmic_narrative,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def identify_karmic_connections(self, entity_data, connection_type='team'):
        """
        Identifier les connexions karmiques d'une équipe ou d'un joueur.
        
        Args:
            entity_data (dict): Données de l'entité (équipe/joueur)
            connection_type (str): Type de connexion ('team', 'player', 'rivalry')
            
        Returns:
            dict: Connexions karmiques identifiées
        """
        # Extraire les informations de base
        entity_id = entity_data.get('id', '')
        entity_name = entity_data.get('name', '')
        entity_type = 'team' if connection_type in ['team', 'rivalry'] else 'player'
        
        # Récupérer l'historique des matchs/événements
        history = entity_data.get('match_history', [])
        
        if not history:
            return {
                'status': 'insufficient_data',
                'message': 'Historique insuffisant pour identifier des connexions karmiques'
            }
        
        # Initialiser les structures pour les connexions
        karmic_connections = {
            'rivalries': [],
            'nemesis': [],
            'favorable_opponents': [],
            'karmic_balance': {}
        }
        
        # Analyser différents types de connexions
        if connection_type in ['team', 'rivalry']:
            # Analyser les rivalités d'équipe
            karmic_connections['rivalries'] = self._identify_team_rivalries(entity_data, history)
            
            # Analyser les adversaires récurrents (nemesis et favorables)
            opponent_analysis = self._analyze_recurring_opponents(entity_data, history)
            karmic_connections['nemesis'] = opponent_analysis['nemesis']
            karmic_connections['favorable_opponents'] = opponent_analysis['favorable']
            
        elif connection_type == 'player':
            # Analyser les connexions de joueur à joueur
            karmic_connections['player_connections'] = self._identify_player_connections(entity_data, history)
            
            # Analyser les équipes avec lesquelles le joueur a une connexion
            karmic_connections['team_connections'] = self._identify_player_team_connections(entity_data, history)
        
        # Calculer la balance karmique globale
        karmic_balance = self._calculate_karmic_balance(entity_id, entity_type)
        karmic_connections['karmic_balance'] = karmic_balance
        
        # Identifier les moments karmiques clés dans l'histoire
        key_moments = self._identify_key_karmic_moments(entity_id, entity_type)
        
        # Préparer le résultat
        result = {
            'entity_name': entity_name,
            'entity_type': entity_type,
            'connection_type': connection_type,
            'karmic_connections': karmic_connections,
            'key_karmic_moments': key_moments,
            'overall_karmic_state': self._get_entity_karmic_state(entity_id),
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def predict_karmic_outcomes(self, match_data, historical_context=None):
        """
        Prédire les potentiels résultats karmiques pour un match à venir.
        
        Args:
            match_data (dict): Données du match à venir
            historical_context (dict, optional): Contexte historique supplémentaire
            
        Returns:
            dict: Prédictions basées sur l'analyse karmique
        """
        # Extraire les informations de base
        home_team = match_data.get('home_team', {})
        away_team = match_data.get('away_team', {})
        
        home_id = home_team.get('id', '')
        away_id = away_team.get('id', '')
        
        home_name = home_team.get('name', '')
        away_name = away_team.get('name', '')
        
        competition = match_data.get('competition', '')
        stage = match_data.get('stage', '')
        
        # Récupérer le contexte historique si non fourni
        if not historical_context:
            home_context = self._retrieve_historical_context(home_id, 'team')
            away_context = self._retrieve_historical_context(away_id, 'team')
            
            historical_context = {
                'home': home_context,
                'away': away_context,
                'head_to_head': self._retrieve_head_to_head(home_id, away_id)
            }
        
        # Identifier les patterns karmiques potentiels pour chaque équipe
        home_patterns = self._identify_potential_karmic_patterns(home_id, 'team', away_id, historical_context)
        away_patterns = self._identify_potential_karmic_patterns(away_id, 'team', home_id, historical_context)
        
        # Calculer les scores karmiques pour chaque équipe
        home_karmic_score = self._calculate_team_karmic_score(home_id, home_patterns, match_data)
        away_karmic_score = self._calculate_team_karmic_score(away_id, away_patterns, match_data)
        
        # Identifier quel côté a un potentiel karmique plus fort
        karmic_advantage = 'home' if home_karmic_score > away_karmic_score else ('away' if away_karmic_score > home_karmic_score else 'neutral')
        advantage_magnitude = abs(home_karmic_score - away_karmic_score)
        
        # Évaluer s'il y a un scenario karmique significatif dans ce match
        significant_scenario = advantage_magnitude > self.karmic_parameters['minimum_karma_score']
        
        # Générer les scenarios potentiels
        karmic_scenarios = self._generate_karmic_scenarios(
            home_team, away_team, home_patterns, away_patterns, karmic_advantage, advantage_magnitude
        )
        
        # Évaluer comment le karma pourrait influencer le résultat
        outcome_influence = self._evaluate_karmic_outcome_influence(
            home_karmic_score, away_karmic_score, match_data
        )
        
        # Préparer le résultat
        result = {
            'match': f"{home_name} vs {away_name}",
            'competition': competition,
            'stage': stage,
            'karmic_analysis': {
                'home_team': {
                    'name': home_name,
                    'karmic_score': home_karmic_score,
                    'potential_patterns': home_patterns
                },
                'away_team': {
                    'name': away_name,
                    'karmic_score': away_karmic_score,
                    'potential_patterns': away_patterns
                },
                'karmic_advantage': {
                    'team': home_name if karmic_advantage == 'home' else (away_name if karmic_advantage == 'away' else 'neutral'),
                    'magnitude': advantage_magnitude,
                    'description': f"{'Fort' if advantage_magnitude > 0.7 else 'Modéré' if advantage_magnitude > 0.4 else 'Léger'} avantage karmique"
                },
                'has_significant_scenario': significant_scenario
            },
            'karmic_scenarios': karmic_scenarios,
            'outcome_influence': outcome_influence,
            'prediction_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def generate_karmic_narrative(self, entity_data, narrative_type='season'):
        """
        Générer une narration karmique pour une entité sportive.
        
        Args:
            entity_data (dict): Données de l'entité (équipe/joueur)
            narrative_type (str): Type de narration ('season', 'career', 'moment')
            
        Returns:
            dict: Narration karmique générée
        """
        # Extraire les informations de base
        entity_id = entity_data.get('id', '')
        entity_name = entity_data.get('name', '')
        entity_type = entity_data.get('type', 'team')
        
        # Récupérer l'historique karmique
        karmic_history = []
        for record in self.karmic_analysis_history:
            if record['entity_id'] == entity_id:
                karmic_history.append(record)
        
        if not karmic_history:
            return {
                'status': 'insufficient_data',
                'message': 'Historique karmique insuffisant pour générer une narration'
            }
        
        # Trier par ordre chronologique
        karmic_history.sort(key=lambda x: x['timestamp'])
        
        # Identifier les moments karmiques clés
        key_moments = []
        for record in karmic_history:
            if record['karmic_potential'] > self.karmic_parameters['minimum_karma_score']:
                key_moments.append(record)
        
        # Structurer la narration selon le type demandé
        narrative_elements = []
        
        if narrative_type == 'season':
            # Narration de saison
            narrative_elements = self._generate_season_narrative(entity_data, key_moments)
            
        elif narrative_type == 'career':
            # Narration de carrière (pour joueur)
            if entity_type == 'player':
                narrative_elements = self._generate_career_narrative(entity_data, key_moments)
            else:
                narrative_elements = self._generate_long_term_narrative(entity_data, key_moments)
                
        elif narrative_type == 'moment':
            # Narration centrée sur un moment spécifique
            if key_moments:
                most_significant = max(key_moments, key=lambda x: x['karmic_potential'])
                narrative_elements = self._generate_moment_narrative(entity_data, most_significant)
        
        # Calculer l'arc karmique global
        karmic_arc = self._calculate_karmic_arc(karmic_history)
        
        # Préparer le résultat
        result = {
            'entity_name': entity_name,
            'entity_type': entity_type,
            'narrative_type': narrative_type,
            'narrative_elements': narrative_elements,
            'karmic_arc': karmic_arc,
            'key_moments_count': len(key_moments),
            'narrative_coherence': self._calculate_narrative_coherence(narrative_elements),
            'generation_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def _evaluate_karmic_pattern(self, pattern_name, event_data, historical_context):
        """Évaluer la correspondance d'un événement à un pattern karmique."""
        pattern_def = self.karmic_patterns[pattern_name]
        event_type = event_data.get('type', '')
        
        # Initialiser le score de correspondance
        match_score = 0.0
        relevance_factors = []
        
        # Évaluer selon le type de pattern
        if pattern_name == 'revenge':
            # Vérifier s'il y a un élément de revanche
            previous_defeat = False
            previous_opponent = event_data.get('opponent_id', '')
            
            if historical_context and 'previous_matches' in historical_context:
                for match in historical_context['previous_matches']:
                    if match.get('opponent_id', '') == previous_opponent and match.get('result', '') == 'loss':
                        previous_defeat = True
                        time_since = self._calculate_time_since(match.get('date', ''))
                        
                        # La revanche est plus forte si elle est encore fraîche
                        if time_since < 365:  # Moins d'un an
                            relevance_factors.append(('recent_defeat', 0.9))
                        elif time_since < 3*365:  # Moins de 3 ans
                            relevance_factors.append(('past_defeat', 0.7))
                        else:
                            relevance_factors.append(('old_defeat', 0.5))
                        
                        break
            
            if previous_defeat:
                if event_type == 'victory':
                    match_score = 0.9  # Forte correspondance
                elif event_type == 'draw':
                    match_score = 0.6  # Correspondance modérée
            
        elif pattern_name == 'redemption':
            # Vérifier s'il y a un élément de rédemption
            previous_failure = False
            same_stage = False
            same_competition = False
            
            if historical_context and 'previous_failures' in historical_context:
                for failure in historical_context['previous_failures']:
                    if failure.get('type', '') == event_data.get('context', ''):
                        previous_failure = True
                        if failure.get('stage', '') == event_data.get('stage', ''):
                            same_stage = True
                        if failure.get('competition', '') == event_data.get('competition', ''):
                            same_competition = True
                        
                        time_since = self._calculate_time_since(failure.get('date', ''))
                        if time_since < 365:  # Moins d'un an
                            relevance_factors.append(('recent_failure', 0.9))
                        elif time_since < 3*365:  # Moins de 3 ans
                            relevance_factors.append(('past_failure', 0.7))
                        else:
                            relevance_factors.append(('long_awaited_redemption', 0.8))
                        
                        break
            
            if previous_failure:
                if event_type == 'victory' or event_type == 'achievement':
                    base_score = 0.8
                    if same_stage:
                        base_score += 0.1
                    if same_competition:
                        base_score += 0.1
                    match_score = min(1.0, base_score)
            
        elif pattern_name == 'poetic_justice':
            # Vérifier s'il y a un élément de justice poétique
            if historical_context and 'controversies' in historical_context:
                for controversy in historical_context['controversies']:
                    related = (
                        controversy.get('opponent_id', '') == event_data.get('opponent_id', '') or
                        controversy.get('context', '') == event_data.get('context', '')
                    )
                    
                    if related:
                        # La justice poétique est plus forte si elle renverse une injustice
                        if controversy.get('type', '') == 'injustice' and event_type == 'victory':
                            match_score = 0.9
                            relevance_factors.append(('justice_served', 0.9))
                        # Ou si l'arroseur est arrosé
                        elif controversy.get('type', '') == 'behavior' and event_type == 'defeat':
                            match_score = 0.85
                            relevance_factors.append(('karma_payback', 0.85))
        
        elif pattern_name == 'long_awaited':
            # Vérifier s'il s'agit d'un accomplissement longtemps attendu
            if event_type == 'achievement':
                achievement_type = event_data.get('achievement_type', '')
                waiting_period = event_data.get('waiting_period', 0)
                
                if waiting_period > 10:  # Plus de 10 ans
                    match_score = 0.9
                    relevance_factors.append(('very_long_wait', 0.9))
                elif waiting_period > 5:  # Plus de 5 ans
                    match_score = 0.8
                    relevance_factors.append(('long_wait', 0.8))
                elif waiting_period > 2:  # Plus de 2 ans
                    match_score = 0.7
                    relevance_factors.append(('moderate_wait', 0.7))
        
        elif pattern_name == 'reversal_of_fortune':
            # Vérifier s'il s'agit d'un renversement dramatique
            match_situation = event_data.get('match_situation', {})
            
            if match_situation:
                was_losing = match_situation.get('was_losing', False)
                comeback = match_situation.get('comeback', False)
                last_minute = match_situation.get('last_minute', False)
                
                if was_losing and comeback:
                    base_score = 0.8
                    if last_minute:
                        base_score += 0.1
                    match_score = base_score
                    relevance_factors.append(('dramatic_comeback', base_score))
        
        elif pattern_name == 'nemesis':
            # Vérifier s'il s'agit d'un adversaire récurrent problématique
            opponent_id = event_data.get('opponent_id', '')
            
            if historical_context and 'opponent_record' in historical_context:
                for opponent, record in historical_context['opponent_record'].items():
                    if opponent == opponent_id:
                        losses = record.get('losses', 0)
                        total = record.get('total', 0)
                        
                        if total >= 5 and losses / total > 0.7:  # Plus de 70% de défaites
                            match_score = 0.85
                            relevance_factors.append(('historical_nemesis', 0.85))
                        elif total >= 3 and losses / total > 0.6:  # Plus de 60% de défaites
                            match_score = 0.7
                            relevance_factors.append(('recurring_problem', 0.7))
        
        # Préparer le résultat de l'évaluation
        evaluation = {
            'pattern': pattern_name,
            'pattern_description': pattern_def['description'],
            'match_score': match_score,
            'threshold': pattern_def['detection_threshold'],
            'relevance_factors': relevance_factors,
            'narrative_power': pattern_def['narrative_power'],
            'emotional_impact': pattern_def['emotional_impact']
        }
        
        return evaluation
    
    def _calculate_amplification_factors(self, event_data, historical_context):
        """Calculer les facteurs d'amplification du karma."""
        total_amplification = 0.0
        
        # Vérifier chaque facteur d'amplification
        
        # 1. Couverture médiatique
        media_coverage = event_data.get('media_coverage', 0.5)
        total_amplification += media_coverage * self.amplification_factors['media_coverage']
        
        # 2. Sentiment des fans
        fan_sentiment = event_data.get('fan_sentiment', 0.5)
        total_amplification += fan_sentiment * self.amplification_factors['fan_sentiment']
        
        # 3. Rivalité historique
        historical_rivalry = False
        if historical_context and 'rivalries' in historical_context:
            opponent_id = event_data.get('opponent_id', '')
            if opponent_id in historical_context['rivalries']:
                historical_rivalry = True
        
        if historical_rivalry:
            total_amplification += self.amplification_factors['historical_rivalry']
        
        # 4. Prestige de la compétition
        competition_type = event_data.get('competition_type', '')
        competition_prestige = 0.0
        
        if competition_type == 'international':
            competition_prestige = 1.0
        elif competition_type == 'continental':
            competition_prestige = 0.8
        elif competition_type == 'domestic_cup':
            competition_prestige = 0.6
        elif competition_type == 'league':
            competition_prestige = 0.5
        
        total_amplification += competition_prestige * self.amplification_factors['competition_prestige']
        
        # 5. Niveau de drame
        drama_level = event_data.get('drama_level', 0.0)
        total_amplification += drama_level * self.amplification_factors['drama_level']
        
        # 6. Caractère historique/record
        is_milestone = event_data.get('is_milestone', False)
        if is_milestone:
            total_amplification += self.amplification_factors['milestone']
        
        return total_amplification
    
    def _generate_karmic_narrative(self, pattern_evaluation, event_data, historical_context):
        """Générer une narration karmique pour un événement."""
        pattern_name = pattern_evaluation['pattern']
        entity_name = event_data.get('entity_name', '')
        event_type = event_data.get('type', '')
        opponent_name = event_data.get('opponent_name', '')
        
        # Éléments narratifs selon le pattern
        if pattern_name == 'revenge':
            narratives = [
                f"{entity_name} prend sa revanche après une défaite précédente contre {opponent_name}.",
                f"Les comptes sont soldés pour {entity_name} qui règle un vieux contentieux avec {opponent_name}.",
                f"La roue tourne en faveur de {entity_name} qui efface l'humiliation subie face à {opponent_name}."
            ]
            
        elif pattern_name == 'redemption':
            failure_type = event_data.get('context', 'ce contexte')
            narratives = [
                f"{entity_name} trouve sa rédemption après ses échecs précédents dans {failure_type}.",
                f"L'histoire est réécrite pour {entity_name} qui efface les déceptions passées.",
                f"Un nouveau chapitre s'ouvre pour {entity_name}, lavant les erreurs du passé."
            ]
            
        elif pattern_name == 'poetic_justice':
            narratives = [
                f"La justice poétique frappe pour {entity_name} dans un renversement de situation ironique.",
                f"Le destin offre un alignement parfait où {entity_name} trouve une conclusion appropriée.",
                f"Le karma sportif s'équilibre parfaitement dans cette situation pour {entity_name}."
            ]
            
        elif pattern_name == 'long_awaited':
            achievement = event_data.get('achievement_description', 'cet accomplissement')
            waiting_period = event_data.get('waiting_period', 'longtemps')
            narratives = [
                f"Après {waiting_period} ans d'attente, {entity_name} réalise enfin {achievement}.",
                f"La patience est récompensée pour {entity_name} qui atteint {achievement} après tant d'années.",
                f"Le long voyage de {entity_name} vers {achievement} trouve enfin sa conclusion."
            ]
            
        elif pattern_name == 'reversal_of_fortune':
            narratives = [
                f"Un renversement spectaculaire de situation pour {entity_name} qui change complètement le destin du match.",
                f"Le vent tourne dramatiquement en faveur de {entity_name} dans une démonstration de résilience.",
                f"Quand tout semblait perdu, {entity_name} réécrit le script dans un final improbable."
            ]
            
        elif pattern_name == 'nemesis':
            narratives = [
                f"{opponent_name} continue de jouer le rôle de bête noire pour {entity_name} dans une dynamique karmique persistante.",
                f"La malédiction de {opponent_name} frappe encore {entity_name}, perpétuant un cycle difficile à briser.",
                f"Les astres ne s'alignent jamais pour {entity_name} face à {opponent_name}, son éternel adversaire fatidique."
            ]
        
        else:
            # Narratif par défaut
            narratives = [
                f"Un moment chargé de signification karmique pour {entity_name}.",
                f"Le destin sportif de {entity_name} prend une tournure significative.",
                f"Les échos du passé résonnent fortement dans ce moment pour {entity_name}."
            ]
        
        # Sélectionner une narration aléatoire
        chosen_narrative = random.choice(narratives)
        
        # Enrichir avec des détails contextuels
        if historical_context:
            if 'key_events' in historical_context and historical_context['key_events']:
                key_event = historical_context['key_events'][0]
                key_event_desc = key_event.get('description', '')
                
                if key_event_desc:
                    chosen_narrative += f" Cela rappelle {key_event_desc}."
        
        return chosen_narrative
    
    def _retrieve_historical_context(self, entity_id, entity_type):
        """Récupérer le contexte historique pour une entité."""
        # Cette fonction simulerait la récupération de données historiques depuis une base de données
        # Pour cette implémentation, nous retournons un contexte fictif
        
        if entity_type == 'team':
            # Générer un contexte historique d'équipe fictif
            return {
                'previous_matches': [
                    {
                        'opponent_id': f"opp_{(int(entity_id) + 1) % 10}",
                        'result': 'loss',
                        'date': (datetime.now() - timedelta(days=180)).isoformat()
                    },
                    {
                        'opponent_id': f"opp_{(int(entity_id) + 2) % 10}",
                        'result': 'win',
                        'date': (datetime.now() - timedelta(days=90)).isoformat()
                    }
                ],
                'previous_failures': [
                    {
                        'type': 'final_loss',
                        'competition': 'League Cup',
                        'stage': 'final',
                        'date': (datetime.now() - timedelta(days=365)).isoformat()
                    }
                ],
                'controversies': [
                    {
                        'opponent_id': f"opp_{(int(entity_id) + 3) % 10}",
                        'type': 'injustice',
                        'context': 'referee_decision',
                        'date': (datetime.now() - timedelta(days=120)).isoformat()
                    }
                ],
                'rivalries': [f"opp_{(int(entity_id) + 1) % 10}", f"opp_{(int(entity_id) + 5) % 10}"],
                'opponent_record': {
                    f"opp_{(int(entity_id) + 1) % 10}": {'wins': 3, 'losses': 7, 'draws': 2, 'total': 12},
                    f"opp_{(int(entity_id) + 2) % 10}": {'wins': 5, 'losses': 2, 'draws': 3, 'total': 10}
                },
                'key_events': [
                    {
                        'type': 'historic_win',
                        'description': 'victoire historique en finale de 1999',
                        'date': '1999-05-26'
                    }
                ]
            }
        
        elif entity_type == 'player':
            # Générer un contexte historique de joueur fictif
            return {
                'career_highs': [
                    {
                        'type': 'trophy',
                        'competition': 'World Cup',
                        'date': (datetime.now() - timedelta(days=1000)).isoformat()
                    }
                ],
                'career_lows': [
                    {
                        'type': 'missed_penalty',
                        'competition': 'Champions League',
                        'stage': 'final',
                        'date': (datetime.now() - timedelta(days=730)).isoformat()
                    }
                ],
                'rivalries': [f"player_{(int(entity_id) + 10) % 50}", f"player_{(int(entity_id) + 15) % 50}"],
                'key_events': [
                    {
                        'type': 'debut',
                        'description': 'premier match professionnel en 2010',
                        'date': '2010-08-14'
                    }
                ]
            }
        
        # Si type non reconnu, retourner un contexte vide
        return {}
    
    def _retrieve_head_to_head(self, team_id1, team_id2):
        """Récupérer l'historique des confrontations directes entre deux équipes."""
        # Cette fonction simulerait la récupération depuis une base de données
        # Pour cette implémentation, nous retournons des données fictives
        
        return {
            'matches': [
                {
                    'date': (datetime.now() - timedelta(days=180)).isoformat(),
                    'winner': team_id1,
                    'score': '2-1'
                },
                {
                    'date': (datetime.now() - timedelta(days=365)).isoformat(),
                    'winner': team_id2,
                    'score': '3-0'
                },
                {
                    'date': (datetime.now() - timedelta(days=545)).isoformat(),
                    'winner': 'draw',
                    'score': '1-1'
                }
            ],
            'stats': {
                team_id1: {'wins': 3, 'losses': 2, 'draws': 2},
                team_id2: {'wins': 2, 'losses': 3, 'draws': 2}
            },
            'significant_events': [
                {
                    'type': 'red_card',
                    'player': f"player_{team_id1}_7",
                    'match_date': (datetime.now() - timedelta(days=180)).isoformat()
                },
                {
                    'type': 'last_minute_goal',
                    'player': f"player_{team_id2}_9",
                    'match_date': (datetime.now() - timedelta(days=545)).isoformat()
                }
            ]
        }
    
    def _update_entity_karmic_state(self, entity_id, entity_name, entity_type, karmic_score, pattern):
        """Mettre à jour l'état karmique d'une entité."""
        # Récupérer l'état actuel ou en créer un nouveau
        if entity_id in self.entity_karmic_states:
            current_state = self.entity_karmic_states[entity_id]
        else:
            current_state = {
                'entity_id': entity_id,
                'entity_name': entity_name,
                'entity_type': entity_type,
                'karmic_balance': 0.0,
                'dominant_pattern': None,
                'pattern_counts': {},
                'last_updated': None
            }
        
        # Mettre à jour la balance karmique
        # (les scores positifs augmentent la balance, les négatifs la diminuent)
        adjustment = karmic_score * 0.1  # Effet modéré de chaque événement
        current_state['karmic_balance'] += adjustment
        
        # Limiter la balance karmique entre -1 et 1
        current_state['karmic_balance'] = max(-1.0, min(1.0, current_state['karmic_balance']))
        
        # Mettre à jour le compteur de patterns
        if pattern in current_state['pattern_counts']:
            current_state['pattern_counts'][pattern] += 1
        else:
            current_state['pattern_counts'][pattern] = 1
        
        # Déterminer le pattern dominant
        dominant_pattern = max(current_state['pattern_counts'].items(), key=lambda x: x[1])[0]
        current_state['dominant_pattern'] = dominant_pattern
        
        # Mettre à jour la date de dernière mise à jour
        current_state['last_updated'] = datetime.now().isoformat()
        
        # Sauvegarder l'état mis à jour
        self.entity_karmic_states[entity_id] = current_state
    
    def _get_entity_karmic_state(self, entity_id):
        """Récupérer l'état karmique actuel d'une entité."""
        if entity_id in self.entity_karmic_states:
            return self.entity_karmic_states[entity_id]
        return None
    
    def _calculate_time_since(self, date_str):
        """Calculer le nombre de jours écoulés depuis une date."""
        try:
            event_date = datetime.fromisoformat(date_str)
            days_since = (datetime.now() - event_date).days
            return days_since
        except:
            return 1000  # Valeur par défaut élevée en cas d'erreur
    
    def _identify_team_rivalries(self, entity_data, history):
        """Identifier les rivalités d'équipe avec charge karmique."""
        rivalries = []
        
        # Extraire les adversaires de l'historique
        opponents = {}
        for match in history:
            opponent_id = match.get('opponent_id', '')
            opponent_name = match.get('opponent_name', '')
            
            if opponent_id and opponent_name:
                if opponent_id not in opponents:
                    opponents[opponent_id] = {
                        'id': opponent_id,
                        'name': opponent_name,
                        'matches': 0,
                        'intensity': 0.0,
                        'karmic_charge': 0.0,
                        'key_moments': []
                    }
                
                opponents[opponent_id]['matches'] += 1
                
                # Évaluer l'intensité et la charge karmique
                intensity_factor = match.get('intensity', 0.5)
                controversial = match.get('controversial', False)
                dramatic = match.get('dramatic', False)
                
                opponents[opponent_id]['intensity'] += intensity_factor
                
                if controversial or dramatic:
                    karmic_charge = 0.2
                    if controversial:
                        karmic_charge += 0.3
                    if dramatic:
                        karmic_charge += 0.2
                    
                    opponents[opponent_id]['karmic_charge'] += karmic_charge
                    
                    # Enregistrer comme moment clé
                    opponents[opponent_id]['key_moments'].append({
                        'date': match.get('date', ''),
                        'type': 'controversial' if controversial else 'dramatic',
                        'description': match.get('description', '')
                    })
        
        # Normaliser et sélectionner les véritables rivalités
        for opponent_id, data in opponents.items():
            if data['matches'] >= 5:  # Minimum de matchs
                # Normaliser l'intensité et la charge karmique
                data['intensity'] = data['intensity'] / data['matches']
                data['karmic_charge'] = min(1.0, data['karmic_charge'])
                
                # Calculer le score de rivalité
                rivalry_score = (data['intensity'] * 0.5) + (data['karmic_charge'] * 0.5)
                
                if rivalry_score > 0.6:  # Seuil de rivalité significative
                    rivalries.append({
                        'opponent_id': opponent_id,
                        'opponent_name': data['name'],
                        'rivalry_score': rivalry_score,
                        'karmic_charge': data['karmic_charge'],
                        'matches_played': data['matches'],
                        'key_moments': data['key_moments'][:3]  # Limiter aux 3 moments les plus significatifs
                    })
        
        # Trier par score de rivalité
        rivalries.sort(key=lambda x: x['rivalry_score'], reverse=True)
        
        return rivalries
    
    def _analyze_recurring_opponents(self, entity_data, history):
        """Analyser les adversaires récurrents pour identifier nemesis et équipes favorables."""
        opponent_records = {}
        
        # Compiler les résultats contre chaque adversaire
        for match in history:
            opponent_id = match.get('opponent_id', '')
            opponent_name = match.get('opponent_name', '')
            result = match.get('result', '')
            
            if opponent_id and opponent_name and result:
                if opponent_id not in opponent_records:
                    opponent_records[opponent_id] = {
                        'id': opponent_id,
                        'name': opponent_name,
                        'wins': 0,
                        'losses': 0,
                        'draws': 0,
                        'total': 0,
                        'karmic_factor': 0.0
                    }
                
                # Mettre à jour les statistiques
                opponent_records[opponent_id]['total'] += 1
                
                if result == 'win':
                    opponent_records[opponent_id]['wins'] += 1
                elif result == 'loss':
                    opponent_records[opponent_id]['losses'] += 1
                elif result == 'draw':
                    opponent_records[opponent_id]['draws'] += 1
                
                # Facteurs karmiques
                dramatic = match.get('dramatic', False)
                controversial = match.get('controversial', False)
                
                if dramatic or controversial:
                    opponent_records[opponent_id]['karmic_factor'] += 0.2
        
        # Identifier les nemesis (adversaires contre lesquels l'équipe a un mauvais bilan)
        nemesis = []
        favorites = []
        
        for opponent_id, record in opponent_records.items():
            if record['total'] >= 5:  # Minimum de matchs
                win_rate = record['wins'] / record['total']
                loss_rate = record['losses'] / record['total']
                
                # Calculer le différentiel
                win_loss_differential = win_rate - loss_rate
                
                # Nemesis: adversaires contre lesquels l'équipe perd souvent
                if win_loss_differential < -0.3 and record['karmic_factor'] > 0.0:
                    nemesis_score = abs(win_loss_differential) * (1 + record['karmic_factor'])
                    
                    nemesis.append({
                        'opponent_id': opponent_id,
                        'opponent_name': record['name'],
                        'win_rate': win_rate,
                        'loss_rate': loss_rate,
                        'nemesis_score': nemesis_score,
                        'karmic_factor': record['karmic_factor'],
                        'matches_played': record['total']
                    })
                
                # Équipes favorables: adversaires contre lesquels l'équipe gagne souvent
                elif win_loss_differential > 0.3:
                    favorable_score = win_loss_differential
                    
                    favorites.append({
                        'opponent_id': opponent_id,
                        'opponent_name': record['name'],
                        'win_rate': win_rate,
                        'favorable_score': favorable_score,
                        'matches_played': record['total']
                    })
        
        # Trier les listes
        nemesis.sort(key=lambda x: x['nemesis_score'], reverse=True)
        favorites.sort(key=lambda x: x['favorable_score'], reverse=True)
        
        return {
            'nemesis': nemesis,
            'favorable': favorites
        }
    
    def _identify_player_connections(self, entity_data, history):
        """Identifier les connexions karmiques entre joueurs."""
        # Pour un joueur, identifier ses connexions avec d'autres joueurs
        player_connections = []
        
        # Simuler des connexions karmiques
        # En production, cela serait calculé à partir de l'historique réel
        
        # Exemple de connexion rivale
        player_connections.append({
            'player_id': f"player_{(int(entity_data.get('id', '0')) + 10) % 50}",
            'player_name': f"Rival Player {(int(entity_data.get('id', '0')) + 10) % 50}",
            'connection_type': 'rival',
            'connection_strength': 0.85,
            'karmic_charge': 0.7,
            'key_moments': [
                {
                    'date': (datetime.now() - timedelta(days=180)).isoformat(),
                    'description': 'Confrontation directe en finale'
                }
            ]
        })
        
        # Exemple de connexion de mentorat
        player_connections.append({
            'player_id': f"player_{(int(entity_data.get('id', '0')) + 20) % 50}",
            'player_name': f"Mentor Player {(int(entity_data.get('id', '0')) + 20) % 50}",
            'connection_type': 'mentor',
            'connection_strength': 0.75,
            'karmic_charge': 0.6,
            'key_moments': [
                {
                    'date': (datetime.now() - timedelta(days=1000)).isoformat(),
                    'description': 'Première saison ensemble'
                }
            ]
        })
        
        return player_connections
    
    def _identify_player_team_connections(self, entity_data, history):
        """Identifier les connexions karmiques entre un joueur et des équipes."""
        # Pour un joueur, identifier ses connexions avec des équipes
        team_connections = []
        
        # Simuler des connexions karmiques
        # En production, cela serait calculé à partir de l'historique réel
        
        # Exemple de connexion avec ancienne équipe
        team_connections.append({
            'team_id': f"team_{(int(entity_data.get('id', '0')) % 10)}",
            'team_name': f"Former Team {(int(entity_data.get('id', '0')) % 10)}",
            'connection_type': 'former_team',
            'connection_strength': 0.8,
            'karmic_charge': 0.65,
            'key_moments': [
                {
                    'date': (datetime.now() - timedelta(days=1000)).isoformat(),
                    'description': 'Départ controversé'
                }
            ]
        })
        
        # Exemple de connexion avec équipe rivale
        team_connections.append({
            'team_id': f"team_{(int(entity_data.get('id', '0')) + 5) % 20}",
            'team_name': f"Rival Team {(int(entity_data.get('id', '0')) + 5) % 20}",
            'connection_type': 'rival_team',
            'connection_strength': 0.7,
            'karmic_charge': 0.75,
            'key_moments': [
                {
                    'date': (datetime.now() - timedelta(days=500)).isoformat(),
                    'description': 'But décisif contre cette équipe'
                }
            ]
        })
        
        return team_connections
    
    def _calculate_karmic_balance(self, entity_id, entity_type):
        """Calculer la balance karmique globale d'une entité."""
        # Récupérer l'état karmique actuel
        karmic_state = self._get_entity_karmic_state(entity_id)
        
        if karmic_state:
            balance = karmic_state['karmic_balance']
            
            # Déterminer l'état karmique
            if balance > 0.7:
                state = 'very_positive'
                description = 'Balance karmique très positive, en phase ascendante'
            elif balance > 0.3:
                state = 'positive'
                description = 'Balance karmique positive, devrait connaître des événements favorables'
            elif balance > -0.3:
                state = 'neutral'
                description = 'Balance karmique équilibrée, pas de tendance marquée'
            elif balance > -0.7:
                state = 'negative'
                description = 'Balance karmique négative, période potentiellement difficile'
            else:
                state = 'very_negative'
                description = 'Balance karmique très négative, doit surmonter des obstacles significatifs'
            
            return {
                'balance': balance,
                'state': state,
                'description': description,
                'dominant_pattern': karmic_state['dominant_pattern']
            }
        
        # Par défaut, retourner un état neutre
        return {
            'balance': 0.0,
            'state': 'neutral',
            'description': 'Balance karmique indéterminée, pas assez de données',
            'dominant_pattern': None
        }
    
    def _identify_key_karmic_moments(self, entity_id, entity_type):
        """Identifier les moments karmiques clés dans l'histoire d'une entité."""
        key_moments = []
        
        # Parcourir l'historique d'analyse karmique
        for record in self.karmic_analysis_history:
            if record['entity_id'] == entity_id:
                # Sélectionner les événements avec un potentiel karmique significatif
                if record['karmic_potential'] > self.karmic_parameters['minimum_karma_score']:
                    key_moments.append({
                        'date': datetime.fromisoformat(record['timestamp']).strftime('%Y-%m-%d'),
                        'pattern': record['primary_pattern'],
                        'karmic_score': record['karmic_potential'],
                        'event_type': record['event_type']
                    })
        
        # Trier par score karmique
        key_moments.sort(key=lambda x: x['karmic_score'], reverse=True)
        
        # Limiter aux 5 moments les plus significatifs
        return key_moments[:5]
    
    def _identify_potential_karmic_patterns(self, entity_id, entity_type, opponent_id, historical_context):
        """Identifier les patterns karmiques potentiels pour une entité dans un contexte donné."""
        potential_patterns = []
        
        # Récupérer l'état karmique actuel
        karmic_state = self._get_entity_karmic_state(entity_id)
        
        # Vérifier chaque type de pattern
        
        # 1. Vérifier le potentiel de revanche
        if opponent_id:
            # Vérifier l'historique des confrontations directes
            head_to_head = historical_context.get('head_to_head', {})
            matches = head_to_head.get('matches', [])
            
            recent_loss = False
            for match in matches[:3]:  # Vérifier les 3 derniers matchs
                if match.get('winner', '') == opponent_id:
                    recent_loss = True
                    break
            
            if recent_loss:
                potential_patterns.append({
                    'pattern': 'revenge',
                    'likelihood': 0.7,
                    'description': 'Possibilité de revanche sur une défaite récente',
                    'key_factor': 'recent_defeat'
                })
        
        # 2. Vérifier le potentiel de rédemption
        if entity_type == 'team':
            team_context = historical_context.get('home' if entity_id == head_to_head['stats'].keys()[0] else 'away', {})
            
            if 'previous_failures' in team_context:
                for failure in team_context['previous_failures']:
                    # Si échec récent dans un contexte similaire
                    if 'competition' in failure and 'stage' in failure:
                        potential_patterns.append({
                            'pattern': 'redemption',
                            'likelihood': 0.65,
                            'description': f"Possibilité de rédemption après l'échec en {failure['competition']}",
                            'key_factor': 'previous_failure'
                        })
                        break
        
        # 3. Vérifier le potentiel de justice poétique
        if 'significant_events' in head_to_head:
            for event in head_to_head['significant_events']:
                if event.get('type', '') in ['red_card', 'controversy', 'disputed_decision']:
                    potential_patterns.append({
                        'pattern': 'poetic_justice',
                        'likelihood': 0.6,
                        'description': 'Possibilité de justice poétique liée à un événement controversé précédent',
                        'key_factor': 'previous_controversy'
                    })
                    break
        
        # 4. Vérifier s'il s'agit d'un nemesis
        if opponent_id:
            stats = head_to_head.get('stats', {})
            
            if entity_id in stats and opponent_id in stats:
                entity_wins = stats[entity_id].get('wins', 0)
                entity_losses = stats[entity_id].get('losses', 0)
                
                if entity_losses > entity_wins * 1.5 and entity_losses >= 3:
                    potential_patterns.append({
                        'pattern': 'nemesis',
                        'likelihood': 0.75,
                        'description': 'Adversaire qui pose historiquement des problèmes',
                        'key_factor': 'historical_struggles'
                    })
        
        # 5. Vérifier le potentiel de renversement de fortune
        if karmic_state and karmic_state['karmic_balance'] < -0.3:
            potential_patterns.append({
                'pattern': 'reversal_of_fortune',
                'likelihood': 0.5 + abs(karmic_state['karmic_balance']) * 0.3,
                'description': 'Potentiel de renversement de fortune après une période difficile',
                'key_factor': 'karmic_buildup'
            })
        
        # Trier par probabilité
        potential_patterns.sort(key=lambda x: x['likelihood'], reverse=True)
        
        return potential_patterns
    
    def _calculate_team_karmic_score(self, team_id, patterns, match_data):
        """Calculer le score karmique global d'une équipe pour un match spécifique."""
        if not patterns:
            return 0.0
        
        # Base: l'état karmique actuel
        karmic_state = self._get_entity_karmic_state(team_id)
        base_score = karmic_state['karmic_balance'] if karmic_state else 0.0
        
        # Ajouter l'influence des patterns potentiels
        pattern_score = sum(pattern['likelihood'] * 0.2 for pattern in patterns)
        
        # Ajuster selon le contexte du match
        match_context_factor = 0.0
        
        competition_type = match_data.get('competition_type', '')
        if competition_type == 'knockout':
            match_context_factor += 0.2
        
        stage = match_data.get('stage', '')
        if stage in ['final', 'semi_final']:
            match_context_factor += 0.15
        
        # Calculer le score final
        karmic_score = base_score + pattern_score + match_context_factor
        
        # Limiter entre -1 et 1
        return max(-1.0, min(1.0, karmic_score))
    
    def _generate_karmic_scenarios(self, home_team, away_team, home_patterns, away_patterns, advantage, magnitude):
        """Générer des scénarios karmiques potentiels pour un match."""
        scenarios = []
        
        # Si l'avantage est suffisamment important
        if magnitude > 0.3:
            advantaged_team = home_team if advantage == 'home' else away_team
            advantaged_patterns = home_patterns if advantage == 'home' else away_patterns
            
            # Trouver le pattern le plus probable
            if advantaged_patterns:
                top_pattern = max(advantaged_patterns, key=lambda x: x['likelihood'])
                
                if top_pattern['pattern'] == 'revenge':
                    scenarios.append({
                        'type': 'revenge',
                        'description': f"{advantaged_team['name']} pourrait prendre sa revanche dans ce match",
                        'likelihood': top_pattern['likelihood'] * magnitude,
                        'karmic_strength': magnitude
                    })
                
                elif top_pattern['pattern'] == 'redemption':
                    scenarios.append({
                        'type': 'redemption',
                        'description': f"{advantaged_team['name']} a une opportunité de rédemption",
                        'likelihood': top_pattern['likelihood'] * magnitude,
                        'karmic_strength': magnitude
                    })
                
                elif top_pattern['pattern'] == 'nemesis':
                    disadvantaged_team = away_team if advantage == 'home' else home_team
                    scenarios.append({
                        'type': 'breaking_nemesis',
                        'description': f"{advantaged_team['name']} a l'opportunité de briser la malédiction contre {disadvantaged_team['name']}",
                        'likelihood': top_pattern['likelihood'] * magnitude,
                        'karmic_strength': magnitude
                    })
                
                elif top_pattern['pattern'] == 'reversal_of_fortune':
                    scenarios.append({
                        'type': 'karmic_shift',
                        'description': f"Un tournant karmique majeur pourrait se produire pour {advantaged_team['name']}",
                        'likelihood': top_pattern['likelihood'] * magnitude,
                        'karmic_strength': magnitude
                    })
        
        # Si les deux équipes ont des patterns forts, possibilité de drame karmique
        if home_patterns and away_patterns and magnitude < 0.4:
            top_home = max(home_patterns, key=lambda x: x['likelihood'])
            top_away = max(away_patterns, key=lambda x: x['likelihood'])
            
            if top_home['likelihood'] > 0.6 and top_away['likelihood'] > 0.6:
                scenarios.append({
                    'type': 'karmic_clash',
                    'description': f"Collision de forces karmiques entre {home_team['name']} et {away_team['name']}",
                    'likelihood': (top_home['likelihood'] + top_away['likelihood']) / 2,
                    'karmic_strength': max(top_home['likelihood'], top_away['likelihood'])
                })
        
        # Si peu d'avantage, possibilité de moment pivot
        if magnitude < 0.3 and (home_patterns or away_patterns):
            scenarios.append({
                'type': 'karmic_tipping_point',
                'description': "Un moment charnière pourrait basculer l'équilibre karmique dans ce match",
                'likelihood': 0.5 + magnitude,
                'karmic_strength': 0.5
            })
        
        return scenarios
    
    def _evaluate_karmic_outcome_influence(self, home_score, away_score, match_data):
        """Évaluer comment le karma pourrait influencer le résultat du match."""
        # Calculer la différence karmique
        karmic_diff = home_score - away_score
        
        # Évaluer l'influence potentielle
        if abs(karmic_diff) > 0.7:
            influence_level = 'strong'
            influence_description = "Forte influence karmique possible sur le résultat"
        elif abs(karmic_diff) > 0.4:
            influence_level = 'moderate'
            influence_description = "Influence karmique modérée sur le déroulement du match"
        else:
            influence_level = 'subtle'
            influence_description = "Subtile influence karmique, principalement sur des moments clés"
        
        # Déterminer la direction de l'influence
        influence_direction = 'home' if karmic_diff > 0 else ('away' if karmic_diff < 0 else 'neutral')
        
        # Suggérer des moments potentiels d'influence
        potential_moments = []
        
        if abs(karmic_diff) > 0.5:
            potential_moments.append("Décisions arbitrales controversées")
        
        if abs(karmic_diff) > 0.3:
            potential_moments.append("Moments de chance/malchance inhabituels")
        
        potential_moments.append("Performance exceptionnelle d'un joueur clé")
        
        return {
            'influence_level': influence_level,
            'influence_direction': influence_direction,
            'description': influence_description,
            'potential_manifestations': potential_moments,
            'karmic_differential': karmic_diff
        }
    
    def _generate_season_narrative(self, entity_data, key_moments):
        """Générer une narration de saison karmique."""
        # Générer des éléments narratifs pour une saison
        narrative_elements = []
        
        if not key_moments:
            # Narration par défaut si pas de moments clés
            narrative_elements.append({
                'type': 'season_overview',
                'content': f"Une saison relativement neutre sur le plan karmique pour {entity_data['name']}."
            })
            return narrative_elements
        
        # Ajouter une introduction
        narrative_elements.append({
            'type': 'season_introduction',
            'content': f"La saison de {entity_data['name']} a été marquée par plusieurs moments à forte charge karmique."
        })
        
        # Ajouter des éléments pour chaque moment clé
        for i, moment in enumerate(key_moments):
            if i == 0:
                # Premier moment - définissant
                narrative_elements.append({
                    'type': 'defining_moment',
                    'content': f"Un moment déterminant s'est produit le {moment['date']} : {self._describe_pattern(moment['pattern'])}"
                })
            else:
                # Autres moments
                narrative_elements.append({
                    'type': 'key_moment',
                    'content': f"Le {moment['date']}, un nouvel épisode karmique est survenu : {self._describe_pattern(moment['pattern'])}"
                })
        
        # Ajouter une conclusion
        karma_trend = self._determine_karma_trend(key_moments)
        
        if karma_trend == 'positive':
            narrative_elements.append({
                'type': 'season_conclusion',
                'content': f"Dans l'ensemble, la saison a montré une évolution karmique positive pour {entity_data['name']}, suggérant un alignement favorable des forces du destin sportif."
            })
        elif karma_trend == 'negative':
            narrative_elements.append({
                'type': 'season_conclusion',
                'content': f"La saison a révélé un déséquilibre karmique pour {entity_data['name']}, indiquant des défis persistants à surmonter."
            })
        else:
            narrative_elements.append({
                'type': 'season_conclusion',
                'content': f"La saison a présenté un équilibre karmique mixte pour {entity_data['name']}, avec des hauts et des bas significatifs."
            })
        
        return narrative_elements
    
    def _generate_career_narrative(self, entity_data, key_moments):
        """Générer une narration de carrière karmique pour un joueur."""
        # Générer des éléments narratifs pour une carrière
        narrative_elements = []
        
        if not key_moments:
            # Narration par défaut si pas de moments clés
            narrative_elements.append({
                'type': 'career_overview',
                'content': f"La carrière de {entity_data['name']} ne présente pas de motifs karmiques marqués à ce stade."
            })
            return narrative_elements
        
        # Ajouter une introduction
        narrative_elements.append({
            'type': 'career_introduction',
            'content': f"Le parcours de {entity_data['name']} révèle un tissu karmique complexe façonné par plusieurs moments clés."
        })
        
        # Regrouper les moments par patterns
        pattern_groups = {}
        for moment in key_moments:
            pattern = moment['pattern']
            if pattern not in pattern_groups:
                pattern_groups[pattern] = []
            pattern_groups[pattern].append(moment)
        
        # Créer des éléments narratifs pour chaque groupe de patterns
        for pattern, moments in pattern_groups.items():
            if len(moments) > 1:
                # Pattern récurrent
                narrative_elements.append({
                    'type': 'recurring_pattern',
                    'content': f"Un motif de {self._describe_pattern(pattern)} apparaît régulièrement dans la carrière de {entity_data['name']}, notamment en {', '.join([moment['date'].split('-')[0] for moment in moments])}."
                })
            else:
                # Événement unique
                narrative_elements.append({
                    'type': 'singular_moment',
                    'content': f"En {moments[0]['date'].split('-')[0]}, {entity_data['name']} a vécu un moment significatif de {self._describe_pattern(pattern)}."
                })
        
        # Ajouter une conclusion
        dominant_pattern = max(pattern_groups.items(), key=lambda x: len(x[1]))[0]
        
        narrative_elements.append({
            'type': 'career_theme',
            'content': f"Le thème dominant dans le parcours karmique de {entity_data['name']} semble être celui de {self._describe_pattern(dominant_pattern)}, façonnant profondément sa carrière."
        })
        
        return narrative_elements
    
    def _generate_long_term_narrative(self, entity_data, key_moments):
        """Générer une narration sur le long terme pour une équipe."""
        # Générer des éléments narratifs pour une équipe sur le long terme
        narrative_elements = []
        
        if not key_moments:
            # Narration par défaut si pas de moments clés
            narrative_elements.append({
                'type': 'long_term_overview',
                'content': f"L'histoire récente de {entity_data['name']} ne révèle pas de motif karmique clair."
            })
            return narrative_elements
        
        # Ajouter une introduction
        narrative_elements.append({
            'type': 'historical_introduction',
            'content': f"L'analyse de l'histoire récente de {entity_data['name']} révèle plusieurs courants karmiques entrelacés."
        })
        
        # Organiser les moments par année
        year_groups = {}
        for moment in key_moments:
            year = moment['date'].split('-')[0]
            if year not in year_groups:
                year_groups[year] = []
            year_groups[year].append(moment)
        
        # Créer des éléments narratifs pour chaque année
        for year, moments in sorted(year_groups.items()):
            if len(moments) > 1:
                # Année à forte concentration karmique
                narrative_elements.append({
                    'type': 'significant_year',
                    'content': f"L'année {year} a été particulièrement chargée karmiquement pour {entity_data['name']}, avec {len(moments)} moments significatifs."
                })
            else:
                # Année avec un seul moment
                narrative_elements.append({
                    'type': 'key_year_moment',
                    'content': f"En {year}, {entity_data['name']} a connu un moment karmique important : {self._describe_pattern(moments[0]['pattern'])}."
                })
        
        # Ajouter une tendance historique
        karma_cycle = self._identify_karma_cycle(key_moments)
        
        if karma_cycle:
            narrative_elements.append({
                'type': 'karmic_cycle',
                'content': f"Un cycle karmique de {karma_cycle} ans semble se dessiner dans l'histoire de {entity_data['name']}, suggérant des répétitions potentielles de certains schémas."
            })
        else:
            narrative_elements.append({
                'type': 'karmic_evolution',
                'content': f"L'évolution karmique de {entity_data['name']} semble suivre un chemin non cyclique, avec des développements uniques plutôt que répétitifs."
            })
        
        return narrative_elements
    
    def _generate_moment_narrative(self, entity_data, moment):
        """Générer une narration centrée sur un moment karmique spécifique."""
        # Générer des éléments narratifs pour un moment spécifique
        narrative_elements = []
        
        # Ajouter une introduction
        pattern_desc = self._describe_pattern(moment['pattern'])
        event_type = moment['event_type']
        
        narrative_elements.append({
            'type': 'moment_introduction',
            'content': f"Le {moment['date']}, {entity_data['name']} a vécu un moment karmique particulièrement puissant impliquant {pattern_desc}."
        })
        
        # Ajouter des détails sur le moment
        if event_type == 'victory':
            narrative_elements.append({
                'type': 'moment_detail',
                'content': f"Cette victoire n'était pas simplement un résultat sportif, mais l'aboutissement d'un arc karmique plus large."
            })
        elif event_type == 'defeat':
            narrative_elements.append({
                'type': 'moment_detail',
                'content': f"Cette défaite représentait un nœud karmique important, un moment charnière dans le parcours de {entity_data['name']}."
            })
        elif event_type == 'achievement':
            narrative_elements.append({
                'type': 'moment_detail',
                'content': f"Cet accomplissement s'inscrit dans une trame karmique plus large, donnant une signification particulière à cette réussite."
            })
        
        # Ajouter une interprétation
        if moment['pattern'] == 'revenge':
            narrative_elements.append({
                'type': 'moment_interpretation',
                'content': f"Ce moment de revanche a rééquilibré la balance karmique, effaçant une dette du passé sportif de {entity_data['name']}."
            })
        elif moment['pattern'] == 'redemption':
            narrative_elements.append({
                'type': 'moment_interpretation',
                'content': f"Cette rédemption a permis à {entity_data['name']} de transcender des échecs passés, transformant la souffrance en force."
            })
        elif moment['pattern'] == 'poetic_justice':
            narrative_elements.append({
                'type': 'moment_interpretation',
                'content': f"Dans un alignement parfait des forces karmiques, une justice poétique s'est manifestée pour {entity_data['name']}."
            })
        else:
            narrative_elements.append({
                'type': 'moment_interpretation',
                'content': f"Ce moment représente un nœud significatif dans le tissu karmique entourant {entity_data['name']}."
            })
        
        return narrative_elements
    
    def _calculate_karmic_arc(self, karmic_history):
        """Calculer l'arc karmique global à partir de l'historique."""
        if not karmic_history:
            return {
                'trend': 'neutral',
                'volatility': 'low',
                'current_direction': 'stable'
            }
        
        # Extraire les scores karmiques
        scores = [record['karmic_potential'] for record in karmic_history]
        
        # Calculer la tendance
        if len(scores) > 1:
            first_half = scores[:len(scores)//2]
            second_half = scores[len(scores)//2:]
            
            first_avg = sum(first_half) / len(first_half)
            second_avg = sum(second_half) / len(second_half)
            
            if second_avg > first_avg + 0.2:
                trend = 'ascending'
            elif first_avg > second_avg + 0.2:
                trend = 'descending'
            else:
                trend = 'stable'
        else:
            trend = 'neutral'
        
        # Calculer la volatilité
        if len(scores) > 2:
            differences = [abs(scores[i] - scores[i-1]) for i in range(1, len(scores))]
            avg_difference = sum(differences) / len(differences)
            
            if avg_difference > 0.4:
                volatility = 'high'
            elif avg_difference > 0.2:
                volatility = 'medium'
            else:
                volatility = 'low'
        else:
            volatility = 'low'
        
        # Déterminer la direction actuelle
        if len(scores) > 2:
            recent_scores = scores[-3:]
            if recent_scores[-1] > recent_scores[-2] > recent_scores[-3]:
                current_direction = 'upward'
            elif recent_scores[-1] < recent_scores[-2] < recent_scores[-3]:
                current_direction = 'downward'
            else:
                current_direction = 'fluctuating'
        else:
            current_direction = 'stable'
        
        return {
            'trend': trend,
            'volatility': volatility,
            'current_direction': current_direction
        }
    
    def _calculate_narrative_coherence(self, narrative_elements):
        """Calculer la cohérence d'une narration karmique."""
        if not narrative_elements or len(narrative_elements) < 2:
            return 0.5  # Cohérence moyenne par défaut
        
        # Évaluer la cohérence des types d'éléments
        types = [element['type'] for element in narrative_elements]
        type_consistency = len(set(types)) / len(types)  # Plus petit = plus cohérent
        
        # Inverser pour obtenir un score de cohérence (plus élevé = plus cohérent)
        type_coherence = 1 - (type_consistency * 0.5)  # Limiter l'impact
        
        # Évaluer la cohérence du contenu (implémentation simplifiée)
        content_coherence = 0.7  # Valeur par défaut raisonnable
        
        # Combiner les scores
        overall_coherence = (type_coherence * 0.4) + (content_coherence * 0.6)
        
        return overall_coherence
    
    def _determine_karma_trend(self, key_moments):
        """Déterminer la tendance karmique à partir des moments clés."""
        if not key_moments:
            return 'neutral'
        
        # Compter les patterns positifs et négatifs
        positive_patterns = ['redemption', 'long_awaited', 'revenge']
        negative_patterns = ['nemesis', 'poetic_justice']  # Si l'entité est du côté négatif
        
        positive_count = sum(1 for moment in key_moments if moment['pattern'] in positive_patterns)
        negative_count = sum(1 for moment in key_moments if moment['pattern'] in negative_patterns)
        
        if positive_count > negative_count * 1.5:
            return 'positive'
        elif negative_count > positive_count * 1.5:
            return 'negative'
        else:
            return 'mixed'
    
    def _identify_karma_cycle(self, key_moments):
        """Identifier un potentiel cycle karmique dans les moments clés."""
        if len(key_moments) < 4:
            return None
        
        # Extraire les années
        years = [int(moment['date'].split('-')[0]) for moment in key_moments]
        years.sort()
        
        # Vérifier différentes longueurs de cycle
        for cycle_length in range(2, 10):  # 2 à 10 ans
            matches = 0
            
            for i in range(len(years)):
                for j in range(i + 1, len(years)):
                    if (years[j] - years[i]) % cycle_length == 0:
                        matches += 1
            
            # Si suffisamment de correspondances, c'est un cycle potentiel
            if matches >= len(years) // 2:
                return cycle_length
        
        return None
    
    def _describe_pattern(self, pattern):
        """Fournir une description textuelle d'un pattern karmique."""
        descriptions = {
            'revenge': 'revanche',
            'redemption': 'rédemption',
            'poetic_justice': 'justice poétique',
            'long_awaited': 'accomplissement longuement attendu',
            'reversal_of_fortune': 'renversement de fortune',
            'nemesis': 'confrontation avec un adversaire fatidique'
        }
        
        return descriptions.get(pattern, pattern)