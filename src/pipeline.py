"""
pipeline.py
Complete pipeline for Milestones 1-3
Runs search → extraction → analysis → draft generation in sequence
"""

import time
from datetime import datetime
from pathlib import Path
import sys
import os

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from src.config import Config
    from src.paper_search import PaperSearchSystem
    from src.text_extraction import TextExtractor
    from src.paper_analyzer import PaperAnalyzer
    from src.draft_generator import DraftGenerator
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Trying alternative import...")
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from src.config import Config
    from src.paper_search import PaperSearchSystem
    from src.text_extraction import TextExtractor
    from src.paper_analyzer import PaperAnalyzer
    from src.draft_generator import DraftGenerator


class ResearchPipeline:
    """Complete research paper review pipeline"""
    
    def __init__(self, openai_api_key=None):
        """Initialize pipeline"""
        self.openai_key = openai_api_key
        self.topic = None
        self.start_time = None
        self.end_time = None
        self.results = {
            'topic': None,
            'start_time': None,
            'end_time': None,
            'duration': None,
            'milestones': {}
        }
        
        # Initialize modules
        self.searcher = PaperSearchSystem()
        self.extractor = TextExtractor()
        self.analyzer = PaperAnalyzer()
        self.generator = DraftGenerator(openai_api_key)
    
    def run_milestone1(self, topic):
        """Run Milestone 1: Search and download papers"""
        print(f"\n{'='*60}")
        print(f"🎯 MILESTONE 1: PAPER SEARCH & DOWNLOAD")
        print(f"{'='*60}")
        
        milestone_start = datetime.now()
        
        # Search for papers
        print("\n🔍 Searching for papers...")
        papers = self.searcher.search_papers(topic)
        
        if not papers:
            print("❌ No papers found. Try a different topic.")
            self.results['milestones']['milestone1'] = {
                'success': False,
                'completed': datetime.now().isoformat(),
                'error': 'No papers found'
            }
            return False
        
        print(f"✅ Found {len(papers)} papers with PDFs")
        
        # Download papers
        print("\n📥 Downloading papers...")
        downloaded_papers = self.searcher.download_papers(papers)
        
        if not downloaded_papers:
            print("❌ No PDFs downloaded.")
            self.results['milestones']['milestone1'] = {
                'success': False,
                'completed': datetime.now().isoformat(),
                'error': 'No PDFs downloaded'
            }
            return False
        
        print(f"✅ Downloaded {len(downloaded_papers)} PDFs")
        
        # Save dataset
        self.searcher.create_dataset(downloaded_papers)
        
        # Check results
        pdf_count = self.searcher.check_results()
        
        milestone_end = datetime.now()
        duration = (milestone_end - milestone_start).total_seconds()
        
        self.results['milestones']['milestone1'] = {
            'success': True,
            'completed': milestone_end.isoformat(),
            'duration_seconds': duration,
            'papers_found': len(papers),
            'papers_downloaded': len(downloaded_papers),
            'pdf_files': pdf_count
        }
        
        print(f"✅ Milestone 1 complete in {duration:.1f} seconds")
        return True
    
    def run_milestone2(self):
        """Run Milestone 2: Text extraction and analysis"""
        print(f"\n{'='*60}")
        print(f"🎯 MILESTONE 2: TEXT EXTRACTION & ANALYSIS")
        print(f"{'='*60}")
        
        milestone_start = datetime.now()
        
        # Check if we have PDFs
        pdf_files = list(Config.PAPERS_DIR.glob("*.pdf"))
        if not pdf_files:
            print("❌ No PDFs found. Run Milestone 1 first.")
            self.results['milestones']['milestone2'] = {
                'success': False,
                'completed': datetime.now().isoformat(),
                'error': 'No PDFs found'
            }
            return False
        
        print(f"📚 Found {len(pdf_files)} PDF files")
        
        # Extract text from PDFs
        print("\n📖 Extracting text from PDFs...")
        extracted_papers = self.extractor.process_all_papers()
        
        if not extracted_papers:
            print("❌ No text extracted from PDFs.")
            
            # Try to extract at least one
            for pdf_file in pdf_files[:1]:
                print(f"⚠️  Trying single paper extraction: {pdf_file.name}")
                extracted = self.extractor.extract_text(pdf_file)
                if extracted:
                    sections = self.extractor.segment_into_sections(extracted)
                    extracted['sections'] = sections
                    saved_path = self.extractor.save_extracted_text(extracted, pdf_file.stem)
                    if saved_path:
                        extracted_papers = [extracted]
                        break
            
            if not extracted_papers:
                self.results['milestones']['milestone2'] = {
                    'success': False,
                    'completed': datetime.now().isoformat(),
                    'error': 'Text extraction failed'
                }
                return False
        
        print(f"✅ Extracted text from {len(extracted_papers)} papers")
        
        # Analyze papers
        print("\n🔬 Analyzing papers...")
        analyses = self.analyzer.run_complete_analysis()
        
        if not analyses:
            print("⚠️  No analyses generated, creating basic analysis...")
            # Create basic analysis entries
            analyses = []
            for extracted in extracted_papers:
                basic_analysis = {
                    'file_name': extracted.get('file_name', 'unknown'),
                    'total_pages': extracted.get('total_pages', 0),
                    'total_words': extracted.get('total_words', 0),
                    'analysis_date': datetime.now().isoformat(),
                    'keywords': ['research', 'study', 'analysis']
                }
                analyses.append(basic_analysis)
        
        print(f"✅ Analyzed {len(analyses)} papers")
        
        milestone_end = datetime.now()
        duration = (milestone_end - milestone_start).total_seconds()
        
        self.results['milestones']['milestone2'] = {
            'success': True,
            'completed': milestone_end.isoformat(),
            'duration_seconds': duration,
            'papers_extracted': len(extracted_papers),
            'papers_analyzed': len(analyses)
        }
        
        print(f"✅ Milestone 2 complete in {duration:.1f} seconds")
        return True
    
    def run_milestone3(self, topic):
        """Run Milestone 3: Draft generation"""
        print(f"\n{'='*60}")
        print(f"🎯 MILESTONE 3: DRAFT GENERATION")
        print(f"{'='*60}")
        
        milestone_start = datetime.now()
        
        # Generate draft
        print("\n📝 Generating literature review draft...")
        draft_result = self.generator.create_complete_draft(topic)
        
        if not draft_result:
            print("❌ Draft generation failed.")
            self.results['milestones']['milestone3'] = {
                'success': False,
                'completed': datetime.now().isoformat(),
                'error': 'Draft generation failed'
            }
            return False
        
        milestone_end = datetime.now()
        duration = (milestone_end - milestone_start).total_seconds()
        
        self.results['milestones']['milestone3'] = {
            'success': True,
            'completed': milestone_end.isoformat(),
            'duration_seconds': duration,
            'draft_file': draft_result.get('file_path'),
            'papers_reviewed': draft_result.get('papers_reviewed', 0),
            'is_ai_generated': draft_result.get('is_ai_generated', False)
        }
        
        print(f"✅ Milestone 3 complete in {duration:.1f} seconds")
        return True
    
    def run_complete_pipeline(self, topic, openai_api_key=None):
        """Run complete pipeline from search to draft generation"""
        self.start_time = datetime.now()
        self.topic = topic
        
        print(f"\n{'='*60}")
        print(f"🚀 STARTING COMPLETE RESEARCH PIPELINE")
        print(f"📝 Topic: {topic}")
        print(f"⏰ Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # Setup results
        self.results = {
            'topic': topic,
            'start_time': self.start_time.isoformat(),
            'milestones': {},
            'system_version': '1.0.0'
        }
        
        # Update API key if provided
        if openai_api_key:
            self.openai_key = openai_api_key
            self.generator = DraftGenerator(openai_api_key=openai_api_key)
        
        # Milestone 1
        if not self.run_milestone1(topic):
            self.end_time = datetime.now()
            self.results['end_time'] = self.end_time.isoformat()
            self.results['duration_seconds'] = (self.end_time - self.start_time).total_seconds()
            self.save_pipeline_results()
            return self.results
        
        # Small delay between milestones
        time.sleep(1)
        
        # Milestone 2
        if not self.run_milestone2():
            self.end_time = datetime.now()
            self.results['end_time'] = self.end_time.isoformat()
            self.results['duration_seconds'] = (self.end_time - self.start_time).total_seconds()
            self.save_pipeline_results()
            return self.results
        
        # Small delay between milestones
        time.sleep(1)
        
        # Milestone 3
        if not self.run_milestone3(topic):
            self.end_time = datetime.now()
            self.results['end_time'] = self.end_time.isoformat()
            self.results['duration_seconds'] = (self.end_time - self.start_time).total_seconds()
            self.save_pipeline_results()
            return self.results
        
        # Pipeline complete
        self.end_time = datetime.now()
        total_duration = (self.end_time - self.start_time).total_seconds()
        
        self.results['end_time'] = self.end_time.isoformat()
        self.results['duration_seconds'] = total_duration
        self.results['success'] = True
        
        self.save_pipeline_results()
        self.print_final_summary()
        
        return self.results
    
    def save_pipeline_results(self):
        """Save pipeline results to JSON file"""
        try:
            results_file = Config.DATA_DIR / "pipeline_results.json"
            
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Pipeline results saved: {results_file.name}")
            
        except Exception as e:
            print(f"⚠️  Error saving pipeline results: {e}")
    
    def print_final_summary(self):
        """Print final summary of the pipeline"""
        print(f"\n{'='*60}")
        print(f"🎉 PIPELINE COMPLETE!")
        print(f"{'='*60}")
        
        total_duration = self.results.get('duration_seconds', 0)
        
        print(f"\n📊 SUMMARY:")
        print(f"   📝 Topic: {self.results.get('topic', 'Unknown')}")
        print(f"   ⏰ Total duration: {total_duration:.1f} seconds")
        print(f"   🎯 Milestones completed: 3/3")
        
        # Milestone details
        for milestone, data in self.results.get('milestones', {}).items():
            status = "✅ SUCCESS" if data.get('success') else "❌ FAILED"
            duration = data.get('duration_seconds', 0)
            print(f"\n   {milestone.upper()}:")
            print(f"      Status: {status}")
            print(f"      Duration: {duration:.1f}s")
            
            # Add milestone-specific details
            if milestone == 'milestone1':
                print(f"      Papers downloaded: {data.get('papers_downloaded', 0)}")
            elif milestone == 'milestone2':
                print(f"      Papers analyzed: {data.get('papers_analyzed', 0)}")
            elif milestone == 'milestone3':
                draft_file = data.get('draft_file', '')
                if draft_file:
                    print(f"      Draft: {Path(draft_file).name}")
                print(f"      AI Generated: {'Yes' if data.get('is_ai_generated') else 'No (Template)'}")
        
        print(f"\n📁 OUTPUT DIRECTORIES:")
        print(f"   📄 PDFs: {Config.PAPERS_DIR}")
        print(f"   📝 Extracted text: {Config.EXTRACTED_TEXT_DIR}")
        print(f"   🔬 Analysis: {Config.ANALYSIS_DIR}")
        print(f"   ✍️  Drafts: {Config.DRAFTS_DIR}")
        print(f"   📊 Pipeline results: {Config.DATA_DIR}/pipeline_results.json")
        
        print(f"\n💡 NEXT STEPS:")
        print(f"   1. Review the generated draft in drafts/ folder")
        print(f"   2. Edit and refine as needed")
        print(f"   3. Add proper citations and references")
        print(f"   4. Format according to your requirements")
        
        print(f"\n{'='*60}")


def main():
    """Run the complete pipeline"""
    print("\n" + "="*60)
    print("           COMPLETE RESEARCH PIPELINE")
    print("           Milestones 1-3 Integration")
    print("="*60)
    
    # Get topic
    topic = input("\n🔎 Enter research topic: ").strip()
    
    if not topic:
        print("❌ Please enter a topic")
        print("\n💡 Example topics:")
        print("   • machine learning in healthcare")
        print("   • deep learning for medical imaging")
        print("   • natural language processing applications")
        print("   • blockchain technology adoption")
        print("   • renewable energy systems")
        return
    
    # Get OpenAI API key
    openai_key = None
    if Config.OPENAI_API_KEY:
        openai_key = Config.OPENAI_API_KEY
        print(f"\n✅ Using OpenAI API key from .env file")
    else:
        print("\n⚠️  OpenAI API key not found in .env file")
        use_ai = input("   Use AI for draft generation? (y/n): ").strip().lower()
        if use_ai == 'y':
            openai_key = input("   🔑 Enter OpenAI API key: ").strip()
            if not openai_key:
                print("   ❌ No API key entered, will use template mode")
        else:
            print("   📝 Will use template mode for draft generation")
    
    # Run pipeline
    pipeline = ResearchPipeline(openai_api_key=openai_key)
    
    try:
        results = pipeline.run_complete_pipeline(topic, openai_key)
        
        # Show final status
        success_count = sum(1 for m in results.get('milestones', {}).values() if m.get('success'))
        total_milestones = len(results.get('milestones', {}))
        
        print(f"\n📈 PIPELINE STATUS: {success_count}/{total_milestones} milestones completed")
        
        if success_count == total_milestones:
            print("🎉 ALL MILESTONES COMPLETED SUCCESSFULLY!")
        elif success_count > 0:
            print("⚠️  Pipeline partially completed")
        else:
            print("❌ Pipeline failed")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user")
    except Exception as e:
        print(f"\n❌ Pipeline error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check internet connection")
        print("   2. Verify API keys in .env file")
        print("   3. Try a different research topic")
        print("   4. Check available disk space")
    
    print("\n" + "="*60)


# Import json for pipeline results
import json

if __name__ == "__main__":
    main()