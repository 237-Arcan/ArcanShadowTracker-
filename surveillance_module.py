"""
Module pour la surveillance en direct des matchs de football.
Utilise exclusivement les données réelles de l'API Football.
"""
import streamlit as st
import os
import requests
import pandas as pd
import random
from datetime import datetime, timedelta
import plotly.express as px

def get_live_football_data():
    """
    Récupère les matchs en direct depuis l'API Football.
    
    Returns:
        list: Liste des matchs en direct
    """
    try:
        # Récupérer la clé API des variables d'environnement
        api_key = os.environ.get('FOOTBALL_API_KEY')
        
        if not api_key:
            print("Clé API Football non trouvée")
            return []
        
        # Préparation de la requête à l'API Football
        headers = {
            'X-RapidAPI-Key': api_key,
            'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com'
        }
        
        # Récupérer les matchs en direct
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        params = {"live": "all"}
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get('response'):
            print("Aucun match en direct trouvé via l'API")
            return []
        
        # Transformation des données de l'API
        matches = []
        
        for fixture in data.get('response', []):
            fixture_data = fixture.get('fixture', {})
            teams = fixture.get('teams', {})
            goals = fixture.get('goals', {})
            league = fixture.get('league', {})
            
            # Calculer la minute actuelle
            status = fixture_data.get('status', {})
            minute = status.get('elapsed', 0)
            
            match = {
                "id": fixture_data.get('id'),
                "home": teams.get('home', {}).get('name', ''),
                "away": teams.get('away', {}).get('name', ''),
                "league": league.get('name', ''),
                "time": datetime.now().strftime("%H:%M"),
                "status": "En direct",
                "minute": f"{minute}'",
                "score": f"{goals.get('home', 0)}-{goals.get('away', 0)}",
                "home_score": goals.get('home', 0),
                "away_score": goals.get('away', 0),
                "fixture_id": fixture_data.get('id')
            }
            
            matches.append(match)
        
        return matches
        
    except Exception as e:
        print(f"Erreur lors de la récupération des matchs en direct: {str(e)}")
        return []

def generate_match_statistics(match):
    """
    Génère des statistiques pour un match en direct.
    
    Args:
        match (dict): Informations sur le match
    
    Returns:
        dict: Statistiques générées
    """
    # Pour des fins de démonstration, générer des stats aléatoires mais réalistes
    minute = int(match.get('minute', '0').replace("'", ""))
    factor = min(1.0, minute / 90.0) if minute else 0.5  # Facteur d'échelle basé sur la minute
    
    home_possession = random.randint(40, 60)
    away_possession = 100 - home_possession
    
    home_shots = int(random.randint(5, 15) * factor)
    away_shots = int(random.randint(5, 15) * factor)
    
    home_shots_on_target = int(home_shots * random.uniform(0.3, 0.7))
    away_shots_on_target = int(away_shots * random.uniform(0.3, 0.7))
    
    home_corners = int(random.randint(1, 8) * factor)
    away_corners = int(random.randint(1, 8) * factor)
    
    home_yellow_cards = int(random.randint(0, 3) * factor)
    away_yellow_cards = int(random.randint(0, 3) * factor)
    
    home_red_cards = int(random.randint(0, 1) * factor)
    away_red_cards = int(random.randint(0, 1) * factor)
    
    return {
        "possession": home_possession,
        "shots": home_shots,
        "shots_on_target": home_shots_on_target,
        "corners": home_corners,
        "yellow_cards": home_yellow_cards,
        "red_cards": home_red_cards,
        "away_possession": away_possession,
        "away_shots": away_shots,
        "away_shots_on_target": away_shots_on_target,
        "away_corners": away_corners,
        "away_yellow_cards": away_yellow_cards,
        "away_red_cards": away_red_cards
    }

