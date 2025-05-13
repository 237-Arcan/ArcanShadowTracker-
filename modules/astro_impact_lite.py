"""
AstroImpact Lite - Module d'analyse des influences astrologiques sur les événements sportifs.
Évalue les transits astrologiques appliqués aux figures clés et équipes.
"""

import math
import datetime
import random
from collections import defaultdict

class AstroImpactLite:
    """
    AstroImpact Lite - Évaluation des transits astrologiques appliqués aux figures clés.
    Analyse l'influence des positions planétaires sur les performances sportives.
    """
    
    def __init__(self):
        """Initialise le module AstroImpact Lite"""
        # Définition des planètes et leur influence
        self.planets = {
            'sun': {
                'name': 'Soleil',
                'domain': 'Vitalité, leadership, ego',
                'orbit': 365.25,  # jours
                'speed': 1.0,     # degrés par jour
                'sport_influence': {
                    'performance': 0.8,
                    'leadership': 0.9,
                    'endurance': 0.7,
                    'creativity': 0.5,
                    'teamwork': 0.4
                }
            },
            'moon': {
                'name': 'Lune',
                'domain': 'Émotions, intuition, réceptivité',
                'orbit': 29.53,   # jours
                'speed': 13.2,    # degrés par jour
                'sport_influence': {
                    'performance': 0.6,
                    'leadership': 0.4,
                    'endurance': 0.5,
                    'creativity': 0.8,
                    'teamwork': 0.7
                }
            },
            'mercury': {
                'name': 'Mercure',
                'domain': 'Communication, intellect, adaptabilité',
                'orbit': 87.97,   # jours
                'speed': 1.6,     # degrés par jour (moyenne)
                'sport_influence': {
                    'performance': 0.5,
                    'leadership': 0.6,
                    'endurance': 0.4,
                    'creativity': 0.7,
                    'teamwork': 0.6
                }
            },
            'venus': {
                'name': 'Vénus',
                'domain': 'Harmonie, valeurs, relations',
                'orbit': 224.7,   # jours
                'speed': 1.2,     # degrés par jour
                'sport_influence': {
                    'performance': 0.5,
                    'leadership': 0.4,
                    'endurance': 0.3,
                    'creativity': 0.8,
                    'teamwork': 0.9
                }
            },
            'mars': {
                'name': 'Mars',
                'domain': 'Action, énergie, combativité',
                'orbit': 686.98,  # jours
                'speed': 0.5,     # degrés par jour
                'sport_influence': {
                    'performance': 0.9,
                    'leadership': 0.7,
                    'endurance': 0.8,
                    'creativity': 0.4,
                    'teamwork': 0.3
                }
            },
            'jupiter': {
                'name': 'Jupiter',
                'domain': 'Expansion, chance, croissance',
                'orbit': 4332.59, # jours (11.86 ans)
                'speed': 0.084,   # degrés par jour
                'sport_influence': {
                    'performance': 0.7,
                    'leadership': 0.8,
                    'endurance': 0.6,
                    'creativity': 0.6,
                    'teamwork': 0.7
                }
            },
            'saturn': {
                'name': 'Saturne',
                'domain': 'Structure, discipline, limites',
                'orbit': 10759.22,# jours (29.46 ans)
                'speed': 0.033,   # degrés par jour
                'sport_influence': {
                    'performance': 0.6,
                    'leadership': 0.5,
                    'endurance': 0.9,
                    'creativity': 0.3,
                    'teamwork': 0.6
                }
            }
        }
        
        # Définition simplifiée des signes du zodiaque
        self.zodiac_signs = {
            'aries': {
                'name': 'Bélier',
                'element': 'Feu',
                'quality': 'Cardinal',
                'ruling_planet': 'mars',
                'degrees': (0, 30),
                'sport_traits': {
                    'style': 'Offensif, direct, énergique',
                    'strengths': ['initiative', 'courage', 'dynamisme'],
                    'weaknesses': ['impatience', 'impulsivité', 'égocentrisme']
                }
            },
            'taurus': {
                'name': 'Taureau',
                'element': 'Terre',
                'quality': 'Fixe',
                'ruling_planet': 'venus',
                'degrees': (30, 60),
                'sport_traits': {
                    'style': 'Stable, endurant, déterminé',
                    'strengths': ['force', 'endurance', 'fiabilité'],
                    'weaknesses': ['rigidité', 'entêtement', 'réticence au changement']
                }
            },
            'gemini': {
                'name': 'Gémeaux',
                'element': 'Air',
                'quality': 'Mutable',
                'ruling_planet': 'mercury',
                'degrees': (60, 90),
                'sport_traits': {
                    'style': 'Adaptable, rapide, technique',
                    'strengths': ['adaptabilité', 'réflexes', 'intelligence tactique'],
                    'weaknesses': ['inconstance', 'dispersion', 'nervosité']
                }
            },
            'cancer': {
                'name': 'Cancer',
                'element': 'Eau',
                'quality': 'Cardinal',
                'ruling_planet': 'moon',
                'degrees': (90, 120),
                'sport_traits': {
                    'style': 'Défensif, intuitif, tenace',
                    'strengths': ['ténacité', 'intuition', 'esprit d\'équipe'],
                    'weaknesses': ['timidité', 'susceptibilité', 'défensivité excessive']
                }
            },
            'leo': {
                'name': 'Lion',
                'element': 'Feu',
                'quality': 'Fixe',
                'ruling_planet': 'sun',
                'degrees': (120, 150),
                'sport_traits': {
                    'style': 'Dominant, spectaculaire, leader',
                    'strengths': ['confiance', 'leadership', 'générosité'],
                    'weaknesses': ['arrogance', 'autoritarisme', 'ego surdimensionné']
                }
            },
            'virgo': {
                'name': 'Vierge',
                'element': 'Terre',
                'quality': 'Mutable',
                'ruling_planet': 'mercury',
                'degrees': (150, 180),
                'sport_traits': {
                    'style': 'Précis, analytique, méthodique',
                    'strengths': ['précision', 'analytique', 'efficacité'],
                    'weaknesses': ['perfectionnisme', 'critique excessive', 'anxiété']
                }
            },
            'libra': {
                'name': 'Balance',
                'element': 'Air',
                'quality': 'Cardinal',
                'ruling_planet': 'venus',
                'degrees': (180, 210),
                'sport_traits': {
                    'style': 'Équilibré, élégant, coopératif',
                    'strengths': ['harmonie', 'diplomatie', 'sens stratégique'],
                    'weaknesses': ['indécision', 'dépendance aux autres', 'évitement des conflits']
                }
            },
            'scorpio': {
                'name': 'Scorpion',
                'element': 'Eau',
                'quality': 'Fixe',
                'ruling_planet': 'mars',
                'degrees': (210, 240),
                'sport_traits': {
                    'style': 'Intense, stratégique, résilient',
                    'strengths': ['détermination', 'intensité', 'résilience'],
                    'weaknesses': ['jalousie', 'vengeance', 'secrets']
                }
            },
            'sagittarius': {
                'name': 'Sagittaire',
                'element': 'Feu',
                'quality': 'Mutable',
                'ruling_planet': 'jupiter',
                'degrees': (240, 270),
                'sport_traits': {
                    'style': 'Aventurier, enthousiaste, optimiste',
                    'strengths': ['optimisme', 'vision globale', 'honnêteté'],
                    'weaknesses': ['imprudence', 'excès', 'dispersion']
                }
            },
            'capricorn': {
                'name': 'Capricorne',
                'element': 'Terre',
                'quality': 'Cardinal',
                'ruling_planet': 'saturn',
                'degrees': (270, 300),
                'sport_traits': {
                    'style': 'Discipliné, ambitieux, structuré',
                    'strengths': ['discipline', 'ambition', 'organisation'],
                    'weaknesses': ['pessimisme', 'rigidité', 'froideur']
                }
            },
            'aquarius': {
                'name': 'Verseau',
                'element': 'Air',
                'quality': 'Fixe',
                'ruling_planet': 'saturn',
                'degrees': (300, 330),
                'sport_traits': {
                    'style': 'Innovant, imprévisible, collectif',
                    'strengths': ['innovation', 'travail d\'équipe', 'originalité'],
                    'weaknesses': ['détachement', 'rebellion', 'impersonnalité']
                }
            },
            'pisces': {
                'name': 'Poissons',
                'element': 'Eau',
                'quality': 'Mutable',
                'ruling_planet': 'jupiter',
                'degrees': (330, 360),
                'sport_traits': {
                    'style': 'Intuitif, fluide, adaptable',
                    'strengths': ['intuition', 'adaptation', 'empathie'],
                    'weaknesses': ['dispersion', 'confusion', 'fuite de la réalité']
                }
            }
        }
        
        # Définition des aspects astrologiques
        self.aspects = {
            'conjunction': {
                'name': 'Conjonction',
                'angle': 0,
                'orb': 8,
                'nature': 'fusion',
                'influence': 1.0,
                'sport_effect': {
                    'positive': 'Amplification des énergies, potentiel accru',
                    'negative': 'Surcharge d\'énergie, confusion des influences'
                }
            },
            'opposition': {
                'name': 'Opposition',
                'angle': 180,
                'orb': 8,
                'nature': 'tension',
                'influence': 0.9,
                'sport_effect': {
                    'positive': 'Équilibre dynamique, dépassement de soi',
                    'negative': 'Conflit interne, polarisation des forces'
                }
            },
            'trine': {
                'name': 'Trigone',
                'angle': 120,
                'orb': 8,
                'nature': 'harmonie',
                'influence': 0.8,
                'sport_effect': {
                    'positive': 'Fluidité, talents naturellement exprimés',
                    'negative': 'Facilité excessive, manque de challenge'
                }
            },
            'square': {
                'name': 'Carré',
                'angle': 90,
                'orb': 7,
                'nature': 'friction',
                'influence': 0.7,
                'sport_effect': {
                    'positive': 'Tension productive, motivation par le défi',
                    'negative': 'Blocages, obstacles, frustration'
                }
            },
            'sextile': {
                'name': 'Sextile',
                'angle': 60,
                'orb': 6,
                'nature': 'opportunité',
                'influence': 0.6,
                'sport_effect': {
                    'positive': 'Opportunités, complémentarité des talents',
                    'negative': 'Opportunités manquées, talents sous-exploités'
                }
            }
        }
        
        # Définition des maisons astrologiques (simplifié)
        self.houses = {
            1: {
                'name': 'Ascendant',
                'domain': 'Identité, apparence, début',
                'sport_domain': 'Style de jeu, première impression, démarrages'
            },
            2: {
                'name': 'Ressources',
                'domain': 'Possessions, valeurs, ressources',
                'sport_domain': 'Ressources physiques, stabilité, endurance'
            },
            3: {
                'name': 'Communication',
                'domain': 'Communication, entourage, déplacements',
                'sport_domain': 'Jeu à l\'extérieur, adaptabilité, coordination'
            },
            4: {
                'name': 'Racines',
                'domain': 'Famille, foyer, origines',
                'sport_domain': 'Jeu à domicile, fondations d\'équipe, tradition'
            },
            5: {
                'name': 'Créativité',
                'domain': 'Créativité, plaisir, expression',
                'sport_domain': 'Créativité technique, prise de risque, spectacle'
            },
            6: {
                'name': 'Service',
                'domain': 'Travail, santé, routine',
                'sport_domain': 'Entraînement, condition physique, discipline'
            },
            7: {
                'name': 'Partenariats',
                'domain': 'Relations, contrats, alliances',
                'sport_domain': 'Adversaires, partenariats, duels directs'
            },
            8: {
                'name': 'Transformation',
                'domain': 'Crises, transformation, pouvoir',
                'sport_domain': 'Moments décisifs, retournements, renaissance'
            },
            9: {
                'name': 'Expansion',
                'domain': 'Philosophie, voyages, expansion',
                'sport_domain': 'Compétitions internationales, vision stratégique'
            },
            10: {
                'name': 'Carrière',
                'domain': 'Carrière, autorité, ambition',
                'sport_domain': 'Accomplissements, leadership, reconnaissance'
            },
            11: {
                'name': 'Collectif',
                'domain': 'Groupes, amis, projets',
                'sport_domain': 'Esprit d\'équipe, objectifs collectifs, innovation'
            },
            12: {
                'name': 'Transcendance',
                'domain': 'Inconscient, spiritualité, épreuves',
                'sport_domain': 'Défis invisibles, sacrifices, intuition profonde'
            }
        }
        
        # Périodes de rétrogradation des planètes (simplifié avec dates approximatives)
        self.retrograde_periods = {
            'mercury': [(datetime.date(2025, 1, 14), datetime.date(2025, 2, 4)),
                      (datetime.date(2025, 5, 19), datetime.date(2025, 6, 11)),
                      (datetime.date(2025, 9, 23), datetime.date(2025, 10, 15)),
                      (datetime.date(2025, 12, 29), datetime.date(2026, 1, 18))],
            'venus': [(datetime.date(2025, 7, 22), datetime.date(2025, 9, 4))],
            'mars': [(datetime.date(2024, 12, 7), datetime.date(2025, 2, 24))]
        }
        
        # Historique des analyses
        self.analysis_history = []
    
    def calculate_planet_positions(self, date=None):
        """
        Calculer les positions planétaires approximatives pour une date donnée.
        
        Args:
            date (datetime.date, optional): Date pour laquelle calculer les positions
            
        Returns:
            dict: Positions des planètes dans les signes du zodiaque
        """
        # Utiliser la date actuelle si non spécifiée
        if date is None:
            date = datetime.date.today()
            
        # Convertir la date en jour de l'année
        day_of_year = date.timetuple().tm_yday
        year = date.year
        
        # Positions approximatives (simplifiées)
        positions = {}
        
        # Pour chaque planète
        for planet_id, planet_data in self.planets.items():
            # Position de base (calculée à partir du jour de l'année)
            base_position = (day_of_year * planet_data['speed']) % 360
            
            # Ajouter un offset basé sur l'année pour simuler les cycles pluriannuels
            year_offset = ((year % 12) * 30) % 360
            position = (base_position + year_offset) % 360
            
            # Déterminer le signe zodiacal
            sign = None
            for sign_id, sign_data in self.zodiac_signs.items():
                start_deg, end_deg = sign_data['degrees']
                if start_deg <= position < end_deg:
                    sign = sign_id
                    break
            
            # Si c'est une période de rétrogradation, ajuster le mouvement
            is_retrograde = False
            if planet_id in self.retrograde_periods:
                for start_date, end_date in self.retrograde_periods[planet_id]:
                    if start_date <= date <= end_date:
                        is_retrograde = True
                        break
            
            # Ajouter à notre dictionnaire de positions
            positions[planet_id] = {
                'sign': sign,
                'degrees': position % 30,  # Position dans le signe (0-29)
                'absolute_degrees': position,  # Position absolue (0-359)
                'retrograde': is_retrograde
            }
        
        return positions
    
    def analyze_date_influence(self, date=None):
        """
        Analyser l'influence astrologique d'une date spécifique pour le sport.
        
        Args:
            date (datetime.date, optional): Date à analyser
            
        Returns:
            dict: Analyse astrologique de la date pour le contexte sportif
        """
        # Utiliser la date actuelle si non spécifiée
        if date is None:
            date = datetime.date.today()
        elif isinstance(date, str):
            try:
                date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                return {'error': 'Format de date invalide. Utilisez YYYY-MM-DD'}
        
        # Calculer les positions planétaires
        planet_positions = self.calculate_planet_positions(date)
        
        # Identifier les aspects importants entre planètes
        significant_aspects = self._identify_aspects(planet_positions)
        
        # Analyser la phase lunaire
        moon_phase = self._calculate_moon_phase(date)
        
        # Évaluer l'influence globale de la date sur différents aspects du sport
        sport_influences = self._evaluate_sport_influences(planet_positions, significant_aspects, moon_phase)
        
        # Déterminer le signe dominant de la journée
        dominant_sign = self._determine_dominant_sign(planet_positions)
        
        # Déterminer si des planètes sont rétrogrades
        retrograde_planets = [planet for planet, data in planet_positions.items() if data.get('retrograde', False)]
        
        # Identifier les alignements spéciaux ou configurations rares
        special_configurations = self._identify_special_configurations(planet_positions)
        
        # Générer les recommandations sportives
        recommendations = self._generate_sport_recommendations(sport_influences, dominant_sign, retrograde_planets)
        
        # Préparer le résultat
        result = {
            'date': date.strftime('%Y-%m-%d'),
            'planet_positions': self._format_planet_positions(planet_positions),
            'moon_phase': moon_phase,
            'significant_aspects': significant_aspects,
            'dominant_sign': {
                'sign': dominant_sign,
                'traits': self.zodiac_signs[dominant_sign]['sport_traits']
            },
            'retrograde_planets': [{'planet': self.planets[p]['name'], 'effect': self._retrograde_effect(p)} for p in retrograde_planets],
            'sport_influences': sport_influences,
            'special_configurations': special_configurations,
            'recommendations': recommendations,
            'analysis_timestamp': datetime.datetime.now().isoformat()
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'date_influence',
            'date': date.strftime('%Y-%m-%d'),
            'result': result
        })
        
        return result
    
    def analyze_match_compatibility(self, date, team1_data, team2_data):
        """
        Analyser la compatibilité astrologique entre deux équipes pour un match.
        
        Args:
            date (str/datetime.date): Date du match
            team1_data (dict): Données de la première équipe (nom, date de fondation)
            team2_data (dict): Données de la deuxième équipe (nom, date de fondation)
            
        Returns:
            dict: Analyse de compatibilité astrologique
        """
        # Convertir la date en objet date si nécessaire
        if isinstance(date, str):
            try:
                match_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                return {'error': 'Format de date invalide. Utilisez YYYY-MM-DD'}
        else:
            match_date = date
        
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
        
        # Obtenir les thémes natals des équipes
        team1_natal = self.calculate_planet_positions(team1_foundation)
        team2_natal = self.calculate_planet_positions(team2_foundation)
        
        # Obtenir les positions planétaires du jour du match
        match_planets = self.calculate_planet_positions(match_date)
        
        # Analyser les transits pour chaque équipe
        team1_transits = self._analyze_transits(match_planets, team1_natal)
        team2_transits = self._analyze_transits(match_planets, team2_natal)
        
        # Analyser la compatibilité entre les équipes
        team_compatibility = self._analyze_team_compatibility(team1_natal, team2_natal)
        
        # Identifier quelle équipe est plus favorisée par l'astrologie du jour
        favored_team = self._determine_favored_team(team1_transits, team2_transits, team_compatibility)
        
        # Identifier les moments clés potentiels du match
        key_moments = self._identify_key_match_moments(match_planets, team1_natal, team2_natal)
        
        # Préparer le résultat
        result = {
            'match_date': match_date.strftime('%Y-%m-%d'),
            'teams': {
                'team1': {
                    'name': team1_name,
                    'foundation_date': team1_foundation.strftime('%Y-%m-%d')
                },
                'team2': {
                    'name': team2_name,
                    'foundation_date': team2_foundation.strftime('%Y-%m-%d')
                }
            },
            'transits': {
                'team1': team1_transits,
                'team2': team2_transits
            },
            'team_compatibility': team_compatibility,
            'astrological_advantage': favored_team,
            'key_moments': key_moments,
            'analysis_timestamp': datetime.datetime.now().isoformat()
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'match_compatibility',
            'match': f"{team1_name} vs {team2_name}",
            'date': match_date.strftime('%Y-%m-%d'),
            'result': result
        })
        
        return result
    
    def analyze_player_profile(self, birth_date, name=None, current_date=None):
        """
        Analyser le profil astrologique d'un joueur et ses transits actuels.
        
        Args:
            birth_date (str/datetime.date): Date de naissance du joueur
            name (str, optional): Nom du joueur
            current_date (str/datetime.date, optional): Date actuelle pour les transits
            
        Returns:
            dict: Analyse astrologique du joueur
        """
        # Convertir la date de naissance en objet date si nécessaire
        if isinstance(birth_date, str):
            try:
                birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d').date()
            except ValueError:
                return {'error': 'Format de date de naissance invalide. Utilisez YYYY-MM-DD'}
        
        # Utiliser la date actuelle pour les transits si non spécifiée
        if current_date is None:
            current_date = datetime.date.today()
        elif isinstance(current_date, str):
            try:
                current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d').date()
            except ValueError:
                return {'error': 'Format de date actuelle invalide. Utilisez YYYY-MM-DD'}
        
        # Calculer le thème natal
        natal_positions = self.calculate_planet_positions(birth_date)
        
        # Calculer les positions planétaires actuelles
        current_positions = self.calculate_planet_positions(current_date)
        
        # Déterminer le signe solaire (signe zodiacal)
        sun_sign = natal_positions['sun']['sign']
        
        # Analyser les aspects dans le thème natal
        natal_aspects = self._identify_aspects(natal_positions)
        
        # Analyser les transits actuels
        transit_aspects = self._analyze_transits(current_positions, natal_positions)
        
        # Générer le profil sportif basé sur le thème natal
        sport_profile = self._generate_player_sport_profile(natal_positions, natal_aspects, sun_sign)
        
        # Déterminer la phase actuelle du joueur (basée sur les transits)
        current_phase = self._determine_player_phase(transit_aspects, current_positions)
        
        # Générer des prédictions pour les performances futures
        performance_prediction = self._predict_player_performance(transit_aspects, current_positions, sport_profile)
        
        # Identifier les périodes favorables à venir
        favorable_periods = self._identify_player_favorable_periods(natal_positions, current_date)
        
        # Préparer le résultat
        result = {
            'player_name': name or "Joueur",
            'birth_date': birth_date.strftime('%Y-%m-%d'),
            'sun_sign': {
                'name': self.zodiac_signs[sun_sign]['name'],
                'traits': self.zodiac_signs[sun_sign]['sport_traits']
            },
            'natal_positions': self._format_planet_positions(natal_positions),
            'significant_natal_aspects': natal_aspects,
            'sport_profile': sport_profile,
            'current_transits': transit_aspects,
            'current_phase': current_phase,
            'performance_prediction': performance_prediction,
            'favorable_periods': favorable_periods,
            'analysis_timestamp': datetime.datetime.now().isoformat()
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'player_profile',
            'player': name or "Joueur",
            'result': result
        })
        
        return result
    
    def find_optimal_match_date(self, team_data, start_date, end_date, opponent_data=None):
        """
        Trouver la date optimale pour un match entre les dates spécifiées.
        
        Args:
            team_data (dict): Données de l'équipe (nom, date de fondation)
            start_date (str/datetime.date): Date de début de la période
            end_date (str/datetime.date): Date de fin de la période
            opponent_data (dict, optional): Données de l'adversaire
            
        Returns:
            dict: Dates favorables et leur analyse
        """
        # Convertir les dates en objets date si nécessaire
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
        
        # Limiter à 90 jours maximum
        max_days = 90
        if (end_date - start_date).days > max_days:
            end_date = start_date + datetime.timedelta(days=max_days)
        
        # Extraire les données de l'équipe
        team_name = team_data.get('name', 'Équipe')
        team_foundation = team_data.get('foundation_date')
        
        if isinstance(team_foundation, str):
            team_foundation = datetime.datetime.strptime(team_foundation, '%Y-%m-%d').date()
        
        # Obtenir le thème natal de l'équipe
        team_natal = self.calculate_planet_positions(team_foundation)
        
        # Préparer la liste des dates à analyser
        date_scores = []
        current_date = start_date
        
        # Si nous avons un adversaire
        opponent_natal = None
        if opponent_data:
            opponent_foundation = opponent_data.get('foundation_date')
            if isinstance(opponent_foundation, str):
                opponent_foundation = datetime.datetime.strptime(opponent_foundation, '%Y-%m-%d').date()
            opponent_natal = self.calculate_planet_positions(opponent_foundation)
        
        # Analyser chaque date dans la période
        while current_date <= end_date:
            # Obtenir les positions planétaires du jour
            day_positions = self.calculate_planet_positions(current_date)
            
            # Calculer un score de favorabilité pour l'équipe
            team_favorable_score = self._calculate_date_favorability(day_positions, team_natal)
            
            # Si nous avons un adversaire, considérer également sa favorabilité
            advantage_score = team_favorable_score
            if opponent_natal:
                opponent_favorable_score = self._calculate_date_favorability(day_positions, opponent_natal)
                advantage_score = team_favorable_score - opponent_favorable_score
            
            # Ajouter la date et son score à notre liste
            date_scores.append({
                'date': current_date,
                'favorable_score': team_favorable_score,
                'advantage_score': advantage_score
            })
            
            # Passer au jour suivant
            current_date += datetime.timedelta(days=1)
        
        # Trier les dates par score d'avantage (ou score favorable si pas d'adversaire)
        if opponent_natal:
            date_scores.sort(key=lambda x: x['advantage_score'], reverse=True)
        else:
            date_scores.sort(key=lambda x: x['favorable_score'], reverse=True)
        
        # Prendre les 5 meilleures dates
        best_dates = date_scores[:5]
        
        # Analyser en détail les meilleures dates
        detailed_dates = []
        for date_info in best_dates:
            date = date_info['date']
            positions = self.calculate_planet_positions(date)
            
            # Analyser les transits favorables
            favorable_transits = self._analyze_transits(positions, team_natal)
            
            # Déterminer les aspects particulièrement favorables
            key_aspects = [aspect for aspect in favorable_transits 
                          if aspect['influence_score'] > 0.7 and aspect['nature'] in ['opportunité', 'harmonie']]
            
            # Analyser l'opposition si disponible
            opposition_analysis = None
            if opponent_natal:
                opposition_transits = self._analyze_transits(positions, opponent_natal)
                opposition_analysis = {
                    'favorable_score': date_info['favorable_score'],
                    'opponent_score': date_info['favorable_score'] - date_info['advantage_score'],
                    'advantage': date_info['advantage_score'],
                    'significant_aspects': [aspect for aspect in opposition_transits 
                                           if aspect['influence_score'] > 0.7]
                }
            
            detailed_dates.append({
                'date': date.strftime('%Y-%m-%d'),
                'favorable_score': date_info['favorable_score'],
                'advantage_score': date_info['advantage_score'],
                'moon_phase': self._calculate_moon_phase(date),
                'key_planetary_positions': [
                    {'planet': self.planets[p]['name'], 
                     'sign': self.zodiac_signs[positions[p]['sign']]['name']}
                    for p in ['sun', 'moon', 'mars', 'jupiter']  # Planètes les plus importantes pour le sport
                ],
                'favorable_transits': key_aspects,
                'opposition_analysis': opposition_analysis
            })
        
        # Préparer le résultat
        result = {
            'team_name': team_name,
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days_analyzed': (end_date - start_date).days + 1
            },
            'optimal_dates': detailed_dates,
            'best_date': detailed_dates[0] if detailed_dates else None,
            'opposition_considered': opponent_natal is not None,
            'analysis_timestamp': datetime.datetime.now().isoformat()
        }
        
        # Ajouter à l'historique
        self.analysis_history.append({
            'type': 'optimal_date_analysis',
            'team': team_name,
            'result': result
        })
        
        return result
    
    def _identify_aspects(self, planet_positions):
        """Identifier les aspects significatifs entre les planètes."""
        significant_aspects = []
        
        # Comparer chaque paire de planètes
        planets = list(planet_positions.keys())
        for i in range(len(planets)):
            for j in range(i + 1, len(planets)):
                planet1 = planets[i]
                planet2 = planets[j]
                
                # Calculer la différence angulaire
                angle1 = planet_positions[planet1]['absolute_degrees']
                angle2 = planet_positions[planet2]['absolute_degrees']
                
                angle_diff = abs(angle1 - angle2)
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff
                
                # Vérifier si cette différence correspond à un aspect
                for aspect_id, aspect_data in self.aspects.items():
                    aspect_angle = aspect_data['angle']
                    orb = aspect_data['orb']
                    
                    if abs(angle_diff - aspect_angle) <= orb:
                        # Calculer la précision de l'aspect (0-1, où 1 est exact)
                        precision = 1 - (abs(angle_diff - aspect_angle) / orb)
                        
                        # L'influence dépend de la précision et de l'importance des planètes
                        influence = precision * aspect_data['influence']
                        
                        # Déterminer si l'aspect est harmonieux ou tendu
                        is_harmonious = aspect_id in ['trine', 'sextile'] or (aspect_id == 'conjunction' and planet1 != 'saturn' and planet2 != 'saturn')
                        
                        significant_aspects.append({
                            'aspect': aspect_data['name'],
                            'planets': [self.planets[planet1]['name'], self.planets[planet2]['name']],
                            'precision': precision,
                            'influence': influence,
                            'nature': aspect_data['nature'],
                            'harmonious': is_harmonious,
                            'sport_effect': aspect_data['sport_effect']['positive'] if is_harmonious else aspect_data['sport_effect']['negative']
                        })
        
        # Trier par influence
        significant_aspects.sort(key=lambda x: x['influence'], reverse=True)
        
        return significant_aspects
    
    def _calculate_moon_phase(self, date):
        """Calculer la phase lunaire approximative."""
        # Position fictive pour la lune basée sur la date
        day_of_year = date.timetuple().tm_yday
        moon_position = (day_of_year * 13) % 30  # Cycle lunaire simplifié
        
        # Phases de la lune
        if 0 <= moon_position < 1:
            phase = "Nouvelle Lune"
            description = "Début de cycle, nouvelle énergie, démarrages"
            sport_influence = "Favorable pour commencer de nouveaux projets, moins favorable pour les performances maximales"
        elif 1 <= moon_position < 7:
            phase = "Premier Croissant"
            description = "Croissance, développement, momentum"
            sport_influence = "Énergie croissante, bon pour le développement progressif"
        elif 7 <= moon_position < 8:
            phase = "Premier Quartier"
            description = "Action, décision, surmonter les obstacles"
            sport_influence = "Énergie active, favorable pour surmonter les défis"
        elif 8 <= moon_position < 14:
            phase = "Gibbeuse Croissante"
            description = "Expansion, réalisation, force croissante"
            sport_influence = "Force et endurance en augmentation, bon pour les performances globales"
        elif 14 <= moon_position < 16:
            phase = "Pleine Lune"
            description = "Culmination, pleine puissance, clarté"
            sport_influence = "Énergie maximale mais émotions intenses, performances potentiellement exceptionnelles"
        elif 16 <= moon_position < 22:
            phase = "Gibbeuse Décroissante"
            description = "Récolte, évaluation, raffinement"
            sport_influence = "Bonne phase pour affiner la technique et consolider les acquis"
        elif 22 <= moon_position < 23:
            phase = "Dernier Quartier"
            description = "Relâchement, lâcher-prise, révision"
            sport_influence = "Phase de relâchement, bonne pour la récupération et l'analyse"
        else:  # 23-30
            phase = "Dernier Croissant"
            description = "Achèvement, préparation, intégration"
            sport_influence = "Période de finalisation et d'intégration, moins d'énergie physique"
        
        return {
            'phase': phase,
            'description': description,
            'sport_influence': sport_influence,
            'energy_level': self._moon_phase_energy_level(moon_position)
        }
    
    def _moon_phase_energy_level(self, moon_position):
        """Déterminer le niveau d'énergie basé sur la phase lunaire."""
        # Pleine lune a la plus haute énergie, nouvelle lune la plus basse
        if 14 <= moon_position < 16:  # Pleine Lune
            return 0.95
        elif 7 <= moon_position < 8 or 22 <= moon_position < 23:  # Quartiers
            return 0.75
        elif 8 <= moon_position < 14 or 16 <= moon_position < 22:  # Gibbeuses
            return 0.85
        elif 1 <= moon_position < 7:  # Croissant
            return 0.6
        else:  # Nouvelle Lune ou Dernier Croissant
            return 0.4
    
    def _evaluate_sport_influences(self, planet_positions, aspects, moon_phase):
        """Évaluer l'influence des positions planétaires sur différents aspects sportifs."""
        # Initialiser les scores d'influence
        influences = {
            'overall_energy': 0.5,  # Niveau d'énergie global
            'team_performance': 0.5,  # Performance d'équipe
            'individual_excellence': 0.5,  # Excellence individuelle
            'strategy_effectiveness': 0.5,  # Efficacité stratégique
            'mental_strength': 0.5,  # Force mentale
            'physical_power': 0.5,  # Puissance physique
            'adaptability': 0.5,  # Adaptabilité
            'leadership': 0.5,  # Leadership
            'home_advantage': 0.5,  # Avantage du terrain
            'risk_taking': 0.5  # Prise de risque
        }
        
        # Influence de la lune
        moon_energy = moon_phase['energy_level']
        influences['overall_energy'] = (influences['overall_energy'] + moon_energy) / 2
        influences['mental_strength'] = (influences['mental_strength'] + moon_energy) / 2
        
        # Influence des planètes selon leur signe
        for planet_id, position in planet_positions.items():
            sign_id = position['sign']
            sign_data = self.zodiac_signs[sign_id]
            
            # Facteur de retrograde (réduit l'influence positive)
            retrograde_factor = 0.7 if position.get('retrograde', False) else 1.0
            
            # Influence selon la planète
            if planet_id == 'sun':
                # Le Soleil influence l'énergie et le leadership
                influences['overall_energy'] += 0.2 * retrograde_factor
                influences['leadership'] += 0.25 * retrograde_factor
                
                # Influence selon le signe
                if sign_data['element'] == 'Feu':
                    influences['individual_excellence'] += 0.15 * retrograde_factor
                elif sign_data['element'] == 'Terre':
                    influences['physical_power'] += 0.15 * retrograde_factor
                elif sign_data['element'] == 'Air':
                    influences['strategy_effectiveness'] += 0.15 * retrograde_factor
                elif sign_data['element'] == 'Eau':
                    influences['mental_strength'] += 0.15 * retrograde_factor
            
            elif planet_id == 'moon':
                # La Lune influence l'intuition et l'adaptabilité
                influences['adaptability'] += 0.2 * retrograde_factor
                influences['mental_strength'] += 0.15 * retrograde_factor
                
                # Influence selon le signe
                if sign_data['element'] == 'Eau':
                    influences['team_performance'] += 0.15 * retrograde_factor
                elif sign_data['element'] == 'Feu':
                    influences['risk_taking'] += 0.15 * retrograde_factor
            
            elif planet_id == 'mars':
                # Mars influence l'énergie physique et l'agressivité
                influences['physical_power'] += 0.25 * retrograde_factor
                influences['risk_taking'] += 0.2 * retrograde_factor
                
                # Influence selon le signe
                if sign_data['element'] == 'Feu':
                    influences['individual_excellence'] += 0.2 * retrograde_factor
                elif sign_data['element'] == 'Eau':
                    influences['mental_strength'] += 0.1 * retrograde_factor
            
            elif planet_id == 'jupiter':
                # Jupiter influence l'expansion et la chance
                influences['team_performance'] += 0.2 * retrograde_factor
                influences['overall_energy'] += 0.15 * retrograde_factor
                
                # Influence selon le signe
                if sign_data['element'] == 'Feu':
                    influences['leadership'] += 0.15 * retrograde_factor
                elif sign_data['element'] == 'Air':
                    influences['strategy_effectiveness'] += 0.15 * retrograde_factor
            
            elif planet_id == 'saturn':
                # Saturne influence la discipline et l'endurance
                influences['mental_strength'] += 0.15 * retrograde_factor
                influences['physical_power'] += 0.1 * retrograde_factor
                
                # Effet rétrograde plus marqué pour Saturne
                if position.get('retrograde', False):
                    influences['overall_energy'] -= 0.15
                    influences['adaptability'] -= 0.1
                
                # Influence selon le signe
                if sign_data['element'] == 'Terre':
                    influences['home_advantage'] += 0.15 * retrograde_factor
        
        # Influence des aspects
        for aspect in aspects:
            aspect_influence = aspect['influence']
            
            if aspect['harmonious']:
                # Aspects harmonieux
                influences['team_performance'] += 0.05 * aspect_influence
                influences['strategy_effectiveness'] += 0.05 * aspect_influence
                
                if 'Mars' in aspect['planets'] or 'Soleil' in aspect['planets']:
                    influences['physical_power'] += 0.1 * aspect_influence
                
                if 'Jupiter' in aspect['planets']:
                    influences['risk_taking'] += 0.1 * aspect_influence
                    influences['overall_energy'] += 0.05 * aspect_influence
                
                if 'Saturne' in aspect['planets']:
                    influences['mental_strength'] += 0.1 * aspect_influence
            else:
                # Aspects tendus
                influences['adaptability'] -= 0.05 * aspect_influence
                
                if 'Mars' in aspect['planets']:
                    influences['risk_taking'] += 0.1 * aspect_influence  # Plus de prise de risque, mais pas forcément bénéfique
                    influences['team_performance'] -= 0.05 * aspect_influence
                
                if 'Saturne' in aspect['planets']:
                    influences['overall_energy'] -= 0.1 * aspect_influence
                    influences['physical_power'] -= 0.05 * aspect_influence
        
        # Limiter les valeurs entre 0.1 et 0.9
        for key in influences:
            influences[key] = max(0.1, min(0.9, influences[key]))
        
        # Générer des interprétations pour chaque influence
        interpretations = {}
        for aspect, value in influences.items():
            interpretations[aspect] = self._interpret_influence_level(aspect, value)
        
        return {
            'scores': influences,
            'interpretations': interpretations
        }
    
    def _interpret_influence_level(self, aspect, value):
        """Interpréter le niveau d'influence pour un aspect sportif."""
        aspect_descriptions = {
            'overall_energy': {
                'high': "Niveau d'énergie très élevé, favorable aux performances intenses",
                'medium': "Niveau d'énergie équilibré, convenable pour la plupart des activités",
                'low': "Niveau d'énergie bas, conservation des forces recommandée"
            },
            'team_performance': {
                'high': "Excellente cohésion d'équipe et synergie collective",
                'medium': "Dynamique d'équipe normale, communication adéquate",
                'low': "Défis potentiels dans la coordination et l'harmonie d'équipe"
            },
            'individual_excellence': {
                'high': "Performances individuelles exceptionnelles, talent mis en valeur",
                'medium': "Contributions individuelles satisfaisantes, niveau habituel",
                'low': "Difficulté à exprimer pleinement les talents individuels"
            },
            'strategy_effectiveness': {
                'high': "Clarté stratégique exceptionnelle, décisions tactiques judicieuses",
                'medium': "Planification stratégique adéquate, adaptations possibles",
                'low': "Confusion tactique possible, révisions stratégiques nécessaires"
            },
            'mental_strength': {
                'high': "Force mentale supérieure, concentration et résilience",
                'medium': "Équilibre mental satisfaisant pour la performance",
                'low': "Vulnérabilité mentale, besoin de renforcement psychologique"
            },
            'physical_power': {
                'high': "Puissance physique maximale, excellent niveau athlétique",
                'medium': "Capacités physiques dans la norme, performance stable",
                'low': "Énergie physique réduite, risque accru de fatigue"
            },
            'adaptability': {
                'high': "Adaptabilité exceptionnelle aux changements de situation",
                'medium': "Capacité d'adaptation normale aux circonstances",
                'low': "Rigidité potentielle, difficulté à s'ajuster aux imprévus"
            },
            'leadership': {
                'high': "Leadership fort et inspirant, influence positive",
                'medium': "Capacités de leadership adéquates, direction stable",
                'low': "Défis dans l'autorité et la direction, besoin de renforcement"
            },
            'home_advantage': {
                'high': "Avantage du terrain amplifié, connexion forte avec l'environnement",
                'medium': "Bénéfice normal de jouer à domicile",
                'low': "Diminution de l'avantage du terrain, neutralité relative"
            },
            'risk_taking': {
                'high': "Propension élevée à la prise de risque, audace tactique",
                'medium': "Équilibre entre prudence et audace",
                'low': "Approche conservatrice privilégiée, minimisation des risques"
            }
        }
        
        if value >= 0.7:
            level = 'high'
        elif value >= 0.4:
            level = 'medium'
        else:
            level = 'low'
        
        return aspect_descriptions[aspect][level]
    
    def _determine_dominant_sign(self, planet_positions):
        """Déterminer le signe zodiacal dominant de la journée."""
        # Compter les occurrences de chaque signe
        sign_counts = defaultdict(int)
        
        # Pondération des planètes (certaines ont plus d'influence)
        planet_weights = {
            'sun': 3,
            'moon': 2,
            'mars': 2,
            'jupiter': 1.5,
            'saturn': 1.5,
            'mercury': 1,
            'venus': 1
        }
        
        for planet, position in planet_positions.items():
            sign = position['sign']
            weight = planet_weights.get(planet, 1)
            sign_counts[sign] += weight
        
        # Déterminer le signe avec le plus grand poids
        dominant_sign = max(sign_counts.items(), key=lambda x: x[1])[0]
        
        return dominant_sign
    
    def _identify_special_configurations(self, planet_positions):
        """Identifier les alignements spéciaux ou configurations planétaires rares."""
        special_configurations = []
        
        # Compter les planètes par signe
        planets_per_sign = defaultdict(list)
        for planet_id, position in planet_positions.items():
            planets_per_sign[position['sign']].append(planet_id)
        
        # Vérifier les stelliums (3+ planètes dans un même signe)
        for sign, planets in planets_per_sign.items():
            if len(planets) >= 3:
                planet_names = [self.planets[p]['name'] for p in planets]
                special_configurations.append({
                    'type': 'stellium',
                    'sign': self.zodiac_signs[sign]['name'],
                    'planets': planet_names,
                    'description': f"Stellium en {self.zodiac_signs[sign]['name']} ({', '.join(planet_names)})",
                    'sport_influence': f"Forte concentration d'énergie {self.zodiac_signs[sign]['element']} influençant le {self.zodiac_signs[sign]['sport_traits']['style']}"
                })
        
        # Vérifier les rétrogradations multiples
        retrograde_planets = [planet_id for planet_id, position in planet_positions.items() 
                             if position.get('retrograde', False)]
        
        if len(retrograde_planets) >= 2:
            planet_names = [self.planets[p]['name'] for p in retrograde_planets]
            special_configurations.append({
                'type': 'multiple_retrogrades',
                'planets': planet_names,
                'description': f"Plusieurs planètes rétrogrades ({', '.join(planet_names)})",
                'sport_influence': "Période de révision et d'intériorisation, potentiellement challengeante pour les performances extérieures"
            })
        
        # Vérifier les oppositions multiples
        oppositions = []
        planets = list(planet_positions.keys())
        for i in range(len(planets)):
            for j in range(i + 1, len(planets)):
                planet1 = planets[i]
                planet2 = planets[j]
                
                # Calculer la différence angulaire
                angle1 = planet_positions[planet1]['absolute_degrees']
                angle2 = planet_positions[planet2]['absolute_degrees']
                
                angle_diff = abs(angle1 - angle2)
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff
                
                # Vérifier si c'est une opposition
                if abs(angle_diff - 180) <= 8:
                    oppositions.append((planet1, planet2))
        
        if len(oppositions) >= 2:
            opposition_desc = [f"{self.planets[p1]['name']}-{self.planets[p2]['name']}" for p1, p2 in oppositions]
            special_configurations.append({
                'type': 'multiple_oppositions',
                'oppositions': opposition_desc,
                'description': f"Multiples oppositions planétaires ({', '.join(opposition_desc)})",
                'sport_influence': "Tensions dynamiques créant à la fois des défis et des opportunités de dépassement"
            })
        
        # Vérifier les configurations en T (deux planètes en opposition, une troisième en carré aux deux)
        t_squares = []
        for p1, p2 in oppositions:
            for p3 in planets:
                if p3 != p1 and p3 != p2:
                    # Vérifier si p3 forme un carré avec p1 et p2
                    angle1 = abs(planet_positions[p1]['absolute_degrees'] - planet_positions[p3]['absolute_degrees'])
                    if angle1 > 180:
                        angle1 = 360 - angle1
                        
                    angle2 = abs(planet_positions[p2]['absolute_degrees'] - planet_positions[p3]['absolute_degrees'])
                    if angle2 > 180:
                        angle2 = 360 - angle2
                    
                    if abs(angle1 - 90) <= 8 and abs(angle2 - 90) <= 8:
                        t_squares.append((p1, p2, p3))
        
        if t_squares:
            t_square_desc = [f"{self.planets[p1]['name']}-{self.planets[p2]['name']}-{self.planets[p3]['name']}" for p1, p2, p3 in t_squares]
            special_configurations.append({
                'type': 't_square',
                'configurations': t_square_desc,
                'description': f"Configuration en T ({', '.join(t_square_desc)})",
                'sport_influence': "Tension productive motivant l'action et le dépassement des obstacles"
            })
        
        return special_configurations
    
    def _generate_sport_recommendations(self, sport_influences, dominant_sign, retrograde_planets):
        """Générer des recommandations sportives basées sur l'analyse astrologique."""
        recommendations = []
        
        # Extraire les scores d'influence
        scores = sport_influences['scores']
        
        # Recommandations basées sur l'énergie globale
        energy_score = scores['overall_energy']
        if energy_score > 0.7:
            recommendations.append({
                'aspect': 'overall_energy',
                'recommendation': "Profiter du haut niveau d'énergie pour des performances maximales",
                'priority': 'high'
            })
        elif energy_score < 0.4:
            recommendations.append({
                'aspect': 'overall_energy',
                'recommendation': "Privilégier la récupération et la conservation d'énergie",
                'priority': 'high'
            })
        
        # Recommandations basées sur le signe dominant
        sign_traits = self.zodiac_signs[dominant_sign]['sport_traits']
        recommendations.append({
            'aspect': 'play_style',
            'recommendation': f"Adapter le style de jeu pour favoriser: {sign_traits['style']}",
            'priority': 'medium'
        })
        
        # Si des planètes sont rétrogrades
        if retrograde_planets:
            if 'mars' in retrograde_planets:
                recommendations.append({
                    'aspect': 'energy_management',
                    'recommendation': "Attention à la gestion de l'énergie et des actions impulsives, risque de blocages",
                    'priority': 'high'
                })
            if 'mercury' in retrograde_planets:
                recommendations.append({
                    'aspect': 'communication',
                    'recommendation': "Clarifier toutes les communications tactiques pour éviter les malentendus",
                    'priority': 'medium'
                })
        
        # Recommandations basées sur les performances d'équipe vs individuelles
        team_score = scores['team_performance']
        indiv_score = scores['individual_excellence']
        
        if team_score > indiv_score + 0.2:
            recommendations.append({
                'aspect': 'team_focus',
                'recommendation': "Miser sur le jeu collectif plutôt que les performances individuelles",
                'priority': 'high'
            })
        elif indiv_score > team_score + 0.2:
            recommendations.append({
                'aspect': 'individual_focus',
                'recommendation': "Laisser s'exprimer les talents individuels et les joueurs clés",
                'priority': 'high'
            })
        
        # Recommandation sur la prise de risque
        risk_score = scores['risk_taking']
        if risk_score > 0.7:
            recommendations.append({
                'aspect': 'strategy',
                'recommendation': "Jour favorable pour les approches audacieuses et innovations tactiques",
                'priority': 'medium'
            })
        elif risk_score < 0.4:
            recommendations.append({
                'aspect': 'strategy',
                'recommendation': "Privilégier une approche conservatrice et des tactiques éprouvées",
                'priority': 'medium'
            })
        
        # Recommandation sur la préparation mentale
        mental_score = scores['mental_strength']
        if mental_score < 0.5:
            recommendations.append({
                'aspect': 'mental_preparation',
                'recommendation': "Renforcer la préparation mentale et la concentration avant la compétition",
                'priority': 'high'
            })
        
        # Trier par priorité
        recommendations.sort(key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x['priority']])
        
        return recommendations
    
    def _format_planet_positions(self, positions):
        """Formater les positions planétaires pour l'affichage."""
        formatted = []
        
        for planet_id, position in positions.items():
            sign_id = position['sign']
            
            formatted.append({
                'planet': self.planets[planet_id]['name'],
                'sign': self.zodiac_signs[sign_id]['name'],
                'degrees': position['degrees'],
                'retrograde': position.get('retrograde', False),
                'description': f"{self.planets[planet_id]['name']} en {self.zodiac_signs[sign_id]['name']} à {position['degrees']:.1f}°" + 
                              (" rétrograde" if position.get('retrograde', False) else "")
            })
        
        return formatted
    
    def _retrograde_effect(self, planet_id):
        """Décrire l'effet d'une planète rétrograde dans le contexte sportif."""
        effects = {
            'mercury': "Communication et coordination tactique compromises, risque de malentendus",
            'venus': "Harmonie d'équipe réduite, relations tendues, difficulté à maintenir la cohésion",
            'mars': "Énergie dispersée, initiatives freinées, actions impulsives contre-productives"
        }
        
        return effects.get(planet_id, "Influence ralentie, remise en question et intériorisation")
    
    def _analyze_transits(self, current_positions, natal_positions):
        """Analyser les transits entre les positions actuelles et natales."""
        transits = []
        
        # Pour chaque planète actuelle
        for current_planet, current_position in current_positions.items():
            # Comparer avec chaque position natale
            for natal_planet, natal_position in natal_positions.items():
                # Calculer la différence angulaire
                current_angle = current_position['absolute_degrees']
                natal_angle = natal_position['absolute_degrees']
                
                angle_diff = abs(current_angle - natal_angle)
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff
                
                # Vérifier si cette différence correspond à un aspect
                for aspect_id, aspect_data in self.aspects.items():
                    aspect_angle = aspect_data['angle']
                    orb = aspect_data['orb']
                    
                    if abs(angle_diff - aspect_angle) <= orb:
                        # Calculer la précision de l'aspect
                        precision = 1 - (abs(angle_diff - aspect_angle) / orb)
                        
                        # Déterminer si l'aspect est harmonieux
                        is_harmonious = aspect_id in ['trine', 'sextile'] or (aspect_id == 'conjunction' and 
                                                                            current_planet != 'saturn' and natal_planet != 'saturn')
                        
                        # Calculer le score d'influence
                        influence_score = precision * aspect_data['influence']
                        
                        # Ajuster selon la rétrogradation
                        if current_position.get('retrograde', False):
                            influence_score *= 0.8
                        
                        # Créer la description du transit
                        current_planet_name = self.planets[current_planet]['name']
                        natal_planet_name = self.planets[natal_planet]['name']
                        aspect_name = aspect_data['name']
                        
                        description = f"{current_planet_name} actuel en {aspect_name} avec {natal_planet_name} natal"
                        
                        # Ajouter à la liste des transits
                        transits.append({
                            'transiting_planet': current_planet_name,
                            'natal_planet': natal_planet_name,
                            'aspect': aspect_name,
                            'precision': precision,
                            'harmonious': is_harmonious,
                            'nature': aspect_data['nature'],
                            'influence_score': influence_score,
                            'description': description,
                            'effect': aspect_data['sport_effect']['positive'] if is_harmonious else aspect_data['sport_effect']['negative']
                        })
        
        # Trier par influence
        transits.sort(key=lambda x: x['influence_score'], reverse=True)
        
        return transits
    
    def _analyze_team_compatibility(self, team1_natal, team2_natal):
        """Analyser la compatibilité astrologique entre deux équipes."""
        compatibility = {
            'overall_score': 0.5,  # Score par défaut
            'synastry_aspects': [],
            'compatible_elements': 0,
            'challenging_elements': 0
        }
        
        # Analyser les aspects entre les planètes des deux équipes
        synastry_aspects = []
        
        for planet1, position1 in team1_natal.items():
            for planet2, position2 in team2_natal.items():
                # Calculer la différence angulaire
                angle1 = position1['absolute_degrees']
                angle2 = position2['absolute_degrees']
                
                angle_diff = abs(angle1 - angle2)
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff
                
                # Vérifier si cette différence correspond à un aspect
                for aspect_id, aspect_data in self.aspects.items():
                    aspect_angle = aspect_data['angle']
                    orb = aspect_data['orb']
                    
                    if abs(angle_diff - aspect_angle) <= orb:
                        # Calculer la précision de l'aspect
                        precision = 1 - (abs(angle_diff - aspect_angle) / orb)
                        
                        # Déterminer si l'aspect est harmonieux
                        is_harmonious = aspect_id in ['trine', 'sextile'] or (aspect_id == 'conjunction' and 
                                                                            planet1 != 'saturn' and planet2 != 'saturn')
                        
                        # Calculer le score d'influence
                        influence_score = precision * aspect_data['influence']
                        
                        # Créer la description de l'aspect
                        planet1_name = self.planets[planet1]['name']
                        planet2_name = self.planets[planet2]['name']
                        aspect_name = aspect_data['name']
                        
                        # Ajouter à la liste des aspects
                        synastry_aspects.append({
                            'team1_planet': planet1_name,
                            'team2_planet': planet2_name,
                            'aspect': aspect_name,
                            'harmonious': is_harmonious,
                            'influence_score': influence_score,
                            'description': f"{planet1_name} (équipe 1) en {aspect_name} avec {planet2_name} (équipe 2)"
                        })
                        
                        # Comptabiliser les éléments compatibles et challengeants
                        if is_harmonious:
                            compatibility['compatible_elements'] += 1
                        else:
                            compatibility['challenging_elements'] += 1
        
        # Trier par influence
        synastry_aspects.sort(key=lambda x: x['influence_score'], reverse=True)
        compatibility['synastry_aspects'] = synastry_aspects[:5]  # Top 5 aspects
        
        # Calculer le score global de compatibilité
        total_aspects = compatibility['compatible_elements'] + compatibility['challenging_elements']
        if total_aspects > 0:
            compatibility_ratio = compatibility['compatible_elements'] / total_aspects
            compatibility['overall_score'] = 0.3 + (compatibility_ratio * 0.5)  # Plage de 0.3 à 0.8
        
        # Déterminer le niveau de compatibilité
        if compatibility['overall_score'] > 0.7:
            compatibility['level'] = 'high'
            compatibility['description'] = "Forte compatibilité astrologique, dynamique fluide"
        elif compatibility['overall_score'] > 0.5:
            compatibility['level'] = 'medium'
            compatibility['description'] = "Compatibilité modérée, mélange d'harmonies et de défis"
        else:
            compatibility['level'] = 'low'
            compatibility['description'] = "Compatibilité difficile, dynamique potentiellement conflictuelle"
        
        return compatibility
    
    def _determine_favored_team(self, team1_transits, team2_transits, team_compatibility):
        """Déterminer quelle équipe est plus favorisée astrologiquement."""
        # Calculer le score de favorabilité pour chaque équipe
        team1_favorable = 0
        team2_favorable = 0
        
        # Compter les transits harmonieux et leur influence
        for transit in team1_transits:
            if transit['harmonious']:
                team1_favorable += transit['influence_score']
            else:
                team1_favorable -= transit['influence_score'] * 0.5  # Impact négatif moindre
        
        for transit in team2_transits:
            if transit['harmonious']:
                team2_favorable += transit['influence_score']
            else:
                team2_favorable -= transit['influence_score'] * 0.5  # Impact négatif moindre
        
        # Normaliser les scores
        team1_score = max(0, min(1, team1_favorable / 5))
        team2_score = max(0, min(1, team2_favorable / 5))
        
        # Calculer l'avantage
        advantage = abs(team1_score - team2_score)
        favored = 'team1' if team1_score > team2_score else 'team2'
        
        # Déterminer le niveau d'avantage
        if advantage < 0.1:
            level = 'negligible'
            description = "Avantage astrologique négligeable, équilibre des influences"
        elif advantage < 0.25:
            level = 'slight'
            description = f"Léger avantage astrologique pour l'équipe {favored[-1]}"
        elif advantage < 0.4:
            level = 'moderate'
            description = f"Avantage astrologique modéré pour l'équipe {favored[-1]}"
        else:
            level = 'significant'
            description = f"Avantage astrologique significatif pour l'équipe {favored[-1]}"
        
        return {
            'favored_team': favored,
            'advantage_level': level,
            'description': description,
            'team1_score': team1_score,
            'team2_score': team2_score,
            'advantage_magnitude': advantage
        }
    
    def _identify_key_match_moments(self, match_planets, team1_natal, team2_natal):
        """Identifier les moments clés potentiels d'un match basés sur l'astrologie."""
        # Analyser les configurations planétaires pour identifier les moments potentiels
        key_moments = []
        
        # Vérifier les aspects tensionnels qui peuvent indiquer des moments critiques
        tension_aspects = ['opposition', 'square']
        
        # Vérifier les aspects entre les planètes du jour et les thémes natals
        for planet_id, position in match_planets.items():
            for aspect_id in tension_aspects:
                aspect_data = self.aspects[aspect_id]
                aspect_angle = aspect_data['angle']
                orb = aspect_data['orb']
                
                # Vérifier les aspects avec les positions natales des équipes
                for team_idx, natal_positions in enumerate([team1_natal, team2_natal]):
                    team_num = team_idx + 1
                    
                    for natal_planet, natal_position in natal_positions.items():
                        # Calculer la différence angulaire
                        current_angle = position['absolute_degrees']
                        natal_angle = natal_position['absolute_degrees']
                        
                        angle_diff = abs(current_angle - natal_angle)
                        if angle_diff > 180:
                            angle_diff = 360 - angle_diff
                        
                        # Vérifier si c'est un aspect de tension
                        if abs(angle_diff - aspect_angle) <= orb:
                            # Plus l'aspect est précis, plus le moment est significatif
                            precision = 1 - (abs(angle_diff - aspect_angle) / orb)
                            
                            # Certaines planètes indiquent des phases de match spécifiques
                            match_phase = self._determine_match_phase_from_planet(planet_id, natal_planet)
                            
                            # Description de l'influence
                            planet_name = self.planets[planet_id]['name']
                            natal_planet_name = self.planets[natal_planet]['name']
                            aspect_name = aspect_data['name']
                            
                            description = f"{aspect_name} entre {planet_name} du jour et {natal_planet_name} natal de l'équipe {team_num}"
                            
                            key_moments.append({
                                'phase': match_phase,
                                'significance': precision * aspect_data['influence'],
                                'description': description,
                                'affected_team': f"team{team_num}",
                                'nature': aspect_data['nature']
                            })
        
        # Ajouter des moments basés sur les phases lunaires
        moon_phase = self._calculate_moon_phase(datetime.date.today())
        if moon_phase['phase'] in ["Pleine Lune", "Nouvelle Lune"]:
            key_moments.append({
                'phase': 'whole_match',
                'significance': 0.8,
                'description': f"Influence de la {moon_phase['phase']} sur l'intensité émotionnelle du match",
                'affected_team': 'both',
                'nature': 'amplification'
            })
        
        # Trier par significance
        key_moments.sort(key=lambda x: x['significance'], reverse=True)
        
        # Limiter aux moments les plus significatifs
        return key_moments[:5]
    
    def _determine_match_phase_from_planet(self, transit_planet, natal_planet):
        """Déterminer la phase probable du match basée sur les planètes impliquées."""
        # Certaines planètes sont associées à des phases spécifiques du match
        if transit_planet == 'sun' or natal_planet == 'sun':
            return 'mid_match'  # Milieu de match, moment de pleine expression
        elif transit_planet == 'moon' or natal_planet == 'moon':
            return 'variable'   # Peut survenir à tout moment, lié aux émotions
        elif transit_planet == 'mars' or natal_planet == 'mars':
            return 'critical_moments'  # Moments d'action décisive, buts potentiels
        elif transit_planet == 'jupiter' or natal_planet == 'jupiter':
            return 'opportunity_phase'  # Phases d'expansion et d'opportunité
        elif transit_planet == 'saturn' or natal_planet == 'saturn':
            return 'challenging_phase'  # Phases de défi et de restriction
        else:
            return 'throughout'  # Influence tout au long du match
    
    def _calculate_date_favorability(self, day_positions, natal_positions):
        """Calculer un score de favorabilité pour une date basée sur les transits."""
        favorable_score = 0.5  # Valeur par défaut (neutre)
        
        # Analyser les transits
        transits = self._analyze_transits(day_positions, natal_positions)
        
        # Évaluer chaque transit selon sa nature et son influence
        for transit in transits:
            influence = transit['influence_score']
            
            if transit['harmonious']:
                favorable_score += influence * 0.1  # Bonus pour les aspects harmonieux
            else:
                favorable_score -= influence * 0.05  # Malus moindre pour les aspects tendus
        
        # Vérifier les planètes rétrogrades
        retrograde_planets = [planet for planet, data in day_positions.items() if data.get('retrograde', False)]
        if 'mars' in retrograde_planets:
            favorable_score -= 0.1  # Malus significatif pour Mars rétrograde
        if 'mercury' in retrograde_planets:
            favorable_score -= 0.05  # Malus modéré pour Mercure rétrograde
        
        # Prendre en compte la phase lunaire
        moon_position = day_positions['moon']['absolute_degrees']
        moon_phase_position = (moon_position % 30) / 30 * 360  # Normaliser sur 360 degrés
        
        # Pleine lune (autour de 180°) est favorable, nouvelle lune (autour de 0/360°) moins favorable
        if 150 <= moon_phase_position <= 210:  # Proche de la pleine lune
            favorable_score += 0.1
        elif (0 <= moon_phase_position <= 30) or (330 <= moon_phase_position <= 360):  # Proche de la nouvelle lune
            favorable_score -= 0.05
        
        # Limiter le score entre 0.1 et 0.9
        return max(0.1, min(0.9, favorable_score))
    
    def _generate_player_sport_profile(self, natal_positions, natal_aspects, sun_sign):
        """Générer un profil sportif basé sur le thème natal."""
        # Profil de base selon le signe solaire
        sign_traits = self.zodiac_signs[sun_sign]['sport_traits']
        
        # Initialiser les caractéristiques sportives
        sport_profile = {
            'playing_style': sign_traits['style'],
            'natural_strengths': [],
            'challenges': [],
            'ideal_position': '',
            'teamwork_aptitude': 0.5,  # Par défaut
            'leadership_potential': 0.5,  # Par défaut
            'resilience': 0.5,  # Par défaut
            'adaptability': 0.5  # Par défaut
        }
        
        # Ajouter les forces et faiblesses du signe
        sport_profile['natural_strengths'].extend(sign_traits['strengths'][:3])
        sport_profile['challenges'].extend(sign_traits['weaknesses'][:2])
        
        # Analyser l'influence des planètes selon leurs positions
        for planet, position in natal_positions.items():
            sign = position['sign']
            sign_data = self.zodiac_signs[sign]
            
            # Chaque planète influence différents aspects du profil sportif
            if planet == 'sun':  # Expression de soi, vitalité
                if sign_data['element'] == 'Feu':
                    sport_profile['leadership_potential'] += 0.2
                    if sign == 'leo':
                        sport_profile['natural_strengths'].append('présence imposante')
                        sport_profile['ideal_position'] = 'attaquant central ou meneur de jeu'
                elif sign_data['element'] == 'Terre':
                    sport_profile['resilience'] += 0.15
                    if sign == 'taurus':
                        sport_profile['natural_strengths'].append('force physique')
                        sport_profile['ideal_position'] = 'milieu défensif ou défenseur central'
                elif sign_data['element'] == 'Air':
                    sport_profile['adaptability'] += 0.15
                    if sign == 'libra':
                        sport_profile['natural_strengths'].append('sens de l\'équilibre')
                        sport_profile['ideal_position'] = 'milieu de terrain ou ailier'
                elif sign_data['element'] == 'Eau':
                    sport_profile['teamwork_aptitude'] += 0.15
                    if sign == 'scorpio':
                        sport_profile['natural_strengths'].append('intensité psychologique')
                        sport_profile['ideal_position'] = 'meneur de jeu ou finisseur'
            
            elif planet == 'moon':  # Émotions, intuition
                if sign_data['element'] == 'Feu':
                    sport_profile['adaptability'] += 0.1
                elif sign_data['element'] == 'Terre':
                    sport_profile['resilience'] += 0.2
                elif sign_data['element'] == 'Air':
                    sport_profile['teamwork_aptitude'] += 0.1
                elif sign_data['element'] == 'Eau':
                    sport_profile['natural_strengths'].append('intuition tactique')
            
            elif planet == 'mars':  # Énergie, combativité
                if sign_data['element'] == 'Feu':
                    sport_profile['natural_strengths'].append('agressivité offensive')
                    sport_profile['ideal_position'] = 'attaquant ou ailier offensif'
                elif sign_data['element'] == 'Terre':
                    sport_profile['natural_strengths'].append('endurance physique')
                    sport_profile['ideal_position'] = 'milieu box-to-box ou défenseur'
                elif sign_data['element'] == 'Air':
                    sport_profile['natural_strengths'].append('mobilité tactique')
                    sport_profile['ideal_position'] = 'milieu créatif ou ailier'
                elif sign_data['element'] == 'Eau':
                    sport_profile['natural_strengths'].append('intensité émotionnelle')
                    sport_profile['ideal_position'] = 'finisseur ou joueur de coups de pied arrêtés'
            
            elif planet == 'jupiter':  # Expansion, chance
                if sign_data['element'] == 'Feu':
                    sport_profile['leadership_potential'] += 0.15
                elif sign_data['element'] == 'Terre':
                    sport_profile['resilience'] += 0.1
                elif sign_data['element'] == 'Air':
                    sport_profile['adaptability'] += 0.2
                elif sign_data['element'] == 'Eau':
                    sport_profile['teamwork_aptitude'] += 0.2
            
            elif planet == 'saturn':  # Discipline, limites
                if sign_data['element'] == 'Feu':
                    sport_profile['challenges'].append('impulsivité contrôlée')
                elif sign_data['element'] == 'Terre':
                    sport_profile['natural_strengths'].append('discipline tactique')
                    sport_profile['ideal_position'] = 'défenseur central ou milieu défensif'
                elif sign_data['element'] == 'Air':
                    sport_profile['challenges'].append('communication sous pression')
                elif sign_data['element'] == 'Eau':
                    sport_profile['challenges'].append('gestion émotionnelle')
        
        # Tenir compte des aspects significatifs
        for aspect in natal_aspects:
            if 'Soleil' in aspect['planets'] and 'Mars' in aspect['planets']:
                if aspect['harmonious']:
                    sport_profile['natural_strengths'].append('coordination vitalité-action')
                    sport_profile['leadership_potential'] += 0.1
                else:
                    sport_profile['challenges'].append('conflit entre volonté et action')
            
            if 'Jupiter' in aspect['planets']:
                if aspect['harmonious']:
                    sport_profile['natural_strengths'].append('optimisme productif')
                    sport_profile['adaptability'] += 0.1
        
        # Limiter les valeurs entre 0.1 et 0.9
        sport_profile['teamwork_aptitude'] = max(0.1, min(0.9, sport_profile['teamwork_aptitude']))
        sport_profile['leadership_potential'] = max(0.1, min(0.9, sport_profile['leadership_potential']))
        sport_profile['resilience'] = max(0.1, min(0.9, sport_profile['resilience']))
        sport_profile['adaptability'] = max(0.1, min(0.9, sport_profile['adaptability']))
        
        # Éliminer les doublons dans les forces et faiblesses
        sport_profile['natural_strengths'] = list(dict.fromkeys(sport_profile['natural_strengths']))
        sport_profile['challenges'] = list(dict.fromkeys(sport_profile['challenges']))
        
        # Si pas de poste idéal défini, en suggérer un basé sur le profil global
        if not sport_profile['ideal_position']:
            if sport_profile['leadership_potential'] > 0.7:
                sport_profile['ideal_position'] = 'capitaine, meneur de jeu ou défenseur central'
            elif sport_profile['teamwork_aptitude'] > 0.7:
                sport_profile['ideal_position'] = 'milieu de terrain ou joueur de soutien'
            elif sport_profile['adaptability'] > 0.7:
                sport_profile['ideal_position'] = 'joueur polyvalent ou milieu de terrain'
            else:
                sport_profile['ideal_position'] = 'position selon les besoins tactiques'
        
        return sport_profile
    
    def _determine_player_phase(self, transit_aspects, current_positions):
        """Déterminer la phase actuelle du joueur basée sur les transits."""
        # Évaluer l'influence globale des transits
        challenging_score = 0
        favorable_score = 0
        
        for aspect in transit_aspects:
            if aspect['harmonious']:
                favorable_score += aspect['influence_score']
            else:
                challenging_score += aspect['influence_score']
        
        # Normaliser les scores
        max_score = max(favorable_score, challenging_score)
        if max_score > 0:
            favorable_score /= max_score
            challenging_score /= max_score
        
        # Vérifier les planètes rétrogrades
        retrograde_planets = [planet for planet, data in current_positions.items() if data.get('retrograde', False)]
        
        # Déterminer la phase dominante
        if favorable_score > challenging_score * 1.5:
            phase = "phase d'expansion"
            description = "Période favorable pour l'expression des talents et le développement"
        elif challenging_score > favorable_score * 1.5:
            phase = "phase de consolidation"
            description = "Période d'apprentissage à travers les défis, nécessité d'adaptation"
        elif favorable_score > 0.6 and challenging_score > 0.6:
            phase = "phase de transformation"
            description = "Période de changement intense mêlant opportunités et défis"
        elif 'mars' in retrograde_planets:
            phase = "phase de réorientation énergétique"
            description = "Période de recalibrage des actions et de l'approche du jeu"
        elif 'mercury' in retrograde_planets:
            phase = "phase de reconsidération tactique"
            description = "Période propice à réviser les approches tactiques et la communication"
        else:
            phase = "phase d'équilibre"
            description = "Période relativement neutre, stabilité dans la performance"
        
        # Ajouter des détails sur la durée probable
        duration = "quelques semaines"
        for planet, data in current_positions.items():
            if data.get('retrograde', False):
                if planet == 'mars':
                    duration = "environ deux mois"
                elif planet == 'mercury':
                    duration = "environ trois semaines"
        
        return {
            'phase': phase,
            'description': description,
            'favorable_level': favorable_score,
            'challenging_level': challenging_score,
            'estimated_duration': duration
        }
    
    def _predict_player_performance(self, transit_aspects, current_positions, sport_profile):
        """Prédire les performances futures du joueur basées sur les transits."""
        # Initialiser les prédictions
        prediction = {
            'overall_level': 0.5,  # Niveau global par défaut
            'peak_areas': [],      # Domaines où le joueur excelle
            'challenge_areas': [], # Domaines à surveiller
            'optimal_approach': '' # Approche recommandée
        }
        
        # Analyser les transits pour identifier les tendances
        favorable_transits = [a for a in transit_aspects if a['harmonious'] and a['influence_score'] > 0.6]
        challenging_transits = [a for a in transit_aspects if not a['harmonious'] and a['influence_score'] > 0.6]
        
        # Déterminer le niveau global
        if len(favorable_transits) > len(challenging_transits) * 2:
            prediction['overall_level'] = 0.8
            prediction['performance_outlook'] = "Potentiel de performance exceptionnelle"
        elif len(favorable_transits) > len(challenging_transits):
            prediction['overall_level'] = 0.7
            prediction['performance_outlook'] = "Bonne performance attendue"
        elif len(challenging_transits) > len(favorable_transits) * 2:
            prediction['overall_level'] = 0.3
            prediction['performance_outlook'] = "Période difficile nécessitant adaptation"
        elif len(challenging_transits) > len(favorable_transits):
            prediction['overall_level'] = 0.4
            prediction['performance_outlook'] = "Performance sous pression, défis à surmonter"
        else:
            prediction['overall_level'] = 0.5
            prediction['performance_outlook'] = "Performance standard, résultats mixtes"
        
        # Identifier les domaines d'excellence potentiels
        for aspect in favorable_transits:
            if 'Mars' in aspect['planets']:
                prediction['peak_areas'].append("Énergie physique et combativité")
            if 'Jupiter' in aspect['planets']:
                prediction['peak_areas'].append("Confiance et capacité à saisir les opportunités")
            if 'Soleil' in aspect['planets']:
                prediction['peak_areas'].append("Expression des talents et leadership")
            if 'Lune' in aspect['planets']:
                prediction['peak_areas'].append("Intuition et fluidité de jeu")
        
        # Identifier les défis potentiels
        for aspect in challenging_transits:
            if 'Mars' in aspect['planets']:
                prediction['challenge_areas'].append("Gestion de l'énergie et des confrontations")
            if 'Saturne' in aspect['planets']:
                prediction['challenge_areas'].append("Discipline et structure du jeu")
            if 'Mercure' in aspect['planets']:
                prediction['challenge_areas'].append("Communication et adaptabilité tactique")
        
        # Suggérer une approche optimale
        if prediction['overall_level'] > 0.7:
            if 'leadership_potential' in sport_profile and sport_profile['leadership_potential'] > 0.7:
                prediction['optimal_approach'] = "Prendre des initiatives et mener l'équipe par l'exemple"
            else:
                prediction['optimal_approach'] = "Capitaliser sur les forces actuelles et saisir les opportunités"
        elif prediction['overall_level'] < 0.4:
            if 'resilience' in sport_profile and sport_profile['resilience'] > 0.7:
                prediction['optimal_approach'] = "S'appuyer sur la résilience et maintenir la discipline de base"
            else:
                prediction['optimal_approach'] = "Se concentrer sur les fondamentaux et éviter les risques excessifs"
        else:
            if 'adaptability' in sport_profile and sport_profile['adaptability'] > 0.7:
                prediction['optimal_approach'] = "Adapter le jeu selon le flux du match et rester flexible"
            else:
                prediction['optimal_approach'] = "Maintenir l'équilibre entre initiative et prudence"
        
        # Éliminer les doublons
        prediction['peak_areas'] = list(dict.fromkeys(prediction['peak_areas']))
        prediction['challenge_areas'] = list(dict.fromkeys(prediction['challenge_areas']))
        
        return prediction
    
    def _identify_player_favorable_periods(self, natal_positions, current_date):
        """Identifier les périodes favorables à venir pour le joueur."""
        favorable_periods = []
        
        # Simuler les positions planétaires pour les 3 prochains mois
        end_date = current_date + datetime.timedelta(days=90)
        current = current_date
        
        # Échantillonner tous les 7 jours
        while current <= end_date:
            # Calculer les positions planétaires
            positions = self.calculate_planet_positions(current)
            
            # Analyser les transits
            transits = self._analyze_transits(positions, natal_positions)
            
            # Évaluer la favorabilité globale
            favorable_score = sum(t['influence_score'] for t in transits if t['harmonious'])
            challenging_score = sum(t['influence_score'] for t in transits if not t['harmonious'])
            
            net_score = favorable_score - challenging_score
            
            # Si la période est particulièrement favorable
            if net_score > 1.5:
                # Déterminer les planètes impliquées dans les transits favorables
                key_planets = set()
                for transit in transits:
                    if transit['harmonious'] and transit['influence_score'] > 0.7:
                        key_planets.add(transit['transiting_planet'])
                
                # Déterminer le type d'opportunité
                opportunity_type = "performance générale renforcée"
                if 'Mars' in key_planets:
                    opportunity_type = "énergie physique et compétitivité accrues"
                elif 'Jupiter' in key_planets:
                    opportunity_type = "opportunités d'expansion et de reconnaissance"
                elif 'Soleil' in key_planets:
                    opportunity_type = "expression des talents et confiance"
                
                # Estimer la durée de la période favorable
                duration_days = 7  # Estimation par défaut
                if 'Jupiter' in key_planets:
                    duration_days = 14  # Jupiter crée des influences plus durables
                
                # Ajouter cette période
                favorable_periods.append({
                    'start_date': current.strftime('%Y-%m-%d'),
                    'end_date': (current + datetime.timedelta(days=duration_days)).strftime('%Y-%m-%d'),
                    'favorability_score': net_score,
                    'opportunity_type': opportunity_type,
                    'key_influences': list(key_planets)
                })
            
            # Avancer de 7 jours
            current += datetime.timedelta(days=7)
        
        # Trier par score de favorabilité
        favorable_periods.sort(key=lambda x: x['favorability_score'], reverse=True)
        
        # Retourner les 3 meilleures périodes
        return favorable_periods[:3]