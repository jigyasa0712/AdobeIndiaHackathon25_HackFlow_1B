
# Persona-Driven Document Intelligence

## 🧠 Overview
This project extracts and analyzes the most relevant sections and sentences from a collection of PDF documents, guided by a user-defined **persona** and **job-to-be-done**. It uses **TF-IDF** and **cosine similarity** to rank and summarize content effectively.

## ✨ Features
- 📄 Extracts **top sections** from PDFs based on persona and task
- 🧮 Ranks sections and sentences by **relevance score**
- 📦 Outputs **structured JSON** with metadata, extracted sections, and sub-section analysis
- ⚡ **Runs on CPU only** with model size ≤ 1GB
- 🚀 Processes **3–5 documents in under 60 seconds**
- 🔒 **Offline capable** – no internet access required during execution

## 📥 Input
- `challenge1b_input.json`: Defines persona, job-to-be-done, and list of PDF filenames
- PDF files: All referenced PDFs must be placed in the `pdfs/` directory

## 📤 Output
- `output.json`: Structured results including metadata, selected sections, and relevant sentence analysis

## 🛠️ Usage Instructions

### Step 1: Prepare Environment
Place your input JSON and PDF files in the project directory as described.

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Script
```bash
python script.py --input challenge1b_input.json --pdf_dir pdfs --output output.json
```

## 🐳 Docker Instructions

### Step 1: Build Docker Image
```bash
docker build -t persona-doc-intel .
```

### Step 2: Run the Container
On **Windows (CMD or PowerShell)**:
```bash
docker run --rm -v %cd%:/app persona-doc-intel   python script.py --input challenge1b_input.json --pdf_dir pdfs --output output.json
```

On **Linux/Mac**:
```bash
docker run --rm -v $(pwd):/app persona-doc-intel   python script.py --input challenge1b_input.json --pdf_dir pdfs --output output.json
```

## 🧪 Sample Input/Output
- Refer to `challenge1b_input.json` for a sample input format.
- The `output.json` will follow the schema defined in the problem statement.

## ⛓️ Constraints
- ✅ Runs on **CPU only**
- 📦 Model size is **≤ 1GB**
- ⏱️ **≤ 60 seconds** processing time for 3–5 PDFs
- 🌐 **No internet access required** (offline execution supported)

---

<div align="center">

**🔍 Persona-Based PDF Summarization Engine**  
*Efficient • Offline • Relevant*

**Team HackFlow** — Crafting smart document workflows 🚀

</div>
