#!/usr/bin/env python
"""
Setup script for the CISSP Tutor & Exam Platform.
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

import config


def check_system_requirements():
    """Check if the system meets the requirements."""
    print("Checking system requirements...")
    
    # Check Python version
    print("\nChecking Python version...")
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 11):
        print(f"❌ Error: Python 3.11+ is required, but you have {major}.{minor}")
        return False
    print(f"✅ Python version {major}.{minor} is compatible")
    
    # Check available RAM
    print("\nChecking available memory...")
    try:
        if platform.system() == "Windows":
            import psutil
            total_ram = psutil.virtual_memory().total / (1024 ** 3)  # GB
        elif platform.system() == "Darwin":  # macOS
            result = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True,
                text=True,
                check=True
            )
            total_ram = int(result.stdout.strip()) / (1024 ** 3)  # GB
        elif platform.system() == "Linux":
            result = subprocess.run(
                ["grep", "MemTotal", "/proc/meminfo"],
                capture_output=True,
                text=True,
                check=True
            )
            total_ram = int(result.stdout.split()[1]) / (1024 ** 2)  # GB
        else:
            total_ram = None
            print("⚠️ Could not determine available RAM")
        
        if total_ram is not None:
            print(f"System has {total_ram:.1f} GB RAM")
            if total_ram < 8:
                print("⚠️ Warning: Less than 8GB RAM detected. Performance may be limited.")
            elif total_ram < 16:
                print("✅ Minimum RAM requirement met (8GB+)")
            else:
                print("✅ Recommended RAM requirement met (16GB+)")
    except Exception as e:
        print(f"⚠️ Could not determine available RAM: {e}")
    
    # Check for GPU availability
    print("\nChecking for GPU availability...")
    gpu_info = check_gpu_availability()
    
    # Check disk space
    print("\nChecking available disk space...")
    try:
        if platform.system() == "Windows":
            import shutil
            total, used, free = shutil.disk_usage(project_root)
            free_gb = free / (1024 ** 3)  # GB
        else:  # macOS or Linux
            result = subprocess.run(
                ["df", "-h", project_root],
                capture_output=True,
                text=True,
                check=True
            )
            # Parse the output (varies by OS)
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                parts = lines[1].split()
                if platform.system() == "Darwin":  # macOS
                    free_gb = float(parts[3].rstrip("Gi"))
                else:  # Linux
                    free_gb = float(parts[3].rstrip("G"))
            else:
                free_gb = None
        
        if free_gb is not None:
            print(f"Available disk space: {free_gb:.1f} GB")
            if free_gb < 2:
                print("⚠️ Warning: Less than 2GB free disk space. This may not be enough.")
            elif free_gb < 5:
                print("✅ Minimum disk space requirement met (2GB+)")
            else:
                print("✅ Recommended disk space requirement met (5GB+)")
    except Exception as e:
        print(f"⚠️ Could not determine available disk space: {e}")
    
    print("\n✅ System requirements check completed")
    return True


def check_gpu_availability():
    """Check if GPU is available for Ollama."""
    gpu_info = {
        "nvidia": False,
        "amd": False,
        "apple_silicon": False,
        "details": ""
    }
    
    # Check for NVIDIA GPU
    try:
        if platform.system() == "Windows" or platform.system() == "Linux":
            result = subprocess.run(
                ["nvidia-smi"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                gpu_info["nvidia"] = True
                # Extract GPU model and memory
                for line in result.stdout.split('\n'):
                    if "NVIDIA" in line and "GPU" in line:
                        gpu_info["details"] = line.strip()
                        break
                print(f"✅ NVIDIA GPU detected: {gpu_info['details']}")
            else:
                print("❌ No NVIDIA GPU detected")
    except FileNotFoundError:
        print("❌ NVIDIA tools not found (nvidia-smi)")
    
    # Check for AMD GPU on Linux
    if platform.system() == "Linux":
        try:
            result = subprocess.run(
                ["rocminfo"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                gpu_info["amd"] = True
                print("✅ AMD GPU with ROCm support detected")
            else:
                print("❌ No AMD GPU with ROCm support detected")
        except FileNotFoundError:
            print("❌ AMD ROCm tools not found (rocminfo)")
    
    # Check for Apple Silicon
    if platform.system() == "Darwin":
        try:
            result = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True,
                text=True,
                check=True
            )
            cpu_info = result.stdout.strip()
            
            if "Apple" in cpu_info:
                gpu_info["apple_silicon"] = True
                gpu_info["details"] = cpu_info
                print(f"✅ Apple Silicon detected: {cpu_info}")
            else:
                print(f"❌ Intel Mac detected: {cpu_info}")
        except Exception as e:
            print(f"⚠️ Could not determine Mac processor type: {e}")
    
    # Summary
    if gpu_info["nvidia"] or gpu_info["amd"] or gpu_info["apple_silicon"]:
        print("✅ Hardware acceleration available for Ollama")
        if gpu_info["nvidia"]:
            print("   NVIDIA GPUs offer the best performance with Ollama")
        elif gpu_info["apple_silicon"]:
            print("   Apple Silicon provides good acceleration for Ollama")
        elif gpu_info["amd"]:
            print("   AMD GPUs with ROCm provide acceleration for Ollama")
    else:
        print("⚠️ No hardware acceleration detected. Ollama will run in CPU-only mode.")
        print("   This will be significantly slower for inference.")
    
    return gpu_info


def install_dependencies():
    """Install the required dependencies."""
    print("\nInstalling dependencies...")
    
    requirements_file = os.path.join(project_root, "requirements.txt")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", requirements_file],
            check=True
        )
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False


def check_ollama():
    """Check if Ollama is installed and running."""
    print("\nChecking Ollama installation...")
    
    # Check if Ollama is in PATH
    ollama_path = None
    if platform.system() == "Windows":
        try:
            result = subprocess.run(
                ["where", "ollama"],
                capture_output=True,
                text=True,
                check=True
            )
            ollama_path = result.stdout.strip()
        except subprocess.CalledProcessError:
            pass
    else:  # macOS or Linux
        try:
            result = subprocess.run(
                ["which", "ollama"],
                capture_output=True,
                text=True,
                check=True
            )
            ollama_path = result.stdout.strip()
        except subprocess.CalledProcessError:
            pass
    
    if not ollama_path:
        print("Ollama not found in PATH")
        print("Please install Ollama from https://ollama.ai/")
        return False
    
    print(f"Found Ollama at: {ollama_path}")
    
    # Check if Ollama is running
    print("Checking if Ollama is running...")
    
    try:
        response = subprocess.run(
            ["curl", "-s", f"{config.OLLAMA_BASE_URL}/api/tags"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if response.returncode != 0:
            print("Ollama is not running")
            print(f"Please start Ollama with: {ollama_path} serve")
            return False
        
        print("✅ Ollama is running")
        
        # Check if the required model is available
        print(f"Checking if the {config.LLM_MODEL} model is available...")
        
        model_response = subprocess.run(
            ["curl", "-s", f"{config.OLLAMA_BASE_URL}/api/tags"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if config.LLM_MODEL not in model_response.stdout:
            print(f"Model {config.LLM_MODEL} is not available")
            print(f"Please download it with: {ollama_path} pull {config.LLM_MODEL}")
            return False
        
        print(f"✅ Model {config.LLM_MODEL} is available")
        return True
    
    except Exception as e:
        print(f"Error checking Ollama: {e}")
        return False


def create_directories():
    """Create the required directories."""
    print("\nCreating directories...")
    
    try:
        os.makedirs(config.PDF_DIR, exist_ok=True)
        os.makedirs(config.DB_DIR, exist_ok=True)
        
        print(f"✅ Created directory: {config.PDF_DIR}")
        print(f"✅ Created directory: {config.DB_DIR}")
        return True
    except Exception as e:
        print(f"Error creating directories: {e}")
        return False


def download_sample_data():
    """Download sample data for testing."""
    print("\nDownloading sample data...")
    
    try:
        subprocess.run(
            [sys.executable, os.path.join(project_root, "download_samples.py")],
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading sample data: {e}")
        return False


def process_sample_data():
    """Process the sample data."""
    print("\nProcessing sample data...")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "src.ingestion.ingest"],
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error processing sample data: {e}")
        return False


def main():
    """Main setup function."""
    print("=" * 80)
    print("CISSP Tutor & Exam Platform Setup")
    print("=" * 80)
    
    # Check system requirements
    if not check_system_requirements():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Check Ollama
    ollama_ok = check_ollama()
    
    # Download sample data
    download_ok = download_sample_data()
    
    # Process sample data if Ollama is available
    process_ok = False
    if ollama_ok and download_ok:
        process_ok = process_sample_data()
    
    # Print summary
    print("\n" + "=" * 80)
    print("Setup Summary")
    print("=" * 80)
    
    print("✅ System requirements check: Passed")
    print("✅ Dependencies installation: Completed")
    print("✅ Directory creation: Completed")
    print(f"{'✅' if ollama_ok else '❌'} Ollama check: {'Passed' if ollama_ok else 'Failed'}")
    print(f"{'✅' if download_ok else '❌'} Sample data download: {'Completed' if download_ok else 'Failed'}")
    
    if ollama_ok and download_ok:
        print(f"{'✅' if process_ok else '❌'} Sample data processing: {'Completed' if process_ok else 'Failed'}")
    else:
        print("❌ Sample data processing: Skipped")
    
    # Next steps
    print("\n" + "=" * 80)
    print("Next Steps")
    print("=" * 80)
    
    if not ollama_ok:
        print("1. Install Ollama from https://ollama.ai/")
        print(f"2. Pull the {config.LLM_MODEL} model with: ollama pull {config.LLM_MODEL}")
        print("3. Start Ollama with: ollama serve")
    
    if not process_ok:
        if ollama_ok:
            print("1. Process the sample data with: python -m src.ingestion.ingest")
        else:
            print("4. Process the sample data with: python -m src.ingestion.ingest")
    
    print("\nTo start the web interface:")
    print("  python run_app.py")
    
    print("\nTo use the command-line interface:")
    print("  python cli.py ask \"What is the CIA triad?\"")
    
    print("\n" + "=" * 80)
    print("Thank you for installing the CISSP Tutor & Exam Platform!")
    print("=" * 80)


if __name__ == "__main__":
    main()
