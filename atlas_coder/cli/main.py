"""Main CLI entry point for Atlas Coder.

This module implements the main CLI interface for Atlas Coder, providing
cost-optimized DSPy-powered coding workflows.
"""

import os
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

# Import Atlas Coder modules
try:
    from atlas_coder.core.engine import AtlasCoderEngine
    from atlas_coder.core.workflows import WorkflowOrchestrator
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Run: pip install -e . to install Atlas Coder in development mode")
    sys.exit(1)

# Rich console for beautiful output
console = Console()

# Version
__version__ = "1.0.0"


@click.group()
@click.option(
    "--yolo",
    is_flag=True,
    help="Enable YOLO mode (no interactive confirmations for file writes/commits).",
)
@click.option(
    "--model-strategy",
    default="cost-optimal",
    type=click.Choice(["cost-optimal", "quality-optimal", "local-only"]),
    help="Model strategy for cost/quality optimization.",
)
@click.option("--budget", default=1.0, help="Daily budget limit in USD.")
@click.pass_context
def cli(ctx, yolo, model_strategy, budget):
    """Atlas Coder CLI for DSPy-powered systematic programming.

    Cost-optimized LLM workflows using Gemini 2.0 Flash Lite via OpenRouter.
    """
    ctx.ensure_object(dict)
    ctx.obj["YOLO_MODE"] = yolo
    ctx.obj["MODEL_STRATEGY"] = model_strategy
    ctx.obj["BUDGET"] = budget

    if yolo:
        console.print(
            Panel(
                "[bold yellow]YOLO Mode Enabled:[/bold yellow] Automatic confirmations for file writes and commits.",
                title="[bold red]Warning[/bold red]",
                border_style="red",
            )
        )
        if not Confirm.ask(
            "[bold red]Are you absolutely sure you want to proceed in YOLO mode?[/bold red]",
            default=False,
        ):
            console.print("[bold red]YOLO mode cancelled. Exiting.[/bold red]")
            sys.exit(1)

    # Validate environment
    if model_strategy != "local-only" and not os.getenv("OPENROUTER_API_KEY"):
        console.print(
            "[bold red]Error:[/bold red] OPENROUTER_API_KEY environment variable required for cloud models"
        )
        console.print(
            "[yellow]Set OPENROUTER_API_KEY in your environment or use --model-strategy local-only[/yellow]"
        )
        sys.exit(1)


@cli.command()
def version():
    """Show the Atlas Coder version."""
    console.print(f"Atlas Coder Version: [bold green]{__version__}[/bold green]")


@cli.command()
@click.pass_context
def status(ctx):
    """Display the current status of Atlas Coder."""
    try:
        engine = AtlasCoderEngine(
            model_strategy=ctx.obj["MODEL_STRATEGY"], daily_budget=ctx.obj["BUDGET"]
        )
        status = engine.get_status()

        console.print(
            Panel(
                f"""
[bold blue]Atlas Coder Status[/bold blue]
Version: {__version__}
Model Strategy: {status['model_strategy']}
Current Model: {status['current_model']}
Daily Budget: ${status['daily_budget']:.2f}
Current Cost: ${status['current_cost']:.4f}
Remaining: ${status['remaining_budget']:.4f}
Calls Made: {status['calls_made']}
Can Make Calls: {status['can_make_calls']}
YOLO Mode: {ctx.obj['YOLO_MODE']}
""",
                border_style="blue",
            )
        )

    except Exception as e:
        console.print(f"[red]❌ Error getting status: {e}[/red]")


