<<<<<<< HEAD
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from datetime import datetime
import os

def export_summary_to_pdf(summary):
    """Export summary to PDF with proper formatting."""
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"summary_{timestamp}.pdf")
    
    # Create PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#1E88E5')
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        textColor=colors.HexColor('#424242')
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        leading=16
    )
    
    # Build document content
    content = []
    
    # Add logo if exists
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        try:
            img = Image(logo_path, width=2*inch, height=2*inch)
            content.append(img)
            content.append(Spacer(1, 20))
        except Exception as e:
            print(f"Warning: Could not add logo: {str(e)}")
    
    # Add title
    content.append(Paragraph("StudySage Summary", title_style))
    content.append(Spacer(1, 20))
    
    # Add timestamp
    timestamp_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    content.append(Paragraph(timestamp_text, subtitle_style))
    content.append(Spacer(1, 30))
    
    # Add summary content
    content.append(Paragraph("Summary:", subtitle_style))
    content.append(Spacer(1, 10))
    
    # Split summary into paragraphs and add each
    paragraphs = summary.split('\n\n')
    for para in paragraphs:
        if para.strip():
            content.append(Paragraph(para.strip(), body_style))
            content.append(Spacer(1, 10))
    
    # Build PDF
    doc.build(content)
    print(f"📄 PDF exported to: {output_file}")
    return output_file

def export_quiz_to_pdf(questions):
    """Export quiz questions to PDF with proper formatting."""
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"quiz_{timestamp}.pdf")
    
    # Create PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#1E88E5')
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        textColor=colors.HexColor('#424242')
    )
    
    question_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=12,
        leading=18,
        textColor=colors.HexColor('#000000')
    )
    
    option_style = ParagraphStyle(
        'OptionStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=8,
        leading=16,
        leftIndent=20,
        textColor=colors.HexColor('#424242')
    )
    
    answer_style = ParagraphStyle(
        'AnswerStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=20,
        leading=16,
        leftIndent=20,
        textColor=colors.HexColor('#2E7D32')
    )
    
    # Build document content
    content = []
    
    # Add logo if exists
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        try:
            img = Image(logo_path, width=2*inch, height=2*inch)
            content.append(img)
            content.append(Spacer(1, 20))
        except Exception as e:
            print(f"Warning: Could not add logo: {str(e)}")
    
    # Add title
    content.append(Paragraph("StudySage Quiz", title_style))
    content.append(Spacer(1, 20))
    
    # Add timestamp
    timestamp_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    content.append(Paragraph(timestamp_text, subtitle_style))
    content.append(Spacer(1, 30))
    
    # Add questions
    for i, q in enumerate(questions, 1):
        # Add question
        content.append(Paragraph(f"Question {i}:", subtitle_style))
        content.append(Paragraph(q["question"], question_style))
        content.append(Spacer(1, 10))
        
        # Add options
        for j, option in enumerate(q["options"], 1):
            content.append(Paragraph(f"{j}. {option}", option_style))
        
        # Add answer
        content.append(Spacer(1, 10))
        content.append(Paragraph(f"Correct Answer: {q['answer']}", answer_style))
        content.append(Spacer(1, 20))
    
    # Build PDF
    doc.build(content)
    print(f"📄 PDF exported to: {output_file}")
    return output_file
=======
from fpdf import FPDF

def export_summary_to_pdf(summary_text, output_path="summary_output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    # Add Unicode font (make sure the font file is in the folder or system)
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(0, 10, summary_text)
    pdf.output(output_path)
    print(f"📄 PDF exported to: {output_path}")
