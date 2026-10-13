"""Example: Batch processing for books."""

import asyncio
from concurrent.futures import ThreadPoolExecutor

from humanizer import humanize, HumanizeRequest
from humanizer.utils.text_utils import split_into_chapters, split_into_chunks


def process_chapter(chapter: dict, preset: str = "literary-fiction") -> dict:
    """Process a single chapter."""
    
    request = HumanizeRequest(
        text=chapter["text"],
        preset=preset
    )
    
    response = humanize(request)
    
    return {
        "number": chapter["number"],
        "title": chapter["title"],
        "original_text": chapter["text"],
        "revised_text": response.revised_text,
        "original_score": response.original_scores.composite_score,
        "final_score": response.final_scores.composite_score,
        "changes": response.changes_summary,
    }


def process_book(
    book_text: str,
    preset: str = "literary-fiction",
    max_workers: int = 4
) -> dict:
    """
    Process an entire book with parallel chapter processing.
    
    Args:
        book_text: Full book text
        preset: Humanization preset to use
        max_workers: Number of parallel workers
        
    Returns:
        dict with processed chapters and statistics
    """
    # Split into chapters
    chapters = split_into_chapters(book_text)
    
    print(f"Processing {len(chapters)} chapters...")
    
    # Process chapters in parallel
    processed = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_chapter, chapter, preset)
            for chapter in chapters
        ]
        
        for i, future in enumerate(futures):
            result = future.result()
            processed.append(result)
            print(f"  Chapter {i+1}: {result['original_score']:.1f} → {result['final_score']:.1f}")
    
    # Compile statistics
    total_original = sum(c["original_score"] for c in processed)
    total_final = sum(c["final_score"] for c in processed)
    
    return {
        "chapters": processed,
        "statistics": {
            "chapter_count": len(processed),
            "average_original_score": total_original / len(processed),
            "average_final_score": total_final / len(processed),
            "total_changes": sum(len(c["changes"]) for c in processed),
        }
    }


def reassemble_book(processed: dict) -> str:
    """Reassemble processed chapters into full book text."""
    
    chapters = sorted(processed["chapters"], key=lambda c: c["number"])
    
    return "\n\n".join(c["revised_text"] for c in chapters)


# Example usage
if __name__ == "__main__":
    # Sample book text
    sample_book = """
Chapter 1: The Beginning

It is important to note that the journey began on a cold morning. Furthermore, 
the protagonist had no idea what adventures awaited. The landscape stretched 
before them, vast and mysterious. Additionally, there was a sense of anticipation 
in the air.

Chapter 2: The Discovery

The cave entrance loomed before them. It was crucial to proceed with caution. 
Moreover, the ancient symbols on the walls suggested this was no ordinary place. 
The explorer delved deeper into the darkness.

Chapter 3: The Confrontation

The final battle was upon them. It is essential to understand the stakes involved. 
The hero leveraged every skill they had learned. Furthermore, the outcome would 
determine the fate of the entire kingdom.
    """
    
    # Process the book
    result = process_book(sample_book, preset="literary-fiction")
    
    # Print statistics
    print("\n=== Processing Complete ===")
    print(f"Chapters processed: {result['statistics']['chapter_count']}")
    print(f"Average score improvement: {result['statistics']['average_original_score']:.1f} → {result['statistics']['average_final_score']:.1f}")
    print(f"Total changes made: {result['statistics']['total_changes']}")
    
    # Get final book
    final_book = reassemble_book(result)
    print("\n=== Final Book ===")
    print(final_book)