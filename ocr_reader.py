<<<<<<< HEAD
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
=======
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path, lang='eng'):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang=lang).strip()
        
        # Auto-detect bad scan
        if not text or len(text) < 20 or all(c in '!@#$%^&*()_+=-' for c in text[:10]):
            return None  # Bad scan or empty
        return text
    except Exception as e:
        return None
>>>>>>> 466d9410b23ea12dced9bc15ca58d72f3affe172
