"""
Module d'enrichissement des données sur les joueurs et managers pour ArcanShadow.
Ce module s'inspire de la structure de données détaillée de sofascore pour
enrichir les informations sur les joueurs et les managers disponibles dans le système.
"""

import logging
import pandas as pd
import requests
from datetime import datetime
import os
import json

# Importer nos adaptateurs
from api.transfermarkt_integration import is_transfermarkt_available, get_team_players, get_player_profile
from api.soccerdata_integration import is_soccerdata_available, get_soccer_data_integration

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chemins pour le stockage de données en cache
CACHE_DIR = os.path.join(os.getcwd(), 'data', 'player_data_cache')
os.makedirs(CACHE_DIR, exist_ok=True)

# Structure des données pour les joueurs (inspirée de sofascore)
PLAYER_DATA_STRUCTURE = {
    'name': '',                  # Nom du joueur
    'full_name': '',             # Nom complet
    'nationality': '',           # Nationalité
    'birth_date': None,          # Date de naissance
    'age': None,                 # Âge
    'height': None,              # Taille en cm
    'weight': None,              # Poids en kg
    'preferred_foot': '',        # Pied préféré
    'position': '',              # Position principale
    'secondary_position': '',    # Position secondaire
    'shirt_number': None,        # Numéro de maillot
    'team': '',                  # Équipe actuelle
    'market_value': None,        # Valeur marchande
    'contract_until': '',        # Fin de contrat
    'appearances': 0,            # Nombre d'apparitions en match
    'goals': 0,                  # Buts marqués
    'assists': 0,                # Passes décisives
    'yellow_cards': 0,           # Cartons jaunes
    'red_cards': 0,              # Cartons rouges
    'minutes_played': 0,         # Minutes jouées
    'injury_status': '',         # Statut de blessure
    'strength_ratings': {},      # Évaluations des forces
    'weakness_ratings': {},      # Évaluations des faiblesses
    'last_updated': None,        # Date de dernière mise à jour
    'data_sources': []           # Sources des données
}

# Structure des données pour les managers (inspirée de sofascore)
MANAGER_DATA_STRUCTURE = {
    'name': '',                  # Nom du manager
    'full_name': '',             # Nom complet
    'nationality': '',           # Nationalité
    'birth_date': None,          # Date de naissance
    'age': None,                 # Âge
    'team': '',                  # Équipe actuelle
    'preferred_formation': '',   # Formation préférée
    'contract_until': '',        # Fin de contrat
    'games_total': 0,            # Nombre total de matchs
    'games_won': 0,              # Matchs gagnés
    'games_drawn': 0,            # Matchs nuls
    'games_lost': 0,             # Matchs perdus
    'points_per_game': 0.0,      # Points par match
    'trophies': [],              # Trophées remportés
    'previous_teams': [],        # Équipes précédentes
    'playing_style': '',         # Style de jeu
    'last_updated': None,        # Date de dernière mise à jour
    'data_sources': []           # Sources des données
}

