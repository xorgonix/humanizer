"""Rollback node - handles semantic drift."""

from pocketflow import Node

from humanizer.llm.client import get_llm_client
from humanizer.llm.prompts import build_rollback_prompt


class RollbackNode(Node):
    """
    Handle semantic drift.
    
    Attempts a gentler revision or gives up after max retries.
    """
    
    MAX_ROLLBACKS = 2
    
    def prep(self, shared: dict) -> dict:
        """Gather rollback context."""
        return {
            "original": shared["original_text"],
            "drifted": shared["pending_text"],
            "current": shared.get("current_text", shared["original_text"]),
            "rollback_count": shared.get("rollback_count", 0),
            "similarity": shared.get("last_similarity", 0),
        }
    
    def exec(self, data: dict) -> dict:
        """Attempt gentler revision."""
        
        # If we've tried too many times, give up
        if data["rollback_count"] >= self.MAX_ROLLBACKS:
            return {"action": "give_up", "text": data["current"]}
        
        # Try a gentler approach
        prompt = build_rollback_prompt(
            original=data["original"],
            drifted=data["drifted"],
            target_similarity=0.95,
        )
        
        client = get_llm_client()
        response = client.chat(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
        )
        
        return {"action": "retry", "text": response}
    
    def post(self, shared: dict, prep_res: dict, exec_res: dict) -> str:
        """Update state based on rollback result."""
        
        if exec_res["action"] == "give_up":
            # Keep current text, move on
            shared["iteration"] += 1
            shared["rollback_count"] = 0
            shared["changes"].append("Rollback: kept previous version (drift too high)")
            return "give_up"
        
        # Try the gentler version
        shared["pending_text"] = exec_res["text"]
        shared["rollback_count"] = prep_res["rollback_count"] + 1
        shared["changes"].append("Rollback: attempting gentler revision")
        
        return "retry"