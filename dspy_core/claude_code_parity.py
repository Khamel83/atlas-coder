"""
Claude Code Equivalent Features for Atlas Coder v6
Match Claude Code capabilities using DSPy + OpenRouter flexibility
"""

import os
import json
import subprocess
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from datetime import datetime

import dspy
from .signatures import *
from .workflows import get_orchestrator
from .optimization import get_cost_tracker

# Claude Code equivalent signatures
class ProjectManagement(dspy.Signature):
    """Manage project state and plan next actions"""
    project_state = dspy.InputField(desc="Current project files, structure, and status")
    user_intent = dspy.InputField(desc="What the user wants to accomplish")
    recent_changes = dspy.InputField(desc="Recent changes and progress made")
    next_actions = dspy.OutputField(desc="Prioritized list of next actions to take")
    task_breakdown = dspy.OutputField(desc="Detailed breakdown of complex tasks")
    timeline_estimate = dspy.OutputField(desc="Estimated timeline for completion")

class GitOperations(dspy.Signature):
    """Generate git commands and commit messages"""
    changes_summary = dspy.InputField(desc="Summary of changes made to the codebase")
    intent = dspy.InputField(desc="Intent behind the changes")
    project_context = dspy.InputField(desc="Project context and conventions")
    git_commands = dspy.OutputField(desc="Appropriate git commands to execute")
    commit_message = dspy.OutputField(desc="Well-formatted commit message following conventions")
    branch_strategy = dspy.OutputField(desc="Branching strategy recommendations if needed")

class FileOperations(dspy.Signature):
    """Plan and execute file system operations"""
    operation_intent = dspy.InputField(desc="What file operations need to be performed")
    current_structure = dspy.InputField(desc="Current project file structure")
    constraints = dspy.InputField(desc="Constraints and requirements")
    file_operations = dspy.OutputField(desc="Specific file operations to perform")
    structure_changes = dspy.OutputField(desc="How the file structure will change")
    backup_strategy = dspy.OutputField(desc="Backup strategy for safety")

class ArchitectureDesign(dspy.Signature):
    """Design system architecture and make architectural decisions"""
    requirements = dspy.InputField(desc="Functional and non-functional requirements")
    constraints = dspy.InputField(desc="Technical and business constraints")
    existing_system = dspy.InputField(desc="Existing system architecture if any")
    architecture_design = dspy.OutputField(desc="Complete architecture design with components")
    technology_choices = dspy.OutputField(desc="Technology stack with detailed justification")
    trade_offs = dspy.OutputField(desc="Architectural trade-offs and decision rationale")
    implementation_phases = dspy.OutputField(desc="Phased implementation strategy")

class PerformanceOptimization(dspy.Signature):
    """Analyze and optimize performance bottlenecks"""
    code = dspy.InputField(desc="Code to analyze for performance issues")
    performance_metrics = dspy.InputField(desc="Current performance metrics and bottlenecks")
    performance_goals = dspy.InputField(desc="Target performance goals and requirements")
    bottlenecks_analysis = dspy.OutputField(desc="Detailed analysis of performance bottlenecks")
    optimization_strategy = dspy.OutputField(desc="Comprehensive optimization strategy")
    optimized_code = dspy.OutputField(desc="Performance-optimized code implementation")
    benchmarking_plan = dspy.OutputField(desc="Plan for measuring performance improvements")

