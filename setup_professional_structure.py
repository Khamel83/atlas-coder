#!/usr/bin/env python3
"""Professional Project Structure Setup for Atlas Coder.

This script sets up a complete development environment with linting, testing,
and automation tools configured according to Python best practices.

Example:
    python setup_professional_structure.py --create-all --setup-tools
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Any


def setup_professional_structure() -> Dict[str, str]:
    """Set up professional Python project structure with all tooling.
    
    Creates a complete development environment with linting, testing,
    and automation tools configured according to Python best practices.
    
    Returns:
        Dict[str, str]: Status of each component setup.
        
    Example:
        >>> result = setup_professional_structure()
        >>> print(f"Setup status: {result['status']}")
        Setup status: complete
    """
    print("🔄 SETTING UP: Professional project structure...")
    
    setup_results = {}
    
    # 1. Create proper package structure
    create_package_structure()
    setup_results["package_structure"] = "complete"
    print("✅ STRUCTURE: Package layout created")
    
    # 2. Setup development tools
    setup_dev_tools()
    setup_results["dev_tools"] = "complete"
    print("✅ TOOLS: Development tools configured")
    
    # 3. Create auto-environment activation
    setup_auto_venv()
    setup_results["auto_venv"] = "complete"
    print("✅ ENVIRONMENT: Auto-activation configured")
    
    # 4. Setup pre-commit hooks
    setup_precommit_hooks()
    setup_results["precommit"] = "complete"
    print("✅ HOOKS: Pre-commit hooks configured")
    
    # 5. Create package configuration
    create_package_config()
    setup_results["package_config"] = "complete"
    print("✅ CONFIG: Package configuration created")
    
    return {
        "status": "complete", 
        "components": setup_results,
        "tools": ["black", "ruff", "pytest", "mypy", "mkdocs"]
    }


def create_package_structure():
    """Create proper Python package structure.
    
    Sets up a professional directory layout following Python packaging
    best practices with clear separation of concerns.
    """
    print("🔄 CREATING: Professional package structure...")
    
    structure = {
        # Main package
        "atlas_coder/": "Main package directory",
        "atlas_coder/__init__.py": "Package initialization with version info",
        
        # Core modules  
        "atlas_coder/core/": "Core functionality modules",
        "atlas_coder/core/__init__.py": "Core package init",
        "atlas_coder/core/engine.py": "DSPy engine and model management",
        "atlas_coder/core/signatures.py": "DSPy signature definitions",
        "atlas_coder/core/modules.py": "DSPy module implementations",
        "atlas_coder/core/workflows.py": "Workflow orchestration",
        
        # DSPy integration
        "atlas_coder/dspy/": "DSPy integration modules",
        "atlas_coder/dspy/__init__.py": "DSPy package init",
        "atlas_coder/dspy/optimization.py": "Cost and performance optimization",
        "atlas_coder/dspy/progressive.py": "Progressive complexity execution",
        "atlas_coder/dspy/caching.py": "Smart caching implementation",
        
        # CLI interface
        "atlas_coder/cli/": "Command line interface",
        "atlas_coder/cli/__init__.py": "CLI package init",
        "atlas_coder/cli/main.py": "Main CLI entry point",
        "atlas_coder/cli/commands.py": "CLI command implementations",
        "atlas_coder/cli/utils.py": "CLI utility functions",
        
        # Utilities
        "atlas_coder/utils/": "Utility functions",
        "atlas_coder/utils/__init__.py": "Utils package init",
        "atlas_coder/utils/logging.py": "Logging configuration",
        "atlas_coder/utils/config.py": "Configuration management",
        "atlas_coder/utils/exceptions.py": "Custom exception classes",
        
        # Tests
        "tests/": "Test suite",
        "tests/__init__.py": "Test package init",
        "tests/unit/": "Unit tests",
        "tests/unit/__init__.py": "Unit tests init",
        "tests/integration/": "Integration tests", 
        "tests/integration/__init__.py": "Integration tests init",
        "tests/fixtures/": "Test data and mock objects",
        "tests/conftest.py": "Pytest configuration and shared fixtures",
        
        # Documentation
        "docs/": "Documentation",
        "docs/source/": "Documentation source files",
        "docs/source/conf.py": "Sphinx configuration",
        "docs/examples/": "Usage examples",
        
        # Examples
        "examples/": "Usage examples",
        "examples/__init__.py": "Examples package init",
        "examples/basic_usage.py": "Basic usage examples",
        "examples/advanced_workflows.py": "Advanced workflow examples",
        "examples/ai_integration.py": "AI integration examples",
        
        # CI/CD
        ".github/": "GitHub configuration",
        ".github/workflows/": "GitHub Actions workflows",
        ".github/ISSUE_TEMPLATE/": "Issue templates",
        ".github/PULL_REQUEST_TEMPLATE.md": "PR template",
    }
    
    for path, description in structure.items():
        full_path = Path(path)
        
        if path.endswith("/"):
            # Directory
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 CREATED: {path} - {description}")
        else:
            # File
            full_path.parent.mkdir(parents=True, exist_ok=True)
            if not full_path.exists():
                if path.endswith("__init__.py"):
                    create_init_file(full_path, description)
                else:
                    create_placeholder_file(full_path, description)
                print(f"📄 CREATED: {path} - {description}")


def create_init_file(file_path: Path, description: str):
    """Create __init__.py file with proper documentation.
    
    Args:
        file_path: Path to the __init__.py file.
        description: Description for the module.
    """
    package_name = file_path.parent.name
    
    if "atlas_coder/__init__.py" in str(file_path):
        content = '''"""Atlas Coder: Professional DSPy-powered systematic programming.

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
'''
    else:
        content = f'''"""{ description}.

This module is part of the Atlas Coder professional DSPy framework.
"""

