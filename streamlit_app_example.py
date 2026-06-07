"""
Example Streamlit app using the safe_python_executor library.
"""

def main():
    import streamlit as st
    from safe_streamlit_executor import SafePythonExecutor
    st.title("🔒 Safe Streamlit Code Executor")
    st.markdown("Using the `safe_streamlit_executor` library")

    # Initialize the executor
    executor = SafePythonExecutor()

    # Optional: Add custom allowed modules
    # executor.add_allowed_module('custom_module')

    # Code input
    code = st.text_area(
        "Enter Python code (can use import streamlit, numpy, etc.):",
        height=200,
        placeholder="print('Hello, World!')\nimport numpy as np\narr = np.array([1, 2, 3])\nprint(arr)"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Execute Safely", type="primary"):
            if code.strip():
                with st.spinner("Executing code..."):
                    output, error = executor.execute(code)

                    if output is not None:
                        st.success("✅ Execution successful!")
                        st.code(output)

                    if error is not None:
                        st.error(f"❌ Error: {error}")
            else:
                st.warning("Please enter some code to execute.")

    with col2:
        if st.button("🔍 Security Check Only"):
            if code.strip():
                warnings = executor.security_checker.check_code(code)
                if warnings:
                    st.warning("⚠️ Security warnings found:")
                    for warning in warnings:
                        st.write(f"- {warning}")
                else:
                    st.success("✅ No security issues found!")
            else:
                st.warning("Please enter some code to check.")

    # Show allowed modules
    with st.expander("📋 Allowed Modules"):
        st.write("The following modules are allowed for import:")
        allowed_modules = sorted(executor.security_checker.allowed_modules)
        st.write(", ".join(allowed_modules))


if __name__ == "__main__":
    main()
