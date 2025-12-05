#  Multi-Modal RAG Question Answering System  
### End-to-End Retrieval Augmented Generation with Text, OCR, Tables, and Local LLM

This project implements a complete **Multi-Modal Retrieval Augmented Generation (RAG)** system capable of extracting information from **text**, **images**, and **tables** inside PDFs and answering user queries with **page-level citations**.

The system is built according to the assignment requirements and supports:

- PDF ingestion (text + OCR + tables)
- Chunking & metadata construction
- Multimodal embeddings (text + OCR)
- FAISS vector database
- Semantic retrieval (Top-k)
- RAG generation using **local LLM (Ollama – LLaMA 3.1)**
- Interactive Streamlit UI

---

##  Features

### **1. Multi-Modal PDF Ingestion**
- Text extraction using **PyMuPDF**
- Image extraction + OCR using **Pytesseract**
- Table extraction using **Camelot/Tabula**
- Uniform metadata format:
  ```json
  {
    "page": 3,
    "type": "text / image_ocr / table",
    "text": "extracted content..."
  }
  ```

  ---
### **2. Chunking & Preprocessing

-Intelligent chunking of long text
-OCR outputs normalized
-Table text flattened
-Page numbers preserved for citations

---

3. Vector Indexing (FAISS)

-SentenceTransformer MiniLM embeddings
-FAISS index stored under:
```bash
data/index/
```
Metadata stored in JSON for fast retrieval
---

4. Retriever

-Top-k semantic search
-Cosine similarity scoring
-Returns ranked chunks with metadata

---

4. Retriever

-Top-k semantic search
-Cosine similarity scoring
-Returns ranked chunks with metadata

 ---
5. RAG Generation

-Custom prompt builder
-Merges context with citations
-Uses local LLaMA 3.1 (Ollama) for generation:
```bash
{
  "model": "llama3.1",
  "messages": [{"role": "user", "content": prompt}]
}
```
---
6. Streamlit UI

-Simple and intuitive frontend:
-Upload PDF
-Trigger index building
-Ask questions
-View top-k retrieved chunks
-View final answer with page references
Run the UI:
```bash
streamlit run src/ui/app.py
```
---

Project Structure
```bash
multi-modal-rag/
│
├── src/
│   ├── ingestion/          # PDF text, OCR, tables
│   ├── index/              # embeddings + FAISS index builder
│   ├── retriever/          # semantic search
│   ├── rag/                # prompt + LLM response
│   └── ui/                 # Streamlit frontend
│
├── data/
│   ├── docs/               # PDF files
│   └── index/              # vector index + metadata
│
├── .gitignore
├── .gitattributes          # git-lfs tracking rules
├── README.md
└── requirements.txt
```
---

Installation
1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/multi-modal-rag.git
cd multi-modal-rag
```
---

2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```
---

3. Install dependencies
```bash
pip install -r requirements.txt
```
---

4. Install OCR tools

-Install Tesseract OCR
-Windows users: https://github.com/UB-Mannheim/tesseract/wiki

---
Local LLM Setup (Ollama)

Install Ollama:
```bash
https://ollama.com/download
```
Pull model:
```bash
ollama pull llama3.1
```
---
Verify:
```bash
ollama run llama3.1
```
---

Build Index
```bash
python -m src.index.build_index data/docs/yourfile.pdf
```

This generates:
```bash
data/index/embeddings.faiss
data/index/meta.json
```
---

Start the Application
```bash
streamlit run src/ui/app.py
```
Upload a PDF → Ask questions → View citations.
---

##Evaluation

Evaluation scripts include:
recall@k
retrieval accuracy
example Q&A
chunk inspection
(If not included yet, they will be added.)

---

##Technical Report

A detailed multi-page technical report is attached separately, describing:
architecture
multimodal ingestion
embedding strategy
FAISS indexing
retrieval mechanism
RAG prompt design
evaluation metrics
