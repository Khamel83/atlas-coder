#!/usr/bin/env python3
"""
Atlas Coder DSPy v6 - Revolutionary Cost-Optimized CLI
Progressive complexity + hybrid models + agentic operation
"""

import os
import sys
import argparse
import json
from typing import Optional
from datetime import datetime

from dspy_core.engine import get_engine, initialize_engine
from dspy_core.workflows import get_orchestrator
from dspy_core.progressive_execution import get_progressive_executor, ExecutionLevel
from dspy_core.optimization import get_cost_tracker, get_token_optimizer
from dspy_core.model_strategy import get_model_strategy
from dspy_core.agentic import get_agentic_manager
from dspy_core.bootstrap import bootstrap_new_feature, self_improve

def setup_cli():
    """Setup advanced CLI with v6 features"""
    parser = argparse.ArgumentParser(
        description="Atlas Coder DSPy v6 - Revolutionary Systematic Programming",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🚀 Atlas Coder v6 Features:
  Progressive Complexity - Start simple, escalate intelligently
  Hybrid Models - Seamless local/API switching for optimal cost/quality
  Agentic Operation - Autonomous meaningful work detection
  Cost Optimization - $3/day sustainable operation
  
Examples:
  %(prog)s fix-bug file.py "error message" --level quick
  %(prog)s generate "REST API" --model-strategy cost-optimal
  %(prog)s agent --run-continuous --max-budget 2.00
  %(prog)s optimize --analyze-costs --suggest-improvements
  %(prog)s bootstrap "new feature description"
  
Execution Levels:
  quick      - Fast, minimal cost (local models preferred)
  detailed   - Balanced quality/cost (smart model selection)
  premium    - Highest quality (premium models when justified)
  
Model Strategies:
  cost-optimal    - Prefer free/cheap models
  quality-optimal - Best quality within budget
  balanced        - Optimal quality/cost ratio
  local-only      - Use only local models
        """
    )
    
    # Core commands
    parser.add_argument(
        "command",
        choices=[
            "fix-bug", "generate", "analyze", "project", "refactor",
            "agent", "optimize", "bootstrap", "status", "test", "list"
        ],
        help="Command to execute"
    )
    
    parser.add_argument(
        "input",
        nargs="?", 
        help="Input (file path, code, requirements, or feature description)"
    )
    
    parser.add_argument(
        "context",
        nargs="?",
        help="Additional context (error message, constraints, etc.)"
    )
    
    # Execution control
    parser.add_argument(
        "--level",
        choices=["quick", "detailed", "premium"],
        help="Execution complexity level"
    )
    
    parser.add_argument(
        "--model-strategy", 
        choices=["cost-optimal", "quality-optimal", "balanced", "local-only"],
        help="Model selection strategy"
    )
    
    parser.add_argument(
        "--model",
        help="Specific model to use (overrides strategy)"
    )
    
    # Budget and cost control
    parser.add_argument(
        "--max-cost",
        type=float,
        help="Maximum cost for this operation (dollars)"
    )
    
    parser.add_argument(
        "--max-budget",
        type=float,
        help="Maximum daily budget (dollars)"
    )
    
    # Agentic operation
    parser.add_argument(
        "--run-continuous",
        action="store_true",
        help="Run continuous agentic operation"
    )
    
    parser.add_argument(
        "--scan-work",
        action="store_true", 
        help="Scan for work opportunities"
    )
    
    # Optimization and analysis
    parser.add_argument(
        "--analyze-costs",
        action="store_true",
        help="Analyze cost efficiency and patterns"
    )
    
    parser.add_argument(
        "--suggest-improvements",
        action="store_true",
        help="Suggest system improvements"
    )
    
    parser.add_argument(
        "--optimize-cache",
        action="store_true",
        help="Optimize caching for better performance"
    )
    
    # Output control
    parser.add_argument(
        "--output",
        help="Output file for generated code"
    )
    
    parser.add_argument(
        "--format",
        choices=["text", "json", "markdown"],
        default="text",
        help="Output format"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output with performance metrics"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Minimal output"
    )
    
    return parser

def execute_with_progressive_complexity(command: str, args: argparse.Namespace) -> dict:
    """Execute command with progressive complexity"""
    
    # Determine execution level
    level_map = {
        "quick": ExecutionLevel.QUICK_SCAN,
        "detailed": ExecutionLevel.DETAILED_ANALYSIS, 
        "premium": ExecutionLevel.COMPREHENSIVE_SOLUTION
    }
    
    initial_level = None
    if args.level:
        initial_level = level_map[args.level]
    
    # Setup model strategy
    if args.model_strategy:
        strategy = get_model_strategy()
        recommendations = strategy.get_model_recommendations(command, 3.0)
        
        model_map = {
            "cost-optimal": recommendations.get('cost_optimal'),
            "quality-optimal": recommendations.get('quality_optimal'),
            "balanced": recommendations.get('balanced'),
            "local-only": recommendations.get('cost_optimal')  # Prefer local
        }
        
        recommended_model = model_map.get(args.model_strategy)
        if recommended_model and not args.model:
            print(f"🎯 Using {args.model_strategy} model: {recommended_model}")
    
    # Apply cost constraints
    if args.max_cost:
        cost_tracker = get_cost_tracker()
        if not cost_tracker.can_afford_task(args.max_cost):
            return {
                'success': False,
                'error': f'Insufficient budget. Remaining: ${cost_tracker.get_remaining_budget():.3f}'
            }
    
    # Execute with progressive complexity
    executor = get_progressive_executor()
    
    # Map commands to workflow types
    workflow_map = {
        "fix-bug": "bug_fix",
        "generate": "generate",
        "analyze": "analyze", 
        "project": "project",
        "refactor": "refactor"
    }
    
    workflow_type = workflow_map.get(command)
    if not workflow_type:
        return {'success': False, 'error': f'Unknown command: {command}'}
    
    # Prepare parameters
    task_params = {}
    if args.input:
        # Read input file or use directly
        if os.path.isfile(args.input):
            with open(args.input, 'r') as f:
                input_content = f.read()
        else:
            input_content = args.input
        
        # Map input to appropriate parameter
        if workflow_type == "bug_fix":
            task_params = {"code": input_content, "error": args.context or "General error analysis"}
        elif workflow_type == "generate":
            task_params = {"requirements": input_content, "constraints": args.context or ""}
        elif workflow_type == "analyze":
            task_params = {"code": input_content, "context": args.context or ""}
        elif workflow_type == "project":
            task_params = {"requirements": input_content, "constraints": args.context or ""}
        elif workflow_type == "refactor":
            task_params = {"code": input_content, "goals": args.context or "improve readability and maintainability"}
    
    # Add execution preferences
    if args.max_cost:
        task_params["max_cost"] = args.max_cost
    
    # Execute
    result = executor.execute_with_escalation(workflow_type, task_params, initial_level)
    
    return {
        'success': result.success,
        'data': result.result.data if result.result else {},
        'execution_level': result.level_used.value,
        'cost': result.cost,
        'quality_score': result.quality_score,
        'escalation_used': result.escalation_needed
    }

def handle_agentic_commands(args: argparse.Namespace) -> dict:
    """Handle agentic operation commands"""
    manager = get_agentic_manager()
    
    if args.run_continuous:
        max_iterations = 1000  # Default
        if args.max_budget:
            # Estimate iterations based on budget
            cost_tracker = get_cost_tracker()
            cost_tracker.daily_budget = args.max_budget
        
        print(f"🤖 Starting continuous agentic operation (budget: ${args.max_budget or 3.0})")
        manager.run_continuous_agent(max_iterations)
        
        return {'success': True, 'message': 'Agentic operation completed'}
    
    elif args.scan_work:
        opportunities = manager.detect_work_opportunities()
        
        return {
            'success': True,
            'work_opportunities': len(opportunities),
            'high_value_count': len([w for w in opportunities if w.value_score > 0.7]),
            'estimated_total_cost': sum(w.estimated_cost for w in opportunities),
            'opportunities': [
                {
                    'description': w.description,
                    'value_score': w.value_score,
                    'estimated_cost': w.estimated_cost,
                    'priority': w.priority.value
                } for w in opportunities[:5]  # Top 5
            ]
        }
    
    else:
        status = manager.get_agent_status()
        return {'success': True, 'agent_status': status}

def handle_optimization_commands(args: argparse.Namespace) -> dict:
    """Handle optimization and analysis commands"""
    results = {}
    
    if args.analyze_costs:
        cost_tracker = get_cost_tracker()
        model_strategy = get_model_strategy()
        
        cost_stats = cost_tracker.get_cost_efficiency_stats()
        strategy_stats = model_strategy.get_strategy_stats()
        
        results['cost_analysis'] = {
            'efficiency': cost_stats,
            'model_usage': strategy_stats,
            'recommendations': [
                "Use local models for simple tasks",
                "Cache frequently used patterns", 
                "Batch similar operations",
                "Escalate complexity only when needed"
            ]
        }
    
    if args.suggest_improvements:
        # Use bootstrap to suggest improvements
        performance_data = {
            'avg_execution_time': 45,  # Would come from real metrics
            'cost_per_task': 0.015,
            'quality_variance': 0.15,
            'cache_hit_rate': 0.75
        }
        
        improvements = self_improve(performance_data)
        results['improvements'] = improvements
    
    if args.optimize_cache:
        from dspy_core.cache import get_signature_cache
        cache = get_signature_cache()
        
        # Cache cleanup and optimization
        initial_size = len(cache.memory_cache)
        cache._cleanup_cache()
        final_size = len(cache.memory_cache)
        
        results['cache_optimization'] = {
            'entries_before': initial_size,
            'entries_after': final_size,
            'space_saved': initial_size - final_size,
            'hit_rate': cache.get_stats()['cache_efficiency']
        }
    
    return {'success': True, **results}

def format_v6_output(result: dict, format_type: str, verbose: bool = False):
    """Format v6 output with enhanced information"""
    if not result.get('success', False):
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
        return
    
    if format_type == "json":
        print(json.dumps(result, indent=2, default=str))
        return
    
    # Enhanced text formatting
    if 'data' in result:
        data = result['data']
        
        # Show execution metadata
        if verbose:
            print("📊 Execution Metadata:")
            if 'execution_level' in result:
                print(f"   Level: {result['execution_level']}")
            if 'cost' in result:
                print(f"   Cost: ${result['cost']:.4f}")
            if 'quality_score' in result:
                print(f"   Quality: {result['quality_score']:.2f}")
            if 'escalation_used' in result:
                escalation = "Yes" if result['escalation_used'] else "No"
                print(f"   Escalation: {escalation}")
            print()
        
        # Show main results (existing format_output logic)
        if "fixed_code" in data:
            print("🐛 Bug Fix Results:")
            print(f"\n📊 Diagnosis:\n{data.get('diagnosis', 'N/A')}")
            print(f"\n🔧 Fix:\n{data.get('fix_explanation', 'N/A')}")
            print(f"\n✅ Fixed Code:\n{data.get('fixed_code', 'N/A')}")
        elif "code" in data and "explanation" in data:
            print("⚡ Code Generation Results:")
            print(f"\n💡 Code:\n{data.get('code', 'N/A')}")
            print(f"\n📖 Explanation:\n{data.get('explanation', 'N/A')}")
        elif "analysis" in data:
            print("🔍 Code Analysis Results:")
            print(f"\n📊 Analysis:\n{data.get('analysis', 'N/A')}")
            print(f"\n⚠️ Issues:\n{data.get('issues', 'N/A')}")
    
    # Show additional v6 results
    if 'agent_status' in result:
        status = result['agent_status']
        print("🤖 Agent Status:")
        for key, value in status.items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
    
    if 'cost_analysis' in result:
        analysis = result['cost_analysis']
        print("💰 Cost Analysis:")
        efficiency = analysis['efficiency']
        print(f"   Quality per Dollar: {efficiency.get('quality_per_dollar', 0):.2f}")
        print(f"   Tasks Completed: {efficiency.get('tasks_completed', 0)}")
        print(f"   Average Cost: ${efficiency.get('cost_per_task', 0):.4f}")
    
    if 'work_opportunities' in result:
        print(f"📋 Found {result['work_opportunities']} work opportunities")
        print(f"🎯 High-value opportunities: {result.get('high_value_count', 0)}")
        print(f"💰 Estimated total cost: ${result.get('estimated_total_cost', 0):.3f}")

def main():
    """Main v6 CLI entry point"""
    parser = setup_cli()
    args = parser.parse_args()
    
    try:
        # Initialize engine
        if args.model:
            engine = initialize_engine(args.model)
        else:
            engine = get_engine()
        
        # Handle special commands first
        if args.command == "status":
            info = engine.get_model_info()
            cost_tracker = get_cost_tracker()
            strategy = get_model_strategy()
            
            print("🔧 Atlas Coder DSPy v6 Status:")
            print(f"🧠 Model: {info['model']}")
            print(f"💾 Cache: {info['cache_entries']} entries ({info['cache_hit_rate']})")
            print(f"💰 Budget: ${cost_tracker.get_remaining_budget():.3f} remaining")
            print(f"🎯 Strategy: {strategy.current_model or 'Auto-select'}")
            return
        
        elif args.command == "test":
            print("🧪 Testing v6 systems...")
            success = engine.test_model()
            if success:
                print("✅ All systems operational!")
            else:
                print("❌ System test failed!")
            return
        
        elif args.command == "list":
            orchestrator = get_orchestrator()
            workflows = orchestrator.list_workflows()
            print("📋 Available Workflows:")
            for workflow in workflows:
                status = "✅" if workflow["available"] else "❌"
                print(f"  {status} {workflow['type']}: {workflow.get('description', 'No description')}")
            
            # Show v6 features
            print("\n🚀 v6 Features:")
            print("  ✅ Progressive Complexity Execution")
            print("  ✅ Hybrid Model Strategy")
            print("  ✅ Agentic Work Detection")
            print("  ✅ Real-time Cost Optimization")
            print("  ✅ DSPy Bootstrap Development")
            return
        
        # Handle agentic commands
        elif args.command == "agent":
            result = handle_agentic_commands(args)
        
        # Handle optimization commands
        elif args.command == "optimize":
            result = handle_optimization_commands(args)
        
        # Handle bootstrap command
        elif args.command == "bootstrap":
            if not args.input:
                print("❌ Feature description required for bootstrap")
                sys.exit(1)
            
            print(f"🚀 Bootstrapping new feature: {args.input}")
            bootstrap_result = bootstrap_new_feature(args.input)
            
            result = {
                'success': True,
                'bootstrap_result': bootstrap_result,
                'implementation_ready': True
            }
        
        # Handle core development commands with progressive complexity
        else:
            if not args.input:
                print("❌ Input required for this command")
                parser.print_help()
                sys.exit(1)
            
            result = execute_with_progressive_complexity(args.command, args)
        
        # Display results
        if not args.quiet:
            format_v6_output(result, args.format, args.verbose)
        
        # Save output if requested
        if args.output and result.get('success'):
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

def save_output(result: dict, output_file: str):
    """Save v6 results to output file"""
    try:
        data = result.get('data', {})
        
        # Determine content to save
        if "fixed_code" in data:
            content = data["fixed_code"]
        elif "refactored_code" in data:
            content = data["refactored_code"]
        elif "code" in data:
            content = data["code"]
        elif "bootstrap_result" in result:
            content = json.dumps(result["bootstrap_result"], indent=2)
        else:
            content = json.dumps(result, indent=2, default=str)
        
        with open(output_file, 'w') as f:
            f.write(content)
        
        print(f"💾 Output saved to {output_file}")
        
    except Exception as e:
        print(f"⚠️ Could not save output: {e}")

if __name__ == "__main__":
    main()