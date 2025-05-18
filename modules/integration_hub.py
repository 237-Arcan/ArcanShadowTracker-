"""
IntegrationHub - Module de connexion entre les nouveaux modules et l'architecture ArcanShadow existante.
Assure la communication harmonieuse entre GematriaOracle, PredictiveForge et les modules existants.
"""
import logging
import os
import json
from datetime import datetime

class IntegrationHub:
    """
    IntegrationHub - Module servant de pont entre les nouvelles technologies (Gematria, XGBoost)
    et l'architecture ArcanShadow existante. Facilite l'enrichissement des analyses via une
    intégration transparente et bidirectionnelle.
    """
    
    def __init__(self, meta_systems=None):
        """
        Initialise le module IntegrationHub.
        
        Args:
            meta_systems: Référence au module MetaSystems pour l'intégration
        """
        self.meta_systems = meta_systems
        self.modules = {}
        self.connection_status = {}
        self.integration_logs = []
        
        # Configurer le logging
        self._setup_logging()
        
        # Enregistrer les gestionnaires d'événements
        self._register_events()
        
        self.logger.info("Module IntegrationHub initialisé")
    
    def _setup_logging(self):
        """Configure le système de logging."""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, "integration_hub.log")
        
        # Configurer le logger
        self.logger = logging.getLogger("IntegrationHub")
        self.logger.setLevel(logging.INFO)
        
        # Configurer les handlers
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Ajouter les handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def register_module(self, module_name, module_instance):
        """
        Enregistre un module pour l'intégration.
        
        Args:
            module_name (str): Nom du module
            module_instance: Instance du module
            
        Returns:
            bool: True si l'enregistrement a réussi, False sinon
        """
        if module_name in self.modules:
            self.logger.warning(f"Le module {module_name} est déjà enregistré")
            return False
        
        self.modules[module_name] = module_instance
        self.connection_status[module_name] = True
        
        self.logger.info(f"Module {module_name} enregistré avec succès")
        
        # Journaliser l'événement
        self._log_integration_event(
            "module_registration", 
            {"module": module_name, "status": "success"}
        )
        
        return True
    
    def unregister_module(self, module_name):
        """
        Désenregistre un module.
        
        Args:
            module_name (str): Nom du module
            
        Returns:
            bool: True si le désenregistrement a réussi, False sinon
        """
        if module_name not in self.modules:
            self.logger.warning(f"Le module {module_name} n'est pas enregistré")
            return False
        
        del self.modules[module_name]
        del self.connection_status[module_name]
        
        self.logger.info(f"Module {module_name} désenregistré avec succès")
        
        # Journaliser l'événement
        self._log_integration_event(
            "module_unregistration", 
            {"module": module_name, "status": "success"}
        )
        
        return True
    
    def get_module(self, module_name):
        """
        Récupère un module enregistré.
        
        Args:
            module_name (str): Nom du module
            
        Returns:
            object: Instance du module, None si non trouvé
        """
        return self.modules.get(module_name)
    
    def enrich_arcan_brain_analysis(self, analysis_result):
        """
        Enrichit les résultats d'analyse d'ArcanBrain avec les insights de GematriaOracle et PredictiveForge.
        
        Args:
            analysis_result (dict): Résultats d'analyse d'ArcanBrain
            
        Returns:
            dict: Résultats d'analyse enrichis
        """
        if not analysis_result or not isinstance(analysis_result, dict):
            self.logger.error("Résultats d'analyse invalides")
            return analysis_result
        
        self.logger.info("Enrichissement des résultats d'analyse d'ArcanBrain")
        
        # Copier les résultats pour éviter de modifier l'original
        enriched_result = analysis_result.copy()
        
        # Enrichir avec GematriaOracle
        if "GematriaOracle" in self.modules and self.connection_status.get("GematriaOracle", False):
            try:
                gematria_oracle = self.modules["GematriaOracle"]
                enriched_result = gematria_oracle.integrate_with_arcan_brain(enriched_result)
                
                self._log_integration_event(
                    "enrichment", 
                    {"module": "GematriaOracle", "status": "success"}
                )
            except Exception as e:
                self.logger.error(f"Erreur lors de l'enrichissement avec GematriaOracle: {e}")
                self._log_integration_event(
                    "enrichment", 
                    {"module": "GematriaOracle", "status": "error", "message": str(e)}
                )
        
        # Enrichir avec PredictiveForge
        if "PredictiveForge" in self.modules and self.connection_status.get("PredictiveForge", False):
            try:
                predictive_forge = self.modules["PredictiveForge"]
                enriched_result = predictive_forge.integrate_with_arcan_brain(enriched_result)
                
                self._log_integration_event(
                    "enrichment", 
                    {"module": "PredictiveForge", "status": "success"}
                )
            except Exception as e:
                self.logger.error(f"Erreur lors de l'enrichissement avec PredictiveForge: {e}")
                self._log_integration_event(
                    "enrichment", 
                    {"module": "PredictiveForge", "status": "error", "message": str(e)}
                )
        
        # Vérifier si des enrichissements ont été ajoutés
        if "additional_analyses" in enriched_result:
            # Calculer un score de confiance composite
            self._calculate_composite_confidence(enriched_result)
        
        return enriched_result
    
    def _calculate_composite_confidence(self, result):
        """
        Calcule un score de confiance composite basé sur les analyses des différents modules.
        
        Args:
            result (dict): Résultats d'analyse
        """
        if "additional_analyses" not in result:
            return
        
        confidence_scores = []
        
        # Confiance d'ArcanBrain
        if "confidence" in result:
            confidence_scores.append(result["confidence"])
        
        # Confiance de GematriaOracle
        if "gematria" in result.get("additional_analyses", {}):
            gematria_analysis = result["additional_analyses"]["gematria"]
            if "insights" in gematria_analysis and "avantage_numérique" in gematria_analysis["insights"]:
                # Extraire la valeur numérique de l'avantage
                advantage_text = gematria_analysis["insights"]["avantage_numérique"]
                try:
                    # Chercher la valeur entre parenthèses
                    import re
                    match = re.search(r"\(([^)]+)%\)", advantage_text)
                    if match:
                        advantage = float(match.group(1)) / 100
                        confidence_scores.append(0.5 + (advantage / 2))  # Normaliser entre 0.5 et 1
                except Exception:
                    pass
        
        # Confiance de PredictiveForge
        if "xgboost" in result.get("additional_analyses", {}):
            xgboost_analysis = result["additional_analyses"]["xgboost"]
            if "match_result" in xgboost_analysis and "confidence" in xgboost_analysis["match_result"]:
                confidence_scores.append(xgboost_analysis["match_result"]["confidence"])
        
        # Calculer la moyenne pondérée des scores de confiance
        if confidence_scores:
            # Pondérations: ArcanBrain (0.5), GematriaOracle (0.2), PredictiveForge (0.3)
            weights = [0.5, 0.2, 0.3]
            
            # Ajuster les poids si certains scores sont manquants
            if len(confidence_scores) < len(weights):
                weights = weights[:len(confidence_scores)]
                weights = [w / sum(weights) for w in weights]  # Normaliser
            
            # Calculer la moyenne pondérée
            composite_confidence = sum(s * w for s, w in zip(confidence_scores, weights))
            
            # Ajouter le score composite aux résultats
            result["composite_confidence"] = composite_confidence
    
    def enrich_numeric_analysis(self, numeri_code_results):
        """
        Enrichit les résultats de NumeriCode avec les insights de GematriaOracle.
        
        Args:
            numeri_code_results (dict): Résultats de NumeriCode
            
        Returns:
            dict: Résultats enrichis
        """
        if not numeri_code_results or not isinstance(numeri_code_results, dict):
            self.logger.error("Résultats de NumeriCode invalides")
            return numeri_code_results
        
        self.logger.info("Enrichissement des résultats de NumeriCode")
        
        # Enrichir avec GematriaOracle
        if "GematriaOracle" in self.modules and self.connection_status.get("GematriaOracle", False):
            try:
                gematria_oracle = self.modules["GematriaOracle"]
                enriched_result = gematria_oracle.integrate_with_numerics(numeri_code_results)
                
                self._log_integration_event(
                    "enrichment", 
                    {"module": "NumeriCode", "target": "GematriaOracle", "status": "success"}
                )
                
                return enriched_result
            except Exception as e:
                self.logger.error(f"Erreur lors de l'enrichissement de NumeriCode avec GematriaOracle: {e}")
                self._log_integration_event(
                    "enrichment", 
                    {"module": "NumeriCode", "target": "GematriaOracle", "status": "error", "message": str(e)}
                )
        
        return numeri_code_results
    
    def enhance_score_analysis(self, score_matrix_results):
        """
        Améliore l'analyse de ScoreMatrix avec les prédictions de PredictiveForge.
        
        Args:
            score_matrix_results (dict): Résultats de ScoreMatrix
            
        Returns:
            dict: Résultats améliorés
        """
        if not score_matrix_results or not isinstance(score_matrix_results, dict):
            self.logger.error("Résultats de ScoreMatrix invalides")
            return score_matrix_results
        
        self.logger.info("Amélioration des résultats de ScoreMatrix")
        
        # Enrichir avec PredictiveForge
        if "PredictiveForge" in self.modules and self.connection_status.get("PredictiveForge", False):
            try:
                predictive_forge = self.modules["PredictiveForge"]
                
                # Vérifier si le modèle de prédiction de score est disponible
                if hasattr(predictive_forge, "score_predictor") and "score_prediction_model" in predictive_forge.score_predictor.score_models:
                    # Extraire les informations du match
                    match_data = score_matrix_results.get("match_data", {})
                    
                    if match_data:
                        # Prédire le score
                        score_prediction = predictive_forge.predict_match_score(match_data)
                        
                        # Enrichir les résultats
                        enriched_results = score_matrix_results.copy()
                        enriched_results["xgboost_prediction"] = score_prediction
                        
                        # Calculer la compatibilité entre les analyses
                        if "score_patterns" in score_matrix_results and "predicted_score" in score_prediction:
                            compatibility = self._calculate_score_compatibility(
                                score_matrix_results["score_patterns"],
                                score_prediction["predicted_score"]
                            )
                            enriched_results["compatibility_index"] = compatibility
                        
                        self._log_integration_event(
                            "enrichment", 
                            {"module": "ScoreMatrix", "target": "PredictiveForge", "status": "success"}
                        )
                        
                        return enriched_results
            except Exception as e:
                self.logger.error(f"Erreur lors de l'amélioration de ScoreMatrix avec PredictiveForge: {e}")
                self._log_integration_event(
                    "enrichment", 
                    {"module": "ScoreMatrix", "target": "PredictiveForge", "status": "error", "message": str(e)}
                )
        
        return score_matrix_results
    
    def _calculate_score_compatibility(self, score_patterns, predicted_score):
        """
        Calcule la compatibilité entre les patterns de score et la prédiction.
        
        Args:
            score_patterns (dict): Patterns de score
            predicted_score (str): Score prédit au format "X-Y"
            
        Returns:
            float: Indice de compatibilité (0-1)
        """
        if not score_patterns or not predicted_score:
            return 0.5
        
        try:
            # Extraire les scores
            home_score, away_score = map(int, predicted_score.split("-"))
            
            # Vérifier les patterns pertinents
            compatibility_factors = []
            
            # Pattern de distribution
            if "distribution" in score_patterns:
                distribution = score_patterns["distribution"]
                if predicted_score in distribution:
                    frequency = distribution[predicted_score]
                    normalized_freq = min(frequency / 0.1, 1.0)  # Normaliser, max 1.0
                    compatibility_factors.append(normalized_freq)
            
            # Pattern de timing
            if "timing" in score_patterns:
                timing = score_patterns["timing"]
                if "scoring_tendency" in timing:
                    tendency = timing["scoring_tendency"]
                    if "early_goals" in tendency and tendency["early_goals"] > 0.6:
                        compatibility_factors.append(0.8)  # Compatible avec des scores plus élevés
                    elif "late_goals" in tendency and tendency["late_goals"] > 0.6:
                        compatibility_factors.append(0.6)  # Compatibilité moyenne
            
            # Pattern de séquence
            if "sequences" in score_patterns:
                sequences = score_patterns["sequences"]
                if "common_flows" in sequences:
                    flows = sequences["common_flows"]
                    if f"{home_score}-{away_score}" in flows:
                        compatibility_factors.append(0.9)
            
            # Calculer la compatibilité moyenne
            if compatibility_factors:
                return sum(compatibility_factors) / len(compatibility_factors)
            
            return 0.5  # Compatibilité moyenne par défaut
        except Exception:
            return 0.5
    
    def _register_events(self):
        """Enregistre les gestionnaires d'événements avec MetaSystems."""
        if self.meta_systems:
            self.meta_systems.register_event_handler("match_analysis_complete", self._handle_match_analysis_complete)
            self.meta_systems.register_event_handler("numeric_analysis_complete", self._handle_numeric_analysis_complete)
            self.meta_systems.register_event_handler("score_matrix_complete", self._handle_score_matrix_complete)
    
    def _handle_match_analysis_complete(self, event_data):
        """
        Gestionnaire d'événement pour les analyses de match complètes.
        
        Args:
            event_data (dict): Données de l'événement
        """
        if "analysis_result" not in event_data:
            self.logger.error("Résultats d'analyse manquants dans l'événement")
            return
        
        analysis_result = event_data["analysis_result"]
        
        # Enrichir les résultats
        enriched_result = self.enrich_arcan_brain_analysis(analysis_result)
        
        # Transmettre les résultats enrichis
        if self.meta_systems:
            self.meta_systems.trigger_event("enriched_analysis_complete", {
                "match_id": event_data.get("match_id"),
                "analysis_result": enriched_result,
                "source": "IntegrationHub",
                "timestamp": datetime.now().isoformat()
            })
    
    def _handle_numeric_analysis_complete(self, event_data):
        """
        Gestionnaire d'événement pour les analyses numériques complètes.
        
        Args:
            event_data (dict): Données de l'événement
        """
        if "numeri_code_results" not in event_data:
            self.logger.error("Résultats de NumeriCode manquants dans l'événement")
            return
        
        numeri_code_results = event_data["numeri_code_results"]
        
        # Enrichir les résultats
        enriched_result = self.enrich_numeric_analysis(numeri_code_results)
        
        # Transmettre les résultats enrichis
        if self.meta_systems:
            self.meta_systems.trigger_event("enriched_numeric_analysis_complete", {
                "match_id": event_data.get("match_id"),
                "numeri_code_results": enriched_result,
                "source": "IntegrationHub",
                "timestamp": datetime.now().isoformat()
            })
    
    def _handle_score_matrix_complete(self, event_data):
        """
        Gestionnaire d'événement pour les analyses de matrice de score complètes.
        
        Args:
            event_data (dict): Données de l'événement
        """
        if "score_matrix_results" not in event_data:
            self.logger.error("Résultats de ScoreMatrix manquants dans l'événement")
            return
        
        score_matrix_results = event_data["score_matrix_results"]
        
        # Améliorer les résultats
        enhanced_result = self.enhance_score_analysis(score_matrix_results)
        
        # Transmettre les résultats améliorés
        if self.meta_systems:
            self.meta_systems.trigger_event("enhanced_score_matrix_complete", {
                "match_id": event_data.get("match_id"),
                "score_matrix_results": enhanced_result,
                "source": "IntegrationHub",
                "timestamp": datetime.now().isoformat()
            })
    
    def _log_integration_event(self, event_type, event_data):
        """
        Journalise un événement d'intégration.
        
        Args:
            event_type (str): Type d'événement
            event_data (dict): Données de l'événement
        """
        event = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": event_data
        }
        
        self.integration_logs.append(event)
        
        # Limiter la taille du journal
        if len(self.integration_logs) > 1000:
            self.integration_logs = self.integration_logs[-1000:]
    
    def get_integration_logs(self, event_type=None, limit=50):
        """
        Récupère les journaux d'intégration.
        
        Args:
            event_type (str, optional): Type d'événement à filtrer
            limit (int): Nombre maximum d'événements à retourner
            
        Returns:
            list: Événements d'intégration
        """
        if event_type:
            filtered_logs = [log for log in self.integration_logs if log["type"] == event_type]
            return filtered_logs[-limit:]
        
        return self.integration_logs[-limit:]
    
    def get_connection_status(self):
        """
        Récupère l'état des connexions avec les modules.
        
        Returns:
            dict: État des connexions
        """
        return self.connection_status.copy()
    
    def test_connections(self):
        """
        Teste les connexions avec tous les modules enregistrés.
        
        Returns:
            dict: Résultats des tests
        """
        results = {}
        
        for module_name, module in self.modules.items():
            try:
                # Vérifier si le module a une méthode de test
                if hasattr(module, "test_connection") and callable(module.test_connection):
                    status = module.test_connection()
                else:
                    # Essayer d'accéder à un attribut pour vérifier que le module est fonctionnel
                    # Cela dépendra de l'implémentation spécifique de chaque module
                    if hasattr(module, "logger"):
                        _ = module.logger
                        status = True
                    else:
                        status = bool(module)
                
                self.connection_status[module_name] = status
                results[module_name] = status
            except Exception as e:
                self.logger.error(f"Erreur lors du test de connexion avec {module_name}: {e}")
                self.connection_status[module_name] = False
                results[module_name] = False
        
        return results
    
    def generate_integration_report(self):
        """
        Génère un rapport sur l'état de l'intégration.
        
        Returns:
            dict: Rapport d'intégration
        """
        # Tester les connexions
        self.test_connections()
        
        # Compter les événements par type
        event_counts = {}
        for event in self.integration_logs:
            event_type = event["type"]
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        # Compter les succès et erreurs d'enrichissement
        enrichment_success = 0
        enrichment_errors = 0
        
        for event in self.integration_logs:
            if event["type"] == "enrichment":
                if event["data"].get("status") == "success":
                    enrichment_success += 1
                elif event["data"].get("status") == "error":
                    enrichment_errors += 1
        
        # Générer le rapport
        report = {
            "timestamp": datetime.now().isoformat(),
            "module_status": self.connection_status,
            "modules_registered": len(self.modules),
            "modules_connected": sum(1 for status in self.connection_status.values() if status),
            "event_counts": event_counts,
            "enrichment_stats": {
                "success": enrichment_success,
                "errors": enrichment_errors,
                "success_rate": enrichment_success / (enrichment_success + enrichment_errors) if (enrichment_success + enrichment_errors) > 0 else 0
            },
            "recent_events": self.get_integration_logs(limit=10)
        }
        
        return report