class PlayerDataEnrichment:
    """
    Classe pour enrichir les données des joueurs et managers en combinant
    différentes sources (Transfermarkt, soccerdata, etc.).
    """
    
    def __init__(self):
        """Initialise le système d'enrichissement de données."""
        self.sources_available = self._check_sources_availability()
        self.cache_expiration = 86400  # 24 heures en secondes
    
    def _check_sources_availability(self):
        """
        Vérifie la disponibilité des différentes sources de données.
        
        Returns:
            dict: Dictionnaire indiquant la disponibilité de chaque source
        """
        sources = {
            'transfermarkt': is_transfermarkt_available(),
            'soccerdata': is_soccerdata_available()
        }
        
        # Vérifier quelles sources soccerdata sont disponibles
        if sources['soccerdata']:
            soccer_data = get_soccer_data_integration()
            available_sources = soccer_data.get_available_sources()
            
            # Ajouter les sources soccerdata disponibles
            for source, available in available_sources.items():
                sources[f'soccerdata_{source}'] = available
        
        return sources
    
    def _load_from_cache(self, cache_type, entity_id):
        """
        Charge des données depuis le cache.
        
        Args:
            cache_type (str): Type de cache ('players' ou 'managers')
            entity_id (str): Identifiant de l'entité
        
        Returns:
            dict: Données en cache ou None si non disponibles
        """
        cache_file = os.path.join(CACHE_DIR, f"{cache_type}_{entity_id}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Vérifier l'expiration du cache
                if 'last_updated' in data:
                    last_updated = datetime.fromisoformat(data['last_updated'])
                    now = datetime.now()
                    
                    if (now - last_updated).total_seconds() < self.cache_expiration:
                        logger.info(f"Données de {cache_type} {entity_id} chargées depuis le cache")
                        return data
            except Exception as e:
                logger.error(f"Erreur lors du chargement du cache pour {cache_type} {entity_id}: {e}")
        
        return None
    
    def _save_to_cache(self, cache_type, entity_id, data):
        """
        Sauvegarde des données dans le cache.
        
        Args:
            cache_type (str): Type de cache ('players' ou 'managers')
            entity_id (str): Identifiant de l'entité
            data (dict): Données à mettre en cache
        """
        cache_file = os.path.join(CACHE_DIR, f"{cache_type}_{entity_id}.json")
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Données de {cache_type} {entity_id} sauvegardées dans le cache")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde du cache pour {cache_type} {entity_id}: {e}")
    
    def _clean_player_name(self, name):
        """
        Nettoie un nom de joueur pour l'identifier de manière cohérente.
        
        Args:
            name (str): Nom du joueur
        
        Returns:
            str: Nom nettoyé
        """
        if not name:
            return ""
        
        # Supprimer les accents, convertir en minuscules, supprimer les caractères spéciaux
        import unicodedata
        cleaned = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
        cleaned = cleaned.lower()
        
        # Supprimer les suffixes/préfixes communs
        prefixes = ['mr. ', 'mr ', 'dr. ', 'dr ']
        for prefix in prefixes:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):]
        
        # Retourner uniquement les caractères alphanumériques et espaces
        return ''.join(c for c in cleaned if c.isalnum() or c.isspace())
    
    def get_detailed_player_data(self, player_name, team_name=None, player_id=None):
        """
        Récupère des données détaillées sur un joueur en combinant plusieurs sources.
        
        Args:
            player_name (str): Nom du joueur
            team_name (str, optional): Nom de l'équipe pour aider à identifier le joueur
            player_id (str, optional): ID du joueur dans Transfermarkt (si connu)
        
        Returns:
            dict: Données détaillées sur le joueur
        """
        # Créer une clé de cache basée sur le nom du joueur (et l'équipe si disponible)
        cache_key = self._clean_player_name(player_name)
        if team_name:
            cache_key += f"_{self._clean_player_name(team_name)}"
        
        # Vérifier le cache
        cached_data = self._load_from_cache('players', cache_key)
        if cached_data:
            return cached_data
        
        # Créer une structure de base pour les données du joueur
        player_data = PLAYER_DATA_STRUCTURE.copy()
        player_data['name'] = player_name
        player_data['team'] = team_name if team_name else ""
        player_data['last_updated'] = datetime.now().isoformat()
        
        # Collecter les données de différentes sources
        sources_used = []
        
        # 1. Données de Transfermarkt (si disponible)
        if self.sources_available['transfermarkt']:
            try:
                # Si l'ID du joueur est fourni, l'utiliser directement
                if player_id:
                    tm_player_data = get_player_profile(player_id)
                    if tm_player_data and 'status' not in tm_player_data:
                        self._enhance_with_transfermarkt_player(player_data, tm_player_data)
                        sources_used.append('transfermarkt')
                # Sinon, rechercher le joueur par nom
                elif team_name:
                    # Rechercher les joueurs de l'équipe
                    from api.transfermarkt_integration import search_club_by_name, get_club_profile, get_team_players
                    
                    club_search = search_club_by_name(team_name)
                    if club_search and 'items' in club_search and club_search['items']:
                        club_id = club_search['items'][0]['id']
                        players = get_team_players(club_id)
                        
                        if players and 'players' in players:
                            # Essayer de trouver le joueur par correspondance de nom
                            clean_player_name = self._clean_player_name(player_name)
                            for tm_player in players['players']:
                                if self._clean_player_name(tm_player.get('name', '')) == clean_player_name:
                                    tm_player_id = tm_player.get('id')
                                    if tm_player_id:
                                        tm_player_data = get_player_profile(tm_player_id)
                                        if tm_player_data and 'status' not in tm_player_data:
                                            self._enhance_with_transfermarkt_player(player_data, tm_player_data)
                                            sources_used.append('transfermarkt')
                                            break
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des données Transfermarkt pour {player_name}: {e}")
        
        # 2. Données de soccerdata (si disponible)
        if self.sources_available['soccerdata']:
            try:
                soccer_data = get_soccer_data_integration()
                
                # Essayer d'abord avec FBref (statistiques détaillées)
                if self.sources_available.get('soccerdata_fbref', False):
                    player_stats = soccer_data.get_player_detailed_stats(
                        player_name=player_name,
                        team_name=team_name,
                        source='fbref'
                    )
                    
                    if not player_stats.empty:
                        self._enhance_with_fbref_player(player_data, player_stats)
                        sources_used.append('soccerdata_fbref')
                
                # Essayer ensuite avec SoFIFA (attributs détaillés)
                if self.sources_available.get('soccerdata_sofifa', False):
                    player_stats = soccer_data.get_player_detailed_stats(
                        player_name=player_name,
                        team_name=team_name,
                        source='sofifa'
                    )
                    
                    if not player_stats.empty:
                        self._enhance_with_sofifa_player(player_data, player_stats)
                        sources_used.append('soccerdata_sofifa')
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des données soccerdata pour {player_name}: {e}")
        
        # Enregistrer les sources utilisées
        player_data['data_sources'] = sources_used
        
        # Sauvegarder dans le cache
        self._save_to_cache('players', cache_key, player_data)
        
        return player_data
    
    def _enhance_with_transfermarkt_player(self, player_data, tm_player_data):
        """
        Enrichit les données d'un joueur avec des informations de Transfermarkt.
        
        Args:
            player_data (dict): Données du joueur à enrichir
            tm_player_data (dict): Données du joueur depuis Transfermarkt
        """
        try:
            # Mettre à jour les informations de base
            player_data['full_name'] = tm_player_data.get('name', player_data['name'])
            player_data['nationality'] = tm_player_data.get('citizenship', {}).get('name', player_data['nationality'])
            
            # Date de naissance et âge
            if 'dateOfBirth' in tm_player_data:
                player_data['birth_date'] = tm_player_data['dateOfBirth']
                # Calcul de l'âge si la date de naissance est disponible
                try:
                    birth_date = datetime.strptime(tm_player_data['dateOfBirth'], '%Y-%m-%d')
                    today = datetime.now()
                    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                    player_data['age'] = age
                except Exception:
                    pass
            
            # Caractéristiques physiques
            player_data['height'] = tm_player_data.get('height', player_data['height'])
            
            # Position
            if 'positions' in tm_player_data and tm_player_data['positions']:
                main_position = tm_player_data['positions'][0] if tm_player_data['positions'] else {}
                player_data['position'] = main_position.get('name', player_data['position'])
                
                # Position secondaire
                if len(tm_player_data['positions']) > 1:
                    player_data['secondary_position'] = tm_player_data['positions'][1].get('name', '')
            
            # Valeur marchande
            if 'marketValue' in tm_player_data:
                player_data['market_value'] = tm_player_data['marketValue'].get('value', player_data['market_value'])
            
            # Équipe actuelle
            if 'club' in tm_player_data and tm_player_data['club']:
                player_data['team'] = tm_player_data['club'].get('name', player_data['team'])
            
            # Numéro de maillot
            player_data['shirt_number'] = tm_player_data.get('shirtNumber', player_data['shirt_number'])
            
            # Pied préféré
            player_data['preferred_foot'] = tm_player_data.get('foot', player_data['preferred_foot'])
            
            # Contrat
            if 'contract' in tm_player_data and tm_player_data['contract']:
                player_data['contract_until'] = tm_player_data['contract'].get('until', player_data['contract_until'])
            
            # Statistiques si disponibles
            if 'statistics' in tm_player_data and tm_player_data['statistics']:
                for stat in tm_player_data['statistics']:
                    if 'appearances' in stat:
                        player_data['appearances'] += stat.get('appearances', 0)
                    if 'goals' in stat:
                        player_data['goals'] += stat.get('goals', 0)
                    if 'assists' in stat:
                        player_data['assists'] += stat.get('assists', 0)
                    if 'minutesPlayed' in stat:
                        player_data['minutes_played'] += stat.get('minutesPlayed', 0)
            
            # Statut de blessure
            if 'injuryHistory' in tm_player_data and tm_player_data['injuryHistory']:
                latest_injury = tm_player_data['injuryHistory'][0] if tm_player_data['injuryHistory'] else {}
                if latest_injury.get('until') == 'Unknown' or (
                    'until' in latest_injury and
                    datetime.strptime(latest_injury['until'], '%Y-%m-%d') > datetime.now()
                ):
                    player_data['injury_status'] = latest_injury.get('injury', 'Blessé')
        
        except Exception as e:
            logger.error(f"Erreur lors de l'enrichissement avec les données Transfermarkt: {e}")
    
    def _enhance_with_fbref_player(self, player_data, fbref_player_stats):
        """
        Enrichit les données d'un joueur avec des informations de FBref.
        
        Args:
            player_data (dict): Données du joueur à enrichir
            fbref_player_stats (pd.DataFrame): Statistiques du joueur depuis FBref
        """
        try:
            # Convertir DataFrame en dictionnaire pour faciliter l'accès
            stats = fbref_player_stats.iloc[0].to_dict() if not fbref_player_stats.empty else {}
            
            # Mettre à jour les informations de base
            if 'player' in stats:
                player_data['name'] = stats['player']
            
            if 'nationality' in stats:
                player_data['nationality'] = stats['nationality']
            
            if 'age' in stats:
                player_data['age'] = stats['age']
            
            if 'position' in stats:
                player_data['position'] = stats['position']
            
            if 'team' in stats:
                player_data['team'] = stats['team']
            
            # Statistiques
            if 'games' in stats:
                player_data['appearances'] = stats['games']
            
            if 'goals' in stats:
                player_data['goals'] = stats['goals']
            
            if 'assists' in stats:
                player_data['assists'] = stats['assists']
            
            if 'minutes' in stats:
                player_data['minutes_played'] = stats['minutes']
            
            if 'cards_yellow' in stats:
                player_data['yellow_cards'] = stats['cards_yellow']
            
            if 'cards_red' in stats:
                player_data['red_cards'] = stats['cards_red']
            
            # Statistiques avancées pour les forces et faiblesses
            strength_ratings = {}
            weakness_ratings = {}
            
            # Exemples de statistiques qui peuvent indiquer des forces
            strength_keys = ['goals_per90', 'assists_per90', 'goals_assists_per90', 'xg_per90', 'npxg_per90',
                            'xa_per90', 'passes_completed', 'passes_pct', 'progressive_passes',
                            'progressive_carries', 'dribbles_completed', 'dribbles_completed_pct',
                            'tackles', 'interceptions', 'blocks', 'clearances', 'aerials_won',
                            'aerials_won_pct', 'save_pct', 'clean_sheets']
            
            for key in strength_keys:
                if key in stats and stats[key] is not None:
                    # Normaliser la valeur entre 0 et 1 (simplifié)
                    value = float(stats[key])
                    if value > 0:
                        strength_ratings[key] = value
            
            player_data['strength_ratings'] = strength_ratings
            player_data['weakness_ratings'] = weakness_ratings
        
        except Exception as e:
            logger.error(f"Erreur lors de l'enrichissement avec les données FBref: {e}")
    
    def _enhance_with_sofifa_player(self, player_data, sofifa_player_stats):
        """
        Enrichit les données d'un joueur avec des informations de SoFIFA.
        
        Args:
            player_data (dict): Données du joueur à enrichir
            sofifa_player_stats (pd.DataFrame): Statistiques du joueur depuis SoFIFA
        """
        try:
            # Convertir DataFrame en dictionnaire pour faciliter l'accès
            stats = sofifa_player_stats.iloc[0].to_dict() if not sofifa_player_stats.empty else {}
            
            # Mettre à jour les informations de base
            if 'name' in stats:
                player_data['name'] = stats['name']
            
            if 'nationality' in stats:
                player_data['nationality'] = stats['nationality']
            
            if 'age' in stats:
                player_data['age'] = stats['age']
            
            if 'height' in stats:
                player_data['height'] = stats['height']
            
            if 'weight' in stats:
                player_data['weight'] = stats['weight']
            
            if 'position' in stats:
                player_data['position'] = stats['position']
            
            if 'foot' in stats:
                player_data['preferred_foot'] = stats['foot']
            
            # Ratings détaillés pour forces et faiblesses
            strength_ratings = {}
            weakness_ratings = {}
            
            # SoFIFA a des ratings détaillés
            rating_keys = ['overall', 'potential', 'pace', 'shooting', 'passing',
                          'dribbling', 'defending', 'physic', 'skill_moves',
                          'weak_foot', 'attacking_crossing', 'attacking_finishing',
                          'attacking_heading_accuracy', 'attacking_short_passing',
                          'attacking_volleys', 'skill_dribbling', 'skill_curve',
                          'skill_fk_accuracy', 'skill_long_passing', 'skill_ball_control',
                          'movement_acceleration', 'movement_sprint_speed',
                          'movement_agility', 'movement_reactions', 'movement_balance',
                          'power_shot_power', 'power_jumping', 'power_stamina',
                          'power_strength', 'power_long_shots', 'mentality_aggression',
                          'mentality_interceptions', 'mentality_positioning',
                          'mentality_vision', 'mentality_penalties', 'mentality_composure',
                          'defending_marking', 'defending_standing_tackle',
                          'defending_sliding_tackle', 'goalkeeping_diving',
                          'goalkeeping_handling', 'goalkeeping_kicking',
                          'goalkeeping_positioning', 'goalkeeping_reflexes']
            
            for key in rating_keys:
                if key in stats and stats[key] is not None:
                    try:
                        value = float(stats[key])
                        if value >= 75:  # Considéré comme une force si >= 75
                            strength_ratings[key] = value
                        elif value <= 65:  # Considéré comme une faiblesse si <= 65
                            weakness_ratings[key] = value
                    except (ValueError, TypeError):
                        pass
            
            player_data['strength_ratings'] = strength_ratings
            player_data['weakness_ratings'] = weakness_ratings
            
            # Valeur marchande
            if 'value' in stats:
                player_data['market_value'] = stats['value']
            
            # Équipe
            if 'team' in stats:
                player_data['team'] = stats['team']
        
        except Exception as e:
            logger.error(f"Erreur lors de l'enrichissement avec les données SoFIFA: {e}")
    
    def get_detailed_manager_data(self, manager_name, team_name=None):
        """
        Récupère des données détaillées sur un manager en combinant plusieurs sources.
        
        Args:
            manager_name (str): Nom du manager
            team_name (str, optional): Nom de l'équipe pour aider à identifier le manager
        
        Returns:
            dict: Données détaillées sur le manager
        """
        # Créer une clé de cache basée sur le nom du manager (et l'équipe si disponible)
        cache_key = self._clean_player_name(manager_name)
        if team_name:
            cache_key += f"_{self._clean_player_name(team_name)}"
        
        # Vérifier le cache
        cached_data = self._load_from_cache('managers', cache_key)
        if cached_data:
            return cached_data
        
        # Créer une structure de base pour les données du manager
        manager_data = MANAGER_DATA_STRUCTURE.copy()
        manager_data['name'] = manager_name
        manager_data['team'] = team_name if team_name else ""
        manager_data['last_updated'] = datetime.now().isoformat()
        
        # Collecter les données de différentes sources
        sources_used = []
        
        # 1. Données de Transfermarkt (si disponible)
        if self.sources_available['transfermarkt'] and team_name:
            try:
                from api.transfermarkt_integration import search_club_by_name, get_club_profile
                
                club_search = search_club_by_name(team_name)
                if club_search and 'items' in club_search and club_search['items']:
                    club_id = club_search['items'][0]['id']
                    club_data = get_club_profile(club_id)
                    
                    if club_data and 'staff' in club_data:
                        # Rechercher le manager dans le staff
                        for staff_member in club_data['staff']:
                            if staff_member.get('role', '').lower() in ['manager', 'head coach', 'coach', 'entraîneur', 'entraîneur principal']:
                                if self._clean_player_name(staff_member.get('name', '')) == self._clean_player_name(manager_name):
                                    self._enhance_with_transfermarkt_manager(manager_data, staff_member, club_data)
                                    sources_used.append('transfermarkt')
                                    break
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des données Transfermarkt pour le manager {manager_name}: {e}")
        
        # 2. Données de soccerdata (si disponible, certaines sources comme WhoScored ont des infos sur les managers)
        if self.sources_available['soccerdata'] and self.sources_available.get('soccerdata_sofascore', False) and team_name:
            try:
                soccer_data = get_soccer_data_integration()
                
                # Récupérer les données du match pour trouver des informations sur le manager
                # (pas directement disponible, mais peut être extraite des rapports de match)
                # Cette fonctionnalité dépend des capacités exactes de soccerdata pour chaque source
                pass
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des données soccerdata pour le manager {manager_name}: {e}")
        
        # Enregistrer les sources utilisées
        manager_data['data_sources'] = sources_used
        
        # Sauvegarder dans le cache
        self._save_to_cache('managers', cache_key, manager_data)
        
        return manager_data
    
    def _enhance_with_transfermarkt_manager(self, manager_data, tm_manager_data, club_data):
        """
        Enrichit les données d'un manager avec des informations de Transfermarkt.
        
        Args:
            manager_data (dict): Données du manager à enrichir
            tm_manager_data (dict): Données du manager depuis Transfermarkt
            club_data (dict): Données du club depuis Transfermarkt
        """
        try:
            # Mettre à jour les informations de base
            manager_data['full_name'] = tm_manager_data.get('name', manager_data['name'])
            manager_data['nationality'] = tm_manager_data.get('citizenship', {}).get('name', manager_data['nationality'])
            
            # Date de naissance et âge
            if 'dateOfBirth' in tm_manager_data:
                manager_data['birth_date'] = tm_manager_data['dateOfBirth']
                # Calcul de l'âge si la date de naissance est disponible
                try:
                    birth_date = datetime.strptime(tm_manager_data['dateOfBirth'], '%Y-%m-%d')
                    today = datetime.now()
                    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                    manager_data['age'] = age
                except Exception:
                    pass
            
            # Équipe actuelle
            if 'club' in club_data:
                manager_data['team'] = club_data['name']
            
            # Formation préférée (pas toujours disponible dans l'API Transfermarkt)
            
            # Informations sur le contrat (si disponibles)
            if 'contract' in tm_manager_data:
                manager_data['contract_until'] = tm_manager_data.get('contract', {}).get('until', manager_data['contract_until'])
            
            # Historique (équipes précédentes)
            if 'managerStations' in tm_manager_data:
                previous_teams = []
                for station in tm_manager_data.get('managerStations', []):
                    if 'club' in station and station['club'].get('name') != manager_data['team']:
                        previous_teams.append({
                            'team': station['club'].get('name', ''),
                            'from': station.get('from', ''),
                            'until': station.get('until', '')
                        })
                manager_data['previous_teams'] = previous_teams
            
            # Palmarès (trophées)
            if 'trophies' in tm_manager_data:
                trophies = []
                for trophy in tm_manager_data.get('trophies', []):
                    trophies.append({
                        'name': trophy.get('name', ''),
                        'season': trophy.get('season', ''),
                        'club': trophy.get('club', {}).get('name', '')
                    })
                manager_data['trophies'] = trophies
        
        except Exception as e:
            logger.error(f"Erreur lors de l'enrichissement avec les données Transfermarkt pour le manager: {e}")

