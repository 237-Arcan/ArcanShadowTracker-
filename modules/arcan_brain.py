"""
ArcanBrain - Neural intelligence layer for ArcanShadow prediction system.
Provides advanced machine learning analysis and pattern recognition capabilities.
"""

import numpy as np
import random
import time
from datetime import datetime, timedelta
import json
import os
import sqlite3
import math
import hashlib
from collections import deque

class ArcanBrain:
    """
    ArcanBrain - Neural intelligence core of the ArcanShadow system.
    Processes complex patterns and relationships using machine learning techniques.
    """
    
    def __init__(self, meta_systems=None):
        """
        Initialize the ArcanBrain module with references to other system components.
        
        Args:
            meta_systems: Reference to the MetaSystems module for integration
        """
        # Store module references
        self.meta_systems = meta_systems
        
        # Initialize the neural layers
        self.neural_layers = {
            'TemporalNet': self._temporal_net,
            'PatternMatrix': self._pattern_matrix,
            'ChaosFilter': self._chaos_filter,
            'SymbolicEncoder': self._symbolic_encoder,
            'AnomalyDetector': self._anomaly_detector,
            'SymmetryRecognizer': self._symmetry_recognizer
        }
        
        # Initialize memory systems
        self.short_term_memory = deque(maxlen=100)  # Recent matches and predictions
        self.long_term_memory = {}  # Persistent pattern storage
        self.associative_memory = {}  # Related concepts and patterns
        
        # Load trained models and weights if available
        self._load_neural_weights()
        
        # Learning parameters
        self.learning_rate = 0.03
        self.pattern_threshold = 0.65
        self.anomaly_threshold = 0.85
        self.insight_temperature = 0.7  # Controls randomness in pattern exploration
        
        # Neural activation trackers
        self.activation_history = []
        self.synapse_strength = {}
        
        # System state
        self.state = {
            'last_training': None,
            'total_patterns_recognized': 0,
            'confidence_calibration': 1.0,
            'insight_level': 0.0,
            'activation_level': 0.0
        }
        
        # Register event handlers if MetaSystems is available
        if self.meta_systems:
            self._register_event_handlers()
    
    def analyze_match(self, match_data, arcan_x_results=None, shadow_odds_results=None):
        """
        Perform neural analysis on match data and module outputs.
        
        Args:
            match_data (dict): Match information
            arcan_x_results (dict, optional): Results from ArcanX module
            shadow_odds_results (dict, optional): Results from ShadowOdds module
            
        Returns:
            dict: Neural analysis results with pattern recognition
        """
        analysis_id = self._generate_analysis_id(match_data)
        
        # Initialize the result structure
        result = {
            'analysis_id': analysis_id,
            'neural_confidence': 0.0,
            'pattern_recognition': [],
            'anomalies': [],
            'insight_connections': [],
            'prediction_delta': 0.0,
            'timestamp': datetime.now().isoformat()
        }
        
        # Apply each neural layer for progressive analysis
        temporal_patterns = self._temporal_net(match_data)
        pattern_matrices = self._pattern_matrix(match_data, temporal_patterns)
        filtered_patterns = self._chaos_filter(pattern_matrices)
        encoded_symbols = self._symbolic_encoder(filtered_patterns, arcan_x_results)
        anomalies = self._anomaly_detector(match_data, encoded_symbols, shadow_odds_results)
        symmetries = self._symmetry_recognizer(encoded_symbols, anomalies)
        
        # Process the neural outputs
        for pattern in filtered_patterns:
            if pattern['confidence'] > self.pattern_threshold:
                result['pattern_recognition'].append(pattern)
        
        for anomaly in anomalies:
            if anomaly['score'] > self.anomaly_threshold:
                result['anomalies'].append(anomaly)
        
        # Generate insight connections - relationships between detected patterns
        if len(result['pattern_recognition']) >= 2:
            insights = self._generate_insights(result['pattern_recognition'])
            result['insight_connections'] = insights
        
        # Calculate neural confidence based on pattern strength and coherence
        if result['pattern_recognition']:
            pattern_confidence = sum(p['confidence'] for p in result['pattern_recognition']) / len(result['pattern_recognition'])
            coherence = self._calculate_pattern_coherence(result['pattern_recognition'])
            anomaly_penalty = sum(a['score'] for a in result['anomalies']) * 0.1 if result['anomalies'] else 0
            
            # Final neural confidence calculation
            result['neural_confidence'] = (pattern_confidence * 0.6 + coherence * 0.4) * (1 - anomaly_penalty)
            result['neural_confidence'] = max(0, min(1, result['neural_confidence']))
        
        # Store in short-term memory
        self.short_term_memory.append({
            'match_data': match_data,
            'analysis_result': result,
            'timestamp': datetime.now().isoformat()
        })
        
        # Update neural state
        self.state['activation_level'] = result['neural_confidence']
        
        # Calculate Delta for prediction refinement (difference from other module predictions)
        if arcan_x_results and 'confidence' in arcan_x_results:
            arcan_delta = result['neural_confidence'] - arcan_x_results['confidence']
            result['prediction_delta'] = arcan_delta * 0.15  # Scale factor for adjustment
        
        # Trigger events based on analysis results if MetaSystems is available
        if self.meta_systems:
            # Trigger pattern event if significant patterns were recognized
            significant_patterns = [p for p in result['pattern_recognition'] 
                                   if p.get('confidence', 0) > self.pattern_threshold]
            if significant_patterns:
                self.meta_systems.trigger_event('significant_pattern_detected', {
                    'source': 'ArcanBrain',
                    'match_id': match_data.get('id', analysis_id),
                    'patterns': significant_patterns,
                    'neural_confidence': result['neural_confidence']
                })
            
            # Trigger anomaly event if significant anomalies were detected
            significant_anomalies = [a for a in result['anomalies'] 
                                    if a.get('score', 0) > self.anomaly_threshold]
            if significant_anomalies:
                self.meta_systems.trigger_event('significant_anomaly_detected', {
                    'source': 'ArcanBrain',
                    'match_id': match_data.get('id', analysis_id),
                    'anomalies': significant_anomalies,
                    'neural_confidence': result['neural_confidence']
                })
        
        return result
    
    def train_on_result(self, match_data, prediction, actual_result):
        """
        Train the neural system based on prediction outcomes.
        
        Args:
            match_data (dict): The match data that was analyzed
            prediction (dict): The prediction that was made
            actual_result (dict): The actual outcome of the match
            
        Returns:
            dict: Training report
        """
        # Check if prediction was correct
        was_correct = self._is_prediction_correct(prediction, actual_result)
        
        # Extract patterns that were identified
        patterns = prediction.get('pattern_recognition', [])
        
        report = {
            'patterns_updated': 0,
            'learning_applied': 0.0,
            'new_connections': 0,
            'insight_development': 0.0
        }
        
        if patterns:
            # Update pattern confidence based on outcome
            for pattern in patterns:
                pattern_id = pattern.get('id', '')
                if pattern_id in self.long_term_memory:
                    # Update existing pattern
                    stored_pattern = self.long_term_memory[pattern_id]
                    
                    if was_correct:
                        # Strengthen pattern confidence
                        new_confidence = stored_pattern['confidence'] + self.learning_rate * (1 - stored_pattern['confidence'])
                        stored_pattern['correct_count'] = stored_pattern.get('correct_count', 0) + 1
                    else:
                        # Weaken pattern confidence
                        new_confidence = stored_pattern['confidence'] - self.learning_rate * stored_pattern['confidence']
                        stored_pattern['incorrect_count'] = stored_pattern.get('incorrect_count', 0) + 1
                    
                    stored_pattern['confidence'] = max(0.1, min(0.95, new_confidence))
                    stored_pattern['last_updated'] = datetime.now().isoformat()
                    report['patterns_updated'] += 1
                else:
                    # Store new pattern
                    self.long_term_memory[pattern_id] = {
                        'id': pattern_id,
                        'type': pattern.get('type', 'unknown'),
                        'features': pattern.get('features', {}),
                        'confidence': 0.6 if was_correct else 0.4,
                        'correct_count': 1 if was_correct else 0,
                        'incorrect_count': 0 if was_correct else 1,
                        'first_seen': datetime.now().isoformat(),
                        'last_updated': datetime.now().isoformat()
                    }
                    report['patterns_updated'] += 1
        
        # Create associative connections between patterns
        if len(patterns) > 1:
            for i in range(len(patterns)):
                for j in range(i+1, len(patterns)):
                    connection_id = f"{patterns[i].get('id', '')}_{patterns[j].get('id', '')}"
                    
                    if connection_id not in self.associative_memory:
                        self.associative_memory[connection_id] = {
                            'patterns': [patterns[i].get('id', ''), patterns[j].get('id', '')],
                            'strength': 0.5,
                            'co_occurrence': 1,
                            'correct_together': 1 if was_correct else 0,
                            'first_seen': datetime.now().isoformat()
                        }
                        report['new_connections'] += 1
                    else:
                        # Strengthen existing connection
                        connection = self.associative_memory[connection_id]
                        connection['co_occurrence'] += 1
                        if was_correct:
                            connection['correct_together'] += 1
                        
                        # Update connection strength
                        success_rate = connection['correct_together'] / connection['co_occurrence']
                        connection['strength'] = 0.5 + (success_rate - 0.5) * min(1.0, connection['co_occurrence'] / 10)
        
        # Update insight level based on learning
        insight_gain = self.learning_rate * (1 if was_correct else 0.2)
        self.state['insight_level'] = min(1.0, self.state['insight_level'] + insight_gain)
        report['insight_development'] = insight_gain
        
        # Update system state
        self.state['last_training'] = datetime.now().isoformat()
        self.state['total_patterns_recognized'] += report['patterns_updated']
        
        # Save neural state periodically (after every 10 training iterations)
        if self.state['total_patterns_recognized'] % 10 == 0:
            self._save_neural_state()
        
        # Notify MetaSystems of learning results if available
        if self.meta_systems and report['adjustment_magnitude'] > 0.01:
            self.meta_systems.trigger_event('neural_learning_complete', {
                'source': 'ArcanBrain',
                'match_id': match_data.get('id', ''),
                'was_correct': was_correct,
                'learning_details': {
                    'new_patterns': report['new_patterns'],
                    'strengthened_patterns': report['strengthened_patterns'],
                    'new_connections': report['new_connections'],
                    'adjustment_magnitude': report['adjustment_magnitude']
                },
                'current_state': {
                    'learning_rate': self.learning_rate,
                    'pattern_threshold': self.pattern_threshold,
                    'confidence_calibration': self.state['confidence_calibration']
                }
            })
        
        return report
    
    def detect_emerging_insight(self, match_data=None):
        """
        Detect emerging insights from accumulated patterns and learning.
        
        Args:
            match_data (dict, optional): Current match context for insight relevance
            
        Returns:
            dict: Emerging insights and recommendations
        """
        insights = []
        
        # Only generate insights if we have sufficient pattern recognition
        if len(self.long_term_memory) < 10:
            return {
                'status': 'insufficient_data',
                'insights': [],
                'confidence': 0.0
            }
        
        # Look for high-confidence patterns that have consistent outcomes
        strong_patterns = []
        for pattern_id, pattern in self.long_term_memory.items():
            total_occurrences = pattern.get('correct_count', 0) + pattern.get('incorrect_count', 0)
            
            if total_occurrences >= 5 and pattern.get('confidence', 0) > 0.75:
                accuracy = pattern.get('correct_count', 0) / total_occurrences
                if accuracy > 0.7:
                    strong_patterns.append({
                        'id': pattern_id,
                        'type': pattern.get('type', ''),
                        'confidence': pattern.get('confidence', 0),
                        'accuracy': accuracy,
                        'occurrences': total_occurrences
                    })
        
        # Look for strong associative connections
        strong_connections = []
        for connection_id, connection in self.associative_memory.items():
            if connection.get('co_occurrence', 0) >= 3 and connection.get('strength', 0) > 0.7:
                strong_connections.append({
                    'id': connection_id,
                    'patterns': connection.get('patterns', []),
                    'strength': connection.get('strength', 0),
                    'co_occurrences': connection.get('co_occurrence', 0)
                })
        
        # Generate specific insights from patterns
        if strong_patterns:
            # Group patterns by type
            pattern_types = {}
            for pattern in strong_patterns:
                pattern_type = pattern.get('type', 'unknown')
                if pattern_type not in pattern_types:
                    pattern_types[pattern_type] = []
                pattern_types[pattern_type].append(pattern)
            
            # Generate insights for each pattern type
            for pattern_type, patterns in pattern_types.items():
                if len(patterns) >= 2:
                    avg_confidence = sum(p.get('confidence', 0) for p in patterns) / len(patterns)
                    avg_accuracy = sum(p.get('accuracy', 0) for p in patterns) / len(patterns)
                    
                    insights.append({
                        'type': f"{pattern_type}_affinity",
                        'description': f"Strong predictive power for {pattern_type} patterns",
                        'confidence': avg_confidence,
                        'accuracy': avg_accuracy,
                        'pattern_ids': [p.get('id') for p in patterns]
                    })
        
        # Generate insights from connections
        if strong_connections:
            for connection in strong_connections:
                # Get the pattern types involved
                pattern_ids = connection.get('patterns', [])
                pattern_types = []
                
                for pattern_id in pattern_ids:
                    if pattern_id in self.long_term_memory:
                        pattern_types.append(self.long_term_memory[pattern_id].get('type', 'unknown'))
                
                if len(pattern_types) >= 2:
                    insights.append({
                        'type': 'pattern_synergy',
                        'description': f"Synergy between {pattern_types[0]} and {pattern_types[1]} patterns",
                        'confidence': connection.get('strength', 0),
                        'co_occurrences': connection.get('co_occurrence', 0),
                        'pattern_ids': pattern_ids
                    })
        
        # Filter insights for relevance if match_data is provided
        if match_data and insights:
            match_features = self._extract_match_features(match_data)
            filtered_insights = []
            
            for insight in insights:
                relevance = self._calculate_insight_relevance(insight, match_features)
                if relevance > 0.6:
                    insight['relevance'] = relevance
                    filtered_insights.append(insight)
            
            insights = filtered_insights
        
        # Sort insights by confidence
        insights.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        # Calculate overall insight confidence
        insight_confidence = sum(insight.get('confidence', 0) for insight in insights) / len(insights) if insights else 0
        
        return {
            'status': 'insights_generated',
            'insights': insights,
            'confidence': insight_confidence,
            'patterns_analyzed': len(self.long_term_memory),
            'connections_analyzed': len(self.associative_memory)
        }
    
    def visualize_neural_state(self):
        """
        Generate a visualization of the current neural network state.
        
        Returns:
            dict: Visualization data for the neural system
        """
        # Generate node data for patterns
        nodes = []
        for pattern_id, pattern in self.long_term_memory.items():
            # Only include stronger patterns for clarity
            if pattern.get('confidence', 0) > 0.6:
                total_uses = pattern.get('correct_count', 0) + pattern.get('incorrect_count', 0)
                nodes.append({
                    'id': pattern_id,
                    'type': pattern.get('type', 'unknown'),
                    'size': min(100, 20 + total_uses * 5),  # Scale node size by usage
                    'confidence': pattern.get('confidence', 0),
                    'accuracy': pattern.get('correct_count', 0) / total_uses if total_uses > 0 else 0
                })
        
        # Generate edge data for connections
        edges = []
        for connection_id, connection in self.associative_memory.items():
            # Only include stronger connections for clarity
            if connection.get('strength', 0) > 0.6:
                edges.append({
                    'id': connection_id,
                    'source': connection.get('patterns', ['', ''])[0],
                    'target': connection.get('patterns', ['', ''])[1],
                    'weight': connection.get('strength', 0),
                    'width': 1 + connection.get('co_occurrence', 0) * 0.5
                })
        
        # Generate cluster data for pattern types
        clusters = {}
        for node in nodes:
            node_type = node.get('type', 'unknown')
            if node_type not in clusters:
                clusters[node_type] = []
            clusters[node_type].append(node.get('id', ''))
        
        return {
            'nodes': nodes,
            'edges': edges,
            'clusters': clusters,
            'neural_state': {
                'patterns': len(self.long_term_memory),
                'connections': len(self.associative_memory),
                'insight_level': self.state.get('insight_level', 0),
                'activation_level': self.state.get('activation_level', 0),
                'last_training': self.state.get('last_training')
            }
        }
    
    def predict_advanced_structures(self, match_data):
        """
        Generate advanced predictions about complex structures in the match.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Advanced structural predictions
        """
        result = {
            'narrative_structures': [],
            'cyclical_patterns': [],
            'paradoxical_elements': [],
            'symbolic_resonance': []
        }
        
        # Skip if insufficient pattern data
        if len(self.long_term_memory) < 15:
            return {
                'status': 'insufficient_pattern_data',
                'message': 'Need more pattern recognition training'
            }
        
        # Generate match features
        features = self._extract_match_features(match_data)
        
        # Analyze for narrative structures (storylines in the match)
        narratives = self._detect_narratives(features)
        if narratives:
            result['narrative_structures'] = narratives
        
        # Detect cyclical patterns
        cycles = self._detect_cycles(features, match_data)
        if cycles:
            result['cyclical_patterns'] = cycles
        
        # Find paradoxical elements (contradictions that may resolve)
        paradoxes = self._detect_paradoxes(features, match_data)
        if paradoxes:
            result['paradoxical_elements'] = paradoxes
        
        # Analyze symbolic resonance (deep mythic/archetypal patterns)
        symbols = self._detect_symbolic_resonance(features, match_data)
        if symbols:
            result['symbolic_resonance'] = symbols
        
        # Calculate prediction confidence based on pattern support
        confident_predictions = 0
        total_predictions = 0
        
        # Only analyze list categories for confidence calculation
        for key, category in result.items():
            if isinstance(category, list):
                for prediction in category:
                    total_predictions += 1
                    if prediction.get('confidence', 0) > 0.7:
                        confident_predictions += 1
        
        # Calculate confidence as a float value
        confidence = confident_predictions / total_predictions if total_predictions > 0 else 0
        
        # Add meta-information to results outside the category lists
        result_meta = {
            'confidence': confidence,
            'total_predictions': total_predictions,
            'confident_predictions': confident_predictions
        }
        
        # Combine into final result
        final_result = {**result, **result_meta}
        
        return final_result
    
    def run_counterfactual_analysis(self, match_data, scenario_changes):
        """
        Run a counterfactual analysis by changing specific match factors.
        
        Args:
            match_data (dict): Original match information
            scenario_changes (dict): Changes to apply to the scenario
            
        Returns:
            dict: Counterfactual analysis results
        """
        # Create a modified match data
        modified_match = match_data.copy()
        
        # Apply scenario changes
        for key, value in scenario_changes.items():
            if isinstance(value, dict) and key in modified_match and isinstance(modified_match[key], dict):
                # Update nested dictionary
                modified_match[key].update(value)
            else:
                # Set or replace value
                modified_match[key] = value
        
        # Run neural analysis on the modified scenario
        counterfactual_result = self.analyze_match(modified_match)
        
        # Calculate differences between original and counterfactual
        differences = {
            'neural_confidence_delta': counterfactual_result.get('neural_confidence', 0) - 0.5,  # Assuming baseline of 0.5
            'pattern_changes': [],
            'new_anomalies': [],
            'changed_insights': []
        }
        
        # Log the scenario that was tested
        result = {
            'scenario_description': self._generate_scenario_description(scenario_changes),
            'modified_factors': list(scenario_changes.keys()),
            'counterfactual_confidence': counterfactual_result.get('neural_confidence', 0),
            'differences': differences,
            'conclusion': self._generate_counterfactual_conclusion(differences)
        }
        
        return result
    
    def _temporal_net(self, match_data):
        """TemporalNet layer - Analyzes time-based patterns."""
        patterns = []
        
        # Extract relevant temporal features
        match_date = match_data.get('date')
        if not match_date:
            match_date = datetime.now()
        elif isinstance(match_date, str):
            try:
                match_date = datetime.fromisoformat(match_date.replace('Z', '+00:00'))
            except:
                match_date = datetime.now()
        
        # Get day of week (0 = Monday, 6 = Sunday)
        day_of_week = match_date.weekday()
        
        # Extract time of day if available
        hour = match_date.hour if hasattr(match_date, 'hour') else 12
        
        # Get season information
        month = match_date.month
        season = 'winter' if month in [12, 1, 2] else 'spring' if month in [3, 4, 5] else 'summer' if month in [6, 7, 8] else 'fall'
        
        # Extract historical matchup data if available
        historical_matches = match_data.get('historical_matchups', [])
        
        # Analyze day of week patterns
        day_pattern = self._analyze_day_pattern(day_of_week, historical_matches)
        if day_pattern:
            patterns.append(day_pattern)
        
        # Analyze time of day patterns
        time_pattern = self._analyze_time_pattern(hour, historical_matches)
        if time_pattern:
            patterns.append(time_pattern)
        
        # Analyze seasonal patterns
        season_pattern = self._analyze_season_pattern(season, historical_matches)
        if season_pattern:
            patterns.append(season_pattern)
        
        # Analyze interval patterns between matches
        if len(historical_matches) >= 3:
            interval_pattern = self._analyze_interval_pattern(match_date, historical_matches)
            if interval_pattern:
                patterns.append(interval_pattern)
        
        # Analyze cyclical time patterns in match history
        if len(historical_matches) >= 5:
            cycle_pattern = self._analyze_cycle_pattern(match_date, historical_matches)
            if cycle_pattern:
                patterns.append(cycle_pattern)
        
        return patterns
    
    def _pattern_matrix(self, match_data, temporal_patterns):
        """PatternMatrix layer - Constructs multi-dimensional pattern matrices."""
        matrices = []
        
        # Extract team information
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # Create form matrices if available
        home_form = match_data.get('home_form', '')
        away_form = match_data.get('away_form', '')
        
        if home_form and away_form:
            form_matrix = self._construct_form_matrix(home_form, away_form)
            if form_matrix:
                matrices.append({
                    'id': f"form_matrix_{home_team}_{away_team}",
                    'type': 'form_matrix',
                    'dimensions': form_matrix.get('dimensions', []),
                    'patterns': form_matrix.get('patterns', []),
                    'confidence': form_matrix.get('confidence', 0.5)
                })
        
        # Create historic result matrices if available
        historical_matchups = match_data.get('historical_matchups', [])
        
        if len(historical_matchups) >= 3:
            result_matrix = self._construct_result_matrix(historical_matchups, home_team, away_team)
            if result_matrix:
                matrices.append({
                    'id': f"result_matrix_{home_team}_{away_team}",
                    'type': 'result_matrix',
                    'dimensions': result_matrix.get('dimensions', []),
                    'patterns': result_matrix.get('patterns', []),
                    'confidence': result_matrix.get('confidence', 0.5)
                })
        
        # Create score pattern matrices if available
        if len(historical_matchups) >= 4:
            score_matrix = self._construct_score_matrix(historical_matchups)
            if score_matrix:
                matrices.append({
                    'id': f"score_matrix_{home_team}_{away_team}",
                    'type': 'score_matrix',
                    'dimensions': score_matrix.get('dimensions', []),
                    'patterns': score_matrix.get('patterns', []),
                    'confidence': score_matrix.get('confidence', 0.5)
                })
        
        # Integrate temporal patterns into matrices
        if temporal_patterns:
            temporal_matrix = self._construct_temporal_matrix(temporal_patterns)
            if temporal_matrix:
                matrices.append({
                    'id': f"temporal_matrix_{home_team}_{away_team}",
                    'type': 'temporal_matrix',
                    'dimensions': temporal_matrix.get('dimensions', []),
                    'patterns': temporal_matrix.get('patterns', []),
                    'confidence': temporal_matrix.get('confidence', 0.5)
                })
        
        return matrices
    
    def _chaos_filter(self, pattern_matrices):
        """ChaosFilter layer - Filters out noise and enhances signal in pattern matrices."""
        filtered_patterns = []
        
        for matrix in pattern_matrices:
            matrix_patterns = matrix.get('patterns', [])
            matrix_confidence = matrix.get('confidence', 0.5)
            
            # Filter patterns by confidence
            strong_patterns = [p for p in matrix_patterns if p.get('confidence', 0) > 0.6]
            
            # Check for pattern coherence
            coherence = self._calculate_pattern_coherence(strong_patterns)
            
            if coherence > 0.5 and strong_patterns:
                # Generate a unique ID for this filtered pattern set
                pattern_hash = hashlib.md5(str(strong_patterns).encode()).hexdigest()[:8]
                pattern_type = matrix.get('type', 'unknown')
                
                filtered_patterns.append({
                    'id': f"{pattern_type}_filtered_{pattern_hash}",
                    'type': pattern_type,
                    'patterns': strong_patterns,
                    'coherence': coherence,
                    'confidence': matrix_confidence * coherence,
                    'features': {
                        'pattern_count': len(strong_patterns),
                        'dimension_count': len(matrix.get('dimensions', [])),
                        'average_strength': sum(p.get('confidence', 0) for p in strong_patterns) / len(strong_patterns) if strong_patterns else 0
                    }
                })
        
        return filtered_patterns
    
    def _symbolic_encoder(self, filtered_patterns, arcan_x_results=None):
        """SymbolicEncoder layer - Translates patterns into symbolic representations."""
        encoded_symbols = []
        
        # Get archetypal symbols from ArcanX if available
        archetypes = []
        if arcan_x_results and 'factors' in arcan_x_results:
            for factor in arcan_x_results['factors']:
                factor_name = factor.get('name', '')
                factor_value = factor.get('value', '')
                if 'tarot' in factor_name.lower() or 'archetype' in factor_name.lower():
                    archetypes.append({
                        'type': 'tarot',
                        'name': factor_name,
                        'value': factor_value
                    })
                elif 'element' in factor_name.lower():
                    archetypes.append({
                        'type': 'element',
                        'name': factor_name,
                        'value': factor_value
                    })
        
        # Process each filtered pattern
        for pattern in filtered_patterns:
            pattern_type = pattern.get('type', 'unknown')
            sub_patterns = pattern.get('patterns', [])
            
            # Generate symbolic representation based on pattern type
            if pattern_type == 'form_matrix':
                symbol = self._encode_form_pattern(pattern)
                if symbol:
                    encoded_symbols.append(symbol)
            
            elif pattern_type == 'result_matrix':
                symbol = self._encode_result_pattern(pattern)
                if symbol:
                    encoded_symbols.append(symbol)
            
            elif pattern_type == 'score_matrix':
                symbol = self._encode_score_pattern(pattern)
                if symbol:
                    encoded_symbols.append(symbol)
            
            elif pattern_type == 'temporal_matrix':
                symbol = self._encode_temporal_pattern(pattern)
                if symbol:
                    encoded_symbols.append(symbol)
        
        # Integrate with archetypes if available
        if archetypes and encoded_symbols:
            for i, symbol in enumerate(encoded_symbols):
                if i < len(archetypes):
                    symbol['archetype'] = archetypes[i].get('value', '')
                    symbol['resonance'] = 0.7  # Assumed resonance
        
        return encoded_symbols
    
    def _anomaly_detector(self, match_data, encoded_symbols, shadow_odds_results=None):
        """AnomalyDetector layer - Identifies anomalies and unusual patterns."""
        anomalies = []
        
        # Extract odds data if available
        odds_data = {}
        if shadow_odds_results and 'factors' in shadow_odds_results:
            for factor in shadow_odds_results['factors']:
                factor_name = factor.get('name', '')
                factor_value = factor.get('value', '')
                if 'odds' in factor_name.lower() or 'line' in factor_name.lower():
                    odds_data[factor_name] = factor_value
        
        # Check for form anomalies
        home_form = match_data.get('home_form', '')
        away_form = match_data.get('away_form', '')
        
        if home_form and away_form:
            form_anomaly = self._detect_form_anomaly(home_form, away_form)
            if form_anomaly:
                anomalies.append(form_anomaly)
        
        # Check for odds anomalies
        if odds_data:
            odds_anomaly = self._detect_odds_anomaly(odds_data, match_data)
            if odds_anomaly:
                anomalies.append(odds_anomaly)
        
        # Check for symbolic pattern anomalies
        if encoded_symbols:
            symbolic_anomaly = self._detect_symbolic_anomaly(encoded_symbols)
            if symbolic_anomaly:
                anomalies.append(symbolic_anomaly)
        
        # Check for historical anomalies
        historical_matchups = match_data.get('historical_matchups', [])
        if historical_matchups:
            historical_anomaly = self._detect_historical_anomaly(historical_matchups, match_data)
            if historical_anomaly:
                anomalies.append(historical_anomaly)
        
        return anomalies
    
    def _symmetry_recognizer(self, encoded_symbols, anomalies):
        """SymmetryRecognizer layer - Identifies symmetrical patterns across dimensions."""
        symmetries = []
        
        # Need at least two symbols to find symmetries
        if len(encoded_symbols) < 2:
            return symmetries
        
        # Check for pairs of symbols that might form symmetries
        for i in range(len(encoded_symbols)):
            for j in range(i+1, len(encoded_symbols)):
                symbol1 = encoded_symbols[i]
                symbol2 = encoded_symbols[j]
                
                # Check for complementary symbols
                if symbol1.get('type') == symbol2.get('type'):
                    continue  # Skip same types
                
                # Check for pattern resonance
                resonance = self._calculate_symbol_resonance(symbol1, symbol2)
                
                if resonance > 0.7:
                    # Generate a unique ID for this symmetry
                    symmetry_id = f"{symbol1.get('id', '')}_{symbol2.get('id', '')}"
                    
                    symmetries.append({
                        'id': symmetry_id,
                        'type': 'symbolic_symmetry',
                        'symbols': [symbol1.get('id', ''), symbol2.get('id', '')],
                        'resonance': resonance,
                        'confidence': (symbol1.get('confidence', 0.5) + symbol2.get('confidence', 0.5)) / 2,
                        'description': f"Symmetry between {symbol1.get('type', '')} and {symbol2.get('type', '')}"
                    })
        
        # Check how anomalies might affect symmetries
        if anomalies and symmetries:
            for symmetry in symmetries:
                for anomaly in anomalies:
                    # Check if the anomaly affects the symbols in this symmetry
                    if any(symbol_id in anomaly.get('affected_elements', []) for symbol_id in symmetry.get('symbols', [])):
                        # Reduce confidence based on anomaly score
                        symmetry['confidence'] = max(0.1, symmetry['confidence'] - anomaly.get('score', 0) * 0.2)
                        symmetry['affected_by_anomaly'] = anomaly.get('id', '')
        
        return symmetries
    
    def _analyze_day_pattern(self, day_of_week, historical_matches):
        """Analyze patterns related to day of the week."""
        if not historical_matches:
            return None
        
        day_results = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Collect results by day of week
        for match in historical_matches:
            match_date = match.get('date')
            if not match_date:
                continue
            
            if isinstance(match_date, str):
                try:
                    match_date = datetime.fromisoformat(match_date.replace('Z', '+00:00'))
                except:
                    continue
            
            match_day = match_date.weekday()
            result = match.get('result', '')
            
            if result:
                day_results[match_day].append(result)
        
        # Check if we have enough data for the current day
        if day_of_week in day_results and len(day_results[day_of_week]) >= 3:
            # Calculate win percentage for current day
            wins = day_results[day_of_week].count('W')
            total = len(day_results[day_of_week])
            win_percentage = wins / total if total > 0 else 0
            
            # Compare to overall win percentage
            all_results = []
            for day_result in day_results.values():
                all_results.extend(day_result)
            
            overall_wins = all_results.count('W')
            overall_total = len(all_results)
            overall_win_percentage = overall_wins / overall_total if overall_total > 0 else 0
            
            # If there's a significant difference, return a pattern
            if abs(win_percentage - overall_win_percentage) > 0.2 and total >= 3:
                pattern_id = f"day_pattern_{day_names[day_of_week]}"
                
                return {
                    'id': pattern_id,
                    'type': 'day_of_week',
                    'day': day_of_week,
                    'day_name': day_names[day_of_week],
                    'win_percentage': win_percentage,
                    'overall_win_percentage': overall_win_percentage,
                    'difference': win_percentage - overall_win_percentage,
                    'sample_size': total,
                    'confidence': min(0.9, 0.5 + abs(win_percentage - overall_win_percentage))
                }
        
        return None
    
    def _analyze_time_pattern(self, hour, historical_matches):
        """Analyze patterns related to time of day."""
        if not historical_matches:
            return None
        
        # Group matches into time slots
        morning = []  # 6-12
        afternoon = []  # 12-18
        evening = []  # 18-24
        night = []  # 0-6
        
        # Collect results by time of day
        for match in historical_matches:
            match_date = match.get('date')
            if not match_date:
                continue
            
            if isinstance(match_date, str):
                try:
                    match_date = datetime.fromisoformat(match_date.replace('Z', '+00:00'))
                except:
                    continue
            
            match_hour = match_date.hour
            result = match.get('result', '')
            
            if result:
                if 6 <= match_hour < 12:
                    morning.append(result)
                elif 12 <= match_hour < 18:
                    afternoon.append(result)
                elif 18 <= match_hour < 24:
                    evening.append(result)
                else:
                    night.append(result)
        
        # Determine current time slot
        current_slot = None
        slot_results = None
        slot_name = ''
        
        if 6 <= hour < 12:
            current_slot = 'morning'
            slot_results = morning
            slot_name = 'Morning'
        elif 12 <= hour < 18:
            current_slot = 'afternoon'
            slot_results = afternoon
            slot_name = 'Afternoon'
        elif 18 <= hour < 24:
            current_slot = 'evening'
            slot_results = evening
            slot_name = 'Evening'
        else:
            current_slot = 'night'
            slot_results = night
            slot_name = 'Night'
        
        # Check if we have enough data for the current time slot
        if slot_results and len(slot_results) >= 3:
            # Calculate win percentage for current time slot
            wins = slot_results.count('W')
            total = len(slot_results)
            win_percentage = wins / total if total > 0 else 0
            
            # Compare to overall win percentage
            all_results = morning + afternoon + evening + night
            overall_wins = all_results.count('W')
            overall_total = len(all_results)
            overall_win_percentage = overall_wins / overall_total if overall_total > 0 else 0
            
            # If there's a significant difference, return a pattern
            if abs(win_percentage - overall_win_percentage) > 0.2 and total >= 3:
                pattern_id = f"time_pattern_{current_slot}"
                
                return {
                    'id': pattern_id,
                    'type': 'time_of_day',
                    'time_slot': current_slot,
                    'time_name': slot_name,
                    'win_percentage': win_percentage,
                    'overall_win_percentage': overall_win_percentage,
                    'difference': win_percentage - overall_win_percentage,
                    'sample_size': total,
                    'confidence': min(0.9, 0.5 + abs(win_percentage - overall_win_percentage))
                }
        
        return None
    
    def _analyze_season_pattern(self, season, historical_matches):
        """Analyze patterns related to seasons."""
        if not historical_matches:
            return None
        
        # Group matches by season
        winter_results = []
        spring_results = []
        summer_results = []
        fall_results = []
        
        # Collect results by season
        for match in historical_matches:
            match_date = match.get('date')
            if not match_date:
                continue
            
            if isinstance(match_date, str):
                try:
                    match_date = datetime.fromisoformat(match_date.replace('Z', '+00:00'))
                except:
                    continue
            
            match_month = match_date.month
            match_season = 'winter' if match_month in [12, 1, 2] else 'spring' if match_month in [3, 4, 5] else 'summer' if match_month in [6, 7, 8] else 'fall'
            result = match.get('result', '')
            
            if result:
                if match_season == 'winter':
                    winter_results.append(result)
                elif match_season == 'spring':
                    spring_results.append(result)
                elif match_season == 'summer':
                    summer_results.append(result)
                else:
                    fall_results.append(result)
        
        # Determine current season's results
        current_results = None
        if season == 'winter':
            current_results = winter_results
        elif season == 'spring':
            current_results = spring_results
        elif season == 'summer':
            current_results = summer_results
        else:
            current_results = fall_results
        
        # Check if we have enough data for the current season
        if current_results and len(current_results) >= 3:
            # Calculate win percentage for current season
            wins = current_results.count('W')
            total = len(current_results)
            win_percentage = wins / total if total > 0 else 0
            
            # Compare to overall win percentage
            all_results = winter_results + spring_results + summer_results + fall_results
            overall_wins = all_results.count('W')
            overall_total = len(all_results)
            overall_win_percentage = overall_wins / overall_total if overall_total > 0 else 0
            
            # If there's a significant difference, return a pattern
            if abs(win_percentage - overall_win_percentage) > 0.2 and total >= 3:
                pattern_id = f"season_pattern_{season}"
                
                return {
                    'id': pattern_id,
                    'type': 'season',
                    'season': season,
                    'win_percentage': win_percentage,
                    'overall_win_percentage': overall_win_percentage,
                    'difference': win_percentage - overall_win_percentage,
                    'sample_size': total,
                    'confidence': min(0.9, 0.5 + abs(win_percentage - overall_win_percentage))
                }
        
        return None
    
    def _analyze_interval_pattern(self, match_date, historical_matches):
        """Analyze patterns related to intervals between matches."""
        if not historical_matches or len(historical_matches) < 3:
            return None
        
        # Sort matches by date
        sorted_matches = sorted(historical_matches, key=lambda m: m.get('date', datetime.now()))
        
        # Calculate intervals in days
        intervals = []
        for i in range(1, len(sorted_matches)):
            prev_date = sorted_matches[i-1].get('date')
            curr_date = sorted_matches[i].get('date')
            
            if not prev_date or not curr_date:
                continue
            
            if isinstance(prev_date, str):
                try:
                    prev_date = datetime.fromisoformat(prev_date.replace('Z', '+00:00'))
                except:
                    continue
            
            if isinstance(curr_date, str):
                try:
                    curr_date = datetime.fromisoformat(curr_date.replace('Z', '+00:00'))
                except:
                    continue
            
            interval = (curr_date - prev_date).days
            if interval > 0:
                intervals.append(interval)
        
        if not intervals:
            return None
        
        # Find the average interval
        avg_interval = sum(intervals) / len(intervals)
        
        # Find the most recent match date
        most_recent_date = sorted_matches[-1].get('date')
        if isinstance(most_recent_date, str):
            try:
                most_recent_date = datetime.fromisoformat(most_recent_date.replace('Z', '+00:00'))
            except:
                return None
        
        # Calculate days since most recent match
        days_since_last = (match_date - most_recent_date).days if hasattr(match_date, 'days') else 0
        
        # Check if the current interval is close to the average
        interval_ratio = days_since_last / avg_interval if avg_interval > 0 else 0
        
        # Return pattern if we detect a meaningful interval relationship
        if 0.8 <= interval_ratio <= 1.2 and days_since_last > 0:
            pattern_id = f"interval_pattern_{days_since_last}"
            
            return {
                'id': pattern_id,
                'type': 'match_interval',
                'avg_interval': avg_interval,
                'current_interval': days_since_last,
                'interval_ratio': interval_ratio,
                'sample_size': len(intervals),
                'confidence': 0.6  # Moderate confidence
            }
        
        return None
    
    def _analyze_cycle_pattern(self, match_date, historical_matches):
        """Analyze cyclical patterns in match history."""
        if not historical_matches or len(historical_matches) < 5:
            return None
        
        # Sort matches by date
        sorted_matches = sorted(historical_matches, key=lambda m: m.get('date', datetime.now()))
        
        # Extract results as a sequence
        result_sequence = []
        for match in sorted_matches:
            result = match.get('result', '')
            if result in ['W', 'D', 'L']:
                result_sequence.append(result)
        
        if len(result_sequence) < 5:
            return None
        
        # Check for simple repeating patterns (length 2 to 4)
        for pattern_length in range(2, 5):
            if len(result_sequence) >= pattern_length * 2:
                # Check if the last <pattern_length> results repeat
                pattern = result_sequence[-pattern_length:]
                
                # Look for this pattern in earlier results
                occurrences = 0
                for i in range(0, len(result_sequence) - pattern_length, pattern_length):
                    if result_sequence[i:i+pattern_length] == pattern:
                        occurrences += 1
                
                # If pattern occurs multiple times, return it
                if occurrences >= 2:
                    pattern_str = ''.join(pattern)
                    pattern_id = f"cycle_pattern_{pattern_str}"
                    
                    return {
                        'id': pattern_id,
                        'type': 'result_cycle',
                        'pattern': pattern,
                        'pattern_str': pattern_str,
                        'pattern_length': pattern_length,
                        'occurrences': occurrences,
                        'confidence': min(0.9, 0.5 + (occurrences / 10))
                    }
        
        return None
    
    def _construct_form_matrix(self, home_form, away_form):
        """Construct a form matrix from team form strings."""
        if not home_form or not away_form:
            return None
        
        # Extract form as lists (most recent first)
        home_form_list = [result for result in home_form if result in ['W', 'D', 'L']]
        away_form_list = [result for result in away_form if result in ['W', 'D', 'L']]
        
        # Ensure we have enough data
        if len(home_form_list) < 3 or len(away_form_list) < 3:
            return None
        
        # Create form matrix (up to 5x5)
        max_form_length = min(5, len(home_form_list), len(away_form_list))
        
        # Build the matrix
        matrix = []
        for i in range(max_form_length):
            row = []
            for j in range(max_form_length):
                home_result = home_form_list[i] if i < len(home_form_list) else None
                away_result = away_form_list[j] if j < len(away_form_list) else None
                
                if home_result and away_result:
                    # Create a cell value based on the combination
                    if home_result == 'W' and away_result == 'W':
                        value = 1.0  # Both teams in winning form
                    elif home_result == 'L' and away_result == 'L':
                        value = -1.0  # Both teams in losing form
                    elif home_result == 'W' and away_result == 'L':
                        value = 0.5  # Home advantage
                    elif home_result == 'L' and away_result == 'W':
                        value = -0.5  # Away advantage
                    else:
                        value = 0.0  # Draw or mixed form
                    
                    row.append(value)
                else:
                    row.append(0.0)
            
            matrix.append(row)
        
        # Extract patterns from the matrix
        patterns = []
        
        # Check diagonal trend (most recent to least recent)
        diagonal_sum = sum(matrix[i][i] for i in range(min(len(matrix), len(matrix[0]))))
        diagonal_length = min(len(matrix), len(matrix[0]))
        diagonal_avg = diagonal_sum / diagonal_length if diagonal_length > 0 else 0
        
        if abs(diagonal_avg) > 0.3:
            direction = 'positive' if diagonal_avg > 0 else 'negative'
            patterns.append({
                'type': 'diagonal_trend',
                'direction': direction,
                'strength': abs(diagonal_avg),
                'confidence': 0.5 + abs(diagonal_avg) * 0.5
            })
        
        # Check row trends (home team form impact)
        for i, row in enumerate(matrix):
            row_sum = sum(row)
            row_avg = row_sum / len(row) if row else 0
            
            if abs(row_avg) > 0.4:
                direction = 'positive' if row_avg > 0 else 'negative'
                patterns.append({
                    'type': 'home_form_impact',
                    'row': i,
                    'direction': direction,
                    'strength': abs(row_avg),
                    'confidence': 0.5 + abs(row_avg) * 0.4
                })
        
        # Check column trends (away team form impact)
        for j in range(len(matrix[0]) if matrix else 0):
            col = [matrix[i][j] for i in range(len(matrix))]
            col_sum = sum(col)
            col_avg = col_sum / len(col) if col else 0
            
            if abs(col_avg) > 0.4:
                direction = 'positive' if col_avg > 0 else 'negative'
                patterns.append({
                    'type': 'away_form_impact',
                    'column': j,
                    'direction': direction,
                    'strength': abs(col_avg),
                    'confidence': 0.5 + abs(col_avg) * 0.4
                })
        
        # Calculate overall matrix confidence based on patterns
        confidence = sum(p.get('confidence', 0) for p in patterns) / len(patterns) if patterns else 0.5
        
        return {
            'dimensions': [max_form_length, max_form_length],
            'matrix': matrix,
            'patterns': patterns,
            'confidence': confidence
        }
    
    def _construct_result_matrix(self, historical_matchups, home_team, away_team):
        """Construct a matrix of historical results between teams."""
        if not historical_matchups or len(historical_matchups) < 3:
            return None
        
        # Filter matchups between these two teams
        team_matchups = []
        for match in historical_matchups:
            match_home = match.get('home_team', '')
            match_away = match.get('away_team', '')
            
            if (match_home == home_team and match_away == away_team) or \
               (match_home == away_team and match_away == home_team):
                team_matchups.append(match)
        
        if len(team_matchups) < 3:
            return None
        
        # Sort by date (oldest to newest)
        sorted_matchups = sorted(team_matchups, key=lambda m: m.get('date', datetime.now()))
        
        # Create a matrix of win/loss/draw with home/away
        matrix_size = min(5, len(sorted_matchups))
        
        # 2D matrix: [recency][venue]
        # recency: 0 = most recent, increasing = older
        # venue: 0 = current home team at home, 1 = current home team away
        matrix = []
        for i in range(matrix_size):
            match = sorted_matchups[-(i+1)] if i < len(sorted_matchups) else None
            
            if match:
                match_home = match.get('home_team', '')
                match_result = match.get('result', '')
                
                # Determine venue (from perspective of current home team)
                venue = 0 if match_home == home_team else 1
                
                # Determine result value (from perspective of current home team)
                if match_result == 'W':
                    result_value = 1.0 if match_home == home_team else -1.0
                elif match_result == 'L':
                    result_value = -1.0 if match_home == home_team else 1.0
                else:  # Draw
                    result_value = 0.0
                
                matrix.append([venue, result_value])
            else:
                matrix.append([0, 0.0])
        
        # Extract patterns
        patterns = []
        
        # Check for home advantage pattern
        home_results = [row[1] for row in matrix if row[0] == 0]
        away_results = [row[1] for row in matrix if row[0] == 1]
        
        if home_results and away_results:
            home_avg = sum(home_results) / len(home_results)
            away_avg = sum(away_results) / len(away_results)
            venue_diff = home_avg - away_avg
            
            if abs(venue_diff) > 0.5:
                advantage = 'home' if venue_diff > 0 else 'away'
                patterns.append({
                    'type': 'venue_advantage',
                    'advantage': advantage,
                    'strength': abs(venue_diff),
                    'confidence': 0.5 + abs(venue_diff) * 0.4
                })
        
        # Check for recency trend (most recent 3 matches)
        recent = matrix[:3] if len(matrix) >= 3 else matrix
        recent_results = [row[1] for row in recent]
        
        if recent_results:
            trend_direction = 0
            for i in range(1, len(recent_results)):
                if recent_results[i] > recent_results[i-1]:
                    trend_direction += 1
                elif recent_results[i] < recent_results[i-1]:
                    trend_direction -= 1
            
            if abs(trend_direction) == len(recent_results) - 1:  # Perfect trend
                direction = 'improving' if trend_direction > 0 else 'declining'
                patterns.append({
                    'type': 'recency_trend',
                    'direction': direction,
                    'strength': 1.0,
                    'confidence': 0.7
                })
        
        # Calculate overall confidence
        confidence = sum(p.get('confidence', 0) for p in patterns) / len(patterns) if patterns else 0.5
        
        return {
            'dimensions': [matrix_size, 2],
            'matrix': matrix,
            'patterns': patterns,
            'confidence': confidence
        }
    
    def _construct_score_matrix(self, historical_matchups):
        """Construct a matrix analyzing scoring patterns."""
        if not historical_matchups or len(historical_matchups) < 4:
            return None
        
        # Extract scoring information
        scores = []
        for match in historical_matchups:
            home_score = match.get('home_score')
            away_score = match.get('away_score')
            
            if home_score is not None and away_score is not None:
                scores.append([home_score, away_score])
        
        if len(scores) < 4:
            return None
        
        # Sort by date (oldest to newest)
        sorted_scores = scores[-5:] if len(scores) > 5 else scores  # Most recent 5
        
        # Create a scoring pattern matrix
        matrix = []
        for i, score in enumerate(sorted_scores):
            home_goals = score[0]
            away_goals = score[1]
            total_goals = home_goals + away_goals
            
            # Calculate goal values
            goal_diff = home_goals - away_goals
            goal_ratio = home_goals / max(1, away_goals)
            
            matrix.append([home_goals, away_goals, total_goals, goal_diff, goal_ratio])
        
        # Extract patterns
        patterns = []
        
        # Check for consistent total goals
        total_goals = [row[2] for row in matrix]
        avg_total = sum(total_goals) / len(total_goals)
        total_variance = sum((g - avg_total) ** 2 for g in total_goals) / len(total_goals)
        
        if total_variance < 1.5:  # Low variance indicates consistency
            goal_type = 'high_scoring' if avg_total > 2.5 else 'low_scoring'
            patterns.append({
                'type': 'total_goals_consistency',
                'goal_type': goal_type,
                'avg_total': avg_total,
                'variance': total_variance,
                'confidence': 0.5 + (1.0 / (1 + total_variance))
            })
        
        # Check for consistent goal difference
        goal_diffs = [row[3] for row in matrix]
        consistent_direction = all(g > 0 for g in goal_diffs) or all(g < 0 for g in goal_diffs)
        
        if consistent_direction:
            dominant_team = 'home' if goal_diffs[0] > 0 else 'away'
            patterns.append({
                'type': 'consistent_dominance',
                'dominant_team': dominant_team,
                'streak_length': len(goal_diffs),
                'confidence': 0.5 + min(0.4, len(goal_diffs) * 0.1)
            })
        
        # Check for repeating exact scores
        score_counts = {}
        for score in sorted_scores:
            score_key = f"{score[0]}-{score[1]}"
            if score_key not in score_counts:
                score_counts[score_key] = 0
            score_counts[score_key] += 1
        
        repeat_scores = [(score, count) for score, count in score_counts.items() if count > 1]
        if repeat_scores:
            for score, count in repeat_scores:
                patterns.append({
                    'type': 'repeating_score',
                    'score': score,
                    'occurrences': count,
                    'confidence': 0.5 + min(0.4, count * 0.1)
                })
        
        # Calculate overall confidence
        confidence = sum(p.get('confidence', 0) for p in patterns) / len(patterns) if patterns else 0.5
        
        return {
            'dimensions': [len(sorted_scores), 5],
            'matrix': matrix,
            'patterns': patterns,
            'confidence': confidence
        }
    
    def _construct_temporal_matrix(self, temporal_patterns):
        """Construct a matrix from temporal patterns."""
        if not temporal_patterns:
            return None
        
        # Extract pattern types and values
        pattern_types = []
        pattern_values = []
        
        for pattern in temporal_patterns:
            pattern_type = pattern.get('type', '')
            
            if pattern_type == 'day_of_week':
                pattern_types.append('day')
                pattern_values.append(pattern.get('day', 0))
            elif pattern_type == 'time_of_day':
                pattern_types.append('time')
                time_slot = pattern.get('time_slot', '')
                time_value = {'morning': 0, 'afternoon': 1, 'evening': 2, 'night': 3}.get(time_slot, 0)
                pattern_values.append(time_value)
            elif pattern_type == 'season':
                pattern_types.append('season')
                season = pattern.get('season', '')
                season_value = {'winter': 0, 'spring': 1, 'summer': 2, 'fall': 3}.get(season, 0)
                pattern_values.append(season_value)
            elif pattern_type == 'match_interval':
                pattern_types.append('interval')
                pattern_values.append(pattern.get('current_interval', 0))
            elif pattern_type == 'result_cycle':
                pattern_types.append('cycle')
                pattern_values.append(pattern.get('pattern_length', 0))
        
        if not pattern_types or not pattern_values:
            return None
        
        # Create a matrix of temporal factors
        matrix = []
        for i, pattern_type in enumerate(pattern_types):
            # For each pattern, create a row representing its temporal dimensions
            row = [0] * 5  # 5 dimensions: day, time, season, interval, cycle
            
            # Set the value for this pattern's dimension
            if pattern_type == 'day':
                row[0] = pattern_values[i]
            elif pattern_type == 'time':
                row[1] = pattern_values[i]
            elif pattern_type == 'season':
                row[2] = pattern_values[i]
            elif pattern_type == 'interval':
                row[3] = pattern_values[i]
            elif pattern_type == 'cycle':
                row[4] = pattern_values[i]
            
            matrix.append(row)
        
        # Extract combined patterns (interactions between temporal factors)
        combined_patterns = []
        
        # Check for day-time interactions
        if 'day' in pattern_types and 'time' in pattern_types:
            day_idx = pattern_types.index('day')
            time_idx = pattern_types.index('time')
            
            combined_patterns.append({
                'type': 'day_time_interaction',
                'day': pattern_values[day_idx],
                'time': pattern_values[time_idx],
                'confidence': 0.65
            })
        
        # Check for season-cycle interactions
        if 'season' in pattern_types and 'cycle' in pattern_types:
            season_idx = pattern_types.index('season')
            cycle_idx = pattern_types.index('cycle')
            
            combined_patterns.append({
                'type': 'season_cycle_interaction',
                'season': pattern_values[season_idx],
                'cycle': pattern_values[cycle_idx],
                'confidence': 0.7
            })
        
        # Calculate overall confidence
        pattern_confidence = sum(p.get('confidence', 0) for p in temporal_patterns) / len(temporal_patterns)
        combined_confidence = sum(p.get('confidence', 0) for p in combined_patterns) / len(combined_patterns) if combined_patterns else 0.5
        
        overall_confidence = pattern_confidence * 0.7 + combined_confidence * 0.3
        
        return {
            'dimensions': [len(matrix), 5],
            'matrix': matrix,
            'patterns': combined_patterns,
            'confidence': overall_confidence
        }
    
    def _encode_form_pattern(self, pattern):
        """Encode a form pattern into a symbolic representation."""
        sub_patterns = pattern.get('patterns', [])
        pattern_type = pattern.get('type', '')
        
        if not sub_patterns or pattern_type != 'form_matrix':
            return None
        
        # Look for prominent pattern types
        has_diagonal_trend = any(p.get('type') == 'diagonal_trend' for p in sub_patterns)
        has_home_impact = any(p.get('type') == 'home_form_impact' for p in sub_patterns)
        has_away_impact = any(p.get('type') == 'away_form_impact' for p in sub_patterns)
        
        # Generate a symbolic meaning
        symbol_id = f"form_symbol_{hash(str(sub_patterns))}"[:16]
        symbol_type = ''
        symbol_meaning = ''
        confidence = pattern.get('confidence', 0.5)
        
        if has_diagonal_trend:
            trend = next((p for p in sub_patterns if p.get('type') == 'diagonal_trend'), None)
            if trend:
                direction = trend.get('direction', '')
                if direction == 'positive':
                    symbol_type = 'ascending_spiral'
                    symbol_meaning = 'Mutually rising form trajectory'
                else:
                    symbol_type = 'descending_spiral'
                    symbol_meaning = 'Mutually declining form trajectory'
        elif has_home_impact and not has_away_impact:
            symbol_type = 'home_dominance'
            symbol_meaning = 'Home team form dictates match dynamic'
        elif has_away_impact and not has_home_impact:
            symbol_type = 'away_dominance'
            symbol_meaning = 'Away team form dictates match dynamic'
        elif has_home_impact and has_away_impact:
            symbol_type = 'form_balance'
            symbol_meaning = 'Balanced form influence from both teams'
        else:
            symbol_type = 'form_chaos'
            symbol_meaning = 'No clear form pattern emerges'
            confidence *= 0.8  # Reduce confidence for unclear patterns
        
        return {
            'id': symbol_id,
            'type': symbol_type,
            'meaning': symbol_meaning,
            'confidence': confidence,
            'source_pattern': pattern.get('id', '')
        }
    
    def _encode_result_pattern(self, pattern):
        """Encode a result pattern into a symbolic representation."""
        sub_patterns = pattern.get('patterns', [])
        pattern_type = pattern.get('type', '')
        
        if not sub_patterns or pattern_type != 'result_matrix':
            return None
        
        # Look for prominent pattern types
        has_venue_advantage = any(p.get('type') == 'venue_advantage' for p in sub_patterns)
        has_recency_trend = any(p.get('type') == 'recency_trend' for p in sub_patterns)
        
        # Generate a symbolic meaning
        symbol_id = f"result_symbol_{hash(str(sub_patterns))}"[:16]
        symbol_type = ''
        symbol_meaning = ''
        confidence = pattern.get('confidence', 0.5)
        
        if has_venue_advantage:
            advantage = next((p for p in sub_patterns if p.get('type') == 'venue_advantage'), None)
            if advantage:
                adv_type = advantage.get('advantage', '')
                if adv_type == 'home':
                    symbol_type = 'fortress'
                    symbol_meaning = 'Strong home territory advantage'
                else:
                    symbol_type = 'road_warriors'
                    symbol_meaning = 'Strong away performance pattern'
        elif has_recency_trend:
            trend = next((p for p in sub_patterns if p.get('type') == 'recency_trend'), None)
            if trend:
                direction = trend.get('direction', '')
                if direction == 'improving':
                    symbol_type = 'ascension'
                    symbol_meaning = 'Improving trajectory in recent confrontations'
                else:
                    symbol_type = 'decline'
                    symbol_meaning = 'Declining trajectory in recent confrontations'
        else:
            symbol_type = 'result_uncertainty'
            symbol_meaning = 'No clear historical result pattern'
            confidence *= 0.8  # Reduce confidence for unclear patterns
        
        return {
            'id': symbol_id,
            'type': symbol_type,
            'meaning': symbol_meaning,
            'confidence': confidence,
            'source_pattern': pattern.get('id', '')
        }
    
    def _encode_score_pattern(self, pattern):
        """Encode a score pattern into a symbolic representation."""
        sub_patterns = pattern.get('patterns', [])
        pattern_type = pattern.get('type', '')
        
        if not sub_patterns or pattern_type != 'score_matrix':
            return None
        
        # Look for prominent pattern types
        has_goals_consistency = any(p.get('type') == 'total_goals_consistency' for p in sub_patterns)
        has_consistent_dominance = any(p.get('type') == 'consistent_dominance' for p in sub_patterns)
        has_repeating_score = any(p.get('type') == 'repeating_score' for p in sub_patterns)
        
        # Generate a symbolic meaning
        symbol_id = f"score_symbol_{hash(str(sub_patterns))}"[:16]
        symbol_type = ''
        symbol_meaning = ''
        confidence = pattern.get('confidence', 0.5)
        
        if has_goals_consistency:
            consistency = next((p for p in sub_patterns if p.get('type') == 'total_goals_consistency'), None)
            if consistency:
                goal_type = consistency.get('goal_type', '')
                if goal_type == 'high_scoring':
                    symbol_type = 'goal_abundance'
                    symbol_meaning = 'High-scoring encounters with consistent pattern'
                else:
                    symbol_type = 'goal_scarcity'
                    symbol_meaning = 'Low-scoring encounters with consistent pattern'
        elif has_consistent_dominance:
            dominance = next((p for p in sub_patterns if p.get('type') == 'consistent_dominance'), None)
            if dominance:
                dominant = dominance.get('dominant_team', '')
                if dominant == 'home':
                    symbol_type = 'home_dominance'
                    symbol_meaning = 'Home team consistently outscores opposition'
                else:
                    symbol_type = 'away_dominance'
                    symbol_meaning = 'Away team consistently outscores opposition'
        elif has_repeating_score:
            repeat = next((p for p in sub_patterns if p.get('type') == 'repeating_score'), None)
            if repeat:
                symbol_type = 'score_echo'
                symbol_meaning = f"Repeating score pattern: {repeat.get('score', '')}"
        else:
            symbol_type = 'score_variability'
            symbol_meaning = 'Highly variable scoring patterns'
            confidence *= 0.8  # Reduce confidence for unclear patterns
        
        return {
            'id': symbol_id,
            'type': symbol_type,
            'meaning': symbol_meaning,
            'confidence': confidence,
            'source_pattern': pattern.get('id', '')
        }
    
    def _encode_temporal_pattern(self, pattern):
        """Encode a temporal pattern into a symbolic representation."""
        sub_patterns = pattern.get('patterns', [])
        pattern_type = pattern.get('type', '')
        
        if pattern_type != 'temporal_matrix':
            return None
        
        # Look for prominent pattern types
        has_day_time = any(p.get('type') == 'day_time_interaction' for p in sub_patterns)
        has_season_cycle = any(p.get('type') == 'season_cycle_interaction' for p in sub_patterns)
        
        # Generate a symbolic meaning
        symbol_id = f"temporal_symbol_{hash(str(sub_patterns))}"[:16]
        symbol_type = ''
        symbol_meaning = ''
        confidence = pattern.get('confidence', 0.5)
        
        if has_day_time:
            symbol_type = 'temporal_resonance'
            symbol_meaning = 'Specific day-time combination creates resonant pattern'
        elif has_season_cycle:
            symbol_type = 'seasonal_cycle'
            symbol_meaning = 'Seasonal influence interacts with result cycles'
        else:
            symbol_type = 'temporal_web'
            symbol_meaning = 'Complex web of temporal factors'
            confidence *= 0.8  # Reduce confidence for unclear patterns
        
        return {
            'id': symbol_id,
            'type': symbol_type,
            'meaning': symbol_meaning,
            'confidence': confidence,
            'source_pattern': pattern.get('id', '')
        }
    
    def _detect_form_anomaly(self, home_form, away_form):
        """Detect anomalies in team form patterns."""
        if not home_form or not away_form:
            return None
        
        # Extract form as lists (most recent first)
        home_form_list = [result for result in home_form if result in ['W', 'D', 'L']]
        away_form_list = [result for result in away_form if result in ['W', 'D', 'L']]
        
        # Ensure we have enough data
        if len(home_form_list) < 3 or len(away_form_list) < 3:
            return None
        
        # Look for perfect form with underdog odds (potential anomaly)
        perfect_home_form = all(result == 'W' for result in home_form_list[:3])
        perfect_away_form = all(result == 'W' for result in away_form_list[:3])
        
        if perfect_home_form and perfect_away_form:
            # Both teams in perfect form - potential anomaly
            return {
                'id': 'dual_perfect_form',
                'type': 'form_anomaly',
                'description': 'Both teams showing perfect recent form',
                'score': 0.8,
                'affected_elements': ['form_matrix']
            }
        
        # Look for sharp form reversals
        home_reversal = False
        if len(home_form_list) >= 5:
            recent_form = home_form_list[:3]
            earlier_form = home_form_list[3:5]
            
            if all(r == 'W' for r in recent_form) and all(r == 'L' for r in earlier_form):
                home_reversal = True
                
        away_reversal = False
        if len(away_form_list) >= 5:
            recent_form = away_form_list[:3]
            earlier_form = away_form_list[3:5]
            
            if all(r == 'W' for r in recent_form) and all(r == 'L' for r in earlier_form):
                away_reversal = True
        
        if home_reversal or away_reversal:
            team = 'home' if home_reversal else 'away'
            return {
                'id': f'{team}_form_reversal',
                'type': 'form_anomaly',
                'description': f'{team.capitalize()} team showing dramatic form reversal',
                'score': 0.75,
                'affected_elements': ['form_matrix']
            }
        
        return None
    
    def _detect_odds_anomaly(self, odds_data, match_data):
        """Detect anomalies in odds behavior."""
        if not odds_data:
            return None
        
        # Look for odds that don't align with form
        home_form = match_data.get('home_form', '')
        away_form = match_data.get('away_form', '')
        
        if home_form and away_form and len(home_form) >= 3 and len(away_form) >= 3:
            # Calculate form points (W=3, D=1, L=0 for most recent 3 matches)
            home_points = sum(3 if result == 'W' else 1 if result == 'D' else 0 for result in home_form[:3])
            away_points = sum(3 if result == 'W' else 1 if result == 'D' else 0 for result in away_form[:3])
            
            # Calculate form differential
            form_diff = home_points - away_points
            
            # Extract favorite from odds data text
            favorite = ''
            favorite_odds = 0
            underdog_odds = 0
            
            for key, value in odds_data.items():
                if 'favorite' in key.lower() and isinstance(value, str):
                    if 'home' in value.lower():
                        favorite = 'home'
                    elif 'away' in value.lower():
                        favorite = 'away'
                
                if 'odds' in key.lower() and 'home' in key.lower() and isinstance(value, str):
                    try:
                        favorite_odds = float(value.split()[-1])
                    except:
                        pass
                
                if 'odds' in key.lower() and 'away' in key.lower() and isinstance(value, str):
                    try:
                        underdog_odds = float(value.split()[-1])
                    except:
                        pass
            
            # Check for form-odds discrepancy
            if favorite and favorite_odds and underdog_odds:
                if favorite == 'home' and form_diff < -3:
                    # Home is favorite but away team has much better form
                    return {
                        'id': 'home_favorite_form_discrepancy',
                        'type': 'odds_anomaly',
                        'description': 'Home team favored despite significantly worse form',
                        'form_differential': form_diff,
                        'score': 0.85,
                        'affected_elements': ['form_matrix', 'odds_evaluation']
                    }
                elif favorite == 'away' and form_diff > 3:
                    # Away is favorite but home team has much better form
                    return {
                        'id': 'away_favorite_form_discrepancy',
                        'type': 'odds_anomaly',
                        'description': 'Away team favored despite significantly worse form',
                        'form_differential': form_diff,
                        'score': 0.85,
                        'affected_elements': ['form_matrix', 'odds_evaluation']
                    }
        
        return None
    
    def _detect_symbolic_anomaly(self, encoded_symbols):
        """Detect anomalies in symbolic patterns."""
        if not encoded_symbols or len(encoded_symbols) < 2:
            return None
        
        # Look for conflicting symbolic meanings
        contradictions = []
        for i in range(len(encoded_symbols)):
            for j in range(i+1, len(encoded_symbols)):
                symbol1 = encoded_symbols[i]
                symbol2 = encoded_symbols[j]
                
                # Check for direct contradictions
                if (symbol1.get('type') == 'ascending_spiral' and symbol2.get('type') == 'descending_spiral') or \
                   (symbol1.get('type') == 'descending_spiral' and symbol2.get('type') == 'ascending_spiral') or \
                   (symbol1.get('type') == 'home_dominance' and symbol2.get('type') == 'away_dominance') or \
                   (symbol1.get('type') == 'away_dominance' and symbol2.get('type') == 'home_dominance') or \
                   (symbol1.get('type') == 'goal_abundance' and symbol2.get('type') == 'goal_scarcity') or \
                   (symbol1.get('type') == 'goal_scarcity' and symbol2.get('type') == 'goal_abundance'):
                    contradictions.append((symbol1.get('id', ''), symbol2.get('id', '')))
        
        if contradictions:
            symbols_involved = []
            for s1, s2 in contradictions:
                symbols_involved.append(s1)
                symbols_involved.append(s2)
            
            return {
                'id': 'symbolic_contradiction',
                'type': 'symbolic_anomaly',
                'description': 'Contradictory symbolic patterns detected',
                'contradiction_count': len(contradictions),
                'score': 0.7 + min(0.2, len(contradictions) * 0.1),
                'affected_elements': list(set(symbols_involved))
            }
        
        return None
    
    def _detect_historical_anomaly(self, historical_matchups, match_data):
        """Detect anomalies in historical patterns."""
        if not historical_matchups or len(historical_matchups) < 4:
            return None
        
        # Sort matchups by date
        sorted_matchups = sorted(historical_matchups, key=lambda m: m.get('date', datetime.now()))
        
        # Look for unusual streaks
        results = []
        for match in sorted_matchups:
            result = match.get('result', '')
            if result in ['W', 'D', 'L']:
                results.append(result)
        
        if len(results) >= 4:
            # Check for perfect streaks
            last_four = results[-4:]
            
            if all(r == last_four[0] for r in last_four):
                # Perfect streak of same result
                return {
                    'id': 'perfect_result_streak',
                    'type': 'historical_anomaly',
                    'description': f'Perfect streak of {last_four[0]} results in last {len(last_four)} matches',
                    'streak_result': last_four[0],
                    'streak_length': len(last_four),
                    'score': 0.75,
                    'affected_elements': ['result_matrix']
                }
        
        # Look for unusual score patterns
        scores = []
        for match in sorted_matchups:
            home_score = match.get('home_score')
            away_score = match.get('away_score')
            
            if home_score is not None and away_score is not None:
                scores.append([home_score, away_score])
        
        if len(scores) >= 3:
            # Check for exact repeating scores
            last_three = scores[-3:]
            
            if all(s == last_three[0] for s in last_three):
                # Exact same score in last three matches
                return {
                    'id': 'repeating_exact_score',
                    'type': 'historical_anomaly',
                    'description': f'Exact same score ({last_three[0][0]}-{last_three[0][1]}) in last {len(last_three)} matches',
                    'score_pattern': f"{last_three[0][0]}-{last_three[0][1]}",
                    'repetition_count': len(last_three),
                    'score': 0.85,
                    'affected_elements': ['score_matrix']
                }
        
        return None
    
    def _calculate_pattern_coherence(self, patterns):
        """Calculate the coherence of a set of patterns."""
        if not patterns or len(patterns) < 2:
            return 0.5  # Neutral coherence for a single pattern
        
        # Calculate average confidence
        avg_confidence = sum(p.get('confidence', 0.5) for p in patterns) / len(patterns)
        
        # Count patterns supporting each outcome
        home_support = 0
        away_support = 0
        draw_support = 0
        
        for pattern in patterns:
            pattern_type = pattern.get('type', '')
            
            # Categorize pattern support
            if pattern_type in ['home_dominance', 'fortress', 'ascending_spiral'] or \
               (pattern_type == 'venue_advantage' and pattern.get('advantage') == 'home'):
                home_support += pattern.get('confidence', 0.5)
            elif pattern_type in ['away_dominance', 'road_warriors', 'descending_spiral'] or \
                 (pattern_type == 'venue_advantage' and pattern.get('advantage') == 'away'):
                away_support += pattern.get('confidence', 0.5)
            elif pattern_type in ['form_balance', 'score_echo', 'goal_scarcity']:
                draw_support += pattern.get('confidence', 0.5)
        
        # Calculate support distribution
        total_support = home_support + away_support + draw_support
        if total_support == 0:
            return 0.5  # No clear support
        
        # Calculate normalized distribution
        home_pct = home_support / total_support
        away_pct = away_support / total_support
        draw_pct = draw_support / total_support
        
        # Calculate entropy of distribution (lower entropy = more coherent)
        entropy = 0
        for p in [home_pct, away_pct, draw_pct]:
            if p > 0:
                entropy -= p * math.log2(p)
        
        # Normalize entropy to 0-1 (0 = completely incoherent, 1 = perfectly coherent)
        max_entropy = math.log2(3)  # Maximum entropy with 3 outcomes
        normalized_coherence = 1 - (entropy / max_entropy)
        
        # Combine with average confidence
        coherence = normalized_coherence * 0.7 + avg_confidence * 0.3
        
        return coherence
    
    def _calculate_symbol_resonance(self, symbol1, symbol2):
        """Calculate the resonance between two symbolic patterns."""
        # Check if symbols have different types
        if symbol1.get('type', '') == symbol2.get('type', ''):
            return 0.0  # Same type = no resonance
        
        # Define resonant pairs
        resonant_pairs = [
            ('ascending_spiral', 'home_dominance'),
            ('descending_spiral', 'away_dominance'),
            ('form_balance', 'goal_scarcity'),
            ('fortress', 'goal_abundance'),
            ('road_warriors', 'score_variability'),
            ('temporal_resonance', 'ascension')
        ]
        
        # Check if these types form a resonant pair
        type1 = symbol1.get('type', '')
        type2 = symbol2.get('type', '')
        
        for pair in resonant_pairs:
            if (type1 == pair[0] and type2 == pair[1]) or (type1 == pair[1] and type2 == pair[0]):
                # Calculate resonance based on confidence levels
                confidence1 = symbol1.get('confidence', 0.5)
                confidence2 = symbol2.get('confidence', 0.5)
                
                # Strong resonance if both symbols have high confidence
                return (confidence1 * confidence2) ** 0.5  # Geometric mean
        
        # No resonance found
        return 0.3  # Low default resonance
    
    def _generate_insights(self, patterns):
        """Generate insights from pattern relationships."""
        if not patterns or len(patterns) < 2:
            return []
        
        insights = []
        
        # Group patterns by type
        pattern_by_type = {}
        for pattern in patterns:
            pattern_type = pattern.get('type', 'unknown')
            if pattern_type not in pattern_by_type:
                pattern_by_type[pattern_type] = []
            pattern_by_type[pattern_type].append(pattern)
        
        # Generate insights for form + result interactions
        if 'form_matrix' in pattern_by_type and 'result_matrix' in pattern_by_type:
            form_patterns = pattern_by_type['form_matrix']
            result_patterns = pattern_by_type['result_matrix']
            
            for form_pattern in form_patterns:
                for result_pattern in result_patterns:
                    # Generate a unique insight ID
                    insight_id = f"insight_form_result_{hash(form_pattern['id'] + result_pattern['id'])}"[:16]
                    
                    # Calculate relationship strength
                    relationship = self._calculate_form_result_relationship(form_pattern, result_pattern)
                    
                    if relationship['strength'] > 0.6:
                        insights.append({
                            'id': insight_id,
                            'type': 'form_result_insight',
                            'description': relationship['description'],
                            'patterns': [form_pattern['id'], result_pattern['id']],
                            'confidence': relationship['strength']
                        })
        
        # Generate insights for temporal + score interactions
        if 'temporal_matrix' in pattern_by_type and 'score_matrix' in pattern_by_type:
            temporal_patterns = pattern_by_type['temporal_matrix']
            score_patterns = pattern_by_type['score_matrix']
            
            for temporal_pattern in temporal_patterns:
                for score_pattern in score_patterns:
                    # Generate a unique insight ID
                    insight_id = f"insight_temporal_score_{hash(temporal_pattern['id'] + score_pattern['id'])}"[:16]
                    
                    # Calculate relationship strength
                    relationship = self._calculate_temporal_score_relationship(temporal_pattern, score_pattern)
                    
                    if relationship['strength'] > 0.6:
                        insights.append({
                            'id': insight_id,
                            'type': 'temporal_score_insight',
                            'description': relationship['description'],
                            'patterns': [temporal_pattern['id'], score_pattern['id']],
                            'confidence': relationship['strength']
                        })
        
        return insights
    
    def _calculate_form_result_relationship(self, form_pattern, result_pattern):
        """Calculate the relationship between form and result patterns."""
        # Default relationship
        relationship = {
            'strength': 0.5,
            'description': 'Form and result patterns show standard correlation'
        }
        
        # Extracting sub-patterns
        form_sub_patterns = form_pattern.get('patterns', [])
        result_sub_patterns = result_pattern.get('patterns', [])
        
        # Look for specific combinations
        has_diagonal_trend = any(p.get('type') == 'diagonal_trend' for p in form_sub_patterns)
        has_venue_advantage = any(p.get('type') == 'venue_advantage' for p in result_sub_patterns)
        
        if has_diagonal_trend and has_venue_advantage:
            # Get the details of each pattern
            diagonal_trend = next((p for p in form_sub_patterns if p.get('type') == 'diagonal_trend'), None)
            venue_advantage = next((p for p in result_sub_patterns if p.get('type') == 'venue_advantage'), None)
            
            if diagonal_trend and venue_advantage:
                trend_direction = diagonal_trend.get('direction', '')
                advantage_type = venue_advantage.get('advantage', '')
                
                # Check for reinforcing patterns
                if (trend_direction == 'positive' and advantage_type == 'home') or \
                   (trend_direction == 'negative' and advantage_type == 'away'):
                    relationship['strength'] = 0.85
                    relationship['description'] = f"{trend_direction.capitalize()} form trend reinforces {advantage_type} venue advantage"
                else:
                    # Conflicting patterns
                    relationship['strength'] = 0.7
                    relationship['description'] = f"{trend_direction.capitalize()} form trend conflicts with {advantage_type} venue advantage"
        
        return relationship
    
    def _calculate_temporal_score_relationship(self, temporal_pattern, score_pattern):
        """Calculate the relationship between temporal and score patterns."""
        # Default relationship
        relationship = {
            'strength': 0.5,
            'description': 'Temporal and score patterns show standard correlation'
        }
        
        # Extracting sub-patterns
        temporal_sub_patterns = temporal_pattern.get('patterns', [])
        score_sub_patterns = score_pattern.get('patterns', [])
        
        # Look for specific combinations
        has_day_time = any(p.get('type') == 'day_time_interaction' for p in temporal_sub_patterns)
        has_goals_consistency = any(p.get('type') == 'total_goals_consistency' for p in score_sub_patterns)
        
        if has_day_time and has_goals_consistency:
            # Get the details of each pattern
            day_time = next((p for p in temporal_sub_patterns if p.get('type') == 'day_time_interaction'), None)
            goals_consistency = next((p for p in score_sub_patterns if p.get('type') == 'total_goals_consistency'), None)
            
            if day_time and goals_consistency:
                day = day_time.get('day', 0)
                time = day_time.get('time', 0)
                goal_type = goals_consistency.get('goal_type', '')
                
                # Check for weekend night games with high scoring
                if day >= 5 and time >= 2 and goal_type == 'high_scoring':
                    relationship['strength'] = 0.85
                    relationship['description'] = "Weekend evening matches show strong correlation with high scoring"
                elif day <= 4 and time <= 1 and goal_type == 'low_scoring':
                    relationship['strength'] = 0.8
                    relationship['description'] = "Weekday day matches show strong correlation with low scoring"
                else:
                    relationship['strength'] = 0.65
                    relationship['description'] = f"Specific {['weekday', 'weekend'][day >= 5]} {['day', 'evening'][time >= 2]} pattern correlates with {goal_type} matches"
        
        return relationship
    
    def _extract_match_features(self, match_data):
        """Extract key features from match data for pattern matching."""
        features = {}
        
        # Basic match information
        features['sport'] = match_data.get('sport', '')
        features['league'] = match_data.get('league', '')
        features['home_team'] = match_data.get('home_team', '')
        features['away_team'] = match_data.get('away_team', '')
        
        # Date and time features
        match_date = match_data.get('date')
        if match_date:
            if isinstance(match_date, str):
                try:
                    match_date = datetime.fromisoformat(match_date.replace('Z', '+00:00'))
                except:
                    match_date = datetime.now()
            
            features['day_of_week'] = match_date.weekday()
            features['hour'] = match_date.hour
            features['month'] = match_date.month
            features['season'] = 'winter' if match_date.month in [12, 1, 2] else 'spring' if match_date.month in [3, 4, 5] else 'summer' if match_date.month in [6, 7, 8] else 'fall'
        
        # Form features
        home_form = match_data.get('home_form', '')
        away_form = match_data.get('away_form', '')
        
        if home_form and away_form:
            # Calculate recent form points (W=3, D=1, L=0)
            home_recent = home_form[:3] if len(home_form) >= 3 else home_form
            away_recent = away_form[:3] if len(away_form) >= 3 else away_form
            
            home_points = sum(3 if result == 'W' else 1 if result == 'D' else 0 for result in home_recent)
            away_points = sum(3 if result == 'W' else 1 if result == 'D' else 0 for result in away_recent)
            
            features['home_form_points'] = home_points
            features['away_form_points'] = away_points
            features['form_differential'] = home_points - away_points
        
        # Odds features if available
        home_odds = match_data.get('home_odds')
        draw_odds = match_data.get('draw_odds')
        away_odds = match_data.get('away_odds')
        
        if home_odds is not None and away_odds is not None:
            features['home_odds'] = home_odds
            features['away_odds'] = away_odds
            features['odds_differential'] = away_odds - home_odds
            
            # Favorite determination
            if home_odds < away_odds:
                features['favorite'] = 'home'
                features['underdog'] = 'away'
            else:
                features['favorite'] = 'away'
                features['underdog'] = 'home'
            
            if draw_odds is not None:
                features['draw_odds'] = draw_odds
        
        return features
    
    def _calculate_insight_relevance(self, insight, match_features):
        """Calculate how relevant an insight is to a specific match."""
        # Default moderate relevance
        relevance = 0.5
        
        insight_type = insight.get('type', '')
        
        # Adjust relevance based on insight type and match features
        if insight_type == 'form_result_insight':
            # Check form differential against insight
            form_diff = match_features.get('form_differential', 0)
            
            # Increase relevance for insights that match current form situation
            if 'strong form' in insight.get('description', '').lower() and abs(form_diff) > 5:
                relevance += 0.2
            elif 'balanced form' in insight.get('description', '').lower() and abs(form_diff) < 3:
                relevance += 0.2
        
        elif insight_type == 'pattern_synergy':
            # Check if the pattern types match the current match features
            pattern_types = insight.get('description', '').lower()
            
            # Adjust for temporal patterns
            if 'day' in pattern_types or 'time' in pattern_types or 'season' in pattern_types:
                relevance += 0.15
            
            # Adjust for venue patterns
            if 'home' in pattern_types or 'away' in pattern_types:
                relevance += 0.15
            
            # Adjust for score patterns
            if 'score' in pattern_types or 'goal' in pattern_types:
                relevance += 0.1
        
        # Normalize to 0-1 range
        return max(0, min(1, relevance))
    
    def _detect_narratives(self, features):
        """Detect narrative structures in match features."""
        narratives = []
        
        # Check for underdog story
        if 'favorite' in features and 'form_differential' in features:
            favorite = features.get('favorite', '')
            form_diff = features.get('form_differential', 0)
            
            if favorite == 'home' and form_diff < -3:
                # Underdog home team with strong favorite status
                narratives.append({
                    'id': 'home_underdog',
                    'type': 'underdog_narrative',
                    'description': 'Home team cast as favorite despite underdog form',
                    'confidence': 0.7
                })
            elif favorite == 'away' and form_diff > 3:
                # Underdog away team with strong favorite status
                narratives.append({
                    'id': 'away_underdog',
                    'type': 'underdog_narrative',
                    'description': 'Away team cast as favorite despite underdog form',
                    'confidence': 0.7
                })
        
        # Check for rivalry narrative
        home_team = features.get('home_team', '')
        away_team = features.get('away_team', '')
        
        if home_team and away_team:
            # Simple heuristic for classic rivalries
            rivalries = [
                (['Manchester United', 'Manchester City'], 'manchester_derby'),
                (['Liverpool', 'Everton'], 'merseyside_derby'),
                (['Arsenal', 'Tottenham'], 'north_london_derby'),
                (['Barcelona', 'Real Madrid'], 'el_clasico'),
                (['Roma', 'Lazio'], 'derby_della_capitale')
            ]
            
            for teams, rivalry_id in rivalries:
                if (teams[0] in home_team and teams[1] in away_team) or \
                   (teams[1] in home_team and teams[0] in away_team):
                    narratives.append({
                        'id': rivalry_id,
                        'type': 'rivalry_narrative',
                        'description': f'Classic rivalry match between historical adversaries',
                        'confidence': 0.9
                    })
        
        # Check for redemption narrative
        if 'home_form' in features and 'away_form' in features:
            home_form = features.get('home_form', '')
            away_form = features.get('away_form', '')
            
            if len(home_form) >= 5 and home_form[0] == 'W' and all(r == 'L' for r in home_form[1:4]):
                narratives.append({
                    'id': 'home_redemption',
                    'type': 'redemption_narrative',
                    'description': 'Home team seeking redemption after string of losses',
                    'confidence': 0.75
                })
            elif len(away_form) >= 5 and away_form[0] == 'W' and all(r == 'L' for r in away_form[1:4]):
                narratives.append({
                    'id': 'away_redemption',
                    'type': 'redemption_narrative',
                    'description': 'Away team seeking redemption after string of losses',
                    'confidence': 0.75
                })
        
        return narratives
    
    def _detect_cycles(self, features, match_data):
        """Detect cyclical patterns in match features."""
        cycles = []
        
        # Extract historical matchups
        historical_matchups = match_data.get('historical_matchups', [])
        
        if len(historical_matchups) >= 5:
            # Sort by date
            sorted_matches = sorted(historical_matchups, key=lambda m: m.get('date', datetime.now()))
            
            # Extract result sequence
            results = []
            for match in sorted_matches:
                result = match.get('result', '')
                if result in ['W', 'D', 'L']:
                    results.append(result)
            
            # Look for repeating patterns of length 2-3
            for pattern_length in [2, 3]:
                if len(results) >= pattern_length * 2:
                    # Check if the last <pattern_length> results repeat
                    pattern = results[-pattern_length:]
                    
                    # Check if this pattern appears earlier
                    for i in range(len(results) - pattern_length * 2 + 1):
                        if results[i:i+pattern_length] == pattern:
                            cycles.append({
                                'id': f"result_cycle_{pattern_length}",
                                'type': 'result_cycle',
                                'pattern': pattern,
                                'description': f"Cyclical pattern of results repeating every {pattern_length} matches",
                                'confidence': 0.6 + 0.1 * pattern_length
                            })
                            break
        
        # Check for seasonal cycles
        season = features.get('season', '')
        if season:
            # Check historical performance in this season
            season_matches = []
            for match in historical_matchups:
                match_date = match.get('date')
                if not match_date:
                    continue
                
                if isinstance(match_date, str):
                    try:
                        match_date = datetime.fromisoformat(match_date.replace('Z', '+00:00'))
                    except:
                        continue
                
                match_month = match_date.month
                match_season = 'winter' if match_month in [12, 1, 2] else 'spring' if match_month in [3, 4, 5] else 'summer' if match_month in [6, 7, 8] else 'fall'
                
                if match_season == season:
                    season_matches.append(match)
            
            if len(season_matches) >= 3:
                # Calculate win percentage in this season
                wins = sum(1 for m in season_matches if m.get('result', '') == 'W')
                season_win_pct = wins / len(season_matches)
                
                # Compare to overall win percentage
                all_wins = sum(1 for m in historical_matchups if m.get('result', '') == 'W')
                overall_win_pct = all_wins / len(historical_matchups) if historical_matchups else 0
                
                # If there's a significant difference
                if abs(season_win_pct - overall_win_pct) > 0.2:
                    performance = 'strong' if season_win_pct > overall_win_pct else 'weak'
                    cycles.append({
                        'id': f"{season}_cycle",
                        'type': 'seasonal_cycle',
                        'season': season,
                        'description': f"{performance.capitalize()} cyclical performance during {season} season",
                        'confidence': 0.5 + abs(season_win_pct - overall_win_pct)
                    })
        
        return cycles
    
    def _detect_paradoxes(self, features, match_data):
        """Detect paradoxical elements in match features."""
        paradoxes = []
        
        # Check for form vs. odds paradox
        if 'favorite' in features and 'form_differential' in features:
            favorite = features.get('favorite', '')
            form_diff = features.get('form_differential', 0)
            
            if (favorite == 'home' and form_diff < -5) or (favorite == 'away' and form_diff > 5):
                # Strong form contradiction with odds
                paradoxes.append({
                    'id': 'form_odds_paradox',
                    'type': 'betting_paradox',
                    'description': 'Strong contradiction between team form and betting odds',
                    'confidence': 0.8
                })
        
        # Check for historical vs. current form paradox
        historical_matchups = match_data.get('historical_matchups', [])
        
        if historical_matchups and len(historical_matchups) >= 4:
            # Calculate historical dominance
            home_team = features.get('home_team', '')
            away_team = features.get('away_team', '')
            
            home_wins = 0
            away_wins = 0
            
            for match in historical_matchups:
                match_home = match.get('home_team', '')
                match_away = match.get('away_team', '')
                match_result = match.get('result', '')
                
                if match_home == home_team and match_away == away_team:
                    if match_result == 'W':
                        home_wins += 1
                    elif match_result == 'L':
                        away_wins += 1
                elif match_home == away_team and match_away == home_team:
                    if match_result == 'W':
                        away_wins += 1
                    elif match_result == 'L':
                        home_wins += 1
            
            # Determine historical dominant team
            historically_dominant = None
            if home_wins > away_wins * 2 and home_wins >= 3:
                historically_dominant = 'home'
            elif away_wins > home_wins * 2 and away_wins >= 3:
                historically_dominant = 'away'
            
            # Check against current form
            if historically_dominant and 'form_differential' in features:
                form_diff = features.get('form_differential', 0)
                
                if historically_dominant == 'home' and form_diff < -5:
                    # Home team historically dominant but in much worse form
                    paradoxes.append({
                        'id': 'home_dominance_paradox',
                        'type': 'historical_paradox',
                        'description': 'Historically dominant home team currently in much worse form',
                        'confidence': 0.7
                    })
                elif historically_dominant == 'away' and form_diff > 5:
                    # Away team historically dominant but in much worse form
                    paradoxes.append({
                        'id': 'away_dominance_paradox',
                        'type': 'historical_paradox',
                        'description': 'Historically dominant away team currently in much worse form',
                        'confidence': 0.7
                    })
        
        return paradoxes
    
    def _detect_symbolic_resonance(self, features, match_data):
        """Detect symbolic resonance patterns in match features."""
        symbols = []
        
        # Check for day-of-week symbolism
        day_of_week = features.get('day_of_week')
        if day_of_week is not None:
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_energies = ['renewal', 'conflict', 'balance', 'expansion', 'culmination', 'activation', 'reflection']
            
            symbols.append({
                'id': f"day_energy_{day_names[day_of_week].lower()}",
                'type': 'temporal_symbolism',
                'element': day_names[day_of_week],
                'resonance': day_energies[day_of_week],
                'description': f"{day_names[day_of_week]} energy pattern - {day_energies[day_of_week]}",
                'confidence': 0.6
            })
        
        # Check for season symbolism
        season = features.get('season', '')
        if season:
            season_elements = {
                'winter': 'water',
                'spring': 'wood',
                'summer': 'fire',
                'fall': 'metal'
            }
            
            if season in season_elements:
                symbols.append({
                    'id': f"season_element_{season}",
                    'type': 'elemental_symbolism',
                    'element': season_elements[season],
                    'season': season,
                    'description': f"{season.capitalize()} season resonates with {season_elements[season]} element energy",
                    'confidence': 0.65
                })
        
        # Check for team name symbolism
        home_team = features.get('home_team', '')
        away_team = features.get('away_team', '')
        
        if home_team and away_team:
            home_elements = self._extract_team_symbolism(home_team)
            away_elements = self._extract_team_symbolism(away_team)
            
            if home_elements:
                symbols.append({
                    'id': f"home_team_symbolism",
                    'type': 'team_symbolism',
                    'team': 'home',
                    'elements': home_elements,
                    'description': f"Home team name resonates with {', '.join(home_elements)} energies",
                    'confidence': 0.6
                })
            
            if away_elements:
                symbols.append({
                    'id': f"away_team_symbolism",
                    'type': 'team_symbolism',
                    'team': 'away',
                    'elements': away_elements,
                    'description': f"Away team name resonates with {', '.join(away_elements)} energies",
                    'confidence': 0.6
                })
        
        return symbols
    
    def _extract_team_symbolism(self, team_name):
        """Extract symbolic elements from a team name."""
        elements = []
        
        # Color associations
        color_elements = {
            'red': 'fire',
            'blue': 'water',
            'green': 'wood',
            'white': 'metal',
            'black': 'water',
            'gold': 'metal',
            'yellow': 'earth'
        }
        
        for color, element in color_elements.items():
            if color in team_name.lower():
                elements.append(element)
        
        # Animal/mascot associations
        animal_elements = {
            'lion': 'fire',
            'tiger': 'wood',
            'dragon': 'water',
            'eagle': 'metal',
            'bear': 'earth',
            'wolf': 'metal',
            'fox': 'fire'
        }
        
        for animal, element in animal_elements.items():
            if animal in team_name.lower():
                elements.append(element)
        
        # Nature associations
        nature_elements = {
            'forest': 'wood',
            'lake': 'water',
            'mountain': 'earth',
            'river': 'water',
            'star': 'fire',
            'city': 'metal',
            'united': 'earth'
        }
        
        for nature, element in nature_elements.items():
            if nature in team_name.lower():
                elements.append(element)
        
        return list(set(elements))  # Remove duplicates
    
    def _generate_scenario_description(self, scenario_changes):
        """Generate a descriptive summary of a counterfactual scenario."""
        if not scenario_changes:
            return "Baseline scenario with no modifications"
        
        descriptions = []
        
        # Process each type of change
        for key, value in scenario_changes.items():
            if key == 'home_form' or key == 'away_form':
                descriptions.append(f"Modified {key.replace('_', ' ')} to '{value}'")
            elif key == 'home_odds' or key == 'away_odds' or key == 'draw_odds':
                descriptions.append(f"Changed {key.replace('_', ' ')} to {value}")
            elif isinstance(value, dict):
                sub_changes = [f"{k.replace('_', ' ')} to {v}" for k, v in value.items()]
                descriptions.append(f"Modified {key.replace('_', ' ')}: {', '.join(sub_changes)}")
            else:
                descriptions.append(f"Changed {key.replace('_', ' ')} to {value}")
        
        return "; ".join(descriptions)
    
    def _generate_counterfactual_conclusion(self, differences):
        """Generate a conclusion from counterfactual analysis differences."""
        delta = differences.get('neural_confidence_delta', 0)
        
        if abs(delta) < 0.1:
            return "The scenario changes have minimal impact on prediction confidence"
        elif delta > 0.1:
            strength = "slightly" if delta < 0.2 else "moderately" if delta < 0.3 else "significantly"
            return f"The scenario changes {strength} increase prediction confidence by {delta:.1%}"
        else:  # delta < -0.1
            strength = "slightly" if delta > -0.2 else "moderately" if delta > -0.3 else "significantly"
            return f"The scenario changes {strength} decrease prediction confidence by {abs(delta):.1%}"
    
    def _generate_analysis_id(self, match_data):
        """Generate a unique ID for an analysis."""
        # Extract key match info
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        match_date = match_data.get('date', datetime.now())
        
        if isinstance(match_date, str):
            date_str = match_date
        else:
            date_str = match_date.strftime('%Y%m%d%H%M')
        
        # Generate a unique hash
        match_str = f"{home_team}_{away_team}_{date_str}"
        hash_id = hashlib.md5(match_str.encode()).hexdigest()[:8]
        
        return f"neural_analysis_{hash_id}"
    
    def _is_prediction_correct(self, prediction, actual_result):
        """Check if a prediction matches the actual result."""
        # Extract predicted outcome
        predicted = prediction.get('outcome', '')
        
        # Extract actual outcome
        actual = actual_result.get('outcome', '')
        
        return predicted == actual
    
    def recalibrate_patterns(self, specific_patterns=None):
        """
        Recalibrate pattern weights based on historical performance.
        This method is typically called by ArcanReflex when pattern-based anomalies are detected.
        
        Args:
            specific_patterns (list, optional): List of specific pattern IDs to recalibrate. 
                                                If None, all patterns are recalibrated.
                                                
        Returns:
            dict: Recalibration report
        """
        patterns_to_recalibrate = specific_patterns or list(self.long_term_memory.keys())
        
        recalibration_report = {
            'patterns_recalibrated': 0,
            'patterns_strengthened': 0,
            'patterns_weakened': 0,
            'average_confidence_delta': 0.0,
            'details': []
        }
        
        total_confidence_delta = 0.0
        
        for pattern_id in patterns_to_recalibrate:
            if pattern_id not in self.long_term_memory:
                continue
                
            pattern = self.long_term_memory[pattern_id]
            
            # Skip patterns with insufficient data
            correct_count = pattern.get('correct_count', 0)
            incorrect_count = pattern.get('incorrect_count', 0)
            
            if correct_count + incorrect_count < 3:
                continue
                
            # Calculate success ratio
            success_ratio = correct_count / (correct_count + incorrect_count)
            
            # Current confidence
            current_confidence = pattern.get('confidence', 0.5)
            
            # Calculate ideal confidence based on performance
            ideal_confidence = 0.5 + (success_ratio - 0.5) * 0.8
            
            # Apply smoothing to avoid extreme values
            ideal_confidence = max(0.2, min(0.95, ideal_confidence))
            
            # Calculate confidence adjustment factor 
            # (higher for patterns with more data, lower for newer patterns)
            adjustment_factor = min(0.7, (correct_count + incorrect_count) / 20)
            
            # Calculate new confidence
            new_confidence = current_confidence * (1 - adjustment_factor) + ideal_confidence * adjustment_factor
            
            # Apply the new confidence
            confidence_delta = new_confidence - current_confidence
            pattern['confidence'] = new_confidence
            pattern['last_recalibrated'] = datetime.now().isoformat()
            
            recalibration_report['patterns_recalibrated'] += 1
            total_confidence_delta += abs(confidence_delta)
            
            if confidence_delta > 0.01:
                recalibration_report['patterns_strengthened'] += 1
            elif confidence_delta < -0.01:
                recalibration_report['patterns_weakened'] += 1
                
            # Store details for the report
            recalibration_report['details'].append({
                'pattern_id': pattern_id,
                'pattern_type': pattern.get('type', 'unknown'),
                'old_confidence': current_confidence,
                'new_confidence': new_confidence,
                'delta': confidence_delta,
                'success_ratio': success_ratio,
                'data_points': correct_count + incorrect_count
            })
        
        # Calculate average confidence delta
        if recalibration_report['patterns_recalibrated'] > 0:
            recalibration_report['average_confidence_delta'] = total_confidence_delta / recalibration_report['patterns_recalibrated']
            
        # Notify MetaSystems of recalibration
        if self.meta_systems and recalibration_report['patterns_recalibrated'] > 0:
            self.meta_systems.trigger_event('patterns_recalibrated', {
                'source': 'ArcanBrain',
                'timestamp': datetime.now().isoformat(),
                'patterns_recalibrated': recalibration_report['patterns_recalibrated'],
                'patterns_strengthened': recalibration_report['patterns_strengthened'],
                'patterns_weakened': recalibration_report['patterns_weakened'],
                'average_confidence_delta': recalibration_report['average_confidence_delta']
            })
            
        return recalibration_report
    
    def apply_transfer_learning(self, source_context, target_context, similarity_threshold=0.6):
        """
        Apply transfer learning from a source context to a target context.
        This allows patterns learned in one type of match or league to be applied
        to a new context with appropriate adjustments.
        
        Args:
            source_context (dict): The source context with patterns to transfer from
                                  (e.g., {'sport': 'football', 'league': 'Premier League'})
            target_context (dict): The target context to transfer patterns to
                                  (e.g., {'sport': 'football', 'league': 'La Liga'})
            similarity_threshold (float): Minimum similarity score required for transfer
            
        Returns:
            dict: Transfer learning report
        """
        report = {
            'patterns_analyzed': 0,
            'patterns_transferred': 0,
            'patterns_strengthened': 0,
            'patterns_created': 0,
            'average_similarity': 0.0,
            'details': []
        }
        
        # Extract context keys for comparison
        source_keys = sorted(source_context.keys())
        target_keys = sorted(target_context.keys())
        
        # Calculate base context similarity
        context_similarity = self._calculate_context_similarity(source_context, target_context)
        
        # Only proceed if contexts are similar enough for transfer
        if context_similarity < similarity_threshold * 0.7:
            report['error'] = f"Contexts too dissimilar for transfer learning ({context_similarity:.2f})"
            return report
            
        # Find patterns in long-term memory that match the source context
        source_patterns = []
        for pattern_id, pattern in self.long_term_memory.items():
            pattern_context = pattern.get('context', {})
            matches_source = True
            
            for key, value in source_context.items():
                if pattern_context.get(key) != value:
                    matches_source = False
                    break
                    
            if matches_source:
                source_patterns.append(pattern)
                report['patterns_analyzed'] += 1
                
        # Transfer applicable patterns to target context
        total_similarity = 0.0
        
        for source_pattern in source_patterns:
            # Skip patterns with low confidence or insufficient data
            if source_pattern.get('confidence', 0) < 0.4:
                continue
                
            pattern_type = source_pattern.get('type', '')
            pattern_features = source_pattern.get('features', {})
            
            # Calculate pattern transferability
            transferability = self._calculate_pattern_transferability(
                pattern_type, 
                pattern_features,
                source_context, 
                target_context
            )
            
            if transferability < similarity_threshold:
                continue
                
            # Check if a similar pattern already exists in target context
            target_pattern_id = None
            target_pattern = None
            
            for p_id, p in self.long_term_memory.items():
                if (p.get('type') == pattern_type and 
                    self._match_context(p.get('context', {}), target_context) and
                    self._calculate_feature_similarity(p.get('features', {}), pattern_features) > 0.8):
                    target_pattern_id = p_id
                    target_pattern = p
                    break
                    
            # Transfer learning logic
            if target_pattern:
                # Update existing pattern in target context
                old_confidence = target_pattern.get('confidence', 0.5)
                
                # Calculate influence based on source pattern strength and transferability
                source_influence = source_pattern.get('confidence', 0.5) * transferability * 0.4
                
                # Apply transfer learning with dampening (less influence than direct learning)
                new_confidence = old_confidence * 0.7 + source_influence * 0.3
                
                # Apply updated confidence
                target_pattern['confidence'] = new_confidence
                target_pattern['last_transfer_update'] = datetime.now().isoformat()
                target_pattern['transfer_source'] = source_pattern.get('id', '')
                
                report['patterns_transferred'] += 1
                
                if new_confidence > old_confidence + 0.02:
                    report['patterns_strengthened'] += 1
                    
                report['details'].append({
                    'pattern_id': target_pattern_id,
                    'pattern_type': pattern_type,
                    'action': 'updated',
                    'old_confidence': old_confidence,
                    'new_confidence': new_confidence,
                    'transferability': transferability,
                    'source_pattern': source_pattern.get('id', '')
                })
            else:
                # Create new pattern in target context based on source pattern
                new_pattern_id = f"{pattern_type}_{uuid.uuid4().hex[:8]}"
                
                # Create a copy of the source pattern with adjusted confidence
                new_pattern = copy.deepcopy(source_pattern)
                new_pattern['id'] = new_pattern_id
                new_pattern['context'] = target_context
                new_pattern['confidence'] = source_pattern.get('confidence', 0.5) * transferability * 0.6
                new_pattern['correct_count'] = max(1, int(source_pattern.get('correct_count', 0) * transferability * 0.3))
                new_pattern['incorrect_count'] = max(0, int(source_pattern.get('incorrect_count', 0) * transferability * 0.3))
                new_pattern['created_by'] = 'transfer_learning'
                new_pattern['source_pattern'] = source_pattern.get('id', '')
                new_pattern['transfer_date'] = datetime.now().isoformat()
                
                # Store the new pattern
                self.long_term_memory[new_pattern_id] = new_pattern
                
                report['patterns_transferred'] += 1
                report['patterns_created'] += 1
                
                report['details'].append({
                    'pattern_id': new_pattern_id,
                    'pattern_type': pattern_type,
                    'action': 'created',
                    'confidence': new_pattern['confidence'],
                    'transferability': transferability,
                    'source_pattern': source_pattern.get('id', '')
                })
                
            total_similarity += transferability
                
        # Calculate average similarity of transferred patterns
        if report['patterns_transferred'] > 0:
            report['average_similarity'] = total_similarity / report['patterns_transferred']
            
        # Notify MetaSystems of transfer learning
        if self.meta_systems and report['patterns_transferred'] > 0:
            self.meta_systems.trigger_event('transfer_learning_applied', {
                'source': 'ArcanBrain',
                'source_context': source_context,
                'target_context': target_context,
                'patterns_transferred': report['patterns_transferred'],
                'patterns_created': report['patterns_created'],
                'average_similarity': report['average_similarity'],
                'timestamp': datetime.now().isoformat()
            })
            
        return report
            
    def _calculate_context_similarity(self, context1, context2):
        """Calculate similarity between two contexts."""
        # Extract keys that exist in both contexts
        common_keys = set(context1.keys()) & set(context2.keys())
        all_keys = set(context1.keys()) | set(context2.keys())
        
        if not all_keys:
            return 0.0
            
        # Calculate similarity
        similarity = 0.0
        
        for key in all_keys:
            if key in common_keys and context1[key] == context2[key]:
                similarity += 1.0
            elif key in common_keys:
                # Partial similarity for different values of the same key
                if isinstance(context1[key], str) and isinstance(context2[key], str):
                    # Text similarity for string values
                    similarity += self._calculate_text_similarity(context1[key], context2[key]) * 0.7
                else:
                    # Small similarity for different values
                    similarity += 0.2
        
        return similarity / len(all_keys) if all_keys else 0.0
        
    def _calculate_pattern_transferability(self, pattern_type, pattern_features, source_context, target_context):
        """Calculate how transferable a pattern is between contexts."""
        # Base transferability on context similarity
        transferability = self._calculate_context_similarity(source_context, target_context)
        
        # Different pattern types have different transferability
        type_modifiers = {
            'temporal': 0.9,  # Temporal patterns are usually highly transferable
            'form': 0.8,      # Form patterns transfer well
            'result': 0.6,    # Result patterns are moderately transferable
            'score': 0.5,     # Score patterns transfer less well
            'odds': 0.7,      # Odds patterns are fairly transferable
            'team': 0.3       # Team-specific patterns don't transfer well
        }
        
        # Apply pattern type modifier
        pattern_category = next((key for key in type_modifiers if key in pattern_type), 'default')
        type_modifier = type_modifiers.get(pattern_category, 0.7)
        transferability *= type_modifier
        
        # Consider feature similarity
        source_sport = source_context.get('sport', '')
        target_sport = target_context.get('sport', '')
        
        # Cross-sport transfers are more limited
        if source_sport != target_sport and source_sport and target_sport:
            transferability *= 0.3
            
        return min(1.0, max(0.0, transferability))
        
    def _calculate_text_similarity(self, text1, text2):
        """Calculate similarity between two text strings."""
        if not text1 or not text2:
            return 0.0
            
        # Convert to lowercase
        text1 = text1.lower()
        text2 = text2.lower()
        
        # Simple case: exact match
        if text1 == text2:
            return 1.0
            
        # Partial matching based on character overlap
        chars1 = set(text1)
        chars2 = set(text2)
        common_chars = len(chars1.intersection(chars2))
        all_chars = len(chars1.union(chars2))
        
        char_similarity = common_chars / all_chars if all_chars else 0.0
        
        # Partial matching based on word overlap
        words1 = set(text1.split())
        words2 = set(text2.split())
        common_words = len(words1.intersection(words2))
        all_words = len(words1.union(words2))
        
        word_similarity = common_words / all_words if all_words else 0.0
        
        # Combine character and word similarities (word similarity is weighted more)
        return word_similarity * 0.7 + char_similarity * 0.3
        
    def _calculate_feature_similarity(self, features1, features2):
        """Calculate similarity between pattern features."""
        if not features1 or not features2:
            return 0.0
            
        # Get all feature keys
        all_keys = set(features1.keys()) | set(features2.keys())
        if not all_keys:
            return 0.0
            
        # Calculate similarity across features
        similarity = 0.0
        
        for key in all_keys:
            if key in features1 and key in features2:
                if features1[key] == features2[key]:
                    similarity += 1.0
                elif isinstance(features1[key], (int, float)) and isinstance(features2[key], (int, float)):
                    # For numeric features, calculate relative similarity
                    max_val = max(abs(features1[key]), abs(features2[key]))
                    if max_val > 0:
                        similarity += 1.0 - min(1.0, abs(features1[key] - features2[key]) / max_val)
                elif isinstance(features1[key], str) and isinstance(features2[key], str):
                    # Text similarity for string features
                    similarity += self._calculate_text_similarity(features1[key], features2[key])
            
        return similarity / len(all_keys)
        
    def _match_context(self, pattern_context, match_context):
        """Check if a pattern context matches a match context."""
        for key, value in match_context.items():
            if key in pattern_context and pattern_context[key] != value:
                return False
        return True
            
    def _load_neural_weights(self):
        """Load trained neural weights from storage."""
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'arcanshadow.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if table exists
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='neural_weights'
            """)
            
            if cursor.fetchone():
                cursor.execute("SELECT layer, weights FROM neural_weights")
                rows = cursor.fetchall()
                
                if rows:
                    # We have weights to load
                    for layer, weights_json in rows:
                        weights = json.loads(weights_json)
                        self.synapse_strength[layer] = weights
            
            conn.close()
        except Exception as e:
            print(f"Error loading neural weights: {str(e)}")
    
    def _save_neural_state(self):
        """Save neural state including weights and memory to storage."""
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'arcanshadow.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create tables if they don't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS neural_weights (
                    layer TEXT PRIMARY KEY,
                    weights TEXT,
                    last_updated TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS neural_memory (
                    pattern_id TEXT PRIMARY KEY,
                    pattern_data TEXT,
                    confidence REAL,
                    last_updated TEXT
                )
            """)
            
            # Save synapse strengths
            for layer, weights in self.synapse_strength.items():
                weights_json = json.dumps(weights)
                cursor.execute("""
                    INSERT OR REPLACE INTO neural_weights
                    (layer, weights, last_updated)
                    VALUES (?, ?, ?)
                """, (layer, weights_json, datetime.now().isoformat()))
            
            # Save long-term memory patterns
            for pattern_id, pattern in self.long_term_memory.items():
                pattern_json = json.dumps(pattern)
                confidence = pattern.get('confidence', 0.5)
                cursor.execute("""
                    INSERT OR REPLACE INTO neural_memory
                    (pattern_id, pattern_data, confidence, last_updated)
                    VALUES (?, ?, ?, ?)
                """, (pattern_id, pattern_json, confidence, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving neural state: {str(e)}")
            return False
            
    def _register_event_handlers(self):
        """Register event handlers with MetaSystems event system."""
        # Register for odds change events
        self.meta_systems.register_event_handler(
            'odds_change_detected', 
            self._handle_odds_change_event,
            'ArcanBrain'
        )
        
        # Register for anomaly events
        self.meta_systems.register_event_handler(
            'anomaly_detected', 
            self._handle_anomaly_event,
            'ArcanBrain'
        )
        
        # Register for module activation events
        self.meta_systems.register_event_handler(
            'module_activated', 
            self._handle_module_activation_event,
            'ArcanBrain'
        )
        
        # Register for prediction results
        self.meta_systems.register_event_handler(
            'prediction_evaluated', 
            self._handle_prediction_evaluation_event,
            'ArcanBrain'
        )

    def _handle_odds_change_event(self, event_data):
        """
        Handle odds change events from ShadowOdds or other odds monitoring modules.
        
        Args:
            event_data (dict): Data about the odds change event
        """
        if not event_data:
            return
            
        match_id = event_data.get('match_id')
        if not match_id:
            return
            
        # Store in associative memory
        if 'odds_changes' not in self.associative_memory:
            self.associative_memory['odds_changes'] = {}
            
        if match_id not in self.associative_memory['odds_changes']:
            self.associative_memory['odds_changes'][match_id] = []
            
        self.associative_memory['odds_changes'][match_id].append({
            'timestamp': datetime.now().isoformat(),
            'change_data': event_data,
            'neural_response': self._generate_odds_change_response(event_data)
        })
        
    def _handle_anomaly_event(self, event_data):
        """
        Handle anomaly events from various system modules.
        
        Args:
            event_data (dict): Data about the detected anomaly
        """
        if not event_data:
            return
            
        # Add to short-term memory for pattern recognition
        self.short_term_memory.append({
            'type': 'anomaly',
            'timestamp': datetime.now().isoformat(),
            'data': event_data,
            'neural_signature': self._generate_neural_signature(event_data)
        })
        
        # Analyze for patterns with past anomalies
        pattern = self._detect_anomaly_pattern(event_data)
        
        # If significant pattern found, emit an event
        if pattern and pattern.get('significance', 0) > self.pattern_threshold:
            if self.meta_systems:
                self.meta_systems.trigger_event('pattern_recognized', {
                    'source': 'ArcanBrain',
                    'pattern_type': 'anomaly_sequence',
                    'pattern_data': pattern,
                    'related_matches': pattern.get('related_matches', [])
                })
                
    def _handle_module_activation_event(self, event_data):
        """
        Handle module activation events to adjust neural pathways.
        
        Args:
            event_data (dict): Data about module activation
        """
        module_name = event_data.get('module_name')
        if not module_name:
            return
            
        # Strengthen synaptic connections related to this module
        if module_name not in self.synapse_strength:
            self.synapse_strength[module_name] = 0.5  # Default strength
            
        # Increase connection strength (with ceiling)
        self.synapse_strength[module_name] = min(
            1.0, 
            self.synapse_strength[module_name] + 0.05
        )
        
        # Record activation in history
        self.activation_history.append({
            'module': module_name,
            'timestamp': datetime.now().isoformat(),
            'strength': self.synapse_strength[module_name]
        })
        
    def _handle_prediction_evaluation_event(self, event_data):
        """
        Handle prediction evaluation events to adapt neural learning.
        
        Args:
            event_data (dict): Data about prediction evaluation
        """
        if not event_data:
            return
            
        prediction_accuracy = event_data.get('accuracy', 0)
        match_data = event_data.get('match_data', {})
        
        # Adjust learning parameters based on prediction accuracy
        if prediction_accuracy < 0.4:  # Poor performance
            # Increase learning rate to adapt faster
            self.learning_rate = min(0.1, self.learning_rate * 1.2)
            # Reduce pattern threshold to consider more patterns
            self.pattern_threshold = max(0.5, self.pattern_threshold * 0.9)
        elif prediction_accuracy > 0.7:  # Good performance
            # Slightly decrease learning rate to stabilize
            self.learning_rate = max(0.01, self.learning_rate * 0.95)
            # Increase pattern threshold to focus on stronger patterns
            self.pattern_threshold = min(0.8, self.pattern_threshold * 1.05)
        
        # Notify MetaSystems of parameter adaptation
        if self.meta_systems:
            self.meta_systems.trigger_event('parameters_adapted', {
                'source': 'ArcanBrain',
                'learning_rate': self.learning_rate,
                'pattern_threshold': self.pattern_threshold,
                'based_on_accuracy': prediction_accuracy
            })
            
    def _generate_odds_change_response(self, change_data):
        """Generate a neural response to odds change data."""
        # This would contain complex logic in a full implementation
        return {
            'sensitivity': random.uniform(0.3, 0.9),
            'reaction_intensity': random.uniform(0.1, 1.0)
        }
        
    def _generate_neural_signature(self, event_data):
        """Generate a unique neural signature for an event."""
        # This would be a complex fingerprint in a full implementation
        event_str = json.dumps(event_data, sort_keys=True)
        signature = hashlib.md5(event_str.encode()).hexdigest()
        return signature
        
    def _detect_anomaly_pattern(self, new_anomaly):
        """Detect patterns in anomaly occurrences."""
        # This would use sophisticated pattern recognition in a full implementation
        return {
            'significance': random.uniform(0.4, 0.9),
            'type': random.choice(['sequential', 'cyclic', 'divergent']),
            'related_matches': []
        }
    
    def generate_analysis_insight(self, match_data, prediction):
        """
        Generate deep analysis insight for a match prediction based on patterns, anomalies, and context.
        
        Args:
            match_data (dict): The match information
            prediction (dict): The prediction data
            
        Returns:
            str: Detailed insight text for the match
        """
        # Extract team names
        home_team = match_data.get('home_team', 'Home Team')
        away_team = match_data.get('away_team', 'Away Team')
        
        # Initialize insights list
        insights = []
        
        # 1. Analyze team form resonance
        form_insight = False
        if 'statistical_factors' in prediction:
            for factor in prediction['statistical_factors']:
                if factor['name'].lower() in ['form analysis', 'analyse de forme'] and 'strong' in factor['value'].lower():
                    form_insight = True
                    break
        
        if form_insight:
            insights.append(f"L'analyse de forme indique une dynamique significative pour {home_team if 'home' in prediction['outcome'] else away_team}.")
        
        # 2. Check for esoteric patterns
        esoteric_insight = False
        if 'esoteric_factors' in prediction:
            for factor in prediction['esoteric_factors']:
                if 'strong' in factor['value'].lower():
                    esoteric_insight = True
                    factor_name = factor['name'].lower()
                    if 'numerical' in factor_name:
                        insights.append(f"Une forte résonance numérique est présente dans ce match, suggérant un alignement favorisant {prediction['outcome']}.")
                    elif 'karmic' in factor_name:
                        insights.append(f"Un équilibre karmique se manifeste entre ces équipes, affectant potentiellement le résultat du match.")
                    elif 'cycle' in factor_name:
                        insights.append(f"Un motif cyclique émergent influence fortement ce match, créant une opportunité de prédiction fiable.")
                    elif 'tarot' in factor_name or 'astrological' in factor_name:
                        insights.append(f"Les influences cosmiques et symboliques favorisent particulièrement {home_team if 'home' in prediction['outcome'] else away_team if 'away' in prediction['outcome'] else 'un résultat équilibré'}.")
                    break
        
        # 3. Analyze betting patterns
        betting_insight = False
        public_vs_sharp = False
        if 'odds_factors' in prediction:
            for factor in prediction['odds_factors']:
                factor_name = factor['name'].lower()
                if ('public' in factor_name and 'strong' in factor['value'].lower()):
                    betting_insight = True
                    insights.append(f"Le public penche fortement vers {home_team if 'home' not in prediction['outcome'] else away_team}, créant une opportunité de valeur contraire.")
                    public_vs_sharp = True
                elif ('sharp' in factor_name and 'strong' in factor['value'].lower()):
                    betting_insight = True
                    insights.append(f"Les parieurs professionnels montrent un intérêt significatif pour {home_team if 'home' in prediction['outcome'] else away_team if 'away' in prediction['outcome'] else 'le match nul'}.")
                elif ('trap' in factor_name and 'detect' in factor['value'].lower()):
                    betting_insight = True
                    insights.append("Un piège de cotes a été détecté dans ce match, suggérant que les bookmakers tentent de manipuler le marché.")
        
        # 4. Generate convergence insight
        if form_insight and esoteric_insight and betting_insight:
            insights.append(f"Une convergence rare de facteurs statistiques, ésotériques et de cotes soutient cette prédiction, augmentant considérablement sa fiabilité.")
        elif form_insight and esoteric_insight:
            insights.append(f"La convergence entre l'analyse de forme et les facteurs ésotériques suggère une prédiction fiable.")
        elif form_insight and betting_insight:
            insights.append(f"L'analyse de forme est confirmée par les tendances de paris, renforçant la confiance dans cette prédiction.")
        elif esoteric_insight and betting_insight:
            insights.append(f"Les facteurs ésotériques alignés avec les mouvements de cotes indiquent une opportunité cachée.")
            
        # 5. Add contrarian insight if applicable
        if prediction.get('contrarian', False):
            insights.append(f"Cette prédiction va à l'encontre du consensus général, offrant une opportunité de valeur significative si correcte.")
            
        # 6. Add value bet insight if applicable
        if prediction.get('value_bet', False):
            insights.append(f"Les cotes actuelles offrent une valeur considérable basée sur notre évaluation de la probabilité réelle.")
        
        # 7. Generate neural network insight based on pattern recognition
        outcome_probability = prediction.get('confidence', 0.5) * 100
        if outcome_probability > 80:
            insights.append(f"Le réseau neuronal détecte un schéma à haute confiance ({outcome_probability:.1f}%) pour ce résultat spécifique.")
        elif public_vs_sharp:
            insights.append(f"Le réseau neuronal a identifié une divergence significative entre l'opinion publique et celle des parieurs professionnels.")
        
        # If no insights generated, add a default one
        if not insights:
            insights.append(f"L'analyse prédictive suggère une tendance favorable pour {home_team if 'home' in prediction['outcome'] else away_team if 'away' in prediction['outcome'] else 'un match équilibré'}, mais avec des facteurs mixtes.")
        
        # Create a cohesive narrative from the insights
        if len(insights) >= 3:
            # Use only the top 3 most interesting insights
            final_text = " ".join(insights[:3])
        else:
            final_text = " ".join(insights)
            
        return final_text
            
    def generate_reflex_feedback(self, analysis_result, match_data=None):
        """
        Generate feedback for ArcanReflex based on neural analysis results.
        This enables the bidirectional communication loop between ArcanBrain and ArcanReflex.
        
        Args:
            analysis_result (dict): Results from analyze_match
            match_data (dict, optional): Match information
            
        Returns:
            dict: Feedback metrics for ArcanReflex
        """
        if not analysis_result:
            return {
                'pattern_confidence': 0.5,
                'insight_quality': 0.5,
                'anomaly_relevance': 0.5,
                'suggestion': 'Insufficient analysis data'
            }
        
        # Extract key metrics from the analysis result
        patterns = analysis_result.get('pattern_recognition', [])
        anomalies = analysis_result.get('anomalies', [])
        insights = analysis_result.get('insight_connections', [])
        neural_confidence = analysis_result.get('neural_confidence', 0.5)
        
        # Calculate pattern confidence
        pattern_confidence = 0.5  # Default moderate confidence
        if patterns:
            # Average confidence weighted by pattern strength
            total_weight = 0
            weighted_sum = 0
            for pattern in patterns:
                weight = pattern.get('confidence', 0.5)
                weighted_sum += weight * weight  # Square to emphasize stronger patterns
                total_weight += weight
                
            if total_weight > 0:
                pattern_confidence = min(1.0, weighted_sum / total_weight)
        
        # Calculate insight quality
        insight_quality = 0.5  # Default moderate quality
        if insights:
            # Base quality on insight confidence and coherence
            insight_confidences = [insight.get('confidence', 0.5) for insight in insights]
            avg_confidence = sum(insight_confidences) / len(insight_confidences) if insight_confidences else 0.5
            
            # Higher quality if more insights are present (up to a point)
            insight_count_factor = min(1.0, len(insights) / 5)  # Cap at 5 insights
            
            # Combine factors
            insight_quality = (avg_confidence * 0.7) + (insight_count_factor * 0.3)
        
        # Calculate anomaly relevance
        anomaly_relevance = 0.5  # Default moderate relevance
        if anomalies:
            # Base relevance on anomaly scores and count
            anomaly_scores = [anomaly.get('score', 0.5) for anomaly in anomalies]
            avg_score = sum(anomaly_scores) / len(anomaly_scores) if anomaly_scores else 0.5
            
            # Higher relevance if more anomalies are present
            anomaly_count_factor = min(1.0, len(anomalies) / 3)  # Cap at 3 anomalies
            
            # Combine factors
            anomaly_relevance = (avg_score * 0.6) + (anomaly_count_factor * 0.4)
        
        # Generate architectural adaptation suggestion
        suggestion = self._generate_adaptation_suggestion(
            pattern_confidence, 
            insight_quality, 
            anomaly_relevance,
            neural_confidence
        )
        
        # Return comprehensive feedback
        return {
            'pattern_confidence': pattern_confidence,
            'insight_quality': insight_quality,
            'anomaly_relevance': anomaly_relevance,
            'neural_confidence': neural_confidence,
            'pattern_count': len(patterns),
            'anomaly_count': len(anomalies),
            'insight_count': len(insights),
            'suggestion': suggestion,
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_adaptation_suggestion(self, pattern_confidence, insight_quality, anomaly_relevance, neural_confidence):
        """
        Generate architectural adaptation suggestions for ArcanReflex based on analysis metrics.
        
        Args:
            pattern_confidence (float): Confidence in detected patterns
            insight_quality (float): Quality of generated insights
            anomaly_relevance (float): Relevance of detected anomalies
            neural_confidence (float): Overall neural confidence
            
        Returns:
            str: Adaptation suggestion for ArcanReflex
        """
        # Determine the dominant feature of the analysis
        features = {
            'Pattern Recognition': pattern_confidence,
            'Insight Generation': insight_quality,
            'Anomaly Detection': anomaly_relevance
        }
        
        dominant_feature = max(features.items(), key=lambda x: x[1])
        
        # Generate suggestion based on the dominant feature and overall confidence
        if neural_confidence < 0.4:
            if dominant_feature[0] == 'Pattern Recognition':
                return "Low confidence with pattern focus suggests activating more historical modules for context enrichment"
            elif dominant_feature[0] == 'Insight Generation':
                return "Low confidence with insight focus suggests reducing evaluation threshold to explore more module combinations"
            else:  # Anomaly Detection
                return "Low confidence with anomaly focus suggests broadening module activation to triangulate unusual signals"
        elif neural_confidence > 0.75:
            if dominant_feature[0] == 'Pattern Recognition':
                return "High confidence with pattern focus suggests increasing evaluation standards to refine module selection"
            elif dominant_feature[0] == 'Insight Generation':
                return "High confidence with insight focus suggests extending memory retention to preserve valuable patterns"
            else:  # Anomaly Detection
                return "High confidence with anomaly focus suggests isolating specialized modules for anomaly validation"
        else:
            # Moderate confidence - general suggestions
            if pattern_confidence > 0.7 and anomaly_relevance > 0.7:
                return "Strong pattern-anomaly contrast suggests activation pattern alternation for deeper exploration"
            elif insight_quality < 0.4:
                return "Moderate confidence with weak insights suggests module diversification to generate novel connections"
            else:
                return "Balanced analysis suggests maintaining current module activation strategy"