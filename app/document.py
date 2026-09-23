import pymupdf


PDF_PATH = "data/banking_policy.pdf"


def extract_text_from_pdf(pdf_path):
    document = pymupdf.open(pdf_path)

    pages = []

    for page in document:
        text = page.get_text()
        pages.append(text)

    document.close()

    return pages


if __name__ == "__main__":
    pages = extract_text_from_pdf(PDF_PATH)

    print(f"Number of pages: {len(pages)}")

    print("\n--- FIRST PAGE ---\n")
    print(pages[0])