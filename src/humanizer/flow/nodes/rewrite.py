"""Rewrite node - LLM-powered text transformation."""

import json
from pocketflow import Node

from humanizer.llm.client import get_llm_client
from humanizer.llm.prompts import build_rewrite_prompt
from humanizer.analyzers import generate_issues


class RewriteNode(Node):
    """
    LLM-powered rewriting.
    
    Receives flagged issues and applies targeted revisions.
    """
    
    def prep(self, shared: dict) -> dict:
        """Prepare rewrite context."""
        
        issues = generate_issues(shared["scores"])
        
        return {
            "text": shared.get("current_text", shared["original_text"]),
            "issues": issues,
            "params": shared["params"],
            "iteration": shared["iteration"],
        }
    
    def exec(self, data: dict) -> dict:
        """Call LLM for rewrite."""
        
        prompt = build_rewrite_prompt(
            text=data["text"],
            issues=data["issues"],
            tone=data["params"].tone,
            allow_contractions=data["params"].allow_contractions,
            allow_fragments=data["params"].allow_fragments,
            banned_words=data["params"].banned_words,
            protected_phrases=data["params"].protected_phrases,
            naturalness_target=data["params"].naturalness_target,
        )
        
        client = get_llm_client()
        response = client.chat(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
        )
        
        # Parse JSON response
        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            # Fallback: treat entire response as revised text
            result = {
                "revised_text": response,
                "changes": ["Applied revisions (details unavailable)"]
            }
        
        return result
    
    def post(self, shared: dict, prep_res: dict, exec_res: dict) -> str:
        """Store pending text for validation."""
        from humanizer.analyzers.ai_isms import AIIsmDetector
        
        pending = exec_res.get("revised_text", prep_res["text"])
        
        # Check for introduced AI-isms
        detector = AIIsmDetector()
        original_isms = set(detector.analyze(prep_res["text"])["found_list"])
        revised_isms = set(detector.analyze(pending)["found_list"])
        introduced = revised_isms - original_isms
        
        if introduced:
            shared["changes"].append(f"⚠️ LLM introduced AI-isms: {list(introduced)}")
        
        shared["pending_text"] = pending
        shared["changes"].extend(exec_res.get("changes", []))
        
        return "default"  # Goes to ValidateNode