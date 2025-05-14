"""
Translations module for the ArcanShadow application.
Provides text content in multiple languages.
"""

# English translations
en = {
    # General
    "app_title": "ArcanShadow - Hybrid Sports Prediction System",
    "app_subtitle": "Hybrid Prediction System: Statistics + Esoteric Analysis + Odds Behavior",
    
    # Sidebar
    "system_controls": "System Controls",
    "select_sport": "Select Sport",
    "select_league": "Select League",
    "select_date": "Select Date",
    "select_language": "Select Language",
    "active_modules": "Active Modules",
    "advanced_settings": "Advanced Settings",
    "confidence_threshold": "Confidence Threshold",
    "cycles_depth": "Historical Cycles Depth",
    "esoteric_influence": "Esoteric Influence Weight",
    "generate_predictions": "Generate Predictions",
    "todays_matches": "Today's Matches",
    "upcoming_matches": "Upcoming Matches",
    "featured_matches": "Featured Matches",
    "no_matches_today": "No matches today for selected sport and league",
    "no_upcoming_matches": "No upcoming matches in the next 7 days",
    
    # Tab titles
    "predictions_tab": "Predictions",
    "dashboard_tab": "System Dashboard",
    "historical_tab": "Historical Analysis",
    "module_details_tab": "Module Details",
    "live_match_tab": "Live Match 🔴",
    "live_monitoring_tab": "Live Monitoring 🔄",
    "performance_notifications_tab": "Performance Notifications 📊",
    "daily_combo_tab": "Daily Combo 🎯",
    "smart_recommendations_title": "Smart Recommendations 🎲",
    "notifications_center": "Notifications Center",
    "live_match_monitoring": "Live Match Monitoring",
    
    # Daily Combo Tab
    "daily_combo_title": "Daily Betting Combo",
    "daily_combo_description": "Automatically generated betting selections based on module analyses and predictions",
    "market_selection": "Market Selection",
    "betting_markets": "Betting Markets",
    "recommended_bets": "Recommended Bets",
    "bet_confidence": "Confidence",
    "bet_odds": "Odds",
    "bet_market": "Market",
    
    # Smart Market Recommendations
    "smart_recommendations_title": "Smart Market Recommendations",
    "smart_recommendations_description": "Personalized market recommendations based on your betting history and preferences",
    "your_betting_history": "Your Betting History",
    "preferred_markets": "Your Preferred Markets",
    "recommended_markets": "Recommended Markets for You",
    "market_preference_score": "Preference Score",
    "market_success_rate": "Success Rate",
    "no_betting_history": "No betting history found. Start placing bets to get personalized recommendations.",
    "add_bet_button": "Add New Bet",
    "recommendation_reason": "Recommendation Reason",
    "match_details": "Match Details",
    "view_all_recommendations": "View All Recommendations",
    "filter_recommendations": "Filter Recommendations",
    "overall_performance": "Overall Performance",
    "bet_selection": "Selection",
    "total_combo_odds": "Total Combo Odds",
    "potential_return": "Potential Return",
    "expected_value": "Expected Value",
    "module_source": "Source Module",
    "key_insights": "Key Insights",
    "risk_assessment": "Risk Assessment",
    "probability_rating": "Probability Rating",
    "add_to_combo": "Add to Combo",
    "remove_from_combo": "Remove",
    "clear_combo": "Clear Combo",
    "no_recommendations": "No recommendations available for current matches",
    "use_top_modules": "Use top-performing modules only",
    "top_modules_help": "When enabled, only predictions from modules with a success rate above 60% will be used",
    "top_modules_active": "Using {count} predictions from top-performing modules: {modules}...",
    "no_top_modules_data": "No predictions from top-performing modules currently available",
    
    # Predictions tab
    "match_predictions": "Match Predictions",
    "predictions_description": "Predictions generated using ArcanShadow's multi-layer architecture combining statistical data, esoteric patterns, and odds behavior analysis.",
    "vs": "vs",
    "date": "Date",
    "prediction": "Prediction",
    "confidence": "Confidence",
    "view_details": "View Prediction Details",
    "statistical_factors": "Statistical Factors",
    "esoteric_factors": "Esoteric Factors",
    "odds_analysis": "Odds Analysis",
    "no_predictions": "Click 'Generate Predictions' in the sidebar to analyze upcoming matches.",
    "no_matches": "No upcoming matches found for {league} on {date}.",
    
    # Enhanced predictions tab
    "prediction_filters": "Intelligent Filters",
    "prediction_type": "Prediction Type",
    "all_predictions": "All Predictions",
    "high_confidence_only": "High Confidence Only",
    "value_bets_only": "Value Bets Only",
    "contrarian_picks": "Contrarian Picks",
    "min_confidence": "Min. Confidence",
    "min_factors": "Min. Confirming Factors",
    "analyzing_matches": "Analyzing Matches",
    "matches_found": "Matches Found",
    "no_matches_criteria": "No matches match your current filter criteria",
    "detailed_predictions": "Detailed Predictions",
    "deep_analysis": "Deep Analysis",
    "odds": "Odds",
    "match": "Match",
    "time": "Time", 
    "value": "Value",
    "contrarian": "Contrarian",
    "value_bet": "Value Bet",
    "contrarian_pick": "Contrarian Pick",
    "prediction_summary": "Prediction Summary",
    
    # Dashboard tab
    "system_dashboard": "System Dashboard",
    "dashboard_description": "Real-time monitoring of ArcanShadow's performance and module activities.",
    "prediction_accuracy": "Prediction Accuracy (7d)",
    "arcanx_confidence": "ArcanX Confidence",
    "shadowodds_accuracy": "ShadowOdds Accuracy",
    "active_modules_count": "Active Modules",
    "system_health": "System Health & Performance",
    "system_activity": "System Activity Timeline",
    
    # Historical tab
    "historical_analysis": "Historical Analysis",
    "historical_description": "Review past predictions and performance metrics to improve future forecasts.",
    "sport": "Sport",
    "league": "League",
    "time_period": "Time Period",
    "performance_summary": "Prediction Performance Summary",
    "overall_accuracy": "Overall Accuracy",
    "roi": "ROI",
    "predictions_made": "Predictions Made",
    "module_performance": "Module Performance Over Time",
    "recent_predictions": "Recent Predictions",
    "match": "Match",
    "result": "Result",
    "correct": "Correct",
    "no_recent_data": "No recent prediction data available for the selected filters.",
    "no_historical_data": "No historical data available for the selected criteria.",
    
    # Module details tab
    "module_details": "Module Details",
    "module_description": "Explore the inner workings of ArcanShadow's prediction modules.",
    "select_module": "Select Module",
    "module_category": "Module Category",
    "specific_module": "Specific Module",
    "module_info": "Module Information",
    "performance_metrics": "Performance Metrics",
    "module_relationships": "Module Relationships",
    "module_interactions": "How {module} interacts with other components of ArcanShadow.",
    
    # Module descriptions
    "module_description_bettrapmap": "Maps betting trap zones and identifies safe markets based on odds anomalies and betting patterns.",
    "module_description_stadiumspirit": "Analyzes stadium energy, aura and vibrational memory to determine venue influence on matches.",
    "module_description_numericode": "Interprets numérological patterns in dates, jersey numbers, cycles, scores and calendar days.",
    "module_description_gematriapulse": "Analyzes kabbalistic values of team names, players, cities, stadiums, and competitions.",
    "module_description_astroimpact": "Analyzes celestial positions and their influence on specific matches and teams.",
    "module_description_tarotecho": "Applies tarot symbolism to evaluate the energy and potential outcomes of matches.",
    "module_description_yiflow": "Uses I Ching hexagrams to analyze the flow of energy in sporting contests.",
    "module_description_karmicflow": "Detects karmic patterns in team histories and confrontations.",
    "module_description_radiesthesiamap": "Measures energy fields of venues and their impact on team performance.",
    "module_description_cyclemirror": "Identifies cyclical patterns in match histories between teams.",
    "module_description_linetrap": "Identifies trapped odds that are misaligned with actual sport dynamics.",
    "module_description_betpulse": "Analyzes betting volume and timing patterns to detect significant market moves.",
    "module_description_crowdpressure": "Monitors excessive public betting on one side that can distort odds.",
    "module_description_marketecho": "Analyzes discrepancies between bookmakers and suspicious movements.",
    "module_description_collapsedetektor": "Detects signs that a team may be about to dramatically underperform.",
    "module_description_shadowmomentum": "Identifies subtle momentum shifts in betting patterns before they become obvious.",
    "module_description_settrapindicator": "Evaluates whether bookmakers may be setting a trap for public bettors.",
    
    # Module inputs/outputs
    "module_inputs": "Inputs",
    "module_output": "Output",
    "module_accuracy": "Historical Accuracy",
    "description": "Description",
    
    # Prediction outcomes
    "home_win": "Home Win",
    "away_win": "Away Win",
    "draw": "Draw",
    "over_goals": "Over {value} Goals",
    "under_goals": "Under {value} Goals",
    "btts_yes": "Both Teams To Score: Yes",
    "btts_no": "Both Teams To Score: No",
    
    # Prediction factors
    "form_analysis": "Form Analysis",
    "head_to_head": "Head-to-Head Record",
    "home_advantage": "Home Advantage",
    "injury_impact": "Injury Impact",
    "recent_momentum": "Recent Momentum",
    "numerical_resonance": "Numerical Resonance",
    "gematria_value": "Gematria Value",
    "astrological_position": "Astrological Position",
    "tarot_association": "Tarot Association",
    "karmic_balance": "Karmic Balance",
    "venue_energy": "Venue Energy",
    "cycle_pattern": "Cycle Pattern",
    "line_movement": "Line Movement",
    "public_betting": "Public Betting %",
    "sharp_action": "Sharp Action",
    "odds_divergence": "Odds Divergence",
    "market_overreaction": "Market Overreaction",
    "trap_indicator": "Trap Indicator",
    
    # Time periods
    "last_7_days": "Last 7 days",
    "last_30_days": "Last 30 days",
    "last_3_months": "Last 3 months",
    "last_6_months": "Last 6 months",
    "last_year": "Last year",
    
    # Live match mode
    "live_mode_title": "Live Match Analysis",
    "live_mode_description": "Real-time match analysis with ArcanSentinel",
    "match_setup": "Match Setup",
    "home_team": "Home Team",
    "away_team": "Away Team",
    "start_tracking": "Start Live Tracking",
    "stop_tracking": "Stop Live Tracking",
    "current_minute": "Current Minute",
    "update_match_state": "Update Match State",
    "current_score": "Current Score",
    "add_event": "Add Match Event",
    "event_type": "Event Type",
    "event_details": "Event Details",
    "live_analysis": "Live Analysis",
    "active_modules": "Active Modules",
    "match_phase": "Match Phase",
    "prediction_evolution": "Prediction Evolution",
    "key_factors": "Key Factors",
    "momentum_analysis": "Momentum Analysis",
    "betting_trends": "Betting Trends",
    "karmic_patterns": "Karmic Patterns",
    
    # ArcanX factor explanations
    "prime_match_day": "Prime Match Day: Match occurs on day {day}, a prime number",
    "dynamic_life_path": "Dynamic Life Path: Match Life Path {number} suggests action/change",
    "earth_element_match": "Earth Element Match: Match under Taurus - stable, defensive",
    "full_moon_energy": "Full Moon Energy: Match near Full Moon - heightened energy",
    "match_foundation_sun": "Match Foundation: The Sun: Success, vitality, positive outcome",
    "current_energy_moon": "Current Energy: The Moon: Illusion, deception, uncertainty",
    "outcome_tendency_fool": "Outcome Tendency: The Fool: Unpredictable outcome, new beginnings",
    
    # Smart Recommendations Tab
    "smart_recommendations_description": "Get personalized betting market recommendations based on your betting history and preferences",
    "recommended_markets": "Recommended Markets",
    "preferred_markets": "Your Preferred Markets",
    "your_betting_history": "Your Betting History",
    "market_preference_score": "Preference Score",
    "market_success_rate": "Success Rate",
    "no_betting_history": "No betting history found. Add some bets to get recommendations.",
    "add_bet_button": "Add Sample Betting History",
    "recommendation_reason": "Reason",
    "overall_performance": "Overall Performance"
}

