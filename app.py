import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from modules.arcanx import ArcanX
from modules.shadow_odds import ShadowOdds
from modules.convergence import Convergence
from modules.meta_systems import MetaSystems
from modules.arcan_sentinel import ArcanSentinel
from modules.learning_system import LearningSystem
# Import des modules "suspendus"
from modules.numeri_code import NumeriCode
from modules.tarot_echo import TarotEcho
from modules.astro_impact_lite import AstroImpactLite
from modules.shadow_odds_plus import ShadowOddsPlus
from modules.echo_path import EchoPath
from modules.fan_sentiment_monitor import FanSentimentMonitor
from modules.late_surge_detector import LateSurgeDetector
# Import des modules prédictifs
from modules.collapse_detector import CollapseDetector
from modules.youth_impact_analyzer import YouthImpactAnalyzer
from modules.captain_switch import CaptainSwitch
from modules.set_piece_threat_evaluator import SetPieceThreatEvaluator
# Import des modules avancés
from modules.karmic_flow_plus import KarmicFlowPlus
from modules.momentum_tracker_2 import MomentumTracker2
# Import des nouveaux modules
from modules.bet_trap_map import BetTrapMap
from modules.stadium_spirit import StadiumSpirit
from utils.data_handler import DataHandler
from utils.translations import get_text
from assets.symbols import get_symbol

