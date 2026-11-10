#!/usr/bin/env python3
"""
Setup script for SDLC Expert Agent
"""

from setuptools import setup, find_packages

setup(
    name="sdlc_expert_agent",
    version="1.0.0",
    description="A conversational SDLC expert agent that converts PRD text to test cases",
    author="SDLC Expert Team",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "rich>=13.0.0",
        "textual>=0.1.0", 
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "sdlc-agent = src.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
)
