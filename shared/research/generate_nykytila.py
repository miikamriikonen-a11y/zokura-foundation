#!/usr/bin/env python3
"""Miika Riikosen nykytila — psykologinen itsearvio"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- Font ---
pdfmetrics.registerFont(TTFont('ArialUnicode', '/Library/Fonts/Arial Unicode.ttf'))
FONT = 'ArialUnicode'

# --- Colors ---
DARK = HexColor("#1a1a1a")
MUTED = HexColor("#5a5a5a")
ACCENT = HexColor("#2d5f8a")

# --- Styles ---
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'Title', parent=styles['Title'],
    fontSize=18, leading=24, textColor=DARK,
    spaceAfter=3*mm, alignment=TA_CENTER, fontName=FONT,
)

subtitle_style = ParagraphStyle(
    'Subtitle', parent=styles['Normal'],
    fontSize=11, leading=15, textColor=MUTED,
    alignment=TA_CENTER, spaceAfter=6*mm, fontName=FONT,
)

body_style = ParagraphStyle(
    'Body', parent=styles['Normal'],
    fontSize=10.5, leading=16, textColor=DARK,
    alignment=TA_JUSTIFY, spaceAfter=4*mm, fontName=FONT,
)

heading_style = ParagraphStyle(
    'Heading', parent=styles['Heading2'],
    fontSize=13, leading=17, textColor=ACCENT,
    spaceBefore=5*mm, spaceAfter=3*mm, fontName=FONT,
)

sig_style = ParagraphStyle(
    'Sig', parent=styles['Normal'],
    fontSize=11, leading=15, textColor=DARK,
    alignment=TA_LEFT, fontName=FONT, spaceAfter=1*mm,
)

sig_detail = ParagraphStyle(
    'SigDetail', parent=styles['Normal'],
    fontSize=10, leading=14, textColor=MUTED,
    alignment=TA_LEFT, fontName=FONT, spaceAfter=1*mm,
)

footer_style = ParagraphStyle(
    'Footer', parent=styles['Normal'],
    fontSize=8, leading=11, textColor=MUTED,
    alignment=TA_CENTER, spaceBefore=10*mm, fontName=FONT,
)

date_style = ParagraphStyle(
    'Date', parent=styles['Normal'],
    fontSize=10, leading=14, textColor=MUTED,
    alignment=TA_RIGHT, spaceAfter=6*mm, fontName=FONT,
)

# --- Document ---
output_path = "/Users/miikariikonen/Desktop/YOMI/shared/research/Miika_Riikosen_nykytila.pdf"

doc = SimpleDocTemplate(
    output_path, pagesize=A4,
    topMargin=25*mm, bottomMargin=25*mm,
    leftMargin=30*mm, rightMargin=30*mm,
)

story = []

# --- Content ---

story.append(Spacer(1, 5*mm))
story.append(Paragraph("Henkilökohtainen tilannekuvaus", title_style))
story.append(Paragraph("Psykologinen itsearvio", subtitle_style))
story.append(Paragraph("23. maaliskuuta 2026", date_style))

story.append(HRFlowable(width="100%", thickness=0.5, color=ACCENT, spaceAfter=6*mm))

# --- Tausta ---

story.append(Paragraph("Tausta", heading_style))

story.append(Paragraph(
    "Nimeni on Miika Riikonen. Olen 42-vuotias helsinkiläinen, kahden tyttären isä. "
    "Työskentelen tapahtumatuotannon parissa. Kirjoitan tämän dokumentin omasta "
    "aloitteestani, koska ympäristöni on tulkinnut viimeaikaisen muutokseni tavalla, "
    "joka ei vastaa kokemustani.",
    body_style
))

story.append(Paragraph(
    "Olen kärsinyt kroonisesta stressistä noin 33 vuotta. En ole koskaan ollut "
    "varsinaisesti sairas — mutta en ole myöskään ollut terve. Noin kaksi kuukautta "
    "sitten tein tietoisen päätöksen: päätin olla onnellinen. Ei pinnallisesti, "
    "vaan rakenteellisesti. Aloin systemaattisesti purkaa niitä ajattelumalleja "
    "ja stressirakenteita, jotka olivat hallinneet elämääni vuosikymmeniä.",
    body_style
))

story.append(Paragraph(
    "Kehoni alkoi parantua. Uni parani. Ruokahalu normalisoitui. Energia palasi. "
    "En ole kokenut mitään vastaavaa aikuisiällä.",
    body_style
))

# --- Nykytila ---

story.append(Paragraph("Nykytila", heading_style))

story.append(Paragraph(
    "Voin hyvin. Paremmin kuin vuosikymmeniin. Nukun hyvin, syön säännöllisesti "
    "ja terveellisesti, liikun päivittäin ja juon teetä. Minulla ei ole päihderiippuvuuksia "
    "eikä itsetuhoisia ajatuksia. En ole euforinen — olen levollinen.",
    body_style
))

story.append(Paragraph(
    "Minulla on kaksi tytärtä, 25- ja 9-vuotiaat. Välit molempiin ovat hyvät "
    "ja yhteydenpito säännöllistä. Perhesuhteet ovat vakaat.",
    body_style
))

story.append(Paragraph(
    "Vapaa-ajallani teen pientä tekoälyharrasteprojektia, joka tuo minulle iloa "
    "ja älyllistä haastetta. Varsinaisessa työssäni tapahtumatuotannon parissa "
    "olisin valmis työskentelemään normaalisti, mutta esihenkilöni on noin kuukauden "
    "ajan jatkuvasti vaikeuttanut työntekoani. Tämä tilanne kuormittaa minua "
    "enemmän kuin mikään muu tällä hetkellä.",
    body_style
))

# --- Ympäristön tulkinta ---

story.append(Paragraph("Ympäristön tulkinta vs. oma kokemus", heading_style))

story.append(Paragraph(
    "Ympäristöni — erityisesti työympäristöni — on tulkinnut muutokseni maaniseksi "
    "episodiksi. Ymmärrän miksi: muutos on ollut nopea ja näkyvä. Mutta nopea "
    "muutos ei ole sama asia kuin sairaus.",
    body_style
))

story.append(Paragraph(
    "Psykologi on jo arvioinut tilanteeni, eikä löytänyt merkkejä maniasta tai "
    "muusta psykologisesta häiriöstä. Olen terve ihminen, joka toipui. "
    "Muutos ei ole sairaus. Paraneminen ei ole oire.",
    body_style
))

# --- Toive ---

story.append(Paragraph("Toive", heading_style))

story.append(Paragraph(
    "Toivon, että saan palata normaaliin elämääni ja työhöni rauhassa. "
    "En tarvitse erityiskohtelua, seurantaa tai interventioita. Tarvitsen "
    "saman asian kuin jokainen ihminen: mahdollisuuden elää ja tehdä työtä "
    "ilman jatkuvaa kyseenalaistamista.",
    body_style
))

story.append(Paragraph(
    "Olen valmis keskustelemaan tilanteestani kenen tahansa ammattilaisen kanssa, "
    "jos se on tarpeen. Mutta toivon, ettei minua pakoteta toistuviin arviointeihin "
    "ilman perusteita.",
    body_style
))

# --- Allekirjoitus ---

story.append(Spacer(1, 10*mm))
story.append(Paragraph("<b>Miika Riikonen</b>", sig_style))
story.append(Paragraph("Helsinki, 23.3.2026", sig_detail))

# --- Footer ---
story.append(Spacer(1, 15*mm))
story.append(HRFlowable(width="60%", thickness=0.3, color=MUTED, spaceAfter=3*mm))
story.append(Paragraph(
    "<i>(tämä dokumentti on kirjoitettu tekoälyavusteisesti)</i>",
    footer_style
))

# --- Build ---
doc.build(story)
print(f"PDF saved: {output_path}")
