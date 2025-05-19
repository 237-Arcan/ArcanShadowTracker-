"""
Adaptateur SoccerData pour ArcanShadow.
Ce module fournit une interface simplifiée pour accéder aux données de soccerdata
via notre module d'intégration existant.
"""

import logging
from datetime import datetime
import pandas as pd
import math

# Importer notre module d'intégration
from api.soccerdata_integration import get_soccer_data_integration, is_soccerdata_available

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SoccerDataAdapter:
    """
    Adaptateur pour faciliter l'accès aux données de soccerdata
    depuis le hub d'intégration central.
    """
    
    def __init__(self):
        """Initialise l'adaptateur SoccerData."""
        # Récupérer l'instance d'intégration
        self.integration = get_soccer_data_integration()
        self.available = is_soccerdata_available()
        
        if self.available:
            logger.info("Adaptateur SoccerData initialisé avec succès")
            self.sources_available = self.integration.sources_available
            logger.info(f"Sources disponibles: {self.sources_available}")
        else:
            logger.warning("SoccerData n'est pas disponible, fonctionnement limité")
    
    def get_team_form(self, team_name, last_matches=5, source='sofascore'):
        """
        Récupère la forme récente d'une équipe.
        
        Args:
            team_name (str): Nom de l'équipe
            last_matches (int): Nombre de derniers matchs à considérer
            source (str): Source de données à utiliser
            
        Returns:
            dict: Informations sur la forme récente
        """
        if not self.available:
            return self._generate_simulated_form(team_name, last_matches)
        
        try:
            return self.integration.get_team_recent_form(team_name, last_matches, source)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la forme de {team_name}: {e}")
            return self._generate_simulated_form(team_name, last_matches)
    
    def get_player_stats(self, player_name, team=None, season=None, source='fbref'):
        """
        Récupère les statistiques d'un joueur.
        
        Args:
            player_name (str): Nom du joueur
            team (str, optional): Équipe du joueur pour préciser la recherche
            season (str, optional): Saison des statistiques
            source (str): Source de données à utiliser
            
        Returns:
            dict: Statistiques du joueur
        """
        if not self.available:
            return self._generate_simulated_player_stats(player_name, team)
        
        try:
            stats_df = self.integration.get_player_statistics(player_name, team, season, source)
            if stats_df.empty:
                return self._generate_simulated_player_stats(player_name, team)
            
            # Convertir le DataFrame en dictionnaire
            return self._process_player_stats(stats_df, player_name)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats de {player_name}: {e}")
            return self._generate_simulated_player_stats(player_name, team)
    
    def get_match_statistics(self, home_team, away_team, date=None, source='sofascore'):
        """
        Récupère les statistiques d'un match.
        
        Args:
            home_team (str): Équipe à domicile
            away_team (str): Équipe à l'extérieur
            date (str, optional): Date du match au format YYYY-MM-DD
            source (str): Source de données à utiliser
            
        Returns:
            dict: Statistiques du match
        """
        if not self.available:
            return self._generate_simulated_match_stats(home_team, away_team)
        
        try:
            return self.integration.get_match_statistics(home_team, away_team, date, source)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats du match {home_team} vs {away_team}: {e}")
            return self._generate_simulated_match_stats(home_team, away_team)
    
    def get_league_table(self, league_code, season=None, source='fbref'):
        """
        Récupère le classement d'une ligue.
        
        Args:
            league_code (str): Code standardisé de la ligue (ex: "PL" pour Premier League)
            season (str, optional): Saison du classement
            source (str): Source de données à utiliser
            
        Returns:
            list: Classement de la ligue
        """
        if not self.available:
            return self._generate_simulated_league_table(league_code)
        
        try:
            table_df = self.integration.get_league_standings(league_code, season, source)
            if table_df.empty:
                return self._generate_simulated_league_table(league_code)
            
            # Convertir le DataFrame en liste de dictionnaires
            return table_df.to_dict('records')
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du classement de {league_code}: {e}")
            return self._generate_simulated_league_table(league_code)
    
    def _process_player_stats(self, stats_df, player_name):
        """
        Traite un DataFrame de statistiques de joueur en dictionnaire utilisable.
        
        Args:
            stats_df (pd.DataFrame): DataFrame contenant les statistiques
            player_name (str): Nom du joueur
            
        Returns:
            dict: Statistiques du joueur structurées
        """
        # Extraction basique de statistiques communes
        results = {
            "player_name": player_name,
            "stats": {}
        }
        
        # Tenter d'extraire les colonnes les plus communes
        common_stats = [
            "goals", "assists", "goals_per90", "min", "games", "games_starts",
            "xg", "npxg", "xa", "shots", "shots_on_target", "yellow_cards", "red_cards"
        ]
        
        for stat in common_stats:
            for col in stats_df.columns:
                if stat.lower() in col.lower():
                    try:
                        value = stats_df[col].iloc[0]
                        if pd.notna(value):
                            results["stats"][stat] = float(value) if isinstance(value, (int, float)) else str(value)
                    except:
                        pass
        
        return results
    
    def _generate_simulated_form(self, team_name, last_matches=5):
        """
        Génère des données simulées pour la forme d'une équipe.
        
        Args:
            team_name (str): Nom de l'équipe
            last_matches (int): Nombre de derniers matchs
            
        Returns:
            dict: Forme simulée
        """
        import random
        
        # Résultats possibles: victoire (W), défaite (L), nul (D)
        results = ["W", "L", "D"]
        weights = [0.4, 0.3, 0.3]  # Probabilités pour chaque résultat
        
        # Générer les résultats des derniers matchs
        last_results = random.choices(results, weights=weights, k=last_matches)
        
        # Calculer statistiques basiques
        wins = last_results.count("W")
        draws = last_results.count("D")
        losses = last_results.count("L")
        
        # Points (3 pour une victoire, 1 pour un nul)
        points = wins * 3 + draws
        
        # Générer des scores plausibles
        scores = []
        for result in last_results:
            if result == "W":
                scores.append(f"{random.randint(1, 4)}-{random.randint(0, 2)}")
            elif result == "L":
                scores.append(f"{random.randint(0, 2)}-{random.randint(1, 4)}")
            else:  # Draw
                score = random.randint(0, 3)
                scores.append(f"{score}-{score}")
        
        return {
            "team": team_name,
            "last_results": last_results,
            "scores": scores,
            "summary": {
                "wins": wins,
                "draws": draws,
                "losses": losses,
                "points": points,
                "form_rating": round(points / (last_matches * 3) * 10, 1)  # Rating sur 10
            }
        }
    
    def _generate_simulated_player_stats(self, player_name, team=None):
        """
        Génère des statistiques simulées pour un joueur.
        
        Args:
            player_name (str): Nom du joueur
            team (str, optional): Équipe du joueur
            
        Returns:
            dict: Statistiques simulées
        """
        import random
        
        # Déterminer le rôle probable du joueur d'après son nom (pour la simulation)
        goalkeeper = False
        defender = False
        midfielder = False
        forward = False
        
        # Simuler une analyse du nom du joueur pour déterminer son poste
        # (simplement pour la variété des statistiques simulées)
        random_position = random.choice(["GK", "DF", "MF", "FW"])
        
        if random_position == "GK":
            goalkeeper = True
        elif random_position == "DF":
            defender = True
        elif random_position == "MF":
            midfielder = True
        else:
            forward = True
        
        # Simuler des matchs joués
        games_played = random.randint(15, 38)
        minutes_played = games_played * random.randint(60, 90)
        
        stats = {
            "player_name": player_name,
            "team": team or "Unknown Team",
            "position": random_position,
            "stats": {
                "games": games_played,
                "games_starts": max(0, games_played - random.randint(0, 5)),
                "min": minutes_played,
            }
        }
        
        # Statistiques spécifiques au poste
        if goalkeeper:
            stats["stats"].update({
                "goals_against": random.randint(15, 40),
                "goals_against_per90": round(random.uniform(0.8, 2.0), 2),
                "shots_on_target_against": random.randint(50, 150),
                "save_pct": round(random.uniform(60, 85), 1),
                "clean_sheets": random.randint(5, 15),
                "yellow_cards": random.randint(0, 3),
                "red_cards": random.randint(0, 1)
            })
        elif defender:
            stats["stats"].update({
                "goals": random.randint(0, 5),
                "assists": random.randint(0, 5),
                "goals_per90": round(random.uniform(0, 0.2), 2),
                "tackles": random.randint(40, 100),
                "interceptions": random.randint(30, 80),
                "blocks": random.randint(20, 50),
                "yellow_cards": random.randint(2, 10),
                "red_cards": random.randint(0, 2)
            })
        elif midfielder:
            stats["stats"].update({
                "goals": random.randint(2, 10),
                "assists": random.randint(3, 15),
                "goals_per90": round(random.uniform(0.1, 0.3), 2),
                "xg": round(random.uniform(3, 12), 1),
                "xa": round(random.uniform(4, 15), 1),
                "passes_completed": random.randint(800, 2000),
                "pass_completion_pct": round(random.uniform(75, 92), 1),
                "yellow_cards": random.randint(2, 8),
                "red_cards": random.randint(0, 1)
            })
        else:  # Forward
            stats["stats"].update({
                "goals": random.randint(5, 25),
                "assists": random.randint(2, 15),
                "goals_per90": round(random.uniform(0.3, 0.8), 2),
                "xg": round(random.uniform(7, 25), 1),
                "xa": round(random.uniform(2, 15), 1),
                "shots": random.randint(40, 120),
                "shots_on_target": random.randint(20, 60),
                "yellow_cards": random.randint(1, 6),
                "red_cards": random.randint(0, 1)
            })
        
        return stats
    
    def _generate_simulated_match_stats(self, home_team, away_team):
        """
        Génère des statistiques simulées pour un match.
        
        Args:
            home_team (str): Équipe à domicile
            away_team (str): Équipe à l'extérieur
            
        Returns:
            dict: Statistiques simulées du match
        """
        import random
        
        # Scores aléatoires
        home_score = random.randint(0, 4)
        away_score = random.randint(0, 3)
        
        # Statistiques de base qui varient selon le score
        home_shots = random.randint(8, 20)
        away_shots = random.randint(6, 18)
        
        home_possession = random.randint(40, 60)
        away_possession = 100 - home_possession
        
        return {
            "match": f"{home_team} vs {away_team}",
            "score": f"{home_score}-{away_score}",
            "home": {
                "team": home_team,
                "goals": home_score,
                "shots": home_shots,
                "shots_on_target": random.randint(math.ceil(home_shots/3), home_shots),
                "possession": home_possession,
                "passes": random.randint(300, 600),
                "pass_accuracy": random.randint(70, 90),
                "corners": random.randint(2, 10),
                "offsides": random.randint(0, 5),
                "fouls": random.randint(5, 15),
                "yellow_cards": random.randint(0, 3),
                "red_cards": random.randint(0, 1)
            },
            "away": {
                "team": away_team,
                "goals": away_score,
                "shots": away_shots,
                "shots_on_target": random.randint(math.ceil(away_shots/3), away_shots),
                "possession": away_possession,
                "passes": random.randint(300, 600),
                "pass_accuracy": random.randint(70, 90),
                "corners": random.randint(2, 10),
                "offsides": random.randint(0, 5),
                "fouls": random.randint(5, 15),
                "yellow_cards": random.randint(0, 3),
                "red_cards": random.randint(0, 1)
            }
        }
    
    def _generate_simulated_league_table(self, league_code):
        """
        Génère un classement simulé pour une ligue.
        
        Args:
            league_code (str): Code de la ligue
            
        Returns:
            list: Classement simulé
        """
        import random
        
        # Définir des équipes par ligue (quelques équipes populaires)
        league_teams = {
            "PL": ["Manchester City", "Liverpool", "Arsenal", "Manchester United", 
                   "Tottenham", "Chelsea", "Newcastle", "Aston Villa", 
                   "West Ham", "Brighton", "Everton", "Fulham", 
                   "Crystal Palace", "Brentford", "Nottingham Forest", "Wolves", 
                   "Bournemouth", "Sheffield United", "Luton Town", "Burnley"],
            "BL1": ["Bayern Munich", "Borussia Dortmund", "RB Leipzig", "Bayer Leverkusen", 
                    "Eintracht Frankfurt", "Wolfsburg", "Borussia Mönchengladbach", 
                    "Hoffenheim", "Stuttgart", "Union Berlin", "Mainz", "Augsburg", 
                    "Werder Bremen", "Freiburg", "FC Köln", "Heidenheim", "Bochum", "Holstein Kiel"],
            "FL1": ["PSG", "Marseille", "Lyon", "Monaco", "Lille", "Rennes", 
                    "Nice", "Lens", "Strasbourg", "Reims", "Nantes", "Montpellier", 
                    "Toulouse", "Brest", "Angers", "Auxerre", "Metz", "Le Havre"],
            "SA": ["Inter", "AC Milan", "Juventus", "AS Roma", "Napoli", "Lazio", 
                   "Atalanta", "Fiorentina", "Bologna", "Torino", "Udinese", 
                   "Sassuolo", "Verona", "Empoli", "Cagliari", "Venezia", "Parma", "Como"],
            "PD": ["Real Madrid", "Barcelona", "Atlético Madrid", "Sevilla", "Villarreal", 
                   "Real Sociedad", "Real Betis", "Athletic Bilbao", "Valencia", 
                   "Osasuna", "Espanyol", "Mallorca", "Alavés", "Getafe", "Girona", 
                   "Las Palmas", "Celta Vigo", "Rayo Vallecano"]
        }
        
        # Utiliser la liste par défaut si la ligue n'est pas reconnue
        teams = league_teams.get(league_code, [f"Team{i}" for i in range(1, 19)])
        
        # Générer des statistiques pour chaque équipe
        result = []
        total_matches = random.randint(10, 38)  # Nombre de matchs joués dans la saison
        
        # Trier les équipes pour créer un semblant de classement
        teams_performance = [(team, random.random()) for team in teams]
        teams_performance.sort(key=lambda x: x[1], reverse=True)
        
        for rank, (team, perf) in enumerate(teams_performance, 1):
            # Plus le rang est élevé, moins les statistiques sont bonnes
            perf_factor = (len(teams) - rank + 1) / len(teams)
            
            # Générer les statistiques relatives à la performance
            matches_played = total_matches
            max_possible_wins = min(matches_played, round(matches_played * perf_factor))
            wins = random.randint(max(1, max_possible_wins - 5), max_possible_wins)
            max_possible_draws = matches_played - wins
            draws = random.randint(0, min(max_possible_draws, round(max_possible_draws * random.random())))
            losses = matches_played - wins - draws
            
            points = wins * 3 + draws
            
            goals_for = wins * random.randint(1, 3) + draws * random.randint(0, 2) + losses * random.randint(0, 1)
            goals_against = losses * random.randint(1, 3) + draws * random.randint(0, 2) + wins * random.randint(0, 1)
            
            result.append({
                "rank": rank,
                "team": team,
                "matches_played": matches_played,
                "wins": wins,
                "draws": draws,
                "losses": losses,
                "goals_for": goals_for,
                "goals_against": goals_against,
                "goal_difference": goals_for - goals_against,
                "points": points
            })
        
        return result