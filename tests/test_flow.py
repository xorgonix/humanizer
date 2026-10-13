"""Tests for the humanization flow."""

import pytest

from humanizer.api.models import HumanizeRequest, AnalyzeRequest
from humanizer.flow.flow import humanize, analyze
from humanizer.utils.thresholds import compute_thresholds


class TestThresholds:
    """Tests for threshold computation."""
    
    def test_high_naturalness_strict_thresholds(self):
        request = HumanizeRequest(
            text="Test",
            naturalness_target=100
        )
        thresholds = compute_thresholds(request)
        
        assert thresholds["max_ai_isms"] == 0
        assert thresholds["min_sentence_variance"] > 0
    
    def test_low_naturalness_relaxed_thresholds(self):
        request = HumanizeRequest(
            text="Test",
            naturalness_target=0
        )
        thresholds = compute_thresholds(request)
        
        assert thresholds["max_ai_isms"] == 10
        assert thresholds["min_sentence_variance"] == 0
    
    def test_ai_ism_tolerance_adds(self):
        request = HumanizeRequest(
            text="Test",
            naturalness_target=100,
            ai_ism_tolerance=5
        )
        thresholds = compute_thresholds(request)
        
        assert thresholds["max_ai_isms"] == 5


class TestAnalyze:
    """Tests for analysis endpoint."""
    
    def test_analyze_returns_scores(self):
        request = AnalyzeRequest(
            text="It's important to note that we should leverage this crucial opportunity."
        )
        
        response = analyze(request)
        
        assert response.scores.ai_ism_count > 0
        assert len(response.issues) > 0
    
    def test_analyze_clean_text(self):
        request = AnalyzeRequest(
            text="The morning sun cast long shadows across the dew-covered grass."
        )
        
        response = analyze(request)
        
        assert response.scores.ai_ism_count == 0


class TestHumanize:
    """Tests for humanization endpoint."""
    
    def test_zero_naturalness_no_changes(self):
        original = "This text should not change at all."
        
        request = HumanizeRequest(
            text=original,
            naturalness_target=0
        )
        
        response = humanize(request)
        
        assert response.revised_text == original
        assert response.iterations_used == 0
    
    def test_returns_response_model(self):
        request = HumanizeRequest(
            text="It is important to note that this is a test.",
            naturalness_target=50
        )
        
        response = humanize(request)
        
        assert hasattr(response, 'revised_text')
        assert hasattr(response, 'original_scores')
        assert hasattr(response, 'final_scores')
        assert hasattr(response, 'iterations_used')