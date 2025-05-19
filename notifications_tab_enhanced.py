"""
Module amélioré pour l'onglet Notifications d'ArcanShadow.
Ce module centralise toutes les notifications importantes du système,
en intégrant des alertes enrichies par de multiples sources de données.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importer notre hub d'intégration de données
from api.data_integration_hub import DataIntegrationHub

# Importer les composants améliorés
# Importer les composants améliorés
try:
    from modules.enhanced_components import get_enhanced_components
    enhanced_components = get_enhanced_components()
    
    # Récupération des composants améliorés
    ShadowOddsPlusEnhanced = enhanced_components.get_component('shadow_odds_plus')
    FanSentimentMonitorEnhanced = enhanced_components.get_component('fan_sentiment_monitor')
except ImportError:
    ShadowOddsPlusEnhanced = None
    FanSentimentMonitorEnhanced = None

def generate_enhanced_notifications(count=10):
    """
    Génère des notifications enrichies pour le système ArcanShadow
    en utilisant les données issues de multiples sources.
    
    Args:
        count (int): Nombre de notifications à générer
        
    Returns:
        list: Liste des notifications enrichies générées
    """
    # Initialisation du hub d'intégration de données
    data_hub = DataIntegrationHub()
    
    # Initialiser les composants améliorés si disponibles
    odds_analyzer = ShadowOddsPlusEnhanced if ShadowOddsPlusEnhanced else None
    sentiment_analyzer = FanSentimentMonitorEnhanced if FanSentimentMonitorEnhanced else None
    
    # Catégories de notifications
    categories = [
        "Alerte de cotes",
        "Événement important",
        "Opportunité détectée",
        "Mise à jour système",
        "Alerte de performance"
    ]
    
    # Ajouter des catégories liées aux modules améliorés s'ils sont disponibles
    if odds_analyzer:
        categories.append("Anomalie de cotes")
        categories.append("Mouvement suspect")
    
    if sentiment_analyzer:
        categories.append("Sentiment des fans")
        categories.append("Tendance social media")
    
    # Date actuelle
    now = datetime.now()
    
    # Génération des notifications
    notifications = []
    
    for i in range(count):
        # Date aléatoire dans les 7 derniers jours
        minutes_ago = random.randint(1, 10080)  # 7 jours en minutes
        notification_date = now - timedelta(minutes=minutes_ago)
        
        # Catégorie aléatoire
        category = random.choice(categories)
        
        # Priorité basée sur la catégorie et la récence
        if category in ["Anomalie de cotes", "Mouvement suspect", "Alerte de performance"]:
            priority = random.choice(["Haute", "Critique"])
        elif category in ["Opportunité détectée", "Événement important"]:
            priority = random.choice(["Moyenne", "Haute"])
        else:
            priority = random.choice(["Basse", "Moyenne"])
        
        # Contenu de la notification en fonction de la catégorie
        if category == "Alerte de cotes":
            teams = [
                random.choice(["Arsenal", "Chelsea", "Liverpool", "Man City", "Man United", "Tottenham"]),
                random.choice(["Leicester", "Everton", "West Ham", "Aston Villa", "Newcastle", "Wolves"])
            ]
            movement = random.choice(["chute", "hausse"])
            odds_change = round(random.uniform(0.2, 1.0), 2)
            
            content = f"Importante {movement} des cotes ({odds_change}) pour {teams[0]} vs {teams[1]}. Possible information non publique."
        
        elif category == "Anomalie de cotes":
            leagues = ["Premier League", "Ligue 1", "La Liga", "Bundesliga", "Serie A"]
            market_types = ["1X2", "Over/Under", "BTTS", "Handicap Asiatique"]
            
            league = random.choice(leagues)
            market = random.choice(market_types)
            confidence = round(random.uniform(0.65, 0.95), 2)
            
            if odds_analyzer:
                try:
                    # Utiliser l'API football_data pour obtenir les prochains matchs
                    from api.football_data import get_upcoming_matches
                    matches = get_upcoming_matches(days_ahead=1)
                except Exception as e:
                    st.warning(f"Impossible de récupérer les matchs à venir: {e}")
                    matches = []
                if matches:
                    match = random.choice(matches)
                    analysis = odds_analyzer.analyze_match_odds(
                        match_id=match.get("id", 0),
                        home_team=match.get("home_team", "Équipe A"),
                        away_team=match.get("away_team", "Équipe B")
                    )
                    
                    anomalies = analysis.get("anomalies", [])
                    if anomalies:
                        anomaly = anomalies[0]
                        content = f"Anomalie détectée ({confidence:.0%} confiance) sur {anomaly.get('market', market)} pour {match.get('home_team', 'Équipe A')} vs {match.get('away_team', 'Équipe B')}. {anomaly.get('description', 'Mouvement suspect des cotes')}."
                    else:
                        content = f"Anomalie potentielle ({confidence:.0%} confiance) détectée sur {market} dans {league}. Pattern inhabituel dans les mouvements de cotes."
                else:
                    content = f"Anomalie potentielle ({confidence:.0%} confiance) détectée sur {market} dans {league}. Pattern inhabituel dans les mouvements de cotes."
            else:
                teams = [f"Équipe {chr(65+i)}" for i in range(10)]
                team1, team2 = random.sample(teams, 2)
                content = f"Anomalie potentielle ({confidence:.0%} confiance) détectée sur {market} pour {team1} vs {team2} en {league}. Pattern inhabituel dans les mouvements de cotes."
        
        elif category == "Mouvement suspect":
            bookmakers = ["Bet365", "Unibet", "Winamax", "Betclic", "Bwin", "1xBet"]
            teams = [
                random.choice(["Bayern Munich", "Dortmund", "RB Leipzig", "Leverkusen"]),
                random.choice(["Wolfsburg", "Mönchengladbach", "Freiburg", "Hoffenheim"])
            ]
            
            bookmaker = random.choice(bookmakers)
            movement_pct = round(random.uniform(15, 40))
            
            if odds_analyzer:
                # Utiliser l'analyseur avancé pour des informations plus précises
                choices = ['victoire à domicile', 'match nul', 'victoire à extérieur']
                content = f"Mouvement suspect détecté chez {bookmaker}: {movement_pct}% de volume inhabituel sur {teams[0]} vs {teams[1]}. Activité concentrée sur {random.choice(choices)}."
            else:
                content = f"Volume de paris inhabituellement élevé (+{movement_pct}%) chez {bookmaker} pour {teams[0]} vs {teams[1]}."
        
        elif category == "Sentiment des fans":
            teams = ["PSG", "Marseille", "Lyon", "Monaco", "Lille", "Nice"]
            sentiments = ["très négatif", "négatif", "mitigé", "positif", "très positif"]
            
            team = random.choice(teams)
            sentiment = random.choice(sentiments)
            change = random.choice(["stable", "en hausse", "en baisse"])
            
            if sentiment_analyzer:
                # Utiliser l'analyseur avancé pour une analyse plus précise
                events = ['la dernière défaite', 'la victoire récente', 'l\'annonce du transfert', 'la conférence de presse']
                selected_event = random.choice(events)
                content = f"Sentiment {sentiment} ({change}) des fans de {team} suite à {selected_event}. Impact potentiel sur la motivation de l'équipe."
            else:
                content = f"Sentiment {sentiment} des fans de {team}. Tendance {change} sur les réseaux sociaux."
        
        elif category == "Tendance social media":
            players = ["Mbappé", "Haaland", "Vinicius Jr", "De Bruyne", "Salah", "Lewandowski"]
            topics = ["blessure", "méforme", "conflit avec l'entraîneur", "problème personnel", "transfert imminent"]
            
            player = random.choice(players)
            topic = random.choice(topics)
            
            if sentiment_analyzer:
                # Utiliser l'analyseur avancé pour une analyse plus précise
                player_data = data_hub.get_player_details(player_name=player) if hasattr(data_hub, "get_player_details") else None
                team_name = player_data.get("team", "son équipe") if player_data else "son équipe"
                
                impact_levels = ["minimal", "modéré", "significatif", "majeur"]
                impact = random.choice(impact_levels)
                
                content = f"Forte activité sociale concernant {player} ({team_name}) sur le sujet: {topic}. Analyse prévoit un impact {impact} sur les performances à venir."
            else:
                content = f"Pic d'activité sur les réseaux sociaux concernant {player} et une possible {topic}."
        
        elif category == "Événement important":
            events = [
                "Changement d'entraîneur pour {0}. Historique du nouvel entraîneur suggère un impact {1} sur le style de jeu.",
                "Blessure de {0}, joueur clé de {1}. Durée d'indisponibilité estimée: {2} semaines.",
                "Conditions météo extrêmes prévues pour {0} vs {1}. Impact probable sur les équipes à style de jeu technique.",
                "Tension dans le vestiaire de {0} suite aux déclarations de {1}. Possible impact sur la cohésion d'équipe.",
                "Retour de blessure de {0} pour {1}. Stats historiques montrent une période d'adaptation de {2} matchs."
            ]
            
            teams = ["Barcelona", "Real Madrid", "Juventus", "Inter", "AC Milan", "Roma", "Ajax", "PSV"]
            players = ["Messi", "Ronaldo", "Neymar", "Benzema", "Kane", "Son", "Kimmich", "Müller"]
            impacts = ["mineur", "modéré", "significatif", "majeur"]
            durations = ["2-3", "4-6", "6-8", "8-10"]
            
            team1, team2 = random.sample(teams, 2)
            player = random.choice(players)
            impact = random.choice(impacts)
            duration = random.choice(durations)
            
            event_template = random.choice(events)
            content = event_template.format(
                random.choice([player, team1]), 
                random.choice([team1, team2]), 
                random.choice([duration, impact])
            )
        
        elif category == "Opportunité détectée":
            opportunities = [
                "Value Bet identifiée pour {0} vs {1} sur le marché {2}. Écart de {3}% avec notre modèle.",
                "Opportunité Combo: intégrer {0} avec {1} augmente la valeur espérée de {2}%.",
                "Pattern identifié: {0} surperforme systématiquement en {1} période contre des équipes de style {2}.",
                "Inefficacité de marché sur {0}: surévaluation du {1} en raison de {2}.",
                "Opportunité de trading identifiée pour {0} vs {1}. Configuration idéale pour stratégie {2}."
            ]
            
            teams = ["Liverpool", "Chelsea", "Napoli", "Lazio", "Valencia", "Sevilla", "Lyon", "Rennes"]
            markets = ["Victoire/Nul/Défaite", "Over/Under", "BTTS", "Handicap asiatique", "Score exact"]
            periods = ["première", "deuxième"]
            strategies = ["Scalping", "Dutching", "Lay the draw", "Back-to-lay"]
            reasons = ["biais médiatique", "surréaction à une absence", "historique récent", "facteur météo négligé"]
            
            team1, team2 = random.sample(teams, 2)
            market = random.choice(markets)
            ecart = random.randint(5, 15)
            valeur = random.randint(8, 25)
            period = random.choice(periods)
            strategy = random.choice(strategies)
            reason = random.choice(reasons)
            styles = ["possession", "contre-attaque", "pressing haut", "défensif"]
            
            opportunity_template = random.choice(opportunities)
            content = opportunity_template.format(
                team1, 
                team2, 
                random.choice([market, period, strategy, reason, f"{ecart}%"]), 
                random.choice([ecart, valeur, random.choice(styles)])
            )
        
        elif category == "Mise à jour système":
            updates = [
                "Nouveau modèle de prédiction intégré pour les ligues {0}. Amélioration de précision estimée: {1}%.",
                "Mise à jour de l'algorithme d'analyse des {0}. Détection des anomalies améliorée de {1}%.",
                "Nouvelles données {0} intégrées dans le système. Couverture étendue à {1} nouvelles compétitions.",
                "Optimisation du module {0}. Temps de traitement réduit de {1}%.",
                "Recalibration des paramètres du module {0} suite à l'analyse de {1} matchs récents."
            ]
            
            modules = ["ArcanPredict", "BetTrapMap", "ShadowOddsPlus", "FanSentimentMonitor"]
            leagues = ["scandinaves", "sud-américaines", "asiatiques", "africaines", "secondaires européennes"]
            data_types = ["Transfermarkt", "SoccerData", "statistiques avancées", "d'analyse vidéo", "de performance physique"]
            improvement = random.randint(5, 25)
            new_competitions = random.randint(3, 15)
            matches_analyzed = random.randint(200, 2000)
            
            update_template = random.choice(updates)
            content = update_template.format(
                random.choice([random.choice(modules), random.choice(leagues), random.choice(data_types)]),
                random.choice([improvement, new_competitions, matches_analyzed])
            )
        
        elif category == "Alerte de performance":
            alerts = [
                "Performance inhabituelle de {0}: {1}% au-dessus des prévisions sur les {2} derniers matchs.",
                "Sous-performance significative de {0} à domicile: {1}% en dessous des attentes.",
                "Écart statistique détecté: {0} présente un différentiel de {1} entre xG et buts réels.",
                "Tendance émergente: {0} montre une amélioration de {1}% en efficacité défensive sous {2}.",
                "Alerte de cohérence: variabilité de {1}% dans les performances de {0} avec configuration {2}."
            ]
            
            teams = ["Atletico Madrid", "Porto", "Benfica", "Sporting", "Celtic", "Rangers", "Ajax", "Feyenoord"]
            coaches = ["nouvel entraîneur", "système 3-5-2", "pressing intensif", "approche défensive"]
            configurations = ["à l'extérieur", "contre le top 5", "après une défaite", "avec rotation d'effectif"]
            
            performance_pct = random.randint(15, 40)
            matches = random.randint(3, 8)
            differential = round(random.uniform(0.8, 3.5), 1)
            
            alert_template = random.choice(alerts)
            content = alert_template.format(
                random.choice(teams),
                random.choice([performance_pct, differential]),
                random.choice([matches, random.choice(coaches), random.choice(configurations)])
            )
        
        else:  # Catégorie par défaut si nécessaire
            content = f"Notification système: Mise à jour importante dans la catégorie {category}."
        
        # Création de la notification
        notifications.append({
            "id": i+1,
            "category": category,
            "content": content,
            "date": notification_date,
            "priority": priority,
            "read": random.random() > 0.7,  # 30% de notifications non lues
            "actions": get_notification_actions(category),
            "details": get_notification_details(category),
            "enhanced": ShadowOddsPlusEnhanced is not None or FanSentimentMonitorEnhanced is not None
        })
    
    # Tri des notifications par date, des plus récentes aux plus anciennes
    notifications.sort(key=lambda x: x["date"], reverse=True)
    
    return notifications

def get_notification_actions(category):
    """
    Génère des actions possibles pour une notification selon sa catégorie.
    
    Args:
        category (str): Catégorie de la notification
        
    Returns:
        list: Liste des actions disponibles
    """
    # Actions de base disponibles pour toutes les notifications
    base_actions = ["Marquer comme lu", "Ignorer"]
    
    # Actions spécifiques selon la catégorie
    if category in ["Alerte de cotes", "Anomalie de cotes", "Mouvement suspect"]:
        return base_actions + ["Analyser en détail", "Créer une alerte", "Ajouter au suivi"]
    
    elif category in ["Sentiment des fans", "Tendance social media"]:
        return base_actions + ["Voir l'analyse complète", "Surveiller l'évolution", "Exporter les données"]
    
    elif category == "Événement important":
        return base_actions + ["Évaluer l'impact", "Mettre à jour les prévisions", "Partager"]
    
    elif category == "Opportunité détectée":
        return base_actions + ["Ajouter aux favoris", "Intégrer au combo", "Analyser les risques"]
    
    elif category == "Mise à jour système":
        return base_actions + ["Voir les détails", "Vérifier la compatibilité", "Consulter le changelog"]
    
    elif category == "Alerte de performance":
        return base_actions + ["Voir les statistiques", "Comparer avec les prévisions", "Approfondir l'analyse"]
    
    # Actions par défaut
    return base_actions

def get_notification_details(category):
    """
    Génère des détails supplémentaires pour une notification selon sa catégorie.
    
    Args:
        category (str): Catégorie de la notification
        
    Returns:
        dict: Détails supplémentaires
    """
    # Détails spécifiques selon la catégorie
    if category in ["Alerte de cotes", "Anomalie de cotes", "Mouvement suspect"]:
        return {
            "mouvement": f"{random.choice(['+', '-'])}{random.uniform(0.1, 1.5):.2f}",
            "bookmakers": random.sample(["Bet365", "Unibet", "Winamax", "Betclic", "Bwin", "1xBet"], random.randint(1, 3)),
            "confiance": f"{random.uniform(0.65, 0.95):.0%}",
            "heure_detection": (datetime.now() - timedelta(minutes=random.randint(5, 120))).strftime("%H:%M")
        }
    
    elif category in ["Sentiment des fans", "Tendance social media"]:
        return {
            "sources": random.sample(["Twitter", "Facebook", "Instagram", "Reddit", "Forums spécialisés"], random.randint(1, 3)),
            "volume": f"{random.randint(500, 10000)} posts",
            "tendance": random.choice(["en hausse", "stable", "en baisse"]),
            "sentiment": f"{random.uniform(0.2, 0.8):.0%} positif"
        }
    
    elif category == "Événement important":
        return {
            "impact_estime": random.choice(["Faible", "Modéré", "Élevé", "Critique"]),
            "source": random.choice(["Communiqué officiel", "Presse sportive", "Sources internes", "Réseaux sociaux"]),
            "fiabilite": f"{random.uniform(0.7, 1.0):.0%}",
            "date_impact": (datetime.now() + timedelta(days=random.randint(0, 7))).strftime("%d/%m/%Y")
        }
    
    elif category == "Opportunité détectée":
        return {
            "valeur_estimee": f"{random.uniform(1.5, 10.0):.1f}%",
            "niveau_risque": random.choice(["Faible", "Modéré", "Élevé"]),
            "fenetre_optimale": f"{random.randint(1, 24)} heures",
            "confidence": f"{random.uniform(0.6, 0.9):.0%}"
        }
    
    elif category == "Mise à jour système":
        return {
            "version": f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
            "amelioration": f"{random.uniform(2.0, 15.0):.1f}%",
            "modules_concernes": random.sample(["ArcanPredict", "BetTrapMap", "ShadowOddsPlus", "FanSentimentMonitor"], random.randint(1, 3)),
            "date_deploiement": datetime.now().strftime("%d/%m/%Y")
        }
    
    elif category == "Alerte de performance":
        return {
            "ecart": f"{random.choice(['+', '-'])}{random.uniform(10.0, 35.0):.1f}%",
            "metrique": random.choice(["xG", "possession", "tirs cadrés", "duels gagnés", "PPDA"]),
            "matches_analyses": random.randint(3, 10),
            "niveau_confiance": f"{random.uniform(0.7, 0.95):.0%}"
        }
    
    # Détails par défaut
    return {
        "date_detection": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "niveau_importance": random.choice(["Basse", "Moyenne", "Haute"]),
        "source": random.choice(["Système", "Analyse automatique", "API externe"])
    }

def format_notification_date(date):
    """
    Formate la date d'une notification de manière relative.
    
    Args:
        date (datetime): Date à formater
        
    Returns:
        str: Date formatée
    """
    now = datetime.now()
    diff = now - date
    
    if diff.days > 0:
        if diff.days == 1:
            return "hier"
        elif diff.days < 7:
            return f"il y a {diff.days} jours"
        else:
            return date.strftime("%d/%m/%Y")
    else:
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        
        if hours > 0:
            return f"il y a {hours} heure{'s' if hours > 1 else ''}"
        elif minutes > 0:
            return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"
        else:
            return "à l'instant"

def display_enhanced_notifications_tab():
    """
    Affiche l'onglet Notifications enrichi complet.
    """
    st.markdown("## 🔔 Notifications")
    st.markdown("Système centralisé de notifications avec analyse multi-sources")
    
    # Génération des notifications si nécessaire
    if "notifications" not in st.session_state:
        st.session_state.notifications = generate_enhanced_notifications(15)
    
    # Récupération des notifications
    notifications = st.session_state.notifications
    
    # Filtrage des notifications
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Recherche
        search = st.text_input("Rechercher dans les notifications", "")
    
    with col2:
        # Filtre par catégorie
        categories = ["Toutes"] + sorted(list(set([n["category"] for n in notifications])))
        selected_category = st.selectbox("Catégorie", categories)
    
    with col3:
        # Filtre par priorité
        priorities = ["Toutes", "Basse", "Moyenne", "Haute", "Critique"]
        selected_priority = st.selectbox("Priorité", priorities)
    
    # Application des filtres
    filtered_notifications = notifications
    
    if search:
        filtered_notifications = [n for n in filtered_notifications if search.lower() in n["content"].lower()]
    
    if selected_category != "Toutes":
        filtered_notifications = [n for n in filtered_notifications if n["category"] == selected_category]
    
    if selected_priority != "Toutes":
        filtered_notifications = [n for n in filtered_notifications if n["priority"] == selected_priority]
    
    # Affichage du nombre de notifications
    st.markdown(f"### {len(filtered_notifications)} notification{'s' if len(filtered_notifications) != 1 else ''}")
    
    # CSS personnalisé pour les notifications
    st.markdown("""
    <style>
    .notification {
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 5px;
        border-left: 5px solid;
    }
    .notification-high {
        background-color: rgba(231, 76, 60, 0.1);
        border-left-color: #e74c3c;
    }
    .notification-critical {
        background-color: rgba(192, 57, 43, 0.1);
        border-left-color: #c0392b;
    }
    .notification-medium {
        background-color: rgba(241, 196, 15, 0.1);
        border-left-color: #f1c40f;
    }
    .notification-low {
        background-color: rgba(46, 204, 113, 0.1);
        border-left-color: #2ecc71;
    }
    .notification-unread {
        background-color: rgba(94, 75, 139, 0.05);
    }
    .notification-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
    }
    .notification-category {
        font-weight: bold;
    }
    .notification-date {
        color: gray;
        font-size: 0.9em;
    }
    .notification-enhanced {
        display: inline-block;
        background-color: rgba(163, 119, 254, 0.2);
        color: #A377FE;
        font-size: 0.8em;
        padding: 2px 6px;
        border-radius: 10px;
        margin-left: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Affichage des notifications filtrées
    for notification in filtered_notifications:
        # Détermination de la classe CSS selon la priorité
        priority_class = "notification-low"
        if notification["priority"] == "Haute":
            priority_class = "notification-high"
        elif notification["priority"] == "Critique":
            priority_class = "notification-critical"
        elif notification["priority"] == "Moyenne":
            priority_class = "notification-medium"
        
        # Classe pour les notifications non lues
        unread_class = " notification-unread" if not notification["read"] else ""
        
        # Formatage de la date
        formatted_date = format_notification_date(notification["date"])
        
        # Affichage de la notification
        with st.container():
            st.markdown(f"""
            <div class="notification {priority_class}{unread_class}">
                <div class="notification-header">
                    <div>
                        <span class="notification-category">{notification["category"]}</span>
                        {' <span class="notification-enhanced">Enrichi</span>' if notification.get("enhanced") else ''}
                    </div>
                    <span class="notification-date">{formatted_date}</span>
                </div>
                <p>{notification["content"]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Affichage des actions et détails dans un expander
            with st.expander("Actions et détails"):
                # Colonnes pour les actions et détails
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Actions")
                    for action in notification["actions"]:
                        st.button(
                            action, 
                            key=f"action_{notification['id']}_{action}",
                            help=f"Exécuter l'action '{action}' pour cette notification"
                        )
                
                with col2:
                    st.markdown("#### Détails")
                    for key, value in notification["details"].items():
                        if isinstance(value, list):
                            value_str = ", ".join(value)
                        else:
                            value_str = str(value)
                        
                        st.markdown(f"**{key.replace('_', ' ').title()}**: {value_str}")
    
    # Message si aucune notification
    if not filtered_notifications:
        st.info("Aucune notification ne correspond aux critères de filtrage.")
    
    # Boutons d'action globaux
    st.markdown("### Actions globales")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Marquer tout comme lu"):
            for notification in st.session_state.notifications:
                notification["read"] = True
            st.success("Toutes les notifications ont été marquées comme lues.")
            st.rerun()
    
    with col2:
        if st.button("Actualiser"):
            st.session_state.notifications = generate_enhanced_notifications(15)
            st.success("Les notifications ont été actualisées.")
            st.rerun()
    
    with col3:
        # Bouton pour configurer les préférences de notification (simulé)
        if st.button("Préférences"):
            st.info("La configuration des préférences de notification sera disponible dans une future mise à jour.")

def add_enhanced_notifications_tab(tab):
    """
    Ajoute l'onglet Notifications enrichi à l'application principale.
    
    Args:
        tab: Objet tab Streamlit
    """
    with tab:
        display_enhanced_notifications_tab()