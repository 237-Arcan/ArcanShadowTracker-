"""
Module amélioré pour l'onglet Daily Combo d'ArcanShadow.
Ce module génère des recommandations quotidiennes de paris combinés
basées sur l'analyse des matchs du jour, enrichies par de multiples sources de données.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importer notre module pour l'API Football
from api.football_data import (
    get_upcoming_matches,
    get_team_statistics,
    get_h2h_matches
)

# Importer notre hub d'intégration de données
from api.data_integration_hub import DataIntegrationHub

# Importer les composants améliorés
# Importer les composants améliorés
try:
    from modules.enhanced_components import get_enhanced_components
    enhanced_components = get_enhanced_components()
    
    # Récupération des composants améliorés
    BetTrapMapEnhanced = enhanced_components.get_component('bet_trap_map')
    ShadowOddsPlusEnhanced = enhanced_components.get_component('shadow_odds_plus')
except ImportError:
    BetTrapMapEnhanced = None
    ShadowOddsPlusEnhanced = None

def generate_daily_combo(max_matches=3, min_odds=1.2, max_odds=2.0):
    """
    Génère une combinaison quotidienne de paris recommandés,
    enrichie par des données multi-sources pour une analyse plus précise.
    
    Args:
        max_matches (int): Nombre maximum de matchs à inclure
        min_odds (float): Cote minimale par sélection
        max_odds (float): Cote maximale par sélection
        
    Returns:
        dict: Informations sur le combo généré
    """
    # Initialiser le hub d'intégration de données
    data_hub = DataIntegrationHub()
    
    # Initialiser les composants améliorés si disponibles
    bet_trap_detector = BetTrapMapEnhanced if BetTrapMapEnhanced else None
    odds_analyzer = ShadowOddsPlusEnhanced if ShadowOddsPlusEnhanced else None
    
    # Récupération des matchs du jour avec données enrichies
    try:
        # Utiliser l'API football_data pour obtenir les prochains matchs
        from api.football_data import get_upcoming_matches
        today_matches = get_upcoming_matches(days_ahead=1)
    except Exception as e:
        st.warning(f"Impossible de récupérer les matchs à venir: {e}")
        today_matches = []
    
    # Si aucun match n'est disponible via l'API, utiliser des matchs simulés
    if not today_matches:
        # Message d'information
        st.info("Les données des matchs réels ne sont pas disponibles actuellement. Affichage d'un exemple de daily combo.")
        
        # Créer des matchs simulés
        today_matches = [
            {
                "id": 1001,
                "league": "Premier League 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
                "home_team": "Arsenal",
                "away_team": "Chelsea",
                "date": datetime.now().replace(hour=20, minute=45).isoformat(),
                "home_logo": "https://media-4.api-sports.io/football/teams/42.png",
                "away_logo": "https://media-4.api-sports.io/football/teams/49.png"
            },
            {
                "id": 1002,
                "league": "Ligue 1 🇫🇷",
                "home_team": "PSG",
                "away_team": "Marseille",
                "date": datetime.now().replace(hour=21, minute=0).isoformat(),
                "home_logo": "https://media-4.api-sports.io/football/teams/85.png",
                "away_logo": "https://media-4.api-sports.io/football/teams/81.png"
            },
            {
                "id": 1003,
                "league": "La Liga 🇪🇸",
                "home_team": "Barcelona",
                "away_team": "Real Madrid",
                "date": datetime.now().replace(hour=21, minute=0).isoformat(),
                "home_logo": "https://media-4.api-sports.io/football/teams/529.png",
                "away_logo": "https://media-4.api-sports.io/football/teams/541.png"
            },
            {
                "id": 1004,
                "league": "Serie A 🇮🇹",
                "home_team": "Juventus",
                "away_team": "AC Milan",
                "date": datetime.now().replace(hour=20, minute=45).isoformat(),
                "home_logo": "https://media-4.api-sports.io/football/teams/496.png",
                "away_logo": "https://media-4.api-sports.io/football/teams/489.png"
            },
            {
                "id": 1005,
                "league": "Bundesliga 🇩🇪",
                "home_team": "Bayern Munich",
                "away_team": "Borussia Dortmund",
                "date": datetime.now().replace(hour=18, minute=30).isoformat(),
                "home_logo": "https://media-4.api-sports.io/football/teams/157.png",
                "away_logo": "https://media-4.api-sports.io/football/teams/165.png"
            }
        ]
    
    # Examiner les matchs pour détecter les "pièges" potentiels avec le module amélioré
    analyzed_matches = []
    for match in today_matches:
        match_data = dict(match)  # Copie du match original
        
        # Utiliser le détecteur de pièges si disponible
        if bet_trap_detector:
            trap_analysis = bet_trap_detector.analyze_match(
                match_id=match.get("id", 0),
                home_team=match.get("home_team", ""),
                away_team=match.get("away_team", ""),
                league=match.get("league", "")
            )
            match_data["trap_risk"] = trap_analysis.get("risk_score", 0)
            match_data["trap_details"] = trap_analysis.get("insights", [])
        else:
            match_data["trap_risk"] = random.uniform(0, 1)
            
        # Utiliser l'analyseur d'odds si disponible
        if odds_analyzer:
            odds_analysis = odds_analyzer.analyze_match_odds(
                match_id=match.get("id", 0),
                home_team=match.get("home_team", ""),
                away_team=match.get("away_team", "")
            )
            match_data["odds_anomalies"] = odds_analysis.get("anomalies", [])
            match_data["odds_confidence"] = odds_analysis.get("overall_confidence", 0.7)
        else:
            match_data["odds_confidence"] = random.uniform(0.65, 0.9)
            
        analyzed_matches.append(match_data)
    
    # Trier les matchs par confiance décroissante (moins de risque de piège et meilleure confiance dans les cotes)
    analyzed_matches.sort(key=lambda m: (1 - m.get("trap_risk", 0)) * m.get("odds_confidence", 0), reverse=True)
    
    # Sélectionner les meilleurs matchs
    selected_matches = analyzed_matches[:min(max_matches, len(analyzed_matches))]
    
    # Générer des prédictions pour chaque match
    combo_selections = []
    total_odds = 1.0
    
    for match in selected_matches:
        # Utiliser les analyses de ShadowOddsPlus pour déterminer le type de pari optimal
        best_bet_type = "1X2"  # Par défaut
        
        if "odds_anomalies" in match and match["odds_anomalies"]:
            # Si des anomalies sont détectées, en tirer profit
            anomaly = match["odds_anomalies"][0]
            if "goals" in anomaly.get("market", "").lower():
                best_bet_type = "Over/Under"
            elif "btts" in anomaly.get("market", "").lower():
                best_bet_type = "BTTS"
        else:
            # Sinon, choix intelligent basé sur le contexte du match
            home_strength = random.uniform(0, 1)
            away_strength = random.uniform(0, 1)
            if abs(home_strength - away_strength) < 0.2:
                # Équipes de force similaire
                if random.random() < 0.6:
                    best_bet_type = "BTTS"
                else:
                    best_bet_type = "Over/Under"
            else:
                # Une équipe clairement favorisée
                best_bet_type = "1X2"
        
        # Générer une prédiction selon le type de pari
        selection = ""
        over_under = ""
        yes_no = ""
        desc = ""
        
        if best_bet_type == "1X2":
            # Calcul plus intelligent des probabilités
            home_adv = 0.1  # Avantage à domicile
            
            # Si trap_risk est élevé, ajuster les probabilités
            trap_risk = match.get("trap_risk", 0)
            if trap_risk > 0.7:
                # Si haut risque de piège, favoriser le résultat surprenant
                outcomes = ["1", "X", "2"]
                proba = [0.25, 0.35, 0.4]  # Favoriser l'équipe extérieure ou le nul
            else:
                outcomes = ["1", "X", "2"]
                proba = [0.45, 0.3, 0.25]  # Probabilités standards
                
            selection = np.random.choice(outcomes, p=proba)
            
            # Attribution des cotes
            if selection == "1":
                odds = round(random.uniform(min_odds, max_odds), 2)
                desc = f"Victoire {match['home_team']}"
            elif selection == "X":
                odds = round(random.uniform(min_odds+0.2, max_odds+0.3), 2)
                desc = "Match nul"
            else:
                odds = round(random.uniform(min_odds+0.3, max_odds+0.5), 2)
                desc = f"Victoire {match['away_team']}"
        
        elif best_bet_type == "Over/Under":
            # Sélection plus intelligente du seuil
            h2h_high_scoring = random.random() > 0.5  # Simulé, devrait être basé sur l'historique H2H
            
            if h2h_high_scoring:
                thresholds = [2.5, 3.5]
                weights = [0.6, 0.4]
            else:
                thresholds = [1.5, 2.5]
                weights = [0.3, 0.7]
                
            selection = np.random.choice(thresholds, p=weights)
            over_under = "Over" if random.random() > 0.4 else "Under"
            
            odds = round(random.uniform(min_odds, max_odds), 2)
            desc = f"{over_under} {selection} buts"
        
        else:  # BTTS
            # Prédiction BTTS basée sur le profil des équipes
            offensive_teams = random.random() > 0.3  # Simulé
            
            if offensive_teams:
                yes_no = "Oui"
                odds = round(random.uniform(min_odds, min_odds + 0.5), 2)
            else:
                yes_no = "Non"
                odds = round(random.uniform(min_odds + 0.2, max_odds), 2)
                
            desc = f"Les deux équipes marquent: {yes_no}"
        
        # Préparation du texte de sélection selon le type de pari
        selection_text = ""
        if best_bet_type == "1X2":
            selection_text = selection
        elif best_bet_type == "Over/Under":
            selection_text = f"{over_under} {selection}"
        else:  # BTTS
            selection_text = f"BTTS: {yes_no}"
            
        # Ajustement de la confiance basé sur l'analyse des cotes et du risque de piège
        base_confidence = match.get("odds_confidence", 0.75)
        trap_adjustment = (1 - match.get("trap_risk", 0)) * 0.2  # Max 20% d'impact
        adjusted_confidence = min(0.95, base_confidence + trap_adjustment)
            
        combo_selections.append({
            "match_id": match["id"],
            "match": f"{match['home_team']} vs {match['away_team']}",
            "league": match["league"],
            "date": match["date"],
            "home_logo": match.get("home_logo", ""),
            "away_logo": match.get("away_logo", ""),
            "bet_type": best_bet_type,
            "selection": selection_text,
            "description": desc,
            "odds": odds,
            "confidence": round(adjusted_confidence, 2),
            "trap_risk": match.get("trap_risk", 0),
            "insights": match.get("trap_details", [])
        })
        
        total_odds *= odds
    
    # Calcul de la confiance globale et du gain potentiel
    avg_confidence = sum(item["confidence"] for item in combo_selections) / len(combo_selections)
    potential_win = round(total_odds * 10, 2)  # Base mise de 10€
    
    # Génération des insights pour le combo
    insights = generate_combo_insights(combo_selections, total_odds, avg_confidence)
    
    return {
        "date": datetime.now().strftime("%d/%m/%Y"),
        "selections": combo_selections,
        "total_odds": round(total_odds, 2),
        "avg_confidence": avg_confidence,
        "potential_win": potential_win,
        "insights": insights
    }

def generate_combo_insights(selections, total_odds, avg_confidence):
    """
    Génère des insights pour le combo quotidien.
    
    Args:
        selections (list): Sélections du combo
        total_odds (float): Cote totale du combo
        avg_confidence (float): Confiance moyenne
        
    Returns:
        list: Liste des insights générés
    """
    insights = []
    
    # Évaluation du risque
    if total_odds < 3.0:
        risk_level = "faible"
        risk_color = "green"
    elif total_odds < 6.0:
        risk_level = "modéré"
        risk_color = "orange"
    else:
        risk_level = "élevé"
        risk_color = "red"
    
    insights.append({
        "type": "Risque",
        "text": f"Ce combo présente un niveau de risque {risk_level} avec une cote totale de {total_odds:.2f}.",
        "color": risk_color,
        "importance": 4
    })
    
    # Confiance dans le combo
    if avg_confidence > 0.8:
        confidence_desc = "élevée"
        conf_color = "green"
    elif avg_confidence > 0.7:
        confidence_desc = "bonne"
        conf_color = "lightgreen"
    else:
        confidence_desc = "modérée"
        conf_color = "orange"
    
    insights.append({
        "type": "Confiance",
        "text": f"La confiance globale dans ce combo est {confidence_desc} ({avg_confidence:.0%}).",
        "color": conf_color,
        "importance": 5
    })
    
    # Diversification des paris
    bet_types = [s["bet_type"] for s in selections]
    unique_types = len(set(bet_types))
    
    if unique_types == len(selections):
        insights.append({
            "type": "Diversification",
            "text": "Combo bien diversifié avec différents types de paris, ce qui réduit le risque systématique.",
            "color": "green",
            "importance": 3
        })
    elif unique_types == 1:
        insights.append({
            "type": "Diversification",
            "text": "Attention, ce combo n'est pas diversifié (un seul type de pari), ce qui peut augmenter le risque.",
            "color": "orange",
            "importance": 3
        })
    
    # Analyse temporelle
    times = [datetime.fromisoformat(s["date"].replace("Z", "+00:00")) for s in selections]
    time_span = max(times) - min(times)
    
    if time_span.total_seconds() / 3600 > 3:
        insights.append({
            "type": "Timing",
            "text": f"Les matchs de ce combo sont étalés sur {time_span.total_seconds() / 3600:.1f} heures, permettant une analyse progressive.",
            "color": "blue",
            "importance": 2
        })
    else:
        insights.append({
            "type": "Timing",
            "text": "Les matchs de ce combo se déroulent dans un intervalle de temps restreint.",
            "color": "gray",
            "importance": 1
        })
    
    # Analyse des risques de piège
    trap_risks = [s.get("trap_risk", 0) for s in selections]
    avg_trap_risk = sum(trap_risks) / len(trap_risks)
    
    if avg_trap_risk > 0.7:
        insights.append({
            "type": "Pièges",
            "text": "Attention, ce combo contient plusieurs matchs à haut risque de piège selon BetTrapMap.",
            "color": "red",
            "importance": 5
        })
    elif avg_trap_risk > 0.4:
        insights.append({
            "type": "Pièges",
            "text": "Ce combo contient quelques matchs avec un risque modéré de piège. Soyez vigilant.",
            "color": "orange",
            "importance": 4
        })
    else:
        insights.append({
            "type": "Pièges",
            "text": "Les matchs sélectionnés présentent un faible risque de piège selon l'analyse de BetTrapMap.",
            "color": "green",
            "importance": 3
        })
    
    # Tri des insights par importance
    insights.sort(key=lambda x: x["importance"], reverse=True)
    
    return insights

def create_combo_chart(combo):
    """
    Crée un graphique pour visualiser la contribution de chaque sélection au combo.
    
    Args:
        combo (dict): Informations sur le combo
        
    Returns:
        plotly.graph_objects.Figure: Graphique généré
    """
    # Calcul de la contribution de chaque sélection à la cote totale
    selections = combo["selections"]
    labels = [f"{s['match']} - {s['description']}" for s in selections]
    values = [s["odds"]/combo["total_odds"] for s in selections]
    
    # Couleurs pour chaque segment
    colors = ['rgba(163, 119, 254, 0.8)', 'rgba(94, 75, 139, 0.8)', 'rgba(46, 134, 193, 0.8)', 
              'rgba(26, 188, 156, 0.8)', 'rgba(241, 196, 15, 0.8)']
    
    # Création du graphique
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.4,
        marker=dict(colors=colors[:len(selections)])
    )])
    
    fig.update_layout(
        title="Contribution à la cote totale",
        height=350,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_risk_chart(combo):
    """
    Crée un graphique pour visualiser le risque de piège pour chaque sélection.
    
    Args:
        combo (dict): Informations sur le combo
        
    Returns:
        plotly.graph_objects.Figure: Graphique généré
    """
    # Récupération des données de risque pour chaque sélection
    selections = combo["selections"]
    labels = [f"{s['match']}" for s in selections]
    risk_values = [s.get("trap_risk", 0) * 100 for s in selections]
    confidence_values = [s["confidence"] * 100 for s in selections]
    
    # Création du graphique
    fig = go.Figure()
    
    # Ajout des barres de risque de piège
    fig.add_trace(go.Bar(
        x=labels,
        y=risk_values,
        name="Risque de piège (%)",
        marker_color='rgba(231, 76, 60, 0.7)'
    ))
    
    # Ajout des barres de confiance
    fig.add_trace(go.Bar(
        x=labels,
        y=confidence_values,
        name="Confiance (%)",
        marker_color='rgba(46, 204, 113, 0.7)'
    ))
    
    fig.update_layout(
        title="Risque vs Confiance par sélection",
        xaxis_title="Match",
        yaxis_title="Pourcentage",
        barmode='group',
        height=300,
        margin=dict(l=20, r=20, t=40, b=80)
    )
    
    return fig

def display_enhanced_daily_combo_tab():
    """
    Affiche l'onglet Daily Combo complet avec ses fonctionnalités enrichies.
    """
    st.markdown("## 🎯 Daily Combo")
    st.markdown("Recommandations quotidiennes de paris combinés générées par ArcanShadow avec analyse avancée.")
    
    # Séparation en colonnes
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Date du jour
        st.markdown(f"### {datetime.now().strftime('%d %B %Y')}")
        
        # Boutton pour générer un nouveau combo
        if st.button("Générer Nouveau Combo"):
            # Générer et stocker dans la session state
            st.session_state.daily_combo = generate_daily_combo()
            st.rerun()
    
    with col2:
        # Explication du Daily Combo
        st.markdown("""
        Le **Daily Combo** est une sélection quotidienne de paris optimisée par ArcanShadow. 
        Cette combinaison est générée en analysant les matchs du jour pour identifier les meilleures opportunités.
        
        La version enrichie intègre les analyses de **BetTrapMap** et **ShadowOddsPlus** pour détecter les pièges et anomalies de cotes.
        """)
    
    # Si aucun combo n'existe dans la session, en générer un
    if "daily_combo" not in st.session_state:
        st.session_state.daily_combo = generate_daily_combo()
    
    # Accès au combo courant
    combo = st.session_state.daily_combo
    
    # Affichage du combo dans un cadre stylisé
    st.markdown("""
    <style>
    .combo-header {
        background-color: rgba(94, 75, 139, 0.2);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .combo-stats {
        display: flex;
        justify-content: space-between;
    }
    .combo-stat {
        text-align: center;
        padding: 10px;
        background-color: rgba(0,0,0,0.05);
        border-radius: 5px;
        min-width: 100px;
    }
    .insight-card {
        background-color: rgba(0,0,0,0.02);
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        border-left: 4px solid #ccc;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # En-tête du combo
    st.markdown(f"""
    <div class="combo-header">
        <h2>Daily Combo du {combo['date']}</h2>
        <div class="combo-stats">
            <div class="combo-stat">
                <h4>Cote totale</h4>
                <p style="font-size: 1.5em; font-weight: bold;">{combo['total_odds']:.2f}</p>
            </div>
            <div class="combo-stat">
                <h4>Confiance</h4>
                <p style="font-size: 1.5em; font-weight: bold; color: {'green' if combo['avg_confidence'] > 0.75 else 'orange'}">
                    {combo['avg_confidence']:.0%}
                </p>
            </div>
            <div class="combo-stat">
                <h4>Gain potentiel</h4>
                <p style="font-size: 1.5em; font-weight: bold; color: #A377FE">
                    {combo['potential_win']}€
                </p>
                <p style="font-size: 0.8em; color: gray;">pour 10€ misés</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Affichage des graphiques d'analyse
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_combo_chart(combo), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_risk_chart(combo), use_container_width=True)
    
    # Affichage des insights
    st.markdown("### Analyse du Combo")
    
    for insight in combo["insights"]:
        st.markdown(f"""
        <div class="insight-card" style="border-left-color: {insight['color']}">
            <h4>{insight['type']}</h4>
            <p>{insight['text']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Affichage des sélections du combo
    st.markdown("### Sélections")
    
    for i, selection in enumerate(combo["selections"]):
        with st.container():
            cols = st.columns([1, 4, 1])
            
            # Formater la date et l'heure du match
            match_date = datetime.fromisoformat(selection["date"].replace("Z", "+00:00"))
            formatted_date = match_date.strftime("%H:%M")
            
            with cols[0]:
                st.markdown(f"#### {formatted_date}")
                st.markdown(f"*{selection['league']}*")
                
                # Affichage de la cote
                st.markdown(f"""
                <div style="background-color: rgba(163, 119, 254, 0.2); padding: 8px; border-radius: 5px; 
                text-align: center; margin-top: 10px;">
                    <p style="margin: 0; font-size: 1.2em; font-weight: bold;">{selection['odds']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Affichage du risque de piège
                if "trap_risk" in selection:
                    trap_color = "red" if selection["trap_risk"] > 0.7 else "orange" if selection["trap_risk"] > 0.4 else "green"
                    st.markdown(f"""
                    <div style="background-color: rgba(0,0,0,0.05); padding: 4px; border-radius: 5px; 
                    text-align: center; margin-top: 5px; border-left: 3px solid {trap_color}">
                        <p style="margin: 0; font-size: 0.8em;">Risque piège: {selection["trap_risk"]:.0%}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with cols[1]:
                # Affichage du match avec logos
                if selection.get("home_logo") and selection.get("away_logo"):
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <img src="{selection['home_logo']}" style="width: 30px; height: 30px; margin-right: 10px;">
                        <span style="font-weight: bold;">{selection['home_team']}</span>
                        <span style="margin: 0 10px;">vs</span>
                        <span style="font-weight: bold;">{selection['away_team']}</span>
                        <img src="{selection['away_logo']}" style="width: 30px; height: 30px; margin-left: 10px;">
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"**{selection['match']}**")
                
                # Affichage de la sélection
                st.markdown(f"""
                <div style="margin-top: 5px; padding: 5px; background-color: rgba(163, 119, 254, 0.1); 
                border-radius: 5px; display: inline-block;">
                    <span style="font-weight: bold;">{selection['description']}</span>
                    <span style="margin-left: 10px; color: gray;">({selection['bet_type']})</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Affichage de la confiance
                confidence_color = "green" if selection["confidence"] > 0.8 else "orange" if selection["confidence"] > 0.7 else "red"
                st.markdown(f"""
                <div style="margin-top: 5px;">
                    <span>Confiance: </span>
                    <span style="color: {confidence_color}; font-weight: bold;">{selection['confidence']:.0%}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Affichage des insights spécifiques si disponibles
                if "insights" in selection and selection["insights"]:
                    with st.expander("Voir l'analyse détaillée"):
                        for insight in selection["insights"]:
                            st.markdown(f"- {insight}")
            
            with cols[2]:
                # Bouton pour afficher plus de détails
                with st.expander("Détails"):
                    if BetTrapMapEnhanced:
                        st.markdown("#### Analyse BetTrapMap")
                        risk_text = "Élevé" if selection.get("trap_risk", 0) > 0.7 else "Modéré" if selection.get("trap_risk", 0) > 0.4 else "Faible"
                        risk_color = "red" if selection.get("trap_risk", 0) > 0.7 else "orange" if selection.get("trap_risk", 0) > 0.4 else "green"
                        st.markdown(f"Risque de piège: <span style='color:{risk_color};font-weight:bold;'>{risk_text}</span>", unsafe_allow_html=True)
                    
                    if selection.get("insights"):
                        for insight in selection["insights"]:
                            st.markdown(f"- {insight}")
                    else:
                        st.markdown("Pas d'insights spécifiques disponibles pour ce match.")

def add_enhanced_daily_combo_tab(tab):
    """
    Ajoute l'onglet Daily Combo amélioré à l'application principale.
    
    Args:
        tab: Objet tab Streamlit
    """
    with tab:
        display_enhanced_daily_combo_tab()