"""
Tableau de bord principal pour ArcanShadow
Permet de visualiser la santé du système et ses connexions aux sources externes.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import os
import json
import logging
import random
import requests

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tentative d'import du hub central
try:
    from api.data_integration_hub import DataIntegrationHub
    hub = DataIntegrationHub()
    HUB_AVAILABLE = True
    logger.info("Hub d'intégration disponible pour le tableau de bord")
except Exception as e:
    logger.error(f"Erreur lors de l'initialisation du hub d'intégration: {e}")
    HUB_AVAILABLE = False
    hub = None

def load_custom_css():
    """Charge le CSS personnalisé pour le tableau de bord"""
    st.markdown("""
    <style>
    .status-card {
        background-color: #1E1E2E;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #7038FF;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .status-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    .status-title {
        font-weight: bold;
        font-size: 18px;
        margin: 0;
    }
    .status-badge {
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
    }
    .status-online {
        background-color: #00B894;
        color: white;
    }
    .status-limited {
        background-color: #FDCB6E;
        color: #2D3436;
    }
    .status-offline {
        background-color: #D63031;
        color: white;
    }
    .metric-container {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-top: 20px;
    }
    .metric-card {
        flex: 1;
        min-width: 120px;
        background-color: #2D2D44;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 12px;
        color: #999;
    }
    .metric-good {
        color: #00B894;
    }
    .metric-warning {
        color: #FDCB6E;
    }
    .metric-bad {
        color: #D63031;
    }
    .health-indicator {
        margin-top: 5px;
        width: 100%;
        height: 4px;
        background-color: #444;
        border-radius: 2px;
        overflow: hidden;
    }
    .health-bar {
        height: 100%;
        border-radius: 2px;
    }
    .connection-line {
        border-left: 2px dashed #444;
        padding-left: 20px;
        margin: 15px 0 15px 20px;
    }
    .indicator-dot {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 10px;
    }
    .pulse {
        box-shadow: 0 0 0 rgba(0, 184, 148, 0.4);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(0, 184, 148, 0.4);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(0, 184, 148, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(0, 184, 148, 0);
        }
    }
    </style>
    """, unsafe_allow_html=True)

def display_system_status():
    """Affiche l'état général du système"""
    # Obtenir le statut du hub et des sources si disponible
    if HUB_AVAILABLE and hub:
        sources_status = hub.sources_status
        connected_sources = sum(1 for status in sources_status.values() if status)
        total_sources = len(sources_status)
        health_percentage = (connected_sources / total_sources) * 100 if total_sources > 0 else 0
        
        if health_percentage >= 75:
            system_status = "online"
            status_color = "status-online"
            health_color = "#00B894"
        elif health_percentage >= 40:
            system_status = "limited"
            status_color = "status-limited"
            health_color = "#FDCB6E"
        else:
            system_status = "offline"
            status_color = "status-offline"
            health_color = "#D63031"
    else:
        system_status = "offline"
        status_color = "status-offline"
        health_color = "#D63031"
        health_percentage = 0
        sources_status = {}
    
    # Afficher la carte de statut du système
    st.markdown(f"""
    <div class="status-card">
        <div class="status-header">
            <h3 class="status-title">Statut du Système</h3>
            <span class="status-badge {status_color}">{system_status.upper()}</span>
        </div>
        <p>Dernière vérification: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        <div class="health-indicator">
            <div class="health-bar" style="width: {health_percentage}%; background-color: {health_color};"></div>
        </div>
        <p style="text-align: right; font-size: 12px; margin-top: 5px;">{health_percentage:.1f}% opérationnel</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Afficher les métriques du système
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    
    # CPU et Mémoire simulés
    cpu_usage = random.uniform(10, 90)
    memory_usage = random.uniform(20, 80)
    uptime_days = random.randint(1, 30)
    
    if cpu_usage < 50:
        cpu_class = "metric-good"
    elif cpu_usage < 80:
        cpu_class = "metric-warning"
    else:
        cpu_class = "metric-bad"
        
    if memory_usage < 50:
        memory_class = "metric-good"
    elif memory_usage < 80:
        memory_class = "metric-warning"
    else:
        memory_class = "metric-bad"
    
    # Métriques système
    metrics = [
        {"label": "CPU", "value": f"{cpu_usage:.1f}%", "class": cpu_class},
        {"label": "Mémoire", "value": f"{memory_usage:.1f}%", "class": memory_class},
        {"label": "Uptime", "value": f"{uptime_days} jours", "class": "metric-good"},
        {"label": "Sources", "value": f"{connected_sources}/{total_sources}", "class": "metric-good" if connected_sources == total_sources else "metric-warning" if connected_sources > 0 else "metric-bad"}
    ]
    
    for metric in metrics:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{metric['label']}</div>
            <div class="metric-value {metric['class']}">{metric['value']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def display_sources_health():
    """Affiche la santé des différentes sources de données"""
    st.markdown("## 🌐 Sources de Données")
    
    if HUB_AVAILABLE and hub:
        sources_status = hub.sources_status
        
        # Essayer de rafraîchir le statut des connexions
        try:
            hub.check_api_connections()
            sources_status = hub.sources_status
        except:
            pass
        
        # Créer un graphique d'état des sources
        labels = list(sources_status.keys())
        values = [1 if status else 0 for status in sources_status.values()]
        colors = ['#00B894' if status else '#D63031' for status in sources_status.values()]
        
        # Nettoyer les noms pour l'affichage
        display_names = {
            'football_api': 'API Football',
            'transfermarkt': 'Transfermarkt',
            'soccerdata': 'SoccerData',
            'time_module': 'Module Temps',
            'cross_platform': 'Adaptateur Cross-Platform'
        }
        
        display_labels = [display_names.get(label, label) for label in labels]
        
        # Créer le graphique avec Plotly
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=display_labels,
            y=values,
            marker_color=colors,
            text=['En ligne' if status else 'Hors ligne' for status in sources_status.values()],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="État des sources de données",
            xaxis_title="Source",
            yaxis_title="Statut",
            template="plotly_dark",
            plot_bgcolor='rgba(25, 25, 44, 0.0)',
            paper_bgcolor='rgba(25, 25, 44, 0.0)',
            height=400,
            yaxis=dict(
                tickvals=[0, 1],
                ticktext=['Hors ligne', 'En ligne']
            ),
            margin=dict(l=40, r=40, t=60, b=40),
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Afficher les détails de chaque source
        for label, status in sources_status.items():
            display_name = display_names.get(label, label)
            status_color = "status-online" if status else "status-offline"
            status_text = "EN LIGNE" if status else "HORS LIGNE"
            status_dot_color = "#00B894" if status else "#D63031"
            pulse_class = "pulse" if status else ""
            
            st.markdown(f"""
            <div class="status-card" style="border-left-color: {status_dot_color};">
                <div class="status-header">
                    <h3 class="status-title">
                        <span class="indicator-dot {pulse_class}" style="background-color: {status_dot_color};"></span>
                        {display_name}
                    </h3>
                    <span class="status-badge {status_color}">{status_text}</span>
                </div>
                <div class="connection-line">
                    <p>Dernière synchronisation: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                    <p>{"Connecté et fonctionnel" if status else "Non connecté - Vérifiez les paramètres de connexion"}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Hub d'intégration non disponible. Impossible d'afficher l'état des sources.")

def display_modules_health():
    """Affiche la santé des différents modules du système"""
    st.markdown("## 🧩 Modules du Système")
    
    # Modules à surveiller
    modules = [
        {
            "name": "Module Prédictions XGBoost",
            "health": random.uniform(0.7, 1.0),
            "last_check": datetime.now() - timedelta(minutes=random.randint(1, 60)),
            "dependencies": ["API Football", "Module Temps"]
        },
        {
            "name": "Module Daily Combo",
            "health": random.uniform(0.6, 1.0),
            "last_check": datetime.now() - timedelta(minutes=random.randint(1, 60)),
            "dependencies": ["API Football", "Transfermarkt"]
        },
        {
            "name": "Module Système d'Apprentissage",
            "health": random.uniform(0.5, 1.0),
            "last_check": datetime.now() - timedelta(minutes=random.randint(1, 60)),
            "dependencies": ["API Football", "SoccerData"]
        },
        {
            "name": "Module Adaptateur Cross-Platform",
            "health": random.uniform(0.8, 1.0),
            "last_check": datetime.now() - timedelta(minutes=random.randint(1, 60)),
            "dependencies": ["Module Temps"]
        },
        {
            "name": "Routes API",
            "health": random.uniform(0.7, 1.0),
            "last_check": datetime.now() - timedelta(minutes=random.randint(1, 60)),
            "dependencies": ["Module Temps", "Adaptateur Cross-Platform"]
        }
    ]
    
    # Créer un dataframe pour la visualisation
    modules_df = pd.DataFrame({
        "Module": [m["name"] for m in modules],
        "Santé": [m["health"] for m in modules]
    })
    
    # Créer un graphique de la santé des modules
    fig = px.bar(
        modules_df,
        x="Module",
        y="Santé",
        color="Santé",
        color_continuous_scale=["#D63031", "#FDCB6E", "#00B894"],
        range_color=[0, 1],
        template="plotly_dark"
    )
    
    fig.update_layout(
        title="Santé des modules",
        xaxis_title="",
        yaxis_title="Niveau de santé",
        plot_bgcolor='rgba(25, 25, 44, 0.0)',
        paper_bgcolor='rgba(25, 25, 44, 0.0)',
        height=400,
        margin=dict(l=40, r=40, t=60, b=80),
    )
    
    fig.update_xaxes(tickangle=45)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Afficher les détails de chaque module
    for module in modules:
        health = module["health"]
        
        if health >= 0.8:
            health_status = "Excellent"
            health_color = "#00B894"
            status_color = "status-online"
        elif health >= 0.6:
            health_status = "Bon"
            health_color = "#FDCB6E"
            status_color = "status-limited"
        else:
            health_status = "Dégradé"
            health_color = "#D63031"
            status_color = "status-offline"
        
        st.markdown(f"""
        <div class="status-card">
            <div class="status-header">
                <h3 class="status-title">{module["name"]}</h3>
                <span class="status-badge {status_color}">{health_status}</span>
            </div>
            <p>Dernière vérification: {module["last_check"].strftime('%d/%m/%Y %H:%M:%S')}</p>
            <div class="health-indicator">
                <div class="health-bar" style="width: {health*100}%; background-color: {health_color};"></div>
            </div>
            <p style="text-align: right; font-size: 12px; margin-top: 5px;">{health*100:.1f}% opérationnel</p>
            <div class="connection-line">
                <p><strong>Dépendances:</strong> {', '.join(module["dependencies"])}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_api_readiness():
    """Affiche l'état de préparation de l'API pour l'application mobile"""
    st.markdown("## 📱 Préparation ArcanApp")
    
    # Vérifier si l'adaptateur cross-platform est disponible
    cross_platform_ready = HUB_AVAILABLE and hub and hub.sources_status.get('cross_platform', False)
    
    # Évaluer l'état de préparation de l'API
    api_components = [
        {
            "name": "Endpoints API",
            "ready": True,
            "description": "Les routes API de base sont en place pour l'application mobile."
        },
        {
            "name": "Adaptateur Cross-Platform",
            "ready": cross_platform_ready,
            "description": "L'adaptateur qui optimise les données pour différentes plateformes."
        },
        {
            "name": "Module Temporel",
            "ready": HUB_AVAILABLE and hub and hub.sources_status.get('time_module', False),
            "description": "Module de gestion du temps pour l'affichage contextualisé des matchs."
        },
        {
            "name": "Configuration Mobile",
            "ready": cross_platform_ready,
            "description": "Configuration prête pour l'application mobile."
        },
        {
            "name": "Sources de Données",
            "ready": HUB_AVAILABLE and hub and hub.sources_status.get('football_api', False),
            "description": "Sources de données réelles pour alimenter l'application."
        }
    ]
    
    # Calculer le pourcentage de préparation global
    ready_components = sum(1 for c in api_components if c["ready"])
    total_components = len(api_components)
    readiness_percentage = (ready_components / total_components) * 100 if total_components > 0 else 0
    
    # Afficher la jauge de préparation
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = readiness_percentage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "État de préparation ArcanApp"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "#7038FF"},
            'steps': [
                {'range': [0, 30], 'color': "#D63031"},
                {'range': [30, 70], 'color': "#FDCB6E"},
                {'range': [70, 100], 'color': "#00B894"}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        plot_bgcolor='rgba(25, 25, 44, 0.0)',
        paper_bgcolor='rgba(25, 25, 44, 0.0)',
        margin=dict(l=40, r=40, t=60, b=40),
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Afficher les détails des composants
    for component in api_components:
        status_color = "status-online" if component["ready"] else "status-offline"
        status_text = "PRÊT" if component["ready"] else "NON PRÊT"
        status_dot_color = "#00B894" if component["ready"] else "#D63031"
        
        st.markdown(f"""
        <div class="status-card" style="border-left-color: {status_dot_color};">
            <div class="status-header">
                <h3 class="status-title">
                    <span class="indicator-dot" style="background-color: {status_dot_color};"></span>
                    {component["name"]}
                </h3>
                <span class="status-badge {status_color}">{status_text}</span>
            </div>
            <p>{component["description"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Message de conseil pour la création de l'application mobile
    if readiness_percentage >= 80:
        st.success("""
        ✅ **ArcanShadow est prêt pour ArcanApp !**
        
        Vous pouvez maintenant commencer le développement de l'application mobile en utilisant les endpoints API
        et l'adaptateur cross-platform qui sont en place.
        """)
        
        # Étapes pour ArcanApp
        st.markdown("""
        ### Étapes pour créer ArcanApp :
        
        1. **Choisir un framework mobile**
           - React Native (JavaScript/TypeScript) pour un développement multi-plateforme
           - Flutter (Dart) pour une interface hautement personnalisée
           - Swift/SwiftUI (iOS natif) pour une expérience optimisée sur iOS
           - Kotlin (Android natif) pour une expérience optimisée sur Android
        
        2. **Configurer l'environnement de développement**
           - Installer les SDK et outils nécessaires
           - Configurer l'IDE (XCode, Android Studio, VS Code)
        
        3. **Créer la structure de l'application**
           - Architecture : MVVM ou Redux recommandé
           - Navigation : Tabs + Stack Navigation
           - État global : Context API ou Redux
        
        4. **Intégrer les API**
           - Utiliser les endpoints fournis `/api/matches`, `/api/predictions`, etc.
           - Configuration pour les environnements de dev/prod
        
        5. **Développer les fonctionnalités principales**
           - Authentification utilisateur
           - Liste des matchs
           - Détails des prédictions
           - Notifications push
        
        6. **Tests et déploiement**
           - Tests unitaires et d'intégration
           - Publication sur App Store et Play Store
        """)
    else:
        st.warning(f"""
        ⚠️ **ArcanShadow est partiellement prêt ({readiness_percentage:.0f}%) pour ArcanApp**
        
        Certains composants doivent être complétés avant de commencer le développement mobile :
        
        {"- Assurez-vous que l'adaptateur cross-platform est fonctionnel" if not cross_platform_ready else ""}
        {"- Connectez au moins une source de données réelle" if not (HUB_AVAILABLE and hub and hub.sources_status.get('football_api', False)) else ""}
        {"- Vérifiez que le module temporel est actif" if not (HUB_AVAILABLE and hub and hub.sources_status.get('time_module', False)) else ""}
        """)

def main():
    """Fonction principale du tableau de bord"""
    # Configuration de la page Streamlit
    st.set_page_config(
        page_title="ArcanShadow - Tableau de Bord",
        page_icon="📊",
        layout="wide"
    )
    
    # Charger le CSS personnalisé
    load_custom_css()
    
    # En-tête
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <span style="font-size: 48px; margin-right: 15px;">📊</span>
        <div>
            <h1 style="margin: 0;">ArcanShadow - Tableau de Bord</h1>
            <p style="margin: 0; color: #999;">Surveillance du système et préparation ArcanApp</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Afficher l'état général du système
    display_system_status()
    
    # Afficher l'état des sources et des modules dans des colonnes
    col1, col2 = st.columns(2)
    
    with col1:
        display_sources_health()
        
    with col2:
        display_modules_health()
    
    # Afficher l'état de préparation de l'API pour l'application mobile
    display_api_readiness()
    
    # Rafraîchissement automatique toutes les 60 secondes
    st.markdown("""
    <script>
        setTimeout(function(){
            window.location.reload();
        }, 60000);
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()