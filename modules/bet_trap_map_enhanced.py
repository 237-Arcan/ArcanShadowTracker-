"""
BetTrapMap (Version Enrichie) - Module avancé de cartographie des pièges à mise.
Cette version améliorée intègre des données provenant de multiples sources (Transfermarkt, soccerdata, 
détails des joueurs/managers) pour une détection plus précise des pièges de paris.
"""

import random
from datetime import datetime, timedelta
import numpy as np
import logging
from collections import defaultdict
import pandas as pd

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Intégration de l'adaptateur Transfermarkt
from api.transfermarkt_integration import (
    is_transfermarkt_available,
    get_team_profile,
    get_team_players, 
    search_club_by_name
)

# Vérifier si nos nouvelles sources de données sont disponibles
try:
    # Importer le hub d'intégration de données
    import api.data_integration_hub
    DATA_HUB_AVAILABLE = True
    
    # Vérifier quelles sources spécifiques sont disponibles
    try:
        import soccerdata
        SOCCERDATA_AVAILABLE = True
    except ImportError:
        SOCCERDATA_AVAILABLE = False
    
    # Module d'enrichissement des joueurs
    try:
        import api.player_data_enrichment
        PLAYER_ENRICHMENT_AVAILABLE = True
    except ImportError:
        PLAYER_ENRICHMENT_AVAILABLE = False
    
    logger.info(f"BetTrapMap amélioré initialisé avec sources additionnelles. SoccerData: {SOCCERDATA_AVAILABLE}, Enrichissement joueurs: {PLAYER_ENRICHMENT_AVAILABLE}")
except ImportError:
    DATA_HUB_AVAILABLE = False
    SOCCERDATA_AVAILABLE = False
    PLAYER_ENRICHMENT_AVAILABLE = False
    logger.warning("Hub d'intégration de données non disponible, fonctionnalités avancées désactivées")