# Créer une instance singleton pour l'accès global
_player_data_enrichment = None

def get_player_data_enrichment():
    """
    Récupère l'instance singleton d'enrichissement de données joueur.
    
    Returns:
        PlayerDataEnrichment: Instance d'enrichissement de données joueur
    """
    global _player_data_enrichment
    
    if _player_data_enrichment is None:
        logger.info("Initialisation de l'enrichissement de données joueur global")
        _player_data_enrichment = PlayerDataEnrichment()
        
    return _player_data_enrichment

def get_detailed_player_data(player_name, team_name=None, player_id=None):
    """
    Récupère des données détaillées sur un joueur.
    
    Args:
        player_name (str): Nom du joueur
        team_name (str, optional): Nom de l'équipe pour aider à identifier le joueur
        player_id (str, optional): ID du joueur dans Transfermarkt (si connu)
    
    Returns:
        dict: Données détaillées sur le joueur
    """
    enrichment = get_player_data_enrichment()
    return enrichment.get_detailed_player_data(player_name, team_name, player_id)

def get_detailed_manager_data(manager_name, team_name=None):
    """
    Récupère des données détaillées sur un manager.
    
    Args:
        manager_name (str): Nom du manager
        team_name (str, optional): Nom de l'équipe pour aider à identifier le manager
    
    Returns:
        dict: Données détaillées sur le manager
    """
    enrichment = get_player_data_enrichment()
    return enrichment.get_detailed_manager_data(manager_name, team_name)

