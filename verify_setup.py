#!/usr/bin/env python
"""
Simple script to verify project setup and dependencies.
Run: python verify_setup.py
"""

import sys
from pathlib import Path

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("✗ Python 3.11+ required")
        return False
    return True


def check_directories():
    """Check directory structure."""
    required_dirs = ["src", "data", "docs", "powerbi", "tests", "scripts", "assets"]
    project_root = Path(__file__).parent
    
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"✓ {dir_name}/ exists")
        else:
            print(f"✗ {dir_name}/ missing")
            return False
    
    return True


def check_files():
    """Check required files."""
    required_files = [
        "app.py",
        "requirements.txt",
        ".env.example",
        ".gitignore",
        "README.md",
        "LICENSE",
    ]
    project_root = Path(__file__).parent
    
    for file_name in required_files:
        file_path = project_root / file_name
        if file_path.exists():
            print(f"✓ {file_name} exists")
        else:
            print(f"✗ {file_name} missing")
            return False
    
    return True


def check_dependencies():
    """Check if main dependencies are installed."""
    dependencies = [
        "streamlit",
        "pandas",
        "plotly",
        "langchain",
        "chromadb",
        "pydantic_settings",
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep} installed")
        except ImportError:
            print(f"✗ {dep} not installed")
            return False
    
    return True


def check_env():
    """Check .env configuration."""
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        print(f"✓ .env file exists")
        return True
    else:
        print(f"⚠ .env file missing (use .env.example as template)")
        return False


def main():
    """Run all checks."""
    print("\n🔍 Verification Setup\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Directories", check_directories),
        ("Files", check_files),
        ("Dependencies", check_dependencies),
        (".env Configuration", check_env),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"✗ Error: {e}")
            results.append(False)
    
    print("\n" + "="*50)
    if all(results[:-1]):  # Exclude .env check (it's optional)
        print("✅ Setup is valid! You can run: streamlit run app.py")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
