"""
API Integrations module for ArcanShadow
Handles connection to various external APIs for real data

This module connects to:
1. The Odds API - For real-time betting odds
2. API-Sports - For live match data and statistics
3. Astrology API - For astronomical data
"""

import os
import requests
import json
import time
from datetime import datetime, timedelta

class APIIntegrations:
    """Main class for handling all API integrations for ArcanShadow."""
    
    def __init__(self):
        """Initialize API connections and configurations."""
        # Check available API keys from environment
        self.odds_api_key = os.environ.get('ODDS_API_KEY', '')
        self.api_sports_key = os.environ.get('API_SPORTS_KEY', '')
        self.astrology_api_key = os.environ.get('ASTROLOGY_API_KEY', '')
        
        # Check which APIs are available
        self.odds_api_available = bool(self.odds_api_key)
        self.api_sports_available = bool(self.api_sports_key)
        self.astrology_api_available = bool(self.astrology_api_key)
        
        # Base URLs for APIs
        self.odds_api_base_url = "https://api.the-odds-api.com/v4"
        self.api_sports_base_url = "https://v3.football.api-sports.io"
        self.astrology_api_base_url = "https://json.astrologyapi.com/v1"
        
        # Cache to reduce API calls
        self.cache = {}
        self.cache_expiry = {}
        self.cache_durations = {
            'odds': 5 * 60,  # 5 minutes for betting odds
            'matches': 30 * 60,  # 30 minutes for match data
            'astro': 24 * 60 * 60  # 24 hours for astrological data (changes slowly)
        }
    
    def get_odds(self, sport, league_or_event=None, date=None):
        """
        Get current betting odds from The Odds API
        
        Args:
            sport (str): Sport to get odds for (e.g., 'soccer', 'basketball')
            league_or_event (str, optional): Specific league or event
            date (datetime.date, optional): Date to get odds for
            
        Returns:
            dict: Odds data or None if unavailable
        """
        if not self.odds_api_available:
            print("The Odds API key not available")
            return None
            
        # Create cache key
        cache_key = f"odds_{sport}_{league_or_event}_{date.strftime('%Y-%m-%d') if date else 'now'}"
        
        # Return cached data if available and not expired
        if cache_key in self.cache and time.time() < self.cache_expiry.get(cache_key, 0):
            return self.cache[cache_key]
            
        # Build request parameters
        endpoint = f"{self.odds_api_base_url}/sports/{sport}/odds"
        params = {
            'apiKey': self.odds_api_key,
            'regions': 'uk,us,eu',  # Get odds from multiple regions
            'markets': 'h2h,spreads,totals',  # Get multiple market types
            'oddsFormat': 'decimal'
        }
        
        # Add date parameter if provided
        if date:
            params['commenceTimeTo'] = (date + timedelta(days=1)).strftime('%Y-%m-%dT00:00:00Z')
            params['commenceTimeFrom'] = date.strftime('%Y-%m-%dT00:00:00Z')
            
        # Add league parameter if provided
        if league_or_event:
            # Map ArcanShadow league names to The Odds API format
            league_mapping = {
                'Premier League': 'soccer_epl',
                'La Liga': 'soccer_spain_la_liga',
                'Bundesliga': 'soccer_germany_bundesliga',
                'Serie A': 'soccer_italy_serie_a',
                'Ligue 1': 'soccer_france_ligue_one',
                'Champions League': 'soccer_uefa_champs_league',
                'MLS': 'soccer_usa_mls',
                'Campeonato Brasileiro Série A': 'soccer_brazil_campeonato'
            }
            params['league'] = league_mapping.get(league_or_event, league_or_event)
        
        try:
            # Make the API request
            response = requests.get(endpoint, params=params)
            
            if response.status_code == 200:
                odds_data = response.json()
                
                # Process the data into our format
                processed_odds = self._process_odds_data(odds_data, sport)
                
                # Cache the results
                self.cache[cache_key] = processed_odds
                self.cache_expiry[cache_key] = time.time() + self.cache_durations['odds']
                
                return processed_odds
            else:
                print(f"The Odds API request failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error fetching odds data: {e}")
            return None
    
    def get_live_match_data(self, match_id=None, fixture_id=None):
        """
        Get live match data from API-Sports
        
        Args:
            match_id (str, optional): Specific match ID to get data for
            fixture_id (int, optional): Specific fixture ID for API-Sports
            
        Returns:
            dict: Live match data or None if unavailable
        """
        if not self.api_sports_available:
            print("API-Sports key not available")
            return None
            
        # Create cache key - for live data, we don't cache for long
        cache_key = f"live_{match_id or fixture_id}_live"
        
        # Build request parameters
        if fixture_id:
            endpoint = f"{self.api_sports_base_url}/fixtures"
            params = {'id': fixture_id}
        else:
            # Get all current live matches
            endpoint = f"{self.api_sports_base_url}/fixtures"
            params = {'live': 'all'}
            
        headers = {
            'x-rapidapi-key': self.api_sports_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
        
        try:
            # Make the API request
            response = requests.get(endpoint, params=params, headers=headers)
            
            if response.status_code == 200:
                match_data = response.json()
                
                # Process the data into our format
                processed_match = self._process_match_data(match_data)
                
                # We don't cache live data for long - just 30 seconds
                self.cache[cache_key] = processed_match
                self.cache_expiry[cache_key] = time.time() + 30  # 30 seconds
                
                return processed_match
            else:
                print(f"API-Sports request failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error fetching live match data: {e}")
            return None
    
    def get_planetary_positions(self, date=None):
        """
        Get planetary positions from Astrology API
        
        Args:
            date (datetime.date, optional): Date to get positions for
            
        Returns:
            dict: Planetary positions or None if unavailable
        """
        if not self.astrology_api_available:
            print("Astrology API key not available")
            return None
            
        # Default to today if no date provided
        if not date:
            date = datetime.now().date()
            
        # Create cache key
        cache_key = f"astro_{date.strftime('%Y-%m-%d')}"
        
        # Return cached data if available and not expired
        if cache_key in self.cache and time.time() < self.cache_expiry.get(cache_key, 0):
            return self.cache[cache_key]
            
        # Build request parameters
        endpoint = f"{self.astrology_api_base_url}/planets"
        
        # Format date as required by API
        date_str = date.strftime('%Y-%m-%d')
        
        # Data to send in the request
        data = {
            'day': date.day,
            'month': date.month,
            'year': date.year,
            'hour': 12,  # Noon
            'min': 0,
            'lat': 0,  # Default to equator
            'lon': 0,  # Default to Greenwich
            'tzone': 0  # UTC
        }
        
        headers = {
            'Authorization': f'Basic {self.astrology_api_key}'
        }
        
        try:
            # Make the API request
            response = requests.post(endpoint, json=data, headers=headers)
            
            if response.status_code == 200:
                astro_data = response.json()
                
                # Process the data into our format
                processed_data = self._process_astro_data(astro_data)
                
                # Cache the results
                self.cache[cache_key] = processed_data
                self.cache_expiry[cache_key] = time.time() + self.cache_durations['astro']
                
                return processed_data
            else:
                print(f"Astrology API request failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error fetching astrological data: {e}")
            return None
    
    def get_team_historical_data(self, team_name, league=None, last_n_matches=10):
        """
        Get historical data for a team from API-Sports
        
        Args:
            team_name (str): Name of the team
            league (str, optional): League name
            last_n_matches (int): Number of past matches to retrieve
            
        Returns:
            dict: Team historical data or None if unavailable
        """
        if not self.api_sports_available:
            print("API-Sports key not available")
            return None
            
        # Create cache key
        cache_key = f"team_history_{team_name}_{league}_{last_n_matches}"
        
        # Return cached data if available and not expired
        if cache_key in self.cache and time.time() < self.cache_expiry.get(cache_key, 0):
            return self.cache[cache_key]
            
        # First, we need to find the team ID in the API
        team_id = self._get_team_id(team_name, league)
        if not team_id:
            print(f"Could not find team ID for {team_name}")
            return None
            
        # Build request parameters for team's last matches
        endpoint = f"{self.api_sports_base_url}/fixtures"
        params = {
            'team': team_id,
            'last': last_n_matches
        }
        
        headers = {
            'x-rapidapi-key': self.api_sports_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
        
        try:
            # Make the API request
            response = requests.get(endpoint, params=params, headers=headers)
            
            if response.status_code == 200:
                history_data = response.json()
                
                # Process the data into our format
                processed_history = self._process_team_history(history_data, team_name)
                
                # Cache the results
                self.cache[cache_key] = processed_history
                self.cache_expiry[cache_key] = time.time() + self.cache_durations['matches']
                
                return processed_history
            else:
                print(f"API-Sports request failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error fetching team historical data: {e}")
            return None
    
    def get_head_to_head(self, team1, team2, last_n_matches=10):
        """
        Get head-to-head data for two teams from API-Sports
        
        Args:
            team1 (str): Name of the first team
            team2 (str): Name of the second team
            last_n_matches (int): Number of past head-to-head matches to retrieve
            
        Returns:
            dict: Head-to-head data or None if unavailable
        """
        if not self.api_sports_available:
            print("API-Sports key not available")
            return None
            
        # Create cache key
        cache_key = f"h2h_{team1}_{team2}_{last_n_matches}"
        
        # Return cached data if available and not expired
        if cache_key in self.cache and time.time() < self.cache_expiry.get(cache_key, 0):
            return self.cache[cache_key]
            
        # Find team IDs
        team1_id = self._get_team_id(team1)
        team2_id = self._get_team_id(team2)
        
        if not team1_id or not team2_id:
            print(f"Could not find team IDs for {team1} and/or {team2}")
            return None
            
        # Build request parameters
        endpoint = f"{self.api_sports_base_url}/fixtures/headtohead"
        params = {
            'h2h': f"{team1_id}-{team2_id}",
            'last': last_n_matches
        }
        
        headers = {
            'x-rapidapi-key': self.api_sports_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
        
        try:
            # Make the API request
            response = requests.get(endpoint, params=params, headers=headers)
            
            if response.status_code == 200:
                h2h_data = response.json()
                
                # Process the data into our format
                processed_h2h = self._process_h2h_data(h2h_data, team1, team2)
                
                # Cache the results
                self.cache[cache_key] = processed_h2h
                self.cache_expiry[cache_key] = time.time() + self.cache_durations['matches']
                
                return processed_h2h
            else:
                print(f"API-Sports request failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error fetching head-to-head data: {e}")
            return None
    
    def _process_odds_data(self, odds_data, sport):
        """Process odds data from The Odds API into our format"""
        processed_odds = []
        
        for event in odds_data:
            match_odds = {
                'event_id': event.get('id'),
                'sport': sport,
                'league': event.get('sport_title'),
                'home_team': event.get('home_team'),
                'away_team': event.get('away_team'),
                'match_time': event.get('commence_time'),
                'markets': {}
            }
            
            # Process different market types
            for bookmaker in event.get('bookmakers', []):
                for market in bookmaker.get('markets', []):
                    market_type = market.get('key')
                    if market_type not in match_odds['markets']:
                        match_odds['markets'][market_type] = {}
                    
                    # Process outcomes
                    for outcome in market.get('outcomes', []):
                        name = outcome.get('name')
                        price = outcome.get('price')
                        if name and price:
                            if market_type == 'h2h':
                                if name == event.get('home_team'):
                                    match_odds['home_odds'] = price
                                elif name == event.get('away_team'):
                                    match_odds['away_odds'] = price
                                elif name.lower() == 'draw':
                                    match_odds['draw_odds'] = price
                            
                            if market_type not in match_odds['markets']:
                                match_odds['markets'][market_type] = {}
                            
                            match_odds['markets'][market_type][name] = price
            
            processed_odds.append(match_odds)
        
        return processed_odds
    
    def _process_match_data(self, match_data):
        """Process match data from API-Sports into our format"""
        processed_matches = []
        
        for fixture in match_data.get('response', []):
            fixture_data = fixture.get('fixture', {})
            league_data = fixture.get('league', {})
            teams_data = fixture.get('teams', {})
            goals_data = fixture.get('goals', {})
            score_data = fixture.get('score', {})
            
            match = {
                'fixture_id': fixture_data.get('id'),
                'event_timestamp': fixture_data.get('timestamp'),
                'status': fixture_data.get('status', {}).get('long'),
                'elapsed': fixture_data.get('status', {}).get('elapsed'),
                'league': league_data.get('name'),
                'country': league_data.get('country'),
                'home_team': teams_data.get('home', {}).get('name'),
                'away_team': teams_data.get('away', {}).get('name'),
                'home_logo': teams_data.get('home', {}).get('logo'),
                'away_logo': teams_data.get('away', {}).get('logo'),
                'home_score': goals_data.get('home', 0),
                'away_score': goals_data.get('away', 0),
                'halftime_score': score_data.get('halftime', {})
            }
            
            processed_matches.append(match)
        
        return processed_matches
    
    def _process_astro_data(self, astro_data):
        """Process astrological data into our format"""
        processed_data = {
            'planets': {},
            'houses': {},
            'aspects': []
        }
        
        for planet in astro_data:
            name = planet.get('name', '')
            if name:
                processed_data['planets'][name] = {
                    'sign': planet.get('sign'),
                    'sign_num': planet.get('sign_num'),
                    'degrees': planet.get('norm_degree'),
                    'retrograde': planet.get('is_retro') == 1,
                    'house': planet.get('house')
                }
        
        return processed_data
    
    def _process_team_history(self, history_data, team_name):
        """Process team historical data into our format"""
        processed_history = {
            'team': team_name,
            'matches': [],
            'stats': {
                'total_wins': 0,
                'total_draws': 0,
                'total_losses': 0,
                'goals_scored': 0,
                'goals_conceded': 0,
                'clean_sheets': 0
            }
        }
        
        for fixture in history_data.get('response', []):
            fixture_data = fixture.get('fixture', {})
            teams_data = fixture.get('teams', {})
            goals_data = fixture.get('goals', {})
            league_data = fixture.get('league', {})
            
            # Determine if team was home or away
            is_home = teams_data.get('home', {}).get('name') == team_name
            
            team_goals = goals_data.get('home' if is_home else 'away', 0) or 0
            opponent_goals = goals_data.get('away' if is_home else 'home', 0) or 0
            
            # Calculate result (win, draw, loss)
            if team_goals > opponent_goals:
                result = 'W'
                processed_history['stats']['total_wins'] += 1
            elif team_goals < opponent_goals:
                result = 'L'
                processed_history['stats']['total_losses'] += 1
            else:
                result = 'D'
                processed_history['stats']['total_draws'] += 1
            
            # Update stats
            processed_history['stats']['goals_scored'] += team_goals
            processed_history['stats']['goals_conceded'] += opponent_goals
            if opponent_goals == 0:
                processed_history['stats']['clean_sheets'] += 1
            
            # Add match details
            match = {
                'date': fixture_data.get('date'),
                'competition': league_data.get('name'),
                'opponent': teams_data.get('away' if is_home else 'home', {}).get('name'),
                'venue': 'Home' if is_home else 'Away',
                'result': result,
                'team_goals': team_goals,
                'opponent_goals': opponent_goals
            }
            
            processed_history['matches'].append(match)
        
        return processed_history
    
    def _process_h2h_data(self, h2h_data, team1, team2):
        """Process head-to-head data into our format"""
        processed_h2h = {
            'team1': team1,
            'team2': team2,
            'matches': [],
            'stats': {
                'team1_wins': 0,
                'team2_wins': 0,
                'draws': 0,
                'team1_goals': 0,
                'team2_goals': 0
            }
        }
        
        for fixture in h2h_data.get('response', []):
            fixture_data = fixture.get('fixture', {})
            teams_data = fixture.get('teams', {})
            goals_data = fixture.get('goals', {})
            league_data = fixture.get('league', {})
            
            team1_is_home = teams_data.get('home', {}).get('name') == team1
            
            team1_goals = goals_data.get('home' if team1_is_home else 'away', 0) or 0
            team2_goals = goals_data.get('away' if team1_is_home else 'home', 0) or 0
            
            # Calculate result
            if team1_goals > team2_goals:
                result = f"{team1} won"
                processed_h2h['stats']['team1_wins'] += 1
            elif team1_goals < team2_goals:
                result = f"{team2} won"
                processed_h2h['stats']['team2_wins'] += 1
            else:
                result = "Draw"
                processed_h2h['stats']['draws'] += 1
            
            # Update stats
            processed_h2h['stats']['team1_goals'] += team1_goals
            processed_h2h['stats']['team2_goals'] += team2_goals
            
            # Add match details
            match = {
                'date': fixture_data.get('date'),
                'competition': league_data.get('name'),
                'venue': fixture_data.get('venue', {}).get('name'),
                'result': result,
                'score': f"{team1_goals} - {team2_goals}"
            }
            
            processed_h2h['matches'].append(match)
        
        return processed_h2h
    
    def _get_team_id(self, team_name, league=None):
        """Get team ID from API-Sports by name"""
        # Create cache key
        cache_key = f"team_id_{team_name}_{league if league else ''}"
        
        # Return cached ID if available
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        # Build request parameters
        endpoint = f"{self.api_sports_base_url}/teams"
        params = {'name': team_name}
        
        if league:
            # Map ArcanShadow league names to API-Sports league IDs
            league_id_mapping = {
                'Premier League': 39,
                'La Liga': 140,
                'Bundesliga': 78,
                'Serie A': 135,
                'Ligue 1': 61,
                'Champions League': 2,
                'MLS': 253,
                'Campeonato Brasileiro Série A': 71
            }
            league_id = league_id_mapping.get(league)
            if league_id:
                params['league'] = league_id
        
        headers = {
            'x-rapidapi-key': self.api_sports_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
        
        try:
            # Make the API request
            response = requests.get(endpoint, params=params, headers=headers)
            
            if response.status_code == 200:
                teams_data = response.json()
                teams = teams_data.get('response', [])
                
                if teams:
                    team_id = teams[0].get('team', {}).get('id')
                    
                    # Cache the team ID
                    self.cache[cache_key] = team_id
                    
                    return team_id
                else:
                    print(f"No team found with name {team_name}")
                    return None
                    
            else:
                print(f"API-Sports request failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error fetching team ID: {e}")
            return None
    
    def check_api_status(self):
        """Check if all APIs are available and working"""
        status = {
            'odds_api': False,
            'api_sports': False,
            'astrology_api': False
        }
        
        # Check The Odds API
        if self.odds_api_available:
            try:
                endpoint = f"{self.odds_api_base_url}/sports"
                params = {'apiKey': self.odds_api_key}
                response = requests.get(endpoint, params=params)
                status['odds_api'] = response.status_code == 200
            except:
                pass
        
        # Check API-Sports
        if self.api_sports_available:
            try:
                endpoint = f"{self.api_sports_base_url}/status"
                headers = {
                    'x-rapidapi-key': self.api_sports_key,
                    'x-rapidapi-host': 'v3.football.api-sports.io'
                }
                response = requests.get(endpoint, headers=headers)
                status['api_sports'] = response.status_code == 200
            except:
                pass
        
        # Check Astrology API
        if self.astrology_api_available:
            try:
                endpoint = f"{self.astrology_api_base_url}/timezone_with_dst"
                headers = {'Authorization': f'Basic {self.astrology_api_key}'}
                response = requests.get(endpoint, headers=headers)
                status['astrology_api'] = response.status_code == 200
            except:
                pass
        
        return status