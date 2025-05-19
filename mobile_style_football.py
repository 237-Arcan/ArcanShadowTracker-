"""
Module pour l'affichage des matchs de football en style mobile
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

def load_custom_css():
    """Charge un CSS personnalisé pour l'interface style mobile"""
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

def generate_date_selector():
    """Génère un sélecteur de dates horizontal style mobile"""
    today = datetime.now()
    date_options = []
    
    # Générer les options de date pour les 7 prochains jours
    for i in range(7):
        day = today + timedelta(days=i)
        if i == 0:
            label = "AUJOURD'HUI"
        elif i == 1:
            label = "DEMAIN"
        else:
            # Utiliser le nom court du jour en majuscule
            label = day.strftime("%a").upper()
        
        date_str = day.strftime("%d.%m")
        date_options.append({
            "date": day.date(),
            "label": label,
            "full_label": f"{label} {date_str}"
        })
    
    # Afficher le sélecteur de dates horizontal
    date_selector_html = '<div class="date-selector">'
    for i, date_opt in enumerate(date_options):
        active_class = "date-active" if i == 0 else "date-inactive"
        date_selector_html += f'<div class="date-item {active_class}">{date_opt["label"]}<br>{date_opt["date"].strftime("%d.%m")}</div>'
    date_selector_html += '</div>'
    
    st.markdown(date_selector_html, unsafe_allow_html=True)
    
    # Par défaut, sélectionner la date d'aujourd'hui
    return today.date()