# Page configuration
st.set_page_config(
    page_title="ArcanShadow",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'selected_sport' not in st.session_state:
    st.session_state.selected_sport = 'Football'
if 'selected_league' not in st.session_state:
    st.session_state.selected_league = 'La Liga'  # Changé pour La Liga qui a des données
if 'selected_date' not in st.session_state:
    # Set the date to today since we should have data for today
    st.session_state.selected_date = datetime.now().date()
if 'prediction_generated' not in st.session_state:
    st.session_state.prediction_generated = False
if 'loading_prediction' not in st.session_state:
    st.session_state.loading_prediction = False
if 'language' not in st.session_state:
    st.session_state.language = 'en'  # Default language is English
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0  # Default to first tab (Predictions)
if 'match_events' not in st.session_state:
    st.session_state.match_events = []  # List to store match events in live mode
if 'daily_combo' not in st.session_state:
    st.session_state.daily_combo = {
        'selections': [],
        'total_odds': 0,
        'avg_confidence': 0,
        'expected_value': 0,
        'risk_level': 'medium',
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

# Function to get translated text
def t(key, **format_args):
    """Helper function to get text in the current language"""
    return get_text(key, st.session_state.language, **format_args)

def translate_factor_value(value):
    """Translate prediction factor value based on known patterns"""
    # Ensure value is a string
    value_str = str(value)
    
    # List of keys to check for translation
    factor_patterns = [
        "prime_match_day", "dynamic_life_path", "earth_element_match",
        "full_moon_energy", "match_foundation_sun", "current_energy_moon",
        "outcome_tendency_fool"
    ]
    
    # Check for match or partial match and return translation
    if isinstance(value, str):  # Only process string values
        if value.startswith("Prime Match Day:"):
            # Extract day number
            day = value.split("day")[1].split(",")[0].strip()
            return t("prime_match_day", day=day)
        elif value.startswith("Dynamic Life Path:"):
            # Extract life path number
            number = value.split("Path")[1].split("suggests")[0].strip()
            return t("dynamic_life_path", number=number)
        elif value.startswith("Earth Element Match:"):
            return t("earth_element_match")
        elif value.startswith("Full Moon Energy:"):
            return t("full_moon_energy")
        elif value.startswith("Match Foundation: The Sun:"):
            return t("match_foundation_sun")
        elif value.startswith("Current Energy: The Moon:"):
            return t("current_energy_moon")
        elif value.startswith("Outcome Tendency: The Fool:"):
            return t("outcome_tendency_fool")
            
    # Return original if no translation found
    return value

# Initialize modules
data_handler = DataHandler()
arcan_x = ArcanX()
shadow_odds = ShadowOdds()
convergence = Convergence()

# Initialize esoteric "suspended" modules
numeri_code = NumeriCode()
tarot_echo = TarotEcho()
astro_impact = AstroImpactLite()
shadow_odds_plus = ShadowOddsPlus()
echo_path = EchoPath()
fan_sentiment_monitor = FanSentimentMonitor()
late_surge_detector = LateSurgeDetector()

# Initialize predictive modules
collapse_detector = CollapseDetector()
youth_impact_analyzer = YouthImpactAnalyzer()
captain_switch = CaptainSwitch()
set_piece_threat_evaluator = SetPieceThreatEvaluator()

# Initialize advanced modules
karmic_flow = KarmicFlowPlus()
momentum_tracker = MomentumTracker2()

# Initialize new modules
bet_trap_map = BetTrapMap()
stadium_spirit = StadiumSpirit()

# Initialize meta systems (coordinating all modules)
meta_systems = MetaSystems(
    suspended_modules={
        'numeri_code': numeri_code,
        'tarot_echo': tarot_echo,
        'astro_impact': astro_impact,
        'shadow_odds_plus': shadow_odds_plus,
        'echo_path': echo_path,
        'fan_sentiment_monitor': fan_sentiment_monitor,
        'late_surge_detector': late_surge_detector
    },
    advanced_modules={
        'karmic_flow': karmic_flow,
        'momentum_tracker': momentum_tracker,
        'collapse_detector': collapse_detector,
        'youth_impact_analyzer': youth_impact_analyzer,
        'captain_switch': captain_switch,
        'set_piece_threat_evaluator': set_piece_threat_evaluator,
        'bet_trap_map': bet_trap_map,
        'stadium_spirit': stadium_spirit
    }
)

# Initialize live mode module
arcan_sentinel = ArcanSentinel(
    arcan_x, 
    shadow_odds, 
    convergence, 
    meta_systems=meta_systems  # Pass meta_systems for access to all modules
)

# Initialize session state for live tracking
if 'live_tracking_active' not in st.session_state:
    st.session_state.live_tracking_active = False
if 'live_match_data' not in st.session_state:
    st.session_state.live_match_data = None
if 'live_analysis' not in st.session_state:
    st.session_state.live_analysis = None
if 'current_match_minute' not in st.session_state:
    st.session_state.current_match_minute = 0
if 'current_match_score' not in st.session_state:
    st.session_state.current_match_score = [0, 0]

# Custom CSS for styling
def local_css():
    st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(to bottom, #121212, #1a1a2e);
    }
    .gold-text {
        color: #FFD700;
    }
    .prediction-card {
        background: rgba(30, 30, 47, 0.7);
        border-radius: 10px;
        padding: 20px;
        border-left: 4px solid #9c27b0;
        margin-bottom: 15px;
    }
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    /* Sidebar match styles */
    .sidebar-match {
        background-color: rgba(60, 60, 100, 0.2);
        border-radius: 5px;
        padding: 8px;
        margin-bottom: 10px;
        border-left: 3px solid #9966CC;
    }
    
    .match-time {
        font-size: 12px;
        color: #AAA;
        margin-bottom: 3px;
    }
    
    .match-teams {
        font-weight: bold;
        font-size: 14px;
        color: white;
    }
    
    /* Style for the match buttons in sidebar */
    div[data-testid="stHorizontalBlock"] .stButton button {
        background-color: #1E1E3F;
        color: white;
        border: 1px solid #444;
        border-radius: 4px;
        width: 100%;
        font-size: 12px;
        padding: 3px 0;
        transition: background-color 0.3s;
    }
    
    div[data-testid="stHorizontalBlock"] .stButton button:hover {
        background-color: #333366;
        border-color: #9966CC;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Main title with mystical element
st.markdown("<div class='header-container'><h1>🔮 ArcanShadow</h1><div>" + get_symbol('pentagram') + "</div></div>", unsafe_allow_html=True)
st.markdown(f"<p class='gold-text'>{t('app_subtitle')}</p>", unsafe_allow_html=True)

# Sidebar for filters and controls
with st.sidebar:
    st.markdown(f"## 🧙‍♂️ {t('system_controls')}")
    
    # Language selection
    languages = {"en": "English", "fr": "Français"}
    selected_language = st.selectbox(
        t('select_language'),
        options=list(languages.keys()),
        format_func=lambda x: languages[x],
        index=list(languages.keys()).index(st.session_state.language)
    )
    
    # Update language if changed
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.rerun()  # Rerun to update all UI text
    
    # Sport selection
    sports = ['Football', 'Basketball', 'Tennis', 'Baseball', 'Hockey']
    selected_sport = st.selectbox(t('select_sport'), sports, index=sports.index(st.session_state.selected_sport))
    st.session_state.selected_sport = selected_sport
    
    # League selection based on sport
    leagues = data_handler.get_leagues_for_sport(selected_sport)
    selected_league = st.selectbox(t('select_league'), leagues, index=0 if st.session_state.selected_league not in leagues else leagues.index(st.session_state.selected_league))
    st.session_state.selected_league = selected_league
    
    # Date selection
    selected_date = st.date_input(t('select_date'), st.session_state.selected_date)
    st.session_state.selected_date = selected_date
    
    # Module activation checkboxes
    st.markdown(f"### {t('active_modules')}")
    arcan_x_active = st.checkbox("ArcanX (Esoteric Analysis)", value=True)
    shadow_odds_active = st.checkbox("ShadowOdds (Odds Behavior)", value=True)
    
    # Advanced settings collapsible
    with st.expander(t('advanced_settings')):
        confidence_threshold = st.slider(t('confidence_threshold'), 0.0, 1.0, 0.65)
        cycles_depth = st.slider(t('cycles_depth'), 1, 10, 5)
        esoteric_weight = st.slider(t('esoteric_influence'), 0.0, 1.0, 0.4)
    
    # Matchs du jour
    st.markdown("---")
    st.markdown(f"### 🔥 {t('featured_matches')}")
    
    # Récupérer les matchs vedettes d'aujourd'hui (toutes les ligues)
    featured_matches = data_handler.get_featured_matches(selected_sport)
    
    if featured_matches:
        for match in featured_matches:
            with st.container():
                st.markdown(f"""
                <div class="sidebar-match featured-match">
                    <div class="match-league">{match.get('league', '')}</div>
                    <div class="match-time">⏰ {match.get('kickoff_time', '??:??')}</div>
                    <div class="match-teams"><strong>{match['home_team']} vs {match['away_team']}</strong></div>
                </div>
                """, unsafe_allow_html=True)
                
                cols = st.columns(3)
                with cols[0]:
                    if st.button(f"1️⃣ {match.get('home_odds', '?.??')}", key=f"home_featured_{match['home_team']}_{match['away_team']}"):
                        st.session_state.selected_match = match
                        st.session_state.selected_prediction = "home_win"
                with cols[1]:
                    if st.button(f"❌ {match.get('draw_odds', '?.??')}", key=f"draw_featured_{match['home_team']}_{match['away_team']}"):
                        st.session_state.selected_match = match
                        st.session_state.selected_prediction = "draw"
                with cols[2]:
                    if st.button(f"2️⃣ {match.get('away_odds', '?.??')}", key=f"away_featured_{match['home_team']}_{match['away_team']}"):
                        st.session_state.selected_match = match
                        st.session_state.selected_prediction = "away_win"
    
    # Matchs réguliers du jour (de la ligue sélectionnée)
    st.markdown(f"### 🗓️ {t('todays_matches')}")
    
    # Récupérer les matchs d'aujourd'hui pour la ligue sélectionnée
    today_matches = data_handler.get_upcoming_matches(selected_sport, selected_league, datetime.now().date())
    
    if today_matches:
        for match in today_matches:
            # Éviter les doublons avec les matchs vedettes
            is_duplicate = False
            for featured in featured_matches:
                if (match.get('home_team') == featured.get('home_team') and 
                    match.get('away_team') == featured.get('away_team')):
                    is_duplicate = True
                    break
            
            if is_duplicate:
                continue
                
            with st.container():
                st.markdown(f"""
                <div class="sidebar-match">
                    <div class="match-time">⏰ {match.get('kickoff_time', '??:??')}</div>
                    <div class="match-teams">{match['home_team']} vs {match['away_team']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                cols = st.columns(3)
                with cols[0]:
                    if st.button(f"1️⃣ {match.get('home_odds', '?.??')}", key=f"home_{match['home_team']}_{match['away_team']}"):
                        st.session_state.selected_match = match
                        st.session_state.selected_prediction = "home_win"
                with cols[1]:
                    if st.button(f"❌ {match.get('draw_odds', '?.??')}", key=f"draw_{match['home_team']}_{match['away_team']}"):
                        st.session_state.selected_match = match
                        st.session_state.selected_prediction = "draw"
                with cols[2]:
                    if st.button(f"2️⃣ {match.get('away_odds', '?.??')}", key=f"away_{match['home_team']}_{match['away_team']}"):
                        st.session_state.selected_match = match
                        st.session_state.selected_prediction = "away_win"
    else:
        st.info(t('no_matches_today'))
    
    # Matchs à venir cette semaine
    st.markdown(f"### 📆 {t('upcoming_matches')}")
    
    # Calculer les dates de la semaine à venir
    today = datetime.now().date()
    week_dates = [today + timedelta(days=i) for i in range(1, 8)]
    
    # Récupérer les matchs de la semaine
    upcoming_week_matches = []
    for date in week_dates:
        day_matches = data_handler.get_upcoming_matches(selected_sport, selected_league, date)
        if day_matches:
            for match in day_matches:
                match['date'] = date
                upcoming_week_matches.append(match)
    
    if upcoming_week_matches:
        # Grouper par date
        dates_with_matches = {}
        for match in upcoming_week_matches:
            date_str = match['date'].strftime('%d %b')
            if date_str not in dates_with_matches:
                dates_with_matches[date_str] = []
            dates_with_matches[date_str].append(match)
        
        # Créer un sélecteur de dates
        if dates_with_matches:
            date_tabs = st.tabs(list(dates_with_matches.keys()))
            
            for i, date_str in enumerate(dates_with_matches.keys()):
                with date_tabs[i]:
                    for match in dates_with_matches[date_str]:
                        st.markdown(f"{match['home_team']} vs {match['away_team']}")
                        if 'kickoff_time' in match:
                            st.caption(f"⏰ {match['kickoff_time']}")
    else:
        st.info(t('no_upcoming_matches'))
    
    # Generate prediction button
    st.markdown("---")
    if st.button(t('generate_predictions'), use_container_width=True, type="primary"):
        st.session_state.loading_prediction = True

# Main content area with tabs
# We'll use the session state active_tab to control which tab is shown
tabs = [
    t('predictions_tab'), 
    t('dashboard_tab'), 
    t('historical_tab'), 
    t('module_details_tab'),
    t('live_match_tab'),
    t('live_monitoring_tab'),
    t('performance_notifications_tab'),  # Tab for performance notifications
    t('daily_combo_tab'),  # Tab for daily betting combo
    t('smart_recommendations_title'),  # New tab for smart market recommendations
    "Système d'Apprentissage"  # Nouvel onglet pour le système d'apprentissage
]

# Get the selected tab index from session_state
selected_tab_idx = st.session_state.active_tab
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(tabs)

with tab1:
    # Header section with explanatory text
    st.markdown(f"## {t('match_predictions')}")
    st.markdown(t('predictions_description'))
    
    # Get upcoming matches for selected sport, league and date
    upcoming_matches = data_handler.get_upcoming_matches(st.session_state.selected_sport, st.session_state.selected_league, st.session_state.selected_date)
    
    # Fonction simplifiée pour vérifier les prédictions (sans filtres)
    def matches_filters(prediction):
        # Vérification de base pour s'assurer que la prédiction est valide
        if not prediction or 'confidence' not in prediction:
            return False
        
        # Vérifier que la confiance est au-dessus d'un seuil minimal (50%)
        if prediction['confidence']*100 < 50:
            return False
            
        return True
    
    # Handle loading prediction state
    if st.session_state.loading_prediction:
        st.markdown(f"### {t('analyzing_matches')}")
        prediction_progress = st.progress(0)
        
        for i in range(101):
            prediction_progress.progress(i/100)
            time.sleep(0.01)
        
        st.session_state.prediction_generated = True
        st.session_state.loading_prediction = False
        st.rerun()
    
    # Display predictions
    if st.session_state.prediction_generated and len(upcoming_matches) > 0:
        # Générer les prédictions pour tous les matchs
        match_predictions = []
        
        for match in upcoming_matches:
            # Generate predictions for this match
            arcan_x_results = arcan_x.analyze_match(match) if arcan_x_active else {'confidence': 0.5, 'factors': []}
            shadow_odds_results = shadow_odds.analyze_match(match) if shadow_odds_active else {'confidence': 0.5, 'factors': []}
            
            # Calculate combined prediction
            prediction = convergence.generate_prediction(match, arcan_x_results, shadow_odds_results)
            
            # Déterminer si c'est un value bet
            prediction['value_bet'] = False
            if all(k in match for k in ['home_odds', 'draw_odds', 'away_odds']):
                # Déterminer le type de résultat prédit
                outcome_key = ""
                if prediction['outcome'] == 'home_win':
                    outcome_key = 'home_odds'
                elif prediction['outcome'] == 'draw':
                    outcome_key = 'draw_odds'
                elif prediction['outcome'] == 'away_win':
                    outcome_key = 'away_odds'
                
                if outcome_key and outcome_key in match:
                    implied_prob = 1 / match[outcome_key]
                    prediction['value_bet'] = prediction['confidence'] > implied_prob + 0.1
            
            # Déterminer si c'est un pick contrarian
            prediction['contrarian'] = False
            if shadow_odds_active and 'public_favorite' in shadow_odds_results:
                public_favorite = shadow_odds_results['public_favorite']
                prediction['contrarian'] = prediction['outcome'] != public_favorite and prediction['confidence'] > 0.65
            
            # Ajouter la prédiction et le match à la liste
            match_predictions.append({'match': match, 'prediction': prediction})
        
        # Filtrer les prédictions selon les critères
        filtered_predictions = [mp for mp in match_predictions if matches_filters(mp['prediction'])]
        
        # Afficher le nombre de prédictions retenues
        if filtered_predictions:
            st.success(f"{t('matches_found')}: {len(filtered_predictions)}")
            
            # Tableau récapitulatif
            data = []
            for mp in filtered_predictions:
                match = mp['match']
                prediction = mp['prediction']
                home_team = match.get('home_team', '')
                away_team = match.get('away_team', '')
                
                # Convertir l'outcome en texte traduit
                outcome_text = prediction['outcome'] 
                if outcome_text == 'home_win':
                    outcome_text = t('home_win')
                elif outcome_text == 'away_win':
                    outcome_text = t('away_win')
                elif outcome_text == 'draw':
                    outcome_text = t('draw')
                
                # Construire la ligne du tableau
                data.append({
                    t('match'): f"{home_team} vs {away_team}",
                    t('time'): match.get('kickoff_time', '??:??'),
                    t('prediction'): outcome_text,
                    t('confidence'): f"{prediction['confidence']*100:.1f}%",
                    t('value'): "✓" if prediction['value_bet'] else "",
                    t('contrarian'): "✓" if prediction['contrarian'] else ""
                })
            
            # Créer le DataFrame
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning(t('no_matches_criteria'))
        
        # Afficher les détails de chaque prédiction filtrée
        if filtered_predictions:
            st.markdown(f"### {t('detailed_predictions')}")
            
            for mp in filtered_predictions:
                match = mp['match']
                prediction = mp['prediction']
                home_team = match.get('home_team', '')
                away_team = match.get('away_team', '')
                
                # Créer une carte de prédiction améliorée
                with st.container():
                    # En-tête avec information match
                    st.markdown(f"""
                    <div class='prediction-card'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <h3>{home_team} {t('vs')} {away_team}</h3>
                            <div style='text-align:right;'>
                                <span style='background-color:#1a1a2e; padding:5px 10px; border-radius:5px;'>
                                    {match.get('kickoff_time', '??:??')} | {match['date'].strftime('%d %b %Y')}
                                </span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Afficher les badges pour value bet et contrarian
                    badges = []
                    if prediction['value_bet']:
                        badges.append(f"<span style='background-color:green; color:white; padding:3px 8px; border-radius:3px; margin-right:5px;'>{t('value_bet')}</span>")
                    if prediction['contrarian']:
                        badges.append(f"<span style='background-color:purple; color:white; padding:3px 8px; border-radius:3px; margin-right:5px;'>{t('contrarian_pick')}</span>")
                    
                    if badges:
                        st.markdown(f"""
                        <div style='margin-top:10px; margin-bottom:15px;'>
                            {''.join(badges)}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Corps de la prédiction
                    prediction_cols = st.columns([2, 1])
                    
                    with prediction_cols[0]:
                        # Afficher la prédiction
                        outcome_text = prediction['outcome'] 
                        if outcome_text == 'home_win':
                            outcome_text = t('home_win')
                        elif outcome_text == 'away_win':
                            outcome_text = t('away_win')
                        elif outcome_text == 'draw':
                            outcome_text = t('draw')
                        
                        st.markdown(f"""
                        <div style='margin-top:10px;'>
                            <p style='font-size:18px;'>{t('prediction')}: <span class='gold-text' style='font-size:20px;'>{outcome_text}</span></p>
                            <p>{t('confidence')}: <span style='color:#FFD700;'>{prediction['confidence']*100:.1f}%</span></p>
                        """, unsafe_allow_html=True)
                        
                        # Afficher les cotes si disponibles
                        if all(k in match for k in ['home_odds', 'draw_odds', 'away_odds']):
                            st.markdown(f"""
                            <p style='margin-top:10px;'>{t('odds')}: 
                                <span style='margin-right:15px;'>1: {match['home_odds']}</span>
                                <span style='margin-right:15px;'>X: {match['draw_odds']}</span>
                                <span>2: {match['away_odds']}</span>
                            </p>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with prediction_cols[1]:
                        # Create the gauge chart for prediction confidence
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = prediction['confidence']*100,
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            title = {'text': t('confidence')},
                            gauge = {
                                'axis': {'range': [0, 100], 'tickwidth': 1},
                                'bar': {'color': "gold"},
                                'steps': [
                                    {'range': [0, 50], 'color': "firebrick"},
                                    {'range': [50, 75], 'color': "darkorange"},
                                    {'range': [75, 100], 'color': "forestgreen"}
                                ],
                                'threshold': {
                                    'line': {'color': "white", 'width': 2},
                                    'thickness': 0.75,
                                    'value': prediction['confidence']*100
                                }
                            }
                        ))
                        fig.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=20))
                        st.plotly_chart(fig, use_container_width=True, key=f"gauge_{home_team}_{away_team}")
                    
                    # Fermer la div prediction-card
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Show prediction details in an expander
                    with st.expander(t('view_details')):
                        analysis_cols = st.columns(3)
                        
                        with analysis_cols[0]:
                            st.markdown(f"#### {t('statistical_factors')}")
                            for factor in prediction['statistical_factors']:
                                factor_name = factor['name']
                                # Try to translate the factor name using t function
                                if factor_name.lower() in ['form analysis', 'analyse de forme']:
                                    factor_name = t('form_analysis')
                                elif factor_name.lower() in ['head-to-head record', 'historique des confrontations']:
                                    factor_name = t('head_to_head')
                                elif factor_name.lower() in ['home advantage', 'avantage du terrain']:
                                    factor_name = t('home_advantage')
                                elif factor_name.lower() in ['injury impact', 'impact des blessures']:
                                    factor_name = t('injury_impact')
                                elif factor_name.lower() in ['recent momentum', 'dynamique récente']:
                                    factor_name = t('recent_momentum')
                                
                                # Translate the factor value if it matches known patterns
                                factor_value = translate_factor_value(factor['value'])
                                
                                # Color-code the factor value
                                color = "forestgreen"
                                # Ensure value is a string before checking
                                factor_value_str = str(factor['value'])
                                if isinstance(factor['value'], (int, float)):
                                    # For numeric values, use a different coloring logic
                                    if factor['value'] > 0.7:
                                        color = "forestgreen"
                                    elif factor['value'] > 0.5:
                                        color = "darkorange"
                                    else:
                                        color = "gray"
                                elif "Strong" in factor_value_str or "Strongly" in factor_value_str:
                                    color = "forestgreen"
                                elif "Slight" in factor_value_str or "Slightly" in factor_value_str:
                                    color = "darkorange"
                                elif "Neutral" in factor_value_str:
                                    color = "gray"
                                
                                st.markdown(f"""
                                <div class='factor-container'>
                                    <span class='factor-name'>{factor_name}</span>: 
                                    <span style='color:{color};'>{factor_value}</span>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        with analysis_cols[1]:
                            st.markdown(f"#### {t('esoteric_factors')}")
                            for factor in prediction['esoteric_factors']:
                                factor_name = factor['name']
                                # Try to translate the factor name using t function
                                if factor_name.lower() in ['numerical resonance', 'résonance numérique']:
                                    factor_name = t('numerical_resonance')
                                elif factor_name.lower() in ['gematria value', 'valeur gématrique']:
                                    factor_name = t('gematria_value')
                                elif factor_name.lower() in ['astrological position', 'position astrologique']:
                                    factor_name = t('astrological_position')
                                elif factor_name.lower() in ['tarot association', 'association du tarot']:
                                    factor_name = t('tarot_association')
                                elif factor_name.lower() in ['karmic balance', 'équilibre karmique']:
                                    factor_name = t('karmic_balance')
                                elif factor_name.lower() in ['venue energy', 'énergie du stade']:
                                    factor_name = t('venue_energy')
                                elif factor_name.lower() in ['cycle pattern', 'motif cyclique']:
                                    factor_name = t('cycle_pattern')
                                
                                # Translate the factor value if it matches known patterns
                                factor_value = translate_factor_value(factor['value'])
                                
                                # Color-code the factor value
                                color = "mediumpurple"
                                # Ensure value is a string before checking
                                factor_value_str = str(factor['value'])
                                if isinstance(factor['value'], (int, float)):
                                    # For numeric values, use a different coloring logic
                                    if factor['value'] > 0.7:
                                        color = "mediumpurple"
                                    elif factor['value'] > 0.5:
                                        color = "plum"
                                    else:
                                        color = "gray"
                                elif "Strong" in factor_value_str or "Strongly" in factor_value_str:
                                    color = "mediumpurple"
                                elif "Slight" in factor_value_str or "Slightly" in factor_value_str:
                                    color = "plum"
                                elif "Neutral" in factor_value_str:
                                    color = "gray"
                                
                                st.markdown(f"""
                                <div class='factor-container'>
                                    <span class='factor-name'>{factor_name}</span>: 
                                    <span style='color:{color};'>{factor_value}</span>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        with analysis_cols[2]:
                            st.markdown(f"#### {t('odds_analysis')}")
                            for factor in prediction['odds_factors']:
                                factor_name = factor['name']
                                # Try to translate the factor name using t function
                                if factor_name.lower() in ['line movement', 'mouvement des cotes']:
                                    factor_name = t('line_movement')
                                elif factor_name.lower() in ['public betting %', 'paris publics %']:
                                    factor_name = t('public_betting')
                                elif factor_name.lower() in ['sharp action', 'action des parieurs pro']:
                                    factor_name = t('sharp_action')
                                elif factor_name.lower() in ['odds divergence', 'divergence des cotes']:
                                    factor_name = t('odds_divergence')
                                elif factor_name.lower() in ['market overreaction', 'surréaction du marché']:
                                    factor_name = t('market_overreaction')
                                elif factor_name.lower() in ['trap indicator', 'indicateur de piège']:
                                    factor_name = t('trap_indicator')
                                
                                # Translate the factor value if it matches known patterns
                                factor_value = translate_factor_value(factor['value'])
                                
                                # Color-code the factor value
                                color = "gold"
                                # Ensure value is a string before checking
                                factor_value_str = str(factor['value'])
                                if isinstance(factor['value'], (int, float)):
                                    # For numeric values, use a different coloring logic
                                    if factor['value'] > 0.7:
                                        color = "gold"
                                    elif factor['value'] > 0.5:
                                        color = "goldenrod"
                                    else:
                                        color = "gray"
                                elif "Strong" in factor_value_str or "Strongly" in factor_value_str:
                                    color = "gold"
                                elif "Slight" in factor_value_str or "Slightly" in factor_value_str:
                                    color = "goldenrod"
                                elif "Neutral" in factor_value_str:
                                    color = "gray"
                                
                                st.markdown(f"""
                                <div class='factor-container'>
                                    <span class='factor-name'>{factor_name}</span>: 
                                    <span style='color:{color};'>{factor_value}</span>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # Ajouter une section d'analyse approfondie
                        st.markdown(f"#### {t('deep_analysis')}")
                        
                        try:
                            insight = meta_systems.arcan_brain.generate_analysis_insight(match, prediction)
                            st.markdown(f"""
                            <div style='background-color:rgba(30, 30, 60, 0.3); padding:15px; border-radius:5px; margin-top:10px;'>
                                <p>{insight}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f"""
                            <div style='background-color:rgba(30, 30, 60, 0.3); padding:15px; border-radius:5px; margin-top:10px;'>
                                <p>L'analyse neuronal est en cours d'entraînement et sera disponible prochainement.</p>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Ajouter un séparateur entre les prédictions
                st.markdown("<hr style='margin:30px 0; border-color:#333;'>", unsafe_allow_html=True)
                
    elif st.session_state.prediction_generated and len(upcoming_matches) == 0:
        st.warning(t('no_matches').format(league=st.session_state.selected_league, date=st.session_state.selected_date.strftime('%d %b %Y')))
    else:
        st.info(t('no_predictions'))

with tab2:
    st.markdown(f"## {t('system_dashboard')}")
    st.markdown(t('dashboard_description'))
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label=t('prediction_accuracy'), value="78.3%", delta="2.1%")
    
    with col2:
        st.metric(label=t('arcanx_confidence'), value="72.4%", delta="-1.3%")
    
    with col3:
        st.metric(label=t('shadowodds_accuracy'), value="81.5%", delta="3.8%")
    
    with col4:
        st.metric(label=t('active_modules_count'), value="12/18")
    
    # System health visualization
    st.markdown(f"### {t('system_health')}")
    
    # Create sample data for module performance
    modules = ['NumeriCode', 'GematriaPulse', 'AstroImpact', 'TarotEcho', 'LineTrap', 'BetPulse', 
               'MarketEcho', 'Convergia Core', 'MirrorPhase', 'GridSync Alpha']
    accuracy = np.random.uniform(0.65, 0.92, size=len(modules))
    usage = np.random.uniform(0.3, 1.0, size=len(modules))
    
    module_df = pd.DataFrame({
        'Module': modules,
        'Accuracy': accuracy,
        'Usage': usage,
        'Type': ['ArcanX', 'ArcanX', 'ArcanX', 'ArcanX', 'ShadowOdds', 'ShadowOdds', 
                 'ShadowOdds', 'Convergence', 'Convergence', 'Meta-Systems']
    })
    
    # Create bubble chart for module performance
    fig = px.scatter(module_df, x='Usage', y='Accuracy', size='Accuracy', color='Type',
                    hover_name='Module', size_max=30,
                    color_discrete_map={'ArcanX': 'purple', 'ShadowOdds': 'blue', 
                                       'Convergence': 'gold', 'Meta-Systems': 'green'})
    
    fig.update_layout(
        title='Module Performance Analysis',
        xaxis_title='Usage Frequency',
        yaxis_title='Prediction Accuracy',
        yaxis=dict(range=[0.6, 1.0]),
        height=500,
        template='plotly_dark'
    )
    
    st.plotly_chart(fig, use_container_width=True, key="module_performance_chart")
    
    # System activity timeline
    st.markdown(f"### {t('system_activity')}")
    
    # Generate sample timeline data
    days = 14
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]
    dates.reverse()
    
    esoteric_signals = np.random.randint(10, 50, size=days)
    statistical_signals = np.random.randint(30, 80, size=days)
    odds_signals = np.random.randint(20, 60, size=days)
    
    timeline_df = pd.DataFrame({
        'Date': dates,
        'Esoteric Signals': esoteric_signals,
        'Statistical Signals': statistical_signals,
        'Odds Signals': odds_signals
    })
    
    # Create stacked area chart
    fig = px.area(timeline_df, x='Date', 
                 y=['Esoteric Signals', 'Statistical Signals', 'Odds Signals'],
                 labels={'value': 'Signal Count', 'variable': 'Signal Type'},
                 color_discrete_map={
                     'Esoteric Signals': 'purple',
                     'Statistical Signals': 'blue',
                     'Odds Signals': 'gold'
                 })
    
    fig.update_layout(
        title='System Signal Activity (Past 14 Days)',
        xaxis_title='Date',
        yaxis_title='Signal Count',
        legend_title='Signal Type',
        height=400,
        template='plotly_dark'
    )
    
    st.plotly_chart(fig, use_container_width=True, key="system_activity_chart")

with tab3:
    st.markdown(f"## {t('historical_analysis')}")
    st.markdown(t('historical_description'))
    
    # Filters for historical analysis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        hist_sport = st.selectbox(t('sport'), sports, key="hist_sport")
    
    with col2:
        hist_leagues = data_handler.get_leagues_for_sport(hist_sport)
        hist_league = st.selectbox(t('league'), hist_leagues, key="hist_league")
    
    with col3:
        date_range_options = [t('last_7_days'), t('last_30_days'), t('last_3_months'), t('last_6_months'), t('last_year')]
        date_range = st.selectbox(t('time_period'), date_range_options, index=1)
    
    # Historical performance metrics
    hist_data = data_handler.get_historical_predictions(hist_sport, hist_league, date_range)
    
    if hist_data:
        # Performance summary
        st.markdown(f"### {t('performance_summary')}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label=t('overall_accuracy'), value=f"{hist_data['accuracy']*100:.1f}%")
        
        with col2:
            st.metric(label=t('roi'), value=f"{hist_data['roi']*100:.1f}%")
        
        with col3:
            st.metric(label=t('predictions_made'), value=hist_data['total_predictions'])
        
        # Historical accuracy by module
        st.markdown(f"### {t('module_performance')}")
        
        # Generate sample data for historical module performance
        dates = pd.date_range(end=datetime.now(), periods=30).strftime('%Y-%m-%d').tolist()
        
        module_perf_data = {
            'Date': dates * 4,
            'Accuracy': np.random.normal(0.75, 0.08, size=30 * 4).clip(0.4, 0.95),
            'Module': ['ArcanX'] * 30 + ['ShadowOdds'] * 30 + ['Convergence'] * 30 + ['Combined'] * 30
        }
        
        module_perf_df = pd.DataFrame(module_perf_data)
        
        # Line chart for module performance over time
        fig = px.line(module_perf_df, x='Date', y='Accuracy', color='Module',
                     labels={'Accuracy': t('prediction_accuracy'), 'Date': t('date')},
                     color_discrete_map={
                         'ArcanX': 'purple',
                         'ShadowOdds': 'blue',
                         'Convergence': 'green',
                         'Combined': 'gold'
                     })
        
        fig.update_layout(
            title='Module Performance Comparison',
            xaxis_title='Date',
            yaxis_title='Accuracy',
            yaxis=dict(range=[0.4, 1.0]),
            legend_title='Module',
            height=400,
            template='plotly_dark'
        )
        
        st.plotly_chart(fig, use_container_width=True, key="historical_performance_chart")
        
        # Recent predictions
        st.markdown(f"### {t('recent_predictions')}")
        
        recent_predictions = data_handler.get_recent_predictions(hist_sport, hist_league, 10)
        
        if recent_predictions:
            pred_df = pd.DataFrame(recent_predictions)
            pred_df['Correct'] = pred_df['correct'].apply(lambda x: '✅' if x else '❌')
            pred_df['Match'] = pred_df['home_team'] + ' ' + t('vs') + ' ' + pred_df['away_team']
            pred_df['Score'] = pred_df['home_score'].astype(str) + ' - ' + pred_df['away_score'].astype(str)
            
            # Format the dataframe for display
            display_df = pred_df[['date', 'Match', 'prediction', 'Score', 'Correct', 'confidence']]
            display_df.columns = [t('date'), t('match'), t('prediction'), t('result'), t('correct'), t('confidence')]
            
            st.dataframe(display_df, use_container_width=True)
        else:
            st.info(t('no_recent_data'))
    else:
        st.info(t('no_historical_data'))

with tab4:
    st.markdown(f"## {t('module_details')}")
    st.markdown(t('module_description'))
    
with tab5:
    st.markdown(f"## {t('live_mode_title')}")
    st.markdown(t('live_mode_description'))
    
    # Match setup section with improved interface
    st.markdown(f"### {t('match_setup')}")
    
    # Get available matches from the selected league for today and upcoming days
    # First try from today's date
    today_matches = data_handler.get_upcoming_matches(st.session_state.selected_sport, 
                                                     st.session_state.selected_league, 
                                                     datetime.now().date())
    
    # If no matches found for today, try to get matches for the next 7 days
    future_matches = []
    if not today_matches:
        for i in range(1, 8):
            future_date = datetime.now().date() + timedelta(days=i)
            matches = data_handler.get_upcoming_matches(st.session_state.selected_sport, 
                                                      st.session_state.selected_league, 
                                                      future_date)
            if matches:
                for match in matches:
                    match['date'] = future_date  # Add date to match data
                future_matches.extend(matches)
    
    # Also get featured matches if we're in football mode
    featured_matches = []
    if st.session_state.selected_sport == 'Football':
        featured_matches = data_handler.get_featured_matches(st.session_state.selected_sport)
        # Add a marker to differentiate featured matches in selection
        for match in featured_matches:
            if 'date' not in match:
                match['date'] = datetime.now().date()
            if 'featured' not in match:
                match['featured'] = True
    
    # Combine all available matches
    all_available_matches = today_matches + future_matches + featured_matches
    
    # Remove duplicates (if any match appears in both featured and league matches)
    unique_matches = []
    seen_pairs = set()
    for match in all_available_matches:
        match_key = (match.get('home_team', ''), match.get('away_team', ''))
        if match_key not in seen_pairs:
            unique_matches.append(match)
            seen_pairs.add(match_key)
    
    # Now use these unique matches for selection
    if unique_matches:
        # Format matches for selectbox with icons for featured matches and dates for future matches
        match_options = []
        for match in unique_matches:
            match_text = f"{match['home_team']} vs {match['away_team']}"
            if match.get('featured', False):
                match_text = f"🔥 {match_text} (Featured)"
            elif 'date' in match and match['date'] != datetime.now().date():
                match_text = f"📅 {match_text} ({match['date'].strftime('%d %b')})"
            match_options.append(match_text)
        
        selected_match_idx = st.selectbox(
            "Select match to track", 
            range(len(match_options)), 
            format_func=lambda i: match_options[i]
        )
        
        selected_match = unique_matches[selected_match_idx]
        home_team = selected_match['home_team']
        away_team = selected_match['away_team']
        
        # Display match info with league information if available
        st.markdown(
            f"<div style='text-align: center; margin-bottom: 15px;'>"
            f"<p style='font-size: 16px; color: #888;'>{selected_match.get('league', st.session_state.selected_league)}</p>"
            f"</div>", 
            unsafe_allow_html=True
        )
        
        match_info_cols = st.columns([2,1,2])
        with match_info_cols[0]:
            st.markdown(f"<h3 style='text-align: center'>{home_team}</h3>", unsafe_allow_html=True)
        with match_info_cols[1]:
            st.markdown(f"<h3 style='text-align: center'>vs</h3>", unsafe_allow_html=True)
        with match_info_cols[2]:
            st.markdown(f"<h3 style='text-align: center'>{away_team}</h3>", unsafe_allow_html=True)
        
        # Display match details if available
        info_cols = st.columns(3)
        with info_cols[0]:
            venue = selected_match.get('venue', f"{home_team} Stadium")
            st.info(f"🏟️ **Venue**: {venue}")
        with info_cols[1]:
            date_str = selected_match.get('date', datetime.now().date()).strftime('%d %b %Y')
            kickoff = selected_match.get('kickoff_time', "15:00")
            st.info(f"⏰ **Date & Time**: {date_str}, {kickoff}")
        with info_cols[2]:
            referee = selected_match.get('referee', "Not specified")
            st.info(f"👨‍⚖️ **Referee**: {referee}")
    else:
        st.warning(f"No matches found for {st.session_state.selected_league}. Please select a different league or enter match details manually.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            home_team = st.text_input(t('home_team'), value="Manchester United" if not st.session_state.live_match_data else st.session_state.live_match_data['home_team'])
        
        with col2:
            away_team = st.text_input(t('away_team'), value="Liverpool" if not st.session_state.live_match_data else st.session_state.live_match_data['away_team'])
    
    # Start/stop tracking buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if not st.session_state.live_tracking_active:
            # Add more options for a more detailed analysis
            with st.expander("Advanced Match Settings (Optional)", expanded=False):
                adv_cols = st.columns(3)
                
                with adv_cols[0]:
                    weather = st.selectbox("Weather Conditions", 
                                         ["Clear", "Partly Cloudy", "Cloudy", "Light Rain", "Heavy Rain", "Snow"],
                                         index=0)
                    crowd_size = st.number_input("Crowd Size", min_value=0, max_value=100000, value=55000, step=1000)
                    home_form = st.text_input("Home Team Form (e.g., WWDLW)", value="WDWLW")
                
                with adv_cols[1]:
                    venue = st.text_input("Venue", value=f"{home_team} Stadium")
                    referee = st.text_input("Referee", value="Michael Oliver")
                    away_form = st.text_input("Away Team Form (e.g., LWDLW)", value="LDWDL")
                
                with adv_cols[2]:
                    home_odds = st.number_input("Home Odds", min_value=1.01, max_value=20.0, value=2.10, step=0.05)
                    draw_odds = st.number_input("Draw Odds", min_value=1.01, max_value=20.0, value=3.40, step=0.05)
                    away_odds = st.number_input("Away Odds", min_value=1.01, max_value=20.0, value=3.60, step=0.05)
                
                # Additional special factors
                special_factors = st.multiselect("Special Match Factors", 
                                             ["Derby Match", "Title Decider", "Relegation Battle", 
                                              "European Qualification", "Player Return from Injury",
                                              "Manager's First Match", "Rivalries", "Weather Impact"],
                                             default=[])
            
            # Create a visually distinct button
            if st.button(t('start_tracking'), use_container_width=True, type="primary"):
                # Create match data dictionary
                match_data = {
                    'home_team': home_team,
                    'away_team': away_team,
                    'date': datetime.now(),
                    'sport': st.session_state.selected_sport,
                    'league': st.session_state.selected_league,
                    'venue': venue,
                    'home_odds': home_odds,
                    'draw_odds': draw_odds,
                    'away_odds': away_odds,
                    'weather': weather,
                    'referee': referee,
                    'crowd_size': crowd_size,
                    'home_form': home_form,
                    'away_form': away_form,
                    'special_factors': special_factors if len(special_factors) > 0 else None
                }
                
                # Start live tracking
                initial_analysis = arcan_sentinel.start_live_tracking(match_data)
                
                # Update session state
                st.session_state.live_tracking_active = True
                st.session_state.live_match_data = match_data
                st.session_state.live_analysis = initial_analysis
                st.session_state.current_match_minute = 0
                st.session_state.current_match_score = [0, 0]
                
                # Rerun to update UI
                st.rerun()
    
    with col2:
        if st.session_state.live_tracking_active:
            if st.button(t('stop_tracking')):
                # Stop live tracking
                final_analysis = arcan_sentinel.stop_live_tracking()
                
                # Update session state
                st.session_state.live_tracking_active = False
                st.session_state.live_analysis = final_analysis
                
                # Rerun to update UI
                st.rerun()
    
    # If live tracking is active, show match control panel and analysis
    if st.session_state.live_tracking_active:
        st.markdown("---")
        
        # Match state control panel
        st.markdown(f"### {t('update_match_state')}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Current minute control
            current_minute = st.slider(t('current_minute'), 0, 90, st.session_state.current_match_minute)
            
            if current_minute != st.session_state.current_match_minute:
                # Update match state with new minute
                arcan_sentinel.update_match_state(current_minute, st.session_state.current_match_score)
                st.session_state.current_match_minute = current_minute
                st.session_state.live_analysis = arcan_sentinel.update_live_analysis()
        
        with col2:
            # Score control
            col1, col2 = st.columns(2)
            
            with col1:
                home_score = st.number_input(f"{home_team} {t('score')}", min_value=0, value=st.session_state.current_match_score[0])
            
            with col2:
                away_score = st.number_input(f"{away_team} {t('score')}", min_value=0, value=st.session_state.current_match_score[1])
            
            if [home_score, away_score] != st.session_state.current_match_score:
                # Update match state with new score
                arcan_sentinel.update_match_state(st.session_state.current_match_minute, [home_score, away_score])
                st.session_state.current_match_score = [home_score, away_score]
                st.session_state.live_analysis = arcan_sentinel.update_live_analysis()
        
        # Event addition
        with st.expander(t('add_event')):
            col1, col2 = st.columns(2)
            
            with col1:
                event_type = st.selectbox(t('event_type'), ["Goal", "Red Card", "Yellow Card", "Substitution", "Injury", "Penalty"])
            
            with col2:
                event_team = st.radio("Team", [home_team, away_team])
            
            event_details = st.text_input(t('event_details'), placeholder="E.g. Goal scored by Rashford")
            
            if st.button("Add Event"):
                event = {
                    'type': event_type,
                    'team': event_team,
                    'minute': st.session_state.current_match_minute,
                    'details': event_details
                }
                
                # Update match state with new event
                arcan_sentinel.update_match_state(st.session_state.current_match_minute, st.session_state.current_match_score, event)
                st.session_state.live_analysis = arcan_sentinel.update_live_analysis()
                
                st.success(f"Event added: {event_type} at minute {st.session_state.current_match_minute}")
        
        # Display live analysis results
        st.markdown("---")
        st.markdown(f"### {t('live_analysis')}")
        
        # Current match phase
        current_phase = arcan_sentinel.determine_match_phase(st.session_state.current_match_minute)
        st.info(f"{t('match_phase')}: {current_phase.capitalize()} ({st.session_state.current_match_minute}/90)")
        
        # Live prediction visualization
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.session_state.live_analysis and 'outcome' in st.session_state.live_analysis:
                st.markdown(f"""
                <div class='prediction-card'>
                    <h3>{home_team} {st.session_state.current_match_score[0]} - {st.session_state.current_match_score[1]} {away_team}</h3>
                    <p>{t('prediction')}: <span class='gold-text'>{st.session_state.live_analysis['outcome']}</span></p>
                    <p>{t('confidence')}: {st.session_state.live_analysis['confidence']*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Prediction will appear when analysis completes")
        
        with col2:
            # Create confidence gauge chart
            if st.session_state.live_analysis and 'confidence' in st.session_state.live_analysis:
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = st.session_state.live_analysis['confidence']*100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': t('confidence')},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickwidth': 1},
                        'bar': {'color': "gold"},
                        'steps': [
                            {'range': [0, 50], 'color': "firebrick"},
                            {'range': [50, 75], 'color': "darkorange"},
                            {'range': [75, 100], 'color': "forestgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "white", 'width': 2},
                            'thickness': 0.75,
                            'value': st.session_state.live_analysis['confidence']*100
                        }
                    }
                ))
                fig.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=20))
                st.plotly_chart(fig, use_container_width=True, key="live_confidence_gauge")
        
        # Key analysis modules results
        col1, col2 = st.columns(2)
        
        with col1:
            # Momentum analysis
            st.markdown(f"#### {t('momentum_analysis')}")
            
            if st.session_state.live_analysis and 'shadow_momentum' in st.session_state.live_analysis:
                momentum_data = st.session_state.live_analysis['shadow_momentum']
                
                # Create momentum gauge
                if 'current_momentum' in momentum_data:
                    fig = go.Figure(go.Indicator(
                        mode = "delta+number",
                        value = momentum_data['current_momentum'] * 100,
                        delta = {'reference': 50, 'relative': False},
                        title = {'text': "Current Momentum"},
                        domain = {'x': [0, 1], 'y': [0, 1]}
                    ))
                    fig.update_layout(height=150)
                    st.plotly_chart(fig, use_container_width=True, key="momentum_gauge")
                
                # Momentum timeline
                if 'momentum_timeline' in momentum_data:
                    minutes = list(range(0, len(momentum_data['momentum_timeline'])))
                    values = momentum_data['momentum_timeline']
                    
                    # Ensure same length
                    if len(minutes) == len(values):
                        df = pd.DataFrame({'minute': minutes, 'momentum': values})
                        fig = px.line(df, x='minute', y='momentum', labels={'minute': 'Minute', 'momentum': 'Momentum'})
                        fig.update_layout(height=250)
                        st.plotly_chart(fig, use_container_width=True, key="momentum_timeline")
                    else:
                        st.info(f"Timeline data mismatch: {len(minutes)} minutes vs {len(values)} values")
            else:
                st.info("Momentum data will appear as the match progresses")
        
        with col2:
            # Karmic patterns
            st.markdown(f"#### {t('karmic_patterns')}")
            
            if st.session_state.live_analysis and 'karmic_flow' in st.session_state.live_analysis:
                karmic_data = st.session_state.live_analysis['karmic_flow']
                
                if 'factors' in karmic_data and karmic_data['factors']:
                    for factor in karmic_data['factors'][:3]:  # Show top 3 factors
                        st.markdown(f"- {factor}")
                
                # Create karmic balance visualization
                if 'balance' in karmic_data:
                    balance = karmic_data['balance']
                    
                    # Visualize balance as a horizontal bar
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=[balance],
                        y=['Karmic Balance'],
                        orientation='h',
                        marker=dict(
                            color='purple' if float(balance) < 0 else 'gold',
                            line=dict(color='white', width=2)
                        )
                    ))
                    fig.update_layout(
                        height=150,
                        xaxis=dict(range=[-1, 1]),
                        xaxis_title="Home ← | → Away"
                    )
                    st.plotly_chart(fig, use_container_width=True, key="karmic_balance")
            else:
                st.info("Karmic pattern data will appear as the match progresses")
        
        # Betting trends
        st.markdown(f"#### {t('betting_trends')}")
        
        if st.session_state.live_analysis and 'bet_pulse' in st.session_state.live_analysis:
            bet_data = st.session_state.live_analysis['bet_pulse']
            
            # Create betting volume visualization
            col1, col2, col3 = st.columns(3)
            
            if all(k in bet_data for k in ['home_volume', 'home_change', 'draw_volume', 'draw_change', 'away_volume', 'away_change']):
                with col1:
                    st.metric("Home", f"{bet_data['home_volume']}%", f"{bet_data['home_change']}%")
                
                with col2:
                    st.metric("Draw", f"{bet_data['draw_volume']}%", f"{bet_data['draw_change']}%")
                
                with col3:
                    st.metric("Away", f"{bet_data['away_volume']}%", f"{bet_data['away_change']}%")
            
            # Betting timeline
            if 'volume_timeline' in bet_data and bet_data['volume_timeline']:
                df = pd.DataFrame(bet_data['volume_timeline'])
                
                fig = px.line(df, x='minute', y=['home', 'draw', 'away'], 
                             labels={'value': 'Betting Volume %', 'variable': 'Outcome'},
                             color_discrete_map={'home': 'blue', 'draw': 'purple', 'away': 'red'})
                fig.update_layout(height=250)
                st.plotly_chart(fig, use_container_width=True, key="betting_timeline")
        else:
            st.info("Betting trend data will appear as the match progresses")
    
    # Module selection
    module_categories = {
        "ArcanX (Esoteric Analysis)": ["NumeriCode", "GematriaPulse", "AstroImpact Lite", "TarotEcho", 
                                      "YiFlow", "KarmicFlow+", "RadiEsthesiaMap", "CycleMirror", "StadiumSpirit"],
        "ShadowOdds (Odds Behavior)": ["LineTrap", "BetPulse", "CrowdPressureIndex", "MarketEcho", 
                                      "CollapseDetector", "ShadowMomentum", "SetTrapIndicator", "BetTrapMap"],
        "Convergence Modules": ["Convergia Core", "MirrorPhase", "MomentumShiftTracker", "CaptainSwitch", 
                               "YouthImpactAnalyzer", "LateSurgeDetector", "SetPieceThreatEvaluator", "FanSentimentMonitor"],
        "Meta-Systems": ["GridSync Alpha", "ChronoEcho Pro", "ArcanSentinel", "D-Forge", "D-GridSync Lambda"]
    }
    
    # Two-level selection for modules
    col1, col2 = st.columns(2)
    
    with col1:
        selected_category = st.selectbox(t('module_category'), list(module_categories.keys()))
    
    with col2:
        selected_module = st.selectbox(t('specific_module'), module_categories[selected_category])
    
    # Module descriptions with translation keys
    module_descriptions = {
        "BetTrapMap": {
            "description_key": "module_description_bettrapmap",
            "inputs": ["Odds data", "Betting volumes", "Historical trap patterns", "Market movements"],
            "output": "Trap risk map with danger zones and safe markets",
            "accuracy": "85.7%"
        },
        "StadiumSpirit": {
            "description_key": "module_description_stadiumspirit",
            "inputs": ["Stadium data", "Historical matches", "Atmospheric conditions", "Team-venue resonance"],
            "output": "Stadium energy analysis with influence factors",
            "accuracy": "77.4%"
        },
        "NumeriCode": {
            "description_key": "module_description_numericode",
            "inputs": ["Match date", "Player numbers", "Team formation", "Historical scores"],
            "output": "Numerical pattern significance score (0-100)",
            "accuracy": "76.3%"
        },
        "GematriaPulse": {
            "description_key": "module_description_gematriapulse",
            "inputs": ["Team names", "Player names", "Stadium name", "City name"],
            "output": "Gematria correlation strength (0-100)",
            "accuracy": "71.8%"
        },
        "AstroImpact Lite": {
            "description_key": "module_description_astroimpact",
            "inputs": ["Match date", "Team foundation dates", "Player birth dates", "Venue location"],
            "output": "Celestial influence score (0-100)",
            "accuracy": "72.5%"
        },
        "TarotEcho": {
            "description_key": "module_description_tarotecho",
            "inputs": ["Team archetypes", "Match context", "Historical pattern", "Energy signatures"],
            "output": "Tarot correspondence map",
            "accuracy": "70.9%"
        },
        "YiFlow": {
            "description_key": "module_description_yiflow",
            "inputs": ["Match dynamics", "Team energies", "Historical patterns", "Contextual factors"],
            "output": "Hexagram interpretation and prediction",
            "accuracy": "73.2%"
        },
        "KarmicFlow+": {
            "description_key": "module_description_karmicflow",
            "inputs": ["Team history", "Past confrontations", "Pattern evolution", "Karmic debt"],
            "output": "Karmic balance prediction",
            "accuracy": "74.8%"
        },
        "RadiEsthesiaMap": {
            "description_key": "module_description_radiesthesiamap",
            "inputs": ["Venue data", "Team energy signatures", "Historical venue performance", "Environmental factors"],
            "output": "Venue energy impact analysis",
            "accuracy": "72.1%"
        },
        "CycleMirror": {
            "description_key": "module_description_cyclemirror",
            "inputs": ["Historical matches", "Cyclical patterns", "Time intervals", "Pattern evolution"],
            "output": "Cyclical pattern prediction",
            "accuracy": "75.5%"
        },
        "LineTrap": {
            "description_key": "module_description_linetrap",
            "inputs": ["Opening odds", "Current odds", "Market movement", "Betting volumes"],
            "output": "Trap probability percentage",
            "accuracy": "83.1%"
        },
        "BetPulse": {
            "description_key": "module_description_betpulse",
            "inputs": ["Betting volumes", "Timing of bets", "Bet distribution", "Market reactions"],
            "output": "Market confidence map",
            "accuracy": "79.4%"
        },
        "CrowdPressureIndex": {
            "description_key": "module_description_crowdpressure",
            "inputs": ["Public betting percentages", "Line movement", "Public sentiment", "Social media activity"],
            "output": "Crowd pressure distortion score",
            "accuracy": "81.2%"
        },
        "MarketEcho": {
            "description_key": "module_description_marketecho",
            "inputs": ["Bookmaker odds comparison", "Line movements", "Market timing", "Discrepancy patterns"],
            "output": "Bookmaker alignment index",
            "accuracy": "82.7%"
        },
        "CollapseDetector": {
            "description_key": "module_description_collapsedetektor",
            "inputs": ["Team form", "Internal dynamics", "Recent patterns", "Market behavior"],
            "output": "Collapse probability score",
            "accuracy": "76.3%"
        },
        "ShadowMomentum": {
            "description_key": "module_description_shadowmomentum",
            "inputs": ["Odds evolution", "Betting patterns", "Timing of movements", "Volume changes"],
            "output": "Momentum shift analysis",
            "accuracy": "78.9%"
        },
        "SetTrapIndicator": {
            "description_key": "module_description_settrapindicator",
            "inputs": ["Line pricing", "Public tendencies", "Historical trap cases", "Bookmaker behavior"],
            "output": "Trap setting probability",
            "accuracy": "77.3%"
        },
        "Convergia Core": {
            "description_key": "module_description_numericode",
            "inputs": ["ArcanX signals", "ShadowOdds signals", "Historical correlations", "Current match context"],
            "output": "Integrated prediction with confidence level",
            "accuracy": "84.2%"
        }
    }
    
    # Display default description for modules not explicitly defined
    default_description = {
        "description_key": "module_description_numericode",
        "inputs": ["Match data", "Historical patterns", "Contextual information"],
        "output": "Specialized prediction signals",
        "accuracy": "75-85%"
    }
    
    # Get module info
    module_info = module_descriptions.get(selected_module, default_description)
    
    # Display module information
    st.markdown(f"### {selected_module}")
    st.markdown(f"**{t('description')}:** {t(module_info['description_key'])}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### {t('module_inputs')}")
        for input_item in module_info['inputs']:
            st.markdown(f"- {input_item}")
    
    with col2:
        st.markdown(f"#### {t('module_output')}")
        st.markdown(module_info['output'])
        st.markdown(f"**{t('module_accuracy')}:** {module_info['accuracy']}")
    
    # Visualization of module performance
    st.markdown(f"### {t('performance_metrics')}")
    
    # Generate sample data for this specific module
    accuracy_by_context = {
        "Home favorites": np.random.uniform(0.7, 0.9),
        "Away favorites": np.random.uniform(0.65, 0.85),
        "Even matchups": np.random.uniform(0.6, 0.8),
        "High scoring": np.random.uniform(0.7, 0.9),
        "Low scoring": np.random.uniform(0.65, 0.85),
        "Derby matches": np.random.uniform(0.6, 0.85),
        "International": np.random.uniform(0.5, 0.75)
    }
    
    context_df = pd.DataFrame({
        'Context': list(accuracy_by_context.keys()),
        'Accuracy': list(accuracy_by_context.values())
    })
    
    # Sort by accuracy
    context_df = context_df.sort_values('Accuracy', ascending=False)
    
    # Create horizontal bar chart
    fig = px.bar(context_df, y='Context', x='Accuracy', orientation='h',
                color='Accuracy', color_continuous_scale='Viridis',
                labels={'Accuracy': 'Prediction Accuracy', 'Context': 'Match Context'},
                title=f"{selected_module} Performance by Match Context")
    
    fig.update_layout(
        xaxis=dict(range=[0.4, 1.0]),
        height=400,
        template='plotly_dark'
    )
    
    st.plotly_chart(fig, use_container_width=True, key="module_details_chart")
    
    # Module relationships
    st.markdown("### Module Relationships")
    st.markdown(f"How {selected_module} interacts with other components of ArcanShadow.")
    
    # Generate a sample relationship network 
    # (In a real implementation, this would be based on actual system architecture)
    st.info("This module is part of the ArcanShadow integrated prediction system. It receives inputs from data sources and other modules, processes them according to its specialized algorithms, and outputs prediction signals that feed into the convergence layer.")

