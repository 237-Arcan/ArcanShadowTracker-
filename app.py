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

# Importer les versions enrichies (si disponibles)
try:
    from predictions_tab_enhanced import display_enhanced_predictions_tab
    ENHANCED_PREDICTIONS_AVAILABLE = True
    logger.info("Module de prédictions enrichi disponible")
except ImportError:
    ENHANCED_PREDICTIONS_AVAILABLE = False
    logger.warning("Module de prédictions enrichi non disponible, utilisation de la version classique")

# Vérifier si le hub de données est disponible
try:
    from api.data_integration_hub import get_data_integration_hub, get_available_sources
    DATA_HUB_AVAILABLE = True
    # Récupérer les sources disponibles pour informations
    available_sources = get_available_sources()
    logger.info(f"Hub d'intégration de données disponible. Sources: {available_sources}")
except ImportError:
    DATA_HUB_AVAILABLE = False
    logger.warning("Hub d'intégration de données non disponible")

# Vérifier si le module FanSentimentMonitor enrichi est disponible
try:
    from modules.fan_sentiment_monitor_enhanced import FanSentimentMonitorEnhanced
    ENHANCED_SENTIMENT_AVAILABLE = True
    logger.info("Module FanSentimentMonitor enrichi disponible")
except ImportError:
    ENHANCED_SENTIMENT_AVAILABLE = False
    logger.warning("Module FanSentimentMonitor enrichi non disponible")

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

# Affichage des onglets
with tabs[0]:
    # Utiliser la version améliorée de l'onglet Prédictions si disponible
    if ENHANCED_PREDICTIONS_AVAILABLE:
        st.info("🌟 Version enrichie avec données multi-sources activée")
        display_enhanced_predictions_tab()
    else:
        display_predictions_tab()
    
with tabs[1]:
    display_daily_combo_tab()
    
with tabs[2]:
    display_learning_system_tab()
    
with tabs[3]:
    display_notifications_tab()