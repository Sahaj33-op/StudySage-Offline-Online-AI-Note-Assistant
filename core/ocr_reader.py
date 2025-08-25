# core/ocr_reader.py
import os
from typing import Optional, Tuple
from PIL import Image
import numpy as np
import pytesseract

# Windows Tesseract autodetect
if os.name == "nt":
    try:
        if not getattr(pytesseract.pytesseract, "tesseract_cmd", None):
            p = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            if os.path.exists(p):
                pytesseract.pytesseract.tesseract_cmd = p
    except Exception:
        pass

_LANG_MAP = {
    "en": "eng", "hi": "hin", "gu": "guj", "bn": "ben", "ta": "tam",
    "te": "tel", "mr": "mar", "pa": "pan", "ur": "urd", "kn": "kan",
    "ml": "mal", "or": "ori", "sa": "san"
}

def _detect_lang_code(sample_text: str) -> Tuple[Optional[str], float]:
    sample = (sample_text or "").strip()
    if not sample:
        return None, 0.0
    try:
        from langdetect import detect_langs
        cands = detect_langs(sample[:1000])
        if not cands:
            return None, 0.0
        best = max(cands, key=lambda x: x.prob)
        tess = _LANG_MAP.get(best.lang)
        return (tess, best.prob if tess else 0.0)
    except Exception:
        return None, 0.0

def _cv2_preprocess_screen(image_path: str) -> Optional[Image.Image]:
    try:
        import cv2
        img = cv2.imread(image_path)
        if img is None:
            return None

        # Pre-resize huge photos
        h0, w0 = img.shape[:2]
        max_side = max(h0, w0)
        if max_side > 2200:
            scale = 2200 / max_side
            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

        # Denoise (helps moiré), then grayscale
        img = cv2.fastNlMeansDenoisingColored(img, None, 5, 5, 7, 21)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        dark_ui = float(np.mean(gray)) < 110  # heuristic

        # Unsharp mask
        blur = cv2.GaussianBlur(gray, (0, 0), 1.2)
        sharp = cv2.addWeighted(gray, 1.6, blur, -0.6, 0)

        # Gamma boost for dark UIs
        if dark_ui:
            inv_gamma = 1.0 / 1.3
            table = (np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8"))
            sharp = cv2.LUT(sharp, table)

        # Adaptive threshold; invert for dark UI
        th = cv2.adaptiveThreshold(sharp, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10)
        if dark_ui:
            th = cv2.bitwise_not(th)

        # Light morphology + upscale if tiny
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        th = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=1)
        h, w = th.shape[:2]
        if min(h, w) < 900:
            th = cv2.resize(th, None, fx=1.7, fy=1.7, interpolation=cv2.INTER_CUBIC)

        return Image.fromarray(th)
    except Exception:
        return None

def _tesseract(pil_img: Image.Image, lang: str, psm: int) -> str:
    cfg = f"--oem 3 --psm {psm} -c preserve_interword_spaces=1"
    try:
        return pytesseract.image_to_string(pil_img, lang=lang, config=cfg, timeout=30) or ""
    except Exception:
        return ""

def extract_text_from_image(image_path: str, lang: str = "auto") -> str:
    pil = _cv2_preprocess_screen(image_path)
    if pil is None:
        try:
            pil = Image.open(image_path).convert("L")
        except Exception:
            return ""

    psms = [6, 3]  # block-of-text, then auto-layout

    if lang != "auto":
        for p in psms:
            out = _tesseract(pil, lang, p)
            if len(out.strip()) >= 10:
                return out
        return _tesseract(pil, lang, 6)

    # AUTO: Pass 1: English
    best = ""
    for p in psms:
        t = _tesseract(pil, "eng", p)
        if len(t) > len(best):
            best = t

    stripped = (best or "").strip()
    det_lang, prob = _detect_lang_code(stripped)

    import re
    latin = re.sub(r"[^A-Za-z]+", "", stripped or "")
    latin_ratio = len(latin) / max(len((stripped or "").replace(" ", "")), 1)

    should_try_other = (len(stripped) < 30) or (latin_ratio < 0.25) or (det_lang and det_lang != "eng" and prob >= 0.70)

    if should_try_other:
        tried = set()
        if det_lang:
            tried.add(det_lang)
            combo = "eng+" + det_lang if det_lang != "eng" else "eng"
            for p in psms:
                t = _tesseract(pil, combo, p)
                if len(t.strip()) > len(best.strip()):
                    best = t
        for guess in ("hin", "guj", "ben", "mar", "tam", "tel"):
            if guess in tried:
                continue
            combo = "eng+" + guess
            for p in psms:
                t = _tesseract(pil, combo, p)
                if len(t.strip()) > len(best.strip()):
                    best = t

    return best or ""
