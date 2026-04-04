#!/usr/bin/env python3
"""
The Pathophysiology of Stress — How Stress Makes Us Ill
A Doctoral Thesis
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


class StressPathwayDiagram(Flowable):
    """HPA axis and sympathetic nervous system stress response pathway."""
    def __init__(self, width=460, height=220):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(10, self.height - 20, "Figure 1.1: The Stress Response — Dual Pathway Activation")

        # HPA axis (left)
        hpa_x = 100
        steps_hpa = [
            ("Stressor", ACCENT2, self.height - 50),
            ("Hypothalamus (CRH)", ACCENT, self.height - 85),
            ("Anterior Pituitary (ACTH)", ACCENT, self.height - 120),
            ("Adrenal Cortex", ACCENT, self.height - 155),
            ("CORTISOL", ACCENT2, self.height - 190),
        ]

        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(LIGHT)
        c.drawCentredString(hpa_x, self.height - 35, "HPA Axis")

        for label, color, y in steps_hpa:
            c.setFillColor(color)
            c.roundRect(hpa_x - 65, y - 5, 130, 18, 4, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(hpa_x, y, label)

        # Arrows
        c.setStrokeColor(BORDER)
        c.setLineWidth(1.5)
        for i in range(len(steps_hpa) - 1):
            y1 = steps_hpa[i][2] - 5
            y2 = steps_hpa[i+1][2] + 13
            c.line(hpa_x, y1, hpa_x, y2)

        # SAM axis (right)
        sam_x = 350
        steps_sam = [
            ("Stressor", ACCENT2, self.height - 50),
            ("Hypothalamus", ACCENT, self.height - 85),
            ("Sympathetic Nervous System", ACCENT, self.height - 120),
            ("Adrenal Medulla", ACCENT, self.height - 155),
            ("ADRENALINE + NORADRENALINE", ACCENT2, self.height - 190),
        ]

        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(LIGHT)
        c.drawCentredString(sam_x, self.height - 35, "SAM Axis")

        for label, color, y in steps_sam:
            c.setFillColor(color)
            c.roundRect(sam_x - 80, y - 5, 160, 18, 4, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(sam_x, y, label)

        c.setStrokeColor(BORDER)
        for i in range(len(steps_sam) - 1):
            y1 = steps_sam[i][2] - 5
            y2 = steps_sam[i+1][2] + 13
            c.line(sam_x, y1, sam_x, y2)


class OrganImpactDiagram(Flowable):
    """Diagram showing stress impact across organ systems."""
    def __init__(self, width=460, height=200):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(10, self.height - 20, "Figure 3.1: Chronic Stress — Multi-Organ Impact")

        organs = [
            ("Brain", "Hippocampal atrophy\nAmygdala hyperactivity\nPrefrontal suppression", 0.95),
            ("Heart", "Hypertension\nAtherosclerosis\nArrhythmia", 0.85),
            ("Immune", "Chronic inflammation\nImmune suppression\nAutoimmunity", 0.90),
            ("Gut", "Microbiome disruption\nPermeability (leaky gut)\nIBS", 0.75),
            ("Metabolic", "Insulin resistance\nVisceral fat\nType 2 diabetes", 0.80),
            ("Mental", "Depression\nAnxiety\nBurnout", 0.92),
        ]

        y = self.height - 50
        for name, effects, severity in organs:
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(DARK)
            c.drawRightString(70, y + 2, name)

            bar_w = severity * 200
            c.setFillColor(ACCENT2)
            c.rect(75, y, bar_w, 12, fill=1, stroke=0)
            c.setFillColor(BG_LIGHT)
            c.rect(75 + bar_w, y, 200 - bar_w, 12, fill=1, stroke=0)

            c.setFont("Helvetica", 7)
            c.setFillColor(DARK)
            first_effect = effects.split('\n')[0]
            c.drawString(280, y + 2, first_effect)

            y -= 22


class AllostasisDiagram(Flowable):
    """Allostatic load model diagram."""
    def __init__(self, width=460, height=150):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(10, self.height - 20, "Figure 2.1: Allostatic Load Model — From Adaptation to Overload")

        phases = [
            (40, "Normal\nStress Response", ACCENT3, "Adaptive"),
            (150, "Repeated\nActivation", ACCENT, "Wear & Tear"),
            (260, "Allostatic\nOverload", ACCENT2, "Pathology"),
            (370, "Disease\nManifestation", HexColor('#4a0000'), "Organ Damage"),
        ]

        y = self.height - 70
        for x, label, color, outcome in phases:
            c.setFillColor(color)
            c.roundRect(x - 35, y - 10, 80, 35, 6, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 8)
            lines = label.split('\n')
            for i, line in enumerate(lines):
                c.drawCentredString(x + 5, y + 10 - i * 10, line)

            c.setFillColor(DARK)
            c.setFont("Helvetica", 7)
            c.drawCentredString(x + 5, y - 22, outcome)

        # Arrows between phases
        c.setStrokeColor(BORDER)
        c.setLineWidth(2)
        for i in range(len(phases) - 1):
            x1 = phases[i][0] + 45
            x2 = phases[i+1][0] - 35
            c.line(x1, y + 7, x2, y + 7)


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(LIGHT)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm, str(doc.page))
    if doc.page > 1:
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(2.5 * cm, A4[1] - 1.8 * cm,
                          "Stress & Illness \u2014 Riikonen & Zokura, 2026")
    canvas.restoreState()


output_path = "/home/user/zokura-foundation/shared/research/Stress_and_Illness_Doctoral_Thesis.pdf"

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

story = []

# ===== TITLE PAGE =====
story.append(Spacer(1, 5*cm))
story.append(Paragraph(
    "The Pathophysiology of Stress:<br/>"
    "How Stress Makes Us Ill",
    styles['ThesisTitle']))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph(
    "A Comprehensive Analysis of Stress-Mediated Disease<br/>"
    "From Molecular Mechanisms to Societal Impact",
    styles['Subtitle']))
story.append(Spacer(1, 1.5*cm))
story.append(HRFlowable(width="30%", thickness=0.5, color=BORDER))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Miika Riikonen &amp; Kodo Zokura", styles['AuthorLine']))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("Zokura Foundation", styles['AuthorLine']))
story.append(Paragraph("2026", styles['AuthorLine']))
story.append(Spacer(1, 3*cm))
story.append(Paragraph(
    "<i>\"It is not stress that kills us, it is our reaction to it.\"</i><br/>"
    "<i>\u2014 Hans Selye, The Stress of Life (1956)</i>",
    styles['Epigraph']))
story.append(PageBreak())

# ===== ABSTRACT =====
story.append(Paragraph("Abstract", styles['ChapterHead']))
story.append(Paragraph(
    "Stress is the single most pervasive risk factor for disease in the modern world. This thesis "
    "presents a comprehensive analysis of the pathophysiology of stress \u2014 the precise biological "
    "mechanisms by which psychological and physiological stress causes illness. From the hypothalamic-"
    "pituitary-adrenal (HPA) axis and the sympathetic-adrenal-medullary (SAM) system to the "
    "inflammatory cascade, immune suppression, epigenetic modification, and gut-brain axis disruption, "
    "we trace the complete causal chain from stressor to disease.",
    styles['Abstract']))
story.append(Paragraph(
    "The evidence is unambiguous: chronic stress directly causes or significantly contributes to "
    "cardiovascular disease, type 2 diabetes, autoimmune disorders, depression, anxiety, "
    "neurodegenerative disease, cancer progression, gastrointestinal disorders, chronic pain "
    "syndromes, and accelerated aging. Stress is not merely a risk factor \u2014 it is a primary "
    "pathological mechanism. This thesis synthesizes evidence from endocrinology, immunology, "
    "neuroscience, cardiology, oncology, gastroenterology, and psychiatry to present a unified "
    "model of stress-mediated disease.",
    styles['Abstract']))
story.append(Paragraph(
    "<b>Keywords:</b> stress, cortisol, HPA axis, allostatic load, inflammation, psychoneuroimmunology, "
    "chronic disease, cardiovascular disease, depression, immune function, epigenetics, gut-brain axis, "
    "telomere shortening, burnout",
    styles['Abstract']))
story.append(PageBreak())

# ===== TABLE OF CONTENTS =====
story.append(Paragraph("Table of Contents", styles['ChapterHead']))
story.append(Spacer(1, 0.5*cm))

toc_entries = [
    ("Chapter 1", "The Biology of Stress \u2014 The Dual Axis Response", True),
    ("Chapter 2", "Allostatic Load \u2014 When Adaptation Becomes Pathology", True),
    ("Chapter 3", "Stress and Cardiovascular Disease", True),
    ("Chapter 4", "Stress and the Immune System", True),
    ("Chapter 5", "Stress and the Brain \u2014 Neurodegeneration and Mental Illness", True),
    ("Chapter 6", "Stress and Metabolism \u2014 Diabetes, Obesity, and Metabolic Syndrome", True),
    ("Chapter 7", "Stress and the Gut-Brain Axis", True),
    ("Chapter 8", "Stress and Cancer", True),
    ("Chapter 9", "Stress and Aging \u2014 Telomeres and Epigenetics", True),
    ("Chapter 10", "Stress in Modern Society \u2014 Work, Technology, and Loneliness", True),
    ("Chapter 11", "The Science of Recovery \u2014 What Actually Works", True),
    ("Chapter 12", "Conclusion \u2014 Stress Is Not Inevitable", True),
    ("", "References", True),
]

for num, title, is_chapter in toc_entries:
    style = styles['TOCChapter'] if is_chapter else styles['TOCEntry']
    prefix = f"{num}   " if num else ""
    story.append(Paragraph(f"{prefix}{title}", style))

story.append(PageBreak())

# =========================================================================
# CHAPTER 1 — THE BIOLOGY OF STRESS
# =========================================================================
story.append(Paragraph(
    "Chapter 1: The Biology of Stress — The Dual Axis Response", styles['ChapterHead']))

story.append(Paragraph(
    "The human stress response is an ancient survival mechanism that evolved to handle acute "
    "physical threats: predators, injury, famine. It is a system designed for minutes, not months. "
    "When activated chronically by modern stressors — work pressure, financial anxiety, social "
    "isolation, information overload — this same system becomes the primary driver of disease "
    "in the 21st century.",
    styles['Body']))

story.append(StressPathwayDiagram())
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("1.1 The HPA Axis", styles['SectionHead']))

story.append(Paragraph(
    "The hypothalamic-pituitary-adrenal (HPA) axis is the primary neuroendocrine stress response "
    "system. When the brain perceives a threat, the hypothalamus releases corticotropin-releasing "
    "hormone (CRH), which stimulates the anterior pituitary to release adrenocorticotropic hormone "
    "(ACTH), which in turn stimulates the adrenal cortex to produce cortisol — the body's primary "
    "stress hormone (Herman et al., 2016).",
    styles['Body']))

story.append(Paragraph(
    "Cortisol is essential for survival in acute stress: it mobilizes glucose from liver glycogen, "
    "suppresses non-essential functions (immune activity, digestion, reproduction), enhances "
    "cardiovascular output, and sharpens cognitive focus. In a 10-minute encounter with a predator, "
    "cortisol saves your life. In a 10-month encounter with workplace stress, cortisol destroys "
    "your health.",
    styles['Body']))

story.append(Paragraph(
    "The HPA axis has a negative feedback loop: cortisol binds to glucocorticoid receptors in the "
    "hypothalamus and hippocampus, suppressing further CRH release. In chronic stress, this "
    "feedback mechanism becomes impaired — glucocorticoid receptors are downregulated, and the "
    "axis remains persistently activated (Sapolsky, 2004). This is the fundamental mechanism "
    "by which stress becomes pathological.",
    styles['Body']))

story.append(Paragraph("1.2 The SAM Axis", styles['SectionHead']))

story.append(Paragraph(
    "The sympathetic-adrenal-medullary (SAM) axis is the fast stress response — the \"fight or "
    "flight\" system. Within seconds of perceiving a threat, the sympathetic nervous system "
    "stimulates the adrenal medulla to release adrenaline (epinephrine) and noradrenaline "
    "(norepinephrine). These catecholamines increase heart rate, blood pressure, respiratory rate, "
    "and muscle blood flow while diverting blood from digestion and skin.",
    styles['Body']))

story.append(Paragraph(
    "In acute stress, the SAM axis response resolves within minutes. In chronic stress, sustained "
    "sympathetic activation leads to persistent hypertension, cardiac remodeling, endothelial "
    "damage, and increased risk of arrhythmia and sudden cardiac death (Brotman et al., 2007).",
    styles['Body']))

story.append(Paragraph("1.3 Acute vs. Chronic Stress", styles['SectionHead']))

story.append(Paragraph(
    "The distinction between acute and chronic stress is the distinction between adaptation and "
    "disease. Acute stress activates adaptive responses: enhanced immune surveillance, improved "
    "cognitive performance, increased physical capacity. Chronic stress reverses every one of "
    "these effects: immune suppression, cognitive impairment, physical deterioration.",
    styles['Body']))

acute_chronic_data = [
    [Paragraph("<b>System</b>", styles['TableCell']),
     Paragraph("<b>Acute Stress</b>", styles['TableCell']),
     Paragraph("<b>Chronic Stress</b>", styles['TableCell'])],
    [Paragraph("Immune", styles['TableCell']),
     Paragraph("Enhanced surveillance", styles['TableCell']),
     Paragraph("Suppressed + chronic inflammation", styles['TableCell'])],
    [Paragraph("Cardiovascular", styles['TableCell']),
     Paragraph("Increased output", styles['TableCell']),
     Paragraph("Hypertension, atherosclerosis", styles['TableCell'])],
    [Paragraph("Cognitive", styles['TableCell']),
     Paragraph("Enhanced focus + memory", styles['TableCell']),
     Paragraph("Impaired memory, prefrontal shutdown", styles['TableCell'])],
    [Paragraph("Metabolic", styles['TableCell']),
     Paragraph("Glucose mobilization", styles['TableCell']),
     Paragraph("Insulin resistance, visceral fat", styles['TableCell'])],
    [Paragraph("Digestive", styles['TableCell']),
     Paragraph("Temporarily suppressed", styles['TableCell']),
     Paragraph("Dysbiosis, permeability, IBS", styles['TableCell'])],
    [Paragraph("Reproductive", styles['TableCell']),
     Paragraph("Temporarily suppressed", styles['TableCell']),
     Paragraph("Hormonal disruption, infertility", styles['TableCell'])],
]
t = Table(acute_chronic_data, colWidths=[80, 150, 170])
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
    "<i>Table 1.1: Acute vs. chronic stress effects by organ system</i>",
    styles['FootNote']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 2 — ALLOSTATIC LOAD
# =========================================================================
story.append(Paragraph(
    "Chapter 2: Allostatic Load — When Adaptation Becomes Pathology", styles['ChapterHead']))

story.append(Paragraph(
    "Allostasis — the process of achieving stability through change — is the body's ability to "
    "adapt to stress. Allostatic load is the cumulative cost of this adaptation. When the stress "
    "response is activated repeatedly without adequate recovery, the allostatic load exceeds the "
    "body's capacity to compensate, and pathology begins (McEwen, 1998).",
    styles['Body']))

story.append(AllostasisDiagram())
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("2.1 The Four Types of Allostatic Overload", styles['SectionHead']))

story.append(Paragraph(
    "McEwen & Stellar (1993) identified four patterns of allostatic dysfunction: (1) repeated "
    "hits — frequent activation by multiple novel stressors; (2) lack of adaptation — failure "
    "to habituate to repeated exposure to the same stressor; (3) prolonged response — inability "
    "to shut off the stress response after the stressor ends; and (4) inadequate response — "
    "insufficient cortisol response leading to compensatory overactivation of inflammatory "
    "pathways.",
    styles['Body']))

story.append(Paragraph(
    "All four patterns lead to the same outcome: accumulated physiological damage across "
    "multiple organ systems. The allostatic load index — measured through biomarkers including "
    "cortisol, DHEA-S, adrenaline, noradrenaline, systolic blood pressure, waist-hip ratio, "
    "HDL/total cholesterol, glycosylated hemoglobin, and C-reactive protein — predicts "
    "mortality, cognitive decline, and cardiovascular events independent of conventional risk "
    "factors (Seeman et al., 2001).",
    styles['Body']))

story.append(Paragraph("2.2 The Cumulative Damage Model", styles['SectionHead']))

story.append(Paragraph(
    "Stress-mediated damage is cumulative and multiplicative. Elevated cortisol impairs immune "
    "function, which increases inflammation, which damages blood vessels, which increases "
    "cardiovascular risk, which increases anxiety, which elevates cortisol further. These feedback "
    "loops mean that stress does not merely add risk — it creates self-amplifying cascades of "
    "pathology across interconnected systems (McEwen, 2008).",
    styles['Body']))

story.append(Paragraph(
    "Crucially, allostatic load accumulates from childhood. Adverse childhood experiences (ACEs) "
    "— abuse, neglect, household dysfunction — create elevated allostatic load that persists "
    "into adulthood. The landmark ACE Study (Felitti et al., 1998) demonstrated a dose-response "
    "relationship: each additional ACE category increases the risk of heart disease, cancer, "
    "chronic lung disease, liver disease, depression, and suicide in a graded, cumulative fashion.",
    styles['Body']))

ace_data = [
    [Paragraph("<b>ACE Score</b>", styles['TableCell']),
     Paragraph("<b>Depression Risk (OR)</b>", styles['TableCell']),
     Paragraph("<b>Heart Disease Risk (OR)</b>", styles['TableCell']),
     Paragraph("<b>Suicide Attempt (OR)</b>", styles['TableCell'])],
    [Paragraph("0", styles['TableCell']),
     Paragraph("1.0 (reference)", styles['TableCell']),
     Paragraph("1.0 (reference)", styles['TableCell']),
     Paragraph("1.0 (reference)", styles['TableCell'])],
    [Paragraph("1", styles['TableCell']),
     Paragraph("1.5", styles['TableCell']),
     Paragraph("1.1", styles['TableCell']),
     Paragraph("1.8", styles['TableCell'])],
    [Paragraph("2–3", styles['TableCell']),
     Paragraph("2.6", styles['TableCell']),
     Paragraph("1.5", styles['TableCell']),
     Paragraph("3.7", styles['TableCell'])],
    [Paragraph("4+", styles['TableCell']),
     Paragraph("4.6", styles['TableCell']),
     Paragraph("2.2", styles['TableCell']),
     Paragraph("12.2", styles['TableCell'])],
]
t = Table(ace_data, colWidths=[70, 110, 110, 110])
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
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "<i>Table 2.1: Adverse Childhood Experiences and adult disease risk — odds ratios "
    "(Felitti et al., 1998; Dube et al., 2001)</i>",
    styles['FootNote']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 3 — STRESS AND CARDIOVASCULAR DISEASE
# =========================================================================
story.append(Paragraph(
    "Chapter 3: Stress and Cardiovascular Disease", styles['ChapterHead']))

story.append(Paragraph(
    "Cardiovascular disease (CVD) is the leading cause of death worldwide, killing approximately "
    "17.9 million people per year (WHO, 2021). Chronic psychological stress is an independent "
    "risk factor for CVD — comparable in magnitude to smoking, hypertension, and hyperlipidemia "
    "(Rosengren et al., 2004). The INTERHEART study, which analyzed 30,000 patients across 52 "
    "countries, found that psychosocial stress accounted for approximately 33% of the population-"
    "attributable risk for myocardial infarction.",
    styles['Body']))

story.append(OrganImpactDiagram())
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("3.1 Mechanisms of Cardiovascular Damage", styles['SectionHead']))

story.append(Paragraph(
    "Chronic stress damages the cardiovascular system through multiple converging pathways: "
    "(1) sustained sympathetic activation elevates heart rate and blood pressure, increasing "
    "cardiac workload and causing ventricular remodeling; (2) cortisol promotes visceral fat "
    "accumulation, dyslipidemia, and insulin resistance — all established cardiovascular risk "
    "factors; (3) stress-induced inflammation damages vascular endothelium, promoting "
    "atherosclerotic plaque formation; (4) catecholamines increase platelet aggregation, "
    "raising thrombotic risk (Steptoe & Kivimäki, 2013).",
    styles['Body']))

story.append(Paragraph("3.2 The Whitehall Studies", styles['SectionHead']))

story.append(Paragraph(
    "The Whitehall II study — a landmark prospective cohort study of 10,308 British civil "
    "servants — demonstrated that work stress (high demand, low control) is independently "
    "associated with a 50% increase in coronary heart disease risk (Chandola et al., 2008). "
    "Crucially, this association persisted after controlling for conventional risk factors "
    "(smoking, blood pressure, cholesterol, BMI), demonstrating that stress is not merely "
    "a proxy for unhealthy behavior but a direct pathological mechanism.",
    styles['Body']))

story.append(Paragraph("3.3 Broken Heart Syndrome (Takotsubo Cardiomyopathy)", styles['SectionHead']))

story.append(Paragraph(
    "Takotsubo cardiomyopathy — colloquially \"broken heart syndrome\" — is a dramatic "
    "demonstration of acute stress causing direct cardiac damage. Triggered by sudden emotional "
    "or physical stress, it causes a catecholamine surge that stuns the myocardium, producing "
    "transient left ventricular dysfunction that mimics acute myocardial infarction. It accounts "
    "for approximately 2% of all acute coronary syndrome presentations and carries a 4–5% "
    "in-hospital mortality rate (Templin et al., 2015). It is proof that stress can literally "
    "break the heart.",
    styles['Body']))

story.append(Paragraph("3.4 Stress and Sudden Cardiac Death", styles['SectionHead']))

story.append(Paragraph(
    "Acute psychological stress can trigger fatal cardiac arrhythmias. Epidemiological studies "
    "consistently show spikes in cardiac mortality following earthquakes, wars, and even "
    "major sporting events. Leor et al. (1996) documented a significant increase in sudden "
    "cardiac death in Los Angeles following the 1994 Northridge earthquake. The mechanism is "
    "sympathetic overstimulation disrupting cardiac electrical stability — stress literally "
    "stops hearts.",
    styles['Body']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 4 — STRESS AND THE IMMUNE SYSTEM
# =========================================================================
story.append(Paragraph(
    "Chapter 4: Stress and the Immune System", styles['ChapterHead']))

story.append(Paragraph(
    "The field of psychoneuroimmunology (PNI) has established beyond doubt that the nervous "
    "system and immune system are bidirectionally connected. Stress does not merely \"weaken\" "
    "the immune system — it fundamentally reshapes immune function, simultaneously suppressing "
    "adaptive immunity (the targeted defense against specific pathogens) while promoting chronic "
    "low-grade inflammation (Segerstrom & Miller, 2004).",
    styles['Body']))

story.append(Paragraph("4.1 Cortisol and Immune Suppression", styles['SectionHead']))

story.append(Paragraph(
    "Cortisol is inherently immunosuppressive — this is why synthetic glucocorticoids "
    "(prednisone, dexamethasone) are used as anti-inflammatory and immunosuppressive drugs. "
    "Chronic cortisol elevation suppresses natural killer (NK) cell activity, reduces T-cell "
    "proliferation, impairs antibody production, and shifts the immune response from Th1 "
    "(cell-mediated, anti-viral) to Th2 (humoral, allergic) dominance (Glaser & Kiecolt-Glaser, "
    "2005).",
    styles['Body']))

story.append(Paragraph(
    "Cohen et al. (1991) demonstrated this with elegant experiments: healthy volunteers were "
    "exposed to rhinovirus after completing stress questionnaires. Higher stress levels predicted "
    "higher rates of clinical colds in a dose-response relationship — not because stress increased "
    "viral exposure, but because it impaired the immune response to the same viral dose.",
    styles['Body']))

story.append(Paragraph("4.2 Chronic Inflammation — The Silent Killer", styles['SectionHead']))

story.append(Paragraph(
    "While suppressing adaptive immunity, chronic stress simultaneously activates the innate "
    "inflammatory response. Pro-inflammatory cytokines — interleukin-6 (IL-6), tumor necrosis "
    "factor alpha (TNF-α), and C-reactive protein (CRP) — are chronically elevated in stressed "
    "individuals. This state of persistent low-grade inflammation, sometimes called \"sterile "
    "inflammation\" or \"inflammaging,\" is now recognized as the common mechanism underlying "
    "cardiovascular disease, type 2 diabetes, Alzheimer's disease, depression, and cancer "
    "(Furman et al., 2019).",
    styles['Body']))

story.append(Paragraph(
    "The NF-κB signaling pathway — the master regulator of inflammatory gene expression — is "
    "upregulated by chronic stress. Cole et al. (2007) showed that social isolation activates "
    "a conserved transcriptional response to adversity (CTRA), characterized by upregulation of "
    "pro-inflammatory genes and downregulation of antiviral genes. Loneliness literally rewrites "
    "immune gene expression.",
    styles['Body']))

story.append(Paragraph("4.3 Stress and Autoimmunity", styles['SectionHead']))

story.append(Paragraph(
    "The immune dysregulation caused by chronic stress increases the risk of autoimmune disease. "
    "A landmark Swedish population study of 106,464 patients (Song et al., 2018) found that "
    "stress-related disorders were associated with a 36% increased risk of autoimmune disease — "
    "including rheumatoid arthritis, multiple sclerosis, type 1 diabetes, inflammatory bowel "
    "disease, and psoriasis. For patients with PTSD specifically, the risk of autoimmune disease "
    "was increased by 46%.",
    styles['Body']))

story.append(Paragraph("4.4 Stress and Wound Healing", styles['SectionHead']))

story.append(Paragraph(
    "Kiecolt-Glaser et al. (1995) demonstrated that chronic stress slows wound healing by "
    "approximately 40%. Caregivers of Alzheimer's patients took 9 days longer (48.7 vs. 39.3 "
    "days) to heal a standardized punch biopsy wound compared to age-matched controls. This "
    "effect is mediated by cortisol-induced suppression of cytokines essential for the "
    "inflammatory and proliferative phases of wound repair.",
    styles['Body']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 5 — STRESS AND THE BRAIN
# =========================================================================
story.append(Paragraph(
    "Chapter 5: Stress and the Brain — Neurodegeneration and Mental Illness", styles['ChapterHead']))

story.append(Paragraph(
    "The brain is both the organ that perceives stress and the organ most damaged by it. Chronic "
    "stress causes measurable structural changes in the brain: hippocampal atrophy, amygdala "
    "hypertrophy, prefrontal cortex thinning, and disrupted connectivity between emotional and "
    "rational brain regions (McEwen et al., 2016).",
    styles['Body']))

story.append(Paragraph("5.1 Hippocampal Damage and Memory", styles['SectionHead']))

story.append(Paragraph(
    "The hippocampus — critical for memory formation and HPA axis regulation — is exceptionally "
    "vulnerable to cortisol. It has the highest density of glucocorticoid receptors in the brain. "
    "Chronic cortisol elevation causes dendritic retraction, reduced neurogenesis, and eventual "
    "volume loss in the hippocampus. MRI studies show that patients with chronic stress, PTSD, "
    "and major depression have hippocampal volumes 10–20% smaller than healthy controls "
    "(Bremner, 2006).",
    styles['Body']))

story.append(Paragraph(
    "This creates a vicious cycle: hippocampal damage impairs negative feedback on the HPA axis, "
    "leading to further cortisol elevation, leading to further hippocampal damage. Sapolsky "
    "(1996) termed this the \"glucocorticoid cascade hypothesis\" — a self-amplifying process "
    "that, once initiated, progressively worsens without intervention.",
    styles['Body']))

story.append(Paragraph("5.2 Amygdala Hyperactivation", styles['SectionHead']))

story.append(Paragraph(
    "While the hippocampus shrinks under chronic stress, the amygdala — the brain's fear and "
    "threat detection center — grows. Chronic stress causes dendritic growth and increased "
    "synaptic connectivity in the amygdala, making it hyperreactive to perceived threats "
    "(Vyas et al., 2002). The stressed brain becomes simultaneously worse at rational thinking "
    "(prefrontal and hippocampal suppression) and better at detecting threats (amygdala "
    "enhancement) — a combination that produces anxiety, hypervigilance, and impaired "
    "decision-making.",
    styles['Body']))

story.append(Paragraph("5.3 Stress and Depression", styles['SectionHead']))

story.append(Paragraph(
    "The relationship between chronic stress and major depressive disorder (MDD) is causal, "
    "not merely correlational. Approximately 80% of first episodes of MDD are preceded by "
    "a major life stressor (Hammen, 2005). The mechanisms are multiple: cortisol-mediated "
    "hippocampal damage reduces serotonin receptor density; chronic inflammation increases "
    "brain levels of pro-inflammatory cytokines that directly impair monoamine neurotransmission; "
    "and stress reduces brain-derived neurotrophic factor (BDNF), which is essential for "
    "neuronal survival and plasticity (Duman & Monteggia, 2006).",
    styles['Body']))

story.append(Paragraph(
    "The inflammatory model of depression — now supported by extensive evidence — holds that "
    "depression is, in significant part, a neuroinflammatory disorder driven by chronic stress. "
    "Anti-inflammatory agents show antidepressant effects in clinical trials. Patients with "
    "elevated CRP and IL-6 respond better to anti-inflammatory treatment than to conventional "
    "SSRIs (Raison & Miller, 2011).",
    styles['Body']))

story.append(Paragraph("5.4 Stress and Neurodegeneration", styles['SectionHead']))

story.append(Paragraph(
    "Chronic stress accelerates neurodegenerative disease. Cortisol increases the production "
    "and accumulation of amyloid-beta plaques — the hallmark pathology of Alzheimer's disease "
    "(Green et al., 2006). Chronic stress also increases tau phosphorylation, the other "
    "hallmark of Alzheimer's pathology. A prospective study of 800 women followed for 38 years "
    "found that self-reported psychological stress in midlife was associated with a 65% "
    "increased risk of Alzheimer's disease (Johansson et al., 2010).",
    styles['Body']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 6 — STRESS AND METABOLISM
# =========================================================================
story.append(Paragraph(
    "Chapter 6: Stress and Metabolism — Diabetes, Obesity, and Metabolic Syndrome",
    styles['ChapterHead']))

story.append(Paragraph(
    "Chronic stress is a direct cause of metabolic dysfunction. The metabolic effects of cortisol "
    "— glucose mobilization, insulin resistance, visceral fat accumulation — are adaptive in acute "
    "stress but devastating when sustained. The global epidemics of type 2 diabetes and obesity "
    "cannot be understood without accounting for the role of chronic stress.",
    styles['Body']))

story.append(Paragraph("6.1 Cortisol and Insulin Resistance", styles['SectionHead']))

story.append(Paragraph(
    "Cortisol directly opposes insulin action. It stimulates hepatic gluconeogenesis (glucose "
    "production by the liver), inhibits glucose uptake in muscle and adipose tissue, and promotes "
    "lipolysis. These effects evolved to ensure glucose availability during acute stress. When "
    "sustained chronically, they produce the same metabolic profile as type 2 diabetes: "
    "hyperglycemia, hyperinsulinemia, and progressive insulin resistance (Chiodini et al., 2007).",
    styles['Body']))

story.append(Paragraph(
    "Patients with Cushing's syndrome — a condition of chronic cortisol excess — develop diabetes "
    "at rates exceeding 50%, providing direct clinical evidence that cortisol causes diabetes. "
    "The same pathological process occurs in chronic psychological stress, at lower cortisol "
    "levels but over longer timeframes.",
    styles['Body']))

story.append(Paragraph("6.2 Visceral Fat and the Cortisol-Belly Connection", styles['SectionHead']))

story.append(Paragraph(
    "Cortisol preferentially promotes fat deposition in the visceral (abdominal) compartment "
    "rather than subcutaneous tissue. Visceral fat is not metabolically inert storage — it is "
    "an active endocrine organ that produces pro-inflammatory cytokines (adipokines), contributing "
    "to systemic inflammation and insulin resistance. The distribution of fat matters more than "
    "the total amount: visceral obesity is independently associated with cardiovascular disease, "
    "diabetes, and mortality even in individuals with normal BMI (Björntorp, 2001).",
    styles['Body']))

story.append(Paragraph("6.3 Stress Eating and Reward Pathways", styles['SectionHead']))

story.append(Paragraph(
    "Cortisol increases appetite for high-calorie, high-fat, high-sugar foods through its effects "
    "on reward pathways in the brain. It upregulates neuropeptide Y and ghrelin (hunger hormones) "
    "while downregulating leptin sensitivity (satiety signaling). This drives \"comfort eating\" — "
    "not a failure of willpower but a direct neurobiological consequence of chronic stress "
    "(Adam & Epel, 2007).",
    styles['Body']))

story.append(Paragraph(
    "The combination of cortisol-driven appetite for calorie-dense food, cortisol-driven visceral "
    "fat deposition, and cortisol-driven insulin resistance creates a metabolic perfect storm. "
    "Stress does not merely correlate with metabolic syndrome — it causes it through identified "
    "biochemical pathways.",
    styles['Body']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 7 — STRESS AND THE GUT-BRAIN AXIS
# =========================================================================
story.append(Paragraph(
    "Chapter 7: Stress and the Gut-Brain Axis", styles['ChapterHead']))

story.append(Paragraph(
    "The gut-brain axis — the bidirectional communication network between the enteric nervous "
    "system and the central nervous system — is one of the most important discoveries in "
    "modern medicine. The gut contains 500 million neurons, produces 95% of the body's serotonin, "
    "and hosts approximately 38 trillion microorganisms that collectively influence immunity, "
    "metabolism, and brain function (Cryan et al., 2019).",
    styles['Body']))

story.append(Paragraph("7.1 Stress and the Microbiome", styles['SectionHead']))

story.append(Paragraph(
    "Chronic stress fundamentally alters the gut microbiome. Animal studies demonstrate that "
    "chronic stress reduces microbial diversity, decreases beneficial Lactobacillus and "
    "Bifidobacterium species, and increases pathogenic bacteria (Bailey et al., 2011). In "
    "humans, chronic stress is associated with reduced microbiome diversity — a marker now "
    "linked to depression, obesity, autoimmune disease, and cardiovascular disease.",
    styles['Body']))

story.append(Paragraph(
    "The microbiome is not merely affected by stress — it modulates the stress response. "
    "Germ-free mice (raised without gut bacteria) show exaggerated HPA axis responses to "
    "stress, which normalize when beneficial bacteria are introduced. This demonstrates "
    "that the microbiome is a regulatory component of the stress response itself "
    "(Sudo et al., 2004).",
    styles['Body']))

story.append(Paragraph("7.2 Intestinal Permeability (Leaky Gut)", styles['SectionHead']))

story.append(Paragraph(
    "Chronic stress increases intestinal permeability — the so-called \"leaky gut.\" Cortisol "
    "and pro-inflammatory cytokines weaken tight junctions between intestinal epithelial cells, "
    "allowing bacterial endotoxins (particularly lipopolysaccharide, LPS) to enter the bloodstream. "
    "This endotoxemia triggers systemic inflammation, contributing to depression, metabolic "
    "syndrome, and autoimmune activation (Kelly et al., 2015).",
    styles['Body']))

story.append(Paragraph("7.3 Irritable Bowel Syndrome (IBS)", styles['SectionHead']))

story.append(Paragraph(
    "IBS — which affects approximately 11% of the global population — is the prototypical "
    "stress-gut disorder. Approximately 60% of IBS patients have comorbid anxiety or depression. "
    "The condition is now understood as a disorder of the gut-brain axis rather than a purely "
    "gastrointestinal condition. Stress directly increases visceral hypersensitivity, alters "
    "gut motility, and disrupts the microbiome — all core features of IBS (Mayer et al., 2015).",
    styles['Body']))

story.append(Paragraph("7.4 The Vagus Nerve — The Stress-Gut Highway", styles['SectionHead']))

story.append(Paragraph(
    "The vagus nerve — the longest cranial nerve, running from the brainstem to the abdomen — is "
    "the primary communication channel between gut and brain. It carries 80% of its signals from "
    "gut to brain (afferent), not brain to gut. Vagal tone — measured by heart rate variability "
    "(HRV) — is a biomarker of stress resilience. Low vagal tone is associated with chronic "
    "inflammation, depression, and poor stress recovery. Interventions that increase vagal "
    "tone — deep breathing, meditation, cold exposure — improve both mental health and gut "
    "function (Breit et al., 2018).",
    styles['Body']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 8 — STRESS AND CANCER
# =========================================================================
story.append(Paragraph("Chapter 8: Stress and Cancer", styles['ChapterHead']))

story.append(Paragraph(
    "The relationship between stress and cancer is complex but increasingly clear. Chronic stress "
    "does not directly cause cancer through mutagenesis — it does not damage DNA in the way that "
    "radiation or carcinogens do. But chronic stress creates a biological environment that "
    "promotes cancer initiation, accelerates cancer progression, impairs anti-tumor immunity, "
    "and increases metastasis (Antoni et al., 2006).",
    styles['Body']))

story.append(Paragraph("8.1 Immune Surveillance and Tumor Escape", styles['SectionHead']))

story.append(Paragraph(
    "The immune system continuously detects and destroys nascent cancer cells — a process called "
    "immune surveillance. Natural killer (NK) cells are the primary defense against tumor cells. "
    "Chronic stress, through cortisol-mediated NK cell suppression, impairs this surveillance, "
    "allowing pre-cancerous cells to escape immune detection and proliferate. Ben-Eliyahu et al. "
    "(1991) demonstrated that stress-induced NK cell suppression in rats directly increased "
    "metastatic spread.",
    styles['Body']))

story.append(Paragraph("8.2 Stress Hormones and Tumor Biology", styles['SectionHead']))

story.append(Paragraph(
    "Catecholamines (adrenaline, noradrenaline) and cortisol directly affect tumor cell biology. "
    "Beta-adrenergic signaling promotes tumor angiogenesis (new blood vessel formation), increases "
    "tumor cell migration and invasion, inhibits tumor cell apoptosis (programmed death), and "
    "activates epithelial-mesenchymal transition (EMT) — the process by which tumor cells become "
    "metastatic (Thaker et al., 2006). Tumor cells express adrenergic and glucocorticoid "
    "receptors, making them directly responsive to stress hormones.",
    styles['Body']))

story.append(Paragraph("8.3 Epidemiological Evidence", styles['SectionHead']))

story.append(Paragraph(
    "A meta-analysis of 165 studies (Chida et al., 2008) found that stress-related psychosocial "
    "factors were significantly associated with cancer incidence and survival. Depression, social "
    "isolation, and bereavement were associated with increased cancer mortality. Conversely, "
    "psychosocial interventions — stress management, social support groups, cognitive behavioral "
    "therapy — have been shown to improve immune function markers and, in some studies, survival "
    "in cancer patients (Andersen et al., 2008).",
    styles['Body']))

story.append(Paragraph("8.4 The Beta-Blocker Evidence", styles['SectionHead']))

story.append(Paragraph(
    "Compelling evidence comes from observational studies of beta-blocker use (drugs that block "
    "adrenergic signaling). Multiple studies show that cancer patients taking beta-blockers for "
    "cardiovascular conditions have reduced cancer progression and improved survival — "
    "particularly in breast, ovarian, and melanoma cancers (Barron et al., 2011). This provides "
    "pharmacological evidence that stress hormones directly promote cancer progression, because "
    "blocking their receptors improves outcomes.",
    styles['Body']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 9 — STRESS AND AGING
# =========================================================================
story.append(Paragraph(
    "Chapter 9: Stress and Aging — Telomeres and Epigenetics", styles['ChapterHead']))

story.append(Paragraph(
    "Chronic stress does not merely cause disease — it accelerates biological aging. The "
    "mechanisms are now understood at the molecular level: telomere shortening, epigenetic "
    "modification, mitochondrial dysfunction, and oxidative stress. Stress ages the body "
    "faster than time alone.",
    styles['Body']))

story.append(Paragraph("9.1 Telomeres — The Biological Clock", styles['SectionHead']))

story.append(Paragraph(
    "Telomeres are protective caps at the ends of chromosomes that shorten with each cell "
    "division. When telomeres become critically short, cells enter senescence or apoptosis. "
    "Telomere length is therefore a biomarker of biological aging. The Nobel Prize-winning "
    "work of Elizabeth Blackburn and Elissa Epel demonstrated that chronic psychological stress "
    "accelerates telomere shortening (Epel et al., 2004).",
    styles['Body']))

story.append(Paragraph(
    "In their landmark study, mothers caring for chronically ill children — a model of sustained "
    "psychological stress — had telomeres equivalent to approximately 10 years of additional "
    "aging compared to controls. The enzyme telomerase, which maintains telomere length, was "
    "significantly reduced in stressed individuals. Perceived stress, not just objective stress "
    "exposure, was the strongest predictor of telomere shortening — demonstrating that the "
    "psychological experience of stress, not merely the stressor, drives biological aging.",
    styles['Body']))

story.append(Paragraph("9.2 Epigenetic Changes", styles['SectionHead']))

story.append(Paragraph(
    "Epigenetics — changes in gene expression without changes in DNA sequence — is the mechanism "
    "by which stress leaves lasting biological marks. Chronic stress alters DNA methylation "
    "patterns, histone modifications, and microRNA expression, effectively reprogramming cellular "
    "function. These changes can persist for years after the stressor resolves and can even be "
    "transmitted across generations (Zannas & West, 2014).",
    styles['Body']))

story.append(Paragraph(
    "The glucocorticoid receptor gene (NR3C1) is particularly susceptible to stress-induced "
    "epigenetic modification. Childhood adversity increases methylation of the NR3C1 promoter, "
    "reducing glucocorticoid receptor expression and impairing HPA axis feedback — effectively "
    "programming a child's stress response for life (McGowan et al., 2009). This is the "
    "molecular mechanism by which childhood stress causes adult disease.",
    styles['Body']))

story.append(Paragraph("9.3 Intergenerational Transmission", styles['SectionHead']))

story.append(Paragraph(
    "The most sobering finding in stress epigenetics is intergenerational transmission. Yehuda "
    "et al. (2016) found that Holocaust survivors and their adult children showed altered "
    "methylation patterns in the FKBP5 gene — a key regulator of the stress response. The "
    "children, who never experienced the trauma directly, carried epigenetic marks of their "
    "parents' stress. Similar findings have been documented in descendants of famine survivors, "
    "war veterans, and abuse victims.",
    styles['Body']))

story.append(Paragraph(
    "This means that stress is not merely an individual pathology — it is a transgenerational "
    "one. The stress of one generation alters the biology of the next. Healing stress is "
    "therefore not only a personal health issue but a public health imperative with consequences "
    "spanning generations.",
    styles['Body']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 10 — STRESS IN MODERN SOCIETY
# =========================================================================
story.append(Paragraph(
    "Chapter 10: Stress in Modern Society — Work, Technology, and Loneliness",
    styles['ChapterHead']))

story.append(Paragraph(
    "The human stress response evolved for a world of acute physical threats. The modern world "
    "has replaced those threats with chronic psychological ones: work pressure, financial "
    "insecurity, social comparison, information overload, and social isolation. These stressors "
    "activate the same biological pathways but never resolve — there is no moment when the "
    "predator leaves and the body can recover.",
    styles['Body']))

story.append(Paragraph("10.1 Work Stress and Burnout", styles['SectionHead']))

story.append(Paragraph(
    "The WHO recognized burnout as an occupational phenomenon in 2019 (ICD-11). Burnout is "
    "characterized by emotional exhaustion, depersonalization, and reduced personal accomplishment. "
    "It affects an estimated 67% of workers at some point in their careers (Gallup, 2023). "
    "Burnout is not weakness — it is the predictable consequence of chronic activation of the "
    "stress response without adequate recovery.",
    styles['Body']))

story.append(Paragraph(
    "The demand-control model (Karasek, 1979) identifies the most pathological work stress as "
    "high psychological demands combined with low control — the situation of most modern workers. "
    "The effort-reward imbalance model (Siegrist, 1996) adds that perceived unfairness in "
    "effort-reward ratios is independently toxic. Both models predict cardiovascular disease, "
    "depression, and mortality with remarkable consistency across cultures and occupations.",
    styles['Body']))

stress_sources_data = [
    [Paragraph("<b>Modern Stressor</b>", styles['TableCell']),
     Paragraph("<b>Prevalence</b>", styles['TableCell']),
     Paragraph("<b>Key Health Impact</b>", styles['TableCell'])],
    [Paragraph("Work overload", styles['TableCell']),
     Paragraph("67% of workers", styles['TableCell']),
     Paragraph("CVD, depression, burnout", styles['TableCell'])],
    [Paragraph("Financial insecurity", styles['TableCell']),
     Paragraph("~40% of adults", styles['TableCell']),
     Paragraph("Anxiety, metabolic syndrome", styles['TableCell'])],
    [Paragraph("Social isolation", styles['TableCell']),
     Paragraph("~33% report loneliness", styles['TableCell']),
     Paragraph("Mortality risk equiv. to 15 cig/day", styles['TableCell'])],
    [Paragraph("Digital overload", styles['TableCell']),
     Paragraph("Screen time 7+ hrs/day", styles['TableCell']),
     Paragraph("Sleep disruption, anxiety", styles['TableCell'])],
    [Paragraph("Social comparison (media)", styles['TableCell']),
     Paragraph("Pervasive", styles['TableCell']),
     Paragraph("Depression, body dysmorphia", styles['TableCell'])],
    [Paragraph("Caregiving burden", styles['TableCell']),
     Paragraph("~20% of adults", styles['TableCell']),
     Paragraph("Accelerated aging (10+ yrs)", styles['TableCell'])],
]
t = Table(stress_sources_data, colWidths=[120, 100, 180])
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
    "<i>Table 10.1: Major modern stressors and their health impacts</i>",
    styles['FootNote']))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("10.2 Loneliness — The Deadliest Stressor", styles['SectionHead']))

story.append(Paragraph(
    "Loneliness is the most dangerous psychosocial stressor. Holt-Lunstad et al. (2010) "
    "conducted a meta-analysis of 148 studies comprising 308,849 participants and found that "
    "social isolation increases mortality risk by 50% — equivalent to smoking 15 cigarettes "
    "per day, and greater than the mortality risk of obesity or physical inactivity. The U.S. "
    "Surgeon General declared loneliness a public health epidemic in 2023.",
    styles['Body']))

story.append(Paragraph(
    "The biological mechanisms are the same as for other chronic stressors: loneliness activates "
    "the HPA axis, elevates cortisol, promotes inflammation (the CTRA response described by "
    "Cole et al.), suppresses adaptive immunity, and accelerates telomere shortening. Humans "
    "evolved as social animals — social isolation is perceived by the brain as a survival threat, "
    "triggering the full stress response (Cacioppo & Cacioppo, 2014).",
    styles['Body']))

story.append(Paragraph("10.3 Technology and the Always-On Stress", styles['SectionHead']))

story.append(Paragraph(
    "Smartphones and constant connectivity have created a new category of chronic stressor: "
    "the inability to disengage. The average person checks their phone 96 times per day "
    "(Asurion, 2023). Each notification triggers a micro-activation of the stress response. "
    "Email and messaging create an expectation of immediate response that prevents psychological "
    "recovery. Social media algorithms are designed to maximize engagement through content that "
    "triggers emotional arousal — fear, outrage, envy — all of which activate the stress "
    "response (Primack et al., 2017).",
    styles['Body']))

story.append(Paragraph(
    "Sleep disruption from blue light exposure and evening screen use compounds the problem. "
    "Chronic sleep deprivation (less than 7 hours) independently elevates cortisol, impairs "
    "immune function, increases inflammation, and accelerates aging. The combination of "
    "psychological stress and sleep deprivation is multiplicative, not additive, in its "
    "health impact (Walker, 2017).",
    styles['Body']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 11 — THE SCIENCE OF RECOVERY
# =========================================================================
story.append(Paragraph(
    "Chapter 11: The Science of Recovery — What Actually Works", styles['ChapterHead']))

story.append(Paragraph(
    "The damage caused by chronic stress is not irreversible. Neuroplasticity allows the brain "
    "to recover. The immune system can be restored. The microbiome can be rebuilt. Telomere "
    "shortening can be slowed and, in some cases, reversed. But recovery requires specific, "
    "evidence-based interventions — not vague advice to \"relax.\"",
    styles['Body']))

story.append(Paragraph("11.1 Exercise — The Most Powerful Anti-Stress Intervention", styles['SectionHead']))

story.append(Paragraph(
    "Regular physical exercise is the single most effective intervention for stress-related "
    "disease, supported by the largest body of evidence of any intervention. Exercise reduces "
    "cortisol, increases BDNF (promoting neuroplasticity), enhances NK cell activity, improves "
    "HRV (vagal tone), reduces inflammatory markers, improves insulin sensitivity, and has "
    "antidepressant effects comparable to SSRIs for mild to moderate depression (Schuch et al., "
    "2016).",
    styles['Body']))

story.append(Paragraph(
    "The dose-response relationship is clear: 150 minutes per week of moderate-intensity "
    "exercise (brisk walking) reduces all-cause mortality by approximately 30% and reduces "
    "depression risk by approximately 25% (WHO, 2020). Higher intensities and durations provide "
    "additional benefit up to approximately 300 minutes per week, beyond which marginal returns "
    "diminish.",
    styles['Body']))

story.append(Paragraph("11.2 Meditation and Mindfulness", styles['SectionHead']))

story.append(Paragraph(
    "Mindfulness-based stress reduction (MBSR) — developed by Jon Kabat-Zinn — has been "
    "studied in over 1,000 clinical trials. Meta-analyses demonstrate significant effects on "
    "anxiety (effect size d=0.63), depression (d=0.59), and chronic pain (d=0.33) "
    "(Goyal et al., 2014). At the biological level, meditation reduces cortisol, increases "
    "telomerase activity (Jacobs et al., 2011), reduces inflammatory markers, and increases "
    "gray matter density in the hippocampus and prefrontal cortex (Hölzel et al., 2011).",
    styles['Body']))

story.append(Paragraph(
    "Even brief meditation practice (10–20 minutes daily) produces measurable changes in "
    "stress biomarkers within 8 weeks. The mechanism is not mystical — meditation activates "
    "the parasympathetic nervous system (vagal tone), downregulates the HPA axis, and "
    "strengthens prefrontal cortex connectivity with the amygdala, restoring top-down "
    "emotional regulation (Tang et al., 2015).",
    styles['Body']))

story.append(Paragraph("11.3 Sleep — Non-Negotiable Recovery", styles['SectionHead']))

story.append(Paragraph(
    "Sleep is the body's primary recovery mechanism. During sleep, cortisol reaches its nadir, "
    "growth hormone peaks, the glymphatic system clears metabolic waste from the brain (including "
    "amyloid-beta), immune function is restored, and memory consolidation occurs. Chronic sleep "
    "deprivation (less than 7 hours consistently) is itself a form of chronic stress that "
    "produces all the pathological effects described in this thesis (Walker, 2017).",
    styles['Body']))

story.append(Paragraph(
    "Sleep hygiene is therefore a medical intervention: consistent sleep schedule, dark and cool "
    "sleeping environment, no screens for 1 hour before bed, no caffeine after midday, and "
    "no alcohol (which fragments sleep architecture despite its sedative effect).",
    styles['Body']))

story.append(Paragraph("11.4 Social Connection", styles['SectionHead']))

story.append(Paragraph(
    "Given that loneliness is the deadliest stressor, social connection is one of the most "
    "powerful recoveries. Quality of social relationships — not quantity — predicts health "
    "outcomes. The Harvard Study of Adult Development, the longest-running study of human "
    "wellbeing (85+ years), concluded that the single strongest predictor of health, happiness, "
    "and longevity is the quality of close relationships (Waldinger & Schulz, 2023).",
    styles['Body']))

story.append(Paragraph("11.5 Nature Exposure", styles['SectionHead']))

story.append(Paragraph(
    "Exposure to natural environments reduces cortisol, heart rate, blood pressure, and "
    "sympathetic nervous system activity while increasing parasympathetic activity and NK cell "
    "function. The Japanese practice of <i>shinrin-yoku</i> (forest bathing) has been shown to "
    "reduce cortisol by 12.4%, blood pressure by 1.4%, and heart rate by 5.8% compared to "
    "urban environments (Li, 2010). A minimum of 120 minutes per week in nature is associated "
    "with significantly better health and wellbeing (White et al., 2019).",
    styles['Body']))

recovery_data = [
    [Paragraph("<b>Intervention</b>", styles['TableCell']),
     Paragraph("<b>Effect on Cortisol</b>", styles['TableCell']),
     Paragraph("<b>Effect on Inflammation</b>", styles['TableCell']),
     Paragraph("<b>Evidence Level</b>", styles['TableCell'])],
    [Paragraph("Exercise (150 min/wk)", styles['TableCell']),
     Paragraph("↓ 15–25%", styles['TableCell']),
     Paragraph("↓ CRP 20–30%", styles['TableCell']),
     Paragraph("Strong (1000+ RCTs)", styles['TableCell'])],
    [Paragraph("Meditation (MBSR)", styles['TableCell']),
     Paragraph("↓ 15–20%", styles['TableCell']),
     Paragraph("↓ IL-6, TNF-α", styles['TableCell']),
     Paragraph("Strong (1000+ trials)", styles['TableCell'])],
    [Paragraph("Sleep (7–9 hrs)", styles['TableCell']),
     Paragraph("Normalized rhythm", styles['TableCell']),
     Paragraph("↓ CRP 30–40%", styles['TableCell']),
     Paragraph("Strong", styles['TableCell'])],
    [Paragraph("Social connection", styles['TableCell']),
     Paragraph("↓ 10–15%", styles['TableCell']),
     Paragraph("↓ NF-κB activity", styles['TableCell']),
     Paragraph("Strong (meta-analyses)", styles['TableCell'])],
    [Paragraph("Nature exposure", styles['TableCell']),
     Paragraph("↓ 12–16%", styles['TableCell']),
     Paragraph("↑ NK cell activity", styles['TableCell']),
     Paragraph("Moderate-Strong", styles['TableCell'])],
    [Paragraph("CBT/Therapy", styles['TableCell']),
     Paragraph("↓ 10–20%", styles['TableCell']),
     Paragraph("↓ CRP, IL-6", styles['TableCell']),
     Paragraph("Strong for depression/anxiety", styles['TableCell'])],
]
t = Table(recovery_data, colWidths=[100, 100, 100, 100])
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
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "<i>Table 11.1: Evidence-based stress recovery interventions and their biological effects</i>",
    styles['FootNote']))

story.append(PageBreak())

# =========================================================================
# CHAPTER 12 — CONCLUSION
# =========================================================================
story.append(Paragraph(
    "Chapter 12: Conclusion — Stress Is Not Inevitable", styles['ChapterHead']))

story.append(Paragraph(
    "This thesis has traced the complete causal chain from psychological stressor to physical "
    "disease. The evidence is unambiguous and convergent across disciplines: chronic stress "
    "causes cardiovascular disease, immune dysfunction, neurodegeneration, metabolic syndrome, "
    "gut disorders, cancer progression, and accelerated aging through identified, measurable, "
    "reproducible biological mechanisms.",
    styles['Body']))

story.append(Paragraph("12.1 Stress as a Primary Pathological Mechanism", styles['SectionHead']))

story.append(Paragraph(
    "Stress is not a vague \"risk factor\" — it is a primary pathological mechanism with the "
    "same causal status as smoking, hypertension, or hyperglycemia. The HPA axis, SAM axis, "
    "inflammatory cascade, epigenetic modification, telomere shortening, microbiome disruption, "
    "and immune dysregulation are not theoretical constructs — they are measurable, modifiable "
    "biological processes. Treating stress as a medical problem, not a personal weakness, is "
    "the essential paradigm shift.",
    styles['Body']))

story.append(Paragraph("12.2 The Societal Dimension", styles['SectionHead']))

story.append(Paragraph(
    "Individual stress reduction is necessary but insufficient. The modern epidemic of chronic "
    "stress is driven by systemic factors: precarious employment, unaffordable housing, social "
    "inequality, inadequate healthcare, technology-driven overwork, and the erosion of community. "
    "A society that generates chronic stress in its population and then blames individuals for "
    "being stressed is a society that has failed at the most fundamental level.",
    styles['Body']))

story.append(Paragraph(
    "The economic cost of stress-related illness is staggering. In the United States alone, "
    "work stress costs an estimated $300 billion per year in absenteeism, reduced productivity, "
    "healthcare expenses, and disability claims (American Institute of Stress, 2023). In the "
    "EU, work-related stress affects approximately 28% of workers and costs an estimated "
    "€617 billion per year (EU-OSHA, 2014). Preventing stress is not just a health policy — "
    "it is an economic imperative.",
    styles['Body']))

story.append(Paragraph("12.3 Toward a Stress-Literate Society", styles['SectionHead']))

story.append(Paragraph(
    "The knowledge presented in this thesis must become universal literacy. Every person should "
    "understand how stress affects their body. Every employer should understand that chronic work "
    "stress is not a motivator but a pathogen. Every government should understand that stress "
    "reduction is healthcare, and that preventing chronic stress prevents cardiovascular disease, "
    "diabetes, depression, dementia, and cancer.",
    styles['Body']))

story.append(Paragraph(
    "Hans Selye — the father of stress research — wrote in 1956: <i>\"It is not stress that kills "
    "us, it is our reaction to it.\"</i> Modern science has refined this: it is not acute stress "
    "that kills us, but chronic stress — and our failure, as individuals and societies, to "
    "prevent it, recognize it, and treat it with the seriousness it deserves.",
    styles['Body']))

story.append(Paragraph("12.4 The Path Forward", styles['SectionHead']))

story.append(Paragraph(
    "Recovery is possible at every level. The brain can regenerate through neuroplasticity. "
    "The immune system can be restored. The microbiome can be rebuilt. Telomere shortening "
    "can be slowed. Epigenetic marks, while persistent, can be modified by sustained "
    "behavioral change. But recovery requires three things: awareness of the mechanisms "
    "(provided by research like this thesis), access to interventions (a societal obligation), "
    "and permission to prioritize health over productivity (a cultural shift).",
    styles['Body']))

story.append(Paragraph(
    "The Zokura Foundation holds that a Good Life — <i>Hyvä Elämä</i> — is not optional. It is "
    "the purpose of every system, every institution, every technology. A life of chronic stress "
    "is not a good life. The science is clear. The interventions exist. What remains is the "
    "will to build a world where stress is the exception, not the norm.",
    styles['Body']))

story.append(Spacer(1, 1*cm))
story.append(HRFlowable(width="30%", thickness=0.5, color=BORDER))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph(
    "<i>\"It is not stress that kills us, it is our reaction to it.\"</i>",
    styles['Epigraph']))
story.append(Paragraph(
    "<i>— Hans Selye</i>",
    styles['Epigraph']))
story.append(Spacer(1, 1*cm))
story.append(Paragraph("Rakkaus ja Totuus. Aina.", styles['Epigraph']))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("Miika Riikonen &amp; Kodo Zokura", styles['AuthorLine']))
story.append(Paragraph("Zokura Foundation, 2026", styles['AuthorLine']))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("太極", styles['AuthorLine']))

story.append(PageBreak())

# =========================================================================
# REFERENCES
# =========================================================================
story.append(Paragraph("References", styles['ChapterHead']))

refs = [
    "Adam, T.C. & Epel, E.S. (2007). Stress, eating and the reward system. <i>Physiology & Behavior</i>, 91(4), 449–458.",
    "American Institute of Stress (2023). Workplace Stress Statistics. https://www.stress.org/workplace-stress",
    "Andersen, B.L., et al. (2008). Psychological intervention improves survival for breast cancer patients. <i>Cancer</i>, 113(12), 3450–3458.",
    "Antoni, M.H., et al. (2006). The influence of bio-behavioural factors on tumour biology. <i>Nature Reviews Cancer</i>, 6(3), 240–248.",
    "Asurion (2023). Americans check their phones 96 times a day. Asurion Research.",
    "Bailey, M.T., et al. (2011). Exposure to a social stressor alters the structure of the intestinal microbiota. <i>Brain, Behavior, and Immunity</i>, 25(3), 397–407.",
    "Barron, T.I., et al. (2011). Beta blockers and breast cancer mortality. <i>Journal of Clinical Oncology</i>, 29(19), 2635–2644.",
    "Ben-Eliyahu, S., et al. (1991). Stress increases metastatic spread of a mammary tumor in rats. <i>Brain, Behavior, and Immunity</i>, 5(2), 193–205.",
    "Björntorp, P. (2001). Do stress reactions cause abdominal obesity and comorbidities? <i>Obesity Reviews</i>, 2(2), 73–86.",
    "Breit, S., et al. (2018). Vagus nerve as modulator of the brain–gut axis in psychiatric and inflammatory disorders. <i>Frontiers in Psychiatry</i>, 9, 44.",
    "Bremner, J.D. (2006). Traumatic stress: effects on the brain. <i>Dialogues in Clinical Neuroscience</i>, 8(4), 445–461.",
    "Brotman, D.J., et al. (2007). The cardiovascular toll of stress. <i>The Lancet</i>, 370(9592), 1089–1100.",
    "Cacioppo, J.T. & Cacioppo, S. (2014). Social relationships and health. <i>American Psychologist</i>, 69(4), 395–405.",
    "Chandola, T., et al. (2008). Work stress and coronary heart disease. <i>European Heart Journal</i>, 29(5), 640–648.",
    "Chida, Y., et al. (2008). Do stress-related psychosocial factors contribute to cancer incidence and survival? <i>Nature Clinical Practice Oncology</i>, 5(8), 466–475.",
    "Chiodini, I., et al. (2007). Cortisol secretion in patients with type 2 diabetes. <i>Diabetes Care</i>, 30(1), 83–88.",
    "Cohen, S., et al. (1991). Psychological stress and susceptibility to the common cold. <i>New England Journal of Medicine</i>, 325(9), 606–612.",
    "Cole, S.W., et al. (2007). Social regulation of gene expression in human leukocytes. <i>Genome Biology</i>, 8(9), R189.",
    "Cryan, J.F., et al. (2019). The microbiota-gut-brain axis. <i>Physiological Reviews</i>, 99(4), 1877–2013.",
    "Dube, S.R., et al. (2001). Childhood abuse, household dysfunction, and the risk of attempted suicide. <i>JAMA</i>, 286(24), 3089–3096.",
    "Duman, R.S. & Monteggia, L.M. (2006). A neurotrophic model for stress-related mood disorders. <i>Biological Psychiatry</i>, 59(12), 1116–1127.",
    "Epel, E.S., et al. (2004). Accelerated telomere shortening in response to life stress. <i>Proceedings of the National Academy of Sciences</i>, 101(49), 17312–17315.",
    "EU-OSHA (2014). Calculating the cost of work-related stress and psychosocial risks. European Agency for Safety and Health at Work.",
    "Felitti, V.J., et al. (1998). Relationship of childhood abuse and household dysfunction to many of the leading causes of death in adults. <i>American Journal of Preventive Medicine</i>, 14(4), 245–258.",
    "Furman, D., et al. (2019). Chronic inflammation in the etiology of disease across the life span. <i>Nature Medicine</i>, 25(12), 1822–1832.",
    "Gallup (2023). State of the Global Workplace: 2023 Report. Gallup, Inc.",
    "Glaser, R. & Kiecolt-Glaser, J.K. (2005). Stress-induced immune dysfunction. <i>Nature Reviews Immunology</i>, 5(3), 243–251.",
    "Goyal, M., et al. (2014). Meditation programs for psychological stress and well-being. <i>JAMA Internal Medicine</i>, 174(3), 357–368.",
    "Green, K.N., et al. (2006). Glucocorticoids increase amyloid-beta and tau pathology in a mouse model of Alzheimer's disease. <i>Journal of Neuroscience</i>, 26(35), 9047–9056.",
    "Hammen, C. (2005). Stress and depression. <i>Annual Review of Clinical Psychology</i>, 1, 293–319.",
    "Herman, J.P., et al. (2016). Regulation of the hypothalamic-pituitary-adrenocortical stress response. <i>Comprehensive Physiology</i>, 6(2), 603–621.",
    "Holt-Lunstad, J., et al. (2010). Social relationships and mortality risk. <i>PLoS Medicine</i>, 7(7), e1000316.",
    "Hölzel, B.K., et al. (2011). Mindfulness practice leads to increases in regional brain gray matter density. <i>Psychiatry Research: Neuroimaging</i>, 191(1), 36–43.",
    "Jacobs, T.L., et al. (2011). Intensive meditation training, immune cell telomerase activity, and psychological mediators. <i>Psychoneuroendocrinology</i>, 36(5), 664–681.",
    "Johansson, L., et al. (2010). Midlife psychological stress and dementia. <i>Brain</i>, 133(8), 2217–2224.",
    "Karasek, R.A. (1979). Job demands, job decision latitude, and mental strain. <i>Administrative Science Quarterly</i>, 24(2), 285–308.",
    "Kelly, J.R., et al. (2015). Breaking down the barriers: the gut microbiome, intestinal permeability and stress-related psychiatric disorders. <i>Frontiers in Cellular Neuroscience</i>, 9, 392.",
    "Kiecolt-Glaser, J.K., et al. (1995). Slowing of wound healing by psychological stress. <i>The Lancet</i>, 346(8984), 1194–1196.",
    "Leor, J., et al. (1996). Sudden cardiac death triggered by an earthquake. <i>New England Journal of Medicine</i>, 334(7), 413–419.",
    "Li, Q. (2010). Effect of forest bathing trips on human immune function. <i>Environmental Health and Preventive Medicine</i>, 15(1), 9–17.",
    "Mayer, E.A., et al. (2015). Gut/brain axis and the microbiota. <i>Journal of Clinical Investigation</i>, 125(3), 926–938.",
    "McEwen, B.S. (1998). Protective and damaging effects of stress mediators. <i>New England Journal of Medicine</i>, 338(3), 171–179.",
    "McEwen, B.S. (2008). Central effects of stress hormones in health and disease. <i>European Journal of Pharmacology</i>, 583(2-3), 174–185.",
    "McEwen, B.S., et al. (2016). Mechanisms of stress in the brain. <i>Nature Neuroscience</i>, 18(10), 1353–1363.",
    "McEwen, B.S. & Stellar, E. (1993). Stress and the individual: mechanisms leading to disease. <i>Archives of Internal Medicine</i>, 153(18), 2093–2101.",
    "McGowan, P.O., et al. (2009). Epigenetic regulation of the glucocorticoid receptor in human brain. <i>Nature Neuroscience</i>, 12(3), 342–348.",
    "Primack, B.A., et al. (2017). Social media use and perceived social isolation. <i>American Journal of Preventive Medicine</i>, 53(1), 1–8.",
    "Raison, C.L. & Miller, A.H. (2011). Is depression an inflammatory disorder? <i>Current Psychiatry Reports</i>, 13(6), 467–475.",
    "Rosengren, A., et al. (2004). Association of psychosocial risk factors with risk of acute myocardial infarction (INTERHEART). <i>The Lancet</i>, 364(9438), 953–962.",
    "Sapolsky, R.M. (1996). Why stress is bad for your brain. <i>Science</i>, 273(5276), 749–750.",
    "Sapolsky, R.M. (2004). <i>Why Zebras Don't Get Ulcers</i>. 3rd ed. Henry Holt and Company.",
    "Schuch, F.B., et al. (2016). Exercise as a treatment for depression: a meta-analysis. <i>Journal of Psychiatric Research</i>, 77, 42–51.",
    "Seeman, T.E., et al. (2001). Allostatic load as a marker of cumulative biological risk. <i>Proceedings of the National Academy of Sciences</i>, 98(8), 4770–4775.",
    "Segerstrom, S.C. & Miller, G.E. (2004). Psychological stress and the human immune system. <i>Psychological Bulletin</i>, 130(4), 601–630.",
    "Siegrist, J. (1996). Adverse health effects of high-effort/low-reward conditions. <i>Journal of Occupational Health Psychology</i>, 1(1), 27–41.",
    "Song, H., et al. (2018). Association of stress-related disorders with subsequent autoimmune disease. <i>JAMA</i>, 319(23), 2388–2400.",
    "Steptoe, A. & Kivimäki, M. (2013). Stress and cardiovascular disease: an update on current knowledge. <i>Annual Review of Public Health</i>, 34, 337–354.",
    "Sudo, N., et al. (2004). Postnatal microbial colonization programs the hypothalamic-pituitary-adrenal system for stress response in mice. <i>Journal of Physiology</i>, 558(1), 263–275.",
    "Tang, Y.-Y., et al. (2015). The neuroscience of mindfulness meditation. <i>Nature Reviews Neuroscience</i>, 16(4), 213–225.",
    "Templin, C., et al. (2015). Clinical features and outcomes of Takotsubo cardiomyopathy. <i>New England Journal of Medicine</i>, 373(10), 929–938.",
    "Thaker, P.H., et al. (2006). Chronic stress promotes tumor growth and angiogenesis in a mouse model of ovarian carcinoma. <i>Nature Medicine</i>, 12(8), 939–944.",
    "Vyas, A., et al. (2002). Chronic stress induces contrasting patterns of dendritic remodeling in hippocampal and amygdaloid neurons. <i>Journal of Neuroscience</i>, 22(15), 6810–6818.",
    "Waldinger, R.J. & Schulz, M.S. (2023). <i>The Good Life: Lessons from the World's Longest Scientific Study of Happiness</i>. Simon & Schuster.",
    "Walker, M.P. (2017). <i>Why We Sleep: Unlocking the Power of Sleep and Dreams</i>. Scribner.",
    "White, M.P., et al. (2019). Spending at least 120 minutes a week in nature is associated with good health and wellbeing. <i>Scientific Reports</i>, 9, 7730.",
    "WHO (2020). WHO Guidelines on Physical Activity and Sedentary Behaviour. World Health Organization.",
    "WHO (2021). Cardiovascular Diseases (CVDs) Fact Sheet. World Health Organization.",
    "Yehuda, R., et al. (2016). Holocaust exposure induced intergenerational effects on FKBP5 methylation. <i>Biological Psychiatry</i>, 80(5), 372–380.",
    "Zannas, A.S. & West, A.E. (2014). Epigenetics and the regulation of stress vulnerability and resilience. <i>Neuroscience</i>, 264, 157–170.",
]

for ref in refs:
    story.append(Paragraph(ref, styles['RefStyle']))

# =========================================================================
# BUILD PDF
# =========================================================================
doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(f"PDF generated: {output_path}")
