"""
Utilitaire pour mettre à jour les matchs en direct avec des données réelles.
"""
from datetime import datetime
from utils.live_monitoring import get_live_matches

def update_live_matches(session_state):
    """
    Met à jour la liste des matchs en direct dans le session_state avec des données réelles.
    
    Args:
        session_state: Session state de Streamlit pour stocker les données
        
    Returns:
        list: Liste des matchs en direct formatés
    """
    try:
        # Récupération des matchs en direct depuis l'API
        real_live_matches = get_live_matches()
        
        # Formater les données pour l'interface
        formatted_matches = []
        for idx, match in enumerate(real_live_matches):
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
        
        # Mettre à jour les matchs en direct dans la session
        session_state.live_matches = formatted_matches
        
        return formatted_matches
    except Exception as e:
        print(f"Erreur lors de la mise à jour des matchs en direct: {e}")
        # En cas d'erreur, renvoyer une liste vide
        return []