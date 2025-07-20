"""Logging configuration for Atlas Coder.

This module provides centralized logging configuration with cost tracking,
performance monitoring, and error handling for Atlas Coder operations.
"""

import logging
import sys
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.logging import RichHandler


class AtlasCoderLogger:
    """Centralized logger for Atlas Coder with cost and performance tracking."""

    def __init__(
        self,
        name: str = "atlas_coder",
        level: str = "INFO",
        log_file: str | None = None,
        use_rich: bool = True,
    ):
        """Initialize the Atlas Coder logger.

        Args:
            name: Logger name
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional log file path
            use_rich: Use Rich formatting for console output
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))

        # Clear existing handlers
        self.logger.handlers.clear()

        # Console handler
        if use_rich:
            console = Console()
            console_handler = RichHandler(
                console=console, rich_tracebacks=True, show_time=True, show_path=False
            )
        else:
            console_handler = logging.StreamHandler(sys.stdout)

        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler (optional)
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_path)
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message with optional context."""
        self._log_with_context(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message with optional context."""
        self._log_with_context(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message with optional context."""
        self._log_with_context(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message with optional context."""
        self._log_with_context(logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message with optional context."""
        self._log_with_context(logging.CRITICAL, message, **kwargs)

    def log_cost(self, operation: str, cost: float, tokens: int = 0) -> None:
        """Log cost information for API operations."""
        self.info(
            f"💰 Cost tracking: {operation}",
            cost=cost,
            tokens=tokens,
            operation=operation,
        )

    def log_performance(self, operation: str, duration: float) -> None:
        """Log performance information for operations."""
        self.info(
            f"⚡ Performance: {operation} completed in {duration:.2f}s",
            duration=duration,
            operation=operation,
        )

    def log_api_call(
        self, model: str, input_tokens: int, output_tokens: int, cost: float
    ) -> None:
        """Log API call details."""
        self.info(
            f"🤖 API call: {model}",
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
        )

    def _log_with_context(self, level: int, message: str, **kwargs: Any) -> None:
        """Internal method to log with additional context."""
        if kwargs:
            context = " | ".join(f"{k}={v}" for k, v in kwargs.items())
            full_message = f"{message} | {context}"
        else:
            full_message = message

        self.logger.log(level, full_message)


# Global logger instance
_logger_instance: AtlasCoderLogger | None = None


def get_logger(
    name: str = "atlas_coder",
    level: str = "INFO",
    log_file: str | None = None,
    use_rich: bool = True,
) -> AtlasCoderLogger:
    """Get or create Atlas Coder logger instance."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = AtlasCoderLogger(
            name=name, level=level, log_file=log_file, use_rich=use_rich
        )
    return _logger_instance


def setup_logging(config: dict[str, Any]) -> AtlasCoderLogger:
    """Setup logging from configuration."""
    return get_logger(
        level=config.get("level", "INFO"),
        log_file=config.get("file"),
        use_rich=config.get("use_rich", True),
    )
