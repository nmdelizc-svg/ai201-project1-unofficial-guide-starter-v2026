import re
from dataclasses import dataclass

import config
from ingest import Document

# Every document in advice_threads is a THREAD: line followed by replies, each
# one introduced by a marker like "--- reply 2 (29 votes) ---". The documents
# hand me their own boundaries; I don't have to guess where one ends.
REPLY_MARKER = re.compile(r"^--- reply \d+ \([^)]*\) ---$", re.MULTILINE)


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _segments(text: str) -> tuple[str, list[str]]:
    """The THREAD line, and one block per reply. No markers: no blocks."""
    marks = list(REPLY_MARKER.finditer(text))
    if not marks:
        return text.strip(), []

    header = text[: marks[0].start()].strip()
    blocks = [
        text[m.start() : (marks[i + 1].start() if i + 1 < len(marks) else len(text))].strip()
        for i, m in enumerate(marks)
    ]
    return header, blocks


def _by_sentence(text: str, limit: int) -> list[str]:
    """Last resort for a single reply longer than the limit. Never cuts mid-sentence."""
    pieces: list[str] = []
    current = ""
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        if current and len(current) + 1 + len(sentence) > limit:
            pieces.append(current)
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        pieces.append(current)
    return pieces


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split on reply boundaries, never inside one. One thread stays one chunk.

    What the starter did, measured on this corpus: 23 documents became 26
    chunks, the shortest 2 characters. Those three extra chunks are not
    documents that were too long — nothing in the corpus reaches the
    800-character window. They come from the stride. `fallback_split` advances
    `chunk_size - overlap` = 680 characters, so every document between 681 and
    800 characters gets a second window that holds only its tail: 793 - 680 =
    113, 739 - 680 = 59, 682 - 680 = 2. The overlap, which exists so a thought
    isn't lost at a boundary, is what manufactured `t.` and `nd it's the only
    reason I got mine back`.

    So the decision the brief asks for — should one post stay one chunk — has
    a clear answer here. A thread is a question with its answers underneath it;
    a reply that loses its question is close to useless, and every one of my 23
    documents already fits inside the window. One thread, one chunk.

    Chunk size: 800 characters, kept from the starter. It is above my longest
    document (793), so on this corpus it acts as a ceiling for growth rather
    than a knife, and nothing currently splits at all.

    Overlap: no character overlap. It was the cause of the damage, and the
    thing it protects against — a piece that doesn't say what it is about —
    I handle instead by repeating the THREAD line at the top of every piece
    when a thread does have to come apart. That is the context the overlap was
    trying and failing to preserve.

    Above the ceiling, threads split between replies, never inside one. Only a
    single reply longer than 800 characters falls back to a sentence split,
    which no document in this corpus currently triggers.
    """
    limit = config.CHUNK_SIZE
    chunks: list[Chunk] = []

    for doc in documents:
        text = doc.text.strip()
        header, blocks = _segments(text)

        if len(text) <= limit:
            pieces = [text]
        elif not blocks:
            pieces = _by_sentence(text, limit)
        else:
            pieces = []
            current = header
            for block in blocks:
                candidate = f"{current}\n\n{block}" if current else block
                if current and len(candidate) > limit:
                    pieces.append(current)
                    current = f"{header}\n\n{block}" if header else block
                    if len(current) > limit:
                        *full, current = _by_sentence(current, limit)
                        pieces.extend(full)
                else:
                    current = candidate
            if current:
                pieces.append(current)

        for index, piece in enumerate(p for p in pieces if p.strip()):
            chunks.append(
                Chunk(
                    text=piece,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
