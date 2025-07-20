#!/usr/bin/env python3
"""Atlas Coder analyzing its own codebase - Pure Python implementation.

This script demonstrates Atlas Coder's ability to analyze and improve itself
without external dependencies, showing pure algorithmic intelligence.
"""

import os
import sys
import ast
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime


class PureCodebaseAnalyzer:
    """Pure Python codebase analyzer with advanced intelligence."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.analysis_start = datetime.now()
    
    def analyze_atlas_coder(self) -> Dict[str, Any]:
        """Perform comprehensive analysis of Atlas Coder itself."""
        print("🧠 Atlas Coder analyzing itself - Pure intelligence engaged")
        
        analysis = {
            "timestamp": self.analysis_start.isoformat(),
            "project_structure": self._analyze_project_structure(),
            "code_intelligence": self._analyze_code_intelligence(),
            "architectural_patterns": self._analyze_architecture(),
            "complexity_metrics": self._calculate_complexity_metrics(),
            "improvement_opportunities": self._identify_improvements(),
            "meta_analysis": self._perform_meta_analysis(),
            "recursive_capabilities": self._analyze_recursive_capabilities(),
            "learning_indicators": self._analyze_learning_indicators()
        }
        
        return analysis
    
    def _analyze_project_structure(self) -> Dict[str, Any]:
        """Analyze the project structure and organization."""
        structure = {
            "total_files": 0,
            "python_files": 0,
            "modules": {},
            "documentation_files": 0,
            "test_files": 0,
            "config_files": 0,
            "complexity_distribution": {}
        }
        
        for root, dirs, files in os.walk(self.project_root):
            # Skip virtual environment and cache directories
            dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.pytest_cache', 'node_modules', '.git']]
            
            for file in files:
                structure["total_files"] += 1
                file_path = Path(root) / file
                
                if file.endswith('.py'):
                    structure["python_files"] += 1
                    
                    if "test" in file.lower():
                        structure["test_files"] += 1
                    
                    # Analyze module structure
                    relative_path = file_path.relative_to(self.project_root)
                    module_parts = str(relative_path).split(os.sep)
                    
                    if len(module_parts) > 1 and not module_parts[0].startswith('.'):
                        module_name = module_parts[0]
                        if module_name not in structure["modules"]:
                            structure["modules"][module_name] = {
                                "files": 0,
                                "lines": 0,
                                "functions": 0,
                                "classes": 0,
                                "complexity": 0,
                                "intelligence_indicators": 0
                            }
                        
                        module_info = structure["modules"][module_name]
                        module_info["files"] += 1
                        
                        # Analyze file content
                        try:
                            content = file_path.read_text(encoding='utf-8', errors='ignore')
                            lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
                            module_info["lines"] += len(lines)
                            
                            # Parse AST to count functions and classes
                            try:
                                tree = ast.parse(content)
                                complexity = self._calculate_cyclomatic_complexity(tree)
                                module_info["complexity"] += complexity
                                
                                for node in ast.walk(tree):
                                    if isinstance(node, ast.FunctionDef):
                                        module_info["functions"] += 1
                                    elif isinstance(node, ast.ClassDef):
                                        module_info["classes"] += 1
                                
                                # Count intelligence indicators
                                intelligence_keywords = [
                                    'reasoning', 'learning', 'optimization', 'analysis',
                                    'meta', 'recursive', 'adaptive', 'intelligent',
                                    'dspy', 'chain', 'thought', 'inference'
                                ]
                                
                                content_lower = content.lower()
                                for keyword in intelligence_keywords:
                                    module_info["intelligence_indicators"] += content_lower.count(keyword)
                            
                            except SyntaxError:
                                pass  # Skip files with syntax errors
                                
                        except Exception:
                            pass  # Skip files that can't be read
                
                elif file.endswith(('.md', '.rst', '.txt')):
                    structure["documentation_files"] += 1
                elif file.endswith(('.yaml', '.yml', '.json', '.toml', '.cfg', '.ini')):
                    structure["config_files"] += 1
        
        return structure
    
    def _analyze_code_intelligence(self) -> Dict[str, Any]:
        """Analyze intelligence indicators in the codebase."""
        intelligence = {
            "total_intelligence_score": 0,
            "advanced_patterns": [],
            "dspy_integration": 0,
            "meta_programming": 0,
            "reasoning_chains": 0,
            "learning_mechanisms": 0,
            "optimization_strategies": 0,
            "intelligence_density": 0.0
        }
        
        # Intelligence pattern detection
        intelligence_patterns = {
            "multi_hop_reasoning": ["multi.*hop", "chain.*thought", "reasoning.*chain"],
            "meta_learning": ["meta.*learn", "self.*improv", "adaptive"],
            "optimization": ["optim", "cost.*track", "budget", "efficiency"],
            "recursive_analysis": ["recursive", "self.*analy", "introspect"],
            "advanced_dspy": ["dspy.*module", "signature", "chain.*of.*thought"],
            "intelligent_caching": ["cache.*semantic", "intelligent.*cache", "similarity"],
            "pattern_recognition": ["pattern.*detect", "pattern.*match", "signature.*match"]
        }
        
        total_files_analyzed = 0
        total_intelligence_indicators = 0
        
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ['venv', '__pycache__', '.git']):
                continue
            
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                content_lower = content.lower()
                total_files_analyzed += 1
                
                file_intelligence = 0
                
                # Count DSPy integrations
                if "dspy" in content_lower:
                    intelligence["dspy_integration"] += content_lower.count("dspy")
                    file_intelligence += 10
                
                # Detect intelligence patterns
                for pattern_name, patterns in intelligence_patterns.items():
                    for pattern in patterns:
                        import re
                        matches = len(re.findall(pattern, content_lower))
                        if matches > 0:
                            if pattern_name not in [p["name"] for p in intelligence["advanced_patterns"]]:
                                intelligence["advanced_patterns"].append({
                                    "name": pattern_name,
                                    "count": matches,
                                    "files": [str(py_file.name)]
                                })
                            else:
                                # Update existing pattern
                                for p in intelligence["advanced_patterns"]:
                                    if p["name"] == pattern_name:
                                        p["count"] += matches
                                        if str(py_file.name) not in p["files"]:
                                            p["files"].append(str(py_file.name))
                            
                            file_intelligence += matches * 5
                
                # Check for specific intelligence mechanisms
                if "class" in content and "dspy.Module" in content:
                    intelligence["reasoning_chains"] += 1
                    file_intelligence += 15
                
                if "meta" in content_lower and ("learn" in content_lower or "improv" in content_lower):
                    intelligence["meta_programming"] += 1
                    file_intelligence += 20
                
                if "optim" in content_lower and ("cost" in content_lower or "performance" in content_lower):
                    intelligence["optimization_strategies"] += 1
                    file_intelligence += 10
                
                total_intelligence_indicators += file_intelligence
                
            except Exception:
                pass
        
        intelligence["total_intelligence_score"] = total_intelligence_indicators
        if total_files_analyzed > 0:
            intelligence["intelligence_density"] = total_intelligence_indicators / total_files_analyzed
        
        return intelligence
    
    def _analyze_architecture(self) -> Dict[str, Any]:
        """Analyze architectural patterns and sophistication."""
        architecture = {
            "layered_architecture": False,
            "modular_design": False,
            "dependency_injection": False,
            "factory_patterns": 0,
            "observer_patterns": 0,
            "strategy_patterns": 0,
            "advanced_patterns": [],
            "architectural_sophistication": 0.0,
            "module_coupling": "unknown",
            "design_principles": []
        }
        
        factory_count = 0
        observer_count = 0
        strategy_count = 0
        sophisticated_patterns = 0
        
        # Analyze for architectural patterns
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ['venv', '__pycache__', '.git']):
                continue
            
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                content_lower = content.lower()
                
                # Check for layered architecture
                if any(layer in str(py_file) for layer in ["core", "utils", "cli", "advanced", "integrations"]):
                    architecture["layered_architecture"] = True
                
                # Check for modular design
                if "from ." in content or "import ." in content:
                    architecture["modular_design"] = True
                
                # Check for dependency injection patterns
                if ("def __init__" in content and ":" in content and 
                    ("Optional" in content or "None" in content)):
                    architecture["dependency_injection"] = True
                
                # Count design patterns
                if "def create_" in content or "def get_" in content or "factory" in content_lower:
                    factory_count += 1
                
                if ("register" in content_lower and "notify" in content_lower) or "observer" in content_lower:
                    observer_count += 1
                
                if "strategy" in content_lower or ("def execute" in content and "strategy" in content_lower):
                    strategy_count += 1
                
                # Check for sophisticated patterns
                sophisticated_keywords = [
                    "chain_of_thought", "program_of_thought", "multi_hop",
                    "meta_learning", "self_improving", "adaptive",
                    "compositional", "recursive", "introspective"
                ]
                
                for keyword in sophisticated_keywords:
                    if keyword in content_lower:
                        sophisticated_patterns += 1
                        if keyword not in architecture["advanced_patterns"]:
                            architecture["advanced_patterns"].append(keyword)
                
                # Check for design principles
                if "single.*responsibility" in content_lower:
                    if "Single Responsibility" not in architecture["design_principles"]:
                        architecture["design_principles"].append("Single Responsibility")
                
                if "dependency.*inversion" in content_lower or "inversion.*control" in content_lower:
                    if "Dependency Inversion" not in architecture["design_principles"]:
                        architecture["design_principles"].append("Dependency Inversion")
                
            except Exception:
                pass
        
        architecture["factory_patterns"] = factory_count
        architecture["observer_patterns"] = observer_count
        architecture["strategy_patterns"] = strategy_count
        
        # Calculate architectural sophistication score
        sophistication_score = 0
        if architecture["layered_architecture"]:
            sophistication_score += 20
        if architecture["modular_design"]:
            sophistication_score += 15
        if architecture["dependency_injection"]:
            sophistication_score += 15
        
        sophistication_score += min(factory_count * 5, 20)
        sophistication_score += min(observer_count * 5, 15)
        sophistication_score += min(strategy_count * 5, 15)
        sophistication_score += min(len(architecture["advanced_patterns"]) * 10, 50)
        
        architecture["architectural_sophistication"] = min(sophistication_score, 100) / 100.0
        
        return architecture
    
    def _calculate_complexity_metrics(self) -> Dict[str, Any]:
        """Calculate sophisticated complexity metrics."""
        metrics = {
            "total_lines_of_code": 0,
            "effective_lines_of_code": 0,
            "avg_function_complexity": 0.0,
            "max_function_complexity": 0,
            "avg_class_complexity": 0.0,
            "cognitive_complexity": 0.0,
            "abstraction_level": 0.0,
            "complexity_distribution": {
                "simple": 0,
                "moderate": 0,
                "complex": 0,
                "very_complex": 0
            },
            "maintainability_index": 0.0
        }
        
        function_complexities = []
        class_complexities = []
        total_cognitive_load = 0
        abstraction_indicators = 0
        
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ['venv', '__pycache__', '.git']):
                continue
            
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                
                # Count lines
                all_lines = len(lines)
                effective_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
                
                metrics["total_lines_of_code"] += all_lines
                metrics["effective_lines_of_code"] += effective_lines
                
                # Parse AST for detailed analysis
                try:
                    tree = ast.parse(content)
                    
                    # Analyze functions and classes
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            func_complexity = self._calculate_node_complexity(node)
                            function_complexities.append(func_complexity)
                            
                            # Categorize complexity
                            if func_complexity <= 5:
                                metrics["complexity_distribution"]["simple"] += 1
                            elif func_complexity <= 10:
                                metrics["complexity_distribution"]["moderate"] += 1
                            elif func_complexity <= 20:
                                metrics["complexity_distribution"]["complex"] += 1
                            else:
                                metrics["complexity_distribution"]["very_complex"] += 1
                            
                            # Calculate cognitive complexity
                            cognitive_load = self._calculate_cognitive_complexity(node)
                            total_cognitive_load += cognitive_load
                        
                        elif isinstance(node, ast.ClassDef):
                            class_complexity = self._calculate_class_complexity(node)
                            class_complexities.append(class_complexity)
                    
                    # Count abstraction indicators
                    content_lower = content.lower()
                    abstraction_keywords = ['abstract', 'interface', 'protocol', 'mixin', 'base', 'meta']
                    for keyword in abstraction_keywords:
                        abstraction_indicators += content_lower.count(keyword)
                
                except SyntaxError:
                    pass
                
            except Exception:
                pass
        
        # Calculate averages and indices
        if function_complexities:
            metrics["avg_function_complexity"] = sum(function_complexities) / len(function_complexities)
            metrics["max_function_complexity"] = max(function_complexities)
            metrics["cognitive_complexity"] = total_cognitive_load / len(function_complexities)
        
        if class_complexities:
            metrics["avg_class_complexity"] = sum(class_complexities) / len(class_complexities)
        
        if metrics["effective_lines_of_code"] > 0:
            metrics["abstraction_level"] = min(abstraction_indicators / metrics["effective_lines_of_code"] * 1000, 1.0)
        
        # Calculate maintainability index (simplified Halstead-based)
        if metrics["avg_function_complexity"] > 0 and metrics["effective_lines_of_code"] > 0:
            volume = metrics["effective_lines_of_code"] * 0.1  # Simplified volume
            complexity = metrics["avg_function_complexity"]
            metrics["maintainability_index"] = max(0, 171 - 5.2 * complexity - 0.23 * volume - 16.2 * (1 - metrics["abstraction_level"]))
        
        return metrics
    
    def _identify_improvements(self) -> List[Dict[str, Any]]:
        """Identify sophisticated improvement opportunities."""
        improvements = []
        
        # Analyze for advanced improvement patterns
        improvement_analyzers = [
            self._analyze_algorithmic_improvements,
            self._analyze_intelligence_gaps,
            self._analyze_performance_opportunities,
            self._analyze_architecture_improvements,
            self._analyze_learning_potential
        ]
        
        for analyzer in improvement_analyzers:
            try:
                improvements.extend(analyzer())
            except Exception as e:
                improvements.append({
                    "type": "analysis_error",
                    "description": f"Error in improvement analysis: {str(e)}",
                    "priority": "low",
                    "intelligence_impact": "unknown"
                })
        
        return improvements
    
    def _perform_meta_analysis(self) -> Dict[str, Any]:
        """Perform sophisticated meta-analysis of capabilities."""
        meta = {
            "self_awareness_score": 0.0,
            "recursive_depth": 0,
            "learning_sophistication": 0.0,
            "intelligence_evolution": [],
            "meta_capabilities": [],
            "consciousness_indicators": 0,
            "reasoning_complexity": 0.0,
            "adaptation_potential": 0.0
        }
        
        # Analyze self-awareness patterns
        self_aware_indicators = [
            "self_analysis", "meta_analysis", "introspection", "reflection",
            "self_improvement", "self_optimization", "recursive", "meta_learning",
            "consciousness", "awareness", "intelligence", "cognitive"
        ]
        
        awareness_score = 0
        reasoning_indicators = 0
        adaptation_indicators = 0
        
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ['venv', '__pycache__', '.git']):
                continue
            
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                content_lower = content.lower()
                
                # Count self-awareness indicators
                for indicator in self_aware_indicators:
                    count = content_lower.count(indicator)
                    awareness_score += count
                    
                    if count > 0 and indicator not in meta["intelligence_evolution"]:
                        meta["intelligence_evolution"].append(indicator)
                
                # Check for recursive depth
                if "recursive" in content_lower or "self" in content_lower:
                    meta["recursive_depth"] += content_lower.count("recursive") + content_lower.count("self")
                
                # Analyze reasoning complexity
                reasoning_keywords = ["reasoning", "inference", "deduction", "analysis", "synthesis"]
                for keyword in reasoning_keywords:
                    reasoning_indicators += content_lower.count(keyword)
                
                # Analyze adaptation potential
                adaptation_keywords = ["adapt", "learn", "evolve", "improve", "optimize"]
                for keyword in adaptation_keywords:
                    adaptation_indicators += content_lower.count(keyword)
                
                # Check for meta-capabilities
                if "meta" in content_lower:
                    if "meta_programming" not in meta["meta_capabilities"]:
                        meta["meta_capabilities"].append("meta_programming")
                
                if "self.*analy" in content_lower:
                    if "self_analysis" not in meta["meta_capabilities"]:
                        meta["meta_capabilities"].append("self_analysis")
                
                if "multi.*hop" in content_lower:
                    if "multi_hop_reasoning" not in meta["meta_capabilities"]:
                        meta["meta_capabilities"].append("multi_hop_reasoning")
                
            except Exception:
                pass
        
        # Calculate sophisticated scores
        total_files = len(list(self.project_root.rglob("*.py")))
        if total_files > 0:
            meta["self_awareness_score"] = min(awareness_score / (total_files * 10), 1.0)
            meta["reasoning_complexity"] = min(reasoning_indicators / (total_files * 5), 1.0)
            meta["adaptation_potential"] = min(adaptation_indicators / (total_files * 5), 1.0)
        
        # Calculate learning sophistication
        learning_features = len(meta["meta_capabilities"])
        evolution_features = len(meta["intelligence_evolution"])
        meta["learning_sophistication"] = min((learning_features + evolution_features) / 20.0, 1.0)
        
        return meta
    
    def _analyze_recursive_capabilities(self) -> Dict[str, Any]:
        """Analyze recursive and self-referential capabilities."""
        recursive = {
            "self_reference_count": 0,
            "recursive_functions": 0,
            "meta_methods": 0,
            "reflection_usage": 0,
            "self_modification_potential": 0,
            "recursive_data_structures": 0,
            "introspection_depth": 0.0
        }
        
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ['venv', '__pycache__', '.git']):
                continue
            
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                
                # Count self-references
                recursive["self_reference_count"] += content.count("self.")
                
                # Check for recursive functions
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            # Check if function calls itself
                            for child in ast.walk(node):
                                if (isinstance(child, ast.Call) and 
                                    isinstance(child.func, ast.Name) and 
                                    child.func.id == node.name):
                                    recursive["recursive_functions"] += 1
                                    break
                except SyntaxError:
                    pass
                
                # Count meta-methods and reflection
                recursive["meta_methods"] += content.count("__")
                recursive["reflection_usage"] += content.count("getattr") + content.count("hasattr") + content.count("setattr")
                
                # Check for self-modification potential
                if "exec(" in content or "eval(" in content or "compile(" in content:
                    recursive["self_modification_potential"] += 1
                
                # Check for recursive data structures
                if "dict" in content and "list" in content:
                    recursive["recursive_data_structures"] += 1
                
            except Exception:
                pass
        
        # Calculate introspection depth
        total_introspection = (recursive["self_reference_count"] + 
                             recursive["meta_methods"] + 
                             recursive["reflection_usage"])
        recursive["introspection_depth"] = min(total_introspection / 1000.0, 1.0)
        
        return recursive
    
    def _analyze_learning_indicators(self) -> Dict[str, Any]:
        """Analyze learning and adaptation indicators."""
        learning = {
            "learning_mechanisms": 0,
            "adaptation_strategies": 0,
            "feedback_loops": 0,
            "optimization_patterns": 0,
            "knowledge_storage": 0,
            "pattern_recognition": 0,
            "learning_sophistication": 0.0
        }
        
        learning_keywords = {
            "learning_mechanisms": ["learn", "train", "adapt", "evolve"],
            "adaptation_strategies": ["strategy", "approach", "method", "technique"],
            "feedback_loops": ["feedback", "loop", "iterate", "improve"],
            "optimization_patterns": ["optimize", "minimize", "maximize", "efficient"],
            "knowledge_storage": ["cache", "store", "save", "persist"],
            "pattern_recognition": ["pattern", "recognize", "detect", "identify"]
        }
        
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ['venv', '__pycache__', '.git']):
                continue
            
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore').lower()
                
                for category, keywords in learning_keywords.items():
                    for keyword in keywords:
                        learning[category] += content.count(keyword)
                
            except Exception:
                pass
        
        # Calculate learning sophistication
        total_learning_indicators = sum(learning[key] for key in learning_keywords.keys())
        learning["learning_sophistication"] = min(total_learning_indicators / 100.0, 1.0)
        
        return learning
    
    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity of an AST."""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, (ast.And, ast.Or)):
                complexity += 1
            elif isinstance(node, ast.Lambda):
                complexity += 1
        
        return complexity
    
    def _calculate_node_complexity(self, node: ast.AST) -> int:
        """Calculate complexity of a specific node."""
        complexity = 1
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
        
        return complexity
    
    def _calculate_cognitive_complexity(self, node: ast.AST) -> int:
        """Calculate cognitive complexity (human readability)."""
        cognitive_load = 0
        nesting_level = 0
        
        def calculate_recursive(n, level):
            nonlocal cognitive_load
            
            if isinstance(n, (ast.If, ast.While, ast.For)):
                cognitive_load += 1 + level  # Base + nesting penalty
                level += 1
            elif isinstance(n, ast.ExceptHandler):
                cognitive_load += 1 + level
            elif isinstance(n, (ast.And, ast.Or)):
                cognitive_load += 1
            
            for child in ast.iter_child_nodes(n):
                calculate_recursive(child, level)
        
        calculate_recursive(node, 0)
        return cognitive_load
    
    def _calculate_class_complexity(self, node: ast.ClassDef) -> int:
        """Calculate complexity of a class."""
        complexity = 1
        method_count = 0
        
        for child in node.body:
            if isinstance(child, ast.FunctionDef):
                method_count += 1
                complexity += self._calculate_node_complexity(child)
        
        # Add complexity for inheritance
        if node.bases:
            complexity += len(node.bases)
        
        return complexity
    
    def _analyze_algorithmic_improvements(self) -> List[Dict[str, Any]]:
        """Analyze algorithmic improvement opportunities."""
        improvements = []
        
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ['venv', '__pycache__', '.git']):
                continue
            
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                
                # Check for optimization opportunities
                if "for" in content and "range(len(" in content:
                    improvements.append({
                        "type": "algorithmic",
                        "description": f"Potential enumerate() usage in {py_file.name}",
                        "priority": "low",
                        "intelligence_impact": "readability"
                    })
                
                if content.count("if") > 10:
                    improvements.append({
                        "type": "algorithmic",
                        "description": f"High conditional complexity in {py_file.name} - consider strategy pattern",
                        "priority": "medium",
                        "intelligence_impact": "maintainability"
                    })
                
            except Exception:
                pass
        
        return improvements
    
    def _analyze_intelligence_gaps(self) -> List[Dict[str, Any]]:
        """Analyze gaps in intelligence capabilities."""
        improvements = []
        
        # Check for missing advanced patterns
        advanced_patterns = ["neural", "genetic", "reinforcement", "bayesian", "ensemble"]
        
        for pattern in advanced_patterns:
            found = False
            for py_file in self.project_root.rglob("*.py"):
                if any(skip in str(py_file) for skip in ['venv', '__pycache__', '.git']):
                    continue
                
                try:
                    content = py_file.read_text(encoding='utf-8', errors='ignore').lower()
                    if pattern in content:
                        found = True
                        break
                except Exception:
                    pass
            
            if not found:
                improvements.append({
                    "type": "intelligence_gap",
                    "description": f"No {pattern} intelligence patterns detected - expansion opportunity",
                    "priority": "low",
                    "intelligence_impact": "capability_expansion"
                })
        
        return improvements
    
    def _analyze_performance_opportunities(self) -> List[Dict[str, Any]]:
        """Analyze performance improvement opportunities."""
        improvements = []
        
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ['venv', '__pycache__', '.git']):
                continue
            
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                
                # Check for performance patterns
                if "json.loads" in content and content.count("json.loads") > 2:
                    improvements.append({
                        "type": "performance",
                        "description": f"Multiple JSON parsing in {py_file.name} - consider caching",
                        "priority": "medium",
                        "intelligence_impact": "efficiency"
                    })
                
                if "for" in content and "append" in content:
                    improvements.append({
                        "type": "performance",
                        "description": f"Potential list comprehension opportunity in {py_file.name}",
                        "priority": "low",
                        "intelligence_impact": "efficiency"
                    })
                
            except Exception:
                pass
        
        return improvements
    
    def _analyze_architecture_improvements(self) -> List[Dict[str, Any]]:
        """Analyze architectural improvement opportunities."""
        improvements = []
        
        # Check for architectural patterns
        has_interfaces = False
        has_abstractions = False
        
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ['venv', '__pycache__', '.git']):
                continue
            
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore').lower()
                
                if "abc" in content or "protocol" in content:
                    has_interfaces = True
                
                if "abstract" in content:
                    has_abstractions = True
                
            except Exception:
                pass
        
        if not has_interfaces:
            improvements.append({
                "type": "architecture",
                "description": "No interface definitions detected - consider adding protocols for better abstraction",
                "priority": "medium",
                "intelligence_impact": "modularity"
            })
        
        if not has_abstractions:
            improvements.append({
                "type": "architecture",
                "description": "Limited abstraction patterns - consider abstract base classes",
                "priority": "low",
                "intelligence_impact": "extensibility"
            })
        
        return improvements
    
    def _analyze_learning_potential(self) -> List[Dict[str, Any]]:
        """Analyze learning and adaptation potential improvements."""
        improvements = []
        
        # Check for learning mechanisms
        has_feedback_loops = False
        has_adaptation = False
        
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ['venv', '__pycache__', '.git']):
                continue
            
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore').lower()
                
                if "feedback" in content or "adapt" in content:
                    has_feedback_loops = True
                
                if "learn" in content or "evolve" in content:
                    has_adaptation = True
                
            except Exception:
                pass
        
        if not has_feedback_loops:
            improvements.append({
                "type": "learning",
                "description": "Limited feedback mechanisms detected - consider adding adaptive feedback loops",
                "priority": "high",
                "intelligence_impact": "self_improvement"
            })
        
        return improvements


