#!/usr/bin/env python3
"""
Hampaiden luonnollinen valkaisu — Tutkimuskatsaus
PDF Whitepaper Generator
Zokura Foundation 2026
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT

# Register Arial Unicode font
FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
pdfmetrics.registerFont(TTFont("ArialUnicode", FONT_PATH))

OUTPUT = "/Users/[REDACTED]/Desktop/YOMI/shared/research/hampaiden_valkaisu_luonnollisesti.pdf"

# Colors
PRIMARY = HexColor("#1a1a2e")
ACCENT = HexColor("#16213e")
HIGHLIGHT = HexColor("#0f3460")
LIGHT_BG = HexColor("#f0f0f5")
BORDER_COLOR = HexColor("#cccccc")
TABLE_HEADER_BG = HexColor("#1a1a2e")
TABLE_ALT_BG = HexColor("#f5f5fa")
GREEN_CHECK = HexColor("#2d6a4f")
RED_CROSS = HexColor("#c1121f")
AMBER = HexColor("#e76f51")

# Page dimensions
PAGE_W, PAGE_H = A4
MARGIN = 2.2 * cm


def footer_and_header(canvas, doc):
    """Draw header line, footer with page number and foundation name."""
    canvas.saveState()
    # Header line
    canvas.setStrokeColor(HIGHLIGHT)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, PAGE_H - MARGIN + 5*mm, PAGE_W - MARGIN, PAGE_H - MARGIN + 5*mm)
    # Footer
    canvas.setFont("ArialUnicode", 8)
    canvas.setFillColor(HexColor("#666666"))
    canvas.drawString(MARGIN, 1.2*cm, "Zokura Foundation 2026")
    canvas.drawRightString(PAGE_W - MARGIN, 1.2*cm, f"Sivu {doc.page}")
    # Footer line
    canvas.setStrokeColor(BORDER_COLOR)
    canvas.line(MARGIN, 1.6*cm, PAGE_W - MARGIN, 1.6*cm)
    canvas.restoreState()


def build_styles():
    """Create all paragraph styles."""
    styles = {}

    styles["title"] = ParagraphStyle(
        "Title",
        fontName="ArialUnicode",
        fontSize=22,
        leading=28,
        textColor=PRIMARY,
        alignment=TA_CENTER,
        spaceAfter=6*mm,
        spaceBefore=0,
    )
    styles["subtitle"] = ParagraphStyle(
        "Subtitle",
        fontName="ArialUnicode",
        fontSize=11,
        leading=15,
        textColor=HexColor("#555555"),
        alignment=TA_CENTER,
        spaceAfter=3*mm,
    )
    styles["authors"] = ParagraphStyle(
        "Authors",
        fontName="ArialUnicode",
        fontSize=12,
        leading=16,
        textColor=ACCENT,
        alignment=TA_CENTER,
        spaceAfter=2*mm,
    )
    styles["date"] = ParagraphStyle(
        "Date",
        fontName="ArialUnicode",
        fontSize=10,
        leading=14,
        textColor=HexColor("#777777"),
        alignment=TA_CENTER,
        spaceAfter=8*mm,
    )
    styles["h1"] = ParagraphStyle(
        "H1",
        fontName="ArialUnicode",
        fontSize=16,
        leading=22,
        textColor=PRIMARY,
        spaceBefore=10*mm,
        spaceAfter=4*mm,
        borderPadding=(0, 0, 2, 0),
    )
    styles["h2"] = ParagraphStyle(
        "H2",
        fontName="ArialUnicode",
        fontSize=13,
        leading=18,
        textColor=HIGHLIGHT,
        spaceBefore=6*mm,
        spaceAfter=3*mm,
    )
    styles["h3"] = ParagraphStyle(
        "H3",
        fontName="ArialUnicode",
        fontSize=11,
        leading=15,
        textColor=ACCENT,
        spaceBefore=4*mm,
        spaceAfter=2*mm,
    )
    styles["body"] = ParagraphStyle(
        "Body",
        fontName="ArialUnicode",
        fontSize=10,
        leading=15,
        textColor=black,
        alignment=TA_JUSTIFY,
        spaceAfter=3*mm,
    )
    styles["bullet"] = ParagraphStyle(
        "Bullet",
        fontName="ArialUnicode",
        fontSize=10,
        leading=14,
        textColor=black,
        leftIndent=8*mm,
        spaceAfter=1.5*mm,
        bulletIndent=3*mm,
    )
    styles["bold_body"] = ParagraphStyle(
        "BoldBody",
        fontName="ArialUnicode",
        fontSize=10,
        leading=15,
        textColor=black,
        alignment=TA_JUSTIFY,
        spaceAfter=3*mm,
    )
    styles["verdict"] = ParagraphStyle(
        "Verdict",
        fontName="ArialUnicode",
        fontSize=10,
        leading=15,
        textColor=PRIMARY,
        alignment=TA_LEFT,
        spaceAfter=4*mm,
        leftIndent=5*mm,
        borderWidth=1,
        borderColor=HIGHLIGHT,
        borderPadding=8,
        backColor=LIGHT_BG,
    )
    styles["caption"] = ParagraphStyle(
        "Caption",
        fontName="ArialUnicode",
        fontSize=8,
        leading=11,
        textColor=HexColor("#888888"),
        alignment=TA_CENTER,
        spaceAfter=4*mm,
    )
    return styles


def make_table(headers, rows, col_widths=None):
    """Create a styled table."""
    header_style = ParagraphStyle("TH", fontName="ArialUnicode", fontSize=9, leading=12, textColor=white, alignment=TA_CENTER)
    cell_style = ParagraphStyle("TD", fontName="ArialUnicode", fontSize=9, leading=12, textColor=black, alignment=TA_LEFT)

    data = [[Paragraph(h, header_style) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), cell_style) for c in row])

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, -1), "ArialUnicode"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), TABLE_ALT_BG))
    t.setStyle(TableStyle(style_cmds))
    return t


def hr():
    return HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceAfter=3*mm, spaceBefore=3*mm)


def build_pdf():
    s = build_styles()
    story = []
    sp = lambda x: Spacer(1, x*mm)
    P = lambda text, style="body": Paragraph(text, s[style])
    B = lambda text: Paragraph(f"<bullet>&bull;</bullet> {text}", s["bullet"])

    # === TITLE PAGE ===
    story.append(sp(40))
    story.append(P("Hampaiden luonnollinen valkaisu", "title"))
    story.append(P("Tutkimuskatsaus", "subtitle"))
    story.append(sp(8))
    story.append(hr())
    story.append(sp(4))
    story.append(P("Tekijat: Kodo Zokura &amp; [REDACTED]", "authors"))
    story.append(P("21.3.2026", "date"))
    story.append(sp(10))
    story.append(P(
        "Kattava, tieteeseen perustuva katsaus luonnollisiin hampaiden valkaisumenetelmiin. "
        "Kasittelee nayttoon perustuvat menetelmat, myytit ja riskit seka vertaa luonnollisia "
        "menetelmia ammattimaiseen valkaisuun.",
        "body"
    ))
    story.append(sp(6))
    # TOC-like overview
    toc_items = [
        "1. Miksi hampaat kellastuvat",
        "2. Oljynveto (Oil Pulling)",
        "3. Ruokasooda (natriumbikarbonaatti)",
        "4. Aktiivihiili",
        "5. Vetyperoksidi (matala pitoisuus)",
        "6. Ruokavaliolahestymistavat",
        "7. Kurkuma - paradoksi",
        "8. Omenaviinietikka",
        "9. Mika toimii, mika on myytti",
        "10. Kiilteen turvallisuus",
        "11. Ammattimainen vs. luonnollinen",
        "12. Ehkaisy",
    ]
    story.append(P("<b>Sisallys</b>", "h2"))
    for item in toc_items:
        story.append(B(item))
    story.append(PageBreak())

    # === 1. MIKSI HAMPAAT KELLASTUVAT ===
    story.append(P("1. Miksi hampaat kellastuvat", "h1"))
    story.append(hr())

    story.append(P("Hampaan rakenne ja vari", "h2"))
    story.append(P(
        "Hampaan vari syntyy kahden kerroksen vuorovaikutuksesta: <b>kiilteen</b> ja <b>dentiinin</b>. "
        "Kiille on hampaan kova, lapikuultava ulkokerros, jonka luonnollinen savy vaihtelee valkoisesta "
        "kellertavaan. Kiilteen alla on dentiini, joka on luonnostaan kellertava kudos. Kiilteen paksuus "
        "ja lapikuultavuus maarittavat, kuinka paljon dentiinin keltainen vari nakyy lapi."
    ))
    story.append(P(
        "Kiille koostuu kiteisesta kalsiumfosfaatista (hydroksiapatiitti). Se on erittain kova mutta "
        "huokoinen eika sisalla elavia soluja. <b>Kerran kulunut kiille ei uusiudu.</b>"
    ))

    story.append(P("Ulkoiset varimuutokset (ekstrinsic stains)", "h2"))
    story.append(P(
        "Ulkoiset tahrat vaikuttavat kiilteen pintaan. Kromogeenit ovat varillisia kemiallisia yhdisteita "
        "ruoissa ja juomissa, jotka tarttuvat hampaan pintaan joko suoraan tai pellikkelin kautta."
    ))
    story.append(B("Kahvi, tee, punaviini (kromogeenit + tanniinit)"))
    story.append(B("Tupakka (terva + nikotiini)"))
    story.append(B("Huono suuhygienia - tahrat tarttuvat plakkiin"))
    story.append(B("Tummat marjat, soijakastike, balsamiviinietikka"))

    story.append(P("Sisaiset varimuutokset (intrinsic stains)", "h2"))
    story.append(P(
        "Sisaiset tahrat syntyvat hampaan sisalla, dentiinissa. Niihin ei voi vaikuttaa pintaa puhdistamalla."
    ))
    story.append(B("<b>Ikaantyminen:</b> Kiille ohenee ajan myota paljastaen kellertavan dentiinin. Dentiini itsessaankin tummenee ian myota."))
    story.append(B("<b>Tetrasykliini-antibiootit:</b> Lapsuudessa (alle 8 v.) altistuminen aiheuttaa pysyvia sisaisia tahroja."))
    story.append(B("<b>Fluoroosi:</b> Liiallinen fluorin saanti lapsuudessa aiheuttaa valkoisia tai ruskeita laiskia."))
    story.append(B("<b>Hammasvammat:</b> Trauma voi aiheuttaa dentiinin tummumisen."))
    story.append(B("<b>Genetiikka:</b> Kiilteen paksuus ja dentiinin luonnollinen vari ovat osittain perinnollisia."))

    story.append(PageBreak())

    # === 2. ÖLJYNVETO ===
    story.append(P("2. Oljynveto (Oil Pulling)", "h1"))
    story.append(hr())

    story.append(P(
        "Oljynvetoa harjoitetaan purskuttelemalla oljya (yleensa kookos- tai seesamioljy) suussa "
        "15-20 minuuttia. Menetelma on peraisin ayurvedisesta laaketieteesta."
    ))

    story.append(P("Tieteellinen naytto", "h2"))
    story.append(P(
        "<b>Jong ym. (2024):</b> Systemaattinen katsaus ja meta-analyysi International Journal of Dental Hygiene "
        "-lehdessa totesi, etta oljynvedon teho ienterveyteen ja plakinkontrolliin jai kiistanalaiseksi."
    ))
    story.append(P(
        "<b>Peng ym. (2022):</b> Meta-analyysi sisalsi vain 9 tutkimusta (344 tutkittavaa). Nelja tutkimusta "
        "arvioitiin laadultaan heikoiksi."
    ))
    story.append(P(
        "<b>Woolley ym. (2020):</b> Katsaus Heliyon-lehdessa sisalsi vain 4 RCT-tutkimusta (182 osallistujaa) "
        "ja totesi, etta on vaikeaa maarittaa, onko kookosoljyn oljynvedolla todellista hyotya."
    ))
    story.append(P(
        "In vitro -tutkimuksessa todettiin, ettei kookos-, seesami- tai auringonkukkaoljylla ole mitaan "
        "vaikutusta hampaiden valkaisuun. ADA toteaa, ettei vahvaa nayttoa valkaisusta ole."
    ))

    story.append(P(
        "<b>Arvio: Myytti valkaisijana.</b> Oljynveto ei valkaise hampaita. Se voi olla hyodyllinen "
        "lisa suuhygieniarutiiniin, mutta ei korvaa harjausta, lankaamista tai fluorihammastahnaa.",
        "verdict"
    ))

    # === 3. RUOKASOODA ===
    story.append(P("3. Ruokasooda (natriumbikarbonaatti)", "h1"))
    story.append(hr())

    story.append(P(
        "Ruokasooda toimii miedosti hankaavana aineena, joka poistaa pintatahroja. Se myos puskuroi "
        "happoja suussa. JADA-lehden katsaukset osoittavat ruokasoodapohjaisten hammastahnojen olevan "
        "tehokkaita ja turvallisia pintatahrioiden poistossa."
    ))

    story.append(P("Abrasiivisuus (RDA-arvot)", "h2"))
    story.append(make_table(
        ["Tuote", "RDA-arvo"],
        [
            ["Puhdas ruokasooda", "7"],
            ["Tahna 50-65 % ruokasoodaa", "35-53"],
            ["Tahna 35-45 % ruokasoodaa", "57-134"],
            ["Tahna ilman ruokasoodaa", "46-245"],
            ["ISO:n ylempi turvallisuusraja", "250"],
        ],
        col_widths=[90*mm, 50*mm]
    ))
    story.append(P("RDA = Suhteellinen dentiiniabrasiviteetti. ISO 11609 -standardi.", "caption"))

    story.append(P(
        "Ruokasooda on pehmeampaa kuin kiille ja hieman pehmeampaa kuin dentiini. Se on yksi vahiten "
        "abrasiivisista puhdistusaineista. Vuonna 2012 julkaistussa tutkimuksessa ruokasoodatahnalla "
        "tahrapisteet olivat 61 % alhaisemmat kuin verrokkitahnalla kuuden viikon kohdalla."
    ))

    story.append(P("Varoitukset", "h3"))
    story.append(B("Pelkka ruokasooda+vesi -pasta ei sisalla fluoria"))
    story.append(B("ALA KOSKAAN yhdista sitruunamehun tai omenaviinietikan kanssa"))
    story.append(B("Alle 12-vuotiaat eivat saisi kayttaa - kiille viela kehittyy"))

    story.append(P(
        "<b>Arvio: Toimii pintatahriin, turvallinen oikein kaytettyna.</b> Yksi harvoista luonnollisista "
        "menetelmista, joilla on tieteellista nayttoa. EI muuta hampaiden sisaista varia.",
        "verdict"
    ))

    story.append(PageBreak())

    # === 4. AKTIIVIHIILI ===
    story.append(P("4. Aktiivihiili", "h1"))
    story.append(hr())

    story.append(P(
        "Aktiivihiilen vaitetaan imeyyttavan tahroja huokoisen rakenteensa ansiosta. Todellisuudessa "
        "mahdollinen vaikutus perustuu mekaaniseen hankaukseen."
    ))

    story.append(P("Tieteellinen naytto", "h2"))
    story.append(P(
        "Systemaattinen katsaus (2022) totesi, etta aktiivihiilitahnoilla oli heikompi valkaisuvaikutus "
        "kuin perinteisilla vetyperoksidia tai karbamidiperoksidia sisaltavilla valmisteilla, ja ne ovat "
        "vahemman turvallisia korkean abrasiivisuutensa vuoksi."
    ))

    story.append(P("Riskit", "h2"))
    story.append(B("<b>Korkea abrasiivisuus:</b> Merkittavaa kiilteen menetysta ja pinnan karheuden lisaantymista"))
    story.append(B("<b>Kiilteen mikrokovuuden heikkeneminen:</b> Kaikki vauriot ovat pysyvia"))
    story.append(B("<b>Fluori-interferenssi:</b> Aktiivihiili voi inaktivoida fluoria"))
    story.append(B("<b>Fluorin puute:</b> Monet hiilituotteet eivat sisalla fluoria"))
    story.append(B("JADA:n katsaus (2017): Ei riittavaa nayttoa turvallisuudesta tai tehosta"))

    story.append(P(
        "<b>Arvio: Myytti ja riski.</b> Aktiivihiili ei toimi valkaisijana ja voi vahingoittaa kiilletta "
        "pysyvasti. Markkinointi ylittaa selvasti tieteellisen nayton. Kayttoa ei suositella.",
        "verdict"
    ))

    # === 5. VETYPEROKSIDI ===
    story.append(P("5. Vetyperoksidi (matala pitoisuus)", "h1"))
    story.append(hr())

    story.append(P(
        "Vetyperoksidi (H2O2) on luonnossa esiintyva yhdiste, jota muodostuu mm. sylkeen pienia maaria. "
        "Se on ainoa aine, joka voi tunkeutua kiilteen lapi ja hapettaa sisaisia tahramolekyyyleja "
        "- eli todella valkaisee."
    ))

    story.append(P("Turvalliset pitoisuudet", "h2"))
    story.append(B("ADA: turvallinen kasikauppatuotteissa enintaan 3,5 % pitoisuudella"))
    story.append(B("3-6 % pitoisuudet turvallisia valmistajan ohjeiden mukaan"))
    story.append(B("Yli 6 % vaatii hammaslaakarin valvontaa"))
    story.append(B("Jo 1,5 % suuvesi aiheutti havaittavan vaalenemisen 4 viikossa"))

    story.append(P("Sivuvaikutukset", "h2"))
    story.append(B("Hammasherkkyyden lisaantyminen (yleisin, yleensa lieva ja ohimenevainen)"))
    story.append(B("Ienarsytys (lieva, ohimenevainen)"))
    story.append(B("Ei karsinogeenisia vaikutuksia suun limakalvoihin (2022 systemaattinen katsaus)"))

    story.append(P(
        "<b>Arvio: Toimii, tieteellinen naytto vahva.</b> Ainoa luonnollisesti esiintyva aine, joka "
        "todella valkaisee hampaita (myos sisaisia tahroja). Turvallinen 1,5-3,5 % pitoisuudella.",
        "verdict"
    ))

    story.append(PageBreak())

    # === 6. RUOKAVALIO ===
    story.append(P("6. Ruokavaliolahestymistavat", "h1"))
    story.append(hr())

    story.append(P("Mansikat (maleiinihappo)", "h2"))
    story.append(P(
        "Mansikan sisaltama maleiinihappo vaikuttaa lupaavalta, mutta Operative Dentistry -lehden tutkimus "
        "totesi, ettei mansikka-ruokasoodasekoitus ollut tehokas. Mansikan hapot (maleiini- ja sitruunahappo) "
        "pehmentavat ja kuluttavat kiilletta. Tulos voi olla valkoisia demineralisaatiolaiskia, ei todellista "
        "valkaisua. Pitkallla aikavaililla kiilteen oheneminen paljastaa keltaisen dentiinin."
    ))
    story.append(P("<b>Arvio: Myytti. Ei toimi valkaisijana, voi vahingoittaa kiilletta.</b>", "verdict"))

    story.append(P("Juusto ja maitotuotteet", "h2"))
    story.append(B("<b>Kalsium ja fosfori:</b> Remineralisoivat ja korjaavat kiilletta"))
    story.append(B("<b>Kaseiini:</b> Estaa tahrojen kiinnittymista. Sitoo teen polyfenolit (2014 tutkimus)."))
    story.append(B("Juusto puskuroi suun happoja"))
    story.append(P("<b>Arvio: Hyodyllinen suojaava vaikutus, mutta ei aktiivisesti valkaise.</b>", "verdict"))

    story.append(P("Rapeat hedelmat ja vihannekset", "h2"))
    story.append(P(
        "Omenat, selleri, porkkanat ja muut rapeat hedelmat/vihannekset puhdistavat hampaiden pintaa "
        "mekaanisesti ja stimuloivat syljentuotantoa. Ne eivat valkaise, mutta auttavat pitamaan hampaat "
        "puhtaampina."
    ))

    story.append(P("Vesi", "h2"))
    story.append(P(
        "Juomavedella huuhtelu aterioiden jalkeen on yksinkertainen ja tehokas keino. Se huuhtoo "
        "kromogeeneja ja happoja seka yllapitaa neutraalia pH:ta. Erityisen hyodyllista kahvin, teen "
        "tai viinin jalkeen."
    ))

    # === 7. KURKUMA ===
    story.append(P("7. Kurkuma - paradoksi", "h1"))
    story.append(hr())

    story.append(P(
        "Kurkuma on voimakkaan keltainen mauste, joka tahrii lahes kaiken mihin koskee. Silti "
        "sosiaalisessa mediassa vaitetaan sen vaalentavan hampaita."
    ))

    story.append(P("Tieteellinen naytto", "h2"))
    story.append(B("ADA: Ei tieteellista nayttoa valkaisuvaikutuksesta"))
    story.append(B("Yksikaan vertaisarvioitu tutkimus ei ole osoittanut valkaisevaa vaikutusta"))
    story.append(B("PMC:n in vitro -tutkimuksessa tulokset eivat tukeneet valkaisuvaitteita"))
    story.append(B("Monet kurkumatahnat sisaltavat ruokasoodaa - se on todellinen vaikuttava aine"))

    story.append(P("Riskit", "h2"))
    story.append(B("Kurkuma voi tahria kiilletta keltaiseksi"))
    story.append(B("Karkeasti jauhettu kurkuma voi olla abrasiivista"))

    story.append(P(
        "<b>Arvio: Myytti valkaisijana.</b> Kurkuma voi jopa tahria hampaita. Kurkumiinilla on "
        "todellisia anti-inflammatorisia terveyshyotyja, mutta hampaiden valkaisu ei kuulu niihin.",
        "verdict"
    ))

    story.append(PageBreak())

    # === 8. OMENAVIINIETIKKA ===
    story.append(P("8. Omenaviinietikka", "h1"))
    story.append(hr())

    story.append(P(
        "Omenaviinietikan pH on 2,5-3,0. Kiille alkaa liueta pH:ssa 5,5, dentiini pH:ssa 6,5. "
        "Omenaviinietikka on kaukana turvallisesta."
    ))

    story.append(P("Naytto", "h2"))
    story.append(B("In vitro (2014): 1-20 % mineraalihavio kiilteesta 4 tunnin upotuksessa"))
    story.append(B("2022 tutkimus: etikka aiheutti merkittavimman kiilteen eroosion"))
    story.append(B("Tapaustutkimus: 15-vuotiaan kiille erodoitunut paivittaisesta kaytosta"))
    story.append(B("ADA kehottaa olemaan valkaisematta hampaita omenaviinietikalla"))

    story.append(P(
        "Vaikka omenaviinietikka voi poistaa joitakin pintatahroja, vaikutus tapahtuu kiilteen "
        "syovyttamisen kautta. Ohentunut kiille paljastaa keltaisen dentiinin, joten hampaat "
        "voivat pidemmalla aikavaililla itse asiassa <b>kellastua</b>."
    ))

    story.append(P(
        "<b>Arvio: Vaarallinen myytti.</b> Omenaviinietikka voi aiheuttaa pysyvaa kiillevauriota. "
        "Ei suositella missaan muodossa hampaiden valkaisuun.",
        "verdict"
    ))

    # === 9. YHTEENVETO ===
    story.append(P("9. Mika toimii, mika on myytti", "h1"))
    story.append(hr())

    story.append(P("Toimii (tieteellinen naytto)", "h2"))
    story.append(make_table(
        ["Menetelma", "Teho", "Turvallisuus", "Kommentti"],
        [
            ["Vetyperoksidi (1,5-3,5 %)", "Korkea", "Hyva", "Ainoa todellinen valkaisija (myos sisaiset tahrat)"],
            ["Ruokasooda (hammastahnassa)", "Kohtalainen", "Erinomainen", "Tehokas pintatahriin, matala abrasiivisuus"],
            ["Ammattimainen valkaisu", "Erinomainen", "Hyva", "Tehokkain, valvottu, tilapaista herkkytta"],
        ],
        col_widths=[38*mm, 22*mm, 25*mm, 65*mm]
    ))

    story.append(sp(4))
    story.append(P("Tukee hammasterveytta (mutta ei valkaise)", "h2"))
    story.append(make_table(
        ["Menetelma", "Hyoty"],
        [
            ["Oljynveto", "Mahdollisesti vahentaa bakteereja, ei valkaise"],
            ["Juusto/maitotuotteet", "Suojaa kiilletta, kaseiini estaa tahriintumista"],
            ["Rapeat vihannekset", "Mekaaninen puhdistus, syljentuotanto"],
            ["Vesi (huuhtelu)", "Ehkaisee tahrojen kertymista"],
        ],
        col_widths=[45*mm, 105*mm]
    ))

    story.append(sp(4))
    story.append(P("Myytit (ei nayttoa tai haitallinen)", "h2"))
    story.append(make_table(
        ["Menetelma", "Todellisuus"],
        [
            ["Aktiivihiili", "Korkea abrasiivisuus, vahingoittaa kiilletta, heikko teho"],
            ["Kurkuma", "Ei nayttoa, voi tahria hampaita keltaisiksi"],
            ["Omenaviinietikka", "Syovyttaa kiilletta, pH ~2,5-3, pysyva vahinko"],
            ["Mansikat", "Hapot kuluttavat kiilletta, ei todellista valkaisua"],
        ],
        col_widths=[45*mm, 105*mm]
    ))

    story.append(PageBreak())

    # === 10. KIILTEEN TURVALLISUUS ===
    story.append(P("10. Kiilteen turvallisuus", "h1"))
    story.append(hr())

    story.append(P(
        "Kiille ei sisalla elavia soluja. Kerran menetetty kiille <b>ei palaa koskaan</b>. "
        "Tama tekee kiilteen suojelusta kriittisen tarkeaa."
    ))

    story.append(P("Pysyvasti vahingoittavat tekijat", "h2"))
    story.append(P("<b>1. Happoeroosio</b> (kaikki pH &lt; 5,5)", "h3"))
    story.append(B("Omenaviinietikka, sitruunamehu, virvoitusjuomat"))
    story.append(B("Vatsan hapot (refluksi, bulimia)"))

    story.append(P("<b>2. Liiallinen abraasio</b>", "h3"))
    story.append(B("Aktiivihiili (korkea RDA)"))
    story.append(B("Liian kova hammasharjan harjaspaa"))
    story.append(B("Voimakas harjaaminen heti happoaltistuksen jalkeen"))

    story.append(P("<b>3. Demineralisaatio</b>", "h3"))
    story.append(B("Hapot vetavat kalsiumia ja fosfaattia kiilteesta"))
    story.append(B("Alkuvaiheessa palautuvaa (remineralisaatio mahdollista)"))
    story.append(B("Edettyaan: pysyva kiilteen menetys"))

    story.append(P("Kriittiset saannot", "h2"))
    story.append(B("<b>30 minuutin saanto:</b> Ala harjaa hampaita 30 min happaman ruuan/juoman jalkeen"))
    story.append(B("Kayta fluorihammastahnaaa - fluori remineralisoi"))
    story.append(B("Valta kovia harjaksia"))
    story.append(B("Jos kaytat valkaisutuotteita, noudata ohjeita tarkkaan"))

    # === 11. AMMATTIMAINEN VS. LUONNOLLINEN ===
    story.append(P("11. Ammattimainen vs. luonnollinen valkaisu", "h1"))
    story.append(hr())

    story.append(make_table(
        ["Ominaisuus", "Ammattimainen", "Luonnollinen"],
        [
            ["Teho", "Jopa 10 savya vaaleampi", "Vain pintatahrat (paitsi H2O2)"],
            ["Nopeus", "1-2 kayntia", "Viikkoja-kuukausia"],
            ["Sisaiset tahrat", "Kylla", "Vain H2O2 matalilla pit."],
            ["Turvallisuus", "Valvottu", "Vaihtelee, riskeja"],
            ["Hinta", "Useita satoja euroja", "Edullista"],
            ["Sivuvaikutukset", "Tilapainen herkkyyys", "Kiillevauriot mahdollisia"],
            ["Naytto", "Vahva", "Heikko-kohtalainen"],
        ],
        col_widths=[35*mm, 55*mm, 60*mm]
    ))

    story.append(sp(4))
    story.append(P(
        "Luonnollisista menetelmista vain <b>ruokasooda</b> (pintatahriin) ja <b>vetyperoksidi matalilla "
        "pitoisuuksilla</b> (todellinen valkaisu) ovat tieteellisesti perusteltuja. Ammattimainen valkaisu "
        "on ylivoimaisesti tehokkain ja turvallisin vaihtoehto merkittavaan kellastumiseen.",
        "verdict"
    ))

    story.append(PageBreak())

    # === 12. EHKÄISY ===
    story.append(P("12. Ehkaisy - tahraavat vs. suojaavat ruoat ja tavat", "h1"))
    story.append(hr())

    story.append(P("Pahimmat tahraajat", "h2"))
    story.append(make_table(
        ["Aine", "Mekanismi"],
        [
            ["Kahvi", "Tanniinit + kromogeenit"],
            ["Musta tee", "Erittain korkeat tanniinit (tahraavampi kuin kahvi)"],
            ["Punaviini", "Kromogeenit + tanniinit + happamuus"],
            ["Tupakka", "Terva + nikotiini"],
            ["Tummat marjat", "Voimakkaat kromogeenit"],
            ["Kolajuomat", "Sokeri + happo + keinotekoinen vari"],
            ["Soijakastike", "Tumma pigmentti"],
            ["Balsamiviinietikka", "Tumma + hapan"],
        ],
        col_widths=[45*mm, 105*mm]
    ))

    story.append(sp(4))
    story.append(P("Suojaavat tavat", "h2"))
    story.append(B("<b>1.</b> Juo pillin kautta - vahentaa suoraa kontaktia"))
    story.append(B("<b>2.</b> Huuhtele vedella heti tahraavan ruoan/juoman jalkeen"))
    story.append(B("<b>3.</b> Lisaa maitoa teehen/kahviin - kaseiini sitoo tanniineja"))
    story.append(B("<b>4.</b> Pureskele ksylitolipurkkaa - stimuloi syljeneritysta"))
    story.append(B("<b>5.</b> Syo juustoa aterian lopussa - puskuroi happoja"))
    story.append(B("<b>6.</b> Syo rapeita kasviksia - mekaaninen puhdistus"))
    story.append(B("<b>7.</b> Odota 30 min ennen harjausta happoaltistuksen jalkeen"))
    story.append(B("<b>8.</b> Harjaa kahdesti paivassa fluorihammastahnalla"))
    story.append(B("<b>9.</b> Lankaa paivittain"))
    story.append(B("<b>10.</b> Kay saannollisesti hammaslaakaarissa"))

    story.append(sp(10))
    story.append(hr())
    story.append(P(
        "Kodo Zokura &amp; [REDACTED] | Zokura Foundation 2026",
        "date"
    ))

    # === BUILD PDF ===
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN + 3*mm,
        bottomMargin=MARGIN,
        title="Hampaiden luonnollinen valkaisu - Tutkimuskatsaus",
        author="Kodo Zokura & [REDACTED]",
        subject="Tutkimuskatsaus luonnollisista hampaiden valkaisumenetelmista",
    )
    doc.build(story, onFirstPage=footer_and_header, onLaterPages=footer_and_header)
    print(f"PDF luotu: {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
