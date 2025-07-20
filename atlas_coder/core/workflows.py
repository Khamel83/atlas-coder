"""Workflow orchestration for Atlas Coder.

This module orchestrates the execution of DSPy-powered workflows for bug fixing,
code generation, analysis, and other Atlas Coder functions.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.json import JSON

from .engine import AtlasCoderEngine
from .modules import (
    CompleteBugFixer, CodeGenerator, CodeAnalyzer, 
    CodeRefactorer, ProgramOfThought
)

console = Console()


class WorkflowOrchestrator:
    """Orchestrates the execution of Atlas Coder workflows."""
    
    def __init__(self, 
                 model_strategy: str = "cost-optimal",
                 daily_budget: float = 1.0,
                 yolo_mode: bool = False):
        """Initialize the WorkflowOrchestrator.
        
        Args:
            model_strategy: Model strategy for cost/quality optimization
            daily_budget: Daily budget limit in USD
            yolo_mode: If True, automatically save files without prompting
        """
        self.engine = AtlasCoderEngine(model_strategy=model_strategy, daily_budget=daily_budget)
        self.yolo_mode = yolo_mode
        
        # Initialize DSPy modules
        self.bug_fixer = CompleteBugFixer()
        self.code_generator = CodeGenerator()
        self.code_analyzer = CodeAnalyzer()
        self.code_refactorer = CodeRefactorer()
        self.program_of_thought = ProgramOfThought()
    
    def _display_status(self) -> None:
        """Display current engine status."""
        status = self.engine.get_status()
        console.print(Panel(f"""
[bold blue]Atlas Coder Status[/bold blue]
Model: {status['current_model']}
Strategy: {status['model_strategy']}
Daily Budget: ${status['daily_budget']:.2f}
Current Cost: ${status['current_cost']:.4f}
Remaining: ${status['remaining_budget']:.4f}
Calls Made: {status['calls_made']}
""", border_style="blue"))
    
    def _save_result(self, result: Dict[str, Any], filename: str) -> None:
        """Save workflow result to file if in YOLO mode or user confirms."""
        if not self.yolo_mode:
            save = console.input(f"Save result to {filename}? (y/N): ").lower().startswith('y')
            if not save:
                return
        
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        console.print(f"[green]✓ Result saved to {filename}[/green]")
    
    def generate(self, requirements: str, level: str = "detailed", model_strategy: str = "cost-optimal") -> str:
        """Generate new code based on requirements.
        
        Args:
            requirements: The requirements for code generation
            level: Execution level (quick, detailed, premium)
            model_strategy: Model strategy override
            
        Returns:
            Success message with generated code info
        """
        self._display_status()
        
        if not self.engine.can_execute():
            return "❌ Daily budget exceeded. Cannot generate code."
        
        try:
            console.print(f"[blue]Generating code for: {requirements}[/blue]")
            
            # Execute code generation with cost tracking
            result = self.engine.execute_with_tracking(
                self.code_generator,
                requirements=requirements,
                language="Python"
            )
            
            # Format and display result
            output = {
                "requirements": requirements,
                "level": level,
                "model_strategy": model_strategy,
                "generated_code": result.code,
                "structure": result.structure,
                "usage_example": result.usage_example,
                "timestamp": str(console._get_time())
            }
            
            console.print(Panel(f"[bold green]Generated Code:[/bold green]\n{result.code}", 
                              title="Code Generation Result", border_style="green"))
            console.print(f"[blue]Structure:[/blue] {result.structure}")
            console.print(f"[blue]Usage:[/blue] {result.usage_example}")
            
            # Save result
            self._save_result(output, f"atlas_output/generated_code_{len(requirements.split())}_words.json")
            
            return f"✅ Code generated successfully for '{requirements[:50]}...'"
            
        except Exception as e:
            console.print(f"[red]❌ Error generating code: {e}[/red]")
            return f"❌ Code generation failed: {e}"
    
    def fix_bug(self, code_file: str, error_message: str = "", level: str = "detailed") -> str:
        """Fix a bug in the given code file.
        
        Args:
            code_file: Path to the buggy code file
            error_message: Error message associated with the bug
            level: Execution level (quick, detailed, premium)
            
        Returns:
            Success message with fix details
        """
        self._display_status()
        
        if not self.engine.can_execute():
            return "❌ Daily budget exceeded. Cannot fix bug."
        
        try:
            # Read the code file
            if not os.path.exists(code_file):
                return f"❌ File not found: {code_file}"
            
            with open(code_file, 'r') as f:
                code = f.read()
            
            console.print(f"[blue]Fixing bug in: {code_file}[/blue]")
            
            # Execute complete bug fixing workflow
            result = self.engine.execute_with_tracking(
                self.bug_fixer,
                code=code,
                error_message=error_message,
                context=f"File: {code_file}"
            )
            
            # Display results
            console.print(Panel(f"""
