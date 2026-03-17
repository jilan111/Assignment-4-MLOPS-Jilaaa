#!/usr/bin/env python3
import subprocess
import os

os.chdir("/Users/jilan/Documents/Assignmnet 3 MLOps")

# Check if reportlab is installed
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
except ImportError:
    print("Installing reportlab...")
    subprocess.run(["/Library/Developer/CommandLineTools/usr/bin/python3", "-m", "pip", "install", "reportlab", "-q"], check=False)
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak

# Create PDF
pdf_file = "GitHub_Actions_Bug_Report.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add title
title_style = ParagraphStyle('Custom', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#1f6feb'))
story.append(Paragraph("GitHub Actions Pipeline - Bug Report and Fixes", title_style))
story.append(Spacer(1, 0.2*inch))

# Add metadata
metadata_style = ParagraphStyle('Metadata', parent=styles['Normal'], fontSize=11)
story.append(Paragraph("<b>Date:</b> March 17, 2026", metadata_style))
story.append(Paragraph("<b>Assignment:</b> ML Model CI Pipeline", metadata_style))
story.append(Paragraph("<b>Status:</b> All Bugs Fixed and Documented", metadata_style))
story.append(Spacer(1, 0.3*inch))

# Add summary
heading_style = styles['Heading2']
story.append(Paragraph("Executive Summary", heading_style))
summary = "This report documents all 6 bugs found in the GitHub Actions workflow and their fixes."
story.append(Paragraph(summary, styles['Normal']))
story.append(Spacer(1, 0.2*inch))

# Add bugs
story.append(Paragraph("Bugs Identified and Fixed", heading_style))
bugs = [
    ("Bug #1: Missing Repository Checkout Step", "CRITICAL", "Added missing actions/checkout@v4"),
    ("Bug #2: Improper YAML Indentation", "HIGH", "Fixed indentation in 'on:' block"),
    ("Bug #3: Incomplete Linter Check", "HIGH", "Added missing 'run:' command"),
    ("Bug #4: Incorrect Branch Trigger Logic", "MEDIUM", "Changed to run on all branches except main"),
    ("Bug #5: Missing Artifact Upload", "MEDIUM", "Added artifact upload step"),
    ("Bug #6: Inconsistent Step Indentation", "MEDIUM", "Fixed indentation throughout"),
]

for title, severity, fix in bugs:
    story.append(Paragraph(f"<b>{title}</b> [{severity}]", styles['Heading3']))
    story.append(Paragraph(f"Fix: {fix}", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

story.append(PageBreak())

# Add summary table
story.append(Paragraph("Summary of Changes", heading_style))
story.append(Spacer(1, 0.1*inch))

table_data = [
    ["Bug #", "Issue", "Type", "Status"],
    ["1", "Missing checkout", "Addition", "Fixed"],
    ["2", "YAML indentation", "Syntax", "Fixed"],
    ["3", "Incomplete linter", "Addition", "Fixed"],
    ["4", "Wrong trigger logic", "Logic", "Fixed"],
    ["5", "Missing upload", "Addition", "Fixed"],
    ["6", "Inconsistent indent", "Syntax", "Fixed"],
]

table = Table(table_data, colWidths=[0.8*inch, 2*inch, 1.5*inch, 1*inch])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f6f8fa')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0d7de')),
]))
story.append(table)
story.append(Spacer(1, 0.2*inch))

# Add features
story.append(Paragraph("Corrected Workflow Features", heading_style))
features = ["Automated repository checkout", "Python 3.10 setup", "Dependency installation", 
            "Linter checks", "Environment validation", "Artifact upload", 
            "Smart branch triggering", "Pull request support"]
for f in features:
    story.append(Paragraph(f"✅ {f}", styles['Normal']))

# Build
doc.build(story)
print("✅ PDF created: GitHub_Actions_Bug_Report.pdf")
