"""
Module pour l'analyse prédictive des matchs de football.
"""
import random
from datetime import datetime
from utils.football_data import get_team_form, get_head_to_head, get_team_stats

def get_prediction_data(match, all_matches=None):
    """
    Génère les données de prédiction pour un match spécifique.
    
    Args:
        match (dict): Données du match
        all_matches (list): Toutes les données de match disponibles
        
    Returns:
        dict: Données de prédiction formatées
    """
    if not isinstance(match, dict):
        return {"error": "Format de match invalide"}
        
    # Extraire les informations du match
    home_team = match.get('home_team', match.get('home', '?'))
    away_team = match.get('away_team', match.get('away', '?'))
    league = match.get('league', '')
    date = match.get('date', '')
    time = match.get('time', '')
    
    # Obtenir les cotes et probabilités
    home_odds = match.get('home_odds', 0)
    draw_odds = match.get('draw_odds', 0) 
    away_odds = match.get('away_odds', 0)
    
    home_prob = match.get('home_prob', 0)
    draw_prob = match.get('draw_prob', 0)
    away_prob = match.get('away_prob', 0)
    
    # Obtenir les données de forme pour chaque équipe
    home_form = get_team_form(home_team)
    away_form = get_team_form(away_team)
    
    # Obtenir l'historique des confrontations directes
    head_to_head = get_head_to_head(home_team, away_team)
    
    # Obtenir les statistiques des équipes
    home_stats = get_team_stats(home_team)
    away_stats = get_team_stats(away_team)
    
    # Déterminer le résultat le plus probable
    outcomes = ['Victoire à domicile', 'Match nul', 'Victoire à l\'extérieur']
    probabilities = [home_prob, draw_prob, away_prob]
    main_outcome = outcomes[probabilities.index(max(probabilities))]
    
    # Trouver les trois scénarios de score les plus probables
    possible_scores = []
    
    # Victoires à domicile
    if home_prob > 20:
        home_win_scores = ['1-0', '2-0', '2-1', '3-1']
        weight_factor = home_prob / 100
        for score in home_win_scores:
            # Attribution aléatoire de probabilités, mais influencées par la probabilité générale
            probability = int(random.uniform(0.5, 1.0) * weight_factor * 100)
            possible_scores.append({
                'score': score,
                'probability': probability,
                'outcome': 'Victoire à domicile'
            })
    
    # Matchs nuls
    if draw_prob > 10:
        draw_scores = ['0-0', '1-1', '2-2']
        weight_factor = draw_prob / 100
        for score in draw_scores:
            possible_scores.append({
                'score': score,
                'probability': int(random.uniform(0.5, 1.0) * weight_factor * 100),
                'outcome': 'Match nul'
            })
    
    # Victoires à l'extérieur
    if away_prob > 20:
        away_win_scores = ['0-1', '0-2', '1-2', '1-3']
        weight_factor = away_prob / 100
        for score in away_win_scores:
            probability = int(random.uniform(0.5, 1.0) * weight_factor * 100)
            possible_scores.append({
                'score': score,
                'probability': probability,
                'outcome': 'Victoire à l\'extérieur'
            })
    
    # Trier par probabilité et prendre les plus probables
    possible_scores.sort(key=lambda x: x['probability'], reverse=True)
    top_scores = possible_scores[:5]
    
    # Générer des scénarios alternatifs
    other_scenarios = []
    
    # Scénario de but de chaque équipe
    other_scenarios.append({
        'name': 'Les deux équipes marquent',
        'probability': _calculate_both_teams_score(home_stats, away_stats),
        'odds': round(1.5 + random.random() * 1, 2)
    })
    
    # Scénario de plus/moins de buts
    other_scenarios.append({
        'name': 'Plus de 2.5 buts',
        'probability': _calculate_over_under_probability(home_stats, away_stats, 2.5, 'over'),
        'odds': round(1.8 + random.random() * 0.8, 2)
    })
    
    # Scénario de clean sheet
    other_scenarios.append({
        'name': f'Clean sheet pour {home_team}',
        'probability': _calculate_clean_sheet_probability(home_stats, away_stats, True),
        'odds': round(2.0 + random.random() * 1.5, 2)
    })
    
    # Scénario de victoire sans concéder
    other_scenarios.append({
        'name': f'{home_team} gagne sans concéder',
        'probability': int(home_prob * _calculate_clean_sheet_probability(home_stats, away_stats, True) / 100),
        'odds': round(home_odds * 1.5, 2)
    })
    
    # Scénario de première mi-temps / match complet
    other_scenarios.append({
        'name': f'Mi-temps/Fin: {home_team}/{home_team}',
        'probability': int(home_prob * 0.7),
        'odds': round(home_odds * 2, 2)
    })
    
    # Générer un narratif d'analyse pour le match
    narrative = _generate_match_narrative(
        home_team, away_team, 
        home_form, away_form,
        head_to_head,
        home_stats, away_stats,
        main_outcome, top_scores[0] if top_scores else None
    )
    
    # Structure finale des données de prédiction
    prediction_data = {
        'match_info': {
            'home_team': home_team,
            'away_team': away_team,
            'league': league,
            'date': date,
            'time': time,
            'home_odds': home_odds,
            'draw_odds': draw_odds,
            'away_odds': away_odds
        },
        'main_prediction': {
            'outcome': main_outcome,
            'odds': home_odds if main_outcome == 'Victoire à domicile' else
                     draw_odds if main_outcome == 'Match nul' else away_odds,
            'confidence': max(probabilities)
        },
        'score_predictions': top_scores,
        'team_forms': {
            'home': home_form,
            'away': away_form
        },
        'head_to_head': head_to_head,
        'team_stats': {
            'home': home_stats,
            'away': away_stats
        },
        'other_scenarios': other_scenarios,
        'narrative': narrative
    }
    
    return prediction_data

