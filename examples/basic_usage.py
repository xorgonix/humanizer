"""Basic usage examples for Humanizer."""

from humanizer import humanize, analyze, HumanizeRequest, AnalyzeRequest


def example_analyze():
    """Example: Analyze text without rewriting."""
    
    text = """
    It is important to note that artificial intelligence is rapidly transforming 
    the landscape of modern business. Furthermore, organizations must leverage 
    these cutting-edge technologies to remain competitive. Additionally, the 
    crucial nature of this transformation cannot be overstated.
    """
    
    request = AnalyzeRequest(text=text)
    response = analyze(request)
    
    print("=== Analysis Results ===")
    print(f"AI-isms found: {response.scores.ai_isms_found}")
    print(f"Sentence variance: {response.scores.sentence_variance:.2f}")
    print(f"Composite score: {response.scores.composite_score:.1f}")
    print(f"\nIssues:")
    for issue in response.issues:
        print(f"  - {issue}")
    print(f"\nSuggestions:")
    for suggestion in response.suggestions:
        print(f"  - {suggestion}")


def example_humanize_light():
    """Example: Light humanization (minimal changes)."""
    
    text = """
    It is important to note that the project deadline is approaching. 
    Furthermore, we need to leverage our resources effectively.
    """
    
    request = HumanizeRequest(
        text=text,
        naturalness_target=30,  # Light touch
        max_iterations=1
    )
    
    response = humanize(request)
    
    print("=== Light Humanization ===")
    print(f"Original score: {response.original_scores.composite_score:.1f}")
    print(f"Final score: {response.final_scores.composite_score:.1f}")
    print(f"\nRevised text:\n{response.revised_text}")


def example_humanize_aggressive():
    """Example: Aggressive humanization."""
    
    text = """
    It is important to note that the project deadline is approaching. 
    Furthermore, we need to leverage our resources effectively.
    """
    
    request = HumanizeRequest(
        text=text,
        naturalness_target=85,  # Aggressive
        tone="casual",
        allow_contractions=True,
        allow_fragments=True,
        max_iterations=3
    )
    
    response = humanize(request)
    
    print("=== Aggressive Humanization ===")
    print(f"Original score: {response.original_scores.composite_score:.1f}")
    print(f"Final score: {response.final_scores.composite_score:.1f}")
    print(f"Iterations used: {response.iterations_used}")
    print(f"\nRevised text:\n{response.revised_text}")
    print(f"\nChanges:")
    for change in response.changes_summary:
        print(f"  - {change}")


def example_with_preset():
    """Example: Using a genre preset."""
    
    text = """
    The detective examined the crime scene carefully. It was evident that 
    the perpetrator had left several clues. Furthermore, the forensic 
    evidence would prove crucial to solving the case.
    """
    
    request = HumanizeRequest(
        text=text,
        preset="thriller"  # Uses thriller preset settings
    )
    
    response = humanize(request)
    
    print("=== Thriller Preset ===")
    print(f"\nRevised text:\n{response.revised_text}")


def example_with_constraints():
    """Example: Using banned words and protected phrases."""
    
    text = """
    The magical sword basically just glowed with power. "I am the chosen one," 
    the hero said. It was a very important moment.
    """
    
    request = HumanizeRequest(
        text=text,
        naturalness_target=70,
        banned_words=["basically", "just", "very"],
        protected_phrases=['"I am the chosen one," the hero said'],
        tone="literary"
    )
    
    response = humanize(request)
    
    print("=== With Constraints ===")
    print(f"\nRevised text:\n{response.revised_text}")


if __name__ == "__main__":
    print("\n" + "="*60)
    example_analyze()
    
    print("\n" + "="*60)
    example_humanize_light()
    
    print("\n" + "="*60)
    example_humanize_aggressive()
    
    print("\n" + "="*60)
    example_with_preset()
    
    print("\n" + "="*60)
    example_with_constraints()