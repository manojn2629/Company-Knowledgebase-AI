import pdfplumber


def extract_chart_text(pdf_path):
    chart_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words()

            for word in words:
                chart_data.append(
                    word["text"]
                )

    return chart_data