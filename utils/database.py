"""
Database utilities for the ArcanShadow system.
Handles database connection, models, and operations.
"""

import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a base class for our models
Base = declarative_base()

# Define our models
class Prediction(Base):
    """Model for storing match predictions."""
    __tablename__ = 'predictions'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now)
    sport = Column(String(50), nullable=False)
    league = Column(String(50), nullable=False)
    home_team = Column(String(100), nullable=False)
    away_team = Column(String(100), nullable=False)
    prediction = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    outcome = Column(String(50), nullable=True)  # Actual outcome once known
    correct = Column(Boolean, nullable=True)  # Whether prediction was correct
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    arcanx_confidence = Column(Float, nullable=True)
    shadow_odds_confidence = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Prediction(id={self.id}, match='{self.home_team} vs {self.away_team}', prediction='{self.prediction}')>"


class Match(Base):
    """Model for storing match data."""
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    sport = Column(String(50), nullable=False)
    league = Column(String(50), nullable=False)
    home_team = Column(String(100), nullable=False)
    away_team = Column(String(100), nullable=False)
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    stadium = Column(String(100), nullable=True)
    city = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    home_odds = Column(Float, nullable=True)
    draw_odds = Column(Float, nullable=True)
    away_odds = Column(Float, nullable=True)
    home_form = Column(String(20), nullable=True)
    away_form = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Match(id={self.id}, match='{self.home_team} vs {self.away_team}', date='{self.date}')>"


class EsotericFactor(Base):
    """Model for storing esoteric factors used in predictions."""
    __tablename__ = 'esoteric_factors'
    
    id = Column(Integer, primary_key=True)
    prediction_id = Column(Integer, nullable=False)
    factor_name = Column(String(100), nullable=False)
    factor_value = Column(Text, nullable=False)
    influence_score = Column(Float, nullable=True)
    module_source = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<EsotericFactor(id={self.id}, name='{self.factor_name}')>"


class OddsFactor(Base):
    """Model for storing odds behavior factors used in predictions."""
    __tablename__ = 'odds_factors'
    
    id = Column(Integer, primary_key=True)
    prediction_id = Column(Integer, nullable=False)
    factor_name = Column(String(100), nullable=False)
    factor_value = Column(Text, nullable=False)
    influence_score = Column(Float, nullable=True)
    module_source = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<OddsFactor(id={self.id}, name='{self.factor_name}')>"


class SystemMetric(Base):
    """Model for storing system performance metrics."""
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    module = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<SystemMetric(id={self.id}, metric='{self.metric_name}', value={self.metric_value})>"


class UserBettingHistory(Base):
    """Model for storing user betting history."""
    __tablename__ = 'user_betting_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False, default="default_user")  # In a real system, this would be a foreign key
    date = Column(DateTime, default=datetime.now)
    sport = Column(String(50), nullable=False)
    league = Column(String(50), nullable=False)
    match_id = Column(Integer, nullable=True)
    market_type = Column(String(50), nullable=False)  # e.g., "1X2", "Over/Under", "BTTS"
    selection = Column(String(50), nullable=False)    # e.g., "Home Win", "Over 2.5"
    odds = Column(Float, nullable=False)
    stake = Column(Float, nullable=True)
    outcome = Column(String(20), nullable=True)       # "win", "loss", "void", "pending"
    return_amount = Column(Float, nullable=True)
    profit_loss = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<UserBettingHistory(id={self.id}, market='{self.market_type}', selection='{self.selection}', outcome='{self.outcome}')>"


class UserMarketPreference(Base):
    """Model for storing user market preferences calculated from betting history."""
    __tablename__ = 'user_market_preferences'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False, default="default_user")
    market_type = Column(String(50), nullable=False)
    preference_score = Column(Float, nullable=False)  # 0-100 score representing preference
    success_rate = Column(Float, nullable=True)       # Success rate in this market
    avg_odds = Column(Float, nullable=True)           # Average odds for this market
    frequency = Column(Integer, nullable=False)       # Number of bets in this market
    last_updated = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<UserMarketPreference(id={self.id}, market='{self.market_type}', score={self.preference_score})>"


