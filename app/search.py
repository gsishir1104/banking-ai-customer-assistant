import re
from collections import Counter

from app.chunker import chunk_policy
from app.document import extract_text_from_pdf


PDF_PATH = "data/banking_policy.pdf"

# Minimum similarity required for a result
MIN_SCORE = 0.05


def tokenize(text):
    """Convert text into simple lowercase words."""
    return re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())


def build_search_index(chunks):
    """Build a lightweight TF-IDF-style search index."""
    document_tokens = []
    document_frequency = Counter()

    for chunk in chunks:
        tokens = set(tokenize(chunk["text"]))
        document_tokens.append(tokens)

        for token in tokens:
            document_frequency[token] += 1

    return {
        "chunks": chunks,
        "document_tokens": document_tokens,
        "document_frequency": document_frequency,
        "total_documents": len(chunks),
    }


def search(query, search_index, top_k=2):
    """Find the most relevant policy chunks using keyword similarity."""

    query_tokens = set(tokenize(query))

    if not query_tokens:
        return []

    chunks = search_index["chunks"]
    document_tokens = search_index["document_tokens"]
    document_frequency = search_index["document_frequency"]
    total_documents = search_index["total_documents"]

    scored_results = []

    for position, tokens in enumerate(document_tokens):

        if not tokens:
            continue

        matched_tokens = query_tokens.intersection(tokens)

        if not matched_tokens:
            continue

        score = 0.0

        for token in matched_tokens:
            # Simple inverse-document-frequency weighting
            idf = 1.0 + (
                total_documents /
                (1 + document_frequency[token])
            )

            score += idf

        # Normalize by query size
        score = score / len(query_tokens)

        if score >= MIN_SCORE:
            scored_results.append({
                "chunk": chunks[position]["text"],
                "page": chunks[position]["page"],
                "distance": score,
            })

    scored_results.sort(
        key=lambda result: result["distance"],
        reverse=True
    )

    return scored_results[:top_k]


def get_context(results):
    """Combine retrieved chunks into LLM context."""

    if not results:
        return None

    context_parts = []

    for result in results:
        context_parts.append(result["chunk"])

    return "\n\n".join(context_parts)


if __name__ == "__main__":

    # 1. Read PDF
    pages = extract_text_from_pdf(PDF_PATH)

    # 2. Create chunks
    chunks = chunk_policy(pages)

    print(f"Total chunks: {len(chunks)}")

    # 3. Build lightweight search index
    print("\nBuilding lightweight search index...")

    search_index = build_search_index(chunks)

    # 4. Test question
    query = "What documents are required to change my address?"

    print("\nQUESTION:")
    print(query)

    # 5. Search
    results = search(
        query,
        search_index,
        top_k=2
    )

    # 6. Display results
    print("\nRELEVANT RESULTS:")

    if not results:

        print(
            "No relevant policy information was found."
        )

    else:

        for number, result in enumerate(
            results,
            start=1
        ):

            print(f"\n--- RESULT {number} ---")

            print(
                f"Score: "
                f"{result['distance']:.4f}"
            )

            print(
                f"Page: {result['page']}"
            )

            print(
                result["chunk"]
            )

    # 7. Create context
    context = get_context(results)

    print("\n--- LLM CONTEXT ---")

    if context:
        print(context)
    else:
        print("No context available.")