def get_country_flag_emoji(country):
    """Renvoie l'emoji du drapeau correspondant au pays"""
    country = country.upper()
    
    flag_mapping = {
        "ANGLETERRE": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "ENGLAND": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
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

def display_leagues_with_matches(all_matches, selected_date):
    """Affiche les ligues avec des matchs pour la date sélectionnée"""
    # Récupérer les ligues disponibles
    leagues = load_available_leagues()
    
    # Regrouper les matchs par ligue pour la date sélectionnée
    leagues_with_matches = {}
    
    for match in all_matches:
        try:
            match_date = datetime.fromisoformat(match['date'].replace('Z', '+00:00')).date()
            
            # Si le match est à la date sélectionnée
            if match_date == selected_date:
                league_id = match.get('league_id', 0)
                if league_id not in leagues_with_matches:
                    # Trouver les détails de la ligue
                    league_info = next((l for l in leagues if l.get('id') == league_id), 
                                     {"id": league_id, "name": f"Ligue {league_id}", "country": "Inconnu"})
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
            logger.error(f"Erreur lors du traitement du match: {e}")
    
    # Diviser en compétitions favorites et autres compétitions
    favorite_leagues = [39, 140, 61, 78, 135, 2]  # Les IDs des ligues majeures: EPL, Liga, etc.
    
    # Afficher les compétitions favorites
    st.markdown('<div class="header-section">COMPÉTITIONS FAVORITES</div>', unsafe_allow_html=True)
    
    has_favorite = False
    for league_id in favorite_leagues:
        if league_id in leagues_with_matches:
            has_favorite = True
            league_data = leagues_with_matches[league_id]
            display_league_item(league_data)
    
    if not has_favorite:
        st.info("Pas de matchs dans vos compétitions favorites aujourd'hui")
    
    # Afficher les autres compétitions
    st.markdown('<div class="header-section">AUTRES COMPÉTITIONS [A-Z]</div>', unsafe_allow_html=True)
    
    other_leagues = [lid for lid in leagues_with_matches if lid not in favorite_leagues]
    
    if not other_leagues:
        st.info("Pas d'autres matchs disponibles aujourd'hui")
    else:
        for league_id in other_leagues:
            league_data = leagues_with_matches[league_id]
            display_league_item(league_data)
    
    return leagues_with_matches

def display_league_item(league_data):
    """Affiche un élément de ligue avec son drapeau et le nombre de matchs"""
    league_info = league_data["info"]
    matches_count = len(league_data["matches"])
    league_id = league_info.get("id", 0)
    
    # Déterminer le drapeau basé sur le pays
    country = league_info.get("country", "").upper()
    flag_emoji = get_country_flag_emoji(country)
    
    # Créer une clé unique pour le bouton
    league_key = f"league_{league_id}"
    
    # Afficher la ligue avec son drapeau et le nombre de matchs
    league_html = f"""
    <div class="league-item" onclick="console.log('Clicked: {league_key}')">
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
    
    # Créer un bouton déguisé en HTML
    if st.markdown(league_html, unsafe_allow_html=True):
        return league_id
    
    return None

def display_match_list(matches):
    """Affiche une liste de matchs au style mobile"""
    st.markdown('<div class="match-list">', unsafe_allow_html=True)
    
    for match in matches:
        time_str = match.get('time', '??:??')
        if isinstance(match.get('date'), str) and 'T' in match['date']:
            try:
                match_dt = datetime.fromisoformat(match['date'].replace('Z', '+00:00'))
                time_str = match_dt.strftime('%H:%M')
            except:
                pass
        
        match_html = f"""
        <div class="match-item">
            <div class="team-home">{match['home_team']}</div>
            <div class="match-time">{time_str}</div>
            <div class="team-away">{match['away_team']}</div>
        </div>
        """
        st.markdown(match_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_mobile_interface():
    """
    Affiche l'interface principale style mobile
    """
    # Charger le CSS personnalisé
    load_custom_css()
    
    # En-tête avec logo et titre
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <span style="font-size: 32px; margin-right: 10px;">⚽</span>
            <h1 style="margin: 0;">Football</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Générer le sélecteur de dates
    selected_date = generate_date_selector()
    
    # Récupérer tous les matchs à venir pour les 7 prochains jours
    try:
        all_upcoming_matches = get_upcoming_matches(days_ahead=7)
    except Exception as e:
        st.error(f"Erreur lors de la récupération des matchs: {e}")
        st.info("Génération de données de démonstration...")
        # Générer des matchs de démo en cas d'erreur
        all_upcoming_matches = generate_demo_matches(days=7)
    
    # Afficher les ligues avec des matchs
    leagues_with_matches = display_leagues_with_matches(all_upcoming_matches, selected_date)
    
    # Si l'utilisateur clique sur une ligue, afficher les matchs de cette ligue
    if 'selected_league_id' in st.session_state:
        league_id = st.session_state['selected_league_id']
        if league_id in leagues_with_matches:
            st.subheader(f"Matchs - {leagues_with_matches[league_id]['info']['name']}")
            display_match_list(leagues_with_matches[league_id]['matches'])

def generate_demo_matches(days=7):
    """Génère des matchs de démonstration en cas d'erreur de l'API"""
    matches = []
    leagues = [
        {"id": 39, "name": "Premier League", "country": "Angleterre"},
        {"id": 140, "name": "La Liga", "country": "Espagne"},
        {"id": 61, "name": "Ligue 1", "country": "France"},
        {"id": 78, "name": "Bundesliga", "country": "Allemagne"},
        {"id": 135, "name": "Serie A", "country": "Italie"},
        {"id": 2, "name": "Champions League", "country": "Europe"},
        {"id": 233, "name": "Premiership", "country": "Afrique du Sud"},
        {"id": 262, "name": "Saudi Pro League", "country": "Arabie Saoudite"}
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
                # Sélectionner deux équipes différentes de cette ligue
                teams = random.sample(teams_by_league[league_id], 2)
                home_team, away_team = teams[0], teams[1]
                
                # Créer un nouveau match
                match_hour = random.randint(12, 21)
                match_minute = random.choice([0, 15, 30, 45])
                match_datetime = current_date.replace(hour=match_hour, minute=match_minute)
                
                # Sélectionner un stade pour ce match
                venue = random.choice(venues.get(league_id, ["Stade Municipal"]))
                
                match = {
                    "id": f"{day}_{league_id}_{hash(home_team+away_team) % 1000}",
                    "league_id": league_id,
                    "league": {"id": league_id, "name": league["name"]},
                    "league_name": league["name"],
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

def main():
    """Point d'entrée principal"""
    st.set_page_config(
        page_title="Football ⚽ Prédictions",
        page_icon="⚽",
        layout="mobile"
    )
    
    display_mobile_interface()

if __name__ == "__main__":
    main()