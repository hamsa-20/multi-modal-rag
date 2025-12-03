from sentence_transformers import SentenceTransformer
import os

MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(MODEL)

    def embed_texts(self, texts):
        return self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