def enrich_team_with_player_data(team_data):
    """
    Enrichit les données d'une équipe avec des informations détaillées sur ses joueurs.
    
    Args:
        team_data (dict): Données de l'équipe à enrichir
    
    Returns:
        dict: Données de l'équipe enrichies
    """
    enrichment = get_player_data_enrichment()
    
    # Créer une copie des données pour éviter de modifier l'original
    enriched_data = team_data.copy()
    
    # Récupérer le nom de l'équipe
    team_name = enriched_data.get('team_name') or enriched_data.get('name')
    
    if not team_name:
        logger.warning("Nom d'équipe non disponible pour l'enrichissement des données")
        return enriched_data
    
    # Si des joueurs sont déjà présents dans les données
    players = []
    
    # Essayer de récupérer les joueurs de l'équipe depuis Transfermarkt
    if 'transfermarkt_data' in enriched_data:
        tm_team_id = enriched_data['transfermarkt_data'].get('id')
        if tm_team_id:
            try:
                from api.transfermarkt_integration import get_team_players
                team_players = get_team_players(tm_team_id)
                
                if team_players and 'players' in team_players:
                    for tm_player in team_players['players']:
                        player_name = tm_player.get('name')
                        player_id = tm_player.get('id')
                        
                        if player_name and player_id:
                            # Récupérer des données détaillées sur le joueur
                            detailed_player = enrichment.get_detailed_player_data(
                                player_name=player_name,
                                team_name=team_name,
                                player_id=player_id
                            )
                            
                            players.append(detailed_player)
            except Exception as e:
                logger.error(f"Erreur lors de l'enrichissement de l'équipe {team_name} avec des données de joueur: {e}")
    
    # Si aucun joueur n'a été trouvé via Transfermarkt, essayer avec soccerdata
    if not players and enrichment.sources_available['soccerdata']:
        try:
            soccer_data = get_soccer_data_integration()
            
            # Essayer différentes sources
            for source in ['fbref', 'sofifa', 'sofascore']:
                if enrichment.sources_available.get(f'soccerdata_{source}', False):
                    team_players = soccer_data.get_team_players(
                        team_name=team_name,
                        source=source
                    )
                    
                    if not team_players.empty:
                        for _, player_row in team_players.iterrows():
                            player_name = player_row.get('player_name')
                            
                            if player_name:
                                # Récupérer des données détaillées sur le joueur
                                detailed_player = enrichment.get_detailed_player_data(
                                    player_name=player_name,
                                    team_name=team_name
                                )
                                
                                players.append(detailed_player)
                        
                        # Si des joueurs ont été trouvés, sortir de la boucle
                        if players:
                            break
        except Exception as e:
            logger.error(f"Erreur lors de l'enrichissement de l'équipe {team_name} avec des données de joueur via soccerdata: {e}")
    
    if players:
        enriched_data['detailed_players'] = players
    
    # Essayer de récupérer des informations sur le manager
    try:
        # Le manager pourrait être trouvé dans les données Transfermarkt
        manager_name = None
        
        if 'transfermarkt_data' in enriched_data and 'staff' in enriched_data['transfermarkt_data']:
            for staff_member in enriched_data['transfermarkt_data']['staff']:
                if staff_member.get('role', '').lower() in ['manager', 'head coach', 'coach', 'entraîneur', 'entraîneur principal']:
                    manager_name = staff_member.get('name')
                    break
        
        if manager_name:
            # Récupérer des données détaillées sur le manager
            detailed_manager = enrichment.get_detailed_manager_data(
                manager_name=manager_name,
                team_name=team_name
            )
            
            enriched_data['detailed_manager'] = detailed_manager
    except Exception as e:
        logger.error(f"Erreur lors de l'enrichissement de l'équipe {team_name} avec des données de manager: {e}")
    
    return enriched_data