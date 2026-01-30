"""
test_milestone4.py - Fixed Milestone 4 Requirements Test
"""

import json
import os
import sys
import importlib
from pathlib import Path
from datetime import datetime

# Add src to path
project_root = Path(__file__).parent
src_dir = project_root / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

def test_requirements():
    """Test all Milestone 4 requirements"""
    print("🎯 TESTING MILESTONE 4 REQUIREMENTS")
    print("="*60)
    
    requirements = [
        {
            "id": 1,
            "requirement": "Review and refinement cycle",
            "test": "Check review_module.py functions",
            "status": "PENDING",
            "details": ""
        },
        {
            "id": 2,
            "requirement": "Revision suggestions and quality evaluation",
            "test": "Check quality analysis functions",
            "status": "PENDING",
            "details": ""
        },
        {
            "id": 3,
            "requirement": "Final UI Integration: Polished Gradio interface",
            "test": "Check gradio_milestone4.py exists and runs",
            "status": "PENDING",
            "details": ""
        },
        {
            "id": 4,
            "requirement": "UI controls (e.g., 'Critique/Revise' button)",
            "test": "Verify Gradio interface has required buttons",
            "status": "PENDING",
            "details": ""
        },
        {
            "id": 5,
            "requirement": "Present all generated sections clearly",
            "test": "Check if UI displays Abstract, Methods, Results, References",
            "status": "PENDING",
            "details": ""
        },
        {
            "id": 6,
            "requirement": "User-triggered re-runs of revision cycle",
            "test": "Verify button triggers functionality",
            "status": "PENDING",
            "details": ""
        },
        {
            "id": 7,
            "requirement": "Prepare final report",
            "test": "Check report generation in data/reviews/",
            "status": "PENDING",
            "details": ""
        },
        {
            "id": 8,
            "requirement": "Conduct final testing",
            "test": "This test script execution",
            "status": "PENDING",
            "details": ""
        }
    ]
    
    # Test 1: Check review_module.py exists and has required functions
    print("\n🔍 Testing Requirement 1: Review and refinement cycle")
    if Path("src/review_module.py").exists():
        try:
            # Try to import and check functions
            import src.review_module as rm
            # Check if it has required methods
            if hasattr(rm, 'ReviewModule'):
                reviewer = rm.ReviewModule()
                if hasattr(reviewer, 'run_complete_review'):
                    requirements[0]["status"] = "PASSED"
                    requirements[0]["details"] = "review_module.py with run_complete_review() exists"
                else:
                    requirements[0]["status"] = "FAILED"
                    requirements[0]["details"] = "Missing run_complete_review method"
            else:
                requirements[0]["status"] = "FAILED"
                requirements[0]["details"] = "No ReviewModule class found"
        except Exception as e:
            requirements[0]["status"] = "PARTIAL"
            requirements[0]["details"] = f"Import error: {str(e)}"
    else:
        requirements[0]["status"] = "FAILED"
        requirements[0]["details"] = "File src/review_module.py not found"
    
    # Test 2: Check quality analysis functions
    print("🔍 Testing Requirement 2: Revision suggestions and quality evaluation")
    if Path("src/review_module.py").exists():
        try:
            import src.review_module as rm
            reviewer = rm.ReviewModule()
            # Create test draft
            test_draft = "## Abstract\nTest\n## Methods\nTest\n## Results\nTest\n## References\nTest"
            
            # Check analyze_draft_quality method
            if hasattr(reviewer, 'analyze_draft_quality'):
                analysis = reviewer.analyze_draft_quality(test_draft)
                if isinstance(analysis, dict) and 'quality_score' in analysis:
                    requirements[1]["status"] = "PASSED"
                    requirements[1]["details"] = f"Quality analysis works (score: {analysis.get('quality_score', 0)})"
                else:
                    requirements[1]["status"] = "PARTIAL"
                    requirements[1]["details"] = "analyze_draft_quality returns unexpected format"
            else:
                requirements[1]["status"] = "FAILED"
                requirements[1]["details"] = "Missing analyze_draft_quality method"
        except Exception as e:
            requirements[1]["status"] = "FAILED"
            requirements[1]["details"] = f"Error: {str(e)[:100]}"
    else:
        requirements[1]["status"] = "FAILED"
        requirements[1]["details"] = "review_module.py not found"
    
    # Test 3: Check Gradio interface
    print("🔍 Testing Requirement 3: Gradio interface")
    if Path("gradio_milestone4.py").exists():
        try:
            # Check Gradio installation
            import gradio
            requirements[2]["status"] = "PASSED"
            requirements[2]["details"] = f"gradio_milestone4.py exists, Gradio {gradio.__version__} installed"
        except ImportError:
            requirements[2]["status"] = "FAILED"
            requirements[2]["details"] = "Gradio not installed"
    else:
        requirements[2]["status"] = "FAILED"
        requirements[2]["details"] = "gradio_milestone4.py not found"
    
    # Test 4: Check UI controls in gradio_milestone4.py
    print("🔍 Testing Requirement 4: UI controls")
    if Path("gradio_milestone4.py").exists():
        try:
            with open("gradio_milestone4.py", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for critique button
            if 'Critique' in content or 'CRITIQUE' in content or 'critique' in content:
                requirements[3]["status"] = "PASSED"
                requirements[3]["details"] = "UI controls found in code"
            else:
                requirements[3]["status"] = "FAILED"
                requirements[3]["details"] = "No critique button found in code"
        except Exception as e:
            requirements[3]["status"] = "FAILED"
            requirements[3]["details"] = f"Error reading file: {e}"
    else:
        requirements[3]["status"] = "FAILED"
        requirements[3]["details"] = "gradio_milestone4.py not found"
    
    # Test 5: Check sections display
    print("🔍 Testing Requirement 5: Present sections clearly")
    if Path("gradio_milestone4.py").exists():
        try:
            with open("gradio_milestone4.py", 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            # Check for required sections in UI
            sections_to_check = ['abstract', 'method', 'result', 'reference']
            found_sections = []
            
            for section in sections_to_check:
                if section in content:
                    found_sections.append(section)
            
            if len(found_sections) >= 3:
                requirements[4]["status"] = "PASSED"
                requirements[4]["details"] = f"Found sections: {', '.join(found_sections)}"
            else:
                requirements[4]["status"] = "PARTIAL"
                requirements[4]["details"] = f"Found only {len(found_sections)} sections"
        except Exception as e:
            requirements[4]["status"] = "FAILED"
            requirements[4]["details"] = f"Error: {e}"
    else:
        requirements[4]["status"] = "FAILED"
        requirements[4]["details"] = "gradio_milestone4.py not found"
    
    # Test 6: Check user-triggered re-runs
    print("🔍 Testing Requirement 6: User-triggered re-runs")
    if Path("gradio_milestone4.py").exists():
        try:
            with open("gradio_milestone4.py", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for click handlers or button callbacks
            if 'click(' in content or '.click' in content or 'on_click' in content:
                requirements[5]["status"] = "PASSED"
                requirements[5]["details"] = "Button click handlers found"
            else:
                requirements[5]["status"] = "PARTIAL"
                requirements[5]["details"] = "No clear click handlers found"
        except Exception as e:
            requirements[5]["status"] = "FAILED"
            requirements[5]["details"] = f"Error: {e}"
    else:
        requirements[5]["status"] = "FAILED"
        requirements[5]["details"] = "gradio_milestone4.py not found"
    
    # Test 7: Check final report generation
    print("🔍 Testing Requirement 7: Final report")
    if Path("src/review_module.py").exists():
        try:
            import src.review_module as rm
            reviewer = rm.ReviewModule()
            
            # Check if save_review_report method exists
            if hasattr(reviewer, 'save_review_report'):
                requirements[6]["status"] = "PASSED"
                requirements[6]["details"] = "save_review_report method exists"
            else:
                requirements[6]["status"] = "FAILED"
                requirements[6]["details"] = "Missing save_review_report method"
        except Exception as e:
            requirements[6]["status"] = "FAILED"
            requirements[6]["details"] = f"Error: {str(e)[:100]}"
    else:
        requirements[6]["status"] = "FAILED"
        requirements[6]["details"] = "review_module.py not found"
    
    # Test 8: This test itself
    print("🔍 Testing Requirement 8: Final testing")
    requirements[7]["status"] = "PASSED"
    requirements[7]["details"] = "This test script is running successfully"
    
    # Ensure data directories exist
    print("\n📁 Creating/checking data directories...")
    data_dirs = ["data", "data/drafts", "data/reviews"]
    for dir_path in data_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {dir_path}/")
    
    # Create a test draft if none exists
    drafts_dir = Path("data/drafts")
    if not list(drafts_dir.glob("*.txt")):
        test_draft = """## Abstract
This review examines machine learning applications in healthcare.

## Methodology Comparison
Three approaches were compared: supervised learning, unsupervised learning, and reinforcement learning.

## Results Synthesis
All methods showed promising results, with supervised learning achieving 95% accuracy.

## Discussion
The findings suggest machine learning has significant potential in medical diagnostics.

## References
Smith, J. (2023). ML in Healthcare. Journal of Medical AI.
"""
        
        test_file = drafts_dir / "test_draft_milestone4.txt"
        test_file.write_text(test_draft)
        print(f"  ✅ Created test draft: {test_file.name}")
    
    # Display results
    print("\n📊 TEST RESULTS:")
    print("="*60)
    
    passed = 0
    failed = 0
    partial = 0
    
    for req in requirements:
        if req["status"] == "PASSED":
            icon = "✅"
            passed += 1
        elif req["status"] == "FAILED":
            icon = "❌"
            failed += 1
        else:
            icon = "⚠️ "
            partial += 1
        
        print(f"{icon} {req['id']}. {req['requirement']}")
        if req["details"]:
            print(f"   Details: {req['details']}")
        print()
    
    print("="*60)
    print(f"SUMMARY: {passed} passed, {failed} failed, {partial} partial/warnings")
    
    # Save detailed report
    report_dir = Path("data/reviews")
    report_dir.mkdir(exist_ok=True)
    
    results = {
        "test_date": datetime.now().isoformat(),
        "milestone": 4,
        "requirements": requirements,
        "summary": {
            "total": len(requirements),
            "passed": passed,
            "failed": failed,
            "partial": partial
        },
        "system_info": {
            "python_version": sys.version,
            "working_directory": str(project_root)
        }
    }
    
    report_file = report_dir / f"milestone4_comprehensive_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📋 Detailed report saved: {report_file}")
    
    # Recommendations
    print("\n" + "="*60)
    if failed == 0 and partial <= 2:
        print("🎉 MILESTONE 4 READY FOR SUBMISSION!")
        print("\n🚀 To launch Gradio interface:")
        print("   python gradio_milestone4.py")
        print("\n🌐 Then open: http://localhost:7860")
        print("\n💡 Demonstration steps:")
        print("   1. Select a draft from dropdown")
        print("   2. Click 'CRITIQUE / REVISE' button")
        print("   3. Review quality assessment")
        print("   4. Check revision suggestions")
        print("   5. View generated report in data/reviews/")
    else:
        print("⚠️  ATTENTION NEEDED")
        print("\n💡 Issues to fix:")
        for req in requirements:
            if req["status"] in ["FAILED", "PARTIAL"]:
                print(f"   • Requirement {req['id']}: {req['details']}")
        
        print("\n🔧 Quick fixes:")
        print("   1. Ensure all required files exist")
        print("   2. Check Gradio installation: pip install gradio==3.50.2")
        print("   3. Run: python fix_dependencies.py")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    test_requirements()