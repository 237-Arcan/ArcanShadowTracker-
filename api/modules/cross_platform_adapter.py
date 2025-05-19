"""
Module d'adaptation cross-platform pour ArcanShadow.
Facilite la transition vers une application mobile en préparant les données
pour différents formats d'affichage et en optimisant les flux de données.
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Union, Optional

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrossPlatformAdapter:
    """
    Adapter pour faciliter la transition des données entre l'application web et mobile.
    Prépare les données pour être consommées de manière optimisée sur différentes plateformes.
    """
    
    def __init__(self, data_hub=None):
        """
        Initialise l'adaptateur cross-platform
        
        Args:
            data_hub: Instance du hub d'intégration central (optionnel)
        """
        self.data_hub = data_hub
        self.platform_settings = {
            "web": {
                "image_quality": "high",
                "data_freshness": 300,  # 5 minutes
                "batch_size": 20
            },
            "mobile": {
                "image_quality": "medium",
                "data_freshness": 600,  # 10 minutes
                "batch_size": 10
            },
            "watch": {
                "image_quality": "low",
                "data_freshness": 900,  # 15 minutes
                "batch_size": 5
            }
        }
        logger.info("Adaptateur cross-platform initialisé")
        
    def optimize_data_for_platform(self, data: Union[Dict, List], platform: str = "web") -> Union[Dict, List]:
        """
        Optimise les données pour une plateforme spécifique
        
        Args:
            data: Données à optimiser (dict ou liste)
            platform: Plateforme cible ('web', 'mobile', 'watch')
            
        Returns:
            Données optimisées pour la plateforme
        """
        if platform not in self.platform_settings:
            logger.warning(f"Plateforme inconnue: {platform}, utilisation des paramètres web par défaut")
            platform = "web"
            
        settings = self.platform_settings[platform]
        
        if isinstance(data, list):
            # Limiter le nombre d'éléments selon la plateforme
            max_items = settings["batch_size"]
            optimized_data = data[:max_items]
            
            # Optimiser chaque élément
            for i, item in enumerate(optimized_data):
                if isinstance(item, dict):
                    optimized_data[i] = self._optimize_item(item, platform)
                    
            return optimized_data
        
        elif isinstance(data, dict):
            return self._optimize_item(data, platform)
        
        else:
            logger.warning(f"Type de données non pris en charge: {type(data)}")
            return data
    
    def _optimize_item(self, item: Dict, platform: str) -> Dict:
        """
        Optimise un élément de données pour une plateforme
        
        Args:
            item: Élément à optimiser
            platform: Plateforme cible
            
        Returns:
            Élément optimisé
        """
        settings = self.platform_settings[platform]
        optimized = {}
        
        # Copier les données essentielles
        essential_fields = ["id", "date", "home_team", "away_team", "league_id", "league_name"]
        for field in essential_fields:
            if field in item:
                optimized[field] = item[field]
        
        # Optimiser les images selon la qualité définie pour la plateforme
        if "images" in item:
            image_quality = settings["image_quality"]
            if isinstance(item["images"], dict) and image_quality in item["images"]:
                optimized["images"] = {image_quality: item["images"][image_quality]}
            else:
                optimized["images"] = item["images"]
                
        # Ajouter un champ indiquant si les données sont complètes ou optimisées
        optimized["optimized_for"] = platform
        
        # Transférer les autres champs importants
        for key, value in item.items():
            if key not in optimized and key not in ["detailed_stats", "full_history"]:
                optimized[key] = value
                
        return optimized
    
    def prepare_matches_for_app(self, matches: List[Dict], platform: str = "mobile") -> List[Dict]:
        """
        Prépare les matchs pour l'application mobile en optimisant et en ajoutant 
        des métadonnées pour le rendu sur l'application
        
        Args:
            matches: Liste des matchs à préparer
            platform: Plateforme cible
            
        Returns:
            Liste des matchs préparés pour l'application
        """
        if not matches:
            return []
            
        # Optimiser les données selon la plateforme
        optimized_matches = self.optimize_data_for_platform(matches, platform)
        
        # Enrichir avec des métadonnées pour l'application
        for match in optimized_matches:
            # Ajouter un ID unique pour le tracking dans l'app
            if "id" not in match:
                match["id"] = f"match_{hash(str(match.get('home_team', '')) + str(match.get('away_team', '')))}"
                
            # Ajouter des informations de navigation pour l'app
            match["app_navigation"] = {
                "detail_route": f"/match/{match['id']}",
                "share_url": f"arcanapp://match/{match['id']}"
            }
            
            # Utiliser le module de temps du hub si disponible
            if self.data_hub and hasattr(self.data_hub, 'time_module') and self.data_hub.time_module:
                try:
                    # Ajouter des métadonnées temporelles pour l'app
                    match_time = self.data_hub.format_match_time(match.get('date'))
                    match_date = self.data_hub.format_match_date(match.get('date'), "compact")
                    
                    match["app_display"] = {
                        "time": match_time,
                        "date": match_date,
                        "countdown": self.data_hub.time_module.format_countdown(match.get('date')),
                        "is_today": datetime.fromisoformat(match.get('date').replace('Z', '+00:00')).date() == datetime.now().date()
                    }
                except Exception as e:
                    logger.error(f"Erreur lors de l'enrichissement temporel: {e}")
            
            # Ajouter des métadonnées visuelles pour l'interface
            if "league_id" in match:
                match["app_ui"] = {
                    "league_color": self._get_league_color(match["league_id"]),
                    "priority": self._calculate_match_priority(match)
                }
        
        return optimized_matches
    
    def _get_league_color(self, league_id: Union[int, str]) -> str:
        """
        Renvoie une couleur associée à la ligue pour l'interface
        
        Args:
            league_id: ID de la ligue
            
        Returns:
            Code couleur hexadécimal
        """
        league_colors = {
            39: "#3d185c",  # Premier League
            140: "#162b4e",  # La Liga
            61: "#001e50",  # Ligue 1
            78: "#cd122d",  # Bundesliga
            135: "#213e7c",  # Serie A
            2: "#14418b",   # Champions League
        }
        
        return league_colors.get(int(league_id) if isinstance(league_id, str) else league_id, "#2d2d44")
    
    def _calculate_match_priority(self, match: Dict) -> int:
        """
        Calcule la priorité d'affichage d'un match pour l'application
        
        Args:
            match: Données du match
            
        Returns:
            Score de priorité (0-100)
        """
        priority = 50  # Priorité par défaut
        
        # Facteurs augmentant la priorité
        major_leagues = [39, 140, 61, 78, 135, 2]
        if match.get('league_id') in major_leagues:
            priority += 20
            
        if match.get('is_derby', False):
            priority += 15
            
        if match.get('is_hot_match', False):
            priority += 10
            
        if match.get('is_value_bet', False):
            priority += 5
            
        # Facteurs réduisant la priorité
        if match.get('is_trap_match', False):
            priority -= 5
            
        # Normaliser entre 0 et 100
        return max(0, min(100, priority))
    
    def generate_app_configuration(self, platform: str = "mobile") -> Dict:
        """
        Génère une configuration pour l'application mobile
        
        Args:
            platform: Plateforme cible
            
        Returns:
            Configuration pour l'application
        """
        config = {
            "platform": platform,
            "version": "1.0.0",
            "api_endpoints": {
                "matches": "/api/matches",
                "predictions": "/api/predictions",
                "user": "/api/user"
            },
            "features": {
                "real_time_notifications": True,
                "dark_mode": True,
                "offline_mode": True,
                "language": "auto"
            },
            "display": {
                "theme": "dark",
                "accent_color": "#7038FF",
                "font_size": "medium"
            },
            "data": {
                "refresh_interval": 300,  # 5 minutes
                "cache_duration": 3600,   # 1 heure
                "max_offline_days": 2
            }
        }
        
        # Personnaliser selon la plateforme
        if platform == "mobile":
            config["features"]["haptic_feedback"] = True
            config["display"]["navigation"] = "bottom_tabs"
        elif platform == "web":
            config["features"]["haptic_feedback"] = False
            config["display"]["navigation"] = "sidebar"
        elif platform == "watch":
            config["features"]["offline_mode"] = False
            config["data"]["refresh_interval"] = 900  # 15 minutes
            config["display"]["font_size"] = "large"
            
        return config
        
    def export_data_for_app(self, data: Dict, format: str = "json") -> str:
        """
        Exporte les données dans un format adapté pour l'application
        
        Args:
            data: Données à exporter
            format: Format d'exportation ('json' ou 'compact')
            
        Returns:
            Données exportées au format demandé
        """
        if format == "json":
            return json.dumps(data)
        elif format == "compact":
            # Version compacte pour minimiser la taille
            return json.dumps(data, separators=(',', ':'))
        else:
            logger.warning(f"Format inconnu: {format}, utilisation de JSON par défaut")
            return json.dumps(data)