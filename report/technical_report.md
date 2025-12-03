# Multi-Modal RAG — Technical Report

## 1. Summary (30 words)
An end-to-end Multi-Modal Retrieval-Augmented Generation (RAG) system that ingests PDFs (text, images, tables), extracts OCR and tables, indexes semantically with FAISS, and answers queries with page-level citations.

## 2. Architecture (diagram + components)
- Ingestion: pymupdf for text & images, pytesseract for OCR, camelot/pdfplumber for tables.
- Processing: paragraph-based chunking; embeddings via sentence-transformers.
- Indexing: FAISS (IndexFlatL2) storing embeddings + chunk text + metadata.
- Retrieval: semantic nearest-neighbor search (top-k).
- Generation: prompt-based RAG using retrieved contexts; OpenAI optional.
- UI: Streamlit demo for upload, query, and debug view.

## 3. Implementation details
- Chunking: paragraph split with 2000-char limit to keep context size reasonable.
- Embeddings: `all-MiniLM-L6-v2` (384 dim) for CPU-speed semantic retrieval.
- Citation: each chunk metadata contains `page`, `type` (text/image/table) enabling citation `[page X]`.

## 4. Evaluation methodology
- Retrieval: recall@k measured with a small benchmark CSV of question -> correct page.
- Answering: faithfulness check via keyword-match & manual spot-check.
- Latency: measure end-to-end time for retrieval + generation (log in eval script).

## 5. Limitations & improvements
- OCR quality depends on scanned resolution; pre-processing (binarization) helps.
- Table extraction reliability varies; consider manual table normalization.
- For production: use hybrid search (FAISS + BM25) and larger LLMs or on-prem LLM.

## 6. Reproducibility
- Steps to reproduce are in README. Index stored in `data/index/`.
