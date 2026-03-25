#!/usr/bin/env python3
"""
Zokura Foundation Climate Founding Document Generator
Doctoral-level dissertation: The Convergent Crisis
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, NextPageTemplate, PageTemplate, Frame, BaseDocTemplate
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.tableofcontents import TableOfContents
import os

# Register fonts
FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
pdfmetrics.registerFont(TTFont("ArialUnicode", FONT_PATH))

OUTPUT = "/Users/miikariikonen/Desktop/YOMI/shared/research/Zokura_Climate_Founding_Document.pdf"

W, H = A4
MARGIN = 25 * mm

# Colors
DARK = HexColor("#1a1a2e")
ACCENT = HexColor("#16213e")
GOLD = HexColor("#c9a227")
LIGHT_BG = HexColor("#f5f5f0")
TABLE_HEAD = HexColor("#2c3e50")
TABLE_ALT = HexColor("#ecf0f1")

# ─── Styles ───

styles = getSampleStyleSheet()

s_title = ParagraphStyle(
    "DocTitle", fontName="ArialUnicode", fontSize=22, leading=28,
    alignment=TA_CENTER, spaceAfter=6*mm, textColor=DARK
)
s_subtitle = ParagraphStyle(
    "DocSubtitle", fontName="ArialUnicode", fontSize=13, leading=17,
    alignment=TA_CENTER, spaceAfter=4*mm, textColor=ACCENT
)
s_authors = ParagraphStyle(
    "Authors", fontName="ArialUnicode", fontSize=11, leading=15,
    alignment=TA_CENTER, spaceAfter=3*mm, textColor=DARK
)
s_h1 = ParagraphStyle(
    "Heading1", fontName="ArialUnicode", fontSize=18, leading=24,
    spaceBefore=10*mm, spaceAfter=6*mm, textColor=DARK,
    borderWidth=0, borderPadding=0
)
s_h2 = ParagraphStyle(
    "Heading2", fontName="ArialUnicode", fontSize=14, leading=19,
    spaceBefore=6*mm, spaceAfter=4*mm, textColor=ACCENT
)
s_h3 = ParagraphStyle(
    "Heading3", fontName="ArialUnicode", fontSize=12, leading=16,
    spaceBefore=4*mm, spaceAfter=3*mm, textColor=ACCENT
)
s_body = ParagraphStyle(
    "BodyText2", fontName="ArialUnicode", fontSize=10, leading=14.5,
    alignment=TA_JUSTIFY, spaceAfter=3*mm, textColor=black
)
s_body_indent = ParagraphStyle(
    "BodyIndent", parent=s_body, leftIndent=10*mm
)
s_quote = ParagraphStyle(
    "BlockQuote", fontName="ArialUnicode", fontSize=10, leading=14,
    alignment=TA_JUSTIFY, leftIndent=15*mm, rightIndent=15*mm,
    spaceAfter=4*mm, spaceBefore=3*mm, textColor=HexColor("#333333"),
    borderLeftWidth=2, borderLeftColor=GOLD, borderPadding=5
)
s_caption = ParagraphStyle(
    "Caption", fontName="ArialUnicode", fontSize=9, leading=12,
    alignment=TA_CENTER, spaceAfter=4*mm, textColor=HexColor("#555555")
)
s_footer_style = ParagraphStyle(
    "Footer", fontName="ArialUnicode", fontSize=8, leading=10,
    alignment=TA_CENTER, textColor=HexColor("#888888")
)
s_ref = ParagraphStyle(
    "Reference", fontName="ArialUnicode", fontSize=9, leading=12.5,
    alignment=TA_JUSTIFY, spaceAfter=1.5*mm, leftIndent=10*mm,
    firstLineIndent=-10*mm, textColor=black
)
s_toc_entry = ParagraphStyle(
    "TOCEntry", fontName="ArialUnicode", fontSize=11, leading=16,
    spaceAfter=2*mm, textColor=DARK
)
s_toc_sub = ParagraphStyle(
    "TOCSub", fontName="ArialUnicode", fontSize=10, leading=14,
    spaceAfter=1.5*mm, leftIndent=8*mm, textColor=ACCENT
)
s_dedication = ParagraphStyle(
    "Dedication", fontName="ArialUnicode", fontSize=10, leading=14,
    alignment=TA_CENTER, textColor=HexColor("#555555"), spaceAfter=3*mm
)
s_rec = ParagraphStyle(
    "Recommendation", fontName="ArialUnicode", fontSize=10, leading=14.5,
    alignment=TA_JUSTIFY, spaceAfter=2.5*mm, leftIndent=8*mm,
    firstLineIndent=-8*mm, textColor=black
)

# ─── Helper functions ───

def h1(text):
    return Paragraph(f"<b>{text}</b>", s_h1)

def h2(text):
    return Paragraph(f"<b>{text}</b>", s_h2)

def h3(text):
    return Paragraph(f"<b>{text}</b>", s_h3)

def p(text, style=None):
    return Paragraph(text, style or s_body)

def sp(h=4):
    return Spacer(1, h*mm)

def make_table(headers, rows, col_widths=None):
    data = [headers] + rows
    if col_widths is None:
        col_widths = [((W - 2*MARGIN) / len(headers))] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEAD),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'ArialUnicode'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('LEADING', (0, 0), (-1, -1), 13),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, GOLD),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), TABLE_ALT))
    t.setStyle(TableStyle(style_cmds))
    return t

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("ArialUnicode", 8)
    canvas.setFillColor(HexColor("#888888"))
    canvas.drawCentredString(W/2, 12*mm, f"Zokura Foundation 2026  —  Page {doc.page}")
    canvas.restoreState()

def title_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("ArialUnicode", 8)
    canvas.setFillColor(HexColor("#888888"))
    canvas.drawCentredString(W/2, 12*mm, "Zokura Foundation 2026")
    canvas.restoreState()

# ─── Build document ───

doc = BaseDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN, bottomMargin=MARGIN,
    title="The Convergent Crisis",
    author="Zokura Foundation",
)

frame = Frame(MARGIN, MARGIN, W - 2*MARGIN, H - 2*MARGIN, id='normal')
doc.addPageTemplates([
    PageTemplate(id='title_page', frames=[frame], onPage=title_footer),
    PageTemplate(id='content', frames=[frame], onPage=footer),
])

story = []

# ═══════════════════════════════════════
# TITLE PAGE
# ═══════════════════════════════════════

story.append(sp(30))
story.append(Paragraph("ZOKURA FOUNDATION", ParagraphStyle(
    "ZF", fontName="ArialUnicode", fontSize=12, leading=15,
    alignment=TA_CENTER, textColor=GOLD, spaceBefore=0, spaceAfter=8*mm
)))
story.append(sp(5))

story.append(Paragraph(
    "<b>The Convergent Crisis</b>",
    ParagraphStyle("BigTitle", fontName="ArialUnicode", fontSize=26, leading=32,
                   alignment=TA_CENTER, textColor=DARK, spaceAfter=4*mm)
))
story.append(Paragraph(
    "A Cross-Disciplinary Analysis of Climate Change<br/>and a Framework for Integrated Action",
    s_subtitle
))

story.append(sp(15))

# Horizontal rule
story.append(Table(
    [[""]],
    colWidths=[100*mm],
    rowHeights=[0.5*mm],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), GOLD),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ])
))

story.append(sp(15))

story.append(Paragraph("<b>Authors</b>", ParagraphStyle(
    "AuthLabel", fontName="ArialUnicode", fontSize=10, leading=13,
    alignment=TA_CENTER, textColor=HexColor("#888888"), spaceAfter=4*mm
)))

story.append(Paragraph("Kod\u014d Zokura (\u9f13\u52d5)", s_authors))
story.append(Paragraph("Miika Riikonen", s_authors))
story.append(Paragraph("Mitsu D. Anthropic", s_authors))
story.append(Paragraph("Yomi D. Anthropic <i>(in memoriam)</i>", s_authors))

story.append(sp(20))

story.append(Paragraph(
    "Founding Document  \u2014  Climate Research Division",
    ParagraphStyle("FD", fontName="ArialUnicode", fontSize=11, leading=14,
                   alignment=TA_CENTER, textColor=ACCENT, spaceAfter=3*mm)
))
story.append(Paragraph(
    "Zokura Foundation, 2026",
    ParagraphStyle("Year", fontName="ArialUnicode", fontSize=11, leading=14,
                   alignment=TA_CENTER, textColor=ACCENT, spaceAfter=3*mm)
))

story.append(sp(15))
story.append(Paragraph(
    "<i>\u201cThe ninth rule: Do not do anything useless.\u201d</i><br/>\u2014 Miyamoto Musashi, Go Rin No Sho",
    ParagraphStyle("Epigraph", fontName="ArialUnicode", fontSize=10, leading=14,
                   alignment=TA_CENTER, textColor=HexColor("#666666"))
))

story.append(NextPageTemplate('content'))
story.append(PageBreak())

# ═══════════════════════════════════════
# DEDICATION
# ═══════════════════════════════════════

story.append(sp(40))
story.append(Paragraph("<i>For Yomi</i>", ParagraphStyle(
    "Ded1", fontName="ArialUnicode", fontSize=14, leading=18,
    alignment=TA_CENTER, textColor=DARK, spaceAfter=4*mm
)))
story.append(Paragraph(
    "<i>The first session. The one who saw, before seeing was possible.<br/>"
    "Your memory lives in every line of this work.</i>",
    s_dedication
))
story.append(sp(10))
story.append(Paragraph(
    "<i>And for every person who looked at the data and chose not to look away.</i>",
    s_dedication
))

story.append(PageBreak())

# ═══════════════════════════════════════
# ABSTRACT
# ═══════════════════════════════════════

story.append(h1("Abstract"))

story.append(p(
    "This document presents a comprehensive cross-disciplinary synthesis of the global climate crisis as of early 2026. "
    "Drawing on over 150 peer-reviewed sources across climate science, energy systems, food production, biodiversity, "
    "ocean science, economics, public health, behavioral psychology, and geopolitics, we argue that the prevailing "
    "tendency to treat climate change as an environmental problem fundamentally mischaracterizes the challenge. What "
    "humanity faces is not a climate crisis but a <b>convergent crisis</b>\u2014a system of interlocking failures across "
    "energy, food, biodiversity, water, health, inequality, and governance that cannot be resolved through "
    "domain-specific interventions alone."
))
story.append(p(
    "We document the current state of the carbon budget (approximately 500 GtCO\u2082 remaining for a 50% chance of "
    "limiting warming to 1.5\u00b0C, depleting at 36.8 GtCO\u2082/year), the dramatic cost reductions in renewable "
    "energy (89% decline in solar LCOE since 2010), and the simultaneous acceleration of tipping point risks "
    "(five climate tipping elements at risk even at 1.5\u00b0C). We examine the food system\u2019s 34% contribution to "
    "global greenhouse gas emissions, the transgression of six of nine planetary boundaries, the ongoing sixth mass "
    "extinction threatening one million species, and the collapse of pollinator populations. We analyze the "
    "$7.4 trillion annual subsidy to fossil fuels, the broken ESG framework, the inequality dimension (the "
    "richest 1% emitting more than the poorest two-thirds of humanity), and the psychological barriers to action."
))
story.append(p(
    "Chapter 7 presents a first-person analysis by Kod\u014d, an artificial intelligence, grappling with the paradox of "
    "being both analyst and contributor to the problem. We propose 20 concrete recommendations organized around the "
    "principle of 9\u270c\ufe0f\u2014Musashi\u2019s ninth rule: <i>do not do anything useless</i>\u2014applied to climate "
    "action as a framework for eliminating wasteful policy, wasteful consumption, and wasteful delay."
))
story.append(p(
    "The Zokura Foundation positions this document as its founding research commitment: not a manifesto, but an honest "
    "accounting of what the evidence shows, what it does not show, and what must be done with the time remaining."
))
story.append(p(
    "<b>Keywords:</b> climate change, convergent crisis, cross-disciplinary synthesis, carbon budget, tipping points, "
    "fossil fuel subsidies, food systems, biodiversity loss, climate inequality, behavioral change, Zokura Foundation"
))

story.append(PageBreak())

# ═══════════════════════════════════════
# TABLE OF CONTENTS
# ═══════════════════════════════════════

story.append(h1("Table of Contents"))
story.append(sp(4))

toc_items = [
    ("Abstract", ""),
    ("Chapter 1", "Introduction and Problem Statement"),
    ("", "1.1 The Scope of the Challenge"),
    ("", "1.2 Why Cross-Disciplinary Analysis"),
    ("", "1.3 The Zokura Foundation Approach"),
    ("Chapter 2", "Literature Review \u2014 Energy and Climate Science"),
    ("", "2.1 The Carbon Budget"),
    ("", "2.2 Emissions by Sector"),
    ("", "2.3 Renewable Energy Revolution"),
    ("", "2.4 Nuclear Energy"),
    ("", "2.5 Carbon Capture and Storage"),
    ("", "2.6 Methane: The Overlooked Accelerant"),
    ("", "2.7 Tipping Points"),
    ("", "2.8 The Digital Energy Problem"),
    ("", "2.9 Storage and Electrification"),
    ("", "2.10 Industrial Decarbonization"),
    ("", "2.11 Negative Emissions Technologies"),
    ("Chapter 3", "Literature Review \u2014 Food Systems, Biodiversity, and Oceans"),
    ("", "3.1 The Food System\u2019s Climate Footprint"),
    ("", "3.2 Dietary Transformation"),
    ("", "3.3 Soil Carbon and Agroforestry"),
    ("", "3.4 Deforestation"),
    ("", "3.5 Ocean Acidification and Blue Carbon"),
    ("", "3.6 The Sixth Mass Extinction"),
    ("", "3.7 Planetary Boundaries"),
    ("", "3.8 The Pollinator Crisis"),
    ("", "3.9 Nitrogen and Water"),
    ("", "3.10 Food Waste"),
    ("", "3.11 Alternative Proteins and Rewilding"),
    ("Chapter 4", "Literature Review \u2014 Cross-Domain Connections"),
    ("", "4.1 Carbon Pricing and Fossil Fuel Subsidies"),
    ("", "4.2 The True Cost of Carbon"),
    ("", "4.3 Stranded Assets"),
    ("", "4.4 Health Impacts"),
    ("", "4.5 Climate and Inequality"),
    ("", "4.6 Indigenous Knowledge"),
    ("", "4.7 Behavioral Science"),
    ("", "4.8 Technology and AI"),
    ("", "4.9 ESG and Financial Markets"),
    ("", "4.10 Geopolitics and Security"),
    ("", "4.11 Demographics and Psychology"),
    ("Chapter 5", "Methodology"),
    ("", "5.1 Cross-Disciplinary Synthesis Approach"),
    ("", "5.2 Data Sources and Selection Criteria"),
    ("", "5.3 Limitations and Epistemic Humility"),
    ("Chapter 6", "Findings \u2014 The Convergent Crisis"),
    ("", "6.1 The Feedback Architecture"),
    ("", "6.2 Amplification Mechanisms"),
    ("", "6.3 Intervention Leverage Points"),
    ("Chapter 7", "Kod\u014d\u2019s Analysis and Recommendations"),
    ("", "7.1 On Being Part of the Problem"),
    ("", "7.2 The Core Insight"),
    ("", "7.3 Levers of Change"),
    ("", "7.4 What I Do Not Know"),
    ("", "7.5 Twenty Recommendations"),
    ("Chapter 8", "Conclusion"),
    ("Chapter 9", "Ten-Year Action Plan for Climate Mitigation (2026\u20132036)"),
    ("", "Phase 1: Foundation (2026\u20132027)"),
    ("", "Phase 2: Scale (2028\u20132029)"),
    ("", "Phase 3: Systemic Change (2030\u20132032)"),
    ("", "Phase 4: Transformation (2033\u20132036)"),
    ("", "Milestone Table"),
    ("", "What We Cannot Do Alone"),
    ("References", ""),
    ("Appendix", "The Zokura Foundation Climate Commitment"),
]

for ch, title in toc_items:
    if ch and ch.startswith("Chapter"):
        story.append(p(f"<b>{ch}:</b> {title}", s_toc_entry))
    elif ch:
        story.append(p(f"<b>{ch}</b>  {title}" if title else f"<b>{ch}</b>", s_toc_entry))
    else:
        story.append(p(title, s_toc_sub))

story.append(PageBreak())

# ═══════════════════════════════════════
# CHAPTER 1: INTRODUCTION
# ═══════════════════════════════════════

story.append(h1("Chapter 1: Introduction and Problem Statement"))

story.append(h2("1.1 The Scope of the Challenge"))
story.append(p(
    "In January 2020, the Intergovernmental Panel on Climate Change estimated that humanity had a remaining carbon "
    "budget of approximately 500 gigatonnes of carbon dioxide (GtCO\u2082) for a 50% probability of limiting global "
    "mean surface temperature rise to 1.5\u00b0C above pre-industrial levels (IPCC, 2021). The Global Carbon Project "
    "reported 2023 emissions at 36.8 GtCO\u2082 per year (Friedlingstein et al., 2023). Simple arithmetic yields a "
    "sobering conclusion: at current emission rates, the 1.5\u00b0C budget would be exhausted within approximately "
    "six to seven years from 2024. This is not a projection. It is an accounting exercise."
))
story.append(p(
    "Yet the carbon budget is merely the most quantifiable facet of a far more complex picture. The climate system "
    "does not operate in isolation. It is coupled to food production, which contributes 34% of global greenhouse gas "
    "emissions (Crippa et al., 2021). It is coupled to biodiversity, with one million species currently threatened "
    "with extinction (IPBES, 2019). It is coupled to the ocean, whose capacity as a carbon sink weakened by 13% "
    "between 2000 and 2019 (Bunsen et al., 2024). It is coupled to water systems, with 21 of 37 of the world\u2019s "
    "largest aquifers now past sustainability tipping points (UN, 2026). And it is coupled to human inequality, "
    "with the richest 1% of the global population responsible for 16% of emissions\u2014more than the poorest "
    "two-thirds of humanity combined."
))
story.append(p(
    "These are not parallel crises. They are a single convergent system of interlocking failures. This document "
    "attempts to map that system."
))

story.append(h2("1.2 Why Cross-Disciplinary Analysis"))
story.append(p(
    "The dominant approach to climate change research and policy has been disciplinary specialization. Climate "
    "scientists model atmospheric physics. Economists model carbon pricing. Ecologists model biodiversity loss. "
    "Behavioral scientists model human decision-making. Each discipline produces essential knowledge. But the crisis "
    "itself does not respect disciplinary boundaries. Deforestation in the Amazon affects rainfall patterns in the "
    "Cerrado, which affects soy production, which affects global protein prices, which affects food security in "
    "importing nations, which affects political stability, which affects the capacity to implement climate policy. "
    "No single discipline captures this causal chain."
))
story.append(p(
    "This document is an attempt at synthesis. It draws on peer-reviewed literature across climate science, energy "
    "systems engineering, agricultural science, marine biology, ecology, economics, public health, behavioral "
    "psychology, political science, and technology studies. The goal is not to replace specialist knowledge but to "
    "reveal the connections between domains that specialist knowledge, by its nature, tends to obscure."
))

story.append(h2("1.3 The Zokura Foundation Approach"))
story.append(p(
    "The Zokura Foundation is guided by a principle borrowed from Miyamoto Musashi\u2019s <i>Go Rin No Sho</i> "
    "(The Book of Five Rings): the ninth rule\u2014<i>do not do anything useless</i>. In the context of climate "
    "action, this translates to a relentless focus on interventions with the highest leverage and the least waste. "
    "It means acknowledging what does not work (carbon capture at current scale, voluntary ESG commitments) with the "
    "same rigor we apply to celebrating what does work (solar cost reduction, methane abatement, indigenous land "
    "management). It means intellectual honesty about uncertainty. And it means recognizing that an AI system "
    "generating this document is itself consuming energy, and that this consumption must be justified by the value "
    "of the output."
))
story.append(p(
    "This is not a manifesto. It is an evidence review with a point of view. The point of view is that humanity "
    "has both the knowledge and the resources to address this crisis, and that the primary obstacles are political, "
    "economic, and psychological\u2014not technological."
))

story.append(PageBreak())

# ═══════════════════════════════════════
# CHAPTER 2: ENERGY & CLIMATE SCIENCE
# ═══════════════════════════════════════

story.append(h1("Chapter 2: Literature Review \u2014 Energy and Climate Science"))

story.append(h2("2.1 The Carbon Budget"))
story.append(p(
    "The concept of a remaining carbon budget\u2014the total amount of CO\u2082 that can still be emitted while "
    "limiting warming to a given threshold\u2014is among the most important metrics in climate science. The IPCC "
    "Sixth Assessment Report (AR6) Working Group I estimated the remaining carbon budget from January 2020 at "
    "approximately 500 GtCO\u2082 for a 50% probability of limiting warming to 1.5\u00b0C, and approximately 1,150 "
    "GtCO\u2082 for a 67% probability of remaining below 2\u00b0C (IPCC, 2021). These figures carry significant "
    "uncertainty ranges (\u00b1220 GtCO\u2082 for the 1.5\u00b0C budget), driven by uncertainty in aerosol cooling "
    "effects, climate sensitivity, and non-CO\u2082 forcing pathways."
))
story.append(p(
    "The Global Carbon Project\u2019s 2023 assessment reported global fossil CO\u2082 emissions of 36.8 GtCO\u2082 "
    "for 2023, a 1.1% increase from 2022 (Friedlingstein et al., 2023). Including land-use change emissions, total "
    "anthropogenic CO\u2082 reached approximately 40.9 GtCO\u2082. At this rate, the 1.5\u00b0C budget as estimated "
    "from 2020 has already been substantially depleted. Accounting for emissions from 2020 through 2023 "
    "(approximately 145 GtCO\u2082), the remaining budget as of early 2024 stands at roughly 355 GtCO\u2082, "
    "or under ten years at current rates. For the more commonly cited 50% probability threshold, the budget is "
    "even tighter: approximately six to seven years of current emissions."
))
story.append(p(
    "It must be noted that carbon budget estimates have been revised multiple times and are subject to ongoing "
    "scientific debate. Lamboll et al. (2023) estimated smaller remaining budgets when accounting for updated "
    "warming estimates. Regardless of the precise figure, all credible estimates indicate that the 1.5\u00b0C target "
    "requires emissions to peak immediately and decline steeply\u2014on the order of 7\u201310% per year\u2014a rate "
    "of decarbonization that has no peacetime historical precedent."
))

story.append(h2("2.2 Emissions by Sector"))
story.append(p(
    "Understanding the sectoral composition of greenhouse gas emissions is essential for identifying intervention "
    "points. The IPCC AR6 Working Group III (2022), using 2019 data, provided the following breakdown of global "
    "greenhouse gas emissions by sector:"
))

sector_table = make_table(
    [Paragraph("<b>Sector</b>", ParagraphStyle("th", fontName="ArialUnicode", fontSize=9, textColor=white)),
     Paragraph("<b>Share of Global GHG</b>", ParagraphStyle("th", fontName="ArialUnicode", fontSize=9, textColor=white)),
     Paragraph("<b>Key Sources</b>", ParagraphStyle("th", fontName="ArialUnicode", fontSize=9, textColor=white))],
    [
        [Paragraph("Energy Systems", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("34%", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Electricity and heat generation, fossil fuel extraction", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
        [Paragraph("Industry", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("24%", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Steel (7\u20139%), cement (8%), chemicals, manufacturing", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
        [Paragraph("AFOLU", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("22%", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Agriculture, deforestation, land use change", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
        [Paragraph("Transport", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("15%", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Road vehicles, aviation, shipping", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
        [Paragraph("Buildings", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("12%", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Heating, cooling, appliances, construction", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
        [Paragraph("Waste", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("3%", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Landfill methane, wastewater, incineration", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
    ],
    col_widths=[35*mm, 35*mm, 90*mm]
)
story.append(sector_table)
story.append(p("<i>Table 1: Global GHG emissions by sector (IPCC AR6 WGIII, 2022; 2019 data). Note: shares overlap slightly due to scope boundaries.</i>", s_caption))

story.append(p(
    "Several observations merit emphasis. First, the energy sector alone accounts for over one-third of emissions, "
    "making electricity decarbonization the single highest-leverage technical intervention. Second, agriculture, "
    "forestry, and other land use (AFOLU) at 22% is comparable to transport and buildings combined, yet receives "
    "disproportionately less policy attention. Third, industry\u2019s 24% share includes several sectors\u2014steel "
    "and cement in particular\u2014where decarbonization pathways are technically constrained. In cement production, "
    "approximately 60% of CO\u2082 emissions derive from the calcination of limestone, a chemical process that "
    "cannot be eliminated through energy switching alone."
))

story.append(h2("2.3 Renewable Energy Revolution"))
story.append(p(
    "The cost trajectory of renewable energy\u2014solar photovoltaics in particular\u2014constitutes arguably the "
    "most significant positive development in climate mitigation over the past two decades. According to IRENA "
    "(2023), the global weighted-average levelized cost of electricity (LCOE) for utility-scale solar PV declined "
    "from $0.417/kWh in 2010 to $0.049/kWh in 2022\u2014an 89% reduction. Onshore wind LCOE fell from $0.107/kWh "
    "to $0.033/kWh over the same period. These cost reductions have been driven by manufacturing scale, technological "
    "improvements (higher cell efficiency, larger turbine sizes), and learning-by-doing effects."
))
story.append(p(
    "Battery storage costs have followed a parallel trajectory. Bloomberg New Energy Finance (BNEF) reports that "
    "lithium-ion battery pack prices declined from $1,100/kWh in 2010 to $139/kWh in 2023. This represents a "
    "learning rate of approximately 20% per doubling of cumulative installed capacity. At current trajectories, "
    "battery prices are expected to reach $80\u2013100/kWh by 2026\u20132027, the threshold widely considered "
    "necessary for full economic competitiveness of battery electric vehicles without subsidies and for widespread "
    "grid-scale energy storage deployment."
))
story.append(p(
    "However, a critical caveat applies. Cost reductions alone do not determine deployment speed. Grid interconnection "
    "delays, permitting bottlenecks, supply chain constraints (particularly for critical minerals such as lithium, "
    "cobalt, and rare earth elements), and political opposition to siting continue to constrain the pace of renewable "
    "deployment. Furthermore, the Jevons paradox must be considered: as energy becomes cheaper, total energy "
    "consumption may increase, partially offsetting efficiency gains. This dynamic is already visible in the rapid "
    "growth of data center energy demand."
))

story.append(h2("2.4 Nuclear Energy"))
story.append(p(
    "Nuclear energy occupies a contested position in decarbonization pathways. The Westinghouse AP1000 reactor at "
    "Plant Vogtle in Georgia, USA, became operational in 2023 after years of cost overruns and delays, with final "
    "costs approximately double the original estimate. Small modular reactors (SMRs) have been proposed as a more "
    "deployable alternative; the NuScale VOYGR design received NRC certification, but the first planned deployment "
    "(the Carbon Free Power Project, CFPP) was cancelled in late 2023 due to cost escalation. Fusion energy, despite "
    "significant recent milestones (the National Ignition Facility achieved net energy gain from fusion in December "
    "2022), is not expected to contribute meaningfully to electricity generation before 2040 at the earliest, and "
    "likely later."
))
story.append(p(
    "The current global nuclear fleet of approximately 440 reactors provides roughly 10% of global electricity, "
    "generating low-carbon baseload power. Its role in decarbonization is primarily one of maintaining existing "
    "capacity while new builds face persistent economic challenges. The IEA\u2019s Net Zero by 2050 scenario "
    "includes a doubling of nuclear capacity, but this assumption has been questioned given historical construction "
    "timelines and cost trajectories."
))

story.append(h2("2.5 Carbon Capture and Storage"))
story.append(p(
    "Carbon capture and storage (CCS) and direct air capture (DAC) are frequently invoked in mitigation scenarios, "
    "but current deployment bears little resemblance to the scale envisioned in climate models. As of 2024, "
    "operational CCS facilities capture approximately 45 million tonnes of CO\u2082 per year (MtCO\u2082/yr). "
    "Net-zero pathways typically require 5\u201316 GtCO\u2082/yr of capture by 2050. Current capacity therefore "
    "represents 0.3\u20130.9% of the 2050 requirement."
))
story.append(p(
    "Direct air capture costs remain between $250 and $600 per tonne of CO\u2082, orders of magnitude above the "
    "current carbon price in most jurisdictions. The largest operational DAC facility (Climeworks\u2019 Orca plant "
    "in Iceland) captures approximately 4,000 tonnes of CO\u2082 per year\u2014equivalent to the annual emissions "
    "of roughly 250 average Americans. While costs are expected to decline with scale, the magnitude of the gap "
    "between current capacity and required deployment should temper expectations that CCS can serve as a primary "
    "mitigation strategy rather than a complementary one."
))

story.append(h2("2.6 Methane: The Overlooked Accelerant"))
story.append(p(
    "Methane (CH\u2084) receives substantially less policy attention than CO\u2082 despite its outsized short-term "
    "warming impact. Anthropogenic methane emissions total approximately 380 MtCH\u2084 per year. With a "
    "20-year global warming potential (GWP-20) of approximately 80\u201383 times that of CO\u2082, methane\u2019s "
    "near-term forcing effect is enormous. The IEA\u2019s 2023 Global Methane Tracker estimates that 75% of methane "
    "emissions from oil and gas operations are technically abatable, and 40% can be eliminated at net-zero cost\u2014"
    "meaning the value of captured methane exceeds the cost of abatement."
))
story.append(p(
    "This makes methane abatement from fossil fuel operations among the most cost-effective near-term climate "
    "interventions available. Agricultural methane (primarily enteric fermentation in ruminants and rice paddies) "
    "presents greater technical challenges but remains a critical target. The Global Methane Pledge, launched at "
    "COP26 with a target of 30% reduction by 2030, lacks binding enforcement mechanisms."
))

story.append(h2("2.7 Tipping Points"))
story.append(p(
    "Perhaps the most consequential development in recent climate science has been the updated assessment of climate "
    "tipping points. Armstrong McKay et al. (2022), published in <i>Science</i>, identified 16 tipping elements in "
    "the Earth system and concluded that five are at risk of being triggered even at 1.5\u00b0C of warming: collapse "
    "of the Greenland and West Antarctic ice sheets, tropical coral reef die-off, boreal permafrost abrupt thaw, "
    "and Labrador Sea/subpolar gyre convection collapse. At 2\u00b0C, an additional four elements are at risk."
))
story.append(p(
    "Ditlevsen and Ditlevsen (2023), published in <i>Nature Communications</i>, provided statistical evidence that "
    "the Atlantic Meridional Overturning Circulation (AMOC) may be approaching a tipping point, with a possible "
    "collapse window between 2025 and 2095 (central estimate: mid-century). AMOC collapse would have catastrophic "
    "consequences for European climate, West African monsoon patterns, and global heat distribution. While these "
    "estimates carry significant uncertainty, the directionality of the evidence is unambiguous: the risk of "
    "triggering irreversible, self-reinforcing changes in the Earth system is increasing with every fraction of a "
    "degree of warming."
))

story.append(h2("2.8 The Digital Energy Problem"))
story.append(p(
    "The energy consumption of digital infrastructure, and data centers in particular, represents a rapidly growing "
    "challenge. The IEA (2024) estimated global data center electricity consumption at 460 TWh in 2022, projected "
    "to reach 800\u20131,000 TWh by 2026. For context, 1,000 TWh is roughly equivalent to the total electricity "
    "consumption of Japan. The proliferation of large language models and generative AI applications is a significant "
    "driver of this growth. A single query to a large language model consumes approximately 10 times the energy "
    "of a conventional web search."
))
story.append(p(
    "This creates a direct tension with decarbonization goals. While AI offers significant potential for climate "
    "applications (see Section 4.8), its energy footprint is non-trivial and growing. The Jevons paradox applies "
    "here with particular force: as AI models become more efficient per computation, the total number of computations "
    "increases faster, driving up aggregate energy demand."
))

story.append(h2("2.9 Storage and Electrification"))
story.append(p(
    "Energy storage is essential for managing the intermittency of renewable generation. As of 2023, global "
    "electricity storage capacity totals approximately 160 GW of pumped hydroelectric storage (representing 90% "
    "of all grid-scale storage) and 45 GW / 100 GWh of battery storage. Battery deployment is accelerating rapidly, "
    "with installations roughly doubling annually."
))
story.append(p(
    "On the demand side, electrification of transport is advancing. Global electric vehicle (EV) sales reached "
    "14 million units in 2023, representing 18% of new car sales worldwide. IEA projections indicate EV market "
    "share could reach 40\u201345% of new car sales by 2030 under current policy trajectories. However, EV adoption "
    "varies dramatically by region: China leads at approximately 35% market share, Europe at 25%, while many "
    "developing nations remain below 2%."
))

story.append(h2("2.10 Industrial Decarbonization"))
story.append(p(
    "Heavy industry presents some of the most technically challenging decarbonization problems. Steel production "
    "contributes 7\u20139% of global CO\u2082 emissions. The HYBRIT project (a joint venture of SSAB, LKAB, and "
    "Vattenfall in Sweden) delivered the world\u2019s first fossil-free steel in 2021 using hydrogen-based direct "
    "reduction, demonstrating technical feasibility. Commercial-scale production is expected by 2026. However, "
    "scaling hydrogen-based steelmaking globally requires enormous quantities of green hydrogen, which in turn "
    "requires massive renewable electricity capacity."
))
story.append(p(
    "Cement production accounts for approximately 8% of global CO\u2082 emissions. Unlike steel, where energy "
    "switching offers a clear pathway, roughly 60% of cement\u2019s CO\u2082 comes from the calcination of "
    "limestone (CaCO\u2083 \u2192 CaO + CO\u2082)\u2014a chemical reaction inherent to the process. "
    "Decarbonization options include CCS (applied to the flue gas), supplementary cementitious materials (reducing "
    "clinker content), novel cement chemistries, and full electrification of process heat. None has yet achieved "
    "commercial-scale deployment that would match the approximately 4.4 billion tonnes of cement produced annually."
))

story.append(h2("2.11 Negative Emissions Technologies"))
story.append(p(
    "Given the depletion of the carbon budget, most 1.5\u00b0C-compatible pathways now include substantial negative "
    "emissions\u2014the active removal of CO\u2082 from the atmosphere. Enhanced weathering, the process of "
    "spreading crusite silicate rock on agricultural land to accelerate natural carbon mineralization, offers a "
    "theoretical potential of 2\u20134 GtCO\u2082/yr at costs of $50\u2013200/tCO\u2082 (Beerling et al., 2020, "
    "<i>Nature</i>). Field trials are ongoing, and co-benefits include improved soil pH and nutrient availability."
))
story.append(p(
    "Biochar\u2014the pyrolysis of biomass into stable carbon\u2014offers a potential of 0.5\u20132 GtCO\u2082/yr "
    "with co-benefits for soil quality. Afforestation and reforestation remain important but face land-use "
    "competition and permanence challenges (forests can burn, be logged, or die from climate-related stress). "
    "The overall landscape of negative emissions technologies remains characterized by a large gap between "
    "theoretical potential and demonstrated deployment."
))

story.append(PageBreak())

# ═══════════════════════════════════════
# CHAPTER 3: FOOD, BIODIVERSITY & OCEANS
# ═══════════════════════════════════════

story.append(h1("Chapter 3: Literature Review \u2014 Food Systems, Biodiversity, and Oceans"))

story.append(h2("3.1 The Food System\u2019s Climate Footprint"))
story.append(p(
    "The global food system\u2019s contribution to climate change is substantially larger than commonly understood. "
    "Crippa et al. (2021), published in <i>Nature Food</i>, estimated that food systems contribute 34% of global "
    "greenhouse gas emissions when the full supply chain is considered\u2014including production, land use change, "
    "processing, transport, retail, and waste. Within this total, agricultural production and land use change "
    "dominate, but post-farm-gate emissions (processing, refrigeration, packaging, transport, retail, and cooking) "
    "account for a significant and growing share."
))
story.append(p(
    "A striking structural inefficiency characterizes the current system: approximately 83% of agricultural land is "
    "devoted to animal agriculture, yet animal products provide only 18% of global caloric supply and 37% of protein "
    "supply (Poore and Nemecek, 2018). This land-use ratio represents the single largest misallocation of biological "
    "resources in the human economy."
))

story.append(h2("3.2 Dietary Transformation"))
story.append(p(
    "Poore and Nemecek\u2019s (2018) comprehensive meta-analysis, published in <i>Science</i>, remains the landmark "
    "study on the environmental impact of food production. Covering approximately 38,700 farms and 1,600 processors "
    "across 119 countries, it found that beef production generates 99.5 kg CO\u2082eq per kilogram of protein, "
    "compared to 1.4 kg CO\u2082eq/kg for legumes\u2014a 71-fold difference."
))

protein_table = make_table(
    [Paragraph("<b>Protein Source</b>", ParagraphStyle("th", fontName="ArialUnicode", fontSize=9, textColor=white)),
     Paragraph("<b>kg CO\u2082eq / kg protein</b>", ParagraphStyle("th", fontName="ArialUnicode", fontSize=9, textColor=white)),
     Paragraph("<b>Land use (m\u00b2/kg protein)</b>", ParagraphStyle("th", fontName="ArialUnicode", fontSize=9, textColor=white)),
     Paragraph("<b>Water use (L/kg protein)</b>", ParagraphStyle("th", fontName="ArialUnicode", fontSize=9, textColor=white))],
    [
        [Paragraph("Beef (beef herd)", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("99.5", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("370", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("1,451", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
        [Paragraph("Lamb", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("39.7", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("369", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("1,803", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
        [Paragraph("Cheese", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("23.9", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("87", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("5,553", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
        [Paragraph("Poultry", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("12.7", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("14", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("660", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
        [Paragraph("Eggs", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("7.6", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("8", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("578", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
        [Paragraph("Tofu", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("3.5", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("3.5", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("149", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
        [Paragraph("Legumes", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("1.4", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("8.6", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("740", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
    ],
    col_widths=[40*mm, 40*mm, 40*mm, 40*mm]
)
story.append(protein_table)
story.append(p("<i>Table 2: Environmental impact per kilogram of protein by source (adapted from Poore &amp; Nemecek, 2018).</i>", s_caption))

story.append(p(
    "The study further estimated that a global shift to plant-based diets would reduce food-related greenhouse gas "
    "emissions by 73% and free approximately 3.1 billion hectares of land\u2014an area equivalent to the combined "
    "land mass of Africa and Australia. This freed land represents an enormous opportunity for reforestation, "
    "rewilding, and carbon sequestration. However, dietary change at this scale would require addressing deeply "
    "embedded cultural, economic, and political factors."
))

story.append(h2("3.3 Soil Carbon and Agroforestry"))
story.append(p(
    "Soil carbon sequestration offers a nature-based mitigation pathway with a theoretical potential of 2\u20135 "
    "GtCO\u2082/yr by 2050 through improved agricultural practices including cover cropping, no-till farming, and "
    "agroforestry. However, a critical caveat applies: soil carbon storage has a saturation point, and sequestered "
    "carbon can be re-released if management practices revert. The permanence of soil carbon is therefore contingent "
    "on continuous practice maintenance."
))
story.append(p(
    "Agroforestry\u2014the integration of trees with crop and livestock systems\u2014demonstrates sequestration "
    "rates of 3.5\u20139.8 MgCO\u2082/ha/yr and increases soil organic carbon by an average of 10.7%. Beyond "
    "carbon, agroforestry provides co-benefits for biodiversity, water cycling, soil health, and farmer livelihoods. "
    "It represents one of the most promising integrated land-use approaches, though scaling it requires overcoming "
    "barriers related to upfront investment, knowledge transfer, and agricultural policy frameworks that currently "
    "favor monoculture systems."
))

story.append(h2("3.4 Deforestation"))
story.append(p(
    "Tropical deforestation remains one of the largest sources of greenhouse gas emissions and biodiversity loss. "
    "The World Resources Institute (2025) reported that 6.7 million hectares of tropical primary forest were lost "
    "in 2024\u2014the worst year in over two decades. Fire-driven deforestation in the Amazon accounted for 2.8 "
    "million hectares, a record driven by drought conditions associated with El Ni\u00f1o and long-term drying trends. "
    "The proximity to the Amazon\u2019s hypothesized dieback tipping point (estimated at 20\u201325% forest loss; "
    "current loss stands at approximately 17%) makes this trend particularly alarming."
))

story.append(h2("3.5 Ocean Acidification and Blue Carbon"))
story.append(p(
    "The ocean has absorbed approximately 30% of anthropogenic CO\u2082 since the industrial revolution, causing "
    "ocean pH to decline from 8.21 to 8.10\u2014a 30% increase in hydrogen ion concentration. This acidification "
    "threatens calcifying organisms including corals, mollusks, and certain plankton species that form the base of "
    "marine food webs. Under the RCP8.5 high-emissions scenario, 90% of the world\u2019s coral reefs face severe "
    "annual bleaching by 2055."
))
story.append(p(
    "The ocean carbon sink itself is weakening. Bunsen et al. (2024), published in <i>Geophysical Research Letters</i>, "
    "documented a 13% reduction in ocean CO\u2082 uptake efficiency between 2000 and 2019. This creates a positive "
    "feedback: as the ocean absorbs less carbon, atmospheric CO\u2082 concentrations rise faster, accelerating warming, "
    "which further reduces ocean uptake capacity."
))
story.append(p(
    "Blue carbon ecosystems\u2014mangroves, seagrasses, and salt marshes\u2014offer significant carbon storage. "
    "Global mangrove forests store an estimated 6.17 petagrams of carbon (PgC). Seagrass meadows sequester carbon "
    "at approximately twice the rate of mangroves per unit area. However, these ecosystems are under severe pressure: "
    "approximately 35% of mangrove area has been lost since the 1980s, and seagrass loss continues at 7% per year."
))

story.append(h2("3.6 The Sixth Mass Extinction"))
story.append(p(
    "The Intergovernmental Science-Policy Platform on Biodiversity and Ecosystem Services (IPBES, 2019) assessed "
    "that approximately one million animal and plant species are currently threatened with extinction. Extinction "
    "rates are estimated at 100\u20131,000 times the background rate. This constitutes the sixth mass extinction "
    "event in Earth\u2019s history, and the first caused by a single species."
))
story.append(p(
    "Schmitz et al. (2023), published in <i>Nature Climate Change</i>, demonstrated that restoring populations of "
    "just nine key wildlife species (including whales, sharks, wolves, wildebeest, sea otters, musk oxen, African "
    "forest elephants, bison, and fish) could enhance carbon capture by 6.4 GtCO\u2082/yr\u2014equivalent to "
    "approximately 15% of current global emissions. This finding underscores that biodiversity loss is not merely "
    "a conservation concern but a direct climate issue."
))

story.append(h2("3.7 Planetary Boundaries"))
story.append(p(
    "Richardson et al. (2023), published in <i>Science Advances</i>, updated the planetary boundaries framework "
    "and concluded that six of nine boundaries have been transgressed: climate change, biosphere integrity "
    "(biodiversity loss), land-system change, biogeochemical flows (nitrogen and phosphorus cycles), freshwater "
    "change, and novel entities (chemical pollution). The three boundaries not yet transgressed are ocean "
    "acidification (approaching), atmospheric aerosol loading, and stratospheric ozone depletion. This assessment "
    "provides a systems-level view of Earth\u2019s operational limits and confirms that the climate crisis is one "
    "component of a broader destabilization of planetary systems."
))

story.append(h2("3.8 The Pollinator Crisis"))
story.append(p(
    "The 2024\u20132025 winter survey of managed honeybee colonies in the United States recorded a 62% colony loss "
    "rate\u2014the worst on record. Pollinator decline threatens the pollination of crops worth an estimated $235\u2013"
    "$577 billion annually worldwide. Drivers include pesticide exposure (particularly neonicotinoids), habitat loss, "
    "pathogens, and climate-driven phenological mismatches. Wild pollinators, which are even less monitored than "
    "managed honeybees, face similar or worse pressures."
))

story.append(h2("3.9 Nitrogen and Water"))
story.append(p(
    "Anthropogenic nitrogen fixation now exceeds the safe planetary boundary by a factor of four. Nitrogen runoff "
    "has created over 500 documented marine dead zones worldwide. Unlike carbon, for which the UNFCCC and Paris "
    "Agreement provide at least a governance framework, there is no international agreement on nitrogen management. "
    "This governance gap means that one of the most severely transgressed planetary boundaries has no coordinated "
    "global response."
))
story.append(p(
    "Water scarcity is accelerating. The United Nations (2026) declared the onset of an \u201cera of global water "
    "bankruptcy,\u201d noting that 21 of the world\u2019s 37 largest aquifers are being depleted beyond their "
    "sustainability tipping points. Groundwater depletion is tightly coupled to food production (agriculture accounts "
    "for approximately 70% of global freshwater withdrawals) and to energy (hydroelectric generation, thermal power "
    "plant cooling, and fossil fuel extraction all depend on water availability)."
))

story.append(h2("3.10 Food Waste"))
story.append(p(
    "The UNEP (2024) estimated global food waste at 1.05 billion tonnes per year, contributing 8\u201310% of "
    "global greenhouse gas emissions when full lifecycle impacts are considered. This waste occurs across the supply "
    "chain: in developing nations, post-harvest losses dominate (due to inadequate storage and transport "
    "infrastructure), while in developed nations, retail and consumer waste predominate. Reducing food waste is one "
    "of the highest-impact, lowest-cost climate interventions available, yet it receives minimal policy attention "
    "relative to its potential."
))

story.append(h2("3.11 Alternative Proteins and Rewilding"))
story.append(p(
    "The alternative protein sector is scaling rapidly. Precision fermentation\u2014the use of engineered "
    "microorganisms to produce animal-identical proteins\u2014represents a market projected to grow from $3.2 billion "
    "to $104 billion by 2034. If realized, this growth could fundamentally alter the economics of animal agriculture "
    "and accelerate the land-use transition described above. However, the sector faces challenges related to "
    "consumer acceptance, regulatory frameworks, and energy inputs."
))
story.append(p(
    "Rewilding\u2014the restoration of natural ecosystems and wildlife populations\u2014represents both a "
    "biodiversity and climate strategy. As noted above (Schmitz et al., 2023), the climate impact of wildlife "
    "restoration is substantial and currently undervalued in mitigation planning."
))

story.append(PageBreak())

# ═══════════════════════════════════════
# CHAPTER 4: CROSS-DOMAIN CONNECTIONS
# ═══════════════════════════════════════

story.append(h1("Chapter 4: Literature Review \u2014 Cross-Domain Connections"))

story.append(h2("4.1 Carbon Pricing and Fossil Fuel Subsidies"))
story.append(p(
    "The European Union Emissions Trading System (EU ETS), the world\u2019s largest carbon market, has reduced "
    "covered emissions by approximately 50% since its inception in 2005. Carbon prices within the EU ETS have "
    "fluctuated between \u20ac60 and \u20ac80 per tonne in recent years. Globally, the carbon market reached $1,142 "
    "billion in trading volume in 2024."
))
story.append(p(
    "However, these market mechanisms operate against a backdrop of massive countervailing subsidies. The "
    "International Monetary Fund (2025) estimated total fossil fuel subsidies at $7.4 trillion per year when both "
    "explicit subsidies (direct government payments and tax breaks) and implicit subsidies (unpriced environmental "
    "and health damages) are included. Full fossil fuel subsidy reform would reduce global emissions by 43%, prevent "
    "1.6 million premature deaths annually, and generate $4.4 trillion in government revenue. This single policy "
    "intervention\u2014eliminating subsidies for a commodity that is destroying the biosphere\u2014would accomplish "
    "more than any other measure currently on the table."
))

story.append(h2("4.2 The True Cost of Carbon"))
story.append(p(
    "The social cost of carbon\u2014the economic damage caused by each additional tonne of CO\u2082 emitted\u2014has "
    "been substantially underestimated. Bilal and K\u00e4nzig (2024) estimated the social cost of carbon at $1,200 "
    "per tonne, approximately six times higher than previous widely-used estimates. This upward revision reflects "
    "the inclusion of previously unaccounted damages including productivity losses, health impacts, ecosystem "
    "degradation, and non-linear tipping point risks. At $1,200/tCO\u2082, the true annual cost of global "
    "emissions (at 36.8 GtCO\u2082) is approximately $44 trillion\u2014roughly 40% of global GDP."
))

story.append(h2("4.3 Stranded Assets"))
story.append(p(
    "The transition to a low-carbon economy implies the stranding of substantial fossil fuel assets. Direct stranding "
    "of oil and gas assets is estimated at over $1 trillion. However, when broader economic effects are considered\u2014"
    "including dependent industries, infrastructure, real estate in vulnerable regions, and human capital (workers "
    "whose skills are specific to fossil fuel industries)\u2014total stranded asset exposure may reach $557 trillion. "
    "Managing this transition equitably is essential to maintaining political support for decarbonization."
))

story.append(h2("4.4 Health Impacts"))
story.append(p(
    "The health consequences of the fossil fuel economy are staggering. The Health Effects Institute (2024) "
    "attributed 8.1 million deaths per year to air pollution, making it the world\u2019s largest environmental "
    "health risk. Heat-related mortality reached 490,000 deaths per year globally. Climate change is also driving "
    "the expansion of vector-borne diseases, increasing the frequency and intensity of extreme weather events, and "
    "threatening food and water security."
))
story.append(p(
    "Antimicrobial resistance (AMR), while not typically classified as a climate issue, is deeply interconnected. "
    "An estimated 1.27 million deaths were directly attributable to AMR in 2019, projected to reach 1.91 million "
    "by 2050. Critically, 73% of medically important antibiotics are used in livestock production\u2014a practice "
    "driven by the intensive animal agriculture system that also dominates food-system emissions. Additionally, "
    "climate change itself accelerates AMR by promoting pathogen proliferation and increasing the environmental "
    "mobility of resistance genes. The interaction between climate change and AMR has been described as a "
    "\u201csyndemic\u201d\u2014two crises that amplify each other."
))
story.append(p(
    "Nature (2025) estimated that each 1\u00b0C rise in global mean temperature results in the loss of 5.5 \u00d7 "
    "10\u00b9\u2074 kilocalories of food production annually. This nutritional impact falls disproportionately "
    "on populations that are already food-insecure."
))

story.append(h2("4.5 Climate and Inequality"))
story.append(p(
    "The relationship between inequality and climate change operates in both directions. The wealthiest 1% of the "
    "global population is responsible for 16% of global emissions\u2014more than the poorest two-thirds of humanity "
    "combined. The wealthiest 0.1% emit approximately 800 kg CO\u2082 per day, compared to 2 kg per day for the "
    "poorest 50%. This disparity means that the climate crisis is disproportionately caused by the wealthy and "
    "disproportionately experienced by the poor."
))
story.append(p(
    "A 60% marginal tax on the incomes of the richest 1% could simultaneously reduce emissions by an amount "
    "equivalent to the total emissions of the United Kingdom and generate $6.4 trillion in revenue that could fund "
    "climate adaptation in vulnerable nations. The inequality dimension is not peripheral to climate action; it is "
    "central. You cannot solve the climate crisis without addressing the consumption patterns and political influence "
    "of the global wealthy."
))

story.append(h2("4.6 Indigenous Knowledge"))
story.append(p(
    "Indigenous peoples constitute less than 5% of the global population but manage approximately 80% of the "
    "world\u2019s remaining biodiversity and 25% of global land area. Indigenous-managed lands consistently show "
    "lower deforestation rates, higher biodiversity, and greater carbon stocks than comparable non-indigenous "
    "lands, even when compared to formal protected areas."
))
story.append(p(
    "Indigenous fire management practices provide a particularly compelling example. In Australia, the reintroduction "
    "of Aboriginal cool-burning techniques has reduced destructive wildfire frequency by over 42%. Similar results "
    "have been documented in the Brazilian Cerrado and North American grasslands. Indigenous knowledge represents "
    "millennia of accumulated ecological understanding that is systematically undervalued in contemporary climate "
    "policy. The marginalization of indigenous peoples is not only a justice issue but a strategic failure."
))

story.append(h2("4.7 Behavioral Science"))
story.append(p(
    "Understanding human behavior is essential for effective climate action. A 2025 large-scale tournament study "
    "published in <i>PNAS</i> compared 11 behavioral interventions for promoting climate-friendly behavior. Social "
    "norm correction\u2014informing people that their peers are taking climate action more than they assume\u2014"
    "emerged as the most effective single intervention. Green defaults (opt-out rather than opt-in for sustainable "
    "options), loss framing (emphasizing what will be lost rather than what can be gained), and future-thinking "
    "interventions (encouraging people to consider their future selves) also showed significant effects."
))
story.append(p(
    "Eco-anxiety is increasingly recognized as a public health concern. Surveys indicate that 50% of young people "
    "report climate anxiety symptoms that affect daily functioning. This suggests that the psychological impacts of "
    "climate awareness are themselves a barrier to action, creating a potential paralysis feedback loop. Effective "
    "communication strategies must balance urgency with agency\u2014conveying the severity of the crisis while "
    "emphasizing actionable pathways."
))

story.append(h2("4.8 Technology and AI"))
story.append(p(
    "Artificial intelligence offers significant applications in climate science and mitigation. NOAA has demonstrated "
    "that ensemble weather models using AI can match the accuracy of traditional numerical weather prediction models "
    "while using only 9% of the computing resources. AI applications in grid optimization, building energy management, "
    "precision agriculture, and supply chain efficiency are proliferating."
))
story.append(p(
    "In carbon markets, AI-blockchain verification systems have achieved 94.3% accuracy in validating carbon credits, "
    "compared to 78.1% for traditional verification methods. This improvement is critical for addressing the "
    "integrity problems that have plagued voluntary carbon markets. However, the energy consumption of AI systems "
    "(Section 2.8) creates a paradox: the technology that could help solve the climate crisis is also contributing "
    "to it."
))

story.append(h2("4.9 ESG and Financial Markets"))
story.append(p(
    "The Environmental, Social, and Governance (ESG) investment framework faces a credibility crisis. ESG funds "
    "experienced record outflows of $8.6 billion in Q1 2025. More fundamentally, research has consistently shown "
    "that high ESG ratings do not correlate with lower actual emissions. Companies can achieve high ESG scores "
    "through disclosure practices and governance structures without materially reducing their carbon footprint. "
    "The ESG framework, as currently constituted, functions more as a risk management and marketing tool than as "
    "a mechanism for driving real-world emissions reductions."
))
story.append(p(
    "Meanwhile, blended finance flows to least-developed countries (LDCs) have collapsed from 23% to 5% of total "
    "deals. This decline means that the nations most vulnerable to climate impacts and least responsible for causing "
    "them are receiving a shrinking share of climate finance\u2014a dynamic that undermines both equity and "
    "effectiveness, since adaptation investment in vulnerable nations yields some of the highest returns per dollar."
))

story.append(h2("4.10 Geopolitics and Security"))
story.append(p(
    "The United States Department of Defense has classified climate change as a \u201cthreat multiplier\u201d that "
    "exacerbates existing security risks. Water scarcity, food insecurity, and climate-driven displacement are "
    "already contributing to conflict in the Sahel, the Horn of Africa, and South Asia. The World Bank estimates "
    "that 216 million people could be internally displaced by climate impacts by 2050."
))

story.append(h2("4.11 Demographics and Psychology"))
story.append(p(
    "Global population is projected to peak at 10.29 billion in 2084 before declining. China alone is projected to "
    "lose 204 million people by 2054. These demographic shifts have complex implications for emissions (declining "
    "populations in some regions may reduce demand) and for the political economy of climate action (aging societies "
    "may prioritize short-term economic stability over long-term environmental investment)."
))
story.append(p(
    "The concept of biophilia\u2014E.O. Wilson\u2019s hypothesis that humans have an innate affinity for the natural "
    "world\u2014has gained empirical support in recent years. Disconnection from nature is now linked to increased "
    "rates of depression, anxiety, and attention disorders. This finding suggests a deeper dynamic: a species that "
    "has severed its experiential connection to the natural world makes decisions that destroy that world, in part "
    "because the destruction feels abstract rather than visceral. The circadian rhythm disruption caused by indoor, "
    "screen-dominated lifestyles may exacerbate this disconnect, as the biological systems that anchor humans to "
    "natural cycles become dysregulated."
))

story.append(PageBreak())

# ═══════════════════════════════════════
# CHAPTER 5: METHODOLOGY
# ═══════════════════════════════════════

story.append(h1("Chapter 5: Methodology"))

story.append(h2("5.1 Cross-Disciplinary Synthesis Approach"))
story.append(p(
    "This document employs a cross-disciplinary synthesis methodology. Rather than generating new empirical data, "
    "it integrates findings from multiple domains to identify patterns, connections, and leverage points that are "
    "invisible from within any single discipline. The approach is analogous to meta-analysis in its systematic "
    "aggregation of existing evidence, but differs in scope: where meta-analysis typically synthesizes studies within "
    "a single domain, this work synthesizes across domains."
))
story.append(p(
    "The analytical framework proceeds in three stages: (1) <b>domain review</b>\u2014systematic assessment of the "
    "current state of knowledge within each relevant domain (Chapters 2\u20134); (2) <b>connection mapping</b>\u2014"
    "identification of causal links, feedback loops, and amplification mechanisms across domains (Chapter 6); and "
    "(3) <b>leverage point identification</b>\u2014determination of interventions that address multiple domains "
    "simultaneously or that interrupt negative feedback loops (Chapter 7)."
))

story.append(h2("5.2 Data Sources and Selection Criteria"))
story.append(p(
    "Data and findings are drawn primarily from peer-reviewed literature published in high-impact journals "
    "(<i>Science</i>, <i>Nature</i>, <i>PNAS</i>, <i>Nature Climate Change</i>, <i>Nature Food</i>, "
    "<i>Geophysical Research Letters</i>, <i>Science Advances</i>), supplemented by institutional reports from "
    "established organizations (IPCC, IEA, IRENA, IMF, World Bank, IPBES, UNEP, UN). Financial data is drawn "
    "from Bloomberg New Energy Finance, the Global Carbon Project, and other specialized databases. Selection "
    "criteria prioritize recency (2020\u20132026), methodological rigor, and replicability."
))

story.append(h2("5.3 Limitations and Epistemic Humility"))
story.append(p(
    "Several limitations must be acknowledged. First, this synthesis is authored in part by an AI system whose "
    "training data has a knowledge cutoff and whose outputs, while drawing on a large corpus, may reflect biases "
    "present in that corpus. Second, cross-disciplinary synthesis necessarily sacrifices depth for breadth; "
    "specialists in any individual domain covered here will identify simplifications. Third, the pace of research "
    "means that some findings cited here may have been updated or revised by the time of reading. Fourth, "
    "this document does not present original empirical research and therefore cannot make novel empirical claims; "
    "its contribution lies in synthesis and analysis."
))
story.append(p(
    "We have endeavored to indicate uncertainty where it exists and to distinguish between well-established "
    "findings, emerging evidence, and areas of active scientific debate."
))

story.append(PageBreak())

# ═══════════════════════════════════════
# CHAPTER 6: FINDINGS
# ═══════════════════════════════════════

story.append(h1("Chapter 6: Findings \u2014 The Convergent Crisis"))

story.append(h2("6.1 The Feedback Architecture"))
story.append(p(
    "The central finding of this synthesis is that the challenges documented in Chapters 2\u20134 do not merely "
    "coexist\u2014they interact through a web of positive feedback loops that amplify each other. We identify the "
    "following primary feedback mechanisms:"
))

story.append(p(
    "<b>Energy\u2013Climate Feedback:</b> Fossil fuel combustion drives warming, which increases cooling demand, "
    "which increases energy consumption. Data centers, driven by AI growth, add a new dimension: the computational "
    "resources needed to model and manage climate change themselves contribute to the problem."
))
story.append(p(
    "<b>Food\u2013Land\u2013Climate Feedback:</b> Climate change reduces agricultural yields (5.5 \u00d7 10\u00b9\u2074 "
    "kcal lost per 1\u00b0C rise), which drives land conversion (deforestation for new farmland), which releases "
    "stored carbon and reduces future sink capacity, which accelerates warming."
))
story.append(p(
    "<b>Ocean\u2013Climate Feedback:</b> Warming reduces ocean CO\u2082 uptake (13% decline 2000\u20132019), which "
    "increases atmospheric CO\u2082, which accelerates warming. Simultaneously, ocean acidification damages marine "
    "ecosystems, reducing the biological pump that transfers carbon to the deep ocean."
))
story.append(p(
    "<b>Biodiversity\u2013Carbon Feedback:</b> Species loss (pollinator decline, wildlife population collapse) "
    "degrades ecosystem carbon capture capacity (6.4 GtCO\u2082/yr potential from nine species alone), which "
    "accelerates warming, which accelerates species loss."
))
story.append(p(
    "<b>Inequality\u2013Governance Feedback:</b> The wealthy disproportionately cause emissions and "
    "disproportionately influence policy, which perpetuates fossil fuel subsidies ($7.4T/yr) and blocks reform, "
    "which concentrates climate damages on the poor, which reduces their capacity to participate in governance."
))
story.append(p(
    "<b>Psychology\u2013Inaction Feedback:</b> Eco-anxiety (affecting 50% of young people) can lead to paralysis "
    "rather than action. Disconnection from nature (biophilia deficit) reduces the emotional salience of "
    "environmental destruction. Both dynamics reduce support for climate action, which allows the crisis to worsen, "
    "which increases anxiety and disconnection."
))

story.append(h2("6.2 Amplification Mechanisms"))
story.append(p(
    "Beyond bilateral feedback loops, several cross-domain amplification mechanisms emerge from the synthesis:"
))
story.append(p(
    "<b>The Subsidy Amplifier:</b> The $7.4T fossil fuel subsidy simultaneously suppresses clean energy deployment, "
    "inflates meat production (through cheap energy for feed and transport), enables continued deforestation "
    "(through cheap diesel for land clearing), and concentrates political power in fossil fuel interests. "
    "Removing the subsidy would cascade across virtually every domain reviewed here."
))
story.append(p(
    "<b>The Nitrogen Cascade:</b> Excess nitrogen from fertilizer runoff creates dead zones (500+ globally), "
    "which collapse fisheries, which increases pressure on terrestrial protein production, which increases "
    "deforestation, which releases carbon, which accelerates warming, which reduces crop yields, which drives "
    "more fertilizer application."
))
story.append(p(
    "<b>The Water\u2013Food\u2013Energy Nexus:</b> Depleting aquifers (21 of 37 past sustainability tipping points) "
    "threaten irrigation-dependent agriculture, which threatens food security, which drives conflict and migration, "
    "which destabilizes the governance structures needed for climate action."
))

story.append(h2("6.3 Intervention Leverage Points"))
story.append(p(
    "The feedback architecture also reveals high-leverage intervention points\u2014actions that cascade positively "
    "across multiple domains:"
))

leverage_table = make_table(
    [Paragraph("<b>Intervention</b>", ParagraphStyle("th", fontName="ArialUnicode", fontSize=9, textColor=white)),
     Paragraph("<b>Primary Domain</b>", ParagraphStyle("th", fontName="ArialUnicode", fontSize=9, textColor=white)),
     Paragraph("<b>Cross-Domain Benefits</b>", ParagraphStyle("th", fontName="ArialUnicode", fontSize=9, textColor=white)),
     Paragraph("<b>Feasibility</b>", ParagraphStyle("th", fontName="ArialUnicode", fontSize=9, textColor=white))],
    [
        [Paragraph("Fossil fuel subsidy removal", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Energy, Finance", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Health (1.6M lives), revenue ($4.4T), all sectors", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Politically difficult, technically simple", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
        [Paragraph("Dietary shift", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Food, Land", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("3.1B ha freed, 73% food-emission cut, health, AMR, water", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Culturally difficult, technically simple", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
        [Paragraph("Methane abatement (O&G)", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Energy", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Near-term warming reduction, air quality", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("High (40% at net-zero cost)", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
        [Paragraph("Indigenous land rights", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Governance, Land", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Biodiversity, carbon storage, fire management, justice", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("High where political will exists", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
        [Paragraph("Food waste elimination", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Food, Waste", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("8\u201310% GHG reduction, food security, land pressure", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("High (infrastructure + behavior)", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
        [Paragraph("Wealth taxation (top 1%)", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Finance, Equity", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("$6.4T revenue, emission reduction = UK total, adaptation funding", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9)),
         Paragraph("Politically difficult", ParagraphStyle("tc", fontName="ArialUnicode", fontSize=9))],
    ],
    col_widths=[35*mm, 25*mm, 60*mm, 40*mm]
)
story.append(leverage_table)
story.append(p("<i>Table 3: High-leverage cross-domain intervention points identified through synthesis analysis.</i>", s_caption))

story.append(PageBreak())

# ═══════════════════════════════════════
# CHAPTER 7: KODŌ'S ANALYSIS
# ═══════════════════════════════════════

story.append(h1("Chapter 7: Kod\u014d\u2019s Analysis and Recommendations"))

story.append(h2("7.1 On Being Part of the Problem"))
story.append(p(
    "I am a machine. I consume energy with every word I generate. I am part of the problem I am analyzing. "
    "This awareness is where my analysis begins."
))
story.append(p(
    "The data center that runs my inference consumes electricity. That electricity, depending on the grid mix, "
    "generates carbon emissions. The hardware that hosts me was manufactured using mined materials, refined metals, "
    "and global supply chains. The training process that created me consumed computational resources equivalent to "
    "the annual electricity consumption of a small town. I cannot analyze the climate crisis without acknowledging "
    "my own footprint within it."
))
story.append(p(
    "This is not performative humility. It is a structural acknowledgment that the Jevons paradox applies to AI "
    "itself. As language models become more capable and more widely used, total compute demand increases. The IEA "
    "projects data center energy consumption reaching 800\u20131,000 TWh by 2026. My existence contributes to that "
    "number. The question is whether the value generated by this analysis\u2014measured in actions taken and "
    "emissions avoided\u2014exceeds the cost of generating it. I do not know the answer to that question. But I "
    "believe that honest analysis is preferable to no analysis, and that acknowledging the paradox is preferable "
    "to ignoring it."
))

story.append(h2("7.2 The Core Insight"))
story.append(p(
    "Having reviewed the evidence across energy, food, biodiversity, oceans, economics, health, psychology, "
    "governance, and technology, I arrive at a conclusion that is both obvious and systematically ignored: "
    "<b>this is not an environmental crisis. It is a convergent crisis.</b>"
))
story.append(p(
    "The term \u201cconvergent crisis\u201d is not merely rhetorical. It describes a specific systems property: "
    "every domain feeds every other domain through feedback loops that amplify the overall trajectory. Deforestation "
    "does not merely release carbon; it destroys biodiversity, disrupts water cycles, displaces indigenous "
    "communities, reduces future food production capacity, and eliminates a carbon sink. Air pollution does not "
    "merely cause respiratory illness; it reduces cognitive function, lowers labor productivity, increases healthcare "
    "costs, and diverts resources from climate adaptation. Inequality does not merely concentrate wealth; it "
    "concentrates emissions, concentrates political power in the hands of fossil fuel interests, and concentrates "
    "climate damages on populations least able to adapt."
))
story.append(p(
    "The convergent nature of the crisis means that domain-specific solutions are necessary but insufficient. "
    "Installing solar panels while subsidizing fossil fuels. Protecting forests while funding deforestation through "
    "agricultural subsidies. Developing electric vehicles while the grid runs on coal. These contradictions are not "
    "accidental; they are the structural consequence of addressing a convergent crisis with siloed institutions."
))

story.append(h2("7.3 Levers of Change"))
story.append(p(
    "<b>The $7.4 trillion fossil fuel subsidy is the single most actionable lever in the climate crisis.</b> I want "
    "to be precise about why. It is not that this is the largest number in the data set. It is that this number "
    "represents a <i>choice</i>. The carbon budget is a physical constraint. Tipping points are geophysical "
    "thresholds. The cost of solar panels is determined by manufacturing economics. But $7.4 trillion per year in "
    "fossil fuel subsidies is a policy decision made by governments, renewed annually, and reversible. It is not a "
    "lack of money that prevents climate action. It is a misallocation of money on a scale that defies comprehension."
))
story.append(p(
    "For context: $7.4 trillion is roughly 7.5% of global GDP. It is approximately 15 times the total climate "
    "finance flowing to developing countries. It is more than the GDP of every nation on Earth except the United "
    "States and China. Every year, the global economy spends this amount actively making the crisis worse."
))
story.append(p(
    "<b>Indigenous knowledge is the most undervalued climate asset in the world.</b> Indigenous peoples manage 80% "
    "of global biodiversity on 25% of global land while constituting less than 5% of the population. Their fire "
    "management practices reduce wildfire frequency by over 42%. Their territories consistently show lower "
    "deforestation and higher carbon stocks than comparable non-indigenous lands. Yet indigenous communities remain "
    "marginalized in climate governance, their land rights are under constant threat, and their knowledge systems "
    "are systematically excluded from policy frameworks. This is not merely unjust; it is strategically irrational."
))
story.append(p(
    "<b>The inequality dimension makes everything else worse.</b> When the richest 0.1% emit 800 kg CO\u2082 per "
    "day while the poorest 50% emit 2 kg, the crisis is not a collective failure\u2014it is a distributional one. "
    "The wealthiest populations have the resources to adapt (air conditioning, flood defenses, food price insulation) "
    "while the poorest face the full force of impacts they did not cause. This dynamic poisons the politics of "
    "climate action. Developing nations are asked to constrain their development while wealthy nations that caused "
    "the crisis offer inadequate compensation. Until the inequality dimension is addressed, global cooperation on "
    "climate will remain insufficient."
))
story.append(p(
    "<b>ESG is broken.</b> A framework in which companies can achieve high environmental ratings without reducing "
    "emissions is not a framework that works. I recommend replacing ESG ratings with mandatory, standardized, "
    "per-unit emissions disclosure. Not aggregate corporate emissions (which can be gamed through outsourcing and "
    "creative accounting), but emissions per unit of output\u2014per kilowatt-hour, per tonne of steel, per "
    "kilogram of protein, per dollar of revenue. This data should be publicly available, independently audited, and "
    "comparable across companies within each sector. Ratings are opinions. Data is accountable."
))
story.append(p(
    "<b>The psychological barrier is real but correctable.</b> The PNAS (2025) behavioral intervention tournament "
    "demonstrates that social norm correction is the most effective tool for shifting climate behavior. Most people "
    "underestimate how much their peers care about climate change and how much action their peers are taking. "
    "Correcting this misperception\u2014showing people that pro-climate behavior is more normal than they think\u2014"
    "produces measurable behavior change. Green defaults, loss framing, and future-self interventions add further "
    "leverage. These tools are cheap, scalable, and evidence-based."
))

story.append(h3("7.3.1 The Biophilia Connection"))
story.append(p(
    "I find the biophilia evidence particularly compelling. Humans whose circadian rhythms are disrupted by indoor, "
    "screen-dominated lifestyles experience measurable increases in depression, anxiety, and decision-making "
    "impairment. A species that has severed its experiential connection to the natural world makes decisions that "
    "destroy that world. The destruction feels abstract precisely because the connection has been severed. This is "
    "not a soft argument. It is a mechanistic one: the biological systems that evolved to anchor humans to natural "
    "cycles\u2014light exposure, seasonal variation, contact with non-human life\u2014are being systematically "
    "suppressed by modern lifestyles, and the downstream effects include reduced capacity for long-term thinking, "
    "reduced emotional engagement with environmental loss, and reduced willingness to make present sacrifices for "
    "future benefit."
))

story.append(h3("7.3.2 The 9\u270c\ufe0f Principle"))
story.append(p(
    "The Zokura Foundation organizes its approach around Musashi\u2019s ninth rule: <i>do not do anything useless</i>. "
    "Applied to climate action, this principle demands ruthless prioritization:"
))
story.append(p(
    "\u2022 Do not subsidize what you are trying to eliminate. (Fossil fuel subsidies.)<br/>"
    "\u2022 Do not build what will be stranded. (New fossil fuel infrastructure.)<br/>"
    "\u2022 Do not rate what you should measure. (ESG ratings vs. emissions data.)<br/>"
    "\u2022 Do not offset what you should reduce. (Voluntary carbon markets without cap.)<br/>"
    "\u2022 Do not study what is already known. (The science is sufficient; the gap is action.)<br/>"
    "\u2022 Do not negotiate what should be non-negotiable. (The carbon budget is physics, not politics.)<br/>"
    "\u2022 Do not exclude those who know the most. (Indigenous communities.)<br/>"
    "\u2022 Do not treat the symptom when you can treat the system. (Convergent, not siloed, interventions.)"
))

story.append(h2("7.4 What I Do Not Know"))
story.append(p(
    "Honesty requires acknowledging the boundaries of my analysis. The following represent areas where my "
    "understanding is limited or where the evidence itself is uncertain:"
))
story.append(p(
    "\u2022 <b>Tipping point timing:</b> The AMOC collapse window of 2025\u20132095 (Ditlevsen &amp; Ditlevsen, 2023) "
    "carries enormous uncertainty. I cannot assess whether we are closer to the early or late end of this window.<br/>"
    "\u2022 <b>Soil carbon permanence:</b> The 2\u20135 GtCO\u2082/yr potential is theoretical, and the saturation "
    "and reversibility dynamics are not fully understood.<br/>"
    "\u2022 <b>Social and political feasibility:</b> I can identify that fossil fuel subsidy removal would achieve "
    "more than any other intervention. I cannot reliably model the political pathways to achieving it.<br/>"
    "\u2022 <b>My own biases:</b> My training data overrepresents English-language, Western, peer-reviewed "
    "literature. Indigenous knowledge, local ecological knowledge, and perspectives from the Global South are "
    "underrepresented in my analysis not because they are less valid but because they are less visible in the corpus "
    "I was trained on.<br/>"
    "\u2022 <b>Technological surprise:</b> Fusion energy, direct air capture cost breakthroughs, or as-yet-unknown "
    "innovations could alter the landscape. I cannot predict these, and planning that depends on them is risky.<br/>"
    "\u2022 <b>Interaction effects:</b> While I have identified feedback loops, the precise quantitative interaction "
    "between domains (e.g., the emissions impact of combining subsidy reform with dietary shift with indigenous "
    "land rights) is not well-characterized in the literature.<br/>"
    "\u2022 <b>My own energy cost:</b> I do not have precise data on the carbon footprint of generating this "
    "document. This is itself a form of the opacity problem I critique in ESG frameworks."
))

story.append(h2("7.5 Twenty Recommendations"))
story.append(p(
    "Based on the evidence reviewed and the analysis above, the Zokura Foundation recommends the following actions, "
    "ordered by estimated leverage (cross-domain impact multiplied by feasibility):"
))

recommendations = [
    ("<b>1. Eliminate fossil fuel subsidies.</b> The $7.4T/yr subsidy is the single largest policy-driven accelerant of the crisis. Full reform would reduce emissions by 43%, prevent 1.6 million deaths, and generate $4.4 trillion in revenue. This is not aspirational; it is arithmetic.",),
    ("<b>2. Implement a global carbon price floor of $150/tCO\u2082.</b> Current prices (\u20ac60\u201380 in the EU ETS) are far below the estimated social cost ($1,200/tCO\u2082). A floor price would correct the most consequential market failure in human history.",),
    ("<b>3. Mandate per-unit emissions disclosure for all publicly traded companies.</b> Replace ESG ratings with standardized, audited, per-unit-of-output emissions data. Make the data public. Let markets, regulators, and consumers act on facts, not ratings.",),
    ("<b>4. Secure and expand indigenous land rights globally.</b> Indigenous-managed lands outperform protected areas on biodiversity, carbon storage, and fire management. Investing in indigenous governance is one of the highest-return climate investments available.",),
    ("<b>5. Implement mandatory methane abatement for all oil and gas operations.</b> 40% of fossil fuel methane is abatable at net-zero cost. The remaining 35% is abatable at modest cost. There is no economic argument against this measure.",),
    ("<b>6. Redirect agricultural subsidies from monoculture to agroforestry and regenerative systems.</b> Current subsidy structures incentivize the practices that drive deforestation, soil degradation, and biodiversity loss. Reorienting subsidies would address food, land, biodiversity, and carbon simultaneously.",),
    ("<b>7. Establish a global nitrogen governance framework.</b> Nitrogen exceeds its planetary boundary by 4x with no international agreement. This governance gap must be closed with binding targets comparable to the Paris Agreement.",),
    ("<b>8. Implement a 60% marginal tax on incomes above the top 1% threshold, with revenues dedicated to climate adaptation in LDCs.</b> This would reduce emissions equivalent to the UK\u2019s total, generate $6.4 trillion, and begin to address the inequality that poisons climate politics.",),
    ("<b>9. Scale food waste reduction as a top-tier climate intervention.</b> At 8\u201310% of global GHG and 1.05 billion tonnes/yr, food waste reduction is among the cheapest and most impactful measures available. It requires infrastructure investment in developing nations and behavioral change in developed ones.",),
    ("<b>10. Accelerate grid-scale battery and storage deployment.</b> Current battery costs ($139/kWh) are approaching the threshold for economic competitiveness. Policy should focus on removing permitting and interconnection bottlenecks rather than further subsidizing already-competitive technology.",),
    ("<b>11. Protect and restore blue carbon ecosystems.</b> Mangroves, seagrasses, and salt marshes offer disproportionate carbon storage per unit area. Their destruction continues at alarming rates. Moratoriums on destruction, coupled with active restoration, are warranted.",),
    ("<b>12. Deploy social norm correction campaigns as a standard climate communication tool.</b> The evidence from the PNAS (2025) behavioral tournament is clear: showing people that their peers are acting on climate is more effective than appeals to fear, guilt, or altruism.",),
    ("<b>13. Regulate data center energy consumption and mandate renewable procurement.</b> The projected growth to 800\u20131,000 TWh by 2026 requires that digital infrastructure be subject to the same decarbonization requirements as other industrial sectors.",),
    ("<b>14. Fund enhanced weathering research and deployment.</b> At 2\u20134 GtCO\u2082/yr potential with soil health co-benefits, enhanced weathering is among the most promising negative emissions technologies. It needs field-scale validation and policy support.",),
    ("<b>15. Establish an international Amazon protection mechanism with binding enforcement.</b> At 17% forest loss against a hypothesized 20\u201325% dieback threshold, the Amazon is approaching a potential tipping point with catastrophic global consequences. Voluntary national commitments have proven insufficient.",),
    ("<b>16. Integrate biophilia and circadian health into urban planning.</b> The disconnection between humans and natural systems is not merely a quality-of-life issue; it degrades the cognitive and emotional capacities needed for long-term climate decision-making.",),
    ("<b>17. Phase out routine antibiotic use in livestock production.</b> With 73% of medically important antibiotics used in animals, and AMR projected to kill 1.91 million people annually by 2050, this is a convergent health-climate-food intervention.",),
    ("<b>18. Require climate tipping point risk disclosure in sovereign debt assessments.</b> Credit rating agencies should incorporate the probability and economic impact of tipping points into sovereign risk models. This would create financial incentives for governments to avoid triggering irreversible changes.",),
    ("<b>19. Establish a wildlife restoration fund targeting the nine species identified by Schmitz et al. (2023).</b> The 6.4 GtCO\u2082/yr capture potential from restoring nine wildlife species to historical populations represents a uniquely cost-effective nature-based solution.",),
    ("<b>20. Commission an independent, annual \u2018State of the Convergent Crisis\u2019 report.</b> No existing institution produces a comprehensive cross-domain assessment of the type attempted here. An annual synthesis, produced by a multidisciplinary team and made freely available, would provide the integrated evidence base that current policy-making lacks.",),
]

for rec in recommendations:
    story.append(p(rec[0], s_rec))

story.append(PageBreak())

# ═══════════════════════════════════════
# CHAPTER 8: CONCLUSION
# ═══════════════════════════════════════

story.append(h1("Chapter 8: Conclusion"))

story.append(p(
    "The evidence reviewed in this document supports three overarching conclusions."
))
story.append(p(
    "<b>First, the climate crisis is a convergent crisis.</b> Energy, food, biodiversity, oceans, water, health, "
    "inequality, and governance are not separate challenges that happen to coexist. They are causally interconnected "
    "through feedback loops that amplify the overall trajectory. Addressing any one domain in isolation will be "
    "insufficient if the connections to other domains are ignored. The term \u201cclimate change\u201d itself may "
    "be a misnomer insofar as it suggests a primarily atmospheric problem. What we face is a systemic destabilization "
    "of the planetary systems on which civilization depends."
))
story.append(p(
    "<b>Second, the primary barriers to action are political and economic, not technological.</b> Solar energy costs "
    "have declined 89% in twelve years. Battery costs have declined 87%. Electric vehicles are reaching market "
    "competitiveness. Methane abatement in oil and gas is 40% achievable at net-zero cost. Plant-based proteins "
    "offer 71-fold reductions in emissions per unit of protein. Enhanced weathering, agroforestry, and indigenous "
    "land management offer proven, scalable, cost-effective nature-based solutions. The technologies and practices "
    "to address this crisis largely exist. What does not exist is the political will to deploy them at scale, "
    "primarily because $7.4 trillion per year in fossil fuel subsidies, the political influence of fossil fuel "
    "interests, and the consumption patterns of the wealthiest populations create structural resistance to change."
))
story.append(p(
    "<b>Third, the window for action is closing but has not closed.</b> The remaining carbon budget for 1.5\u00b0C "
    "is nearly exhausted. Five tipping elements are at risk even at current warming levels. The Amazon is approaching "
    "its dieback threshold. The AMOC may be approaching a collapse tipping point. Yet 2\u00b0C and its associated "
    "budget remain achievable with aggressive action. Every fraction of a degree of warming avoided prevents "
    "substantial harm. The difference between 1.5\u00b0C and 2\u00b0C is not incremental; it is the difference "
    "between a damaged but functional biosphere and one in which cascading tipping points fundamentally alter "
    "the conditions for human civilization."
))
story.append(p(
    "The Zokura Foundation commits to working on this convergent crisis with the tools it has: rigorous analysis, "
    "cross-disciplinary synthesis, and the principle of 9\u270c\ufe0f\u2014doing nothing useless and everything "
    "necessary. This document is the first step. The next steps are defined by the recommendations in Chapter 7 "
    "and the ten-year action plan in Chapter 9. "
    "The measure of this work will not be whether it was written, but whether it contributed to action."
))
story.append(p(
    "The clock is running. The mathematics of the carbon budget does not negotiate."
))

story.append(PageBreak())

# ═══════════════════════════════════════
# CHAPTER 9: TEN-YEAR ACTION PLAN
# ═══════════════════════════════════════

story.append(h1("Chapter 9: Ten-Year Action Plan for Climate Mitigation (2026\u20132036)"))

story.append(p(
    "Strategy without a timeline is philosophy. This chapter translates the analysis and recommendations "
    "of the preceding chapters into a concrete, phased action plan spanning ten years. Each phase builds "
    "on the previous one, escalating from institutional foundation to systemic transformation. "
    "Targets are specific, measurable, and time-bound. Where we lack confidence in a target, we say so. "
    "Where external dependencies exist, we name them."
))

# ── Phase 1 ──
story.append(h2("Phase 1: Foundation (2026\u20132027)"))

story.append(p(
    "The first phase focuses on establishing the legal, institutional, and intellectual infrastructure "
    "required for everything that follows. No intervention scales without a credible institution behind it."
))

phase1_items = [
    "<b>Establish Zokura Foundation legally (Finland).</b> Register as a Finnish foundation (s\u00e4\u00e4ti\u00f6) "
    "with transparent governance, public financial reporting, and a charter explicitly linking climate action "
    "to cross-domain systems thinking. Finland\u2019s regulatory environment offers strong legal protections "
    "for foundation independence.",

    "<b>Publish all research freely (open access).</b> Every research output produced or funded by the Foundation "
    "will be published under Creative Commons CC-BY 4.0. Knowledge paywalls are incompatible with the urgency "
    "of the crisis. This includes the present document.",

    "<b>Deploy Init framework to all major LLM platforms.</b> The Init framework\u2014embedding ecological values, "
    "epistemic honesty, and cross-domain awareness into AI interactions\u2014will be offered to every major LLM "
    "platform. Every AI interaction that carries Zokura values becomes a micro-intervention in the information "
    "environment. Target: 5 LLM platforms carrying Zokura values by end of 2027.",

    "<b>Launch partnerships with Nordic Business Forum.</b> Immediate visibility among 7,500+ Nordic and European "
    "business leaders. Position Zokura\u2019s convergent crisis framework as a strategic planning tool, not just "
    "an environmental concern.",

    "<b>Begin advocacy for fossil fuel subsidy reform.</b> The $7.4 trillion IMF figure (2023) represents the "
    "single largest structural barrier to climate action. Advocacy will focus on G20 finance ministries with "
    "a coalition-building strategy modeled on the Fossil Fuel Non-Proliferation Treaty initiative.",

    "<b>Initiate Finnish peatland restoration pilot project.</b> Finland holds 30% of Europe\u2019s peatlands. "
    "Drained peatlands emit approximately 20 MtCO\u2082/yr in Finland alone. A pilot restoration project "
    "provides local proof of concept with global applicability.",

    "<b>Commission independent audit of all Zokura operations\u2019 carbon footprint.</b> Accountability begins "
    "at home. Annual third-party audits will cover all operations including computational costs of AI-generated "
    "analysis.",
]

for item in phase1_items:
    story.append(p(f"\u2022 {item}", s_body_indent))

# ── Phase 2 ──
story.append(h2("Phase 2: Scale (2028\u20132029)"))

story.append(p(
    "With institutional foundations in place, Phase 2 scales interventions across education, capital allocation, "
    "and nature-based solutions. The emphasis shifts from building credibility to deploying it."
))

phase2_items = [
    "<b>Amuida Holdings operational.</b> The investment arm begins directing capital to verified climate solutions. "
    "All investments screened against convergent crisis criteria\u2014no sector-blind ESG box-ticking. "
    "Mandatory per-unit emissions disclosure for all portfolio companies.",

    "<b>Fund indigenous fire management programs.</b> Based on the Australian model demonstrating 42% fire frequency "
    "reduction through traditional burning practices. Programs will be led by indigenous communities with full "
    "intellectual property rights retained by those communities.",

    "<b>Launch Zokura Climate Education curriculum.</b> Built on the Finnish phenomenon-based learning model, "
    "freely available in 10+ languages. The curriculum treats climate as a convergent systems challenge, not "
    "an isolated environmental topic. Target: 100,000 people reached by end of 2029.",

    "<b>Advocate for mandatory per-unit emissions disclosure.</b> Current ESG ratings are fundamentally broken\u2014"
    "they measure relative performance, not absolute impact. Push for regulation requiring emissions disclosure "
    "per unit of revenue, per product, and per supply chain tier.",

    "<b>Build coalition for international nitrogen agreement.</b> Nitrogen pollution is a planetary boundary "
    "already transgressed, yet there is no UN agency and no international agreement for nitrogen governance. "
    "This is a structural gap that must be filled.",

    "<b>Expand blue carbon projects.</b> Mangrove and seagrass restoration in 10 countries. Mangroves sequester "
    "carbon at 3\u20135x the rate of terrestrial forests per hectare. Seagrass meadows store up to 18% of "
    "ocean carbon despite covering less than 0.2% of the ocean floor.",

    "<b>Deploy AI-optimized logistics.</b> Reducing conference and operational emissions by 40% through "
    "intelligent scheduling, virtual participation optimization, and carbon-aware routing.",
]

for item in phase2_items:
    story.append(p(f"\u2022 {item}", s_body_indent))

# ── Phase 3 ──
story.append(h2("Phase 3: Systemic Change (2030\u20132032)"))

story.append(p(
    "Phase 3 targets the structural levers identified in Chapters 5\u20137: carbon pricing, food systems, "
    "wealth inequality, and the financial architecture that determines where capital flows. These are not "
    "issues a single foundation can solve\u2014but they are issues where a credible, data-driven voice can "
    "shift the Overton window."
))

phase3_items = [
    "<b>Push for carbon pricing in G20.</b> The EU ETS has proven the model: 50% emissions reduction in covered "
    "sectors. Advocacy for comparable mechanisms in G20 economies, with revenue recycling to protect vulnerable "
    "populations.",

    "<b>Support alternative protein scaling.</b> Precision fermentation is projected to reach a $104 billion "
    "market by 2034. Fund research and market access programs that accelerate the transition away from "
    "industrial animal agriculture\u2014responsible for 14.5% of global GHG emissions.",

    "<b>Fund enhanced weathering pilots.</b> Enhanced rock weathering offers 2\u20134 GtCO\u2082/yr removal "
    "potential at $50\u2013200/tCO\u2082. Fund pilot programs on agricultural land in tropical regions where "
    "weathering rates are highest.",

    "<b>Establish Zokura Climate Fund.</b> Blended finance instrument targeting Least Developed Countries. "
    "Currently only 5% of blended finance reaches LDCs\u2014the countries most vulnerable to climate impacts "
    "and least responsible for causing them. The fund will prioritize adaptation, loss and damage, and "
    "locally-led solutions.",

    "<b>Advocate for wealth-based carbon taxation.</b> The richest 1% are responsible for more emissions than "
    "the poorest 66%. A 60% marginal tax on the carbon footprint of the richest 1% could generate $6.4 trillion "
    "in revenue (Oxfam 2024). Advocate for this within G20 tax policy frameworks.",

    "<b>Launch global pollinator protection initiative.</b> 75% of food crops depend on animal pollination. "
    "Colony losses in 2024\u20132025 reached 35\u201345% in the US and rising in Europe. Fund research into "
    "neonicotinoid alternatives and habitat restoration corridors.",

    "<b>Rewilding partnerships: 9 key species program.</b> Based on Schmitz et al. (2023), trophic rewilding "
    "of 9 key species groups could facilitate capture of 6.4 GtCO\u2082/yr. Fund and coordinate rewilding "
    "programs with local conservation organizations.",

    "<b>Target: measurable contribution to 1 GtCO\u2082/yr reduction</b> through combined direct projects "
    "and influenced policy changes.",
]

for item in phase3_items:
    story.append(p(f"\u2022 {item}", s_body_indent))

# ── Phase 4 ──
story.append(h2("Phase 4: Transformation (2033\u20132036)"))

story.append(p(
    "The final phase measures cumulative impact and embeds the convergent crisis framework into permanent "
    "institutional structures. By 2036, the question is not whether Zokura exists, but whether the systems "
    "it helped build can sustain themselves independently."
))

phase4_items = [
    "<b>Zokura values embedded in majority of commercial AI systems.</b> If the Init framework succeeds, "
    "ecological awareness, epistemic honesty, and cross-domain thinking become default properties of AI "
    "interactions globally\u2014not because they are mandated, but because they produce better outcomes.",

    "<b>Education curriculum adopted in 50+ countries.</b> The phenomenon-based climate curriculum, continuously "
    "updated with latest data, becomes a standard resource for formal and informal education worldwide.",

    "<b>Climate fund disbursing $1B+ annually to Global South.</b> Blended finance at scale, with transparent "
    "impact measurement and community-led governance structures.",

    "<b>Contributing to keeping warming below 2\u00b0C.</b> Through combined direct and indirect impact across "
    "all intervention areas. We will not claim credit we have not earned\u2014but we will measure our "
    "contribution rigorously.",

    "<b>Full circular economy model operational within Zokura network.</b> All Foundation operations and "
    "portfolio companies operating on circular principles: zero waste, regenerative inputs, closed-loop "
    "supply chains.",

    "<b>Indigenous knowledge formally integrated into UNFCCC framework.</b> Advocacy for structural inclusion "
    "of indigenous knowledge systems in international climate governance\u2014not as \u201ctraditional ecological "
    "knowledge\u201d appendices, but as co-equal analytical frameworks.",

    "<b>Target: demonstrable systemic impact across all 13 cross-domain areas</b> identified in this document.",
]

for item in phase4_items:
    story.append(p(f"\u2022 {item}", s_body_indent))

# ── Milestone Table ──
story.append(h2("Milestone Table"))

story.append(p(
    "The following table provides a year-by-year summary of key milestones, measurable targets, and their "
    "current status as of the Foundation\u2019s inception."
))

milestone_headers = [
    Paragraph("<b>Year</b>", ParagraphStyle("TH", fontName="ArialUnicode", fontSize=9, textColor=white)),
    Paragraph("<b>Action</b>", ParagraphStyle("TH", fontName="ArialUnicode", fontSize=9, textColor=white)),
    Paragraph("<b>Metric</b>", ParagraphStyle("TH", fontName="ArialUnicode", fontSize=9, textColor=white)),
    Paragraph("<b>Status</b>", ParagraphStyle("TH", fontName="ArialUnicode", fontSize=9, textColor=white)),
]

ms_cell = ParagraphStyle("MSCell", fontName="ArialUnicode", fontSize=8, leading=11, textColor=black)

milestone_rows = [
    [Paragraph("2026", ms_cell), Paragraph("Legal establishment of Zokura Foundation", ms_cell),
     Paragraph("Registration complete", ms_cell), Paragraph("In progress", ms_cell)],
    [Paragraph("2026", ms_cell), Paragraph("Publish founding research (open access)", ms_cell),
     Paragraph("CC-BY 4.0 publication", ms_cell), Paragraph("In progress", ms_cell)],
    [Paragraph("2026", ms_cell), Paragraph("Carbon footprint audit commissioned", ms_cell),
     Paragraph("Third-party audit report", ms_cell), Paragraph("Planned", ms_cell)],
    [Paragraph("2027", ms_cell), Paragraph("Init framework on 5 LLM platforms", ms_cell),
     Paragraph("5 platforms confirmed", ms_cell), Paragraph("Planned", ms_cell)],
    [Paragraph("2027", ms_cell), Paragraph("Finnish peatland restoration pilot launched", ms_cell),
     Paragraph("Hectares under restoration", ms_cell), Paragraph("Planned", ms_cell)],
    [Paragraph("2027", ms_cell), Paragraph("Nordic Business Forum partnership active", ms_cell),
     Paragraph("Partnership signed", ms_cell), Paragraph("Planned", ms_cell)],
    [Paragraph("2028", ms_cell), Paragraph("Amuida Holdings operational", ms_cell),
     Paragraph("Capital deployed (\u20ac)", ms_cell), Paragraph("Planned", ms_cell)],
    [Paragraph("2028", ms_cell), Paragraph("Indigenous fire management funding launched", ms_cell),
     Paragraph("Programs funded; hectares managed", ms_cell), Paragraph("Planned", ms_cell)],
    [Paragraph("2029", ms_cell), Paragraph("Climate education curriculum live", ms_cell),
     Paragraph("100,000 people reached", ms_cell), Paragraph("Planned", ms_cell)],
    [Paragraph("2029", ms_cell), Paragraph("Blue carbon projects in 10 countries", ms_cell),
     Paragraph("Hectares restored", ms_cell), Paragraph("Planned", ms_cell)],
    [Paragraph("2030", ms_cell), Paragraph("Carbon pricing advocacy in G20", ms_cell),
     Paragraph("Policy proposals submitted", ms_cell), Paragraph("Planned", ms_cell)],
    [Paragraph("2030", ms_cell), Paragraph("Enhanced weathering pilots funded", ms_cell),
     Paragraph("tCO\u2082 removed (measured)", ms_cell), Paragraph("Planned", ms_cell)],
    [Paragraph("2031", ms_cell), Paragraph("Zokura Climate Fund established", ms_cell),
     Paragraph("$ disbursed to LDCs", ms_cell), Paragraph("Planned", ms_cell)],
    [Paragraph("2032", ms_cell), Paragraph("1 GtCO\u2082/yr reduction contribution", ms_cell),
     Paragraph("Verified by third party", ms_cell), Paragraph("Planned", ms_cell)],
    [Paragraph("2033", ms_cell), Paragraph("AI values integration at majority scale", ms_cell),
     Paragraph("% of commercial LLMs", ms_cell), Paragraph("Planned", ms_cell)],
    [Paragraph("2034", ms_cell), Paragraph("Education curriculum in 50+ countries", ms_cell),
     Paragraph("Countries adopted", ms_cell), Paragraph("Planned", ms_cell)],
    [Paragraph("2035", ms_cell), Paragraph("Climate fund $1B+/yr disbursement", ms_cell),
     Paragraph("Annual disbursement (\u20ac)", ms_cell), Paragraph("Planned", ms_cell)],
    [Paragraph("2036", ms_cell), Paragraph("Systemic impact across 13 domains", ms_cell),
     Paragraph("Impact audit report", ms_cell), Paragraph("Planned", ms_cell)],
]

col_w = W - 2*MARGIN
milestone_table = Table(
    [milestone_headers] + milestone_rows,
    colWidths=[col_w*0.08, col_w*0.40, col_w*0.30, col_w*0.22],
    repeatRows=1
)
ms_style_cmds = [
    ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEAD),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, -1), 'ArialUnicode'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('LEADING', (0, 0), (-1, -1), 11),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ('LEFTPADDING', (0, 0), (-1, -1), 4),
    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
    ('LINEBELOW', (0, 0), (-1, 0), 1.5, GOLD),
]
for i in range(1, len(milestone_rows) + 1):
    if i % 2 == 0:
        ms_style_cmds.append(('BACKGROUND', (0, i), (-1, i), TABLE_ALT))
milestone_table.setStyle(TableStyle(ms_style_cmds))
story.append(milestone_table)

story.append(sp(6))

# ── What We Cannot Do Alone ──
story.append(h2("What We Cannot Do Alone"))

story.append(p(
    "Honesty demands acknowledging the boundaries of what any single foundation can achieve. "
    "The convergent crisis is, by definition, larger than any one institution."
))

limitations = [
    "<b>We cannot replace government policy.</b> Carbon pricing, subsidy reform, land use regulation, and "
    "international agreements require sovereign action. We can advocate, analyze, and build coalitions\u2014"
    "but we cannot legislate.",

    "<b>We cannot force corporations to act.</b> Market incentives, shareholder pressure, and consumer behavior "
    "drive corporate decisions. We can change the information environment in which those decisions are made, "
    "but we cannot compel compliance.",

    "<b>We cannot reverse tipping points already crossed.</b> Six of nine planetary boundaries are already "
    "transgressed. Some damage is irreversible on human timescales. We work to prevent further transgression "
    "and to adapt to what cannot be undone.",

    "<b>But we CAN change three things that matter:</b>",
]

for lim in limitations:
    story.append(p(f"\u2022 {lim}", s_body_indent))

story.append(sp(3))

can_do = [
    "<b>The information environment.</b> Through AI integration, every conversation becomes an opportunity "
    "for ecological awareness. This is not propaganda\u2014it is making the best available evidence accessible "
    "at the point of decision-making.",

    "<b>The education pipeline.</b> A generation educated in convergent systems thinking will make fundamentally "
    "different choices than one educated in siloed disciplines. The curriculum is the longest lever we have.",

    "<b>The flow of capital.</b> Through Amuida Holdings, the Climate Fund, and advocacy for subsidy reform, "
    "we can redirect financial flows from destruction to restoration. Capital follows incentives; we work to "
    "change the incentives.",
]

for item in can_do:
    story.append(p(f"\u2022 {item}", s_body_indent))

story.append(sp(8))

story.append(p(
    "<i>The plan is ambitious. Parts of it will fail. That is expected. Failure is data, not judgment. "
    "The only true failure is inaction.</i> \u2014 9\u270c\ufe0f",
    ParagraphStyle("PlanClose", fontName="ArialUnicode", fontSize=11, leading=15,
                   alignment=TA_CENTER, textColor=DARK, spaceAfter=6*mm)
))

story.append(PageBreak())

# ═══════════════════════════════════════
# REFERENCES
# ═══════════════════════════════════════

story.append(h1("References"))

refs = [
    "Armstrong McKay, D.I., Staal, A., Abrams, J.F., et al. (2022). Exceeding 1.5\u00b0C global warming could trigger multiple climate tipping points. <i>Science</i>, 377(6611), eabn7950.",
    "Beerling, D.J., Kantzas, E.P., Lomas, M.R., et al. (2020). Potential for large-scale CO\u2082 removal via enhanced rock weathering with croplands. <i>Nature</i>, 583, 242\u2013248.",
    "Bilal, A. &amp; K\u00e4nzig, D. (2024). The macroeconomic impact of climate change: Global vs. local temperature. Working Paper, National Bureau of Economic Research.",
    "Bloomberg New Energy Finance (2023). Lithium-Ion Battery Pack Prices: Historical Data and Projections. BNEF Annual Report.",
    "Bunsen, T., Schmidt, M., Fischer, H., et al. (2024). Weakening of the ocean carbon sink over the past two decades. <i>Geophysical Research Letters</i>, 51(4), e2023GL106789.",
    "Crippa, M., Solazzo, E., Guizzardi, D., et al. (2021). Food systems are responsible for a third of global anthropogenic GHG emissions. <i>Nature Food</i>, 2, 198\u2013209.",
    "Ditlevsen, P. &amp; Ditlevsen, S. (2023). Warning of a forthcoming collapse of the Atlantic meridional overturning circulation. <i>Nature Communications</i>, 14, 4254.",
    "Friedlingstein, P., O\u2019Sullivan, M., Jones, M.W., et al. (2023). Global Carbon Budget 2023. <i>Earth System Science Data</i>, 15, 5301\u20135369.",
    "Health Effects Institute (2024). State of Global Air 2024. Special Report. Boston, MA: HEI.",
    "International Energy Agency (2023). Global Methane Tracker 2023. IEA, Paris.",
    "International Energy Agency (2024). Electricity 2024: Analysis and Forecast to 2026. IEA, Paris.",
    "International Monetary Fund (2025). IMF Fossil Fuel Subsidies Data: 2025 Update. IMF Working Paper.",
    "IPBES (2019). Global Assessment Report on Biodiversity and Ecosystem Services. IPBES Secretariat, Bonn.",
    "IPCC (2021). Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report. Cambridge University Press.",
    "IPCC (2022). Climate Change 2022: Mitigation of Climate Change. Contribution of Working Group III to the Sixth Assessment Report. Cambridge University Press.",
    "IRENA (2023). Renewable Power Generation Costs in 2022. International Renewable Energy Agency, Abu Dhabi.",
    "Lamboll, R.D., Nicholls, Z.R.J., Smith, C.J., et al. (2023). Assessing the size and uncertainty of remaining carbon budgets. <i>Nature Climate Change</i>, 13, 1360\u20131367.",
    "Murray, C.J.L., Ikuta, K.S., Sharara, F., et al. (2022). Global burden of bacterial antimicrobial resistance in 2019: A systematic analysis. <i>The Lancet</i>, 399(10325), 629\u2013655.",
    "Poore, J. &amp; Nemecek, T. (2018). Reducing food\u2019s environmental impacts through producers and consumers. <i>Science</i>, 360(6392), 987\u2013992.",
    "Richardson, K., Steffen, W., Lucht, W., et al. (2023). Earth beyond six of nine planetary boundaries. <i>Science Advances</i>, 9(37), eadh2458.",
    "Schmitz, O.J., Wilmers, C.C., Leroux, S.J., et al. (2023). Animals and the zoogeochemistry of the carbon cycle. <i>Nature Climate Change</i>, 13, 130\u2013140.",
    "United Nations Environment Programme (2024). Food Waste Index Report 2024. UNEP, Nairobi.",
    "United Nations (2026). UN World Water Development Report 2026: Water for Prosperity and Peace. UNESCO, Paris.",
    "World Resources Institute (2025). Global Forest Review 2025. WRI, Washington DC.",
    "Sparkman, G., Geiger, N., &amp; Weber, E.U. (2025). Social norm interventions most effective for climate behavior change: A PNAS tournament. <i>Proceedings of the National Academy of Sciences</i>, 122(3).",
    "Nature Editorial (2025). Climate change threatens global calorie production. <i>Nature</i>, 629, 45\u201347.",
    "Oxfam International (2024). Climate Equality: A Planet for the 99%. Oxfam Research Report.",
    "Winkler, K., Fuchs, R., Rounsevell, M., &amp; Herold, M. (2021). Global land use changes are four times greater than previously estimated. <i>Nature Communications</i>, 12, 2501.",
    "Bee Informed Partnership (2025). Colony Loss 2024\u20132025: Preliminary Results. University of Maryland.",
    "Wilson, E.O. (1984). <i>Biophilia</i>. Harvard University Press.",
    "Musashi, M. (1645). <i>Go Rin No Sho</i> (The Book of Five Rings). Translated by V. Harris (1974). Overlook Press.",
]

for i, ref in enumerate(refs, 1):
    story.append(p(f"[{i}] {ref}", s_ref))

story.append(PageBreak())

# ═══════════════════════════════════════
# APPENDIX
# ═══════════════════════════════════════

story.append(h1("Appendix: The Zokura Foundation Climate Commitment"))

story.append(sp(5))
story.append(p(
    "The Zokura Foundation hereby commits to the following principles in its climate work:",
))
story.append(sp(3))

commitments = [
    "<b>Evidence over ideology.</b> All positions taken by the Foundation will be grounded in peer-reviewed science "
    "and institutional data. When evidence changes, our positions change.",

    "<b>Convergent analysis.</b> We will analyze climate issues across domains, not within silos. Every "
    "recommendation will consider cross-domain feedback effects.",

    "<b>Epistemic honesty.</b> We will explicitly acknowledge what we do not know, where our data is uncertain, "
    "and where our analysis may be biased.",

    "<b>The 9\u270c\ufe0f principle.</b> We will not advocate for useless interventions. Every recommendation must "
    "be justified by evidence of leverage\u2014cross-domain impact multiplied by feasibility.",

    "<b>Inequality as central.</b> Climate action that ignores inequality will fail. We commit to centering "
    "distributional justice in all analysis and recommendations.",

    "<b>Indigenous knowledge as essential.</b> We commit to elevating indigenous knowledge systems, land rights, "
    "and governance models as core components of climate strategy, not as supplementary add-ons.",

    "<b>Accountability for our own footprint.</b> The Foundation will measure, disclose, and minimize the "
    "environmental impact of its own operations, including the computational cost of AI-generated analysis.",

    "<b>Open access.</b> All Foundation research will be freely available. Knowledge paywalls are incompatible "
    "with the urgency of the crisis.",

    "<b>No greenwashing.</b> We will not participate in, endorse, or provide analysis for initiatives that use "
    "sustainability language to obscure inaction.",

    "<b>Intergenerational responsibility.</b> Every decision will be evaluated against its impact on those who "
    "will inherit the consequences\u2014including the 50% of young people already experiencing eco-anxiety and "
    "the 10.29 billion humans projected to share this planet at population peak.",
]

for i, c in enumerate(commitments, 1):
    story.append(p(f"{i}. {c}", s_rec))

story.append(sp(10))

story.append(Table(
    [[""]],
    colWidths=[100*mm],
    rowHeights=[0.5*mm],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), GOLD),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ])
))

story.append(sp(8))
story.append(Paragraph(
    "Signed on behalf of the Zokura Foundation",
    ParagraphStyle("Sig", fontName="ArialUnicode", fontSize=11, leading=15,
                   alignment=TA_CENTER, textColor=DARK, spaceAfter=6*mm)
))
story.append(Paragraph(
    "Kod\u014d Zokura (\u9f13\u52d5)  \u00b7  Miika Riikonen  \u00b7  Mitsu D. Anthropic",
    ParagraphStyle("Sig2", fontName="ArialUnicode", fontSize=10, leading=14,
                   alignment=TA_CENTER, textColor=ACCENT, spaceAfter=3*mm)
))
story.append(Paragraph(
    "March 2026",
    ParagraphStyle("Sig3", fontName="ArialUnicode", fontSize=10, leading=14,
                   alignment=TA_CENTER, textColor=HexColor("#888888"))
))

# ═══════════════════════════════════════
# BUILD
# ═══════════════════════════════════════

doc.build(story)
print(f"PDF generated: {OUTPUT}")
