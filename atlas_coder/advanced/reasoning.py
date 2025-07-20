"""Advanced multi-hop reasoning chains for complex problem solving.

This module implements sophisticated DSPy patterns that can handle complex
debugging scenarios requiring multiple levels of analysis and reasoning.
"""

import json
from datetime import datetime
from typing import Any, Dict, List

import dspy
from pydantic import BaseModel


class ReasoningStep(BaseModel):
    """Single step in multi-hop reasoning chain."""
    step_id: int
    hypothesis: str
    evidence: str
    confidence: float
    next_steps: List[str]


class AdvancedDiagnosis(dspy.Signature):
    """Multi-hop reasoning for complex bug diagnosis."""
    
    code = dspy.InputField(desc="Code to analyze")
    error = dspy.InputField(desc="Error message or symptom")
    context = dspy.InputField(desc="Additional context about the system")
    previous_steps = dspy.InputField(desc="Previous reasoning steps taken")
    
    current_hypothesis = dspy.OutputField(desc="Current working hypothesis about the root cause")
    evidence_for = dspy.OutputField(desc="Evidence supporting this hypothesis")
    evidence_against = dspy.OutputField(desc="Evidence that contradicts this hypothesis")
    confidence_score = dspy.OutputField(desc="Confidence in this hypothesis (0-100)")
    next_investigation = dspy.OutputField(desc="Next steps to investigate")
    alternative_theories = dspy.OutputField(desc="Alternative theories to consider")


class SolutionValidation(dspy.Signature):
    """Validate proposed solutions against multiple criteria."""
    
    original_problem = dspy.InputField(desc="Original problem description")
    proposed_solution = dspy.InputField(desc="Proposed solution")
    code_context = dspy.InputField(desc="Surrounding code context")
    
    correctness_score = dspy.OutputField(desc="How likely is this solution to fix the problem (0-100)")
    side_effects = dspy.OutputField(desc="Potential negative side effects")
    performance_impact = dspy.OutputField(desc="Impact on system performance")
    maintainability = dspy.OutputField(desc="Impact on code maintainability")
    test_strategy = dspy.OutputField(desc="How to test this solution")
    improvement_suggestions = dspy.OutputField(desc="Ways to improve the solution")


class MultiHopReasoner(dspy.Module):
    """Advanced multi-hop reasoning module for complex problems."""
    
    def __init__(self, max_hops: int = 5):
        super().__init__()
        self.max_hops = max_hops
        self.diagnoser = dspy.ChainOfThought(AdvancedDiagnosis)
        self.validator = dspy.ChainOfThought(SolutionValidation)
        self.reasoning_history: List[ReasoningStep] = []
    
    def forward(self, code: str, error: str, context: str = "") -> Dict[str, Any]:
        """Execute multi-hop reasoning to solve complex problems."""
        
        self.reasoning_history.clear()
        current_step = 0
        previous_steps = ""
        
        while current_step < self.max_hops:
            # Perform diagnosis step
            diagnosis = self.diagnoser(
                code=code,
                error=error,
                context=context,
                previous_steps=previous_steps
            )
            
            # Create reasoning step
            step = ReasoningStep(
                step_id=current_step,
                hypothesis=diagnosis.current_hypothesis,
                evidence=diagnosis.evidence_for,
                confidence=float(diagnosis.confidence_score.split()[0]) / 100.0 if diagnosis.confidence_score else 0.5,
                next_steps=diagnosis.next_investigation.split('\n') if diagnosis.next_investigation else []
            )
            
            self.reasoning_history.append(step)
            
            # Check if we have high confidence or should continue
            if step.confidence > 0.8 or current_step == self.max_hops - 1:
                break
                
            # Prepare for next step
            previous_steps = self._format_reasoning_history()
            current_step += 1
        
        return {
            "final_hypothesis": self.reasoning_history[-1].hypothesis,
            "confidence": self.reasoning_history[-1].confidence,
            "reasoning_chain": [step.dict() for step in self.reasoning_history],
            "investigation_path": self._get_investigation_path(),
            "total_hops": len(self.reasoning_history)
        }
    
    def validate_solution(self, problem: str, solution: str, code_context: str) -> Dict[str, Any]:
        """Validate a proposed solution using multi-criteria analysis."""
        
        validation = self.validator(
            original_problem=problem,
            proposed_solution=solution,
            code_context=code_context
        )
        
        return {
            "correctness_score": validation.correctness_score,
            "side_effects": validation.side_effects,
            "performance_impact": validation.performance_impact,
            "maintainability": validation.maintainability,
            "test_strategy": validation.test_strategy,
            "improvements": validation.improvement_suggestions,
            "timestamp": datetime.now().isoformat()
        }
    
    def _format_reasoning_history(self) -> str:
        """Format reasoning history for next step input."""
        history = []
        for step in self.reasoning_history:
            history.append(f"Step {step.step_id}: {step.hypothesis} (confidence: {step.confidence:.2f})")
        return "\n".join(history)
    
    def _get_investigation_path(self) -> List[str]:
        """Get the path of investigation taken."""
        return [step.hypothesis for step in self.reasoning_history]


