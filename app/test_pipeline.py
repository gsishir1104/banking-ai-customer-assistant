from sentence_transformers import SentenceTransformer

from app.chunker import chunk_policy
from app.document import extract_text_from_pdf
from app.search import build_search_index, search, get_context
from app.llm import generate_answer


PDF_PATH = "data/banking_policy.pdf"
MODEL_NAME = "all-MiniLM-L6-v2"


# 1. Read PDF
pages = extract_text_from_pdf(PDF_PATH)

# 2. Create policy chunks
all_text = "\n".join(pages)
chunks = chunk_policy(all_text)

print(f"Total chunks: {len(chunks)}")


# 3. Load embedding model
print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME, local_files_only=True)


# 4. Build FAISS index
print("Building FAISS index...")
index = build_search_index(chunks, model)


# 5. Ask a question
question = "What documents are required to change my address?"

print("\nQUESTION:")
print(question)


# 6. Search the policy
results = search(
    question,
    chunks,
    index,
    model,
    top_k=2
)


# 7. Create context
context = get_context(results)


print("\nRETRIEVED CONTEXT:")
print(context)


# 8. Send context to mock LLM
answer = generate_answer(question, context)


print("\nFINAL AI ANSWER:")
print(answer)