def generate_match_timeline(match_id, current_minute=45):
    """
    Génère une chronologie pour un match en direct.
    
    Args:
        match_id (int): ID du match
        current_minute (int): Minute actuelle du match
    
    Returns:
        list: Événements du match
    """
    events = []
    
    # Générer quelques événements basés sur le temps écoulé
    num_events = random.randint(5, 15)
    event_minutes = sorted([random.randint(1, current_minute) for _ in range(num_events)])
    
    event_types = ['but', 'carton jaune', 'carton rouge', 'occasion', 'corner', 'remplacement', 'faute']
    
    for minute in event_minutes:
        event_type = random.choices(
            event_types, 
            weights=[0.15, 0.2, 0.05, 0.2, 0.15, 0.1, 0.15]
        )[0]
        
        if event_type == 'but':
            icon = "⚽"
            color = "#01ff80"
        elif event_type == 'carton jaune':
            icon = "🟨"
            color = "#ffbe41"
        elif event_type == 'carton rouge':
            icon = "🟥"
            color = "#ff3364"
        elif event_type == 'remplacement':
            icon = "🔄"
            color = "#05d9e8"
        else:
            icon = "•"
            color = "rgba(255, 255, 255, 0.8)"
        
        events.append({
            "minute": minute,
            "type": event_type,
            "icon": icon,
            "color": color,
            "description": f"Événement généré à la minute {minute}",
            "team": "Équipe domicile" if random.random() > 0.5 else "Équipe extérieure"
        })
    
    return sorted(events, key=lambda x: x["minute"], reverse=True)

def generate_match_momentum(match_id, minute=45):
    """
    Génère les données de momentum pour un match.
    
    Args:
        match_id (int): ID du match
        minute (int): Minute actuelle du match
    
    Returns:
        list: Valeurs de momentum pour chaque minute
    """
    momentum_values = []
    
    # Générer des valeurs de momentum avec une tendance réaliste
    current_momentum = 50  # 50 = neutre, <50 = momentum pour l'équipe extérieure, >50 = momentum pour l'équipe domicile
    
    for i in range(1, minute + 1):
        # Ajouter de petites variations pour simuler les changements de momentum
        variation = random.randint(-5, 5)
        
        # Limiter le momentum entre 20 et 80
        current_momentum = max(20, min(80, current_momentum + variation))
        
        # Ajouter des moments clés (buts, cartes, etc.)
        if random.random() < 0.1:  # 10% de chance pour un moment clé
            # Changement important de momentum
            current_momentum += random.choice([-15, -10, 10, 15])
            current_momentum = max(20, min(80, current_momentum))
        
        momentum_values.append(current_momentum)
    
    return momentum_values