# Package imports will be added as modules are implemented
'''
    
    file_path.write_text(content)


def create_placeholder_file(file_path: Path, description: str):
    """Create placeholder file with documentation header.
    
    Args:
        file_path: Path to the file to create.
        description: Description for the file purpose.
    """
    if file_path.suffix == ".py":
        content = f'''"""{ description}.

This module is part of the Atlas Coder professional DSPy framework.
Implements {description.lower()} functionality with proper documentation
following PEP 257 and Google Python Style Guide.

Example:
    >>> # Usage example will be added when implemented
    >>> pass
"""

# Implementation will be added in subsequent development phases
'''
    elif file_path.suffix == ".md":
        content = f'''# { description}

This document is part of the Atlas Coder professional documentation.

## Overview

{description} - Implementation pending.

## Usage

Usage examples will be added when implemented.
'''
    else:
        content = f"# { description}\n# Implementation pending\n"
    
    file_path.write_text(content)


def setup_dev_tools():
    """Setup development tools configuration.
    
    Creates configuration files for black, ruff, pytest, mypy, and other
    development tools with professional settings.
    """
    print("🔄 CONFIGURING: Development tools...")
    
    # Black configuration (pyproject.toml)
    pyproject_content = '''[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "atlas-coder"
version = "1.0.0"
description = "Professional DSPy-powered systematic programming"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Atlas Coder Contributors"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
requires-python = ">=3.11"
dependencies = [
    "dspy-ai>=2.6.27",
    "click>=8.0.0",
    "rich>=13.7.1",
    "pydantic>=2.11.7",
    "python-dotenv>=1.1.1",
]

[project.optional-dependencies]
dev = [
    "black>=23.0.0",
    "ruff>=0.1.0", 
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
]
docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.0.0",
]

[project.scripts]
atlas-coder = "atlas_coder.cli.main:main"

[tool.black]
line-length = 88
target-version = ['py311']
include = '\\.pyi?$'
extend-exclude = """
/(
  # directories
  \\.eggs
  | \\.git
  | \\.hg
  | \\.mypy_cache
  | \\.tox
  | \\.venv
  | _build
  | buck-out
  | build
  | dist
)/
"""

[tool.ruff]
target-version = "py311"
line-length = 88
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings  
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
    "UP", # pyupgrade
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
    "C901",  # too complex
]

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]
"tests/**/*" = ["B011"]

