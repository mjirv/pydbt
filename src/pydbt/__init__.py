"""
PyDBT: Python-based helper for dbt projects using Ibis
"""

from .core import run_all_models
from .config import ConnectionConfig
from .testing import TestCase, ModelTester

__version__ = "0.1.0"

# Public API exports
__all__ = [
    "ConnectionConfig",  # For custom connection configuration
    "TestCase",         # For writing model tests
    "ModelTester",      # For programmatic test execution
    "run_all_models",   # Core functionality for SQL generation
]