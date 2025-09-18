from typing import Dict, Any, List
from src.models.rag_model import RAGModel

class AnalysisPipeline:
    def __init__(self):
        self.rag_model = RAGModel()
        
    def perform_analysis(self, query: str, analysis_type: str = 'general') -> Dict[str, Any]:
        rag_response = self.rag_model.query(query)
        
        if analysis_type == 'statistical':
            return self._statistical_analysis(query, rag_response)
        elif analysis_type == 'trend':
            return self._trend_analysis(query, rag_response)
        elif analysis_type == 'comparative':
            return self._comparative_analysis(query, rag_response)
        else:
            return self._general_analysis(query, rag_response)
    
    def _statistical_analysis(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'type': 'statistical',
            'analysis': context['answer'],
            'confidence': context['confidence']
        }
    
    def _trend_analysis(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'type': 'trend',
            'analysis': context['answer'],
            'trends': self._identify_trends(context['context'])
        }
    
    def _comparative_analysis(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'type': 'comparative',
            'analysis': context['answer'],
            'comparisons': self._extract_comparisons(context['context'])
        }
    
    def _general_analysis(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'type': 'general',
            'analysis': context['answer'],
            'sources': context['sources']
        }
    
    def _identify_trends(self, context: str) -> List[str]:
        trend_keywords = ['increase', 'decrease', 'growth', 'decline']
        trends = []
        for keyword in trend_keywords:
            if keyword in context.lower():
                trends.append(f"Trend detected: {keyword}")
        return trends
    
    def _extract_comparisons(self, context: str) -> List[str]:
        comparison_words = ['higher', 'lower', 'better', 'worse']
        comparisons = []
        for word in comparison_words:
            if word in context.lower():
                comparisons.append(f"Comparison found: {word}")
        return comparisons