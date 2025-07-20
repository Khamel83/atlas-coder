#!/usr/bin/env python3
"""
Atlas Coder DSPy CLI
Revolutionary systematic programming interface
"""

import os
import sys
import argparse
import json
from typing import Optional
from dspy_core.engine import get_engine, initialize_engine
from dspy_core.workflows import get_orchestrator

def setup_cli():
    """Setup command line interface"""
    parser = argparse.ArgumentParser(
        description="Atlas Coder DSPy - Systematic Programming Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s fix-bug file.py "Authentication not working"
  %(prog)s generate "Create a REST API for user management"
  %(prog)s analyze project.py
  %(prog)s project "Build a todo app with SQLite database"
  %(prog)s refactor legacy_code.py "improve performance"
  
Available workflows:
  bug_fix    - Fix bugs systematically
  generate   - Generate code from requirements
  analyze    - Analyze code quality and structure
  project    - Generate complete projects
  refactor   - Refactor and improve code
        """
    )
    
    parser.add_argument(
        "workflow",
        choices=["fix-bug", "generate", "analyze", "project", "refactor", "status", "test", "list"],
        help="Workflow to execute"
    )
    
    parser.add_argument(
        "input",
        nargs="?",
        help="Input (file path, code, or requirements)"
    )
    
    parser.add_argument(
        "context", 
        nargs="?",
        help="Additional context (error message, goals, etc.)"
    )
    
    parser.add_argument(
        "--model",
        help="Model to use (default: auto-detect free model)"
    )
    
    parser.add_argument(
        "--output",
        help="Output file for generated code"
    )
    
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    return parser

def read_input(input_arg: str) -> str:
    """Read input from file or use as direct input"""
    if not input_arg:
        return ""
    
    # Check if it's a file path
    if os.path.isfile(input_arg):
        try:
            with open(input_arg, 'r') as f:
                return f.read()
        except Exception as e:
            print(f"⚠️ Could not read file {input_arg}: {e}")
            return input_arg
    
    # Use as direct input
    return input_arg

def format_output(result, format_type: str, verbose: bool = False):
    """Format and display workflow results"""
    if not result.success:
        print(f"❌ Error: {result.error}")
        return
    
    if format_type == "json":
        print(json.dumps(result.to_dict(), indent=2))
        return
    
    # Text format
    data = result.data
    
    if "fixed_code" in data:
        # Bug fixing workflow
        print("🐛 Bug Fix Results:")
        print(f"\n📊 Diagnosis:\n{data.get('diagnosis', 'N/A')}")
        print(f"\n🔧 Fix:\n{data.get('fix_explanation', 'N/A')}")
        print(f"\n✅ Fixed Code:\n{data.get('fixed_code', 'N/A')}")
        
        if verbose and data.get('validation_tests'):
            print(f"\n🧪 Validation Tests:\n{data.get('validation_tests')}")
    
    elif "code" in data and "explanation" in data:
        # Code generation workflow
        print("⚡ Code Generation Results:")
        print(f"\n📝 Understanding:\n{data.get('understanding', 'N/A')}")
        print(f"\n💡 Code:\n{data.get('code', 'N/A')}")
        print(f"\n📖 Explanation:\n{data.get('explanation', 'N/A')}")
        
        if verbose and data.get('tests'):
            print(f"\n🧪 Tests:\n{data.get('tests')}")
    
    elif "analysis" in data:
        # Analysis workflow
        print("🔍 Code Analysis Results:")
        print(f"\n📊 Analysis:\n{data.get('analysis', 'N/A')}")
        print(f"\n⚠️ Issues:\n{data.get('issues', 'N/A')}")
        print(f"\n🏗️ Architecture:\n{data.get('architecture', 'N/A')}")
        
        if verbose and data.get('suggestions'):
            print(f"\n💡 Suggestions:\n{data.get('suggestions')}")
    
    elif "refactored_code" in data:
        # Refactoring workflow
        print("🔧 Refactoring Results:")
        print(f"\n✨ Improvements:\n{data.get('improvements', 'N/A')}")
        print(f"\n🔄 Refactored Code:\n{data.get('refactored_code', 'N/A')}")
        
        if verbose and data.get('migration_guide'):
            print(f"\n📋 Migration Guide:\n{data.get('migration_guide')}")
    
    else:
        # Generic output
        print("✅ Results:")
        for key, value in data.items():
            if key not in ['original_code', 'code'] or verbose:
                print(f"\n{key.replace('_', ' ').title()}:\n{value}")

def save_output(result, output_file: str):
    """Save results to output file"""
    try:
        data = result.data
        
        # Determine what to save based on workflow
        output_content = ""
        
        if "fixed_code" in data:
            output_content = data["fixed_code"]
        elif "refactored_code" in data:
            output_content = data["refactored_code"]
        elif "code" in data:
            output_content = data["code"]
        else:
            output_content = json.dumps(data, indent=2)
        
        with open(output_file, 'w') as f:
            f.write(output_content)
        
        print(f"💾 Output saved to {output_file}")
        
    except Exception as e:
        print(f"⚠️ Could not save output: {e}")

def main():
    """Main CLI entry point"""
    parser = setup_cli()
    args = parser.parse_args()
    
    try:
        # Initialize engine with specified model
        if args.model:
            engine = initialize_engine(args.model)
        else:
            engine = get_engine()
        
        # Handle special commands
        if args.workflow == "status":
            info = engine.get_model_info()
            print("🔧 Atlas Coder DSPy Status:")
            for key, value in info.items():
                print(f"  {key}: {value}")
            return
        
        if args.workflow == "test":
            print("🧪 Testing model connection...")
            success = engine.test_model()
            if success:
                print("✅ Model test successful!")
            else:
                print("❌ Model test failed!")
            return
        
        if args.workflow == "list":
            orchestrator = get_orchestrator()
            workflows = orchestrator.list_workflows()
            print("📋 Available Workflows:")
            for workflow in workflows:
                status = "✅" if workflow["available"] else "❌"
                print(f"  {status} {workflow['type']}: {workflow.get('description', 'No description')}")
            return
        
        # Validate required input for workflows
        if not args.input and args.workflow not in ["status", "test", "list"]:
            print("❌ Error: Input required for this workflow")
            parser.print_help()
            sys.exit(1)
        
        # Read input
        input_content = read_input(args.input)
        context_content = args.context or ""
        
        # Get orchestrator and execute workflow
        orchestrator = get_orchestrator()
        
        # Map CLI workflows to internal workflow types
        workflow_map = {
            "fix-bug": "bug_fix",
            "generate": "generate", 
            "analyze": "analyze",
            "project": "project",
            "refactor": "refactor"
        }
        
        workflow_type = workflow_map.get(args.workflow)
        if not workflow_type:
            print(f"❌ Unknown workflow: {args.workflow}")
            sys.exit(1)
        
        print(f"🚀 Executing {workflow_type} workflow...")
        
        # Prepare workflow parameters based on type
        if workflow_type == "bug_fix":
            result = orchestrator.execute_workflow(
                workflow_type,
                code=input_content,
                error=context_content or "General error analysis"
            )
        elif workflow_type == "generate":
            result = orchestrator.execute_workflow(
                workflow_type,
                requirements=input_content,
                constraints=context_content
            )
        elif workflow_type == "analyze":
            result = orchestrator.execute_workflow(
                workflow_type,
                code=input_content,
                context=context_content
            )
        elif workflow_type == "project":
            result = orchestrator.execute_workflow(
                workflow_type,
                requirements=input_content,
                constraints=context_content
            )
        elif workflow_type == "refactor":
            result = orchestrator.execute_workflow(
                workflow_type,
                code=input_content,
                goals=context_content or "improve readability and maintainability"
            )
        
        # Display results
        format_output(result, args.format, args.verbose)
        
        # Save output if requested
        if args.output and result.success:
            save_output(result, args.output)
    
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()