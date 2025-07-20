#!/usr/bin/env python3
"""Real usage demonstration of Atlas Coder.

This script demonstrates real-world usage of Atlas Coder for:
1. Bug fixing with CompleteBugFixer
2. Code generation
3. Cost tracking
4. Analysis workflows
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from atlas_coder.core.engine import AtlasCoderEngine
from atlas_coder.core.modules import CompleteBugFixer, CodeGenerator, CodeAnalyzer
from atlas_coder.utils.logging import get_logger


def demo_cost_tracking():
    """Demonstrate cost tracking functionality."""
    print("🔄 Demo: Cost Tracking System")
    
    # Initialize engine with local-only strategy (no API costs)
    engine = AtlasCoderEngine(model_strategy="local-only", daily_budget=1.0)
    
    # Get status
    status = engine.get_status()
    print(f"✅ Model Strategy: {status['model_strategy']}")
    print(f"✅ Daily Budget: ${status['daily_budget']:.2f}")
    print(f"✅ Current Cost: ${status['current_cost']:.4f}")
    print(f"✅ Calls Made: {status['calls_made']}")
    print()


def demo_bug_fixing():
    """Demonstrate bug fixing workflow."""
    print("🔄 Demo: CompleteBugFixer Module")
    
    # Sample buggy code
    buggy_code = '''
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)  # Bug: Division by zero if empty list

# Usage
scores = []
average = calculate_average(scores)  # This will crash!
print(f"Average: {average}")
'''
    
    error_message = "ZeroDivisionError: division by zero"
    
    print("🐛 Buggy Code:")
    print(buggy_code)
    print(f"❌ Error: {error_message}")
    print()
    
    # Note: This would use actual DSPy modules in a real scenario
    # For demo purposes, we'll show the expected workflow
    print("✅ Bug fixing workflow would:")
    print("  1. Diagnose the root cause (division by zero)")
    print("  2. Generate fixed code with proper validation")
    print("  3. Create tests to prevent regression")
    print("  4. Track API costs for the operation")
    print()


def demo_code_generation():
    """Demonstrate code generation workflow."""
    print("🔄 Demo: Code Generation")
    
    requirements = "Create a simple REST API endpoint for user authentication with JWT tokens"
    
    print(f"📝 Requirements: {requirements}")
    print()
    print("✅ Code generation would:")
    print("  1. Generate Flask/FastAPI endpoint code")
    print("  2. Include JWT token validation")
    print("  3. Add proper error handling")
    print("  4. Generate accompanying tests")
    print("  5. Include usage documentation")
    print()


def demo_cost_analysis():
    """Demonstrate cost analysis for different model strategies."""
    print("🔄 Demo: Cost Analysis by Model Strategy")
    
    strategies = ["cost-optimal", "quality-optimal", "local-only"]
    
    for strategy in strategies:
        engine = AtlasCoderEngine(model_strategy=strategy, daily_budget=1.0)
        
        # Estimate cost for typical operations
        typical_cost = engine.estimate_cost(input_tokens=2000, output_tokens=1000)
        
        print(f"📊 {strategy.title()}:")
        print(f"   Model: {engine.current_model.model if hasattr(engine.current_model, 'model') else 'Local'}")
        print(f"   Cost per call: ${typical_cost:.4f}")
        print(f"   Calls per day (${engine.cost_tracker.daily_budget} budget): {int(engine.cost_tracker.daily_budget / max(typical_cost, 0.001))}")
        print()


def demo_cli_usage():
    """Demonstrate CLI usage examples."""
    print("🔄 Demo: CLI Usage Examples")
    
    cli_examples = [
        "# Fix a bug in your code",
        "atlas-coder fix-bug buggy_script.py --error 'IndexError on line 42'",
        "",
        "# Generate new code",
        "atlas-coder generate 'REST API with user authentication' --level detailed",
        "",
        "# Analyze code quality",
        "atlas-coder analyze myproject/ --focus security",
        "",
        "# Get cost report",
        "atlas-coder cost-report",
        "",
        "# Use local-only mode (no API costs)",
        "atlas-coder --model-strategy local-only status",
        "",
        "# Enable YOLO mode for automatic operations",
        "atlas-coder --yolo fix-bug script.py",
    ]
    
    for example in cli_examples:
        if example.startswith("#"):
            print(f"\033[92m{example}\033[0m")  # Green for comments
        elif example == "":
            print()
        else:
            print(f"\033[94m$ {example}\033[0m")  # Blue for commands


def main():
    """Main demo function."""
    print("🚀 Atlas Coder - Real Usage Demonstration")
    print("=" * 50)
    print()
    
    # Setup logging
    logger = get_logger(level="INFO", use_rich=True)
    logger.info("Starting Atlas Coder demonstration")
    
    try:
        demo_cost_tracking()
        demo_bug_fixing()
        demo_code_generation()
        demo_cost_analysis()
        demo_cli_usage()
        
        print("✅ Demo completed successfully!")
        print()
        print("🎯 Next Steps:")
        print("1. Set OPENROUTER_API_KEY for cloud models")
        print("2. Try: atlas-coder --help")
        print("3. Start with: atlas-coder status")
        print("4. Read the docs: README.md")
        
        logger.info("Demo completed successfully")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"❌ Demo failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())