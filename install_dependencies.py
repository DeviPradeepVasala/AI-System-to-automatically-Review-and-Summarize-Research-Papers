"""
install_dependencies.py
Install all required packages
"""

import subprocess
import sys

def install_packages():
    packages = [
        "python-dotenv",
        "requests",
        "PyMuPDF",
        "pdfplumber",
        "pytesseract",
        "Pillow",
        "nltk",
        "scikit-learn",
        "tqdm",
        "openai",
        "langchain",
        "langchain-google-genai",
        "gradio",
        "numpy"
    ]
    
    print("=" * 60)
    print("Installing Research Paper Reviewer Dependencies")
    print("=" * 60)
    
    for package in packages:
        try:
            print(f"\nInstalling {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
    
    print("\n" + "=" * 60)
    print("✅ All packages installed!")
    print("\nNext steps:")
    print("1. Create a .env file with your API keys")
    print("2. Run: python run_all.py")
    print("=" * 60)

if __name__ == "__main__":
    install_packages()