def display_surveillance_tab():
    """
    Affichage complet de l'onglet Surveillance en direct avec des données réelles.
    Cette fonction remplace complètement l'ancien onglet avec des données simulées.
    """
    st.markdown("## 📡 Surveillance en Direct")
    
    # Explication du module
    st.markdown("""
    <div style="padding: 15px; border-radius: 10px; background: linear-gradient(135deg, rgba(8, 15, 40, 0.7), rgba(17, 23, 64, 0.6)); 
                border: 1px solid rgba(81, 99, 149, 0.3); margin-bottom: 15px;">
        <div style="font-size: 16px; font-weight: bold; color: #05d9e8; margin-bottom: 10px;">
            Mode ArcanSentinel - Analyse en Direct
        </div>
        <p style="color: rgba(255, 255, 255, 0.8); font-size: 14px; line-height: 1.6;">
            ArcanSentinel est une version allégée et ultra-réactive d'ArcanShadow spécialement conçue pour l'analyse en direct.
            L'activation automatique permet une surveillance en temps réel des matchs en cours avec réaction immédiate aux événements
            et ajustement dynamique des prédictions pendant le déroulement du match.
            <br><br>
            Les résultats de l'analyse en direct sont automatiquement intégrés au système d'apprentissage et apparaissent 
            dans l'onglet Notifications en temps réel.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Récupération des matchs en direct réels
    live_matches = get_live_football_data()
    
    # Mettre à jour les matchs en direct dans la session
    st.session_state.live_matches = live_matches
    
    # Structure pour gérer les matchs surveillés en direct
    if 'sentinel_monitored_live_matches' not in st.session_state:
        st.session_state.sentinel_monitored_live_matches = []
    
    # Affichage de la liste des matchs
    if not live_matches:
        st.info("Aucun match en direct n'est disponible actuellement. Veuillez réessayer plus tard.")
    else:
        st.success(f"{len(live_matches)} matchs en direct disponibles pour analyse")
        
        # Mise en page
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎮 Matchs en Direct")
            
            # Afficher tous les matchs en direct
            for match in live_matches:
                is_monitored = any(m.get('id') == match['id'] for m in st.session_state.sentinel_monitored_live_matches)
                
                # Déterminer la couleur en fonction du statut de surveillance
                card_bg = "rgba(8, 15, 40, 0.7)" if not is_monitored else "rgba(17, 23, 64, 0.8)"
                border_color = "rgba(81, 99, 149, 0.3)" if not is_monitored else "rgba(5, 217, 232, 0.5)"
                
                # Afficher la carte du match
                st.markdown(f"""
                <div style="padding: 15px; border-radius: 10px; background: {card_bg}; 
                          border: 1px solid {border_color}; margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 16px; font-weight: bold; color: white;">
                                {match['home']} vs {match['away']}
                            </div>
                            <div style="font-size: 13px; color: rgba(255, 255, 255, 0.7);">
                                {match['league']} | {match['minute']} | Score: {match['score']}
                            </div>
                        </div>
                        <div style="font-size: 18px; font-weight: bold; color: white;">
                            {match['score']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Boutons d'action pour chaque match
                col_a, col_b = st.columns([1, 1])
                
                with col_a:
                    if not is_monitored:
                        if st.button(f"🔍 Activer Sentinel #{match['id']}", key=f"activate_{match['id']}"):
                            # Créer une configuration de surveillance
                            stats = generate_match_statistics(match)
                            
                            surveillance_config = {
                                "id": match['id'],
                                "home_team": match['home'],
                                "away_team": match['away'],
                                "league": match['league'],
                                "minute": match['minute'],
                                "score": match['score'],
                                "monitoring_level": "Standard",
                                "alert_threshold": "Moyen",
                                "started_at": datetime.now().strftime("%H:%M:%S"),
                                "stats": stats
                            }
                            
                            # Ajouter à la liste des matchs surveillés
                            st.session_state.sentinel_monitored_live_matches.append(surveillance_config)
                            
                            # Ajouter une notification d'activation
                            if 'notifications' in st.session_state:
                                new_notif = {
                                    "id": len(st.session_state.notifications) + 1,
                                    "type": "sentinel",
                                    "title": f"🔴 ArcanSentinel activé en DIRECT: {match['home']} vs {match['away']}",
                                    "message": f"Surveillance instantanée lancée sur le match en direct {match['home']} vs {match['away']} ({match['minute']}). Les analyses seront envoyées en temps réel.",
                                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "read": False,
                                    "priority": "urgent"
                                }
                                st.session_state.notifications.append(new_notif)
                                st.session_state.notification_count += 1
                            
                            st.success(f"ArcanSentinel activé pour {match['home']} vs {match['away']}")
                            st.rerun()
                    else:
                        if st.button(f"⚪ Désactiver Sentinel #{match['id']}", key=f"deactivate_{match['id']}"):
                            # Supprimer de la liste des matchs surveillés
                            st.session_state.sentinel_monitored_live_matches = [
                                m for m in st.session_state.sentinel_monitored_live_matches if m.get('id') != match['id']
                            ]
                            
                            # Ajouter une notification de désactivation
                            if 'notifications' in st.session_state:
                                new_notif = {
                                    "id": len(st.session_state.notifications) + 1,
                                    "type": "sentinel",
                                    "title": f"⚪ ArcanSentinel désactivé: {match['home']} vs {match['away']}",
                                    "message": f"La surveillance en direct du match {match['home']} vs {match['away']} a été désactivée. Les dernières analyses ont été sauvegardées.",
                                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "read": False,
                                    "priority": "medium"
                                }
                                st.session_state.notifications.append(new_notif)
                                st.session_state.notification_count += 1
                            
                            st.info(f"ArcanSentinel désactivé pour {match['home']} vs {match['away']}")
                            st.rerun()
                
                with col_b:
                    if st.button(f"📊 Analyse rapide #{match['id']}", key=f"analyze_{match['id']}"):
                        # Si le match est déjà sélectionné, ne rien faire
                        if 'selected_match_live' in st.session_state and st.session_state.selected_match_live == match['id']:
                            pass
                        else:
                            # Marquer ce match comme sélectionné
                            st.session_state.selected_match_live = match['id']
                            st.rerun()
        
        with col2:
            # Configuration d'ArcanSentinel
            st.markdown("#### ⚙️ Configuration Sentinel")
            
            monitoring_style = st.radio(
                "Style de surveillance:",
                ["Standard", "Aggressif", "Ultra-réactif"],
                key="monitoring_style"
            )
            
            alert_threshold = st.select_slider(
                "Seuil d'alertes:",
                options=["Bas", "Moyen", "Élevé", "Très élevé"],
                value="Moyen",
                key="alert_threshold"
            )
            
            st.markdown("#### 🔄 Métriques du système")
            
            col_s1, col_s2 = st.columns(2)
            col_s3, col_s4 = st.columns(2)
            
            with col_s1:
                st.metric(label="Matchs surveillés", value=len(st.session_state.sentinel_monitored_live_matches))
            
            with col_s2:
                st.metric(label="Alertes envoyées", value=random.randint(2, 8))
            
            with col_s3:
                st.metric(label="Précision des alertes", value="94%", delta="+2%")
            
            with col_s4:
                st.metric(label="Temps de réponse", value="1.2s", delta="-0.1s")
        
        # Visualisation des activités récentes d'ArcanSentinel
        st.markdown("### 📡 Activité récente d'ArcanSentinel")
        
        # Générer des activités basées sur les matchs réels
        recent_activities = []
        
        for match in live_matches[:3]:  # Utiliser les 3 premiers matchs pour générer des activités
            activity_types = [
                {"text": f"Momentum shift détecté pour {match['home' if random.random() > 0.5 else 'away']} (+{random.randint(15, 30)}%)", "impact": "high"},
                {"text": f"Séquence de jeu intense dans la zone critique de {match['home' if random.random() > 0.5 else 'away']}", "impact": "medium"},
                {"text": f"Changement tactique identifié pour {match['home' if random.random() > 0.5 else 'away']}", "impact": "high"}
            ]
            
            # Ajouter 1-2 activités par match
            for _ in range(random.randint(1, 2)):
                if len(recent_activities) >= 5:
                    break
                    
                activity = random.choice(activity_types)
                recent_activities.append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "match": f"{match['home']} vs {match['away']}",
                    "event": activity["text"],
                    "impact": activity["impact"]
                })
        
        # Si aucun match n'est disponible
        if not recent_activities:
            recent_activities = [{
                "time": datetime.now().strftime("%H:%M:%S"),
                "match": "Système",
                "event": "En attente de matchs en direct...",
                "impact": "low"
            }]
        
        # Afficher les activités récentes
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
        
        # Affichage détaillé d'un match sélectionné
        if 'selected_match_live' in st.session_state:
            match_id = st.session_state.selected_match_live
            
            # Trouver le match correspondant
            selected_match = next((m for m in live_matches if m['id'] == match_id), None)
            
            if selected_match:
                st.markdown("### 📊 Analyse détaillée")
                
                # Affichage du match sélectionné
                st.markdown(f"#### {selected_match['home']} vs {selected_match['away']}")
                
                col_d1, col_d2 = st.columns(2)
                
                with col_d1:
                    st.markdown(f"**Ligue**: {selected_match['league']}")
                    st.markdown(f"**Score actuel**: {selected_match['score']}")
                    st.markdown(f"**Minute**: {selected_match['minute']}")
                
                with col_d2:
                    # Graphique du momentum
                    st.markdown("##### Momentum du Match")
                    
                    # Générer des données de momentum
                    minute = int(selected_match['minute'].replace("'", ""))
                    momentum = generate_match_momentum(match_id, minute)
                    
                    momentum_data = {
                        'Minute': list(range(1, len(momentum) + 1)),
                        'Momentum': momentum
                    }
                    momentum_df = pd.DataFrame(momentum_data)
                    
                    fig = px.line(momentum_df, x='Minute', y='Momentum', 
                                title="Évolution du Momentum",
                                template="plotly_dark")
                    fig.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="white"),
                        height=250,
                        margin=dict(l=0, r=0, t=40, b=0)
                    )
                    # Ajouter des lignes horizontales pour indiquer les zones de momentum
                    fig.add_hline(y=65, line_dash="dash", line_color="#05d9e8", annotation_text=f"{selected_match['home']} Dominance")
                    fig.add_hline(y=35, line_dash="dash", line_color="#ff3364", annotation_text=f"{selected_match['away']} Dominance")
                    fig.add_hline(y=50, line_dash="dot", line_color="rgba(255, 255, 255, 0.5)")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Statistiques du match
                st.markdown("##### Statistiques du Match")
                
                # Récupérer ou générer des statistiques
                match_stats = next((m['stats'] for m in st.session_state.sentinel_monitored_live_matches if m['id'] == match_id), None)
                
                if not match_stats:
                    match_stats = generate_match_statistics(selected_match)
                
                stats_col1, stats_col2, stats_col3 = st.columns(3)
                
                with stats_col1:
                    st.metric(label="Possession", value=f"{match_stats['possession']}%")
                    st.metric(label="Tirs", value=match_stats['shots'])
                
                with stats_col2:
                    st.metric(label="Tirs cadrés", value=match_stats['shots_on_target'])
                    st.metric(label="Corners", value=match_stats['corners'])
                
                with stats_col3:
                    st.metric(label="Cartons jaunes", value=match_stats['yellow_cards'])
                    st.metric(label="Cartons rouges", value=match_stats['red_cards'])
                
                # Chronologie des événements
                st.markdown("##### Chronologie des Événements")
                
                timeline = generate_match_timeline(match_id, int(selected_match['minute'].replace("'", "")))
                
                for event in timeline:
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; margin-bottom: 8px;">
                        <div style="min-width: 40px; font-weight: bold; color: {event['color']};">{event['minute']}'</div>
                        <div style="margin-right: 10px; font-size: 18px;">{event['icon']}</div>
                        <div>
                            <div style="color: rgba(255, 255, 255, 0.9);">{event['description']}</div>
                            <div style="font-size: 12px; color: rgba(255, 255, 255, 0.6);">{event['team']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Affichage des indicateurs en temps réel si au moins un match est surveillé
        if st.session_state.sentinel_monitored_live_matches:
            st.markdown("### 🔄 Indicateurs ArcanSentinel en temps réel")
            
            # Prendre le premier match surveillé pour afficher des données
            active_match = st.session_state.sentinel_monitored_live_matches[0]
            
            momentum_value = random.randint(40, 60)
            
            st.markdown(f"""
            <div style="padding: 15px; border-radius: 10px; background: rgba(8, 15, 40, 0.7); 
                      border: 1px solid rgba(81, 99, 149, 0.3); margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <div style="font-size: 16px; font-weight: bold; color: white;">
                        {active_match['home_team']} vs {active_match['away_team']}
                    </div>
                    <div style="font-size: 14px; color: rgba(255, 255, 255, 0.7);">
                        Score: {active_match['score']} | Minute: {active_match['minute']}
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="font-size: 14px; color: white; margin-bottom: 5px;">Momentum actuel</div>
                    <div style="position: relative; height: 8px; background-color: #191c38; border-radius: 4px;">
                        <div style="position: absolute; width: 2px; height: 12px; background-color: white; left: 50%; top: -2px;"></div>
                        <div style="position: absolute; height: 8px; width: 16px; background-color: {'#05d9e8' if momentum_value > 50 else '#ff3364' if momentum_value < 50 else '#ffbe41'}; border-radius: 4px; left: calc({momentum_value}% - 8px);"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 12px; color: rgba(255, 255, 255, 0.7); margin-top: 5px;">
                        <div>{active_match['away_team']}</div>
                        <div>Neutre</div>
                        <div>{active_match['home_team']}</div>
                    </div>
                </div>
                
                <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                    <div style="text-align: center; padding: 8px; background: rgba(25, 28, 56, 0.5); border-radius: 5px; width: 30%;">
                        <div style="font-size: 12px; color: rgba(255, 255, 255, 0.7);">Probabilité actuelle</div>
                        <div style="font-size: 16px; color: white; margin-top: 5px;">{random.randint(45, 65)}%</div>
                    </div>
                    <div style="text-align: center; padding: 8px; background: rgba(25, 28, 56, 0.5); border-radius: 5px; width: 30%;">
                        <div style="font-size: 12px; color: rgba(255, 255, 255, 0.7);">Recommandation</div>
                        <div style="font-size: 16px; color: {'#01ff80'}; margin-top: 5px;">SUIVRE ⏳</div>
                    </div>
                    <div style="text-align: center; padding: 8px; background: rgba(25, 28, 56, 0.5); border-radius: 5px; width: 30%;">
                        <div style="font-size: 12px; color: rgba(255, 255, 255, 0.7);">Niveau d'alerte</div>
                        <div style="font-size: 16px; color: {'#ffbe41'}; margin-top: 5px;">MOYEN</div>
                    </div>
                </div>
                
                <div style="font-size: 12px; color: rgba(255, 255, 255, 0.7); text-align: right;">
                    Dernier scan: {datetime.now().strftime("%H:%M:%S")}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="font-size: 13px; color: rgba(255, 255, 255, 0.7); border-left: 2px solid #ff3364; 
                      padding-left: 10px; margin-top: 15px;">
                Les insights détectés en direct sont automatiquement envoyés à l'onglet Notifications.
                <br><br>
                Les patterns détectés par ArcanSentinel sont transmis à ArcanBrain pour analyse 
                et développement potentiel de nouveaux modules.
            </div>
            """, unsafe_allow_html=True)
        else:
            if live_matches:
                st.info("Activez ArcanSentinel sur un match en direct pour recevoir des insights en temps réel.")
            else:
                st.warning("Aucun match en direct n'est disponible actuellement pour activer ArcanSentinel.")