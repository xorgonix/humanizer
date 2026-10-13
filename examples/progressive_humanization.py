"""Demo that humanizes the same three-paragraph LLM draft at escalating naturalness targets."""

from __future__ import annotations

import os
import sys
import textwrap
from io import StringIO

from humanizer import HumanizeRequest, humanize


LLM_DRAFT = (
    "It is important to note that our cutting-edge platform leverages state-of-the-art technology to revolutionize the way businesses operate. "
    "Furthermore, we are committed to delivering comprehensive solutions that empower organizations to achieve their full potential. "
    "Additionally, our innovative approach ensures seamless integration with existing systems while maximizing efficiency and ROI.\n\n"
    "The robust features of our solution are designed to address the evolving needs of modern enterprises. "
    "It is crucial to understand that by utilizing our advanced analytics and automation capabilities, companies can streamline operations and drive sustainable growth. "
    "Moreover, our dedicated team of experts provides unparalleled support to ensure optimal outcomes for every client.\n\n"
    "In conclusion, partnering with us enables organizations to unlock unprecedented value and stay ahead in today's competitive landscape. "
    "Our holistic methodology combines industry best practices with transformative insights to deliver measurable results. "
    "Ultimately, we facilitate the journey toward digital excellence and operational transformation."
)


def run_level(step: int, target: int) -> None:
    """Humanize the draft at a given naturalness target and print key results."""
    request = HumanizeRequest(
        text=LLM_DRAFT,
        naturalness_target=target,
        max_iterations=3,
    )

    print("\n" + "=" * 72)
    print(f"Step {step}: naturalness target {target}")
    print(
        "Request settings:\n"
        f"  tone={request.tone} allow_contractions={request.allow_contractions} allow_fragments={request.allow_fragments}\n"
        f"  max_iterations={request.max_iterations} semantic_similarity_floor={request.semantic_similarity_floor}\n"
        f"  sentence_variance_target={request.sentence_variance_target} ai_ism_tolerance={request.ai_ism_tolerance}\n"
        f"  preset={request.preset} llm_stub={os.getenv('LLM_STUB', '0')} llm_base_url={os.getenv('LLM_BASE_URL', os.getenv('OPENAI_BASE_URL', ''))}"
    )

    print("\n" + "─" * 96)
    print("INPUT TEXT:")
    print("─" * 96 + "\n")
    print(textwrap.fill(request.text, width=96))
    print("\n" + "─" * 96 + "\n")

    # Suppress flow logs during humanize
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        response = humanize(request)
    finally:
        sys.stdout = old_stdout

    print("─" * 96)
    print("REVISED TEXT:")
    print("─" * 96 + "\n")
    print(textwrap.fill(response.revised_text, width=96))
    print("\n" + "─" * 96 + "\n")
    print("Key changes:")
    for change in response.changes_summary:
        print(f"- {change}")


def main() -> None:
    print("\n" + "─" * 96)
    print("ORIGINAL DRAFT:")
    print("─" * 96 + "\n")
    print(textwrap.fill(LLM_DRAFT, width=96))
    print("\n" + "─" * 96 + "\n")
    targets = (25, 50, 70, 90)
    for idx, target in enumerate(targets, start=1):
        run_level(idx, target)


if __name__ == "__main__":
    main()
