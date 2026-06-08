from pathlib import Path

from backend.app.schemas.evidence import RetrievedChunk


DEFAULT_POLICY_SET = "hipaa"
CORPUS_ROOT = Path("data/corpus")


def list_policy_sets(corpus_root: str = "data/corpus") -> list[str]:
    root = Path(corpus_root)

    if not root.exists():
        return []

    return sorted(
        path.name
        for path in root.iterdir()
        if path.is_dir()
    )


def _resolve_policy_dir(policy_set: str, corpus_root: str = "data/corpus") -> Path:
    available = list_policy_sets(corpus_root)
    selected = policy_set if policy_set in available else DEFAULT_POLICY_SET
    return Path(corpus_root) / selected


def load_policy_chunks(
    corpus_dir: str = "data/corpus",
    policy_set: str = DEFAULT_POLICY_SET,
) -> list[RetrievedChunk]:
    chunks: list[RetrievedChunk] = []
    policy_dir = _resolve_policy_dir(policy_set, corpus_dir)

    for path in policy_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        for index, paragraph in enumerate(paragraphs):
            chunks.append(
                RetrievedChunk(
                    chunk_id=f"{policy_set}:{path.stem}-{index}",
                    source=str(path),
                    text=paragraph,
                )
            )

    return chunks


def retrieve(
    question: str,
    limit: int = 3,
    policy_set: str = DEFAULT_POLICY_SET,
) -> list[RetrievedChunk]:
    chunks = load_policy_chunks(policy_set=policy_set)
    query_terms = set(question.lower().split())

    scored = []
    for chunk in chunks:
        chunk_terms = set(chunk.text.lower().split())
        score = len(query_terms.intersection(chunk_terms))
        scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for score, chunk in scored[:limit] if score > 0]
