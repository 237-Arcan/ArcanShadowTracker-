"""
CycleMirror - Module d'analyse des cycles et coïncidences statistiques.
Détecte et évalue les patterns cycliques et les parallèles statistiques dans l'historique du football.
"""

import numpy as np
import random
from datetime import datetime, timedelta
import json
import os
from collections import deque
import math

class CycleMirror:
    """
    CycleMirror - Analyse des patterns cycliques et des coïncidences statistiques.
    Détecte les parallèles historiques, les cycles de performance et les "rhymes" dans l'histoire du football.
    """
    
    def __init__(self):
        """Initialise le module CycleMirror."""
        # Cycles temporels typiques dans le football
        self.temporal_cycles = {
            'season': {
                'period': 1,               # En années
                'description': 'Cycle annuel (saison complète)',
                'significance': 0.8,       # Importance statistique
                'predictive_power': 0.6    # Force prédictive
            },
            'manager_cycle': {
                'period': 3,               # En années
                'description': 'Cycle typique d'un entraîneur',
                'significance': 0.7,
                'predictive_power': 0.5
            },
            'team_generation': {
                'period': 4,               # En années
                'description': 'Cycle générationnel d'une équipe',
                'significance': 0.75,
                'predictive_power': 0.55
            },
            'league_dominance': {
                'period': 5,               # En années
                'description': 'Cycle de domination dans un championnat',
                'significance': 0.6,
                'predictive_power': 0.45
            },
            'international_cycle': {
                'period': 4,               # En années
                'description': 'Cycle entre compétitions internationales majeures',
                'significance': 0.65,
                'predictive_power': 0.4
            },
            'club_renaissance': {
                'period': 8,               # En années
                'description': 'Cycle de renaissance d'un club',
                'significance': 0.5,
                'predictive_power': 0.35
            }
        }
        
        # Types de coïncidences et parallèles historiques
        self.coincidence_types = {
            'career_parallel': {
                'description': 'Parallèle entre les trajectoires de carrière de joueurs',
                'recognition_threshold': 0.7,   # Seuil de reconnaissance
                'minimum_data_points': 5,       # Points de données minimums
                'statistical_weight': 0.6       # Poids dans les prédictions
            },
            'team_parallel': {
                'description': 'Parallèle entre équipes de différentes époques',
                'recognition_threshold': 0.75,
                'minimum_data_points': 8,
                'statistical_weight': 0.65
            },
            'title_sequence': {
                'description': 'Séquence récurrente de vainqueurs de titre',
                'recognition_threshold': 0.8,
                'minimum_data_points': 4,
                'statistical_weight': 0.7
            },
            'cross_competition': {
                'description': 'Corrélation entre résultats dans différentes compétitions',
                'recognition_threshold': 0.7,
                'minimum_data_points': 6,
                'statistical_weight': 0.55
            },
            'player_connection': {
                'description': 'Connexion statistique entre joueurs liés',
                'recognition_threshold': 0.65,
                'minimum_data_points': 4,
                'statistical_weight': 0.5
            },
            'numerical_pattern': {
                'description': 'Motif numérique récurrent dans les statistiques',
                'recognition_threshold': 0.85,
                'minimum_data_points': 7,
                'statistical_weight': 0.4
            }
        }
        
        # Historique des cycles détectés
        self.detected_cycles = []
        
        # Historique des parallèles détectés
        self.detected_parallels = []
        
        # Bases de données des événements historiques notables
        self.historical_events_db = {}
        
        # Configurations pour l'analyse de cycles
        self.cycle_analysis_config = {
            'min_cycle_period': 2,         # En années
            'max_cycle_period': 20,        # En années
            'peak_prominence': 0.3,        # Proéminence minimale pour détecter un pic
            'correlation_threshold': 0.7,  # Seuil de corrélation pour confirmation
            'min_repetitions': 2,          # Nombre minimum de répétitions pour confirmer un cycle
            'sensitivity': 0.65            # Sensibilité générale de la détection
        }
    
    def detect_team_cycles(self, team_data, category='performance'):
        """
        Détecter les cycles de performance ou autres caractéristiques d'une équipe.
        
        Args:
            team_data (dict): Données historiques de l'équipe
            category (str): Catégorie de cycle à analyser ('performance', 'style', 'management', etc.)
            
        Returns:
            dict: Cycles détectés et leur analyse
        """
        # Extraire les données pertinentes
        team_id = team_data.get('id', '')
        team_name = team_data.get('name', '')
        historical_data = team_data.get('historical_data', {})
        
        if not historical_data:
            return {
                'status': 'insufficient_data',
                'message': 'Données historiques insuffisantes pour détecter des cycles'
            }
        
        # Extraire la série temporelle selon la catégorie
        time_series = []
        years = []
        
        if category == 'performance':
            # Utiliser les classements ou points comme indicateur de performance
            for year, data in sorted(historical_data.items()):
                if 'league_position' in data:
                    # Inverser le classement pour que les meilleures performances soient plus élevées
                    max_position = 20  # Nombre d'équipes typique dans une ligue
                    normalized_position = (max_position - data['league_position'] + 1) / max_position
                    time_series.append(normalized_position)
                    years.append(int(year))
                elif 'points' in data and 'max_points' in data:
                    # Normaliser les points sur le maximum possible
                    normalized_points = data['points'] / data['max_points']
                    time_series.append(normalized_points)
                    years.append(int(year))
        
        elif category == 'style':
            # Utiliser des indicateurs de style de jeu (attaque, possession, etc.)
            for year, data in sorted(historical_data.items()):
                if 'attacking_rating' in data:
                    time_series.append(data['attacking_rating'])
                    years.append(int(year))
                elif 'style_index' in data:
                    time_series.append(data['style_index'])
                    years.append(int(year))
        
        elif category == 'management':
            # Utiliser les changements de management et stabilité
            for year, data in sorted(historical_data.items()):
                if 'manager_stability' in data:
                    time_series.append(data['manager_stability'])
                    years.append(int(year))
                elif 'management_changes' in data:
                    # Inverser pour que moins de changements = score plus élevé
                    normalized_changes = 1.0 - min(1.0, data['management_changes'] / 3.0)
                    time_series.append(normalized_changes)
                    years.append(int(year))
        
        else:  # Catégorie personnalisée ou non reconnue
            return {
                'status': 'invalid_category',
                'message': f'Catégorie de cycle "{category}" non reconnue ou non prise en charge'
            }
        
        # Vérifier si nous avons assez de données
        if len(time_series) < self.cycle_analysis_config['min_repetitions'] * 2:
            return {
                'status': 'insufficient_data',
                'message': f'Série temporelle trop courte ({len(time_series)} points) pour détecter des cycles fiables'
            }
        
        # Détecter les cycles potentiels
        detected_cycles = self._detect_cycles_in_timeseries(time_series, years)
        
        # Filtrer et évaluer les cycles détectés
        validated_cycles = self._validate_cycles(detected_cycles, time_series, years)
        
        # Prédire les prochains pics/creux basés sur les cycles
        future_predictions = self._predict_future_cycle_points(validated_cycles, time_series, years)
        
        # Enregistrer les cycles détectés
        for cycle in validated_cycles:
            self.detected_cycles.append({
                'team_id': team_id,
                'team_name': team_name,
                'category': category,
                'cycle_period': cycle['period'],
                'confidence': cycle['confidence'],
                'timestamp': datetime.now().isoformat()
            })
        
        # Préparer le résultat
        result = {
            'team_name': team_name,
            'category': category,
            'detected_cycles': validated_cycles,
            'future_predictions': future_predictions,
            'data_points': len(time_series),
            'year_range': f"{years[0]}-{years[-1]}",
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def find_historical_parallels(self, entity_data, entity_type='team', comparison_depth=30):
        """
        Trouver des parallèles historiques pour une équipe, un joueur ou une saison.
        
        Args:
            entity_data (dict): Données de l'entité (équipe, joueur, etc.)
            entity_type (str): Type d'entité ('team', 'player', 'season')
            comparison_depth (int): Nombre d'entités historiques à comparer
            
        Returns:
            dict: Parallèles historiques identifiés
        """
        # Extraire les informations de base
        entity_id = entity_data.get('id', '')
        entity_name = entity_data.get('name', '')
        
        # Charger la base de données historique correspondante
        historical_db = self._load_historical_database(entity_type)
        
        if not historical_db:
            return {
                'status': 'no_historical_database',
                'message': f'Base de données historique pour le type "{entity_type}" non disponible'
            }
        
        # Extraire le profil statistique de l'entité actuelle
        current_profile = self._extract_statistical_profile(entity_data, entity_type)
        
        if not current_profile:
            return {
                'status': 'invalid_entity_data',
                'message': 'Impossible d\'extraire un profil statistique valide des données fournies'
            }
        
        # Comparer avec les entités historiques
        parallels = []
        
        for hist_entity in historical_db[:comparison_depth]:
            hist_profile = self._extract_statistical_profile(hist_entity, entity_type)
            
            if not hist_profile:
                continue
            
            # Calculer la similarité
            similarity = self._calculate_profile_similarity(current_profile, hist_profile)
            
            # Si la similarité dépasse le seuil, c'est un parallèle potentiel
            if similarity['overall'] > 0.7:
                parallels.append({
                    'historical_entity': {
                        'id': hist_entity.get('id', ''),
                        'name': hist_entity.get('name', ''),
                        'era': hist_entity.get('era', ''),
                        'achievements': hist_entity.get('achievements', [])
                    },
                    'similarity': similarity,
                    'key_parallels': similarity['key_factors'],
                    'outcome_potential': self._extract_outcome_potential(hist_entity)
                })
        
        # Trier par similarité globale
        parallels.sort(key=lambda x: x['similarity']['overall'], reverse=True)
        
        # Classer les parallèles par type
        categorized_parallels = self._categorize_parallels(parallels, entity_type)
        
        # Préparer les insights basés sur les parallèles
        historical_insights = self._generate_historical_insights(parallels, entity_type)
        
        # Enregistrer les parallèles détectés
        for parallel in parallels[:3]:  # Garder uniquement les 3 plus pertinents
            self.detected_parallels.append({
                'entity_id': entity_id,
                'entity_name': entity_name,
                'entity_type': entity_type,
                'parallel_entity': parallel['historical_entity']['name'],
                'similarity': parallel['similarity']['overall'],
                'timestamp': datetime.now().isoformat()
            })
        
        # Préparer le résultat
        result = {
            'entity_name': entity_name,
            'entity_type': entity_type,
            'parallels_count': len(parallels),
            'top_parallels': parallels[:5],  # Limiter aux 5 meilleurs parallèles
            'categorized_parallels': categorized_parallels,
            'historical_insights': historical_insights,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def analyze_coincidental_patterns(self, pattern_data, pattern_type='sequence'):
        """
        Analyser les patterns de coïncidences statistiques ou séquentielles.
        
        Args:
            pattern_data (dict): Données du pattern à analyser
            pattern_type (str): Type de pattern ('sequence', 'correlation', 'numeric')
            
        Returns:
            dict: Analyse du pattern et sa signification statistique
        """
        # Vérifier le type de pattern
        if pattern_type not in ['sequence', 'correlation', 'numeric']:
            return {
                'status': 'invalid_pattern_type',
                'message': f'Type de pattern "{pattern_type}" non pris en charge'
            }
        
        # Initialiser les résultats
        pattern_analysis = {
            'pattern_type': pattern_type,
            'statistical_significance': 0.0,
            'coincidence_factor': 0.0,
            'repeatability': 0.0,
            'detected_instances': []
        }
        
        # Traiter selon le type de pattern
        if pattern_type == 'sequence':
            # Analyser une séquence d'événements (ex: ordre des vainqueurs)
            sequence = pattern_data.get('sequence', [])
            historical_sequences = pattern_data.get('historical_sequences', [])
            
            if not sequence or not historical_sequences:
                return {
                    'status': 'insufficient_data',
                    'message': 'Données de séquence insuffisantes pour l\'analyse'
                }
            
            # Calculer la signification statistique de la séquence
            pattern_analysis = self._analyze_event_sequence(sequence, historical_sequences)
            
        elif pattern_type == 'correlation':
            # Analyser une corrélation entre événements (ex: coïncidence entre compétitions)
            event_a = pattern_data.get('event_a', [])
            event_b = pattern_data.get('event_b', [])
            
            if not event_a or not event_b:
                return {
                    'status': 'insufficient_data',
                    'message': 'Données de corrélation insuffisantes pour l\'analyse'
                }
            
            # Calculer la signification statistique de la corrélation
            pattern_analysis = self._analyze_event_correlation(event_a, event_b)
            
        elif pattern_type == 'numeric':
            # Analyser un pattern numérique (ex: statistiques spécifiques)
            number_series = pattern_data.get('number_series', [])
            
            if not number_series or len(number_series) < 3:
                return {
                    'status': 'insufficient_data',
                    'message': 'Données numériques insuffisantes pour l\'analyse'
                }
            
            # Calculer la signification statistique du pattern numérique
            pattern_analysis = self._analyze_numeric_pattern(number_series)
        
        # Préparer une explication narrative du pattern
        pattern_explanation = self._generate_pattern_explanation(pattern_analysis, pattern_data, pattern_type)
        
        # Préparer le résultat final
        result = {
            'pattern_type': pattern_type,
            'analysis': pattern_analysis,
            'explanation': pattern_explanation,
            'coincidence_level': self._classify_coincidence_level(pattern_analysis['coincidence_factor']),
            'predictive_value': self._calculate_predictive_value(pattern_analysis),
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def predict_based_on_cycles(self, target_data, target_type='team', season=None):
        """
        Générer des prédictions basées sur les cycles détectés.
        
        Args:
            target_data (dict): Données de la cible (équipe, joueur, etc.)
            target_type (str): Type de cible ('team', 'player', 'league')
            season (str, optional): Saison pour laquelle générer la prédiction
            
        Returns:
            dict: Prédictions basées sur les cycles
        """
        # Extraire les informations de base
        target_id = target_data.get('id', '')
        target_name = target_data.get('name', '')
        
        # Définir la saison si non spécifiée
        if not season:
            current_year = datetime.now().year
            season = f"{current_year-1}-{current_year}"
        
        # Récupérer les cycles détectés pour cette cible
        relevant_cycles = []
        for cycle in self.detected_cycles:
            if target_type == 'team' and cycle.get('team_id', '') == target_id:
                relevant_cycles.append(cycle)
        
        # Si aucun cycle n'a été détecté, en chercher maintenant
        if not relevant_cycles and target_type == 'team':
            cycles_result = self.detect_team_cycles(target_data, 'performance')
            if 'detected_cycles' in cycles_result:
                for cycle in cycles_result['detected_cycles']:
                    relevant_cycles.append({
                        'team_id': target_id,
                        'team_name': target_name,
                        'category': 'performance',
                        'cycle_period': cycle['period'],
                        'confidence': cycle['confidence']
                    })
        
        # Récupérer les parallèles historiques pour cette cible
        relevant_parallels = []
        for parallel in self.detected_parallels:
            if parallel.get('entity_type', '') == target_type and parallel.get('entity_id', '') == target_id:
                relevant_parallels.append(parallel)
        
        # Si aucun parallèle n'a été détecté, en chercher maintenant
        if not relevant_parallels:
            parallels_result = self.find_historical_parallels(target_data, target_type)
            if 'top_parallels' in parallels_result:
                for parallel in parallels_result['top_parallels']:
                    relevant_parallels.append({
                        'entity_id': target_id,
                        'entity_name': target_name,
                        'entity_type': target_type,
                        'parallel_entity': parallel['historical_entity']['name'],
                        'similarity': parallel['similarity']['overall']
                    })
        
        # Générer des prédictions basées sur les cycles
        cycle_predictions = []
        for cycle in relevant_cycles:
            cycle_period = cycle.get('cycle_period', 0)
            confidence = cycle.get('confidence', 0.0)
            
            if cycle_period > 0:
                cycle_prediction = self._generate_cycle_prediction(target_data, cycle_period, confidence, season)
                if cycle_prediction:
                    cycle_predictions.append(cycle_prediction)
        
        # Générer des prédictions basées sur les parallèles historiques
        parallel_predictions = []
        for parallel in relevant_parallels:
            parallel_entity = parallel.get('parallel_entity', '')
            similarity = parallel.get('similarity', 0.0)
            
            if parallel_entity and similarity > 0.7:
                parallel_prediction = self._generate_parallel_prediction(target_data, parallel_entity, similarity, season)
                if parallel_prediction:
                    parallel_predictions.append(parallel_prediction)
        
        # Combiner les prédictions en une prédiction globale
        combined_prediction = self._combine_cycle_predictions(cycle_predictions, parallel_predictions)
        
        # Préparer le résultat
        result = {
            'target_name': target_name,
            'target_type': target_type,
            'season': season,
            'cycle_predictions': cycle_predictions,
            'historical_parallel_predictions': parallel_predictions,
            'combined_prediction': combined_prediction,
            'prediction_confidence': self._calculate_prediction_confidence(cycle_predictions, parallel_predictions),
            'prediction_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def _detect_cycles_in_timeseries(self, time_series, years):
        """Détecter les cycles potentiels dans une série temporelle."""
        # Méthode simplifiée: recherche de périodicité par auto-corrélation
        cycles = []
        
        # Écart minimum entre les années
        min_years = self.cycle_analysis_config['min_cycle_period']
        max_years = min(self.cycle_analysis_config['max_cycle_period'], len(years) // 2)
        
        # Tester différentes périodes possibles
        for period in range(min_years, max_years + 1):
            # Calculer l'auto-corrélation à ce décalage
            correlation = self._calculate_autocorrelation(time_series, period)
            
            # Si la corrélation est suffisamment forte, c'est un cycle potentiel
            if correlation > self.cycle_analysis_config['correlation_threshold']:
                # Vérifier si nous voyons des répétitions claires
                peaks = self._find_peaks_in_series(time_series)
                repeats = self._check_peak_periodicity(peaks, period, len(time_series))
                
                if repeats >= self.cycle_analysis_config['min_repetitions']:
                    cycles.append({
                        'period': period,
                        'correlation': correlation,
                        'repetitions_found': repeats,
                        'years': period if isinstance(period, int) else period * (years[1] - years[0])
                    })
        
        return cycles
    
    def _validate_cycles(self, detected_cycles, time_series, years):
        """Valider et affiner les cycles détectés."""
        validated_cycles = []
        
        for cycle in detected_cycles:
            period = cycle['period']
            correlation = cycle['correlation']
            
            # Vérifier la répétabilité du cycle en divisant la série
            if len(time_series) >= period * 2:
                segments = [time_series[i:i+period] for i in range(0, len(time_series) - period + 1, period)]
                
                if len(segments) >= 2:
                    segment_correlations = []
                    for i in range(len(segments) - 1):
                        segment_corr = self._calculate_correlation(segments[i], segments[i+1])
                        segment_correlations.append(segment_corr)
                    
                    avg_segment_correlation = sum(segment_correlations) / len(segment_correlations)
                    
                    # Calculer un score de confiance
                    confidence = (correlation * 0.6) + (avg_segment_correlation * 0.4)
                    
                    # Classer la force du cycle
                    cycle_strength = 'moderate'
                    if confidence > 0.85:
                        cycle_strength = 'very_strong'
                    elif confidence > 0.75:
                        cycle_strength = 'strong'
                    elif confidence < 0.6:
                        cycle_strength = 'weak'
                    
                    # Si la confiance est suffisante, le cycle est validé
                    if confidence > 0.6:
                        validated_cycles.append({
                            'period': period,
                            'years': period if isinstance(period, int) else int(period * (years[1] - years[0])),
                            'confidence': confidence,
                            'strength': cycle_strength,
                            'detected_repetitions': cycle['repetitions_found']
                        })
        
        # Trier par confiance
        validated_cycles.sort(key=lambda x: x['confidence'], reverse=True)
        
        return validated_cycles
    
    def _predict_future_cycle_points(self, validated_cycles, time_series, years):
        """Prédire les prochains points hauts/bas du cycle."""
        predictions = []
        
        current_year = datetime.now().year
        
        for cycle in validated_cycles:
            period = cycle['period']
            confidence = cycle['confidence']
            
            # Trouver les pics et creux récents
            peaks = self._find_peaks_in_series(time_series)
            troughs = self._find_troughs_in_series(time_series)
            
            # Pour chaque pic/creux, projeter au prochain cycle
            for peak_idx in peaks:
                peak_year = years[peak_idx]
                years_since_peak = current_year - peak_year
                years_to_next_peak = period - (years_since_peak % period)
                
                if years_to_next_peak > 0:
                    next_peak_year = current_year + years_to_next_peak
                    predictions.append({
                        'type': 'peak',
                        'year': next_peak_year,
                        'confidence': confidence * (1 - (years_to_next_peak / (period * 2))),
                        'based_on_cycle': period,
                        'description': f"Pic de performance prévu en {next_peak_year} (cycle de {period} ans)"
                    })
            
            for trough_idx in troughs:
                trough_year = years[trough_idx]
                years_since_trough = current_year - trough_year
                years_to_next_trough = period - (years_since_trough % period)
                
                if years_to_next_trough > 0:
                    next_trough_year = current_year + years_to_next_trough
                    predictions.append({
                        'type': 'trough',
                        'year': next_trough_year,
                        'confidence': confidence * (1 - (years_to_next_trough / (period * 2))),
                        'based_on_cycle': period,
                        'description': f"Creux de performance prévu en {next_trough_year} (cycle de {period} ans)"
                    })
        
        # Trier chronologiquement
        predictions.sort(key=lambda x: x['year'])
        
        # Regrouper par année si plusieurs prédictions pour la même année
        grouped_predictions = {}
        for prediction in predictions:
            year = prediction['year']
            if year not in grouped_predictions:
                grouped_predictions[year] = []
            grouped_predictions[year].append(prediction)
        
        # Fusionner les prédictions pour la même année
        merged_predictions = []
        for year, year_predictions in grouped_predictions.items():
            if len(year_predictions) > 1:
                # Si plusieurs prédictions pour la même année, prendre celle avec la plus haute confiance
                best_prediction = max(year_predictions, key=lambda x: x['confidence'])
                merged_predictions.append(best_prediction)
            else:
                merged_predictions.append(year_predictions[0])
        
        return merged_predictions
    
    def _calculate_autocorrelation(self, series, lag):
        """Calculer l'auto-corrélation d'une série temporelle avec un décalage donné."""
        # Vérifier que le lag n'est pas plus grand que la série
        if lag >= len(series):
            return 0.0
        
        # Séries décalées
        series1 = series[:-lag]
        series2 = series[lag:]
        
        # Calcul de la corrélation
        return self._calculate_correlation(series1, series2)
    
    def _calculate_correlation(self, series1, series2):
        """Calculer la corrélation entre deux séries."""
        # Vérifier qu'elles ont la même longueur
        min_len = min(len(series1), len(series2))
        series1 = series1[:min_len]
        series2 = series2[:min_len]
        
        if min_len == 0:
            return 0.0
        
        # Calcul de la moyenne
        mean1 = sum(series1) / min_len
        mean2 = sum(series2) / min_len
        
        # Calcul de la covariance et des variances
        covariance = sum((series1[i] - mean1) * (series2[i] - mean2) for i in range(min_len))
        variance1 = sum((x - mean1) ** 2 for x in series1)
        variance2 = sum((x - mean2) ** 2 for x in series2)
        
        # Éviter la division par zéro
        if variance1 == 0 or variance2 == 0:
            return 0.0
        
        # Calcul du coefficient de corrélation
        correlation = covariance / (math.sqrt(variance1) * math.sqrt(variance2))
        
        return correlation
    
    def _find_peaks_in_series(self, series):
        """Trouver les indices des pics dans une série."""
        peaks = []
        
        # Exclure les bords
        for i in range(1, len(series) - 1):
            if series[i] > series[i-1] and series[i] > series[i+1]:
                # Vérifier si le pic est suffisamment proéminent
                prominence = min(series[i] - series[i-1], series[i] - series[i+1])
                if prominence > self.cycle_analysis_config['peak_prominence']:
                    peaks.append(i)
        
        return peaks
    
    def _find_troughs_in_series(self, series):
        """Trouver les indices des creux dans une série."""
        troughs = []
        
        # Exclure les bords
        for i in range(1, len(series) - 1):
            if series[i] < series[i-1] and series[i] < series[i+1]:
                # Vérifier si le creux est suffisamment proéminent
                prominence = min(series[i-1] - series[i], series[i+1] - series[i])
                if prominence > self.cycle_analysis_config['peak_prominence']:
                    troughs.append(i)
        
        return troughs
    
    def _check_peak_periodicity(self, peaks, period, series_length):
        """Vérifier si les pics suivent une périodicité donnée."""
        if not peaks or len(peaks) < 2:
            return 0
        
        # Compter combien de pics respectent la périodicité
        periodicity_count = 0
        
        for i in range(len(peaks) - 1):
            for j in range(i + 1, len(peaks)):
                if abs(peaks[j] - peaks[i]) % period <= 1:  # Tolérance de 1
                    periodicity_count += 1
        
        return periodicity_count
    
    def _load_historical_database(self, entity_type):
        """Charger la base de données des entités historiques."""
        # Cette fonction simule le chargement d'une base de données
        # En production, elle chargerait des données réelles depuis une source externe
        
        if entity_type == 'team':
            return [
                {
                    'id': 'hist_team_1',
                    'name': 'Ajax Amsterdam 1995',
                    'era': '1994-1996',
                    'achievements': ['Champions League 1995', 'Eredivisie 1995', 'Eredivisie 1996'],
                    'profile': {
                        'style': 'total_football',
                        'youth_focus': 0.9,
                        'avg_age': 23.5,
                        'international_players': 15,
                        'goals_per_game': 2.3,
                        'conceded_per_game': 0.7
                    }
                },
                {
                    'id': 'hist_team_2',
                    'name': 'Barcelona 2011',
                    'era': '2008-2012',
                    'achievements': ['Champions League 2009', 'Champions League 2011', 'La Liga 2009-2011'],
                    'profile': {
                        'style': 'tiki_taka',
                        'youth_focus': 0.8,
                        'avg_age': 26.2,
                        'international_players': 18,
                        'goals_per_game': 2.7,
                        'conceded_per_game': 0.8
                    }
                },
                {
                    'id': 'hist_team_3',
                    'name': 'Milan 1989',
                    'era': '1988-1994',
                    'achievements': ['European Cup 1989', 'European Cup 1990', 'Serie A 1992'],
                    'profile': {
                        'style': 'catenaccio_evolved',
                        'youth_focus': 0.6,
                        'avg_age': 27.8,
                        'international_players': 16,
                        'goals_per_game': 2.0,
                        'conceded_per_game': 0.5
                    }
                }
            ]
        elif entity_type == 'player':
            return [
                {
                    'id': 'hist_player_1',
                    'name': 'Pelé',
                    'era': '1956-1977',
                    'achievements': ['World Cup 1958', 'World Cup 1962', 'World Cup 1970'],
                    'profile': {
                        'position': 'forward',
                        'goals_ratio': 0.92,
                        'international_caps': 92,
                        'international_goals': 77,
                        'career_peak_age': 28
                    }
                },
                {
                    'id': 'hist_player_2',
                    'name': 'Johan Cruyff',
                    'era': '1964-1984',
                    'achievements': ['Ballon d\'Or 1971', 'Ballon d\'Or 1973', 'Ballon d\'Or 1974'],
                    'profile': {
                        'position': 'forward',
                        'goals_ratio': 0.63,
                        'international_caps': 48,
                        'international_goals': 33,
                        'career_peak_age': 27
                    }
                }
            ]
        
        # Si type non pris en charge, retourner une liste vide
        return []
    
    def _extract_statistical_profile(self, entity_data, entity_type):
        """Extraire un profil statistique à partir des données d'une entité."""
        profile = {}
        
        if entity_type == 'team':
            # Extraire des caractéristiques clés pour les équipes
            profile = {
                'style': entity_data.get('playing_style', entity_data.get('style', 'unknown')),
                'youth_focus': entity_data.get('youth_focus', entity_data.get('youth_development', 0.5)),
                'avg_age': entity_data.get('average_age', entity_data.get('avg_age', 26.0)),
                'international_players': entity_data.get('international_players', 10),
                'goals_per_game': entity_data.get('goals_per_game', 1.5),
                'conceded_per_game': entity_data.get('conceded_per_game', 1.2)
            }
        elif entity_type == 'player':
            # Extraire des caractéristiques clés pour les joueurs
            profile = {
                'position': entity_data.get('position', 'unknown'),
                'goals_ratio': entity_data.get('goals_ratio', entity_data.get('goals_per_game', 0.3)),
                'international_caps': entity_data.get('international_caps', 0),
                'international_goals': entity_data.get('international_goals', 0),
                'career_peak_age': entity_data.get('peak_age', entity_data.get('career_peak_age', 27))
            }
        
        return profile
    
    def _calculate_profile_similarity(self, profile1, profile2):
        """Calculer la similarité entre deux profils statistiques."""
        # Liste pour stocker les similarités par facteur
        factor_similarities = []
        key_factors = []
        
        # Comparer chaque facteur commun
        common_factors = set(profile1.keys()).intersection(set(profile2.keys()))
        
        for factor in common_factors:
            # Comparer les valeurs selon leur type
            val1 = profile1[factor]
            val2 = profile2[factor]
            
            similarity = 0.0
            
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                # Pour les valeurs numériques, calculer une similarité normalisée
                max_val = max(abs(val1), abs(val2))
                if max_val > 0:
                    similarity = 1.0 - (abs(val1 - val2) / max_val)
                else:
                    similarity = 1.0  # Les deux sont zéro
            elif isinstance(val1, str) and isinstance(val2, str):
                # Pour les chaînes, vérifier l'égalité
                similarity = 1.0 if val1 == val2 else 0.0
            
            factor_similarities.append((factor, similarity))
            
            # Si la similarité est forte, ajouter aux facteurs clés
            if similarity > 0.8:
                key_factors.append({
                    'factor': factor,
                    'similarity': similarity,
                    'values': {'current': val1, 'historical': val2}
                })
        
        # Calculer la moyenne pour obtenir la similarité globale
        overall_similarity = 0.0
        if factor_similarities:
            overall_similarity = sum(sim for _, sim in factor_similarities) / len(factor_similarities)
        
        # Trier les facteurs clés par similarité
        key_factors.sort(key=lambda x: x['similarity'], reverse=True)
        
        return {
            'overall': overall_similarity,
            'factor_count': len(factor_similarities),
            'key_factors': key_factors[:3]  # Limiter aux 3 plus similaires
        }
    
    def _extract_outcome_potential(self, historical_entity):
        """Extraire le potentiel de résultats basé sur une entité historique."""
        # Extraire les réalisations de l'entité historique
        achievements = historical_entity.get('achievements', [])
        
        # Examiner les années suivant l'ère spécifiée
        era = historical_entity.get('era', '')
        subsequent_achievements = []
        
        if era:
            # Extraire l'année de fin d'ère
            try:
                end_year = int(era.split('-')[1])
                
                # Filtrer les réalisations ultérieures
                subsequent_achievements = [
                    achievement for achievement in achievements
                    if any(str(year) in achievement for year in range(end_year + 1, end_year + 5))
                ]
            except (IndexError, ValueError):
                pass
        
        # Si pas d'informations ultérieures, utiliser toutes les réalisations
        if not subsequent_achievements:
            subsequent_achievements = achievements
        
        # Préparer le résultat
        outcome = {
            'potential_achievements': subsequent_achievements,
            'success_continuation': len(subsequent_achievements) > 0,
            'achievement_types': self._categorize_achievements(subsequent_achievements)
        }
        
        return outcome
    
    def _categorize_achievements(self, achievements):
        """Catégoriser les types de réalisations."""
        categories = {
            'domestic': 0,
            'continental': 0,
            'international': 0,
            'individual': 0
        }
        
        for achievement in achievements:
            achievement_lower = achievement.lower()
            
            if any(term in achievement_lower for term in ['league', 'cup', 'copa', 'serie', 'bundesliga', 'ligue', 'eredivisie']):
                categories['domestic'] += 1
            
            if any(term in achievement_lower for term in ['champions league', 'europa', 'libertadores', 'european cup']):
                categories['continental'] += 1
            
            if any(term in achievement_lower for term in ['world cup', 'euro', 'copa america', 'nations']):
                categories['international'] += 1
            
            if any(term in achievement_lower for term in ['ballon d\'or', 'player of the year', 'golden boot']):
                categories['individual'] += 1
        
        return categories
    
    def _categorize_parallels(self, parallels, entity_type):
        """Classer les parallèles par type."""
        categorized = {}
        
        if entity_type == 'team':
            categorized = {
                'style_parallels': [],
                'performance_parallels': [],
                'developmental_parallels': []
            }
            
            for parallel in parallels:
                key_factors = parallel.get('key_parallels', [])
                
                # Classer selon les facteurs clés
                for factor in key_factors:
                    factor_name = factor.get('factor', '')
                    
                    if factor_name in ['style', 'goals_per_game', 'conceded_per_game']:
                        categorized['style_parallels'].append(parallel)
                        break
                    elif factor_name in ['youth_focus', 'avg_age']:
                        categorized['developmental_parallels'].append(parallel)
                        break
                    else:
                        categorized['performance_parallels'].append(parallel)
                        break
        
        elif entity_type == 'player':
            categorized = {
                'career_path_parallels': [],
                'performance_parallels': [],
                'style_parallels': []
            }
            
            # Classification similaire pour les joueurs...
        
        return categorized
    
    def _generate_historical_insights(self, parallels, entity_type):
        """Générer des insights basés sur les parallèles historiques."""
        insights = []
        
        if not parallels:
            return insights
        
        # Agréger les potentiels résultats des parallèles
        potential_outcomes = []
        for parallel in parallels:
            outcome = parallel.get('outcome_potential', {})
            if outcome and 'potential_achievements' in outcome:
                for achievement in outcome['potential_achievements']:
                    potential_outcomes.append({
                        'achievement': achievement,
                        'source_parallel': parallel['historical_entity']['name'],
                        'similarity': parallel['similarity']['overall']
                    })
        
        # Grouper les résultats similaires
        grouped_outcomes = {}
        for outcome in potential_outcomes:
            achievement = outcome['achievement']
            achievement_type = next((k for k, v in self._categorize_achievements({achievement}).items() if v > 0), 'other')
            
            key = f"{achievement_type}:{achievement}"
            if key not in grouped_outcomes:
                grouped_outcomes[key] = {
                    'achievement': achievement,
                    'type': achievement_type,
                    'sources': [],
                    'average_similarity': 0.0
                }
            
            grouped_outcomes[key]['sources'].append({
                'parallel': outcome['source_parallel'],
                'similarity': outcome['similarity']
            })
            
            # Recalculer la similarité moyenne
            similarities = [source['similarity'] for source in grouped_outcomes[key]['sources']]
            grouped_outcomes[key]['average_similarity'] = sum(similarities) / len(similarities)
        
        # Convertir en liste et trier par similarité moyenne
        insight_outcomes = list(grouped_outcomes.values())
        insight_outcomes.sort(key=lambda x: x['average_similarity'], reverse=True)
        
        # Générer des insights à partir des résultats
        if insight_outcomes:
            top_outcome = insight_outcomes[0]
            insights.append({
                'type': 'historical_projection',
                'content': f"Les parallèles historiques suggèrent un potentiel pour: {top_outcome['achievement']}",
                'confidence': top_outcome['average_similarity'],
                'supporting_evidence': [source['parallel'] for source in top_outcome['sources']]
            })
        
        # Identifier des tendances communes
        common_traits = self._identify_common_traits(parallels)
        if common_traits:
            insights.append({
                'type': 'common_traits',
                'content': f"Traits communs avec les parallèles historiques: {', '.join(common_traits)}",
                'confidence': 0.7,
                'supporting_evidence': [parallel['historical_entity']['name'] for parallel in parallels[:3]]
            })
        
        return insights
    
    def _identify_common_traits(self, parallels):
        """Identifier les traits communs parmi les parallèles."""
        if not parallels or len(parallels) < 2:
            return []
        
        # Extraire les traits mentionnés dans les facteurs clés
        trait_counts = {}
        
        for parallel in parallels:
            key_factors = parallel.get('key_parallels', [])
            
            for factor in key_factors:
                factor_name = factor.get('factor', '')
                
                if factor_name not in trait_counts:
                    trait_counts[factor_name] = 0
                
                trait_counts[factor_name] += 1
        
        # Sélectionner les traits qui apparaissent dans au moins 2 parallèles
        common_traits = [factor for factor, count in trait_counts.items() if count >= 2]
        
        return common_traits
    
    def _analyze_event_sequence(self, sequence, historical_sequences):
        """Analyser une séquence d'événements et sa signification statistique."""
        if not sequence or not historical_sequences:
            return {
                'statistical_significance': 0.0,
                'coincidence_factor': 0.0,
                'repeatability': 0.0,
                'detected_instances': []
            }
        
        # Compter les occurrences de la séquence dans l'historique
        detected_instances = []
        sequence_length = len(sequence)
        
        for i, hist_sequence in enumerate(historical_sequences):
            if len(hist_sequence) >= sequence_length:
                # Rechercher la séquence exacte
                for j in range(len(hist_sequence) - sequence_length + 1):
                    subsequence = hist_sequence[j:j+sequence_length]
                    
                    # Calculer la similarité
                    similarity = sum(1 for k in range(sequence_length) if subsequence[k] == sequence[k]) / sequence_length
                    
                    if similarity >= 0.7:  # 70% de correspondance
                        detected_instances.append({
                            'historical_sequence_id': i,
                            'start_position': j,
                            'similarity': similarity,
                            'matching_elements': sum(1 for k in range(sequence_length) if subsequence[k] == sequence[k])
                        })
        
        # Calculer la signification statistique
        total_subsequences = sum(len(hist_seq) - sequence_length + 1 for hist_seq in historical_sequences if len(hist_seq) >= sequence_length)
        
        if total_subsequences == 0:
            return {
                'statistical_significance': 0.0,
                'coincidence_factor': 0.0,
                'repeatability': 0.0,
                'detected_instances': []
            }
        
        # Probabilité d'occurrence aléatoire
        # Plus le nombre d'instances détectées est élevé par rapport au total, plus la séquence est statistiquement significative
        statistical_significance = len(detected_instances) / total_subsequences
        
        # Facteur de coïncidence (combinaison de significativité et similarité)
        avg_similarity = sum(instance['similarity'] for instance in detected_instances) / len(detected_instances) if detected_instances else 0
        coincidence_factor = (statistical_significance * 0.7) + (avg_similarity * 0.3)
        
        # Répétabilité (constance dans l'historique)
        unique_histories = len(set(instance['historical_sequence_id'] for instance in detected_instances))
        repeatability = unique_histories / len(historical_sequences) if historical_sequences else 0
        
        return {
            'statistical_significance': statistical_significance,
            'coincidence_factor': coincidence_factor,
            'repeatability': repeatability,
            'detected_instances': detected_instances
        }
    
    def _analyze_event_correlation(self, event_a, event_b):
        """Analyser la corrélation entre deux séries d'événements."""
        if not event_a or not event_b:
            return {
                'statistical_significance': 0.0,
                'coincidence_factor': 0.0,
                'repeatability': 0.0,
                'detected_instances': []
            }
        
        # Vérifier si les événements sont de même longueur
        min_length = min(len(event_a), len(event_b))
        event_a = event_a[:min_length]
        event_b = event_b[:min_length]
        
        # Calculer la corrélation
        correlation = self._calculate_correlation(event_a, event_b)
        
        # Détecter les instances où les deux événements montrent une forte correspondance
        detected_instances = []
        for i in range(min_length):
            if abs(event_a[i] - event_b[i]) < 0.2 * max(abs(event_a[i]), abs(event_b[i])):
                detected_instances.append({
                    'position': i,
                    'value_a': event_a[i],
                    'value_b': event_b[i],
                    'correlation': 1.0 - (abs(event_a[i] - event_b[i]) / max(abs(event_a[i]), abs(event_b[i])))
                })
        
        # Calculer la significativité statistique
        statistical_significance = len(detected_instances) / min_length
        
        # Facteur de coïncidence
        coincidence_factor = (correlation * 0.7) + (statistical_significance * 0.3)
        
        # Répétabilité (constance à travers les données)
        repeatability = sum(instance['correlation'] for instance in detected_instances) / len(detected_instances) if detected_instances else 0
        
        return {
            'statistical_significance': statistical_significance,
            'coincidence_factor': coincidence_factor,
            'repeatability': repeatability,
            'correlation': correlation,
            'detected_instances': detected_instances
        }
    
    def _analyze_numeric_pattern(self, number_series):
        """Analyser un pattern numérique et sa signification statistique."""
        if not number_series or len(number_series) < 3:
            return {
                'statistical_significance': 0.0,
                'coincidence_factor': 0.0,
                'repeatability': 0.0,
                'detected_instances': []
            }
        
        # Vérifier différents types de patterns
        patterns_tested = {
            'arithmetic': self._test_arithmetic_progression(number_series),
            'geometric': self._test_geometric_progression(number_series),
            'fibonacci': self._test_fibonacci_like(number_series),
            'repeating': self._test_repeating_pattern(number_series)
        }
        
        # Déterminer le pattern le plus fort
        best_pattern = max(patterns_tested.items(), key=lambda x: x[1]['confidence'])
        
        # Si aucun pattern n'est suffisamment fort, c'est une série aléatoire
        if best_pattern[1]['confidence'] < 0.4:
            return {
                'statistical_significance': 0.2,
                'coincidence_factor': 0.1,
                'repeatability': 0.0,
                'detected_instances': [],
                'best_pattern': 'random',
                'pattern_confidence': 0.0
            }
        
        # Calculer la signification statistique
        statistical_significance = best_pattern[1]['confidence'] * 0.8
        
        # Facteur de coïncidence
        coincidence_factor = best_pattern[1]['confidence'] * 0.7
        
        # Répétabilité
        repeatability = best_pattern[1]['coverage']
        
        return {
            'statistical_significance': statistical_significance,
            'coincidence_factor': coincidence_factor,
            'repeatability': repeatability,
            'detected_instances': best_pattern[1].get('instances', []),
            'best_pattern': best_pattern[0],
            'pattern_confidence': best_pattern[1]['confidence'],
            'pattern_parameters': best_pattern[1].get('parameters', {})
        }
    
    def _test_arithmetic_progression(self, series):
        """Tester si une série suit une progression arithmétique."""
        if len(series) < 3:
            return {'confidence': 0.0, 'coverage': 0.0}
        
        # Calculer les différences entre éléments consécutifs
        differences = [series[i+1] - series[i] for i in range(len(series)-1)]
        
        # Calculer la différence moyenne
        avg_diff = sum(differences) / len(differences)
        
        # Calculer l'écart type pour vérifier la constance
        std_dev = math.sqrt(sum((d - avg_diff)**2 for d in differences) / len(differences))
        
        # Normaliser l'écart type pour obtenir un score de confiance
        max_diff = max(abs(d) for d in differences)
        normalized_std = std_dev / max_diff if max_diff > 0 else 0
        
        confidence = 1.0 - normalized_std
        
        # Compter combien d'éléments suivent le pattern
        matching_elements = 0
        for i in range(len(series)-1):
            if abs(series[i+1] - series[i] - avg_diff) < 0.1 * abs(avg_diff):
                matching_elements += 1
        
        coverage = matching_elements / (len(series) - 1)
        
        return {
            'confidence': confidence,
            'coverage': coverage,
            'parameters': {'common_difference': avg_diff},
            'instances': [{'position': i, 'expected': series[i-1] + avg_diff, 'actual': series[i]} for i in range(1, len(series))]
        }
    
    def _test_geometric_progression(self, series):
        """Tester si une série suit une progression géométrique."""
        if len(series) < 3 or any(x == 0 for x in series):
            return {'confidence': 0.0, 'coverage': 0.0}
        
        # Calculer les ratios entre éléments consécutifs
        ratios = [series[i+1] / series[i] for i in range(len(series)-1) if series[i] != 0]
        
        if not ratios:
            return {'confidence': 0.0, 'coverage': 0.0}
        
        # Calculer le ratio moyen
        avg_ratio = sum(ratios) / len(ratios)
        
        # Calculer l'écart type pour vérifier la constance
        std_dev = math.sqrt(sum((r - avg_ratio)**2 for r in ratios) / len(ratios))
        
        # Normaliser l'écart type pour obtenir un score de confiance
        normalized_std = std_dev / avg_ratio if avg_ratio > 0 else 0
        
        confidence = 1.0 - normalized_std
        
        # Compter combien d'éléments suivent le pattern
        matching_elements = 0
        for i in range(len(series)-1):
            if series[i] != 0 and abs(series[i+1] / series[i] - avg_ratio) < 0.1 * avg_ratio:
                matching_elements += 1
        
        coverage = matching_elements / (len(series) - 1)
        
        return {
            'confidence': confidence,
            'coverage': coverage,
            'parameters': {'common_ratio': avg_ratio},
            'instances': [{'position': i, 'expected': series[i-1] * avg_ratio, 'actual': series[i]} for i in range(1, len(series))]
        }
    
    def _test_fibonacci_like(self, series):
        """Tester si une série suit un pattern similaire à Fibonacci (chaque élément est la somme des deux précédents)."""
        if len(series) < 3:
            return {'confidence': 0.0, 'coverage': 0.0}
        
        # Vérifier si chaque élément est approximativement la somme des deux précédents
        matching_elements = 0
        instances = []
        
        for i in range(2, len(series)):
            expected = series[i-1] + series[i-2]
            actual = series[i]
            error = abs(expected - actual) / max(1, abs(expected))
            
            if error < 0.1:  # 10% de tolérance
                matching_elements += 1
                instances.append({
                    'position': i,
                    'expected': expected,
                    'actual': actual,
                    'error': error
                })
        
        coverage = matching_elements / (len(series) - 2)
        confidence = coverage * 0.9  # Facteur de conviction
        
        return {
            'confidence': confidence,
            'coverage': coverage,
            'instances': instances
        }
    
    def _test_repeating_pattern(self, series):
        """Tester si une série contient un pattern répétitif."""
        if len(series) < 4:
            return {'confidence': 0.0, 'coverage': 0.0}
        
        best_pattern_length = 0
        best_confidence = 0.0
        best_coverage = 0.0
        best_instances = []
        
        # Tester différentes longueurs de pattern
        for pattern_length in range(1, len(series) // 2 + 1):
            # Extraire le premier motif supposé
            pattern = series[:pattern_length]
            
            # Vérifier combien de fois ce motif se répète
            matching_elements = 0
            instances = []
            
            for i in range(pattern_length, len(series), pattern_length):
                # S'assurer que nous avons assez d'éléments pour comparer
                remaining = min(pattern_length, len(series) - i)
                
                # Compter les correspondances
                matches = 0
                for j in range(remaining):
                    expected = pattern[j]
                    actual = series[i + j]
                    error = abs(expected - actual) / max(1, abs(expected))
                    
                    if error < 0.1:  # 10% de tolérance
                        matches += 1
                        instances.append({
                            'position': i + j,
                            'expected': expected,
                            'actual': actual,
                            'error': error
                        })
                
                matching_elements += matches
            
            # Calculer la couverture
            coverage = matching_elements / (len(series) - pattern_length)
            
            # Calculer la confiance (plus le pattern est long et bien répété, plus la confiance est élevée)
            repeat_count = (len(series) - pattern_length) / pattern_length
            confidence = coverage * (1.0 - (1.0 / (1.0 + repeat_count)))
            
            if confidence > best_confidence:
                best_pattern_length = pattern_length
                best_confidence = confidence
                best_coverage = coverage
                best_instances = instances
        
        return {
            'confidence': best_confidence,
            'coverage': best_coverage,
            'parameters': {'pattern_length': best_pattern_length},
            'instances': best_instances
        }
    
    def _generate_pattern_explanation(self, pattern_analysis, pattern_data, pattern_type):
        """Générer une explication narrative du pattern détecté."""
        if pattern_type == 'numeric':
            # Explication pour les patterns numériques
            best_pattern = pattern_analysis.get('best_pattern', 'random')
            confidence = pattern_analysis.get('pattern_confidence', 0.0)
            
            if best_pattern == 'random' or confidence < 0.4:
                return "Aucun pattern numérique significatif détecté. Les valeurs semblent aléatoires ou sans corrélation claire."
            
            if best_pattern == 'arithmetic':
                diff = pattern_analysis.get('pattern_parameters', {}).get('common_difference', 0)
                return f"Pattern de progression arithmétique détecté avec une différence commune d'environ {diff:.2f}. Chaque valeur tend à augmenter/diminuer de cette quantité par rapport à la précédente."
            
            if best_pattern == 'geometric':
                ratio = pattern_analysis.get('pattern_parameters', {}).get('common_ratio', 0)
                return f"Pattern de progression géométrique détecté avec un ratio commun d'environ {ratio:.2f}. Chaque valeur tend à être multipliée par ce facteur par rapport à la précédente."
            
            if best_pattern == 'fibonacci':
                return "Pattern de type Fibonacci détecté. Chaque valeur tend à être la somme des deux valeurs précédentes."
            
            if best_pattern == 'repeating':
                length = pattern_analysis.get('pattern_parameters', {}).get('pattern_length', 0)
                return f"Pattern répétitif détecté avec une longueur de cycle d'environ {length} éléments. La séquence tend à se répéter à cette fréquence."
        
        elif pattern_type == 'sequence':
            # Explication pour les séquences d'événements
            instances = pattern_analysis.get('detected_instances', [])
            significance = pattern_analysis.get('statistical_significance', 0.0)
            
            if not instances or significance < 0.3:
                return "Aucune correspondance significative n'a été trouvée entre cette séquence et les données historiques."
            
            if significance > 0.7:
                return f"Pattern de séquence très significatif détecté avec {len(instances)} instances similaires dans les données historiques. Cette séquence a une forte tendance à se reproduire."
            else:
                return f"Pattern de séquence modérément significatif détecté avec {len(instances)} instances similaires. Il existe une certaine tendance de cette séquence à se reproduire, mais avec des variations."
        
        elif pattern_type == 'correlation':
            # Explication pour les corrélations
            correlation = pattern_analysis.get('correlation', 0.0)
            
            if correlation > 0.8:
                return "Forte corrélation détectée entre les deux séries d'événements. Ils tendent à évoluer ensemble de manière très significative."
            elif correlation > 0.5:
                return "Corrélation modérée détectée entre les deux séries d'événements. Il existe une tendance à évoluer dans la même direction, mais avec des variations."
            elif correlation > 0.0:
                return "Faible corrélation positive détectée. Il peut y avoir une légère tendance commune, mais elle n'est pas statistiquement très significative."
            elif correlation > -0.5:
                return "Faible corrélation négative détectée. Les séries tendent légèrement à évoluer en sens opposé."
            else:
                return "Forte corrélation négative détectée. Les séries tendent clairement à évoluer en sens opposé."
        
        return "Analyse de pattern réalisée, mais aucune explication spécifique n'est disponible pour ce type."
    
    def _classify_coincidence_level(self, coincidence_factor):
        """Classifier le niveau de coïncidence."""
        if coincidence_factor > 0.8:
            return "exceptionnelle"
        elif coincidence_factor > 0.65:
            return "forte"
        elif coincidence_factor > 0.5:
            return "modérée"
        elif coincidence_factor > 0.3:
            return "faible"
        else:
            return "négligeable"
    
    def _calculate_predictive_value(self, pattern_analysis):
        """Calculer la valeur prédictive d'un pattern."""
        # Combiner la signification statistique, le facteur de coïncidence et la répétabilité
        significance = pattern_analysis.get('statistical_significance', 0.0)
        coincidence = pattern_analysis.get('coincidence_factor', 0.0)
        repeatability = pattern_analysis.get('repeatability', 0.0)
        
        predictive_value = (significance * 0.4) + (coincidence * 0.4) + (repeatability * 0.2)
        
        # Classifier la valeur prédictive
        if predictive_value > 0.8:
            return {
                'value': predictive_value,
                'category': 'très_élevée',
                'confidence': 'haute',
                'description': "Ce pattern a une très forte valeur prédictive et peut être considéré comme un indicateur fiable."
            }
        elif predictive_value > 0.6:
            return {
                'value': predictive_value,
                'category': 'élevée',
                'confidence': 'moyenne-haute',
                'description': "Ce pattern a une bonne valeur prédictive et constitue un indicateur significatif."
            }
        elif predictive_value > 0.4:
            return {
                'value': predictive_value,
                'category': 'modérée',
                'confidence': 'moyenne',
                'description': "Ce pattern a une valeur prédictive modérée et peut être considéré comme un indicateur complémentaire."
            }
        elif predictive_value > 0.2:
            return {
                'value': predictive_value,
                'category': 'faible',
                'confidence': 'basse',
                'description': "Ce pattern a une faible valeur prédictive et devrait être considéré avec prudence."
            }
        else:
            return {
                'value': predictive_value,
                'category': 'très_faible',
                'confidence': 'très_basse',
                'description': "Ce pattern a une valeur prédictive négligeable et ne devrait pas être utilisé pour des prédictions."
            }
    
    def _generate_cycle_prediction(self, target_data, cycle_period, confidence, season):
        """Générer une prédiction basée sur un cycle détecté."""
        # Extraire les informations pertinentes
        team_name = target_data.get('name', '')
        historical_data = target_data.get('historical_data', {})
        
        if not historical_data:
            return None
        
        # Extraire l'année de la saison
        try:
            season_year = int(season.split('-')[0])
        except (IndexError, ValueError):
            current_year = datetime.now().year
            season_year = current_year
        
        # Rechercher les périodes similaires dans le cycle
        similar_years = []
        
        # Vérifier les années qui sont à n*period dans le passé
        for year_offset in range(1, 5):  # Vérifier jusqu'à 5 cycles en arrière
            similar_year = season_year - (cycle_period * year_offset)
            similar_year_str = str(similar_year)
            
            if similar_year_str in historical_data or f"{similar_year}-{similar_year+1}" in historical_data:
                similar_years.append(similar_year)
        
        if not similar_years:
            return None
        
        # Analyser les performances dans les années similaires
        performances = []
        
        for year in similar_years:
            year_str = str(year)
            year_range = f"{year}-{year+1}"
            
            # Chercher les données pour cette année
            year_data = historical_data.get(year_str, historical_data.get(year_range, None))
            
            if year_data:
                # Extraire la performance
                if 'league_position' in year_data:
                    performances.append({
                        'year': year,
                        'performance': year_data['league_position'],
                        'type': 'position'
                    })
                elif 'points' in year_data:
                    performances.append({
                        'year': year,
                        'performance': year_data['points'],
                        'type': 'points'
                    })
        
        if not performances:
            return None
        
        # Calculer la prédiction basée sur les performances passées
        if performances[0]['type'] == 'position':
            # Pour les positions, calculer la médiane (plus robuste que la moyenne)
            positions = sorted([p['performance'] for p in performances])
            median_position = positions[len(positions) // 2]
            
            prediction = {
                'based_on_cycle': cycle_period,
                'confidence': confidence,
                'prediction_type': 'league_position',
                'predicted_value': median_position,
                'historical_basis': similar_years,
                'description': f"Basé sur un cycle de {cycle_period} ans, {team_name} devrait finir aux environs de la {median_position}e place"
            }
        else:
            # Pour les points, calculer la moyenne
            points = [p['performance'] for p in performances]
            avg_points = sum(points) / len(points)
            
            prediction = {
                'based_on_cycle': cycle_period,
                'confidence': confidence,
                'prediction_type': 'points',
                'predicted_value': round(avg_points),
                'historical_basis': similar_years,
                'description': f"Basé sur un cycle de {cycle_period} ans, {team_name} devrait marquer environ {round(avg_points)} points"
            }
        
        return prediction
    
    def _generate_parallel_prediction(self, target_data, parallel_entity, similarity, season):
        """Générer une prédiction basée sur un parallèle historique."""
        # Extraire les informations de base
        team_name = target_data.get('name', '')
        
        # Simuler une recherche dans la base de données historique
        parallel_data = None
        for hist_entity in self._load_historical_database('team'):
            if hist_entity['name'] == parallel_entity:
                parallel_data = hist_entity
                break
        
        if not parallel_data:
            return None
        
        # Extraire les réalisations associées au parallèle
        achievements = parallel_data.get('achievements', [])
        
        if not achievements:
            return None
        
        # Déterminer la plus importante réalisation
        key_achievement = achievements[0]  # Par simplicité, prendre la première
        
        # Adapter l'année de la réalisation au contexte actuel
        try:
            season_year = int(season.split('-')[0])
            achievement_year = None
            
            for ach in achievements:
                # Chercher une année dans la réalisation
                for year in range(1900, 2100):
                    if str(year) in ach:
                        achievement_year = year
                        key_achievement = ach
                        break
                
                if achievement_year:
                    break
            
            # Si aucune année trouvée, utiliser le premier achievement
            if not achievement_year:
                key_achievement = achievements[0]
        except (IndexError, ValueError):
            key_achievement = achievements[0]
        
        # Créer la prédiction
        prediction = {
            'based_on_parallel': parallel_entity,
            'similarity': similarity,
            'prediction_type': 'achievement',
            'predicted_achievement': self._adapt_achievement_to_current_context(key_achievement, season),
            'historical_achievement': key_achievement,
            'description': f"Basé sur la similarité avec {parallel_entity}, {team_name} pourrait réaliser: {self._adapt_achievement_to_current_context(key_achievement, season)}"
        }
        
        return prediction
    
    def _adapt_achievement_to_current_context(self, achievement, season):
        """Adapter une réalisation historique au contexte actuel."""
        # Extraire l'année de la saison
        try:
            season_year = int(season.split('-')[0])
        except (IndexError, ValueError):
            season_year = datetime.now().year
        
        # Remplacer les années dans la réalisation par l'année actuelle
        adapted = achievement
        for year in range(1900, 2100):
            if str(year) in achievement:
                adapted = adapted.replace(str(year), str(season_year))
        
        return adapted
    
    def _combine_cycle_predictions(self, cycle_predictions, parallel_predictions):
        """Combiner plusieurs prédictions en une prédiction consolidée."""
        if not cycle_predictions and not parallel_predictions:
            return {
                'summary': "Prédiction impossible en raison d'un manque de données cycliques et historiques",
                'confidence': 0.0
            }
        
        # Prioriser les prédictions cycliques
        if cycle_predictions:
            # Trier par confiance
            sorted_cycle_predictions = sorted(cycle_predictions, key=lambda x: x['confidence'], reverse=True)
            best_cycle_prediction = sorted_cycle_predictions[0]
            
            # Extraire le type et la valeur
            prediction_type = best_cycle_prediction['prediction_type']
            predicted_value = best_cycle_prediction['predicted_value']
            
            # Fusionner avec d'autres prédictions cycliques du même type
            matching_predictions = [p for p in cycle_predictions if p['prediction_type'] == prediction_type]
            
            if len(matching_predictions) > 1:
                # Calcul pondéré par la confiance
                weighted_sum = sum(p['predicted_value'] * p['confidence'] for p in matching_predictions)
                total_confidence = sum(p['confidence'] for p in matching_predictions)
                
                predicted_value = weighted_sum / total_confidence if total_confidence > 0 else predicted_value
            
            combined = {
                'prediction_type': prediction_type,
                'predicted_value': predicted_value if prediction_type != 'league_position' else round(predicted_value),
                'confidence': best_cycle_prediction['confidence'],
                'primary_basis': 'cycle',
                'cycle_period': best_cycle_prediction['based_on_cycle'],
                'summary': best_cycle_prediction['description']
            }
        else:
            # Utiliser les prédictions basées sur parallèles historiques
            sorted_parallel_predictions = sorted(parallel_predictions, key=lambda x: x['similarity'], reverse=True)
            best_parallel_prediction = sorted_parallel_predictions[0]
            
            combined = {
                'prediction_type': 'achievement',
                'predicted_achievement': best_parallel_prediction['predicted_achievement'],
                'confidence': best_parallel_prediction['similarity'],
                'primary_basis': 'historical_parallel',
                'parallel_entity': best_parallel_prediction['based_on_parallel'],
                'summary': best_parallel_prediction['description']
            }
        
        # Si nous avons les deux types, enrichir la prédiction
        if cycle_predictions and parallel_predictions:
            best_parallel = sorted(parallel_predictions, key=lambda x: x['similarity'], reverse=True)[0]
            combined['historical_insight'] = best_parallel['predicted_achievement']
            combined['supporting_parallel'] = best_parallel['based_on_parallel']
            combined['summary'] += f" et pourrait {best_parallel['predicted_achievement']} comme {best_parallel['based_on_parallel']}"
        
        return combined
    
    def _calculate_prediction_confidence(self, cycle_predictions, parallel_predictions):
        """Calculer la confiance globale dans la prédiction combinée."""
        cycle_confidence = max([p['confidence'] for p in cycle_predictions]) if cycle_predictions else 0.0
        parallel_confidence = max([p['similarity'] for p in parallel_predictions]) if parallel_predictions else 0.0
        
        # Si nous avons les deux types, combiner avec une légère priorité aux cycles
        if cycle_confidence > 0 and parallel_confidence > 0:
            return (cycle_confidence * 0.6) + (parallel_confidence * 0.4)
        
        # Sinon, utiliser la confiance disponible
        return cycle_confidence or parallel_confidence