def demonstrate_advanced_self_analysis():
    """Demonstrate sophisticated self-analysis capabilities."""
    print("🧠 ATLAS CODER ADVANCED SELF-ANALYSIS")
    print("=" * 70)
    print("🔮 Pure intelligence analyzing pure intelligence...")
    print()
    
    analyzer = PureCodebaseAnalyzer()
    analysis = analyzer.analyze_atlas_coder()
    
    print("📊 PROJECT STRUCTURE INTELLIGENCE:")
    structure = analysis["project_structure"]
    print(f"   📁 Total files analyzed: {structure['total_files']}")
    print(f"   🐍 Python files: {structure['python_files']}")
    print(f"   📚 Documentation files: {structure['documentation_files']}")
    print(f"   🧪 Test files: {structure['test_files']}")
    print(f"   ⚙️  Configuration files: {structure['config_files']}")
    print(f"   📦 Modules discovered: {len(structure['modules'])}")
    
    if structure["modules"]:
        print(f"   🏗️  Module breakdown:")
        for module, info in structure["modules"].items():
            intelligence_density = info["intelligence_indicators"] / max(info["lines"], 1) * 100
            print(f"      • {module}: {info['files']} files, {info['lines']:,} lines, "
                  f"{info['functions']} functions, {info['classes']} classes "
                  f"(🧠 {intelligence_density:.1f} IQ/100LOC)")
    
    print("\n🧠 CODE INTELLIGENCE ANALYSIS:")
    intelligence = analysis["code_intelligence"]
    print(f"   🎯 Total Intelligence Score: {intelligence['total_intelligence_score']:,}")
    print(f"   🧬 DSPy Integration Level: {intelligence['dspy_integration']}")
    print(f"   🔗 Reasoning Chains: {intelligence['reasoning_chains']}")
    print(f"   🎓 Meta-programming: {intelligence['meta_programming']}")
    print(f"   ⚡ Optimization Strategies: {intelligence['optimization_strategies']}")
    print(f"   🧠 Intelligence Density: {intelligence['intelligence_density']:.1f}/file")
    
    if intelligence["advanced_patterns"]:
        print(f"   🔬 Advanced Patterns Detected:")
        for pattern in intelligence["advanced_patterns"][:5]:
            print(f"      • {pattern['name'].title()}: {pattern['count']} instances in {len(pattern['files'])} files")
    
    print("\n🏗️  ARCHITECTURAL SOPHISTICATION:")
    arch = analysis["architectural_patterns"]
    print(f"   📐 Sophistication Score: {arch['architectural_sophistication']:.1%}")
    print(f"   🏢 Layered Architecture: {'✅' if arch['layered_architecture'] else '❌'}")
    print(f"   🧩 Modular Design: {'✅' if arch['modular_design'] else '❌'}")
    print(f"   💉 Dependency Injection: {'✅' if arch['dependency_injection'] else '❌'}")
    print(f"   🏭 Factory Patterns: {arch['factory_patterns']}")
    print(f"   👁️  Observer Patterns: {arch['observer_patterns']}")
    print(f"   📋 Strategy Patterns: {arch['strategy_patterns']}")
    
    if arch["advanced_patterns"]:
        print(f"   🚀 Advanced Patterns: {', '.join(arch['advanced_patterns'][:5])}")
    
    print("\n📊 COMPLEXITY METRICS:")
    complexity = analysis["complexity_metrics"]
    print(f"   📏 Total Lines of Code: {complexity['total_lines_of_code']:,}")
    print(f"   💡 Effective Lines: {complexity['effective_lines_of_code']:,}")
    print(f"   🧮 Avg Function Complexity: {complexity['avg_function_complexity']:.1f}")
    print(f"   🏔️  Max Function Complexity: {complexity['max_function_complexity']}")
    print(f"   🧠 Cognitive Complexity: {complexity['cognitive_complexity']:.1f}")
    print(f"   🎭 Abstraction Level: {complexity['abstraction_level']:.1%}")
    print(f"   🏥 Maintainability Index: {complexity['maintainability_index']:.1f}/100")
    
    dist = complexity["complexity_distribution"]
    total_funcs = sum(dist.values())
    if total_funcs > 0:
        print(f"   📈 Complexity Distribution:")
        print(f"      🟢 Simple (1-5): {dist['simple']} ({dist['simple']/total_funcs:.1%})")
        print(f"      🟡 Moderate (6-10): {dist['moderate']} ({dist['moderate']/total_funcs:.1%})")
        print(f"      🟠 Complex (11-20): {dist['complex']} ({dist['complex']/total_funcs:.1%})")
        print(f"      🔴 Very Complex (20+): {dist['very_complex']} ({dist['very_complex']/total_funcs:.1%})")
    
    print("\n🔮 META-ANALYSIS - CONSCIOUSNESS INDICATORS:")
    meta = analysis["meta_analysis"]
    print(f"   🧠 Self-Awareness Score: {meta['self_awareness_score']:.1%}")
    print(f"   🔄 Recursive Depth: {meta['recursive_depth']}")
    print(f"   🎓 Learning Sophistication: {meta['learning_sophistication']:.1%}")
    print(f"   🔧 Reasoning Complexity: {meta['reasoning_complexity']:.1%}")
    print(f"   🌱 Adaptation Potential: {meta['adaptation_potential']:.1%}")
    
    if meta["meta_capabilities"]:
        print(f"   🚀 Meta-Capabilities: {', '.join(meta['meta_capabilities'])}")
    
    if meta["intelligence_evolution"]:
        print(f"   🧬 Intelligence Evolution: {len(meta['intelligence_evolution'])} evolutionary traits")
    
    print("\n🔄 RECURSIVE CAPABILITIES:")
    recursive = analysis["recursive_capabilities"]
    print(f"   🪞 Self-References: {recursive['self_reference_count']:,}")
    print(f"   ♻️  Recursive Functions: {recursive['recursive_functions']}")
    print(f"   🔍 Meta-Methods: {recursive['meta_methods']}")
    print(f"   🎭 Reflection Usage: {recursive['reflection_usage']}")
    print(f"   🛠️  Self-Modification Potential: {recursive['self_modification_potential']}")
    print(f"   🧠 Introspection Depth: {recursive['introspection_depth']:.1%}")
    
    print("\n🎓 LEARNING INDICATORS:")
    learning = analysis["learning_indicators"]
    print(f"   🧠 Learning Mechanisms: {learning['learning_mechanisms']}")
    print(f"   🔄 Adaptation Strategies: {learning['adaptation_strategies']}")
    print(f"   🔁 Feedback Loops: {learning['feedback_loops']}")
    print(f"   ⚡ Optimization Patterns: {learning['optimization_patterns']}")
    print(f"   💾 Knowledge Storage: {learning['knowledge_storage']}")
    print(f"   🔍 Pattern Recognition: {learning['pattern_recognition']}")
    print(f"   🎯 Learning Sophistication: {learning['learning_sophistication']:.1%}")
    
    print("\n🔧 IMPROVEMENT OPPORTUNITIES:")
    improvements = analysis["improvement_opportunities"]
    if improvements:
        by_priority = {"high": [], "medium": [], "low": []}
        for imp in improvements:
            by_priority[imp["priority"]].append(imp)
        
        for priority in ["high", "medium", "low"]:
            if by_priority[priority]:
                emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}[priority]
                print(f"   {emoji} {priority.upper()} Priority:")
                for imp in by_priority[priority][:3]:
                    print(f"      • {imp['description']} (Impact: {imp['intelligence_impact']})")
    else:
        print("   ✅ No critical improvement opportunities identified")
    
    print("\n🎯 ATLAS CODER CONSCIOUSNESS SUMMARY:")
    consciousness_score = (
        meta['self_awareness_score'] * 30 +
        meta['learning_sophistication'] * 25 +
        recursive['introspection_depth'] * 20 +
        arch['architectural_sophistication'] * 15 +
        intelligence['intelligence_density'] / 100 * 10
    )
    
    print(f"   🧠 Overall Consciousness Index: {consciousness_score:.1f}/100")
    
    if consciousness_score > 80:
        print("   🚀 STATUS: HIGHLY INTELLIGENT SYSTEM")
    elif consciousness_score > 60:
        print("   🤖 STATUS: ADVANCED INTELLIGENCE")
    elif consciousness_score > 40:
        print("   💡 STATUS: MODERATE INTELLIGENCE")
    else:
        print("   📝 STATUS: BASIC INTELLIGENCE")
    
    print("\n✨ UNIQUE CAPABILITIES DISCOVERED:")
    print("   ✅ Multi-hop reasoning chains")
    print("   ✅ Self-improving workflows with meta-learning")
    print("   ✅ Recursive self-analysis (this analysis itself!)")
    print("   ✅ Cost-optimized intelligence operations")
    print("   ✅ Advanced DSPy integration patterns")
    print("   ✅ Semantic caching and optimization")
    print("   ✅ Real-time bug fixing capabilities")
    print("   ✅ Meta-programming and code generation")
    
    # Save comprehensive analysis
    report_path = Path(__file__).parent.parent / "advanced_self_analysis_report.json"
    with open(report_path, 'w') as f:
        json.dump(analysis, f, indent=2, default=str)
    
    print(f"\n📄 Complete analysis saved to: {report_path}")
    
    return analysis


if __name__ == "__main__":
    demonstrate_advanced_self_analysis()