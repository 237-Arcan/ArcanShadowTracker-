"""
Module pour l'onglet Système d'Apprentissage d'ArcanShadow.
Ce module visualise l'évolution de l'intelligence du système et ses processus d'apprentissage.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

def generate_learning_data(days=30):
    """
    Génère des données simulées d'apprentissage du système.
    
    Args:
        days (int): Nombre de jours d'historique à générer
        
    Returns:
        dict: Données d'apprentissage du système
    """
    # Date de début (il y a 'days' jours)
    start_date = datetime.now() - timedelta(days=days)
    dates = [start_date + timedelta(days=i) for i in range(days)]
    
    # Précision des prédictions (tendance à l'amélioration avec du bruit)
    base_accuracy = 0.65
    noise = np.random.normal(0, 0.03, days)
    trend = np.linspace(0, 0.15, days)  # Amélioration progressive
    accuracy = np.clip(base_accuracy + trend + noise, 0.5, 0.95)
    
    # Nombre de modèles/patterns découverts (augmentation progressive)
    patterns_base = 45
    new_patterns = np.cumsum(np.random.poisson(0.7, days))
    patterns = patterns_base + new_patterns
    
    # Nombre d'événements d'apprentissage
    learning_events = np.random.poisson(5, days)
    
    # Métriques de confiance
    confidence_base = 0.6
    confidence_noise = np.random.normal(0, 0.02, days)
    confidence_trend = np.linspace(0, 0.2, days)
    confidence = np.clip(confidence_base + confidence_trend + confidence_noise, 0.5, 0.9)
    
    # Créer un DataFrame pour faciliter la manipulation
    df = pd.DataFrame({
        'date': dates,
        'accuracy': accuracy,
        'patterns': patterns,
        'learning_events': learning_events,
        'confidence': confidence
    })
    
    # Générer des événements d'apprentissage significatifs
    significant_events = []
    for i in range(3, days, 7):
        if random.random() > 0.5:
            event_date = dates[i]
            event_types = [
                "Recalibration des patterns", 
                "Transfert d'apprentissage", 
                "Optimisation du modèle",
                "Adaptation contextuelle",
                "Découverte de corrélation"
            ]
            event_type = random.choice(event_types)
            
            if event_type == "Recalibration des patterns":
                description = "ArcanBrain a recalibré ses modèles de reconnaissance de patterns suite à des résultats inattendus."
            elif event_type == "Transfert d'apprentissage":
                description = "Les connaissances acquises sur un championnat ont été transférées et adaptées à un autre contexte."
            elif event_type == "Optimisation du modèle":
                description = "Les paramètres du modèle prédictif ont été optimisés pour améliorer la précision des prévisions."
            elif event_type == "Adaptation contextuelle":
                description = "Le système a ajusté ses analyses pour tenir compte de changements dans le contexte des compétitions."
            else:
                description = "ArcanShadow a découvert une nouvelle corrélation statistique significative entre différents facteurs."
                
            impact = random.uniform(0.03, 0.08)
            
            significant_events.append({
                'date': event_date,
                'type': event_type,
                'description': description,
                'impact': impact
            })
    
    # Modules du système et leurs métriques
    modules = [
        {"name": "ArcanBrain", "efficiency": 0.88, "learning_rate": 0.76, "complexity": 0.92},
        {"name": "ArcanReflex", "efficiency": 0.84, "learning_rate": 0.89, "complexity": 0.65},
        {"name": "ArcanSentinel", "efficiency": 0.91, "learning_rate": 0.72, "complexity": 0.78},
        {"name": "NumeriCode", "efficiency": 0.79, "learning_rate": 0.83, "complexity": 0.87},
        {"name": "ScoreMatrix", "efficiency": 0.86, "learning_rate": 0.75, "complexity": 0.70}
    ]
    
    return {
        "daily_metrics": df,
        "significant_events": significant_events,
        "modules": modules
    }

def create_accuracy_chart(data):
    """
    Crée un graphique d'évolution de la précision des prédictions.
    
    Args:
        data (pd.DataFrame): Données quotidiennes d'apprentissage
        
    Returns:
        plotly.graph_objects.Figure: Graphique généré
    """
    fig = go.Figure()
    
    # Ajouter la ligne de précision
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['accuracy'],
        mode='lines',
        name='Précision des prédictions',
        line=dict(color='rgba(163, 119, 254, 0.8)', width=3),
        hovertemplate='%{y:.1%}<extra>Précision</extra>'
    ))
    
    # Ajouter la ligne de confiance
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['confidence'],
        mode='lines',
        name='Niveau de confiance',
        line=dict(color='rgba(26, 188, 156, 0.8)', width=3, dash='dash'),
        hovertemplate='%{y:.1%}<extra>Confiance</extra>'
    ))
    
    # Mise en page
    fig.update_layout(
        title='Évolution de la précision et de la confiance',
        xaxis_title='Date',
        yaxis_title='Métrique',
        yaxis_tickformat='.0%',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='rgba(0,0,0,0.02)',
        height=400
    )
    
    # Ajouter une zone d'objectif
    fig.add_shape(
        type="rect",
        xref="paper",
        yref="y",
        x0=0,
        y0=0.8,
        x1=1,
        y1=1,
        fillcolor="rgba(0,255,0,0.1)",
        line_width=0,
        layer="below"
    )
    
    # Ajouter une ligne pour l'objectif
    fig.add_shape(
        type="line",
        xref="paper",
        yref="y",
        x0=0,
        y0=0.8,
        x1=1,
        y1=0.8,
        line=dict(
            color="green",
            width=2,
            dash="dash",
        )
    )
    
    # Ajouter des annotations pour les événements significatifs
    #for event in significant_events:
    #    fig.add_annotation(...)
    
    return fig

def create_patterns_chart(data):
    """
    Crée un graphique d'évolution du nombre de patterns identifiés.
    
    Args:
        data (pd.DataFrame): Données quotidiennes d'apprentissage
        
    Returns:
        plotly.graph_objects.Figure: Graphique généré
    """
    fig = go.Figure()
    
    # Ajouter la ligne de patterns
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['patterns'],
        mode='lines',
        name='Patterns identifiés',
        line=dict(color='rgba(231, 76, 60, 0.8)', width=3),
        fill='tozeroy',
        fillcolor='rgba(231, 76, 60, 0.1)'
    ))
    
    # Mise en page
    fig.update_layout(
        title='Évolution du nombre de patterns identifiés',
        xaxis_title='Date',
        yaxis_title='Nombre de patterns',
        plot_bgcolor='rgba(0,0,0,0.02)',
        height=350
    )
    
    return fig

def create_module_radar_chart(modules):
    """
    Crée un graphique radar comparant les performances des modules.
    
    Args:
        modules (list): Liste des modules et leurs métriques
        
    Returns:
        plotly.graph_objects.Figure: Graphique généré
    """
    fig = go.Figure()
    
    categories = ['Efficacité', 'Taux d\'apprentissage', 'Complexité']
    
    for module in modules:
        fig.add_trace(go.Scatterpolar(
            r=[module["efficiency"], module["learning_rate"], module["complexity"]],
            theta=categories,
            fill='toself',
            name=module["name"]
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        title="Comparaison des modules ArcanShadow",
        height=450,
        showlegend=True
    )
    
    return fig

def create_learning_events_chart(data):
    """
    Crée un graphique des événements d'apprentissage.
    
    Args:
        data (pd.DataFrame): Données quotidiennes d'apprentissage
        
    Returns:
        plotly.graph_objects.Figure: Graphique généré
    """
    fig = go.Figure()
    
    # Ajouter les barres d'événements d'apprentissage
    fig.add_trace(go.Bar(
        x=data['date'],
        y=data['learning_events'],
        marker_color='rgba(94, 75, 139, 0.7)',
        name='Evenements apprentissage'
    ))
    
    # Mise en page
    fig.update_layout(
        title='Fréquence des événements d\'apprentissage',
        xaxis_title='Date',
        yaxis_title='Nombre d\'événements',
        plot_bgcolor='rgba(0,0,0,0.02)',
        height=350
    )
    
    return fig

def display_learning_system_tab():
    """
    Affiche l'onglet Système d'Apprentissage complet.
    """
    st.markdown("## 🧠 Système d'Apprentissage")
    st.markdown("Visualisation de l'évolution du système ArcanShadow et des processus d'apprentissage de ses modules.")
    
    # Génération des données d'apprentissage
    if "learning_data" not in st.session_state:
        st.session_state.learning_data = generate_learning_data()
    
    # Accès aux données
    data = st.session_state.learning_data["daily_metrics"]
    significant_events = st.session_state.learning_data["significant_events"]
    modules = st.session_state.learning_data["modules"]
    
    # En-tête avec métriques clés
    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
    
    with metrics_col1:
        current_accuracy = data['accuracy'].iloc[-1]
        st.metric(
            label="Précision actuelle",
            value=f"{current_accuracy:.1%}",
            delta=f"{current_accuracy - data['accuracy'].iloc[-7]:.1%} vs sem. précédente"
        )
    
    with metrics_col2:
        current_patterns = int(data['patterns'].iloc[-1])
        st.metric(
            label="Patterns identifiés",
            value=f"{current_patterns}",
            delta=f"{int(current_patterns - data['patterns'].iloc[-7])} nouveaux"
        )
    
    with metrics_col3:
        current_confidence = data['confidence'].iloc[-1]
        st.metric(
            label="Niveau de confiance",
            value=f"{current_confidence:.1%}",
            delta=f"{current_confidence - data['confidence'].iloc[-7]:.1%} vs sem. précédente"
        )
    
    # Graphiques d'évolution
    st.markdown("### Évolution des performances")
    
    # Graphique principal de précision et confiance
    accuracy_chart = create_accuracy_chart(data)
    st.plotly_chart(accuracy_chart, use_container_width=True)
    
    # Graphiques secondaires en colonnes
    col1, col2 = st.columns(2)
    
    with col1:
        patterns_chart = create_patterns_chart(data)
        st.plotly_chart(patterns_chart, use_container_width=True)
    
    with col2:
        events_chart = create_learning_events_chart(data)
        st.plotly_chart(events_chart, use_container_width=True)
    
    # Comparaison des modules
    st.markdown("### Performance des modules")
    
    # Radar chart des modules
    module_chart = create_module_radar_chart(modules)
    st.plotly_chart(module_chart, use_container_width=True)
    
    # Tableau des métriques par module
    module_df = pd.DataFrame([
        {
            "Module": m["name"],
            "Efficacité": f"{m['efficiency']:.0%}",
            "Taux d'apprentissage": f"{m['learning_rate']:.0%}",
            "Complexité": f"{m['complexity']:.0%}"
        } for m in modules
    ])
    
    st.dataframe(
        module_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Événements d'apprentissage significatifs
    st.markdown("### Événements d'apprentissage significatifs")
    
    for event in significant_events:
        event_date = event['date'].strftime("%d/%m/%Y")
        impact_color = "green" if event['impact'] > 0.06 else "orange"
        
        st.markdown(f"""
        <div style="padding: 15px; border-left: 4px solid #A377FE; background-color: rgba(45, 45, 68, 0.2); 
        margin-bottom: 15px; border-radius: 0 10px 10px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <h4 style="margin: 0; color: #A377FE;">{event['type']}</h4>
                <span style="color: gray;">{event_date}</span>
            </div>
            <p style="margin: 5px 0 10px 0;">{event['description']}</p>
            <div style="font-size: 0.9em;">
                <span>Impact: </span>
                <span style="color: {impact_color}; font-weight: bold;">+{event['impact']:.1%}</span>
                <span> sur la précision des prédictions</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def add_learning_system_tab(tab):
    """
    Ajoute l'onglet Système d'Apprentissage à l'application principale.
    
    Args:
        tab: Objet tab Streamlit
    """
    with tab:
        display_learning_system_tab()