#!/usr/bin/env python
"""
Script to run the CISSP Tutor & Exam Platform Streamlit application.
"""
import os
import subprocess
import sys

# Ensure we're in the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_root)

# Run the Streamlit app
try:
    print("Starting CISSP Tutor & Exam Platform...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
except KeyboardInterrupt:
    print("\nShutting down CISSP Tutor & Exam Platform...")
except Exception as e:
    print(f"Error running the application: {e}")
    sys.exit(1)
