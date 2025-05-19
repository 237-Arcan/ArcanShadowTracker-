"""
Module de gestion du temps pour le hub d'intégration central d'ArcanShadow.
Fournit des fonctionnalités avancées de programmation des matchs et 
de calcul des fenêtres temporelles pour tous les modules de l'application.
"""

import logging
import pytz
from datetime import datetime, timedelta, time
import calendar
from typing import List, Dict, Optional, Tuple, Union

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TimeWindow:
    """Classe représentant une fenêtre temporelle utilisée pour les matchs"""
    
    def __init__(self, start_time: datetime, end_time: datetime, category: str = "standard"):
        """
        Initialise une fenêtre temporelle
        
        Args:
            start_time: Heure de début
            end_time: Heure de fin
            category: Catégorie de la fenêtre (standard, prime_time, late_night, etc.)
        """
        self.start_time = start_time
        self.end_time = end_time
        self.category = category
        self.duration_minutes = int((end_time - start_time).total_seconds() / 60)
    
    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')} ({self.category})"
    
    def contains(self, dt: datetime) -> bool:
        """Vérifie si la date donnée est dans cette fenêtre temporelle"""
        if not isinstance(dt, datetime):
            return False
        return self.start_time <= dt <= self.end_time
    
    def to_dict(self) -> Dict:
        """Convertit l'objet en dictionnaire"""
        return {
            "start": self.start_time.isoformat(),
            "end": self.end_time.isoformat(),
            "category": self.category,
            "duration_minutes": self.duration_minutes
        }


