import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.chunker import chunk_policy
from app.document import extract_text_from_pdf


PDF_PATH = "data/banking_policy.pdf"
MODEL_NAME = "all-MiniLM-L6-v2"

# Smaller distance = more similar
MAX_DISTANCE = 1.0


def build_search_index(chunks, model):
    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(texts)

    embeddings = np.array(
        embeddings
    ).astype("float32")

    index = faiss.IndexFlatL2(
        embeddings.shape[1]
    )

    index.add(embeddings)

    return index


def search(
    query,
    chunks,
    index,
    model,
    top_k=2
):
    query_embedding = model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for distance, index_number in zip(
        distances[0],
        indices[0]
    ):
        distance = float(distance)

        # Ignore weak matches
        if distance > MAX_DISTANCE:
            continue

        results.append({
            "chunk": chunks[index_number]["text"],
            "page": chunks[index_number]["page"],
            "distance": distance
        })

    return results


def get_context(results):
    if not results:
        return None

    context_parts = []

    for result in results:
        context_parts.append(
            result["chunk"]
        )

    return "\n\n".join(
        context_parts
    )


if __name__ == "__main__":

    # 1. Read PDF
    pages = extract_text_from_pdf(
        PDF_PATH
    )

    # 2. Create chunks with page numbers
    chunks = chunk_policy(pages)

    print(
        f"Total chunks: {len(chunks)}"
    )

    # 3. Load embedding model
    print(
        "\nLoading embedding model..."
    )

    model = SentenceTransformer(
        MODEL_NAME,
        local_files_only=True
    )

    # 4. Build FAISS index
    print(
        "Building FAISS index..."
    )

    index = build_search_index(
        chunks,
        model
    )

    # 5. Test question
    query = (
        "What documents are required "
        "to change my address?"
    )

    print("\nQUESTION:")
    print(query)

    # 6. Search
    results = search(
        query,
        chunks,
        index,
        model,
        top_k=2
    )

    # 7. Display results
    print("\nRELEVANT RESULTS:")

    if not results:

        print(
            "No relevant policy information "
            "was found."
        )

    else:

        for number, result in enumerate(
            results,
            start=1
        ):

            print(
                f"\n--- RESULT {number} ---"
            )

            print(
                f"Distance: "
                f"{result['distance']:.4f}"
            )

            print(
                f"Page: {result['page']}"
            )

            print(
                result["chunk"]
            )

    # 8. Create context for LLM
    context = get_context(
        results
    )

    print("\n--- LLM CONTEXT ---")

    if context:
        print(context)

    else:
        print(
            "No context available."
        )