"""
Market Recommender Module for ArcanShadow.

This module implements a smart recommendation system for betting markets based on user
preferences, historical betting patterns, and current match predictions.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union

from utils.database import Database, UserBettingHistory, UserMarketPreference, MarketRecommendation

# Initialize database connection
db = Database()

# Set up logging
logger = logging.getLogger(__name__)


def get_market_recommendations(user_id: str, sport: Optional[str] = None, league: Optional[str] = None) -> List[MarketRecommendation]:
    """
    Get current market recommendations for a user.
    
    Args:
        user_id (str): User identifier
        sport (str, optional): Filter by sport
        league (str, optional): Filter by league
            
    Returns:
        list: List of MarketRecommendation objects
    """
    return db.get_market_recommendations(user_id, sport=sport, league=league)


class BettingMarketRecommender:
    """
    Betting market recommendation engine that analyzes user betting history
    and preferences to provide personalized market recommendations.
    """
    
    def __init__(self, user_id: str = "default_user"):
        """
        Initialize the market recommender for a specific user.
        
        Args:
            user_id (str): User identifier
        """
        self.user_id = user_id
        self.db = db
        
        # Make sure user preferences are up to date
        self.db.update_user_preferences(user_id)
    
    def get_user_preferences(self) -> List[UserMarketPreference]:
        """
        Get user market preferences.
        
        Returns:
            list: List of UserMarketPreference objects
        """
        return self.db.get_user_market_preferences(self.user_id)
    
    def calculate_match_market_score(self, match: Dict[str, Any], market_type: str) -> Dict[str, Union[float, str]]:
        """
        Calculate a recommendation score for a specific match and market type.
        
        Args:
            match (dict): Match information
            market_type (str): Type of betting market
            
        Returns:
            dict: Recommendation details including score and reason
        """
        # Get user preferences for this market type
        preferences = self.get_user_preferences()
        market_pref = next((p for p in preferences if p.market_type == market_type), None)
        
        # Default values if no preference exists
        preference_score = 0.0
        success_rate = 0.0
        
        if market_pref:
            preference_score = market_pref.preference_score / 100.0  # Convert to 0-1 scale
            success_rate = market_pref.success_rate if market_pref.success_rate else 0.0
        
        # Calculate various factors for recommendation
        
        # Factor 1: User's historical performance in this market (50%)
        historical_score = preference_score * 50.0
        
        # Factor 2: Match prediction confidence for this market (30%)
        # Try to find prediction for this match and market
        session = self.db.Session()
        try:
            prediction = session.query(self.db.Prediction).filter(
                self.db.Prediction.sport == match.get('sport'),
                self.db.Prediction.league == match.get('league'),
                self.db.Prediction.home_team == match.get('home_team'),
                self.db.Prediction.away_team == match.get('away_team')
            ).first()
            
            prediction_score = prediction.confidence * 30.0 if prediction else 15.0
        finally:
            session.close()
        
        # Factor 3: Team form and match significance (20%)
        form_score = 10.0  # Default middle value
        
        # Calculate final score as weighted sum of factors
        final_score = historical_score + prediction_score + form_score
        
        # Generate explanation
        reason = f"Ce marché correspond à votre historique de paris ({historical_score:.1f}/50). "
        
        if prediction:
            reason += f"Notre système prédit ce résultat avec une confiance de {prediction.confidence:.2f} ({prediction_score:.1f}/30). "
        else:
            reason += "Nous n'avons pas de prédiction spécifique pour ce match. "
            
        reason += f"Forme des équipes: {form_score:.1f}/20."
        
        return {
            "score": final_score,
            "reason": reason,
            "market_type": market_type
        }
    
    def generate_recommendations(self, sport: Optional[str] = None, limit: int = 10) -> List[MarketRecommendation]:
        """
        Generate market recommendations for upcoming matches.
        
        Args:
            sport (str, optional): Filter by sport
            limit (int): Maximum number of recommendations to generate
            
        Returns:
            list: List of generated MarketRecommendation objects
        """
        # Get upcoming matches
        session = self.db.Session()
        try:
            # Get matches happening in the next week
            start_date = datetime.now()
            end_date = start_date + timedelta(days=7)
            
            query = session.query(self.db.Match).filter(
                self.db.Match.date >= start_date,
                self.db.Match.date <= end_date
            )
            
            if sport:
                query = query.filter(self.db.Match.sport == sport)
                
            matches = query.order_by(self.db.Match.date).limit(30).all()
            
            # Get user preferences
            preferences = self.get_user_preferences()
            
            # If no preferences exist, use default market types
            if not preferences:
                market_types = ["1X2", "Over/Under 2.5", "BTTS", "Asian Handicap"]
            else:
                # Use top user preferred markets
                market_types = [p.market_type for p in preferences[:5]]
            
            # Generate recommendations for each match and preferred market type
            recommendations = []
            
            for match in matches:
                match_dict = {
                    'id': match.id,
                    'sport': match.sport,
                    'league': match.league,
                    'home_team': match.home_team,
                    'away_team': match.away_team,
                    'date': match.date
                }
                
                for market_type in market_types:
                    # Calculate recommendation score for this match and market
                    recommendation = self.calculate_match_market_score(match_dict, market_type)
                    
                    # Create recommendation object
                    rec_data = {
                        'user_id': self.user_id,
                        'match_id': match.id,
                        'sport': match.sport,
                        'league': match.league,
                        'market_type': market_type,
                        'recommendation_score': recommendation['score'],
                        'reason': recommendation['reason']
                    }
                    
                    # Save to database
                    rec_obj = self.db.save_market_recommendation(rec_data)
                    recommendations.append(rec_obj)
            
            # Return only the top recommendations
            recommendations.sort(key=lambda x: x.recommendation_score, reverse=True)
            return recommendations[:limit]
        
        finally:
            session.close()