from pathlib import Path
from backend.app.schemas.evidence import RetrievedChunk


def load_policy_chunks(corpus_dir: str = "data/corpus") -> list[RetrievedChunk]:
    chunks: list[RetrievedChunk] = []

    for path in Path(corpus_dir).glob("*.md"):
        text = path.read_text(encoding="utf-8")
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        for index, paragraph in enumerate(paragraphs):
            chunks.append(
                RetrievedChunk(
                    chunk_id=f"{path.stem}-{index}",
                    source=str(path),
                    text=paragraph,
                )
            )

    return chunks


def retrieve(question: str, limit: int = 3) -> list[RetrievedChunk]:
    chunks = load_policy_chunks()
    query_terms = set(question.lower().split())

    scored = []
    for chunk in chunks:
        chunk_terms = set(chunk.text.lower().split())
        score = len(query_terms.intersection(chunk_terms))
        scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for score, chunk in scored[:limit] if score > 0]
