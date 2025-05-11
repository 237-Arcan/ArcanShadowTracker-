import numpy as np
from datetime import datetime
import random

class Convergence:
    """
    Convergence module - Central integration point for ArcanShadow's prediction system.
    Combines outputs from ArcanX and ShadowOdds to generate final predictions.
    """
    
    def __init__(self):
        """Initialize the Convergence module with necessary components."""
        self.submodules = {
            'ConvergiaCore': self.convergia_core,
            'MirrorPhase': self.mirror_phase,
            'MomentumShiftTracker': self.momentum_shift_tracker,
            'CaptainSwitch': self.captain_switch,
            'YouthImpactAnalyzer': self.youth_impact_analyzer,
            'LateSurgeDetector': self.late_surge_detector,
            'SetPieceThreatEvaluator': self.set_piece_threat_evaluator,
            'FanSentimentMonitor': self.fan_sentiment_monitor
        }
        
        # Initialize correlation matrix for factor weighting
        self.correlation_matrix = self._initialize_correlation_matrix()
        
        # Cache for results to avoid redundant calculations
        self.cache = {}
    
    def generate_prediction(self, match_data, arcan_x_results, shadow_odds_results):
        """
        Main method to generate final prediction by combining ArcanX and ShadowOdds outputs.
        
        Args:
            match_data (dict): Match information
            arcan_x_results (dict): Results from ArcanX module
            shadow_odds_results (dict): Results from ShadowOdds module
            
        Returns:
            dict: Final prediction with confidence score and factors
        """
        # Generate a unique hash for this match to ensure consistent results
        match_key = f"{match_data.get('home_team', '')}_{match_data.get('away_team', '')}_{match_data.get('date', datetime.now())}"
        match_hash = hash(match_key)
        # Ensure the seed is within valid range (0 to 2^32 - 1)
        seed_value = abs(match_hash) % (2**32 - 1)
        random.seed(seed_value)
        
        # Set up the prediction structure
        prediction = {
            'match': f"{match_data.get('home_team', '')} vs {match_data.get('away_team', '')}",
            'date': match_data.get('date', datetime.now()),
            'confidence': 0.0,
            'outcome': '',
            'statistical_factors': [],
            'esoteric_factors': [],
            'odds_factors': []
        }
        
        # Run convergence submodules
        submodule_results = {}
        for name, module_func in self.submodules.items():
            try:
                submodule_results[name] = module_func(match_data, arcan_x_results, shadow_odds_results)
            except Exception as e:
                # In production, log the error properly
                print(f"Error in {name}: {str(e)}")
                submodule_results[name] = {'confidence': 0.5, 'factors': []}
        
        # Calculate weighted convergence of arcan_x and shadow_odds results
        arcan_x_confidence = arcan_x_results.get('confidence', 0.5)
        shadow_odds_confidence = shadow_odds_results.get('confidence', 0.5)
        
        # Base weights of the two systems (can be adjusted based on historical performance)
        arcan_x_weight = 0.45
        shadow_odds_weight = 0.55
        
        # Apply submodule modifications to weights
        for submodule, result in submodule_results.items():
            # Some submodules might suggest adjusting the weight balance
            if 'arcan_x_weight_mod' in result:
                arcan_x_weight += result['arcan_x_weight_mod']
                shadow_odds_weight -= result['arcan_x_weight_mod']
        
        # Normalize weights to ensure they sum to 1
        total_weight = arcan_x_weight + shadow_odds_weight
        arcan_x_weight /= total_weight
        shadow_odds_weight /= total_weight
        
        # Calculate combined confidence
        base_confidence = (arcan_x_confidence * arcan_x_weight) + (shadow_odds_confidence * shadow_odds_weight)
        
        # Apply convergence modifiers from submodules
        confidence_modifiers = 0
        for submodule, result in submodule_results.items():
            if 'confidence_mod' in result:
                confidence_modifiers += result['confidence_mod']
        
        # Apply modifiers to base confidence
        final_confidence = base_confidence + confidence_modifiers
        
        # Ensure confidence is between 0 and 1
        final_confidence = max(0, min(1, final_confidence))
        
        # Set the final confidence
        prediction['confidence'] = final_confidence
        
        # Determine the outcome based on the combined analysis
        # For simplicity, we'll select between home win, draw, and away win for football
        # Other sports would have different outcome options
        
        # Extract home and away teams
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # Generate outcome based on the match_hash to ensure consistency
        # This would be based on more sophisticated algorithms in a real system
        
        # Determine outcome tendency
        # Higher confidence generally means stronger lean toward a specific outcome
        if match_data.get('sport', '') == 'Football':
            # For football, we have three possible outcomes
            r = random.random()
            
            # Adjust probabilities based on confidence
            # Higher confidence means less randomness
            if final_confidence > 0.8:
                # Very confident - strong tendency
                if r < 0.6:
                    outcome = f"{home_team} Win"
                elif r < 0.8:
                    outcome = f"{away_team} Win"
                else:
                    outcome = "Draw"
            elif final_confidence > 0.6:
                # Moderately confident
                if r < 0.45:
                    outcome = f"{home_team} Win"
                elif r < 0.75:
                    outcome = f"{away_team} Win"
                else:
                    outcome = "Draw"
            else:
                # Low confidence
                if r < 0.4:
                    outcome = f"{home_team} Win"
                elif r < 0.7:
                    outcome = f"{away_team} Win"
                else:
                    outcome = "Draw"
        else:
            # For other sports, default to binary outcome
            if random.random() < 0.5:
                outcome = f"{home_team} Win"
            else:
                outcome = f"{away_team} Win"
        
        prediction['outcome'] = outcome
        
        # Add factors from ArcanX and ShadowOdds
        # Categorize factors for better presentation
        
        # Extract and categorize ArcanX factors
        for factor in arcan_x_results.get('factors', []):
            prediction['esoteric_factors'].append(factor)
        
        # Extract and categorize ShadowOdds factors
        for factor in shadow_odds_results.get('factors', []):
            prediction['odds_factors'].append(factor)
        
        # Add statistical factors (basic match stats)
        prediction['statistical_factors'] = [
            {
                'name': 'Home Form',
                'value': match_data.get('home_form', 'N/A')
            },
            {
                'name': 'Away Form',
                'value': match_data.get('away_form', 'N/A')
            },
            {
                'name': 'Home Odds',
                'value': match_data.get('home_odds', 'N/A')
            },
            {
                'name': 'Away Odds',
                'value': match_data.get('away_odds', 'N/A')
            }
        ]
        
        # Add additional factors from convergence submodules
        for submodule, result in submodule_results.items():
            for factor in result.get('factors', []):
                if 'type' in factor and factor['type'] == 'statistical':
                    prediction['statistical_factors'].append(factor)
                elif 'type' in factor and factor['type'] == 'esoteric':
                    prediction['esoteric_factors'].append(factor)
                elif 'type' in factor and factor['type'] == 'odds':
                    prediction['odds_factors'].append(factor)
                else:
                    # Default to statistical if not specified
                    prediction['statistical_factors'].append(factor)
        
        return prediction
    
    def convergia_core(self, match_data, arcan_x_results, shadow_odds_results):
        """
        ConvergiaCore: Main integration engine for combining results from multiple modules.
        
        Args:
            match_data (dict): Match information
            arcan_x_results (dict): Results from ArcanX
            shadow_odds_results (dict): Results from ShadowOdds
            
        Returns:
            dict: Integration results
        """
        result = {
            'confidence_mod': 0,
            'factors': [],
            'arcan_x_weight_mod': 0  # Adjustment to ArcanX weight
        }
        
        # Check for agreement/disagreement between ArcanX and ShadowOdds
        arcan_x_confidence = arcan_x_results.get('confidence', 0.5)
        shadow_odds_confidence = shadow_odds_results.get('confidence', 0.5)
        
        # Calculate the difference in confidence
        confidence_diff = abs(arcan_x_confidence - shadow_odds_confidence)
        
        # Check if there's strong agreement
        if confidence_diff < 0.1 and arcan_x_confidence > 0.6 and shadow_odds_confidence > 0.6:
            result['factors'].append({
                'name': 'Module Convergence',
                'value': 'Strong agreement between esoteric and odds analysis',
                'type': 'statistical'
            })
            
            # Agreement boosts overall confidence
            result['confidence_mod'] += 0.1
        
        # Check if there's strong disagreement
        elif confidence_diff > 0.3:
            result['factors'].append({
                'name': 'Module Divergence',
                'value': 'Significant disagreement between esoteric and odds analysis',
                'type': 'statistical'
            })
            
            # Disagreement reduces overall confidence
            result['confidence_mod'] -= 0.1
            
            # When modules disagree, favor the one with stronger signal
            if arcan_x_confidence > shadow_odds_confidence:
                result['arcan_x_weight_mod'] = 0.15  # Increase ArcanX influence
                result['factors'].append({
                    'name': 'Esoteric Signal Strength',
                    'value': 'Esoteric signals stronger than market signals',
                    'type': 'esoteric'
                })
            else:
                result['arcan_x_weight_mod'] = -0.15  # Decrease ArcanX influence
                result['factors'].append({
                    'name': 'Market Signal Strength',
                    'value': 'Market signals stronger than esoteric signals',
                    'type': 'odds'
                })
        
        # Check for moderate alignment
        else:
            result['factors'].append({
                'name': 'Module Alignment',
                'value': 'Moderate alignment between esoteric and odds analysis',
                'type': 'statistical'
            })
            
            # Small confidence boost for alignment
            result['confidence_mod'] += 0.05
        
        # Check for synergistic factors across both modules
        
        # Count how many factors mention momentum
        momentum_factors = 0
        for factor in arcan_x_results.get('factors', []):
            if 'momentum' in factor['name'].lower() or 'momentum' in factor['value'].lower():
                momentum_factors += 1
        
        for factor in shadow_odds_results.get('factors', []):
            if 'momentum' in factor['name'].lower() or 'momentum' in factor['value'].lower():
                momentum_factors += 1
        
        # If multiple modules detect momentum, it's a stronger signal
        if momentum_factors >= 2:
            result['factors'].append({
                'name': 'Momentum Synergy',
                'value': 'Multiple modules detecting momentum patterns',
                'type': 'statistical'
            })
            
            result['confidence_mod'] += 0.08
        
        return result
    
    def mirror_phase(self, match_data, arcan_x_results, shadow_odds_results):
        """
        MirrorPhase: Synchronizes cycles and behavioral patterns from different modules.
        
        Args:
            match_data (dict): Match information
            arcan_x_results (dict): Results from ArcanX
            shadow_odds_results (dict): Results from ShadowOdds
            
        Returns:
            dict: Synchronization results
        """
        result = {
            'confidence_mod': 0,
            'factors': []
        }
        
        # Extract cycle-related factors from ArcanX
        cycle_factors = []
        for factor in arcan_x_results.get('factors', []):
            if any(term in factor['name'].lower() for term in ['cycle', 'pattern', 'recurring', 'historical']):
                cycle_factors.append(factor)
        
        # Extract behavioral pattern factors from ShadowOdds
        behavior_factors = []
        for factor in shadow_odds_results.get('factors', []):
            if any(term in factor['name'].lower() for term in ['pattern', 'movement', 'trend', 'historical']):
                behavior_factors.append(factor)
        
        # Check if we have both types of factors
        if cycle_factors and behavior_factors:
            # Generate a random consistency score for demonstration
            consistency = random.uniform(0.5, 1.0)
            
            if consistency > 0.8:
                result['factors'].append({
                    'name': 'High Pattern Synchronization',
                    'value': 'Esoteric cycles align strongly with market behavior patterns',
                    'type': 'esoteric'
                })
                
                result['confidence_mod'] += 0.15
            elif consistency > 0.6:
                result['factors'].append({
                    'name': 'Moderate Pattern Synchronization',
                    'value': 'Some alignment between esoteric cycles and market behavior',
                    'type': 'esoteric'
                })
                
                result['confidence_mod'] += 0.08
            else:
                result['factors'].append({
                    'name': 'Low Pattern Synchronization',
                    'value': 'Limited alignment between esoteric cycles and market behavior',
                    'type': 'esoteric'
                })
                
                result['confidence_mod'] += 0.03
        
        # Check for specific pattern types that might be synchronized
        
        # Check for lunar patterns in ArcanX
        has_lunar_pattern = False
        for factor in arcan_x_results.get('factors', []):
            if any(term in factor['name'].lower() or term in factor['value'].lower() 
                  for term in ['moon', 'lunar', 'tide']):
                has_lunar_pattern = True
                break
        
        # Check for volume patterns in ShadowOdds
        has_volume_pattern = False
        for factor in shadow_odds_results.get('factors', []):
            if any(term in factor['name'].lower() or term in factor['value'].lower() 
                  for term in ['volume', 'betting', 'surge']):
                has_volume_pattern = True
                break
        
        # If both are present, check for potential synchronization
        if has_lunar_pattern and has_volume_pattern:
            result['factors'].append({
                'name': 'Lunar-Volume Synchronization',
                'value': 'Potential relationship between lunar cycle and betting volume patterns',
                'type': 'esoteric'
            })
            
            result['confidence_mod'] += 0.1
        
        return result
    
    def momentum_shift_tracker(self, match_data, arcan_x_results, shadow_odds_results):
        """
        MomentumShiftTracker: Detects changes in momentum across various dimensions.
        
        Args:
            match_data (dict): Match information
            arcan_x_results (dict): Results from ArcanX
            shadow_odds_results (dict): Results from ShadowOdds
            
        Returns:
            dict: Momentum analysis results
        """
        result = {
            'confidence_mod': 0,
            'factors': []
        }
        
        # Check if ShadowOdds detected a momentum shift
        shadow_momentum_shift = False
        shadow_momentum_direction = None
        
        for factor in shadow_odds_results.get('factors', []):
            if 'momentum' in factor['name'].lower() or 'momentum' in factor['value'].lower():
                shadow_momentum_shift = True
                
                # Try to extract the direction
                if 'home' in factor['value'].lower():
                    shadow_momentum_direction = 'home'
                elif 'away' in factor['value'].lower():
                    shadow_momentum_direction = 'away'
                
                break
        
        # Check if ArcanX detected a momentum or energy shift
        arcan_momentum_shift = False
        arcan_momentum_direction = None
        
        for factor in arcan_x_results.get('factors', []):
            if any(term in factor['name'].lower() or term in factor['value'].lower() 
                  for term in ['momentum', 'energy', 'flow', 'shift']):
                arcan_momentum_shift = True
                
                # Try to extract the direction
                if 'home' in factor['value'].lower():
                    arcan_momentum_direction = 'home'
                elif 'away' in factor['value'].lower():
                    arcan_momentum_direction = 'away'
                
                break
        
        # Check if both modules detected a momentum shift
        if shadow_momentum_shift and arcan_momentum_shift:
            # Check if the directions align
            if shadow_momentum_direction == arcan_momentum_direction:
                result['factors'].append({
                    'name': 'Aligned Momentum Shift',
                    'value': f'Both market and esoteric analysis detect momentum shift toward {shadow_momentum_direction} team',
                    'type': 'statistical'
                })
                
                result['confidence_mod'] += 0.18
            else:
                result['factors'].append({
                    'name': 'Conflicting Momentum Signals',
                    'value': 'Market and esoteric analysis detect momentum shifts in different directions',
                    'type': 'statistical'
                })
                
                result['confidence_mod'] -= 0.05
        elif shadow_momentum_shift:
            result['factors'].append({
                'name': 'Market Momentum Shift',
                'value': f'Market analysis detects momentum shift toward {shadow_momentum_direction} team',
                'type': 'odds'
            })
            
            result['confidence_mod'] += 0.1
        elif arcan_momentum_shift:
            result['factors'].append({
                'name': 'Esoteric Momentum Shift',
                'value': f'Esoteric analysis detects momentum shift toward {arcan_momentum_direction} team',
                'type': 'esoteric'
            })
            
            result['confidence_mod'] += 0.08
        
        # Check for recent form momentum (basic statistical analysis)
        home_form = match_data.get('home_form', '')
        away_form = match_data.get('away_form', '')
        
        if home_form.startswith('WW') and not away_form.startswith('WW'):
            result['factors'].append({
                'name': 'Home Form Momentum',
                'value': f'Home team on winning streak: {home_form}',
                'type': 'statistical'
            })
            
            result['confidence_mod'] += 0.05
        
        if away_form.startswith('WW') and not home_form.startswith('WW'):
            result['factors'].append({
                'name': 'Away Form Momentum',
                'value': f'Away team on winning streak: {away_form}',
                'type': 'statistical'
            })
            
            result['confidence_mod'] += 0.05
        
        return result
    
    def captain_switch(self, match_data, arcan_x_results, shadow_odds_results):
        """
        CaptainSwitch: Analyzes the impact of leadership changes on team dynamics.
        
        Args:
            match_data (dict): Match information
            arcan_x_results (dict): Results from ArcanX
            shadow_odds_results (dict): Results from ShadowOdds
            
        Returns:
            dict: Leadership analysis results
        """
        result = {
            'confidence_mod': 0,
            'factors': []
        }
        
        # This would normally check if there's a captain change
        # For demonstration, we'll simulate it
        
        # Generate a unique seed from match data
        match_hash = hash(f"{match_data.get('home_team', '')}_{match_data.get('away_team', '')}_{match_data.get('date', datetime.now())}")
        random.seed(match_hash)
        
        # Simulate captain changes
        home_captain_change = random.random() < 0.15  # 15% chance
        away_captain_change = random.random() < 0.15
        
        if home_captain_change:
            result['factors'].append({
                'name': 'Home Captain Change',
                'value': 'Home team playing with different captain than usual',
                'type': 'statistical'
            })
            
            # Determine impact (positive or negative)
            impact = random.choice(['positive', 'neutral', 'negative'])
            
            if impact == 'positive':
                result['factors'].append({
                    'name': 'Positive Leadership Impact',
                    'value': 'New home captain brings positive energy to team',
                    'type': 'esoteric'
                })
                
                result['confidence_mod'] += 0.08
            elif impact == 'negative':
                result['factors'].append({
                    'name': 'Negative Leadership Impact',
                    'value': 'Home team showing signs of leadership instability',
                    'type': 'esoteric'
                })
                
                result['confidence_mod'] -= 0.08
        
        if away_captain_change:
            result['factors'].append({
                'name': 'Away Captain Change',
                'value': 'Away team playing with different captain than usual',
                'type': 'statistical'
            })
            
            # Determine impact (positive or negative)
            impact = random.choice(['positive', 'neutral', 'negative'])
            
            if impact == 'positive':
                result['factors'].append({
                    'name': 'Positive Leadership Impact',
                    'value': 'New away captain brings positive energy to team',
                    'type': 'esoteric'
                })
                
                result['confidence_mod'] += 0.08
            elif impact == 'negative':
                result['factors'].append({
                    'name': 'Negative Leadership Impact',
                    'value': 'Away team showing signs of leadership instability',
                    'type': 'esoteric'
                })
                
                result['confidence_mod'] -= 0.08
        
        # Check for manager/coach changes as well
        home_manager_change = random.random() < 0.1  # 10% chance
        away_manager_change = random.random() < 0.1
        
        if home_manager_change:
            result['factors'].append({
                'name': 'Home Manager Change',
                'value': 'Home team recently changed manager/coach',
                'type': 'statistical'
            })
            
            # New manager often brings temporary boost
            result['confidence_mod'] += 0.05
        
        if away_manager_change:
            result['factors'].append({
                'name': 'Away Manager Change',
                'value': 'Away team recently changed manager/coach',
                'type': 'statistical'
            })
            
            # New manager often brings temporary boost
            result['confidence_mod'] += 0.05
        
        return result
    
    def youth_impact_analyzer(self, match_data, arcan_x_results, shadow_odds_results):
        """
        YouthImpactAnalyzer: Evaluates the influence of young players on match dynamics.
        
        Args:
            match_data (dict): Match information
            arcan_x_results (dict): Results from ArcanX
            shadow_odds_results (dict): Results from ShadowOdds
            
        Returns:
            dict: Youth impact analysis results
        """
        result = {
            'confidence_mod': 0,
            'factors': []
        }
        
        # This would normally analyze young player involvement
        # For demonstration, we'll simulate it
        
        # Generate a unique seed from match data
        match_hash = hash(f"{match_data.get('home_team', '')}_{match_data.get('away_team', '')}_{match_data.get('date', datetime.now())}")
        random.seed(match_hash)
        
        # Simulate youth involvement
        home_youth_factor = random.random() < 0.3  # 30% chance
        away_youth_factor = random.random() < 0.3
        
        if home_youth_factor:
            youth_type = random.choice(['debut', 'breakthrough', 'key role'])
            
            result['factors'].append({
                'name': 'Home Youth Factor',
                'value': f'Young player in {youth_type} situation for home team',
                'type': 'statistical'
            })
            
            # Check if there's an esoteric energy aspect
            if random.random() < 0.5:
                result['factors'].append({
                    'name': 'Youth Energy',
                    'value': 'Young player brings fresh, unpredictable energy to home team',
                    'type': 'esoteric'
                })
                
                # Youth can add unpredictability
                result['confidence_mod'] -= 0.05
        
        if away_youth_factor:
            youth_type = random.choice(['debut', 'breakthrough', 'key role'])
            
            result['factors'].append({
                'name': 'Away Youth Factor',
                'value': f'Young player in {youth_type} situation for away team',
                'type': 'statistical'
            })
            
            # Check if there's an esoteric energy aspect
            if random.random() < 0.5:
                result['factors'].append({
                    'name': 'Youth Energy',
                    'value': 'Young player brings fresh, unpredictable energy to away team',
                    'type': 'esoteric'
                })
                
                # Youth can add unpredictability
                result['confidence_mod'] -= 0.05
        
        # Check for "golden generation" factor
        golden_gen = random.random() < 0.15  # 15% chance
        
        if golden_gen:
            team = random.choice(['home', 'away'])
            
            result['factors'].append({
                'name': 'Golden Generation',
                'value': f'{team.capitalize()} team has emerging group of talented young players',
                'type': 'statistical'
            })
            
            # A golden generation can have karmic momentum
            result['factors'].append({
                'name': 'Generational Karma',
                'value': f'Positive karmic cycle for {team} team\'s young core',
                'type': 'esoteric'
            })
            
            result['confidence_mod'] += 0.1
        
        return result
    
    def late_surge_detector(self, match_data, arcan_x_results, shadow_odds_results):
        """
        LateSurgeDetector: Identifies teams likely to have strong late-game performance.
        
        Args:
            match_data (dict): Match information
            arcan_x_results (dict): Results from ArcanX
            shadow_odds_results (dict): Results from ShadowOdds
            
        Returns:
            dict: Late surge analysis results
        """
        result = {
            'confidence_mod': 0,
            'factors': []
        }
        
        # Generate a unique seed from match data
        match_hash = hash(f"{match_data.get('home_team', '')}_{match_data.get('away_team', '')}_{match_data.get('date', datetime.now())}")
        random.seed(match_hash)
        
        # Check for late surge indicators in both modules
        
        # Check ArcanX factors
        arcan_late_indicator = False
        for factor in arcan_x_results.get('factors', []):
            if any(term in factor['name'].lower() or term in factor['value'].lower() 
                  for term in ['late', 'surge', 'finish', 'closing']):
                arcan_late_indicator = True
                break
        
        # Check ShadowOdds factors
        shadow_late_indicator = False
        for factor in shadow_odds_results.get('factors', []):
            if any(term in factor['name'].lower() or term in factor['value'].lower() 
                  for term in ['late', 'surge', 'movement', 'closing']):
                shadow_late_indicator = True
                break
        
        # Simulate historical late goal patterns
        home_late_goals = random.random() < 0.35  # 35% chance
        away_late_goals = random.random() < 0.35
        
        if home_late_goals:
            result['factors'].append({
                'name': 'Home Late Goal Pattern',
                'value': 'Home team has history of scoring late goals',
                'type': 'statistical'
            })
            
            # If also detected in other modules, stronger signal
            if arcan_late_indicator or shadow_late_indicator:
                result['factors'].append({
                    'name': 'Confirmed Late Surge Potential',
                    'value': 'Multiple indicators suggest home team late surge potential',
                    'type': 'statistical'
                })
                
                result['confidence_mod'] += 0.12
            else:
                result['confidence_mod'] += 0.05
        
        if away_late_goals:
            result['factors'].append({
                'name': 'Away Late Goal Pattern',
                'value': 'Away team has history of scoring late goals',
                'type': 'statistical'
            })
            
            # If also detected in other modules, stronger signal
            if arcan_late_indicator or shadow_late_indicator:
                result['factors'].append({
                    'name': 'Confirmed Late Surge Potential',
                    'value': 'Multiple indicators suggest away team late surge potential',
                    'type': 'statistical'
                })
                
                result['confidence_mod'] += 0.12
            else:
                result['confidence_mod'] += 0.05
        
        # Check for "clutch time" performers
        clutch_factor = random.random() < 0.25  # 25% chance
        
        if clutch_factor:
            team = random.choice(['home', 'away'])
            
            result['factors'].append({
                'name': 'Clutch Performer',
                'value': f'{team.capitalize()} team has key player who excels in decisive moments',
                'type': 'statistical'
            })
            
            # Add esoteric dimension
            result['factors'].append({
                'name': 'Clutch Energy',
                'value': f'Strong decisive moment energy detected for {team} team',
                'type': 'esoteric'
            })
            
            result['confidence_mod'] += 0.08
        
        return result
    
    def set_piece_threat_evaluator(self, match_data, arcan_x_results, shadow_odds_results):
        """
        SetPieceThreatEvaluator: Analyzes set piece effectiveness and potential.
        
        Args:
            match_data (dict): Match information
            arcan_x_results (dict): Results from ArcanX
            shadow_odds_results (dict): Results from ShadowOdds
            
        Returns:
            dict: Set piece analysis results
        """
        result = {
            'confidence_mod': 0,
            'factors': []
        }
        
        # Generate a unique seed from match data
        match_hash = hash(f"{match_data.get('home_team', '')}_{match_data.get('away_team', '')}_{match_data.get('date', datetime.now())}")
        random.seed(match_hash)
        
        # Only relevant for football/soccer
        if match_data.get('sport', '') != 'Football':
            return result
        
        # Simulate set piece effectiveness data
        home_set_piece_strength = random.uniform(0.3, 0.9)
        away_set_piece_strength = random.uniform(0.3, 0.9)
        
        # Check for significant advantage
        set_piece_diff = home_set_piece_strength - away_set_piece_strength
        
        if abs(set_piece_diff) > 0.3:
            # Significant advantage
            stronger_team = 'home' if set_piece_diff > 0 else 'away'
            
            result['factors'].append({
                'name': 'Set Piece Advantage',
                'value': f'{stronger_team.capitalize()} team has significant set piece advantage',
                'type': 'statistical'
            })
            
            # Check if there's any astrological support in ArcanX
            astro_support = False
            for factor in arcan_x_results.get('factors', []):
                if 'astr' in factor['name'].lower() or 'astr' in factor['value'].lower():
                    astro_support = True
                    break
            
            if astro_support:
                result['factors'].append({
                    'name': 'Astrological Set Piece Boost',
                    'value': f'Celestial alignment enhances {stronger_team} team set piece effectiveness',
                    'type': 'esoteric'
                })
                
                result['confidence_mod'] += 0.15
            else:
                result['confidence_mod'] += 0.08
        
        # Check for dead ball specialists
        specialist_factor = random.random() < 0.4  # 40% chance
        
        if specialist_factor:
            team = random.choice(['home', 'away'])
            
            result['factors'].append({
                'name': 'Dead Ball Specialist',
                'value': f'{team.capitalize()} team has exceptional set piece taker',
                'type': 'statistical'
            })
            
            # Add energy dimension
            result['factors'].append({
                'name': 'Focus Energy',
                'value': f'Strong concentration energy for {team} team set pieces',
                'type': 'esoteric'
            })
            
            result['confidence_mod'] += 0.06
        
        return result
    
    def fan_sentiment_monitor(self, match_data, arcan_x_results, shadow_odds_results):
        """
        FanSentimentMonitor: Analyzes crowd energy and its impact on the match.
        
        Args:
            match_data (dict): Match information
            arcan_x_results (dict): Results from ArcanX
            shadow_odds_results (dict): Results from ShadowOdds
            
        Returns:
            dict: Fan sentiment analysis results
        """
        result = {
            'confidence_mod': 0,
            'factors': []
        }
        
        # Generate a unique seed from match data
        match_hash = hash(f"{match_data.get('home_team', '')}_{match_data.get('away_team', '')}_{match_data.get('date', datetime.now())}")
        random.seed(match_hash)
        
        # Simulate fan sentiment data
        home_support_level = random.uniform(0.5, 1.0)  # Home fans usually provide decent support
        away_support_level = random.uniform(0.2, 0.7)  # Away support varies more
        
        # Check for special home support
        if home_support_level > 0.8:
            result['factors'].append({
                'name': 'Strong Home Support',
                'value': 'Exceptional home crowd energy expected',
                'type': 'statistical'
            })
            
            # Check for stadium energy in ArcanX
            stadium_energy = False
            for factor in arcan_x_results.get('factors', []):
                if 'stadium' in factor['name'].lower() or 'venue' in factor['name'].lower():
                    stadium_energy = True
                    break
            
            if stadium_energy:
                result['factors'].append({
                    'name': 'Amplified Stadium Energy',
                    'value': 'Fan energy amplifies existing stadium energetic properties',
                    'type': 'esoteric'
                })
                
                result['confidence_mod'] += 0.12
            else:
                result['confidence_mod'] += 0.05
        
        # Check for strong away support
        if away_support_level > 0.6:
            result['factors'].append({
                'name': 'Strong Away Support',
                'value': 'Unusually strong away fan presence expected',
                'type': 'statistical'
            })
            
            # This can sometimes neutralize home advantage
            result['confidence_mod'] -= 0.03
        
        # Check for derby/rivalry
        is_derby = random.random() < 0.15  # 15% chance
        
        if is_derby:
            result['factors'].append({
                'name': 'Derby/Rivalry Match',
                'value': 'Heightened emotions due to local rivalry',
                'type': 'statistical'
            })
            
            # Add esoteric dimension
            result['factors'].append({
                'name': 'Rivalry Energy',
                'value': 'Historical karmic patterns activated by rivalry context',
                'type': 'esoteric'
            })
            
            # Derbies can be more unpredictable
            result['confidence_mod'] -= 0.08
        
        # Check for special occasion
        special_occasion = random.random() < 0.1  # 10% chance
        
        if special_occasion:
            occasion_type = random.choice(['anniversary', 'memorial', 'celebration', 'homecoming'])
            
            result['factors'].append({
                'name': 'Special Occasion',
                'value': f'Match coincides with {occasion_type} event for home team',
                'type': 'statistical'
            })
            
            # Special occasions often boost performance
            result['factors'].append({
                'name': 'Ceremonial Energy',
                'value': 'Elevated emotional and symbolic energy due to special occasion',
                'type': 'esoteric'
            })
            
            result['confidence_mod'] += 0.1
        
        return result
    
    def _initialize_correlation_matrix(self):
        """Initialize correlation matrix for weighting factors."""
        # In a full implementation, this would be learned from historical data
        # For now, return a placeholder
        return {}
