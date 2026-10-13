"""Text processing utilities."""

import re


def split_into_chunks(text: str, max_chunk_size: int = 2000) -> list[str]:
    """
    Split text into chunks for processing.
    
    Tries to split on paragraph boundaries, falling back to sentences.
    
    Args:
        text: Text to split
        max_chunk_size: Maximum characters per chunk
        
    Returns:
        List of text chunks
    """
    if len(text) <= max_chunk_size:
        return [text]
    
    # Try splitting on paragraphs first
    paragraphs = text.split("\n\n")
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 <= max_chunk_size:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            # If single paragraph is too long, split on sentences
            if len(para) > max_chunk_size:
                sentence_chunks = _split_long_paragraph(para, max_chunk_size)
                chunks.extend(sentence_chunks[:-1])
                current_chunk = sentence_chunks[-1] + "\n\n"
            else:
                current_chunk = para + "\n\n"
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks


def _split_long_paragraph(para: str, max_size: int) -> list[str]:
    """Split a long paragraph on sentence boundaries."""
    
    sentences = re.split(r'(?<=[.!?])\s+', para)
    
    chunks = []
    current = ""
    
    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= max_size:
            current += sentence + " "
        else:
            if current:
                chunks.append(current.strip())
            current = sentence + " "
    
    if current.strip():
        chunks.append(current.strip())
    
    return chunks


def split_into_chapters(book_text: str) -> list[dict]:
    """
    Split a book into chapters.
    
    Looks for common chapter markers.
    
    Args:
        book_text: Full book text
        
    Returns:
        List of dicts with chapter number and text
    """
    # Common chapter patterns
    chapter_pattern = re.compile(
        r'^(?:Chapter|CHAPTER)\s+(\d+|[IVXLC]+)[\s:.\-]*(.*)$',
        re.MULTILINE
    )
    
    matches = list(chapter_pattern.finditer(book_text))
    
    if not matches:
        # No chapters found, return as single chunk
        return [{"number": 1, "title": "", "text": book_text}]
    
    chapters = []
    
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(book_text)
        
        chapter_text = book_text[start:end].strip()
        
        chapters.append({
            "number": i + 1,
            "title": match.group(2).strip() if match.group(2) else "",
            "text": chapter_text,
        })
    
    return chapters


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text."""
    
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    
    # Replace multiple newlines with double newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()