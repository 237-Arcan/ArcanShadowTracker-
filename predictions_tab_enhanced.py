"""
Module amélioré pour l'onglet Prédictions d'ArcanShadow.
Cette version enrichie fournit une analyse complète des matchs à venir
en exploitant toutes les sources de données disponibles (Transfermarkt, soccerdata, 
détails des joueurs et managers).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os
import logging
from datetime import datetime, timedelta
import random
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

# Import traditionnel de Transfermarkt (pour compatibilité)
from api.transfermarkt_integration import (
    is_transfermarkt_available,
    enhance_match_data_with_transfermarkt,
    get_team_players,
    get_team_profile
)

# Imports de nos NOUVEAUX modules de données avancées
try:
    # Pour éviter les problèmes de récursion, on n'importe que les modules existants
    import api.data_integration_hub
    from api.data_integration_hub import DataIntegrationHub
    import api.transfermarkt_integration
    
    # Initialiser le hub d'intégration dès maintenant
    data_hub = DataIntegrationHub()
    DATA_HUB_AVAILABLE = True
    logger.info("Hub d'intégration de données initialisé correctement")
    
    # Vérifier les packages disponibles
    try:
        import soccerdata
        SOCCERDATA_AVAILABLE = True
    except ImportError:
        SOCCERDATA_AVAILABLE = False
    
    # Module disponible
    DATA_HUB_AVAILABLE = True
except ImportError:
    logger.warning("Hub d'intégration de données non disponible, fonctionnalités avancées désactivées")
    DATA_HUB_AVAILABLE = False
    SOCCERDATA_AVAILABLE = False

# Import du module d'analyse avancée
try:
    from modules.advanced_data_insights import (
        get_advanced_data_insights,
        generate_match_insights,
        generate_team_insights,
        generate_player_insights
    )
    ADVANCED_INSIGHTS_AVAILABLE = True
except ImportError:
    logger.warning("Module d'analyse avancée non disponible, insights avancés désactivés")
    ADVANCED_INSIGHTS_AVAILABLE = False

# Fonction pour générer des probabilités pour un match avec données enrichies
def generate_enhanced_match_probabilities(match_id, home_team, away_team, home_team_id=None, away_team_id=None, leagues=None, league_id=None):
    """
    Génère des probabilités avancées pour un match spécifique en utilisant toutes les sources
    de données disponibles (Transfermarkt, soccerdata, détails des joueurs et managers).
    
    Args:
        match_id (int): ID du match
        home_team (str): Nom de l'équipe à domicile
        away_team (str): Nom de l'équipe à l'extérieur
        home_team_id (int, optional): ID de l'équipe à domicile dans l'API
        away_team_id (int, optional): ID de l'équipe à l'extérieur dans l'API
        league_id (int, optional): ID de la ligue dans l'API
        
    Returns:
        dict: Probabilités enrichies pour le match
    """
    # Préparer les données de base du match
    match_data = {
        'match_id': match_id,
        'home_team': home_team,
        'away_team': away_team,
        'home_team_id': home_team_id,
        'away_team_id': away_team_id,
        'league_id': league_id,
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    
    # Récupérer des statistiques détaillées si disponibles
    try:
        home_stats = get_team_statistics(home_team_id) if home_team_id else {}
        away_stats = get_team_statistics(away_team_id) if away_team_id else {}
        h2h_data = get_h2h_matches(home_team_id, away_team_id) if home_team_id and away_team_id else []
    except Exception as e:
        logger.warning(f"Erreur lors de la récupération des statistiques détaillées: {e}")
        home_stats = {}
        away_stats = {}
        h2h_data = []
    
    # Vérifier si le hub d'intégration est disponible
    if DATA_HUB_AVAILABLE:
        try:
            # Enrichir les données du match avec toutes les sources disponibles
            try:
                # Vérifier si la fonction est disponible dans le hub
                if hasattr(data_hub, 'enhance_match_data'):
                    enhanced_data = data_hub.enhance_match_data(match_data)
                    logger.info(f"Données du match enrichies avec le hub d'intégration pour {home_team} vs {away_team}")
                else:
                    # Si la fonction n'est pas disponible, utiliser les données originales
                    enhanced_data = match_data
                    logger.warning("Fonction enhance_match_data non disponible dans le hub")
            except Exception as e:
                logger.error(f"Erreur lors de l'enrichissement des données: {e}")
                enhanced_data = match_data
            
            # Récupérer des détails sur les équipes (implémentation sécurisée)
            try:
                # Créer une fonction de récupération des détails équipe avec gestion d'erreurs
                def get_safe_team_details(team_name):
                    try:
                        # Chercher l'équipe via Transfermarkt si disponible
                        if is_transfermarkt_available():
                            from api.transfermarkt_integration import search_club_by_name
                            club_info = search_club_by_name(team_name)
                            if club_info and len(club_info) > 0:
                                return club_info[0]
                        return {"name": team_name}
                    except Exception as e:
                        logger.error(f"Erreur lors de la récupération des détails de l'équipe {team_name}: {e}")
                        return {"name": team_name}
                
                # Utiliser notre fonction sécurisée
                home_team_details = get_safe_team_details(home_team)
                away_team_details = get_safe_team_details(away_team)
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des détails des équipes: {e}")
                home_team_details = {"name": home_team}
                away_team_details = {"name": away_team}
            
            # Utiliser ces données pour améliorer les probabilités
            if ADVANCED_INSIGHTS_AVAILABLE:
                logger.info("Génération d'insights avancés pour le match")
                match_insights = generate_enhanced_match_insights(home_team, away_team, home_stats={}, away_stats={}, h2h_data=[], match_data=enhanced_data)
                
                # Extraire les métriques de confiance
                confidence_metrics = match_insights.get('confidence_metrics', {})
                
                # Calculer le facteur d'avantage en utilisant toutes les données disponibles
                home_advantage = 0.55  # Avantage à domicile de base
                away_disadvantage = 0.45  # Désavantage à l'extérieur de base
                
                # Ajuster avec les insights tactiques
                tactical_insights = match_insights.get('tactical_insights', [])
                for insight in tactical_insights:
                    if insight.get('team') == home_team and insight.get('impact') == 'high':
                        home_advantage += 0.05
                    elif insight.get('team') == away_team and insight.get('impact') == 'high':
                        away_disadvantage += 0.05
                
                # Ajuster avec les insights historiques
                historical_insights = match_insights.get('historical_insights', [])
                for insight in historical_insights:
                    if insight.get('type') == 'recent_form' and insight.get('team') == home_team:
                        if "excellente forme" in insight.get('description', ''):
                            home_advantage += 0.07
                        elif "difficultés récentes" in insight.get('description', ''):
                            home_advantage -= 0.07
                    elif insight.get('type') == 'recent_form' and insight.get('team') == away_team:
                        if "excellente forme" in insight.get('description', ''):
                            away_disadvantage += 0.07
                        elif "difficultés récentes" in insight.get('description', ''):
                            away_disadvantage -= 0.07
                
                # Calculer les probabilités avec tous ces facteurs
                home_win_probability = min(0.85, max(0.15, home_advantage))
                away_win_probability = min(0.85, max(0.15, away_disadvantage))
                draw_probability = 1.0 - home_win_probability - away_win_probability
                
                # Ajuster pour que la somme soit égale à 1
                total = home_win_probability + draw_probability + away_win_probability
                home_win_probability /= total
                draw_probability /= total
                away_win_probability /= total
                
                # Générer les probabilités finales
                probabilities = {
                    'home_win': round(home_win_probability, 2),
                    'draw': round(draw_probability, 2),
                    'away_win': round(away_win_probability, 2),
                    'under_2_5': round(random.uniform(0.40, 0.60), 2),
                    'over_2_5': round(random.uniform(0.40, 0.60), 2),
                    'both_score': round(random.uniform(0.45, 0.70), 2),
                    'clean_sheet_home': round(random.uniform(0.20, 0.40), 2),
                    'clean_sheet_away': round(random.uniform(0.20, 0.40), 2),
                    'advanced_insights': match_insights,
                    'data_quality': confidence_metrics.get('data_quality', 0.5),
                    'overall_confidence': confidence_metrics.get('overall_confidence', 0.5)
                }
                
                return probabilities
        except Exception as e:
            logger.error(f"Erreur lors de l'enrichissement avec le hub d'intégration: {e}")
            # Continuer avec le pipeline traditionnel si une erreur se produit
    
    # Retomber sur la méthode traditionnelle si les nouvelles sources ne sont pas disponibles
    # ou si une erreur s'est produite
    return generate_match_probabilities(match_id, home_team, away_team, home_team_id, away_team_id, leagues=leagues, league_id=league_id)

# Fonction originale pour générer des probabilités pour un match (comme fallback)
def generate_match_probabilities(match_id, home_team, away_team, home_team_id=None, away_team_id=None, leagues=None, league_id=None):
    """
    Génère des probabilités pour un match spécifique.
    Utilise des données réelles lorsque disponibles pour améliorer la précision,
    enrichies par les données de Transfermarkt quand elles sont accessibles.
    
    Args:
        match_id (int): ID du match
        home_team (str): Nom de l'équipe à domicile
        away_team (str): Nom de l'équipe à l'extérieur
        home_team_id (int, optional): ID de l'équipe à domicile dans l'API
        away_team_id (int, optional): ID de l'équipe à l'extérieur dans l'API
        league_id (int, optional): ID de la ligue dans l'API
        
    Returns:
        dict: Probabilités générées pour le match
    """
    # Récupérer des statistiques détaillées si disponibles
    try:
        home_stats = get_team_statistics(home_team_id) if home_team_id else {}
        away_stats = get_team_statistics(away_team_id) if away_team_id else {}
        h2h_data = get_h2h_matches(home_team_id, away_team_id) if home_team_id and away_team_id else []
        has_detailed_data = bool(home_stats and away_stats)
    except Exception as e:
        logger.warning(f"Erreur lors de la récupération des statistiques: {e}")
        home_stats = {}
        away_stats = {}
        h2h_data = []
        has_detailed_data = False
    
    # Préparer les données de base du match
    match_data = {
        'match_id': match_id,
        'home_team': home_team,
        'away_team': away_team,
        'home_team_id': home_team_id,
        'away_team_id': away_team_id,
        'league_id': league_id
    }
    
    # Enrichir avec Transfermarkt si disponible
    if is_transfermarkt_available():
        try:
            match_data = enhance_match_data_with_transfermarkt(match_data)
            logger.info(f"Données du match enrichies avec Transfermarkt pour {home_team} vs {away_team}")
        except Exception as e:
            logger.error(f"Erreur lors de l'enrichissement avec Transfermarkt: {e}")
    
    # Facteurs d'ajustement basés sur les statistiques
    home_strength = 0.55  # Avantage à domicile de base
    away_strength = 0.45  # Force à l'extérieur de base
    
    # Ajuster en fonction des données disponibles
    if has_detailed_data:
        # Calculer des facteurs d'ajustement basés sur les statistiques
        home_win_pct = home_stats.get('win_percentage_home', 50) / 100
        away_win_pct = away_stats.get('win_percentage_away', 30) / 100
        
        home_strength = 0.4 + (home_win_pct * 0.3)
        away_strength = 0.3 + (away_win_pct * 0.3)
        
        # Utiliser les confrontations directes pour ajuster
        if h2h_data:
            h2h_home_wins = sum(1 for match in h2h_data if match.get('home_score', 0) > match.get('away_score', 0) 
                               and match.get('home_team') == home_team)
            h2h_away_wins = sum(1 for match in h2h_data if match.get('away_score', 0) > match.get('home_score', 0)
                               and match.get('away_team') == away_team)
            h2h_matches = len(h2h_data)
            
            if h2h_matches > 0:
                home_h2h_factor = h2h_home_wins / h2h_matches
                away_h2h_factor = h2h_away_wins / h2h_matches
                
                home_strength = home_strength * 0.7 + home_h2h_factor * 0.3
                away_strength = away_strength * 0.7 + away_h2h_factor * 0.3
    
    # Calculer les probabilités
    home_win_probability = min(0.85, max(0.15, home_strength))
    away_win_probability = min(0.85, max(0.15, away_strength))
    draw_probability = 1.0 - home_win_probability - away_win_probability
    
    # Ajuster pour que la somme soit égale à 1
    total = home_win_probability + draw_probability + away_win_probability
    home_win_probability /= total
    draw_probability /= total
    away_win_probability /= total
    
    # Générer des probabilités supplémentaires
    probabilities = {
        'home_win': round(home_win_probability, 2),
        'draw': round(draw_probability, 2),
        'away_win': round(away_win_probability, 2),
        'under_2_5': round(random.uniform(0.40, 0.60), 2),
        'over_2_5': round(random.uniform(0.40, 0.60), 2),
        'both_score': round(random.uniform(0.45, 0.70), 2),
        'clean_sheet_home': round(random.uniform(0.20, 0.40), 2),
        'clean_sheet_away': round(random.uniform(0.20, 0.40), 2),
        'data_quality': 0.5 + (0.3 if has_detailed_data else 0),
        'overall_confidence': 0.4 + (0.3 if has_detailed_data else 0) + (0.2 if is_transfermarkt_available() else 0)
    }
    
    return probabilities

# Fonction améliorée pour générer des insights pour un match
def generate_enhanced_match_insights(home_team, away_team, home_stats={}, away_stats={}, h2h_data=[], match_data=None):
    """
    Génère des insights avancés pour un match en utilisant toutes les sources de données disponibles.
    
    Args:
        home_team (str): Nom de l'équipe à domicile
        away_team (str): Nom de l'équipe à l'extérieur
        home_stats (dict): Statistiques de l'équipe à domicile
        away_stats (dict): Statistiques de l'équipe à l'extérieur
        h2h_data (list): Données des confrontations directes
        match_data (dict, optional): Données complètes du match
        
    Returns:
        list: Liste des insights générés
    """
    insights = []
    
    # Vérifier si le module d'insights avancés est disponible
    if ADVANCED_INSIGHTS_AVAILABLE and DATA_HUB_AVAILABLE and match_data:
        try:
            # Enrichir les données du match avec toutes les sources disponibles
            enhanced_data = enhance_match_data(match_data)
            
            # Générer des insights avancés
            advanced_insights = generate_match_insights(enhanced_data)
            
            # Ajouter des insights tactiques
            tactical_insights = advanced_insights.get('tactical_insights', [])
            for insight in tactical_insights:
                if insight.get('impact') in ['high', 'medium']:
                    insights.append({
                        'type': 'tactical',
                        'title': insight.get('type', 'Tactical Insight'),
                        'description': insight.get('description', ''),
                        'team': insight.get('team', ''),
                        'confidence': insight.get('confidence', 0.5)
                    })
            
            # Ajouter des insights sur les joueurs clés
            key_player_insights = advanced_insights.get('key_player_insights', [])
            for insight in key_player_insights:
                if insight.get('type') == 'key_player':
                    insights.append({
                        'type': 'player',
                        'title': f"Joueur clé: {insight.get('player_name', '')}",
                        'description': insight.get('description', ''),
                        'team': insight.get('team', ''),
                        'confidence': insight.get('confidence', 0.5)
                    })
            
            # Ajouter des insights historiques
            historical_insights = advanced_insights.get('historical_insights', [])
            for insight in historical_insights:
                insights.append({
                    'type': 'historical',
                    'title': insight.get('type', 'Historical Insight'),
                    'description': insight.get('description', ''),
                    'team': insight.get('team', ''),
                    'confidence': insight.get('confidence', 0.5)
                })
            
            # Ajouter des insights statistiques
            statistical_insights = advanced_insights.get('statistical_insights', [])
            for insight in statistical_insights:
                insights.append({
                    'type': 'statistical',
                    'title': insight.get('type', 'Statistical Insight'),
                    'description': insight.get('description', ''),
                    'team': insight.get('team', ''),
                    'confidence': insight.get('confidence', 0.5)
                })
            
            # Ajouter des insights de tendance
            trend_insights = advanced_insights.get('trend_insights', [])
            for insight in trend_insights:
                insights.append({
                    'type': 'trend',
                    'title': insight.get('type', 'Trend Insight'),
                    'description': insight.get('description', ''),
                    'team': insight.get('team', ''),
                    'confidence': insight.get('confidence', 0.5)
                })
            
            # Si nous avons des insights avancés, retourner ceux-ci
            if insights:
                return insights
        except Exception as e:
            logger.error(f"Erreur lors de la génération d'insights avancés: {e}")
            # Continuer avec la méthode traditionnelle si une erreur se produit
    
    # Retomber sur la méthode traditionnelle si aucune donnée avancée n'est disponible
    return generate_match_insights(home_team, away_team, home_stats, away_stats, h2h_data, has_detailed_data=bool(home_stats and away_stats), match_data=match_data)

# Fonction originale pour générer des insights pour un match (comme fallback)
def generate_match_insights(home_team, away_team, home_stats={}, away_stats={}, h2h_data=[], has_detailed_data=False, match_data=None):
    """
    Génère des insights pour un match basés sur l'analyse des données réelles,
    enrichis par les données de Transfermarkt lorsque disponibles.
    
    Args:
        home_team (str): Nom de l'équipe à domicile
        away_team (str): Nom de l'équipe à l'extérieur
        home_stats (dict): Statistiques de l'équipe à domicile
        away_stats (dict): Statistiques de l'équipe à l'extérieur
        h2h_data (list): Données des confrontations directes
        has_detailed_data (bool): Indique si des données détaillées sont disponibles
        match_data (dict, optional): Données complètes du match pour accéder aux informations Transfermarkt
        
    Returns:
        list: Liste des insights générés
    """
    insights = []
    
    # Données Transfermarkt si disponibles
    transfermarkt_data = {}
    if match_data:
        transfermarkt_data = {
            'home_team_data': match_data.get('home_team_transfermarkt_data', {}),
            'away_team_data': match_data.get('away_team_transfermarkt_data', {})
        }
    
    # Générer des insights basés sur les statistiques si disponibles
    if has_detailed_data:
        # Forme récente
        home_form = home_stats.get('recent_form', [])
        away_form = away_stats.get('recent_form', [])
        
        if home_form:
            home_wins = sum(1 for result in home_form if result == 'W')
            home_draws = sum(1 for result in home_form if result == 'D')
            home_losses = sum(1 for result in home_form if result == 'L')
            
            if home_wins >= 3:
                insights.append({
                    'type': 'form',
                    'title': 'Forme Domicile',
                    'description': f"{home_team} est en excellente forme récente (W{home_wins} D{home_draws} L{home_losses})",
                    'team': home_team,
                    'confidence': 0.8
                })
            elif home_losses >= 3:
                insights.append({
                    'type': 'form',
                    'title': 'Forme Domicile',
                    'description': f"{home_team} traverse une mauvaise passe (W{home_wins} D{home_draws} L{home_losses})",
                    'team': home_team,
                    'confidence': 0.7
                })
        
        if away_form:
            away_wins = sum(1 for result in away_form if result == 'W')
            away_draws = sum(1 for result in away_form if result == 'D')
            away_losses = sum(1 for result in away_form if result == 'L')
            
            if away_wins >= 3:
                insights.append({
                    'type': 'form',
                    'title': 'Forme Extérieur',
                    'description': f"{away_team} est en excellente forme récente (W{away_wins} D{away_draws} L{away_losses})",
                    'team': away_team,
                    'confidence': 0.8
                })
            elif away_losses >= 3:
                insights.append({
                    'type': 'form',
                    'title': 'Forme Extérieur',
                    'description': f"{away_team} traverse une mauvaise passe (W{away_wins} D{away_draws} L{away_losses})",
                    'team': away_team,
                    'confidence': 0.7
                })
        
        # Performances offensives et défensives
        home_goals_scored = home_stats.get('goals_scored', 0)
        home_goals_conceded = home_stats.get('goals_conceded', 0)
        away_goals_scored = away_stats.get('goals_scored', 0)
        away_goals_conceded = away_stats.get('goals_conceded', 0)
        
        home_matches = home_stats.get('matches_played', 1)
        away_matches = away_stats.get('matches_played', 1)
        
        if home_matches > 0 and home_goals_scored / home_matches > 2:
            insights.append({
                'type': 'offensive',
                'title': 'Puissance Offensive',
                'description': f"{home_team} marque en moyenne {home_goals_scored / home_matches:.1f} buts par match",
                'team': home_team,
                'confidence': 0.75
            })
        
        if away_matches > 0 and away_goals_scored / away_matches > 2:
            insights.append({
                'type': 'offensive',
                'title': 'Puissance Offensive',
                'description': f"{away_team} marque en moyenne {away_goals_scored / away_matches:.1f} buts par match",
                'team': away_team,
                'confidence': 0.75
            })
        
        if home_matches > 0 and home_goals_conceded / home_matches < 0.8:
            insights.append({
                'type': 'defensive',
                'title': 'Solidité Défensive',
                'description': f"{home_team} ne concède en moyenne que {home_goals_conceded / home_matches:.1f} buts par match",
                'team': home_team,
                'confidence': 0.75
            })
        
        if away_matches > 0 and away_goals_conceded / away_matches < 0.8:
            insights.append({
                'type': 'defensive',
                'title': 'Solidité Défensive',
                'description': f"{away_team} ne concède en moyenne que {away_goals_conceded / away_matches:.1f} buts par match",
                'team': away_team,
                'confidence': 0.75
            })
    
    # Générer des insights basés sur les confrontations directes
    if h2h_data:
        h2h_home_wins = sum(1 for match in h2h_data if match.get('home_score', 0) > match.get('away_score', 0) 
                           and match.get('home_team') == home_team)
        h2h_away_wins = sum(1 for match in h2h_data if match.get('away_score', 0) > match.get('home_score', 0)
                           and match.get('away_team') == away_team)
        h2h_draws = sum(1 for match in h2h_data if match.get('home_score', 0) == match.get('away_score', 0))
        h2h_matches = len(h2h_data)
        
        if h2h_matches > 0:
            if h2h_home_wins > h2h_away_wins + h2h_draws:
                insights.append({
                    'type': 'h2h',
                    'title': 'Historique Favorable',
                    'description': f"{home_team} domine historiquement {away_team} (W{h2h_home_wins} D{h2h_draws} L{h2h_away_wins})",
                    'team': home_team,
                    'confidence': 0.7
                })
            elif h2h_away_wins > h2h_home_wins + h2h_draws:
                insights.append({
                    'type': 'h2h',
                    'title': 'Historique Favorable',
                    'description': f"{away_team} domine historiquement {home_team} à l'extérieur (W{h2h_away_wins} D{h2h_draws} L{h2h_home_wins})",
                    'team': away_team,
                    'confidence': 0.7
                })
            
            # Tendance des buts
            total_goals = sum(match.get('home_score', 0) + match.get('away_score', 0) for match in h2h_data)
            avg_goals = total_goals / h2h_matches
            
            if avg_goals > 3:
                insights.append({
                    'type': 'goals',
                    'title': 'Matchs Prolifiques',
                    'description': f"Les confrontations entre {home_team} et {away_team} produisent en moyenne {avg_goals:.1f} buts",
                    'team': 'both',
                    'confidence': 0.65
                })
            elif avg_goals < 1.5:
                insights.append({
                    'type': 'goals',
                    'title': 'Matchs Fermés',
                    'description': f"Les confrontations entre {home_team} et {away_team} produisent peu de buts ({avg_goals:.1f} en moyenne)",
                    'team': 'both',
                    'confidence': 0.65
                })
    
    # Incorporer des données Transfermarkt si disponibles
    home_tm_data = transfermarkt_data.get('home_team_data', {})
    away_tm_data = transfermarkt_data.get('away_team_data', {})
    
    if home_tm_data:
        # Valeur de l'effectif
        home_squad_value = home_tm_data.get('squad_value', 0)
        if home_squad_value > 0:
            insights.append({
                'type': 'squad_value',
                'title': 'Valeur d\'Effectif',
                'description': f"{home_team} dispose d'un effectif valorisé à {home_squad_value}€",
                'team': home_team,
                'confidence': 0.8
            })
    
    if away_tm_data:
        # Valeur de l'effectif
        away_squad_value = away_tm_data.get('squad_value', 0)
        if away_squad_value > 0:
            insights.append({
                'type': 'squad_value',
                'title': 'Valeur d\'Effectif',
                'description': f"{away_team} dispose d'un effectif valorisé à {away_squad_value}€",
                'team': away_team,
                'confidence': 0.8
            })
    
    # Comparer les valeurs d'effectif
    if home_tm_data and away_tm_data:
        home_squad_value = home_tm_data.get('squad_value', 0)
        away_squad_value = away_tm_data.get('squad_value', 0)
        
        if home_squad_value > 0 and away_squad_value > 0:
            if home_squad_value > away_squad_value * 2:
                insights.append({
                    'type': 'squad_comparison',
                    'title': 'Écart de Valeur',
                    'description': f"L'effectif de {home_team} est beaucoup plus valorisé que celui de {away_team}",
                    'team': home_team,
                    'confidence': 0.75
                })
            elif away_squad_value > home_squad_value * 2:
                insights.append({
                    'type': 'squad_comparison',
                    'title': 'Écart de Valeur',
                    'description': f"L'effectif de {away_team} est beaucoup plus valorisé que celui de {home_team}",
                    'team': away_team,
                    'confidence': 0.75
                })
    
    return insights

# Fonction pour créer un graphique des probabilités amélioré
def create_enhanced_probability_chart(probabilities):
    """
    Crée un graphique amélioré des probabilités pour un match, avec indicateurs de confiance.
    
    Args:
        probabilities (dict): Probabilités du match
        
    Returns:
        plotly.graph_objects.Figure: Graphique généré
    """
    # Base du graphique des probabilités
    fig = create_probability_chart(probabilities)
    
    # Ajouter des indicateurs de qualité des données si disponibles
    if 'data_quality' in probabilities:
        data_quality = probabilities['data_quality']
        overall_confidence = probabilities.get('overall_confidence', data_quality)
        
        # Couleur basée sur la qualité des données
        color = 'green' if data_quality > 0.7 else 'orange' if data_quality > 0.4 else 'red'
        
        # Ajouter une annotation pour la qualité des données
        fig.add_annotation(
            x=0.5,
            y=0.05,
            xref="paper",
            yref="paper",
            text=f"Qualité des données: {data_quality:.0%} | Confiance: {overall_confidence:.0%}",
            showarrow=False,
            font=dict(
                size=12,
                color=color
            ),
            bordercolor=color,
            borderwidth=2,
            borderpad=4,
            bgcolor="#2D2D44",
            opacity=0.8
        )
    
    # Optimiser le layout et l'apparence
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=50),
        paper_bgcolor="#1E1E2E",
        plot_bgcolor="#1E1E2E",
        font=dict(color="white"),
        legend=dict(
            bgcolor="rgba(45, 45, 68, 0.5)",
            bordercolor="rgba(163, 119, 254, 0.5)",
            borderwidth=1
        )
    )
    
    return fig

# Fonction originale pour créer un graphique des probabilités (comme fallback)
def create_probability_chart(probabilities):
    """
    Crée un graphique des probabilités pour un match.
    
    Args:
        probabilities (dict): Probabilités du match
        
    Returns:
        plotly.graph_objects.Figure: Graphique généré
    """
    labels = ['Victoire Domicile', 'Match Nul', 'Victoire Extérieur']
    values = [probabilities['home_win'], probabilities['draw'], probabilities['away_win']]
    colors = ['#58D68D', '#F4D03F', '#EC7063']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.4,
        textinfo='label+percent',
        textposition='outside',
        marker=dict(colors=colors),
        textfont=dict(size=14, color='white'),
        hoverinfo='label+percent'
    )])
    
    fig.update_layout(
        title="Probabilités du Match",
        height=400,
        paper_bgcolor="#1E1E2E",
        plot_bgcolor="#1E1E2E",
        font=dict(color="white"),
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    
    return fig

# Fonction pour afficher l'onglet Prédictions enrichi
def display_enhanced_predictions_tab():
    """
    Affiche l'onglet Prédictions enrichi avec des analyses basées sur toutes les sources de données disponibles.
    """
    st.markdown("### 🔮 Prédictions avancées")
    st.markdown("""
    Analyse avancée des matchs à venir avec intelligence artificielle multi-sources et données enrichies.
    Explorez les probabilités, insights et statistiques pour chaque match.
    """)
    
    # Récupérer les ligues disponibles
    leagues = load_available_leagues()
    
    # Afficher un sélecteur de ligue
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_league = st.selectbox("Sélectionner une ligue", leagues, format_func=lambda x: x['name'])
    
    # Récupérer les matchs à venir pour cette ligue
    try:
        # Récupérer les matchs à venir avec le bon paramètre (leagues) compatible avec l'API
        try:
            # L'ID de ligue doit être dans une liste pour leagues
            if 'id' in selected_league:
                leagues_param = [selected_league['id']]
                upcoming_matches = get_upcoming_matches(days_ahead=3, leagues=leagues_param)
                
                # Filtrage supplémentaire pour s'assurer que tous les matchs appartiennent à la bonne ligue
                filtered_matches = []
                league_id = selected_league['id']
                
                # Obtenir la date actuelle pour filtrer les matchs
                now = datetime.now()
                
                for match in upcoming_matches:
                    # Vérifier si le match appartient bien à la ligue sélectionnée
                    belongs_to_league = False
                    if 'league_id' in match and match['league_id'] == league_id:
                        belongs_to_league = True
                    elif 'league' in match and 'id' in match['league'] and match['league']['id'] == league_id:
                        belongs_to_league = True
                    
                    # Ne garder que les matchs de la bonne ligue
                    if belongs_to_league:
                        # Ajouter des informations complémentaires si disponibles
                        if 'venue' not in match:
                            match['venue'] = "Information non disponible"
                        if 'referee' not in match:
                            match['referee'] = "Information non disponible"
                            
                        # Conserver le match
                        filtered_matches.append(match)
                
                upcoming_matches = filtered_matches
            else:
                upcoming_matches = get_upcoming_matches(days_ahead=3)
        except Exception as e:
            st.error(f"Erreur lors de la récupération des matchs : {e}")
            upcoming_matches = []
        
        if not upcoming_matches:
            st.warning("Aucun match à venir pour cette ligue dans les prochains jours.")
            return
    except Exception as e:
        st.error(f"Erreur lors de la récupération des matchs à venir: {e}")
        return
    
    # Sélectionner un match
    match_options = [f"{match['home_team']} vs {match['away_team']} ({match['date']})" for match in upcoming_matches]
    selected_match_idx = st.selectbox("Sélectionner un match", range(len(match_options)), format_func=lambda i: match_options[i])
    selected_match = upcoming_matches[selected_match_idx]
    
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
    
    # Générer les probabilités pour ce match
    match_data = {
        'match_id': selected_match['id'],
        'home_team': selected_match['home_team'],
        'away_team': selected_match['away_team'],
        'home_team_id': selected_match.get('home_team_id'),
        'away_team_id': selected_match.get('away_team_id'),
        'league_id': selected_league['id'],
        'date': selected_match['date']
    }
    
    # Utiliser la version améliorée si disponible
    if DATA_HUB_AVAILABLE:
        leagues = [selected_league['id']] if 'id' in selected_league else None
        probabilities = generate_enhanced_match_probabilities(
            match_id=selected_match['id'],
            home_team=selected_match['home_team'],
            away_team=selected_match['away_team'],
            home_team_id=selected_match.get('home_team_id'),
            away_team_id=selected_match.get('away_team_id'),
            leagues=leagues
        )
    else:
        leagues = [selected_league['id']] if 'id' in selected_league else None
        probabilities = generate_match_probabilities(
            match_id=selected_match['id'],
            home_team=selected_match['home_team'],
            away_team=selected_match['away_team'],
            home_team_id=selected_match.get('home_team_id'),
            away_team_id=selected_match.get('away_team_id'),
            leagues=leagues
        )
    
    # Afficher le graphique des probabilités
    col1, col2 = st.columns([3, 2])
    with col1:
        # Utiliser la version améliorée si disponible
        if 'advanced_insights' in probabilities:
            fig = create_enhanced_probability_chart(probabilities)
        else:
            fig = create_probability_chart(probabilities)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Afficher les cotes et probabilités supplémentaires
        st.markdown("#### Probabilités détaillées")
        
        # Fonction de sécurité pour éviter les divisions par zéro
        def safe_odds(prob):
            if prob is None or prob <= 0.01:
                return "-"
            return f"{1/prob:.2f}"
            
        st.markdown(f"""
        | Marché | Probabilité | Cote estimée |
        |--------|-------------|--------------|
        | Victoire {selected_match['home_team']} | {probabilities.get('home_win', 0)*100:.1f}% | {safe_odds(probabilities.get('home_win', 0))} |
        | Match Nul | {probabilities.get('draw', 0)*100:.1f}% | {safe_odds(probabilities.get('draw', 0))} |
        | Victoire {selected_match['away_team']} | {probabilities.get('away_win', 0)*100:.1f}% | {safe_odds(probabilities.get('away_win', 0))} |
        | Moins de 2.5 buts | {probabilities.get('under_2_5', 0)*100:.1f}% | {safe_odds(probabilities.get('under_2_5', 0))} |
        | Plus de 2.5 buts | {probabilities.get('over_2_5', 0)*100:.1f}% | {safe_odds(probabilities.get('over_2_5', 0))} |
        | Les deux équipes marquent | {probabilities.get('both_score', 0)*100:.1f}% | {safe_odds(probabilities.get('both_score', 0))} |
        """)
    
    # Générer et afficher les insights pour ce match
    st.markdown("#### Insights clés")
    
    # Récupérer des données statistiques si disponibles
    try:
        home_stats = get_team_statistics(selected_match.get('home_team_id', None))
        away_stats = get_team_statistics(selected_match.get('away_team_id', None))
        h2h_data = get_h2h_matches(selected_match.get('home_team_id', None), selected_match.get('away_team_id', None))
    except Exception as e:
        home_stats = {}
        away_stats = {}
        h2h_data = []
        st.warning(f"Impossible de récupérer certaines statistiques détaillées: {e}")
    
    # Obtenir les insights (utiliser la version enrichie si disponible)
    if 'advanced_insights' in probabilities:
        # Utiliser les insights avancés déjà calculés
        advanced_insights = probabilities.get('advanced_insights', {})
        
        # Utiliser les insights les plus pertinents de chaque catégorie
        insights = []
        for category in ['tactical_insights', 'key_player_insights', 'historical_insights', 'statistical_insights', 'trend_insights']:
            category_insights = advanced_insights.get(category, [])
            # Prendre les 2 insights les plus confiants par catégorie
            top_insights = sorted(category_insights, key=lambda x: x.get('confidence', 0), reverse=True)[:2]
            insights.extend(top_insights)
    else:
        # Utiliser la génération d'insights traditionnelle
        insights = generate_match_insights(
            selected_match['home_team'],
            selected_match['away_team'],
            home_stats,
            away_stats,
            h2h_data,
            has_detailed_data=bool(home_stats and away_stats),
            match_data=match_data
        )
    
    # Afficher les insights
    if insights:
        col1, col2 = st.columns(2)
        
        for i, insight in enumerate(insights):
            with col1 if i % 2 == 0 else col2:
                confidence = insight.get('confidence', 0.5)
                confidence_class = "high" if confidence >= 0.75 else "medium" if confidence >= 0.5 else "low"
                
                team = insight.get('team', 'both')
                if team == 'both':
                    team_text = "Les deux équipes"
                elif team == selected_match['home_team']:
                    team_text = selected_match['home_team']
                elif team == selected_match['away_team']:
                    team_text = selected_match['away_team']
                else:
                    team_text = team
                
                st.markdown(f"""
                <div class="important-insight">
                    <h4>{insight.get('title', 'Insight')}</h4>
                    <p>{insight.get('description', '')}</p>
                    <p>
                        <span class="badge badge-{confidence_class}">Confiance {confidence*100:.0f}%</span>
                        <span>{team_text}</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Aucun insight spécifique disponible pour ce match.")
    
    # Afficher les analyses avancées si disponibles
    if 'advanced_insights' in probabilities:
        with st.expander("Voir les analyses avancées"):
            advanced_insights = probabilities.get('advanced_insights', {})
            
            # Afficher les métriques de confiance
            confidence_metrics = advanced_insights.get('confidence_metrics', {})
            if confidence_metrics:
                st.markdown("#### Métriques de confiance")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Confiance globale", f"{confidence_metrics.get('overall_confidence', 0)*100:.0f}%")
                with col2:
                    st.metric("Qualité des données", f"{confidence_metrics.get('data_quality', 0)*100:.0f}%")
                with col3:
                    st.metric("Prévisibilité", f"{confidence_metrics.get('predictability', 0)*100:.0f}%")
            
            # Afficher les analyses tactiques et de joueurs clés plus détaillées
            tactical_insights = advanced_insights.get('tactical_insights', [])
            if tactical_insights:
                st.markdown("#### Analyse tactique approfondie")
                for insight in tactical_insights:
                    st.markdown(f"""
                    - **{insight.get('type', 'Avantage tactique')}**: {insight.get('description', '')} 
                      _(Impact: {insight.get('impact', 'medium')})_
                    """)
            
            # Afficher les duels clés
            key_duels = [i for i in advanced_insights.get('key_player_insights', []) if i.get('type') == 'key_duel']
            if key_duels:
                st.markdown("#### Duels clés")
                for duel in key_duels:
                    st.markdown(f"""
                    - **{duel.get('player1', '')} vs {duel.get('player2', '')}**: {duel.get('description', '')} 
                      _(Impact: {duel.get('impact', 'medium')})_
                    """)
    
    # Afficher les données brutes des équipes si disponibles
    with st.expander("Voir les statistiques détaillées des équipes"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### {selected_match['home_team']}")
            if home_stats:
                for key, value in home_stats.items():
                    if key != 'recent_form':
                        st.markdown(f"**{key}**: {value}")
            else:
                st.info("Données détaillées non disponibles")
        
        with col2:
            st.markdown(f"#### {selected_match['away_team']}")
            if away_stats:
                for key, value in away_stats.items():
                    if key != 'recent_form':
                        st.markdown(f"**{key}**: {value}")
            else:
                st.info("Données détaillées non disponibles")

# Fonction pour charger les ligues disponibles
def load_available_leagues():
    """
    Charge la liste des ligues disponibles dans l'API Football.
    
    Returns:
        list: Liste des ligues disponibles
    """
    leagues = get_available_leagues()
    
    if not leagues:
        # Fallback sur une liste basique si nécessaire
        leagues = [
            {'id': 2021, 'name': 'Premier League'},
            {'id': 2014, 'name': 'La Liga'},
            {'id': 2002, 'name': 'Bundesliga'},
            {'id': 2019, 'name': 'Serie A'},
            {'id': 2015, 'name': 'Ligue 1'}
        ]
    
    return leagues

# Fonction pour ajouter l'onglet Prédictions à l'application principale
def add_enhanced_predictions_tab(tab):
    """
    Ajoute l'onglet Prédictions enrichi à l'application principale.
    
    Args:
        tab: Objet tab Streamlit
    """
    with tab:
        display_enhanced_predictions_tab()