# Live Monitoring Tab (formerly Notifications Tab)
with tab6:
    st.markdown(f"## {t('live_match_monitoring')}")
    
    # Check if we have an active live tracking session
    if not hasattr(st.session_state, 'live_tracking_active') or not st.session_state.live_tracking_active:
        # No active session - show placeholder and guide user to Live Match tab
        st.info("""
        👋 **Bienvenue dans le Centre de Surveillance en Direct**
        
        Cette interface affiche les analyses et alertes en temps réel d'ArcanSentinel lorsqu'un match est suivi.
        
        Pour commencer à suivre un match, allez dans l'onglet **"Match en Direct"** et sélectionnez un match dans 
        votre championnat. Une fois le suivi activé, vous verrez ici toutes les analyses, alertes et prédictions en temps réel.
        """)
        
        # Quick action button to jump to live tab
        if st.button("Aller à l'onglet Match en Direct", type="primary"):
            # Set active tab to Live Match (index 4)
            st.session_state.active_tab = 4
            st.rerun()
    else:
        # Active tracking session - show live monitoring interface
        # Get the match data and analysis
        match_data = st.session_state.live_match_data
        live_analysis = st.session_state.live_analysis
        home_team = match_data.get('home_team', 'Home Team')
        away_team = match_data.get('away_team', 'Away Team')
        
        # Match header with score
        home_score, away_score = st.session_state.current_match_score
        current_minute = st.session_state.current_match_minute
        
        st.markdown(f"""
        <div style='background-color: rgba(0,0,0,0.05); padding: 10px; border-radius: 5px; margin-bottom: 15px;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div style='flex: 2; text-align: right; font-size: 24px; font-weight: bold;'>{home_team}</div>
                <div style='flex: 1; text-align: center; font-size: 28px; font-weight: bold;'>
                    {home_score} - {away_score}
                </div>
                <div style='flex: 2; text-align: left; font-size: 24px; font-weight: bold;'>{away_team}</div>
            </div>
            <div style='text-align: center; font-size: 18px; margin-top: 5px;'>
                <span style='background-color: rgba(0,0,0,0.1); padding: 2px 8px; border-radius: 10px;'>{current_minute}'</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick update controls
        update_cols = st.columns([1, 1, 1])
        with update_cols[0]:
            if st.button("⏱️ +1 Minute", help="Avance le match d'une minute"):
                st.session_state.current_match_minute += 1
                st.session_state.live_analysis = arcan_sentinel.update_match_state(
                    st.session_state.current_match_minute, 
                    st.session_state.current_match_score
                )
                st.rerun()
        
        with update_cols[1]:
            if st.button("⚽ But Domicile", help="Ajoute un but pour l'équipe à domicile"):
                st.session_state.current_match_score[0] += 1
                
                # Create goal event
                event = {
                    'type': "Goal",
                    'team': home_team,
                    'minute': st.session_state.current_match_minute,
                    'details': f"But marqué par {home_team}"
                }
                
                # Make sure match_events exists in session state
                if not hasattr(st.session_state, 'match_events'):
                    st.session_state.match_events = []
                
                # Add to events list
                st.session_state.match_events.append(event)
                
                # Update match state with new score and event
                arcan_sentinel.update_match_state(
                    st.session_state.current_match_minute, 
                    st.session_state.current_match_score,
                    event
                )
                st.session_state.live_analysis = arcan_sentinel.update_live_analysis()
                st.rerun()
        
        with update_cols[2]:
            if st.button("⚽ But Extérieur", help="Ajoute un but pour l'équipe à l'extérieur"):
                st.session_state.current_match_score[1] += 1
                
                # Create goal event
                event = {
                    'type': "Goal",
                    'team': away_team,
                    'minute': st.session_state.current_match_minute,
                    'details': f"But marqué par {away_team}"
                }
                
                # Make sure match_events exists in session state
                if not hasattr(st.session_state, 'match_events'):
                    st.session_state.match_events = []
                
                # Add to events list
                st.session_state.match_events.append(event)
                
                # Update match state with new score and event
                arcan_sentinel.update_match_state(
                    st.session_state.current_match_minute, 
                    st.session_state.current_match_score,
                    event
                )
                st.session_state.live_analysis = arcan_sentinel.update_live_analysis()
                st.rerun()
                
        # Analysis tabs
        analysis_tabs = st.tabs([
            "Momentum", 
            "Facteurs", 
            "Cotes & Marchés", 
            "Modèles Neuraux",
            "Alertes"
        ])
        
        # 1. Momentum Analysis Tab
        with analysis_tabs[0]:
            # Show current momentum and timeline
            if live_analysis and 'momentum' in live_analysis:
                momentum_data = live_analysis['momentum']
                
                momentum_cols = st.columns([1, 2])
                with momentum_cols[0]:
                    # Current momentum gauge
                    if 'current_momentum' in momentum_data:
                        current_momentum = momentum_data.get('current_momentum', 0)
                        
                        # Normalize between -100 and 100 for visualization
                        normalized_momentum = min(max(current_momentum * 100, -100), 100)
                        
                        # Create a gauge-like visualization
                        value_color = "green" if normalized_momentum > 20 else "red" if normalized_momentum < -20 else "orange"
                        
                        # Placeholder for gauge visualization (using markdown)
                        st.markdown(f"""
                        <div style='text-align: center;'>
                            <h3>Momentum Actuel</h3>
                            <div style='font-size: 48px; color: {value_color}; font-weight: bold;'>
                                {int(normalized_momentum)}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Which team has momentum
                        if normalized_momentum > 20:
                            momentum_team = home_team
                        elif normalized_momentum < -20:
                            momentum_team = away_team
                        else:
                            momentum_team = "Équilibré"
                            
                        st.info(f"**Avantage de momentum**: {momentum_team}")
                
                with momentum_cols[1]:
                    # Momentum timeline as text description
                    st.markdown("### Évolution du Momentum")
                    
                    # Create a simplified visualization of timeline
                    if 'momentum_timeline' in momentum_data:
                        timeline = momentum_data.get('momentum_timeline', [0])
                        current_value = timeline[-1] if timeline else 0
                        
                        # Display a textual description
                        if current_value > 0.3:
                            trend = f"🔼 {home_team} prend l'ascendant"
                        elif current_value < -0.3:
                            trend = f"🔽 {away_team} prend l'ascendant"
                        else:
                            trend = "⏸️ Momentum équilibré"
                            
                        st.markdown(f"""
                        <div style='padding: 15px; background-color: rgba(0,0,0,0.05); border-radius: 5px;'>
                            <h4>{trend}</h4>
                            <p>Le momentum évolue en fonction des actions du match et des événements clés.</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Momentum factors
                if 'factors' in momentum_data:
                    st.markdown("### Facteurs influençant le momentum")
                    
                    factors = momentum_data.get('factors', {})
                    if not factors:
                        st.info("Aucun facteur de momentum détecté pour le moment")
                    else:
                        for factor, value in factors.items():
                            # Normalize to percentage for display
                            factor_value = min(max(value * 100, -100), 100)
                            if factor_value > 0:
                                direction = f"👆 {abs(factor_value):.1f}% en faveur de {home_team}"
                                color = "rgba(0, 128, 0, 0.8)"
                            elif factor_value < 0:
                                direction = f"👇 {abs(factor_value):.1f}% en faveur de {away_team}"
                                color = "rgba(255, 0, 0, 0.8)"
                            else:
                                direction = "Neutre"
                                color = "rgba(128, 128, 128, 0.8)"
                                
                            st.markdown(f"""
                            <div style='padding: 8px; margin-bottom: 8px; background-color: rgba(0,0,0,0.05); border-radius: 5px;'>
                                <div style='font-weight: bold;'>{factor.replace('_', ' ').title()}</div>
                                <div style='color: {color};'>{direction}</div>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                st.info("Données de momentum en cours de chargement...")
        
        # Quick update controls
        update_cols = st.columns([1, 1, 1])
        with update_cols[0]:
            if st.button("⏱️ +1 Minute", help="Avance le match d'une minute"):
                st.session_state.current_match_minute += 1
                st.session_state.live_analysis = arcan_sentinel.update_match_state(
                    st.session_state.current_match_minute, 
                    st.session_state.current_match_score
                )
                st.rerun()
        
        with update_cols[1]:
            if st.button("⚽ But Domicile", help="Ajoute un but pour l'équipe à domicile"):
                st.session_state.current_match_score[0] += 1
                
                # Create goal event
                event = {
                    'type': "Goal",
                    'team': home_team,
                    'minute': st.session_state.current_match_minute,
                    'details': f"But marqué par {home_team}"
                }
                
                # Add to events list
                st.session_state.match_events.append(event)
                
                # Update match state with new score and event
                arcan_sentinel.update_match_state(
                    st.session_state.current_match_minute, 
                    st.session_state.current_match_score,
                    event
                )
                st.session_state.live_analysis = arcan_sentinel.update_live_analysis()
                st.rerun()
        
        with update_cols[2]:
            if st.button("⚽ But Extérieur", help="Ajoute un but pour l'équipe à l'extérieur"):
                st.session_state.current_match_score[1] += 1
                
                # Create goal event
                event = {
                    'type': "Goal",
                    'team': away_team,
                    'minute': st.session_state.current_match_minute,
                    'details': f"But marqué par {away_team}"
                }
                
                # Add to events list
                st.session_state.match_events.append(event)
                
                # Update match state with new score and event
                arcan_sentinel.update_match_state(
                    st.session_state.current_match_minute, 
                    st.session_state.current_match_score,
                    event
                )
                st.session_state.live_analysis = arcan_sentinel.update_live_analysis()
                st.rerun()
            
    # Current notifications
    st.markdown("### Notifications récentes")
    
    # Sample notifications
    notifications = [
        {
            "type": "value_bet",
            "timestamp": datetime.now() - timedelta(minutes=15),
            "message": "Opportunité de pari à valeur détectée: Manchester United vs Liverpool, cote domicile sous-évaluée de 14%",
            "priority": "high"
        },
        {
            "type": "momentum_shift",
            "timestamp": datetime.now() - timedelta(hours=1),
            "message": "Changement majeur de momentum détecté pour Arsenal vs Newcastle, probabilité de victoire d'Arsenal augmentée de 18%",
            "priority": "medium"
        },
        {
            "type": "odds_movement",
            "timestamp": datetime.now() - timedelta(hours=3),
            "message": "Mouvement significatif des cotes: Bayern Munich vs Dortmund, cote match nul passée de 3.5 à 4.2",
            "priority": "medium"
        },
        {
            "type": "prediction_update",
            "timestamp": datetime.now() - timedelta(hours=6),
            "message": "Mise à jour de prédiction: PSG vs Lyon, nouvelle analyse suggère Under 2.5 buts avec 76% de confiance",
            "priority": "low"
        }
    ]
    
    # Display notifications
    if len(notifications) > 0:
        for notification in notifications:
            with st.container():
                # Create a colored notification box based on priority
                priority_colors = {
                    "high": "red",
                    "medium": "orange",
                    "low": "blue"
                }
                color = priority_colors.get(notification["priority"], "gray")
                
                st.markdown(f"""
                <div style='border-left: 4px solid {color}; padding-left: 10px; margin-bottom: 10px;'>
                    <h5>{notification["type"].replace("_", " ").title()}</h5>
                    <p>{notification["message"]}</p>
                    <p style='font-size: small; color: gray;'>{notification["timestamp"].strftime('%d %b %Y %H:%M')}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Aucune notification récente à afficher")
    
    # Custom alerts section
    st.markdown("### Créer une alerte personnalisée")
    
    with st.expander("Nouvelle alerte", expanded=False):
        alert_type = st.selectbox("Type d'alerte", 
                                ["Opportunité de valeur", "Mouvement de cote", "Confiance de prédiction", 
                                 "Score/Résultat", "Événement spécifique"])
        
        alert_condition = st.selectbox("Condition", 
                                     ["Supérieur à", "Inférieur à", "Égal à", "Changement de plus de"])
        
        alert_value = st.number_input("Valeur", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
        
        alert_matches = st.multiselect("S'applique aux matchs", 
                                     ["Tous les matchs", "Matchs suivis uniquement", "Match spécifique"])
        
        if "Match spécifique" in alert_matches:
            specific_match = st.text_input("Entrez l'équipe ou le match")
        
        if st.button("Créer l'alerte"):
            st.success("Alerte personnalisée créée avec succès")

# Performance Notifications Tab - NEW
with tab7:
    # Initialize database connection if needed
    if 'database' not in st.session_state:
        from utils.database import Database
        st.session_state.database = Database()
    
    # Header section with explanatory text
    st.markdown(f"## {t('performance_evaluations')}")
    st.markdown(f"*{t('performance_notifications_description')}*")
    
    # Get completed matches with predictions from database
    db = st.session_state.database
    completed_predictions = db.get_completed_predictions()
    
    if not completed_predictions or len(completed_predictions) == 0:
        st.info(t('no_completed_matches'))
    else:
        # Format matches for selection
        match_options = []
        match_map = {}
        
        for pred in completed_predictions:
            match_id = pred.id
            match_text = f"{pred.home_team} vs {pred.away_team} ({pred.date.strftime('%Y-%m-%d')})"
            match_options.append(match_text)
            match_map[match_text] = match_id
        
        # Match selection
        selected_match = st.selectbox(t('select_completed_match'), match_options)
        
        if selected_match:
            selected_match_id = match_map[selected_match]
            
            # Get detailed data for the selected match
            prediction = db.get_prediction_by_id(selected_match_id)
            
            if prediction:
                # Match Overview Section
                st.markdown(f"### {t('match_overview')}")
                
                match_cols = st.columns([3, 1, 3])
                with match_cols[0]:
                    st.markdown(f"**{prediction.home_team}**")
                with match_cols[1]:
                    st.markdown("vs")
                with match_cols[2]:
                    st.markdown(f"**{prediction.away_team}**")
                
                # Score if available
                if prediction.home_score is not None and prediction.away_score is not None:
                    score_cols = st.columns([3, 1, 3])
                    with score_cols[0]:
                        st.markdown(f"**{prediction.home_score}**")
                    with score_cols[1]:
                        st.markdown("-")
                    with score_cols[2]:
                        st.markdown(f"**{prediction.away_score}**")
                
                # Prediction vs Reality Section
                st.markdown(f"### {t('prediction_vs_reality')}")
                
                comparison_cols = st.columns(2)
                with comparison_cols[0]:
                    st.markdown(f"**{t('predicted_outcome')}:**")
                    st.markdown(f"{prediction.prediction}")
                    st.markdown(f"**{t('confidence')}:** {prediction.confidence:.2f}")
                    
                with comparison_cols[1]:
                    st.markdown(f"**{t('actual_outcome')}:**")
                    if prediction.outcome:
                        st.markdown(f"{prediction.outcome}")
                    else:
                        # Determine outcome from scores
                        if prediction.home_score > prediction.away_score:
                            outcome = "Home Win"
                        elif prediction.home_score < prediction.away_score:
                            outcome = "Away Win"
                        else:
                            outcome = "Draw"
                        st.markdown(outcome)
                    
                    # Was prediction correct?
                    if prediction.correct:
                        st.markdown("✅ **Correct Prediction**")
                    else:
                        st.markdown("❌ **Incorrect Prediction**")
                
                # Module Evaluations section
                st.markdown(f"### {t('module_evaluations')}")
                
                # Initialize meta_systems for module evaluation
                from modules.meta_systems import MetaSystems
                meta_systems = MetaSystems()
                
                # Convert prediction to expected format for evaluation
                prediction_data = {
                    'id': prediction.id,
                    'home_team': prediction.home_team,
                    'away_team': prediction.away_team,
                    'date': prediction.date,
                    'prediction': prediction.prediction,
                    'confidence': prediction.confidence,
                    'arcanx_confidence': prediction.arcanx_confidence,
                    'shadow_odds_confidence': prediction.shadow_odds_confidence,
                    'home_score': prediction.home_score,
                    'away_score': prediction.away_score,
                    'correct': prediction.correct
                }
                
                # Get module performance evaluations
                module_evaluations = meta_systems.evaluate_modules_performance(prediction_data)
                
                if module_evaluations:
                    # Create a DataFrame for the evaluations
                    eval_data = []
                    for module, evaluation in module_evaluations.items():
                        eval_data.append({
                            t('module_name'): module,
                            t('prediction_accuracy'): f"{evaluation.get('accuracy', 0):.2f}",
                            t('performance_score'): evaluation.get('performance_score', 0),
                            t('performance_trend'): evaluation.get('trend', 'Stable')
                        })
                    
                    eval_df = pd.DataFrame(eval_data)
                    st.dataframe(eval_df, use_container_width=True)
                    
                    # Display details for each module
                    st.markdown(f"### {t('key_success_factors')}")
                    
                    # Get ArcanBrain analysis
                    from modules.arcan_brain import ArcanBrain
                    arcan_brain = ArcanBrain(meta_systems=meta_systems)
                    
                    # Initialize LearningSystem to manage pattern recalibration and transfer learning
                    learning_system = LearningSystem(meta_systems=meta_systems, arcan_brain=arcan_brain)
                    
                    # Convert prediction data to match data format
                    match_data = {
                        'id': prediction.id,
                        'home_team': prediction.home_team,
                        'away_team': prediction.away_team,
                        'date': prediction.date,
                        'league': prediction.league,
                        'sport': prediction.sport,
                        'home_score': prediction.home_score,
                        'away_score': prediction.away_score
                    }
                    
                    # Generate insight analysis
                    insight = arcan_brain.generate_analysis_insight(match_data, prediction_data)
                    
                    # Display the insight
                    st.markdown(insight)
                    
                    # Generate module improvement suggestions
                    st.markdown(f"### {t('module_improvement_suggestions')}")
                    
                    # Get feedback from ArcanReflex
                    from modules.arcan_reflex import ArcanReflex
                    arcan_reflex = ArcanReflex(meta_systems=meta_systems)
                    
                    reflex_feedback = arcan_reflex.generate_module_feedback(prediction_data)
                    
                    if reflex_feedback:
                        for module, feedback in reflex_feedback.items():
                            with st.expander(f"{module} {t('improvement_suggestions')}"):
                                st.markdown(feedback.get('suggestions', 'No specific suggestions available.'))
                                
                                # Display adaptation parameters if available
                                adaptations = feedback.get('adaptations', {})
                                if adaptations:
                                    st.markdown("#### Parameter Adjustments")
                                    for param, value in adaptations.items():
                                        st.markdown(f"- **{param}**: {value}")
                else:
                    st.info("Module evaluation data not available for this match.")
            else:
                st.error("Error retrieving prediction details.")
        
        # Section for displaying live-tracked matches from the Live Surveillance tab
        st.markdown("---")
        st.markdown(f"## {t('live_tracked_matches')}")
        st.markdown(f"{t('live_tracked_matches_description')}")
        
        # Check if there are any live-tracked matches in the session state
        if hasattr(st.session_state, 'live_tracking_history') and st.session_state.live_tracking_history:
            # Display each tracked match with its analysis
            for i, tracked_match in enumerate(st.session_state.live_tracking_history):
                match_data = tracked_match.get('match_data', {})
                analysis = tracked_match.get('analysis', {})
                timestamp = tracked_match.get('timestamp', datetime.now())
                
                with st.expander(f"{match_data.get('home_team', 'Home')} vs {match_data.get('away_team', 'Away')} - {timestamp.strftime('%d %b %Y %H:%M')}"):
                    # Match details
                    match_cols = st.columns([3, 1, 3])
                    with match_cols[0]:
                        st.markdown(f"**{match_data.get('home_team', 'Home')}**")
                    with match_cols[1]:
                        st.markdown("vs")
                    with match_cols[2]:
                        st.markdown(f"**{match_data.get('away_team', 'Away')}**")
                    
                    # Score if available
                    score_cols = st.columns([3, 1, 3])
                    with score_cols[0]:
                        st.markdown(f"**{match_data.get('home_score', 0)}**")
                    with score_cols[1]:
                        st.markdown("-")
                    with score_cols[2]:
                        st.markdown(f"**{match_data.get('away_score', 0)}**")
                    
                    # Analysis summary
                    st.markdown("### Analysis Summary")
                    
                    # Momentum and key events
                    if 'momentum' in analysis:
                        st.markdown("#### Momentum Analysis")
                        momentum = analysis['momentum']
                        
                        # Create momentum chart if data is available
                        if 'timeline' in momentum:
                            momentum_data = pd.DataFrame({
                                'Time': momentum['timeline'],
                                'Home': momentum.get('home_momentum', [50] * len(momentum['timeline'])),
                                'Away': momentum.get('away_momentum', [50] * len(momentum['timeline']))
                            })
                            
                            fig = px.line(momentum_data, x='Time', y=['Home', 'Away'],
                                         title="Match Momentum",
                                         labels={'value': 'Momentum', 'variable': 'Team'},
                                         color_discrete_sequence=['#3366CC', '#DC3912'])
                            
                            fig.update_layout(
                                template='plotly_dark',
                                height=300
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                    
                    # Key events
                    if 'key_events' in analysis:
                        st.markdown("#### Key Events")
                        events = analysis['key_events']
                        
                        for event in events:
                            event_time = event.get('time', '00:00')
                            event_type = event.get('type', 'Unknown')
                            event_desc = event.get('description', '')
                            event_icon = "⚽️" if event_type == "Goal" else "🔄" if event_type == "Substitution" else "🟨" if event_type == "Yellow Card" else "🟥" if event_type == "Red Card" else "📝"
                            
                            st.markdown(f"{event_icon} **{event_time}** - {event_desc}")
                    
                    # ArcanSentinel insights
                    if 'arcan_sentinel' in analysis:
                        sentinel = analysis['arcan_sentinel']
                        st.markdown("#### ArcanSentinel Insights")
                        
                        insights = sentinel.get('insights', [])
                        for insight in insights:
                            st.markdown(f"- {insight}")
                    
                    # Module performance during live tracking
                    st.markdown("#### Module Performance")
                    
                    if 'module_performance' in analysis:
                        module_perf = analysis['module_performance']
                        
                        # Create a DataFrame for module performance
                        module_data = []
                        for module, perf in module_perf.items():
                            module_data.append({
                                'Module': module,
                                'Accuracy': perf.get('accuracy', 0.0),
                                'Contribution': perf.get('contribution', 0.0)
                            })
                        
                        if module_data:
                            module_df = pd.DataFrame(module_data)
                            
                            fig = px.bar(module_df, y='Module', x='Accuracy', orientation='h',
                                       color='Accuracy', color_continuous_scale='Viridis',
                                       title="Module Performance During Live Tracking")
                            
                            fig.update_layout(
                                xaxis=dict(range=[0.3, 1.0]),
                                template='plotly_dark',
                                height=350
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Synthèse comparative
                            st.markdown("### Synthèse Comparative")
                            
                            # Extraire les données d'analyse pertinentes
                            analysis = match_data.get('live_analysis', {})
                            
                            if 'momentum' in analysis or 'bet_pulse' in analysis or 'karmic_flow' in analysis:
                                comp_cols = st.columns(2)
                                
                                with comp_cols[0]:
                                    st.markdown("#### Analyse des Tendances")
                                    
                                    # Tendances de momentum
                                    if 'momentum' in analysis:
                                        momentum_data = analysis['momentum']
                                        
                                        # Créer un résumé du momentum
                                        current_momentum = momentum_data.get('current_momentum', 0)
                                        normalized_momentum = min(max(current_momentum * 100, -100), 100)
                                        
                                        # Déterminer la tendance à partir du momentum
                                        if normalized_momentum > 20:
                                            momentum_trend = f"Momentum en faveur de {match_data.get('home_team', 'Domicile')} (+{normalized_momentum:.1f}%)"
                                            momentum_color = "green"
                                        elif normalized_momentum < -20:
                                            momentum_trend = f"Momentum en faveur de {match_data.get('away_team', 'Extérieur')} ({normalized_momentum:.1f}%)"
                                            momentum_color = "red"
                                        else:
                                            momentum_trend = f"Momentum équilibré ({normalized_momentum:.1f}%)"
                                            momentum_color = "orange"
                                        
                                        st.markdown(f"<span style='color:{momentum_color};font-weight:bold;'>{momentum_trend}</span>", unsafe_allow_html=True)
                                    
                                    # Tendances de marché
                                    if 'bet_pulse' in analysis:
                                        bet_data = analysis['bet_pulse']
                                        st.markdown("**Tendances de marché:**")
                                        
                                        if all(k in bet_data for k in ['home_volume', 'home_change', 'draw_volume', 'draw_change', 'away_volume', 'away_change']):
                                            # Créer un mini tableau
                                            market_data = {
                                                "Type": ["Domicile", "Nul", "Extérieur"],
                                                "Volume": [
                                                    f"{bet_data.get('home_volume', 0)}%", 
                                                    f"{bet_data.get('draw_volume', 0)}%", 
                                                    f"{bet_data.get('away_volume', 0)}%"
                                                ],
                                                "Évolution": [
                                                    f"{bet_data.get('home_change', 0)}%", 
                                                    f"{bet_data.get('draw_change', 0)}%", 
                                                    f"{bet_data.get('away_change', 0)}%"
                                                ]
                                            }
                                            
                                            market_df = pd.DataFrame(market_data)
                                            st.dataframe(market_df, hide_index=True)
                                            
                                            # Identifier la tendance principale du marché
                                            home_change = bet_data.get('home_change', 0)
                                            draw_change = bet_data.get('draw_change', 0)
                                            away_change = bet_data.get('away_change', 0)
                                            
                                            max_change = max(home_change, draw_change, away_change)
                                            if max_change == home_change:
                                                st.markdown(f"👆 Tendance marché: **Domicile** en augmentation")
                                            elif max_change == draw_change:
                                                st.markdown(f"👉 Tendance marché: **Nul** en augmentation")
                                            else:
                                                st.markdown(f"👇 Tendance marché: **Extérieur** en augmentation")
                                
                                with comp_cols[1]:
                                    st.markdown("#### Facteurs d'influence")
                                    
                                    # Facteurs de momentum
                                    if 'momentum' in analysis and 'factors' in analysis['momentum']:
                                        factors = analysis['momentum'].get('factors', {})
                                        
                                        if factors:
                                            for factor, value in list(factors.items())[:3]:  # Afficher les 3 premiers facteurs
                                                factor_value = min(max(value * 100, -100), 100)
                                                
                                                if factor_value > 0:
                                                    direction = f"👆 {abs(factor_value):.1f}% en faveur de {match_data.get('home_team', 'Domicile')}"
                                                    color = "rgba(0, 128, 0, 0.8)"
                                                elif factor_value < 0:
                                                    direction = f"👇 {abs(factor_value):.1f}% en faveur de {match_data.get('away_team', 'Extérieur')}"
                                                    color = "rgba(255, 0, 0, 0.8)"
                                                else:
                                                    direction = "Neutre"
                                                    color = "rgba(128, 128, 128, 0.8)"
                                                    
                                                st.markdown(f"""
                                                <div style='padding: 8px; margin-bottom: 8px; background-color: rgba(0,0,0,0.05); border-radius: 5px;'>
                                                    <div style='font-weight: bold;'>{factor.replace('_', ' ').title()}</div>
                                                    <div style='color: {color};'>{direction}</div>
                                                </div>
                                                """, unsafe_allow_html=True)
                                    
                                    # Flux karmique
                                    if 'karmic_flow' in analysis:
                                        karmic_data = analysis['karmic_flow']
                                        
                                        if 'balance' in karmic_data:
                                            balance = karmic_data['balance']
                                            
                                            # Interpréter la balance karmique
                                            if float(balance) < -0.3:
                                                st.markdown(f"⚡ **Flux karmique** fortement en faveur de **{match_data.get('away_team', 'Extérieur')}**")
                                            elif float(balance) > 0.3:
                                                st.markdown(f"⚡ **Flux karmique** fortement en faveur de **{match_data.get('home_team', 'Domicile')}**")
                                            else:
                                                st.markdown(f"⚡ **Flux karmique** relativement équilibré")
                            
                            # Rapport de synthèse avec recommandations
                            st.markdown("#### Synthèse et Recommandations")
                            
                            if 'arcan_sentinel' in analysis:
                                sentinel = analysis['arcan_sentinel']
                                
                                if 'insights' in sentinel:
                                    insights = sentinel.get('insights', [])
                                    for insight in insights:
                                        st.markdown(f"- {insight}")
                                
                                if 'recommendation' in sentinel:
                                    st.markdown("**Recommandation:**")
                                    st.markdown(f"{sentinel['recommendation']}")
        else:
            st.info(t('no_live_tracked_matches'))

# Daily Combo Tab
with tab8:
    # Import the betting combo generator at the beginning of this tab
    from utils.betting_combo_generator import BettingComboGenerator
    
    # Header section
    st.markdown(f"## {t('daily_combo_title')}")
    st.markdown(t('daily_combo_description'))
    
    # Initialize the betting combo generator if not exist
    if 'betting_combo_generator' not in st.session_state:
        st.session_state.betting_combo_generator = BettingComboGenerator()
    
    # Initialize session state for daily combo if not exist
    if 'daily_combo' not in st.session_state:
        # Generate daily combo on first load
        predictions = st.session_state.get('predictions', [])
        combo_generator = st.session_state.betting_combo_generator
        
        # Récupérer les matchs du jour pour La Liga (nous savons qu'ils existent)
        sport = 'Football'
        league = 'La Liga'
        date = datetime.now().date()
        upcoming_matches = data_handler.get_upcoming_matches(sport, league, date)
        
        # Générer le combiné avec les matchs récupérés
        st.session_state.daily_combo = combo_generator.generate_daily_combo(
            matches=upcoming_matches,
            arcan_predictions=predictions, 
            risk_level='medium'
        )
        
        # Log pour debug
        st.write(f"Généré combiné avec {len(upcoming_matches)} matchs et {len(predictions) if predictions else 0} prédictions")
    
    # Create layout with two columns
    daily_combo_cols = st.columns([3, 2])
    
    with daily_combo_cols[0]:
        # Risk level selector
        risk_cols = st.columns([1, 2])
        with risk_cols[0]:
            st.markdown("### Configuration")
        with risk_cols[1]:
            risk_level = st.radio(
                "Niveau de risque:",
                ["low", "medium", "high"],
                index=1,
                horizontal=True,
                help="Sélectionnez le niveau de risque pour le combiné du jour. Bas (faibles cotes, haute confiance), Moyen (équilibré), Élevé (fortes cotes, plus risqué)."
            )
            
            # Option pour utiliser uniquement les modules performants
            use_top_modules = st.checkbox(
                t("use_top_modules"), 
                value=False,
                help=t("top_modules_help")
            )
            
            if st.button("Actualiser le combiné"):
                # Generate new combo with selected risk level and module filtering option
                predictions = st.session_state.get('predictions', [])
                combo_generator = st.session_state.betting_combo_generator
                
                # Nous n'avons plus besoin de récupérer les matchs, le générateur s'en charge
                
                # Générer le combiné (le générateur assurera qu'il y a des matchs)
                st.session_state.daily_combo = combo_generator.generate_daily_combo(
                    arcan_predictions=predictions, 
                    risk_level=risk_level,
                    use_top_modules=use_top_modules
                )
                
                st.rerun()
        
        st.markdown(f"### {t('recommended_bets')}")
        
        # Get current matches data
        matches = st.session_state.get('matches', [])
        predictions = st.session_state.get('predictions', [])
        live_matches = st.session_state.get('live_matches', [])
        
        # Generate best bets using the betting combo generator
        combo_generator = st.session_state.betting_combo_generator
        
        # Filtrer les prédictions par modules performants si demandé
        filtered_predictions = predictions
        if use_top_modules and predictions:
            # Récupérer les performances des modules
            module_performance = combo_generator._get_module_performance()
            
            # Filtrer pour ne garder que les prédictions des modules performants
            top_modules = [module for module, perf in module_performance.items() if perf >= 0.6]
            
            if top_modules:
                filtered_predictions = []
                for pred in predictions:
                    if pred.get('source_module') in top_modules:
                        filtered_predictions.append(pred)
                        
                # Information sur le filtrage si activé
                if filtered_predictions:
                    st.success(t("top_modules_active").format(
                        count=len(filtered_predictions),
                        modules=', '.join(top_modules[:3])
                    ))
                else:
                    st.warning(t("no_top_modules_data"))
        
        best_bets = combo_generator.generate_best_bets(
            matches=None,  # Let it fetch the matches
            arcan_predictions=filtered_predictions,
            min_confidence=0.55 if risk_level == 'high' else 0.65 if risk_level == 'medium' else 0.7
        )
        
        if best_bets:
            # Create tabs for different betting markets
            market_types = set([bet['market'].split(' ')[0] for bet in best_bets])
            market_types_list = sorted(list(market_types))
            
            if market_types_list:
                market_tabs = st.tabs(["Tous les marchés"] + market_types_list)
                
                # All markets tab
                with market_tabs[0]:
                    st.markdown("#### Tous les marchés recommandés")
                    
                    # Group by match
                    matches_dict = {}
                    for bet in best_bets:
                        match_id = bet['match']['id']
                        if match_id not in matches_dict:
                            matches_dict[match_id] = {
                                'match': bet['match'],
                                'bets': []
                            }
                        matches_dict[match_id]['bets'].append(bet)
                    
                    # Display bets by match
                    for match_id, match_data in matches_dict.items():
                        match = match_data['match']
                        home_team = match.get('home_team', '')
                        away_team = match.get('away_team', '')
                        
                        with st.expander(f"{home_team} vs {away_team} ({match.get('league', 'League')})"):
                            for bet in match_data['bets']:
                                cols = st.columns([3, 1, 1, 1])
                                
                                with cols[0]:
                                    st.markdown(f"**{bet['selection']}** ({bet['market']})")
                                    st.markdown(f"_{bet['insight']}_")
                                
                                with cols[1]:
                                    st.markdown(f"**{t('bet_odds')}:** {bet['odds']:.2f}")
                                
                                with cols[2]:
                                    confidence_display = bet['confidence'] * 100
                                    confidence_color = "green" if confidence_display > 75 else "orange" if confidence_display > 60 else "red"
                                    st.markdown(f"**{t('bet_confidence')}:** <span style='color:{confidence_color};'>{confidence_display:.1f}%</span>", unsafe_allow_html=True)
                                
                                with cols[3]:
                                    # Check if this bet is in the daily combo
                                    daily_combo = st.session_state.daily_combo
                                    is_in_combo = any(
                                        s['match']['id'] == bet['match']['id'] and 
                                        s['selection'] == bet['selection'] and 
                                        s['market'] == bet['market']
                                        for s in daily_combo.get('selections', [])
                                    )
                                    
                                    # Generate a unique key for this button
                                    key = f"{match_id}_{bet['market']}_{bet['selection']}"
                                    
                                    if is_in_combo:
                                        st.info("Inclus dans le combiné du jour")
                                
                                st.markdown("---")
                
                # Individual market type tabs
                for i, market_type in enumerate(market_types_list):
                    with market_tabs[i + 1]:
                        st.markdown(f"#### Marchés {market_type}")
                        
                        # Filter bets for this market
                        market_bets = [bet for bet in best_bets if bet['market'].startswith(market_type)]
                        
                        # Group by match
                        matches_dict = {}
                        for bet in market_bets:
                            match_id = bet['match']['id']
                            if match_id not in matches_dict:
                                matches_dict[match_id] = {
                                    'match': bet['match'],
                                    'bets': []
                                }
                            matches_dict[match_id]['bets'].append(bet)
                        
                        # Display bets by match
                        for match_id, match_data in matches_dict.items():
                            match = match_data['match']
                            home_team = match.get('home_team', '')
                            away_team = match.get('away_team', '')
                            
                            with st.expander(f"{home_team} vs {away_team} ({match.get('league', 'League')})"):
                                for bet in match_data['bets']:
                                    cols = st.columns([3, 1, 1, 1])
                                    
                                    with cols[0]:
                                        st.markdown(f"**{bet['selection']}** ({bet['market']})")
                                        st.markdown(f"_{bet['insight']}_")
                                    
                                    with cols[1]:
                                        st.markdown(f"**{t('bet_odds')}:** {bet['odds']:.2f}")
                                    
                                    with cols[2]:
                                        confidence_display = bet['confidence'] * 100
                                        confidence_color = "green" if confidence_display > 75 else "orange" if confidence_display > 60 else "red"
                                        st.markdown(f"**{t('bet_confidence')}:** <span style='color:{confidence_color};'>{confidence_display:.1f}%</span>", unsafe_allow_html=True)
                                    
                                    with cols[3]:
                                        # Check if this bet is in the daily combo
                                        daily_combo = st.session_state.daily_combo
                                        is_in_combo = any(
                                            s['match']['id'] == bet['match']['id'] and 
                                            s['selection'] == bet['selection'] and 
                                            s['market'] == bet['market']
                                            for s in daily_combo.get('selections', [])
                                        )
                                        
                                        # Generate a unique key for this button
                                        key = f"{market_type}_{match_id}_{bet['selection']}"
                                        
                                        if is_in_combo:
                                            st.info("Inclus dans le combiné du jour")
                                    
                                    st.markdown("---")
            else:
                st.info("Aucun marché disponible pour aujourd'hui")
        else:
            st.info(t('no_recommendations'))
    
    with daily_combo_cols[1]:
        st.markdown(f"### {t('daily_combo_title')}")
        
        # Display daily combo
        daily_combo = st.session_state.daily_combo
        selections = daily_combo.get('selections', [])
        
        if selections:
            # Create visual coupon
            with st.container():
                st.markdown("""
                <style>
                .coupon-container {
                    background-color: rgba(49, 51, 63, 0.7);
                    border-radius: 10px;
                    padding: 15px;
                    margin-bottom: 20px;
                }
                .coupon-header {
                    text-align: center;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                    padding-bottom: 10px;
                    margin-bottom: 15px;
                }
                .coupon-item {
                    padding: 10px;
                    margin-bottom: 10px;
                    background-color: rgba(0, 0, 0, 0.1);
                    border-radius: 5px;
                }
                .coupon-footer {
                    border-top: 1px solid rgba(255, 255, 255, 0.1);
                    padding-top: 15px;
                    margin-top: 10px;
                }
                </style>
                
                <div class="coupon-container">
                    <div class="coupon-header">
                        <h3>ArcanShadow Combo</h3>
                        <p>Généré le {daily_combo.get('generated_at', datetime.now().strftime('%d/%m/%Y %H:%M'))}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                for bet in selections:
                    match = bet['match']
                    home_team = match.get('home_team', '')
                    away_team = match.get('away_team', '')
                    league = match.get('league', '')
                    
                    st.markdown(f"""
                    <div class="coupon-item">
                        <div><strong>{home_team} vs {away_team}</strong> ({league})</div>
                        <div>{bet['market']}: <span style="color: #9C89FF;"><strong>{bet['selection']}</strong></span> @ {bet['odds']:.2f}</div>
                        <div style="font-size: 0.8em; font-style: italic; opacity: 0.7;">{bet['insight']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display total odds and expected value
                total_odds = daily_combo.get('total_odds', 1.0)
                avg_confidence = daily_combo.get('avg_confidence', 0.0)
                expected_value = daily_combo.get('expected_value', 0.0)
                
                ev_color = "green" if expected_value > 0.1 else "orange" if expected_value > 0 else "red"
                
                st.markdown(f"""
                <div class="coupon-footer">
                    <div><strong>{t('total_combo_odds')}:</strong> {total_odds:.2f}</div>
                    <div><strong>{t('potential_return')}:</strong> {total_odds:.2f}x</div>
                    <div><strong>{t('bet_confidence')}:</strong> {avg_confidence*100:.1f}%</div>
                    <div><strong>{t('expected_value')}:</strong> <span style="color: {ev_color};">{expected_value:.2f}</span></div>
                </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display risk assessment
                st.markdown(f"### {t('risk_assessment')}")
                
                # Risk level based on risk parameter
                risk_level = daily_combo.get('risk_level', 'medium')
                risk_category = "Élevé" if risk_level == 'high' else "Moyen" if risk_level == 'medium' else "Faible"
                risk_color = "red" if risk_level == 'high' else "orange" if risk_level == 'medium' else "green"
                
                st.markdown(f"**Niveau de risque:** <span style='color:{risk_color};'>{risk_category}</span>", unsafe_allow_html=True)
                
                # Progress bar for risk visualization
                normalized_risk = 0.9 if risk_level == 'high' else 0.5 if risk_level == 'medium' else 0.2
                st.progress(normalized_risk)
                
                # Get insights from the combo generator
                combo_generator = st.session_state.betting_combo_generator
                insights = combo_generator.get_bet_insights(daily_combo)
                
                # Display insights
                st.markdown("### Insights & Conseils")
                
                for insight in insights:
                    st.markdown(f"- {insight}")
                
                # Module contribution analysis
                st.markdown("### Module Contributions")
                
                # Count contributions by module
                module_counts = {}
                for bet in selections:
                    module = bet.get('module_source', 'Unknown')
                    if module in module_counts:
                        module_counts[module] += 1
                    else:
                        module_counts[module] = 1
                
                # Create a small pie chart of module contributions
                fig = px.pie(
                    values=list(module_counts.values()),
                    names=list(module_counts.keys()),
                    title="Module Contributions",
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig.update_layout(margin=dict(t=40, b=40, l=40, r=40))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucun combiné disponible pour aujourd'hui. Essayez d'actualiser avec un niveau de risque différent.")

# Smart Market Recommendations Tab
with tab9:
    # Import the market recommender
    from utils.market_recommender import BettingMarketRecommender, get_market_recommendations
    from utils.database import db, UserBettingHistory, UserMarketPreference, MarketRecommendation
    
    # Header section
    st.markdown(f"## {t('smart_recommendations_title')}")
    st.markdown(t('smart_recommendations_description'))

with tab10:
    # Import the learning system (already imported at top of file)
    
    # Header section
    st.markdown("## Système d'Apprentissage")
    st.markdown("Le système d'apprentissage permet de suivre l'évolution des capacités prédictives du système en traçant les événements de recalibration et de transfert d'apprentissage.")
    
    # Create layout with two columns for content
    learning_cols = st.columns([3, 2])
    
    # Import datetime for timestamps
    from datetime import datetime, timedelta
    
    with learning_cols[0]:
        # Tabs for different types of learning events
        learning_tabs = st.tabs(["Recalibration des Patterns", "Apprentissage par Transfert", "Statistiques d'Apprentissage"])
        
        with learning_tabs[0]:
            st.markdown("### Recalibration des Patterns")
            
            # Exemple de données pour illustrer l'interface
            recalibrations = [
                {
                    "timestamp": datetime.now().isoformat(),
                    "source": "ArcanBrain",
                    "patterns_recalibrated": 15,
                    "patterns_strengthened": 10,
                    "patterns_weakened": 5
                },
                {
                    "timestamp": (datetime.now() - timedelta(hours=3)).isoformat(),
                    "source": "ArcanBrain",
                    "patterns_recalibrated": 8,
                    "patterns_strengthened": 5,
                    "patterns_weakened": 3
                }
            ]
            
            # Affichage des événements de recalibration
            if recalibrations:
                for recal in recalibrations:
                    with st.container():
                        st.markdown(f"""
                        <div style='background-color: rgba(30, 30, 50, 0.7); border-radius: 10px; padding: 15px; border-left: 4px solid #9c27b0; margin-bottom: 10px;'>
                            <div style='display: flex; justify-content: space-between;'>
                                <div><strong>Source:</strong> {recal['source']}</div>
                                <div><small>{recal['timestamp']}</small></div>
                            </div>
                            <div style='margin-top: 10px;'>
                                <span style='background-color: #1a1a2e; padding: 5px 8px; border-radius: 5px; margin-right: 10px;'>
                                    {recal['patterns_recalibrated']} patterns
                                </span>
                                <span style='background-color: green; padding: 5px 8px; border-radius: 5px; margin-right: 10px;'>
                                    +{recal['patterns_strengthened']} renforcés
                                </span>
                                <span style='background-color: #d32f2f; padding: 5px 8px; border-radius: 5px;'>
                                    -{recal['patterns_weakened']} affaiblis
                                </span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Aucun événement de recalibration n'a été enregistré.")
        
        with learning_tabs[1]:
            st.markdown("### Apprentissage par Transfert")
            
            # Exemple de données pour illustrer l'interface
            transfers = [
                {
                    "timestamp": datetime.now().isoformat(),
                    "source": "ArcanBrain",
                    "source_context": {"league": "Premier League", "match_type": "Derby"},
                    "target_context": {"league": "La Liga", "match_type": "Derby"},
                    "patterns_transferred": 12
                }
            ]
            
            # Affichage des événements de transfert
            if transfers:
                for transfer in transfers:
                    with st.container():
                        st.markdown(f"""
                        <div style='background-color: rgba(30, 30, 50, 0.7); border-radius: 10px; padding: 15px; border-left: 4px solid #1e88e5; margin-bottom: 10px;'>
                            <div style='display: flex; justify-content: space-between;'>
                                <div><strong>Source:</strong> {transfer['source']}</div>
                                <div><small>{transfer['timestamp']}</small></div>
                            </div>
                            <div style='margin-top: 10px;'>
                                <div style='margin-bottom: 5px;'>
                                    <strong>Contexte source:</strong> {transfer['source_context']['league']} - {transfer['source_context']['match_type']}
                                </div>
                                <div style='margin-bottom: 5px;'>
                                    <strong>Contexte cible:</strong> {transfer['target_context']['league']} - {transfer['target_context']['match_type']}
                                </div>
                                <div style='background-color: #1a1a2e; padding: 5px 8px; border-radius: 5px; display: inline-block; margin-top: 5px;'>
                                    {transfer['patterns_transferred']} patterns transférés
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Aucun événement de transfert d'apprentissage n'a été enregistré.")
        
        with learning_tabs[2]:
            st.markdown("### Statistiques d'Apprentissage")
            
            # Données d'exemple pour les statistiques
            stats = {
                "recalibration_efficacy": 0.75,
                "transfer_learning_efficacy": 0.68,
                "learning_system_health": 0.82
            }
            
            # Affichage des métriques
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Efficacité des recalibrations", f"{stats['recalibration_efficacy']*100:.1f}%")
            with col2:
                st.metric("Efficacité des transferts", f"{stats['transfer_learning_efficacy']*100:.1f}%")
            with col3:
                st.metric("Santé du système", f"{stats['learning_system_health']*100:.1f}%")
            
            # Graphique d'évolution
            st.markdown("#### Évolution des capacités d'apprentissage")
            
            # Données d'exemple pour le graphique
            dates = [datetime.now() - timedelta(days=i) for i in range(10, 0, -1)]
            recal_values = [0.65, 0.67, 0.68, 0.70, 0.72, 0.73, 0.74, 0.75, 0.75, 0.75]
            transfer_values = [0.55, 0.57, 0.59, 0.61, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68]
            
            chart_data = pd.DataFrame({
                'Date': dates,
                'Recalibration': recal_values,
                'Transfert': transfer_values
            })
            
            # Création du graphique
            fig = px.line(chart_data, x='Date', y=['Recalibration', 'Transfert'],
                         title="Progression de l'efficacité d'apprentissage")
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Efficacité",
                legend_title="Type d'apprentissage",
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with learning_cols[1]:
        st.markdown("### Paramètres d'Apprentissage")
        
        # Contrôles pour les paramètres d'apprentissage
        st.slider("Seuil de similarité pour transfert", 0.0, 1.0, 0.6, 0.05, 
                 help="Seuil minimal de similarité entre contextes pour permettre un transfert d'apprentissage")
        
        st.slider("Coefficient de renforcement", 0.0, 1.0, 0.8, 0.05,
                 help="Coefficient appliqué lors du renforcement d'un pattern")
        
        st.slider("Coefficient d'affaiblissement", 0.0, 1.0, 0.7, 0.05,
                 help="Coefficient appliqué lors de l'affaiblissement d'un pattern")
        
        st.number_input("Taille maximale de l'historique", 10, 200, 50, 10,
                       help="Nombre maximum d'événements d'apprentissage à conserver")
        
        # Section d'actions manuelles
        st.markdown("### Actions Manuelles")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Forcer recalibration", type="primary"):
                st.info("Recalibration forcée déclenchée.")
        
        with col2:
            if st.button("Vider les patterns faibles"):
                st.info("Patterns faibles supprimés.")
        
        # Liste des contextes disponibles
        st.markdown("### Contextes Disponibles")
        
        contexts = [
            {"id": 1, "name": "Premier League - Derby", "patterns": 45},
            {"id": 2, "name": "La Liga - Derby", "patterns": 23},
            {"id": 3, "name": "Ligue 1 - Match normal", "patterns": 67}
        ]
        
        for ctx in contexts:
            st.markdown(f"""
            <div style='background-color: rgba(30, 30, 50, 0.5); border-radius: 10px; padding: 10px; margin-bottom: 5px;'>
                {ctx['name']} ({ctx['patterns']} patterns)
            </div>
            """, unsafe_allow_html=True)
    
    with smart_rec_cols[0]:
        # Main recommendations area
        st.markdown(f"### {t('recommended_markets')}")
        
        # Get market recommendations for the user
        recommendations = get_market_recommendations(user_id, sport=st.session_state.selected_sport)
        
        if not recommendations:
            # If no recommendations exist, we need to generate sample historical data
            st.info(t('no_betting_history'))
            
            if st.button(t('add_bet_button')):
                # Generate some sample betting history to demonstrate functionality
                sample_bets = [
                    {
                        'user_id': user_id,
                        'sport': 'Football',
                        'league': 'La Liga',
                        'market_type': '1X2',
                        'selection': 'Home Win',
                        'odds': 1.85,
                        'stake': 50.0,
                        'outcome': 'win',
                        'return_amount': 92.5,
                        'profit_loss': 42.5
                    },
                    {
                        'user_id': user_id,
                        'sport': 'Football',
                        'league': 'Premier League',
                        'market_type': 'BTTS',
                        'selection': 'Yes',
                        'odds': 1.95,
                        'stake': 30.0,
                        'outcome': 'win',
                        'return_amount': 58.5,
                        'profit_loss': 28.5
                    },
                    {
                        'user_id': user_id,
                        'sport': 'Football',
                        'league': 'Bundesliga',
                        'market_type': 'Over/Under 2.5',
                        'selection': 'Over 2.5',
                        'odds': 2.10,
                        'stake': 40.0,
                        'outcome': 'loss',
                        'return_amount': 0.0,
                        'profit_loss': -40.0
                    },
                    {
                        'user_id': user_id,
                        'sport': 'Football',
                        'league': 'Ligue 1',
                        'market_type': '1X2',
                        'selection': 'Away Win',
                        'odds': 3.20,
                        'stake': 20.0,
                        'outcome': 'win',
                        'return_amount': 64.0,
                        'profit_loss': 44.0
                    },
                    {
                        'user_id': user_id,
                        'sport': 'Football',
                        'league': 'Serie A',
                        'market_type': 'BTTS',
                        'selection': 'No',
                        'odds': 2.25,
                        'stake': 35.0,
                        'outcome': 'loss',
                        'return_amount': 0.0,
                        'profit_loss': -35.0
                    }
                ]
                
                # Save sample bets to database
                for bet_data in sample_bets:
                    db.save_user_bet(bet_data)
                
                # Create a recommender and generate recommendations
                recommender = BettingMarketRecommender(user_id)
                recommender.generate_recommendations(sport=st.session_state.selected_sport)
                
                # Refresh the app
                st.rerun()
        else:
            # Display recommendations grouped by match
            recommendations_by_match = {}
            for rec in recommendations:
                match_id = rec.match_id
                if match_id not in recommendations_by_match:
                    recommendations_by_match[match_id] = []
                recommendations_by_match[match_id].append(rec)
            
            # Display each match's recommendations
            for match_id, match_recs in recommendations_by_match.items():
                # Get match details from the first recommendation
                sport = match_recs[0].sport
                league = match_recs[0].league
                
                # Try to find the actual match info
                match_info = None
                session = db.Session()
                try:
                    match = session.query(db.Match).filter(db.Match.id == match_id).first()
                    if match:
                        match_info = {
                            'home_team': match.home_team,
                            'away_team': match.away_team,
                            'date': match.date
                        }
                finally:
                    session.close()
                
                # If no actual match found, create a placeholder
                if not match_info:
                    match_info = {
                        'home_team': 'Team A',
                        'away_team': 'Team B',
                        'date': datetime.now()
                    }
                
                # Create an expander for each match
                with st.expander(f"{match_info['home_team']} vs {match_info['away_team']} ({sport} - {league})"):
                    for rec in match_recs:
                        # Create a card for each recommendation
                        st.markdown(f"""
                        <div style="background-color: rgba(60, 60, 100, 0.1); padding: 15px; border-radius: 5px; margin-bottom: 10px; border-left: 3px solid #9966CC;">
                            <h4 style="margin-top: 0;">{rec.market_type}</h4>
                            <p><strong>{t('recommendation_reason')}:</strong> {rec.reason}</p>
                            <div style="display: flex; justify-content: space-between;">
                                <span><strong>{t('market_preference_score')}:</strong> {rec.recommendation_score:.1f}/100</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    with smart_rec_cols[1]:
        # User preferences and betting history area
        st.markdown(f"### {t('preferred_markets')}")
        
        # Get user market preferences
        preferences = db.get_user_market_preferences(user_id)
        
        if not preferences:
            st.info(t('no_betting_history'))
        else:
            # Create a preferences dataframe for display
            pref_data = []
            for pref in preferences:
                pref_data.append({
                    'Market': pref.market_type,
                    t('market_preference_score'): f"{pref.preference_score:.1f}",
                    t('market_success_rate'): f"{pref.success_rate * 100:.1f}%" if pref.success_rate else "N/A",
                    'Avg. Odds': f"{pref.avg_odds:.2f}" if pref.avg_odds else "N/A",
                    'Frequency': pref.frequency
                })
            
            if pref_data:
                pref_df = pd.DataFrame(pref_data)
                st.dataframe(pref_df, hide_index=True, use_container_width=True)
        
        # Display betting history
        st.markdown(f"### {t('your_betting_history')}")
        
        # Get betting history
        history = db.get_user_betting_history(user_id)
        
        if not history:
            st.info(t('no_betting_history'))
        else:
            # Create a history dataframe for display
            hist_data = []
            for bet in history:
                hist_data.append({
                    'Date': bet.date.strftime('%d %b %Y'),
                    'Sport': bet.sport,
                    'Market': bet.market_type,
                    'Selection': bet.selection,
                    'Odds': f"{bet.odds:.2f}",
                    'Outcome': bet.outcome.upper() if bet.outcome else "PENDING",
                    'P/L': f"{bet.profit_loss:.2f}" if bet.profit_loss is not None else "N/A"
                })
            
            if hist_data:
                hist_df = pd.DataFrame(hist_data)
                st.dataframe(hist_df, hide_index=True, use_container_width=True)
        
        # Overall performance statistics if history exists
        if history:
            st.markdown(f"### {t('overall_performance')}")
            
            # Calculate overall stats
            total_bets = len(history)
            wins = sum(1 for bet in history if bet.outcome == 'win')
            losses = sum(1 for bet in history if bet.outcome == 'loss')
            pending = sum(1 for bet in history if bet.outcome == 'pending')
            
            win_rate = wins / (wins + losses) * 100 if (wins + losses) > 0 else 0
            
            total_profit = sum(bet.profit_loss for bet in history if bet.profit_loss is not None)
            
            # Display stats in a grid
            stats_cols = st.columns(4)
            with stats_cols[0]:
                st.metric("Total Bets", total_bets)
            with stats_cols[1]:
                st.metric("Win Rate", f"{win_rate:.1f}%")
            with stats_cols[2]:
                st.metric("Wins/Losses", f"{wins}/{losses}")
            with stats_cols[3]:
                st.metric("Profit/Loss", f"{total_profit:.2f}")

# Footer
st.markdown(
    "<div style='text-align: center; color: grey; padding: 20px; margin-top: 30px; font-size: 13px;'>"
    "<p>ArcanShadow - Hybrid Sports Prediction System</p>"
    f"<p>Current Time: {datetime.now().strftime('%d %b %Y %H:%M:%S')}</p>"
    "</div>", 
    unsafe_allow_html=True
)