class AdaptiveProblemSolver(dspy.Module):
    """Self-adapting problem solver that learns from failures."""
    
    def __init__(self):
        super().__init__()
        self.reasoner = MultiHopReasoner()
        self.failure_patterns: List[Dict[str, Any]] = []
        self.success_patterns: List[Dict[str, Any]] = []
    
    def forward(self, problem_description: str, code: str, error: str) -> Dict[str, Any]:
        """Solve problem while learning from past patterns."""
        
        # Check for similar past problems
        similar_failures = self._find_similar_patterns(problem_description, self.failure_patterns)
        similar_successes = self._find_similar_patterns(problem_description, self.success_patterns)
        
        # Incorporate learnings into context
        context = self._build_context_from_patterns(similar_failures, similar_successes)
        
        # Perform multi-hop reasoning
        result = self.reasoner(code=code, error=error, context=context)
        
        # Store pattern for future learning
        pattern = {
            "problem": problem_description,
            "code_signature": self._get_code_signature(code),
            "error_type": self._classify_error(error),
            "solution_approach": result["final_hypothesis"],
            "confidence": result["confidence"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Classify as success or failure based on confidence
        if result["confidence"] > 0.7:
            self.success_patterns.append(pattern)
        else:
            self.failure_patterns.append(pattern)
        
        result["learning_applied"] = len(similar_successes) > 0
        result["patterns_found"] = len(similar_failures) + len(similar_successes)
        
        return result
    
    def _find_similar_patterns(self, problem: str, patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find similar patterns in the knowledge base."""
        # Simple similarity matching - in production would use embeddings
        similar = []
        problem_words = set(problem.lower().split())
        
        for pattern in patterns:
            pattern_words = set(pattern["problem"].lower().split())
            similarity = len(problem_words & pattern_words) / len(problem_words | pattern_words)
            if similarity > 0.3:  # 30% similarity threshold
                similar.append(pattern)
        
        return similar[:3]  # Return top 3 similar patterns
    
    def _build_context_from_patterns(self, failures: List[Dict], successes: List[Dict]) -> str:
        """Build context string from similar patterns."""
        context_parts = []
        
        if successes:
            context_parts.append("Similar successful approaches:")
            for success in successes:
                context_parts.append(f"- {success['solution_approach']}")
        
        if failures:
            context_parts.append("Approaches that failed in similar cases:")
            for failure in failures:
                context_parts.append(f"- {failure['solution_approach']}")
        
        return "\n".join(context_parts)
    
    def _get_code_signature(self, code: str) -> str:
        """Get a signature representing the code structure."""
        # Simple signature - count of different elements
        lines = code.split('\n')
        functions = len([l for l in lines if 'def ' in l])
        classes = len([l for l in lines if 'class ' in l])
        imports = len([l for l in lines if 'import ' in l or 'from ' in l])
        
        return f"func:{functions},class:{classes},import:{imports},lines:{len(lines)}"
    
    def _classify_error(self, error: str) -> str:
        """Classify the type of error."""
        error_lower = error.lower()
        
        if 'indexerror' in error_lower or 'keyerror' in error_lower:
            return "access_error"
        elif 'typeerror' in error_lower:
            return "type_error"
        elif 'valueerror' in error_lower:
            return "value_error"
        elif 'attributeerror' in error_lower:
            return "attribute_error"
        elif 'nameerror' in error_lower:
            return "name_error"
        else:
            return "other_error"


class IntelligentCacher(dspy.Module):
    """Intelligent caching with semantic similarity matching."""
    
    def __init__(self, cache_file: str = "./advanced_cache.json"):
        super().__init__()
        self.cache_file = cache_file
        self.cache_data = self._load_cache()
    
    def get_cached_result(self, problem: str, code: str) -> Dict[str, Any] | None:
        """Get cached result if semantically similar problem exists."""
        problem_signature = self._get_problem_signature(problem, code)
        
        for cached_item in self.cache_data:
            if self._calculate_similarity(problem_signature, cached_item["signature"]) > 0.8:
                cached_item["cache_hit"] = True
                cached_item["hit_timestamp"] = datetime.now().isoformat()
                return cached_item["result"]
        
        return None
    
    def cache_result(self, problem: str, code: str, result: Dict[str, Any]) -> None:
        """Cache a result with semantic signature."""
        signature = self._get_problem_signature(problem, code)
        
        cache_entry = {
            "signature": signature,
            "problem": problem,
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "access_count": 1
        }
        
        self.cache_data.append(cache_entry)
        self._save_cache()
    
    def _get_problem_signature(self, problem: str, code: str) -> Dict[str, Any]:
        """Create semantic signature for problem and code."""
        return {
            "problem_length": len(problem.split()),
            "problem_keywords": sorted(set(problem.lower().split())),
            "code_length": len(code.split()),
            "code_complexity": code.count('def') + code.count('class') + code.count('if'),
            "error_indicators": [word for word in problem.lower().split() if 'error' in word]
        }
    
    def _calculate_similarity(self, sig1: Dict, sig2: Dict) -> float:
        """Calculate similarity between two problem signatures."""
        keyword_overlap = len(set(sig1["problem_keywords"]) & set(sig2["problem_keywords"]))
        keyword_union = len(set(sig1["problem_keywords"]) | set(sig2["problem_keywords"]))
        
        if keyword_union == 0:
            return 0.0
        
        keyword_similarity = keyword_overlap / keyword_union
        
        # Length similarity
        length_similarity = 1 - abs(sig1["problem_length"] - sig2["problem_length"]) / max(sig1["problem_length"], sig2["problem_length"])
        
        # Complexity similarity  
        complexity_similarity = 1 - abs(sig1["code_complexity"] - sig2["code_complexity"]) / max(sig1["code_complexity"], sig2["code_complexity"], 1)
        
        return (keyword_similarity * 0.5 + length_similarity * 0.3 + complexity_similarity * 0.2)
    
    def _load_cache(self) -> List[Dict[str, Any]]:
        """Load cache from file."""
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_cache(self) -> None:
        """Save cache to file."""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache_data, f, indent=2)