"""Advanced meta-learning and self-improving workflows.

This module implements sophisticated self-improvement patterns that learn
from successes and failures to optimize future performance.
"""

import json
import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

import dspy
from pydantic import BaseModel


class PerformanceMetric(BaseModel):
    """Track performance of different approaches."""
    approach_id: str
    success_rate: float
    avg_confidence: float
    avg_execution_time: float
    cost_per_success: float
    sample_count: int
    last_updated: str


class LearningPattern(BaseModel):
    """Patterns learned from successful/failed attempts."""
    pattern_id: str
    pattern_type: str  # "success" or "failure"
    context_signature: Dict[str, Any]
    approach_used: str
    outcome_quality: float
    frequency: int
    first_seen: str
    last_seen: str


class SelfImprovingOptimizer(dspy.Module):
    """Meta-optimizer that improves its own performance over time."""
    
    def __init__(self, knowledge_base_path: str = "./meta_knowledge.json"):
        super().__init__()
        self.knowledge_base_path = Path(knowledge_base_path)
        self.performance_metrics: Dict[str, PerformanceMetric] = {}
        self.learning_patterns: Dict[str, LearningPattern] = {}
        self.load_knowledge_base()
        
        # Available optimization strategies
        self.strategies = {
            "conservative": self._conservative_approach,
            "aggressive": self._aggressive_approach,
            "balanced": self._balanced_approach,
            "adaptive": self._adaptive_approach
        }
    
    def optimize_approach(self, task_context: Dict[str, Any]) -> Tuple[str, float]:
        """Select optimal approach based on learned patterns."""
        context_signature = self._create_context_signature(task_context)
        
        # Find similar past contexts
        similar_patterns = self._find_similar_patterns(context_signature)
        
        if not similar_patterns:
            # No similar patterns, use balanced approach
            return "balanced", 0.5
        
        # Analyze success rates of different approaches for similar contexts
        approach_scores = {}
        for pattern in similar_patterns:
            approach = pattern.approach_used
            if approach not in approach_scores:
                approach_scores[approach] = {"total_quality": 0, "count": 0}
            
            # Weight by recency and frequency
            recency_weight = self._calculate_recency_weight(pattern.last_seen)
            frequency_weight = min(pattern.frequency / 10.0, 1.0)
            weight = recency_weight * frequency_weight
            
            approach_scores[approach]["total_quality"] += pattern.outcome_quality * weight
            approach_scores[approach]["count"] += weight
        
        # Calculate weighted averages
        best_approach = "balanced"
        best_score = 0.0
        
        for approach, scores in approach_scores.items():
            if scores["count"] > 0:
                avg_score = scores["total_quality"] / scores["count"]
                if avg_score > best_score:
                    best_score = avg_score
                    best_approach = approach
        
        return best_approach, best_score
    
    def execute_with_learning(self, task: Dict[str, Any], target_module: dspy.Module) -> Dict[str, Any]:
        """Execute task while learning from the outcome."""
        start_time = datetime.now()
        context_signature = self._create_context_signature(task)
        
        # Select optimal approach
        approach, confidence = self.optimize_approach(task)
        
        try:
            # Execute with selected strategy
            result = self.strategies[approach](task, target_module)
            
            # Measure performance
            execution_time = (datetime.now() - start_time).total_seconds()
            success = result.get("success", False)
            quality_score = result.get("quality_score", 0.0)
            
            # Learn from outcome
            self._record_outcome(
                context_signature=context_signature,
                approach=approach,
                success=success,
                quality_score=quality_score,
                execution_time=execution_time
            )
            
            # Update result with meta-information
            result["meta_learning"] = {
                "approach_used": approach,
                "confidence": confidence,
                "execution_time": execution_time,
                "learning_applied": len(self._find_similar_patterns(context_signature)) > 0
            }
            
            return result
            
        except Exception as e:
            # Learn from failures too
            execution_time = (datetime.now() - start_time).total_seconds()
            self._record_failure(context_signature, approach, str(e), execution_time)
            raise e
    
    def generate_improvement_report(self) -> Dict[str, Any]:
        """Generate comprehensive improvement analysis."""
        report = {
            "total_patterns": len(self.learning_patterns),
            "total_metrics": len(self.performance_metrics),
            "approach_performance": {},
            "improvement_trends": {},
            "recommendations": []
        }
        
        # Analyze approach performance
        for approach, metric in self.performance_metrics.items():
            report["approach_performance"][approach] = {
                "success_rate": metric.success_rate,
                "avg_confidence": metric.avg_confidence,
                "efficiency": metric.cost_per_success,
                "sample_size": metric.sample_count
            }
        
        # Identify improvement trends
        success_patterns = [p for p in self.learning_patterns.values() if p.pattern_type == "success"]
        failure_patterns = [p for p in self.learning_patterns.values() if p.pattern_type == "failure"]
        
        report["improvement_trends"] = {
            "success_pattern_growth": len(success_patterns),
            "failure_pattern_reduction": max(0, len(success_patterns) - len(failure_patterns)),
            "most_successful_approach": self._get_best_approach(),
            "learning_velocity": self._calculate_learning_velocity()
        }
        
        # Generate recommendations
        recommendations = []
        
        # Recommend approach adjustments
        best_approach = self._get_best_approach()
        if best_approach and best_approach != "balanced":
            recommendations.append(f"Consider defaulting to '{best_approach}' approach for better results")
        
        # Recommend pattern optimizations
        common_failures = self._get_common_failure_patterns()
        if common_failures:
            recommendations.append(f"Focus on improving handling of: {', '.join(common_failures[:3])}")
        
        report["recommendations"] = recommendations
        return report
    
    def _conservative_approach(self, task: Dict[str, Any], module: dspy.Module) -> Dict[str, Any]:
        """Conservative approach with high confidence thresholds."""
        # Use simpler, more reliable methods
        result = module(**task)
        
        # Add conservative quality assessment
        quality_score = 0.7  # Conservative baseline
        if hasattr(result, 'confidence') and result.confidence:
            quality_score = min(float(result.confidence), quality_score)
        
        return {
            "result": result,
            "success": True,
            "quality_score": quality_score,
            "approach": "conservative"
        }
    
    def _aggressive_approach(self, task: Dict[str, Any], module: dspy.Module) -> Dict[str, Any]:
        """Aggressive approach using advanced techniques."""
        # Use more sophisticated methods, accept higher risk
        result = module(**task)
        
        # Add aggressive quality assessment
        quality_score = 0.9  # Optimistic baseline
        if hasattr(result, 'confidence') and result.confidence:
            quality_score = float(result.confidence)
        
        return {
            "result": result,
            "success": True,
            "quality_score": quality_score,
            "approach": "aggressive"
        }
    
    def _balanced_approach(self, task: Dict[str, Any], module: dspy.Module) -> Dict[str, Any]:
        """Balanced approach mixing conservative and aggressive elements."""
        result = module(**task)
        
        quality_score = 0.8  # Balanced baseline
        if hasattr(result, 'confidence') and result.confidence:
            quality_score = float(result.confidence)
        
        return {
            "result": result,
            "success": True,
            "quality_score": quality_score,
            "approach": "balanced"
        }
    
    def _adaptive_approach(self, task: Dict[str, Any], module: dspy.Module) -> Dict[str, Any]:
        """Adaptive approach that changes based on task characteristics."""
        # Analyze task complexity
        complexity = self._assess_task_complexity(task)
        
        if complexity < 0.3:
            return self._conservative_approach(task, module)
        elif complexity > 0.7:
            return self._aggressive_approach(task, module)
        else:
            return self._balanced_approach(task, module)
    
    def _create_context_signature(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a signature for context matching."""
        signature = {}
        
        # Extract key characteristics
        if "code" in context:
            signature["code_length"] = len(str(context["code"]).split())
            signature["code_complexity"] = str(context["code"]).count("def") + str(context["code"]).count("class")
        
        if "error" in context:
            signature["error_type"] = self._classify_error_type(str(context["error"]))
        
        if "requirements" in context:
            signature["requirements_complexity"] = len(str(context["requirements"]).split())
        
        # Add temporal context
        signature["time_of_day"] = datetime.now().hour
        signature["day_of_week"] = datetime.now().weekday()
        
        return signature
    
    def _find_similar_patterns(self, context_signature: Dict[str, Any]) -> List[LearningPattern]:
        """Find patterns similar to the given context."""
        similar = []
        
        for pattern in self.learning_patterns.values():
            similarity = self._calculate_similarity(context_signature, pattern.context_signature)
            if similarity > 0.6:  # 60% similarity threshold
                similar.append(pattern)
        
        return sorted(similar, key=lambda p: p.frequency, reverse=True)
    
    def _calculate_similarity(self, sig1: Dict[str, Any], sig2: Dict[str, Any]) -> float:
        """Calculate similarity between two context signatures."""
        common_keys = set(sig1.keys()) & set(sig2.keys())
        if not common_keys:
            return 0.0
        
        similarity_sum = 0.0
        for key in common_keys:
            if isinstance(sig1[key], (int, float)) and isinstance(sig2[key], (int, float)):
                # Numerical similarity
                max_val = max(abs(sig1[key]), abs(sig2[key]))
                if max_val == 0:
                    similarity_sum += 1.0
                else:
                    diff = abs(sig1[key] - sig2[key])
                    similarity_sum += 1.0 - (diff / max_val)
            elif sig1[key] == sig2[key]:
                # Exact match
                similarity_sum += 1.0
            else:
                # No match
                similarity_sum += 0.0
        
        return similarity_sum / len(common_keys)
    
    def _record_outcome(self, context_signature: Dict, approach: str, success: bool, 
                       quality_score: float, execution_time: float):
        """Record learning from an outcome."""
        pattern_id = self._generate_pattern_id(context_signature, approach)
        timestamp = datetime.now().isoformat()
        
        # Update or create learning pattern
        if pattern_id in self.learning_patterns:
            pattern = self.learning_patterns[pattern_id]
            pattern.frequency += 1
            pattern.last_seen = timestamp
            # Update outcome quality with exponential moving average
            alpha = 0.3
            pattern.outcome_quality = alpha * quality_score + (1 - alpha) * pattern.outcome_quality
        else:
            self.learning_patterns[pattern_id] = LearningPattern(
                pattern_id=pattern_id,
                pattern_type="success" if success else "failure",
                context_signature=context_signature,
                approach_used=approach,
                outcome_quality=quality_score,
                frequency=1,
                first_seen=timestamp,
                last_seen=timestamp
            )
        
        # Update performance metrics
        self._update_performance_metrics(approach, success, quality_score, execution_time)
        
        # Save knowledge base
        self.save_knowledge_base()
    
    def _record_failure(self, context_signature: Dict, approach: str, error: str, execution_time: float):
        """Record learning from a failure."""
        self._record_outcome(context_signature, approach, False, 0.0, execution_time)
    
    def _update_performance_metrics(self, approach: str, success: bool, quality_score: float, execution_time: float):
        """Update performance metrics for an approach."""
        if approach not in self.performance_metrics:
            self.performance_metrics[approach] = PerformanceMetric(
                approach_id=approach,
                success_rate=0.0,
                avg_confidence=0.0,
                avg_execution_time=0.0,
                cost_per_success=0.0,
                sample_count=0,
                last_updated=datetime.now().isoformat()
            )
        
        metric = self.performance_metrics[approach]
        
        # Update with exponential moving average
        alpha = 0.2
        metric.sample_count += 1
        
        if success:
            metric.success_rate = alpha * 1.0 + (1 - alpha) * metric.success_rate
            metric.avg_confidence = alpha * quality_score + (1 - alpha) * metric.avg_confidence
        else:
            metric.success_rate = alpha * 0.0 + (1 - alpha) * metric.success_rate
        
        metric.avg_execution_time = alpha * execution_time + (1 - alpha) * metric.avg_execution_time
        metric.cost_per_success = metric.avg_execution_time / max(metric.success_rate, 0.01)
        metric.last_updated = datetime.now().isoformat()
    
    def _calculate_recency_weight(self, timestamp: str) -> float:
        """Calculate weight based on how recent the pattern is."""
        try:
            pattern_time = datetime.fromisoformat(timestamp)
            age_days = (datetime.now() - pattern_time).days
            # Exponential decay with half-life of 30 days
            return 2 ** (-age_days / 30.0)
        except:
            return 0.1  # Very low weight for invalid timestamps
    
    def _assess_task_complexity(self, task: Dict[str, Any]) -> float:
        """Assess the complexity of a task (0.0 to 1.0)."""
        complexity = 0.0
        
        # Code complexity
        if "code" in task:
            code = str(task["code"])
            complexity += min(len(code) / 1000.0, 0.3)  # Length factor
            complexity += min(code.count("def") / 10.0, 0.2)  # Function factor
            complexity += min(code.count("class") / 5.0, 0.2)  # Class factor
        
        # Error complexity
        if "error" in task:
            error = str(task["error"])
            if any(word in error.lower() for word in ["traceback", "exception", "error"]):
                complexity += 0.2
        
        # Requirements complexity
        if "requirements" in task:
            req = str(task["requirements"])
            complexity += min(len(req.split()) / 50.0, 0.3)
        
        return min(complexity, 1.0)
    
    def _classify_error_type(self, error: str) -> str:
        """Classify error type for pattern matching."""
        error_lower = error.lower()
        
        if "syntax" in error_lower:
            return "syntax_error"
        elif "type" in error_lower:
            return "type_error"
        elif "index" in error_lower or "key" in error_lower:
            return "access_error"
        elif "import" in error_lower:
            return "import_error"
        elif "attribute" in error_lower:
            return "attribute_error"
        else:
            return "other_error"
    
    def _generate_pattern_id(self, context_signature: Dict, approach: str) -> str:
        """Generate unique ID for a pattern."""
        content = json.dumps(context_signature, sort_keys=True) + approach
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def _get_best_approach(self) -> Optional[str]:
        """Get the best performing approach."""
        if not self.performance_metrics:
            return None
        
        best_approach = None
        best_score = 0.0
        
        for approach, metric in self.performance_metrics.items():
            if metric.sample_count >= 3:  # Minimum sample size
                # Combined score: success rate * confidence / cost
                score = (metric.success_rate * metric.avg_confidence) / max(metric.cost_per_success, 0.01)
                if score > best_score:
                    best_score = score
                    best_approach = approach
        
        return best_approach
    
    def _get_common_failure_patterns(self) -> List[str]:
        """Get most common failure patterns."""
        failure_patterns = [p for p in self.learning_patterns.values() if p.pattern_type == "failure"]
        
        # Group by approach and count
        approach_failures = {}
        for pattern in failure_patterns:
            approach = pattern.approach_used
            approach_failures[approach] = approach_failures.get(approach, 0) + pattern.frequency
        
        # Sort by frequency
        sorted_failures = sorted(approach_failures.items(), key=lambda x: x[1], reverse=True)
        return [approach for approach, count in sorted_failures]
    
    def _calculate_learning_velocity(self) -> float:
        """Calculate how fast the system is learning."""
        if not self.learning_patterns:
            return 0.0
        
        # Count patterns created in last 7 days
        recent_patterns = 0
        cutoff = datetime.now().timestamp() - (7 * 24 * 3600)  # 7 days ago
        
        for pattern in self.learning_patterns.values():
            try:
                pattern_time = datetime.fromisoformat(pattern.first_seen).timestamp()
                if pattern_time > cutoff:
                    recent_patterns += 1
            except:
                continue
        
        return recent_patterns / 7.0  # Patterns per day
    
    def load_knowledge_base(self):
        """Load knowledge base from file."""
        if not self.knowledge_base_path.exists():
            return
        
        try:
            with open(self.knowledge_base_path, 'r') as f:
                data = json.load(f)
            
            # Load performance metrics
            if "performance_metrics" in data:
                for approach, metric_data in data["performance_metrics"].items():
                    self.performance_metrics[approach] = PerformanceMetric(**metric_data)
            
            # Load learning patterns
            if "learning_patterns" in data:
                for pattern_id, pattern_data in data["learning_patterns"].items():
                    self.learning_patterns[pattern_id] = LearningPattern(**pattern_data)
        
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
    
    def save_knowledge_base(self):
        """Save knowledge base to file."""
        data = {
            "performance_metrics": {k: v.dict() for k, v in self.performance_metrics.items()},
            "learning_patterns": {k: v.dict() for k, v in self.learning_patterns.items()}
        }
        
        try:
            self.knowledge_base_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.knowledge_base_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving knowledge base: {e}")


def create_self_improving_workflow(knowledge_base_path: str = "./atlas_meta_knowledge.json") -> SelfImprovingOptimizer:
    """Factory function to create self-improving workflow."""
    return SelfImprovingOptimizer(knowledge_base_path)