"""Analysis node - scores text for AI-likeness."""

from pocketflow import Node

from humanizer.analyzers import analyze_text


class AnalyzeNode(Node):
    """
    Deterministic scoring of text.
    
    Runs all analyzers and produces composite score.
    """
    
    def prep(self, shared: dict) -> str:
        """Get text to analyze."""
        return shared.get("current_text", shared["original_text"])
    
    def exec(self, text: str) -> dict:
        """Run all analyzers."""
        return analyze_text(text)
    
    def post(self, shared: dict, prep_res: str, exec_res: dict) -> str:
        """Store scores and proceed to decision."""
        
        # Store original scores on first pass
        if shared["original_scores"] is None:
            shared["original_scores"] = exec_res
        
        shared["scores"] = exec_res
        
        return "default"  # Goes to DecideNode