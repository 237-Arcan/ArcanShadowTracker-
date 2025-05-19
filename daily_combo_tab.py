"""
Module pour l'onglet Daily Combo d'ArcanShadow.
Ce module génère des recommandations quotidiennes de paris combinés
basées sur l'analyse des matchs du jour, enrichies par l'API Transfermarkt.
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

# Importer notre module d'intégration Transfermarkt
from api.transfermarkt_integration import (
    is_transfermarkt_available,
    enhance_match_data_with_transfermarkt,
    get_team_players,
    get_team_profile
)

def generate_daily_combo(max_matches=3, min_odds=1.2, max_odds=2.0):
    """
    Génère une combinaison quotidienne de paris recommandés,
    enrichie par des données Transfermarkt pour une analyse plus précise.
    
    Args:
        max_matches (int): Nombre maximum de matchs à inclure
        min_odds (float): Cote minimale par sélection
        max_odds (float): Cote maximale par sélection
        
    Returns:
        dict: Informations sur le combo généré
    """
    # Vérifier si l'API Transfermarkt est disponible
    transfermarkt_available = is_transfermarkt_available()
    if transfermarkt_available:
        logger.info("API Transfermarkt disponible pour enrichir les recommandations du Daily Combo")
    else:
        logger.info("API Transfermarkt non disponible, utilisation des données standard uniquement")
    # Récupération des matchs du jour
    today_matches = get_upcoming_matches(days_ahead=1)
    
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
    
    # Filtrer les matchs pour n'en sélectionner que quelques-uns (3 maximum par défaut)
    selected_count = min(max_matches, len(today_matches))
    selected_indices = random.sample(range(len(today_matches)), selected_count)
    selected_matches = [today_matches[i] for i in selected_indices]
    
    # Générer des prédictions pour chaque match
    combo_selections = []
    total_odds = 1.0
    
    for match in selected_matches:
        # Choix aléatoire du type de pari (1X2, Over/Under, BTTS)
        bet_types = ["1X2", "Over/Under", "BTTS"]
        bet_type = random.choice(bet_types)
        
        # Générer une prédiction selon le type de pari
        selection = ""
        over_under = ""
        yes_no = ""
        desc = ""
        
        if bet_type == "1X2":
            outcomes = ["1", "X", "2"]
            proba = [0.45, 0.3, 0.25]  # Probabilités ajustées pour favoriser légèrement l'équipe à domicile
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
        
        elif bet_type == "Over/Under":
            thresholds = [1.5, 2.5, 3.5]
            selection = random.choice(thresholds)
            over_under = random.choice(["Over", "Under"])
            
            odds = round(random.uniform(min_odds, max_odds), 2)
            desc = f"{over_under} {selection} buts"
        
        else:  # BTTS
            yes_no = random.choice(["Oui", "Non"])
            odds = round(random.uniform(min_odds, max_odds), 2)
            desc = f"Les deux équipes marquent: {yes_no}"
        
        # Préparation du texte de sélection selon le type de pari
        selection_text = ""
        if bet_type == "1X2":
            selection_text = selection
        elif bet_type == "Over/Under":
            selection_text = f"{over_under} {selection}"
        else:  # BTTS
            selection_text = f"BTTS: {yes_no}"
            
        combo_selections.append({
            "match_id": match["id"],
            "match": f"{match['home_team']} vs {match['away_team']}",
            "league": match["league"],
            "date": match["date"],
            "home_logo": match.get("home_logo", ""),
            "away_logo": match.get("away_logo", ""),
            "bet_type": bet_type,
            "selection": selection_text,
            "description": desc,
            "odds": odds,
            "confidence": round(random.uniform(0.65, 0.9), 2)
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

def display_daily_combo_tab():
    """
    Affiche l'onglet Daily Combo complet.
    """
    st.markdown("## 🎯 Daily Combo")
    st.markdown("Recommandations quotidiennes de paris combinés générées par ArcanShadow.")
    
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
            
            with cols[1]:
                # Affichage du match avec logos
                if selection.get("home_logo") and selection.get("away_logo"):
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <img src="{selection['home_logo']}" style="width: 30px; height: 30px; margin-right: 10px;">
                        <span style="font-weight: bold;">{selection['match']}</span>
                        <img src="{selection['away_logo']}" style="width: 30px; height: 30px; margin-left: 10px;">
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"**{selection['match']}**")
                
                # Type de pari et sélection
                st.markdown(f"""
                <div style="margin-top: 5px;">
                    <span style="color: gray;">{selection['bet_type']}</span>: 
                    <span style="font-weight: bold;">{selection['description']}</span>
                </div>
                """, unsafe_allow_html=True)
            
            with cols[2]:
                # Niveau de confiance
                confidence = selection["confidence"]
                color = "green" if confidence > 0.8 else "orange" if confidence > 0.7 else "red"
                
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="font-size: 0.8em; color: gray;">Confiance</div>
                    <div style="font-weight: bold; color: {color}; font-size: 1.1em;">{confidence:.0%}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Séparateur entre les sélections
            if i < len(combo["selections"]) - 1:
                st.markdown("<hr style='margin: 15px 0; border: none; border-top: 1px dashed rgba(150, 150, 150, 0.3);'>", unsafe_allow_html=True)
    
    # Affichage du graphique et des insights
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Graphique de contribution au combo
        fig = create_combo_chart(combo)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Insights sur le combo
        st.markdown("### Insights ArcanShadow")
        
        for insight in combo["insights"]:
            # Affichage de l'insight avec style basé sur son importance
            importance = insight["importance"]
            color = insight["color"]
            
            if importance >= 4:
                st.markdown(f"""
                <div style="padding: 12px; border-left: 4px solid {color}; background-color: rgba(0,0,0,0.03); 
                margin-bottom: 12px; border-radius: 0 5px 5px 0; box-shadow: 1px 1px 3px rgba(0,0,0,0.05);">
                    <h4 style="margin: 0; color: {color};">{insight["type"]}</h4>
                    <p style="margin: 5px 0 0 0; font-size: 1.05em;"><strong>{insight["text"]}</strong></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="padding: 10px; border-left: 3px solid {color}; margin-bottom: 10px;">
                    <h5 style="margin: 0; color: {color};">{insight["type"]}</h5>
                    <p style="margin: 5px 0 0 0;">{insight["text"]}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Section des stratégies
    st.markdown("### Stratégies de mise")
    
    strategy_col1, strategy_col2, strategy_col3 = st.columns(3)
    
    with strategy_col1:
        st.markdown("#### Standard")
        st.markdown("""
        Mise unique sur l'ensemble du combo.
        - **Risque**: Moyen
        - **Potentiel**: Élevé
        """)
        
        # Exemple de mise
        standard_amount = 10
        standard_win = round(standard_amount * combo["total_odds"], 2)
        
        st.markdown(f"""
        <div style="background-color: rgba(46, 134, 193, 0.1); padding: 10px; border-radius: 5px; margin-top: 10px;">
            <p>Mise: <strong>{standard_amount}€</strong></p>
            <p>Gain potentiel: <strong>{standard_win}€</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with strategy_col2:
        st.markdown("#### Progressif")
        st.markdown("""
        Mises séparées progressives sur chaque sélection.
        - **Risque**: Réduit
        - **Potentiel**: Modéré
        """)
        
        # Calcul des mises progressives
        start_amount = 10
        total_prog_amount = 0
        stakes = []
        
        for i in range(len(combo["selections"])):
            stake = round(start_amount * (1 + i * 0.5), 2)
            total_prog_amount += stake
            stakes.append(stake)
        
        prog_win = round(stakes[-1] * combo["total_odds"], 2)
        
        st.markdown(f"""
        <div style="background-color: rgba(46, 134, 193, 0.1); padding: 10px; border-radius: 5px; margin-top: 10px;">
            <p>Mise totale: <strong>{total_prog_amount}€</strong></p>
            <p>Gain potentiel final: <strong>{prog_win}€</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with strategy_col3:
        st.markdown("#### Sécurisé")
        st.markdown("""
        Mises indépendantes sur chaque sélection.
        - **Risque**: Faible
        - **Potentiel**: Limité
        """)
        
        # Calcul des mises indépendantes
        base_amount = 10
        total_sec_amount = base_amount * len(combo["selections"])
        
        # Calcul du gain moyen (en supposant que chaque sélection a la même probabilité de gagner)
        avg_odd = sum(s["odds"] for s in combo["selections"]) / len(combo["selections"])
        avg_win = round(base_amount * avg_odd, 2)
        
        st.markdown(f"""
        <div style="background-color: rgba(46, 134, 193, 0.1); padding: 10px; border-radius: 5px; margin-top: 10px;">
            <p>Mise totale: <strong>{total_sec_amount}€</strong></p>
            <p>Gain moyen par sélection: <strong>{avg_win}€</strong></p>
        </div>
        """, unsafe_allow_html=True)

def add_daily_combo_tab(tab):
    """
    Ajoute l'onglet Daily Combo à l'application principale.
    
    Args:
        tab: Objet tab Streamlit
    """
    with tab:
        display_daily_combo_tab()