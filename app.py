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
from assets.symbols import get_symbol

# Page configuration
st.set_page_config(
    page_title="ArcanShadow - Hybrid Sports Prediction System",
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
st.markdown("<p class='gold-text'>Hybrid Prediction System: Statistics + Esoteric Analysis + Odds Behavior</p>", unsafe_allow_html=True)

# Sidebar for filters and controls
with st.sidebar:
    st.markdown("## 🧙‍♂️ System Controls")
    
    # Sport selection
    sports = ['Football', 'Basketball', 'Tennis', 'Baseball', 'Hockey']
    selected_sport = st.selectbox("Select Sport", sports, index=sports.index(st.session_state.selected_sport))
    st.session_state.selected_sport = selected_sport
    
    # League selection based on sport
    leagues = data_handler.get_leagues_for_sport(selected_sport)
    selected_league = st.selectbox("Select League", leagues, index=0 if st.session_state.selected_league not in leagues else leagues.index(st.session_state.selected_league))
    st.session_state.selected_league = selected_league
    
    # Date selection
    selected_date = st.date_input("Select Date", st.session_state.selected_date)
    st.session_state.selected_date = selected_date
    
    # Module activation checkboxes
    st.markdown("### Active Modules")
    arcan_x_active = st.checkbox("ArcanX (Esoteric Analysis)", value=True)
    shadow_odds_active = st.checkbox("ShadowOdds (Odds Behavior)", value=True)
    
    # Advanced settings collapsible
    with st.expander("Advanced Settings"):
        confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.65)
        cycles_depth = st.slider("Historical Cycles Depth", 1, 10, 5)
        esoteric_weight = st.slider("Esoteric Influence Weight", 0.0, 1.0, 0.4)
    
    # Generate prediction button
    if st.button("Generate Predictions"):
        st.session_state.loading_prediction = True

# Main content area with tabs
tab1, tab2, tab3, tab4 = st.tabs(["Predictions", "System Dashboard", "Historical Analysis", "Module Details"])

