#!/usr/bin/env python3
"""
Sylki -- Kehon aliarvostetuin neste
Whitepaper PDF Generator
Zokura Foundation 2026
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.tableofcontents import TableOfContents

# Register font
pdfmetrics.registerFont(TTFont('ArialUni', '/Library/Fonts/Arial Unicode.ttf'))

# Colors
DARK_BLUE = HexColor('#1a1a2e')
MEDIUM_BLUE = HexColor('#16213e')
ACCENT_BLUE = HexColor('#0f3460')
ACCENT_GOLD = HexColor('#c4a35a')
LIGHT_GRAY = HexColor('#f5f5f5')
MEDIUM_GRAY = HexColor('#666666')
TABLE_HEADER = HexColor('#1a1a2e')
TABLE_ALT = HexColor('#f0f0f5')
BORDER_COLOR = HexColor('#cccccc')

# Page dimensions
PAGE_W, PAGE_H = A4
MARGIN_LEFT = 25 * mm
MARGIN_RIGHT = 25 * mm
MARGIN_TOP = 25 * mm
MARGIN_BOTTOM = 30 * mm

page_number = [0]

def header_footer(canvas, doc):
    """Draw header line and footer on every page."""
    page_number[0] += 1
    pn = page_number[0]
    canvas.saveState()

    # Header line
    canvas.setStrokeColor(ACCENT_GOLD)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_LEFT, PAGE_H - MARGIN_TOP + 5*mm, PAGE_W - MARGIN_RIGHT, PAGE_H - MARGIN_TOP + 5*mm)

    # Footer
    canvas.setFont('ArialUni', 8)
    canvas.setFillColor(MEDIUM_GRAY)
    canvas.drawString(MARGIN_LEFT, 15 * mm, "Zokura Foundation 2026")
    canvas.drawRightString(PAGE_W - MARGIN_RIGHT, 15 * mm, f"{pn}")

    # Footer line
    canvas.setStrokeColor(BORDER_COLOR)
    canvas.setLineWidth(0.3)
    canvas.line(MARGIN_LEFT, 20 * mm, PAGE_W - MARGIN_RIGHT, 20 * mm)

    canvas.restoreState()

def first_page(canvas, doc):
    """Title page."""
    canvas.saveState()

    # Background gradient effect - dark top section
    canvas.setFillColor(DARK_BLUE)
    canvas.rect(0, PAGE_H * 0.45, PAGE_W, PAGE_H * 0.55, fill=1, stroke=0)

    # Gold accent line
    canvas.setStrokeColor(ACCENT_GOLD)
    canvas.setLineWidth(2)
    canvas.line(PAGE_W * 0.3, PAGE_H * 0.52, PAGE_W * 0.7, PAGE_H * 0.52)

    # Title
    canvas.setFont('ArialUni', 36)
    canvas.setFillColor(white)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H * 0.72, "SYLKI")

    # Subtitle
    canvas.setFont('ArialUni', 14)
    canvas.setFillColor(ACCENT_GOLD)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H * 0.66, "Kehon aliarvostetuin neste")

    # Thin separator
    canvas.setStrokeColor(HexColor('#ffffff40'))
    canvas.setLineWidth(0.5)
    canvas.line(PAGE_W * 0.35, PAGE_H * 0.63, PAGE_W * 0.65, PAGE_H * 0.63)

    # Authors
    canvas.setFont('ArialUni', 11)
    canvas.setFillColor(HexColor('#cccccc'))
    canvas.drawCentredString(PAGE_W / 2, PAGE_H * 0.58, u"Kod\u014d Zokura  &  Miika Riikonen")

    # Date
    canvas.setFont('ArialUni', 10)
    canvas.setFillColor(HexColor('#999999'))
    canvas.drawCentredString(PAGE_W / 2, PAGE_H * 0.545, "21. maaliskuuta 2026")

    # Bottom section - abstract area
    canvas.setFillColor(HexColor('#fafafa'))
    canvas.rect(0, 0, PAGE_W, PAGE_H * 0.45, fill=1, stroke=0)

    # Abstract title
    canvas.setFont('ArialUni', 11)
    canvas.setFillColor(DARK_BLUE)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H * 0.40, "TIIVISTELM\u00c4")

    # Abstract gold underline
    canvas.setStrokeColor(ACCENT_GOLD)
    canvas.setLineWidth(1)
    canvas.line(PAGE_W * 0.42, PAGE_H * 0.393, PAGE_W * 0.58, PAGE_H * 0.393)

    # Abstract text
    abstract_lines = [
        "Sylki on yksi ihmiskehon monimutkaisimmista ja aliarvostetuimmista nesteist\u00e4.",
        "Se ei ole pelkk\u00e4\u00e4 vett\u00e4, vaan dynaaminen bioneste, joka sis\u00e4lt\u00e4\u00e4 tuhansia",
        "proteiineja, entsyymej\u00e4, immunoglobuliineja ja mineraaleja. Sylki suojaa",
        "hampaita, aloittaa ruoansulatuksen, torjuu patogeenej\u00e4, nopeuttaa haavojen",
        "paranemista ja toimii koko kehon terveydentilan peilikuvana.",
        "",
        "T\u00e4ss\u00e4 tutkimuskatsauksessa tarkastellaan syljen koostumusta, tuotantoa,",
        "suojamekanismeja ja uusimpia diagnostisia sovelluksia."
    ]
    canvas.setFont('ArialUni', 9)
    canvas.setFillColor(MEDIUM_GRAY)
    y = PAGE_H * 0.37
    for line in abstract_lines:
        canvas.drawCentredString(PAGE_W / 2, y, line)
        y -= 14

    # Foundation credit
    canvas.setFont('ArialUni', 8)
    canvas.setFillColor(BORDER_COLOR)
    canvas.drawCentredString(PAGE_W / 2, 20 * mm, "Zokura Foundation 2026")

    canvas.restoreState()

def build_styles():
    """Create paragraph styles."""
    styles = {}

    styles['h1'] = ParagraphStyle(
        'Heading1',
        fontName='ArialUni',
        fontSize=18,
        leading=24,
        textColor=DARK_BLUE,
        spaceBefore=20,
        spaceAfter=10,
        keepWithNext=True,
    )

    styles['h2'] = ParagraphStyle(
        'Heading2',
        fontName='ArialUni',
        fontSize=13,
        leading=18,
        textColor=ACCENT_BLUE,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True,
    )

    styles['h3'] = ParagraphStyle(
        'Heading3',
        fontName='ArialUni',
        fontSize=11,
        leading=15,
        textColor=DARK_BLUE,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )

    styles['body'] = ParagraphStyle(
        'BodyText',
        fontName='ArialUni',
        fontSize=9.5,
        leading=14,
        textColor=black,
        spaceBefore=3,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
    )

    styles['bullet'] = ParagraphStyle(
        'Bullet',
        fontName='ArialUni',
        fontSize=9.5,
        leading=13,
        textColor=black,
        spaceBefore=2,
        spaceAfter=2,
        leftIndent=15,
        bulletIndent=5,
        alignment=TA_LEFT,
    )

    styles['sub_bullet'] = ParagraphStyle(
        'SubBullet',
        fontName='ArialUni',
        fontSize=9,
        leading=12,
        textColor=MEDIUM_GRAY,
        spaceBefore=1,
        spaceAfter=1,
        leftIndent=30,
        bulletIndent=20,
        alignment=TA_LEFT,
    )

    styles['caption'] = ParagraphStyle(
        'Caption',
        fontName='ArialUni',
        fontSize=8,
        leading=11,
        textColor=MEDIUM_GRAY,
        spaceBefore=4,
        spaceAfter=8,
        alignment=TA_CENTER,
    )

    styles['ref'] = ParagraphStyle(
        'Reference',
        fontName='ArialUni',
        fontSize=7.5,
        leading=10,
        textColor=MEDIUM_GRAY,
        spaceBefore=1,
        spaceAfter=1,
        leftIndent=15,
        firstLineIndent=-15,
    )

    return styles

def make_table(headers, data, col_widths=None):
    """Create a styled table."""
    table_data = [headers] + data
    if col_widths is None:
        available = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT
        col_widths = [available / len(headers)] * len(headers)

    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('FONTNAME', (0, 0), (-1, -1), 'ArialUni'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('LEADING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('TEXTCOLOR', (0, 1), (-1, -1), black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.3, BORDER_COLOR),
    ]
    # Alternate row colors
    for i in range(1, len(table_data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), TABLE_ALT))

    t.setStyle(TableStyle(style_cmds))
    return t

def section_divider():
    return HRFlowable(width="100%", thickness=0.5, color=ACCENT_GOLD, spaceBefore=6, spaceAfter=6)

def build_document():
    """Build the full PDF."""
    output_path = '/Users/miikariikonen/Desktop/YOMI/shared/research/sylki_tutkimus.pdf'

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title='Sylki \u2014 Kehon aliarvostetuin neste',
        author='Kod\u014d Zokura & Miika Riikonen',
    )

    s = build_styles()
    story = []

    # Title page placeholder (handled by first_page callback)
    story.append(PageBreak())

    # ===== TABLE OF CONTENTS =====
    story.append(Paragraph("SIS\u00c4LLYSLUETTELO", s['h1']))
    story.append(Spacer(1, 5*mm))

    toc_items = [
        ("1.", "Koostumus"),
        ("2.", "Tuotanto"),
        ("3.", "Remineralisaatio"),
        ("4.", "pH-puskurointi"),
        ("5.", "Antimikrobiaalinen puolustus"),
        ("6.", "Ruoansulatus"),
        ("7.", "Haavan paraneminen"),
        ("8.", "Kserostomia (kuiva suu)"),
        ("9.", "Sylki ja systeeminen terveys"),
        ("10.", "Syljenerityksen vuorokausirytmi"),
        ("11.", u"K\u00e4yt\u00e4nn\u00f6n sovellukset"),
        ("12.", "Uusin tutkimus"),
        ("", u"L\u00e4hteet"),
    ]
    for num, title in toc_items:
        story.append(Paragraph(f"<b>{num}</b>  {title}", s['body']))

    story.append(PageBreak())

    # ===== 1. KOOSTUMUS =====
    story.append(Paragraph("1. Koostumus", s['h1']))
    story.append(section_divider())

    story.append(Paragraph("1.1 Vesi ja peruskoostumus", s['h2']))
    story.append(Paragraph(
        "Sylki on 99 % vett\u00e4 ja 1 % orgaanisia ja ep\u00e4orgaanisia aineita. "
        "T\u00e4m\u00e4 pieni osuus on kuitenkin funktionaalisesti \u00e4\u00e4rimm\u00e4isen merkitt\u00e4v\u00e4: "
        "se sis\u00e4lt\u00e4\u00e4 l\u00e4hes 2\u2009000 proteiinia, kymmeni\u00e4 entsyymej\u00e4, immunoglobuliineja, "
        "elektrolyyttej\u00e4 ja muita bioaktiivisia molekyylej\u00e4.", s['body']))

    story.append(Paragraph("1.2 Elektrolyytit", s['h2']))
    story.append(Paragraph(
        "Syljen ep\u00e4orgaaniset komponentit ovat kriittisi\u00e4 sek\u00e4 pH-puskuroinnille "
        "ett\u00e4 hampaiden remineralisaatiolle.", s['body']))

    available_w = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT
    electrolyte_table = make_table(
        ["Elektrolyytti", "Pitoisuus (mmol/l)", u"Teht\u00e4v\u00e4"],
        [
            ["Kalium (K\u207a)", "20\u201325", "Solujen toiminta"],
            ["Natrium (Na\u207a)", "2\u201330", "Osmoottinen tasapaino"],
            ["Kloridi (Cl\u207b)", "15\u201320", "Amylaasin aktivointi"],
            [u"Bikarbonaatti (HCO\u2083\u207b)", "4\u201325", "pH-puskurointi"],
            [u"Kalsium (Ca\u00b2\u207a)", "1\u20132", "Remineralisaatio"],
            [u"Fosfaatti (PO\u2084)", "3\u20135", "Remineralisaatio, puskurointi"],
            [u"Magnesium (Mg\u00b2\u207a)", "0,1\u20130,5", "Entsyymien kofaktori"],
        ],
        col_widths=[available_w * 0.30, available_w * 0.30, available_w * 0.40]
    )
    story.append(electrolyte_table)
    story.append(Paragraph("Taulukko 1. Syljen p\u00e4\u00e4asialliset elektrolyytit ja niiden teht\u00e4v\u00e4t.", s['caption']))

    story.append(Paragraph("1.3 Proteiinit", s['h2']))
    story.append(Paragraph(
        "Syljen proteomi k\u00e4sitt\u00e4\u00e4 l\u00e4hes 2\u2009000 proteiinia, joista noin 600 on "
        "havaittu my\u00f6s veriplasmassa. T\u00e4rkeimm\u00e4t ryhm\u00e4t:", s['body']))

    proteins = [
        (u"<b>Musiinit (MUC5B, MUC7):</b>", "Glykoproteiineja, jotka muodostavat syljen viskoosin limakerroksen. Suojaavat limakalvoja mekaaniselta vauriolta ja kuivumiselta."),
        (u"<b>Immunoglobuliinit:</b>", u"SIgA (90\u201398 % syljen vasta-aineista), IgG (1\u201310 %), pieni\u00e4 m\u00e4\u00e4ri\u00e4 IgM:aa ja IgE:t\u00e4."),
        ("<b>Lysotsyymi:</b>", u"Hajottaa bakteerien solusein\u00e4n peptidoglykaania."),
        ("<b>Laktoferriini:</b>", u"Sitoo rautaa, est\u00e4\u00e4 bakteerien kasvua ja biofilmin muodostumista."),
        ("<b>Histatiinit (Hst1\u20135):</b>", u"Antimikrobiaalisia peptidej\u00e4, erityisesti sienilajeja vastaan. Kriittinen rooli haavan paranemisessa."),
        (u"<b>Defensiinit (\u03b1 ja \u03b2):</b>", u"Kationisia peptidej\u00e4, jotka muodostavat huokosia mikrobien solukalvoihin."),
        ("<b>Statheriini ja PRP:</b>", u"Est\u00e4v\u00e4t kalsiumfosfaatin spontaania saostumista, osallistuvat pellikkelin muodostumiseen."),
    ]
    for title, desc in proteins:
        story.append(Paragraph(f"\u2022 {title} {desc}", s['bullet']))

    story.append(Paragraph(u"1.4 Entsyymit", s['h2']))
    enzymes = [
        (u"<b>Alfa-amylaasi (ptyaliini):</b>", u"Pilkkoo t\u00e4rkkelyksen maltoosiksi ja maltotrioosiksi. AMY1-geenin koodaama."),
        ("<b>Linguaalinen lipaasi:</b>", u"Aloittaa rasvojen pilkkomisen suussa, toimii pH 4,5\u20135,4."),
        (u"<b>Laktoperoksidaasi:</b>", u"Tuottaa hypotiosyanaattia, joka est\u00e4\u00e4 bakteerien aineenvaihduntaa."),
        (u"<b>Hiilihappoanhydraasi (CA):</b>", u"Katalysoi bikarbonaattipuskurij\u00e4rjestelm\u00e4\u00e4, nopeuttaa happojen neutralointia."),
    ]
    for title, desc in enzymes:
        story.append(Paragraph(f"\u2022 {title} {desc}", s['bullet']))

    story.append(PageBreak())

    # ===== 2. TUOTANTO =====
    story.append(Paragraph("2. Tuotanto", s['h1']))
    story.append(section_divider())

    story.append(Paragraph("2.1 Sylkirauhaset", s['h2']))
    story.append(Paragraph(
        u"Ihmisell\u00e4 on kolme paria suuria sylkirauhasia ja satoja pieni\u00e4 sylkirauhasia "
        u"suuontelon limakalvoilla.", s['body']))

    story.append(Paragraph("Korvasylkirauhanen (glandula parotis)", s['h3']))
    story.append(Paragraph(
        u"Suurin sylkirauhanen, sijaitsee korvan edess\u00e4. Tuottaa vesipohjaista, "
        u"entsyymirikasta sylke\u00e4 (seroosi eritys). Levossa noin 25 % ja stimuloituna "
        u"yli 50 % kokonaisvolyymist\u00e4. Hermotus: glossopharyngeus-hermo (CN IX) "
        u"parasympaattisesti ganglion oticumin kautta.", s['body']))

    story.append(Paragraph("Leuanalussylkirauhanen (glandula submandibularis)", s['h3']))
    story.append(Paragraph(
        u"Sekoitettu rauhanen (seroosi + mukoosi). Tuottaa levossa 65\u201370 % kokonais\u00advolyymist\u00e4. "
        u"Hermotus: facialis-hermo (CN VII) ganglion submandibularen kautta.", s['body']))

    story.append(Paragraph("Kielenalussylkirauhanen (glandula sublingualis)", s['h3']))
    story.append(Paragraph(
        u"P\u00e4\u00e4asiassa mukoosi rauhanen, tuottaa paksua musiinirikasta sylke\u00e4. "
        u"Noin 5 % kokonaisvolyymist\u00e4.", s['body']))

    gland_table = make_table(
        ["Rauhanen", "Tyyppi", "Eritys", "Osuus (lepo)"],
        [
            ["Korvasylkirauhanen", "Seroosi", u"Vesipohjainen, entsyymirikasta", "25 %"],
            ["Leuanalussylkirauhanen", "Sekoitettu", u"Sek\u00e4 vesipohjaista ett\u00e4 limapitoista", u"65\u201370 %"],
            ["Kielenalussylkirauhanen", "Mukoosi", "Paksua, musiinirikasta", "5 %"],
        ],
        col_widths=[available_w * 0.28, available_w * 0.17, available_w * 0.35, available_w * 0.20]
    )
    story.append(Spacer(1, 3*mm))
    story.append(gland_table)
    story.append(Paragraph(u"Taulukko 2. Suuret sylkirauhaset ja niiden ominaisuudet.", s['caption']))

    story.append(Paragraph("2.2 Hermostollinen s\u00e4\u00e4tely", s['h2']))
    story.append(Paragraph(
        u"Syljeneritys on hermoston s\u00e4\u00e4telem\u00e4 refleksi. <b>Parasympaattinen hermosto</b> (dominoiva) "
        u"k\u00e4ytt\u00e4\u00e4 asetyylikoliinia v\u00e4litt\u00e4j\u00e4aineena ja tuottaa suuren m\u00e4\u00e4r\u00e4n vesipohjaista, "
        u"entsyymirikasta sylke\u00e4. <b>Sympaattinen hermosto</b> k\u00e4ytt\u00e4\u00e4 noradrenaliinia ja tuottaa "
        u"pienemm\u00e4n m\u00e4\u00e4r\u00e4n proteiinirikasta, paksumpaa sylke\u00e4. T\u00e4st\u00e4 johtuu stressin aiheuttama "
        u"kuivan suun tunne.", s['body']))

    story.append(Paragraph(u"2.3 P\u00e4ivitt\u00e4inen tuotanto", s['h2']))
    prod_items = [
        u"\u2022 <b>Kokonaistuotanto:</b> 0,5\u20131,5 litraa vuorokaudessa",
        u"\u2022 <b>Lepovirtaus:</b> 0,3\u20130,4 ml/min",
        u"\u2022 <b>Stimuloitu virtaus:</b> 4,0\u20135,0 ml/min (pureskelun aikana)",
        u"\u2022 <b>Y\u00f6aika:</b> laskee noin 0,1 ml/min tasolle",
        u"\u2022 Yli 90 % tuotetaan kolmessa suuressa rauhasparissa",
    ]
    for item in prod_items:
        story.append(Paragraph(item, s['bullet']))

    story.append(PageBreak())

    # ===== 3. REMINERALISAATIO =====
    story.append(Paragraph("3. Remineralisaatio", s['h1']))
    story.append(section_divider())

    story.append(Paragraph(
        u"Sylki on ylikyll\u00e4steinen liuos kalsiumin ja fosfaatin suhteen hammasluun "
        u"p\u00e4\u00e4komponenttiin, hydroksiapatiittiin (Ca\u2081\u2080(PO\u2084)\u2086(OH)\u2082) n\u00e4hden. "
        u"Normaalissa pH:ssa (6,5\u20137,4) t\u00e4m\u00e4 ylikyll\u00e4istystila est\u00e4\u00e4 demineralisaation.", s['body']))

    story.append(Paragraph("3.1 Kriittinen pH", s['h2']))
    story.append(Paragraph(
        u"Kun suun pH laskee noin 5,5:een (esim. happohyokk\u00e4ys sy\u00f6misen j\u00e4lkeen), "
        u"sylki ei en\u00e4\u00e4 ole ylikyll\u00e4steinen ja demineralisaatio alkaa. Kun pH palautuu "
        u"neutraaliksi, remineralisaatio k\u00e4ynnistyy uudelleen.", s['body']))

    story.append(Paragraph(u"3.2 Kiteytymisprosessi", s['h2']))
    story.append(Paragraph(
        u"Remineralisaatio tapahtuu vaiheittain metastabiilien kalsiumfosfaattivaiheiden kautta:", s['body']))

    remin_steps = [
        u"\u2022 <b>Amorfinen kalsiumfosfaatti (ACP):</b> ensimm\u00e4inen saostuva vaihe",
        u"\u2022 <b>Dikalsiumfosfaattidihydraatti (DCPD):</b> v\u00e4livaihe",
        u"\u2022 <b>Oktakalsiumfosfaatti (OCP):</b> l\u00e4hemp\u00e4n\u00e4 hydroksiapatiittia",
        u"\u2022 <b>Hydroksiapatiitti:</b> lopullinen kidemuoto, vastaa hampaan emalia",
    ]
    for item in remin_steps:
        story.append(Paragraph(item, s['bullet']))

    story.append(Paragraph(
        u"Vaihtoehtoisessa mekanismissa kalsiumfosfaatti muodostaa nanokokoisia klustereita "
        u"(Posnerin klusterit), jotka kiinnittyv\u00e4t emalin pintaan ja j\u00e4rjest\u00e4ytyv\u00e4t mesokristalleiksi.", s['body']))

    story.append(Paragraph("3.3 Proteiinien rooli", s['h2']))
    story.append(Paragraph(
        u"<b>Statheriini</b> est\u00e4\u00e4 kalsiumfosfaatin spontaania saostumista ja pit\u00e4\u00e4 syljen "
        u"ylikyll\u00e4istystilan vakaana. <b>Kaseiinifosfopeptidit (CPP)</b> stabiloivat amorfista "
        u"kalsiumfosfaattia ja lokalisoivat sen plakkiin. Remineralisoitu pinta on muutaman "
        u"mikrometrin paksuinen mutta mekaanisesti ja kemiallisesti heikompi kuin luonnollinen emali.", s['body']))

    # ===== 4. PH-PUSKUROINTI =====
    story.append(Paragraph("4. pH-puskurointi", s['h1']))
    story.append(section_divider())

    story.append(Paragraph(
        u"Syljess\u00e4 toimii kolme keskeist\u00e4 puskurij\u00e4rjestelm\u00e4\u00e4, jotka yhdess\u00e4 "
        u"yll\u00e4pit\u00e4v\u00e4t suun pH:n turvallisella alueella (6,5\u20137,4).", s['body']))

    story.append(Paragraph(u"4.1 Bikarbonaattij\u00e4rjestelm\u00e4 (primaari)", s['h2']))
    story.append(Paragraph(
        u"T\u00e4rkein puskurij\u00e4rjestelm\u00e4: H\u207a + HCO\u2083\u207b \u2192 H\u2082CO\u2083 \u2192 CO\u2082 + H\u2082O. "
        u"Bikarbonaatti-ionit sitovat ylim\u00e4\u00e4r\u00e4iset vetyionit. Hiilihappoanhydraasi (CA) katalysoi "
        u"reaktiota. Erityisen tehokas pH < 6 alueella. Stimuloidussa syljess\u00e4 bikarbonaatti\u00ad"
        u"pitoisuus nousee: levossa 4,4 mmol/l, stimuloituna 9,7 mmol/l.", s['body']))

    story.append(Paragraph(u"4.2 Fosfaattij\u00e4rjestelm\u00e4 (sekundaari)", s['h2']))
    story.append(Paragraph(
        u"H\u207a + HPO\u2084\u00b2\u207b \u2192 H\u2082PO\u2084\u207b. Dominoi lepotilan syljess\u00e4 ja on kriittinen "
        u"perusfysiologiassa. Pitoisuus noin 3,8\u20134,5 mmol/l.", s['body']))

    story.append(Paragraph("4.3 Proteiinipuskuri", s['h2']))
    story.append(Paragraph(
        u"Vaikuttaa erityisesti hyvin happamissa olosuhteissa (pH 4\u20135). Syljen proteiinit "
        u"(noin 1,9 mg/ml) toimivat amfoteerisina puskureina.", s['body']))

    story.append(Paragraph("4.4 Stephan-k\u00e4yr\u00e4 ja puskurikapasiteetin vahvistaminen", s['h2']))
    story.append(Paragraph(
        u"Sy\u00f6misen j\u00e4lkeen plaakin pH laskee nopeasti noin 5:een (Stephan-k\u00e4yr\u00e4). Puskuri\u00ad"
        u"j\u00e4rjestelm\u00e4t palauttavat pH:n neutraaliksi 20\u201360 minuutissa. Sokerittoman purukumin "
        u"pureskelu stimuloi syljenerityksen 10\u201312-kertaiseksi, mik\u00e4 nostaa bikarbonaatti\u00ad"
        u"pitoisuutta ja puskurikapasiteettia dramaattisesti.", s['body']))

    story.append(PageBreak())

    # ===== 5. ANTIMIKROBIAALINEN PUOLUSTUS =====
    story.append(Paragraph("5. Antimikrobiaalinen puolustus", s['h1']))
    story.append(section_divider())

    story.append(Paragraph(
        u"Sylki muodostaa monikerroksisen antimikrobiaalisen puolustusj\u00e4rjestelm\u00e4n, jossa "
        u"komponentit toimivat usein synergistisesti.", s['body']))

    story.append(Paragraph("5.1 Luontaisen immuniteetin komponentit", s['h2']))

    story.append(Paragraph("<b>Lysotsyymi</b>", s['h3']))
    story.append(Paragraph(
        u"Hajottaa bakteerien solusein\u00e4n peptidoglykaanin \u03b2(1\u20134)-sidoksia, tehden bakteerit "
        u"alttiiksi osmoottiselle lyysille. Toimii synergistisesti laktoferriinin ja SIgA:n kanssa.", s['body']))

    story.append(Paragraph("<b>Laktoferriini</b>", s['h3']))
    lf_items = [
        u"\u2022 <b>Raudan kelatointi:</b> riist\u00e4\u00e4 mikro-organismeilta v\u00e4ltt\u00e4m\u00e4tt\u00f6m\u00e4n kasvutekij\u00e4n",
        u"\u2022 <b>Suora antimikrobiaalinen vaikutus:</b> sitoutuu bakteereihin ja agglutinoi S. mutansia",
        u"\u2022 <b>Biofilmin esto:</b> sitoutuu hydroksiapatiittiin, est\u00e4\u00e4 bakteerien kiinnittymisen",
        u"\u2022 <b>Virulenssitefaktorien hajotus:</b> proteolyyttinen aktiivisuus",
    ]
    for item in lf_items:
        story.append(Paragraph(item, s['bullet']))

    story.append(Paragraph("<b>Histatiinit</b>", s['h3']))
    story.append(Paragraph(
        u"Laaja-alaisesti antibakteerisia, sientenvastaisia ja antiviraalisia. Histatiini 5 on erityisen "
        u"tehokas Candida albicans -sient\u00e4 vastaan. Histatiini 1 kiinnittyy pellikkkeliin ja est\u00e4\u00e4 "
        u"kariogeenisten bakteerien adsorptiota.", s['body']))

    story.append(Paragraph(u"<b>Defensiinit (\u03b1 ja \u03b2)</b>", s['h3']))
    story.append(Paragraph(
        u"Pieni\u00e4 kationisia peptidej\u00e4: positiivinen varaus sitoutuu mikrobien negatiivisesti "
        u"varautuneisiin solukalvoihin ja muodostaa huokosia. \u03b2-defensiinit ovat syljen luontaisen "
        u"immuniteetin p\u00e4\u00e4efektorit. \u03b1-defensiinit inaktivoivat my\u00f6s viruksia (HSV, CMV, influenssa A).", s['body']))

    story.append(Paragraph("5.2 Adaptiivinen immuniteetti", s['h2']))
    story.append(Paragraph(
        u"<b>SIgA</b> on syljen p\u00e4\u00e4immunoglobuliini (90\u201398 % vasta-aineista). Se neutraloi toksiineja, "
        u"agglutinoi bakteereja ja est\u00e4\u00e4 niiden kiinnittymisen limakalvopintoihin. SIgA-eritys noudattaa "
        u"vuorokausirytmi\u00e4 ja huipentuu unen aikana.", s['body']))

    story.append(Paragraph("5.3 Synergistiset vuorovaikutukset", s['h2']))
    story.append(Paragraph(
        u"Monet puolustusproteiinit esiintyv\u00e4t matalina pitoisuuksina, mutta niiden vaikutukset ovat "
        u"kumulatiivisia ja synergistisi\u00e4. Laktoferriini ja lysotsyymi sitoutuvat SIgA:han, joka vahvistaa "
        u"laktoferriinin antimikrobiaalisia ominaisuuksia.", s['body']))

    story.append(PageBreak())

    # ===== 6. RUOANSULATUS =====
    story.append(Paragraph("6. Ruoansulatus", s['h1']))
    story.append(section_divider())

    story.append(Paragraph("6.1 Alfa-amylaasi", s['h2']))
    story.append(Paragraph(
        u"AMY1-geenin koodaama entsyymi pilkkoo t\u00e4rkkelyksen \u03b1-1,4-glykosidisidoksia, mutta ei "
        u"\u03b1-1,6-haarakohtia. Optimaalinen pH: 6,7\u20137,0. Merkitt\u00e4v\u00e4 hydrolyysi tapahtuu sekunneissa "
        u"suuontelossa. AMY1-geenin kopioluku vaihtelee populaatioiden v\u00e4lill\u00e4: paljon t\u00e4rkkelyst\u00e4 "
        u"sy\u00f6neill\u00e4 populaatioilla on korkeampi kopioluku ja tehokkaampi t\u00e4rkkelyksen pilkkominen.", s['body']))

    story.append(Paragraph("6.2 Linguaalinen lipaasi", s['h2']))
    story.append(Paragraph(
        u"Erittyy kielenseroosirauhasista vallihautapapillojen l\u00e4heisyydest\u00e4. Pilkkoo triglyseridit "
        u"diglyserideiksi. pH-optimi 4,5\u20135,4, joten se toimii my\u00f6s mahalaukussa. Ei tarvitse "
        u"sappihappoja. Erityisen t\u00e4rke\u00e4 vastasyntyneille. Erittyy l\u00e4hell\u00e4 rasvan makureseptoreita, "
        u"mik\u00e4 viittaa rasvamaisteen s\u00e4\u00e4telyyn.", s['body']))

    story.append(Paragraph(u"6.3 Makuaistin v\u00e4litt\u00e4minen", s['h2']))
    story.append(Paragraph(
        u"Sylki toimii makuaineiden kuljetusnesteen\u00e4 makusilmuihin. Amylaasin tuottamat malto-"
        u"oligosakkaridit havaitaan makuj\u00e4rjestelm\u00e4n kautta \u2014 t\u00e4rkkelyksen makea maku syntyy "
        u"suussa tapahtuvan pilkkomisen ansiosta. Linguaalinen lipaasi sijaitsee l\u00e4hell\u00e4 "
        u"rasvareseptoreita, mik\u00e4 kytkee rasvan havaitsemisen lipidien pilkkomiseen.", s['body']))

    # ===== 7. HAAVAN PARANEMINEN =====
    story.append(Paragraph("7. Haavan paraneminen", s['h1']))
    story.append(section_divider())

    story.append(Paragraph(
        u"Suuontelon haavat paranevat merkitt\u00e4v\u00e4sti nopeammin kuin ihohaavat. T\u00e4h\u00e4n vaikuttavat "
        u"syljen kostea ymp\u00e4rist\u00f6 ja bioaktiiviset komponentit.", s['body']))

    story.append(Paragraph(u"7.1 Histatiinit \u2014 p\u00e4\u00e4paranemistekij\u00e4t", s['h2']))
    story.append(Paragraph(
        u"Toisin kuin jyrsij\u00f6ill\u00e4, joiden syljess\u00e4 on runsaasti EGF:aa ja NGF:aa, ihmisell\u00e4 n\u00e4iden "
        u"pitoisuudet ovat noin 100\u2009000 kertaa pienemm\u00e4t. Sen sijaan <b>histatiinit</b> (erityisesti "
        u"Hst1 ja Hst2) ovat ihmissyljen t\u00e4rkeimm\u00e4t haavan sulkemista edistavat tekij\u00e4t.", s['body']))

    hist_items = [
        u"\u2022 <b>Histatiini 1:</b> edist\u00e4\u00e4 epiteelisolujen, fibroblastien ja endoteelisolujen migraatiota",
        u"\u2022 Aktivoi ERK1/2-signalointireitin \u2014 edist\u00e4\u00e4 migraatiota, ei proliferaatiota",
        u"\u2022 Syklinen muoto on noin 1\u2009000 kertaa tehokkaampi kuin lineaarinen",
    ]
    for item in hist_items:
        story.append(Paragraph(item, s['bullet']))

    story.append(Paragraph("7.2 Muut tekij\u00e4t", s['h2']))
    story.append(Paragraph(
        u"Sylki yll\u00e4pit\u00e4\u00e4 kosteaa ymp\u00e4rist\u00f6\u00e4, joka parantaa tulehdussolujen toimintaa ja "
        u"edist\u00e4\u00e4 re-epitelialisaatiota. Lis\u00e4ksi syljen eksosomien sis\u00e4lt\u00e4m\u00e4 kudostekija kiihdytt\u00e4\u00e4 "
        u"veren hyytymist\u00e4. Muut kasvutekij\u00e4t (EGF, NGF, TGF-\u03b2, FGF, IGF) osallistuvat kudosten "
        u"yll\u00e4pitoon ja korjautumiseen. Histatiinipohjaiset haavanhoidon l\u00e4\u00e4kkeet ovat aktiivisen "
        u"tutkimuksen kohteena.", s['body']))

    story.append(PageBreak())

    # ===== 8. KSEROSTOMIA =====
    story.append(Paragraph("8. Kserostomia (kuiva suu)", s['h1']))
    story.append(section_divider())

    story.append(Paragraph(
        u"Kserostomia on subjektiivinen suun kuivuuden tunne, josta k\u00e4rsii noin 20 % "
        u"v\u00e4est\u00f6st\u00e4. Riskitekij\u00e4t: naissukupuoli, monil\u00e4\u00e4kitys, yli 71 vuoden ik\u00e4.", s['body']))

    story.append(Paragraph(u"8.1 Syyt", s['h2']))
    story.append(Paragraph("<b>L\u00e4\u00e4kkeet (yleisin syy):</b>", s['h3']))
    story.append(Paragraph(
        u"Satoja l\u00e4\u00e4kkeit\u00e4 aiheuttaa kserostomiaa: masennusl\u00e4\u00e4kkeet (trisykliset), antihistamiinit, "
        u"verenpainl\u00e4\u00e4kkeet, diureetit, ahdistuneisuusl\u00e4\u00e4kkeet, epilepsial\u00e4\u00e4kkeet, opioidit, "
        u"antikolinergiset l\u00e4\u00e4kkeet. Ik\u00e4\u00e4ntyneiden kohonnut riski johtuu todenn\u00e4k\u00f6isesti "
        u"l\u00e4\u00e4kkeiden k\u00e4yt\u00f6st\u00e4, ei ik\u00e4\u00e4ntymisest\u00e4 itsest\u00e4\u00e4n.", s['body']))

    story.append(Paragraph("<b>Muut syyt:</b>", s['h3']))
    other_causes = [
        u"\u2022 Sj\u00f6grenin oireyhtym\u00e4 (yleisin ei-l\u00e4\u00e4keper\u00e4inen syy)",
        u"\u2022 P\u00e4\u00e4n ja kaulan alueen s\u00e4dehoito",
        u"\u2022 Autoimmuunisairaudet (SLE, nivelreuma, kilpirauhasen sairaudet)",
        u"\u2022 Suuhengitys, kuivuminen, huonosti hallittu diabetes",
    ]
    for item in other_causes:
        story.append(Paragraph(item, s['bullet']))

    story.append(Paragraph("8.2 Seuraukset hammasterveydelle", s['h2']))
    consequences = [
        u"\u2022 Hampaiden reikiintymisen merkitt\u00e4v\u00e4 nopeutuminen",
        u"\u2022 Ientulehdus ja parodontiitti",
        u"\u2022 Suun kandidoosi (sieni-infektiot)",
        u"\u2022 Emalin eroosion kiihtyminen ilman pH-puskurointia",
        u"\u2022 Puhe- ja nielemisvaikeudet, makuaistin h\u00e4iri\u00f6t",
        u"\u2022 Ravitsemush\u00e4iri\u00f6t: kun eritys v\u00e4henee puoleen, pureskelu vaikeutuu",
        u"\u2022 Proteesien k\u00e4yt\u00f6n vaikeutuminen, halitoosi",
    ]
    for item in consequences:
        story.append(Paragraph(item, s['bullet']))

    story.append(Paragraph("8.3 Hoito", s['h2']))
    treatments = [
        u"\u2022 Sokeriiton purukumi ja ksylitolipastillit (stimulointi)",
        u"\u2022 L\u00e4\u00e4kkeet: pilokarpiini, sevimeliini",
        u"\u2022 Keinotekoinen sylki, kosteuttimet",
        u"\u2022 L\u00e4\u00e4kevaihto tai annoksen sovittaminen",
        u"\u2022 Huolellinen suuhygienia: fluorituotteet, tihennetyt tarkastukset",
    ]
    for item in treatments:
        story.append(Paragraph(item, s['bullet']))

    # ===== 9. SYLKI JA SYSTEEMINEN TERVEYS =====
    story.append(Paragraph("9. Sylki ja systeeminen terveys", s['h1']))
    story.append(section_divider())

    story.append(Paragraph(
        u"Sylki on noussut lupaavaksi diagnostiseksi v\u00e4lineeksi: ker\u00e4ys on ei-invasiivista, "
        u"s\u00e4ilytys yksinkertaista, ja 20\u201330 % syljen proteomista on p\u00e4\u00e4llekk\u00e4ist\u00e4 "
        u"plasman proteomin kanssa.", s['body']))

    story.append(Paragraph("9.1 Biomarkkerit", s['h2']))
    biomarker_table = make_table(
        ["Sairaus / tila", "Biomarkkeri syljess\u00e4"],
        [
            ["Diabetes", "Glukoosi, adiponektiini"],
            [u"Syd\u00e4n- ja verisuonitaudit", "CRP, MMP-8"],
            [u"Suusy\u00f6p\u00e4", u"IL-8, IL-1\u03b2, p53-vasta-aineet"],
            [u"Rintasy\u00f6p\u00e4", "HER2, CA 15-3"],
            [u"Keuhkosy\u00f6p\u00e4", "SERS-pohjainen proteiiniprofiili"],
            ["Parodontiitti", "MMP-8, IL-6, RANKL"],
            ["Neurologiset sairaudet", u"\u03b1-synukleiini, tau-proteiini"],
            ["Stressi / unirytmi", "Kortisoli, melatoniini"],
        ],
        col_widths=[available_w * 0.40, available_w * 0.60]
    )
    story.append(biomarker_table)
    story.append(Paragraph(u"Taulukko 3. Esimerkkej\u00e4 syljest\u00e4 mitattavista biomarkkereista.", s['caption']))

    story.append(Paragraph(u'9.2 "Nestem\u00e4inen biopsia"', s['h2']))
    story.append(Paragraph(
        u"Salivaomics-ala kattaa syljen genomin, proteomin, transkriptomin ja metabolomin "
        u"analyysin. Syljen eksosomit kuljettavat biomarkkereita kaukaisista kudoksista. "
        u"COVID-19-pandemia kiihdytti merkitt\u00e4v\u00e4sti kehityst\u00e4. Haasteina ovat biomarkkerien "
        u"spesifisyyden varmistaminen, ker\u00e4yksen standardointi ja vuorokausirytmin vaikutus "
        u"mittaustuloksiin.", s['body']))

    story.append(PageBreak())

    # ===== 10. VUOROKAUSIRYTMI =====
    story.append(Paragraph(u"10. Syljenerityksen vuorokausirytmi", s['h1']))
    story.append(section_divider())

    story.append(Paragraph("10.1 Sirkadiaaninen vaihtelu", s['h2']))
    story.append(Paragraph(
        u"Syljeneritys noudattaa selke\u00e4\u00e4 vuorokausirytmi\u00e4: alin taso y\u00f6ll\u00e4 (noin 0,1 ml/min), "
        u"nousu her\u00e4tyksest\u00e4, huippu iltap\u00e4iv\u00e4ll\u00e4, lasku illalla. Suprakiasmaattinen tumake (SCN) "
        u"s\u00e4\u00e4telee rytmi\u00e4 sympaattisen hermoston kautta. Kellogeenit (ARNTL1, PER2, NR1D1) "
        u"ilmentyv\u00e4t sirkadiaanisesti.", s['body']))

    story.append(Paragraph(u"10.2 Suun sis\u00e4isen pH:n vaihtelu", s['h2']))
    story.append(Paragraph(
        u"Suun pH vaihtelee vuorokaudessa: maksimi noin 7,73 ja minimi noin 6,6 "
        u"(12 tunnin intervalli). pH alkaa laskea nukahtaessa ja nousee unen loppuvaiheessa. "
        u"SIgA-pitoisuudet huipentuvat unen aikana, mik\u00e4 kompensoi alentunutta virtausta.", s['body']))

    story.append(Paragraph(u"10.3 Y\u00f6llisen suuhengityksen seuraukset", s['h2']))
    story.append(Paragraph(
        u"Kun syljeneritys on y\u00f6ll\u00e4 minimiss\u00e4\u00e4n, suuhengitys pahentaa tilannetta: ilmavirta "
        u"haihduttaa kosteuden suun kudoksista. Obstruktiivisesta uniapneasta k\u00e4rsivill\u00e4 "
        u"31,4 % her\u00e4\u00e4 kuivaan suuhun (vaikeassa muodossa 40,7 %). Seuraukset: kariesriski, "
        u"ientulehdus, halitoosi ja suun kandidoosi.", s['body']))

    story.append(Paragraph(u"10.4 Sirkadiaaninen h\u00e4iri\u00f6 ja suunterveys", s['h2']))
    story.append(Paragraph(
        u"Vuorokausirytmin h\u00e4iri\u00f6 v\u00e4hent\u00e4\u00e4 melatoniinin erityst\u00e4, mik\u00e4 laskee antioksidantti\u00ad"
        u"tasoja ja lis\u00e4\u00e4 reaktiivisten happiyhdisteita (ROS) tuotantoa syljess\u00e4. Muuttunut "
        u"oksidatiivinen biokemia on yhdistetty kariesriskiin. Sirkadiaanisen kellon "
        u"toimintah\u00e4iri\u00f6 voi johtaa Sj\u00f6grenin oireyhtym\u00e4\u00e4n ja suusy\u00f6p\u00e4\u00e4n.", s['body']))

    # ===== 11. KAYTANNON SOVELLUKSET =====
    story.append(Paragraph(u"11. K\u00e4yt\u00e4nn\u00f6n sovellukset", s['h1']))
    story.append(section_divider())

    story.append(Paragraph(u"11.1 Syljeneriyst\u00e4 edistavat tekij\u00e4t", s['h2']))
    promote = [
        u"\u2022 <b>Pureskelu:</b> stimuloi erityksen 10\u201312-kertaiseksi",
        u"\u2022 <b>Happamat maut:</b> sitruunahappo on voimakas stimulantti",
        u"\u2022 <b>Ksylitoli:</b> stimuloi makeusreseptoreita ilman kariogenik\u00e4 vaikutusta. 4\u20135 kertaa/pv "
        u"5 min aterian j\u00e4lkeen v\u00e4hent\u00e4\u00e4 S. mutans -kantaa merkitt\u00e4v\u00e4sti",
        u"\u2022 <b>Riitt\u00e4v\u00e4 nesteytys:</b> v\u00e4hint\u00e4\u00e4n 8 lasillista vett\u00e4 p\u00e4iv\u00e4ss\u00e4",
        u"\u2022 <b>Nen\u00e4hengitys:</b> erityisen t\u00e4rke\u00e4\u00e4 y\u00f6ll\u00e4",
    ]
    for item in promote:
        story.append(Paragraph(item, s['bullet']))

    story.append(Paragraph(u"11.2 Syljenerityst\u00e4 heikent\u00e4v\u00e4t tekij\u00e4t", s['h2']))
    inhibit = [
        u"\u2022 <b>Alkoholi:</b> kuivattava vaikutus (my\u00f6s alkoholipitoiset suuvedet)",
        u"\u2022 <b>Tupakka:</b> v\u00e4hent\u00e4\u00e4 erityst\u00e4 ja muuttaa koostumusta",
        u"\u2022 <b>Kofeiini:</b> suurina m\u00e4\u00e4rin\u00e4 kuivattava",
        u"\u2022 <b>Stressi:</b> sympaattinen aktivaatio v\u00e4hent\u00e4\u00e4 nestem\u00e4ist\u00e4 erityst\u00e4",
        u"\u2022 <b>L\u00e4\u00e4kkeet:</b> satoja l\u00e4\u00e4kkeit\u00e4 (ks. kserostomia-osio)",
    ]
    for item in inhibit:
        story.append(Paragraph(item, s['bullet']))

    story.append(Paragraph("11.3 Ksylitolin erityisasema", s['h2']))
    story.append(Paragraph(
        u"Ksylitoli on 5-hiilinen sokerialkoholi, jota S. mutans ei pysty metaboloimaan. "
        u"Bakteerit ottavat ksylitolia sis\u00e4\u00e4n mutta eiv\u00e4t saa energiaa \u2014 turha energian\u00ad"
        u"kulutus heikent\u00e4\u00e4 bakteerikantaa. Ajan my\u00f6t\u00e4 S. mutans -populaatio pienenee. "
        u"S\u00e4dehoitopotilailla ksylitoli-, oliivi\u00f6ljy- ja betaiinivalmisteet paransivat "
        u"syljen virtausta 45 %.", s['body']))
    story.append(Paragraph(
        u"<b>Varoitus:</b> Ksylitoli on myrkyllist\u00e4 koirille \u2014 aiheuttaa hypoglykemiaa "
        u"ja mahdollisesti maksavaurion.", s['body']))

    story.append(PageBreak())

    # ===== 12. UUSIN TUTKIMUS =====
    story.append(Paragraph("12. Uusin tutkimus", s['h1']))
    story.append(section_divider())

    story.append(Paragraph("12.1 Keinotekoinen sylki", s['h2']))
    story.append(Paragraph(
        u"Keinotekoisia sylkivalmisteita kehitet\u00e4\u00e4n kserostomiapotilaille. Nykyiset tuotteet "
        u"sis\u00e4lt\u00e4v\u00e4t lysotsyymiä ja laktoferriinia antimikrobiaalisen suojan yll\u00e4pit\u00e4miseksi, "
        u"musiinipohjaisia voiteluaineita ja CPP-ACP-yhdisteit\u00e4 remineralisaation tueksi. "
        u"Mik\u00e4\u00e4n valmiste ei korvaa t\u00e4ydellisesti luonnollista sylke\u00e4.", s['body']))

    story.append(Paragraph("12.2 Sylkidiagnostiikka", s['h2']))
    diag_items = [
        u"\u2022 <b>EFIRM:</b> s\u00e4hk\u00f6keemiallinen alusta, mittaa useita biomarkkereita yhdest\u00e4 sylkipisarasta",
        u"\u2022 <b>SERS + teko\u00e4ly:</b> keuhkosy\u00f6v\u00e4n seulonta syljest\u00e4 (91,2 % herkkyys, AUC 0,95)",
        u"\u2022 <b>Salivaomics:</b> kokonaisvaltainen genomi-, proteomi-, transkriptomi- ja metabolomianalyysi",
        u"\u2022 <b>Eksosomitutkimus:</b> eksosomit kuljettavat biomarkkereita kaukaisista kudoksista",
        u"\u2022 <b>Nanohiukkasmenetelm\u00e4t:</b> RIKEN-tutkijoiden nanopartikkeli-Raman-menetelm\u00e4",
    ]
    for item in diag_items:
        story.append(Paragraph(item, s['bullet']))

    story.append(Paragraph(u"12.3 COVID-19-detektio syljest\u00e4", s['h2']))
    story.append(Paragraph(
        u"EFIRM-teknologia mahdollistaa 4-parametrisen SARS-CoV-2-testin yhdest\u00e4 sylkipisarasta: "
        u"viraalinen RNA, nukleokapsidin antigeeni, sitova ja neutraloiva vasta-aine. "
        u"vRNA-testi: AUC 0,9818, herkkyys 90 %, spesifisyys 100 %. "
        u"Antigenitesti: AUC 1,000. Sylkitestien ei-invasiivisuus teki niist\u00e4 ihanteellisia "
        u"laajamittaiseen v\u00e4est\u00f6seulontaan.", s['body']))

    story.append(Paragraph(u"12.4 Tulevaisuuden n\u00e4kym\u00e4t", s['h2']))
    future = [
        u"\u2022 Syljest\u00e4 tapahtuva sy\u00f6p\u00e4diagnostiikka ja seuranta",
        u"\u2022 Personoitu l\u00e4\u00e4ketiede syljen biomarkkerien perusteella",
        u"\u2022 Pistetestit (point-of-care) kentt\u00e4olosuhteisiin",
        u"\u2022 Histatiinipohjaiset haavanhoidon innovaatiot",
        u"\u2022 Biomiimeettinen remineralisaatio amelogeniinipeptidien avulla",
    ]
    for item in future:
        story.append(Paragraph(item, s['bullet']))

    story.append(PageBreak())

    # ===== LAHTEET =====
    story.append(Paragraph(u"L\u00e4hteet", s['h1']))
    story.append(section_divider())

    refs = [
        u"1. BMC Immunology (2025). Natural and induced immune responses in oral cavity and saliva.",
        u"2. Medicina (2025). Saliva as a Diagnostic Tool for Systemic Diseases \u2014 A Narrative Review.",
        u"3. Int. J. Mol. Sci. (2025). Analyzing the Biochemistry of Saliva: Flow, Total Protein, Amylase Enzymatic Activity.",
        u"4. Dentistry (2024). The Remineralization of Enamel from Saliva: A Chemical Perspective.",
        u"5. Dawes (1972). Circadian rhythms in human salivary flow rate and composition. J. Physiol.",
        u"6. npj Biological Timing and Sleep (2025). Comprehensive integrative analysis of circadian rhythms in human saliva.",
        u"7. Oudhoff et al. (2008). Histatins are the major wound-closure stimulating factors in human saliva. FASEB J.",
        u"8. Torres et al. (2018). Histatins, wound healing, and cell migration. Oral Diseases.",
        u"9. PMC (2021). The Bigger Picture: Why Oral Mucosa Heals Better Than Skin.",
        u"10. StatPearls. Xerostomia. NCBI Bookshelf.",
        u"11. Theranostics (2024). Salivary diagnostics: opportunities and challenges.",
        u"12. JADA (2024). Saliva diagnostics: Salivaomics, saliva exosomics, and saliva liquid biopsy.",
        u"13. Scientific Reports (2024). Direct detection of 4-dimensions of SARS-CoV-2 in saliva.",
        u"14. StatPearls. Physiology, Salivation. NCBI Bookshelf.",
        u"15. Physiol Rev (2021). Salivary gland function, development, and regeneration.",
        u"16. PMC (2019). The power of saliva: Antimicrobial and beyond.",
        u"17. Frontiers in Physiology (2022). Circadian clock \u2014 A promising scientific target in oral science.",
        u"18. Chemistry LibreTexts. Buffer Systems in the Human Oral Environment.",
        u"19. PMC (2000). The buffer capacity and buffer systems of human whole saliva.",
        u"20. PMC (2023). The Relationship between Sleep, Chronotype, and Dental Caries.",
    ]
    for ref in refs:
        story.append(Paragraph(ref, s['ref']))

    # Build
    doc.build(story, onFirstPage=first_page, onLaterPages=header_footer)
    print(f"PDF generated: {output_path}")

if __name__ == '__main__':
    build_document()
