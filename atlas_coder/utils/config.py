"""Configuration management.

This module is part of the Atlas Coder professional DSPy framework.
Implements configuration management functionality with proper documentation
following PEP 257 and Google Python Style Guide.
"""

import os
import dspy
from dotenv import load_dotenv

def configure_dspy_lm():
    """Configures the DSPy language model using OPENROUTER_API_KEY from .env."""
    load_dotenv()
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

    if not openrouter_api_key:
        raise ValueError("OPENROUTER_API_KEY not found in .env. Please set it.")

    dspy.configure(lm=dspy.OpenAI(model="openrouter/auto", api_key=openrouter_api_key))