def _calculate_both_teams_score(home_stats, away_stats):
    """Calcule la probabilité que les deux équipes marquent."""
    # Utiliser les statistiques d'attaque et de défense pour estimer la probabilité
    home_attack = home_stats['goals_scored'] / (home_stats['home_record']['wins'] + 
                                               home_stats['home_record']['draws'] + 
                                               home_stats['home_record']['losses'])
    away_attack = away_stats['goals_scored'] / (away_stats['away_record']['wins'] + 
                                               away_stats['away_record']['draws'] + 
                                               away_stats['away_record']['losses'])
    
    # Normaliser pour obtenir une probabilité entre 40% et 90%
    base_prob = (home_attack + away_attack) * 10
    return max(40, min(90, int(base_prob)))

def _calculate_over_under_probability(home_stats, away_stats, line, direction='over'):
    """Calcule la probabilité de dépasser ou non une ligne de buts."""
    # Calculer le nombre moyen de buts par match pour chaque équipe
    home_avg_goals = home_stats['goals_scored'] / (home_stats['home_record']['wins'] + 
                                                 home_stats['home_record']['draws'] + 
                                                 home_stats['home_record']['losses'])
    away_avg_goals = away_stats['goals_scored'] / (away_stats['away_record']['wins'] + 
                                                 away_stats['away_record']['draws'] + 
                                                 away_stats['away_record']['losses'])
    
    # Estimer le nombre total de buts attendus
    expected_goals = home_avg_goals + away_avg_goals
    
    # Calculer la probabilité en fonction de la ligne et de la direction
    if direction == 'over':
        base_prob = 50 + (expected_goals - line) * 20
    else:  # under
        base_prob = 50 - (expected_goals - line) * 20
    
    # Limiter la probabilité entre 25% et 85%
    return max(25, min(85, int(base_prob)))

def _calculate_clean_sheet_probability(home_stats, away_stats, is_home):
    """Calcule la probabilité d'un clean sheet."""
    if is_home:
        # Probabilité de clean sheet pour l'équipe à domicile
        clean_sheet_ratio = home_stats['clean_sheets'] / (home_stats['home_record']['wins'] + 
                                                         home_stats['home_record']['draws'] + 
                                                         home_stats['home_record']['losses'])
        
        # Ajuster en fonction de la capacité offensive de l'équipe adverse
        away_attack_strength = away_stats['goals_scored'] / (away_stats['away_record']['wins'] + 
                                                           away_stats['away_record']['draws'] + 
                                                           away_stats['away_record']['losses'])
    else:
        # Probabilité de clean sheet pour l'équipe à l'extérieur
        clean_sheet_ratio = away_stats['clean_sheets'] / (away_stats['away_record']['wins'] + 
                                                         away_stats['away_record']['draws'] + 
                                                         away_stats['away_record']['losses'])
        
        # Ajuster en fonction de la capacité offensive de l'équipe adverse
        home_attack_strength = home_stats['goals_scored'] / (home_stats['home_record']['wins'] + 
                                                           home_stats['home_record']['draws'] + 
                                                           home_stats['home_record']['losses'])
    
    # Calculer la probabilité finale
    base_prob = clean_sheet_ratio * 50
    
    # Limiter la probabilité entre 10% et 70%
    return max(10, min(70, int(base_prob)))