[bold red]Diagnosis:[/bold red] {result['diagnosis']['diagnosis']}
[bold yellow]Root Cause:[/bold yellow] {result['diagnosis']['root_cause']}
[bold blue]Severity:[/bold blue] {result['diagnosis']['severity']}
""", title="Bug Analysis", border_style="red"))
            
            console.print(Panel(f"[bold green]Fixed Code:[/bold green]\n{result['fix']['fixed_code']}", 
                              title="Fixed Code", border_style="green"))
            
            console.print(f"[blue]Changes Made:[/blue] {result['fix']['changes_made']}")
            console.print(f"[blue]Explanation:[/blue] {result['fix']['explanation']}")
            
            if result.get('tests'):
                console.print(Panel(f"[bold purple]Test Code:[/bold purple]\n{result['tests']['test_code']}", 
                                  title="Generated Tests", border_style="purple"))
            
            # Save fixed code
            if self.yolo_mode or console.input(f"Apply fix to {code_file}? (y/N): ").lower().startswith('y'):
                # Backup original
                backup_path = f"{code_file}.backup"
                with open(backup_path, 'w') as f:
                    f.write(code)
                
                # Write fixed code
                with open(code_file, 'w') as f:
                    f.write(result['fix']['fixed_code'])
                
                console.print(f"[green]✓ Fix applied to {code_file} (backup saved as {backup_path})[/green]")
            
            # Save full result
            self._save_result(result, f"atlas_output/bug_fix_{Path(code_file).stem}.json")
            
            return f"✅ Bug fixed in {code_file}. Severity: {result['diagnosis']['severity']}"
            
        except Exception as e:
            console.print(f"[red]❌ Error fixing bug: {e}[/red]")
            return f"❌ Bug fix failed: {e}"
    
    def analyze(self, target: str, level: str = "detailed") -> str:
        """Analyze code for quality and security.
        
        Args:
            target: Path to code file or directory to analyze
            level: Execution level (quick, detailed, premium)
            
        Returns:
            Success message with analysis summary
        """
        self._display_status()
        
        if not self.engine.can_execute():
            return "❌ Daily budget exceeded. Cannot analyze code."
        
        try:
            # Read code from file or directory
            if os.path.isfile(target):
                with open(target, 'r') as f:
                    code = f.read()
            elif os.path.isdir(target):
                # Analyze multiple files (simplified for MVP)
                code_files = []
                for root, dirs, files in os.walk(target):
                    for file in files:
                        if file.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c')):
                            code_files.append(os.path.join(root, file))
                
                if not code_files:
                    return f"❌ No code files found in {target}"
                
                # For MVP, analyze the first file
                with open(code_files[0], 'r') as f:
                    code = f.read()
                target = code_files[0]
            else:
                return f"❌ Target not found: {target}"
            
            console.print(f"[blue]Analyzing: {target}[/blue]")
            
            # Execute code analysis
            result = self.engine.execute_with_tracking(
                self.code_analyzer,
                code=code,
                focus="all"
            )
            
            # Display analysis results
            console.print(Panel(f"""
