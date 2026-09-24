from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel


load_dotenv()

client = OpenAI()


class AIAnswer(BaseModel):
    answer: str
    source: str


def generate_answer(question, context):
    """
    Generate a structured answer using OpenAI.

    The model answers only from the retrieved
    banking policy context.
    """

    if not context:
        return AIAnswer(
            answer=(
                "I couldn't find this information in the "
                "provided banking policy document."
            ),
            source="None",
        )

    response = client.responses.parse(
        model="gpt-5.6-luna",
        input=[
            {
                "role": "system",
                "content": (
                    "You are a banking policy assistant for bank employees.\n\n"
                    "Answer ONLY using the provided banking policy context.\n"
                    "Do not invent information.\n"
                    "If the context does not contain enough information, "
                    "say that the information was not found.\n"
                    "Return a concise and professional answer.\n"
                    "Do not decide whether human review is required. "
                    "The application will determine that separately."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Customer/employee question:\n{question}\n\n"
                    f"Banking policy context:\n{context}"
                ),
            },
        ],
        text_format=AIAnswer,
    )

    return response.output_parsed