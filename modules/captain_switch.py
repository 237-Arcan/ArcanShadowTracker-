"""
CaptainSwitch - Module d'analyse de l'impact des changements de capitaine.
Évalue l'influence potentielle et observée de modifications du leadership sur la dynamique d'équipe.
"""

import numpy as np
import random
from datetime import datetime, timedelta
import json
import os
from collections import deque

class CaptainSwitch:
    """
    CaptainSwitch - Analyse l'impact des changements de capitaine sur la performance d'équipe.
    Évalue les conséquences des modifications de leadership sur la dynamique collective et les résultats.
    """
    
    def __init__(self):
        """Initialise le module CaptainSwitch."""
        # Facteurs d'influence du capitaine
        self.leadership_factors = {
            'experience': 0.2,          # Expérience globale
            'tenure': 0.15,             # Ancienneté dans l'équipe
            'leadership_quality': 0.25, # Qualités de leadership
            'performance_level': 0.15,  # Niveau de performance
            'squad_respect': 0.15,      # Respect dans le vestiaire
            'media_handling': 0.1       # Gestion des médias
        }
        
        # Types de capitaines et leurs caractéristiques
        self.captain_types = {
            'vocal_leader': {
                'description': 'Leader vocal qui motive et organise sur le terrain',
                'impact_areas': {
                    'communication': 0.9,
                    'motivation': 0.8,
                    'tactical_organization': 0.7,
                    'referee_management': 0.8,
                    'crisis_management': 0.6
                }
            },
            'lead_by_example': {
                'description': 'Leader par l\'exemple qui inspire par ses performances',
                'impact_areas': {
                    'communication': 0.5,
                    'motivation': 0.7,
                    'tactical_organization': 0.5,
                    'referee_management': 0.4,
                    'crisis_management': 0.6
                }
            },
            'tactical_leader': {
                'description': 'Leader tactique qui organise et ajuste sur le terrain',
                'impact_areas': {
                    'communication': 0.7,
                    'motivation': 0.5,
                    'tactical_organization': 0.9,
                    'referee_management': 0.6,
                    'crisis_management': 0.7
                }
            },
            'club_ambassador': {
                'description': 'Ambassadeur du club avec forte influence institutionnelle',
                'impact_areas': {
                    'communication': 0.8,
                    'motivation': 0.6,
                    'tactical_organization': 0.4,
                    'referee_management': 0.5,
                    'crisis_management': 0.5
                }
            },
            'emerging_leader': {
                'description': 'Jeune leader en développement avec potentiel',
                'impact_areas': {
                    'communication': 0.6,
                    'motivation': 0.7,
                    'tactical_organization': 0.5,
                    'referee_management': 0.4,
                    'crisis_management': 0.4
                }
            }
        }
        
        # Types de transitions de capitaine
        self.transition_types = {
            'natural_succession': {
                'description': 'Succession planifiée avec transition fluide',
                'disruption_factor': 0.2,
                'adaptation_period': 3  # Matchs
            },
            'emergency_change': {
                'description': 'Changement d\'urgence suite à blessure/suspension',
                'disruption_factor': 0.6,
                'adaptation_period': 5
            },
            'tactical_switch': {
                'description': 'Changement tactique pour modifier la dynamique',
                'disruption_factor': 0.4,
                'adaptation_period': 4
            },
            'hierarchy_shift': {
                'description': 'Changement dans la hiérarchie du vestiaire',
                'disruption_factor': 0.7,
                'adaptation_period': 6
            },
            'generational_change': {
                'description': 'Passage à une nouvelle génération de leaders',
                'disruption_factor': 0.5,
                'adaptation_period': 8
            }
        }
        
        # Historique des analyses de capitaines
        self.captain_analysis_history = []
        
        # Suivi des changements de capitaine
        self.captain_switches = []
    
    def analyze_captain_impact(self, captain_data, team_data, match_data=None):
        """
        Analyser l'impact d'un capitaine sur son équipe.
        
        Args:
            captain_data (dict): Données du capitaine
            team_data (dict): Données de l'équipe
            match_data (dict, optional): Données du match pour analyse contextuelle
            
        Returns:
            dict: Analyse de l'impact du capitaine
        """
        # Extraire les informations pertinentes
        captain_id = captain_data.get('id', '')
        captain_name = captain_data.get('name', '')
        team_name = team_data.get('name', '')
        
        # Facteurs d'évaluation du leadership
        captain_experience = captain_data.get('experience', 0.5)  # 0-1
        team_tenure = captain_data.get('team_tenure', 0.5)  # 0-1
        leadership_rating = captain_data.get('leadership', 0.5)  # 0-1
        current_form = captain_data.get('current_form', 0.5)  # 0-1
        squad_respect = captain_data.get('squad_respect', 0.5)  # 0-1
        media_skills = captain_data.get('media_handling', 0.5)  # 0-1
        
        # Calculer le score de leadership global
        leadership_score = (
            captain_experience * self.leadership_factors['experience'] +
            team_tenure * self.leadership_factors['tenure'] +
            leadership_rating * self.leadership_factors['leadership_quality'] +
            current_form * self.leadership_factors['performance_level'] +
            squad_respect * self.leadership_factors['squad_respect'] +
            media_skills * self.leadership_factors['media_handling']
        )
        
        # Déterminer le type de capitaine
        captain_type, type_confidence = self._determine_captain_type(captain_data)
        
        # Évaluer l'adéquation avec les besoins de l'équipe
        team_needs = self._assess_team_leadership_needs(team_data)
        match_needs = None
        if match_data:
            match_needs = self._assess_match_leadership_needs(match_data)
        
        # Calculer l'adéquation
        team_fit = self._calculate_leadership_fit(captain_type, team_needs)
        match_fit = None
        if match_needs:
            match_fit = self._calculate_leadership_fit(captain_type, match_needs)
        
        # Évaluer les domaines d'influence spécifiques
        impact_areas = {}
        if captain_type in self.captain_types:
            base_impacts = self.captain_types[captain_type]['impact_areas']
            
            # Ajuster les impacts selon le leadership_score
            for area, base_value in base_impacts.items():
                adjusted_impact = base_value * leadership_score
                impact_areas[area] = adjusted_impact
        
        # Évaluer l'impact global sur l'équipe
        overall_impact = leadership_score * (team_fit if team_fit else 0.5)
        
        # Préparer le résultat
        result = {
            'captain_name': captain_name,
            'team_name': team_name,
            'leadership_score': leadership_score,
            'captain_type': captain_type,
            'type_confidence': type_confidence,
            'team_fit': team_fit,
            'match_fit': match_fit,
            'impact_areas': impact_areas,
            'overall_impact': overall_impact,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        # Enregistrer l'analyse dans l'historique
        self.captain_analysis_history.append({
            'captain_id': captain_id,
            'timestamp': datetime.now().isoformat(),
            'leadership_score': leadership_score,
            'overall_impact': overall_impact
        })
        
        return result
    
    def analyze_captain_switch(self, previous_captain, new_captain, team_data, transition_context=None):
        """
        Analyser l'impact d'un changement de capitaine.
        
        Args:
            previous_captain (dict): Données de l'ancien capitaine
            new_captain (dict): Données du nouveau capitaine
            team_data (dict): Données de l'équipe
            transition_context (dict, optional): Contexte de la transition
            
        Returns:
            dict: Analyse de l'impact du changement de capitaine
        """
        # Extraire les informations pertinentes
        previous_id = previous_captain.get('id', '')
        previous_name = previous_captain.get('name', '')
        new_id = new_captain.get('id', '')
        new_name = new_captain.get('name', '')
        team_name = team_data.get('name', '')
        
        # Analyser chaque capitaine individuellement
        previous_analysis = self.analyze_captain_impact(previous_captain, team_data)
        new_analysis = self.analyze_captain_impact(new_captain, team_data)
        
        # Déterminer le type de transition
        transition_type = self._determine_transition_type(
            previous_captain, new_captain, transition_context
        )
        
        # Facteurs de la transition
        disruption_factor = self.transition_types[transition_type]['disruption_factor']
        adaptation_period = self.transition_types[transition_type]['adaptation_period']
        
        # Calculer le différentiel de leadership
        leadership_change = new_analysis['leadership_score'] - previous_analysis['leadership_score']
        
        # Calculer le différentiel d'impact
        impact_change = new_analysis['overall_impact'] - previous_analysis['overall_impact']
        
        # Évaluer le changement dans les domaines d'influence
        impact_area_changes = {}
        for area in set(list(previous_analysis['impact_areas'].keys()) + list(new_analysis['impact_areas'].keys())):
            prev_value = previous_analysis['impact_areas'].get(area, 0)
            new_value = new_analysis['impact_areas'].get(area, 0)
            impact_area_changes[area] = new_value - prev_value
        
        # Calculer l'impact à court et long terme
        short_term_impact = impact_change - disruption_factor
        long_term_impact = impact_change
        
        # Prédire les changements dans la dynamique d'équipe
        team_dynamics_prediction = self._predict_team_dynamics_changes(
            previous_analysis, new_analysis, transition_type, team_data
        )
        
        # Enregistrer le changement de capitaine
        switch_record = {
            'timestamp': datetime.now().isoformat(),
            'previous_captain': {
                'id': previous_id,
                'name': previous_name,
                'leadership_score': previous_analysis['leadership_score']
            },
            'new_captain': {
                'id': new_id,
                'name': new_name,
                'leadership_score': new_analysis['leadership_score']
            },
            'transition_type': transition_type,
            'leadership_change': leadership_change,
            'short_term_impact': short_term_impact,
            'adaptation_period': adaptation_period
        }
        
        self.captain_switches.append(switch_record)
        
        # Préparer le résultat
        result = {
            'previous_captain': {
                'name': previous_name,
                'type': previous_analysis['captain_type'],
                'leadership_score': previous_analysis['leadership_score']
            },
            'new_captain': {
                'name': new_name,
                'type': new_analysis['captain_type'],
                'leadership_score': new_analysis['leadership_score']
            },
            'transition_type': transition_type,
            'transition_description': self.transition_types[transition_type]['description'],
            'leadership_change': leadership_change,
            'impact_change': impact_change,
            'impact_area_changes': impact_area_changes,
            'short_term_impact': short_term_impact,
            'long_term_impact': long_term_impact,
            'disruption_factor': disruption_factor,
            'adaptation_period': adaptation_period,
            'team_dynamics_prediction': team_dynamics_prediction,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def track_captain_transition(self, team_id, matches_after_switch, baseline_results=None):
        """
        Suivre une transition de capitaine sur une série de matchs pour en évaluer l'impact.
        
        Args:
            team_id (str): Identifiant de l'équipe
            matches_after_switch (list): Résultats des matchs après le changement
            baseline_results (list, optional): Résultats avant le changement pour comparaison
            
        Returns:
            dict: Analyse de l'évolution post-changement
        """
        # Vérifier si des données sont disponibles
        if not matches_after_switch:
            return {
                'status': 'error',
                'message': 'Aucune donnée de match fournie'
            }
        
        # Chercher le changement de capitaine le plus récent pour cette équipe
        latest_switch = None
        for switch in reversed(self.captain_switches):
            if switch.get('team_id', '') == team_id:
                latest_switch = switch
                break
        
        if not latest_switch:
            return {
                'status': 'error',
                'message': 'Aucun changement de capitaine enregistré pour cette équipe'
            }
        
        # Extraire les informations de la transition
        transition_type = latest_switch.get('transition_type', 'natural_succession')
        adaptation_period = self.transition_types[transition_type]['adaptation_period']
        disruption_factor = self.transition_types[transition_type]['disruption_factor']
        
        # Diviser les matchs en périodes d'adaptation
        adaptation_matches = []
        post_adaptation_matches = []
        
        for i, match in enumerate(matches_after_switch):
            if i < adaptation_period:
                adaptation_matches.append(match)
            else:
                post_adaptation_matches.append(match)
        
        # Analyser les résultats pour chaque période
        adaptation_performance = self._analyze_period_performance(adaptation_matches)
        post_adaptation_performance = self._analyze_period_performance(post_adaptation_matches)
        
        # Comparer avec les performances de base si disponibles
        baseline_performance = None
        if baseline_results:
            baseline_performance = self._analyze_period_performance(baseline_results)
        
        # Collecter les indicateurs de leadership
        leadership_indicators = self._extract_leadership_indicators(matches_after_switch, latest_switch)
        
        # Évaluer si l'adaptation est terminée
        adaptation_complete = len(matches_after_switch) >= adaptation_period
        
        # Calculer les différentiels de performance
        performance_differentials = {}
        
        if baseline_performance:
            # Comparer avec la période précédente
            for metric in baseline_performance:
                if metric in post_adaptation_performance:
                    performance_differentials[metric] = post_adaptation_performance[metric] - baseline_performance[metric]
        
        # Déterminer l'impact global du changement
        impact_assessment = 'neutral'
        impact_score = 0.0
        
        if performance_differentials:
            # Utiliser les différentiels de performance clés
            win_diff = performance_differentials.get('win_percentage', 0)
            goals_diff = performance_differentials.get('avg_goals_scored', 0)
            conceded_diff = performance_differentials.get('avg_goals_conceded', 0) * -1  # Inverser pour que positif = meilleur
            
            # Calculer un score d'impact
            impact_score = (win_diff * 0.5) + (goals_diff * 0.25) + (conceded_diff * 0.25)
            
            # Classifier l'impact
            if impact_score > 0.1:
                impact_assessment = 'positive'
            elif impact_score < -0.1:
                impact_assessment = 'negative'
        
        # Préparer le résultat
        result = {
            'switch_date': latest_switch.get('timestamp', ''),
            'previous_captain': latest_switch.get('previous_captain', {}),
            'new_captain': latest_switch.get('new_captain', {}),
            'transition_type': transition_type,
            'adaptation_period': {
                'expected_length': adaptation_period,
                'matches_elapsed': len(adaptation_matches),
                'complete': adaptation_complete,
                'performance': adaptation_performance
            },
            'post_adaptation_period': {
                'matches': len(post_adaptation_matches),
                'performance': post_adaptation_performance
            },
            'baseline_performance': baseline_performance,
            'performance_differentials': performance_differentials,
            'leadership_indicators': leadership_indicators,
            'impact_assessment': {
                'score': impact_score,
                'category': impact_assessment,
                'confidence': min(1.0, len(matches_after_switch) / (adaptation_period * 2))  # Confiance basée sur le nombre de matchs
            },
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def predict_captain_suitability(self, candidate_data, team_data, season_context=None):
        """
        Prédire l'adéquation d'un joueur comme futur capitaine.
        
        Args:
            candidate_data (dict): Données du joueur candidat
            team_data (dict): Données de l'équipe
            season_context (dict, optional): Contexte de la saison
            
        Returns:
            dict: Évaluation du potentiel comme capitaine
        """
        # Extraire les informations pertinentes
        candidate_id = candidate_data.get('id', '')
        candidate_name = candidate_data.get('name', '')
        
        # Évaluer les attributs de leadership
        leadership_attributes = self._evaluate_leadership_attributes(candidate_data)
        
        # Évaluer les besoins actuels de l'équipe
        team_needs = self._assess_team_leadership_needs(team_data)
        
        # Prédire le type de capitaine
        predicted_type, type_confidence = self._determine_captain_type(candidate_data)
        
        # Calculer l'adéquation aux besoins
        team_fit = self._calculate_leadership_fit(predicted_type, team_needs)
        
        # Calculer le score de potentiel comme capitaine
        leadership_potential = (
            leadership_attributes['overall'] * 0.6 +
            team_fit * 0.4
        )
        
        # Facteurs contextuels qui pourraient influencer la décision
        contextual_factors = []
        
        if season_context:
            # Facteurs de saison pertinents
            if season_context.get('rebuilding_phase', False):
                contextual_factors.append({
                    'factor': 'rebuilding_phase',
                    'impact': 'positive' if leadership_attributes['inspiring'] > 0.7 else 'neutral',
                    'importance': 'high'
                })
            
            if season_context.get('title_challenge', False):
                contextual_factors.append({
                    'factor': 'title_challenge',
                    'impact': 'positive' if leadership_attributes['pressure_handling'] > 0.7 else 'negative',
                    'importance': 'high'
                })
            
            if season_context.get('young_squad', False):
                contextual_factors.append({
                    'factor': 'young_squad',
                    'impact': 'positive' if leadership_attributes['mentoring'] > 0.6 else 'neutral',
                    'importance': 'medium'
                })
        
        # Évaluer les forces et faiblesses comme capitaine
        strengths = []
        weaknesses = []
        
        for attr, score in leadership_attributes.items():
            if attr != 'overall' and score > 0.75:
                strengths.append({
                    'attribute': attr,
                    'score': score,
                    'description': self._get_leadership_attribute_description(attr, score)
                })
            elif attr != 'overall' and score < 0.4:
                weaknesses.append({
                    'attribute': attr,
                    'score': score,
                    'description': self._get_leadership_attribute_description(attr, score)
                })
        
        # Générer des recommandations
        recommendations = self._generate_captain_recommendations(
            candidate_data, leadership_attributes, team_fit, team_needs
        )
        
        # Classifier le potentiel
        potential_category = 'average'
        if leadership_potential > 0.8:
            potential_category = 'excellent'
        elif leadership_potential > 0.65:
            potential_category = 'good'
        elif leadership_potential < 0.4:
            potential_category = 'poor'
        
        # Préparer le résultat
        result = {
            'candidate_name': candidate_name,
            'leadership_attributes': leadership_attributes,
            'predicted_captain_type': predicted_type,
            'type_confidence': type_confidence,
            'team_fit': team_fit,
            'leadership_potential': leadership_potential,
            'potential_category': potential_category,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'contextual_factors': contextual_factors,
            'recommendations': recommendations,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def _determine_captain_type(self, captain_data):
        """Déterminer le type de capitaine en fonction des caractéristiques du joueur."""
        # Extraire les attributs pertinents
        vocal_leadership = captain_data.get('attributes', {}).get('vocal_leadership', 0.5)
        leading_by_example = captain_data.get('attributes', {}).get('leading_by_example', 0.5)
        tactical_awareness = captain_data.get('attributes', {}).get('tactical_awareness', 0.5)
        club_loyalty = captain_data.get('attributes', {}).get('club_loyalty', 0.5)
        age = captain_data.get('age', 28)
        
        # Calculer les scores pour chaque type
        type_scores = {
            'vocal_leader': vocal_leadership * 0.8 + tactical_awareness * 0.2,
            'lead_by_example': leading_by_example * 0.9 + vocal_leadership * 0.1,
            'tactical_leader': tactical_awareness * 0.7 + vocal_leadership * 0.3,
            'club_ambassador': club_loyalty * 0.7 + vocal_leadership * 0.3,
            'emerging_leader': 0.0  # Par défaut
        }
        
        # Ajuster pour les jeunes leaders
        if age < 24:
            emerging_score = 0.7 + (leading_by_example * 0.1) + (vocal_leadership * 0.1) + (tactical_awareness * 0.1)
            type_scores['emerging_leader'] = emerging_score
        
        # Trouver le type avec le score le plus élevé
        best_type = max(type_scores.items(), key=lambda x: x[1])
        
        # Calculer la confiance (écart avec le deuxième score le plus élevé)
        sorted_scores = sorted(type_scores.values(), reverse=True)
        confidence = 0.5
        if len(sorted_scores) > 1:
            confidence = min(1.0, (sorted_scores[0] - sorted_scores[1]) * 2 + 0.5)
        
        return best_type[0], confidence
    
    def _assess_team_leadership_needs(self, team_data):
        """Évaluer les besoins de leadership actuels de l'équipe."""
        # Extraire les informations pertinentes
        team_experience = team_data.get('squad_experience', 0.5)  # 0-1
        discipline_issues = team_data.get('discipline_issues', 0.3)  # 0-1
        tactical_complexity = team_data.get('tactical_complexity', 0.5)  # 0-1
        season_pressure = team_data.get('season_pressure', 0.5)  # 0-1
        dressing_room_harmony = team_data.get('dressing_room_harmony', 0.7)  # 0-1
        
        # Calculer les besoins spécifiques
        communication_need = (1 - team_experience) * 0.7 + tactical_complexity * 0.3
        motivation_need = (1 - dressing_room_harmony) * 0.6 + season_pressure * 0.4
        tactical_need = tactical_complexity * 0.8 + (1 - team_experience) * 0.2
        referee_need = discipline_issues * 0.8 + season_pressure * 0.2
        crisis_need = (1 - dressing_room_harmony) * 0.4 + season_pressure * 0.6
        
        return {
            'communication': communication_need,
            'motivation': motivation_need,
            'tactical_organization': tactical_need,
            'referee_management': referee_need,
            'crisis_management': crisis_need
        }
    
    def _assess_match_leadership_needs(self, match_data):
        """Évaluer les besoins de leadership spécifiques à un match."""
        # Extraire les informations pertinentes
        match_importance = match_data.get('importance', 0.5)  # 0-1
        opponent_quality = match_data.get('opponent_quality', 0.5)  # 0-1
        referee_strictness = match_data.get('referee_strictness', 0.5)  # 0-1
        tactical_challenge = match_data.get('tactical_challenge', 0.5)  # 0-1
        external_pressure = match_data.get('external_pressure', 0.5)  # 0-1
        
        # Calculer les besoins spécifiques pour ce match
        communication_need = tactical_challenge * 0.7 + opponent_quality * 0.3
        motivation_need = match_importance * 0.8 + external_pressure * 0.2
        tactical_need = tactical_challenge * 0.9 + opponent_quality * 0.1
        referee_need = referee_strictness * 0.8 + match_importance * 0.2
        crisis_need = match_importance * 0.5 + opponent_quality * 0.3 + external_pressure * 0.2
        
        return {
            'communication': communication_need,
            'motivation': motivation_need,
            'tactical_organization': tactical_need,
            'referee_management': referee_need,
            'crisis_management': crisis_need
        }
    
    def _calculate_leadership_fit(self, captain_type, leadership_needs):
        """Calculer l'adéquation entre le type de capitaine et les besoins de leadership."""
        if captain_type not in self.captain_types:
            return 0.5  # Valeur par défaut si type inconnu
        
        # Récupérer les caractéristiques du type de capitaine
        captain_impact_areas = self.captain_types[captain_type]['impact_areas']
        
        # Calculer la correspondance pondérée
        weighted_match = 0.0
        total_need = 0.0
        
        for area, need in leadership_needs.items():
            if area in captain_impact_areas:
                area_match = captain_impact_areas[area] * need
                weighted_match += area_match
                total_need += need
        
        # Normaliser le résultat
        if total_need > 0:
            return weighted_match / total_need
        else:
            return 0.5
    
    def _determine_transition_type(self, previous_captain, new_captain, transition_context=None):
        """Déterminer le type de transition de capitaine."""
        # Par défaut, considérer comme succession naturelle
        default_type = 'natural_succession'
        
        if not transition_context:
            return default_type
        
        # Extraire les informations du contexte
        reason = transition_context.get('reason', '')
        urgency = transition_context.get('urgency', 'planned')
        age_gap = new_captain.get('age', 28) - previous_captain.get('age', 30)
        
        # Déterminer le type selon le contexte
        if 'injury' in reason.lower() or 'suspension' in reason.lower() or urgency == 'emergency':
            return 'emergency_change'
        
        if 'tactical' in reason.lower() or 'form' in reason.lower():
            return 'tactical_switch'
        
        if 'dressing_room' in reason.lower() or 'conflict' in reason.lower():
            return 'hierarchy_shift'
        
        if age_gap < -5 or 'generation' in reason.lower():
            return 'generational_change'
        
        # Si aucun critère spécifique, retourner le type par défaut
        return default_type
    
    def _predict_team_dynamics_changes(self, previous_analysis, new_analysis, transition_type, team_data):
        """Prédire les changements dans la dynamique d'équipe suite à un changement de capitaine."""
        # Récupérer les caractéristiques de l'équipe
        team_experience = team_data.get('squad_experience', 0.5)
        squad_adaptability = team_data.get('squad_adaptability', 0.5)
        dressing_room_harmony = team_data.get('dressing_room_harmony', 0.7)
        
        # Récupérer les facteurs de disruption
        disruption_factor = self.transition_types[transition_type]['disruption_factor']
        adaptation_period = self.transition_types[transition_type]['adaptation_period']
        
        # Calculer l'impact initial sur la dynamique
        initial_disruption = disruption_factor * (1 - squad_adaptability)
        
        # Calculer la vitesse d'adaptation
        adaptation_speed = 1 + ((squad_adaptability - 0.5) * 0.5) + ((team_experience - 0.5) * 0.3)
        adjusted_period = max(1, adaptation_period / adaptation_speed)
        
        # Prédire les changements dans des domaines spécifiques
        communication_change = new_analysis['impact_areas'].get('communication', 0.5) - previous_analysis['impact_areas'].get('communication', 0.5)
        motivation_change = new_analysis['impact_areas'].get('motivation', 0.5) - previous_analysis['impact_areas'].get('motivation', 0.5)
        organization_change = new_analysis['impact_areas'].get('tactical_organization', 0.5) - previous_analysis['impact_areas'].get('tactical_organization', 0.5)
        harmony_impact = 0.0
        
        # Impact sur l'harmonie du vestiaire
        if communication_change > 0.2 or motivation_change > 0.2:
            harmony_impact = 0.2
        elif communication_change < -0.2 or motivation_change < -0.2:
            harmony_impact = -0.2
        
        # Prédire la nouvelle harmonie du vestiaire
        new_harmony = max(0, min(1, dressing_room_harmony - initial_disruption + harmony_impact))
        
        # Prédire les changements généraux
        general_dynamic_change = (
            communication_change * 0.3 +
            motivation_change * 0.3 +
            organization_change * 0.2 +
            (new_harmony - dressing_room_harmony) * 0.2
        )
        
        # Classifier les changements
        dynamic_category = 'minimal_change'
        if general_dynamic_change > 0.15:
            dynamic_category = 'significant_improvement'
        elif general_dynamic_change > 0.05:
            dynamic_category = 'slight_improvement'
        elif general_dynamic_change < -0.15:
            dynamic_category = 'significant_disruption'
        elif general_dynamic_change < -0.05:
            dynamic_category = 'slight_disruption'
        
        return {
            'initial_disruption': initial_disruption,
            'adjusted_adaptation_period': round(adjusted_period, 1),
            'communication_change': communication_change,
            'motivation_change': motivation_change,
            'tactical_organization_change': organization_change,
            'harmony_impact': harmony_impact,
            'predicted_new_harmony': new_harmony,
            'general_dynamic_change': general_dynamic_change,
            'dynamic_category': dynamic_category
        }
    
    def _analyze_period_performance(self, matches):
        """Analyser les performances sur une période donnée."""
        if not matches:
            return None
        
        # Compter les résultats
        total_matches = len(matches)
        wins = sum(1 for match in matches if match.get('result', '') == 'W')
        draws = sum(1 for match in matches if match.get('result', '') == 'D')
        losses = sum(1 for match in matches if match.get('result', '') == 'L')
        
        # Calculer les statistiques offensives et défensives
        goals_scored = sum(match.get('goals_scored', 0) for match in matches)
        goals_conceded = sum(match.get('goals_conceded', 0) for match in matches)
        
        # Calculer les métriques
        win_percentage = wins / total_matches if total_matches > 0 else 0
        avg_points = (wins * 3 + draws) / total_matches if total_matches > 0 else 0
        avg_goals_scored = goals_scored / total_matches if total_matches > 0 else 0
        avg_goals_conceded = goals_conceded / total_matches if total_matches > 0 else 0
        
        return {
            'matches': total_matches,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'win_percentage': win_percentage,
            'avg_points': avg_points,
            'avg_goals_scored': avg_goals_scored,
            'avg_goals_conceded': avg_goals_conceded
        }
    
    def _extract_leadership_indicators(self, matches, captain_switch):
        """Extraire les indicateurs de leadership à partir des matchs."""
        # Identifiant du nouveau capitaine
        captain_id = captain_switch.get('new_captain', {}).get('id', '')
        
        if not captain_id:
            return None
        
        # Collecter les indicateurs
        matches_as_captain = 0
        yellow_cards = 0
        red_cards = 0
        goals = 0
        assists = 0
        minutes_played = 0
        influence_ratings = []
        
        for match in matches:
            # Vérifier si le capitaine a joué
            player_stats = match.get('player_stats', {}).get(captain_id, {})
            
            if player_stats:
                matches_as_captain += 1
                minutes_played += player_stats.get('minutes', 0)
                yellow_cards += player_stats.get('yellow_cards', 0)
                red_cards += player_stats.get('red_cards', 0)
                goals += player_stats.get('goals', 0)
                assists += player_stats.get('assists', 0)
                
                # Récupérer l'évaluation d'influence si disponible
                if 'leadership_rating' in player_stats:
                    influence_ratings.append(player_stats['leadership_rating'])
        
        # Calculer les moyennes
        avg_minutes = minutes_played / matches_as_captain if matches_as_captain > 0 else 0
        avg_influence = sum(influence_ratings) / len(influence_ratings) if influence_ratings else None
        
        # Préparation des résultats
        result = {
            'matches_as_captain': matches_as_captain,
            'avg_minutes': avg_minutes,
            'disciplinary': {
                'yellow_cards': yellow_cards,
                'red_cards': red_cards
            },
            'contribution': {
                'goals': goals,
                'assists': assists
            }
        }
        
        if avg_influence is not None:
            result['avg_leadership_rating'] = avg_influence
        
        return result
    
    def _evaluate_leadership_attributes(self, player_data):
        """Évaluer les attributs de leadership d'un joueur."""
        # Attributs bruts
        attributes = player_data.get('attributes', {})
        
        # Attributs spécifiques au leadership
        commanding = attributes.get('commanding', 0.5)
        vocal_leadership = attributes.get('vocal_leadership', 0.5)
        leading_by_example = attributes.get('leading_by_example', 0.5)
        tactical_awareness = attributes.get('tactical_awareness', 0.5)
        determination = attributes.get('determination', 0.5)
        pressure_handling = attributes.get('pressure_handling', 0.5)
        professionalism = attributes.get('professionalism', 0.5)
        
        # Facteurs contextuels
        team_tenure = player_data.get('team_tenure', 0.5)
        squad_respect = player_data.get('squad_respect', 0.5)
        
        # Calculer les attributs composites
        inspiring = (vocal_leadership * 0.4) + (leading_by_example * 0.4) + (determination * 0.2)
        organizing = (commanding * 0.4) + (tactical_awareness * 0.6)
        diplomatic = player_data.get('diplomatic', 0.5)  # Attribut direct s'il existe
        mentoring = (professionalism * 0.5) + (team_tenure * 0.3) + (squad_respect * 0.2)
        
        # Calculer le score global
        overall = (
            inspiring * 0.25 +
            organizing * 0.25 +
            diplomatic * 0.15 +
            mentoring * 0.15 +
            pressure_handling * 0.2
        )
        
        return {
            'overall': overall,
            'inspiring': inspiring,
            'organizing': organizing,
            'diplomatic': diplomatic,
            'mentoring': mentoring,
            'pressure_handling': pressure_handling
        }
    
    def _get_leadership_attribute_description(self, attribute, score):
        """Obtenir une description textuelle d'un attribut de leadership."""
        if attribute == 'inspiring':
            if score > 0.8:
                return "Capacité exceptionnelle à inspirer et motiver l'équipe"
            elif score > 0.6:
                return "Bonne capacité à inspirer ses coéquipiers"
            else:
                return "Difficulté à inspirer et motiver l'équipe"
        elif attribute == 'organizing':
            if score > 0.8:
                return "Excellence dans l'organisation et la direction sur le terrain"
            elif score > 0.6:
                return "Bonnes capacités d'organisation tactique"
            else:
                return "Manque de capacités d'organisation sur le terrain"
        elif attribute == 'diplomatic':
            if score > 0.8:
                return "Excellentes compétences de médiation et de gestion des conflits"
            elif score > 0.6:
                return "Bonnes compétences diplomatiques dans le vestiaire"
            else:
                return "Difficultés à gérer les tensions et résoudre les conflits"
        elif attribute == 'mentoring':
            if score > 0.8:
                return "Excellent mentor pour les jeunes joueurs"
            elif score > 0.6:
                return "Bonne capacité à guider les joueurs moins expérimentés"
            else:
                return "Peu enclin au mentorat des jeunes joueurs"
        elif attribute == 'pressure_handling':
            if score > 0.8:
                return "Excellente gestion de la pression dans les moments décisifs"
            elif score > 0.6:
                return "Bonne résistance à la pression"
            else:
                return "Difficulté à maintenir le calme sous pression"
        else:
            return f"Score de {attribute}: {score:.2f}"
    
    def _generate_captain_recommendations(self, candidate_data, leadership_attributes, team_fit, team_needs):
        """Générer des recommandations pour un candidat au capitanat."""
        recommendations = []
        
        # Évaluer les différents aspects
        strengths_count = sum(1 for attr, score in leadership_attributes.items() if attr != 'overall' and score > 0.7)
        weaknesses_count = sum(1 for attr, score in leadership_attributes.items() if attr != 'overall' and score < 0.4)
        
        # Recommandation sur la pertinence globale
        if leadership_attributes['overall'] > 0.7 and team_fit > 0.7:
            recommendations.append({
                'type': 'suitability',
                'recommendation': 'Excellent candidat pour le capitanat',
                'reasoning': 'Combinaison idéale de qualités de leadership et d\'adéquation avec les besoins de l\'équipe',
                'priority': 'high'
            })
        elif leadership_attributes['overall'] > 0.6 and team_fit > 0.6:
            recommendations.append({
                'type': 'suitability',
                'recommendation': 'Bon candidat pour le capitanat',
                'reasoning': 'Bonnes qualités de leadership et bonne adéquation avec les besoins de l\'équipe',
                'priority': 'medium'
            })
        elif leadership_attributes['overall'] < 0.5 or team_fit < 0.5:
            recommendations.append({
                'type': 'suitability',
                'recommendation': 'Candidat sous-optimal pour le capitanat',
                'reasoning': 'Certaines qualités de leadership ou l\'adéquation avec l\'équipe sont insuffisantes',
                'priority': 'high'
            })
        
        # Recommandation sur le développement
        if weaknesses_count > 0:
            weakest_attribute = min(
                [(attr, score) for attr, score in leadership_attributes.items() if attr != 'overall'],
                key=lambda x: x[1]
            )
            
            if weakest_attribute[0] == 'inspiring':
                recommendations.append({
                    'type': 'development',
                    'recommendation': 'Travailler la communication et l\'inspiration',
                    'reasoning': 'Améliorer la capacité à motiver et inspirer l\'équipe',
                    'priority': 'medium'
                })
            elif weakest_attribute[0] == 'organizing':
                recommendations.append({
                    'type': 'development',
                    'recommendation': 'Développer les compétences d\'organisation tactique',
                    'reasoning': 'Renforcer la capacité à organiser l\'équipe sur le terrain',
                    'priority': 'medium'
                })
            elif weakest_attribute[0] == 'diplomatic':
                recommendations.append({
                    'type': 'development',
                    'recommendation': 'Améliorer la gestion des conflits',
                    'reasoning': 'Développer les compétences diplomatiques pour gérer les tensions dans le vestiaire',
                    'priority': 'medium'
                })
        
        # Recommandation sur la préparation au rôle
        age = candidate_data.get('age', 28)
        experience = candidate_data.get('experience', 0.5)
        
        if age < 24 and experience < 0.6:
            recommendations.append({
                'type': 'preparation',
                'recommendation': 'Préparer progressivement au rôle de capitaine',
                'reasoning': 'Jeune joueur nécessitant une adaptation progressive aux responsabilités',
                'priority': 'high'
            })
            
            recommendations.append({
                'type': 'preparation',
                'recommendation': 'Nommer vice-capitaine avant le capitanat complet',
                'reasoning': 'Permettre d\'acquérir de l\'expérience dans un rôle de leadership secondaire',
                'priority': 'medium'
            })
        
        # Recommandation sur la transition
        club_tenure = candidate_data.get('team_tenure', 0.5)
        if club_tenure < 0.3:
            recommendations.append({
                'type': 'transition',
                'recommendation': 'Transition progressive vers le capitanat',
                'reasoning': 'Relativement nouveau dans l\'équipe, nécessite du temps pour établir son autorité',
                'priority': 'high'
            })
        
        # Recommandation sur le type de leadership
        leader_type, _ = self._determine_captain_type(candidate_data)
        highest_need = max(team_needs.items(), key=lambda x: x[1])
        
        if leader_type == 'vocal_leader' and highest_need[0] == 'tactical_organization':
            recommendations.append({
                'type': 'adaptation',
                'recommendation': 'Développer les compétences d\'organisation tactique',
                'reasoning': 'Leader vocal qui doit renforcer sa compréhension tactique pour répondre aux besoins de l\'équipe',
                'priority': 'medium'
            })
        
        return recommendations