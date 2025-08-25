# core/io.py
import os
from pathlib import Path
import fitz  # PyMuPDF
from core.ocr_reader import extract_text_from_image
from core.summarize import summarize_text

def load_text_from_file(file_path: str, lang: str = "auto", force_ocr: bool = False) -> str:
    ext = Path(file_path).suffix.lower()
    if ext in {".txt", ".md", ".py", ".json", ".csv"}:
        return Path(file_path).read_text(encoding="utf-8", errors="ignore")

    if ext == ".pdf":
        if force_ocr:
            return _ocr_pdf(file_path, lang=lang)
        text = _extract_pdf_text(file_path)
        return text if text.strip() else _ocr_pdf(file_path, lang=lang)

    if ext in {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}:
        return extract_text_from_image(file_path, lang=lang) or ""

    raise ValueError(f"Unsupported file: {ext}")

def _extract_pdf_text(file_path: str) -> str:
    out = []
    doc = fitz.open(file_path)
    for i in range(len(doc)):
        page = doc.load_page(i)
        t = page.get_text("text") or ""
        if t.strip():
            out.append(t.strip())
    return "\n".join(out)

def _ocr_pdf(file_path: str, lang: str = "auto") -> str:
    Path("output").mkdir(exist_ok=True)
    doc = fitz.open(file_path)
    out = []
    for i in range(len(doc)):
        page = doc.load_page(i)
        pix = page.get_pixmap(dpi=300)
        tmp = Path("output") / f"_page_{i}.png"
        pix.save(tmp.as_posix())
        try:
            txt = extract_text_from_image(tmp.as_posix(), lang=lang)
            if txt.strip():
                out.append(txt.strip())
        finally:
            try: os.remove(tmp)
            except: pass
    return "\n".join(out).strip()

def process_file(file_path: str, mode="offline", api_key=None, min_length=30, max_length=200, lang: str = "auto"):
    text = load_text_from_file(file_path, lang=lang)
    if not text.strip():
        return "No text could be extracted from the file. The file may be empty, contain no recognizable text, or OCR may have failed."
    config = {"mode": mode, "api_key": api_key or ""}
    return summarize_text(text, min_length, max_length, config)
