"""
TarotEcho - Module d'analyse symbolique utilisant les arcanes du Tarot.
Interprète les archétypes du tarot appliqués aux événements sportifs pour déceler des énergies invisibles.
"""

import random
import datetime
import math
from collections import defaultdict

class TarotEcho:
    """
    TarotEcho - Utilise des tirages symboliques pour déterminer des énergies invisibles sur le match.
    Applique les arcanes du Tarot de Marseille pour révéler des patterns énergétiques et influences subtiles.
    """
    
    def __init__(self):
        """Initialise le module TarotEcho"""
        # Définition des arcanes majeurs
        self.major_arcana = {
            0: {
                'name': 'Le Mat',
                'energy': 'Chaos, Potentiel, Imprévisibilité',
                'keywords': ['surprise', 'imprévisible', 'innovation', 'folie', 'risque'],
                'upright_meaning': 'Imprévisibilité totale, coups de génie, risques élevés',
                'reversed_meaning': 'Errance, mauvais choix, confusion, échec',
                'sport_influence': {
                    'upright': 'Match complètement imprévisible, potentiel de surprise majeure',
                    'reversed': 'Chaos dysfonctionnel, erreurs improbables, désordre collectif',
                    'teams': 'Favorise les équipes imprévisibles et les outsiders',
                    'player_type': 'Favorise les joueurs créatifs et imprévisibles',
                    'game_phase': 'Impact sur les moments inattendus et décisifs'
                }
            },
            1: {
                'name': 'Le Bateleur',
                'energy': 'Habileté, Initiative, Talent',
                'keywords': ['talent', 'adresse', 'initiative', 'commencement', 'créativité'],
                'upright_meaning': 'Habileté technique, vivacité, confiance, initiative',
                'reversed_meaning': 'Manque de concentration, inefficacité, mauvaise exécution',
                'sport_influence': {
                    'upright': 'Excellence technique, gestes décisifs, départ fort',
                    'reversed': 'Maladresse technique, incapacité à concrétiser',
                    'teams': 'Favorise les équipes techniques et bien préparées',
                    'player_type': 'Favorise les joueurs techniques et les créateurs',
                    'game_phase': 'Impact sur le début de match et les phases techniques'
                }
            },
            2: {
                'name': 'La Papesse',
                'energy': 'Intuition, Mystère, Connaissance',
                'keywords': ['intuition', 'sagesse', 'patience', 'secret', 'connaissance'],
                'upright_meaning': 'Intelligence tactique, intuition juste, patience stratégique',
                'reversed_meaning': 'Blocage tactique, manque de vision, impatience',
                'sport_influence': {
                    'upright': 'Coups tactiques parfaits, timing impeccable, lecture du jeu',
                    'reversed': 'Incompréhensions tactiques, décisions mal synchronisées',
                    'teams': 'Favorise les équipes tactiques et patientes',
                    'player_type': 'Favorise les stratèges et organisateurs',
                    'game_phase': 'Impact sur la construction et la lecture du jeu'
                }
            },
            3: {
                'name': 'L\'Impératrice',
                'energy': 'Créativité, Abondance, Puissance',
                'keywords': ['créativité', 'abondance', 'fécondité', 'action', 'expression'],
                'upright_meaning': 'Créativité offensive, production de jeu abondante, fluidité',
                'reversed_meaning': 'Stérilité offensive, improductivité, manque d\'idées',
                'sport_influence': {
                    'upright': 'Jeu offensif fluide, nombreuses occasions créées',
                    'reversed': 'Manque de création, stérilité offensive',
                    'teams': 'Favorise les équipes à vocation offensive',
                    'player_type': 'Favorise les créateurs et leaders offensifs',
                    'game_phase': 'Impact sur les phases offensives et la création'
                }
            },
            4: {
                'name': 'L\'Empereur',
                'energy': 'Autorité, Structure, Contrôle',
                'keywords': ['autorité', 'structure', 'contrôle', 'stabilité', 'discipline'],
                'upright_meaning': 'Domination, contrôle du jeu, autorité sur le terrain',
                'reversed_meaning': 'Perte d\'autorité, manque de structure, désorganisation',
                'sport_influence': {
                    'upright': 'Contrôle du match, leadership décisif, organisation tactique',
                    'reversed': 'Désorganisation, perte de structure, autorité contestée',
                    'teams': 'Favorise les équipes bien organisées avec un leader fort',
                    'player_type': 'Favorise les capitaines et organisateurs',
                    'game_phase': 'Impact sur le contrôle du match et l\'organisation'
                }
            },
            5: {
                'name': 'Le Pape',
                'energy': 'Sagesse, Tradition, Conformité',
                'keywords': ['sagesse', 'tradition', 'guidance', 'conformisme', 'enseignement'],
                'upright_meaning': 'Conseils tactiques suivis, respect du plan de jeu, cohésion',
                'reversed_meaning': 'Dogmatisme tactique, manque d\'adaptation, division',
                'sport_influence': {
                    'upright': 'Cohérence tactique, respect des consignes, unité d\'équipe',
                    'reversed': 'Tactique inadaptée, dissensions internes, manque d\'ajustements',
                    'teams': 'Favorise les équipes expérimentées et bien entraînées',
                    'player_type': 'Favorise les joueurs disciplinés et les mentors',
                    'game_phase': 'Impact sur la cohésion d\'équipe et le respect tactique'
                }
            },
            6: {
                'name': 'L\'Amoureux',
                'energy': 'Choix, Harmonie, Attraction',
                'keywords': ['choix', 'harmonie', 'relations', 'valeurs', 'désir'],
                'upright_meaning': 'Harmonie d\'équipe, choix tactiques judicieux, complicité',
                'reversed_meaning': 'Mauvais choix, indécision, conflit interne, dysharmonie',
                'sport_influence': {
                    'upright': 'Combinaisons parfaites, chimie d\'équipe, partenariat efficace',
                    'reversed': 'Mésentente entre joueurs, confusion des rôles, choix hésitants',
                    'teams': 'Favorise les équipes avec forte cohésion et complicité',
                    'player_type': 'Favorise les duos complémentaires et les joueurs altruistes',
                    'game_phase': 'Impact sur les choix décisifs et la cohésion offensive'
                }
            },
            7: {
                'name': 'Le Chariot',
                'energy': 'Victoire, Détermination, Direction',
                'keywords': ['détermination', 'victoire', 'mouvement', 'contrôle', 'succès'],
                'upright_meaning': 'Détermination vers la victoire, contrôle du match, avancée',
                'reversed_meaning': 'Défaite dans les moments clés, perte de contrôle, obstacles',
                'sport_influence': {
                    'upright': 'Avancée inexorable vers la victoire, volonté supérieure',
                    'reversed': 'Obstacles majeurs, difficultés à avancer, progression bloquée',
                    'teams': 'Favorise les équipes déterminées et en progression',
                    'player_type': 'Favorise les leaders et les vainqueurs naturels',
                    'game_phase': 'Impact sur la progression et les moments de conquête'
                }
            },
            8: {
                'name': 'La Justice',
                'energy': 'Équilibre, Vérité, Équité',
                'keywords': ['équilibre', 'justice', 'vérité', 'cause-effet', 'impartialité'],
                'upright_meaning': 'Équilibre du jeu, résultat juste, méritocratie',
                'reversed_meaning': 'Injustice, déséquilibre, résultat trompeur',
                'sport_influence': {
                    'upright': 'Victoire méritée, équité des décisions, équilibre du match',
                    'reversed': 'Décisions controversées, résultat injuste, déséquilibre flagrant',
                    'teams': 'Favorise l\'équipe qui mérite objectivement de gagner',
                    'player_type': 'Favorise les joueurs justes et équilibrés',
                    'game_phase': 'Impact sur les décisions d\'arbitrage et l\'équité globale'
                }
            },
            9: {
                'name': 'L\'Hermite',
                'energy': 'Introspection, Sagesse, Solitude',
                'keywords': ['introspection', 'recherche', 'guide', 'prudence', 'isolement'],
                'upright_meaning': 'Sagesse tactique, patience, observation efficace',
                'reversed_meaning': 'Isolation, prudence excessive, manque de communication',
                'sport_influence': {
                    'upright': 'Décisions réfléchies, timing parfait, guidage stratégique',
                    'reversed': 'Trop de prudence, manque de communication, isolement tactique',
                    'teams': 'Favorise les équipes réfléchies et les plans tactiques subtils',
                    'player_type': 'Favorise les mentors et joueurs d\'expérience isolés',
                    'game_phase': 'Impact sur les phases d\'observation et ajustements tactiques'
                }
            },
            10: {
                'name': 'La Roue de Fortune',
                'energy': 'Hasard, Cycles, Changement',
                'keywords': ['chance', 'cycle', 'changement', 'destin', 'opportunité'],
                'upright_meaning': 'Tournant du match, chance favorable, momentum positif',
                'reversed_meaning': 'Malchance, retournement négatif, momentum adverse',
                'sport_influence': {
                    'upright': 'Changement positif de dynamique, chance souriante, opportunités',
                    'reversed': 'Malchance persistante, retournements défavorables, occasions manquées',
                    'teams': 'Favorise les équipes au bon moment cyclique ou chanceux',
                    'player_type': 'Favorise les joueurs opportunistes et chanceux',
                    'game_phase': 'Impact sur les tournants du match et moments charnières'
                }
            },
            11: {
                'name': 'La Force',
                'energy': 'Courage, Puissance, Persévérance',
                'keywords': ['force', 'courage', 'persévérance', 'énergie', 'maîtrise'],
                'upright_meaning': 'Force mentale et physique, courage dans l\'adversité, domination',
                'reversed_meaning': 'Faiblesse, manque de courage, puissance mal canalisée',
                'sport_influence': {
                    'upright': 'Domination physique, résistance mentale, puissance contrôlée',
                    'reversed': 'Fatigue précoce, faiblesse mentale, puissance désordonnée',
                    'teams': 'Favorise les équipes physiques avec mental d\'acier',
                    'player_type': 'Favorise les joueurs puissants et mentalement forts',
                    'game_phase': 'Impact sur les duels physiques et moments d\'adversité'
                }
            },
            12: {
                'name': 'Le Pendu',
                'energy': 'Sacrifice, Attente, Perspective',
                'keywords': ['sacrifice', 'attente', 'perspective', 'suspension', 'lâcher-prise'],
                'upright_meaning': 'Sacrifice tactique, nouvelle perspective, patience payante',
                'reversed_meaning': 'Sacrifices vains, délais inutiles, perspective limitée',
                'sport_influence': {
                    'upright': 'Stratégie de sacrifice récompensée, patience productive',
                    'reversed': 'Attente improductive, sacrifices tactiques stériles',
                    'teams': 'Favorise les équipes patientes avec vision à long terme',
                    'player_type': 'Favorise les joueurs altruistes prêts au sacrifice',
                    'game_phase': 'Impact sur les phases d\'attente et de préparation'
                }
            },
            13: {
                'name': 'La Mort',
                'energy': 'Fin, Transformation, Transition',
                'keywords': ['fin', 'transformation', 'transition', 'lâcher-prise', 'renouveau'],
                'upright_meaning': 'Fin d\'une dynamique, transformation radicale, renouveau',
                'reversed_meaning': 'Stagnation, résistance au changement, transitions difficiles',
                'sport_influence': {
                    'upright': 'Changement radical de dynamique, fin d\'une domination, transition',
                    'reversed': 'Incapacité à changer de dynamique, résistance au changement nécessaire',
                    'teams': 'Favorise les équipes en transformation ou fin de cycle',
                    'player_type': 'Favorise les agents de changement, impact des remplaçants',
                    'game_phase': 'Impact sur les grandes transformations et moments décisifs'
                }
            },
            14: {
                'name': 'Tempérance',
                'energy': 'Équilibre, Modération, Harmonie',
                'keywords': ['équilibre', 'modération', 'patience', 'combinaison', 'harmonie'],
                'upright_meaning': 'Équilibre parfait, harmonie d\'équipe, combinaisons fluides',
                'reversed_meaning': 'Déséquilibre, excès, manque d\'harmonie, impatience',
                'sport_influence': {
                    'upright': 'Jeu équilibré, combinaisons harmonieuses, patience tactique',
                    'reversed': 'Déséquilibre tactique, excès offensifs ou défensifs',
                    'teams': 'Favorise les équipes équilibrées avec jeu harmonieux',
                    'player_type': 'Favorise les joueurs équilibrés et patients',
                    'game_phase': 'Impact sur l\'équilibre général et les phases de construction'
                }
            },
            15: {
                'name': 'Le Diable',
                'energy': 'Tentation, Obsession, Instinct',
                'keywords': ['tentation', 'dépendance', 'matérialisme', 'instinct', 'excès'],
                'upright_meaning': 'Instinct brut, obsession de gagner, forces primaires',
                'reversed_meaning': 'Auto-sabotage, obsessions négatives, pièges mentaux',
                'sport_influence': {
                    'upright': 'Jeu instinctif puissant, détermination féroce, intensité',
                    'reversed': 'Auto-sabotage, pièges tactiques, trop d\'individualisme',
                    'teams': 'Favorise les équipes instinctives et physiquement intenses',
                    'player_type': 'Favorise les joueurs instinctifs et dominateurs',
                    'game_phase': 'Impact sur les phases d\'intensité et lutte primaire'
                }
            },
            16: {
                'name': 'La Maison Dieu',
                'energy': 'Destruction, Révélation, Libération',
                'keywords': ['destruction', 'révélation', 'choc', 'changement', 'libération'],
                'upright_meaning': 'Bouleversement du match, révélation de faiblesses, destruction',
                'reversed_meaning': 'Désastre évité, peur du changement, résistance à l\'évidence',
                'sport_influence': {
                    'upright': 'Retournement complet de situation, effondrement soudain',
                    'reversed': 'Évitement d\'un désastre, peurs non fondées, crise évitée',
                    'teams': 'Favorise les équipes capables de causer ou survivre aux chocs',
                    'player_type': 'Favorise les révélateurs ou agents de destruction',
                    'game_phase': 'Impact sur les moments de crise et effondrements'
                }
            },
            17: {
                'name': 'L\'Étoile',
                'energy': 'Espoir, Inspiration, Sérénité',
                'keywords': ['espoir', 'inspiration', 'sérénité', 'guidance', 'renouveau'],
                'upright_meaning': 'Talent inspiré, espoir renouvelé, sérénité dans le jeu',
                'reversed_meaning': 'Espoirs déçus, inspiration perdue, démoralisation',
                'sport_influence': {
                    'upright': 'Performance inspirée, confiance sereine, fluidité naturelle',
                    'reversed': 'Déception des attentes, talent non exprimé, perte de confiance',
                    'teams': 'Favorise les équipes confiantes et sources d\'inspiration',
                    'player_type': 'Favorise les joueurs talentueux et inspirants',
                    'game_phase': 'Impact sur les moments d\'inspiration et de renouveau'
                }
            },
            18: {
                'name': 'La Lune',
                'energy': 'Illusion, Intuition, Incertitude',
                'keywords': ['illusion', 'intuition', 'incertitude', 'peur', 'instinct'],
                'upright_meaning': 'Intuition profonde, mystère tactique, confusion de l\'adversaire',
                'reversed_meaning': 'Illusions dissipées, peurs irrationnelles, confusion interne',
                'sport_influence': {
                    'upright': 'Jeu mystérieux et imprévisible, intuition puissante',
                    'reversed': 'Confusion interne, peurs non fondées, illusions dissipées',
                    'teams': 'Favorise les équipes mystérieuses ou très intuitives',
                    'player_type': 'Favorise les joueurs intuitifs et mystérieux',
                    'game_phase': 'Impact sur les phases d\'incertitude et décisions instinctives'
                }
            },
            19: {
                'name': 'Le Soleil',
                'energy': 'Succès, Joie, Vitalité',
                'keywords': ['succès', 'vitalité', 'joie', 'clarté', 'confiance'],
                'upright_meaning': 'Succès éclatant, vitalité maximale, confiance rayonnante',
                'reversed_meaning': 'Succès temporaire, vitalité diminuée, excès de confiance',
                'sport_influence': {
                    'upright': 'Performance éclatante, énergie débordante, succès manifeste',
                    'reversed': 'Énergie en baisse, confiance fragile, succès incomplet',
                    'teams': 'Favorise les équipes en pleine forme et confiantes',
                    'player_type': 'Favorise les joueurs énergiques et positifs',
                    'game_phase': 'Impact sur les moments de pleine expression et d\'éclat'
                }
            },
            20: {
                'name': 'Le Jugement',
                'energy': 'Jugement, Renouveau, Réveil',
                'keywords': ['jugement', 'renouveau', 'réveil', 'rédemption', 'vocation'],
                'upright_meaning': 'Moment de vérité, réveil collectif, rédemption',
                'reversed_meaning': 'Jugement erroné, réveil avorté, rédemption manquée',
                'sport_influence': {
                    'upright': 'Réveil d\'équipe, moment de vérité, rédemption collective',
                    'reversed': 'Incapacité à se révéler, opportunité manquée, faux réveil',
                    'teams': 'Favorise les équipes en quête de rédemption ou à un tournant',
                    'player_type': 'Favorise les joueurs rédempteurs ou catalyseurs',
                    'game_phase': 'Impact sur les moments de révélation et de vérité'
                }
            },
            21: {
                'name': 'Le Monde',
                'energy': 'Accomplissement, Complétude, Harmonie',
                'keywords': ['accomplissement', 'complétude', 'harmonie', 'perfection', 'succès'],
                'upright_meaning': 'Performance complète, accomplissement total, harmonie parfaite',
                'reversed_meaning': 'Inachèvement, manque d\'harmonie, victoire incomplète',
                'sport_influence': {
                    'upright': 'Performance parfaite et complète, expression totale du potentiel',
                    'reversed': 'Performance incomplète, succès partiel, manque de complétude',
                    'teams': 'Favorise les équipes complètes et accomplies',
                    'player_type': 'Favorise les joueurs accomplis et complets',
                    'game_phase': 'Impact sur l\'accomplissement final et réussite globale'
                }
            }
        }
        
        # Définition simplifiée des arcanes mineurs
        self.minor_arcana_suits = {
            'cups': {
                'element': 'Eau',
                'domain': 'Émotions, intuition, relations',
                'sport_aspect': 'Intelligence émotionnelle, esprit d\'équipe, fluidité'
            },
            'wands': {
                'element': 'Feu',
                'domain': 'Énergie, passion, action',
                'sport_aspect': 'Dynamisme, attaque, intensité'
            },
            'swords': {
                'element': 'Air',
                'domain': 'Intellect, conflit, clarté',
                'sport_aspect': 'Stratégie, précision, conflits'
            },
            'pentacles': {
                'element': 'Terre',
                'domain': 'Matière, stabilité, ressources',
                'sport_aspect': 'Endurance, défense, solidité'
            }
        }
        
        # Signification simplifiée des valeurs des arcanes mineurs
        self.minor_arcana_values = {
            'ace': 'Potentiel pur, commencement',
            '2': 'Équilibre, dualité, choix',
            '3': 'Croissance, expression, manifestation',
            '4': 'Stabilité, structure, fondation',
            '5': 'Conflit, adaptation, changement',
            '6': 'Harmonie, ajustement, transition',
            '7': 'Réflexion, évaluation, épreuve',
            '8': 'Mouvement, progrès, pouvoir',
            '9': 'Réalisation, préparation, accomplissement',
            '10': 'Complétude, conclusion, transition',
            'page': 'Apprentissage, message, curiosité',
            'knight': 'Action, mouvement, impulsivité',
            'queen': 'Maîtrise, réceptivité, nourrissement',
            'king': 'Autorité, contrôle, réalisation'
        }
        
        # Correspondances numériques des cartes
        self.card_numbers = {
            'ace': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'page': 11,
            'knight': 12,
            'queen': 13,
            'king': 14
        }
        
        # Historique des tirages
        self.reading_history = []
        
        # Poids d'influence des positions dans un tirage
        self.position_weights = {
            'center': 1.0,           # Position centrale
            'crossing': 0.9,         # Influence croisée/obstacle
            'above': 0.8,            # Influences supérieures, idéaux
            'below': 0.7,            # Fondations, inconscient
            'past': 0.6,             # Influences passées
            'future': 0.8,           # Influences futures
            'attitude': 0.7,         # Attitude du sujet
            'environment': 0.7,      # Influences externes
            'hopes_fears': 0.5,      # Espoirs et craintes
            'outcome': 0.9           # Résultat final
        }
        
        # Type de tirages disponibles
        self.spread_types = {
            'single': 'Tirage simple (1 carte)',
            'three': 'Tirage à trois cartes (passé, présent, futur)',
            'cross': 'Croix celtique (10 cartes, analyse complète)',
            'horseshoe': 'Fer à cheval (7 cartes, progression)',
            'teams': 'Tirage des équipes (2-4 cartes par équipe)',
            'match': 'Tirage de match (7 cartes pour l\'événement)'
        }
    
    def draw_cards(self, count=1, seed=None):
        """
        Tirer un nombre spécifique de cartes du tarot.
        
        Args:
            count (int): Nombre de cartes à tirer
            seed (any, optional): Graine pour la reproductibilité du tirage
            
        Returns:
            list: Cartes tirées avec leur orientation
        """
        # Créer la liste complète des cartes
        all_cards = []
        
        # Ajouter les arcanes majeurs
        for i in range(22):
            all_cards.append({'arcana': 'major', 'index': i, 'name': self.major_arcana[i]['name']})
        
        # Ajouter les arcanes mineurs si nécessaire
        suits = ['cups', 'wands', 'swords', 'pentacles']
        values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'page', 'knight', 'queen', 'king']
        
        for suit in suits:
            for value in values:
                all_cards.append({'arcana': 'minor', 'suit': suit, 'value': value, 'name': f"{value.capitalize()} of {suit.capitalize()}"})
        
        # Initialiser le générateur aléatoire avec une graine si fournie
        if seed is not None:
            random.seed(seed)
        
        # Mélanger les cartes
        shuffled_cards = all_cards.copy()
        random.shuffle(shuffled_cards)
        
        # Tirer les cartes avec orientation aléatoire
        drawn_cards = []
        for i in range(min(count, len(shuffled_cards))):
            card = shuffled_cards[i]
            # 20% de chance que la carte soit inversée
            card['reversed'] = random.random() < 0.2
            drawn_cards.append(card)
        
        return drawn_cards
    
    def do_simple_reading(self, query="", seed=None):
        """
        Effectuer un tirage simple d'une carte.
        
        Args:
            query (str): Question ou sujet du tirage
            seed (any, optional): Graine pour la reproductibilité du tirage
            
        Returns:
            dict: Interprétation de la carte
        """
        # Tirer une carte
        card = self.draw_cards(1, seed)[0]
        
        # Interpréter la carte
        interpretation = self._interpret_card(card)
        
        # Adapter l'interprétation au contexte sportif
        sport_meaning = self._apply_to_sports(interpretation)
        
        # Préparer le résultat
        result = {
            'query': query or "Tirage général pour obtenir un aperçu",
            'spread_type': 'single',
            'card': {
                'name': card['name'],
                'arcana': card['arcana'],
                'reversed': card['reversed']
            },
            'meaning': interpretation['meaning'],
            'keywords': interpretation['keywords'],
            'sport_application': sport_meaning,
            'advice': self._generate_advice(interpretation),
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # Ajouter à l'historique
        self.reading_history.append({
            'type': 'simple_reading',
            'query': query,
            'result': result
        })
        
        return result
    
    def do_three_card_reading(self, query="", time_based=True, seed=None):
        """
        Effectuer un tirage de trois cartes.
        
        Args:
            query (str): Question ou sujet du tirage
            time_based (bool): Si True, les positions représentent passé/présent/futur
            seed (any, optional): Graine pour la reproductibilité du tirage
            
        Returns:
            dict: Interprétation des trois cartes
        """
        # Tirer trois cartes
        cards = self.draw_cards(3, seed)
        
        # Définir les positions selon le type de tirage
        if time_based:
            positions = ['past', 'present', 'future']
            position_names = ['Passé', 'Présent', 'Futur']
        else:
            positions = ['situation', 'challenge', 'advice']
            position_names = ['Situation', 'Défi', 'Conseil']
        
        # Interpréter chaque carte
        interpretations = []
        overall_energy = []
        
        for i, card in enumerate(cards):
            interpretation = self._interpret_card(card)
            sport_meaning = self._apply_to_sports(interpretation)
            
            # Pondérer l'énergie de chaque carte selon sa position
            position_weight = 0.7 if i == 1 else 0.5  # Plus de poids au présent/situation
            overall_energy.append({
                'energy': interpretation['energy'],
                'weight': position_weight
            })
            
            interpretations.append({
                'position': positions[i],
                'position_name': position_names[i],
                'card': {
                    'name': card['name'],
                    'arcana': card['arcana'],
                    'reversed': card['reversed']
                },
                'meaning': interpretation['meaning'],
                'keywords': interpretation['keywords'],
                'sport_application': sport_meaning
            })
        
        # Calculer la synergie entre les cartes
        synergy = self._calculate_cards_synergy(cards)
        
        # Interpréter la lecture globale
        overall_interpretation = self._interpret_overall_reading(
            interpretations, 
            overall_energy,
            synergy
        )
        
        # Préparer le résultat
        result = {
            'query': query or "Tirage à trois cartes pour une vision élargie",
            'spread_type': 'three_card',
            'time_based': time_based,
            'card_interpretations': interpretations,
            'card_synergy': synergy,
            'overall_interpretation': overall_interpretation,
            'advice': self._generate_advice_from_spread(interpretations, overall_interpretation),
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # Ajouter à l'historique
        self.reading_history.append({
            'type': 'three_card_reading',
            'query': query,
            'result': result
        })
        
        return result
    
    def do_match_reading(self, match_data, team1_name, team2_name, seed=None):
        """
        Effectuer un tirage spécifique pour un match.
        
        Args:
            match_data (dict): Données du match
            team1_name (str): Nom de l'équipe 1
            team2_name (str): Nom de l'équipe 2
            seed (any, optional): Graine pour la reproductibilité du tirage
            
        Returns:
            dict: Interprétation du match via le tarot
        """
        # Tirer 7 cartes pour le schéma de match
        cards = self.draw_cards(7, seed)
        
        # Définir les positions des cartes
        positions = [
            'match_energy', 'team1_energy', 'team2_energy', 
            'first_half', 'second_half', 'key_moment', 'outcome'
        ]
        position_names = [
            'Énergie Globale du Match', f'Énergie de {team1_name}', f'Énergie de {team2_name}',
            'Première Mi-temps', 'Seconde Mi-temps', 'Moment Clé', 'Résultat'
        ]
        
        # Interpréter chaque carte
        interpretations = []
        
        for i, card in enumerate(cards):
            interpretation = self._interpret_card(card)
            sport_meaning = self._apply_to_sports(interpretation)
            
            # Adapter l'interprétation au contexte spécifique de la position
            position_context = self._adapt_to_position(
                interpretation, sport_meaning, positions[i], {'team1': team1_name, 'team2': team2_name}
            )
            
            interpretations.append({
                'position': positions[i],
                'position_name': position_names[i],
                'card': {
                    'name': card['name'],
                    'arcana': card['arcana'],
                    'reversed': card['reversed']
                },
                'meaning': interpretation['meaning'],
                'keywords': interpretation['keywords'],
                'sport_application': sport_meaning,
                'position_context': position_context
            })
        
        # Comparer les énergies des équipes
        team_comparison = self._compare_team_energies(
            interpretations[1], interpretations[2]
        )
        
        # Interprétation du déroulement du match
        match_flow = self._interpret_match_flow(
            interpretations[3], interpretations[4], interpretations[5]
        )
        
        # Déterminer les arcanes dominants
        dominant_arcana = self._identify_dominant_arcana(cards)
        
        # Calculer la prédiction du match
        match_prediction = self._calculate_match_prediction(
            interpretations, team_comparison, dominant_arcana
        )
        
        # Préparer le résultat
        result = {
            'query': f"Tirage pour le match {team1_name} vs {team2_name}",
            'spread_type': 'match_reading',
            'match_details': {
                'team1': team1_name,
                'team2': team2_name,
                'date': match_data.get('date', datetime.datetime.now().strftime('%Y-%m-%d'))
            },
            'card_interpretations': interpretations,
            'team_comparison': team_comparison,
            'match_flow': match_flow,
            'dominant_energies': dominant_arcana,
            'match_prediction': match_prediction,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # Ajouter à l'historique
        self.reading_history.append({
            'type': 'match_reading',
            'match': f"{team1_name} vs {team2_name}",
            'result': result
        })
        
        return result
    
    def do_team_analysis(self, team_name, team_data=None, detailed=False, seed=None):
        """
        Effectuer une analyse d'équipe basée sur le tarot.
        
        Args:
            team_name (str): Nom de l'équipe
            team_data (dict, optional): Données supplémentaires sur l'équipe
            detailed (bool): Si True, effectue une analyse plus détaillée
            seed (any, optional): Graine pour la reproductibilité du tirage
            
        Returns:
            dict: Analyse de l'équipe basée sur le tarot
        """
        # Déterminer le nombre de cartes selon le niveau de détail
        card_count = 5 if detailed else 3
        
        # Tirer les cartes
        cards = self.draw_cards(card_count, seed)
        
        # Définir les positions des cartes
        if detailed:
            positions = ['team_essence', 'current_state', 'strengths', 'challenges', 'potential']
            position_names = ['Essence de l\'Équipe', 'État Actuel', 'Forces', 'Défis', 'Potentiel']
        else:
            positions = ['team_essence', 'strengths', 'challenges']
            position_names = ['Essence de l\'Équipe', 'Forces', 'Défis']
        
        # Interpréter chaque carte
        interpretations = []
        
        for i, card in enumerate(cards):
            interpretation = self._interpret_card(card)
            sport_meaning = self._apply_to_sports(interpretation)
            
            interpretations.append({
                'position': positions[i],
                'position_name': position_names[i],
                'card': {
                    'name': card['name'],
                    'arcana': card['arcana'],
                    'reversed': card['reversed']
                },
                'meaning': interpretation['meaning'],
                'keywords': interpretation['keywords'],
                'sport_application': sport_meaning
            })
        
        # Déterminer les archétypes dominants
        team_archetypes = self._identify_team_archetypes(cards, interpretations)
        
        # Identifier les énergies élémentaires
        elemental_energies = self._analyze_elemental_energies(cards)
        
        # Générer un profil d'équipe
        team_profile = self._generate_team_profile(interpretations, team_archetypes, elemental_energies)
        
        # Préparer le résultat
        result = {
            'team_name': team_name,
            'spread_type': 'team_analysis',
            'detailed': detailed,
            'card_interpretations': interpretations,
            'team_archetypes': team_archetypes,
            'elemental_energies': elemental_energies,
            'team_profile': team_profile,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # Ajouter à l'historique
        self.reading_history.append({
            'type': 'team_analysis',
            'team': team_name,
            'result': result
        })
        
        return result
    
    def analyze_match_momentum(self, match_data, current_minute, team1_score, team2_score, seed=None):
        """
        Analyser le momentum actuel d'un match en cours.
        
        Args:
            match_data (dict): Données du match
            current_minute (int): Minute actuelle du match
            team1_score (int): Score de l'équipe 1
            team2_score (int): Score de l'équipe 2
            seed (any, optional): Graine pour la reproductibilité du tirage
            
        Returns:
            dict: Analyse du momentum actuel du match
        """
        # Créer une graine basée sur les données du match si non fournie
        if seed is None:
            seed_str = f"{match_data.get('date', '')}-{current_minute}-{team1_score}-{team2_score}"
            seed = hash(seed_str)
        
        # Tirer 3 cartes pour l'analyse du momentum
        cards = self.draw_cards(3, seed)
        
        # Définir les positions des cartes
        positions = ['current_momentum', 'hidden_forces', 'emerging_trend']
        position_names = ['Momentum Actuel', 'Forces Invisibles', 'Tendance Émergente']
        
        # Interpréter chaque carte
        interpretations = []
        
        for i, card in enumerate(cards):
            interpretation = self._interpret_card(card)
            sport_meaning = self._apply_to_sports(interpretation)
            
            interpretations.append({
                'position': positions[i],
                'position_name': position_names[i],
                'card': {
                    'name': card['name'],
                    'arcana': card['arcana'],
                    'reversed': card['reversed']
                },
                'meaning': interpretation['meaning'],
                'keywords': interpretation['keywords'],
                'sport_application': sport_meaning
            })
        
        # Analyser le momentum
        momentum_analysis = self._analyze_momentum(
            interpretations, current_minute, team1_score, team2_score
        )
        
        # Déterminer les énergies dominantes
        dominant_energies = self._identify_dominant_energies(cards)
        
        # Identifier les points de pivotement potentiels
        pivot_points = self._identify_momentum_pivot_points(
            interpretations, current_minute
        )
        
        # Préparer le résultat
        result = {
            'match_state': {
                'minute': current_minute,
                'team1_score': team1_score,
                'team2_score': team2_score,
                'team1_name': match_data.get('team1', 'Équipe 1'),
                'team2_name': match_data.get('team2', 'Équipe 2')
            },
            'spread_type': 'momentum_analysis',
            'card_interpretations': interpretations,
            'momentum_analysis': momentum_analysis,
            'dominant_energies': dominant_energies,
            'pivot_points': pivot_points,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # Ajouter à l'historique
        self.reading_history.append({
            'type': 'momentum_analysis',
            'match': f"{match_data.get('team1', 'Équipe 1')} vs {match_data.get('team2', 'Équipe 2')}",
            'minute': current_minute,
            'result': result
        })
        
        return result
    
    def suggest_optimal_timing(self, team_name, event_type, start_date, end_date, seed=None):
        """
        Suggérer un timing optimal pour un événement sportif.
        
        Args:
            team_name (str): Nom de l'équipe
            event_type (str): Type d'événement (match, transfert, etc.)
            start_date (str): Date de début de la période (format YYYY-MM-DD)
            end_date (str): Date de fin de la période (format YYYY-MM-DD)
            seed (any, optional): Graine pour la reproductibilité du tirage
            
        Returns:
            dict: Suggestion de timing optimal
        """
        # Convertir les dates en objets datetime
        try:
            start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return {'error': 'Format de date invalide. Utilisez YYYY-MM-DD'}
        
        # Vérifier que la période est valide
        if start > end:
            return {'error': 'La date de début doit être antérieure à la date de fin'}
        
        # Calculer le nombre de jours dans la période
        days_count = (end - start).days + 1
        if days_count > 90:  # Limiter à 90 jours pour éviter des calculs trop lourds
            return {'error': 'Période trop longue. Limitez l\'analyse à 90 jours maximum'}
        
        # Tirer une carte pour chaque semaine dans la période
        weekly_readings = []
        current_date = start
        
        while current_date <= end:
            # Générer une graine basée sur la date pour la reproductibilité
            date_seed = seed if seed is not None else hash(f"{team_name}-{current_date.strftime('%Y-%m-%d')}")
            
            # Tirer une carte pour cette date
            card = self.draw_cards(1, date_seed)[0]
            interpretation = self._interpret_card(card)
            
            # Évaluer l'opportunité pour l'événement
            event_opportunity = self._evaluate_event_opportunity(
                interpretation, event_type
            )
            
            weekly_readings.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'card': {
                    'name': card['name'],
                    'arcana': card['arcana'],
                    'reversed': card['reversed']
                },
                'energy': interpretation['energy'],
                'opportunity_score': event_opportunity['score'],
                'opportunity_description': event_opportunity['description']
            })
            
            # Avancer d'une semaine
            current_date += datetime.timedelta(days=7)
        
        # Identifier la meilleure période
        best_period = max(weekly_readings, key=lambda x: x['opportunity_score'])
        
        # Affiner l'analyse pour la semaine optimale en analysant chaque jour
        best_date = datetime.datetime.strptime(best_period['date'], '%Y-%m-%d')
        daily_readings = []
        
        for i in range(7):
            current_day = best_date + datetime.timedelta(days=i)
            if current_day > end:
                break
                
            # Générer une graine pour cette date spécifique
            day_seed = hash(f"{team_name}-{current_day.strftime('%Y-%m-%d')}-daily")
            
            # Tirer une carte pour ce jour
            card = self.draw_cards(1, day_seed)[0]
            interpretation = self._interpret_card(card)
            
            # Évaluer l'opportunité
            event_opportunity = self._evaluate_event_opportunity(
                interpretation, event_type
            )
            
            daily_readings.append({
                'date': current_day.strftime('%Y-%m-%d'),
                'weekday': current_day.strftime('%A'),
                'card': {
                    'name': card['name'],
                    'arcana': card['arcana'],
                    'reversed': card['reversed']
                },
                'energy': interpretation['energy'],
                'opportunity_score': event_opportunity['score'],
                'opportunity_description': event_opportunity['description']
            })
        
        # Identifier le jour optimal
        optimal_day = max(daily_readings, key=lambda x: x['opportunity_score'])
        
        # Préparer le résultat
        result = {
            'team_name': team_name,
            'event_type': event_type,
            'period': {
                'start_date': start_date,
                'end_date': end_date,
                'days_analyzed': days_count
            },
            'weekly_analysis': weekly_readings,
            'optimal_week': best_period,
            'daily_analysis': daily_readings,
            'optimal_day': optimal_day,
            'recommendation': {
                'date': optimal_day['date'],
                'weekday': optimal_day['weekday'],
                'card': optimal_day['card']['name'],
                'opportunity_score': optimal_day['opportunity_score'],
                'description': f"La date optimale recommandée est le {optimal_day['date']} ({optimal_day['weekday']}), sous l'influence de la carte {optimal_day['card']['name']} "
                              f"({optimal_day['energy']}). {optimal_day['opportunity_description']}"
            },
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # Ajouter à l'historique
        self.reading_history.append({
            'type': 'optimal_timing_analysis',
            'team': team_name,
            'event': event_type,
            'result': result
        })
        
        return result
    
    def _interpret_card(self, card):
        """Interpréter une carte de tarot."""
        if card['arcana'] == 'major':
            # Obtenir les informations sur l'arcane majeur
            arcana_info = self.major_arcana[card['index']]
            
            # Déterminer la signification selon l'orientation
            if card['reversed']:
                meaning = arcana_info['reversed_meaning']
                keywords = arcana_info['keywords'][:2]  # Utiliser moins de mots-clés pour les cartes inversées
            else:
                meaning = arcana_info['upright_meaning']
                keywords = arcana_info['keywords']
            
            return {
                'arcana_type': 'major',
                'name': arcana_info['name'],
                'energy': arcana_info['energy'],
                'meaning': meaning,
                'keywords': keywords,
                'reversed': card['reversed'],
                'influence_strength': 0.8 if not card['reversed'] else 0.6  # Les arcanes majeurs ont plus d'influence
            }
        
        else:  # arcane mineur
            # Obtenir les informations sur la famille et la valeur
            suit_info = self.minor_arcana_suits[card['suit']]
            value_meaning = self.minor_arcana_values[card['value']]
            
            # Construire une signification composite
            if card['reversed']:
                meaning = f"Aspect défié de {value_meaning} dans le domaine de {suit_info['domain']}."
            else:
                meaning = f"{value_meaning} dans le domaine de {suit_info['domain']}."
            
            # Déterminer des mots-clés basés sur la valeur et la famille
            keywords = [card['value'], card['suit'], suit_info['element']]
            
            return {
                'arcana_type': 'minor',
                'name': card['name'],
                'energy': f"{value_meaning} / {suit_info['element']}",
                'meaning': meaning,
                'keywords': keywords,
                'reversed': card['reversed'],
                'influence_strength': 0.6 if not card['reversed'] else 0.4  # Les arcanes mineurs ont moins d'influence
            }
    
    def _apply_to_sports(self, interpretation):
        """Adapter l'interprétation d'une carte au contexte sportif."""
        # Pour les arcanes majeurs
        if interpretation['arcana_type'] == 'major':
            card_name = interpretation['name']
            reversed = interpretation['reversed']
            
            # Obtenir l'information spécifique au sport
            arcana_index = next((i for i, info in self.major_arcana.items() if info['name'] == card_name), None)
            
            if arcana_index is not None:
                sport_info = self.major_arcana[arcana_index]['sport_influence']
                orientation = 'reversed' if reversed else 'upright'
                
                return {
                    'general': sport_info[orientation],
                    'teams': sport_info['teams'],
                    'player_type': sport_info['player_type'],
                    'game_phase': sport_info['game_phase']
                }
        
        # Pour les arcanes mineurs
        else:
            suit = interpretation.get('keywords', [])[1] if len(interpretation.get('keywords', [])) > 1 else None
            reversed = interpretation['reversed']
            
            if suit and suit in self.minor_arcana_suits:
                sport_aspect = self.minor_arcana_suits[suit]['sport_aspect']
                
                # Adapter l'aspect sportif selon l'orientation
                if reversed:
                    general_meaning = f"Difficulté ou défi concernant: {sport_aspect}"
                else:
                    general_meaning = f"Influence positive concernant: {sport_aspect}"
                
                return {
                    'general': general_meaning,
                    'aspect': sport_aspect,
                    'element': self.minor_arcana_suits[suit]['element']
                }
        
        # Par défaut, retourner une interprétation générique
        return {
            'general': "Influence à considérer dans le contexte sportif",
            'note': "Pas d'application sportive spécifique"
        }
    
    def _calculate_cards_synergy(self, cards):
        """Calculer la synergie entre plusieurs cartes."""
        if len(cards) < 2:
            return {'synergy_level': 0, 'description': "Pas assez de cartes pour calculer une synergie"}
        
        # Compter les types d'arcanes
        major_count = sum(1 for card in cards if card['arcana'] == 'major')
        minor_count = len(cards) - major_count
        
        # Analyser les orientations
        upright_count = sum(1 for card in cards if not card.get('reversed', False))
        reversed_count = len(cards) - upright_count
        
        # Pour les arcanes mineurs, compter les occurrences des familles
        suits_count = defaultdict(int)
        for card in cards:
            if card['arcana'] == 'minor':
                suits_count[card.get('suit', '')] += 1
        
        # Déterminer si certaines familles sont prédominantes
        dominant_suit = max(suits_count.items(), key=lambda x: x[1])[0] if suits_count else None
        dominant_count = max(suits_count.values()) if suits_count else 0
        
        # Calculer le niveau de synergie
        synergy_level = 0.5  # Niveau neutre par défaut
        
        # Ajuster selon la composition
        if major_count > minor_count:
            synergy_level += 0.1  # Influence forte des arcanes majeurs
        
        if upright_count > reversed_count:
            synergy_level += 0.1  # Orientation positive globale
        elif reversed_count > upright_count:
            synergy_level -= 0.1  # Orientation négative globale
        
        # Ajuster selon la cohérence des familles (pour les arcanes mineurs)
        if dominant_count > 1 and dominant_count >= minor_count * 0.7:
            synergy_level += 0.15  # Forte cohérence élémentaire
            dominant_element = self.minor_arcana_suits[dominant_suit]['element'] if dominant_suit else ""
        else:
            dominant_element = "mixte"
        
        # Limiter la synergie entre 0 et 1
        synergy_level = max(0.0, min(1.0, synergy_level))
        
        # Préparer la description de la synergie
        if synergy_level > 0.7:
            description = f"Forte synergie entre les cartes, dominée par l'élément {dominant_element}"
        elif synergy_level > 0.5:
            description = f"Synergie modérée, influence de l'élément {dominant_element}"
        elif synergy_level > 0.3:
            description = f"Faible synergie, énergies diverses avec présence de l'élément {dominant_element}"
        else:
            description = "Peu de synergie entre les cartes, énergies contradictoires"
        
        return {
            'synergy_level': synergy_level,
            'description': description,
            'major_minor_ratio': {'major': major_count, 'minor': minor_count},
            'upright_reversed_ratio': {'upright': upright_count, 'reversed': reversed_count},
            'dominant_element': dominant_element
        }
    
    def _interpret_overall_reading(self, interpretations, energies, synergy):
        """Interpréter un tirage complet pour en tirer une conclusion globale."""
        # Calculer l'énergie globale pondérée
        total_weight = sum(e['weight'] for e in energies)
        overall_energy = " / ".join(set(e['energy'].split(",")[0].strip() for e in energies))
        
        # Déterminer l'orientation globale du tirage
        reversed_count = sum(1 for i in interpretations if i['card']['reversed'])
        reading_orientation = "challengée" if reversed_count > len(interpretations) / 2 else "favorable"
        
        # Construire une interprétation basée sur les cartes et leur synergie
        if synergy['synergy_level'] > 0.6:
            coherence = "forte cohérence interne"
        elif synergy['synergy_level'] > 0.4:
            coherence = "cohérence modérée"
        else:
            coherence = "faible cohérence, énergies contradictoires"
        
        # Créer une synthèse globale
        synthesis = f"Le tirage révèle une énergie globale de {overall_energy}, avec une orientation {reading_orientation} et une {coherence}."
        
        # Ajouter des observations basées sur la composition des cartes
        if synergy['major_minor_ratio']['major'] > synergy['major_minor_ratio']['minor']:
            synthesis += " Les forces en jeu sont puissantes et significatives (prédominance d'arcanes majeurs)."
        else:
            synthesis += " Les énergies sont plus subtiles et contextuelles (prédominance d'arcanes mineurs)."
        
        if synergy['dominant_element'] != "mixte":
            synthesis += f" L'élément {synergy['dominant_element']} est particulièrement influent dans cette situation."
        
        return {
            'overall_energy': overall_energy,
            'orientation': reading_orientation,
            'coherence': coherence,
            'synthesis': synthesis,
            'dominant_element': synergy['dominant_element']
        }
    
    def _generate_advice(self, interpretation):
        """Générer un conseil basé sur l'interprétation d'une carte."""
        # Base du conseil selon le type d'arcane
        if interpretation['arcana_type'] == 'major':
            # Pour les arcanes majeurs
            card_name = interpretation['name']
            reversed = interpretation['reversed']
            
            # Conseils spécifiques pour chaque arcane majeur
            if card_name == 'Le Mat':
                if reversed:
                    return "Attention aux risques excessifs et au manque de préparation"
                else:
                    return "Embrassez l'imprévisibilité et soyez prêt à improviser"
            
            elif card_name == 'Le Bateleur':
                if reversed:
                    return "Concentrez-vous sur la précision technique et la confiance en vos capacités"
                else:
                    return "Utilisez votre habileté technique et votre créativité pour créer des opportunités"
            
            # Autres arcanes majeurs...
            elif card_name == 'La Papesse':
                if reversed:
                    return "Ne négligez pas les informations disponibles et faites confiance à votre intuition"
                else:
                    return "Observez attentivement et utilisez votre intelligence tactique"
            
            # Conseil par défaut pour les autres arcanes majeurs
            else:
                return "Considérez l'énergie de cette carte dans votre approche du match"
        
        else:
            # Pour les arcanes mineurs
            suit = interpretation.get('keywords', [])[1] if len(interpretation.get('keywords', [])) > 1 else None
            value = interpretation.get('keywords', [])[0] if interpretation.get('keywords', []) else None
            reversed = interpretation['reversed']
            
            # Conseils basés sur la famille
            if suit == 'cups':
                if reversed:
                    return "Attention à l'impact émotionnel et à la cohésion d'équipe"
                else:
                    return "Utilisez l'intelligence émotionnelle et renforcez les liens d'équipe"
            
            elif suit == 'wands':
                if reversed:
                    return "Gérez votre énergie efficacement et évitez l'impulsivité"
                else:
                    return "Canalisez votre passion et votre énergie de manière constructive"
            
            elif suit == 'swords':
                if reversed:
                    return "Évitez les conflits inutiles et clarifiez votre stratégie"
                else:
                    return "Utilisez votre intelligence tactique et votre précision"
            
            elif suit == 'pentacles':
                if reversed:
                    return "Renforcez votre base défensive et votre stabilité"
                else:
                    return "Capitalisez sur votre solidité et votre endurance"
            
            # Conseil par défaut pour les autres arcanes mineurs
            else:
                return "Adaptez votre approche en fonction de l'énergie de cette carte"
        
        return "Considérez les messages de cette carte dans votre approche"
    
    def _generate_advice_from_spread(self, interpretations, overall_interpretation):
        """Générer un conseil basé sur l'interprétation complète d'un tirage."""
        # Extraire les éléments clés des interprétations
        energies = [i['meaning'] for i in interpretations]
        keywords = [k for i in interpretations for k in i.get('keywords', [])]
        
        # Tenir compte de l'orientation globale
        orientation = overall_interpretation['orientation']
        
        # Construire un conseil adapté
        if orientation == "favorable":
            advice_base = "Capitalisez sur les énergies positives présentes"
        else:
            advice_base = "Soyez attentif aux défis indiqués et adaptez votre approche"
        
        # Ajouter des conseils spécifiques selon les positions
        position_advice = []
        
        for interp in interpretations:
            position = interp['position']
            
            if position == 'past' or position == 'situation':
                if interp['card']['reversed']:
                    position_advice.append("Prenez conscience des difficultés récentes mais ne vous y attardez pas")
                else:
                    position_advice.append("Construisez sur les bases établies précédemment")
            
            elif position == 'present' or position == 'challenge':
                if interp['card']['reversed']:
                    position_advice.append("Abordez les obstacles actuels avec lucidité et adaptabilité")
                else:
                    position_advice.append("Utilisez pleinement les forces actuellement disponibles")
            
            elif position == 'future' or position == 'advice':
                if interp['card']['reversed']:
                    position_advice.append("Préparez-vous aux défis à venir en renforçant vos points faibles")
                else:
                    position_advice.append("Orientez-vous vers les opportunités qui se présentent")
        
        # Combiner le tout
        full_advice = f"{advice_base}. " + " ".join(position_advice)
        
        return full_advice
    
    def _adapt_to_position(self, interpretation, sport_meaning, position, context):
        """Adapter l'interprétation d'une carte à sa position spécifique dans un tirage."""
        team1 = context.get('team1', 'Équipe 1')
        team2 = context.get('team2', 'Équipe 2')
        
        # Adapter selon la position
        if position == 'match_energy':
            return f"L'énergie globale du match est caractérisée par {interpretation['energy']}. {sport_meaning['general']}"
        
        elif position == 'team1_energy':
            return f"{team1} apporte une énergie de {interpretation['energy']}. {sport_meaning['general']}"
        
        elif position == 'team2_energy':
            return f"{team2} apporte une énergie de {interpretation['energy']}. {sport_meaning['general']}"
        
        elif position == 'first_half':
            return f"La première mi-temps sera marquée par {interpretation['energy']}. {sport_meaning['general']}"
        
        elif position == 'second_half':
            return f"La seconde mi-temps sera caractérisée par {interpretation['energy']}. {sport_meaning['general']}"
        
        elif position == 'key_moment':
            return f"Un moment clé du match sera défini par {interpretation['energy']}. {sport_meaning['general']}"
        
        elif position == 'outcome':
            reversed = interpretation['reversed']
            outcome_text = "Le résultat final reflètera une énergie"
            
            if reversed:
                outcome_text += " complexe ou challengée"
            else:
                outcome_text += " claire et directe"
            
            return f"{outcome_text} de {interpretation['energy']}. {sport_meaning['general']}"
        
        # Position par défaut
        return f"Dans cette position, l'énergie de {interpretation['energy']} signifie: {sport_meaning['general']}"
    
    def _compare_team_energies(self, team1_interpretation, team2_interpretation):
        """Comparer les énergies des deux équipes pour déterminer avantages et compatibilités."""
        team1_card = team1_interpretation['card']
        team2_card = team2_interpretation['card']
        
        team1_name = team1_interpretation['position_name'].replace('Énergie de ', '')
        team2_name = team2_interpretation['position_name'].replace('Énergie de ', '')
        
        # Déterminer les principales caractéristiques de chaque équipe
        team1_traits = {
            'arcana_type': 'major' if team1_card['arcana'] == 'major' else 'minor',
            'orientation': 'reversed' if team1_card['reversed'] else 'upright',
            'energy': team1_interpretation.get('meaning', '')
        }
        
        team2_traits = {
            'arcana_type': 'major' if team2_card['arcana'] == 'major' else 'minor',
            'orientation': 'reversed' if team2_card['reversed'] else 'upright',
            'energy': team2_interpretation.get('meaning', '')
        }
        
        # Calculer l'avantage relatif
        advantage_factors = {
            'arcana_weight': 0.3 if team1_traits['arcana_type'] == team2_traits['arcana_type'] else 0.0,
            'orientation_weight': 0.4 if team1_traits['orientation'] != 'reversed' and team2_traits['orientation'] == 'reversed' else
                              (-0.4 if team1_traits['orientation'] == 'reversed' and team2_traits['orientation'] != 'reversed' else 0.0)
        }
        
        # Intégrer la compatibilité élémentaire pour les arcanes mineurs
        elemental_advantage = 0.0
        
        # Déterminer l'avantage global
        net_advantage = sum(advantage_factors.values()) + elemental_advantage
        
        advantage_team = None
        if net_advantage > 0.2:
            advantage_team = team1_name
            advantage_desc = f"Avantage pour {team1_name} en raison de son énergie plus favorable"
        elif net_advantage < -0.2:
            advantage_team = team2_name
            advantage_desc = f"Avantage pour {team2_name} en raison de son énergie plus favorable"
        else:
            advantage_team = "neutre"
            advantage_desc = "Énergies équilibrées entre les équipes, sans avantage significatif"
        
        # Analyser la compatibilité/opposition des énergies
        if team1_card['arcana'] == 'major' and team2_card['arcana'] == 'major':
            cards_relationship = self._analyze_major_arcana_relationship(team1_card['name'], team2_card['name'])
        else:
            cards_relationship = "Les énergies des équipes présentent des dynamiques intéressantes"
        
        # Résumer la comparaison
        return {
            'advantage': {
                'team': advantage_team,
                'description': advantage_desc,
                'magnitude': abs(net_advantage)
            },
            'energies': {
                team1_name: team1_traits['energy'],
                team2_name: team2_traits['energy']
            },
            'cards_relationship': cards_relationship
        }
    
    def _interpret_match_flow(self, first_half, second_half, key_moment):
        """Interpréter le déroulement du match basé sur les cartes des mi-temps et moment clé."""
        # Extraire les informations pertinentes
        first_half_card = first_half['card']
        second_half_card = second_half['card']
        key_moment_card = key_moment['card']
        
        # Analyser l'évolution énergétique entre première et seconde mi-temps
        energy_evolution = "équilibrée"
        if first_half_card['reversed'] and not second_half_card['reversed']:
            energy_evolution = "améliorée"
        elif not first_half_card['reversed'] and second_half_card['reversed']:
            energy_evolution = "dégradée"
        
        # Analyser la nature du moment clé
        key_nature = "transformateur"
        if key_moment_card['arcana'] == 'major':
            key_nature = "décisif et majeur"
        if key_moment_card['reversed']:
            key_nature += ", potentiellement problématique"
        else:
            key_nature += ", potentiellement favorable"
        
        # Déterminer quand le moment clé pourrait survenir
        moment_timing = "indéterminé"
        if first_half_card['name'] == key_moment_card['name'] or self._cards_are_related(first_half_card, key_moment_card):
            moment_timing = "probablement en première mi-temps"
        elif second_half_card['name'] == key_moment_card['name'] or self._cards_are_related(second_half_card, key_moment_card):
            moment_timing = "probablement en seconde mi-temps"
        else:
            # Estimation basée sur la nature des cartes
            if key_moment_card['arcana'] == 'major':
                if key_moment_card['reversed']:
                    moment_timing = "possiblement en fin de match"
                else:
                    moment_timing = "possiblement à un moment crucial du match"
        
        # Analyser le rythme global du match
        match_rhythm = "équilibré"
        if first_half_card['arcana'] == 'major' and second_half_card['arcana'] == 'minor':
            match_rhythm = "démarrage fort puis stabilisation"
        elif first_half_card['arcana'] == 'minor' and second_half_card['arcana'] == 'major':
            match_rhythm = "démarrage lent puis intensification"
        
        # Préparer l'analyse
        flow_analysis = {
            'energy_evolution': energy_evolution,
            'key_moment': {
                'nature': key_nature,
                'timing': moment_timing
            },
            'match_rhythm': match_rhythm,
            'first_half_character': first_half['meaning'],
            'second_half_character': second_half['meaning'],
            'key_moment_character': key_moment['meaning']
        }
        
        return flow_analysis
    
    def _identify_dominant_arcana(self, cards):
        """Identifier les arcanes dominants dans un tirage."""
        # Compter les occurrences des arcanes majeurs
        major_counts = defaultdict(int)
        for card in cards:
            if card['arcana'] == 'major':
                major_counts[card['index']] += 1
        
        # Déterminer les arcanes majeurs dominants
        dominant_majors = [
            {
                'name': self.major_arcana[idx]['name'],
                'energy': self.major_arcana[idx]['energy'],
                'count': count
            }
            for idx, count in major_counts.items()
            if count > 0
        ]
        
        # Compter les occurrences des familles d'arcanes mineurs
        suit_counts = defaultdict(int)
        for card in cards:
            if card['arcana'] == 'minor':
                suit_counts[card['suit']] += 1
        
        # Déterminer les familles dominantes
        dominant_suits = [
            {
                'suit': suit,
                'element': self.minor_arcana_suits[suit]['element'],
                'energy': self.minor_arcana_suits[suit]['domain'],
                'count': count
            }
            for suit, count in suit_counts.items()
            if count > 0
        ]
        
        # Organiser par influence
        dominant_majors.sort(key=lambda x: x['count'], reverse=True)
        dominant_suits.sort(key=lambda x: x['count'], reverse=True)
        
        return {
            'major_arcana': dominant_majors[:2],  # Les 2 plus dominants
            'minor_suits': dominant_suits[:2]     # Les 2 plus dominants
        }
    
    def _calculate_match_prediction(self, interpretations, team_comparison, dominant_arcana):
        """Calculer une prédiction pour le match basée sur les cartes et analyses."""
        # Extraire l'interprétation du résultat
        outcome_card = next((i for i in interpretations if i['position'] == 'outcome'), None)
        
        # Déterminer l'avantage d'équipe
        advantage_team = team_comparison['advantage']['team']
        advantage_magnitude = team_comparison['advantage']['magnitude']
        
        # Pondérer la prédiction
        prediction_confidence = 0.5  # Base neutre
        
        # Augmenter la confiance si l'avantage est significatif
        if advantage_magnitude > 0.3:
            prediction_confidence += 0.15
        
        # Ajuster selon l'orientation de la carte de résultat
        if outcome_card and outcome_card['card']['reversed']:
            prediction_confidence -= 0.1  # Résultat moins clair si carte inversée
        
        # Limiter entre 0.3 et 0.8 (tarot n'est jamais 100% certain)
        prediction_confidence = max(0.3, min(0.8, prediction_confidence))
        
        # Formater la prédiction
        if advantage_team == "neutre":
            prediction = {
                'outcome': 'match_balanced',
                'description': "Match équilibré sans vainqueur clair",
                'confidence': prediction_confidence,
                'favored_team': None
            }
        else:
            prediction = {
                'outcome': 'team_advantage',
                'description': f"Avantage énergétique pour {advantage_team}",
                'confidence': prediction_confidence,
                'favored_team': advantage_team
            }
        
        # Ajouter des nuances basées sur les arcanes dominants
        if dominant_arcana['major_arcana'] and outcome_card:
            dominant_major = dominant_arcana['major_arcana'][0]['name']
            
            # Modifiers spécifiques basés sur certains arcanes majeurs dominants
            if dominant_major == 'La Roue de Fortune' or dominant_major == 'Le Monde':
                prediction['description'] += " avec potentiel de tournants décisifs"
            elif dominant_major == 'Le Mat' or dominant_major == 'La Maison Dieu':
                prediction['description'] += " mais avec forte imprévisibilité"
                prediction['confidence'] = max(0.3, prediction['confidence'] - 0.1)
            elif dominant_major == 'La Justice':
                prediction['description'] += " avec un résultat qui reflétera le mérite"
            elif dominant_major == 'La Force' or dominant_major == 'L\'Empereur':
                prediction['description'] += " avec domination probable"
                prediction['confidence'] += 0.05
        
        return prediction
    
    def _identify_team_archetypes(self, cards, interpretations):
        """Identifier les archétypes d'équipe dominants basés sur le tirage."""
        archetypes = []
        
        # Vérifier l'archétype basé sur la carte d'essence d'équipe
        team_essence = next((i for i in interpretations if i['position'] == 'team_essence'), None)
        
        if team_essence:
            essence_card = team_essence['card']
            
            # Déterminer l'archétype principal
            if essence_card['arcana'] == 'major':
                # Archétypes basés sur les arcanes majeurs
                card_name = essence_card['name']
                reversed = essence_card['reversed']
                
                if card_name == 'Le Bateleur' and not reversed:
                    archetypes.append({
                        'type': 'technical_innovator',
                        'description': "Équipe technique et créative, valorisant l'habileté individuelle",
                        'strength': 0.8
                    })
                elif card_name == 'L\'Empereur' and not reversed:
                    archetypes.append({
                        'type': 'dominant_controller',
                        'description': "Équipe structurée et autoritaire, cherchant à contrôler le jeu",
                        'strength': 0.85
                    })
                elif card_name == 'Le Chariot' and not reversed:
                    archetypes.append({
                        'type': 'determined_competitor',
                        'description': "Équipe déterminée et compétitive, orientée vers la victoire",
                        'strength': 0.9
                    })
                elif card_name == 'La Force' and not reversed:
                    archetypes.append({
                        'type': 'physical_powerhouse',
                        'description': "Équipe physiquement dominante avec forte résilience mentale",
                        'strength': 0.85
                    })
                elif card_name == 'Tempérance' and not reversed:
                    archetypes.append({
                        'type': 'balanced_harmonizer',
                        'description': "Équipe équilibrée avec grand sens de l'harmonie collective",
                        'strength': 0.8
                    })
                elif card_name == 'L\'Étoile' and not reversed:
                    archetypes.append({
                        'type': 'inspiring_talent',
                        'description': "Équipe talentueuse et inspirante avec grande fluidité",
                        'strength': 0.75
                    })
                elif card_name == 'Le Soleil' and not reversed:
                    archetypes.append({
                        'type': 'dominant_winner',
                        'description': "Équipe rayonnante et victorieuse avec grande vitalité",
                        'strength': 0.9
                    })
                # Archétypes pour les cartes inversées
                elif card_name == 'La Maison Dieu' and reversed:
                    archetypes.append({
                        'type': 'team_in_reconstruction',
                        'description': "Équipe en reconstruction après bouleversements",
                        'strength': 0.7
                    })
                elif card_name == 'Le Pendu' and reversed:
                    archetypes.append({
                        'type': 'stagnant_transitioner',
                        'description': "Équipe en transition difficile, cherchant un nouveau départ",
                        'strength': 0.65
                    })
                # Archétype par défaut
                else:
                    archetypes.append({
                        'type': 'complex_character',
                        'description': f"Équipe caractérisée par l'énergie de {card_name}",
                        'strength': 0.7
                    })
            
            else:
                # Archétypes basés sur les arcanes mineurs
                suit = essence_card.get('suit', '')
                if suit == 'cups':
                    archetypes.append({
                        'type': 'emotional_harmonizer',
                        'description': "Équipe intuitive valorisant l'harmonie et la connexion émotionnelle",
                        'strength': 0.75
                    })
                elif suit == 'wands':
                    archetypes.append({
                        'type': 'energetic_attacker',
                        'description': "Équipe énergique avec style offensif et passionné",
                        'strength': 0.8
                    })
                elif suit == 'swords':
                    archetypes.append({
                        'type': 'strategic_thinker',
                        'description': "Équipe analytique et stratégique, précise et directe",
                        'strength': 0.75
                    })
                elif suit == 'pentacles':
                    archetypes.append({
                        'type': 'solid_builder',
                        'description': "Équipe solide et stable, valorisant l'endurance et la défense",
                        'strength': 0.8
                    })
        
        # Analyser les autres cartes pour identifier des archétypes secondaires
        strengths_card = next((i for i in interpretations if i['position'] == 'strengths'), None)
        challenges_card = next((i for i in interpretations if i['position'] == 'challenges'), None)
        
        # Archétype secondaire basé sur les forces
        if strengths_card:
            # Logique similaire pour déterminer un archétype secondaire
            secondary_archetype = self._identify_secondary_archetype(strengths_card['card'], 'strengths')
            if secondary_archetype:
                archetypes.append(secondary_archetype)
        
        # Archétype de défi basé sur les difficultés
        if challenges_card:
            challenge_archetype = self._identify_secondary_archetype(challenges_card['card'], 'challenges')
            if challenge_archetype:
                archetypes.append(challenge_archetype)
        
        return archetypes
    
    def _identify_secondary_archetype(self, card, position):
        """Identifier un archétype secondaire basé sur une carte de force ou défi."""
        if card['arcana'] == 'major':
            card_name = card['name']
            reversed = card['reversed']
            
            # Archétypes de force
            if position == 'strengths':
                if card_name == 'La Justice' and not reversed:
                    return {
                        'type': 'balanced_competitor',
                        'description': "Force secondaire: approche équilibrée et juste du jeu",
                        'strength': 0.7
                    }
                elif card_name == 'Le Bateleur' and not reversed:
                    return {
                        'type': 'technical_specialist',
                        'description': "Force secondaire: excellence technique et créativité",
                        'strength': 0.7
                    }
                # Autres mappings...
            
            # Archétypes de défi
            elif position == 'challenges':
                if card_name == 'La Tour' and not reversed:
                    return {
                        'type': 'vulnerability_to_collapse',
                        'description': "Défi: vulnérabilité aux effondrements soudains",
                        'strength': 0.6
                    }
                elif card_name == 'La Lune' and not reversed:
                    return {
                        'type': 'struggles_with_consistency',
                        'description': "Défi: difficultés avec la constance et les illusions",
                        'strength': 0.65
                    }
                # Autres mappings...
        
        elif card['arcana'] == 'minor':
            suit = card.get('suit', '')
            
            # Archétypes de force mineurs
            if position == 'strengths':
                if suit == 'wands':
                    return {
                        'type': 'passionate_performer',
                        'description': "Force secondaire: intensité et passion dans l'exécution",
                        'strength': 0.65
                    }
                # Autres mappings...
            
            # Archétypes de défi mineurs
            elif position == 'challenges':
                if suit == 'swords':
                    return {
                        'type': 'overthinking_tactician',
                        'description': "Défi: tendance à l'analyse excessive et aux conflits",
                        'strength': 0.55
                    }
                # Autres mappings...
        
        return None
    
    def _analyze_elemental_energies(self, cards):
        """Analyser la distribution des énergies élémentaires dans le tirage."""
        # Compter la présence des éléments
        element_counts = {
            'Feu': 0,   # Baguettes + certains arcanes majeurs
            'Eau': 0,   # Coupes + certains arcanes majeurs
            'Air': 0,   # Épées + certains arcanes majeurs
            'Terre': 0  # Pentacles + certains arcanes majeurs
        }
        
        # Associer certains arcanes majeurs à des éléments
        major_element_map = {
            'Le Bateleur': 'Air',
            'L\'Impératrice': 'Terre',
            'L\'Empereur': 'Feu',
            'Le Pape': 'Terre',
            'Les Amoureux': 'Air',
            'Le Chariot': 'Eau',
            'La Force': 'Feu',
            'L\'Hermite': 'Terre',
            'La Roue de Fortune': 'Feu',
            'La Justice': 'Air',
            'La Tempérance': 'Eau',
            'Le Diable': 'Feu',
            'La Tour': 'Feu',
            'L\'Étoile': 'Air',
            'La Lune': 'Eau',
            'Le Soleil': 'Feu',
            'Le Jugement': 'Feu',
            'Le Monde': 'Terre'
        }
        
        # Comptage des éléments dans les cartes
        for card in cards:
            if card['arcana'] == 'minor':
                suit = card.get('suit', '')
                if suit == 'wands':
                    element_counts['Feu'] += 1
                elif suit == 'cups':
                    element_counts['Eau'] += 1
                elif suit == 'swords':
                    element_counts['Air'] += 1
                elif suit == 'pentacles':
                    element_counts['Terre'] += 1
            else:  # Major arcana
                card_name = card['name']
                element = major_element_map.get(card_name)
                if element:
                    element_counts[element] += 1
        
        # Calculer les pourcentages
        total_cards = len(cards)
        element_percentages = {
            element: (count / total_cards * 100) if total_cards > 0 else 0
            for element, count in element_counts.items()
        }
        
        # Déterminer l'élément dominant
        dominant_element = max(element_counts.items(), key=lambda x: x[1])[0] if element_counts else None
        
        # Déterminer l'équilibre élémentaire
        max_element = max(element_counts.values()) if element_counts else 0
        min_element = min(element_counts.values()) if element_counts else 0
        balance_score = 1 - ((max_element - min_element) / max(1, total_cards))
        
        balance_description = "équilibré"
        if balance_score < 0.5:
            balance_description = "très déséquilibré"
        elif balance_score < 0.7:
            balance_description = "légèrement déséquilibré"
        
        # Interprétation des énergies élémentaires
        interpretations = {}
        
        if element_percentages['Feu'] > 40:
            interpretations['Feu'] = "Équipe très dynamique et offensive, menée par la passion et l'énergie"
        elif element_percentages['Feu'] > 25:
            interpretations['Feu'] = "Bonne présence d'énergie offensive et de dynamisme"
        
        if element_percentages['Eau'] > 40:
            interpretations['Eau'] = "Équipe très intuitive et fluide, avec grande cohésion émotionnelle"
        elif element_percentages['Eau'] > 25:
            interpretations['Eau'] = "Bonne présence d'intuition et de fluidité collective"
        
        if element_percentages['Air'] > 40:
            interpretations['Air'] = "Équipe très analytique et communicative, avec grande intelligence tactique"
        elif element_percentages['Air'] > 25:
            interpretations['Air'] = "Bonne présence d'intelligence tactique et de communication"
        
        if element_percentages['Terre'] > 40:
            interpretations['Terre'] = "Équipe très solide et stable, avec grande endurance défensive"
        elif element_percentages['Terre'] > 25:
            interpretations['Terre'] = "Bonne présence de stabilité et de solidité défensive"
        
        return {
            'counts': element_counts,
            'percentages': element_percentages,
            'dominant_element': dominant_element,
            'balance': {
                'score': balance_score,
                'description': balance_description
            },
            'interpretations': interpretations
        }
    
    def _generate_team_profile(self, interpretations, team_archetypes, elemental_energies):
        """Générer un profil d'équipe basé sur les analyses des cartes."""
        # Extraire les archétypes principaux
        main_archetype = team_archetypes[0] if team_archetypes else None
        archetype_desc = main_archetype['description'] if main_archetype else "Équipe sans archétype dominant clair"
        
        # Extraire l'élément dominant
        dominant_element = elemental_energies['dominant_element']
        element_desc = elemental_energies['interpretations'].get(dominant_element, "")
        
        # Construire le profil
        profile_components = [archetype_desc]
        
        if element_desc:
            profile_components.append(element_desc)
        
        # Ajouter les forces et défis majeurs
        strengths_card = next((i for i in interpretations if i['position'] == 'strengths'), None)
        challenges_card = next((i for i in interpretations if i['position'] == 'challenges'), None)
        
        if strengths_card:
            strengths_desc = f"Points forts: {strengths_card['meaning']}"
            profile_components.append(strengths_desc)
        
        if challenges_card:
            challenges_desc = f"Points faibles: {challenges_card['meaning']}"
            profile_components.append(challenges_desc)
        
        # Ajouter les tendances tactiques basées sur les éléments
        tactical_tendencies = []
        
        if elemental_energies['percentages']['Feu'] > 30:
            tactical_tendencies.append("approche offensive")
        
        if elemental_energies['percentages']['Eau'] > 30:
            tactical_tendencies.append("jeu fluide et adaptable")
        
        if elemental_energies['percentages']['Air'] > 30:
            tactical_tendencies.append("intelligence tactique")
        
        if elemental_energies['percentages']['Terre'] > 30:
            tactical_tendencies.append("solidité défensive")
        
        if tactical_tendencies:
            tactics_desc = f"Tendances tactiques: {', '.join(tactical_tendencies)}"
            profile_components.append(tactics_desc)
        
        # Construire le profil final
        profile = ". ".join(profile_components)
        
        # Déterminer le style de jeu optimal
        optimal_style = self._determine_optimal_playing_style(elemental_energies, main_archetype)
        
        return {
            'summary': profile,
            'archetype': main_archetype['type'] if main_archetype else "undefined",
            'dominant_element': dominant_element,
            'optimal_playing_style': optimal_style,
            'elemental_balance': elemental_energies['balance']['description']
        }
    
    def _determine_optimal_playing_style(self, elemental_energies, main_archetype):
        """Déterminer le style de jeu optimal pour l'équipe basé sur les énergies et l'archétype."""
        # Base du style selon l'élément dominant
        dominant = elemental_energies['dominant_element']
        
        style_base = ""
        if dominant == 'Feu':
            style_base = "Style offensif et dynamique"
        elif dominant == 'Eau':
            style_base = "Style fluide et intuitif"
        elif dominant == 'Air':
            style_base = "Style tactique et précis"
        elif dominant == 'Terre':
            style_base = "Style solide et structuré"
        else:
            style_base = "Style équilibré"
        
        # Ajuster selon l'archétype
        if main_archetype:
            archetype_type = main_archetype['type']
            
            if 'technical' in archetype_type:
                style_base += ", mettant l'accent sur la technicité"
            elif 'physical' in archetype_type:
                style_base += ", mettant l'accent sur la domination physique"
            elif 'balanced' in archetype_type:
                style_base += ", avec équilibre entre attaque et défense"
            elif 'dominant' in archetype_type:
                style_base += ", avec volonté de contrôler le match"
        
        # Ajustements basés sur l'équilibre élémentaire
        balance = elemental_energies['balance']['score']
        if balance < 0.5:
            style_base += ". Approche très spécialisée"
        else:
            style_base += ". Approche adaptable"
        
        return style_base
    
    def _analyze_major_arcana_relationship(self, card1_name, card2_name):
        """Analyser la relation entre deux arcanes majeurs."""
        # Simplification: quelques relations spécifiques entre arcanes majeurs
        special_relationships = {
            ('Le Soleil', 'La Lune'): "Opposition complémentaire entre clarté et mystère",
            ('L\'Empereur', 'L\'Impératrice'): "Complémentarité parfaite entre énergie masculine et féminine",
            ('Le Bateleur', 'Le Monde'): "Progression du début à l'accomplissement",
            ('La Justice', 'Le Jugement'): "Résonance entre équilibre terrestre et jugement spirituel",
            ('La Tour', 'La Maison Dieu'): "Intensification des énergies disruptives",
            ('Le Diable', 'La Tempérance'): "Opposition entre excès et équilibre",
            ('Le Chariot', 'La Force'): "Synergie entre mouvement et puissance"
        }
        
        # Vérifier dans les deux sens
        for (card_a, card_b), description in special_relationships.items():
            if (card1_name == card_a and card2_name == card_b) or (card1_name == card_b and card2_name == card_a):
                return description
        
        # Description générique si pas de relation spécifique
        return "Interaction intéressante entre différentes énergies archétypales"
    
    def _cards_are_related(self, card1, card2):
        """Déterminer si deux cartes sont liées d'une façon significative."""
        # Même arcane majeur
        if card1['arcana'] == 'major' and card2['arcana'] == 'major':
            if card1['name'] == card2['name']:
                return True
            
            # Vérifier les relations spéciales
            special_pairs = [
                ('Le Soleil', 'La Lune'), ('L\'Empereur', 'L\'Impératrice'),
                ('Le Bateleur', 'Le Monde'), ('La Justice', 'Le Jugement'),
                ('Le Mat', 'Le Monde'), ('Le Diable', 'Le Jugement')
            ]
            
            for pair in special_pairs:
                if (card1['name'] in pair and card2['name'] in pair):
                    return True
        
        # Même famille d'arcanes mineurs
        elif card1['arcana'] == 'minor' and card2['arcana'] == 'minor':
            if card1.get('suit', '') == card2.get('suit', ''):
                return True
        
        return False
    
    def _analyze_momentum(self, interpretations, current_minute, team1_score, team2_score):
        """Analyser le momentum actuel du match basé sur les cartes."""
        # Extraire les cartes pertinentes
        current_momentum_card = interpretations[0]['card']
        hidden_forces_card = interpretations[1]['card']
        emerging_trend_card = interpretations[2]['card']
        
        # Analyser le momentum actuel
        current_state = {
            'energy': interpretations[0]['meaning'],
            'orientation': 'challenging' if current_momentum_card['reversed'] else 'favorable',
            'strength': 0.7 if current_momentum_card['arcana'] == 'major' else 0.5
        }
        
        # Analyser la direction du momentum
        score_difference = team1_score - team2_score
        leading_team = 'team1' if score_difference > 0 else ('team2' if score_difference < 0 else 'balanced')
        
        momentum_direction = 'stable'
        if not emerging_trend_card['reversed'] and hidden_forces_card['reversed']:
            momentum_direction = 'improving'
        elif emerging_trend_card['reversed'] and not hidden_forces_card['reversed']:
            momentum_direction = 'deteriorating'
        
        # Déterminer l'équipe favorisée par le momentum
        favored_team = 'balanced'
        
        # Si une équipe mène au score et que le momentum est stable ou s'améliore
        if leading_team != 'balanced' and momentum_direction in ['stable', 'improving']:
            favored_team = leading_team
        # Si le match est équilibré mais que le momentum montre une tendance
        elif leading_team == 'balanced' and momentum_direction != 'stable':
            # Analyse basée sur les cartes (simplifié)
            if emerging_trend_card['arcana'] == 'major':
                # Analyse plus sophistiquée nécessaire ici
                if emerging_trend_card['name'] in ['Le Soleil', 'Le Chariot', 'La Force'] and not emerging_trend_card['reversed']:
                    favored_team = 'team1'  # Simplification
                elif emerging_trend_card['name'] in ['La Tour', 'La Lune', 'Le Diable'] and emerging_trend_card['reversed']:
                    favored_team = 'team2'  # Simplification
        
        # Évaluer la volatilité du momentum
        momentum_volatility = 'moderate'
        if hidden_forces_card['name'] in ['La Tour', 'Le Mat', 'La Roue de Fortune']:
            momentum_volatility = 'high'
        elif hidden_forces_card['name'] in ['L\'Hermite', 'Le Monde', 'La Justice']:
            momentum_volatility = 'low'
        
        # Prédire l'évolution à court terme
        short_term_prediction = ""
        if momentum_direction == 'improving':
            short_term_prediction = "Le momentum devrait continuer à s'améliorer, favorisant une dynamique positive"
        elif momentum_direction == 'deteriorating':
            short_term_prediction = "Le momentum pourrait se dégrader, créant des obstacles ou difficultés"
        else:
            short_term_prediction = "Le momentum devrait rester relativement stable dans l'immédiat"
        
        # Ajouter des nuances basées sur la volatilité
        if momentum_volatility == 'high':
            short_term_prediction += ", mais avec potentiel de changements brusques et imprévisibles"
        elif momentum_volatility == 'low':
            short_term_prediction += ", avec une progression régulière et prévisible"
        
        return {
            'current_state': current_state,
            'momentum_direction': momentum_direction,
            'favored_team': favored_team,
            'volatility': momentum_volatility,
            'short_term_prediction': short_term_prediction,
            'score_influence': "Le momentum actuel " + (
                "renforce l'avantage au score" if leading_team == favored_team and leading_team != 'balanced' else
                "pourrait permettre de renverser la tendance du score" if leading_team != favored_team and leading_team != 'balanced' else
                "pourrait faire basculer ce match équilibré"
            )
        }
    
    def _identify_dominant_energies(self, cards):
        """Identifier les énergies dominantes présentes dans les cartes tirées."""
        # Catégoriser les énergies
        energies = {
            'dynamic': 0,      # Énergie de changement, action
            'stable': 0,       # Énergie de maintien, conservation
            'creative': 0,     # Énergie de création, expression
            'destructive': 0,  # Énergie de destruction, transformation
            'intuitive': 0,    # Énergie d'intuition, perception
            'rational': 0,     # Énergie de rationalité, analyse
            'collective': 0,   # Énergie de groupe, cohésion
            'individual': 0    # Énergie individuelle, autonomie
        }
        
        # Mappings simplifié des arcanes majeurs vers les types d'énergie
        major_energy_map = {
            'Le Mat': ['dynamic', 'individual'],
            'Le Bateleur': ['creative', 'individual'],
            'La Papesse': ['intuitive', 'stable'],
            'L\'Impératrice': ['creative', 'intuitive'],
            'L\'Empereur': ['stable', 'rational'],
            'Le Pape': ['collective', 'stable'],
            'L\'Amoureux': ['intuitive', 'collective'],
            'Le Chariot': ['dynamic', 'individual'],
            'La Justice': ['rational', 'stable'],
            'L\'Hermite': ['intuitive', 'individual'],
            'La Roue de Fortune': ['dynamic', 'destructive'],
            'La Force': ['dynamic', 'stable'],
            'Le Pendu': ['intuitive', 'individual'],
            'La Mort': ['destructive', 'dynamic'],
            'Tempérance': ['stable', 'collective'],
            'Le Diable': ['destructive', 'individual'],
            'La Maison Dieu': ['destructive', 'dynamic'],
            'L\'Étoile': ['creative', 'intuitive'],
            'La Lune': ['intuitive', 'destructive'],
            'Le Soleil': ['creative', 'collective'],
            'Le Jugement': ['destructive', 'collective'],
            'Le Monde': ['collective', 'stable']
        }
        
        # Mappings des familles d'arcanes mineurs vers les types d'énergie
        minor_energy_map = {
            'cups': ['intuitive', 'collective'],
            'wands': ['dynamic', 'creative'],
            'swords': ['rational', 'destructive'],
            'pentacles': ['stable', 'rational']
        }
        
        # Analyser chaque carte
        for card in cards:
            if card['arcana'] == 'major':
                card_name = card['name']
                if card_name in major_energy_map:
                    for energy_type in major_energy_map[card_name]:
                        energies[energy_type] += 1 if not card['reversed'] else 0.5
            else:  # Minor arcana
                suit = card.get('suit', '')
                if suit in minor_energy_map:
                    for energy_type in minor_energy_map[suit]:
                        energies[energy_type] += 0.7 if not card['reversed'] else 0.3
        
        # Normaliser les scores
        total = sum(energies.values())
        if total > 0:
            normalized_energies = {k: v / total for k, v in energies.items()}
        else:
            normalized_energies = {k: 0 for k in energies}
        
        # Identifier les énergies dominantes (top 3)
        dominant_types = sorted(normalized_energies.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Interprétations des combinaisons d'énergies dominantes
        energy_combinations = {
            ('dynamic', 'creative'): "Énergie offensive explosive et imprévisible",
            ('dynamic', 'destructive'): "Potentiel de changements radicaux et moments pivots",
            ('stable', 'rational'): "Structure défensive solide et approche calculée",
            ('intuitive', 'collective'): "Intelligence collective fluide et adaptabilité",
            ('creative', 'intuitive'): "Créativité inspirée et moments de génie",
            ('rational', 'individual'): "Précision technique et performances individuelles"
        }
        
        # Vérifier si une combinaison dominante est présente
        dominant_pair = (dominant_types[0][0], dominant_types[1][0])
        reverse_pair = (dominant_types[1][0], dominant_types[0][0])
        
        combination_description = None
        if dominant_pair in energy_combinations:
            combination_description = energy_combinations[dominant_pair]
        elif reverse_pair in energy_combinations:
            combination_description = energy_combinations[reverse_pair]
        
        return {
            'energies': normalized_energies,
            'dominant': [{'type': e[0], 'strength': e[1]} for e in dominant_types],
            'balance': max(normalized_energies.values()) - min(normalized_energies.values()),
            'combination': combination_description
        }
    
    def _identify_momentum_pivot_points(self, interpretations, current_minute):
        """Identifier les points de pivotement potentiels pour le momentum."""
        # Extraire les cartes
        current_momentum = interpretations[0]['card']
        hidden_forces = interpretations[1]['card']
        emerging_trend = interpretations[2]['card']
        
        pivot_points = []
        
        # Analyser en fonction des cartes tirées
        # Certaines cartes indiquent des pivot points spécifiques
        if current_momentum['name'] == 'La Roue de Fortune':
            pivot_points.append({
                'timing': 'imminent',
                'description': "Changement imminent de momentum",
                'minute_estimate': current_minute + random.randint(3, 7)
            })
        
        if hidden_forces['name'] == 'La Maison Dieu':
            pivot_points.append({
                'timing': 'upcoming',
                'description': "Bouleversement majeur à venir",
                'minute_estimate': current_minute + random.randint(10, 15)
            })
        
        if emerging_trend['name'] == 'La Mort':
            pivot_points.append({
                'timing': 'later',
                'description': "Transformation complète du momentum",
                'minute_estimate': current_minute + random.randint(15, 25)
            })
        
        # Si pas de cartes spécifiques, estimer basé sur d'autres facteurs
        if not pivot_points:
            # Déterminer un point pivot possible basé sur le temps de jeu
            if current_minute < 30:
                pivot_points.append({
                    'timing': 'mid_first_half',
                    'description': "Possible changement de dynamique en milieu de première mi-temps",
                    'minute_estimate': random.randint(25, 35)
                })
            elif current_minute < 45:
                pivot_points.append({
                    'timing': 'before_halftime',
                    'description': "Potentiel moment décisif avant la mi-temps",
                    'minute_estimate': 45
                })
            elif current_minute < 60:
                pivot_points.append({
                    'timing': 'early_second_half',
                    'description': "Dynamique nouvelle possible en début de seconde période",
                    'minute_estimate': random.randint(48, 55)
                })
            elif current_minute < 75:
                pivot_points.append({
                    'timing': 'mid_second_half',
                    'description': "Changement possible en milieu de seconde période",
                    'minute_estimate': random.randint(70, 80)
                })
            else:
                pivot_points.append({
                    'timing': 'late_game',
                    'description': "Momentum final décisif en fin de match",
                    'minute_estimate': random.randint(85, 90)
                })
        
        return pivot_points
    
    def _evaluate_event_opportunity(self, interpretation, event_type):
        """Évaluer l'opportunité d'un événement basé sur l'interprétation d'une carte."""
        card_name = interpretation['name']
        reversed = interpretation['reversed']
        energy = interpretation['energy']
        
        # Score de base
        base_score = 0.5
        
        # Ajustements selon le type d'événement
        if event_type == 'match':
            # Cartes très favorables pour un match
            favorable_cards = ['Le Soleil', 'Le Chariot', 'La Force', 'La Justice', 'Tempérance']
            unfavorable_cards = ['La Tour', 'La Lune', 'Le Diable', 'La Mort', 'Le Pendu']
            
            if card_name in favorable_cards and not reversed:
                base_score += 0.3
            elif card_name in unfavorable_cards and not reversed:
                base_score -= 0.2
            elif card_name in favorable_cards and reversed:
                base_score -= 0.1
            elif card_name in unfavorable_cards and reversed:
                base_score += 0.1
        
        elif event_type == 'transfer':
            # Cartes favorables pour un transfert
            favorable_cards = ['Le Mat', 'Le Bateleur', 'La Mort', 'Le Monde', 'Le Jugement']
            unfavorable_cards = ['Le Pendu', 'La Tour', 'L\'Hermite', 'L\'Empereur']
            
            if card_name in favorable_cards and not reversed:
                base_score += 0.3
            elif card_name in unfavorable_cards and not reversed:
                base_score -= 0.2
            elif card_name in favorable_cards and reversed:
                base_score -= 0.1
            elif card_name in unfavorable_cards and reversed:
                base_score += 0.1
        
        elif event_type == 'training':
            # Cartes favorables pour un entraînement
            favorable_cards = ['L\'Hermite', 'La Papesse', 'L\'Empereur', 'Tempérance', 'L\'Étoile']
            unfavorable_cards = ['La Tour', 'Le Mat', 'Le Diable']
            
            if card_name in favorable_cards and not reversed:
                base_score += 0.3
            elif card_name in unfavorable_cards and not reversed:
                base_score -= 0.2
            elif card_name in favorable_cards and reversed:
                base_score -= 0.1
            elif card_name in unfavorable_cards and reversed:
                base_score += 0.1
        
        # Limiter le score entre 0 et 1
        final_score = max(0.0, min(1.0, base_score))
        
        # Générer une description
        if final_score > 0.8:
            description = f"Opportunité exceptionnelle. L'énergie de {card_name} ({energy}) est parfaitement alignée pour cet événement."
        elif final_score > 0.6:
            description = f"Bonne opportunité. L'énergie de {card_name} ({energy}) est favorable pour cet événement."
        elif final_score > 0.4:
            description = f"Opportunité moyenne. L'énergie de {card_name} ({energy}) est neutre pour cet événement."
        elif final_score > 0.2:
            description = f"Opportunité faible. L'énergie de {card_name} ({energy}) n'est pas idéale pour cet événement."
        else:
            description = f"Opportunité très défavorable. L'énergie de {card_name} ({energy}) est en opposition avec cet événement."
        
        return {
            'score': final_score,
            'description': description,
            'card': card_name,
            'reversed': reversed
        }