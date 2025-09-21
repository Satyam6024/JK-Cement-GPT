import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import pickle
import os

class VectorDatabase:
    def __init__(self, persist_directory: str = "./vector_db"):
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Simple in-memory storage
        self.documents = []
        self.metadatas = []
        self.ids = []
        self.embeddings = []
        
        # Try to load existing data
        self._load_data()
    
    def add_documents(self, texts: List[str], metadatas: List[Dict], ids: List[str]):
        embeddings = self.encoder.encode(texts, convert_to_numpy=True)
        
        self.documents.extend(texts)
        self.metadatas.extend(metadatas)
        self.ids.extend(ids)
        self.embeddings.extend(embeddings)
        
        self._save_data()
    
    def search(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        if not self.embeddings:
            return {'documents': [], 'metadatas': [], 'distances': []}
        
        query_embedding = self.encoder.encode([query], convert_to_numpy=True)
        
        # Calculate cosine similarities
        similarities = []
        for emb in self.embeddings:
            sim = np.dot(query_embedding[0], emb) / (np.linalg.norm(query_embedding[0]) * np.linalg.norm(emb))
            similarities.append(sim)
        
        # Get top results
        top_indices = np.argsort(similarities)[-n_results:][::-1]
        
        results = {
            'documents': [self.documents[i] for i in top_indices],
            'metadatas': [self.metadatas[i] for i in top_indices],
            'distances': [[1 - similarities[i] for i in top_indices]]  # Convert to distances
        }
        
        return results
    
    def get_collection_stats(self) -> Dict[str, int]:
        return {"document_count": len(self.documents)}
    
    def _save_data(self):
        data = {
            'documents': self.documents,
            'metadatas': self.metadatas,
            'ids': self.ids,
            'embeddings': self.embeddings
        }
        
        with open(os.path.join(self.persist_directory, 'data.pkl'), 'wb') as f:
            pickle.dump(data, f)
    
    def _load_data(self):
        data_path = os.path.join(self.persist_directory, 'data.pkl')
        if os.path.exists(data_path):
            try:
                with open(data_path, 'rb') as f:
                    data = pickle.load(f)
                
                self.documents = data.get('documents', [])
                self.metadatas = data.get('metadatas', [])
                self.ids = data.get('ids', [])
                self.embeddings = data.get('embeddings', [])
            except:
                # If loading fails, start fresh
                pass