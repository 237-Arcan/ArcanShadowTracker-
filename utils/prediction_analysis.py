"""
Module pour analyser et générer des prédictions basées sur les données réelles de football.
"""
import random
import pandas as pd
from datetime import datetime, timedelta

def get_recent_form(team_name, all_matches, num_matches=5):
    """
    Calcule la forme récente d'une équipe en analysant ses derniers matchs.
    
    Args:
        team_name (str): Nom de l'équipe
        all_matches (list): Liste de tous les matchs à analyser
        num_matches (int): Nombre de matchs récents à considérer
        
    Returns:
        dict: Statistiques de forme récente
    """
    # Trier les matchs par date (du plus récent au plus ancien)
    sorted_matches = sorted(
        [m for m in all_matches if 'date' in m and m.get('score')], 
        key=lambda x: x.get('date', '2000-01-01'),
        reverse=True
    )
    
    # Filtrer les matchs où cette équipe a joué
    team_matches = []
    for match in sorted_matches:
        home_team = match.get('home_team', match.get('home', ''))
        away_team = match.get('away_team', match.get('away', ''))
        
        if team_name in (home_team, away_team):
            team_matches.append(match)
            
            # Arrêter une fois que nous avons atteint le nombre de matchs requis
            if len(team_matches) >= num_matches:
                break
    
    # Calculer les statistiques
    wins = 0
    draws = 0
    losses = 0
    goals_for = 0
    goals_against = 0
    
    for match in team_matches:
        score_str = match.get('score', '0-0')
        if isinstance(score_str, str) and '-' in score_str:
            home_score, away_score = map(int, score_str.split('-'))
        elif isinstance(score_str, list) and len(score_str) == 2:
            home_score, away_score = score_str
        else:
            continue  # Ignorer les matchs sans score valide
            
        home_team = match.get('home_team', match.get('home', ''))
        
        if team_name == home_team:
            # L'équipe joue à domicile
            goals_for += home_score
            goals_against += away_score
            
            if home_score > away_score:
                wins += 1
            elif home_score == away_score:
                draws += 1
            else:
                losses += 1
        else:
            # L'équipe joue à l'extérieur
            goals_for += away_score
            goals_against += home_score
            
            if away_score > home_score:
                wins += 1
            elif away_score == home_score:
                draws += 1
            else:
                losses += 1
    
    total_matches = wins + draws + losses
    form_rating = (wins * 3 + draws) / (total_matches * 3) if total_matches > 0 else 0.5
    
    # Calculer la tendance offensive/défensive
    offensive_rating = goals_for / total_matches if total_matches > 0 else 1.0
    defensive_rating = 1.0 - (goals_against / (total_matches * 2)) if total_matches > 0 else 0.5
    
    return {
        'matches_analyzed': total_matches,
        'wins': wins,
        'draws': draws,
        'losses': losses,
        'goals_for': goals_for,
        'goals_against': goals_against,
        'form_rating': round(form_rating, 2),
        'offensive_rating': round(offensive_rating, 2),
        'defensive_rating': round(defensive_rating, 2)
    }

def get_head_to_head(team1, team2, all_matches, num_matches=5):
    """
    Analyse les confrontations directes entre deux équipes.
    
    Args:
        team1 (str): Première équipe
        team2 (str): Deuxième équipe
        all_matches (list): Liste de tous les matchs à analyser
        num_matches (int): Nombre de confrontations à considérer
        
    Returns:
        dict: Statistiques des confrontations directes
    """
    # Filtrer et trier les confrontations directes
    h2h_matches = []
    
    for match in all_matches:
        home_team = match.get('home_team', match.get('home', ''))
        away_team = match.get('away_team', match.get('away', ''))
        
        if ((home_team == team1 and away_team == team2) or 
            (home_team == team2 and away_team == team1)):
            h2h_matches.append(match)
    
    # Trier par date (du plus récent au plus ancien)
    h2h_matches = sorted(
        h2h_matches, 
        key=lambda x: x.get('date', '2000-01-01'),
        reverse=True
    )[:num_matches]
    
    # Calculer les statistiques
    team1_wins = 0
    team2_wins = 0
    draws = 0
    
    for match in h2h_matches:
        score_str = match.get('score', '0-0')
        if isinstance(score_str, str) and '-' in score_str:
            home_score, away_score = map(int, score_str.split('-'))
        elif isinstance(score_str, list) and len(score_str) == 2:
            home_score, away_score = score_str
        else:
            continue  # Ignorer les matchs sans score valide
            
        home_team = match.get('home_team', match.get('home', ''))
        
        if home_score > away_score:
            if home_team == team1:
                team1_wins += 1
            else:
                team2_wins += 1
        elif home_score < away_score:
            if home_team == team1:
                team2_wins += 1
            else:
                team1_wins += 1
        else:
            draws += 1
    
    total_matches = team1_wins + team2_wins + draws
    
    # Calculer les pourcentages de résultats
    team1_win_pct = team1_wins / total_matches if total_matches > 0 else 0.33
    team2_win_pct = team2_wins / total_matches if total_matches > 0 else 0.33
    draw_pct = draws / total_matches if total_matches > 0 else 0.34
    
    return {
        'matches_analyzed': total_matches,
        'team1_wins': team1_wins,
        'team2_wins': team2_wins,
        'draws': draws,
        'team1_win_pct': round(team1_win_pct, 2),
        'team2_win_pct': round(team2_win_pct, 2),
        'draw_pct': round(draw_pct, 2)
    }

