# Safe Python Streamlit Executor with Streamlit library

A reusable Python library for safely executing Streamlit-based Python code with RestrictedPython and AST security checks.

## Features

- 🔒 **AST-based security checking**: Analyzes code before execution for dangerous patterns
- 🚫 **Import whitelisting**: Only allows approved modules to be imported
- 🛡️ **RestrictedPython integration**: Uses RestrictedPython for runtime protection
- 🔧 **Customizable**: Easy to add or remove allowed modules
- 📦 **Reusable**: Can be used in any Python application, especially Streamlit apps

## Installation
	bash pip install safe_streamlit_executor

Or install from source:

	bash git clone https://github.com/yeungacm/safe_streamlit_executor.git 
	cd safe_streamlit_executor 
	pip install -e .

## Quick Start

python

	from safe_streamlit_executor import SafePythonExecutor
	#Create executor
	executor = SafePythonExecutor()
	#Execute code safely
	code = """
	import numpy as np
	arr = np.array([1, 2, 3])
	print(f"Array: {arr}")
	print(f"Sum: {np.sum(arr)}")
		"""
	output, error = executor.execute(code)
	if output:
		print("Output:", output)
	if error:
		print("Error:", error)

## Usage with Streamlit

python

	import streamlit as st
	from safe_streamlit_executor import SafePythonExecutor
	executor = SafePythonExecutor()
	code = st.text_area("Enter Python code:")
	if st.button("Execute"):
		output, error = executor.execute(code) 
	if output:
		st.code(output) 
	if error:
		st.error(error)

## Customization

python

Add custom allowed modules

	executor.add_allowed_module('my_custom_module')

Remove modules from whitelist

	executor.remove_allowed_module('os.path')

Create executor with custom module list

	from safe_streamlit_executor.utils import create_executor_with_custom_modules
	executor = create_executor_with_custom_modules( additional_modules={'my_module'}, remove_modules={'PIL'} )

## Security Features

- Blocks dangerous functions: `eval`, `exec`, `open`, `compile`, etc.
- Prevents access to special attributes (`__class__`, `__dict__`, etc.)
- Restricts imports to whitelisted modules only
- Uses RestrictedPython for runtime protection
- AST-based static analysis before execution

## License

MIT License

Usage Example:

	streamlit_app_example.py

Any Streamlit program can now use this library like this:

	import streamlit as st
	from safe_streamlit_executor import SafePythonExecutor

# Create executor instance
executor = SafePythonExecutor()

# Use in your Streamlit app

	code = st.text_area("Enter code:")
	if st.button("Run"):
    output, error = executor.execute(code)
    if output:
        st.success(output)
    if error:
        st.error(error)

This library provides a clean, reusable interface for safe Python code execution that can be easily integrated into any Streamlit application or other Python project.
