"""Decision node - determines if targets are met."""

from pocketflow import Node


class DecideNode(Node):
    """
    Check if we've hit targets or exhausted iterations.
    
    Routes to either output (done) or rewrite (needs work).
    """
    
    def prep(self, shared: dict) -> dict:
        """Gather decision inputs."""
        return {
            "scores": shared["scores"],
            "thresholds": shared["thresholds"],
            "iteration": shared["iteration"],
            "max_iterations": shared["params"].max_iterations,
        }
    
    def exec(self, data: dict) -> str:
        """Make routing decision."""
        # Check iteration limit
        if data["iteration"] >= data["max_iterations"]:
            return "max_iterations"
        
        # Check if all thresholds are met
        if self._passes_thresholds(data["scores"], data["thresholds"]):
            return "passes"
        
        return "needs_work"
    
    def _passes_thresholds(self, scores: dict, thresholds: dict) -> bool:
        """Check if scores meet all thresholds."""
        
        # AI-ism count
        if scores.ai_ism_count > thresholds["max_ai_isms"]:
            return False
        
        # Sentence variance (higher is better)
        if scores.sentence_variance < thresholds["min_sentence_variance"]:
            return False
        
        # Repetition score (lower is better)
        if scores.repetition_score > thresholds["max_repetition"]:
            return False
        
        return True
    
    def post(self, shared: dict, prep_res: dict, exec_res: str) -> str:
        """Return decision as next action."""
        return exec_res