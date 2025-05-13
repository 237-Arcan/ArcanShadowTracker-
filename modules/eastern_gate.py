"""
EasternGate - Specialized module for Asian football competitions in ArcanShadow.
Provides cultural, spiritual, and regional adaptations for Asian competitions.
"""

import numpy as np
import math
from datetime import datetime, timedelta
import random
import os
from utils.api_integrations import APIIntegrations

class EasternGate:
    """
    EasternGate module - Specialized analysis for Asian competitions.
    Incorporates regional cultural, spiritual, and stylistic adaptations.
    """
    
    def __init__(self):
        """Initialize the EasternGate module with necessary components."""
        # Define supported competitions
        self.supported_leagues = [
            'J-League', 
            'K-League', 
            'Chinese Super League',
            'AFC Champions League',
            'J1 League', # Alternative name
            'K League 1', # Alternative name
            'CSL',        # Alternative name
            'J2 League',
            'K League 2'
        ]
        
        # Initialize API integrations
        self.api = APIIntegrations()
        
        # Initialize specialized sub-modules
        self.submodules = {
            'ElementalBalance': self.elemental_balance,
            'LunarPhaseTracker': self.lunar_phase_tracker,
            'LocalRitualImpact': self.local_ritual_impact,
            'CityEnergyField': self.city_energy_field,
            'RegionalDeityInfluence': self.regional_deity_influence
        }
        
        # Initialize element associations
        self._initialize_elements()
        
        # Cache for results to avoid redundant calculations
        self.cache = {}
    
    def analyze_match(self, match_data):
        """
        Main method to analyze an Asian match using specialized parameters.
        
        Args:
            match_data (dict): Match information including teams, league, etc.
            
        Returns:
            dict: Results of the Asia-specific analysis
        """
        # Clear cache for new match
        self.cache = {}
        
        # Check if the league is supported
        league = match_data.get('league', '')
        
        if not any(supported in league for supported in self.supported_leagues):
            return {
                'active': False,
                'message': 'EasternGate not applicable for this competition',
                'confidence': 0,
                'factors': []
            }
        
        results = {
            'active': True,
            'confidence': 0,
            'factors': []
        }
        
        # Run each submodule and collect results
        submodule_results = {}
        for name, module_func in self.submodules.items():
            try:
                submodule_results[name] = module_func(match_data)
            except Exception as e:
                print(f"Error in EasternGate {name}: {str(e)}")
                submodule_results[name] = {'confidence': 0.5, 'factors': []}
        
        # Calculate weighted confidence
        module_weights = {
            'ElementalBalance': 0.25,
            'LunarPhaseTracker': 0.20,
            'LocalRitualImpact': 0.15,
            'CityEnergyField': 0.20,
            'RegionalDeityInfluence': 0.20
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
            results['confidence'] = 0.5
        
        # Add region-specific insight
        results['region'] = self._determine_region(match_data)
        
        return results
    
    def elemental_balance(self, match_data):
        """
        ElementalBalance: Analyzes the five elements (Wu Xing) balance in teams.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Elemental balance analysis
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # Get team names
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        if not home_team or not away_team:
            result['factors'].append({
                'name': 'Insufficient Data',
                'value': 'Team names required for elemental analysis'
            })
            return result
        
        # Determine team elements
        home_elements = self._calculate_team_elements(home_team)
        away_elements = self._calculate_team_elements(away_team)
        
        # Calculate dominant elements
        home_dominant = max(home_elements.items(), key=lambda x: x[1])
        away_dominant = max(away_elements.items(), key=lambda x: x[1])
        
        # Calculate elemental advantage
        advantage = self._calculate_elemental_advantage(home_dominant[0], away_dominant[0])
        
        # Add the dominant elements to factors
        result['factors'].append({
            'name': 'Dominant Elements',
            'value': f"{home_team}: {home_dominant[0].capitalize()} ({home_dominant[1]:.0f}%), {away_team}: {away_dominant[0].capitalize()} ({away_dominant[1]:.0f}%)"
        })
        
        # Add the advantage factor
        if advantage['team'] == 'home':
            result['factors'].append({
                'name': 'Elemental Advantage',
                'value': f"{home_team} has {advantage['magnitude']:.0f}% {advantage['type']} advantage"
            })
            # Adjust confidence based on advantage magnitude
            result['confidence'] += (advantage['magnitude'] / 100) * 0.3
        elif advantage['team'] == 'away':
            result['factors'].append({
                'name': 'Elemental Advantage',
                'value': f"{away_team} has {advantage['magnitude']:.0f}% {advantage['type']} advantage"
            })
            # Adjust confidence based on advantage magnitude
            result['confidence'] -= (advantage['magnitude'] / 100) * 0.3
        else:
            result['factors'].append({
                'name': 'Elemental Balance',
                'value': 'Teams are in elemental equilibrium'
            })
        
        # Check for elemental harmony within teams
        home_harmony = self._calculate_element_harmony(home_elements)
        away_harmony = self._calculate_element_harmony(away_elements)
        
        if home_harmony > away_harmony:
            harmony_diff = home_harmony - away_harmony
            result['factors'].append({
                'name': 'Internal Harmony',
                'value': f"{home_team} has {harmony_diff:.0f}% better elemental harmony"
            })
            result['confidence'] += harmony_diff * 0.005
        elif away_harmony > home_harmony:
            harmony_diff = away_harmony - home_harmony
            result['factors'].append({
                'name': 'Internal Harmony',
                'value': f"{away_team} has {harmony_diff:.0f}% better elemental harmony"
            })
            result['confidence'] -= harmony_diff * 0.005
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def lunar_phase_tracker(self, match_data):
        """
        LunarPhaseTracker: Analyzes the lunar calendar impact on team performance.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Lunar influence analysis
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # Get match date
        match_date = match_data.get('date')
        if not match_date:
            match_date = datetime.now()
        elif isinstance(match_date, str):
            try:
                match_date = datetime.fromisoformat(match_date.replace('Z', '+00:00'))
            except:
                match_date = datetime.now()
        
        # Calculate lunar phase
        lunar_phase = self._calculate_lunar_phase(match_date)
        phase_name = self._get_phase_name(lunar_phase)
        
        # Add lunar phase to factors
        result['factors'].append({
            'name': 'Lunar Phase',
            'value': f"{phase_name} ({lunar_phase:.1f}%)"
        })
        
        # Get team names
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # Calculate lunar influence on teams
        home_influence = self._calculate_lunar_team_influence(home_team, lunar_phase)
        away_influence = self._calculate_lunar_team_influence(away_team, lunar_phase)
        
        # Add lunar influences to factors
        result['factors'].append({
            'name': 'Lunar Influence',
            'value': f"{home_team}: {home_influence['description']}, {away_team}: {away_influence['description']}"
        })
        
        # Compare influences
        if home_influence['magnitude'] > away_influence['magnitude']:
            diff = home_influence['magnitude'] - away_influence['magnitude']
            result['factors'].append({
                'name': 'Lunar Advantage',
                'value': f"{home_team} has {diff:.0f}% stronger lunar resonance"
            })
            result['confidence'] += diff * 0.005
        elif away_influence['magnitude'] > home_influence['magnitude']:
            diff = away_influence['magnitude'] - home_influence['magnitude']
            result['factors'].append({
                'name': 'Lunar Advantage',
                'value': f"{away_team} has {diff:.0f}% stronger lunar resonance"
            })
            result['confidence'] -= diff * 0.005
        
        # Check for special lunar dates
        if self._is_special_lunar_date(match_date):
            special_date = self._get_special_lunar_date(match_date)
            result['factors'].append({
                'name': 'Special Lunar Date',
                'value': f"Match occurs during {special_date['name']}: {special_date['description']}"
            })
            
            # Adjust confidence based on team affinity with the special date
            home_affinity = self._calculate_special_date_affinity(home_team, special_date)
            away_affinity = self._calculate_special_date_affinity(away_team, special_date)
            
            if home_affinity > away_affinity:
                result['confidence'] += (home_affinity - away_affinity) * 0.1
            else:
                result['confidence'] -= (away_affinity - home_affinity) * 0.1
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def local_ritual_impact(self, match_data):
        """
        LocalRitualImpact: Analyzes the influence of local cultural rituals on the match.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Local ritual analysis
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # Get venue and country
        venue = match_data.get('venue', '')
        country = self._determine_country(match_data)
        
        if not venue or not country:
            result['factors'].append({
                'name': 'Insufficient Data',
                'value': 'Venue and country information required for ritual analysis'
            })
            return result
        
        # Check for local rituals
        local_rituals = self._get_local_rituals(country, venue)
        
        if not local_rituals:
            result['factors'].append({
                'name': 'No Significant Rituals',
                'value': 'No major local rituals affecting the match'
            })
            return result
        
        # Analyze the impact of each ritual
        total_home_impact = 0
        total_away_impact = 0
        
        for ritual in local_rituals:
            home_impact = ritual['home_impact']
            away_impact = ritual['away_impact']
            
            result['factors'].append({
                'name': f"Local Ritual: {ritual['name']}",
                'value': ritual['description']
            })
            
            # Add specific impact descriptions
            if home_impact > 0:
                result['factors'].append({
                    'name': 'Home Team Ritual Benefit',
                    'value': f"+{home_impact:.0f}% {ritual['benefit_type']}"
                })
            
            if away_impact > 0:
                result['factors'].append({
                    'name': 'Away Team Ritual Benefit',
                    'value': f"+{away_impact:.0f}% {ritual['benefit_type']}"
                })
            
            total_home_impact += home_impact
            total_away_impact += away_impact
        
        # Adjust confidence based on ritual impacts
        net_impact = total_home_impact - total_away_impact
        result['confidence'] += (net_impact / 100) * 0.2
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def city_energy_field(self, match_data):
        """
        CityEnergyField: Analyzes the energy fields of the venue city.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: City energy analysis
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # Get venue
        venue = match_data.get('venue', '')
        
        if not venue:
            result['factors'].append({
                'name': 'Insufficient Data',
                'value': 'Venue information required for city energy analysis'
            })
            return result
        
        # Calculate city energy profile
        energy_profile = self._calculate_city_energy(venue)
        
        # Add main energy type to factors
        result['factors'].append({
            'name': 'City Energy Profile',
            'value': f"{venue} dominant energy: {energy_profile['dominant_type']} ({energy_profile['dominant_strength']:.0f}%)"
        })
        
        # Get team names
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # Calculate energy compatibility for each team
        home_compatibility = self._calculate_energy_compatibility(home_team, energy_profile)
        away_compatibility = self._calculate_energy_compatibility(away_team, energy_profile)
        
        # Add compatibility to factors
        result['factors'].append({
            'name': 'Energy Compatibility',
            'value': f"{home_team}: {home_compatibility:.0f}%, {away_team}: {away_compatibility:.0f}%"
        })
        
        # Adjust confidence based on compatibility difference
        compatibility_diff = home_compatibility - away_compatibility
        result['confidence'] += (compatibility_diff / 100) * 0.25
        
        # Check for energy anomalies
        if energy_profile.get('anomalies'):
            for anomaly in energy_profile['anomalies']:
                result['factors'].append({
                    'name': 'Energy Anomaly',
                    'value': f"{anomaly['description']} ({anomaly['impact']})"
                })
                
                # Adjust confidence based on anomaly
                if anomaly['team'] == 'home':
                    result['confidence'] += anomaly['magnitude'] * 0.05
                elif anomaly['team'] == 'away':
                    result['confidence'] -= anomaly['magnitude'] * 0.05
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def regional_deity_influence(self, match_data):
        """
        RegionalDeityInfluence: Analyzes the influence of regional deities and belief systems.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            dict: Regional deity analysis
        """
        result = {
            'confidence': 0.5,
            'factors': []
        }
        
        # Get country and region
        country = self._determine_country(match_data)
        region = match_data.get('region', self._determine_region(match_data))
        
        if not country:
            result['factors'].append({
                'name': 'Insufficient Data',
                'value': 'Country information required for deity analysis'
            })
            return result
        
        # Get regional deities
        regional_deities = self._get_regional_deities(country, region)
        
        if not regional_deities:
            result['factors'].append({
                'name': 'No Significant Influences',
                'value': 'No major deity influences affecting the match'
            })
            return result
        
        # Get team names
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # Calculate total influence
        home_total_influence = 0
        away_total_influence = 0
        
        for deity in regional_deities:
            # Calculate influence on each team
            home_influence = self._calculate_deity_influence(deity, home_team)
            away_influence = self._calculate_deity_influence(deity, away_team)
            
            # Add significant influences to factors
            if home_influence > 20 or away_influence > 20:
                result['factors'].append({
                    'name': f"Deity Influence: {deity['name']}",
                    'value': f"{deity['domain']}: {home_team} ({home_influence:.0f}%), {away_team} ({away_influence:.0f}%)"
                })
            
            home_total_influence += home_influence
            away_total_influence += away_influence
        
        # Add overall influence to factors
        if home_total_influence > 0 or away_total_influence > 0:
            result['factors'].append({
                'name': 'Total Deity Influence',
                'value': f"{home_team}: {home_total_influence:.0f}%, {away_team}: {away_total_influence:.0f}%"
            })
        
        # Adjust confidence based on influence difference
        influence_diff = home_total_influence - away_total_influence
        result['confidence'] += (influence_diff / 100) * 0.2
        
        # Normalize confidence
        result['confidence'] = max(0, min(1, result['confidence']))
        
        return result
    
    def _initialize_elements(self):
        """Initialize the five elements system and associations."""
        # The five elements (Wu Xing)
        self.elements = ['wood', 'fire', 'earth', 'metal', 'water']
        
        # Element relationships
        self.element_relationships = {
            'wood': {'generates': 'fire', 'controls': 'earth', 'weakened_by': 'metal', 'countered_by': 'water'},
            'fire': {'generates': 'earth', 'controls': 'metal', 'weakened_by': 'water', 'countered_by': 'wood'},
            'earth': {'generates': 'metal', 'controls': 'water', 'weakened_by': 'wood', 'countered_by': 'fire'},
            'metal': {'generates': 'water', 'controls': 'wood', 'weakened_by': 'fire', 'countered_by': 'earth'},
            'water': {'generates': 'wood', 'controls': 'fire', 'weakened_by': 'earth', 'countered_by': 'metal'}
        }
        
        # Team name character associations
        self.character_element_map = {
            # Japanese characters
            '森': 'wood', '林': 'wood', '木': 'wood', '緑': 'wood',
            '火': 'fire', '炎': 'fire', '赤': 'fire', '熱': 'fire',
            '土': 'earth', '山': 'earth', '地': 'earth', '黄': 'earth',
            '金': 'metal', '銀': 'metal', '鉄': 'metal', '白': 'metal',
            '水': 'water', '海': 'water', '川': 'water', '青': 'water',
            
            # Korean characters
            '나무': 'wood', '숲': 'wood', '녹색': 'wood',
            '불': 'fire', '화재': 'fire', '빨간색': 'fire',
            '흙': 'earth', '산': 'earth', '황색': 'earth',
            '금속': 'metal', '쇠': 'metal', '하얀색': 'metal',
            '물': 'water', '바다': 'water', '파란색': 'water',
            
            # Chinese characters
            '树': 'wood', '森': 'wood', '林': 'wood', '绿': 'wood',
            '火': 'fire', '焰': 'fire', '红': 'fire', '热': 'fire',
            '土': 'earth', '山': 'earth', '地': 'earth', '黄': 'earth',
            '金': 'metal', '银': 'metal', '铁': 'metal', '白': 'metal',
            '水': 'water', '海': 'water', '河': 'water', '蓝': 'water'
        }
        
        # Team color associations
        self.color_element_map = {
            'green': 'wood',
            'blue': 'water',
            'black': 'water',
            'red': 'fire',
            'orange': 'fire',
            'yellow': 'earth',
            'brown': 'earth',
            'white': 'metal',
            'silver': 'metal',
            'gold': 'metal'
        }
        
        # Team mascot associations
        self.mascot_element_map = {
            'dragon': {'fire': 0.6, 'water': 0.4},
            'tiger': {'wood': 0.7, 'fire': 0.3},
            'phoenix': {'fire': 0.8, 'metal': 0.2},
            'turtle': {'water': 0.8, 'earth': 0.2},
            'lion': {'fire': 0.6, 'metal': 0.4},
            'bear': {'earth': 0.7, 'wood': 0.3},
            'eagle': {'metal': 0.7, 'wood': 0.3},
            'fish': {'water': 1.0},
            'wolf': {'metal': 0.5, 'water': 0.5},
            'horse': {'fire': 0.6, 'earth': 0.4},
            'snake': {'fire': 0.4, 'earth': 0.6},
            'crane': {'metal': 0.6, 'water': 0.4},
            'dolphin': {'water': 0.9, 'wood': 0.1},
            'ox': {'earth': 0.8, 'metal': 0.2},
            'rabbit': {'wood': 0.9, 'earth': 0.1}
        }
    
    def _calculate_team_elements(self, team_name):
        """Calculate the elemental composition of a team based on its name."""
        result = {element: 0 for element in self.elements}
        
        if not team_name:
            return result
        
        # Default elemental distribution based on team name length
        # This ensures we always have some values even without specific associations
        seed = hash(team_name) % 100
        random.seed(seed)
        
        for element in self.elements:
            result[element] = random.uniform(10, 30)
        
        # Normalize to make sure total is 100%
        total = sum(result.values())
        for element in result:
            result[element] = (result[element] / total) * 100
        
        # Check for specific character associations
        for char in team_name:
            if char in self.character_element_map:
                element = self.character_element_map[char]
                result[element] += 15  # Significant boost for character match
        
        # Check for color associations (simplified - would use team color data in a real implementation)
        for color, element in self.color_element_map.items():
            if color.lower() in team_name.lower():
                result[element] += 10  # Moderate boost for color match
        
        # Check for mascot associations (simplified)
        for mascot, elements in self.mascot_element_map.items():
            if mascot.lower() in team_name.lower():
                for element, value in elements.items():
                    result[element] += 20 * value  # Strong boost for mascot match
        
        # Normalize to 100%
        total = sum(result.values())
        for element in result:
            result[element] = (result[element] / total) * 100
        
        return result
    
    def _calculate_elemental_advantage(self, home_element, away_element):
        """Calculate the elemental advantage between two teams."""
        result = {
            'team': 'neutral',
            'type': 'neutral',
            'magnitude': 0
        }
        
        if home_element == away_element:
            return result
        
        # Check if home generates/controls away
        if self.element_relationships[home_element]['generates'] == away_element:
            result['team'] = 'home'
            result['type'] = 'generative'
            result['magnitude'] = 25  # Moderate advantage
        elif self.element_relationships[home_element]['controls'] == away_element:
            result['team'] = 'home'
            result['type'] = 'controlling'
            result['magnitude'] = 40  # Strong advantage
            
        # Check if away generates/controls home
        elif self.element_relationships[away_element]['generates'] == home_element:
            result['team'] = 'away'
            result['type'] = 'generative'
            result['magnitude'] = 25  # Moderate advantage
        elif self.element_relationships[away_element]['controls'] == home_element:
            result['team'] = 'away'
            result['type'] = 'controlling'
            result['magnitude'] = 40  # Strong advantage
        
        return result
    
    def _calculate_element_harmony(self, elements):
        """Calculate the internal harmony of a team's elements."""
        # A well-balanced team should have representation across multiple elements
        # Too much focus on one element can be a weakness
        
        # Calculate entropy as a measure of balance
        total = sum(elements.values())
        entropy = 0
        
        for value in elements.values():
            if value > 0:
                p = value / total
                entropy -= p * math.log2(p)
        
        # Normalize to 0-100 scale
        # Max entropy for 5 elements would be log2(5) = 2.32
        harmony = (entropy / 2.32) * 100
        
        return harmony
    
    def _calculate_lunar_phase(self, date):
        """Calculate the lunar phase (0-100, where 0=new moon, 50=full moon, 100=new moon again)."""
        # This is a simplified calculation
        # In a real implementation, this would use proper lunar calendar calculations
        
        # Lunar cycle is approximately 29.53059 days
        lunar_cycle = 29.53059
        
        # Base date (known new moon)
        base_date = datetime(2025, 1, 1)  # Example reference date
        
        # Calculate days since base date
        days_since = (date - base_date).total_seconds() / (24 * 3600)
        
        # Calculate position in lunar cycle
        position = (days_since % lunar_cycle) / lunar_cycle
        
        # Convert to 0-100 scale
        phase = position * 100
        
        return phase
    
    def _get_phase_name(self, phase):
        """Get the name of the lunar phase."""
        if phase < 5 or phase > 95:
            return "New Moon"
        elif 5 <= phase < 20:
            return "Waxing Crescent"
        elif 20 <= phase < 30:
            return "First Quarter"
        elif 30 <= phase < 45:
            return "Waxing Gibbous"
        elif 45 <= phase < 55:
            return "Full Moon"
        elif 55 <= phase < 70:
            return "Waning Gibbous"
        elif 70 <= phase < 80:
            return "Last Quarter"
        else:  # 80 <= phase < 95
            return "Waning Crescent"
    
    def _calculate_lunar_team_influence(self, team_name, lunar_phase):
        """Calculate the lunar influence on a team."""
        if not team_name:
            return {
                'description': 'Neutral',
                'magnitude': 0
            }
        
        # Generate a consistent team lunar affinity based on the team name
        seed = hash(team_name) % (2**32 - 1)
        np.random.seed(seed)
        
        # Generate team's lunar affinity profile
        # This determines which lunar phases strengthen or weaken the team
        affinity = {}
        
        # Generate peak affinity phase (where team is strongest)
        peak_phase = np.random.randint(0, 100)
        
        # Calculate distance from current phase to peak phase (circular)
        distance = min(abs(lunar_phase - peak_phase), 100 - abs(lunar_phase - peak_phase))
        
        # Normalize distance to 0-1 scale (0 = at peak, 1 = opposite of peak)
        normalized_distance = distance / 50
        
        # Calculate influence (100 at peak, diminishing with distance)
        influence = 100 * (1 - normalized_distance)
        
        # Determine description based on influence
        if influence > 80:
            description = "Strong Positive"
        elif influence > 60:
            description = "Positive"
        elif influence > 40:
            description = "Slightly Positive"
        elif influence > 20:
            description = "Neutral"
        else:
            description = "Negative"
        
        return {
            'description': description,
            'magnitude': influence
        }
    
    def _is_special_lunar_date(self, date):
        """Check if the date is a special lunar calendar date."""
        # In a real implementation, this would check against a lunar calendar
        # For now, use a simplified approach with pre-defined dates
        
        special_dates = [
            datetime(2025, 1, 22),  # Chinese New Year
            datetime(2025, 2, 21),  # Lantern Festival
            datetime(2025, 4, 5),   # Qingming Festival
            datetime(2025, 6, 10),  # Dragon Boat Festival
            datetime(2025, 9, 18),  # Mid-Autumn Festival
        ]
        
        # Check if date is close to a special date (within 3 days)
        for special_date in special_dates:
            if abs((date - special_date).days) <= 3:
                return True
        
        return False
    
    def _get_special_lunar_date(self, date):
        """Get information about a special lunar date."""
        # Define special dates
        special_dates = [
            {
                'date': datetime(2025, 1, 22),
                'name': 'Chinese New Year',
                'description': 'Beginning of the lunar year, strong renewal energy'
            },
            {
                'date': datetime(2025, 2, 21),
                'name': 'Lantern Festival',
                'description': 'Marks the end of New Year, illuminating energy'
            },
            {
                'date': datetime(2025, 4, 5),
                'name': 'Qingming Festival',
                'description': 'Clear and bright energy, connection to ancestors'
            },
            {
                'date': datetime(2025, 6, 10),
                'name': 'Dragon Boat Festival',
                'description': 'Powerful protective energy, warding off misfortune'
            },
            {
                'date': datetime(2025, 9, 18),
                'name': 'Mid-Autumn Festival',
                'description': 'Harvest energy, fullness and completion'
            }
        ]
        
        # Find closest special date
        closest_date = None
        closest_diff = float('inf')
        
        for special_date in special_dates:
            diff = abs((date - special_date['date']).days)
            if diff < closest_diff and diff <= 3:
                closest_diff = diff
                closest_date = special_date
        
        return closest_date or {
            'name': 'No Special Date',
            'description': 'No significant lunar calendar event'
        }
    
    def _calculate_special_date_affinity(self, team_name, special_date):
        """Calculate a team's affinity with a special lunar date."""
        if not team_name or 'name' not in special_date:
            return 0
        
        # Generate a consistent team affinity based on the team name and special date
        seed = hash(team_name + special_date['name']) % (2**32 - 1)
        np.random.seed(seed)
        
        # Generate affinity score (0-100)
        affinity = np.random.uniform(20, 80)
        
        # Adjust based on date name presence in team name or vice versa
        if any(word.lower() in team_name.lower() for word in special_date['name'].lower().split()):
            affinity += 15
        
        return min(affinity, 100)
    
    def _get_local_rituals(self, country, venue):
        """Get local rituals for a specific country and venue."""
        # Define rituals by country
        rituals_by_country = {
            'Japan': [
                {
                    'name': 'Shinto Blessing',
                    'description': 'Pre-match shrine visit by home team',
                    'home_impact': 15,
                    'away_impact': 0,
                    'benefit_type': 'mental clarity'
                },
                {
                    'name': 'Taiko Drums',
                    'description': 'Traditional drum performance before match',
                    'home_impact': 10,
                    'away_impact': -5,
                    'benefit_type': 'energy boost'
                }
            ],
            'South Korea': [
                {
                    'name': 'Taegeuk Ceremony',
                    'description': 'Pre-match harmony ritual',
                    'home_impact': 12,
                    'away_impact': 0,
                    'benefit_type': 'team unity'
                },
                {
                    'name': 'Ssireum Tribute',
                    'description': 'Traditional wrestling homage',
                    'home_impact': 8,
                    'away_impact': 0,
                    'benefit_type': 'physical strength'
                }
            ],
            'China': [
                {
                    'name': 'Dragon Dance',
                    'description': 'Traditional pre-match performance',
                    'home_impact': 12,
                    'away_impact': -5,
                    'benefit_type': 'auspicious energy'
                },
                {
                    'name': 'Feng Shui Alignment',
                    'description': 'Stadium energy alignment',
                    'home_impact': 15,
                    'away_impact': 0,
                    'benefit_type': 'environmental harmony'
                }
            ]
        }
        
        # Special venue-specific rituals
        venue_rituals = {
            'Saitama Stadium': [
                {
                    'name': 'Musashi Blessing',
                    'description': 'Special blessing invoking the spirit of Musashi',
                    'home_impact': 18,
                    'away_impact': 0,
                    'benefit_type': 'strategic insight'
                }
            ],
            'Seoul World Cup Stadium': [
                {
                    'name': 'Red Devil Energy',
                    'description': 'Fan unity ritual from 2002 World Cup',
                    'home_impact': 20,
                    'away_impact': -10,
                    'benefit_type': 'fan energy transfer'
                }
            ],
            'Shanghai Stadium': [
                {
                    'name': 'Pearl Tower Alignment',
                    'description': 'Energy alignment with the Oriental Pearl Tower',
                    'home_impact': 15,
                    'away_impact': 0,
                    'benefit_type': 'city energy connection'
                }
            ]
        }
        
        # Combine country and venue rituals
        rituals = []
        
        if country in rituals_by_country:
            rituals.extend(rituals_by_country[country])
        
        if venue in venue_rituals:
            rituals.extend(venue_rituals[venue])
        
        return rituals
    
    def _calculate_city_energy(self, venue):
        """Calculate the energy profile of a venue city."""
        if not venue:
            return {
                'dominant_type': 'neutral',
                'dominant_strength': 0
            }
        
        # Generate a consistent energy profile based on the venue name
        seed = hash(venue) % (2**32 - 1)
        np.random.seed(seed)
        
        # Generate energy distribution across types
        energy_types = ['flowing', 'stable', 'ascending', 'descending', 'cyclical']
        energy_distribution = {}
        
        for energy_type in energy_types:
            energy_distribution[energy_type] = np.random.uniform(10, 50)
        
        # Normalize to 100%
        total = sum(energy_distribution.values())
        for energy_type in energy_distribution:
            energy_distribution[energy_type] = (energy_distribution[energy_type] / total) * 100
        
        # Find dominant energy type
        dominant_type = max(energy_distribution.items(), key=lambda x: x[1])
        
        # Check for energy anomalies
        anomalies = []
        if np.random.random() < 0.3:  # 30% chance of anomaly
            anomaly_types = [
                {
                    'description': 'Energy Vortex',
                    'impact': 'Creates unpredictability',
                    'team': 'away' if np.random.random() < 0.7 else 'home',  # Usually benefits away team
                    'magnitude': np.random.uniform(0.1, 0.3)
                },
                {
                    'description': 'Harmonic Convergence',
                    'impact': 'Amplifies team unity',
                    'team': 'home' if np.random.random() < 0.8 else 'away',  # Usually benefits home team
                    'magnitude': np.random.uniform(0.1, 0.3)
                },
                {
                    'description': 'Elemental Imbalance',
                    'impact': 'Disrupts flow',
                    'team': 'away' if np.random.random() < 0.6 else 'home',  # Slightly more likely to affect away team
                    'magnitude': np.random.uniform(0.1, 0.3)
                }
            ]
            
            anomalies.append(np.random.choice(anomaly_types))
        
        return {
            'dominant_type': dominant_type[0],
            'dominant_strength': dominant_type[1],
            'energy_distribution': energy_distribution,
            'anomalies': anomalies
        }
    
    def _calculate_energy_compatibility(self, team_name, energy_profile):
        """Calculate compatibility between a team and city energy profile."""
        if not team_name or 'dominant_type' not in energy_profile:
            return 50  # Neutral compatibility
        
        # Generate a consistent compatibility based on team name and energy type
        seed = hash(team_name + energy_profile['dominant_type']) % (2**32 - 1)
        np.random.seed(seed)
        
        # Base compatibility
        compatibility = np.random.uniform(40, 60)
        
        # Adjust based on energy type matching team characteristics
        team_elements = self._calculate_team_elements(team_name)
        
        # Different energy types favor different elements
        energy_element_affinities = {
            'flowing': {'water': 0.8, 'wood': 0.6, 'fire': 0.3, 'earth': 0.1, 'metal': 0.2},
            'stable': {'earth': 0.8, 'metal': 0.6, 'water': 0.3, 'wood': 0.2, 'fire': 0.1},
            'ascending': {'fire': 0.8, 'wood': 0.6, 'earth': 0.4, 'metal': 0.2, 'water': 0.1},
            'descending': {'metal': 0.8, 'water': 0.6, 'earth': 0.4, 'fire': 0.1, 'wood': 0.2},
            'cyclical': {'wood': 0.5, 'fire': 0.5, 'earth': 0.5, 'metal': 0.5, 'water': 0.5}
        }
        
        # Calculate element-based compatibility
        if energy_profile['dominant_type'] in energy_element_affinities:
            affinities = energy_element_affinities[energy_profile['dominant_type']]
            
            for element, team_value in team_elements.items():
                affinity = affinities.get(element, 0.3)
                compatibility += (team_value / 100) * affinity * 20
        
        # Normalize to 0-100
        compatibility = max(0, min(100, compatibility))
        
        return compatibility
    
    def _get_regional_deities(self, country, region=None):
        """Get regional deities and belief systems for a country/region."""
        # Define deities by country/region
        deities_by_country = {
            'Japan': [
                {
                    'name': 'Amaterasu',
                    'domain': 'Sun and Universe',
                    'influence': 'Illumination and clarity',
                    'regions': ['All']
                },
                {
                    'name': 'Hachiman',
                    'domain': 'War and Warriors',
                    'influence': 'Strategy and victory',
                    'regions': ['Kanto', 'All']
                },
                {
                    'name': 'Inari',
                    'domain': 'Prosperity and Rice',
                    'influence': 'Abundance and success',
                    'regions': ['Kansai', 'All']
                }
            ],
            'South Korea': [
                {
                    'name': 'Sanshin',
                    'domain': 'Mountain Spirit',
                    'influence': 'Strength and endurance',
                    'regions': ['All']
                },
                {
                    'name': 'Haemosu',
                    'domain': 'Sun God',
                    'influence': 'Leadership and vitality',
                    'regions': ['Seoul', 'All']
                }
            ],
            'China': [
                {
                    'name': 'Guandi',
                    'domain': 'War and Justice',
                    'influence': 'Loyalty and righteousness',
                    'regions': ['All']
                },
                {
                    'name': 'Caishen',
                    'domain': 'Wealth and Fortune',
                    'influence': 'Prosperity and opportunity',
                    'regions': ['Shanghai', 'Guangzhou', 'All']
                },
                {
                    'name': 'Mazu',
                    'domain': 'Sea Goddess',
                    'influence': 'Protection and safe journey',
                    'regions': ['Coastal', 'All']
                }
            ]
        }
        
        # Filter deities by country and region
        if country not in deities_by_country:
            return []
        
        result = []
        
        for deity in deities_by_country[country]:
            if region in deity['regions'] or 'All' in deity['regions']:
                result.append(deity)
        
        return result
    
    def _calculate_deity_influence(self, deity, team_name):
        """Calculate the influence of a deity on a team."""
        if not team_name:
            return 0
        
        # Generate a consistent influence based on team name and deity
        seed = hash(team_name + deity['name']) % (2**32 - 1)
        np.random.seed(seed)
        
        # Base influence value
        influence = np.random.uniform(10, 30)
        
        # Check for team name associations with the deity's domain
        domain_keywords = deity['domain'].lower().split()
        for keyword in domain_keywords:
            if keyword in team_name.lower() and len(keyword) > 3:  # Avoid matching short common words
                influence += 25
                break
        
        # Check for influence associations
        influence_keywords = deity['influence'].lower().split()
        for keyword in influence_keywords:
            if keyword in team_name.lower() and len(keyword) > 3:
                influence += 15
                break
        
        # Normalize to 0-100
        influence = max(0, min(100, influence))
        
        return influence
    
    def _determine_country(self, match_data):
        """Determine the country based on match data."""
        # Try to get country from venue
        country = match_data.get('country', '')
        if country:
            return country
        
        # Try to infer from league
        league = match_data.get('league', '')
        
        if 'J-League' in league or 'J1' in league or 'J2' in league:
            return 'Japan'
        elif 'K-League' in league or 'K League' in league:
            return 'South Korea'
        elif 'Chinese Super League' in league or 'CSL' in league:
            return 'China'
        
        # Default to Japan if can't determine
        return 'Japan'
    
    def _determine_region(self, match_data):
        """Determine the region within a country based on match data."""
        venue = match_data.get('venue', '')
        country = self._determine_country(match_data)
        
        # Japanese regions
        japan_regions = {
            'Tokyo': 'Kanto',
            'Yokohama': 'Kanto',
            'Saitama': 'Kanto',
            'Osaka': 'Kansai',
            'Kobe': 'Kansai',
            'Kyoto': 'Kansai',
            'Sapporo': 'Hokkaido',
            'Fukuoka': 'Kyushu'
        }
        
        # Korean regions
        korea_regions = {
            'Seoul': 'Seoul',
            'Incheon': 'Seoul',
            'Suwon': 'Gyeonggi',
            'Jeonju': 'Jeollabuk',
            'Busan': 'Busan',
            'Daegu': 'Daegu'
        }
        
        # Chinese regions
        china_regions = {
            'Shanghai': 'Shanghai',
            'Beijing': 'Beijing',
            'Guangzhou': 'Guangdong',
            'Shenzhen': 'Guangdong',
            'Tianjin': 'Tianjin',
            'Wuhan': 'Hubei'
        }
        
        # Check for venue matches
        if country == 'Japan':
            for city, region in japan_regions.items():
                if city in venue:
                    return region
        elif country == 'South Korea':
            for city, region in korea_regions.items():
                if city in venue:
                    return region
        elif country == 'China':
            for city, region in china_regions.items():
                if city in venue:
                    return region
        
        # Check for coastal regions in China
        if country == 'China' and any(city in venue for city in ['Shanghai', 'Guangzhou', 'Qingdao', 'Dalian']):
            return 'Coastal'
        
        # Default regions by country
        default_regions = {
            'Japan': 'Kanto',
            'South Korea': 'Seoul',
            'China': 'Beijing'
        }
        
        return default_regions.get(country, 'Unknown')