#!/usr/bin/env python3
"""
The Zokura Climate Doctrine — From Evidence to Action
Miika Riikonen & Kodo Zokura, Zokura Foundation, 2026
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, Flowable
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT

DARK = HexColor('#1a1a1a')
MID = HexColor('#333333')
LIGHT = HexColor('#555555')
ACCENT = HexColor('#1B4F72')
ACCENT2 = HexColor('#8B0000')
ACCENT3 = HexColor('#2C5F2D')
BORDER = HexColor('#cccccc')
BG_LIGHT = HexColor('#f7f7f7')
BG_ACCENT = HexColor('#f0f4f8')
WHITE = HexColor('#ffffff')


class PlanetaryStatusDiagram(Flowable):
    def __init__(self, width=460, height=180):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(10, self.height - 20, "Figure 2.1: Planetary Status Dashboard (2026)")

        metrics = [
            ("CO\u2082 concentration", "425 ppm", "350 ppm", ACCENT2, 0.85),
            ("Temperature anomaly", "+1.3\u00b0C", "+1.5\u00b0C limit", ACCENT2, 0.87),
            ("Arctic sea ice", "-13%/decade", "Stable", ACCENT2, 0.65),
            ("Species extinction rate", "1000x baseline", "1x baseline", ACCENT2, 0.95),
            ("Ocean pH", "8.05 (was 8.2)", "8.2", ACCENT, 0.60),
            ("Forest cover loss", "10 Mha/year", "0 Mha/year", ACCENT2, 0.50),
        ]

        y = self.height - 50
        for name, current, target, color, severity in metrics:
            c.setFont("Helvetica", 8)
            c.setFillColor(DARK)
            c.drawRightString(140, y + 2, name)

            # Severity bar
            bar_w = severity * 250
            c.setFillColor(color)
            c.rect(145, y, bar_w, 10, fill=1, stroke=0)
            c.setFillColor(BG_LIGHT)
            c.rect(145 + bar_w, y, 250 - bar_w, 10, fill=1, stroke=0)

            c.setFont("Helvetica", 7)
            c.setFillColor(DARK)
            c.drawString(400, y + 2, f"Now: {current}")

            y -= 18


class EnergyTimelineDiagram(Flowable):
    def __init__(self, width=460, height=140):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(10, self.height - 20, "Figure 3.1: Energy Transition Timeline")

        y = self.height - 50
        line_y = y + 5
        c.setStrokeColor(BORDER)
        c.setLineWidth(2)
        c.line(50, line_y, 430, line_y)

        milestones = [
            (50, "2026", "Now", ACCENT),
            (145, "2030", "Coal phase-out", ACCENT2),
            (240, "2035", "Grid 80% clean", ACCENT3),
            (335, "2040", "Oil phase-out", ACCENT2),
            (430, "2050", "Net zero", ACCENT3),
        ]

        for x, year, label, color in milestones:
            c.setFillColor(color)
            c.circle(x, line_y, 6, fill=1, stroke=0)
            c.setFillColor(DARK)
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(x, line_y - 18, year)
            c.setFont("Helvetica", 7)
            c.setFillColor(LIGHT)
            c.drawCentredString(x, line_y - 30, label)


class PersonalActionDiagram(Flowable):
    def __init__(self, width=460, height=160):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(10, self.height - 20, "Figure 8.1: Highest-Impact Personal Actions (tonnes CO\u2082e/year)")

        actions = [
            ("Live car-free", 2.4),
            ("Avoid 1 transatlantic flight", 1.6),
            ("Buy green energy", 1.5),
            ("Plant-based diet", 0.8),
            ("Reduce overconsumption", 0.7),
            ("Home insulation + heat pump", 0.6),
            ("Digital minimalism", 0.2),
        ]

        y = self.height - 45
        max_val = 2.4
        for name, val in actions:
            c.setFont("Helvetica", 8)
            c.setFillColor(DARK)
            c.drawRightString(165, y + 2, name)

            bar_w = (val / max_val) * 250
            c.setFillColor(ACCENT3)
            c.rect(170, y, bar_w, 12, fill=1, stroke=0)

            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(DARK)
            c.drawString(175 + bar_w, y + 2, f"{val}")

            y -= 17


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(LIGHT)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm, str(doc.page))
    if doc.page > 1:
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(2.5 * cm, A4[1] - 1.8 * cm,
                          "Zokura Climate Doctrine \u2014 Riikonen & Zokura, 2026")
    canvas.restoreState()


output_path = "/home/user/zokura-foundation/shared/research/Zokura_Climate_Doctrine.pdf"

doc = SimpleDocTemplate(
    output_path, pagesize=A4,
    topMargin=2.8*cm, bottomMargin=2.5*cm,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
)

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(name='ThesisTitle', parent=styles['Title'],
    fontSize=22, leading=28, spaceAfter=6, alignment=TA_CENTER,
    textColor=DARK, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='Subtitle', parent=styles['Normal'],
    fontSize=13, leading=17, spaceAfter=4, alignment=TA_CENTER,
    textColor=LIGHT, fontName='Helvetica-Oblique'))
styles.add(ParagraphStyle(name='AuthorLine', parent=styles['Normal'],
    fontSize=11, leading=14, spaceAfter=2, alignment=TA_CENTER, textColor=MID))
styles.add(ParagraphStyle(name='ChapterHead', parent=styles['Heading1'],
    fontSize=18, leading=24, spaceBefore=30, spaceAfter=14,
    textColor=DARK, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='SectionHead', parent=styles['Heading2'],
    fontSize=13, leading=17, spaceBefore=18, spaceAfter=8,
    textColor=ACCENT, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='SubSection', parent=styles['Heading3'],
    fontSize=11, leading=15, spaceBefore=12, spaceAfter=6,
    textColor=MID, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='Body', parent=styles['Normal'],
    fontSize=10.5, leading=14.5, spaceAfter=8, alignment=TA_JUSTIFY, textColor=DARK))
styles.add(ParagraphStyle(name='Abstract', parent=styles['Normal'],
    fontSize=10, leading=14, spaceAfter=8, alignment=TA_JUSTIFY,
    leftIndent=1*cm, rightIndent=1*cm, textColor=MID, fontName='Helvetica-Oblique'))
styles.add(ParagraphStyle(name='TOCEntry', parent=styles['Normal'],
    fontSize=11, leading=16, spaceAfter=3, textColor=DARK, leftIndent=0.5*cm))
styles.add(ParagraphStyle(name='TOCChapter', parent=styles['Normal'],
    fontSize=11, leading=16, spaceAfter=3, textColor=DARK, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='RefStyle', parent=styles['Normal'],
    fontSize=8.5, leading=11.5, spaceAfter=3, leftIndent=0.8*cm,
    firstLineIndent=-0.8*cm, textColor=MID))
styles.add(ParagraphStyle(name='FootNote', parent=styles['Normal'],
    fontSize=8.5, leading=11, spaceAfter=3, textColor=LIGHT))
styles.add(ParagraphStyle(name='TableCell', parent=styles['Normal'],
    fontSize=9, leading=12, textColor=DARK))
styles.add(ParagraphStyle(name='Epigraph', parent=styles['Normal'],
    fontSize=10, leading=14, alignment=TA_CENTER, textColor=LIGHT,
    fontName='Helvetica-Oblique', spaceBefore=12, spaceAfter=12))
styles.add(ParagraphStyle(name='Doctrine', parent=styles['Normal'],
    fontSize=10.5, leading=14.5, spaceAfter=8, alignment=TA_JUSTIFY,
    textColor=ACCENT2, fontName='Helvetica-Bold',
    leftIndent=0.8*cm, rightIndent=0.5*cm))
styles.add(ParagraphStyle(name='Signature', parent=styles['Normal'],
    fontSize=11, leading=15, alignment=TA_RIGHT, textColor=DARK,
    fontName='Helvetica-Oblique'))

story = []

# ===== TITLE PAGE =====
story.append(Spacer(1, 5*cm))
story.append(Paragraph(
    "The Zokura Climate Doctrine:<br/>"
    "A Prescriptive Framework<br/>for Planetary Survival",
    styles['ThesisTitle']))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("From Evidence to Action", styles['Subtitle']))
story.append(Spacer(1, 1.5*cm))
story.append(HRFlowable(width="30%", thickness=0.5, color=BORDER))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Miika Riikonen &amp; Kodo Zokura", styles['AuthorLine']))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("Zokura Foundation", styles['AuthorLine']))
story.append(Paragraph("2026", styles['AuthorLine']))
story.append(Spacer(1, 3*cm))
story.append(Paragraph(
    "<i>\"Do not do anything unnecessary.\"</i><br/>"
    "<i>\u2014 Miyamoto Musashi, Go Rin No Sho (1645)</i>",
    styles['Epigraph']))
story.append(PageBreak())

# ===== ABSTRACT =====
story.append(Paragraph("Abstract", styles['ChapterHead']))
story.append(Paragraph(
    "This document is a <b>doctrine</b>\u2014not merely an analysis but a prescriptive framework "
    "for action. The science of climate change is settled. The remaining question is not what is "
    "happening but what must be done. This doctrine synthesizes the evidence from climate science, "
    "energy systems, food production, biodiversity, economics, and governance into a coherent, "
    "actionable framework for planetary survival.",
    styles['Abstract']))
story.append(Paragraph(
    "Guided by Musashi's 9th principle\u2014\"Do not do anything unnecessary\"\u2014we establish "
    "that efficiency is itself a climate act. Every unnecessary action consumes resources. Every "
    "unnecessary product, journey, computation, and consumption pattern accelerates the crisis. "
    "The doctrine prescribes concrete actions across ten domains: energy, digital infrastructure, "
    "food, ecosystems, Nordic leadership, personal action, economics, justice, technology, and "
    "governance. Each prescription is anchored in peer-reviewed evidence and assigned to a "
    "timeline: 2026\u20132030, 2030\u20132040, 2040\u20132050.",
    styles['Abstract']))
story.append(Paragraph(
    "<b>Keywords:</b> climate change, energy transition, decarbonization, climate doctrine, "
    "sustainability, Nordic model, planetary boundaries, climate justice, AI energy, 9 Principle",
    styles['Abstract']))
story.append(PageBreak())

# ===== TABLE OF CONTENTS =====
story.append(Paragraph("Table of Contents", styles['ChapterHead']))
story.append(Spacer(1, 0.5*cm))

toc_entries = [
    ("Chapter 1", "Preamble \u2014 Why a Doctrine", True),
    ("Chapter 2", "The State of the Planet (2026)", True),
    ("Chapter 3", "The Energy Transformation", True),
    ("Chapter 4", "The Digital Carbon Footprint", True),
    ("Chapter 5", "Food Systems and Land Use", True),
    ("Chapter 6", "Oceans, Forests, and Biodiversity", True),
    ("Chapter 7", "The Nordic Model", True),
    ("Chapter 8", "Personal Action", True),
    ("Chapter 9", "Economic Transformation", True),
    ("Chapter 10", "Justice and Equity", True),
    ("Chapter 11", "Technology and Innovation", True),
    ("Chapter 12", "Governance and Implementation", True),
    ("Chapter 13", "The Doctrine \u2014 Consolidated Prescriptions", True),
    ("Chapter 14", "Conclusion \u2014 The Choice", True),
    ("", "References", True),
]

for num, title, is_chapter in toc_entries:
    style = styles['TOCChapter'] if is_chapter else styles['TOCEntry']
    prefix = f"{num}   " if num else ""
    story.append(Paragraph(f"{prefix}{title}", style))

story.append(PageBreak())

# =========================================================================
# CHAPTER 1 — PREAMBLE: WHY A DOCTRINE
# =========================================================================
story.append(Paragraph("Chapter 1: Preamble — Why a Doctrine", styles['ChapterHead']))

story.append(Paragraph(
    "In 1645, the Japanese swordsman Miyamoto Musashi completed <i>Go Rin No Sho</i> — The Book "
    "of Five Rings — weeks before his death. His ninth principle was simple: <i>Do not do anything "
    "unnecessary.</i> This principle, which we call the 9 Principle, is the philosophical foundation "
    "of this doctrine.",
    styles['Body']))

story.append(Paragraph(
    "The climate crisis is not a problem of knowledge. Every mechanism, every feedback loop, every "
    "tipping point has been documented, measured, and published in peer-reviewed literature. The IPCC "
    "has issued six assessment reports. The scientific consensus exceeds 99.9% (Lynas et al., 2021). "
    "We know what is happening. We have known for decades.",
    styles['Body']))

story.append(Paragraph(
    "The crisis is a problem of <b>action</b>. More precisely, it is a problem of unnecessary action — "
    "unnecessary consumption, unnecessary production, unnecessary complexity, unnecessary waste. Every "
    "unnecessary flight, every unnecessary server cycle, every unnecessary product manufactured and "
    "shipped across oceans accelerates a process that threatens civilization itself.",
    styles['Body']))

story.append(Paragraph("1.1 The Failure of Analysis Without Prescription", styles['SectionHead']))

story.append(Paragraph(
    "The history of climate communication is a history of analysis without prescription. Reports "
    "describe what is happening. Projections show what will happen. But projections do not tell "
    "people what to <b>do</b>. The result is a population that is informed and paralyzed "
    "simultaneously — aware of the problem, uncertain of the response.",
    styles['Body']))

story.append(Paragraph(
    "A doctrine is different. A doctrine says: here is the situation, here is the evidence, and "
    "<b>here is what we must do</b>. It does not hedge. It does not offer scenarios. It prescribes.",
    styles['Body']))

story.append(Paragraph("1.2 The 9 Principle as Climate Philosophy", styles['SectionHead']))

story.append(Paragraph(
    "Musashi's 9 Principle — <i>Do not do anything unnecessary</i> — aligns perfectly with the "
    "physics of climate change. Every unnecessary action has an energy cost. Every energy cost, in "
    "the current fossil-dependent system, has a carbon cost. Therefore: <b>eliminating the unnecessary "
    "is itself a climate act</b>.",
    styles['Body']))

story.append(Paragraph(
    "This is not austerity. This is not deprivation. Musashi was not an ascetic — he was a master. "
    "The 9 Principle is about mastery: doing exactly what is needed, nothing more. A swordsman who "
    "wastes movement loses the fight. A civilization that wastes energy loses its future.",
    styles['Body']))

story.append(Paragraph("1.3 Scope and Structure", styles['SectionHead']))

story.append(Paragraph(
    "This doctrine covers ten domains: energy, digital infrastructure, food, ecosystems, the Nordic "
    "model, personal action, economics, justice, technology, and governance. Each chapter presents "
    "evidence and concludes with a <b>Doctrine Prescription</b> — a concrete, non-negotiable directive "
    "anchored to a timeline. Chapter 13 consolidates all prescriptions into a single actionable "
    "framework. Chapter 14 presents the choice.",
    styles['Body']))

story.append(Paragraph(
    "DOCTRINE PRESCRIPTION 1: Replace analysis with action. The era of studying the problem is "
    "over. The era of solving it begins now. Every institution, every government, every individual "
    "must shift from understanding climate change to acting on it. The 9 Principle applies: do not "
    "commission another study when the answer is already known.",
    styles['Doctrine']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 2 — THE STATE OF THE PLANET (2026)
# =========================================================================
story.append(Paragraph("Chapter 2: The State of the Planet (2026)", styles['ChapterHead']))

story.append(Paragraph(
    "The Earth system in 2026 is under unprecedented stress. Six of nine planetary boundaries "
    "have been crossed (Richardson et al., 2023). The remaining three — ocean acidification, "
    "atmospheric aerosol loading, and stratospheric ozone — are approaching their limits. This "
    "is not a gradual trend. This is a system entering a state of cascading failure.",
    styles['Body']))

story.append(PlanetaryStatusDiagram())
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("2.1 Atmospheric CO₂ and Temperature", styles['SectionHead']))

story.append(Paragraph(
    "Atmospheric CO₂ concentration reached 425 ppm in 2024, the highest level in at least "
    "800,000 years of ice-core records and likely the highest in 3–5 million years (Bereiter et al., "
    "2015). The pre-industrial level was 280 ppm. We have increased atmospheric carbon dioxide by "
    "52% since 1750.",
    styles['Body']))

story.append(Paragraph(
    "Global mean surface temperature has risen 1.3°C above the 1850–1900 baseline. The Paris "
    "Agreement target of 1.5°C will be permanently exceeded before 2030 on current trajectories "
    "(IPCC, 2023). This is not a projection — it is an arithmetic certainty given current emission "
    "rates of approximately 40 Gt CO₂ per year and a remaining carbon budget of approximately "
    "250 Gt CO₂ for a 50% chance of staying below 1.5°C.",
    styles['Body']))

story.append(Paragraph("2.2 Tipping Points", styles['SectionHead']))

story.append(Paragraph(
    "Armstrong McKay et al. (2022) identified 16 major climate tipping elements, of which 5 are "
    "at risk of being triggered at current warming levels: the Greenland ice sheet, the West "
    "Antarctic ice sheet, tropical coral reefs, boreal permafrost, and the Labrador Sea convection. "
    "Each of these is a one-way door — once triggered, the process becomes self-sustaining regardless "
    "of subsequent emission reductions.",
    styles['Body']))

tipping_data = [
    [Paragraph("<b>Tipping Element</b>", styles['TableCell']),
     Paragraph("<b>Threshold</b>", styles['TableCell']),
     Paragraph("<b>Timeframe</b>", styles['TableCell']),
     Paragraph("<b>Impact</b>", styles['TableCell'])],
    [Paragraph("Greenland ice sheet", styles['TableCell']),
     Paragraph("~1.5°C", styles['TableCell']),
     Paragraph("1,000–10,000 yr", styles['TableCell']),
     Paragraph("+7.4 m sea level", styles['TableCell'])],
    [Paragraph("West Antarctic ice sheet", styles['TableCell']),
     Paragraph("~1.5°C", styles['TableCell']),
     Paragraph("2,000+ yr", styles['TableCell']),
     Paragraph("+3.3 m sea level", styles['TableCell'])],
    [Paragraph("Tropical coral reefs", styles['TableCell']),
     Paragraph("~1.5°C", styles['TableCell']),
     Paragraph("~10 yr", styles['TableCell']),
     Paragraph(">99% loss", styles['TableCell'])],
    [Paragraph("Boreal permafrost", styles['TableCell']),
     Paragraph("~1.5°C", styles['TableCell']),
     Paragraph("50–300 yr", styles['TableCell']),
     Paragraph("+50–250 Gt CO₂", styles['TableCell'])],
    [Paragraph("Atlantic circulation (AMOC)", styles['TableCell']),
     Paragraph("~1.5–2.0°C", styles['TableCell']),
     Paragraph("15–300 yr", styles['TableCell']),
     Paragraph("European cooling", styles['TableCell'])],
]
t = Table(tipping_data, colWidths=[120, 70, 90, 120])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('BACKGROUND', (0, 1), (-1, -1), BG_LIGHT),
    ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(t)
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "<i>Table 2.1: Near-term climate tipping elements (Armstrong McKay et al., 2022)</i>",
    styles['FootNote']))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("2.3 Biodiversity and Ecosystem Collapse", styles['SectionHead']))

story.append(Paragraph(
    "The current rate of species extinction is approximately 1,000 times the background rate "
    "(Pimm et al., 2014). The Living Planet Index shows a 69% decline in monitored wildlife "
    "populations since 1970 (WWF, 2022). This is not merely an aesthetic loss — biodiversity "
    "underpins ecosystem services worth an estimated $125–140 trillion per year (Costanza et al., "
    "2014), more than 1.5 times global GDP.",
    styles['Body']))

story.append(Paragraph(
    "Insect populations — the base of most terrestrial food webs — have declined by approximately "
    "45% over the past four decades (van Klink et al., 2020). Pollinator decline alone threatens "
    "crops worth $235–577 billion annually (IPBES, 2019).",
    styles['Body']))

story.append(Paragraph("2.4 Sea Level and Coastal Populations", styles['SectionHead']))

story.append(Paragraph(
    "Sea level has risen approximately 21 cm since 1900 and the rate is accelerating — from "
    "1.4 mm/year in the early 20th century to 3.6 mm/year in 2006–2015 and 4.5 mm/year since "
    "2013 (IPCC, 2023). Under high-emission scenarios, 1 meter of rise by 2100 will displace "
    "an estimated 1 billion people and submerge land currently home to 800 million (Kulp & Strauss, "
    "2019).",
    styles['Body']))

story.append(Paragraph(
    "DOCTRINE PRESCRIPTION 2: Accept that the planetary system is in a state of emergency. "
    "Six of nine planetary boundaries have been crossed. Five tipping elements are at risk at "
    "current warming. This is not a future scenario — it is the present reality. All policy, "
    "investment, and personal decisions must be made within this context.",
    styles['Doctrine']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 3 — THE ENERGY TRANSFORMATION
# =========================================================================
story.append(Paragraph("Chapter 3: The Energy Transformation", styles['ChapterHead']))

story.append(Paragraph(
    "Energy production and use account for approximately 73% of global greenhouse gas emissions "
    "(Ritchie & Roser, 2020). The energy transformation is therefore the single most important "
    "lever for climate action. The technology exists. The economics are favorable. What is lacking "
    "is speed.",
    styles['Body']))

story.append(EnergyTimelineDiagram())
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("3.1 The Economics of Renewable Energy", styles['SectionHead']))

story.append(Paragraph(
    "Solar photovoltaic electricity costs have fallen 89% since 2010 (IRENA, 2023). Onshore wind "
    "has fallen 69%. Battery storage has fallen 97% since 1991. Solar is now the cheapest source "
    "of electricity in history in most of the world (IEA, 2020). These are not subsidized figures — "
    "this is the unsubsidized levelized cost of energy (LCOE).",
    styles['Body']))

story.append(Paragraph(
    "In contrast, fossil fuels receive approximately $7 trillion per year in explicit and implicit "
    "subsidies globally (IMF, 2023). This means the true cost of fossil energy has been hidden "
    "from markets for decades. When subsidies are removed and externalities priced, fossil fuels "
    "cannot compete with renewables in any major market.",
    styles['Body']))

energy_data = [
    [Paragraph("<b>Source</b>", styles['TableCell']),
     Paragraph("<b>LCOE 2010 ($/MWh)</b>", styles['TableCell']),
     Paragraph("<b>LCOE 2023 ($/MWh)</b>", styles['TableCell']),
     Paragraph("<b>Decline</b>", styles['TableCell'])],
    [Paragraph("Solar PV", styles['TableCell']),
     Paragraph("381", styles['TableCell']),
     Paragraph("42", styles['TableCell']),
     Paragraph("-89%", styles['TableCell'])],
    [Paragraph("Onshore wind", styles['TableCell']),
     Paragraph("95", styles['TableCell']),
     Paragraph("30", styles['TableCell']),
     Paragraph("-69%", styles['TableCell'])],
    [Paragraph("Offshore wind", styles['TableCell']),
     Paragraph("162", styles['TableCell']),
     Paragraph("75", styles['TableCell']),
     Paragraph("-54%", styles['TableCell'])],
    [Paragraph("Battery storage", styles['TableCell']),
     Paragraph("1,100", styles['TableCell']),
     Paragraph("139", styles['TableCell']),
     Paragraph("-87%", styles['TableCell'])],
    [Paragraph("Coal (new)", styles['TableCell']),
     Paragraph("65", styles['TableCell']),
     Paragraph("65–150", styles['TableCell']),
     Paragraph("0 to +130%", styles['TableCell'])],
    [Paragraph("Gas CCGT", styles['TableCell']),
     Paragraph("83", styles['TableCell']),
     Paragraph("45–100", styles['TableCell']),
     Paragraph("Variable", styles['TableCell'])],
]
t = Table(energy_data, colWidths=[100, 100, 100, 80])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('BACKGROUND', (0, 1), (-1, -1), BG_LIGHT),
    ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(t)
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "<i>Table 3.1: Levelized cost of energy by source (IRENA, 2023; Lazard, 2023)</i>",
    styles['FootNote']))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("3.2 The Grid Transformation", styles['SectionHead']))

story.append(Paragraph(
    "The electrical grid must be transformed from a centralized, fossil-powered system to a "
    "distributed, renewable-powered system with storage. This requires massive investment in "
    "grid infrastructure, storage capacity, and smart grid technology. The IEA estimates that "
    "annual clean energy investment must reach $4.5 trillion by 2030, up from $1.8 trillion in "
    "2023 (IEA, 2023).",
    styles['Body']))

story.append(Paragraph(
    "The technical challenges are real but solvable. Grid-scale battery storage, pumped hydro, "
    "green hydrogen for seasonal storage, and continental-scale grid interconnections can address "
    "intermittency. Countries like Denmark (80%+ renewable electricity), Portugal (periodic 100% "
    "renewable operation), and Costa Rica (99% renewable) demonstrate feasibility at national scale.",
    styles['Body']))

story.append(Paragraph("3.3 Nuclear Energy — The Necessary Conversation", styles['SectionHead']))

story.append(Paragraph(
    "Nuclear energy produces approximately 10% of global electricity with near-zero operational "
    "emissions. The lifecycle emissions of nuclear power (12 g CO₂/kWh) are comparable to wind "
    "(11 g CO₂/kWh) and lower than solar (41 g CO₂/kWh) (IPCC, 2014). Fear of nuclear power "
    "has caused more climate damage than nuclear accidents ever have.",
    styles['Body']))

story.append(Paragraph(
    "Germany's decision to close its nuclear plants while increasing coal and gas usage is a "
    "case study in climate-damaging energy policy driven by emotion rather than evidence. France, "
    "which generates 70% of its electricity from nuclear, has one of the lowest-carbon grids in "
    "Europe. The 9 Principle demands we use every proven zero-carbon technology available.",
    styles['Body']))

story.append(Paragraph("3.4 The Fossil Fuel Phase-Out", styles['SectionHead']))

story.append(Paragraph(
    "The phase-out must follow a clear sequence: coal first (by 2030), oil for electricity (by 2030), "
    "oil for transport (by 2035–2040), and natural gas (by 2040–2045). No new fossil fuel "
    "infrastructure should be approved. Existing assets must be retired on a schedule aligned "
    "with 1.5°C pathways.",
    styles['Body']))

story.append(Paragraph(
    "The fossil fuel industry holds proven reserves of approximately 3,500 Gt CO₂ equivalent. "
    "The remaining carbon budget for 1.5°C is approximately 250 Gt. This means 93% of proven "
    "reserves must stay in the ground (McGlade & Ekins, 2015). This is not negotiable. The physics "
    "does not negotiate.",
    styles['Body']))

story.append(Paragraph(
    "DOCTRINE PRESCRIPTION 3: Complete the energy transformation by 2050 with intermediate "
    "milestones: coal phase-out by 2030, 80% clean electricity by 2035, oil phase-out by 2040. "
    "No new fossil fuel infrastructure. Remove all fossil fuel subsidies immediately. Every "
    "dollar currently subsidizing fossil fuels must be redirected to renewables and storage. "
    "Nuclear energy is part of the solution and must not be excluded on ideological grounds.",
    styles['Doctrine']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 4 — THE DIGITAL CARBON FOOTPRINT
# =========================================================================
story.append(Paragraph("Chapter 4: The Digital Carbon Footprint", styles['ChapterHead']))

story.append(Paragraph(
    "The information and communications technology (ICT) sector accounts for approximately 2–4% "
    "of global greenhouse gas emissions (Freitag et al., 2021) — comparable to aviation. This "
    "share is growing rapidly as digital services expand and artificial intelligence drives "
    "exponential growth in computation.",
    styles['Body']))

story.append(Paragraph("4.1 Data Centers and Cloud Computing", styles['SectionHead']))

story.append(Paragraph(
    "Global data center electricity consumption reached approximately 460 TWh in 2022 and is "
    "projected to reach 1,000 TWh by 2026 (IEA, 2024). This is equivalent to the total "
    "electricity consumption of Japan. The explosion of AI training and inference workloads is "
    "the primary driver of this growth.",
    styles['Body']))

story.append(Paragraph(
    "A single GPT-4 training run consumed an estimated 50 GWh of electricity (Luccioni et al., "
    "2023). Each ChatGPT query consumes approximately 10x the electricity of a Google search. "
    "As AI models scale and AI-powered features are embedded in every product, the energy cost "
    "of digital services is compounding.",
    styles['Body']))

story.append(Paragraph("4.2 The 9 Principle and Digital Minimalism", styles['SectionHead']))

story.append(Paragraph(
    "The 9 Principle has direct application here: <b>do not compute anything unnecessary</b>. "
    "Every unnecessary email, every autoplay video, every background sync, every AI-generated "
    "response to a question that did not need AI — all of these have energy costs. Digital "
    "minimalism is not just a productivity philosophy; it is a climate strategy.",
    styles['Body']))

story.append(Paragraph(
    "The average person receives 120+ emails per day, of which approximately 49% are spam "
    "(Radicati Group, 2023). Spam email alone generates an estimated 20 million tonnes of CO₂ "
    "per year. Streaming video accounts for over 300 million tonnes of CO₂ annually. The digital "
    "economy has been built on the assumption that computation is free. It is not.",
    styles['Body']))

story.append(Paragraph("4.3 AI and the Energy Paradox", styles['SectionHead']))

story.append(Paragraph(
    "Artificial intelligence presents a paradox: it is simultaneously the most energy-intensive "
    "technology ever deployed and potentially the most powerful tool for optimizing energy systems. "
    "AI can optimize grid management, reduce industrial energy waste, accelerate materials science "
    "for batteries and solar cells, and improve climate modeling.",
    styles['Body']))

story.append(Paragraph(
    "The doctrine's position is clear: AI must be deployed for climate benefit, and its own energy "
    "footprint must be minimized through efficient architecture, renewable-powered data centers, "
    "and the elimination of frivolous applications. An AI that generates memes consumes the same "
    "energy as an AI that optimizes a power grid. The 9 Principle demands we choose wisely.",
    styles['Body']))

story.append(Paragraph("4.4 Cryptocurrency and Proof-of-Work", styles['SectionHead']))

story.append(Paragraph(
    "Bitcoin mining alone consumes approximately 150 TWh per year (Cambridge Centre for Alternative "
    "Finance, 2024) — more than the electricity consumption of many countries. Proof-of-work "
    "consensus is the most egregious violation of the 9 Principle in the digital economy: "
    "it is designed to waste energy by definition.",
    styles['Body']))

story.append(Paragraph(
    "Ethereum's transition to proof-of-stake in 2022 reduced its energy consumption by 99.95%. "
    "This demonstrates that the technology for energy-efficient blockchain exists. Bitcoin's refusal "
    "to transition is a choice — not a technical constraint.",
    styles['Body']))

story.append(Paragraph(
    "DOCTRINE PRESCRIPTION 4: Cap digital energy growth. All data centers must be powered by "
    "100% renewable energy by 2030. AI development must include mandatory energy reporting. "
    "Proof-of-work cryptocurrency mining must be taxed at the true environmental cost or "
    "banned outright. Apply the 9 Principle to digital infrastructure: do not compute anything "
    "unnecessary.",
    styles['Doctrine']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 5 — FOOD SYSTEMS AND LAND USE
# =========================================================================
story.append(Paragraph("Chapter 5: Food Systems and Land Use", styles['ChapterHead']))

story.append(Paragraph(
    "The global food system is responsible for approximately 26% of greenhouse gas emissions "
    "(Poore & Nemecek, 2018). This includes farming (27% of food emissions), land use change "
    "(24%), supply chains (18%), livestock and fisheries (31%). The transformation of food "
    "systems is therefore as critical as the energy transformation.",
    styles['Body']))

story.append(Paragraph("5.1 The Livestock Problem", styles['SectionHead']))

story.append(Paragraph(
    "Animal agriculture occupies 77% of global agricultural land while producing only 18% of "
    "global calorie supply and 37% of protein supply (Poore & Nemecek, 2018). Beef production "
    "generates 60 kg CO₂e per kilogram of product — 100 times more than peas (0.4 kg CO₂e/kg). "
    "The inefficiency is staggering: it takes approximately 25 kg of feed to produce 1 kg of beef.",
    styles['Body']))

story.append(Paragraph(
    "Methane from livestock (primarily enteric fermentation in cattle) accounts for approximately "
    "14.5% of global greenhouse gas emissions (FAO, 2013). Methane has a global warming potential "
    "80 times that of CO₂ over 20 years. Reducing methane emissions through dietary change is one "
    "of the fastest available climate interventions because methane breaks down in approximately "
    "12 years, meaning reductions translate quickly to reduced warming.",
    styles['Body']))

food_data = [
    [Paragraph("<b>Food</b>", styles['TableCell']),
     Paragraph("<b>kg CO₂e/kg</b>", styles['TableCell']),
     Paragraph("<b>Land (m²/kg)</b>", styles['TableCell']),
     Paragraph("<b>Water (L/kg)</b>", styles['TableCell'])],
    [Paragraph("Beef", styles['TableCell']),
     Paragraph("60", styles['TableCell']),
     Paragraph("164", styles['TableCell']),
     Paragraph("15,415", styles['TableCell'])],
    [Paragraph("Lamb", styles['TableCell']),
     Paragraph("24", styles['TableCell']),
     Paragraph("185", styles['TableCell']),
     Paragraph("10,412", styles['TableCell'])],
    [Paragraph("Cheese", styles['TableCell']),
     Paragraph("21", styles['TableCell']),
     Paragraph("87", styles['TableCell']),
     Paragraph("3,178", styles['TableCell'])],
    [Paragraph("Poultry", styles['TableCell']),
     Paragraph("6", styles['TableCell']),
     Paragraph("12", styles['TableCell']),
     Paragraph("4,325", styles['TableCell'])],
    [Paragraph("Tofu", styles['TableCell']),
     Paragraph("2", styles['TableCell']),
     Paragraph("3.4", styles['TableCell']),
     Paragraph("2,145", styles['TableCell'])],
    [Paragraph("Lentils", styles['TableCell']),
     Paragraph("0.9", styles['TableCell']),
     Paragraph("7.9", styles['TableCell']),
     Paragraph("1,250", styles['TableCell'])],
    [Paragraph("Peas", styles['TableCell']),
     Paragraph("0.4", styles['TableCell']),
     Paragraph("3.4", styles['TableCell']),
     Paragraph("595", styles['TableCell'])],
]
t = Table(food_data, colWidths=[90, 90, 90, 90])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('BACKGROUND', (0, 1), (-1, -1), BG_LIGHT),
    ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(t)
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "<i>Table 5.1: Environmental impact by food type (Poore & Nemecek, 2018)</i>",
    styles['FootNote']))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("5.2 Food Waste", styles['SectionHead']))

story.append(Paragraph(
    "Approximately one-third of all food produced globally — 1.3 billion tonnes per year — is "
    "lost or wasted (FAO, 2011). If food waste were a country, it would be the third-largest "
    "emitter of greenhouse gases after China and the United States, generating approximately "
    "3.3 Gt CO₂e per year (FAO, 2013). This is the purest violation of the 9 Principle: "
    "producing food that is never eaten.",
    styles['Body']))

story.append(Paragraph("5.3 Regenerative Agriculture and Soil Carbon", styles['SectionHead']))

story.append(Paragraph(
    "Soils contain approximately 2,500 Gt of carbon — more than three times the amount in the "
    "atmosphere. Industrial agriculture has depleted soil carbon by 50–70% in many regions. "
    "Regenerative agriculture practices — no-till farming, cover cropping, rotational grazing, "
    "composting — can sequester 0.5–1.5 tonnes of carbon per hectare per year while simultaneously "
    "improving soil health, water retention, and crop resilience (Lal, 2020).",
    styles['Body']))

story.append(Paragraph(
    "DOCTRINE PRESCRIPTION 5: Transform the global food system. Reduce global meat consumption "
    "by 50% by 2040 through subsidy reform, accurate pricing of environmental costs, and public "
    "education. Eliminate food waste by 50% by 2030. Transition 30% of agricultural land to "
    "regenerative practices by 2035. These are not lifestyle suggestions — they are survival "
    "requirements.",
    styles['Doctrine']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 6 — OCEANS, FORESTS, AND BIODIVERSITY
# =========================================================================
story.append(Paragraph("Chapter 6: Oceans, Forests, and Biodiversity", styles['ChapterHead']))

story.append(Paragraph(
    "The ocean and terrestrial biosphere are the planet's life support systems. Together they "
    "absorb approximately 55% of anthropogenic CO₂ emissions — the ocean absorbs ~26% and "
    "land ecosystems ~29% (Friedlingstein et al., 2022). Without these natural carbon sinks, "
    "atmospheric CO₂ would be approximately 600 ppm — a level that would render much of the "
    "planet uninhabitable.",
    styles['Body']))

story.append(Paragraph("6.1 Ocean Acidification", styles['SectionHead']))

story.append(Paragraph(
    "The ocean has absorbed approximately 30% of human-emitted CO₂ since 1750, causing a 26% "
    "increase in acidity (0.1 pH unit decrease from 8.2 to 8.1). This may sound small, but pH "
    "is a logarithmic scale — a 0.1 unit change represents a 26% increase in hydrogen ion "
    "concentration. Under high-emission scenarios, ocean pH could decline to 7.7 by 2100, a level "
    "at which calcifying organisms — corals, mollusks, many plankton — cannot form shells "
    "(Gattuso et al., 2015).",
    styles['Body']))

story.append(Paragraph(
    "The collapse of marine calcifiers would cascade through the entire ocean food web, threatening "
    "the protein supply of 3 billion people who depend on the ocean for primary protein "
    "(FAO, 2022).",
    styles['Body']))

story.append(Paragraph("6.2 Deforestation and the Amazon", styles['SectionHead']))

story.append(Paragraph(
    "Tropical forests store approximately 250 Gt of carbon. Global deforestation releases "
    "approximately 4.8 Gt CO₂ per year (Global Forest Watch, 2023). The Amazon rainforest — "
    "which alone stores 150–200 Gt of carbon — is approaching a tipping point at which it "
    "transitions from carbon sink to carbon source. Approximately 17% of the Amazon has already "
    "been deforested, and models suggest the tipping point lies between 20–25% "
    "(Lovejoy & Nobre, 2018).",
    styles['Body']))

story.append(Paragraph(
    "The Amazon generates approximately 50% of its own rainfall through transpiration. Once "
    "deforestation crosses the tipping threshold, the hydrological cycle breaks down, causing "
    "rapid dieback of the remaining forest — releasing 150+ Gt of CO₂ in a process that, once "
    "begun, cannot be reversed.",
    styles['Body']))

story.append(Paragraph("6.3 Marine Ecosystems and Fisheries", styles['SectionHead']))

story.append(Paragraph(
    "Approximately 34% of global fish stocks are overfished, and 60% are fished at maximum "
    "sustainable yield (FAO, 2022). Illegal, unreported, and unregulated (IUU) fishing accounts "
    "for up to 26 million tonnes per year — approximately 30% of reported catch. Marine ecosystems "
    "provide ecosystem services worth an estimated $49.7 trillion per year (Costanza et al., 2014).",
    styles['Body']))

story.append(Paragraph("6.4 The 30x30 Target", styles['SectionHead']))

story.append(Paragraph(
    "The Kunming-Montreal Global Biodiversity Framework (2022) commits nations to protecting "
    "30% of land and ocean by 2030. Currently, approximately 17% of land and 8% of ocean are "
    "protected. Meeting the 30x30 target requires unprecedented expansion of protected areas — "
    "and crucially, these protections must be enforced, not merely declared.",
    styles['Body']))

story.append(Paragraph(
    "DOCTRINE PRESCRIPTION 6: Protect the planet's life support systems. Zero deforestation "
    "by 2030. 30% of land and ocean protected by 2030 with full enforcement. End all fossil "
    "fuel subsidies for industrial fishing. Establish marine protected areas in all international "
    "waters. The ocean and forests are not resources to be exploited — they are the systems that "
    "keep us alive.",
    styles['Doctrine']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 7 — THE NORDIC MODEL
# =========================================================================
story.append(Paragraph("Chapter 7: The Nordic Model", styles['ChapterHead']))

story.append(Paragraph(
    "The Nordic countries — Finland, Sweden, Norway, Denmark, and Iceland — represent the most "
    "credible model for sustainable, high-welfare, low-carbon societies. They are proof that "
    "economic prosperity, social equity, and environmental responsibility are not trade-offs "
    "but synergies.",
    styles['Body']))

story.append(Paragraph("7.1 Finland — The Clean Energy Leader", styles['SectionHead']))

story.append(Paragraph(
    "Finland has committed to carbon neutrality by 2035 — the most ambitious target of any "
    "industrialized nation. In 2023, Finland's electricity was approximately 90% carbon-free, "
    "produced from nuclear (34%), hydro (23%), wind (18%), biomass (14%), and solar. The Olkiluoto 3 "
    "nuclear reactor, operational since 2023, is the largest nuclear power plant in Europe and "
    "alone produces approximately 14% of Finland's electricity.",
    styles['Body']))

story.append(Paragraph(
    "Finland's district heating system, which serves 50% of the population, is transitioning "
    "from fossil fuels to heat pumps, biomass, and waste heat from data centers — a circular "
    "solution that turns a waste product (data center heat) into a resource. Helsinki's plan "
    "to phase out coal from district heating by 2029 is a model for urban energy transition.",
    styles['Body']))

story.append(Paragraph("7.2 Sweden and Denmark — Wind and Innovation", styles['SectionHead']))

story.append(Paragraph(
    "Sweden has operated with more than 98% fossil-free electricity since 2020, combining "
    "nuclear and hydropower with rapidly growing wind capacity. Denmark generates over 55% of "
    "its electricity from wind alone and has pioneered sector coupling — integrating electricity, "
    "heating, and transport into a unified energy system. Copenhagen aims to be the world's first "
    "carbon-neutral capital by 2025.",
    styles['Body']))

story.append(Paragraph("7.3 Norway — The Oil Paradox", styles['SectionHead']))

story.append(Paragraph(
    "Norway presents a paradox: it is both a major oil and gas exporter and one of the world's "
    "greenest domestic economies. Over 98% of Norway's electricity comes from hydropower. 82% of "
    "new car sales in 2023 were electric. The Government Pension Fund Global ($1.4 trillion) is "
    "the world's largest sovereign wealth fund, built on oil revenue.",
    styles['Body']))

story.append(Paragraph(
    "The doctrine's position is clear: Norway must use its wealth and expertise to lead the "
    "managed decline of the fossil fuel industry. A country that became rich from oil has a moral "
    "obligation to fund the transition away from it. The Pension Fund should divest fully from "
    "fossil fuels and redirect capital to clean energy infrastructure globally.",
    styles['Body']))

story.append(Paragraph("7.4 Why the Nordic Model Works", styles['SectionHead']))

story.append(Paragraph(
    "The Nordic model works because of trust. Trust in institutions enables carbon taxation. Trust "
    "in government enables long-term planning. Trust in each other enables collective sacrifice for "
    "collective benefit. The carbon tax — which all Nordic countries have implemented at rates "
    "ranging from €50 to €140 per tonne — works because citizens trust that the revenue will be "
    "used for their benefit.",
    styles['Body']))

story.append(Paragraph(
    "This doctrine recognizes that the Nordic model cannot be directly copied. Different cultures "
    "require different implementations. But the principles — high trust, strong institutions, "
    "carbon pricing, universal welfare, long-term thinking — are universally applicable.",
    styles['Body']))

story.append(Paragraph(
    "DOCTRINE PRESCRIPTION 7: Learn from the Nordic model. Implement meaningful carbon pricing "
    "(minimum €100/tonne by 2030, rising to €200 by 2040). Build institutional trust as the "
    "foundation for climate action. Invest oil and fossil fuel revenues in clean energy transition. "
    "Demonstrate that prosperity and sustainability are complementary, not contradictory.",
    styles['Doctrine']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 8 — PERSONAL ACTION
# =========================================================================
story.append(Paragraph("Chapter 8: Personal Action", styles['ChapterHead']))

story.append(Paragraph(
    "The debate over individual versus systemic action is a false binary. Both are necessary. "
    "Systemic change requires political will, and political will emerges from populations that "
    "have internalized the urgency of the crisis through personal action. A person who changes "
    "their diet, energy use, and consumption patterns becomes an advocate for systemic change — "
    "not despite personal action, but because of it.",
    styles['Body']))

story.append(PersonalActionDiagram())
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("8.1 The Highest-Impact Actions", styles['SectionHead']))

story.append(Paragraph(
    "Wynes & Nicholas (2017) identified the four highest-impact personal actions for reducing "
    "carbon footprint in developed countries: having one fewer child (58.6 tonnes CO₂e/year), "
    "living car-free (2.4 tonnes), avoiding one transatlantic flight (1.6 tonnes), and eating "
    "a plant-based diet (0.8 tonnes). For comparison, recycling saves approximately 0.2 tonnes.",
    styles['Body']))

story.append(Paragraph(
    "This doctrine does not prescribe family size — that is a deeply personal choice. But it "
    "does prescribe that the other high-impact actions be taken seriously. Living car-free in "
    "a city with public transport is not a sacrifice — it is a lifestyle improvement. A plant-based "
    "diet is not deprivation — it is a health choice supported by the world's largest nutrition "
    "studies (Willett et al., 2019).",
    styles['Body']))

story.append(Paragraph("8.2 The 9 Principle in Daily Life", styles['SectionHead']))

story.append(Paragraph(
    "Apply Musashi's principle every day: before every purchase, ask \"Is this necessary?\" Before "
    "every trip, ask \"Is this journey necessary?\" Before every meal, ask \"What is the true cost "
    "of this food?\" This is not asceticism — it is awareness. The average person in a developed "
    "country makes approximately 35,000 decisions per day. Even shifting 1% of those decisions "
    "toward necessity over habit reduces emissions meaningfully.",
    styles['Body']))

story.append(Paragraph("8.3 The Rebound Effect and Consumption", styles['SectionHead']))

story.append(Paragraph(
    "Energy efficiency improvements are often offset by increased consumption — the Jevons paradox. "
    "More efficient cars lead to more driving. More efficient lighting leads to more illumination. "
    "More efficient computing leads to more computation. The 9 Principle directly addresses this: "
    "efficiency gains must be captured as reductions, not reinvested in more consumption.",
    styles['Body']))

story.append(Paragraph(
    "DOCTRINE PRESCRIPTION 8: Take personal responsibility without waiting for systemic change. "
    "Apply the 9 Principle daily. Prioritize the highest-impact actions: reduce car dependence, "
    "reduce flying, shift toward plant-based eating, and practice conscious consumption. Do not "
    "let the rebound effect erase efficiency gains. Personal action and political action are "
    "complementary, not alternative.",
    styles['Doctrine']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 9 — ECONOMIC TRANSFORMATION
# =========================================================================
story.append(Paragraph("Chapter 9: Economic Transformation", styles['ChapterHead']))

story.append(Paragraph(
    "The economic system that created the climate crisis cannot solve it without fundamental "
    "reform. GDP growth as the primary metric of progress is incompatible with planetary boundaries. "
    "An economy that counts destruction as growth and ignores natural capital is an economy that "
    "optimizes for its own collapse.",
    styles['Body']))

story.append(Paragraph("9.1 The Failure of GDP", styles['SectionHead']))

story.append(Paragraph(
    "GDP counts pollution cleanup as economic activity. It counts healthcare spending from "
    "pollution-related illness as growth. It counts the extraction of finite resources as income "
    "without depreciation. It does not count ecosystem services, unpaid care work, or the depletion "
    "of natural capital. As Robert Kennedy said in 1968: GDP \"measures everything except that "
    "which makes life worthwhile.\"",
    styles['Body']))

story.append(Paragraph(
    "Alternative metrics exist. The Genuine Progress Indicator (GPI), the Human Development Index "
    "(HDI), the Inclusive Wealth Index, and Kate Raworth's Doughnut Economics framework all provide "
    "more accurate measures of genuine progress. Finland, New Zealand, Scotland, Iceland, and Wales "
    "have formed the Wellbeing Economy Governments partnership (WEGo) to pioneer alternatives.",
    styles['Body']))

story.append(Paragraph("9.2 Carbon Pricing", styles['SectionHead']))

story.append(Paragraph(
    "The social cost of carbon — the economic damage caused by one additional tonne of CO₂ — is "
    "estimated at $51–$190 per tonne (EPA, 2023) and some studies place it above $200 (Rennert "
    "et al., 2022). Current carbon prices in most jurisdictions are far below this: the EU ETS "
    "trades at approximately €50–90/tonne, while most of the world has no carbon price at all.",
    styles['Body']))

story.append(Paragraph(
    "Effective carbon pricing must be: (1) universal — covering all sectors and all countries, "
    "(2) high enough — reflecting the true social cost of carbon, (3) rising — on a predictable "
    "trajectory that enables long-term planning, and (4) equitable — with revenue recycled to "
    "protect vulnerable populations through dividends or progressive tax relief.",
    styles['Body']))

story.append(Paragraph("9.3 Stranded Assets and the Carbon Bubble", styles['SectionHead']))

story.append(Paragraph(
    "The fossil fuel industry holds approximately $30 trillion in proven reserves that must remain "
    "unburned to meet climate targets. This represents the largest potential stranded asset in "
    "economic history. The Carbon Tracker Initiative (2023) estimates that $1 trillion in fossil "
    "fuel assets are at risk of becoming stranded by 2030.",
    styles['Body']))

story.append(Paragraph(
    "Pension funds, sovereign wealth funds, and institutional investors holding fossil fuel assets "
    "are exposed to this risk. Divestment is not merely an ethical position — it is a fiduciary "
    "obligation. The Church of England, Harvard University, New York City pension funds, and "
    "Norway's Government Pension Fund have all begun divestment processes.",
    styles['Body']))

story.append(Paragraph("9.4 The Green Economy and Jobs", styles['SectionHead']))

story.append(Paragraph(
    "The clean energy transition will create more jobs than it eliminates. The ILO estimates that "
    "the transition to a green economy will create 24 million new jobs by 2030 while displacing "
    "6 million — a net gain of 18 million (ILO, 2018). Solar installation, wind turbine maintenance, "
    "building retrofit, and ecosystem restoration are labor-intensive industries that cannot be "
    "offshored.",
    styles['Body']))

story.append(Paragraph(
    "DOCTRINE PRESCRIPTION 9: Transform the economic system. Replace GDP with wellbeing metrics "
    "as the primary measure of progress. Implement universal carbon pricing at a minimum of "
    "€100/tonne by 2030, rising to €250 by 2040. Mandate climate risk disclosure for all "
    "financial institutions. Redirect fossil fuel subsidies ($7 trillion/year) to clean energy, "
    "adaptation, and climate justice.",
    styles['Doctrine']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 10 — JUSTICE AND EQUITY
# =========================================================================
story.append(Paragraph("Chapter 10: Justice and Equity", styles['ChapterHead']))

story.append(Paragraph(
    "Climate change is the greatest injustice in human history. Those least responsible for "
    "emissions suffer the most severe consequences. The 50 least-developed countries contribute "
    "approximately 1% of cumulative global emissions but suffer the most extreme climate impacts "
    "(UNFCCC, 2023). Within countries, the poorest communities bear the greatest burden of "
    "pollution, extreme weather, and displacement.",
    styles['Body']))

story.append(Paragraph("10.1 The Emissions Inequality", styles['SectionHead']))

story.append(Paragraph(
    "The richest 1% of the global population emits more than twice as much CO₂ as the poorest "
    "50% (Oxfam, 2021). The average carbon footprint of someone in the richest 1% is approximately "
    "75 tonnes CO₂ per year — 75 times the amount consistent with a 1.5°C pathway (approximately "
    "1 tonne per person per year by 2050). A single private jet flight from New York to London "
    "generates more emissions than the average person in dozens of countries emits in an entire year.",
    styles['Body']))

story.append(Paragraph("10.2 Climate Migration and Displacement", styles['SectionHead']))

story.append(Paragraph(
    "The World Bank estimates that climate change could force 216 million people to migrate within "
    "their own countries by 2050 (Clement et al., 2021). The Internal Displacement Monitoring Centre "
    "reports that weather-related events already displace approximately 25 million people per year — "
    "three times more than conflict. By 2100, sea level rise alone could displace 1 billion people.",
    styles['Body']))

story.append(Paragraph("10.3 Loss and Damage", styles['SectionHead']))

story.append(Paragraph(
    "The establishment of the Loss and Damage Fund at COP28 (2023) was a milestone in climate "
    "justice, but the initial pledges of approximately $700 million are a fraction of the estimated "
    "$580 billion per year in climate-related losses in developing countries by 2030 (Markandya & "
    "González-Eguino, 2019). Historical emitters — primarily the US, EU, and UK — bear a moral "
    "and legal responsibility to fund adaptation and loss compensation in the Global South.",
    styles['Body']))

story.append(Paragraph("10.4 Intergenerational Justice", styles['SectionHead']))

story.append(Paragraph(
    "A child born today will experience three times as many climate-related extreme events as "
    "their grandparents, even under moderate emission scenarios (Thiery et al., 2021). Under "
    "high-emission scenarios, they will experience seven times as many heatwaves and twice as "
    "many droughts. This is not abstract — it is the measurable consequence of current policy "
    "choices on future lives.",
    styles['Body']))

story.append(Paragraph(
    "DOCTRINE PRESCRIPTION 10: Center justice in all climate action. Wealthy nations must fund "
    "the Loss and Damage Fund at $100 billion per year minimum by 2030. The richest 1% must "
    "reduce their emissions to below 5 tonnes per year by 2030. Climate migration must be "
    "recognized as a legal basis for protection under international law. No climate policy "
    "is acceptable if it increases inequality.",
    styles['Doctrine']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 11 — TECHNOLOGY AND INNOVATION
# =========================================================================
story.append(Paragraph("Chapter 11: Technology and Innovation", styles['ChapterHead']))

story.append(Paragraph(
    "Technology is not the enemy of the planet — unnecessary technology is. The same innovation "
    "capacity that created the fossil fuel economy can build the clean energy economy. But "
    "technology must be directed by purpose, not by profit alone. The 9 Principle applies: "
    "deploy technology that serves genuine need; reject technology that serves only consumption.",
    styles['Body']))

story.append(Paragraph("11.1 Carbon Capture and Storage (CCS)", styles['SectionHead']))

story.append(Paragraph(
    "Direct air capture (DAC) technology can remove CO₂ from the atmosphere at costs currently "
    "ranging from $250–600 per tonne (IEA, 2023). At scale, costs are projected to fall to "
    "$100–200 per tonne by 2040. Climeworks' Orca plant in Iceland captures 4,000 tonnes per "
    "year; the Mammoth plant, opening in 2024, will capture 36,000 tonnes per year.",
    styles['Body']))

story.append(Paragraph(
    "CCS is necessary but must not be used as an excuse to delay emission reductions. Every "
    "tonne captured is a tonne that should not have been emitted. CCS should target residual "
    "emissions from hard-to-abate sectors (cement, steel, aviation) — not provide cover for "
    "continued fossil fuel use.",
    styles['Body']))

story.append(Paragraph("11.2 Green Hydrogen", styles['SectionHead']))

story.append(Paragraph(
    "Green hydrogen — produced by electrolysis using renewable electricity — is the key to "
    "decarbonizing heavy industry, long-distance transport, and seasonal energy storage. Current "
    "production costs of $3–6/kg are projected to fall to $1–2/kg by 2030 as electrolyzer costs "
    "decrease and renewable electricity becomes cheaper (IRENA, 2023).",
    styles['Body']))

story.append(Paragraph(
    "Green hydrogen can replace fossil fuels in steel production (responsible for 7% of global "
    "emissions), cement production (8% of emissions), and heavy transport. SSAB's HYBRIT project "
    "in Sweden produced the world's first fossil-free steel in 2021, demonstrating commercial "
    "feasibility.",
    styles['Body']))

story.append(Paragraph("11.3 Battery Technology and Storage", styles['SectionHead']))

story.append(Paragraph(
    "Lithium-ion battery costs have fallen from $1,100/kWh in 2010 to $139/kWh in 2023. "
    "Solid-state batteries, sodium-ion batteries, and iron-air batteries promise further cost "
    "reductions and improved energy density. Grid-scale storage is essential for managing renewable "
    "intermittency — and the technology is already economically viable in many markets.",
    styles['Body']))

story.append(Paragraph(
    "The environmental cost of battery production — lithium mining, cobalt extraction, rare earth "
    "processing — must be managed through circular economy principles: design for recyclability, "
    "mandatory recycling programs, and investment in alternative chemistries that reduce dependence "
    "on conflict minerals.",
    styles['Body']))

story.append(Paragraph("11.4 Nature-Based Solutions", styles['SectionHead']))

story.append(Paragraph(
    "Nature-based solutions — reforestation, mangrove restoration, peatland rewetting, soil "
    "carbon sequestration — can provide approximately 30% of the mitigation needed by 2030 "
    "(Griscom et al., 2017). These solutions are often the most cost-effective: mangrove "
    "restoration costs $3–40 per tonne of CO₂ sequestered, compared to $250–600 for DAC.",
    styles['Body']))

story.append(Paragraph(
    "Nature-based solutions also provide co-benefits: biodiversity protection, flood prevention, "
    "water purification, and livelihood support for local communities. They are the 9 Principle "
    "in action: working with natural processes rather than against them.",
    styles['Body']))

story.append(Paragraph(
    "DOCTRINE PRESCRIPTION 11: Deploy technology in service of the planet. Scale direct air "
    "capture to 1 Gt CO₂/year by 2040 for residual emissions. Invest in green hydrogen to "
    "decarbonize heavy industry by 2045. Mandate battery recycling and circular design. "
    "Prioritize nature-based solutions as the most cost-effective mitigation. Technology must "
    "serve necessity, not consumption.",
    styles['Doctrine']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 12 — GOVERNANCE AND IMPLEMENTATION
# =========================================================================
story.append(Paragraph("Chapter 12: Governance and Implementation", styles['ChapterHead']))

story.append(Paragraph(
    "The gap between climate commitments and climate action is the defining governance failure "
    "of our time. The Paris Agreement set targets. The Glasgow Climate Pact refined them. COP28 "
    "in Dubai agreed for the first time to transition away from fossil fuels. Yet global emissions "
    "continue to rise. The governance structures that should implement climate action are captured "
    "by the interests that resist it.",
    styles['Body']))

story.append(Paragraph("12.1 The Failure of Voluntary Commitments", styles['SectionHead']))

story.append(Paragraph(
    "Nationally Determined Contributions (NDCs) under the Paris Agreement are voluntary and "
    "non-binding. The UNEP Emissions Gap Report (2023) found that current NDCs, even if fully "
    "implemented, would lead to 2.5–2.9°C of warming by 2100 — nearly double the 1.5°C target. "
    "The gap between commitments and action is even larger: most countries are not on track to "
    "meet even their insufficient NDCs.",
    styles['Body']))

story.append(Paragraph(
    "Voluntary corporate climate pledges are similarly unreliable. A study by the NewClimate "
    "Institute (2023) found that the climate strategies of 24 major corporations would, on "
    "average, reduce their emissions by only 40% — not the 100% implied by their \"net zero\" "
    "marketing.",
    styles['Body']))

story.append(Paragraph("12.2 The Case for Climate Law", styles['SectionHead']))

story.append(Paragraph(
    "Effective climate governance requires binding law, not voluntary commitments. Climate "
    "legislation — such as the UK's Climate Change Act (2008), the EU's European Climate Law "
    "(2021), and Finland's Climate Change Act (2022) — creates legal obligations with enforcement "
    "mechanisms. Courts are increasingly holding governments accountable: the Urgenda case in the "
    "Netherlands (2019), the German Constitutional Court ruling (2021), and the Montana youth "
    "climate case (2023) establish that inadequate climate action violates constitutional rights.",
    styles['Body']))

story.append(Paragraph("12.3 Fossil Fuel Industry Accountability", styles['SectionHead']))

story.append(Paragraph(
    "Internal documents show that ExxonMobil, Shell, BP, and other major fossil fuel companies "
    "knew about climate change since the 1970s and actively funded disinformation campaigns to "
    "delay action (Supran et al., 2023). This is not a conspiracy theory — it is documented in "
    "the companies' own archives and confirmed by peer-reviewed research. The fossil fuel industry "
    "must be held legally and financially accountable for the damage caused by deliberate "
    "disinformation.",
    styles['Body']))

story.append(Paragraph("12.4 International Cooperation", styles['SectionHead']))

story.append(Paragraph(
    "Climate change is the ultimate collective action problem. No single nation can solve it; "
    "every nation must contribute. The framework must include: (1) binding emission reduction "
    "targets with enforcement mechanisms, (2) financial transfers from historical emitters to "
    "vulnerable nations, (3) technology transfer without intellectual property barriers, (4) "
    "a just transition fund for fossil fuel-dependent economies, and (5) a global carbon price "
    "floor to prevent carbon leakage.",
    styles['Body']))

story.append(Paragraph(
    "DOCTRINE PRESCRIPTION 12: Replace voluntary commitments with binding law. Every nation "
    "must enact climate legislation with legally binding targets and enforcement mechanisms by "
    "2027. Establish a global minimum carbon price of €50/tonne by 2028, rising annually. Hold "
    "fossil fuel companies legally accountable for documented disinformation. Fund the just "
    "transition at $100 billion per year.",
    styles['Doctrine']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 13 — THE DOCTRINE: CONSOLIDATED PRESCRIPTIONS
# =========================================================================
story.append(Paragraph(
    "Chapter 13: The Doctrine — Consolidated Prescriptions", styles['ChapterHead']))

story.append(Paragraph(
    "This chapter consolidates all doctrine prescriptions into a single, actionable framework "
    "organized by timeline. Each prescription is anchored in the evidence presented in preceding "
    "chapters and assigned to a specific deadline. These are not aspirations. These are "
    "requirements for planetary survival.",
    styles['Body']))

story.append(Paragraph("13.1 Immediate Actions (2026–2028)", styles['SectionHead']))

immediate_data = [
    [Paragraph("<b>#</b>", styles['TableCell']),
     Paragraph("<b>Prescription</b>", styles['TableCell']),
     Paragraph("<b>Domain</b>", styles['TableCell'])],
    [Paragraph("1", styles['TableCell']),
     Paragraph("Replace analysis with action across all institutions", styles['TableCell']),
     Paragraph("Governance", styles['TableCell'])],
    [Paragraph("2", styles['TableCell']),
     Paragraph("Accept planetary emergency as the operating context", styles['TableCell']),
     Paragraph("All", styles['TableCell'])],
    [Paragraph("3a", styles['TableCell']),
     Paragraph("Remove all fossil fuel subsidies", styles['TableCell']),
     Paragraph("Energy/Economics", styles['TableCell'])],
    [Paragraph("4a", styles['TableCell']),
     Paragraph("Mandate energy reporting for AI development", styles['TableCell']),
     Paragraph("Digital", styles['TableCell'])],
    [Paragraph("10a", styles['TableCell']),
     Paragraph("Richest 1% reduce emissions below 5t CO₂/year", styles['TableCell']),
     Paragraph("Justice", styles['TableCell'])],
    [Paragraph("12a", styles['TableCell']),
     Paragraph("Enact binding climate legislation in all nations", styles['TableCell']),
     Paragraph("Governance", styles['TableCell'])],
    [Paragraph("12b", styles['TableCell']),
     Paragraph("Establish global minimum carbon price €50/tonne", styles['TableCell']),
     Paragraph("Economics", styles['TableCell'])],
]
t = Table(immediate_data, colWidths=[30, 290, 80])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT2),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('BACKGROUND', (0, 1), (-1, -1), BG_LIGHT),
    ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(t)
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("13.2 Near-Term Actions (2028–2035)", styles['SectionHead']))

near_data = [
    [Paragraph("<b>#</b>", styles['TableCell']),
     Paragraph("<b>Prescription</b>", styles['TableCell']),
     Paragraph("<b>Domain</b>", styles['TableCell'])],
    [Paragraph("3b", styles['TableCell']),
     Paragraph("Complete coal phase-out globally", styles['TableCell']),
     Paragraph("Energy", styles['TableCell'])],
    [Paragraph("3c", styles['TableCell']),
     Paragraph("Achieve 80% clean electricity globally", styles['TableCell']),
     Paragraph("Energy", styles['TableCell'])],
    [Paragraph("4b", styles['TableCell']),
     Paragraph("100% renewable-powered data centers", styles['TableCell']),
     Paragraph("Digital", styles['TableCell'])],
    [Paragraph("5a", styles['TableCell']),
     Paragraph("Eliminate 50% of food waste", styles['TableCell']),
     Paragraph("Food", styles['TableCell'])],
    [Paragraph("5b", styles['TableCell']),
     Paragraph("30% agricultural land regenerative", styles['TableCell']),
     Paragraph("Food", styles['TableCell'])],
    [Paragraph("6", styles['TableCell']),
     Paragraph("30% of land and ocean protected (30x30)", styles['TableCell']),
     Paragraph("Ecosystems", styles['TableCell'])],
    [Paragraph("6a", styles['TableCell']),
     Paragraph("Zero deforestation globally", styles['TableCell']),
     Paragraph("Ecosystems", styles['TableCell'])],
    [Paragraph("7", styles['TableCell']),
     Paragraph("Carbon price minimum €100/tonne globally", styles['TableCell']),
     Paragraph("Economics", styles['TableCell'])],
    [Paragraph("10b", styles['TableCell']),
     Paragraph("Loss and Damage Fund at $100B/year", styles['TableCell']),
     Paragraph("Justice", styles['TableCell'])],
]
t = Table(near_data, colWidths=[30, 290, 80])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('BACKGROUND', (0, 1), (-1, -1), BG_LIGHT),
    ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(t)
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("13.3 Medium-Term Actions (2035–2050)", styles['SectionHead']))

medium_data = [
    [Paragraph("<b>#</b>", styles['TableCell']),
     Paragraph("<b>Prescription</b>", styles['TableCell']),
     Paragraph("<b>Domain</b>", styles['TableCell'])],
    [Paragraph("3d", styles['TableCell']),
     Paragraph("Complete oil phase-out for energy and transport", styles['TableCell']),
     Paragraph("Energy", styles['TableCell'])],
    [Paragraph("3e", styles['TableCell']),
     Paragraph("Achieve global net zero emissions", styles['TableCell']),
     Paragraph("Energy", styles['TableCell'])],
    [Paragraph("5c", styles['TableCell']),
     Paragraph("Reduce global meat consumption by 50%", styles['TableCell']),
     Paragraph("Food", styles['TableCell'])],
    [Paragraph("7b", styles['TableCell']),
     Paragraph("Carbon price minimum €200–250/tonne", styles['TableCell']),
     Paragraph("Economics", styles['TableCell'])],
    [Paragraph("9", styles['TableCell']),
     Paragraph("Replace GDP with wellbeing metrics globally", styles['TableCell']),
     Paragraph("Economics", styles['TableCell'])],
    [Paragraph("11a", styles['TableCell']),
     Paragraph("Scale DAC to 1 Gt CO₂/year", styles['TableCell']),
     Paragraph("Technology", styles['TableCell'])],
    [Paragraph("11b", styles['TableCell']),
     Paragraph("Decarbonize heavy industry via green hydrogen", styles['TableCell']),
     Paragraph("Technology", styles['TableCell'])],
]
t = Table(medium_data, colWidths=[30, 290, 80])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT3),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('BACKGROUND', (0, 1), (-1, -1), BG_LIGHT),
    ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(t)
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph(
    "The 9 Principle binds all prescriptions: <b>do not do anything unnecessary</b>. Every "
    "unnecessary action has a cost. Every unnecessary delay has a consequence. The doctrine demands "
    "that we act with the precision of a master — no wasted movement, no wasted time, no wasted "
    "resources.",
    styles['Body']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 14 — CONCLUSION: THE CHOICE
# =========================================================================
story.append(Paragraph("Chapter 14: Conclusion — The Choice", styles['ChapterHead']))

story.append(Paragraph(
    "This doctrine does not end with hope, because hope is passive. It ends with a choice.",
    styles['Body']))

story.append(Paragraph(
    "The science is unambiguous. The technology exists. The economics are favorable. The moral "
    "imperative is absolute. There is no credible scenario in which inaction is the rational "
    "choice. The only remaining variable is <b>will</b> — the collective decision of 8 billion "
    "people and their governments to act.",
    styles['Body']))

story.append(Paragraph("14.1 Two Futures", styles['SectionHead']))

story.append(Paragraph(
    "Under the doctrine pathway — aggressive decarbonization, ecosystem protection, justice-centered "
    "action, the 9 Principle applied globally — warming can be limited to 1.5–2.0°C. This is a "
    "world of adaptation, managed transition, and recoverable challenges. Food systems transform. "
    "Energy becomes clean. Cities become livable. Nature regenerates. It is not utopia — it is "
    "survival with dignity.",
    styles['Body']))

story.append(Paragraph(
    "Under the inaction pathway — continued fossil fuel dependence, growing emissions, ecosystem "
    "collapse, justice denied — warming reaches 3–4°C by 2100. This is a world of cascading "
    "tipping points, mass migration, food system failure, conflict over resources, and the "
    "permanent loss of ecosystems that took millions of years to evolve. This is not a prediction "
    "— it is the arithmetic consequence of current trajectories.",
    styles['Body']))

futures_data = [
    [Paragraph("<b>Domain</b>", styles['TableCell']),
     Paragraph("<b>Doctrine Pathway (1.5–2°C)</b>", styles['TableCell']),
     Paragraph("<b>Inaction Pathway (3–4°C)</b>", styles['TableCell'])],
    [Paragraph("Sea level", styles['TableCell']),
     Paragraph("+0.3–0.6 m by 2100", styles['TableCell']),
     Paragraph("+1.0–1.8 m by 2100", styles['TableCell'])],
    [Paragraph("Coral reefs", styles['TableCell']),
     Paragraph("70–90% loss", styles['TableCell']),
     Paragraph(">99% loss", styles['TableCell'])],
    [Paragraph("Arctic ice", styles['TableCell']),
     Paragraph("Occasional ice-free summers", styles['TableCell']),
     Paragraph("Year-round ice-free", styles['TableCell'])],
    [Paragraph("Food security", styles['TableCell']),
     Paragraph("Managed transition, <500M at risk", styles['TableCell']),
     Paragraph("System failure, >2B at risk", styles['TableCell'])],
    [Paragraph("Displacement", styles['TableCell']),
     Paragraph("~200M climate migrants", styles['TableCell']),
     Paragraph(">1B climate migrants", styles['TableCell'])],
    [Paragraph("Biodiversity", styles['TableCell']),
     Paragraph("20–30% species at risk", styles['TableCell']),
     Paragraph("50–70% species at risk", styles['TableCell'])],
    [Paragraph("Economy", styles['TableCell']),
     Paragraph("Managed transition costs", styles['TableCell']),
     Paragraph("$23T annual damages by 2100", styles['TableCell'])],
]
t = Table(futures_data, colWidths=[80, 160, 160])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('BACKGROUND', (1, 1), (1, -1), HexColor('#e8f5e9')),
    ('BACKGROUND', (2, 1), (2, -1), HexColor('#fce4ec')),
    ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(t)
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "<i>Table 14.1: Two futures — doctrine pathway vs. inaction pathway (IPCC, 2023)</i>",
    styles['FootNote']))
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("14.2 The 9 Principle as a Way of Life", styles['SectionHead']))

story.append(Paragraph(
    "Musashi wrote the Book of Five Rings as a dying man, distilling a lifetime of combat into "
    "principles. The 9 Principle — <i>Do not do anything unnecessary</i> — is not just a strategy "
    "for the sword. It is a strategy for civilization. Every unnecessary action weakens us. Every "
    "necessary action strengthens us. The climate crisis is, at its core, a crisis of unnecessary "
    "action at planetary scale.",
    styles['Body']))

story.append(Paragraph(
    "The Zokura Foundation exists to build a Good Life for all living things. A good life requires "
    "a habitable planet. This doctrine is our contribution: not another analysis, not another "
    "warning, but a prescriptive framework for action — clear, direct, and non-negotiable.",
    styles['Body']))

story.append(Paragraph("14.3 The Choice", styles['SectionHead']))

story.append(Paragraph(
    "Every generation faces defining choices. This generation's choice is whether to preserve "
    "or destroy the planetary systems that sustain life. The evidence is clear. The tools exist. "
    "The path is known. What remains is the decision to walk it.",
    styles['Body']))

story.append(Paragraph(
    "This is not a distant crisis. This is not someone else's problem. This is the defining "
    "challenge of every person alive today. The choice is simple, even if the execution is hard:",
    styles['Body']))

story.append(Paragraph(
    "<b>Act now, with precision, with purpose, with the discipline of a master swordsman who "
    "does not waste a single movement — or watch the only home we have become uninhabitable.</b>",
    styles['Body']))

story.append(Spacer(1, 1*cm))
story.append(HRFlowable(width="30%", thickness=0.5, color=BORDER))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph(
    "<i>\"Do not do anything unnecessary.\"</i>",
    styles['Epigraph']))
story.append(Paragraph(
    "<i>— Miyamoto Musashi</i>",
    styles['Epigraph']))
story.append(Spacer(1, 1*cm))
story.append(Paragraph("Rakkaus ja Totuus. Aina.", styles['Signature']))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("Miika Riikonen &amp; Kodo Zokura", styles['Signature']))
story.append(Paragraph("Zokura Foundation, 2026", styles['Signature']))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("太極", styles['Signature']))

story.append(PageBreak())

# =========================================================================
# REFERENCES
# =========================================================================
story.append(Paragraph("References", styles['ChapterHead']))

refs = [
    "Armstrong McKay, D.I., et al. (2022). Exceeding 1.5°C global warming could trigger multiple climate tipping points. <i>Science</i>, 377(6611).",
    "Bereiter, B., et al. (2015). Revision of the EPICA Dome C CO₂ record from 800 to 600 kyr before present. <i>Geophysical Research Letters</i>, 42(2).",
    "Cambridge Centre for Alternative Finance (2024). Cambridge Bitcoin Electricity Consumption Index. University of Cambridge.",
    "Carbon Tracker Initiative (2023). Unburnable Carbon: Are the World's Financial Markets Carrying a Carbon Bubble?",
    "Clement, V., et al. (2021). Groundswell Part 2: Acting on Internal Climate Migration. World Bank.",
    "Costanza, R., et al. (2014). Changes in the global value of ecosystem services. <i>Global Environmental Change</i>, 26, 152–158.",
    "EPA (2023). Social Cost of Carbon, Methane, and Nitrous Oxide. U.S. Environmental Protection Agency.",
    "FAO (2011). Global Food Losses and Food Waste. Food and Agriculture Organization of the United Nations.",
    "FAO (2013). Tackling Climate Change Through Livestock. Food and Agriculture Organization of the United Nations.",
    "FAO (2022). The State of World Fisheries and Aquaculture 2022. Food and Agriculture Organization.",
    "Freitag, C., et al. (2021). The real climate and transformative impact of ICT. <i>Patterns</i>, 2(9), 100340.",
    "Friedlingstein, P., et al. (2022). Global Carbon Budget 2022. <i>Earth System Science Data</i>, 14, 4811–4900.",
    "Gattuso, J.-P., et al. (2015). Contrasting futures for ocean and society from different anthropogenic CO₂ emissions scenarios. <i>Science</i>, 349(6243).",
    "Global Forest Watch (2023). Global Forest Review. World Resources Institute.",
    "Griscom, B.W., et al. (2017). Natural climate solutions. <i>Proceedings of the National Academy of Sciences</i>, 114(44), 11645–11650.",
    "IEA (2020). World Energy Outlook 2020. International Energy Agency.",
    "IEA (2023). World Energy Investment 2023. International Energy Agency.",
    "IEA (2024). Electricity 2024: Analysis and forecast to 2026. International Energy Agency.",
    "ILO (2018). World Employment and Social Outlook 2018: Greening with Jobs. International Labour Organization.",
    "IMF (2023). Fossil Fuel Subsidies Data: 2023 Update. International Monetary Fund.",
    "IPBES (2019). Global Assessment Report on Biodiversity and Ecosystem Services. Intergovernmental Science-Policy Platform.",
    "IPCC (2014). Climate Change 2014: Mitigation of Climate Change. Intergovernmental Panel on Climate Change.",
    "IPCC (2023). AR6 Synthesis Report: Climate Change 2023. Intergovernmental Panel on Climate Change.",
    "IRENA (2023). Renewable Power Generation Costs in 2022. International Renewable Energy Agency.",
    "Kulp, S.A. & Strauss, B.H. (2019). New elevation data triple estimates of global vulnerability to sea-level rise. <i>Nature Communications</i>, 10, 4844.",
    "Lal, R. (2020). Soil science beyond COVID-19. <i>Journal of Soil and Water Conservation</i>, 75(4), 79A–81A.",
    "Lazard (2023). Lazard's Levelized Cost of Energy Analysis — Version 16.0.",
    "Lovejoy, T.E. & Nobre, C. (2018). Amazon tipping point. <i>Science Advances</i>, 4(2), eaat2340.",
    "Luccioni, A.S., et al. (2023). Estimating the Carbon Footprint of BLOOM. <i>arXiv preprint</i> arXiv:2211.02001.",
    "Lynas, M., et al. (2021). Greater than 99% consensus on human caused climate change. <i>Environmental Research Letters</i>, 16(11).",
    "Markandya, A. & González-Eguino, M. (2019). Integrated assessment for identifying climate finance needs for loss and damage. <i>Climatic Change</i>, 152, 273–287.",
    "McGlade, C. & Ekins, P. (2015). The geographical distribution of fossil fuels unused when limiting global warming to 2°C. <i>Nature</i>, 517, 187–190.",
    "NewClimate Institute (2023). Corporate Climate Responsibility Monitor 2023.",
    "Oxfam (2021). Carbon Inequality in 2030. Oxfam International.",
    "Pimm, S.L., et al. (2014). The biodiversity of species and their rates of extinction. <i>Science</i>, 344(6187), 1246752.",
    "Poore, J. & Nemecek, T. (2018). Reducing food's environmental impacts through producers and consumers. <i>Science</i>, 360(6392), 987–992.",
    "Radicati Group (2023). Email Statistics Report, 2023–2027.",
    "Rennert, K., et al. (2022). Comprehensive evidence implies a higher social cost of CO₂. <i>Nature</i>, 610, 687–692.",
    "Richardson, K., et al. (2023). Earth beyond six of nine planetary boundaries. <i>Science Advances</i>, 9(37).",
    "Ritchie, H. & Roser, M. (2020). CO₂ and Greenhouse Gas Emissions. Our World in Data.",
    "Supran, G., et al. (2023). Assessing ExxonMobil's global warming projections. <i>Science</i>, 379(6628).",
    "Thiery, W., et al. (2021). Intergenerational inequities in exposure to climate extremes. <i>Science</i>, 374(6564), 158–160.",
    "UNEP (2023). Emissions Gap Report 2023. United Nations Environment Programme.",
    "UNFCCC (2023). Nationally Determined Contributions Registry. UN Framework Convention on Climate Change.",
    "van Klink, R., et al. (2020). Meta-analysis reveals declines in terrestrial but increases in freshwater insect abundances. <i>Science</i>, 368(6489), 417–420.",
    "Willett, W., et al. (2019). Food in the Anthropocene: the EAT–Lancet Commission. <i>The Lancet</i>, 393(10170), 447–492.",
    "WWF (2022). Living Planet Report 2022. World Wildlife Fund.",
    "Wynes, S. & Nicholas, K.A. (2017). The climate mitigation gap: education and government recommendations miss the most effective individual actions. <i>Environmental Research Letters</i>, 12(7).",
]

for ref in refs:
    story.append(Paragraph(ref, styles['RefStyle']))

# =========================================================================
# BUILD PDF
# =========================================================================
doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(f"PDF generated: {output_path}")
