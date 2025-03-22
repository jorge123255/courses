#!/usr/bin/env python
"""
Fixed launcher for the CISSP Tutor & Exam Platform that applies patches.

This script handles the PyTorch-Streamlit compatibility issues before launching the app.
"""
import os
import sys
import importlib.util
import subprocess

def main():
    """Apply patches and run the Streamlit app."""
    print("Starting CISSP Tutor & Exam Platform with patches...")
    
    # Apply patches
    try:
        import streamlit_patch
        streamlit_patch.apply_patches()
        print("Patches applied successfully")
    except ImportError:
        print("Warning: streamlit_patch.py not found in path. Some features may not work correctly.")
    
    # Install nest_asyncio if not present
    try:
        import nest_asyncio
    except ImportError:
        print("Installing nest_asyncio for better compatibility...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "nest_asyncio"])
    
    # Run the streamlit app with environment variables to suppress some warnings
    os.environ["PYTHONWARNINGS"] = "ignore::DeprecationWarning"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    
    import streamlit.web.cli as streamlit_cli
    sys.argv = ["streamlit", "run", "app.py"]
    streamlit_cli.main()

if __name__ == "__main__":
    main()
