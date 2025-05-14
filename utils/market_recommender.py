"""
Système de recommandation intelligent pour sélection de marchés de paris.
Analyse l'historique des paris de l'utilisateur et les tendances de réussite
pour suggérer des marchés de paris personnalisés.
"""

import random
from datetime import datetime
import pandas as pd
import numpy as np
from utils.database import db, Match, Prediction, UserMarketPreference, MarketRecommendation

class BettingMarketRecommender:
    """
    Système de recommandation intelligent pour les marchés de paris sportifs.
    Utilise l'historique de l'utilisateur et des modèles de prédiction pour
    suggérer des marchés de paris personnalisés.
    """
    
    # Définition des types de marchés disponibles
    MARKET_TYPES = {
        "football": [
            "1X2",                  # Victoire domicile, nul, victoire extérieur
            "Double Chance",        # 1X, 12, X2
            "BTTS",                 # Les deux équipes marquent
            "Over/Under 2.5",       # Plus/moins de 2.5 buts
            "Over/Under 1.5",       # Plus/moins de 1.5 buts
            "Correct Score",        # Score exact
            "Half-time/Full-time",  # Résultat à la mi-temps/fin du match
            "First Team to Score",  # Première équipe à marquer
            "Handicap",             # Paris avec handicap
            "Draw No Bet",          # Remboursement en cas de match nul
            "Win to Nil",           # Victoire sans encaisser de but
            "Win Both Halves",      # Gagner les deux mi-temps
            "Score in Both Halves", # Marquer dans les deux mi-temps
            "Clean Sheet",          # Ne pas encaisser de but
            "Win From Behind",      # Gagner après avoir été mené
            "Score Exact First Half" # Score exact à la mi-temps
        ],
        "basketball": [
            "Money Line",           # Vainqueur du match
            "Point Spread",         # Écart de points
            "Over/Under",           # Total de points
            "Race to 20",           # Premier à 20 points
            "Player Points",        # Points marqués par un joueur
            "Quarter Winner",       # Vainqueur d'un quart-temps
            "Halftime/Fulltime",    # Résultat à la mi-temps/fin du match
            "Margin of Victory",    # Marge de victoire
            "3-Point Field Goals",  # Nombre de tirs à 3 points
            "Team to Score First",  # Équipe qui marque en premier
            "Highest Scoring Quarter" # Quart-temps le plus prolifique
        ],
        "tennis": [
            "Match Winner",         # Vainqueur du match
            "Set Betting",          # Score en sets
            "Total Games",          # Nombre total de jeux
            "Games Handicap",       # Handicap en jeux
            "Player to Win a Set",  # Joueur gagnant au moins un set
            "Total Sets",           # Nombre total de sets
            "First Set Winner",     # Vainqueur du premier set
            "Correct Score in Set", # Score exact dans un set
            "Tie Break in Match",   # Tie-break dans le match
            "To Win From Behind",   # Gagner après avoir perdu un set
            "Player Games Won"      # Nombre de jeux gagnés par un joueur
        ]
    }
    
    def __init__(self, user_id="default_user"):
        """
        Initialise le système de recommandation.
        
        Args:
            user_id (str): Identifiant de l'utilisateur
        """
        self.user_id = user_id
        self.preference_weight = 0.4  # Poids des préférences utilisateur
        self.prediction_weight = 0.4  # Poids des prédictions système
        self.form_weight = 0.2        # Poids de la forme récente
    
    def generate_recommendations(self, match_id=None, sport=None, league=None):
        """
        Génère des recommandations de marchés de paris pour un match spécifique
        ou pour tous les matchs à venir dans un sport/ligue.
        
        Args:
            match_id (int, optional): ID du match pour lequel générer des recommandations
            sport (str, optional): Sport pour lequel générer des recommandations
            league (str, optional): Ligue pour laquelle générer des recommandations
            
        Returns:
            list: Liste de recommandations générées
        """
        # Récupérer les préférences utilisateur
        user_preferences = db.get_user_market_preferences(self.user_id)
        
        # Convertir en dictionnaire pour un accès facile
        preferences_dict = {p.market_type: p.preference_score for p in user_preferences}
        
        # Récupérer les matchs pour lesquels générer des recommandations
        session = db.Session()
        try:
            matches_query = session.query(Match)
            
            # Filtrer les matchs futurs (aujourd'hui ou plus tard)
            from_date = datetime.now()
            matches_query = matches_query.filter(Match.date >= from_date)
            
            if match_id:
                matches_query = matches_query.filter(Match.id == match_id)
            if sport:
                matches_query = matches_query.filter(Match.sport == sport)
            if league:
                matches_query = matches_query.filter(Match.league == league)
                
            matches = matches_query.all()
            
            all_recommendations = []
            
            # Pour chaque match, générer des recommandations de marchés
            for match in matches:
                # Sélectionner les types de marché disponibles pour ce sport
                available_markets = self.MARKET_TYPES.get(match.sport.lower(), [])
                if not available_markets:
                    # Si le sport n'est pas reconnu, utiliser une liste générique
                    available_markets = ["1X2", "Over/Under", "BTTS"]
                
                # Récupérer les prédictions existantes pour ce match
                predictions = session.query(Prediction).filter(
                    Prediction.sport == match.sport,
                    Prediction.league == match.league,
                    Prediction.home_team == match.home_team,
                    Prediction.away_team == match.away_team
                ).all()
                
                # Calculer les scores de recommandation pour chaque marché
                market_scores = {}
                for market_type in available_markets:
                    # 1. Score basé sur les préférences utilisateur (0-100)
                    preference_score = preferences_dict.get(market_type, 50)  # Valeur par défaut si pas d'historique
                    
                    # 2. Score basé sur les prédictions système (0-100)
                    prediction_score = self._calculate_prediction_score(predictions, market_type)
                    
                    # 3. Score basé sur la forme récente des équipes (0-100)
                    form_score = self._calculate_form_score(match, market_type)
                    
                    # Calcul du score final pondéré
                    final_score = (
                        self.preference_weight * preference_score +
                        self.prediction_weight * prediction_score +
                        self.form_weight * form_score
                    )
                    
                    market_scores[market_type] = final_score
                
                # Sélectionner les 3 meilleurs marchés pour ce match
                top_markets = sorted(market_scores.items(), key=lambda x: x[1], reverse=True)[:3]
                
                # Enregistrer les recommandations
                for market_type, score in top_markets:
                    reason = self._generate_recommendation_reason(
                        match, market_type, 
                        preference_score, prediction_score, form_score
                    )
                    
                    recommendation_data = {
                        'user_id': self.user_id,
                        'match_id': match.id,
                        'sport': match.sport,
                        'league': match.league,
                        'market_type': market_type,
                        'recommendation_score': score,
                        'reason': reason
                    }
                    
                    # Sauvegarder la recommandation dans la base de données
                    recommendation = db.save_market_recommendation(recommendation_data)
                    all_recommendations.append(recommendation)
            
            return all_recommendations
                    
        finally:
            session.close()
    
    def _calculate_prediction_score(self, predictions, market_type):
        """
        Calcule un score de confiance pour un type de marché basé sur les prédictions.
        
        Args:
            predictions (list): Liste des prédictions pour un match
            market_type (str): Type de marché à évaluer
            
        Returns:
            float: Score de prédiction (0-100)
        """
        if not predictions:
            return 50  # Score neutre en l'absence de prédictions
        
        # Chaque module du système a des affinités pour certains types de marchés
        module_market_affinity = {
            "ShadowOdds": ["1X2", "Over/Under 2.5", "Double Chance"],
            "MomentumTracker": ["BTTS", "Over/Under 1.5", "First Team to Score"],
            "AstroImpact": ["1X2", "Half-time/Full-time", "Correct Score"],
            "EchoPath": ["1X2", "Win to Nil", "Win Both Halves"],
            "VolumeAnalyzer": ["1X2", "Over/Under 2.5", "Draw No Bet"]
        }
        
        # Variables pour le calcul du score
        total_confidence = 0
        relevant_predictions = 0
        
        # Évaluer l'adéquation des prédictions au marché
        for prediction in predictions:
            # Récupérer les facteurs ésotériques pour cette prédiction
            # Simulons la source des facteurs (normalement stockée dans la base de données)
            module_sources = ["ShadowOdds", "MomentumTracker", "AstroImpact", "EchoPath", "VolumeAnalyzer"]
            
            for module in module_sources:
                if market_type in module_market_affinity.get(module, []):
                    # Ce module est pertinent pour ce type de marché
                    relevant_predictions += 1
                    
                    # Utiliser la confiance globale ou spécifique au module si disponible
                    if module == "ShadowOdds" and prediction.shadow_odds_confidence:
                        total_confidence += prediction.shadow_odds_confidence * 100
                    elif module == "ArcanX" and prediction.arcanx_confidence:
                        total_confidence += prediction.arcanx_confidence * 100
                    else:
                        total_confidence += prediction.confidence * 100
        
        if relevant_predictions == 0:
            return 50  # Score neutre si aucune prédiction pertinente
        
        # Calculer le score moyen
        return total_confidence / relevant_predictions
    
    def _calculate_form_score(self, match, market_type):
        """
        Calcule un score basé sur la forme récente des équipes.
        
        Args:
            match (Match): Objet match
            market_type (str): Type de marché à évaluer
            
        Returns:
            float: Score de forme (0-100)
        """
        # Récupérer la forme des équipes (W=win, D=draw, L=loss), ex: "WWDLW"
        home_form = match.home_form or "WDLWW"  # Exemple par défaut si non disponible
        away_form = match.away_form or "LWDWL"  # Exemple par défaut si non disponible
        
        # Convertir la forme en valeurs numériques
        form_values = {"W": 3, "D": 1, "L": 0}
        
        home_score = sum(form_values.get(result, 0) for result in home_form) / (len(home_form) * 3) * 100
        away_score = sum(form_values.get(result, 0) for result in away_form) / (len(away_form) * 3) * 100
        
        # Adapter le score en fonction du type de marché
        if market_type == "1X2":
            if home_score > away_score + 20:
                return 80  # Forte recommandation pour victoire à domicile
            elif away_score > home_score + 20:
                return 80  # Forte recommandation pour victoire à l'extérieur
            else:
                return 60  # Recommandation modérée pour un match nul
        elif market_type == "BTTS":
            # Recommander "Les deux équipes marquent" si les deux équipes sont en forme
            if home_score > 60 and away_score > 60:
                return 90
            else:
                return 50
        elif market_type == "Over/Under 2.5":
            # Recommander "Plus de 2.5 buts" si les deux équipes sont en forme
            if home_score > 70 and away_score > 50:
                return 85
            elif home_score > 50 and away_score > 70:
                return 85
            else:
                return 60
        
        # Valeur par défaut pour les autres types de marchés
        return 65
    
    def _generate_recommendation_reason(self, match, market_type, preference_score, prediction_score, form_score):
        """
        Génère une explication textuelle pour une recommandation de marché.
        
        Args:
            match (Match): Objet match
            market_type (str): Type de marché recommandé
            preference_score (float): Score de préférence utilisateur
            prediction_score (float): Score basé sur les prédictions
            form_score (float): Score basé sur la forme des équipes
            
        Returns:
            str: Explication textuelle de la recommandation
        """
        reasons = []
        
        # Ajouter une raison basée sur les préférences utilisateur
        if preference_score > 80:
            reasons.append(f"Ce marché '{market_type}' est parmi vos plus performants historiquement.")
        elif preference_score > 60:
            reasons.append(f"Vous avez eu un bon succès avec les paris '{market_type}' par le passé.")
        elif preference_score > 0:
            reasons.append(f"Basé sur votre historique de paris sur '{market_type}'.")
        
        # Ajouter une raison basée sur les prédictions système
        if prediction_score > 80:
            reasons.append("Nos modules de prédiction sont très confiants pour ce marché.")
        elif prediction_score > 60:
            reasons.append("Plusieurs de nos indicateurs prédictifs favorisent ce marché.")
        
        # Ajouter une raison basée sur la forme des équipes
        if form_score > 80:
            reasons.append("La forme récente des équipes est particulièrement favorable pour ce type de pari.")
        elif form_score > 60:
            reasons.append("Les tendances de forme récente supportent ce marché.")
        
        # Raisons spécifiques au type de marché
        if market_type == "1X2":
            if match.home_odds and match.away_odds:
                if match.home_odds < match.away_odds:
                    reasons.append(f"{match.home_team} est favori selon les cotes ({match.home_odds:.2f}).")
                else:
                    reasons.append(f"{match.away_team} est favori selon les cotes ({match.away_odds:.2f}).")
        elif market_type == "BTTS":
            if match.home_form and match.away_form:
                home_scores = sum(1 for result in match.home_form if result == "W")
                away_scores = sum(1 for result in match.away_form if result == "W")
                if home_scores > 2 and away_scores > 2:
                    reasons.append("Les deux équipes ont montré une bonne capacité offensive récemment.")
        elif market_type == "Over/Under 2.5":
            reasons.append("Les statistiques de buts récentes suggèrent un match avec plusieurs buts.")
        
        # Joindre les raisons avec des séparateurs
        return " ".join(reasons)

# Fonction d'utilité pour obtenir des recommandations
def get_market_recommendations(user_id="default_user", match_id=None, sport=None, league=None):
    """
    Récupère les recommandations de marchés de paris pour un utilisateur.
    
    Args:
        user_id (str): Identifiant de l'utilisateur
        match_id (int, optional): ID du match pour filtrer les recommandations
        sport (str, optional): Sport pour filtrer les recommandations
        league (str, optional): Ligue pour filtrer les recommandations
        
    Returns:
        list: Liste des recommandations de marchés
    """
    # Vérifier s'il existe déjà des recommandations récentes
    existing_recommendations = db.get_market_recommendations(user_id, sport, league)
    
    # Si aucune recommandation récente, en générer de nouvelles
    if not existing_recommendations:
        recommender = BettingMarketRecommender(user_id)
        recommender.generate_recommendations(match_id, sport, league)
        
        # Récupérer les recommandations fraîchement générées
        existing_recommendations = db.get_market_recommendations(user_id, sport, league)
    
    return existing_recommendations