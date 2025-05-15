"""
LearningSystem - Module d'apprentissage avancé pour ArcanShadow.
Fournit des capacités de recalibration des patterns et d'apprentissage par transfert.
"""

import json
from datetime import datetime

class LearningSystem:
    """
    LearningSystem - Système d'apprentissage avancé pour ArcanShadow.
    Gère les processus d'apprentissage entre modules et les mécanismes de transfert.
    """
    
    def __init__(self, meta_systems=None, arcan_brain=None):
        """
        Initialise le système d'apprentissage avec des références aux autres composants.
        
        Args:
            meta_systems: Référence au module MetaSystems pour l'intégration
            arcan_brain: Référence au module ArcanBrain pour les interactions
        """
        self.meta_systems = meta_systems
        self.arcan_brain = arcan_brain
        self.learning_memory = LearningMemory()
        
        # Enregistrement des gestionnaires d'événements si MetaSystems est disponible
        if meta_systems:
            self._register_event_handlers()
            
    def _register_event_handlers(self):
        """Enregistre les gestionnaires d'événements auprès du système d'événements."""
        # Événements de recalibration de patterns
        self.meta_systems.register_event_handler(
            'patterns_recalibrated',
            self.handle_pattern_recalibration_event,
            'LearningSystem'
        )
        
        # Événements d'apprentissage par transfert
        self.meta_systems.register_event_handler(
            'transfer_learning_applied',
            self.handle_transfer_learning_event,
            'LearningSystem'
        )
    
    def handle_pattern_recalibration_event(self, event_data):
        """
        Gère les événements de recalibration de patterns provenant d'ArcanBrain.
        Utilise ces données pour ajuster les paramètres du module selon les besoins.
        
        Args:
            event_data (dict): Données sur la recalibration des patterns
        """
        # Extraction des données de l'événement
        source = event_data.get('source', '')
        patterns_recalibrated = event_data.get('patterns_recalibrated', 0)
        patterns_strengthened = event_data.get('patterns_strengthened', 0)
        patterns_weakened = event_data.get('patterns_weakened', 0)
        
        # Journalisation de l'événement
        if self.meta_systems:
            self.meta_systems.log_event(f"Pattern recalibration from {source}: {patterns_recalibrated} patterns recalibrated")
        
        # Mise à jour de la mémoire d'apprentissage
        self.learning_memory.record_recalibration({
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'patterns_recalibrated': patterns_recalibrated,
            'patterns_strengthened': patterns_strengthened,
            'patterns_weakened': patterns_weakened
        })
        
        # Si ArcanBrain est disponible, nous pouvons analyser les patterns recalibrés
        # et potentiellement proposer des ajustements supplémentaires
        if self.arcan_brain:
            # Logique future pour optimiser les recalibrations
            pass
    
    def handle_transfer_learning_event(self, event_data):
        """
        Gère les événements d'apprentissage par transfert d'ArcanBrain.
        Suit les transferts de connaissances entre différents contextes.
        
        Args:
            event_data (dict): Données sur le processus d'apprentissage par transfert
        """
        # Extraction des données de l'événement
        source = event_data.get('source', '')
        source_context = event_data.get('source_context', {})
        target_context = event_data.get('target_context', {})
        patterns_transferred = event_data.get('patterns_transferred', 0)
        
        # Journalisation de l'événement
        if self.meta_systems:
            context_src = json.dumps(source_context)
            context_tgt = json.dumps(target_context)
            self.meta_systems.log_event(
                f"Transfer learning: {patterns_transferred} patterns transferred from {context_src} to {context_tgt}"
            )
        
        # Mise à jour de la mémoire d'apprentissage
        self.learning_memory.record_transfer({
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'source_context': source_context,
            'target_context': target_context,
            'patterns_transferred': patterns_transferred
        })
        
        # Si ArcanBrain est disponible, nous pouvons suggérer de nouveaux transferts
        # ou évaluer l'efficacité des transferts précédents
        if self.arcan_brain:
            # Logique future pour optimiser les transferts
            pass
    
    def suggest_transfer_contexts(self, source_context, similarity_threshold=0.6):
        """
        Suggère des contextes cibles potentiels pour l'apprentissage par transfert.
        
        Args:
            source_context (dict): Contexte source avec des patterns à transférer
            similarity_threshold (float): Seuil de similarité minimum
            
        Returns:
            list: Liste des contextes cibles recommandés
        """
        # Cette méthode sera implémentée dans une version future
        # Elle analysera les contextes disponibles et recommandera des cibles
        # pour l'apprentissage par transfert
        return []
    
    def evaluate_learning_efficacy(self):
        """
        Évalue l'efficacité globale du système d'apprentissage.
        
        Returns:
            dict: Métriques d'efficacité
        """
        # Cette méthode sera implémentée dans une version future
        # Elle analysera l'historique des recalibrations et transferts
        # pour évaluer leur impact sur les performances de prédiction
        return {
            'recalibration_efficacy': 0.0,
            'transfer_learning_efficacy': 0.0,
            'learning_system_health': 0.0
        }
        
    def get_learning_history(self, event_type=None, limit=50):
        """
        Récupère l'historique des événements d'apprentissage.
        
        Args:
            event_type (str, optional): Type d'événement ('recalibration' ou 'transfer')
            limit (int): Nombre maximum d'événements à retourner
            
        Returns:
            list: Historique des événements d'apprentissage
        """
        if event_type == 'recalibration':
            return self.learning_memory.get_recalibrations(limit)
        elif event_type == 'transfer':
            return self.learning_memory.get_transfers(limit)
        else:
            # Fusion des deux types d'événements, triés par date
            combined = []
            for recal in self.learning_memory.get_recalibrations(limit):
                recal['event_type'] = 'recalibration'
                combined.append(recal)
                
            for transfer in self.learning_memory.get_transfers(limit):
                transfer['event_type'] = 'transfer'
                combined.append(transfer)
                
            # Tri par timestamp (du plus récent au plus ancien)
            combined.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return combined[:limit]


class LearningMemory:
    """Classe pour stocker l'historique des événements d'apprentissage."""
    
    def __init__(self):
        self.recalibrations = []
        self.transfers = []
        self.max_history = 50
    
    def record_recalibration(self, recalibration_data):
        """Enregistre un événement de recalibration."""
        self.recalibrations.append(recalibration_data)
        
        # Limite à max_history événements
        if len(self.recalibrations) > self.max_history:
            self.recalibrations = self.recalibrations[-self.max_history:]
    
    def record_transfer(self, transfer_data):
        """Enregistre un événement d'apprentissage par transfert."""
        self.transfers.append(transfer_data)
        
        # Limite à max_history événements
        if len(self.transfers) > self.max_history:
            self.transfers = self.transfers[-self.max_history:]
    
    def get_recalibrations(self, limit=None):
        """Récupère l'historique des recalibrations."""
        if limit:
            return self.recalibrations[-limit:]
        return self.recalibrations
    
    def get_transfers(self, limit=None):
        """Récupère l'historique des transferts."""
        if limit:
            return self.transfers[-limit:]
        return self.transfers