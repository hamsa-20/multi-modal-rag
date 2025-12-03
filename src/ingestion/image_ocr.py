import pytesseract
from PIL import Image

def ocr_image(path):
    try:
        img = Image.open(path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception:
        return ""
