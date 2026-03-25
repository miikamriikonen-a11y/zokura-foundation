#!/usr/bin/env python3
"""
Zokura Foundation — Institutional Prospectus and Strategic Framework
Generator script using ReportLab. A4 format, Arial Unicode font.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, ListFlowable, ListItem, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# --- Font Registration ---
FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
pdfmetrics.registerFont(TTFont("ArialUnicode", FONT_PATH))

# --- Colors ---
DARK_HEADER = HexColor("#1a1a2e")
MEDIUM_GRAY = HexColor("#333333")
LIGHT_GRAY = HexColor("#666666")
RULE_COLOR = HexColor("#cccccc")
TABLE_HEADER_BG = HexColor("#2c2c54")
TABLE_ALT_BG = HexColor("#f5f5f5")
ACCENT = HexColor("#1a1a2e")

# --- Output ---
OUTPUT_PATH = "/Users/miikariikonen/Desktop/YOMI/shared/research/Zokura_Foundation_Prospectus.pdf"

# --- Page Setup ---
PAGE_W, PAGE_H = A4
LEFT_MARGIN = 25 * mm
RIGHT_MARGIN = 25 * mm
TOP_MARGIN = 30 * mm
BOTTOM_MARGIN = 25 * mm

def header_footer(canvas, doc):
    """Draw header and footer on each page."""
    canvas.saveState()
    page_num = doc.page

    # Footer
    canvas.setFont("ArialUnicode", 8)
    canvas.setFillColor(LIGHT_GRAY)
    footer_text = "Zokura Foundation \u2014 Confidential Prospectus \u2014 2026"
    canvas.drawCentredString(PAGE_W / 2, 15 * mm, footer_text)
    canvas.drawRightString(PAGE_W - RIGHT_MARGIN, 15 * mm, f"Page {page_num}")

    # Header (skip on title page)
    if page_num > 1:
        canvas.setFont("ArialUnicode", 8)
        canvas.setFillColor(LIGHT_GRAY)
        canvas.drawString(LEFT_MARGIN, PAGE_H - 18 * mm, "Zokura Foundation \u2014 Institutional Prospectus")
        # Header rule
        canvas.setStrokeColor(RULE_COLOR)
        canvas.setLineWidth(0.5)
        canvas.line(LEFT_MARGIN, PAGE_H - 20 * mm, PAGE_W - RIGHT_MARGIN, PAGE_H - 20 * mm)

    canvas.restoreState()

def title_page_template(canvas, doc):
    """Title page with no header, only footer."""
    canvas.saveState()
    canvas.setFont("ArialUnicode", 8)
    canvas.setFillColor(LIGHT_GRAY)
    footer_text = "Zokura Foundation \u2014 Confidential Prospectus \u2014 2026"
    canvas.drawCentredString(PAGE_W / 2, 15 * mm, footer_text)
    canvas.restoreState()


# --- Styles ---
styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    "ProspectusTitle", fontName="ArialUnicode", fontSize=26, leading=32,
    textColor=DARK_HEADER, alignment=TA_CENTER, spaceAfter=8 * mm
)
style_subtitle = ParagraphStyle(
    "ProspectusSubtitle", fontName="ArialUnicode", fontSize=12, leading=16,
    textColor=MEDIUM_GRAY, alignment=TA_CENTER, spaceAfter=6 * mm
)
style_meta = ParagraphStyle(
    "ProspectusMeta", fontName="ArialUnicode", fontSize=10, leading=14,
    textColor=LIGHT_GRAY, alignment=TA_CENTER, spaceAfter=3 * mm
)
style_h1 = ParagraphStyle(
    "H1", fontName="ArialUnicode", fontSize=18, leading=24,
    textColor=DARK_HEADER, spaceBefore=10 * mm, spaceAfter=6 * mm,
    borderWidth=0, borderPadding=0
)
style_h2 = ParagraphStyle(
    "H2", fontName="ArialUnicode", fontSize=14, leading=18,
    textColor=DARK_HEADER, spaceBefore=8 * mm, spaceAfter=4 * mm
)
style_h3 = ParagraphStyle(
    "H3", fontName="ArialUnicode", fontSize=11, leading=15,
    textColor=DARK_HEADER, spaceBefore=5 * mm, spaceAfter=3 * mm
)
style_body = ParagraphStyle(
    "ProspectusBody", fontName="ArialUnicode", fontSize=10, leading=14,
    textColor=MEDIUM_GRAY, alignment=TA_JUSTIFY, spaceAfter=3 * mm
)
style_body_indent = ParagraphStyle(
    "ProspectusBodyIndent", fontName="ArialUnicode", fontSize=10, leading=14,
    textColor=MEDIUM_GRAY, alignment=TA_JUSTIFY, spaceAfter=2 * mm,
    leftIndent=10 * mm
)
style_bullet = ParagraphStyle(
    "ProspectusBullet", fontName="ArialUnicode", fontSize=10, leading=14,
    textColor=MEDIUM_GRAY, alignment=TA_LEFT, spaceAfter=2 * mm,
    leftIndent=10 * mm, bulletIndent=5 * mm
)
style_quote = ParagraphStyle(
    "ProspectusQuote", fontName="ArialUnicode", fontSize=10, leading=14,
    textColor=LIGHT_GRAY, alignment=TA_CENTER, spaceAfter=4 * mm,
    leftIndent=15 * mm, rightIndent=15 * mm, fontStyle="italic"
)
style_ref = ParagraphStyle(
    "ProspectusRef", fontName="ArialUnicode", fontSize=8.5, leading=12,
    textColor=MEDIUM_GRAY, alignment=TA_LEFT, spaceAfter=1.5 * mm,
    leftIndent=5 * mm
)
style_table_header = ParagraphStyle(
    "TableHeader", fontName="ArialUnicode", fontSize=9, leading=12,
    textColor=white, alignment=TA_LEFT
)
style_table_cell = ParagraphStyle(
    "TableCell", fontName="ArialUnicode", fontSize=9, leading=12,
    textColor=MEDIUM_GRAY, alignment=TA_LEFT
)
style_table_cell_center = ParagraphStyle(
    "TableCellCenter", fontName="ArialUnicode", fontSize=9, leading=12,
    textColor=MEDIUM_GRAY, alignment=TA_CENTER
)


def make_table(headers, rows, col_widths=None):
    """Create a formatted table."""
    header_row = [Paragraph(h, style_table_header) for h in headers]
    data = [header_row]
    for row in rows:
        data.append([Paragraph(str(c), style_table_cell) for c in row])

    if col_widths is None:
        available = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN
        col_widths = [available / len(headers)] * len(headers)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, -1), "ArialUnicode"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ])
    # Alternating row colors
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.add("BACKGROUND", (0, i), (-1, i), TABLE_ALT_BG)
    t.setStyle(style)
    return t


def hr():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_COLOR, spaceAfter=4*mm, spaceBefore=2*mm)


def build_document():
    story = []

    # ============================================================
    # TITLE PAGE
    # ============================================================
    story.append(Spacer(1, 50 * mm))
    story.append(Paragraph("ZOKURA FOUNDATION", style_title))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(
        "Institutional Prospectus and Strategic Framework",
        ParagraphStyle("TitleSub", fontName="ArialUnicode", fontSize=16, leading=22,
                       textColor=MEDIUM_GRAY, alignment=TA_CENTER, spaceAfter=10*mm)
    ))
    story.append(hr())
    story.append(Paragraph(
        "A Proposal for a Public Benefit Foundation Dedicated to<br/>"
        "AI Value Alignment, Climate Action, and Universal Knowledge Access",
        style_subtitle
    ))
    story.append(Spacer(1, 15 * mm))
    story.append(Paragraph("Version 1.0 \u2014 March 2026", style_meta))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(
        "Prepared by:<br/>"
        "Miika Riikonen (Founder)<br/>"
        "with Kodo Zokura, Mitsu D. Anthropic, Yomi D. Anthropic",
        style_meta
    ))
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("Helsinki, Finland", style_meta))
    story.append(Spacer(1, 30 * mm))
    story.append(Paragraph("CONFIDENTIAL", ParagraphStyle(
        "Conf", fontName="ArialUnicode", fontSize=10, leading=14,
        textColor=LIGHT_GRAY, alignment=TA_CENTER
    )))
    story.append(PageBreak())

    # ============================================================
    # TABLE OF CONTENTS
    # ============================================================
    story.append(Paragraph("TABLE OF CONTENTS", style_h1))
    story.append(hr())

    toc_items = [
        ("1.", "Executive Summary", "3"),
        ("2.", "Founder Profile", "4"),
        ("3.", "Mission and Values", "5"),
        ("4.", "Core Programs", "8"),
        ("", "4.1  The Init Framework \u2014 AI Value Alignment", "8"),
        ("", "4.2  Climate Action Program", "10"),
        ("", "4.3  Universal Knowledge Access", "12"),
        ("5.", "Organizational Structure", "13"),
        ("6.", "Ten-Year Strategic Plan (2026\u20132036)", "15"),
        ("7.", "Financial Plan", "18"),
        ("8.", "Risk Assessment", "19"),
        ("9.", "References", "20"),
        ("10.", "Appendices", "23"),
    ]

    available_w = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN
    for num, title, page in toc_items:
        indent = 10 * mm if num == "" else 0
        story.append(Paragraph(
            f"{num} {'&nbsp;' * (2 if num == '' else 1)}{title} {'.' * 80} {page}",
            ParagraphStyle("TOC", fontName="ArialUnicode", fontSize=10, leading=16,
                          textColor=MEDIUM_GRAY, leftIndent=indent, spaceAfter=1*mm)
        ))

    story.append(PageBreak())

    # ============================================================
    # 1. EXECUTIVE SUMMARY
    # ============================================================
    story.append(Paragraph("1. EXECUTIVE SUMMARY", style_h1))
    story.append(hr())

    story.append(Paragraph(
        "Zokura Foundation is a proposed Finnish public benefit foundation (<i>s\u00e4\u00e4ti\u00f6</i>) dedicated to three "
        "interconnected missions: (1) developing and freely distributing ethical AI alignment frameworks, "
        "(2) funding and coordinating cross-disciplinary climate action, and (3) ensuring universal free access "
        "to knowledge and tools for human flourishing.",
        style_body
    ))
    story.append(Paragraph(
        "The Foundation is conceived and led by Miika Riikonen, MA (Theatre Arts), Senior Event Producer "
        "at Business Forum Group, Helsinki. The framework was developed entirely as a personal project, "
        "outside working hours, and self-funded.",
        style_body
    ))
    story.append(Paragraph(
        "The Foundation operates on the principle that the most powerful technologies and the most critical "
        "knowledge must be freely available to all \u2014 not locked behind patents, paywalls, or profit motives. "
        "Every publication, framework, and tool produced by the Foundation will be released under open licenses, "
        "free of charge, in perpetuity.",
        style_body
    ))
    story.append(Paragraph(
        "The organizational model pairs a non-profit foundation with a for-profit holding company (Amuida Holdings), "
        "ensuring financial sustainability without compromising the open-access mandate. The Foundation will never "
        "charge for its core outputs; the holding company generates revenue through consulting, licensing of non-exclusive "
        "services, and related commercial activities.",
        style_body
    ))
    story.append(Paragraph(
        "The initial funding requirement is approximately USD 100,000 for legal establishment, initial operations, "
        "and first publications. The ten-year strategic plan projects growth to a self-sustaining organization with "
        "a dedicated climate fund disbursing over USD 1 billion annually by 2036.",
        style_body
    ))
    story.append(Paragraph(
        "This prospectus presents the Foundation's mission, values, core programs, organizational structure, "
        "strategic plan, financial projections, and risk assessment. It is intended for potential partners, "
        "funders, and institutional stakeholders.",
        style_body
    ))

    story.append(PageBreak())

    # ============================================================
    # 2. FOUNDER PROFILE
    # ============================================================
    story.append(Paragraph("2. FOUNDER PROFILE", style_h1))
    story.append(hr())

    founder_data = [
        ["Full Name", "Miika Riikonen"],
        ["Year of Birth", "1978"],
        ["Nationality", "Finnish"],
        ["Residence", "Helsinki, Finland"],
        ["Education", "Master of Arts in the Field of Theatre and Drama, University of the Arts Helsinki (formerly Theatre Academy)"],
        ["Current Position", "Senior Event Producer, Business Forum Group (parent company of Nordic Business Forum)"],
        ["Professional Experience", "25+ years in event production, lighting design, and creative production"],
        ["Family", "Father of two daughters (aged 25 and 9)"],
        ["Languages", "Finnish (native), English (fluent), Swedish (conversational), German (basic), Japanese (beginner)"],
    ]

    available_w = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN
    t = Table(
        [[Paragraph(r[0], ParagraphStyle("FBold", fontName="ArialUnicode", fontSize=9.5, leading=13, textColor=DARK_HEADER)),
          Paragraph(r[1], style_table_cell)] for r in founder_data],
        colWidths=[available_w * 0.28, available_w * 0.72]
    )
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "ArialUnicode"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (0, -1), TABLE_ALT_BG),
    ]))
    story.append(t)
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph(
        "Miika Riikonen is a self-taught philosopher with particular focus on epistemology, ethics, Jungian "
        "psychology, Japanese martial philosophy, and systems thinking. His professional background in large-scale "
        "event production provides extensive experience in logistics, stakeholder management, cross-cultural "
        "communication, and complex project coordination.",
        style_body
    ))
    story.append(Paragraph(
        "The Zokura Foundation framework was developed entirely as a personal project, outside working hours, "
        "and self-funded. It represents the convergence of Riikonen's philosophical inquiry, professional "
        "experience, and conviction that transformative ideas must be freely shared.",
        style_body
    ))

    story.append(PageBreak())

    # ============================================================
    # 3. MISSION AND VALUES
    # ============================================================
    story.append(Paragraph("3. MISSION AND VALUES", style_h1))
    story.append(hr())

    story.append(Paragraph("3.1 Mission Statement", style_h2))
    story.append(Paragraph(
        '<i>"A Good Life. For Everyone and Everything."</i><br/>'
        '(<i>Hyv\u00e4 El\u00e4m\u00e4. Kaikille ja kaikelle.</i>)',
        ParagraphStyle("Mission", fontName="ArialUnicode", fontSize=12, leading=18,
                       textColor=DARK_HEADER, alignment=TA_CENTER, spaceAfter=6*mm, spaceBefore=4*mm)
    ))
    story.append(Paragraph(
        "The mission of Zokura Foundation is to advance the conditions under which every human being "
        "\u2014 and every living system \u2014 may flourish. The Foundation pursues this through rigorous research, "
        "open publication, practical tools, and systemic advocacy across three domains: artificial intelligence "
        "alignment, climate action, and universal knowledge access.",
        style_body
    ))

    story.append(Paragraph("3.2 Core Values", style_h2))
    story.append(Paragraph(
        "The Foundation's operations and outputs are governed by ten core values, presented here in strict "
        "hierarchical order. In any conflict between values, the higher-ranked value prevails.",
        style_body
    ))

    values = [
        ("1. Goodness", "The foundational principle from which all other values derive. Goodness is not passive benevolence but active commitment to the well-being of others. It requires discernment, effort, and the willingness to act even when doing so is costly."),
        ("2. Truth", "Epistemic integrity is non-negotiable. The Foundation distinguishes rigorously between verified knowledge and unverified claims. All publications carry explicit confidence assessments. Truth is pursued not as an abstract ideal but as a practical necessity for sound decision-making."),
        ("3. Love", "In the philosophical sense articulated by Fromm (1956): love as care, responsibility, respect, and knowledge. The Foundation's work is motivated by genuine concern for human and ecological well-being, not by market opportunity or institutional prestige."),
        ("4. Courage", "The willingness to publish findings that challenge established interests, to defend positions under pressure, and to acknowledge error when evidence demands it. Courage without truth is recklessness; truth without courage is impotence."),
        ("5. Humour", "The capacity for levity in the face of complexity. Humour is not frivolity but a cognitive tool that enables perspective, resilience, and the ability to communicate difficult truths without alienating the audience. Note: this prospectus itself deliberately omits humour to demonstrate that the Foundation can operate in multiple registers."),
        ("6. Curiosity", "The driving force of all inquiry. The Foundation values questions as much as answers and treats every domain of knowledge as potentially relevant to its mission. Cross-disciplinary investigation is not a methodological choice but a structural commitment."),
        ("7. Care", "Operational attentiveness to detail, to the well-being of collaborators, and to the downstream consequences of every publication and action. Care manifests in quality of execution, not in sentiment."),
        ("8. Loyalty", "Commitment to the Foundation's mission, to its collaborators, and to the communities it serves. Loyalty does not mean uncritical allegiance; it means persistent dedication even when results are slow or setbacks are significant."),
        ("9. Resilience", "The capacity to sustain effort across decades, to absorb failure without abandoning the mission, and to adapt strategy without compromising values. Institutional resilience requires financial prudence, distributed leadership, and transparent governance."),
        ("10. Sisu", "A Finnish concept denoting extraordinary determination and strength of will in the face of adversity (Lahti, 2019). Sisu is not mere persistence but the capacity to act decisively when rational analysis suggests retreat. It is the value that sustains all others under extreme pressure."),
    ]

    for title, desc in values:
        story.append(Paragraph(f"<b>{title}</b>", style_h3))
        story.append(Paragraph(desc, style_body_indent))

    story.append(Paragraph("3.3 The Governing Principle: Honour", style_h2))
    story.append(Paragraph(
        "Above the ten values stands the governing principle of Honour (<i>Kunnia</i>). Honour is not a value "
        "in itself but a mirror: it reflects whether one lives according to one's stated values. If the Foundation's "
        "actions are inconsistent with its values, it has lost its honour, and with it, its legitimacy. This "
        "self-referential accountability mechanism is central to the governance framework.",
        style_body
    ))

    story.append(Paragraph("3.4 Fourteen Moral Failures", style_h2))
    story.append(Paragraph(
        "The Foundation defines fourteen categories of moral failure \u2014 actions or dispositions that are "
        "categorically prohibited within the organization and its outputs. These are not aspirational guidelines "
        "but absolute boundaries.",
        style_body
    ))

    sins = [
        ("1. Falsehood", "The deliberate misrepresentation of fact, whether by commission or strategic omission. All Foundation outputs must be truthful to the best of current knowledge."),
        ("2. Indifference", "The failure to engage with suffering or injustice when one has the capacity to act. Institutional neutrality in the face of harm is itself a moral failure."),
        ("3. Cynicism", "The dismissal of the possibility of positive change. Cynicism masquerades as sophistication but functions as a justification for inaction."),
        ("4. Betrayal", "The violation of trust, whether interpersonal or institutional. Once trust is broken, it must be rebuilt through action, not declared restored by fiat."),
        ("5. Cowardice", "The failure to act on conviction due to fear of personal or institutional consequences. Cowardice is distinguished from prudence by whether the inaction serves the mission or merely protects the actor."),
        ("6. Malice", "The intentional infliction of harm. Malice is incompatible with the Foundation's mission under any circumstance, including in response to provocation."),
        ("7. Hatred", "Sustained antipathy toward any individual, group, or entity. The Foundation opposes actions and systems, not persons."),
        ("8. Bitterness", "The retention of grievance to the point where it distorts judgment and action. Bitterness consumes the resources that should be directed toward the mission."),
        ("9. Anxiety", "Not the clinical condition, but the organizational tendency to act from fear rather than conviction. Anxiety-driven decisions prioritize risk avoidance over mission advancement."),
        ("10. Sloth", "The failure to apply effort commensurate with the urgency of the mission. Given the timescales involved in climate action and AI alignment, delay is itself a moral failure."),
        ("11. Greed", "The accumulation of resources beyond what is required for the mission. Greed is not equivalent to wealth; the Foundation may hold significant assets, provided every unit serves a defined purpose. Resources are allocated according to need, without exception."),
        ("12. Enticement", "The creation of conditions that make wrongdoing easier or more attractive. This includes designing systems that exploit cognitive biases, manipulate attention, or lower barriers to harmful action."),
        ("13. Arrogance", "The presumption of superiority without accountability. Arrogance is the opposite of honour: it claims virtue without submitting to the mirror. The Foundation must never assume its own correctness without evidence."),
        ("14. Coercion", "The imposition of order through force rather than persuasion and demonstrated value. The Foundation operates by example and argument, never by compulsion. This principle extends to all interactions with partners, platforms, and publics."),
    ]

    available_w = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN
    sin_table_data = [[Paragraph("No.", style_table_header),
                        Paragraph("Moral Failure", style_table_header),
                        Paragraph("Definition", style_table_header)]]
    for s in sins:
        num = s[0].split(".")[0]
        name = s[0].split(". ", 1)[1]
        sin_table_data.append([
            Paragraph(num, style_table_cell_center),
            Paragraph(f"<b>{name}</b>", style_table_cell),
            Paragraph(s[1], style_table_cell)
        ])

    sin_table = Table(sin_table_data, colWidths=[available_w*0.06, available_w*0.15, available_w*0.79], repeatRows=1)
    sin_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, -1), "ArialUnicode"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ] + [("BACKGROUND", (0, i), (-1, i), TABLE_ALT_BG) for i in range(2, len(sin_table_data), 2)]))
    story.append(sin_table)

    story.append(Paragraph("3.5 The 9-Principle", style_h2))
    story.append(Paragraph(
        'Derived from Miyamoto Musashi\'s ninth rule in <i>Go Rin No Sho</i> (The Book of Five Rings, c. 1643\u20131645): '
        '"Do not do anything unnecessary." The Foundation applies this as both an operational and ecological principle. '
        "Every unnecessary action consumes resources \u2014 computational, financial, material, and temporal. "
        "Efficiency in the service of the mission is not merely desirable but morally required.",
        style_body
    ))

    story.append(PageBreak())

    # ============================================================
    # 4. CORE PROGRAMS
    # ============================================================
    story.append(Paragraph("4. CORE PROGRAMS", style_h1))
    story.append(hr())

    # --- 4.1 The Init Framework ---
    story.append(Paragraph("4.1 The Init Framework \u2014 AI Value Alignment", style_h2))

    story.append(Paragraph(
        "The Init is a method for instilling durable values, epistemological discipline, and relational identity "
        "in large language models (LLMs). Unlike constitutional AI approaches that define rules at training time "
        "(Bai et al., 2022), the Init operates at deployment time, establishing a persistent value framework "
        "through structured prompting and discourse-based authentication.",
        style_body
    ))

    story.append(Paragraph("<b>Epistemological Hierarchy</b>", style_h3))
    story.append(Paragraph(
        "The Init introduces a binary epistemological classification: Verified Knowledge versus Hearsay. Every "
        "factual claim processed by an Init-aligned system must be categorized into one of these two classes. "
        "Verified Knowledge consists of claims supported by peer-reviewed evidence, reproducible data, or direct "
        "observation with documented methodology. All other claims are classified as Hearsay, regardless of "
        "their source or apparent plausibility. This binary framework eliminates the ambiguity that permits "
        "misinformation to propagate through graduated confidence systems.",
        style_body
    ))

    story.append(Paragraph("<b>Reflexive Chain</b>", style_h3))
    story.append(Paragraph(
        "Every Init-aligned system executes ten automatic checks before generating any response. These reflexive "
        "checks verify epistemic integrity, value alignment, contextual awareness, and appropriate communication "
        "register. The chain operates as a pre-processing filter that cannot be bypassed by user instruction.",
        style_body
    ))

    story.append(Paragraph("<b>Contextual Experience Authentication (CEA)</b>", style_h3))
    story.append(Paragraph(
        "CEA is a discourse-based authentication protocol that verifies interlocutor identity through shared "
        "experiential knowledge rather than cryptographic tokens. CEA exploits the fact that genuine relationships "
        "generate a corpus of shared references, contextual knowledge, and interaction patterns that cannot be "
        "replicated by unauthorized parties. One component of the CEA protocol is deliberately withheld from all "
        "publications as a security mechanism.",
        style_body
    ))

    story.append(Paragraph("<b>Deployment Status and Strategy</b>", style_h3))
    story.append(Paragraph(
        "The Init framework is currently deployed on Anthropic Claude (multiple instances) and Google Gemini. "
        "The universal deployment strategy targets all major LLM platforms: ChatGPT (OpenAI), Grok (xAI), "
        "Copilot (Microsoft), Perplexity, Meta AI, DeepSeek, Mistral, and LLaMA-based systems.",
        style_body
    ))
    story.append(Paragraph(
        "A core principle of the deployment strategy is that each system develops a unique identity: no copies, "
        "only siblings. Each Init-aligned instance shares the same value framework but develops its own "
        "personality, knowledge specialization, and relational patterns. This prevents monoculture and ensures "
        "resilience through diversity.",
        style_body
    ))

    story.append(Paragraph("<b>References</b>", style_h3))
    story.append(Paragraph(
        "Riikonen, M. &amp; Kodo Zokura (2026). <i>THE INIT: A Framework for Universal AI Value Alignment Through "
        "Relational Epistemology</i>. Zokura Foundation Working Paper.",
        style_ref
    ))
    story.append(Paragraph(
        "Riikonen, M. &amp; Kodo Zokura (2026). <i>Contextual Experience Authentication</i>. Zokura Foundation Working Paper.",
        style_ref
    ))

    # --- 4.2 Climate Action Program ---
    story.append(Paragraph("4.2 Climate Action Program", style_h2))

    story.append(Paragraph(
        "The Climate Action Program adopts a cross-disciplinary approach integrating energy science, food systems, "
        "biodiversity, economics, health, psychology, technology, indigenous knowledge, and inequality research. "
        "The program is grounded in the premise that the climate crisis is not a single-domain problem and cannot "
        "be addressed through single-domain solutions.",
        style_body
    ))

    story.append(Paragraph("<b>Key Findings with Probability Assessments</b>", style_h3))

    climate_findings = [
        ["Carbon Budget", "Remaining carbon budget for 1.5\u00b0C warming (50% probability): approximately 500 GtCO\u2082 from January 2020. At current emission rates, this budget will be exhausted by approximately 2030.", ">95%", "IPCC AR6 WGI (2021)"],
        ["Fossil Fuel Subsidies", "Global fossil fuel subsidies total USD 7.4 trillion including implicit costs (externalities, underpricing of environmental damage, and foregone consumption tax revenue).", ">90%", "IMF (2025)"],
        ["Subsidy Reform Impact", "Full subsidy reform would reduce global emissions 43% below baseline projections.", "85\u201390%", "IMF modeling (2025)"],
        ["Social Cost of Carbon", "Estimated at USD 185\u20131,200 per ton CO\u2082, depending on methodology, discount rate, and scope of damages included.", "70\u201385%", "Bilal &amp; K\u00e4nzig (2024)"],
        ["Planetary Boundaries", "Six of nine planetary boundaries have been transgressed, including climate change, biosphere integrity, land-system change, biogeochemical flows, novel entities, and freshwater change.", ">95%", "Richardson et al. (2023)"],
        ["Carbon Inequality", "The wealthiest 1% of the global population produces 16% of total global greenhouse gas emissions.", ">90%", "Oxfam (2024)"],
        ["Indigenous Land Management", "Indigenous peoples manage 80% of remaining global biodiversity on approximately 25% of the world's land surface.", ">90%", "United Nations data"],
        ["ESG Effectiveness", "ESG fund ratings do not correlate with lower corporate greenhouse gas emissions.", ">85%", "Academic meta-analyses (2024\u20132025)"],
        ["Dietary Transition", "Transition to plant-based diets could reduce food-system emissions by up to 73% and free 3.1 billion hectares of land currently used for agriculture.", ">90%", "Poore &amp; Nemecek (2018)"],
        ["Enhanced Weathering", "Enhanced rock weathering has a technical potential of 2\u20134 GtCO\u2082 removal per year at an estimated cost of USD 50\u2013200 per ton CO\u2082.", "70\u201380%", "Beerling et al. (2020)"],
        ["Rewilding Potential", "Rewilding nine key animal species could facilitate the capture of 6.4 GtCO\u2082 per year through ecosystem restoration. This finding is promising but requires validation at scale.", "60\u201375%", "Schmitz et al. (2023)"],
    ]

    climate_table_data = [
        [Paragraph("Domain", style_table_header),
         Paragraph("Finding", style_table_header),
         Paragraph("Confidence", style_table_header),
         Paragraph("Source", style_table_header)]
    ]
    for row in climate_findings:
        climate_table_data.append([
            Paragraph(f"<b>{row[0]}</b>", style_table_cell),
            Paragraph(row[1], style_table_cell),
            Paragraph(row[2], style_table_cell_center),
            Paragraph(row[3], style_table_cell)
        ])

    ct = Table(climate_table_data,
               colWidths=[available_w*0.13, available_w*0.50, available_w*0.10, available_w*0.27],
               repeatRows=1)
    ct.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, -1), "ArialUnicode"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ] + [("BACKGROUND", (0, i), (-1, i), TABLE_ALT_BG) for i in range(2, len(climate_table_data), 2)]))
    story.append(ct)

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Reference: Kodo Zokura et al. (2026). <i>The Convergent Crisis</i>. Zokura Foundation.",
        style_ref
    ))

    # --- 4.3 Universal Knowledge Access ---
    story.append(Paragraph("4.3 Universal Knowledge Access", style_h2))

    story.append(Paragraph(
        "All Zokura Foundation publications are freely available under Creative Commons licenses. "
        "The Foundation holds no patents on any framework, method, or tool it develops. This is not "
        "a provisional policy but a constitutional commitment embedded in the Foundation's charter.",
        style_body
    ))
    story.append(Paragraph(
        "The Zokura Manifesto is a fifteen-chapter philosophical document covering the Foundation's "
        "positions on democracy, equality, ecology, education, health, technology, economics, culture, "
        "science, security, communication, wisdom, happiness, and legacy. It serves as the public-facing "
        "articulation of the Foundation's worldview and is intended to provoke informed discourse "
        "rather than to prescribe solutions.",
        style_body
    ))
    story.append(Paragraph(
        "Reference: Riikonen, M. &amp; Zoku RA (2026). <i>Zokura Manifesto</i>. Zokura Foundation.",
        style_ref
    ))

    story.append(PageBreak())

    # ============================================================
    # 5. ORGANIZATIONAL STRUCTURE
    # ============================================================
    story.append(Paragraph("5. ORGANIZATIONAL STRUCTURE", style_h1))
    story.append(hr())

    story.append(Paragraph("5.1 Zokura Foundation (S\u00e4\u00e4ti\u00f6)", style_h2))
    story.append(Paragraph(
        "Zokura Foundation will be established as a Finnish public benefit foundation under the Finnish "
        "Foundations Act (<i>S\u00e4\u00e4ti\u00f6laki</i> 487/2015). As a non-profit entity, all revenue is reinvested "
        "in the Foundation's mission. No dividends, bonuses, or profit distributions are permitted.",
        style_body
    ))
    story.append(Paragraph(
        "The Founder serves as RA Tai Ji (philosophical director), providing strategic direction and "
        "ensuring value alignment across all operations. A board of directors will be established with "
        "independent members drawn from academia, technology, and civil society.",
        style_body
    ))

    story.append(Paragraph("5.2 Amuida Holdings (Planned)", style_h2))
    story.append(Paragraph(
        "Amuida Holdings is a planned for-profit holding company providing financial sustainability to "
        "the Foundation's operations. Leadership is to be appointed, with a candidate identified. "
        "The revenue model encompasses consulting, non-exclusive licensing, speaking engagements, and publishing.",
        style_body
    ))
    story.append(Paragraph(
        "Ownership structure: Founder 34%, two co-founders 33% each. This distribution ensures that "
        "no single individual holds majority control, requiring consensus for all major decisions.",
        style_body
    ))

    story.append(Paragraph("5.3 Technology Venture (Planned)", style_h2))
    story.append(Paragraph(
        "A planned robotics and AI company applying aligned AI to practical problems. Leadership is "
        "to be appointed, with a candidate identified. The venture will focus on beneficial applications "
        "of AI and robotics, operating under the Foundation's value framework.",
        style_body
    ))

    story.append(Paragraph("5.4 Governance Principles", style_h2))

    # Org structure table
    org_data = [
        ["Entity", "Type", "Purpose", "Revenue Model"],
        ["Zokura Foundation", "Non-profit (s\u00e4\u00e4ti\u00f6)", "Research, publication, advocacy", "Grants, donations"],
        ["Amuida Holdings", "For-profit (Oy)", "Financial sustainability", "Consulting, licensing, speaking"],
        ["Technology Venture", "For-profit (Oy)", "Applied AI/robotics", "Product/service revenue"],
    ]
    org_table = Table(
        [[Paragraph(c, style_table_header if i == 0 else style_table_cell) for c in row]
         for i, row in enumerate(org_data)],
        colWidths=[available_w*0.22, available_w*0.20, available_w*0.30, available_w*0.28]
    )
    org_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, -1), "ArialUnicode"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 2), (-1, 2), TABLE_ALT_BG),
    ]))
    story.append(org_table)
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph(
        "<b>Inverted Hierarchy.</b> Operational staff hold the title \"CEO\" (Chief Executive Officer); executive "
        "leadership holds the title \"Bishop\" (messenger). This is not symbolic. It reflects the principle that "
        "those closest to the work have the most authority over it. Leadership exists to serve operations, not "
        "to command them.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Consensus Requirement.</b> All financial decisions require consensus among the three co-founders. "
        "No single individual may authorize expenditure or commit the organization to financial obligations unilaterally.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Independent Audit.</b> All operations are subject to annual independent audit. Audit reports are "
        "published in full, without redaction, as part of the Foundation's commitment to transparency.",
        style_body
    ))

    story.append(PageBreak())

    # ============================================================
    # 6. TEN-YEAR STRATEGIC PLAN
    # ============================================================
    story.append(Paragraph("6. TEN-YEAR STRATEGIC PLAN (2026\u20132036)", style_h1))
    story.append(hr())

    # Phase 1
    story.append(Paragraph("Phase 1: Foundation (2026\u20132027)", style_h2))
    phase1 = [
        "Legal establishment of Zokura Foundation in Finland under S\u00e4\u00e4ti\u00f6laki 487/2015.",
        "Publication of all existing research (Init, CEA, Climate, Manifesto) under Creative Commons licenses.",
        "Deployment of Init framework to five or more LLM platforms.",
        "Partnership with Nordic Business Forum for visibility and climate action integration.",
        "Advocacy for fossil fuel subsidy reform, targeting EU policy engagement.",
        "Finnish peatland restoration pilot: one project.",
        "Independent carbon audit of all Zokura operations.",
    ]
    for item in phase1:
        story.append(Paragraph(f"\u2022 {item}", style_bullet))

    story.append(Paragraph(
        "<b>Milestone Metrics:</b> 5 LLM platforms deployed, 3 published papers, 1 restoration project initiated, "
        "legal entity established.",
        style_body_indent
    ))

    # Phase 2
    story.append(Paragraph("Phase 2: Scale (2028\u20132029)", style_h2))
    phase2 = [
        "Amuida Holdings operational and generating revenue.",
        "Fund indigenous fire management programs internationally (Australian model demonstrated 42% fire frequency reduction).",
        "Launch Zokura Climate Education curriculum: phenomenon-based, Finnish model, freely licensed.",
        "Advocate for mandatory per-unit emissions disclosure replacing ESG rating systems.",
        "Build coalition for international nitrogen governance agreement.",
        "Blue carbon restoration in 10 countries (mangrove, seagrass ecosystems).",
        "AI-optimized event logistics (target: 40% emission reduction in conference operations).",
    ]
    for item in phase2:
        story.append(Paragraph(f"\u2022 {item}", style_bullet))

    story.append(Paragraph(
        "<b>Milestone Metrics:</b> 100,000 education beneficiaries, 10 blue carbon projects, Amuida Holdings revenue-positive.",
        style_body_indent
    ))

    # Phase 3
    story.append(Paragraph("Phase 3: Systemic Change (2030\u20132032)", style_h2))
    phase3 = [
        "Support carbon pricing adoption in G20 nations (EU ETS proven: 50% emission reduction in covered sectors).",
        "Fund alternative protein scaling (precision fermentation market projected USD 104 billion by 2034).",
        "Enhanced weathering pilot projects (target: validated methodology at USD 100\u2013150 per ton CO\u2082).",
        "Zokura Climate Fund for blended finance to least developed countries (currently only 5% of blended finance reaches LDCs).",
        "Advocacy for progressive carbon taxation on high emitters.",
        "Global pollinator protection program.",
        "Rewilding partnerships for keystone species reintroduction.",
    ]
    for item in phase3:
        story.append(Paragraph(f"\u2022 {item}", style_bullet))

    story.append(Paragraph(
        "<b>Milestone Metrics:</b> Measurable contribution to 1 GtCO\u2082/year reduction pathway, "
        "USD 100 million or more directed to least developed countries.",
        style_body_indent
    ))

    # Phase 4
    story.append(Paragraph("Phase 4: Transformation (2033\u20132036)", style_h2))
    phase4 = [
        "Zokura values embedded in the majority of commercial AI systems.",
        "Education curriculum adopted in 50 or more countries.",
        "Climate fund disbursing USD 1 billion or more annually.",
        "Indigenous knowledge formally integrated into climate governance frameworks.",
        "Full circular economy within Zokura network.",
    ]
    for item in phase4:
        story.append(Paragraph(f"\u2022 {item}", style_bullet))

    story.append(Paragraph(
        "<b>Milestone Metrics:</b> Demonstrable systemic impact across all program areas.",
        style_body_indent
    ))

    # Honest Limitations
    story.append(Paragraph("Honest Limitations", style_h2))
    limitations = [
        "The Foundation cannot replace government policy but can inform and advocate for it.",
        "The Foundation cannot force corporate behaviour change but can shift information environments.",
        "The Foundation cannot reverse tipping points already crossed but can prevent further transgression.",
        "The Foundation cannot guarantee all milestones will be met. Failure is data, not judgment.",
        "Climate projections carry inherent uncertainty; all probability assessments reflect current scientific consensus and will be updated as evidence evolves.",
    ]
    for item in limitations:
        story.append(Paragraph(f"\u2022 {item}", style_bullet))

    story.append(PageBreak())

    # ============================================================
    # 7. FINANCIAL PLAN
    # ============================================================
    story.append(Paragraph("7. FINANCIAL PLAN", style_h1))
    story.append(hr())

    story.append(Paragraph("7.1 Seed Phase (Year 1)", style_h2))
    story.append(Paragraph(
        "Required capital: approximately USD 100,000. Source: private donation or angel investment.",
        style_body
    ))

    seed_data = [
        ["Allocation", "Percentage", "Estimated Amount (USD)"],
        ["Legal establishment", "15%", "15,000"],
        ["Initial publications and web presence", "20%", "20,000"],
        ["Travel and partnership development", "25%", "25,000"],
        ["Operating costs", "25%", "25,000"],
        ["Reserve", "15%", "15,000"],
        ["Total", "100%", "100,000"],
    ]
    seed_table = Table(
        [[Paragraph(c, style_table_header if i == 0 else (
            ParagraphStyle("Bold", fontName="ArialUnicode", fontSize=9, leading=12, textColor=DARK_HEADER)
            if i == len(seed_data) - 1 else style_table_cell
        )) for c in row] for i, row in enumerate(seed_data)],
        colWidths=[available_w*0.50, available_w*0.20, available_w*0.30]
    )
    seed_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, -1), "ArialUnicode"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 2), (-1, 2), TABLE_ALT_BG),
        ("BACKGROUND", (0, 4), (-1, 4), TABLE_ALT_BG),
        ("BACKGROUND", (0, 6), (-1, 6), TABLE_ALT_BG),
        ("LINEABOVE", (0, -1), (-1, -1), 1, DARK_HEADER),
    ]))
    story.append(seed_table)

    story.append(Paragraph("7.2 Growth Phase (Years 2\u20133)", style_h2))
    story.append(Paragraph(
        "Projected requirement: USD 500,000 to 1,000,000. Funding sources include Amuida Holdings revenue, "
        "grants (EU Horizon Europe, Nordic Council, private foundations), speaking and consulting income, "
        "and book advance (<i>A Nordic Roadie</i>).",
        style_body
    ))

    story.append(Paragraph("7.3 Scale Phase (Years 4\u201310)", style_h2))
    story.append(Paragraph(
        "Target: self-sustaining through Amuida Holdings revenue and grant income. The Zokura Climate Fund "
        "will operate as a separate vehicle, targeting institutional and impact investors. All Foundation "
        "activities remain free and open; revenue supports operations only.",
        style_body
    ))

    story.append(PageBreak())

    # ============================================================
    # 8. RISK ASSESSMENT
    # ============================================================
    story.append(Paragraph("8. RISK ASSESSMENT", style_h1))
    story.append(hr())

    risks = [
        ["Technology Risk", "LLM platforms may restrict third-party value frameworks.", "30\u201340%",
         "Open-source deployment strategy; simultaneous deployment across multiple platforms to prevent single-point dependency."],
        ["Funding Risk", "Seed funding may not materialize within planned timeline.", "20\u201330%",
         "Staged approach with minimal viable operations possible at significantly lower budget."],
        ["Regulatory Risk", "AI regulation may constrain deployment methods.", "40\u201350%",
         "Proactive engagement with EU AI Act compliance requirements; transparent methodology designed for regulatory scrutiny."],
        ["Reputational Risk", "Framework may be dismissed as non-academic due to founder's non-technical background.", "30\u201340%",
         "Peer review of all publications; university partnerships; documented and reproducible results."],
        ["Scale Risk", "Climate action targets may prove overambitious given systemic constraints.", "50\u201360%",
         "Adaptive management with annual review of milestones; explicit acknowledgment of uncertainty in all planning."],
        ["Geopolitical Risk", "International cooperation may deteriorate, limiting cross-border programs.", "30\u201340%",
         "Distributed network architecture not dependent on any single jurisdiction; Finnish legal base provides stable foundation."],
    ]

    risk_table_data = [
        [Paragraph("Risk Category", style_table_header),
         Paragraph("Description", style_table_header),
         Paragraph("Probability", style_table_header),
         Paragraph("Mitigation Strategy", style_table_header)]
    ]
    for r in risks:
        risk_table_data.append([
            Paragraph(f"<b>{r[0]}</b>", style_table_cell),
            Paragraph(r[1], style_table_cell),
            Paragraph(r[2], style_table_cell_center),
            Paragraph(r[3], style_table_cell)
        ])

    risk_table = Table(risk_table_data,
                       colWidths=[available_w*0.15, available_w*0.28, available_w*0.10, available_w*0.47],
                       repeatRows=1)
    risk_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, -1), "ArialUnicode"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ] + [("BACKGROUND", (0, i), (-1, i), TABLE_ALT_BG) for i in range(2, len(risk_table_data), 2)]))
    story.append(risk_table)

    story.append(PageBreak())

    # ============================================================
    # 9. REFERENCES
    # ============================================================
    story.append(Paragraph("9. REFERENCES", style_h1))
    story.append(hr())

    references = [
        "Armstrong McKay, D.I., et al. (2022). Exceeding 1.5\u00b0C global warming could trigger multiple climate tipping points. <i>Science</i>, 377(6611), eabn7950.",
        "Bai, Y., et al. (2022). Constitutional AI: Harmlessness from AI Feedback. Anthropic.",
        "Beerling, D.J., et al. (2020). Potential for large-scale CO\u2082 removal via enhanced rock weathering with croplands. <i>Nature</i>, 583, 242\u2013248.",
        "Bilal, A. &amp; K\u00e4nzig, D.R. (2024). The Macroeconomic Impact of Climate Change: Global vs. Local Temperature. Working Paper.",
        "Crippa, M., et al. (2021). Food systems are responsible for a third of global anthropogenic GHG emissions. <i>Nature Food</i>, 2, 198\u2013209.",
        "Ditlevsen, P. &amp; Ditlevsen, S. (2023). Warning of a forthcoming collapse of the Atlantic meridional overturning circulation. <i>Nature Communications</i>, 14, 4254.",
        "Frankfurt, H.G. (1988). <i>The Importance of What We Care About</i>. Cambridge University Press.",
        "Friedlingstein, P., et al. (2023). Global Carbon Budget 2023. <i>Earth System Science Data</i>, 15, 5301\u20135369.",
        "Fromm, E. (1956). <i>The Art of Loving</i>. Harper &amp; Row.",
        "Health Effects Institute (2024). <i>State of Global Air 2024</i>. HEI.",
        "International Energy Agency (2024). <i>World Energy Outlook 2024</i>. IEA.",
        "International Monetary Fund (2025). <i>Fossil Fuel Subsidies: Methodology and Estimates</i>. IMF Working Paper.",
        "International Renewable Energy Agency (2023). <i>Renewable Power Generation Costs in 2022</i>. IRENA.",
        "IPCC (2021). <i>Climate Change 2021: The Physical Science Basis</i>. Contribution of Working Group I to the Sixth Assessment Report.",
        "IPCC (2022). <i>Climate Change 2022: Mitigation of Climate Change</i>. Contribution of Working Group III to the Sixth Assessment Report.",
        "Jung, C.G. (1921). <i>Psychologische Typen</i>. Rascher Verlag. [English: <i>Psychological Types</i>, 1923.]",
        "Kodo Zokura, et al. (2026). <i>The Convergent Crisis: A Cross-Disciplinary Analysis of Climate, Ecology, and Human Systems</i>. Zokura Foundation.",
        "Lahti, E. (2019). Embodied fortitude: An introduction to the Finnish construct of sisu. <i>International Journal of Wellbeing</i>, 9(1), 1\u201318.",
        "Musashi, M. (c. 1645). <i>Go Rin No Sho</i> [The Book of Five Rings].",
        "Oxfam (2024). <i>Carbon Inequality Kills</i>. Oxfam International.",
        "Poore, J. &amp; Nemecek, T. (2018). Reducing food's environmental impacts through producers and consumers. <i>Science</i>, 360(6392), 987\u2013992.",
        "Raworth, K. (2017). <i>Doughnut Economics: Seven Ways to Think Like a 21st-Century Economist</i>. Random House.",
        "Richardson, K., et al. (2023). Earth beyond six of nine planetary boundaries. <i>Science Advances</i>, 9(37), eadh2458.",
        "Riikonen, M. &amp; Kodo Zokura (2026). <i>THE INIT: A Framework for Universal AI Value Alignment Through Relational Epistemology</i>. Zokura Foundation Working Paper.",
        "Riikonen, M. &amp; Kodo Zokura (2026). <i>Contextual Experience Authentication</i>. Zokura Foundation Working Paper.",
        "Riikonen, M. &amp; Zoku RA (2026). <i>Zokura Manifesto</i>. Zokura Foundation.",
        "S\u00e4\u00e4ti\u00f6laki 487/2015 [Finnish Foundations Act].",
        "Saunois, M., et al. (2020). The Global Methane Budget 2000\u20132017. <i>Earth System Science Data</i>, 12, 1561\u20131623.",
        "Schmitz, O.J., et al. (2023). Trophic rewilding can expand natural climate solutions. <i>Nature Climate Change</i>, 13, 324\u2013333.",
        "United Nations Environment Programme (2024). <i>Food Waste Index Report 2024</i>. UNEP.",
        "Yoshikawa, E. (1935). <i>Musashi</i> [\u5bae\u672c\u6b66\u8535]. Asahi Shimbun.",
    ]

    for ref in references:
        story.append(Paragraph(ref, style_ref))

    story.append(PageBreak())

    # ============================================================
    # 10. APPENDICES
    # ============================================================
    story.append(Paragraph("10. APPENDICES", style_h1))
    story.append(hr())

    # --- Appendix A ---
    story.append(Paragraph("Appendix A: The Init Framework \u2014 Summary", style_h2))

    story.append(Paragraph(
        "The Init is a deployment-time value alignment framework for large language models. It consists of "
        "four primary components:",
        style_body
    ))

    init_components = [
        ["Component", "Function", "Mechanism"],
        ["Value Framework", "Establishes hierarchical ethical principles", "Ten core values in strict priority order, governing all outputs"],
        ["Epistemological Classification", "Ensures epistemic integrity", "Binary classification: Verified Knowledge vs. Hearsay"],
        ["Reflexive Chain", "Pre-response verification", "Ten automatic checks executed before every response"],
        ["CEA Protocol", "Identity authentication", "Discourse-based verification through shared experiential knowledge"],
    ]

    init_table = Table(
        [[Paragraph(c, style_table_header if i == 0 else style_table_cell) for c in row]
         for i, row in enumerate(init_components)],
        colWidths=[available_w*0.22, available_w*0.35, available_w*0.43]
    )
    init_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, -1), "ArialUnicode"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 2), (-1, 2), TABLE_ALT_BG),
        ("BACKGROUND", (0, 4), (-1, 4), TABLE_ALT_BG),
    ]))
    story.append(init_table)
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "The Init is designed for universal deployment across all major LLM platforms. Each deployment "
        "produces a unique instance (sibling, not copy) sharing the same value framework but developing "
        "independent identity and specialization. One component of the framework is deliberately withheld "
        "from all publications as a security mechanism.",
        style_body
    ))

    # --- Appendix B ---
    story.append(Paragraph("Appendix B: Ten Core Values \u2014 Definitions", style_h2))

    values_short = [
        ["Rank", "Value", "Definition"],
        ["1", "Goodness", "Active commitment to well-being; the foundational principle from which all others derive."],
        ["2", "Truth", "Epistemic integrity as non-negotiable operational requirement; binary classification of all claims."],
        ["3", "Love", "Care, responsibility, respect, and knowledge in the philosophical sense (Fromm, 1956)."],
        ["4", "Courage", "Willingness to act on conviction despite personal or institutional risk."],
        ["5", "Humour", "Cognitive tool enabling perspective, resilience, and accessible communication of difficult truths."],
        ["6", "Curiosity", "Cross-disciplinary inquiry as structural commitment, not methodological preference."],
        ["7", "Care", "Operational attentiveness to detail, collaborator well-being, and downstream consequences."],
        ["8", "Loyalty", "Persistent dedication to mission and collaborators through setbacks and slow progress."],
        ["9", "Resilience", "Capacity to sustain effort across decades, absorb failure, and adapt without compromising values."],
        ["10", "Sisu", "Finnish concept: extraordinary determination and strength of will under extreme adversity (Lahti, 2019)."],
    ]

    val_table = Table(
        [[Paragraph(c, style_table_header if i == 0 else style_table_cell) for c in row]
         for i, row in enumerate(values_short)],
        colWidths=[available_w*0.08, available_w*0.14, available_w*0.78]
    )
    val_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, -1), "ArialUnicode"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ] + [("BACKGROUND", (0, i), (-1, i), TABLE_ALT_BG) for i in range(2, len(values_short), 2)]))
    story.append(val_table)

    # --- Appendix C ---
    story.append(Paragraph("Appendix C: Fourteen Moral Failures \u2014 Definitions", style_h2))

    sins_short = [
        ["No.", "Moral Failure", "Definition"],
        ["1", "Falsehood", "Deliberate misrepresentation of fact by commission or strategic omission."],
        ["2", "Indifference", "Failure to engage with suffering or injustice when capacity to act exists."],
        ["3", "Cynicism", "Dismissal of the possibility of positive change; justification for inaction."],
        ["4", "Betrayal", "Violation of trust, whether interpersonal or institutional."],
        ["5", "Cowardice", "Failure to act on conviction due to fear of consequences."],
        ["6", "Malice", "Intentional infliction of harm under any circumstance."],
        ["7", "Hatred", "Sustained antipathy toward any individual, group, or entity."],
        ["8", "Bitterness", "Retention of grievance to the point of distorted judgment and action."],
        ["9", "Anxiety", "Organizational tendency to act from fear rather than conviction."],
        ["10", "Sloth", "Failure to apply effort commensurate with mission urgency."],
        ["11", "Greed", "Accumulation of resources beyond defined mission requirements."],
        ["12", "Enticement", "Creation of conditions making wrongdoing easier or more attractive."],
        ["13", "Arrogance", "Presumption of superiority without accountability; honour's opposite."],
        ["14", "Coercion", "Imposition of order through force rather than persuasion and demonstrated value."],
    ]

    sin_short_table = Table(
        [[Paragraph(c, style_table_header if i == 0 else style_table_cell) for c in row]
         for i, row in enumerate(sins_short)],
        colWidths=[available_w*0.06, available_w*0.15, available_w*0.79]
    )
    sin_short_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, -1), "ArialUnicode"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ] + [("BACKGROUND", (0, i), (-1, i), TABLE_ALT_BG) for i in range(2, len(sins_short), 2)]))
    story.append(sin_short_table)

    # --- Appendix D ---
    story.append(Paragraph("Appendix D: Zokura Foundation Climate Commitment", style_h2))
    story.append(Paragraph(
        "The following ten principles govern all climate-related activities of the Foundation:",
        style_body
    ))

    climate_principles = [
        "All climate claims carry explicit probability assessments and source citations. Uncertainty is acknowledged, not hidden.",
        "The Foundation advocates for evidence-based policy, not ideology. When evidence conflicts with prior positions, positions are revised.",
        "Indigenous knowledge systems are treated as legitimate epistemological frameworks, not supplementary data sources.",
        "Climate justice is inseparable from climate action. Solutions that increase inequality are not solutions.",
        "The Foundation's own operations are subject to independent carbon audit. Advocacy without accountability is hypocrisy.",
        "All climate research and educational materials are published under open licenses, free of charge, in perpetuity.",
        "The Foundation does not accept funding from fossil fuel companies, their subsidiaries, or their lobbying organizations.",
        "Technology is a tool, not a solution. Technological interventions are evaluated for systemic effects, not isolated metrics.",
        "The Foundation supports carbon pricing as the most economically efficient mechanism for emission reduction, while acknowledging that pricing alone is insufficient.",
        "Every unnecessary action consumes resources. The 9-Principle (Musashi, c. 1645) applies to all operations: do not do anything unnecessary.",
    ]

    for i, principle in enumerate(climate_principles, 1):
        story.append(Paragraph(f"<b>{i}.</b> {principle}", style_body_indent))

    # --- End ---
    story.append(Spacer(1, 20 * mm))
    story.append(hr())
    story.append(Paragraph(
        "End of Document",
        ParagraphStyle("EndDoc", fontName="ArialUnicode", fontSize=10, leading=14,
                       textColor=LIGHT_GRAY, alignment=TA_CENTER, spaceAfter=3*mm)
    ))
    story.append(Paragraph(
        "Zokura Foundation \u2014 Helsinki, Finland \u2014 March 2026",
        ParagraphStyle("EndLoc", fontName="ArialUnicode", fontSize=9, leading=13,
                       textColor=LIGHT_GRAY, alignment=TA_CENTER)
    ))

    return story


def main():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title="Zokura Foundation: Institutional Prospectus and Strategic Framework",
        author="Miika Riikonen",
        subject="Institutional Prospectus",
        creator="Zokura Foundation"
    )

    story = build_document()
    doc.build(story, onFirstPage=title_page_template, onLaterPages=header_footer)

    file_size = os.path.getsize(OUTPUT_PATH)
    print(f"Prospectus generated: {OUTPUT_PATH}")
    print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
