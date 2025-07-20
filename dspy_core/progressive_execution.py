"""
Progressive Complexity Execution for Atlas Coder v6
Start simple, escalate intelligently based on results and requirements
"""

import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

from .optimization import get_progressive_complexity, get_cost_tracker, CostMetrics
from .model_strategy import get_model_strategy
from .workflows import get_orchestrator, WorkflowResult

class ExecutionLevel(Enum):
    """Execution complexity levels"""
    QUICK_SCAN = "quick_scan"
    DETAILED_ANALYSIS = "detailed_analysis"
    COMPREHENSIVE_SOLUTION = "comprehensive_solution"

@dataclass
class ExecutionResult:
    """Result from progressive execution"""
    success: bool
    level_used: ExecutionLevel
    result: Any
    cost: float
    execution_time: float
    quality_score: float
    escalation_needed: bool
    next_level: Optional[ExecutionLevel]

class ProgressiveExecutor:
    """Execute tasks with progressive complexity escalation"""
    
    def __init__(self):
        self.complexity_manager = get_progressive_complexity()
        self.cost_tracker = get_cost_tracker()
        self.model_strategy = get_model_strategy()
        self.orchestrator = get_orchestrator()
        
        # Execution settings
        self.max_escalations = 2
        self.quality_threshold = 0.8
        self.cost_escalation_factor = 1.5
        
    def execute_with_escalation(self, 
                               workflow_type: str,
                               task_params: Dict[str, Any],
                               initial_level: Optional[ExecutionLevel] = None) -> ExecutionResult:
        """Execute task with automatic escalation if needed"""
        
        # Determine initial complexity level
        if initial_level is None:
            task_info = {
                'type': workflow_type,
                'urgency': task_params.get('urgency', 'normal'),
                'quality_requirement': task_params.get('quality_requirement', 0.7)
            }
            level_name = self.complexity_manager.determine_initial_complexity(task_info)
            current_level = ExecutionLevel(level_name)
        else:
            current_level = initial_level
        
        print(f"🎯 Starting execution at {current_level.value} level")
        
        escalation_count = 0
        last_result = None
        
        while escalation_count <= self.max_escalations:
            # Execute at current level
            exec_result = self._execute_at_level(
                workflow_type, task_params, current_level
            )
            
            last_result = exec_result
            
            # Check if escalation is needed
            if not exec_result.escalation_needed or escalation_count >= self.max_escalations:
                break
            
            if exec_result.next_level is None:
                break  # No higher level available
            
            # Check if we can afford escalation
            estimated_escalation_cost = exec_result.cost * self.cost_escalation_factor
            if not self.cost_tracker.can_afford_task(estimated_escalation_cost):
                print(f"💰 Escalation would exceed budget, staying at {current_level.value}")
                break
            
            # Escalate
            current_level = exec_result.next_level
            escalation_count += 1
            print(f"🔄 Escalating to {current_level.value} level (attempt {escalation_count + 1})")
        
        return last_result
    
    def _execute_at_level(self, 
                         workflow_type: str,
                         task_params: Dict[str, Any],
                         level: ExecutionLevel) -> ExecutionResult:
        """Execute task at specific complexity level"""
        
        start_time = time.time()
        
        # Get level configuration
        level_config = self.complexity_manager.complexity_levels[level.value]
        
        # Select appropriate model for this level
        model = self._select_model_for_level(level, workflow_type, task_params)
        
        # Optimize parameters for this level
        optimized_params = self._optimize_params_for_level(task_params, level_config)
        
        try:
            # Execute workflow with level constraints
            result = self._execute_constrained_workflow(
                workflow_type, optimized_params, level_config, model
            )
            
            execution_time = time.time() - start_time
            
            # Evaluate result quality
            quality_score = self._evaluate_quality(result, workflow_type, level)
            
            # Estimate cost
            cost = self._estimate_execution_cost(result, model, execution_time)
            
            # Record performance
            self.model_strategy.record_performance(
                model, workflow_type, result.success, quality_score, execution_time, cost
            )
            
            # Record cost metrics
            metrics = CostMetrics(
                tokens_used=self._estimate_tokens_used(result),
                api_calls=1,
                execution_time=execution_time,
                quality_score=quality_score,
                task_type=workflow_type,
                model_used=model,
                cost_estimate=cost,
                timestamp=time.time()
            )
            self.cost_tracker.record_usage(metrics)
            
            # Check if escalation is needed
            escalation_needed = self._should_escalate(result, quality_score, level, workflow_type)
            next_level = self._get_next_level(level) if escalation_needed else None
            
            return ExecutionResult(
                success=result.success,
                level_used=level,
                result=result,
                cost=cost,
                execution_time=execution_time,
                quality_score=quality_score,
                escalation_needed=escalation_needed,
                next_level=next_level
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ Execution failed at {level.value}: {e}")
            
            # Create failure result
            failure_result = WorkflowResult(success=False, error=str(e))
            
            return ExecutionResult(
                success=False,
                level_used=level,
                result=failure_result,
                cost=0.01,  # Minimal cost for failed execution
                execution_time=execution_time,
                quality_score=0.0,
                escalation_needed=True,
                next_level=self._get_next_level(level)
            )
    
    def _select_model_for_level(self, 
                               level: ExecutionLevel,
                               workflow_type: str, 
                               task_params: Dict[str, Any]) -> str:
        """Select appropriate model for execution level"""
        
        level_config = self.complexity_manager.complexity_levels[level.value]
        model_preference = level_config['model_preference']
        
        # Map level preferences to complexity/quality requirements
        if model_preference == 'fast':
            complexity = 0.3
            quality = 0.6
        elif model_preference == 'balanced':
            complexity = 0.6
            quality = 0.8
        elif model_preference == 'quality':
            complexity = 0.9
            quality = 0.95
        else:
            complexity = 0.5
            quality = 0.7
        
        # Get remaining budget
        budget = self.cost_tracker.get_remaining_budget()
        
        # Select model using strategy
        return self.model_strategy.select_model(
            task_complexity=complexity,
            quality_requirement=quality,
            budget_remaining=budget,
            task_type=workflow_type,
            urgency=task_params.get('urgency', 'normal')
        )
    
    def _optimize_params_for_level(self, 
                                  params: Dict[str, Any], 
                                  level_config: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize task parameters for specific execution level"""
        optimized = params.copy()
        
        # Add level-specific constraints
        optimized['max_tokens'] = level_config['max_tokens']
        optimized['timeout'] = level_config['timeout']
        optimized['cost_target'] = level_config['cost_target']
        
        # Optimize input size based on level
        if 'code' in optimized:
            code = optimized['code']
            if len(code) > level_config['max_tokens'] * 2:  # Rough token estimation
                # Compress code for lower levels
                from .optimization import get_token_optimizer
                optimizer = get_token_optimizer()
                
                preserve_semantics = level_config['model_preference'] != 'fast'
                optimized['code'], _ = optimizer.optimize_context(code, '', preserve_semantics)
        
        return optimized
    
    def _execute_constrained_workflow(self,
                                    workflow_type: str,
                                    params: Dict[str, Any],
                                    level_config: Dict[str, Any],
                                    model: str) -> WorkflowResult:
        """Execute workflow with level-specific constraints"""
        
        # Set timeout for execution
        timeout = level_config['timeout']
        
        # Execute with timeout (simplified - real implementation would need async)
        start_time = time.time()
        result = self.orchestrator.execute_workflow(workflow_type, **params)
        execution_time = time.time() - start_time
        
        # Check timeout
        if execution_time > timeout:
            print(f"⏱️ Execution exceeded timeout ({timeout}s)")
            # In real implementation, would cancel execution
        
        return result
    
    def _evaluate_quality(self, 
                         result: WorkflowResult, 
                         workflow_type: str, 
                         level: ExecutionLevel) -> float:
        """Evaluate result quality for escalation decisions"""
        
        if not result.success:
            return 0.0
        
        # Use the complexity manager's evaluation
        task_info = {'type': workflow_type}
        return self.complexity_manager._evaluate_result_quality(result, task_info)
    
    def _estimate_execution_cost(self, 
                                result: WorkflowResult, 
                                model: str, 
                                execution_time: float) -> float:
        """Estimate cost of execution"""
        
        if model.startswith('ollama/'):
            return 0.0  # Local models are free
        
        # Rough estimation based on result content
        from .optimization import get_token_optimizer
        optimizer = get_token_optimizer()
        
        # Estimate tokens from result content
        content_length = 0
        if result.success and result.data:
            content_length = sum(len(str(v)) for v in result.data.values())
        
        # Add base cost for API call
        estimated_cost = optimizer.estimate_cost(
            text="x" * content_length, 
            model=model, 
            is_output=True
        )
        
        return max(0.001, estimated_cost)  # Minimum cost
    
    def _estimate_tokens_used(self, result: WorkflowResult) -> int:
        """Estimate tokens used in execution"""
        if not result.success or not result.data:
            return 100  # Minimal estimation
        
        # Rough estimation: 4 characters per token
        content_length = sum(len(str(v)) for v in result.data.values())
        return max(100, content_length // 4)
    
    def _should_escalate(self, 
                        result: WorkflowResult, 
                        quality_score: float, 
                        level: ExecutionLevel, 
                        workflow_type: str) -> bool:
        """Determine if escalation is needed"""
        
        if not result.success:
            return True  # Always escalate on failure
        
        if quality_score < self.quality_threshold:
            return True  # Escalate if quality is too low
        
        # Use complexity manager's escalation logic
        task_info = {'type': workflow_type}
        return self.complexity_manager.should_escalate(result, level.value, task_info)
    
    def _get_next_level(self, current_level: ExecutionLevel) -> Optional[ExecutionLevel]:
        """Get next escalation level"""
        level_order = [
            ExecutionLevel.QUICK_SCAN,
            ExecutionLevel.DETAILED_ANALYSIS,
            ExecutionLevel.COMPREHENSIVE_SOLUTION
        ]
        
        try:
            current_index = level_order.index(current_level)
            if current_index < len(level_order) - 1:
                return level_order[current_index + 1]
        except ValueError:
            pass
        
        return None
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        cost_stats = self.cost_tracker.get_cost_efficiency_stats()
        strategy_stats = self.model_strategy.get_strategy_stats()
        
        return {
            'cost_efficiency': cost_stats,
            'model_strategy': strategy_stats,
            'quality_threshold': self.quality_threshold,
            'max_escalations': self.max_escalations
        }

# Convenience functions for common execution patterns
def execute_simple_task(workflow_type: str, **params) -> ExecutionResult:
    """Execute task starting at quick_scan level"""
    executor = ProgressiveExecutor()
    return executor.execute_with_escalation(
        workflow_type, params, ExecutionLevel.QUICK_SCAN
    )

def execute_quality_task(workflow_type: str, **params) -> ExecutionResult:
    """Execute task starting at comprehensive level for quality"""
    executor = ProgressiveExecutor()
    return executor.execute_with_escalation(
        workflow_type, params, ExecutionLevel.COMPREHENSIVE_SOLUTION
    )

def execute_balanced_task(workflow_type: str, **params) -> ExecutionResult:
    """Execute task starting at detailed analysis level"""
    executor = ProgressiveExecutor()
    return executor.execute_with_escalation(
        workflow_type, params, ExecutionLevel.DETAILED_ANALYSIS
    )

# Global instance
_progressive_executor = None

def get_progressive_executor() -> ProgressiveExecutor:
    """Get global progressive executor instance"""
    global _progressive_executor
    if _progressive_executor is None:
        _progressive_executor = ProgressiveExecutor()
    return _progressive_executor