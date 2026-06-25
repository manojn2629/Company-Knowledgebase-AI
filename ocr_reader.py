from PIL import Image
import pytesseract
from pdf2image import convert_from_path

# Windows Tesseract path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\manoj.n3\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)


def extract_ocr_text(file_path):
    try:
        text = ""

        # If PDF → convert pages to images
        if file_path.endswith(".pdf"):
            pages = convert_from_path(file_path)

            for page in pages:
                text += pytesseract.image_to_string(
                    page
                )

        # If image file
        elif file_path.endswith(
            (".png", ".jpg", ".jpeg")
        ):
            image = Image.open(file_path)

            text = pytesseract.image_to_string(
                image
            )

        return text.strip()

    except Exception as e:
        print(f"OCR Error: {e}")
        return ""