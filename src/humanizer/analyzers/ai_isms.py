"""Detector for common AI-generated text patterns."""

import re


class AIIsmDetector:
    """
    Detects words and phrases commonly overused by LLMs.
    
    Categorized by signal strength for weighted scoring.
    """
    
    STRONG_SIGNALS = [
        "delve", "delving", "delved",
        "tapestry",
        "landscape",
        "paradigm shift",
        "It's important to note",
        "It's worth noting",
        "In today's world",
        "In today's fast-paced",
        "In conclusion",
        "To summarize",
        "Let's explore",
        "Let's dive",
        "dive into",
        "deep dive",
        "unpack this",
        "at the end of the day",
        "moving forward",
        "going forward",
        "leverage this",
        "the fact that",
        "It is important to",
        "It is essential to",
        "It is crucial to",
        "It is worth mentioning",
    ]
    
    MODERATE_SIGNALS = [
        "crucial", "vital", "essential",  # overused intensifiers
        "leverage", "utilize", "facilitate", "optimize",
        "Moreover", "Furthermore", "Additionally", "Consequently",
        "comprehensive", "robust", "streamline", "enhance",
        "cutting-edge", "game-changer", "groundbreaking",
        "innovative", "revolutionize", "transform",
        "seamless", "seamlessly",
        "empower", "empowering",
        "foster", "fostering",
        "nuanced", "multifaceted",
        "myriad",
        "plethora",
        "realm",
        "endeavor",
        "pivotal",
        "holistic",
    ]
    
    WEAK_SIGNALS = [
        "very", "really", "extremely", "highly",  # not AI-specific but bland
        "In order to",  # wordier than "to"
        "due to the fact that",  # wordier than "because"
        "at this point in time",  # wordier than "now"
        "in the event that",  # wordier than "if"
        "a large number of",  # wordier than "many"
        "in spite of the fact that",  # wordier than "although"
        "for the purpose of",  # wordier than "to"
        "with regard to",  # wordier than "about"
        "in reference to",  # wordier than "about"
    ]
    
    def analyze(self, text: str) -> dict:
        """
        Analyze text for AI-isms.
        
        Args:
            text: Text to analyze
            
        Returns:
            dict with found items, counts, and weighted score
        """
        text_lower = text.lower()
        
        found = {
            "strong": [],
            "moderate": [],
            "weak": []
        }
        
        # Check each category with word boundaries
        for word in self.STRONG_SIGNALS:
            if ' ' in word:
                # Phrase: use simple contains
                if word.lower() in text_lower:
                    found["strong"].append(word)
            else:
                # Single word: use word boundary
                pattern = rf'\b{re.escape(word.lower())}\b'
                if re.search(pattern, text_lower):
                    found["strong"].append(word)
        
        for word in self.MODERATE_SIGNALS:
            if ' ' in word:
                if word.lower() in text_lower:
                    found["moderate"].append(word)
            else:
                pattern = rf'\b{re.escape(word.lower())}\b'
                if re.search(pattern, text_lower):
                    found["moderate"].append(word)
        
        for word in self.WEAK_SIGNALS:
            if ' ' in word:
                if word.lower() in text_lower:
                    found["weak"].append(word)
            else:
                pattern = rf'\b{re.escape(word.lower())}\b'
                if re.search(pattern, text_lower):
                    found["weak"].append(word)
        
        # Calculate weighted score
        score = (
            len(found["strong"]) * 3 +
            len(found["moderate"]) * 2 +
            len(found["weak"]) * 1
        )
        
        # Flatten for convenience
        found_list = found["strong"] + found["moderate"] + found["weak"]
        
        return {
            "found": found,
            "found_list": found_list,
            "score": score,
            "count": len(found_list),
        }