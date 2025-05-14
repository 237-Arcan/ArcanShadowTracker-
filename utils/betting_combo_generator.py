"""
Betting Combo Generator - Module de génération de combinés de paris optimisés
Ce module utilise les données enrichies et les prédictions des modules d'ArcanShadow
pour générer des combinés de paris à forte valeur espérée.
"""

import logging
import random
from datetime import datetime
import pandas as pd
import numpy as np
from .data_enrichment import DataEnrichment

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('betting_combo_generator')

class BettingComboGenerator:
    """
    Générateur de combinés de paris optimisés.
    Utilise les données enrichies et les prédictions des modules d'ArcanShadow.
    """
    def __init__(self):
        """
        Initialise le générateur de combinés.
        """
        self.data_enrichment = DataEnrichment()
        
    def predict_match_outcomes(self, match, arcan_predictions=None):
        """
        Prédit les résultats d'un match en combinant les données enrichies et les prédictions ArcanShadow.
        
        Args:
            match (dict): Données du match
            arcan_predictions (dict, optional): Prédictions des modules ArcanShadow
            
        Returns:
            dict: Prédictions de résultats pour différents marchés
        """
        try:
            # Données de base du match
            home_team = match.get('home_team', '')
            away_team = match.get('away_team', '')
            
            # Récupérer les données enrichies
            home_form = match.get('home_form', [])
            away_form = match.get('away_form', [])
            h2h = match.get('head_to_head', [])
            stats = match.get('stats', {})
            odds = match.get('odds', {})
            
            # 1. Analyse de base (1X2)
            # -----------------------------
            # Calculer la forme récente (% de victoires)
            home_wins = sum(1 for m in home_form if m.get('result') == 'W')
            home_draws = sum(1 for m in home_form if m.get('result') == 'D')
            home_form_rating = home_wins / len(home_form) if home_form else 0.5
            home_draw_rating = home_draws / len(home_form) if home_form else 0.2
            
            away_wins = sum(1 for m in away_form if m.get('result') == 'W')
            away_draws = sum(1 for m in away_form if m.get('result') == 'D')
            away_form_rating = away_wins / len(away_form) if away_form else 0.5
            away_draw_rating = away_draws / len(away_form) if away_form else 0.2
            
            # Analyser les H2H
            h2h_home_wins = 0
            h2h_away_wins = 0
            h2h_draws = 0
            h2h_total_goals = 0
            h2h_matches_count = 0
            
            for h2h_match in h2h:
                try:
                    home_team_h2h = h2h_match.get('home_team')
                    score = h2h_match.get('score', '').split('-')
                    
                    if len(score) == 2:
                        home_score = int(score[0].strip())
                        away_score = int(score[1].strip())
                        h2h_total_goals += home_score + away_score
                        h2h_matches_count += 1
                        
                        if home_score > away_score:
                            if home_team_h2h == home_team:
                                h2h_home_wins += 1
                            else:
                                h2h_away_wins += 1
                        elif home_score < away_score:
                            if home_team_h2h == home_team:
                                h2h_away_wins += 1
                            else:
                                h2h_home_wins += 1
                        else:
                            h2h_draws += 1
                except Exception as e:
                    logger.error(f"Erreur lors de l'analyse d'un match H2H: {e}")
                    continue
            
            h2h_total = h2h_home_wins + h2h_away_wins + h2h_draws
            h2h_home_ratio = h2h_home_wins / h2h_total if h2h_total > 0 else 0.33
            h2h_away_ratio = h2h_away_wins / h2h_total if h2h_total > 0 else 0.33
            h2h_draw_ratio = h2h_draws / h2h_total if h2h_total > 0 else 0.33
            
            # Calculer les probabilités estimées (modèle de base)
            home_probability = (home_form_rating * 0.4) + (h2h_home_ratio * 0.4) + 0.2  # Avantage à domicile
            away_probability = (away_form_rating * 0.4) + (h2h_away_ratio * 0.4)
            draw_probability = (home_draw_rating * 0.2) + (away_draw_rating * 0.2) + (h2h_draw_ratio * 0.4) + 0.2
            
            # Normaliser
            total_prob = home_probability + away_probability + draw_probability
            if total_prob > 0:
                home_probability /= total_prob
                away_probability /= total_prob
                draw_probability /= total_prob
            
            # 2. Analyse pour Over/Under
            # ---------------------------
            avg_goals_h2h = h2h_total_goals / h2h_matches_count if h2h_matches_count > 0 else 2.5
            
            # Calculer les buts marqués/encaissés dans les matchs récents
            home_goals_scored = 0
            home_goals_conceded = 0
            home_match_count = 0
            
            for m in home_form:
                try:
                    score = m.get('score', '').split('-')
                    if len(score) == 2:
                        home_match_count += 1
                        if m.get('home_team') == home_team:
                            home_goals_scored += int(score[0].strip())
                            home_goals_conceded += int(score[1].strip())
                        else:
                            home_goals_scored += int(score[1].strip())
                            home_goals_conceded += int(score[0].strip())
                except Exception:
                    continue
            
            away_goals_scored = 0
            away_goals_conceded = 0
            away_match_count = 0
            
            for m in away_form:
                try:
                    score = m.get('score', '').split('-')
                    if len(score) == 2:
                        away_match_count += 1
                        if m.get('home_team') == away_team:
                            away_goals_scored += int(score[0].strip())
                            away_goals_conceded += int(score[1].strip())
                        else:
                            away_goals_scored += int(score[1].strip())
                            away_goals_conceded += int(score[0].strip())
                except Exception:
                    continue
            
            # Calculer les moyennes
            home_goals_scored_avg = home_goals_scored / home_match_count if home_match_count > 0 else 1.5
            home_goals_conceded_avg = home_goals_conceded / home_match_count if home_match_count > 0 else 1.0
            away_goals_scored_avg = away_goals_scored / away_match_count if away_match_count > 0 else 1.0
            away_goals_conceded_avg = away_goals_conceded / away_match_count if away_match_count > 0 else 1.5
            
            # Prédire le nombre de buts
            expected_goals = (home_goals_scored_avg * 0.25) + (away_goals_conceded_avg * 0.25) + (away_goals_scored_avg * 0.25) + (home_goals_conceded_avg * 0.25)
            
            # Probabilités Over/Under 2.5
            over_probability = 0.5
            if expected_goals > 2.5:
                over_probability = 0.5 + ((expected_goals - 2.5) * 0.15)
            else:
                over_probability = 0.5 - ((2.5 - expected_goals) * 0.15)
            
            # Ajuster avec les H2H
            if avg_goals_h2h > 2.5:
                over_probability += (avg_goals_h2h - 2.5) * 0.1
            else:
                over_probability -= (2.5 - avg_goals_h2h) * 0.1
            
            # Limites
            over_probability = max(0.2, min(0.9, over_probability))
            under_probability = 1 - over_probability
            
            # 3. Analyse pour BTTS (Both Teams To Score)
            # ------------------------------------------
            btts_yes_matches_h2h = sum(1 for m in h2h if len(m.get('score', '').split('-')) == 2 and int(m.get('score', '').split('-')[0]) > 0 and int(m.get('score', '').split('-')[1]) > 0)
            btts_yes_ratio_h2h = btts_yes_matches_h2h / h2h_matches_count if h2h_matches_count > 0 else 0.5
            
            # Calcul basé sur la capacité offensive et défensive des équipes
            home_attacking_strength = home_goals_scored_avg / 1.5  # Normaliser par rapport à la moyenne
            away_attacking_strength = away_goals_scored_avg / 1.0  # Normaliser par rapport à la moyenne
            home_defensive_weakness = home_goals_conceded_avg / 1.0  # Normaliser par rapport à la moyenne
            away_defensive_weakness = away_goals_conceded_avg / 1.5  # Normaliser par rapport à la moyenne
            
            # Probabilité que chaque équipe marque
            home_scores_prob = (home_attacking_strength * 0.7) + (away_defensive_weakness * 0.3)
            away_scores_prob = (away_attacking_strength * 0.7) + (home_defensive_weakness * 0.3)
            
            # Probabilité BTTS
            btts_yes_probability = home_scores_prob * away_scores_prob
            btts_yes_probability = (btts_yes_probability * 0.6) + (btts_yes_ratio_h2h * 0.4)
            
            # Limites
            btts_yes_probability = max(0.3, min(0.9, btts_yes_probability))
            btts_no_probability = 1 - btts_yes_probability
            
            # 4. Intégrer les prédictions ArcanShadow si disponibles
            # -----------------------------------------------------
            if arcan_predictions:
                # Ajuster les probabilités avec les prédictions ArcanShadow
                arcan_prediction_type = arcan_predictions.get('prediction_type', '')
                arcan_confidence = arcan_predictions.get('confidence', 0.0)
                
                if arcan_prediction_type == 'home_win' and arcan_confidence > 0.5:
                    # Ajuster les probabilités en intégrant la prédiction ArcanShadow
                    home_probability = (home_probability * 0.6) + (arcan_confidence * 0.4)
                    away_probability *= 0.8
                    draw_probability *= 0.8
                    
                    # Renormaliser
                    total = home_probability + away_probability + draw_probability
                    home_probability /= total
                    away_probability /= total
                    draw_probability /= total
                
                elif arcan_prediction_type == 'away_win' and arcan_confidence > 0.5:
                    # Ajuster les probabilités en intégrant la prédiction ArcanShadow
                    away_probability = (away_probability * 0.6) + (arcan_confidence * 0.4)
                    home_probability *= 0.8
                    draw_probability *= 0.8
                    
                    # Renormaliser
                    total = home_probability + away_probability + draw_probability
                    home_probability /= total
                    away_probability /= total
                    draw_probability /= total
                
                elif arcan_prediction_type == 'draw' and arcan_confidence > 0.5:
                    # Ajuster les probabilités en intégrant la prédiction ArcanShadow
                    draw_probability = (draw_probability * 0.6) + (arcan_confidence * 0.4)
                    home_probability *= 0.8
                    away_probability *= 0.8
                    
                    # Renormaliser
                    total = home_probability + away_probability + draw_probability
                    home_probability /= total
                    away_probability /= total
                    draw_probability /= total
                
                # Intégrer les prédictions pour Over/Under si disponibles
                if 'goals_prediction' in arcan_predictions:
                    goals_pred = arcan_predictions['goals_prediction']
                    arcan_over_confidence = goals_pred.get('over_confidence', 0.0)
                    arcan_under_confidence = goals_pred.get('under_confidence', 0.0)
                    
                    if arcan_over_confidence > 0.5:
                        over_probability = (over_probability * 0.6) + (arcan_over_confidence * 0.4)
                        under_probability = 1 - over_probability
                    
                    elif arcan_under_confidence > 0.5:
                        under_probability = (under_probability * 0.6) + (arcan_under_confidence * 0.4)
                        over_probability = 1 - under_probability
                
                # Intégrer les prédictions pour BTTS si disponibles
                if 'btts_prediction' in arcan_predictions:
                    btts_pred = arcan_predictions['btts_prediction']
                    arcan_btts_probability = btts_pred.get('btts_probability', 0.0)
                    
                    if arcan_btts_probability > 0.3:
                        btts_yes_probability = (btts_yes_probability * 0.6) + (arcan_btts_probability * 0.4)
                        btts_no_probability = 1 - btts_yes_probability
            
            # 5. Collecter les prédictions finales
            # -----------------------------------
            predictions = {
                # Marché 1X2
                '1X2': {
                    'home_win': {
                        'probability': home_probability,
                        'selection': home_team,
                        'market': '1X2',
                        'odds': float(odds.get('1', 0)) if odds.get('1') else 0,
                        'confidence': home_probability,
                        'insight': f"Forme récente: {home_form_rating:.2f}, H2H: {h2h_home_ratio:.2f}",
                        'ev': (home_probability * float(odds.get('1', 0))) - 1 if odds.get('1') else 0
                    },
                    'draw': {
                        'probability': draw_probability,
                        'selection': 'Draw',
                        'market': '1X2',
                        'odds': float(odds.get('X', 0)) if odds.get('X') else 0,
                        'confidence': draw_probability,
                        'insight': f"Matchs nuls récents des deux équipes, H2H: {h2h_draw_ratio:.2f}",
                        'ev': (draw_probability * float(odds.get('X', 0))) - 1 if odds.get('X') else 0
                    },
                    'away_win': {
                        'probability': away_probability,
                        'selection': away_team,
                        'market': '1X2',
                        'odds': float(odds.get('2', 0)) if odds.get('2') else 0,
                        'confidence': away_probability,
                        'insight': f"Forme récente: {away_form_rating:.2f}, H2H: {h2h_away_ratio:.2f}",
                        'ev': (away_probability * float(odds.get('2', 0))) - 1 if odds.get('2') else 0
                    }
                },
                
                # Marché Over/Under
                'O/U 2.5': {
                    'over': {
                        'probability': over_probability,
                        'selection': 'Over 2.5 Goals',
                        'market': 'O/U 2.5',
                        'odds': 1.90,  # Cotes par défaut si non disponibles
                        'confidence': over_probability,
                        'insight': f"Buts attendus: {expected_goals:.2f}, Moyenne H2H: {avg_goals_h2h:.2f}",
                        'ev': (over_probability * 1.90) - 1
                    },
                    'under': {
                        'probability': under_probability,
                        'selection': 'Under 2.5 Goals',
                        'market': 'O/U 2.5',
                        'odds': 1.90,  # Cotes par défaut si non disponibles
                        'confidence': under_probability,
                        'insight': f"Buts attendus: {expected_goals:.2f}, Moyenne H2H: {avg_goals_h2h:.2f}",
                        'ev': (under_probability * 1.90) - 1
                    }
                },
                
                # Marché BTTS
                'BTTS': {
                    'yes': {
                        'probability': btts_yes_probability,
                        'selection': 'Yes',
                        'market': 'BTTS',
                        'odds': 1.85,  # Cotes par défaut si non disponibles
                        'confidence': btts_yes_probability,
                        'insight': f"Force attaque: {home_attacking_strength:.2f}/{away_attacking_strength:.2f}, BTTS en H2H: {btts_yes_ratio_h2h:.2f}",
                        'ev': (btts_yes_probability * 1.85) - 1
                    },
                    'no': {
                        'probability': btts_no_probability,
                        'selection': 'No',
                        'market': 'BTTS',
                        'odds': 1.95,  # Cotes par défaut si non disponibles
                        'confidence': btts_no_probability,
                        'insight': f"Force défense: {(2-home_defensive_weakness):.2f}/{(2-away_defensive_weakness):.2f}, Clean sheets en H2H: {1-btts_yes_ratio_h2h:.2f}",
                        'ev': (btts_no_probability * 1.95) - 1
                    }
                },
                
                # Informations générales
                'match_info': {
                    'home_team': home_team,
                    'away_team': away_team,
                    'expected_goals': expected_goals,
                    'home_form_rating': home_form_rating,
                    'away_form_rating': away_form_rating,
                    'h2h_home_ratio': h2h_home_ratio,
                    'h2h_away_ratio': h2h_away_ratio,
                    'h2h_draw_ratio': h2h_draw_ratio,
                    'avg_goals_h2h': avg_goals_h2h
                }
            }
            
            return predictions
            
        except Exception as e:
            logger.error(f"Erreur lors de la prédiction des résultats du match: {e}")
            return {
                '1X2': {},
                'O/U 2.5': {},
                'BTTS': {},
                'match_info': {}
            }
    
    def generate_best_bets(self, matches=None, arcan_predictions=None, min_confidence=0.6, min_ev=0.05):
        """
        Génère les meilleurs paris pour une liste de matchs.
        
        Args:
            matches (list, optional): Liste de matchs (si None, récupère les matchs du jour)
            arcan_predictions (dict, optional): Prédictions des modules ArcanShadow
            min_confidence (float): Confiance minimale pour les paris
            min_ev (float): Valeur espérée minimale pour les paris
            
        Returns:
            list: Liste des meilleurs paris
        """
        try:
            # Si aucun match n'est fourni, récupérer les matchs du jour
            if matches is None:
                matches = self.data_enrichment.get_daily_matches()
                
                # Enrichir les données des matchs
                matches = self.data_enrichment.enrich_matches_data(matches)
            
            best_bets = []
            
            for match in matches:
                try:
                    match_id = match.get('id')
                    
                    # Récupérer les prédictions ArcanShadow pour ce match si disponibles
                    match_arcan_predictions = None
                    if arcan_predictions:
                        for pred in arcan_predictions:
                            if pred.get('match_id') == match_id:
                                match_arcan_predictions = pred
                                break
                    
                    # Prédire les résultats du match
                    predictions = self.predict_match_outcomes(match, match_arcan_predictions)
                    
                    # Pour chaque marché, récupérer le meilleur pari
                    for market, market_predictions in predictions.items():
                        if market == 'match_info':
                            continue
                        
                        for outcome, prediction in market_predictions.items():
                            # Vérifier si le pari répond aux critères
                            if prediction.get('confidence', 0) >= min_confidence and prediction.get('ev', 0) >= min_ev:
                                best_bets.append({
                                    'match': {
                                        'id': match.get('id'),
                                        'home_team': match.get('home_team'),
                                        'away_team': match.get('away_team'),
                                        'time': match.get('time'),
                                        'date': match.get('date'),
                                        'league': match.get('league')
                                    },
                                    'selection': prediction.get('selection'),
                                    'market': prediction.get('market'),
                                    'odds': prediction.get('odds'),
                                    'confidence': prediction.get('confidence'),
                                    'ev': prediction.get('ev'),
                                    'insight': prediction.get('insight'),
                                    'module_source': 'BettingComboGenerator'
                                })
                
                except Exception as e:
                    logger.error(f"Erreur lors de l'analyse du match {match.get('id')}: {e}")
                    continue
            
            # Trier par valeur espérée décroissante
            best_bets.sort(key=lambda x: x.get('ev', 0), reverse=True)
            
            return best_bets
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération des meilleurs paris: {e}")
            return []
    
    def generate_daily_combo(self, matches=None, arcan_predictions=None, max_selections=4, risk_level='medium', use_top_modules=False):
        """
        Génère un combiné de paris du jour.
        
        Args:
            matches (list, optional): Liste de matchs (si None, récupère les matchs du jour)
            arcan_predictions (dict, optional): Prédictions des modules ArcanShadow
            max_selections (int): Nombre maximum de sélections dans le combiné
            risk_level (str): Niveau de risque ('low', 'medium', 'high')
            use_top_modules (bool): Utiliser uniquement les prédictions des modules les plus performants
            
        Returns:
            dict: Combiné du jour
        """
        try:
            # Paramètres selon le niveau de risque
            risk_params = {
                'low': {'min_confidence': 0.7, 'min_ev': 0.1, 'max_odds': 1.8},
                'medium': {'min_confidence': 0.65, 'min_ev': 0.05, 'max_odds': 2.5},
                'high': {'min_confidence': 0.55, 'min_ev': 0.0, 'max_odds': 4.0}
            }
            
            params = risk_params.get(risk_level, risk_params['medium'])
            
            # Filtrer les prédictions par modules performants si demandé
            filtered_predictions = arcan_predictions
            if use_top_modules and arcan_predictions:
                # Récupérer les performances des modules (à implémenter dans un système réel)
                module_performance = self._get_module_performance()
                
                # Filtrer pour ne garder que les prédictions des modules performants
                top_modules = [module for module, perf in module_performance.items() if perf >= 0.6]
                
                if top_modules:
                    filtered_predictions = []
                    for pred in arcan_predictions:
                        if pred.get('source_module') in top_modules:
                            filtered_predictions.append(pred)
            
            # Générer les meilleurs paris
            best_bets = self.generate_best_bets(
                matches=matches,
                arcan_predictions=filtered_predictions,
                min_confidence=params['min_confidence'],
                min_ev=params['min_ev']
            )
            
            # Filtrer selon les cotes maximales
            filtered_bets = [bet for bet in best_bets if bet.get('odds', 0) <= params['max_odds']]
            
            # Assurer que nous ne sélectionnons pas plus d'un pari par match
            selected_matches = set()
            combo_selections = []
            
            for bet in filtered_bets:
                match_id = bet.get('match', {}).get('id')
                
                if match_id not in selected_matches and len(combo_selections) < max_selections:
                    selected_matches.add(match_id)
                    combo_selections.append(bet)
            
            # Si nous n'avons pas assez de sélections, compléter avec d'autres paris
            if len(combo_selections) < max_selections and len(best_bets) > len(combo_selections):
                for bet in best_bets:
                    match_id = bet.get('match', {}).get('id')
                    
                    if match_id not in selected_matches and len(combo_selections) < max_selections:
                        selected_matches.add(match_id)
                        combo_selections.append(bet)
            
            # Calculer les cotes totales et la confiance
            total_odds = 1.0
            for selection in combo_selections:
                total_odds *= selection.get('odds', 1.0)
            
            # Calculer la confiance globale (moyenne géométrique)
            total_confidence = 1.0
            for selection in combo_selections:
                total_confidence *= selection.get('confidence', 0.5)
            
            avg_confidence = total_confidence ** (1 / len(combo_selections)) if combo_selections else 0
            
            # Calculer la valeur espérée
            expected_value = (avg_confidence * total_odds) - 1
            
            return {
                'selections': combo_selections,
                'total_odds': total_odds,
                'avg_confidence': avg_confidence,
                'expected_value': expected_value,
                'risk_level': risk_level,
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération du combiné du jour: {e}")
            return {
                'selections': [],
                'total_odds': 0,
                'avg_confidence': 0,
                'expected_value': 0,
                'risk_level': risk_level,
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
    
    def _get_module_performance(self):
        """
        Récupère les performances des modules (taux de réussite des prédictions).
        Dans un système réel, cela serait connecté à une base de données de résultats.
        
        Returns:
            dict: Dictionnaire des modules avec leur performance (0-1)
        """
        # Simulation des performances des modules
        # Dans un système réel, ces données viendraient d'une analyse des prédictions passées
        return {
            'ArcanX': 0.72,               # Module principal d'analyse de tendances
            'ShadowOdds': 0.68,           # Module d'analyse des cotes et mouvements
            'MatchMomentum': 0.65,        # Module d'analyse de momentum
            'ArcanBrain': 0.78,           # Module d'intelligence neuronal
            'GoalFlowAnalyzer': 0.67,     # Module d'analyse de buts
            'DefenseVulnerabilityScanner': 0.62, # Module d'analyse défensive
            'FanSentimentMonitor': 0.52,  # Module d'analyse de sentiment des fans
            'StrengthDisparityAnalyzer': 0.64,   # Module d'analyse de disparité
            'ArcanSentinel': 0.73,        # Module de surveillance en direct
            'LateSurgeDetector': 0.59,    # Module de détection de tendances tardives
            'FormCycleAnalyzer': 0.66     # Module d'analyse des cycles de forme
        }
    
    def get_bet_insights(self, combo):
        """
        Génère des insights pour un combiné.
        
        Args:
            combo (dict): Combiné de paris
            
        Returns:
            list: Liste des insights
        """
        insights = []
        
        try:
            selections = combo.get('selections', [])
            ev = combo.get('expected_value', 0)
            
            if not selections:
                insights.append("Aucune sélection dans le combiné du jour.")
                return insights
            
            # Insight sur la valeur globale
            if ev > 0.3:
                insights.append("⭐⭐⭐ Combiné à très forte valeur espérée")
            elif ev > 0.15:
                insights.append("⭐⭐ Combiné à bonne valeur espérée")
            elif ev > 0:
                insights.append("⭐ Combiné à valeur espérée positive")
            else:
                insights.append("⚠️ Combiné à valeur espérée négative ou nulle")
            
            # Insight sur les cotes
            total_odds = combo.get('total_odds', 1.0)
            if total_odds > 10:
                insights.append("📈 Combiné à forte cote - rendement potentiel élevé mais risqué")
            elif total_odds > 5:
                insights.append("📊 Combiné à cote moyenne - bon équilibre risque/rendement")
            else:
                insights.append("🔒 Combiné à cote prudente - moins risqué mais rendement limité")
            
            # Analyse des marchés représentés
            markets = {}
            for selection in selections:
                market = selection.get('market', '')
                if market in markets:
                    markets[market] += 1
                else:
                    markets[market] = 1
            
            if '1X2' in markets and markets['1X2'] > 1:
                insights.append(f"📝 Ce combiné contient plusieurs paris sur le résultat final ({markets['1X2']} sélections)")
            
            if 'O/U 2.5' in markets and markets['O/U 2.5'] > 1:
                insights.append(f"⚽ Ce combiné contient plusieurs paris sur le nombre de buts ({markets['O/U 2.5']} sélections)")
            
            if 'BTTS' in markets and markets['BTTS'] > 1:
                insights.append(f"🥅 Ce combiné contient plusieurs paris sur les deux équipes qui marquent ({markets['BTTS']} sélections)")
            
            # Analyse de la diversité des marchés
            if len(markets) > 2:
                insights.append("🔄 Combiné diversifié avec différents types de marchés - bonne stratégie")
            
            # Analyse des cotes individuelles
            high_odds_count = sum(1 for s in selections if s.get('odds', 0) > 2.5)
            if high_odds_count > 0:
                insights.append(f"⚠️ Ce combiné contient {high_odds_count} sélection(s) à forte cote (>2.5)")
            
            # Conseils généraux
            insights.append("💡 Rappelez-vous que les paris sportifs comportent toujours une part d'incertitude")
            if len(selections) > 3:
                insights.append("💰 Conseil: Envisagez aussi des paris en système pour plus de sécurité")
            
            return insights
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération des insights: {e}")
            return ["Erreur lors de l'analyse du combiné"]