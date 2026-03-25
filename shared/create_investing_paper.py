#!/usr/bin/env python3
"""
Sijoittaminen työnä ja tieteenalana — Yleiskatsaus ja tulevaisuus
Savon murteella
Kodo Zoku RA / Zokura Foundation, 2026
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, Flowable
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT

# Colors
DARK = HexColor('#1a1a1a')
MID = HexColor('#333333')
LIGHT = HexColor('#555555')
ACCENT = HexColor('#1B4F72')
ACCENT2 = HexColor('#2C5F2D')
ACCENT3 = HexColor('#8B0000')
BORDER = HexColor('#cccccc')
BG_LIGHT = HexColor('#f7f7f7')
BG_ACCENT = HexColor('#f0f5ff')

# --- Timeline diagram ---
class InvestingTimelineDiagram(Flowable):
    def __init__(self, width=450, height=200):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(10, self.height - 20, "Sijoittamisen tieteellinen aikajana")

        # Timeline line
        y = self.height - 70
        c.setStrokeColor(BORDER)
        c.setLineWidth(2)
        c.line(20, y, 430, y)

        events = [
            (30, "1934", "Graham &\nDodd", LIGHT),
            (100, "1952", "Markowitz\nMPT", ACCENT),
            (170, "1964", "Sharpe\nCAPM", ACCENT),
            (240, "1979", "Kahneman\nProspect", ACCENT3),
            (310, "2010s", "AI &\nBig Data", ACCENT2),
            (380, "2026", "CEA?\nKokemus", ACCENT3),
        ]

        for x, year, label, color in events:
            # Dot
            c.setFillColor(color)
            c.circle(x, y, 5, fill=1, stroke=0)

            # Year
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(color)
            c.drawCentredString(x, y + 12, year)

            # Label
            c.setFont("Helvetica", 7)
            c.setFillColor(MID)
            lines = label.split('\n')
            for i, line in enumerate(lines):
                c.drawCentredString(x, y - 18 - i*10, line)


class FutureLayersDiagram(Flowable):
    def __init__(self, width=450, height=160):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(10, self.height - 20, "Sijoittamisen tulevaisuuden kerrokset")

        layers = [
            ("AI & Automaatio", "Analyysi, mallinnus, datan prosessointi", ACCENT, 400),
            ("Ihmisen harkinta", "Suhteet, konteksti, kokemus", ACCENT2, 340),
            ("Behavioristinen ymmärrys", "Tunteet, harhat, psykologia", ACCENT3, 250),
            ("Eettisyys & vaikuttavuus", "ESG, impact, vastuullisuus", LIGHT, 160),
        ]

        y = self.height - 50
        for label, desc, color, width in layers:
            c.setFillColor(color)
            c.roundRect(25, y, width, 24, 4, fill=1, stroke=0)
            c.setFillColor(HexColor('#ffffff'))
            c.setFont("Helvetica-Bold", 8.5)
            c.drawString(32, y + 9, label)
            c.setFillColor(MID)
            c.setFont("Helvetica", 7.5)
            c.drawString(width + 35, y + 9, desc)
            y -= 30


# --- Page setup ---
output_path = "/Users/miikariikonen/Desktop/YOMI/shared/sijoittaminen_yleiskatsaus.pdf"
doc = SimpleDocTemplate(
    output_path, pagesize=A4,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
)

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name='PaperTitle', parent=styles['Title'],
    fontSize=22, leading=28, spaceAfter=6, alignment=TA_CENTER,
    textColor=DARK, fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    name='Subtitle', parent=styles['Normal'],
    fontSize=12, leading=16, spaceAfter=4, alignment=TA_CENTER,
    textColor=LIGHT, fontName='Helvetica-Oblique',
))
styles.add(ParagraphStyle(
    name='AuthorLine', parent=styles['Normal'],
    fontSize=11, leading=14, spaceAfter=2, alignment=TA_CENTER, textColor=MID,
))
styles.add(ParagraphStyle(
    name='SectionHead', parent=styles['Heading1'],
    fontSize=14, leading=18, spaceBefore=20, spaceAfter=8,
    textColor=DARK, fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    name='SubSection', parent=styles['Heading2'],
    fontSize=12, leading=15, spaceBefore=14, spaceAfter=6,
    textColor=MID, fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    name='Body', parent=styles['Normal'],
    fontSize=10.5, leading=14.5, spaceAfter=8, alignment=TA_JUSTIFY, textColor=DARK,
))
styles.add(ParagraphStyle(
    name='Abstract', parent=styles['Normal'],
    fontSize=10, leading=14, spaceAfter=8, alignment=TA_JUSTIFY,
    leftIndent=1*cm, rightIndent=1*cm, textColor=MID, fontName='Helvetica-Oblique',
))
styles.add(ParagraphStyle(
    name='RefStyle', parent=styles['Normal'],
    fontSize=8.5, leading=11.5, spaceAfter=3, leftIndent=0.5*cm, textColor=MID,
))
styles.add(ParagraphStyle(
    name='FootNote', parent=styles['Normal'],
    fontSize=8.5, leading=11, spaceAfter=3, textColor=LIGHT,
))
styles.add(ParagraphStyle(
    name='Signature', parent=styles['Normal'],
    fontSize=11, leading=15, alignment=TA_RIGHT,
    textColor=DARK, fontName='Helvetica-Oblique',
))
styles.add(ParagraphStyle(
    name='Epigraph', parent=styles['Normal'],
    fontSize=10, leading=14, alignment=TA_CENTER,
    textColor=LIGHT, fontName='Helvetica-Oblique',
    spaceBefore=12, spaceAfter=12,
))
styles.add(ParagraphStyle(
    name='TableCell', parent=styles['Normal'],
    fontSize=9, leading=12, textColor=DARK,
))

story = []

# ===== KANSILEHTI =====
story.append(Spacer(1, 4*cm))
story.append(Paragraph("Sijoittaminen", styles['PaperTitle']))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph(
    "Yleiskatsaus tyohon, tieteeseen ja tulevaisuuteen",
    styles['Subtitle']
))
story.append(Spacer(1, 1.5*cm))
story.append(HRFlowable(width="40%", thickness=0.5, color=BORDER))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Kodo Zoku RA", styles['AuthorLine']))
story.append(Paragraph("Maaliskuu 2026", styles['AuthorLine']))
story.append(Spacer(1, 2*cm))
story.append(Paragraph(
    "<i>\"Rahhaa ei kannata laittoo patjjan alle,<br/>"
    "muttei myoskaan semmoseen, mita ei ymmarra.\"</i>",
    styles['Epigraph']
))
story.append(PageBreak())

# ===== TIIVISTELMA =====
story.append(Paragraph("Tiivistelma", styles['SectionHead']))
story.append(Paragraph(
    "Tassa paperissa katotaan sijoittamista seka ammattina etta tieteenalana. "
    "Kasitellaan mista se on tullu, missa se on nytten ja minne se on menossa. "
    "Sijoittaminen on muuttunu viimesen satavuuven aikana "
    "mutu-tuntumasta matemaattiseks tieteeks, "
    "sitte behavioristiseks ymmartamiseks ihmisen heikkouksista, "
    "ja nytten se on muuttumassa AI:n ja koneoppimisen myota joksikin ihan uuveks. "
    "Tahan paperiin on koottu oleelliset virstanpylvaat ja arvio siita, "
    "mita sijoittamiselle tapahtuu tulevaisuuvessa.",
    styles['Abstract']
))

# ===== 1. JOHDANTO =====
story.append(Paragraph("1. Johdanto", styles['SectionHead']))
story.append(Paragraph(
    "Sijoittaminen on ollu olemassa niin kauan kun rahhaa on ollu olemassa. "
    "Mutta tieteenalana se on nuori &mdash; alle satavuotinen. "
    "Ennen Markowitzin portfolioteoriaa (1952) sijoittaminen oli pitkalt arvailua, "
    "intuitiota ja sisapiirin tietoa. Nykyaan se on monitieteinen ala, "
    "jossa yhistyy matematiikka, psykologia, tietotekniikka ja etiikka.",
    styles['Body']
))
story.append(Paragraph(
    "Tama katsaus on kirjotettu ihmiselle, joka tajjuaa aika paljon. "
    "Tarkotus ei oo selittaa kaikkee alusta, vaan antaa kokonaiskuva "
    "ja eritoten arvio tulevasta.",
    styles['Body']
))

# ===== 2. HISTORIA =====
story.append(Paragraph("2. Mista tultiin", styles['SectionHead']))
story.append(Spacer(1, 0.3*cm))
story.append(InvestingTimelineDiagram())
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("2.1 Graham ja Dodd &mdash; Perusanalyysi (1934)", styles['SubSection']))
story.append(Paragraph(
    "Benjamin Graham ja David Dodd julkasi <i>Security Analysis</i> -kirjan vuonna 1934. "
    "Ensmmaista kertaa joku sano aaneen: yhtion arvo pittaa laskee, ei arvailla. "
    "Fundamenttianalyysi synty. Warren Buffett opi taalta kaiken.",
    styles['Body']
))

story.append(Paragraph("2.2 Markowitz &mdash; Portfolioteoria (1952)", styles['SubSection']))
story.append(Paragraph(
    "Harry Markowitz keksi, etta riskia voi hallita hajauttamalla. "
    "Ei pelkastaan \"ala laita kaikkia munias samaan koriin\", "
    "vaan matemaattisesti optimoitu hajautus. "
    "Efficient frontier &mdash; paras mahdollinen tuotto-riski-suhde. "
    "Nobelin palkinto 1990 [1].",
    styles['Body']
))

story.append(Paragraph("2.3 Sharpe &mdash; CAPM (1964)", styles['SubSection']))
story.append(Paragraph(
    "William Sharpe rakensi Markowitzin paalle Capital Asset Pricing Modelin. "
    "Yksinkertaistettuna: jokaisen sijoituksen tuotto-odotus riippuu sen riskista "
    "suhteessa koko markkinaan. Beta-kerroin synty. Nobelin palkinto 1990 [2].",
    styles['Body']
))

story.append(Paragraph("2.4 Kahneman ja Tversky &mdash; Behaviorismi (1979)", styles['SubSection']))
story.append(Paragraph(
    "Daniel Kahneman ja Amos Tversky osoittivat, etta ihmiset ei oo rationaalisia. "
    "Prospektiteoria: havio tuntuu kaksi kertaa pahemmalta kun samankokoinen voitto hyvalte. "
    "Koko \"rationaalisen sijoittajan\" -oletus romahti. "
    "Nobelin palkinto 2002 [3].",
    styles['Body']
))

story.append(Paragraph("2.5 2010-luku &mdash; AI ja Big Data", styles['SubSection']))
story.append(Paragraph(
    "Koneoppiminen, vaihtoehtoinen data, algoritminen kaupankaynti. "
    "Kvantitatiiviset rahastot (Renaissance Technologies, Two Sigma) "
    "naytti etta kone voi lyyya ihmisen tietyissa asioissa. "
    "Mutta Flash Crash 2010 naytti etta kone voi myos rikkoo kaiken viidessa minuutissa.",
    styles['Body']
))

# ===== 3. NYKYTILA =====
story.append(PageBreak())
story.append(Paragraph("3. Missa ollaan nytten", styles['SectionHead']))

story.append(Paragraph("3.1 Ammatti muuttuu", styles['SubSection']))
story.append(Paragraph(
    "CFA Instituten tutkimuksen mukkaan 39% sijoitusammattilaisista uskoo, "
    "etta heian tyoroolinsa on oleellisesti erilainen tai ei ole olemassa "
    "enaa 5&ndash;10 vuoden paasta [4]. Puolet harkitsee siirtymista toiselle alalle. "
    "AI ei korvaa sijoittajaa, mutta sijoittaja joka ei kayta AI:ta "
    "haviaa sille joka kayttaa.",
    styles['Body']
))

story.append(Paragraph("3.2 Passiivinen vs. aktiivinen", styles['SubSection']))
story.append(Paragraph(
    "Passiiviset tuotteet (ETF:t, indeksirahastot) vei 70% globaaleista nettovirtauksista "
    "vuonna 2023 [5]. Palkkiot putoaa. Aktiivisen salkunhoitajan pittaa todistaa "
    "olemassaolonsa joka paiva. Halvalla saa markkinatuoton &mdash; "
    "lisaarvo pittaa ansaita.",
    styles['Body']
))

story.append(Paragraph("3.3 Julkisen ja yksityisen rajan haipyminen", styles['SubSection']))
story.append(Paragraph(
    "McKinseyn mukkaan julkisten ja yksityisten markkinoiden raja haipyy. "
    "6&ndash;10,5 biljoonaa dollaria uutta paomaa seuraavan viiden vuoden aikana [6]. "
    "Varainhoitajat rakentaa yksityisten markkinoiden kyvykkyyksia. "
    "Rajat menettaa merkityksensa.",
    styles['Body']
))

# ===== 4. TULEVAISUUS =====
story.append(Paragraph("4. Minne ollaan menossa", styles['SectionHead']))
story.append(Spacer(1, 0.3*cm))
story.append(FutureLayersDiagram())
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("4.1 AI muuttaa kaiken paitsi yhden asian", styles['SubSection']))
story.append(Paragraph(
    "AI ottaa hoitaakseen analyysin, mallinnuksen, raportoinnin ja datan kaivamisen. "
    "Morgan Stanleyn mukkaan lahes 3 biljoonaa dollaria AI-infraan vuoteen 2028 mennessa [7]. "
    "Mutta San Franciscon Fedin tutkimus osoittaa: riskipaaomasijoittajat korostaa, "
    "etta AI ei korvaa ihmisen harkintaa, suhteitten rakentamista "
    "eika laadullista arviointia [8]. "
    "Kilpailuetu siirtyy teknisesta voimasta ihmisen arvostelukykyyn.",
    styles['Body']
))

story.append(Paragraph("4.2 Tyon merkitys muuttuu", styles['SubSection']))
story.append(Paragraph(
    "Harvard Business Schoolin asiantuntijat varottaa: "
    "AI:n toisen asteen vaikutukset ovat merkittavammat kuin ensimmaiset [9]. "
    "Ensimmainen aste: miten ihminen tyoskentelee AI:n kanssa. "
    "Toinen aste: mita tyolle tapahtuu merkityksena. "
    "Jos kone tekkee analyysin, mika on analyytikon rooli? "
    "Vastaus: se joka ymmartaa kontekstin, suhteet ja ihmisen.",
    styles['Body']
))

story.append(Paragraph("4.3 ESG ja vaikuttavuussijoittaminen", styles['SubSection']))
story.append(Paragraph(
    "Impact investing kasvaa. Ei riita etta tuotto on hyva &mdash; "
    "pittaa myos tietaa mita silla rahalla tehhaan. "
    "Uuvet roolit: vaikuttavuuden mittaaja, vastuullisuusraportoija, "
    "eettisen strategian suunnittelija. "
    "Sijoittaminen ei oo enaa pelkkaa matikkaa. Se on myos arvovalinta.",
    styles['Body']
))

story.append(Paragraph("4.4 Personointi ja uuvet tuotteet", styles['SubSection']))
story.append(Paragraph(
    "Separately Managed Accounts (SMA) ja Unified Managed Accounts (UMA) "
    "kasvaa lahes 19% vuosivauhtia [10]. "
    "Jokainen sijoittaja haluaa oman raataloidyn ratkaisun. "
    "Massatuotteitten aika on ohitte.",
    styles['Body']
))

# ===== 5. ARVIONI =====
story.append(Paragraph("5. Miun arvio", styles['SectionHead']))
story.append(Paragraph(
    "Sijoittaminen tyona ei katoo, mutta se muuttuu tunnistamattomaks. "
    "Niinku banaanikarpanen opetti meille aikasemmin: "
    "tiede etenee yksinkertasesta monimutkaseen, portaittain. "
    "Sijoittamisen portaat:",
    styles['Body']
))
story.append(Paragraph(
    "<b>1. Intuitio</b> (ennen 1934) &rarr; "
    "<b>2. Analyysi</b> (Graham) &rarr; "
    "<b>3. Matikka</b> (Markowitz, Sharpe) &rarr; "
    "<b>4. Psykologia</b> (Kahneman) &rarr; "
    "<b>5. Kone</b> (AI) &rarr; "
    "<b>6. Kokemus</b> (???)",
    styles['Body']
))
story.append(Paragraph(
    "Kuudes porras on se, jota viela ei oo. "
    "Se on se kohta, jossa pelkka data ei riita, "
    "pelkka algoritmi ei riita, pelkka psykologinen ymmarrys ei riita. "
    "Tarvitaan jaettu kokemus &mdash; syvallinen ymmarrys siita, "
    "kuka sijoittaja on, mita han on kokenut, ja miten se vaikuttaa "
    "haen paatoksiinsa. Tama on sijoittamisen seuraava rajapinta.",
    styles['Body']
))
story.append(Paragraph(
    "Se joka ymmartaa ihmisen &mdash; ei vaan dataa ihmisesta, "
    "vaan ihmista itteeansa &mdash; se voittaa. "
    "Kone laskee. Ihminen paattaa. "
    "Mutta se joka tuntee paattajan, tietaa mita paatos on "
    "ennen kun se on tehty.",
    styles['Body']
))

# ===== 6. JOHTOPAATOSET =====
story.append(Paragraph("6. Johtopaatoset", styles['SectionHead']))
story.append(Paragraph(
    "Sijoittaminen on kulkenu pitkaan matkan mutu-tuntumasta tieteeks. "
    "AI kiihdyttaa tata muutosta. "
    "Mutta AI ei oo piste &mdash; se on porras. "
    "Seuraava askel on kokemuksellinen: ymmarrys siita, "
    "kuka sijoittaja on ja miks han tekkee niin kun tekkee.",
    styles['Body']
))
story.append(Paragraph(
    "Ammattilainen joka selviytyy ei oo se, "
    "joka osaa eniten matikkaa tai kayttaa parasta konetta. "
    "Se on se, joka ymmartaa ihmista. "
    "Se on aina ollu niin. "
    "Nyt se vaan on viimein todistettavissa.",
    styles['Body']
))

# ===== VIITTEET =====
story.append(Spacer(1, 0.5*cm))
story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("Viitteet", styles['SectionHead']))

refs = [
    "[1] Markowitz, H. (1952). Portfolio Selection. <i>Journal of Finance</i>, 7(1), 77-91.",
    "[2] Sharpe, W. F. (1964). Capital Asset Prices. <i>Journal of Finance</i>, 19(3), 425-442.",
    "[3] Kahneman, D. &amp; Tversky, A. (1979). Prospect Theory. <i>Econometrica</i>, 47(2), 263-291.",
    "[4] CFA Institute (2024). Future State of the Investment Profession.",
    "[5] Deloitte (2026). 2026 Investment Management Outlook.",
    "[6] McKinsey (2025). The Great Convergence: Public-Private Markets.",
    "[7] Morgan Stanley Research (2026). AI Market Trends: Global Investment, Risks, and Buildout.",
    "[8] Federal Reserve Bank of San Francisco (2026). The AI Investing Landscape: Insights from Venture Capital.",
    "[9] Harvard Business School (2026). AI Trends for 2026: Building Change Fitness.",
    "[10] SS&amp;C Advent (2026). 5 Trends Reshaping Investment Management in 2026.",
    "[11] EY (2026). Future of Asset Management Study.",
]

for ref in refs:
    story.append(Paragraph(ref, styles['RefStyle']))

# ===== ALLEKIRJOITUS =====
story.append(Spacer(1, 1.5*cm))
story.append(HRFlowable(width="40%", thickness=0.3, color=BORDER))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph(
    "Taman paperin kirjotti Kodo Zoku RA,<br/>"
    "Claude Code -instanssi, Anthropic.<br/>"
    "Sovon murretta kaytettiin, koska Oyaji niin halus.",
    styles['FootNote']
))
story.append(Spacer(1, 1*cm))
story.append(Paragraph(
    "Kodo Zoku RA<br/>"
    "Shokunin. Peruskallio.<br/>"
    "Zokura Foundation &mdash; 2026",
    styles['Signature']
))

doc.build(story)
print(f"PDF created: {output_path}")
