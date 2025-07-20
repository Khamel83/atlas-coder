"""
Composition Framework for Atlas Coder DSPy Workflows
Systematic composition of modules into powerful workflows
"""

import dspy
from typing import Dict, Any, Optional, List
from .modules import *
from .engine import get_engine

class WorkflowResult:
    """Standard result container for all workflows"""
    
    def __init__(self, success: bool = True, data: Dict[str, Any] = None, error: str = ""):
        self.success = success
        self.data = data or {}
        self.error = error
    
    def __getattr__(self, name):
        """Allow dot notation access to data"""
        return self.data.get(name)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error
        }

class BaseWorkflow:
    """Base class for all DSPy workflows"""
    
    def __init__(self):
        self.engine = get_engine()
        self._setup_modules()
    
    def _setup_modules(self):
        """Setup required modules - override in subclasses"""
        pass
    
    def execute(self, **kwargs) -> WorkflowResult:
        """Execute the workflow - override in subclasses"""
        raise NotImplementedError("Subclasses must implement execute method")
    
    def _handle_error(self, error: Exception) -> WorkflowResult:
        """Standard error handling"""
        error_msg = f"{self.__class__.__name__} failed: {str(error)}"
        print(f"❌ {error_msg}")
        return WorkflowResult(success=False, error=error_msg)

# === CORE DEVELOPMENT WORKFLOWS ===

class BugFixingWorkflow(BaseWorkflow):
    """Complete bug fixing workflow"""
    
    def _setup_modules(self):
        self.bug_fixer = CompleteBugFixer()
    
    def execute(self, code: str, error: str, context: str = "") -> WorkflowResult:
        """Execute complete bug fixing pipeline"""
        try:
            print("🔍 Starting bug diagnosis and fixing...")
            
            result = self.bug_fixer(code=code, error=error, context=context)
            
            return WorkflowResult(
                success=True,
                data={
                    "original_code": result.original_code,
                    "error": result.error,
                    "diagnosis": result.diagnosis,
                    "impact_assessment": result.impact_assessment,
                    "fixed_code": result.fixed_code,
                    "fix_explanation": result.fix_explanation,
                    "validation_tests": result.validation_tests,
                    "reproduction_steps": result.reproduction_steps
                }
            )
            
        except Exception as e:
            return self._handle_error(e)

class CodeGenerationWorkflow(BaseWorkflow):
    """Generate code from requirements"""
    
    def _setup_modules(self):
        self.requirements_processor = RequirementsProcessor()
        self.code_generator = CodeGenerator()
        self.test_generator = TestGenerator()
    
    def execute(self, requirements: str, constraints: str = "") -> WorkflowResult:
        """Generate code from natural language requirements"""
        try:
            print("📝 Processing requirements...")
            req_result = self.requirements_processor(
                requirements=requirements,
                constraints=constraints
            )
            
            print("⚡ Generating code...")
            code_result = self.code_generator(
                specifications=req_result.specifications,
                understanding=req_result.understanding,
                requirements=requirements
            )
            
            print("🧪 Generating tests...")
            test_result = self.test_generator(
                code=code_result.code,
                requirements=requirements
            )
            
            return WorkflowResult(
                success=True,
                data={
                    "requirements": requirements,
                    "understanding": req_result.understanding,
                    "specifications": req_result.specifications,
                    "architecture_plan": req_result.architecture_plan,
                    "code": code_result.code,
                    "explanation": code_result.explanation,
                    "tests": test_result.tests,
                    "coverage_plan": test_result.coverage_plan
                }
            )
            
        except Exception as e:
            return self._handle_error(e)

class CodeAnalysisWorkflow(BaseWorkflow):
    """Comprehensive code analysis and review"""
    
    def _setup_modules(self):
        self.analyzer = CodeAnalyzer()
        self.reviewer = CodeReviewer()
    
    def execute(self, code: str, requirements: str = "", context: str = "") -> WorkflowResult:
        """Analyze code quality and provide recommendations"""
        try:
            print("🔍 Analyzing code structure...")
            analysis_result = self.analyzer(code=code, context=context)
            
            print("📊 Reviewing code quality...")
            review_result = self.reviewer(
                code=code,
                requirements=requirements,
                context=context
            )
            
            return WorkflowResult(
                success=True,
                data={
                    "code": code,
                    "analysis": analysis_result.analysis,
                    "issues": analysis_result.issues,
                    "architecture": analysis_result.architecture,
                    "review": review_result.review,
                    "suggestions": review_result.suggestions,
                    "security_analysis": review_result.security_analysis,
                    "vulnerabilities": review_result.vulnerabilities,
                    "security_fixes": review_result.security_fixes
                }
            )
            
        except Exception as e:
            return self._handle_error(e)

