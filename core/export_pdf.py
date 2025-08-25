# core/export_pdf.py
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from pathlib import Path
from typing import List, Dict

LOGO = Path("assets/images/logo.png")  # single place
OUTDIR = Path("output"); OUTDIR.mkdir(exist_ok=True)

def _draw_header(cnv: canvas.Canvas, title: str):
    if LOGO.exists():
        try:
            cnv.drawImage(ImageReader(LOGO.as_posix()), 40, 780, width=60, height=60, preserveAspectRatio=True, mask='auto')
        except Exception:
            pass
    cnv.setFont("Helvetica-Bold", 16)
    cnv.drawString(120, 810, "StudySage")
    cnv.setFont("Helvetica", 12)
    cnv.drawString(120, 790, title)
    cnv.line(40, 775, 555, 775)

def export_summary_to_pdf(summary: str) -> str:
    out = OUTDIR / "summary.pdf"
    cnv = canvas.Canvas(out.as_posix(), pagesize=A4)
    _draw_header(cnv, "Summary")
    cnv.setFont("Helvetica", 11)
    width, height = A4
    x, y = 40, 750
    for line in summary.splitlines():
        if y < 60:
            cnv.showPage(); _draw_header(cnv, "Summary"); cnv.setFont("Helvetica", 11); y = 750
        cnv.drawString(x, y, line[:110])
        y -= 16
    cnv.save()
    return out.as_posix()

def export_quiz_to_pdf(questions: List[Dict[str, object]]) -> str:
    out = OUTDIR / "quiz.pdf"
    cnv = canvas.Canvas(out.as_posix(), pagesize=A4)
    _draw_header(cnv, "Quiz")
    cnv.setFont("Helvetica", 11)
    width, height = A4
    x, y = 40, 750
    for i, q in enumerate(questions, 1):
        block = [f"Q{i}. {q['question']}"] + [f"  {j}. {opt}" for j, opt in enumerate(q['options'], 1)] + [f"  ✅ Answer: {q['answer']}", ""]
        for line in block:
            if y < 60:
                cnv.showPage(); _draw_header(cnv, "Quiz"); cnv.setFont("Helvetica", 11); y = 750
            cnv.drawString(x, y, str(line)[:110]); y -= 16
    cnv.save()
    return out.as_posix()
