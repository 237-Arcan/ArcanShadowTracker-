"""
NumeriCode - Module d'interprétation numérologique des éléments sportifs.
Analyse les dates, dossards, cycles, scores et jours du calendrier sous un angle numérologique.
"""

import math
import datetime
import random
from collections import defaultdict

class NumeriCode:
    """
    NumeriCode - Interprétation numérologique des dates, dossards, cycles, scores et jours du calendrier.
    Applique des principes numérologiques pour détecter des patterns significatifs dans les événements sportifs.
    """
    
    def __init__(self):
        """Initialise le module NumeriCode"""
        # Signification numérologique des nombres de 1 à 9
        self.number_meanings = {
            1: {
                'energy': 'Leadership, ambition, initiation',
                'strength': 0.85,
                'characteristics': ['individualité', 'confiance', 'innovation'],
                'favorable_for': ['leaders', 'attaquants', 'nouveaux projets'],
                'unfavorable_for': ['travail d\'équipe', 'défense']
            },
            2: {
                'energy': 'Équilibre, diplomatie, patience',
                'strength': 0.75,
                'characteristics': ['partenariat', 'harmonie', 'adaptabilité'],
                'favorable_for': ['défenseurs', 'matchs serrés', 'stratégie défensive'],
                'unfavorable_for': ['confrontations directes', 'matchs à haute intensité']
            },
            3: {
                'energy': 'Créativité, expression, joie',
                'strength': 0.8,
                'characteristics': ['optimisme', 'talent', 'communication'],
                'favorable_for': ['matchs offensifs', 'créativité tactique', 'milieux de terrain'],
                'unfavorable_for': ['matchs défensifs', 'discipline stricte']
            },
            4: {
                'energy': 'Structure, stabilité, discipline',
                'strength': 0.85,
                'characteristics': ['ordre', 'persévérance', 'fiabilité'],
                'favorable_for': ['défense solide', 'organisation d\'équipe', 'endurance'],
                'unfavorable_for': ['changements tactiques', 'improvisation']
            },
            5: {
                'energy': 'Liberté, changement, aventure',
                'strength': 0.8,
                'characteristics': ['adaptabilité', 'dynamisme', 'imprévisibilité'],
                'favorable_for': ['changements tactiques', 'remontada', 'contre-attaques'],
                'unfavorable_for': ['stabilité défensive', 'contrôle du match']
            },
            6: {
                'energy': 'Harmonie, responsabilité, équilibre',
                'strength': 0.75,
                'characteristics': ['stabilité', 'beauté', 'solidarité'],
                'favorable_for': ['cohésion d\'équipe', 'jeu collectif', 'matchs à domicile'],
                'unfavorable_for': ['individualités fortes', 'déplacements difficiles']
            },
            7: {
                'energy': 'Analyse, perfection, introspection',
                'strength': 0.9,
                'characteristics': ['réflexion', 'intelligence', 'vision'],
                'favorable_for': ['stratégies complexes', 'adaptation tactique', 'coaching'],
                'unfavorable_for': ['jeu instinctif', 'réactions immédiates']
            },
            8: {
                'energy': 'Pouvoir, succès, abondance',
                'strength': 0.95,
                'characteristics': ['ambition', 'réussite', 'autorité'],
                'favorable_for': ['équipes favorites', 'matchs importants', 'finales'],
                'unfavorable_for': ['équipes outsiders', 'début de compétition']
            },
            9: {
                'energy': 'Sagesse, accomplissement, altruisme',
                'strength': 0.85,
                'characteristics': ['humanité', 'conclusion', 'universalité'],
                'favorable_for': ['fin de cycles', 'expérience', 'joueurs vétérans'],
                'unfavorable_for': ['début de projets', 'jeunes joueurs']
            }
        }
        
        # Nombres maîtres (restent intacts dans les calculs)
        self.master_numbers = [11, 22, 33]
        self.master_meanings = {
            11: {
                'energy': 'Illumination, intuition, inspiration',
                'strength': 0.95,
                'characteristics': ['vision', 'sensibilité', 'intuition'],
                'favorable_for': ['moments décisifs', 'joueurs créatifs', 'surprises tactiques'],
                'unfavorable_for': ['situations de haute pression', 'discipline stricte']
            },
            22: {
                'energy': 'Construction, manifestation, réussite à grande échelle',
                'strength': 0.98,
                'characteristics': ['pragmatisme', 'organisation', 'vision à long terme'],
                'favorable_for': ['grands projets', 'équipes en reconstruction', 'matchs décisifs'],
                'unfavorable_for': ['solutions temporaires', 'approches individuelles']
            },
            33: {
                'energy': 'Service, altruisme, enseignement',
                'strength': 0.9,
                'characteristics': ['compassion', 'guérison', 'inspiration'],
                'favorable_for': ['équipes jeunes', 'mentors', 'développement tactique'],
                'unfavorable_for': ['approches égoïstes', 'tactiques défensives']
            }
        }
        
        # Cycles numérologiques (9 ans)
        self.numerological_cycles = {
            1: {
                'energy': 'Nouveaux départs, opportunités, croissance',
                'strength': 0.8,
                'characteristics': ['renouveau', 'innovation', 'leadership'],
                'favorable_for': ['nouvelles approches', 'nouveaux managers', 'révolution tactique']
            },
            2: {
                'energy': 'Patience, développement, attente',
                'strength': 0.6,
                'characteristics': ['coopération', 'diplomatie', 'préparation'],
                'favorable_for': ['construction d\'équipe', 'patience tactique', 'phases transitoires']
            },
            3: {
                'energy': 'Expansion, expression, succès',
                'strength': 0.75,
                'characteristics': ['créativité', 'joie', 'communication'],
                'favorable_for': ['offensive', 'créativité tactique', 'relations médiatiques']
            },
            4: {
                'energy': 'Construction, travail, discipline',
                'strength': 0.7,
                'characteristics': ['solidité', 'fiabilité', 'méthode'],
                'favorable_for': ['défense solide', 'discipline tactique', 'organisation']
            },
            5: {
                'energy': 'Changement, aventure, adaptation',
                'strength': 0.8,
                'characteristics': ['mouvement', 'liberté', 'surprise'],
                'favorable_for': ['transferts', 'changements tactiques', 'adaptabilité']
            },
            6: {
                'energy': 'Responsabilité, harmonie, service',
                'strength': 0.65,
                'characteristics': ['équilibre', 'beauté', 'communauté'],
                'favorable_for': ['équilibre tactique', 'cohésion d\'équipe', 'travail de fond']
            },
            7: {
                'energy': 'Réflexion, introspection, perfectionnement',
                'strength': 0.7,
                'characteristics': ['analyse', 'spiritualité', 'sagesse'],
                'favorable_for': ['analyse tactique', 'préparation mentale', 'ajustements précis']
            },
            8: {
                'energy': 'Pouvoir, succès, récompense',
                'strength': 0.85,
                'characteristics': ['réussite', 'richesse', 'influence'],
                'favorable_for': ['succès', 'objectifs ambitieux', 'domination']
            },
            9: {
                'energy': 'Accomplissement, conclusion, transformation',
                'strength': 0.75,
                'characteristics': ['finalisation', 'lâcher-prise', 'ascension'],
                'favorable_for': ['fins de cycle', 'dernières saisons', 'transitions']
            }
        }
        
        # Compatibilité numérologique entre les nombres
        self.number_compatibility = {
            1: {1: 0.5, 2: 0.6, 3: 0.9, 4: 0.5, 5: 0.8, 6: 0.4, 7: 0.7, 8: 0.9, 9: 0.6},
            2: {1: 0.6, 2: 0.8, 3: 0.5, 4: 0.7, 5: 0.4, 6: 0.9, 7: 0.6, 8: 0.5, 9: 0.7},
            3: {1: 0.9, 2: 0.5, 3: 0.8, 4: 0.6, 5: 0.9, 6: 0.7, 7: 0.5, 8: 0.6, 9: 0.9},
            4: {1: 0.5, 2: 0.7, 3: 0.6, 4: 0.9, 5: 0.5, 6: 0.8, 7: 0.7, 8: 0.8, 9: 0.4},
            5: {1: 0.8, 2: 0.4, 3: 0.9, 4: 0.5, 5: 0.7, 6: 0.5, 7: 0.6, 8: 0.7, 9: 0.8},
            6: {1: 0.4, 2: 0.9, 3: 0.7, 4: 0.8, 5: 0.5, 6: 0.9, 7: 0.6, 8: 0.5, 9: 0.8},
            7: {1: 0.7, 2: 0.6, 3: 0.5, 4: 0.7, 5: 0.6, 6: 0.6, 7: 0.9, 8: 0.7, 9: 0.9},
            8: {1: 0.9, 2: 0.5, 3: 0.6, 4: 0.8, 5: 0.7, 6: 0.5, 7: 0.7, 8: 0.8, 9: 0.6},
            9: {1: 0.6, 2: 0.7, 3: 0.9, 4: 0.4, 5: 0.8, 6: 0.8, 7: 0.9, 8: 0.6, 9: 0.7}
        }
        
        # Jours de la semaine et leur vibration numérologique
        self.day_vibrations = {
            0: {'number': 1, 'day': 'Dimanche', 'energy': 'Succès, leadership, vitalité'},
            1: {'number': 2, 'day': 'Lundi', 'energy': 'Intuition, collaboration, sensibilité'},
            2: {'number': 3, 'day': 'Mardi', 'energy': 'Dynamisme, courage, compétition'},
            3: {'number': 4, 'day': 'Mercredi', 'energy': 'Communication, adaptabilité, intelligence'},
            4: {'number': 5, 'day': 'Jeudi', 'energy': 'Expansion, chance, opportunité'},
            5: {'number': 6, 'day': 'Vendredi', 'energy': 'Harmonie, amour, équilibre'},
            6: {'number': 7, 'day': 'Samedi', 'energy': 'Réflexion, sagesse, introspection'}
        }
        
        # Historique des analyses
        self.analysis_history = []
    
    def analyze_date(self, date_str=None, date_obj=None):
        """
        Analyser la numérologie d'une date spécifique.
        
        Args:
            date_str (str, optional): Date au format 'YYYY-MM-DD'
            date_obj (datetime.date, optional): Objet date Python
            
        Returns:
            dict: Analyse numérologique de la date
        """
        # Obtenir l'objet date
        if date_obj is None:
            if date_str is None:
                date_obj = datetime.date.today()
            else:
                try:
                    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    return {'error': 'Format de date invalide. Utilisez YYYY-MM-DD'}
        
        # Extraire composantes
        day = date_obj.day
        month = date_obj.month
        year = date_obj.year
        
        # Calcul du nombre du jour
        day_number = self._reduce_number(day)
        
        # Calcul du nombre du mois
        month_number = self._reduce_number(month)
        
        # Calcul du nombre de l'année
        year_number = self._reduce_number(year)
        
        # Calcul du nombre de la date complète
        date_number = self._reduce_number(day + month + year)
        
        # Calcul du jour de la semaine
        weekday = date_obj.weekday()
        weekday_info = self.day_vibrations.get(weekday, {})
        
        # Déterminer si la date contient des nombres maîtres
        master_numbers_present = []
        if day in self.master_numbers:
            master_numbers_present.append(day)
        if month in self.master_numbers:
            master_numbers_present.append(month)
        if self._calculate_life_path_number(date_obj, keep_master=True) in self.master_numbers:
            master_numbers_present.append(self._calculate_life_path_number(date_obj, keep_master=True))
        
        # Vérifier si c'est une date miroir (comme 11-11 ou 12-21)
        is_mirror_date = self._is_mirror_date(date_obj)
        
        # Vérifier si la date contient un nombre premier
        is_prime_day = self._is_prime(day)
        is_prime_month = self._is_prime(month)
        is_prime_date = self._is_prime(day) and self._is_prime(month)
        
        # Calculer le chemin de vie (life path) de la date
        life_path = self._calculate_life_path_number(date_obj)
        life_path_master = self._calculate_life_path_number(date_obj, keep_master=True)
        
        # Récupérer l'information numérologique des nombres calculés
        date_numerology = self._get_number_meaning(date_number)
        life_path_numerology = self._get_number_meaning(life_path)
        
        # Si un nombre maître est présent dans le chemin de vie
        if life_path_master in self.master_numbers:
            life_path_numerology = self._get_master_number_meaning(life_path_master)
        
        # Vibration du jour de la semaine
        day_vibration = weekday_info.get('energy', '')
        day_number_vibration = self._get_number_meaning(weekday_info.get('number', 0))
        
        # Calculer le cycle numérologique actuel
        current_cycle = self._calculate_current_cycle(date_obj)
        cycle_info = self.numerological_cycles.get(current_cycle, {})
        
        # Préparation du résultat
        result = {
            'date': date_obj.strftime('%Y-%m-%d'),
            'day_of_week': weekday_info.get('day', ''),
            'day_number': day_number,
            'month_number': month_number,
            'year_number': year_number,
            'date_number': date_number,
            'life_path_number': life_path,
            'special_characteristics': {
                'contains_master_numbers': len(master_numbers_present) > 0,
                'master_numbers_present': master_numbers_present,
                'is_mirror_date': is_mirror_date,
                'is_prime_day': is_prime_day,
                'is_prime_month': is_prime_month,
                'is_prime_date': is_prime_date
            },
            'numerological_meaning': {
                'date_energy': date_numerology.get('energy', ''),
                'date_characteristics': date_numerology.get('characteristics', []),
                'life_path_energy': life_path_numerology.get('energy', ''),
                'life_path_characteristics': life_path_numerology.get('characteristics', []),
                'day_vibration': day_vibration,
                'day_number_energy': day_number_vibration.get('energy', '')
            },
            'current_cycle': {
                'number': current_cycle,
                'energy': cycle_info.get('energy', ''),
                'strength': cycle_info.get('strength', 0.5),
                'favorable_for': cycle_info.get('favorable_for', [])
            },
            'sports_influence': {
                'favorable_for': date_numerology.get('favorable_for', []),
                'unfavorable_for': date_numerology.get('unfavorable_for', []),
                'energy_strength': date_numerology.get('strength', 0.5),
                'compatibility': self._calculate_number_compatibility(date_number, life_path)
            }
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'date_analysis',
            'date': date_obj.strftime('%Y-%m-%d'),
            'result': result
        })
        
        return result
    
    def analyze_jersey_numbers(self, numbers, team_name=None):
        """
        Analyser la signification numérologique des numéros de maillot d'une équipe.
        
        Args:
            numbers (list): Liste des numéros de maillot
            team_name (str, optional): Nom de l'équipe
            
        Returns:
            dict: Analyse des numéros et leur influence collective
        """
        if not numbers:
            return {'error': 'Aucun numéro de maillot fourni'}
        
        # Analyse individuelle de chaque numéro
        number_analyses = []
        
        for number in numbers:
            reduced_number = self._reduce_number(number)
            is_master = number in self.master_numbers
            
            # Obtenir la signification numérologique
            if is_master:
                meaning = self._get_master_number_meaning(number)
            else:
                meaning = self._get_number_meaning(reduced_number)
            
            number_analyses.append({
                'jersey_number': number,
                'reduced_number': reduced_number,
                'is_master_number': is_master,
                'energy': meaning.get('energy', ''),
                'characteristics': meaning.get('characteristics', []),
                'favorable_for': meaning.get('favorable_for', []),
                'unfavorable_for': meaning.get('unfavorable_for', []),
                'strength': meaning.get('strength', 0.5)
            })
        
        # Analyse collective
        sum_all_numbers = sum(numbers)
        reduced_sum = self._reduce_number(sum_all_numbers)
        team_number_meaning = self._get_number_meaning(reduced_sum)
        
        # Compter la fréquence de chaque nombre réduit
        number_frequency = defaultdict(int)
        for number in numbers:
            reduced = self._reduce_number(number)
            number_frequency[reduced] += 1
        
        # Déterminer le nombre dominant
        dominant_number = max(number_frequency.items(), key=lambda x: x[1])[0] if number_frequency else None
        
        # Vérifier les nombres maîtres présents
        master_numbers_present = [num for num in numbers if num in self.master_numbers]
        
        # Calculer la compatibilité moyenne entre tous les numéros
        compatibility_sum = 0
        compatibility_count = 0
        
        for i in range(len(numbers)):
            for j in range(i+1, len(numbers)):
                num1 = self._reduce_number(numbers[i])
                num2 = self._reduce_number(numbers[j])
                compatibility = self._calculate_number_compatibility(num1, num2)
                compatibility_sum += compatibility
                compatibility_count += 1
        
        # Éviter division par zéro
        avg_compatibility = compatibility_sum / compatibility_count if compatibility_count > 0 else 0
        
        # Évaluer l'équilibre des nombres (distribution entre différents types d'énergie)
        balance_score = self._calculate_number_balance(number_frequency)
        
        # Préparer le résultat
        result = {
            'team_name': team_name,
            'individual_numbers': number_analyses,
            'collective_analysis': {
                'sum_of_all_numbers': sum_all_numbers,
                'team_number': reduced_sum,
                'team_energy': team_number_meaning.get('energy', ''),
                'team_characteristics': team_number_meaning.get('characteristics', []),
                'dominant_number': dominant_number,
                'dominant_number_frequency': number_frequency.get(dominant_number, 0) if dominant_number else 0,
                'master_numbers_present': master_numbers_present,
                'number_distribution': dict(number_frequency),
                'number_balance_score': balance_score,
                'average_compatibility': avg_compatibility
            },
            'team_potential': {
                'strengths': self._identify_team_number_strengths(number_frequency, master_numbers_present),
                'weaknesses': self._identify_team_number_weaknesses(number_frequency, master_numbers_present),
                'optimal_playing_style': self._suggest_optimal_playing_style(number_frequency, reduced_sum),
                'favorable_conditions': team_number_meaning.get('favorable_for', []),
                'unfavorable_conditions': team_number_meaning.get('unfavorable_for', [])
            }
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'jersey_numbers_analysis',
            'team': team_name,
            'result': result
        })
        
        return result
    
    def analyze_score(self, home_score, away_score, teams=None):
        """
        Analyser la signification numérologique d'un score de match.
        
        Args:
            home_score (int): Score de l'équipe à domicile
            away_score (int): Score de l'équipe à l'extérieur
            teams (dict, optional): Noms des équipes {'home': 'Équipe 1', 'away': 'Équipe 2'}
            
        Returns:
            dict: Analyse numérologique du score
        """
        if home_score < 0 or away_score < 0:
            return {'error': 'Scores invalides. Les scores doivent être positifs.'}
        
        # Calculs de base
        total_goals = home_score + away_score
        score_difference = abs(home_score - away_score)
        
        # Réduction numérologique
        reduced_home = self._reduce_number(home_score)
        reduced_away = self._reduce_number(away_score)
        reduced_total = self._reduce_number(total_goals)
        reduced_difference = self._reduce_number(score_difference)
        
        # Vérifier les nombres maîtres
        master_numbers_present = []
        if home_score in self.master_numbers:
            master_numbers_present.append({'number': home_score, 'team': 'home'})
        if away_score in self.master_numbers:
            master_numbers_present.append({'number': away_score, 'team': 'away'})
        if total_goals in self.master_numbers:
            master_numbers_present.append({'number': total_goals, 'team': 'both'})
        
        # Obtenir les significations
        home_meaning = self._get_number_meaning(reduced_home)
        away_meaning = self._get_number_meaning(reduced_away)
        total_meaning = self._get_number_meaning(reduced_total)
        difference_meaning = self._get_number_meaning(reduced_difference)
        
        # Compatibilité entre les nombres
        score_compatibility = self._calculate_number_compatibility(reduced_home, reduced_away)
        
        # Vérifier les scores miroirs (comme 1-1, 2-2, etc.)
        is_mirror_score = home_score == away_score
        
        # Vérifier si un score contient un nombre premier
        is_prime_home = self._is_prime(home_score)
        is_prime_away = self._is_prime(away_score)
        is_prime_total = self._is_prime(total_goals)
        
        # Calculer la vibration karmique du score
        karmic_vibration = self._calculate_karmic_vibration(home_score, away_score)
        
        # Noms des équipes
        home_team_name = teams['home'] if teams and 'home' in teams else 'Équipe domicile'
        away_team_name = teams['away'] if teams and 'away' in teams else 'Équipe extérieure'
        
        # Préparer le résultat
        result = {
            'score': f"{home_score} - {away_score}",
            'teams': {
                'home': home_team_name,
                'away': away_team_name
            },
            'basic_analysis': {
                'total_goals': total_goals,
                'score_difference': score_difference,
                'home_number': reduced_home,
                'away_number': reduced_away,
                'total_number': reduced_total,
                'difference_number': reduced_difference
            },
            'special_characteristics': {
                'contains_master_numbers': len(master_numbers_present) > 0,
                'master_numbers_present': master_numbers_present,
                'is_mirror_score': is_mirror_score,
                'is_prime_home': is_prime_home,
                'is_prime_away': is_prime_away,
                'is_prime_total': is_prime_total
            },
            'numerological_meaning': {
                'home_energy': home_meaning.get('energy', ''),
                'away_energy': away_meaning.get('energy', ''),
                'total_energy': total_meaning.get('energy', ''),
                'difference_energy': difference_meaning.get('energy', '')
            },
            'karmic_analysis': {
                'karmic_vibration': karmic_vibration,
                'karmic_level': self._classify_karmic_level(karmic_vibration),
                'karmic_interpretation': self._interpret_karmic_score(karmic_vibration, is_mirror_score)
            },
            'compatibility': {
                'score_harmony': score_compatibility,
                'harmony_level': self._classify_harmony_level(score_compatibility),
                'interpretation': self._interpret_score_harmony(score_compatibility, is_mirror_score)
            }
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'score_analysis',
            'score': f"{home_score} - {away_score}",
            'result': result
        })
        
        return result
    
    def calculate_team_life_path(self, foundation_date, team_name=None):
        """
        Calculer le chemin de vie numérologique d'une équipe basé sur sa date de fondation.
        
        Args:
            foundation_date (str/datetime): Date de fondation de l'équipe
            team_name (str, optional): Nom de l'équipe
            
        Returns:
            dict: Analyse du chemin de vie de l'équipe
        """
        # Convertir la date en objet datetime si nécessaire
        if isinstance(foundation_date, str):
            try:
                foundation_date = datetime.datetime.strptime(foundation_date, '%Y-%m-%d').date()
            except ValueError:
                return {'error': 'Format de date invalide. Utilisez YYYY-MM-DD'}
        
        # Calculer le chemin de vie
        life_path = self._calculate_life_path_number(foundation_date)
        life_path_master = self._calculate_life_path_number(foundation_date, keep_master=True)
        
        # Vérifier si c'est un nombre maître
        is_master = life_path_master in self.master_numbers
        
        # Obtenir la signification
        if is_master:
            meaning = self._get_master_number_meaning(life_path_master)
            life_path_number = life_path_master
        else:
            meaning = self._get_number_meaning(life_path)
            life_path_number = life_path
        
        # Calculer l'année personnelle actuelle
        current_year = datetime.date.today().year
        personal_year = self._calculate_personal_year(foundation_date, current_year)
        personal_year_meaning = self._get_number_meaning(personal_year)
        
        # Déterminer le chemin de destinée (basé sur le nom)
        destiny_number = None
        destiny_meaning = {}
        if team_name:
            destiny_number = self._calculate_destiny_number(team_name)
            destiny_meaning = self._get_number_meaning(destiny_number)
            
            # Vérifier la compatibilité entre chemin de vie et nombre de destinée
            life_destiny_compatibility = self._calculate_number_compatibility(life_path, destiny_number)
        else:
            life_destiny_compatibility = None
        
        # Préparer le résultat
        result = {
            'team_name': team_name,
            'foundation_date': foundation_date.strftime('%Y-%m-%d'),
            'life_path': {
                'number': life_path_number,
                'is_master_number': is_master,
                'energy': meaning.get('energy', ''),
                'characteristics': meaning.get('characteristics', []),
                'strengths': meaning.get('favorable_for', []),
                'challenges': meaning.get('unfavorable_for', [])
            },
            'destiny_path': {
                'number': destiny_number,
                'energy': destiny_meaning.get('energy', '') if destiny_number else None,
                'characteristics': destiny_meaning.get('characteristics', []) if destiny_number else None
            },
            'current_cycle': {
                'personal_year': personal_year,
                'energy': personal_year_meaning.get('energy', ''),
                'focus': personal_year_meaning.get('characteristics', [])
            },
            'compatibility': {
                'life_destiny_harmony': life_destiny_compatibility,
                'interpretation': self._interpret_life_destiny_harmony(life_destiny_compatibility) if life_destiny_compatibility else None
            },
            'team_potential': {
                'natural_strengths': self._identify_life_path_strengths(life_path_number),
                'natural_challenges': self._identify_life_path_challenges(life_path_number),
                'optimal_development_path': self._suggest_development_path(life_path_number, destiny_number)
            }
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'team_life_path_analysis',
            'team': team_name,
            'result': result
        })
        
        return result
    
    def analyze_match_compatibility(self, match_date, team1_data, team2_data):
        """
        Analyser la compatibilité numérologique entre deux équipes pour un match spécifique.
        
        Args:
            match_date (str/datetime): Date du match
            team1_data (dict): Données de la première équipe (nom, date de fondation, numéros de maillot)
            team2_data (dict): Données de la deuxième équipe (nom, date de fondation, numéros de maillot)
            
        Returns:
            dict: Analyse de compatibilité entre les équipes
        """
        # Convertir la date en objet datetime si nécessaire
        if isinstance(match_date, str):
            try:
                match_date_obj = datetime.datetime.strptime(match_date, '%Y-%m-%d').date()
            except ValueError:
                return {'error': 'Format de date invalide. Utilisez YYYY-MM-DD'}
        else:
            match_date_obj = match_date
        
        # Extraire les données des équipes
        team1_name = team1_data.get('name', 'Équipe 1')
        team2_name = team2_data.get('name', 'Équipe 2')
        
        # Convertir les dates de fondation
        team1_foundation = team1_data.get('foundation_date')
        team2_foundation = team2_data.get('foundation_date')
        
        if isinstance(team1_foundation, str):
            team1_foundation = datetime.datetime.strptime(team1_foundation, '%Y-%m-%d').date()
        if isinstance(team2_foundation, str):
            team2_foundation = datetime.datetime.strptime(team2_foundation, '%Y-%m-%d').date()
        
        # Calculer les chemins de vie
        team1_life_path = self._calculate_life_path_number(team1_foundation)
        team2_life_path = self._calculate_life_path_number(team2_foundation)
        
        # Analyser la date du match
        match_numerology = self.analyze_date(date_obj=match_date_obj)
        match_number = match_numerology['date_number']
        
        # Calculer les compatibilités
        team1_match_compatibility = self._calculate_number_compatibility(team1_life_path, match_number)
        team2_match_compatibility = self._calculate_number_compatibility(team2_life_path, match_number)
        teams_compatibility = self._calculate_number_compatibility(team1_life_path, team2_life_path)
        
        # Calculer les cycles personnels pour la date du match
        team1_personal_day = self._calculate_personal_day(team1_foundation, match_date_obj)
        team2_personal_day = self._calculate_personal_day(team2_foundation, match_date_obj)
        
        # Influence des numéros de maillot
        team1_jerseys = team1_data.get('jersey_numbers', [])
        team2_jerseys = team2_data.get('jersey_numbers', [])
        
        jersey_influence = None
        if team1_jerseys and team2_jerseys:
            jersey_influence = self._analyze_jersey_compatibility(team1_jerseys, team2_jerseys)
        
        # Déterminer l'équipe favorisée par la numérologie
        favored_team = None
        advantage_strength = 0
        
        if team1_match_compatibility > team2_match_compatibility + 0.1:
            favored_team = team1_name
            advantage_strength = team1_match_compatibility - team2_match_compatibility
        elif team2_match_compatibility > team1_match_compatibility + 0.1:
            favored_team = team2_name
            advantage_strength = team2_match_compatibility - team1_match_compatibility
        
        # Vérifier les résonances spéciales
        special_resonances = self._check_special_resonances(
            match_date_obj, team1_foundation, team2_foundation, team1_life_path, team2_life_path
        )
        
        # Préparer le résultat
        result = {
            'match_date': match_date_obj.strftime('%Y-%m-%d'),
            'teams': {
                'team1': team1_name,
                'team2': team2_name
            },
            'match_numerology': {
                'date_number': match_number,
                'life_path': match_numerology['life_path_number'],
                'day_energy': match_numerology['numerological_meaning']['day_vibration']
            },
            'compatibility': {
                'team1_match_compatibility': team1_match_compatibility,
                'team2_match_compatibility': team2_match_compatibility,
                'teams_mutual_compatibility': teams_compatibility
            },
            'personal_cycles': {
                'team1_personal_day': team1_personal_day,
                'team2_personal_day': team2_personal_day,
                'team1_day_energy': self._get_number_meaning(team1_personal_day).get('energy', ''),
                'team2_day_energy': self._get_number_meaning(team2_personal_day).get('energy', '')
            },
            'jersey_influence': jersey_influence,
            'numerological_advantage': {
                'favored_team': favored_team,
                'advantage_strength': advantage_strength,
                'advantage_level': self._classify_advantage_level(advantage_strength)
            },
            'special_resonances': special_resonances
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'match_compatibility_analysis',
            'match': f"{team1_name} vs {team2_name}",
            'date': match_date_obj.strftime('%Y-%m-%d'),
            'result': result
        })
        
        return result
    
    def find_favorable_dates(self, team_data, start_date, end_date, min_compatibility=0.7):
        """
        Trouver les dates les plus favorables pour une équipe dans une période donnée.
        
        Args:
            team_data (dict): Données de l'équipe (nom, date de fondation)
            start_date (str/datetime): Date de début de la période
            end_date (str/datetime): Date de fin de la période
            min_compatibility (float): Compatibilité minimale requise (0-1)
            
        Returns:
            dict: Dates favorables et leur analyse
        """
        # Convertir les dates en objets datetime si nécessaire
        if isinstance(start_date, str):
            try:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                return {'error': 'Format de date de début invalide. Utilisez YYYY-MM-DD'}
        
        if isinstance(end_date, str):
            try:
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return {'error': 'Format de date de fin invalide. Utilisez YYYY-MM-DD'}
        
        # Vérifier que la période est valide
        if start_date > end_date:
            return {'error': 'La date de début doit être antérieure à la date de fin'}
        
        # Maximum de 90 jours pour limiter les calculs
        max_days = 90
        if (end_date - start_date).days > max_days:
            end_date = start_date + datetime.timedelta(days=max_days)
        
        # Extraire les données de l'équipe
        team_name = team_data.get('name', 'Équipe')
        
        # Convertir la date de fondation
        team_foundation = team_data.get('foundation_date')
        if isinstance(team_foundation, str):
            team_foundation = datetime.datetime.strptime(team_foundation, '%Y-%m-%d').date()
        
        # Calculer le chemin de vie de l'équipe
        team_life_path = self._calculate_life_path_number(team_foundation)
        
        # Parcourir chaque date dans la période
        favorable_dates = []
        current_date = start_date
        
        while current_date <= end_date:
            # Analyser la numérologie de la date
            date_numerology = self.analyze_date(date_obj=current_date)
            date_number = date_numerology['date_number']
            
            # Calculer la compatibilité
            compatibility = self._calculate_number_compatibility(team_life_path, date_number)
            
            # Calculer le jour personnel pour cette date
            personal_day = self._calculate_personal_day(team_foundation, current_date)
            personal_day_meaning = self._get_number_meaning(personal_day)
            
            # Vérifier si la date est favorable
            if compatibility >= min_compatibility:
                favorable_dates.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'day_of_week': date_numerology['day_of_week'],
                    'compatibility': compatibility,
                    'date_number': date_number,
                    'date_energy': date_numerology['numerological_meaning']['date_energy'],
                    'personal_day': personal_day,
                    'personal_day_energy': personal_day_meaning.get('energy', ''),
                    'compatibility_level': self._classify_compatibility_level(compatibility),
                    'special_characteristics': date_numerology['special_characteristics'],
                    'favorable_aspects': self._identify_favorable_aspects(date_numerology, personal_day_meaning)
                })
            
            # Passer au jour suivant
            current_date += datetime.timedelta(days=1)
        
        # Trier les dates par compatibilité
        favorable_dates.sort(key=lambda x: x['compatibility'], reverse=True)
        
        # Préparer le résultat
        result = {
            'team_name': team_name,
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days_analyzed': (end_date - start_date).days + 1
            },
            'team_life_path': team_life_path,
            'favorable_dates_count': len(favorable_dates),
            'favorable_dates': favorable_dates,
            'most_favorable_date': favorable_dates[0] if favorable_dates else None,
            'compatibility_threshold': min_compatibility
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'favorable_dates_analysis',
            'team': team_name,
            'result': result
        })
        
        return result
    
    def analyze_match_cycle(self, team1_data, team2_data, previous_matches):
        """
        Analyser les cycles numérologiques dans l'historique des confrontations entre deux équipes.
        
        Args:
            team1_data (dict): Données de la première équipe
            team2_data (dict): Données de la deuxième équipe
            previous_matches (list): Liste des confrontations précédentes (date, résultat)
            
        Returns:
            dict: Analyse des cycles et patterns numérologiques
        """
        if not previous_matches or len(previous_matches) < 3:
            return {'error': 'Historique insuffisant pour l\'analyse des cycles'}
        
        # Extraire les données des équipes
        team1_name = team1_data.get('name', 'Équipe 1')
        team2_name = team2_data.get('name', 'Équipe 2')
        
        # Préparer l'analyse des matchs précédents
        match_analyses = []
        win_cycle = []
        score_pattern = []
        date_numbers = []
        
        for match in previous_matches:
            # Extraire les informations du match
            match_date = match.get('date')
            if isinstance(match_date, str):
                match_date = datetime.datetime.strptime(match_date, '%Y-%m-%d').date()
            
            result = match.get('result', '')  # 'team1_win', 'team2_win', 'draw'
            score = match.get('score', '')
            
            # Analyser la numérologie de la date
            date_numerology = self.analyze_date(date_obj=match_date)
            
            # Stocker les résultats et numéros de date
            win_cycle.append(result)
            if score:
                score_pattern.append(score)
            date_numbers.append(date_numerology['date_number'])
            
            # Analyser le score si disponible
            score_analysis = None
            if score and '-' in score:
                try:
                    home_score, away_score = map(int, score.split('-'))
                    score_analysis = self.analyze_score(
                        home_score, away_score, 
                        {'home': team1_name, 'away': team2_name}
                    )
                except:
                    pass
            
            # Ajouter l'analyse de ce match
            match_analyses.append({
                'date': match_date.strftime('%Y-%m-%d'),
                'result': result,
                'score': score,
                'date_number': date_numerology['date_number'],
                'date_energy': date_numerology['numerological_meaning']['date_energy'],
                'score_analysis': score_analysis
            })
        
        # Détecter les cycles de victoire
        victory_cycles = self._detect_victory_cycles(win_cycle, team1_name, team2_name)
        
        # Détecter les patterns de score
        score_patterns = self._detect_score_patterns(score_pattern)
        
        # Détecter les cycles de dates
        date_cycles = self._detect_number_cycles(date_numbers)
        
        # Calculer la prochaine date favorable
        next_favorable_date = self._predict_next_favorable_date(previous_matches, team1_data, team2_data)
        
        # Préparer le résultat
        result = {
            'teams': {
                'team1': team1_name,
                'team2': team2_name
            },
            'matches_analyzed': len(previous_matches),
            'match_analyses': match_analyses,
            'numerological_patterns': {
                'victory_cycles': victory_cycles,
                'score_patterns': score_patterns,
                'date_number_cycles': date_cycles
            },
            'cycle_predictions': {
                'next_favorable_date': next_favorable_date,
                'predicted_pattern': self._predict_next_match_pattern(
                    win_cycle, score_pattern, date_numbers, team1_name, team2_name
                )
            }
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'match_cycle_analysis',
            'match': f"{team1_name} vs {team2_name}",
            'result': result
        })
        
        return result
    
    def get_personal_day_forecast(self, foundation_date, date=None):
        """
        Obtenir les prévisions basées sur le jour personnel d'une équipe.
        
        Args:
            foundation_date (str/datetime): Date de fondation de l'équipe
            date (str/datetime, optional): Date pour laquelle calculer le jour personnel
            
        Returns:
            dict: Prévisions basées sur le jour personnel
        """
        # Convertir la date de fondation en objet datetime si nécessaire
        if isinstance(foundation_date, str):
            try:
                foundation_date = datetime.datetime.strptime(foundation_date, '%Y-%m-%d').date()
            except ValueError:
                return {'error': 'Format de date de fondation invalide. Utilisez YYYY-MM-DD'}
        
        # Utiliser la date actuelle si non spécifiée
        if date is None:
            date = datetime.date.today()
        elif isinstance(date, str):
            try:
                date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                return {'error': 'Format de date invalide. Utilisez YYYY-MM-DD'}
        
        # Calculer le jour personnel
        personal_day = self._calculate_personal_day(foundation_date, date)
        
        # Obtenir la signification du jour personnel
        day_meaning = self._get_number_meaning(personal_day)
        
        # Calculer les chiffres essentiels
        essence_numbers = self._calculate_essence_numbers(foundation_date, date)
        
        # Préparer les prévisions
        forecasts = {
            'general': self._generate_personal_day_forecast(personal_day, 'general'),
            'performance': self._generate_personal_day_forecast(personal_day, 'performance'),
            'team_dynamics': self._generate_personal_day_forecast(personal_day, 'team'),
            'challenges': self._generate_personal_day_forecast(personal_day, 'challenges')
        }
        
        # Préparer le résultat
        result = {
            'date': date.strftime('%Y-%m-%d'),
            'foundation_date': foundation_date.strftime('%Y-%m-%d'),
            'personal_day': {
                'number': personal_day,
                'energy': day_meaning.get('energy', ''),
                'characteristics': day_meaning.get('characteristics', [])
            },
            'essence_numbers': essence_numbers,
            'forecasts': forecasts,
            'favorable_for': day_meaning.get('favorable_for', []),
            'unfavorable_for': day_meaning.get('unfavorable_for', []),
            'day_potential': {
                'energy_level': self._calculate_energy_level(personal_day, essence_numbers),
                'performance_potential': self._calculate_performance_potential(personal_day, essence_numbers),
                'challenge_level': self._calculate_challenge_level(personal_day, essence_numbers)
            }
        }
        
        return result
    
    def _reduce_number(self, number, keep_master=False):
        """Réduire un nombre à un chiffre (1-9) selon les principes de numérologie."""
        # Si c'est déjà un nombre à un chiffre, le retourner directement
        if 0 < number < 10:
            return number
        
        # Pour les nombres négatifs, utiliser la valeur absolue
        number = abs(number)
        
        # Vérifier si c'est un nombre maître (11, 22, 33) avant réduction
        if keep_master and number in self.master_numbers:
            return number
        
        # Réduire en additionnant les chiffres jusqu'à obtenir un nombre à un chiffre
        while number > 9:
            number = sum(int(digit) for digit in str(number))
            
            # Vérifier à nouveau si c'est un nombre maître après réduction
            if keep_master and number in self.master_numbers:
                return number
        
        return number
    
    def _calculate_life_path_number(self, date_obj, keep_master=False):
        """Calculer le nombre du chemin de vie à partir d'une date."""
        # Extraire jour, mois, année
        day = date_obj.day
        month = date_obj.month
        year = date_obj.year
        
        # Réduire chaque composante
        day_reduced = self._reduce_number(day)
        month_reduced = self._reduce_number(month)
        year_reduced = self._reduce_number(year)
        
        # Additionner les composantes réduites
        life_path = day_reduced + month_reduced + year_reduced
        
        # Réduire à un seul chiffre (ou conserver les nombres maîtres)
        return self._reduce_number(life_path, keep_master)
    
    def _calculate_personal_day(self, birth_date, target_date):
        """Calculer le nombre du jour personnel pour une date spécifique."""
        # Extraire jour, mois de la date cible
        day = target_date.day
        month = target_date.month
        year = target_date.year
        
        # Extraire jour, mois, année de la date de naissance
        birth_day = birth_date.day
        birth_month = birth_date.month
        birth_year = birth_date.year
        
        # Réduire chaque composante
        day_reduced = self._reduce_number(day)
        month_reduced = self._reduce_number(month)
        year_reduced = self._reduce_number(year)
        birth_day_reduced = self._reduce_number(birth_day)
        birth_month_reduced = self._reduce_number(birth_month)
        birth_year_reduced = self._reduce_number(birth_year)
        
        # Calculer le jour personnel
        personal_day = day_reduced + month_reduced + year_reduced + birth_day_reduced + birth_month_reduced + birth_year_reduced
        
        # Réduire à un seul chiffre
        return self._reduce_number(personal_day)
    
    def _calculate_personal_year(self, birth_date, year):
        """Calculer le nombre de l'année personnelle."""
        # Extraire mois, jour de la date de naissance
        birth_day = birth_date.day
        birth_month = birth_date.month
        
        # Réduire l'année en numérologie
        year_reduced = self._reduce_number(year)
        
        # Réduire le jour et le mois de naissance
        birth_day_reduced = self._reduce_number(birth_day)
        birth_month_reduced = self._reduce_number(birth_month)
        
        # Calculer l'année personnelle
        personal_year = year_reduced + birth_day_reduced + birth_month_reduced
        
        # Réduire à un seul chiffre
        return self._reduce_number(personal_year)
    
    def _calculate_essence_numbers(self, birth_date, target_date):
        """Calculer les nombres d'essence pour une date spécifique."""
        # Calculer le jour, mois, année personnels
        personal_day = self._calculate_personal_day(birth_date, target_date)
        personal_month = self._reduce_number(target_date.month + self._reduce_number(birth_date.day + birth_date.month))
        personal_year = self._calculate_personal_year(birth_date, target_date.year)
        
        # Calculer le nombre d'essence (combinaison des trois)
        essence = self._reduce_number(personal_day + personal_month + personal_year)
        
        return {
            'personal_day': personal_day,
            'personal_month': personal_month,
            'personal_year': personal_year,
            'essence': essence
        }
    
    def _calculate_current_cycle(self, date_obj):
        """Calculer le cycle numérologique actuel (1-9) basé sur l'année."""
        # Extraire l'année
        year = date_obj.year
        
        # Calculer le cycle (1-9)
        cycle = ((year - 1) % 9) + 1
        
        return cycle
    
    def _is_mirror_date(self, date_obj):
        """Vérifier si une date est une date miroir (comme 11/11, 12/21, etc.)."""
        day = date_obj.day
        month = date_obj.month
        
        # Formats miroir simples (jour = mois, comme 1/1, 2/2, etc.)
        if day == month:
            return True
        
        # Formats miroir inversés (jour = mois inversé, comme 12/21, 10/01, etc.)
        day_str = f"{day:02d}"
        month_str = f"{month:02d}"
        
        if day_str == month_str[::-1]:
            return True
        
        return False
    
    def _is_prime(self, n):
        """Vérifier si un nombre est premier."""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
            
        return True
    
    def _get_number_meaning(self, number):
        """Obtenir la signification numérologique d'un nombre."""
        # Réduire le nombre si nécessaire
        if number > 9:
            reduced = self._reduce_number(number)
        else:
            reduced = number
        
        # Retourner la signification
        return self.number_meanings.get(reduced, {
            'energy': 'Inconnu',
            'characteristics': [],
            'strength': 0.5,
            'favorable_for': [],
            'unfavorable_for': []
        })
    
    def _get_master_number_meaning(self, number):
        """Obtenir la signification d'un nombre maître."""
        if number in self.master_numbers:
            return self.master_meanings.get(number, {})
        
        # Si ce n'est pas un nombre maître, retourner la signification du nombre réduit
        return self._get_number_meaning(number)
    
    def _calculate_number_compatibility(self, num1, num2):
        """Calculer la compatibilité entre deux nombres."""
        # Réduire les nombres si nécessaire
        reduced1 = self._reduce_number(num1)
        reduced2 = self._reduce_number(num2)
        
        # Obtenir la compatibilité depuis la matrice
        compatibility = self.number_compatibility.get(reduced1, {}).get(reduced2, 0.5)
        
        return compatibility
    
    def _calculate_karmic_vibration(self, home_score, away_score):
        """Calculer la vibration karmique d'un score."""
        # Calculer la différence et la somme
        difference = abs(home_score - away_score)
        total = home_score + away_score
        
        # Voir si des nombres maîtres sont présents
        has_master = home_score in self.master_numbers or away_score in self.master_numbers or total in self.master_numbers
        
        # Réduire les nombres
        reduced_home = self._reduce_number(home_score)
        reduced_away = self._reduce_number(away_score)
        reduced_total = self._reduce_number(total)
        reduced_diff = self._reduce_number(difference)
        
        # Calculer la vibration karmique
        karmic_base = (reduced_home + reduced_away + reduced_total + reduced_diff) / 4
        
        # Ajuster selon la présence de nombres maîtres
        if has_master:
            karmic_base *= 1.2
        
        # Ajuster selon les nombres premiers
        if self._is_prime(home_score) or self._is_prime(away_score):
            karmic_base *= 1.1
        
        # Normaliser entre 0 et 1
        karmic_vibration = min(1.0, karmic_base / 9)
        
        return karmic_vibration
    
    def _calculate_destiny_number(self, name):
        """Calculer le nombre de destinée à partir d'un nom."""
        # Tableau de correspondance alphabétique
        letter_values = {
            'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
            'j': 1, 'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 6, 'p': 7, 'q': 8, 'r': 9,
            's': 1, 't': 2, 'u': 3, 'v': 4, 'w': 5, 'x': 6, 'y': 7, 'z': 8
        }
        
        # Nettoyer et convertir le nom
        name = name.lower().replace(' ', '')
        
        # Calculer la somme
        name_sum = sum(letter_values.get(letter, 0) for letter in name)
        
        # Réduire à un seul chiffre
        return self._reduce_number(name_sum)
    
    def _calculate_number_balance(self, frequency):
        """Calculer l'équilibre des nombres dans une équipe."""
        # Si aucun nombre, retourner un équilibre moyen
        if not frequency:
            return 0.5
        
        # Calculer les écarts à la distribution idéale
        total_numbers = sum(frequency.values())
        ideal_per_number = total_numbers / 9  # Distribution idéale entre les 9 nombres
        
        # Somme des écarts carrés
        variance = sum((count - ideal_per_number) ** 2 for count in frequency.values())
        
        # Normaliser l'écart
        balance = 1.0 - min(1.0, math.sqrt(variance) / total_numbers)
        
        return balance
    
    def _identify_team_number_strengths(self, frequency, master_numbers):
        """Identifier les forces numériques d'une équipe."""
        strengths = []
        
        # Forces basées sur les fréquences
        dominant_numbers = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        
        if dominant_numbers:
            top_number, count = dominant_numbers[0]
            if count >= 3:
                strengths.append(f"Force collective du nombre {top_number}: {self._get_number_meaning(top_number).get('energy', '')}")
        
        # Forces basées sur les nombres maîtres
        if master_numbers:
            strengths.append(f"Présence de {len(master_numbers)} nombre(s) maître(s): vitalité et potentiel supérieur")
        
        # Forces basées sur l'équilibre des nombres
        balance = self._calculate_number_balance(frequency)
        if balance > 0.7:
            strengths.append("Équilibre harmonieux des énergies numérologiques")
        
        # Forces basées sur les combinaisons spécifiques
        if 1 in frequency and 8 in frequency:
            strengths.append("Combinaison leadership (1) et succès (8): force compétitive")
        if 3 in frequency and 6 in frequency:
            strengths.append("Combinaison créativité (3) et harmonie (6): jeu collectif inspiré")
        if 7 in frequency and 9 in frequency:
            strengths.append("Combinaison analyse (7) et accomplissement (9): maturité tactique")
        
        return strengths
    
    def _identify_team_number_weaknesses(self, frequency, master_numbers):
        """Identifier les faiblesses numériques d'une équipe."""
        weaknesses = []
        
        # Faiblesses basées sur les nombres manquants
        missing_numbers = [i for i in range(1, 10) if i not in frequency]
        if missing_numbers:
            energies = [self._get_number_meaning(num).get('energy', '') for num in missing_numbers]
            weakness_str = f"Absence des énergies: {', '.join(energies[:2])}"
            weaknesses.append(weakness_str)
        
        # Faiblesses basées sur les déséquilibres
        balance = self._calculate_number_balance(frequency)
        if balance < 0.4:
            weaknesses.append("Déséquilibre des énergies numériques: manque de polyvalence")
        
        # Faiblesses basées sur les excès
        excessive_numbers = [(num, count) for num, count in frequency.items() if count > 3]
        if excessive_numbers:
            num, count = excessive_numbers[0]
            weaknesses.append(f"Excès d'énergie {num}: {self._get_number_meaning(num).get('unfavorable_for', ['déséquilibre'])[0]}")
        
        # Faiblesses basées sur les combinaisons problématiques
        if 1 in frequency and 4 in frequency and frequency.get(1, 0) > 2 and frequency.get(4, 0) > 2:
            weaknesses.append("Conflit entre leadership individuel (1) et structure rigide (4)")
        if 5 in frequency and 8 in frequency and frequency.get(5, 0) > 2 and frequency.get(8, 0) > 2:
            weaknesses.append("Tension entre changement (5) et pouvoir établi (8)")
        
        return weaknesses
    
    def _suggest_optimal_playing_style(self, frequency, team_number):
        """Suggérer un style de jeu optimal basé sur la numérologie de l'équipe."""
        # Styles de jeu par nombre dominant
        styles = {
            1: "Offensif, basé sur des individualités fortes",
            2: "Défensif, patient et équilibré",
            3: "Créatif, expressif et offensif",
            4: "Structuré, discipliné et méthodique",
            5: "Adaptable, dynamique et imprévisible",
            6: "Harmonieux, collectif et élégant",
            7: "Stratégique, analytique et précis",
            8: "Dominant, puissant et ambitieux",
            9: "Expérimenté, complet et inspirant"
        }
        
        # Déterminer les nombres dominants
        dominant_numbers = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        
        # Style suggéré basé sur le nombre d'équipe global
        suggested_style = styles.get(team_number, "Style équilibré")
        
        # Ajouts basés sur les combinaisons
        style_influences = []
        
        # Vérifier les combinaisons spécifiques
        if 1 in frequency and 3 in frequency and frequency.get(1, 0) >= 2 and frequency.get(3, 0) >= 2:
            style_influences.append("Offensif créatif")
        if 2 in frequency and 4 in frequency and frequency.get(2, 0) >= 2 and frequency.get(4, 0) >= 2:
            style_influences.append("Défensif compact")
        if 5 in frequency and 3 in frequency and frequency.get(5, 0) >= 2 and frequency.get(3, 0) >= 2:
            style_influences.append("Contre-attaques rapides")
        if 6 in frequency and 8 in frequency and frequency.get(6, 0) >= 2 and frequency.get(8, 0) >= 2:
            style_influences.append("Dominant collectif")
        if 7 in frequency and 9 in frequency and frequency.get(7, 0) >= 2 and frequency.get(9, 0) >= 2:
            style_influences.append("Tactique mature")
        
        # Préparer la suggestion
        if style_influences:
            suggested_style += f" avec des éléments de {', '.join(style_influences)}"
        
        return suggested_style
    
    def _identify_life_path_strengths(self, life_path):
        """Identifier les forces naturelles basées sur le chemin de vie."""
        strengths = []
        
        # Forces selon le chemin de vie
        life_path_meaning = self._get_number_meaning(life_path) if life_path not in self.master_numbers else self._get_master_number_meaning(life_path)
        
        # Ajouter les forces principales
        for strength in life_path_meaning.get('favorable_for', [])[:3]:
            strengths.append(f"{strength.capitalize()}")
        
        # Ajouter des forces spécifiques selon le chemin de vie
        if life_path == 1:
            strengths.append("Culture de leaders et d'innovateurs")
        elif life_path == 2:
            strengths.append("Excellence dans la cohésion d'équipe")
        elif life_path == 3:
            strengths.append("Expression créative et offensive inspirée")
        elif life_path == 4:
            strengths.append("Organisation défensive solide")
        elif life_path == 5:
            strengths.append("Adaptabilité tactique exceptionnelle")
        elif life_path == 6:
            strengths.append("Harmonie et équilibre collectif")
        elif life_path == 7:
            strengths.append("Intelligence tactique supérieure")
        elif life_path == 8:
            strengths.append("Mentalité de champions et ambition")
        elif life_path == 9:
            strengths.append("Sagesse et expérience collective")
        elif life_path == 11:
            strengths.append("Intuition et inspiration hors du commun")
        elif life_path == 22:
            strengths.append("Capacité à construire des succès majeurs")
        elif life_path == 33:
            strengths.append("Développement exceptionnel des jeunes talents")
        
        return strengths
    
    def _identify_life_path_challenges(self, life_path):
        """Identifier les défis naturels basés sur le chemin de vie."""
        challenges = []
        
        # Défis selon le chemin de vie
        life_path_meaning = self._get_number_meaning(life_path) if life_path not in self.master_numbers else self._get_master_number_meaning(life_path)
        
        # Ajouter les défis principaux
        for challenge in life_path_meaning.get('unfavorable_for', [])[:2]:
            challenges.append(f"{challenge.capitalize()}")
        
        # Ajouter des défis spécifiques selon le chemin de vie
        if life_path == 1:
            challenges.append("Difficulté avec le jeu collectif")
        elif life_path == 2:
            challenges.append("Manque d'initiative et de prise de risque")
        elif life_path == 3:
            challenges.append("Manque de rigueur défensive")
        elif life_path == 4:
            challenges.append("Rigidité tactique et manque de créativité")
        elif life_path == 5:
            challenges.append("Instabilité et inconstance dans les performances")
        elif life_path == 6:
            challenges.append("Difficulté lors des déplacements difficiles")
        elif life_path == 7:
            challenges.append("Overthinking tactique, manque d'instinct")
        elif life_path == 8:
            challenges.append("Pression excessive et gestion des attentes")
        elif life_path == 9:
            challenges.append("Adaptation aux nouvelles générations")
        elif life_path == 11:
            challenges.append("Gestion de la pression dans les moments clés")
        elif life_path == 22:
            challenges.append("Trop de focus sur le long terme vs présent")
        elif life_path == 33:
            challenges.append("Sacrifice de résultats immédiats pour développement")
        
        return challenges
    
    def _suggest_development_path(self, life_path, destiny_number=None):
        """Suggérer un chemin de développement optimal pour une équipe."""
        # Base de développement sur le chemin de vie
        development_path = ""
        
        if life_path == 1:
            development_path = "Développer le leadership et l'innovation tout en renforçant la cohésion d'équipe"
        elif life_path == 2:
            development_path = "Renforcer la résilience collective tout en développant plus d'audace offensive"
        elif life_path == 3:
            development_path = "Canaliser la créativité offensive en ajoutant plus de structure défensive"
        elif life_path == 4:
            development_path = "Maintenir la solidité structurelle tout en intégrant plus de flexibilité tactique"
        elif life_path == 5:
            development_path = "Équilibrer l'adaptabilité avec plus de constance dans les performances"
        elif life_path == 6:
            development_path = "Construire sur l'harmonie collective tout en développant plus de caractère à l'extérieur"
        elif life_path == 7:
            development_path = "Utiliser l'intelligence tactique tout en développant l'instinct de tueur"
        elif life_path == 8:
            development_path = "Canaliser l'ambition en force constante tout en gérant les attentes"
        elif life_path == 9:
            development_path = "Capitaliser sur l'expérience tout en intégrant la jeunesse et l'innovation"
        elif life_path == 11:
            development_path = "Transformer l'inspiration en résultats concrets tout en gérant la pression"
        elif life_path == 22:
            development_path = "Construire des fondations solides pour un succès durable et spectaculaire"
        elif life_path == 33:
            development_path = "Créer un environnement de développement exceptionnel tout en visant les titres"
        
        # Intégrer le nombre de destinée si disponible
        if destiny_number:
            destiny_meaning = self._get_number_meaning(destiny_number)
            destiny_focus = destiny_meaning.get('characteristics', [])[0] if destiny_meaning.get('characteristics', []) else ''
            
            if destiny_focus:
                development_path += f", avec un accent particulier sur {destiny_focus}"
        
        return development_path
    
    def _interpret_karmic_score(self, karmic_vibration, is_mirror_score):
        """Interpréter la signification karmique d'un score."""
        interpretation = ""
        
        if karmic_vibration > 0.8:
            interpretation = "Score à très forte résonance karmique, indiquant un moment de justice cosmique ou équilibre rétabli"
        elif karmic_vibration > 0.6:
            interpretation = "Score à forte charge karmique, suggérant un règlement de comptes ou une dette sportive remboursée"
        elif karmic_vibration > 0.4:
            interpretation = "Score avec une influence karmique modérée, reflétant potentiellement des cycles ou tendances"
        else:
            interpretation = "Score avec peu de résonance karmique, résultat principalement basé sur les performances du jour"
        
        # Ajouter des détails pour les scores miroirs
        if is_mirror_score:
            interpretation += ". Le score miroir amplifie la symétrie karmique, suggérant un équilibre parfait des énergies"
        
        return interpretation
    
    def _classify_karmic_level(self, karmic_vibration):
        """Classifier le niveau karmique."""
        if karmic_vibration > 0.8:
            return "très élevé"
        elif karmic_vibration > 0.6:
            return "élevé"
        elif karmic_vibration > 0.4:
            return "modéré"
        elif karmic_vibration > 0.2:
            return "faible"
        else:
            return "très faible"
    
    def _interpret_score_harmony(self, score_compatibility, is_mirror_score):
        """Interpréter l'harmonie numérologique d'un score."""
        interpretation = ""
        
        if score_compatibility > 0.8:
            interpretation = "Score avec une très forte harmonie numérologique, indiquant un résultat aligné avec les forces cosmiques"
        elif score_compatibility > 0.6:
            interpretation = "Score avec une bonne harmonie numérologique, suggérant un résultat naturel et équilibré"
        elif score_compatibility > 0.4:
            interpretation = "Score avec une harmonie modérée, reflétant un résultat acceptable mais pas idéal"
        else:
            interpretation = "Score avec une faible harmonie numérologique, suggérant un résultat contre-nature ou forcé"
        
        # Ajouter des détails pour les scores miroirs
        if is_mirror_score:
            interpretation += ". Le score miroir renforce l'idée d'équilibre parfait entre les forces en présence"
        
        return interpretation
    
    def _classify_harmony_level(self, compatibility):
        """Classifier le niveau d'harmonie."""
        if compatibility > 0.8:
            return "très élevé"
        elif compatibility > 0.6:
            return "élevé"
        elif compatibility > 0.4:
            return "modéré"
        elif compatibility > 0.2:
            return "faible"
        else:
            return "très faible"
    
    def _interpret_life_destiny_harmony(self, compatibility):
        """Interpréter l'harmonie entre chemin de vie et destinée."""
        if compatibility > 0.8:
            return "Harmonie exceptionnelle entre l'identité profonde de l'équipe et sa manifestation extérieure"
        elif compatibility > 0.6:
            return "Bonne cohérence entre les valeurs fondamentales et l'image de l'équipe"
        elif compatibility > 0.4:
            return "Équilibre acceptable entre histoire et identité actuelle"
        else:
            return "Potentiel conflit entre les racines historiques et l'identité actuelle"
    
    def _check_special_resonances(self, match_date, foundation1, foundation2, life_path1, life_path2):
        """Vérifier les résonances numériques spéciales entre les équipes et la date."""
        resonances = []
        
        # Vérifier les cycles
        years_between_foundations = abs(foundation1.year - foundation2.year)
        days_between_foundations = abs((foundation1 - foundation2).days)
        
        # Résonance si l'écart en années est un nombre significatif
        if self._is_prime(years_between_foundations):
            resonances.append({
                'type': 'écart_fondation_premier',
                'description': f"L'écart de {years_between_foundations} ans entre les fondations est un nombre premier",
                'strength': 0.7
            })
        
        # Résonance si le match tombe à une date anniversaire
        days_since_foundation1 = (match_date - foundation1).days
        days_since_foundation2 = (match_date - foundation2).days
        
        if days_since_foundation1 % 1000 < 5 or days_since_foundation1 % 1000 > 995:
            resonances.append({
                'type': 'milestone_team1',
                'description': f"Le match se joue près d'un jalon de {days_since_foundation1//1000}000 jours depuis la fondation de {life_path1}",
                'strength': 0.8
            })
        
        if days_since_foundation2 % 1000 < 5 or days_since_foundation2 % 1000 > 995:
            resonances.append({
                'type': 'milestone_team2',
                'description': f"Le match se joue près d'un jalon de {days_since_foundation2//1000}000 jours depuis la fondation de {life_path2}",
                'strength': 0.8
            })
        
        # Résonance si la date du match a une forte connexion avec les chemins de vie
        match_number = self._reduce_number(match_date.day + match_date.month + match_date.year)
        
        if match_number == life_path1:
            resonances.append({
                'type': 'match_life_path1',
                'description': f"Le numéro de la date du match ({match_number}) correspond exactement au chemin de vie de l'équipe 1",
                'strength': 0.9
            })
        
        if match_number == life_path2:
            resonances.append({
                'type': 'match_life_path2',
                'description': f"Le numéro de la date du match ({match_number}) correspond exactement au chemin de vie de l'équipe 2",
                'strength': 0.9
            })
        
        # Résonance si les chemins de vie sont complémentaires (somme = 10)
        if life_path1 + life_path2 == 10:
            resonances.append({
                'type': 'complémentarité_vie',
                'description': f"Les chemins de vie des équipes ({life_path1} et {life_path2}) sont parfaitement complémentaires (somme = 10)",
                'strength': 0.85
            })
        
        # Résonance si le match tombe un jour de vibration spéciale
        weekday = match_date.weekday()
        if weekday == 0 and match_number == 1:  # Lundi (2) avec énergie 1
            resonances.append({
                'type': 'jour_energie',
                'description': "Match un lundi avec énergie 1: puissance initiatique amplifiée",
                'strength': 0.75
            })
        elif weekday == 6 and match_number == 7:  # Samedi (7) avec énergie 7
            resonances.append({
                'type': 'jour_energie',
                'description': "Match un samedi avec énergie 7: amplification de l'intuition et sagesse",
                'strength': 0.8
            })
        
        return resonances
    
    def _analyze_jersey_compatibility(self, team1_jerseys, team2_jerseys):
        """Analyser la compatibilité entre les numéros de maillot de deux équipes."""
        # Calculer les nombres d'équipe
        team1_sum = sum(team1_jerseys)
        team2_sum = sum(team2_jerseys)
        
        team1_number = self._reduce_number(team1_sum)
        team2_number = self._reduce_number(team2_sum)
        
        # Calculer la compatibilité
        jersey_compatibility = self._calculate_number_compatibility(team1_number, team2_number)
        
        # Vérifier les oppositions ou renforcements spécifiques
        opposing_pairs = 0
        reinforcing_pairs = 0
        
        for num1 in team1_jerseys:
            reduced1 = self._reduce_number(num1)
            for num2 in team2_jerseys:
                reduced2 = self._reduce_number(num2)
                
                # Opposition (somme = 10)
                if reduced1 + reduced2 == 10:
                    opposing_pairs += 1
                
                # Renforcement (même nombre)
                if reduced1 == reduced2:
                    reinforcing_pairs += 1
        
        # Résultat de l'analyse
        return {
            'team1_number': team1_number,
            'team2_number': team2_number,
            'compatibility': jersey_compatibility,
            'opposing_pairs': opposing_pairs,
            'reinforcing_pairs': reinforcing_pairs,
            'compatibility_level': self._classify_compatibility_level(jersey_compatibility),
            'jersey_influence': self._interpret_jersey_influence(jersey_compatibility, opposing_pairs, reinforcing_pairs)
        }
    
    def _classify_compatibility_level(self, compatibility):
        """Classifier le niveau de compatibilité."""
        if compatibility > 0.8:
            return "très élevé"
        elif compatibility > 0.6:
            return "élevé"
        elif compatibility > 0.4:
            return "modéré"
        elif compatibility > 0.2:
            return "faible"
        else:
            return "très faible"
    
    def _classify_advantage_level(self, advantage):
        """Classifier le niveau d'avantage."""
        if advantage > 0.3:
            return "significatif"
        elif advantage > 0.2:
            return "notable"
        elif advantage > 0.1:
            return "léger"
        else:
            return "minime"
    
    def _interpret_jersey_influence(self, compatibility, opposing_pairs, reinforcing_pairs):
        """Interpréter l'influence des numéros de maillot."""
        interpretation = ""
        
        if compatibility > 0.7:
            base = "Les numéros de maillot créent une atmosphère harmonieuse"
        elif compatibility > 0.5:
            base = "Les numéros de maillot créent une atmosphère équilibrée"
        elif compatibility > 0.3:
            base = "Les numéros de maillot créent une légère tension"
        else:
            base = "Les numéros de maillot créent une forte tension énergétique"
        
        # Ajouter des détails sur les paires
        if opposing_pairs > reinforcing_pairs and opposing_pairs > 2:
            interpretation = f"{base}, avec {opposing_pairs} oppositions directes qui favorisent un match disputé"
        elif reinforcing_pairs > opposing_pairs and reinforcing_pairs > 2:
            interpretation = f"{base}, avec {reinforcing_pairs} paires de renforcement qui favorisent un match fluide"
        else:
            interpretation = f"{base} entre les équipes"
        
        return interpretation
    
    def _identify_favorable_aspects(self, date_numerology, personal_day_meaning):
        """Identifier les aspects favorables d'une date."""
        favorable_aspects = []
        
        # Aspects basés sur les caractéristiques spéciales de la date
        special = date_numerology['special_characteristics']
        
        if special['contains_master_numbers']:
            favorable_aspects.append("Présence de nombres maîtres: énergie supérieure")
        
        if special['is_mirror_date']:
            favorable_aspects.append("Date miroir: équilibre énergétique et harmonie")
        
        if special['is_prime_date']:
            favorable_aspects.append("Date prime: énergie unique et indivisible")
        
        # Aspects basés sur le jour personnel
        if personal_day_meaning.get('favorable_for'):
            favorable_aspects.append(f"Jour personnel favorable pour: {personal_day_meaning['favorable_for'][0]}")
        
        # Aspects basés sur l'énergie de la date
        date_energy = date_numerology['numerological_meaning']['date_energy']
        if date_energy:
            favorable_aspects.append(f"Énergie du jour: {date_energy}")
        
        return favorable_aspects
    
    def _detect_victory_cycles(self, win_cycle, team1_name, team2_name):
        """Détecter les cycles de victoire dans l'historique des confrontations."""
        cycles = []
        
        # Compter les séquences
        current_streak = 1
        current_winner = win_cycle[0] if win_cycle else None
        
        for i in range(1, len(win_cycle)):
            if win_cycle[i] == current_winner:
                current_streak += 1
            else:
                # Enregistrer la séquence si elle est significative
                if current_streak >= 3:
                    cycles.append({
                        'type': 'winning_streak',
                        'team': current_winner,
                        'length': current_streak,
                        'description': f"Série de {current_streak} victoires consécutives pour {team1_name if current_winner == 'team1_win' else team2_name}"
                    })
                
                # Réinitialiser
                current_streak = 1
                current_winner = win_cycle[i]
        
        # Vérifier la dernière séquence
        if current_streak >= 3:
            cycles.append({
                'type': 'winning_streak',
                'team': current_winner,
                'length': current_streak,
                'description': f"Série de {current_streak} victoires consécutives pour {team1_name if current_winner == 'team1_win' else team2_name}"
            })
        
        # Chercher des patterns d'alternance
        alternating_patterns = []
        pattern_length = min(len(win_cycle) // 2, 5)  # Maximum 5 matchs pour une période de pattern
        
        for length in range(2, pattern_length + 1):
            pattern_candidates = []
            
            for i in range(len(win_cycle) - length):
                pattern = win_cycle[i:i+length]
                remaining = win_cycle[i+length:]
                
                # Vérifier si le pattern se répète
                repeats = 0
                for j in range(0, len(remaining), length):
                    if j + length <= len(remaining) and remaining[j:j+length] == pattern:
                        repeats += 1
                
                if repeats > 0:
                    pattern_candidates.append({
                        'pattern': pattern,
                        'repeats': repeats,
                        'start_index': i
                    })
            
            # Ajouter le meilleur pattern de cette longueur
            if pattern_candidates:
                best_pattern = max(pattern_candidates, key=lambda x: x['repeats'])
                pattern_str = []
                
                for result in best_pattern['pattern']:
                    if result == 'team1_win':
                        pattern_str.append(team1_name)
                    elif result == 'team2_win':
                        pattern_str.append(team2_name)
                    else:
                        pattern_str.append("Nul")
                
                alternating_patterns.append({
                    'type': 'alternating_pattern',
                    'pattern': best_pattern['pattern'],
                    'pattern_str': ' → '.join(pattern_str),
                    'length': length,
                    'repeats': best_pattern['repeats'],
                    'description': f"Pattern de {length} matchs: {' → '.join(pattern_str)}, répété {best_pattern['repeats']} fois"
                })
        
        # Ajouter les patterns d'alternance aux cycles
        cycles.extend(alternating_patterns)
        
        return cycles
    
    def _detect_score_patterns(self, score_pattern):
        """Détecter les patterns récurrents dans les scores."""
        if len(score_pattern) < 3:
            return []
        
        patterns = []
        
        # Compter les occurrences de chaque score
        score_counts = {}
        for score in score_pattern:
            if score not in score_counts:
                score_counts[score] = 0
            score_counts[score] += 1
        
        # Identifier les scores récurrents
        recurring_scores = [(score, count) for score, count in score_counts.items() if count >= 2]
        recurring_scores.sort(key=lambda x: x[1], reverse=True)
        
        for score, count in recurring_scores[:3]:  # Top 3 des scores récurrents
            patterns.append({
                'type': 'recurring_score',
                'score': score,
                'occurrences': count,
                'description': f"Score {score} apparu {count} fois dans l'historique"
            })
        
        # Vérifier les tendances de buts
        total_goals = [sum(map(int, score.split('-'))) for score in score_pattern]
        avg_goals = sum(total_goals) / len(total_goals) if total_goals else 0
        
        if avg_goals > 3.5:
            patterns.append({
                'type': 'high_scoring',
                'average': avg_goals,
                'description': f"Confrontations à haute intensité offensive (moyenne de {avg_goals:.1f} buts par match)"
            })
        elif avg_goals < 1.5:
            patterns.append({
                'type': 'low_scoring',
                'average': avg_goals,
                'description': f"Confrontations défensives (moyenne de {avg_goals:.1f} buts par match)"
            })
        
        return patterns
    
    def _detect_number_cycles(self, numbers):
        """Détecter les cycles dans une série de nombres."""
        if len(numbers) < 5:
            return []
        
        cycles = []
        
        # Vérifier les séquences de nombres identiques
        current_streak = 1
        current_number = numbers[0]
        
        for i in range(1, len(numbers)):
            if numbers[i] == current_number:
                current_streak += 1
            else:
                # Enregistrer la séquence si elle est significative
                if current_streak >= 3:
                    cycles.append({
                        'type': 'number_streak',
                        'number': current_number,
                        'length': current_streak,
                        'description': f"Séquence de {current_streak} occurrences consécutives du nombre {current_number}"
                    })
                
                # Réinitialiser
                current_streak = 1
                current_number = numbers[i]
        
        # Vérifier la dernière séquence
        if current_streak >= 3:
            cycles.append({
                'type': 'number_streak',
                'number': current_number,
                'length': current_streak,
                'description': f"Séquence de {current_streak} occurrences consécutives du nombre {current_number}"
            })
        
        # Vérifier les progressions
        # (arithmétique, géométrique, etc.)
        # Pour simplifier, on se concentre sur les progressions linéaires
        
        for i in range(len(numbers) - 3):
            diff1 = numbers[i+1] - numbers[i]
            diff2 = numbers[i+2] - numbers[i+1]
            diff3 = numbers[i+3] - numbers[i+2]
            
            if diff1 == diff2 == diff3 and diff1 != 0:
                cycles.append({
                    'type': 'arithmetic_progression',
                    'start': i,
                    'difference': diff1,
                    'description': f"Progression arithmétique (différence de {diff1}) détectée à partir de l'indice {i}"
                })
                break
        
        return cycles
    
    def _predict_next_favorable_date(self, previous_matches, team1_data, team2_data):
        """Prédire la prochaine date favorable en fonction des patterns historiques."""
        if not previous_matches or len(previous_matches) < 3:
            return None
        
        # Extraire les informations
        dates = []
        results = []
        
        for match in previous_matches:
            date_str = match.get('date')
            if isinstance(date_str, str):
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            else:
                date = date_str
            
            result = match.get('result', '')
            
            dates.append(date)
            results.append(result)
        
        # Identifier les patterns temporels
        date_diffs = []
        for i in range(1, len(dates)):
            date_diffs.append((dates[i] - dates[i-1]).days)
        
        # Calculer l'écart moyen entre les matchs
        avg_diff = sum(date_diffs) / len(date_diffs) if date_diffs else 180  # 6 mois par défaut
        
        # Estimer la prochaine date
        next_date = dates[-1] + datetime.timedelta(days=round(avg_diff))
        
        # Prédire le jour le plus favorable
        # Chercher dans une fenêtre de 7 jours autour de cette date
        window_start = next_date - datetime.timedelta(days=3)
        window_end = next_date + datetime.timedelta(days=3)
        
        # Extraire les données des équipes
        team1_foundation = team1_data.get('foundation_date')
        team2_foundation = team2_data.get('foundation_date')
        
        if isinstance(team1_foundation, str):
            team1_foundation = datetime.datetime.strptime(team1_foundation, '%Y-%m-%d').date()
        if isinstance(team2_foundation, str):
            team2_foundation = datetime.datetime.strptime(team2_foundation, '%Y-%m-%d').date()
        
        # Calculer les chemins de vie
        team1_life_path = self._calculate_life_path_number(team1_foundation)
        team2_life_path = self._calculate_life_path_number(team2_foundation)
        
        # Chercher le jour le plus favorable dans la fenêtre
        best_day = None
        best_compatibility = 0
        
        current_day = window_start
        while current_day <= window_end:
            date_number = self._reduce_number(current_day.day + current_day.month + current_day.year)
            
            # Calculer la compatibilité pour chaque équipe
            team1_compatibility = self._calculate_number_compatibility(team1_life_path, date_number)
            team2_compatibility = self._calculate_number_compatibility(team2_life_path, date_number)
            
            # Prendre la moyenne (match équilibré)
            avg_compatibility = (team1_compatibility + team2_compatibility) / 2
            
            if avg_compatibility > best_compatibility:
                best_compatibility = avg_compatibility
                best_day = current_day
            
            current_day += datetime.timedelta(days=1)
        
        if best_day:
            return {
                'date': best_day.strftime('%Y-%m-%d'),
                'compatibility': best_compatibility,
                'day_of_week': self.day_vibrations[best_day.weekday()]['day'],
                'date_energy': self._get_number_meaning(self._reduce_number(best_day.day + best_day.month + best_day.year)).get('energy', '')
            }
        
        return None
    
    def _predict_next_match_pattern(self, win_cycle, score_pattern, date_numbers, team1_name, team2_name):
        """Prédire le pattern du prochain match en fonction des historiques."""
        if not win_cycle or len(win_cycle) < 3:
            return {
                'confidence': 0.3,
                'prediction': 'Données insuffisantes pour une prédiction fiable'
            }
        
        prediction = ""
        confidence = 0.0
        
        # Vérifier les alternances de victoire
        # Exemple: équipe 1, équipe 2, équipe 1, équipe 2, ...
        alternating = True
        for i in range(1, len(win_cycle)):
            if win_cycle[i] == win_cycle[i-1]:
                alternating = False
                break
        
        if alternating and len(win_cycle) >= 4:
            next_winner = 'team1_win' if win_cycle[-1] == 'team2_win' else 'team2_win'
            prediction = f"Basé sur l'alternance parfaite des victoires, {team1_name if next_winner == 'team1_win' else team2_name} devrait gagner le prochain match"
            confidence = 0.7
        
        # Vérifier les séries consécutives
        else:
            current_streak = 1
            for i in range(len(win_cycle)-2, -1, -1):
                if win_cycle[i] == win_cycle[-1]:
                    current_streak += 1
                else:
                    break
            
            if current_streak >= 3:
                # Forte série en cours
                next_winner = win_cycle[-1]
                prediction = f"Série en cours de {current_streak} victoires pour {team1_name if next_winner == 'team1_win' else team2_name}, tendance à la continuation"
                confidence = 0.65
            elif current_streak >= 2:
                # Série modérée
                next_winner = win_cycle[-1]
                prediction = f"Série de {current_streak} victoires en cours pour {team1_name if next_winner == 'team1_win' else team2_name}, léger avantage pour la continuation"
                confidence = 0.55
            else:
                # Pas de série claire, vérifier les tendances globales
                team1_wins = win_cycle.count('team1_win')
                team2_wins = win_cycle.count('team2_win')
                draws = win_cycle.count('draw')
                
                if team1_wins > team2_wins + 2:
                    prediction = f"Domination historique de {team1_name} ({team1_wins} victoires contre {team2_wins})"
                    confidence = 0.6
                elif team2_wins > team1_wins + 2:
                    prediction = f"Domination historique de {team2_name} ({team2_wins} victoires contre {team1_wins})"
                    confidence = 0.6
                elif draws > team1_wins and draws > team2_wins:
                    prediction = f"Tendance historique aux matchs nuls ({draws} nuls sur {len(win_cycle)} confrontations)"
                    confidence = 0.55
                else:
                    prediction = "Aucun pattern dominant détecté dans l'historique des confrontations"
                    confidence = 0.4
        
        # Vérifier les tendances de score si disponibles
        if score_pattern and len(score_pattern) >= 3:
            score_counts = {}
            for score in score_pattern:
                if score not in score_counts:
                    score_counts[score] = 0
                score_counts[score] += 1
            
            most_common_score = max(score_counts.items(), key=lambda x: x[1])
            
            if most_common_score[1] >= 3 or most_common_score[1] / len(score_pattern) >= 0.4:
                prediction += f" avec une probabilité élevée du score {most_common_score[0]} ({most_common_score[1]} occurrences)"
                confidence += 0.1
        
        return {
            'confidence': min(0.95, confidence),
            'prediction': prediction
        }
    
    def _calculate_energy_level(self, personal_day, essence_numbers):
        """Calculer le niveau d'énergie basé sur le jour personnel et les nombres d'essence."""
        # Base: jour personnel
        base_energy = self._get_number_meaning(personal_day).get('strength', 0.5)
        
        # Influence des nombres d'essence
        essence_energy = self._get_number_meaning(essence_numbers['essence']).get('strength', 0.5)
        
        # Calculer le niveau global
        energy_level = (base_energy * 0.6) + (essence_energy * 0.4)
        
        # Ajuster selon les compatibilités
        compatibility = self._calculate_number_compatibility(personal_day, essence_numbers['essence'])
        
        # Facteur d'ajustement basé sur la compatibilité
        adjustment = (compatibility - 0.5) * 0.2
        
        # Niveau final
        final_level = min(1.0, max(0.0, energy_level + adjustment))
        
        return final_level
    
    def _calculate_performance_potential(self, personal_day, essence_numbers):
        """Calculer le potentiel de performance basé sur les nombres numérologiques."""
        # Base: jour personnel
        day_meaning = self._get_number_meaning(personal_day)
        base_potential = day_meaning.get('strength', 0.5)
        
        # Influence de l'essence
        essence_meaning = self._get_number_meaning(essence_numbers['essence'])
        essence_potential = essence_meaning.get('strength', 0.5)
        
        # Facteur positif si le jour est favorable pour les performances
        favorable_bonus = 0.0
        if 'matchs' in day_meaning.get('favorable_for', []) or 'performance' in day_meaning.get('favorable_for', []):
            favorable_bonus = 0.1
        
        # Facteur négatif si le jour est défavorable
        unfavorable_penalty = 0.0
        if 'matchs' in day_meaning.get('unfavorable_for', []) or 'performance' in day_meaning.get('unfavorable_for', []):
            unfavorable_penalty = 0.1
        
        # Calculer le potentiel final
        performance_potential = (base_potential * 0.5) + (essence_potential * 0.5) + favorable_bonus - unfavorable_penalty
        
        # Limiter à [0, 1]
        return min(1.0, max(0.0, performance_potential))
    
    def _calculate_challenge_level(self, personal_day, essence_numbers):
        """Calculer le niveau de défi basé sur les nombres numérologiques."""
        # Base: jour personnel
        day_meaning = self._get_number_meaning(personal_day)
        
        # Facteurs de défi
        challenge_base = 0.5  # Niveau moyen par défaut
        
        # Ajuster selon les caractéristiques du jour
        if personal_day in [4, 7, 8]:
            challenge_base += 0.1  # Jours plus exigeants
        elif personal_day in [3, 6, 9]:
            challenge_base -= 0.1  # Jours plus fluides
        
        # Ajuster selon la compatibilité avec l'essence
        compatibility = self._calculate_number_compatibility(personal_day, essence_numbers['essence'])
        challenge_adjustment = (0.5 - compatibility) * 0.4  # Moins compatible = plus de défis
        
        # Facteur supplémentaire si le jour est explicitement défavorable
        unfavorable_factor = 0.0
        if 'défis' in day_meaning.get('favorable_for', []) or 'obstacles' in day_meaning.get('favorable_for', []):
            unfavorable_factor = 0.15
        
        # Calculer le niveau final
        challenge_level = challenge_base + challenge_adjustment + unfavorable_factor
        
        # Limiter à [0, 1]
        return min(1.0, max(0.0, challenge_level))
    
    def _generate_personal_day_forecast(self, personal_day, category):
        """Générer une prévision basée sur le jour personnel."""
        # Obtenur la signification du jour
        day_meaning = self._get_number_meaning(personal_day)
        
        # Prévisions selon la catégorie
        if category == 'general':
            forecasts = {
                1: "Jour d'initiative et de leadership. Favorable pour prendre les devants et imposer son style.",
                2: "Jour d'équilibre et de diplomatie. Propice au jeu collectif et aux ajustements tactiques.",
                3: "Jour de créativité et d'expression. Idéal pour un jeu offensif et inspiré.",
                4: "Jour de structure et de discipline. Favorable à une approche méthodique et organisée.",
                5: "Jour de changement et d'adaptabilité. Propice aux surprises tactiques et aux ajustements.",
                6: "Jour d'harmonie et d'équilibre. Favorable à la cohésion d'équipe et au jeu collectif.",
                7: "Jour d'analyse et de précision. Idéal pour une approche stratégique et réfléchie.",
                8: "Jour de pouvoir et d'ambition. Propice aux performances dominantes et décisives.",
                9: "Jour d'accomplissement et de sagesse. Favorable à l'expérience et à la maturité."
            }
        elif category == 'performance':
            forecasts = {
                1: "Potentiel de performance individuelle élevé, particulièrement pour les leaders et joueurs dominants.",
                2: "Performance collective harmonieuse, mais possible manque d'intensité dans les duels.",
                3: "Créativité et flair au rendez-vous, mais risque de négligence défensive.",
                4: "Solidité et fiabilité, particulièrement en défense, mais possible manque de spontanéité.",
                5: "Adaptabilité et réactivité excellentes, mais risque d'inconstance au cours du match.",
                6: "Équilibre et jeu collectif favorisés, particulièrement à domicile.",
                7: "Précision technique et exécution tactique optimales, mais possible overthinking.",
                8: "Performance de haut niveau, particulièrement dans les moments importants.",
                9: "Expérience et maturité en jeu, favorable pour gérer les moments clés."
            }
        elif category == 'team':
            forecasts = {
                1: "Dynamique tournée vers le leadership, certains joueurs peuvent se démarquer fortement.",
                2: "Cohésion d'équipe renforcée, communication fluide entre les lignes.",
                3: "Atmosphère positive et créative, propice aux combinaisons inspirées.",
                4: "Organisation collective solide, chacun connaît et respecte son rôle.",
                5: "Flexibilité et adaptabilité collectives, capacité à changer de système.",
                6: "Harmonie et responsabilité partagée, soutien mutuel entre coéquipiers.",
                7: "Intelligence collective et lecture du jeu supérieure.",
                8: "Ambition et détermination collectives, mentalité de gagnant.",
                9: "Sagesse d'équipe et gestion optimale des différentes phases du match."
            }
        elif category == 'challenges':
            forecasts = {
                1: "Tendance à l'individualisme excessif, risque de manque de jeu collectif.",
                2: "Possible hésitation dans les moments décisifs, manque d'initiative.",
                3: "Risque de déséquilibre défensif en cherchant trop le beau jeu.",
                4: "Risque de rigidité tactique et difficulté à s'adapter aux changements.",
                5: "Possible instabilité et inconstance au cours du match.",
                6: "Difficulté potentielle lors des déplacements ou face à un jeu très physique.",
                7: "Risque de sur-analyse et réaction trop lente aux événements imprévus.",
                8: "Pression et attentes élevées pouvant affecter la performance.",
                9: "Possible difficulté face à des approches très innovantes ou des équipes jeunes."
            }
        else:
            return "Catégorie de prévision non reconnue"
        
        return forecasts.get(personal_day, "Jour personnel non reconnu")