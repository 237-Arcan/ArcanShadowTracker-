"""
Module pour la génération de combinaisons quotidiennes de paris
basées sur des données réelles de football.
"""
import random
from datetime import datetime, timedelta

def filter_matches_by_date(matches, target_date=None, days_range=3):
    """
    Filtre les matchs pour ne garder que ceux dans une plage de dates spécifique.
    
    Args:
        matches (list): Liste de tous les matchs disponibles
        target_date (str): Date cible au format YYYY-MM-DD (par défaut aujourd'hui)
        days_range (int): Nombre de jours autour de la date cible
        
    Returns:
        list: Matchs filtrés dans la plage de dates
    """
    if not target_date:
        target_date = datetime.now().strftime("%Y-%m-%d")
        
    target_dt = datetime.strptime(target_date, "%Y-%m-%d")
    start_date = (target_dt - timedelta(days=days_range)).strftime("%Y-%m-%d")
    end_date = (target_dt + timedelta(days=days_range)).strftime("%Y-%m-%d")
    
    filtered_matches = []
    for match in matches:
        if not isinstance(match, dict):
            continue
            
        match_date = match.get('date', '')
        if start_date <= match_date <= end_date:
            filtered_matches.append(match)
    
    return filtered_matches

def select_best_matches(matches, num_matches=3):
    """
    Sélectionne les meilleurs matchs pour les paris combinés.
    
    Args:
        matches (list): Liste de matchs disponibles
        num_matches (int): Nombre de matchs à sélectionner
        
    Returns:
        list: Matchs sélectionnés pour les combinaisons
    """
    if not matches:
        return []
        
    # Trier les matchs par fiabilité prédictive
    matches_with_confidence = []
    
    for match in matches:
        if not isinstance(match, dict):
            continue
            
        # Calculer un score de confiance pour ce match
        home_prob = match.get('home_prob', 0.33)
        draw_prob = match.get('draw_prob', 0.33)
        away_prob = match.get('away_prob', 0.33)
        
        # Un match avec une forte probabilité dans un sens ou l'autre est plus fiable
        max_prob = max(home_prob, draw_prob, away_prob)
        confidence = (max_prob - 0.33) * 1.5  # Normaliser à une échelle plus étendue
        
        # Ajouter des métadonnées temporaires
        match_with_meta = dict(match)
        match_with_meta['confidence'] = confidence
        match_with_meta['max_prob'] = max_prob
        match_with_meta['max_outcome'] = 'home' if max_prob == home_prob else ('draw' if max_prob == draw_prob else 'away')
        
        matches_with_confidence.append(match_with_meta)
    
    # Trier par confiance décroissante
    sorted_matches = sorted(matches_with_confidence, key=lambda x: x['confidence'], reverse=True)
    
    # Sélectionner les N meilleurs matchs (ou moins si pas assez disponibles)
    best_matches = sorted_matches[:min(num_matches, len(sorted_matches))]
    
    return best_matches

def generate_daily_combos(matches, combo_sizes=[2, 3, 4]):
    """
    Génère des combinaisons quotidiennes de paris à partir des matchs sélectionnés.
    
    Args:
        matches (list): Liste des matchs sélectionnés
        combo_sizes (list): Tailles des combinaisons à générer
        
    Returns:
        dict: Combinaisons organisées par taille
    """
    combos = {}
    
    for size in combo_sizes:
        if len(matches) < size:
            # Pas assez de matchs pour cette taille de combo
            continue
            
        # Générer des combinaisons de cette taille
        combo_matches = random.sample(matches, size)
        
        # Calculer la cote combinée et la confiance globale
        combo_odds = 1.0
        combo_confidence = 1.0
        combo_selections = []
        
        for match in combo_matches:
            outcome = match.get('max_outcome', 'home')
            
            if outcome == 'home':
                selection = f"Victoire {match.get('home_team', match.get('home', '?'))}"
                odds = match.get('home_odds', 1.5)
                outcome_desc = f"1 ({match.get('home_team', match.get('home', '?'))})"
            elif outcome == 'draw':
                selection = f"Match nul"
                odds = match.get('draw_odds', 3.5)
                outcome_desc = "X (Nul)"
            else:  # away
                selection = f"Victoire {match.get('away_team', match.get('away', '?'))}"
                odds = match.get('away_odds', 2.5)
                outcome_desc = f"2 ({match.get('away_team', match.get('away', '?'))})"
            
            combo_odds *= odds
            combo_confidence *= match.get('confidence', 0.5)
            
            # Construire les détails de la sélection
            combo_selections.append({
                'match': f"{match.get('home_team', match.get('home', '?'))} vs {match.get('away_team', match.get('away', '?'))}",
                'league': match.get('league', '?'),
                'date': match.get('date', ''),
                'time': match.get('time', match.get('kickoff_time', '??:??')),
                'selection': selection,
                'outcome': outcome_desc,
                'odds': odds,
                'confidence': round(match.get('confidence', 0.5) * 100)
            })
        
        # Arrondir les cotes combinées
        combo_odds = round(combo_odds, 2)
        combo_confidence = round(combo_confidence * 100)
        
        # Ajouter cette combinaison au dictionnaire
        if size not in combos:
            combos[size] = []
            
        combos[size].append({
            'matches': combo_selections,
            'total_odds': combo_odds,
            'confidence': combo_confidence
        })
    
    return combos

def get_daily_combos(all_matches, days_range=3, combo_sizes=[2, 3, 4]):
    """
    Fonction principale pour obtenir les combinaisons quotidiennes.
    
    Args:
        all_matches (list): Liste complète des matchs disponibles
        days_range (int): Plage de jours pour les matchs
        combo_sizes (list): Tailles des combinaisons à générer
        
    Returns:
        dict: Combinaisons organisées par taille
    """
    # Filtrer les matchs par date
    filtered_matches = filter_matches_by_date(all_matches, days_range=days_range)
    
    # Sélectionner les meilleurs matchs
    best_matches = select_best_matches(filtered_matches, num_matches=10)
    
    # Générer les combinaisons
    combos = generate_daily_combos(best_matches, combo_sizes=combo_sizes)
    
    return combos