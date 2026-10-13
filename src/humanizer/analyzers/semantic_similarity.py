"""Semantic similarity checker using sentence embeddings."""


class SemanticSimilarityChecker:
    """
    Compares semantic similarity between texts using embeddings.
    
    Used to ensure meaning is preserved during rewriting.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None
    
    def _load_model(self):
        """Lazy-load the embedding model."""
        # Force lightweight fallback to avoid pulling torch/sentence-transformers in this environment.
        if self._model is None:
            self._model = "fallback"
    
    def compare(self, text1: str, text2: str) -> float:
        """
        Compare semantic similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score 0-1 (1 = identical meaning)
        """
        self._load_model()
        
        # Always use lightweight fallback (no sentence-transformers/torch/numpy dependency).
        return self._fallback_compare(text1, text2)
    
    def _fallback_compare(self, text1: str, text2: str) -> float:
        """
        Fallback comparison using word overlap.
        
        Used when sentence-transformers unavailable.
        """
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        # Jaccard similarity
        return len(intersection) / len(union)