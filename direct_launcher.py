#!/usr/bin/env python
"""
Direct launcher for CISSP Tutor with improved user experience.

This script provides a simple way to start the CISSP Tutor with proper patches
and compatibility fixes for PyTorch and Streamlit.
"""
import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

# ASCII art for startup
BANNER = """
 ██████╗██╗███████╗███████╗██████╗     ████████╗██╗   ██╗████████╗ ██████╗ ██████╗ 
██╔════╝██║██╔════╝██╔════╝██╔══██╗    ╚══██╔══╝██║   ██║╚══██╔══╝██╔═══██╗██╔══██╗
██║     ██║███████╗███████╗██████╔╝       ██║   ██║   ██║   ██║   ██║   ██║██████╔╝
██║     ██║╚════██║╚════██║██╔═══╝        ██║   ██║   ██║   ██║   ██║   ██║██╔══██╗
╚██████╗██║███████║███████║██║            ██║   ╚██████╔╝   ██║   ╚██████╔╝██║  ██║
 ╚═════╝╚═╝╚══════╝╚══════╝╚═╝            ╚═╝    ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                                                                    
 Interactive Learning Platform for CISSP Preparation
 Powered by RAG and LLM Technologies
---------------------------------------------------------------------------
"""

def check_requirements():
    """Check that all required dependencies are installed."""
    try:
        import streamlit
        import langchain
        import chromadb
        import sentence_transformers
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Installing required dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return False

def check_torch_install():
    """Check that PyTorch is properly installed."""
    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
        if torch.cuda.is_available():
            print(f"CUDA available: {torch.cuda.get_device_name(0)}")
        elif hasattr(torch, 'mps') and torch.backends.mps.is_available():
            print("MPS (Apple Silicon) acceleration available")
        else:
            print("Running in CPU mode")
        return True
    except ImportError:
        print("PyTorch not installed. Will attempt to install...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "torch"])
        return False

def check_ollama():
    """Check if Ollama is running and available."""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                print(f"Ollama is running with {len(models)} models available:")
                for model in models:
                    print(f" - {model['name']}")
                return True
            else:
                print("Ollama is running but no models are available")
                print("Run 'ollama pull llama3:8b' to download a compatible model")
                return False
        else:
            print("Ollama API responded but returned an error")
            return False
    except Exception as e:
        print(f"Ollama is not running or not available: {e}")
        print("Please install Ollama from https://ollama.ai/")
        print("After installing, run 'ollama pull llama3:8b'")
        return False

def main():
    """Run the CISSP Tutor application."""
    print(BANNER)
    
    # Check requirements
    print("Checking dependencies...")
    if not check_requirements():
        print("Dependencies installed. Proceeding...")
    
    # Check PyTorch
    print("\nChecking PyTorch installation...")
    if not check_torch_install():
        print("PyTorch installed. Proceeding...")
    
    # Check Ollama
    print("\nChecking Ollama availability...")
    check_ollama()
    
    # Run the app
    print("\nStarting CISSP Tutor & Exam Platform...")
    print("This may take a few moments to initialize...")
    
    # Create the command to run
    python_executable = sys.executable
    run_script = Path(__file__).parent / "run_app_fixed.py"
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(3)  # Give Streamlit time to start
        webbrowser.open("http://localhost:8501")
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run the Streamlit app
    os.environ["PYTHONPATH"] = str(Path(__file__).parent)
    subprocess.run([python_executable, str(run_script)])

if __name__ == "__main__":
    main()
