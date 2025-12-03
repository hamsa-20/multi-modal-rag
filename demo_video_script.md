# Demo video script (3-5 minutes) — follow these steps

1. Intro (10s)
   - "Hi, I'm Hamsa. This demo shows the Multi-Modal RAG submission for the AI/ML intern assignment."

2. Folder overview (20s)
   - Show repo root, `data/docs/qatar_test_doc.pdf`, `data/index/`, `src/`, `report/technical_report.pdf`.

3. Installation & index build (40s)
   - Show `.env` with OPENAI_API_KEY blank (if used).
   - Terminal: `python -m venv .venv` -> `pip install -r requirements.txt`.
   - Run: `python -m src.index.build_index data/docs/qatar_test_doc.pdf` and show logs that index is built.

4. Streamlit UI demo (60-90s)
   - Start UI: `streamlit run src/ui/app.py`.
   - Ask 2 demo questions:
     - Example Q1: "What is the projected GDP growth in 2024–25?" — show answer with `[page X]`.
     - Example Q2: "Show the content of table in section X" — show retrieval of table text & citation.
   - Open debug pane to show retrieved chunks and page numbers.

5. Explain evaluation (20s)
   - Show `src/eval/evaluate.py` with small bench and sample output metrics (recall & match).

6. Wrap-up & deliverables (10s)
   - "All source, index, report, and demo video are in the Google Drive folder. Thank you."

Optional:
- Mention any known issues (table extraction, OCR on low-res scanned pages) and how to improve.
