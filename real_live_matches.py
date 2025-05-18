"""
Module pour récupérer et afficher les matchs en direct depuis l'API Football.
"""
import os
import requests
from datetime import datetime
import streamlit as st
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_live_football_matches():
    """
    Récupère les matchs en direct depuis l'API Football.
    
    Returns:
        list: Liste des matchs en direct au format de l'application
    """
    try:
        # Récupérer la clé API
        api_key = os.environ.get('FOOTBALL_API_KEY')
        
        if not api_key:
            st.warning("Clé API Football non trouvée. Veuillez configurer la clé API pour accéder aux données réelles.")
            return []
        
        # Préparer la requête
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
        
        # Transformer les données
        formatted_matches = []
        
        if data.get('response'):
            st.success(f"Données réelles récupérées: {len(data['response'])} matchs en direct trouvés")
            
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
                    # Ajout des clés utilisées par l'application
                    "home_team": teams.get('home', {}).get('name', ''),
                    "away_team": teams.get('away', {}).get('name', ''),
                    "period": status.get('long', 'En direct')
                }
                
                formatted_matches.append(match_data)
        else:
            st.info("Aucun match en direct n'est disponible actuellement via l'API.")
        
        return formatted_matches
        
    except Exception as e:
        st.error(f"Erreur lors de la récupération des matchs en direct: {str(e)}")
        return []

def update_live_matches_section():
    """
    Met à jour la section des matchs en direct dans l'application.
    Cette fonction sera appelée depuis l'application principale.
    """
    # Récupérer les matchs en direct depuis l'API
    live_matches = get_live_football_matches()
    
    # Mettre à jour la session state
    if live_matches:
        st.session_state.live_matches = live_matches
    else:
        # Si aucun match n'est disponible, utiliser une liste vide
        st.session_state.live_matches = []
        st.warning("Aucun match en direct n'est disponible actuellement. Veuillez réessayer plus tard.")
    
    return live_matches