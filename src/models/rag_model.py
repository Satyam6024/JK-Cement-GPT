from typing import List, Dict, Any
import openai
from src.utils.vectorizer import VectorDatabase
from src.data.processors import DataProcessor
from src.config.config import Config

class RAGModel:
    def __init__(self, vector_db_path: str = "./vector_db"):
        self.vector_db = VectorDatabase(vector_db_path)
        self.data_processor = DataProcessor()
        self.config = Config()
        openai.api_key = self.config.OPENAI_API_KEY
        
    def ingest_data(self, data: Any, metadata: Dict[str, Any]) -> str:
        chunks = self.data_processor.chunk_data(data)
        doc_id = metadata.get('file_id', 'unknown')
        ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
        metadatas = [metadata for _ in chunks]
        
        self.vector_db.add_documents(chunks, metadatas, ids)
        return doc_id
    
    def query(self, question: str, n_results: int = 5) -> Dict[str, Any]:
        search_results = self.vector_db.search(question, n_results)
        context = "\n".join(search_results.get('documents', []))
        
        prompt = f"""
        Data Context: {context}
        User Query: {question}
        
        Provide detailed data analysis, insights, and actionable business recommendations.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.3
        )
        
        return {
            'answer': response.choices[0].message.content,
            'context': context,
            'sources': search_results.get('metadatas', []),
            'confidence': self._calculate_confidence(search_results)
        }
    
    def generate_insights(self, file_id: str) -> Dict[str, Any]:
        results = self.vector_db.search(f"file_id:{file_id}", n_results=50)
        context = "\n".join(results.get('documents', []))
        
        insights_query = "Generate comprehensive business insights, trends, and recommendations from this data."
        insights = self.query(insights_query)
        
        return {
            'insights': insights['answer'],
            'data_summary': context[:500] + "...",
            'recommendations': self._extract_recommendations(insights['answer'])
        }
    
    def _calculate_confidence(self, search_results: Dict[str, Any]) -> float:
        distances = search_results.get('distances', [[]])[0]
        if not distances:
            return 0.0
        return max(0, 1 - min(distances))
    
    def _extract_recommendations(self, insights: str) -> List[str]:
        lines = insights.split('\n')
        recommendations = []
        for line in lines:
            if any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'should']):
                recommendations.append(line.strip())
        return recommendations[:5]