class TimeModule:
    """
    Module de gestion du temps pour ArcanShadow.
    Fournit des fonctionnalités avancées pour la programmation des matchs et
    le calcul des fenêtres temporelles pour tous les modules de l'application.
    """
    
    def __init__(self, timezone: str = "Europe/Paris"):
        """
        Initialise le module de temps
        
        Args:
            timezone: Fuseau horaire par défaut (format pytz)
        """
        self.timezone = pytz.timezone(timezone)
        self.current_time = datetime.now(self.timezone)
        logger.info(f"Module de temps initialisé avec le fuseau horaire {timezone}")
        
        # Définir les fenêtres temporelles standard pour les matchs de football
        self._initialize_standard_time_windows()
        
        # Mémoriser les préférences de l'utilisateur
        self.user_preferences = {
            "preferred_timezone": timezone,
            "display_format": "24h",  # ou "12h"
            "favorite_time_slots": []
        }
    
    def _initialize_standard_time_windows(self):
        """Initialise les fenêtres temporelles standard pour les matchs de football"""
        # Structure: jour de la semaine -> liste de fenêtres temporelles
        # 0 = lundi, 6 = dimanche
        base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        self.standard_time_windows = {
            # Lundi à Jeudi: soirées principalement
            0: [
                TimeWindow(base_date.replace(hour=18, minute=45), base_date.replace(hour=20, minute=45), "evening_early"),
                TimeWindow(base_date.replace(hour=20, minute=45), base_date.replace(hour=22, minute=45), "evening_late")
            ],
            1: [
                TimeWindow(base_date.replace(hour=18, minute=45), base_date.replace(hour=20, minute=45), "evening_early"),
                TimeWindow(base_date.replace(hour=20, minute=45), base_date.replace(hour=22, minute=45), "evening_late")
            ],
            2: [
                TimeWindow(base_date.replace(hour=18, minute=45), base_date.replace(hour=20, minute=45), "evening_early"),
                TimeWindow(base_date.replace(hour=20, minute=45), base_date.replace(hour=22, minute=45), "evening_late")
            ],
            3: [
                TimeWindow(base_date.replace(hour=18, minute=45), base_date.replace(hour=20, minute=45), "evening_early"),
                TimeWindow(base_date.replace(hour=20, minute=45), base_date.replace(hour=22, minute=45), "evening_late")
            ],
            # Vendredi: soir et nuit
            4: [
                TimeWindow(base_date.replace(hour=19, minute=0), base_date.replace(hour=21, minute=0), "evening_prime"),
                TimeWindow(base_date.replace(hour=21, minute=0), base_date.replace(hour=23, minute=0), "evening_late")
            ],
            # Samedi: toute la journée
            5: [
                TimeWindow(base_date.replace(hour=13, minute=30), base_date.replace(hour=15, minute=30), "afternoon_early"),
                TimeWindow(base_date.replace(hour=15, minute=30), base_date.replace(hour=17, minute=30), "afternoon_late"),
                TimeWindow(base_date.replace(hour=18, minute=0), base_date.replace(hour=20, minute=0), "evening_early"),
                TimeWindow(base_date.replace(hour=20, minute=0), base_date.replace(hour=22, minute=0), "evening_prime")
            ],
            # Dimanche: toute la journée
            6: [
                TimeWindow(base_date.replace(hour=13, minute=0), base_date.replace(hour=15, minute=0), "afternoon_early"),
                TimeWindow(base_date.replace(hour=15, minute=0), base_date.replace(hour=17, minute=0), "afternoon_late"),
                TimeWindow(base_date.replace(hour=17, minute=0), base_date.replace(hour=19, minute=0), "evening_early"),
                TimeWindow(base_date.replace(hour=20, minute=45), base_date.replace(hour=22, minute=45), "evening_late")
            ]
        }
        
        # Créer un dictionnaire des fenêtres pour un accès rapide par catégorie
        self.time_windows_by_category = {}
        for day, windows in self.standard_time_windows.items():
            for window in windows:
                if window.category not in self.time_windows_by_category:
                    self.time_windows_by_category[window.category] = []
                self.time_windows_by_category[window.category].append((day, window))
    
    def update_current_time(self):
        """Met à jour l'heure actuelle"""
        self.current_time = datetime.now(self.timezone)
        return self.current_time
    
    def set_timezone(self, timezone: str):
        """
        Change le fuseau horaire du module
        
        Args:
            timezone: Nouveau fuseau horaire (format pytz)
        """
        try:
            self.timezone = pytz.timezone(timezone)
            self.user_preferences["preferred_timezone"] = timezone
            self.update_current_time()
            logger.info(f"Fuseau horaire changé pour {timezone}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors du changement de fuseau horaire: {e}")
            return False
    
    def get_match_time_window(self, match_datetime: datetime) -> Optional[TimeWindow]:
        """
        Détermine la fenêtre temporelle d'un match
        
        Args:
            match_datetime: Date et heure du match
            
        Returns:
            TimeWindow ou None si aucune fenêtre ne correspond
        """
        if not isinstance(match_datetime, datetime):
            try:
                match_datetime = datetime.fromisoformat(match_datetime.replace('Z', '+00:00'))
            except:
                logger.error(f"Format de date invalide: {match_datetime}")
                return None
        
        # S'assurer que la date est dans le bon fuseau horaire
        if match_datetime.tzinfo is None:
            match_datetime = self.timezone.localize(match_datetime)
        elif match_datetime.tzinfo != self.timezone:
            match_datetime = match_datetime.astimezone(self.timezone)
        
        # Obtenir le jour de la semaine (0 = lundi, 6 = dimanche)
        weekday = match_datetime.weekday()
        
        # Vérifier chaque fenêtre temporelle pour ce jour
        if weekday in self.standard_time_windows:
            match_time = match_datetime.time()
            for window in self.standard_time_windows[weekday]:
                window_start_time = window.start_time.time()
                window_end_time = window.end_time.time()
                
                if window_start_time <= match_time <= window_end_time:
                    return window
        
        return None
    
    def format_match_time(self, match_datetime: Union[datetime, str], format_type: str = None) -> str:
        """
        Formate l'heure d'un match selon les préférences
        
        Args:
            match_datetime: Date et heure du match
            format_type: Type de format (None = utiliser les préférences utilisateur)
            
        Returns:
            Chaîne formatée de l'heure du match
        """
        if format_type is None:
            format_type = self.user_preferences["display_format"]
        
        # Convertir en datetime si nécessaire
        if isinstance(match_datetime, str):
            try:
                match_datetime = datetime.fromisoformat(match_datetime.replace('Z', '+00:00'))
            except:
                return match_datetime  # Retourner la chaîne originale en cas d'erreur
        
        # S'assurer que la date est dans le bon fuseau horaire
        if match_datetime.tzinfo is None:
            match_datetime = self.timezone.localize(match_datetime)
        elif match_datetime.tzinfo != self.timezone:
            match_datetime = match_datetime.astimezone(self.timezone)
        
        # Formater selon les préférences
        if format_type == "12h":
            return match_datetime.strftime("%I:%M %p")
        else:  # 24h par défaut
            return match_datetime.strftime("%H:%M")
    
    def get_day_name(self, date: Union[datetime, str], short: bool = False) -> str:
        """
        Obtient le nom du jour de la semaine
        
        Args:
            date: Date
            short: Si True, retourne la forme abrégée (Lun, Mar, etc.)
            
        Returns:
            Nom du jour
        """
        # Convertir en datetime si nécessaire
        if isinstance(date, str):
            try:
                date = datetime.fromisoformat(date.replace('Z', '+00:00'))
            except:
                return ""
        
        # Tableau des noms de jours en français
        days_fr = [
            ("Lundi", "Lun"), 
            ("Mardi", "Mar"), 
            ("Mercredi", "Mer"), 
            ("Jeudi", "Jeu"), 
            ("Vendredi", "Ven"), 
            ("Samedi", "Sam"), 
            ("Dimanche", "Dim")
        ]
        
        day_idx = date.weekday()
        return days_fr[day_idx][1 if short else 0]
    
    def get_month_name(self, date: Union[datetime, str], short: bool = False) -> str:
        """
        Obtient le nom du mois
        
        Args:
            date: Date
            short: Si True, retourne la forme abrégée (Jan, Fév, etc.)
            
        Returns:
            Nom du mois
        """
        # Convertir en datetime si nécessaire
        if isinstance(date, str):
            try:
                date = datetime.fromisoformat(date.replace('Z', '+00:00'))
            except:
                return ""
        
        # Tableau des noms de mois en français
        months_fr = [
            ("Janvier", "Jan"), 
            ("Février", "Fév"), 
            ("Mars", "Mar"), 
            ("Avril", "Avr"), 
            ("Mai", "Mai"), 
            ("Juin", "Juin"), 
            ("Juillet", "Juil"), 
            ("Août", "Août"), 
            ("Septembre", "Sept"), 
            ("Octobre", "Oct"), 
            ("Novembre", "Nov"), 
            ("Décembre", "Déc")
        ]
        
        month_idx = date.month - 1  # Les mois commencent à 1
        return months_fr[month_idx][1 if short else 0]
    
    def format_match_date(self, match_datetime: Union[datetime, str], format_type: str = "full") -> str:
        """
        Formate la date d'un match selon le format spécifié
        
        Args:
            match_datetime: Date et heure du match
            format_type: Type de format (full, short, day_only, etc.)
            
        Returns:
            Chaîne formatée de la date du match
        """
        # Convertir en datetime si nécessaire
        if isinstance(match_datetime, str):
            try:
                match_datetime = datetime.fromisoformat(match_datetime.replace('Z', '+00:00'))
            except:
                return match_datetime
        
        # S'assurer que la date est dans le bon fuseau horaire
        if match_datetime.tzinfo is None:
            match_datetime = self.timezone.localize(match_datetime)
        elif match_datetime.tzinfo != self.timezone:
            match_datetime = match_datetime.astimezone(self.timezone)
        
        # Vérifier si c'est aujourd'hui, demain ou après-demain
        today = datetime.now(self.timezone).date()
        match_date = match_datetime.date()
        
        if match_date == today:
            day_text = "Aujourd'hui"
        elif match_date == today + timedelta(days=1):
            day_text = "Demain"
        elif match_date == today + timedelta(days=2):
            day_text = "Après-demain"
        else:
            # Utiliser le nom du jour
            day_text = self.get_day_name(match_datetime)
        
        # Formater selon le type demandé
        if format_type == "full":
            return f"{day_text} {match_date.day} {self.get_month_name(match_datetime)}"
        elif format_type == "short":
            return f"{day_text} {match_date.day}/{match_date.month}"
        elif format_type == "day_only":
            return day_text
        elif format_type == "compact":
            if match_date == today or match_date == today + timedelta(days=1):
                return day_text
            else:
                return f"{self.get_day_name(match_datetime, short=True)} {match_date.day}/{match_date.month}"
        else:
            return f"{match_date.day} {self.get_month_name(match_datetime)}"
    
    def get_upcoming_days(self, count: int = 7) -> List[Dict]:
        """
        Génère une liste formatée des prochains jours
        Utile pour les sélecteurs de date dans l'interface
        
        Args:
            count: Nombre de jours à générer
            
        Returns:
            Liste de dictionnaires avec des informations formatées sur chaque jour
        """
        days = []
        today = datetime.now(self.timezone).date()
        
        for i in range(count):
            current_date = today + timedelta(days=i)
            day_name = self.get_day_name(current_date, short=True)
            
            # Déterminer s'il s'agit d'aujourd'hui, demain, etc.
            if i == 0:
                display_name = "Aujourd'hui"
            elif i == 1:
                display_name = "Demain"
            else:
                display_name = day_name
            
            days.append({
                "date": current_date.isoformat(),
                "day": current_date.day,
                "month": current_date.month,
                "month_name": self.get_month_name(current_date, short=True),
                "day_name": day_name,
                "display_name": display_name,
                "is_weekend": current_date.weekday() >= 5,
                "formatted_date": f"{current_date.day} {self.get_month_name(current_date, short=True)}"
            })
        
        return days
    
    def group_matches_by_time_slots(self, matches: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Regroupe les matchs par créneaux horaires
        
        Args:
            matches: Liste de dictionnaires représentant des matchs
            
        Returns:
            Dictionnaire avec les créneaux horaires comme clés et les matchs comme valeurs
        """
        grouped_matches = {}
        
        for match in matches:
            # Obtenir la date/heure du match
            match_datetime = None
            if 'date' in match:
                try:
                    match_datetime = datetime.fromisoformat(match['date'].replace('Z', '+00:00'))
                except:
                    # Essayer un autre format si nécessaire
                    continue
            
            if not match_datetime:
                continue
            
            # Déterminer la fenêtre temporelle
            time_window = self.get_match_time_window(match_datetime)
            time_slot = time_window.category if time_window else "other"
            
            # Ajouter le match au créneau horaire
            if time_slot not in grouped_matches:
                grouped_matches[time_slot] = []
            
            # Ajouter des informations temporelles au match
            match['time_slot'] = time_slot
            match['formatted_time'] = self.format_match_time(match_datetime)
            match['formatted_date'] = self.format_match_date(match_datetime, "compact")
            
            grouped_matches[time_slot].append(match)
        
        return grouped_matches
    
    def get_prime_time_matches(self, matches: List[Dict]) -> List[Dict]:
        """
        Filtre les matchs pour ne garder que ceux en prime time
        
        Args:
            matches: Liste de dictionnaires représentant des matchs
            
        Returns:
            Liste des matchs en prime time
        """
        prime_time_matches = []
        
        for match in matches:
            # Obtenir la date/heure du match
            if 'date' in match:
                try:
                    match_datetime = datetime.fromisoformat(match['date'].replace('Z', '+00:00'))
                    time_window = self.get_match_time_window(match_datetime)
                    
                    if time_window and "prime" in time_window.category:
                        prime_time_matches.append(match)
                except:
                    continue
        
        return prime_time_matches
    
    def get_best_matches_by_day(self, matches: List[Dict], top_n: int = 3) -> Dict[str, List[Dict]]:
        """
        Identifie les meilleurs matchs pour chaque jour
        
        Args:
            matches: Liste de dictionnaires représentant des matchs
            top_n: Nombre de matchs à sélectionner par jour
            
        Returns:
            Dictionnaire avec les dates comme clés et les meilleurs matchs comme valeurs
        """
        # Regrouper par jour
        matches_by_day = {}
        
        for match in matches:
            if 'date' in match:
                try:
                    match_datetime = datetime.fromisoformat(match['date'].replace('Z', '+00:00'))
                    day_str = match_datetime.date().isoformat()
                    
                    if day_str not in matches_by_day:
                        matches_by_day[day_str] = []
                    
                    matches_by_day[day_str].append(match)
                except:
                    continue
        
        # Sélectionner les meilleurs matchs par jour
        # Critères: ligue majeure, prime time, etc.
        best_matches = {}
        major_leagues = [39, 140, 61, 78, 135, 2]  # Premier League, La Liga, etc.
        
        for day, day_matches in matches_by_day.items():
            # Trier les matchs par importance
            sorted_matches = sorted(day_matches, key=lambda m: (
                m.get('league_id') in major_leagues,  # D'abord les ligues majeures
                self.get_match_time_window(m.get('date')) and "prime" in self.get_match_time_window(m.get('date')).category,  # Puis le prime time
                m.get('is_derby', False),  # Puis les derbys
                not m.get('is_value_bet', False)  # Puis les value bets
            ), reverse=True)
            
            best_matches[day] = sorted_matches[:top_n]
        
        return best_matches
    
    def get_time_window_distribution(self, matches: List[Dict]) -> Dict[str, int]:
        """
        Calcule la distribution des matchs par fenêtre temporelle
        
        Args:
            matches: Liste de dictionnaires représentant des matchs
            
        Returns:
            Dictionnaire avec les catégories de fenêtres comme clés et le nombre de matchs comme valeurs
        """
        distribution = {}
        
        for match in matches:
            if 'date' in match:
                try:
                    match_datetime = datetime.fromisoformat(match['date'].replace('Z', '+00:00'))
                    time_window = self.get_match_time_window(match_datetime)
                    
                    if time_window:
                        category = time_window.category
                        distribution[category] = distribution.get(category, 0) + 1
                except:
                    continue
        
        return distribution
    
    def enhance_match_data_with_time_info(self, match: Dict) -> Dict:
        """
        Enrichit les données d'un match avec des informations temporelles
        
        Args:
            match: Dictionnaire représentant un match
            
        Returns:
            Match enrichi avec des informations temporelles
        """
        if 'date' not in match:
            return match
        
        try:
            match_datetime = datetime.fromisoformat(match['date'].replace('Z', '+00:00'))
            
            # Ajouter les informations temporelles
            match['formatted_time'] = self.format_match_time(match_datetime)
            match['formatted_date'] = self.format_match_date(match_datetime)
            match['day_name'] = self.get_day_name(match_datetime)
            match['is_today'] = match_datetime.date() == datetime.now(self.timezone).date()
            match['is_tomorrow'] = match_datetime.date() == (datetime.now(self.timezone).date() + timedelta(days=1))
            
            # Obtenir la fenêtre temporelle
            time_window = self.get_match_time_window(match_datetime)
            if time_window:
                match['time_window'] = time_window.to_dict()
                match['time_slot'] = time_window.category
                match['is_prime_time'] = "prime" in time_window.category
            
            # Ajouter des informations sur l'heure locale
            match['local_time'] = match_datetime.strftime('%H:%M')
            match['timezone'] = str(self.timezone)
            
        except Exception as e:
            logger.error(f"Erreur lors de l'enrichissement des données temporelles: {e}")
        
        return match
    
    def format_countdown(self, target_datetime: Union[datetime, str]) -> str:
        """
        Calcule et formate le compte à rebours jusqu'à une date cible
        
        Args:
            target_datetime: Date et heure cible
            
        Returns:
            Chaîne formatée du compte à rebours
        """
        # Convertir en datetime si nécessaire
        if isinstance(target_datetime, str):
            try:
                target_datetime = datetime.fromisoformat(target_datetime.replace('Z', '+00:00'))
            except:
                return "N/A"
        
        # S'assurer que la date est dans le bon fuseau horaire
        if target_datetime.tzinfo is None:
            target_datetime = self.timezone.localize(target_datetime)
        elif target_datetime.tzinfo != self.timezone:
            target_datetime = target_datetime.astimezone(self.timezone)
        
        # Calculer la différence
        now = datetime.now(self.timezone)
        diff = target_datetime - now
        
        # Si la date est déjà passée
        if diff.total_seconds() < 0:
            return "Terminé"
        
        # Calculer jours, heures, minutes
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        # Formater selon la durée
        if days > 0:
            return f"{days}j {hours}h"
        elif hours > 0:
            return f"{hours}h {minutes}min"
        else:
            return f"{minutes}min"
    
    def get_user_preferences(self) -> Dict:
        """Retourne les préférences temporelles de l'utilisateur"""
        return self.user_preferences
    
    def set_user_preferences(self, preferences: Dict) -> bool:
        """
        Met à jour les préférences temporelles de l'utilisateur
        
        Args:
            preferences: Dictionnaire des préférences
            
        Returns:
            True si la mise à jour a réussi, False sinon
        """
        try:
            # Mettre à jour uniquement les clés existantes
            for key, value in preferences.items():
                if key in self.user_preferences:
                    self.user_preferences[key] = value
            
            # Si le fuseau horaire est changé, mettre à jour l'objet timezone
            if "preferred_timezone" in preferences:
                self.set_timezone(preferences["preferred_timezone"])
                
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour des préférences: {e}")
            return False