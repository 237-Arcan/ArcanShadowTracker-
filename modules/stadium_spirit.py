"""
StadiumSpirit - Module d'analyse de l'énergie des stades, de leur aura et de leur mémoire historique.
Analyse l'influence des lieux sur les matchs et les performances des équipes.
"""

import random
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict
import math

class StadiumSpirit:
    """
    StadiumSpirit - Système d'analyse de l'énergie des stades et de leur influence historique.
    
    Ce module évalue l'aura énergétique des stades, leur influence sur les matchs,
    et leur mémoire vibratoire liée aux événements passés.
    """
    
    def __init__(self):
        """Initialise le module StadiumSpirit"""
        # Paramètres d'analyse
        self.analysis_params = {
            'historical_weight': 0.4,           # Poids de l'histoire du stade
            'atmospheric_weight': 0.3,          # Poids des conditions atmosphériques
            'crowd_energy_weight': 0.3,         # Poids de l'énergie de la foule
            'memory_decay_rate': 0.05,          # Taux de décroissance de la mémoire vibratoire
            'resonance_threshold': 0.7,         # Seuil pour les résonances significatives
            'energy_spike_threshold': 0.8,      # Seuil pour les pics d'énergie significatifs
            'minimum_historical_matches': 10,    # Nombre minimum de matchs pour l'analyse historique complète
            'aura_scaling_factor': 1.3          # Facteur d'échelle pour l'aura du stade
        }
        
        # Types d'auras de stade
        self.aura_types = {
            'fortress': {
                'description': "Forteresse - Avantage défensif très prononcé pour l'équipe hôte",
                'home_boost': 0.25,
                'visitor_penalty': -0.15
            },
            'cathedral': {
                'description': "Cathédrale - Stade historique avec forte charge émotionnelle",
                'home_boost': 0.2,
                'visitor_penalty': -0.1
            },
            'cauldron': {
                'description': "Chaudron - Ambiance intense et intimidante",
                'home_boost': 0.15,
                'visitor_penalty': -0.2
            },
            'theatre': {
                'description': "Théâtre - Lieu emblématique qui inspire les grands spectacles",
                'home_boost': 0.15,
                'visitor_penalty': -0.05
            },
            'coliseum': {
                'description': "Colisée - Arène qui pousse les deux équipes à se dépasser",
                'home_boost': 0.1,
                'visitor_penalty': 0.05
            },
            'neutral_ground': {
                'description': "Terrain neutre - Peu d'influence sur les équipes",
                'home_boost': 0.05,
                'visitor_penalty': 0.0
            },
            'cursed_ground': {
                'description': "Terrain maudit - Histoire de défaites pour l'équipe hôte",
                'home_boost': -0.1,
                'visitor_penalty': 0.1
            },
            'modern_arena': {
                'description': "Arène moderne - Confortable mais manquant d'âme",
                'home_boost': 0.1,
                'visitor_penalty': 0.0
            }
        }
        
        # Caractéristiques des stades pour l'analyse
        self.stadium_characteristics = [
            'capacity',                      # Capacité du stade
            'construction_year',             # Année de construction
            'roof_coverage',                 # Couverture du toit (0-1)
            'pitch_quality',                 # Qualité de la pelouse (0-1)
            'pitch_dimensions',              # Dimensions du terrain
            'altitude',                      # Altitude
            'historical_significance',       # Signification historique (0-1)
            'acoustic_properties',           # Propriétés acoustiques (0-1)
            'architectural_design',          # Design architectural (style)
            'renovations',                   # Historique des rénovations
            'spatial_configuration'          # Configuration spatiale (compact, ouvert, etc.)
        ]
        
        # Types d'événements historiques marquants
        self.significant_event_types = [
            'championship_victory',          # Victoire de championnat
            'relegation_match',              # Match de relégation
            'derby_outcome',                 # Résultat de derby
            'record_attendance',             # Record d'affluence
            'legendary_performance',         # Performance légendaire
            'tragic_incident',               # Incident tragique
            'memorable_comeback',            # Remontée mémorable
            'controversial_decision',        # Décision controversée
            'first_match',                   # Premier match
            'stadium_inauguration',          # Inauguration du stade
            'international_match',           # Match international
            'season_finale'                  # Finale de saison
        ]
        
        # Base de données des stades (serait normalement chargée depuis une source externe)
        self.stadium_database = {}
        
        # Historique des analyses
        self.analysis_history = []
    
    def analyze_stadium_influence(self, match_data, stadium_data=None, historical_data=None, atmospheric_conditions=None):
        """
        Analyser l'influence du stade sur un match.
        
        Args:
            match_data (dict): Données du match
            stadium_data (dict, optional): Données du stade
            historical_data (dict, optional): Données historiques du stade
            atmospheric_conditions (dict, optional): Conditions atmosphériques
            
        Returns:
            dict: Analyse complète de l'influence du stade
        """
        # Extraire les informations pertinentes
        home_team = match_data.get('home_team', 'Équipe domicile')
        away_team = match_data.get('away_team', 'Équipe extérieure')
        stadium_name = match_data.get('stadium', stadium_data.get('name', 'Stade inconnu') if stadium_data else 'Stade inconnu')
        match_date = match_data.get('date', datetime.now().isoformat())
        
        # Base de l'analyse
        influence_analysis = {
            'match': f"{home_team} vs {away_team}",
            'stadium': stadium_name,
            'match_date': match_date,
            'analysis_timestamp': datetime.now().isoformat(),
            'aura_type': None,                      # Type d'aura du stade
            'energy_level': 0.0,                    # Niveau d'énergie global
            'home_advantage_factor': 0.0,           # Facteur d'avantage pour l'équipe hôte
            'resonant_memories': [],                # Souvenirs qui résonnent avec ce match
            'current_atmospheric_influence': {},    # Influence des conditions atmosphériques
            'spiritual_prediction': {},             # Prédiction basée sur l'énergie spirituelle
            'key_energy_patterns': []               # Patterns énergétiques clés
        }
        
        # Obtenir ou simuler les données du stade
        stadium_data = stadium_data or self._get_stadium_data(stadium_name)
        
        # Obtenir ou simuler les données historiques
        historical_data = historical_data or self._get_historical_data(stadium_name, home_team)
        
        # Obtenir ou simuler les conditions atmosphériques
        atmospheric_conditions = atmospheric_conditions or self._get_atmospheric_conditions(match_data)
        
        # Analyser l'aura du stade
        aura_analysis = self._analyze_stadium_aura(
            stadium_data, historical_data, home_team, away_team
        )
        
        # Analyser la mémoire vibratoire du stade
        memory_analysis = self._analyze_vibrational_memory(
            stadium_data, historical_data, match_data
        )
        
        # Analyser l'influence atmosphérique
        atmospheric_analysis = self._analyze_atmospheric_influence(
            atmospheric_conditions, stadium_data
        )
        
        # Analyser l'énergie de la foule projetée
        crowd_analysis = self._project_crowd_energy(
            match_data, stadium_data, historical_data
        )
        
        # Combiner toutes les analyses
        influence_analysis['aura_type'] = aura_analysis.get('aura_type')
        influence_analysis['aura_description'] = aura_analysis.get('description')
        influence_analysis['aura_strength'] = aura_analysis.get('strength', 0.0)
        influence_analysis['home_advantage_factor'] = aura_analysis.get('home_advantage_factor', 0.1)
        
        influence_analysis['resonant_memories'] = memory_analysis.get('resonant_memories', [])
        influence_analysis['memory_potency'] = memory_analysis.get('overall_potency', 0.0)
        
        influence_analysis['current_atmospheric_influence'] = atmospheric_analysis
        
        influence_analysis['crowd_energy'] = crowd_analysis.get('energy_level', 0.0)
        influence_analysis['crowd_intensity'] = crowd_analysis.get('intensity', 0.0)
        influence_analysis['crowd_sentiment'] = crowd_analysis.get('primary_sentiment')
        
        # Calculer le niveau d'énergie global
        influence_analysis['energy_level'] = (
            aura_analysis.get('strength', 0.0) * self.analysis_params['historical_weight'] +
            atmospheric_analysis.get('overall_influence', 0.0) * self.analysis_params['atmospheric_weight'] +
            crowd_analysis.get('energy_level', 0.0) * self.analysis_params['crowd_energy_weight']
        )
        
        # Générer une prédiction spirituelle
        influence_analysis['spiritual_prediction'] = self._generate_spiritual_prediction(
            influence_analysis, home_team, away_team
        )
        
        # Identifier les patterns énergétiques clés
        influence_analysis['key_energy_patterns'] = self._identify_energy_patterns(
            aura_analysis, memory_analysis, atmospheric_analysis, crowd_analysis
        )
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'match': f"{home_team} vs {away_team}",
            'stadium': stadium_name,
            'date': match_date,
            'energy_level': influence_analysis['energy_level'],
            'aura_type': influence_analysis['aura_type']
        })
        
        return influence_analysis
    
    def evaluate_stadium_memory(self, stadium_name, team_name=None, event_type=None, timeframe=None):
        """
        Évaluer la mémoire vibratoire d'un stade.
        
        Args:
            stadium_name (str): Nom du stade
            team_name (str, optional): Filtrer par équipe
            event_type (str, optional): Filtrer par type d'événement
            timeframe (str, optional): Période d'analyse ('recent', 'all', 'historic')
            
        Returns:
            dict: Évaluation de la mémoire vibratoire
        """
        # Base de l'évaluation
        memory_evaluation = {
            'stadium': stadium_name,
            'team_filter': team_name,
            'event_type_filter': event_type,
            'timeframe': timeframe or 'all',
            'analysis_timestamp': datetime.now().isoformat(),
            'memory_strength': 0.0,
            'significant_memories': [],
            'memory_patterns': [],
            'emotional_residue': {},
            'current_memory_state': {}
        }
        
        # Obtenir les données du stade
        stadium_data = self._get_stadium_data(stadium_name)
        
        # Obtenir les données historiques
        historical_data = self._get_historical_data(stadium_name, team_name)
        
        # Filtrer les événements historiques
        filtered_events = historical_data.get('significant_events', [])
        
        if team_name:
            filtered_events = [e for e in filtered_events if e.get('team') == team_name or e.get('home_team') == team_name or e.get('away_team') == team_name]
        
        if event_type:
            filtered_events = [e for e in filtered_events if e.get('event_type') == event_type]
        
        if timeframe == 'recent':
            # Événements des 2 dernières années
            cutoff_date = (datetime.now() - timedelta(days=730)).isoformat()
            filtered_events = [e for e in filtered_events if e.get('date', '') >= cutoff_date]
        elif timeframe == 'historic':
            # Événements d'il y a plus de 10 ans
            cutoff_date = (datetime.now() - timedelta(days=3650)).isoformat()
            filtered_events = [e for e in filtered_events if e.get('date', '') <= cutoff_date]
        
        # Évaluer la force des souvenirs
        memory_strength = 0.0
        significant_memories = []
        
        for event in filtered_events:
            # Calculer la potence de la mémoire en fonction du temps écoulé et de l'importance
            event_date = datetime.fromisoformat(event.get('date', datetime.now().isoformat()))
            days_since = (datetime.now() - event_date).days
            
            # La puissance diminue avec le temps, sauf pour les événements très significatifs
            memory_decay = math.exp(-self.analysis_params['memory_decay_rate'] * (days_since / 365))
            
            event_significance = event.get('significance', 0.5)
            memory_potency = event_significance * (memory_decay + (1 - memory_decay) * event_significance * 0.5)
            
            if memory_potency > 0.4 or event_significance > 0.8:
                significant_memories.append({
                    'event_description': event.get('description', 'Événement significatif'),
                    'date': event.get('date'),
                    'event_type': event.get('event_type'),
                    'teams_involved': [event.get('home_team', ''), event.get('away_team', '')],
                    'significance': event_significance,
                    'memory_potency': memory_potency,
                    'emotional_charge': event.get('emotional_charge', 'neutral')
                })
            
            # Contribuer à la force globale de la mémoire
            memory_strength += memory_potency
        
        # Normaliser la force de la mémoire
        if filtered_events:
            memory_strength = min(1.0, memory_strength / math.sqrt(len(filtered_events)))
        
        memory_evaluation['memory_strength'] = memory_strength
        
        # Trier les souvenirs significatifs par potence
        significant_memories.sort(key=lambda x: x.get('memory_potency', 0), reverse=True)
        memory_evaluation['significant_memories'] = significant_memories[:5]  # Top 5
        
        # Analyser les patterns de mémoire
        memory_evaluation['memory_patterns'] = self._analyze_memory_patterns(filtered_events)
        
        # Évaluer le résidu émotionnel
        memory_evaluation['emotional_residue'] = self._evaluate_emotional_residue(filtered_events)
        
        # Déterminer l'état actuel de la mémoire
        memory_evaluation['current_memory_state'] = self._determine_memory_state(
            memory_strength, significant_memories, memory_evaluation['emotional_residue']
        )
        
        return memory_evaluation
    
    def analyze_stadium_harmonics(self, stadium_name, match_conditions=None):
        """
        Analyser les harmoniques vibratoires d'un stade.
        
        Args:
            stadium_name (str): Nom du stade
            match_conditions (dict, optional): Conditions du match à venir
            
        Returns:
            dict: Analyse des harmoniques du stade
        """
        # Base de l'analyse
        harmonic_analysis = {
            'stadium': stadium_name,
            'analysis_timestamp': datetime.now().isoformat(),
            'base_frequency': 0.0,
            'harmonic_patterns': [],
            'resonance_points': [],
            'energy_nodes': {},
            'harmonic_prediction': {}
        }
        
        # Obtenir les données du stade
        stadium_data = self._get_stadium_data(stadium_name)
        
        # Calcul de la fréquence de base (dépend des caractéristiques physiques du stade)
        base_frequency = self._calculate_stadium_base_frequency(stadium_data)
        harmonic_analysis['base_frequency'] = base_frequency
        
        # Identifier les patterns harmoniques
        harmonic_patterns = self._identify_harmonic_patterns(stadium_data)
        harmonic_analysis['harmonic_patterns'] = harmonic_patterns
        
        # Identifier les points de résonance
        resonance_points = self._identify_resonance_points(stadium_data, base_frequency)
        harmonic_analysis['resonance_points'] = resonance_points
        
        # Cartographier les nœuds d'énergie
        energy_nodes = self._map_energy_nodes(stadium_data, harmonic_patterns)
        harmonic_analysis['energy_nodes'] = energy_nodes
        
        # Générer une prédiction basée sur les harmoniques
        if match_conditions:
            harmonic_prediction = self._generate_harmonic_prediction(
                base_frequency, harmonic_patterns, resonance_points, match_conditions
            )
            harmonic_analysis['harmonic_prediction'] = harmonic_prediction
        
        return harmonic_analysis
    
    def compare_stadium_auras(self, stadium_list, reference_team=None):
        """
        Comparer les auras de plusieurs stades.
        
        Args:
            stadium_list (list): Liste des noms de stades à comparer
            reference_team (str, optional): Équipe de référence pour la comparaison
            
        Returns:
            dict: Analyse comparative des auras
        """
        # Base de l'analyse
        comparative_analysis = {
            'stadiums_compared': stadium_list,
            'reference_team': reference_team,
            'analysis_timestamp': datetime.now().isoformat(),
            'aura_comparison': [],
            'energy_ranking': [],
            'compatibility_matrix': {},
            'notable_differences': [],
            'team_specific_insights': {}
        }
        
        # Analyser chaque stade
        stadium_analyses = []
        
        for stadium_name in stadium_list:
            stadium_data = self._get_stadium_data(stadium_name)
            historical_data = self._get_historical_data(stadium_name, reference_team)
            
            # Analyser l'aura du stade
            aura_analysis = self._analyze_stadium_aura(
                stadium_data, historical_data, reference_team, None
            )
            
            stadium_analyses.append({
                'stadium': stadium_name,
                'aura_type': aura_analysis.get('aura_type'),
                'aura_strength': aura_analysis.get('strength', 0.0),
                'description': aura_analysis.get('description'),
                'home_advantage_factor': aura_analysis.get('home_advantage_factor', 0.0),
                'dominant_elements': aura_analysis.get('dominant_elements', [])
            })
        
        # Trier par force d'aura
        stadium_analyses.sort(key=lambda x: x.get('aura_strength', 0), reverse=True)
        
        # Préparer la comparaison des auras
        comparative_analysis['aura_comparison'] = stadium_analyses
        
        # Créer un classement par niveau d'énergie
        energy_ranking = [(s.get('stadium'), s.get('aura_strength')) for s in stadium_analyses]
        comparative_analysis['energy_ranking'] = energy_ranking
        
        # Créer une matrice de compatibilité
        compatibility_matrix = {}
        
        for i, stadium1 in enumerate(stadium_list):
            compatibility_matrix[stadium1] = {}
            
            for stadium2 in stadium_list:
                if stadium1 != stadium2:
                    compatibility = self._calculate_aura_compatibility(
                        next((s for s in stadium_analyses if s.get('stadium') == stadium1), {}),
                        next((s for s in stadium_analyses if s.get('stadium') == stadium2), {})
                    )
                    compatibility_matrix[stadium1][stadium2] = compatibility
        
        comparative_analysis['compatibility_matrix'] = compatibility_matrix
        
        # Identifier les différences notables
        if len(stadium_analyses) >= 2:
            for i in range(len(stadium_analyses) - 1):
                for j in range(i + 1, len(stadium_analyses)):
                    s1 = stadium_analyses[i]
                    s2 = stadium_analyses[j]
                    
                    # Comparer les types d'aura
                    if s1.get('aura_type') != s2.get('aura_type'):
                        comparative_analysis['notable_differences'].append({
                            'difference_type': 'aura_type',
                            'stadiums': [s1.get('stadium'), s2.get('stadium')],
                            'values': [s1.get('aura_type'), s2.get('aura_type')],
                            'description': f"Types d'aura différents: {s1.get('aura_type')} vs {s2.get('aura_type')}"
                        })
                    
                    # Comparer la force d'aura
                    aura_diff = abs(s1.get('aura_strength', 0) - s2.get('aura_strength', 0))
                    if aura_diff > 0.3:
                        comparative_analysis['notable_differences'].append({
                            'difference_type': 'aura_strength',
                            'stadiums': [s1.get('stadium'), s2.get('stadium')],
                            'values': [s1.get('aura_strength'), s2.get('aura_strength')],
                            'difference': aura_diff,
                            'description': f"Différence significative de force d'aura: {aura_diff:.2f}"
                        })
                    
                    # Comparer l'avantage à domicile
                    home_adv_diff = abs(s1.get('home_advantage_factor', 0) - s2.get('home_advantage_factor', 0))
                    if home_adv_diff > 0.15:
                        comparative_analysis['notable_differences'].append({
                            'difference_type': 'home_advantage',
                            'stadiums': [s1.get('stadium'), s2.get('stadium')],
                            'values': [s1.get('home_advantage_factor'), s2.get('home_advantage_factor')],
                            'difference': home_adv_diff,
                            'description': f"Différence significative d'avantage à domicile: {home_adv_diff:.2f}"
                        })
        
        # Insights spécifiques à l'équipe de référence
        if reference_team:
            team_insights = self._generate_team_specific_insights(stadium_analyses, reference_team)
            comparative_analysis['team_specific_insights'] = team_insights
        
        return comparative_analysis
    
    def _analyze_stadium_aura(self, stadium_data, historical_data, home_team, away_team):
        """Analyser l'aura du stade."""
        # Base de l'analyse
        aura_analysis = {
            'aura_type': 'neutral_ground',  # Type par défaut
            'strength': 0.5,                # Force par défaut
            'description': "Terrain à l'influence modérée",
            'dominant_elements': [],
            'home_advantage_factor': 0.1    # Facteur par défaut
        }
        
        # Extraire les caractéristiques du stade
        capacity = stadium_data.get('capacity', 30000)
        age = datetime.now().year - stadium_data.get('construction_year', 2000)
        historical_significance = stadium_data.get('historical_significance', 0.5)
        
        # Facteurs contribuant à l'aura
        aura_factors = {}
        
        # Âge et histoire
        if age > 75:
            aura_factors['age'] = min(1.0, age / 100)
        else:
            aura_factors['age'] = min(0.7, age / 100)
        
        # Capacité
        if capacity > 60000:
            aura_factors['capacity'] = 0.9
        elif capacity > 40000:
            aura_factors['capacity'] = 0.7
        elif capacity > 20000:
            aura_factors['capacity'] = 0.5
        else:
            aura_factors['capacity'] = 0.3
        
        # Architecture
        if 'iconic' in stadium_data.get('architectural_design', '').lower():
            aura_factors['architecture'] = 0.9
        elif 'traditional' in stadium_data.get('architectural_design', '').lower():
            aura_factors['architecture'] = 0.7
        elif 'modern' in stadium_data.get('architectural_design', '').lower():
            aura_factors['architecture'] = 0.5
        else:
            aura_factors['architecture'] = 0.4
        
        # Acoustique
        aura_factors['acoustics'] = stadium_data.get('acoustic_properties', 0.5)
        
        # Historique de performances de l'équipe à domicile
        home_win_rate = historical_data.get('home_win_rate', 0.5)
        
        if home_win_rate > 0.7:
            aura_factors['home_performance'] = 0.9
        elif home_win_rate > 0.6:
            aura_factors['home_performance'] = 0.7
        elif home_win_rate > 0.5:
            aura_factors['home_performance'] = 0.5
        else:
            aura_factors['home_performance'] = 0.3
        
        # Événements significatifs
        significant_events = historical_data.get('significant_events', [])
        event_factor = 0.0
        event_count = 0
        
        for event in significant_events:
            if event.get('significance', 0) > 0.7:
                event_factor += event.get('significance', 0)
                event_count += 1
        
        if event_count > 0:
            aura_factors['significant_events'] = min(1.0, event_factor / event_count)
        else:
            aura_factors['significant_events'] = 0.3
        
        # Calculer la force d'aura globale
        aura_strength = sum(aura_factors.values()) / len(aura_factors)
        aura_strength = min(1.0, aura_strength * self.analysis_params['aura_scaling_factor'])
        
        # Determiner le type d'aura
        dominant_elements = sorted(aura_factors.items(), key=lambda x: x[1], reverse=True)[:2]
        dominant_elements = [{'element': e[0], 'strength': e[1]} for e in dominant_elements]
        
        aura_type = self._determine_aura_type(aura_factors, home_win_rate)
        
        # Récupérer les caractéristiques de ce type d'aura
        aura_data = self.aura_types.get(aura_type, self.aura_types['neutral_ground'])
        
        # Déterminer le facteur d'avantage à domicile
        home_advantage = aura_data.get('home_boost', 0.1) * aura_strength
        
        aura_analysis['aura_type'] = aura_type
        aura_analysis['strength'] = aura_strength
        aura_analysis['description'] = aura_data.get('description', '')
        aura_analysis['dominant_elements'] = dominant_elements
        aura_analysis['home_advantage_factor'] = home_advantage
        
        return aura_analysis
    
    def _analyze_vibrational_memory(self, stadium_data, historical_data, match_data):
        """Analyser la mémoire vibratoire du stade."""
        # Base de l'analyse
        memory_analysis = {
            'overall_potency': 0.0,
            'resonant_memories': [],
            'memory_profile': {},
            'vibrational_patterns': []
        }
        
        # Extraire les événements significatifs
        significant_events = historical_data.get('significant_events', [])
        
        if not significant_events:
            memory_analysis['overall_potency'] = 0.2
            return memory_analysis
        
        # Extraire les données du match actuel
        match_date = match_data.get('date', datetime.now().isoformat())
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # Analyser chaque événement significatif
        resonance_values = []
        resonant_memories = []
        
        for event in significant_events:
            event_date = event.get('date', '')
            event_teams = [event.get('home_team', ''), event.get('away_team', '')]
            event_type = event.get('event_type', '')
            event_significance = event.get('significance', 0.5)
            
            # Calculer l'âge de la mémoire
            try:
                event_datetime = datetime.fromisoformat(event_date)
                current_datetime = datetime.fromisoformat(match_date) if match_date else datetime.now()
                years_since = (current_datetime - event_datetime).days / 365
            except:
                years_since = 10  # Valeur par défaut si la date est invalide
            
            # Calculer la décroissance de la mémoire
            memory_decay = math.exp(-self.analysis_params['memory_decay_rate'] * years_since)
            
            # Calculer le facteur de résonance
            resonance_factor = 0.0
            
            # Même(s) équipe(s)
            if home_team in event_teams and away_team in event_teams:
                resonance_factor += 0.4
            elif home_team in event_teams or away_team in event_teams:
                resonance_factor += 0.2
            
            # Même période de l'année
            try:
                event_month = datetime.fromisoformat(event_date).month
                current_month = datetime.fromisoformat(match_date).month if match_date else datetime.now().month
                
                if event_month == current_month:
                    resonance_factor += 0.15
                elif abs(event_month - current_month) <= 1 or abs(event_month - current_month) == 11:
                    resonance_factor += 0.05
            except:
                pass
            
            # Derby, finale, ou autre match spécial
            if event_type in ['derby_outcome', 'championship_victory', 'relegation_match']:
                resonance_factor += 0.25
            
            # Calculer la potence totale de cette mémoire
            memory_potency = event_significance * memory_decay * (1 + resonance_factor)
            
            resonance_values.append(memory_potency)
            
            # Si la mémoire est suffisamment forte, l'ajouter aux souvenirs résonants
            if memory_potency > self.analysis_params['resonance_threshold'] or (resonance_factor > 0.5 and memory_potency > 0.4):
                resonant_memories.append({
                    'description': event.get('description', 'Événement significatif'),
                    'date': event_date,
                    'teams': event_teams,
                    'event_type': event_type,
                    'significance': event_significance,
                    'resonance_factor': resonance_factor,
                    'memory_potency': memory_potency,
                    'similarity_factors': [],
                    'potential_influence': self._determine_memory_influence(event, memory_potency)
                })
        
        # Calculer la potence globale de la mémoire
        if resonance_values:
            memory_analysis['overall_potency'] = sum(resonance_values) / len(resonance_values)
        
        # Trier les souvenirs résonants par potence
        resonant_memories.sort(key=lambda x: x.get('memory_potency', 0), reverse=True)
        memory_analysis['resonant_memories'] = resonant_memories[:3]  # Top 3
        
        # Analyser le profil de mémoire
        memory_profile = self._analyze_memory_profile(significant_events, resonant_memories)
        memory_analysis['memory_profile'] = memory_profile
        
        # Identifier les patterns vibratoires
        vibrational_patterns = self._identify_vibrational_patterns(significant_events, resonant_memories)
        memory_analysis['vibrational_patterns'] = vibrational_patterns
        
        return memory_analysis
    
    def _analyze_atmospheric_influence(self, atmospheric_conditions, stadium_data):
        """Analyser l'influence des conditions atmosphériques."""
        # Base de l'analyse
        atmospheric_analysis = {
            'weather_influence': 0.0,
            'temporal_influence': 0.0,
            'cosmic_alignment': 0.0,
            'overall_influence': 0.0,
            'primary_condition': None,
            'influence_factors': []
        }
        
        # Extraire les conditions météo
        weather = atmospheric_conditions.get('weather', 'clear')
        temperature = atmospheric_conditions.get('temperature', 20)
        precipitation = atmospheric_conditions.get('precipitation', 0)
        wind = atmospheric_conditions.get('wind', 0)
        
        # Extraire les informations temporelles
        time_of_day = atmospheric_conditions.get('time_of_day', 'afternoon')
        season = atmospheric_conditions.get('season', 'summer')
        moon_phase = atmospheric_conditions.get('moon_phase', 'full')
        solar_activity = atmospheric_conditions.get('solar_activity', 'normal')
        
        # Caractéristiques du stade pertinentes
        has_roof = stadium_data.get('roof_coverage', 0) > 0.5
        stadium_orientation = stadium_data.get('orientation', 'north-south')
        altitude = stadium_data.get('altitude', 0)
        
        # Évaluer l'influence météorologique
        weather_influence = 0.0
        weather_factors = []
        
        # Pluie
        if precipitation > 10 and not has_roof:
            weather_influence += 0.2
            weather_factors.append({
                'factor': 'heavy_rain',
                'influence': 0.2,
                'description': "Forte pluie affectant les conditions de jeu"
            })
        elif precipitation > 0 and not has_roof:
            weather_influence += 0.1
            weather_factors.append({
                'factor': 'light_rain',
                'influence': 0.1,
                'description': "Légère pluie modifiant les conditions de jeu"
            })
        
        # Vent
        if wind > 30 and not has_roof:
            weather_influence += 0.25
            weather_factors.append({
                'factor': 'strong_wind',
                'influence': 0.25,
                'description': "Vent fort perturbant le jeu aérien"
            })
        elif wind > 15 and not has_roof:
            weather_influence += 0.15
            weather_factors.append({
                'factor': 'moderate_wind',
                'influence': 0.15,
                'description': "Vent modéré affectant certaines phases de jeu"
            })
        
        # Température
        if temperature > 30:
            weather_influence += 0.2
            weather_factors.append({
                'factor': 'heat',
                'influence': 0.2,
                'description': "Chaleur intense augmentant la fatigue"
            })
        elif temperature < 5:
            weather_influence += 0.15
            weather_factors.append({
                'factor': 'cold',
                'influence': 0.15,
                'description': "Froid affectant la mobilité et la concentration"
            })
        
        # Altitude
        if altitude > 1500:
            weather_influence += 0.3
            weather_factors.append({
                'factor': 'high_altitude',
                'influence': 0.3,
                'description': "Haute altitude affectant l'endurance et le ballon"
            })
        elif altitude > 500:
            weather_influence += 0.1
            weather_factors.append({
                'factor': 'moderate_altitude',
                'influence': 0.1,
                'description': "Altitude modérée affectant subtilement le jeu"
            })
        
        weather_influence = min(1.0, weather_influence)
        
        # Évaluer l'influence temporelle
        temporal_influence = 0.0
        temporal_factors = []
        
        # Heure du jour
        if time_of_day == 'night':
            temporal_influence += 0.15
            temporal_factors.append({
                'factor': 'night_match',
                'influence': 0.15,
                'description': "Match en nocturne, atmosphère plus intense"
            })
        elif time_of_day == 'twilight':
            temporal_influence += 0.1
            temporal_factors.append({
                'factor': 'twilight_match',
                'influence': 0.1,
                'description': "Match au crépuscule, conditions visuelles transitoires"
            })
        
        # Saison
        if season == 'winter' and not has_roof:
            temporal_influence += 0.1
            temporal_factors.append({
                'factor': 'winter_match',
                'influence': 0.1,
                'description': "Match hivernal, terrain potentiellement lourd"
            })
        elif season == 'autumn' and not has_roof:
            temporal_influence += 0.05
            temporal_factors.append({
                'factor': 'autumn_match',
                'influence': 0.05,
                'description': "Match automnal, possibles conditions variables"
            })
        
        temporal_influence = min(1.0, temporal_influence)
        
        # Évaluer l'alignement cosmique
        cosmic_influence = 0.0
        cosmic_factors = []
        
        # Phase lunaire
        if moon_phase == 'full':
            cosmic_influence += 0.1
            cosmic_factors.append({
                'factor': 'full_moon',
                'influence': 0.1,
                'description': "Pleine lune intensifiant l'énergie du stade"
            })
        elif moon_phase == 'new':
            cosmic_influence += 0.07
            cosmic_factors.append({
                'factor': 'new_moon',
                'influence': 0.07,
                'description': "Nouvelle lune favorisant les énergies subtiles"
            })
        
        # Activité solaire
        if solar_activity == 'high':
            cosmic_influence += 0.08
            cosmic_factors.append({
                'factor': 'high_solar_activity',
                'influence': 0.08,
                'description': "Forte activité solaire augmentant la charge énergétique"
            })
        
        cosmic_influence = min(1.0, cosmic_influence)
        
        # Déterminer la condition primaire
        influence_factors = weather_factors + temporal_factors + cosmic_factors
        influence_factors.sort(key=lambda x: x.get('influence', 0), reverse=True)
        
        primary_condition = influence_factors[0].get('factor') if influence_factors else None
        
        # Calculer l'influence globale
        overall_influence = 0.6 * weather_influence + 0.3 * temporal_influence + 0.1 * cosmic_influence
        
        atmospheric_analysis['weather_influence'] = weather_influence
        atmospheric_analysis['temporal_influence'] = temporal_influence
        atmospheric_analysis['cosmic_alignment'] = cosmic_influence
        atmospheric_analysis['overall_influence'] = overall_influence
        atmospheric_analysis['primary_condition'] = primary_condition
        atmospheric_analysis['influence_factors'] = influence_factors
        
        return atmospheric_analysis
    
    def _project_crowd_energy(self, match_data, stadium_data, historical_data):
        """Projeter l'énergie de la foule attendue."""
        # Base de l'analyse
        crowd_analysis = {
            'energy_level': 0.0,
            'intensity': 0.0,
            'primary_sentiment': 'neutral',
            'energy_patterns': [],
            'crowd_factors': []
        }
        
        # Extraire les informations pertinentes
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        expected_attendance = match_data.get('expected_attendance', stadium_data.get('capacity', 30000) * 0.7)
        capacity = stadium_data.get('capacity', 30000)
        
        # Calculer le taux de remplissage
        fill_rate = min(1.0, expected_attendance / capacity) if capacity > 0 else 0.7
        
        # Facteurs affectant l'énergie de la foule
        crowd_factors = []
        
        # Taux de remplissage
        if fill_rate > 0.9:
            crowd_factors.append({
                'factor': 'full_stadium',
                'energy_contribution': 0.3,
                'description': "Stade plein ou quasi-plein, atmosphère électrique"
            })
        elif fill_rate > 0.7:
            crowd_factors.append({
                'factor': 'good_attendance',
                'energy_contribution': 0.2,
                'description': "Bonne affluence générant une ambiance solide"
            })
        elif fill_rate > 0.5:
            crowd_factors.append({
                'factor': 'moderate_attendance',
                'energy_contribution': 0.1,
                'description': "Affluence modérée, ambiance correcte"
            })
        else:
            crowd_factors.append({
                'factor': 'low_attendance',
                'energy_contribution': 0.0,
                'description': "Faible affluence, atmosphère limitée"
            })
        
        # Importance du match
        match_importance = match_data.get('importance', 'regular')
        
        if match_importance == 'derby':
            crowd_factors.append({
                'factor': 'derby_match',
                'energy_contribution': 0.4,
                'description': "Derby local générant une intense rivalité"
            })
        elif match_importance == 'critical':
            crowd_factors.append({
                'factor': 'critical_match',
                'energy_contribution': 0.35,
                'description': "Match crucial pour le classement ou la qualification"
            })
        elif match_importance == 'high':
            crowd_factors.append({
                'factor': 'important_match',
                'energy_contribution': 0.25,
                'description': "Match important avec de forts enjeux"
            })
        elif match_importance == 'regular':
            crowd_factors.append({
                'factor': 'regular_match',
                'energy_contribution': 0.1,
                'description': "Match de championnat régulier"
            })
        
        # Rivalité historique
        historical_rivalry = historical_data.get('rivalry_level', {}).get(away_team, 0.0)
        
        if historical_rivalry > 0.7:
            crowd_factors.append({
                'factor': 'intense_rivalry',
                'energy_contribution': 0.3,
                'description': "Rivalité historique intense entre les équipes"
            })
        elif historical_rivalry > 0.4:
            crowd_factors.append({
                'factor': 'moderate_rivalry',
                'energy_contribution': 0.15,
                'description': "Rivalité modérée entre les équipes"
            })
        
        # Forme récente de l'équipe à domicile
        home_form = match_data.get('home_form', 'DDWLW')
        
        if home_form:
            recent_results = home_form[-3:]
            win_count = recent_results.count('W')
            loss_count = recent_results.count('L')
            
            if win_count >= 2:
                crowd_factors.append({
                    'factor': 'home_good_form',
                    'energy_contribution': 0.2,
                    'description': "Bonne forme récente de l'équipe à domicile"
                })
            elif loss_count >= 2:
                crowd_factors.append({
                    'factor': 'home_poor_form',
                    'energy_contribution': -0.1,
                    'description': "Mauvaise forme récente de l'équipe à domicile"
                })
        
        # Acoustique du stade
        acoustic_properties = stadium_data.get('acoustic_properties', 0.5)
        
        if acoustic_properties > 0.7:
            crowd_factors.append({
                'factor': 'excellent_acoustics',
                'energy_contribution': 0.2,
                'description': "Excellente acoustique amplifiant l'ambiance"
            })
        elif acoustic_properties > 0.5:
            crowd_factors.append({
                'factor': 'good_acoustics',
                'energy_contribution': 0.1,
                'description': "Bonne acoustique favorisant l'ambiance"
            })
        
        # Calculer l'énergie totale de la foule
        base_energy = 0.3  # Niveau de base
        energy_contributions = [factor.get('energy_contribution', 0) for factor in crowd_factors]
        energy_level = base_energy + sum(energy_contributions)
        energy_level = max(0.1, min(1.0, energy_level))
        
        # Déterminer l'intensité (volatilité de l'énergie)
        intensity = 0.5  # Niveau par défaut
        
        if 'derby_match' in [f.get('factor') for f in crowd_factors] or 'intense_rivalry' in [f.get('factor') for f in crowd_factors]:
            intensity += 0.3
        
        if 'full_stadium' in [f.get('factor') for f in crowd_factors]:
            intensity += 0.2
        
        intensity = min(1.0, intensity)
        
        # Déterminer le sentiment primaire
        primary_sentiment = 'neutral'
        
        if 'home_good_form' in [f.get('factor') for f in crowd_factors]:
            primary_sentiment = 'optimistic'
        elif 'home_poor_form' in [f.get('factor') for f in crowd_factors]:
            primary_sentiment = 'anxious'
        
        if 'derby_match' in [f.get('factor') for f in crowd_factors] or 'intense_rivalry' in [f.get('factor') for f in crowd_factors]:
            primary_sentiment = 'passionate'
        
        # Identifier des patterns d'énergie
        energy_patterns = self._identify_crowd_energy_patterns(crowd_factors, historical_data)
        
        crowd_analysis['energy_level'] = energy_level
        crowd_analysis['intensity'] = intensity
        crowd_analysis['primary_sentiment'] = primary_sentiment
        crowd_analysis['energy_patterns'] = energy_patterns
        crowd_analysis['crowd_factors'] = crowd_factors
        
        return crowd_analysis
    
    def _generate_spiritual_prediction(self, influence_analysis, home_team, away_team):
        """Générer une prédiction basée sur l'analyse spirituelle."""
        # Base de la prédiction
        prediction = {
            'energy_favors': None,
            'match_flow_pattern': None,
            'key_moments_timing': [],
            'spiritual_outcome': None,
            'confidence': 0.0,
            'spiritual_insights': []
        }
        
        # Extraire les facteurs d'influence clés
        aura_type = influence_analysis.get('aura_type')
        aura_strength = influence_analysis.get('aura_strength', 0.0)
        home_advantage = influence_analysis.get('home_advantage_factor', 0.0)
        energy_level = influence_analysis.get('energy_level', 0.0)
        memory_potency = influence_analysis.get('memory_potency', 0.0)
        resonant_memories = influence_analysis.get('resonant_memories', [])
        
        # Déterminer quelle équipe est favorisée par l'énergie
        energy_favor_home = home_advantage
        energy_favor_away = 0.0
        
        # Ajuster en fonction des souvenirs résonants
        for memory in resonant_memories:
            teams = memory.get('teams', [])
            influence = memory.get('potential_influence', {})
            
            if home_team in teams:
                energy_favor_home += influence.get('value', 0) * influence.get('direction', 0)
            
            if away_team in teams:
                energy_favor_away += influence.get('value', 0) * influence.get('direction', 0)
        
        # Déterminer l'équipe favorisée
        if energy_favor_home > energy_favor_away + 0.1:
            prediction['energy_favors'] = 'home'
        elif energy_favor_away > energy_favor_home + 0.1:
            prediction['energy_favors'] = 'away'
        else:
            prediction['energy_favors'] = 'neutral'
        
        # Déterminer le pattern de flow du match
        if aura_type in ['fortress', 'cathedral', 'cauldron']:
            prediction['match_flow_pattern'] = 'home_dominance'
        elif aura_type == 'cursed_ground':
            prediction['match_flow_pattern'] = 'away_dominance'
        elif aura_type == 'coliseum':
            prediction['match_flow_pattern'] = 'back_and_forth'
        elif energy_level > 0.7:
            prediction['match_flow_pattern'] = 'high_energy_chaos'
        elif memory_potency > 0.7:
            prediction['match_flow_pattern'] = 'historical_echo'
        else:
            prediction['match_flow_pattern'] = 'balanced_contest'
        
        # Prédire les moments clés
        if prediction['match_flow_pattern'] == 'home_dominance':
            prediction['key_moments_timing'] = ['15-25 minutes', '65-75 minutes']
        elif prediction['match_flow_pattern'] == 'away_dominance':
            prediction['key_moments_timing'] = ['30-40 minutes', '80-90 minutes']
        elif prediction['match_flow_pattern'] == 'back_and_forth':
            prediction['key_moments_timing'] = ['20-30 minutes', '55-65 minutes', '85-90 minutes']
        elif prediction['match_flow_pattern'] == 'high_energy_chaos':
            prediction['key_moments_timing'] = ['10-20 minutes', '40-50 minutes', '75-85 minutes']
        else:
            prediction['key_moments_timing'] = ['25-35 minutes', '70-80 minutes']
        
        # Prédire le résultat spirituel
        if prediction['energy_favors'] == 'home':
            if aura_strength > 0.7:
                prediction['spiritual_outcome'] = 'strong_home_victory'
            else:
                prediction['spiritual_outcome'] = 'narrow_home_victory'
        elif prediction['energy_favors'] == 'away':
            if aura_strength > 0.7:
                prediction['spiritual_outcome'] = 'surprising_away_victory'
            else:
                prediction['spiritual_outcome'] = 'battling_away_result'
        else:
            if energy_level > 0.7:
                prediction['spiritual_outcome'] = 'high_scoring_draw'
            else:
                prediction['spiritual_outcome'] = 'tactical_draw'
        
        # Déterminer la confiance
        confidence_factors = [
            aura_strength,
            memory_potency,
            abs(energy_favor_home - energy_favor_away) / 2
        ]
        
        prediction['confidence'] = sum(confidence_factors) / len(confidence_factors)
        
        # Générer des insights spirituels
        if aura_strength > 0.7:
            prediction['spiritual_insights'].append({
                'type': 'aura_insight',
                'description': f"L'aura puissante du stade ({aura_type}) sera un facteur déterminant"
            })
        
        if memory_potency > 0.6 and resonant_memories:
            prediction['spiritual_insights'].append({
                'type': 'memory_insight',
                'description': f"Écho vibratoire d'événements passés similaires, particulièrement {resonant_memories[0].get('description', '')}"
            })
        
        if energy_level > 0.7:
            prediction['spiritual_insights'].append({
                'type': 'energy_insight',
                'description': "Niveau d'énergie exceptionnellement élevé, favorisant des moments d'inspiration"
            })
        
        return prediction
    
    def _identify_energy_patterns(self, aura_analysis, memory_analysis, atmospheric_analysis, crowd_analysis):
        """Identifier les patterns énergétiques clés."""
        patterns = []
        
        # Pattern 1: Congruence énergétique
        energy_values = [
            aura_analysis.get('strength', 0.0),
            memory_analysis.get('overall_potency', 0.0),
            atmospheric_analysis.get('overall_influence', 0.0),
            crowd_analysis.get('energy_level', 0.0)
        ]
        
        max_energy = max(energy_values)
        min_energy = min(energy_values)
        energy_range = max_energy - min_energy
        
        if energy_range < 0.2 and np.mean(energy_values) > 0.6:
            patterns.append({
                'pattern_type': 'high_congruence',
                'strength': 0.8,
                'description': "Haute congruence énergétique - tous les facteurs alignés à un niveau élevé",
                'prediction': "Match d'intensité rare avec des moments mémorables"
            })
        elif energy_range < 0.2 and np.mean(energy_values) < 0.4:
            patterns.append({
                'pattern_type': 'low_congruence',
                'strength': 0.7,
                'description': "Congruence énergétique basse - tous les facteurs alignés à un niveau faible",
                'prediction': "Match potentiellement plat et peu inspiré"
            })
        
        # Pattern 2: Dominance d'un facteur
        dominant_idx = energy_values.index(max_energy)
        if max_energy > 0.7 and max_energy > np.mean(energy_values) + 0.25:
            dominant_source = ['aura', 'mémoire', 'atmosphère', 'foule'][dominant_idx]
            patterns.append({
                'pattern_type': 'dominant_factor',
                'factor': dominant_source,
                'strength': max_energy,
                'description': f"Dominance du facteur {dominant_source} sur l'énergie globale",
                'prediction': f"Le match sera fortement influencé par l'{dominant_source} du stade"
            })
        
        # Pattern 3: Résonance mémoire-aura
        if abs(aura_analysis.get('strength', 0.0) - memory_analysis.get('overall_potency', 0.0)) < 0.15:
            resonance_value = (aura_analysis.get('strength', 0.0) + memory_analysis.get('overall_potency', 0.0)) / 2
            if resonance_value > 0.6:
                patterns.append({
                    'pattern_type': 'memory_aura_resonance',
                    'strength': resonance_value,
                    'description': "Forte résonance entre mémoire vibratoire et aura du stade",
                    'prediction': "Les événements passés pourraient se reproduire sous une forme nouvelle"
                })
        
        # Pattern 4: Dissonance atmosphère-foule
        atmospheric_influence = atmospheric_analysis.get('overall_influence', 0.0)
        crowd_energy = crowd_analysis.get('energy_level', 0.0)
        
        if abs(atmospheric_influence - crowd_energy) > 0.3:
            patterns.append({
                'pattern_type': 'atmosphere_crowd_dissonance',
                'strength': abs(atmospheric_influence - crowd_energy),
                'description': "Dissonance entre conditions atmosphériques et énergie de foule attendue",
                'prediction': "Match potentiellement imprévisible avec retournements de situation"
            })
        
        # Trier les patterns par force
        patterns.sort(key=lambda x: x.get('strength', 0), reverse=True)
        
        return patterns
    
    def _get_stadium_data(self, stadium_name):
        """Obtenir les données d'un stade (ou simuler si non disponibles)."""
        # Vérifier si le stade est dans la base de données
        if stadium_name in self.stadium_database:
            return self.stadium_database[stadium_name]
        
        # Sinon, générer des données simulées
        current_year = datetime.now().year
        
        # Simuler différents types de stades
        stadium_types = [
            {
                'name': 'Modern Arena',
                'construction_year': random.randint(2000, current_year - 5),
                'capacity': random.randint(40000, 70000),
                'roof_coverage': random.uniform(0.5, 1.0),
                'pitch_quality': random.uniform(0.8, 1.0),
                'historical_significance': random.uniform(0.1, 0.4),
                'acoustic_properties': random.uniform(0.4, 0.8),
                'architectural_design': 'modern'
            },
            {
                'name': 'Historic Stadium',
                'construction_year': random.randint(1900, 1980),
                'capacity': random.randint(30000, 60000),
                'roof_coverage': random.uniform(0.0, 0.5),
                'pitch_quality': random.uniform(0.6, 0.9),
                'historical_significance': random.uniform(0.7, 1.0),
                'acoustic_properties': random.uniform(0.6, 0.9),
                'architectural_design': 'traditional'
            },
            {
                'name': 'Compact Ground',
                'construction_year': random.randint(1950, 1990),
                'capacity': random.randint(15000, 35000),
                'roof_coverage': random.uniform(0.3, 0.7),
                'pitch_quality': random.uniform(0.5, 0.8),
                'historical_significance': random.uniform(0.5, 0.8),
                'acoustic_properties': random.uniform(0.7, 1.0),
                'architectural_design': 'compact'
            },
            {
                'name': 'Iconic Venue',
                'construction_year': random.randint(1910, 1970),
                'capacity': random.randint(50000, 90000),
                'roof_coverage': random.uniform(0.2, 0.6),
                'pitch_quality': random.uniform(0.7, 1.0),
                'historical_significance': random.uniform(0.8, 1.0),
                'acoustic_properties': random.uniform(0.7, 0.9),
                'architectural_design': 'iconic'
            }
        ]
        
        # Choisir un type de stade et personnaliser pour le nom fourni
        stadium_type = random.choice(stadium_types)
        stadium_data = {
            'name': stadium_name,
            'construction_year': stadium_type['construction_year'],
            'capacity': stadium_type['capacity'],
            'roof_coverage': stadium_type['roof_coverage'],
            'pitch_quality': stadium_type['pitch_quality'],
            'pitch_dimensions': f"{random.randint(100, 110)}x{random.randint(65, 75)}",
            'altitude': random.randint(0, 500),
            'historical_significance': stadium_type['historical_significance'],
            'acoustic_properties': stadium_type['acoustic_properties'],
            'architectural_design': stadium_type['architectural_design'],
            'renovations': random.randint(0, 3),
            'spatial_configuration': random.choice(['compact', 'open', 'balanced']),
            'orientation': random.choice(['north-south', 'east-west', 'northeast-southwest'])
        }
        
        # Sauvegarder dans la base de données
        self.stadium_database[stadium_name] = stadium_data
        
        return stadium_data
    
    def _get_historical_data(self, stadium_name, team_name=None):
        """Obtenir les données historiques d'un stade (ou simuler si non disponibles)."""
        # Simuler des données historiques
        num_seasons = random.randint(5, 30)
        matches_per_season = random.randint(15, 25)
        total_matches = num_seasons * matches_per_season
        
        # Simuler le taux de victoires à domicile
        home_win_rate = random.uniform(0.45, 0.65)
        home_draw_rate = random.uniform(0.15, 0.25)
        home_loss_rate = 1 - home_win_rate - home_draw_rate
        
        # Générer des événements significatifs
        num_significant_events = random.randint(10, 20)
        significant_events = []
        
        # Liste des équipes potentielles
        teams = [
            "Arsenal", "Manchester United", "Liverpool", "Chelsea", "Manchester City",
            "Tottenham", "PSG", "Bayern Munich", "Barcelona", "Real Madrid",
            "Juventus", "Inter Milan", "AC Milan", "Ajax", "Dortmund"
        ]
        
        if team_name and team_name not in teams:
            teams.append(team_name)
        
        # Générer les événements
        for i in range(num_significant_events):
            event_year = datetime.now().year - random.randint(1, num_seasons * 2)
            event_month = random.randint(1, 12)
            event_day = random.randint(1, 28)
            event_date = datetime(event_year, event_month, event_day).isoformat()
            
            # Équipes impliquées
            home_team = team_name if team_name and random.random() < 0.7 else random.choice(teams)
            remaining_teams = [t for t in teams if t != home_team]
            away_team = random.choice(remaining_teams)
            
            # Type d'événement
            event_type = random.choice(self.significant_event_types)
            
            # Description de l'événement
            event_descriptions = {
                'championship_victory': f"Victoire du titre pour {home_team}",
                'relegation_match': f"Match de relégation crucial pour {home_team}",
                'derby_outcome': f"Derby historique {home_team} vs {away_team}",
                'record_attendance': f"Record d'affluence établi lors de {home_team} vs {away_team}",
                'legendary_performance': f"Performance légendaire d'un joueur de {random.choice([home_team, away_team])}",
                'tragic_incident': f"Incident mémorable lors d'un match",
                'memorable_comeback': f"{random.choice([home_team, away_team])} a réalisé une remontée spectaculaire de 3 buts",
                'controversial_decision': f"Décision arbitrale très controversée affectant {random.choice([home_team, away_team])}",
                'first_match': f"Premier match officiel joué dans ce stade",
                'stadium_inauguration': f"Inauguration officielle du stade",
                'international_match': f"Match international important",
                'season_finale': f"Finale de saison décisive pour {random.choice([home_team, away_team])}"
            }
            
            description = event_descriptions.get(event_type, "Événement significatif")
            
            # Significance et charge émotionnelle
            significance = random.uniform(0.6, 1.0)
            emotional_charges = ['positive', 'negative', 'mixed', 'euphoric', 'tragic', 'tense']
            emotional_charge = random.choice(emotional_charges)
            
            significant_events.append({
                'date': event_date,
                'event_type': event_type,
                'home_team': home_team,
                'away_team': away_team,
                'description': description,
                'significance': significance,
                'emotional_charge': emotional_charge,
                'historical_impact': random.uniform(0.5, 1.0)
            })
        
        # Trier par date
        significant_events.sort(key=lambda x: x.get('date', ''))
        
        # Générer des niveaux de rivalité
        rivalry_levels = {}
        for t in teams:
            if t != team_name:
                rivalry_levels[t] = random.uniform(0.1, 0.9)
        
        # Générer des données historiques agrégées
        historical_data = {
            'stadium': stadium_name,
            'total_matches': total_matches,
            'home_win_rate': home_win_rate,
            'home_draw_rate': home_draw_rate,
            'home_loss_rate': home_loss_rate,
            'significant_events': significant_events,
            'rivalry_level': rivalry_levels,
            'historical_performance': {
                'goals_scored_avg': random.uniform(1.3, 2.0),
                'goals_conceded_avg': random.uniform(0.8, 1.5),
                'clean_sheets_rate': random.uniform(0.25, 0.4)
            }
        }
        
        return historical_data
    
    def _get_atmospheric_conditions(self, match_data):
        """Obtenir les conditions atmosphériques (ou simuler si non disponibles)."""
        # Simuler des conditions atmosphériques
        weather_types = ['clear', 'partly_cloudy', 'cloudy', 'light_rain', 'heavy_rain', 'snow']
        time_of_day = ['morning', 'afternoon', 'evening', 'night']
        seasons = ['spring', 'summer', 'autumn', 'winter']
        moon_phases = ['new', 'waxing_crescent', 'first_quarter', 'waxing_gibbous', 
                     'full', 'waning_gibbous', 'last_quarter', 'waning_crescent']
        solar_activities = ['low', 'normal', 'high', 'storm']
        
        # Déterminer la saison en fonction de la date du match
        season = 'summer'  # par défaut
        if match_data.get('date'):
            try:
                match_month = datetime.fromisoformat(match_data.get('date')).month
                if 3 <= match_month <= 5:
                    season = 'spring'
                elif 6 <= match_month <= 8:
                    season = 'summer'
                elif 9 <= match_month <= 11:
                    season = 'autumn'
                else:
                    season = 'winter'
            except:
                pass
        
        # Générer des températures cohérentes avec la saison
        temperature_ranges = {
            'spring': (10, 20),
            'summer': (18, 30),
            'autumn': (8, 18),
            'winter': (-5, 10)
        }
        temp_range = temperature_ranges.get(season, (10, 25))
        temperature = random.uniform(temp_range[0], temp_range[1])
        
        # Générer des conditions météorologiques plus probables selon la saison
        if season == 'winter':
            weather = random.choices(weather_types, weights=[0.1, 0.2, 0.2, 0.2, 0.1, 0.2])[0]
        elif season == 'summer':
            weather = random.choices(weather_types, weights=[0.4, 0.3, 0.1, 0.1, 0.1, 0.0])[0]
        else:
            weather = random.choices(weather_types, weights=[0.2, 0.3, 0.2, 0.2, 0.1, 0.0])[0]
        
        # Générer des précipitations cohérentes avec la météo
        precipitation = 0
        if weather == 'light_rain':
            precipitation = random.uniform(1, 5)
        elif weather == 'heavy_rain':
            precipitation = random.uniform(5, 20)
        elif weather == 'snow':
            precipitation = random.uniform(1, 10)
        
        # Générer des conditions atmosphériques complètes
        atmospheric_conditions = {
            'weather': weather,
            'temperature': temperature,
            'precipitation': precipitation,
            'wind': random.uniform(0, 40),
            'time_of_day': random.choice(time_of_day),
            'season': season,
            'moon_phase': random.choice(moon_phases),
            'solar_activity': random.choices(solar_activities, weights=[0.4, 0.5, 0.09, 0.01])[0]
        }
        
        return atmospheric_conditions
    
    def _determine_aura_type(self, aura_factors, home_win_rate):
        """Déterminer le type d'aura du stade en fonction des facteurs."""
        # Facteurs clés pour chaque type d'aura
        if home_win_rate > 0.65 and aura_factors.get('home_performance', 0) > 0.8:
            return 'fortress'
        elif aura_factors.get('age', 0) > 0.7 and aura_factors.get('significant_events', 0) > 0.7:
            return 'cathedral'
        elif aura_factors.get('acoustics', 0) > 0.7 and aura_factors.get('capacity', 0) > 0.7:
            return 'cauldron'
        elif aura_factors.get('architecture', 0) > 0.8 and aura_factors.get('significant_events', 0) > 0.6:
            return 'theatre'
        elif aura_factors.get('architecture', 0) > 0.6 and home_win_rate > 0.55:
            return 'coliseum'
        elif home_win_rate < 0.4 and aura_factors.get('home_performance', 0) < 0.4:
            return 'cursed_ground'
        elif aura_factors.get('age', 0) < 0.3 and aura_factors.get('architecture', 0) > 0.6:
            return 'modern_arena'
        else:
            return 'neutral_ground'
    
    def _determine_memory_influence(self, event, memory_potency):
        """Déterminer l'influence potentielle d'un souvenir."""
        # Base de l'influence
        influence = {
            'value': memory_potency,
            'direction': 0.0,  # -1 à 1, négatif = contre l'équipe à domicile
            'description': ""
        }
        
        # Déterminer la direction de l'influence
        event_type = event.get('event_type', '')
        home_team = event.get('home_team', '')
        emotional_charge = event.get('emotional_charge', 'neutral')
        
        # Événements positifs pour l'équipe à domicile
        positive_events = [
            'championship_victory',
            'legendary_performance',
            'memorable_comeback'
        ]
        
        # Événements négatifs pour l'équipe à domicile
        negative_events = [
            'relegation_match',
            'tragic_incident'
        ]
        
        # Déterminer la direction
        if event_type in positive_events and emotional_charge in ['positive', 'euphoric']:
            influence['direction'] = 1.0
            influence['description'] = "Souvenir renforçant pour l'équipe à domicile"
        elif event_type in negative_events or emotional_charge in ['negative', 'tragic']:
            influence['direction'] = -1.0
            influence['description'] = "Souvenir inhibant pour l'équipe à domicile"
        else:
            # Influence neutre ou mixte
            influence['direction'] = random.uniform(-0.5, 0.5)
            influence['description'] = "Souvenir à l'influence variable"
        
        return influence
    
    def _analyze_memory_profile(self, significant_events, resonant_memories):
        """Analyser le profil de mémoire vibratoire d'un stade."""
        # Base du profil
        memory_profile = {
            'dominant_emotional_charge': 'neutral',
            'emotional_spectrum': {},
            'vibrational_coherence': 0.5,
            'memory_age_distribution': {}
        }
        
        if not significant_events:
            return memory_profile
        
        # Analyser le spectre émotionnel
        emotional_counts = defaultdict(int)
        for event in significant_events:
            emotional_charge = event.get('emotional_charge', 'neutral')
            emotional_counts[emotional_charge] += 1
        
        # Calculer les proportions
        total_events = len(significant_events)
        emotional_spectrum = {emotion: count / total_events for emotion, count in emotional_counts.items()}
        
        # Déterminer la charge émotionnelle dominante
        dominant_emotional = max(emotional_counts.items(), key=lambda x: x[1])[0]
        
        # Analyser la distribution par âge des souvenirs
        current_year = datetime.now().year
        age_distribution = {
            'recent': 0,      # 0-5 ans
            'mid_term': 0,    # 5-20 ans
            'historic': 0     # 20+ ans
        }
        
        for event in significant_events:
            try:
                event_year = datetime.fromisoformat(event.get('date', '')).year
                years_ago = current_year - event_year
                
                if years_ago <= 5:
                    age_distribution['recent'] += 1
                elif years_ago <= 20:
                    age_distribution['mid_term'] += 1
                else:
                    age_distribution['historic'] += 1
            except:
                age_distribution['mid_term'] += 1  # par défaut si date invalide
        
        # Normaliser la distribution
        for key in age_distribution:
            age_distribution[key] = age_distribution[key] / total_events
        
        # Évaluer la cohérence vibratoire
        if resonant_memories:
            resonant_emotions = [m.get('emotional_charge', 'neutral') for m in resonant_memories if 'emotional_charge' in m]
            most_common_emotion = max(set(resonant_emotions), key=resonant_emotions.count) if resonant_emotions else 'neutral'
            
            # Si une émotion est prédominante dans les souvenirs résonants, la cohérence est élevée
            if resonant_emotions.count(most_common_emotion) / len(resonant_emotions) > 0.6:
                vibrational_coherence = 0.8
            else:
                vibrational_coherence = 0.5
        else:
            vibrational_coherence = 0.5
        
        memory_profile['dominant_emotional_charge'] = dominant_emotional
        memory_profile['emotional_spectrum'] = emotional_spectrum
        memory_profile['vibrational_coherence'] = vibrational_coherence
        memory_profile['memory_age_distribution'] = age_distribution
        
        return memory_profile
    
    def _identify_vibrational_patterns(self, significant_events, resonant_memories):
        """Identifier des patterns vibratoires dans les souvenirs."""
        patterns = []
        
        if not significant_events:
            return patterns
        
        # Pattern 1: Cycles temporels
        # Vérifier s'il y a des cycles dans les dates des événements significatifs
        event_years = []
        event_months = []
        
        for event in significant_events:
            try:
                event_date = datetime.fromisoformat(event.get('date', ''))
                event_years.append(event_date.year)
                event_months.append(event_date.month)
            except:
                pass
        
        if event_years:
            # Chercher des cycles d'années
            year_diffs = [event_years[i+1] - event_years[i] for i in range(len(event_years)-1)]
            if year_diffs and max(year_diffs) == min(year_diffs) and len(year_diffs) >= 2:
                patterns.append({
                    'pattern_type': 'temporal_cycle',
                    'cycle_length': year_diffs[0],
                    'description': f"Cycle temporel de {year_diffs[0]} ans dans les événements significatifs"
                })
        
        # Pattern 2: Congruence émotionnelle
        if resonant_memories and len(resonant_memories) >= 2:
            emotional_charges = [m.get('emotional_charge', 'neutral') for m in resonant_memories if 'emotional_charge' in m]
            unique_emotions = set(emotional_charges)
            
            if len(unique_emotions) == 1:
                patterns.append({
                    'pattern_type': 'emotional_congruence',
                    'emotion': list(unique_emotions)[0],
                    'description': f"Congruence émotionnelle parfaite: tous les souvenirs résonants portent la charge '{list(unique_emotions)[0]}'"
                })
        
        # Pattern 3: Progression d'intensité
        if resonant_memories and len(resonant_memories) >= 3:
            potencies = [m.get('memory_potency', 0) for m in resonant_memories]
            
            # Vérifier si les potences sont en ordre croissant
            if all(potencies[i] <= potencies[i+1] for i in range(len(potencies)-1)):
                patterns.append({
                    'pattern_type': 'intensity_progression',
                    'description': "Progression d'intensité: les souvenirs plus récents ont une potence vibratoire croissante"
                })
        
        # Pattern 4: Résonance type d'événement
        if resonant_memories and len(resonant_memories) >= 2:
            event_types = [m.get('event_type', '') for m in resonant_memories]
            most_common_type = max(set(event_types), key=event_types.count)
            
            if event_types.count(most_common_type) >= len(event_types) * 0.5:
                patterns.append({
                    'pattern_type': 'event_type_resonance',
                    'event_type': most_common_type,
                    'description': f"Résonance de type d'événement: prédominance des événements de type '{most_common_type}'"
                })
        
        return patterns
    
    def _identify_crowd_energy_patterns(self, crowd_factors, historical_data):
        """Identifier des patterns dans l'énergie de la foule."""
        patterns = []
        
        # Extraire les facteurs positifs et négatifs
        positive_factors = [f for f in crowd_factors if f.get('energy_contribution', 0) > 0]
        negative_factors = [f for f in crowd_factors if f.get('energy_contribution', 0) < 0]
        
        # Pattern 1: Dominance de facteurs positifs
        if len(positive_factors) >= 3 and len(negative_factors) <= 1:
            patterns.append({
                'pattern_type': 'positive_dominance',
                'strength': min(1.0, len(positive_factors) * 0.15),
                'description': "Dominance de facteurs positifs dans l'énergie de la foule"
            })
        
        # Pattern 2: Amplification mutuelle
        if any(f.get('factor') == 'full_stadium' for f in crowd_factors) and any(f.get('factor') in ['derby_match', 'intense_rivalry'] for f in crowd_factors):
            patterns.append({
                'pattern_type': 'mutual_amplification',
                'strength': 0.8,
                'description': "Amplification mutuelle entre affluence maximale et haute intensité du match"
            })
        
        # Pattern 3: Facteur dominant
        if crowd_factors:
            max_contribution = max([abs(f.get('energy_contribution', 0)) for f in crowd_factors])
            dominant_factors = [f for f in crowd_factors if abs(f.get('energy_contribution', 0)) == max_contribution]
            
            if dominant_factors and max_contribution > 0.3:
                patterns.append({
                    'pattern_type': 'dominant_factor',
                    'factor': dominant_factors[0].get('factor', ''),
                    'strength': max_contribution,
                    'description': f"Facteur dominant: {dominant_factors[0].get('description', '')}"
                })
        
        # Pattern 4: Résonance historique
        significant_events = historical_data.get('significant_events', [])
        recent_events = []
        
        for event in significant_events:
            try:
                event_date = datetime.fromisoformat(event.get('date', ''))
                years_ago = (datetime.now() - event_date).days / 365
                if years_ago <= 1 and event.get('significance', 0) > 0.7:
                    recent_events.append(event)
            except:
                pass
        
        if recent_events:
            patterns.append({
                'pattern_type': 'recent_historical_resonance',
                'strength': 0.7,
                'events': [e.get('description', '') for e in recent_events],
                'description': "Résonance avec des événements historiques récents et significatifs"
            })
        
        return patterns
    
    def _calculate_stadium_base_frequency(self, stadium_data):
        """Calculer la fréquence vibratoire de base d'un stade."""
        # Facteurs contribuant à la fréquence de base
        capacity = stadium_data.get('capacity', 30000)
        age = datetime.now().year - stadium_data.get('construction_year', 2000)
        acoustics = stadium_data.get('acoustic_properties', 0.5)
        
        # Algorithme simple pour calculer une fréquence
        base_value = (capacity / 100000) * 0.3 + (min(age, 100) / 100) * 0.4 + acoustics * 0.3
        
        # Normaliser entre 0.3 et 0.9
        base_frequency = 0.3 + base_value * 0.6
        
        return base_frequency
    
    def _identify_harmonic_patterns(self, stadium_data):
        """Identifier les patterns harmoniques d'un stade."""
        patterns = []
        
        # Facteurs contribuant aux harmoniques
        design = stadium_data.get('architectural_design', '')
        spatial_config = stadium_data.get('spatial_configuration', '')
        
        # Pattern 1: Résonance architecturale
        if design == 'compact' and spatial_config == 'compact':
            patterns.append({
                'pattern_type': 'amplification_chamber',
                'frequency_modifier': 1.3,
                'description': "Configuration de type chambre d'amplification"
            })
        elif design == 'open' and spatial_config == 'open':
            patterns.append({
                'pattern_type': 'dispersive_field',
                'frequency_modifier': 0.8,
                'description': "Configuration de type champ dispersif"
            })
        
        # Pattern 2: Nœuds acoustiques
        if stadium_data.get('acoustic_properties', 0) > 0.7:
            patterns.append({
                'pattern_type': 'acoustic_nodes',
                'frequency_modifier': 1.2,
                'description': "Présence de nœuds acoustiques naturels"
            })
        
        # Pattern 3: Résonance de forme
        pitch_dimensions = stadium_data.get('pitch_dimensions', '105x68')
        try:
            length, width = map(int, pitch_dimensions.split('x'))
            aspect_ratio = length / width
            
            if 1.5 <= aspect_ratio <= 1.6:
                patterns.append({
                    'pattern_type': 'golden_ratio',
                    'frequency_modifier': 1.5,
                    'description': "Dimensions du terrain proches du nombre d'or"
                })
        except:
            pass
        
        # Ajouter un pattern par défaut si aucun pattern spécifique n'est identifié
        if not patterns:
            patterns.append({
                'pattern_type': 'standard_harmonic',
                'frequency_modifier': 1.0,
                'description': "Harmoniques stadières standard"
            })
        
        return patterns
    
    def _identify_resonance_points(self, stadium_data, base_frequency):
        """Identifier les points de résonance d'un stade."""
        resonance_points = []
        
        # Simuler quelques points de résonance
        num_points = random.randint(2, 5)
        
        for i in range(num_points):
            resonance_value = base_frequency * (1 + random.uniform(-0.2, 0.3))
            location = random.choice(['north_stand', 'south_stand', 'east_stand', 'west_stand', 'center_circle', 'penalty_area'])
            condition = random.choice(['always', 'when_full', 'under_pressure', 'during_chants'])
            
            resonance_points.append({
                'frequency': resonance_value,
                'location': location,
                'activation_condition': condition,
                'intensity': random.uniform(0.5, 0.9)
            })
        
        return resonance_points
    
    def _map_energy_nodes(self, stadium_data, harmonic_patterns):
        """Cartographier les nœuds d'énergie dans un stade."""
        # Simuler une carte des nœuds d'énergie
        energy_nodes = {
            'primary_nodes': [],
            'secondary_nodes': [],
            'energy_flows': []
        }
        
        # Générer des nœuds primaires
        num_primary = random.randint(1, 3)
        for i in range(num_primary):
            energy_nodes['primary_nodes'].append({
                'location': random.choice(['north_stand', 'south_stand', 'east_stand', 'west_stand', 'center_circle']),
                'energy_type': random.choice(['amplifying', 'stabilizing', 'transformative']),
                'intensity': random.uniform(0.7, 1.0)
            })
        
        # Générer des nœuds secondaires
        num_secondary = random.randint(2, 5)
        for i in range(num_secondary):
            energy_nodes['secondary_nodes'].append({
                'location': random.choice(['corner_flag', 'tunnel', 'technical_area', 'goal_area', 'halfway_line']),
                'energy_type': random.choice(['reflective', 'absorptive', 'neutral']),
                'intensity': random.uniform(0.3, 0.7)
            })
        
        # Générer des flux d'énergie
        if energy_nodes['primary_nodes'] and energy_nodes['secondary_nodes']:
            num_flows = min(len(energy_nodes['primary_nodes']) + len(energy_nodes['secondary_nodes']) - 1, 5)
            
            all_nodes = energy_nodes['primary_nodes'] + energy_nodes['secondary_nodes']
            
            for i in range(num_flows):
                source_idx = random.randint(0, len(all_nodes) - 1)
                target_idx = random.randint(0, len(all_nodes) - 1)
                
                # Éviter les flux vers le même nœud
                while target_idx == source_idx:
                    target_idx = random.randint(0, len(all_nodes) - 1)
                
                energy_nodes['energy_flows'].append({
                    'source': all_nodes[source_idx]['location'],
                    'target': all_nodes[target_idx]['location'],
                    'strength': random.uniform(0.4, 0.9),
                    'flow_type': random.choice(['continuous', 'pulsating', 'conditional'])
                })
        
        return energy_nodes
    
    def _generate_harmonic_prediction(self, base_frequency, harmonic_patterns, resonance_points, match_conditions):
        """Générer une prédiction basée sur les harmoniques du stade."""
        # Base de la prédiction
        prediction = {
            'harmonic_state': '',
            'resonance_likelihood': 0.0,
            'potential_peak_moments': [],
            'key_insight': ''
        }
        
        # Calculer la fréquence modifiée
        modified_frequency = base_frequency
        for pattern in harmonic_patterns:
            modified_frequency *= pattern.get('frequency_modifier', 1.0)
        
        # Déterminer l'état harmonique
        if modified_frequency > 1.0:
            harmonic_state = 'heightened'
        elif modified_frequency < 0.5:
            harmonic_state = 'dampened'
        else:
            harmonic_state = 'balanced'
        
        prediction['harmonic_state'] = harmonic_state
        
        # Déterminer la probabilité de résonance
        crowd_energy = match_conditions.get('crowd_energy', 0.5)
        match_intensity = match_conditions.get('match_intensity', 0.5)
        
        resonance_likelihood = (modified_frequency * 0.3 + crowd_energy * 0.4 + match_intensity * 0.3)
        prediction['resonance_likelihood'] = min(1.0, resonance_likelihood)
        
        # Générer des moments potentiels de pic
        if prediction['resonance_likelihood'] > 0.6:
            num_peaks = random.randint(1, 3)
            for i in range(num_peaks):
                prediction['potential_peak_moments'].append({
                    'timing': f"{random.randint(1, 9)}0-{random.randint(1, 9)}5 minutes",
                    'type': random.choice(['crowd_surge', 'player_inspiration', 'momentum_shift']),
                    'intensity': random.uniform(0.7, 0.9)
                })
        
        # Générer un insight clé
        if harmonic_state == 'heightened':
            prediction['key_insight'] = "Les vibrations amplifiées du stade pourraient catalyser des moments d'inspiration collective"
        elif harmonic_state == 'dampened':
            prediction['key_insight'] = "Les harmoniques atténuées suggèrent un match plus technique que passionnel"
        else:
            prediction['key_insight'] = "L'équilibre harmonique favorise un flow naturel du jeu avec des moments clés répartis"
        
        return prediction
    
    def _calculate_aura_compatibility(self, stadium1_data, stadium2_data):
        """Calculer la compatibilité entre deux auras de stade."""
        # Extraire les types d'aura
        aura_type1 = stadium1_data.get('aura_type', 'neutral_ground')
        aura_type2 = stadium2_data.get('aura_type', 'neutral_ground')
        
        # Matrice de compatibilité des auras (valeurs de 0 à 1)
        compatibility_matrix = {
            'fortress': {
                'fortress': 0.4,
                'cathedral': 0.7,
                'cauldron': 0.5,
                'theatre': 0.6,
                'coliseum': 0.3,
                'neutral_ground': 0.5,
                'cursed_ground': 0.2,
                'modern_arena': 0.4
            },
            'cathedral': {
                'fortress': 0.7,
                'cathedral': 0.9,
                'cauldron': 0.6,
                'theatre': 0.8,
                'coliseum': 0.5,
                'neutral_ground': 0.6,
                'cursed_ground': 0.3,
                'modern_arena': 0.5
            },
            'cauldron': {
                'fortress': 0.5,
                'cathedral': 0.6,
                'cauldron': 0.4,
                'theatre': 0.5,
                'coliseum': 0.7,
                'neutral_ground': 0.5,
                'cursed_ground': 0.3,
                'modern_arena': 0.6
            },
            'theatre': {
                'fortress': 0.6,
                'cathedral': 0.8,
                'cauldron': 0.5,
                'theatre': 0.8,
                'coliseum': 0.7,
                'neutral_ground': 0.6,
                'cursed_ground': 0.4,
                'modern_arena': 0.7
            },
            'coliseum': {
                'fortress': 0.3,
                'cathedral': 0.5,
                'cauldron': 0.7,
                'theatre': 0.7,
                'coliseum': 0.6,
                'neutral_ground': 0.5,
                'cursed_ground': 0.4,
                'modern_arena': 0.5
            },
            'neutral_ground': {
                'fortress': 0.5,
                'cathedral': 0.6,
                'cauldron': 0.5,
                'theatre': 0.6,
                'coliseum': 0.5,
                'neutral_ground': 0.7,
                'cursed_ground': 0.6,
                'modern_arena': 0.7
            },
            'cursed_ground': {
                'fortress': 0.2,
                'cathedral': 0.3,
                'cauldron': 0.3,
                'theatre': 0.4,
                'coliseum': 0.4,
                'neutral_ground': 0.6,
                'cursed_ground': 0.5,
                'modern_arena': 0.4
            },
            'modern_arena': {
                'fortress': 0.4,
                'cathedral': 0.5,
                'cauldron': 0.6,
                'theatre': 0.7,
                'coliseum': 0.5,
                'neutral_ground': 0.7,
                'cursed_ground': 0.4,
                'modern_arena': 0.8
            }
        }
        
        # Récupérer la compatibilité de base
        base_compatibility = compatibility_matrix.get(aura_type1, {}).get(aura_type2, 0.5)
        
        # Ajuster en fonction des forces d'aura
        aura_strength1 = stadium1_data.get('aura_strength', 0.5)
        aura_strength2 = stadium2_data.get('aura_strength', 0.5)
        
        strength_factor = (aura_strength1 + aura_strength2) / 2
        
        # Une compatibilité élevée est amplifiée par des auras fortes
        # Une compatibilité faible est atténuée par des auras faibles
        if base_compatibility > 0.5:
            adjusted_compatibility = base_compatibility * (0.8 + 0.4 * strength_factor)
        else:
            adjusted_compatibility = base_compatibility * (1.0 + 0.2 * strength_factor)
        
        # Limiter entre 0.1 et 1.0
        return max(0.1, min(1.0, adjusted_compatibility))
    
    def _generate_team_specific_insights(self, stadium_analyses, reference_team):
        """Générer des insights spécifiques à une équipe concernant les stades."""
        insights = {
            'most_compatible_stadium': None,
            'least_compatible_stadium': None,
            'aura_affinities': {},
            'recommendations': []
        }
        
        if not stadium_analyses:
            return insights
        
        # Évaluer la compatibilité de chaque stade avec l'équipe
        compatibilities = []
        
        for stadium_data in stadium_analyses:
            stadium_name = stadium_data.get('stadium', '')
            aura_type = stadium_data.get('aura_type', '')
            home_advantage = stadium_data.get('home_advantage_factor', 0.0)
            
            # Simuler une affinité d'équipe pour ce type d'aura
            aura_affinity = random.uniform(0.3, 0.9)
            
            # Calculer la compatibilité globale
            compatibility = aura_affinity * home_advantage
            
            compatibilities.append({
                'stadium': stadium_name,
                'compatibility': compatibility,
                'aura_type': aura_type,
                'aura_affinity': aura_affinity
            })
        
        # Trier par compatibilité
        compatibilities.sort(key=lambda x: x.get('compatibility', 0), reverse=True)
        
        # Identifier les stades les plus et moins compatibles
        if compatibilities:
            insights['most_compatible_stadium'] = {
                'stadium': compatibilities[0].get('stadium', ''),
                'compatibility': compatibilities[0].get('compatibility', 0),
                'reason': f"Forte affinité avec l'aura de type {compatibilities[0].get('aura_type', '')}"
            }
            
            insights['least_compatible_stadium'] = {
                'stadium': compatibilities[-1].get('stadium', ''),
                'compatibility': compatibilities[-1].get('compatibility', 0),
                'reason': f"Faible affinité avec l'aura de type {compatibilities[-1].get('aura_type', '')}"
            }
        
        # Déterminer les affinités avec différents types d'aura
        aura_affinities = {}
        
        for compatibility in compatibilities:
            aura_type = compatibility.get('aura_type', '')
            affinity = compatibility.get('aura_affinity', 0)
            
            if aura_type not in aura_affinities:
                aura_affinities[aura_type] = affinity
        
        insights['aura_affinities'] = aura_affinities
        
        # Générer des recommandations
        if compatibilities:
            # Recommandation basée sur le stade le plus compatible
            insights['recommendations'].append({
                'recommendation_type': 'stadium_preference',
                'description': f"Privilégier les matchs au {insights['most_compatible_stadium']['stadium']} qui offre une forte résonance avec l'identité de l'équipe"
            })
            
            # Recommandation basée sur le type d'aura préféré
            preferred_aura = max(aura_affinities.items(), key=lambda x: x[1])[0]
            insights['recommendations'].append({
                'recommendation_type': 'aura_affinity',
                'description': f"Chercher des stades avec une aura de type '{preferred_aura}' qui amplifie les forces de l'équipe"
            })
            
            # Recommandation pour le stade le moins compatible
            insights['recommendations'].append({
                'recommendation_type': 'stadium_caution',
                'description': f"Adopter une approche tactique différente au {insights['least_compatible_stadium']['stadium']} pour contrebalancer l'incompatibilité énergétique"
            })
        
        return insights
    
    def _determine_memory_state(self, memory_strength, significant_memories, emotional_residue):
        """Déterminer l'état actuel de la mémoire vibratoire d'un stade."""
        # Base de l'état
        memory_state = {
            'current_state': 'dormant',
            'dominant_memory': None,
            'activation_potential': 0.0,
            'stability_factor': 0.5
        }
        
        # Déterminer l'état en fonction de la force de la mémoire
        if memory_strength > 0.7:
            memory_state['current_state'] = 'highly_active'
        elif memory_strength > 0.5:
            memory_state['current_state'] = 'active'
        elif memory_strength > 0.3:
            memory_state['current_state'] = 'semi_active'
        else:
            memory_state['current_state'] = 'dormant'
        
        # Identifier la mémoire dominante
        if significant_memories:
            memory_state['dominant_memory'] = significant_memories[0]
        
        # Calculer le potentiel d'activation
        dominant_emotion = emotional_residue.get('dominant_emotional_charge', 'neutral')
        emotion_strength = 0.5
        
        if dominant_emotion in ['positive', 'euphoric']:
            emotion_strength = 0.7
        elif dominant_emotion in ['negative', 'tragic']:
            emotion_strength = 0.6
        
        memory_state['activation_potential'] = memory_strength * emotion_strength
        
        # Déterminer le facteur de stabilité
        if 'vibrational_coherence' in emotional_residue:
            memory_state['stability_factor'] = emotional_residue['vibrational_coherence']
        else:
            # Estimer la stabilité en fonction de la distribution émotionnelle
            if len(emotional_residue.get('emotional_spectrum', {})) <= 2:
                memory_state['stability_factor'] = 0.8  # Peu d'émotions = plus stable
            else:
                memory_state['stability_factor'] = 0.4  # Beaucoup d'émotions = moins stable
        
        return memory_state
    
    def _evaluate_emotional_residue(self, events):
        """Évaluer le résidu émotionnel laissé par les événements passés."""
        # Base de l'évaluation
        emotional_residue = {
            'dominant_emotional_charge': 'neutral',
            'emotional_intensity': 0.5,
            'emotional_spectrum': {},
            'vibrational_coherence': 0.5
        }
        
        if not events:
            return emotional_residue
        
        # Compter les différentes charges émotionnelles
        emotion_counts = defaultdict(int)
        emotion_intensities = defaultdict(float)
        
        for event in events:
            emotion = event.get('emotional_charge', 'neutral')
            significance = event.get('significance', 0.5)
            
            emotion_counts[emotion] += 1
            emotion_intensities[emotion] += significance
        
        # Déterminer la charge émotionnelle dominante
        if emotion_counts:
            dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
            emotional_residue['dominant_emotional_charge'] = dominant_emotion
        
        # Calculer l'intensité émotionnelle globale
        total_significance = sum([event.get('significance', 0.5) for event in events])
        if events:
            emotional_residue['emotional_intensity'] = total_significance / len(events)
        
        # Calculer le spectre émotionnel
        total_count = sum(emotion_counts.values())
        for emotion, count in emotion_counts.items():
            avg_intensity = emotion_intensities[emotion] / count if count > 0 else 0.5
            emotional_residue['emotional_spectrum'][emotion] = {
                'proportion': count / total_count,
                'average_intensity': avg_intensity
            }
        
        # Évaluer la cohérence vibratoire
        if len(emotion_counts) == 1:
            emotional_residue['vibrational_coherence'] = 0.9  # Une seule émotion = très cohérent
        elif len(emotion_counts) == 2:
            emotional_residue['vibrational_coherence'] = 0.7  # Deux émotions = assez cohérent
        elif len(emotion_counts) == 3:
            emotional_residue['vibrational_coherence'] = 0.5  # Trois émotions = moyennement cohérent
        else:
            emotional_residue['vibrational_coherence'] = 0.3  # Plus de trois émotions = peu cohérent
        
        return emotional_residue
    
    def _analyze_memory_patterns(self, events):
        """Analyser les patterns de mémoire dans les événements historiques."""
        patterns = []
        
        if not events or len(events) < 5:
            return patterns
        
        # Trier les événements par date
        sorted_events = sorted(events, key=lambda x: x.get('date', ''))
        
        # Pattern 1: Cycles temporels
        # Chercher des événements similaires qui se répètent à intervalles réguliers
        event_years = []
        event_types = []
        
        for event in sorted_events:
            try:
                event_date = datetime.fromisoformat(event.get('date', ''))
                event_years.append(event_date.year)
                event_types.append(event.get('event_type', ''))
            except:
                pass
        
        # Chercher des cycles dans les types d'événements
        if len(event_types) >= 6:
            for cycle_length in range(2, 4):  # Chercher des cycles de longueur 2 ou 3
                for i in range(len(event_types) - cycle_length * 2):
                    cycle = event_types[i:i+cycle_length]
                    next_segment = event_types[i+cycle_length:i+cycle_length*2]
                    
                    if cycle == next_segment:
                        patterns.append({
                            'pattern_type': 'event_cycle',
                            'cycle_length': cycle_length,
                            'events': cycle,
                            'description': f"Cycle de {cycle_length} événements qui se répète: {', '.join(cycle)}"
                        })
                        break
        
        # Pattern 2: Progression d'intensité
        # Vérifier si les événements récents sont de plus en plus significatifs
        if len(sorted_events) >= 5:
            recent_events = sorted_events[-5:]
            significances = [event.get('significance', 0.5) for event in recent_events]
            
            increasing = True
            for i in range(len(significances) - 1):
                if significances[i] > significances[i+1]:
                    increasing = False
                    break
            
            if increasing and significances[-1] > significances[0] + 0.2:
                patterns.append({
                    'pattern_type': 'increasing_intensity',
                    'start_value': significances[0],
                    'end_value': significances[-1],
                    'description': "Progression d'intensité: les événements récents sont de plus en plus significatifs"
                })
        
        # Pattern 3: Concentration émotionnelle
        emotion_counts = defaultdict(int)
        for event in events:
            emotion_counts[event.get('emotional_charge', 'neutral')] += 1
        
        total_events = len(events)
        for emotion, count in emotion_counts.items():
            if count / total_events > 0.6:  # Si plus de 60% des événements ont la même charge émotionnelle
                patterns.append({
                    'pattern_type': 'emotional_concentration',
                    'emotion': emotion,
                    'proportion': count / total_events,
                    'description': f"Concentration émotionnelle: prédominance de la charge '{emotion}'"
                })
        
        # Pattern 4: Résonance historique
        # Chercher des événements qui résonnent fortement avec l'identité du stade
        high_impact_events = [event for event in events if event.get('significance', 0.5) > 0.8]
        if high_impact_events:
            patterns.append({
                'pattern_type': 'historical_anchors',
                'count': len(high_impact_events),
                'top_event': high_impact_events[0].get('description', ''),
                'description': f"Ancres historiques: {len(high_impact_events)} événements à très fort impact définissent l'identité du stade"
            })
        
        return patterns
    
    def _detect_cycle(self, values, cycle_size):
        """Détecter un cycle dans une série de valeurs."""
        # Méthode simplifiée pour détecter des cycles
        if len(values) < cycle_size * 2:
            return False
        
        # Comparer différentes sections de la séquence
        similarity_sum = 0
        comparisons = 0
        
        for i in range(len(values) - cycle_size):
            if i + cycle_size * 2 <= len(values):
                segment1 = values[i:i+cycle_size]
                segment2 = values[i+cycle_size:i+cycle_size*2]
                
                # Calculer la similarité (corrélation)
                correlation = np.corrcoef(segment1, segment2)[0, 1]
                
                if not np.isnan(correlation):
                    similarity_sum += correlation
                    comparisons += 1
        
        if comparisons > 0:
            avg_similarity = similarity_sum / comparisons
            return avg_similarity > 0.7
        
        return False