with tab1:
    # Header section with explanatory text
    st.markdown("## Match Predictions")
    st.markdown("Predictions generated using ArcanShadow's multi-layer architecture combining statistical data, esoteric patterns, and odds behavior analysis.")
    
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
                    <h3>{match['home_team']} vs {match['away_team']}</h3>
                    <p>Date: {match['date'].strftime('%d %b %Y %H:%M')}</p>
                    <p>Prediction: <span class='gold-text'>{prediction['outcome']}</span></p>
                    <p>Confidence: {prediction['confidence']*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Create the gauge chart for prediction confidence
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = prediction['confidence']*100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Confidence"},
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
                st.plotly_chart(fig, use_container_width=True)
            
            # Show prediction details in an expander
            with st.expander("View Prediction Details"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Statistical Factors")
                    for factor in prediction['statistical_factors']:
                        st.markdown(f"- {factor['name']}: {factor['value']}")
                
                with col2:
                    st.markdown("### Esoteric Factors")
                    for factor in prediction['esoteric_factors']:
                        st.markdown(f"- {factor['name']}: {factor['value']}")
                
                st.markdown("### Odds Analysis")
                for factor in prediction['odds_factors']:
                    st.markdown(f"- {factor['name']}: {factor['value']}")
    elif not st.session_state.prediction_generated:
        st.info("Click 'Generate Predictions' in the sidebar to analyze upcoming matches.")
    else:
        st.info(f"No upcoming matches found for {st.session_state.selected_league} on {st.session_state.selected_date}.")

with tab2:
    st.markdown("## System Dashboard")
    st.markdown("Real-time monitoring of ArcanShadow's performance and module activities.")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Prediction Accuracy (7d)", value="78.3%", delta="2.1%")
    
    with col2:
        st.metric(label="ArcanX Confidence", value="72.4%", delta="-1.3%")
    
    with col3:
        st.metric(label="ShadowOdds Accuracy", value="81.5%", delta="3.8%")
    
    with col4:
        st.metric(label="Active Modules", value="12/18")
    
    # System health visualization
    st.markdown("### System Health & Performance")
    
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
    
    st.plotly_chart(fig, use_container_width=True)
    
    # System activity timeline
    st.markdown("### System Activity Timeline")
    
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
    
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("## Historical Analysis")
    st.markdown("Review past predictions and performance metrics to improve future forecasts.")
    
    # Filters for historical analysis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        hist_sport = st.selectbox("Sport", sports, key="hist_sport")
    
    with col2:
        hist_leagues = data_handler.get_leagues_for_sport(hist_sport)
        hist_league = st.selectbox("League", hist_leagues, key="hist_league")
    
    with col3:
        date_range = st.selectbox("Time Period", 
                               ["Last 7 days", "Last 30 days", "Last 3 months", "Last 6 months", "Last year"],
                               index=1)
    
    # Historical performance metrics
    hist_data = data_handler.get_historical_predictions(hist_sport, hist_league, date_range)
    
    if hist_data:
        # Performance summary
        st.markdown("### Prediction Performance Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="Overall Accuracy", value=f"{hist_data['accuracy']*100:.1f}%")
        
        with col2:
            st.metric(label="ROI", value=f"{hist_data['roi']*100:.1f}%")
        
        with col3:
            st.metric(label="Predictions Made", value=hist_data['total_predictions'])
        
        # Historical accuracy by module
        st.markdown("### Module Performance Over Time")
        
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
                     labels={'Accuracy': 'Prediction Accuracy', 'Date': 'Date'},
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
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent predictions
        st.markdown("### Recent Predictions")
        
        recent_predictions = data_handler.get_recent_predictions(hist_sport, hist_league, 10)
        
        if recent_predictions:
            pred_df = pd.DataFrame(recent_predictions)
            pred_df['Correct'] = pred_df['correct'].apply(lambda x: '✅' if x else '❌')
            pred_df['Match'] = pred_df['home_team'] + ' vs ' + pred_df['away_team']
            pred_df['Score'] = pred_df['home_score'].astype(str) + ' - ' + pred_df['away_score'].astype(str)
            
            # Format the dataframe for display
            display_df = pred_df[['date', 'Match', 'prediction', 'Score', 'Correct', 'confidence']]
            display_df.columns = ['Date', 'Match', 'Prediction', 'Result', 'Correct', 'Confidence']
            
            st.dataframe(display_df, use_container_width=True)
        else:
            st.info("No recent prediction data available for the selected filters.")
    else:
        st.info("No historical data available for the selected criteria.")

with tab4:
    st.markdown("## Module Details")
    st.markdown("Explore the inner workings of ArcanShadow's prediction modules.")
    
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
        selected_category = st.selectbox("Module Category", list(module_categories.keys()))
    
    with col2:
        selected_module = st.selectbox("Specific Module", module_categories[selected_category])
    
    # Module descriptions (hardcoded for demonstration)
    module_descriptions = {
        "NumeriCode": {
            "description": "Interprets numérological patterns in dates, dossards, cycles, scores and calendar days.",
            "inputs": ["Match date", "Player numbers", "Team formation", "Historical scores"],
            "output": "Numerical pattern significance score (0-100)",
            "accuracy": "76.3%"
        },
        "GematriaPulse": {
            "description": "Analyzes kabbalistic values of team names, players, cities, stadiums, and competitions.",
            "inputs": ["Team names", "Player names", "Stadium name", "City name"],
            "output": "Gematria correlation strength (0-100)",
            "accuracy": "71.8%"
        },
        "LineTrap": {
            "description": "Identifies trapped odds that are misaligned with actual sport dynamics.",
            "inputs": ["Opening odds", "Current odds", "Market movement", "Betting volumes"],
            "output": "Trap probability percentage",
            "accuracy": "83.1%"
        },
        "BetPulse": {
            "description": "Tracks real-time rhythm and peaks in market betting patterns.",
            "inputs": ["Betting volumes", "Timing of bets", "Bet distribution", "Market reactions"],
            "output": "Market confidence map",
            "accuracy": "79.4%"
        },
        "Convergia Core": {
            "description": "Core fusion engine merging ArcanX and ShadowOdds outputs into a unified decision matrix.",
            "inputs": ["ArcanX signals", "ShadowOdds signals", "Historical correlations", "Current match context"],
            "output": "Integrated prediction with confidence level",
            "accuracy": "84.2%"
        }
    }
    
    # Display default description for modules not explicitly defined
    default_description = {
        "description": "Advanced prediction module within the ArcanShadow system.",
        "inputs": ["Match data", "Historical patterns", "Contextual information"],
        "output": "Specialized prediction signals",
        "accuracy": "75-85%"
    }
    
    # Get module info
    module_info = module_descriptions.get(selected_module, default_description)
    
    # Display module information
    st.markdown(f"### {selected_module}")
    st.markdown(f"**Description:** {module_info['description']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Inputs")
        for input_item in module_info['inputs']:
            st.markdown(f"- {input_item}")
    
    with col2:
        st.markdown("#### Output")
        st.markdown(module_info['output'])
        st.markdown(f"**Historical Accuracy:** {module_info['accuracy']}")
    
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
    
    st.plotly_chart(fig, use_container_width=True)
    
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
