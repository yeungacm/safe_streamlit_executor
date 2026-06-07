"""
Security module for AST-based code analysis and import whitelisting.
"""

import ast
from typing import List, Set, Optional


class CodeSecurityChecker:
    """AST-based security checker for Python code."""

    # Default allowed modules whitelist
    DEFAULT_ALLOWED_MODULES: Set[str] = {
        # Data analysis and scientific computing
        'numpy', 'pandas', 'scipy', 'sklearn',
        # Chart plotting
        'matplotlib', 'seaborn', 'plotly',
        # Mathematics and statistics
        'math', 'statistics', 'random', 'cmath', 'decimal', 'fractions',
        # Time and file paths (read-only)
        'datetime', 'dateutil', 'time',
        'pathlib', 'os.path',  # Only allow os.path, not os
        # Text processing and serialization
        'json', 'csv', 're', 'string', 'collections', 'itertools', 'functools',
        'typing', 'hashlib', 'base64',
        # Image processing
        'PIL', 'cv2',
        # Streamlit
        'streamlit',
        # Other common tools
        'copy', 'pprint', 'textwrap', 'unicodedata',
        'io',  # Allow io objects, but actual file operations are still blocked
        'sympy',  # For symbolic calculations if needed
    }

    # Dangerous functions that should be blocked
    DANGEROUS_FUNCTIONS: Set[str] = {
        'eval', 'exec', 'open', 'compile', '__import_sys__', 'input',
        'globals', 'locals', 'vars', 'dir',
        'getattr', 'setattr', 'delattr',
        '__builtins__'
    }

    def __init__(self, allowed_modules: Optional[Set[str]] = None):
        """
        Initialize the security checker.

        Args:
            allowed_modules: Optional set of allowed module names. 
                           If None, uses DEFAULT_ALLOWED_MODULES.
        """
        self.allowed_modules = allowed_modules or self.DEFAULT_ALLOWED_MODULES
        self.warnings: List[str] = []

    def check_code(self, code: str) -> List[str]:
        """
        Check Python code for security issues.

        Args:
            code: Python code string to check

        Returns:
            List of warning messages (empty if no issues found)
        """
        self.warnings = []

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return [f"Syntax error: {e}"]

        visitor = self._create_visitor()
        visitor.visit(tree)

        return self.warnings

    def _create_visitor(self) -> ast.NodeVisitor:
        """Create an AST visitor for security checking."""
        checker = self

        class SecurityVisitor(ast.NodeVisitor):
            """AST visitor that marks unauthorized modules and dangerous statements."""

            def visit_Import(self, node):
                for alias in node.names:
                    mod_name = alias.name
                    if not checker._is_module_allowed(mod_name):
                        checker.warnings.append(f"Import not allowed: {mod_name}")
                self.generic_visit(node)

            def visit_ImportFrom(self, node):
                if node.module is not None:
                    if not checker._is_module_allowed(node.module):
                        checker.warnings.append(f"Import from module not allowed: {node.module}")
                self.generic_visit(node)

            def visit_Call(self, node):
                # Check direct calls to dangerous functions
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                    if name in checker.DANGEROUS_FUNCTIONS:
                        checker.warnings.append(f"Dangerous function call: {name}()")
                # Check dangerous calls through objects (e.g., obj.__class__)
                elif isinstance(node.func, ast.Attribute):
                    attr_name = node.func.attr
                    if attr_name.startswith('__') and attr_name.endswith('__'):
                        checker.warnings.append(f"Use of special attribute: .{attr_name}")
                self.generic_visit(node)

            def visit_Attribute(self, node):
                # Double-check any attribute access
                if isinstance(node.attr, str) and node.attr.startswith('__') and node.attr.endswith('__'):
                    checker.warnings.append(f"Access to special attribute: .{node.attr}")
                self.generic_visit(node)

        return SecurityVisitor()

    def _is_module_allowed(self, full_name: str) -> bool:
        """
        Check if a module name is allowed.

        Args:
            full_name: Full module name (e.g., 'numpy.linalg')

        Returns:
            True if the module is allowed, False otherwise
        """
        # Direct match
        if full_name in self.allowed_modules:
            return True

        # Allow submodules: if the top-level package is in the whitelist
        top_pkg = full_name.split('.')[0]
        if top_pkg in self.allowed_modules:
            return True

        # Special allowance for 'os.path'
        if full_name == 'os.path':
            return True

        return False

    def add_allowed_module(self, module_name: str) -> None:
        """Add a module to the allowed modules whitelist."""
        self.allowed_modules.add(module_name)

    def remove_allowed_module(self, module_name: str) -> None:
        """Remove a module from the allowed modules whitelist."""
        self.allowed_modules.discard(module_name)
