"""
Main executor module for safe Python code execution.
"""

import sys
import builtins
from io import StringIO
from typing import Tuple, Optional, Dict, Any, Set

from RestrictedPython import compile_restricted
from RestrictedPython.Guards import (
    guarded_iter_unpack_sequence,
    guarded_unpack_sequence,
    safe_builtins
)

from .security import CodeSecurityChecker
from .guards import SafeGuards


class SafePythonExecutor:
    """
    Safe Python code executor with RestrictedPython and AST security checks.
    """

    def __init__(self, allowed_modules: Optional[Set[str]] = None):
        """
        Initialize the safe executor.

        Args:
            allowed_modules: Optional set of allowed module names
        """
        self.security_checker = CodeSecurityChecker(allowed_modules)
        self.guards = SafeGuards()
        self._real_import = builtins.__import__

    def safe_import(self, name: str, globals=None, locals=None, fromlist=(), level=0):
        """
        Safe import function that only allows whitelisted modules.

        Args:
            name: Module name to import
            globals: Global namespace
            locals: Local namespace
            fromlist: List of names to import from module
            level: Relative import level

        Returns:
            Imported module

        Raises:
            ImportError: If module is not allowed
        """
        if name:
            # Check if module is allowed
            if not self.security_checker._is_module_allowed(name):
                raise ImportError(f"Import not allowed: {name}")

        # Call the real __import__
        return self._real_import(name, globals, locals, fromlist, level)

    def _create_safe_globals(self) -> Dict[str, Any]:
        """
        Create a safe globals dictionary for RestrictedPython execution.

        Returns:
            Dictionary with safe builtins and guard functions
        """
        safe_globals_dict = {
            '__builtins__': {
                # Basic functions
                'print': print,
                'len': len,
                'range': range,
                'int': int,
                'float': float,
                'str': str,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'bool': bool,
                'True': True,
                'False': False,
                'None': None,

                # Mathematical operations
                'abs': abs,
                'max': max,
                'min': min,
                'sum': sum,
                'round': round,
                'pow': pow,
                'divmod': divmod,
                'hex': hex,
                'oct': oct,
                'bin': bin,
                'ord': ord,
                'chr': chr,

                # Iterable operations
                'sorted': sorted,
                'reversed': reversed,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
                'any': any,
                'all': all,

                # Type operations
                'isinstance': isinstance,
                'type': type,

                # Safe import (replaces built-in __import__)
                '__import__': self.safe_import,
            },

            # RestrictedPython guard functions
            '_getattr_': getattr,
            '_setattr_': setattr,
            '_delattr_': delattr,
            '_getiter_': self.guards.safe_getiter,
            '_getitem_': self.guards.safe_getitem,
            '_setitem_': self.guards.safe_setitem,
            '_delitem_': self.guards.safe_delitem,
            '_unpack_sequence_': guarded_unpack_sequence,
            '_iter_unpack_sequence_': guarded_iter_unpack_sequence,
        }

        return safe_globals_dict

    def execute(self, code: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Execute Python code safely.

        Args:
            code: Python code string to execute

        Returns:
            Tuple of (output, error) where:
            - output: Captured stdout output if successful, None otherwise
            - error: Error message if failed, None if successful
        """
        # Step 1: AST security check
        warnings = self.security_checker.check_code(code)
        if warnings:
            warning_msg = "\n".join(f"- {w}" for w in warnings)
            return None, f"Security check found potential risks:\n{warning_msg}"

        # Step 2: Create safe globals
        safe_globals_dict = self._create_safe_globals()

        try:
            # Step 3: Compile with RestrictedPython
            byte_code = compile_restricted(code, '<string>', 'exec')

            # Step 4: Capture stdout
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()

            # Step 5: Execute
            exec(byte_code, safe_globals_dict)

            sys.stdout = old_stdout
            return captured_output.getvalue(), None

        except Exception as e:
            sys.stdout = old_stdout
            return None, str(e)

    def add_allowed_module(self, module_name: str) -> None:
        """Add a module to the allowed modules whitelist."""
        self.security_checker.add_allowed_module(module_name)

    def remove_allowed_module(self, module_name: str) -> None:
        """Remove a module from the allowed modules whitelist."""
        self.security_checker.remove_allowed_module(module_name)
