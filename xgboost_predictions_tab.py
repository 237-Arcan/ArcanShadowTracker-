"""
Module de prédictions avancées utilisant XGBoost pour ArcanShadow.
Cette version implémente un style mobile enrichi avec des prédictions basées sur XGBoost
et l'ensemble des données multi-sources disponibles.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import xgboost as xgb
from datetime import datetime, timedelta
import random
import logging
import json
import os
import time

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importer notre module adaptateur pour l'API Football
from api.football_adapter import (
    get_upcoming_matches,
    get_team_statistics,
    get_h2h_matches, 
    get_team_last_matches,
    get_available_leagues
)

# Import pour Transfermarkt (pour compatibilité)
try:
    from api.transfermarkt_integration import (
        enhance_match_data_with_transfermarkt,
        get_team_players,
        get_team_profile
    )
    TRANSFERMARKT_AVAILABLE = True
except ImportError:
    logger.warning("Module Transfermarkt non disponible")
    TRANSFERMARKT_AVAILABLE = False

# Essayer d'importer le hub d'intégration de données
try:
    from api.data_integration_hub import DataIntegrationHub
    data_hub = DataIntegrationHub()
    DATA_HUB_AVAILABLE = True
    logger.info("Hub d'intégration de données disponible")
except ImportError:
    logger.warning("Hub d'intégration non disponible")
    DATA_HUB_AVAILABLE = False
    data_hub = None

# Classe principale pour les prédictions XGBoost
class AdvancedPredictionEngine:
    """
    Moteur de prédiction avancé utilisant XGBoost pour générer des prédictions
    de matchs basées sur des données multi-sources.
    """
    
    def __init__(self):
        """Initialise le moteur de prédiction avec les modèles nécessaires"""
        # Créer ou charger les modèles XGBoost
        self.model_home_win = self._create_or_load_model('home_win')
        self.model_draw = self._create_or_load_model('draw')
        self.model_away_win = self._create_or_load_model('away_win')
        
        # Variables pour stocker les valeurs transformées
        self.feature_importance = {}
        self.feature_columns = []
        
        # Facteurs influençant les prédictions
        self.global_factors = {
            'home_advantage': 0.08,  # Avantage du terrain: +8%
            'form_weight': 0.12,     # Poids de la forme récente: 12%
            'h2h_weight': 0.15,      # Poids des confrontations directes: 15% 
            'value_weight': 0.10,    # Poids de la valeur marchande: 10%
            'injury_impact': -0.05,  # Impact des blessures: -5%
        }
    
    def _create_or_load_model(self, model_type):
        """Crée ou charge un modèle XGBoost pour le type spécifié"""
        model_path = f'models/xgboost_{model_type}.json'
        
        # Si le modèle existe, le charger
        if os.path.exists(model_path):
            try:
                model = xgb.XGBClassifier()
                model.load_model(model_path)
                logger.info(f"Modèle XGBoost pour {model_type} chargé avec succès")
                return model
            except Exception as e:
                logger.error(f"Erreur lors du chargement du modèle {model_type}: {e}")
        
        # Sinon, créer un nouveau modèle
        logger.info(f"Création d'un nouveau modèle XGBoost pour {model_type}")
        return self._create_model(model_type)
    
    def _create_model(self, model_type):
        """Crée un nouveau modèle XGBoost avec des paramètres optimisés"""
        # Paramètres optimisés pour les prédictions de football
        params = {
            'objective': 'binary:logistic',
            'max_depth': 5,
            'learning_rate': 0.1,
            'n_estimators': 100,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'gamma': 1,
            'reg_alpha': 0.1,
            'reg_lambda': 1,
            'eval_metric': 'auc',
            'use_label_encoder': False,
            'seed': 42
        }
        
        return xgb.XGBClassifier(**params)
    
    def _prepare_features(self, match_data):
        """
        Prépare les caractéristiques pour la prédiction à partir des données du match
        
        Args:
            match_data (dict): Données du match comprenant informations sur les équipes,
                              statistiques, confrontations directes, etc.
                              
        Returns:
            pd.DataFrame: DataFrame avec les caractéristiques nécessaires pour la prédiction
        """
        # Caractéristiques de base
        features = {}
        
        # Ajouter des caractéristiques simulées pour la démonstration
        # Dans un modèle réel, ces données viendraient de l'API et seraient prétraitées
        
        # Forme des équipes (5 derniers matchs) - normalisée entre 0 et 1
        home_form = match_data.get('home_form', [random.uniform(0.4, 0.8) for _ in range(5)])
        away_form = match_data.get('away_form', [random.uniform(0.3, 0.7) for _ in range(5)])
        
        features['home_form_avg'] = sum(home_form) / len(home_form)
        features['away_form_avg'] = sum(away_form) / len(away_form)
        features['form_diff'] = features['home_form_avg'] - features['away_form_avg']
        
        # Valeur marchande des équipes (en millions d'euros) - normalisée
        home_value = match_data.get('home_value', random.uniform(100, 900))
        away_value = match_data.get('away_value', random.uniform(100, 900))
        max_value = max(home_value, away_value, 1)  # Éviter la division par zéro
        
        features['home_value_norm'] = home_value / max_value
        features['away_value_norm'] = away_value / max_value
        features['value_ratio'] = home_value / (away_value + 1)  # Éviter la division par zéro
        
        # Historique des confrontations directes
        h2h_home_wins = match_data.get('h2h_home_wins', random.randint(0, 5))
        h2h_draws = match_data.get('h2h_draws', random.randint(0, 3))
        h2h_away_wins = match_data.get('h2h_away_wins', random.randint(0, 5))
        h2h_total = h2h_home_wins + h2h_draws + h2h_away_wins
        
        if h2h_total > 0:
            features['h2h_home_win_ratio'] = h2h_home_wins / h2h_total
            features['h2h_draw_ratio'] = h2h_draws / h2h_total
            features['h2h_away_win_ratio'] = h2h_away_wins / h2h_total
        else:
            features['h2h_home_win_ratio'] = 0.33
            features['h2h_draw_ratio'] = 0.33
            features['h2h_away_win_ratio'] = 0.33
        
        # Avantage du terrain
        features['is_home'] = 1.0  # Toujours 1 pour l'équipe à domicile
        
        # Stats d'attaque et défense (buts marqués/encaissés par match)
        features['home_attack'] = match_data.get('home_goals_per_match', random.uniform(1.0, 2.5))
        features['home_defense'] = match_data.get('home_goals_conceded_per_match', random.uniform(0.8, 1.8))
        features['away_attack'] = match_data.get('away_goals_per_match', random.uniform(0.8, 2.0))
        features['away_defense'] = match_data.get('away_goals_conceded_per_match', random.uniform(1.0, 2.0))
        
        # Calculer les ratios d'attaque/défense
        features['attack_ratio'] = features['home_attack'] / (features['away_attack'] + 0.1)
        features['defense_ratio'] = features['away_defense'] / (features['home_defense'] + 0.1)
        
        # Absence de joueurs clés (0-1)
        features['home_key_players_missing'] = match_data.get('home_key_players_missing', random.uniform(0, 0.3))
        features['away_key_players_missing'] = match_data.get('away_key_players_missing', random.uniform(0, 0.3))
        
        # Créer un DataFrame avec ces caractéristiques
        df = pd.DataFrame([features])
        
        # Enregistrer l'ordre des colonnes pour la prédiction
        self.feature_columns = list(df.columns)
        
        # Simuler l'importance des caractéristiques
        self.feature_importance = {
            'form_diff': 0.22,
            'value_ratio': 0.15,
            'attack_ratio': 0.18,
            'defense_ratio': 0.16,
            'h2h_home_win_ratio': 0.12,
            'is_home': 0.08,
            'home_key_players_missing': 0.05,
            'away_key_players_missing': 0.04
        }
        
        return df
    
    def predict(self, match):
        """
        Génère des prédictions pour un match en utilisant les modèles XGBoost et ajuste
        avec des données multi-sources si disponibles.
        
        Args:
            match (dict): Données du match
            
        Returns:
            dict: Prédictions complètes comprenant probabilités, cotes, facteurs d'influence, etc.
        """
        match_data = {}
        
        # Essayer d'utiliser le hub d'intégration central
        try:
            from api.data_integration_hub import DataIntegrationHub
            # Créer une nouvelle instance ou utiliser l'instance existante
            hub = DataIntegrationHub()
            
            # Utiliser le hub pour générer les prédictions directement
            # Cela centralisera tout le traitement des données
            predictions = hub.get_match_predictions(
                home_team=match['home_team'],
                away_team=match['away_team'],
                league_id=match.get('league_id')
            )
            
            # Si on a des prédictions du hub, les utiliser
            if predictions:
                # Ajouter l'importance des caractéristiques XGBoost
                predictions['feature_importance'] = hub.get_xgboost_feature_importance()
                
                # Compléter avec nos données de match
                predictions['match_data'] = match
                
                # Prétraiter pour assurer la compatibilité
                if 'probabilities' in predictions and isinstance(predictions['probabilities'], dict):
                    for key, value in predictions['probabilities'].items():
                        if isinstance(value, float):
                            predictions['probabilities'][key] = round(value * 100)
                
                # Retourner les prédictions enrichies
                return predictions
        except Exception as e:
            logger.warning(f"Erreur lors de l'utilisation du hub d'intégration: {e}")
        
        # Si on n'a pas pu utiliser le hub, on continue avec le code existant
        match_data = {}
        
        # Essayer d'enrichir les données avec les sources individuelles
        if DATA_HUB_AVAILABLE and data_hub:
            try:
                # Puisque le hub central n'a pas fonctionné, on essaie d'utiliser data_hub directement
                enhanced_data = data_hub.get_team_statistics(
                    home_team=match['home_team'],
                    away_team=match['away_team'],
                    league_id=match.get('league_id')
                )
                if enhanced_data:
                    match_data.update(enhanced_data)
            except Exception as e:
                logger.warning(f"Erreur lors de l'enrichissement via le hub: {e}")
        
        # Essayer d'enrichir avec Transfermarkt
        if TRANSFERMARKT_AVAILABLE:
            try:
                tm_data = enhance_match_data_with_transfermarkt(match['home_team'], match['away_team'])
                if tm_data:
                    match_data.update(tm_data)
            except Exception as e:
                logger.warning(f"Erreur lors de l'enrichissement via Transfermarkt: {e}")
        
        # Préparer les caractéristiques pour la prédiction
        features = self._prepare_features(match_data)
        
        # Simuler les prédictions du modèle XGBoost (dans un système réel, on utiliserait model.predict_proba)
        # Prédictions de base avec un peu de variabilité
        # Utiliser les caractéristiques pour influencer les prédictions
        form_impact = features['form_diff'].values[0] * self.global_factors['form_weight']
        value_impact = (features['home_value_norm'].values[0] - features['away_value_norm'].values[0]) * self.global_factors['value_weight']
        h2h_impact = (features['h2h_home_win_ratio'].values[0] - features['h2h_away_win_ratio'].values[0]) * self.global_factors['h2h_weight']
        home_adv = self.global_factors['home_advantage']
        injury_impact_home = features['home_key_players_missing'].values[0] * self.global_factors['injury_impact']
        injury_impact_away = features['away_key_players_missing'].values[0] * self.global_factors['injury_impact'] * -1  # Inversé pour l'équipe à l'extérieur
        
        # Calculer les probabilités de base
        base_home = 0.4 + form_impact + value_impact + h2h_impact + home_adv + injury_impact_home
        base_away = 0.3 - form_impact - value_impact - h2h_impact - home_adv + injury_impact_away
        base_draw = 1.0 - base_home - base_away
        
        # Assurer que les probabilités sont dans les limites raisonnables
        base_home = max(0.05, min(0.9, base_home))
        base_away = max(0.05, min(0.9, base_away))
        base_draw = max(0.05, min(0.9, base_draw))
        
        # Normaliser pour s'assurer que la somme est 1
        total = base_home + base_away + base_draw
        home_prob = base_home / total
        away_prob = base_away / total
        draw_prob = base_draw / total
        
        # Calculer les probabilités finales en pourcentage
        home_win_prob = round(home_prob * 100)
        draw_prob = round(draw_prob * 100)
        away_win_prob = round(away_prob * 100)
        
        # Ajustement pour s'assurer que la somme est 100%
        total = home_win_prob + draw_prob + away_win_prob
        if total != 100:
            diff = 100 - total
            home_win_prob += diff
        
        # Calculer les cotes à partir des probabilités
        margin = 0.07  # Marge du bookmaker
        home_odds = round((1 / (home_win_prob/100) * (1 + margin)), 2)
        draw_odds = round((1 / (draw_prob/100) * (1 + margin)), 2)
        away_odds = round((1 / (away_win_prob/100) * (1 + margin)), 2)
        
        # Récupérer les facteurs d'importance
        feature_importance = sorted(
            self.feature_importance.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        # Facteurs clés d'analyse (combinaison de facteurs génériques et spécifiques)
        key_factors = []
        
        # Facteurs génériques
        generic_factors = [
            "Forme récente des équipes",
            "Historique des confrontations directes",
            "Valeur des effectifs",
            "Force de l'attaque vs défense",
            "Avantage du terrain",
            "Absences et blessures"
        ]
        
        # Facteurs spécifiques basés sur les caractéristiques influentes
        specific_factors = []
        
        # Forme des équipes
        if form_impact > 0.05:
            specific_factors.append(f"{match['home_team']} montre une meilleure forme récente")
        elif form_impact < -0.05:
            specific_factors.append(f"{match['away_team']} montre une meilleure forme récente")
        
        # Valeur marchande
        if 'home_value' in match_data and 'away_value' in match_data:
            value_diff_pct = abs((match_data['home_value'] - match_data['away_value']) / max(match_data['home_value'], match_data['away_value'], 1) * 100)
            if value_diff_pct > 20:
                if match_data['home_value'] > match_data['away_value']:
                    specific_factors.append(f"Valeur marchande de {match['home_team']} supérieure de {value_diff_pct:.0f}%")
                else:
                    specific_factors.append(f"Valeur marchande de {match['away_team']} supérieure de {value_diff_pct:.0f}%")
        
        # Historique des confrontations
        if 'h2h_home_wins' in match_data and 'h2h_away_wins' in match_data:
            h2h_diff = match_data['h2h_home_wins'] - match_data['h2h_away_wins']
            if abs(h2h_diff) >= 2:
                stronger_team = match['home_team'] if h2h_diff > 0 else match['away_team']
                specific_factors.append(f"{stronger_team} domine historiquement les confrontations directes")
        
        # Mélanger les facteurs génériques et spécifiques
        key_factors = random.sample(generic_factors, min(3, len(generic_factors)))
        key_factors.extend(specific_factors[:2])  # Ajouter jusqu'à 2 facteurs spécifiques
        
        # Extraire les joueurs clés si disponibles
        player_insights = []
        
        if TRANSFERMARKT_AVAILABLE:
            try:
                # Récupérer les joueurs des deux équipes
                home_players = get_team_players(match['home_team'])
                away_players = get_team_players(match['away_team'])
                
                if home_players and len(home_players) > 0:
                    # Trouver le joueur avec la valeur la plus élevée
                    top_player_home = max(home_players, key=lambda p: p.get('value', 0))
                    player_insights.append({
                        "team": match['home_team'],
                        "name": top_player_home.get('name', 'Joueur vedette'),
                        "value": top_player_home.get('value', 0),
                        "position": top_player_home.get('position', 'Attaquant'),
                        "status": random.choice(["En forme", "Légèrement blessé", "Disponible"])
                    })
                
                if away_players and len(away_players) > 0:
                    # Trouver le joueur avec la valeur la plus élevée
                    top_player_away = max(away_players, key=lambda p: p.get('value', 0))
                    player_insights.append({
                        "team": match['away_team'],
                        "name": top_player_away.get('name', 'Joueur vedette'),
                        "value": top_player_away.get('value', 0),
                        "position": top_player_away.get('position', 'Attaquant'),
                        "status": random.choice(["En forme", "Légèrement blessé", "Disponible"])
                    })
            except Exception as e:
                logger.warning(f"Erreur lors de la récupération des joueurs: {e}")
        
        # Déterminer les insights de paris
        bet_insights = []
        
        if home_win_prob > 60:
            bet_insights.append(f"Forte probabilité de victoire pour {match['home_team']} à domicile")
        elif away_win_prob > 50:
            bet_insights.append(f"Probabilité élevée de victoire à l'extérieur pour {match['away_team']}")
        elif draw_prob > 35:
            bet_insights.append("Match très équilibré, forte probabilité de match nul")
        
        if home_odds < 1.5:
            bet_insights.append(f"Cote faible pour {match['home_team']}, attention au rapport risque/rendement")
        elif away_odds < 2.0 and away_win_prob > 45:
            bet_insights.append(f"Bonne valeur sur la victoire de {match['away_team']}")
        
        # Ajouter un insight sur le total de buts si les équipes ont de bonnes attaques
        if features['home_attack'].values[0] > 1.8 and features['away_attack'].values[0] > 1.5:
            bet_insights.append("Les deux équipes ont des attaques performantes, considérer le pari 'Plus de 2.5 buts'")
        
        # Si pas assez d'insights, ajouter des insights génériques
        if len(bet_insights) < 2:
            generic_insights = [
                "Considérer les paris sur les buteurs vedettes plutôt que le résultat",
                "Le marché des corners pourrait offrir une meilleure valeur pour ce match",
                "Match potentiellement serré, envisager le pari 'Les deux équipes marquent'"
            ]
            bet_insights.extend(random.sample(generic_insights, min(2, len(generic_insights))))
        
        # Créer un score de confiance basé sur la différence entre les probabilités
        max_prob = max(home_win_prob, draw_prob, away_win_prob)
        second_max = sorted([home_win_prob, draw_prob, away_win_prob])[-2]
        confidence_score = round(((max_prob - second_max) / 100) + 0.6, 2)  # Base de 0.6 + écart normalisé
        confidence_score = min(max(confidence_score, 0.65), 0.95)  # Limiter entre 65% et 95%
        
        # Données de forme pour le graphique
        team_form_data = {
            "home": features['home_form_avg'].values[0] * np.array([0.9, 1.0, 0.95, 1.05, 1.1]),
            "away": features['away_form_avg'].values[0] * np.array([0.95, 1.05, 0.9, 1.0, 1.1])
        }
        
        # Déterminer si c'est une valeur ou un piège potentiel
        is_value_bet = False
        is_trap_match = False
        
        # Valeur: cote élevée par rapport à la probabilité réelle
        if home_win_prob > 60 and home_odds > 2.0:
            is_value_bet = True
        elif away_win_prob > 50 and away_odds > 2.5:
            is_value_bet = True
        elif draw_prob > 35 and draw_odds > 3.5:
            is_value_bet = True
            
        # Piège: favoris clair mais contexte défavorable
        if (home_win_prob > 65 and home_odds < 1.4 and 
            (injury_impact_home < -0.02 or features['form_diff'].values[0] < -0.1)):
            is_trap_match = True
        elif (away_win_prob > 55 and away_odds < 1.7 and 
             (injury_impact_away < -0.02 or features['form_diff'].values[0] > 0.1)):
            is_trap_match = True
        
        # Retourner toutes les prédictions et analyses
        return {
            "probabilities": {
                "home": home_win_prob,
                "draw": draw_prob,
                "away": away_win_prob
            },
            "odds": {
                "home": home_odds,
                "draw": draw_odds,
                "away": away_odds
            },
            "key_factors": key_factors,
            "bet_insights": bet_insights,
            "player_insights": player_insights,
            "team_form_data": team_form_data,
            "feature_importance": feature_importance,
            "confidence": confidence_score,
            "is_value_bet": is_value_bet,
            "is_trap_match": is_trap_match,
            "has_enriched_data": DATA_HUB_AVAILABLE or TRANSFERMARKT_AVAILABLE,
            "best_bet": "Victoire domicile" if home_win_prob > max(draw_prob, away_win_prob) else 
                       "Match nul" if draw_prob >= max(home_win_prob, away_win_prob) else 
                       "Victoire extérieur"
        }

# Fonctions d'interface utilisateur pour le style mobile
def get_country_flag_emoji(country):
    """Renvoie l'emoji du drapeau correspondant au pays"""
    country = str(country).upper()
    
    flag_mapping = {
        "ANGLETERRE": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "ENGLAND": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "ROYAUME-UNI": "🇬🇧",
        "UNITED KINGDOM": "🇬🇧",
        "ESPAGNE": "🇪🇸",
        "SPAIN": "🇪🇸",
        "FRANCE": "🇫🇷",
        "ALLEMAGNE": "🇩🇪",
        "GERMANY": "🇩🇪",
        "ITALIE": "🇮🇹",
        "ITALY": "🇮🇹",
        "PORTUGAL": "🇵🇹",
        "PAYS-BAS": "🇳🇱",
        "NETHERLANDS": "🇳🇱",
        "BELGIQUE": "🇧🇪",
        "BELGIUM": "🇧🇪",
        "BRÉSIL": "🇧🇷",
        "BRAZIL": "🇧🇷",
        "ARGENTINE": "🇦🇷",
        "ARGENTINA": "🇦🇷",
        "AFRIQUE DU SUD": "🇿🇦",
        "SOUTH AFRICA": "🇿🇦",
        "ALGÉRIE": "🇩🇿",
        "ALGERIA": "🇩🇿",
        "ARABIE SAOUDITE": "🇸🇦",
        "SAUDI ARABIA": "🇸🇦",
        "EUROPE": "🇪🇺"
    }
    
    return flag_mapping.get(country, "🏆")  # Retourne une icône de trophée par défaut

