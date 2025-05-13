"""
Sports API module for ArcanShadow
Handles retrieval of real sports data from external APIs
"""

import requests
import json
from datetime import datetime, timedelta
import os
import random  # As fallback
import time

class SportsAPI:
    """
    Handles interaction with external sports data APIs.
    Currently uses football-data.org API for football matches.
    """
    
    def __init__(self):
        """Initialize the API connections"""
        # Check if API key is available in environment variables
        self.football_api_key = os.environ.get('FOOTBALL_API_KEY', '')
        self.api_ready = bool(self.football_api_key)
        
        # Base URLs for APIs
        self.football_base_url = "https://api.football-data.org/v4"
        
        # Cache to reduce API calls
        self.cache = {}
        self.cache_expiry = {}
        self.cache_duration = 60 * 30  # 30 minutes
        
        # League mapping
        self.league_mapping = {
            'Premier League': 'PL',
            'La Liga': 'PD',
            'Bundesliga': 'BL1',
            'Serie A': 'SA',
            'Ligue 1': 'FL1',
            'Champions League': 'CL',
            'MLS': 'MLS',
            'Campeonato Brasileiro Série A': 'BSA'  # Brazilian league added
        }
        
        # Sport mapping
        self.sport_mapping = {
            'Football': 'SOCCER',
            'Basketball': 'BASKETBALL',
            'Tennis': 'TENNIS',
            'Baseball': 'BASEBALL',
            'Hockey': 'ICE_HOCKEY'
        }
        
    def get_matches(self, sport, league, date):
        """
        Get matches for a specific sport, league and date
        
        Args:
            sport (str): Sport name
            league (str): League name
            date (datetime.date): Date to get matches for
            
        Returns:
            list: List of match dictionaries
        """
        if not self.api_ready:
            print("API key not available, using fallback data")
            return None  # Return None to indicate fallback should be used
        
        cache_key = f"{sport}_{league}_{date.strftime('%Y-%m-%d')}"
        
        # Return cached data if available and not expired
        if cache_key in self.cache and time.time() < self.cache_expiry.get(cache_key, 0):
            return self.cache[cache_key]
        
        # Handle football data
        if sport == 'Football':
            matches = self._get_football_matches(league, date)
            
            # Cache the results
            if matches:
                self.cache[cache_key] = matches
                self.cache_expiry[cache_key] = time.time() + self.cache_duration
                
            return matches
            
        # For other sports, return None to use fallback data
        return None
        
    def _get_football_matches(self, league, date):
        """Get football matches for a specific league and date"""
        # Format date
        date_str = date.strftime('%Y-%m-%d')
        
        # API headers with authentication
        headers = {
            'X-Auth-Token': self.football_api_key
        }
        
        # Try getting matches for a specific league if we have a mapping
        league_code = self.league_mapping.get(league)
        league_matches = []
        
        if league_code:
            # API endpoint for league-specific matches
            league_endpoint = f"{self.football_base_url}/competitions/{league_code}/matches"
            
            # API parameters
            params = {
                'dateFrom': date_str,
                'dateTo': date_str
            }
            
            try:
                # Make the API request
                response = requests.get(league_endpoint, params=params, headers=headers)
                
                # Check if request was successful
                if response.status_code == 200:
                    data = response.json()
                    
                    # Process the matches
                    for match in data.get('matches', []):
                        match_dict = self._process_match_data(match, league)
                        league_matches.append(match_dict)
                        
                    if league_matches:
                        return league_matches
                    
                else:
                    print(f"League API request failed with status code: {response.status_code}")
                    print(f"Response: {response.text}")
                    
            except Exception as e:
                print(f"Error fetching league-specific football matches: {e}")
        
        # If we don't have league-specific matches, try getting all matches for this date
        try:
            # API endpoint for all matches
            all_matches_endpoint = f"{self.football_base_url}/matches"
            
            # API parameters
            params = {
                'dateFrom': date_str,
                'dateTo': date_str
            }
            
            # Make the API request
            response = requests.get(all_matches_endpoint, params=params, headers=headers)
            
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                all_matches = []
                
                # Process all matches, filtering for the requested league
                for match in data.get('matches', []):
                    # Check if this match is from the requested league
                    match_league = match.get('competition', {}).get('name', '')
                    
                    if match_league == league or (league_code and match.get('competition', {}).get('code', '') == league_code):
                        match_dict = self._process_match_data(match, league)
                        all_matches.append(match_dict)
                
                if all_matches:
                    return all_matches
                
            else:
                print(f"All matches API request failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"Error fetching all football matches: {e}")
        
        return None
        
    def _process_match_data(self, match, league):
        """Process match data from the API into our format"""
        match_dict = {
            'sport': 'Football',
            'league': league,
            'home_team': match.get('homeTeam', {}).get('name', 'Unknown'),
            'away_team': match.get('awayTeam', {}).get('name', 'Unknown'),
            'date': datetime.strptime(match.get('utcDate', ''), '%Y-%m-%dT%H:%M:%SZ'),
            'stadium': match.get('venue', 'Unknown Stadium'),
            'city': '',  # Not provided by this API
            'country': match.get('area', {}).get('name', ''),
            'home_odds': 2.0,  # Default odds
            'draw_odds': 3.0,  # Default odds
            'away_odds': 3.5,  # Default odds
            'home_form': '',  # Not provided by this API
            'away_form': '',  # Not provided by this API
            'historical_matchups': [],  # Not provided by this API
            'home_formation': '',  # Not provided by this API
            'away_formation': ''  # Not provided by this API
        }
        
        # Add score if available (for finished matches)
        if match.get('status') == 'FINISHED':
            score = match.get('score', {})
            full_time = score.get('fullTime', {})
            match_dict['home_score'] = full_time.get('home')
            match_dict['away_score'] = full_time.get('away')
        
        # Add some randomly generated odds (since the API doesn't provide them)
        match_dict['home_odds'] = round(random.uniform(1.5, 4.0), 2)
        match_dict['draw_odds'] = round(random.uniform(2.5, 4.5), 2)
        match_dict['away_odds'] = round(random.uniform(1.5, 4.0), 2)
        
        return match_dict
            
    def check_api_status(self):
        """
        Check if the APIs are available and working
        
        Returns:
            dict: Status of each API
        """
        status = {
            'football_api': False
        }
        
        # Check football API
        if self.football_api_key:
            try:
                endpoint = f"{self.football_base_url}/competitions"
                headers = {'X-Auth-Token': self.football_api_key}
                response = requests.get(endpoint, headers=headers)
                status['football_api'] = response.status_code == 200
            except:
                pass
                
        return status