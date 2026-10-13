"""Analyzer for sentence length variance."""

import re
import statistics


class SentenceVarianceScorer:
    """
    Measures variation in sentence lengths.
    
    Human writing typically has more varied sentence lengths
    than AI-generated text.
    """
    
    def analyze(self, text: str) -> dict:
        """
        Analyze sentence length variance.
        
        Args:
            text: Text to analyze
            
        Returns:
            dict with variance metrics
        """
        # Split on sentence boundaries
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 2:
            return {
                "variance": 0.0,
                "mean_length": len(sentences[0].split()) if sentences else 0,
                "lengths": [],
                "shortest": 0,
                "longest": 0,
                "range": 0,
                "issue": "too_few_sentences",
            }
        
        lengths = [len(s.split()) for s in sentences]
        
        variance = statistics.stdev(lengths)
        mean_length = statistics.mean(lengths)
        
        return {
            "variance": variance,
            "mean_length": mean_length,
            "lengths": lengths,
            "shortest": min(lengths),
            "longest": max(lengths),
            "range": max(lengths) - min(lengths),
            "sentence_count": len(sentences),
        }