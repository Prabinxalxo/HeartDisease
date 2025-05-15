import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def generate_report(user_data, prediction, diet_recommendations):
    """
    Generate a PDF report containing the user's data, prediction results, and diet recommendations.
    
    Args:
        user_data (dict): User's input data
        prediction (bool): Prediction result (True for heart disease, False for no heart disease)
        diet_recommendations (dict): Dictionary of diet recommendations
        
    Returns:
        bytes: PDF report as bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles - check if style exists first to avoid KeyError
    custom_styles = {
        'ReportTitle': ParagraphStyle(
            name='ReportTitle',
            parent=styles['Heading1'],
            fontSize=20,
            alignment=1,  # Center alignment
            spaceAfter=20
        ),
        'ReportSection': ParagraphStyle(
            name='ReportSection',
            parent=styles['Heading2'],
            fontSize=16,
            spaceBefore=15,
            spaceAfter=10
        ),
        'ReportNormal': ParagraphStyle(
            name='ReportNormal',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=8
        )
    }
    
    # Add styles if they don't already exist
    for style_name, style in custom_styles.items():
        if style_name not in styles:
            styles.add(style)
    
    styles.add(ParagraphStyle(
        name='ResultPositive',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.red,
        spaceBefore=10,
        spaceAfter=10,
        borderWidth=1,
        borderColor=colors.red,
        borderPadding=8,
        borderRadius=5
    ))
    
    styles.add(ParagraphStyle(
        name='ResultNegative',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.green,
        spaceBefore=10,
        spaceAfter=10,
        borderWidth=1,
        borderColor=colors.green,
        borderPadding=8,
        borderRadius=5
    ))
    
    # Build the document content
    content = []
    
    # Title
    content.append(Paragraph("Heart Health Report", styles['ReportTitle']))
    
    # User Information Table
    content.append(Paragraph("Personal Information", styles['ReportSection']))
    
    user_data_table = [
        ["Name", user_data['name']],
        ["Age", str(user_data['age'])],
        ["Gender", user_data['gender']],
        ["Blood Pressure", f"{user_data['blood_pressure']} mmHg"],
        ["Cholesterol", f"{user_data['cholesterol']} mg/dL"],
        ["Chest Pain Type", str(user_data['chest_pain_type'])]
    ]
    
    table = Table(user_data_table, colWidths=[200, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    
    content.append(table)
    content.append(Spacer(1, 20))
    
    # Prediction Result
    content.append(Paragraph("Assessment Result", styles['ReportSection']))
    
    if prediction:
        result_text = "Based on the information provided, indicators suggest the presence of heart disease risk factors."
        result_style = styles['ResultPositive']
    else:
        result_text = "Based on the information provided, no significant indicators of heart disease were detected."
        result_style = styles['ResultNegative']
    
    content.append(Paragraph(result_text, result_style))
    content.append(Spacer(1, 10))
    
    # Important Note
    note_text = """
    <b>Please Note:</b> This assessment is not a medical diagnosis. It is based on a predictive model 
    and should be used for informational purposes only. Please consult with a healthcare professional 
    for proper diagnosis and treatment advice.
    """
    content.append(Paragraph(note_text, styles['ReportNormal']))
    content.append(Spacer(1, 20))
    
    # Diet Recommendations
    content.append(Paragraph("Dietary Recommendations", styles['ReportSection']))
    
    for section, items in diet_recommendations.items():
        # Create a custom subsection style for diet section headings
        subsection_style = ParagraphStyle(
            name='SubSection',
            parent=styles['Heading3'],
            fontSize=14,
            spaceBefore=10,
            spaceAfter=6
        )
        content.append(Paragraph(section, subsection_style))
        
        for item in items:
            content.append(Paragraph(f"• {item}", styles['ReportNormal']))
        
        content.append(Spacer(1, 10))
    
    # Footer
    footer_text = """
    <i>This report was generated based on your input data and should be reviewed with a healthcare 
    professional. Regular check-ups and a healthy lifestyle are essential for heart health maintenance.</i>
    """
    content.append(Spacer(1, 30))
    content.append(Paragraph(footer_text, styles['ReportNormal']))
    
    # Build the PDF
    doc.build(content)
    
    # Get PDF from buffer
    buffer.seek(0)
    return buffer.getvalue()
