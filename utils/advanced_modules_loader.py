"""
Module de chargement des fonctionnalités avancées d'ArcanShadow.
Ce module initialise l'intégration de GematriaOracle et PredictiveForge dans ArcanShadow.
"""
import logging
import os
import importlib
import sys

# Configurer le logging
logger = logging.getLogger("AdvancedModulesLoader")
logger.setLevel(logging.INFO)

# Vérifier si le répertoire de logs existe
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configurer le gestionnaire de fichiers
file_handler = logging.FileHandler("logs/advanced_modules_loader.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Configurer le gestionnaire de console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logger.addHandler(console_handler)

def load_advanced_modules(arcan_brain=None, numeri_code=None, score_matrix=None, meta_systems=None):
    """
    Charge et initialise les modules avancés d'ArcanShadow.
    
    Args:
        arcan_brain: Instance d'ArcanBrain pour l'intégration (optionnel)
        numeri_code: Instance de NumeriCode pour l'intégration (optionnel)
        score_matrix: Sous-module ScoreMatrix pour l'intégration (optionnel)
        meta_systems: Instance de MetaSystems pour l'intégration des événements (optionnel)
        
    Returns:
        dict: Instances des modules chargés, None en cas d'erreur
    """
    logger.info("Chargement des modules avancés")
    
    # Vérifier si le module d'intégration avancée est disponible
    try:
        # Importer le module d'intégration avancée
        advanced_integration = importlib.import_module("modules.advanced_integration")
        logger.info("Module d'intégration avancée importé avec succès")
    except ImportError as e:
        logger.error(f"Erreur lors de l'importation du module d'intégration avancée: {e}")
        return None
    
    try:
        # Initialiser l'intégration
        modules = advanced_integration.initialize_integration(meta_systems)
        logger.info(f"Modules initialisés: {', '.join(modules.keys())}")
        
        # Intégrer avec ArcanBrain si disponible
        if arcan_brain and "IntegrationHub" in modules:
            success = advanced_integration.integrate_with_arcan_brain(arcan_brain, modules)
            if success:
                logger.info("Intégration avec ArcanBrain réussie")
            else:
                logger.warning("Échec de l'intégration avec ArcanBrain")
        
        # Intégrer avec NumeriCode si disponible
        if numeri_code and "GematriaOracle" in modules:
            success = advanced_integration.integrate_with_numeri_code(numeri_code, modules)
            if success:
                logger.info("Intégration avec NumeriCode réussie")
            else:
                logger.warning("Échec de l'intégration avec NumeriCode")
        
        # Intégrer avec ScoreMatrix si disponible
        if score_matrix and "PredictiveForge" in modules:
            success = advanced_integration.integrate_with_score_matrix(score_matrix, modules)
            if success:
                logger.info("Intégration avec ScoreMatrix réussie")
            else:
                logger.warning("Échec de l'intégration avec ScoreMatrix")
        
        return modules
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation des modules avancés: {e}")
        return None

def get_integration_hub(modules=None):
    """
    Récupère l'instance d'IntegrationHub.
    
    Args:
        modules (dict, optional): Modules déjà chargés
        
    Returns:
        IntegrationHub: Instance d'IntegrationHub, None si non disponible
    """
    if modules and "IntegrationHub" in modules:
        return modules["IntegrationHub"]
    
    try:
        advanced_integration = importlib.import_module("modules.advanced_integration")
        return advanced_integration.get_integration_hub(modules or {})
    except ImportError:
        logger.error("Module d'intégration avancée non disponible")
        return None

def get_gematria_oracle(modules=None):
    """
    Récupère l'instance de GematriaOracle.
    
    Args:
        modules (dict, optional): Modules déjà chargés
        
    Returns:
        GematriaOracle: Instance de GematriaOracle, None si non disponible
    """
    if modules and "GematriaOracle" in modules:
        return modules["GematriaOracle"]
    
    try:
        advanced_integration = importlib.import_module("modules.advanced_integration")
        return advanced_integration.get_gematria_oracle(modules or {})
    except ImportError:
        logger.error("Module d'intégration avancée non disponible")
        return None

def get_predictive_forge(modules=None):
    """
    Récupère l'instance de PredictiveForge.
    
    Args:
        modules (dict, optional): Modules déjà chargés
        
    Returns:
        PredictiveForge: Instance de PredictiveForge, None si non disponible
    """
    if modules and "PredictiveForge" in modules:
        return modules["PredictiveForge"]
    
    try:
        advanced_integration = importlib.import_module("modules.advanced_integration")
        return advanced_integration.get_predictive_forge(modules or {})
    except ImportError:
        logger.error("Module d'intégration avancée non disponible")
        return None