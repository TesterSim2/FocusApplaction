"""Prompt Processing and Enhancement System"""

import re
from typing import Dict, List, Tuple
import nltk
from textblob import TextBlob
import spacy

class PromptProcessor:
    """Advanced prompt processing capabilities"""
    
    def __init__(self):
        # Initialize NLP models
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception:
            # Fallback if spacy model not installed
            self.nlp = None
        
    def ground_prompt(self, prompt: str) -> str:
        """Ground the prompt with necessary context and prerequisites"""
        # Extract key concepts
        concepts = self._extract_concepts(prompt)
        
        # Identify prerequisites
        prerequisites = self._identify_prerequisites(concepts)
        
        # Build grounded prompt
        grounded = f"Context and Prerequisites:\n"
        for prereq in prerequisites:
            grounded += f"- {prereq}\n"
        grounded += f"\nGrounded Request: {prompt}"
        
        return grounded
    
    def enhance_prompt(self, prompt: str) -> str:
        """Enhance prompt for better AI understanding"""
        # Add clarity markers
        enhanced = prompt
        
        # Add specificity
        if "explain" in prompt.lower():
            enhanced += " Please provide a detailed explanation with examples."
        
        # Add structure requests
        if len(prompt.split()) > 20:
            enhanced += " Please structure your response with clear sections."
        
        # Add output format hints
        if any(word in prompt.lower() for word in ['list', 'steps', 'points']):
            enhanced += " Format as a numbered list."
        
        return enhanced
    
    def _extract_concepts(self, prompt: str) -> List[str]:
        """Extract key concepts from prompt"""
        if self.nlp:
            doc = self.nlp(prompt)
            concepts = [ent.text for ent in doc.ents]
            concepts.extend([token.text for token in doc if token.pos_ in ['NOUN', 'VERB']])
            return list(set(concepts))
        else:
            # Fallback: simple noun extraction
            words = prompt.split()
            return [w for w in words if len(w) > 4]
    
    def _identify_prerequisites(self, concepts: List[str]) -> List[str]:
        """Identify prerequisites for understanding concepts"""
        prerequisites = []
        
        # Knowledge domain mapping
        domain_prereqs = {
            'machine learning': ['Basic statistics', 'Linear algebra', 'Python programming'],
            'quantum': ['Physics fundamentals', 'Mathematics', 'Probability theory'],
            'blockchain': ['Cryptography basics', 'Distributed systems', 'Consensus mechanisms']
        }
        
        for concept in concepts:
            for domain, prereqs in domain_prereqs.items():
                if domain in concept.lower():
                    prerequisites.extend(prereqs)
        
        return list(set(prerequisites))
