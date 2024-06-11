from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr(path:str)->str:
# Path to the single image
    image = Image.open(path)
    return pytesseract.image_to_string(image, lang='kor+eng')
