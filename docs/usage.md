# Basic Usage (v6)

```bash
# Progressive complexity execution
python atlas_dspy_v6.py fix-bug buggy_code.py "Error message" --level quick
python atlas_dspy_v6.py generate "REST API" --model-strategy cost-optimal

# Agentic operation
python atlas_dspy_v6.py agent --run-continuous --max-budget 2.00
python atlas_dspy_v6.py agent --scan-work

# Cost optimization  
python atlas_dspy_v6.py optimize --analyze-costs --suggest-improvements
python atlas_dspy_v6.py bootstrap "new feature description"

# Check v6 status
python atlas_dspy_v6.py status
```

## Execution Levels
- `--level quick` - Fast, minimal cost (local models preferred)
- `--level detailed` - Balanced quality/cost (smart model selection)  
- `--level premium` - Highest quality (premium models when justified)

## Model Strategies
- `--model-strategy cost-optimal` - Prefer free/cheap models
- `--model-strategy quality-optimal` - Best quality within budget
- `--model-strategy balanced` - Optimal quality/cost ratio
- `--model-strategy local-only` - Use only local models

# Examples

## Bug Fixing Example
```python
from dspy_core.workflows import get_orchestrator

orchestrator = get_orchestrator()
result = orchestrator.execute_workflow(
    "bug_fix",
    code=buggy_code,
    error="ZeroDivisionError: division by zero"
)

print(result.data['fixed_code'])
print(result.data['fix_explanation'])
```

## Code Generation Example
```python
result = orchestrator.execute_workflow(
    "generate",
    requirements="Create a function to validate email addresses",
    constraints="Use only standard library"
)

print(result.data['code'])
print(result.data['tests'])
```

# Advanced Usage

## Custom Workflows
```python
from dspy_core.workflows import BaseWorkflow

class CustomWorkflow(BaseWorkflow):
    def execute(self, **kwargs):
        # Your systematic programming logic
        pass
```

## Model Configuration
```python
from dspy_core.engine import initialize_engine

# Use specific model
engine = initialize_engine("ollama/codellama")

# Check performance
info = engine.get_model_info()
print(f"Cache hit rate: {info['cache_hit_rate']}")
```
