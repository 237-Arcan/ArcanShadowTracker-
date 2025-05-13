"""
ArcanReflex - Self-evaluation and adaptive mechanism for ArcanShadow.
Provides real-time evaluation and adjustment of active modules based on performance.
"""

import numpy as np
import random
import time
from datetime import datetime, timedelta
import json
import os
import sqlite3

class ArcanReflex:
    """
    ArcanReflex - Self-evaluation and adaptation mechanism for ArcanShadow.
    Continuously monitors module performance and adjusts activation patterns.
    """
    
    def __init__(self, arcan_x=None, shadow_odds=None, convergence=None, meta_systems=None, arcan_brain=None):
        """
        Initialize the ArcanReflex module with references to other system components.
        
        Args:
            arcan_x: ArcanX module instance
            shadow_odds: ShadowOdds module instance
            convergence: Convergence module instance
            meta_systems: MetaSystems module instance
            arcan_brain: ArcanBrain module instance
        """
        # Store module references
        self.arcan_x = arcan_x
        self.shadow_odds = shadow_odds
        self.convergence = convergence
        self.meta_systems = meta_systems
        self.arcan_brain = arcan_brain  # New reference to ArcanBrain
        
        # Initialize internal components
        self.reflex_eval = ReflexEval()
        self.reflex_switch = ReflexSwitch()
        self.reflex_memory = ReflexMemory()
        
        # Load historical performance data if available
        self._load_performance_data()
        
        # Configuration
        self.evaluation_threshold = 0.6  # Minimum score to keep a module active
        self.learning_rate = 0.05  # Rate at which module weights are adjusted
        self.memory_retention = 90  # Days to retain performance memory
        
        # ArcanBrain parameter control ranges (meta-cognition)
        self.brain_param_ranges = {
            'learning_rate': (0.01, 0.1),
            'pattern_threshold': (0.45, 0.85),
            'anomaly_threshold': (0.7, 0.95),
            'insight_temperature': (0.4, 0.9)
        }
        
        # Current state
        self.active_modules = {}  # Currently active modules
        self.module_performance = {}  # Recent performance of modules
        self.brain_param_history = []  # History of ArcanBrain parameter adjustments
        self.pattern_library = {}  # Identified effective patterns
        
        # Performance metrics
        self.system_accuracy = 0.0
        self.module_contribution = {}
    
    def evaluate_system_performance(self, prediction_results=None):
        """
        Evaluate the overall system performance and identify strengths/weaknesses.
        
        Args:
            prediction_results (dict, optional): Results of recent predictions
            
        Returns:
            dict: System performance evaluation
        """
        # Get module performance data
        module_eval = self.reflex_eval.evaluate_modules(
            self.active_modules, 
            prediction_results
        )
        
        # Update internal state with new evaluations
        self.module_performance.update(module_eval['module_scores'])
        
        # Identify underperforming modules
        underperforming = []
        for module, score in module_eval['module_scores'].items():
            if score < self.evaluation_threshold:
                underperforming.append(module)
                
        # Take action on underperforming modules
        if underperforming:
            deactivation_candidates = self.reflex_switch.suggest_deactivations(
                underperforming, 
                self.module_performance,
                prediction_results
            )
            
            # Store this information for future reference
            for module in deactivation_candidates:
                self.active_modules[module] = False
        
        # Calculate system-wide performance
        if prediction_results:
            correct_predictions = sum(1 for result in prediction_results if result.get('correct', False))
            total_predictions = len(prediction_results)
            accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
            self.system_accuracy = (self.system_accuracy * 0.7) + (accuracy * 0.3)  # Weighted average
        
        # Update pattern memory
        if prediction_results and any(result.get('correct', False) for result in prediction_results):
            # Only store patterns from correct predictions
            correct_patterns = [
                {
                    'active_modules': result.get('active_modules', []),
                    'match_data': result.get('match_data', {}),
                    'confidence': result.get('confidence', 0)
                }
                for result in prediction_results if result.get('correct', False)
            ]
            
            self.reflex_memory.store_patterns(correct_patterns)
        
        # Generate summary report
        summary = {
            'system_accuracy': self.system_accuracy,
            'module_performance': self.module_performance,
            'underperforming_modules': underperforming,
            'deactivation_candidates': deactivation_candidates if 'deactivation_candidates' in locals() else [],
            'performance_improvement': module_eval.get('improvement', 0),
            'timestamp': datetime.now().isoformat()
        }
        
        # Save updated performance data
        self._save_performance_data()
        
        return summary
    
    def optimize_module_activation(self, match_data):
        """
        Optimize which modules should be active for a specific match.
        
        Args:
            match_data (dict): Information about the match
            
        Returns:
            dict: Optimized module activation configuration
        """
        # First, check if we have memory patterns that match this type of match
        relevant_patterns = self.reflex_memory.find_relevant_patterns(match_data)
        
        # Determine base activation plan
        if relevant_patterns:
            # Use the most successful historical pattern
            base_config = relevant_patterns[0].get('active_modules', [])
            match_similarity = relevant_patterns[0].get('similarity', 0)
            
            # Record the source of our decision
            activation_source = 'historical_pattern'
            pattern_confidence = relevant_patterns[0].get('confidence', 0)
        else:
            # No relevant historical pattern, use meta-systems default
            if self.meta_systems:
                grid_sync_result = self.meta_systems.grid_sync_alpha(match_data)
                base_config = grid_sync_result.get('activated_modules', [])
                activation_source = 'grid_sync_default'
                pattern_confidence = 0.5  # Medium confidence
            else:
                # Fallback to a basic configuration if meta_systems isn't available
                base_config = self._get_default_activation()
                activation_source = 'default_fallback'
                pattern_confidence = 0.4  # Lower confidence
        
        # Apply RefleXSwitch optimizations to the base configuration
        optimized_config = self.reflex_switch.optimize_activation(
            base_config,
            match_data,
            self.module_performance
        )
        
        # Record the new active module configuration
        self.active_modules = {module: True for module in optimized_config}
        
        result = {
            'active_modules': optimized_config,
            'activation_source': activation_source,
            'pattern_confidence': pattern_confidence,
            'modifications': list(set(optimized_config) - set(base_config)),
            'timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def track_prediction_outcome(self, prediction, actual_outcome, modules_used):
        """
        Track the outcome of a prediction to update module performance metrics.
        
        Args:
            prediction (dict): The prediction that was made
            actual_outcome (dict): The actual outcome that occurred
            modules_used (list): Modules that were used in the prediction
            
        Returns:
            dict: Updated performance metrics
        """
        # Determine if prediction was correct
        correct = self._compare_prediction_outcome(prediction, actual_outcome)
        
        # Prepare result data
        result_data = {
            'correct': correct,
            'active_modules': modules_used,
            'match_data': prediction.get('match_data', {}),
            'confidence': prediction.get('confidence', 0),
            'factors': prediction.get('factors', []),
            'timestamp': datetime.now().isoformat()
        }
        
        # Update module performance based on this outcome
        self.reflex_eval.track_prediction_result(result_data)
        
        # If prediction was correct and high confidence, store the pattern
        if correct and prediction.get('confidence', 0) > 0.7:
            self.reflex_memory.store_patterns([result_data])
        
        return {
            'tracked': True,
            'prediction_correct': correct,
            'modules_credited': modules_used,
            'timestamp': datetime.now().isoformat()
        }
    
    def suggest_new_modules(self, performance_data=None):
        """
        Suggest new modules that could be created to address gaps in system performance.
        
        Args:
            performance_data (dict, optional): Recent performance data
            
        Returns:
            dict: Suggestions for new modules
        """
        # This would connect to D-Forge in a full implementation
        # For now, we'll just provide suggestions based on performance gaps
        
        suggestions = []
        
        # Check if we've been struggling with specific types of matches
        problem_leagues = self._identify_problem_leagues(performance_data)
        for league in problem_leagues:
            suggestions.append({
                'module_type': 'league_specialist',
                'target': league,
                'rationale': f"Performance in {league} has been below average by {problem_leagues[league]:.1%}",
                'priority': min(1.0, problem_leagues[league] * 2)
            })
        
        # Check if we're struggling with specific bet types
        problem_bet_types = self._identify_problem_bet_types(performance_data)
        for bet_type in problem_bet_types:
            suggestions.append({
                'module_type': 'bet_specialist',
                'target': bet_type,
                'rationale': f"Performance in {bet_type} has been below average by {problem_bet_types[bet_type]:.1%}",
                'priority': min(1.0, problem_bet_types[bet_type] * 2)
            })
        
        # Sort by priority
        suggestions.sort(key=lambda x: x.get('priority', 0), reverse=True)
        
        return {
            'suggestions': suggestions,
            'timestamp': datetime.now().isoformat()
        }
    
    def _compare_prediction_outcome(self, prediction, actual_outcome):
        """Helper to compare a prediction with the actual outcome."""
        # In a real system, this would have complex logic for different bet types
        # For now, we'll just do a simple comparison
        pred_outcome = prediction.get('outcome', '')
        actual = actual_outcome.get('outcome', '')
        
        return pred_outcome == actual
    
    def _get_default_activation(self):
        """Get a default module activation configuration."""
        # Basic set of modules that should generally work well together
        return [
            # ArcanX modules
            'NumeriCode', 'GematriaPulse', 'KarmicFlow',
            # ShadowOdds modules
            'LineTrap', 'BetPulse', 'MarketEcho',
            # Convergence modules
            'ConvergiaCore', 'MirrorPhase'
        ]
    
    def _identify_problem_leagues(self, performance_data):
        """Identify leagues where the system has been struggling."""
        # Simplified implementation for demonstration
        problem_leagues = {}
        
        # In a real system, this would analyze actual performance data
        if performance_data and 'league_performance' in performance_data:
            for league, data in performance_data['league_performance'].items():
                if data['accuracy'] < self.system_accuracy - 0.1:
                    problem_leagues[league] = self.system_accuracy - data['accuracy']
        
        return problem_leagues
    
    def _identify_problem_bet_types(self, performance_data):
        """Identify bet types where the system has been struggling."""
        # Simplified implementation for demonstration
        problem_bet_types = {}
        
        # In a real system, this would analyze actual performance data
        if performance_data and 'bet_type_performance' in performance_data:
            for bet_type, data in performance_data['bet_type_performance'].items():
                if data['accuracy'] < self.system_accuracy - 0.15:
                    problem_bet_types[bet_type] = self.system_accuracy - data['accuracy']
        
        return problem_bet_types
    
    def _load_performance_data(self):
        """Load performance data from persistent storage."""
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'arcanshadow.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if table exists
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='module_performance'
            """)
            
            if cursor.fetchone():
                cursor.execute("SELECT module_name, performance, last_updated FROM module_performance")
                rows = cursor.fetchall()
                
                for row in rows:
                    module_name, performance, _ = row
                    self.module_performance[module_name] = float(performance)
            
            conn.close()
        except Exception as e:
            print(f"Error loading performance data: {str(e)}")
    
    def _save_performance_data(self):
        """Save performance data to persistent storage."""
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'arcanshadow.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS module_performance (
                    module_name TEXT PRIMARY KEY,
                    performance REAL,
                    last_updated TEXT
                )
            """)
            
            # Save module performance data
            for module, performance in self.module_performance.items():
                cursor.execute("""
                    INSERT OR REPLACE INTO module_performance (module_name, performance, last_updated)
                    VALUES (?, ?, ?)
                """, (module, performance, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error saving performance data: {str(e)}")


class ReflexEval:
    """
    ReflexEval component - Evaluates the performance and relevance of each module.
    """
    
    def __init__(self):
        """Initialize the ReflexEval component."""
        self.module_scores = {}  # Current performance scores for each module
        self.historical_scores = {}  # Historical performance tracking
        self.evaluation_window = 20  # Number of predictions to consider for evaluation
        self.recent_results = []  # Recent prediction results for evaluation
    
    def evaluate_modules(self, active_modules, prediction_results=None):
        """
        Evaluate the performance of all active modules based on prediction results.
        
        Args:
            active_modules (dict): Currently active modules
            prediction_results (list, optional): Recent prediction results
            
        Returns:
            dict: Evaluation results with module scores
        """
        # Update our record of recent results
        if prediction_results:
            self.recent_results = (self.recent_results + prediction_results)[-self.evaluation_window:]
        
        # If we don't have enough data, use existing scores
        if len(self.recent_results) < 3:
            return {
                'module_scores': self.module_scores.copy(),
                'improvement': 0
            }
        
        # Calculate new scores based on contribution to correct predictions
        new_scores = {}
        total_correct = sum(1 for result in self.recent_results if result.get('correct', False))
        
        # Only analyze if we have some correct predictions
        if total_correct > 0:
            # Count module appearances in correct and incorrect predictions
            module_correct = {}
            module_incorrect = {}
            
            for result in self.recent_results:
                is_correct = result.get('correct', False)
                modules = result.get('active_modules', [])
                
                for module in modules:
                    if is_correct:
                        module_correct[module] = module_correct.get(module, 0) + 1
                    else:
                        module_incorrect[module] = module_incorrect.get(module, 0) + 1
            
            # Calculate scores based on contribution to correct predictions
            for module in set(list(module_correct.keys()) + list(module_incorrect.keys())):
                correct = module_correct.get(module, 0)
                incorrect = module_incorrect.get(module, 0)
                total = correct + incorrect
                
                if total > 0:
                    # Base score is the ratio of correct to total uses
                    base_score = correct / total
                    
                    # Adjust for the module's contribution to overall correct predictions
                    contribution = correct / total_correct if total_correct > 0 else 0
                    
                    # Final score is a weighted combination
                    new_scores[module] = (base_score * 0.7) + (contribution * 0.3)
                else:
                    # If the module hasn't been used, keep its existing score
                    new_scores[module] = self.module_scores.get(module, 0.5)
        else:
            # If no correct predictions, retain existing scores
            new_scores = self.module_scores.copy()
        
        # Calculate system improvement
        old_avg_score = sum(self.module_scores.values()) / max(1, len(self.module_scores))
        new_avg_score = sum(new_scores.values()) / max(1, len(new_scores))
        improvement = new_avg_score - old_avg_score
        
        # Update historical tracking
        for module, score in new_scores.items():
            if module not in self.historical_scores:
                self.historical_scores[module] = []
            
            self.historical_scores[module].append({
                'score': score,
                'timestamp': datetime.now().isoformat()
            })
            
            # Keep history manageable
            if len(self.historical_scores[module]) > 100:
                self.historical_scores[module] = self.historical_scores[module][-100:]
        
        # Update internal state
        self.module_scores = new_scores
        
        return {
            'module_scores': new_scores,
            'improvement': improvement
        }
    
    def track_prediction_result(self, result_data):
        """
        Track the result of a single prediction for module evaluation.
        
        Args:
            result_data (dict): Data about the prediction result
            
        Returns:
            bool: True if tracking was successful
        """
        self.recent_results.append(result_data)
        
        # Keep the recent results list manageable
        if len(self.recent_results) > self.evaluation_window:
            self.recent_results = self.recent_results[-self.evaluation_window:]
        
        return True
    
    def get_module_trend(self, module_name, days=30):
        """
        Get the performance trend for a specific module.
        
        Args:
            module_name (str): Name of the module
            days (int): Number of days to look back
            
        Returns:
            dict: Trend analysis for the module
        """
        if module_name not in self.historical_scores:
            return {
                'trend': 'unknown',
                'data_points': 0
            }
        
        # Filter for entries within the time window
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_scores = [
            entry for entry in self.historical_scores[module_name] 
            if datetime.fromisoformat(entry['timestamp']) > cutoff_date
        ]
        
        if len(recent_scores) < 2:
            return {
                'trend': 'stable',
                'data_points': len(recent_scores)
            }
        
        # Calculate trend
        scores = [entry['score'] for entry in recent_scores]
        
        # Simple linear regression
        x = list(range(len(scores)))
        x_mean = sum(x) / len(x)
        y_mean = sum(scores) / len(scores)
        
        numerator = sum((x[i] - x_mean) * (scores[i] - y_mean) for i in range(len(scores)))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(len(scores)))
        
        slope = numerator / denominator if denominator != 0 else 0
        
        # Determine trend based on slope
        if abs(slope) < 0.001:
            trend = 'stable'
        elif slope > 0:
            trend = 'improving' if slope > 0.005 else 'slightly_improving'
        else:
            trend = 'declining' if slope < -0.005 else 'slightly_declining'
        
        return {
            'trend': trend,
            'slope': slope,
            'data_points': len(recent_scores),
            'current_score': scores[-1],
            'start_score': scores[0]
        }


class ReflexSwitch:
    """
    ReflexSwitch component - Manages module activation and deactivation based on performance.
    """
    
    def __init__(self):
        """Initialize the ReflexSwitch component."""
        self.deactivated_modules = {}  # Modules that have been deactivated with timestamps
        self.deactivation_threshold = 0.4  # Performance threshold for deactivation
        self.reactivation_threshold = 0.6  # Performance threshold for reactivation
        self.deactivation_period = 10  # Minimum deactivation period in days
    
    def suggest_deactivations(self, underperforming_modules, module_performance, prediction_results=None):
        """
        Suggest modules to deactivate based on performance.
        
        Args:
            underperforming_modules (list): Modules that are underperforming
            module_performance (dict): Performance metrics for all modules
            prediction_results (list, optional): Recent prediction results
            
        Returns:
            list: Modules that should be deactivated
        """
        deactivation_candidates = []
        
        for module in underperforming_modules:
            # Check if performance is below threshold
            if module_performance.get(module, 0.5) < self.deactivation_threshold:
                # Check if it's a critical module that shouldn't be deactivated
                if not self._is_critical_module(module):
                    deactivation_candidates.append(module)
                    
                    # Record the deactivation
                    self.deactivated_modules[module] = {
                        'timestamp': datetime.now().isoformat(),
                        'reason': 'performance_below_threshold',
                        'score': module_performance.get(module, 0.5)
                    }
        
        return deactivation_candidates
    
    def optimize_activation(self, base_config, match_data, module_performance):
        """
        Optimize the module activation configuration for a specific match.
        
        Args:
            base_config (list): Base module activation configuration
            match_data (dict): Information about the match
            module_performance (dict): Performance metrics for all modules
            
        Returns:
            list: Optimized module activation configuration
        """
        optimized_config = base_config.copy()
        
        # Check if any deactivated modules have served their time
        current_time = datetime.now()
        for module, data in list(self.deactivated_modules.items()):
            deactivation_time = datetime.fromisoformat(data['timestamp'])
            days_deactivated = (current_time - deactivation_time).days
            
            # If it's been deactivated long enough and has a decent score now, reactivate
            if days_deactivated >= self.deactivation_period:
                current_score = module_performance.get(module, 0.5)
                if current_score >= self.reactivation_threshold:
                    # The module is eligible for reactivation
                    if self._is_suitable_for_match(module, match_data):
                        if module not in optimized_config:
                            optimized_config.append(module)
                        # Remove from deactivated list
                        del self.deactivated_modules[module]
        
        # Remove any modules that should be deactivated
        optimized_config = [
            module for module in optimized_config
            if module not in self.deactivated_modules
        ]
        
        # Check if specialized modules should be added for this match
        league = match_data.get('league', '')
        sport = match_data.get('sport', '')
        
        # For Asian leagues, add EasternGate if available
        if 'J-League' in league or 'K-League' in league or 'Chinese Super League' in league:
            eastern_gate_modules = self._get_eastern_gate_modules(match_data)
            for module in eastern_gate_modules:
                if module not in optimized_config and module not in self.deactivated_modules:
                    optimized_config.append(module)
        
        # For derbies, ensure fan sentiment monitoring
        is_derby = self._is_derby_match(match_data)
        if is_derby and 'FanSentimentMonitor' not in optimized_config:
            if 'FanSentimentMonitor' not in self.deactivated_modules:
                optimized_config.append('FanSentimentMonitor')
        
        # For important matches, add more modules for thoroughness
        if self._is_important_match(match_data):
            for module in self._get_additional_modules_for_important_match(sport):
                if module not in optimized_config and module not in self.deactivated_modules:
                    optimized_config.append(module)
        
        return optimized_config
    
    def manually_deactivate(self, module_name, reason='manual'):
        """
        Manually deactivate a module.
        
        Args:
            module_name (str): Name of the module to deactivate
            reason (str): Reason for manual deactivation
            
        Returns:
            bool: True if deactivation was successful
        """
        self.deactivated_modules[module_name] = {
            'timestamp': datetime.now().isoformat(),
            'reason': f'manual_{reason}',
            'score': 0
        }
        
        return True
    
    def manually_reactivate(self, module_name):
        """
        Manually reactivate a module.
        
        Args:
            module_name (str): Name of the module to reactivate
            
        Returns:
            bool: True if reactivation was successful
        """
        if module_name in self.deactivated_modules:
            del self.deactivated_modules[module_name]
            return True
        
        return False
    
    def _is_critical_module(self, module_name):
        """Check if a module is critical and should not be deactivated."""
        critical_modules = [
            'ConvergiaCore', 'NumeriCode', 'LineTrap'  # Example critical modules
        ]
        
        return module_name in critical_modules
    
    def _is_suitable_for_match(self, module_name, match_data):
        """Check if a module is suitable for a specific match type."""
        # Simple examples of match suitability
        if module_name == 'SetPieceThreatEvaluator' and match_data.get('sport', '') != 'Football':
            return False
            
        if module_name == 'YouthImpactAnalyzer' and not match_data.get('has_youth_players', False):
            return False
            
        return True
    
    def _is_derby_match(self, match_data):
        """Check if a match is a derby or rivalry match."""
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # This would be much more sophisticated in a real implementation
        # For now, just check if the teams are from the same city/region
        if home_team and away_team:
            # Example derby check: teams from same city often share part of name
            home_parts = home_team.lower().split()
            away_parts = away_team.lower().split()
            
            for part in home_parts:
                if part in away_parts and len(part) > 3:  # Avoid matching on common words
                    return True
            
            # Check explicit rivalries (would be from a database in real system)
            rivalries = [
                {'team1': 'Manchester United', 'team2': 'Manchester City'},
                {'team1': 'Liverpool', 'team2': 'Everton'},
                {'team1': 'Arsenal', 'team2': 'Tottenham'},
                {'team1': 'Barcelona', 'team2': 'Real Madrid'},
                {'team1': 'Boca Juniors', 'team2': 'River Plate'}
            ]
            
            for rivalry in rivalries:
                if (rivalry['team1'] in home_team and rivalry['team2'] in away_team) or \
                   (rivalry['team2'] in home_team and rivalry['team1'] in away_team):
                    return True
        
        return False
    
    def _is_important_match(self, match_data):
        """Check if a match is important (cup final, title decider, etc.)."""
        # This would be more sophisticated in a real implementation
        important_indicators = [
            'final', 'semi final', 'title decider', 'relegation battle',
            'promotion', 'qualifier', 'championship'
        ]
        
        match_description = match_data.get('description', '').lower()
        
        for indicator in important_indicators:
            if indicator in match_description:
                return True
        
        return False
    
    def _get_eastern_gate_modules(self, match_data):
        """Get appropriate EasternGate modules for Asian competitions."""
        # These would be specialized modules for Asian leagues
        return ['ElementalBalance', 'LocalRitualImpact', 'LunarPhaseTracker']
    
    def _get_additional_modules_for_important_match(self, sport):
        """Get additional modules to activate for important matches."""
        # This would be more sophisticated in a real implementation
        if sport == 'Football':
            return ['ClutchTimeScanner', 'KarmicFlow', 'PressurePointsTracker']
        elif sport == 'Basketball':
            return ['MomentumWaveAnalyzer', 'ClutchPerformanceIndex']
        elif sport == 'Tennis':
            return ['BreakPointAnalyzer', 'MentalFortitudeScanner']
        else:
            return ['MomentumShiftTracker']


class ReflexMemory:
    """
    ReflexMemory component - Stores and retrieves effective patterns for future use.
    """
    
    def __init__(self):
        """Initialize the ReflexMemory component."""
        self.pattern_library = []  # Library of successful patterns
        self.max_patterns = 1000  # Maximum number of patterns to store
        self.similarity_threshold = 0.6  # Threshold for pattern similarity
        self.confidence_boost = 0.1  # Confidence boost for matched patterns
    
    def store_patterns(self, patterns):
        """
        Store new patterns in the pattern library.
        
        Args:
            patterns (list): Patterns to store
            
        Returns:
            int: Number of patterns stored
        """
        stored_count = 0
        
        for pattern in patterns:
            # Skip if pattern doesn't have required fields
            if 'active_modules' not in pattern or 'match_data' not in pattern:
                continue
                
            # Check if pattern is similar to existing ones
            is_similar = False
            for existing in self.pattern_library:
                similarity = self._calculate_pattern_similarity(pattern, existing)
                if similarity > self.similarity_threshold:
                    # Update the existing pattern's confidence
                    existing_confidence = existing.get('confidence', 0.5)
                    new_confidence = pattern.get('confidence', 0.5)
                    
                    # Weighted average, favoring higher confidence
                    if new_confidence > existing_confidence:
                        updated_confidence = (existing_confidence * 0.3) + (new_confidence * 0.7)
                    else:
                        updated_confidence = (existing_confidence * 0.7) + (new_confidence * 0.3)
                    
                    existing['confidence'] = updated_confidence
                    existing['use_count'] = existing.get('use_count', 1) + 1
                    existing['last_used'] = datetime.now().isoformat()
                    
                    is_similar = True
                    break
            
            # If not similar to any existing pattern, add it
            if not is_similar:
                pattern['use_count'] = 1
                pattern['first_used'] = datetime.now().isoformat()
                pattern['last_used'] = datetime.now().isoformat()
                self.pattern_library.append(pattern)
                stored_count += 1
        
        # Ensure we don't exceed the maximum pattern count
        if len(self.pattern_library) > self.max_patterns:
            # Sort by combination of confidence and recency
            self.pattern_library.sort(key=lambda p: 
                (p.get('confidence', 0) * 0.7) + 
                (p.get('use_count', 1) / 10 * 0.3), 
                reverse=True
            )
            
            # Keep the top patterns
            self.pattern_library = self.pattern_library[:self.max_patterns]
        
        return stored_count
    
    def find_relevant_patterns(self, match_data):
        """
        Find patterns relevant to a specific match.
        
        Args:
            match_data (dict): Information about the match
            
        Returns:
            list: Relevant patterns with similarity scores
        """
        relevant_patterns = []
        
        for pattern in self.pattern_library:
            pattern_match_data = pattern.get('match_data', {})
            
            # Calculate match similarity
            similarity = self._calculate_match_similarity(match_data, pattern_match_data)
            
            if similarity > self.similarity_threshold:
                # Create a copy of the pattern with the similarity score
                relevant_pattern = pattern.copy()
                relevant_pattern['similarity'] = similarity
                
                # Add confidence boost based on similarity
                confidence_boost = self.confidence_boost * similarity
                relevant_pattern['boosted_confidence'] = min(1.0, 
                    relevant_pattern.get('confidence', 0.5) + confidence_boost
                )
                
                relevant_patterns.append(relevant_pattern)
        
        # Sort by similarity and confidence
        relevant_patterns.sort(
            key=lambda p: (p.get('similarity', 0) * 0.6) + (p.get('confidence', 0) * 0.4),
            reverse=True
        )
        
        return relevant_patterns
    
    def get_pattern_stats(self):
        """
        Get statistics about the pattern library.
        
        Returns:
            dict: Pattern library statistics
        """
        if not self.pattern_library:
            return {
                'total_patterns': 0,
                'avg_confidence': 0,
                'avg_use_count': 0
            }
        
        total = len(self.pattern_library)
        avg_confidence = sum(p.get('confidence', 0) for p in self.pattern_library) / total
        avg_use_count = sum(p.get('use_count', 1) for p in self.pattern_library) / total
        
        # Count patterns by sport
        sport_counts = {}
        for pattern in self.pattern_library:
            sport = pattern.get('match_data', {}).get('sport', 'Unknown')
            sport_counts[sport] = sport_counts.get(sport, 0) + 1
        
        return {
            'total_patterns': total,
            'avg_confidence': avg_confidence,
            'avg_use_count': avg_use_count,
            'sport_distribution': sport_counts
        }
    
    def prune_old_patterns(self, days_threshold=90):
        """
        Remove old patterns that haven't been used recently.
        
        Args:
            days_threshold (int): Number of days of inactivity before pruning
            
        Returns:
            int: Number of patterns pruned
        """
        if not self.pattern_library:
            return 0
        
        cutoff_date = datetime.now() - timedelta(days=days_threshold)
        initial_count = len(self.pattern_library)
        
        # Keep only patterns used after the cutoff date
        self.pattern_library = [
            pattern for pattern in self.pattern_library
            if datetime.fromisoformat(pattern.get('last_used', datetime.now().isoformat())) > cutoff_date
        ]
        
        return initial_count - len(self.pattern_library)
    
    def _calculate_pattern_similarity(self, pattern1, pattern2):
        """Calculate the similarity between two patterns."""
        # Calculate similarity between active modules
        modules1 = set(pattern1.get('active_modules', []))
        modules2 = set(pattern2.get('active_modules', []))
        
        if not modules1 or not modules2:
            return 0
        
        module_similarity = len(modules1.intersection(modules2)) / max(len(modules1), len(modules2))
        
        # Calculate similarity between match data
        match_similarity = self._calculate_match_similarity(
            pattern1.get('match_data', {}),
            pattern2.get('match_data', {})
        )
        
        # Weighted combination
        return (module_similarity * 0.6) + (match_similarity * 0.4)
    
    def _calculate_match_similarity(self, match1, match2):
        """Calculate the similarity between two match data dictionaries."""
        if not match1 or not match2:
            return 0
        
        similarity_score = 0
        total_weight = 0
        
        # Sport (high weight)
        if 'sport' in match1 and 'sport' in match2:
            weight = 3.0
            if match1['sport'] == match2['sport']:
                similarity_score += weight
            total_weight += weight
        
        # League (high weight)
        if 'league' in match1 and 'league' in match2:
            weight = 2.5
            if match1['league'] == match2['league']:
                similarity_score += weight
            total_weight += weight
        
        # Team similarity (medium-high weight)
        if 'home_team' in match1 and 'home_team' in match2:
            weight = 2.0
            # Check exact match
            if match1['home_team'] == match2['home_team']:
                similarity_score += weight
            # Check partial match
            elif match1['home_team'] in match2['home_team'] or match2['home_team'] in match1['home_team']:
                similarity_score += weight * 0.5
            total_weight += weight
        
        if 'away_team' in match1 and 'away_team' in match2:
            weight = 2.0
            # Check exact match
            if match1['away_team'] == match2['away_team']:
                similarity_score += weight
            # Check partial match
            elif match1['away_team'] in match2['away_team'] or match2['away_team'] in match1['away_team']:
                similarity_score += weight * 0.5
            total_weight += weight
        
        # Form similarity (medium weight)
        if 'home_form' in match1 and 'home_form' in match2:
            weight = 1.5
            form1 = match1['home_form']
            form2 = match2['home_form']
            
            # Calculate form similarity
            if isinstance(form1, str) and isinstance(form2, str):
                form_similarity = sum(1 for a, b in zip(form1, form2) if a == b) / max(len(form1), len(form2))
                similarity_score += weight * form_similarity
            total_weight += weight
        
        # Match importance (medium weight)
        if 'is_important' in match1 and 'is_important' in match2:
            weight = 1.5
            if match1['is_important'] == match2['is_important']:
                similarity_score += weight
            total_weight += weight
        
        # Normalize to 0-1 range
        if total_weight > 0:
            return similarity_score / total_weight
        else:
            return 0