from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def create_embeddings(chunks):
    model = SentenceTransformer(MODEL_NAME)

    embeddings = model.encode(chunks)

    return embeddings


if __name__ == "__main__":
    sample_chunks = [
        "Customers need government-issued identification and proof of address.",
        "Customers can request a phone number change.",
        "Lost debit cards must be reported immediately.",
    ]

    embeddings = create_embeddings(sample_chunks)

    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Embedding size: {len(embeddings[0])}")