class BetTrapMapEnhanced:
    """
    BetTrapMap (Version Enrichie) - Système avancé d'analyse et de cartographie des pièges à mise.
    
    Cette version améliorée utilise des données provenant de multiples sources pour identifier
    les configurations de paris potentiellement piégeuses avec une précision accrue.
    """
    
    def __init__(self):
        """Initialise le module BetTrapMap enrichi avec accès à toutes les sources de données"""
        # Vérifier si Transfermarkt est disponible
        self.transfermarkt_available = is_transfermarkt_available()
        
        if self.transfermarkt_available:
            logger.info("Transfermarkt disponible pour BetTrapMap")
        else:
            logger.warning("API Transfermarkt non disponible, certaines fonctionnalités seront limitées")
        
        # Statut général des sources
        self.use_enhanced_data = DATA_HUB_AVAILABLE
        self.available_sources = {
            'transfermarkt': self.transfermarkt_available,
            'soccerdata': SOCCERDATA_AVAILABLE,
            'player_enrichment': PLAYER_ENRICHMENT_AVAILABLE
        }
        
        # Paramètres de détection améliorés (avec valorisation des données réelles)
        self.detection_params = {
            'odds_anomaly_threshold': 0.18,      # Seuil d'anomalie dans les cotes (baissé car données plus précises)
            'volume_imbalance_threshold': 0.65,  # Seuil de déséquilibre de volume (ajusté)
            'odds_movement_significance': 0.12,  # Seuil de mouvement significatif des cotes (plus sensible)
            'historical_trap_weight': 0.5,       # Poids des pièges historiques (augmenté avec données réelles)
            'confidence_threshold': 0.7,         # Seuil de confiance pour signaler un piège (ajusté)
            'min_trap_severity': 0.55,           # Sévérité minimale pour un piège significatif (diminuée car détection plus fine)
            'max_safe_markets': 4,               # Nombre max de marchés "sûrs" à recommander (augmenté)
            'real_data_bonus': 0.1               # Bonus de confiance pour les données réelles vs simulées
        }
        
        # Types de pièges connus (version enrichie)
        self.trap_types = {
            'odds_reversal': {
                'description': "Inversion des cotes peu avant le match",
                'severity': 0.8,
                'detection_patterns': ['late_odds_movement', 'counter_public_movement']
            },
            'implied_probability_gap': {
                'description': "Écart suspect entre probabilités implicites des différentes cotes",
                'severity': 0.7,
                'detection_patterns': ['implied_prob_inconsistency', 'arbitrage_opportunity']
            },
            'false_favorite': {
                'description': "Favori surévalué par rapport à sa valeur réelle",
                'severity': 0.85,
                'detection_patterns': ['heavy_public_favorite', 'odds_mispricing']
            },
            'steam_move': {
                'description': "Mouvement soudain des cotes sans catalyseur apparent",
                'severity': 0.75,
                'detection_patterns': ['rapid_odds_shift', 'sharp_action_detected']
            },
            'artificial_boost': {
                'description': "Cotes artificiellement gonflées pour attirer les mises",
                'severity': 0.8,
                'detection_patterns': ['outlier_odds_value', 'house_advantage_increase']
            },
            'line_freeze': {
                'description': "Immobilité suspecte des cotes malgré des facteurs changeants",
                'severity': 0.65,
                'detection_patterns': ['odds_stagnation', 'news_odds_disconnect']
            },
            'balanced_action_illusion': {
                'description': "Illusion d'action équilibrée masquant un déséquilibre réel",
                'severity': 0.7,
                'detection_patterns': ['visible_balanced_volume', 'hidden_imbalance']
            },
            'reverse_movement_trigger': {
                'description': "Changement déclenché pour inverser le flux des mises",
                'severity': 0.75,
                'detection_patterns': ['odds_movement_against_volume', 'timing_pattern']
            },
            # Nouveaux types de pièges détectables grâce aux données enrichies
            'form_deception': {
                'description': "Équipe dont la forme réelle diffère significativement de la perception publique",
                'severity': 0.85,
                'detection_patterns': ['form_reality_gap', 'misleading_media_narrative']
            },
            'key_player_distortion': {
                'description': "Impact excessif ou insuffisant accordé à l'absence d'un joueur clé",
                'severity': 0.8,
                'detection_patterns': ['player_impact_mispricing', 'replacement_quality_ignored']
            },
            'tactical_mismatch_ignorance': {
                'description': "Avantage tactique significatif ignoré dans les cotes",
                'severity': 0.75,
                'detection_patterns': ['style_advantage', 'historical_tactical_edge']
            },
            'contextual_factor_distortion': {
                'description': "Facteurs contextuels (météo, calendrier, rivalité) mal évalués dans les cotes",
                'severity': 0.7,
                'detection_patterns': ['context_impact_mispricing', 'secondary_factors_ignored']
            }
        }
        
        # États de marchés pour l'identification des pièges (version enrichie)
        self.market_states = [
            'normal',               # État normal, pas d'anomalie
            'suspicious',           # Activité suspecte mais pas confirmée
            'probable_trap',        # Forte probabilité de piège
            'confirmed_trap',       # Piège confirmé par plusieurs indicateurs
            'manipulated',          # Marché clairement manipulé
            'correcting',           # Marché en phase de correction
            'value_opportunity',    # Opportunité de valeur (anti-piège)
            'data_inconsistency',   # Incohérence dans les données (nouveau)
            'smart_money_active',   # Activité des parieurs avisés détectée (nouveau)
            'trap_reversal'         # Piège initial qui devient une opportunité (nouveau)
        ]
        
        # Historique des pièges détectés
        self.trap_history = []
    
    def analyze_team_data_enhanced(self, team_name, team_id=None):
        """
        Analyse avancée des données d'une équipe en utilisant toutes les sources disponibles.
        
        Args:
            team_name (str): Nom de l'équipe
            team_id (str, optional): ID de l'équipe dans Transfermarkt
            
        Returns:
            dict: Analyse enrichie des facteurs de l'équipe liés aux pièges
        """
        # Base de l'analyse
        analysis = {
            'team_name': team_name,
            'team_id': team_id,
            'timestamp': datetime.now().isoformat(),
            'factors_analyzed': 0,
            'key_factors': [],
            'player_factors': [],
            'team_stability': 0.0,
            'consistency_score': 0.0,
            'form_analysis': {},
            'key_absences': [],
            'tactical_profile': {},
            'overall_trap_risk': 0.0,
            'data_quality': 0.0,
            'sources_used': []
        }
        
        # Liste pour collecter et fusionner les données de toutes les sources
        all_players = []
        
        # 1. Récupérer les données Transfermarkt si disponibles
        if self.transfermarkt_available and team_id:
            analysis['sources_used'].append('transfermarkt')
            try:
                # Récupérer le profil du club et ses joueurs
                club_profile = get_team_profile(team_id)
                if 'status' not in club_profile:
                    club_players = get_team_players(team_id)
                    
                    if 'status' not in club_players:
                        # Extraire les informations clés du club
                        club_name = club_profile.get('name', team_name)
                        league = club_profile.get('league', {}).get('name', 'Inconnue')
                        
                        analysis['team_name'] = club_name
                        analysis['league'] = league
                        
                        # Analyser les joueurs
                        squad = club_players.get('squad', [])
                        
                        # Extraire les données des joueurs pour analyse
                        for player in squad:
                            if isinstance(player, dict):
                                player_data = {
                                    'name': player.get('name', 'Inconnu'),
                                    'position': player.get('position', 'Inconnu'),
                                    'join_date': player.get('join_date', ''),
                                    'market_value': player.get('market_value', 0),
                                    'nationality': player.get('nationality', 'Inconnue'),
                                    'age': player.get('age', 0),
                                    'data_source': 'transfermarkt'
                                }
                                all_players.append(player_data)
                        
                        analysis['data_quality'] += 0.5
                    else:
                        logger.warning(f"Erreur lors de la récupération des joueurs: {club_players.get('message', '')}")
                else:
                    logger.warning(f"Erreur lors de la récupération du profil du club: {club_profile.get('message', '')}")
            except Exception as e:
                logger.error(f"Erreur lors de l'analyse Transfermarkt: {e}")
        
        # 2. Intégrer des données du hub central si disponible
        if DATA_HUB_AVAILABLE:
            try:
                # Utiliser le module player_data_enrichment
                if PLAYER_ENRICHMENT_AVAILABLE:
                    analysis['sources_used'].append('player_enrichment')
                    
                    # Importer de manière dynamique pour éviter les problèmes de récursion
                    from api.player_data_enrichment import get_team_detailed_players, get_team_manager
                    
                    # Récupérer les joueurs détaillés
                    detailed_players = get_team_detailed_players(team_name)
                    if detailed_players and len(detailed_players) > 0:
                        for player in detailed_players:
                            # Créer une entrée enrichie
                            player_data = {
                                'name': player.get('name', 'Inconnu'),
                                'position': player.get('position', 'Inconnu'),
                                'market_value': player.get('market_value', 0),
                                'nationality': player.get('nationality', 'Inconnue'),
                                'age': player.get('age', 0),
                                'form': player.get('form', 'normal'),
                                'injury_status': player.get('injury_status', None),
                                'goals': player.get('goals', 0),
                                'assists': player.get('assists', 0),
                                'minutes_played': player.get('minutes_played', 0),
                                'key_player': player.get('is_key_player', False),
                                'data_source': 'player_enrichment'
                            }
                            all_players.append(player_data)
                        
                        analysis['data_quality'] += 0.3
                    
                    # Récupérer les informations sur l'entraîneur
                    manager = get_team_manager(team_name)
                    if manager:
                        analysis['manager'] = {
                            'name': manager.get('name', 'Inconnu'),
                            'age': manager.get('age', 0),
                            'nationality': manager.get('nationality', 'Inconnue'),
                            'tactical_style': manager.get('tactical_style', 'Inconnu'),
                            'tenure': manager.get('tenure_days', 0),
                            'win_percentage': manager.get('win_percentage', 0.0)
                        }
                
                # Utiliser les données soccerdata
                if SOCCERDATA_AVAILABLE:
                    analysis['sources_used'].append('soccerdata')
                    
                    # Importer de manière dynamique pour éviter les problèmes de récursion
                    from api.soccerdata_integration import get_team_form, get_team_stats
                    
                    # Récupérer la forme récente
                    form_data = get_team_form(team_name)
                    if not isinstance(form_data, str) and not form_data.empty:
                        # Convertir les données en format lisible
                        form_dict = form_data.to_dict()
                        
                        # Analyser la forme récente
                        try:
                            recent_results = form_dict.get('result', {})
                            if recent_results:
                                # Convertir en liste de résultats
                                recent_matches = []
                                for idx, result in recent_results.items():
                                    match_data = {
                                        'result': result,
                                        'opponent': form_dict.get('opponent', {}).get(idx, 'Inconnu'),
                                        'score': form_dict.get('score', {}).get(idx, '0-0'),
                                        'date': form_dict.get('date', {}).get(idx, ''),
                                        'is_home': form_dict.get('is_home', {}).get(idx, False)
                                    }
                                    recent_matches.append(match_data)
                                
                                # Calculer des métriques de forme
                                wins = sum(1 for match in recent_matches if match['result'] == 'W')
                                draws = sum(1 for match in recent_matches if match['result'] == 'D')
                                losses = sum(1 for match in recent_matches if match['result'] == 'L')
                                
                                form_quality = (wins * 3 + draws) / (len(recent_matches) * 3) if recent_matches else 0.5
                                
                                analysis['form_analysis'] = {
                                    'recent_matches': recent_matches,
                                    'wins': wins,
                                    'draws': draws,
                                    'losses': losses,
                                    'form_quality': form_quality
                                }
                                
                                analysis['data_quality'] += 0.2
                        except Exception as e:
                            logger.error(f"Erreur lors de l'analyse de la forme: {e}")
                    
                    # Récupérer les statistiques de l'équipe
                    team_stats = get_team_stats(team_name)
                    if not isinstance(team_stats, str) and not team_stats.empty:
                        try:
                            # Convertir en dictionnaire
                            stats_dict = team_stats.iloc[0].to_dict() if len(team_stats) > 0 else {}
                            
                            # Ajouter les statistiques importantes
                            analysis['team_stats'] = {
                                'goals_scored': stats_dict.get('goals_for', 0),
                                'goals_conceded': stats_dict.get('goals_against', 0),
                                'shots_per_game': stats_dict.get('shots_per_game', 0),
                                'possession': stats_dict.get('possession', 0),
                                'pass_accuracy': stats_dict.get('pass_success', 0),
                                'rating': stats_dict.get('rating', 0)
                            }
                            
                            # Extraire le profil tactique basé sur les statistiques
                            analysis['tactical_profile'] = self._extract_tactical_profile(stats_dict)
                            
                            analysis['data_quality'] += 0.2
                        except Exception as e:
                            logger.error(f"Erreur lors de l'analyse des statistiques: {e}")
            
            except Exception as e:
                logger.error(f"Erreur lors de l'intégration des données enrichies: {e}")
        
        # 3. Analyse des joueurs consolidée
        if all_players:
            # Dédupliquer les joueurs
            player_dict = {}
            for player in all_players:
                name = player['name']
                # Garder la meilleure source ou fusionner les informations
                if name not in player_dict or player.get('data_source') == 'player_enrichment':
                    player_dict[name] = player
            
            # Convertir en liste
            consolidated_players = list(player_dict.values())
            
            # Trouver les joueurs clés
            key_players = []
            injured_key_players = []
            
            for player in consolidated_players:
                is_key = False
                
                # Déterminer si c'est un joueur clé
                if player.get('key_player', False):
                    is_key = True
                elif isinstance(player.get('market_value'), (int, float)) and player.get('market_value', 0) > 15000000:
                    is_key = True
                elif isinstance(player.get('market_value'), str) and 'M' in player.get('market_value', ''):
                    try:
                        value = float(player.get('market_value', '0').replace('M', '').replace('€', ''))
                        if value > 15:  # 15M+
                            is_key = True
                    except:
                        pass
                elif player.get('goals', 0) > 5 or player.get('assists', 0) > 5:
                    is_key = True
                
                if is_key:
                    key_players.append(player)
                    
                    # Vérifier s'il est blessé
                    if player.get('injury_status'):
                        injured_key_players.append(player)
            
            # Analyser les nouveaux transferts
            recent_transfers = []
            for player in consolidated_players:
                join_date = player.get('join_date', '')
                if join_date:
                    try:
                        # Essayer plusieurs formats de date
                        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%b %d, %Y'):
                            try:
                                join_datetime = datetime.strptime(join_date, fmt)
                                # Considérer comme récent si moins de 3 mois
                                if (datetime.now() - join_datetime).days <= 90:
                                    recent_transfers.append(player)
                                break
                            except ValueError:
                                continue
                    except Exception:
                        pass
            
            # Calculer la stabilité de l'équipe
            squad_size = len(consolidated_players)
            stability_score = 1.0 - min(0.9, (len(recent_transfers) / max(squad_size, 15)) * 1.5)
            
            # Calculer la cohérence de l'équipe (impact des blessures et transferts)
            key_player_count = len(key_players)
            if key_player_count > 0:
                key_changes = len(injured_key_players) + sum(1 for p in recent_transfers if p in key_players)
                consistency_score = 1.0 - min(0.9, (key_changes / key_player_count) * 1.2)
            else:
                consistency_score = 0.6  # Valeur par défaut
            
            # Mettre à jour l'analyse
            analysis['squad_size'] = squad_size
            analysis['key_players'] = [{'name': p['name'], 'position': p['position']} for p in key_players]
            analysis['recent_transfers'] = [{'name': p['name'], 'position': p['position']} for p in recent_transfers]
            analysis['injured_key_players'] = [{'name': p['name'], 'position': p['position']} for p in injured_key_players]
            analysis['team_stability'] = stability_score
            analysis['consistency_score'] = consistency_score
            
            # Ajouter aux facteurs clés
            if recent_transfers:
                analysis['key_factors'].append({
                    'factor_type': 'team_composition',
                    'description': f"{len(recent_transfers)} transferts récents",
                    'impact_score': 1.0 - stability_score,
                    'trap_correlation': 0.7 if any(p in key_players for p in recent_transfers) else 0.4
                })
            
            if injured_key_players:
                analysis['key_factors'].append({
                    'factor_type': 'key_absences',
                    'description': f"{len(injured_key_players)} joueurs clés absents",
                    'impact_score': min(0.9, len(injured_key_players) * 0.2),
                    'trap_correlation': 0.8
                })
        
        # 4. Intégrer l'analyse de forme dans les facteurs
        if 'form_analysis' in analysis and analysis['form_analysis']:
            form_quality = analysis['form_analysis'].get('form_quality', 0.5)
            
            # Forme exceptionnelle (potentiellement surévaluée par le public)
            if form_quality > 0.8:
                analysis['key_factors'].append({
                    'factor_type': 'recent_form',
                    'description': f"Forme exceptionnelle récente (W{analysis['form_analysis'].get('wins', 0)} D{analysis['form_analysis'].get('draws', 0)} L{analysis['form_analysis'].get('losses', 0)})",
                    'impact_score': form_quality - 0.5,  # L'écart par rapport à la normale
                    'trap_correlation': 0.75  # Forte corrélation - équipes en forme souvent surévaluées
                })
            # Mauvaise forme (potentiellement sous-évaluée par le public)
            elif form_quality < 0.3:
                analysis['key_factors'].append({
                    'factor_type': 'recent_form',
                    'description': f"Mauvaise forme récente (W{analysis['form_analysis'].get('wins', 0)} D{analysis['form_analysis'].get('draws', 0)} L{analysis['form_analysis'].get('losses', 0)})",
                    'impact_score': 0.5 - form_quality,  # L'écart par rapport à la normale
                    'trap_correlation': 0.7  # Forte corrélation - équipes en méforme souvent sous-évaluées
                })
        
        # 5. Intégrer le profil tactique dans les facteurs
        if analysis['tactical_profile']:
            tactical_type = analysis['tactical_profile'].get('type', '')
            tactical_strength = analysis['tactical_profile'].get('primary_strength', '')
            
            if tactical_type and tactical_strength:
                analysis['key_factors'].append({
                    'factor_type': 'tactical_profile',
                    'description': f"Style de jeu {tactical_type} avec force en {tactical_strength}",
                    'impact_score': analysis['tactical_profile'].get('purity', 0.5),
                    'trap_correlation': 0.6  # Corrélation moyenne - facteur souvent sous-estimé
                })
        
        # 6. Calculer le risque global de piège
        trap_risk_factors = []
        total_weight = 0
        
        for factor in analysis['key_factors']:
            weight = factor.get('trap_correlation', 0.5)
            score = factor.get('impact_score', 0.5)
            trap_risk_factors.append(score * weight)
            total_weight += weight
        
        # Ajouter des facteurs de base pour la stabilité et la consistance
        base_weight = 1.0
        trap_risk_factors.append((1.0 - analysis['team_stability']) * 0.7 * base_weight)
        trap_risk_factors.append((1.0 - analysis['consistency_score']) * 0.6 * base_weight)
        total_weight += 1.3 * base_weight  # 0.7 + 0.6
        
        # Calculer le risque moyen
        if total_weight > 0:
            avg_trap_risk = sum(trap_risk_factors) / total_weight
        else:
            avg_trap_risk = 0.5  # Valeur par défaut
        
        # Limiter entre 0 et 1
        analysis['overall_trap_risk'] = max(0.0, min(1.0, avg_trap_risk))
        analysis['factors_analyzed'] = len(analysis['key_factors']) + 2  # +2 pour stabilité et consistance
        
        # Normaliser la qualité des données
        analysis['data_quality'] = min(1.0, analysis['data_quality'])
        
        return analysis
    
    def _extract_tactical_profile(self, stats_dict):
        """
        Extrait le profil tactique d'une équipe à partir de ses statistiques.
        
        Args:
            stats_dict (dict): Statistiques de l'équipe
            
        Returns:
            dict: Profil tactique
        """
        # Valeurs par défaut
        profile = {
            'type': 'Équilibré',
            'primary_strength': 'Polyvalence',
            'secondary_strength': 'Adaptation',
            'weakness': 'Aucune dominante claire',
            'purity': 0.5  # Pureté du style
        }
        
        # Extraire les métriques clés
        possession = stats_dict.get('possession', 50)
        pass_success = stats_dict.get('pass_success', 75)
        shots = stats_dict.get('shots_per_game', 10)
        shots_conceded = stats_dict.get('shots_against_per_game', 10)
        tackles = stats_dict.get('tackles_per_game', 15)
        fouls = stats_dict.get('fouls_per_game', 10)
        
        # Déterminer le style de jeu principal
        if possession > 58 and pass_success > 85:
            profile['type'] = 'Possession'
            profile['primary_strength'] = 'Contrôle du jeu'
            profile['purity'] = min(1.0, (possession - 50) / 25)
        elif shots > 15 and possession > 52:
            profile['type'] = 'Offensif'
            profile['primary_strength'] = 'Attaque'
            profile['purity'] = min(1.0, shots / 20)
        elif tackles > 20 and shots_conceded < 8:
            profile['type'] = 'Défensif'
            profile['primary_strength'] = 'Organisation défensive'
            profile['purity'] = min(1.0, tackles / 25)
        elif fouls > 15 and tackles > 18:
            profile['type'] = 'Agressif'
            profile['primary_strength'] = 'Intensité physique'
            profile['purity'] = min(1.0, fouls / 20)
        elif shots > 12 and shots_conceded > 12:
            profile['type'] = 'Ouvert'
            profile['primary_strength'] = 'Jeu de transition'
            profile['purity'] = min(1.0, (shots + shots_conceded) / 30)
        
        # Déterminer les faiblesses potentielles
        if possession < 45 and pass_success < 75:
            profile['weakness'] = 'Conservation du ballon'
        elif shots < 8:
            profile['weakness'] = 'Création d\'occasions'
        elif shots_conceded > 15:
            profile['weakness'] = 'Vulnérabilité défensive'
        elif pass_success < 70:
            profile['weakness'] = 'Précision technique'
        
        return profile
    
    def analyze_market_traps_enhanced(self, match_data, odds_data=None, betting_volumes=None, historical_data=None):
        """
        Analyser les pièges potentiels sur tous les marchés d'un match avec données multi-sources.
        
        Args:
            match_data (dict): Données du match
            odds_data (dict, optional): Données de cotes par marché
            betting_volumes (dict, optional): Volumes de paris par marché
            historical_data (dict, optional): Données historiques pertinentes
            
        Returns:
            dict: Analyse complète des pièges potentiels
        """
        # Extraire les noms des équipes
        home_team = match_data.get('home_team', 'Équipe domicile')
        away_team = match_data.get('away_team', 'Équipe extérieure')
        match_date = match_data.get('date', datetime.now().isoformat())
        
        # Base de l'analyse
        trap_analysis = {
            'match': f"{home_team} vs {away_team}",
            'match_date': match_date,
            'analysis_timestamp': datetime.now().isoformat(),
            'trap_risk_level': 0.0,            # Niveau global de risque
            'traps_detected': [],              # Liste des pièges détectés
            'market_analysis': {},             # Analyse par marché
            'safe_markets': [],                # Marchés considérés comme sûrs
            'high_risk_markets': [],           # Marchés à haut risque
            'betting_recommendations': [],     # Recommandations de paris
            'team_analyses': {},               # Analyses des équipes
            'data_quality': 0.0,               # Qualité des données
            'sources_used': []                 # Sources utilisées
        }
        
        # Enrichir avec des données de nos différentes sources
        # 1. Transfermarkt
        if self.transfermarkt_available:
            trap_analysis['sources_used'].append('transfermarkt')
            
            # Récupérer les IDs des équipes si non fournis
            home_team_id = match_data.get('home_team_id')
            away_team_id = match_data.get('away_team_id')
            
            if not home_team_id:
                try:
                    search_results = search_club_by_name(home_team)
                    if search_results and 'items' in search_results and search_results['items']:
                        home_team_id = search_results['items'][0]['id']
                        logger.info(f"ID Transfermarkt trouvé pour {home_team}: {home_team_id}")
                except Exception as e:
                    logger.error(f"Erreur lors de la recherche de l'ID pour {home_team}: {e}")
            
            if not away_team_id:
                try:
                    search_results = search_club_by_name(away_team)
                    if search_results and 'items' in search_results and search_results['items']:
                        away_team_id = search_results['items'][0]['id']
                        logger.info(f"ID Transfermarkt trouvé pour {away_team}: {away_team_id}")
                except Exception as e:
                    logger.error(f"Erreur lors de la recherche de l'ID pour {away_team}: {e}")
            
            # Analyse enrichie des équipes
            if home_team_id or home_team:
                try:
                    home_analysis = self.analyze_team_data_enhanced(home_team, home_team_id)
                    trap_analysis['team_analyses']['home'] = home_analysis
                    trap_analysis['data_quality'] += home_analysis.get('data_quality', 0) * 0.3
                except Exception as e:
                    logger.error(f"Erreur lors de l'analyse enrichie pour {home_team}: {e}")
            
            if away_team_id or away_team:
                try:
                    away_analysis = self.analyze_team_data_enhanced(away_team, away_team_id)
                    trap_analysis['team_analyses']['away'] = away_analysis
                    trap_analysis['data_quality'] += away_analysis.get('data_quality', 0) * 0.3
                except Exception as e:
                    logger.error(f"Erreur lors de l'analyse enrichie pour {away_team}: {e}")
        
        # 2. Données du module d'intégration central
        if DATA_HUB_AVAILABLE:
            # Ajouter d'autres sources selon disponibilité
            if SOCCERDATA_AVAILABLE:
                trap_analysis['sources_used'].append('soccerdata')
                
                try:
                    # Importer de manière dynamique
                    from api.soccerdata_integration import get_head_to_head
                    
                    # Récupérer les confrontations directes
                    h2h_data = get_head_to_head(home_team, away_team)
                    if not isinstance(h2h_data, str) and not h2h_data.empty:
                        # Convertir en liste utilisable
                        h2h_matches = []
                        h2h_dict = h2h_data.to_dict(orient='records')
                        
                        for match in h2h_dict:
                            h2h_matches.append({
                                'date': match.get('date', ''),
                                'home_team': match.get('home_team', ''),
                                'away_team': match.get('away_team', ''),
                                'home_score': match.get('home_score', 0),
                                'away_score': match.get('away_score', 0),
                                'result': match.get('result', '')
                            })
                        
                        trap_analysis['head_to_head'] = h2h_matches
                        trap_analysis['data_quality'] += 0.2
                except Exception as e:
                    logger.error(f"Erreur lors de la récupération des confrontations directes: {e}")
        
        # Calculer le facteur d'instabilité d'équipe pour l'analyse des pièges
        team_instability_factor = 0.0
        teams_analyzed = 0
        
        if 'home' in trap_analysis['team_analyses']:
            home_risk = trap_analysis['team_analyses']['home'].get('overall_trap_risk', 0.0)
            team_instability_factor += home_risk
            teams_analyzed += 1
            
        if 'away' in trap_analysis['team_analyses']:
            away_risk = trap_analysis['team_analyses']['away'].get('overall_trap_risk', 0.0)
            team_instability_factor += away_risk
            teams_analyzed += 1
            
        if teams_analyzed > 0:
            team_instability_factor /= teams_analyzed
            trap_analysis['team_instability_factor'] = team_instability_factor
        
        # Analyser les confrontations directes pour détecter les pièges potentiels
        h2h_trap_factors = []
        
        if 'head_to_head' in trap_analysis and trap_analysis['head_to_head']:
            h2h_matches = trap_analysis['head_to_head']
            
            # Calculer des statistiques sur les confrontations
            home_wins = sum(1 for m in h2h_matches 
                           if m['home_team'] == home_team and m['home_score'] > m['away_score'] or
                              m['away_team'] == home_team and m['away_score'] > m['home_score'])
            
            away_wins = sum(1 for m in h2h_matches 
                           if m['home_team'] == away_team and m['home_score'] > m['away_score'] or
                              m['away_team'] == away_team and m['away_score'] > m['home_score'])
            
            draws = len(h2h_matches) - home_wins - away_wins
            
            # Vérifier s'il y a une tendance forte pour une équipe
            if len(h2h_matches) >= 3:
                if home_wins > away_wins * 2 and home_wins > draws * 2:
                    h2h_trap_factors.append({
                        'type': 'h2h_dominance',
                        'description': f"{home_team} domine historiquement ces confrontations (W{home_wins} D{draws} L{away_wins})",
                        'favors': home_team,
                        'trap_potential': 0.7 if away_wins == 0 else 0.5,
                        'underestimated': False
                    })
                elif away_wins > home_wins * 2 and away_wins > draws * 2:
                    h2h_trap_factors.append({
                        'type': 'h2h_dominance',
                        'description': f"{away_team} domine historiquement ces confrontations (W{away_wins} D{draws} L{home_wins})",
                        'favors': away_team,
                        'trap_potential': 0.75 if home_wins == 0 else 0.55,  # Plus élevé car c'est l'équipe extérieure
                        'underestimated': True
                    })
            
            # Analyser les scores
            total_goals = sum(m['home_score'] + m['away_score'] for m in h2h_matches)
            avg_goals = total_goals / len(h2h_matches) if h2h_matches else 0
            
            if avg_goals > 3.5 and len(h2h_matches) >= 3:
                h2h_trap_factors.append({
                    'type': 'h2h_goal_pattern',
                    'description': f"Confrontations historiquement prolifiques ({avg_goals:.1f} buts/match)",
                    'favors': 'both',
                    'trap_potential': 0.65,
                    'underestimated': True
                })
            elif avg_goals < 1.5 and len(h2h_matches) >= 3:
                h2h_trap_factors.append({
                    'type': 'h2h_goal_pattern',
                    'description': f"Confrontations historiquement fermées ({avg_goals:.1f} buts/match)",
                    'favors': 'both',
                    'trap_potential': 0.6,
                    'underestimated': True
                })
        
        # Analyser les pièges potentiels basés sur la forme récente
        form_trap_factors = []
        
        for team_key, team_label in [('home', home_team), ('away', away_team)]:
            if team_key in trap_analysis['team_analyses'] and 'form_analysis' in trap_analysis['team_analyses'][team_key]:
                form_analysis = trap_analysis['team_analyses'][team_key]['form_analysis']
                
                form_quality = form_analysis.get('form_quality', 0.5)
                
                # Vérifier si la forme est extrême (très bonne ou très mauvaise)
                if form_quality > 0.8:
                    # Très bonne forme - potentiellement surévaluée par le marché
                    form_trap_factors.append({
                        'type': 'form_overvaluation',
                        'description': f"{team_label} en excellente forme - potentiellement surévalué par le marché",
                        'favors': 'opposite',  # Favorise l'adversaire
                        'trap_potential': 0.7,
                        'underestimated': False
                    })
                elif form_quality < 0.2:
                    # Très mauvaise forme - potentiellement sous-évaluée par le marché
                    form_trap_factors.append({
                        'type': 'form_undervaluation',
                        'description': f"{team_label} en mauvaise forme - potentiellement sous-évalué par le marché",
                        'favors': team_label,  # Favorise cette équipe
                        'trap_potential': 0.65,
                        'underestimated': True
                    })
        
        # Analyser les pièges potentiels basés sur les absences de joueurs clés
        key_player_trap_factors = []
        
        for team_key, team_label in [('home', home_team), ('away', away_team)]:
            if team_key in trap_analysis['team_analyses']:
                team_analysis = trap_analysis['team_analyses'][team_key]
                
                # Vérifier les absences de joueurs clés
                if 'injured_key_players' in team_analysis and team_analysis['injured_key_players']:
                    injured_count = len(team_analysis['injured_key_players'])
                    
                    if injured_count >= 2:
                        key_player_trap_factors.append({
                            'type': 'key_absences',
                            'description': f"{team_label} privé de {injured_count} joueurs clés",
                            'favors': 'opposite',  # Favorise l'adversaire
                            'trap_potential': min(0.9, 0.6 + injured_count * 0.1),
                            'underestimated': False
                        })
                
                # Vérifier les transferts récents de joueurs clés
                if 'recent_transfers' in team_analysis and team_analysis['recent_transfers']:
                    transfers_count = len(team_analysis['recent_transfers'])
                    
                    key_transfers = [p for p in team_analysis['recent_transfers'] 
                                    if p in team_analysis.get('key_players', [])]
                    
                    if key_transfers:
                        key_player_trap_factors.append({
                            'type': 'recent_key_transfers',
                            'description': f"{team_label} avec {len(key_transfers)} nouveaux joueurs clés - intégration incertaine",
                            'favors': 'opposite',  # Favorise l'adversaire
                            'trap_potential': 0.6,
                            'underestimated': False
                        })
        
        # Analyser les pièges potentiels basés sur les profils tactiques
        tactical_trap_factors = []
        
        if ('home' in trap_analysis['team_analyses'] and 'tactical_profile' in trap_analysis['team_analyses']['home'] and
            'away' in trap_analysis['team_analyses'] and 'tactical_profile' in trap_analysis['team_analyses']['away']):
            
            home_tactical = trap_analysis['team_analyses']['home']['tactical_profile']
            away_tactical = trap_analysis['team_analyses']['away']['tactical_profile']
            
            # Vérifier si un style est particulièrement efficace contre l'autre
            if home_tactical.get('type') == 'Possession' and away_tactical.get('type') == 'Agressif':
                tactical_trap_factors.append({
                    'type': 'tactical_advantage',
                    'description': f"Style de possession de {home_team} vulnérable contre le pressing de {away_team}",
                    'favors': away_team,
                    'trap_potential': 0.7,
                    'underestimated': True
                })
            elif home_tactical.get('type') == 'Défensif' and away_tactical.get('type') == 'Offensif':
                tactical_trap_factors.append({
                    'type': 'tactical_advantage',
                    'description': f"Style défensif de {home_team} efficace contre l'approche offensive de {away_team}",
                    'favors': home_team,
                    'trap_potential': 0.65,
                    'underestimated': True
                })
            elif away_tactical.get('type') == 'Possession' and home_tactical.get('weakness') == 'Vulnérabilité défensive':
                tactical_trap_factors.append({
                    'type': 'tactical_vulnerability',
                    'description': f"Style de possession de {away_team} expose la faiblesse défensive de {home_team}",
                    'favors': away_team,
                    'trap_potential': 0.75,
                    'underestimated': True
                })
        
        # Obtenir ou simuler les données des cotes
        odds_data = odds_data or self._simulate_odds_data(home_team, away_team)
        
        # Analyser chaque marché de paris
        for market_name, market_odds in odds_data.items():
            market_analysis = self._analyze_market_enhanced(
                market_name, market_odds,
                betting_volumes.get(market_name, {}) if betting_volumes else {},
                historical_data.get(market_name, {}) if historical_data else {},
                h2h_trap_factors, form_trap_factors, key_player_trap_factors, tactical_trap_factors,
                team_instability_factor
            )
            
            trap_analysis['market_analysis'][market_name] = market_analysis
            
            # Identifier les marchés à haut risque
            if market_analysis['trap_risk'] >= self.detection_params['min_trap_severity']:
                trap_analysis['high_risk_markets'].append({
                    'market': market_name,
                    'risk': market_analysis['trap_risk'],
                    'trap_type': market_analysis['detected_trap_type'],
                    'description': market_analysis['trap_description']
                })
                
                # Ajouter à la liste des pièges détectés
                if market_analysis['detected_trap_type']:
                    trap_analysis['traps_detected'].append({
                        'market': market_name,
                        'trap_type': market_analysis['detected_trap_type'],
                        'severity': market_analysis['trap_risk'],
                        'description': market_analysis['trap_description'],
                        'confidence': market_analysis['detection_confidence']
                    })
            
            # Identifier les marchés sûrs (faible risque)
            elif market_analysis['trap_risk'] <= 0.3:
                # Limiter le nombre de marchés sûrs recommandés
                if len(trap_analysis['safe_markets']) < self.detection_params['max_safe_markets']:
                    trap_analysis['safe_markets'].append({
                        'market': market_name,
                        'risk': market_analysis['trap_risk'],
                        'value_rating': market_analysis.get('value_rating', 0.0),
                        'recommendation': market_analysis.get('recommended_bet', 'Aucune')
                    })
        
        # Calculer le niveau global de risque de piège
        if trap_analysis['high_risk_markets']:
            total_risk = sum(market['risk'] for market in trap_analysis['high_risk_markets'])
            avg_risk = total_risk / len(trap_analysis['high_risk_markets'])
            
            # Ajuster en fonction du nombre de pièges détectés
            risk_factor = min(1.0, len(trap_analysis['high_risk_markets']) / 3 * 0.5 + 0.5)
            trap_analysis['trap_risk_level'] = avg_risk * risk_factor
        else:
            trap_analysis['trap_risk_level'] = 0.2  # Risque de base faible
        
        # Générer des recommandations de paris
        trap_analysis['betting_recommendations'] = self._generate_betting_recommendations(
            trap_analysis['safe_markets'],
            trap_analysis['high_risk_markets'],
            odds_data,
            trap_analysis['team_analyses'] if 'team_analyses' in trap_analysis else {}
        )
        
        # Normaliser la qualité des données
        trap_analysis['data_quality'] = min(1.0, trap_analysis['data_quality'])
        
        return trap_analysis
    
    def _analyze_market_enhanced(self, market_name, market_odds, volume_data, historical_data,
                               h2h_factors, form_factors, key_player_factors, tactical_factors,
                               team_instability_factor):
        """
        Analyse approfondie d'un marché spécifique pour détecter les pièges potentiels.
        
        Args:
            market_name (str): Nom du marché de paris
            market_odds (dict): Cotes actuelles du marché
            volume_data (dict): Données sur les volumes de paris
            historical_data (dict): Données historiques sur ce marché
            h2h_factors (list): Facteurs basés sur les confrontations directes
            form_factors (list): Facteurs basés sur la forme récente
            key_player_factors (list): Facteurs basés sur les absences de joueurs clés
            tactical_factors (list): Facteurs basés sur les profils tactiques
            team_instability_factor (float): Facteur d'instabilité globale des équipes
            
        Returns:
            dict: Analyse complète du marché
        """
        # Base de l'analyse
        market_analysis = {
            'market': market_name,
            'current_odds': market_odds,
            'trap_risk': 0.0,
            'detection_confidence': 0.0,
            'factors_analyzed': [],
            'market_state': 'normal',
            'detected_trap_type': None,
            'trap_description': '',
            'value_opportunities': []
        }
        
        # Facteurs de risque spécifiques au marché
        market_risk_factors = []
        
        # 1. Analyser l'équilibre des cotes et des probabilités implicites
        try:
            # Pour un marché à 3 issues (1X2)
            if (market_name == '1X2' or market_name == 'Match Result') and len(market_odds) >= 3:
                home_odds = market_odds.get('1', market_odds.get('home', 0))
                draw_odds = market_odds.get('X', market_odds.get('draw', 0))
                away_odds = market_odds.get('2', market_odds.get('away', 0))
                
                if home_odds > 0 and draw_odds > 0 and away_odds > 0:
                    # Calculer les probabilités implicites
                    home_prob = 1 / home_odds
                    draw_prob = 1 / draw_odds
                    away_prob = 1 / away_odds
                    
                    # Vérifier la marge du bookmaker
                    total_prob = home_prob + draw_prob + away_prob
                    margin = total_prob - 1.0
                    
                    # Normaliser les probabilités
                    home_prob_fair = home_prob / total_prob
                    draw_prob_fair = draw_prob / total_prob
                    away_prob_fair = away_prob / total_prob
                    
                    # Détecter des anomalies dans les cotes
                    if home_odds < 1.3 and home_prob_fair < 0.65:
                        market_risk_factors.append({
                            'type': 'false_favorite',
                            'description': f"Cote domicile ({home_odds}) anormalement basse pour la probabilité implicite ({home_prob_fair:.2f})",
                            'severity': min(1.0, (0.65 - home_prob_fair) * 3),
                            'confidence': 0.7
                        })
                    
                    if away_odds < 2.0 and away_prob_fair < 0.4:
                        market_risk_factors.append({
                            'type': 'false_favorite',
                            'description': f"Cote extérieur ({away_odds}) anormalement basse pour la probabilité implicite ({away_prob_fair:.2f})",
                            'severity': min(1.0, (0.4 - away_prob_fair) * 3),
                            'confidence': 0.75
                        })
                    
                    # Analyser la marge
                    if margin > 0.12:
                        market_risk_factors.append({
                            'type': 'high_margin',
                            'description': f"Marge élevée du bookmaker ({margin:.2f}), peut cacher des valeurs biaisées",
                            'severity': min(1.0, margin * 3),
                            'confidence': 0.65
                        })
            
            # Pour un marché Over/Under
            elif 'Over/Under' in market_name or 'Goals' in market_name:
                over_odds = market_odds.get('Over', market_odds.get('over', 0))
                under_odds = market_odds.get('Under', market_odds.get('under', 0))
                
                if over_odds > 0 and under_odds > 0:
                    # Calculer les probabilités implicites
                    over_prob = 1 / over_odds
                    under_prob = 1 / under_odds
                    
                    # Vérifier la marge du bookmaker
                    total_prob = over_prob + under_prob
                    margin = total_prob - 1.0
                    
                    # Normaliser les probabilités
                    over_prob_fair = over_prob / total_prob
                    under_prob_fair = under_prob / total_prob
                    
                    # Détecter des anomalies dans les cotes
                    if abs(over_prob_fair - under_prob_fair) > 0.2:
                        market_risk_factors.append({
                            'type': 'imbalanced_probabilities',
                            'description': f"Déséquilibre significatif entre over ({over_prob_fair:.2f}) et under ({under_prob_fair:.2f})",
                            'severity': min(1.0, abs(over_prob_fair - under_prob_fair) * 2),
                            'confidence': 0.6
                        })
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse des cotes pour {market_name}: {e}")
        
        # 2. Intégrer les facteurs de confrontations directes
        for factor in h2h_factors:
            # Déterminer si ce facteur est pertinent pour ce marché
            is_relevant = False
            
            if (market_name == '1X2' or market_name == 'Match Result'):
                is_relevant = True
            elif 'Goals' in market_name and factor['type'] == 'h2h_goal_pattern':
                is_relevant = True
            
            if is_relevant:
                market_risk_factors.append({
                    'type': 'h2h_pattern',
                    'description': factor['description'],
                    'severity': factor['trap_potential'],
                    'confidence': 0.7,
                    'favors': factor['favors']
                })
        
        # 3. Intégrer les facteurs de forme
        for factor in form_factors:
            # Plus pertinent pour les marchés de résultat
            if (market_name == '1X2' or market_name == 'Match Result'):
                market_risk_factors.append({
                    'type': 'form_mispricing',
                    'description': factor['description'],
                    'severity': factor['trap_potential'],
                    'confidence': 0.65,
                    'favors': factor['favors']
                })
        
        # 4. Intégrer les facteurs de joueurs clés
        for factor in key_player_factors:
            # Pertinent pour presque tous les marchés
            market_risk_factors.append({
                'type': 'player_impact',
                'description': factor['description'],
                'severity': factor['trap_potential'],
                'confidence': 0.75,
                'favors': factor['favors']
            })
        
        # 5. Intégrer les facteurs tactiques
        for factor in tactical_factors:
            # Plus pertinent pour certains marchés spécifiques
            if (market_name == '1X2' or market_name == 'Match Result' or
                'Goals' in market_name or 'Cards' in market_name or 'Corners' in market_name):
                market_risk_factors.append({
                    'type': 'tactical_mismatch',
                    'description': factor['description'],
                    'severity': factor['trap_potential'],
                    'confidence': 0.7,
                    'favors': factor['favors']
                })
        
        # 6. Analyser les volumes de paris si disponibles
        if volume_data:
            try:
                # Vérifier le déséquilibre de volume
                max_volume = 0
                max_volume_option = None
                total_volume = sum(volume_data.values())
                
                for option, volume in volume_data.items():
                    if volume > max_volume:
                        max_volume = volume
                        max_volume_option = option
                
                if total_volume > 0:
                    max_volume_ratio = max_volume / total_volume
                    
                    if max_volume_ratio > self.detection_params['volume_imbalance_threshold']:
                        market_risk_factors.append({
                            'type': 'public_heavy_favorite',
                            'description': f"Déséquilibre de volume extrême sur {max_volume_option} ({max_volume_ratio:.0%})",
                            'severity': min(1.0, max_volume_ratio * 0.8),
                            'confidence': 0.8
                        })
            except Exception as e:
                logger.error(f"Erreur lors de l'analyse des volumes pour {market_name}: {e}")
        
        # 7. Analyser les données historiques si disponibles
        if historical_data:
            try:
                # Vérifier les mouvements significatifs de cotes
                if 'odds_movement' in historical_data:
                    for option, movements in historical_data['odds_movement'].items():
                        if option in market_odds and len(movements) >= 2:
                            initial_odds = movements[0]
                            current_odds = market_odds[option]
                            
                            movement_pct = abs(current_odds - initial_odds) / initial_odds
                            
                            if movement_pct > self.detection_params['odds_movement_significance']:
                                movement_direction = 'diminué' if current_odds < initial_odds else 'augmenté'
                                market_risk_factors.append({
                                    'type': 'significant_odds_movement',
                                    'description': f"Cotes pour {option} ont {movement_direction} de {movement_pct:.0%}",
                                    'severity': min(1.0, movement_pct * 2),
                                    'confidence': 0.7
                                })
                
                # Vérifier les mouvements tardifs
                if 'late_movement' in historical_data and historical_data['late_movement']:
                    for move in historical_data['late_movement']:
                        market_risk_factors.append({
                            'type': 'late_odds_movement',
                            'description': f"Mouvement tardif détecté: {move['description']}",
                            'severity': move.get('severity', 0.7),
                            'confidence': 0.75
                        })
            except Exception as e:
                logger.error(f"Erreur lors de l'analyse des données historiques pour {market_name}: {e}")
        
        # 8. Appliquer le facteur d'instabilité des équipes
        if team_instability_factor > 0.5:
            instability_severity = (team_instability_factor - 0.5) * 2
            market_risk_factors.append({
                'type': 'team_instability',
                'description': f"Instabilité globale des équipes (transferts, blessures, forme inconsistante)",
                'severity': instability_severity,
                'confidence': 0.65
            })
        
        # Analyser tous les facteurs de risque et déterminer le risque global
        if market_risk_factors:
            # Trier par sévérité
            market_risk_factors.sort(key=lambda x: x['severity'], reverse=True)
            
            # Calculer le risque moyen pondéré
            total_weight = 0
            weighted_risk = 0
            
            for factor in market_risk_factors:
                weight = factor['confidence']
                risk = factor['severity']
                
                weighted_risk += risk * weight
                total_weight += weight
            
            # Calculer le risque moyen
            if total_weight > 0:
                avg_risk = weighted_risk / total_weight
            else:
                avg_risk = 0.0
            
            # Déterminer le type de piège détecté (le plus sévère)
            detected_trap = market_risk_factors[0]
            detected_trap_type = detected_trap['type']
            
            # Associer à un type de piège connu
            known_trap_type = None
            for trap_name, trap_info in self.trap_types.items():
                if detected_trap_type in trap_info['detection_patterns']:
                    known_trap_type = trap_name
                    break
            
            if not known_trap_type:
                # Utiliser directement le type détecté
                known_trap_type = detected_trap_type
            
            # Déterminer l'état du marché
            if avg_risk >= 0.8:
                market_state = 'confirmed_trap'
            elif avg_risk >= 0.65:
                market_state = 'probable_trap'
            elif avg_risk >= 0.5:
                market_state = 'suspicious'
            else:
                market_state = 'normal'
            
            # Mettre à jour l'analyse
            market_analysis['trap_risk'] = avg_risk
            market_analysis['detection_confidence'] = market_risk_factors[0]['confidence']
            market_analysis['factors_analyzed'] = market_risk_factors
            market_analysis['market_state'] = market_state
            market_analysis['detected_trap_type'] = known_trap_type
            market_analysis['trap_description'] = detected_trap['description']
            
            # Déterminer si ce piège présente une opportunité de valeur
            value_opportunity = self._find_value_in_trap(
                market_name, market_odds, detected_trap, market_risk_factors
            )
            
            if value_opportunity:
                market_analysis['value_opportunities'].append(value_opportunity)
                
                if len(value_opportunity.get('bet', '')) > 0:
                    market_analysis['recommended_bet'] = value_opportunity['bet']
                    market_analysis['value_rating'] = value_opportunity['value_rating']
        else:
            # Aucun facteur de risque détecté
            market_analysis['market_state'] = 'normal'
            market_analysis['trap_risk'] = 0.2  # Risque de base faible
            market_analysis['detection_confidence'] = 0.5
        
        return market_analysis
    
    def _find_value_in_trap(self, market_name, market_odds, main_trap_factor, all_risk_factors):
        """
        Identifie si un piège à parieurs contient paradoxalement une opportunité de valeur.
        
        Args:
            market_name (str): Nom du marché
            market_odds (dict): Cotes du marché
            main_trap_factor (dict): Facteur principal du piège
            all_risk_factors (list): Tous les facteurs de risque
            
        Returns:
            dict or None: Opportunité de valeur identifiée, ou None
        """
        # Pas d'opportunité par défaut
        if not main_trap_factor or 'favors' not in main_trap_factor:
            return None
        
        try:
            # Déterminer l'option favorisée par le facteur principal
            favored = main_trap_factor['favors']
            
            # Pour le marché 1X2
            if market_name == '1X2' or market_name == 'Match Result':
                home_odds = market_odds.get('1', market_odds.get('home', 0))
                draw_odds = market_odds.get('X', market_odds.get('draw', 0))
                away_odds = market_odds.get('2', market_odds.get('away', 0))
                
                # Si un facteur favorise clairement une équipe
                if favored in ['home', 'away'] or favored not in ['both', 'opposite']:
                    # Option de valeur potentielle
                    if favored == 'home' or (isinstance(favored, str) and 'home' in favored.lower()):
                        value_rating = min(0.9, main_trap_factor['severity'] * 0.8 + 0.3)
                        return {
                            'bet': '1' if '1' in market_odds else 'home',
                            'odds': home_odds,
                            'description': f"Opportunité de valeur sur la victoire à domicile, négligée par le marché",
                            'value_rating': value_rating
                        }
                    elif favored == 'away' or (isinstance(favored, str) and 'away' in favored.lower()):
                        value_rating = min(0.9, main_trap_factor['severity'] * 0.8 + 0.3)
                        return {
                            'bet': '2' if '2' in market_odds else 'away',
                            'odds': away_odds,
                            'description': f"Opportunité de valeur sur la victoire à l'extérieur, négligée par le marché",
                            'value_rating': value_rating
                        }
            
            # Pour d'autres marchés, une analyse plus contextualisée serait nécessaire
            
        except Exception as e:
            logger.error(f"Erreur lors de la recherche d'opportunités de valeur: {e}")
        
        return None
    
    def _generate_betting_recommendations(self, safe_markets, high_risk_markets, odds_data, team_analyses):
        """
        Génère des recommandations de paris basées sur l'analyse des pièges.
        
        Args:
            safe_markets (list): Marchés considérés comme sûrs
            high_risk_markets (list): Marchés à haut risque
            odds_data (dict): Données de cotes complètes
            team_analyses (dict): Analyses des équipes
            
        Returns:
            list: Recommandations de paris
        """
        recommendations = []
        
        # Générer des recommandations basées sur les opportunités de valeur dans les marchés sûrs
        value_opportunities = sorted(
            [market for market in safe_markets if 'value_rating' in market],
            key=lambda x: x['value_rating'],
            reverse=True
        )
        
        for opportunity in value_opportunities[:2]:  # Top 2 des opportunités
            recommendations.append({
                'market': opportunity['market'],
                'bet': opportunity['recommendation'],
                'confidence': min(0.9, opportunity['value_rating'] * 1.2),
                'reasoning': f"Opportunité de valeur identifiée sur {opportunity['market']} ({opportunity['recommendation']})",
                'risk_level': 'low',
                'avoid_reason': None
            })
        
        # Recommandations d'évitement pour les marchés à haut risque
        for market in high_risk_markets[:3]:  # Top 3 des marchés à risque
            recommendations.append({
                'market': market['market'],
                'bet': 'ÉVITER',
                'confidence': min(0.9, market['risk'] * 1.1),
                'reasoning': f"Piège de paris identifié: {market['description']}",
                'risk_level': 'high',
                'avoid_reason': market['description']
            })
        
        # Ajouter des recommandations basées sur l'analyse des équipes
        if team_analyses and 'home' in team_analyses and 'away' in team_analyses:
            home_analysis = team_analyses['home']
            away_analysis = team_analyses['away']
            
            if 'form_analysis' in home_analysis and 'form_analysis' in away_analysis:
                home_form = home_analysis['form_analysis'].get('form_quality', 0.5)
                away_form = away_analysis['form_analysis'].get('form_quality', 0.5)
                
                # Si l'écart de forme est significatif
                if abs(home_form - away_form) > 0.3:
                    better_form = 'home' if home_form > away_form else 'away'
                    worse_form = 'away' if better_form == 'home' else 'home'
                    
                    form_diff = abs(home_form - away_form)
                    confidence = min(0.8, 0.5 + form_diff)
                    
                    # Vérifier si ce n'est pas un piège déjà identifié
                    is_trap = any(
                        market['market'] == '1X2' and 
                        ('home' in market['description'] or 'away' in market['description'])
                        for market in high_risk_markets
                    )
                    
                    if not is_trap and '1X2' in odds_data:
                        bet_option = '1' if better_form == 'home' else '2'
                        
                        recommendations.append({
                            'market': '1X2',
                            'bet': bet_option,
                            'confidence': confidence,
                            'reasoning': f"Écart significatif de forme en faveur de l'équipe {better_form}",
                            'risk_level': 'medium',
                            'avoid_reason': None
                        })
                
                # Recommandations de buts basées sur les profils des équipes
                if 'team_stats' in home_analysis and 'team_stats' in away_analysis:
                    home_goals_scored = home_analysis['team_stats'].get('goals_scored', 0)
                    home_goals_conceded = home_analysis['team_stats'].get('goals_conceded', 0)
                    away_goals_scored = away_analysis['team_stats'].get('goals_scored', 0)
                    away_goals_conceded = away_analysis['team_stats'].get('goals_conceded', 0)
                    
                    # Estimer le nombre total de buts
                    expected_goals = (home_goals_scored * 0.6 + away_goals_conceded * 0.4 +
                                    away_goals_scored * 0.5 + home_goals_conceded * 0.5) / 2
                    
                    # Recommandation basée sur les buts attendus
                    goals_market = None
                    for market_name in odds_data.keys():
                        if 'Over/Under' in market_name or 'Goals' in market_name:
                            goals_market = market_name
                            break
                    
                    if goals_market and goals_market not in [m['market'] for m in high_risk_markets]:
                        if expected_goals > 3:
                            recommendations.append({
                                'market': goals_market,
                                'bet': 'Over',
                                'confidence': min(0.8, 0.5 + (expected_goals - 2.5) * 0.2),
                                'reasoning': f"Profils offensifs des équipes suggèrent un match ouvert",
                                'risk_level': 'medium',
                                'avoid_reason': None
                            })
                        elif expected_goals < 2:
                            recommendations.append({
                                'market': goals_market,
                                'bet': 'Under',
                                'confidence': min(0.8, 0.5 + (2.5 - expected_goals) * 0.2),
                                'reasoning': f"Profils défensifs des équipes suggèrent un match fermé",
                                'risk_level': 'medium',
                                'avoid_reason': None
                            })
        
        return recommendations
    
    def _simulate_odds_data(self, home_team, away_team):
        """
        Simule des données de cotes pour un match lorsque les données réelles ne sont pas disponibles.
        
        Args:
            home_team (str): Nom de l'équipe à domicile
            away_team (str): Nom de l'équipe à l'extérieur
            
        Returns:
            dict: Données de cotes simulées
        """
        # Paramètres de simulation
        home_strength = random.uniform(0.5, 0.8)  # Force à domicile
        away_strength = random.uniform(0.4, 0.7)  # Force à l'extérieur
        
        # Ajuster les forces en fonction des noms d'équipe connus
        big_teams = ['Barcelona', 'Real Madrid', 'Manchester City', 'Liverpool', 
                    'Bayern Munich', 'Paris Saint-Germain', 'Juventus']
        
        if home_team in big_teams:
            home_strength += random.uniform(0.05, 0.15)
        if away_team in big_teams:
            away_strength += random.uniform(0.05, 0.15)
        
        # Normaliser les forces
        home_strength = min(0.9, home_strength)
        away_strength = min(0.8, away_strength)
        
        # Calculer les probabilités de base
        home_win_prob = home_strength * (1 - away_strength * 0.7)
        away_win_prob = away_strength * (1 - home_strength * 0.8)
        draw_prob = 1 - home_win_prob - away_win_prob
        
        # Ajuster pour éviter les valeurs négatives
        if draw_prob < 0.1:
            deficit = 0.1 - draw_prob
            home_win_prob -= deficit * 0.6
            away_win_prob -= deficit * 0.4
            draw_prob = 0.1
        
        # Calculer les cotes (avec une marge de bookmaker de ~7%)
        margin = 1.07
        home_odds = round((1 / home_win_prob) * margin, 2)
        draw_odds = round((1 / draw_prob) * margin, 2)
        away_odds = round((1 / away_win_prob) * margin, 2)
        
        # Probabilité de marquer des buts
        goals_expectation = home_strength * 1.3 + away_strength * 1.0
        over_prob = 0.5 + (goals_expectation - 2.5) * 0.2
        over_prob = max(0.3, min(0.7, over_prob))
        under_prob = 1 - over_prob
        
        over_odds = round((1 / over_prob) * margin, 2)
        under_odds = round((1 / under_prob) * margin, 2)
        
        # Générer les données de cotes
        odds_data = {
            '1X2': {
                '1': home_odds,
                'X': draw_odds,
                '2': away_odds
            },
            'Over/Under 2.5': {
                'Over': over_odds,
                'Under': under_odds
            },
            'Double Chance': {
                '1X': round(1 / (home_win_prob + draw_prob) * margin, 2),
                '12': round(1 / (home_win_prob + away_win_prob) * margin, 2),
                'X2': round(1 / (draw_prob + away_win_prob) * margin, 2)
            },
            'Both Teams to Score': {
                'Yes': round(1 / (0.5 + goals_expectation * 0.05) * margin, 2),
                'No': round(1 / (0.5 - goals_expectation * 0.05) * margin, 2)
            }
        }
        
        return odds_data