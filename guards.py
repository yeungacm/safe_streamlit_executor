"""
Guard functions for RestrictedPython safe execution.
"""

from typing import Any, Iterator


class SafeGuards:
    """Collection of safe guard functions for RestrictedPython."""

    @staticmethod
    def safe_getiter(ob: Any) -> Iterator:
        """
        Safe iterator acquisition function.

        Args:
            ob: Object to get iterator from

        Returns:
            Iterator for the object

        Raises:
            TypeError: If object is not iterable
        """
        if hasattr(ob, '__iter__'):
            return iter(ob)
        elif hasattr(ob, '__getitem__'):
            # Create a safe iterator for indexable objects
            class SafeIndexIterator:
                def __init__(self, obj):
                    self.obj = obj
                    self.index = 0

                def __iter__(self):
                    return self

                def __next__(self):
                    try:
                        result = self.obj[self.index]
                        self.index += 1
                        return result
                    except (IndexError, KeyError):
                        raise StopIteration

            return SafeIndexIterator(ob)
        else:
            raise TypeError(f"'{type(ob).__name__}' object is not iterable")

    @staticmethod
    def safe_getitem(ob: Any, index: Any) -> Any:
        """
        Safe index access function.

        Args:
            ob: Object to access
            index: Index to access

        Returns:
            Value at the specified index

        Raises:
            KeyError: If trying to access special attributes
        """
        # Prevent accessing dangerous internal attributes through __getitem__
        if isinstance(index, str) and index.startswith('__') and index.endswith('__'):
            raise KeyError(f"Access to special attribute '{index}' is not allowed")
        return ob[index]

    @staticmethod
    def safe_setitem(ob: Any, index: Any, value: Any) -> None:
        """
        Safe index setting function.

        Args:
            ob: Object to modify
            index: Index to set
            value: Value to set

        Raises:
            KeyError: If trying to modify special attributes
        """
        # Prevent modifying dangerous internal attributes through __setitem__
        if isinstance(index, str) and index.startswith('__') and index.endswith('__'):
            raise KeyError(f"Modification of special attribute '{index}' is not allowed")
        ob[index] = value

    @staticmethod
    def safe_delitem(ob: Any, index: Any) -> None:
        """
        Safe index deletion function.

        Args:
            ob: Object to modify
            index: Index to delete

        Raises:
            KeyError: If trying to delete special attributes
        """
        # Prevent deleting dangerous internal attributes through __delitem__
        if isinstance(index, str) and index.startswith('__') and index.endswith('__'):
            raise KeyError(f"Deletion of special attribute '{index}' is not allowed")
        del ob[index]
