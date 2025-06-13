from PIL import Image
import pytesseract
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path: str, lang: str = 'eng') -> str:
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        with Image.open(image_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            text = pytesseract.image_to_string(img, lang=lang).strip()
            
            if not text:
                logger.warning("No text could be extracted from the image")
                return ""
                
            return text

    except Exception as e:
        logger.error(f"Failed to process image: {str(e)}")
        return ""
