"""
PredictiveForge - Module d'apprentissage automatique avancé pour ArcanShadow.
Utilise XGBoost comme moteur principal pour générer des prédictions de haute précision.
"""
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import accuracy_score, log_loss, precision_score, recall_score, f1_score
from sklearn.feature_selection import SelectFromModel
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pickle
import os
import logging
import datetime
import json

class PredictiveForge:
    """
    PredictiveForge - Module d'apprentissage automatique avancé utilisant XGBoost.
    Génère des prédictions sportives de haute précision et s'intègre avec les autres modules.
    """
    
    def __init__(self, meta_systems=None, data_path=None):
        """
        Initialise le module PredictiveForge.
        
        Args:
            meta_systems: Référence au module MetaSystems pour l'intégration
            data_path (str, optional): Chemin vers les données d'entraînement
        """
        self.meta_systems = meta_systems
        self.data_path = data_path or "data"
        self.models = {}
        self.feature_importance = {}
        self.encoders = {}
        self.metrics = {
            "accuracy": [],
            "precision": [],
            "recall": [],
            "f1_score": [],
            "log_loss": []
        }
        
        # Initialiser les sous-modules
        self.core_xgboost = CoreXGBoost(self)
        self.feature_engineer = FeatureEngineer(self)
        self.hyper_tuner = HyperTuner(self)
        self.ensemble_director = EnsembleDirector(self)
        self.anomaly_xgboost = AnomalyXGBoost(self)
        self.score_predictor = ScorePredictor(self)
        
        # Créer le répertoire de données s'il n'existe pas
        os.makedirs(self.data_path, exist_ok=True)
        
        # Configurer le logging
        self._setup_logging()
        
        # Charger les modèles existants
        self._load_models()
        
        # Enregistrer les gestionnaires d'événements
        self._register_events()
        
        self.logger.info("Module PredictiveForge initialisé")
    
    def _setup_logging(self):
        """Configure le système de logging."""
        log_dir = os.path.join(self.data_path, "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, "predictive_forge.log")
        
        # Configurer le logger
        self.logger = logging.getLogger("PredictiveForge")
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
    
    def _load_models(self):
        """Charge les modèles existants à partir du disque."""
        models_dir = os.path.join(self.data_path, "models")
        os.makedirs(models_dir, exist_ok=True)
        
        # Parcourir les fichiers de modèles
        for filename in os.listdir(models_dir):
            if filename.endswith(".pkl"):
                model_name = filename.split(".")[0]
                model_path = os.path.join(models_dir, filename)
                
                try:
                    with open(model_path, "rb") as f:
                        self.models[model_name] = pickle.load(f)
                    self.logger.info(f"Modèle chargé: {model_name}")
                except Exception as e:
                    self.logger.error(f"Erreur lors du chargement du modèle {model_name}: {e}")
    
    def _save_model(self, model_name, model):
        """
        Sauvegarde un modèle sur le disque.
        
        Args:
            model_name (str): Nom du modèle
            model: Modèle à sauvegarder
        """
        models_dir = os.path.join(self.data_path, "models")
        os.makedirs(models_dir, exist_ok=True)
        
        model_path = os.path.join(models_dir, f"{model_name}.pkl")
        
        try:
            with open(model_path, "wb") as f:
                pickle.dump(model, f)
            self.logger.info(f"Modèle sauvegardé: {model_name}")
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde du modèle {model_name}: {e}")
    
    def _register_events(self):
        """Enregistre les gestionnaires d'événements avec MetaSystems."""
        if self.meta_systems:
            self.meta_systems.register_event_handler("match_prediction_request", self._handle_prediction_request)
            self.meta_systems.register_event_handler("model_training_request", self._handle_training_request)
            self.meta_systems.register_event_handler("anomaly_detection_request", self._handle_anomaly_detection_request)
    
    def train_match_result_model(self, data, test_size=0.2, model_name="match_result_model"):
        """
        Entraîne un modèle XGBoost pour la prédiction des résultats de match.
        
        Args:
            data (pd.DataFrame): Données d'entraînement
            test_size (float): Proportion des données à utiliser pour le test
            model_name (str): Nom du modèle à entraîner
            
        Returns:
            dict: Métriques d'évaluation du modèle
        """
        self.logger.info(f"Début de l'entraînement du modèle {model_name}")
        
        if data is None or len(data) == 0:
            self.logger.error("Données d'entraînement vides ou invalides")
            return {"error": "Données d'entraînement invalides"}
        
        try:
            # Préparation des données
            processed_data = self.feature_engineer.preprocess_match_data(data)
            
            if processed_data is None:
                self.logger.error("Échec du prétraitement des données")
                return {"error": "Échec du prétraitement des données"}
            
            X = processed_data["features"]
            y = processed_data["target"]
            
            # Diviser en ensembles d'entraînement et de test
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
            
            # Entraîner le modèle avec CoreXGBoost
            model, params = self.core_xgboost.train_model(X_train, y_train, objective="multi:softprob", num_class=3)
            
            # Évaluer le modèle
            y_pred_proba = model.predict_proba(X_test)
            y_pred = np.argmax(y_pred_proba, axis=1)
            
            # Calculer les métriques
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average="weighted")
            recall = recall_score(y_test, y_pred, average="weighted")
            f1 = f1_score(y_test, y_pred, average="weighted")
            loss = log_loss(y_test, y_pred_proba)
            
            # Stocker les métriques
            self.metrics["accuracy"].append(accuracy)
            self.metrics["precision"].append(precision)
            self.metrics["recall"].append(recall)
            self.metrics["f1_score"].append(f1)
            self.metrics["log_loss"].append(loss)
            
            # Stocker l'importance des caractéristiques
            feature_importance = {}
            for i, score in enumerate(model.feature_importances_):
                if hasattr(X, 'columns'):
                    feature_name = X.columns[i]
                else:
                    feature_name = f"feature_{i}"
                feature_importance[feature_name] = float(score)
            
            self.feature_importance[model_name] = feature_importance
            
            # Sauvegarder le modèle
            self.models[model_name] = model
            self._save_model(model_name, model)
            
            # Sauvegarder les encodeurs
            if hasattr(processed_data, "encoders"):
                self.encoders[model_name] = processed_data["encoders"]
                encoder_path = os.path.join(self.data_path, "models", f"{model_name}_encoders.pkl")
                with open(encoder_path, "wb") as f:
                    pickle.dump(processed_data["encoders"], f)
            
            # Résultats
            results = {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "log_loss": loss,
                "model_params": params,
                "feature_importance": feature_importance
            }
            
            self.logger.info(f"Modèle {model_name} entraîné avec succès. Accuracy: {accuracy:.4f}")
            return results
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'entraînement du modèle {model_name}: {e}")
            return {"error": str(e)}
    
    def predict_match_result(self, match_data, model_name="match_result_model"):
        """
        Prédit le résultat d'un match.
        
        Args:
            match_data (dict): Données du match
            model_name (str): Nom du modèle à utiliser
            
        Returns:
            dict: Prédiction du résultat
        """
        self.logger.info(f"Demande de prédiction pour un match avec le modèle {model_name}")
        
        if model_name not in self.models:
            self.logger.error(f"Modèle {model_name} non trouvé")
            return {"error": f"Modèle {model_name} non trouvé"}
        
        try:
            # Convertir en DataFrame si nécessaire
            if isinstance(match_data, dict):
                match_df = pd.DataFrame([match_data])
            else:
                match_df = match_data
            
            # Prétraiter les données
            processed_data = self.feature_engineer.preprocess_match_data(
                match_df, 
                training=False, 
                encoders=self.encoders.get(model_name)
            )
            
            if processed_data is None:
                self.logger.error("Échec du prétraitement des données de match")
                return {"error": "Échec du prétraitement des données"}
            
            X = processed_data["features"]
            
            # Obtenir la prédiction
            model = self.models[model_name]
            y_pred_proba = model.predict_proba(X)
            
            # Préparer les résultats
            result_labels = ["Victoire domicile", "Match nul", "Victoire extérieur"]
            predictions = []
            
            for i, proba in enumerate(y_pred_proba):
                pred_dict = {
                    "probabilities": {
                        result_labels[j]: float(p) for j, p in enumerate(proba)
                    },
                    "predicted_result": result_labels[np.argmax(proba)],
                    "confidence": float(np.max(proba))
                }
                predictions.append(pred_dict)
            
            # Si une seule prédiction, retourner directement
            if len(predictions) == 1:
                result = predictions[0]
                result["match_data"] = match_data if isinstance(match_data, dict) else match_data.iloc[0].to_dict()
                return result
            
            return {"predictions": predictions}
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la prédiction du match: {e}")
            return {"error": str(e)}
    
    def train_score_prediction_model(self, data, test_size=0.2, model_name="score_prediction_model"):
        """
        Entraîne un modèle pour prédire le score exact d'un match.
        
        Args:
            data (pd.DataFrame): Données d'entraînement
            test_size (float): Proportion des données à utiliser pour le test
            model_name (str): Nom du modèle à entraîner
            
        Returns:
            dict: Métriques d'évaluation du modèle
        """
        return self.score_predictor.train_model(data, test_size, model_name)
    
    def predict_match_score(self, match_data, model_name="score_prediction_model"):
        """
        Prédit le score d'un match.
        
        Args:
            match_data (dict): Données du match
            model_name (str): Nom du modèle à utiliser
            
        Returns:
            dict: Prédiction du score
        """
        return self.score_predictor.predict_score(match_data, model_name)
    
    def detect_anomalies(self, match_data, threshold=0.9, model_name="match_result_model"):
        """
        Détecte les anomalies dans les données de match.
        
        Args:
            match_data (pd.DataFrame): Données de match
            threshold (float): Seuil de confiance pour la détection d'anomalies
            model_name (str): Nom du modèle à utiliser
            
        Returns:
            dict: Anomalies détectées
        """
        return self.anomaly_xgboost.detect_anomalies(match_data, threshold, model_name)
    
    def _handle_prediction_request(self, event_data):
        """
        Gestionnaire d'événement pour les demandes de prédiction.
        
        Args:
            event_data (dict): Données de l'événement
        """
        if "match_data" not in event_data:
            self.logger.error("Données de match manquantes dans la demande de prédiction")
            return
        
        match_data = event_data["match_data"]
        model_name = event_data.get("model_name", "match_result_model")
        
        # Effectuer la prédiction
        prediction = self.predict_match_result(match_data, model_name)
        
        # Si demandé, prédire également le score
        if event_data.get("predict_score", False):
            score_prediction = self.predict_match_score(match_data, "score_prediction_model")
            prediction["score_prediction"] = score_prediction
        
        # Envoyer le résultat via le système d'événements
        if self.meta_systems:
            self.meta_systems.trigger_event("match_prediction_complete", {
                "match_id": event_data.get("match_id"),
                "prediction": prediction,
                "model_used": model_name,
                "timestamp": datetime.datetime.now().isoformat()
            })
    
    def _handle_training_request(self, event_data):
        """
        Gestionnaire d'événement pour les demandes d'entraînement.
        
        Args:
            event_data (dict): Données de l'événement
        """
        if "training_data" not in event_data:
            self.logger.error("Données d'entraînement manquantes dans la demande")
            return
        
        training_data = event_data["training_data"]
        model_type = event_data.get("model_type", "match_result")
        model_name = event_data.get("model_name", f"{model_type}_model")
        
        # Effectuer l'entraînement selon le type de modèle
        if model_type == "match_result":
            results = self.train_match_result_model(training_data, model_name=model_name)
        elif model_type == "score_prediction":
            results = self.train_score_prediction_model(training_data, model_name=model_name)
        else:
            self.logger.error(f"Type de modèle non pris en charge: {model_type}")
            results = {"error": f"Type de modèle non pris en charge: {model_type}"}
        
        # Envoyer les résultats via le système d'événements
        if self.meta_systems:
            self.meta_systems.trigger_event("model_training_complete", {
                "model_name": model_name,
                "model_type": model_type,
                "results": results,
                "timestamp": datetime.datetime.now().isoformat()
            })
    
    def _handle_anomaly_detection_request(self, event_data):
        """
        Gestionnaire d'événement pour les demandes de détection d'anomalies.
        
        Args:
            event_data (dict): Données de l'événement
        """
        if "match_data" not in event_data:
            self.logger.error("Données de match manquantes dans la demande de détection d'anomalies")
            return
        
        match_data = event_data["match_data"]
        threshold = event_data.get("threshold", 0.9)
        model_name = event_data.get("model_name", "match_result_model")
        
        # Effectuer la détection d'anomalies
        anomalies = self.detect_anomalies(match_data, threshold, model_name)
        
        # Envoyer les résultats via le système d'événements
        if self.meta_systems and anomalies:
            self.meta_systems.trigger_event("anomaly_detection_complete", {
                "match_id": event_data.get("match_id"),
                "anomalies": anomalies,
                "model_used": model_name,
                "timestamp": datetime.datetime.now().isoformat()
            })
    
    def integrate_with_arcan_brain(self, arcan_brain_result):
        """
        Intègre les résultats de PredictiveForge avec ceux d'ArcanBrain.
        
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
        
        # Effectuer les prédictions
        match_result_prediction = None
        score_prediction = None
        
        try:
            if "match_result_model" in self.models:
                match_result_prediction = self.predict_match_result(match_data)
            
            if "score_prediction_model" in self.models:
                score_prediction = self.predict_match_score(match_data)
                
        except Exception as e:
            self.logger.error(f"Erreur lors de l'intégration avec ArcanBrain: {e}")
            return arcan_brain_result
        
        # Intégrer les résultats
        enriched_result = arcan_brain_result.copy()
        
        # Ajouter l'analyse XGBoost
        if 'additional_analyses' not in enriched_result:
            enriched_result['additional_analyses'] = {}
        
        enriched_result['additional_analyses']['xgboost'] = {}
        
        if match_result_prediction and 'error' not in match_result_prediction:
            enriched_result['additional_analyses']['xgboost']['match_result'] = match_result_prediction
            
            # Intégrer les probabilités dans les insights principaux
            if 'insights' in enriched_result and 'probabilities' in match_result_prediction:
                for outcome, probability in match_result_prediction['probabilities'].items():
                    enriched_result['insights'][f'xgboost_{outcome.lower()}'] = f"{outcome}: {probability:.2%}"
        
        if score_prediction and 'error' not in score_prediction:
            enriched_result['additional_analyses']['xgboost']['score_prediction'] = score_prediction
            
            # Intégrer la prédiction de score dans les insights principaux
            if 'insights' in enriched_result and 'predicted_score' in score_prediction:
                enriched_result['insights']['xgboost_score'] = f"Score prédit: {score_prediction['predicted_score']}"
        
        return enriched_result
    
    def get_model_metrics(self, model_name=None):
        """
        Récupère les métriques des modèles.
        
        Args:
            model_name (str, optional): Nom du modèle spécifique
            
        Returns:
            dict: Métriques des modèles
        """
        if model_name:
            metrics = {}
            for metric_name, values in self.metrics.items():
                if len(values) > 0:
                    metrics[metric_name] = values[-1]
            return {model_name: metrics}
        
        return self.metrics
    
    def get_feature_importance(self, model_name=None):
        """
        Récupère l'importance des caractéristiques d'un modèle.
        
        Args:
            model_name (str, optional): Nom du modèle spécifique
            
        Returns:
            dict: Importance des caractéristiques
        """
        if model_name:
            return {model_name: self.feature_importance.get(model_name, {})}
        
        return self.feature_importance
    
    def generate_model_summary(self, model_name=None):
        """
        Génère un résumé des performances du modèle.
        
        Args:
            model_name (str, optional): Nom du modèle spécifique
            
        Returns:
            str: Résumé du modèle
        """
        if model_name and model_name not in self.models:
            return f"Modèle {model_name} non trouvé"
        
        summary = []
        summary.append("=== Résumé des modèles PredictiveForge ===")
        
        if model_name:
            models_to_summarize = [model_name]
        else:
            models_to_summarize = list(self.models.keys())
        
        for name in models_to_summarize:
            summary.append(f"\nModèle: {name}")
            
            # Métriques
            metrics = self.get_model_metrics(name)
            if name in metrics and metrics[name]:
                summary.append("  Métriques:")
                for metric_name, value in metrics[name].items():
                    summary.append(f"    {metric_name}: {value:.4f}")
            
            # Importance des caractéristiques
            importance = self.get_feature_importance(name)
            if name in importance and importance[name]:
                summary.append("  Caractéristiques les plus importantes:")
                sorted_features = sorted(importance[name].items(), key=lambda x: x[1], reverse=True)
                for feature, imp in sorted_features[:5]:
                    summary.append(f"    {feature}: {imp:.4f}")
        
        return "\n".join(summary)


class CoreXGBoost:
    """Sous-module implémentant le cœur XGBoost."""
    
    def __init__(self, predictive_forge):
        """
        Initialise le sous-module CoreXGBoost.
        
        Args:
            predictive_forge (PredictiveForge): Instance du module parent
        """
        self.predictive_forge = predictive_forge
        self.logger = predictive_forge.logger
    
    def train_model(self, X, y, objective="binary:logistic", num_class=None, params=None):
        """
        Entraîne un modèle XGBoost.
        
        Args:
            X: Caractéristiques d'entraînement
            y: Cibles d'entraînement
            objective (str): Objectif du modèle
            num_class (int, optional): Nombre de classes pour la classification multiclasse
            params (dict, optional): Paramètres personnalisés
            
        Returns:
            tuple: (modèle entraîné, paramètres utilisés)
        """
        self.logger.info("Entraînement d'un modèle XGBoost")
        
        # Paramètres par défaut
        default_params = {
            'objective': objective,
            'learning_rate': 0.1,
            'max_depth': 5,
            'min_child_weight': 1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'gamma': 0,
            'reg_alpha': 0,
            'reg_lambda': 1,
            'scale_pos_weight': 1,
            'seed': 42,
            'n_jobs': -1
        }
        
        # Ajouter num_class pour la classification multiclasse
        if objective.startswith('multi:') and num_class:
            default_params['num_class'] = num_class
        
        # Fusionner avec les paramètres personnalisés
        if params:
            default_params.update(params)
        
        # Obtenir des paramètres optimisés
        optimized_params = self.predictive_forge.hyper_tuner.get_optimized_params(X, y, default_params)
        
        # Créer le modèle
        model = xgb.XGBClassifier(**optimized_params)
        
        # Entraîner le modèle
        model.fit(X, y)
        
        return model, optimized_params
    
    def create_ensemble(self, X, y, num_models=3, objective="binary:logistic", num_class=None):
        """
        Crée un ensemble de modèles XGBoost.
        
        Args:
            X: Caractéristiques d'entraînement
            y: Cibles d'entraînement
            num_models (int): Nombre de modèles dans l'ensemble
            objective (str): Objectif des modèles
            num_class (int, optional): Nombre de classes pour la classification multiclasse
            
        Returns:
            list: Liste des modèles entraînés
        """
        self.logger.info(f"Création d'un ensemble de {num_models} modèles XGBoost")
        
        models = []
        for i in range(num_models):
            seed = 42 + i
            params = {
                'objective': objective,
                'seed': seed,
                'subsample': 0.8 + (i * 0.05),
                'colsample_bytree': 0.8 - (i * 0.05)
            }
            
            if objective.startswith('multi:') and num_class:
                params['num_class'] = num_class
            
            model, _ = self.train_model(X, y, objective, num_class, params)
            models.append(model)
        
        return models
    
    def predict_with_ensemble(self, X, models, is_classification=True):
        """
        Effectue une prédiction avec un ensemble de modèles.
        
        Args:
            X: Caractéristiques pour la prédiction
            models (list): Liste des modèles
            is_classification (bool): Si True, retourne la prédiction de classe
            
        Returns:
            np.ndarray: Prédictions de l'ensemble
        """
        if not models:
            self.logger.error("Liste de modèles vide pour la prédiction d'ensemble")
            return None
        
        if is_classification:
            # Prédictions de probabilités
            probas = []
            for model in models:
                probas.append(model.predict_proba(X))
            
            # Moyenne des probabilités
            avg_proba = np.mean(probas, axis=0)
            
            # Classe prédite
            return np.argmax(avg_proba, axis=1)
        else:
            # Prédictions de valeurs
            preds = []
            for model in models:
                preds.append(model.predict(X))
            
            # Moyenne des prédictions
            return np.mean(preds, axis=0)


class FeatureEngineer:
    """Sous-module pour la création et la transformation des caractéristiques."""
    
    def __init__(self, predictive_forge):
        """
        Initialise le sous-module FeatureEngineer.
        
        Args:
            predictive_forge (PredictiveForge): Instance du module parent
        """
        self.predictive_forge = predictive_forge
        self.logger = predictive_forge.logger
        self.label_encoders = {}
        self.onehot_encoders = {}
    
    def preprocess_match_data(self, data, training=True, encoders=None):
        """
        Prétraite les données de match pour l'entraînement ou la prédiction.
        
        Args:
            data (pd.DataFrame): Données de match
            training (bool): Si True, mode d'entraînement, sinon mode de prédiction
            encoders (dict, optional): Encodeurs préexistants pour le mode de prédiction
            
        Returns:
            dict: Données prétraitées
        """
        self.logger.info(f"Prétraitement des données en mode {'entraînement' if training else 'prédiction'}")
        
        if data is None or len(data) == 0:
            self.logger.error("Données vides ou invalides")
            return None
        
        try:
            # Copier pour éviter de modifier l'original
            df = data.copy()
            
            # Vérification des colonnes nécessaires
            required_columns = ["home_team", "away_team"]
            if training:
                required_columns.append("result")
            
            for col in required_columns:
                if col not in df.columns:
                    self.logger.error(f"Colonne requise manquante: {col}")
                    return None
            
            # Caractéristiques catégorielles à encoder
            categorical_features = ["home_team", "away_team", "competition", "season"]
            categorical_features = [f for f in categorical_features if f in df.columns]
            
            # Caractéristiques numériques
            numerical_features = ["home_form", "away_form", "home_ranking", "away_ranking", 
                                "home_goals_scored", "away_goals_scored", "home_goals_conceded", 
                                "away_goals_conceded"]
            numerical_features = [f for f in numerical_features if f in df.columns]
            
            # Encoder les caractéristiques catégorielles
            if training:
                # Créer de nouveaux encodeurs
                self.label_encoders = {}
                self.onehot_encoders = {}
                
                for feature in categorical_features:
                    le = LabelEncoder()
                    df[f"{feature}_encoded"] = le.fit_transform(df[feature])
                    self.label_encoders[feature] = le
                
                # One-hot encoding pour certaines caractéristiques
                onehot_features = ["competition", "season"]
                onehot_features = [f for f in onehot_features if f in df.columns]
                
                for feature in onehot_features:
                    ohe = OneHotEncoder(sparse=False, handle_unknown='ignore')
                    encoded = ohe.fit_transform(df[[feature]])
                    
                    # Créer un DataFrame avec les nouvelles colonnes
                    encoded_df = pd.DataFrame(
                        encoded, 
                        columns=[f"{feature}_{i}" for i in range(encoded.shape[1])]
                    )
                    
                    # Concaténer avec le DataFrame original
                    df = pd.concat([df, encoded_df], axis=1)
                    
                    self.onehot_encoders[feature] = ohe
            else:
                # Utiliser les encodeurs existants
                if encoders:
                    for feature, le in encoders.get("label", {}).items():
                        if feature in df.columns:
                            df[f"{feature}_encoded"] = df[feature].map(lambda x: 
                                le.transform([x])[0] if x in le.classes_ else -1)
                    
                    for feature, ohe in encoders.get("onehot", {}).items():
                        if feature in df.columns:
                            try:
                                encoded = ohe.transform(df[[feature]])
                                encoded_df = pd.DataFrame(
                                    encoded, 
                                    columns=[f"{feature}_{i}" for i in range(encoded.shape[1])]
                                )
                                df = pd.concat([df, encoded_df], axis=1)
                            except Exception as e:
                                self.logger.error(f"Erreur lors de l'encodage one-hot de {feature}: {e}")
            
            # Création de caractéristiques
            # Différence de forme
            if "home_form" in df.columns and "away_form" in df.columns:
                df["form_diff"] = df["home_form"] - df["away_form"]
            
            # Différence de classement
            if "home_ranking" in df.columns and "away_ranking" in df.columns:
                df["ranking_diff"] = df["away_ranking"] - df["home_ranking"]
            
            # Ratio de buts marqués/concédés
            if all(f in df.columns for f in ["home_goals_scored", "home_goals_conceded"]):
                df["home_goal_ratio"] = df["home_goals_scored"] / df["home_goals_conceded"].replace(0, 0.5)
            
            if all(f in df.columns for f in ["away_goals_scored", "away_goals_conceded"]):
                df["away_goal_ratio"] = df["away_goals_scored"] / df["away_goals_conceded"].replace(0, 0.5)
            
            # Caractéristiques temporelles
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                df["day_of_week"] = df["date"].dt.dayofweek
                df["month"] = df["date"].dt.month
                df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
                
                numerical_features.extend(["day_of_week", "month", "is_weekend"])
            
            # Construire la liste finale des caractéristiques
            feature_columns = []
            
            # Caractéristiques encodées
            for feature in categorical_features:
                feature_columns.append(f"{feature}_encoded")
            
            # Colonnes one-hot
            if training:
                onehot_columns = []
                for feature in onehot_features:
                    onehot_columns.extend([col for col in df.columns if col.startswith(f"{feature}_")])
                feature_columns.extend(onehot_columns)
            else:
                if encoders:
                    for feature in encoders.get("onehot", {}):
                        feature_columns.extend([col for col in df.columns if col.startswith(f"{feature}_")])
            
            # Caractéristiques numériques
            feature_columns.extend(numerical_features)
            
            # Caractéristiques dérivées
            derived_features = ["form_diff", "ranking_diff", "home_goal_ratio", "away_goal_ratio"]
            feature_columns.extend([f for f in derived_features if f in df.columns])
            
            # Filtrer pour ne garder que les colonnes qui existent
            feature_columns = [col for col in feature_columns if col in df.columns]
            
            # Construire X
            X = df[feature_columns]
            
            # Construire y en mode entraînement
            if training:
                # Encoder la cible
                if "result" in df.columns:
                    le_result = LabelEncoder()
                    y = le_result.fit_transform(df["result"])
                    self.label_encoders["result"] = le_result
                else:
                    self.logger.error("Colonne 'result' manquante pour l'entraînement")
                    return None
            else:
                y = None
            
            # Créer la sortie
            result = {
                "features": X,
                "feature_names": feature_columns,
            }
            
            if training:
                result["target"] = y
                result["encoders"] = {
                    "label": self.label_encoders,
                    "onehot": self.onehot_encoders
                }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erreur lors du prétraitement des données: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return None
    
    def select_best_features(self, X, y, k=10):
        """
        Sélectionne les meilleures caractéristiques.
        
        Args:
            X (pd.DataFrame): Caractéristiques
            y: Cible
            k (int): Nombre de caractéristiques à sélectionner
            
        Returns:
            pd.DataFrame: Caractéristiques sélectionnées
        """
        self.logger.info(f"Sélection des {k} meilleures caractéristiques")
        
        # Créer un modèle simple
        model = xgb.XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=4)
        
        # Sélectionner les caractéristiques
        selector = SelectFromModel(model, threshold=-np.inf, max_features=k, prefit=False)
        selector.fit(X, y)
        
        # Obtenir les masques des caractéristiques sélectionnées
        feature_mask = selector.get_support()
        
        # Obtenir les noms des caractéristiques sélectionnées
        selected_features = X.columns[feature_mask]
        
        # Nouvelle matrice avec les caractéristiques sélectionnées
        X_selected = X[selected_features]
        
        self.logger.info(f"Caractéristiques sélectionnées: {', '.join(selected_features)}")
        
        return X_selected, list(selected_features)
    
    def create_interaction_features(self, X):
        """
        Crée des caractéristiques d'interaction.
        
        Args:
            X (pd.DataFrame): Caractéristiques originales
            
        Returns:
            pd.DataFrame: Caractéristiques avec interactions
        """
        self.logger.info("Création de caractéristiques d'interaction")
        
        X_new = X.copy()
        
        # Sélectionner les paires de caractéristiques pour les interactions
        # Exemple : forme de l'équipe domicile × forme de l'équipe extérieur
        if "home_form" in X.columns and "away_form" in X.columns:
            X_new["home_away_form_interaction"] = X["home_form"] * X["away_form"]
        
        # Forme domicile × but ratio domicile
        if "home_form" in X.columns and "home_goal_ratio" in X.columns:
            X_new["home_form_goal_interaction"] = X["home_form"] * X["home_goal_ratio"]
        
        # Forme extérieur × but ratio extérieur
        if "away_form" in X.columns and "away_goal_ratio" in X.columns:
            X_new["away_form_goal_interaction"] = X["away_form"] * X["away_goal_ratio"]
        
        # Classement domicile × classement extérieur
        if "home_ranking" in X.columns and "away_ranking" in X.columns:
            X_new["ranking_interaction"] = X["home_ranking"] * X["away_ranking"]
        
        # Jour de la semaine × équipe à domicile
        if "day_of_week" in X.columns and "home_team_encoded" in X.columns:
            X_new["home_day_interaction"] = X["day_of_week"] * X["home_team_encoded"]
        
        # Jour de la semaine × équipe à l'extérieur
        if "day_of_week" in X.columns and "away_team_encoded" in X.columns:
            X_new["away_day_interaction"] = X["day_of_week"] * X["away_team_encoded"]
        
        return X_new


class HyperTuner:
    """Sous-module pour l'optimisation des hyperparamètres."""
    
    def __init__(self, predictive_forge):
        """
        Initialise le sous-module HyperTuner.
        
        Args:
            predictive_forge (PredictiveForge): Instance du module parent
        """
        self.predictive_forge = predictive_forge
        self.logger = predictive_forge.logger
        self.param_cache = {}
    
    def _get_param_grid(self, base_params):
        """
        Génère une grille de paramètres pour l'optimisation.
        
        Args:
            base_params (dict): Paramètres de base
            
        Returns:
            dict: Grille de paramètres
        """
        # Grille de paramètres à explorer
        param_grid = {
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.1, 0.2],
            'n_estimators': [50, 100, 200],
            'subsample': [0.6, 0.8, 1.0],
            'colsample_bytree': [0.6, 0.8, 1.0],
            'min_child_weight': [1, 3, 5],
            'gamma': [0, 0.1, 0.2]
        }
        
        # Si c'est une classification multiclasse, ajouter num_class
        if 'num_class' in base_params:
            param_grid['num_class'] = [base_params['num_class']]
        
        # Si objective est spécifié, le conserver
        if 'objective' in base_params:
            param_grid['objective'] = [base_params['objective']]
        
        return param_grid
    
    def optimize_params_grid_search(self, X, y, base_params=None):
        """
        Optimise les hyperparamètres avec GridSearchCV.
        
        Args:
            X: Caractéristiques d'entraînement
            y: Cibles d'entraînement
            base_params (dict, optional): Paramètres de base
            
        Returns:
            dict: Paramètres optimisés
        """
        self.logger.info("Optimisation des hyperparamètres avec GridSearchCV")
        
        # Paramètres de base
        if not base_params:
            base_params = {}
        
        # Calculer une clé de cache
        cache_key = f"grid_{X.shape[0]}_{X.shape[1]}_{base_params.get('objective', 'default')}"
        
        # Vérifier si déjà dans le cache
        if cache_key in self.param_cache:
            self.logger.info("Utilisation des paramètres optimisés en cache")
            return self.param_cache[cache_key]
        
        # Créer le modèle de base
        model = xgb.XGBClassifier()
        
        # Obtenir la grille de paramètres
        param_grid = self._get_param_grid(base_params)
        
        # Réduire la grille pour les gros ensembles de données
        if X.shape[0] > 10000:
            self.logger.info("Grand ensemble de données détecté, réduction de la grille de paramètres")
            for param, values in param_grid.items():
                if len(values) > 2:
                    param_grid[param] = [values[0], values[-1]]
        
        # Recherche par grille
        grid_search = GridSearchCV(
            model, param_grid, cv=3, scoring='accuracy', verbose=0, n_jobs=-1
        )
        
        # Ajuster le modèle
        grid_search.fit(X, y)
        
        # Obtenir les meilleurs paramètres
        best_params = grid_search.best_params_
        
        # Ajouter les paramètres manquants depuis base_params
        for param, value in base_params.items():
            if param not in best_params:
                best_params[param] = value
        
        # Stocker dans le cache
        self.param_cache[cache_key] = best_params
        
        self.logger.info(f"Meilleurs paramètres trouvés: {best_params}")
        return best_params
    
    def optimize_params_bayesian(self, X, y, base_params=None):
        """
        Optimise les hyperparamètres avec l'optimisation bayésienne.
        Non implémenté pour simplifier, mais pourrait être ajouté.
        
        Args:
            X: Caractéristiques d'entraînement
            y: Cibles d'entraînement
            base_params (dict, optional): Paramètres de base
            
        Returns:
            dict: Paramètres optimisés
        """
        self.logger.info("Optimisation bayésienne non implémentée, utilisation de GridSearchCV")
        return self.optimize_params_grid_search(X, y, base_params)
    
    def get_optimized_params(self, X, y, base_params=None, method="grid"):
        """
        Obtient des paramètres optimisés selon la méthode spécifiée.
        
        Args:
            X: Caractéristiques d'entraînement
            y: Cibles d'entraînement
            base_params (dict, optional): Paramètres de base
            method (str): Méthode d'optimisation ('grid' ou 'bayesian')
            
        Returns:
            dict: Paramètres optimisés
        """
        if method == "grid":
            return self.optimize_params_grid_search(X, y, base_params)
        elif method == "bayesian":
            return self.optimize_params_bayesian(X, y, base_params)
        else:
            self.logger.error(f"Méthode d'optimisation inconnue: {method}")
            return base_params or {}


