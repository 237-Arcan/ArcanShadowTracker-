import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import os
import matplotlib.pyplot as plt
import requests
import random
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importer nos modules pour les différents onglets - versions classiques
from predictions_tab import display_predictions_tab
from daily_combo_tab import display_daily_combo_tab
from learning_system_tab import display_learning_system_tab
from notifications_tab import display_notifications_tab

# Import des versions améliorées
try:
    # Import direct des modules améliorés
    from predictions_tab_enhanced import display_enhanced_predictions_tab
    DIRECT_ENHANCED_PREDICTIONS_AVAILABLE = True
except ImportError:
    DIRECT_ENHANCED_PREDICTIONS_AVAILABLE = False
    display_enhanced_predictions_tab = None
    
try:
    from daily_combo_tab_enhanced import display_enhanced_daily_combo_tab
    DIRECT_ENHANCED_DAILY_COMBO_AVAILABLE = True
except ImportError:
    DIRECT_ENHANCED_DAILY_COMBO_AVAILABLE = False
    display_enhanced_daily_combo_tab = None
    
try:
    from learning_system_tab_enhanced import display_enhanced_learning_system_tab
    DIRECT_ENHANCED_LEARNING_SYSTEM_AVAILABLE = True
except ImportError:
    DIRECT_ENHANCED_LEARNING_SYSTEM_AVAILABLE = False
    display_enhanced_learning_system_tab = None
    
try:
    from notifications_tab_enhanced import display_enhanced_notifications_tab
    DIRECT_ENHANCED_NOTIFICATIONS_AVAILABLE = True
except ImportError:
    DIRECT_ENHANCED_NOTIFICATIONS_AVAILABLE = False
    display_enhanced_notifications_tab = None

# Importer le module d'intégration des composants enrichis
try:
    from modules.enhanced_components import get_enhanced_components
    enhanced_components = get_enhanced_components()
    ENHANCED_COMPONENTS_AVAILABLE = True
    
    # Récupérer le statut des composants enrichis
    components_summary = enhanced_components.get_available_components_summary()
    logger.info(f"Composants enrichis disponibles: {components_summary}")
    
    # Vérifier si les composants spécifiques sont disponibles via le gestionnaire
    ENHANCED_PREDICTIONS_AVAILABLE = enhanced_components.is_enhanced('predictions_tab') and DIRECT_ENHANCED_PREDICTIONS_AVAILABLE
    ENHANCED_DAILY_COMBO_AVAILABLE = enhanced_components.is_enhanced('daily_combo_tab') and DIRECT_ENHANCED_DAILY_COMBO_AVAILABLE
    ENHANCED_LEARNING_SYSTEM_AVAILABLE = enhanced_components.is_enhanced('learning_system_tab') and DIRECT_ENHANCED_LEARNING_SYSTEM_AVAILABLE
    ENHANCED_NOTIFICATIONS_AVAILABLE = enhanced_components.is_enhanced('notifications_tab') and DIRECT_ENHANCED_NOTIFICATIONS_AVAILABLE
    ENHANCED_BET_TRAP_MAP_AVAILABLE = enhanced_components.is_enhanced('bet_trap_map')
    ENHANCED_SHADOW_ODDS_PLUS_AVAILABLE = enhanced_components.is_enhanced('shadow_odds_plus')
    ENHANCED_SENTIMENT_AVAILABLE = enhanced_components.is_enhanced('fan_sentiment_monitor')
    
    # Récupérer les fonctions/instances enrichies
    if ENHANCED_PREDICTIONS_AVAILABLE:
        display_enhanced_predictions_tab = enhanced_components.get_display_predictions_tab()
        logger.info("Module de prédictions enrichi disponible via le gestionnaire de composants")
    
    if ENHANCED_DAILY_COMBO_AVAILABLE:
        display_enhanced_daily_combo_tab = enhanced_components.get_daily_combo_tab()
        logger.info("Module Daily Combo enrichi disponible via le gestionnaire de composants")
    
    if ENHANCED_LEARNING_SYSTEM_AVAILABLE:
        display_enhanced_learning_system_tab = enhanced_components.get_learning_system_tab()
        logger.info("Module Système d'Apprentissage enrichi disponible via le gestionnaire de composants")
    
    if ENHANCED_NOTIFICATIONS_AVAILABLE:
        display_enhanced_notifications_tab = enhanced_components.get_notifications_tab()
        logger.info("Module Notifications enrichi disponible via le gestionnaire de composants")
    
    if ENHANCED_BET_TRAP_MAP_AVAILABLE:
        bet_trap_map = enhanced_components.get_bet_trap_map()
        logger.info("Module BetTrapMap enrichi disponible via le gestionnaire de composants")
    
    if ENHANCED_SHADOW_ODDS_PLUS_AVAILABLE:
        shadow_odds_plus = enhanced_components.get_shadow_odds_plus()
        logger.info("Module ShadowOddsPlus enrichi disponible via le gestionnaire de composants")
    
    if ENHANCED_SENTIMENT_AVAILABLE:
        fan_sentiment_monitor = enhanced_components.get_fan_sentiment_monitor()
        logger.info("Module FanSentimentMonitor enrichi disponible via le gestionnaire de composants")

