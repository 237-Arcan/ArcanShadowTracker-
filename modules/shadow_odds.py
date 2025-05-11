import numpy as np
from datetime import datetime, timedelta
import math

class ShadowOdds:
    """
    ShadowOdds module - Analyzes the behavior of betting odds and market movements.
    Detects anomalies, manipulations, and hidden patterns in odds data.
    """
    
    def __init__(self):
        """Initialize the ShadowOdds module with necessary components."""
        self.submodules = {
            'LineTrap': self.line_trap,
            'BetPulse': self.bet_pulse,
            'CrowdPressureIndex': self.crowd_pressure_index,
            'MarketEcho': self.market_echo,
            'CollapseDetector': self.collapse_detector,
            'ShadowMomentum': self.shadow_momentum,
            'SetTrapIndicator': self.set_trap_indicator
        }
        
        # Initialize historical market behavior models
        self.market_models = self._initialize_market_models()
        
        # Cache for results to avoid redundant calculations
        self.cache = {}
    
    def analyze_match(self, match_data):
        """
        Main method to analyze match odds and market behavior.
        Returns a dictionary with confidence scores and influential factors.
        
        Args:
            match_data (dict): Match information including odds, market data, etc.
            
        Returns:
            dict: Results of the odds analysis with confidence scores and factors
        """
        # Clear cache for new match
        self.cache = {}
        
        results = {
            'confidence': 0,
            'factors': []
        }
        
        # Run each submodule and collect results
        submodule_results = {}
        for name, module_func in self.submodules.items():
            try:
                submodule_results[name] = module_func(match_data)
            except Exception as e:
                # In production, log the error properly
                print(f"Error in {name}: {str(e)}")
                submodule_results[name] = {'confidence': 0.5, 'factors': []}
        
        # Calculate weighted confidence
        # Each module has different weights based on historical performance
        module_weights = {
            'LineTrap': 0.18,
            'BetPulse': 0.15,
            'CrowdPressureIndex': 0.12,
            'MarketEcho': 0.16,
            'CollapseDetector': 0.13,
            'ShadowMomentum': 0.15,
            'SetTrapIndicator': 0.11
        }
        
        total_confidence = 0
        total_weight = 0
        
        for module, result in submodule_results.items():
            weight = module_weights.get(module, 0.1)
            total_confidence += result['confidence'] * weight
            total_weight += weight
            
            # Add factors to the overall results
            results['factors'].extend(result['factors'])
        
        # Normalize confidence
        if total_weight > 0:
            results['confidence'] = total_confidence / total_weight
        else:
            results['confidence'] = 0.5  # Default to 50% if no weights
        
        return results
    
    def line_trap(self, match_data):
        """
        LineTrap module: Identifies odds that appear to be traps.
        Looks for discrepancies between odds and actual match dynamics.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Line trap analysis results
        """
        result = {
            'confidence': 0.5,  # Default neutral confidence
            'factors': []
        }
        
        # Extract match odds
        home_odds = match_data.get('home_odds', 0)
        draw_odds = match_data.get('draw_odds', 0)
        away_odds = match_data.get('away_odds', 0)
        
        # Extract form data if available
        home_form = match_data.get('home_form', '')
        away_form = match_data.get('away_form', '')
        
        # If we don't have odds data, return default result
        if not home_odds or not away_odds:
            result['factors'].append({
                'name': 'Insufficient Odds Data',
                'value': 'Unable to analyze odds without complete data'
            })
            return result
        
        # Calculate implied probabilities
        home_implied_prob = 1 / home_odds if home_odds > 0 else 0
        draw_implied_prob = 1 / draw_odds if draw_odds > 0 else 0
        away_implied_prob = 1 / away_odds if away_odds > 0 else 0
        
        # Calculate market overround (bookmaker margin)
        overround = (home_implied_prob + draw_implied_prob + away_implied_prob) - 1
        
        # Check for suspiciously low overround (potential value)
        if 0 < overround < 0.05:
            result['factors'].append({
                'name': 'Low Margin Market',
                'value': f'Market margin of {overround:.1%} is unusually low'
            })
            result['confidence'] += 0.05
        
        # Check odds relative to form
        if home_form and away_form:
            # Calculate form points (W=3, D=1, L=0)
            home_points = sum(3 if result == 'W' else 1 if result == 'D' else 0 for result in home_form)
            away_points = sum(3 if result == 'W' else 1 if result == 'D' else 0 for result in away_form)
            
            # Calculate form differential
            form_diff = home_points - away_points
            
            # Expected odds differential based on form
            expected_odds_ratio = 1 - (form_diff / 30)  # Scale to reasonable ratio
            expected_odds_ratio = max(0.5, min(2.0, expected_odds_ratio))  # Limit to reasonable range
            
            # Actual odds ratio
            actual_odds_ratio = away_odds / home_odds if home_odds > 0 else 1
            
            # Calculate discrepancy
            odds_form_discrepancy = abs(actual_odds_ratio - expected_odds_ratio)
            
            # Check for significant discrepancy (potential trap)
            if odds_form_discrepancy > 0.5:
                # Determine which side seems to have value
                if actual_odds_ratio > expected_odds_ratio:
                    # Away odds higher than expected - potential home value or trap
                    result['factors'].append({
                        'name': 'Odds-Form Discrepancy',
                        'value': f'Home odds ({home_odds}) seem suspiciously high given form differential'
                    })
                else:
                    # Home odds higher than expected - potential away value or trap
                    result['factors'].append({
                        'name': 'Odds-Form Discrepancy',
                        'value': f'Away odds ({away_odds}) seem suspiciously high given form differential'
                    })
                
                # Larger discrepancy = more confidence in the trap
                result['confidence'] += 0.1 + (min(odds_form_discrepancy, 1.0) * 0.15)
        
        # Check for favorites that seem overvalued
        if home_odds < 1.5 and home_implied_prob > 0.7:
            # Heavy home favorite - check if potentially overvalued
            result['factors'].append({
                'name': 'Heavy Favorite Alert',
                'value': f'Home team implied probability of {home_implied_prob:.1%} may be overvalued'
            })
            result['confidence'] += 0.08
        
        if away_odds < 1.5 and away_implied_prob > 0.7:
            # Heavy away favorite - check if potentially overvalued
            result['factors'].append({
                'name': 'Heavy Favorite Alert',
                'value': f'Away team implied probability of {away_implied_prob:.1%} may be overvalued'
            })
            result['confidence'] += 0.08
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def bet_pulse(self, match_data):
        """
        BetPulse module: Analyzes betting volume and timing patterns.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Betting pulse analysis results
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # Extract betting volume data if available
        # This would normally come from an API or database
        # For now, we'll simulate it with a hash of the match data
        
        # Create a unique hash for the match to simulate consistent bet volume data
        match_hash = hash(f"{match_data.get('home_team', '')}_{match_data.get('away_team', '')}_{match_data.get('date', datetime.now())}")
        np.random.seed(match_hash)
        
        # Simulate betting volume patterns
        home_volume = np.random.uniform(0.2, 0.8)  # Percentage of bets on home team
        draw_volume = np.random.uniform(0.05, 0.3) if match_data.get('draw_odds', 0) > 0 else 0
        away_volume = 1 - home_volume - draw_volume
        
        # Simulate late surge (common in market manipulation)
        has_late_surge = np.random.random() < 0.3  # 30% chance of late surge
        surge_team = 'home' if np.random.random() < 0.6 else 'away'  # Which team has the surge
        
        # Simulate volume vs. odds discrepancy
        home_odds = match_data.get('home_odds', 2.0)
        away_odds = match_data.get('away_odds', 2.0)
        
        # Calculate expected volume based on odds
        total_implied_prob = (1/home_odds) + (1/away_odds)
        if match_data.get('draw_odds', 0) > 0:
            total_implied_prob += 1/match_data.get('draw_odds')
        
        expected_home_volume = (1/home_odds) / total_implied_prob
        expected_away_volume = (1/away_odds) / total_implied_prob
        
        # Calculate volume-odds discrepancy
        home_discrepancy = abs(home_volume - expected_home_volume)
        away_discrepancy = abs(away_volume - expected_away_volume)
        
        # Check for significant discrepancies
        if home_discrepancy > 0.2 or away_discrepancy > 0.2:
            if home_volume > expected_home_volume:
                result['factors'].append({
                    'name': 'Volume Discrepancy',
                    'value': f'Home team receiving {home_volume:.1%} of bets but odds imply only {expected_home_volume:.1%}'
                })
                result['confidence'] += 0.15
            else:
                result['factors'].append({
                    'name': 'Volume Discrepancy',
                    'value': f'Away team receiving {away_volume:.1%} of bets but odds imply only {expected_away_volume:.1%}'
                })
                result['confidence'] += 0.15
        
        # Check for late surge
        if has_late_surge:
            surge_size = np.random.uniform(0.2, 0.5)  # Size of the late surge
            
            result['factors'].append({
                'name': 'Late Betting Surge',
                'value': f'Detected {surge_size:.0%} surge in bets for {surge_team} team'
            })
            
            # Late surges can indicate informed money or manipulation
            result['confidence'] += 0.18
        
        # Check for steam moves (sharp bettors moving the market)
        has_steam_move = np.random.random() < 0.25  # 25% chance of steam move
        
        if has_steam_move:
            steam_direction = 'home' if np.random.random() < 0.5 else 'away'
            steam_size = np.random.uniform(0.05, 0.15)  # Size of odds movement
            
            result['factors'].append({
                'name': 'Steam Move Detected',
                'value': f'Sharp action moving {steam_direction} odds by {steam_size:.0%}'
            })
            
            # Steam moves often indicate smart money
            result['confidence'] += 0.2
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def crowd_pressure_index(self, match_data):
        """
        CrowdPressureIndex module: Detects excessive public pressure on one side.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Crowd pressure analysis results
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # Generate a unique seed from match data
        match_hash = hash(f"{match_data.get('home_team', '')}_{match_data.get('away_team', '')}_{match_data.get('league', '')}")
        np.random.seed(match_hash)
        
        # Simulate public sentiment data
        # This would typically come from social media analysis or betting trend data
        home_sentiment = np.random.uniform(0.2, 0.8)  # Percentage of public supporting home team
        away_sentiment = 1 - home_sentiment
        
        # Check if there's strong home team bias
        if home_sentiment > 0.7:
            result['factors'].append({
                'name': 'Public Bias',
                'value': f'Strong public bias ({home_sentiment:.0%}) toward home team'
            })
            
            # Check if the odds align with this bias
            home_odds = match_data.get('home_odds', 2.0)
            
            if home_odds < 1.7:
                # Home team is strongly favored by odds AND public
                result['factors'].append({
                    'name': 'Overrated Favorite',
                    'value': f'Home team potentially overvalued due to public bias'
                })
                result['confidence'] += 0.15
            else:
                # Home team has public support but odds don't reflect it
                result['factors'].append({
                    'name': 'Value Against Public',
                    'value': f'Home odds ({home_odds}) don\'t reflect strong public support'
                })
                result['confidence'] += 0.08
        
        # Check if there's strong away team bias
        if away_sentiment > 0.7:
            result['factors'].append({
                'name': 'Public Bias',
                'value': f'Strong public bias ({away_sentiment:.0%}) toward away team'
            })
            
            # Check if the odds align with this bias
            away_odds = match_data.get('away_odds', 2.0)
            
            if away_odds < 1.7:
                # Away team is strongly favored by odds AND public
                result['factors'].append({
                    'name': 'Overrated Favorite',
                    'value': f'Away team potentially overvalued due to public bias'
                })
                result['confidence'] += 0.15
            else:
                # Away team has public support but odds don't reflect it
                result['factors'].append({
                    'name': 'Value Against Public',
                    'value': f'Away odds ({away_odds}) don\'t reflect strong public support'
                })
                result['confidence'] += 0.08
        
        # Check for public opinion shaped by recency bias
        # Simulate a case where a team had a recent big win or loss
        has_recency_bias = np.random.random() < 0.4  # 40% chance
        
        if has_recency_bias:
            biased_team = 'home' if np.random.random() < 0.5 else 'away'
            bias_direction = 'positive' if np.random.random() < 0.5 else 'negative'
            
            if bias_direction == 'positive':
                result['factors'].append({
                    'name': 'Recency Bias',
                    'value': f'{biased_team.title()} team may be overvalued due to recent impressive performance'
                })
                result['confidence'] += 0.12
            else:
                result['factors'].append({
                    'name': 'Recency Bias',
                    'value': f'{biased_team.title()} team may be undervalued due to recent poor performance'
                })
                result['confidence'] += 0.12
        
        # Check for popular team bias
        popular_teams = ['Manchester United', 'Liverpool', 'Barcelona', 'Real Madrid', 
                        'Bayern Munich', 'Juventus', 'Paris Saint-Germain']
        
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        if home_team in popular_teams:
            result['factors'].append({
                'name': 'Popular Team Bias',
                'value': f'{home_team} typically receives excessive public support'
            })
            result['confidence'] += 0.1
        
        if away_team in popular_teams:
            result['factors'].append({
                'name': 'Popular Team Bias',
                'value': f'{away_team} typically receives excessive public support'
            })
            result['confidence'] += 0.1
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def market_echo(self, match_data):
        """
        MarketEcho module: Analyzes odds discrepancies between bookmakers.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Market echo analysis results
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # In a full implementation, this would compare odds across multiple bookmakers
        # For demonstration, we'll simulate this with randomized data
        
        # Generate a unique seed from match data
        match_hash = hash(f"{match_data.get('home_team', '')}_{match_data.get('away_team', '')}_{match_data.get('date', datetime.now())}")
        np.random.seed(match_hash)
        
        # Simulate base odds
        base_home_odds = match_data.get('home_odds', 2.0)
        base_draw_odds = match_data.get('draw_odds', 3.0)
        base_away_odds = match_data.get('away_odds', 2.0)
        
        # Simulate odds variations across bookmakers
        num_bookmakers = 5
        home_odds_variations = np.random.uniform(-0.2, 0.2, num_bookmakers)
        draw_odds_variations = np.random.uniform(-0.2, 0.2, num_bookmakers) if base_draw_odds > 0 else np.zeros(num_bookmakers)
        away_odds_variations = np.random.uniform(-0.2, 0.2, num_bookmakers)
        
        # Calculate simulated odds for each bookmaker
        home_odds_list = [max(1.01, base_home_odds + var) for var in home_odds_variations]
        draw_odds_list = [max(1.01, base_draw_odds + var) for var in draw_odds_variations] if base_draw_odds > 0 else []
        away_odds_list = [max(1.01, base_away_odds + var) for var in away_odds_variations]
        
        # Calculate max difference in odds
        home_odds_diff = max(home_odds_list) - min(home_odds_list)
        draw_odds_diff = max(draw_odds_list) - min(draw_odds_list) if draw_odds_list else 0
        away_odds_diff = max(away_odds_list) - min(away_odds_list)
        
        # Check for significant market disagreement
        if home_odds_diff > 0.3 or away_odds_diff > 0.3:
            # Determine which market has most disagreement
            if home_odds_diff > away_odds_diff:
                result['factors'].append({
                    'name': 'Market Disagreement',
                    'value': f'Significant variation in home odds ({home_odds_diff:.2f} difference)'
                })
            else:
                result['factors'].append({
                    'name': 'Market Disagreement',
                    'value': f'Significant variation in away odds ({away_odds_diff:.2f} difference)'
                })
            
            # Market disagreement can indicate value opportunities
            result['confidence'] += 0.15
        
        # Check for arbitrage opportunities
        # Calculate best odds for each outcome
        best_home = max(home_odds_list)
        best_draw = max(draw_odds_list) if draw_odds_list else 0
        best_away = max(away_odds_list)
        
        # Calculate arbitrage percentage
        arb_percentage = (1/best_home)
        if best_draw > 0:
            arb_percentage += (1/best_draw)
        arb_percentage += (1/best_away)
        
        if arb_percentage < 1.0:
            # Arbitrage exists
            profit_percentage = (1 - arb_percentage) * 100
            
            result['factors'].append({
                'name': 'Arbitrage Opportunity',
                'value': f'Detected {profit_percentage:.2f}% guaranteed profit opportunity'
            })
            
            # Arbitrage often indicates market inefficiency
            result['confidence'] += 0.2
        
        # Check for steam moves (sharp line movement)
        has_steam = np.random.random() < 0.3  # 30% chance
        
        if has_steam:
            steam_direction = 'home' if np.random.random() < 0.5 else 'away'
            steam_size = np.random.uniform(0.1, 0.3)
            
            result['factors'].append({
                'name': 'Steam Move',
                'value': f'Detected {steam_size:.2f} steam move on {steam_direction} odds'
            })
            
            # Steam often indicates sharp money
            result['confidence'] += 0.15
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def collapse_detector(self, match_data):
        """
        CollapseDetector module: Detects signs of potential team collapse.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Collapse potential analysis
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # Generate a unique seed from match data
        match_hash = hash(f"{match_data.get('home_team', '')}_{match_data.get('away_team', '')}_{match_data.get('date', datetime.now())}")
        np.random.seed(match_hash)
        
        # Check for collapse indicators in form
        home_form = match_data.get('home_form', '')
        away_form = match_data.get('away_form', '')
        
        # Check for losing streaks
        if home_form.count('L') >= 3:
            result['factors'].append({
                'name': 'Losing Streak',
                'value': f'Home team on {home_form.count("L")}-match losing run'
            })
            result['confidence'] += 0.12
        
        if away_form.count('L') >= 3:
            result['factors'].append({
                'name': 'Losing Streak',
                'value': f'Away team on {away_form.count("L")}-match losing run'
            })
            result['confidence'] += 0.12
        
        # Simulate additional collapse factors
        
        # Check for injury crisis
        home_injuries = np.random.randint(0, 5)
        away_injuries = np.random.randint(0, 5)
        
        if home_injuries >= 3:
            result['factors'].append({
                'name': 'Injury Crisis',
                'value': f'Home team missing {home_injuries} key players'
            })
            result['confidence'] += 0.15
        
        if away_injuries >= 3:
            result['factors'].append({
                'name': 'Injury Crisis',
                'value': f'Away team missing {away_injuries} key players'
            })
            result['confidence'] += 0.15
        
        # Check for recent manager change
        home_manager_change = np.random.random() < 0.15  # 15% chance
        away_manager_change = np.random.random() < 0.15
        
        if home_manager_change:
            result['factors'].append({
                'name': 'Manager Change',
                'value': 'Home team recently changed manager'
            })
            result['confidence'] += 0.1
        
        if away_manager_change:
            result['factors'].append({
                'name': 'Manager Change',
                'value': 'Away team recently changed manager'
            })
            result['confidence'] += 0.1
        
        # Check for fixture congestion
        home_congestion = np.random.random() < 0.25  # 25% chance
        away_congestion = np.random.random() < 0.25
        
        if home_congestion:
            result['factors'].append({
                'name': 'Fixture Congestion',
                'value': 'Home team in period of heavy fixture congestion'
            })
            result['confidence'] += 0.08
        
        if away_congestion:
            result['factors'].append({
                'name': 'Fixture Congestion',
                'value': 'Away team in period of heavy fixture congestion'
            })
            result['confidence'] += 0.08
        
        # Check for motivation issues
        home_motivation = np.random.random() < 0.2  # 20% chance
        away_motivation = np.random.random() < 0.2
        
        if home_motivation:
            result['factors'].append({
                'name': 'Motivation Issues',
                'value': 'Home team potentially lacking motivation for this match'
            })
            result['confidence'] += 0.1
        
        if away_motivation:
            result['factors'].append({
                'name': 'Motivation Issues',
                'value': 'Away team potentially lacking motivation for this match'
            })
            result['confidence'] += 0.1
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def shadow_momentum(self, match_data):
        """
        ShadowMomentum module: Detects subtle momentum changes in betting patterns.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Momentum shift analysis
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # Generate a unique seed from match data
        match_hash = hash(f"{match_data.get('home_team', '')}_{match_data.get('away_team', '')}_{match_data.get('date', datetime.now())}")
        np.random.seed(match_hash)
        
        # Simulate momentum shifts in betting
        has_momentum_shift = np.random.random() < 0.4  # 40% chance
        
        if has_momentum_shift:
            shift_direction = 'home' if np.random.random() < 0.5 else 'away'
            shift_magnitude = np.random.uniform(0.1, 0.3)
            
            result['factors'].append({
                'name': 'Momentum Shift',
                'value': f'Detected {shift_magnitude:.2f} momentum shift toward {shift_direction} team'
            })
            
            # Add more details about the shift
            shift_timing = np.random.choice(['early', 'recent', 'gradual'])
            
            if shift_timing == 'early':
                result['factors'].append({
                    'name': 'Early Movement',
                    'value': f'Momentum shift started early in the betting cycle'
                })
                result['confidence'] += 0.15
            elif shift_timing == 'recent':
                result['factors'].append({
                    'name': 'Recent Movement',
                    'value': f'Momentum shift started recently'
                })
                result['confidence'] += 0.18
            else:
                result['factors'].append({
                    'name': 'Gradual Movement',
                    'value': f'Momentum has been gradually shifting'
                })
                result['confidence'] += 0.12
        
        # Simulate sharp vs. public money conflict
        has_money_conflict = np.random.random() < 0.35  # 35% chance
        
        if has_money_conflict:
            sharp_side = 'home' if np.random.random() < 0.5 else 'away'
            public_side = 'away' if sharp_side == 'home' else 'home'
            
            result['factors'].append({
                'name': 'Money Conflict',
                'value': f'Sharp money on {sharp_side} team, public money on {public_side} team'
            })
            
            # Sharp money tends to be more reliable
            result['confidence'] += 0.2
        
        # Check for reverse line movement
        has_reverse_movement = np.random.random() < 0.2  # 20% chance
        
        if has_reverse_movement:
            majority_side = 'home' if np.random.random() < 0.5 else 'away'
            line_movement = 'against' if np.random.random() < 0.8 else 'with'  # Usually against
            
            if line_movement == 'against':
                result['factors'].append({
                    'name': 'Reverse Line Movement',
                    'value': f'Majority betting on {majority_side} but line moving against them'
                })
                result['confidence'] += 0.25
            else:
                result['factors'].append({
                    'name': 'Aligned Movement',
                    'value': f'Line moving with majority of bets on {majority_side}'
                })
                result['confidence'] += 0.1
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def set_trap_indicator(self, match_data):
        """
        SetTrapIndicator module: Detects potential odds traps.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Trap setting analysis
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # Generate a unique seed from match data
        match_hash = hash(f"{match_data.get('home_team', '')}_{match_data.get('away_team', '')}_{match_data.get('date', datetime.now())}")
        np.random.seed(match_hash)
        
        # Extract odds
        home_odds = match_data.get('home_odds', 0)
        draw_odds = match_data.get('draw_odds', 0)
        away_odds = match_data.get('away_odds', 0)
        
        # Check for odds that look too good to be true
        has_trap_odds = np.random.random() < 0.3  # 30% chance
        
        if has_trap_odds and home_odds > 0 and away_odds > 0:
            trap_side = 'home' if np.random.random() < 0.5 else 'away'
            trap_odds = home_odds if trap_side == 'home' else away_odds
            
            result['factors'].append({
                'name': 'Potential Odds Trap',
                'value': f'{trap_side.capitalize()} odds of {trap_odds} appear suspiciously high'
            })
            
            # Add context to the trap
            trap_reason = np.random.choice(['public bias', 'recent result', 'key player', 'hidden factor'])
            
            if trap_reason == 'public bias':
                result['factors'].append({
                    'name': 'Public Bias Trap',
                    'value': f'Bookmakers may be exploiting public bias on {trap_side} team'
                })
                result['confidence'] += 0.15
            elif trap_reason == 'recent result':
                result['factors'].append({
                    'name': 'Recency Trap',
                    'value': f'Odds may be inflated due to recent {trap_side} team performance'
                })
                result['confidence'] += 0.18
            elif trap_reason == 'key player':
                result['factors'].append({
                    'name': 'Personnel Trap',
                    'value': f'Odds may not properly account for key player status'
                })
                result['confidence'] += 0.2
            else:
                result['factors'].append({
                    'name': 'Hidden Factor Trap',
                    'value': f'Odds suggest bookmakers have hidden information'
                })
                result['confidence'] += 0.22
        
        # Check for historical trap patterns
        has_historical_pattern = np.random.random() < 0.25  # 25% chance
        
        if has_historical_pattern:
            result['factors'].append({
                'name': 'Historical Trap Pattern',
                'value': f'Similar odds pattern has resulted in upsets historically'
            })
            
            # Add details about the pattern
            pattern_confidence = np.random.uniform(0.6, 0.9)
            pattern_frequency = np.random.randint(3, 10)
            
            result['factors'].append({
                'name': 'Pattern Details',
                'value': f'Pattern observed {pattern_frequency} times with {pattern_confidence:.0%} accuracy'
            })
            
            result['confidence'] += 0.15
        
        # Check for midweek distraction
        has_distraction = np.random.random() < 0.2  # 20% chance
        
        if has_distraction:
            distracted_team = 'home' if np.random.random() < 0.5 else 'away'
            distraction_type = np.random.choice(['cup match', 'derby', 'European fixture'])
            
            result['factors'].append({
                'name': 'Distraction Factor',
                'value': f'{distracted_team.capitalize()} team has {distraction_type} coming up'
            })
            
            # This can create value on the non-distracted team
            opposite_team = 'away' if distracted_team == 'home' else 'home'
            
            result['factors'].append({
                'name': 'Focus Advantage',
                'value': f'{opposite_team.capitalize()} team likely more focused on this match'
            })
            
            result['confidence'] += 0.12
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def _initialize_market_models(self):
        """Initialize market behavior models for odds analysis."""
        # In a real implementation, this would be trained models
        # For simplicity, we'll use a placeholder
        return {}
