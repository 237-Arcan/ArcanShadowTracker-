from datetime import datetime
import json

def _handle_pattern_recalibration_event(self, event_data):
    """
    Handle pattern recalibration events from ArcanBrain.
    Use this to track system learning and adjust module parameters as needed.
    
    Args:
        event_data (dict): Data about the pattern recalibration
    """
    # Extract event data
    source = event_data.get('source', '')
    patterns_recalibrated = event_data.get('patterns_recalibrated', 0)
    patterns_strengthened = event_data.get('patterns_strengthened', 0)
    patterns_weakened = event_data.get('patterns_weakened', 0)
    
    # Log the event for monitoring purposes
    if self.meta_systems:
        self.meta_systems.log_event(f"Pattern recalibration from {source}: {patterns_recalibrated} patterns recalibrated")
    
    # Update reflex memory with recalibration metrics
    if not hasattr(self.reflex_memory, 'recalibrations'):
        self.reflex_memory.recalibrations = []
        
    self.reflex_memory.recalibrations.append({
        'timestamp': datetime.now().isoformat(),
        'source': source,
        'patterns_recalibrated': patterns_recalibrated,
        'patterns_strengthened': patterns_strengthened,
        'patterns_weakened': patterns_weakened
    })
    
    # Keep only the most recent recalibration events (max 50)
    if len(self.reflex_memory.recalibrations) > 50:
        self.reflex_memory.recalibrations = self.reflex_memory.recalibrations[-50:]

def _handle_transfer_learning_event(self, event_data):
    """
    Handle transfer learning events from ArcanBrain.
    Track knowledge transfer between different contexts.
    
    Args:
        event_data (dict): Data about the transfer learning process
    """
    # Extract event data
    source = event_data.get('source', '')
    source_context = event_data.get('source_context', {})
    target_context = event_data.get('target_context', {})
    patterns_transferred = event_data.get('patterns_transferred', 0)
    
    # Log the event for monitoring purposes
    if self.meta_systems:
        context_src = json.dumps(source_context)
        context_tgt = json.dumps(target_context)
        self.meta_systems.log_event(
            f"Transfer learning: {patterns_transferred} patterns transferred from {context_src} to {context_tgt}"
        )
    
    # Update reflex memory with transfer learning information
    if not hasattr(self.reflex_memory, 'transfers'):
        self.reflex_memory.transfers = []
        
    self.reflex_memory.transfers.append({
        'timestamp': datetime.now().isoformat(),
        'source': source,
        'source_context': source_context,
        'target_context': target_context,
        'patterns_transferred': patterns_transferred
    })
    
    # Keep only the most recent transfer events (max 50)
    if len(self.reflex_memory.transfers) > 50:
        self.reflex_memory.transfers = self.reflex_memory.transfers[-50:]