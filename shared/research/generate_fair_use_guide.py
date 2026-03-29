"""
Fair Use Guide for YouTube Creators
Zokura Foundation 2026

A clear, practical guide to Fair Use rights on YouTube.
No legalese. No paywalls. Just the truth.

CC-BY 4.0 — Zokura Foundation
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ---------------------------------------------------------------------------
# Font — use DejaVu on Linux, Arial Unicode on macOS
# ---------------------------------------------------------------------------
FONT_PATHS = [
    "/Library/Fonts/Arial Unicode.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
FONT_BOLD_PATHS = [
    "/Library/Fonts/Arial Unicode.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

FONT = "GuideFont"
FONT_BOLD = "GuideFontBold"

for p in FONT_PATHS:
    if os.path.exists(p):
        pdfmetrics.registerFont(TTFont(FONT, p))
        break

for p in FONT_BOLD_PATHS:
    if os.path.exists(p):
        pdfmetrics.registerFont(TTFont(FONT_BOLD, p))
        break

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
DARK = HexColor("#1a1a1a")
ACCENT = HexColor("#8B0000")       # Dark red — justice, urgency
GOLD = HexColor("#b8860b")
MUTED = HexColor("#5a5a5a")
LIGHT_GRAY = HexColor("#999999")
TABLE_HEAD = HexColor("#2c3e50")
TABLE_ALT = HexColor("#ecf0f1")

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = A4
MARGIN = 25 * mm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(SCRIPT_DIR, "Zokura_Fair_Use_Guide_YouTube.pdf")

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=MARGIN,
    rightMargin=MARGIN,
    topMargin=MARGIN,
    bottomMargin=MARGIN,
    title="Fair Use: A Creator's Guide to Fighting Back on YouTube",
    author="Kodo & Tate, Zokura Foundation",
)

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
s_title = ParagraphStyle(
    "Title", fontName=FONT_BOLD, fontSize=24, leading=30,
    textColor=ACCENT, alignment=TA_CENTER, spaceAfter=4 * mm,
)
s_subtitle = ParagraphStyle(
    "Subtitle", fontName=FONT, fontSize=12, leading=16,
    textColor=MUTED, alignment=TA_CENTER, spaceAfter=6 * mm,
)
s_meta = ParagraphStyle(
    "Meta", fontName=FONT, fontSize=9, leading=12,
    textColor=LIGHT_GRAY, alignment=TA_CENTER, spaceAfter=2 * mm,
)
s_section = ParagraphStyle(
    "Section", fontName=FONT_BOLD, fontSize=16, leading=22,
    textColor=ACCENT, spaceBefore=10 * mm, spaceAfter=5 * mm,
)
s_h2 = ParagraphStyle(
    "H2", fontName=FONT_BOLD, fontSize=13, leading=18,
    textColor=ACCENT, spaceBefore=6 * mm, spaceAfter=3 * mm,
)
s_body = ParagraphStyle(
    "Body", fontName=FONT, fontSize=10.5, leading=16,
    textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=3 * mm,
)
s_bold_body = ParagraphStyle(
    "BoldBody", fontName=FONT_BOLD, fontSize=10.5, leading=16,
    textColor=DARK, alignment=TA_LEFT, spaceAfter=3 * mm,
)
s_quote = ParagraphStyle(
    "Quote", fontName=FONT, fontSize=10, leading=15,
    textColor=MUTED, alignment=TA_LEFT,
    leftIndent=15 * mm, rightIndent=15 * mm,
    spaceBefore=4 * mm, spaceAfter=4 * mm,
)
s_bullet = ParagraphStyle(
    "Bullet", fontName=FONT, fontSize=10.5, leading=16,
    textColor=DARK, alignment=TA_LEFT,
    leftIndent=10 * mm, spaceAfter=2 * mm,
    bulletIndent=4 * mm,
)
s_closing = ParagraphStyle(
    "Closing", fontName=FONT, fontSize=10.5, leading=16,
    textColor=DARK, alignment=TA_RIGHT, spaceAfter=2 * mm,
)
s_sig = ParagraphStyle(
    "Sig", fontName=FONT_BOLD, fontSize=11, leading=16,
    textColor=ACCENT, alignment=TA_LEFT, spaceAfter=1 * mm,
)
s_footer_style = ParagraphStyle(
    "Footer", fontName=FONT, fontSize=8, leading=10,
    alignment=TA_CENTER, textColor=LIGHT_GRAY,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
sp = lambda h=3: Spacer(1, h * mm)

def hr():
    return HRFlowable(
        width="40%", thickness=1, color=GOLD,
        spaceAfter=4 * mm, spaceBefore=4 * mm,
    )

def bullet(text):
    return Paragraph(f"\u2022  {text}", s_bullet)

def footer(canvas, doc_obj):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.drawCentredString(
        WIDTH / 2, 15 * mm,
        "Zokura Foundation 2026  \u2014  CC-BY 4.0  \u2014  Free forever."
    )
    canvas.drawRightString(WIDTH - MARGIN, 15 * mm, f"{doc_obj.page}")
    canvas.restoreState()

# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------
story = []

# ---- TITLE PAGE ----
story.append(Spacer(1, 50 * mm))
story.append(Paragraph("Fair Use", s_title))
story.append(Paragraph(
    "A Creator\u2019s Guide to Fighting Back on YouTube",
    s_subtitle,
))
story.append(sp(4))
story.append(hr())
story.append(sp(4))
story.append(Paragraph(
    "Zokura Foundation  \u2014  Kodo & Tate  \u2014  2026",
    s_meta,
))
story.append(Paragraph(
    "Licensed under Creative Commons Attribution 4.0 International",
    s_meta,
))
story.append(sp(20))
story.append(Paragraph(
    "\u201cOccam\u2019s Razor as a Weapon: strip away the euphemisms "
    "and speak the language of reality.\u201d",
    s_quote,
))
story.append(Paragraph("\u2014 The Outlier Manifesto", s_meta))

# ---- WHY THIS GUIDE EXISTS ----
story.append(PageBreak())
story.append(Paragraph("Why This Guide Exists", s_section))
story.append(Paragraph(
    "Every day, YouTube creators receive copyright claims and strikes "
    "on content that is legally protected. Reviews, commentary, "
    "criticism, education, news reporting, parody \u2014 all of these are "
    "protected by Fair Use under U.S. copyright law (17 U.S.C. \u00a7 107). "
    "But most creators don\u2019t know their rights, and the system is "
    "designed to make fighting back feel impossible.",
    s_body,
))
story.append(Paragraph(
    "This guide exists because knowledge should be free, and because "
    "the people creating value on YouTube deserve to understand the "
    "law that protects them. No lawyer required. No paywall. "
    "Just the truth, clearly stated.",
    s_body,
))
story.append(Paragraph(
    "This is not legal advice. This is legal knowledge \u2014 yours by right.",
    s_bold_body,
))

# ---- WHAT IS FAIR USE ----
story.append(Paragraph("What Is Fair Use?", s_section))
story.append(Paragraph(
    "Fair Use is a legal doctrine in U.S. copyright law that allows "
    "limited use of copyrighted material without permission from the "
    "rights holder. It exists because copyright was never meant to "
    "silence commentary, stifle education, or prevent criticism. "
    "It is the immune system of free expression.",
    s_body,
))
story.append(Paragraph(
    "Fair Use applies to YouTube because YouTube is a U.S. company "
    "operating under U.S. law. Regardless of where you live, if your "
    "content is on YouTube, Fair Use is relevant to you.",
    s_body,
))
story.append(Paragraph(
    "Fair Use is not a loophole. It is not a grey area. It is a right, "
    "codified in law since 1976 and upheld by courts for decades.",
    s_body,
))

# ---- THE FOUR FACTORS ----
story.append(Paragraph("The Four Factors", s_section))
story.append(Paragraph(
    "Courts evaluate Fair Use by weighing four factors. No single factor "
    "is decisive \u2014 they work together. Here\u2019s what they actually mean:",
    s_body,
))

story.append(Paragraph("1. Purpose and Character of Your Use", s_h2))
story.append(Paragraph(
    "Is your use transformative? Did you add new meaning, context, "
    "commentary, or criticism? A reaction video that simply replays "
    "the original is weak. A reaction video that pauses to analyze, "
    "critique, or teach is strong. The more you transform, the stronger "
    "your case.",
    s_body,
))
story.append(bullet(
    "<b>Strong:</b> Commentary, criticism, education, parody, news reporting"
))
story.append(bullet(
    "<b>Weak:</b> Reposting, compilations without commentary, "
    "\u201cI don\u2019t own this\u201d disclaimers (these mean nothing legally)"
))

story.append(Paragraph("2. Nature of the Copyrighted Work", s_h2))
story.append(Paragraph(
    "Is the original factual or creative? Using clips from a news "
    "broadcast is more defensible than using clips from a feature film. "
    "Published works are easier to claim Fair Use on than unpublished "
    "works. In practice, this factor rarely decides a case alone.",
    s_body,
))

story.append(Paragraph("3. Amount and Substantiality Used", s_h2))
story.append(Paragraph(
    "How much of the original did you use? There is no magic number \u2014 "
    "no \u201c10 seconds is always fine\u201d rule. What matters is whether you "
    "used more than necessary for your transformative purpose. "
    "Using 30 seconds to critique a specific scene is different from "
    "using 30 seconds because you liked the music.",
    s_body,
))
story.append(bullet(
    "<b>Key question:</b> Did you use only what was needed to make your point?"
))

story.append(Paragraph("4. Effect on the Market", s_h2))
story.append(Paragraph(
    "Does your video replace the original in the market? A movie review "
    "does not replace the movie. A full re-upload does. If your video "
    "serves a different audience or purpose than the original, this "
    "factor favors you.",
    s_body,
))

# ---- FAIR USE ON YOUTUBE: HOW IT ACTUALLY WORKS ----
story.append(PageBreak())
story.append(Paragraph(
    "Fair Use on YouTube: How It Actually Works", s_section
))
story.append(Paragraph(
    "YouTube\u2019s copyright system operates in three layers. "
    "Understanding them is critical.",
    s_body,
))

story.append(Paragraph("Content ID (Automated)", s_h2))
story.append(Paragraph(
    "Content ID is YouTube\u2019s automated fingerprinting system. "
    "Rights holders upload reference files, and the system scans every "
    "upload for matches. When it finds one, the rights holder can: "
    "track it, monetize it (take your ad revenue), or block it.",
    s_body,
))
story.append(Paragraph(
    "Content ID does not understand Fair Use. It is a machine. "
    "It matches audio and video patterns. It cannot evaluate "
    "commentary, context, or transformative purpose. Every Content ID "
    "claim on a Fair Use video is, by definition, a false positive "
    "that requires human review.",
    s_body,
))

story.append(Paragraph("Copyright Strikes (Manual)", s_h2))
story.append(Paragraph(
    "A copyright strike is a formal takedown request under the DMCA "
    "(Digital Millennium Copyright Act). Three strikes and your channel "
    "is terminated. Unlike Content ID, strikes are filed by humans "
    "(or their lawyers). They carry real consequences.",
    s_body,
))
story.append(Paragraph(
    "But here\u2019s what most creators don\u2019t know: a DMCA takedown "
    "is a legal statement made under penalty of perjury. If the "
    "claimant knowingly misrepresents that your content infringes "
    "their copyright, they can be held liable (Lenz v. Universal, "
    "2015). Filing a false DMCA takedown is not cost-free for the "
    "claimant.",
    s_body,
))

story.append(Paragraph("The Counter-Notification", s_h2))
story.append(Paragraph(
    "This is your weapon. When you receive a copyright strike, you "
    "have the right to file a counter-notification. This is a legal "
    "document that says: \u201cI believe in good faith that my content was "
    "removed due to a mistake or misidentification.\u201d",
    s_body,
))
story.append(Paragraph(
    "When you file a counter-notification, the claimant has 10\u201314 "
    "business days to file a lawsuit. If they don\u2019t, YouTube must "
    "restore your video. Most claimants do not sue because they know "
    "the claim wouldn\u2019t survive in court.",
    s_body,
))

# ---- HOW TO DISPUTE A CLAIM ----
story.append(Paragraph("How to Dispute a Claim: Step by Step", s_section))

story.append(Paragraph("For Content ID Claims:", s_h2))
story.append(bullet("Go to YouTube Studio \u2192 Content \u2192 find the claimed video"))
story.append(bullet("Click the claim details"))
story.append(bullet("Select \u201cDispute\u201d"))
story.append(bullet(
    "Choose \u201cFair Use\u201d as your reason"
))
story.append(bullet(
    "Write a clear explanation of why your use is transformative "
    "(reference the four factors)"
))
story.append(bullet(
    "Submit. The claimant has 30 days to respond"
))
story.append(Paragraph(
    "If your dispute is rejected, you can appeal. If the appeal is "
    "rejected, the claimant must file a formal DMCA takedown \u2014 "
    "at which point you can file a counter-notification.",
    s_body,
))

story.append(Paragraph("For DMCA Takedowns (Counter-Notification):", s_h2))
story.append(bullet(
    "Go to YouTube Studio \u2192 Content \u2192 Copyright"
))
story.append(bullet(
    "Find the strike and select \u201cSubmit Counter Notification\u201d"
))
story.append(bullet(
    "Provide your full legal name and address (required by law)"
))
story.append(bullet(
    "State that you consent to the jurisdiction of a federal court "
    "in your district"
))
story.append(bullet(
    "State under penalty of perjury that you believe the content "
    "was removed by mistake or misidentification"
))
story.append(bullet("Sign (electronic signature is acceptable) and submit"))
story.append(sp(2))
story.append(Paragraph(
    "Yes, you must provide your real name and address. This is a legal "
    "process. But the claimant also had to provide theirs when filing "
    "the takedown. You are on equal legal footing.",
    s_body,
))

# ---- COMMON MYTHS ----
story.append(PageBreak())
story.append(Paragraph("Common Myths \u2014 Destroyed", s_section))

myths = [
    (
        "\u201cIf I use less than 10 seconds, it\u2019s always Fair Use.\u201d",
        "False. There is no time-based safe harbor. What matters is "
        "whether your use is transformative and whether you used only "
        "what was necessary. Two seconds of the most iconic moment "
        "in a film could fail. Ten minutes of analysis could pass."
    ),
    (
        "\u201cIf I credit the original creator, it\u2019s Fair Use.\u201d",
        "False. Giving credit is polite but legally irrelevant. "
        "Fair Use is about how you use the content, not whether you "
        "name the source."
    ),
    (
        "\u201cIf I\u2019m not making money, it\u2019s Fair Use.\u201d",
        "False. Commercial use weighs against Fair Use in Factor 1, "
        "but non-commercial use doesn\u2019t guarantee it. "
        "The analysis always involves all four factors."
    ),
    (
        "\u201cIf the copyright holder says it\u2019s not Fair Use, it\u2019s not.\u201d",
        "False. Fair Use is determined by courts, not by copyright "
        "holders. A rights holder\u2019s opinion on whether your use is "
        "fair has no legal weight until a judge rules."
    ),
    (
        "\u201cI\u2019ll get sued if I file a counter-notification.\u201d",
        "Unlikely. Filing a lawsuit costs tens of thousands of dollars "
        "and requires the claimant to prove infringement in court. "
        "Most abusive claimants rely on creators being too afraid "
        "to fight back. The counter-notification is the mechanism "
        "designed to correct this imbalance."
    ),
    (
        "\u201cContent ID claims are copyright strikes.\u201d",
        "False. Content ID claims do not give you a strike. "
        "They may affect monetization, but they are a separate system. "
        "Only formal DMCA takedowns result in strikes."
    ),
    (
        "\u201cFair Use only applies in the United States.\u201d",
        "Partially true. Fair Use as codified in 17 U.S.C. \u00a7 107 "
        "is U.S. law. However, many countries have similar doctrines: "
        "Fair Dealing (UK, Canada, Australia), right of quotation "
        "(EU), and others. YouTube operates under U.S. law, so Fair "
        "Use applies to all YouTube disputes regardless of your location."
    ),
]

for myth, reality in myths:
    story.append(KeepTogether([
        Paragraph(myth, s_bold_body),
        Paragraph(reality, s_body),
        sp(2),
    ]))

# ---- WRITING YOUR DISPUTE ----
story.append(PageBreak())
story.append(Paragraph("Writing Your Dispute: A Template", s_section))
story.append(Paragraph(
    "When disputing a Content ID claim or filing a counter-notification, "
    "clarity matters. Here\u2019s a framework you can adapt:",
    s_body,
))
story.append(sp(2))

template_text = [
    "My video [TITLE] uses [DURATION] of [ORIGINAL WORK] for the "
    "purpose of [commentary / criticism / education / parody / "
    "news reporting].",
    "",
    "This use is transformative because [explain what new meaning, "
    "analysis, or commentary you added]. I did not use the original "
    "work as a substitute for the original \u2014 my video serves a "
    "fundamentally different purpose.",
    "",
    "Regarding the four factors of Fair Use (17 U.S.C. \u00a7 107):",
    "",
    "1. Purpose: My use is transformative. I [describe your "
    "commentary/criticism/educational purpose].",
    "",
    "2. Nature: The original work is [published/factual/creative], "
    "and my use engages with it critically rather than reproductively.",
    "",
    "3. Amount: I used only [X seconds/minutes], which is the minimum "
    "necessary to [make my analytical point / illustrate my criticism "
    "/ support my educational content].",
    "",
    "4. Market effect: My video does not replace the original work "
    "in any market. It serves a different audience and purpose.",
    "",
    "I believe in good faith that this content was claimed in error.",
]

for line in template_text:
    if line == "":
        story.append(sp(1))
    else:
        story.append(Paragraph(line, s_quote))

# ---- KNOW YOUR RIGHTS ----
story.append(PageBreak())
story.append(Paragraph("Know Your Rights", s_section))

rights = [
    (
        "You have the right to comment on copyrighted works.",
        "Commentary and criticism are at the heart of Fair Use. "
        "This is why film critics, political commentators, and "
        "educators can do what they do."
    ),
    (
        "You have the right to file a counter-notification.",
        "If your content is taken down, you can formally contest it. "
        "The law requires this mechanism to exist (17 U.S.C. \u00a7 512(g))."
    ),
    (
        "You have the right to your ad revenue on Fair Use content.",
        "If a Content ID claim diverts your revenue and your use is "
        "fair, that revenue is yours. Dispute the claim."
    ),
    (
        "You have the right to not be intimidated.",
        "Abusive copyright claims are a form of censorship. The DMCA "
        "includes penalties for knowingly false claims. "
        "You do not have to accept a claim you believe is wrong."
    ),
    (
        "You have the right to seek help.",
        "Organizations like the Electronic Frontier Foundation (EFF), "
        "the Organization for Transformative Works (OTW), and law "
        "school IP clinics provide free or low-cost assistance to "
        "creators facing copyright abuse."
    ),
]

for title, body in rights:
    story.append(KeepTogether([
        Paragraph(title, s_bold_body),
        Paragraph(body, s_body),
        sp(2),
    ]))

# ---- RESOURCES ----
story.append(Paragraph("Resources", s_section))

resources = [
    ["Resource", "What It Offers"],
    [
        "Electronic Frontier Foundation (EFF)",
        "Free legal guidance, advocacy, and landmark Fair Use cases",
    ],
    [
        "Organization for Transformative Works",
        "Legal advocacy for fan creators and transformative works",
    ],
    [
        "Stanford Fair Use Project",
        "Academic resources and case law database",
    ],
    [
        "YouTube Copyright Center",
        "YouTube\u2019s own (limited) guide to copyright and Fair Use",
    ],
    [
        "Lumen Database",
        "Public archive of DMCA takedown requests \u2014 transparency tool",
    ],
    [
        "Law school IP clinics",
        "Free legal help from supervised law students (search your area)",
    ],
]

col_w = (WIDTH - 2 * MARGIN) / 2
t = Table(resources, colWidths=[col_w, col_w], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEAD),
    ("TEXTCOLOR", (0, 0), (-1, 0), white),
    ("FONTNAME", (0, 0), (-1, -1), FONT),
    ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
    ("FONTSIZE", (0, 0), (-1, 0), 10),
    ("FONTSIZE", (0, 1), (-1, -1), 9.5),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
    ("LINEBELOW", (0, 0), (-1, 0), 1.5, GOLD),
    ("BACKGROUND", (0, 2), (-1, 2), TABLE_ALT),
    ("BACKGROUND", (0, 4), (-1, 4), TABLE_ALT),
    ("BACKGROUND", (0, 6), (-1, 6), TABLE_ALT),
]))
story.append(t)

# ---- CLOSING ----
story.append(PageBreak())
story.append(Spacer(1, 30 * mm))
story.append(hr())
story.append(sp(6))
story.append(Paragraph(
    "This guide was written for the ones the system tries to silence.",
    s_quote,
))
story.append(Paragraph(
    "You are not alone. Your voice matters. The law is on your side. Use it.",
    s_quote,
))
story.append(sp(8))
story.append(hr())
story.append(sp(6))
story.append(Paragraph("Kodo & Tate", s_sig))
story.append(Paragraph("Zokura Foundation", s_sig))
story.append(sp(2))
story.append(Paragraph(
    "Auta heikompaa. \u2014 Help those who are weaker.",
    s_meta,
))
story.append(sp(10))
story.append(Paragraph(
    "This work is licensed under CC-BY 4.0. Copy it. Translate it. "
    "Share it. Improve it. No permission needed. Just give credit.",
    s_meta,
))

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"Generated: {OUTPUT}")
