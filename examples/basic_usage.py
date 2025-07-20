#!/usr/bin/env python3
"""
Atlas Coder DSPy Examples
Demonstrating revolutionary systematic programming
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dspy_core.engine import initialize_engine
from dspy_core.workflows import get_orchestrator

def example_bug_fixing():
    """Example: Fix a bug systematically"""
    print("🐛 Example: Bug Fixing Workflow")
    print("=" * 50)
    
    # Sample buggy code
    buggy_code = '''
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)  # Bug: Division by zero if numbers is empty

# Usage
scores = []
avg = calculate_average(scores)  # This will crash!
print(f"Average: {avg}")
'''
    
    error_message = "ZeroDivisionError: division by zero"
    
    orchestrator = get_orchestrator()
    result = orchestrator.execute_workflow(
        "bug_fix",
        code=buggy_code,
        error=error_message,
        context="Function crashes when called with empty list"
    )
    
    if result.success:
        print("✅ Bug fixed successfully!")
        print(f"\n🔧 Fixed Code:\n{result.data['fixed_code']}")
        print(f"\n📝 Explanation:\n{result.data['fix_explanation']}")
    else:
        print(f"❌ Bug fixing failed: {result.error}")

def example_code_generation():
    """Example: Generate code from requirements"""
    print("\n⚡ Example: Code Generation Workflow")
    print("=" * 50)
    
    requirements = """
    Create a Python function that:
    1. Takes a list of student grades (0-100)
    2. Calculates letter grades (A, B, C, D, F)
    3. Returns a summary with count of each letter grade
    4. Handles edge cases like empty lists
    5. Includes proper error handling
    """
    
    orchestrator = get_orchestrator()
    result = orchestrator.execute_workflow(
        "generate",
        requirements=requirements,
        constraints="Use only standard Python library, focus on readability"
    )
    
    if result.success:
        print("✅ Code generated successfully!")
        print(f"\n💡 Generated Code:\n{result.data['code']}")
        print(f"\n📖 Explanation:\n{result.data['explanation']}")
    else:
        print(f"❌ Code generation failed: {result.error}")

def example_code_analysis():
    """Example: Analyze code quality"""
    print("\n🔍 Example: Code Analysis Workflow")
    print("=" * 50)
    
    code_to_analyze = '''
import requests
import json

def get_user_data(user_id):
    url = f"https://api.example.com/users/{user_id}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data["user_info"]

def process_users(user_ids):
    results = []
    for id in user_ids:
        user = get_user_data(id)
        results.append(user)
    return results
'''
    
    orchestrator = get_orchestrator()
    result = orchestrator.execute_workflow(
        "analyze",
        code=code_to_analyze,
        context="API client code for user management system"
    )
    
    if result.success:
        print("✅ Analysis completed!")
        print(f"\n📊 Analysis:\n{result.data['analysis']}")
        print(f"\n⚠️ Issues Found:\n{result.data['issues']}")
        print(f"\n💡 Suggestions:\n{result.data['suggestions']}")
    else:
        print(f"❌ Analysis failed: {result.error}")

def example_project_generation():
    """Example: Generate a complete project"""
    print("\n🚀 Example: Full Project Generation")
    print("=" * 50)
    
    project_requirements = """
    Create a simple TODO application with:
    1. Add, remove, and list TODO items
    2. Mark items as complete/incomplete
    3. Save data to a JSON file
    4. Command-line interface
    5. Proper error handling and validation
    """
    
    orchestrator = get_orchestrator()
    result = orchestrator.execute_workflow(
        "project",
        requirements=project_requirements,
        constraints="Single Python file, minimal dependencies, beginner-friendly"
    )
    
    if result.success:
        print("✅ Project generated successfully!")
        print(f"\n📝 Understanding:\n{result.data['understanding']}")
        print(f"\n🏗️ Architecture:\n{result.data['architecture_plan']}")
        print(f"\n💻 Code:\n{result.data['code'][:500]}...")
        print("\n[Code truncated for display - full version available]")
    else:
        print(f"❌ Project generation failed: {result.error}")

def main():
    """Run all examples"""
    print("🌟 Atlas Coder DSPy Examples")
    print("Revolutionary Systematic Programming")
    print("=" * 60)
    
    # Initialize engine with free model
    print("🔧 Initializing DSPy engine...")
    try:
        engine = initialize_engine()
        print(f"✅ Engine initialized with model: {engine.model}")
        
        # Test model connection
        if not engine.test_model():
            print("❌ Model test failed - examples may not work properly")
            return
        
        # Show engine info
        info = engine.get_model_info()
        print(f"📊 Engine Info:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        print("\n" + "=" * 60)
        
        # Run examples
        example_bug_fixing()
        example_code_generation()
        example_code_analysis()
        example_project_generation()
        
        print("\n" + "=" * 60)
        print("🎉 All examples completed!")
        print("💡 Try the CLI: python atlas_dspy.py --help")
        
    except Exception as e:
        print(f"❌ Example execution failed: {e}")
        print("💡 Make sure you have set OPENAI_API_KEY or installed Ollama")

if __name__ == "__main__":
    main()