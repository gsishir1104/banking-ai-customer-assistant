import json

from sentence_transformers import SentenceTransformer

from app.chunker import chunk_policy
from app.document import extract_text_from_pdf
from app.search import build_search_index, search
from app.llm import AIAnswer
from app.main import requires_human_review


PDF_PATH = "data/banking_policy.pdf"
MODEL_NAME = "all-MiniLM-L6-v2"


def load_evaluation_questions():
    with open("evaluation/questions.json", "r") as file:
        return json.load(file)


def setup_search():
    pages = extract_text_from_pdf(PDF_PATH)
    all_text = "\n".join(pages)

    chunks = chunk_policy(all_text)

    model = SentenceTransformer(
        MODEL_NAME,
        local_files_only=True
    )

    index = build_search_index(
        chunks,
        model
    )

    return chunks, model, index


def evaluate():
    questions = load_evaluation_questions()

    chunks, model, index = setup_search()

    total = len(questions)

    source_correct = 0
    review_correct = 0

    print(f"Evaluating {total} questions...\n")

    for number, item in enumerate(questions, start=1):

        question = item["question"]
        expected_source = item["expected_source"]
        expected_review = item["expected_human_review"]

        results = search(
            question,
            chunks,
            index,
            model,
            top_k=2,
        )

        # Check whether the expected policy was retrieved.
        if results:

            retrieved_text = results[0]["chunk"]

            source_correct_for_question = (
                expected_source.lower()
                in retrieved_text.lower()
            )

        else:

            source_correct_for_question = (
                expected_source == "None"
            )

        # Create an answer object for testing
        # the application's human-review rules.
        if expected_source == "None":

            answer = AIAnswer(
                answer="Information not found.",
                source="None",
            )

        else:

            answer = AIAnswer(
                answer="Evaluation answer.",
                source=expected_source,
            )

        actual_review = requires_human_review(
            question,
            answer,
        )

        if source_correct_for_question:
            source_correct += 1

        if actual_review == expected_review:
            review_correct += 1

        print(f"{number}. {question}")

        print(
            f"   Expected source: "
            f"{expected_source}"
        )

        print(
            f"   Source correct: "
            f"{source_correct_for_question}"
        )

        print(
            f"   Expected human review: "
            f"{expected_review}"
        )

        print(
            f"   Human review correct: "
            f"{actual_review == expected_review}"
        )

        print()


    source_accuracy = (
        source_correct / total
    ) * 100

    review_accuracy = (
        review_correct / total
    ) * 100


    print("================================")
    print("EVALUATION RESULTS")
    print("================================")

    print(
        f"Source accuracy: "
        f"{source_accuracy:.1f}%"
    )

    print(
        f"Human-review accuracy: "
        f"{review_accuracy:.1f}%"
    )

    print(
        f"Questions evaluated: "
        f"{total}"
    )


if __name__ == "__main__":
    evaluate()