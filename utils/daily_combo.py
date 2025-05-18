"""
Module pour la génération des combinaisons quotidiennes.
"""
import random
from datetime import datetime, timedelta

def get_daily_combos(all_matches, days_range=3, combo_sizes=None, min_odds=1.3, max_selections=5):
    """
    Génère des combinaisons optimisées à partir des matchs disponibles.
    
    Args:
        all_matches (list): Liste de tous les matchs disponibles
        days_range (int): Nombre de jours à considérer pour les matchs
        combo_sizes (list): Tailles des combinaisons à générer
        min_odds (float): Cote minimale par sélection
        max_selections (int): Nombre maximal de sélections par combinaison
        
    Returns:
        dict: Combinaisons par taille
    """
    if combo_sizes is None:
        combo_sizes = [2, 3, 4, 5]
    
    # Filtrer les matchs des prochains jours
    today = datetime.now().date()
    filtered_matches = []
    
    for match in all_matches:
        if not isinstance(match, dict):
            continue
            
        match_date_str = match.get('date', '')
        if not match_date_str:
            continue
            
        try:
            match_date = datetime.strptime(match_date_str, "%Y-%m-%d").date()
            days_diff = (match_date - today).days
            
            if 0 <= days_diff <= days_range:
                filtered_matches.append(match)
        except ValueError:
            # Si la date n'est pas parsable, ignorer le match
            continue
    
    # Si aucun match n'est disponible, retourner un dictionnaire vide
    if not filtered_matches:
        return {size: [] for size in combo_sizes}
    
    # Analyser les matchs pour déterminer les meilleures sélections
    all_selections = []
    
    for match in filtered_matches:
        # Récupérer les informations du match
        home_team = match.get('home_team', match.get('home', '?'))
        away_team = match.get('away_team', match.get('away', '?'))
        league = match.get('league', '')
        date = match.get('date', '')
        time = match.get('time', '')
        match_display = f"{home_team} vs {away_team}"
        
        # Récupérer les cotes et probabilités
        home_odds = match.get('home_odds', 0)
        draw_odds = match.get('draw_odds', 0)
        away_odds = match.get('away_odds', 0)
        
        home_prob = match.get('home_prob', 0)
        draw_prob = match.get('draw_prob', 0)
        away_prob = match.get('away_prob', 0)
        
        # Vérifier si les cotes sont valides
        if home_odds <= 1.0 or draw_odds <= 1.0 or away_odds <= 1.0:
            continue
        
        # Créer des sélections pour ce match
        selections = []
        
        # Victoire à domicile
        if home_odds >= min_odds:
            confidence = home_prob
            value_rating = _calculate_value_rating(home_odds, home_prob)
            
            selections.append({
                'match': match_display,
                'league': league,
                'date': date,
                'time': time,
                'selection': f"Victoire {home_team}",
                'odds': home_odds,
                'confidence': confidence,
                'value_rating': value_rating
            })
        
        # Match nul
        if draw_odds >= min_odds:
            confidence = draw_prob
            value_rating = _calculate_value_rating(draw_odds, draw_prob)
            
            selections.append({
                'match': match_display,
                'league': league,
                'date': date,
                'time': time,
                'selection': "Match nul",
                'odds': draw_odds,
                'confidence': confidence,
                'value_rating': value_rating
            })
        
        # Victoire à l'extérieur
        if away_odds >= min_odds:
            confidence = away_prob
            value_rating = _calculate_value_rating(away_odds, away_prob)
            
            selections.append({
                'match': match_display,
                'league': league,
                'date': date,
                'time': time,
                'selection': f"Victoire {away_team}",
                'odds': away_odds,
                'confidence': confidence,
                'value_rating': value_rating
            })
        
        # Doubles chances (optionnel)
        # 1X (Domicile ou Nul)
        home_draw_odds = round(1 / ((1/home_odds) + (1/draw_odds)), 2)
        if home_draw_odds >= min_odds:
            confidence = home_prob + draw_prob
            value_rating = _calculate_value_rating(home_draw_odds, confidence)
            
            selections.append({
                'match': match_display,
                'league': league,
                'date': date,
                'time': time,
                'selection': f"Double chance: {home_team} ou Nul",
                'odds': home_draw_odds,
                'confidence': confidence,
                'value_rating': value_rating
            })
        
        # X2 (Nul ou Extérieur)
        draw_away_odds = round(1 / ((1/draw_odds) + (1/away_odds)), 2)
        if draw_away_odds >= min_odds:
            confidence = draw_prob + away_prob
            value_rating = _calculate_value_rating(draw_away_odds, confidence)
            
            selections.append({
                'match': match_display,
                'league': league,
                'date': date,
                'time': time,
                'selection': f"Double chance: Nul ou {away_team}",
                'odds': draw_away_odds,
                'confidence': confidence,
                'value_rating': value_rating
            })
        
        # Ajouter toutes les sélections pour ce match
        all_selections.extend(selections)
    
    # Trier les sélections par valeur décroissante
    all_selections.sort(key=lambda x: x['value_rating'], reverse=True)
    
    # Limiter aux meilleures sélections
    best_selections = all_selections[:min(30, len(all_selections))]
    
    # Générer des combinaisons pour chaque taille demandée
    combos_by_size = {}
    
    for size in combo_sizes:
        if size > len(best_selections) or size > max_selections:
            combos_by_size[size] = []
            continue
        
        # Générer un certain nombre de combinaisons (jusqu'à 5)
        combos = []
        
        for _ in range(min(5, len(best_selections) // size)):
            # Sélectionner un sous-ensemble aléatoire de sélections
            combo_selections = random.sample(best_selections, size)
            
            # Éviter les sélections du même match
            matches_set = set()
            is_valid = True
            
            for sel in combo_selections:
                if sel['match'] in matches_set:
                    is_valid = False
                    break
                matches_set.add(sel['match'])
            
            if not is_valid:
                # Si une combinaison contient plusieurs sélections du même match, réessayer
                continue
            
            # Calculer la cote totale
            total_odds = 1.0
            for sel in combo_selections:
                total_odds *= sel['odds']
            
            # Calculer la confiance moyenne
            avg_confidence = sum(sel['confidence'] for sel in combo_selections) / len(combo_selections)
            
            # Créer l'objet combinaison
            combo = {
                'matches': combo_selections,
                'total_odds': total_odds,
                'avg_confidence': avg_confidence,
                'expected_value': total_odds * (avg_confidence / 100),
                'size': size
            }
            
            combos.append(combo)
        
        # Trier les combinaisons par valeur attendue
        combos.sort(key=lambda x: x['expected_value'], reverse=True)
        
        combos_by_size[size] = combos
    
    return combos_by_size

def _calculate_value_rating(odds, probability):
    """
    Calcule un indice de valeur pour une sélection.
    
    Args:
        odds (float): Cote de la sélection
        probability (float): Probabilité estimée (0-100)
        
    Returns:
        float: Indice de valeur
    """
    # Convertir la probabilité en décimal
    prob_decimal = probability / 100
    
    # Calculer la valeur attendue (espérance mathématique)
    expected_value = prob_decimal * odds
    
    # Calculer la valeur implicite des cotes
    implied_probability = 1 / odds
    
    # Calculer l'avantage de valeur
    value_edge = prob_decimal - implied_probability
    
    # Combiner les métriques en un indice de valeur
    value_rating = (expected_value * 0.7) + (value_edge * 100 * 0.3)
    
    return value_rating

def get_daily_combo_analysis(combo):
    """
    Génère une analyse détaillée d'une combinaison.
    
    Args:
        combo (dict): Données de la combinaison
        
    Returns:
        dict: Analyse détaillée
    """
    # Extraire les informations de la combinaison
    selections = combo['matches']
    total_odds = combo['total_odds']
    avg_confidence = combo['avg_confidence']
    
    # Calculer les probabilités et le risque
    win_probability = avg_confidence / 100
    loss_probability = 1 - win_probability
    
    # Niveau de risque
    risk_level = "Élevé" if total_odds > 10 else "Moyen" if total_odds > 5 else "Faible"
    
    # Mise recommandée (simulée)
    base_stake = 10  # Mise de base en unités
    recommended_stake = max(1, min(25, int(100 / total_odds)))
    
    # Motifs de sélection
    selection_reasons = []
    for sel in selections:
        match_name = sel['match']
        selection_text = sel['selection']
        confidence = sel['confidence']
        
        reason = f"{match_name}: {selection_text} ({confidence}% de confiance)"
        selection_reasons.append(reason)
    
    # Générer l'analyse
    analysis = {
        'win_probability': win_probability,
        'expected_return': total_odds * base_stake * win_probability,
        'risk_level': risk_level,
        'recommended_stake': recommended_stake,
        'selection_reasons': selection_reasons,
        'advice': _generate_combo_advice(total_odds, avg_confidence, risk_level)
    }
    
    return analysis

def _generate_combo_advice(total_odds, avg_confidence, risk_level):
    """
    Génère un conseil pour une combinaison.
    
    Args:
        total_odds (float): Cote totale de la combinaison
        avg_confidence (float): Confiance moyenne
        risk_level (str): Niveau de risque
        
    Returns:
        str: Conseil pour la combinaison
    """
    if risk_level == "Élevé":
        advice = f"Cette combinaison présente un odds total élevé de {total_odds:.2f}, "
        advice += f"avec une probabilité de réussite estimée à {avg_confidence:.1f}%. "
        advice += "Considérez une mise plus faible que la normale, "
        advice += "car le risque est élevé malgré la forte valeur potentielle."
        
    elif risk_level == "Moyen":
        advice = f"Cette combinaison a un odds total de {total_odds:.2f}, "
        advice += f"avec une probabilité de succès de {avg_confidence:.1f}%. "
        advice += "Le risque est modéré, donc une mise standard est recommandée, "
        advice += "avec un bon équilibre entre risque et récompense."
        
    else:  # Faible
        advice = f"Cette combinaison présente un odds total modéré de {total_odds:.2f}, "
        advice += f"avec une bonne probabilité de succès estimée à {avg_confidence:.1f}%. "
        advice += "Le risque est relativement faible, vous pouvez donc envisager "
        advice += "une mise légèrement supérieure à votre mise habituelle."
    
    return advice