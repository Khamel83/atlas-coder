"""Atlas Coder: Professional DSPy-powered systematic programming.

A production-ready open source tool for cost-effective AI-assisted development
using Stanford's DSPy framework with progressive complexity and hybrid models.

Example:
    >>> from atlas_coder import AtlasCoder
    >>> coder = AtlasCoder()
    >>> result = coder.fix_bug("code.py", "error message")
    >>> print(result.status)
    'success'
"""

__version__ = "1.0.0"
__author__ = "Atlas Coder Contributors"
__license__ = "MIT"

from .core.engine import AtlasCoderEngine
from .core.workflows import WorkflowOrchestrator

# Main interface
class AtlasCoder:
    """Main Atlas Coder interface for systematic programming."""
    
    def __init__(self):
        """Initialize Atlas Coder with default configuration."""
        self.engine = AtlasCoderEngine()
        self.orchestrator = WorkflowOrchestrator()
    
    def fix_bug(self, code_file: str, error_message: str):
        """Fix a bug systematically using DSPy workflows."""
        return self.orchestrator.execute_workflow('bug_fix', 
                                                 code_file=code_file,
                                                 error=error_message)

__all__ = ['AtlasCoder', 'AtlasCoderEngine', 'WorkflowOrchestrator']
