"""
BetTrapMap - Module de cartographie des pièges à mise dans l'écosystème des paris sportifs.
Analyse les configurations propices aux trappes à parieurs et identifie les paris à éviter.
Intègre des données réelles de Transfermarkt pour une analyse plus précise.
"""

import random
from datetime import datetime, timedelta
import numpy as np
import logging
from collections import defaultdict

# Intégration de l'adaptateur Transfermarkt
from api.transfermarkt_adapter import TransfermarktAdapter

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BetTrapMap:
    """
    BetTrapMap - Système d'analyse et de cartographie des pièges à mise.
    
    Ce module identifie et catégorise les configurations de paris potentiellement 
    piégeuses en analysant les anomalies dans les cotes, les comportements des parieurs
    et les distorsions statistiques.
    """
    
    def __init__(self):
        """Initialise le module BetTrapMap avec l'adaptateur Transfermarkt"""
        # Initialiser l'adaptateur Transfermarkt pour obtenir des données réelles
        self.transfermarkt = TransfermarktAdapter()
        logger.info("Initialisation de l'adaptateur Transfermarkt pour BetTrapMap")
        self.use_real_data = self.transfermarkt.api_online
        
        if self.use_real_data:
            logger.info("BetTrapMap utilisera les données réelles de Transfermarkt")
        else:
            logger.warning("API Transfermarkt non disponible, BetTrapMap utilisera des données simulées")
        
        # Paramètres de détection
        self.detection_params = {
            'odds_anomaly_threshold': 0.2,       # Seuil d'anomalie dans les cotes
            'volume_imbalance_threshold': 0.7,   # Seuil de déséquilibre de volume
            'odds_movement_significance': 0.15,  # Seuil de mouvement significatif des cotes
            'historical_trap_weight': 0.4,       # Poids des pièges historiques
            'confidence_threshold': 0.75,        # Seuil de confiance pour signaler un piège
            'min_trap_severity': 0.6,            # Sévérité minimale pour un piège significatif
            'max_safe_markets': 3                # Nombre max de marchés "sûrs" à recommander
        }
        
        # Types de pièges connus
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
            }
        }
        
        # États de marchés pour l'identification des pièges
        self.market_states = [
            'normal',               # État normal, pas d'anomalie
            'suspicious',           # Activité suspecte mais pas confirmée
            'probable_trap',        # Forte probabilité de piège
            'confirmed_trap',       # Piège confirmé par plusieurs indicateurs
            'manipulated',          # Marché clairement manipulé
            'correcting',           # Marché en phase de correction
            'value_opportunity'     # Opportunité de valeur (anti-piège)
        ]
        
        # Historique des pièges détectés
        self.trap_history = []
        
    def analyze_team_data(self, team_id):
        """
        Analyse les données d'une équipe à partir de Transfermarkt pour détecter des facteurs
        pouvant influencer les pièges de paris.
        
        Args:
            team_id (str): ID de l'équipe dans Transfermarkt
            
        Returns:
            dict: Analyse des facteurs de l'équipe liés aux pièges
        """
        analysis = {
            'team_id': team_id,
            'timestamp': datetime.now().isoformat(),
            'factors_analyzed': 0,
            'key_factors': [],
            'player_factors': [],
            'team_stability': 0.0,
            'consistency_score': 0.0,
            'overall_trap_risk': 0.0
        }
        
        # Récupérer les données de l'équipe seulement si l'API est disponible
        if not self.use_real_data or not team_id:
            analysis['error'] = "Impossible d'analyser l'équipe: données Transfermarkt non disponibles"
            return analysis
            
        try:
            # Récupérer le profil du club et ses joueurs
            club_profile = self.transfermarkt.get_club_profile(team_id)
            if 'status' in club_profile and club_profile['status'] == 'error':
                analysis['error'] = f"Erreur lors de la récupération du profil du club: {club_profile.get('message', '')}"
                return analysis
                
            club_players = self.transfermarkt.get_club_players(team_id)
            if 'status' in club_players and club_players['status'] == 'error':
                analysis['error'] = f"Erreur lors de la récupération des joueurs du club: {club_players.get('message', '')}"
                return analysis
                
            # Extraire les informations clés du club
            club_name = club_profile.get('name', 'Inconnu')
            league = club_profile.get('league', 'Inconnue')
            
            analysis['team_name'] = club_name
            analysis['league'] = league
            
            # Analyser la stabilité de l'équipe (basée sur les transferts récents)
            squad = club_players.get('squad', [])
            recent_transfers_count = 0
            key_player_changes = 0
            
            for player in squad:
                if isinstance(player, dict):
                    # Vérifier si le joueur a été transféré récemment
                    join_date = player.get('join_date')
                    if join_date:
                        try:
                            # Format de date peut varier, essayer plusieurs formats
                            try:
                                join_datetime = datetime.strptime(join_date, '%Y-%m-%d')
                            except:
                                try:
                                    join_datetime = datetime.strptime(join_date, '%d/%m/%Y')
                                except:
                                    join_datetime = datetime.strptime(join_date, '%b %d, %Y')
                                
                            # Considérer comme récent si moins de 3 mois
                            if (datetime.now() - join_datetime).days <= 90:
                                recent_transfers_count += 1
                                
                                # Si c'est un joueur clé (basé sur la valeur marchande ou le statut)
                                market_value = player.get('market_value', 0)
                                if isinstance(market_value, str):
                                    try:
                                        # Convertir en nombre
                                        market_value = float(''.join(c for c in market_value if c.isdigit() or c == '.'))
                                    except:
                                        market_value = 0
                                
                                if market_value > 10000000:  # 10M+ = joueur clé
                                    key_player_changes += 1
                                    
                                    # Ajouter aux facteurs de joueur
                                    analysis['player_factors'].append({
                                        'player_name': player.get('name', 'Inconnu'),
                                        'transfer_type': 'arrivée',
                                        'date': join_date,
                                        'importance': min(1.0, market_value / 50000000),  # Normaliser sur 50M
                                        'impact_description': "Nouveau joueur clé, peut affecter la dynamique d'équipe"
                                    })
                        except Exception as e:
                            logger.warning(f"Erreur lors de l'analyse de la date de transfert: {e}")
            
            # Calculer le score de stabilité (inverse des changements récents)
            team_size = len(squad) if squad else 25  # Valeur par défaut
            stability_score = 1.0 - min(0.9, (recent_transfers_count / team_size) * 1.5)
            consistency_score = 1.0 - min(0.9, (key_player_changes / 5) * 1.2)  # 5+ changements clés = instabilité majeure
            
            analysis['team_stability'] = stability_score
            analysis['consistency_score'] = consistency_score
            
            # Ajouter aux facteurs clés
            if recent_transfers_count > 0:
                analysis['key_factors'].append({
                    'factor_type': 'team_composition',
                    'description': f"{recent_transfers_count} transferts récents",
                    'impact_score': 1.0 - stability_score,
                    'trap_correlation': 0.7 if key_player_changes > 2 else 0.4
                })
            
            # Intégrer à l'analyse globale du risque de piège
            factors_analyzed = 1  # Le facteur de stabilité
            trap_risk = (1.0 - stability_score) * 0.6 + (1.0 - consistency_score) * 0.4
            
            # Finaliser l'analyse
            analysis['factors_analyzed'] = factors_analyzed
            analysis['overall_trap_risk'] = trap_risk
            
            logger.info(f"Analyse Transfermarkt complétée pour {club_name}: score de stabilité {stability_score:.2f}")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse des données d'équipe: {e}")
            analysis['error'] = f"Erreur lors de l'analyse: {str(e)}"
            
        return analysis
        
    def analyze_market_traps(self, match_data, odds_data=None, betting_volumes=None, historical_data=None):
        """
        Analyser les pièges potentiels sur tous les marchés d'un match.
        Utilise les données de Transfermarkt pour enrichir l'analyse si disponibles.
        
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
            'team_analyses': {}                # Analyses des équipes (Transfermarkt)
        }
        
        # Enrichir avec des données Transfermarkt si possible
        if self.use_real_data:
            # Récupérer des données d'équipe si IDs disponibles
            home_team_id = match_data.get('home_team_id')
            away_team_id = match_data.get('away_team_id')
            
            if home_team_id:
                try:
                    logger.info(f"BetTrapMap: Analyse des données Transfermarkt pour l'équipe domicile {home_team_id}")
                    home_analysis = self.analyze_team_data(home_team_id)
                    if 'error' not in home_analysis:
                        trap_analysis['team_analyses']['home'] = home_analysis
                        logger.info(f"Analyse Transfermarkt intégrée pour {home_team}")
                except Exception as e:
                    logger.error(f"Erreur lors de l'analyse Transfermarkt pour {home_team}: {e}")
            
            if away_team_id:
                try:
                    logger.info(f"BetTrapMap: Analyse des données Transfermarkt pour l'équipe extérieure {away_team_id}")
                    away_analysis = self.analyze_team_data(away_team_id)
                    if 'error' not in away_analysis:
                        trap_analysis['team_analyses']['away'] = away_analysis
                        logger.info(f"Analyse Transfermarkt intégrée pour {away_team}")
                except Exception as e:
                    logger.error(f"Erreur lors de l'analyse Transfermarkt pour {away_team}: {e}")
                    
            # Calculer un facteur d'instabilité d'équipe pour l'analyse des pièges
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
                logger.info(f"Facteur d'instabilité d'équipe: {team_instability_factor:.2f}")
        else:
            logger.info("Analyse Transfermarkt non disponible pour ce match")
        
        # Obtenir ou simuler les données des cotes
        odds_data = odds_data or self._simulate_odds_data(home_team, away_team)
        
        # Obtenir ou simuler les volumes de paris
        betting_volumes = betting_volumes or self._simulate_betting_volumes(odds_data)
        
        # Obtenir ou simuler les données historiques
        historical_data = historical_data or self._simulate_historical_data(home_team, away_team)
        
        # Analyser chaque marché
        for market_name, market_odds in odds_data.items():
            market_analysis = self._analyze_market(
                market_name, market_odds, 
                betting_volumes.get(market_name, {}),
                historical_data.get(market_name, {}),
                match_data
            )
            
            trap_analysis['market_analysis'][market_name] = market_analysis
            
            # Si un piège est détecté, l'ajouter à la liste
            if market_analysis.get('trap_detected', False):
                trap_info = {
                    'market': market_name,
                    'trap_type': market_analysis.get('trap_type'),
                    'severity': market_analysis.get('trap_severity', 0.0),
                    'confidence': market_analysis.get('detection_confidence', 0.0),
                    'description': market_analysis.get('trap_description', '')
                }
                trap_analysis['traps_detected'].append(trap_info)
                
                # Ajouter aux marchés à haut risque si sévérité élevée
                if market_analysis.get('trap_severity', 0.0) >= self.detection_params['min_trap_severity']:
                    trap_analysis['high_risk_markets'].append({
                        'market': market_name,
                        'risk_level': market_analysis.get('trap_severity', 0.0),
                        'warning': market_analysis.get('trap_description', '')
                    })
            else:
                # Si pas de piège, vérifier si c'est un marché sûr
                safety_score = market_analysis.get('market_safety_score', 0.0)
                if safety_score > 0.7:
                    trap_analysis['safe_markets'].append({
                        'market': market_name,
                        'safety_score': safety_score,
                        'recommendation': market_analysis.get('betting_advice', '')
                    })
        
        # Trier les marchés sûrs par score de sécurité et limiter le nombre
        trap_analysis['safe_markets'].sort(key=lambda x: x.get('safety_score', 0), reverse=True)
        trap_analysis['safe_markets'] = trap_analysis['safe_markets'][:self.detection_params['max_safe_markets']]
        
        # Trier les marchés à risque par niveau de risque
        trap_analysis['high_risk_markets'].sort(key=lambda x: x.get('risk_level', 0), reverse=True)
        
        # Calculer le niveau global de risque
        if trap_analysis['traps_detected']:
            risk_values = [trap.get('severity', 0) * trap.get('confidence', 0) 
                          for trap in trap_analysis['traps_detected']]
            trap_analysis['trap_risk_level'] = sum(risk_values) / len(risk_values)
        
        # Générer des recommandations de paris
        trap_analysis['betting_recommendations'] = self._generate_betting_recommendations(
            trap_analysis['safe_markets'],
            trap_analysis['high_risk_markets'],
            match_data
        )
        
        # Ajouter à l'historique
        self.trap_history.append({
            'match': f"{home_team} vs {away_team}",
            'date': match_date,
            'traps_count': len(trap_analysis['traps_detected']),
            'risk_level': trap_analysis['trap_risk_level'],
            'markets_analyzed': len(odds_data)
        })
        
        return trap_analysis
    
    def evaluate_trap_presence(self, match_data, market_name, odds_data=None):
        """
        Évaluer la présence d'un piège sur un marché spécifique.
        
        Args:
            match_data (dict): Données du match
            market_name (str): Nom du marché à analyser
            odds_data (dict, optional): Données de cotes pour ce marché
            
        Returns:
            dict: Évaluation de la présence de piège
        """
        # Base de l'évaluation
        evaluation = {
            'market': market_name,
            'match': f"{match_data.get('home_team', 'Équipe 1')} vs {match_data.get('away_team', 'Équipe 2')}",
            'trap_detected': False,
            'trap_probability': 0.0,
            'trap_type': None,
            'warning_signs': [],
            'safety_indicators': [],
            'recommendation': ''
        }
        
        # Obtenir ou simuler les données des cotes pour ce marché
        if odds_data is None:
            odds_data = self._simulate_odds_data(
                match_data.get('home_team', 'Équipe 1'),
                match_data.get('away_team', 'Équipe 2')
            ).get(market_name, {})
            
            # Si même la simulation ne produit pas de données, retourner évaluation par défaut
            if not odds_data:
                evaluation['recommendation'] = "Données insuffisantes pour évaluer ce marché"
                return evaluation
        
        # Simuler les volumes et historique pour l'analyse
        betting_volumes = self._simulate_betting_volumes({market_name: odds_data}).get(market_name, {})
        historical_data = self._simulate_historical_data(
            match_data.get('home_team', 'Équipe 1'),
            match_data.get('away_team', 'Équipe 2')
        ).get(market_name, {})
        
        # Effectuer l'analyse complète du marché
        market_analysis = self._analyze_market(
            market_name, odds_data, betting_volumes, historical_data, match_data
        )
        
        # Transférer les résultats de l'analyse
        evaluation['trap_detected'] = market_analysis.get('trap_detected', False)
        evaluation['trap_probability'] = market_analysis.get('detection_confidence', 0.0)
        evaluation['trap_type'] = market_analysis.get('trap_type')
        evaluation['warning_signs'] = market_analysis.get('warning_signs', [])
        evaluation['safety_indicators'] = market_analysis.get('safety_indicators', [])
        
        # Générer une recommandation
        if evaluation['trap_detected']:
            trap_severity = market_analysis.get('trap_severity', 0.0)
            evaluation['recommendation'] = f"ÉVITER ce marché - {market_analysis.get('trap_description', 'Piège détecté')}"
            
            if trap_severity > 0.8:
                evaluation['recommendation'] += " - Risque extrêmement élevé"
            elif trap_severity > 0.6:
                evaluation['recommendation'] += " - Risque élevé"
            else:
                evaluation['recommendation'] += " - Risque modéré"
        else:
            safety_score = market_analysis.get('market_safety_score', 0.0)
            
            if safety_score > 0.8:
                evaluation['recommendation'] = "Marché considéré comme sûr - Aucun piège détecté"
            elif safety_score > 0.6:
                evaluation['recommendation'] = "Marché probablement sûr - Faible risque de piège"
            else:
                evaluation['recommendation'] = "Données insuffisantes ou incertitudes - Procéder avec prudence"
        
        return evaluation
    
    def identify_trap_patterns(self, timeframe='recent', team_name=None, market_type=None):
        """
        Identifier des patterns récurrents de pièges.
        
        Args:
            timeframe (str): Période d'analyse ('recent', 'season', 'all')
            team_name (str, optional): Filtrer par équipe
            market_type (str, optional): Filtrer par type de marché
            
        Returns:
            dict: Patterns de pièges identifiés
        """
        # Base de l'analyse
        pattern_analysis = {
            'timeframe': timeframe,
            'team_filter': team_name,
            'market_filter': market_type,
            'patterns_identified': [],
            'trap_frequency': {},
            'team_vulnerability': {},
            'market_vulnerability': {},
            'temporal_patterns': []
        }
        
        # Simuler l'historique des pièges pour l'analyse
        # Dans une implémentation réelle, cela viendrait de données stockées
        trap_history = self._simulate_trap_history(timeframe, team_name, market_type)
        
        # Analyser la fréquence des types de piège
        trap_type_count = defaultdict(int)
        total_traps = 0
        
        for trap in trap_history:
            if 'trap_type' in trap:
                trap_type_count[trap['trap_type']] += 1
                total_traps += 1
        
        # Calculer les fréquences
        if total_traps > 0:
            for trap_type, count in trap_type_count.items():
                pattern_analysis['trap_frequency'][trap_type] = count / total_traps
        
        # Analyser la vulnérabilité des équipes
        team_trap_count = defaultdict(int)
        team_match_count = defaultdict(int)
        
        for trap in trap_history:
            if 'home_team' in trap and 'away_team' in trap:
                team_trap_count[trap['home_team']] += 1
                team_trap_count[trap['away_team']] += 1
                team_match_count[trap['home_team']] += 1
                team_match_count[trap['away_team']] += 1
        
        # Calculer le taux de vulnérabilité
        for team, trap_count in team_trap_count.items():
            match_count = team_match_count[team]
            if match_count > 0:
                pattern_analysis['team_vulnerability'][team] = trap_count / match_count
        
        # Analyser la vulnérabilité des marchés
        market_trap_count = defaultdict(int)
        market_analysis_count = defaultdict(int)
        
        for trap in trap_history:
            if 'market' in trap:
                market_trap_count[trap['market']] += 1
                market_analysis_count[trap['market']] += 1
        
        # Calculer le taux de vulnérabilité
        for market, trap_count in market_trap_count.items():
            analysis_count = market_analysis_count[market]
            if analysis_count > 0:
                pattern_analysis['market_vulnerability'][market] = trap_count / analysis_count
        
        # Identifier des patterns temporels
        if len(trap_history) > 5:
            # Analyser par jour de la semaine
            day_trap_counts = defaultdict(int)
            day_match_counts = defaultdict(int)
            
            for trap in trap_history:
                if 'date' in trap:
                    try:
                        trap_date = datetime.fromisoformat(trap['date'])
                        day_of_week = trap_date.strftime('%A')
                        
                        day_trap_counts[day_of_week] += 1
                        day_match_counts[day_of_week] += 1
                    except:
                        pass
            
            # Calculer les taux par jour
            for day, trap_count in day_trap_counts.items():
                match_count = day_match_counts[day]
                if match_count > 5:  # Seuil minimum pour être significatif
                    trap_rate = trap_count / match_count
                    
                    # Ajouter si le taux est significativement différent de la moyenne
                    avg_rate = total_traps / sum(day_match_counts.values())
                    if abs(trap_rate - avg_rate) > 0.15:
                        temporal_pattern = {
                            'type': 'day_of_week',
                            'value': day,
                            'trap_rate': trap_rate,
                            'comparison_to_avg': trap_rate / avg_rate if avg_rate > 0 else 1.0,
                            'significance': abs(trap_rate - avg_rate) / avg_rate if avg_rate > 0 else 0.0
                        }
                        pattern_analysis['temporal_patterns'].append(temporal_pattern)
        
        # Identifier des patterns significatifs
        significant_patterns = []
        
        # Patterns basés sur les types de piège
        for trap_type, frequency in pattern_analysis['trap_frequency'].items():
            if frequency > 0.2:  # Seuil de fréquence significative
                pattern = {
                    'pattern_type': 'trap_type_frequency',
                    'trap_type': trap_type,
                    'frequency': frequency,
                    'description': f"Fréquence élevée du piège '{trap_type}': {frequency:.1%}",
                    'significance': frequency
                }
                significant_patterns.append(pattern)
        
        # Patterns basés sur la vulnérabilité des équipes
        for team, vulnerability in pattern_analysis['team_vulnerability'].items():
            if vulnerability > 0.25:  # Seuil de vulnérabilité significative
                pattern = {
                    'pattern_type': 'team_vulnerability',
                    'team': team,
                    'vulnerability_rate': vulnerability,
                    'description': f"Vulnérabilité élevée de l'équipe {team}: {vulnerability:.1%}",
                    'significance': vulnerability
                }
                significant_patterns.append(pattern)
        
        # Patterns basés sur la vulnérabilité des marchés
        for market, vulnerability in pattern_analysis['market_vulnerability'].items():
            if vulnerability > 0.3:  # Seuil de vulnérabilité significative
                pattern = {
                    'pattern_type': 'market_vulnerability',
                    'market': market,
                    'vulnerability_rate': vulnerability,
                    'description': f"Vulnérabilité élevée du marché {market}: {vulnerability:.1%}",
                    'significance': vulnerability
                }
                significant_patterns.append(pattern)
        
        # Ajouter les patterns temporels identifiés
        for temporal_pattern in pattern_analysis['temporal_patterns']:
            if temporal_pattern['significance'] > 0.2:  # Seuil de signification
                pattern = {
                    'pattern_type': 'temporal_pattern',
                    'pattern_subtype': temporal_pattern['type'],
                    'value': temporal_pattern['value'],
                    'trap_rate': temporal_pattern['trap_rate'],
                    'description': f"Taux de piège anormal pour {temporal_pattern['value']}: {temporal_pattern['trap_rate']:.1%}",
                    'significance': temporal_pattern['significance']
                }
                significant_patterns.append(pattern)
        
        # Trier par signification
        significant_patterns.sort(key=lambda x: x.get('significance', 0), reverse=True)
        pattern_analysis['patterns_identified'] = significant_patterns
        
        return pattern_analysis
    
    def generate_trap_avoidance_strategy(self, upcoming_matches, historical_patterns=None):
        """
        Générer une stratégie d'évitement des pièges pour des matchs à venir.
        
        Args:
            upcoming_matches (list): Liste des matchs à venir
            historical_patterns (dict, optional): Patterns historiques identifiés
            
        Returns:
            dict: Stratégie d'évitement des pièges
        """
        # Base de la stratégie
        strategy = {
            'analysis_timestamp': datetime.now().isoformat(),
            'matches_analyzed': len(upcoming_matches),
            'global_warnings': [],
            'match_strategies': {},
            'high_risk_situations': [],
            'global_recommendations': []
        }
        
        # Utiliser les patterns historiques fournis ou simuler des patterns
        if historical_patterns is None:
            historical_patterns = self.identify_trap_patterns()
        
        # Ajouter des avertissements globaux basés sur les patterns
        for pattern in historical_patterns.get('patterns_identified', []):
            if pattern.get('significance', 0) > 0.5:
                strategy['global_warnings'].append({
                    'warning_type': pattern.get('pattern_type'),
                    'description': pattern.get('description', ''),
                    'significance': pattern.get('significance', 0)
                })
        
        # Analyser chaque match à venir
        for match in upcoming_matches:
            home_team = match.get('home_team', 'Équipe domicile')
            away_team = match.get('away_team', 'Équipe extérieure')
            match_date = match.get('date', datetime.now().isoformat())
            
            # Vérifier la vulnérabilité des équipes
            team_vulnerabilities = historical_patterns.get('team_vulnerability', {})
            home_vulnerability = team_vulnerabilities.get(home_team, 0)
            away_vulnerability = team_vulnerabilities.get(away_team, 0)
            
            # Base de l'analyse par match
            match_strategy = {
                'match': f"{home_team} vs {away_team}",
                'date': match_date,
                'risk_assessment': {
                    'overall_risk': 0.0,
                    'team_risk_factors': [],
                    'temporal_risk_factors': []
                },
                'markets_to_avoid': [],
                'safer_alternatives': [],
                'recommendations': []
            }
            
            # Évaluer les facteurs de risque liés aux équipes
            if home_vulnerability > 0.2:
                match_strategy['risk_assessment']['team_risk_factors'].append({
                    'team': home_team,
                    'vulnerability': home_vulnerability,
                    'description': f"{home_team} présente une vulnérabilité historique aux pièges"
                })
            
            if away_vulnerability > 0.2:
                match_strategy['risk_assessment']['team_risk_factors'].append({
                    'team': away_team,
                    'vulnerability': away_vulnerability,
                    'description': f"{away_team} présente une vulnérabilité historique aux pièges"
                })
            
            # Évaluer les facteurs de risque temporels
            try:
                match_datetime = datetime.fromisoformat(match_date)
                day_of_week = match_datetime.strftime('%A')
                
                # Vérifier si ce jour présente un risque particulier
                for pattern in historical_patterns.get('temporal_patterns', []):
                    if pattern.get('type') == 'day_of_week' and pattern.get('value') == day_of_week:
                        if pattern.get('trap_rate', 0) > 0.3:
                            match_strategy['risk_assessment']['temporal_risk_factors'].append({
                                'factor_type': 'day_of_week',
                                'value': day_of_week,
                                'trap_rate': pattern.get('trap_rate', 0),
                                'description': f"Jour à risque élevé de pièges: {day_of_week}"
                            })
            except:
                pass
            
            # Analyser les marchés à risque pour ce match
            market_vulnerabilities = historical_patterns.get('market_vulnerability', {})
            
            for market, vulnerability in market_vulnerabilities.items():
                if vulnerability > 0.3:
                    match_strategy['markets_to_avoid'].append({
                        'market': market,
                        'vulnerability': vulnerability,
                        'reason': f"Vulnérabilité historique élevée: {vulnerability:.1%}"
                    })
            
            # Suggérer des alternatives plus sûres
            safer_markets = [m for m, v in market_vulnerabilities.items() if v < 0.15]
            safer_markets = safer_markets[:3]  # Limiter à 3 suggestions
            
            for market in safer_markets:
                match_strategy['safer_alternatives'].append({
                    'market': market,
                    'safety_score': 1.0 - market_vulnerabilities.get(market, 0),
                    'description': f"Alternative plus sûre avec historique favorable"
                })
            
            # Calculer le risque global
            team_risk = max(home_vulnerability, away_vulnerability)
            temporal_risk = max([f.get('trap_rate', 0) for f in match_strategy['risk_assessment']['temporal_risk_factors']], default=0)
            market_risk = max([m.get('vulnerability', 0) for m in match_strategy['markets_to_avoid']], default=0)
            
            # Pondérer les différents risques
            match_strategy['risk_assessment']['overall_risk'] = (
                team_risk * 0.4 + 
                temporal_risk * 0.3 + 
                market_risk * 0.3
            )
            
            # Générer des recommandations basées sur le niveau de risque
            if match_strategy['risk_assessment']['overall_risk'] > 0.6:
                match_strategy['recommendations'].append(
                    "HAUTE VIGILANCE - Match présentant plusieurs facteurs de risque élevés de pièges"
                )
                match_strategy['recommendations'].append(
                    "Éviter complètement les marchés à haut risque identifiés"
                )
                
                # Ajouter aux situations à haut risque
                strategy['high_risk_situations'].append({
                    'match': f"{home_team} vs {away_team}",
                    'date': match_date,
                    'risk_level': match_strategy['risk_assessment']['overall_risk'],
                    'primary_factors': [
                        f['description'] for f in match_strategy['risk_assessment']['team_risk_factors'] +
                        match_strategy['risk_assessment']['temporal_risk_factors']
                    ][:2]  # Limiter aux 2 facteurs principaux
                })
            elif match_strategy['risk_assessment']['overall_risk'] > 0.3:
                match_strategy['recommendations'].append(
                    "PRUDENCE - Risque modéré de pièges dans certains marchés"
                )
                match_strategy['recommendations'].append(
                    "Réduire les mises et se concentrer sur les marchés alternatifs plus sûrs"
                )
            else:
                match_strategy['recommendations'].append(
                    "RISQUE STANDARD - Aucun facteur de risque particulier identifié"
                )
                match_strategy['recommendations'].append(
                    "Appliquer les principes habituels de gestion de bankroll et d'analyse"
                )
            
            # Ajouter la stratégie de ce match à la stratégie globale
            strategy['match_strategies'][f"{home_team} vs {away_team}"] = match_strategy
        
        # Trier les situations à haut risque
        strategy['high_risk_situations'].sort(key=lambda x: x.get('risk_level', 0), reverse=True)
        
        # Générer des recommandations globales
        if strategy['high_risk_situations']:
            strategy['global_recommendations'].append(
                "Plusieurs situations à haut risque détectées - Redoubler de prudence dans cette période"
            )
            
            if len(strategy['high_risk_situations']) / len(upcoming_matches) > 0.3:
                strategy['global_recommendations'].append(
                    "Considérer une réduction temporaire de l'exposition globale au marché"
                )
        
        # Ajouter des recommandations basées sur les patterns historiques
        frequent_trap_types = [(t, f) for t, f in historical_patterns.get('trap_frequency', {}).items() if f > 0.2]
        if frequent_trap_types:
            top_trap = max(frequent_trap_types, key=lambda x: x[1])
            strategy['global_recommendations'].append(
                f"Vigilance particulière contre les pièges de type '{top_trap[0]}' - {top_trap[1]:.1%} de fréquence"
            )
        
        vulnerable_markets = [(m, v) for m, v in historical_patterns.get('market_vulnerability', {}).items() if v > 0.25]
        if vulnerable_markets:
            vulnerable_markets.sort(key=lambda x: x[1], reverse=True)
            markets_to_avoid = [m[0] for m in vulnerable_markets[:3]]
            strategy['global_recommendations'].append(
                f"Éviter ou réduire l'exposition aux marchés à haut risque: {', '.join(markets_to_avoid)}"
            )
        
        return strategy
    
    def _analyze_market(self, market_name, market_odds, betting_volumes, historical_data, match_data):
        """
        Analyser un marché spécifique pour détecter les pièges potentiels.
        Utilise les données de Transfermarkt pour enrichir l'analyse si disponibles.
        """
        # Base de l'analyse
        market_analysis = {
            'market': market_name,
            'trap_detected': False,
            'trap_type': None,
            'trap_severity': 0.0,
            'trap_description': '',
            'detection_confidence': 0.0,
            'warning_signs': [],
            'safety_indicators': [],
            'market_safety_score': 0.5,  # Score par défaut
            'betting_advice': '',
            'transfermarkt_insights': []  # Insights issus des données Transfermarkt
        }
        
        # Incorporer les facteurs d'instabilité d'équipe de Transfermarkt si disponibles
        team_analyses = match_data.get('team_analyses', {})
        
        if team_analyses and self.use_real_data:
            # Extraire les facteurs clés des analyses d'équipe qui peuvent affecter ce marché
            for team_position, team_analysis in team_analyses.items():
                team_name = team_analysis.get('team_name', f"Équipe {team_position}")
                
                # Vérifier si des facteurs clés existent
                for factor in team_analysis.get('key_factors', []):
                    factor_type = factor.get('factor_type')
                    impact_score = factor.get('impact_score', 0.0)
                    
                    # Déterminer si ce facteur affecte ce marché spécifique
                    affects_market = False
                    
                    # Logique de correspondance entre facteurs d'équipe et marchés
                    if factor_type == 'team_composition':
                        # Les changements de composition affectent presque tous les marchés
                        affects_market = True
                    elif 'player_rotation' in factor_type and ('goals' in market_name.lower() or 'score' in market_name.lower()):
                        # La rotation des joueurs affecte principalement les marchés de buts
                        affects_market = True
                    elif 'injuries' in factor_type and market_name.lower() in ['asian_handicap', '1x2', 'over_under']:
                        # Les blessures affectent les marchés principaux
                        affects_market = True
                    
                    # Si ce facteur affecte ce marché, ajouter un insight et ajuster l'analyse
                    if affects_market and impact_score > 0.2:
                        insight = {
                            'team': team_name,
                            'factor': factor.get('description', factor_type),
                            'impact': impact_score,
                            'relevance': 'haute' if impact_score > 0.6 else 'moyenne'
                        }
                        market_analysis['transfermarkt_insights'].append(insight)
                        
                        # Ajouter un avertissement si l'impact est significatif
                        if impact_score > 0.5:
                            warning = f"Attention: {factor.get('description')} pour {team_name} peut créer une incertitude sur ce marché"
                            market_analysis['warning_signs'].append(warning)
                            
                            # Ajuster la détection de piège
                            # Les facteurs d'équipe augmentent la probabilité de piège
                            trap_contribution = impact_score * factor.get('trap_correlation', 0.5)
                            market_analysis['detection_confidence'] += trap_contribution / 4  # Impact modéré
                
                # Vérifier les facteurs de joueur spécifiques
                for player_factor in team_analysis.get('player_factors', []):
                    player_name = player_factor.get('player_name', 'Joueur inconnu')
                    importance = player_factor.get('importance', 0.0)
                    
                    # Si c'est un joueur important, il peut affecter le marché
                    if importance > 0.4:
                        insight = {
                            'team': team_name,
                            'player': player_name,
                            'factor': player_factor.get('impact_description', 'Transfert récent'),
                            'importance': importance
                        }
                        market_analysis['transfermarkt_insights'].append(insight)
                        
                        # Pour les joueurs très importants, ajouter un avertissement
                        if importance > 0.7:
                            warning = f"Joueur clé {player_name} récemment transféré à {team_name}"
                            market_analysis['warning_signs'].append(warning)
            
            # Intégrer le facteur d'instabilité global dans l'analyse
            if 'team_instability_factor' in match_data and match_data['team_instability_factor'] > 0.4:
                market_analysis['warning_signs'].append(f"Instabilité d'équipe détectée (facteur: {match_data['team_instability_factor']:.2f})")
                market_analysis['detection_confidence'] += match_data['team_instability_factor'] * 0.3
        
        # Extraire les données historiques de cotes si disponibles
        historical_odds = historical_data.get('odds_history', [])
        
        # Analyser les anomalies dans les cotes actuelles
        odds_anomalies = self._detect_odds_anomalies(market_odds, historical_odds)
        
        # Analyser les déséquilibres de volume
        volume_anomalies = self._detect_volume_anomalies(betting_volumes, market_odds)
        
        # Analyser les mouvements récents des cotes
        movement_anomalies = self._detect_odds_movement_anomalies(market_odds, historical_odds)
        
        # Combiner tous les signaux d'avertissement
        warning_signs = odds_anomalies + volume_anomalies + movement_anomalies
        
        # Ajouter les signaux à l'analyse
        market_analysis['warning_signs'] = warning_signs
        
        # Détecter des signaux de sécurité
        safety_indicators = self._detect_safety_indicators(market_odds, betting_volumes, historical_data)
        market_analysis['safety_indicators'] = safety_indicators
        
        # Calculer un score de sécurité (0 = dangereux, 1 = sûr)
        warning_weight = sum([sign.get('significance', 0) for sign in warning_signs])
        safety_weight = sum([indicator.get('significance', 0) for indicator in safety_indicators])
        
        # Ajuster le score de sécurité
        if warning_weight + safety_weight > 0:
            market_analysis['market_safety_score'] = safety_weight / (warning_weight + safety_weight)
        
        # Vérifier si un piège est détecté
        trap_detected, trap_info = self._evaluate_trap_signals(
            warning_signs, safety_indicators, market_name, match_data
        )
        
        if trap_detected:
            market_analysis['trap_detected'] = True
            market_analysis['trap_type'] = trap_info.get('trap_type')
            market_analysis['trap_severity'] = trap_info.get('severity', 0.0)
            market_analysis['trap_description'] = trap_info.get('description', '')
            market_analysis['detection_confidence'] = trap_info.get('confidence', 0.0)
        
        # Générer un conseil de paris
        if market_analysis['trap_detected']:
            market_analysis['betting_advice'] = f"ÉVITER - {market_analysis['trap_description']}"
        elif market_analysis['market_safety_score'] > 0.7:
            market_analysis['betting_advice'] = "Marché considéré comme sûr pour les paris"
        else:
            market_analysis['betting_advice'] = "Procéder avec prudence - données insuffisantes ou mixtes"
        
        return market_analysis
    
    def _detect_odds_anomalies(self, market_odds, historical_odds):
        """Détecter les anomalies dans les cotes actuelles."""
        anomalies = []
        
        # Vérifier des cotes aberrantes
        for outcome, odds in market_odds.items():
            if isinstance(odds, (int, float)) and odds > 0:
                # Convertir en probabilité implicite
                implied_prob = 1 / odds
                
                # Vérifier si la cote est aberrante (trop élevée ou trop basse)
                if odds > 10.0 and implied_prob < 0.1:
                    anomalies.append({
                        'anomaly_type': 'outlier_high_odds',
                        'outcome': outcome,
                        'odds_value': odds,
                        'implied_probability': implied_prob,
                        'description': f"Cote anormalement élevée pour {outcome}: {odds}",
                        'significance': 0.6
                    })
                elif odds < 1.2 and implied_prob > 0.85:
                    anomalies.append({
                        'anomaly_type': 'outlier_low_odds',
                        'outcome': outcome,
                        'odds_value': odds,
                        'implied_probability': implied_prob,
                        'description': f"Cote anormalement basse pour {outcome}: {odds}",
                        'significance': 0.7
                    })
        
        # Vérifier l'incohérence des probabilités implicites
        total_implied_prob = sum([1 / odds for outcome, odds in market_odds.items() 
                                if isinstance(odds, (int, float)) and odds > 0])
        
        # La somme des probabilités implicites devrait être proche de 1.05-1.15 (marge du bookmaker)
        if total_implied_prob > 1.2:
            anomalies.append({
                'anomaly_type': 'high_overround',
                'total_implied_probability': total_implied_prob,
                'description': f"Surround élevé: {total_implied_prob:.2f} - Marge excessive du bookmaker",
                'significance': (total_implied_prob - 1.15) * 2  # Significativité proportionnelle à l'excès
            })
        elif total_implied_prob < 1.0:
            anomalies.append({
                'anomaly_type': 'arbitrage_opportunity',
                'total_implied_probability': total_implied_prob,
                'description': f"Opportunité d'arbitrage potentielle: {total_implied_prob:.2f}",
                'significance': 0.9  # Très significatif - situation rare
            })
        
        # Comparer aux cotes historiques si disponibles
        if historical_odds:
            for outcome, current_odds in market_odds.items():
                if not isinstance(current_odds, (int, float)) or current_odds <= 0:
                    continue
                    
                # Chercher les cotes historiques pour cet outcome
                historical_values = []
                for hist_odds in historical_odds:
                    if outcome in hist_odds:
                        if isinstance(hist_odds[outcome], (int, float)) and hist_odds[outcome] > 0:
                            historical_values.append(hist_odds[outcome])
                
                if historical_values:
                    avg_historical = sum(historical_values) / len(historical_values)
                    
                    # Détecter un écart significatif
                    if current_odds > avg_historical * 1.5:
                        anomalies.append({
                            'anomaly_type': 'historical_odds_increase',
                            'outcome': outcome,
                            'current_odds': current_odds,
                            'historical_avg': avg_historical,
                            'increase_factor': current_odds / avg_historical,
                            'description': f"Hausse anormale des cotes pour {outcome}: {current_odds} vs moyenne historique {avg_historical:.2f}",
                            'significance': min(0.8, (current_odds / avg_historical - 1.0) * 1.5)
                        })
                    elif current_odds < avg_historical * 0.7:
                        anomalies.append({
                            'anomaly_type': 'historical_odds_decrease',
                            'outcome': outcome,
                            'current_odds': current_odds,
                            'historical_avg': avg_historical,
                            'decrease_factor': avg_historical / current_odds,
                            'description': f"Baisse anormale des cotes pour {outcome}: {current_odds} vs moyenne historique {avg_historical:.2f}",
                            'significance': min(0.85, (avg_historical / current_odds - 0.7) * 2.0)
                        })
        
        return anomalies
    
    def _detect_volume_anomalies(self, betting_volumes, market_odds):
        """Détecter les anomalies dans les volumes de paris."""
        anomalies = []
        
        if not betting_volumes:
            return anomalies
        
        # Calculer le volume total
        total_volume = sum([vol for outcome, vol in betting_volumes.items() 
                           if isinstance(vol, (int, float))])
        
        if total_volume <= 0:
            return anomalies
        
        # Vérifier le déséquilibre de volume
        for outcome, odds in market_odds.items():
            if outcome in betting_volumes:
                volume = betting_volumes[outcome]
                
                if not isinstance(volume, (int, float)) or not isinstance(odds, (int, float)):
                    continue
                
                # Calculer la part du volume total
                volume_share = volume / total_volume if total_volume > 0 else 0
                
                # Calculer la probabilité implicite
                implied_prob = 1 / odds if odds > 0 else 0
                
                # Détecter un déséquilibre entre volume et cotes
                if volume_share > 0.7 and implied_prob < 0.4:
                    anomalies.append({
                        'anomaly_type': 'volume_odds_imbalance',
                        'outcome': outcome,
                        'volume_share': volume_share,
                        'implied_probability': implied_prob,
                        'description': f"Déséquilibre volume/cotes pour {outcome}: {volume_share:.1%} du volume mais probabilité implicite de seulement {implied_prob:.1%}",
                        'significance': min(0.9, volume_share * 1.2)
                    })
                elif volume_share < 0.2 and implied_prob > 0.6:
                    anomalies.append({
                        'anomaly_type': 'reverse_volume_odds_imbalance',
                        'outcome': outcome,
                        'volume_share': volume_share,
                        'implied_probability': implied_prob,
                        'description': f"Déséquilibre inverse volume/cotes pour {outcome}: seulement {volume_share:.1%} du volume mais probabilité implicite élevée de {implied_prob:.1%}",
                        'significance': min(0.85, implied_prob * 1.3)
                    })
        
        # Vérifier la concentration anormale du volume
        max_volume = max([vol for outcome, vol in betting_volumes.items() 
                         if isinstance(vol, (int, float))], default=0)
        max_volume_share = max_volume / total_volume if total_volume > 0 else 0
        
        if max_volume_share > self.detection_params['volume_imbalance_threshold']:
            # Trouver l'outcome avec le volume max
            max_outcome = None
            for outcome, volume in betting_volumes.items():
                if volume == max_volume:
                    max_outcome = outcome
                    break
            
            anomalies.append({
                'anomaly_type': 'concentrated_volume',
                'outcome': max_outcome,
                'volume_share': max_volume_share,
                'description': f"Concentration anormale du volume sur {max_outcome}: {max_volume_share:.1%}",
                'significance': min(0.9, max_volume_share * 1.1)
            })
        
        return anomalies
    
    def _detect_odds_movement_anomalies(self, market_odds, historical_odds):
        """Détecter les anomalies dans les mouvements récents des cotes."""
        anomalies = []
        
        # Vérifier si on a suffisamment d'historique
        if len(historical_odds) < 2:
            return anomalies
        
        # Trier l'historique par timestamp (du plus ancien au plus récent)
        sorted_history = sorted(historical_odds, key=lambda x: x.get('timestamp', ''))
        recent_history = sorted_history[-3:]  # 3 derniers points de données
        
        # Vérifier les changements rapides récents
        for outcome, current_odds in market_odds.items():
            if not isinstance(current_odds, (int, float)) or current_odds <= 0:
                continue
                
            # Extraire les cotes historiques récentes pour cet outcome
            recent_values = []
            for hist_odds in recent_history:
                if outcome in hist_odds and isinstance(hist_odds[outcome], (int, float)) and hist_odds[outcome] > 0:
                    recent_values.append(hist_odds[outcome])
            
            if len(recent_values) < 2:
                continue
            
            # Calculer le changement récent
            most_recent = recent_values[-1]
            previous = recent_values[0]
            
            pct_change_recent = (most_recent - previous) / previous
            pct_change_current = (current_odds - most_recent) / most_recent
            
            # Détecter un renversement de tendance
            if (pct_change_recent > 0.1 and pct_change_current < -0.15) or \
               (pct_change_recent < -0.1 and pct_change_current > 0.15):
                anomalies.append({
                    'anomaly_type': 'odds_reversal',
                    'outcome': outcome,
                    'recent_trend': 'increasing' if pct_change_recent > 0 else 'decreasing',
                    'current_change': 'decreasing' if pct_change_current < 0 else 'increasing',
                    'description': f"Renversement des cotes pour {outcome}: tendance récente {pct_change_recent:+.1%}, puis changement de {pct_change_current:+.1%}",
                    'significance': min(0.9, abs(pct_change_current) * 3)
                })
            
            # Détecter un mouvement soudain et important
            elif abs(pct_change_current) > self.detection_params['odds_movement_significance']:
                anomalies.append({
                    'anomaly_type': 'sudden_odds_movement',
                    'outcome': outcome,
                    'movement': pct_change_current,
                    'description': f"Mouvement soudain des cotes pour {outcome}: {pct_change_current:+.1%}",
                    'significance': min(0.8, abs(pct_change_current) * 2.5)
                })
        
        # Vérifier si toutes les cotes ont bougé dans la même direction
        if len(market_odds) >= 2:
            all_movements = []
            
            for outcome, current_odds in market_odds.items():
                if not isinstance(current_odds, (int, float)) or current_odds <= 0:
                    continue
                
                if recent_history and outcome in recent_history[-1]:
                    prev_odds = recent_history[-1][outcome]
                    if isinstance(prev_odds, (int, float)) and prev_odds > 0:
                        movement = (current_odds - prev_odds) / prev_odds
                        all_movements.append(movement)
            
            if len(all_movements) >= 2:
                # Vérifier si tous les mouvements sont dans la même direction
                all_positive = all(m > 0.05 for m in all_movements)
                all_negative = all(m < -0.05 for m in all_movements)
                
                if all_positive or all_negative:
                    anomalies.append({
                        'anomaly_type': 'uniform_odds_movement',
                        'direction': 'increasing' if all_positive else 'decreasing',
                        'description': f"Toutes les cotes se déplacent dans la même direction: {'augmentation' if all_positive else 'diminution'}",
                        'significance': 0.7
                    })
        
        return anomalies
    
    def _detect_safety_indicators(self, market_odds, betting_volumes, historical_data):
        """Détecter des indicateurs de sécurité pour le marché."""
        indicators = []
        
        # Vérifier la stabilité des cotes
        odds_stable = True
        
        # Extraire l'historique récent
        historical_odds = historical_data.get('odds_history', [])
        recent_history = sorted(historical_odds, key=lambda x: x.get('timestamp', ''))[-3:] if historical_odds else []
        
        if recent_history:
            for outcome, current_odds in market_odds.items():
                if not isinstance(current_odds, (int, float)) or current_odds <= 0:
                    continue
                
                # Vérifier si l'outcome existe dans l'historique récent
                recent_values = []
                for hist_odds in recent_history:
                    if outcome in hist_odds and isinstance(hist_odds[outcome], (int, float)) and hist_odds[outcome] > 0:
                        recent_values.append(hist_odds[outcome])
                
                if recent_values:
                    # Calculer la variabilité
                    max_val = max(recent_values)
                    min_val = min(recent_values)
                    
                    if max_val > min_val * 1.15:
                        odds_stable = False
                        break
            
            if odds_stable:
                indicators.append({
                    'indicator_type': 'stable_odds',
                    'description': "Cotes stables sur la période récente",
                    'significance': 0.7
                })
        
        # Vérifier l'équilibre des volumes (si disponibles)
        if betting_volumes:
            total_volume = sum([vol for outcome, vol in betting_volumes.items() 
                               if isinstance(vol, (int, float))])
            
            if total_volume > 0:
                volumes = [vol for outcome, vol in betting_volumes.items() 
                          if isinstance(vol, (int, float))]
                
                max_share = max(volumes) / total_volume if volumes else 0
                
                if max_share < 0.6:
                    indicators.append({
                        'indicator_type': 'balanced_volume',
                        'max_share': max_share,
                        'description': f"Volume de paris équilibré entre les outcomes (max {max_share:.1%})",
                        'significance': 0.6
                    })
        
        # Vérifier la cohérence des probabilités implicites
        implied_probs = [1 / odds for outcome, odds in market_odds.items() 
                        if isinstance(odds, (int, float)) and odds > 0]
        
        if implied_probs:
            total_implied = sum(implied_probs)
            
            # Vérifier si le total est cohérent avec une marge bookmaker normale
            if 1.05 <= total_implied <= 1.15:
                indicators.append({
                    'indicator_type': 'fair_margin',
                    'total_implied': total_implied,
                    'description': f"Marge bookmaker équitable: {(total_implied - 1) * 100:.1f}%",
                    'significance': 0.75
                })
        
        # Vérifier la cohérence avec les données historiques
        if historical_data.get('average_odds'):
            avg_odds = historical_data.get('average_odds', {})
            consistent_with_history = True
            
            for outcome, current_odds in market_odds.items():
                if outcome in avg_odds:
                    avg_value = avg_odds[outcome]
                    
                    if isinstance(current_odds, (int, float)) and isinstance(avg_value, (int, float)):
                        if current_odds < avg_value * 0.7 or current_odds > avg_value * 1.4:
                            consistent_with_history = False
                            break
            
            if consistent_with_history:
                indicators.append({
                    'indicator_type': 'historical_consistency',
                    'description': "Cotes cohérentes avec les moyennes historiques",
                    'significance': 0.8
                })
        
        return indicators
    
    def _evaluate_trap_signals(self, warning_signs, safety_indicators, market_name, match_data):
        """Évaluer si les signaux indiquent un piège et déterminer son type."""
        # Base de la détection
        trap_detected = False
        trap_info = {
            'trap_type': None,
            'severity': 0.0,
            'confidence': 0.0,
            'description': ''
        }
        
        # Pas d'avertissements, pas de piège
        if not warning_signs:
            return trap_detected, trap_info
        
        # Calculer un score global d'avertissement
        warning_score = sum([sign.get('significance', 0) for sign in warning_signs])
        safety_score = sum([indicator.get('significance', 0) for indicator in safety_indicators])
        
        # Calculer un ratio avertissement/sécurité
        warning_ratio = warning_score / (warning_score + safety_score) if (warning_score + safety_score) > 0 else 0
        
        # Si le ratio est suffisamment élevé, c'est un piège potentiel
        if warning_ratio > 0.65 and warning_score > 1.0:
            trap_detected = True
            
            # Déterminer le type de piège en fonction des avertissements
            # Convertir les types d'anomalies en patterns de détection
            anomaly_types = [sign.get('anomaly_type', '') for sign in warning_signs]
            
            # Mapper les anomalies aux patterns de détection
            detection_patterns = []
            pattern_mapping = {
                'outlier_high_odds': 'outlier_odds_value',
                'outlier_low_odds': 'outlier_odds_value',
                'high_overround': 'house_advantage_increase',
                'arbitrage_opportunity': 'implied_prob_inconsistency',
                'historical_odds_increase': 'odds_mispricing',
                'historical_odds_decrease': 'odds_mispricing',
                'volume_odds_imbalance': 'visible_balanced_volume',
                'reverse_volume_odds_imbalance': 'hidden_imbalance',
                'concentrated_volume': 'heavy_public_favorite',
                'odds_reversal': 'late_odds_movement',
                'sudden_odds_movement': 'rapid_odds_shift',
                'uniform_odds_movement': 'counter_public_movement'
            }
            
            for anomaly in anomaly_types:
                if anomaly in pattern_mapping:
                    detection_patterns.append(pattern_mapping[anomaly])
            
            # Trouver le type de piège correspondant le mieux aux patterns
            matched_trap = None
            max_pattern_matches = 0
            
            for trap_type, trap_data in self.trap_types.items():
                trap_patterns = trap_data.get('detection_patterns', [])
                matches = sum(1 for pattern in detection_patterns if pattern in trap_patterns)
                
                if matches > max_pattern_matches:
                    max_pattern_matches = matches
                    matched_trap = trap_type
            
            # Si on a trouvé un type de piège, l'utiliser
            if matched_trap and max_pattern_matches > 0:
                trap_type = matched_trap
                trap_data = self.trap_types[trap_type]
                
                trap_info['trap_type'] = trap_type
                trap_info['severity'] = trap_data.get('severity', 0.7) * (warning_ratio / 0.65)
                trap_info['description'] = trap_data.get('description', 'Piège détecté')
                
                # Calculer la confiance en fonction du nombre de patterns correspondants
                pattern_match_ratio = max_pattern_matches / len(trap_data.get('detection_patterns', []))
                trap_info['confidence'] = min(0.95, warning_ratio * 0.7 + pattern_match_ratio * 0.3)
            else:
                # Piège générique si aucun type spécifique ne correspond
                trap_info['trap_type'] = 'generic_trap'
                trap_info['severity'] = warning_ratio * 0.8
                trap_info['description'] = "Configuration suspecte des cotes et volumes"
                trap_info['confidence'] = warning_ratio * 0.9
        
        return trap_detected, trap_info
    
    def _generate_betting_recommendations(self, safe_markets, high_risk_markets, match_data):
        """Générer des recommandations de paris basées sur l'analyse."""
        recommendations = []
        
        # Recommander d'éviter les marchés à haut risque
        if high_risk_markets:
            high_risk_names = [market.get('market', '') for market in high_risk_markets]
            
            recommendations.append({
                'recommendation_type': 'avoid',
                'markets': high_risk_names,
                'description': f"Éviter ces marchés à haut risque: {', '.join(high_risk_names)}",
                'confidence': min(0.9, max([market.get('risk_level', 0) for market in high_risk_markets]))
            })
        
        # Recommander des marchés sûrs
        if safe_markets:
            safe_names = [market.get('market', '') for market in safe_markets]
            
            recommendations.append({
                'recommendation_type': 'safe_markets',
                'markets': safe_names,
                'description': f"Marchés considérés comme sûrs: {', '.join(safe_names)}",
                'confidence': min(0.85, max([market.get('safety_score', 0) for market in safe_markets]))
            })
        
        # Recommandation globale basée sur le ratio risque/sécurité
        high_risk_count = len(high_risk_markets)
        safe_count = len(safe_markets)
        
        if high_risk_count > safe_count * 2:
            recommendations.append({
                'recommendation_type': 'global_caution',
                'description': "PRUDENCE GLOBALE - Nombreux marchés à risque détectés",
                'confidence': 0.8
            })
        elif safe_count > 0 and high_risk_count == 0:
            recommendations.append({
                'recommendation_type': 'proceed_with_confidence',
                'description': "CONDITIONS FAVORABLES - Aucun piège majeur détecté",
                'confidence': 0.75
            })
        else:
            recommendations.append({
                'recommendation_type': 'selective_approach',
                'description': "APPROCHE SÉLECTIVE - Rester sur les marchés considérés comme sûrs",
                'confidence': 0.7
            })
        
        return recommendations
    
    def _simulate_odds_data(self, home_team, away_team):
        """Simuler des données de cotes pour les tests."""
        markets = {
            'match_result': {
                'home': round(random.uniform(1.5, 4.0), 2),
                'draw': round(random.uniform(2.5, 4.5), 2),
                'away': round(random.uniform(1.5, 5.0), 2)
            },
            'over_under_2.5': {
                'over': round(random.uniform(1.7, 2.2), 2),
                'under': round(random.uniform(1.7, 2.2), 2)
            },
            'both_teams_to_score': {
                'yes': round(random.uniform(1.6, 2.1), 2),
                'no': round(random.uniform(1.7, 2.3), 2)
            },
            'draw_no_bet': {
                'home': round(random.uniform(1.3, 2.5), 2),
                'away': round(random.uniform(1.3, 3.0), 2)
            },
            'double_chance': {
                'home_draw': round(random.uniform(1.2, 1.5), 2),
                'home_away': round(random.uniform(1.2, 1.6), 2),
                'draw_away': round(random.uniform(1.2, 1.6), 2)
            }
        }
        
        # Ajouter des handicaps asiatiques
        asian_handicaps = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]
        selected_handicaps = random.sample(asian_handicaps, 3)
        
        for handicap in selected_handicaps:
            market_name = f"asian_handicap_{handicap}"
            markets[market_name] = {
                'home': round(random.uniform(1.7, 2.3), 2),
                'away': round(random.uniform(1.7, 2.3), 2)
            }
        
        # Randomly introduce potential traps
        if random.random() < 0.3:  # 30% chance of introducing a trap
            trap_market = random.choice(list(markets.keys()))
            
            if trap_market == 'match_result':
                # Create a false favorite trap
                if random.random() < 0.5:
                    markets[trap_market]['home'] = round(markets[trap_market]['home'] * 0.7, 2)  # artificially low odds
                else:
                    markets[trap_market]['away'] = round(markets[trap_market]['away'] * 0.7, 2)  # artificially low odds
            elif trap_market == 'over_under_2.5':
                # Create an odds reversal trap
                if random.random() < 0.5:
                    markets[trap_market]['over'] = round(markets[trap_market]['over'] * 1.4, 2)  # artificially high odds
                else:
                    markets[trap_market]['under'] = round(markets[trap_market]['under'] * 1.4, 2)  # artificially high odds
        
        return markets
    
    def _simulate_betting_volumes(self, odds_data):
        """Simuler des données de volume de paris pour les tests."""
        volumes = {}
        
        for market_name, market_odds in odds_data.items():
            market_volumes = {}
            total_volume = random.randint(5000, 50000)
            
            # Distribuer le volume entre les outcomes
            outcomes = list(market_odds.keys())
            
            # Weighted distribution based on odds (lower odds get more volume)
            inverse_odds = []
            for outcome in outcomes:
                odds = market_odds[outcome]
                if isinstance(odds, (int, float)) and odds > 0:
                    inverse_odds.append(1 / odds)
                else:
                    inverse_odds.append(0.5)  # Default if odds are invalid
            
            # Normalize to get weights
            total_inverse = sum(inverse_odds)
            weights = [inv / total_inverse for inv in inverse_odds] if total_inverse > 0 else [1/len(outcomes)] * len(outcomes)
            
            # Randomly skew the distribution sometimes to simulate imbalances
            if random.random() < 0.3:  # 30% chance
                # Choose one outcome to skew
                skew_idx = random.randrange(len(weights))
                skew_factor = random.uniform(1.5, 3.0)
                
                weights[skew_idx] *= skew_factor
                total_weights = sum(weights)
                weights = [w / total_weights for w in weights]
            
            # Distribute volumes according to weights
            remaining_volume = total_volume
            for i, outcome in enumerate(outcomes):
                if i == len(outcomes) - 1:  # Last outcome gets whatever is left
                    market_volumes[outcome] = remaining_volume
                else:
                    volume = int(total_volume * weights[i])
                    market_volumes[outcome] = volume
                    remaining_volume -= volume
            
            volumes[market_name] = market_volumes
        
        return volumes
    
    def _simulate_historical_data(self, home_team, away_team):
        """Simuler des données historiques pour les tests."""
        historical_data = {}
        
        # Créer un historique pour quelques marchés typiques
        for market_name in ['match_result', 'over_under_2.5', 'both_teams_to_score']:
            market_history = {
                'odds_history': [],
                'average_odds': {}
            }
            
            # Générer 5 points historiques
            for i in range(5):
                timestamp = (datetime.now() - timedelta(hours=(5-i) * 12)).isoformat()
                
                if market_name == 'match_result':
                    hist_odds = {
                        'timestamp': timestamp,
                        'home': round(random.uniform(1.5, 4.0), 2),
                        'draw': round(random.uniform(2.5, 4.5), 2),
                        'away': round(random.uniform(1.5, 5.0), 2)
                    }
                elif market_name == 'over_under_2.5':
                    hist_odds = {
                        'timestamp': timestamp,
                        'over': round(random.uniform(1.7, 2.2), 2),
                        'under': round(random.uniform(1.7, 2.2), 2)
                    }
                else:  # both_teams_to_score
                    hist_odds = {
                        'timestamp': timestamp,
                        'yes': round(random.uniform(1.6, 2.1), 2),
                        'no': round(random.uniform(1.7, 2.3), 2)
                    }
                
                market_history['odds_history'].append(hist_odds)
            
            # Calculate average odds
            for key in market_history['odds_history'][0].keys():
                if key != 'timestamp':
                    values = [odds[key] for odds in market_history['odds_history'] if key in odds]
                    if values:
                        market_history['average_odds'][key] = sum(values) / len(values)
            
            historical_data[market_name] = market_history
        
        return historical_data
    
    def _simulate_trap_history(self, timeframe='recent', team_name=None, market_type=None):
        """Simuler un historique de pièges pour l'analyse de patterns."""
        # Nombre d'entrées historiques à générer
        if timeframe == 'recent':
            num_entries = 20
        elif timeframe == 'season':
            num_entries = 50
        else:  # all
            num_entries = 100
        
        # Liste d'équipes pour la simulation
        teams = [
            "Arsenal", "Manchester United", "Liverpool", "Chelsea", "Manchester City",
            "Tottenham", "PSG", "Bayern Munich", "Barcelona", "Real Madrid",
            "Juventus", "Inter Milan", "AC Milan", "Ajax", "Dortmund"
        ]
        
        # Liste de marchés pour la simulation
        markets = [
            "match_result", "over_under_2.5", "both_teams_to_score", "double_chance",
            "draw_no_bet", "correct_score", "halftime_fulltime", "first_goalscorer",
            "asian_handicap", "european_handicap"
        ]
        
        # Types de piège
        trap_types = list(self.trap_types.keys())
        
        # Générer l'historique
        history = []
        
        for i in range(num_entries):
            # Date du match (dispersion sur les derniers mois)
            match_date = (datetime.now() - timedelta(days=random.randint(1, 120))).isoformat()
            
            # Équipes
            if team_name and random.random() < 0.3:  # 30% chance d'inclure l'équipe spécifiée
                if random.random() < 0.5:
                    home_team = team_name
                    away_team = random.choice([t for t in teams if t != team_name])
                else:
                    home_team = random.choice([t for t in teams if t != team_name])
                    away_team = team_name
            else:
                home_team, away_team = random.sample(teams, 2)
            
            # Marché
            if market_type:
                market = market_type
            else:
                market = random.choice(markets)
            
            # 50% chance d'être un piège
            is_trap = random.random() < 0.5
            
            if is_trap:
                trap_type = random.choice(trap_types)
                trap_severity = round(random.uniform(0.6, 0.9), 2)
                
                history.append({
                    'date': match_date,
                    'home_team': home_team,
                    'away_team': away_team,
                    'market': market,
                    'is_trap': True,
                    'trap_type': trap_type,
                    'severity': trap_severity
                })
            else:
                history.append({
                    'date': match_date,
                    'home_team': home_team,
                    'away_team': away_team,
                    'market': market,
                    'is_trap': False
                })
        
        return history