class EnsembleDirector:
    """Sous-module pour la gestion des modèles d'ensemble."""
    
    def __init__(self, predictive_forge):
        """
        Initialise le sous-module EnsembleDirector.
        
        Args:
            predictive_forge (PredictiveForge): Instance du module parent
        """
        self.predictive_forge = predictive_forge
        self.logger = predictive_forge.logger
        self.ensembles = {}
    
    def create_ensemble(self, X, y, model_name, num_models=5, diversity_method="params"):
        """
        Crée un ensemble de modèles.
        
        Args:
            X: Caractéristiques d'entraînement
            y: Cibles d'entraînement
            model_name (str): Nom de l'ensemble
            num_models (int): Nombre de modèles dans l'ensemble
            diversity_method (str): Méthode pour assurer la diversité ('params', 'features', 'both')
            
        Returns:
            list: Liste des modèles de l'ensemble
        """
        self.logger.info(f"Création d'un ensemble de {num_models} modèles pour {model_name}")
        
        # Détecter si c'est une classification multiclasse
        num_classes = len(np.unique(y))
        objective = "multi:softprob" if num_classes > 2 else "binary:logistic"
        
        models = []
        
        for i in range(num_models):
            # Diversifier les paramètres
            if diversity_method in ["params", "both"]:
                params = {
                    'objective': objective,
                    'learning_rate': 0.1 + (i * 0.02),
                    'max_depth': 5 + (i % 3),
                    'subsample': 0.7 + (i * 0.05),
                    'colsample_bytree': 0.7 + ((num_models - i) * 0.05),
                    'seed': 42 + i
                }
                
                if num_classes > 2:
                    params['num_class'] = num_classes
            else:
                params = None
            
            # Diversifier les caractéristiques
            if diversity_method in ["features", "both"]:
                # Sélectionner un sous-ensemble aléatoire de caractéristiques
                n_features = X.shape[1]
                n_selected = max(int(n_features * 0.7), 1)  # Au moins 70% des caractéristiques
                
                if hasattr(X, 'columns'):
                    # Pour DataFrame
                    selected_cols = np.random.choice(X.columns, n_selected, replace=False)
                    X_subset = X[selected_cols]
                else:
                    # Pour ndarray
                    selected_indices = np.random.choice(n_features, n_selected, replace=False)
                    X_subset = X[:, selected_indices]
            else:
                X_subset = X
            
            # Entraîner le modèle
            model, _ = self.predictive_forge.core_xgboost.train_model(X_subset, y, params=params)
            models.append(model)
        
        # Sauvegarder l'ensemble
        self.ensembles[model_name] = models
        
        # Sauvegarder sur le disque
        ensemble_dir = os.path.join(self.predictive_forge.data_path, "ensembles")
        os.makedirs(ensemble_dir, exist_ok=True)
        
        ensemble_path = os.path.join(ensemble_dir, f"{model_name}.pkl")
        try:
            with open(ensemble_path, "wb") as f:
                pickle.dump(models, f)
            self.logger.info(f"Ensemble {model_name} sauvegardé")
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde de l'ensemble {model_name}: {e}")
        
        return models
    
    def predict_with_ensemble(self, X, model_name, weighted=False):
        """
        Effectue une prédiction avec un ensemble.
        
        Args:
            X: Caractéristiques pour la prédiction
            model_name (str): Nom de l'ensemble
            weighted (bool): Si True, utilise une pondération des modèles
            
        Returns:
            dict: Résultats de la prédiction
        """
        if model_name not in self.ensembles:
            # Essayer de charger l'ensemble
            ensemble_path = os.path.join(self.predictive_forge.data_path, "ensembles", f"{model_name}.pkl")
            if os.path.exists(ensemble_path):
                try:
                    with open(ensemble_path, "rb") as f:
                        self.ensembles[model_name] = pickle.load(f)
                except Exception as e:
                    self.logger.error(f"Erreur lors du chargement de l'ensemble {model_name}: {e}")
                    return {"error": f"Ensemble {model_name} non trouvé"}
            else:
                return {"error": f"Ensemble {model_name} non trouvé"}
        
        models = self.ensembles[model_name]
        
        if not models:
            return {"error": f"Ensemble {model_name} vide"}
        
        # Calculer les poids si nécessaire
        weights = None
        if weighted:
            # Exemple simple: donner plus de poids aux modèles plus récents
            weights = [1 + i/len(models) for i in range(len(models))]
            weights = [w / sum(weights) for w in weights]  # Normaliser
        
        # Vérifier si c'est un problème de classification
        is_classifier = all(hasattr(model, 'predict_proba') for model in models)
        
        if is_classifier:
            # Prédictions de probabilités
            probas = []
            for i, model in enumerate(models):
                model_proba = model.predict_proba(X)
                if weights:
                    model_proba *= weights[i]
                probas.append(model_proba)
            
            # Moyenne des probabilités
            if weights:
                avg_proba = np.sum(probas, axis=0)
            else:
                avg_proba = np.mean(probas, axis=0)
            
            # Classes prédites
            predictions = np.argmax(avg_proba, axis=1)
            
            # Confiance (probabilité maximale)
            confidence = np.max(avg_proba, axis=1)
            
            return {
                "predictions": predictions,
                "probabilities": avg_proba,
                "confidence": confidence
            }
        else:
            # Prédictions de valeurs
            preds = []
            for i, model in enumerate(models):
                model_pred = model.predict(X)
                if weights:
                    model_pred *= weights[i]
                preds.append(model_pred)
            
            # Moyenne des prédictions
            if weights:
                predictions = np.sum(preds, axis=0)
            else:
                predictions = np.mean(preds, axis=0)
            
            return {"predictions": predictions}
    
    def evaluate_ensemble(self, X, y, model_name):
        """
        Évalue les performances d'un ensemble.
        
        Args:
            X: Caractéristiques pour l'évaluation
            y: Cibles pour l'évaluation
            model_name (str): Nom de l'ensemble
            
        Returns:
            dict: Métriques d'évaluation
        """
        prediction_result = self.predict_with_ensemble(X, model_name)
        
        if "error" in prediction_result:
            return prediction_result
        
        predictions = prediction_result["predictions"]
        
        # Calculer les métriques
        accuracy = accuracy_score(y, predictions)
        
        # Vérifier si multiclasse
        n_classes = len(np.unique(y))
        if n_classes > 2:
            precision = precision_score(y, predictions, average="weighted")
            recall = recall_score(y, predictions, average="weighted")
            f1 = f1_score(y, predictions, average="weighted")
        else:
            precision = precision_score(y, predictions)
            recall = recall_score(y, predictions)
            f1 = f1_score(y, predictions)
        
        # Ajouter log_loss si les probabilités sont disponibles
        metrics = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        }
        
        if "probabilities" in prediction_result:
            loss = log_loss(y, prediction_result["probabilities"])
            metrics["log_loss"] = loss
        
        return metrics


