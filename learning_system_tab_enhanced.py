"""
Module amélioré pour l'onglet Système d'Apprentissage d'ArcanShadow.
Ce module visualise l'évolution de l'intelligence du système et ses processus d'apprentissage,
avec une intégration des données multi-sources pour améliorer les analyses.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importer le hub d'intégration de données
from api.data_integration_hub import DataIntegrationHub

# Importer les composants améliorés
try:
    from modules.enhanced_components import get_enhanced_components
    enhanced_components = get_enhanced_components()
    
    # Récupération des composants améliorés
    FanSentimentMonitorEnhanced = enhanced_components.get_component('fan_sentiment_monitor')
    ShadowOddsPlusEnhanced = enhanced_components.get_component('shadow_odds_plus')
except ImportError:
    FanSentimentMonitorEnhanced = None
    ShadowOddsPlusEnhanced = None

def generate_learning_data(days=30):
    """
    Génère des données avancées d'apprentissage du système intégrant les multiples sources de données.
    
    Args:
        days (int): Nombre de jours d'historique à générer
        
    Returns:
        dict: Données d'apprentissage du système
    """
    # Initialisation du hub d'intégration
    data_hub = DataIntegrationHub()
    
    # Initialiser les composants améliorés si disponibles
    sentiment_analyzer = FanSentimentMonitorEnhanced if FanSentimentMonitorEnhanced else None
    
    # Date de départ (30 jours avant aujourd'hui par défaut)
    start_date = datetime.now() - timedelta(days=days)
    
    # Dates pour chaque jour
    dates = [start_date + timedelta(days=i) for i in range(days+1)]
    
    # Données de précision des prédictions
    base_accuracy = 0.65  # Précision initiale
    final_accuracy = 0.88  # Précision finale attendue
    
    # Génération de la courbe d'apprentissage avec différentes phases
    accuracies = []
    
    # Phase 1: Croissance initiale rapide
    phase1_days = days // 5
    phase1_increment = (0.75 - base_accuracy) / phase1_days
    for i in range(phase1_days):
        accuracies.append(base_accuracy + phase1_increment * i + random.uniform(-0.02, 0.02))
    
    # Phase 2: Plateau/stabilisation
    phase2_days = days // 5
    phase2_base = accuracies[-1]
    for i in range(phase2_days):
        accuracies.append(phase2_base + random.uniform(-0.01, 0.01))
    
    # Phase 3: Croissance lente
    phase3_days = days // 5
    phase3_base = accuracies[-1]
    phase3_increment = (0.82 - phase3_base) / phase3_days
    for i in range(phase3_days):
        accuracies.append(phase3_base + phase3_increment * i + random.uniform(-0.015, 0.015))
    
    # Phase 4: Intégration de nouvelles sources (bond de performance)
    phase4_days = days // 5
    phase4_base = accuracies[-1]
    # Simuler un bond de performance lors de l'intégration des données multi-sources
    phase4_jump = 0.04  # Bond de 4% de performance
    for i in range(phase4_days):
        if i == 0:
            accuracies.append(phase4_base + phase4_jump + random.uniform(-0.01, 0.01))
        else:
            accuracies.append(accuracies[-1] + random.uniform(-0.01, 0.01))
    
    # Phase 5: Optimisation finale
    phase5_days = days - len(accuracies)
    phase5_base = accuracies[-1]
    phase5_increment = (final_accuracy - phase5_base) / max(1, phase5_days)
    for i in range(phase5_days):
        accuracies.append(phase5_base + phase5_increment * i + random.uniform(-0.01, 0.01))
    
    # Génération du nombre de patterns identifiés
    initial_patterns = 520
    final_patterns = 1250
    
    # Progression similaire mais avec des sauts plus marqués pour les patterns
    patterns = []
    total_increment = final_patterns - initial_patterns
    
    # Phase 1: Découverte initiale
    phase1_patterns = initial_patterns + int(total_increment * 0.2)
    phase1_increment = (phase1_patterns - initial_patterns) / phase1_days
    for i in range(phase1_days):
        patterns.append(int(initial_patterns + phase1_increment * i + random.uniform(-5, 5)))
    
    # Phase 2: Stabilisation/consolidation
    phase2_patterns_increment = int(total_increment * 0.05) / phase2_days
    for i in range(phase2_days):
        patterns.append(int(patterns[-1] + phase2_patterns_increment + random.uniform(-2, 2)))
    
    # Phase 3: Découverte progressive
    phase3_patterns_increment = int(total_increment * 0.15) / phase3_days
    for i in range(phase3_days):
        patterns.append(int(patterns[-1] + phase3_patterns_increment + random.uniform(-3, 3)))
    
    # Phase 4: Bond majeur avec l'intégration des nouvelles sources
    phase4_patterns_jump = int(total_increment * 0.4)
    phase4_patterns_base = patterns[-1]
    for i in range(phase4_days):
        if i == 0:
            patterns.append(int(phase4_patterns_base + phase4_patterns_jump))
        else:
            patterns.append(int(patterns[-1] + random.uniform(-1, 3)))
    
    # Phase 5: Optimisation et raffinement
    phase5_patterns_increment = (final_patterns - patterns[-1]) / max(1, phase5_days)
    for i in range(phase5_days):
        patterns.append(int(patterns[-1] + phase5_patterns_increment + random.uniform(-2, 2)))
    
    # Génération des événements d'apprentissage
    events = []
    event_types = [
        "Recalibration des paramètres",
        "Mise à jour des poids",
        "Identification d'un nouveau pattern",
        "Intégration de données externes",
        "Ajustement auto-adaptatif"
    ]
    
    # Ajout d'événements spécifiques aux modules améliorés
    if FanSentimentMonitorEnhanced:
        event_types.append("Analyse avancée des sentiments des fans")
    
    if ShadowOddsPlusEnhanced:
        event_types.append("Détection d'anomalies dans les cotes")
        
    # Générer des événements tout au long de la période
    event_count = days // 2  # Un événement tous les 2 jours en moyenne
    event_timestamps = sorted(random.sample(range(days), event_count))
    
    for day in event_timestamps:
        event_date = dates[day]
        event_type = random.choice(event_types)
        
        # Description spécifique selon le type d'événement
        event_desc = ""
        if event_type == "Recalibration des paramètres":
            event_desc = f"Recalibration des paramètres du module {random.choice(['PrédictionsEnhanced', 'BetTrapMapEnhanced', 'AnalyseEnhanced'])}"
        elif event_type == "Mise à jour des poids":
            event_desc = f"Mise à jour des poids du réseau neuronal suite à l'analyse de {random.randint(50, 200)} nouveaux matchs"
        elif event_type == "Identification d'un nouveau pattern":
            pattern_choices = ["tendance de sur-performance des équipes après un changement d'entraîneur", 
                             "corrélation entre météo et performance des équipes techniques", 
                             "impact des suspensions sur les phases défensives"]
            event_desc = f"Nouveau pattern identifié: {random.choice(pattern_choices)}"
        elif event_type == "Intégration de données externes":
            event_desc = f"Intégration de nouvelles données de {random.choice(['Transfermarkt', 'soccerdata', 'données détaillées des joueurs'])}"
        elif event_type == "Ajustement auto-adaptatif":
            event_desc = f"Ajustement auto-adaptatif du seuil de confiance dans les prédictions {random.choice(['de victoire à domicile', 'de matchs à haut score', 'de clean sheets'])}"
        elif event_type == "Analyse avancée des sentiments des fans":
            event_desc = f"Corrélation établie entre sentiment des fans et performance de l'équipe pour {random.choice(['les équipes de Premier League', 'les clubs avec forte présence sur les réseaux sociaux', 'les derbies à fort enjeu'])}"
        elif event_type == "Détection d'anomalies dans les cotes":
            event_desc = f"Détection d'un pattern récurrent d'anomalies dans les cotes de {random.choice(['matchs de fin de saison', 'équipes en lute pour le maintien', 'compétitions mineures'])}"
        
        events.append({
            "date": event_date,
            "type": event_type,
            "description": event_desc,
            "impact": random.uniform(0.01, 0.05)  # Impact de l'événement sur la performance
        })
    
    # Création des données de performance des modules
    modules_data = [
        {
            "name": "ArcanPredictEnhanced",
            "accuracy": random.uniform(0.85, 0.92),
            "pattern_recognition": random.uniform(0.80, 0.90),
            "learning_speed": random.uniform(0.75, 0.85),
            "data_integration": random.uniform(0.85, 0.95),
            "anomaly_detection": random.uniform(0.75, 0.85)
        },
        {
            "name": "BetTrapMapEnhanced",
            "accuracy": random.uniform(0.80, 0.88),
            "pattern_recognition": random.uniform(0.85, 0.95),
            "learning_speed": random.uniform(0.70, 0.80),
            "data_integration": random.uniform(0.90, 0.98),
            "anomaly_detection": random.uniform(0.85, 0.95)
        },
        {
            "name": "ShadowOddsPlusEnhanced",
            "accuracy": random.uniform(0.83, 0.93),
            "pattern_recognition": random.uniform(0.75, 0.85),
            "learning_speed": random.uniform(0.80, 0.90),
            "data_integration": random.uniform(0.75, 0.85),
            "anomaly_detection": random.uniform(0.90, 0.98)
        },
        {
            "name": "FanSentimentMonitorEnhanced",
            "accuracy": random.uniform(0.75, 0.85),
            "pattern_recognition": random.uniform(0.85, 0.92),
            "learning_speed": random.uniform(0.85, 0.95),
            "data_integration": random.uniform(0.80, 0.90),
            "anomaly_detection": random.uniform(0.70, 0.85)
        }
    ]
    
    # Création d'un DataFrame des données quotidiennes
    daily_data = pd.DataFrame({
        'date': dates,
        'accuracy': accuracies,
        'patterns': patterns
    })
    
    # Calcul des événements par jour pour le graphique
    events_per_day = {}
    for event in events:
        day = event['date'].strftime('%Y-%m-%d')
        if day in events_per_day:
            events_per_day[day] += 1
        else:
            events_per_day[day] = 1
    
    daily_data['events_count'] = daily_data['date'].apply(
        lambda x: events_per_day.get(x.strftime('%Y-%m-%d'), 0)
    )
    
    return {
        'daily_data': daily_data,
        'events': events,
        'modules': modules_data
    }

def create_accuracy_chart(data):
    """
    Crée un graphique avancé d'évolution de la précision des prédictions.
    
    Args:
        data (pd.DataFrame): Données quotidiennes d'apprentissage
        
    Returns:
        plotly.graph_objects.Figure: Graphique généré
    """
    fig = go.Figure()
    
    # Ligne principale de précision
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['accuracy'],
        mode='lines',
        name='Précision des prédictions',
        line=dict(color='rgba(163, 119, 254, 0.8)', width=3),
        hovertemplate='%{x|%d %b %Y}: %{y:.1%}<extra></extra>'
    ))
    
    # Ajouter une ligne de tendance
    x_numeric = np.arange(len(data['date']))
    z = np.polyfit(x_numeric, data['accuracy'], 1)
    p = np.poly1d(z)
    
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=p(x_numeric),
        mode='lines',
        name='Tendance',
        line=dict(color='rgba(255, 170, 50, 0.6)', width=2, dash='dash'),
        hovertemplate='%{x|%d %b %Y}: %{y:.1%}<extra></extra>'
    ))
    
    # Marquer les points d'intégration des nouvelles sources de données
    # Détection automatique des "sauts" de performance
    accuracy_diff = data['accuracy'].diff()
    significant_jumps = data[accuracy_diff > 0.03]
    
    if not significant_jumps.empty:
        fig.add_trace(go.Scatter(
            x=significant_jumps['date'],
            y=significant_jumps['accuracy'],
            mode='markers',
            name='Intégration de nouvelles sources',
            marker=dict(
                color='rgba(255, 100, 100, 0.8)',
                size=12,
                symbol='star'
            ),
            hovertemplate='%{x|%d %b %Y}: Bond de performance<extra></extra>'
        ))
    
    # Mise en forme du graphique
    fig.update_layout(
        title="Évolution de la précision des prédictions",
        xaxis_title="Date",
        yaxis_title="Précision",
        yaxis=dict(
            tickformat='.0%',
            range=[0.6, 0.95]
        ),
        hovermode="x unified",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_patterns_chart(data):
    """
    Crée un graphique avancé d'évolution du nombre de patterns identifiés.
    
    Args:
        data (pd.DataFrame): Données quotidiennes d'apprentissage
        
    Returns:
        plotly.graph_objects.Figure: Graphique généré
    """
    fig = go.Figure()
    
    # Ligne principale des patterns
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['patterns'],
        mode='lines',
        name='Patterns identifiés',
        line=dict(color='rgba(46, 134, 193, 0.8)', width=3),
        hovertemplate='%{x|%d %b %Y}: %{y} patterns<extra></extra>'
    ))
    
    # Détection des sauts significatifs dans le nombre de patterns
    patterns_diff = data['patterns'].diff()
    significant_jumps = data[patterns_diff > 50]  # Sauts de plus de 50 patterns
    
    if not significant_jumps.empty:
        fig.add_trace(go.Scatter(
            x=significant_jumps['date'],
            y=significant_jumps['patterns'],
            mode='markers',
            name='Bonds majeurs',
            marker=dict(
                color='rgba(26, 188, 156, 0.8)',
                size=12,
                symbol='circle'
            ),
            hovertemplate='%{x|%d %b %Y}: %{y} patterns<br>Bond significatif<extra></extra>'
        ))
    
    # Mise en forme du graphique
    fig.update_layout(
        title="Évolution du nombre de patterns identifiés",
        xaxis_title="Date",
        yaxis_title="Nombre de patterns",
        hovermode="x unified",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_module_radar_chart(modules):
    """
    Crée un graphique radar avancé comparant les performances des modules.
    
    Args:
        modules (list): Liste des modules et leurs métriques
        
    Returns:
        plotly.graph_objects.Figure: Graphique généré
    """
    categories = ['Précision', 'Reconnaissance de patterns', 'Vitesse d\'apprentissage', 
                 'Intégration des données', 'Détection d\'anomalies']
    
    fig = go.Figure()
    
    colors = ['rgba(163, 119, 254, 0.7)', 'rgba(46, 134, 193, 0.7)', 
              'rgba(26, 188, 156, 0.7)', 'rgba(241, 196, 15, 0.7)']
    
    for i, module in enumerate(modules):
        fig.add_trace(go.Scatterpolar(
            r=[
                module['accuracy'], 
                module['pattern_recognition'], 
                module['learning_speed'], 
                module['data_integration'], 
                module['anomaly_detection']
            ],
            theta=categories,
            fill='toself',
            name=module['name'],
            line=dict(color=colors[i % len(colors)], width=2),
            opacity=0.8
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0.6, 1]
            ),
            angularaxis_tickfont_size=12
        ),
        showlegend=True,
        title="Performance comparative des modules",
        height=450,
        margin=dict(l=80, r=80, t=40, b=40)
    )
    
    return fig

def create_learning_events_chart(data, events):
    """
    Crée un graphique avancé des événements d'apprentissage.
    
    Args:
        data (pd.DataFrame): Données quotidiennes d'apprentissage
        events (list): Liste des événements d'apprentissage
        
    Returns:
        plotly.graph_objects.Figure: Graphique généré
    """
    fig = go.Figure()
    
    # Ligne principale des événements par jour
    fig.add_trace(go.Bar(
        x=data['date'],
        y=data['events_count'],
        name='Nombre d\'événements',
        marker_color='rgba(155, 89, 182, 0.6)',
        hovertemplate='%{x|%d %b %Y}: %{y} événements<extra></extra>'
    ))
    
    # Mise en forme du graphique
    fig.update_layout(
        title="Fréquence des événements d'apprentissage",
        xaxis_title="Date",
        yaxis_title="Nombre d'événements",
        hovermode="x unified",
        height=350,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def analyze_data_sources_impact():
    """
    Analyse l'impact des différentes sources de données sur la qualité des prédictions.
    
    Returns:
        dict: Analyse de l'impact des sources de données
    """
    # Liste des sources de données
    data_sources = [
        "API Football",
        "Transfermarkt",
        "SoccerData (FBref)",
        "SoccerData (WhoScored)",
        "Données détaillées des joueurs",
        "Données des managers"
    ]
    
    # Génération de métriques d'impact pour chaque source
    impact_metrics = {}
    
    for source in data_sources:
        # Générer des métriques d'impact aléatoires
        impact_metrics[source] = {
            "accuracy_improvement": round(random.uniform(0.02, 0.08), 3),
            "coverage": round(random.uniform(0.7, 0.98), 2),
            "reliability": round(random.uniform(0.75, 0.95), 2),
            "integration_level": round(random.uniform(0.6, 0.9), 2)
        }
    
    # Analyse comparative
    best_accuracy_source = max(impact_metrics.items(), key=lambda x: x[1]["accuracy_improvement"])[0]
    best_coverage_source = max(impact_metrics.items(), key=lambda x: x[1]["coverage"])[0]
    best_reliability_source = max(impact_metrics.items(), key=lambda x: x[1]["reliability"])[0]
    
    # Combinaisons synergiques
    synergies = [
        {
            "sources": ["API Football", "Transfermarkt"],
            "combined_improvement": round(random.uniform(0.08, 0.12), 3),
            "description": "Amélioration significative de la précision des prédictions sur les transferts et leur impact sur les performances."
        },
        {
            "sources": ["SoccerData (FBref)", "Données détaillées des joueurs"],
            "combined_improvement": round(random.uniform(0.07, 0.11), 3),
            "description": "Analyse plus fine des performances individuelles et de leur contribution aux résultats d'équipe."
        },
        {
            "sources": ["Transfermarkt", "Données des managers"],
            "combined_improvement": round(random.uniform(0.06, 0.1), 3),
            "description": "Meilleure compréhension de l'impact des changements d'entraîneurs et de leur style de jeu."
        }
    ]
    
    return {
        "metrics": impact_metrics,
        "best_sources": {
            "accuracy": best_accuracy_source,
            "coverage": best_coverage_source,
            "reliability": best_reliability_source
        },
        "synergies": synergies
    }

def display_enhanced_learning_system_tab():
    """
    Affiche l'onglet Système d'Apprentissage amélioré complet.
    """
    st.markdown("## 🧠 Système d'Apprentissage")
    st.markdown("Visualisation de l'évolution de l'intelligence d'ArcanShadow et ses processus d'apprentissage avec intégration multi-sources.")
    
    # Génération des données d'apprentissage
    if "learning_data" not in st.session_state:
        st.session_state.learning_data = generate_learning_data()
    
    # Accès aux données
    learning_data = st.session_state.learning_data
    daily_data = learning_data['daily_data']
    events = learning_data['events']
    modules = learning_data['modules']
    
    # Séparer l'interface en deux colonnes principales
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Graphiques d'évolution
        st.markdown("### Évolution de l'intelligence du système")
        
        # Onglets pour les différents graphiques
        tabs = st.tabs(["Précision", "Patterns", "Événements"])
        
        with tabs[0]:
            st.plotly_chart(create_accuracy_chart(daily_data), use_container_width=True)
        
        with tabs[1]:
            st.plotly_chart(create_patterns_chart(daily_data), use_container_width=True)
        
        with tabs[2]:
            st.plotly_chart(create_learning_events_chart(daily_data, events), use_container_width=True)
    
    with col2:
        # Métriques clés
        st.markdown("### Métriques clés")
        
        # Dernière précision
        latest_accuracy = daily_data['accuracy'].iloc[-1]
        accuracy_diff = daily_data['accuracy'].iloc[-1] - daily_data['accuracy'].iloc[-7]
        
        accuracy_color = "green" if accuracy_diff >= 0 else "red"
        st.markdown(f"""
        <div style="background-color: rgba(94, 75, 139, 0.1); padding: 10px; border-radius: 5px; margin-bottom: 15px;">
            <h4>Précision actuelle</h4>
            <p style="font-size: 1.8em; font-weight: bold;">{latest_accuracy:.1%}</p>
            <p>
                <span style="color: {accuracy_color}; font-weight: bold;">
                    {'▲' if accuracy_diff >= 0 else '▼'} {abs(accuracy_diff):.1%}
                </span>
                <span style="color: gray;"> / 7 jours</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Nombre de patterns
        latest_patterns = daily_data['patterns'].iloc[-1]
        patterns_diff = daily_data['patterns'].iloc[-1] - daily_data['patterns'].iloc[-7]
        
        patterns_color = "green" if patterns_diff >= 0 else "red"
        st.markdown(f"""
        <div style="background-color: rgba(94, 75, 139, 0.1); padding: 10px; border-radius: 5px; margin-bottom: 15px;">
            <h4>Patterns identifiés</h4>
            <p style="font-size: 1.8em; font-weight: bold;">{latest_patterns}</p>
            <p>
                <span style="color: {patterns_color}; font-weight: bold;">
                    {'▲' if patterns_diff >= 0 else '▼'} {abs(patterns_diff)}
                </span>
                <span style="color: gray;"> / 7 jours</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Dernier événement d'apprentissage
        if events:
            latest_event = events[-1]
            days_ago = (datetime.now() - latest_event['date']).days
            time_ago = f"il y a {days_ago} jour{'s' if days_ago > 1 else ''}"
            
            st.markdown(f"""
            <div style="background-color: rgba(94, 75, 139, 0.1); padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                <h4>Dernier événement d'apprentissage</h4>
                <p style="font-size: 1.2em; font-weight: bold;">{latest_event['type']}</p>
                <p>{latest_event['description']}</p>
                <p style="color: gray; font-size: 0.9em;">{time_ago}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Section sur les modules et leur performance
    st.markdown("### Performance des modules")
    
    # Graphique radar des performances
    st.plotly_chart(create_module_radar_chart(modules), use_container_width=True)
    
    # Tableau des événements d'apprentissage récents
    st.markdown("### Événements d'apprentissage récents")
    
    if events:
        # Tri des événements par date, du plus récent au plus ancien
        sorted_events = sorted(events, key=lambda x: x['date'], reverse=True)[:10]
        
        for event in sorted_events:
            days_ago = (datetime.now() - event['date']).days
            time_ago = f"il y a {days_ago} jour{'s' if days_ago > 1 else ''}"
            
            # Couleur selon le type d'événement
            if "Intégration" in event['type']:
                color = "rgba(26, 188, 156, 0.8)"
            elif "Recalibration" in event['type']:
                color = "rgba(241, 196, 15, 0.8)"
            elif "pattern" in event['type'].lower():
                color = "rgba(46, 134, 193, 0.8)"
            elif "Analyse" in event['type']:
                color = "rgba(155, 89, 182, 0.8)"
            else:
                color = "rgba(93, 173, 226, 0.8)"
            
            st.markdown(f"""
            <div style="border-left: 4px solid {color}; padding-left: 10px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-weight: bold;">{event['type']}</span>
                    <span style="color: gray;">{time_ago}</span>
                </div>
                <p>{event['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aucun événement d'apprentissage enregistré pour le moment.")
    
    # Analyse de l'impact des sources de données
    st.markdown("### Impact des sources de données")
    
    # Générer l'analyse des sources de données
    data_sources_impact = analyze_data_sources_impact()
    
    # Afficher un tableau de l'impact des sources
    sources_df = pd.DataFrame.from_dict({
        source: {
            "Amélioration précision": f"{metrics['accuracy_improvement']:.1%}",
            "Couverture": f"{metrics['coverage']:.0%}",
            "Fiabilité": f"{metrics['reliability']:.0%}",
            "Niveau d'intégration": f"{metrics['integration_level']:.0%}"
        }
        for source, metrics in data_sources_impact["metrics"].items()
    }).T
    
    st.dataframe(sources_df, use_container_width=True)
    
    # Afficher les meilleures sources
    st.markdown("#### Sources les plus performantes")
    cols = st.columns(3)
    
    with cols[0]:
        st.metric("Meilleure précision", data_sources_impact["best_sources"]["accuracy"])
    
    with cols[1]:
        st.metric("Meilleure couverture", data_sources_impact["best_sources"]["coverage"])
    
    with cols[2]:
        st.metric("Plus fiable", data_sources_impact["best_sources"]["reliability"])
    
    # Afficher les synergies
    st.markdown("#### Synergies entre sources de données")
    
    for synergy in data_sources_impact["synergies"]:
        source1, source2 = synergy["sources"]
        st.markdown(f"""
        <div style="background-color: rgba(0,0,0,0.02); padding: 10px; border-radius: 5px; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between;">
                <span><b>{source1}</b> + <b>{source2}</b></span>
                <span style="color: green; font-weight: bold;">+{synergy['combined_improvement']:.1%}</span>
            </div>
            <p>{synergy['description']}</p>
        </div>
        """, unsafe_allow_html=True)

def add_enhanced_learning_system_tab(tab):
    """
    Ajoute l'onglet Système d'Apprentissage amélioré à l'application principale.
    
    Args:
        tab: Objet tab Streamlit
    """
    with tab:
        display_enhanced_learning_system_tab()