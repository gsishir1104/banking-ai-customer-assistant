from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from app.chunker import chunk_policy
from app.document import extract_text_from_pdf
from app.search import build_search_index, search, get_context
from app.llm import generate_answer


app = FastAPI(
    title="Banking AI Customer Assistant",
    description="RAG-based banking policy assistant",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_origin_regex=r"https://.*\.app\.github\.dev",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


PDF_PATH = "data/banking_policy.pdf"
MODEL_NAME = "all-MiniLM-L6-v2"


# Load policy document
pages = extract_text_from_pdf(
    PDF_PATH
)

# Create policy chunks with page numbers
chunks = chunk_policy(
    pages
)


# Load embedding model
model = SentenceTransformer(
    MODEL_NAME
)


# Build FAISS search index
index = build_search_index(
    chunks,
    model
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Banking AI Customer Assistant is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


def requires_human_review(
    question,
    answer
):
    """
    Deterministic business rules for human review.

    The LLM does not control this decision.
    """

    question_lower = question.lower()

    sensitive_terms = [
        "fraud",
        "fraudulent",
        "unauthorized",
        "without permission",
        "stolen",
        "lost card",
        "card is lost",
        "debit card is lost",
        "lost debit card",
        "duplicate charge",
        "charged twice",
    ]

    for term in sensitive_terms:

        if term in question_lower:
            return True

    if answer.source == "None":
        return True

    return False


@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    results = search(
        request.question,
        chunks,
        index,
        model,
        top_k=2,
    )

    context = get_context(
        results
    )

    answer = generate_answer(
        request.question,
        context,
    )

    human_review = requires_human_review(
        request.question,
        answer,
    )

    # Use the first retrieved result
    # as the source page.
    page = None

    if results:
        page = results[0]["page"]

    return {
        "answer": answer.answer,
        "source": answer.source,
        "page": page,
        "requires_human_review": human_review,
    }