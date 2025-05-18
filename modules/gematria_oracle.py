"""
GematriaOracle - Module d'analyse numérique ésotérique pour ArcanShadow.
Fournit des analyses basées sur la Gematria pour enrichir les prédictions sportives.
"""
import re
import numpy as np
from collections import defaultdict

class GematriaOracle:
    """
    GematriaOracle - Module d'analyse numérique ésotérique utilisant la Gematria.
    Analyse les noms et termes liés aux matchs pour identifier des patterns numériques.
    """
    
    def __init__(self, meta_systems=None):
        """
        Initialise le module GematriaOracle.
        
        Args:
            meta_systems: Référence au module MetaSystems pour l'intégration
        """
        self.meta_systems = meta_systems
        self.systems = {
            'hébreu': self._create_hebrew_system(),
            'grec': self._create_greek_system(),
            'latin': self._create_latin_system(),
            'simple': self._create_simple_system(),
            'réduit': self._create_reduced_system()
        }
        self.correspondence_cache = {}
        self.resonance_patterns = defaultdict(list)
        self._register_events()
        
    def _create_hebrew_system(self):
        """Crée le système de valeurs numériques hébraïques."""
        hebrew = {}
        # Création d'un dictionnaire de correspondance entre caractères latins et valeurs hébraïques
        # Aleph = 1, Beth = 2, etc.
        values = [
            ('a', 1), ('b', 2), ('g', 3), ('d', 4), ('h', 5),
            ('v', 6), ('z', 7), ('ch', 8), ('t', 9), ('i', 10),
            ('k', 20), ('l', 30), ('m', 40), ('n', 50), ('s', 60),
            ('o', 70), ('p', 80), ('ts', 90), ('q', 100), ('r', 200),
            ('sh', 300), ('th', 400)
        ]
        for char, val in values:
            hebrew[char] = val
        return hebrew
    
    def _create_greek_system(self):
        """Crée le système de valeurs numériques grecques."""
        greek = {}
        # Création d'un dictionnaire de correspondance entre caractères latins et valeurs grecques
        # Alpha = 1, Beta = 2, etc.
        values = [
            ('a', 1), ('b', 2), ('g', 3), ('d', 4), ('e', 5),
            ('z', 7), ('h', 8), ('th', 9), ('i', 10), ('k', 20),
            ('l', 30), ('m', 40), ('n', 50), ('x', 60), ('o', 70),
            ('p', 80), ('q', 90), ('r', 100), ('s', 200), ('t', 300),
            ('u', 400), ('ph', 500), ('ch', 600), ('ps', 700), ('o', 800)
        ]
        for char, val in values:
            greek[char] = val
        return greek
    
    def _create_latin_system(self):
        """Crée le système de valeurs numériques latines (valeurs romaines)."""
        latin = {
            'i': 1, 'v': 5, 'x': 10, 'l': 50, 
            'c': 100, 'd': 500, 'm': 1000
        }
        return latin
    
    def _create_simple_system(self):
        """Crée un système simple où A=1, B=2, etc."""
        simple = {}
        for i, char in enumerate('abcdefghijklmnopqrstuvwxyz'):
            simple[char] = i + 1
        return simple
    
    def _create_reduced_system(self):
        """Crée un système réduit où les valeurs sont réduites à un seul chiffre."""
        reduced = {}
        for i, char in enumerate('abcdefghijklmnopqrstuvwxyz'):
            value = i + 1
            # Réduction numérique (ex: 12 -> 1+2 = 3)
            reduced_value = value
            while reduced_value >= 10:
                reduced_value = sum(int(digit) for digit in str(reduced_value))
            reduced[char] = reduced_value
        return reduced
    
    def calculate_value(self, text, system='simple'):
        """
        Calcule la valeur numérique d'un texte selon le système spécifié.
        
        Args:
            text (str): Le texte à analyser
            system (str): Le système à utiliser ('hébreu', 'grec', 'latin', 'simple', 'réduit')
            
        Returns:
            int: La valeur numérique du texte
        """
        if system not in self.systems:
            raise ValueError(f"Système inconnu: {system}")
            
        text = text.lower()
        system_dict = self.systems[system]
        
        # Gestion spéciale pour les systèmes avec digraphes (comme 'ch', 'sh', etc.)
        if system in ['hébreu', 'grec']:
            # Remplacer les digraphes avant le calcul
            for digraph in [k for k in system_dict.keys() if len(k) > 1]:
                text = text.replace(digraph, f"_{digraph}_")
                
            # Traiter chaque caractère ou digraph marqué
            value = 0
            parts = text.split('_')
            for part in parts:
                if part in system_dict:
                    value += system_dict[part]
                else:
                    # Pour les caractères individuels
                    for char in part:
                        if char in system_dict:
                            value += system_dict[char]
            return value
        else:
            # Pour les systèmes sans digraphes
            return sum(system_dict.get(char, 0) for char in text)
    
    def analyze_name(self, name, systems=None):
        """
        Analyse un nom selon différents systèmes de Gematria.
        
        Args:
            name (str): Le nom à analyser
            systems (list, optional): Liste des systèmes à utiliser. Si None, tous sont utilisés.
            
        Returns:
            dict: Valeurs numériques selon chaque système
        """
        if systems is None:
            systems = list(self.systems.keys())
            
        results = {}
        for system in systems:
            results[system] = self.calculate_value(name, system)
            
        # Ajouter quelques métriques dérivées
        results['somme'] = sum(results.values())
        results['moyenne'] = results['somme'] / len(results)
        results['écart-type'] = np.std(list(results.values()))
        
        return results
    
    def find_correspondences(self, name1, name2, threshold=0.8):
        """
        Trouve les correspondances numériques entre deux noms.
        
        Args:
            name1 (str): Premier nom
            name2 (str): Deuxième nom
            threshold (float): Seuil de similarité pour les correspondances
            
        Returns:
            dict: Correspondances numériques identifiées
        """
        # Utiliser le cache si disponible
        cache_key = f"{name1.lower()}:{name2.lower()}"
        if cache_key in self.correspondence_cache:
            return self.correspondence_cache[cache_key]
        
        values1 = self.analyze_name(name1)
        values2 = self.analyze_name(name2)
        
        correspondences = {}
        
        # Correspondances exactes
        exact_matches = []
        for system in self.systems.keys():
            if values1[system] == values2[system]:
                exact_matches.append(system)
        
        if exact_matches:
            correspondences['correspondances_exactes'] = exact_matches
        
        # Ratio de similarité
        similarities = {}
        for system in self.systems.keys():
            val1, val2 = values1[system], values2[system]
            # Éviter division par zéro
            max_val = max(val1, val2)
            if max_val > 0:
                similarity = min(val1, val2) / max_val
                if similarity >= threshold:
                    similarities[system] = similarity
        
        if similarities:
            correspondences['similarités'] = similarities
        
        # Sommes et produits
        sum1, sum2 = values1['somme'], values2['somme']
        correspondences['relation_sommes'] = sum1 / sum2 if sum2 != 0 else float('inf')
        
        # Motifs cachés
        hidden_patterns = self._find_hidden_patterns(values1, values2)
        if hidden_patterns:
            correspondences['motifs_cachés'] = hidden_patterns
        
        # Stocker dans le cache
        self.correspondence_cache[cache_key] = correspondences
        
        return correspondences
    
    def _find_hidden_patterns(self, values1, values2):
        """Trouve des motifs cachés dans les valeurs numériques."""
        patterns = []
        
        # Vérifier les relations multiplicatives (x2, x3, etc.)
        for system in self.systems.keys():
            val1, val2 = values1[system], values2[system]
            if val1 > 0 and val2 > 0:
                ratio = val2 / val1
                # Si le ratio est proche d'un nombre entier
                if abs(ratio - round(ratio)) < 0.05 and 1 <= round(ratio) <= 12:
                    patterns.append(f"{system}: relation x{round(ratio)}")
        
        # Vérifier les séquences de Fibonacci
        fibonacci_numbers = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
        for system in self.systems.keys():
            val = values1[system]
            if val in fibonacci_numbers:
                patterns.append(f"{system}: valeur Fibonacci ({val})")
            
            val = values2[system]
            if val in fibonacci_numbers:
                patterns.append(f"{system}: valeur Fibonacci ({val})")
        
        # Vérifier les nombres premiers
        def is_prime(n):
            """Vérifie si un nombre est premier."""
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
        
        for system in self.systems.keys():
            val = values1[system]
            if is_prime(val):
                patterns.append(f"{system}: nombre premier ({val})")
                
            val = values2[system]
            if is_prime(val):
                patterns.append(f"{system}: nombre premier ({val})")
        
        return patterns
    
    def analyze_match(self, home_team, away_team, date=None, competition=None):
        """
        Analyse un match selon les principes de Gematria.
        
        Args:
            home_team (str): Nom de l'équipe à domicile
            away_team (str): Nom de l'équipe à l'extérieur
            date (str, optional): Date du match
            competition (str, optional): Nom de la compétition
            
        Returns:
            dict: Analyse numérique du match
        """
        analysis = {
            'équipe_domicile': self.analyze_name(home_team),
            'équipe_extérieur': self.analyze_name(away_team),
            'correspondances': self.find_correspondences(home_team, away_team)
        }
        
        # Ajouter analyse de la date si disponible
        if date:
            analysis['date'] = self._analyze_date(date)
        
        # Ajouter analyse de la compétition si disponible
        if competition:
            analysis['compétition'] = self.analyze_name(competition)
            
        # Calculer la signature numérique globale du match
        signature = self._calculate_match_signature(home_team, away_team, date, competition)
        analysis['signature'] = signature
        
        # Identifier les résonances cycliques
        if date:
            cycles = self._identify_cycles(home_team, away_team, date)
            if cycles:
                analysis['cycles'] = cycles
        
        return analysis
    
    def _analyze_date(self, date_str):
        """Analyse la valeur numérique d'une date."""
        # Extraire les composantes de la date
        # Format attendu: YYYY-MM-DD ou DD/MM/YYYY
        if '-' in date_str:
            parts = date_str.split('-')
            if len(parts[0]) == 4:  # YYYY-MM-DD
                year, month, day = parts
            else:  # DD-MM-YYYY
                day, month, year = parts
        elif '/' in date_str:
            parts = date_str.split('/')
            if len(parts[2]) == 4:  # DD/MM/YYYY
                day, month, year = parts
            else:  # YYYY/MM/DD
                year, month, day = parts
        else:
            # Format non reconnu
            return {'erreur': 'Format de date non reconnu'}
        
        # Convertir en nombres
        try:
            day, month, year = int(day), int(month), int(year)
        except ValueError:
            return {'erreur': 'Valeurs de date non numériques'}
        
        # Calculs numériques
        day_reduced = sum(int(digit) for digit in str(day))
        month_reduced = sum(int(digit) for digit in str(month))
        year_reduced = sum(int(digit) for digit in str(year))
        
        date_sum = day + month + year
        date_product = day * month * year
        
        # Réduction numérique complète
        full_reduction = date_sum
        while full_reduction >= 10:
            full_reduction = sum(int(digit) for digit in str(full_reduction))
        
        return {
            'jour': day,
            'jour_réduit': day_reduced,
            'mois': month,
            'mois_réduit': month_reduced,
            'année': year,
            'année_réduite': year_reduced,
            'somme': date_sum,
            'produit': date_product,
            'réduction_complète': full_reduction
        }
    
    def _calculate_match_signature(self, home_team, away_team, date=None, competition=None):
        """Calcule une signature numérique globale pour le match."""
        # Valeurs de base des équipes
        home_values = self.analyze_name(home_team)
        away_values = self.analyze_name(away_team)
        
        # Valeur composite de base
        base_signature = {
            'simple': home_values['simple'] + away_values['simple'],
            'réduit': (home_values['réduit'] + away_values['réduit']) % 9 or 9,  # 9 au lieu de 0
            'rapport': home_values['simple'] / away_values['simple'] if away_values['simple'] != 0 else float('inf')
        }
        
        # Intégrer la date si disponible
        if date:
            date_analysis = self._analyze_date(date)
            if 'erreur' not in date_analysis:
                base_signature['date_influence'] = date_analysis['réduction_complète']
                # Facteur composite date-équipes
                composite = (home_values['simple'] + away_values['simple']) * date_analysis['réduction_complète']
                base_signature['composite'] = composite
                
                # Réduction du composite
                reduced_composite = composite
                while reduced_composite >= 10:
                    reduced_composite = sum(int(digit) for digit in str(reduced_composite))
                base_signature['composite_réduit'] = reduced_composite
        
        # Intégrer la compétition si disponible
        if competition:
            comp_values = self.analyze_name(competition)
            base_signature['compétition_influence'] = comp_values['simple'] % 9 or 9
            
        return base_signature
    
    def _identify_cycles(self, home_team, away_team, date_str):
        """Identifie les résonances cycliques basées sur la date et les équipes."""
        date_analysis = self._analyze_date(date_str)
        if 'erreur' in date_analysis:
            return []
        
        cycles = []
        
        # Cycle lunaire (basé sur le jour du mois)
        day = date_analysis['jour']
        lunar_phase = (day % 28) + 1  # 1-28
        lunar_position = ""
        if 1 <= lunar_phase <= 7:
            lunar_position = "Premier quartier"
        elif 8 <= lunar_phase <= 14:
            lunar_position = "Pleine lune"
        elif 15 <= lunar_phase <= 21:
            lunar_position = "Dernier quartier"
        else:
            lunar_position = "Nouvelle lune"
        
        cycles.append({"type": "lunaire", "phase": lunar_phase, "position": lunar_position})
        
        # Cycle annuel (saison)
        month = date_analysis['mois']
        season = ""
        if 3 <= month <= 5:
            season = "Printemps"
        elif 6 <= month <= 8:
            season = "Été"
        elif 9 <= month <= 11:
            season = "Automne"
        else:
            season = "Hiver"
        
        cycles.append({"type": "saison", "nom": season})
        
        # Cycle numérique personnel
        home_values = self.analyze_name(home_team)
        away_values = self.analyze_name(away_team)
        
        # Calculer le cycle personnel (1-9)
        personal_cycle_home = ((home_values['simple'] % 9) or 9)
        personal_cycle_away = ((away_values['simple'] % 9) or 9)
        
        # Le jour est-il en résonance avec l'une des équipes?
        day_reduced = date_analysis['jour_réduit']
        while day_reduced >= 10:
            day_reduced = sum(int(digit) for digit in str(day_reduced))
        
        resonances = []
        if day_reduced == personal_cycle_home:
            resonances.append(f"Jour en résonance avec {home_team}")
        if day_reduced == personal_cycle_away:
            resonances.append(f"Jour en résonance avec {away_team}")
        
        if resonances:
            cycles.append({"type": "résonance_jour", "détails": resonances})
        
        return cycles
    
    def generate_insights(self, match_analysis):
        """
        Génère des insights basés sur l'analyse numérique du match.
        
        Args:
            match_analysis (dict): Analyse complète du match par GematriaOracle
            
        Returns:
            dict: Insights numériques pour le match
        """
        insights = {}
        
        # Analyser les correspondances
        correspondences = match_analysis.get('correspondances', {})
        exact_matches = correspondences.get('correspondances_exactes', [])
        
        if exact_matches:
            insights['correspondances_notables'] = f"Correspondance exacte dans {len(exact_matches)} système(s): {', '.join(exact_matches)}"
        
        # Analyser la signature
        signature = match_analysis.get('signature', {})
        if 'composite_réduit' in signature:
            composite = signature['composite_réduit']
            if composite == 1:
                insights['signature_interprétation'] = "Commencement, individualité. Match qui pourrait marquer un nouveau départ."
            elif composite == 2:
                insights['signature_interprétation'] = "Dualité, coopération. Équilibre entre attaque et défense."
            elif composite == 3:
                insights['signature_interprétation'] = "Expression créative. Potentiel pour un match spectaculaire."
            elif composite == 4:
                insights['signature_interprétation'] = "Stabilité, structure. Match potentiellement tactique et discipliné."
            elif composite == 5:
                insights['signature_interprétation'] = "Changement, adaptation. Possibilité de rebondissements."
            elif composite == 6:
                insights['signature_interprétation'] = "Harmonie, équilibre. Match fluide avec bonne entente."
            elif composite == 7:
                insights['signature_interprétation'] = "Introspection, mystère. Match imprévisible avec des moments clés inattendus."
            elif composite == 8:
                insights['signature_interprétation'] = "Pouvoir, abondance. Potentiel pour un score élevé ou domination."
            elif composite == 9:
                insights['signature_interprétation'] = "Accomplissement, complétion. Match avec un résultat décisif ou significatif."
        
        # Analyser les cycles
        cycles = match_analysis.get('cycles', [])
        for cycle in cycles:
            if cycle['type'] == 'résonance_jour':
                insights['résonance_temporelle'] = "Alignement numérique entre la date et une équipe."
        
        # Avantage numérique
        home_values = match_analysis['équipe_domicile']
        away_values = match_analysis['équipe_extérieur']
        
        home_power = home_values['simple'] + (home_values['hébreu'] * 0.5) + (home_values['grec'] * 0.3)
        away_power = away_values['simple'] + (away_values['hébreu'] * 0.5) + (away_values['grec'] * 0.3)
        
        # Calculer la différence en pourcentage
        power_diff = ((home_power - away_power) / ((home_power + away_power) / 2)) * 100
        
        if abs(power_diff) > 20:  # Différence significative
            if power_diff > 0:
                insights['avantage_numérique'] = f"Avantage numérique substantiel pour l'équipe à domicile ({power_diff:.1f}%)."
            else:
                insights['avantage_numérique'] = f"Avantage numérique substantiel pour l'équipe à l'extérieur ({-power_diff:.1f}%)."
        elif abs(power_diff) > 10:  # Différence modérée
            if power_diff > 0:
                insights['avantage_numérique'] = f"Léger avantage numérique pour l'équipe à domicile ({power_diff:.1f}%)."
            else:
                insights['avantage_numérique'] = f"Léger avantage numérique pour l'équipe à l'extérieur ({-power_diff:.1f}%)."
        else:  # Différence faible
            insights['avantage_numérique'] = f"Équilibre numérique entre les équipes (différence: {abs(power_diff):.1f}%)."
        
        return insights
    
    def _register_events(self):
        """Enregistre les gestionnaires d'événements avec MetaSystems."""
        if self.meta_systems:
            self.meta_systems.register_event_handler("match_analysis_request", self._handle_match_analysis_request)
            self.meta_systems.register_event_handler("pattern_identified", self._handle_pattern_identified)
    
    def _handle_match_analysis_request(self, event_data):
        """
        Gestionnaire d'événement pour les demandes d'analyse de match.
        
        Args:
            event_data (dict): Données de l'événement
        """
        if 'home_team' in event_data and 'away_team' in event_data:
            home_team = event_data['home_team']
            away_team = event_data['away_team']
            date = event_data.get('date')
            competition = event_data.get('competition')
            
            analysis = self.analyze_match(home_team, away_team, date, competition)
            insights = self.generate_insights(analysis)
            
            # Envoyer les résultats via le système d'événements
            if self.meta_systems:
                self.meta_systems.trigger_event("gematria_analysis_complete", {
                    "match_id": event_data.get("match_id"),
                    "analysis": analysis,
                    "insights": insights
                })
    
    def _handle_pattern_identified(self, event_data):
        """
        Gestionnaire d'événement pour les patterns identifiés par d'autres modules.
        
        Args:
            event_data (dict): Données de l'événement
        """
        if 'pattern_type' in event_data and 'pattern_details' in event_data:
            pattern_type = event_data['pattern_type']
            pattern_details = event_data['pattern_details']
            
            # Stocker le pattern pour référence future
            self.resonance_patterns[pattern_type].append(pattern_details)
    
    def integrate_with_arcan_brain(self, arcan_brain_result):
        """
        Intègre les résultats de GematriaOracle avec ceux d'ArcanBrain.
        
        Args:
            arcan_brain_result (dict): Résultats de l'analyse ArcanBrain
            
        Returns:
            dict: Résultats enrichis
        """
        if not arcan_brain_result or not isinstance(arcan_brain_result, dict):
            return arcan_brain_result
        
        # Vérifier si l'analyse contient les informations nécessaires
        if 'match_data' not in arcan_brain_result:
            return arcan_brain_result
        
        match_data = arcan_brain_result['match_data']
        
        # Extraire les informations des équipes
        if 'home_team' in match_data and 'away_team' in match_data:
            home_team = match_data['home_team']
            away_team = match_data['away_team']
            date = match_data.get('date')
            competition = match_data.get('competition')
            
            # Effectuer l'analyse Gematria
            gematria_analysis = self.analyze_match(home_team, away_team, date, competition)
            gematria_insights = self.generate_insights(gematria_analysis)
            
            # Intégrer les résultats
            enriched_result = arcan_brain_result.copy()
            
            # Ajouter l'analyse Gematria
            if 'additional_analyses' not in enriched_result:
                enriched_result['additional_analyses'] = {}
            
            enriched_result['additional_analyses']['gematria'] = {
                'analysis': gematria_analysis,
                'insights': gematria_insights
            }
            
            # Intégrer les insights dans les insights principaux
            if 'insights' in enriched_result:
                for key, value in gematria_insights.items():
                    enriched_result['insights'][f'gematria_{key}'] = value
            
            return enriched_result
        
        return arcan_brain_result
    
    def integrate_with_numerics(self, numeri_code_results):
        """
        Intègre les résultats de NumeriCode avec l'analyse Gematria.
        
        Args:
            numeri_code_results (dict): Résultats de l'analyse NumeriCode
            
        Returns:
            dict: Résultats enrichis
        """
        if not numeri_code_results or not isinstance(numeri_code_results, dict):
            return numeri_code_results
        
        # Vérifier si les résultats contiennent les informations nécessaires
        if 'match_info' not in numeri_code_results:
            return numeri_code_results
        
        match_info = numeri_code_results['match_info']
        
        # Extraire les informations des équipes
        if 'home_team' in match_info and 'away_team' in match_info:
            home_team = match_info['home_team']
            away_team = match_info['away_team']
            
            # Effectuer une analyse simplifiée
            home_values = self.analyze_name(home_team)
            away_values = self.analyze_name(away_team)
            
            # Identifier les résonances entre les résultats NumeriCode et les valeurs Gematria
            resonances = []
            
            # Vérifier les séquences numériques de NumeriCode
            if 'sequences' in numeri_code_results:
                sequences = numeri_code_results['sequences']
                
                for seq_name, seq_value in sequences.items():
                    # Convertir en chaîne si nécessaire
                    if isinstance(seq_value, (list, tuple)):
                        seq_str = ''.join(map(str, seq_value))
                    else:
                        seq_str = str(seq_value)
                    
                    # Vérifier les résonances avec les valeurs Gematria
                    for system, value in home_values.items():
                        if isinstance(value, (int, float)) and str(value) in seq_str:
                            resonances.append(f"Résonance entre {home_team} ({system}: {value}) et séquence {seq_name}")
                    
                    for system, value in away_values.items():
                        if isinstance(value, (int, float)) and str(value) in seq_str:
                            resonances.append(f"Résonance entre {away_team} ({system}: {value}) et séquence {seq_name}")
            
            # Intégrer les résultats
            enriched_results = numeri_code_results.copy()
            
            enriched_results['gematria_integration'] = {
                'home_team_values': home_values,
                'away_team_values': away_values,
                'resonances': resonances
            }
            
            return enriched_results
        
        return numeri_code_results