# Core workflow commands
@cli.command()
@click.argument("requirements")
@click.option(
    "--level",
    default="detailed",
    type=click.Choice(["quick", "detailed", "premium"]),
    help="Execution level.",
)
@click.option("--language", default="Python", help="Programming language.")
@click.pass_context
def generate(ctx, requirements, level, language):
    """Generate new code based on requirements.

    Examples:
      atlas-coder generate "REST API with user authentication"
      atlas-coder generate "binary search algorithm" --level quick
    """
    try:
        orchestrator = WorkflowOrchestrator(
            model_strategy=ctx.obj["MODEL_STRATEGY"],
            daily_budget=ctx.obj["BUDGET"],
            yolo_mode=ctx.obj["YOLO_MODE"],
        )
        result = orchestrator.generate(requirements, level, ctx.obj["MODEL_STRATEGY"])
        console.print(result)

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@cli.command(name="fix-bug")
@click.argument("code_file", type=click.Path(exists=True))
@click.option("--error", default="", help="Error message or description.")
@click.option(
    "--level",
    default="detailed",
    type=click.Choice(["quick", "detailed", "premium"]),
    help="Execution level.",
)
@click.pass_context
def fix_bug_cmd(ctx, code_file, error, level):
    """Systematically diagnose and fix bugs in your code.

    Examples:
      atlas-coder fix-bug buggy_script.py --error "IndexError on line 42"
      atlas-coder fix-bug app.py --yolo
    """
    try:
        orchestrator = WorkflowOrchestrator(
            model_strategy=ctx.obj["MODEL_STRATEGY"],
            daily_budget=ctx.obj["BUDGET"],
            yolo_mode=ctx.obj["YOLO_MODE"],
        )
        result = orchestrator.fix_bug(code_file, error, level)
        console.print(result)

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@cli.command()
@click.argument("target", type=click.Path(exists=True))
@click.option(
    "--level",
    default="detailed",
    type=click.Choice(["quick", "detailed", "premium"]),
    help="Execution level.",
)
@click.option(
    "--focus",
    default="all",
    type=click.Choice(["security", "performance", "style", "all"]),
    help="Analysis focus area.",
)
@click.pass_context
def analyze(ctx, target, level, focus):
    """Perform deep quality and security analysis on your codebase.

    Examples:
      atlas-coder analyze myproject/ --focus security
      atlas-coder analyze script.py --level premium
    """
    try:
        orchestrator = WorkflowOrchestrator(
            model_strategy=ctx.obj["MODEL_STRATEGY"],
            daily_budget=ctx.obj["BUDGET"],
            yolo_mode=ctx.obj["YOLO_MODE"],
        )
        result = orchestrator.analyze(target, level)
        console.print(result)

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@cli.command()
@click.argument("target", type=click.Path(exists=True))
@click.option(
    "--level",
    default="detailed",
    type=click.Choice(["quick", "detailed", "premium"]),
    help="Execution level.",
)
@click.pass_context
def refactor(ctx, target, level):
    """Get intelligent suggestions for refactoring and improving your code.

    Examples:
      atlas-coder refactor legacy_code.py
      atlas-coder refactor module.py --level premium --yolo
    """
    try:
        orchestrator = WorkflowOrchestrator(
            model_strategy=ctx.obj["MODEL_STRATEGY"],
            daily_budget=ctx.obj["BUDGET"],
            yolo_mode=ctx.obj["YOLO_MODE"],
        )
        result = orchestrator.refactor(target, level)
        console.print(result)

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@cli.command()
@click.argument("description")
@click.option(
    "--level",
    default="premium",
    type=click.Choice(["quick", "detailed", "premium"]),
    help="Execution level.",
)
@click.pass_context
def project(ctx, description, level):
    """Generate complete project structures from high-level descriptions.

    Examples:
      atlas-coder project "Flask web app with user auth and database"
      atlas-coder project "CLI tool for file processing" --level detailed
    """
    try:
        orchestrator = WorkflowOrchestrator(
            model_strategy=ctx.obj["MODEL_STRATEGY"],
            daily_budget=ctx.obj["BUDGET"],
            yolo_mode=ctx.obj["YOLO_MODE"],
        )
        result = orchestrator.project(description, level)
        console.print(result)

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


# Utility commands
@cli.command(name="cost-report")
@click.pass_context
def cost_report_cmd(ctx):
    """Show detailed cost analysis and usage reports."""
    try:
        engine = AtlasCoderEngine(
            model_strategy=ctx.obj["MODEL_STRATEGY"], daily_budget=ctx.obj["BUDGET"]
        )
        status = engine.get_status()

        console.print(
            Panel(
                f"""
[bold blue]Cost Report[/bold blue]
Daily Budget: ${status['daily_budget']:.2f}
Current Cost: ${status['current_cost']:.4f}
Percentage Used: {(status['current_cost'] / status['daily_budget'] * 100):.1f}%
Remaining Budget: ${status['remaining_budget']:.4f}
Total Calls Made: {status['calls_made']}
Average Cost per Call: ${(status['current_cost'] / max(status['calls_made'], 1)):.4f}
Last Reset: {status['last_reset']}
Status: {'🟢 Within Budget' if status['can_make_calls'] else '🔴 Budget Exceeded'}
""",
                title="Cost Analysis",
                border_style="green" if status["can_make_calls"] else "red",
            )
        )

    except Exception as e:
        console.print(f"[red]❌ Error generating cost report: {e}[/red]")


# Git integration placeholder
@cli.group()
def git():
    """Git integration commands (future implementation)."""
    pass


@git.command()
def setup():
    """Setup Git repository with professional workflows."""
    console.print("[yellow]Git integration coming soon![/yellow]")


def main():
    """Entry point for the atlas-coder CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
