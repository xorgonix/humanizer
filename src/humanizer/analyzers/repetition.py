"""Analyzer for repetitive patterns."""

import re
from collections import Counter


class RepetitionDetector:
    """
    Detects repetitive patterns in text.
    
    Looks for:
    - Repeated sentence starters
    - Repeated phrases
    - Repeated transition words
    - Overused conversational openers
    """
    
    CONVERSATIONAL_OPENERS = [
        "here's the thing",
        "here's the kicker",
        "the kicker is",
        "bottom line",
        "truth is",
        "fact is",
        "thing is",
        "point is",
        "let's be honest",
        "let's be real",
        "let's face it",
        "here's the deal",
        "the deal is",
    ]
    
    def analyze(self, text: str) -> dict:
        """
        Analyze text for repetition.
        
        Args:
            text: Text to analyze
            
        Returns:
            dict with repetition metrics
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Check for repeated sentence starters
        starters = []
        for s in sentences:
            words = s.split()
            if words:
                # Get first 1-2 words as starter
                starter = words[0].lower()
                if len(words) > 1:
                    starter = f"{words[0].lower()} {words[1].lower()}"
                starters.append(starter)
        
        starter_counts = Counter(starters)
        repeated_starters = {k: v for k, v in starter_counts.items() if v > 2}
        
        # Check for repeated phrases (3+ words appearing 2+ times)
        words = text.lower().split()
        trigrams = [" ".join(words[i:i+3]) for i in range(len(words)-2)]
        trigram_counts = Counter(trigrams)
        repeated_phrases = {k: v for k, v in trigram_counts.items() if v > 1}
        
        # Check for repeated transitions
        transitions = ["however", "therefore", "moreover", "furthermore", 
                      "additionally", "consequently", "nevertheless"]
        transition_counts = {t: text.lower().count(t) for t in transitions}
        overused_transitions = {k: v for k, v in transition_counts.items() if v > 2}
        
        # Check for overused conversational openers
        text_lower = text.lower()
        opener_counts = {}
        for opener in self.CONVERSATIONAL_OPENERS:
            count = text_lower.count(opener)
            if count > 0:
                opener_counts[opener] = count
        
        overused_openers = {k: v for k, v in opener_counts.items() if v > 1}
        
        # Compute monotony score
        monotony_score = (
            len(repeated_starters) * 2 +
            len([p for p, c in repeated_phrases.items() if c > 2]) +
            len(overused_transitions) +
            len(overused_openers) * 2
        )
        
        return {
            "repeated_starters": repeated_starters,
            "repeated_phrases": dict(list(repeated_phrases.items())[:10]),
            "overused_transitions": overused_transitions,
            "overused_openers": overused_openers,
            "monotony_score": monotony_score,
        }