class Calculateur:
    """Sous-module pour calculer les valeurs Gematria."""
    
    def __init__(self, gematria_oracle):
        """
        Initialise le calculateur.
        
        Args:
            gematria_oracle (GematriaOracle): Instance du module parent
        """
        self.gematria_oracle = gematria_oracle
        self.systems = gematria_oracle.systems
    
    def calculate_single_value(self, text, system='simple'):
        """
        Calcule la valeur selon un système spécifique.
        
        Args:
            text (str): Texte à analyser
            system (str): Système à utiliser
            
        Returns:
            int: Valeur numérique
        """
        return self.gematria_oracle.calculate_value(text, system)
    
    def calculate_all_systems(self, text):
        """
        Calcule la valeur selon tous les systèmes disponibles.
        
        Args:
            text (str): Texte à analyser
            
        Returns:
            dict: Valeurs selon chaque système
        """
        return {system: self.calculate_single_value(text, system) for system in self.systems}
    
    def calculate_phrase(self, phrase):
        """
        Calcule les valeurs pour chaque mot d'une phrase.
        
        Args:
            phrase (str): Phrase à analyser
            
        Returns:
            dict: Valeurs par mot et totaux
        """
        words = re.findall(r'\b\w+\b', phrase.lower())
        word_values = {word: self.calculate_all_systems(word) for word in words}
        
        # Calculer les totaux
        totals = {}
        for system in self.systems:
            totals[system] = sum(word_values[word][system] for word in words)
        
        return {
            'words': word_values,
            'totals': totals
        }

