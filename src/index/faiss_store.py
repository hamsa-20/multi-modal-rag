import faiss
import numpy as np
import json
from pathlib import Path

class FaissStore:
    def __init__(self, dim, index_dir="data/index"):
        self.dim = dim
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.index_dir / "faiss.index"
        self.meta_file = self.index_dir / "faiss.metadata.json"
        self.index = faiss.IndexFlatL2(dim)
        self.metadatas = []
        self.texts = []  # parallel list of actual chunk texts

    def add(self, embeddings, metadatas, texts):
        if embeddings.dtype != np.float32:
            embeddings = embeddings.astype('float32')
        self.index.add(embeddings)
        self.metadatas.extend(metadatas)
        self.texts.extend(texts)
        self.save()

    def search(self, q_embedding, k=5):
        if q_embedding.dtype != np.float32:
            q_embedding = q_embedding.astype('float32')
        D, I = self.index.search(q_embedding, k)
        results = []
        for i_idx, ids in enumerate(I):
            for j, idx in enumerate(ids):
                if idx == -1: continue
                results.append({
                    "meta": self.metadatas[idx],
                    "text": self.texts[idx],
                    "score": float(D[i_idx][j])
                })
        return results

    def save(self):
        faiss.write_index(self.index, str(self.index_file))
        with open(self.meta_file, "w", encoding="utf-8") as f:
            json.dump({"metadatas": self.metadatas, "texts": self.texts}, f, ensure_ascii=False, indent=2)

    def load(self):
        if self.index_file.exists() and self.meta_file.exists():
            self.index = faiss.read_index(str(self.index_file))
            import json
            with open(self.meta_file, "r", encoding="utf-8") as f:
                d = json.load(f)
                self.metadatas = d.get("metadatas", [])
                self.texts = d.get("texts", [])
