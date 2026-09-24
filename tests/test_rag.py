from fastapi.testclient import TestClient
from sentence_transformers import SentenceTransformer

from app.chunker import chunk_policy
from app.document import extract_text_from_pdf
from app.search import build_search_index, search


PDF_PATH = "data/banking_policy.pdf"
MODEL_NAME = "all-MiniLM-L6-v2"


def setup_search():
    pages = extract_text_from_pdf(PDF_PATH)
    all_text = "\n".join(pages)

    chunks = chunk_policy(all_text)

    model = SentenceTransformer(
        MODEL_NAME,
        local_files_only=True
    )

    index = build_search_index(chunks, model)

    return chunks, model, index


def test_address_question_retrieves_address_policy():
    chunks, model, index = setup_search()

    question = "What documents are required to change my address?"

    results = search(
        question,
        chunks,
        index,
        model,
        top_k=2,
    )

    assert len(results) > 0

    retrieved_text = " ".join(
        result["chunk"] for result in results
    ).lower()

    assert "address change policy" in retrieved_text
    assert "government-issued photo id" in retrieved_text
    assert "proof of the new address" in retrieved_text


def test_unsupported_question_returns_no_results():
    chunks, model, index = setup_search()

    question = "How can I apply for a home loan?"

    results = search(
        question,
        chunks,
        index,
        model,
        top_k=2,
    )

    assert len(results) == 0


def test_unauthorized_transaction_requires_human_review():
    from app.llm import AIAnswer
    from app.main import requires_human_review

    question = "Someone used my card without permission."

    answer = AIAnswer(
        answer="This case requires human review.",
        source="Unauthorized Card Transaction",
    )

    result = requires_human_review(
        question,
        answer,
    )

    assert result is True


def test_ask_api_returns_expected_fields():
    from app.main import app

    client = TestClient(app)

    response = client.post(
        "/ask",
        json={
            "question": "What documents are required to change my address?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "source" in data
    assert "requires_human_review" in data

    assert data["requires_human_review"] is False