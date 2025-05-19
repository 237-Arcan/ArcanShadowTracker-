"""
Module pour l'affichage des prédictions au format mobile
Implémente un design d'interface similaire aux applications mobiles de paris sportifs
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import time
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importer notre module adaptateur pour l'API Football
from api.football_adapter import (
    get_upcoming_matches,
    get_team_statistics,
    get_h2h_matches, 
    get_team_last_matches,
    get_available_leagues
)

def get_country_flag_emoji(country):
    """Renvoie l'emoji du drapeau correspondant au pays"""
    country = str(country).upper()
    
    flag_mapping = {
        "ANGLETERRE": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "ENGLAND": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "ROYAUME-UNI": "🇬🇧",
        "UNITED KINGDOM": "🇬🇧",
        "ESPAGNE": "🇪🇸",
        "SPAIN": "🇪🇸",
        "FRANCE": "🇫🇷",
        "ALLEMAGNE": "🇩🇪",
        "GERMANY": "🇩🇪",
        "ITALIE": "🇮🇹",
        "ITALY": "🇮🇹",
        "PORTUGAL": "🇵🇹",
        "PAYS-BAS": "🇳🇱",
        "NETHERLANDS": "🇳🇱",
        "BELGIQUE": "🇧🇪",
        "BELGIUM": "🇧🇪",
        "BRÉSIL": "🇧🇷",
        "BRAZIL": "🇧🇷",
        "ARGENTINE": "🇦🇷",
        "ARGENTINA": "🇦🇷",
        "AFRIQUE DU SUD": "🇿🇦",
        "SOUTH AFRICA": "🇿🇦",
        "ALGÉRIE": "🇩🇿",
        "ALGERIA": "🇩🇿",
        "ARABIE SAOUDITE": "🇸🇦",
        "SAUDI ARABIA": "🇸🇦",
        "EUROPE": "🇪🇺"
    }
    
    return flag_mapping.get(country, "🏆")  # Retourne une icône de trophée par défaut

