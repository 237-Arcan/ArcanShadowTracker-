import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import os

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

# Créer les onglets
tabs = st.tabs(["Dashboard", "Prédictions", "Analyse live", "Statistiques", "Match en direct"])

with tabs[0]:  # Dashboard
    # Panneau ésotérique dans la barre latérale
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
    st.markdown("## 🔮 Système de prédiction avancé")
    st.markdown("Cette section présente les prédictions détaillées générées par notre système ArcanShadow.")
    
    # Simulons des données de prédiction
    st.markdown("### 📊 Convergence des modèles")
    
    # Créer une visualisation de convergence avec Plotly
    models = ["ArcanX", "ShadowOdds", "NumeriCode", "KarmicFlow+", "AstroImpact"]
    match_outcomes = ["Home Win", "Draw", "Away Win"]
    
    # Générer des données aléatoires pour la démo
    data = []
    for model in models:
        for outcome in match_outcomes:
            confidence = np.random.uniform(0.1, 0.9)
            data.append({"Model": model, "Outcome": outcome, "Confidence": confidence})
    
    df = pd.DataFrame(data)
    
    # Créer un heatmap pour visualiser la convergence
    fig = px.density_heatmap(
        df, x="Model", y="Outcome", z="Confidence", 
        color_continuous_scale=["blue", "purple", "gold"],
        title="Convergence des modèles prédictifs"
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:  # Analyse live
    st.markdown("## 📊 Analyse des matchs en direct")
    st.markdown("Visualisez les dynamiques de match en temps réel avec nos outils d'analyse avancés.")
    
    # Simuler des données de momentum pour un match en direct
    match_time = list(range(0, 91, 5))
    home_momentum = [50 + np.random.normal(0, 10) for _ in match_time]
    away_momentum = [50 - m + 50 + np.random.normal(0, 5) for m in home_momentum]
    
    # Normaliser pour que la somme soit toujours 100
    for i in range(len(match_time)):
        total = home_momentum[i] + away_momentum[i]
        home_momentum[i] = (home_momentum[i] / total) * 100
        away_momentum[i] = (away_momentum[i] / total) * 100
    
    # Créer un dataframe
    momentum_data = pd.DataFrame({
        "Minute": match_time,
        "Domicile": home_momentum,
        "Extérieur": away_momentum
    })
    
    # Visualiser le momentum avec Plotly
    fig_momentum = px.line(
        momentum_data, x="Minute", y=["Domicile", "Extérieur"],
        title="Évolution du momentum (Real Madrid vs Barcelona)",
        color_discrete_sequence=["#01ff80", "#ff3364"]
    )
    
    fig_momentum.update_layout(
        xaxis_title="Minute de jeu",
        yaxis_title="Momentum (%)",
        legend_title="Équipe",
        template="plotly_dark"
    )
    
    st.plotly_chart(fig_momentum, use_container_width=True)

with tabs[3]:  # Statistiques
    st.markdown("## 📈 Statistiques avancées")
    st.markdown("Explorez les statistiques détaillées et les tendances historiques.")
    
    # Simuler des données pour les graphiques
    leagues = ["Ligue 1", "Premier League", "LaLiga", "Bundesliga", "Serie A"]
    home_win_rates = [np.random.uniform(0.4, 0.55) for _ in leagues]
    draw_rates = [np.random.uniform(0.2, 0.3) for _ in leagues]
    away_win_rates = [1 - h - d for h, d in zip(home_win_rates, draw_rates)]
    
    # Créer un dataframe
    outcome_data = pd.DataFrame({
        "League": leagues,
        "Home Win": home_win_rates,
        "Draw": draw_rates,
        "Away Win": away_win_rates
    })
    
    # Créer un graphique à barres empilées
    fig_outcomes = px.bar(
        outcome_data, x="League", y=["Home Win", "Draw", "Away Win"],
        title="Répartition des résultats par ligue (2024-2025)",
        color_discrete_sequence=["#01ff80", "#ffbe41", "#ff3364"]
    )
    
    fig_outcomes.update_layout(
        xaxis_title="Ligue",
        yaxis_title="Proportion",
        legend_title="Résultat",
        template="plotly_dark"
    )
    
    st.plotly_chart(fig_outcomes, use_container_width=True)

with tabs[4]:  # Match en direct
    st.markdown("## ⚽ Suivi de match en direct")
    st.markdown("Experience immersive de suivi de match avec analyse temps réel.")
    
    # Créer un affichage de match en direct simulé
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        st.markdown("### 🏠 Real Madrid")
        st.markdown("##### Formation: 4-3-3")
        st.markdown("##### Possession: 58%")
        
    with col2:
        st.markdown("""
        <div style="text-align: center; font-size: 24px; font-weight: bold;">
            2 - 1
        </div>
        <div style="text-align: center; font-size: 16px;">
            73'
        </div>
        """, unsafe_allow_html=True)
        
        # Afficher les événements du match
        st.markdown("""
        <div style="border-left: 2px solid #7000ff; padding-left: 10px; margin: 20px 0;">
            <div style="margin-bottom: 10px;"><span style="color: #01ff80;">⚽ 23'</span> - But par Mbappé (Real Madrid)</div>
            <div style="margin-bottom: 10px;"><span style="color: #ff3364;">🟨 45+2'</span> - Carton jaune pour Gavi (Barcelona)</div>
            <div style="margin-bottom: 10px;"><span style="color: #01ff80;">⚽ 58'</span> - But par Vinicius Jr (Real Madrid)</div>
            <div style="margin-bottom: 10px;"><span style="color: #01ff80;">⚽ 67'</span> - But par Lewandowski (Barcelona)</div>
            <div style="margin-bottom: 10px;"><span style="color: #ffbe41;">🔄 70'</span> - Remplacement: Yamal ⟶ Ferran Torres (Barcelona)</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("### 🛫 Barcelona")
        st.markdown("##### Formation: 4-3-3")
        st.markdown("##### Possession: 42%")
        
    # Afficher les prédictions en direct
    st.markdown("### 🔮 Prédictions en direct")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 15px; background: rgba(1, 255, 128, 0.1); border-radius: 10px; border: 1px solid rgba(1, 255, 128, 0.3);">
            <div style="font-size: 18px; font-weight: bold; color: #01ff80;">Real Madrid gagne</div>
            <div style="font-size: 24px; font-weight: bold;">78%</div>
            <div style="font-size: 14px; color: rgba(255, 255, 255, 0.7);">ArcanShadow</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 15px; background: rgba(255, 190, 65, 0.1); border-radius: 10px; border: 1px solid rgba(255, 190, 65, 0.3);">
            <div style="font-size: 18px; font-weight: bold; color: #ffbe41;">Match nul</div>
            <div style="font-size: 24px; font-weight: bold;">15%</div>
            <div style="font-size: 14px; color: rgba(255, 255, 255, 0.7);">ArcanShadow</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 15px; background: rgba(255, 51, 100, 0.1); border-radius: 10px; border: 1px solid rgba(255, 51, 100, 0.3);">
            <div style="font-size: 18px; font-weight: bold; color: #ff3364;">Barcelona gagne</div>
            <div style="font-size: 24px; font-weight: bold;">7%</div>
            <div style="font-size: 14px; color: rgba(255, 255, 255, 0.7);">ArcanShadow</div>
        </div>
        """, unsafe_allow_html=True)