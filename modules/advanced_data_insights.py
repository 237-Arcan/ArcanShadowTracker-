"""
Module d'analyse avancée des données pour ArcanShadow.
Ce module utilise les données enrichies par les nouvelles sources (soccerdata, détails joueurs)
pour fournir des insights plus profonds pour les prédictions.
"""

import logging
from datetime import datetime
import pandas as pd
import numpy as np
import os
import json

# Importer notre nouveau hub d'intégration
try:
    from api.data_integration_hub import (
        get_data_integration_hub,
        enhance_match_data,
        get_player_details,
        get_team_details,
        get_league_standings,
        get_match_statistics,
        is_source_available,
        get_available_sources
    )
    DATA_HUB_AVAILABLE = True
except ImportError:
    DATA_HUB_AVAILABLE = False

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedDataInsights:
    """
    Classe d'analyse avancée qui exploite les données enrichies de multiples sources
    pour générer des insights plus précis et détaillés sur les matchs.
    """
    
    def __init__(self):
        """Initialise le système d'analyse avancée des données."""
        self.data_sources = self._check_data_sources()
        # Dossier pour stocker les modèles et les analyses
        self.models_dir = os.path.join(os.getcwd(), 'data', 'advanced_insights_models')
        os.makedirs(self.models_dir, exist_ok=True)
    
    def _check_data_sources(self):
        """
        Vérifie les sources de données disponibles.
        
        Returns:
            dict: Sources de données disponibles
        """
        data_sources = {}
        
        if DATA_HUB_AVAILABLE:
            hub = get_data_integration_hub()
            data_sources = hub.get_available_sources()
        else:
            logger.warning("Hub d'intégration de données non disponible")
            
            # Sources de base
            try:
                from api.transfermarkt_integration import is_transfermarkt_available
                data_sources['transfermarkt'] = is_transfermarkt_available()
            except ImportError:
                data_sources['transfermarkt'] = False
            
            # Nouvelles sources
            try:
                from api.soccerdata_integration import is_soccerdata_available
                data_sources['soccerdata'] = is_soccerdata_available()
            except ImportError:
                data_sources['soccerdata'] = False
            
            try:
                from api.player_data_enrichment import get_player_data_enrichment
                data_sources['player_enrichment'] = True
            except ImportError:
                data_sources['player_enrichment'] = False
        
        logger.info(f"Sources de données disponibles pour les insights avancés: {data_sources}")
        return data_sources
    
    def generate_match_insights(self, match_data):
        """
        Génère des insights avancés pour un match en utilisant toutes les sources disponibles.
        
        Args:
            match_data (dict): Données du match
            
        Returns:
            dict: Insights générés pour le match
        """
        insights = {
            'tactical_insights': [],
            'key_player_insights': [],
            'historical_insights': [],
            'statistical_insights': [],
            'trend_insights': [],
            'confidence_metrics': {}
        }
        
        # Enrichir les données du match si le hub est disponible
        if DATA_HUB_AVAILABLE:
            try:
                enhanced_match = enhance_match_data(match_data)
            except Exception as e:
                logger.error(f"Erreur lors de l'enrichissement des données du match: {e}")
                enhanced_match = match_data
        else:
            enhanced_match = match_data
        
        # 1. Insights tactiques
        tactical_insights = self._generate_tactical_insights(enhanced_match)
        if tactical_insights:
            insights['tactical_insights'].extend(tactical_insights)
        
        # 2. Insights sur les joueurs clés
        key_player_insights = self._generate_key_player_insights(enhanced_match)
        if key_player_insights:
            insights['key_player_insights'].extend(key_player_insights)
        
        # 3. Insights historiques
        historical_insights = self._generate_historical_insights(enhanced_match)
        if historical_insights:
            insights['historical_insights'].extend(historical_insights)
        
        # 4. Insights statistiques
        statistical_insights = self._generate_statistical_insights(enhanced_match)
        if statistical_insights:
            insights['statistical_insights'].extend(statistical_insights)
        
        # 5. Insights de tendance
        trend_insights = self._generate_trend_insights(enhanced_match)
        if trend_insights:
            insights['trend_insights'].extend(trend_insights)
        
        # 6. Métriques de confiance
        confidence_metrics = self._calculate_confidence_metrics(enhanced_match)
        if confidence_metrics:
            insights['confidence_metrics'] = confidence_metrics
        
        return insights
    
    def _generate_tactical_insights(self, match_data):
        """
        Génère des insights tactiques sur le match.
        
        Args:
            match_data (dict): Données enrichies du match
            
        Returns:
            list: Insights tactiques
        """
        tactical_insights = []
        
        # Utiliser les données détaillées des équipes si disponibles
        home_team_detailed = match_data.get('home_team_detailed', {})
        away_team_detailed = match_data.get('away_team_detailed', {})
        
        # Analyse des formations et styles de jeu
        if home_team_detailed and 'detailed_manager' in home_team_detailed:
            home_manager = home_team_detailed['detailed_manager']
            if 'preferred_formation' in home_manager and home_manager['preferred_formation']:
                tactical_insights.append({
                    'type': 'formation',
                    'team': match_data.get('home_team', ''),
                    'description': f"Formation préférée : {home_manager['preferred_formation']}",
                    'impact': 'medium',
                    'confidence': 0.75
                })
        
        if away_team_detailed and 'detailed_manager' in away_team_detailed:
            away_manager = away_team_detailed['detailed_manager']
            if 'preferred_formation' in away_manager and away_manager['preferred_formation']:
                tactical_insights.append({
                    'type': 'formation',
                    'team': match_data.get('away_team', ''),
                    'description': f"Formation préférée : {away_manager['preferred_formation']}",
                    'impact': 'medium',
                    'confidence': 0.75
                })
        
        # Analyse des styles de jeu et matchups tactiques
        if home_team_detailed and away_team_detailed:
            # Comparer les forces et faiblesses des deux équipes
            home_strengths = self._extract_team_strengths(home_team_detailed)
            away_strengths = self._extract_team_strengths(away_team_detailed)
            
            # Identifier les avantages tactiques
            tactical_advantages = self._identify_tactical_advantages(
                home_strengths, away_strengths,
                match_data.get('home_team', ''),
                match_data.get('away_team', '')
            )
            
            tactical_insights.extend(tactical_advantages)
        
        return tactical_insights
    
    def _extract_team_strengths(self, team_data):
        """
        Extrait les forces d'une équipe à partir des données détaillées.
        
        Args:
            team_data (dict): Données détaillées de l'équipe
            
        Returns:
            dict: Forces de l'équipe par catégorie
        """
        strengths = {
            'attacking': 0,
            'midfield': 0,
            'defense': 0,
            'set_pieces': 0,
            'counterattack': 0,
            'possession': 0
        }
        
        # Analyser les joueurs détaillés si disponibles
        if 'detailed_players' in team_data:
            for player in team_data['detailed_players']:
                # Joueurs offensifs
                if player['position'] in ['Attaquant', 'Ailier', 'Forward', 'Striker', 'Winger']:
                    # Analyser les forces des attaquants
                    attacking_rating = 0
                    for key, value in player.get('strength_ratings', {}).items():
                        if key in ['goals_per90', 'xg_per90', 'attacking_finishing', 'dribbles_completed', 'shooting']:
                            attacking_rating += value
                    
                    if attacking_rating > 0:
                        strengths['attacking'] += attacking_rating / 5  # Normaliser
                
                # Milieux de terrain
                elif player['position'] in ['Milieu', 'Milieu central', 'Midfielder', 'Central Midfielder']:
                    # Analyser les forces des milieux
                    midfield_rating = 0
                    for key, value in player.get('strength_ratings', {}).items():
                        if key in ['passes_completed', 'passes_pct', 'progressive_passes', 'skill_long_passing', 'passing']:
                            midfield_rating += value
                    
                    if midfield_rating > 0:
                        strengths['midfield'] += midfield_rating / 5  # Normaliser
                        
                    # Contribution à la possession
                    possession_rating = 0
                    for key, value in player.get('strength_ratings', {}).items():
                        if key in ['passes_pct', 'skill_ball_control', 'dribbling']:
                            possession_rating += value
                    
                    if possession_rating > 0:
                        strengths['possession'] += possession_rating / 3  # Normaliser
                
                # Défenseurs
                elif player['position'] in ['Défenseur', 'Défenseur central', 'Defender', 'Centre-Back']:
                    # Analyser les forces des défenseurs
                    defense_rating = 0
                    for key, value in player.get('strength_ratings', {}).items():
                        if key in ['tackles', 'interceptions', 'blocks', 'clearances', 'defending']:
                            defense_rating += value
                    
                    if defense_rating > 0:
                        strengths['defense'] += defense_rating / 5  # Normaliser
                    
                    # Contribution aux coups de pied arrêtés (grandes tailles)
                    if player.get('height', 0) > 185:  # Plus de 1m85
                        strengths['set_pieces'] += 1
        
        # Normaliser les valeurs par le nombre de joueurs (estimation)
        num_players = len(team_data.get('detailed_players', []))
        if num_players > 0:
            strengths['attacking'] /= max(1, num_players / 4)
            strengths['midfield'] /= max(1, num_players / 4)
            strengths['defense'] /= max(1, num_players / 4)
            strengths['set_pieces'] /= max(1, num_players / 4)
            strengths['possession'] /= max(1, num_players / 4)
        
        # Analyser le manager si disponible
        if 'detailed_manager' in team_data:
            manager = team_data['detailed_manager']
            
            # Influence du style de jeu du manager
            if manager.get('playing_style') == 'Possession':
                strengths['possession'] *= 1.2
            elif manager.get('playing_style') == 'Counter-attack':
                strengths['counterattack'] *= 1.2
        
        return strengths
    
    def _identify_tactical_advantages(self, home_strengths, away_strengths, home_team, away_team):
        """
        Identifie les avantages tactiques entre deux équipes.
        
        Args:
            home_strengths (dict): Forces de l'équipe à domicile
            away_strengths (dict): Forces de l'équipe à l'extérieur
            home_team (str): Nom de l'équipe à domicile
            away_team (str): Nom de l'équipe à l'extérieur
            
        Returns:
            list: Insights sur les avantages tactiques
        """
        advantages = []
        
        # Comparer les forces par catégorie
        categories = ['attacking', 'midfield', 'defense', 'set_pieces', 'counterattack', 'possession']
        category_names = {
            'attacking': 'attaque',
            'midfield': 'milieu de terrain',
            'defense': 'défense',
            'set_pieces': 'coups de pied arrêtés',
            'counterattack': 'contre-attaque',
            'possession': 'possession'
        }
        
        for category in categories:
            home_strength = home_strengths.get(category, 0)
            away_strength = away_strengths.get(category, 0)
            
            # Seuil de différence significative
            threshold = 1.5
            
            if home_strength > away_strength * threshold:
                advantages.append({
                    'type': 'tactical_advantage',
                    'team': home_team,
                    'category': category_names.get(category, category),
                    'description': f"Avantage significatif en {category_names.get(category, category)} pour {home_team}",
                    'impact': 'high',
                    'confidence': min(0.9, home_strength / (away_strength + 0.1))
                })
            elif away_strength > home_strength * threshold:
                advantages.append({
                    'type': 'tactical_advantage',
                    'team': away_team,
                    'category': category_names.get(category, category),
                    'description': f"Avantage significatif en {category_names.get(category, category)} pour {away_team}",
                    'impact': 'high',
                    'confidence': min(0.9, away_strength / (home_strength + 0.1))
                })
        
        return advantages
    
    def _generate_key_player_insights(self, match_data):
        """
        Génère des insights sur les joueurs clés du match.
        
        Args:
            match_data (dict): Données enrichies du match
            
        Returns:
            list: Insights sur les joueurs clés
        """
        key_player_insights = []
        
        # Utiliser les données détaillées des équipes si disponibles
        home_team_detailed = match_data.get('home_team_detailed', {})
        away_team_detailed = match_data.get('away_team_detailed', {})
        
        # Analyse des joueurs clés de l'équipe à domicile
        if home_team_detailed and 'detailed_players' in home_team_detailed:
            home_key_players = self._identify_key_players(
                home_team_detailed['detailed_players'],
                match_data.get('home_team', '')
            )
            key_player_insights.extend(home_key_players)
        
        # Analyse des joueurs clés de l'équipe à l'extérieur
        if away_team_detailed and 'detailed_players' in away_team_detailed:
            away_key_players = self._identify_key_players(
                away_team_detailed['detailed_players'],
                match_data.get('away_team', '')
            )
            key_player_insights.extend(away_key_players)
        
        # Analyse des duels clés entre joueurs
        if home_team_detailed and away_team_detailed and 'detailed_players' in home_team_detailed and 'detailed_players' in away_team_detailed:
            key_duels = self._identify_key_duels(
                home_team_detailed['detailed_players'],
                away_team_detailed['detailed_players'],
                match_data.get('home_team', ''),
                match_data.get('away_team', '')
            )
            key_player_insights.extend(key_duels)
        
        return key_player_insights
    
    def _identify_key_players(self, players, team_name):
        """
        Identifie les joueurs clés d'une équipe.
        
        Args:
            players (list): Liste des joueurs détaillés
            team_name (str): Nom de l'équipe
            
        Returns:
            list: Insights sur les joueurs clés
        """
        key_player_insights = []
        
        # Calculer un score d'impact pour chaque joueur
        player_scores = []
        for player in players:
            impact_score = 0
            
            # Facteurs contribuant au score d'impact
            if player.get('goals', 0) > 0:
                impact_score += player['goals'] * 2
            
            if player.get('assists', 0) > 0:
                impact_score += player['assists'] * 1.5
            
            if player.get('minutes_played', 0) > 0:
                impact_score += player['minutes_played'] / 1000
            
            # Forces spécifiques
            for key, value in player.get('strength_ratings', {}).items():
                if key in ['goals_per90', 'xg_per90', 'attacking_finishing', 'skill_ball_control', 'skill_fk_accuracy']:
                    impact_score += value / 10
            
            # Valeur marchande (indicateur de qualité)
            if player.get('market_value'):
                try:
                    # Convertir en nombre si c'est une chaîne
                    if isinstance(player['market_value'], str):
                        if 'M' in player['market_value']:
                            market_value = float(player['market_value'].replace('M', '').replace('€', '')) * 1000000
                        elif 'K' in player['market_value']:
                            market_value = float(player['market_value'].replace('K', '').replace('€', '')) * 1000
                        else:
                            market_value = float(player['market_value'].replace('€', ''))
                    else:
                        market_value = player['market_value']
                    
                    impact_score += market_value / 10000000  # 10M€ = +1 point
                except (ValueError, TypeError):
                    pass
            
            player_scores.append((player, impact_score))
        
        # Trier par score d'impact décroissant
        player_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Sélectionner les 3 meilleurs joueurs
        top_players = player_scores[:3]
        
        for player, score in top_players:
            if score > 1:  # Seuil minimal pour être considéré comme joueur clé
                # Déterminer le type d'impact
                impact_types = []
                
                if player.get('goals', 0) > 0 or player.get('assists', 0) > 0:
                    impact_types.append('offensif')
                
                if player.get('position') in ['Défenseur', 'Défenseur central', 'Defender', 'Centre-Back']:
                    impact_types.append('défensif')
                
                if player.get('position') in ['Milieu', 'Milieu central', 'Midfielder', 'Central Midfielder']:
                    impact_types.append('organisateur')
                
                # Combiner les types d'impact
                impact_description = ' et '.join(impact_types) if impact_types else 'global'
                
                key_player_insights.append({
                    'type': 'key_player',
                    'team': team_name,
                    'player_name': player['name'],
                    'position': player.get('position', ''),
                    'description': f"Joueur clé à impact {impact_description}",
                    'impact_score': score,
                    'impact': 'high',
                    'confidence': min(0.9, score / 10)
                })
        
        return key_player_insights
    
    def _identify_key_duels(self, home_players, away_players, home_team, away_team):
        """
        Identifie les duels clés entre joueurs des deux équipes.
        
        Args:
            home_players (list): Liste des joueurs détaillés de l'équipe à domicile
            away_players (list): Liste des joueurs détaillés de l'équipe à l'extérieur
            home_team (str): Nom de l'équipe à domicile
            away_team (str): Nom de l'équipe à l'extérieur
            
        Returns:
            list: Insights sur les duels clés
        """
        key_duels = []
        
        # Regrouper les joueurs par position
        home_by_position = {}
        away_by_position = {}
        
        position_mapping = {
            # Attaquants
            'Attaquant': 'forward',
            'Ailier': 'forward',
            'Forward': 'forward',
            'Striker': 'forward',
            'Winger': 'forward',
            # Milieux
            'Milieu': 'midfield',
            'Milieu central': 'midfield',
            'Midfielder': 'midfield',
            'Central Midfielder': 'midfield',
            # Défenseurs
            'Défenseur': 'defense',
            'Défenseur central': 'defense',
            'Defender': 'defense',
            'Centre-Back': 'defense',
            # Gardiens
            'Gardien': 'goalkeeper',
            'Goalkeeper': 'goalkeeper'
        }
        
        # Classer les joueurs par position
        for player in home_players:
            pos = player.get('position', '')
            group = position_mapping.get(pos, 'other')
            if group not in home_by_position:
                home_by_position[group] = []
            home_by_position[group].append(player)
        
        for player in away_players:
            pos = player.get('position', '')
            group = position_mapping.get(pos, 'other')
            if group not in away_by_position:
                away_by_position[group] = []
            away_by_position[group].append(player)
        
        # Identifier les duels potentiels
        if 'forward' in home_by_position and 'defense' in away_by_position:
            # Attaquants domicile vs défenseurs extérieur
            top_forward = max(home_by_position['forward'], key=lambda p: p.get('goals', 0) + p.get('assists', 0), default=None)
            top_defender = max(away_by_position['defense'], key=lambda p: p.get('minutes_played', 0), default=None)
            
            if top_forward and top_defender:
                key_duels.append({
                    'type': 'key_duel',
                    'player1': f"{top_forward['name']} ({home_team})",
                    'player2': f"{top_defender['name']} ({away_team})",
                    'description': f"Duel clé entre l'attaquant {top_forward['name']} et le défenseur {top_defender['name']}",
                    'impact': 'high',
                    'confidence': 0.7
                })
        
        if 'forward' in away_by_position and 'defense' in home_by_position:
            # Attaquants extérieur vs défenseurs domicile
            top_forward = max(away_by_position['forward'], key=lambda p: p.get('goals', 0) + p.get('assists', 0), default=None)
            top_defender = max(home_by_position['defense'], key=lambda p: p.get('minutes_played', 0), default=None)
            
            if top_forward and top_defender:
                key_duels.append({
                    'type': 'key_duel',
                    'player1': f"{top_forward['name']} ({away_team})",
                    'player2': f"{top_defender['name']} ({home_team})",
                    'description': f"Duel clé entre l'attaquant {top_forward['name']} et le défenseur {top_defender['name']}",
                    'impact': 'high',
                    'confidence': 0.7
                })
        
        if 'midfield' in home_by_position and 'midfield' in away_by_position:
            # Duel de milieux de terrain
            top_home_mid = max(home_by_position['midfield'], key=lambda p: sum(p.get('strength_ratings', {}).values()), default=None)
            top_away_mid = max(away_by_position['midfield'], key=lambda p: sum(p.get('strength_ratings', {}).values()), default=None)
            
            if top_home_mid and top_away_mid:
                key_duels.append({
                    'type': 'key_duel',
                    'player1': f"{top_home_mid['name']} ({home_team})",
                    'player2': f"{top_away_mid['name']} ({away_team})",
                    'description': f"Bataille au milieu entre {top_home_mid['name']} et {top_away_mid['name']}",
                    'impact': 'medium',
                    'confidence': 0.6
                })
        
        return key_duels
    
    def _generate_historical_insights(self, match_data):
        """
        Génère des insights historiques sur le match.
        
        Args:
            match_data (dict): Données enrichies du match
            
        Returns:
            list: Insights historiques
        """
        historical_insights = []
        
        # Utiliser les données de forme des équipes si disponibles
        home_form = match_data.get('home_team_form', {})
        away_form = match_data.get('away_team_form', {})
        
        if home_form and isinstance(home_form, dict) and 'data' in home_form:
            form_data = pd.DataFrame(home_form['data'])
            
            if not form_data.empty and 'result' in form_data.columns:
                # Analyser la forme récente
                win_count = sum(form_data['result'] == 'W')
                draw_count = sum(form_data['result'] == 'D')
                loss_count = sum(form_data['result'] == 'L')
                
                form_description = ""
                if win_count >= 3:
                    form_description = "excellente forme avec plusieurs victoires récentes"
                    confidence = 0.8
                    impact = 'high'
                elif win_count >= 2:
                    form_description = "bonne dynamique récente"
                    confidence = 0.7
                    impact = 'medium'
                elif loss_count >= 3:
                    form_description = "série de défaites préoccupante"
                    confidence = 0.8
                    impact = 'high'
                elif loss_count >= 2:
                    form_description = "difficultés récentes"
                    confidence = 0.7
                    impact = 'medium'
                
                if form_description:
                    historical_insights.append({
                        'type': 'recent_form',
                        'team': match_data.get('home_team', ''),
                        'description': f"{match_data.get('home_team', '')} montre une {form_description}",
                        'details': f"{win_count}V-{draw_count}N-{loss_count}D sur les derniers matchs",
                        'impact': impact,
                        'confidence': confidence
                    })
        
        if away_form and isinstance(away_form, dict) and 'data' in away_form:
            form_data = pd.DataFrame(away_form['data'])
            
            if not form_data.empty and 'result' in form_data.columns:
                # Analyser la forme récente
                win_count = sum(form_data['result'] == 'W')
                draw_count = sum(form_data['result'] == 'D')
                loss_count = sum(form_data['result'] == 'L')
                
                form_description = ""
                if win_count >= 3:
                    form_description = "excellente forme avec plusieurs victoires récentes"
                    confidence = 0.8
                    impact = 'high'
                elif win_count >= 2:
                    form_description = "bonne dynamique récente"
                    confidence = 0.7
                    impact = 'medium'
                elif loss_count >= 3:
                    form_description = "série de défaites préoccupante"
                    confidence = 0.8
                    impact = 'high'
                elif loss_count >= 2:
                    form_description = "difficultés récentes"
                    confidence = 0.7
                    impact = 'medium'
                
                if form_description:
                    historical_insights.append({
                        'type': 'recent_form',
                        'team': match_data.get('away_team', ''),
                        'description': f"{match_data.get('away_team', '')} montre une {form_description}",
                        'details': f"{win_count}V-{draw_count}N-{loss_count}D sur les derniers matchs",
                        'impact': impact,
                        'confidence': confidence
                    })
        
        # Analyser les confrontations directes si disponibles
        if 'soccerdata_match_stats' in match_data and 'h2h' in match_data['soccerdata_match_stats']:
            h2h_data = match_data['soccerdata_match_stats']['h2h']
            
            if h2h_data and isinstance(h2h_data, list):
                home_wins = sum(1 for match in h2h_data if match.get('home_score', 0) > match.get('away_score', 0) and match.get('home_team') == match_data.get('home_team'))
                away_wins = sum(1 for match in h2h_data if match.get('away_score', 0) > match.get('home_score', 0) and match.get('away_team') == match_data.get('away_team'))
                draws = sum(1 for match in h2h_data if match.get('home_score', 0) == match.get('away_score', 0))
                
                if home_wins + away_wins + draws > 0:
                    h2h_description = ""
                    if home_wins > away_wins + draws:
                        h2h_description = f"avantage historique pour {match_data.get('home_team', '')}"
                        confidence = 0.7
                        impact = 'medium'
                    elif away_wins > home_wins + draws:
                        h2h_description = f"avantage historique pour {match_data.get('away_team', '')}"
                        confidence = 0.7
                        impact = 'medium'
                    elif home_wins == away_wins and home_wins > 0:
                        h2h_description = "équilibre parfait dans les confrontations directes"
                        confidence = 0.6
                        impact = 'low'
                    
                    if h2h_description:
                        historical_insights.append({
                            'type': 'head_to_head',
                            'description': f"Historique des confrontations: {h2h_description}",
                            'details': f"{home_wins}V-{draws}N-{away_wins}D pour {match_data.get('home_team', '')}",
                            'impact': impact,
                            'confidence': confidence
                        })
        
        return historical_insights
    
    def _generate_statistical_insights(self, match_data):
        """
        Génère des insights statistiques sur le match.
        
        Args:
            match_data (dict): Données enrichies du match
            
        Returns:
            list: Insights statistiques
        """
        statistical_insights = []
        
        # Utiliser les statistiques détaillées des équipes si disponibles
        if 'home_team_detailed' in match_data and 'stats' in match_data['home_team_detailed']:
            home_stats = match_data['home_team_detailed']['stats']
            
            # Analyser les statistiques offensives
            if isinstance(home_stats, dict) and 'data' in home_stats:
                stats_data = pd.DataFrame(home_stats['data'])
                
                if not stats_data.empty:
                    # Analyser les buts marqués
                    if 'goals' in stats_data.columns:
                        goals_per_game = stats_data['goals'].mean()
                        
                        if goals_per_game > 2:
                            statistical_insights.append({
                                'type': 'offensive_power',
                                'team': match_data.get('home_team', ''),
                                'description': f"{match_data.get('home_team', '')} marque en moyenne {goals_per_game:.1f} buts par match",
                                'impact': 'high',
                                'confidence': 0.8
                            })
                    
                    # Analyser les buts encaissés
                    if 'goals_against' in stats_data.columns:
                        goals_against_per_game = stats_data['goals_against'].mean()
                        
                        if goals_against_per_game < 1:
                            statistical_insights.append({
                                'type': 'defensive_strength',
                                'team': match_data.get('home_team', ''),
                                'description': f"{match_data.get('home_team', '')} n'encaisse en moyenne que {goals_against_per_game:.1f} buts par match",
                                'impact': 'high',
                                'confidence': 0.8
                            })
        
        if 'away_team_detailed' in match_data and 'stats' in match_data['away_team_detailed']:
            away_stats = match_data['away_team_detailed']['stats']
            
            # Analyser les statistiques offensives
            if isinstance(away_stats, dict) and 'data' in away_stats:
                stats_data = pd.DataFrame(away_stats['data'])
                
                if not stats_data.empty:
                    # Analyser les buts marqués
                    if 'goals' in stats_data.columns:
                        goals_per_game = stats_data['goals'].mean()
                        
                        if goals_per_game > 2:
                            statistical_insights.append({
                                'type': 'offensive_power',
                                'team': match_data.get('away_team', ''),
                                'description': f"{match_data.get('away_team', '')} marque en moyenne {goals_per_game:.1f} buts par match",
                                'impact': 'high',
                                'confidence': 0.8
                            })
                    
                    # Analyser les buts encaissés
                    if 'goals_against' in stats_data.columns:
                        goals_against_per_game = stats_data['goals_against'].mean()
                        
                        if goals_against_per_game < 1:
                            statistical_insights.append({
                                'type': 'defensive_strength',
                                'team': match_data.get('away_team', ''),
                                'description': f"{match_data.get('away_team', '')} n'encaisse en moyenne que {goals_against_per_game:.1f} buts par match",
                                'impact': 'high',
                                'confidence': 0.8
                            })
        
        # Analyser les classements Elo si disponibles
        if 'home_team_elo' in match_data and 'away_team_elo' in match_data:
            home_elo = match_data['home_team_elo']
            away_elo = match_data['away_team_elo']
            
            if home_elo and away_elo:
                elo_diff = home_elo - away_elo
                
                if abs(elo_diff) > 100:
                    team = match_data.get('home_team', '') if elo_diff > 0 else match_data.get('away_team', '')
                    statistical_insights.append({
                        'type': 'elo_advantage',
                        'team': team,
                        'description': f"Avantage significatif au classement Elo pour {team}",
                        'details': f"Différence de {abs(elo_diff):.0f} points Elo",
                        'impact': 'high',
                        'confidence': min(0.9, abs(elo_diff) / 300)
                    })
        
        return statistical_insights
    
    def _generate_trend_insights(self, match_data):
        """
        Génère des insights sur les tendances observées.
        
        Args:
            match_data (dict): Données enrichies du match
            
        Returns:
            list: Insights sur les tendances
        """
        trend_insights = []
        
        # Analyser les tendances de buts si des statistiques sont disponibles
        goal_trends = self._analyze_goal_trends(match_data)
        if goal_trends:
            trend_insights.extend(goal_trends)
        
        # Analyser les tendances à domicile/extérieur
        home_away_trends = self._analyze_home_away_trends(match_data)
        if home_away_trends:
            trend_insights.extend(home_away_trends)
        
        return trend_insights
    
    def _analyze_goal_trends(self, match_data):
        """
        Analyse les tendances en termes de buts pour le match.
        
        Args:
            match_data (dict): Données enrichies du match
            
        Returns:
            list: Insights sur les tendances de buts
        """
        goal_trends = []
        
        # Analyser les tendances de buts à partir des formes récentes
        if 'home_team_form' in match_data and isinstance(match_data['home_team_form'], dict) and 'data' in match_data['home_team_form']:
            home_form = pd.DataFrame(match_data['home_team_form']['data'])
            
            if not home_form.empty and 'home_score' in home_form.columns and 'away_score' in home_form.columns:
                # Calculer les tendances pour les matchs récents
                total_goals = home_form['home_score'] + home_form['away_score']
                avg_goals = total_goals.mean()
                
                if avg_goals > 3:
                    goal_trends.append({
                        'type': 'goal_trend',
                        'team': match_data.get('home_team', ''),
                        'description': f"Les matchs récents de {match_data.get('home_team', '')} produisent beaucoup de buts",
                        'details': f"Moyenne de {avg_goals:.1f} buts par match",
                        'impact': 'medium',
                        'confidence': 0.7
                    })
                elif avg_goals < 1.5:
                    goal_trends.append({
                        'type': 'goal_trend',
                        'team': match_data.get('home_team', ''),
                        'description': f"Les matchs récents de {match_data.get('home_team', '')} produisent peu de buts",
                        'details': f"Moyenne de {avg_goals:.1f} buts par match",
                        'impact': 'medium',
                        'confidence': 0.7
                    })
        
        if 'away_team_form' in match_data and isinstance(match_data['away_team_form'], dict) and 'data' in match_data['away_team_form']:
            away_form = pd.DataFrame(match_data['away_team_form']['data'])
            
            if not away_form.empty and 'home_score' in away_form.columns and 'away_score' in away_form.columns:
                # Calculer les tendances pour les matchs récents
                total_goals = away_form['home_score'] + away_form['away_score']
                avg_goals = total_goals.mean()
                
                if avg_goals > 3:
                    goal_trends.append({
                        'type': 'goal_trend',
                        'team': match_data.get('away_team', ''),
                        'description': f"Les matchs récents de {match_data.get('away_team', '')} produisent beaucoup de buts",
                        'details': f"Moyenne de {avg_goals:.1f} buts par match",
                        'impact': 'medium',
                        'confidence': 0.7
                    })
                elif avg_goals < 1.5:
                    goal_trends.append({
                        'type': 'goal_trend',
                        'team': match_data.get('away_team', ''),
                        'description': f"Les matchs récents de {match_data.get('away_team', '')} produisent peu de buts",
                        'details': f"Moyenne de {avg_goals:.1f} buts par match",
                        'impact': 'medium',
                        'confidence': 0.7
                    })
        
        return goal_trends
    
    def _analyze_home_away_trends(self, match_data):
        """
        Analyse les tendances à domicile/extérieur pour le match.
        
        Args:
            match_data (dict): Données enrichies du match
            
        Returns:
            list: Insights sur les tendances à domicile/extérieur
        """
        home_away_trends = []
        
        # Analyser les performances à domicile de l'équipe qui joue à domicile
        if 'home_team_form' in match_data and isinstance(match_data['home_team_form'], dict) and 'data' in match_data['home_team_form']:
            home_form = pd.DataFrame(match_data['home_team_form']['data'])
            
            if not home_form.empty and 'home_team' in home_form.columns and 'result' in home_form.columns:
                # Filtrer uniquement les matchs à domicile
                home_matches = home_form[home_form['home_team'] == match_data.get('home_team', '')]
                
                if not home_matches.empty:
                    home_wins = sum(home_matches['result'] == 'W')
                    home_draws = sum(home_matches['result'] == 'D')
                    home_losses = sum(home_matches['result'] == 'L')
                    
                    if home_wins > home_draws + home_losses:
                        home_away_trends.append({
                            'type': 'home_advantage',
                            'team': match_data.get('home_team', ''),
                            'description': f"{match_data.get('home_team', '')} est très performant à domicile",
                            'details': f"{home_wins}V-{home_draws}N-{home_losses}D à domicile",
                            'impact': 'high',
                            'confidence': 0.8
                        })
        
        # Analyser les performances à l'extérieur de l'équipe qui joue à l'extérieur
        if 'away_team_form' in match_data and isinstance(match_data['away_team_form'], dict) and 'data' in match_data['away_team_form']:
            away_form = pd.DataFrame(match_data['away_team_form']['data'])
            
            if not away_form.empty and 'away_team' in away_form.columns and 'result' in away_form.columns:
                # Filtrer uniquement les matchs à l'extérieur
                away_matches = away_form[away_form['away_team'] == match_data.get('away_team', '')]
                
                if not away_matches.empty:
                    away_wins = sum(away_matches['result'] == 'W')
                    away_draws = sum(away_matches['result'] == 'D')
                    away_losses = sum(away_matches['result'] == 'L')
                    
                    if away_wins > away_draws + away_losses:
                        home_away_trends.append({
                            'type': 'away_strength',
                            'team': match_data.get('away_team', ''),
                            'description': f"{match_data.get('away_team', '')} est très performant à l'extérieur",
                            'details': f"{away_wins}V-{away_draws}N-{away_losses}D à l'extérieur",
                            'impact': 'high',
                            'confidence': 0.8
                        })
        
        return home_away_trends
    
    def _calculate_confidence_metrics(self, match_data):
        """
        Calcule des métriques de confiance pour les prédictions.
        
        Args:
            match_data (dict): Données enrichies du match
            
        Returns:
            dict: Métriques de confiance
        """
        confidence_metrics = {
            'overall_confidence': 0.0,
            'data_quality': 0.0,
            'predictability': 0.0,
            'source_reliability': 0.0
        }
        
        # Évaluer la qualité des données
        data_quality = 0.5  # Base par défaut
        
        # Vérifier la disponibilité des différentes sources de données
        sources_count = 0
        sources_available = 0
        
        # Transfermarkt
        sources_count += 1
        if 'home_team_transfermarkt_data' in match_data and 'away_team_transfermarkt_data' in match_data:
            sources_available += 1
            data_quality += 0.1
        
        # soccerdata
        sources_count += 1
        if 'soccerdata_match_stats' in match_data:
            sources_available += 1
            data_quality += 0.1
        
        # Données de forme
        sources_count += 1
        if 'home_team_form' in match_data and 'away_team_form' in match_data:
            sources_available += 1
            data_quality += 0.1
        
        # Données Elo
        sources_count += 1
        if 'home_team_elo' in match_data and 'away_team_elo' in match_data:
            sources_available += 1
            data_quality += 0.1
        
        # Données détaillées des joueurs
        sources_count += 1
        if 'home_team_detailed' in match_data and 'away_team_detailed' in match_data:
            if 'detailed_players' in match_data['home_team_detailed'] and 'detailed_players' in match_data['away_team_detailed']:
                sources_available += 1
                data_quality += 0.1
        
        # Normaliser la qualité des données
        if sources_count > 0:
            source_reliability = sources_available / sources_count
            confidence_metrics['source_reliability'] = source_reliability
        
        confidence_metrics['data_quality'] = min(1.0, data_quality)
        
        # Évaluer la prévisibilité du match
        predictability = 0.5  # Base par défaut
        
        # Les matchs sont généralement plus prévisibles si :
        # - Il y a une grande différence de niveau entre les équipes
        # - Les équipes ont des formes récentes très différentes
        # - Il y a un fort avantage à domicile/extérieur
        
        # Différence de niveau (Elo)
        if 'home_team_elo' in match_data and 'away_team_elo' in match_data:
            home_elo = match_data['home_team_elo']
            away_elo = match_data['away_team_elo']
            
            if home_elo and away_elo:
                elo_diff = abs(home_elo - away_elo)
                
                # Plus la différence est grande, plus le match est prévisible
                if elo_diff > 200:
                    predictability += 0.2
                elif elo_diff > 100:
                    predictability += 0.1
                elif elo_diff < 50:
                    predictability -= 0.1  # Moins prévisible si les équipes sont proches
        
        # Forme récente
        home_wins = away_wins = home_losses = away_losses = 0
        
        if 'home_team_form' in match_data and isinstance(match_data['home_team_form'], dict) and 'data' in match_data['home_team_form']:
            home_form = pd.DataFrame(match_data['home_team_form']['data'])
            
            if not home_form.empty and 'result' in home_form.columns:
                home_wins = sum(home_form['result'] == 'W')
                home_losses = sum(home_form['result'] == 'L')
        
        if 'away_team_form' in match_data and isinstance(match_data['away_team_form'], dict) and 'data' in match_data['away_team_form']:
            away_form = pd.DataFrame(match_data['away_team_form']['data'])
            
            if not away_form.empty and 'result' in away_form.columns:
                away_wins = sum(away_form['result'] == 'W')
                away_losses = sum(away_form['result'] == 'L')
        
        # Grande différence de forme
        form_diff = abs((home_wins - home_losses) - (away_wins - away_losses))
        if form_diff >= 4:
            predictability += 0.2
        elif form_diff >= 2:
            predictability += 0.1
        
        confidence_metrics['predictability'] = min(1.0, predictability)
        
        # Calculer la confiance globale
        confidence_metrics['overall_confidence'] = (
            confidence_metrics['data_quality'] * 0.4 +
            confidence_metrics['predictability'] * 0.4 +
            confidence_metrics['source_reliability'] * 0.2
        )
        
        return confidence_metrics
    
    def generate_team_insights(self, team_name):
        """
        Génère des insights avancés pour une équipe spécifique.
        
        Args:
            team_name (str): Nom de l'équipe
            
        Returns:
            dict: Insights générés pour l'équipe
        """
        insights = {
            'team_strengths': [],
            'team_weaknesses': [],
            'key_players': [],
            'tactical_analysis': [],
            'historical_trends': [],
            'confidence_metrics': {}
        }
        
        # Récupérer les données détaillées de l'équipe si le hub est disponible
        if DATA_HUB_AVAILABLE:
            try:
                team_details = get_team_details(team_name)
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des détails de l'équipe: {e}")
                team_details = {'team_name': team_name}
        else:
            team_details = {'team_name': team_name}
        
        # 1. Forces de l'équipe
        team_strengths = self._analyze_team_strengths(team_details)
        if team_strengths:
            insights['team_strengths'].extend(team_strengths)
        
        # 2. Faiblesses de l'équipe
        team_weaknesses = self._analyze_team_weaknesses(team_details)
        if team_weaknesses:
            insights['team_weaknesses'].extend(team_weaknesses)
        
        # 3. Joueurs clés
        if 'detailed_players' in team_details:
            key_players = self._identify_key_players(team_details['detailed_players'], team_name)
            if key_players:
                insights['key_players'].extend(key_players)
        
        # 4. Analyse tactique
        if 'detailed_manager' in team_details:
            tactical_analysis = self._analyze_team_tactics(team_details)
            if tactical_analysis:
                insights['tactical_analysis'].extend(tactical_analysis)
        
        # 5. Tendances historiques
        if 'form' in team_details:
            historical_trends = self._analyze_team_historical_trends(team_details)
            if historical_trends:
                insights['historical_trends'].extend(historical_trends)
        
        # 6. Métriques de confiance
        confidence_metrics = self._calculate_team_confidence_metrics(team_details)
        if confidence_metrics:
            insights['confidence_metrics'] = confidence_metrics
        
        return insights
    
    def _analyze_team_strengths(self, team_details):
        """
        Analyse les forces d'une équipe.
        
        Args:
            team_details (dict): Données détaillées de l'équipe
            
        Returns:
            list: Forces identifiées
        """
        team_strengths = []
        
        # Extraire les forces à partir des données détaillées
        strengths = self._extract_team_strengths(team_details)
        
        # Convertir en insights
        strength_thresholds = [
            ('attacking', 2.5, 'Puissance offensive', 'L\'équipe possède une attaque redoutable'),
            ('midfield', 2.5, 'Contrôle du milieu', 'Domination au milieu de terrain'),
            ('defense', 2.5, 'Solidité défensive', 'Défense particulièrement solide'),
            ('set_pieces', 2.0, 'Coups de pied arrêtés', 'Efficacité sur les coups de pied arrêtés'),
            ('counterattack', 2.0, 'Contre-attaques', 'Dangereuse en contre-attaque'),
            ('possession', 2.5, 'Possession de balle', 'Maîtrise de la possession')
        ]
        
        for category, threshold, title, description in strength_thresholds:
            if category in strengths and strengths[category] >= threshold:
                team_strengths.append({
                    'type': category,
                    'title': title,
                    'description': description,
                    'value': strengths[category],
                    'confidence': min(0.9, strengths[category] / 4)
                })
        
        # Ajouter des forces basées sur les statistiques
        if 'stats' in team_details and isinstance(team_details['stats'], dict) and 'data' in team_details['stats']:
            stats_data = pd.DataFrame(team_details['stats']['data'])
            
            if not stats_data.empty:
                # Buts marqués
                if 'goals' in stats_data.columns:
                    goals_per_game = stats_data['goals'].mean()
                    
                    if goals_per_game > 2:
                        team_strengths.append({
                            'type': 'scoring',
                            'title': 'Efficacité offensive',
                            'description': f"Marque en moyenne {goals_per_game:.1f} buts par match",
                            'value': goals_per_game,
                            'confidence': 0.8
                        })
                
                # Clean sheets
                if 'clean_sheets' in stats_data.columns and 'games' in stats_data.columns:
                    clean_sheet_ratio = stats_data['clean_sheets'].sum() / stats_data['games'].sum()
                    
                    if clean_sheet_ratio > 0.3:
                        team_strengths.append({
                            'type': 'clean_sheets',
                            'title': 'Clean sheets fréquents',
                            'description': f"Garde sa cage inviolée dans {clean_sheet_ratio*100:.0f}% des matchs",
                            'value': clean_sheet_ratio,
                            'confidence': 0.7
                        })
        
        # Forces basées sur le classement Elo
        if 'elo_rating' in team_details:
            elo = team_details['elo_rating']
            
            if elo > 1800:
                team_strengths.append({
                    'type': 'elo',
                    'title': 'Équipe d\'élite',
                    'description': f"Classement Elo très élevé ({elo:.0f})",
                    'value': elo,
                    'confidence': 0.8
                })
            elif elo > 1700:
                team_strengths.append({
                    'type': 'elo',
                    'title': 'Équipe de haut niveau',
                    'description': f"Bon classement Elo ({elo:.0f})",
                    'value': elo,
                    'confidence': 0.7
                })
        
        return team_strengths
    
    def _analyze_team_weaknesses(self, team_details):
        """
        Analyse les faiblesses d'une équipe.
        
        Args:
            team_details (dict): Données détaillées de l'équipe
            
        Returns:
            list: Faiblesses identifiées
        """
        team_weaknesses = []
        
        # Extraire les forces (pour identifier les faiblesses par contraste)
        strengths = self._extract_team_strengths(team_details)
        
        # Convertir en insights de faiblesse (les catégories avec les scores les plus bas)
        weakness_thresholds = [
            ('attacking', 1.0, 'Manque d\'efficacité offensive', 'Difficultés à marquer des buts'),
            ('midfield', 1.0, 'Milieu de terrain fragile', 'Manque de contrôle au milieu de terrain'),
            ('defense', 1.0, 'Fragilité défensive', 'Défense vulnérable'),
            ('set_pieces', 0.8, 'Vulnérabilité sur coups de pied arrêtés', 'Difficultés sur les phases arrêtées'),
            ('counterattack', 0.8, 'Vulnérabilité en contre-attaque', 'Exposée aux contre-attaques'),
            ('possession', 1.0, 'Difficultés à garder le ballon', 'Perd souvent la possession')
        ]
        
        for category, threshold, title, description in weakness_thresholds:
            if category in strengths and strengths[category] <= threshold:
                team_weaknesses.append({
                    'type': category,
                    'title': title,
                    'description': description,
                    'value': strengths[category],
                    'confidence': min(0.9, (1.5 - strengths[category]) / 1.5)
                })
        
        # Ajouter des faiblesses basées sur les statistiques
        if 'stats' in team_details and isinstance(team_details['stats'], dict) and 'data' in team_details['stats']:
            stats_data = pd.DataFrame(team_details['stats']['data'])
            
            if not stats_data.empty:
                # Buts encaissés
                if 'goals_against' in stats_data.columns:
                    goals_against_per_game = stats_data['goals_against'].mean()
                    
                    if goals_against_per_game > 1.5:
                        team_weaknesses.append({
                            'type': 'defending',
                            'title': 'Fragilité défensive',
                            'description': f"Encaisse en moyenne {goals_against_per_game:.1f} buts par match",
                            'value': goals_against_per_game,
                            'confidence': 0.8
                        })
                
                # Défaites lourdes
                if 'result' in stats_data.columns and 'goals_difference' in stats_data.columns:
                    heavy_losses = sum((stats_data['result'] == 'L') & (stats_data['goals_difference'] <= -2))
                    
                    if heavy_losses >= 3:
                        team_weaknesses.append({
                            'type': 'heavy_losses',
                            'title': 'Vulnérabilité aux défaites lourdes',
                            'description': f"A subi {heavy_losses} défaites par 2 buts d'écart ou plus",
                            'value': heavy_losses,
                            'confidence': 0.7
                        })
        
        # Analyse des joueurs blessés
        if 'detailed_players' in team_details:
            injured_key_players = []
            
            for player in team_details['detailed_players']:
                if player.get('injury_status') and (player.get('market_value', 0) > 10000000 or player.get('goals', 0) > 5 or player.get('assists', 0) > 5):
                    injured_key_players.append(player['name'])
            
            if injured_key_players:
                team_weaknesses.append({
                    'type': 'injuries',
                    'title': 'Joueurs clés blessés',
                    'description': f"{len(injured_key_players)} joueurs importants indisponibles",
                    'details': ", ".join(injured_key_players),
                    'confidence': 0.9
                })
        
        return team_weaknesses
    
    def _analyze_team_tactics(self, team_details):
        """
        Analyse tactique d'une équipe.
        
        Args:
            team_details (dict): Données détaillées de l'équipe
            
        Returns:
            list: Analyse tactique
        """
        tactical_analysis = []
        
        # Analyse basée sur le manager
        if 'detailed_manager' in team_details:
            manager = team_details['detailed_manager']
            
            if 'preferred_formation' in manager and manager['preferred_formation']:
                tactical_analysis.append({
                    'type': 'formation',
                    'title': 'Formation préférée',
                    'description': f"Formation habituelle : {manager['preferred_formation']}",
                    'confidence': 0.8
                })
            
            if 'playing_style' in manager and manager['playing_style']:
                tactical_analysis.append({
                    'type': 'playing_style',
                    'title': 'Style de jeu',
                    'description': f"Style de jeu dominant : {manager['playing_style']}",
                    'confidence': 0.7
                })
        
        # Analyse basée sur les statistiques d'équipe
        if 'stats' in team_details and isinstance(team_details['stats'], dict) and 'data' in team_details['stats']:
            stats_data = pd.DataFrame(team_details['stats']['data'])
            
            if not stats_data.empty:
                # Possession
                if 'possession' in stats_data.columns:
                    avg_possession = stats_data['possession'].mean()
                    
                    if avg_possession > 60:
                        tactical_analysis.append({
                            'type': 'possession',
                            'title': 'Équipe de possession',
                            'description': f"Domine la possession avec {avg_possession:.1f}% en moyenne",
                            'confidence': 0.8
                        })
                    elif avg_possession < 45:
                        tactical_analysis.append({
                            'type': 'counter_attack',
                            'title': 'Équipe de contre-attaque',
                            'description': f"Joue souvent sans le ballon ({avg_possession:.1f}% de possession en moyenne)",
                            'confidence': 0.7
                        })
                
                # Pressing
                if 'tackles' in stats_data.columns and 'interceptions' in stats_data.columns:
                    defensive_actions = stats_data['tackles'].mean() + stats_data['interceptions'].mean()
                    
                    if defensive_actions > 30:
                        tactical_analysis.append({
                            'type': 'pressing',
                            'title': 'Pressing intense',
                            'description': "Utilise un pressing haut et agressif",
                            'confidence': 0.7
                        })
        
        # Analyse basée sur la distribution des positions des joueurs
        if 'detailed_players' in team_details:
            positions = {}
            
            for player in team_details['detailed_players']:
                pos = player.get('position', 'Unknown')
                if pos not in positions:
                    positions[pos] = 0
                positions[pos] += 1
            
            # Identifier les tendances de position
            attacker_count = sum(positions.get(pos, 0) for pos in ['Attaquant', 'Ailier', 'Forward', 'Striker', 'Winger'])
            midfielder_count = sum(positions.get(pos, 0) for pos in ['Milieu', 'Milieu central', 'Midfielder', 'Central Midfielder'])
            defender_count = sum(positions.get(pos, 0) for pos in ['Défenseur', 'Défenseur central', 'Defender', 'Centre-Back'])
            
            if attacker_count > defender_count + 2:
                tactical_analysis.append({
                    'type': 'offensive_focus',
                    'title': 'Équipe orientée attaque',
                    'description': "Effectif axé sur les positions offensives",
                    'confidence': 0.6
                })
            elif defender_count > attacker_count + 2:
                tactical_analysis.append({
                    'type': 'defensive_focus',
                    'title': 'Équipe orientée défense',
                    'description': "Effectif axé sur les positions défensives",
                    'confidence': 0.6
                })
        
        return tactical_analysis
    
    def _analyze_team_historical_trends(self, team_details):
        """
        Analyse les tendances historiques d'une équipe.
        
        Args:
            team_details (dict): Données détaillées de l'équipe
            
        Returns:
            list: Tendances historiques
        """
        historical_trends = []
        
        # Analyse de la forme récente
        if 'form' in team_details and isinstance(team_details['form'], dict) and 'data' in team_details['form']:
            form_data = pd.DataFrame(team_details['form']['data'])
            
            if not form_data.empty and 'result' in form_data.columns:
                # Analyser les résultats récents
                recent_results = form_data['result'].tolist()[:5]  # 5 derniers matchs
                
                wins = recent_results.count('W')
                draws = recent_results.count('D')
                losses = recent_results.count('L')
                
                # Déterminer la forme récente
                if wins >= 4:
                    historical_trends.append({
                        'type': 'recent_form',
                        'title': 'Excellente forme récente',
                        'description': f"A gagné {wins} de ses 5 derniers matchs",
                        'details': f"{wins}V-{draws}N-{losses}D",
                        'confidence': 0.9
                    })
                elif wins >= 3:
                    historical_trends.append({
                        'type': 'recent_form',
                        'title': 'Bonne forme récente',
                        'description': f"A gagné {wins} de ses 5 derniers matchs",
                        'details': f"{wins}V-{draws}N-{losses}D",
                        'confidence': 0.8
                    })
                elif losses >= 4:
                    historical_trends.append({
                        'type': 'recent_form',
                        'title': 'Mauvaise passe',
                        'description': f"A perdu {losses} de ses 5 derniers matchs",
                        'details': f"{wins}V-{draws}N-{losses}D",
                        'confidence': 0.9
                    })
                elif losses >= 3:
                    historical_trends.append({
                        'type': 'recent_form',
                        'title': 'Forme préoccupante',
                        'description': f"A perdu {losses} de ses 5 derniers matchs",
                        'details': f"{wins}V-{draws}N-{losses}D",
                        'confidence': 0.8
                    })
        
        # Analyse des performances à domicile/extérieur
        if 'form' in team_details and isinstance(team_details['form'], dict) and 'data' in team_details['form']:
            form_data = pd.DataFrame(team_details['form']['data'])
            
            if not form_data.empty and 'home_team' in form_data.columns and 'away_team' in form_data.columns and 'result' in form_data.columns:
                # Performances à domicile
                home_matches = form_data[form_data['home_team'] == team_details.get('team_name')]
                
                if not home_matches.empty:
                    home_wins = sum(home_matches['result'] == 'W')
                    home_draws = sum(home_matches['result'] == 'D')
                    home_losses = sum(home_matches['result'] == 'L')
                    
                    if home_wins > home_draws + home_losses and len(home_matches) >= 3:
                        historical_trends.append({
                            'type': 'home_form',
                            'title': 'Force à domicile',
                            'description': f"Très performant sur son terrain",
                            'details': f"{home_wins}V-{home_draws}N-{home_losses}D à domicile",
                            'confidence': 0.8
                        })
                    elif home_losses > home_wins + home_draws and len(home_matches) >= 3:
                        historical_trends.append({
                            'type': 'home_form',
                            'title': 'Difficultés à domicile',
                            'description': f"Peine à s'imposer sur son terrain",
                            'details': f"{home_wins}V-{home_draws}N-{home_losses}D à domicile",
                            'confidence': 0.7
                        })
                
                # Performances à l'extérieur
                away_matches = form_data[form_data['away_team'] == team_details.get('team_name')]
                
                if not away_matches.empty:
                    away_wins = sum(away_matches['result'] == 'W')
                    away_draws = sum(away_matches['result'] == 'D')
                    away_losses = sum(away_matches['result'] == 'L')
                    
                    if away_wins > away_draws + away_losses and len(away_matches) >= 3:
                        historical_trends.append({
                            'type': 'away_form',
                            'title': 'Force à l\'extérieur',
                            'description': f"Très performant loin de ses bases",
                            'details': f"{away_wins}V-{away_draws}N-{away_losses}D à l'extérieur",
                            'confidence': 0.8
                        })
                    elif away_losses > away_wins + away_draws and len(away_matches) >= 3:
                        historical_trends.append({
                            'type': 'away_form',
                            'title': 'Difficultés à l\'extérieur',
                            'description': f"Peine à s'imposer loin de son terrain",
                            'details': f"{away_wins}V-{away_draws}N-{away_losses}D à l'extérieur",
                            'confidence': 0.7
                        })
        
        return historical_trends
    
    def _calculate_team_confidence_metrics(self, team_details):
        """
        Calcule des métriques de confiance pour les analyses d'équipe.
        
        Args:
            team_details (dict): Données détaillées de l'équipe
            
        Returns:
            dict: Métriques de confiance
        """
        confidence_metrics = {
            'overall_confidence': 0.0,
            'data_quality': 0.0,
            'data_recency': 0.0,
            'source_reliability': 0.0
        }
        
        # Évaluer la qualité des données
        data_quality = 0.5  # Base par défaut
        
        # Vérifier la disponibilité des différentes sources de données
        sources_count = 0
        sources_available = 0
        
        # Transfermarkt
        sources_count += 1
        if 'transfermarkt_data' in team_details:
            sources_available += 1
            data_quality += 0.1
        
        # Données de forme
        sources_count += 1
        if 'form' in team_details:
            sources_available += 1
            data_quality += 0.1
        
        # Données Elo
        sources_count += 1
        if 'elo_rating' in team_details:
            sources_available += 1
            data_quality += 0.1
        
        # Données statistiques
        sources_count += 1
        if 'stats' in team_details:
            sources_available += 1
            data_quality += 0.1
        
        # Données détaillées des joueurs
        sources_count += 1
        if 'detailed_players' in team_details:
            sources_available += 1
            data_quality += 0.1
        
        # Données du manager
        sources_count += 1
        if 'detailed_manager' in team_details:
            sources_available += 1
            data_quality += 0.1
        
        # Normaliser la qualité des données
        if sources_count > 0:
            source_reliability = sources_available / sources_count
            confidence_metrics['source_reliability'] = source_reliability
        
        confidence_metrics['data_quality'] = min(1.0, data_quality)
        
        # Évaluer la récence des données
        data_recency = 0.5  # Base par défaut
        
        # Vérifier la récence des données de forme
        if 'form' in team_details and isinstance(team_details['form'], dict) and 'data' in team_details['form']:
            form_data = pd.DataFrame(team_details['form']['data'])
            
            if not form_data.empty and 'date' in form_data.columns:
                try:
                    latest_date = pd.to_datetime(form_data['date'].max())
                    today = pd.to_datetime(datetime.now().date())
                    days_diff = (today - latest_date).days
                    
                    if days_diff <= 7:
                        data_recency += 0.3
                    elif days_diff <= 14:
                        data_recency += 0.2
                    elif days_diff <= 30:
                        data_recency += 0.1
                except Exception:
                    pass
        
        confidence_metrics['data_recency'] = min(1.0, data_recency)
        
        # Calculer la confiance globale
        confidence_metrics['overall_confidence'] = (
            confidence_metrics['data_quality'] * 0.4 +
            confidence_metrics['data_recency'] * 0.3 +
            confidence_metrics['source_reliability'] * 0.3
        )
        
        return confidence_metrics
    
    def generate_player_insights(self, player_name, team_name=None):
        """
        Génère des insights avancés pour un joueur spécifique.
        
        Args:
            player_name (str): Nom du joueur
            team_name (str, optional): Nom de l'équipe
            
        Returns:
            dict: Insights générés pour le joueur
        """
        insights = {
            'player_strengths': [],
            'player_weaknesses': [],
            'form_analysis': [],
            'statistical_highlights': [],
            'comparison_insights': [],
            'confidence_metrics': {}
        }
        
        # Récupérer les données détaillées du joueur si le hub est disponible
        if DATA_HUB_AVAILABLE:
            try:
                player_details = get_player_details(player_name, team_name)
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des détails du joueur: {e}")
                player_details = {'name': player_name, 'team': team_name}
        else:
            player_details = {'name': player_name, 'team': team_name}
        
        # 1. Forces du joueur
        player_strengths = self._analyze_player_strengths(player_details)
        if player_strengths:
            insights['player_strengths'].extend(player_strengths)
        
        # 2. Faiblesses du joueur
        player_weaknesses = self._analyze_player_weaknesses(player_details)
        if player_weaknesses:
            insights['player_weaknesses'].extend(player_weaknesses)
        
        # 3. Analyse de forme
        form_analysis = self._analyze_player_form(player_details)
        if form_analysis:
            insights['form_analysis'].extend(form_analysis)
        
        # 4. Points forts statistiques
        statistical_highlights = self._generate_player_statistical_highlights(player_details)
        if statistical_highlights:
            insights['statistical_highlights'].extend(statistical_highlights)
        
        # 5. Comparaisons
        comparison_insights = self._generate_player_comparisons(player_details)
        if comparison_insights:
            insights['comparison_insights'].extend(comparison_insights)
        
        # 6. Métriques de confiance
        confidence_metrics = self._calculate_player_confidence_metrics(player_details)
        if confidence_metrics:
            insights['confidence_metrics'] = confidence_metrics
        
        return insights
    
    def _analyze_player_strengths(self, player_details):
        """
        Analyse les forces d'un joueur.
        
        Args:
            player_details (dict): Données détaillées du joueur
            
        Returns:
            list: Forces identifiées
        """
        player_strengths = []
        
        # Analyser les forces à partir des ratings
        if 'strength_ratings' in player_details:
            for key, value in player_details['strength_ratings'].items():
                if value > 80:  # Seuil pour considérer comme une force
                    # Mapper les clés techniques à des descriptions plus lisibles
                    key_mapping = {
                        'goals_per90': 'Buteur prolifique',
                        'assists_per90': 'Excellent passeur',
                        'xg_per90': 'Création d\'occasions',
                        'passes_completed_pct': 'Précision des passes',
                        'progressive_passes': 'Passes progressives',
                        'tackles': 'Tacles',
                        'interceptions': 'Interceptions',
                        'dribbles_completed_pct': 'Dribbles réussis',
                        'aerial_won_pct': 'Duels aériens',
                        'shooting': 'Finition',
                        'dribbling': 'Technique de dribble',
                        'passing': 'Vision de jeu',
                        'defending': 'Défense',
                        'pace': 'Vitesse',
                        'physic': 'Puissance physique'
                    }
                    
                    description = key_mapping.get(key, key.replace('_', ' ').title())
                    
                    player_strengths.append({
                        'type': key,
                        'title': description,
                        'value': value,
                        'confidence': min(0.9, value / 100)
                    })
        
        # Analyser les statistiques brutes
        if player_details.get('goals', 0) > 10:
            player_strengths.append({
                'type': 'goals',
                'title': 'Buteur',
                'description': f"A marqué {player_details['goals']} buts",
                'confidence': 0.9
            })
        
        if player_details.get('assists', 0) > 5:
            player_strengths.append({
                'type': 'assists',
                'title': 'Passeur',
                'description': f"A délivré {player_details['assists']} passes décisives",
                'confidence': 0.9
            })
        
        if player_details.get('minutes_played', 0) > 2000:
            player_strengths.append({
                'type': 'consistency',
                'title': 'Joueur régulier',
                'description': "Accumule beaucoup de temps de jeu",
                'confidence': 0.8
            })
        
        # Ajouter une force basée sur la valeur marchande
        if player_details.get('market_value'):
            try:
                # Convertir en nombre si c'est une chaîne
                if isinstance(player_details['market_value'], str):
                    if 'M' in player_details['market_value']:
                        market_value = float(player_details['market_value'].replace('M', '').replace('€', '')) * 1000000
                    elif 'K' in player_details['market_value']:
                        market_value = float(player_details['market_value'].replace('K', '').replace('€', '')) * 1000
                    else:
                        market_value = float(player_details['market_value'].replace('€', ''))
                else:
                    market_value = player_details['market_value']
                
                if market_value > 50000000:
                    player_strengths.append({
                        'type': 'market_value',
                        'title': 'Superstar',
                        'description': f"Valeur marchande très élevée",
                        'value': market_value,
                        'confidence': 0.9
                    })
                elif market_value > 20000000:
                    player_strengths.append({
                        'type': 'market_value',
                        'title': 'Joueur de grande valeur',
                        'description': f"Valeur marchande importante",
                        'value': market_value,
                        'confidence': 0.8
                    })
            except (ValueError, TypeError):
                pass
        
        return player_strengths
    
    def _analyze_player_weaknesses(self, player_details):
        """
        Analyse les faiblesses d'un joueur.
        
        Args:
            player_details (dict): Données détaillées du joueur
            
        Returns:
            list: Faiblesses identifiées
        """
        player_weaknesses = []
        
        # Analyser les faiblesses à partir des ratings
        if 'weakness_ratings' in player_details:
            for key, value in player_details['weakness_ratings'].items():
                if value < 60:  # Seuil pour considérer comme une faiblesse
                    # Mapper les clés techniques à des descriptions plus lisibles
                    key_mapping = {
                        'goals_per90': 'Manque d\'efficacité devant le but',
                        'assists_per90': 'Peu de passes décisives',
                        'passes_completed_pct': 'Imprécision des passes',
                        'tackles': 'Difficulté dans les tacles',
                        'interceptions': 'Peu d\'interceptions',
                        'dribbles_completed_pct': 'Dribbles peu réussis',
                        'aerial_won_pct': 'Faiblesse dans les duels aériens',
                        'shooting': 'Finition à améliorer',
                        'dribbling': 'Technique de dribble limitée',
                        'passing': 'Vision de jeu limitée',
                        'defending': 'Lacunes défensives',
                        'pace': 'Manque de vitesse',
                        'physic': 'Fragilité physique'
                    }
                    
                    description = key_mapping.get(key, f"Faiblesse en {key.replace('_', ' ')}")
                    
                    player_weaknesses.append({
                        'type': key,
                        'title': description,
                        'value': value,
                        'confidence': min(0.9, (60 - value) / 60)
                    })
        
        # Analyser les cartons
        if player_details.get('yellow_cards', 0) > 8:
            player_weaknesses.append({
                'type': 'discipline',
                'title': 'Problèmes disciplinaires',
                'description': f"A reçu {player_details['yellow_cards']} cartons jaunes",
                'confidence': 0.8
            })
        
        if player_details.get('red_cards', 0) > 1:
            player_weaknesses.append({
                'type': 'discipline',
                'title': 'Risque d\'exclusion',
                'description': f"A reçu {player_details['red_cards']} cartons rouges",
                'confidence': 0.9
            })
        
        # Vérifier le statut de blessure
        if player_details.get('injury_status'):
            player_weaknesses.append({
                'type': 'injury',
                'title': 'Actuellement blessé',
                'description': player_details['injury_status'],
                'confidence': 0.95
            })
        
        # Manque de temps de jeu
        if player_details.get('appearances', 0) > 0 and player_details.get('minutes_played', 0) < 500:
            player_weaknesses.append({
                'type': 'playing_time',
                'title': 'Temps de jeu limité',
                'description': f"Seulement {player_details.get('minutes_played')} minutes jouées",
                'confidence': 0.8
            })
        
        return player_weaknesses
    
    def _analyze_player_form(self, player_details):
        """
        Analyse la forme récente d'un joueur.
        
        Args:
            player_details (dict): Données détaillées du joueur
            
        Returns:
            list: Analyse de forme
        """
        form_analysis = []
        
        # Peu de données disponibles sur la forme récente des joueurs individuels
        # dans les API/sources actuelles
        
        # Vérifier si des données de forme sont disponibles
        if 'recent_performances' in player_details:
            recent_performances = player_details['recent_performances']
            
            if isinstance(recent_performances, list) and recent_performances:
                # Analyser les performances récentes
                recent_goals = sum(perf.get('goals', 0) for perf in recent_performances)
                recent_assists = sum(perf.get('assists', 0) for perf in recent_performances)
                
                if recent_goals > 3:
                    form_analysis.append({
                        'type': 'recent_goals',
                        'title': 'En grande forme offensive',
                        'description': f"A marqué {recent_goals} buts lors de ses derniers matchs",
                        'confidence': 0.8
                    })
                
                if recent_assists > 2:
                    form_analysis.append({
                        'type': 'recent_assists',
                        'title': 'Créatif récemment',
                        'description': f"A délivré {recent_assists} passes décisives lors de ses derniers matchs",
                        'confidence': 0.8
                    })
        
        # Analyser la tendance des minutes jouées
        if 'minutes_per_game_trend' in player_details:
            trend = player_details['minutes_per_game_trend']
            
            if trend == 'increasing':
                form_analysis.append({
                    'type': 'playing_time',
                    'title': 'De plus en plus utilisé',
                    'description': "Temps de jeu en augmentation sur les derniers matchs",
                    'confidence': 0.7
                })
            elif trend == 'decreasing':
                form_analysis.append({
                    'type': 'playing_time',
                    'title': 'Moins utilisé récemment',
                    'description': "Temps de jeu en diminution sur les derniers matchs",
                    'confidence': 0.7
                })
        
        return form_analysis
    
    def _generate_player_statistical_highlights(self, player_details):
        """
        Génère des points forts statistiques pour un joueur.
        
        Args:
            player_details (dict): Données détaillées du joueur
            
        Returns:
            list: Points forts statistiques
        """
        statistical_highlights = []
        
        # Analyser les statistiques disponibles
        if player_details.get('goals') is not None and player_details.get('appearances') is not None and player_details.get('appearances') > 0:
            goals_per_game = player_details['goals'] / player_details['appearances']
            
            if goals_per_game > 0.5:
                statistical_highlights.append({
                    'type': 'goals_per_game',
                    'title': 'Buteur régulier',
                    'description': f"Moyenne de {goals_per_game:.2f} buts par match",
                    'value': goals_per_game,
                    'confidence': 0.8
                })
        
        if player_details.get('assists') is not None and player_details.get('appearances') is not None and player_details.get('appearances') > 0:
            assists_per_game = player_details['assists'] / player_details['appearances']
            
            if assists_per_game > 0.3:
                statistical_highlights.append({
                    'type': 'assists_per_game',
                    'title': 'Passeur régulier',
                    'description': f"Moyenne de {assists_per_game:.2f} passes décisives par match",
                    'value': assists_per_game,
                    'confidence': 0.8
                })
        
        # Points forts basés sur des statistiques spécifiques à la position
        position = player_details.get('position', '').lower()
        
        if 'attaquant' in position or 'forward' in position or 'striker' in position:
            # Statistiques spécifiques aux attaquants
            if player_details.get('shots_on_target_pct', 0) > 60:
                statistical_highlights.append({
                    'type': 'shooting_accuracy',
                    'title': 'Précision de tir',
                    'description': f"{player_details['shots_on_target_pct']}% de tirs cadrés",
                    'value': player_details['shots_on_target_pct'],
                    'confidence': 0.8
                })
        
        elif 'milieu' in position or 'midfielder' in position:
            # Statistiques spécifiques aux milieux
            if player_details.get('pass_completion', 0) > 85:
                statistical_highlights.append({
                    'type': 'passing_accuracy',
                    'title': 'Précision des passes',
                    'description': f"{player_details['pass_completion']}% de passes réussies",
                    'value': player_details['pass_completion'],
                    'confidence': 0.8
                })
        
        elif 'défenseur' in position or 'defender' in position:
            # Statistiques spécifiques aux défenseurs
            if player_details.get('tackles_per90', 0) > 2.5:
                statistical_highlights.append({
                    'type': 'tackles',
                    'title': 'Tacler solide',
                    'description': f"{player_details['tackles_per90']:.1f} tacles par 90 minutes",
                    'value': player_details['tackles_per90'],
                    'confidence': 0.8
                })
        
        elif 'gardien' in position or 'goalkeeper' in position:
            # Statistiques spécifiques aux gardiens
            if player_details.get('save_pct', 0) > 75:
                statistical_highlights.append({
                    'type': 'saves',
                    'title': 'Taux d\'arrêts élevé',
                    'description': f"{player_details['save_pct']}% de tirs arrêtés",
                    'value': player_details['save_pct'],
                    'confidence': 0.8
                })
        
        return statistical_highlights
    
    def _generate_player_comparisons(self, player_details):
        """
        Génère des comparaisons avec d'autres joueurs.
        
        Args:
            player_details (dict): Données détaillées du joueur
            
        Returns:
            list: Insights de comparaison
        """
        comparison_insights = []
        
        # Cette fonctionnalité nécessiterait une base de données de comparaison de joueurs
        # qui n'est pas disponible directement via les API actuelles
        
        # Exemple de ce que pourrait être un insight de comparaison
        if player_details.get('similar_players'):
            for similar in player_details['similar_players']:
                comparison_insights.append({
                    'type': 'similar_player',
                    'title': f"Similaire à {similar['name']}",
                    'description': f"Style de jeu proche de {similar['name']} ({similar['team']})",
                    'similarity_score': similar.get('similarity', 0.7),
                    'confidence': similar.get('similarity', 0.7)
                })
        
        return comparison_insights
    
    def _calculate_player_confidence_metrics(self, player_details):
        """
        Calcule des métriques de confiance pour les analyses de joueur.
        
        Args:
            player_details (dict): Données détaillées du joueur
            
        Returns:
            dict: Métriques de confiance
        """
        confidence_metrics = {
            'overall_confidence': 0.0,
            'data_quality': 0.0,
            'data_coverage': 0.0,
            'source_reliability': 0.0
        }
        
        # Évaluer la qualité des données
        data_quality = 0.5  # Base par défaut
        
        # Compter les champs disponibles
        available_fields = sum(1 for key, value in player_details.items() if value is not None)
        
        # Vérifier la disponibilité des champs clés
        key_fields = ['name', 'position', 'team', 'age', 'nationality']
        key_fields_available = sum(1 for field in key_fields if player_details.get(field) is not None)
        
        # Bonus pour chaque champ clé disponible
        data_quality += 0.1 * (key_fields_available / len(key_fields))
        
        # Bonus pour les statistiques détaillées
        if player_details.get('goals') is not None:
            data_quality += 0.05
        
        if player_details.get('assists') is not None:
            data_quality += 0.05
        
        if player_details.get('minutes_played') is not None:
            data_quality += 0.05
        
        if player_details.get('appearances') is not None:
            data_quality += 0.05
        
        # Bonus important pour les ratings de forces/faiblesses
        if 'strength_ratings' in player_details and player_details['strength_ratings']:
            data_quality += 0.1
        
        if 'weakness_ratings' in player_details and player_details['weakness_ratings']:
            data_quality += 0.1
        
        confidence_metrics['data_quality'] = min(1.0, data_quality)
        
        # Évaluer la couverture des données
        total_possible_fields = 20  # Estimation du nombre total de champs possibles
        data_coverage = available_fields / total_possible_fields
        
        confidence_metrics['data_coverage'] = min(1.0, data_coverage)
        
        # Évaluer la fiabilité des sources
        source_reliability = 0.6  # Base par défaut
        
        # Bonus pour les sources de données connues
        if 'data_sources' in player_details:
            sources = player_details['data_sources']
            
            if 'transfermarkt' in sources:
                source_reliability += 0.1
            
            if 'soccerdata_fbref' in sources:
                source_reliability += 0.1
            
            if 'soccerdata_sofifa' in sources:
                source_reliability += 0.1
        
        confidence_metrics['source_reliability'] = min(1.0, source_reliability)
        
        # Calculer la confiance globale
        confidence_metrics['overall_confidence'] = (
            confidence_metrics['data_quality'] * 0.4 +
            confidence_metrics['data_coverage'] * 0.3 +
            confidence_metrics['source_reliability'] * 0.3
        )
        
        return confidence_metrics

