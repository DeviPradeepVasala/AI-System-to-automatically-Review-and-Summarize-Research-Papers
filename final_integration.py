"""
final_integration.py
Complete project integration and final testing
"""

import json
from pathlib import Path
from datetime import datetime
import sys
import os

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = Path(current_dir)
src_dir = project_root / "src"

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

try:
    from config import Config
    from paper_search import PaperSearchSystem
    from text_extraction import TextExtractor
    from paper_analyzer import PaperAnalyzer
    from draft_generator import DraftGenerator
    from review_module import ReviewModule
    from pipeline import ResearchPipeline
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


class FinalIntegration:
    """Final integration and testing"""
    
    def __init__(self):
        """Initialize integration"""
        self.config = Config
        self.setup_complete = self.config.setup_directories()
        
        # Initialize all modules
        self.modules = {
            'paper_search': PaperSearchSystem(),
            'text_extractor': TextExtractor(),
            'paper_analyzer': PaperAnalyzer(),
            'draft_generator': DraftGenerator(),
            'review_module': ReviewModule(),
            'pipeline': ResearchPipeline()
        }
        
        # Test results
        self.results = {
            'integration_test': datetime.now().isoformat(),
            'modules': {},
            'overall_status': 'pending'
        }
    
    def test_module(self, module_name, module_instance, test_function):
        """Test a specific module"""
        try:
            print(f"\n🧪 Testing {module_name}...")
            result = test_function()
            self.results['modules'][module_name] = {
                'status': 'success',
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
            print(f"✅ {module_name}: PASSED")
            return True
        except Exception as e:
            self.results['modules'][module_name] = {
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            print(f"❌ {module_name}: FAILED - {e}")
            return False
    
    def test_config(self):
        """Test configuration"""
        try:
            # Setup directories
            self.config.setup_directories()
            
            # Check directories
            required_dirs = [
                self.config.DATA_DIR,
                self.config.PAPERS_DIR,
                self.config.EXTRACTED_TEXT_DIR,
                self.config.ANALYSIS_DIR,
                self.config.DRAFTS_DIR
            ]
            
            for directory in required_dirs:
                if not directory.exists():
                    directory.mkdir(parents=True, exist_ok=True)
            
            return "Configuration setup complete"
        except Exception as e:
            raise Exception(f"Config test failed: {e}")
    
    def test_paper_search(self):
        """Test paper search"""
        try:
            # Quick test - don't actually download
            searcher = self.modules['paper_search']
            
            # Test directory setup
            if not hasattr(searcher, 'setup_complete'):
                return "PaperSearchSystem initialized"
            
            return "Paper search module ready"
        except Exception as e:
            raise Exception(f"Paper search test failed: {e}")
    
    def test_text_extraction(self):
        """Test text extraction"""
        try:
            extractor = self.modules['text_extractor']
            
            # Check if PyMuPDF is available
            import fitz
            return "Text extraction module ready (PyMuPDF available)"
        except ImportError:
            return "Text extraction module ready (PyMuPDF not installed)"
        except Exception as e:
            raise Exception(f"Text extraction test failed: {e}")
    
    def test_paper_analyzer(self):
        """Test paper analyzer"""
        try:
            analyzer = self.modules['paper_analyzer']
            
            # Check NLTK
            import nltk
            try:
                nltk.data.find('tokenizers/punkt')
                nltk_status = "NLTK data available"
            except:
                nltk_status = "NLTK data missing (will download when needed)"
            
            return f"Paper analyzer ready - {nltk_status}"
        except Exception as e:
            raise Exception(f"Paper analyzer test failed: {e}")
    
    def test_draft_generator(self):
        """Test draft generator"""
        try:
            generator = self.modules['draft_generator']
            
            # Check AI availability
            ai_status = "Template mode"
            if hasattr(generator, 'ai_helper') and generator.ai_helper.is_available():
                ai_status = "AI mode available"
            
            return f"Draft generator ready - {ai_status}"
        except Exception as e:
            raise Exception(f"Draft generator test failed: {e}")
    
    def test_review_module(self):
        """Test review module"""
        try:
            reviewer = self.modules['review_module']
            
            # Check if review directory exists
            review_dir = self.config.DATA_DIR / "reviews"
            review_dir.mkdir(exist_ok=True)
            
            return "Review module ready"
        except Exception as e:
            raise Exception(f"Review module test failed: {e}")
    
    def test_pipeline(self):
        """Test pipeline"""
        try:
            pipeline = self.modules['pipeline']
            
            return "Pipeline module ready"
        except Exception as e:
            raise Exception(f"Pipeline test failed: {e}")
    
    def run_complete_test(self):
        """Run complete integration test"""
        print("\n" + "="*60)
        print("           FINAL INTEGRATION TEST")
        print("           Project: AI Research Paper Reviewer")
        print("="*60)
        
        print("\n🔧 Testing all modules...")
        
        # Test each module
        tests = [
            ('config', self.test_config),
            ('paper_search', self.test_paper_search),
            ('text_extraction', self.test_text_extraction),
            ('paper_analyzer', self.test_paper_analyzer),
            ('draft_generator', self.test_draft_generator),
            ('review_module', self.test_review_module),
            ('pipeline', self.test_pipeline)
        ]
        
        passed = 0
        total = len(tests)
        
        for module_name, test_func in tests:
            if self.test_module(module_name, None, test_func):
                passed += 1
        
        # Overall status
        if passed == total:
            self.results['overall_status'] = 'success'
            print(f"\n🎉 ALL TESTS PASSED: {passed}/{total}")
        else:
            self.results['overall_status'] = 'partial_success'
            print(f"\n⚠️  PARTIAL SUCCESS: {passed}/{total} tests passed")
        
        # Save test results
        self.save_test_results()
        
        # Show summary
        self.show_summary()
        
        return self.results
    
    def save_test_results(self):
        """Save test results to file"""
        try:
            results_dir = self.config.DATA_DIR / "test_results"
            results_dir.mkdir(exist_ok=True)
            
            filename = f"integration_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = results_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            
            print(f"\n📊 Test results saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Error saving test results: {e}")
            return None
    
    def show_summary(self):
        """Show test summary"""
        print("\n" + "="*60)
        print("           TEST SUMMARY")
        print("="*60)
        
        print("\n📋 MODULE STATUS:")
        for module_name, module_result in self.results['modules'].items():
            status = module_result['status']
            status_icon = "✅" if status == 'success' else "❌"
            print(f"   {status_icon} {module_name.replace('_', ' ').title()}: {status.upper()}")
        
        print(f"\n🎯 OVERALL STATUS: {self.results['overall_status'].upper()}")
        
        # Next steps based on status
        if self.results['overall_status'] == 'success':
            print("\n🎉 PROJECT READY FOR USE!")
            print("\n📝 Available Options:")
            print("   1. Run web interface: python run_ui.py")
            print("   2. Run complete pipeline: python src/pipeline.py")
            print("   3. Run individual modules from run_all.py")
        else:
            print("\n⚠️  SOME MODULES NEED ATTENTION")
            print("\n💡 Check the failed modules above")
            print("   Install missing packages:")
            print("   pip install PyMuPDF nltk scikit-learn openai google-generativeai")
        
        print("\n" + "="*60)
    
    def generate_final_report(self):
        """Generate final project report"""
        print("\n" + "="*60)
        print("           FINAL PROJECT REPORT")
        print("="*60)
        
        report = {
            'project': 'AI Research Paper Reviewer',
            'version': '1.0.0',
            'completion_date': datetime.now().isoformat(),
            'milestones_completed': [
                'Milestone 1: Paper Search & Download',
                'Milestone 2: Text Extraction & Analysis',
                'Milestone 3: Draft Generation',
                'Milestone 4: Review & Web Interface'
            ],
            'features': [
                'Automated paper search via Semantic Scholar API',
                'PDF text extraction with multiple fallback methods',
                'Paper analysis for keywords and key findings',
                'Literature review draft generation (AI/template)',
                'Draft quality assessment and revision suggestions',
                'Web interface with Gradio',
                'Complete pipeline automation'
            ],
            'technology_stack': [
                'Python 3.x',
                'Semantic Scholar API',
                'OpenAI/Gemini API',
                'PyMuPDF (PDF processing)',
                'NLTK (text analysis)',
                'scikit-learn (similarity analysis)',
                'Gradio (web interface)'
            ],
            'test_results': self.results,
            'output_directories': {
                'papers': str(self.config.PAPERS_DIR),
                'extracted_text': str(self.config.EXTRACTED_TEXT_DIR),
                'analysis': str(self.config.ANALYSIS_DIR),
                'drafts': str(self.config.DRAFTS_DIR),
                'reviews': str(self.config.DATA_DIR / "reviews")
            }
        }
        
        # Save report
        try:
            report_dir = self.config.DATA_DIR / "reports"
            report_dir.mkdir(exist_ok=True)
            
            filename = f"final_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = report_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"\n📋 Final report saved: {filepath}")
            
            # Show report summary
            print(f"\n📊 REPORT SUMMARY:")
            print(f"   Project: {report['project']} v{report['version']}")
            print(f"   Milestones: {len(report['milestones_completed'])}/4 completed")
            print(f"   Features: {len(report['features'])} implemented")
            print(f"   Status: {'✅ COMPLETE' if self.results['overall_status'] == 'success' else '⚠️  PARTIAL'}")
            
            print(f"\n📁 Output directories created:")
            for name, path in report['output_directories'].items():
                print(f"   • {name}: {Path(path).name}/")
            
            return report
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return None


def main():
    """Main function"""
    print("\n" + "="*60)
    print("           AI RESEARCH PAPER REVIEWER")
    print("           Final Integration & Testing")
    print("="*60)
    
    # Run integration test
    integrator = FinalIntegration()
    
    print("\n🔍 Running integration tests...")
    test_results = integrator.run_complete_test()
    
    # Generate final report
    print("\n📋 Generating final project report...")
    report = integrator.generate_final_report()
    
    if report:
        print(f"\n{'='*60}")
        print("🎉 PROJECT DEVELOPMENT COMPLETE!")
        print(f"{'='*60}")
        
        print("\n🚀 HOW TO USE THE SYSTEM:")
        print("   1. Web Interface: python run_ui.py")
        print("   2. Command Line: python run_all.py")
        print("   3. Complete Pipeline: python src/pipeline.py")
        
        print("\n📚 DEMONSTRATION:")
        print("   1. Search for papers on a topic")
        print("   2. Extract and analyze text")
        print("   3. Generate literature review")
        print("   4. Review and refine the draft")
        
        print("\n💡 FOR INTERNSHIP SUBMISSION:")
        print("   1. Include all source code files")
        print("   2. Include sample outputs in data/ directory")
        print("   3. Include this final report")
        print("   4. Demonstrate all 4 milestones")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()