# --- F:\Sahaj\Python\StudySage\TGB BOT\export_pdf.py ---
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from datetime import datetime
import os

def export_summary_to_pdf(summary):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"summary_{timestamp}.pdf")

    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, spaceAfter=30, textColor=colors.HexColor('#1E88E5'))
    subtitle_style = ParagraphStyle('CustomSubtitle', parent=styles['Heading2'], fontSize=16, spaceAfter=20, textColor=colors.HexColor('#424242'))
    body_style = ParagraphStyle('CustomBody', parent=styles['Normal'], fontSize=12, spaceAfter=12, leading=16)

    content = []
    logo_path = "assets/images/logo.png"
    if os.path.exists(logo_path):
        try:
            content.append(Image(logo_path, width=2*inch, height=2*inch))
            content.append(Spacer(1, 20))
        except Exception:
            pass

    content.append(Paragraph("StudySage Summary", title_style))
    content.append(Spacer(1, 20))
    content.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subtitle_style))
    content.append(Spacer(1, 30))
    content.append(Paragraph("Summary:", subtitle_style))
    content.append(Spacer(1, 10))

    for para in summary.split('\n\n'):
        if para.strip():
            content.append(Paragraph(para.strip(), body_style))
            content.append(Spacer(1, 10))

    doc.build(content)
    print(f"📄 PDF exported to: {output_file}")
    return output_file

def export_quiz_to_pdf(questions):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"quiz_{timestamp}.pdf")

    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, spaceAfter=30, textColor=colors.HexColor('#1E88E5'))
    subtitle_style = ParagraphStyle('CustomSubtitle', parent=styles['Heading2'], fontSize=16, spaceAfter=20, textColor=colors.HexColor('#424242'))
    question_style = ParagraphStyle('QuestionStyle', parent=styles['Normal'], fontSize=14, spaceAfter=12, leading=18)
    option_style = ParagraphStyle('OptionStyle', parent=styles['Normal'], fontSize=12, spaceAfter=8, leading=16, leftIndent=20)
    answer_style = ParagraphStyle('AnswerStyle', parent=styles['Normal'], fontSize=12, spaceAfter=20, leading=16, leftIndent=20, textColor=colors.HexColor('#2E7D32'))

    content = []
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        try:
            content.append(Image(logo_path, width=2*inch, height=2*inch))
            content.append(Spacer(1, 20))
        except Exception:
            pass

    content.append(Paragraph("StudySage Quiz", title_style))
    content.append(Spacer(1, 20))
    content.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subtitle_style))
    content.append(Spacer(1, 30))

    for i, q in enumerate(questions, 1):
        content.append(Paragraph(f"Question {i}:", subtitle_style))
        content.append(Paragraph(q["question"], question_style))
        content.append(Spacer(1, 10))
        for j, option in enumerate(q["options"], 1):
            content.append(Paragraph(f"{j}. {option}", option_style))
        content.append(Spacer(1, 10))
        content.append(Paragraph(f"Correct Answer: {q['answer']}", answer_style))
        content.append(Spacer(1, 20))

    doc.build(content)
    print(f"📄 PDF exported to: {output_file}")
    return output_file