class AnomalyXGBoost:
    """Sous-module pour la détection d'anomalies avec XGBoost."""
    
    def __init__(self, predictive_forge):
        """
        Initialise le sous-module AnomalyXGBoost.
        
        Args:
            predictive_forge (PredictiveForge): Instance du module parent
        """
        self.predictive_forge = predictive_forge
        self.logger = predictive_forge.logger
        self.anomaly_models = {}
    
    def train_anomaly_model(self, data, model_name="anomaly_model"):
        """
        Entraîne un modèle de détection d'anomalies.
        
        Args:
            data (pd.DataFrame): Données d'entraînement (normales)
            model_name (str): Nom du modèle
            
        Returns:
            dict: Résultat de l'entraînement
        """
        self.logger.info(f"Entraînement du modèle d'anomalies {model_name}")
        
        # Prétraiter les données
        processed_data = self.predictive_forge.feature_engineer.preprocess_match_data(data)
        
        if processed_data is None or "features" not in processed_data:
            return {"error": "Échec du prétraitement des données"}
        
        X = processed_data["features"]
        
        # Créer le modèle d'isolation forest avec XGBoost
        # Note: XGBoost n'a pas d'implémentation directe d'isolation forest,
        # mais nous pouvons utiliser un modèle de régression pour prédire la "normalité"
        model = xgb.XGBRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            objective='reg:squarederror'
        )
        
        # Créer des cibles synthétiques (toutes normales)
        y = np.ones(X.shape[0])
        
        # Entraîner le modèle
        model.fit(X, y)
        
        # Prédire sur les données d'entraînement
        scores = model.predict(X)
        
        # Calculer les statistiques des scores
        mean_score = np.mean(scores)
        std_score = np.std(scores)
        min_score = np.min(scores)
        max_score = np.max(scores)
        
        # Calculer le seuil d'anomalie (par exemple, 3 écarts-types de la moyenne)
        threshold = mean_score - (3 * std_score)
        
        # Stocker le modèle et les métadonnées
        self.anomaly_models[model_name] = {
            "model": model,
            "mean_score": mean_score,
            "std_score": std_score,
            "threshold": threshold,
            "encoders": processed_data.get("encoders")
        }
        
        # Sauvegarder le modèle
        models_dir = os.path.join(self.predictive_forge.data_path, "models")
        os.makedirs(models_dir, exist_ok=True)
        
        model_path = os.path.join(models_dir, f"{model_name}.pkl")
        meta_path = os.path.join(models_dir, f"{model_name}_meta.json")
        
        try:
            with open(model_path, "wb") as f:
                pickle.dump(model, f)
            
            # Sauvegarder les métadonnées (sauf le modèle)
            meta_data = {
                "mean_score": float(mean_score),
                "std_score": float(std_score),
                "threshold": float(threshold)
            }
            
            with open(meta_path, "w") as f:
                json.dump(meta_data, f)
            
            # Sauvegarder les encodeurs
            if "encoders" in processed_data:
                encoder_path = os.path.join(models_dir, f"{model_name}_encoders.pkl")
                with open(encoder_path, "wb") as f:
                    pickle.dump(processed_data["encoders"], f)
            
            self.logger.info(f"Modèle d'anomalies {model_name} sauvegardé")
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde du modèle d'anomalies {model_name}: {e}")
        
        return {
            "mean_score": float(mean_score),
            "std_score": float(std_score),
            "threshold": float(threshold),
            "min_score": float(min_score),
            "max_score": float(max_score)
        }
    
    def detect_anomalies(self, match_data, threshold=None, model_name="anomaly_model"):
        """
        Détecte les anomalies dans les données de match.
        
        Args:
            match_data: Données de match
            threshold (float, optional): Seuil personnalisé
            model_name (str): Nom du modèle à utiliser
            
        Returns:
            dict: Anomalies détectées
        """
        self.logger.info(f"Détection d'anomalies avec le modèle {model_name}")
        
        # Charger le modèle si nécessaire
        if model_name not in self.anomaly_models:
            # Essayer de charger le modèle et les métadonnées
            models_dir = os.path.join(self.predictive_forge.data_path, "models")
            model_path = os.path.join(models_dir, f"{model_name}.pkl")
            meta_path = os.path.join(models_dir, f"{model_name}_meta.json")
            encoder_path = os.path.join(models_dir, f"{model_name}_encoders.pkl")
            
            if not os.path.exists(model_path) or not os.path.exists(meta_path):
                return {"error": f"Modèle d'anomalies {model_name} non trouvé"}
            
            try:
                # Charger le modèle
                with open(model_path, "rb") as f:
                    model = pickle.load(f)
                
                # Charger les métadonnées
                with open(meta_path, "r") as f:
                    meta_data = json.load(f)
                
                # Charger les encodeurs si disponibles
                encoders = None
                if os.path.exists(encoder_path):
                    with open(encoder_path, "rb") as f:
                        encoders = pickle.load(f)
                
                # Stocker le modèle et les métadonnées
                self.anomaly_models[model_name] = {
                    "model": model,
                    "mean_score": meta_data["mean_score"],
                    "std_score": meta_data["std_score"],
                    "threshold": meta_data["threshold"],
                    "encoders": encoders
                }
                
                self.logger.info(f"Modèle d'anomalies {model_name} chargé")
            except Exception as e:
                self.logger.error(f"Erreur lors du chargement du modèle d'anomalies {model_name}: {e}")
                return {"error": f"Erreur lors du chargement du modèle: {e}"}
        
        # Vérifier si le modèle est disponible
        if model_name not in self.anomaly_models:
            return {"error": f"Modèle d'anomalies {model_name} non disponible"}
        
        model_data = self.anomaly_models[model_name]
        model = model_data["model"]
        default_threshold = model_data["threshold"]
        
        # Utiliser le seuil personnalisé ou celui du modèle
        anomaly_threshold = threshold if threshold is not None else default_threshold
        
        # Convertir en DataFrame si nécessaire
        if isinstance(match_data, dict):
            match_df = pd.DataFrame([match_data])
        else:
            match_df = match_data
        
        # Prétraiter les données
        processed_data = self.predictive_forge.feature_engineer.preprocess_match_data(
            match_df, 
            training=False, 
            encoders=model_data.get("encoders")
        )
        
        if processed_data is None or "features" not in processed_data:
            return {"error": "Échec du prétraitement des données"}
        
        X = processed_data["features"]
        
        # Prédire les scores
        scores = model.predict(X)
        
        # Identifier les anomalies
        anomalies = scores < anomaly_threshold
        
        # Préparer les résultats
        results = []
        for i, is_anomaly in enumerate(anomalies):
            if is_anomaly:
                match_info = match_df.iloc[i].to_dict() if hasattr(match_df, 'iloc') else match_data
                anomaly_info = {
                    "match_info": match_info,
                    "anomaly_score": float(scores[i]),
                    "threshold": float(anomaly_threshold),
                    "deviation": float((model_data["mean_score"] - scores[i]) / model_data["std_score"])
                }
                results.append(anomaly_info)
        
        return {
            "anomalies_detected": len(results),
            "anomalies": results,
            "mean_score": float(model_data["mean_score"]),
            "threshold_used": float(anomaly_threshold)
        }


