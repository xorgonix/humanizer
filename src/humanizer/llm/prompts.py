"""Prompt templates for LLM calls."""


def build_rewrite_prompt(
    text: str,
    issues: list[str],
    tone: str,
    allow_contractions: bool,
    allow_fragments: bool,
    banned_words: list[str],
    protected_phrases: list[str],
    naturalness_target: int,
) -> str:
    """
    Build the rewrite prompt for the LLM.
    
    Args:
        text: Text to rewrite
        issues: List of identified issues
        tone: Target tone
        allow_contractions: Whether contractions are allowed
        allow_fragments: Whether sentence fragments are allowed
        banned_words: Words to avoid
        protected_phrases: Phrases to preserve exactly
        naturalness_target: 0-100 humanization intensity
        
    Returns:
        Formatted prompt string
    """
    
    intensity = "light" if naturalness_target < 40 else "moderate" if naturalness_target < 70 else "aggressive"
    
    issues_text = "\n".join(f"- {issue}" for issue in issues) if issues else "- No specific issues flagged"
    banned_text = ", ".join(banned_words) if banned_words else "None"
    protected_text = ", ".join(f'"{p}"' for p in protected_phrases) if protected_phrases else "None"
    
    return f"""# Role
You are a prose refinement assistant. Your job is to revise text to sound 
more naturally written while preserving meaning and the author's voice.

# Task
Revise the following text with {intensity} humanization.

# Flagged Issues
{issues_text}

# Style Parameters
- Tone: {tone}
- Allow contractions: {allow_contractions}
- Allow sentence fragments: {allow_fragments}
- Banned words: {banned_text}
- Protected phrases (keep exactly): {protected_text}

# Intensity Guidelines
- Light: Only fix the worst AI-isms, minimal changes
- Moderate: Address all flagged issues, improve flow
- Aggressive: Substantial reworking for natural voice

# Techniques You May Use
- Replace flagged AI-isms with natural alternatives
- Vary sentence length (mix short punchy with longer flowing)
- Reorder sentence elements for variety
- Add contractions (if allowed)
- Use em dashes, parentheticals (sparingly)
- Break up run-on sentences
- Combine choppy short sentences

# Techniques to Avoid
- Don't add flowery language not in the original
- Don't inject humor unless original had it
- Don't add metaphors that aren't there
- Don't change factual content
- Don't over-correct—subtle beats dramatic

# CRITICAL: Words/Phrases to NEVER Introduce
Do not use these AI-isms in your revision:
- "game-changer", "game-changing", "groundbreaking"
- "at the end of the day"
- "leverage", "utilize", "facilitate"
- "delve", "dive into", "deep dive"
- "seamless", "seamlessly"
- "landscape" (in business context)
- "paradigm", "paradigm shift"
- "holistic", "robust", "comprehensive"
- "empower", "foster", "streamline"
- "tapestry", "myriad", "plethora"
- "cutting-edge", "innovative", "revolutionize"
- "It's important to note", "It's worth noting"
- "In today's world", "moving forward"

# Simple Replacements (use these instead)
- leverage → use
- utilize → use
- facilitate → help, enable
- streamline → simplify, speed up
- crucial/vital/essential → important
- robust → strong, solid
- comprehensive → complete, full
- seamless → smooth
- transform → change
- innovative → new, fresh
- revolutionize → change, shake up

# Anti-Repetition Rules
- Do NOT reuse the same conversational opener more than once
- If you use "Here's the thing", don't use it again—try "Truth is", "Look,", "The point?", etc.
- Vary your sentence starters throughout the entire text
- Avoid repeating phrases like "Here's the kicker", "Bottom line", "The deal is"

# Text to Revise
{text}

# Output Format
Return ONLY valid JSON:
{{
  "revised_text": "your revised version here",
  "changes": [
    "brief description of change 1",
    "brief description of change 2"
  ]
}}"""


def build_rollback_prompt(
    original: str,
    drifted: str,
    target_similarity: float,
) -> str:
    """
    Build prompt for gentler revision after semantic drift.
    
    Args:
        original: Original text
        drifted: Revised text that drifted too far
        target_similarity: Target similarity score
        
    Returns:
        Formatted prompt string
    """
    
    return f"""# Task
The following revision drifted too far from the original meaning.
Create a gentler revision that stays much closer to the source text.

# Original Text
{original}

# Over-Revised Version (too different)
{drifted}

# Instructions
- Stay very close to the original wording
- Only make minimal changes to address obvious AI patterns
- Preserve the original sentence structure where possible
- Target similarity should be {target_similarity:.0%} or higher

# Output
Return ONLY the revised text, nothing else."""