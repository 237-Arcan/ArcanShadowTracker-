"""
Module pour l'onglet Notifications d'ArcanShadow.
Ce module centralise toutes les notifications importantes du système.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

def generate_notifications(count=10):
    """
    Génère des notifications simulées pour le système ArcanShadow.
    
    Args:
        count (int): Nombre de notifications à générer
        
    Returns:
        list: Liste des notifications générées
    """
    # Types de notifications possibles
    notification_types = [
        {"type": "prediction_success", "icon": "✅", "title": "Prédiction réussie", "color": "#58D68D"},
        {"type": "prediction_failure", "icon": "❌", "title": "Prédiction échouée", "color": "#EC7063"},
        {"type": "pattern_detected", "icon": "🔍", "title": "Nouveau pattern détecté", "color": "#5499C7"},
        {"type": "system_update", "icon": "🔄", "title": "Mise à jour du système", "color": "#AF7AC5"},
        {"type": "high_value_match", "icon": "💎", "title": "Match à haute valeur", "color": "#F4D03F"},
        {"type": "unusual_pattern", "icon": "⚠️", "title": "Anomalie détectée", "color": "#E67E22"},
        {"type": "learning_event", "icon": "🧠", "title": "Événement d'apprentissage", "color": "#A377FE"}
    ]
    
    # Exemples d'équipes
    teams = [
        "Arsenal", "Chelsea", "Liverpool", "Manchester United", "Manchester City",
        "PSG", "Marseille", "Lyon", "Monaco",
        "Barcelona", "Real Madrid", "Atletico Madrid",
        "Bayern Munich", "Borussia Dortmund",
        "Juventus", "AC Milan", "Inter Milan"
    ]
    
    # Génération des notifications
    notifications = []
    
    # Date de référence (maintenant)
    now = datetime.now()
    
    for i in range(count):
        # Sélection aléatoire du type de notification
        notification_type = random.choice(notification_types)
        
        # Date de la notification (plus récente pour les premiers éléments)
        days_ago = min(30, int(i * 1.5))
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        
        notification_date = now - timedelta(
            days=days_ago,
            hours=hours_ago,
            minutes=minutes_ago
        )
        
        # Génération du contenu selon le type
        if notification_type["type"] == "prediction_success":
            team1 = random.choice(teams)
            team2 = random.choice([t for t in teams if t != team1])
            content = f"La prédiction pour le match {team1} vs {team2} s'est avérée correcte. Score final : {random.randint(0, 3)}-{random.randint(0, 3)}."
            
        elif notification_type["type"] == "prediction_failure":
            team1 = random.choice(teams)
            team2 = random.choice([t for t in teams if t != team1])
            content = f"La prédiction pour le match {team1} vs {team2} était incorrecte. Ce match sera analysé pour améliorer les futurs modèles."
            
        elif notification_type["type"] == "pattern_detected":
            team = random.choice(teams)
            patterns = [
                f"{team} a montré une tendance à marquer dans les 15 dernières minutes lors de matchs à domicile",
                f"Les matchs de {team} ont une moyenne de buts inhabituellement élevée lorsqu'ils jouent sous la pluie",
                f"{team} performe significativement mieux contre des équipes qui favorisent la possession"
            ]
            content = random.choice(patterns)
            
        elif notification_type["type"] == "system_update":
            modules = ["ArcanBrain", "ArcanReflex", "ArcanSentinel", "NumeriCode", "ScoreMatrix"]
            module = random.choice(modules)
            updates = [
                f"Le module {module} a été optimisé pour une meilleure précision des prédictions",
                f"Nouvelle version de {module} déployée avec des améliorations dans le traitement des données",
                f"Mise à jour de {module} avec une algorithme de reconnaissance de patterns amélioré"
            ]
            content = random.choice(updates)
            
        elif notification_type["type"] == "high_value_match":
            team1 = random.choice(teams)
            team2 = random.choice([t for t in teams if t != team1])
            reasons = [
                "anomalies statistiques significatives",
                "opportunités de valeur dans les cotes",
                "pattern historique favorable"
            ]
            content = f"Le match {team1} vs {team2} a été identifié comme ayant un potentiel élevé en raison de {random.choice(reasons)}."
            
        elif notification_type["type"] == "unusual_pattern":
            team = random.choice(teams)
            patterns = [
                f"Performance inhabituelle de {team} après une série de défaites",
                f"Variation significative dans le style de jeu de {team} lors des matchs à l'extérieur",
                f"Comportement statistique atypique de {team} contre des équipes du bas de classement"
            ]
            content = random.choice(patterns)
            
        else:  # learning_event
            topics = [
                "la reconnaissance des styles de jeu défensifs",
                "l'influence des changements d'entraîneur",
                "l'impact des conditions météorologiques sur les résultats",
                "l'adaptation à la fatigue des joueurs en période de matchs fréquents"
            ]
            content = f"Le système a approfondi son apprentissage sur {random.choice(topics)}."
        
        # Création de la notification
        notification = {
            "id": i + 1,
            "type": notification_type["type"],
            "icon": notification_type["icon"],
            "title": notification_type["title"],
            "content": content,
            "color": notification_type["color"],
            "date": notification_date,
            "read": random.random() > 0.3  # 30% de chance d'être non lu
        }
        
        notifications.append(notification)
    
    # Tri par date (plus récent en premier)
    notifications.sort(key=lambda x: x["date"], reverse=True)
    
    return notifications

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
    
    if diff.days > 365:
        return f"il y a {diff.days // 365} an(s)"
    elif diff.days > 30:
        return f"il y a {diff.days // 30} mois"
    elif diff.days > 0:
        return f"il y a {diff.days} jour(s)"
    elif diff.seconds // 3600 > 0:
        return f"il y a {diff.seconds // 3600} heure(s)"
    elif diff.seconds // 60 > 0:
        return f"il y a {diff.seconds // 60} minute(s)"
    else:
        return "à l'instant"

def display_notifications_tab():
    """
    Affiche l'onglet Notifications complet.
    """
    st.markdown("## 📬 Centre de Notifications")
    st.markdown("Toutes les informations importantes du système ArcanShadow sont centralisées ici.")
    
    # Génération des notifications si nécessaire
    if "notifications" not in st.session_state:
        st.session_state.notifications = generate_notifications(15)
    
    # Comptage des notifications non lues
    unread_count = sum(1 for n in st.session_state.notifications if not n["read"])
    
    # Mise à jour du compteur global de notifications (pour l'affichage dans l'onglet)
    if "notification_count" not in st.session_state:
        st.session_state.notification_count = unread_count
    else:
        st.session_state.notification_count = unread_count
    
    # Filtres pour les notifications
    st.markdown("### Filtrer les notifications")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        # Filtre par type
        notification_types = [
            "Tous les types",
            "Prédictions",
            "Patterns détectés",
            "Système",
            "Matchs à valeur"
        ]
        selected_type = st.selectbox("Type", notification_types)
        
        # Mappage des types sélectionnés vers les types réels
        type_mapping = {
            "Prédictions": ["prediction_success", "prediction_failure"],
            "Patterns détectés": ["pattern_detected", "unusual_pattern"],
            "Système": ["system_update", "learning_event"],
            "Matchs à valeur": ["high_value_match"]
        }
    
    with col2:
        # Filtre par date
        date_filters = [
            "Toutes les dates",
            "Aujourd'hui",
            "7 derniers jours",
            "30 derniers jours"
        ]
        selected_date = st.selectbox("Période", date_filters)
        
        # Calcul des dates limites
        now = datetime.now()
        date_limits = {
            "Aujourd'hui": now - timedelta(days=1),
            "7 derniers jours": now - timedelta(days=7),
            "30 derniers jours": now - timedelta(days=30)
        }
    
    with col3:
        # Filtre lu/non lu
        read_filters = ["Tous", "Non lus", "Lus"]
        selected_read = st.selectbox("Statut", read_filters)
    
    # Application des filtres
    filtered_notifications = st.session_state.notifications.copy()
    
    # Filtre par type
    if selected_type != "Tous les types":
        types_to_include = type_mapping.get(selected_type, [])
        filtered_notifications = [n for n in filtered_notifications if n["type"] in types_to_include]
    
    # Filtre par date
    if selected_date != "Toutes les dates":
        date_limit = date_limits.get(selected_date)
        filtered_notifications = [n for n in filtered_notifications if n["date"] >= date_limit]
    
    # Filtre par statut de lecture
    if selected_read == "Non lus":
        filtered_notifications = [n for n in filtered_notifications if not n["read"]]
    elif selected_read == "Lus":
        filtered_notifications = [n for n in filtered_notifications if n["read"]]
    
    # Bouton pour marquer toutes les notifications comme lues
    if st.button("Marquer toutes comme lues"):
        for notification in st.session_state.notifications:
            notification["read"] = True
        st.session_state.notification_count = 0
        st.rerun()
    
    # Affichage des notifications filtrées
    st.markdown("### Notifications")
    
    if not filtered_notifications:
        st.info("Aucune notification ne correspond aux filtres sélectionnés.")
    else:
        for notification in filtered_notifications:
            # Création d'un style CSS personnalisé pour chaque notification
            is_unread = not notification["read"]
            unread_class = "notification-new" if is_unread else ""
            
            # Formatage de la date
            formatted_date = format_notification_date(notification["date"])
            
            # Affichage de la notification
            st.markdown(f"""
            <div class="notification {unread_class}" style="border-left-color: {notification['color']};">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <h4 style="margin: 0; color: {notification['color']};">
                        {notification['icon']} {notification['title']}
                        {' <span style="font-size: 0.7em; padding: 1px 6px; background-color: #EC7063; color: white; border-radius: 10px;">Nouveau</span>' if is_unread else ''}
                    </h4>
                    <span style="color: gray; font-size: 0.9em;">{formatted_date}</span>
                </div>
                <p style="margin: 5px 0 0 0;">{notification['content']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Bouton pour marquer comme lu (seulement pour les non lus)
            if is_unread:
                if st.button(f"Marquer comme lu", key=f"mark_read_{notification['id']}"):
                    # Mise à jour du statut dans la liste originale
                    for n in st.session_state.notifications:
                        if n["id"] == notification["id"]:
                            n["read"] = True
                            break
                    
                    # Mise à jour du compteur
                    st.session_state.notification_count -= 1
                    st.rerun()
    
    # Statistiques sur les notifications
    st.markdown("### Statistiques des notifications")
    
    # Création d'un DataFrame pour l'analyse
    df = pd.DataFrame(st.session_state.notifications)
    
    # Comptage par type
    type_counts = df["type"].value_counts().reset_index()
    type_counts.columns = ["Type", "Nombre"]
    
    # Mappage des types pour l'affichage
    type_names = {
        "prediction_success": "Prédictions réussies",
        "prediction_failure": "Prédictions échouées",
        "pattern_detected": "Patterns détectés",
        "system_update": "Mises à jour système",
        "high_value_match": "Matchs à haute valeur",
        "unusual_pattern": "Anomalies détectées",
        "learning_event": "Événements d'apprentissage"
    }
    
    # Appliquer le mappage avec une fonction pour éviter l'erreur
    def map_type_name(type_key):
        return type_names.get(type_key, type_key)
    
    type_counts["Type"] = type_counts["Type"].apply(map_type_name)
    
    # Colonnes pour statistiques et visualisation
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.dataframe(
            type_counts,
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        # Création d'un graphique simple
        st.markdown("Répartition des notifications par type")
        
        # Utilisation d'un graphique HTML simple (sans Plotly pour simplifier)
        colors = ["#58D68D", "#EC7063", "#5499C7", "#AF7AC5", "#F4D03F", "#E67E22", "#A377FE"]
        
        # Création d'un texte simple pour éviter les erreurs de formatage
        bar_html = "<div>"
        
        # Utilisez des boucles simples et des couleurs fixes
        for i, row in type_counts.iterrows():
            typ = row['Type']
            num = row['Nombre']
            width = min(100, num * 10)
            
            # Alterner entre quelques couleurs fixes
            if i % 3 == 0:
                color = "#5499C7"
            elif i % 3 == 1:
                color = "#58D68D"
            else:
                color = "#F4D03F"
                
            bar_html += f"""
            <div style="margin-bottom: 10px;">
                <div style="font-size: 0.9em;">{typ}</div>
                <div style="display: flex; align-items: center;">
                    <div style="width: {width}%; height: 20px; background-color: {color}; 
                    border-radius: 3px; margin-right: 10px;"></div>
                    <div>{num}</div>
                </div>
            </div>
            """
            
        bar_html += "</div>"
        
        st.markdown(f"""
        <div style="padding: 15px; background-color: rgba(45, 45, 68, 0.1); border-radius: 5px;">
            {bar_html}
        </div>
        """, unsafe_allow_html=True)

def add_notifications_tab(tab):
    """
    Ajoute l'onglet Notifications à l'application principale.
    
    Args:
        tab: Objet tab Streamlit
    """
    with tab:
        display_notifications_tab()