def _generate_match_narrative(home_team, away_team, home_form, away_form, h2h, 
                             home_stats, away_stats, prediction, score_prediction):
    """
    Génère une analyse narrative du match basée sur les statistiques et prédictions.
    
    Returns:
        str: Texte d'analyse narrative
    """
    # Tendances de forme
    home_trend = home_form['form_trend']
    away_trend = away_form['form_trend']
    
    # Déterminer les points forts et faibles
    home_strengths = []
    home_weaknesses = []
    away_strengths = []
    away_weaknesses = []
    
    # Forces et faiblesses de l'équipe à domicile
    if home_stats['goals_scored'] > 45:
        home_strengths.append("attaque prolifique")
    if home_stats['clean_sheets'] > 10:
        home_strengths.append("défense solide")
    if home_stats['possession'] > 55:
        home_strengths.append("contrôle du ballon")
    if home_stats['pass_completion'] > 85:
        home_strengths.append("précision des passes")
        
    if home_stats['goals_conceded'] > 45:
        home_weaknesses.append("défense vulnérable")
    if home_stats['cards']['yellow'] > 60:
        home_weaknesses.append("indiscipline")
    if home_stats['clean_sheets'] < 8:
        home_weaknesses.append("difficulté à garder sa cage inviolée")
    if home_stats['possession'] < 48:
        home_weaknesses.append("faible possession")
        
    # Forces et faiblesses de l'équipe à l'extérieur
    if away_stats['goals_scored'] > 45:
        away_strengths.append("attaque redoutable")
    if away_stats['clean_sheets'] > 10:
        away_strengths.append("solidité défensive")
    if away_stats['possession'] > 55:
        away_strengths.append("maîtrise du jeu")
    if away_stats['pass_completion'] > 85:
        away_strengths.append("qualité technique")
        
    if away_stats['goals_conceded'] > 45:
        away_weaknesses.append("fragilité défensive")
    if away_stats['cards']['yellow'] > 60:
        away_weaknesses.append("tendance à l'indiscipline")
    if away_stats['clean_sheets'] < 8:
        away_weaknesses.append("vulnérabilité défensive")
    if away_stats['possession'] < 48:
        away_weaknesses.append("difficulté à garder le ballon")
    
    # Assurer qu'il y a au moins un élément dans chaque liste
    if not home_strengths:
        home_strengths.append("jeu à domicile")
    if not home_weaknesses:
        home_weaknesses.append("pression à domicile")
    if not away_strengths:
        away_strengths.append("vitesse en contre")
    if not away_weaknesses:
        away_weaknesses.append("performances variables à l'extérieur")
    
    # Construire le narratif
    narrative = f"Ce match entre {home_team} et {away_team} s'annonce comme "
    
    if prediction == 'Victoire à domicile':
        narrative += f"une rencontre où {home_team} devrait avoir l'avantage. "
    elif prediction == 'Match nul':
        narrative += "une rencontre équilibrée entre deux équipes de niveau similaire. "
    else:
        narrative += f"une rencontre où {away_team} pourrait créer la surprise à l'extérieur. "
    
    # Ajouter des informations sur la forme
    narrative += f"\n\n{home_team} est actuellement dans une dynamique {home_trend}, "
    narrative += f"avec {home_form['wins']} victoires sur leurs {len(home_form['results'])} derniers matchs. "
    narrative += f"Leurs principales forces sont leur {home_strengths[0]}"
    if len(home_strengths) > 1:
        narrative += f" et leur {home_strengths[1]}"
    narrative += f", mais ils montrent des faiblesses en termes de {home_weaknesses[0]}. "
    
    narrative += f"\n\n{away_team}, de leur côté, affiche une forme {away_trend} "
    narrative += f"avec {away_form['wins']} succès lors de leurs {len(away_form['results'])} dernières sorties. "
    narrative += f"Ils excellent particulièrement dans leur {away_strengths[0]}"
    if len(away_strengths) > 1:
        narrative += f" et leur {away_strengths[1]}"
    narrative += f", mais peuvent être vulnérables sur leur {away_weaknesses[0]}. "
    
    # Ajouter des informations sur les confrontations directes
    h2h_team1_wins = sum(1 for match in h2h if match['result'] == 'team1_win')
    h2h_draws = sum(1 for match in h2h if match['result'] == 'draw')
    h2h_team2_wins = sum(1 for match in h2h if match['result'] == 'team2_win')
    
    narrative += f"\n\nL'historique récent entre ces deux équipes montre que {home_team} a remporté {h2h_team1_wins} des {len(h2h)} dernières confrontations, "
    narrative += f"contre {h2h_team2_wins} pour {away_team}, avec {h2h_draws} match{'s' if h2h_draws > 1 else ''} nul{'s' if h2h_draws > 1 else ''}. "
    
    # Ajouter une prediction de score si disponible
    if score_prediction:
        narrative += f"\n\nNotre modèle prédit un score probable de {score_prediction['score']}, "
        narrative += f"avec une confiance de {score_prediction['probability']}%. "
    
    # Ajouter un conseil de pari
    if prediction == 'Victoire à domicile' and home_form['form_trend'] == 'positive':
        narrative += f"\n\nConseil de pari: Victoire de {home_team} semble être une option solide avec un bon ratio risque/récompense."
    elif prediction == 'Victoire à l\'extérieur' and away_form['form_trend'] == 'positive':
        narrative += f"\n\nConseil de pari: Victoire de {away_team} à l'extérieur pourrait offrir une valeur intéressante étant donné leur forme actuelle."
    elif prediction == 'Match nul':
        narrative += "\n\nConseil de pari: Le match nul semble être une option à considérer vu l'équilibre des forces."
    else:
        # Conseils basés sur les scénarios de but
        if _calculate_both_teams_score(home_stats, away_stats) > 60:
            narrative += "\n\nConseil de pari: 'Les deux équipes marquent' semble être une option intéressante pour ce match."
        elif _calculate_over_under_probability(home_stats, away_stats, 2.5, 'over') > 60:
            narrative += "\n\nConseil de pari: Le marché 'Plus de 2.5 buts' pourrait offrir une bonne opportunité."
    
    return narrative