def generate_demo_matches(days=7):
    """Génère des matchs de démonstration en cas d'erreur de l'API"""
    matches = []
    leagues = [
        {"id": 39, "name": "Premier League", "country": "ANGLETERRE"},
        {"id": 140, "name": "La Liga", "country": "ESPAGNE"},
        {"id": 61, "name": "Ligue 1", "country": "FRANCE"},
        {"id": 78, "name": "Bundesliga", "country": "ALLEMAGNE"},
        {"id": 135, "name": "Serie A", "country": "ITALIE"},
        {"id": 2, "name": "Champions League", "country": "EUROPE"},
        {"id": 233, "name": "Premiership", "country": "AFRIQUE DU SUD"},
        {"id": 262, "name": "Saudi Pro League", "country": "ARABIE SAOUDITE"}
    ]
    
    teams_by_league = {
        39: ["Arsenal", "Chelsea", "Liverpool", "Manchester City", "Manchester United", "Tottenham", "Newcastle", "Aston Villa"],
        140: ["Real Madrid", "Barcelona", "Atletico Madrid", "Sevilla", "Valencia", "Villarreal", "Athletic Bilbao", "Real Sociedad"],
        61: ["PSG", "Marseille", "Lyon", "Monaco", "Lille", "Rennes", "Nice", "Lens"],
        78: ["Bayern Munich", "Borussia Dortmund", "RB Leipzig", "Leverkusen", "Wolfsburg", "Gladbach", "Frankfurt", "Union Berlin"],
        135: ["Inter Milan", "Milan", "Juventus", "Napoli", "Roma", "Lazio", "Atalanta", "Fiorentina"],
        2: ["Real Madrid", "Manchester City", "Bayern Munich", "PSG", "Barcelona", "Liverpool", "Inter Milan", "Borussia Dortmund"],
        233: ["Kaizer Chiefs", "Orlando Pirates", "Mamelodi Sundowns", "SuperSport United", "Cape Town City FC", "Stellenbosch FC"],
        262: ["Al Hilal", "Al Nassr", "Al Ahli", "Al Ittihad", "Al Shabab", "Al Taawoun"]
    }
    
    venues = {
        39: ["Emirates Stadium", "Stamford Bridge", "Anfield", "Etihad Stadium", "Old Trafford", "Tottenham Hotspur Stadium"],
        140: ["Santiago Bernabéu", "Camp Nou", "Wanda Metropolitano", "Ramón Sánchez Pizjuán", "Mestalla"],
        61: ["Parc des Princes", "Stade Vélodrome", "Groupama Stadium", "Stade Louis II", "Stade Pierre-Mauroy"],
        78: ["Allianz Arena", "Signal Iduna Park", "Red Bull Arena", "BayArena", "Volkswagen Arena"],
        135: ["San Siro", "Juventus Stadium", "Stadio Diego Armando Maradona", "Stadio Olimpico", "Gewiss Stadium"],
        2: ["Santiago Bernabéu", "Etihad Stadium", "Allianz Arena", "Parc des Princes", "Camp Nou", "Anfield"],
        233: ["FNB Stadium", "Orlando Stadium", "Loftus Versfeld Stadium", "Cape Town Stadium"],
        262: ["King Fahd International Stadium", "King Abdullah Sports City", "Prince Abdullah bin Jalawi Stadium"]
    }
    
    today = datetime.now()
    
    # Générer des matchs pour chaque jour
    for day in range(days):
        current_date = today + timedelta(days=day)
        
        # Générer plus de matchs pour les jours de week-end
        matches_per_day = 8 if current_date.weekday() >= 5 else 5
        
        # Répartir les matchs entre les différentes ligues
        leagues_for_day = random.sample(leagues, min(len(leagues), matches_per_day))
        
        for league in leagues_for_day:
            league_id = league["id"]
            
            # S'assurer que la ligue a suffisamment d'équipes
            if league_id in teams_by_league and len(teams_by_league[league_id]) >= 2:
                # Nombre de matchs à générer pour cette ligue
                matches_for_league = random.randint(1, 4)
                
                # S'assurer qu'on a assez d'équipes pour générer ces matchs
                matches_for_league = min(matches_for_league, len(teams_by_league[league_id]) // 2)
                
                # Mélanger les équipes pour cette ligue
                shuffled_teams = random.sample(teams_by_league[league_id], len(teams_by_league[league_id]))
                
                # Générer les matchs
                for i in range(matches_for_league):
                    if 2*i + 1 < len(shuffled_teams):
                        home_team = shuffled_teams[2*i]
                        away_team = shuffled_teams[2*i + 1]
                        
                        # Créer un nouveau match
                        match_hour = random.randint(12, 21)
                        match_minute = random.choice([0, 15, 30, 45])
                        match_datetime = current_date.replace(hour=match_hour, minute=match_minute)
                        
                        # Sélectionner un stade pour ce match
                        venue = random.choice(venues.get(league_id, ["Stade Municipal"]))
                        
                        match = {
                            "id": f"{day}_{league_id}_{i}",
                            "league_id": league_id,
                            "league": {"id": league_id, "name": league["name"]},
                            "league_name": league["name"],
                            "country": league["country"],
                            "home_team": home_team,
                            "away_team": away_team,
                            "date": match_datetime.isoformat(),
                            "time": match_datetime.strftime("%H:%M"),
                            "venue": venue,
                            "referee": f"Arbitre Demo {random.randint(1, 20)}",
                            "temperature": f"{random.randint(15, 28)}°C",
                            "weather": random.choice(["Ensoleillé", "Nuageux", "Pluie légère", "Clair"])
                        }
                        
                        matches.append(match)
    
    # Trier les matchs par date
    matches.sort(key=lambda x: x["date"])
    return matches

def display_mobile_football_predictions():
    """
    Affiche les prédictions de football dans un style mobile comme demandé
    """
    # Ajouter le CSS personnalisé
    st.markdown("""
    <style>
    .date-selector {
        display: flex;
        overflow-x: auto;
        margin-bottom: 20px;
        padding: 10px 0;
        border-bottom: 1px solid #333;
    }
    .date-item {
        flex: 0 0 auto;
        padding: 8px 15px;
        margin-right: 10px;
        border-radius: 20px;
        cursor: pointer;
        text-align: center;
        font-weight: bold;
    }
    .date-active {
        background-color: #FF2B6B;
        color: white;
    }
    .date-inactive {
        background-color: #333;
        color: #ccc;
    }
    .league-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 15px;
        margin-bottom: 8px;
        background-color: #2E2E3F;
        border-radius: 10px;
        cursor: pointer;
    }
    .league-item:hover {
        background-color: #3E3E4F;
    }
    .flag-icon {
        width: 24px;
        height: 18px;
        margin-right: 10px;
    }
    .league-name {
        flex: 1;
        font-weight: bold;
    }
    .match-count {
        font-weight: bold;
        color: #aaa;
    }
    .header-section {
        font-weight: bold;
        color: #999;
        margin: 15px 0 10px 0;
        text-transform: uppercase;
        font-size: 14px;
    }
    .match-list {
        margin-top: 20px;
    }
    .match-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #2E2E3F;
        border-radius: 10px;
        cursor: pointer;
    }
    .team-home, .team-away {
        text-align: center;
        width: 40%;
    }
    .match-time {
        text-align: center;
        width: 20%;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # En-tête
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <span style="font-size: 32px; margin-right: 10px;">⚽</span>
            <h1 style="margin: 0;">Football</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialiser la session_state
    if 'selected_date_idx' not in st.session_state:
        st.session_state.selected_date_idx = 0
    
    # Créer un sélecteur de dates sur 7 jours
    today = datetime.now()
    date_options = []
    
    # Générer les options de date pour les 7 prochains jours
    for i in range(7):
        day = today + timedelta(days=i)
        date_options.append({
            "date": day.date(),
            "label": "AUJOURD'HUI" if i == 0 else "DEMAIN" if i == 1 else day.strftime("%a").upper(),
            "day": day.strftime("%d"),
            "month": day.strftime("%m")
        })
    
    # Générer le HTML pour le sélecteur de dates
    date_selector_html = '<div class="date-selector">'
    for i, date_opt in enumerate(date_options):
        active_class = "date-active" if i == st.session_state.selected_date_idx else "date-inactive"
        date_selector_html += f'<div class="date-item {active_class}" id="date_{i}">{date_opt["label"]}<br>{date_opt["day"]}.{date_opt["month"]}</div>'
    date_selector_html += '</div>'
    
    st.markdown(date_selector_html, unsafe_allow_html=True)
    
    # Pour la démo, permettre à l'utilisateur de sélectionner une date avec un select standard
    selected_date_idx = st.selectbox(
        "Sélectionner une date",
        range(len(date_options)),
        format_func=lambda i: f"{date_options[i]['label']} {date_options[i]['day']}.{date_options[i]['month']}",
        index=st.session_state.selected_date_idx,
        key="date_select"
    )
    
    # Mettre à jour la date sélectionnée
    st.session_state.selected_date_idx = selected_date_idx
    selected_date = date_options[selected_date_idx]["date"]
    
    # Récupérer tous les matchs à venir
    try:
        all_upcoming_matches = get_upcoming_matches(days_ahead=7)
        logger.info(f"Récupéré {len(all_upcoming_matches)} matchs à venir")
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des matchs: {str(e)}")
        st.info("Utilisation de données de démonstration...")
        all_upcoming_matches = generate_demo_matches(days=7)
    
    # Récupérer les ligues disponibles
    try:
        leagues = load_available_leagues()
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des ligues: {str(e)}")
        # Utiliser les ligues de nos matchs de démo
        leagues = []
        for match in all_upcoming_matches:
            league_id = match.get('league_id', 0)
            league_name = match.get('league_name', '')
            country = match.get('country', 'Inconnu')
            
            if not any(l.get('id') == league_id for l in leagues):
                leagues.append({
                    'id': league_id,
                    'name': league_name,
                    'country': country
                })
    
    # Regrouper les matchs par ligue pour la date sélectionnée
    leagues_with_matches = {}
    
    for match in all_upcoming_matches:
        try:
            match_date = datetime.fromisoformat(match['date'].replace('Z', '+00:00')).date()
            
            # Si le match est à la date sélectionnée
            if match_date == selected_date:
                league_id = match.get('league_id', 0)
                if league_id not in leagues_with_matches:
                    # Trouver les détails de la ligue
                    league_info = next((l for l in leagues if l.get('id') == league_id), 
                                     {"id": league_id, "name": match.get('league_name', f"Ligue {league_id}"), 
                                      "country": match.get('country', "Inconnu")})
                    leagues_with_matches[league_id] = {
                        "info": league_info,
                        "matches": []
                    }
                
                # Ajouter des informations complémentaires si nécessaires
                if 'venue' not in match:
                    match['venue'] = "Information non disponible"
                if 'referee' not in match:
                    match['referee'] = "Information non disponible"
                    
                leagues_with_matches[league_id]["matches"].append(match)
        except Exception as e:
            logger.error(f"Erreur lors du traitement du match: {str(e)}")
    
    # Nombre total de matchs pour la date sélectionnée
    total_matches = sum(len(league_data["matches"]) for league_data in leagues_with_matches.values())
    
    # Afficher le compteur de matchs
    st.markdown(f'<div style="display: flex; align-items: center; margin: 20px 0;"><div style="display: flex; align-items: center;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 6H20M4 12H20M4 18H20" stroke="white" stroke-width="2"/></svg></div><div style="margin-left: 10px; font-weight: bold;">Tous les matchs</div><div style="margin-left: auto; color: #999; font-weight: bold;">{total_matches}</div></div>', unsafe_allow_html=True)
    
    # Diviser en compétitions favorites et autres compétitions
    favorite_leagues = [39, 140, 61, 78, 135, 2]  # Les IDs des ligues majeures: Premier League, Liga, etc.
    
    # Afficher les compétitions favorites
    st.markdown('<div class="header-section">COMPÉTITIONS FAVORITES</div>', unsafe_allow_html=True)
    
    has_favorite = False
    for league_id in favorite_leagues:
        if league_id in leagues_with_matches:
            has_favorite = True
            league_data = leagues_with_matches[league_id]
            league_info = league_data["info"]
            matches_count = len(league_data["matches"])
            
            # Déterminer le drapeau basé sur le pays
            country = league_info.get("country", "Inconnu")
            flag_emoji = get_country_flag_emoji(country)
            
            # Créer un identifiant unique pour cette ligue
            league_key = f"league_{league_id}"
            
            # Afficher la ligue avec son drapeau et le nombre de matchs
            league_html = f"""
            <div class="league-item" id="{league_key}">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 24px; margin-right: 10px;">{flag_emoji}</span>
                    <div>
                        <div style="color: #999; font-size: 12px;">{country}</div>
                        <div class="league-name">{league_info["name"]}</div>
                    </div>
                </div>
                <div class="match-count">{matches_count}</div>
            </div>
            """
            
            st.markdown(league_html, unsafe_allow_html=True)
            
            # Créer un bouton caché à côté pour la sélection
            if st.button(f"Voir {league_info['name']}", key=league_key, help=f"Voir les matchs de {league_info['name']}"):
                st.session_state.selected_league_id = league_id
    
    if not has_favorite:
        st.info("Pas de matchs dans vos compétitions favorites pour cette date")
    
    # Afficher les autres compétitions
    st.markdown('<div class="header-section">AUTRES COMPÉTITIONS [A-Z]</div>', unsafe_allow_html=True)
    
    other_leagues = [lid for lid in leagues_with_matches if lid not in favorite_leagues]
    
    if not other_leagues:
        st.info("Pas d'autres matchs disponibles pour cette date")
    else:
        for league_id in other_leagues:
            league_data = leagues_with_matches[league_id]
            league_info = league_data["info"]
            matches_count = len(league_data["matches"])
            
            # Déterminer le drapeau basé sur le pays
            country = league_info.get("country", "Inconnu")
            flag_emoji = get_country_flag_emoji(country)
            
            # Créer un identifiant unique pour cette ligue
            league_key = f"other_league_{league_id}"
            
            # Afficher la ligue avec son drapeau et le nombre de matchs
            league_html = f"""
            <div class="league-item" id="{league_key}">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 24px; margin-right: 10px;">{flag_emoji}</span>
                    <div>
                        <div style="color: #999; font-size: 12px;">{country}</div>
                        <div class="league-name">{league_info["name"]}</div>
                    </div>
                </div>
                <div class="match-count">{matches_count}</div>
            </div>
            """
            
            st.markdown(league_html, unsafe_allow_html=True)
            
            # Créer un bouton caché à côté pour la sélection
            if st.button(f"Voir {league_info['name']}", key=league_key, help=f"Voir les matchs de {league_info['name']}"):
                st.session_state.selected_league_id = league_id
    
    # Si une ligue est sélectionnée, afficher ses matchs
    if 'selected_league_id' in st.session_state and st.session_state.selected_league_id in leagues_with_matches:
        selected_league_id = st.session_state.selected_league_id
        selected_league_info = leagues_with_matches[selected_league_id]["info"]
        selected_league_matches = leagues_with_matches[selected_league_id]["matches"]
        
        st.markdown(f"## Matchs - {selected_league_info['name']}")
        
        # Afficher les matchs
        for match in selected_league_matches:
            match_time = match.get('time', '??:??')
            if isinstance(match.get('date'), str) and 'T' in match['date']:
                try:
                    match_dt = datetime.fromisoformat(match['date'].replace('Z', '+00:00'))
                    match_time = match_dt.strftime('%H:%M')
                except:
                    pass
            
            # Afficher le match
            match_html = f"""
            <div class="match-item">
                <div class="team-home">{match['home_team']}</div>
                <div class="match-time">{match_time}</div>
                <div class="team-away">{match['away_team']}</div>
            </div>
            """
            
            st.markdown(match_html, unsafe_allow_html=True)
            
            # Créer un bouton pour voir les détails de ce match
            match_key = f"match_{match.get('id', hash(match['home_team'] + match['away_team']))}"
            if st.button(f"Analyser ce match", key=match_key):
                st.session_state.selected_match = match
    
    # Si un match est sélectionné, afficher ses détails
    if 'selected_match' in st.session_state:
        selected_match = st.session_state.selected_match
        
        st.markdown("## Détails du match")
        
        # Afficher une carte détaillée du match
        match_date = datetime.fromisoformat(selected_match['date'].replace('Z', '+00:00'))
        date_string = match_date.strftime('%d/%m/%Y %H:%M')
        
        # Créer une présentation élégante du match
        st.markdown(f"""
        <div class="match-card" style="background-color: #1E1E2E; padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #444;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div style="text-align: center; width: 40%;">
                    <h4>{selected_match['home_team']}</h4>
                </div>
                <div style="text-align: center; width: 20%;">
                    <h3>VS</h3>
                </div>
                <div style="text-align: center; width: 40%;">
                    <h4>{selected_match['away_team']}</h4>
                </div>
            </div>
            
            <hr style="border-color: #444; margin: 10px 0;">
            
            <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                <div style="width: 50%;">
                    <p><strong>Date:</strong> {date_string}</p>
                    <p><strong>Stade:</strong> {selected_match.get('venue', 'Information non disponible')}</p>
                </div>
                <div style="width: 50%;">
                    <p><strong>Arbitre:</strong> {selected_match.get('referee', 'Information non disponible')}</p>
                    <p><strong>Météo:</strong> {selected_match.get('temperature', '')} {selected_match.get('weather', 'Information non disponible')}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Afficher les prédictions pour ce match (section factice pour la démonstration)
        st.markdown("### Prédictions ArcanShadow")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="text-align:center; padding: 15px; background-color: #2E3E4F; border-radius: 10px;">
                <h4>Victoire Domicile</h4>
                <h2>42%</h2>
                <p>Cote: 1.85</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div style="text-align:center; padding: 15px; background-color: #2E3E4F; border-radius: 10px;">
                <h4>Match Nul</h4>
                <h2>28%</h2>
                <p>Cote: 3.40</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div style="text-align:center; padding: 15px; background-color: #2E3E4F; border-radius: 10px;">
                <h4>Victoire Extérieur</h4>
                <h2>30%</h2>
                <p>Cote: 3.25</p>
            </div>
            """, unsafe_allow_html=True)

def display_mobile_predictions():
    """
    Fonction principale pour afficher l'onglet Prédictions au format mobile
    """
    display_mobile_football_predictions()

if __name__ == "__main__":
    st.set_page_config(page_title="ArcanShadow Prédictions", page_icon="⚽", layout="wide")
    display_mobile_predictions()