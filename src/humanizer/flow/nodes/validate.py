"""Validation node - checks semantic similarity."""

from pocketflow import Node

from humanizer.analyzers.semantic_similarity import SemanticSimilarityChecker


class ValidateNode(Node):
    """
    Check semantic similarity to original.
    
    Ensures meaning wasn't lost during rewriting.
    """
    
    def __init__(self):
        super().__init__()
        self._checker = None
    
    @property
    def checker(self) -> SemanticSimilarityChecker:
        """Lazy-load the similarity checker."""
        if self._checker is None:
            self._checker = SemanticSimilarityChecker()
        return self._checker
    
    def prep(self, shared: dict) -> dict:
        """Get texts to compare."""
        return {
            "original": shared["original_text"],
            "revised": shared["pending_text"],
            "floor": shared["params"].semantic_similarity_floor,
        }
    
    def exec(self, data: dict) -> dict:
        """Compute semantic similarity."""
        similarity = self.checker.compare(
            data["original"],
            data["revised"]
        )
        
        return {
            "similarity": similarity,
            "passes": similarity >= data["floor"],
        }
    
    def post(self, shared: dict, prep_res: dict, exec_res: dict) -> str:
        """Accept or rollback based on similarity."""
        shared["last_similarity"] = exec_res["similarity"]
        
        # Check if enforcement is enabled
        enforce = shared["params"].enforce_similarity
        
        if enforce and not exec_res["passes"]:
            return "rollback"
        
        # Accept the revision
        shared["current_text"] = shared["pending_text"]
        shared["iteration"] += 1
        return "accept"