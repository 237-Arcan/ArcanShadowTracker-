import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import os
import matplotlib.pyplot as plt
import sys
import requests
import random

# Importer notre fonction pour obtenir des matchs réels
from get_real_matches import get_football_api_matches

# Configuration de la page
st.set_page_config(
    page_title="ArcanShadow",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonction pour charger le CSS personnalisé
def load_custom_css():
    """Charge le fichier CSS personnalisé pour transformer l'interface ArcanShadow"""
    try:
        with open('.streamlit/style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erreur lors du chargement du CSS: {e}")

# Fonction d'aide pour les traductions
def t(key, **format_args):
    """Helper function to get text in the current language"""
    # Placeholder pour la fonction de traduction réelle
    translations = {
        "app_title": {"en": "ArcanShadow", "fr": "ArcanShadow"},
        "welcome_message": {
            "en": "Welcome to the future of sports prediction",
            "fr": "Bienvenue dans le futur de la prédiction sportive"
        },
        "todays_matches": {
            "en": "Today's Matches",
            "fr": "Matchs du jour"
        },
        "featured_matches": {
            "en": "Featured Matches",
            "fr": "Matchs à la une"
        },
        "predictions": {
            "en": "Predictions",
            "fr": "Prédictions"
        },
        "analysis": {
            "en": "Analysis",
            "fr": "Analyse"
        },
        "esoteric_panel": {
            "en": "Esoteric Insights",
            "fr": "Aperçus Ésotériques"
        }
    }
    
    # Langue par défaut (français)
    lang = "fr"
    
    # Obtenir la traduction
    if key in translations and lang in translations[key]:
        text = translations[key][lang]
        # Appliquer les arguments de format s'il y en a
        if format_args:
            text = text.format(**format_args)
        return text
    return key

# Charger notre CSS personnalisé
load_custom_css()

# Fonction simulée pour obtenir des données d'exemple
def get_sample_data():
    leagues = ["Ligue 1", "Premier League", "LaLiga", "Bundesliga", "Serie A"]
    teams = {
        "Ligue 1": ["PSG", "Marseille", "Lyon", "Monaco", "Lille"],
        "Premier League": ["Manchester City", "Liverpool", "Arsenal", "Chelsea", "Tottenham"],
        "LaLiga": ["Real Madrid", "Barcelona", "Atletico Madrid", "Sevilla", "Valencia"],
        "Bundesliga": ["Bayern Munich", "Dortmund", "RB Leipzig", "Leverkusen", "Frankfurt"],
        "Serie A": ["Inter", "Milan", "Juventus", "Napoli", "Roma"]
    }
    
    matches = []
    for league in leagues:
        for i in range(3):  # 3 matches par ligue
            home_idx = np.random.randint(0, len(teams[league]))
            away_idx = (home_idx + 1 + np.random.randint(0, len(teams[league])-1)) % len(teams[league])
            
            home_team = teams[league][home_idx]
            away_team = teams[league][away_idx]
            
            # Cotes générées aléatoirement
            home_odds = round(1.5 + np.random.random() * 2, 2)
            draw_odds = round(3.0 + np.random.random() * 1.5, 2)
            away_odds = round(2.0 + np.random.random() * 3.5, 2)
            
            # Probabilités dérivées des cotes
            total = 1/home_odds + 1/draw_odds + 1/away_odds
            home_prob = round((1/home_odds) / total, 2)
            draw_prob = round((1/draw_odds) / total, 2)
            away_prob = round((1/away_odds) / total, 2)
            
            # Générer l'heure de coup d'envoi dans les 12 prochaines heures
            hours_ahead = np.random.randint(1, 12)
            match_time = (datetime.now() + timedelta(hours=hours_ahead)).strftime("%H:%M")
            
            # Pays pour les codes de drapeaux
            countries = {
                "Ligue 1": "fr", 
                "Premier League": "gb", 
                "LaLiga": "es", 
                "Bundesliga": "de", 
                "Serie A": "it"
            }
            
            match = {
                "league": league,
                "country": countries[league],
                "country_code": countries[league],
                "home_team": home_team,
                "away_team": away_team,
                "kickoff_time": match_time,
                "home_odds": home_odds,
                "draw_odds": draw_odds,
                "away_odds": away_odds,
                "home_prob": home_prob,
                "draw_prob": draw_prob,
                "away_prob": away_prob
            }
            matches.append(match)
    
    # Marquer certains matchs comme importants
    featured_indices = np.random.choice(range(len(matches)), 3, replace=False)
    featured_matches = [matches[i] for i in featured_indices]
    
    # Retirer les matchs à la une de la liste principale pour éviter les doublons
    remaining_matches = [match for i, match in enumerate(matches) if i not in featured_indices]
    
    return featured_matches, remaining_matches

# Création de données simulées
featured_matches, today_matches = get_sample_data()

# Interface principale
st.title(f"🔮 {t('app_title')}")
st.markdown(f"### {t('welcome_message')}")

# Simuler un nombre de notifications non lues
if 'notification_count' not in st.session_state:
    st.session_state.notification_count = 3

# Créer les onglets spécifiques au système ArcanShadow
tabs = st.tabs([
    "🔮 Prédictions",
    "🔔 Performance Notifications", 
    "🎯 Daily Combo", 
    "💡 Smart Market Recommendations", 
    "🧠 Système d'Apprentissage",
    f"📬 Notifications ({st.session_state.notification_count})"
])

with tabs[0]:  # Prédictions
    st.markdown("## 🔮 Prédictions")
    st.markdown("Analysez les prochains matchs avec notre technologie de prédiction exclusive.")
    
    # Section des prédictions avancées
    st.markdown("### 🔮 Prédictions par Intelligence Artificielle")
    
    st.markdown("""
    <div style="padding: 15px; border-radius: 10px; background: linear-gradient(135deg, rgba(8, 15, 40, 0.7), rgba(17, 23, 64, 0.6)); 
                border: 1px solid rgba(81, 99, 149, 0.3); margin-bottom: 15px;">
        <div style="font-size: 16px; font-weight: bold; color: #05d9e8; margin-bottom: 10px;">
            Système ArcanShadow - Prédictions Avancées
        </div>
        <p style="color: rgba(255, 255, 255, 0.8); font-size: 14px; line-height: 1.6;">
            Le système de prédiction d'ArcanShadow combine analyse statistique approfondie et algorithmes d'apprentissage automatique.
            Notre intelligence artificielle analyse des milliers de variables pour chaque match et génère des prédictions de haute précision.
            <br><br>
            Les résultats sont constamment évalués et le système s'améliore en permanence pour optimiser la précision des prédictions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Structure pour les matchs en direct
    if 'live_matches' not in st.session_state:
        st.session_state.live_matches = [
            {"id": 1, "home": "PSG", "away": "Lyon", "league": "Ligue 1", "time": "20:45", "status": "En direct", "minute": "37'", "score": "1-0"},
            {"id": 2, "home": "Liverpool", "away": "Arsenal", "league": "Premier League", "time": "17:30", "status": "En direct", "minute": "68'", "score": "2-1"},
            {"id": 3, "home": "Bayern Munich", "away": "Dortmund", "league": "Bundesliga", "time": "18:30", "status": "En direct", "minute": "52'", "score": "0-0"}
        ]
    
    # Structure pour gérer les matchs surveillés en direct
    if 'sentinel_monitored_live_matches' not in st.session_state:
        st.session_state.sentinel_monitored_live_matches = []
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Tableau des matchs en direct disponibles
        st.markdown("#### 🔴 Matchs actuellement en direct")
        
        for match in st.session_state.live_matches:
            is_monitored = any(m['id'] == match['id'] for m in st.session_state.sentinel_monitored_live_matches)
            status_color = "#01ff80" if is_monitored else "rgba(255, 255, 255, 0.8)"
            status_text = "🟢 Surveillé en direct" if is_monitored else "⚪ Disponible"
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; 
                      padding: 12px; border-radius: 5px; margin-bottom: 15px; 
                      background: rgba(255, 51, 100, 0.1); border: 1px solid rgba(255, 51, 100, 0.2);">
                <div>
                    <div style="font-weight: bold; font-size: 16px; color: white;">
                        {match['home']} {match['score']} {match['away']}
                    </div>
                    <div style="font-size: 13px; color: #ff3364; font-weight: bold; margin-top: 4px;">
                        {match['minute']} • EN DIRECT
                    </div>
                    <div style="font-size: 12px; color: rgba(255, 255, 255, 0.6); margin-top: 2px;">
                        {match['league']}
                    </div>
                </div>
                <div style="font-size: 13px; color: {status_color};">
                    {status_text}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Pour chaque match, ajouter des boutons d'action
            col_a, col_b = st.columns([3, 2])
            with col_a:
                if not is_monitored:
                    if st.button(f"Activer surveillance en direct", key=f"activate_live_{match['id']}"):
                        # Configuration de surveillance
                        surveillance_config = {
                            "id": match['id'],
                            "home": match['home'],
                            "away": match['away'],
                            "league": match['league'],
                            "minute": match['minute'],
                            "score": match['score'],
                            "monitoring_level": "Maximum",  # Plus haut niveau pour les matchs en direct
                            "modules": ["ShadowMomentum", "LineTrap", "KarmicFlow", "MirrorPhase", "BetPulse"],
                            "activated_at": "2025-05-17 " + datetime.now().strftime("%H:%M:%S"),
                            "alert_threshold": 5  # Seuil plus bas pour être plus réactif aux matchs en direct
                        }
                        st.session_state.sentinel_monitored_live_matches.append(surveillance_config)
                        
                        # Ajouter une notification d'activation
                        if 'notifications' in st.session_state:
                            new_notif = {
                                "id": len(st.session_state.notifications) + 1,
                                "type": "sentinel",
                                "title": f"🔴 ArcanSentinel activé en DIRECT: {match['home']} vs {match['away']}",
                                "message": f"Surveillance instantanée lancée sur le match en direct {match['home']} vs {match['away']} ({match['minute']}). Les analyses seront envoyées en temps réel.",
                                "timestamp": datetime.now().strftime("2025-05-17 %H:%M:%S"),
                                "read": False,
                                "priority": "urgent"
                            }
                            st.session_state.notifications.append(new_notif)
                            st.session_state.notification_count += 1
                            st.rerun()
                else:
                    if st.button(f"Désactiver la surveillance", key=f"deactivate_live_{match['id']}"):
                        # Retirer la surveillance
                        st.session_state.sentinel_monitored_live_matches = [
                            m for m in st.session_state.sentinel_monitored_live_matches if m['id'] != match['id']
                        ]
                        
                        # Ajouter une notification de désactivation
                        if 'notifications' in st.session_state:
                            new_notif = {
                                "id": len(st.session_state.notifications) + 1,
                                "type": "sentinel",
                                "title": f"⚪ ArcanSentinel désactivé: {match['home']} vs {match['away']}",
                                "message": f"La surveillance en direct du match {match['home']} vs {match['away']} a été désactivée. Les dernières analyses ont été sauvegardées.",
                                "timestamp": datetime.now().strftime("2025-05-17 %H:%M:%S"),
                                "read": False,
                                "priority": "medium"
                            }
                            st.session_state.notifications.append(new_notif)
                            st.session_state.notification_count += 1
                            st.rerun()
    
    with col2:
        # Configuration d'ArcanSentinel
        st.markdown("#### ⚙️ Configuration Sentinel")
        
        monitoring_style = st.radio(
            "Style de surveillance:",
            ["Standard", "Aggressif", "Ultra-réactif"],
            index=2,
            help="Détermine la sensibilité des alertes et la fréquence d'analyse"
        )
        
        notification_lvl = st.select_slider(
            "Niveau de notification:",
            options=["Minimal", "Normal", "Détaillé", "Complet"],
            value="Détaillé",
            help="Contrôle la quantité d'informations dans les alertes"
        )
        
        st.markdown("##### Modules Sentinel actifs:")
        col_m1, col_m2 = st.columns(2)
        
        with col_m1:
            st.checkbox("ShadowMomentum", value=True)
            st.checkbox("LineTrap", value=True)
            st.checkbox("KarmicFlow", value=True)
        
        with col_m2:
            st.checkbox("MirrorPhase", value=True)
            st.checkbox("BetPulse", value=True)
            st.checkbox("QuantumVar", value=False)
            
    # Statistiques de surveillance
    st.markdown("### 📊 Statistiques de Surveillance")
    
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    
    with col_s1:
        st.metric(label="Matchs surveillés", value=f"{len(st.session_state.sentinel_monitored_live_matches)}/3", delta="+1")
    
    with col_s2:
        st.metric(label="Alertes générées", value="14", delta="+3")
    
    with col_s3:
        st.metric(label="Précision des alertes", value="92%", delta="+4%")
    
    with col_s4:
        st.metric(label="Temps de réponse", value="1.3s", delta="-0.2s")
        
    # Visualisation des activités récentes d'ArcanSentinel
    st.markdown("### 📡 Activité récente d'ArcanSentinel")
    
    # Créer des exemples d'activités récentes
    recent_activities = [
        {"time": "17:32:45", "match": "Liverpool vs Arsenal", "event": "Momentum shift détecté pour Liverpool (+23%)", "impact": "high"},
        {"time": "17:28:12", "match": "PSG vs Lyon", "event": "Séquence de jeu intense détectée dans la zone critique", "impact": "medium"},
        {"time": "17:25:30", "match": "Bayern Munich vs Dortmund", "event": "Changement tactique identifié: Dortmund 4-3-3 → 3-5-2", "impact": "high"},
        {"time": "17:18:47", "match": "Liverpool vs Arsenal", "event": "Blessure potentielle détectée: joueur #7", "impact": "medium"},
        {"time": "17:15:22", "match": "PSG vs Lyon", "event": "Pression défensive accrue de Lyon (+32% d'intensité)", "impact": "low"}
    ]
    
    for activity in recent_activities:
        impact_color = "#ff3364" if activity["impact"] == "high" else "#ffbe41" if activity["impact"] == "medium" else "#01ff80"
        
        st.markdown(f"""
        <div style="display: flex; padding: 10px; border-radius: 5px; margin-bottom: 8px; 
                  background: rgba(8, 15, 40, 0.5); border-left: 3px solid {impact_color};">
            <div style="min-width: 80px; font-size: 13px; color: rgba(255, 255, 255, 0.7);">
                {activity["time"]}
            </div>
            <div style="flex-grow: 1;">
                <div style="font-size: 14px; color: white;">
                    {activity["event"]}
                </div>
                <div style="font-size: 12px; color: rgba(255, 255, 255, 0.6); margin-top: 3px;">
                    {activity["match"]}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with st.sidebar:
        st.markdown("## 🔯 Aperçus Ésotériques")
        
        # Tarot du jour
        st.markdown("### 🃏 Tarot du jour")
        tarot_cards = ["Le Magicien", "La Grande Prêtresse", "L'Impératrice", "L'Empereur", "Le Pape"]
        daily_tarot = np.random.choice(tarot_cards)
        st.markdown(f"**Carte dominante:** {daily_tarot}")
        
        # Runes nordiques
        st.markdown("### ᚠ Runes Actives")
        runes = ["Fehu (Prospérité)", "Uruz (Force)", "Thurisaz (Protection)", "Ansuz (Communication)"]
        active_runes = np.random.choice(runes, 2, replace=False)
        st.markdown(f"**Influence primaire:** {active_runes[0]}")
        st.markdown(f"**Influence secondaire:** {active_runes[1]}")
        
        # Influences astrales
        st.markdown("### ♃ Influences Astrales")
        planets = ["Jupiter ⬆️", "Mars ⬇️", "Vénus ↔️", "Mercure ⬆️", "Saturne ⬇️"]
        active_planets = np.random.choice(planets, 3, replace=False)
        for planet in active_planets:
            st.markdown(f"• {planet}")
    
    # Affichage des matchs à la une
    st.markdown(f"## 🌟 {t('featured_matches')}")
    
    for match in featured_matches:
        # Classes de probabilité pour le code couleur
        home_prob = match.get('home_prob', 0.45)
        draw_prob = match.get('draw_prob', 0.25)
        away_prob = match.get('away_prob', 0.30)
        
        home_prob_class = "high" if home_prob >= 0.6 else ("medium" if home_prob >= 0.4 else "low")
        draw_prob_class = "high" if draw_prob >= 0.6 else ("medium" if draw_prob >= 0.4 else "low")
        away_prob_class = "high" if away_prob >= 0.6 else ("medium" if away_prob >= 0.4 else "low")
        
        # Code du pays pour les drapeaux
        country_code = match.get('country_code', 'fr').lower()
        
        # Carte de match élégante avec notre nouvelle conception
        st.markdown(f"""
        <div class="match-card featured">
            <div class="match-header">
                <div class="match-time">{match.get('kickoff_time', '??:??')}</div>
                <div class="match-league">
                    <img src="https://flagcdn.com/48x36/{country_code}.png" width="24" />
                    <span>{match.get('league', '')}</span>
                </div>
            </div>
            <div class="match-teams">
                <div class="home-team">{match['home_team']}</div>
                <div class="versus">VS</div>
                <div class="away-team">{match['away_team']}</div>
            </div>
            <div class="match-odds">
                <div class="prob-{home_prob_class}">{match.get('home_odds', '?.??')} ({int(home_prob * 100)}%)</div>
                <div class="prob-{draw_prob_class}">{match.get('draw_odds', '?.??')} ({int(draw_prob * 100)}%)</div>
                <div class="prob-{away_prob_class}">{match.get('away_odds', '?.??')} ({int(away_prob * 100)}%)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Affichage des matchs du jour
    st.markdown(f"## 🗓️ {t('todays_matches')}")
    
    for match in today_matches:
        # Classes de probabilité pour le code couleur
        home_prob = match.get('home_prob', 0.45)
        draw_prob = match.get('draw_prob', 0.25)
        away_prob = match.get('away_prob', 0.30)
        
        home_prob_class = "high" if home_prob >= 0.6 else ("medium" if home_prob >= 0.4 else "low")
        draw_prob_class = "high" if draw_prob >= 0.6 else ("medium" if draw_prob >= 0.4 else "low")
        away_prob_class = "high" if away_prob >= 0.6 else ("medium" if away_prob >= 0.4 else "low")
        
        # Code du pays pour les drapeaux
        country_code = match.get('country_code', 'fr').lower()
        
        # Carte de match élégante standard
        st.markdown(f"""
        <div class="match-card">
            <div class="match-header">
                <div class="match-time">{match.get('kickoff_time', '??:??')}</div>
                <div class="match-league">
                    <img src="https://flagcdn.com/48x36/{country_code}.png" width="24" />
                    <span>{match.get('league', '')}</span>
                </div>
            </div>
            <div class="match-teams">
                <div class="home-team">{match['home_team']}</div>
                <div class="versus">VS</div>
                <div class="away-team">{match['away_team']}</div>
            </div>
            <div class="match-odds">
                <div class="prob-{home_prob_class}">{match.get('home_odds', '?.??')} ({int(home_prob * 100)}%)</div>
                <div class="prob-{draw_prob_class}">{match.get('draw_odds', '?.??')} ({int(draw_prob * 100)}%)</div>
                <div class="prob-{away_prob_class}">{match.get('away_odds', '?.??')} ({int(away_prob * 100)}%)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tabs[1]:  # Prédictions
    st.markdown("## 🔮 Prédictions d'ArcanShadow")
    st.markdown("Analyse détaillée des prédictions pour les matchs sélectionnés, avec explication des modules contributeurs.")
    
    # Sélection du match à analyser
    st.markdown("### ⚽ Sélectionner un match")
    
    # Créer des données fictives de matchs à venir pour la sélection
    upcoming_matches = [
        "PSG vs Lyon (Ligue 1) - 20:45",
        "Real Madrid vs Barcelona (La Liga) - 21:00",
        "Liverpool vs Arsenal (Premier League) - 17:30",
        "Bayern Munich vs Dortmund (Bundesliga) - 18:30",
        "Inter vs Milan (Serie A) - 20:45"
    ]
    
    selected_match = st.selectbox("Match à analyser:", upcoming_matches)
    
    # Extraire les équipes et la ligue du match sélectionné
    match_parts = selected_match.split(" (")
    teams = match_parts[0].split(" vs ")
    home_team = teams[0]
    away_team = teams[1]
    league = match_parts[1].split(")")[0]
    
    # Afficher le résumé de la prédiction
    st.markdown(f"### 📊 Prédiction pour {home_team} vs {away_team}")
    
    # Au lieu d'une seule grande structure HTML, on va la diviser en plusieurs parties
    
    # En-tête de la prédiction
    st.markdown("""
    <div style="padding: 20px; border-radius: 10px; background: linear-gradient(135deg, rgba(8, 15, 40, 0.8), rgba(17, 23, 64, 0.7)); 
                border: 1px solid rgba(81, 99, 149, 0.3); margin-bottom: 20px;">
    """, unsafe_allow_html=True)
    
    # Titre et confiance
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <div style="font-size: 24px; font-weight: bold; color: white;">Prédiction principale</div>
            <div style="background: rgba(1, 255, 128, 0.1); padding: 5px 10px; border-radius: 5px; 
                     border: 1px solid rgba(1, 255, 128, 0.3); color: #01ff80; font-weight: bold;">
                Confiance: 87%
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Résultat le plus probable
    st.markdown("""
        <div style="background: rgba(112, 0, 255, 0.1); padding: 15px; border-radius: 8px; 
                  border: 1px solid rgba(112, 0, 255, 0.2); margin-bottom: 15px;">
            <table width="100%" style="border-collapse: collapse;">
                <tr>
                    <td>
                        <div style="font-size: 18px; color: rgba(255, 255, 255, 0.9);">Résultat le plus probable</div>
                        <div style="font-size: 28px; font-weight: bold; color: #7000ff;">Victoire de Liverpool</div>
                    </td>
                    <td align="right">
                        <div style="font-size: 24px; font-weight: bold; color: white;">1.85</div>
                    </td>
                </tr>
            </table>
        </div>
    """, unsafe_allow_html=True)
    
    # Titre des autres scénarios
    st.markdown("""
        <div style="font-size: 18px; font-weight: bold; margin-bottom: 10px; color: white;">Autres scénarios</div>
    """, unsafe_allow_html=True)
    
    # Les scénarios en 2 colonnes (premier arrangement)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style="padding: 10px; background: rgba(255, 255, 255, 0.05); border-radius: 5px; margin-bottom: 10px;">
                <table width="100%" style="border-collapse: collapse;">
                    <tr>
                        <td><div style="color: white;">Match nul</div></td>
                        <td align="right"><div style="color: #ffbe41;">3.40 <span style="opacity: 0.7; font-size: 0.9em;">(24%)</span></div></td>
                    </tr>
                </table>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="padding: 10px; background: rgba(255, 255, 255, 0.05); border-radius: 5px; margin-bottom: 10px;">
                <table width="100%" style="border-collapse: collapse;">
                    <tr>
                        <td><div style="color: white;">Victoire d'Arsenal</div></td>
                        <td align="right"><div style="color: #ff3364;">4.50 <span style="opacity: 0.7; font-size: 0.9em;">(19%)</span></div></td>
                    </tr>
                </table>
            </div>
        """, unsafe_allow_html=True)
    
    # Les scénarios en 2 colonnes (deuxième arrangement)
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
            <div style="padding: 10px; background: rgba(255, 255, 255, 0.05); border-radius: 5px;">
                <table width="100%" style="border-collapse: collapse;">
                    <tr>
                        <td><div style="color: white;">Plus de 2.5 buts</div></td>
                        <td align="right"><div style="color: #01ff80;">1.72 <span style="opacity: 0.7; font-size: 0.9em;">(82%)</span></div></td>
                    </tr>
                </table>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div style="padding: 10px; background: rgba(255, 255, 255, 0.05); border-radius: 5px;">
                <table width="100%" style="border-collapse: collapse;">
                    <tr>
                        <td><div style="color: white;">Les deux équipes marquent</div></td>
                        <td align="right"><div style="color: #01ff80;">1.65 <span style="opacity: 0.7; font-size: 0.9em;">(85%)</span></div></td>
                    </tr>
                </table>
            </div>
        """, unsafe_allow_html=True)
    
    # Fermeture du conteneur principal
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)
    
    # Modules contributeurs et leur impact
    st.markdown("### 🧠 Modules contributeurs")
    
    # Créer des statistiques pour les modules qui ont contribué à la prédiction
    contributing_modules = [
        {"name": "ArcanX", "confidence": 0.92, "weight": 0.35, "key_insights": "Alignement Jupiter-Mars favorable à l'équipe locale"},
        {"name": "ShadowOdds", "confidence": 0.83, "weight": 0.25, "key_insights": "Anomalie de cote identifiée: sous-évaluation de Liverpool +0.22"},
        {"name": "KarmicFlow+", "confidence": 0.79, "weight": 0.15, "key_insights": "Séquence karmique positive détectée pour Liverpool (3 cycles)"},
        {"name": "NumeriCode", "confidence": 0.87, "weight": 0.10, "key_insights": "Concordance numérique: date du match (17) + patron tactique (4-3-3)"},
        {"name": "MetaSystems", "confidence": 0.89, "weight": 0.15, "key_insights": "Projection de volume d'échange: Liverpool dominant à 63%"}
    ]
    
    # Créer un dataframe pour les modules contributeurs
    df_modules_contrib = pd.DataFrame(contributing_modules)
    
    # Calculer l'impact de chaque module (confiance × poids)
    df_modules_contrib["impact"] = df_modules_contrib["confidence"] * df_modules_contrib["weight"]
    
    # Trier par impact
    df_modules_contrib = df_modules_contrib.sort_values(by="impact", ascending=False)
    
    # Créer une visualisation pour montrer la contribution de chaque module
    fig = px.bar(
        df_modules_contrib,
        x="impact",
        y="name",
        orientation='h',
        labels={"impact": "Impact sur la prédiction", "name": "Module"},
        title="Contribution des modules à la prédiction finale",
        color="confidence",
        text=df_modules_contrib["impact"].apply(lambda x: f"{x:.2f}"),
        color_continuous_scale=["red", "gold", "green"],
        range_color=[0.6, 1.0],
        height=400
    )
    
    fig.update_layout(
        template="plotly_dark", 
        yaxis=dict(autorange="reversed"),
        dragmode=False,
        xaxis=dict(fixedrange=True),  # Désactive le zoom sur l'axe X
        yaxis_fixedrange=True         # Désactive le zoom sur l'axe Y
    )
    
    # Rendre le graphique complètement statique
    st.plotly_chart(
        fig, 
        use_container_width=True, 
        config={
            'staticPlot': True,               # Force un plot statique
            'displayModeBar': False,          # Masque la barre d'outils
            'showTips': False,                # Désactive les astuces
            'doubleClick': False,             # Désactive le double-clic
            'showAxisDragHandles': False,     # Désactive les poignées d'axe
            'showAxisRangeEntryBoxes': False, # Désactive les boîtes de plage d'axe
            'displaylogo': False              # Désactive le logo Plotly
        }
    )
    
    # Afficher les insights clés de chaque module
    st.markdown("### 🔑 Insights clés par module")
    
    for module in df_modules_contrib.itertuples():
        confidence_color = "#01ff80" if module.confidence >= 0.85 else "#ffbe41" if module.confidence >= 0.75 else "#ff3364"
        
        st.markdown(f"""
        <div style="padding: 12px; border-radius: 8px; background: rgba(8, 15, 40, 0.6); 
                    border-left: 4px solid {confidence_color}; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-weight: bold; font-size: 16px;">{module.name}</div>
                <div style="color: {confidence_color}; font-family: 'JetBrains Mono', monospace;">
                    Confiance: {module.confidence:.0%}
                </div>
            </div>
            <div style="margin-top: 5px; color: rgba(255, 255, 255, 0.8);">
                {module.key_insights}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Narratif de la prédiction
    st.markdown("### 📜 Narratif de la prédiction")
    
    st.markdown("""
    <div style="padding: 15px; border-radius: 10px; background: rgba(112, 0, 255, 0.05); 
                border: 1px solid rgba(112, 0, 255, 0.2); margin-bottom: 20px;">
        <p style="color: rgba(255, 255, 255, 0.85); font-size: 16px; line-height: 1.6;">
            L'analyse des cycles karmiques révèle un alignement favorable pour <b>Liverpool</b> qui entre dans une phase ascendante
            après trois matchs de consolidation. Cette dynamique est amplifiée par une configuration astrale propice
            avec Jupiter en transit dans la maison de la victoire.
            <br><br>
            L'analyse <b>NumeriCode</b> détecte une forte résonance entre la date du match (17) et le schéma tactique (4-3-3),
            créant une harmonique vibratoire qui favorise historiquement l'équipe locale dans ce type de confrontation.
            <br><br>
            Les cotes actuelles sous-évaluent le potentiel de Liverpool de <b>0.22 points</b>, créant une opportunité
            de value bet selon le module <b>ShadowOdds</b>. Cette anomalie est généralement corrélée avec un taux de succès supérieur.
            <br><br>
            <b>Conclusion:</b> La convergence de signaux positifs multiples, renforcée par le méta-système de pondération
            suggère une victoire de Liverpool avec un niveau de confiance élevé (87%).
        </p>
    </div>
    """, unsafe_allow_html=True)
    
with tabs[2]:  # Performance Notifications
    st.markdown("## 🔔 Notifications de Performance")
    st.markdown("Suivi et analyse des performances prédictives du système ArcanShadow avec comparaison aux résultats réels.")
    
    # En-tête avec statistiques globales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Précision Globale", value="78%", delta="+2.3%")
    with col2:
        st.metric(label="ROI Hebdomadaire", value="12.7%", delta="+0.8%")
    with col3:
        st.metric(label="Modules Actifs", value="14/16", delta="+1")
    with col4:
        st.metric(label="Échantillon", value="342 matchs", delta="+47")
    
    # Tableau des performances récentes
    st.markdown("### 📈 Bilan de Synthèse (7 derniers jours)")
    
    # Créer des données de performance simulées
    performance_data = {
        "Date": [(datetime.now() - timedelta(days=i)).strftime("%d/%m/%Y") for i in range(7)],
        "Matchs": [np.random.randint(12, 25) for _ in range(7)],
        "Prédictions Correctes": [np.random.randint(8, 20) for _ in range(7)],
        "Précision": [f"{np.random.randint(65, 90)}%" for _ in range(7)],
        "Module Star": np.random.choice(["ArcanX", "ShadowOdds", "NumeriCode", "KarmicFlow+", "AstroImpact"], 7)
    }
    
    # Calculer le taux de précision
    for i in range(7):
        matches = performance_data["Matchs"][i]
        correct = performance_data["Prédictions Correctes"][i]
        performance_data["Précision"][i] = f"{round((correct / matches) * 100)}%"
    
    df_performance = pd.DataFrame(performance_data)
    st.dataframe(df_performance, use_container_width=True)
    
    # Graphique de performance des modules
    st.markdown("### 🧩 Performance des Modules Prédictifs")
    
    modules = ["ArcanX", "ShadowOdds", "NumeriCode", "KarmicFlow+", "AstroImpact", 
               "EchoPath", "TarotEcho", "ShadowOdds+", "MetaSystems"]
    accuracy = [np.random.uniform(0.65, 0.92) for _ in modules]
    sample_size = [np.random.randint(50, 300) for _ in modules]
    
    # Trier par précision
    sorted_indices = sorted(range(len(accuracy)), key=lambda i: accuracy[i], reverse=True)
    sorted_modules = [modules[i] for i in sorted_indices]
    sorted_accuracy = [accuracy[i] for i in sorted_indices]
    sorted_sample = [sample_size[i] for i in sorted_indices]
    
    # Créer un dataframe
    df_modules = pd.DataFrame({
        "Module": sorted_modules,
        "Précision": sorted_accuracy,
        "Échantillon": sorted_sample
    })
    
    # Créer un graphique à barres horizontal statique
    fig = px.bar(
        df_modules, y="Module", x="Précision", 
        orientation='h',
        title="Précision par Module (30 derniers jours)",
        color="Précision",
        color_continuous_scale=["red", "gold", "green"],
        range_color=[0.5, 1.0],
        text=df_modules["Précision"].apply(lambda x: f"{x:.1%}"),
        height=500
    )
    
    fig.update_layout(
        xaxis_title="Précision (%)",
        yaxis_title="Module Prédictif",
        template="plotly_dark",
        dragmode=False,
        hovermode=False
    )
    
    # Afficher le graphique de manière statique (sans interaction)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
    
    # Alertes et recommandations de calibration
    st.markdown("### ⚠️ Alertes et Recommandations")
    
    alert1, alert2 = st.columns(2)
    
    with alert1:
        st.markdown("""
        <div style="padding: 15px; border-radius: 10px; background-color: rgba(255, 51, 100, 0.1); border: 1px solid rgba(255, 51, 100, 0.3);">
            <h4 style="color: #ff3364;">⚠️ Module en sous-performance</h4>
            <p><b>EchoPath</b> montre une baisse de précision de 8.7% sur les 14 derniers jours. Recalibration recommandée.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with alert2:
        st.markdown("""
        <div style="padding: 15px; border-radius: 10px; background-color: rgba(1, 255, 128, 0.1); border: 1px solid rgba(1, 255, 128, 0.3);">
            <h4 style="color: #01ff80;">✅ Module surperformant</h4>
            <p><b>ShadowOdds+</b> affiche une précision exceptionnelle de 91.3% dans la Ligue 1. Augmentation de pondération recommandée.</p>
        </div>
        """, unsafe_allow_html=True)


with tabs[3]:  # Daily Combo
    st.markdown("## 🎯 Combiné du Jour")
    st.markdown("Sélection automatique optimisée des meilleures opportunités de paris, basée sur les modules les plus performants.")
    
    # Paramètres du combiné
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("### ⚙️ Configuration")
        confidence_level = st.slider("Niveau de confiance minimum", 60, 95, 75, 5)
        
    with col2:
        st.metric(label="Nombre de Sélections", value="3")
        st.metric(label="Cote Combinée", value="7.36")
    
    with col3:
        st.metric(label="Confiance Globale", value="83%", delta="+8%")
        st.metric(label="Module Dominant", value="ArcanX")
    
    # Sélection des modules performants
    st.markdown("### 🧩 Modules Utilisés (sélection automatique)")
    
    modules_used = ["ArcanX", "ShadowOdds+", "KarmicFlow+", "MetaSystems"]
    module_weights = [0.35, 0.25, 0.22, 0.18]
    
    # Créer un graphique camembert statique
    fig_modules = px.pie(
        values=module_weights, 
        names=modules_used,
        title="Pondération des modules pour le combiné",
        color_discrete_sequence=["#7000ff", "#01ff80", "#ffbe41", "#05d9e8"]
    )
    
    # Désactiver toutes les interactions possibles
    fig_modules.update_layout(
        dragmode=False,
        hovermode=False
    )
    
    # Afficher le graphique de manière complètement statique
    st.plotly_chart(fig_modules, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
    
    # Sélections du jour
    st.markdown("### 📊 Sélections du Combiné")
    
    # Création des sélections
    selections = [
        {
            "match": "PSG vs Lyon",
            "league": "Ligue 1",
            "prediction": "PSG gagne",
            "odds": 1.82,
            "confidence": 86,
            "key_factors": ["Momentum favorable: +23%", "Cycle karmique positif", "Delta de cote: 0.21"]
        },
        {
            "match": "Barcelona vs Atletico Madrid",
            "league": "La Liga",
            "prediction": "Plus de 2.5 buts",
            "odds": 1.95,
            "confidence": 79,
            "key_factors": ["Tarot: La Tour (renversement)", "Convergence offensive: 68%", "Historique: 8/10 matchs"]
        },
        {
            "match": "Liverpool vs Chelsea",
            "league": "Premier League",
            "prediction": "Les deux équipes marquent",
            "odds": 2.10,
            "confidence": 84,
            "key_factors": ["Planetary transit: Jupiter+Mars", "Anomalie de cote: -0.32", "Attack strength: +17%"]
        }
    ]
    
    # Afficher les sélections dans des cartes visuelles
    for selection in selections:
        conf_color = "#01ff80" if selection["confidence"] >= 80 else "#ffbe41"
        
        st.markdown(f"""
        <div style="padding: 15px; border-radius: 10px; background: rgba(8, 15, 40, 0.6); 
                    border: 1px solid rgba(81, 99, 149, 0.2); margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div>
                    <div style="font-size: 18px; font-weight: bold;">{selection["match"]}</div>
                    <div style="font-size: 14px; color: rgba(255, 255, 255, 0.7);">{selection["league"]}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 22px; font-weight: bold; font-family: 'JetBrains Mono', monospace;">{selection["odds"]}</div>
                    <div style="font-size: 14px; color: {conf_color};">Confiance: {selection["confidence"]}%</div>
                </div>
            </div>
            <div style="background: rgba(112, 0, 255, 0.1); padding: 10px; border-radius: 8px; 
                        border: 1px solid rgba(112, 0, 255, 0.2); margin-bottom: 10px;">
                <div style="font-size: 16px; font-weight: bold; color: #7000ff; margin-bottom: 5px;">
                    💡 Prédiction: {selection["prediction"]}
                </div>
            </div>
            <div style="font-size: 14px; color: rgba(255, 255, 255, 0.8);">
                <b>Facteurs clés:</b>
                <ul style="margin-top: 5px; padding-left: 20px;">
                    <li>{selection["key_factors"][0]}</li>
                    <li>{selection["key_factors"][1]}</li>
                    <li>{selection["key_factors"][2]}</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Historique des performances
    st.markdown("### 📈 Historique des Combinés")
    
    history_data = {
        "Date": [(datetime.now() - timedelta(days=i)).strftime("%d/%m/%Y") for i in range(1, 11)],
        "Selections": [np.random.randint(2, 5) for _ in range(10)],
        "Cote": [round(np.random.uniform(3.5, 12.5), 2) for _ in range(10)],
        "Résultat": np.random.choice(["✅ Gagné", "❌ Perdu"], 10, p=[0.6, 0.4])
    }
    
    df_history = pd.DataFrame(history_data)
    st.dataframe(df_history, use_container_width=True)

with tabs[4]:  # Smart Market Recommendations
    st.markdown("## 💡 Recommandations intelligentes de marché")
    st.markdown("Recommandations intelligentes de paris basées sur l'analyse multidimensionnelle des marchés et des anomalies de cotes.")
    
    # Filtres de marché
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_sport = st.selectbox("Sport", ["Football", "Basketball", "Tennis", "Hockey"])
    with col2:
        selected_league = st.selectbox("Compétition", ["Toutes", "Ligue 1", "Premier League", "LaLiga", "Bundesliga", "Serie A"])
    with col3:
        market_type = st.selectbox("Type de Marché", ["Résultat final", "Les deux équipes marquent", "Over/Under", "Handicap", "Score exact"])
    
    # Tableau de bord des opportunités
    st.markdown("### 💎 Opportunités Détectées")
    
    # Créer un tableau d'anomalies de cotes
    anomalies = [
        {
            "match": "PSG vs Lyon",
            "market": "Lyon ou Nul",
            "odds": 2.45,
            "fair_odds": 2.10,
            "value": "+16.7%",
            "confidence": 82,
            "modules": "ShadowOdds, LineTrap"
        },
        {
            "match": "Arsenal vs Liverpool",
            "market": "Plus de 2.5 buts",
            "odds": 1.95,
            "fair_odds": 1.76,
            "value": "+10.8%",
            "confidence": 89,
            "modules": "NumeriCode, AstroImpact"
        },
        {
            "match": "Real Madrid vs Barcelona",
            "market": "Les deux équipes marquent",
            "odds": 1.75,
            "fair_odds": 1.58,
            "value": "+10.8%",
            "confidence": 91,
            "modules": "ArcanX, KarmicFlow+"
        },
        {
            "match": "Bayern Munich vs Dortmund",
            "market": "Bayern gagne et Plus de 3.5 buts",
            "odds": 3.25,
            "fair_odds": 2.85,
            "value": "+14.0%",
            "confidence": 76,
            "modules": "EchoPath, MetaSystems"
        },
        {
            "match": "Milan vs Inter",
            "market": "Milan gagne",
            "odds": 3.10,
            "fair_odds": 2.65,
            "value": "+17.0%",
            "confidence": 73,
            "modules": "TarotEcho, ShadowOdds+"
        }
    ]
    
    # Créer un tableau
    anomalies_df = pd.DataFrame(anomalies)
    
    # Appliquer un style conditionnel
    def highlight_value(val):
        if '+' in str(val):
            return 'color: #01ff80; font-weight: bold'
        return ''
    
    # Afficher le tableau avec style - using style.map instead of style.applymap (which is deprecated)
    st.dataframe(anomalies_df.style.map(highlight_value, subset=['value']), use_container_width=True)
    
    # Graphique de distribution des valeurs
    st.markdown("### 📊 Distribution des Valeurs sur le Marché")
    
    # Utiliser une image prédéfinie pour éviter toute interactivité
    # Simuler des données pour l'histogramme
    market_values = np.random.normal(0, 5, 1000)
    thresholds = np.percentile(market_values, [5, 95])
    
    # Créer un histogramme simple avec Plotly mais le convertir en image
    fig_hist = px.histogram(
        market_values, 
        nbins=40,
        title="Distribution de la Valeur (Value) sur le marché",
        labels={"value": "Valeur (%)", "count": "Nombre de paris"},
        color_discrete_sequence=["#7000ff"]
    )
    
    # Ajouter les lignes de seuil
    fig_hist.add_vline(x=thresholds[0], line_dash="dash", line_color="#ff3364")
    fig_hist.add_vline(x=thresholds[1], line_dash="dash", line_color="#01ff80")
    
    # Ajouter l'annotation
    fig_hist.add_annotation(
        x=thresholds[1] + 1,
        y=50,
        text="Zone de valeur",
        showarrow=True,
        arrowhead=1,
        arrowcolor="#01ff80",
        font=dict(color="#01ff80")
    )
    
    # Mise en page
    fig_hist.update_layout(
        template="plotly_dark",
        margin=dict(l=10, r=10, t=30, b=10),
        height=400,
        dragmode=False,
        xaxis=dict(fixedrange=True),  # Désactive le zoom sur l'axe X
        yaxis=dict(fixedrange=True)   # Désactive le zoom sur l'axe Y
    )
    
    # Utiliser un rendu statique (en désactivant tous les contrôles et interactions)
    st.plotly_chart(
        fig_hist, 
        use_container_width=True, 
        config={
            "staticPlot": True,              # Force un plot statique
            "displayModeBar": False,         # Masque la barre d'outils
            "showTips": False,               # Désactive les astuces
            "doubleClick": False,            # Désactive le double-clic
            "showAxisDragHandles": False,    # Désactive les poignées d'axe
            "showAxisRangeEntryBoxes": False, # Désactive les boîtes de plage d'axe
            "displaylogo": False             # Désactive le logo Plotly
        }
    )
    
    # Analyse ésotérique des influences
    st.markdown("### 🔮 Influences Ésotériques Actives")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="padding: 15px; border-radius: 10px; background: rgba(112, 0, 255, 0.1); 
                    border: 1px solid rgba(112, 0, 255, 0.2); margin-bottom: 15px;">
            <div style="font-size: 18px; font-weight: bold; color: #7000ff; margin-bottom: 10px;">
                ♃ Jupiter en Transit (Impact: Élevé)
            </div>
            <div style="font-size: 14px; color: rgba(255, 255, 255, 0.8);">
                Jupiter en transit dans la maison V favorise les équipes dominantes.
                <br><br>
                <b>Équipes amplifiées:</b> PSG, Real Madrid, Man City, Bayern
                <br>
                <b>Marchés favorisés:</b> Victoire à domicile + Over 2.5
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style="padding: 15px; border-radius: 10px; background: rgba(1, 255, 128, 0.1); 
                    border: 1px solid rgba(1, 255, 128, 0.2); margin-bottom: 15px;">
            <div style="font-size: 18px; font-weight: bold; color: #01ff80; margin-bottom: 10px;">
                ᛘ Rune Mannaz Active (Impact: Moyen)
            </div>
            <div style="font-size: 14px; color: rgba(255, 255, 255, 0.8);">
                L'influence de Mannaz renforce la cohésion d'équipe et l'harmonie collective.
                <br><br>
                <b>Équipes amplifiées:</b> Arsenal, Liverpool, Barcelona
                <br>
                <b>Marchés favorisés:</b> Les deux équipes marquent, Over 1.5 MI-TEMPS
            </div>
        </div>
        """, unsafe_allow_html=True)

with tabs[5]:  # Système d'Apprentissage
    st.markdown("## 🧠 Système d'Apprentissage")
    st.markdown("Visualisation de l'évolution du système ArcanShadow et des processus d'apprentissage de ses modules.")

# Nouvel onglet Notifications
with tabs[5]:  # Notifications
    st.markdown("## 📬 Centre de Notifications")
    st.markdown("Toutes les informations importantes du système ArcanShadow sont centralisées ici.")
    
    # Structure pour gérer les notifications
    if 'notifications' not in st.session_state:
        st.session_state.notifications = [
            {
                "id": 1,
                "type": "recalibration",
                "title": "Recalibration automatique de ArcanX",
                "message": "ArcanBrain a détecté une dérive de performance de 3.7% sur ArcanX et a procédé à une recalibration Deep Learning. Performance améliorée de +5.2%.",
                "timestamp": "2025-05-17 09:14:32",
                "read": False,
                "priority": "medium"
            },
            {
                "id": 2,
                "type": "pattern",
                "title": "Nouveau pattern détecté par ArcanReflex",
                "message": "Un pattern cyclique de type Fibonacci a été identifié dans les résultats de la Premier League. Ce motif a été intégré au module KarmicFlow+.",
                "timestamp": "2025-05-16 21:03:47",
                "read": False,
                "priority": "high"
            },
            {
                "id": 3,
                "type": "sentinel",
                "title": "Analyse en direct PSG vs Lyon",
                "message": "ArcanSentinel a détecté une augmentation de l'énergie offensive de Lyon à la 37e minute, suggérant une probabilité accrue de but avant la mi-temps.",
                "timestamp": "2025-05-16 15:37:21",
                "read": False,
                "priority": "urgent"
            },
            {
                "id": 4,
                "type": "module",
                "title": "Nouveau module recommandé par D-forge",
                "message": "D-forge a identifié le besoin d'un nouveau module 'ResilienceCore' pour analyser la capacité des équipes à rebondir après un but encaissé. Requête envoyée à ArcanConceptor.",
                "timestamp": "2025-05-15 18:42:09",
                "read": True,
                "priority": "medium"
            },
            {
                "id": 5,
                "type": "performance",
                "title": "Synthèse de performance hebdomadaire",
                "message": "Taux de précision global: 78.3% (+2.1% vs semaine précédente). Modules les plus performants: TarotEcho (83.9%), ArcanX (81.7%), KarmicFlow+ (80.3%).",
                "timestamp": "2025-05-15 08:00:00", 
                "read": True,
                "priority": "medium"
            }
        ]
    
    # Filtres pour les notifications
    col1, col2 = st.columns([1, 2])
    with col1:
        filter_option = st.selectbox("Filtrer par", ["Toutes", "Non lues", "Recalibration", "Pattern", "Sentinel", "Module", "Performance"], index=0)
    with col2:
        sort_option = st.radio("Trier par", ["Plus récent", "Plus ancien", "Priorité"], horizontal=True)
    
    # Appliquer les filtres
    filtered_notifications = st.session_state.notifications.copy()
    if filter_option == "Non lues":
        filtered_notifications = [n for n in filtered_notifications if not n["read"]]
    elif filter_option != "Toutes":
        filter_type = filter_option.lower()
        filtered_notifications = [n for n in filtered_notifications if n["type"] == filter_type]
    
    # Appliquer le tri
    if sort_option == "Plus récent":
        filtered_notifications.sort(key=lambda x: x["timestamp"], reverse=True)
    elif sort_option == "Plus ancien":
        filtered_notifications.sort(key=lambda x: x["timestamp"])
    elif sort_option == "Priorité":
        priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
        filtered_notifications.sort(key=lambda x: (priority_order.get(x["priority"], 4), x["timestamp"]), reverse=True)
    
    # Bouton pour marquer toutes les notifications comme lues
    if st.button("Marquer toutes comme lues"):
        for notif in st.session_state.notifications:
            notif["read"] = True
        st.session_state.notification_count = 0
        st.rerun()
    
    # Affichage des notifications
    st.markdown("### Notifications récentes")
    
    if not filtered_notifications:
        st.info("Aucune notification ne correspond aux filtres sélectionnés.")
    
    for notification in filtered_notifications:
        # Couleur basée sur le type et la priorité
        color_map = {
            "recalibration": "#7000ff",  # Violet
            "pattern": "#01ff80",  # Vert
            "sentinel": "#ff3860",  # Rouge
            "module": "#ffbe41",  # Orange
            "performance": "#3273dc"  # Bleu
        }
        
        priority_bg = {
            "urgent": "rgba(255, 56, 96, 0.15)",
            "high": "rgba(255, 190, 65, 0.15)",
            "medium": "rgba(112, 0, 255, 0.15)",
            "low": "rgba(50, 115, 220, 0.15)"
        }
        
        border_color = color_map.get(notification["type"], "#3273dc")
        bg_color = priority_bg.get(notification["priority"], "rgba(50, 115, 220, 0.15)")
        read_marker = "" if notification["read"] else "📌 "
        
        st.markdown(f"""
        <div style="border-left: 4px solid {border_color}; background: {bg_color}; 
                  border-radius: 5px; padding: 15px; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div style="font-weight: bold; font-size: 16px; color: white;">
                    {read_marker}{notification["title"]}
                </div>
                <div style="color: rgba(255, 255, 255, 0.6); font-size: 12px;">
                    {notification["timestamp"]}
                </div>
            </div>
            <p style="color: rgba(255, 255, 255, 0.8); margin: 8px 0;">
                {notification["message"]}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Option pour marquer une notification comme lue
        if not notification["read"]:
            if st.button(f"Marquer comme lu #{notification['id']}", key=f"mark_read_{notification['id']}"):
                for notif in st.session_state.notifications:
                    if notif["id"] == notification["id"]:
                        notif["read"] = True
                        break
                
                # Mettre à jour le compteur de notifications
                st.session_state.notification_count = sum(1 for n in st.session_state.notifications if not n["read"])
                st.rerun()
    
    # Vue d'ensemble du système
    st.markdown("### 🔄 État du Système ArcanReflex")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Modules Actifs", value="14/16", delta="+1")
    with col2:
        st.metric(label="Apprentissage", value="73%", delta="+5.2%")
    with col3:
        st.metric(label="Adaptation", value="91%", delta="+2.8%")
    with col4:
        st.metric(label="Précision", value="87%", delta="+3.5%")
    
    # Visualisation des connexions entre modules
    st.markdown("### 🌐 Réseau Neural ArcanBrain")
    
    # Créer un réseau de modules en apprentissage
    nodes = [
        "ArcanX", "ShadowOdds", "NumeriCode", "TarotEcho", "AstroImpact", 
        "KarmicFlow+", "EchoPath", "MetaSystems", "GridSync", "ArcanSentinel"
    ]
    
    connections = []
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if np.random.random() < 0.4:  # 40% de chance d'avoir une connexion
                connections.append((i, j, np.random.uniform(0.1, 1.0)))
    
    # Préparer les données pour le graphique
    edge_x = []
    edge_y = []
    edge_weights = []
    
    # Créer une disposition circulaire pour les nœuds
    node_x = [np.cos(2*np.pi*i/len(nodes)) for i in range(len(nodes))]
    node_y = [np.sin(2*np.pi*i/len(nodes)) for i in range(len(nodes))]
    
    for src, dst, weight in connections:
        edge_x.extend([node_x[src], node_x[dst], None])
        edge_y.extend([node_y[src], node_y[dst], None])
        edge_weights.append(weight)
    
    # Créer le graphique
    fig = go.Figure()
    
    # Ajouter les liens
    for i in range(0, len(edge_x), 3):
        opacity = min(1, edge_weights[i//3] * 2)
        width = 1 + 3 * edge_weights[i//3]
        fig.add_trace(go.Scatter(
            x=edge_x[i:i+3], y=edge_y[i:i+3],
            line=dict(width=width, color=f'rgba(112, 0, 255, {opacity})'),
            hoverinfo='none',
            mode='lines'
        ))
    
    # Ajouter les nœuds
    node_colors = ['#7000ff', '#01ff80', '#ffbe41', '#05d9e8', '#ff3364', 
                  '#7000ff', '#01ff80', '#ffbe41', '#05d9e8', '#ff3364']
    
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=nodes,
        textposition="top center",
        marker=dict(
            showscale=False,
            color=node_colors,
            size=20,
            line_width=2,
            line=dict(color='white')
        )
    ))
    
    fig.update_layout(
        title="Réseau de connexions entre modules",
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(b=0, l=0, r=0, t=40),
        template="plotly_dark",
        height=500,
        dragmode=False,
        hovermode=False
    )
    
    # Rendre le graphique complètement statique
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
    
    # Tableau de bord des événements d'apprentissage
    st.markdown("### 📝 Événements d'apprentissage récents")
    
    # Créer des données d'événements simulées
    events = [
        {
            "timestamp": "17/05/2025 18:12",
            "type": "Pattern Recalibration",
            "module": "TarotEcho",
            "description": "Recalibrage des patterns de récurrence La Tour + L'Étoile"
        },
        {
            "timestamp": "17/05/2025 15:47",
            "type": "Transfer Learning",
            "module": "ArcanX",
            "description": "Transfert de connaissance entre contextes Premier League → Ligue 1"
        },
        {
            "timestamp": "17/05/2025 14:33",
            "type": "Module Activation",
            "module": "ShadowOdds+",
            "description": "Activation après seuil de précision atteint (91.3%)"
        },
        {
            "timestamp": "16/05/2025 22:18",
            "type": "Pattern Recalibration",
            "module": "NumeriCode",
            "description": "Ajustement des séquences numériques 3-7-11 → 3-7-12"
        },
        {
            "timestamp": "16/05/2025 17:52",
            "type": "Architecture Update",
            "module": "GridSync",
            "description": "Optimisation de la couche de convergence +8.2% efficacité"
        }
    ]
    
    # Créer un dataframe
    events_df = pd.DataFrame(events)
    st.dataframe(events_df, use_container_width=True)
    
    # Système de logs détaillés
    st.markdown("### 📋 Logs d'apprentissage détaillés")
    
    learning_logs = """
2025-05-17 18:12:23 [INFO] [TarotEcho] Pattern Recalibration initiated
2025-05-17 18:12:24 [INFO] [TarotEcho] Analyzing historical pattern accuracy for sequence La Tour + L'Étoile
2025-05-17 18:12:26 [INFO] [TarotEcho] Previous accuracy: 78.4%, New accuracy after recalibration: 86.2%
2025-05-17 18:12:27 [INFO] [ArcanReflex] Recognizing improved pattern, saving to ReflexMemory
2025-05-17 18:12:28 [SUCCESS] [TarotEcho] Pattern recalibration complete, awaiting validation in next predictions

2025-05-17 15:47:09 [INFO] [ArcanX] Transfer Learning process initiated
2025-05-17 15:47:10 [INFO] [ArcanX] Source context: Premier League (confidence: 91.7%)
2025-05-17 15:47:11 [INFO] [ArcanX] Target context: Ligue 1 (pre-transfer confidence: 76.3%)
2025-05-17 15:47:15 [INFO] [ArcanX] Adapting Premier League pattern recognition to Ligue 1 context
2025-05-17 15:47:18 [INFO] [ArcanX] Key transformations: adjusted home advantage -3.2%, tactical variety +7.8%
2025-05-17 15:47:20 [SUCCESS] [ArcanX] Transfer Learning complete, new Ligue 1 confidence: 84.5%

2025-05-17 14:33:45 [INFO] [ShadowOdds+] Activation threshold check: 91.3% precision reached
2025-05-17 14:33:47 [INFO] [ShadowOdds+] Analyzing prediction stability across last 241 matches
2025-05-17 14:33:49 [INFO] [ShadowOdds+] Standard deviation: 4.2%, within acceptable range
2025-05-17 14:33:50 [INFO] [GridSync] Integrating ShadowOdds+ into primary prediction matrix
2025-05-17 14:33:52 [INFO] [GridSync] Assigned weight coefficient: 0.23 (moderate-high)
2025-05-17 14:33:53 [SUCCESS] [ShadowOdds+] Module activation complete, actively contributing to system
    """
    
    st.code(learning_logs, language="plaintext")
    
    # Section de recalibration automatique
    st.markdown("### ⚙️ Système de recalibration automatique")
    
    # Interface de recalibration avec structure HTML corrigée
    st.markdown("""
    <div style="border: 1px solid rgba(112, 0, 255, 0.3); border-radius: 10px; padding: 20px; background: rgba(112, 0, 255, 0.05);">
        <!-- En-tête avec statut -->
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="color: #7000ff; margin: 0;">Processus de recalibration par ArcanBrain</h4>
                <div style="background: rgba(1, 255, 128, 0.1); padding: 5px 10px; border-radius: 5px; 
                         border: 1px solid rgba(1, 255, 128, 0.3); color: #01ff80; font-weight: bold;">
                    Actif
                </div>
            </div>
        </div>
        
        <!-- Description -->
        <div style="margin-bottom: 15px;">
            <p style="color: rgba(255, 255, 255, 0.8); font-size: 15px; line-height: 1.6;">
                ArcanBrain surveille en permanence les performances du système et procède automatiquement
                à des recalibrations intelligentes des modules prédictifs, selon leurs besoins spécifiques.
                Les processus de recalibration sont entièrement gérés par l'intelligence système.
            </p>
        </div>
        
        <!-- Modes de recalibration -->
        <div style="background: rgba(255, 255, 255, 0.05); border-radius: 8px; padding: 15px; margin-bottom: 15px;">
            <div style="font-weight: bold; margin-bottom: 8px; color: rgba(255, 255, 255, 0.9);">
                Modes de recalibration automatiques:
            </div>
            <div style="color: rgba(255, 255, 255, 0.8); font-size: 14px; margin-left: 20px;">
                • <b>Standard:</b> Recalibration basique sur les dernières données<br>
                • <b>Deep Learning:</b> Restructuration complète des couches de patterns<br>
                • <b>Transfer Learning:</b> Application des connaissances d'une ligue à une autre<br>
                • <b>Pattern Recognition:</b> Focus sur la détection des motifs récurrents
            </div>
        </div>
        
        <!-- Informations système -->
        <div style="font-size: 15px; color: rgba(255, 255, 255, 0.8);">
            <div><b>Dernier diagnostic système:</b> Tous les modules fonctionnent dans les paramètres optimaux.</div>
            <div style="margin-top: 5px;"><b>Temps écoulé depuis la dernière recalibration:</b> 3h 17min</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Métriques ArcanReflex")
    
    # Afficher les métriques de santé du système
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Santé globale", value="97%", delta="+2.3%")
    with col2:
        st.metric(label="Efficacité d'apprentissage", value="91.4%", delta="+4.7%")
    with col3:
        st.metric(label="Confiance système", value="88.9%", delta="+1.2%")
    
    
    # Structure pour les matchs en direct
    if 'live_matches' not in st.session_state:
        st.session_state.live_matches = [
            {"id": 1, "home": "PSG", "away": "Lyon", "league": "Ligue 1", "time": "20:45", "status": "En direct", "minute": "37'", "score": "1-0"},
            {"id": 2, "home": "Liverpool", "away": "Arsenal", "league": "Premier League", "time": "17:30", "status": "En direct", "minute": "68'", "score": "2-1"},
            {"id": 3, "home": "Bayern Munich", "away": "Dortmund", "league": "Bundesliga", "time": "18:30", "status": "En direct", "minute": "52'", "score": "0-0"}
        ]
    
    # Structure pour gérer les matchs surveillés en direct
    if 'sentinel_monitored_live_matches' not in st.session_state:
        st.session_state.sentinel_monitored_live_matches = []
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Tableau des matchs en direct disponibles
        st.markdown("#### 🔴 Matchs actuellement en direct")
        
        for match in st.session_state.live_matches:
            is_monitored = any(m['id'] == match['id'] for m in st.session_state.sentinel_monitored_live_matches)
            status_color = "#01ff80" if is_monitored else "rgba(255, 255, 255, 0.8)"
            status_text = "🟢 Surveillé en direct" if is_monitored else "⚪ Disponible"
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; 
                      padding: 12px; border-radius: 5px; margin-bottom: 15px; 
                      background: rgba(255, 51, 100, 0.1); border: 1px solid rgba(255, 51, 100, 0.2);">
                <div>
                    <div style="font-weight: bold; font-size: 16px; color: white;">
                        {match['home']} {match['score']} {match['away']}
                    </div>
                    <div style="font-size: 13px; color: #ff3364; font-weight: bold; margin-top: 4px;">
                        {match['minute']} • EN DIRECT
                    </div>
                    <div style="font-size: 12px; color: rgba(255, 255, 255, 0.6); margin-top: 2px;">
                        {match['league']}
                    </div>
                </div>
                <div style="font-size: 13px; color: {status_color};">
                    {status_text}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Pour chaque match, ajouter des boutons d'action
            col_a, col_b = st.columns([3, 2])
            with col_a:
                if not is_monitored:
                    if st.button(f"Activer surveillance en direct", key=f"activate_live_notif_{match['id']}"):
                        # Configuration de surveillance
                        surveillance_config = {
                            "id": match['id'],
                            "home": match['home'],
                            "away": match['away'],
                            "league": match['league'],
                            "minute": match['minute'],
                            "score": match['score'],
                            "monitoring_level": "Maximum",  # Plus haut niveau pour les matchs en direct
                            "modules": ["ShadowMomentum", "LineTrap", "KarmicFlow", "MirrorPhase", "BetPulse"],
                            "activated_at": "2025-05-17 " + datetime.now().strftime("%H:%M:%S"),
                            "alert_threshold": 5  # Seuil plus bas pour être plus réactif aux matchs en direct
                        }
                        st.session_state.sentinel_monitored_live_matches.append(surveillance_config)
                        
                        # Ajouter une notification d'activation
                        if 'notifications' in st.session_state:
                            new_notif = {
                                "id": len(st.session_state.notifications) + 1,
                                "type": "sentinel",
                                "title": f"🔴 ArcanSentinel activé en DIRECT: {match['home']} vs {match['away']}",
                                "message": f"Surveillance instantanée lancée sur le match en direct {match['home']} vs {match['away']} ({match['minute']}). Les analyses seront envoyées en temps réel.",
                                "timestamp": "2025-05-17 " + datetime.now().strftime("%H:%M:%S"),
                                "read": False,
                                "priority": "urgent"
                            }
                            st.session_state.notifications.append(new_notif)
                            # Mise à jour du compteur
                            st.session_state.notification_count = sum(1 for n in st.session_state.notifications if not n["read"])
                        
                        st.rerun()
                else:
                    if st.button(f"Désactiver", key=f"deactivate_live_{match['id']}"):
                        st.session_state.sentinel_monitored_live_matches = [m for m in st.session_state.sentinel_monitored_live_matches if m['id'] != match['id']]
                        st.rerun()
    
    with col2:
        st.markdown("#### Configuration pour l'analyse en direct")
        
        st.markdown("""
        <div style="border: 1px solid rgba(255, 51, 100, 0.3); border-radius: 10px; padding: 15px; background: rgba(255, 51, 100, 0.05);">
            <h4 style="color: #ff3364; margin-top: 0;">Surveillance en Direct</h4>
            <p style="color: rgba(255, 255, 255, 0.8); font-size: 14px;">
                ArcanSentinel analyse en temps réel:
            </p>
            <ul style="color: rgba(255, 255, 255, 0.8); font-size: 14px;">
                <li>Les changements instantanés de dynamique de jeu</li>
                <li>Les réactions immédiates des cotes en direct</li>
                <li>Les patterns d'énergie pendant le match</li>
                <li>Les moments critiques avec forte probabilité de but</li>
                <li>Les opportunités de paris optimales en live</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Affichage des matchs surveillés en direct
        if st.session_state.sentinel_monitored_live_matches:
            st.markdown("#### Matchs en direct sous surveillance")
            for match in st.session_state.sentinel_monitored_live_matches:
                # Simuler une progression du match
                current_minute = match.get('minute', "??'")
                if "'" in current_minute:
                    minute_num = int(current_minute.replace("'", ""))
                    minute_num += 3  # Avancer de quelques minutes
                    current_minute = f"{minute_num}'"
                
                st.markdown(f"""
                <div style="background: rgba(255, 51, 100, 0.15); border: 1px solid rgba(255, 51, 100, 0.3); 
                          border-radius: 5px; padding: 15px; margin-top: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="font-weight: bold; color: white;">
                            {match['home']} {match['score']} {match['away']}
                        </div>
                        <div style="color: #ff3364; font-weight: bold; font-size: 14px;">
                            {current_minute}
                        </div>
                    </div>
                    <div style="margin-top: 10px; font-size: 13px; color: rgba(255, 255, 255, 0.7);">
                        <span style="color: #01ff80;">●</span> Analyse en direct active
                    </div>
                    <div style="font-size: 12px; color: rgba(255, 255, 255, 0.5); margin-top: 5px;">
                        5 modules actifs • Seuil d'alerte: {match.get('alert_threshold', 5)}/10
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Information sur le traitement automatique
            st.markdown("""
            <div style="font-size: 13px; color: rgba(255, 255, 255, 0.7); border-left: 2px solid #ff3364; 
                      padding-left: 10px; margin-top: 15px;">
                Les insights détectés en direct sont automatiquement envoyés à l'onglet Notifications.
                <br><br>
                Les patterns détectés par ArcanSentinel sont transmis à D-forge pour analyse 
                et développement potentiel de nouveaux modules.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Aucun match en direct sous surveillance. Activez ArcanSentinel sur un match en cours pour recevoir des insights en temps réel.")
    
    # Affichage des indicateurs en temps réel si au moins un match est surveillé
    if st.session_state.sentinel_monitored_live_matches:
        st.markdown("### 🔄 Indicateurs ArcanSentinel en temps réel")
        
        # Prendre le premier match surveillé pour afficher des données
        active_match = st.session_state.sentinel_monitored_live_matches[0]
        
        st.markdown(f"""
        <div style="padding: 12px; border-radius: 8px; margin-bottom: 15px; 
                    background: rgba(255, 51, 100, 0.1); border: 1px solid rgba(255, 51, 100, 0.2);">
            <div style="font-weight: bold; font-size: 18px; color: white; margin-bottom: 8px;">
                {active_match['home']} {active_match['score']} {active_match['away']} • {active_match['minute']}
            </div>
            <div style="font-size: 13px; color: rgba(255, 255, 255, 0.7);">
                <span style="color: #ff3364; font-weight: bold;">ANALYSE EN DIRECT</span> • {active_match['league']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Surveillance simulée
        sentinel_metrics = [
            {"name": "Momentum", "value": 72, "delta": "+3", "color": "#01ff80"},
            {"name": "Variance de cote", "value": 0.18, "delta": "-0.05", "color": "#ffbe41"}, 
            {"name": "Pression collective", "value": 64, "delta": "+8", "color": "#01ff80"},
            {"name": "Cycle karmique", "value": 88, "delta": "+2", "color": "#01ff80"},
            {"name": "Anomalie structurelle", "value": 22, "delta": "-4", "color": "#ff3364"}
        ]
        
        cols = st.columns(len(sentinel_metrics))
        for i, metric in enumerate(sentinel_metrics):
            with cols[i]:
                st.markdown(f"""
                <div style="text-align: center; padding: 10px;">
                    <div style="font-size: 14px; color: rgba(255, 255, 255, 0.7);">{metric['name']}</div>
                    <div style="font-size: 24px; font-weight: bold; color: {metric['color']};">{metric['value']}</div>
                    <div style="font-size: 12px; color: {metric['color']};">{metric['delta']}</div>
                </div>
                """, unsafe_allow_html=True)