class ScorePredictor:
    """Sous-module pour la prédiction de scores exacts."""
    
    def __init__(self, predictive_forge):
        """
        Initialise le sous-module ScorePredictor.
        
        Args:
            predictive_forge (PredictiveForge): Instance du module parent
        """
        self.predictive_forge = predictive_forge
        self.logger = predictive_forge.logger
        self.score_models = {}
        self.score_distributions = {}
    
    def train_model(self, data, test_size=0.2, model_name="score_prediction_model"):
        """
        Entraîne un modèle de prédiction de score.
        
        Args:
            data (pd.DataFrame): Données d'entraînement
            test_size (float): Proportion des données pour le test
            model_name (str): Nom du modèle
            
        Returns:
            dict: Métriques du modèle
        """
        self.logger.info(f"Entraînement du modèle de prédiction de score {model_name}")
        
        # Vérifier les colonnes requises
        required_columns = ["home_team", "away_team", "home_score", "away_score"]
        for col in required_columns:
            if col not in data.columns:
                return {"error": f"Colonne requise manquante: {col}"}
        
        # Prétraitement des données
        processed_data = self.predictive_forge.feature_engineer.preprocess_match_data(
            data, training=True
        )
        
        if processed_data is None:
            return {"error": "Échec du prétraitement des données"}
        
        X = processed_data["features"]
        
        # Cibles: scores des équipes à domicile et à l'extérieur
        y_home = data["home_score"].values
        y_away = data["away_score"].values
        
        # Diviser en ensembles d'entraînement et de test
        X_train, X_test, y_home_train, y_home_test, y_away_train, y_away_test = train_test_split(
            X, y_home, y_away, test_size=test_size, random_state=42
        )
        
        # Entraîner le modèle pour l'équipe à domicile
        home_model, home_params = self.predictive_forge.core_xgboost.train_model(
            X_train, y_home_train, objective="count:poisson"
        )
        
        # Entraîner le modèle pour l'équipe à l'extérieur
        away_model, away_params = self.predictive_forge.core_xgboost.train_model(
            X_train, y_away_train, objective="count:poisson"
        )
        
        # Évaluer les modèles
        y_home_pred = np.round(home_model.predict(X_test)).astype(int)
        y_away_pred = np.round(away_model.predict(X_test)).astype(int)
        
        # Précision exacte (score exact)
        exact_accuracy = np.mean((y_home_pred == y_home_test) & (y_away_pred == y_away_test))
        
        # Précision du résultat (victoire/nul/défaite)
        y_result_test = np.sign(y_home_test - y_away_test) + 1  # 0:Away win, 1:Draw, 2:Home win
        y_result_pred = np.sign(y_home_pred - y_away_pred) + 1
        result_accuracy = np.mean(y_result_test == y_result_pred)
        
        # Erreur moyenne
        home_error = np.mean(np.abs(y_home_pred - y_home_test))
        away_error = np.mean(np.abs(y_away_pred - y_away_test))
        
        # Calculer la distribution des scores
        score_distribution = {}
        for home in range(10):
            for away in range(10):
                score = f"{home}-{away}"
                count = np.sum((data["home_score"] == home) & (data["away_score"] == away))
                score_distribution[score] = int(count)
        
        # Stocker les modèles et la distribution
        self.score_models[model_name] = {
            "home_model": home_model,
            "away_model": away_model,
            "encoders": processed_data.get("encoders")
        }
        
        self.score_distributions[model_name] = score_distribution
        
        # Sauvegarder les modèles
        models_dir = os.path.join(self.predictive_forge.data_path, "models")
        os.makedirs(models_dir, exist_ok=True)
        
        home_model_path = os.path.join(models_dir, f"{model_name}_home.pkl")
        away_model_path = os.path.join(models_dir, f"{model_name}_away.pkl")
        distribution_path = os.path.join(models_dir, f"{model_name}_distribution.json")
        
        try:
            with open(home_model_path, "wb") as f:
                pickle.dump(home_model, f)
                
            with open(away_model_path, "wb") as f:
                pickle.dump(away_model, f)
                
            with open(distribution_path, "w") as f:
                json.dump(score_distribution, f)
            
            # Sauvegarder les encodeurs
            if "encoders" in processed_data:
                encoder_path = os.path.join(models_dir, f"{model_name}_encoders.pkl")
                with open(encoder_path, "wb") as f:
                    pickle.dump(processed_data["encoders"], f)
            
            self.logger.info(f"Modèle de prédiction de score {model_name} sauvegardé")
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde du modèle {model_name}: {e}")
        
        # Résultats
        return {
            "exact_accuracy": exact_accuracy,
            "result_accuracy": result_accuracy,
            "home_error": home_error,
            "away_error": away_error,
            "home_params": home_params,
            "away_params": away_params,
            "most_common_scores": sorted(score_distribution.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    def predict_score(self, match_data, model_name="score_prediction_model"):
        """
        Prédit le score d'un match.
        
        Args:
            match_data: Données du match
            model_name (str): Nom du modèle à utiliser
            
        Returns:
            dict: Prédiction de score
        """
        self.logger.info(f"Prédiction de score avec le modèle {model_name}")
        
        # Charger les modèles si nécessaire
        if model_name not in self.score_models:
            # Essayer de charger les modèles
            models_dir = os.path.join(self.predictive_forge.data_path, "models")
            home_model_path = os.path.join(models_dir, f"{model_name}_home.pkl")
            away_model_path = os.path.join(models_dir, f"{model_name}_away.pkl")
            distribution_path = os.path.join(models_dir, f"{model_name}_distribution.json")
            encoder_path = os.path.join(models_dir, f"{model_name}_encoders.pkl")
            
            if not os.path.exists(home_model_path) or not os.path.exists(away_model_path):
                return {"error": f"Modèle de prédiction de score {model_name} non trouvé"}
            
            try:
                # Charger les modèles
                with open(home_model_path, "rb") as f:
                    home_model = pickle.load(f)
                
                with open(away_model_path, "rb") as f:
                    away_model = pickle.load(f)
                
                # Charger la distribution des scores
                score_distribution = {}
                if os.path.exists(distribution_path):
                    with open(distribution_path, "r") as f:
                        score_distribution = json.load(f)
                
                # Charger les encodeurs
                encoders = None
                if os.path.exists(encoder_path):
                    with open(encoder_path, "rb") as f:
                        encoders = pickle.load(f)
                
                # Stocker les modèles et la distribution
                self.score_models[model_name] = {
                    "home_model": home_model,
                    "away_model": away_model,
                    "encoders": encoders
                }
                
                self.score_distributions[model_name] = score_distribution
                
                self.logger.info(f"Modèle de prédiction de score {model_name} chargé")
            except Exception as e:
                self.logger.error(f"Erreur lors du chargement du modèle {model_name}: {e}")
                return {"error": f"Erreur lors du chargement du modèle: {e}"}
        
        # Vérifier si les modèles sont disponibles
        if model_name not in self.score_models:
            return {"error": f"Modèle de prédiction de score {model_name} non disponible"}
        
        models = self.score_models[model_name]
        home_model = models["home_model"]
        away_model = models["away_model"]
        
        # Convertir en DataFrame si nécessaire
        if isinstance(match_data, dict):
            match_df = pd.DataFrame([match_data])
        else:
            match_df = match_data
        
        # Prétraiter les données
        processed_data = self.predictive_forge.feature_engineer.preprocess_match_data(
            match_df, 
            training=False, 
            encoders=models.get("encoders")
        )
        
        if processed_data is None:
            return {"error": "Échec du prétraitement des données"}
        
        X = processed_data["features"]
        
        # Prédire les scores
        home_scores = home_model.predict(X)
        away_scores = away_model.predict(X)
        
        # Arrondir les scores
        home_scores_rounded = np.round(home_scores).astype(int)
        away_scores_rounded = np.round(away_scores).astype(int)
        
        # Préparer les résultats
        results = []
        for i in range(len(home_scores)):
            # Informations du match
            match_info = match_df.iloc[i].to_dict() if hasattr(match_df, 'iloc') else match_data
            
            # Score prédit
            home_score = max(0, int(home_scores_rounded[i]))
            away_score = max(0, int(away_scores_rounded[i]))
            
            # Calculer les probabilités pour scores voisins
            score_probabilities = {}
            
            # Prédir les probabilités pour les scores voisins
            for h in range(max(0, home_score - 2), home_score + 3):
                for a in range(max(0, away_score - 2), away_score + 3):
                    score = f"{h}-{a}"
                    # Distance au score prédit
                    distance = np.sqrt((h - home_scores[i])**2 + (a - away_scores[i])**2)
                    # Probabilité selon une distribution normale
                    probability = np.exp(-distance)
                    score_probabilities[score] = float(probability)
            
            # Normaliser les probabilités
            total_prob = sum(score_probabilities.values())
            for score in score_probabilities:
                score_probabilities[score] /= total_prob
            
            # Ajouter des probabilités historiques si disponibles
            historical_probabilities = {}
            total_matches = 0
            
            if model_name in self.score_distributions:
                distribution = self.score_distributions[model_name]
                total_matches = sum(distribution.values())
                
                if total_matches > 0:
                    for score, count in distribution.items():
                        historical_probabilities[score] = count / total_matches
            
            # Déterminer le résultat
            if home_score > away_score:
                result = "Victoire domicile"
            elif home_score < away_score:
                result = "Victoire extérieur"
            else:
                result = "Match nul"
            
            # Créer le dictionnaire de prédiction
            prediction = {
                "home_score": home_score,
                "away_score": away_score,
                "predicted_score": f"{home_score}-{away_score}",
                "result": result,
                "score_probabilities": {k: v for k, v in sorted(score_probabilities.items(), key=lambda x: x[1], reverse=True)[:5]},
                "raw_home_score": float(home_scores[i]),
                "raw_away_score": float(away_scores[i])
            }
            
            # Ajouter les probabilités historiques si disponibles
            if historical_probabilities:
                prediction["historical_probabilities"] = {k: v for k, v in sorted(historical_probabilities.items(), key=lambda x: x[1], reverse=True)[:5]}
            
            results.append(prediction)
        
        # Si une seule prédiction, retourner directement
        if len(results) == 1:
            return results[0]
        
        return {"predictions": results}