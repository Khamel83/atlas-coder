"""AtlasCoderEngine - Core model routing and cost tracking engine.

This module implements the core engine for Atlas Coder, providing model routing,
cost tracking, and DSPy configuration management with cost-optimized defaults.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import dspy
from pydantic import BaseModel


class CostTracker(BaseModel):
    """Track API costs and enforce daily budget limits."""

    daily_budget: float = 1.0  # $1/day default
    current_cost: float = 0.0
    last_reset: str = ""
    calls_made: int = 0

    def reset_if_new_day(self) -> None:
        """Reset cost tracking if it's a new day."""
        today = datetime.now().date().isoformat()
        if self.last_reset != today:
            self.current_cost = 0.0
            self.calls_made = 0
            self.last_reset = today

    def can_make_call(self, estimated_cost: float = 0.01) -> bool:
        """Check if we can make another API call within budget."""
        self.reset_if_new_day()
        return (self.current_cost + estimated_cost) <= self.daily_budget

    def add_cost(self, cost: float) -> None:
        """Add cost to the daily total."""
        self.reset_if_new_day()
        self.current_cost += cost
        self.calls_made += 1


class ModelConfig(BaseModel):
    """Model configuration with cost and performance settings."""

    name: str
    cost_per_million_tokens: float
    max_tokens: int
    supports_json: bool = True
    provider: str = "openrouter"


