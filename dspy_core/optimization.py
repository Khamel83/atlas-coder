"""
Smart Token Management & Cost Optimization for Atlas Coder v6
Revolutionary cost efficiency with $3/day sustainable operation
"""

import re
import ast
import json
import time
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from pathlib import Path

@dataclass
class CostMetrics:
    """Track cost and performance metrics"""
    tokens_used: int
    api_calls: int
    execution_time: float
    quality_score: float
    task_type: str
    model_used: str
    cost_estimate: float
    timestamp: float

class TokenOptimizer:
    """Minimize API costs while maximizing effectiveness"""
    
    def __init__(self, daily_budget: float = 3.00):
        self.daily_budget = daily_budget
        self.cost_per_task_target = 0.01  # 1 cent average per meaningful task
        self.token_costs = {
            # OpenRouter pricing (per 1M tokens)
            'google/gemini-2.0-flash-lite-001': {'input': 0.075, 'output': 0.30},
            'google/gemini-1.5-flash': {'input': 0.075, 'output': 0.30}, 
            'anthropic/claude-3.5-sonnet': {'input': 3.0, 'output': 15.0},
            'anthropic/claude-3-opus': {'input': 15.0, 'output': 75.0},
            'ollama/*': {'input': 0.0, 'output': 0.0},  # Local models are free
        }
        
        # Context optimization settings
        self.max_context_tokens = 4000  # Safe limit for most models
        self.compression_ratio = 0.3  # Target 30% of original size
        
    def estimate_cost(self, text: str, model: str, is_output: bool = False) -> float:
        """Estimate cost for text with given model"""
        if model.startswith('ollama/'):
            return 0.0
            
        # Rough token estimation: ~4 chars per token
        tokens = len(text) / 4
        
        # Get pricing for model
        pricing = self.token_costs.get(model, self.token_costs['google/gemini-1.5-flash'])
        rate = pricing['output'] if is_output else pricing['input']
        
        # Cost per million tokens
        return (tokens / 1_000_000) * rate
    
    def optimize_context(self, code: str, requirements: str, preserve_semantics: bool = True) -> Tuple[str, str]:
        """Reduce token usage without losing essential information"""
        optimized_code = self._optimize_code_context(code, preserve_semantics)
        optimized_requirements = self._optimize_text_context(requirements)
        
        return optimized_code, optimized_requirements
    
    def _optimize_code_context(self, code: str, preserve_semantics: bool) -> str:
        """Optimize code for minimal tokens while preserving meaning"""
        if not code.strip():
            return code
            
        if preserve_semantics:
            # Keep structure but remove unnecessary elements
            optimized = self._remove_comments_and_docstrings(code)
            optimized = self._normalize_whitespace(optimized)
            optimized = self._shorten_variable_names(optimized)
        else:
            # Aggressive optimization for analysis tasks
            optimized = self._extract_code_structure(code)
            
        # Ensure we don't break syntax
        try:
            ast.parse(optimized)
            return optimized
        except SyntaxError:
            # Fall back to minimal optimization
            return self._normalize_whitespace(code)
    
    def _remove_comments_and_docstrings(self, code: str) -> str:
        """Remove comments and docstrings to save tokens"""
        lines = code.split('\n')
        optimized_lines = []
        
        in_multiline_string = False
        quote_type = None
        
        for line in lines:
            stripped = line.strip()
            
            # Skip empty lines and comments
            if not stripped or stripped.startswith('#'):
                continue
                
            # Handle docstrings and multiline strings
            if '"""' in line or "'''" in line:
                if not in_multiline_string:
                    quote_type = '"""' if '"""' in line else "'''"
                    in_multiline_string = True
                elif quote_type in line:
                    in_multiline_string = False
                    quote_type = None
                continue
                
            if in_multiline_string:
                continue
                
            # Remove inline comments
            if '#' in line:
                code_part = line.split('#')[0].rstrip()
                if code_part:
                    optimized_lines.append(code_part)
            else:
                optimized_lines.append(line)
        
        return '\n'.join(optimized_lines)
    
    def _normalize_whitespace(self, code: str) -> str:
        """Normalize whitespace to minimum required"""
        lines = code.split('\n')
        normalized_lines = []
        
        for line in lines:
            if line.strip():
                # Preserve indentation but minimize it
                leading_spaces = len(line) - len(line.lstrip())
                # Convert to minimal indentation (2 spaces per level)
                indent_level = leading_spaces // 4
                minimal_indent = '  ' * indent_level
                normalized_lines.append(minimal_indent + line.strip())
        
        return '\n'.join(normalized_lines)
    
    def _shorten_variable_names(self, code: str) -> str:
        """Shorten variable names to save tokens (careful with semantics)"""
        # Only shorten very long variable names that are clearly descriptive
        long_vars = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]{15,}\b', code)
        
        for long_var in set(long_vars):
            # Create shorter version preserving meaning
            parts = re.split(r'[_]', long_var.lower())
            if len(parts) > 2:
                short_var = ''.join(part[:3] for part in parts[:3])
                code = re.sub(r'\b' + re.escape(long_var) + r'\b', short_var, code)
        
        return code
    
    def _extract_code_structure(self, code: str) -> str:
        """Extract just the structural elements for analysis"""
        try:
            tree = ast.parse(code)
            structure_elements = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    structure_elements.append(f"def {node.name}({', '.join(args)}): pass")
                elif isinstance(node, ast.ClassDef):
                    structure_elements.append(f"class {node.name}: pass")
                elif isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                    structure_elements.append(f"import {', '.join(names)}")
                elif isinstance(node, ast.ImportFrom):
                    names = [alias.name for alias in node.names]
                    structure_elements.append(f"from {node.module} import {', '.join(names)}")
            
            return '\n'.join(structure_elements)
            
        except SyntaxError:
            # Fall back to line-based extraction
            lines = code.split('\n')
            structure_lines = []
            
            for line in lines:
                stripped = line.strip()
                if (stripped.startswith(('def ', 'class ', 'import ', 'from ')) or
                    'def ' in stripped or 'class ' in stripped):
                    structure_lines.append(stripped)
            
            return '\n'.join(structure_lines)
    
    def _optimize_text_context(self, text: str) -> str:
        """Optimize natural language text for fewer tokens"""
        if not text.strip():
            return text
            
        # Remove redundant words and phrases
        optimized = text
        
        # Remove filler words
        filler_words = ['basically', 'actually', 'literally', 'obviously', 'clearly', 'simply']
        for word in filler_words:
            optimized = re.sub(r'\b' + word + r'\b', '', optimized, flags=re.IGNORECASE)
        
        # Compress common phrases
        compressions = {
            'in order to': 'to',
            'due to the fact that': 'because',
            'for the purpose of': 'to',
            'at this point in time': 'now',
            'make use of': 'use',
            'take into consideration': 'consider',
        }
        
        for long_phrase, short_phrase in compressions.items():
            optimized = re.sub(long_phrase, short_phrase, optimized, flags=re.IGNORECASE)
        
        # Normalize whitespace
        optimized = re.sub(r'\s+', ' ', optimized).strip()
        
        return optimized
    
    def should_use_compression(self, text: str, model: str) -> bool:
        """Determine if compression would be cost-effective"""
        current_cost = self.estimate_cost(text, model)
        
        # Use compression if current cost > 0.1 cents or text > 2000 chars
        return current_cost > 0.001 or len(text) > 2000
    
    def batch_similar_tasks(self, tasks: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """Group related tasks to reduce context switching costs"""
        if not tasks:
            return []
        
        # Group by task type and similarity
        task_groups = {}
        
        for task in tasks:
            task_type = task.get('type', 'general')
            signature = task.get('signature', 'default')
            
            key = f"{task_type}_{signature}"
            if key not in task_groups:
                task_groups[key] = []
            task_groups[key].append(task)
        
        # Convert to list of batches
        batches = []
        for group in task_groups.values():
            # Split large groups into manageable batches (max 5 tasks per batch)
            for i in range(0, len(group), 5):
                batches.append(group[i:i+5])
        
        return batches

class ProgressiveComplexity:
    """Start simple, scale up based on success and need"""
    
    def __init__(self):
        self.complexity_levels = {
            'quick_scan': {
                'description': 'Fast analysis with minimal tokens',
                'max_tokens': 1000,
                'cost_target': 0.002,
                'timeout': 30,
                'model_preference': 'fast'
            },
            'detailed_analysis': {
                'description': 'Thorough analysis with moderate token usage',
                'max_tokens': 3000,
                'cost_target': 0.01,
                'timeout': 60,
                'model_preference': 'balanced'
            },
            'comprehensive_solution': {
                'description': 'Full solution generation with high token usage',
                'max_tokens': 8000,
                'cost_target': 0.05,
                'timeout': 120,
                'model_preference': 'quality'
            }
        }
        
        self.success_threshold = 0.8  # Quality score needed to avoid escalation
        
    def determine_initial_complexity(self, task: Dict[str, Any]) -> str:
        """Choose starting complexity level based on task characteristics"""
        task_type = task.get('type', 'general')
        urgency = task.get('urgency', 'normal')
        quality_requirement = task.get('quality_requirement', 0.7)
        
        # Simple heuristics for initial complexity
        if task_type in ['analyze', 'review'] and quality_requirement < 0.8:
            return 'quick_scan'
        elif urgency == 'high' or quality_requirement > 0.9:
            return 'comprehensive_solution'
        else:
            return 'detailed_analysis'
    
    def should_escalate(self, result: Any, complexity_level: str, task: Dict[str, Any]) -> bool:
        """Determine if we should escalate to higher complexity"""
        if complexity_level == 'comprehensive_solution':
            return False  # Already at max
            
        # Check quality of result
        quality_score = self._evaluate_result_quality(result, task)
        
        if quality_score < self.success_threshold:
            return True
            
        # Check if result seems incomplete
        if self._result_seems_incomplete(result, task):
            return True
            
        return False
    
    def _evaluate_result_quality(self, result: Any, task: Dict[str, Any]) -> float:
        """Evaluate quality of result (simplified heuristic)"""
        if not result or not hasattr(result, 'data'):
            return 0.0
            
        data = result.data
        
        # Basic quality indicators
        quality_indicators = 0
        total_indicators = 0
        
        # Check for completeness
        if isinstance(data, dict):
            total_indicators += 1
            if len(data) > 2:  # Has multiple fields
                quality_indicators += 1
                
            # Check for substantial content
            total_indicators += 1
            content_length = sum(len(str(v)) for v in data.values())
            if content_length > 100:  # Substantial content
                quality_indicators += 1
        
        # Check for success indicators
        total_indicators += 1
        if hasattr(result, 'success') and result.success:
            quality_indicators += 1
        
        return quality_indicators / total_indicators if total_indicators > 0 else 0.5
    
    def _result_seems_incomplete(self, result: Any, task: Dict[str, Any]) -> bool:
        """Check if result seems incomplete based on task requirements"""
        if not result or not hasattr(result, 'data'):
            return True
            
        task_type = task.get('type', 'general')
        data = result.data
        
        # Task-specific completeness checks
        if task_type == 'bug_fix':
            required_fields = ['fixed_code', 'fix_explanation']
            return not all(field in data for field in required_fields)
        elif task_type == 'generate':
            required_fields = ['code', 'explanation']
            return not all(field in data for field in required_fields)
        elif task_type == 'analyze':
            required_fields = ['analysis', 'issues']
            return not all(field in data for field in required_fields)
        
        # Generic check
        return len(str(data)) < 50  # Very short response likely incomplete

    def get_escalated_level(self, current_level: str) -> Optional[str]:
        """Get next complexity level for escalation"""
        levels = list(self.complexity_levels.keys())
        current_index = levels.index(current_level)
        
        if current_index < len(levels) - 1:
            return levels[current_index + 1]
        
        return None

class CostTracker:
    """Real-time cost tracking and budget management"""
    
    def __init__(self, daily_budget: float = 3.00):
        self.daily_budget = daily_budget
        self.cost_log_file = Path("./dspy_cache/cost_log.json")
        self.cost_log_file.parent.mkdir(exist_ok=True)
        
        self.daily_costs = self._load_daily_costs()
        self.session_metrics: List[CostMetrics] = []
        
    def _load_daily_costs(self) -> Dict[str, float]:
        """Load daily cost tracking"""
        try:
            if self.cost_log_file.exists():
                with open(self.cost_log_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def _save_daily_costs(self):
        """Save daily cost tracking"""
        try:
            with open(self.cost_log_file, 'w') as f:
                json.dump(self.daily_costs, f, indent=2)
        except Exception as e:
            print(f"⚠️ Cost log save failed: {e}")
    
    def record_usage(self, metrics: CostMetrics):
        """Record usage and update daily costs"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        if today not in self.daily_costs:
            self.daily_costs[today] = 0.0
            
        self.daily_costs[today] += metrics.cost_estimate
        self.session_metrics.append(metrics)
        
        self._save_daily_costs()
        
        # Warn if approaching budget
        if self.daily_costs[today] > self.daily_budget * 0.8:
            remaining = self.daily_budget - self.daily_costs[today]
            print(f"💰 Budget warning: ${remaining:.3f} remaining today")
    
    def get_remaining_budget(self) -> float:
        """Get remaining budget for today"""
        today = datetime.now().strftime('%Y-%m-%d')
        used = self.daily_costs.get(today, 0.0)
        return max(0.0, self.daily_budget - used)
    
    def can_afford_task(self, estimated_cost: float) -> bool:
        """Check if we can afford a task"""
        return estimated_cost <= self.get_remaining_budget()
    
    def get_cost_efficiency_stats(self) -> Dict[str, Any]:
        """Get cost efficiency statistics"""
        if not self.session_metrics:
            return {"efficiency": 0.0, "quality_per_dollar": 0.0}
            
        total_cost = sum(m.cost_estimate for m in self.session_metrics)
        total_quality = sum(m.quality_score for m in self.session_metrics)
        
        avg_quality = total_quality / len(self.session_metrics)
        quality_per_dollar = total_quality / total_cost if total_cost > 0 else 0
        
        return {
            "total_cost": total_cost,
            "avg_quality": avg_quality,
            "quality_per_dollar": quality_per_dollar,
            "tasks_completed": len(self.session_metrics),
            "cost_per_task": total_cost / len(self.session_metrics)
        }

# Global instances
_token_optimizer = None
_progressive_complexity = None
_cost_tracker = None

def get_token_optimizer() -> TokenOptimizer:
    """Get global token optimizer instance"""
    global _token_optimizer
    if _token_optimizer is None:
        _token_optimizer = TokenOptimizer()
    return _token_optimizer

def get_progressive_complexity() -> ProgressiveComplexity:
    """Get global progressive complexity instance"""
    global _progressive_complexity
    if _progressive_complexity is None:
        _progressive_complexity = ProgressiveComplexity()
    return _progressive_complexity

def get_cost_tracker() -> CostTracker:
    """Get global cost tracker instance"""
    global _cost_tracker
    if _cost_tracker is None:
        _cost_tracker = CostTracker()
    return _cost_tracker