class Correspondance:
    """Sous-module pour identifier les correspondances numériques."""
    
    def __init__(self, gematria_oracle):
        """
        Initialise le module de correspondance.
        
        Args:
            gematria_oracle (GematriaOracle): Instance du module parent
        """
        self.gematria_oracle = gematria_oracle
        self.correspondence_cache = {}
    
    def find_team_correspondences(self, team_names, threshold=0.8):
        """
        Trouve les correspondances entre plusieurs équipes.
        
        Args:
            team_names (list): Liste des noms d'équipes
            threshold (float): Seuil de similarité
            
        Returns:
            dict: Correspondances entre équipes
        """
        results = {}
        
        # Comparer chaque paire d'équipes
        for i, team1 in enumerate(team_names):
            for j, team2 in enumerate(team_names[i+1:], i+1):
                key = f"{team1}-{team2}"
                results[key] = self.gematria_oracle.find_correspondences(team1, team2, threshold)
        
        return results
    
    def find_date_team_correspondence(self, team_name, date_str):
        """
        Trouve les correspondances entre une équipe et une date.
        
        Args:
            team_name (str): Nom de l'équipe
            date_str (str): Date à analyser
            
        Returns:
            dict: Correspondances identifiées
        """
        team_values = self.gematria_oracle.analyze_name(team_name)
        date_values = self.gematria_oracle._analyze_date(date_str)
        
        if 'erreur' in date_values:
            return {'erreur': date_values['erreur']}
        
        correspondences = {}
        
        # Vérifier les correspondances avec le jour
        day = date_values['jour']
        day_reduced = date_values['jour_réduit']
        
        for system, value in team_values.items():
            if isinstance(value, (int, float)):
                if value == day:
                    correspondences[f'jour_exact_{system}'] = value
                if value == day_reduced:
                    correspondences[f'jour_réduit_{system}'] = value
        
        # Vérifier les correspondances avec le mois
        month = date_values['mois']
        month_reduced = date_values['mois_réduit']
        
        for system, value in team_values.items():
            if isinstance(value, (int, float)):
                if value == month:
                    correspondences[f'mois_exact_{system}'] = value
                if value == month_reduced:
                    correspondences[f'mois_réduit_{system}'] = value
        
        # Vérifier les correspondances avec l'année réduite
        year_reduced = date_values['année_réduite']
        
        for system, value in team_values.items():
            if isinstance(value, (int, float)):
                if value == year_reduced:
                    correspondences[f'année_réduite_{system}'] = value
        
        return correspondences

