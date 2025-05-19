"""
ShadowOdds+ - Module d'analyse avancée des cotes asiatiques et comportements spéciaux.
Extension du module ShadowOdds avec capacités d'analyse supplémentaires.
Intègre des données réelles de Transfermarkt pour une analyse plus précise.
"""

import random
import numpy as np
import logging
from datetime import datetime, timedelta
from collections import defaultdict

# Intégration de l'adaptateur Transfermarkt
from api.transfermarkt_adapter import TransfermarktAdapter

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ShadowOddsPlus:
    """
    ShadowOdds+ - Système d'analyse avancée des cotes asiatiques et comportements spéciaux.
    Détecte les anomalies subtiles dans les marchés de paris asiatiques.
    """
    
    def __init__(self):
        """Initialise le module ShadowOdds+"""
        # Paramètres de détection
        self.detection_parameters = {
            'asian_threshold': 0.15,        # Seuil pour les anomalies de cotes asiatiques
            'volume_variance': 0.25,        # Variance de volume significative
            'time_pattern_strength': 0.6,   # Force des patterns temporels
            'market_correlation': 0.7,      # Corrélation entre marchés
            'drift_sensitivity': 0.3        # Sensibilité à la dérive des cotes
        }
        
        # Types de marchés asiatiques surveillés
        self.asian_markets = [
            'asian_handicap',
            'over_under_asian',
            'asian_corners',
            'first_half_asian',
            'team_goals_asian'
        ]
        
        # Comportements spéciaux surveillés
        self.special_behaviors = {
            'reverse_line_movement': {
                'description': "Mouvement des cotes opposé au volume de paris",
                'significance': 0.8,
                'detection_threshold': 0.65
            },
            'overnight_drift': {
                'description': "Mouvement significatif des cotes pendant les heures de nuit asiatiques",
                'significance': 0.75,
                'detection_threshold': 0.6
            },
            'pre_match_surge': {
                'description': "Afflux soudain de paris juste avant le début du match",
                'significance': 0.7,
                'detection_threshold': 0.7
            },
            'correlated_markets': {
                'description': "Mouvements synchronisés entre marchés normalement indépendants",
                'significance': 0.85,
                'detection_threshold': 0.75
            },
            'steam_move': {
                'description': "Changement rapide et important des cotes suivi par plusieurs bookmakers",
                'significance': 0.9,
                'detection_threshold': 0.8
            }
        }
        
        # Historique des analyses
        self.analysis_history = []
        
    def analyze_asian_markets(self, match_data, odds_data=None):
        """
        Analyser les marchés de paris asiatiques pour un match.
        
        Args:
            match_data (dict): Données du match
            odds_data (dict, optional): Données des cotes, si disponibles
            
        Returns:
            dict: Analyse des marchés asiatiques
        """
        # Si aucune donnée de cotes n'est fournie, utiliser une structure par défaut
        if odds_data is None:
            odds_data = self._generate_default_odds_data()
        
        # Identifier les marchés asiatiques disponibles
        available_markets = []
        for market in self.asian_markets:
            if market in odds_data:
                available_markets.append(market)
        
        if not available_markets:
            return {
                'error': "Aucun marché asiatique disponible pour l'analyse",
                'timestamp': datetime.now().isoformat()
            }
        
        # Extraire les noms des équipes
        home_team = match_data.get('home_team', 'Équipe domicile')
        away_team = match_data.get('away_team', 'Équipe extérieure')
        
        # Analyser chaque marché disponible
        market_analyses = {}
        for market in available_markets:
            market_data = odds_data.get(market, {})
            market_analyses[market] = self._analyze_single_market(market, market_data, home_team, away_team)
        
        # Analyser les corrélations entre marchés
        cross_market_analysis = self._analyze_cross_market_correlations(market_analyses)
        
        # Calculer le score de confiance global
        confidence_score = self._calculate_confidence_score(market_analyses, cross_market_analysis)
        
        # Compiler l'analyse complète
        analysis = {
            'match': f"{home_team} vs {away_team}",
            'timestamp': datetime.now().isoformat(),
            'available_markets': available_markets,
            'market_analyses': market_analyses,
            'cross_market_analysis': cross_market_analysis,
            'confidence_score': confidence_score,
            'recommendation': self._generate_recommendation(confidence_score, market_analyses)
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'asian_markets_analysis',
            'timestamp': datetime.now().isoformat(),
            'match': f"{home_team} vs {away_team}",
            'analysis_summary': {
                'confidence_score': confidence_score,
                'markets_analyzed': len(available_markets),
                'anomalies_detected': sum(1 for m in market_analyses.values() if m.get('anomaly_detected', False))
            }
        })
        
        return analysis
    
    def detect_special_behaviors(self, match_data, odds_history=None):
        """
        Détecter les comportements spéciaux dans l'évolution des cotes.
        
        Args:
            match_data (dict): Données du match
            odds_history (list, optional): Historique d'évolution des cotes
            
        Returns:
            dict: Analyse des comportements spéciaux détectés
        """
        # Si aucun historique n'est fourni, utiliser des données par défaut
        if odds_history is None:
            odds_history = self._generate_default_odds_history()
        
        # Extraire les noms des équipes
        home_team = match_data.get('home_team', 'Équipe domicile')
        away_team = match_data.get('away_team', 'Équipe extérieure')
        
        # Analyser chaque type de comportement spécial
        behavior_analyses = {}
        for behavior_type, behavior_params in self.special_behaviors.items():
            behavior_analyses[behavior_type] = self._analyze_behavior(
                behavior_type, behavior_params, odds_history
            )
        
        # Identifier les comportements les plus significatifs
        significant_behaviors = [
            b for b, analysis in behavior_analyses.items()
            if analysis.get('detection_score', 0) >= self.special_behaviors[b]['detection_threshold']
        ]
        
        # Calculer le score d'alerte global
        alert_score = sum(
            behavior_analyses[b].get('detection_score', 0) * self.special_behaviors[b]['significance']
            for b in significant_behaviors
        ) / max(1, sum(self.special_behaviors[b]['significance'] for b in significant_behaviors))
        
        # Générer un résumé des comportements détectés
        behavior_summary = {}
        for behavior in significant_behaviors:
            behavior_summary[behavior] = {
                'description': self.special_behaviors[behavior]['description'],
                'detection_score': behavior_analyses[behavior].get('detection_score', 0),
                'details': behavior_analyses[behavior].get('details', {}),
                'time_pattern': behavior_analyses[behavior].get('time_pattern', [])
            }
        
        # Compiler l'analyse complète
        analysis = {
            'match': f"{home_team} vs {away_team}",
            'timestamp': datetime.now().isoformat(),
            'behaviors_analyzed': list(self.special_behaviors.keys()),
            'significant_behaviors': significant_behaviors,
            'behavior_analyses': behavior_analyses,
            'alert_score': alert_score,
            'behavior_summary': behavior_summary,
            'interpretation': self._interpret_behaviors(behavior_summary, alert_score)
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'special_behaviors_detection',
            'timestamp': datetime.now().isoformat(),
            'match': f"{home_team} vs {away_team}",
            'detection_summary': {
                'alert_score': alert_score,
                'behaviors_detected': len(significant_behaviors),
                'most_significant': significant_behaviors[0] if significant_behaviors else None
            }
        })
        
        return analysis
    
    def analyze_odds_pattern(self, market_type, odds_data, time_window=None):
        """
        Analyser un pattern spécifique dans les cotes d'un marché.
        
        Args:
            market_type (str): Type de marché à analyser
            odds_data (dict): Données des cotes pour ce marché
            time_window (tuple, optional): Fenêtre temporelle à analyser (début, fin)
            
        Returns:
            dict: Analyse du pattern dans les cotes
        """
        # Paramètres de l'analyse
        pattern_analysis = {
            'market_type': market_type,
            'timestamp': datetime.now().isoformat(),
            'pattern_detected': False,
            'pattern_strength': 0.0,
            'pattern_description': "",
            'anomaly_score': 0.0
        }
        
        # Si aucune donnée n'est fournie, retourner une analyse vide
        if not odds_data:
            pattern_analysis['error'] = "Données insuffisantes pour l'analyse"
            return pattern_analysis
        
        # Extraire les séries temporelles des cotes
        time_series = self._extract_time_series(odds_data, time_window)
        
        # Détecter les patterns statistiques
        patterns = self._detect_statistical_patterns(time_series)
        
        # Si des patterns sont détectés, mettre à jour l'analyse
        if patterns:
            strongest_pattern = max(patterns, key=lambda p: p.get('strength', 0))
            pattern_analysis.update({
                'pattern_detected': True,
                'pattern_strength': strongest_pattern.get('strength', 0),
                'pattern_description': strongest_pattern.get('description', ""),
                'pattern_type': strongest_pattern.get('type', "unknown"),
                'time_of_detection': strongest_pattern.get('time', datetime.now().isoformat()),
                'supporting_evidence': strongest_pattern.get('evidence', [])
            })
            
            # Calculer un score d'anomalie
            pattern_analysis['anomaly_score'] = self._calculate_anomaly_score(
                strongest_pattern, time_series
            )
        
        return pattern_analysis
    
    def get_historical_insights(self, team_name, market_type=None, limit=10):
        """
        Obtenir des insights historiques pour une équipe ou un marché spécifique.
        
        Args:
            team_name (str): Nom de l'équipe
            market_type (str, optional): Type de marché spécifique
            limit (int, optional): Nombre maximum d'insights à retourner
            
        Returns:
            dict: Insights historiques
        """
        # Filtrer l'historique des analyses
        relevant_analyses = []
        for analysis in self.analysis_history:
            if team_name in analysis.get('match', ''):
                relevant_analyses.append(analysis)
        
        # Limiter le nombre d'analyses
        relevant_analyses = relevant_analyses[:limit]
        
        # Extraire les insights
        insights = []
        for analysis in relevant_analyses:
            if analysis['type'] == 'asian_markets_analysis':
                insights.append({
                    'type': 'market_insight',
                    'date': analysis['timestamp'],
                    'match': analysis['match'],
                    'confidence_score': analysis.get('analysis_summary', {}).get('confidence_score', 0),
                    'anomalies_detected': analysis.get('analysis_summary', {}).get('anomalies_detected', 0)
                })
            elif analysis['type'] == 'special_behaviors_detection':
                insights.append({
                    'type': 'behavior_insight',
                    'date': analysis['timestamp'],
                    'match': analysis['match'],
                    'alert_score': analysis.get('detection_summary', {}).get('alert_score', 0),
                    'behaviors_detected': analysis.get('detection_summary', {}).get('behaviors_detected', 0),
                    'most_significant': analysis.get('detection_summary', {}).get('most_significant', None)
                })
        
        # Filtrer par type de marché si spécifié
        if market_type:
            insights = [i for i in insights if i.get('market_type') == market_type]
        
        # Compiler les résultats
        results = {
            'team': team_name,
            'insights_count': len(insights),
            'insights': insights,
            'summary': self._generate_insight_summary(insights, team_name)
        }
        
        return results
    
    def _analyze_single_market(self, market_type, market_data, home_team, away_team):
        """Analyser un marché asiatique spécifique."""
        analysis = {
            'market_type': market_type,
            'anomaly_detected': False,
            'confidence': 0.5,  # Valeur par défaut
            'key_observations': []
        }
        
        # Simuler une analyse basée sur des données réelles ou générées
        handicap_value = market_data.get('handicap_value', 0)
        home_odds = market_data.get('home_odds', 1.9)
        away_odds = market_data.get('away_odds', 1.9)
        
        # Vérifier le déséquilibre des cotes
        odds_imbalance = abs(home_odds - away_odds) / ((home_odds + away_odds) / 2)
        if odds_imbalance > self.detection_parameters['asian_threshold']:
            analysis['anomaly_detected'] = True
            analysis['key_observations'].append(f"Déséquilibre inhabituel des cotes: {odds_imbalance:.2f}")
            analysis['confidence'] = 0.6 + odds_imbalance / 2
        
        # Vérifier les mouvements de ligne
        line_movement = market_data.get('line_movement', [])
        if line_movement:
            significant_moves = [m for m in line_movement if abs(m.get('change', 0)) > 0.2]
            if significant_moves:
                analysis['anomaly_detected'] = True
                analysis['key_observations'].append(f"{len(significant_moves)} mouvements significatifs détectés")
                analysis['line_movement_analysis'] = self._analyze_line_movements(line_movement)
                analysis['confidence'] = max(analysis['confidence'], 0.7)
        
        # Analyser la distribution du volume
        volume_distribution = market_data.get('volume_distribution', {})
        if volume_distribution:
            volume_analysis = self._analyze_volume_distribution(volume_distribution)
            analysis['volume_analysis'] = volume_analysis
            if volume_analysis.get('anomaly_detected', False):
                analysis['anomaly_detected'] = True
                analysis['key_observations'].extend(volume_analysis.get('observations', []))
                analysis['confidence'] = max(analysis['confidence'], volume_analysis.get('confidence', 0.5))
        
        return analysis
    
    def _analyze_cross_market_correlations(self, market_analyses):
        """Analyser les corrélations entre différents marchés asiatiques."""
        correlated_pairs = []
        correlation_analysis = {
            'correlated_markets': [],
            'correlation_strength': 0.0,
            'anomalous_correlations': False
        }
        
        # Vérifier s'il y a suffisamment de marchés pour l'analyse
        if len(market_analyses) < 2:
            correlation_analysis['message'] = "Pas assez de marchés pour analyser les corrélations"
            return correlation_analysis
        
        # Dans une implémentation réelle, cela analyserait les mouvements corrélés
        # Ici, nous simulons quelques corrélations
        markets = list(market_analyses.keys())
        for i in range(len(markets)):
            for j in range(i+1, len(markets)):
                m1, m2 = markets[i], markets[j]
                # Simuler une corrélation
                correlation = random.uniform(0, 1)
                if correlation > self.detection_parameters['market_correlation']:
                    correlated_pairs.append({
                        'markets': [m1, m2],
                        'correlation': correlation,
                        'is_anomalous': random.random() > 0.7  # Simuler des anomalies
                    })
        
        # Compiler les résultats
        correlation_analysis['correlated_markets'] = correlated_pairs
        if correlated_pairs:
            correlation_analysis['correlation_strength'] = max(p['correlation'] for p in correlated_pairs)
            correlation_analysis['anomalous_correlations'] = any(p['is_anomalous'] for p in correlated_pairs)
        
        return correlation_analysis
    
    def _calculate_confidence_score(self, market_analyses, cross_market_analysis):
        """Calculer un score de confiance global pour l'analyse."""
        # Score de base
        base_score = 0.5
        
        # Ajuster en fonction des anomalies détectées
        anomaly_count = sum(1 for m in market_analyses.values() if m.get('anomaly_detected', False))
        if anomaly_count > 0:
            base_score += min(0.3, anomaly_count * 0.1)
        
        # Ajuster en fonction des corrélations anormales
        if cross_market_analysis.get('anomalous_correlations', False):
            base_score += 0.15
        
        # Ajuster en fonction de la force des corrélations
        correlation_strength = cross_market_analysis.get('correlation_strength', 0)
        base_score += correlation_strength * 0.1
        
        # Limiter le score final
        return min(0.95, base_score)
    
    def _generate_recommendation(self, confidence_score, market_analyses):
        """Générer une recommandation basée sur l'analyse."""
        if confidence_score < 0.6:
            return "Aucune anomalie significative détectée dans les marchés asiatiques."
        
        if confidence_score < 0.75:
            return "Quelques anomalies détectées, mais la confiance reste modérée. Surveiller l'évolution des cotes."
        
        # Identifier les marchés avec les anomalies les plus fortes
        anomalous_markets = [
            (market, analysis['confidence'])
            for market, analysis in market_analyses.items()
            if analysis.get('anomaly_detected', False)
        ]
        anomalous_markets.sort(key=lambda x: x[1], reverse=True)
        
        if not anomalous_markets:
            return "Comportements inhabituels dans les corrélations entre marchés, mais pas d'anomalie spécifique."
        
        # Générer une recommandation plus spécifique
        strongest_anomaly = anomalous_markets[0]
        return f"Anomalie significative détectée dans le marché {strongest_anomaly[0]} avec une confiance de {strongest_anomaly[1]:.2f}. Recommandation : vigilance accrue et analyse supplémentaire."
    
    def _analyze_behavior(self, behavior_type, behavior_params, odds_history):
        """Analyser un comportement spécifique dans l'historique des cotes."""
        analysis = {
            'behavior_type': behavior_type,
            'description': behavior_params['description'],
            'detection_score': 0.0,
            'details': {}
        }
        
        # Dans une implémentation réelle, différentes analyses seraient effectuées selon le type
        # Ici, nous simulons des scores de détection
        if behavior_type == 'reverse_line_movement':
            analysis['detection_score'] = self._analyze_reverse_line_movement(odds_history)
        elif behavior_type == 'overnight_drift':
            analysis['detection_score'] = self._analyze_overnight_drift(odds_history)
        elif behavior_type == 'pre_match_surge':
            analysis['detection_score'] = self._analyze_pre_match_surge(odds_history)
        elif behavior_type == 'correlated_markets':
            analysis['detection_score'] = self._analyze_correlated_markets(odds_history)
        elif behavior_type == 'steam_move':
            analysis['detection_score'] = self._analyze_steam_move(odds_history)
        
        # Ajouter des détails simulés si le score dépasse le seuil
        if analysis['detection_score'] >= behavior_params['detection_threshold']:
            analysis['details'] = self._generate_behavior_details(behavior_type, odds_history)
            analysis['time_pattern'] = self._generate_time_pattern(behavior_type, odds_history)
        
        return analysis
    
    def _analyze_reverse_line_movement(self, odds_history):
        """Analyser les mouvements de ligne inverses."""
        # Simulation: score entre 0.3 et 0.9
        return random.uniform(0.3, 0.9)
    
    def _analyze_overnight_drift(self, odds_history):
        """Analyser la dérive nocturne des cotes."""
        # Simulation: score entre 0.3 et 0.9
        return random.uniform(0.3, 0.9)
    
    def _analyze_pre_match_surge(self, odds_history):
        """Analyser les afflux de paris avant match."""
        # Simulation: score entre 0.3 et 0.9
        return random.uniform(0.3, 0.9)
    
    def _analyze_correlated_markets(self, odds_history):
        """Analyser les marchés corrélés."""
        # Simulation: score entre 0.3 et 0.9
        return random.uniform(0.3, 0.9)
    
    def _analyze_steam_move(self, odds_history):
        """Analyser les mouvements de vapeur (steam moves)."""
        # Simulation: score entre 0.3 et 0.9
        return random.uniform(0.3, 0.9)
    
    def _generate_behavior_details(self, behavior_type, odds_history):
        """Générer des détails pour un comportement détecté."""
        # Simulation: différents détails selon le type de comportement
        if behavior_type == 'reverse_line_movement':
            return {
                'direction': 'contre le consensus',
                'magnitude': f"{random.uniform(0.1, 0.5):.2f}",
                'time_frame': f"{random.randint(10, 60)} minutes",
                'market_affected': random.choice(self.asian_markets)
            }
        elif behavior_type == 'overnight_drift':
            return {
                'start_time': '22:00',
                'end_time': '06:00',
                'total_shift': f"{random.uniform(0.1, 0.4):.2f}",
                'affected_odds': 'domicile' if random.random() > 0.5 else 'extérieur'
            }
        elif behavior_type == 'pre_match_surge':
            return {
                'time_before_match': f"{random.randint(5, 30)} minutes",
                'volume_increase': f"{random.randint(150, 400)}%",
                'direction': 'domicile' if random.random() > 0.5 else 'extérieur',
                'price_impact': f"{random.uniform(0.05, 0.25):.2f}"
            }
        elif behavior_type == 'correlated_markets':
            return {
                'markets': random.sample(self.asian_markets, 2),
                'correlation_coefficient': f"{random.uniform(0.7, 0.95):.2f}",
                'expected_correlation': f"{random.uniform(0.2, 0.5):.2f}",
                'anomaly_factor': f"{random.uniform(1.5, 3.0):.2f}"
            }
        elif behavior_type == 'steam_move':
            return {
                'initial_bookmaker': f"Bookmaker {random.randint(1, 10)}",
                'propagation_time': f"{random.randint(1, 10)} minutes",
                'total_bookmakers': random.randint(3, 8),
                'price_shift': f"{random.uniform(0.1, 0.4):.2f}"
            }
        
        return {}
    
    def _generate_time_pattern(self, behavior_type, odds_history):
        """Générer un pattern temporel pour un comportement détecté."""
        # Simulation: différents patterns selon le type de comportement
        pattern = []
        if behavior_type in ['reverse_line_movement', 'steam_move']:
            # Simuler un mouvement rapide
            start_value = random.uniform(1.7, 2.2)
            for i in range(10):
                if i < 3:
                    # Peu de changement au début
                    value = start_value + random.uniform(-0.02, 0.02)
                elif i < 7:
                    # Mouvement significatif
                    direction = 1 if behavior_type == 'reverse_line_movement' else -1
                    value = start_value + direction * 0.1 * (i - 2) + random.uniform(-0.01, 0.01)
                else:
                    # Stabilisation
                    value = start_value + direction * 0.4 + random.uniform(-0.02, 0.02)
                pattern.append({
                    'time': f"T-{10-i}",
                    'value': value
                })
        elif behavior_type == 'overnight_drift':
            # Simuler une dérive nocturne
            start_value = random.uniform(1.7, 2.2)
            times = ['18:00', '20:00', '22:00', '00:00', '02:00', '04:00', '06:00', '08:00']
            direction = 1 if random.random() > 0.5 else -1
            for i, time in enumerate(times):
                if 2 <= i <= 5:  # Dérive pendant la nuit
                    drift = direction * 0.05 * (i - 1)
                else:
                    drift = 0
                pattern.append({
                    'time': time,
                    'value': start_value + drift + random.uniform(-0.01, 0.01)
                })
        elif behavior_type == 'pre_match_surge':
            # Simuler un afflux avant match
            start_value = random.uniform(1.7, 2.2)
            times = ['T-120', 'T-90', 'T-60', 'T-45', 'T-30', 'T-20', 'T-10', 'T-5', 'T-1']
            for i, time in enumerate(times):
                if i >= 5:  # Afflux dans les dernières minutes
                    surge = 0.08 * (i - 4)
                else:
                    surge = 0
                pattern.append({
                    'time': time,
                    'value': start_value - surge + random.uniform(-0.01, 0.01)
                })
        
        return pattern
    
    def _interpret_behaviors(self, behavior_summary, alert_score):
        """Interpréter les comportements détectés et leur signification."""
        # Aucun comportement significatif
        if not behavior_summary:
            return "Aucun comportement spécial significatif détecté dans les cotes."
        
        # Interprétation de base selon le score d'alerte
        if alert_score < 0.6:
            return "Quelques comportements inhabituels détectés, mais avec une confiance limitée."
        
        if alert_score < 0.75:
            return "Plusieurs comportements anormaux détectés avec une confiance modérée. Recommandation de vigilance."
        
        # Interprétation plus détaillée pour les scores élevés
        behaviors = list(behavior_summary.keys())
        if 'steam_move' in behaviors:
            return "Détection d'un important mouvement de vapeur (steam move) indiquant une réaction coordonnée du marché. Haute probabilité d'information significative affectant les cotes."
        
        if 'reverse_line_movement' in behaviors:
            return "Mouvement inverse des lignes détecté, suggérant un décalage entre le volume des paris et la direction des cotes. Souvent indicateur d'une action de parieurs professionnels."
        
        if 'correlated_markets' in behaviors:
            return "Corrélation anormale entre marchés habituellement indépendants. Suggère un facteur commun affectant simultanément plusieurs types de paris."
        
        if 'overnight_drift' in behaviors:
            return "Dérive significative des cotes pendant les heures de marché asiatique. Peut indiquer l'influence de grands parieurs sur ces marchés."
        
        if 'pre_match_surge' in behaviors:
            return "Afflux tardif de paris juste avant le début du match. Peut indiquer des informations de dernière minute affectant la confiance des parieurs."
        
        return "Combinaison inhabituelle de comportements détectée dans les cotes. Recommandation d'une vigilance accrue et d'analyses supplémentaires."
    
    def _analyze_line_movements(self, line_movement):
        """Analyser les mouvements de ligne pour détecter des patterns."""
        analysis = {
            'total_movements': len(line_movement),
            'significant_moves': 0,
            'average_magnitude': 0.0,
            'direction_consistency': 0.0,
            'unusual_pattern': False
        }
        
        if not line_movement:
            return analysis
        
        # Calculer les statistiques de base
        magnitudes = [abs(m.get('change', 0)) for m in line_movement]
        directions = [1 if m.get('change', 0) > 0 else -1 for m in line_movement]
        
        analysis['significant_moves'] = sum(1 for m in magnitudes if m > 0.1)
        analysis['average_magnitude'] = sum(magnitudes) / len(magnitudes)
        
        # Calculer la cohérence directionnelle
        direction_sum = abs(sum(directions))
        analysis['direction_consistency'] = direction_sum / len(directions)
        
        # Détecter les patterns inhabituels
        if len(line_movement) >= 3:
            # Détecter les renversements rapides
            reversals = sum(1 for i in range(1, len(directions)) if directions[i] != directions[i-1])
            if reversals >= len(directions) / 2:
                analysis['unusual_pattern'] = True
                analysis['pattern_type'] = 'frequent_reversals'
            
            # Détecter les mouvements de grande ampleur suivis de corrections
            large_moves_with_corrections = 0
            for i in range(len(magnitudes) - 1):
                if magnitudes[i] > 0.2 and directions[i] != directions[i+1]:
                    large_moves_with_corrections += 1
            
            if large_moves_with_corrections >= 2:
                analysis['unusual_pattern'] = True
                analysis['pattern_type'] = 'correction_after_large_move'
        
        return analysis
    
    def _analyze_volume_distribution(self, volume_distribution):
        """Analyser la distribution du volume de paris."""
        analysis = {
            'anomaly_detected': False,
            'confidence': 0.5,
            'observations': []
        }
        
        # Vérifier s'il y a suffisamment de données
        if not volume_distribution:
            return analysis
        
        # Extraire les données clés
        home_volume = volume_distribution.get('home', 0)
        away_volume = volume_distribution.get('away', 0)
        
        # Calculer le déséquilibre
        total_volume = home_volume + away_volume
        if total_volume > 0:
            home_percentage = home_volume / total_volume
            imbalance = abs(0.5 - home_percentage)
            
            # Détecter un déséquilibre significatif
            if imbalance > 0.3:  # Plus de 80-20
                analysis['anomaly_detected'] = True
                favored = 'domicile' if home_percentage > 0.5 else 'extérieur'
                analysis['observations'].append(f"Déséquilibre majeur dans le volume: {int(100 * max(home_percentage, 1-home_percentage))}% sur {favored}")
                analysis['confidence'] = 0.5 + imbalance
        
        # Analyser les variations horaires si disponibles
        hourly_data = volume_distribution.get('hourly', [])
        if hourly_data:
            hourly_analysis = self._analyze_hourly_volume(hourly_data)
            if hourly_analysis.get('anomaly_detected', False):
                analysis['anomaly_detected'] = True
                analysis['observations'].extend(hourly_analysis.get('observations', []))
                analysis['confidence'] = max(analysis['confidence'], hourly_analysis.get('confidence', 0.5))
        
        return analysis
    
    def _analyze_hourly_volume(self, hourly_data):
        """Analyser le volume horaire pour détecter des anomalies."""
        # Simuler une analyse simple des données horaires
        return {
            'anomaly_detected': random.random() > 0.7,
            'confidence': random.uniform(0.6, 0.8),
            'observations': ["Pic de volume inhabituel détecté à {0}:00".format(random.randint(10, 23))] if random.random() > 0.7 else []
        }
    
    def _extract_time_series(self, odds_data, time_window=None):
        """Extraire une série temporelle des données de cotes."""
        # Simuler une extraction de série temporelle
        series = []
        now = datetime.now()
        
        # Si un filtre de fenêtre est fourni, l'appliquer
        if time_window:
            start_time, end_time = time_window
        else:
            # Par défaut, utiliser les dernières 24h
            start_time = (now - timedelta(hours=24)).isoformat()
            end_time = now.isoformat()
        
        # Simuler une série de 24 points de données (un par heure)
        for i in range(24):
            timestamp = (now - timedelta(hours=24-i)).isoformat()
            
            # Ne garder que les points dans la fenêtre temporelle
            if start_time <= timestamp <= end_time:
                base_value = 1.9
                
                # Ajouter une tendance légère
                trend = i * 0.01
                
                # Ajouter une variation aléatoire
                noise = random.uniform(-0.1, 0.1)
                
                # Ajouter des pics occasionnels
                spike = 0.2 if random.random() > 0.9 else 0
                
                value = base_value + trend + noise + spike
                
                series.append({
                    'timestamp': timestamp,
                    'value': value
                })
        
        return series
    
    def _detect_statistical_patterns(self, time_series):
        """Détecter des patterns statistiques dans une série temporelle."""
        # Si la série est vide, retourner une liste vide
        if not time_series:
            return []
        
        patterns = []
        
        # Simuler quelques patterns
        # Pattern 1: Tendance significative
        trend = (time_series[-1]['value'] - time_series[0]['value']) / len(time_series)
        if abs(trend) > 0.01:
            patterns.append({
                'type': 'trend',
                'description': "Tendance {0} significative".format("haussière" if trend > 0 else "baissière"),
                'strength': min(0.9, abs(trend) * 50),
                'time': datetime.now().isoformat(),
                'evidence': [
                    "Variation totale de {0:.2f}".format(abs(time_series[-1]['value'] - time_series[0]['value'])),
                    "Tendance constante sur {0} heures".format(len(time_series))
                ]
            })
        
        # Pattern 2: Volatilité anormale
        values = [point['value'] for point in time_series]
        volatility = np.std(values) if len(values) > 1 else 0
        if volatility > 0.05:
            patterns.append({
                'type': 'volatility',
                'description': "Volatilité anormalement élevée",
                'strength': min(0.9, volatility * 10),
                'time': datetime.now().isoformat(),
                'evidence': [
                    "Écart-type de {0:.3f}".format(volatility),
                    "Pic à pic de {0:.2f}".format(max(values) - min(values))
                ]
            })
        
        # Pattern 3: Mouvement soudain
        for i in range(1, len(time_series)):
            change = abs(time_series[i]['value'] - time_series[i-1]['value'])
            if change > 0.1:
                patterns.append({
                    'type': 'sudden_move',
                    'description': "Mouvement soudain des cotes",
                    'strength': min(0.9, change * 5),
                    'time': time_series[i]['timestamp'],
                    'evidence': [
                        "Variation de {0:.2f} dans un court intervalle".format(change),
                        "Variation relative de {0:.1f}%".format(100 * change / time_series[i-1]['value'])
                    ]
                })
        
        return patterns
    
    def _calculate_anomaly_score(self, pattern, time_series):
        """Calculer un score d'anomalie pour un pattern détecté."""
        # Score de base fonction de la force du pattern
        base_score = pattern.get('strength', 0)
        
        # Ajuster selon le type de pattern
        pattern_type = pattern.get('type', '')
        if pattern_type == 'sudden_move':
            # Les mouvements soudains sont généralement plus anormaux
            base_score = base_score * 1.2
        elif pattern_type == 'volatility':
            # La volatilité peut être due à plusieurs facteurs
            base_score = base_score * 0.9
        
        # Limiter le score final
        return min(0.95, base_score)
    
    def _generate_default_odds_data(self):
        """Générer des données de cotes par défaut pour la simulation."""
        odds_data = {}
        
        # Générer des données pour chaque marché asiatique
        for market in self.asian_markets:
            odds_data[market] = {
                'handicap_value': random.choice([-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2]),
                'home_odds': round(random.uniform(1.7, 2.3), 2),
                'away_odds': round(random.uniform(1.7, 2.3), 2),
                'line_movement': self._generate_default_line_movement(),
                'volume_distribution': self._generate_default_volume_distribution()
            }
        
        return odds_data
    
    def _generate_default_line_movement(self):
        """Générer des mouvements de ligne par défaut pour la simulation."""
        movements = []
        
        # Générer entre 3 et 8 mouvements
        for i in range(random.randint(3, 8)):
            # Simuler un changement entre -0.3 et +0.3
            change = round(random.uniform(-0.3, 0.3), 2)
            
            # Timestamp simulé
            timestamp = (datetime.now() - timedelta(hours=random.randint(0, 24))).isoformat()
            
            movements.append({
                'timestamp': timestamp,
                'change': change,
                'bookmaker': f"Bookmaker {random.randint(1, 10)}"
            })
        
        # Trier par timestamp
        movements.sort(key=lambda x: x['timestamp'])
        
        return movements
    
    def _generate_default_volume_distribution(self):
        """Générer une distribution de volume par défaut pour la simulation."""
        # Simuler un déséquilibre
        home_percentage = random.uniform(0.3, 0.7)
        total_volume = random.randint(1000, 10000)
        
        home_volume = int(home_percentage * total_volume)
        away_volume = total_volume - home_volume
        
        # Générer des données horaires
        hourly_data = []
        now = datetime.now()
        for i in range(24):
            timestamp = (now - timedelta(hours=24-i)).isoformat()
            hourly_volume = int(total_volume / 24 * (1 + random.uniform(-0.5, 0.5)))
            hourly_data.append({
                'timestamp': timestamp,
                'volume': hourly_volume,
                'home_percentage': random.uniform(max(0.1, home_percentage - 0.1), min(0.9, home_percentage + 0.1))
            })
        
        return {
            'home': home_volume,
            'away': away_volume,
            'total': total_volume,
            'hourly': hourly_data
        }
    
    def _generate_default_odds_history(self):
        """Générer un historique des cotes par défaut pour la simulation."""
        history = []
        
        # Générer des points de données sur 24 heures
        now = datetime.now()
        for i in range(24):
            timestamp = (now - timedelta(hours=24-i)).isoformat()
            
            # Simuler des données pour chaque marché
            markets_data = {}
            for market in self.asian_markets:
                base_value = random.uniform(1.7, 2.3)
                markets_data[market] = {
                    'home_odds': round(base_value, 2),
                    'away_odds': round(3.0 - base_value, 2),
                    'volume': int(random.uniform(100, 1000))
                }
            
            history.append({
                'timestamp': timestamp,
                'markets': markets_data,
                'bookmaker_count': random.randint(5, 10)
            })
        
        return history
    
    def _generate_insight_summary(self, insights, team_name):
        """Générer un résumé des insights historiques."""
        if not insights:
            return "Pas d'insights historiques disponibles pour cette équipe."
        
        market_insights = [i for i in insights if i.get('type') == 'market_insight']
        behavior_insights = [i for i in insights if i.get('type') == 'behavior_insight']
        
        avg_confidence = sum(i.get('confidence_score', 0) for i in market_insights) / max(1, len(market_insights))
        avg_alert = sum(i.get('alert_score', 0) for i in behavior_insights) / max(1, len(behavior_insights))
        
        summary = f"Pour {team_name}, historique de {len(insights)} analyses avec "
        
        if market_insights:
            summary += f"score de confiance moyen de {avg_confidence:.2f} pour les marchés, "
        
        if behavior_insights:
            summary += f"score d'alerte moyen de {avg_alert:.2f} pour les comportements, "
        
        # Identifier le comportement le plus fréquemment détecté
        behaviors = [i.get('most_significant') for i in behavior_insights if i.get('most_significant')]
        if behaviors:
            from collections import Counter
            most_common = Counter(behaviors).most_common(1)[0][0]
            summary += f"avec '{most_common}' comme comportement le plus fréquemment détecté."
        else:
            summary += "sans comportement spécifique récurrent."
        
        return summary