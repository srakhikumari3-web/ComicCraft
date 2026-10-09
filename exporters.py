from datetime import datetime
from pathlib import Path
from fpdf import FPDF, XPos, YPos

from app.config import EXPORTS_DIR, STATIC_DIR
from app.models import ComicPanel


def save_pdf(layout: list[ComicPanel], story_title: str = "ComicCraft Comic") -> str:
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"comiccraft-{datetime.now().strftime('%Y%m%d-%H%M%S')}.pdf"
    output = EXPORTS_DIR / filename

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(0, 12, f"Panel {panel.panel_number}: {panel.title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        image_path = STATIC_DIR / panel.image_path.removeprefix("/static/")
        if image_path.exists():
            pdf.image(str(image_path), x=15, y=30, w=180, h=120)
            pdf.set_y(155)
        else:
            pdf.set_y(35)

        pdf.set_font("Helvetica", "I", 10)
        pdf.multi_cell(180, 6, panel.scene_description)
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(180, 6, f"Caption: {panel.caption}")
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(180, 6, f"Narration: {panel.narration}")
        if panel.dialogue:
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(180, 6, "Dialogue:")
            pdf.set_font("Helvetica", "", 11)
            for line in panel.dialogue:
                pdf.multi_cell(180, 6, f"- {line}")

    pdf.output(str(output))
    return f"/static/exports/{filename}"