class Traducteur:
    """Sous-module pour traduire les valeurs numériques en insights qualitatifs."""
    
    def __init__(self, gematria_oracle):
        """
        Initialise le traducteur.
        
        Args:
            gematria_oracle (GematriaOracle): Instance du module parent
        """
        self.gematria_oracle = gematria_oracle
        self.number_meanings = self._initialize_number_meanings()
    
    def _initialize_number_meanings(self):
        """Initialise les significations des nombres."""
        meanings = {
            1: "Commencement, individualité, leadership",
            2: "Dualité, coopération, équilibre",
            3: "Expression créative, croissance, expansion",
            4: "Stabilité, structure, ordre",
            5: "Changement, adaptation, liberté",
            6: "Harmonie, responsabilité, équilibre",
            7: "Analyse, perfectionnement, mystère",
            8: "Abondance, pouvoir, réussite matérielle",
            9: "Accomplissement, service, humanité",
            11: "Illumination, intuition, idéalisme",
            22: "Réalisation, pragmatisme, maîtrise",
            33: "Service altruiste, guérison, enseignement"
        }
        return meanings
    
    def translate_value(self, value):
        """
        Traduit une valeur numérique en signification.
        
        Args:
            value (int): Valeur à traduire
            
        Returns:
            str: Signification de la valeur
        """
        # Réduire le nombre si nécessaire
        reduced_value = value
        while reduced_value > 33:
            reduced_value = sum(int(digit) for digit in str(reduced_value))
            # Cas spéciaux pour 11, 22, 33
            if reduced_value <= 9 or reduced_value in [11, 22, 33]:
                break
        
        # Retourner la signification
        return self.number_meanings.get(reduced_value, "Pas de signification spécifique")
    
    def translate_analysis(self, analysis):
        """
        Traduit une analyse complète en interprétations qualitatives.
        
        Args:
            analysis (dict): Analyse numérique
            
        Returns:
            dict: Interprétations qualitatives
        """
        interpretations = {}
        
        # Interpréter les valeurs des équipes
        for team_key in ['équipe_domicile', 'équipe_extérieur']:
            if team_key in analysis:
                team_interpretations = {}
                for system, value in analysis[team_key].items():
                    if isinstance(value, (int, float)) and system in self.gematria_oracle.systems:
                        team_interpretations[system] = self.translate_value(value)
                interpretations[team_key] = team_interpretations
        
        # Interpréter la signature
        if 'signature' in analysis:
            signature = analysis['signature']
            signature_interpretations = {}
            
            for key, value in signature.items():
                if isinstance(value, (int, float)) and key not in ['rapport']:
                    signature_interpretations[key] = self.translate_value(value)
            
            interpretations['signature'] = signature_interpretations
        
        return interpretations