class ClaudeCodeEquivalent(dspy.Module):
    """Match Claude Code capabilities using DSPy + OpenRouter flexibility"""
    
    def __init__(self):
        super().__init__()
        # Core capabilities
        self.file_analyzer = dspy.ChainOfThought(AnalyzeCode)
        self.code_generator = dspy.ProgramOfThought(GenerateCode)
        self.project_manager = dspy.ChainOfThought(ProjectManagement)
        self.git_manager = dspy.ChainOfThought(GitOperations)
        self.file_manager = dspy.ChainOfThought(FileOperations)
        
        # Advanced capabilities
        self.architect = dspy.ChainOfThought(ArchitectureDesign)
        self.performance_optimizer = dspy.ProgramOfThought(PerformanceOptimization)
        self.security_analyzer = dspy.ChainOfThought(SecurityAudit)
        
        # Project state tracking
        self.project_root = Path.cwd()
        self.project_state = {}
        
    def analyze_project_structure(self, path: Optional[str] = None) -> Dict[str, Any]:
        """Analyze complete project structure like Claude Code"""
        if path:
            self.project_root = Path(path)
        
        print("🔍 Analyzing project structure...")
        
        structure = {
            'files': self._scan_project_files(),
            'git_status': self._get_git_status(),
            'dependencies': self._analyze_dependencies(),
            'architecture': self._infer_architecture(),
            'issues': self._detect_issues(),
            'opportunities': self._find_opportunities()
        }
        
        self.project_state = structure
        return structure
    
    def plan_development_workflow(self, user_request: str) -> Dict[str, Any]:
        """Plan complete development workflow like Claude Code"""
        print(f"📋 Planning workflow for: {user_request}")
        
        # Analyze current state
        if not self.project_state:
            self.analyze_project_structure()
        
        # Generate project management plan
        planning = self.project_manager(
            project_state=json.dumps(self.project_state, default=str),
            user_intent=user_request,
            recent_changes=self._get_recent_changes()
        )
        
        return {
            'next_actions': planning.next_actions,
            'task_breakdown': planning.task_breakdown,
            'timeline': planning.timeline_estimate,
            'project_state': self.project_state
        }
    
    def execute_development_task(self, task_description: str) -> Dict[str, Any]:
        """Execute development task with full workflow like Claude Code"""
        print(f"⚡ Executing task: {task_description}")
        
        # Determine task type and execute appropriate workflow
        if 'bug' in task_description.lower() or 'fix' in task_description.lower():
            return self._execute_bug_fix_workflow(task_description)
        elif 'feature' in task_description.lower() or 'implement' in task_description.lower():
            return self._execute_feature_workflow(task_description)
        elif 'optimize' in task_description.lower() or 'performance' in task_description.lower():
            return self._execute_optimization_workflow(task_description)
        elif 'refactor' in task_description.lower():
            return self._execute_refactoring_workflow(task_description)
        elif 'test' in task_description.lower():
            return self._execute_testing_workflow(task_description)
        else:
            return self._execute_general_workflow(task_description)
    
    def manage_git_workflow(self, changes_description: str) -> Dict[str, Any]:
        """Manage git operations like Claude Code"""
        print("📝 Managing git workflow...")
        
        git_management = self.git_manager(
            changes_summary=changes_description,
            intent=changes_description,
            project_context=self._get_project_context()
        )
        
        return {
            'git_commands': git_management.git_commands,
            'commit_message': git_management.commit_message,
            'branch_strategy': git_management.branch_strategy
        }
    
    def design_architecture(self, requirements: str) -> Dict[str, Any]:
        """Design system architecture like Claude Code"""
        print("🏗️ Designing system architecture...")
        
        architecture = self.architect(
            requirements=requirements,
            constraints=self._get_constraints(),
            existing_system=json.dumps(self.project_state.get('architecture', {}))
        )
        
        return {
            'architecture': architecture.architecture_design,
            'technologies': architecture.technology_choices,
            'trade_offs': architecture.trade_offs,
            'implementation': architecture.implementation_phases
        }
    
    def optimize_performance(self, target_code: str, goals: str) -> Dict[str, Any]:
        """Optimize performance like Claude Code"""
        print("🚀 Optimizing performance...")
        
        optimization = self.performance_optimizer(
            code=target_code,
            performance_metrics="Current metrics analysis needed",
            performance_goals=goals
        )
        
        return {
            'analysis': optimization.bottlenecks_analysis,
            'strategy': optimization.optimization_strategy,
            'optimized_code': optimization.optimized_code,
            'benchmarking': optimization.benchmarking_plan
        }
    
    def comprehensive_code_review(self, file_path: str) -> Dict[str, Any]:
        """Comprehensive code review like Claude Code"""
        print(f"📊 Reviewing code: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                code = f.read()
        except Exception as e:
            return {'error': f'Could not read file: {e}'}
        
        # Multi-dimensional analysis
        analysis = self.file_analyzer(code=code)
        security = self.security_analyzer(
            code=code,
            context=self._get_project_context()
        )
        
        return {
            'code_quality': {
                'analysis': analysis.analysis,
                'issues': analysis.issues,
                'architecture': analysis.architecture
            },
            'security': {
                'vulnerabilities': security.vulnerabilities,
                'fixes': security.fixes,
                'compliance': security.compliance
            },
            'recommendations': self._generate_comprehensive_recommendations(analysis, security)
        }
    
    # Private helper methods
    def _scan_project_files(self) -> Dict[str, Any]:
        """Scan and categorize project files"""
        files = {
            'source_files': [],
            'config_files': [],
            'documentation': [],
            'tests': [],
            'assets': []
        }
        
        try:
            for file_path in self.project_root.rglob('*'):
                if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
                    rel_path = file_path.relative_to(self.project_root)
                    
                    if file_path.suffix in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs']:
                        files['source_files'].append(str(rel_path))
                    elif file_path.suffix in ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg']:
                        files['config_files'].append(str(rel_path))
                    elif file_path.suffix in ['.md', '.txt', '.rst']:
                        files['documentation'].append(str(rel_path))
                    elif 'test' in str(file_path).lower():
                        files['tests'].append(str(rel_path))
                    else:
                        files['assets'].append(str(rel_path))
        except Exception as e:
            print(f"⚠️ File scan error: {e}")
        
        return files
    
    def _get_git_status(self) -> str:
        """Get git status"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout if result.returncode == 0 else "Not a git repository"
        except:
            return "Git status unavailable"
    
    def _analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze project dependencies"""
        deps = {}
        
        # Python dependencies
        requirements_files = ['requirements.txt', 'pyproject.toml', 'setup.py']
        for req_file in requirements_files:
            req_path = self.project_root / req_file
            if req_path.exists():
                deps['python'] = req_file
                break
        
        # Node.js dependencies
        if (self.project_root / 'package.json').exists():
            deps['nodejs'] = 'package.json'
        
        # Other common dependency files
        for dep_file in ['Cargo.toml', 'go.mod', 'pom.xml', 'build.gradle']:
            if (self.project_root / dep_file).exists():
                deps[dep_file.split('.')[0]] = dep_file
        
        return deps
    
    def _infer_architecture(self) -> Dict[str, Any]:
        """Infer project architecture"""
        arch = {
            'type': 'unknown',
            'patterns': [],
            'frameworks': []
        }
        
        files = self._scan_project_files()
        
        # Detect common patterns
        if any('main.py' in f for f in files['source_files']):
            arch['type'] = 'python_application'
        elif any('app.py' in f for f in files['source_files']):
            arch['type'] = 'web_application'
        elif any('__init__.py' in f for f in files['source_files']):
            arch['type'] = 'python_package'
        
        # Detect frameworks
        if (self.project_root / 'requirements.txt').exists():
            try:
                with open(self.project_root / 'requirements.txt', 'r') as f:
                    content = f.read().lower()
                    if 'flask' in content:
                        arch['frameworks'].append('Flask')
                    if 'django' in content:
                        arch['frameworks'].append('Django')
                    if 'fastapi' in content:
                        arch['frameworks'].append('FastAPI')
                    if 'dspy' in content:
                        arch['frameworks'].append('DSPy')
            except:
                pass
        
        return arch
    
    def _detect_issues(self) -> List[str]:
        """Detect potential issues"""
        issues = []
        
        # Check for common issues
        if not (self.project_root / 'README.md').exists():
            issues.append("Missing README.md file")
        
        if not (self.project_root / '.gitignore').exists():
            issues.append("Missing .gitignore file")
        
        # Check for large files
        try:
            for file_path in self.project_root.rglob('*'):
                if file_path.is_file() and file_path.stat().st_size > 10 * 1024 * 1024:  # 10MB
                    issues.append(f"Large file detected: {file_path.name}")
        except:
            pass
        
        return issues
    
    def _find_opportunities(self) -> List[str]:
        """Find improvement opportunities"""
        opportunities = []
        
        files = self._scan_project_files()
        
        if not files['tests']:
            opportunities.append("Add test coverage")
        
        if not files['documentation']:
            opportunities.append("Add comprehensive documentation")
        
        if len(files['source_files']) > 10 and not files['config_files']:
            opportunities.append("Add configuration management")
        
        return opportunities
    
    def _get_recent_changes(self) -> str:
        """Get recent changes"""
        try:
            result = subprocess.run(
                ['git', 'log', '--oneline', '-5'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout if result.returncode == 0 else "No recent changes"
        except:
            return "Recent changes unavailable"
    
    def _get_project_context(self) -> str:
        """Get project context"""
        context = []
        
        # README content
        readme_path = self.project_root / 'README.md'
        if readme_path.exists():
            try:
                with open(readme_path, 'r') as f:
                    context.append(f.read()[:1000])  # First 1000 chars
            except:
                pass
        
        # CLAUDE.md content
        claude_path = self.project_root / 'CLAUDE.md'
        if claude_path.exists():
            try:
                with open(claude_path, 'r') as f:
                    context.append(f.read()[:500])
            except:
                pass
        
        return '\n'.join(context) if context else "Atlas Coder DSPy project"
    
    def _get_constraints(self) -> str:
        """Get project constraints"""
        constraints = [
            "Maintain existing architecture patterns",
            "Follow project coding conventions", 
            "Ensure backward compatibility",
            "Optimize for performance and maintainability"
        ]
        
        # Add budget constraints
        cost_tracker = get_cost_tracker()
        remaining = cost_tracker.get_remaining_budget()
        constraints.append(f"Budget constraint: ${remaining:.2f} remaining")
        
        return '\n'.join(constraints)
    
    def _execute_bug_fix_workflow(self, task: str) -> Dict[str, Any]:
        """Execute bug fix workflow"""
        orchestrator = get_orchestrator()
        
        # Extract code context
        code_context = self._extract_code_context(task)
        
        result = orchestrator.execute_workflow(
            'bug_fix',
            code=code_context.get('code', ''),
            error=task,
            context=code_context.get('context', '')
        )
        
        return {'workflow': 'bug_fix', 'result': result.data if result.success else {'error': result.error}}
    
    def _execute_feature_workflow(self, task: str) -> Dict[str, Any]:
        """Execute feature development workflow"""
        orchestrator = get_orchestrator()
        
        result = orchestrator.execute_workflow(
            'generate',
            requirements=task,
            constraints=self._get_constraints()
        )
        
        return {'workflow': 'feature_development', 'result': result.data if result.success else {'error': result.error}}
    
    def _execute_optimization_workflow(self, task: str) -> Dict[str, Any]:
        """Execute optimization workflow"""
        orchestrator = get_orchestrator()
        
        code_context = self._extract_code_context(task)
        
        result = orchestrator.execute_workflow(
            'refactor',
            code=code_context.get('code', ''),
            goals='performance optimization'
        )
        
        return {'workflow': 'optimization', 'result': result.data if result.success else {'error': result.error}}
    
    def _execute_refactoring_workflow(self, task: str) -> Dict[str, Any]:
        """Execute refactoring workflow"""
        orchestrator = get_orchestrator()
        
        code_context = self._extract_code_context(task)
        
        result = orchestrator.execute_workflow(
            'refactor',
            code=code_context.get('code', ''),
            goals='improve code quality and maintainability'
        )
        
        return {'workflow': 'refactoring', 'result': result.data if result.success else {'error': result.error}}
    
    def _execute_testing_workflow(self, task: str) -> Dict[str, Any]:
        """Execute testing workflow"""
        orchestrator = get_orchestrator()
        
        code_context = self._extract_code_context(task)
        
        result = orchestrator.execute_workflow(
            'generate',
            requirements=f"Generate comprehensive tests for: {task}",
            constraints="Focus on test coverage and edge cases"
        )
        
        return {'workflow': 'testing', 'result': result.data if result.success else {'error': result.error}}
    
    def _execute_general_workflow(self, task: str) -> Dict[str, Any]:
        """Execute general analysis workflow"""
        orchestrator = get_orchestrator()
        
        code_context = self._extract_code_context(task)
        
        result = orchestrator.execute_workflow(
            'analyze',
            code=code_context.get('code', ''),
            context=task
        )
        
        return {'workflow': 'analysis', 'result': result.data if result.success else {'error': result.error}}
    
    def _extract_code_context(self, task: str) -> Dict[str, str]:
        """Extract relevant code context for task"""
        context = {'code': '', 'context': ''}
        
        # Look for file references in task
        import re
        file_refs = re.findall(r'[\w\/\.]+\.py', task)
        
        if file_refs:
            for file_ref in file_refs:
                file_path = self.project_root / file_ref
                if file_path.exists():
                    try:
                        with open(file_path, 'r') as f:
                            context['code'] = f.read()
                            context['context'] = f"File: {file_ref}"
                        break
                    except:
                        continue
        
        return context
    
    def _generate_comprehensive_recommendations(self, analysis, security) -> List[str]:
        """Generate comprehensive recommendations"""
        recommendations = []
        
        # Code quality recommendations
        if 'TODO' in analysis.issues:
            recommendations.append("Address TODO items in codebase")
        
        if 'complex' in analysis.analysis.lower():
            recommendations.append("Consider breaking down complex functions")
        
        # Security recommendations
        if security.vulnerabilities:
            recommendations.append("Address identified security vulnerabilities")
        
        # General best practices
        recommendations.extend([
            "Add comprehensive documentation",
            "Implement comprehensive test coverage",
            "Set up continuous integration",
            "Add performance monitoring",
            "Implement proper error handling"
        ])
        
        return recommendations[:5]  # Top 5 recommendations

# Convenience functions for Claude Code parity
def analyze_project(path: Optional[str] = None) -> Dict[str, Any]:
    """Analyze project like Claude Code"""
    claude_equivalent = ClaudeCodeEquivalent()
    return claude_equivalent.analyze_project_structure(path)

def plan_workflow(user_request: str) -> Dict[str, Any]:
    """Plan development workflow like Claude Code"""
    claude_equivalent = ClaudeCodeEquivalent()
    return claude_equivalent.plan_development_workflow(user_request)

def execute_task(task_description: str) -> Dict[str, Any]:
    """Execute development task like Claude Code"""
    claude_equivalent = ClaudeCodeEquivalent()
    return claude_equivalent.execute_development_task(task_description)

def manage_git(changes_description: str) -> Dict[str, Any]:
    """Manage git operations like Claude Code"""
    claude_equivalent = ClaudeCodeEquivalent()
    return claude_equivalent.manage_git_workflow(changes_description)

def design_system(requirements: str) -> Dict[str, Any]:
    """Design system architecture like Claude Code"""
    claude_equivalent = ClaudeCodeEquivalent()
    return claude_equivalent.design_architecture(requirements)

def review_code(file_path: str) -> Dict[str, Any]:
    """Comprehensive code review like Claude Code"""
    claude_equivalent = ClaudeCodeEquivalent()
    return claude_equivalent.comprehensive_code_review(file_path)

# Global instance
_claude_equivalent = None

def get_claude_equivalent() -> ClaudeCodeEquivalent:
    """Get global Claude Code equivalent instance"""
    global _claude_equivalent
    if _claude_equivalent is None:
        _claude_equivalent = ClaudeCodeEquivalent()
    return _claude_equivalent