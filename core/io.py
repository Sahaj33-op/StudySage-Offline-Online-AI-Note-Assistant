# core/io.py
import os
from pathlib import Path
import fitz  # PyMuPDF
from typing import Callable, Optional
from core.ocr_reader import extract_text_from_image

# Import configuration
try:
    from config import OUTPUT_DIR
except ImportError:
    OUTPUT_DIR = "output"

Progress = Optional[Callable[[str, int, int], None]]

def load_text_from_file(file_path: str, lang: str = "auto", force_ocr: bool = False, progress_callback: Progress = None) -> str:
    """
    Unified loader for .txt/.md/.csv, images, and PDFs.
    - PDFs: try text layer first; if empty OR force_ocr=True, rasterize @300 DPI and OCR.
    - Images: aggressive OCR pipeline (screen-photo friendly) with auto language re-run.
    """
    p = Path(file_path)
    ext = p.suffix.lower()

    if ext in {".txt", ".md", ".py", ".json", ".csv"}:
        return p.read_text(encoding="utf-8", errors="ignore")

    if ext in {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}:
        if progress_callback: progress_callback("Running OCR on image", 0, 0)
        return extract_text_from_image(p.as_posix(), lang=lang) or ""

    if ext == ".pdf":
        return _extract_pdf_text_or_ocr(p, lang=lang, force_ocr=force_ocr, progress_callback=progress_callback)

    raise ValueError(f"Unsupported file format: {ext}")

def _extract_pdf_text_or_ocr(pdf_path: Path, lang: str, force_ocr: bool, progress_callback: Progress) -> str:
    if progress_callback: progress_callback("Extracting PDF (text layer)", 0, 0)
    doc = fitz.open(pdf_path.as_posix())

    # 1) Text layer pass (unless forced OCR)
    text_chunks = []
    if not force_ocr:
        for i in range(len(doc)):
            page = doc.load_page(i)
            t = page.get_text("text") or ""
            if t.strip():
                text_chunks.append(t.strip())
        if text_chunks:
            return "\n".join(text_chunks).strip()

    # 2) Forced/fallback OCR
    if progress_callback: progress_callback("OCR PDF pages", 0, len(doc))
    out = []
    tmp_dir = Path(OUTPUT_DIR); tmp_dir.mkdir(exist_ok=True)
    for i in range(len(doc)):
        if progress_callback: progress_callback("OCR PDF pages", i + 1, len(doc))
        page = doc.load_page(i)
        pix = page.get_pixmap(dpi=300)
        tmp = tmp_dir / f"_page_{i}.png"
        pix.save(tmp.as_posix())
        try:
            txt = extract_text_from_image(tmp.as_posix(), lang=lang) or ""
            if txt.strip():
                out.append(txt.strip())
        finally:
            try: tmp.unlink()
            except: pass
    return "\n".join(out).strip()

def process_file(file_path: str, mode: str = "offline", api_key: str = None,
                 min_length: int = 30, max_length: int = 200,
                 lang: str = "auto", progress_callback: Progress = None) -> str:
    """
    Convenience wrapper used by apps: load -> summarize via core.summarize.
    """
    text = load_text_from_file(file_path, lang=lang, force_ocr=False, progress_callback=progress_callback)
    if not text.strip():
        return "No text could be extracted from the file."
    from core.summarize import summarize_text
    config = {"mode": mode, "api_key": api_key or ""}
    return summarize_text(text, min_length, max_length, config, progress_callback=progress_callback)