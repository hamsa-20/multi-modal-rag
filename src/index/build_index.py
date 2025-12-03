import sys
import numpy as np
from pathlib import Path
from src.ingestion.pdf_parser import parse_pdf
from src.embeddings.embedder import Embedder
from src.index.faiss_store import FaissStore

def chunk_text(text, max_chars=2000):
    # naive paragraph-based chunking with char limit
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    for p in paras:
        while len(p) > max_chars:
            chunks.append(p[:max_chars])
            p = p[max_chars:]
        if p:
            chunks.append(p)
    if not chunks and text.strip():
        chunks.append(text.strip())
    return chunks

def build_index(pdf_path, out_dir="data/processed"):
    pdf_path = Path(pdf_path)
    out_dir = Path(out_dir)
    pages = parse_pdf(str(pdf_path), str(out_dir))
    embedder = Embedder()
    texts = []
    metas = []
    for p in pages:
        page_no = p["page"]
        # text chunks
        t_chunks = chunk_text(p["text"] or "")
        for i, c in enumerate(t_chunks):
            metas.append({"source": str(pdf_path.name), "page": page_no, "type": "text", "chunk_id": f"p{page_no}_t{i}"})
            texts.append(c)
        # image OCR chunks
        for img_path, ocr in p["images_ocr"].items():
            metas.append({"source": str(pdf_path.name), "page": page_no, "type": "image_ocr", "image": img_path})
            texts.append(ocr or "")
        # table files
        for t in p["tables"]:
            try:
                with open(t, "r", encoding="utf-8") as f:
                    table_text = f.read()
            except Exception:
                table_text = ""
            metas.append({"source": str(pdf_path.name), "page": page_no, "type": "table", "table": t})
            texts.append(table_text)
    if not texts:
        print("No text extracted. Exiting.")
        return
    print(f"Embedding {len(texts)} chunks ...")
    embeddings = embedder.embed_texts(texts)
    dim = embeddings.shape[1]
    store = FaissStore(dim=dim)
    store.add(embeddings.astype(np.float32), metas, texts)
    print("Index built. chunks:", len(texts))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m src.index.build_index path/to/doc.pdf")
        sys.exit(1)
    build_index(sys.argv[1])