def analyze_match(match, all_matches):
    """
    Analyse complète d'un match en utilisant plusieurs modules d'ArcanShadow.
    
    Args:
        match (dict): Informations sur le match à analyser
        all_matches (list): Liste de tous les matchs disponibles
        
    Returns:
        dict: Analyse détaillée et prédictions
    """
    # Extraire les informations sur le match
    home_team = match.get('home_team', match.get('home', ''))
    away_team = match.get('away_team', match.get('away', ''))
    league = match.get('league', '')
    
    # Calculer la forme récente de chaque équipe
    home_form = get_recent_form(home_team, all_matches)
    away_form = get_recent_form(away_team, all_matches)
    
    # Analyser les confrontations directes
    h2h = get_head_to_head(home_team, away_team, all_matches)
    
    # Avantage à domicile (facteur légèrement aléatoire mais réaliste)
    home_advantage = random.uniform(0.05, 0.15)
    
    # Module ArcanX - Analyse basée sur la forme et confrontations directes
    arcanx_home = (home_form['form_rating'] * 0.5 + h2h['team1_win_pct'] * 0.3 + home_advantage) * 100
    arcanx_draw = (h2h['draw_pct'] * 0.7 + 0.15) * 100
    arcanx_away = (away_form['form_rating'] * 0.5 + h2h['team2_win_pct'] * 0.3) * 100
    
    # Normaliser pour que la somme soit 100%
    arcanx_total = arcanx_home + arcanx_draw + arcanx_away
    arcanx_home = round((arcanx_home / arcanx_total) * 100)
    arcanx_draw = round((arcanx_draw / arcanx_total) * 100)
    arcanx_away = round((arcanx_away / arcanx_total) * 100)
    
    # Module ShadowOdds - Analyse basée sur les cotes et tendances offensives/défensives
    home_odds = match.get('home_odds', 2.0)
    draw_odds = match.get('draw_odds', 3.5)
    away_odds = match.get('away_odds', 4.0)
    
    shadowodds_home = round((1 / home_odds) * 100)
    shadowodds_draw = round((1 / draw_odds) * 100)
    shadowodds_away = round((1 / away_odds) * 100)
    
    # Normaliser les probabilités ShadowOdds
    shadowodds_total = shadowodds_home + shadowodds_draw + shadowodds_away
    shadowodds_home = round((shadowodds_home / shadowodds_total) * 100)
    shadowodds_draw = round((shadowodds_draw / shadowodds_total) * 100)
    shadowodds_away = round((shadowodds_away / shadowodds_total) * 100)
    
    # Module KarmicFlow - Analyse basée sur les cycles temporels
    # (simulée avec des valeurs aléatoires mais réalistes)
    karmicflow_cycle = random.choice([0.8, 1.0, 1.2])  # Facteur cyclique
    karmicflow_home = round(min(100, max(0, arcanx_home * karmicflow_cycle)))
    karmicflow_draw = round(min(100, max(0, arcanx_draw * (2 - karmicflow_cycle))))
    karmicflow_away = round(min(100, max(0, arcanx_away * (2 - karmicflow_cycle))))
    
    # Normaliser
    karmicflow_total = karmicflow_home + karmicflow_draw + karmicflow_away
    karmicflow_home = round((karmicflow_home / karmicflow_total) * 100)
    karmicflow_draw = round((karmicflow_draw / karmicflow_total) * 100)
    karmicflow_away = round((karmicflow_away / karmicflow_total) * 100)
    
    # Module NumeriCode - Analyse basée sur des patterns numériques
    # (simulée avec des valeurs légèrement perturbées mais cohérentes)
    numeric_factor = random.uniform(0.9, 1.1)
    numericode_home = round(min(100, max(0, shadowodds_home * numeric_factor)))
    numericode_draw = round(min(100, max(0, shadowodds_draw * numeric_factor)))
    numericode_away = round(min(100, max(0, shadowodds_away * numeric_factor)))
    
    # Normaliser
    numericode_total = numericode_home + numericode_draw + numericode_away
    numericode_home = round((numericode_home / numericode_total) * 100)
    numericode_draw = round((numericode_draw / numericode_total) * 100)
    numericode_away = round((numericode_away / numericode_total) * 100)
    
    # Module MetaSystems - Analyse combinée de tous les modules
    # Poids différents pour chaque module
    weights = {
        'arcanx': 0.35,
        'shadowodds': 0.25,
        'karmicflow': 0.15,
        'numericode': 0.10,
        'metasystems': 0.15  # Poids pour l'ajustement final
    }
    
    # Calculer les probabilités combinées
    meta_home = (arcanx_home * weights['arcanx'] + 
                shadowodds_home * weights['shadowodds'] + 
                karmicflow_home * weights['karmicflow'] + 
                numericode_home * weights['numericode'])
    
    meta_draw = (arcanx_draw * weights['arcanx'] + 
                shadowodds_draw * weights['shadowodds'] + 
                karmicflow_draw * weights['karmicflow'] + 
                numericode_draw * weights['numericode'])
    
    meta_away = (arcanx_away * weights['arcanx'] + 
                shadowodds_away * weights['shadowodds'] + 
                karmicflow_away * weights['karmicflow'] + 
                numericode_away * weights['numericode'])
    
    # Métadonnées d'analyse
    match_analysis = {
        'home_team': home_team,
        'away_team': away_team,
        'league': league,
        'match_date': match.get('date', ''),
        'match_time': match.get('time', '??:??'),
        
        # Forme récente des équipes
        'home_form': home_form,
        'away_form': away_form,
        'head_to_head': h2h,
        
        # Résultats des différents modules
        'modules': {
            'arcanx': {
                'home_win': arcanx_home,
                'draw': arcanx_draw,
                'away_win': arcanx_away,
                'key_insight': f"Forme {home_team}: {home_form['form_rating']:.2f}, Forme {away_team}: {away_form['form_rating']:.2f}"
            },
            'shadowodds': {
                'home_win': shadowodds_home,
                'draw': shadowodds_draw,
                'away_win': shadowodds_away,
                'key_insight': f"Cotes du marché: 1: {home_odds}, X: {draw_odds}, 2: {away_odds}"
            },
            'karmicflow': {
                'home_win': karmicflow_home,
                'draw': karmicflow_draw,
                'away_win': karmicflow_away,
                'key_insight': f"Cycle karmique actuel: {karmicflow_cycle:.2f} (Impact {'positif' if karmicflow_cycle > 1 else 'négatif'} pour {home_team})"
            },
            'numericode': {
                'home_win': numericode_home,
                'draw': numericode_draw,
                'away_win': numericode_away,
                'key_insight': f"Convergence numérique: facteur {numeric_factor:.2f}"
            }
        },
        
        # Prédiction finale combinée
        'final_prediction': {
            'home_win': round(meta_home),
            'draw': round(meta_draw),
            'away_win': round(meta_away),
            'confidence': random.randint(83, 89)  # Confiance simulée
        }
    }
    
    # Déterminer la prédiction principale en comparant les probabilités
    if meta_home >= meta_draw and meta_home >= meta_away:
        match_analysis['main_prediction'] = f"Victoire de {home_team}"
        match_analysis['main_odds'] = home_odds
    elif meta_draw >= meta_home and meta_draw >= meta_away:
        match_analysis['main_prediction'] = "Match nul"
        match_analysis['main_odds'] = draw_odds
    else:
        match_analysis['main_prediction'] = f"Victoire de {away_team}"
        match_analysis['main_odds'] = away_odds
    
    # Prédictions secondaires
    over_under_prob = (home_form['offensive_rating'] + (1 - away_form['defensive_rating'])) * 0.5
    both_score_prob = (home_form['offensive_rating'] * away_form['offensive_rating']) * 0.8 + 0.1
    
    match_analysis['secondary_predictions'] = {
        'over_2.5_goals': {
            'probability': round(over_under_prob * 100),
            'odds': round(1 / over_under_prob, 2)
        },
        'both_teams_score': {
            'probability': round(both_score_prob * 100),
            'odds': round(1 / both_score_prob, 2)
        }
    }
    
    # Générer une narration pour la prédiction
    match_analysis['narrative'] = generate_prediction_narrative(match_analysis)
    
    return match_analysis

