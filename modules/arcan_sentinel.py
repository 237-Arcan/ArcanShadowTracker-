"""
ArcanSentinel - Lightweight real-time analysis module for ArcanShadow
Provides fast, reactive analysis for live matches
"""

import time
import random
import math
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
            'early_phase': {  # 0-30 minutes
                'shadow_momentum': 0.15,
                'bet_pulse': 0.25,
                'line_trap': 0.30,
                'karmic_flow': 0.10,
                'mirror_phase': 0.10,
                'clutch_time_scanner': 0.10
            },
            'mid_phase': {  # 31-60 minutes
                'shadow_momentum': 0.25,
                'bet_pulse': 0.20,
                'line_trap': 0.15,
                'karmic_flow': 0.15,
                'mirror_phase': 0.15,
                'clutch_time_scanner': 0.10
            },
            'late_phase': {  # 61-90 minutes
                'shadow_momentum': 0.30,
                'bet_pulse': 0.15,
                'line_trap': 0.10,
                'karmic_flow': 0.15,
                'mirror_phase': 0.10,
                'clutch_time_scanner': 0.20
            }
        }
        
        # Live tracking metrics
        self.activity_log = []
        self.start_time = None

        # Shadow momentum data for tracking
        self.momentum_timeline = []
        
        # Betting data for visualization
        self.betting_volumes = {
            'home': [],
            'draw': [],
            'away': []
        }
    
    def start_live_tracking(self, match_data):
        """
        Start real-time tracking of a match
        
        Args:
            match_data (dict): Initial match information
            
        Returns:
            dict: Initial live analysis results
        """
        # Set tracking state
        self.is_active = True
        self.current_match = match_data
        self.match_minute = 0
        self.score = [0, 0]
        self.key_events = []
        self.predictions_history = []
        self.start_time = datetime.now()
        
        # Initialize momentum and betting data
        self.momentum_timeline = [0.5]  # Start at neutral
        
        self.betting_volumes = {
            'home': [],
            'draw': [],
            'away': []
        }
        
        # Log activity
        self.log_activity('start_tracking', f"Started tracking match: {match_data['home_team']} vs {match_data['away_team']}")
        
        # Run initial analysis
        initial_analysis = self.update_live_analysis()
        
        # Store initial prediction
        self.predictions_history.append({
            'minute': self.match_minute,
            'prediction': initial_analysis['outcome'],
            'confidence': initial_analysis['confidence']
        })
        
        return initial_analysis
    
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
        if not self.is_active:
            return {"error": "No active match tracking"}
        
        # Update match time
        prev_phase = self.determine_match_phase(self.match_minute)
        self.match_minute = minute
        new_phase = self.determine_match_phase(minute)
        
        # Log phase transition if it occurred
        if prev_phase != new_phase:
            self.log_activity('phase_change', f"Match entered {new_phase} phase at minute {minute}")
        
        # Update score if provided
        if score is not None:
            if score != self.score:
                self.log_activity('score_update', f"Score changed from {self.score[0]}-{self.score[1]} to {score[0]}-{score[1]}")
                self.score = score
        
        # Add event if provided
        if event is not None:
            self.key_events.append({
                'minute': minute,
                'type': event['type'],
                'team': event['team'],
                'details': event['details']
            })
            self.log_activity('event_recorded', f"{event['type']} for {event['team']} at minute {minute}: {event['details']}")
        
        # Update tracking metrics
        new_analysis = self.update_live_analysis()
        
        # Store prediction
        self.predictions_history.append({
            'minute': minute,
            'prediction': new_analysis['outcome'],
            'confidence': new_analysis['confidence']
        })
        
        return new_analysis
    
    def update_live_analysis(self):
        """
        Run updated analysis based on current match state
        
        Returns:
            dict: Current live prediction and analysis
        """
        if not self.is_active:
            return {"error": "No active match tracking"}
        
        # Create current match state to analyze
        if self.current_match is None:
            return {"error": "Match data not initialized"}
            
        current_state = self.current_match.copy()
        current_state['minute'] = self.match_minute
        current_state['score'] = self.score
        current_state['key_events'] = self.key_events
        
        # Get results from core modules
        arcan_x_results = self.arcan_x.analyze_match(current_state)
        shadow_odds_results = self.shadow_odds.analyze_match(current_state)
        
        # Generate base prediction from convergence module
        base_prediction = self.convergence.generate_prediction(
            current_state,
            arcan_x_results,
            shadow_odds_results
        )
        
        # Run specialized live analysis modules
        live_module_results = {}
        current_phase = self.determine_match_phase(self.match_minute)
        
        for module_name, analysis_func in self.live_modules.items():
            live_module_results[module_name] = analysis_func(current_state)
        
        # Calculate adjusted confidence based on live modules
        adjusted_confidence = base_prediction['confidence']
        confidence_adjustments = 0
        
        for module_name, result in live_module_results.items():
            module_weight = self.live_weights[current_phase][module_name]
            if 'confidence_adjustment' in result:
                confidence_adjustments += result['confidence_adjustment'] * module_weight
        
        # Apply adjustment, ensuring it stays within [0,1]
        adjusted_confidence = max(0.0, min(1.0, adjusted_confidence + confidence_adjustments))
        
        # Generate bet pulse update
        bet_pulse_data = live_module_results['bet_pulse']
        if 'volume_data' in bet_pulse_data:
            self.betting_volumes['home'].append(bet_pulse_data['volume_data']['home'])
            self.betting_volumes['draw'].append(bet_pulse_data['volume_data']['draw'])
            self.betting_volumes['away'].append(bet_pulse_data['volume_data']['away'])
        
        # Update momentum timeline
        if 'current_momentum' in live_module_results['shadow_momentum']:
            self.momentum_timeline.append(live_module_results['shadow_momentum']['current_momentum'])
        
        # Final result
        result = {
            'minute': self.match_minute,
            'score': self.score,
            'phase': current_phase,
            'outcome': base_prediction['outcome'],
            'confidence': adjusted_confidence,
            'factors': [],  # Initialize empty factors list
            'esoteric_factors': base_prediction.get('esoteric_factors', []),
            'odds_factors': base_prediction.get('odds_factors', []),
            'statistical_factors': base_prediction.get('statistical_factors', [])
        }
        
        # Add live module results
        for module_name, module_result in live_module_results.items():
            result[module_name] = module_result
        
        # Add momentum timeline
        if 'shadow_momentum' in result:
            result['shadow_momentum']['momentum_timeline'] = self.momentum_timeline
        
        # Add betting volume timeline
        if 'bet_pulse' in result:
            time_points = list(range(0, len(self.betting_volumes['home'])))
            home_values = self.betting_volumes['home']
            draw_values = self.betting_volumes['draw']
            away_values = self.betting_volumes['away']
            
            result['bet_pulse']['volume_timeline'] = []
            for i in range(len(time_points)):
                result['bet_pulse']['volume_timeline'].append({
                    'minute': time_points[i],
                    'home': home_values[i],
                    'draw': draw_values[i],
                    'away': away_values[i]
                })
        
        return result
    
    def stop_live_tracking(self):
        """
        Stop live tracking and return final analysis
        
        Returns:
            dict: Final analysis results and tracking summary
        """
        if not self.is_active:
            return {"error": "No active match tracking"}
        
        final_analysis = self.update_live_analysis()
        if isinstance(final_analysis, dict) and 'error' not in final_analysis:
            final_analysis['tracking_summary'] = {
                'duration_minutes': self.match_minute,
                'key_events_count': len(self.key_events),
                'analysis_updates': len(self.predictions_history),
                'final_score': self.score
            }
        
        # Log activity
        self.log_activity('stop_tracking', f"Stopped tracking match at minute {self.match_minute} with score {self.score[0]}-{self.score[1]}")
        
        # Reset tracking state
        self.is_active = False
        
        return final_analysis
    
    def shadow_momentum_analysis(self, match_data):
        """
        ShadowMomentum: Detects subtle momentum shifts in betting patterns and match dynamics
        
        Args:
            match_data (dict): Current match information
            
        Returns:
            dict: Momentum analysis results
        """
        # Calculate base momentum using match state
        minute = match_data['minute']
        score = match_data['score']
        events = match_data['key_events'] if 'key_events' in match_data else []
        
        # Start with home advantage as slight base momentum
        base_momentum = 0.52  # Slightly favors home team
        
        # Adjust for score
        if score[0] > score[1]:
            # Home team leading
            base_momentum += 0.05 * (score[0] - score[1])
        elif score[1] > score[0]:
            # Away team leading
            base_momentum -= 0.05 * (score[1] - score[0])
        
        # Adjust for recent events (last 10 minutes)
        recent_events = [e for e in events if minute - e['minute'] <= 10]
        for event in recent_events:
            if event['type'] == 'Goal':
                momentum_shift = 0.15
                if event['team'] == match_data['home_team']:
                    base_momentum += momentum_shift
                else:
                    base_momentum -= momentum_shift
            elif event['type'] == 'Red Card':
                momentum_shift = 0.20
                if event['team'] == match_data['home_team']:
                    base_momentum -= momentum_shift
                else:
                    base_momentum += momentum_shift
            elif event['type'] == 'Yellow Card':
                momentum_shift = 0.05
                if event['team'] == match_data['home_team']:
                    base_momentum -= momentum_shift
                else:
                    base_momentum += momentum_shift
        
        # Add some randomness to simulate real-world fluctuations
        random_factor = random.uniform(-0.05, 0.05)
        momentum = max(0.0, min(1.0, base_momentum + random_factor))
        
        # Calculate impact on prediction confidence
        momentum_difference = abs(0.5 - momentum)
        confidence_adjustment = momentum_difference * 0.2  # Max ±0.1 confidence adjustment
        
        # Determine which team has momentum
        team_with_momentum = match_data['home_team'] if momentum > 0.55 else match_data['away_team'] if momentum < 0.45 else "Neutral"
        
        # Generate factors to report
        factors = []
        if momentum > 0.7:
            factors.append(f"Strong momentum for {match_data['home_team']}")
        elif momentum > 0.6:
            factors.append(f"Good momentum for {match_data['home_team']}")
        elif momentum < 0.3:
            factors.append(f"Strong momentum for {match_data['away_team']}")
        elif momentum < 0.4:
            factors.append(f"Good momentum for {match_data['away_team']}")
        else:
            factors.append("Balanced momentum")
        
        # Add score-based factors
        if score[0] > score[1]:
            factors.append(f"{match_data['home_team']} leading {score[0]}-{score[1]}")
        elif score[1] > score[0]:
            factors.append(f"{match_data['away_team']} leading {score[1]}-{score[0]}")
        
        # Add time-based factors
        phase = self.determine_match_phase(minute)
        if phase == "late_phase" and abs(score[0] - score[1]) <= 1:
            factors.append("Close match in final phase")
        
        return {
            'current_momentum': momentum,
            'confidence_adjustment': confidence_adjustment,
            'team_with_momentum': team_with_momentum,
            'factors': factors
        }
    
    def bet_pulse_analysis(self, match_data):
        """
        BetPulse: Analyzes betting volume and timing patterns
        
        Args:
            match_data (dict): Current match information
            
        Returns:
            dict: Betting pulse analysis results
        """
        minute = match_data['minute']
        score = match_data['score']
        
        # Base volumes that evolve based on match state
        if minute == 0:
            # Initial volumes based on pre-match odds
            home_odds = match_data.get('home_odds', 2.0)
            draw_odds = match_data.get('draw_odds', 3.0)
            away_odds = match_data.get('away_odds', 4.0)
            
            # Convert odds to approximate bet volumes (inverse relationship)
            total = (1/home_odds) + (1/draw_odds) + (1/away_odds)
            home_pct = (1/home_odds) / total * 100
            draw_pct = (1/draw_odds) / total * 100
            away_pct = (1/away_odds) / total * 100
        else:
            # Evolve volumes based on score and time
            if score[0] > score[1]:
                # Home team leading - bets shift to home and draw
                home_pct = 45 + (score[0] - score[1]) * 5
                draw_pct = 35 - (score[0] - score[1]) * 3
                away_pct = 20 - (score[0] - score[1]) * 2
            elif score[1] > score[0]:
                # Away team leading - bets shift to away and draw
                home_pct = 30 - (score[1] - score[0]) * 3
                draw_pct = 35 - (score[1] - score[0]) * 2
                away_pct = 35 + (score[1] - score[0]) * 5
            else:
                # Tied game - bets more even with draw favored as game progresses
                draw_weight = min(50, 30 + minute // 10)
                remainder = 100 - draw_weight
                home_pct = remainder * 0.55  # Slight home advantage
                away_pct = remainder * 0.45
                draw_pct = draw_weight
        
        # Add randomness
        random_shift = random.uniform(-3, 3)
        home_pct += random_shift
        draw_pct -= random_shift/2
        away_pct -= random_shift/2
        
        # Normalize to ensure they sum to 100%
        total = home_pct + draw_pct + away_pct
        home_pct = (home_pct / total) * 100
        draw_pct = (draw_pct / total) * 100
        away_pct = (away_pct / total) * 100
        
        # Calculate changes from "previous" period (simulated)
        home_change = random.uniform(-2, 2) + (1 if score[0] > score[1] else -1 if score[1] > score[0] else 0)
        draw_change = random.uniform(-1.5, 1.5) - abs(score[0] - score[1])
        away_change = random.uniform(-2, 2) + (1 if score[1] > score[0] else -1 if score[0] > score[1] else 0)
        
        # Generate confidence adjustment based on bet volumes
        # If bets heavily favor one outcome, increase confidence
        max_volume = max(home_pct, draw_pct, away_pct)
        volume_difference = max_volume - ((home_pct + draw_pct + away_pct - max_volume) / 2)
        confidence_adjustment = (volume_difference - 20) / 100  # Normalized to reasonable range
        
        # Generate factors to report
        factors = []
        if home_pct > 50:
            factors.append(f"High betting volume on {match_data['home_team']} win ({home_pct:.1f}%)")
        elif away_pct > 50:
            factors.append(f"High betting volume on {match_data['away_team']} win ({away_pct:.1f}%)")
        elif draw_pct > 50:
            factors.append(f"High betting volume on draw ({draw_pct:.1f}%)")
        
        if abs(home_change) > 5:
            factors.append(f"Sharp {home_change:.1f}% change in {match_data['home_team']} betting volume")
        if abs(away_change) > 5:
            factors.append(f"Sharp {away_change:.1f}% change in {match_data['away_team']} betting volume")
        
        return {
            'confidence_adjustment': confidence_adjustment,
            'home_volume': round(home_pct, 1),
            'draw_volume': round(draw_pct, 1),
            'away_volume': round(away_pct, 1),
            'home_change': round(home_change, 1),
            'draw_change': round(draw_change, 1),
            'away_change': round(away_change, 1),
            'volume_data': {
                'home': round(home_pct, 1),
                'draw': round(draw_pct, 1),
                'away': round(away_pct, 1)
            },
            'factors': factors
        }
    
    def line_trap_analysis(self, match_data):
        """
        LineTrap: Identifies odds that appear to be traps
        
        Args:
            match_data (dict): Current match information
            
        Returns:
            dict: Line trap analysis results
        """
        # For now, a simplified implementation
        minute = match_data['minute']
        score = match_data['score']
        
        # Random trap detection with some logic
        trap_probability = random.uniform(0, 0.3)  # Base chance
        
        # Increase trap probability in certain scenarios
        if score[0] == score[1] and minute > 70:
            # Late game tie often has trap odds
            trap_probability += 0.2
        
        if abs(score[0] - score[1]) == 1 and minute > 80:
            # One goal difference late in game
            trap_probability += 0.15
        
        # Randomly choose which outcome might be a trap
        if trap_probability > 0.3:
            trap_outcome = random.choice(["home", "draw", "away"])
            trap_severity = random.uniform(0.4, 0.8)
            confidence_adjustment = -0.05 if trap_probability > 0.4 else -0.02
            
            if trap_outcome == "home":
                description = f"Possible odds trap on {match_data['home_team']} win"
            elif trap_outcome == "away":
                description = f"Possible odds trap on {match_data['away_team']} win"
            else:
                description = "Possible odds trap on draw"
                
            factors = [
                description,
                f"Trap probability: {trap_probability*100:.1f}%",
                f"Severity: {trap_severity*100:.1f}%"
            ]
        else:
            trap_outcome = "none"
            trap_severity = 0
            confidence_adjustment = 0.01
            factors = ["No significant trap patterns detected"]
        
        return {
            'trap_detected': trap_probability > 0.3,
            'trap_outcome': trap_outcome,
            'trap_probability': trap_probability,
            'trap_severity': trap_severity,
            'confidence_adjustment': confidence_adjustment,
            'factors': factors
        }
    
    def karmic_flow_analysis(self, match_data):
        """
        KarmicFlow: Detects karmic patterns in team confrontations
        
        Args:
            match_data (dict): Current match information
            
        Returns:
            dict: Karmic analysis results
        """
        minute = match_data['minute']
        score = match_data['score']
        
        # Generate a karmic balance value (-1 to 1) where negative favors away team
        # Initial balance slightly favors home team (home advantage)
        karmic_seed = hash(match_data['home_team'] + match_data['away_team']) % 1000 / 1000
        karmic_balance = 0.1 + (karmic_seed - 0.5) * 0.3  # Range about -0.05 to 0.25
        
        # Adjust based on current match state
        if score[0] > score[1]:
            # Home team leading - karmic balance shifts away from them
            karmic_balance -= 0.1 * (score[0] - score[1])
        elif score[1] > score[0]:
            # Away team leading - karmic balance shifts away from them
            karmic_balance += 0.1 * (score[1] - score[0])
        
        # Time effect - karma intensifies late in the match
        time_factor = 1.0 + (minute / 90) * 0.5  # Up to 50% stronger late in the game
        karmic_balance *= time_factor
        
        # Ensure it stays in range
        karmic_balance = max(-1.0, min(1.0, karmic_balance))
        
        # Calculate confidence adjustment
        confidence_adjustment = abs(karmic_balance) * 0.1  # Max ±0.1
        if karmic_balance > 0.2:
            factors = [f"Karmic flow favors {match_data['home_team']}"]
            if karmic_balance > 0.5:
                factors.append("Strong karmic resonance detected")
        elif karmic_balance < -0.2:
            factors = [f"Karmic flow favors {match_data['away_team']}"]
            if karmic_balance < -0.5:
                factors.append("Strong karmic resonance detected")
        else:
            factors = ["Neutral karmic balance"]
        
        # Add match phase context
        phase = self.determine_match_phase(minute)
        if phase == "late_phase" and abs(karmic_balance) > 0.4:
            factors.append("Late game karmic shift imminent")
        
        return {
            'balance': karmic_balance,
            'confidence_adjustment': confidence_adjustment,
            'factors': factors
        }
    
    def mirror_phase_analysis(self, match_data):
        """
        MirrorPhase: Synchronizes cycles and patterns
        
        Args:
            match_data (dict): Current match information
            
        Returns:
            dict: Pattern synchronization results
        """
        minute = match_data['minute']
        
        # Calculate synchronicity value
        synchronicity = (math.sin(minute/15) + 1) / 2  # Oscillating value between 0-1
        
        # Add randomness
        synchronicity = max(0, min(1, synchronicity + random.uniform(-0.1, 0.1)))
        
        # Determine phase alignment
        if synchronicity > 0.7:
            alignment = "Strong Alignment"
            confidence_adjustment = 0.08
            factors = ["High pattern synchronicity detected", 
                      "Statistical and esoteric indicators aligned"]
        elif synchronicity > 0.5:
            alignment = "Moderate Alignment"
            confidence_adjustment = 0.04
            factors = ["Moderate pattern synchronicity",
                      "Some alignment between indicators"]
        else:
            alignment = "Weak Alignment"
            confidence_adjustment = -0.02
            factors = ["Low pattern synchronicity",
                      "Divergence between statistical and esoteric indicators"]
        
        return {
            'synchronicity': synchronicity,
            'alignment': alignment,
            'confidence_adjustment': confidence_adjustment,
            'factors': factors
        }
    
    def clutch_time_analysis(self, match_data):
        """
        ClutchTimeScanner: Identifies critical moments in the match
        
        Args:
            match_data (dict): Current match information
            
        Returns:
            dict: Clutch time analysis results
        """
        minute = match_data['minute']
        score = match_data['score']
        
        # Determine if this is clutch time
        is_clutch_time = False
        clutch_factor = 0.0
        
        # End of first half approaching
        if 40 <= minute <= 45:
            is_clutch_time = True
            clutch_factor = 0.5
        
        # End of match approaching
        if minute >= 80:
            is_clutch_time = True
            clutch_factor = 0.8
        
        # Close score makes it more clutch
        if abs(score[0] - score[1]) <= 1:
            clutch_factor += 0.2
        
        # Generate team clutch ratings (0-1)
        home_clutch = random.uniform(0.5, 0.9)  # Simplified - would use team history
        away_clutch = random.uniform(0.5, 0.9)
        
        # Determine which team performs better in clutch situations
        better_clutch_team = match_data['home_team'] if home_clutch > away_clutch else match_data['away_team']
        
        # Calculate confidence adjustment
        if is_clutch_time:
            # Favor the team with better clutch rating
            clutch_diff = abs(home_clutch - away_clutch)
            confidence_adjustment = clutch_diff * clutch_factor * 0.2
            if home_clutch > away_clutch:
                confidence_adjustment = abs(confidence_adjustment)  # Positive for home
            else:
                confidence_adjustment = -abs(confidence_adjustment)  # Negative for away
            
            factors = [
                "Critical match moment detected",
                f"{better_clutch_team} shows stronger clutch performance"
            ]
            
            if minute >= 85 and abs(score[0] - score[1]) <= 1:
                factors.append("High pressure final minutes")
        else:
            confidence_adjustment = 0
            factors = ["No critical match moment currently"]
        
        return {
            'is_clutch_time': is_clutch_time,
            'clutch_factor': clutch_factor,
            'home_clutch_rating': home_clutch,
            'away_clutch_rating': away_clutch,
            'better_clutch_team': better_clutch_team,
            'confidence_adjustment': confidence_adjustment,
            'factors': factors
        }
    
    def determine_match_phase(self, minute):
        """
        Helper method to determine which phase of the match we are in
        
        Args:
            minute (int): Current match minute
            
        Returns:
            str: Match phase ('early', 'mid', or 'late')
        """
        if minute <= 30:
            return "early_phase"
        elif minute <= 60:
            return "mid_phase"
        else:
            return "late_phase"
    
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
    
    def get_activity_log(self):
        """
        Get the complete activity log
        
        Returns:
            list: Activity log entries
        """
        return self.activity_log