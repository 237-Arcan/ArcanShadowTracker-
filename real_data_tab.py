import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime, timedelta
import sys
import os

# Ajouter le répertoire courant au chemin pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.football_data import get_future_matches
from utils.daily_combo import get_daily_combos
from utils.prediction_analysis import get_prediction_data

def load_real_football_data():
    """Charge les données réelles de football"""
    main_leagues = ['en.1', 'es.1', 'it.1', 'de.1', 'fr.1', 'uefa.cl']
    featured_matches, all_matches = get_future_matches(
        days_ahead=10,
        league_ids=main_leagues,
        season="2024-25"
    )
    return featured_matches, all_matches

def display_real_data_tab():
    """Affiche l'onglet avec les données réelles de football"""
    st.title("🌍 Données Réelles de Football")
    st.markdown("Visualisez et analysez les données réelles des principales ligues européennes de football.")
    
    try:
        # Charger les données réelles
        featured_matches, all_matches = load_real_football_data()
        
        # Combiner toutes les données pour analyse
        all_data = featured_matches + all_matches
        
        # Afficher des statistiques générales
        st.subheader("📊 Aperçu des Données")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            num_leagues = len(set([m.get('league', '') for m in all_data if isinstance(m, dict)]))
            st.metric("Ligues couvertes", str(num_leagues))
            
        with col2:
            num_matches = len(all_data)
            st.metric("Matchs disponibles", str(num_matches))
            
        with col3:
            num_teams = len(set([m.get('home_team', m.get('home', '')) for m in all_data if isinstance(m, dict)] + 
                             [m.get('away_team', m.get('away', '')) for m in all_data if isinstance(m, dict)]))
            st.metric("Équipes uniques", str(num_teams))
        
        # Liste déroulante pour choisir une ligue
        leagues = ["Toutes les ligues"] + sorted(list(set([m.get('league', '') for m in all_data if isinstance(m, dict)])))
        selected_league = st.selectbox("Sélectionner une ligue", leagues)
        
        # Filtrer par ligue
        if selected_league != "Toutes les ligues":
            filtered_matches = [m for m in all_data if isinstance(m, dict) and m.get('league', '') == selected_league]
        else:
            filtered_matches = all_data
        
        # Section des matchs
        st.subheader("⚽ Matchs à venir")
        
        # Organiser les matchs par date
        matches_by_date = {}
        for match in filtered_matches:
            if not isinstance(match, dict):
                continue
                
            match_date = match.get('date', '')
            if match_date not in matches_by_date:
                matches_by_date[match_date] = []
                
            matches_by_date[match_date].append(match)
        
        # Trier les dates
        sorted_dates = sorted(matches_by_date.keys())
        
        # Créer un accordéon pour chaque date
        for date in sorted_dates:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
            except:
                formatted_date = date
                
            with st.expander(f"📅 {formatted_date}", expanded=(date == sorted_dates[0])):
                for match in matches_by_date[date]:
                    home_team = match.get('home_team', match.get('home', '?'))
                    away_team = match.get('away_team', match.get('away', '?'))
                    league = match.get('league', '')
                    time = match.get('time', match.get('kickoff_time', '??:??'))
                    
                    # Obtenir les cotes et probabilités
                    home_odds = match.get('home_odds', 0)
                    draw_odds = match.get('draw_odds', 0)
                    away_odds = match.get('away_odds', 0)
                    
                    home_prob = match.get('home_prob', 0)
                    draw_prob = match.get('draw_prob', 0)
                    away_prob = match.get('away_prob', 0)
                    
                    # Carte de match
                    match_col1, match_col2 = st.columns([3, 1])
                    
                    with match_col1:
                        st.markdown(f"""
                        <div style="padding: 10px; border-radius: 8px; background: rgba(17, 23, 64, 0.7); margin-bottom: 10px;">
                            <div style="font-size: 16px; font-weight: bold; color: white; margin-bottom: 5px;">
                                {home_team} vs {away_team}
                            </div>
                            <div style="font-size: 14px; color: rgba(255, 255, 255, 0.7);">
                                {league} • {time}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with match_col2:
                        if home_odds > 0 and draw_odds > 0 and away_odds > 0:
                            st.markdown(f"""
                            <div style="text-align: center; padding: 10px; border-radius: 8px; background: rgba(17, 23, 64, 0.7); margin-bottom: 10px;">
                                <div style="display: flex; justify-content: space-between; font-size: 14px; color: white;">
                                    <div>{home_odds:.2f}</div>
                                    <div>{draw_odds:.2f}</div>
                                    <div>{away_odds:.2f}</div>
                                </div>
                                <div style="display: flex; justify-content: space-between; font-size: 12px; color: rgba(255, 255, 255, 0.7);">
                                    <div>1</div>
                                    <div>X</div>
                                    <div>2</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
        
        # Section d'analyse approfondie
        st.subheader("🔍 Analyse Approfondie")
        
        # Sélectionner un match à analyser
        match_options = []
        for match in all_data:
            if isinstance(match, dict):
                home = match.get('home_team', match.get('home', '?'))
                away = match.get('away_team', match.get('away', '?'))
                league = match.get('league', '?')
                time = match.get('time', match.get('kickoff_time', '??:??'))
                date = match.get('date', '')
                
                if date:
                    try:
                        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
                    except:
                        formatted_date = date
                else:
                    formatted_date = ""
                
                match_options.append(f"{home} vs {away} ({league}) - {formatted_date}")
        
        selected_match_idx = st.selectbox("Sélectionner un match à analyser", range(len(match_options)), format_func=lambda x: match_options[x])
        selected_match = all_data[selected_match_idx] if selected_match_idx < len(all_data) else None
        
        if selected_match:
            # Analyser le match sélectionné
            analysis = get_prediction_data(selected_match, all_data)
            
            # Afficher l'analyse
            home_team = analysis['match_info']['home_team']
            away_team = analysis['match_info']['away_team']
            
            st.markdown(f"#### Prédiction pour {home_team} vs {away_team}")
            
            # Résultat le plus probable
            main_outcome = analysis['main_prediction']['outcome']
            main_odds = analysis['main_prediction']['odds']
            confidence = analysis['main_prediction']['confidence']
            
            st.markdown(f"""
            <div style="background: rgba(112, 0, 255, 0.1); padding: 15px; border-radius: 8px; 
                    border: 1px solid rgba(112, 0, 255, 0.2); margin-bottom: 15px;">
                <table width="100%" style="border-collapse: collapse;">
                    <tr>
                        <td>
                            <div style="font-size: 18px; color: rgba(255, 255, 255, 0.9);">Résultat le plus probable</div>
                            <div style="font-size: 24px; font-weight: bold; color: #7000ff;">{main_outcome}</div>
                        </td>
                        <td align="right">
                            <div style="font-size: 24px; font-weight: bold; color: white;">{main_odds}</div>
                            <div style="font-size: 14px; color: #01ff80;">Confiance: {confidence}%</div>
                        </td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            
            # Autres scénarios
            st.markdown("#### Autres scénarios")
            
            other_scenarios_cols = st.columns(2)
            
            for i, scenario in enumerate(analysis['other_scenarios'][:4]):
                col = other_scenarios_cols[i % 2]
                
                with col:
                    prob = scenario['probability']
                    prob_color = "#01ff80" if prob >= 80 else "#ffbe41" if prob >= 50 else "#ff3364"
                    
                    st.markdown(f"""
                    <div style="padding: 10px; background: rgba(255, 255, 255, 0.05); border-radius: 5px; margin-bottom: 10px;">
                        <table width="100%" style="border-collapse: collapse;">
                            <tr>
                                <td><div style="color: white;">{scenario['name']}</div></td>
                                <td align="right"><div style="color: {prob_color};">{scenario['odds']} <span style="opacity: 0.7; font-size: 0.9em;">({prob}%)</span></div></td>
                            </tr>
                        </table>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Narratif
            st.markdown("#### Narratif de l'analyse")
            
            st.markdown(f"""
            <div style="padding: 15px; border-radius: 10px; background: rgba(8, 15, 40, 0.5); 
                        border: 1px solid rgba(81, 99, 149, 0.3); margin-bottom: 15px;">
                <p style="color: rgba(255, 255, 255, 0.85); font-size: 16px; line-height: 1.6;">
                    {analysis['narrative'].replace('\n\n', '<br><br>')}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Section des combinaisons
        st.subheader("🎯 Combinaisons optimisées")
        
        daily_combos = get_daily_combos(all_data, days_range=7, combo_sizes=[2, 3, 4])
        
        combo_size = st.radio("Nombre de sélections", [2, 3, 4], horizontal=True)
        
        if combo_size in daily_combos and daily_combos[combo_size]:
            combo = daily_combos[combo_size][0]  # Premier combo de la taille sélectionnée
            
            # Afficher les sélections
            for sel in combo['matches']:
                match = sel['match']
                league = sel['league']
                time = sel['time']
                selection = sel['selection']
                odds = sel['odds']
                confidence = sel['confidence']
                
                confidence_color = "#01ff80" if confidence >= 85 else "#ffbe41" if confidence >= 70 else "#ff3364"
                
                st.markdown(f"""
                <div style="border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 12px; 
                          margin-bottom: 10px; background: rgba(17, 23, 64, 0.7);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div style="font-size: 16px; font-weight: bold; color: white;">
                            {match}
                        </div>
                        <div style="color: {confidence_color}; font-weight: bold;">
                            {confidence}%
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 8px;">
                        <div style="color: rgba(255, 255, 255, 0.7);">
                            {league} • {time}
                        </div>
                        <div style="color: white; font-weight: bold;">
                            {odds}
                        </div>
                    </div>
                    <div style="color: white; background: rgba(81, 99, 149, 0.2); padding: 8px; border-radius: 5px; font-size: 15px;">
                        {selection}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Afficher la cote totale
            st.markdown(f"""
            <div style="border: 1px solid rgba(1, 255, 128, 0.3); border-radius: 8px; padding: 15px; 
                      margin-top: 15px; background: rgba(1, 255, 128, 0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-size: 18px; font-weight: bold; color: #01ff80;">
                        Cote combinée
                    </div>
                    <div style="font-size: 22px; font-weight: bold; color: white;">
                        {combo['total_odds']:.2f}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info(f"Aucune combinaison disponible avec {combo_size} sélections.")
        
    except Exception as e:
        st.error(f"Une erreur s'est produite lors du chargement des données: {str(e)}")
        st.info("Les données réelles ne sont pas disponibles actuellement. Veuillez réessayer plus tard.")
        
# Fonction pour ajouter l'onglet au menu principal
def add_real_data_tab():
    if 'show_real_data_tab' not in st.session_state:
        st.session_state.show_real_data_tab = True
        
    if st.session_state.show_real_data_tab:
        display_real_data_tab()