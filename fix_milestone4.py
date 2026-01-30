"""
fix_milestone4.py - Fix all Milestone 4 test issues
"""

import os
import sys
from pathlib import Path

def setup_directories():
    """Create all required directories"""
    directories = [
        "data",
        "data/drafts",
        "data/reviews",
        "data/reports",
        "src"
    ]
    
    for dir_path in directories:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Created: {dir_path}")
    
    return True

def create_sample_draft():
    """Create a sample draft for testing"""
    sample_content = """## Abstract
This literature review examines recent advancements in quantum computing applications. 
The paper analyzes three key research papers that demonstrate practical implementations 
in quantum cryptography, optimization, and machine learning.

## Methodology
A systematic review methodology was employed. Papers were selected based on 
relevance to practical quantum applications, publication date (2020-2023), 
and citation count. Each paper was analyzed for methodology, results, and limitations.

## Results
The review found that quantum computing shows significant promise in specific 
application domains. Key findings include improved error correction rates in 
quantum cryptography and speedup advantages in optimization problems.

## Discussion
While promising, challenges remain in scalability and error rates. 
The integration of classical and quantum systems appears to be the most 
promising near-term approach.

## Conclusion
Quantum computing is advancing rapidly with practical applications emerging 
in several fields. Continued research is needed to overcome current limitations.

## References
Author A. (2023). Quantum Applications Journal.
Author B. (2022). Advances in Quantum Computing.
Author C. (2021). Practical Quantum Implementations."""

    draft_path = Path("data/drafts/sample_review.txt")
    with open(draft_path, 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    print(f"✅ Created sample draft: {draft_path}")
    return True

def check_requirements():
    """Check and install required packages"""
    try:
        import gradio
        print(f"✅ Gradio {gradio.__version__} is installed")
    except ImportError:
        print("❌ Gradio not installed. Installing...")
        os.system(f"{sys.executable} -m pip install gradio==3.50.2")
    
    try:
        import json
        import re
        print("✅ All core dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def main():
    """Main fix function"""
    print("\n" + "="*60)
    print("           FIXING MILESTONE 4 TEST ISSUES")
    print("="*60)
    
    print("\n📁 Step 1: Setting up directories...")
    setup_directories()
    
    print("\n📝 Step 2: Creating sample draft...")
    create_sample_draft()
    
    print("\n🔧 Step 3: Checking requirements...")
    if not check_requirements():
        print("⚠️  Some requirements missing, but continuing...")
    
    print("\n🧪 Step 4: Testing modules...")
    
    # Test review_module
    try:
        from review_module import run_complete_review, analyze_draft_quality
        print("✅ review_module.py imports successfully")
        
        # Quick test
        test_content = "## Test\nTest content"
        result = analyze_draft_quality(test_content)
        print(f"✅ analyze_draft_quality() works: score={result.get('overall_score', 0)}")
        
    except ImportError as e:
        print(f"❌ review_module.py import failed: {e}")
    
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("   1. Run: python test_milestone4.py")
    print("   2. All tests should pass now")
    print("   3. Run: python gradio_milestone4.py for the UI")
    print("\n💡 If tests still fail:")
    print("   - Check all files are in correct location")
    print("   - Ensure data/drafts/ has at least one .txt file")
    print("   - Run: python fix_milestone4.py again")
    print("="*60)

if __name__ == "__main__":
    main()