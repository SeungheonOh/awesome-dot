"""Generate only the fictional labels; uses the local installed ReportLab."""
import json
import argparse
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

root = Path(__file__).resolve().parent.parent
data = json.loads((root / "example-data.json").read_text())
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--font-dir", type=Path, required=True,
                    help="Directory containing DejaVuSans.ttf and DejaVuSans-Bold.ttf")
font_root = parser.parse_args().font_dir
pdfmetrics.registerFont(TTFont("LabelSans", str(font_root / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("LabelBold", str(font_root / "DejaVuSans-Bold.ttf")))
pdf = canvas.Canvas(str(root / "labels.pdf"), pagesize=(612, 792),
                    pageCompression=1, invariant=1)
pdf.setTitle("Fictional box labels - revision 2")
pdf.setAuthor("Fictional workflow example")
pdf.setFont("LabelBold", 17)
pdf.drawString(36, 754, "BOX LABELS / FICTIONAL DRAFT")
pdf.setFont("LabelSans", 10)
pdf.drawString(36, 735, "Revision 2. Review destination rooms before printing.")
pdf.drawString(36, 719, "US Letter. Print at actual size; cut on the dashed outlines.")
for (box_id, room), (x, y) in zip(data["boxes"].items(),
                                 [(36, 424), (316, 424), (36, 134), (316, 134)]):
    pdf.setStrokeColorRGB(0.55, 0.55, 0.55)
    pdf.setDash(4, 4)
    pdf.rect(x, y, 260, 270, stroke=1, fill=0)
    pdf.setDash()
    pdf.setFillColorRGB(0.07, 0.1, 0.15)
    pdf.setFont("LabelBold", 55)
    pdf.drawCentredString(x + 130, y + 152, box_id)
    pdf.setFont("LabelSans", 25)
    pdf.drawCentredString(x + 130, y + 109, room)
pdf.setFillColorRGB(0.3, 0.3, 0.3)
pdf.setFont("LabelSans", 9)
pdf.drawString(36, 94, "Example only. No contents, address or personal names are printed on these labels.")
pdf.drawString(36, 78, "A label does not confirm that a box is packed, received or checked.")
pdf.showPage()
pdf.save()
