"""
YouthImpactAnalyzer - Module d'analyse de l'influence des jeunes joueurs.
Évalue l'impact potentiel et réel des jeunes talents sur les performances d'une équipe.
Intègre les données de Transfermarkt pour des analyses plus précises.
"""

import numpy as np
import random
from datetime import datetime, timedelta
import json
import os
import logging
from collections import deque

# Intégration de l'adaptateur Transfermarkt
from api.transfermarkt_adapter import TransfermarktAdapter

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouthImpactAnalyzer:
    """
    YouthImpactAnalyzer - Analyse l'influence des jeunes joueurs sur les performances d'équipe.
    Évalue la contribution des talents émergents et leur potentiel d'influence sur les résultats.
    """
    
    def __init__(self):
        """Initialise le module YouthImpactAnalyzer avec l'adaptateur Transfermarkt."""
        # Initialiser l'adaptateur Transfermarkt pour obtenir des données réelles
        self.transfermarkt = TransfermarktAdapter()
        logger.info("Initialisation de l'adaptateur Transfermarkt pour YouthImpactAnalyzer")
        self.use_real_data = self.transfermarkt.api_online
        
        if self.use_real_data:
            logger.info("YouthImpactAnalyzer utilisera les données réelles de Transfermarkt")
        else:
            logger.warning("API Transfermarkt non disponible, YouthImpactAnalyzer utilisera des données simulées")
        
        # Définition des âges pour les catégories de jeunes joueurs
        self.youth_categories = {
            'prodigy': {'min_age': 16, 'max_age': 18},  # Prodiges (16-18 ans)
            'breakthrough': {'min_age': 19, 'max_age': 21},  # Jeunes en éclosion (19-21 ans)
            'emerging': {'min_age': 22, 'max_age': 23}  # Talents émergents (22-23 ans)
        }
        
        # Facteurs d'impact des jeunes joueurs
        self.impact_factors = {
            'technical_ability': 0.25,     # Capacité technique
            'physical_development': 0.2,   # Développement physique
            'mental_attributes': 0.2,      # Attributs mentaux
            'tactical_understanding': 0.15,  # Compréhension tactique
            'match_experience': 0.1,       # Expérience en match
            'consistency': 0.1             # Constance des performances
        }
        
        # Facteurs de développement
        self.development_factors = {
            'training_facilities': 0.2,    # Qualité des installations d'entraînement
            'coaching_quality': 0.25,      # Qualité de l'encadrement
            'playing_time': 0.3,           # Temps de jeu
            'team_environment': 0.15,      # Environnement d'équipe
            'competition_level': 0.1       # Niveau de compétition
        }
        
        # Coefficients de potentiel par âge (plus jeune = plus de potentiel)
        self.potential_age_coefficients = {
            16: 1.0, 17: 0.97, 18: 0.95, 19: 0.92, 20: 0.9,
            21: 0.85, 22: 0.8, 23: 0.75
        }
        
        # Modèles d'influence des jeunes
        self.influence_models = {
            'game_changer': {
                'description': 'Jeune joueur capable de changer le cours d\'un match',
                'impact_on_results': 0.7,
                'consistency_requirement': 0.5,
                'threshold': 0.8
            },
            'core_contributor': {
                'description': 'Jeune joueur apportant une contribution régulière',
                'impact_on_results': 0.5,
                'consistency_requirement': 0.7,
                'threshold': 0.75
            },
            'squad_player': {
                'description': 'Jeune joueur participant régulièrement mais sans impact décisif',
                'impact_on_results': 0.3,
                'consistency_requirement': 0.6,
                'threshold': 0.65
            },
            'prospect': {
                'description': 'Jeune joueur prometteur avec un temps de jeu limité',
                'impact_on_results': 0.1,
                'consistency_requirement': 0.4,
                'threshold': 0.5
            }
        }
        
        # Historique des analyses
        self.analysis_history = []
        
        # Suivi des jeunes joueurs
        self.tracked_youth_players = {}  # id_joueur -> historique d'analyse
    
    def analyze_youth_impact(self, team_data, match_data=None):
        """
        Analyser l'impact des jeunes joueurs sur une équipe.
        Utilise les données réelles de Transfermarkt si disponibles.
        
        Args:
            team_data (dict): Données de l'équipe et de ses joueurs
            match_data (dict, optional): Données du match pour analyse contextuelle
            
        Returns:
            dict: Analyse de l'impact des jeunes joueurs
        """
        # Enrichir les données d'équipe avec Transfermarkt si possible
        if self.use_real_data and 'id' in team_data:
            try:
                team_id = team_data.get('id')
                logger.info(f"Récupération des données Transfermarkt pour l'équipe {team_id}")
                
                # Récupérer le profil de l'équipe
                club_profile = self.transfermarkt.get_club_profile(team_id)
                if 'status' not in club_profile or club_profile['status'] != 'error':
                    # Fusionner les données de profil
                    for key, value in club_profile.items():
                        if key not in team_data:
                            team_data[key] = value
                    
                    # Récupérer les joueurs de l'équipe
                    club_players = self.transfermarkt.get_club_players(team_id)
                    if 'status' not in club_players or club_players['status'] != 'error':
                        # Remplacer la liste des joueurs si disponible
                        if 'squad' in club_players and club_players['squad']:
                            team_data['squad'] = club_players['squad']
                            logger.info(f"Données de joueurs enrichies avec Transfermarkt: {len(team_data['squad'])} joueurs")
                
            except Exception as e:
                logger.error(f"Erreur lors de l'enrichissement des données avec Transfermarkt: {e}")
                # Continuer avec les données existantes
        
        # Extraire les données pertinentes
        team_name = team_data.get('name', '')
        squad = team_data.get('squad', [])
        
        # Filtrer pour n'obtenir que les jeunes joueurs (23 ans et moins)
        young_players = []
        for player in squad:
            age = player.get('age', 30)
            if age <= 23:
                category = self._determine_youth_category(age)
                if category:
                    player_with_category = player.copy()
                    player_with_category['youth_category'] = category
                    young_players.append(player_with_category)
        
        # Si aucun jeune joueur, retourner une analyse vide
        if not young_players:
            return {
                'team_name': team_name,
                'youth_presence': 0.0,
                'youth_impact': 0.0,
                'young_players': [],
                'youth_strategy': 'no_youth_focus',
                'analysis_timestamp': datetime.now().isoformat()
            }
        
        # Calculer la présence de jeunes dans l'équipe
        youth_presence = len(young_players) / len(squad) if squad else 0
        
        # Analyser chaque jeune joueur
        analyzed_players = []
        team_youth_impact = 0.0
        team_youth_potential = 0.0
        
        for player in young_players:
            # Analyser l'impact actuel et potentiel
            player_analysis = self._analyze_player(player, team_data, match_data)
            analyzed_players.append(player_analysis)
            
            # Contribution à l'impact global
            minutes_factor = min(1.0, player.get('minutes_played', 0) / 900)  # Normaliser à 10 matchs complets
            team_youth_impact += player_analysis['current_impact'] * minutes_factor
            team_youth_potential += player_analysis['potential_impact'] * minutes_factor
        
        # Normaliser l'impact global selon le nombre de jeunes joueurs significatifs
        significant_youth = sum(1 for p in analyzed_players if p['minutes_factor'] > 0.3)
        normalizer = max(1, significant_youth)
        
        team_youth_impact /= normalizer
        team_youth_potential /= normalizer
        
        # Déterminer la stratégie jeunes de l'équipe
        youth_strategy = self._determine_youth_strategy(young_players, team_data)
        
        # Évaluer l'efficacité du développement des jeunes
        development_effectiveness = self._evaluate_development_effectiveness(analyzed_players, team_data)
        
        # Préparer le résultat
        result = {
            'team_name': team_name,
            'youth_presence': youth_presence,
            'youth_impact': team_youth_impact,
            'youth_potential': team_youth_potential,
            'young_players': analyzed_players,
            'youth_strategy': youth_strategy,
            'development_effectiveness': development_effectiveness,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        # Mettre à jour l'historique d'analyse
        self.analysis_history.append({
            'team': team_name,
            'timestamp': datetime.now().isoformat(),
            'youth_impact': team_youth_impact,
            'youth_potential': team_youth_potential,
            'analyzed_players_count': len(analyzed_players)
        })
        
        # Mettre à jour le suivi des jeunes joueurs
        for player in analyzed_players:
            player_id = player['player_id']
            if player_id not in self.tracked_youth_players:
                self.tracked_youth_players[player_id] = []
            
            self.tracked_youth_players[player_id].append({
                'timestamp': datetime.now().isoformat(),
                'current_impact': player['current_impact'],
                'potential_impact': player['potential_impact'],
                'influence_model': player['influence_model'],
                'minutes_played': player.get('minutes_played', 0)
            })
        
        return result
    
    def predict_youth_development(self, player_data, projection_months=6):
        """
        Prédire le développement d'un jeune joueur sur une période donnée.
        Utilise les données réelles de Transfermarkt pour une prédiction plus précise.
        
        Args:
            player_data (dict): Données du joueur
            projection_months (int): Nombre de mois pour la projection
            
        Returns:
            dict: Prédiction du développement
        """
        # Enrichir les données du joueur avec Transfermarkt si possible
        if self.use_real_data and 'id' in player_data:
            try:
                player_id = player_data.get('id')
                logger.info(f"Récupération des données Transfermarkt pour le joueur {player_id}")
                
                # Récupérer le profil du joueur
                player_profile = self.transfermarkt.get_player_profile(player_id)
                if 'status' not in player_profile or player_profile['status'] != 'error':
                    # Fusionner les données de profil
                    for key, value in player_profile.items():
                        if key not in player_data:
                            player_data[key] = value
                    
                    # Exploiter les informations spécifiques de Transfermarkt
                    if 'market_value' in player_profile:
                        # La valeur marchande peut indiquer le potentiel du joueur
                        market_value = player_profile.get('market_value', 0)
                        
                        # S'assurer que market_value est un nombre
                        if isinstance(market_value, str):
                            try:
                                # Supprimer symboles monétaires et convertir en nombre
                                market_value = float(''.join(c for c in market_value if c.isdigit() or c == '.'))
                            except:
                                market_value = 0
                                
                        if not player_data.get('potential_ability'):
                            # Calculer un potentiel basé sur la valeur marchande et l'âge
                            age_factor = 1.5 if player_data.get('age', 20) < 19 else 1.0
                            # Normaliser la valeur marchande (supposons 50M = 1.0)
                            normalized_value = min(1.0, float(market_value) / 50000000) * age_factor
                            player_data['potential_ability'] = normalized_value
                            
                    # Autres attributs utiles de Transfermarkt
                    if 'stats' in player_profile:
                        player_data['transfermarkt_stats'] = player_profile['stats']
                
            except Exception as e:
                logger.error(f"Erreur lors de l'enrichissement des données de joueur avec Transfermarkt: {e}")
                # Continuer avec les données existantes
        
        # Extraire les informations du joueur
        player_id = player_data.get('id', '')
        player_name = player_data.get('name', '')
        age = player_data.get('age', 20)
        
        # Vérifier si le joueur est un jeune
        if age > 23:
            return {
                'status': 'error',
                'message': 'Le joueur est trop âgé pour une analyse de développement jeune'
            }
        
        # Calculer les facteurs de développement
        development_rate = self._calculate_development_rate(player_data)
        
        # Facteurs qui influencent le développement
        playing_time_forecast = player_data.get('expected_playing_time', 0.5)  # 0-1
        coaching_quality = player_data.get('club_coaching_quality', 0.7)  # 0-1
        competition_level = player_data.get('competition_level', 0.6)  # 0-1
        player_potential = player_data.get('potential_ability', 0.8)  # 0-1
        
        # Calculer le taux mensuel de développement prévu
        monthly_growth_rate = development_rate * (
            0.5 +
            (playing_time_forecast * 0.3) +
            (coaching_quality * 0.1) +
            (competition_level * 0.1)
        ) * (player_potential / 0.8)  # Normalisation par rapport à un potentiel de 0.8
        
        # Projection des attributs
        current_attributes = player_data.get('attributes', {})
        projected_attributes = {}
        
        for attr, value in current_attributes.items():
            # Différents attributs se développent à des rythmes différents
            attr_growth_modifier = 1.0
            if attr in ['technical', 'tactical']:
                attr_growth_modifier = 1.2  # Les capacités techniques se développent plus vite
            elif attr in ['physical', 'stamina']:
                attr_growth_modifier = 0.8  # Le physique se développe plus lentement
            elif attr in ['mental', 'leadership']:
                attr_growth_modifier = 1.1  # Les capacités mentales se développent moyennement vite
            
            # Calculer la croissance projetée
            growth = monthly_growth_rate * projection_months * attr_growth_modifier
            projected_value = min(1.0, value + growth)  # Plafonner à 1.0
            projected_attributes[attr] = projected_value
        
        # Calculer l'impact actuel et projeté
        current_impact = self._calculate_player_impact(player_data)
        
        # Créer un joueur projeté pour calculer l'impact futur
        projected_player = player_data.copy()
        projected_player['attributes'] = projected_attributes
        projected_player['age'] = age + (projection_months / 12)  # Ajouter les mois convertis en années
        
        projected_impact = self._calculate_player_impact(projected_player)
        
        # Déterminer les points de développement clés
        key_development_areas = self._identify_key_development_areas(player_data, projected_attributes)
        
        # Calculer le risque de stagnation
        stagnation_risk = self._calculate_stagnation_risk(player_data, playing_time_forecast, coaching_quality)
        
        # Préparer le résultat
        projection_date = (datetime.now() + timedelta(days=30 * projection_months)).isoformat()
        
        result = {
            'player_name': player_name,
            'player_id': player_id,
            'current_age': age,
            'projected_age': age + (projection_months / 12),
            'current_impact': current_impact,
            'projected_impact': projected_impact,
            'impact_growth': projected_impact - current_impact,
            'monthly_growth_rate': monthly_growth_rate,
            'projected_attributes': projected_attributes,
            'key_development_areas': key_development_areas,
            'stagnation_risk': stagnation_risk,
            'projection_date': projection_date,
            'projection_months': projection_months
        }
        
        return result
    
    def evaluate_team_youth_strategy(self, team_data, league_data=None):
        """
        Évaluer la stratégie de développement des jeunes d'une équipe.
        
        Args:
            team_data (dict): Données de l'équipe
            league_data (dict, optional): Données de comparaison par rapport à la ligue
            
        Returns:
            dict: Évaluation de la stratégie jeunes
        """
        # Extraire les informations pertinentes
        team_name = team_data.get('name', '')
        youth_investment = team_data.get('youth_investment', 0.5)  # 0-1
        youth_facilities = team_data.get('youth_facilities', 0.5)  # 0-1
        youth_coaching = team_data.get('youth_coaching', 0.5)  # 0-1
        youth_playing_time = team_data.get('youth_playing_time', 0.3)  # % de minutes pour les jeunes
        
        # Analyser le pipeline de jeunes joueurs
        academy_quality = team_data.get('academy_quality', 0.5)  # 0-1
        youth_recruitment = team_data.get('youth_recruitment', 0.5)  # 0-1
        youth_transition = team_data.get('youth_transition', 0.5)  # Taux de transition vers l'équipe première
        
        # Calculer les scores de stratégie
        infrastructure_score = (youth_facilities * 0.5) + (youth_coaching * 0.5)
        pipeline_score = (academy_quality * 0.4) + (youth_recruitment * 0.3) + (youth_transition * 0.3)
        utilization_score = youth_playing_time
        investment_efficiency = self._calculate_investment_efficiency(team_data)
        
        overall_strategy_score = (
            infrastructure_score * 0.3 +
            pipeline_score * 0.3 +
            utilization_score * 0.3 +
            investment_efficiency * 0.1
        )
        
        # Déterminer la catégorie de stratégie
        strategy_category = 'average'
        if overall_strategy_score > 0.8:
            strategy_category = 'elite'
        elif overall_strategy_score > 0.7:
            strategy_category = 'excellent'
        elif overall_strategy_score > 0.55:
            strategy_category = 'good'
        elif overall_strategy_score < 0.3:
            strategy_category = 'poor'
        
        # Comparer à la ligue si données disponibles
        league_comparison = None
        if league_data:
            avg_youth_investment = league_data.get('avg_youth_investment', 0.5)
            avg_youth_playing_time = league_data.get('avg_youth_playing_time', 0.3)
            avg_strategy_score = league_data.get('avg_youth_strategy_score', 0.5)
            
            investment_percentile = self._calculate_percentile(youth_investment, league_data.get('youth_investment_distribution', []))
            playing_time_percentile = self._calculate_percentile(youth_playing_time, league_data.get('youth_playing_time_distribution', []))
            strategy_percentile = self._calculate_percentile(overall_strategy_score, league_data.get('strategy_score_distribution', []))
            
            league_comparison = {
                'investment_vs_league': youth_investment - avg_youth_investment,
                'playing_time_vs_league': youth_playing_time - avg_youth_playing_time,
                'strategy_score_vs_league': overall_strategy_score - avg_strategy_score,
                'investment_percentile': investment_percentile,
                'playing_time_percentile': playing_time_percentile,
                'strategy_percentile': strategy_percentile
            }
        
        # Identifier les forces et faiblesses
        strengths = []
        weaknesses = []
        
        if infrastructure_score > 0.7:
            strengths.append({
                'aspect': 'infrastructure',
                'description': 'Excellentes installations et encadrement pour les jeunes'
            })
        elif infrastructure_score < 0.4:
            weaknesses.append({
                'aspect': 'infrastructure',
                'description': 'Infrastructures jeunes insuffisantes pour un développement optimal'
            })
        
        if pipeline_score > 0.7:
            strengths.append({
                'aspect': 'talent_pipeline',
                'description': 'Système efficace de détection et développement des talents'
            })
        elif pipeline_score < 0.4:
            weaknesses.append({
                'aspect': 'talent_pipeline',
                'description': 'Difficultés à identifier et développer les talents jusqu\'au niveau professionnel'
            })
        
        if utilization_score > 0.5:
            strengths.append({
                'aspect': 'youth_utilization',
                'description': 'Forte intégration des jeunes dans l\'équipe première'
            })
        elif utilization_score < 0.2:
            weaknesses.append({
                'aspect': 'youth_utilization',
                'description': 'Temps de jeu très limité accordé aux jeunes joueurs'
            })
        
        # Générer des recommandations
        recommendations = self._generate_strategy_recommendations(team_data, strengths, weaknesses)
        
        # Préparer le résultat
        result = {
            'team_name': team_name,
            'overall_strategy_score': overall_strategy_score,
            'strategy_category': strategy_category,
            'infrastructure_score': infrastructure_score,
            'pipeline_score': pipeline_score,
            'utilization_score': utilization_score,
            'investment_efficiency': investment_efficiency,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'recommendations': recommendations,
            'league_comparison': league_comparison,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def find_top_youth_talents(self, competition_id=None, age_max=23, limit=10):
        """
        Recherche les meilleurs jeunes talents dans une compétition donnée.
        Utilise les données réelles de Transfermarkt quand elles sont disponibles.
        
        Args:
            competition_id (str): ID de la compétition à analyser (Transfermarkt)
            age_max (int): Âge maximum pour considérer un joueur comme jeune (défaut: 23)
            limit (int): Nombre maximum de joueurs à retourner
            
        Returns:
            list: Liste des meilleurs jeunes talents identifiés
        """
        top_talents = []
        
        if self.use_real_data and competition_id:
            try:
                logger.info(f"Recherche des meilleurs jeunes talents dans la compétition {competition_id}")
                
                # Récupérer les clubs de la compétition
                competition_clubs = self.transfermarkt.get_competition_clubs(competition_id)
                if 'status' not in competition_clubs or competition_clubs['status'] != 'error':
                    clubs = competition_clubs.get('clubs', [])
                    
                    # Pour chaque club, analyser les jeunes joueurs
                    all_young_players = []
                    
                    for club in clubs:
                        if isinstance(club, dict):
                            club_id = club.get('id')
                            if not club_id:
                                continue
                                
                            # Récupérer les joueurs du club
                            club_players = self.transfermarkt.get_club_players(club_id)
                            if 'status' not in club_players or club_players['status'] != 'error':
                                players = club_players.get('squad', [])
                                
                                # Filtrer les jeunes joueurs
                                for player in players:
                                    if isinstance(player, dict):
                                        player_age = player.get('age', 30)
                                        try:
                                            player_age = int(player_age)
                                        except (ValueError, TypeError):
                                            player_age = 30
                                            
                                        if player_age <= age_max:
                                            # Ajouter le club au joueur
                                            player_copy = player.copy()  # Travailler sur une copie
                                            player_copy['club'] = club.get('name', '')
                                            player_copy['club_id'] = club_id
                                            
                                            # Calculer un score basé sur les attributs disponibles
                                            market_value = player_copy.get('market_value', 0)
                                            # S'assurer que market_value est un nombre
                                            if isinstance(market_value, str):
                                                try:
                                                    # Supprimer symboles monétaires et convertir en nombre
                                                    market_value = float(''.join(c for c in market_value if c.isdigit() or c == '.'))
                                                except:
                                                    market_value = 0

                                            age_factor = (age_max - player_age + 1) / 10  # Plus jeune = meilleur facteur
                                            
                                            # Le score combine valeur marchande et jeunesse
                                            player_copy['talent_score'] = float(market_value) * age_factor
                                            
                                            # Ajouter à la liste des jeunes joueurs
                                            all_young_players.append(player_copy)
                    
                    # Trier par score de talent et limiter le nombre
                    all_young_players.sort(key=lambda x: x.get('talent_score', 0), reverse=True)
                    top_talents = all_young_players[:limit]
                    
                    logger.info(f"Identification de {len(top_talents)} jeunes talents dans la compétition {competition_id}")
            
            except Exception as e:
                logger.error(f"Erreur lors de la recherche des jeunes talents: {e}")
        
        # Si pas de données réelles ou erreur, utiliser des données simulées
        if not top_talents:
            logger.warning("Utilisation de données simulées pour les jeunes talents")
            # Générer des données simulées
            top_talents = self._generate_simulated_talents(limit)
        
        return top_talents
        
    def _generate_simulated_talents(self, limit=10):
        """
        Génère une liste simulée de jeunes talents pour les cas où l'API n'est pas disponible.
        
        Args:
            limit (int): Nombre de talents à générer
            
        Returns:
            list: Liste des talents simulés
        """
        logger.info(f"Génération de {limit} jeunes talents simulés")
        
        # Listes pour générer des noms aléatoires
        first_names = ['Noah', 'Liam', 'Lucas', 'Ethan', 'Gabriel', 'Mohamed', 'Raphael', 'Adam', 'Leo', 'Hugo',
                      'Mateo', 'Tom', 'Louis', 'Nathan', 'Arthur', 'Jules', 'Yanis', 'Enzo', 'Axel', 'Gael']
        last_names = ['Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Richard', 'Petit', 'Durand', 'Leroy', 'Moreau',
                      'Simon', 'Laurent', 'Lefebvre', 'Michel', 'Garcia', 'David', 'Bertrand', 'Roux', 'Vincent', 'Fournier']
        
        clubs = ['Paris SG', 'Olympique Lyon', 'AS Monaco', 'LOSC Lille', 'OGC Nice', 'Olympique Marseille', 'Stade Rennais',
                'Montpellier HSC', 'RC Strasbourg', 'RC Lens', 'FC Nantes', 'AS Saint-Etienne', 'Bordeaux', 'Angers SCO',
                'Real Madrid', 'FC Barcelona', 'Manchester United', 'Liverpool FC', 'Bayern Munich', 'Juventus']
        
        positions = ['Gardien', 'Défenseur central', 'Arrière droit', 'Arrière gauche', 'Milieu défensif',
                     'Milieu central', 'Milieu offensif', 'Ailier droit', 'Ailier gauche', 'Attaquant']
        
        simulated_talents = []
        
        for i in range(limit):
            # Générer un âge entre 16 et 23 ans
            age = random.randint(16, 23)
            
            # Plus le joueur est jeune, plus son potentiel peut être élevé
            potential_max = 0.9 + ((23 - age) * 0.01)
            
            # Générer un profil aléatoire
            talent = {
                'id': f"SIM{100000 + i}",
                'name': f"{random.choice(first_names)} {random.choice(last_names)}",
                'age': age,
                'position': random.choice(positions),
                'club': random.choice(clubs),
                'club_id': f"CLUB{random.randint(1000, 9999)}",
                'market_value': random.randint(5000000, 80000000),
                'potential_ability': round(random.uniform(0.65, potential_max), 2),
                'attributes': {
                    'technical': round(random.uniform(0.5, 0.95), 2),
                    'physical': round(random.uniform(0.5, 0.95), 2),
                    'mental': round(random.uniform(0.5, 0.95), 2),
                    'tactical': round(random.uniform(0.5, 0.95), 2)
                },
                'talent_score': 0  # Sera calculé ci-dessous
            }
            
            # Calculer un score de talent (plus jeune = bonus)
            age_factor = (24 - age) / 10
            value_factor = talent['market_value'] / 50000000
            attribute_avg = sum(talent['attributes'].values()) / len(talent['attributes'])
            
            talent['talent_score'] = (value_factor * 0.4 + age_factor * 0.3 + attribute_avg * 0.3) * talent['potential_ability']
            
            simulated_talents.append(talent)
        
        # Trier par score de talent
        simulated_talents.sort(key=lambda x: x['talent_score'], reverse=True)
        
        return simulated_talents
    
    def track_youth_player_development(self, player_id, timeframe_months=6):
        """
        Suivre le développement d'un jeune joueur sur une période donnée.
        Utilise les données réelles de Transfermarkt quand elles sont disponibles.
        
        Args:
            player_id (str): Identifiant du joueur à suivre
            timeframe_months (int): Période d'analyse en mois
            
        Returns:
            dict: Analyse de l'évolution du joueur
        """
        # Vérifier si le joueur est suivi
        if player_id not in self.tracked_youth_players or not self.tracked_youth_players[player_id]:
            return {
                'status': 'error',
                'message': 'Aucune donnée de suivi pour ce joueur'
            }
        
        # Récupérer l'historique de suivi
        player_history = self.tracked_youth_players[player_id]
        
        # Filtrer pour la période demandée
        cutoff_date = datetime.now() - timedelta(days=30 * timeframe_months)
        relevant_history = [
            entry for entry in player_history
            if datetime.fromisoformat(entry['timestamp']) >= cutoff_date
        ]
        
        if not relevant_history:
            return {
                'status': 'error',
                'message': f'Aucune donnée de suivi pour les {timeframe_months} derniers mois'
            }
        
        # Trier par date
        relevant_history.sort(key=lambda x: x['timestamp'])
        
        # Extraire les valeurs pour l'analyse de tendance
        impact_values = [entry['current_impact'] for entry in relevant_history]
        potential_values = [entry['potential_impact'] for entry in relevant_history]
        minutes_values = [entry.get('minutes_played', 0) for entry in relevant_history]
        dates = [entry['timestamp'] for entry in relevant_history]
        
        # Calculer les tendances
        impact_trend = self._calculate_trend(impact_values)
        potential_trend = self._calculate_trend(potential_values)
        minutes_trend = self._calculate_trend(minutes_values)
        
        # Calculer le taux de développement
        if len(impact_values) >= 2:
            start_impact = impact_values[0]
            end_impact = impact_values[-1]
            development_rate = (end_impact - start_impact) / len(impact_values)
        else:
            development_rate = 0
        
        # Déterminer la trajectoire
        trajectory = 'stable'
        if development_rate > 0.05:
            trajectory = 'rapid_development'
        elif development_rate > 0.02:
            trajectory = 'steady_development'
        elif development_rate < -0.02:
            trajectory = 'regression'
        
        # Comparer à la courbe de développement attendue
        expected_dev_curve = None  # À implémenter avec des données réelles
        
        # Préparer le résultat
        result = {
            'player_id': player_id,
            'timeframe_months': timeframe_months,
            'development_rate': development_rate,
            'trajectory': trajectory,
            'current_impact': impact_values[-1] if impact_values else None,
            'impact_change': impact_values[-1] - impact_values[0] if len(impact_values) > 1 else 0,
            'potential_change': potential_values[-1] - potential_values[0] if len(potential_values) > 1 else 0,
            'trends': {
                'impact': impact_trend,
                'potential': potential_trend,
                'playing_time': minutes_trend
            },
            'data_points': len(relevant_history),
            'first_assessment': dates[0],
            'latest_assessment': dates[-1],
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def _analyze_player(self, player, team_data, match_data=None):
        """Analyser un jeune joueur individuellement."""
        # Extraire les informations du joueur
        player_id = player.get('id', '')
        player_name = player.get('name', '')
        age = player.get('age', 20)
        position = player.get('position', '')
        youth_category = player.get('youth_category', '')
        
        # Facteurs d'évaluation
        attributes = player.get('attributes', {})
        minutes_played = player.get('minutes_played', 0)
        minutes_factor = min(1.0, minutes_played / 900)  # Normaliser à 10 matchs complets
        
        # Contexte du match si disponible
        match_importance = 0.5
        if match_data:
            match_importance = match_data.get('importance', 0.5)
        
        # Calculer l'impact actuel
        current_impact = self._calculate_player_impact(player)
        
        # Calculer le potentiel d'impact
        potential_impact = self._calculate_player_potential(player, team_data)
        
        # Déterminer le modèle d'influence
        influence_model, influence_score = self._determine_influence_model(
            player, current_impact, minutes_factor
        )
        
        # Évaluer le risque de surcharge
        burnout_risk = self._calculate_burnout_risk(player, minutes_played, team_data)
        
        # Évaluer l'adéquation au style de l'équipe
        team_fit = self._evaluate_team_fit(player, team_data)
        
        # Préparer le résultat d'analyse
        result = {
            'player_id': player_id,
            'player_name': player_name,
            'age': age,
            'position': position,
            'youth_category': youth_category,
            'current_impact': current_impact,
            'potential_impact': potential_impact,
            'growth_potential': potential_impact - current_impact,
            'influence_model': influence_model,
            'influence_score': influence_score,
            'minutes_played': minutes_played,
            'minutes_factor': minutes_factor,
            'burnout_risk': burnout_risk,
            'team_fit': team_fit
        }
        
        return result
    
    def _calculate_player_impact(self, player):
        """Calculer l'impact actuel d'un joueur basé sur ses attributs."""
        attributes = player.get('attributes', {})
        
        # Si attributs vides, utiliser des valeurs par défaut basées sur la réputation
        if not attributes:
            reputation = player.get('reputation', 0.5)
            return reputation * 0.7  # Impact légèrement inférieur à la réputation
        
        # Calculer le score d'impact
        impact_score = 0.0
        total_weight = 0.0
        
        for factor, weight in self.impact_factors.items():
            if factor in attributes:
                impact_score += attributes[factor] * weight
                total_weight += weight
            
        # Normaliser si tous les facteurs ne sont pas présents
        if total_weight > 0:
            impact_score /= total_weight
        else:
            # Fallback à la réputation
            impact_score = player.get('reputation', 0.5) * 0.7
        
        # Ajuster selon les performances récentes
        recent_performance = player.get('recent_performance', 0.5)
        impact_score = (impact_score * 0.7) + (recent_performance * 0.3)
        
        return impact_score
    
    def _calculate_player_potential(self, player, team_data):
        """Calculer le potentiel d'impact futur d'un joueur."""
        # Extraire les informations
        age = player.get('age', 20)
        attributes = player.get('attributes', {})
        
        # Déterminer le coefficient de potentiel par âge
        age_coefficient = self.potential_age_coefficients.get(
            age, self.potential_age_coefficients.get(23, 0.75)
        )
        
        # Évaluer le potentiel brut
        raw_potential = player.get('potential_ability', 0.7)
        
        # Évaluer les facteurs de développement de l'équipe
        team_development_score = 0.0
        total_weight = 0.0
        
        for factor, weight in self.development_factors.items():
            factor_value = team_data.get(factor, 0.5)
            team_development_score += factor_value * weight
            total_weight += weight
        
        # Normaliser
        if total_weight > 0:
            team_development_score /= total_weight
        else:
            team_development_score = 0.5  # Valeur par défaut
        
        # Calculer le potentiel final
        potential_impact = raw_potential * age_coefficient * (0.7 + (team_development_score * 0.3))
        
        # Plafonner à 1.0
        return min(1.0, potential_impact)
    
    def _determine_influence_model(self, player, impact_score, minutes_factor):
        """Déterminer le modèle d'influence du joueur."""
        # Extraire les attributs pertinents
        consistency = player.get('attributes', {}).get('consistency', 0.5)
        big_game_ability = player.get('attributes', {}).get('big_match_influence', 0.5)
        leadership = player.get('attributes', {}).get('leadership', 0.3)
        
        # Calculer les scores d'influence pour chaque modèle
        model_scores = {}
        
        for model_name, model_data in self.influence_models.items():
            # Facteurs spécifiques au modèle
            impact_factor = impact_score / model_data['threshold']
            consistency_match = max(0, consistency / model_data['consistency_requirement'])
            
            # Score spécifique aux modèles
            if model_name == 'game_changer':
                model_scores[model_name] = (impact_factor * 0.5) + (big_game_ability * 0.3) + (minutes_factor * 0.2)
            elif model_name == 'core_contributor':
                model_scores[model_name] = (impact_factor * 0.4) + (consistency_match * 0.4) + (minutes_factor * 0.2)
            elif model_name == 'squad_player':
                model_scores[model_name] = (impact_factor * 0.3) + (consistency_match * 0.3) + (minutes_factor * 0.4)
            else:  # prospect
                model_scores[model_name] = (impact_factor * 0.7) + (minutes_factor * 0.1) + (leadership * 0.2)
        
        # Trouver le modèle avec le score le plus élevé
        best_model = max(model_scores.items(), key=lambda x: x[1])
        
        return best_model[0], best_model[1]
    
    def _calculate_burnout_risk(self, player, minutes_played, team_data):
        """Calculer le risque de surcharge pour un jeune joueur."""
        # Facteurs de risque
        age = player.get('age', 20)
        physical_development = player.get('attributes', {}).get('physical_development', 0.5)
        injury_proneness = player.get('injury_proneness', 0.3)
        fixture_congestion = team_data.get('fixture_congestion', 0.3)
        
        # Base de risque selon l'âge
        base_risk = 0.0
        if age <= 18:
            base_risk = 0.5  # Risque de base plus élevé pour les très jeunes
        elif age <= 21:
            base_risk = 0.3
        else:
            base_risk = 0.2
        
        # Ajuster selon le temps de jeu (normalisé sur une saison de 3420 minutes)
        minutes_factor = minutes_played / 3420  # ~38 matchs de 90 minutes
        
        # Ajuster selon les facteurs individuels et contextuels
        risk_score = base_risk * (
            1.0 +
            (minutes_factor * 0.5) +
            (injury_proneness * 0.3) +
            (fixture_congestion * 0.2) -
            (physical_development * 0.4)  # Meilleur développement physique = moins de risque
        )
        
        # Limiter le score entre 0 et 1
        risk_score = max(0.0, min(1.0, risk_score))
        
        # Classifier le risque
        risk_category = 'low'
        if risk_score > 0.7:
            risk_category = 'high'
        elif risk_score > 0.4:
            risk_category = 'medium'
        
        return {
            'score': risk_score,
            'category': risk_category,
            'minutes_factor': minutes_factor,
            'age_factor': base_risk
        }
    
    def _evaluate_team_fit(self, player, team_data):
        """Évaluer l'adéquation du joueur au style de l'équipe."""
        # Style de jeu de l'équipe
        team_style = team_data.get('playing_style', 'balanced')
        formation = team_data.get('formation', '4-4-2')
        position_emphasis = team_data.get('position_emphasis', {})
        
        # Attributs du joueur
        position = player.get('position', '')
        attributes = player.get('attributes', {})
        
        # Adéquation basée sur le style de jeu
        style_fit = 0.5  # Valeur par défaut
        
        if team_style == 'attacking':
            if 'attacking' in attributes and 'creativity' in attributes:
                style_fit = (attributes['attacking'] * 0.6) + (attributes['creativity'] * 0.4)
        elif team_style == 'defensive':
            if 'defending' in attributes and 'positioning' in attributes:
                style_fit = (attributes['defending'] * 0.6) + (attributes['positioning'] * 0.4)
        elif team_style == 'possession':
            if 'technique' in attributes and 'passing' in attributes:
                style_fit = (attributes['technique'] * 0.5) + (attributes['passing'] * 0.5)
        elif team_style == 'counter':
            if 'speed' in attributes and 'decision_making' in attributes:
                style_fit = (attributes['speed'] * 0.6) + (attributes['decision_making'] * 0.4)
        
        # Adéquation basée sur la position dans la formation
        position_fit = 0.5  # Valeur par défaut
        
        if position in position_emphasis:
            position_importance = position_emphasis[position]
            
            # Plus la position est importante, plus l'adéquation doit être élevée
            position_key_attributes = []
            
            if position in ['GK']:
                position_key_attributes = ['reflexes', 'positioning', 'handling']
            elif position in ['CB', 'LB', 'RB']:
                position_key_attributes = ['defending', 'strength', 'positioning']
            elif position in ['CM', 'CDM']:
                position_key_attributes = ['passing', 'vision', 'stamina']
            elif position in ['CAM', 'LM', 'RM']:
                position_key_attributes = ['creativity', 'passing', 'technique']
            elif position in ['ST', 'CF', 'LW', 'RW']:
                position_key_attributes = ['finishing', 'attacking', 'technique']
            
            # Calculer l'adéquation à la position
            attribute_scores = []
            for attr in position_key_attributes:
                if attr in attributes:
                    attribute_scores.append(attributes[attr])
            
            if attribute_scores:
                position_fit = sum(attribute_scores) / len(attribute_scores)
        
        # Calculer l'adéquation globale
        overall_fit = (style_fit * 0.6) + (position_fit * 0.4)
        
        # Classifier l'adéquation
        fit_category = 'average'
        if overall_fit > 0.8:
            fit_category = 'excellent'
        elif overall_fit > 0.65:
            fit_category = 'good'
        elif overall_fit < 0.4:
            fit_category = 'poor'
        
        return {
            'overall_fit': overall_fit,
            'style_fit': style_fit,
            'position_fit': position_fit,
            'category': fit_category
        }
    
    def _determine_youth_category(self, age):
        """Déterminer la catégorie jeune en fonction de l'âge."""
        for category, age_range in self.youth_categories.items():
            if age_range['min_age'] <= age <= age_range['max_age']:
                return category
        return None
    
    def _determine_youth_strategy(self, young_players, team_data):
        """Déterminer la stratégie jeune de l'équipe."""
        # Analyser la distribution par catégorie
        category_counts = {'prodigy': 0, 'breakthrough': 0, 'emerging': 0}
        
        for player in young_players:
            category = player.get('youth_category', '')
            if category in category_counts:
                category_counts[category] += 1
        
        # Calculer les minutes par catégorie
        total_minutes = sum(player.get('minutes_played', 0) for player in young_players)
        
        # Données supplémentaires de l'équipe
        transfer_policy = team_data.get('youth_transfer_policy', 'balanced')
        academy_focus = team_data.get('academy_focus', 'balanced')
        
        # Déterminer la stratégie
        if total_minutes > 4000 and category_counts['prodigy'] >= 2:
            strategy = 'youth_focused'
        elif category_counts['emerging'] > category_counts['prodigy'] + category_counts['breakthrough']:
            strategy = 'development_buyers'
        elif category_counts['breakthrough'] > category_counts['prodigy'] and total_minutes > 2000:
            strategy = 'breakthrough_platform'
        elif transfer_policy == 'sell_high':
            strategy = 'talent_factory'
        elif academy_focus == 'high' and category_counts['prodigy'] > 0:
            strategy = 'academy_prioritization'
        else:
            strategy = 'balanced_approach'
        
        # Description détaillée
        strategy_descriptions = {
            'youth_focused': 'Forte intégration des jeunes à tous les niveaux',
            'development_buyers': 'Focus sur les jeunes en phase d\'émergence (22-23 ans)',
            'breakthrough_platform': 'Plateforme pour les talents en éclosion (19-21 ans)',
            'talent_factory': 'Développement et vente de jeunes talents',
            'academy_prioritization': 'Accent sur les produits de l\'académie',
            'balanced_approach': 'Approche équilibrée sans focus jeune marqué'
        }
        
        return {
            'type': strategy,
            'description': strategy_descriptions.get(strategy, ''),
            'category_distribution': category_counts,
            'youth_minutes': total_minutes
        }
    
    def _evaluate_development_effectiveness(self, analyzed_players, team_data):
        """Évaluer l'efficacité du développement des jeunes de l'équipe."""
        if not analyzed_players:
            return {
                'effectiveness': 0.0,
                'category': 'insufficient_data'
            }
        
        # Calculer le différentiel moyen entre impact actuel et potentiel
        growth_potentials = [player['growth_potential'] for player in analyzed_players]
        avg_growth_potential = sum(growth_potentials) / len(growth_potentials)
        
        # Facteurs de développement de l'équipe
        training_quality = team_data.get('training_quality', 0.5)
        youth_coaching = team_data.get('youth_coaching', 0.5)
        playing_opportunities = team_data.get('youth_playing_time', 0.3)
        
        # Calculer l'efficacité actuelle
        current_effectiveness = (
            training_quality * 0.4 +
            youth_coaching * 0.4 +
            playing_opportunities * 0.2
        )
        
        # Rapport entre développement et infrastructure
        potential_fulfillment = 0.0
        for player in analyzed_players:
            # Plus les jeunes ont de temps de jeu, plus on peut évaluer
            minutes_factor = min(1.0, player.get('minutes_played', 0) / 900)
            
            if minutes_factor > 0.2:  # Au moins un peu de temps de jeu
                # Ratio entre l'impact actuel et potentiel (normalisé)
                if player['potential_impact'] > 0:
                    fulfillment = player['current_impact'] / player['potential_impact']
                    potential_fulfillment += fulfillment * minutes_factor
        
        # Normaliser
        if sum(player.get('minutes_factor', 0) for player in analyzed_players) > 0:
            potential_fulfillment /= sum(player.get('minutes_factor', 0) for player in analyzed_players)
        else:
            potential_fulfillment = 0.0
        
        # Calculer le score d'efficacité globale
        effectiveness_score = (current_effectiveness * 0.6) + (potential_fulfillment * 0.4)
        
        # Classifier l'efficacité
        effectiveness_category = 'average'
        if effectiveness_score > 0.8:
            effectiveness_category = 'excellent'
        elif effectiveness_score > 0.65:
            effectiveness_category = 'good'
        elif effectiveness_score < 0.4:
            effectiveness_category = 'poor'
        
        return {
            'effectiveness': effectiveness_score,
            'category': effectiveness_category,
            'current_development_quality': current_effectiveness,
            'potential_fulfillment': potential_fulfillment,
            'average_growth_potential': avg_growth_potential
        }
    
    def _calculate_development_rate(self, player_data):
        """Calculer le taux de développement d'un jeune joueur."""
        # Facteurs qui influencent le taux de développement
        age = player_data.get('age', 20)
        potential = player_data.get('potential_ability', 0.7)
        intelligence = player_data.get('attributes', {}).get('intelligence', 0.5)
        professionalism = player_data.get('attributes', {}).get('professionalism', 0.5)
        determination = player_data.get('attributes', {}).get('determination', 0.5)
        
        # Base de taux selon l'âge (les plus jeunes se développent plus vite)
        if age <= 18:
            base_rate = 0.03  # 3% par mois
        elif age <= 21:
            base_rate = 0.02  # 2% par mois
        else:  # 22-23
            base_rate = 0.01  # 1% par mois
        
        # Ajuster selon les attributs
        adjusted_rate = base_rate * (
            1.0 +
            ((potential - 0.5) * 0.4) +  # Plus de potentiel = développement plus rapide
            ((intelligence - 0.5) * 0.2) +
            ((professionalism - 0.5) * 0.2) +
            ((determination - 0.5) * 0.2)
        )
        
        # Limiter à des valeurs raisonnables
        return max(0.005, min(0.04, adjusted_rate))
    
    def _identify_key_development_areas(self, player_data, projected_attributes):
        """Identifier les domaines clés de développement pour un joueur."""
        # Position du joueur
        position = player_data.get('position', '')
        
        # Attributs actuels et projetés
        current_attributes = player_data.get('attributes', {})
        
        # Domaines clés selon la position
        position_key_areas = {}
        
        if position in ['GK']:
            position_key_areas = {'reflexes': 0.3, 'positioning': 0.3, 'handling': 0.2, 'decision_making': 0.2}
        elif position in ['CB', 'LB', 'RB']:
            position_key_areas = {'defending': 0.3, 'positioning': 0.3, 'strength': 0.2, 'passing': 0.1, 'tackling': 0.1}
        elif position in ['CM', 'CDM']:
            position_key_areas = {'passing': 0.3, 'stamina': 0.2, 'vision': 0.2, 'technique': 0.1, 'tackling': 0.1, 'positioning': 0.1}
        elif position in ['CAM', 'LM', 'RM']:
            position_key_areas = {'creativity': 0.3, 'passing': 0.3, 'technique': 0.2, 'vision': 0.1, 'speed': 0.1}
        elif position in ['ST', 'CF', 'LW', 'RW']:
            position_key_areas = {'finishing': 0.3, 'attacking': 0.2, 'technique': 0.2, 'speed': 0.1, 'movement': 0.1, 'strength': 0.1}
        else:
            position_key_areas = {'technique': 0.2, 'passing': 0.2, 'stamina': 0.2, 'defending': 0.2, 'attacking': 0.2}
        
        # Évaluer les attributs actuels par rapport aux exigences de la position
        development_areas = []
        
        for attr, importance in position_key_areas.items():
            if attr in current_attributes:
                current_value = current_attributes[attr]
                projected_value = projected_attributes.get(attr, current_value)
                
                # Calculer l'écart avec un niveau "cible" pour la position (0.7 est considéré comme bon)
                gap = max(0, 0.7 - current_value)
                expected_improvement = projected_value - current_value
                
                # Si l'attribut est important et a besoin d'amélioration
                if gap > 0.1 and importance > 0.1:
                    development_areas.append({
                        'attribute': attr,
                        'current_value': current_value,
                        'projected_value': projected_value,
                        'expected_improvement': expected_improvement,
                        'importance': importance,
                        'gap': gap,
                        'priority': 'high' if (gap * importance) > 0.15 else 'medium'
                    })
        
        # Trier par priorité
        development_areas.sort(key=lambda x: x['gap'] * x['importance'], reverse=True)
        
        return development_areas[:3]  # Retourner les 3 principales zones de développement
    
    def _calculate_stagnation_risk(self, player_data, playing_time_forecast, coaching_quality):
        """Calculer le risque de stagnation d'un jeune joueur."""
        # Facteurs de risque
        age = player_data.get('age', 20)
        potential = player_data.get('potential_ability', 0.7)
        determination = player_data.get('attributes', {}).get('determination', 0.5)
        adaptability = player_data.get('attributes', {}).get('adaptability', 0.5)
        
        # Risque de base (plus le potentiel est élevé, plus le risque de ne pas l'atteindre est grand)
        base_risk = potential * 0.5
        
        # Facteurs d'atténuation
        mitigating_factors = (
            (playing_time_forecast * 0.4) +
            (coaching_quality * 0.3) +
            (determination * 0.2) +
            (adaptability * 0.1)
        )
        
        # Calculer le risque final
        stagnation_risk = base_risk * (1.0 - mitigating_factors)
        
        # Ajuster selon l'âge (risque plus élevé si proche de la limite d'âge "jeune")
        if age >= 22:
            stagnation_risk *= 1.2
        
        # Limiter à des valeurs raisonnables
        stagnation_risk = max(0.1, min(0.9, stagnation_risk))
        
        # Classifier le risque
        risk_category = 'moderate'
        if stagnation_risk > 0.7:
            risk_category = 'high'
        elif stagnation_risk < 0.4:
            risk_category = 'low'
        
        return {
            'risk_score': stagnation_risk,
            'category': risk_category,
            'key_factor': 'playing_time' if playing_time_forecast < 0.3 else (
                'coaching' if coaching_quality < 0.4 else (
                    'mentality' if determination < 0.4 else 'potential_ceiling'
                )
            )
        }
    
    def _calculate_investment_efficiency(self, team_data):
        """Calculer l'efficacité de l'investissement dans les jeunes."""
        youth_investment = team_data.get('youth_investment', 0.5)
        youth_output = team_data.get('youth_output', 0.3)  # Valeur générée par les jeunes
        sales_revenue = team_data.get('youth_sales_revenue', 0.2)  # Revenus des transferts de jeunes
        
        # Si pas d'investissement, pas d'efficacité à calculer
        if youth_investment == 0:
            return 0.0
        
        # Calculer le rapport entre résultats et investissement
        return (youth_output * 0.7 + sales_revenue * 0.3) / youth_investment
    
    def _calculate_percentile(self, value, distribution):
        """Calculer le percentile d'une valeur dans une distribution."""
        if not distribution:
            return 50  # Percentile par défaut
        
        # Trier la distribution
        sorted_dist = sorted(distribution)
        
        # Trouver la position
        count = 0
        for item in sorted_dist:
            if item < value:
                count += 1
            else:
                break
        
        # Calculer le percentile
        return (count / len(sorted_dist)) * 100
    
    def _generate_strategy_recommendations(self, team_data, strengths, weaknesses):
        """Générer des recommandations pour la stratégie jeunes."""
        recommendations = []
        
        # Recommandations basées sur les faiblesses
        for weakness in weaknesses:
            if weakness['aspect'] == 'infrastructure':
                recommendations.append({
                    'area': 'infrastructure',
                    'recommendation': 'Investissement dans les installations de formation',
                    'description': 'Améliorer les infrastructures pour offrir un environnement optimal de développement',
                    'priority': 'high'
                })
            elif weakness['aspect'] == 'talent_pipeline':
                recommendations.append({
                    'area': 'scouting',
                    'recommendation': 'Renforcer le réseau de détection',
                    'description': 'Améliorer la détection des jeunes talents locaux et internationaux',
                    'priority': 'high'
                })
                
                recommendations.append({
                    'area': 'academy',
                    'recommendation': 'Restructuration académique',
                    'description': 'Revoir les méthodes de formation et les objectifs de développement',
                    'priority': 'medium'
                })
            elif weakness['aspect'] == 'youth_utilization':
                recommendations.append({
                    'area': 'playing_time',
                    'recommendation': 'Programme d\'intégration progressive',
                    'description': 'Mettre en place un plan pour accorder plus de temps de jeu aux jeunes',
                    'priority': 'high'
                })
        
        # Recommandations générales si peu de faiblesses spécifiques
        if len(weaknesses) < 2:
            youth_investment = team_data.get('youth_investment', 0.5)
            
            if youth_investment < 0.5:
                recommendations.append({
                    'area': 'investment',
                    'recommendation': 'Augmentation de l\'investissement jeunes',
                    'description': 'Accroître les ressources allouées au département de formation',
                    'priority': 'medium'
                })
            
            recommendations.append({
                'area': 'loan_strategy',
                'recommendation': 'Stratégie de prêts ciblés',
                'description': 'Développer un programme de prêts adaptés au niveau et aux besoins de chaque jeune',
                'priority': 'medium'
            })
        
        # Recommandations pour capitaliser sur les forces
        if any(strength['aspect'] == 'infrastructure' for strength in strengths):
            recommendations.append({
                'area': 'recruitment',
                'recommendation': 'Attirer des jeunes talents premium',
                'description': 'Utiliser la qualité des infrastructures comme argument de recrutement',
                'priority': 'medium'
            })
        
        if any(strength['aspect'] == 'youth_utilization' for strength in strengths):
            recommendations.append({
                'area': 'branding',
                'recommendation': 'Renforcer l\'image "formation"',
                'description': 'Capitaliser sur la réputation de club formateur pour le recrutement',
                'priority': 'low'
            })
        
        return recommendations
    
    def _calculate_trend(self, values):
        """Calculer la tendance d'une série de valeurs."""
        if len(values) < 2:
            return 'insufficient_data'
        
        # Calcul simple de la tendance
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        # Déterminer la direction de la tendance
        if second_avg > first_avg * 1.1:
            return 'strong_increase'
        elif second_avg > first_avg * 1.03:
            return 'moderate_increase'
        elif second_avg > first_avg:
            return 'slight_increase'
        elif second_avg < first_avg * 0.9:
            return 'strong_decrease'
        elif second_avg < first_avg * 0.97:
            return 'moderate_decrease'
        elif second_avg < first_avg:
            return 'slight_decrease'
        else:
            return 'stable'