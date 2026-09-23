import re

from document import extract_text_from_pdf


PDF_PATH = "data/banking_policy.pdf"


def chunk_policy(text):
    # Put PDF text into one continuous line
    text = text.replace("\n", " ")

    # These are the actual policy sections.
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

    # Create one regex that matches ONLY our real policy headings.
    pattern = "(" + "|".join(re.escape(title) for title in policy_titles) + ")"

    # Split at the exact policy headings.
    parts = re.split(pattern, text)

    chunks = []

    current_chunk = ""

    for part in parts:
        part = part.strip()

        if not part:
            continue

        # If this part is an actual policy heading,
        # start a new chunk.
        if part in policy_titles:

            if current_chunk:
                chunks.append(current_chunk.strip())

            current_chunk = part

        else:
            current_chunk += " " + part

    # Add final chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


if __name__ == "__main__":
    pages = extract_text_from_pdf(PDF_PATH)

    all_text = "\n".join(pages)

    chunks = chunk_policy(all_text)

    print(f"Total chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):
        print(f"\n--- CHUNK {index} ---")
        print(chunk)