class MarketRecommendation(Base):
    """Model for storing market recommendations for users."""
    __tablename__ = 'market_recommendations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False, default="default_user")
    match_id = Column(Integer, nullable=True)
    sport = Column(String(50), nullable=False)
    league = Column(String(50), nullable=False)
    market_type = Column(String(50), nullable=False)
    recommendation_score = Column(Float, nullable=False)  # 0-100 score
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<MarketRecommendation(id={self.id}, market='{self.market_type}', score={self.recommendation_score})>"


# Database connection and session management
class Database:
    """Database connection and operations manager."""
    
    def __init__(self, db_path=None):
        """Initialize database connection."""
        if db_path is None:
            db_path = os.environ.get('DATABASE_URL', 'sqlite:///arcanshadow.db')
        
        self.engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.engine)
        
        # Create tables if they don't exist
        Base.metadata.create_all(self.engine)
    
    def save_prediction(self, prediction_data):
        """
        Save a prediction to the database.
        
        Args:
            prediction_data (dict): Prediction data including match info, confidence, etc.
            
        Returns:
            Prediction: The saved prediction object
        """
        session = self.Session()
        try:
            prediction = Prediction(
                date=prediction_data.get('date', datetime.now()),
                sport=prediction_data.get('sport', ''),
                league=prediction_data.get('league', ''),
                home_team=prediction_data.get('home_team', ''),
                away_team=prediction_data.get('away_team', ''),
                prediction=prediction_data.get('prediction', ''),
                confidence=prediction_data.get('confidence', 0.0),
                arcanx_confidence=prediction_data.get('arcanx_confidence', 0.0),
                shadow_odds_confidence=prediction_data.get('shadow_odds_confidence', 0.0),
                notes=prediction_data.get('notes', '')
            )
            session.add(prediction)
            session.commit()
            
            # Save esoteric factors
            for factor in prediction_data.get('esoteric_factors', []):
                esoteric_factor = EsotericFactor(
                    prediction_id=prediction.id,
                    factor_name=factor.get('name', ''),
                    factor_value=factor.get('value', ''),
                    module_source=factor.get('source', '')
                )
                session.add(esoteric_factor)
            
            # Save odds factors
            for factor in prediction_data.get('odds_factors', []):
                odds_factor = OddsFactor(
                    prediction_id=prediction.id,
                    factor_name=factor.get('name', ''),
                    factor_value=factor.get('value', ''),
                    module_source=factor.get('source', '')
                )
                session.add(odds_factor)
            
            session.commit()
            return prediction
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def save_match(self, match_data):
        """
        Save match data to the database.
        
        Args:
            match_data (dict): Match information
            
        Returns:
            Match: The saved match object
        """
        session = self.Session()
        try:
            match = Match(
                date=match_data.get('date', datetime.now()),
                sport=match_data.get('sport', ''),
                league=match_data.get('league', ''),
                home_team=match_data.get('home_team', ''),
                away_team=match_data.get('away_team', ''),
                home_score=match_data.get('home_score'),
                away_score=match_data.get('away_score'),
                stadium=match_data.get('stadium', ''),
                city=match_data.get('city', ''),
                country=match_data.get('country', ''),
                home_odds=match_data.get('home_odds'),
                draw_odds=match_data.get('draw_odds'),
                away_odds=match_data.get('away_odds'),
                home_form=match_data.get('home_form', ''),
                away_form=match_data.get('away_form', '')
            )
            session.add(match)
            session.commit()
            return match
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_recent_predictions(self, limit=10, sport=None, league=None):
        """
        Get recent predictions from the database.
        
        Args:
            limit (int): Maximum number of predictions to return
            sport (str, optional): Filter by sport
            league (str, optional): Filter by league
            
        Returns:
            list: List of Prediction objects
        """
        session = self.Session()
        try:
            query = session.query(Prediction).order_by(Prediction.date.desc())
            
            if sport:
                query = query.filter(Prediction.sport == sport)
            
            if league:
                query = query.filter(Prediction.league == league)
            
            return query.limit(limit).all()
        finally:
            session.close()
            
    def get_completed_predictions(self, limit=20, sport=None, league=None):
        """
        Get completed predictions (with actual results) from the database.
        
        Args:
            limit (int): Maximum number of completed predictions to return
            sport (str, optional): Filter by sport
            league (str, optional): Filter by league
            
        Returns:
            list: List of Prediction objects that have been completed
        """
        session = self.Session()
        try:
            # Get predictions that have outcome and scores
            query = session.query(Prediction).filter(
                Prediction.home_score.isnot(None),
                Prediction.away_score.isnot(None)
            ).order_by(Prediction.date.desc())
            
            if sport:
                query = query.filter(Prediction.sport == sport)
            if league:
                query = query.filter(Prediction.league == league)
                
            predictions = query.limit(limit).all()
            return predictions
        except Exception as e:
            print(f"Error getting completed predictions: {e}")
            return []
        finally:
            session.close()
            
    def get_prediction_by_id(self, prediction_id):
        """
        Get a specific prediction by its ID.
        
        Args:
            prediction_id (int): The ID of the prediction to retrieve
            
        Returns:
            Prediction: The prediction object if found, None otherwise
        """
        session = self.Session()
        try:
            prediction = session.query(Prediction).filter(Prediction.id == prediction_id).first()
            return prediction
        except Exception as e:
            print(f"Error getting prediction by ID: {e}")
            return None
        finally:
            session.close()
    
    def get_prediction_accuracy(self, days=30, sport=None, league=None):
        """
        Calculate prediction accuracy over a time period.
        
        Args:
            days (int): Number of days to look back
            sport (str, optional): Filter by sport
            league (str, optional): Filter by league
            
        Returns:
            dict: Accuracy metrics
        """
        session = self.Session()
        try:
            from_date = datetime.now() - timedelta(days=days)
            
            query = session.query(Prediction).filter(
                Prediction.date >= from_date
            )
            query = query.filter(Prediction.correct != None)
            
            if sport:
                query = query.filter(Prediction.sport == sport)
            
            if league:
                query = query.filter(Prediction.league == league)
            
            predictions = query.all()
            
            total = len(predictions)
            correct = sum(1 for p in predictions if p.correct)
            
            return {
                'total': total,
                'correct': correct,
                'accuracy': correct / total if total > 0 else 0,
                'period_days': days
            }
        finally:
            session.close()
    
    def update_prediction_result(self, prediction_id, home_score, away_score, outcome, correct):
        """
        Update a prediction with the actual result.
        
        Args:
            prediction_id (int): ID of the prediction to update
            home_score (int): Final home team score
            away_score (int): Final away team score
            outcome (str): Actual outcome (e.g., "Home Win")
            correct (bool): Whether the prediction was correct
            
        Returns:
            Prediction: The updated prediction object
        """
        session = self.Session()
        try:
            prediction = session.query(Prediction).filter(Prediction.id == prediction_id).one()
            prediction.home_score = home_score
            prediction.away_score = away_score
            prediction.outcome = outcome
            prediction.correct = correct
            
            session.commit()
            return prediction
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def save_system_metric(self, metric_name, metric_value, module=None, notes=None):
        """
        Save a system performance metric.
        
        Args:
            metric_name (str): Name of the metric
            metric_value (float): Value of the metric
            module (str, optional): Module the metric relates to
            notes (str, optional): Additional notes
            
        Returns:
            SystemMetric: The saved metric object
        """
        session = self.Session()
        try:
            metric = SystemMetric(
                date=datetime.now(),
                metric_name=metric_name,
                metric_value=metric_value,
                module=module,
                notes=notes
            )
            session.add(metric)
            session.commit()
            return metric
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_system_metrics(self, days=30, module=None):
        """
        Get system metrics over a time period.
        
        Args:
            days (int): Number of days to look back
            module (str, optional): Filter by module
            
        Returns:
            list: List of SystemMetric objects
        """
        session = self.Session()
        try:
            from_date = datetime.now() - timedelta(days=days)
            
            query = session.query(SystemMetric).filter(SystemMetric.date >= from_date)
            
            if module:
                query = query.filter(SystemMetric.module == module)
            
            return query.all()
        finally:
            session.close()
    
    def save_user_bet(self, bet_data):
        """
        Save a user bet to the history.
        
        Args:
            bet_data (dict): Bet information including market type, selection, odds, etc.
            
        Returns:
            UserBettingHistory: The saved bet object
        """
        session = self.Session()
        try:
            bet = UserBettingHistory(
                user_id=bet_data.get('user_id', 'default_user'),
                date=bet_data.get('date', datetime.now()),
                sport=bet_data.get('sport', ''),
                league=bet_data.get('league', ''),
                match_id=bet_data.get('match_id'),
                market_type=bet_data.get('market_type', ''),
                selection=bet_data.get('selection', ''),
                odds=bet_data.get('odds', 0.0),
                stake=bet_data.get('stake'),
                outcome=bet_data.get('outcome', 'pending'),
                return_amount=bet_data.get('return_amount'),
                profit_loss=bet_data.get('profit_loss')
            )
            session.add(bet)
            session.commit()
            
            # Update user preferences after adding a new bet
            self.update_user_preferences(bet_data.get('user_id', 'default_user'))
            
            return bet
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def update_bet_outcome(self, bet_id, outcome, return_amount=None, profit_loss=None):
        """
        Update a bet with its outcome.
        
        Args:
            bet_id (int): ID of the bet to update
            outcome (str): Bet outcome ('win', 'loss', 'void')
            return_amount (float, optional): Total return amount
            profit_loss (float, optional): Profit or loss amount
            
        Returns:
            UserBettingHistory: The updated bet object
        """
        session = self.Session()
        try:
            bet = session.query(UserBettingHistory).filter(UserBettingHistory.id == bet_id).one()
            bet.outcome = outcome
            
            if return_amount is not None:
                bet.return_amount = return_amount
                
            if profit_loss is not None:
                bet.profit_loss = profit_loss
                
            session.commit()
            
            # Update user preferences after updating bet outcome
            self.update_user_preferences(bet.user_id)
            
            return bet
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_user_betting_history(self, user_id='default_user', days=90, sport=None, market_type=None):
        """
        Get a user's betting history.
        
        Args:
            user_id (str): User identifier
            days (int): Number of days to look back
            sport (str, optional): Filter by sport
            market_type (str, optional): Filter by market type
            
        Returns:
            list: List of UserBettingHistory objects
        """
        session = self.Session()
        try:
            from_date = datetime.now() - timedelta(days=days)
            
            query = session.query(UserBettingHistory).filter(
                UserBettingHistory.user_id == user_id,
                UserBettingHistory.date >= from_date
            ).order_by(UserBettingHistory.date.desc())
            
            if sport:
                query = query.filter(UserBettingHistory.sport == sport)
                
            if market_type:
                query = query.filter(UserBettingHistory.market_type == market_type)
                
            return query.all()
        finally:
            session.close()
    
    def update_user_preferences(self, user_id='default_user'):
        """
        Update a user's market preferences based on their betting history.
        
        Args:
            user_id (str): User identifier
            
        Returns:
            list: List of updated UserMarketPreference objects
        """
        session = self.Session()
        try:
            # Get user's betting history
            bets = session.query(UserBettingHistory).filter(
                UserBettingHistory.user_id == user_id
            ).all()
            
            # Group bets by market type
            market_stats = {}
            for bet in bets:
                market = bet.market_type
                if market not in market_stats:
                    market_stats[market] = {
                        'count': 0, 
                        'wins': 0, 
                        'total_odds': 0,
                        'total_profit': 0
                    }
                
                market_stats[market]['count'] += 1
                market_stats[market]['total_odds'] += bet.odds
                
                if bet.outcome == 'win':
                    market_stats[market]['wins'] += 1
                    
                if bet.profit_loss:
                    market_stats[market]['total_profit'] += bet.profit_loss
            
            # Calculate preference scores based on frequency, success rate, and profitability
            updated_preferences = []
            for market, stats in market_stats.items():
                # Calculate metrics
                count = stats['count']
                win_rate = stats['wins'] / count if count > 0 else 0
                avg_odds = stats['total_odds'] / count if count > 0 else 0
                
                # Calculate preference score (0-100)
                # Weighted combination of frequency, win rate, and profitability
                frequency_weight = min(count / 10, 1.0) * 25  # Max 25 points from frequency
                win_rate_weight = win_rate * 50               # Max 50 points from win rate
                profit_weight = min(stats['total_profit'] / 100, 1.0) * 25 if stats['total_profit'] > 0 else 0  # Max 25 points from profit
                
                preference_score = frequency_weight + win_rate_weight + profit_weight
                
                # Update or create preference
                preference = session.query(UserMarketPreference).filter(
                    UserMarketPreference.user_id == user_id,
                    UserMarketPreference.market_type == market
                ).first()
                
                if preference:
                    preference.preference_score = preference_score
                    preference.success_rate = win_rate
                    preference.avg_odds = avg_odds
                    preference.frequency = count
                    preference.last_updated = datetime.now()
                else:
                    preference = UserMarketPreference(
                        user_id=user_id,
                        market_type=market,
                        preference_score=preference_score,
                        success_rate=win_rate,
                        avg_odds=avg_odds,
                        frequency=count
                    )
                    session.add(preference)
                
                updated_preferences.append(preference)
            
            session.commit()
            return updated_preferences
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_user_market_preferences(self, user_id='default_user'):
        """
        Get a user's market preferences.
        
        Args:
            user_id (str): User identifier
            
        Returns:
            list: List of UserMarketPreference objects sorted by preference score
        """
        session = self.Session()
        try:
            preferences = session.query(UserMarketPreference).filter(
                UserMarketPreference.user_id == user_id
            ).order_by(UserMarketPreference.preference_score.desc()).all()
            
            return preferences
        finally:
            session.close()
    
    def save_market_recommendation(self, recommendation_data):
        """
        Save a market recommendation.
        
        Args:
            recommendation_data (dict): Recommendation information
            
        Returns:
            MarketRecommendation: The saved recommendation object
        """
        session = self.Session()
        try:
            recommendation = MarketRecommendation(
                user_id=recommendation_data.get('user_id', 'default_user'),
                match_id=recommendation_data.get('match_id'),
                sport=recommendation_data.get('sport', ''),
                league=recommendation_data.get('league', ''),
                market_type=recommendation_data.get('market_type', ''),
                recommendation_score=recommendation_data.get('recommendation_score', 0),
                reason=recommendation_data.get('reason', '')
            )
            session.add(recommendation)
            session.commit()
            return recommendation
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_market_recommendations(self, user_id='default_user', sport=None, league=None):
        """
        Get market recommendations for a user.
        
        Args:
            user_id (str): User identifier
            sport (str, optional): Filter by sport
            league (str, optional): Filter by league
            
        Returns:
            list: List of MarketRecommendation objects sorted by recommendation score
        """
        session = self.Session()
        try:
            query = session.query(MarketRecommendation).filter(
                MarketRecommendation.user_id == user_id
            ).order_by(MarketRecommendation.recommendation_score.desc())
            
            if sport:
                query = query.filter(MarketRecommendation.sport == sport)
                
            if league:
                query = query.filter(MarketRecommendation.league == league)
                
            # Only get recommendations from the last day
            from_date = datetime.now() - timedelta(days=1)
            query = query.filter(MarketRecommendation.created_at >= from_date)
            
            return query.all()
        finally:
            session.close()


# Create database instance
db = Database()