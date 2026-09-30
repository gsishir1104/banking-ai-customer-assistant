from pydantic import BaseModel


class AIAnswer(BaseModel):
    answer: str
    source: str
    requires_human_review: bool


def generate_answer(question, context):
    """
    Temporary mock LLM.

    This simulates what a real LLM will eventually do.
    No API key or internet connection is required.
    """

    if not context:
        return AIAnswer(
            answer=(
                "I couldn't find this information in the provided "
                "banking policy document."
            ),
            source="None",
            requires_human_review=True,
        )

    question_lower = question.lower()

    if "address" in question_lower:
        return AIAnswer(
            answer=(
                "Customers need a government-issued photo ID, "
                "proof of the new address, and a completed "
                "address-change form."
            ),
            source="Address Change Policy",
            requires_human_review=False,
        )

    if "phone" in question_lower:
        return AIAnswer(
            answer=(
                "Customers need government ID, existing account "
                "information, and the new phone number."
            ),
            source="Phone Number Change Policy",
            requires_human_review=False,
        )

    if "lost" in question_lower or "stolen" in question_lower:
        return AIAnswer(
            answer=(
                "The customer should contact the bank immediately. "
                "The employee should verify identity, temporarily "
                "block the card, and record the incident."
            ),
            source="Lost or Stolen Debit Card",
            requires_human_review=True,
        )

    return AIAnswer(
        answer=(
            "I found relevant policy information, but the temporary "
            "mock LLM cannot generate an answer for this question yet."
        ),
        source="Banking Policy",
        requires_human_review=True,
    )