class AtlasCoderEngine:
    """Core engine for Atlas Coder with model routing and cost tracking.

    Provides cost-optimized model routing, primarily using Gemini 2.0 Flash Lite
    via OpenRouter for <$1/day operation.
    """

    DEFAULT_MODELS = {
        "cost-optimal": ModelConfig(
            name="google/gemini-2.0-flash-lite",
            cost_per_million_tokens=0.075,  # $0.075 per 1M tokens
            max_tokens=1048576,  # 1M tokens
            provider="openrouter",
        ),
        "quality-optimal": ModelConfig(
            name="google/gemini-2.0-flash-exp",
            cost_per_million_tokens=0.15,
            max_tokens=1048576,
            provider="openrouter",
        ),
        "local-fallback": ModelConfig(
            name="ollama_chat/llama3.2",
            cost_per_million_tokens=0.0,
            max_tokens=32768,
            provider="ollama",
        ),
    }

    def __init__(
        self,
        model_strategy: str = "cost-optimal",
        daily_budget: float = 1.0,
        cache_dir: str | None = None,
    ):
        """Initialize the AtlasCoderEngine.

        Args:
            model_strategy: Strategy for model selection (cost-optimal, quality-optimal, local-only)
            daily_budget: Daily budget limit in USD
            cache_dir: Directory for caching (defaults to ./dspy_cache)
        """
        self.model_strategy = model_strategy
        self.cache_dir = Path(cache_dir or "./dspy_cache")
        self.cache_dir.mkdir(exist_ok=True)

        # Initialize cost tracking
        self.cost_tracker = self._load_cost_tracker(daily_budget)

        # Configure DSPy settings
        self._configure_dspy()

        # Set up the model
        self.current_model = self._setup_model()

    def _load_cost_tracker(self, daily_budget: float) -> CostTracker:
        """Load or create cost tracker from cache."""
        cost_file = self.cache_dir / "cost_log.json"
        if cost_file.exists():
            try:
                with open(cost_file) as f:
                    data = json.load(f)
                tracker = CostTracker(**data)
                tracker.daily_budget = daily_budget  # Update budget if changed
                return tracker
            except Exception:
                pass

        return CostTracker(
            daily_budget=daily_budget, last_reset=datetime.now().date().isoformat()
        )

    def _save_cost_tracker(self) -> None:
        """Save cost tracker to cache."""
        cost_file = self.cache_dir / "cost_log.json"
        with open(cost_file, "w") as f:
            json.dump(self.cost_tracker.model_dump(), f, indent=2)

    def _configure_dspy(self) -> None:
        """Configure DSPy with caching and settings."""
        # Enable caching for cost optimization
        dspy.settings.configure(
            cache_turn_on=True, cache_db_path=str(self.cache_dir / "dspy_cache.db")
        )

    def _setup_model(self) -> dspy.LM:
        """Set up the DSPy language model based on strategy."""
        if self.model_strategy == "local-only":
            model_config = self.DEFAULT_MODELS["local-fallback"]
        elif self.model_strategy == "quality-optimal":
            model_config = self.DEFAULT_MODELS["quality-optimal"]
        else:  # cost-optimal (default)
            model_config = self.DEFAULT_MODELS["cost-optimal"]

        if model_config.provider == "openrouter":
            # Configure OpenRouter for Gemini access
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError(
                    "OPENROUTER_API_KEY environment variable required for cloud models"
                )

            model = dspy.LM(
                model=f"openrouter/{model_config.name}",
                api_key=api_key,
                max_tokens=8192,  # Reasonable output limit
                cache=True,
            )
        elif model_config.provider == "ollama":
            # Local Ollama fallback
            model = dspy.LM(
                model=model_config.name,
                api_base="http://localhost:11434",
                max_tokens=4096,
                cache=True,
            )
        else:
            raise ValueError(f"Unsupported provider: {model_config.provider}")

        dspy.configure(lm=model)
        return model

    def estimate_cost(self, input_tokens: int, output_tokens: int = 1000) -> float:
        """Estimate cost for a given number of tokens."""
        if self.model_strategy == "local-only":
            return 0.0

        strategy_key = (
            "quality-optimal"
            if self.model_strategy == "quality-optimal"
            else "cost-optimal"
        )
        model_config = self.DEFAULT_MODELS[strategy_key]

        total_tokens = input_tokens + output_tokens
        return (total_tokens / 1_000_000) * model_config.cost_per_million_tokens

    def can_execute(
        self, estimated_input_tokens: int = 2000, estimated_output_tokens: int = 1000
    ) -> bool:
        """Check if we can execute a call within budget."""
        estimated_cost = self.estimate_cost(
            estimated_input_tokens, estimated_output_tokens
        )
        return self.cost_tracker.can_make_call(estimated_cost)

    def record_usage(self, input_tokens: int, output_tokens: int) -> None:
        """Record actual usage and cost."""
        actual_cost = self.estimate_cost(input_tokens, output_tokens)
        self.cost_tracker.add_cost(actual_cost)
        self._save_cost_tracker()

    def get_status(self) -> dict[str, Any]:
        """Get current engine status and cost information."""
        self.cost_tracker.reset_if_new_day()
        return {
            "model_strategy": self.model_strategy,
            "current_model": getattr(self.current_model, "model", "Unknown"),
            "daily_budget": self.cost_tracker.daily_budget,
            "current_cost": self.cost_tracker.current_cost,
            "remaining_budget": self.cost_tracker.daily_budget
            - self.cost_tracker.current_cost,
            "calls_made": self.cost_tracker.calls_made,
            "can_make_calls": self.cost_tracker.can_make_call(),
            "last_reset": self.cost_tracker.last_reset,
        }

    def execute_with_tracking(self, dspy_module, **kwargs) -> Any:
        """Execute a DSPy module with cost tracking."""
        if not self.can_execute():
            raise RuntimeError(
                f"Daily budget of ${self.cost_tracker.daily_budget} exceeded. Current cost: ${self.cost_tracker.current_cost:.4f}"
            )

        try:
            # Execute the DSPy module
            result = dspy_module(**kwargs)

            # Record usage (approximate - real usage tracking would need API response parsing)
            # For now, record a conservative estimate
            self.record_usage(input_tokens=1000, output_tokens=500)

            return result
        except Exception as e:
            # Still record some cost for failed calls
            self.record_usage(input_tokens=500, output_tokens=0)
            raise e


def get_engine(
    model_strategy: str = "cost-optimal", daily_budget: float = 1.0
) -> AtlasCoderEngine:
    """Factory function to get a configured AtlasCoderEngine instance."""
    return AtlasCoderEngine(model_strategy=model_strategy, daily_budget=daily_budget)


def hello() -> str:
    """Returns a friendly greeting.

    Returns:
        A string containing the greeting.
    """
    return "Hello, Atlas Coder Engine!"
