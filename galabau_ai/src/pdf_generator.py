from __future__ import annotations
from pathlib import Path
from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'generated'
OUT.mkdir(exist_ok=True)

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 10, 'GaLaBau Pflanzenbuch', new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', '', 8)
        self.cell(0, 10, f'Seite {self.page_no()}', align='C')


def clean(s):
    return (s or '').encode('latin-1', 'replace').decode('latin-1')


def generate_pflanzenbuch(plants: list[dict], username: str) -> Path:
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 7, clean(f'Persoenliches Pflanzenbuch fuer {username}. Eintraege: {len(plants)}'))
    pdf.ln(5)
    for p in plants:
        pdf.add_page()
        title = p.get('deutscher_name') or 'Unbenannte Pflanze'
        bot = p.get('botanischer_name') or 'noch offen'
        pdf.set_font('Helvetica', 'B', 16)
        pdf.multi_cell(0, 9, clean(title))
        pdf.set_font('Helvetica', 'I', 12)
        pdf.multi_cell(0, 7, clean(bot))
        img = p.get('bildpfad')
        if img and Path(img).exists():
            try:
                pdf.image(img, x=15, y=None, w=80)
                pdf.ln(4)
            except Exception:
                pdf.multi_cell(0, 6, '[Bild konnte nicht eingebunden werden]')
        else:
            pdf.set_font('Helvetica', 'B', 10)
            pdf.multi_cell(0, 6, '[Eigenes Bild fehlt noch / Internetbild bitte Quelle dokumentieren]')
        pdf.set_font('Helvetica', '', 11)
        fields = [('Familie','familie'),('Standort','standort'),('Boden','boden'),('Bluetezeit','bluetezeit'),('Verwendung im GaLaBau','verwendung'),('Pflege/Schnitt','pflege'),('Erkennungsmerkmale','merkmale'),('Bildquelle','bildquelle')]
        for label, key in fields:
            pdf.set_font('Helvetica', 'B', 11)
            pdf.cell(42, 7, clean(label + ':'), new_x='RIGHT', new_y='TOP')
            pdf.set_font('Helvetica', '', 11)
            pdf.multi_cell(0, 7, clean(str(p.get(key) or '-')))
    path = OUT / f'pflanzenbuch_{username}.pdf'
    pdf.output(str(path))
    return path