[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra -q --strict-markers --strict-config"
testpaths = [
    "tests",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[tool.coverage.run]
source = ["atlas_coder"]
omit = [
    "*/tests/*",
    "*/venv/*",
    "*/.venv/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]
'''
    
    Path("pyproject.toml").write_text(pyproject_content)
    print("✅ CREATED: pyproject.toml with tool configurations")


def setup_auto_venv():
    """Create auto-environment activation using direnv.
    
    Sets up automatic virtual environment activation when entering
    the project directory using direnv.
    """
    print("🔄 SETTING UP: Auto-environment activation...")
    
    # Create .envrc for direnv
    envrc_content = '''# Atlas Coder Auto-Environment Configuration
# This file automatically activates the virtual environment when entering the directory
# Install direnv: https://direnv.net/

# Activate virtual environment
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
elif [ -f venv/bin/activate ]; then
    source venv/bin/activate
fi

# Set Python path
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# Development environment variables
export ATLAS_CODER_ENV="development"
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# Display activation status
echo "🚀 ATLAS CODER: Development environment activated"
echo "📊 Python: $(python --version)"
echo "📍 Virtual env: $VIRTUAL_ENV"
'''
    
    Path(".envrc").write_text(envrc_content)
    print("✅ CREATED: .envrc for direnv auto-activation")
    
    # Create .env template
    env_template = '''# Atlas Coder Environment Configuration
# Copy this file to .env and configure your settings

# OpenRouter API Key (optional - for API models)
# Get free key at: https://openrouter.ai/
# OPENAI_API_KEY=your_openrouter_key_here

# Model configuration
# ATLAS_MODEL=ollama/llama3.2
# ATLAS_DAILY_BUDGET=3.00

# Development settings
ATLAS_CODER_ENV=development
ATLAS_LOG_LEVEL=INFO

# Cache configuration  
ATLAS_CACHE_DIR=.atlas_cache
ATLAS_CACHE_ENABLED=true
'''
    
    Path(".env.template").write_text(env_template)
    print("✅ CREATED: .env.template for configuration")


def setup_precommit_hooks():
    """Setup pre-commit hooks for code quality.
    
    Creates pre-commit configuration to automatically run linting,
    formatting, and basic tests before commits.
    """
    print("🔄 SETTING UP: Pre-commit hooks...")
    
    precommit_config = '''# Atlas Coder Pre-commit Configuration
# Automatically formats and checks code before commits

repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/charliermarsh/ruff-pre-commit  
    rev: v0.0.287
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
        exclude: ^tests/

  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
        args: [tests/unit/, -x, -v]
'''
    
    Path(".pre-commit-config.yaml").write_text(precommit_config)
    print("✅ CREATED: .pre-commit-config.yaml")


def create_package_config():
    """Create additional package configuration files.
    
    Creates MANIFEST.in, setup.cfg, and other packaging files
    for professional distribution.
    """
    print("🔄 CREATING: Package configuration files...")
    
    # MANIFEST.in
    manifest_content = '''include README.md
include LICENSE
include CHANGELOG.md
include requirements.txt
include pyproject.toml
recursive-include atlas_coder *.py
recursive-include docs *.md *.rst
recursive-include examples *.py
recursive-exclude * __pycache__
recursive-exclude * *.py[co]
'''
    Path("MANIFEST.in").write_text(manifest_content)
    print("✅ CREATED: MANIFEST.in")
    
    # .gitignore
    gitignore_content = '''# Atlas Coder .gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Atlas Coder specific
.atlas_cache/
dspy_cache/
backup_*/
*.log

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.cache

# Documentation
docs/_build/
site/

# Temporary files
*.tmp
*.temp
'''
    Path(".gitignore").write_text(gitignore_content)
    print("✅ CREATED: .gitignore")


def main():
    """Main setup execution function."""
    print("🚀 ATLAS CODER: Professional Structure Setup")
    print("=" * 50)
    
    try:
        result = setup_professional_structure()
        
        print("\n✅ SETUP COMPLETE: Professional structure ready")
        print(f"📊 COMPONENTS: {len(result['components'])} configured")
        print(f"🔧 TOOLS: {', '.join(result['tools'])}")
        
        print("\n🚀 NEXT STEPS:")
        print("1. Install dev tools: pip install -e .[dev]")
        print("2. Setup direnv: direnv allow .")
        print("3. Install pre-commit: pre-commit install")
        print("4. Run tests: pytest tests/")
        print("5. Format code: black .")
        print("6. Lint code: ruff .")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ SETUP FAILED: {e}")
        return 1


if __name__ == "__main__":
    exit(main())