"""
D-Forge - Adaptive module generation system for ArcanShadow.
Creates new modules in response to recurring patterns and system needs.
"""

import numpy as np
import random
from datetime import datetime, timedelta
import json
import os
import hashlib
import sqlite3

class DForge:
    """
    D-Forge - Adaptive module generation system for ArcanShadow.
    Dynamically creates and deploys new analysis modules based on system needs.
    """
    
    def __init__(self, arcan_reflex=None, meta_systems=None):
        """
        Initialize the D-Forge module with necessary components.
        
        Args:
            arcan_reflex: Reference to ArcanReflex module for performance data
            meta_systems: Reference to MetaSystems for system integration
        """
        # Store module references
        self.arcan_reflex = arcan_reflex
        self.meta_systems = meta_systems
        
        # Configuration
        self.creation_threshold = 0.75  # Minimum confidence to create a new module
        self.pattern_recognition_threshold = 5  # Minimum occurrences to recognize a pattern
        
        # Module templates
        self.module_templates = self._initialize_module_templates()
        
        # Module deployment settings
        self.staging_time = 10  # Days to test a module before full deployment
        
        # Active forge operations
        self.active_forges = []
        
        # Generated modules history
        self.generated_modules = self._load_generated_modules()
        
        # Module creation limiter
        self.max_modules_per_month = 3
        self.recent_creations = []
        
        # Pattern recognition
        self.observed_patterns = {}
    
    def detect_needs(self, performance_data=None, system_state=None):
        """
        Detect system needs that could be addressed by new modules.
        
        Args:
            performance_data (dict, optional): Recent performance data
            system_state (dict, optional): Current system state
            
        Returns:
            dict: Detected needs and potential module candidates
        """
        needs = []
        
        # If we have ArcanReflex data, use its suggestions
        if self.arcan_reflex:
            reflex_suggestions = self.arcan_reflex.suggest_new_modules(performance_data)
            for suggestion in reflex_suggestions.get('suggestions', []):
                needs.append({
                    'type': suggestion.get('module_type', 'unknown'),
                    'target': suggestion.get('target', ''),
                    'priority': suggestion.get('priority', 0.5),
                    'rationale': suggestion.get('rationale', 'Suggested by ArcanReflex'),
                    'source': 'arcan_reflex'
                })
        
        # Analyze performance gaps
        if performance_data:
            gap_needs = self._detect_performance_gaps(performance_data)
            needs.extend(gap_needs)
        
        # Detect emerging patterns
        pattern_needs = self._detect_emerging_patterns(system_state)
        needs.extend(pattern_needs)
        
        # Check for geographic coverage gaps
        geographic_needs = self._detect_geographic_gaps()
        needs.extend(geographic_needs)
        
        # Calculate potential module candidates
        candidates = []
        
        for need in needs:
            # Match need with appropriate module templates
            matched_templates = self._match_templates_to_need(need)
            
            for template in matched_templates:
                # Calculate fitness score for this template
                fitness = self._calculate_template_fitness(template, need)
                
                if fitness > 0.6:  # Minimum fitness threshold
                    candidate = {
                        'need': need,
                        'template': template,
                        'fitness': fitness,
                        'priority': need['priority'],
                        'estimated_impact': fitness * need['priority'],
                        'creation_complexity': template.get('complexity', 0.5)
                    }
                    candidates.append(candidate)
        
        # Sort candidates by estimated impact
        candidates.sort(key=lambda x: x['estimated_impact'], reverse=True)
        
        return {
            'detected_needs': needs,
            'module_candidates': candidates,
            'timestamp': datetime.now().isoformat()
        }
    
    def create_module(self, candidate):
        """
        Create a new module based on a candidate template.
        
        Args:
            candidate (dict): Module candidate to create
            
        Returns:
            dict: Created module information
        """
        # Check if we've hit the monthly limit
        current_month = datetime.now().strftime('%Y-%m')
        current_month_creations = sum(1 for creation in self.recent_creations 
                                    if creation.startswith(current_month))
        
        if current_month_creations >= self.max_modules_per_month:
            return {
                'success': False,
                'message': f'Monthly module creation limit reached ({self.max_modules_per_month})',
                'module_name': None
            }
        
        # Generate a unique module name
        template = candidate['template']
        need = candidate['need']
        
        module_name = self._generate_module_name(template, need)
        
        # Create module blueprint
        blueprint = self._create_module_blueprint(template, need, module_name)
        
        # Generate module code (in a real system, this would have more sophistication)
        code_skeleton = self._generate_module_code(blueprint)
        
        # Create the module record
        module_record = {
            'name': module_name,
            'created_at': datetime.now().isoformat(),
            'status': 'staging',
            'template_id': template.get('id'),
            'need': need,
            'performance': [],
            'blueprint': blueprint,
            'deployment_target': datetime.now() + timedelta(days=self.staging_time),
            'last_evaluated': datetime.now().isoformat()
        }
        
        # Add to active forges
        self.active_forges.append({
            'module': module_record,
            'stage': 'creation',
            'progress': 0.0,
            'start_time': datetime.now().isoformat(),
            'estimated_completion': datetime.now() + timedelta(hours=12),
            'logs': [
                {'timestamp': datetime.now().isoformat(), 'message': f"Started creation of {module_name}"}
            ]
        })
        
        # Add to generated modules
        self.generated_modules.append(module_record)
        
        # Update recent creations
        self.recent_creations.append(datetime.now().strftime('%Y-%m-%d'))
        
        # Save generated modules
        self._save_generated_modules()
        
        return {
            'success': True,
            'message': f'Module {module_name} created successfully',
            'module_name': module_name,
            'status': 'staging',
            'blueprint': blueprint
        }
    
    def train_module(self, module_name):
        """
        Train a module that's in staging.
        
        Args:
            module_name (str): Name of the module to train
            
        Returns:
            dict: Training status
        """
        # Find the module
        module = None
        for m in self.generated_modules:
            if m['name'] == module_name:
                module = m
                break
        
        if not module:
            return {
                'success': False,
                'message': f'Module {module_name} not found'
            }
        
        if module['status'] != 'staging':
            return {
                'success': False,
                'message': f'Module {module_name} is not in staging status'
            }
        
        # Start or continue training
        forge = None
        for f in self.active_forges:
            if f['module']['name'] == module_name:
                forge = f
                break
        
        if not forge:
            # Create a new forge entry
            forge = {
                'module': module,
                'stage': 'training',
                'progress': 0.0,
                'start_time': datetime.now().isoformat(),
                'estimated_completion': datetime.now() + timedelta(days=7),
                'logs': [
                    {'timestamp': datetime.now().isoformat(), 'message': f"Started training of {module_name}"}
                ]
            }
            self.active_forges.append(forge)
        
        # Update training progress
        current_progress = forge['progress']
        if current_progress < 1.0:
            # Simulate training progress
            new_progress = min(1.0, current_progress + 0.1)
            forge['progress'] = new_progress
            
            forge['logs'].append({
                'timestamp': datetime.now().isoformat(),
                'message': f"Training progress: {new_progress:.1%}"
            })
            
            # Update module record
            module['last_evaluated'] = datetime.now().isoformat()
            self._save_generated_modules()
            
            if new_progress >= 1.0:
                # Training complete
                forge['logs'].append({
                    'timestamp': datetime.now().isoformat(),
                    'message': f"Training complete for {module_name}"
                })
                
                # Move to evaluation stage
                forge['stage'] = 'evaluation'
                forge['progress'] = 0.0
        
        return {
            'success': True,
            'message': f'Training updated for {module_name}',
            'progress': forge['progress'],
            'stage': forge['stage']
        }
    
    def evaluate_module(self, module_name):
        """
        Evaluate a module's performance.
        
        Args:
            module_name (str): Name of the module to evaluate
            
        Returns:
            dict: Evaluation results
        """
        # Find the module
        module = None
        for m in self.generated_modules:
            if m['name'] == module_name:
                module = m
                break
        
        if not module:
            return {
                'success': False,
                'message': f'Module {module_name} not found'
            }
        
        # Find the forge
        forge = None
        for f in self.active_forges:
            if f['module']['name'] == module_name:
                forge = f
                break
        
        if not forge or forge['stage'] != 'evaluation':
            return {
                'success': False,
                'message': f'Module {module_name} is not in evaluation stage'
            }
        
        # Generate evaluation metrics
        seed = hash(module_name + datetime.now().isoformat()) % (2**32 - 1)
        random.seed(seed)
        
        accuracy = random.uniform(0.6, 0.9)
        contribution = random.uniform(0.05, 0.25)
        stability = random.uniform(0.7, 0.95)
        
        evaluation = {
            'timestamp': datetime.now().isoformat(),
            'accuracy': accuracy,
            'contribution': contribution,
            'stability': stability,
            'overall_score': (accuracy * 0.5) + (contribution * 0.3) + (stability * 0.2)
        }
        
        # Update module performance
        module['performance'].append(evaluation)
        module['last_evaluated'] = datetime.now().isoformat()
        
        # Check if module is ready for deployment
        deploy_threshold = 0.7
        recent_evaluations = module['performance'][-3:] if len(module['performance']) >= 3 else module['performance']
        avg_score = sum(e['overall_score'] for e in recent_evaluations) / len(recent_evaluations)
        
        deployment_recommendation = avg_score >= deploy_threshold
        
        # Update forge status
        forge['progress'] = 1.0
        forge['logs'].append({
            'timestamp': datetime.now().isoformat(),
            'message': f"Evaluation complete: score {evaluation['overall_score']:.2f}"
        })
        
        if deployment_recommendation:
            forge['stage'] = 'deployment_ready'
            forge['logs'].append({
                'timestamp': datetime.now().isoformat(),
                'message': f"Module recommended for deployment"
            })
        else:
            forge['stage'] = 'needs_improvement'
            forge['logs'].append({
                'timestamp': datetime.now().isoformat(),
                'message': f"Module needs improvement before deployment"
            })
        
        # Save changes
        self._save_generated_modules()
        
        return {
            'success': True,
            'evaluation': evaluation,
            'deployment_recommendation': deployment_recommendation,
            'stage': forge['stage']
        }
    
    def deploy_module(self, module_name):
        """
        Deploy a module to production.
        
        Args:
            module_name (str): Name of the module to deploy
            
        Returns:
            dict: Deployment status
        """
        # Find the module
        module = None
        for m in self.generated_modules:
            if m['name'] == module_name:
                module = m
                break
        
        if not module:
            return {
                'success': False,
                'message': f'Module {module_name} not found'
            }
        
        # Find the forge
        forge = None
        for f in self.active_forges:
            if f['module']['name'] == module_name:
                forge = f
                break
        
        if not forge or forge['stage'] not in ['deployment_ready', 'needs_improvement']:
            return {
                'success': False,
                'message': f'Module {module_name} is not ready for deployment'
            }
        
        # Perform deployment
        module['status'] = 'active'
        module['deployed_at'] = datetime.now().isoformat()
        
        # Update forge
        forge['stage'] = 'deployed'
        forge['logs'].append({
            'timestamp': datetime.now().isoformat(),
            'message': f"Module {module_name} deployed to production"
        })
        
        # Save changes
        self._save_generated_modules()
        
        # Register with meta-systems
        if self.meta_systems:
            # In a real implementation, this would integrate the module
            pass
        
        return {
            'success': True,
            'message': f'Module {module_name} deployed successfully',
            'status': 'active',
            'deployed_at': module['deployed_at']
        }
    
    def get_forge_status(self, module_name=None):
        """
        Get the status of active forge operations.
        
        Args:
            module_name (str, optional): Name of a specific module
            
        Returns:
            dict: Status information
        """
        if module_name:
            # Get status for a specific module
            for forge in self.active_forges:
                if forge['module']['name'] == module_name:
                    return {
                        'module': forge['module']['name'],
                        'stage': forge['stage'],
                        'progress': forge['progress'],
                        'start_time': forge['start_time'],
                        'estimated_completion': forge.get('estimated_completion'),
                        'recent_logs': forge['logs'][-5:] if len(forge['logs']) > 5 else forge['logs']
                    }
            
            return {
                'success': False,
                'message': f'No active forge found for module {module_name}'
            }
        else:
            # Get summary of all forges
            active_count = len(self.active_forges)
            by_stage = {}
            
            for forge in self.active_forges:
                stage = forge['stage']
                if stage not in by_stage:
                    by_stage[stage] = 0
                by_stage[stage] += 1
            
            recently_deployed = [
                m['name'] for m in self.generated_modules
                if m.get('status') == 'active' and m.get('deployed_at') and 
                datetime.fromisoformat(m['deployed_at'].replace('Z', '+00:00')) > datetime.now() - timedelta(days=30)
            ]
            
            return {
                'active_forges': active_count,
                'by_stage': by_stage,
                'recently_deployed': recently_deployed,
                'available_templates': len(self.module_templates),
                'monthly_limit': self.max_modules_per_month,
                'monthly_created': current_month_creations if 'current_month_creations' in locals() else 0
            }
    
    def record_observation(self, match_data, prediction_result, actual_result):
        """
        Record an observation to feed pattern recognition.
        
        Args:
            match_data (dict): Information about the match
            prediction_result (dict): The system's prediction
            actual_result (dict): The actual outcome
            
        Returns:
            bool: True if recording was successful
        """
        # Extract key features for pattern recognition
        features = self._extract_pattern_features(match_data, prediction_result, actual_result)
        
        # Create a hash of the pattern
        pattern_hash = self._hash_pattern(features)
        
        # Check if we've seen this pattern before
        if pattern_hash in self.observed_patterns:
            self.observed_patterns[pattern_hash]['count'] += 1
            self.observed_patterns[pattern_hash]['last_seen'] = datetime.now().isoformat()
            self.observed_patterns[pattern_hash]['examples'].append({
                'match_data': match_data,
                'prediction': prediction_result,
                'actual': actual_result,
                'timestamp': datetime.now().isoformat()
            })
            
            # Limit the number of examples stored
            if len(self.observed_patterns[pattern_hash]['examples']) > 10:
                self.observed_patterns[pattern_hash]['examples'] = self.observed_patterns[pattern_hash]['examples'][-10:]
        else:
            # New pattern
            self.observed_patterns[pattern_hash] = {
                'features': features,
                'count': 1,
                'first_seen': datetime.now().isoformat(),
                'last_seen': datetime.now().isoformat(),
                'examples': [{
                    'match_data': match_data,
                    'prediction': prediction_result,
                    'actual': actual_result,
                    'timestamp': datetime.now().isoformat()
                }]
            }
        
        return True
    
    def _detect_performance_gaps(self, performance_data):
        """Detect performance gaps that could be addressed with new modules."""
        gaps = []
        
        if not performance_data:
            return gaps
        
        # Check for league-specific performance gaps
        if 'league_performance' in performance_data:
            for league, data in performance_data['league_performance'].items():
                if data.get('accuracy', 0.75) < 0.6:  # Below 60% accuracy is concerning
                    gaps.append({
                        'type': 'league_specialist',
                        'target': league,
                        'priority': min(1.0, (0.75 - data.get('accuracy', 0)) * 2),  # Higher priority for worse performance
                        'rationale': f"Performance in {league} is {data.get('accuracy', 0)*100:.1f}%, below target of 75%",
                        'source': 'performance_analysis'
                    })
        
        # Check for bet type performance gaps
        if 'bet_type_performance' in performance_data:
            for bet_type, data in performance_data['bet_type_performance'].items():
                if data.get('accuracy', 0.7) < 0.55:  # Below 55% accuracy is concerning
                    gaps.append({
                        'type': 'bet_type_specialist',
                        'target': bet_type,
                        'priority': min(1.0, (0.7 - data.get('accuracy', 0)) * 2),
                        'rationale': f"Performance for {bet_type} bets is {data.get('accuracy', 0)*100:.1f}%, below target of 70%",
                        'source': 'performance_analysis'
                    })
        
        # Check for time-specific gaps
        if 'time_performance' in performance_data:
            for time_period, data in performance_data['time_performance'].items():
                if data.get('accuracy', 0.7) < 0.6:
                    gaps.append({
                        'type': 'time_specialist',
                        'target': time_period,
                        'priority': min(1.0, (0.7 - data.get('accuracy', 0)) * 1.5),
                        'rationale': f"Performance during {time_period} is {data.get('accuracy', 0)*100:.1f}%, below target of 70%",
                        'source': 'performance_analysis'
                    })
        
        return gaps
    
    def _detect_emerging_patterns(self, system_state):
        """Detect emerging patterns that could be addressed with new modules."""
        needs = []
        
        # Check for patterns that occur frequently
        for pattern_hash, data in self.observed_patterns.items():
            if data['count'] >= self.pattern_recognition_threshold:
                # This is a recurring pattern
                features = data['features']
                
                # Analyze if this pattern represents a failure mode
                if features.get('prediction_correct', True) == False:
                    # This is a failure pattern we should address
                    pattern_type = self._determine_pattern_type(features)
                    
                    needs.append({
                        'type': f'pattern_{pattern_type}',
                        'target': self._determine_pattern_target(features),
                        'priority': min(1.0, data['count'] / (self.pattern_recognition_threshold * 2)),
                        'rationale': f"Recurring failure pattern detected {data['count']} times",
                        'source': 'pattern_recognition',
                        'pattern_hash': pattern_hash
                    })
        
        return needs
    
    def _detect_geographic_gaps(self):
        """Detect geographic coverage gaps."""
        gaps = []
        
        # Example geographic gaps - in a real system this would check actual coverage
        asian_leagues = [
            'J-League', 'K-League', 'Chinese Super League', 'A-League',
            'Thai League 1', 'Indian Super League'
        ]
        
        for league in asian_leagues:
            # Check if we have coverage for this league
            has_coverage = False
            
            for module in self.generated_modules:
                if module.get('status') == 'active' and module.get('blueprint', {}).get('target_leagues', []):
                    if league in module['blueprint']['target_leagues']:
                        has_coverage = True
                        break
            
            if not has_coverage:
                gaps.append({
                    'type': 'geographic_specialist',
                    'target': league,
                    'priority': 0.7,  # Moderately high priority
                    'rationale': f"No specialized coverage for {league}",
                    'source': 'geographic_analysis'
                })
        
        return gaps
    
    def _match_templates_to_need(self, need):
        """Match appropriate templates to a detected need."""
        matched_templates = []
        
        need_type = need.get('type', '')
        need_target = need.get('target', '')
        
        for template in self.module_templates:
            # Check if template addresses this type of need
            if need_type in template.get('applicable_needs', []):
                matched_templates.append(template)
            
            # Check for specialized templates
            if template.get('specialization', '') == need_type:
                matched_templates.append(template)
        
        return matched_templates
    
    def _calculate_template_fitness(self, template, need):
        """Calculate how well a template addresses a need."""
        # Base fitness
        fitness = 0.5
        
        # Check need type match
        if need.get('type', '') in template.get('applicable_needs', []):
            fitness += 0.2
        
        # Check specialization
        if template.get('specialization', '') == need.get('type', ''):
            fitness += 0.3
        
        # Check target compatibility
        if hasattr(template, 'target_compatibility'):
            # This would be a function to check compatibility in a real system
            pass
        
        # Adjust for complexity
        complexity = template.get('complexity', 0.5)
        fitness -= complexity * 0.1  # Slight penalty for complex templates
        
        # Normalize
        fitness = max(0, min(1, fitness))
        
        return fitness
    
    def _generate_module_name(self, template, need):
        """Generate a unique and thematic name for a new module."""
        # Get base name from template
        base_name = template.get('name_prefix', 'Module')
        
        # Add target-specific element
        target = need.get('target', '')
        target_element = ''
        
        if target:
            # Create a suitable modifier from the target
            if need.get('type', '') == 'league_specialist':
                # For leagues, use a geographical reference
                league_geo_map = {
                    'Premier League': 'Albion',
                    'La Liga': 'Iberian',
                    'Bundesliga': 'Teutonic',
                    'Serie A': 'Roman',
                    'Ligue 1': 'Gallic'
                }
                target_element = league_geo_map.get(target, target.split()[0])
            else:
                # For other targets, simplify the name
                target_element = target.split()[0]
        
        # Add a thematic suffix
        suffixes = ['Pulse', 'Nexus', 'Core', 'Echo', 'Lens', 'Wave', 'Node', 'Flux']
        suffix = random.choice(suffixes)
        
        # Add a version identifier
        version = random.choice(['Alpha', 'Beta', 'Prime', 'Zero', 'Sigma'])
        
        # Combine elements
        if target_element:
            name = f"{base_name}{target_element}{suffix}"
        else:
            name = f"{base_name}{suffix}"
        
        # Add version if there's a potential name collision
        for module in self.generated_modules:
            if module['name'] == name:
                name = f"{name}-{version}"
                break
        
        return name
    
    def _create_module_blueprint(self, template, need, module_name):
        """Create a detailed blueprint for a new module."""
        blueprint = {
            'name': module_name,
            'base_template': template.get('id'),
            'description': f"Specialized module for {need.get('target', 'general analysis')}",
            'version': '1.0.0',
            'created': datetime.now().isoformat(),
            'focus_areas': [need.get('target', '')],
            'dependencies': template.get('required_dependencies', []),
            'inputs': template.get('base_inputs', []),
            'outputs': template.get('base_outputs', []),
            'algorithm_class': template.get('algorithm_class', 'heuristic'),
            'target_leagues': [need.get('target', '')] if need.get('type') == 'league_specialist' else []
        }
        
        return blueprint
    
    def _generate_module_code(self, blueprint):
        """Generate code skeleton for a new module based on blueprint."""
        # In a real system, this would generate actual Python code
        # For simulation, we'll return a simple representation
        
        code_structure = {
            'imports': [
                'import numpy as np',
                'from datetime import datetime, timedelta',
                'import random',
                'import math'
            ],
            'class_definition': f"class {blueprint['name']}:",
            'methods': [
                '__init__',
                'analyze',
                'predict',
                'calibrate'
            ],
            'implementation_status': 'skeleton'
        }
        
        return code_structure
    
    def _extract_pattern_features(self, match_data, prediction, actual):
        """Extract key features for pattern recognition."""
        features = {}
        
        # Basic match information
        if match_data:
            features['sport'] = match_data.get('sport', '')
            features['league'] = match_data.get('league', '')
            features['has_favorite'] = bool(match_data.get('favorite', ''))
            
            # Team characteristics
            if 'home_form' in match_data and 'away_form' in match_data:
                home_form = match_data['home_form']
                away_form = match_data['away_form']
                
                # Number of wins in last 5
                home_wins = home_form[:5].count('W') if len(home_form) >= 5 else 0
                away_wins = away_form[:5].count('W') if len(away_form) >= 5 else 0
                
                features['home_form_good'] = home_wins >= 3
                features['away_form_good'] = away_wins >= 3
                features['form_differential'] = home_wins - away_wins
            
            # Odds characteristics
            if 'home_odds' in match_data and 'away_odds' in match_data:
                features['odds_favorite'] = 'home' if match_data['home_odds'] < match_data['away_odds'] else 'away'
                features['odds_gap'] = abs(match_data['home_odds'] - match_data['away_odds'])
                features['high_odds_gap'] = features['odds_gap'] > 2.0
        
        # Prediction characteristics
        if prediction:
            features['prediction'] = prediction.get('outcome', '')
            features['prediction_confidence'] = prediction.get('confidence', 0)
            features['high_confidence'] = prediction.get('confidence', 0) > 0.75
        
        # Actual result and correctness
        if actual:
            features['actual_result'] = actual.get('outcome', '')
            
            # Check if prediction was correct
            if prediction and 'outcome' in prediction and 'outcome' in actual:
                features['prediction_correct'] = prediction['outcome'] == actual['outcome']
            else:
                features['prediction_correct'] = False
        
        return features
    
    def _hash_pattern(self, features):
        """Create a hash for a pattern based on its features."""
        # Create a stable string representation of key features
        key_features = [
            features.get('sport', ''),
            features.get('league', ''),
            str(features.get('has_favorite', False)),
            str(features.get('home_form_good', False)),
            str(features.get('away_form_good', False)),
            str(features.get('form_differential', 0)),
            features.get('odds_favorite', ''),
            str(features.get('high_odds_gap', False)),
            str(features.get('high_confidence', False)),
            str(features.get('prediction_correct', False))
        ]
        
        feature_str = '_'.join(key_features)
        
        # Create a hash of the feature string
        return hashlib.md5(feature_str.encode()).hexdigest()
    
    def _determine_pattern_type(self, features):
        """Determine the type of pattern based on features."""
        if not features.get('prediction_correct', True):
            # This is a failure pattern
            
            if features.get('high_confidence', False):
                return 'high_confidence_failure'
            
            if features.get('league', ''):
                return 'league_specific_failure'
            
            if features.get('odds_favorite', '') and features.get('actual_result', '') != features.get('odds_favorite', ''):
                return 'favorite_upset'
            
            if abs(features.get('form_differential', 0)) > 2:
                return 'form_contradiction'
        
        return 'general'
    
    def _determine_pattern_target(self, features):
        """Determine the most specific target for a pattern."""
        if features.get('league', ''):
            return features.get('league', '')
        
        if features.get('sport', ''):
            return features.get('sport', '')
        
        return 'general'
    
    def _initialize_module_templates(self):
        """Initialize templates for module generation."""
        templates = [
            {
                'id': 'league_specialist',
                'name_prefix': 'League',
                'description': 'Specialized analysis module for a specific league',
                'applicable_needs': ['league_specialist', 'geographic_specialist'],
                'complexity': 0.5,
                'base_inputs': ['match_data', 'team_history', 'league_statistics'],
                'base_outputs': ['league_factors', 'confidence_adjustment'],
                'algorithm_class': 'statistical',
                'required_dependencies': ['pandas', 'numpy']
            },
            {
                'id': 'bet_type_specialist',
                'name_prefix': 'Bet',
                'description': 'Specialized analysis for a specific bet type',
                'applicable_needs': ['bet_type_specialist'],
                'complexity': 0.6,
                'base_inputs': ['match_data', 'odds_history', 'market_movement'],
                'base_outputs': ['bet_type_confidence', 'value_indicators'],
                'algorithm_class': 'probabilistic',
                'required_dependencies': ['numpy', 'scipy']
            },
            {
                'id': 'anomaly_detector',
                'name_prefix': 'Anomaly',
                'description': 'Detects anomalous patterns in odds or team behavior',
                'applicable_needs': ['pattern_high_confidence_failure', 'pattern_favorite_upset'],
                'complexity': 0.7,
                'base_inputs': ['match_data', 'odds_history', 'form_patterns'],
                'base_outputs': ['anomaly_score', 'pattern_matches'],
                'algorithm_class': 'machine_learning',
                'required_dependencies': ['numpy', 'scipy', 'scikit-learn']
            },
            {
                'id': 'pattern_recognizer',
                'name_prefix': 'Pattern',
                'description': 'Identifies recurring patterns in match outcomes',
                'applicable_needs': ['pattern_general', 'pattern_form_contradiction'],
                'complexity': 0.8,
                'base_inputs': ['match_data', 'historical_matches', 'outcome_sequences'],
                'base_outputs': ['pattern_matches', 'sequence_predictions'],
                'algorithm_class': 'sequence_analysis',
                'required_dependencies': ['numpy', 'pandas', 'matplotlib']
            },
            {
                'id': 'seasonal_dynamics',
                'name_prefix': 'Season',
                'description': 'Analyzes changes in team performance throughout a season',
                'applicable_needs': ['time_specialist', 'pattern_seasonal_variation'],
                'complexity': 0.6,
                'base_inputs': ['match_data', 'season_position', 'form_progression'],
                'base_outputs': ['season_phase_factors', 'progression_indicators'],
                'algorithm_class': 'temporal',
                'required_dependencies': ['numpy', 'pandas', 'matplotlib']
            }
        ]
        
        return templates
    
    def _load_generated_modules(self):
        """Load the history of generated modules from the database."""
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'arcanshadow.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if table exists
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='d_forge_modules'
            """)
            
            if cursor.fetchone():
                cursor.execute("SELECT module_data FROM d_forge_modules")
                rows = cursor.fetchall()
                
                modules = []
                for row in rows:
                    try:
                        module_data = json.loads(row[0])
                        modules.append(module_data)
                    except:
                        continue
                
                conn.close()
                return modules
            
            conn.close()
        except Exception as e:
            print(f"Error loading generated modules: {str(e)}")
        
        return []
    
    def _save_generated_modules(self):
        """Save the generated modules to the database."""
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'arcanshadow.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS d_forge_modules (
                    module_name TEXT PRIMARY KEY,
                    module_data TEXT,
                    created_at TEXT,
                    status TEXT
                )
            """)
            
            # Save modules
            for module in self.generated_modules:
                module_name = module['name']
                module_data = json.dumps(module)
                created_at = module.get('created_at', datetime.now().isoformat())
                status = module.get('status', 'unknown')
                
                cursor.execute("""
                    INSERT OR REPLACE INTO d_forge_modules
                    (module_name, module_data, created_at, status)
                    VALUES (?, ?, ?, ?)
                """, (module_name, module_data, created_at, status))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving generated modules: {str(e)}")
            return False