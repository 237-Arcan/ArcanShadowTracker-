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

# Créer les onglets spécifiques au système ArcanShadow
tabs = st.tabs([
    "🔍 Live Monitoring", 
    "🔔 Performance Notifications", 
    "🎯 Daily Combo", 
    "💡 Smart Market Recommendations", 
    "🧠 Système d'Apprentissage"
])

with tabs[0]:  # Live Monitoring
    st.markdown("## 🔍 Suivi des Matchs en Direct")
    st.markdown("Visualisez les dynamiques de match en temps réel avec nos capteurs énergétiques avancés.")
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

with tabs[1]:  # Performance Notifications
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
    
    # Créer un graphique à barres horizontal
    fig = px.bar(
        df_modules, y="Module", x="Précision", 
        orientation='h',
        title="Précision par Module (30 derniers jours)",
        color="Précision",
        color_continuous_scale=["red", "gold", "green"],
        range_color=[0.5, 1.0],
        text=df_modules["Précision"].apply(lambda x: f"{x:.1%}"),
        size="Échantillon",
        size_max=50,
        height=500
    )
    
    fig.update_layout(
        xaxis_title="Précision (%)",
        yaxis_title="Module Prédictif",
        template="plotly_dark"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
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

with tabs[2]:  # Daily Combo
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
    
    # Créer un graphique camembert
    fig_modules = px.pie(
        values=module_weights, 
        names=modules_used,
        title="Pondération des modules pour le combiné",
        color_discrete_sequence=["#7000ff", "#01ff80", "#ffbe41", "#05d9e8"]
    )
    
    st.plotly_chart(fig_modules, use_container_width=True)
    
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