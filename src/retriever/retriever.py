from src.embeddings.embedder import Embedder
from src.index.faiss_store import FaissStore
import os
import numpy as np

class Retriever:
    def __init__(self, index_dir="data/index"):
        self.embedder = Embedder()
        # load dim from env or default 384
        dim = int(os.getenv("TEXT_EMBED_DIM", "384"))
        self.store = FaissStore(dim=dim, index_dir=index_dir)
        self.store.load()

    def retrieve(self, query, topk=5):
        q_emb = self.embedder.embed_texts([query]).astype(np.float32)
        hits = self.store.search(q_emb, k=topk)
        return hits
