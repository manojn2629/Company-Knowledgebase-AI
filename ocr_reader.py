from PIL import Image
import pytesseract

# Windows Tesseract path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\manoj.n3\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)


def extract_ocr_text(image_path):
    try:
        image = Image.open(image_path)

        text = pytesseract.image_to_string(
            image
        )

        return text.strip()

    except Exception as e:
        print(f"OCR Error: {e}")
        return ""