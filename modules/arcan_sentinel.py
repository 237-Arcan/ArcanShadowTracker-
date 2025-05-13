"""
ArcanSentinel - Lightweight real-time analysis module for ArcanShadow
Provides fast, reactive analysis for live matches
"""

import time
import random
import numpy as np
from datetime import datetime

class ArcanSentinel:
    """
    ArcanSentinel - Real-time analysis system for ArcanShadow
    Optimized for live match monitoring and rapid prediction updates
    """
    
    def __init__(self, arcan_x, shadow_odds, convergence):
        """
        Initialize the ArcanSentinel with references to core modules
        
        Args:
            arcan_x: ArcanX module instance for esoteric analysis
            shadow_odds: ShadowOdds module instance for odds analysis
            convergence: Convergence module instance for integrated analysis
        """
        # Store module references
        self.arcan_x = arcan_x
        self.shadow_odds = shadow_odds
        self.convergence = convergence
        
        # Live tracking state
        self.is_active = False
        self.current_match = None
        self.match_minute = 0
        self.score = [0, 0]  # Home - Away
        self.key_events = []
        self.predictions_history = []
        
        # Initialize specialized live modules
        self.live_modules = {
            'shadow_momentum': self.shadow_momentum_analysis,
            'bet_pulse': self.bet_pulse_analysis,
            'line_trap': self.line_trap_analysis,
            'karmic_flow': self.karmic_flow_analysis,
            'mirror_phase': self.mirror_phase_analysis,
            'clutch_time_scanner': self.clutch_time_analysis
        }
        
        # Analysis weights for live mode
        self.live_weights = {
            'shadow_momentum': 0.25,
            'bet_pulse': 0.15,
            'line_trap': 0.20,
            'karmic_flow': 0.15,
            'mirror_phase': 0.15,
            'clutch_time_scanner': 0.10
        }
        
        # Live detection thresholds
        self.momentum_threshold = 0.70
        self.betting_surge_threshold = 2.5  # Multiple of average betting volume
        self.line_movement_threshold = 0.15  # 15% change in odds
        
        # Activity log for real-time tracking
        self.activity_log = []
        
    def start_live_tracking(self, match_data):
        """
        Start real-time tracking of a match
        
        Args:
            match_data (dict): Initial match information
            
        Returns:
            dict: Initial live analysis results
        """
        self.is_active = True
        self.current_match = match_data
        self.match_minute = match_data.get('current_minute', 0)
        self.score = match_data.get('current_score', [0, 0])
        self.key_events = []
        self.predictions_history = []
        
        # Log start of tracking
        self.log_activity("Started live tracking", f"{match_data.get('home_team', '')} vs {match_data.get('away_team', '')}")
        
        # Generate initial analysis
        return self.update_live_analysis()
    
    def update_match_state(self, minute, score=None, event=None):
        """
        Update the current match state
        
        Args:
            minute (int): Current match minute
            score (list, optional): Current score [home, away]
            event (dict, optional): New match event (goal, card, etc.)
            
        Returns:
            dict: Updated live analysis
        """
        old_minute = self.match_minute
        self.match_minute = minute
        
        if score:
            old_score = self.score.copy()
            self.score = score
            
            # Check for goal event
            if old_score[0] != score[0] or old_score[1] != score[1]:
                # Goal event detected
                goal_team = "home" if old_score[0] != score[0] else "away"
                goal_minute = minute
                
                # Add to key events
                self.key_events.append({
                    'type': 'goal',
                    'team': goal_team,
                    'minute': goal_minute,
                    'score': score.copy()
                })
                
                # Log goal event
                self.log_activity("Goal scored", f"{goal_team.capitalize()} team, minute {goal_minute}, score: {score[0]}-{score[1]}")
        
        if event:
            self.key_events.append(event)
            self.log_activity(f"{event.get('type', 'Event')} recorded", f"Minute {minute}, {event.get('details', '')}")
        
        # Determine if significant time has passed (for analysis refresh)
        time_threshold = 5  # Minutes
        if minute - old_minute >= time_threshold or score or event:
            return self.update_live_analysis()
        
        return None
    
    def update_live_analysis(self):
        """
        Run updated analysis based on current match state
        
        Returns:
            dict: Current live prediction and analysis
        """
        if not self.is_active or not self.current_match:
            return {"error": "No active match tracking"}
        
        # Update match_data with current state
        match_data = self.current_match.copy()
        match_data['current_minute'] = self.match_minute
        match_data['current_score'] = self.score
        match_data['key_events'] = self.key_events
        
        # Initialize analysis structure
        analysis = {
            'match': f"{match_data.get('home_team', '')} vs {match_data.get('away_team', '')}",
            'minute': self.match_minute,
            'score': self.score,
            'predictions': {},
            'confidence': 0.0,
            'modules_active': [],
            'factors': []
        }
        
        # Generate hash from current match state for consistent but varied results
        # This is for demonstration; in production, we'd use real analysis
        state_key = f"{match_data.get('home_team', '')}_{match_data.get('away_team', '')}_{self.match_minute}_{self.score[0]}_{self.score[1]}"
        seed_value = abs(hash(state_key)) % (2**32 - 1)
        random.seed(seed_value)
        
        # Run each specialized live module with match_phase awareness
        module_results = {}
        for module_name, module_func in self.live_modules.items():
            try:
                result = module_func(match_data)
                module_results[module_name] = result
                analysis['modules_active'].append(module_name)
                
                # Extract factors from module result
                if 'factors' in result:
                    analysis['factors'].extend(result['factors'])
            except Exception as e:
                self.log_activity(f"Error in {module_name}", str(e))
        
        # Determine match phase for different prediction strategies
        match_phase = self.determine_match_phase(self.match_minute)
        
        # Weighted integration of module results
        confidence_score = 0
        prediction_weights = {}
        
        for module_name, result in module_results.items():
            module_weight = self.live_weights.get(module_name, 0.1)
            
            # Adjust weights based on match phase
            if match_phase == 'early' and module_name in ['karmic_flow', 'mirror_phase']:
                module_weight *= 1.3  # Boost pattern-based early prediction
            elif match_phase == 'mid' and module_name in ['shadow_momentum', 'bet_pulse']:
                module_weight *= 1.2  # Boost market-based mid-game prediction
            elif match_phase == 'late' and module_name in ['clutch_time_scanner', 'shadow_momentum']:
                module_weight *= 1.5  # Boost momentum-based late game prediction
            
            # Combine confidence scores
            if 'confidence' in result:
                confidence_score += result['confidence'] * module_weight
            
            # Track prediction weights
            if 'prediction' in result:
                for pred, pred_conf in result['prediction'].items():
                    if pred not in prediction_weights:
                        prediction_weights[pred] = 0
                    prediction_weights[pred] += pred_conf * module_weight
        
        # Normalize confidence score
        total_weight = sum(self.live_weights.values())
        confidence_score = min(1.0, confidence_score / total_weight)
        
        # Normalize prediction weights
        total_pred_weight = sum(prediction_weights.values())
        if total_pred_weight > 0:
            for pred in prediction_weights:
                prediction_weights[pred] /= total_pred_weight
        
        # Set final analysis values
        analysis['confidence'] = confidence_score
        analysis['predictions'] = prediction_weights
        
        # Store prediction in history
        self.predictions_history.append({
            'minute': self.match_minute,
            'confidence': confidence_score,
            'predictions': prediction_weights.copy(),
            'timestamp': datetime.now()
        })
        
        self.log_activity("Analysis updated", f"Minute {self.match_minute}, confidence: {confidence_score:.2f}")
        
        return analysis
    
    def stop_live_tracking(self):
        """
        Stop live tracking and return final analysis
        
        Returns:
            dict: Final analysis results and tracking summary
        """
        if not self.is_active:
            return {"error": "No active match tracking"}
        
        final_analysis = self.update_live_analysis()
        final_analysis['tracking_summary'] = {
            'duration_minutes': self.match_minute,
            'key_events_count': len(self.key_events),
            'analysis_updates': len(self.predictions_history),
            'final_score': self.score
        }
        
        self.is_active = False
        self.log_activity("Stopped live tracking", f"Final score: {self.score[0]}-{self.score[1]}")
        
        return final_analysis
    
    # Individual live analysis modules
    
    def shadow_momentum_analysis(self, match_data):
        """
        ShadowMomentum: Detects subtle momentum shifts in betting patterns and match dynamics
        
        Args:
            match_data (dict): Current match information
            
        Returns:
            dict: Momentum analysis results
        """
        # In a real system, this would analyze actual betting data and match statistics
        # For demonstration, we'll simulate momentum based on match time and score
        
        minute = match_data.get('current_minute', 0)
        score = match_data.get('current_score', [0, 0])
        
        # Generate a momentum value between -1.0 (away team) and 1.0 (home team)
        # This simulates the feeling of which team has momentum
        
        # Base momentum slightly favors home team
        base_momentum = 0.1
        
        # Score influence
        score_diff = score[0] - score[1]
        if score_diff > 0:
            momentum_score = 0.3 * score_diff  # Home team leads
        elif score_diff < 0:
            momentum_score = 0.3 * score_diff  # Away team leads
        else:
            momentum_score = 0  # Tied game
        
        # Time influence - later in game, momentum becomes more significant
        time_factor = min(1.0, minute / 90.0)
        
        # Random component (would be real data in production)
        random_component = (random.random() * 0.4) - 0.2
        
        # Combine factors
        momentum = base_momentum + momentum_score + (random_component * time_factor)
        # Ensure within range
        momentum = max(-1.0, min(1.0, momentum))
        
        # Determine momentum direction and strength
        if momentum > 0.2:
            direction = 'home'
            strength = momentum
        elif momentum < -0.2:
            direction = 'away'
            strength = abs(momentum)
        else:
            direction = 'neutral'
            strength = abs(momentum)
        
        # Confidence based on strength and time
        confidence = strength * (0.6 + 0.4 * time_factor)
        
        # Determine prediction based on momentum
        prediction = {}
        if direction == 'home' and strength > self.momentum_threshold:
            if score[0] > score[1]:  # Home already leading
                prediction['home_win'] = 0.7 * strength
                prediction['draw'] = 0.2 * strength
            else:  # Home not leading yet
                prediction['home_win'] = 0.4 * strength
                prediction['draw'] = 0.4 * strength
        elif direction == 'away' and strength > self.momentum_threshold:
            if score[1] > score[0]:  # Away already leading
                prediction['away_win'] = 0.7 * strength
                prediction['draw'] = 0.2 * strength
            else:  # Away not leading yet
                prediction['away_win'] = 0.4 * strength
                prediction['draw'] = 0.4 * strength
        else:
            # No strong momentum
            prediction['draw'] = 0.5
            prediction['home_win'] = 0.25
            prediction['away_win'] = 0.25
        
        return {
            'momentum_direction': direction,
            'momentum_strength': strength,
            'confidence': confidence,
            'prediction': prediction,
            'factors': [
                {
                    'name': 'Momentum Direction',
                    'value': f"{direction.capitalize()} team momentum ({strength:.2f})",
                    'type': 'odds'
                },
                {
                    'name': 'Momentum Intensity',
                    'value': f"{'Strong' if strength > 0.7 else 'Moderate' if strength > 0.4 else 'Weak'} {direction} momentum",
                    'type': 'odds'
                }
            ]
        }
    
    def bet_pulse_analysis(self, match_data):
        """
        BetPulse: Analyzes betting volume and timing patterns
        
        Args:
            match_data (dict): Current match information
            
        Returns:
            dict: Betting pulse analysis results
        """
        # Simulated betting volume data - would be real in production
        minute = match_data.get('current_minute', 0)
        
        # Calculate key betting metrics
        base_volume = 100  # Base volume units
        
        # Volume spikes at key moments (kickoff, halftime, late game)
        if minute < 5:
            volume_factor = 2.0  # High volume at kickoff
        elif 42 <= minute <= 47:
            volume_factor = 2.5  # High volume around halftime
        elif minute > 80:
            volume_factor = 3.0  # High volume late game
        else:
            volume_factor = 1.0
        
        # Random component for variability
        random_factor = 0.7 + (random.random() * 0.6)
        
        # Current betting volume
        current_volume = base_volume * volume_factor * random_factor
        
        # Public betting percentages (home/draw/away)
        public_bet_home = 0.45 + (random.random() * 0.2) - 0.1
        public_bet_draw = 0.25 + (random.random() * 0.1) - 0.05
        public_bet_away = 1.0 - public_bet_home - public_bet_draw
        
        # Check for betting surge compared to baseline
        surge_ratio = current_volume / base_volume
        
        is_surge = surge_ratio > self.betting_surge_threshold
        
        # Determine if public is heavily favoring one outcome
        public_skew = max(public_bet_home, public_bet_draw, public_bet_away)
        is_skewed = public_skew > 0.6
        
        # Analysis confidence
        confidence = min(1.0, (surge_ratio / 3.0) * (0.5 + 0.5 * (minute / 90)))
        
        # Predictions based on betting patterns
        prediction = {}
        
        if is_surge and is_skewed:
            # Significant betting action with skew - consider potential contrarian play
            if public_bet_home > 0.6:
                # Public heavy on home - potential value on draw/away
                prediction['draw'] = 0.35
                prediction['away_win'] = 0.45
                prediction['home_win'] = 0.2
            elif public_bet_away > 0.6:
                # Public heavy on away - potential value on draw/home
                prediction['draw'] = 0.35
                prediction['home_win'] = 0.45
                prediction['away_win'] = 0.2
            else:
                # Public heavy on draw - unusual, suggests volatile match
                prediction['home_win'] = 0.4
                prediction['away_win'] = 0.4
                prediction['draw'] = 0.2
        else:
            # No strong signal from betting patterns
            prediction['home_win'] = 0.4
            prediction['draw'] = 0.3
            prediction['away_win'] = 0.3
        
        return {
            'betting_volume': current_volume,
            'surge_ratio': surge_ratio,
            'is_surge': is_surge,
            'public_bet_home': public_bet_home,
            'public_bet_draw': public_bet_draw,
            'public_bet_away': public_bet_away,
            'is_skewed': is_skewed,
            'confidence': confidence,
            'prediction': prediction,
            'factors': [
                {
                    'name': 'Betting Volume',
                    'value': f"{'Surge' if is_surge else 'Normal'} betting volume ({surge_ratio:.1f}x baseline)",
                    'type': 'odds'
                },
                {
                    'name': 'Public Betting',
                    'value': f"Home: {public_bet_home:.0%}, Draw: {public_bet_draw:.0%}, Away: {public_bet_away:.0%}",
                    'type': 'odds'
                }
            ]
        }
    
    def line_trap_analysis(self, match_data):
        """
        LineTrap: Identifies odds that appear to be traps
        
        Args:
            match_data (dict): Current match information
            
        Returns:
            dict: Line trap analysis results
        """
        # For demonstration purposes - would use real odds movements in production
        minute = match_data.get('current_minute', 0)
        score = match_data.get('current_score', [0, 0])
        
        # Generate simulated odds data
        # Starting odds
        initial_odds = {
            'home_win': match_data.get('initial_odds_home', 2.10),
            'draw': match_data.get('initial_odds_draw', 3.25),
            'away_win': match_data.get('initial_odds_away', 3.50)
        }
        
        # Current odds - adjusted based on score and time
        current_odds = initial_odds.copy()
        
        # Score impact on odds
        score_diff = score[0] - score[1]
        
        if score_diff > 0:  # Home team leading
            current_odds['home_win'] *= max(0.7, 1.0 - (score_diff * 0.15))
            current_odds['away_win'] *= min(1.8, 1.0 + (score_diff * 0.25))
        elif score_diff < 0:  # Away team leading
            current_odds['away_win'] *= max(0.7, 1.0 - (abs(score_diff) * 0.15))
            current_odds['home_win'] *= min(1.8, 1.0 + (abs(score_diff) * 0.25))
        
        # Time impact - as game progresses, odds shift more dramatically
        time_factor = minute / 90.0
        
        # More randomness for demonstration
        random_shift = (random.random() * 0.3) - 0.15
        
        # Apply random shift
        for key in current_odds:
            current_odds[key] *= (1 + (random_shift * time_factor))
            current_odds[key] = round(current_odds[key], 2)  # Round to reasonable odds format
        
        # Calculate odds movements
        odds_movement = {
            key: ((current_odds[key] - initial_odds[key]) / initial_odds[key])
            for key in initial_odds
        }
        
        # Look for potential trap situations
        traps = []
        trap_confidence = 0.0
        
        # Trap scenario 1: Line moves against the score
        if score_diff > 0 and odds_movement['home_win'] > 0:
            # Home team is winning but their odds are increasing (unusual)
            traps.append({
                'type': 'score_odds_mismatch',
                'description': 'Home team leading but odds increasing',
                'trap_on': 'home_win'
            })
            trap_confidence = max(trap_confidence, abs(odds_movement['home_win']) * 0.7)
        
        elif score_diff < 0 and odds_movement['away_win'] > 0:
            # Away team is winning but their odds are increasing (unusual)
            traps.append({
                'type': 'score_odds_mismatch',
                'description': 'Away team leading but odds increasing',
                'trap_on': 'away_win'
            })
            trap_confidence = max(trap_confidence, abs(odds_movement['away_win']) * 0.7)
        
        # Trap scenario 2: Odds move dramatically without score change
        for outcome, movement in odds_movement.items():
            if abs(movement) > self.line_movement_threshold and score_diff == 0:
                traps.append({
                    'type': 'significant_movement',
                    'description': f'Large odds shift on {outcome} without score change',
                    'trap_on': outcome
                })
                trap_confidence = max(trap_confidence, abs(movement) * 0.8)
        
        # Build prediction based on trap analysis
        prediction = {}
        if traps:
            # If we've detected a potential trap, bet against it
            for trap in traps:
                trap_on = trap['trap_on']
                if trap_on == 'home_win':
                    prediction['draw'] = 0.40
                    prediction['away_win'] = 0.45
                    prediction['home_win'] = 0.15
                elif trap_on == 'away_win':
                    prediction['draw'] = 0.40
                    prediction['home_win'] = 0.45
                    prediction['away_win'] = 0.15
                elif trap_on == 'draw':
                    # If draw odds look like a trap, predict a decisive result
                    prediction['home_win'] = 0.50
                    prediction['away_win'] = 0.40
                    prediction['draw'] = 0.10
        else:
            # No traps detected, default even prediction
            prediction = {
                'home_win': 0.35,
                'draw': 0.30,
                'away_win': 0.35
            }
        
        return {
            'initial_odds': initial_odds,
            'current_odds': current_odds,
            'odds_movement': odds_movement,
            'traps_detected': traps,
            'confidence': trap_confidence if traps else 0.3,
            'prediction': prediction,
            'factors': [
                {
                    'name': 'Odds Movement',
                    'value': f"Home: {odds_movement['home_win']:+.1%}, Draw: {odds_movement['draw']:+.1%}, Away: {odds_movement['away_win']:+.1%}",
                    'type': 'odds'
                },
                {
                    'name': 'Trap Detection',
                    'value': f"{'Potential trap detected on ' + traps[0]['trap_on'] if traps else 'No traps detected'}",
                    'type': 'odds'
                }
            ]
        }
    
    def karmic_flow_analysis(self, match_data):
        """
        KarmicFlow: Detects karmic patterns in team confrontations
        
        Args:
            match_data (dict): Current match information
            
        Returns:
            dict: Karmic analysis results
        """
        # This would use historical data and esoteric analysis in production
        minute = match_data.get('current_minute', 0)
        score = match_data.get('current_score', [0, 0])
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # Generate a karmic pattern based on teams and match state
        # In production, this would analyze historical context, revenge factors, etc.
        
        # Hash the team names for consistent karmic values
        home_hash = abs(hash(home_team)) % 100
        away_hash = abs(hash(away_team)) % 100
        
        # Karmic balance (-1.0 to 1.0) where positive favors home team
        karmic_base = (home_hash - away_hash) / 100.0
        
        # Karmic factors - would be real in production
        karmic_modifiers = []
        
        # Factor 1: "Revenge" narrative if one team lost the last meeting
        revenge_factor = 0
        if random.random() < 0.5:  # Simulate prior match result
            revenge_factor = 0.2 * (1 if random.random() < 0.5 else -1)
            karmic_modifiers.append({
                'name': 'Revenge Narrative',
                'value': f"{'Home' if revenge_factor > 0 else 'Away'} team seeking redemption",
                'impact': revenge_factor
            })
        
        # Factor 2: "Due for a win" if team has had several losses
        due_factor = 0
        if random.random() < 0.5:
            due_factor = 0.15 * (1 if random.random() < 0.5 else -1)
            karmic_modifiers.append({
                'name': 'Karmic Balance',
                'value': f"{'Home' if due_factor > 0 else 'Away'} team due for a result shift",
                'impact': due_factor
            })
        
        # Factor 3: "Destiny match" - special significance for team
        destiny_factor = 0
        if random.random() < 0.3:
            destiny_factor = 0.25 * (1 if random.random() < 0.5 else -1)
            karmic_modifiers.append({
                'name': 'Destiny Match',
                'value': f"{'Home' if destiny_factor > 0 else 'Away'} team at karmic turning point",
                'impact': destiny_factor
            })
        
        # Calculate total karmic balance
        karmic_balance = karmic_base
        for mod in karmic_modifiers:
            karmic_balance += mod['impact']
        
        # Keep within range
        karmic_balance = max(-1.0, min(1.0, karmic_balance))
        
        # Karmic confidence increases as the game progresses
        time_factor = (minute / 90.0) ** 0.5  # Square root for non-linear scaling
        
        # More confidence if multiple karmic factors align
        modifiers_count = len(karmic_modifiers)
        modifiers_confidence = min(1.0, modifiers_count * 0.2)
        
        # Overall confidence
        confidence = 0.3 + (0.4 * abs(karmic_balance)) + (0.3 * modifiers_confidence * time_factor)
        
        # Karmic prediction based on balance
        prediction = {}
        if karmic_balance > 0.2:
            # Karma favors home team
            prediction['home_win'] = 0.5 + (0.3 * karmic_balance)
            prediction['draw'] = 0.3 - (0.15 * karmic_balance)
            prediction['away_win'] = 0.2 - (0.15 * karmic_balance)
        elif karmic_balance < -0.2:
            # Karma favors away team
            prediction['away_win'] = 0.5 + (0.3 * abs(karmic_balance))
            prediction['draw'] = 0.3 - (0.15 * abs(karmic_balance))
            prediction['home_win'] = 0.2 - (0.15 * abs(karmic_balance))
        else:
            # Balanced karma
            prediction['home_win'] = 0.35
            prediction['draw'] = 0.35
            prediction['away_win'] = 0.30
        
        return {
            'karmic_balance': karmic_balance,
            'karmic_modifiers': karmic_modifiers,
            'confidence': confidence,
            'prediction': prediction,
            'factors': [
                {
                    'name': 'Karmic Balance',
                    'value': f"{'Favorable to Home' if karmic_balance > 0.2 else 'Favorable to Away' if karmic_balance < -0.2 else 'Balanced'} ({karmic_balance:.2f})",
                    'type': 'esoteric'
                }
            ] + [
                {
                    'name': mod['name'],
                    'value': mod['value'],
                    'type': 'esoteric'
                }
                for mod in karmic_modifiers
            ]
        }
    
    def mirror_phase_analysis(self, match_data):
        """
        MirrorPhase: Synchronizes cycles and patterns
        
        Args:
            match_data (dict): Current match information
            
        Returns:
            dict: Pattern synchronization results
        """
        # In production, this would analyze historical patterns and cycle alignment
        minute = match_data.get('current_minute', 0)
        score = match_data.get('current_score', [0, 0])
        
        # Check for "mirror matches" - similar historical scenarios
        # Simulated for demonstration
        
        # Mirror match probability (higher = stronger historical precedent)
        mirror_probability = random.random() * 0.8
        
        # Identified pattern types
        pattern_types = []
        
        if mirror_probability > 0.7:
            # Strong historical match found
            pattern_types.append({
                'name': 'Historical Echo',
                'description': 'Very similar match conditions to historical precedent',
                'similarity': mirror_probability
            })
        
        elif mirror_probability > 0.5:
            # Moderate pattern match
            pattern_types.append({
                'name': 'Pattern Resonance',
                'description': 'Partial alignment with historical pattern',
                'similarity': mirror_probability
            })
        
        # Check for timing patterns (critical minutes)
        critical_minutes = [15, 30, 45, 60, 75, 85]
        nearest_critical = min(critical_minutes, key=lambda x: abs(x - minute))
        time_proximity = 1.0 - (abs(nearest_critical - minute) / 15.0)
        
        if time_proximity > 0.8:
            # Near a critical game minute
            pattern_types.append({
                'name': 'Critical Minute',
                'description': f'Approaching critical minute {nearest_critical}',
                'similarity': time_proximity
            })
        
        # Score pattern (would use historical data in production)
        if score[0] == score[1]:
            # Tied game - check for late equalizer pattern
            if minute > 70:
                pattern_types.append({
                    'name': 'Late Equilibrium',
                    'description': 'Tied late in match - unstable equilibrium pattern',
                    'similarity': 0.6 + (0.3 * (minute - 70) / 20)
                })
        
        # Calculate overall pattern strength and direction
        if pattern_types:
            avg_similarity = sum(p['similarity'] for p in pattern_types) / len(pattern_types)
            
            # Direction of pattern (-1.0 to 1.0) - would be derived from historical data
            # Positive = favors home, Negative = favors away
            pattern_direction = (random.random() * 2.0) - 1.0
            
            # Confidence based on pattern strength and number of patterns
            confidence = avg_similarity * min(1.0, len(pattern_types) * 0.4)
            
            # Generate prediction based on pattern
            prediction = {}
            
            if pattern_direction > 0.2:
                # Pattern favors home
                prediction['home_win'] = 0.5 + (0.3 * pattern_direction)
                prediction['draw'] = 0.3 - (0.15 * pattern_direction)
                prediction['away_win'] = 0.2 - (0.15 * pattern_direction)
            elif pattern_direction < -0.2:
                # Pattern favors away
                prediction['away_win'] = 0.5 + (0.3 * abs(pattern_direction))
                prediction['draw'] = 0.3 - (0.15 * abs(pattern_direction))
                prediction['home_win'] = 0.2 - (0.15 * abs(pattern_direction))
            else:
                # Balanced pattern
                prediction['home_win'] = 0.35
                prediction['draw'] = 0.35
                prediction['away_win'] = 0.30
        else:
            # No strong patterns detected
            pattern_direction = 0
            confidence = 0.2
            prediction = {'home_win': 0.33, 'draw': 0.34, 'away_win': 0.33}
        
        return {
            'patterns_detected': pattern_types,
            'pattern_direction': pattern_direction if pattern_types else 0,
            'confidence': confidence,
            'prediction': prediction,
            'factors': [
                {
                    'name': 'Pattern Strength',
                    'value': f"{'Strong' if confidence > 0.7 else 'Moderate' if confidence > 0.4 else 'Weak'} pattern detection ({confidence:.2f})",
                    'type': 'esoteric'
                }
            ] + [
                {
                    'name': p['name'],
                    'value': p['description'],
                    'type': 'esoteric'
                }
                for p in pattern_types
            ]
        }
    
    def clutch_time_analysis(self, match_data):
        """
        ClutchTimeScanner: Identifies critical moments in the match
        
        Args:
            match_data (dict): Current match information
            
        Returns:
            dict: Clutch time analysis results
        """
        minute = match_data.get('current_minute', 0)
        score = match_data.get('current_score', [0, 0])
        
        # Define clutch time periods - critical phases when important events happen
        clutch_periods = [
            {'start': 40, 'end': 45, 'name': 'End of First Half', 'intensity': 0.7},
            {'start': 45, 'end': 50, 'name': 'Start of Second Half', 'intensity': 0.6},
            {'start': 70, 'end': 80, 'name': 'Championship Minutes', 'intensity': 0.8},
            {'start': 85, 'end': 90, 'name': 'Final Countdown', 'intensity': 0.9}
        ]
        
        # Check if current minute is in a clutch period
        active_clutch = None
        for period in clutch_periods:
            if period['start'] <= minute <= period['end']:
                active_clutch = period
                break
        
        # If in clutch time, analyze the situation
        if active_clutch:
            # Clutch time detected
            clutch_name = active_clutch['name']
            clutch_intensity = active_clutch['intensity']
            
            # Proximity to center of clutch period (higher = more critical)
            period_center = (active_clutch['start'] + active_clutch['end']) / 2
            proximity = 1.0 - (abs(minute - period_center) / ((active_clutch['end'] - active_clutch['start']) / 2))
            
            # Score impact on clutch significance
            score_diff = abs(score[0] - score[1])
            if score_diff == 0:
                # Tied game in clutch time - highly significant
                score_factor = 1.0
            elif score_diff == 1:
                # One goal difference - still significant
                score_factor = 0.8
            else:
                # Larger difference - less critical
                score_factor = max(0.3, 1.0 - (score_diff - 1) * 0.25)
            
            # Calculate overall clutch significance
            clutch_significance = clutch_intensity * proximity * score_factor
            
            # Determine which team benefits from the clutch situation
            # In a tied game, slight home advantage
            # If a team is ahead by 1, the trailing team is under pressure to score
            clutch_benefit = 0  # -1.0 (away) to 1.0 (home)
            
            if score[0] == score[1]:
                # Tied - slight home advantage
                clutch_benefit = 0.1
            elif score[0] > score[1]:
                # Home leading - away needs to score
                if minute < 70:
                    # Still time - pressure on away
                    clutch_benefit = 0.3
                else:
                    # Late game - home defending lead
                    clutch_benefit = -0.2
            elif score[0] < score[1]:
                # Away leading - home needs to score
                if minute < 70:
                    # Still time - pressure on home
                    clutch_benefit = -0.3
                else:
                    # Late game - away defending lead
                    clutch_benefit = 0.2
            
            # Clutch time confidence based on significance
            confidence = clutch_significance
            
            # Generate prediction based on clutch analysis
            prediction = {}
            
            if clutch_benefit > 0.2:
                # Clutch favors home
                prediction['home_win'] = 0.45 + (0.2 * clutch_benefit)
                prediction['draw'] = 0.30
                prediction['away_win'] = 0.25 - (0.2 * clutch_benefit)
            elif clutch_benefit < -0.2:
                # Clutch favors away
                prediction['away_win'] = 0.45 + (0.2 * abs(clutch_benefit))
                prediction['draw'] = 0.30
                prediction['home_win'] = 0.25 - (0.2 * abs(clutch_benefit))
            else:
                # Neutral clutch impact
                prediction['home_win'] = 0.35
                prediction['draw'] = 0.35
                prediction['away_win'] = 0.30
        else:
            # Not in a clutch period
            clutch_name = "Normal Play"
            clutch_significance = 0.2
            clutch_benefit = 0
            confidence = 0.2
            prediction = {'home_win': 0.33, 'draw': 0.34, 'away_win': 0.33}
        
        return {
            'clutch_period': clutch_name,
            'clutch_significance': clutch_significance if active_clutch else 0,
            'clutch_benefit': clutch_benefit,
            'confidence': confidence,
            'prediction': prediction,
            'factors': [
                {
                    'name': 'Match Phase',
                    'value': clutch_name,
                    'type': 'statistical'
                },
                {
                    'name': 'Critical Moment',
                    'value': f"{'High' if active_clutch and clutch_significance > 0.7 else 'Moderate' if active_clutch and clutch_significance > 0.4 else 'Low'} criticality phase",
                    'type': 'statistical'
                }
            ] if active_clutch else [
                {
                    'name': 'Match Phase',
                    'value': "Standard play - no critical phase detected",
                    'type': 'statistical'
                }
            ]
        }
    
    def determine_match_phase(self, minute):
        """
        Helper method to determine which phase of the match we are in
        
        Args:
            minute (int): Current match minute
            
        Returns:
            str: Match phase ('early', 'mid', or 'late')
        """
        if minute < 30:
            return 'early'
        elif minute < 70:
            return 'mid'
        else:
            return 'late'
    
    def log_activity(self, action, details):
        """
        Log an activity in the sentinel's activity log
        
        Args:
            action (str): The action or event
            details (str): Additional details
        """
        self.activity_log.append({
            'timestamp': datetime.now(),
            'action': action,
            'details': details
        })
        
        # Would potentially log to database or notification system in production
        print(f"ArcanSentinel: {action} - {details}")
        
    def get_activity_log(self):
        """
        Get the complete activity log
        
        Returns:
            list: Activity log entries
        """
        return self.activity_log