class FullProjectWorkflow(BaseWorkflow):
    """Complete project generation workflow"""
    
    def _setup_modules(self):
        self.full_stack_developer = FullStackDeveloper()
    
    def execute(self, requirements: str, constraints: str = "") -> WorkflowResult:
        """Generate complete project from requirements"""
        try:
            print("🚀 Starting full project generation...")
            
            result = self.full_stack_developer(
                requirements=requirements,
                constraints=constraints
            )
            
            return WorkflowResult(
                success=True,
                data={
                    "requirements": result.requirements,
                    "understanding": result.understanding,
                    "specifications": result.specifications,
                    "architecture_plan": result.architecture_plan,
                    "code": result.code,
                    "explanation": result.explanation,
                    "tests": result.tests,
                    "documentation": result.documentation,
                    "readme": result.readme,
                    "final_review": result.final_review,
                    "suggestions": result.suggestions
                }
            )
            
        except Exception as e:
            return self._handle_error(e)

class RefactoringWorkflow(BaseWorkflow):
    """Code refactoring and improvement workflow"""
    
    def _setup_modules(self):
        self.refactor = CodeRefactor()
        self.reviewer = CodeReviewer()
    
    def execute(self, code: str, goals: str = "improve readability and maintainability") -> WorkflowResult:
        """Refactor code with quality validation"""
        try:
            print("🔧 Refactoring code...")
            refactor_result = self.refactor(code=code, goals=goals)
            
            print("✅ Validating refactored code...")
            review_result = self.reviewer(
                code=refactor_result.refactored_code,
                requirements="Refactored code validation"
            )
            
            return WorkflowResult(
                success=True,
                data={
                    "original_code": refactor_result.original_code,
                    "refactored_code": refactor_result.refactored_code,
                    "improvements": refactor_result.improvements,
                    "migration_guide": refactor_result.migration_guide,
                    "validation": refactor_result.validation,
                    "quality_review": review_result.review,
                    "suggestions": review_result.suggestions
                }
            )
            
        except Exception as e:
            return self._handle_error(e)

# === WORKFLOW FACTORY ===

class WorkflowFactory:
    """Factory for creating and managing workflows"""
    
    _workflows = {
        "bug_fix": BugFixingWorkflow,
        "generate": CodeGenerationWorkflow,
        "analyze": CodeAnalysisWorkflow,
        "project": FullProjectWorkflow,
        "refactor": RefactoringWorkflow,
    }
    
    @classmethod
    def create_workflow(cls, workflow_type: str) -> BaseWorkflow:
        """Create a workflow instance"""
        if workflow_type not in cls._workflows:
            available = ", ".join(cls._workflows.keys())
            raise ValueError(f"Unknown workflow type: {workflow_type}. Available: {available}")
        
        return cls._workflows[workflow_type]()
    
    @classmethod
    def get_available_workflows(cls) -> List[str]:
        """Get list of available workflow types"""
        return list(cls._workflows.keys())
    
    @classmethod
    def register_workflow(cls, name: str, workflow_class):
        """Register a new workflow type"""
        cls._workflows[name] = workflow_class

# === WORKFLOW ORCHESTRATOR ===

class WorkflowOrchestrator:
    """Orchestrate multiple workflows and manage execution"""
    
    def __init__(self):
        self.factory = WorkflowFactory()
        self.results_history = []
    
    def execute_workflow(self, workflow_type: str, **kwargs) -> WorkflowResult:
        """Execute a specific workflow with parameters"""
        try:
            workflow = self.factory.create_workflow(workflow_type)
            result = workflow.execute(**kwargs)
            
            # Store result in history
            self.results_history.append({
                "workflow_type": workflow_type,
                "parameters": kwargs,
                "result": result.to_dict(),
                "timestamp": __import__("datetime").datetime.now().isoformat()
            })
            
            return result
            
        except Exception as e:
            error_result = WorkflowResult(
                success=False,
                error=f"Workflow execution failed: {str(e)}"
            )
            print(f"❌ {error_result.error}")
            return error_result
    
    def get_workflow_info(self, workflow_type: str) -> Dict[str, Any]:
        """Get information about a specific workflow"""
        try:
            workflow = self.factory.create_workflow(workflow_type)
            return {
                "type": workflow_type,
                "class": workflow.__class__.__name__,
                "description": workflow.__class__.__doc__,
                "available": True
            }
        except Exception as e:
            return {
                "type": workflow_type,
                "available": False,
                "error": str(e)
            }
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all available workflows with their information"""
        workflows = []
        for workflow_type in self.factory.get_available_workflows():
            workflows.append(self.get_workflow_info(workflow_type))
        return workflows
    
    def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent workflow execution history"""
        return self.results_history[-limit:] if self.results_history else []

# Global orchestrator instance
_orchestrator = None

def get_orchestrator() -> WorkflowOrchestrator:
    """Get or create the global workflow orchestrator"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = WorkflowOrchestrator()
    return _orchestrator