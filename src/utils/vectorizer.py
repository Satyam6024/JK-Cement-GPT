import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

class VectorDatabase:
    def __init__(self, persist_directory: str = "./vector_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection = self.client.get_or_create_collection("data_chunks")
    
    def add_documents(self, texts: List[str], metadatas: List[Dict], ids: List[str]):
        embeddings = self.encoder.encode(texts).tolist()
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        query_embedding = self.encoder.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        return results
    
    def get_collection_stats(self) -> Dict[str, int]:
        return {"document_count": self.collection.count()}