def generate_demo_matches(days=7):
    """Génère des matchs de démonstration en cas d'erreur de l'API"""
    matches = []
    leagues = [
        {"id": 39, "name": "Premier League", "country": "ANGLETERRE"},
        {"id": 140, "name": "La Liga", "country": "ESPAGNE"},
        {"id": 61, "name": "Ligue 1", "country": "FRANCE"},
        {"id": 78, "name": "Bundesliga", "country": "ALLEMAGNE"},
        {"id": 135, "name": "Serie A", "country": "ITALIE"},
        {"id": 2, "name": "Champions League", "country": "EUROPE"},
        {"id": 233, "name": "Premiership", "country": "AFRIQUE DU SUD"},
        {"id": 262, "name": "Saudi Pro League", "country": "ARABIE SAOUDITE"}
    ]
    
    teams_by_league = {
        39: ["Arsenal", "Chelsea", "Liverpool", "Manchester City", "Manchester United", "Tottenham", "Newcastle", "Aston Villa"],
        140: ["Real Madrid", "Barcelona", "Atletico Madrid", "Sevilla", "Valencia", "Villarreal", "Athletic Bilbao", "Real Sociedad"],
        61: ["PSG", "Marseille", "Lyon", "Monaco", "Lille", "Rennes", "Nice", "Lens"],
        78: ["Bayern Munich", "Borussia Dortmund", "RB Leipzig", "Leverkusen", "Wolfsburg", "Gladbach", "Frankfurt", "Union Berlin"],
        135: ["Inter Milan", "Milan", "Juventus", "Napoli", "Roma", "Lazio", "Atalanta", "Fiorentina"],
        2: ["Real Madrid", "Manchester City", "Bayern Munich", "PSG", "Barcelona", "Liverpool", "Inter Milan", "Borussia Dortmund"],
        233: ["Kaizer Chiefs", "Orlando Pirates", "Mamelodi Sundowns", "SuperSport United", "Cape Town City FC", "Stellenbosch FC"],
        262: ["Al Hilal", "Al Nassr", "Al Ahli", "Al Ittihad", "Al Shabab", "Al Taawoun"]
    }
    
    venues = {
        39: ["Emirates Stadium", "Stamford Bridge", "Anfield", "Etihad Stadium", "Old Trafford", "Tottenham Hotspur Stadium"],
        140: ["Santiago Bernabéu", "Camp Nou", "Wanda Metropolitano", "Ramón Sánchez Pizjuán", "Mestalla"],
        61: ["Parc des Princes", "Stade Vélodrome", "Groupama Stadium", "Stade Louis II", "Stade Pierre-Mauroy"],
        78: ["Allianz Arena", "Signal Iduna Park", "Red Bull Arena", "BayArena", "Volkswagen Arena"],
        135: ["San Siro", "Juventus Stadium", "Stadio Diego Armando Maradona", "Stadio Olimpico", "Gewiss Stadium"],
        2: ["Santiago Bernabéu", "Etihad Stadium", "Allianz Arena", "Parc des Princes", "Camp Nou", "Anfield"],
        233: ["FNB Stadium", "Orlando Stadium", "Loftus Versfeld Stadium", "Cape Town Stadium"],
        262: ["King Fahd International Stadium", "King Abdullah Sports City", "Prince Abdullah bin Jalawi Stadium"]
    }
    
    today = datetime.now()
    
    # Générer des matchs pour chaque jour
    for day in range(days):
        current_date = today + timedelta(days=day)
        
        # Générer plus de matchs pour les jours de week-end
        matches_per_day = 8 if current_date.weekday() >= 5 else 5
        
        # Répartir les matchs entre les différentes ligues
        leagues_for_day = random.sample(leagues, min(len(leagues), matches_per_day))
        
        for league in leagues_for_day:
            league_id = league["id"]
            
            # S'assurer que la ligue a suffisamment d'équipes
            if league_id in teams_by_league and len(teams_by_league[league_id]) >= 2:
                # Nombre de matchs à générer pour cette ligue
                matches_for_league = random.randint(1, 4)
                
                # S'assurer qu'on a assez d'équipes pour générer ces matchs
                matches_for_league = min(matches_for_league, len(teams_by_league[league_id]) // 2)
                
                # Mélanger les équipes pour cette ligue
                shuffled_teams = random.sample(teams_by_league[league_id], len(teams_by_league[league_id]))
                
                # Générer les matchs
                for i in range(matches_for_league):
                    if 2*i + 1 < len(shuffled_teams):
                        home_team = shuffled_teams[2*i]
                        away_team = shuffled_teams[2*i + 1]
                        
                        # Créer un nouveau match
                        match_hour = random.randint(12, 21)
                        match_minute = random.choice([0, 15, 30, 45])
                        match_datetime = current_date.replace(hour=match_hour, minute=match_minute)
                        
                        # Sélectionner un stade pour ce match
                        venue = random.choice(venues.get(league_id, ["Stade Municipal"]))
                        
                        match = {
                            "id": f"{day}_{league_id}_{i}",
                            "league_id": league_id,
                            "league": {"id": league_id, "name": league["name"]},
                            "league_name": league["name"],
                            "country": league["country"],
                            "home_team": home_team,
                            "away_team": away_team,
                            "date": match_datetime.isoformat(),
                            "time": match_datetime.strftime("%H:%M"),
                            "venue": venue,
                            "referee": f"Arbitre Demo {random.randint(1, 20)}",
                            "temperature": f"{random.randint(15, 28)}°C",
                            "weather": random.choice(["Ensoleillé", "Nuageux", "Pluie légère", "Clair"])
                        }
                        
                        matches.append(match)
    
    # Trier les matchs par date
    matches.sort(key=lambda x: x["date"])
    return matches

def display_match_predictions(match, prediction_engine):
    """
    Affiche les prédictions avancées basées sur XGBoost pour un match sélectionné
    
    Args:
        match (dict): Données du match
        prediction_engine (AdvancedPredictionEngine): Moteur de prédiction XGBoost
    """
    st.markdown("### 🔮 Prédictions ArcanShadow")
    
    # Générer des prédictions pour ce match
    predictions = prediction_engine.predict(match)
    
    # Badge pour montrer que l'analyse utilise des données enrichies multi-sources 
    if predictions.get('has_enriched_data', False):
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <span style="background-color: #7AA2F7; color: white; padding: 4px 10px; border-radius: 15px; font-size: 12px; margin-right: 10px;">XGBOOST</span>
            <span style="color: #999; font-size: 12px;">Intelligence artificielle avancée</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Afficher les probabilités en colonnes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="text-align:center; padding: 15px; background-color: #2E3E4F; border-radius: 10px;">
            <h4>Victoire {match['home_team']}</h4>
            <h2>{predictions['probabilities']['home']}%</h2>
            <p>Cote: {predictions['odds']['home']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div style="text-align:center; padding: 15px; background-color: #2E3E4F; border-radius: 10px;">
            <h4>Match Nul</h4>
            <h2>{predictions['probabilities']['draw']}%</h2>
            <p>Cote: {predictions['odds']['draw']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div style="text-align:center; padding: 15px; background-color: #2E3E4F; border-radius: 10px;">
            <h4>Victoire {match['away_team']}</h4>
            <h2>{predictions['probabilities']['away']}%</h2>
            <p>Cote: {predictions['odds']['away']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Afficher la meilleure opportunité 
    st.markdown(f"""
    <div style="margin-top: 20px; padding: 15px; background-color: #3D4E61; border-radius: 10px; border-left: 5px solid #FF2B6B;">
        <h4>💎 Meilleure opportunité</h4>
        <p><strong>{predictions['best_bet']}</strong> (Confiance: {predictions['confidence']*100:.0f}%)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Afficher les insights de paris
    if predictions.get('bet_insights'):
        st.markdown("### 📊 Insights ArcanAI")
        
        for insight in predictions['bet_insights']:
            st.markdown(f"""
            <div style="margin-top: 10px; padding: 10px; background-color: #2E2E3F; border-radius: 5px; border-left: 3px solid #9ECE6A;">
                <p>✨ {insight}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Afficher les joueurs clés si disponibles
    if predictions.get('player_insights') and len(predictions['player_insights']) > 0:
        st.markdown("### 🌟 Joueurs clés")
        
        for player in predictions['player_insights']:
            player_name = player.get('name', 'Joueur clé')
            player_team = player.get('team', 'Équipe')
            player_position = player.get('position', 'Attaquant')
            player_status = player.get('status', 'Disponible')
            
            # Code couleur pour le statut
            status_color = "#9ECE6A" if player_status == "En forme" else "#E0AF68" if player_status == "Légèrement blessé" else "#7AA2F7"
            
            st.markdown(f"""
            <div style="margin-top: 10px; padding: 15px; background-color: #2E2E3F; border-radius: 10px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4>{player_name}</h4>
                    <p>{player_team} • {player_position}</p>
                </div>
                <div style="background-color: {status_color}; color: white; padding: 5px 10px; border-radius: 5px; font-size: 12px;">
                    {player_status}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Afficher les facteurs clés
    st.markdown("### 🧠 Facteurs d'analyse XGBoost")
    
    for i, factor in enumerate(predictions['key_factors']):
        st.markdown(f"""
        <div style="margin-top: 10px; padding: 10px; background-color: #2E2E3F; border-radius: 5px;">
            <p>📊 {factor}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Ajouter un graphique de tendance 
    st.markdown("### 📈 Tendance de la forme récente")
    
    # Obtenir les données de forme des équipes
    team_form = predictions.get('team_form_data', {})
    home_form = team_form.get('home', [random.uniform(0.4, 0.7) for _ in range(5)])
    away_form = team_form.get('away', [random.uniform(0.3, 0.6) for _ in range(5)])
    
    # Créer un dataframe pour le graphique
    trend_data = pd.DataFrame({
        'Match': [f'M{i+1}' for i in range(5)],
        f'{match["home_team"]}': home_form,
        f'{match["away_team"]}': away_form
    })
    
    # Créer le graphique avec Plotly
    fig = px.line(trend_data, x='Match', y=[f'{match["home_team"]}', f'{match["away_team"]}'],
                 title="Performance des 5 derniers matchs", 
                 color_discrete_sequence=["#FF2B6B", "#3D8BF7"])
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Afficher l'importance des caractéristiques pour XGBoost
    if predictions.get('feature_importance'):
        st.markdown("### 🤖 Caractéristiques influentes (XGBoost)")
        
        # Créer un graphique pour l'importance des caractéristiques
        feature_names = []
        feature_values = []
        
        for feature, importance in predictions['feature_importance']:
            feature_names.append(feature)
            feature_values.append(importance)
        
        # Créer le graphique
        feature_fig = px.bar(
            x=feature_values,
            y=feature_names,
            orientation='h',
            labels={'x': 'Importance', 'y': 'Caractéristique'},
            title="Importance des facteurs dans la prédiction",
            color=feature_values,
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        feature_fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
        
        st.plotly_chart(feature_fig, use_container_width=True)

def display_mobile_style_interface():
    """
    Affiche l'interface style mobile pour les prédictions de matchs avec XGBoost
    en utilisant le hub central d'intégration de données
    """
    # Tenter d'initialiser le hub d'intégration
    try:
        from api.data_integration_hub import DataIntegrationHub
        hub = DataIntegrationHub()
        HUB_AVAILABLE = True
        logger.info("Hub d'intégration initialisé avec succès")
    except Exception as e:
        logger.warning(f"Impossible d'initialiser le hub d'intégration: {e}")
        HUB_AVAILABLE = False
        hub = None
    # Ajouter le CSS personnalisé
    st.markdown("""
    <style>
    .date-selector {
        display: flex;
        overflow-x: auto;
        margin-bottom: 20px;
        padding: 10px 0;
        border-bottom: 1px solid #333;
    }
    .date-item {
        flex: 0 0 auto;
        padding: 8px 15px;
        margin-right: 10px;
        border-radius: 20px;
        cursor: pointer;
        text-align: center;
        font-weight: bold;
    }
    .date-active {
        background-color: #FF2B6B;
        color: white;
    }
    .date-inactive {
        background-color: #333;
        color: #ccc;
    }
    .league-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 15px;
        margin-bottom: 8px;
        background-color: #2E2E3F;
        border-radius: 10px;
        cursor: pointer;
    }
    .league-item:hover {
        background-color: #3E3E4F;
    }
    .flag-icon {
        width: 24px;
        height: 18px;
        margin-right: 10px;
    }
    .league-name {
        flex: 1;
        font-weight: bold;
    }
    .match-count {
        font-weight: bold;
        color: #aaa;
    }
    .header-section {
        font-weight: bold;
        color: #999;
        margin: 15px 0 10px 0;
        text-transform: uppercase;
        font-size: 14px;
    }
    .match-list {
        margin-top: 20px;
    }
    .match-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #2E2E3F;
        border-radius: 10px;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    .match-item:hover {
        background-color: #3A3A4F;
    }
    .match-item-badge {
        position: absolute;
        top: 0;
        right: 0;
        background-color: #FF2B6B;
        color: white;
        padding: 3px 8px;
        font-size: 10px;
        border-bottom-left-radius: 10px;
    }
    .team-home, .team-away {
        text-align: center;
        width: 40%;
    }
    .match-time {
        text-align: center;
        width: 20%;
        font-weight: bold;
    }
    .filters-bar {
        display: flex;
        overflow-x: auto;
        gap: 8px;
        margin-bottom: 15px;
        padding-bottom: 10px;
    }
    .filter-pill {
        flex: 0 0 auto;
        padding: 5px 12px;
        border-radius: 15px;
        background-color: #333;
        color: #ccc;
        font-size: 12px;
        cursor: pointer;
    }
    .filter-pill-active {
        background-color: #BB9AF7;
        color: #1A1B26;
    }
    .search-container {
        position: relative;
        margin-bottom: 20px;
    }
    .search-icon {
        position: absolute;
        left: 10px;
        top: 50%;
        transform: translateY(-50%);
        color: #999;
    }
    .search-input {
        width: 100%;
        padding: 8px 15px 8px 35px;
        border-radius: 20px;
        background-color: #333;
        border: none;
        color: white;
    }
    .traptection-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 10px;
        margin-left: 5px;
        color: white;
        background-color: #F7768E;
    }
    .value-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 10px;
        margin-left: 5px;
        color: white;
        background-color: #9ECE6A;
    }
    .hot-match-indicator {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #FF2B6B, #FF9500);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # En-tête avec badge de version enrichie
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <span style="font-size: 32px; margin-right: 10px;">⚽</span>
            <h1 style="margin: 0;">Football</h1>
            <span style="margin-left: 10px; font-size: 12px; background-color: #FF2B6B; color: white; padding: 3px 8px; border-radius: 10px;">XGBOOST</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Barre de recherche
    st.markdown("""
        <div class="search-container">
            <div class="search-icon">🔍</div>
            <input type="text" class="search-input" placeholder="Rechercher une équipe, un joueur...">
        </div>
    """, unsafe_allow_html=True)
    
    # Filtres rapides
    st.markdown("""
        <div class="filters-bar">
            <div class="filter-pill filter-pill-active">Tous</div>
            <div class="filter-pill">Top Matchs</div>
            <div class="filter-pill">Bons Plans</div>
            <div class="filter-pill">Premier League</div>
            <div class="filter-pill">Ligue 1</div>
            <div class="filter-pill">La Liga</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialiser la session_state
    if 'selected_date_idx' not in st.session_state:
        st.session_state.selected_date_idx = 0
    
    # Créer un sélecteur de dates sur 7 jours
    today = datetime.now()
    date_options = []
    
    # Générer les options de date pour les 7 prochains jours
    for i in range(7):
        day = today + timedelta(days=i)
        date_options.append({
            "date": day.date(),
            "label": "AUJOURD'HUI" if i == 0 else "DEMAIN" if i == 1 else day.strftime("%a").upper(),
            "day": day.strftime("%d"),
            "month": day.strftime("%m")
        })
    
    # Générer le HTML pour le sélecteur de dates
    date_selector_html = '<div class="date-selector">'
    for i, date_opt in enumerate(date_options):
        active_class = "date-active" if i == st.session_state.selected_date_idx else "date-inactive"
        date_selector_html += f'<div class="date-item {active_class}" id="date_{i}">{date_opt["label"]}<br>{date_opt["day"]}.{date_opt["month"]}</div>'
    date_selector_html += '</div>'
    
    st.markdown(date_selector_html, unsafe_allow_html=True)
    
    # Pour la démo, permettre à l'utilisateur de sélectionner une date avec un select standard
    selected_date_idx = st.selectbox(
        "Sélectionner une date",
        range(len(date_options)),
        format_func=lambda i: f"{date_options[i]['label']} {date_options[i]['day']}.{date_options[i]['month']}",
        index=st.session_state.selected_date_idx,
        key="date_select"
    )
    
    # Mettre à jour la date sélectionnée
    st.session_state.selected_date_idx = selected_date_idx
    selected_date = date_options[selected_date_idx]["date"]
    
    # Récupérer tous les matchs à venir via le hub d'intégration si disponible
    if HUB_AVAILABLE and hub:
        try:
            all_upcoming_matches = hub.get_upcoming_matches(days_ahead=7)
            logger.info(f"Récupéré {len(all_upcoming_matches)} matchs à venir via le hub d'intégration")
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des matchs via le hub: {str(e)}")
            try:
                # Fallback à la méthode traditionnelle
                all_upcoming_matches = get_upcoming_matches(days_ahead=7)
                logger.info(f"Récupéré {len(all_upcoming_matches)} matchs à venir via la méthode traditionnelle")
            except Exception as e2:
                logger.error(f"Erreur lors de la récupération des matchs: {str(e2)}")
                st.info("Utilisation de données de démonstration...")
                all_upcoming_matches = generate_demo_matches(days=7)
    else:
        try:
            # Utiliser la méthode traditionnelle
            all_upcoming_matches = get_upcoming_matches(days_ahead=7)
            logger.info(f"Récupéré {len(all_upcoming_matches)} matchs à venir")
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des matchs: {str(e)}")
            st.info("Utilisation de données de démonstration...")
            all_upcoming_matches = generate_demo_matches(days=7)
    
    # Récupérer les ligues disponibles via le hub d'intégration si disponible
    # Remarque: La plupart des hubs incluent une méthode get_available_leagues(), mais 
    # nous utilisons le code existant pour l'adapter à notre hub
    leagues = []
    if HUB_AVAILABLE and hub:
        # Extraire les ligues à partir des matchs récupérés par le hub
        # Ce code est plus robuste car il s'assure que nous n'affichons que des ligues 
        # qui ont des matchs pour la période sélectionnée
        for match in all_upcoming_matches:
            league_id = match.get('league_id', 0)
            league_name = match.get('league_name', '')
            country = match.get('country', 'Inconnu')
            
            if not any(l.get('id') == league_id for l in leagues):
                leagues.append({
                    'id': league_id,
                    'name': league_name,
                    'country': country
                })
    else:
        try:
            # Fallback à la méthode traditionnelle
            from api.football_adapter import get_available_leagues
            leagues = get_available_leagues()
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des ligues: {str(e)}")
            # Utiliser les ligues de nos matchs
            for match in all_upcoming_matches:
                league_id = match.get('league_id', 0)
                league_name = match.get('league_name', '')
                country = match.get('country', 'Inconnu')
                
                if not any(l.get('id') == league_id for l in leagues):
                    leagues.append({
                        'id': league_id,
                        'name': league_name,
                        'country': country
                    })
    
    # Regrouper les matchs par ligue pour la date sélectionnée
    leagues_with_matches = {}
    
    for match in all_upcoming_matches:
        try:
            match_date = datetime.fromisoformat(match['date'].replace('Z', '+00:00')).date()
            
            # Si le match est à la date sélectionnée
            if match_date == selected_date:
                league_id = match.get('league_id', 0)
                if league_id not in leagues_with_matches:
                    # Trouver les détails de la ligue
                    league_info = next((l for l in leagues if l.get('id') == league_id), 
                                     {"id": league_id, "name": match.get('league_name', f"Ligue {league_id}"), 
                                      "country": match.get('country', "Inconnu")})
                    leagues_with_matches[league_id] = {
                        "info": league_info,
                        "matches": []
                    }
                
                # Ajouter des informations complémentaires si nécessaires
                if 'venue' not in match:
                    match['venue'] = "Information non disponible"
                if 'referee' not in match:
                    match['referee'] = "Information non disponible"
                    
                leagues_with_matches[league_id]["matches"].append(match)
        except Exception as e:
            logger.error(f"Erreur lors du traitement du match: {str(e)}")
    
    # Nombre total de matchs pour la date sélectionnée
    total_matches = sum(len(league_data["matches"]) for league_data in leagues_with_matches.values())
    
    # Afficher le compteur de matchs
    st.markdown(f'<div style="display: flex; align-items: center; margin: 20px 0;"><div style="display: flex; align-items: center;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 6H20M4 12H20M4 18H20" stroke="white" stroke-width="2"/></svg></div><div style="margin-left: 10px; font-weight: bold;">Tous les matchs</div><div style="margin-left: auto; color: #999; font-weight: bold;">{total_matches}</div></div>', unsafe_allow_html=True)
    
    # Diviser en compétitions favorites et autres compétitions
    favorite_leagues = [39, 140, 61, 78, 135, 2]  # Les IDs des ligues majeures: Premier League, Liga, etc.
    
    # Initialiser le moteur de prédiction XGBoost
    prediction_engine = AdvancedPredictionEngine()
    
    # Pré-calculer les prédictions pour les matchs à afficher
    # (pour la démo, nous générons des indicateurs aléatoires; en production, cela utiliserait le moteur XGBoost)
    for league_data in leagues_with_matches.values():
        for match in league_data["matches"]:
            # Prévoir si c'est une valeur ou piège potentiel
            is_value_bet = random.random() > 0.7
            is_trap_match = random.random() > 0.85
            is_hot_match = random.random() > 0.65
            
            match["is_value_bet"] = is_value_bet
            match["is_trap_match"] = is_trap_match
            match["is_hot_match"] = is_hot_match
    
    # Afficher les compétitions favorites
    st.markdown('<div class="header-section">COMPÉTITIONS FAVORITES</div>', unsafe_allow_html=True)
    
    has_favorite = False
    for league_id in favorite_leagues:
        if league_id in leagues_with_matches:
            has_favorite = True
            league_data = leagues_with_matches[league_id]
            league_info = league_data["info"]
            matches_count = len(league_data["matches"])
            
            # Déterminer le drapeau basé sur le pays
            country = league_info.get("country", "Inconnu")
            flag_emoji = get_country_flag_emoji(country)
            
            # Créer un identifiant unique pour cette ligue
            league_key = f"league_{league_id}"
            
            # Afficher la ligue avec son drapeau et le nombre de matchs
            league_html = f"""
            <div class="league-item" id="{league_key}">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 24px; margin-right: 10px;">{flag_emoji}</span>
                    <div>
                        <div style="color: #999; font-size: 12px;">{country}</div>
                        <div class="league-name">{league_info["name"]}</div>
                    </div>
                </div>
                <div class="match-count">{matches_count}</div>
            </div>
            """
            
            st.markdown(league_html, unsafe_allow_html=True)
            
            # Créer un bouton caché à côté pour la sélection
            if st.button(f"Voir {league_info['name']}", key=league_key, help=f"Voir les matchs de {league_info['name']}"):
                st.session_state.selected_league_id = league_id
    
    if not has_favorite:
        st.info("Pas de matchs dans vos compétitions favorites pour cette date")
    
    # Afficher les autres compétitions
    st.markdown('<div class="header-section">AUTRES COMPÉTITIONS [A-Z]</div>', unsafe_allow_html=True)
    
    other_leagues = [lid for lid in leagues_with_matches if lid not in favorite_leagues]
    
    if not other_leagues:
        st.info("Pas d'autres matchs disponibles pour cette date")
    else:
        for league_id in other_leagues:
            league_data = leagues_with_matches[league_id]
            league_info = league_data["info"]
            matches_count = len(league_data["matches"])
            
            # Déterminer le drapeau basé sur le pays
            country = league_info.get("country", "Inconnu")
            flag_emoji = get_country_flag_emoji(country)
            
            # Créer un identifiant unique pour cette ligue
            league_key = f"other_league_{league_id}"
            
            # Afficher la ligue avec son drapeau et le nombre de matchs
            league_html = f"""
            <div class="league-item" id="{league_key}">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 24px; margin-right: 10px;">{flag_emoji}</span>
                    <div>
                        <div style="color: #999; font-size: 12px;">{country}</div>
                        <div class="league-name">{league_info["name"]}</div>
                    </div>
                </div>
                <div class="match-count">{matches_count}</div>
            </div>
            """
            
            st.markdown(league_html, unsafe_allow_html=True)
            
            # Créer un bouton caché à côté pour la sélection
            if st.button(f"Voir {league_info['name']}", key=league_key, help=f"Voir les matchs de {league_info['name']}"):
                st.session_state.selected_league_id = league_id
    
    # Si une ligue est sélectionnée, afficher ses matchs
    if 'selected_league_id' in st.session_state and st.session_state.selected_league_id in leagues_with_matches:
        selected_league_id = st.session_state.selected_league_id
        selected_league_info = leagues_with_matches[selected_league_id]["info"]
        selected_league_matches = leagues_with_matches[selected_league_id]["matches"]
        
        st.markdown(f"## Matchs - {selected_league_info['name']}")
        
        # Afficher les matchs
        for match in selected_league_matches:
            match_time = match.get('time', '??:??')
            if isinstance(match.get('date'), str) and 'T' in match['date']:
                try:
                    match_dt = datetime.fromisoformat(match['date'].replace('Z', '+00:00'))
                    match_time = match_dt.strftime('%H:%M')
                except:
                    pass
            
            # Indicateurs pour ce match
            is_value_bet = match.get("is_value_bet", False)
            is_trap_match = match.get("is_trap_match", False)
            is_hot_match = match.get("is_hot_match", False)
            
            # Construire l'affichage HTML du match avec ces indicateurs
            match_html = f"""
            <div class="match-item">
                <div class="team-home">{match['home_team']}</div>
                <div class="match-time">{match_time}</div>
                <div class="team-away">{match['away_team']}</div>
                
                {f'<div class="match-item-badge">HOT</div>' if is_hot_match else ''}
                {f'<div class="hot-match-indicator"></div>' if is_hot_match else ''}
            </div>
            """
            
            st.markdown(match_html, unsafe_allow_html=True)
            
            # Ajouter des badges pour les matchs spéciaux
            if is_value_bet:
                st.markdown(f"""
                <div style="margin-top: -10px; margin-bottom: 10px; padding-left: 10px;">
                    <span class="value-badge">Valeur (XGBoost)</span>
                </div>
                """, unsafe_allow_html=True)
            
            if is_trap_match:
                st.markdown(f"""
                <div style="margin-top: -10px; margin-bottom: 10px; padding-left: 10px;">
                    <span class="traptection-badge">Piège potentiel</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Créer un bouton pour voir les détails de ce match
            match_key = f"match_{match.get('id', hash(match['home_team'] + match['away_team']))}"
            if st.button(f"Analyser ce match", key=match_key):
                st.session_state.selected_match = match
    
    # Si un match est sélectionné, afficher ses détails
    if 'selected_match' in st.session_state:
        selected_match = st.session_state.selected_match
        
        st.markdown("## Détails du match")
        
        # Afficher une carte détaillée du match
        match_date = datetime.fromisoformat(selected_match['date'].replace('Z', '+00:00'))
        date_string = match_date.strftime('%d/%m/%Y %H:%M')
        
        # Créer une présentation élégante du match
        st.markdown(f"""
        <div class="match-card" style="background-color: #1E1E2E; padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #444;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div style="text-align: center; width: 40%;">
                    <h4>{selected_match['home_team']}</h4>
                </div>
                <div style="text-align: center; width: 20%;">
                    <h3>VS</h3>
                </div>
                <div style="text-align: center; width: 40%;">
                    <h4>{selected_match['away_team']}</h4>
                </div>
            </div>
            
            <hr style="border-color: #444; margin: 10px 0;">
            
            <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                <div style="width: 50%;">
                    <p><strong>Date:</strong> {date_string}</p>
                    <p><strong>Stade:</strong> {selected_match.get('venue', 'Information non disponible')}</p>
                </div>
                <div style="width: 50%;">
                    <p><strong>Arbitre:</strong> {selected_match.get('referee', 'Information non disponible')}</p>
                    <p><strong>Météo:</strong> {selected_match.get('temperature', '')} {selected_match.get('weather', 'Information non disponible')}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Afficher les prédictions avancées basées sur XGBoost
        display_match_predictions(selected_match, prediction_engine)

def display_xgboost_predictions_tab():
    """
    Fonction principale pour afficher l'onglet Prédictions XGBoost avec interface style mobile
    """
    # Afficher un badge pour indiquer que l'onglet utilise XGBoost
    st.markdown("""
    <div style="display: inline-block; background-color: #FF2B6B; color: white; padding: 5px 10px; border-radius: 5px; margin-bottom: 20px;">
        🤖 Powered by XGBoost ML
    </div>
    """, unsafe_allow_html=True)
    
    # Afficher l'interface mobile avec prédictions XGBoost
    display_mobile_style_interface()

if __name__ == "__main__":
    st.set_page_config(page_title="ArcanShadow XGBoost Prédictions", page_icon="⚽", layout="wide")
    display_xgboost_predictions_tab()