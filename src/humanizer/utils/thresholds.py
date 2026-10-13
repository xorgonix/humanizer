"""Threshold computation from naturalness target."""

from humanizer.api.models import HumanizeRequest


def compute_thresholds(request: HumanizeRequest) -> dict:
    """
    Map naturalness_target (0-100) to specific metric thresholds.
    
    Higher naturalness = stricter thresholds.
    
    Args:
        request: HumanizeRequest with parameters
        
    Returns:
        dict of threshold values
    """
    n = request.naturalness_target / 100
    
    return {
        # AI-isms: 100 → 0 allowed, 50 → 5 allowed, 0 → 10 allowed
        "max_ai_isms": int((1 - n) * 10) + request.ai_ism_tolerance,
        
        # Sentence variance: higher naturalness = need more variance
        "min_sentence_variance": n * request.sentence_variance_target,
        
        # Repetition: higher naturalness = less repetition tolerated
        "max_repetition": int((1 - n) * 8) + 2,
        
        # Perplexity floor: higher naturalness = need less predictable text
        "min_perplexity": n * 0.4,
        
        # Semantic similarity: always respect the floor
        "min_semantic_similarity": request.semantic_similarity_floor,
    }