"""Text analyzers for AI-likeness detection."""

from humanizer.analyzers.ai_isms import AIIsmDetector
from humanizer.analyzers.sentence_variance import SentenceVarianceScorer
from humanizer.analyzers.repetition import RepetitionDetector
from humanizer.analyzers.perplexity import PerplexityScorer
from humanizer.analyzers.semantic_similarity import SemanticSimilarityChecker
from humanizer.api.models import ScoreBreakdown


def analyze_text(text: str) -> ScoreBreakdown:
    """
    Run all analyzers and return composite scores.
    
    Args:
        text: Text to analyze
        
    Returns:
        ScoreBreakdown with all metrics
    """
    ai_isms = AIIsmDetector().analyze(text)
    variance = SentenceVarianceScorer().analyze(text)
    repetition = RepetitionDetector().analyze(text)
    perplexity = PerplexityScorer().score(text)
    
    # Compute composite score (0-100, lower is more human-like)
    composite = _compute_composite(ai_isms, variance, repetition, perplexity)
    
    return ScoreBreakdown(
        ai_ism_count=ai_isms["count"],
        ai_ism_score=ai_isms["score"],
        ai_isms_found=ai_isms["found_list"],
        sentence_variance=variance["variance"],
        mean_sentence_length=variance["mean_length"],
        repetition_score=repetition["monotony_score"],
        repeated_starters=repetition["repeated_starters"],
        perplexity_normalized=perplexity["normalized"],
        composite_score=composite,
        overused_openers=repetition.get("overused_openers", {}),
    )


def _compute_composite(
    ai_isms: dict,
    variance: dict,
    repetition: dict,
    perplexity: dict
) -> float:
    """
    Compute composite AI-likeness score.
    
    Returns value 0-100 where:
    - 0 = perfectly human-like
    - 100 = obviously AI-generated
    """
    # Weight contributions
    ai_ism_contribution = min(ai_isms["score"] * 5, 40)  # Max 40 points
    
    # Low variance = more AI-like
    variance_contribution = max(0, 20 - variance["variance"] * 4)  # Max 20 points
    
    # High repetition = more AI-like
    repetition_contribution = min(repetition["monotony_score"] * 3, 20)  # Max 20 points
    
    # Low perplexity = more predictable = more AI-like
    perplexity_contribution = max(0, (1 - perplexity["normalized"]) * 20)  # Max 20 points
    
    return min(100, (
        ai_ism_contribution +
        variance_contribution +
        repetition_contribution +
        perplexity_contribution
    ))


def generate_issues(scores: ScoreBreakdown) -> list[str]:
    """Generate human-readable issue descriptions."""
    
    issues = []
    
    if scores.ai_ism_count > 0:
        issues.append(f"Found {scores.ai_ism_count} AI-isms: {', '.join(scores.ai_isms_found[:5])}")
    
    if scores.sentence_variance < 3.0:
        issues.append(f"Low sentence variance ({scores.sentence_variance:.1f}) - too uniform")
    
    if scores.repetition_score > 2:
        issues.append(f"Repetitive patterns detected (score: {scores.repetition_score})")
    
    if scores.perplexity_normalized < 0.3:
        issues.append("Text is highly predictable - may sound robotic")
    
    if scores.overused_openers:
        openers = list(scores.overused_openers.keys())[:3]
        issues.append(f"Overused conversational openers: {', '.join(openers)}")
    
    return issues


def generate_suggestions(scores: ScoreBreakdown) -> list[str]:
    """Generate actionable suggestions."""
    
    suggestions = []
    
    if scores.ai_ism_count > 0:
        suggestions.append("Replace AI-isms with natural alternatives")
    
    if scores.sentence_variance < 3.0:
        suggestions.append("Mix short punchy sentences with longer flowing ones")
    
    if scores.repeated_starters:
        top_repeated = list(scores.repeated_starters.keys())[:3]
        suggestions.append(f"Vary sentence starters ('{', '.join(top_repeated)}' used repeatedly)")
    
    if scores.perplexity_normalized < 0.3:
        suggestions.append("Add varied phrasing and occasional unexpected word choices")
    
    return suggestions


__all__ = [
    "AIIsmDetector",
    "SentenceVarianceScorer",
    "RepetitionDetector",
    "PerplexityScorer",
    "SemanticSimilarityChecker",
    "analyze_text",
    "generate_issues",
    "generate_suggestions",
]