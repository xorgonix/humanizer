"""API route definitions."""

from fastapi import APIRouter, HTTPException

from humanizer.api.models import (
    HumanizeRequest,
    HumanizeResponse,
    AnalyzeRequest,
    AnalyzeResponse,
    PresetsResponse,
    PresetInfo,
)
from humanizer.flow.flow import humanize, analyze
from humanizer.presets.genre_presets import PRESETS, apply_preset

router = APIRouter()


@router.post("/humanize", response_model=HumanizeResponse)
async def humanize_text(request: HumanizeRequest) -> HumanizeResponse:
    """
    Humanize the provided text.
    
    Applies iterative analysis and rewriting to make AI-generated
    text sound more natural while preserving meaning.
    """
    try:
        print(f"[API] /humanize text_len={len(request.text)} preset={request.preset} target={request.naturalness_target}")
        # Apply preset if specified
        if request.preset:
            request = apply_preset(request, request.preset)
        
        response = humanize(request)
        print("[API] /humanize done")
        return response
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze text without rewriting.
    
    Returns scores and suggestions for what could be improved.
    Useful for previewing before committing to humanization.
    """
    try:
        print(f"[API] /analyze text_len={len(request.text)}")
        response = analyze(request)
        print("[API] /analyze done")
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@router.get("/presets", response_model=PresetsResponse)
async def list_presets() -> PresetsResponse:
    """List available humanization presets."""
    
    preset_list = [
        PresetInfo(
            name=name,
            description=config["description"],
            naturalness_target=config["naturalness_target"],
            tone=config["tone"],
            allow_contractions=config["allow_contractions"],
            allow_fragments=config["allow_fragments"],
        )
        for name, config in PRESETS.items()
    ]
    
    return PresetsResponse(presets=preset_list)


@router.post("/suggest")
async def suggest_changes(request: AnalyzeRequest) -> dict:
    """
    Return flagged issues with specific suggested fixes.
    
    Allows users to review and selectively apply changes.
    """
    analysis = analyze(request)
    
    suggestions = []
    for issue in analysis.issues:
        suggestions.append({
            "issue": issue,
            "suggestion": _generate_suggestion(issue),
            "auto_fixable": _is_auto_fixable(issue),
        })
    
    return {
        "text": request.text,
        "suggestions": suggestions,
        "overall_score": analysis.scores.composite_score,
    }


def _generate_suggestion(issue: str) -> str:
    """Generate a human-readable suggestion for an issue."""
    
    if "AI-ism" in issue:
        word = issue.split("'")[1] if "'" in issue else "this word"
        return f"Consider replacing '{word}' with a more natural alternative"
    
    if "variance" in issue.lower():
        return "Try mixing short and long sentences for more natural rhythm"
    
    if "repetition" in issue.lower():
        return "Vary your sentence starters to avoid monotony"
    
    return "Consider revising for a more natural tone"


def _is_auto_fixable(issue: str) -> bool:
    """Determine if an issue can be auto-fixed."""
    
    auto_fixable_patterns = ["AI-ism", "repetition"]
    return any(pattern in issue for pattern in auto_fixable_patterns)