"""Output node - packages final response."""

from pocketflow import Node

from humanizer.api.models import HumanizeResponse, ScoreBreakdown
from humanizer.analyzers import generate_issues


class OutputNode(Node):
    """
    Package final results.
    
    Converts internal state to API response model.
    """
    
    def prep(self, shared: dict) -> dict:
        """Get final state."""
        return shared
    
    def exec(self, shared: dict) -> HumanizeResponse:
        """Build response object."""
        
        final_scores = shared["scores"]
        remaining_issues = generate_issues(final_scores)
        
        return HumanizeResponse(
            revised_text=shared.get("current_text", shared["original_text"]),
            original_scores=self._to_breakdown(shared["original_scores"]),
            final_scores=self._to_breakdown(final_scores),
            iterations_used=shared["iteration"],
            changes_summary=shared["changes"],
            flagged_issues_remaining=remaining_issues,
            semantic_similarity=shared.get("last_similarity", 1.0),
        )
    
    def _to_breakdown(self, scores: dict) -> ScoreBreakdown:
        """Convert internal scores to API model."""
        
        if isinstance(scores, ScoreBreakdown):
            return scores
        
        return ScoreBreakdown(
            ai_ism_count=scores.get("ai_ism_count", 0),
            ai_ism_score=scores.get("ai_ism_score", 0.0),
            ai_isms_found=scores.get("ai_isms_found", []),
            sentence_variance=scores.get("sentence_variance", 0.0),
            mean_sentence_length=scores.get("mean_sentence_length", 0.0),
            repetition_score=scores.get("repetition_score", 0.0),
            repeated_starters=scores.get("repeated_starters", {}),
            perplexity_normalized=scores.get("perplexity_normalized", 0.0),
            composite_score=scores.get("composite_score", 0.0),
            overused_openers=scores.get("overused_openers", {}),
        )
    
    def post(self, shared: dict, prep_res: dict, exec_res: HumanizeResponse) -> None:
        """Store response and end flow."""
        shared["response"] = exec_res
        return None  # End flow