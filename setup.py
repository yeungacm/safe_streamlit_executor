"""
Setup file for the safe_python_executor library.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="safe-python-executor",
    version="1.0.0",
    author="Yeung",
    author_email="yeung.acm@gmail.com",
    description="A reusable library for safely executing Streamlit-based Python code with RestrictedPython and AST security checks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yeungacm/safe-python-executor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.8",
    install_requires=[
        "RestrictedPython>=5.0",
        "streamlit>=1.0.0",
    ],
)
