"""Pydantic models for API requests and responses."""

from enum import Enum
from pydantic import BaseModel, Field


class Tone(str, Enum):
    CASUAL = "casual"
    FORMAL = "formal"
    ACADEMIC = "academic"
    LITERARY = "literary"
    MARKETING = "marketing"
    TECHNICAL = "technical"


class HumanizeRequest(BaseModel):
    """Request model for humanization."""
    
    text: str = Field(..., min_length=1, description="Text to humanize")
    
    # Main dial: 0 = untouched, 100 = maximum humanization
    naturalness_target: int = Field(
        default=70,
        ge=0,
        le=100,
        description="Humanization intensity (0-100)"
    )
    
    # Fine-tuning knobs
    sentence_variance_target: float = Field(
        default=4.0,
        ge=0,
        description="Target standard deviation of sentence lengths"
    )
    semantic_similarity_floor: float = Field(
        default=0.92,
        ge=0.5,
        le=1.0,
        description="Minimum semantic similarity to preserve"
    )
    enforce_similarity: bool = Field(
        default=False,
        description="If true, reject rewrites that drift too far from original"
    )
    ai_ism_tolerance: int = Field(
        default=0,
        ge=0,
        description="Number of AI-isms allowed in final output"
    )
    
    # Style controls
    tone: Tone = Field(default=Tone.CASUAL, description="Target tone")
    allow_contractions: bool = Field(default=True)
    allow_fragments: bool = Field(default=False)
    
    # Processing controls
    max_iterations: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum rewrite iterations"
    )
    
    # Custom word lists
    banned_words: list[str] = Field(
        default_factory=list,
        description="Words to avoid in output"
    )
    protected_phrases: list[str] = Field(
        default_factory=list,
        description="Phrases to preserve exactly"
    )
    
    # Optional preset
    preset: str | None = Field(
        default=None,
        description="Named preset to apply (overrides other settings)"
    )


class ScoreBreakdown(BaseModel):
    """Detailed scoring breakdown."""
    
    ai_ism_count: int
    ai_ism_score: float
    ai_isms_found: list[str]
    sentence_variance: float
    mean_sentence_length: float
    repetition_score: float
    repeated_starters: dict[str, int]
    perplexity_normalized: float
    composite_score: float
    overused_openers: dict[str, int] = Field(default_factory=dict)


class HumanizeResponse(BaseModel):
    """Response model for humanization."""
    
    revised_text: str
    original_scores: ScoreBreakdown
    final_scores: ScoreBreakdown
    iterations_used: int
    changes_summary: list[str]
    flagged_issues_remaining: list[str]
    semantic_similarity: float


class AnalyzeRequest(BaseModel):
    """Request model for analysis only (no rewriting)."""
    
    text: str = Field(..., min_length=1)


class AnalyzeResponse(BaseModel):
    """Response model for analysis."""
    
    scores: ScoreBreakdown
    issues: list[str]
    suggestions: list[str]


class PresetInfo(BaseModel):
    """Information about a preset configuration."""
    
    name: str
    description: str
    naturalness_target: int
    tone: Tone
    allow_contractions: bool
    allow_fragments: bool


class PresetsResponse(BaseModel):
    """Response listing available presets."""
    
    presets: list[PresetInfo]