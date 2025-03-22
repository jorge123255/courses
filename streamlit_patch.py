#!/usr/bin/env python
"""
Patch for Streamlit-PyTorch compatibility issues.

This patch addresses the PyTorch __path__._path error that occurs in Streamlit's file watcher.
"""
import os
import sys
import importlib
from types import ModuleType

class PathProxyModule(ModuleType):
    def __init__(self, module_name):
        super().__init__(module_name)
        self.real_module = importlib.import_module(module_name)
        for attr in dir(self.real_module):
            if attr != "__path__":
                setattr(self, attr, getattr(self.real_module, attr))
    
    @property
    def __path__(self):
        if hasattr(self.real_module, "__path__"):
            return getattr(self.real_module, "__path__")
        return []

def apply_patches():
    """Apply all patches to make Streamlit work with PyTorch."""
    # Patch the PyTorch _classes module to avoid __path__._path errors
    if "torch._classes" in sys.modules:
        torch_classes = sys.modules["torch._classes"]
        patched_module = PathProxyModule("torch._classes")
        sys.modules["torch._classes"] = patched_module
        print("Applied patch for torch._classes __path__ issue")
    
    # Patch the asyncio event loop handling if needed
    try:
        import asyncio
        import nest_asyncio
        nest_asyncio.apply()
        print("Applied nest_asyncio patch for event loop")
    except ImportError:
        print("nest_asyncio not available - run 'pip install nest_asyncio' for better compatibility")
    
    # Patch 3: Fix streamlit's local_sources_watcher
    try:
        from streamlit.watcher import local_sources_watcher
        
        # Replace the problematic extract_paths function
        original_extract_paths = local_sources_watcher.extract_paths
        
        def safe_extract_paths(module):
            """Safely extract paths from a module, handling special cases"""
            try:
                if hasattr(module, "__path__"):
                    if hasattr(module.__path__, "_path"):
                        return list(module.__path__._path)
                return original_extract_paths(module)
            except Exception:
                # If we can't extract paths, return an empty list
                return []
        
        local_sources_watcher.extract_paths = safe_extract_paths
        print("✓ Applied streamlit.watcher.local_sources_watcher patch")
    except Exception as e:
        print(f"✗ Failed to apply streamlit.watcher patch: {e}")
    
    print("Patches applied. Starting application...")

if __name__ == "__main__":
    apply_patches()
    
    # Import and run the app
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Run Streamlit directly with command line arguments
    import streamlit.web.cli as stcli
    sys.argv = ["streamlit", "run", "app.py", "--server.port=8501"]
    stcli.main()