# French translations
fr = {
    # General
    "app_title": "ArcanShadow - Système Hybride de Prédiction Sportive",
    "app_subtitle": "Système de Prédiction Hybride: Statistiques + Analyse Ésotérique + Comportement des Cotes",
    
    # Sidebar
    "system_controls": "Contrôles du Système",
    "select_sport": "Sélectionner un Sport",
    "select_league": "Sélectionner une Ligue",
    "select_date": "Sélectionner une Date",
    "select_language": "Sélectionner une Langue",
    "active_modules": "Modules Actifs",
    "advanced_settings": "Paramètres Avancés",
    "confidence_threshold": "Seuil de Confiance",
    "cycles_depth": "Profondeur des Cycles Historiques",
    "esoteric_influence": "Poids de l'Influence Ésotérique",
    "generate_predictions": "Générer les Prédictions",
    "todays_matches": "Matchs du Jour",
    "upcoming_matches": "Matchs à Venir",
    "featured_matches": "Matchs Vedettes",
    "no_matches_today": "Aucun match aujourd'hui pour le sport et la ligue sélectionnés",
    "no_upcoming_matches": "Aucun match à venir dans les 7 prochains jours",
    
    # Tab titles
    "predictions_tab": "Prédictions",
    "dashboard_tab": "Tableau de Bord",
    "historical_tab": "Analyse Historique",
    "module_details_tab": "Détails des Modules",
    "live_match_tab": "Match en Direct 🔴",
    "live_monitoring_tab": "Surveillance en Direct 🔄",
    "performance_notifications_tab": "Notifications de Performance 📊",
    "daily_combo_tab": "Combiné du Jour 🎯",
    "notifications_center": "Centre de Notifications",
    "live_match_monitoring": "Surveillance de Match en Direct",
    
    # Daily Combo Tab
    "daily_combo_title": "Combiné du Jour",
    "daily_combo_description": "Sélections de paris générées automatiquement sur la base des analyses et prédictions des modules",
    "market_selection": "Sélection de Marché",
    "betting_markets": "Marchés de Paris",
    "recommended_bets": "Paris Recommandés",
    "bet_confidence": "Confiance",
    "bet_odds": "Cotes",
    "bet_market": "Marché",
    "bet_selection": "Sélection",
    "total_combo_odds": "Cote Totale du Combiné",
    "potential_return": "Gain Potentiel",
    "expected_value": "Valeur Espérée",
    "module_source": "Module Source",
    "key_insights": "Insights Clés",
    "risk_assessment": "Évaluation du Risque",
    "probability_rating": "Indice de Probabilité",
    "add_to_combo": "Ajouter au Combiné",
    "remove_from_combo": "Retirer",
    "clear_combo": "Vider le Combiné",
    "no_recommendations": "Aucune recommandation disponible pour les matchs actuels",
    
    # Smart Market Recommendations (French)
    "smart_recommendations_title": "Recommandations Intelligentes de Marchés",
    "smart_recommendations_description": "Recommandations personnalisées de marchés basées sur votre historique et préférences de paris",
    "your_betting_history": "Votre Historique de Paris",
    "preferred_markets": "Vos Marchés Préférés",
    "recommended_markets": "Marchés Recommandés Pour Vous",
    "market_preference_score": "Score de Préférence",
    "market_success_rate": "Taux de Réussite",
    "no_betting_history": "Aucun historique de paris trouvé. Commencez à placer des paris pour obtenir des recommandations personnalisées.",
    "add_bet_button": "Ajouter un Nouveau Pari",
    "recommendation_reason": "Raison de la Recommandation",
    "match_details": "Détails du Match",
    "view_all_recommendations": "Voir Toutes les Recommandations",
    "filter_recommendations": "Filtrer les Recommandations",
    "overall_performance": "Performance Globale",
    "use_top_modules": "Utiliser uniquement les modules performants",
    "top_modules_help": "Lorsque cette option est activée, seules les prédictions des modules ayant un taux de réussite supérieur à 60% sont utilisées",
    "top_modules_active": "Utilisation des {count} prédictions des modules les plus performants: {modules}...",
    "no_top_modules_data": "Aucune prédiction des modules performants disponible actuellement",
    
    # Predictions tab
    "match_predictions": "Prédictions de Matches",
    "predictions_description": "Prédictions générées en utilisant l'architecture multi-couches d'ArcanShadow combinant données statistiques, modèles ésotériques et analyse du comportement des cotes.",
    "vs": "contre",
    "date": "Date",
    "prediction": "Prédiction",
    "confidence": "Confiance",
    "view_details": "Voir les Détails de la Prédiction",
    "statistical_factors": "Facteurs Statistiques",
    "esoteric_factors": "Facteurs Ésotériques",
    "odds_analysis": "Analyse des Cotes",
    "no_predictions": "Cliquez sur 'Générer les Prédictions' dans la barre latérale pour analyser les matchs à venir.",
    "no_matches": "Aucun match à venir trouvé pour {league} le {date}.",
    
    # Enhanced predictions tab
    "prediction_filters": "Filtres Intelligents",
    "prediction_type": "Type de Prédiction",
    "all_predictions": "Toutes les Prédictions",
    "high_confidence_only": "Haute Confiance Uniquement",
    "value_bets_only": "Paris à Valeur Uniquement",
    "contrarian_picks": "Sélections Contraires",
    "min_confidence": "Confiance Min.",
    "min_factors": "Facteurs de Confirmation Min.",
    "analyzing_matches": "Analyse des Matchs",
    "matches_found": "Matchs Trouvés",
    "no_matches_criteria": "Aucun match ne correspond à vos critères de filtre actuels",
    "detailed_predictions": "Prédictions Détaillées",
    "deep_analysis": "Analyse Approfondie",
    "odds": "Cotes",
    "match": "Match",
    "time": "Heure", 
    "value": "Valeur",
    "contrarian": "Contraire",
    "value_bet": "Paris à Valeur",
    "contrarian_pick": "Choix Contraire",
    "prediction_summary": "Résumé des Prédictions",
    
    # Dashboard tab
    "system_dashboard": "Tableau de Bord du Système",
    "dashboard_description": "Suivi en temps réel des performances et activités des modules d'ArcanShadow.",
    "prediction_accuracy": "Précision des Prédictions (7j)",
    "arcanx_confidence": "Confiance d'ArcanX",
    "shadowodds_accuracy": "Précision de ShadowOdds",
    "active_modules_count": "Modules Actifs",
    "system_health": "Santé et Performance du Système",
    "system_activity": "Chronologie d'Activité du Système",
    
    # Historical tab
    "historical_analysis": "Analyse Historique",
    "historical_description": "Examinez les prédictions passées et les métriques de performance pour améliorer les prévisions futures.",
    "sport": "Sport",
    "league": "Ligue",
    "time_period": "Période",
    "performance_summary": "Résumé des Performances de Prédiction",
    "overall_accuracy": "Précision Globale",
    "roi": "ROI",
    "predictions_made": "Prédictions Effectuées",
    "module_performance": "Performance des Modules dans le Temps",
    "recent_predictions": "Prédictions Récentes",
    "match": "Match",
    "result": "Résultat",
    "correct": "Correct",
    "no_recent_data": "Aucune donnée de prédiction récente disponible pour les filtres sélectionnés.",
    "no_historical_data": "Aucune donnée historique disponible pour les critères sélectionnés.",
    
    # Module details tab
    "module_details": "Détails des Modules",
    "module_description": "Explorez le fonctionnement interne des modules de prédiction d'ArcanShadow.",
    "select_module": "Sélectionner un Module",
    "module_category": "Catégorie de Module",
    "specific_module": "Module Spécifique",
    "module_info": "Informations sur le Module",
    "performance_metrics": "Métriques de Performance",
    "module_relationships": "Relations entre Modules",
    "module_interactions": "Comment {module} interagit avec les autres composants d'ArcanShadow.",
    
    # Module descriptions
    "module_description_bettrapmap": "Cartographie les zones de pièges à mise et identifie les marchés sûrs basés sur les anomalies de cotes et les schémas de paris.",
    "module_description_stadiumspirit": "Analyse l'énergie des stades, leur aura et leur mémoire vibratoire pour déterminer l'influence du lieu sur les matchs.",
    "module_description_numericode": "Interprète les schémas numériques dans les dates, numéros de maillot, cycles, scores et jours calendaires.",
    "module_description_gematriapulse": "Analyse les valeurs kabbalistiques des noms d'équipes, de joueurs, de villes, de stades et de compétitions.",
    "module_description_astroimpact": "Analyse les positions célestes et leur influence sur des matchs et des équipes spécifiques.",
    "module_description_tarotecho": "Applique le symbolisme du tarot pour évaluer l'énergie et les résultats potentiels des matchs.",
    "module_description_yiflow": "Utilise les hexagrammes du Yi King pour analyser le flux d'énergie dans les compétitions sportives.",
    "module_description_karmicflow": "Détecte les schémas karmiques dans les historiques d'équipes et les confrontations.",
    "module_description_radiesthesiamap": "Mesure les champs énergétiques des lieux et leur impact sur la performance des équipes.",
    "module_description_cyclemirror": "Identifie les schémas cycliques dans les historiques de matchs entre équipes.",
    "module_description_linetrap": "Identifie les cotes pièges qui sont en décalage avec la dynamique sportive réelle.",
    "module_description_betpulse": "Analyse le volume et les schémas temporels des paris pour détecter les mouvements significatifs du marché.",
    "module_description_crowdpressure": "Surveille les paris publics excessifs sur un côté qui peuvent fausser les cotes.",
    "module_description_marketecho": "Analyse les écarts entre les bookmakers et les mouvements suspects.",
    "module_description_collapsedetektor": "Détecte les signes qu'une équipe pourrait être sur le point de sous-performer dramatiquement.",
    "module_description_shadowmomentum": "Identifie les changements subtils de momentum dans les schémas de paris avant qu'ils ne deviennent évidents.",
    "module_description_settrapindicator": "Évalue si les bookmakers pourraient être en train de tendre un piège aux parieurs publics.",
    
    # Module inputs/outputs
    "module_inputs": "Entrées",
    "module_output": "Sortie",
    "module_accuracy": "Précision Historique",
    "description": "Description",
    
    # Prediction outcomes
    "home_win": "Victoire à Domicile",
    "away_win": "Victoire à l'Extérieur",
    "draw": "Match Nul",
    "over_goals": "Plus de {value} Buts",
    "under_goals": "Moins de {value} Buts",
    "btts_yes": "Les Deux Équipes Marquent: Oui",
    "btts_no": "Les Deux Équipes Marquent: Non",
    
    # Prediction factors
    "form_analysis": "Analyse de Forme",
    "head_to_head": "Historique des Confrontations",
    "home_advantage": "Avantage du Terrain",
    "injury_impact": "Impact des Blessures",
    "recent_momentum": "Dynamique Récente",
    "numerical_resonance": "Résonance Numérique",
    "gematria_value": "Valeur Gématrique",
    "astrological_position": "Position Astrologique",
    "tarot_association": "Association du Tarot",
    "karmic_balance": "Équilibre Karmique",
    "venue_energy": "Énergie du Stade",
    "cycle_pattern": "Motif Cyclique",
    "line_movement": "Mouvement des Cotes",
    "public_betting": "Paris Publics %",
    "sharp_action": "Action des Parieurs Pro",
    "odds_divergence": "Divergence des Cotes",
    "market_overreaction": "Surréaction du Marché",
    "trap_indicator": "Indicateur de Piège",
    
    # Time periods
    "last_7_days": "7 derniers jours",
    "last_30_days": "30 derniers jours",
    "last_3_months": "3 derniers mois",
    "last_6_months": "6 derniers mois",
    "last_year": "Année dernière",
    
    # Live match mode
    "live_mode_title": "Analyse de Match en Direct",
    "live_mode_description": "Analyse en temps réel avec ArcanSentinel",
    "match_setup": "Configuration du Match",
    "home_team": "Équipe à Domicile",
    "away_team": "Équipe Visiteuse",
    "start_tracking": "Démarrer le Suivi en Direct",
    "stop_tracking": "Arrêter le Suivi en Direct",
    "current_minute": "Minute Actuelle",
    "update_match_state": "Mettre à Jour l'État du Match",
    "current_score": "Score Actuel",
    "add_event": "Ajouter un Événement",
    "event_type": "Type d'Événement",
    "event_details": "Détails de l'Événement",
    "live_analysis": "Analyse en Direct",
    "active_modules": "Modules Actifs",
    "match_phase": "Phase du Match",
    "prediction_evolution": "Évolution de la Prédiction",
    "key_factors": "Facteurs Clés",
    "momentum_analysis": "Analyse de l'Élan",
    "betting_trends": "Tendances des Paris",
    "karmic_patterns": "Modèles Karmiques",
    
    # Performance Notifications tab
    "performance_evaluations": "Évaluations de Performance",
    "performance_notifications_description": "Synthèse des prédictions pré-match confrontées aux statistiques post-match pour évaluer la performance des modules.",
    "select_completed_match": "Sélectionner un Match Terminé",
    "prediction_vs_reality": "Prédiction vs Réalité",
    "module_evaluations": "Évaluations des Modules",
    "module_name": "Nom du Module",
    "prediction_accuracy": "Précision de Prédiction",
    "performance_score": "Score de Performance",
    "performance_trend": "Tendance de Performance",
    "key_success_factors": "Facteurs Clés de Succès",
    "key_failure_factors": "Facteurs Clés d'Échec",
    "module_improvement_suggestions": "Suggestions d'Amélioration",
    "match_overview": "Aperçu du Match",
    "predicted_outcome": "Résultat Prédit",
    "actual_outcome": "Résultat Réel",
    "prediction_error": "Erreur de Prédiction",
    "prediction_timeline": "Chronologie de Prédiction",
    "no_completed_matches": "Aucun match terminé disponible pour évaluation",
    
    # ArcanX factor explanations
    "prime_match_day": "Jour de Match Premier: Le match a lieu le jour {day}, un nombre premier",
    "dynamic_life_path": "Chemin de Vie Dynamique: Le chemin de vie du match {number} suggère action/changement",
    "earth_element_match": "Élément Terre du Match: Match sous Taurus - stable, défensif",
    "full_moon_energy": "Énergie Pleine Lune: Match près de la Pleine Lune - énergie amplifiée",
    "match_foundation_sun": "Fondation du Match: Le Soleil: Succès, vitalité, résultat positif",
    "current_energy_moon": "Énergie Actuelle: La Lune: Illusion, tromperie, incertitude",
    "outcome_tendency_fool": "Tendance du Résultat: Le Fou: Résultat imprévisible, nouveaux départs",
    
    # Smart Recommendations Tab
    "smart_recommendations_title": "Recommandations Intelligentes 🎲",
    "smart_recommendations_description": "Obtenez des recommandations personnalisées de marchés de paris basées sur votre historique et vos préférences",
    "recommended_markets": "Marchés Recommandés",
    "preferred_markets": "Vos Marchés Préférés",
    "your_betting_history": "Votre Historique de Paris",
    "market_preference_score": "Score de Préférence",
    "market_success_rate": "Taux de Réussite",
    "no_betting_history": "Aucun historique de paris trouvé. Ajoutez des paris pour obtenir des recommandations.",
    "add_bet_button": "Ajouter un Historique de Paris",
    "recommendation_reason": "Raison",
    "overall_performance": "Performance Globale"
}

# Dictionary to access translations
translations = {
    "en": en,
    "fr": fr
}

# Function to get text in the selected language
def get_text(key, language="en", **format_args):
    """
    Get text in the specified language.
    
    Args:
        key (str): The translation key
        language (str): Language code ('en' or 'fr')
        **format_args: Format arguments for string interpolation
        
    Returns:
        str: Translated text
    """
    if language not in translations:
        language = "en"  # Fallback to English
        
    if key not in translations[language]:
        # Fallback to the English version if the key is missing in the selected language
        if key in translations["en"]:
            text = translations["en"][key]
        else:
            return key  # Return the key itself if it doesn't exist
    else:
        text = translations[language][key]
    
    # Apply formatting if format arguments are provided
    if format_args:
        try:
            text = text.format(**format_args)
        except KeyError:
            pass  # Ignore formatting errors
            
    return text