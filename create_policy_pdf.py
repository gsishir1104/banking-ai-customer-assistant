from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import inch


INPUT_FILE = "data/banking_policy.txt"
OUTPUT_FILE = "data/banking_policy.pdf"


def create_pdf():
    document = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=LETTER,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()
    normal_style = styles["BodyText"]
    normal_style.alignment = TA_LEFT
    normal_style.leading = 14

    story = []

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()

        if not line:
            story.append(Spacer(1, 0.15 * inch))
        else:
            story.append(Paragraph(line, normal_style))

    document.build(story)

    print(f"PDF created successfully: {OUTPUT_FILE}")


if __name__ == "__main__":
    create_pdf()