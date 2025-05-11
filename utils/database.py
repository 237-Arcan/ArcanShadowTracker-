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


# Create database instance
db = Database()