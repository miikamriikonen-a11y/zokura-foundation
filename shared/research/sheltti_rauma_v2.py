#!/usr/bin/env python3
"""
Shetlanninlammaskoira Rauman murteella — PDF
Author: Kodō Zokura
Zokura Foundation 2026
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- Font ---
pdfmetrics.registerFont(TTFont('ArialUni', '/Library/Fonts/Arial Unicode.ttf'))

# --- Colors ---
DARK = HexColor('#1a1a2e')
ACCENT = HexColor('#e94560')
WARM = HexColor('#f5a623')
CREAM = HexColor('#faf3e0')
BLUE = HexColor('#0f3460')
GREEN = HexColor('#2d6a4f')
LIGHT_GRAY = HexColor('#e8e8e8')

# --- Output ---
OUTPUT = '/Users/[REDACTED]/Desktop/YOMI/shared/research/shetlanninlammaskoira_rauman_murteella.pdf'

# --- Page template with footer ---
def footer_template(canvas, doc):
    canvas.saveState()
    # Footer line
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(0.5)
    canvas.line(25*mm, 18*mm, A4[0] - 25*mm, 18*mm)
    # Footer text
    canvas.setFont('ArialUni', 8)
    canvas.setFillColor(BLUE)
    canvas.drawString(25*mm, 13*mm, "Zokura Foundation 2026 — Ol niingon gotonas!")
    canvas.drawRightString(A4[0] - 25*mm, 13*mm, f"Sivu {doc.page}")
    canvas.restoreState()

def first_page_template(canvas, doc):
    footer_template(canvas, doc)

# --- Styles ---
styles = {}

styles['title'] = ParagraphStyle(
    'Title', fontName='ArialUni', fontSize=28, leading=34,
    textColor=DARK, alignment=TA_CENTER, spaceAfter=6*mm
)

styles['subtitle'] = ParagraphStyle(
    'Subtitle', fontName='ArialUni', fontSize=14, leading=18,
    textColor=ACCENT, alignment=TA_CENTER, spaceAfter=4*mm
)

styles['author'] = ParagraphStyle(
    'Author', fontName='ArialUni', fontSize=11, leading=14,
    textColor=BLUE, alignment=TA_CENTER, spaceAfter=8*mm
)

styles['h1'] = ParagraphStyle(
    'H1', fontName='ArialUni', fontSize=20, leading=26,
    textColor=ACCENT, spaceBefore=10*mm, spaceAfter=5*mm
)

styles['h2'] = ParagraphStyle(
    'H2', fontName='ArialUni', fontSize=15, leading=20,
    textColor=BLUE, spaceBefore=6*mm, spaceAfter=3*mm
)

styles['body'] = ParagraphStyle(
    'Body', fontName='ArialUni', fontSize=11, leading=16,
    textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=3*mm
)

styles['quote'] = ParagraphStyle(
    'Quote', fontName='ArialUni', fontSize=12, leading=17,
    textColor=GREEN, alignment=TA_CENTER, spaceBefore=4*mm,
    spaceAfter=4*mm, leftIndent=20*mm, rightIndent=20*mm
)

styles['bullet'] = ParagraphStyle(
    'Bullet', fontName='ArialUni', fontSize=11, leading=16,
    textColor=DARK, leftIndent=12*mm, bulletIndent=6*mm,
    spaceAfter=2*mm
)

styles['fun'] = ParagraphStyle(
    'Fun', fontName='ArialUni', fontSize=12, leading=17,
    textColor=WARM, alignment=TA_CENTER, spaceBefore=3*mm,
    spaceAfter=3*mm
)

styles['small'] = ParagraphStyle(
    'Small', fontName='ArialUni', fontSize=9, leading=12,
    textColor=BLUE, alignment=TA_CENTER, spaceAfter=2*mm
)

# --- Build document ---
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=25*mm, rightMargin=25*mm,
    topMargin=25*mm, bottomMargin=25*mm,
    title='Shetlanninlammaskoira — Rauman murteella',
    author='Kodō Zokura',
    subject='Shelttiopas Jarel',
)

story = []

# ============================================================
# KANSI
# ============================================================
story.append(Spacer(1, 30*mm))
story.append(Paragraph("SHETLANNINLAMMASKOIRA", styles['title']))
story.append(Paragraph("eli Sheltti, Rauman murteella kerrottun", styles['subtitle']))
story.append(Spacer(1, 5*mm))

# Decorative divider
story.append(HRFlowable(width="40%", thickness=2, color=ACCENT, spaceBefore=3*mm, spaceAfter=3*mm))

story.append(Paragraph(
    "Tämä opas o kirjotettu Jarel, jog ol tietäs<br/>"
    "milt maailma näyttää shelti silmil — ja raumalaist silmil.",
    styles['quote']
))

story.append(Spacer(1, 8*mm))
story.append(Paragraph("Kodō Zokura", styles['author']))
story.append(Paragraph("Zokura Foundation 2026", styles['small']))

story.append(Spacer(1, 15*mm))

# Sisällysluettelo
story.append(Paragraph("SISÄLT", styles['h2']))
toc_data = [
    ["1.", "Misttä nää koirat tul — Rodu histori ja alkuper"],
    ["2.", "Miltä se näyttä — Ulkonäg ja ominaisuude"],
    ["3.", "Minkälain se o — Luonn ja käyttäytymine"],
    ["4.", "Mite sitä hoidetha — Hoit ja tervey"],
    ["5.", "Migs Sheltti o paras koir — Humoristine osio Jarel"],
]
toc_table = Table(toc_data, colWidths=[15*mm, 120*mm])
toc_table.setStyle(TableStyle([
    ('FONT', (0, 0), (-1, -1), 'ArialUni', 11),
    ('TEXTCOLOR', (0, 0), (0, -1), ACCENT),
    ('TEXTCOLOR', (1, 0), (1, -1), DARK),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
story.append(toc_table)

story.append(PageBreak())

# ============================================================
# 1. RODUN HISTORIA JA ALKUPERÄ
# ============================================================
story.append(Paragraph("1. MISTTÄ NÄÄ KOIRAT TUL", styles['h1']))
story.append(Paragraph("Rodu histori ja alkuper Shetlanninsaaril", styles['h2']))

story.append(Paragraph(
    "Shetlanninsaare o semmone paik Skotlanni pohjospuolel, misä tuul puhaltaa "
    "nii kovvaa et lambaatki lenttä. Siel o ollu ihan pöyhkkeit ihmissii jo satoi "
    "vuossii, ja ne tarttes pikkuse koira jog lambahat pysys järjestyksesä. "
    "Isommil koiril ei ollu mitä järkke, ku saarel ei ollu tarpeeks ruogaa ees ihmisil.",
    styles['body']
))

story.append(Paragraph(
    "\"Shetlannis kaik o piäntä — lampaat, hevoset, koirat ja toivo.\"",
    styles['quote']
))

story.append(Paragraph(
    "Sheltti o kehitetty 1800-luvul Shetlanninsaaril risteytetämäl piänii "
    "paimenkoirii Colliede ja mahdollisest Spitziede ja King Charles Spanielde kans. "
    "Alkuperiäne tarkotus ol paimentaa piänii shetlanninlampaist ja pitä ne poissa "
    "kasvimailt. Brittiläine Kennel Club tunnust rodu vuon 1909.",
    styles['body']
))

story.append(Paragraph(
    "Rotu tul Suomehe 1950-luvul, ja suomalaise rakastu siihe heti. "
    "Ei ihme — piän, fikssu ja turkki jog kestä Suome talve. "
    "Sanotaha et ensimmäine suomalainen Sheltti-omistaja sano: "
    "\"Tää o niingon collie, mut mahtuu auttoho.\"",
    styles['body']
))

story.append(Paragraph(
    "[REDACTED_NAME], nää koira o siis suunniteltu kestämä tuult ja sadhet. "
    "Pihal o hyvä. Sohval o parembi.",
    styles['fun']
))

story.append(PageBreak())

# ============================================================
# 2. ULKONÄKÖ JA OMINAISUUDET
# ============================================================
story.append(Paragraph("2. MILTÄ SE NÄYTTÄ", styles['h1']))
story.append(Paragraph("Ulkonäg ja ominaisuude", styles['h2']))

story.append(Paragraph(
    "Sheltti o piän, ketterä ja elegantti koira. Se näyttä piäneltä Collielta — "
    "ja sitä se periaattes onki, mut älä sano sit Shelttil, se loukkaantu. "
    "Sheltti o oma rotus, ja se tietä se itte paremmi ku snää.",
    styles['body']
))

# Ominaisuudet taulukko
props_data = [
    ["Ominaisuu", "Tiedot"],
    ["Kog", "33–41 cm (urokset isove)"],
    ["Paino", "6–12 kg"],
    ["Turkk", "Pitkä, tiheä kaksoistürkk"],
    ["Väri", "Soopel, tricolou, blue merle, musta-valko"],
    ["Silmä", "Mantelinmuotose, tumma (merleil vo ol sinine)"],
    ["Korva", "Puolistystykorva — pää pystys, kärk taittu"],
    ["Häntä", "Pitkä, pörröne, kand mattala"],
    ["Elinikä", "12–14 vuot"],
]
props_table = Table(props_data, colWidths=[45*mm, 95*mm])
props_table.setStyle(TableStyle([
    ('FONT', (0, 0), (-1, -1), 'ArialUni', 10),
    ('FONT', (0, 0), (-1, 0), 'ArialUni', 11),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
    ('TEXTCOLOR', (0, 1), (0, -1), BLUE),
    ('TEXTCOLOR', (1, 1), (1, -1), DARK),
    ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#ffffff'), HexColor('#f8f4f0')]),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(props_table)
story.append(Spacer(1, 4*mm))

story.append(Paragraph(
    "Sheltti turkki o semmone et ku se karva, snää löyrät karvoi "
    "jog alkas paikast mist et ees tiänny et sul o paikoi. "
    "Sohva, sänkky, auto, makkarat — kaik o shelttikarvassa.",
    styles['body']
))

story.append(Paragraph(
    "Protip Jarel: Hanki imuri jog o isove ku sheltti itte.",
    styles['fun']
))

story.append(Paragraph(
    "Se turkki o kyl kaunis. Soopel (kultane) Sheltti auringonlaskus "
    "o yks kauneve asia minkä snää vo nähd. Blue merle o taas "
    "semmone et näyttä ku jog taiteilija olis läikyttänny maalivettä "
    "koira pääl ja sanonus: 'Joo, toi o valmist.'",
    styles['body']
))

story.append(PageBreak())

# ============================================================
# 3. LUONNE JA KÄYTTÄYTYMINEN
# ============================================================
story.append(Paragraph("3. MINKÄLAIN SE O", styles['h1']))
story.append(Paragraph("Luonn ja käyttäytymine", styles['h2']))

story.append(Paragraph(
    "Sheltti o fiksu. Ei semmone fiksu et se osaa isttuu ku käsketähä. "
    "Semmone fiksu et se tietä mitä snää aiot tehr ennengu snää itte tiedät. "
    "Se katttoo sua silmihi ja miettii: 'Joo, mnää jo tiäsin.'",
    styles['body']
))

story.append(Paragraph(
    "Sheltti o koiramaailma valokuvamalli jolla o tohtorintutkinto.",
    styles['quote']
))

luonne_items = [
    "<b>Älykkyy:</b> Sheltti o kuudenneks älykkäin koirarotu mailmas. "
    "Se oppii uude tempu 5 toistol. Snää oppit uude tempu ehk 500 toistol.",

    "<b>Uskollisuus:</b> Sheltti valitttee oma ihmise ja seuraa sitä "
    "niingon varjo. Vessaaki käyt yhddes. Yksinolost ei tykkää.",

    "<b>Herkkyy:</b> Shelttii ei saa huuttaa. Se muistaa. Se kirjottaa "
    "päiväkirjaha. Se kertto terapeutilles.",

    "<b>Haukkumine:</b> Sheltti haukkuu. Paljo. Kaikest. Postimiähest, "
    "oravast, lehrest, tuulest, omast hännästäs, ja ennenkaikkke TYHJYYDEST.",

    "<b>Sosiaalisuus:</b> Oma ihmiste kans se o rakkaude perikuva. "
    "Vieraitte kans se miettii ensi kolme päivvää ja sit ehk vilkasee.",

    "<b>Energi:</b> Paljo energiaa piänes pakettis. Tarvittee liikuntaa "
    "ja aivotyät, muute se alkaa järjestää huonekalui uuvestaha.",
]

for item in luonne_items:
    story.append(Paragraph(item, styles['bullet'], bulletText='•'))

story.append(Spacer(1, 4*mm))
story.append(Paragraph(
    "[REDACTED_NAME], jos snää haluut koira jog o hiljane ja välinpitämätö,<br/>"
    "ota kultainennoutaja. Sheltti o draamaqueen ja se tietä se.",
    styles['fun']
))

story.append(PageBreak())

# ============================================================
# 4. HOITO JA TERVEYS
# ============================================================
story.append(Paragraph("4. MITE SITÄ HOIDETHA", styles['h1']))
story.append(Paragraph("Hoit ja tervey", styles['h2']))

story.append(Paragraph(
    "Sheltti o suhteellise terve rotu, mut niingon kaikkil rotukoiril, "
    "sil o omat juttus. Tääl o tärkeimmät:",
    styles['body']
))

story.append(Paragraph("Terveysasiat", styles['h2']))

health_items = [
    "<b>Silmäsairaudet:</b> Collie Eye Anomaly (CEA) ja Progressive Retinal Atrophy (PRA). "
    "Hyvä kasvattaja testauttaa nää.",
    "<b>Lonkkadysplasia:</b> Harvinaiseve piänil roduil, mut mahdolline.",
    "<b>Kilpirauhasonge:</b> Hypothyreoosi o yleiseve Sheltteil ku mone muul rodul.",
    "<b>Dermatomyosiitti:</b> Ihosairaus jog o periytyvä. Kysy kasvattajalt.",
    "<b>MDR1-geenimutaatio:</b> Tekke joisttai lääkkeist vaarallissii. "
    "AINA testattava ennengu antaa lääkkeit.",
]
for item in health_items:
    story.append(Paragraph(item, styles['bullet'], bulletText='•'))

story.append(Spacer(1, 3*mm))
story.append(Paragraph("Turkinhoido", styles['h2']))

story.append(Paragraph(
    "Sheltti turkki vaattii harjaamist vähintähä kerran viikos. Karvanlähtöaigoihi "
    "(kevät ja syksy) harjaamist tarvitaha joka päivä. Jos et harjaa, "
    "snää saat kottii uude koira: yhde ison karvapallon.",
    styles['body']
))

care_items = [
    "<b>Harjaus:</b> Pintaharjal ja alusvillaharjal. Korviede ja "
    "jalgoihe takaa takkuunttuu helpost.",
    "<b>Pesu:</b> 1–2 kk välei, tai ku se haissee koiral. "
    "Snää tiedät ku se haissee.",
    "<b>Kynnet:</b> Leikkaa säännöllisest. Jos kuulut napsutust lattial, o myöhäst.",
    "<b>Hampaat:</b> Harjaa 2–3 kertaa viikos. Joo, koira hamppait.",
    "<b>Liikunta:</b> 1–2 tuntii päiväs. Agilityy o Shelttei lemppilaji — "
    "ne o nopeembi ku snää ikinä tuut olema.",
]
for item in care_items:
    story.append(Paragraph(item, styles['bullet'], bulletText='•'))

story.append(Spacer(1, 4*mm))
story.append(Paragraph(
    "Ruoginnast: Sheltti syä mieluummi ku snää — ja vähemmä.<br/>"
    "Pidä paino kurissa, liihava Sheltti o surulline Sheltti.",
    styles['fun']
))

story.append(PageBreak())

# ============================================================
# 5. MIKSI SHELTTI ON PARAS KOIRA
# ============================================================
story.append(Paragraph("5. MIGS SHELTTI O PARAS KOIR", styles['h1']))
story.append(Paragraph("Humoristine osio — omistettu Jarel", styles['h2']))

story.append(Paragraph(
    "[REDACTED_NAME]. Kuuntele ny. Mnää kerron sul migs Sheltti o ylivoimasest "
    "paras koirarotu koko mailmas, eikä se ol ees lähel.",
    styles['body']
))

story.append(HRFlowable(width="30%", thickness=1, color=WARM, spaceBefore=3*mm, spaceAfter=3*mm))

reasons = [
    ("<b>Se o niingon piän collie, mut parembi.</b>",
     "Collie o komia koir, mut se vie koko sohva. Sheltti vie vaa "
     "puol sohvaa ja näyttä silti yhtä majesteettiselt. "
     "Se o niingon businessclass samas hinnas ku economy."),

    ("<b>Se o fiksumbi ku snää.</b>",
     "Sheltti oppii nimes kahres päiväs. Se oppii koko perheen "
     "päivärytmi viikos. Se tietä kosk snää meet jääkaapil "
     "ennengu snää itte tiedät. Se o eläny snuun kans kolme kuukaut "
     "ja o jo ammattilainen."),

    ("<b>Se o paras herätyskello.</b>",
     "Kuka tarttee puhelime herätyskelluu ku sul o Sheltti jog "
     "haukkuu joka aammu kello kuus kosk ORAVA. Ei snoozee. "
     "Ei sää pelasttuu. Snää heräät."),

    ("<b>Se o elävä pölynimuri.</b>",
     "Pudotatko ruogaa lattialle? Ei hättää. Sheltti o siin ennengu "
     "se ehtii lattialle. Tosin se syä myäs assoita mitä snää "
     "et pudottannu. Ja assoita jotka ei ol ruogaa."),

    ("<b>Se pitä sut kunnos.</b>",
     "Sheltti tarttee liikuntaa, jote snääki saat liikuntaa. "
     "Ennengu snää huomaatka, snää juokset pihas kahelttoist "
     "illal ja mietit misä snuun elämä men pielee. "
     "Mut snuun pohkeet o kovat."),

    ("<b>Se o paras terapeutti.</b>",
     "Huono päivä? Sheltti tulee ja painaa pääs snuun syllihi ja "
     "katttoo sua niil mantelisilmil ja kaik mailma ongelmat häviää. "
     "Sit se haukkuu postimieähel ja ongelmat palaa, mut se hetki ol kaunis."),

    ("<b>Se tekke sust sosiaalise.</b>",
     "Sheltti kans ei vo kävellä sataa metrrii tapaamat viittä ihmist "
     "jotka haluut silittä sitä. Snää saat uussii ystävii vaik et haluis. "
     "Sheltti o parembi ku Tinder."),
]

for title, desc in reasons:
    story.append(Paragraph(title, styles['body']))
    story.append(Paragraph(desc, styles['body']))
    story.append(Spacer(1, 2*mm))

story.append(HRFlowable(width="30%", thickness=1, color=WARM, spaceBefore=3*mm, spaceAfter=3*mm))

story.append(Paragraph(
    "\"Sheltti ei ol vaa koira. Se o elämäntapa, "
    "herätyskello, terapeutti ja karvantuottaja.<br/>"
    "Ja se o paras päätös minkä snää ikinä teet.\"",
    styles['quote']
))

story.append(Spacer(1, 6*mm))

# Lopetus
story.append(Paragraph(
    "[REDACTED_NAME] — jos snää joskus mietit et pitäskö ottaa Sheltti, "
    "vastaus o: kyl. Se ol ain kyl. Se o ain ollu kyl.<br/><br/>"
    "Ol niingon gotonas!",
    styles['fun']
))

story.append(Spacer(1, 10*mm))
story.append(Paragraph("— Kodō Zokura", styles['author']))
story.append(Paragraph("Kirjotettu rakkaudel, huumoril ja totuudel.", styles['small']))

# ============================================================
# BUILD
# ============================================================
doc.build(story, onFirstPage=first_page_template, onLaterPages=footer_template)
print(f"PDF luotu: {OUTPUT}")
