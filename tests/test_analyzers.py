"""Tests for analyzer components."""

import pytest

from humanizer.analyzers.ai_isms import AIIsmDetector
from humanizer.analyzers.sentence_variance import SentenceVarianceScorer
from humanizer.analyzers.repetition import RepetitionDetector


class TestAIIsmDetector:
    """Tests for AI-ism detection."""
    
    def test_detects_strong_signals(self):
        detector = AIIsmDetector()
        
        text = "Let's delve into the landscape of AI technology."
        result = detector.analyze(text)
        
        assert result["count"] >= 2
        assert "delve" in result["found_list"] or "Let's delve" in str(result["found"])
        assert "landscape" in result["found_list"]
    
    def test_detects_moderate_signals(self):
        detector = AIIsmDetector()
        
        text = "We need to leverage this crucial opportunity. Moreover, it's essential."
        result = detector.analyze(text)
        
        assert "leverage" in result["found_list"]
        assert "crucial" in result["found_list"]
        assert "Moreover" in result["found_list"]
    
    def test_clean_text_scores_low(self):
        detector = AIIsmDetector()
        
        text = "The dog ran across the yard. It was a sunny day."
        result = detector.analyze(text)
        
        assert result["score"] == 0
        assert result["count"] == 0
    
    def test_weighted_scoring(self):
        detector = AIIsmDetector()
        
        # Strong signal
        strong = detector.analyze("Let's delve into this.")
        
        # Moderate signal
        moderate = detector.analyze("This is crucial.")
        
        # Strong should score higher
        assert strong["score"] > moderate["score"]


class TestSentenceVarianceScorer:
    """Tests for sentence variance analysis."""
    
    def test_uniform_sentences_low_variance(self):
        scorer = SentenceVarianceScorer()
        
        text = "This is short. That is short. Here is short. There is short."
        result = scorer.analyze(text)
        
        assert result["variance"] < 1.0
    
    def test_varied_sentences_high_variance(self):
        scorer = SentenceVarianceScorer()
        
        text = "Short. This is a much longer sentence with many more words in it. Medium length here. Another very long sentence that goes on and on with lots of words."
        result = scorer.analyze(text)
        
        assert result["variance"] > 3.0
    
    def test_single_sentence(self):
        scorer = SentenceVarianceScorer()
        
        text = "Just one sentence here."
        result = scorer.analyze(text)
        
        assert result["variance"] == 0.0
        assert result.get("issue") == "too_few_sentences"


class TestRepetitionDetector:
    """Tests for repetition detection."""
    
    def test_detects_repeated_starters(self):
        detector = RepetitionDetector()
        
        text = "The cat sat. The cat ran. The cat jumped. The cat slept."
        result = detector.analyze(text)
        
        assert len(result["repeated_starters"]) > 0
    
    def test_detects_overused_transitions(self):
        detector = RepetitionDetector()
        
        text = "First point. However, second point. However, third point. However, fourth point."
        result = detector.analyze(text)
        
        assert "however" in result["overused_transitions"]
    
    def test_clean_text_low_monotony(self):
        detector = RepetitionDetector()
        
        text = "The sun rose. Birds began to sing. A cool breeze stirred the leaves. Morning had arrived."
        result = detector.analyze(text)
        
        assert result["monotony_score"] < 3