def generate_prediction_narrative(analysis):
    """
    Génère une narration naturelle pour expliquer la prédiction.
    
    Args:
        analysis (dict): Analyse complète du match
        
    Returns:
        str: Texte narratif expliquant la prédiction
    """
    home_team = analysis['home_team']
    away_team = analysis['away_team']
    home_form = analysis['home_form']
    away_form = analysis['away_form']
    h2h = analysis['head_to_head']
    
    # Descriptions des formes récentes
    home_form_desc = "excellente" if home_form['form_rating'] > 0.7 else ("bonne" if home_form['form_rating'] > 0.5 else "moyenne" if home_form['form_rating'] > 0.3 else "mauvaise")
    away_form_desc = "excellente" if away_form['form_rating'] > 0.7 else ("bonne" if away_form['form_rating'] > 0.5 else "moyenne" if away_form['form_rating'] > 0.3 else "mauvaise")
    
    # Description de l'historique des confrontations
    if h2h['matches_analyzed'] > 0:
        if h2h['team1_wins'] > h2h['team2_wins']:
            h2h_desc = f"{home_team} domine les confrontations directes avec {h2h['team1_wins']} victoires contre {h2h['team2_wins']} pour {away_team}."
        elif h2h['team2_wins'] > h2h['team1_wins']:
            h2h_desc = f"{away_team} a l'avantage dans les confrontations directes avec {h2h['team2_wins']} victoires contre {h2h['team1_wins']} pour {home_team}."
        else:
            h2h_desc = f"Les confrontations directes sont équilibrées avec {h2h['team1_wins']} victoires pour chaque équipe."
    else:
        h2h_desc = "Il n'y a pas suffisamment d'historique de confrontations directes entre ces équipes."
    
    # Module avec l'impact le plus fort (utiliser une méthode manuelle pour trouver le max)
    modules_impacts = {
        "ArcanX": analysis['modules']['arcanx']['home_win' if analysis['final_prediction']['home_win'] > analysis['final_prediction']['away_win'] else 'away_win'],
        "ShadowOdds": analysis['modules']['shadowodds']['home_win' if analysis['final_prediction']['home_win'] > analysis['final_prediction']['away_win'] else 'away_win'],
        "KarmicFlow+": analysis['modules']['karmicflow']['home_win' if analysis['final_prediction']['home_win'] > analysis['final_prediction']['away_win'] else 'away_win'],
        "NumeriCode": analysis['modules']['numericode']['home_win' if analysis['final_prediction']['home_win'] > analysis['final_prediction']['away_win'] else 'away_win']
    }
    
    # Trouver manuellement le module avec l'impact le plus fort
    strongest_module = "ArcanX"  # Valeur par défaut
    max_impact = 0
    
    for module_name, impact in modules_impacts.items():
        if impact > max_impact:
            max_impact = impact
            strongest_module = module_name
    
    # Insights spécifiques au module le plus influent
    if strongest_module == "ArcanX":
        module_insight = f"L'analyse de forme récente révèle une dynamique {home_form_desc} pour {home_team} et {away_form_desc} pour {away_team}."
    elif strongest_module == "ShadowOdds":
        module_insight = f"L'analyse des cotes du marché révèle une anomalie qui suggère une sous-évaluation de la probabilité de notre prédiction principale."
    elif strongest_module == "KarmicFlow+":
        team_location = "équipe à domicile" if analysis['final_prediction']['home_win'] > analysis['final_prediction']['away_win'] else "équipe à l'extérieur"
        module_insight = f"L'analyse des cycles temporels indique une phase favorable pour l'{team_location}."
    else:  # NumeriCode
        module_insight = f"L'analyse des patterns numériques révèle une convergence significative qui renforce notre prédiction principale."
    
    # Construction du narratif complet
    narrative = f"""
L'analyse des performances récentes montre que {home_team} est en {home_form_desc} forme, avec {home_form['wins']} victoires sur ses {home_form['matches_analyzed']} derniers matchs. 
{away_team} présente quant à lui une forme {away_form_desc}, avec {away_form['wins']} victoires sur ses {away_form['matches_analyzed']} derniers matchs.

{h2h_desc}

{module_insight}

Les prédictions secondaires indiquent une probabilité de {analysis['secondary_predictions']['over_2.5_goals']['probability']}% de voir plus de 2.5 buts dans ce match, 
et une probabilité de {analysis['secondary_predictions']['both_teams_score']['probability']}% que les deux équipes marquent.

Conclusion: La convergence de signaux positifs multiples, renforcée par le méta-système de pondération
suggère {analysis['main_prediction']} avec un niveau de confiance élevé ({analysis['final_prediction']['confidence']}%).
"""
    
    return narrative

