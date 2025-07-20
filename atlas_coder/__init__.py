"""Atlas Coder: Professional DSPy-powered systematic programming.

A production-ready open source tool for cost-effective AI-assisted development
using Stanford's DSPy framework with progressive complexity and hybrid models.
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
        return self.orchestrator.fix_bug(code_file=code_file,
                                         error_message=error_message,
                                         level="detailed") # Default to detailed for API usage

__all__ = ['AtlasCoder', 'AtlasCoderEngine', 'WorkflowOrchestrator']