# Créer une instance singleton pour l'accès global
_advanced_data_insights = None

def get_advanced_data_insights():
    """
    Récupère l'instance singleton d'analyse avancée des données.
    
    Returns:
        AdvancedDataInsights: Instance d'analyse avancée des données
    """
    global _advanced_data_insights
    
    if _advanced_data_insights is None:
        logger.info("Initialisation de l'analyse avancée des données")
        _advanced_data_insights = AdvancedDataInsights()
        
    return _advanced_data_insights

def generate_match_insights(match_data):
    """
    Génère des insights avancés pour un match.
    
    Args:
        match_data (dict): Données du match
        
    Returns:
        dict: Insights générés pour le match
    """
    insights = get_advanced_data_insights()
    return insights.generate_match_insights(match_data)

def generate_team_insights(team_name):
    """
    Génère des insights avancés pour une équipe.
    
    Args:
        team_name (str): Nom de l'équipe
        
    Returns:
        dict: Insights générés pour l'équipe
    """
    insights = get_advanced_data_insights()
    return insights.generate_team_insights(team_name)

def generate_player_insights(player_name, team_name=None):
    """
    Génère des insights avancés pour un joueur.
    
    Args:
        player_name (str): Nom du joueur
        team_name (str, optional): Nom de l'équipe
        
    Returns:
        dict: Insights générés pour le joueur
    """
    insights = get_advanced_data_insights()
    return insights.generate_player_insights(player_name, team_name)