except ImportError as e:
    ENHANCED_COMPONENTS_AVAILABLE = False
    ENHANCED_PREDICTIONS_AVAILABLE = False
    ENHANCED_DAILY_COMBO_AVAILABLE = False
    ENHANCED_LEARNING_SYSTEM_AVAILABLE = False
    ENHANCED_NOTIFICATIONS_AVAILABLE = False
    ENHANCED_BET_TRAP_MAP_AVAILABLE = False
    ENHANCED_SHADOW_ODDS_PLUS_AVAILABLE = False
    ENHANCED_SENTIMENT_AVAILABLE = False
    logger.warning(f"Gestionnaire de composants enrichis non disponible: {e}")
    
    # Essayer d'importer individuellement
    try:
        from predictions_tab_enhanced import display_enhanced_predictions_tab
        ENHANCED_PREDICTIONS_AVAILABLE = True
        logger.info("Module de prédictions enrichi disponible")
    except ImportError:
        ENHANCED_PREDICTIONS_AVAILABLE = False
        logger.warning("Module de prédictions enrichi non disponible, utilisation de la version classique")

# Initialiser le hub d'intégration de données
try:
    # Créer une instance du hub d'intégration pour la partager globalement
    from api.data_integration_hub import DataIntegrationHub
    # Créer l'instance globale qui sera utilisée par tous les modules
    global data_hub
    data_hub = DataIntegrationHub()
    DATA_HUB_AVAILABLE = True
    
    # Vérifier le statut des API
    api_status = data_hub.sources_status
    logger.info(f"Hub d'intégration de données initialisé avec succès. Status des API: {api_status}")
    
    # Si l'API Football n'est pas disponible, vérifier la clé API
    if not api_status.get('football_api', False):
        football_api_key = os.environ.get('FOOTBALL_API_KEY')
        if not football_api_key:
            logger.warning("Clé API Football non trouvée dans les variables d'environnement")
        else:
            logger.warning("Clé API Football trouvée mais l'API n'est pas accessible")
except ImportError as e:
    DATA_HUB_AVAILABLE = False
    data_hub = None
    logger.warning(f"Hub d'intégration de données non disponible: {e}")
except Exception as e:
    DATA_HUB_AVAILABLE = False
    data_hub = None
    logger.error(f"Erreur lors de l'initialisation du hub d'intégration: {e}")

