"""
Utility functions for the safe Python executor library.
"""

from typing import Optional, Set


def create_executor_with_custom_modules(
    additional_modules: Optional[Set[str]] = None,
    remove_modules: Optional[Set[str]] = None
):
    """
    Create a SafePythonExecutor with custom module configuration.

    Args:
        additional_modules: Set of additional modules to allow
        remove_modules: Set of modules to remove from default whitelist

    Returns:
        Configured SafePythonExecutor instance
    """
    from .executor import SafePythonExecutor
    from .security import CodeSecurityChecker

    # Start with default modules
    allowed_modules = CodeSecurityChecker.DEFAULT_ALLOWED_MODULES.copy()

    # Add additional modules
    if additional_modules:
        allowed_modules.update(additional_modules)

    # Remove specified modules
    if remove_modules:
        allowed_modules.difference_update(remove_modules)

    return SafePythonExecutor(allowed_modules=allowed_modules)


def quick_execute(code: str) -> tuple:
    """
    Quick execution function for simple use cases.

    Args:
        code: Python code string to execute

    Returns:
        Tuple of (output, error)
    """
    from .executor import SafePythonExecutor

    executor = SafePythonExecutor()
    return executor.execute(code)
