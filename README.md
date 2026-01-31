# 📘 AI System to Automatically Review and Summarize Research Papers

An intelligent system designed to automate the process of collecting, organizing, and preparing academic research papers for literature review and analysis.

This project simplifies early-stage research by automatically searching scholarly databases, downloading papers, and generating a structured dataset ready for further AI-based analysis.

---

## 🚀 Project Overview

The **AI Research Paper Reviewer** helps researchers, students, and developers reduce manual effort involved in:

- Searching academic papers  
- Collecting metadata  
- Downloading PDFs  
- Preparing clean datasets  

The system is modular and scalable, allowing easy extension for PDF analysis, summarization, and review generation.

---

## ✨ Features

- 🔍 Topic-based academic paper search  
- 🌐 Integration with **Semantic Scholar API**  
- 📄 Automatic retrieval of:
  - Title
  - Authors
  - Publication year
  - Abstract
- 📥 PDF download (when available)
- 🗂 Structured dataset creation in JSON format
- 🧱 Clean and modular project architecture

---

## 🔄 Workflow

User Topic Input
↓
Semantic Scholar API Search
↓
Paper Metadata Collection
↓
Top-N Paper Selection
↓
PDF Download
↓
Dataset Preparation (JSON)


---

## 📁 Project Structure

AI-System-to-automatically-Review-and-Summarize-Research-Papers/
│
├── data/
│ ├── papers/ # Downloaded research PDFs
│ ├── metadata/
│ │ └── papers_metadata.json
│ └── dataset.json # Final prepared dataset
│
├── src/
│ ├── init.py
│ ├── config.py # API keys and configuration
│ ├── paper_search.py # Semantic Scholar search logic
│ └── utils.py # Helper utility functions
│
├── .gitignore
├── requirements.txt
└── README.md


---

## ⚙️ Technology Stack

**Language**
- Python 3.x

**API**
- Semantic Scholar API

**Libraries**
- requests  
- json  
- pathlib  
- tqdm  
- python-dotenv (optional)

---

## 🔧 Setup Instructions

### 1️⃣ Install Python

Ensure Python 3.8 or higher is installed:

```bash
python --version
2️⃣ Clone the Repository
git clone https://github.com/your-username/AI-System-to-automatically-Review-and-Summarize-Research-Papers.git
cd AI-System-to-automatically-Review-and-Summarize-Research-Papers
3️⃣ Create Virtual Environment (Recommended)
python -m venv venv
Activate:

Windows

venv\Scripts\activate
macOS / Linux

source venv/bin/activate
4️⃣ Install Dependencies
pip install -r requirements.txt
5️⃣ Configure API Key
Edit:

src/config.py
Add your Semantic Scholar API key:

SEMANTIC_SCHOLAR_API_KEY = "your_api_key_here"
⚠️ Never upload API keys to GitHub.

▶️ How to Run
python src/paper_search.py
📤 Generated Outputs
File / Folder	Description
papers_metadata.json	Metadata of collected papers
dataset.json	Structured dataset for analysis
data/papers/	Downloaded research PDFs
📊 Sample Dataset Format
{
  "paper_id": "123456",
  "title": "Artificial Intelligence in Healthcare",
  "authors": ["Author A", "Author B"],
  "year": 2023,
  "abstract": "...",
  "pdf_url": "...",
  "local_pdf_path": "data/papers/ai_healthcare.pdf"
}
🔮 Future Enhancements
PDF text extraction

Section-wise segmentation

Key finding identification

Cross-paper comparison

Automated summarization

Review and draft generation

📜 License
This project is intended for educational and research purposes only.