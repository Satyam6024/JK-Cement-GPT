from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

class EmbeddingModel:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    
    def encode_texts(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, convert_to_numpy=True)
    
    def encode_single(self, text: str) -> np.ndarray:
        return self.model.encode([text], convert_to_numpy=True)[0]
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        emb1 = self.encode_single(text1)
        emb2 = self.encode_single(text2)
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))