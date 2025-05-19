"""
Module d'intégration des composants améliorés d'ArcanShadow.
Ce module centralise l'accès à tous les composants enrichis avec les nouvelles sources de données
et facilite leur intégration dans l'application principale.
"""

import logging
import importlib

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedComponents:
    """
    Classe d'intégration des composants améliorés d'ArcanShadow.
    Centralise la détection, l'initialisation et l'accès aux composants enrichis.
    """
    
    def __init__(self):
        """Initialise et détecte les composants améliorés disponibles"""
        # Dictionnaire des composants disponibles
        self.available_components = {}
        
        # Liste des composants à vérifier
        components_to_check = [
            {
                'name': 'predictions_tab',
                'module': 'predictions_tab_enhanced',
                'class': None,
                'function': 'display_enhanced_predictions_tab',
                'fallback_module': 'predictions_tab',
                'fallback_function': 'display_predictions_tab'
            },
            {
                'name': 'bet_trap_map',
                'module': 'modules.bet_trap_map_enhanced',
                'class': 'BetTrapMapEnhanced',
                'fallback_module': 'modules.bet_trap_map',
                'fallback_class': 'BetTrapMap'
            },
            {
                'name': 'shadow_odds_plus',
                'module': 'modules.shadow_odds_plus_enhanced',
                'class': 'ShadowOddsPlusEnhanced',
                'fallback_module': 'modules.shadow_odds_plus',
                'fallback_class': 'ShadowOddsPlus'
            },
            {
                'name': 'fan_sentiment_monitor',
                'module': 'modules.fan_sentiment_monitor_enhanced',
                'class': 'FanSentimentMonitorEnhanced',
                'fallback_module': 'modules.fan_sentiment_monitor',
                'fallback_class': 'FanSentimentMonitor'
            }
        ]
        
        # Vérifier chaque composant
        for component in components_to_check:
            self._check_component(component)
        
        logger.info(f"Composants améliorés disponibles: {list(self.available_components.keys())}")
    
    def _check_component(self, component_info):
        """
        Vérifie si un composant amélioré est disponible.
        
        Args:
            component_info (dict): Informations sur le composant à vérifier
        """
        name = component_info['name']
        module_name = component_info['module']
        class_name = component_info['class']
        function_name = component_info.get('function')
        
        try:
            # Essayer d'importer le module
            module = importlib.import_module(module_name)
            
            # Si le composant est une classe
            if class_name:
                component_class = getattr(module, class_name)
                # Instancier la classe
                component_instance = component_class()
                # Stocker l'instance
                self.available_components[name] = {
                    'type': 'class',
                    'instance': component_instance,
                    'module': module,
                    'enhanced': True
                }
                logger.info(f"Composant amélioré '{name}' (classe {class_name}) disponible")
            
            # Si le composant est une fonction
            elif function_name:
                component_function = getattr(module, function_name)
                # Stocker la fonction
                self.available_components[name] = {
                    'type': 'function',
                    'function': component_function,
                    'module': module,
                    'enhanced': True
                }
                logger.info(f"Composant amélioré '{name}' (fonction {function_name}) disponible")
        
        except (ImportError, AttributeError) as e:
            logger.warning(f"Composant amélioré '{name}' non disponible: {e}")
            
            # Essayer d'importer le composant de repli
            try:
                fallback_module_name = component_info['fallback_module']
                fallback_module = importlib.import_module(fallback_module_name)
                
                # Si le composant de repli est une classe
                if 'fallback_class' in component_info:
                    fallback_class_name = component_info['fallback_class']
                    fallback_class = getattr(fallback_module, fallback_class_name)
                    # Instancier la classe
                    fallback_instance = fallback_class()
                    # Stocker l'instance
                    self.available_components[name] = {
                        'type': 'class',
                        'instance': fallback_instance,
                        'module': fallback_module,
                        'enhanced': False
                    }
                    logger.info(f"Composant standard '{name}' (classe {fallback_class_name}) utilisé en repli")
                
                # Si le composant de repli est une fonction
                elif 'fallback_function' in component_info:
                    fallback_function_name = component_info['fallback_function']
                    fallback_function = getattr(fallback_module, fallback_function_name)
                    # Stocker la fonction
                    self.available_components[name] = {
                        'type': 'function',
                        'function': fallback_function,
                        'module': fallback_module,
                        'enhanced': False
                    }
                    logger.info(f"Composant standard '{name}' (fonction {fallback_function_name}) utilisé en repli")
            
            except (ImportError, AttributeError) as e2:
                logger.error(f"Composant de repli '{name}' également non disponible: {e2}")
    
    def get_component(self, name):
        """
        Récupère un composant par son nom.
        
        Args:
            name (str): Nom du composant
            
        Returns:
            object: Classe ou fonction du composant, ou None si non disponible
        """
        if name not in self.available_components:
            logger.warning(f"Composant '{name}' non disponible")
            return None
        
        component = self.available_components[name]
        
        if component['type'] == 'class':
            return component['instance']
        elif component['type'] == 'function':
            return component['function']
        
        return None
    
    def is_enhanced(self, name):
        """
        Vérifie si un composant est la version améliorée.
        
        Args:
            name (str): Nom du composant
            
        Returns:
            bool: True si c'est la version améliorée, False sinon
        """
        if name not in self.available_components:
            return False
        
        return self.available_components[name]['enhanced']
    
    def get_display_predictions_tab(self):
        """
        Récupère la fonction d'affichage de l'onglet Prédictions.
        
        Returns:
            function: Fonction d'affichage de l'onglet Prédictions
        """
        return self.get_component('predictions_tab')
    
    def get_bet_trap_map(self):
        """
        Récupère l'instance de BetTrapMap.
        
        Returns:
            BetTrapMap: Instance de BetTrapMap ou BetTrapMapEnhanced
        """
        return self.get_component('bet_trap_map')
    
    def get_shadow_odds_plus(self):
        """
        Récupère l'instance de ShadowOddsPlus.
        
        Returns:
            ShadowOddsPlus: Instance de ShadowOddsPlus ou ShadowOddsPlusEnhanced
        """
        return self.get_component('shadow_odds_plus')
    
    def get_fan_sentiment_monitor(self):
        """
        Récupère l'instance de FanSentimentMonitor.
        
        Returns:
            FanSentimentMonitor: Instance de FanSentimentMonitor ou FanSentimentMonitorEnhanced
        """
        return self.get_component('fan_sentiment_monitor')
    
    def get_available_components_summary(self):
        """
        Récupère un résumé des composants disponibles.
        
        Returns:
            dict: Résumé des composants disponibles
        """
        summary = {}
        
        for name, component in self.available_components.items():
            summary[name] = {
                'enhanced': component['enhanced'],
                'type': component['type']
            }
        
        return summary

# Instance globale des composants améliorés
_enhanced_components = None

def get_enhanced_components():
    """
    Récupère l'instance globale des composants améliorés.
    
    Returns:
        EnhancedComponents: Instance des composants améliorés
    """
    global _enhanced_components
    
    if _enhanced_components is None:
        _enhanced_components = EnhancedComponents()
    
    return _enhanced_components