[bold blue]Analysis:[/bold blue] {result.analysis}
[bold yellow]Issues:[/bold yellow] {result.issues}
[bold green]Recommendations:[/bold green] {result.recommendations}
[bold purple]Quality Score:[/bold purple] {result.score}
""", title=f"Code Analysis: {target}", border_style="blue"))
            
            # Save analysis result
            output = {
                "target": target,
                "level": level,
                "analysis": result.analysis,
                "issues": result.issues,
                "recommendations": result.recommendations,
                "score": result.score,
                "timestamp": str(console._get_time())
            }
            
            self._save_result(output, f"atlas_output/analysis_{Path(target).stem}.json")
            
            return f"✅ Analysis completed for {target}"
            
        except Exception as e:
            console.print(f"[red]❌ Error analyzing code: {e}[/red]")
            return f"❌ Code analysis failed: {e}"
    
    def refactor(self, target: str, level: str = "detailed") -> str:
        """Refactor code for improvement.
        
        Args:
            target: Path to code file to refactor
            level: Execution level (quick, detailed, premium)
            
        Returns:
            Success message with refactor details
        """
        self._display_status()
        
        if not self.engine.can_execute():
            return "❌ Daily budget exceeded. Cannot refactor code."
        
        try:
            if not os.path.exists(target):
                return f"❌ File not found: {target}"
            
            with open(target, 'r') as f:
                code = f.read()
            
            console.print(f"[blue]Refactoring: {target}[/blue]")
            
            # Execute refactoring
            result = self.engine.execute_with_tracking(
                self.code_refactorer,
                code=code,
                goals="readability, maintainability, performance"
            )
            
            # Display refactoring results
            console.print(Panel(f"[bold green]Refactored Code:[/bold green]\n{result.refactored_code}", 
                              title="Refactored Code", border_style="green"))
            
            console.print(f"[blue]Improvements:[/blue] {result.improvements}")
            console.print(f"[blue]Benefits:[/blue] {result.benefits}")
            
            # Save refactored code
            if self.yolo_mode or console.input(f"Apply refactoring to {target}? (y/N): ").lower().startswith('y'):
                # Backup original
                backup_path = f"{target}.refactor_backup"
                with open(backup_path, 'w') as f:
                    f.write(code)
                
                # Write refactored code
                with open(target, 'w') as f:
                    f.write(result.refactored_code)
                
                console.print(f"[green]✓ Refactoring applied to {target} (backup saved as {backup_path})[/green]")
            
            # Save result
            output = {
                "target": target,
                "level": level,
                "refactored_code": result.refactored_code,
                "improvements": result.improvements,
                "benefits": result.benefits,
                "timestamp": str(console._get_time())
            }
            
            self._save_result(output, f"atlas_output/refactor_{Path(target).stem}.json")
            
            return f"✅ Refactoring completed for {target}"
            
        except Exception as e:
            console.print(f"[red]❌ Error refactoring code: {e}[/red]")
            return f"❌ Refactoring failed: {e}"
    
    def project(self, description: str, level: str = "premium") -> str:
        """Generate complete project structure from description.
        
        Args:
            description: Description of the project to generate
            level: Execution level (quick, detailed, premium)
            
        Returns:
            Success message with project details
        """
        self._display_status()
        
        if not self.engine.can_execute():
            return "❌ Daily budget exceeded. Cannot generate project."
        
        try:
            console.print(f"[blue]Generating project: {description}[/blue]")
            
            # Use Program of Thought for complex project generation
            result = self.engine.execute_with_tracking(
                self.program_of_thought,
                task=f"Generate complete project structure for: {description}",
                requirements=description,
                language="Python"
            )
            
            if result['generated_code']:
                console.print(Panel(f"[bold green]Generated Project Code:[/bold green]\n{result['generated_code']['code']}", 
                                  title="Project Generation", border_style="green"))
                console.print(f"[blue]Structure:[/blue] {result['generated_code']['structure']}")
                console.print(f"[blue]Usage:[/blue] {result['generated_code']['usage_example']}")
            
            # Save project structure
            self._save_result(result, f"atlas_output/project_{description.replace(' ', '_')[:20]}.json")
            
            return f"✅ Project '{description}' generated successfully"
            
        except Exception as e:
            console.print(f"[red]❌ Error generating project: {e}[/red]")
            return f"❌ Project generation failed: {e}"