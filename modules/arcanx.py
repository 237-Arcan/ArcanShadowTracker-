import numpy as np
import pandas as pd
from datetime import datetime
import math
import os
from utils.api_integrations import APIIntegrations

class ArcanX:
    """
    ArcanX module - Handles esoteric analysis component of the ArcanShadow system.
    Fuses esoteric disciplines with statistical data to generate prediction signals.
    """
    
    def __init__(self):
        self.submodules = {
            'NumeriCode': self.numeri_code,
            'GematriaPulse': self.gematria_pulse,
            'AstroImpact': self.astro_impact,
            'TarotEcho': self.tarot_echo,
            'YiFlow': self.yi_flow,
            'KarmicFlow': self.karmic_flow,
            'RadiEsthesiaMap': self.radiesthesia_map,
            'CycleMirror': self.cycle_mirror
        }
        
        # Initialize API integrations
        self.api = APIIntegrations()
        
        # Initialize gematria values for common names in sports
        self.gematria_values = self._initialize_gematria_values()
        
        # Initialize numerological prime values
        self.numerological_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        
        # Initialize tarot associations
        self.tarot_associations = self._initialize_tarot_associations()
        
        # Initialize hexagram data
        self.hexagrams = self._initialize_hexagrams()
        
        # Cache for results to avoid redundant calculations
        self.cache = {}
    
    def analyze_match(self, match_data):
        """
        Main method to analyze a match using esoteric principles.
        Returns a dictionary with confidence scores and influential factors.
        
        Args:
            match_data (dict): Match information including teams, date, league, etc.
            
        Returns:
            dict: Results of the esoteric analysis with confidence scores and factors
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
            'NumeriCode': 0.15,
            'GematriaPulse': 0.12,
            'AstroImpact': 0.13,
            'TarotEcho': 0.10,
            'YiFlow': 0.10,
            'KarmicFlow': 0.15,
            'RadiEsthesiaMap': 0.10,
            'CycleMirror': 0.15
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
    
    def numeri_code(self, match_data):
        """
        NumeriCode module: Analyzes numerical patterns in the match data.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Numerical analysis results
        """
        result = {
            'confidence': 0.5,  # Default neutral confidence
            'factors': []
        }
        
        # Extract date for numerological analysis
        match_date = match_data.get('date', datetime.now())
        
        # Calculate day number (1-31)
        day_number = match_date.day
        
        # Calculate life path number (numerology)
        # Convert date to format YYYYMMDD and sum all digits
        date_string = match_date.strftime('%Y%m%d')
        life_path = sum(int(digit) for digit in date_string)
        
        # Reduce to single digit (except master numbers 11, 22, 33)
        while life_path > 9 and life_path not in [11, 22, 33]:
            life_path = sum(int(digit) for digit in str(life_path))
        
        # Check if day_number is prime
        is_day_prime = day_number in self.numerological_primes
        
        # Check resonance with team formation if available
        home_formation = match_data.get('home_formation', '4-4-2')
        away_formation = match_data.get('away_formation', '4-4-2')
        
        # Extract first digit of each formation
        try:
            home_first_digit = int(home_formation[0])
            away_first_digit = int(away_formation[0])
            formation_sum = home_first_digit + away_first_digit
            
            # Check if formation sum has numerological significance
            formation_significant = formation_sum in [3, 7, 9, 11]
        except (ValueError, IndexError):
            formation_sum = 0
            formation_significant = False
        
        # Add factors to result
        if is_day_prime:
            result['factors'].append({
                'name': 'Prime Match Day',
                'value': f"Match occurs on day {day_number}, a prime number"
            })
            result['confidence'] += 0.05
        
        if life_path in [1, 3, 5, 7, 9]:
            result['factors'].append({
                'name': 'Dynamic Life Path',
                'value': f"Match Life Path {life_path} suggests action/change"
            })
            result['confidence'] += 0.07
        elif life_path in [2, 4, 6, 8]:
            result['factors'].append({
                'name': 'Stable Life Path',
                'value': f"Match Life Path {life_path} suggests stability/defense"
            })
            result['confidence'] -= 0.03  # Less predictable outcomes
        
        if life_path in [11, 22, 33]:
            result['factors'].append({
                'name': 'Master Number Day',
                'value': f"Match on Master Number {life_path} - heightened energy"
            })
            result['confidence'] += 0.1
        
        if formation_significant:
            result['factors'].append({
                'name': 'Formation Resonance',
                'value': f"Team formations create significant sum {formation_sum}"
            })
            result['confidence'] += 0.04
        
        # Normalize confidence to be between 0 and 1
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def gematria_pulse(self, match_data):
        """
        GematriaPulse module: Analyzes kabbalistic values of team names, players, etc.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Gematria analysis results
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # Extract team names
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # Calculate gematria values
        home_gematria = self._calculate_gematria(home_team)
        away_gematria = self._calculate_gematria(away_team)
        
        # Analyze stadium name if available
        stadium = match_data.get('stadium', '')
        stadium_gematria = self._calculate_gematria(stadium)
        
        # Check for harmonic resonances between values
        home_away_diff = abs(home_gematria - away_gematria)
        
        # Calculate resonance factor (0 to 1)
        resonance = 0
        
        # Check if difference is a fibonacci number (1,1,2,3,5,8,13,21,34,55,89)
        fibonacci = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        if home_away_diff in fibonacci:
            result['factors'].append({
                'name': 'Fibonacci Resonance',
                'value': f"Team names create Fibonacci difference {home_away_diff}"
            })
            resonance += 0.15
        
        # Check for prime number resonance
        if home_gematria in self.numerological_primes or away_gematria in self.numerological_primes:
            result['factors'].append({
                'name': 'Prime Gematria',
                'value': f"Team name has Prime Gematria value"
            })
            resonance += 0.1
        
        # Check if home/away values form a "golden" ratio (~1.618)
        if max(home_gematria, away_gematria) > 0:
            ratio = max(home_gematria, away_gematria) / min(home_gematria, away_gematria) if min(home_gematria, away_gematria) > 0 else 0
            if 1.5 < ratio < 1.7:
                result['factors'].append({
                    'name': 'Golden Ratio',
                    'value': f"Team names create near-Golden Ratio ({ratio:.3f})"
                })
                resonance += 0.2
        
        # Stadium influence if stadium has strong gematria
        if stadium_gematria > 0:
            stadium_resonance = (stadium_gematria % 9) / 9  # Normalized 0-1 value
            if stadium_resonance > 0.7:
                result['factors'].append({
                    'name': 'Stadium Influence',
                    'value': f"Stadium has high gematria resonance ({stadium_resonance:.2f})"
                })
                resonance += 0.12
        
        # Update confidence based on total resonance
        result['confidence'] += resonance
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def astro_impact(self, match_data):
        """
        AstroImpact Lite module: Analyzes astrological influences on the match.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Astrological analysis results
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # Extract match date
        match_date = match_data.get('date', datetime.now())
        
        # Simplified astrological analysis based on sun sign
        sun_sign = self._get_sun_sign(match_date.month, match_date.day)
        
        # Define elemental qualities of signs
        fire_signs = ['Aries', 'Leo', 'Sagittarius']
        earth_signs = ['Taurus', 'Virgo', 'Capricorn']
        air_signs = ['Gemini', 'Libra', 'Aquarius']
        water_signs = ['Cancer', 'Scorpio', 'Pisces']
        
        # Determine match character based on sun sign
        if sun_sign in fire_signs:
            result['factors'].append({
                'name': 'Fire Element Match',
                'value': f"Match under {sun_sign} - high energy, offensive"
            })
            # Fire signs tend to produce more goals and action
            result['confidence'] += 0.08
        
        elif sun_sign in earth_signs:
            result['factors'].append({
                'name': 'Earth Element Match',
                'value': f"Match under {sun_sign} - stable, defensive"
            })
            # Earth signs tend to produce more predictable, structured matches
            result['confidence'] += 0.12
        
        elif sun_sign in air_signs:
            result['factors'].append({
                'name': 'Air Element Match',
                'value': f"Match under {sun_sign} - variable, tactical"
            })
            # Air signs can be unpredictable
            result['confidence'] -= 0.05
        
        elif sun_sign in water_signs:
            result['factors'].append({
                'name': 'Water Element Match',
                'value': f"Match under {sun_sign} - emotional, flowing"
            })
            # Water signs can lead to emotional matches
            result['confidence'] += 0.03
        
        # Check for Mercury retrograde (simplified - just use a date range)
        # Note: In a real system, this would use ephemeris data
        retrograde_periods_2023 = [
            (datetime(2023, 12, 13), datetime(2024, 1, 1)),
            (datetime(2023, 8, 23), datetime(2023, 9, 15)),
            (datetime(2023, 4, 21), datetime(2023, 5, 14)),
            (datetime(2022, 12, 29), datetime(2023, 1, 18))
        ]
        
        in_retrograde = any(start <= match_date <= end for start, end in retrograde_periods_2023)
        
        if in_retrograde:
            result['factors'].append({
                'name': 'Mercury Retrograde',
                'value': "Match during Mercury Retrograde - expect surprises"
            })
            # More unpredictable during retrograde
            result['confidence'] -= 0.1
        
        # Check for full/new moon proximity (simplified)
        moon_phase = self._calculate_moon_phase(match_date)
        
        if 0.95 <= moon_phase <= 1.0 or 0.0 <= moon_phase <= 0.05:
            result['factors'].append({
                'name': 'New Moon Energy',
                'value': "Match near New Moon - beginning of cycle"
            })
            result['confidence'] += 0.06
        
        if 0.45 <= moon_phase <= 0.55:
            result['factors'].append({
                'name': 'Full Moon Energy',
                'value': "Match near Full Moon - heightened energy"
            })
            result['confidence'] -= 0.08  # More unpredictable/emotional
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def tarot_echo(self, match_data):
        """
        TarotEcho module: Uses tarot symbolism to evaluate match energies.
        In a real implementation, this would use more sophisticated algorithms.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Tarot symbolic analysis results
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # Use match date to derive a "tarot seed"
        match_date = match_data.get('date', datetime.now())
        date_seed = int(match_date.strftime('%Y%m%d'))
        
        # Extract team names for additional seed factors
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # Use name lengths as additional factors
        home_length = len(home_team)
        away_length = len(away_team)
        
        # Generate pseudo-random number for card selection
        # Ensure the seed is within valid range (0 to 2^32 - 1)
        seed_value = abs(date_seed + home_length + away_length) % (2**32 - 1)
        np.random.seed(seed_value)
        
        # Select three "cards" for past-present-future of the match
        major_arcana = list(range(0, 22))  # 0-21 for Major Arcana
        selected_cards = np.random.choice(major_arcana, 3, replace=False)
        
        # Map numbers to card names and meanings
        card_names = [
            "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
            "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
            "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
            "The Devil", "The Tower", "The Star", "The Moon", "The Sun",
            "Judgement", "The World"
        ]
        
        # Cards and their meanings for matches
        match_meanings = [
            "Unpredictable outcome, new beginnings",  # Fool
            "Strategic advantage, skill prevails",  # Magician
            "Hidden factors, intuition needed",  # High Priestess
            "Nurturing environment, home advantage",  # Empress
            "Authority, established power dominates",  # Emperor
            "Traditional approach, experience wins",  # Hierophant
            "Partnership, cooperation key",  # Lovers
            "Victory through determination",  # Chariot
            "Inner strength overcomes challenges",  # Strength
            "Careful analysis, defensive match",  # Hermit
            "Changing fortunes, unpredictable",  # Wheel
            "Fair outcome, balanced forces",  # Justice
            "Sacrifice needed, delayed result",  # Hanged Man
            "Transformation, end of a cycle",  # Death
            "Balance, moderation in play",  # Temperance
            "Trapped in negative patterns",  # Devil
            "Sudden change, disruption",  # Tower
            "Hope, inspiration, renewal",  # Star
            "Illusion, deception, uncertainty",  # Moon
            "Success, vitality, positive outcome",  # Sun
            "Evaluation, critical moment",  # Judgement
            "Completion, fulfilled potential"  # World
        ]
        
        # Interpret the cards for the match
        past_card = card_names[selected_cards[0]]
        present_card = card_names[selected_cards[1]]
        future_card = card_names[selected_cards[2]]
        
        past_meaning = match_meanings[selected_cards[0]]
        present_meaning = match_meanings[selected_cards[1]]
        future_meaning = match_meanings[selected_cards[2]]
        
        # Add interpretations to factors
        result['factors'].append({
            'name': 'Match Foundation',
            'value': f"{past_card}: {past_meaning}"
        })
        
        result['factors'].append({
            'name': 'Current Energy',
            'value': f"{present_card}: {present_meaning}"
        })
        
        result['factors'].append({
            'name': 'Outcome Tendency',
            'value': f"{future_card}: {future_meaning}"
        })
        
        # Adjust confidence based on the nature of the cards
        positive_cards = [1, 3, 4, 6, 7, 8, 10, 11, 14, 17, 19, 21]  # Cards that suggest clearer outcomes
        negative_cards = [12, 15, 16, 18]  # Cards that suggest uncertainty
        
        # Adjust confidence based on card combination
        confidence_adjustment = 0
        
        # Check future card
        if selected_cards[2] in positive_cards:
            confidence_adjustment += 0.15
        elif selected_cards[2] in negative_cards:
            confidence_adjustment -= 0.15
        
        # Check present card
        if selected_cards[1] in positive_cards:
            confidence_adjustment += 0.1
        elif selected_cards[1] in negative_cards:
            confidence_adjustment -= 0.1
        
        # Special combinations
        if 9 in selected_cards and 18 in selected_cards:  # Hermit + Moon: deep uncertainty
            confidence_adjustment -= 0.2
            result['factors'].append({
                'name': 'Profound Uncertainty',
                'value': f"The Hermit and Moon combination suggests hidden factors"
            })
        
        if 19 in selected_cards and 7 in selected_cards:  # Sun + Chariot: strong victory energy
            confidence_adjustment += 0.2
            result['factors'].append({
                'name': 'Victory Combination',
                'value': f"The Sun and Chariot combination suggests clear outcome"
            })
        
        # Update overall confidence
        result['confidence'] += confidence_adjustment
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def yi_flow(self, match_data):
        """
        YiFlow module: Applies I Ching hexagrams to match dynamics.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: I Ching analysis results
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # Generate hexagram based on match data
        match_date = match_data.get('date', datetime.now())
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # Create seed from date and team names
        date_seed = int(match_date.strftime('%Y%m%d'))
        name_seed = sum(ord(c) for c in home_team + away_team)
        seed = date_seed + name_seed
        
        # Generate hexagram (6 lines, each yin or yang)
        # Ensure the seed is within valid range (0 to 2^32 - 1)
        seed_value = abs(seed) % (2**32 - 1)
        np.random.seed(seed_value)
        lines = np.random.choice([6, 7, 8, 9], 6)  # Traditional I Ching line values
        
        # Convert to binary (0 for yin, 1 for yang)
        binary_lines = [(line % 2 == 1) for line in lines]
        
        # Calculate hexagram number (1-64)
        # Convert binary to decimal, add 1 (I Ching hexagrams are 1-indexed)
        lower_trigram = 0
        for i in range(3):
            lower_trigram = (lower_trigram << 1) | binary_lines[i+3]
        
        upper_trigram = 0
        for i in range(3):
            upper_trigram = (upper_trigram << 1) | binary_lines[i]
        
        hexagram_index = (upper_trigram * 8) + lower_trigram
        
        # Get hexagram information
        hexagram = self.hexagrams[hexagram_index]
        
        # Add hexagram to factors
        result['factors'].append({
            'name': 'Match Hexagram',
            'value': f"{hexagram['number']}. {hexagram['name']} - {hexagram['meaning']}"
        })
        
        # Analyze changing lines
        changing_lines = [i for i, line in enumerate(lines) if line == 6 or line == 9]
        
        if changing_lines:
            line_positions = [6-i for i in changing_lines]  # Convert to traditional line numbering
            result['factors'].append({
                'name': 'Changing Lines',
                'value': f"Lines {', '.join(map(str, line_positions))} are in transition"
            })
        
        # Adjust confidence based on hexagram nature
        # Some hexagrams are more decisive, others suggest uncertainty
        
        # Decisive hexagrams suggest clearer outcomes
        decisive_hexagrams = [1, 10, 14, 16, 25, 30, 34, 43]
        
        # Uncertain hexagrams suggest more unpredictable situations
        uncertain_hexagrams = [6, 29, 36, 38, 47, 59, 60, 61]
        
        if hexagram['number'] in decisive_hexagrams:
            result['confidence'] += 0.15
            result['factors'].append({
                'name': 'Decisive Energy',
                'value': f"Hexagram {hexagram['number']} suggests clear outcome potential"
            })
            
        if hexagram['number'] in uncertain_hexagrams:
            result['confidence'] -= 0.15
            result['factors'].append({
                'name': 'Uncertain Energy',
                'value': f"Hexagram {hexagram['number']} suggests unpredictable scenario"
            })
        
        # If there are changing lines, add a second hexagram
        if changing_lines:
            # Create the new hexagram by changing the lines
            new_binary_lines = binary_lines.copy()
            for i in changing_lines:
                new_binary_lines[i] = not new_binary_lines[i]
            
            # Calculate new hexagram number
            new_lower_trigram = 0
            for i in range(3):
                new_lower_trigram = (new_lower_trigram << 1) | new_binary_lines[i+3]
            
            new_upper_trigram = 0
            for i in range(3):
                new_upper_trigram = (new_upper_trigram << 1) | new_binary_lines[i]
            
            new_hexagram_index = (new_upper_trigram * 8) + new_lower_trigram
            
            # Get new hexagram information
            new_hexagram = self.hexagrams[new_hexagram_index]
            
            # Add to factors
            result['factors'].append({
                'name': 'Transforming Into',
                'value': f"{new_hexagram['number']}. {new_hexagram['name']} - {new_hexagram['meaning']}"
            })
            
            # If transforming from uncertain to decisive or vice versa, adjust confidence
            if hexagram['number'] in uncertain_hexagrams and new_hexagram['number'] in decisive_hexagrams:
                result['confidence'] += 0.1
            elif hexagram['number'] in decisive_hexagrams and new_hexagram['number'] in uncertain_hexagrams:
                result['confidence'] -= 0.1
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def karmic_flow(self, match_data):
        """
        KarmicFlow+ module: Detects karmic patterns in team confrontations.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Karmic analysis results
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # Extract team history data if available
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # First, try to get real head-to-head data from the API
        api_h2h = None
        if self.api.api_sports_available and home_team and away_team:
            try:
                api_h2h = self.api.get_head_to_head(home_team, away_team, last_n_matches=10)
                if api_h2h:
                    print(f"Retrieved real head-to-head data for {home_team} vs {away_team}")
            except Exception as e:
                print(f"Error getting head-to-head data: {e}")
        
        # If we have API data, convert it to our format
        if api_h2h and 'matches' in api_h2h:
            # Convert API data to our historical_matchups format
            history = []
            for match in api_h2h['matches']:
                # Parse the score, format is typically "1 - 0"
                score_parts = match.get('score', '0 - 0').split(' - ')
                if len(score_parts) == 2:
                    try:
                        home_score = int(score_parts[0])
                        away_score = int(score_parts[1])
                        
                        # Determine if home team was first in the score (depends on API format)
                        if match.get('result', '').startswith(home_team):
                            # Home team was first
                            pass
                        elif match.get('result', '').startswith(away_team):
                            # Away team was first, swap scores
                            home_score, away_score = away_score, home_score
                        
                        historical_match = {
                            'date': match.get('date'),
                            'competition': match.get('competition'),
                            'venue': match.get('venue'),
                            'home_score': home_score,
                            'away_score': away_score
                        }
                        history.append(historical_match)
                    except ValueError:
                        # Skip if we can't parse the score
                        pass
        else:
            # Use the historical matchups from match_data as fallback
            history = match_data.get('historical_matchups', [])
        
        if not history:
            # No history available, use simplified analysis
            result['factors'].append({
                'name': 'Karmic Analysis',
                'value': "Attempting to retrieve historical data for karmic analysis"
            })
            return result
        
        # Find patterns in historical matchups
        
        # Count wins for each team
        home_wins = sum(1 for match in history if match.get('home_score', 0) > match.get('away_score', 0))
        away_wins = sum(1 for match in history if match.get('home_score', 0) < match.get('away_score', 0))
        draws = len(history) - home_wins - away_wins
        
        # Calculate win percentages
        total_matches = len(history)
        home_win_pct = home_wins / total_matches if total_matches > 0 else 0
        away_win_pct = away_wins / total_matches if total_matches > 0 else 0
        draw_pct = draws / total_matches if total_matches > 0 else 0
        
        # Check for dominant team (over 70% win rate)
        if home_win_pct > 0.7:
            result['factors'].append({
                'name': 'Historical Dominance',
                'value': f"{home_team} has won {home_win_pct:.0%} of matches against {away_team}"
            })
            result['confidence'] += 0.15
        
        if away_win_pct > 0.7:
            result['factors'].append({
                'name': 'Historical Dominance',
                'value': f"{away_team} has won {away_win_pct:.0%} of matches against {home_team}"
            })
            result['confidence'] += 0.15
        
        # Check for very balanced history (signs of karmic balance)
        if 0.4 <= home_win_pct <= 0.6 and 0.4 <= away_win_pct <= 0.6:
            result['factors'].append({
                'name': 'Karmic Balance',
                'value': f"Teams have a balanced historical record ({home_win_pct:.0%} vs {away_win_pct:.0%})"
            })
            result['confidence'] -= 0.1  # More unpredictable
        
        # Check for revenge factor (team lost last match)
        if history and len(history) > 0:
            last_match = history[0]  # Assuming most recent first
            home_last_score = last_match.get('home_score', 0)
            away_last_score = last_match.get('away_score', 0)
            
            if home_last_score < away_last_score:
                result['factors'].append({
                    'name': 'Revenge Factor',
                    'value': f"{home_team} lost the last match and seeks revenge"
                })
                result['confidence'] += 0.08
            
            if home_last_score > away_last_score:
                result['factors'].append({
                    'name': 'Revenge Factor',
                    'value': f"{away_team} lost the last match and seeks revenge"
                })
                result['confidence'] += 0.08
        
        # Check for winning/losing streaks (karmic momentum)
        if len(history) >= 3:
            # Check last 3 matches
            recent_matches = history[:3]
            
            # Count recent home team wins
            recent_home_wins = sum(1 for match in recent_matches 
                               if match.get('home_score', 0) > match.get('away_score', 0))
            
            # Count recent away team wins
            recent_away_wins = sum(1 for match in recent_matches 
                               if match.get('home_score', 0) < match.get('away_score', 0))
            
            # Check for streaks
            if recent_home_wins == 3:
                result['factors'].append({
                    'name': 'Win Streak',
                    'value': f"{home_team} has won the last 3 matches - strong positive karma"
                })
                result['confidence'] += 0.12
            
            if recent_away_wins == 3:
                result['factors'].append({
                    'name': 'Win Streak',
                    'value': f"{away_team} has won the last 3 matches - strong positive karma"
                })
                result['confidence'] += 0.12
            
            # Check for alternating pattern (perfect karmic balance)
            results_pattern = []
            for match in recent_matches:
                if match.get('home_score', 0) > match.get('away_score', 0):
                    results_pattern.append('H')
                elif match.get('home_score', 0) < match.get('away_score', 0):
                    results_pattern.append('A')
                else:
                    results_pattern.append('D')
            
            if results_pattern == ['H', 'A', 'H'] or results_pattern == ['A', 'H', 'A']:
                result['factors'].append({
                    'name': 'Alternating Pattern',
                    'value': "Teams show perfect alternating win pattern - karmic cycle"
                })
                result['confidence'] += 0.15
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def radiesthesia_map(self, match_data):
        """
        RadiEsthesiaMap module: Analyzes venue energy and its impact.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Venue energy analysis results
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # Extract venue information
        stadium = match_data.get('stadium', '')
        city = match_data.get('city', '')
        country = match_data.get('country', '')
        
        if not stadium and not city:
            result['factors'].append({
                'name': 'Venue Energy',
                'value': "Insufficient venue data for analysis"
            })
            return result
        
        # Using stadium name and location for a simplified radiesthetic analysis
        stadium_energy = 0
        
        # Calculate "energy" based on name length and characters
        if stadium:
            # Use the sum of character codes as an "energy signature"
            stadium_energy = sum(ord(c) for c in stadium) % 100 / 100
        
        # Add city influence
        city_energy = 0
        if city:
            city_energy = sum(ord(c) for c in city) % 100 / 100
        
        # Combined energy value
        venue_energy = (stadium_energy * 0.7) + (city_energy * 0.3)
        
        # Classify energy level
        if venue_energy > 0.8:
            energy_level = "Very High"
            result['factors'].append({
                'name': 'Venue Energy',
                'value': f"{stadium} has very high energy - intense atmosphere"
            })
            result['confidence'] -= 0.1  # More unpredictable in high energy venues
        
        elif venue_energy > 0.6:
            energy_level = "High"
            result['factors'].append({
                'name': 'Venue Energy',
                'value': f"{stadium} has high energy - advantage to confident teams"
            })
            result['confidence'] += 0.05
        
        elif venue_energy > 0.4:
            energy_level = "Balanced"
            result['factors'].append({
                'name': 'Venue Energy',
                'value': f"{stadium} has balanced energy - neutral impact"
            })
            # No confidence adjustment for balanced energy
        
        elif venue_energy > 0.2:
            energy_level = "Low"
            result['factors'].append({
                'name': 'Venue Energy',
                'value': f"{stadium} has low energy - technical teams favored"
            })
            result['confidence'] += 0.08
        
        else:
            energy_level = "Very Low"
            result['factors'].append({
                'name': 'Venue Energy',
                'value': f"{stadium} has very low energy - strategic approach favored"
            })
            result['confidence'] += 0.1
        
        # Check stadium orientation (using a simplified approach)
        # In a real implementation, this would use actual geographic data
        orientation_factor = hash(stadium) % 4 if stadium else 0
        
        orientations = ["North-South", "East-West", "Northeast-Southwest", "Northwest-Southeast"]
        orientation = orientations[orientation_factor]
        
        result['factors'].append({
            'name': 'Stadium Orientation',
            'value': f"Approximate {orientation} orientation"
        })
        
        # Check for water bodies nearby (simplified)
        # In a real implementation, this would use geographic data
        has_water_nearby = hash(city) % 3 == 0 if city else False
        
        if has_water_nearby:
            result['factors'].append({
                'name': 'Water Influence',
                'value': "Water body near stadium - fluid, flowing energy"
            })
            result['confidence'] -= 0.05  # More unpredictable
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def cycle_mirror(self, match_data):
        """
        CycleMirror module: Detects cyclical patterns in match history.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Cyclical analysis results
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # Extract historical data
        history = match_data.get('historical_matchups', [])
        
        if not history or len(history) < 5:
            result['factors'].append({
                'name': 'Cycle Analysis',
                'value': "Insufficient historical data for cycle detection"
            })
            return result
        
        # Extract date and result patterns
        dates = [match.get('date', datetime.now()) for match in history]
        
        # Extract results as simple codes
        results = []
        for match in history:
            home_score = match.get('home_score', 0)
            away_score = match.get('away_score', 0)
            
            if home_score > away_score:
                results.append('H')  # Home win
            elif home_score < away_score:
                results.append('A')  # Away win
            else:
                results.append('D')  # Draw
        
        # Check for seasonal patterns
        seasons = [date.month for date in dates]
        season_results = {}
        
        for i, season in enumerate(seasons):
            if season not in season_results:
                season_results[season] = []
            
            season_results[season].append(results[i])
        
        # Check if any season has consistent results
        for season, outcomes in season_results.items():
            if len(outcomes) >= 3:  # Need at least 3 matches in this season
                # Check if >75% of results are the same
                home_wins = outcomes.count('H')
                away_wins = outcomes.count('A')
                draws = outcomes.count('D')
                
                max_result = max(home_wins, away_wins, draws)
                consistency = max_result / len(outcomes)
                
                if consistency >= 0.75:
                    # Determine which result is most common
                    if max_result == home_wins:
                        most_common = 'home team wins'
                    elif max_result == away_wins:
                        most_common = 'away team wins'
                    else:
                        most_common = 'draws'
                    
                    month_name = datetime(2000, season, 1).strftime('%B')
                    
                    result['factors'].append({
                        'name': 'Seasonal Pattern',
                        'value': f"Matches in {month_name} typically result in {most_common} ({consistency:.0%})"
                    })
                    
                    result['confidence'] += 0.15
        
        # Check for day-of-week patterns
        weekdays = [date.weekday() for date in dates]
        weekday_results = {}
        
        for i, day in enumerate(weekdays):
            if day not in weekday_results:
                weekday_results[day] = []
            
            weekday_results[day].append(results[i])
        
        # Check if any weekday has consistent results
        for day, outcomes in weekday_results.items():
            if len(outcomes) >= 3:  # Need at least 3 matches on this day
                # Check if >75% of results are the same
                home_wins = outcomes.count('H')
                away_wins = outcomes.count('A')
                draws = outcomes.count('D')
                
                max_result = max(home_wins, away_wins, draws)
                consistency = max_result / len(outcomes)
                
                if consistency >= 0.75:
                    # Determine which result is most common
                    if max_result == home_wins:
                        most_common = 'home team wins'
                    elif max_result == away_wins:
                        most_common = 'away team wins'
                    else:
                        most_common = 'draws'
                    
                    day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][day]
                    
                    result['factors'].append({
                        'name': 'Day Pattern',
                        'value': f"Matches on {day_name} typically result in {most_common} ({consistency:.0%})"
                    })
                    
                    result['confidence'] += 0.1
        
        # Check for score patterns
        scores = [(match.get('home_score', 0), match.get('away_score', 0)) for match in history]
        
        # Count frequency of each score
        score_counts = {}
        for score in scores:
            if score not in score_counts:
                score_counts[score] = 0
            score_counts[score] += 1
        
        # Find most common score
        most_common_score = max(score_counts.items(), key=lambda x: x[1]) if score_counts else None
        
        if most_common_score and most_common_score[1] >= 3:  # Score appeared at least 3 times
            result['factors'].append({
                'name': 'Score Pattern',
                'value': f"The score {most_common_score[0][0]}-{most_common_score[0][1]} appears frequently in this fixture"
            })
            
            result['confidence'] += 0.12
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def _initialize_gematria_values(self):
        """Initialize a simple gematria system for demonstration purposes."""
        # In a real system, this would be much more extensive
        return {}
    
    def _calculate_gematria(self, text):
        """Calculate a simple gematria value for text."""
        if not text:
            return 0
        
        # Simple calculation: sum of character values
        # In a full implementation, this would be more sophisticated
        return sum(ord(c.lower()) - 96 if 'a' <= c.lower() <= 'z' else 0 for c in text)
    
    def _get_sun_sign(self, month, day):
        """Determine astrological sun sign from month and day."""
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "Aries"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "Taurus"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "Gemini"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "Cancer"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "Leo"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "Virgo"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "Libra"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return "Scorpio"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "Sagittarius"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "Capricorn"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "Aquarius"
        else:
            return "Pisces"
    
    def _calculate_moon_phase(self, date):
        """Calculate approximate moon phase (0 to 1) for a given date."""
        # Simplified calculation - in a real system would use ephemeris data
        # This uses a simple approximation based on the lunar cycle
        
        # Define a known new moon date
        known_new_moon = datetime(2000, 1, 6)
        
        # Days since known new moon
        days_since = (date - known_new_moon).days
        
        # Lunar cycle is approximately 29.53 days
        lunar_cycle = 29.53
        
        # Calculate phase (0 to 1, where 0 and 1 are new moon, 0.5 is full moon)
        phase = (days_since % lunar_cycle) / lunar_cycle
        
        return phase
    
    def _initialize_tarot_associations(self):
        """Initialize tarot card associations for sports analysis."""
        # In a real implementation, this would be much more comprehensive
        return {}
    
    def _initialize_hexagrams(self):
        """Initialize I Ching hexagram data."""
        hexagrams = [
            {"number": 1, "name": "The Creative", "meaning": "Strong creative energy, leadership"},
            {"number": 2, "name": "The Receptive", "meaning": "Receptive, yielding, supportive energy"},
            {"number": 3, "name": "Difficulty at the Beginning", "meaning": "Initial obstacles but growth potential"},
            {"number": 4, "name": "Youthful Folly", "meaning": "Inexperience, learning process"},
            {"number": 5, "name": "Waiting", "meaning": "Patience needed, timing is key"},
            {"number": 6, "name": "Conflict", "meaning": "Disagreement, tension, negotiation"},
            {"number": 7, "name": "The Army", "meaning": "Discipline, coordination, strategy"},
            {"number": 8, "name": "Holding Together", "meaning": "Union, alliance, teamwork"},
            {"number": 9, "name": "Small Taming", "meaning": "Gentle restraint, gradual influence"},
            {"number": 10, "name": "Treading", "meaning": "Careful conduct, respect for process"},
            {"number": 11, "name": "Peace", "meaning": "Harmony, prosperity, good fortune"},
            {"number": 12, "name": "Standstill", "meaning": "Stagnation, decline, obstacles"},
            {"number": 13, "name": "Fellowship", "meaning": "Community, shared purpose"},
            {"number": 14, "name": "Great Possession", "meaning": "Abundance, strength, success"},
            {"number": 15, "name": "Modesty", "meaning": "Humility, balance, moderation"},
            {"number": 16, "name": "Enthusiasm", "meaning": "Joy, motivation, inspiration"},
            {"number": 17, "name": "Following", "meaning": "Adaptation, flexibility, alignment"},
            {"number": 18, "name": "Work on the Decayed", "meaning": "Repair, renewal, fixing problems"},
            {"number": 19, "name": "Approach", "meaning": "Advancement, opportunity coming"},
            {"number": 20, "name": "Contemplation", "meaning": "Observation, reflection, insight"},
            {"number": 21, "name": "Biting Through", "meaning": "Decisiveness, overcoming obstacles"},
            {"number": 22, "name": "Grace", "meaning": "Elegance, beauty, refinement"},
            {"number": 23, "name": "Splitting Apart", "meaning": "Disintegration, breakdown"},
            {"number": 24, "name": "Return", "meaning": "Turning point, new beginning"},
            {"number": 25, "name": "Innocence", "meaning": "Natural simplicity, spontaneity"},
            {"number": 26, "name": "Great Taming", "meaning": "Containment of strong forces"},
            {"number": 27, "name": "Nourishment", "meaning": "Sustenance, care, nurturing"},
            {"number": 28, "name": "Preponderance of the Great", "meaning": "Critical mass, great pressure"},
            {"number": 29, "name": "The Abysmal", "meaning": "Danger, depth, persistence"},
            {"number": 30, "name": "The Clinging", "meaning": "Attachment, clarity, illumination"},
            {"number": 31, "name": "Influence", "meaning": "Attraction, impact, stimulus"},
            {"number": 32, "name": "Duration", "meaning": "Endurance, persistence, constancy"},
            {"number": 33, "name": "Retreat", "meaning": "Strategic withdrawal, conservation"},
            {"number": 34, "name": "Great Power", "meaning": "Vigorous action, great strength"},
            {"number": 35, "name": "Progress", "meaning": "Advancement, promotional energy"},
            {"number": 36, "name": "Darkening of the Light", "meaning": "Adversity, challenge"},
            {"number": 37, "name": "The Family", "meaning": "Clan, belonging, roles"},
            {"number": 38, "name": "Opposition", "meaning": "Contrast, polarity, complementary forces"},
            {"number": 39, "name": "Obstruction", "meaning": "Difficulties, impediments"},
            {"number": 40, "name": "Deliverance", "meaning": "Release, resolution, liberation"},
            {"number": 41, "name": "Decrease", "meaning": "Reduction, loss, sacrifice"},
            {"number": 42, "name": "Increase", "meaning": "Gain, expansion, growth"},
            {"number": 43, "name": "Breakthrough", "meaning": "Resolution, decisive action"},
            {"number": 44, "name": "Coming to Meet", "meaning": "Unexpected encounter, serendipity"},
            {"number": 45, "name": "Gathering Together", "meaning": "Congregation, assembly, community"},
            {"number": 46, "name": "Pushing Upward", "meaning": "Gradual progress, advancement"},
            {"number": 47, "name": "Oppression", "meaning": "Exhaustion, being overwhelmed"},
            {"number": 48, "name": "The Well", "meaning": "Source, tradition, sustenance"},
            {"number": 49, "name": "Revolution", "meaning": "Radical change, transformation"},
            {"number": 50, "name": "The Cauldron", "meaning": "Transformation, alchemy"},
            {"number": 51, "name": "Arousing", "meaning": "Shock, excitement, awakening"},
            {"number": 52, "name": "Keeping Still", "meaning": "Stillness, rest, meditation"},
            {"number": 53, "name": "Development", "meaning": "Gradual progress, incremental change"},
            {"number": 54, "name": "The Marrying Maiden", "meaning": "Subordinate role, transition"},
            {"number": 55, "name": "Abundance", "meaning": "Fullness, peak experience"},
            {"number": 56, "name": "The Wanderer", "meaning": "Transience, impermanence, journey"},
            {"number": 57, "name": "Gentle Penetration", "meaning": "Subtle influence, persistence"},
            {"number": 58, "name": "Joyous", "meaning": "Delight, satisfaction, dialog"},
            {"number": 59, "name": "Dispersion", "meaning": "Dissolution, scattering"},
            {"number": 60, "name": "Limitation", "meaning": "Restriction, defining boundaries"},
            {"number": 61, "name": "Inner Truth", "meaning": "Sincerity, centered awareness"},
            {"number": 62, "name": "Small Exceeding", "meaning": "Attention to detail, minor superiority"},
            {"number": 63, "name": "After Completion", "meaning": "Transition after success"},
            {"number": 64, "name": "Before Completion", "meaning": "Approaching the end, final stages"}
        ]
        return hexagrams
