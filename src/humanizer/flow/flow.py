"""Main flow definition and entry points."""

from pocketflow import Flow

from humanizer.api.models import (
    HumanizeRequest,
    HumanizeResponse,
    AnalyzeRequest,
    AnalyzeResponse,
)
from humanizer.flow.nodes import (
    AnalyzeNode,
    DecideNode,
    RewriteNode,
    ValidateNode,
    RollbackNode,
    OutputNode,
)
from humanizer.utils.thresholds import compute_thresholds


def create_humanization_flow() -> Flow:
    """Create and wire the humanization flow."""
    
    # Create nodes
    analyze_node = AnalyzeNode()
    decide_node = DecideNode()
    rewrite_node = RewriteNode()
    validate_node = ValidateNode()
    rollback_node = RollbackNode()
    output_node = OutputNode()
    
    # Wire the flow
    analyze_node >> decide_node
    
    decide_node - "passes" >> output_node
    decide_node - "max_iterations" >> output_node
    decide_node - "needs_work" >> rewrite_node
    
    rewrite_node >> validate_node
    
    validate_node - "accept" >> analyze_node
    validate_node - "rollback" >> rollback_node
    
    rollback_node - "retry" >> validate_node
    rollback_node - "give_up" >> analyze_node
    
    return Flow(start=analyze_node)


def humanize(request: HumanizeRequest) -> HumanizeResponse:
    """
    Main entry point for humanization.
    
    Args:
        request: HumanizeRequest with text and parameters
        
    Returns:
        HumanizeResponse with revised text and metrics
    """
    # Handle zero naturalness (no changes requested)
    if request.naturalness_target == 0:
        from humanizer.analyzers import analyze_text
        scores = analyze_text(request.text)
        
        return HumanizeResponse(
            revised_text=request.text,
            original_scores=scores,
            final_scores=scores,
            iterations_used=0,
            changes_summary=["No changes requested (naturalness_target=0)"],
            flagged_issues_remaining=[],
            semantic_similarity=1.0,
        )
    
    # Create flow and shared context
    flow = create_humanization_flow()
    
    shared = {
        "original_text": request.text,
        "current_text": request.text,
        "params": request,
        "thresholds": compute_thresholds(request),
        "changes": [],
        "iteration": 0,
        "rollback_count": 0,
        "original_scores": None,
        "response": None,
    }
    
    # Run the flow
    flow.run(shared)
    
    return shared["response"]


def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze text without rewriting.
    
    Args:
        request: AnalyzeRequest with text to analyze
        
    Returns:
        AnalyzeResponse with scores and suggestions
    """
    from humanizer.analyzers import analyze_text, generate_issues, generate_suggestions
    
    scores = analyze_text(request.text)
    issues = generate_issues(scores)
    suggestions = generate_suggestions(scores)
    
    return AnalyzeResponse(
        scores=scores,
        issues=issues,
        suggestions=suggestions,
    )