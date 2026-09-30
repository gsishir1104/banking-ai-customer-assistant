import re

from app.document import extract_text_from_pdf


PDF_PATH = "data/banking_policy.pdf"


def chunk_policy(pages):
    policy_titles = [
        "1. ADDRESS CHANGE POLICY",
        "2. PHONE NUMBER CHANGE POLICY",
        "3. EMAIL ADDRESS CHANGE POLICY",
        "4. LOST OR STOLEN DEBIT CARD",
        "5. DUPLICATE CARD CHARGE",
        "6. UNAUTHORIZED CARD TRANSACTION",
        "7. PASSWORD RESET",
        "8. ACCOUNT CLOSURE",
        "9. CUSTOMER COMPLAINTS",
        "10. HUMAN REVIEW POLICY",
    ]

    pattern = "(" + "|".join(
        re.escape(title)
        for title in policy_titles
    ) + ")"

    chunks = []

    for page_number, page_text in enumerate(
        pages,
        start=1
    ):
        page_text = page_text.replace("\n", " ")

        parts = re.split(
            pattern,
            page_text
        )

        current_chunk = ""

        for part in parts:
            part = part.strip()

            if not part:
                continue

            if part in policy_titles:

                if current_chunk:
                    chunks.append({
                        "text": current_chunk.strip(),
                        "page": page_number
                    })

                current_chunk = part

            else:

                current_chunk += " " + part

        if current_chunk:
            chunks.append({
                "text": current_chunk.strip(),
                "page": page_number
            })

    return chunks


if __name__ == "__main__":
    pages = extract_text_from_pdf(PDF_PATH)

    chunks = chunk_policy(pages)

    print(f"Total chunks: {len(chunks)}")

    for index, chunk in enumerate(
        chunks,
        start=1
    ):
        print(f"\n--- CHUNK {index} ---")
        print(f"Page: {chunk['page']}")
        print(chunk["text"])