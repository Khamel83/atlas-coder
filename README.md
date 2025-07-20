# Atlas Coder: Revolutionary Cost-Optimized Programming

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![DSPy](https://img.shields.io/badge/DSPy-2.6+-orange.svg)](https://github.com/stanfordnlp/dspy)


**Revolutionary systematic programming** that matches Claude Code quality while operating sustainably under **$3/day** through progressive complexity, hybrid model strategies, and agentic operation.

## 🚀 Revolutionary Approach

### The Problem DSPy Solves
- **Before**: Brittle prompt engineering with expensive models
- **After**: Systematic programming that works with any model

### Example Transformation

**Old Approach (Prompt Engineering):**
```python
prompt = f"You are an expert programmer. Fix this bug: {code}"
# Brittle, expensive, inconsistent
```

**New Approach (DSPy Programming):**
```python
class BugFixer(dspy.Module):
    def __init__(self):
        self.diagnose = dspy.ChainOfThought("code, error -> diagnosis")
        self.fix = dspy.ProgramOfThought("code, diagnosis -> fixed_code")
    
    def forward(self, code, error):
        diagnosis = self.diagnose(code=code, error=error)
        fix = self.fix(code=code, diagnosis=diagnosis.diagnosis)
        return fix
# Systematic, reliable, works with free models
```

## 🎯 Key Features

### 🧠 Progressive Complexity Execution
- **Start Simple**: Quick scans with local models (free)
- **Escalate Intelligently**: Only use premium models when needed
- **Cost Control**: Respect daily budgets and per-task limits

### 🔄 Hybrid Model Strategy  
- **Local First**: Prefer Ollama models for cost efficiency
- **Smart Selection**: Choose optimal model for task complexity
- **Fallback Chains**: Graceful degradation when models unavailable

### 🤖 Agentic Operation
- **Work Detection**: Automatically find meaningful tasks
- **Value Assessment**: Prioritize work by impact vs cost
- **Continuous Operation**: Run autonomously within budget
- **Project Awareness**: Understand context and goals

### 🛠️ Powerful Workflows
- **Bug Fixing** - Systematic diagnosis and repair
- **Code Generation** - From requirements to production code
- **Code Analysis** - Deep quality and security analysis  
- **Project Generation** - Complete projects from descriptions
- **Code Refactoring** - Intelligent improvement suggestions

### 💰 Cost Optimization
- **Sustainable operation** with intelligent work detection
- **High cache hit rates** after warmup period
- **Progressive complexity** - start cheap, escalate only when needed
- **Token optimization** - minimize API costs while maximizing quality
- **Real-time budget tracking** and cost controls

## 🚀 Quick Start

To get started with Atlas Coder, simply run the setup script:

```bash
./setup.sh
```

This script will:
- Create a Python virtual environment.
- Install all necessary dependencies.
- Configure `direnv` for automatic environment activation (if `direnv` is installed).
- Verify the setup by running `atlas-coder status`.

After running the setup script, you will need to set your `OPENROUTER_API_KEY` in a `.env` file in the project root. You can get a free API key from [OpenRouter](https://openrouter.ai/).

Example `.env` file:
```
OPENROUTER_API_KEY=your_api_key_here
```

## 🧪 Continuous Integration (CI)

This project uses GitHub Actions for continuous integration. The CI pipeline includes:
- Running tests (`pytest`)
- Linting (`ruff`)
- Type checking (`mypy`)
- Code formatting checks (`black --check`)

The CI configuration is defined in [.github/workflows/ci.yml](.github/workflows/ci.yml).

## 🏗️ Architecture

### Core Components
- **`atlas_coder/core/signatures.py`** - Declarative behavior definitions
- **`atlas_coder/core/modules.py`** - Composable programming modules
- **`atlas_coder/core/workflows.py`** - Complete development workflows
- **`atlas_coder/core/engine.py`** - Model management and optimization
- **`atlas_coder/dspy/caching.py`** - Smart caching for efficiency

## 📚 Documentation

This project uses [MkDocs](https://www.mkdocs.org/) with the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme for documentation.

To build and serve the documentation locally, run the following commands:

```bash
# Install documentation dependencies
pip install -e .[docs]

# Build and serve the documentation
mkdocs serve
```

Then, open your web browser to `http://127.0.0.1:8000` to view the documentation.

## 🚀 End-User Workflows

Atlas Coder provides powerful command-line tools to streamline your development workflows. Here are some common use cases:

### Generate Code

Generate new code based on your requirements. You can specify the level of detail and the model strategy to use.

```bash
atlas-coder generate "Create a Python function to validate email addresses" --level detailed --model-strategy quality-optimal
```

- `--level`: Controls the complexity and cost of the generation process. Options: `quick`, `detailed`, `premium`.
- `--model-strategy`: Determines which models are preferred for the task. Options: `cost-optimal`, `quality-optimal`, `balanced`, `local-only`.

### Fix Bugs

Systematically diagnose and fix bugs in your code.

```bash
atlas-coder fix-bug my_buggy_script.py "TypeError: 'NoneType' object is not subscriptable" --level detailed
```

### Analyze Code

Perform deep quality and security analysis on your codebase.

```bash
atlas-coder analyze my_project/ --level quick
```

### Generate Project

Generate complete project structures from high-level descriptions.

```bash
atlas-coder project "A simple web application using Flask and a SQLite database" --level premium
```

### Refactor Code

Get intelligent suggestions for refactoring and improving your code.

```bash
atlas-coder refactor my_old_code.py --level detailed
```

### YOLO Mode

For advanced users, `--yolo` mode disables interactive confirmations for file writes and Git commits. Use with caution!

```bash
atlas-coder generate "Create a new feature" --yolo
```

## 🤝 Contributing

We welcome contributions! Areas of focus:
- New workflow types
- Additional model integrations
- Performance optimizations
- Documentation improvements

## 📄 License

MIT License - build something revolutionary that's freely available to everyone.

## 🌟 Philosophy

Atlas Coder DSPy represents a fundamental shift from "AI assistance" to "systematic programming." By using DSPy's declarative approach, we democratize advanced AI coding capabilities through systematic programming rather than expensive model access.

**The goal: Make sophisticated coding AI accessible to everyone, regardless of budget.**

