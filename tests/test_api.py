"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from humanizer.api.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for health check."""
    
    def test_health_returns_healthy(self, client):
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestPresetsEndpoint:
    """Tests for presets endpoint."""
    
    def test_returns_presets(self, client):
        response = client.get("/presets")
        
        assert response.status_code == 200
        assert "presets" in response.json()
        assert len(response.json()["presets"]) > 0
    
    def test_preset_has_required_fields(self, client):
        response = client.get("/presets")
        preset = response.json()["presets"][0]
        
        assert "name" in preset
        assert "description" in preset
        assert "naturalness_target" in preset
        assert "tone" in preset


class TestAnalyzeEndpoint:
    """Tests for analyze endpoint."""
    
    def test_analyze_valid_text(self, client):
        response = client.post(
            "/analyze",
            json={"text": "This is a test sentence."}
        )
        
        assert response.status_code == 200
        assert "scores" in response.json()
    
    def test_analyze_empty_text_fails(self, client):
        response = client.post(
            "/analyze",
            json={"text": ""}
        )
        
        assert response.status_code == 422


class TestHumanizeEndpoint:
    """Tests for humanize endpoint."""
    
    def test_humanize_valid_request(self, client):
        response = client.post(
            "/humanize",
            json={
                "text": "It is important to note that we should leverage this opportunity.",
                "naturalness_target": 50
            }
        )
        
        assert response.status_code == 200
        assert "revised_text" in response.json()
    
    def test_humanize_with_preset(self, client):
        response = client.post(
            "/humanize",
            json={
                "text": "Test text here.",
                "preset": "conversational"
            }
        )
        
        assert response.status_code == 200
    
    def test_humanize_invalid_preset_fails(self, client):
        response = client.post(
            "/humanize",
            json={
                "text": "Test text.",
                "preset": "nonexistent_preset"
            }
        )
        
        assert response.status_code == 400