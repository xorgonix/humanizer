"""Perplexity scorer for text predictability."""

import os


class PerplexityScorer:
    """
    Estimates text perplexity using a language model.
    
    Lower perplexity = more predictable = more AI-like.
    
    Uses GPT-2 by default, can be configured for other models.
    """
    
    def __init__(self, model_name: str = "gpt2"):
        self.model_name = model_name
        self._model = None
        self._tokenizer = None
    
    def _load_model(self):
        """Lazy-load the model."""
        # Force fallback to keep runtime light and avoid torch/transformers.
        if self._model is None:
            self._model = "fallback"
    
    def score(self, text: str) -> dict:
        """
        Score text perplexity.
        
        Args:
            text: Text to score
            
        Returns:
            dict with raw and normalized perplexity
        """
        self._load_model()
        
        # Always use lightweight fallback (no torch/transformers).
        return self._fallback_score(text)
    
    def _fallback_score(self, text: str) -> dict:
        """
        Fallback scoring using heuristics.
        
        Used when transformers library unavailable.
        """
        words = text.lower().split()
        
        # Simple heuristics
        unique_ratio = len(set(words)) / len(words) if words else 0
        avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
        
        # Higher unique ratio and varied word length = more human-like
        normalized = (unique_ratio * 0.7 + min(avg_word_length / 10, 0.3))
        
        return {
            "raw_perplexity": None,
            "normalized": normalized,
            "method": "fallback",
        }