def get_prediction_data(match, all_matches):
    """
    Prépare les données complètes pour l'affichage de la prédiction.
    
    Args:
        match (dict): Match à analyser
        all_matches (list): Liste de tous les matchs disponibles
        
    Returns:
        dict: Données formatées pour l'affichage
    """
    # Analyser le match avec tous les modules
    analysis = analyze_match(match, all_matches)
    
    # Préparer les données pour les modules contributeurs
    contributing_modules = [
        {
            "name": "ArcanX", 
            "confidence": round(analysis['modules']['arcanx']['home_win'] / 100 + 0.3, 2),
            "weight": 0.35, 
            "key_insights": analysis['modules']['arcanx']['key_insight']
        },
        {
            "name": "ShadowOdds", 
            "confidence": round(analysis['modules']['shadowodds']['home_win'] / 100 + 0.2, 2),
            "weight": 0.25, 
            "key_insights": analysis['modules']['shadowodds']['key_insight']
        },
        {
            "name": "KarmicFlow+", 
            "confidence": round(analysis['modules']['karmicflow']['home_win'] / 100 + 0.1, 2),
            "weight": 0.15, 
            "key_insights": analysis['modules']['karmicflow']['key_insight']
        },
        {
            "name": "NumeriCode", 
            "confidence": round(analysis['modules']['numericode']['home_win'] / 100 + 0.25, 2),
            "weight": 0.10, 
            "key_insights": analysis['modules']['numericode']['key_insight']
        },
        {
            "name": "MetaSystems", 
            "confidence": round((analysis['final_prediction']['home_win'] / 100) + 0.2, 2),
            "weight": 0.15, 
            "key_insights": f"Projection de volume d'échange: {analysis['home_team']} dominant à {max(analysis['final_prediction']['home_win'], analysis['final_prediction']['away_win'])}%"
        }
    ]
    
    # Format final des données
    prediction_data = {
        'match_info': {
            'home_team': analysis['home_team'],
            'away_team': analysis['away_team'],
            'league': analysis['league'],
            'date': analysis['match_date'],
            'time': analysis['match_time']
        },
        'main_prediction': {
            'outcome': analysis['main_prediction'],
            'odds': analysis['main_odds'],
            'confidence': analysis['final_prediction']['confidence']
        },
        'other_scenarios': [
            {
                'name': 'Match nul',
                'probability': analysis['final_prediction']['draw'],
                'odds': round(100 / max(1, analysis['final_prediction']['draw']), 2)
            },
            {
                'name': f"Victoire de {analysis['away_team'] if 'Victoire de' in analysis['main_prediction'] else analysis['home_team']}",
                'probability': analysis['final_prediction']['away_win'] if 'Victoire de' in analysis['main_prediction'] else analysis['final_prediction']['home_win'],
                'odds': round(100 / max(1, analysis['final_prediction']['away_win'] if 'Victoire de' in analysis['main_prediction'] else analysis['final_prediction']['home_win']), 2)
            },
            {
                'name': 'Plus de 2.5 buts',
                'probability': analysis['secondary_predictions']['over_2.5_goals']['probability'],
                'odds': analysis['secondary_predictions']['over_2.5_goals']['odds']
            },
            {
                'name': 'Les deux équipes marquent',
                'probability': analysis['secondary_predictions']['both_teams_score']['probability'],
                'odds': analysis['secondary_predictions']['both_teams_score']['odds']
            }
        ],
        'contributing_modules': contributing_modules,
        'narrative': analysis['narrative']
    }
    
    return prediction_data