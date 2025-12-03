import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(ROOT_DIR)

import streamlit as st
from pathlib import Path
from src.retriever.retriever import Retriever
from src.rag.generator import answer_query
import os
st.set_page_config(page_title="Multi-Modal RAG Demo", layout="wide")

st.title("Multi-Modal RAG — Demo")
st.markdown("Upload a PDF, build the index (run the builder script), then ask questions. Results include page citations.")

DOCS_DIR = Path("data/docs")
DOCS_DIR.mkdir(parents=True, exist_ok=True)

uploaded = st.file_uploader("Upload PDF (or drop the provided Qatar PDF)", type=["pdf"])
if uploaded:
    save_path = DOCS_DIR / uploaded.name
    with open(save_path, "wb") as f:
        f.write(uploaded.read())
    st.success(f"Saved to {save_path}")
    st.info("Now run `python -m src.index.build_index data/docs/yourfile.pdf` in a terminal to build index.")

query = st.text_input("Ask a question about the uploaded document")
col1, col2 = st.columns([1,1])
with col1:
    topk = st.number_input("Top-k retrieval", min_value=1, max_value=10, value=5)
with col2:
    if st.button("Get Answer") and query.strip():
        retriever = Retriever()
        ans = answer_query(query, retriever, topk=topk)
        st.markdown("### Answer")
        st.write(ans)
        st.markdown("---")
        st.markdown("### Debug: Top retrieved chunks")
        hits = retriever.retrieve(query, topk=topk)
        for i,h in enumerate(hits):
            meta = h["meta"]
            st.write(f"**Rank {i+1}** — page {meta.get('page')} | type: {meta.get('type')} | score: {h.get('score'):.4f}")
            st.write(h["text"][:500] + ("..." if len(h["text"])>500 else ""))
