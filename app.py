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
    st.session_state.selected_league = 'Premier League'
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = datetime.now().date()
if 'prediction_generated' not in st.session_state:
    st.session_state.prediction_generated = False
if 'loading_prediction' not in st.session_state:
    st.session_state.loading_prediction = False
if 'language' not in st.session_state:
    st.session_state.language = 'en'  # Default language is English

# Function to get translated text
def t(key, **format_args):
    """Helper function to get text in the current language"""
    return get_text(key, st.session_state.language, **format_args)

# Initialize modules
data_handler = DataHandler()
arcan_x = ArcanX()
shadow_odds = ShadowOdds()
convergence = Convergence()
meta_systems = MetaSystems()

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
    
    # Generate prediction button
    if st.button(t('generate_predictions')):
        st.session_state.loading_prediction = True

# Main content area with tabs
tab1, tab2, tab3, tab4 = st.tabs([
    t('predictions_tab'), 
    t('dashboard_tab'), 
    t('historical_tab'), 
    t('module_details_tab')
])

with tab1:
    # Header section with explanatory text
    st.markdown(f"## {t('match_predictions')}")
    st.markdown(t('predictions_description'))
    
    # Get upcoming matches for selected sport, league and date
    upcoming_matches = data_handler.get_upcoming_matches(st.session_state.selected_sport, st.session_state.selected_league, st.session_state.selected_date)
    
    # Handle loading prediction state
    if st.session_state.loading_prediction:
        prediction_progress = st.progress(0)
        
        for i in range(101):
            prediction_progress.progress(i/100)
            time.sleep(0.02)
        
        st.session_state.prediction_generated = True
        st.session_state.loading_prediction = False
        st.rerun()
    
    # Display predictions
    if st.session_state.prediction_generated and len(upcoming_matches) > 0:
        for match in upcoming_matches:
            # Generate predictions for this match
            arcan_x_results = arcan_x.analyze_match(match) if arcan_x_active else {'confidence': 0.5, 'factors': []}
            shadow_odds_results = shadow_odds.analyze_match(match) if shadow_odds_active else {'confidence': 0.5, 'factors': []}
            
            # Calculate combined prediction
            prediction = convergence.generate_prediction(match, arcan_x_results, shadow_odds_results)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div class='prediction-card'>
                    <h3>{match['home_team']} {t('vs')} {match['away_team']}</h3>
                    <p>{t('date')}: {match['date'].strftime('%d %b %Y %H:%M')}</p>
                    <p>{t('prediction')}: <span class='gold-text'>{prediction['outcome']}</span></p>
                    <p>{t('confidence')}: {prediction['confidence']*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
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
                st.plotly_chart(fig, use_container_width=True, key=f"gauge_{match['home_team']}_{match['away_team']}")
            
            # Show prediction details in an expander
            with st.expander(t('view_details')):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"### {t('statistical_factors')}")
                    for factor in prediction['statistical_factors']:
                        factor_name = factor['name']
                        # Try to translate the factor name
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
                        
                        st.markdown(f"- {factor_name}: {factor['value']}")
                
                with col2:
                    st.markdown(f"### {t('esoteric_factors')}")
                    for factor in prediction['esoteric_factors']:
                        factor_name = factor['name']
                        # Try to translate the factor name
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
                        
                        st.markdown(f"- {factor_name}: {factor['value']}")
                
                st.markdown(f"### {t('odds_analysis')}")
                for factor in prediction['odds_factors']:
                    factor_name = factor['name']
                    # Try to translate the factor name
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
                    
                    st.markdown(f"- {factor_name}: {factor['value']}")
    elif not st.session_state.prediction_generated:
        st.info(t('no_predictions'))
    else:
        st.info(t('no_matches', league=st.session_state.selected_league, date=st.session_state.selected_date.strftime('%d/%m/%Y')))

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
    
    # Module selection
    module_categories = {
        "ArcanX (Esoteric Analysis)": ["NumeriCode", "GematriaPulse", "AstroImpact Lite", "TarotEcho", 
                                      "YiFlow", "KarmicFlow+", "RadiEsthesiaMap", "CycleMirror"],
        "ShadowOdds (Odds Behavior)": ["LineTrap", "BetPulse", "CrowdPressureIndex", "MarketEcho", 
                                      "CollapseDetector", "ShadowMomentum", "SetTrapIndicator"],
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
    st.markdown("### Module Performance Visualization")
    
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

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center;'>"
    "<p>ArcanShadow - Hybrid Sports Prediction System</p>"
    f"<p>Current Time: {datetime.now().strftime('%d %b %Y %H:%M:%S')}</p>"
    "</div>", 
    unsafe_allow_html=True
)
