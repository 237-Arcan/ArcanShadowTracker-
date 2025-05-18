"""
Module pour récupérer les matchs en direct depuis l'API Football.
"""
import os
import requests
from datetime import datetime

def get_real_live_matches():
    """
    Récupère les matchs en direct depuis l'API Football.
    
    Returns:
        list: Liste des matchs en direct au format adapté pour l'interface
    """
    try:
        # Récupérer la clé API des variables d'environnement
        api_key = os.environ.get('FOOTBALL_API_KEY')
        
        if not api_key:
            print("Erreur: Clé API Football non trouvée")
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
        
        # Transformation des données de l'API au format attendu
        formatted_matches = []
        
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
                "score": f"{goals.get('home', 0)}-{goals.get('away', 0)}"
            }
            
            formatted_matches.append(match_data)
        
        print(f"Récupéré {len(formatted_matches)} matchs en direct depuis l'API Football")
        return formatted_matches
        
    except Exception as e:
        print(f"Erreur lors de la récupération des matchs en direct: {str(e)}")
        return []