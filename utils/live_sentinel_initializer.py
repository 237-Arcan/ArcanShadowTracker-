"""
Module d'initialisation des données pour l'onglet Surveillance en direct.
Ce module permet d'assurer que les données utilisées sont des données réelles.
"""

import streamlit as st
from datetime import datetime
from utils.live_monitoring import get_live_matches

def initialize_surveillance_data():
    """
    Initialise les données de surveillance en direct avec des données réelles.
    Cette fonction met à jour st.session_state.live_matches avec les dernières données 
    disponibles via l'API Football.
    
    Returns:
        bool: True si l'initialisation a réussi, False sinon
    """
    try:
        # Récupérer les matchs en direct via l'API Football
        real_matches = get_live_matches()
        
        # Formater les données pour les rendre compatibles avec l'interface
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
        
        # Mettre à jour la session state avec les données réelles
        st.session_state.live_matches = formatted_matches
        
        return True
    except Exception as e:
        print(f"Erreur lors de l'initialisation des données de surveillance: {e}")
        # En cas d'erreur, créer une liste vide
        if 'live_matches' not in st.session_state:
            st.session_state.live_matches = []
        return False