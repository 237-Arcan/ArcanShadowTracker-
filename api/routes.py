"""
Module de routes API pour ArcanShadow.
Fournit les endpoints API pour la future application mobile.
"""

import logging
import json
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Créer le blueprint API
api_blueprint = Blueprint('api', __name__)

# Importer le hub d'intégration pour accéder aux données
try:
    from api.data_integration_hub import DataIntegrationHub
    data_hub = DataIntegrationHub()
    DATA_HUB_AVAILABLE = True
    logger.info("Hub d'intégration disponible pour les routes API")
except Exception as e:
    logger.error(f"Erreur lors de l'initialisation du hub d'intégration: {e}")
    DATA_HUB_AVAILABLE = False

@api_blueprint.route('/status', methods=['GET'])
def api_status():
    """Endpoint pour vérifier le statut de l'API"""
    if DATA_HUB_AVAILABLE:
        # Obtenir le statut des différentes sources de données
        sources_status = data_hub.sources_status
        
        # Générer une réponse détaillée
        response = {
            "status": "online",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "sources": sources_status,
            "features": {
                "real_time_data": sources_status.get('football_api', False),
                "time_module": sources_status.get('time_module', False),
                "mobile_ready": sources_status.get('cross_platform', False)
            }
        }
    else:
        # Réponse de base si le hub n'est pas disponible
        response = {
            "status": "limited",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "message": "Hub d'intégration non disponible"
        }
    
    return jsonify(response)

@api_blueprint.route('/matches', methods=['GET'])
def get_matches():
    """Endpoint pour récupérer les matchs"""
    if not DATA_HUB_AVAILABLE:
        return jsonify({"error": "Service non disponible"}), 503
    
    try:
        # Récupérer les paramètres de la requête
        days_ahead = request.args.get('days', default=3, type=int)
        leagues = request.args.get('leagues', default=None)
        platform = request.args.get('platform', default='mobile')
        
        # Convertir les leagues en liste si spécifié
        if leagues:
            leagues = [int(l) for l in leagues.split(',')]
        
        # Récupérer les matchs via le hub d'intégration
        matches = data_hub.get_upcoming_matches(days_ahead=days_ahead, leagues=leagues)
        
        # Préparer les données pour l'application
        matches_for_app = data_hub.prepare_matches_for_app(matches, platform)
        
        # Ajouter des métadonnées
        response = {
            "count": len(matches_for_app),
            "platform": platform,
            "timestamp": datetime.now().isoformat(),
            "expires": (datetime.now() + timedelta(minutes=10)).isoformat(),
            "data": matches_for_app
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des matchs: {e}")
        return jsonify({"error": "Erreur serveur", "message": str(e)}), 500

@api_blueprint.route('/match/<match_id>', methods=['GET'])
def get_match_details(match_id):
    """Endpoint pour récupérer les détails d'un match spécifique"""
    if not DATA_HUB_AVAILABLE:
        return jsonify({"error": "Service non disponible"}), 503
    
    try:
        platform = request.args.get('platform', default='mobile')
        
        # Simuler la récupération d'un match spécifique
        # Dans une implémentation réelle, cela appellerait une méthode du hub
        # pour récupérer les détails du match via son ID
        
        # Pour l'instant, générer des données simulées
        if DATA_HUB_AVAILABLE and data_hub.sources_status.get('football_api', False):
            # Récupérer le match via l'API Football
            matches = data_hub.get_upcoming_matches(days_ahead=7)
            match = next((m for m in matches if str(m.get('id')) == str(match_id)), None)
            
            if not match:
                return jsonify({"error": "Match non trouvé"}), 404
                
            # Enrichir les données du match
            # Ici, nous aurions plus de détails comme les statistiques, etc.
            match['detailed'] = True
            
            # Préparer pour l'application
            match_for_app = data_hub.prepare_matches_for_app([match], platform)[0]
            
            # Ajouter des prédictions
            match_for_app['predictions'] = {
                'home_win': 0.45,
                'draw': 0.30,
                'away_win': 0.25,
                'confidence': 0.75,
                'value_detected': False
            }
            
            return jsonify(match_for_app)
        else:
            return jsonify({"error": "Données non disponibles"}), 503
            
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des détails du match: {e}")
        return jsonify({"error": "Erreur serveur", "message": str(e)}), 500

@api_blueprint.route('/predictions', methods=['GET'])
def get_predictions():
    """Endpoint pour récupérer les prédictions des matchs"""
    if not DATA_HUB_AVAILABLE:
        return jsonify({"error": "Service non disponible"}), 503
    
    try:
        # Récupérer les paramètres
        days_ahead = request.args.get('days', default=1, type=int)
        platform = request.args.get('platform', default='mobile')
        
        # Récupérer les matchs
        matches = data_hub.get_upcoming_matches(days_ahead=days_ahead)
        
        # Préparer une liste de prédictions
        predictions = []
        
        for match in matches:
            # Dans une implémentation réelle, nous utiliserions le moteur de prédiction XGBoost
            # Pour l'instant, générer des données simulées
            prediction = {
                'match_id': match.get('id'),
                'home_team': match.get('home_team'),
                'away_team': match.get('away_team'),
                'date': match.get('date'),
                'league_id': match.get('league_id'),
                'league_name': match.get('league_name'),
                'probabilities': {
                    'home_win': round(0.4 + 0.2 * (random.random() - 0.5), 2),
                    'draw': round(0.3 + 0.15 * (random.random() - 0.5), 2),
                    'away_win': round(0.3 + 0.15 * (random.random() - 0.5), 2)
                },
                'recommended_bet': None,
                'confidence': round(0.6 + 0.3 * random.random(), 2),
                'value_detected': random.random() > 0.8
            }
            
            # Déterminer le pari recommandé
            probs = prediction['probabilities']
            max_prob = max(probs.values())
            if max_prob == probs['home_win']:
                prediction['recommended_bet'] = 'home_win'
            elif max_prob == probs['draw']:
                prediction['recommended_bet'] = 'draw'
            else:
                prediction['recommended_bet'] = 'away_win'
                
            predictions.append(prediction)
        
        # Préparer les données pour l'application
        predictions_for_app = data_hub.prepare_matches_for_app(predictions, platform)
        
        # Réponse complète
        response = {
            "count": len(predictions_for_app),
            "platform": platform,
            "timestamp": datetime.now().isoformat(),
            "data": predictions_for_app
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des prédictions: {e}")
        return jsonify({"error": "Erreur serveur", "message": str(e)}), 500

@api_blueprint.route('/config', methods=['GET'])
def get_app_config():
    """Endpoint pour récupérer la configuration de l'application"""
    try:
        platform = request.args.get('platform', default='mobile')
        
        if DATA_HUB_AVAILABLE:
            # Générer la configuration via le hub
            config = data_hub.generate_app_configuration(platform)
        else:
            # Configuration de base
            config = {
                "version": "1.0.0",
                "api_url": "/api",
                "refresh_interval": 300,
                "features": {
                    "offline_mode": True,
                    "dark_mode": True
                }
            }
        
        # Ajouter des métadonnées
        config["generated_at"] = datetime.now().isoformat()
        config["expires_at"] = (datetime.now() + timedelta(days=1)).isoformat()
        
        return jsonify(config)
        
    except Exception as e:
        logger.error(f"Erreur lors de la génération de la configuration: {e}")
        return jsonify({"error": "Erreur serveur", "message": str(e)}), 500