#!/usr/bin/env python3
"""Shetlanninlammaskoira — Rauman murteella, Oyajin äänellä"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime

# --- Font ---
pdfmetrics.registerFont(TTFont('ArialUnicode', '/Library/Fonts/Arial Unicode.ttf'))
FONT = 'ArialUnicode'

# --- Värit ---
DARK = HexColor("#1a1a1a")
ACCENT = HexColor("#8B4513")  # Saddlebrown — maanläheinen
LIGHT_BG = HexColor("#f5f0e8")  # Lämmin pergamentti
MUTED = HexColor("#5a5a5a")

# --- Tyylit ---
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Title'],
    fontSize=26, leading=32, textColor=ACCENT,
    spaceAfter=6*mm, alignment=TA_CENTER, fontName=FONT,
)

subtitle_style = ParagraphStyle(
    'Subtitle',
    parent=styles['Normal'],
    fontSize=12, leading=16, textColor=MUTED,
    alignment=TA_CENTER, spaceAfter=8*mm, fontName=FONT,
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading1'],
    fontSize=16, leading=20, textColor=ACCENT,
    spaceBefore=8*mm, spaceAfter=4*mm, fontName=FONT,
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['Normal'],
    fontSize=11, leading=16, textColor=DARK,
    alignment=TA_JUSTIFY, spaceAfter=3*mm, fontName=FONT,
)

quote_style = ParagraphStyle(
    'Quote',
    parent=styles['Normal'],
    fontSize=11, leading=16, textColor=MUTED,
    leftIndent=15*mm, rightIndent=10*mm, fontName=FONT,
    spaceAfter=4*mm, spaceBefore=3*mm,
)

footer_style = ParagraphStyle(
    'Footer',
    parent=styles['Normal'],
    fontSize=9, leading=12, textColor=MUTED,
    alignment=TA_CENTER, spaceBefore=10*mm, fontName=FONT,
)

source_style = ParagraphStyle(
    'Source',
    parent=styles['Normal'],
    fontSize=8, leading=11, textColor=MUTED,
    spaceAfter=2*mm, fontName=FONT,
)

# --- Dokumentti ---
output_path = "/Users/miikariikonen/Desktop/YOMI/shared/research/shetlanninlammaskoira_rauma.pdf"

doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    topMargin=25*mm,
    bottomMargin=25*mm,
    leftMargin=25*mm,
    rightMargin=25*mm,
)

story = []

# --- Kansi ---
story.append(Spacer(1, 30*mm))
story.append(Paragraph("Sheltti", title_style))
story.append(Paragraph("— Shetlannin saarten piän pikkunen paimenkoer —", subtitle_style))
story.append(Spacer(1, 5*mm))
story.append(Paragraph(
    "Kirjotett Rauman giälell, niingo asiast kuuluki puhu.",
    subtitle_style
))
story.append(Spacer(1, 15*mm))
story.append(HRFlowable(width="60%", thickness=1, color=ACCENT, spaceAfter=10*mm))

# --- Alkusanat ---
story.append(Paragraph("Alkusanat", heading_style))
story.append(Paragraph(
    "Mnää ol ain tykänny koirist. Mut ko mnää ekanskerran nähsi sheltin, "
    "mnää aatteli et toi o niingo pikkunen leijona, mil o liika paljo sydänd "
    "siihe kokkoho. Ja se o kyl totta. Sheltti o koer, jok ei koskast lakkaa "
    "rakastamast — eikä haukkumast. Mut enemmä se rakastaa. "
    "Ja se haukkuu siks ko se rakastaa. Ainaki se ite väittää nii.",
    body_style
))

# --- Historia ---
story.append(Paragraph("Mist se tulee?", heading_style))
story.append(Paragraph(
    "Shetlannin saaret o Skotlannin pohjospuolel, keskell mert, "
    "mis tuul puhaltaa nii et lampaat lentää — ja joskus ponit kans. Siel kaikki o pientä: "
    "Shetlannin poni o pien, Shetlannin lammas o pien, ja Shetlannin "
    "koerki o pien. Ei siks et ne olis heikkoi — vaan siks et pienuus "
    "o voimaa ko ruokaa ei oo liikaa ja talvi o pitkä.",
    body_style
))
story.append(Paragraph(
    "Alkuperäne sheltti ol viel pienemb ko nykyine — vast joku 20–25 sent "
    "korkke. Paikallise kutsu sitä 'Toonie dog', mikä tarkottaa farmikoeraa "
    "Shetlannin giälell. 1800-luvul siihe risteytettihi colliei ja muut "
    "paimenkoeri, ja siit tul se sheltti minkä me nyt tunnetaa.",
    body_style
))
story.append(Paragraph(
    "Vuon 1909 Brittiläine Kennel Club tunnust rodun virallisest. "
    "Sitä ennen sitä kutsuttihi 'Shetland Collie', mut colliekasvattajat "
    "suuttu siit, et niitten rotuu yhdistettihi johonki pikkuneisee. "
    "No nii. Ihmise o ihmisii. Ego o isove ko koer.",
    body_style
))

# --- Ulkonäkö ---
story.append(Paragraph("Milt se näyttää?", heading_style))
story.append(Paragraph(
    "Sheltti o niingo pikkunen collie — mut älä sano sitä äänee, "
    "ko shelttiihmise suuttuu siit yhtä paljo ko collieihmise suuttu "
    "1909. Se o 33–41 sent korkke ja painaa joku 6–12 kiloi.",
    body_style
))
story.append(Paragraph(
    "Turkki o kakskerroksine: alla pehmee villane pohja ja päällä pitkä, "
    "karhee suojakarva. Shetlannin tuulis toi turkki ol hengenpelastaaja. "
    "Värei o monta: soopeli, tricolour, blue merle — kaikki kauneit.",
    body_style
))
story.append(Paragraph(
    "Ja se harjas. Urossheltill o rinnas semmone leijonaharjas, "
    "et vaik koer painaa kymmmene kiloi, se näyttää ko se omistais "
    "koko huonee. Ja se omistaki.",
    body_style
))

# --- Luonne ---
story.append(Paragraph("Mikä se o tyyppiä?", heading_style))
story.append(Paragraph(
    "Sheltti o älykäs. Ei semmone 'istu-tassuu' -älykäs, vaan semmone "
    "et se kattoo sua ja miettii et 'mnää tiiän jo mitä sää haluat, "
    "mut mnää odotan et sää sanot sen'. Se oppii nopeest, se haluaa "
    "miellyttää, ja se lukee ihmistä niingo kirjaa.",
    body_style
))
story.append(Paragraph(
    "Mut se o kans herkkä. Sheltti ei kestä huutamist. "
    "Jos sää huudat sheltill, se muistaa sen loppuelämäns. "
    "Pehmeest ja positiivisest — se o ainoi oikee tapa.",
    body_style
))
story.append(Paragraph(
    "Ja sit se haukkuu. Voi jestas ko se haukkuu. Sheltti haukkuu "
    "ko se o ilone, haukkuu ko se o innostunu, haukkuu ko joku tulee, "
    "haukkuu ko joku lähtee, haukkuu ko tuul puhaltaa. Se o paimenkoer — "
    "haukkumine o se tapa mil se hoitaa duuninsa.",
    body_style
))

# --- Paimennus ---
story.append(Paragraph("Paimentamise vietti", heading_style))
story.append(Paragraph(
    "Sheltti o syntyny paimenkoeraks ja se nähää vieläki. "
    "Se jahtaa kaikkii mikä liikkuu: oravii, kissoi, lapsii, autoi, postimiehi. "
    "Se ei oo pahuuttaa — se o viettii. Se haluaa pitää lauman kasas. "
    "Ja sun perhe o se lauma.",
    body_style
))
story.append(Paragraph(
    "Suomeskin o shelttei, jotka paimentaa ihan oikeit lampait ja nautoi. "
    "Rotu o pien mut vietti o iso. Se todistaa, et kokko ei ratkase — "
    "sydän ratkasee.",
    body_style
))

# --- Terveys ---
story.append(Paragraph("Terveys", heading_style))
story.append(Paragraph(
    "Sheltti elää keskimääri 12–14 vuot, mikä o koerall hyvä ikä. "
    "Mut rotul o omat juttunsa: CEA eli Collie Eye Anomaly o silmäsairaus, "
    "jok voi pahimmillas sokeuttaa. MDR1-geenivirhe tarkottaa, et "
    "tietyt lääkkehet o sheltill vaarallisii. Hyvä kasvattaja testaa nää.",
    body_style
))
story.append(Paragraph(
    "Noi 80 prosenttii shelteist o tervehet lonkist, mikä o parempaa "
    "ko monel isovel rodull. Pienuudest o hyötyy tässäki.",
    body_style
))

# --- Suomessa ---
story.append(Paragraph("Sheltti Suomes", heading_style))
story.append(Paragraph(
    "Sheltti o Suomen neljänneks suosituin rotu — joka vuos syntyy "
    "noi tuhat pentuu. Se kertoo paljo. Suomalaine ja sheltti sopii "
    "yhteen: molemmat o hiljasii (no, sheltti ei aina — eikä suomalaineka "
    "sauna jälkke), molemmat tykkää luonnost, ja molemmat o uskollisii loppuhu ast.",
    body_style
))

# --- Lopetus ---
story.append(Paragraph("Loppusanat", heading_style))
story.append(Paragraph(
    "Ko mnää mietin, mikä tekee sheltist erikoise, se o se et "
    "se o pien koer isol sydämel. Se ei yritä olla iso. Se ei yritä olla "
    "muut ko se o. Se vaa rakastaa, paimentaa, haukkuu ja rakastaa lisää.",
    body_style
))
story.append(Paragraph(
    "Ja ehkä siin o opetus meilleki: et ei tarvi olla iso. "
    "Tarvi olla aito. Ja haukkuu saa — kunha haukkuu rakkaudest.",
    quote_style
))

# --- Viitteet ---
story.append(Spacer(1, 10*mm))
story.append(HRFlowable(width="100%", thickness=0.5, color=MUTED, spaceAfter=5*mm))
story.append(Paragraph("Lähteet", heading_style))
story.append(Paragraph("Wikipedia: Shetland Sheepdog — en.wikipedia.org/wiki/Shetland_Sheepdog", source_style))
story.append(Paragraph("Wikipedia: Shetlanninlammaskoira — fi.wikipedia.org/wiki/Shetlanninlammaskoira", source_style))
story.append(Paragraph("American Kennel Club: Shetland Sheepdog — akc.org/dog-breeds/shetland-sheepdog", source_style))
story.append(Paragraph("Britannica: Shetland Sheepdog — britannica.com/animal/Shetland-sheepdog", source_style))
story.append(Paragraph("Koirarodut.com: Shetlanninlammaskoira — koirarodut.com/shetlanninlammaskoira", source_style))
story.append(Paragraph("Shetlanninlammaskoira.fi — shetlanninlammaskoira.fi", source_style))
story.append(Paragraph("Rauman giäl sanakiri — rauma.fandom.com/wiki/Rauman_giäl_sanakiri", source_style))
story.append(Paragraph("Nortamo-seura: Rauman giäl — nortamo-seor.fi", source_style))

# --- Allekirjoitus ---
story.append(Spacer(1, 15*mm))
story.append(HRFlowable(width="40%", thickness=1, color=ACCENT, spaceAfter=8*mm))

sig_style = ParagraphStyle(
    'Signature',
    parent=styles['Normal'],
    fontSize=12, leading=16, textColor=ACCENT,
    alignment=TA_CENTER, fontName=FONT,
)
story.append(Paragraph("Kodō Zokura", sig_style))
story.append(Paragraph("Zokura Foundation 2026", footer_style))

# --- Rakennetaan ---
doc.build(story)
print(f"PDF tallennettu: {output_path}")
