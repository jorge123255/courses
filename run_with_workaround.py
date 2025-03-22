#!/usr/bin/env python
"""
Simple run script for CISSP Tutor that applies all necessary workarounds.

This script handles:
1. PyTorch-Streamlit compatibility issues
2. Asyncio event loop conflicts
3. Proper environment setup
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Run the CISSP Tutor with all necessary workarounds."""
    print("CISSP Tutor - Starting with compatibility fixes...")
    
    # Set environment variables for better compatibility
    os.environ["PYTHONWARNINGS"] = "ignore::DeprecationWarning"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    
    # Create a streamlit patch file if it doesn't exist
    patch_path = Path(__file__).parent / "streamlit_patch.py"
    if not patch_path.exists():
        print("Creating streamlit patch file to fix PyTorch compatibility...")
        with open(patch_path, "w") as f:
            f.write('''
"""
Patch for Streamlit-PyTorch compatibility issues.
Apply this before importing streamlit to avoid runtime errors with path attributes.
"""
import types
import sys

# Only apply the patch if PyTorch is installed
try:
    import torch
    has_torch = True
except ImportError:
    has_torch = False

def patch_streamlit():
    """
    Patch Streamlit's path handling to avoid errors with PyTorch's custom path attributes.
    This prevents the "RuntimeError: Tried to instantiate class '__path__._path'" error.
    """
    if not has_torch:
        return
        
    from streamlit.watcher import local_sources_watcher
    
    # Save the original function
    original_extract_paths = local_sources_watcher.extract_paths
    
    # Create a patched version that handles the PyTorch special case
    def patched_extract_paths(module):
        try:
            # For PyTorch modules, avoid using __path__._path
            if hasattr(module, "__name__") and module.__name__.startswith("torch."):
                if hasattr(module, "__path__"):
                    if isinstance(module.__path__, list):
                        return module.__path__
                    if hasattr(module.__path__, "_path") and isinstance(module.__path__._path, list):
                        return list(module.__path__._path)
                    return []
            
            # For normal modules, use the original function
            return original_extract_paths(module)
        except Exception:
            # Fallback to empty list if there's any error
            return []
    
    # Apply the patch
    local_sources_watcher.extract_paths = patched_extract_paths

# Apply the patch
if has_torch:
    patch_streamlit()
''')
    
    # Create a patched app runner script if it doesn't exist
    run_app_path = Path(__file__).parent / "run_app_fixed.py"
    if not run_app_path.exists():
        print("Creating patched app runner script...")
        with open(run_app_path, "w") as f:
            f.write('''
#!/usr/bin/env python
"""
Fixed runner for CISSP Tutor with PyTorch compatibility patches.
"""
import sys
import importlib.util

# Import and apply the streamlit patch first
import streamlit_patch

# Import nest_asyncio to fix asyncio issues
try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    print("Warning: nest_asyncio not found. Some features may not work correctly.")

# Run the original app
import app
''')
    
    # Install nest_asyncio if needed
    try:
        import nest_asyncio
    except ImportError:
        print("Installing nest_asyncio for better compatibility...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "nest_asyncio"])
    
    # Run the fixed app script
    print("Launching app with compatibility patches applied...")
    subprocess.run([sys.executable, str(run_app_path)])

if __name__ == "__main__":
    main()
