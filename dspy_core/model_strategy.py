"""
Hybrid Model Strategy for Atlas Coder v6
Intelligent model selection for optimal cost/quality balance
"""

import os
import time
import json
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

class ModelTier(Enum):
    """Model tiers based on cost and capability"""
    LOCAL_FREE = "local_free"
    OPENROUTER_CHEAP = "openrouter_cheap"
    OPENROUTER_BALANCED = "openrouter_balanced"
    OPENROUTER_PREMIUM = "openrouter_premium"
    OPENROUTER_MAX = "openrouter_max"

@dataclass
class ModelConfig:
    """Configuration for a specific model"""
    name: str
    tier: ModelTier
    cost_per_1m_input: float
    cost_per_1m_output: float
    max_tokens: int
    quality_score: float  # 0.0 to 1.0
    speed_score: float    # 0.0 to 1.0
    specialization: List[str]  # ['code', 'analysis', 'general']
    api_base: str
    requires_api_key: bool

class HybridModelStrategy:
    """Seamlessly switch between local and OpenRouter models based on task complexity"""
    
    def __init__(self):
        self.models = self._initialize_model_configs()
        self.performance_cache = self._load_performance_cache()
        self.fallback_chain = self._build_fallback_chain()
        
        # Current session tracking
        self.current_model = None
        self.model_switch_count = 0
        self.total_cost = 0.0
        
    def _initialize_model_configs(self) -> Dict[str, ModelConfig]:
        """Initialize all available model configurations"""
        return {
            # Local models (free)
            'ollama/qwen2.5-coder': ModelConfig(
                name='ollama/qwen2.5-coder',
                tier=ModelTier.LOCAL_FREE,
                cost_per_1m_input=0.0,
                cost_per_1m_output=0.0,
                max_tokens=8192,
                quality_score=0.7,
                speed_score=0.9,
                specialization=['code', 'analysis'],
                api_base='http://localhost:11434',
                requires_api_key=False
            ),
            'ollama/llama3.2': ModelConfig(
                name='ollama/llama3.2',
                tier=ModelTier.LOCAL_FREE,
                cost_per_1m_input=0.0,
                cost_per_1m_output=0.0,
                max_tokens=4096,
                quality_score=0.65,
                speed_score=0.8,
                specialization=['general', 'analysis'],
                api_base='http://localhost:11434',
                requires_api_key=False
            ),
            
            # OpenRouter cheap tier
            'google/gemini-2.0-flash-lite-001': ModelConfig(
                name='google/gemini-2.0-flash-lite-001',
                tier=ModelTier.OPENROUTER_CHEAP,
                cost_per_1m_input=0.075,
                cost_per_1m_output=0.30,
                max_tokens=8192,
                quality_score=0.75,
                speed_score=0.95,
                specialization=['general', 'code', 'analysis'],
                api_base='https://openrouter.ai/api/v1',
                requires_api_key=True
            ),
            'google/gemini-1.5-flash': ModelConfig(
                name='google/gemini-1.5-flash',
                tier=ModelTier.OPENROUTER_CHEAP,
                cost_per_1m_input=0.075,
                cost_per_1m_output=0.30,
                max_tokens=8192,
                quality_score=0.78,
                speed_score=0.9,
                specialization=['general', 'code', 'analysis'],
                api_base='https://openrouter.ai/api/v1',
                requires_api_key=True
            ),
            
            # OpenRouter balanced tier
            'anthropic/claude-3.5-haiku': ModelConfig(
                name='anthropic/claude-3.5-haiku',
                tier=ModelTier.OPENROUTER_BALANCED,
                cost_per_1m_input=1.0,
                cost_per_1m_output=5.0,
                max_tokens=8192,
                quality_score=0.85,
                speed_score=0.85,
                specialization=['code', 'analysis', 'general'],
                api_base='https://openrouter.ai/api/v1',
                requires_api_key=True
            ),
            
            # OpenRouter premium tier
            'anthropic/claude-3.5-sonnet': ModelConfig(
                name='anthropic/claude-3.5-sonnet',
                tier=ModelTier.OPENROUTER_PREMIUM,
                cost_per_1m_input=3.0,
                cost_per_1m_output=15.0,
                max_tokens=8192,
                quality_score=0.95,
                speed_score=0.7,
                specialization=['code', 'analysis', 'general', 'architecture'],
                api_base='https://openrouter.ai/api/v1',
                requires_api_key=True
            ),
            
            # OpenRouter max tier
            'anthropic/claude-3-opus': ModelConfig(
                name='anthropic/claude-3-opus',
                tier=ModelTier.OPENROUTER_MAX,
                cost_per_1m_input=15.0,
                cost_per_1m_output=75.0,
                max_tokens=4096,
                quality_score=0.98,
                speed_score=0.5,
                specialization=['architecture', 'complex_reasoning', 'code'],
                api_base='https://openrouter.ai/api/v1',
                requires_api_key=True
            ),
        }
    
    def _load_performance_cache(self) -> Dict[str, Dict[str, Any]]:
        """Load model performance data from previous runs"""
        cache_file = Path("./dspy_cache/model_performance.json")
        try:
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def _save_performance_cache(self):
        """Save model performance data"""
        cache_file = Path("./dspy_cache/model_performance.json")
        try:
            cache_file.parent.mkdir(exist_ok=True)
            with open(cache_file, 'w') as f:
                json.dump(self.performance_cache, f, indent=2)
        except Exception as e:
            print(f"⚠️ Performance cache save failed: {e}")
    
    def _build_fallback_chain(self) -> List[str]:
        """Build intelligent fallback chain"""
        available_models = []
        
        # Check for local models first
        if self._is_ollama_available():
            available_models.extend([
                'ollama/qwen2.5-coder',
                'ollama/llama3.2'
            ])
        
        # Add OpenRouter models if API key available
        if os.getenv('OPENAI_API_KEY'):
            available_models.extend([
                'google/gemini-2.0-flash-lite-001',
                'google/gemini-1.5-flash',
                'anthropic/claude-3.5-haiku',
                'anthropic/claude-3.5-sonnet',
                'anthropic/claude-3-opus'
            ])
        
        return available_models
    
    def _is_ollama_available(self) -> bool:
        """Check if Ollama is running locally"""
        try:
            import requests
            response = requests.get('http://localhost:11434/api/tags', timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def select_model(self, 
                    task_complexity: float,
                    quality_requirement: float, 
                    budget_remaining: float,
                    task_type: str = 'general',
                    urgency: str = 'normal') -> str:
        """Choose optimal model for task based on multiple factors"""
        
        # Score each available model
        model_scores = {}
        
        for model_name in self.fallback_chain:
            if model_name not in self.models:
                continue
                
            model = self.models[model_name]
            score = self._calculate_model_score(
                model, task_complexity, quality_requirement, 
                budget_remaining, task_type, urgency
            )
            
            if score > 0:  # Only consider viable models
                model_scores[model_name] = score
        
        if not model_scores:
            # Emergency fallback
            return self.fallback_chain[0] if self.fallback_chain else 'ollama/llama3.2'
        
        # Select highest scoring model
        best_model = max(model_scores.items(), key=lambda x: x[1])[0]
        
        if best_model != self.current_model:
            self.model_switch_count += 1
            self.current_model = best_model
            print(f"🔄 Switched to {best_model} (score: {model_scores[best_model]:.2f})")
        
        return best_model
    
    def _calculate_model_score(self,
                              model: ModelConfig,
                              task_complexity: float,
                              quality_requirement: float,
                              budget_remaining: float,
                              task_type: str,
                              urgency: str) -> float:
        """Calculate composite score for model selection"""
        
        # Base score from model quality
        quality_score = model.quality_score
        
        # Adjust for task type specialization
        specialization_bonus = 0.0
        if task_type in model.specialization:
            specialization_bonus = 0.1
        
        # Adjust for complexity requirements
        complexity_match = 1.0 - abs(model.quality_score - quality_requirement)
        
        # Cost penalty
        estimated_cost = self._estimate_task_cost(model, task_complexity)
        cost_penalty = 0.0
        
        if model.requires_api_key and budget_remaining > 0:
            cost_ratio = estimated_cost / budget_remaining
            if cost_ratio > 0.5:  # More than 50% of remaining budget
                cost_penalty = cost_ratio * 0.3
        elif model.requires_api_key and budget_remaining <= 0:
            cost_penalty = 1.0  # Can't afford
        
        # Speed bonus for urgent tasks
        speed_bonus = 0.0
        if urgency == 'high':
            speed_bonus = model.speed_score * 0.1
        
        # Availability check
        availability_score = 1.0
        if model.requires_api_key and not os.getenv('OPENAI_API_KEY'):
            availability_score = 0.0
        elif model.tier == ModelTier.LOCAL_FREE and not self._is_ollama_available():
            availability_score = 0.0
        
        # Historical performance adjustment
        historical_bonus = self._get_historical_performance_bonus(model.name, task_type)
        
        # Composite score
        score = (quality_score + 
                specialization_bonus + 
                complexity_match + 
                speed_bonus + 
                historical_bonus - 
                cost_penalty) * availability_score
        
        return max(0.0, score)
    
    def _estimate_task_cost(self, model: ModelConfig, complexity: float) -> float:
        """Estimate cost for task with given model and complexity"""
        if not model.requires_api_key:
            return 0.0
        
        # Rough token estimation based on complexity
        base_tokens = 500  # Minimum tokens
        complexity_tokens = complexity * 2000  # Scale with complexity
        total_tokens = base_tokens + complexity_tokens
        
        # Estimate input/output split (60/40)
        input_tokens = total_tokens * 0.6
        output_tokens = total_tokens * 0.4
        
        input_cost = (input_tokens / 1_000_000) * model.cost_per_1m_input
        output_cost = (output_tokens / 1_000_000) * model.cost_per_1m_output
        
        return input_cost + output_cost
    
    def _get_historical_performance_bonus(self, model_name: str, task_type: str) -> float:
        """Get performance bonus based on historical success"""
        if model_name not in self.performance_cache:
            return 0.0
        
        model_history = self.performance_cache[model_name]
        task_history = model_history.get(task_type, {})
        
        if not task_history:
            return 0.0
        
        success_rate = task_history.get('success_rate', 0.5)
        avg_quality = task_history.get('avg_quality', 0.5)
        
        # Bonus for consistently good performance
        performance_bonus = (success_rate + avg_quality) * 0.05
        
        return performance_bonus
    
    def record_performance(self, 
                          model_name: str,
                          task_type: str, 
                          success: bool,
                          quality_score: float,
                          execution_time: float,
                          cost: float):
        """Record model performance for future selection"""
        
        if model_name not in self.performance_cache:
            self.performance_cache[model_name] = {}
        
        if task_type not in self.performance_cache[model_name]:
            self.performance_cache[model_name][task_type] = {
                'total_runs': 0,
                'successful_runs': 0,
                'total_quality': 0.0,
                'total_time': 0.0,
                'total_cost': 0.0
            }
        
        stats = self.performance_cache[model_name][task_type]
        stats['total_runs'] += 1
        if success:
            stats['successful_runs'] += 1
        stats['total_quality'] += quality_score
        stats['total_time'] += execution_time
        stats['total_cost'] += cost
        
        # Calculate derived metrics
        stats['success_rate'] = stats['successful_runs'] / stats['total_runs']
        stats['avg_quality'] = stats['total_quality'] / stats['total_runs']
        stats['avg_time'] = stats['total_time'] / stats['total_runs']
        stats['avg_cost'] = stats['total_cost'] / stats['total_runs']
        
        self._save_performance_cache()
        self.total_cost += cost
    
    def get_model_recommendations(self, 
                                 task_type: str = 'general',
                                 budget_remaining: float = 3.0) -> Dict[str, Any]:
        """Get model recommendations for different scenarios"""
        
        recommendations = {
            'cost_optimal': None,
            'quality_optimal': None,
            'balanced': None,
            'emergency_fallback': None
        }
        
        available_models = [self.models[name] for name in self.fallback_chain 
                          if name in self.models]
        
        if not available_models:
            return recommendations
        
        # Cost optimal (prefer free models)
        free_models = [m for m in available_models if not m.requires_api_key]
        if free_models:
            recommendations['cost_optimal'] = max(free_models, key=lambda m: m.quality_score).name
        
        # Quality optimal (within budget)
        affordable_models = [m for m in available_models 
                           if not m.requires_api_key or 
                           self._estimate_task_cost(m, 0.5) <= budget_remaining]
        if affordable_models:
            recommendations['quality_optimal'] = max(affordable_models, key=lambda m: m.quality_score).name
        
        # Balanced (good quality/cost ratio)
        if affordable_models:
            def quality_cost_ratio(model):
                cost = self._estimate_task_cost(model, 0.5)
                return model.quality_score / (cost + 0.01)  # Avoid division by zero
            
            recommendations['balanced'] = max(affordable_models, key=quality_cost_ratio).name
        
        # Emergency fallback
        recommendations['emergency_fallback'] = available_models[0].name
        
        return recommendations
    
    def get_strategy_stats(self) -> Dict[str, Any]:
        """Get strategy performance statistics"""
        return {
            'current_model': self.current_model,
            'model_switches': self.model_switch_count,
            'total_session_cost': self.total_cost,
            'available_models': len(self.fallback_chain),
            'local_models_available': self._is_ollama_available(),
            'api_key_configured': bool(os.getenv('OPENAI_API_KEY')),
            'performance_cache_size': sum(len(tasks) for tasks in self.performance_cache.values())
        }

# Global instance
_model_strategy = None

def get_model_strategy() -> HybridModelStrategy:
    """Get global model strategy instance"""
    global _model_strategy
    if _model_strategy is None:
        _model_strategy = HybridModelStrategy()
    return _model_strategy