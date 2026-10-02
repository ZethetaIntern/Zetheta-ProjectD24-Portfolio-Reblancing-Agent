# PDF report generation.

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def create_pdf(path, title, lines):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, 800, title)
    y = 770
    c.setFont("Helvetica", 10)
    for line in lines:
        for chunk in str(line).split("\n"):
            c.drawString(40, y, chunk[:115])
            y -= 15
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = 800
    c.save()
    return str(path)
