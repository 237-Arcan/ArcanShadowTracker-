"""Version corrigée de l'initialisation des matchs en direct pour ArcanSentinel."""

# Cette fonction remplace l'initialisation statique des matchs en direct
def initialize_live_matches(session_state):
    """
    Initialise les matchs en direct avec des données réelles provenant de l'API Football.
    
    Args:
        session_state: Session state de Streamlit pour stocker les données
    """
    try:
        # Importer les fonctions nécessaires
        from utils.live_monitoring import get_live_matches
        from datetime import datetime
        
        # Récupérer les matchs en direct via l'API
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
        session_state.live_matches = formatted_matches
        
        # Log de confirmation
        print(f"Initialisation des matchs en direct réussie: {len(formatted_matches)} matchs récupérés.")
    except Exception as e:
        print(f"Erreur lors de l'initialisation des matchs en direct: {e}")
        # En cas d'erreur, initialiser avec une liste vide
        session_state.live_matches = []

# Instructions:
# 1. Importer cette fonction dans app.py
# 2. Remplacer:
#    ```
#    # Structure pour les matchs en direct
#    if 'live_matches' not in st.session_state:
#        st.session_state.live_matches = [
#            {"id": 1, "home": "PSG", "away": "Lyon", "league": "Ligue 1", "time": "20:45", "status": "En direct", "minute": "37'", "score": "1-0"},
#            {"id": 2, "home": "Liverpool", "away": "Arsenal", "league": "Premier League", "time": "17:30", "status": "En direct", "minute": "68'", "score": "2-1"},
#            {"id": 3, "home": "Bayern Munich", "away": "Dortmund", "league": "Bundesliga", "time": "18:30", "status": "En direct", "minute": "52'", "score": "0-0"}
#        ]
#    ```
#    Par:
#    ```
#    # Structure pour les matchs en direct avec données réelles
#    if 'live_matches' not in st.session_state:
#        initialize_live_matches(st.session_state)
#    ```