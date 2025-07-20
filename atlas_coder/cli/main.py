"""Main CLI entry point.

This module is part of the Atlas Coder professional DSPy framework.
Implements main cli entry point functionality with proper documentation
following PEP 257 and Google Python Style Guide.
"""

import click
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

# Import Atlas Coder modules
try:
    from atlas_coder.utils.config import configure_dspy_lm
    from atlas_coder.core.workflows import WorkflowOrchestrator
    # from atlas_coder.git import AtlasGitManager, GitResult # Will be uncommented later
    # from atlas_coder.core import AtlasCoderEngine # Will be uncommented later
    # from atlas_coder.cost import CostTracker, ProgressiveExecutionEngine # Will be uncommented later
    # from atlas_coder.ai import ConversationProcessor # Will be uncommented later
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(" Run: pip install -e . to install Atlas Coder in development mode")
    sys.exit(1)

# Rich console for beautiful output
console = Console()

# Version
__version__ = "1.0.0"

@click.group()
@click.option('--yolo', is_flag=True, help='Enable YOLO mode (no interactive confirmations for file writes/commits).')
@click.pass_context
def cli(ctx, yolo):
    """Atlas Coder CLI for DSPy-powered systematic programming."""
    ctx.ensure_object(dict)
    ctx.obj['YOLO_MODE'] = yolo
    if yolo:
        console.print(Panel("[bold yellow]YOLO Mode Enabled:[/bold yellow] Automatic confirmations for file writes and commits.", title="[bold red]Warning[/bold red]", border_style="red"))
        if not Confirm.ask("[bold red]Are you absolutely sure you want to proceed in YOLO mode?[/bold red]", default=False):
            console.print("[bold red]YOLO mode cancelled. Exiting.[/bold red]")
            sys.exit(1)
    
    try:
        configure_dspy_lm()
        console.print("[green]DSPy Language Model configured successfully.[/green]")
    except ValueError as e:
        console.print(f"[bold red]Error configuring DSPy Language Model:[/bold red] {e}")
        console.print("[yellow]Please ensure OPENROUTER_API_KEY is set in your .env file.[/yellow]")
        sys.exit(1)

@cli.command()
def version():
    """Show the Atlas Coder version."""
    console.print(f"Atlas Coder Version: [bold green]{__version__}[/bold green]")

@cli.command()
@click.pass_context
def status(ctx):
    """Display the current status of the Atlas Coder environment."""
    console.print(Panel("[bold blue]Atlas Coder Status[/bold blue]", expand=False))
    console.print(f"YOLO Mode: [bold]{ctx.obj['YOLO_MODE']}[/bold]")
    console.print(f"DSPy LM Configured: [green]Yes[/green]")
    # Placeholder for more detailed status checks later
    console.print("[yellow]More detailed status checks will be implemented here.[/yellow]")

# Workflow commands
@cli.command()
@click.argument('requirements')
@click.option('--level', default='detailed', type=click.Choice(['quick', 'detailed', 'premium']), help='Execution level.')
@click.option('--model-strategy', default='balanced', type=click.Choice(['cost-optimal', 'quality-optimal', 'balanced', 'local-only']), help='Model strategy.')
@click.pass_context
def generate(ctx, requirements, level, model_strategy):
    """Generate new code based on requirements."""
    orchestrator = WorkflowOrchestrator()
    result = orchestrator.generate(requirements, level, model_strategy)
    console.print(f"[green]{result}[/green]")

@cli.command(name="fix-bug")
@click.argument('code_file')
@click.argument('error_message')
@click.option('--level', default='detailed', type=click.Choice(['quick', 'detailed', 'premium']), help='Execution level.')
@click.pass_context
def fix_bug_cmd(ctx, code_file, error_message, level):
    """Systematically diagnose and fix bugs in your code."""
    orchestrator = WorkflowOrchestrator()
    result = orchestrator.fix_bug(code_file, error_message, level)
    console.print(f"[green]{result}[/green]")

@cli.command()
@click.argument('target')
@click.option('--level', default='quick', type=click.Choice(['quick', 'detailed', 'premium']), help='Execution level.')
@click.pass_context
def analyze(ctx, target, level):
    """Perform deep quality and security analysis on your codebase."""
    orchestrator = WorkflowOrchestrator()
    result = orchestrator.analyze(target, level)
    console.print(f"[green]{result}[/green]")

@cli.command()
@click.argument('description')
@click.option('--level', default='premium', type=click.Choice(['quick', 'detailed', 'premium']), help='Execution level.')
@click.pass_context
def project(ctx, description, level):
    """Generate complete project structures from high-level descriptions."""
    orchestrator = WorkflowOrchestrator()
    result = orchestrator.project(description, level)
    console.print(f"[green]{result}[/green]")

@cli.command()
@click.argument('target')
@click.option('--level', default='detailed', type=click.Choice(['quick', 'detailed', 'premium']), help='Execution level.')
@click.pass_context
def refactor(ctx, target, level):
    """Get intelligent suggestions for refactoring and improving your code."""
    orchestrator = WorkflowOrchestrator()
    result = orchestrator.refactor(target, level)
    console.print(f"[green]{result}[/green]")

# Placeholder for other commands
@cli.command(name="process-conversation")
def process_conversation_cmd():
    """Process natural language conversation into structured tasks."""
    console.print("[yellow]This command is a placeholder and will be implemented soon.[/yellow]")

@cli.command()
def develop():
    """Execute systematic development workflows."""
    console.print("[yellow]This command is a placeholder and will be implemented soon.[/yellow]")

@cli.command(name="cost-report")
def cost_report_cmd():
    """Show cost analysis and reports."""
    console.print("[yellow]This command is a placeholder and will be implemented soon.[/yellow]")

@cli.group()
def git():
    """Git integration commands."""
    pass

@git.command()
def setup():
    """Setup Git repository with professional workflows."""
    console.print("[yellow]This command is a placeholder and will be implemented soon.[/yellow]")

@git.command()
def commit():
    """Commit development progress."""
    console.print("[yellow]This command is a placeholder and will be implemented soon.[/yellow]")

@git.command()
def push():
    """Push to GitHub."""
    console.print("[yellow]This command is a placeholder and will be implemented soon.[/yellow]")

if __name__ == '__main__':
    cli(obj={})
