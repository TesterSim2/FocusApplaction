"""Certainty Determination System"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class CertaintyAnalyzer:
    """Analyzes certainty and helpfulness of prompts/responses"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.knowledge_base = self._initialize_knowledge_base()
        
    def analyze(self, text: str, context: Optional[List[str]] = None) -> Dict:
        """Analyze certainty of a given text"""
        # Calculate various certainty metrics
        clarity_score = self._calculate_clarity(text)
        specificity_score = self._calculate_specificity(text)
        context_relevance = self._calculate_context_relevance(text, context) if context else 1.0
        
        # Combined certainty score
        certainty_score = np.mean([clarity_score, specificity_score, context_relevance])
        
        # Determine if helpful or harmful
        helpful_probability = self._calculate_helpful_probability(text, certainty_score)
        
        # Identify potential issues
        issues = self._identify_issues(text, certainty_score)
        
        return {
            'score': certainty_score,
            'clarity': clarity_score,
            'specificity': specificity_score,
            'context_relevance': context_relevance,
            'helpful_probability': helpful_probability,
            'potential_issues': issues,
            'recommendation': self._generate_recommendation(certainty_score, issues)
        }
    
    def _calculate_clarity(self, text: str) -> float:
        """Calculate clarity score based on text structure"""
        # Factors: sentence length, word complexity, structure
        sentences = text.split('.')
        avg_sentence_length = np.mean([len(s.split()) for s in sentences if s])
        
        # Optimal sentence length is 15-20 words
        if 15 <= avg_sentence_length <= 20:
            clarity = 1.0
        else:
            clarity = max(0, 1 - abs(avg_sentence_length - 17.5) / 17.5)
        
        return clarity
    
    def _calculate_specificity(self, text: str) -> float:
        """Calculate how specific the text is"""
        # Check for vague terms
        vague_terms = ['thing', 'stuff', 'something', 'whatever', 'maybe', 'probably']
        specific_terms = ['specifically', 'exactly', 'precisely', 'particularly']
        
        text_lower = text.lower()
        vague_count = sum(1 for term in vague_terms if term in text_lower)
        specific_count = sum(1 for term in specific_terms if term in text_lower)
        
        # Calculate score
        total_words = len(text.split())
        specificity = min(1.0, (specific_count * 2 - vague_count) / max(total_words * 0.1, 1))
        
        return max(0, specificity)
    
    def _calculate_helpful_probability(self, text: str, certainty_score: float) -> float:
        """Calculate probability that the text will be helpful"""
        base_probability = certainty_score
        
        # Adjust based on text characteristics
        if '?' in text:  # Questions can be helpful for clarification
            base_probability *= 1.1
        
        if len(text) < 10:  # Very short texts might lack context
            base_probability *= 0.8
        
        return min(1.0, base_probability)
    
    def _identify_issues(self, text: str, certainty_score: float) -> List[str]:
        """Identify potential issues with the text"""
        issues = []
        
        if certainty_score < 0.3:
            issues.append("Very low clarity")
        
        if len(text) < 10:
            issues.append("Too brief")
        
        if len(text) > 1000:
            issues.append("Potentially too verbose")
        
        if text.count('?') > 3:
            issues.append("Multiple questions may dilute focus")
        
        return issues
    
    def _generate_recommendation(self, score: float, issues: List[str]) -> str:
        """Generate recommendation based on analysis"""
        if score > 0.8:
            return "High certainty - proceed with response"
        elif score > 0.5:
            return "Moderate certainty - consider clarifying specific aspects"
        else:
            return f"Low certainty - recommend addressing: {', '.join(issues)}"
    
    def _calculate_context_relevance(self, text: str, context: List[str]) -> float:
        """Calculate relevance of text to provided context"""
        try:
            corpus = context + [text]
            vectors = self.vectorizer.fit_transform(corpus)
            similarity = cosine_similarity(vectors[-1], vectors[:-1])
            return float(np.max(similarity))
        except Exception:
            return 1.0
    
    def _initialize_knowledge_base(self) -> List[str]:
        """Initialize a small knowledge base for context checks"""
        return []
