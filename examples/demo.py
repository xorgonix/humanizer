"""Demo script to exercise the Humanizer API without running a server.

This uses FastAPI's TestClient to call the real API routes so you can see
before/after text, changes, and scores as the flow runs. The flow already
logs its internal steps (Analyze/Rewrite/Validate/Decide) to stdout.

Run:
  uv run python examples/demo.py
"""

from pprint import pprint

from fastapi.testclient import TestClient

from humanizer.api.main import app


client = TestClient(app)


def run_humanize(text: str, *, naturalness: int = 75, preset: str | None = None, sim_floor: float | None = None) -> None:
    payload = {"text": text, "naturalness_target": naturalness}
    if preset:
        payload["preset"] = preset
    if sim_floor is not None:
        payload["semantic_similarity_floor"] = sim_floor

    print("\n=== /humanize call ===")
    print(f"preset={preset} naturalness={naturalness} sim_floor={sim_floor}")
    print("Original:\n", text)

    resp = client.post("/humanize", json=payload)
    print("Status:", resp.status_code)
    if resp.status_code != 200:
        print("Error:", resp.text)
        return

    data = resp.json()
    print("\nRevised:\n", data.get("revised_text", "<missing>"))
    print("\nChanges:")
    for c in data.get("changes_summary", []):
        print("-", c)
    print("\nIterations:", data.get("iterations_used"))
    print("Semantic similarity:", data.get("semantic_similarity"))
    print("Original scores:")
    pprint(data.get("original_scores"))
    print("Final scores:")
    pprint(data.get("final_scores"))


def run_analyze(text: str) -> None:
    print("\n=== /analyze call ===")
    print("Text:\n", text)
    resp = client.post("/analyze", json={"text": text})
    print("Status:", resp.status_code)
    if resp.status_code != 200:
        print("Error:", resp.text)
        return
    data = resp.json()
    print("Scores:")
    pprint(data.get("scores"))
    print("Issues:", data.get("issues"))
    print("Suggestions:", data.get("suggestions"))


def main() -> None:
    text = (
        "The AI system generated this article to showcase its capabilities, but the tone feels stiff and overly formal. "
        "Readers might notice the repetitive phrasing and the absence of vivid details. It would be better if the piece "
        "used more concrete examples, varied sentence lengths, and a warmer, conversational voice. In its current form, "
        "the article sounds like a technical memo rather than something written for people who want to learn. "
        "With some human touch—small anecdotes, sensory descriptions, and clearer transitions—it could become engaging "
        "and easy to follow."
    )

    # Analyze first to see baseline.
    run_analyze(text)

    # Humanize with stricter target and relaxed similarity floor to allow rewrites.
    run_humanize(text, naturalness=85, sim_floor=0.8)

    # Humanize with a preset if available (e.g., conversational).
    run_humanize(text, naturalness=75, preset="conversational", sim_floor=0.8)


if __name__ == "__main__":
    main()
