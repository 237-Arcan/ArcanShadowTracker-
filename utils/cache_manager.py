"""
CacheManager - Module de gestion de cache pour ArcanShadow
Ce module permet de mettre en cache les données des API et des scrapers
pour réduire les requêtes et améliorer les performances.
"""

import os
import json
import time
import logging
import sqlite3
from datetime import datetime, timedelta
import pickle

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('cache_manager')

class CacheManager:
    """
    Module de gestion de cache pour ArcanShadow.
    Permet de stocker et récupérer des données en cache pour réduire
    les appels API et améliorer les performances.
    """
    def __init__(self, db_path="arcanshadow.db"):
        """
        Initialise le gestionnaire de cache.
        
        Args:
            db_path (str): Chemin vers la base de données SQLite
        """
        self.db_path = db_path
        self._init_db()
        
        # Durations de cache par défaut (en secondes)
        self.default_durations = {
            'sports_api': 30 * 60,  # 30 minutes pour les données de matchs
            'flash_scraper': 60 * 60,  # 1 heure pour les données scrapées
            'odds': 5 * 60,  # 5 minutes pour les cotes
            'match_details': 12 * 60 * 60,  # 12 heures pour les détails de matchs
            'historical': 24 * 60 * 60,  # 24 heures pour les données historiques
            'default': 15 * 60  # 15 minutes par défaut
        }
    
    def _init_db(self):
        """
        Initialise la table de cache dans la base de données.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Créer la table de cache si elle n'existe pas
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS cache (
                cache_key TEXT PRIMARY KEY,
                data BLOB,
                source TEXT,
                expiry INTEGER,
                created_at INTEGER
            )
            ''')
            
            conn.commit()
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de la base de données de cache: {e}")
        finally:
            if conn:
                conn.close()
    
    def get(self, key, source='default'):
        """
        Récupère une donnée du cache.
        
        Args:
            key (str): Clé de cache
            source (str): Source de la donnée (pour le logging)
            
        Returns:
            any: Donnée en cache ou None si non trouvée ou expirée
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Récupérer les données et la date d'expiration
            cursor.execute(
                "SELECT data, expiry FROM cache WHERE cache_key = ?",
                (key,)
            )
            result = cursor.fetchone()
            
            if result:
                data_blob, expiry = result
                
                # Vérifier si les données sont expirées
                if expiry > int(time.time()):
                    try:
                        # Désérialiser les données
                        data = pickle.loads(data_blob)
                        logger.info(f"Données récupérées du cache pour {key} (source: {source})")
                        return data
                    except Exception as e:
                        logger.error(f"Erreur lors de la désérialisation des données: {e}")
                else:
                    logger.info(f"Données expirées dans le cache pour {key} (source: {source})")
                    # Supprimer les données expirées
                    self.invalidate(key)
            
            return None
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des données du cache: {e}")
            return None
            
        finally:
            if conn:
                conn.close()
    
    def set(self, key, data, source='default', duration=None):
        """
        Stocke une donnée dans le cache.
        
        Args:
            key (str): Clé de cache
            data (any): Donnée à mettre en cache
            source (str): Source de la donnée
            duration (int, optional): Durée de validité en secondes
            
        Returns:
            bool: True si réussi, False sinon
        """
        if duration is None:
            duration = self.default_durations.get(source, self.default_durations['default'])
            
        try:
            # Sérialiser les données
            data_blob = pickle.dumps(data)
            
            # Calculer la date d'expiration
            expiry = int(time.time()) + duration
            created_at = int(time.time())
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insérer ou remplacer les données en cache
            cursor.execute(
                "INSERT OR REPLACE INTO cache (cache_key, data, source, expiry, created_at) VALUES (?, ?, ?, ?, ?)",
                (key, data_blob, source, expiry, created_at)
            )
            
            conn.commit()
            logger.info(f"Données mises en cache pour {key} (source: {source}, durée: {duration}s)")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la mise en cache des données: {e}")
            return False
            
        finally:
            if conn:
                conn.close()
    
    def invalidate(self, key):
        """
        Invalide une entrée spécifique du cache.
        
        Args:
            key (str): Clé de cache à invalider
            
        Returns:
            bool: True si réussi, False sinon
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM cache WHERE cache_key = ?", (key,))
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Entrée {key} invalidée dans le cache")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Erreur lors de l'invalidation du cache: {e}")
            return False
            
        finally:
            if conn:
                conn.close()
    
    def clear_expired(self):
        """
        Nettoie les entrées expirées du cache.
        
        Returns:
            int: Nombre d'entrées supprimées
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            current_time = int(time.time())
            cursor.execute("DELETE FROM cache WHERE expiry < ?", (current_time,))
            conn.commit()
            
            deleted_count = cursor.rowcount
            if deleted_count > 0:
                logger.info(f"Suppression de {deleted_count} entrées expirées du cache")
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage du cache: {e}")
            return 0
            
        finally:
            if conn:
                conn.close()
    
    def clear_all(self):
        """
        Efface tout le cache.
        
        Returns:
            bool: True si réussi, False sinon
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM cache")
            conn.commit()
            
            logger.info("Cache entièrement effacé")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'effacement du cache: {e}")
            return False
            
        finally:
            if conn:
                conn.close()
    
    def get_stats(self):
        """
        Récupère des statistiques sur le cache.
        
        Returns:
            dict: Statistiques du cache
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Nombre total d'entrées
            cursor.execute("SELECT COUNT(*) FROM cache")
            total_entries = cursor.fetchone()[0]
            
            # Nombre d'entrées actives
            current_time = int(time.time())
            cursor.execute("SELECT COUNT(*) FROM cache WHERE expiry > ?", (current_time,))
            active_entries = cursor.fetchone()[0]
            
            # Nombre d'entrées expirées
            cursor.execute("SELECT COUNT(*) FROM cache WHERE expiry <= ?", (current_time,))
            expired_entries = cursor.fetchone()[0]
            
            # Taille totale du cache
            cursor.execute("SELECT SUM(LENGTH(data)) FROM cache")
            total_size = cursor.fetchone()[0] or 0
            
            # Statistiques par source
            cursor.execute("SELECT source, COUNT(*) FROM cache GROUP BY source")
            sources = {source: count for source, count in cursor.fetchall()}
            
            return {
                'total_entries': total_entries,
                'active_entries': active_entries,
                'expired_entries': expired_entries,
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'sources': sources
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des statistiques du cache: {e}")
            return {}
            
        finally:
            if conn:
                conn.close()