# Fonction pour charger le CSS personnalisé
def load_custom_css():
    """Charge le fichier CSS personnalisé pour transformer l'interface ArcanShadow"""
    st.markdown("""
    <style>
        /* Thème sombre avec accent mystique */
        .stApp {
            background-color: #1E1E2E;
            color: #E0E0E0;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: #2D2D44;
            border-radius: 10px;
            padding: 5px;
            margin-bottom: 20px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 5px;
            color: #D0D0D0;
            background-color: #352F44;
            padding: 5px 10px;
            font-size: 14px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #5E4B8B;
            color: white;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #A377FE;
        }
        .important-insight {
            border-left: 4px solid #A377FE;
            padding-left: 10px;
            background-color: rgba(163, 119, 254, 0.1);
        }
        /* Style pour les cartes de match */
        .match-card {
            background-color: #2D2D44;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #A377FE;
        }
        /* Style pour les badges */
        .badge {
            display: inline-block;
            padding: 3px 8px;
            font-size: 12px;
            font-weight: bold;
            border-radius: 12px;
            margin-right: 5px;
        }
        .badge-high {
            background-color: #58D68D;
            color: #0E2E1E;
        }
        .badge-medium {
            background-color: #F4D03F;
            color: #2E2E0E;
        }
        .badge-low {
            background-color: #EC7063;
            color: #2E0E0E;
        }
        /* Style pour les graphiques */
        .plot-container {
            background-color: #2D2D44;
            border-radius: 10px;
            padding: 15px;
        }
        /* Style pour les notifications */
        .notification {
            background-color: rgba(163, 119, 254, 0.2);
            border-left: 4px solid #A377FE;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
        }
        .notification-new {
            background-color: rgba(88, 214, 141, 0.2);
            border-left: 4px solid #58D68D;
        }
    </style>
    """, unsafe_allow_html=True)

# Fonction d'internationalisation (i18n)
def t(key, **format_args):
    """Helper function to get text in the current language"""
    # Définir la langue (à terme, cette valeur sera configurable)
    lang = "fr"  # ou "en" pour l'anglais
    
    # Dictionnaire de traductions
    translations = {
        "fr": {
            "app_title": "ArcanShadow",
            "welcome_message": "Bienvenue dans l'interface d'ArcanShadow, votre système avancé de prédiction sportive",
            "featured_matches": "Matchs à la une",
            "today_matches": "Matchs du jour",
            "predictions": "Prédictions",
            "performance": "Performance",
            "confidence": "Confiance",
            "notifications": "Notifications",
            "daily_combo": "Combo du jour",
            "smart_recommendations": "Recommandations intelligentes",
            "learning_system": "Système d'apprentissage",
            # Ajouter d'autres traductions au besoin
        },
        "en": {
            "app_title": "ArcanShadow",
            "welcome_message": "Welcome to ArcanShadow interface, your advanced sports prediction system",
            "featured_matches": "Featured Matches",
            "today_matches": "Today's Matches",
            "predictions": "Predictions",
            "performance": "Performance",
            "confidence": "Confidence",
            "notifications": "Notifications",
            "daily_combo": "Daily Combo",
            "smart_recommendations": "Smart Recommendations",
            "learning_system": "Learning System",
            # Ajouter d'autres traductions au besoin
        }
    }
    
    # Récupérer la traduction
    text = translations.get(lang, {}).get(key, key)
    
    # Appliquer les arguments de format si nécessaire
    if format_args:
        text = text.format(**format_args)
    
    return text

