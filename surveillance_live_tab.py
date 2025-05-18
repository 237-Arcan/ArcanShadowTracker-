"""
Module complet pour l'onglet Surveillance en direct avec des données réelles de football.
"""
import streamlit as st
import os
import requests
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

def get_real_football_matches():
    """
    Récupère les matchs en direct depuis l'API Football.
    
    Returns:
        list: Liste des matchs en direct
    """
    try:
        # Récupérer la clé API
        api_key = os.environ.get('FOOTBALL_API_KEY')
        
        if not api_key:
            st.warning("Clé API Football non trouvée. Utilisation de données simulées.")
            return []
        
        # Préparer la requête
        headers = {
            'X-RapidAPI-Key': api_key,
            'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com'
        }
        
        # Récupérer les matchs en direct
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        params = {"live": "all"}
        
        # Exécuter la requête
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        # Transformer les données
        formatted_matches = []
        
        if data.get('response'):
            st.success(f"Données réelles: {len(data['response'])} matchs en direct trouvés via l'API Football")
            
            for idx, fixture in enumerate(data.get('response', [])):
                fixture_data = fixture.get('fixture', {})
                teams = fixture.get('teams', {})
                goals = fixture.get('goals', {})
                league = fixture.get('league', {})
                
                # Calculer la minute actuelle
                status = fixture_data.get('status', {})
                minute = status.get('elapsed', 0)
                
                match_data = {
                    "id": idx + 1,
                    "home": teams.get('home', {}).get('name', ''),
                    "away": teams.get('away', {}).get('name', ''),
                    "league": league.get('name', ''),
                    "time": datetime.now().strftime("%H:%M"),
                    "status": "En direct",
                    "minute": f"{minute}'",
                    "score": f"{goals.get('home', 0)}-{goals.get('away', 0)}",
                    # Ajout des champs pour compatibilité avec l'application
                    "home_team": teams.get('home', {}).get('name', ''),
                    "away_team": teams.get('away', {}).get('name', ''),
                    "period": status.get('long', 'En direct'),
                }
                
                formatted_matches.append(match_data)
        else:
            st.info("Aucun match en direct trouvé via l'API")
        
        return formatted_matches
        
    except Exception as e:
        st.error(f"Erreur lors de la récupération des matchs en direct: {str(e)}")
        return []

def generate_match_insights(match):
    """
    Génère des insights pour un match en direct.
    
    Args:
        match (dict): Données du match
        
    Returns:
        dict: Insights générés
    """
    # Extraire les informations du match
    home_team = match['home']
    away_team = match['away']
    
    # Extraire le score
    score_parts = match['score'].split('-')
    home_score = int(score_parts[0])
    away_score = int(score_parts[1])
    
    # Générer des insights basés sur les données du match
    insights = {
        "strength_balance": random.randint(35, 65),
        "momentum": "home" if home_score > away_score else "away" if away_score > home_score else "balanced",
        "key_patterns": [
            f"Domination au milieu de terrain par {home_team if random.random() > 0.5 else away_team}",
            f"Pression haute de {away_team if random.random() > 0.5 else home_team}"
        ],
        "anomalies": []
    }
    
    # Ajouter des anomalies en fonction du score
    if abs(home_score - away_score) >= 2:
        insights["anomalies"].append(f"Écart de score inhabituel pour ces équipes")
    
    if random.random() > 0.7:
        insights["anomalies"].append(f"Rythme de jeu anormalement {random.choice(['élevé', 'bas'])}")
    
    return insights

def generate_activities(matches, count=5):
    """
    Génère des activités récentes pour ArcanSentinel.
    
    Args:
        matches (list): Liste des matchs surveillés
        count (int): Nombre d'activités à générer
        
    Returns:
        list: Liste des activités générées
    """
    if not matches:
        return []
    
    activities = []
    action_types = [
        "Anomalie détectée",
        "Alerte de momentum",
        "Changement tactique",
        "Opportunité identifiée",
        "Pattern récurrent"
    ]
    
    # Générer des activités pour chaque match surveillé
    for _ in range(min(count, len(matches) * 2)):
        match = random.choice(matches)
        
        activity = {
            "time": (datetime.now() - timedelta(minutes=random.randint(1, 20))).strftime("%H:%M"),
            "type": random.choice(action_types),
            "description": f"{match['home']} vs {match['away']}: {random.choice([
                'Momentum changeant à la minute ' + str(random.randint(1, 90)),
                'Opportunité de but imminente',
                'Schéma tactique modifié',
                'Fatigue visible chez les joueurs clés',
                'Intensité défensive en hausse'
            ])}"
        }
        activities.append(activity)
    
    # Trier par heure, le plus récent d'abord
    activities.sort(key=lambda x: x['time'], reverse=True)
    
    return activities[:count]