class RésonanceCyclique:
    """Sous-module pour analyser les cycles temporels et leur résonance numérique."""
    
    def __init__(self, gematria_oracle):
        """
        Initialise le module de résonance cyclique.
        
        Args:
            gematria_oracle (GematriaOracle): Instance du module parent
        """
        self.gematria_oracle = gematria_oracle
        self.cycle_patterns = self._initialize_cycle_patterns()
    
    def _initialize_cycle_patterns(self):
        """Initialise les modèles de cycles."""
        return {
            # Cycles personnels (1-9)
            'personnel': {
                1: "Cycle d'initiative et de nouveaux départs",
                2: "Cycle de coopération et de diplomatie",
                3: "Cycle d'expression et de créativité",
                4: "Cycle de construction et de stabilité",
                5: "Cycle de changement et d'adaptation",
                6: "Cycle de responsabilité et d'équilibre",
                7: "Cycle d'analyse et d'introspection",
                8: "Cycle de pouvoir et d'abondance",
                9: "Cycle de conclusion et d'accomplissement"
            },
            # Cycles lunaires
            'lunaire': {
                'Premier quartier': "Cycle de croissance et de développement",
                'Pleine lune': "Cycle d'illumination et de révélation",
                'Dernier quartier': "Cycle de relâchement et de libération",
                'Nouvelle lune': "Cycle de renouvellement et de potentialité"
            },
            # Cycles saisonniers
            'saison': {
                'Printemps': "Cycle de renaissance et de croissance",
                'Été': "Cycle d'expression maximale et de vitalité",
                'Automne': "Cycle de récolte et de transition",
                'Hiver': "Cycle de repos et de préparation"
            }
        }
    
    def analyze_date_cycles(self, date_str):
        """
        Analyse les cycles associés à une date.
        
        Args:
            date_str (str): Date à analyser
            
        Returns:
            dict: Cycles identifiés
        """
        date_analysis = self.gematria_oracle._analyze_date(date_str)
        if 'erreur' in date_analysis:
            return {'erreur': date_analysis['erreur']}
        
        cycles = {}
        
        # Cycle personnel (basé sur la réduction complète)
        personal_cycle = date_analysis['réduction_complète']
        if personal_cycle > 9:
            personal_cycle = sum(int(digit) for digit in str(personal_cycle))
        
        cycles['personnel'] = {
            'nombre': personal_cycle,
            'signification': self.cycle_patterns['personnel'].get(personal_cycle, "Cycle non spécifié")
        }
        
        # Cycle lunaire (basé sur le jour du mois)
        day = date_analysis['jour']
        lunar_phase = (day % 28) + 1  # 1-28
        lunar_position = ""
        if 1 <= lunar_phase <= 7:
            lunar_position = "Premier quartier"
        elif 8 <= lunar_phase <= 14:
            lunar_position = "Pleine lune"
        elif 15 <= lunar_phase <= 21:
            lunar_position = "Dernier quartier"
        else:
            lunar_position = "Nouvelle lune"
        
        cycles['lunaire'] = {
            'phase': lunar_phase,
            'position': lunar_position,
            'signification': self.cycle_patterns['lunaire'].get(lunar_position, "Cycle non spécifié")
        }
        
        # Cycle saisonnier (basé sur le mois)
        month = date_analysis['mois']
        season = ""
        if 3 <= month <= 5:
            season = "Printemps"
        elif 6 <= month <= 8:
            season = "Été"
        elif 9 <= month <= 11:
            season = "Automne"
        else:
            season = "Hiver"
        
        cycles['saison'] = {
            'nom': season,
            'signification': self.cycle_patterns['saison'].get(season, "Cycle non spécifié")
        }
        
        return cycles
    
    def analyze_team_cycle(self, team_name, date_str):
        """
        Analyse le cycle numérique d'une équipe à une date donnée.
        
        Args:
            team_name (str): Nom de l'équipe
            date_str (str): Date du match
            
        Returns:
            dict: Analyse du cycle de l'équipe
        """
        team_values = self.gematria_oracle.analyze_name(team_name)
        date_analysis = self.gematria_oracle._analyze_date(date_str)
        
        if 'erreur' in date_analysis:
            return {'erreur': date_analysis['erreur']}
        
        # Calculer le cycle personnel de l'équipe (1-9)
        team_cycle = team_values['simple'] % 9 or a9
        
        # Calculer le jour réduit
        day_reduced = date_analysis['jour_réduit']
        
        # Vérifier la résonance entre l'équipe et la date
        resonance = (team_cycle == day_reduced)
        
        return {
            'équipe': team_name,
            'cycle_personnel': team_cycle,
            'signification_cycle': self.cycle_patterns['personnel'].get(team_cycle, "Cycle non spécifié"),
            'jour_réduit': day_reduced,
            'résonance_jour': resonance,
            'interprétation': "Jour favorable pour l'équipe" if resonance else "Pas de résonance particulière avec le jour"
        }
    
    def find_favorable_dates(self, team_name, year, month):
        """
        Identifie les dates favorables pour une équipe dans un mois donné.
        
        Args:
            team_name (str): Nom de l'équipe
            year (int): Année
            month (int): Mois
            
        Returns:
            list: Dates favorables
        """
        import calendar
        from datetime import date
        
        team_values = self.gematria_oracle.analyze_name(team_name)
        
        # Calculer le cycle personnel de l'équipe (1-9)
        team_cycle = team_values['simple'] % 9 or 9
        
        # Calculer le nombre de jours dans le mois
        _, days_in_month = calendar.monthrange(year, month)
        
        favorable_dates = []
        
        for day in range(1, days_in_month + 1):
            # Créer la date
            current_date = date(year, month, day)
            date_str = current_date.strftime("%Y-%m-%d")
            
            # Analyser la date
            date_analysis = self.gematria_oracle._analyze_date(date_str)
            
            # Vérifier la résonance
            day_reduced = date_analysis['jour_réduit']
            if day_reduced == team_cycle:
                favorable_dates.append({
                    'date': date_str,
                    'jour': day,
                    'résonance': "Forte résonance avec le cycle personnel de l'équipe"
                })
        
        return favorable_dates