# Configuration de la page
st.set_page_config(
    page_title="ArcanShadow",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Charger le CSS personnalisé
load_custom_css()

# Interface principale
st.title(f"🔮 {t('app_title')}")
st.markdown(f"### {t('welcome_message')}")

# Créer les onglets pour la nouvelle version d'ArcanShadow
tabs = st.tabs([
    "🔮 Prédictions",
    "🎯 Daily Combo",
    "🧠 Système d'Apprentissage",
    "📬 Notifications"
])

# Fonction pour afficher un badge de statut des composants améliorés
def show_enhanced_components_status():
    """Affiche un résumé des composants améliorés disponibles"""
    st.sidebar.markdown("### 🔮 Statut ArcanShadow")
    
    # Afficher l'état du hub d'intégration de données
    if DATA_HUB_AVAILABLE and data_hub:
        st.sidebar.markdown("🔄 **Hub d'intégration central** ✅")
        
        # Obtenir le statut des API du hub
        api_status = data_hub.sources_status
        
        # Afficher le statut des API
        st.sidebar.markdown("**Sources de données disponibles:**")
        
        football_api_status = api_status.get('football_api', False)
        football_icon = "✅" if football_api_status else "⚠️"
        football_text = "Connectée" if football_api_status else "Simulation" 
        st.sidebar.markdown(f"- {football_icon} API Football: **{football_text}**")
        
        transfermarkt_status = api_status.get('transfermarkt', False)
        transfermarkt_icon = "✅" if transfermarkt_status else "⚠️"
        transfermarkt_text = "Connectée" if transfermarkt_status else "Simulation"
        st.sidebar.markdown(f"- {transfermarkt_icon} Transfermarkt: **{transfermarkt_text}**")
        
        soccerdata_status = api_status.get('soccerdata', False)
        soccerdata_icon = "✅" if soccerdata_status else "⚠️"
        soccerdata_text = "Connectée" if soccerdata_status else "Simulation"
        st.sidebar.markdown(f"- {soccerdata_icon} soccerdata: **{soccerdata_text}**")
        
        # Ajouter un indicateur de connexion pour aider au débogage
        football_api_key = os.environ.get('FOOTBALL_API_KEY')
        if not football_api_key and not football_api_status:
            st.sidebar.warning("⚠️ Clé API Football non configurée")
        elif not football_api_status and football_api_key:
            st.sidebar.warning("⚠️ Problème de connexion à l'API Football")
    else:
        st.sidebar.markdown("🔄 **Hub d'intégration central** ❌")
        st.sidebar.warning("Hub non initialisé. Les fonctionnalités utiliseront des données simulées.")
    
    # Afficher le statut des composants enrichis
    if ENHANCED_COMPONENTS_AVAILABLE:
        # Compter combien de composants améliorés sont disponibles
        enhanced_count = sum([
            ENHANCED_PREDICTIONS_AVAILABLE,
            ENHANCED_BET_TRAP_MAP_AVAILABLE,
            ENHANCED_SHADOW_ODDS_PLUS_AVAILABLE, 
            ENHANCED_SENTIMENT_AVAILABLE
        ])
        
        total_count = 4  # Nombre total de composants améliorés
        
        if enhanced_count > 0:
            st.sidebar.markdown("### 🌟 Composants enrichis")
            
            # Afficher un indicateur pour chaque composant
            components_status = {
                "Prédictions XGBoost": True,  # Toujours disponible maintenant
                "BetTrapMap": ENHANCED_BET_TRAP_MAP_AVAILABLE,
                "ShadowOddsPlus": ENHANCED_SHADOW_ODDS_PLUS_AVAILABLE,
                "FanSentimentMonitor": ENHANCED_SENTIMENT_AVAILABLE
            }
            
            status_html = "<div style='margin-bottom: 20px;'>"
            for component, is_enhanced in components_status.items():
                icon = "✅" if is_enhanced else "⚪"
                status_html += f"<div>{icon} {component}</div>"
            status_html += "</div>"
            
            st.sidebar.markdown(status_html, unsafe_allow_html=True)
    
    # Afficher un résumé des bénéfices
    st.sidebar.markdown("### ✨ Améliorations activées")
    st.sidebar.markdown("- 🧠 **Moteur XGBoost** pour des prédictions précises")
    st.sidebar.markdown("- 📊 Analyses basées sur des données multi-sources")
    st.sidebar.markdown("- 📱 Interface mobile améliorée")
    st.sidebar.markdown("- 🔍 Détection avancée de patterns")
    
    # Si les données sont simulées, afficher un avertissement
    if DATA_HUB_AVAILABLE and data_hub and not data_hub.sources_status.get('football_api', False):
        with st.sidebar.expander("ℹ️ Mode simulation"):
            st.markdown("""
            Le système fonctionne actuellement avec des données simulées.
            Pour obtenir des prédictions avec des données réelles, veuillez configurer
            votre clé API Football.
            """)
            if st.button("Vérifier les connexions"):
                st.session_state.check_connections = True

# Afficher le statut des composants améliorés
show_enhanced_components_status()

# Affichage des onglets
with tabs[0]:
    # Utiliser notre nouvel onglet de prédictions XGBoost
    try:
        # Importer le module de prédictions XGBoost
        from xgboost_predictions_tab import display_xgboost_predictions_tab
        display_xgboost_predictions_tab()
    except Exception as e:
        st.error(f"Erreur lors de l'affichage de l'interface XGBoost: {e}")
        # Fallback en cas d'erreur critique
        if ENHANCED_PREDICTIONS_AVAILABLE and display_enhanced_predictions_tab is not None:
            st.warning("Retour à l'interface standard en raison d'une erreur")
            display_enhanced_predictions_tab()
        else:
            st.warning("Retour à l'interface standard en raison d'une erreur")
            display_predictions_tab()
    
with tabs[1]:
    # Utiliser la version améliorée de l'onglet Daily Combo si disponible
    if ENHANCED_DAILY_COMBO_AVAILABLE and display_enhanced_daily_combo_tab is not None:
        st.info("🌟 Version enrichie avec données multi-sources activée")
        try:
            display_enhanced_daily_combo_tab()
        except Exception as e:
            st.error(f"Erreur lors de l'affichage de l'onglet Daily Combo enrichi: {e}")
            display_daily_combo_tab()
    else:
        # Afficher un indicateur si les composants enrichis sont utilisés pour Daily Combo
        if ENHANCED_BET_TRAP_MAP_AVAILABLE or ENHANCED_SHADOW_ODDS_PLUS_AVAILABLE:
            st.info("🌟 Composants enrichis utilisés pour l'analyse des opportunités")
        display_daily_combo_tab()
    
with tabs[2]:
    # Utiliser la version améliorée de l'onglet Système d'Apprentissage si disponible
    if ENHANCED_LEARNING_SYSTEM_AVAILABLE and display_enhanced_learning_system_tab is not None:
        st.info("🌟 Version enrichie avec données multi-sources activée")
        try:
            display_enhanced_learning_system_tab()
        except Exception as e:
            st.error(f"Erreur lors de l'affichage de l'onglet Système d'Apprentissage enrichi: {e}")
            display_learning_system_tab()
    else:
        # Afficher un indicateur si les composants enrichis sont utilisés pour le Système d'Apprentissage
        if ENHANCED_PREDICTIONS_AVAILABLE or ENHANCED_SENTIMENT_AVAILABLE:
            st.info("🌟 Données multi-sources intégrées au système d'apprentissage")
        display_learning_system_tab()
    
with tabs[3]:
    # Utiliser la version améliorée de l'onglet Notifications si disponible
    if ENHANCED_NOTIFICATIONS_AVAILABLE and display_enhanced_notifications_tab is not None:
        st.info("🌟 Version enrichie avec données multi-sources activée")
        try:
            display_enhanced_notifications_tab()
        except Exception as e:
            st.error(f"Erreur lors de l'affichage de l'onglet Notifications enrichi: {e}")
            display_notifications_tab()
    else:
        # Afficher un indicateur si les composants enrichis sont utilisés pour les Notifications
        if ENHANCED_SENTIMENT_AVAILABLE or ENHANCED_SHADOW_ODDS_PLUS_AVAILABLE:
            st.info("🌟 Détection avancée des événements significatifs activée")
        display_notifications_tab()