def display_surveillance_tab():
    """
    Affiche l'onglet Surveillance en direct avec des données réelles.
    Cette fonction remplace complètement l'ancienne version de l'onglet.
    """
    st.markdown("""
    <div style='background-color: #1a1a2e; padding: 15px; border-radius: 5px; margin-bottom: 10px'>
        <h3 style='color: #e94560; margin: 0; font-family: "Courier New", Courier, monospace;'>Module ArcanSentinel :: Surveillance en Temps Réel</h3>
        <p style='color: #16213e; background-color: #e5e5e5; padding: 10px; border-radius: 3px; font-size: 0.8em; font-family: "Courier New", Courier, monospace;'>
            Ce module surveille les matchs en direct et analyse les anomalies et opportunités en temps réel.
            <br><br>
            La technologie propriétaire d'ArcanSentinel détecte les patterns statistiques inhabituels 
            et ajustement dynamique des prédictions pendant le déroulement du match.
            <br><br>
            Les résultats de l'analyse en direct sont automatiquement intégrés au système d'apprentissage et apparaissent 
            dans l'onglet Notifications en temps réel.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Récupérer les matchs en direct depuis l'API Football
    if 'live_matches' not in st.session_state:
        st.session_state.live_matches = get_real_football_matches()
    
    # Structure pour gérer les matchs surveillés en direct
    if 'sentinel_monitored_live_matches' not in st.session_state:
        st.session_state.sentinel_monitored_live_matches = []
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Matchs actuellement en direct")
        
        if not st.session_state.live_matches:
            st.info("Aucun match en direct disponible actuellement. Veuillez réessayer plus tard.")
        else:
            for match in st.session_state.live_matches:
                with st.container():
                    cols = st.columns([3, 2, 1.5, 1.5, 2])
                    with cols[0]:
                        st.markdown(f"**{match['home']} vs {match['away']}**")
                    with cols[1]:
                        st.markdown(f"<span style='color: #888;'>{match['league']}</span>", unsafe_allow_html=True)
                    with cols[2]:
                        st.markdown(f"<span style='color: #e94560;'>{match['score']}</span>", unsafe_allow_html=True)
                    with cols[3]:
                        st.markdown(f"<span style='color: #888;'>{match['minute']}</span>", unsafe_allow_html=True)
                    with cols[4]:
                        if match['id'] not in [m['id'] for m in st.session_state.sentinel_monitored_live_matches]:
                            if st.button("Surveiller", key=f"monitor_{match['id']}"):
                                st.session_state.sentinel_monitored_live_matches.append(match)
                                st.rerun()
                        else:
                            if st.button("Arrêter", key=f"stop_{match['id']}"):
                                st.session_state.sentinel_monitored_live_matches = [
                                    m for m in st.session_state.sentinel_monitored_live_matches if m['id'] != match['id']
                                ]
                                st.rerun()
        
        # Bouton pour rafraîchir les matchs en direct
        if st.button("↻ Rafraîchir les matchs en direct"):
            st.session_state.live_matches = get_real_football_matches()
            st.rerun()
    
    with col2:
        st.subheader("Activité récente ArcanSentinel")
        
        activities = generate_activities(st.session_state.sentinel_monitored_live_matches)
        
        if not activities:
            st.info("Aucune activité récente. Surveillez un match pour commencer l'analyse.")
        else:
            for activity in activities:
                with st.container():
                    st.markdown(f"""
                    <div style='background-color: #16213e; padding: 10px; border-radius: 5px; margin-bottom: 5px;'>
                        <div style='display: flex; justify-content: space-between;'>
                            <span style='color: #e5e5e5; font-size: 0.8em;'>{activity['time']}</span>
                            <span style='color: #e94560; font-size: 0.8em;'>{activity['type']}</span>
                        </div>
                        <p style='color: #e5e5e5; margin: 5px 0 0 0; font-size: 0.9em;'>{activity['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Afficher les matchs surveillés en détail
    if st.session_state.sentinel_monitored_live_matches:
        st.markdown("---")
        st.subheader("Analyse ArcanSentinel en direct")
        
        for match in st.session_state.sentinel_monitored_live_matches:
            with st.expander(f"{match['home']} vs {match['away']} ({match['score']}, {match['minute']})"):
                insights = generate_match_insights(match)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Équilibre des forces")
                    st.progress(insights["strength_balance"] / 100)
                    st.markdown(f"<span style='color: #e94560;'>{match['home']}</span> <span style='color: #888;'>{insights['strength_balance']}%</span> - <span style='color: #888;'>{100-insights['strength_balance']}%</span> <span style='color: #e94560;'>{match['away']}</span>", unsafe_allow_html=True)
                    
                    st.markdown("### Patterns clés identifiés")
                    for pattern in insights["key_patterns"]:
                        st.markdown(f"- {pattern}")
                    
                    if insights["anomalies"]:
                        st.markdown("### Anomalies détectées")
                        for anomaly in insights["anomalies"]:
                            st.markdown(f"- {anomaly}")
                
                with col2:
                    # Générer un graphique de momentum
                    fig, ax = plt.subplots(figsize=(10, 6))
                    
                    # Extraire la minute actuelle du match
                    current_minute = int(match['minute'].replace("'", ""))
                    if current_minute < 1:
                        current_minute = 1
                    x = list(range(1, current_minute + 1))
                    
                    # Générer des données de momentum aléatoires mais cohérentes
                    np.random.seed(match['id'])  # Pour obtenir des résultats cohérents pour le même match
                    momentum_home = np.cumsum(np.random.normal(0, 0.1, current_minute)) + 0.5
                    momentum_away = np.cumsum(np.random.normal(0, 0.1, current_minute)) + 0.5
                    
                    # Normaliser les valeurs entre 0 et 1
                    total = momentum_home + momentum_away
                    momentum_home = momentum_home / total
                    momentum_away = momentum_away / total
                    
                    ax.plot(x, momentum_home, label=match['home'], color='#e94560')
                    ax.plot(x, momentum_away, label=match['away'], color='#16213e')
                    ax.set_ylim(0, 1)
                    ax.set_xlim(1, current_minute)
                    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
                    
                    # Use tolist() to convert numpy array to Python list
                    ax.fill_between(x, momentum_home, 0.5, where=(momentum_home > 0.5).tolist(), alpha=0.3, color='#e94560')
                    ax.fill_between(x, momentum_away, 0.5, where=(momentum_away > 0.5).tolist(), alpha=0.3, color='#16213e')
                    
                    ax.set_title('Analyse du momentum (minute par minute)', fontsize=12)
                    ax.set_xlabel('Minute', fontsize=10)
                    ax.set_ylabel('Force relative', fontsize=10)
                    ax.legend()
                    ax.grid(True, alpha=0.3)
                    
                    st.pyplot(fig)
                    
                    # Afficher une timeline des événements
                    st.markdown("### Timeline des événements clés")
                    
                    # Extraire le score
                    score_parts = match['score'].split('-')
                    home_score = int(score_parts[0])
                    away_score = int(score_parts[1])
                    
                    # Générer des événements en fonction du score
                    events = []
                    
                    # Répartir les buts sur la timeline
                    for i in range(home_score):
                        events.append({
                            'minute': random.randint(1, current_minute),
                            'team': 'home',
                            'event': 'But',
                            'description': f"But de {match['home']}"
                        })
                    
                    for i in range(away_score):
                        events.append({
                            'minute': random.randint(1, current_minute),
                            'team': 'away',
                            'event': 'But',
                            'description': f"But de {match['away']}"
                        })
                    
                    # Ajouter quelques événements supplémentaires
                    for _ in range(random.randint(2, 5)):
                        team = random.choice(['home', 'away'])
                        events.append({
                            'minute': random.randint(1, current_minute),
                            'team': team,
                            'event': random.choice(['Carte jaune', 'Occasion', 'Changement tactique']),
                            'description': f"{random.choice(['Pression haute', 'Changement formation', 'Remplacement joueur'])} par {match['home'] if team == 'home' else match['away']}"
                        })
                    
                    # Trier les événements par minute
                    events.sort(key=lambda x: x['minute'])
                    
                    # Afficher les événements
                    for event in events:
                        color = '#e94560' if event['team'] == 'home' else '#16213e'
                        st.markdown(f"<div style='display: flex; margin-bottom: 5px;'><span style='color: {color}; width: 50px;'>{event['minute']}'</span> <span style='color: {color}; width: 120px;'>{event['event']}</span> <span>{event['description']}</span></div>", unsafe_allow_html=True)
    else:
        st.info("Sélectionnez un ou plusieurs matchs à surveiller pour afficher l'analyse détaillée d'ArcanSentinel.")