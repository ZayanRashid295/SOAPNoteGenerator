from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import textwrap

# Function to wrap text and fit it into the page
def wrap_text(text, max_width=80):
    """Wraps text to fit within the specified width."""
    return textwrap.fill(text, width=max_width)

# Basic PDF generation with multi-page support
def generate_pdf(content, filename):
    """Generates a PDF with multi-page support."""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)

    # Margins and line height
    x_margin = 40
    y_margin = 40
    line_height = 14
    y_position = height - y_margin

    # Split content into lines
    lines = content.split("\n")
    for line in lines:
        wrapped_lines = textwrap.wrap(line, width=95)  # Wrap text to fit the page width
        for wrapped_line in wrapped_lines:
            if y_position < y_margin:  # Start a new page if the current page is full
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = height - y_margin
            c.drawString(x_margin, y_position, wrapped_line)
            y_position -= line_height

    c.save()

# Generate the final SOAP note PDF
def generate_final_soap_note_pdf(soap_note, conversation_idx):
    """Generates a PDF for the final SOAP note."""
    content = f"Final SOAP Note:\n\n{soap_note}"
    filename = f"output/final_soap_note_{conversation_idx}.pdf"
    generate_pdf(content, filename)

# Generate analysis report PDF
def generate_analysis_report_pdf(analysis_report, conversation_idx):
    """Generates a PDF for the analysis report."""
    content = "Analysis Report:\n\n"
    # Loop over the explanation and API results
    for key, value in analysis_report.items():
        if isinstance(value, dict):  # Handle nested dictionaries (e.g., scores)
            content += f"{key.capitalize()}:\n"
            for sub_key, sub_value in value.items():
                content += f"  {sub_key.capitalize()}: {sub_value}\n"
        else:
            content += f"{key.capitalize()}:\n{value}\n\n"
    
    filename = f"output/analysis_report_{conversation_idx}.pdf"
    generate_pdf(content, filename)

# Using SimpleDocTemplate for a more advanced approach
def generate_analysis_report_pdf_advanced(analysis_report, conversation_idx):
    """Generates an advanced PDF for the analysis report."""
    filename = f"output/analysis_report_{conversation_idx}_advanced.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    
    # Title section
    title = Paragraph(f"Analysis Report for Conversation {conversation_idx}", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Loop over each API's explanation
    for key, value in analysis_report.items():
        if isinstance(value, dict):  # Handle nested dictionaries (e.g., scores)
            elements.append(Paragraph(f"<b>{key.capitalize()}:</b>", styles['Heading2']))
            for sub_key, sub_value in value.items():
                elements.append(Paragraph(f"{sub_key.capitalize()}: {sub_value}", styles['Normal']))
        else:
            elements.append(Paragraph(f"<b>{key.capitalize()}:</b>", styles['Heading2']))
            elements.append(Paragraph(value, styles['Normal']))
        elements.append(Spacer(1, 12))
    
    # Build the PDF
    doc.build(elements)
