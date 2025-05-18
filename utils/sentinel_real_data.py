"""
Module pour assurer que l'onglet Surveillance en direct utilise les données réelles.
"""
import streamlit as st
from datetime import datetime
from utils.live_monitoring import get_live_matches

def update_sentinel_with_real_data():
    """
    Met à jour la session state de Streamlit avec les données réelles de football
    pour l'onglet Surveillance en direct (ArcanSentinel).
    """
    try:
        # Récupérer les matchs en direct depuis l'API
        real_matches = get_live_matches()
        
        # Formater les données pour l'interface
        formatted_matches = []
        for idx, match in enumerate(real_matches):
            formatted_match = {
                "id": idx + 1,
                "home": match.get('home_team', ''),
                "away": match.get('away_team', ''),
                "league": match.get('league', ''),
                "time": datetime.now().strftime("%H:%M"),
                "status": "En direct",
                "minute": f"{match.get('minute', '0')}'",
                "score": f"{match.get('home_score', 0)}-{match.get('away_score', 0)}"
            }
            formatted_matches.append(formatted_match)
        
        # Mettre à jour la session state
        st.session_state.live_matches = formatted_matches
        
        return True
    except Exception as e:
        print(f"Erreur lors de l'initialisation des données réelles: {e}")
        return False
