"""Genre-specific preset configurations."""

from humanizer.api.models import HumanizeRequest, Tone


PRESETS = {
    "light-touch": {
        "description": "Minimal changes, just fix worst AI-isms",
        "naturalness_target": 30,
        "tone": Tone.FORMAL,
        "allow_contractions": False,
        "allow_fragments": False,
        "max_iterations": 1,
    },
    
    "conversational": {
        "description": "Casual, friendly tone with contractions",
        "naturalness_target": 70,
        "tone": Tone.CASUAL,
        "allow_contractions": True,
        "allow_fragments": True,
        "max_iterations": 3,
    },
    
    "literary-fiction": {
        "description": "High humanization for fiction writing",
        "naturalness_target": 85,
        "tone": Tone.LITERARY,
        "allow_contractions": True,
        "allow_fragments": True,
        "max_iterations": 4,
    },
    
    "romance": {
        "description": "Optimized for romance genre conventions",
        "naturalness_target": 80,
        "tone": Tone.LITERARY,
        "allow_contractions": True,
        "allow_fragments": True,
        "max_iterations": 3,
        "protected_phrases": ["he said", "she said", "he whispered", "she whispered"],
    },
    
    "thriller": {
        "description": "Punchy, tense prose for thrillers",
        "naturalness_target": 75,
        "tone": Tone.CASUAL,
        "allow_contractions": True,
        "allow_fragments": True,
        "sentence_variance_target": 6.0,  # High variance for tension
        "max_iterations": 3,
    },
    
    "technical": {
        "description": "Clean technical writing, no casual elements",
        "naturalness_target": 50,
        "tone": Tone.TECHNICAL,
        "allow_contractions": False,
        "allow_fragments": False,
        "max_iterations": 2,
        "banned_words": ["basically", "simply", "just", "really"],
    },
    
    "academic": {
        "description": "Formal academic prose",
        "naturalness_target": 45,
        "tone": Tone.ACADEMIC,
        "allow_contractions": False,
        "allow_fragments": False,
        "max_iterations": 2,
    },
    
    "marketing": {
        "description": "Engaging marketing copy",
        "naturalness_target": 65,
        "tone": Tone.MARKETING,
        "allow_contractions": True,
        "allow_fragments": True,
        "max_iterations": 3,
    },
    
    "blog": {
        "description": "Friendly blog post style",
        "naturalness_target": 75,
        "tone": Tone.CASUAL,
        "allow_contractions": True,
        "allow_fragments": True,
        "max_iterations": 3,
    },
}


def apply_preset(request: HumanizeRequest, preset_name: str) -> HumanizeRequest:
    """
    Apply a preset to a request.
    
    Args:
        request: Original request
        preset_name: Name of preset to apply
        
    Returns:
        New request with preset values applied
    """
    if preset_name not in PRESETS:
        raise ValueError(f"Unknown preset: {preset_name}. Available: {list(PRESETS.keys())}")
    
    preset = PRESETS[preset_name]
    
    # Create new request with preset values, keeping original text
    return HumanizeRequest(
        text=request.text,
        naturalness_target=preset.get("naturalness_target", request.naturalness_target),
        tone=preset.get("tone", request.tone),
        allow_contractions=preset.get("allow_contractions", request.allow_contractions),
        allow_fragments=preset.get("allow_fragments", request.allow_fragments),
        max_iterations=preset.get("max_iterations", request.max_iterations),
        sentence_variance_target=preset.get("sentence_variance_target", request.sentence_variance_target),
        banned_words=preset.get("banned_words", []) + request.banned_words,
        protected_phrases=preset.get("protected_phrases", []) + request.protected_phrases,
        semantic_similarity_floor=request.semantic_similarity_floor,
    )