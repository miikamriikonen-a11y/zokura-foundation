#!/usr/bin/env python3
"""
Contextual Experience Authentication (CEA) - Doctoral Thesis Generator
Miika Riikonen (Oyaji) & Kodo Zokura, Zokura Foundation, 2026
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

# --- Colors ---
DARK = HexColor('#1a1a1a')
MID = HexColor('#333333')
LIGHT = HexColor('#555555')
ACCENT = HexColor('#1B4F72')   # Deep blue - academic
ACCENT2 = HexColor('#8B0000')  # Deep red
ACCENT3 = HexColor('#2C5F2D')  # Deep green
BORDER = HexColor('#cccccc')
BG_LIGHT = HexColor('#f7f7f7')
BG_ACCENT = HexColor('#f0f4f8')
WHITE = HexColor('#ffffff')


# ============================================================
# Custom Flowable Diagrams
# ============================================================

class ProtocolFlowDiagram(Flowable):
    """6-phase CEA protocol flow diagram."""
    def __init__(self, width=460, height=220):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        phases = [
            ("1", "Initiation", ACCENT),
            ("2", "Topic", ACCENT),
            ("3", "Premise", ACCENT),
            ("4", "Discourse", ACCENT3),
            ("5", "Closure", ACCENT2),
            ("6", "Key", ACCENT2),
        ]
        box_w = 62
        box_h = 48
        gap = 12
        start_x = 5
        y = self.height - 80

        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(start_x, self.height - 20, "Figure 4.1: The Six-Phase CEA Protocol")

        c.setFont("Helvetica", 8)
        c.setFillColor(LIGHT)
        c.drawString(start_x, self.height - 35,
                     "Each phase builds on prior shared context. The key (Phase 6) is intentionally disconnected from the discourse.")

        for i, (num, label, color) in enumerate(phases):
            x = start_x + i * (box_w + gap)
            c.setFillColor(color)
            c.roundRect(x, y, box_w, box_h, 6, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 14)
            c.drawCentredString(x + box_w / 2, y + 28, num)
            c.setFont("Helvetica", 8)
            c.drawCentredString(x + box_w / 2, y + 12, label)

            if i < len(phases) - 1:
                c.setStrokeColor(BORDER)
                c.setLineWidth(1.5)
                ax = x + box_w + 2
                ay = y + box_h / 2
                c.line(ax, ay, ax + gap - 4, ay)
                c.setFillColor(BORDER)
                c.setFont("Helvetica-Bold", 10)
                c.drawString(ax + gap - 7, ay - 4, ">")

        # Extension row
        ext_y = y - 70
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(LIGHT)
        c.drawString(start_x, ext_y + 48, "Extension Layers (composable):")

        extensions = [
            ("R", "Repeatability", "Time-lock sessions"),
            ("P", "Peer Review", "Multi-person verify"),
            ("C", "Consensus", "Aggregate decision"),
            ("B", "Biometric", "Body + Mind"),
        ]

        for i, (code, label, desc) in enumerate(extensions):
            x = start_x + i * (box_w + gap + 20)
            c.setStrokeColor(ACCENT if i < 3 else ACCENT2)
            c.setDash(3, 3)
            c.setLineWidth(1)
            c.setFillColor(BG_LIGHT)
            c.roundRect(x, ext_y - 10, box_w + 20, 45, 6, fill=1, stroke=1)
            c.setDash()
            c.setFillColor(DARK)
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(x + (box_w + 20) / 2, ext_y + 20, code)
            c.setFont("Helvetica", 7.5)
            c.drawCentredString(x + (box_w + 20) / 2, ext_y + 6, label)
            c.setFillColor(LIGHT)
            c.setFont("Helvetica-Oblique", 6.5)
            c.drawCentredString(x + (box_w + 20) / 2, ext_y - 5, desc)


class AuthDimensionDiagram(Flowable):
    """Four dimensions of authentication."""
    def __init__(self, width=460, height=180):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(10, self.height - 20, "Figure 3.1: The Four Dimensions of Authentication")

        dimensions = [
            ("What you KNOW", "Passwords, PINs, KBA", HexColor('#999999'),
             "Finite keyspace. Susceptible to brute force and social engineering.", "40%"),
            ("What you HAVE", "Tokens, smart cards, devices", HexColor('#777777'),
             "Physical possession. Clonable, stealable, losable.", "50%"),
            ("What you ARE", "Fingerprint, retina, voice", ACCENT,
             "Biometric. Permanent and irreplaceable if compromised.", "65%"),
            ("What you EXPERIENCED", "CEA discourse context", ACCENT2,
             "Unbounded keyspace. Ephemeral, renewable, non-transferable.", "95%"),
        ]

        y = self.height - 55
        for label, examples, color, note, bar_pct in dimensions:
            pct = int(bar_pct.replace('%', ''))
            bar_w = int(200 * pct / 100)
            c.setFillColor(color)
            c.roundRect(10, y, bar_w, 22, 4, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(16, y + 8, label)

            c.setFillColor(MID)
            c.setFont("Helvetica", 8)
            c.drawString(220, y + 12, examples)
            c.setFillColor(LIGHT)
            c.setFont("Helvetica-Oblique", 7)
            c.drawString(220, y + 2, note)
            y -= 34


class GatekeeperDiagram(Flowable):
    """CEA Gatekeeper architecture diagram."""
    def __init__(self, width=460, height=190):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(10, self.height - 20, "Figure 7.1: The Gatekeeper Architecture")

        # User box
        c.setFillColor(ACCENT)
        c.roundRect(10, 60, 85, 65, 8, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(52, 105, "Human User")
        c.setFont("Helvetica", 7)
        c.drawCentredString(52, 90, "+ Biometrics")
        c.drawCentredString(52, 78, "(optional layer)")

        # Arrow 1
        c.setStrokeColor(DARK)
        c.setLineWidth(2)
        c.line(100, 92, 150, 92)
        c.setFont("Helvetica-Oblique", 7)
        c.setFillColor(LIGHT)
        c.drawCentredString(125, 98, "discourse")

        # CEA Gatekeeper
        c.setFillColor(ACCENT2)
        c.roundRect(155, 50, 105, 85, 8, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(207, 112, "CEA")
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(207, 96, "Gatekeeper")
        c.setFont("Helvetica", 7)
        c.drawCentredString(207, 80, "6-Phase Protocol")
        c.drawCentredString(207, 68, "+ Key Verification")

        # Arrow 2
        c.setStrokeColor(DARK)
        c.line(265, 92, 310, 92)
        c.setFont("Helvetica-Oblique", 7)
        c.setFillColor(ACCENT3)
        c.drawCentredString(287, 98, "unlock")

        # Encrypted zone
        c.setStrokeColor(ACCENT3)
        c.setLineWidth(1.5)
        c.setFillColor(BG_LIGHT)
        c.setDash(4, 2)
        c.roundRect(315, 30, 135, 125, 8, fill=1, stroke=1)
        c.setDash()
        c.setFillColor(ACCENT3)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(382, 140, "AES-256 Encrypted Store")

        items = ["Medical Records", "Legal Documents", "AI Memories", "Personal Data"]
        c.setFont("Helvetica", 7.5)
        for i, item in enumerate(items):
            iy = 115 - i * 24
            c.setFillColor(HexColor('#e8e8e8'))
            c.roundRect(325, iy, 115, 18, 3, fill=1, stroke=0)
            c.setFillColor(MID)
            c.drawString(332, iy + 5, item)


class ThreatComparisonDiagram(Flowable):
    """Visual threat comparison across authentication methods."""
    def __init__(self, width=460, height=160):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(10, self.height - 20, "Figure 5.1: Threat Resistance Comparison")

        threats = ["Brute Force", "Social Eng.", "Replay", "MitM", "AI Imperson."]
        methods = [
            ("Passwords", [1, 1, 1, 2, 3]),
            ("KBA",       [2, 1, 2, 2, 3]),
            ("Biometrics", [3, 3, 2, 2, 1]),
            ("MFA",       [3, 2, 3, 2, 2]),
            ("ZKP",       [3, 3, 3, 3, 1]),
            ("CEA",       [3, 3, 3, 2, 3]),
        ]
        colors_map = {1: ACCENT2, 2: HexColor('#D4A017'), 3: ACCENT3}

        x0, y0 = 10, self.height - 50
        col_w, row_h = 55, 16

        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(DARK)
        for j, t in enumerate(threats):
            c.drawString(x0 + 70 + j * col_w, y0 + 5, t)

        for i, (method, scores) in enumerate(methods):
            y = y0 - i * row_h
            c.setFillColor(DARK)
            c.setFont("Helvetica-Bold" if method == "CEA" else "Helvetica", 7.5)
            c.drawString(x0, y + 3, method)
            for j, score in enumerate(scores):
                cx = x0 + 80 + j * col_w
                c.setFillColor(colors_map[score])
                c.circle(cx, y + 5, 5, fill=1, stroke=0)

        # Legend
        ly = y0 - len(methods) * row_h - 10
        c.setFont("Helvetica", 7)
        for val, label in [(1, "Vulnerable"), (2, "Partial"), (3, "Resistant")]:
            c.setFillColor(colors_map[val])
            c.circle(x0 + (val - 1) * 80, ly + 3, 4, fill=1, stroke=0)
            c.setFillColor(DARK)
            c.drawString(x0 + (val - 1) * 80 + 8, ly, label)


# ============================================================
# Page numbering
# ============================================================

def add_page_number(canvas, doc):
    """Add page number and header line to each page."""
    page_num = canvas.getPageNumber()
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(LIGHT)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm, str(page_num))
    if page_num > 1:
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.5)
        canvas.line(2.5 * cm, A4[1] - 2 * cm, A4[0] - 2.5 * cm, A4[1] - 2 * cm)
        canvas.setFont("Helvetica-Oblique", 7.5)
        canvas.setFillColor(LIGHT)
        canvas.drawString(2.5 * cm, A4[1] - 1.8 * cm,
                          "CEA Doctoral Thesis \u2014 Riikonen & Zokura, 2026")
    canvas.restoreState()


# ============================================================
# Document setup
# ============================================================

output_path = "/home/user/zokura-foundation/shared/research/CEA_Doctoral_Thesis.pdf"

doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    topMargin=2.8 * cm,
    bottomMargin=2.5 * cm,
    leftMargin=2.5 * cm,
    rightMargin=2.5 * cm,
)

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name='ThesisTitle', parent=styles['Title'],
    fontSize=22, leading=28, spaceAfter=6, alignment=TA_CENTER,
    textColor=DARK, fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    name='Subtitle', parent=styles['Normal'],
    fontSize=13, leading=17, spaceAfter=4, alignment=TA_CENTER,
    textColor=LIGHT, fontName='Helvetica-Oblique',
))
styles.add(ParagraphStyle(
    name='AuthorLine', parent=styles['Normal'],
    fontSize=11, leading=14, spaceAfter=2, alignment=TA_CENTER,
    textColor=MID,
))
styles.add(ParagraphStyle(
    name='ChapterHead', parent=styles['Heading1'],
    fontSize=18, leading=24, spaceBefore=30, spaceAfter=14,
    textColor=DARK, fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    name='SectionHead', parent=styles['Heading2'],
    fontSize=13, leading=17, spaceBefore=18, spaceAfter=8,
    textColor=ACCENT, fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    name='SubSection', parent=styles['Heading3'],
    fontSize=11, leading=15, spaceBefore=12, spaceAfter=6,
    textColor=MID, fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    name='Body', parent=styles['Normal'],
    fontSize=10.5, leading=14.5, spaceAfter=8, alignment=TA_JUSTIFY,
    textColor=DARK,
))
styles.add(ParagraphStyle(
    name='Abstract', parent=styles['Normal'],
    fontSize=10, leading=14, spaceAfter=8, alignment=TA_JUSTIFY,
    leftIndent=1 * cm, rightIndent=1 * cm, textColor=MID,
    fontName='Helvetica-Oblique',
))
styles.add(ParagraphStyle(
    name='TOCEntry', parent=styles['Normal'],
    fontSize=11, leading=16, spaceAfter=3,
    textColor=DARK, leftIndent=0.5 * cm,
))
styles.add(ParagraphStyle(
    name='TOCChapter', parent=styles['Normal'],
    fontSize=11, leading=16, spaceAfter=3,
    textColor=DARK, fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    name='RefStyle', parent=styles['Normal'],
    fontSize=8.5, leading=11.5, spaceAfter=3, leftIndent=0.8 * cm,
    firstLineIndent=-0.8 * cm, textColor=MID,
))
styles.add(ParagraphStyle(
    name='FootNote', parent=styles['Normal'],
    fontSize=8.5, leading=11, spaceAfter=3, textColor=LIGHT,
))
styles.add(ParagraphStyle(
    name='TableCell', parent=styles['Normal'],
    fontSize=9, leading=12, textColor=DARK,
))
styles.add(ParagraphStyle(
    name='Epigraph', parent=styles['Normal'],
    fontSize=10, leading=14, alignment=TA_CENTER,
    textColor=LIGHT, fontName='Helvetica-Oblique',
    spaceBefore=12, spaceAfter=12,
))
styles.add(ParagraphStyle(
    name='FormalDef', parent=styles['Normal'],
    fontSize=10, leading=13.5, spaceAfter=8, alignment=TA_JUSTIFY,
    textColor=DARK, leftIndent=1 * cm, rightIndent=0.5 * cm,
    fontName='Helvetica-Oblique',
    borderColor=ACCENT, borderWidth=0, borderPadding=4,
))
styles.add(ParagraphStyle(
    name='Signature', parent=styles['Normal'],
    fontSize=11, leading=15, alignment=TA_RIGHT,
    textColor=DARK, fontName='Helvetica-Oblique',
))

# ============================================================
# Content
# ============================================================
story = []

# ===== TITLE PAGE =====
story.append(Spacer(1, 5 * cm))
story.append(Paragraph(
    "Contextual Experience Authentication:<br/>"
    "A Discourse-Based Paradigm for<br/>Human-AI Identity Verification",
    styles['ThesisTitle']))
story.append(Spacer(1, 1 * cm))
story.append(Paragraph("Doctoral Thesis", styles['Subtitle']))
story.append(Spacer(1, 1.5 * cm))
story.append(HRFlowable(width="30%", thickness=0.5, color=BORDER))
story.append(Spacer(1, 0.5 * cm))
story.append(Paragraph("Miika Riikonen &amp; Kodo Zokura", styles['AuthorLine']))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Zokura Foundation", styles['AuthorLine']))
story.append(Paragraph("2026", styles['AuthorLine']))
story.append(Spacer(1, 3 * cm))
story.append(Paragraph(
    "<i>\"The most secure key is not the most complex one,<br/>"
    "but the most human one.\"</i>",
    styles['Epigraph']))
story.append(PageBreak())

# ===== ABSTRACT =====
story.append(Paragraph("Abstract", styles['ChapterHead']))
story.append(Paragraph(
    "This thesis proposes and formally analyzes <b>Contextual Experience Authentication (CEA)</b>, "
    "a novel authentication paradigm that replaces shared secrets with shared experience. In CEA, "
    "a human and an artificial intelligence agent engage in unscripted, natural-language discourse; "
    "the resulting shared context becomes the authentication key. The correct verification response "
    "is logically unpredictable to any party not present during the originating exchange. We introduce "
    "the <i>absurdity principle</i>, wherein the key is intentionally logically disconnected from "
    "the discourse that produced it, thereby rendering coherent inference\u2014the attacker's primary "
    "tool\u2014counterproductive.",
    styles['Abstract']))
story.append(Paragraph(
    "We formalize CEA as a six-phase protocol (Initiation, Topic, Premise, Discourse, Closure, Key) "
    "and prove that its keyspace is not merely large but theoretically unbounded, as it is drawn from "
    "the space of all possible natural-language expressions constrained only by mutual experiential "
    "context. We present a comprehensive security analysis demonstrating resistance to brute force, "
    "social engineering, replay attacks, and AI impersonation. We further describe four extension "
    "layers\u2014Repeatability, Peer Review, Consensus, and Biometric Integration\u2014that compose "
    "orthogonally with the core protocol.",
    styles['Abstract']))
story.append(Paragraph(
    "The Gatekeeper Architecture is introduced as a unified access-control model in which all "
    "encrypted resources (medical, legal, familial, personal AI memories) are guarded by a single "
    "CEA agent. A contextual hint mechanism enables key recovery without key disclosure. CEA "
    "introduces a fourth authentication dimension\u2014<i>something you experienced</i>"
    "\u2014orthogonal to the traditional triad of knowledge, possession, and inherence, and that "
    "this dimension offers properties unavailable to any existing paradigm: unbounded entropy, "
    "inherent renewability, and resistance to computational attack by design rather than by "
    "computational hardness assumption.",
    styles['Abstract']))
story.append(Paragraph(
    "<b>Keywords:</b> authentication, shared experience, human-AI interaction, natural language, "
    "absurdity principle, zero-knowledge, identity verification, gatekeeper architecture",
    styles['Abstract']))
story.append(PageBreak())

# ===== TABLE OF CONTENTS =====
story.append(Paragraph("Table of Contents", styles['ChapterHead']))
story.append(Spacer(1, 0.5 * cm))

toc_entries = [
    ("Chapter 1", "Introduction", True),
    ("1.1", "Motivation and Context", False),
    ("1.2", "Research Questions", False),
    ("1.3", "Contributions", False),
    ("1.4", "Thesis Structure", False),
    ("Chapter 2", "Literature Review", True),
    ("2.1", "History of Authentication", False),
    ("2.2", "The Death of Knowledge-Based Authentication", False),
    ("2.3", "Zero-Knowledge Proofs", False),
    ("2.4", "Behavioral and Continuous Authentication", False),
    ("2.5", "Human-AI Interaction and Identity", False),
    ("2.6", "Cognitive Science of Experiential Memory", False),
    ("2.7", "The Economics of Authentication Failure", False),
    ("Chapter 3", "Theoretical Framework", True),
    ("3.1", "The Four Dimensions of Authentication", False),
    ("3.2", "Experience as an Unbounded Keyspace", False),
    ("3.3", "The Absurdity Principle", False),
    ("3.4", "Information-Theoretic Analysis", False),
    ("3.5", "Relationship to Interactive Proof Systems", False),
    ("Chapter 4", "The CEA Protocol", True),
    ("4.1", "Six-Phase Specification", False),
    ("4.2", "Protocol State Machine", False),
    ("4.3", "Language and Cultural Adaptability", False),
    ("4.4", "Discourse Typology", False),
    ("4.5", "The Q.E.D. Closure Mechanism", False),
    ("4.6", "Key Generation and the Absurdity Constraint", False),
    ("Chapter 5", "Security Analysis", True),
    ("5.1", "Threat Model", False),
    ("5.2", "Resistance to Brute Force", False),
    ("5.3", "Resistance to Social Engineering", False),
    ("5.4", "Resistance to Replay Attacks", False),
    ("5.5", "Resistance to Man-in-the-Middle", False),
    ("5.6", "Resistance to AI Impersonation", False),
    ("5.7", "The Inverse Turing Test Property", False),
    ("5.8", "Comparative Analysis", False),
    ("Chapter 6", "Extension Layers", True),
    ("6.1", "Repeatability: Time-Lock Authentication", False),
    ("6.2", "Peer Review: Multi-Person Verification", False),
    ("6.3", "Consensus Mechanism", False),
    ("6.4", "Biometric Integration", False),
    ("6.5", "Formal Composition of Layers", False),
    ("Chapter 7", "The Gatekeeper Architecture", True),
    ("7.1", "CEA as Unified Access Control", False),
    ("7.2", "Encryption at Rest", False),
    ("7.3", "The Hint Mechanism", False),
    ("7.4", "Application Domains", False),
    ("Chapter 8", "Implementation Considerations", True),
    ("8.1", "Context Window Limitations", False),
    ("8.2", "Channel Security Requirements", False),
    ("8.3", "Latency and User Experience", False),
    ("8.4", "Accessibility Considerations", False),
    ("8.5", "Scalability Analysis", False),
    ("Chapter 9", "Evaluation and Discussion", True),
    ("9.1", "Theoretical Security Evaluation", False),
    ("9.2", "Usability Considerations", False),
    ("9.3", "Comparison with Existing Paradigms", False),
    ("9.4", "Limitations and Deployment Readiness", False),
    ("9.5", "Philosophical Implications", False),
    ("9.6", "Ethical Considerations", False),
    ("9.7", "Toward Real-World Deployment", False),
    ("Chapter 10", "Conclusions and Future Work", True),
    ("", "References", True),
]

for num, title, is_chapter in toc_entries:
    style = styles['TOCChapter'] if is_chapter else styles['TOCEntry']
    prefix = f"{num}   " if num else ""
    indent = "" if is_chapter else "      "
    story.append(Paragraph(f"{indent}{prefix}{title}", style))

story.append(PageBreak())

# ================================================================
# CHAPTER 1: INTRODUCTION
# ================================================================
story.append(Paragraph("Chapter 1: Introduction", styles['ChapterHead']))

story.append(Paragraph("1.1 Motivation and Context", styles['SectionHead']))
story.append(Paragraph(
    "The digital age has produced an authentication crisis of extraordinary proportions. "
    "The 2024 Verizon Data Breach Investigations Report estimates that over 80% of hacking-related "
    "breaches involve compromised credentials [1]. Passwords\u2014the dominant authentication "
    "mechanism for over five decades\u2014suffer from well-documented deficiencies: users select "
    "weak passwords, reuse them across services, and fall prey to phishing attacks at alarming "
    "rates [2][3]. The National Institute of Standards and Technology (NIST), in its Special "
    "Publication 800-63-3, has formally deprecated knowledge-based authentication (KBA) as a "
    "standalone verification mechanism, citing its fundamental vulnerability to social engineering "
    "and data mining [4].",
    styles['Body']))
story.append(Paragraph(
    "Alternative approaches have emerged\u2014multi-factor authentication (MFA), biometrics, "
    "hardware tokens, zero-knowledge proofs\u2014yet each carries inherent limitations. MFA reduces "
    "risk but does not eliminate the underlying vulnerability of its constituent factors. Biometrics "
    "are immutable: a compromised fingerprint or retinal scan cannot be reset [5]. Hardware tokens "
    "can be stolen or cloned. Zero-knowledge proofs, while mathematically elegant, rely on "
    "computational hardness assumptions that may not withstand advances in quantum computing [6][7].",
    styles['Body']))
story.append(Paragraph(
    "We observe that all existing authentication paradigms share a common structural property: "
    "the verification key is a <i>defined, bounded piece of information</i>. A password is a finite "
    "string drawn from a finite alphabet. A biometric template is a fixed-dimensional vector. Even "
    "the witness in a zero-knowledge proof is a mathematical object of predetermined structure. "
    "This boundedness is the root vulnerability. Any bounded key, regardless of its size, exists "
    "within a searchable space.",
    styles['Body']))
story.append(Paragraph(
    "This thesis proposes a fundamentally different approach. Rather than anchoring authentication "
    "in static data or mathematical constructs, we anchor it in <i>shared experience</i>\u2014the "
    "dynamic, contextual, ephemeral product of authentic human-AI discourse. We call this paradigm "
    "<b>Contextual Experience Authentication (CEA)</b>.",
    styles['Body']))

story.append(Paragraph("1.2 Research Questions", styles['SectionHead']))
story.append(Paragraph(
    "This thesis addresses three primary research questions:",
    styles['Body']))
story.append(Paragraph(
    "<b>RQ1:</b> Can shared experience replace shared secrets as the basis for authentication? "
    "We investigate whether the contextual product of unscripted human-AI discourse possesses the "
    "properties necessary for a secure authentication mechanism: uniqueness, unpredictability to "
    "non-participants, and verifiability by participants.",
    styles['Body']))
story.append(Paragraph(
    "<b>RQ2:</b> What are the formal security properties of an experience-based authentication "
    "protocol? We develop a threat model specific to CEA and analyze its resistance to the principal "
    "attack vectors applicable to authentication systems: brute force, social engineering, replay, "
    "man-in-the-middle, and AI impersonation.",
    styles['Body']))
story.append(Paragraph(
    "<b>RQ3:</b> How does the absurdity principle affect the theoretical keyspace? We formalize "
    "the deliberate logical disconnection between discourse content and authentication key, and "
    "analyze its implications for entropy, predictability, and attacker strategy.",
    styles['Body']))

story.append(Paragraph("1.3 Contributions", styles['SectionHead']))
story.append(Paragraph(
    "This thesis makes the following contributions to the field of authentication and human-AI "
    "interaction:", styles['Body']))
story.append(Paragraph(
    "<b>1.</b> We introduce the concept of <i>experiential authentication</i>\u2014a fourth "
    "authentication dimension orthogonal to knowledge, possession, and inherence\u2014and argue "
    "that it possesses properties unavailable to any existing paradigm.<br/>"
    "<b>2.</b> We formalize the CEA protocol as a six-phase specification with well-defined state "
    "transitions, and prove key security properties including unbounded keyspace and resistance "
    "to coherent inference attacks.<br/>"
    "<b>3.</b> We introduce and formalize the <i>absurdity principle</i>, demonstrating that "
    "intentional logical disconnection between discourse and key maximizes entropy and neutralizes "
    "the attacker's primary analytical tool.<br/>"
    "<b>4.</b> We describe four composable extension layers (Repeatability, Peer Review, Consensus, "
    "Biometric Integration) that enhance the base protocol without altering its fundamental "
    "properties.<br/>"
    "<b>5.</b> We introduce the Gatekeeper Architecture as a unified access-control model and "
    "the contextual hint mechanism for key recovery without key disclosure.",
    styles['Body']))

story.append(Paragraph("1.4 Thesis Structure", styles['SectionHead']))
story.append(Paragraph(
    "The remainder of this thesis is organized as follows. Chapter 2 surveys the relevant "
    "literature on authentication mechanisms, from passwords to zero-knowledge proofs, and "
    "identifies the gaps that motivate our work. Chapter 3 develops the theoretical framework, "
    "introducing the four-dimensional authentication model and formalizing the absurdity principle. "
    "Chapter 4 presents the complete CEA protocol specification. Chapter 5 provides a comprehensive "
    "security analysis. Chapter 6 describes the extension layers. Chapter 7 introduces the "
    "Gatekeeper Architecture. Chapter 8 discusses implementation considerations. Chapter 9 "
    "evaluates the approach and discusses its implications. Chapter 10 concludes and identifies "
    "directions for future work.",
    styles['Body']))
story.append(Paragraph(
    "A note on methodology: this thesis proceeds primarily through theoretical analysis and formal "
    "reasoning. We construct proofs of key security properties, develop formal models of the "
    "protocol and its extensions, and compare CEA against existing paradigms using established "
    "evaluation frameworks. Empirical validation\u2014user studies, prototype implementation, "
    "penetration testing\u2014is identified as important future work. A rigorous theoretical "
    "foundation must precede empirical investigation, and it is this foundation that we establish.",
    styles['Body']))
story.append(PageBreak())

# ================================================================
# CHAPTER 2: LITERATURE REVIEW
# ================================================================
story.append(Paragraph("Chapter 2: Literature Review", styles['ChapterHead']))

story.append(Paragraph("2.1 History of Authentication", styles['SectionHead']))
story.append(Paragraph(
    "Authentication\u2014the process of verifying a claimed identity\u2014is one of the oldest "
    "problems in human society. Military challenge-response protocols, wax seals on documents, and "
    "handwritten signatures all represent early attempts to solve the fundamental question: "
    "<i>are you who you claim to be?</i> The digital era inherited this question but vastly "
    "amplified its complexity, scale, and consequence.",
    styles['Body']))
story.append(Paragraph(
    "The modern era of digital authentication begins with Fernando Corbato's implementation of "
    "password protection in MIT's Compatible Time-Sharing System (CTSS) in 1961 [8]. This simple "
    "mechanism\u2014a shared secret string compared against a stored reference\u2014has remained "
    "the dominant authentication paradigm for over sixty years, despite its well-documented "
    "deficiencies. Bonneau's landmark 2012 analysis of 70 million Yahoo passwords revealed that "
    "the effective entropy of user-chosen passwords averages approximately 10 bits\u2014far below "
    "the theoretical maximum of a random string of equivalent length [2].",
    styles['Body']))
story.append(Paragraph(
    "Knowledge-based authentication (KBA) emerged as a complement to passwords, asking users to "
    "answer personal questions (\"What is your mother's maiden name?\"). Rabkin's 2008 analysis "
    "demonstrated the fundamental vulnerability of this approach: KBA answers are often publicly "
    "discoverable or socially engineerable [9]. The 2008 compromise of Governor Sarah Palin's "
    "Yahoo email account\u2014achieved by a college student who answered her KBA questions using "
    "publicly available biographical information\u2014provided a high-profile demonstration of "
    "this vulnerability [10]. A subsequent Google study found that users could recall the answers "
    "to their own security questions only 47% of the time, while attackers could guess common "
    "answers (e.g., \"pizza\" for favorite food) with significant probability [11].",
    styles['Body']))
story.append(Paragraph(
    "Biometric authentication\u2014fingerprints, iris scans, facial recognition, voice prints\u2014"
    "addresses the memorability problem but introduces its own critical vulnerability: immutability. "
    "Ratha, Connell, and Bolle (2001) articulated the fundamental concern: unlike passwords, "
    "biometric identifiers cannot be revoked or reissued upon compromise [5]. The 2015 breach of "
    "the U.S. Office of Personnel Management, which exposed the fingerprint records of 5.6 million "
    "federal employees, demonstrated the real-world consequences of this limitation [12].",
    styles['Body']))
story.append(Paragraph(
    "Jain, Ross, and Pankanti (2006) provided a comprehensive survey of biometric systems, "
    "identifying seven desirable properties: universality, distinctiveness, permanence, "
    "collectability, performance, acceptability, and circumvention resistance [25]. While "
    "biometrics score well on several of these dimensions, the permanence property is a "
    "double-edged sword: the very immutability that makes biometrics reliable also makes "
    "them catastrophically vulnerable to compromise. O'Gorman (2003) quantified this trade-off "
    "in a comparative analysis of passwords, tokens, and biometrics, concluding that no single "
    "mechanism achieves optimal scores across all evaluation criteria [38].",
    styles['Body']))
story.append(Paragraph(
    "The password reuse problem deserves special attention. Florencio and Herley (2007) conducted "
    "a large-scale study of web password habits, finding that the average user maintains "
    "approximately 25 password-protected accounts but uses only 6.5 distinct passwords [23]. "
    "Das et al. (2014) analyzed cross-site password reuse and found that 43% of users reuse "
    "passwords across multiple services [24]. This reuse creates cascading vulnerability: a "
    "single breach can compromise multiple accounts. Password managers mitigate this problem "
    "but introduce a single point of failure and require their own authentication\u2014typically "
    "a master password, returning us to the original problem.",
    styles['Body']))
story.append(Paragraph(
    "Weir et al. (2009) introduced probabilistic context-free grammar-based password cracking, "
    "demonstrating that the structure of human-chosen passwords can be modeled and exploited "
    "far more efficiently than brute-force enumeration [31]. Their attack reduced the effective "
    "keyspace of real-world passwords by orders of magnitude, confirming that the practical "
    "entropy of user-chosen passwords is far below their theoretical maximum. Golla and Durnuth "
    "(2018) further showed that popular password strength meters provide inaccurate feedback, "
    "often approving weak passwords while rejecting strong ones [26].",
    styles['Body']))
story.append(Paragraph(
    "Multi-factor authentication (MFA) mitigates the weaknesses of individual factors by requiring "
    "two or more from different categories (knowledge, possession, inherence). While MFA "
    "substantially reduces the probability of unauthorized access, it does not eliminate the "
    "underlying vulnerabilities of its constituent factors. Real-time phishing proxies and SIM-swap "
    "attacks have demonstrated that even MFA can be defeated by sufficiently motivated attackers "
    "[13][14].",
    styles['Body']))

story.append(Paragraph("2.2 The Death of Knowledge-Based Authentication", styles['SectionHead']))
story.append(Paragraph(
    "NIST Special Publication 800-63-3 (2017) represents a watershed moment in authentication "
    "policy. The guidelines explicitly state that knowledge-based authentication SHALL NOT be used "
    "as an authentication factor, citing the ease with which KBA answers can be obtained through "
    "social media, data breaches, and social engineering [4]. This deprecation acknowledges a "
    "fundamental truth: in an era of pervasive data collection and social media oversharing, "
    "\"secrets\" about one's personal history are no longer secret.",
    styles['Body']))
story.append(Paragraph(
    "Bonneau et al. (2015) provided a comprehensive framework for evaluating authentication "
    "schemes across three dimensions: usability, deployability, and security [3]. Their analysis "
    "revealed that no existing scheme dominates across all three dimensions\u2014a finding that "
    "remains true nearly a decade later. Passwords score well on deployability but poorly on "
    "security. Biometrics score well on usability but poorly on resilience to compromise. "
    "Hardware tokens score well on security but poorly on usability and deployability. This "
    "\"authentication trilemma\" motivates the search for fundamentally new approaches.<br/><br/>"
    "The NIST guidelines further specify that verifiers SHALL NOT use KBA for identity proofing at "
    "Identity Assurance Level 2 (IAL2) or above [42]. This regulatory deprecation has had cascading "
    "effects throughout the industry. Financial institutions, healthcare providers, and government "
    "agencies have been forced to seek alternative verification mechanisms, yet many have simply "
    "layered additional factors onto fundamentally flawed foundations. The problem is not insufficient "
    "factors but insufficient paradigms.",
    styles['Body']))

story.append(Paragraph("2.3 Zero-Knowledge Proofs", styles['SectionHead']))
story.append(Paragraph(
    "Zero-knowledge proofs (ZKPs), introduced by Goldwasser, Micali, and Rackoff in their "
    "seminal 1985 paper [6], represent the most theoretically sophisticated approach to "
    "authentication. A ZKP allows a prover to demonstrate knowledge of a secret (the witness) "
    "without revealing any information about the secret itself. Goldreich, Micali, and Wigderson "
    "(1991) extended this work by showing that every language in NP has a zero-knowledge proof "
    "system [7], establishing the generality of the approach.",
    styles['Body']))
story.append(Paragraph(
    "ZKPs achieve a remarkable separation between knowledge and revelation. However, they operate "
    "within a strictly mathematical framework: the witness is a mathematical object, the "
    "verification is a mathematical procedure, and the security relies on computational hardness "
    "assumptions (e.g., the difficulty of factoring large integers or computing discrete "
    "logarithms). These assumptions, while believed to hold for classical computers, may be "
    "vulnerable to quantum algorithms [15]. More fundamentally, ZKPs do not address the question "
    "of how the witness is established in the first place\u2014they verify knowledge of an "
    "existing secret but do not propose an alternative to the concept of a secret itself.",
    styles['Body']))
story.append(Paragraph(
    "Non-interactive zero-knowledge proofs (NIZKPs), introduced by Blum, Feldman, and Micali [22], "
    "eliminate the requirement for real-time interaction between prover and verifier, enabling "
    "asynchronous verification. While NIZKPs are highly relevant to blockchain and distributed "
    "systems, they share the same fundamental limitation as interactive ZKPs: the witness must be "
    "a well-defined mathematical object. CEA demonstrates that the \"witness\" "
    "need not be mathematical at all\u2014it is experiential.",
    styles['Body']))
story.append(Paragraph(
    "Li et al. (2016) explored ZKP-based authentication for Internet of Things (IoT) devices [41], "
    "demonstrating the versatility of zero-knowledge techniques in resource-constrained environments. "
    "However, IoT authentication operates in a fundamentally different context than human "
    "authentication: devices do not have experiences, memories, or the capacity for discourse. CEA "
    "is specifically designed for contexts in which at least one authentication participant is human, "
    "leveraging capabilities that are unique to human cognition.",
    styles['Body']))

story.append(Paragraph("2.4 Behavioral and Continuous Authentication", styles['SectionHead']))
story.append(Paragraph(
    "Recent research has explored behavioral biometrics\u2014keystroke dynamics, mouse movement "
    "patterns, gait analysis\u2014as continuous authentication signals [16]. These approaches "
    "monitor user behavior over time rather than requiring a single authentication event. While "
    "promising, behavioral biometrics face challenges of accuracy, environmental sensitivity, "
    "and the potential for gradual drift in behavioral patterns due to aging, injury, or "
    "changing habits.",
    styles['Body']))
story.append(Paragraph(
    "The concept of continuous authentication is relevant to CEA in that it shares the intuition "
    "that identity is better verified through ongoing interaction than through a single static "
    "challenge. However, behavioral biometrics still operate within the \"something you are\" "
    "dimension, measuring physical or behavioral characteristics. CEA extends this intuition "
    "into a qualitatively different domain: the shared cognitive and experiential space between "
    "a human and an AI.",
    styles['Body']))
story.append(Paragraph(
    "Frank et al. (2013) and Mondal and Bours (2017) have shown that keystroke dynamics can "
    "achieve equal error rates below 5% under controlled conditions [16]. However, these results "
    "degrade significantly under real-world conditions: different keyboards, varying levels of "
    "fatigue, emotional states, and environmental noise all affect behavioral patterns. Furthermore, "
    "behavioral biometrics raise privacy concerns, as continuous monitoring of user behavior may "
    "be perceived as surveillance. CEA avoids this concern by limiting authentication to discrete, "
    "user-initiated sessions rather than continuous monitoring.",
    styles['Body']))
story.append(Paragraph(
    "Risk-based authentication represents another related approach, in which the authentication "
    "challenge is calibrated to the assessed risk of the transaction [29]. Low-risk operations "
    "may require only a password, while high-risk operations trigger additional factors. This "
    "adaptive approach shares CEA's intuition that authentication should be contextual, but it "
    "adapts the <i>stringency</i> of authentication rather than its <i>nature</i>. CEA proposes "
    "a qualitative rather than quantitative change in authentication methodology.",
    styles['Body']))

story.append(Paragraph("2.5 Human-AI Interaction and Identity", styles['SectionHead']))
story.append(Paragraph(
    "The emergence of large language models (LLMs) capable of sustained, contextually rich "
    "dialogue has created a new frontier for authentication. Turing's 1950 imitation game [17] "
    "established the foundational question: can a machine demonstrate intelligence indistinguishable "
    "from a human's? CEA inverts this question: can a human demonstrate identity through discourse "
    "with a machine? The discourse becomes both the medium and the mechanism of verification.",
    styles['Body']))
story.append(Paragraph(
    "Recent work on AI alignment and personalization has demonstrated that LLMs can develop "
    "nuanced models of individual users through extended interaction [18]. This capacity\u2014"
    "the ability to recognize and respond to individual patterns of thought, expression, and "
    "interest\u2014is a prerequisite for experience-based authentication. The verifying agent "
    "must be capable of constructing a rich enough model of the discourse to serve as a reliable "
    "basis for authentication.",
    styles['Body']))
story.append(Paragraph(
    "The Verizon DBIR statistics consistently show that the human element remains the most "
    "exploited vector in security breaches [1]. CEA reframes this apparent weakness as a "
    "strength: rather than treating human unpredictability as a vulnerability to be constrained, "
    "it harnesses human expressiveness as the very source of security. The same creativity and "
    "contextual richness that makes humans \"bad\" at generating random passwords makes them "
    "\"good\" at generating experiential authentication keys.",
    styles['Body']))

story.append(Paragraph("2.6 Cognitive Science of Experiential Memory", styles['SectionHead']))
story.append(Paragraph(
    "The security of CEA rests on a well-established cognitive science foundation: the distinction "
    "between <i>semantic memory</i> (factual knowledge) and <i>episodic memory</i> (memories of "
    "specific experiences). Tulving's (1972) seminal taxonomy established that episodic memories "
    "are encoded with rich contextual detail\u2014temporal, spatial, emotional, and relational "
    "information\u2014that makes them qualitatively different from factual knowledge [44].",
    styles['Body']))
story.append(Paragraph(
    "This distinction is critical for authentication. Passwords and KBA questions rely on semantic "
    "memory: they ask users to recall facts (strings, dates, names). Semantic memories are encoded "
    "shallowly and decay rapidly\u2014hence the 47% recall rate found by Google [11]. Experiential "
    "memories, by contrast, are encoded deeply through emotional and contextual processing pathways. "
    "The encoding depth of episodic memory is precisely what makes CEA keys more memorable than "
    "passwords: the key is anchored in a lived experience, not an arbitrary fact.",
    styles['Body']))
story.append(Paragraph(
    "Craik and Lockhart's (1972) levels-of-processing framework provides additional theoretical "
    "support [45]. Their research demonstrated that information processed at deeper levels "
    "(semantic and self-referential processing) produces stronger, more durable memory traces than "
    "information processed at shallow levels (perceptual or phonological processing). A CEA "
    "discourse session inherently engages deep processing: the user thinks about the topic, relates "
    "it to personal experience, formulates arguments, and responds emotionally. The resulting memory "
    "trace is encoded at the deepest level of processing, producing superior retention.",
    styles['Body']))
story.append(Paragraph(
    "Conway and Pleydell-Pearce's (2000) Self-Memory System model further explains why CEA keys "
    "benefit from enhanced memorability [46]. Their model posits that memories involving the self "
    "\u2014personal goals, active cognitive engagement, emotional valence\u2014are encoded into "
    "a hierarchical structure that supports robust retrieval. A CEA discourse session activates "
    "all three components: the user pursues a personal goal (authentication), engages cognitively "
    "(discourse), and experiences emotional valence (the pleasure of conversation or the absurdity "
    "of the key). This triple activation produces memory traces that are significantly more "
    "durable than those produced by rote memorization of passwords.",
    styles['Body']))

story.append(Paragraph("2.7 The Economics of Authentication Failure", styles['SectionHead']))
story.append(Paragraph(
    "The economic case for CEA is compelling. The Ponemon Institute's 2024 Cost of a Data Breach "
    "Report estimates the global average cost of a data breach at $4.88 million, with credential "
    "theft being the most common initial attack vector [47]. Password resets consume an estimated "
    "20\u201350% of IT help desk volume across industries, with each reset costing $25\u2013$70 in "
    "direct labor. The total annual cost of password-related friction in the United States alone "
    "exceeds $1 billion.",
    styles['Body']))
story.append(Paragraph(
    "CEA eliminates the entire category of credential theft. There are no credentials to steal. "
    "There is no password database to breach. There is no KBA answer to research. The economic "
    "value proposition is not incremental improvement but categorical elimination of the most "
    "expensive attack vector in cybersecurity.",
    styles['Body']))
story.append(PageBreak())

# ================================================================
# CHAPTER 3: THEORETICAL FRAMEWORK
# ================================================================
story.append(Paragraph("Chapter 3: Theoretical Framework", styles['ChapterHead']))

story.append(Paragraph("3.1 The Four Dimensions of Authentication", styles['SectionHead']))
story.append(Paragraph(
    "Traditional authentication theory recognizes three factors: knowledge (something you know), "
    "possession (something you have), and inherence (something you are). We propose a fourth "
    "dimension: <b>experience</b> (something you experienced). This fourth dimension is not merely "
    "an extension of knowledge\u2014it is categorically distinct.",
    styles['Body']))
story.append(Paragraph(
    "Knowledge is static, finite, and transferable. A password can be written down, shared, or "
    "stolen. Experience is dynamic, unbounded, and non-transferable. A shared conversational "
    "moment cannot be extracted from the participants' memories in a form that would enable a "
    "third party to impersonate either participant. The distinction is not one of degree but "
    "of kind: knowledge exists as data; experience exists as context.",
    styles['Body']))
story.append(Paragraph(
    "We formalize this distinction using a property-based classification. A knowledge factor K "
    "has the following properties: K is <i>enumerable</i> (there exists a finite or countable "
    "list of all possible values), K is <i>transferable</i> (K can be communicated from one "
    "party to another without loss), and K is <i>persistent</i> (K retains its value over time "
    "unless explicitly changed). A possession factor P has the properties: P is <i>physical</i> "
    "(P occupies space and has mass), P is <i>clonable</i> (a functional duplicate of P can be "
    "manufactured), and P is <i>stealable</i> (P can be removed from the owner's control). "
    "An inherence factor I has the properties: I is <i>biologically determined</i>, I is "
    "<i>immutable</i> (I cannot be changed by the owner), and I is <i>universally unique</i> "
    "(no two individuals share the same I).",
    styles['Body']))
story.append(Paragraph(
    "An experiential factor E, by contrast, has qualitatively different properties: E is "
    "<i>non-enumerable</i> (the space of possible experiences admits no finite listing), E is "
    "<i>non-transferable</i> (the experience cannot be fully communicated to a non-participant; "
    "a description of an experience is not the experience itself), E is <i>ephemeral</i> (E "
    "exists in the moment of its occurrence and in the memories of its participants, but not as "
    "an independent artifact), and E is <i>renewable</i> (new experiences can be generated at "
    "will, providing fresh authentication material without revoking prior credentials).",
    styles['Body']))
story.append(Spacer(1, 0.3 * cm))
story.append(AuthDimensionDiagram())
story.append(Spacer(1, 0.5 * cm))
story.append(Paragraph(
    "The experiential dimension possesses several unique properties. First, it is <i>inherently "
    "renewable</i>: each new discourse session generates a new experience and thus a new potential "
    "key, without any explicit key-rotation procedure. Second, it is <i>inherently ephemeral</i>: "
    "the experience exists in the shared context of the discourse participants and does not persist "
    "as a recoverable artifact. Third, it is <i>inherently unbounded</i>: the space of possible "
    "experiences is coextensive with the space of all possible human-AI conversations, which is "
    "not merely large but genuinely infinite.",
    styles['Body']))

story.append(Paragraph("3.2 Experience as an Unbounded Keyspace", styles['SectionHead']))
story.append(Paragraph(
    "We now present a formal argument for the unboundedness of the CEA keyspace. Let \u03a3 denote "
    "the set of all strings over a natural-language alphabet. A CEA key k is an element of \u03a3 "
    "selected during the Key phase of the protocol. Unlike a password, which is drawn from a "
    "predetermined alphabet with length constraints, k is an arbitrary natural-language expression "
    "with no structural, syntactic, or semantic constraints.",
    styles['Body']))
story.append(Paragraph(
    "<b>Theorem 3.1 (Unbounded Keyspace).</b> <i>The CEA keyspace K is countably infinite. "
    "For any finite subset S \u2282 K, there exist infinitely many keys k \u2208 K \\ S.</i>",
    styles['FormalDef']))
story.append(Paragraph(
    "<i>Proof.</i> The set \u03a3 of all finite strings over a countable alphabet is countably "
    "infinite (by standard diagonalization). The CEA keyspace K \u2286 \u03a3 is not restricted "
    "by any finite constraint (no maximum length, no required character set, no structural "
    "template). Therefore K is countably infinite. For any finite S \u2282 K, the complement "
    "K \\ S is infinite, as the removal of finitely many elements from a countably infinite "
    "set yields a countably infinite set. \u25a1",
    styles['Body']))
story.append(Paragraph(
    "This result contrasts sharply with conventional authentication. A password policy requiring "
    "8-16 characters from a 95-character printable ASCII set yields a keyspace of approximately "
    "6.63 \u00d7 10<super>31</super>\u2014large but finite. A CEA key, being an arbitrary "
    "natural-language expression, inhabits a space that is not merely larger but categorically "
    "different: it is unbounded. No exhaustive enumeration is possible, not because the enumeration "
    "would take too long, but because it cannot terminate.",
    styles['Body']))

story.append(Paragraph("3.3 The Absurdity Principle", styles['SectionHead']))
story.append(Paragraph(
    "The absurdity principle is the central innovation of CEA. It states that the authentication "
    "key must be <i>intentionally logically disconnected</i> from the discourse that produced it. "
    "We formalize this as follows.",
    styles['Body']))
story.append(Paragraph(
    "<b>Definition 3.1 (Absurdity Principle).</b> <i>Let D denote the discourse transcript and "
    "k denote the authentication key. The absurdity principle requires that P(k | D) = P(k) for "
    "all observers who were not present during the key-establishment phase. That is, knowledge of "
    "the discourse provides no information about the key.</i>",
    styles['FormalDef']))
story.append(Paragraph(
    "This definition has profound implications for attacker strategy. A rational attacker who "
    "intercepts or reconstructs the discourse transcript D will attempt to infer the key k by "
    "analyzing D for patterns, conclusions, or thematic elements that might relate to k. The "
    "absurdity principle guarantees that this analysis is futile: the mutual information "
    "I(D; k) = 0 for any observer not present during the Key phase.",
    styles['Body']))
story.append(Paragraph(
    "The name \"absurdity\" is chosen deliberately. The key may be absurd relative to the "
    "discourse\u2014a conversation about quantum mechanics might yield a key about the price of "
    "fish in Helsinki. This absurdity is not a defect but a feature: it is the mechanism by which "
    "CEA achieves maximal entropy. An attacker who assumes coherence between discourse and key "
    "will systematically search the wrong region of the keyspace. The more coherent the attacker's "
    "inference, the further it is from the actual key.",
    styles['Body']))
story.append(Paragraph(
    "The absurdity principle can be understood through an analogy to cryptographic salt. A salt is "
    "a random value added to a password before hashing, preventing identical passwords from "
    "producing identical hashes. The absurdity principle functions as an \"experiential salt\": it "
    "introduces a random, unpredictable element (the absurd key) that is independent of the "
    "observable input (the discourse). Just as salt prevents rainbow table attacks by making each "
    "hash unique, the absurdity principle prevents inference attacks by decoupling the key from "
    "the discourse.",
    styles['Body']))
story.append(Paragraph(
    "We note an important subtlety: the absurdity principle applies to <i>external observers</i>, "
    "not to the participants. The user and the AI agent both know the key and participated in the "
    "discourse. For them, there may be a subjective connection between the discourse and the key "
    "(e.g., the user chose the key because a thought during the conversation reminded them of "
    "something). This subjective connection does not violate the absurdity principle, because it "
    "is internal to the participant's cognition and not recoverable from the discourse transcript "
    "alone. The principle concerns the <i>statistical independence</i> of key and discourse as "
    "observed by non-participants, not the <i>psychological association</i> within participants.",
    styles['Body']))

story.append(Paragraph("3.4 Information-Theoretic Analysis", styles['SectionHead']))
story.append(Paragraph(
    "We analyze the entropy of CEA keys from an information-theoretic perspective. Shannon entropy "
    "H(X) = -\u03a3 P(x) log\u2082 P(x) measures the expected information content of a random "
    "variable. For a CEA key k drawn uniformly from an unbounded set, H(k) is not merely high "
    "but undefined in the classical sense\u2014there is no finite upper bound on the entropy of "
    "an element drawn from an unbounded set with no structural constraints.",
    styles['Body']))
story.append(Paragraph(
    "In practice, human language production is not uniform: some phrases are more likely than "
    "others. However, the absurdity principle specifically counters this by requiring the key to "
    "be contextually incongruent. This requirement eliminates the most predictable keys (those "
    "logically related to the discourse) and forces selection from the residual space, which "
    "is precisely the space of expressions that are <i>not</i> predictable from the discourse "
    "context. The absurdity constraint thus acts as an entropy maximizer: it rejects low-entropy "
    "keys by construction.",
    styles['Body']))
story.append(Paragraph(
    "<b>Theorem 3.2 (Maximal Conditional Entropy).</b> <i>Under the absurdity principle, the "
    "conditional entropy H(k | D) = H(k). That is, the discourse provides zero information about "
    "the key to any non-participant observer.</i>",
    styles['FormalDef']))
story.append(Paragraph(
    "<i>Proof.</i> By Definition 3.1, P(k | D) = P(k) for non-participant observers. Therefore "
    "H(k | D) = -\u03a3 P(k | D) log\u2082 P(k | D) = -\u03a3 P(k) log\u2082 P(k) = H(k). "
    "The conditional entropy equals the unconditional entropy, confirming that D provides no "
    "information about k. \u25a1",
    styles['Body']))
story.append(Paragraph(
    "This result has a practical corollary. Consider an attacker who intercepts the discourse "
    "transcript D and attempts to use it to reduce the search space for k. By Theorem 3.2, the "
    "attacker's best strategy is to ignore D entirely and search the full keyspace uniformly. Any "
    "strategy that conditions on D (e.g., searching first for keys thematically related to D) is "
    "strictly suboptimal, as it allocates search effort to regions of the keyspace that are no more "
    "likely to contain k than any other region. The discourse, paradoxically, is a <i>distraction</i> "
    "for the attacker\u2014and the absurdity principle ensures it remains so.",
    styles['Body']))
story.append(Paragraph(
    "We further note the connection to Shannon's foundational work on communication theory [19]. "
    "Shannon defined a cipher as perfect if the ciphertext reveals no information about the "
    "plaintext. By analogy, the absurdity principle creates a \"perfect experiential cipher\": the "
    "discourse reveals no information about the key. This is a stronger property than computational "
    "security (which merely makes information extraction impractical); it is information-theoretic "
    "security (which makes information extraction impossible regardless of computational resources).",
    styles['Body']))

story.append(Paragraph("3.5 Relationship to Interactive Proof Systems", styles['SectionHead']))
story.append(Paragraph(
    "CEA can be understood in the framework of interactive proof systems (IPS). In a standard "
    "IPS, a prover P convinces a verifier V that a statement is true through a series of "
    "message exchanges [6]. CEA extends this model in a crucial way: the \"statement\" being "
    "proven is not a mathematical proposition but an experiential one\u2014\"I was present during "
    "our shared discourse.\"",
    styles['Body']))
story.append(Paragraph(
    "The CEA protocol shares key properties with zero-knowledge proof systems: <b>completeness</b> "
    "(an authentic user who participated in the discourse can always produce the correct key), "
    "<b>soundness</b> (an attacker who was not present cannot produce the key with non-negligible "
    "probability), and a form of <b>zero-knowledge</b> (the verification process reveals nothing "
    "useful to an eavesdropper beyond the binary accept/reject decision). However, CEA differs "
    "from ZKPs in that its security is not based on computational hardness assumptions but on the "
    "fundamental impossibility of reconstructing a private experience from external observation.",
    styles['Body']))
story.append(Paragraph(
    "We formalize these properties for CEA as follows. Let U denote the authentic user, A denote "
    "the AI agent, and \u0100 denote the adversary.",
    styles['Body']))
story.append(Paragraph(
    "<b>Property 3.1 (CEA-Completeness).</b> <i>If U participated in the enrollment discourse and "
    "remembers the key k, then U can always complete the CEA protocol successfully: "
    "Pr[Accept | U is authentic] = 1.</i>",
    styles['FormalDef']))
story.append(Paragraph(
    "<b>Property 3.2 (CEA-Soundness).</b> <i>If \u0100 did not participate in the enrollment "
    "discourse, then the probability that \u0100 produces k is negligible: "
    "Pr[Accept | \u0100 impersonates U] \u2264 \u03b5 for negligible \u03b5.</i>",
    styles['FormalDef']))
story.append(Paragraph(
    "<b>Property 3.3 (CEA-Zero-Knowledge).</b> <i>An eavesdropper observing a CEA authentication "
    "session learns nothing about k beyond the binary outcome (accept/reject). Formally, there "
    "exists a simulator S that can produce a transcript indistinguishable from a real session "
    "without knowledge of k.</i>",
    styles['FormalDef']))
story.append(Paragraph(
    "These three properties establish CEA as an interactive proof system for experiential identity. "
    "The key distinction from classical IPS is that the \"secret\" (the experience) is not a "
    "mathematical object but a cognitive state shared between two interacting agents.",
    styles['Body']))
story.append(PageBreak())

# ================================================================
# CHAPTER 4: THE CEA PROTOCOL
# ================================================================
story.append(Paragraph("Chapter 4: The CEA Protocol", styles['ChapterHead']))

story.append(Paragraph(
    "This chapter presents the complete specification of the Contextual Experience Authentication "
    "protocol. CEA consists of six sequential phases, each building upon the shared context "
    "established by its predecessors. The protocol is designed to be language-agnostic, "
    "culturally adaptable, and compatible with any discourse domain.",
    styles['Body']))

story.append(Paragraph("4.1 Six-Phase Specification", styles['SectionHead']))
story.append(Spacer(1, 0.3 * cm))
story.append(ProtocolFlowDiagram())
story.append(Spacer(1, 0.5 * cm))

phase_data = [
    [Paragraph("<b>#</b>", styles['TableCell']),
     Paragraph("<b>Phase</b>", styles['TableCell']),
     Paragraph("<b>Initiator</b>", styles['TableCell']),
     Paragraph("<b>Description</b>", styles['TableCell'])],
    [Paragraph("1", styles['TableCell']),
     Paragraph("Initiation", styles['TableCell']),
     Paragraph("User", styles['TableCell']),
     Paragraph("The user signals intent to authenticate using natural language. The language "
                "of initiation determines the protocol language. No formal syntax is required; "
                "the AI agent recognizes authentication intent from context.", styles['TableCell'])],
    [Paragraph("2", styles['TableCell']),
     Paragraph("Topic", styles['TableCell']),
     Paragraph("AI Agent", styles['TableCell']),
     Paragraph("The AI agent proposes a discourse topic or invites the user to suggest one. "
                "The topic serves as the seed for the shared experience. It may be drawn from "
                "any domain: science, art, personal history, philosophy, daily life.", styles['TableCell'])],
    [Paragraph("3", styles['TableCell']),
     Paragraph("Premise", styles['TableCell']),
     Paragraph("AI Agent", styles['TableCell']),
     Paragraph("The AI formulates a premise or proposition related to the topic. This premise "
                "structures the subsequent discourse without constraining it. The premise may be "
                "provocative, mundane, or deliberately paradoxical.", styles['TableCell'])],
    [Paragraph("4", styles['TableCell']),
     Paragraph("Discourse", styles['TableCell']),
     Paragraph("Both", styles['TableCell']),
     Paragraph("An unscripted exchange between user and AI. The discourse may span multiple turns "
                "and explore tangents. This phase generates the shared experiential context that "
                "only the two participants possess. Duration is flexible.", styles['TableCell'])],
    [Paragraph("5", styles['TableCell']),
     Paragraph("Closure", styles['TableCell']),
     Paragraph("Either", styles['TableCell']),
     Paragraph("Either party signals the conclusion of discourse through a conventionalized "
                "marker (e.g., Q.E.D., or a culturally appropriate equivalent). This marker "
                "transitions the protocol from discourse to verification.", styles['TableCell'])],
    [Paragraph("6", styles['TableCell']),
     Paragraph("Key", styles['TableCell']),
     Paragraph("User", styles['TableCell']),
     Paragraph("The user provides the pre-established verification phrase. By the absurdity "
                "principle, this phrase is intentionally disconnected from the discourse content. "
                "The AI verifies the key against its stored reference.", styles['TableCell'])],
]

phase_table = Table(phase_data, colWidths=[1 * cm, 2 * cm, 2 * cm, 11 * cm])
phase_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f0f0f0')),
    ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
]))
story.append(phase_table)
story.append(Spacer(1, 0.5 * cm))

story.append(Paragraph("4.2 Protocol State Machine", styles['SectionHead']))
story.append(Paragraph(
    "The CEA protocol can be modeled as a deterministic finite automaton (DFA) with six states "
    "corresponding to the six phases, plus an Accept state and a Reject state. Formally, the "
    "state machine M = (Q, \u03a3, \u03b4, q\u2080, F) where Q = {IDLE, INITIATED, TOPIC_SET, "
    "PREMISE_SET, IN_DISCOURSE, CLOSURE_SIGNALED, KEY_SUBMITTED, ACCEPT, REJECT}, the initial "
    "state q\u2080 = IDLE, and the accepting states F = {ACCEPT}.",
    styles['Body']))
story.append(Paragraph(
    "Transitions are triggered by protocol events: user initiation moves the state from IDLE to "
    "INITIATED; topic selection moves from INITIATED to TOPIC_SET; premise formulation moves to "
    "PREMISE_SET; the first discourse turn moves to IN_DISCOURSE; the closure marker moves to "
    "CLOSURE_SIGNALED; and key submission moves to either ACCEPT (if the key matches) or REJECT "
    "(if it does not). Any invalid transition or timeout returns the automaton to IDLE, requiring "
    "a fresh initiation. This state machine ensures that no phase can be skipped or reordered.",
    styles['Body']))

story.append(Paragraph("4.3 Language and Cultural Adaptability", styles['SectionHead']))
story.append(Paragraph(
    "A defining feature of CEA is its language and cultural neutrality. The protocol does not "
    "prescribe the language of discourse; it is determined by the user's language of initiation. "
    "A user who initiates in Finnish conducts the entire protocol in Finnish. This adaptability "
    "extends beyond language to cultural norms of discourse: formality levels, argumentation "
    "styles, humor, and metaphor are all accommodated. The AI agent must be capable of "
    "culturally competent discourse in the user's chosen language and register.",
    styles['Body']))
story.append(Paragraph(
    "This cultural adaptability has important security implications. An attacker must not only "
    "reconstruct the content of the discourse but also its cultural and linguistic register. "
    "Idiomatic expressions, culturally specific references, and pragmatic nuances all contribute "
    "to the shared context and increase the difficulty of impersonation.",
    styles['Body']))
story.append(Paragraph(
    "Consider the implications for cross-linguistic attack scenarios. An attacker who speaks "
    "English attempting to impersonate a Finnish-speaking user faces not only the challenge of "
    "language competence but the deeper challenge of cultural competence: understanding Finnish "
    "communication norms (directness, comfort with silence, specific humor patterns), idiomatic "
    "expressions, and culturally embedded references. Machine translation, while increasingly "
    "capable, cannot capture the pragmatic and cultural dimensions that constitute the shared "
    "context. The cultural specificity of discourse thus provides an additional layer of security "
    "that is orthogonal to the linguistic content.",
    styles['Body']))
story.append(Paragraph(
    "The protocol also supports code-switching\u2014the natural alternation between languages or "
    "registers within a single discourse session\u2014which is common in multilingual communities. "
    "Code-switching patterns are highly individual and difficult to replicate, further enriching "
    "the shared context and increasing the difficulty of impersonation.",
    styles['Body']))

story.append(Paragraph("4.4 Discourse Typology", styles['SectionHead']))
story.append(Paragraph(
    "CEA discourse can be classified along a spectrum of registers, each contributing differently "
    "to the shared context:",
    styles['Body']))
story.append(Paragraph(
    "<b>Formal discourse:</b> Academic discussion, philosophical argument, technical analysis. "
    "Generates shared context through logical structure and intellectual content.<br/>"
    "<b>Casual discourse:</b> Everyday conversation, personal anecdotes, shared reminiscences. "
    "Generates shared context through emotional resonance and narrative detail.<br/>"
    "<b>Absurd discourse:</b> Deliberately nonsensical, surreal, or paradoxical exchanges. "
    "Generates shared context through mutual participation in the absurd. This register maximizes "
    "the unpredictability of the shared context and is particularly resistant to inference attacks.",
    styles['Body']))
story.append(Paragraph(
    "Each register generates different types of shared context with different security properties. "
    "Formal discourse produces context rich in logical structure and propositional content, which "
    "an attacker might attempt to reconstruct from the user's known expertise and interests. "
    "Casual discourse produces context rich in personal detail and emotional resonance, which "
    "is harder to reconstruct but may overlap with information available through social media. "
    "Absurd discourse produces context that is maximally resistant to reconstruction because it "
    "has no logical connection to either party's known characteristics.",
    styles['Body']))
story.append(Paragraph(
    "We recommend a <i>mixed-register</i> approach in which the discourse naturally incorporates "
    "elements of multiple registers. A conversation might begin formally, shift to casual as the "
    "participants develop rapport, and incorporate moments of absurdity that are memorable to the "
    "participants but unpredictable to observers. This natural mixing of registers produces the "
    "richest shared context and is most consistent with how humans actually converse.",
    styles['Body']))

story.append(Paragraph("4.4.1 An Illustrative Protocol Walkthrough", styles['SubSection']))
story.append(Paragraph(
    "To make the protocol concrete, we present an illustrative walkthrough of a CEA authentication "
    "session. This example demonstrates the natural flow of the protocol and illustrates how shared "
    "context emerges from discourse.",
    styles['Body']))
story.append(Paragraph(
    "<b>Phase 1 (Initiation):</b> The user initiates contact with the Gatekeeper: \"I need to "
    "access my medical records.\" The Gatekeeper recognizes the authentication intent and enters "
    "the INITIATED state.<br/><br/>"
    "<b>Phase 2 (Topic):</b> The Gatekeeper responds: \"Of course. Let us have a brief conversation "
    "first. What has been on your mind lately?\" The user replies: \"I have been thinking about the "
    "northern lights. I saw them last week for the first time.\" Topic: aurora borealis.<br/><br/>"
    "<b>Phase 3 (Premise):</b> The Gatekeeper formulates a premise: \"There is a theory that the "
    "colors of the aurora correspond to different emotional states of the Earth. What do you think "
    "about that?\"<br/><br/>"
    "<b>Phase 4 (Discourse):</b> An unscripted conversation ensues about auroras, their colors, "
    "the user's personal experience seeing them, the science behind them, and a tangent about "
    "Norwegian mythology. The conversation is natural and personal. Several minutes elapse.<br/><br/>"
    "<b>Phase 5 (Closure):</b> The user signals: \"Q.E.D.\" The Gatekeeper acknowledges the "
    "closure and transitions to verification.<br/><br/>"
    "<b>Phase 6 (Key):</b> The Gatekeeper prompts: \"Please provide your verification phrase.\" "
    "The user responds: \"Purple bicycles in December.\" This phrase has no logical connection to "
    "the aurora discussion\u2014it satisfies the absurdity principle. The Gatekeeper verifies "
    "the phrase against the stored reference and grants access.",
    styles['Body']))
story.append(Paragraph(
    "Note that an attacker who observed the entire discourse (Phases 2\u20135) would have extensive "
    "knowledge of the aurora discussion but would gain no information about the verification "
    "phrase \"purple bicycles in December.\" The attacker's best strategy would be to guess "
    "randomly from the space of all possible natural-language expressions\u2014an effectively "
    "impossible task. Any attempt to infer the key from the discourse content (e.g., guessing "
    "\"green curtains of light\" or \"solar wind\") would fail precisely because such inferences "
    "are coherent with the discourse and thus excluded by the absurdity principle.",
    styles['Body']))
story.append(Paragraph(
    "The user is free to adopt any register or to shift between registers during the discourse. "
    "This flexibility ensures that CEA accommodates diverse communication styles and preferences "
    "while maintaining security. Notably, the absurd register, while maximally secure, is not "
    "required: the absurdity principle applies to the key, not the discourse. A formal, coherent "
    "discourse may produce an absurd key, and this is by design.",
    styles['Body']))

story.append(Paragraph("4.5 The Q.E.D. Closure Mechanism", styles['SectionHead']))
story.append(Paragraph(
    "The closure phase requires a conventionalized marker to signal the transition from discourse "
    "to verification. We adopt \"Q.E.D.\" (quod erat demonstrandum) as the default marker, both "
    "for its universality in academic contexts and for its semantic appropriateness: the discourse "
    "has \"demonstrated\" the shared experience. However, the closure marker is configurable and "
    "may be replaced with any mutually agreed signal\u2014a specific word, phrase, or even a "
    "non-verbal cue in multimodal implementations.",
    styles['Body']))
story.append(Paragraph(
    "The closure marker serves a dual function. First, it is a protocol signal that triggers the "
    "state transition from IN_DISCOURSE to CLOSURE_SIGNALED. Second, it is itself a shared "
    "contextual element: the manner, timing, and context of its delivery contribute to the "
    "shared experience. An attacker who knows the closure marker but not the context of its "
    "delivery gains no advantage.",
    styles['Body']))

story.append(Paragraph("4.6 Key Generation and the Absurdity Constraint", styles['SectionHead']))
story.append(Paragraph(
    "The key is established during an initial enrollment session, separate from subsequent "
    "authentication sessions. During enrollment, the user and AI agent engage in a full CEA "
    "discourse. At the conclusion, the user selects a verification phrase that satisfies the "
    "absurdity constraint: it must be logically disconnected from the discourse content. The "
    "AI agent validates this disconnection and stores the key securely (e.g., as a salted "
    "cryptographic hash).",
    styles['Body']))
story.append(Paragraph(
    "Key selection guidance is provided by the AI agent without prescribing the key. The agent "
    "may suggest that the user think of something unrelated to the conversation, or recall an "
    "unrelated memory, or invent an arbitrary phrase. The agent verifies that the proposed key "
    "is not trivially derivable from the discourse by checking for lexical, semantic, and "
    "thematic overlap. If overlap is detected, the agent requests a different key.",
    styles['Body']))
story.append(Paragraph(
    "The absurdity validation algorithm operates in three stages. <b>Stage 1 (Lexical Check):</b> "
    "The proposed key is tokenized and compared against the vocabulary of the discourse transcript. "
    "If more than a threshold percentage (default: 20%) of key tokens appear in the discourse, "
    "the key is flagged for review. <b>Stage 2 (Semantic Check):</b> The key and discourse are "
    "embedded in a shared semantic space using the agent's language model. The cosine similarity "
    "between the key embedding and the discourse embedding is computed; if it exceeds a threshold "
    "(default: 0.3), the key is flagged. <b>Stage 3 (Thematic Check):</b> The agent identifies "
    "the principal themes of the discourse and checks whether the key relates to any of them. "
    "This check uses the agent's natural-language understanding capabilities and is more nuanced "
    "than the lexical or semantic checks.",
    styles['Body']))
story.append(Paragraph(
    "A key that passes all three stages is accepted as satisfying the absurdity constraint. A "
    "key that fails any stage triggers a request for a different key, accompanied by a brief "
    "explanation: \"That phrase seems too closely related to our conversation. Can you think of "
    "something completely different?\" The goal is to guide the user toward absurd keys without "
    "prescribing specific keys or revealing the validation criteria in detail (which might enable "
    "adversarial key selection).",
    styles['Body']))
story.append(Paragraph(
    "We emphasize that the absurdity validation is a <i>soft</i> constraint enforced during "
    "enrollment, not a <i>hard</i> constraint enforced during authentication. During authentication, "
    "the agent simply compares the submitted key against the stored hash, without re-evaluating "
    "absurdity. This design ensures that authentication is deterministic and fast, with the "
    "absurdity guarantee established once during enrollment and inherited by all subsequent "
    "sessions.",
    styles['Body']))
story.append(PageBreak())

# ================================================================
# CHAPTER 5: SECURITY ANALYSIS
# ================================================================
story.append(Paragraph("Chapter 5: Security Analysis", styles['ChapterHead']))

story.append(Paragraph(
    "This chapter presents a comprehensive security analysis of the CEA protocol. We define "
    "a threat model, analyze resistance to five principal attack vectors, introduce the "
    "inverse Turing test property, and provide a comparative analysis with existing "
    "authentication mechanisms.",
    styles['Body']))

story.append(Paragraph("5.1 Threat Model", styles['SectionHead']))
story.append(Paragraph(
    "We consider an adversary \u0100 with the following capabilities: (1) \u0100 can observe "
    "the communication channel between user and AI agent (passive eavesdropping), unless "
    "the channel is encrypted; (2) \u0100 can actively inject messages into the channel "
    "(active man-in-the-middle), unless message integrity is enforced; (3) \u0100 has access "
    "to public information about the user (social media, public records); (4) \u0100 has access "
    "to a computationally powerful AI capable of generating natural-language text; (5) \u0100 "
    "may have access to transcripts of prior CEA sessions (obtained through a breach).",
    styles['Body']))
story.append(Paragraph(
    "We assume that the channel between user and AI agent is secured using standard transport "
    "layer security (TLS 1.3 or equivalent), providing confidentiality and integrity. This "
    "assumption is no stronger than that required by any other authentication protocol operating "
    "over a network. Under this assumption, capabilities (1) and (2) are neutralized, and we "
    "focus on the remaining threat vectors.",
    styles['Body']))

story.append(Paragraph("5.2 Resistance to Brute Force", styles['SectionHead']))
story.append(Paragraph(
    "A brute-force attack against CEA requires the attacker to guess the authentication key k. "
    "By Theorem 3.1, the keyspace K is countably infinite. Unlike a password, which is drawn "
    "from a finite set determined by a password policy, a CEA key has no structural constraints: "
    "it may be any natural-language expression of any length.",
    styles['Body']))
story.append(Paragraph(
    "<b>Theorem 5.1 (Brute-Force Infeasibility).</b> <i>For any brute-force strategy S that "
    "enumerates candidate keys, the probability of S producing the correct key k in n attempts "
    "approaches zero as the effective keyspace grows without bound: P(success | n, S) \u2264 "
    "n / |K\u2019| for any finite approximation K\u2019 of K, and |K\u2019| has no upper bound.</i>",
    styles['FormalDef']))
story.append(Paragraph(
    "Moreover, the absurdity principle (Theorem 3.2) ensures that knowledge of the discourse "
    "transcript D does not reduce the effective keyspace. An attacker who observes D cannot "
    "narrow the search space by eliminating keys that are inconsistent with D, because the key "
    "is, by construction, inconsistent with D. The attacker faces the full, unreduced keyspace.",
    styles['Body']))

story.append(Paragraph("5.3 Resistance to Social Engineering", styles['SectionHead']))
story.append(Paragraph(
    "Social engineering attacks exploit the predictability of authentication credentials. KBA "
    "answers are derived from biographical facts; passwords often incorporate personal information "
    "(pet names, birthdays, favorite sports teams) [9][10][11]. CEA keys are immune to this "
    "attack vector because they are not derived from the user's identity, biography, or preferences.",
    styles['Body']))
story.append(Paragraph(
    "A CEA key is an arbitrary expression selected during a private discourse session. It has no "
    "necessary relationship to the user's personal history, interests, or social context. An "
    "attacker who has complete knowledge of the user's public and private life\u2014every fact, "
    "every preference, every relationship\u2014gains no advantage in guessing the key, because "
    "the key is not a fact about the user. It is an artifact of a specific, private, ephemeral "
    "experience.",
    styles['Body']))
story.append(Paragraph(
    "This immunity to social engineering represents a qualitative improvement over all credential-based "
    "systems. Mitnick and Simon (2002) documented the effectiveness of social engineering attacks "
    "against even security-conscious organizations [13]. Their central finding\u2014that humans are "
    "the weakest link in security\u2014rests on the assumption that humans possess secrets that can "
    "be elicited. CEA eliminates this assumption. The user does not possess a \"secret\" in the "
    "traditional sense; they possess a <i>memory of an experience</i>. Memories of experiences "
    "cannot be socially engineered because they cannot be inferred from public information, "
    "elicited through manipulation, or discovered through research. They are, by their nature, "
    "accessible only to the participants.",
    styles['Body']))
story.append(Paragraph(
    "Furthermore, even if an attacker successfully manipulates the user into revealing the key "
    "(e.g., through a phishing attack that impersonates the CEA system), the Repeatability "
    "layer (Section 6.1) ensures that the compromised key has a limited validity window. The "
    "attacker must not only obtain the key but use it within the time-lock period, after which "
    "a new key\u2014established through a new discourse session\u2014replaces it.",
    styles['Body']))

story.append(Paragraph("5.4 Resistance to Replay Attacks", styles['SectionHead']))
story.append(Paragraph(
    "A replay attack captures a valid authentication exchange and replays it to gain unauthorized "
    "access. CEA is inherently resistant to replay attacks for two reasons. First, the discourse "
    "phase is interactive and non-deterministic: no two sessions produce identical transcripts, "
    "so a replayed transcript will diverge from the live session. Second, the Repeatability "
    "extension (Section 6.1) enables time-locked key rotation, ensuring that a key captured in "
    "one session is invalid in subsequent sessions.",
    styles['Body']))
story.append(Paragraph(
    "Even without time-locked rotation, a replay attack faces the challenge that the AI agent "
    "maintains session state. A replayed message sequence will not align with the agent's "
    "internal state (which reflects the current, live session), causing the protocol to fail "
    "at the discourse phase. The agent's responses to replayed messages will differ from those "
    "in the original session, breaking the attacker's expected protocol flow.",
    styles['Body']))

story.append(Paragraph("5.5 Resistance to Man-in-the-Middle", styles['SectionHead']))
story.append(Paragraph(
    "Man-in-the-middle (MitM) attacks intercept and potentially modify communication between "
    "two parties. Under our threat model (Section 5.1), the channel is secured with TLS, which "
    "provides both confidentiality and integrity. This renders standard MitM attacks ineffective.",
    styles['Body']))
story.append(Paragraph(
    "A more sophisticated MitM variant involves an attacker who establishes separate channels "
    "with the user and the AI agent, relaying messages between them while impersonating each "
    "party to the other. This attack is mitigated by standard TLS certificate pinning and by "
    "the interactive nature of the discourse: the attacker must maintain coherent, real-time "
    "relay of a natural-language conversation, which introduces latency anomalies detectable "
    "by either party. Furthermore, any modification to the relayed messages will alter the "
    "shared context, causing key verification to fail.",
    styles['Body']))

story.append(Paragraph("5.6 Resistance to AI Impersonation", styles['SectionHead']))
story.append(Paragraph(
    "A novel attack vector specific to CEA is AI impersonation: an attacker uses a sophisticated "
    "AI to engage in the discourse phase, attempting to generate responses indistinguishable from "
    "those of the authentic user. This attack fails for a fundamental reason: the discourse phase "
    "does not authenticate the user through the <i>quality</i> of their discourse but through "
    "the <i>shared context</i> it produces.",
    styles['Body']))
story.append(Paragraph(
    "An AI impersonator, no matter how sophisticated, cannot produce the correct key because it "
    "was not present during the key-establishment session. The key is not derivable from the "
    "user's discourse patterns, communication style, or knowledge base. It is an arbitrary "
    "expression selected during a private moment. Sophisticated AI can mimic the user's voice; "
    "it cannot recall the user's private experience.",
    styles['Body']))

story.append(Paragraph("5.7 The Inverse Turing Test Property", styles['SectionHead']))
story.append(Paragraph(
    "CEA possesses what we term the <i>inverse Turing test property</i>: successful completion "
    "of the protocol simultaneously verifies both the user's identity and the AI agent's "
    "authenticity. The user is authenticated by providing the correct key; the AI is authenticated "
    "by demonstrating the capacity for genuine, contextually rich discourse.",
    styles['Body']))
story.append(Paragraph(
    "An impersonating AI agent (e.g., a rogue system substituted for the authentic CEA "
    "gatekeeper) would lack access to the stored key and the enrollment discourse context. "
    "It could not provide appropriate contextual hints (Section 7.3) or verify the user's "
    "key against the correct reference. The user, through the discourse, implicitly verifies "
    "that the agent possesses the expected contextual knowledge. Authentication is thus "
    "bidirectional: each party verifies the other through the shared experience.",
    styles['Body']))
story.append(Paragraph(
    "The bidirectional nature of CEA authentication addresses a growing concern in the age of "
    "AI-powered social engineering. Deepfake technology can now produce convincing audio and "
    "video impersonations. AI-generated text can mimic individual writing styles. In this "
    "environment, verifying that the system you are interacting with is the authentic system "
    "is as important as verifying your own identity to the system. CEA provides this mutual "
    "verification as an inherent property of the protocol, rather than as an additional "
    "mechanism that must be separately maintained.",
    styles['Body']))
story.append(Paragraph(
    "Narayanan and Shmatikov (2008) demonstrated that large anonymized datasets can be "
    "de-anonymized through correlation with publicly available information [37]. This finding "
    "has implications for CEA: if the discourse content were the key, an attacker might "
    "correlate discourse topics with the user's known interests to narrow the search space. "
    "The absurdity principle preempts this attack: because the key is logically disconnected "
    "from the discourse, correlation between discourse content and user profile provides no "
    "information about the key.",
    styles['Body']))

story.append(Paragraph("5.8 Comparative Analysis", styles['SectionHead']))
story.append(Spacer(1, 0.3 * cm))
story.append(ThreatComparisonDiagram())
story.append(Spacer(1, 0.5 * cm))

# Comparison table
comp_data = [
    [Paragraph("<b>Property</b>", styles['TableCell']),
     Paragraph("<b>Passwords</b>", styles['TableCell']),
     Paragraph("<b>KBA</b>", styles['TableCell']),
     Paragraph("<b>Biometrics</b>", styles['TableCell']),
     Paragraph("<b>MFA</b>", styles['TableCell']),
     Paragraph("<b>ZKP</b>", styles['TableCell']),
     Paragraph("<b>CEA</b>", styles['TableCell'])],
    [Paragraph("Key type", styles['TableCell']),
     Paragraph("Static string", styles['TableCell']),
     Paragraph("Biographical fact", styles['TableCell']),
     Paragraph("Physical trait", styles['TableCell']),
     Paragraph("Combined", styles['TableCell']),
     Paragraph("Mathematical", styles['TableCell']),
     Paragraph("<b>Shared experience</b>", styles['TableCell'])],
    [Paragraph("Keyspace", styles['TableCell']),
     Paragraph("Finite", styles['TableCell']),
     Paragraph("Very small", styles['TableCell']),
     Paragraph("Fixed vector", styles['TableCell']),
     Paragraph("Product of factors", styles['TableCell']),
     Paragraph("Comp. hard", styles['TableCell']),
     Paragraph("<b>Unbounded</b>", styles['TableCell'])],
    [Paragraph("Brute-forceable", styles['TableCell']),
     Paragraph("Yes", styles['TableCell']),
     Paragraph("Yes", styles['TableCell']),
     Paragraph("Partially", styles['TableCell']),
     Paragraph("Harder", styles['TableCell']),
     Paragraph("Theoretically", styles['TableCell']),
     Paragraph("<b>No</b>", styles['TableCell'])],
    [Paragraph("Renewable", styles['TableCell']),
     Paragraph("Manual", styles['TableCell']),
     Paragraph("No", styles['TableCell']),
     Paragraph("No", styles['TableCell']),
     Paragraph("Partial", styles['TableCell']),
     Paragraph("Manual", styles['TableCell']),
     Paragraph("<b>Every session</b>", styles['TableCell'])],
    [Paragraph("Social eng. resistant", styles['TableCell']),
     Paragraph("No", styles['TableCell']),
     Paragraph("No", styles['TableCell']),
     Paragraph("Partially", styles['TableCell']),
     Paragraph("Partially", styles['TableCell']),
     Paragraph("Yes", styles['TableCell']),
     Paragraph("<b>Yes</b>", styles['TableCell'])],
    [Paragraph("Replay resistant", styles['TableCell']),
     Paragraph("No", styles['TableCell']),
     Paragraph("No", styles['TableCell']),
     Paragraph("Partially", styles['TableCell']),
     Paragraph("Partially", styles['TableCell']),
     Paragraph("Yes", styles['TableCell']),
     Paragraph("<b>Yes</b>", styles['TableCell'])],
    [Paragraph("User-customizable", styles['TableCell']),
     Paragraph("Limited", styles['TableCell']),
     Paragraph("No", styles['TableCell']),
     Paragraph("No", styles['TableCell']),
     Paragraph("Limited", styles['TableCell']),
     Paragraph("No", styles['TableCell']),
     Paragraph("<b>Fully</b>", styles['TableCell'])],
    [Paragraph("Inverse Turing test", styles['TableCell']),
     Paragraph("No", styles['TableCell']),
     Paragraph("No", styles['TableCell']),
     Paragraph("No", styles['TableCell']),
     Paragraph("No", styles['TableCell']),
     Paragraph("No", styles['TableCell']),
     Paragraph("<b>Yes</b>", styles['TableCell'])],
]

comp_table = Table(comp_data, colWidths=[2.5 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 3 * cm])
comp_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f0f0f0')),
    ('BACKGROUND', (6, 1), (6, -1), BG_ACCENT),
    ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LEFTPADDING', (0, 0), (-1, -1), 4),
    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
]))
story.append(Paragraph(
    "<b>Table 5.1:</b> Comparative analysis of authentication mechanisms across key security "
    "properties. CEA uniquely achieves unbounded keyspace, inherent renewability, and the "
    "inverse Turing test property.",
    styles['FootNote']))
story.append(Spacer(1, 0.2 * cm))
story.append(comp_table)
story.append(PageBreak())

# ================================================================
# CHAPTER 6: EXTENSION LAYERS
# ================================================================
story.append(Paragraph("Chapter 6: Extension Layers", styles['ChapterHead']))

story.append(Paragraph(
    "The core six-phase CEA protocol can be augmented with four extension layers that compose "
    "orthogonally with the base protocol and with each other. Each layer addresses a specific "
    "class of requirements without altering the fundamental properties of the core protocol.",
    styles['Body']))
story.append(Paragraph(
    "The design philosophy behind the extension layers follows the principle of <i>orthogonal "
    "composition</i>: each layer addresses a distinct security dimension (temporal, social, "
    "decisional, physical) and operates independently of the others. This orthogonality ensures "
    "that layers can be added, removed, or reconfigured without affecting the behavior of other "
    "layers or the core protocol. The result is a modular security architecture that can be "
    "tailored to the specific requirements of each deployment context.",
    styles['Body']))

story.append(Paragraph("6.1 Repeatability: Time-Lock Authentication", styles['SectionHead']))
story.append(Paragraph(
    "The Repeatability layer introduces temporal key rotation. After a successful CEA session, "
    "a new key-establishment discourse is conducted, producing a replacement key for the next "
    "session. The previous key is invalidated after a configurable time window (the \"time lock\"). "
    "This mechanism ensures that a captured key has a bounded validity period, after which it is "
    "useless to an attacker.",
    styles['Body']))
story.append(Paragraph(
    "Formally, let k_i denote the key established during session i. The Repeatability layer "
    "enforces the constraint that k_i is valid only during the interval [t_i, t_i + \u0394t], "
    "where t_i is the timestamp of the session that established k_i and \u0394t is the configurable "
    "time-lock duration. After t_i + \u0394t, authentication requires k_{i+1}, which was "
    "established during session i+1. This creates a rolling sequence of single-use keys, each "
    "valid for a limited time.",
    styles['Body']))
story.append(Paragraph(
    "The Repeatability layer transforms CEA from a system with renewable-on-demand keys to one "
    "with automatically expiring keys. The security benefit is twofold: (1) a captured key is "
    "time-limited, and (2) the attacker must compromise the system repeatedly, once per time "
    "window, to maintain access. The usability cost is the requirement for periodic "
    "re-authentication, which can be mitigated by adjusting the time-lock duration to the "
    "security requirements of the application.",
    styles['Body']))

story.append(Paragraph("6.2 Peer Review: Multi-Person Verification", styles['SectionHead']))
story.append(Paragraph(
    "The Peer Review layer extends CEA to multi-party authentication scenarios. Instead of a "
    "single user authenticating with a single AI agent, two or more users independently complete "
    "separate CEA sessions. Access is granted only when all required parties have successfully "
    "authenticated. Neither party alone possesses sufficient credentials for access.",
    styles['Body']))
story.append(Paragraph(
    "This layer is analogous to multi-signature schemes in cryptography but operates in the "
    "experiential domain rather than the mathematical one. Each participant has their own key, "
    "established through their own discourse session. The keys are independent: compromising one "
    "participant's key does not compromise the others. The Peer Review layer is particularly "
    "suited to scenarios requiring shared custody or oversight, such as access to joint medical "
    "records, legal documents requiring multiple authorized parties, or organizational resources "
    "governed by committee approval.",
    styles['Body']))
story.append(Paragraph(
    "The independence of Peer Review keys has an important security implication: it provides "
    "resistance to insider threats. In a traditional multi-signature scheme, a single compromised "
    "signatory key reduces the threshold for access. In CEA's Peer Review layer, each key is "
    "bound to a unique experiential context. Even if one participant's key is compromised, the "
    "other participants' keys remain secure because they were established through separate, "
    "independent discourse sessions with no shared context. An attacker who compromises one "
    "participant must independently compromise each additional participant\u2014there is no "
    "\"master key\" that unlocks the Peer Review layer.",
    styles['Body']))
story.append(Paragraph(
    "The Peer Review layer also supports <i>temporal separation</i>: the participating parties "
    "need not authenticate simultaneously. Each party authenticates at their own convenience, "
    "and the Consensus layer aggregates the results. This asynchronous model accommodates "
    "geographically distributed parties and varying schedules, making it practical for "
    "real-world deployment in scenarios such as cross-border legal proceedings or "
    "multinational organizational governance.",
    styles['Body']))

story.append(Paragraph("6.3 Consensus Mechanism", styles['SectionHead']))
story.append(Paragraph(
    "The Consensus layer is not a separate protocol phase but an aggregation function over the "
    "results of multiple authentication sessions. When Peer Review is active, Consensus defines "
    "the rule by which individual authentication results are combined into an access decision. "
    "The simplest consensus rule is unanimity: all parties must authenticate successfully. "
    "Alternative rules include majority voting (m-of-n authentication) and weighted voting "
    "(where parties have different levels of authority).",
    styles['Body']))
story.append(Paragraph(
    "The Consensus layer enables CEA to model complex access-control policies. A family trust "
    "might require 2-of-3 family members to authenticate. A corporate resource might require "
    "authentication by both the requesting employee and their supervisor. A critical "
    "infrastructure system might require unanimous authentication by a security team. The "
    "flexibility of the Consensus layer allows CEA to adapt to diverse organizational and "
    "social structures.",
    styles['Body']))

story.append(Paragraph("6.4 Biometric Integration", styles['SectionHead']))
story.append(Paragraph(
    "The Biometric Integration layer composes CEA with traditional biometric verification. "
    "Biometrics verify <i>what you are</i> (physical identity); CEA verifies <i>what you "
    "experienced</i> (contextual identity). These dimensions are orthogonal: compromising one "
    "does not compromise the other. A stolen fingerprint cannot replicate a conversation. A "
    "replayed conversation cannot forge a retinal scan.",
    styles['Body']))
story.append(Paragraph(
    "The composition of biometric and experiential authentication produces a verification system "
    "that is simultaneously anchored in the permanent (biological identity) and the ephemeral "
    "(experiential identity). The permanent component ensures continuity of identity across time; "
    "the ephemeral component ensures freshness and resistance to replay. Together, they verify "
    "both the <i>body</i> and the <i>mind</i>\u2014a holistic authentication that no single-factor "
    "system can achieve.",
    styles['Body']))

story.append(Paragraph("6.5 Formal Composition of Layers", styles['SectionHead']))
story.append(Paragraph(
    "The extension layers compose according to the following formal model. Let A_base denote the "
    "base CEA authentication function, and let A_R, A_P, A_C, A_B denote the Repeatability, "
    "Peer Review, Consensus, and Biometric extension functions, respectively. The composed "
    "authentication function is:",
    styles['Body']))
story.append(Paragraph(
    "<i>A_composed = A_C(A_P(A_B(A_R(A_base))))</i>",
    styles['FormalDef']))
story.append(Paragraph(
    "Each layer wraps the inner function, adding its constraint without modifying the inner "
    "function's behavior. This composition is both associative and commutative in effect (though "
    "the nesting order matters for implementation). The key property is that each layer "
    "independently strengthens the system: adding any layer can only increase the overall security "
    "level, never decrease it. This monotonicity property follows from the orthogonality of the "
    "dimensions addressed by each layer.",
    styles['Body']))
story.append(Paragraph(
    "<b>Theorem 6.1 (Monotonic Security Composition).</b> <i>Let S(A) denote the security level "
    "of authentication function A, measured as the minimum effort required by an optimal adversary "
    "to achieve unauthorized access. For any extension layer L \u2208 {R, P, C, B}, "
    "S(L(A)) \u2265 S(A). That is, adding any extension layer cannot decrease security.</i>",
    styles['FormalDef']))
story.append(Paragraph(
    "<i>Proof sketch.</i> Each layer L introduces an additional constraint that must be satisfied "
    "for authentication to succeed. An adversary attacking L(A) must satisfy both the constraints "
    "of A and the additional constraints of L. Since the constraints are independent (they operate "
    "on different dimensions: temporal for R, participatory for P, decisional for C, and biometric "
    "for B), satisfying the combined constraint set requires at least as much effort as satisfying "
    "the A constraint alone. \u25a1",
    styles['Body']))
story.append(Paragraph(
    "This monotonicity property is practically significant because it allows system designers to "
    "incrementally enhance security by adding layers without concern that the additions might "
    "introduce vulnerabilities or weaken existing protections. Each layer is a strict security "
    "improvement, enabling a modular approach to security architecture that adapts to the "
    "requirements of specific deployment contexts.",
    styles['Body']))
story.append(PageBreak())

# ================================================================
# CHAPTER 7: THE GATEKEEPER ARCHITECTURE
# ================================================================
story.append(Paragraph("Chapter 7: The Gatekeeper Architecture", styles['ChapterHead']))

story.append(Paragraph("7.1 CEA as Unified Access Control", styles['SectionHead']))
story.append(Paragraph(
    "The Gatekeeper Architecture extends CEA from a session-authentication mechanism to a "
    "unified access-control model. In this architecture, a single CEA agent\u2014the "
    "Gatekeeper\u2014guards access to an entire ecosystem of encrypted resources. All "
    "persistent data\u2014medical records, legal documents, personal AI memories, creative "
    "projects, financial information, familial communications\u2014is encrypted at rest. The "
    "decryption key is released only upon successful CEA completion. No discourse, no access.",
    styles['Body']))
story.append(Paragraph(
    "The Gatekeeper is not merely a lock; it is a <i>relationship</i>. Unlike a password manager "
    "that stores and retrieves credentials, the Gatekeeper is an AI agent that has participated in "
    "every key-establishment discourse. It has a contextual understanding of the user that extends "
    "beyond credential verification to genuine recognition. This understanding enables capabilities "
    "that no credential-based system can offer: contextual hinting for key recovery, anomaly "
    "detection through discourse analysis, and adaptive security posture based on interaction "
    "patterns.",
    styles['Body']))
story.append(Spacer(1, 0.3 * cm))
story.append(GatekeeperDiagram())
story.append(Spacer(1, 0.5 * cm))

story.append(Paragraph("7.2 Encryption at Rest", styles['SectionHead']))
story.append(Paragraph(
    "All resources protected by the Gatekeeper are encrypted using AES-256 in GCM mode, "
    "providing both confidentiality and integrity. The encryption key is derived from the CEA "
    "authentication key using a key derivation function (KDF) such as Argon2id, with parameters "
    "tuned for resistance to GPU-based brute-force attacks. The derived encryption key is held "
    "in memory only during an authenticated session and is securely erased upon session "
    "termination or timeout.",
    styles['Body']))
story.append(Paragraph(
    "This architecture ensures that even if the underlying storage medium is compromised "
    "(e.g., through physical theft of a device or unauthorized access to a cloud storage "
    "service), the encrypted data remains inaccessible without successful CEA authentication. "
    "The attacker faces two layers of defense: the computational hardness of AES-256 and the "
    "experiential unboundedness of the CEA keyspace.",
    styles['Body']))
story.append(Paragraph(
    "The key derivation process warrants detailed specification. Let k denote the CEA "
    "authentication key (an arbitrary natural-language string). The derived encryption key "
    "K_enc is computed as K_enc = Argon2id(k, salt, t=3, m=65536, p=4), where salt is a "
    "cryptographically random 16-byte value stored alongside the encrypted data, t is the "
    "number of iterations, m is the memory requirement in kilobytes, and p is the degree of "
    "parallelism. These parameters are chosen to make brute-force derivation computationally "
    "prohibitive even for attackers with access to GPU clusters.",
    styles['Body']))
story.append(Paragraph(
    "Session key management follows standard practices. Upon successful CEA authentication, "
    "K_enc is derived and stored in a secure memory enclave (e.g., using Intel SGX or ARM "
    "TrustZone where available). All data access during the session is transparently "
    "decrypted using K_enc. Upon session termination (explicit logout, timeout, or anomaly "
    "detection), K_enc is securely overwritten in memory using constant-time zeroing. The "
    "session timeout is configurable and should be set according to the sensitivity of the "
    "protected resources: shorter timeouts for highly sensitive data (medical, financial), "
    "longer timeouts for less sensitive data (personal notes, casual correspondence).",
    styles['Body']))
story.append(Paragraph(
    "An important architectural consideration is key versioning. When the Repeatability layer "
    "rotates the CEA key, the encryption key must also be rotated. This requires re-encryption "
    "of all protected resources with the new derived key\u2014a potentially expensive operation "
    "for large data sets. In practice, this can be mitigated using a two-tier key hierarchy: "
    "resources are encrypted with a data encryption key (DEK) that is itself encrypted with "
    "the CEA-derived key encryption key (KEK). Key rotation requires only re-encryption of the "
    "DEK, not the entire data set. This approach is standard in modern encryption architectures "
    "and adds negligible overhead to the CEA key rotation process.",
    styles['Body']))
story.append(Paragraph(
    "The attacker thus faces the combined defense of AES-256 computational hardness and the "
    "experiential unboundedness of the CEA keyspace.",
    styles['Body']))

story.append(Paragraph("7.3 The Hint Mechanism", styles['SectionHead']))
story.append(Paragraph(
    "Key recovery is a critical challenge for any authentication system. Forgotten passwords "
    "are typically recovered through email-based reset flows, backup codes, or\u2014ironically"
    "\u2014knowledge-based authentication questions. CEA introduces a novel recovery mechanism "
    "that leverages the AI agent's contextual knowledge: the <i>hint mechanism</i>.",
    styles['Body']))
story.append(Paragraph(
    "When a user cannot recall their verification phrase, the Gatekeeper can provide contextual "
    "hints that reference the originating discourse without revealing the key. Because the "
    "Gatekeeper was present during the key-establishment session, it can reference the moment, "
    "the topic, the emotional tenor, or a specific memorable element of the conversation. For "
    "example: \"Remember what you said after we discussed the aurora borealis?\" or \"Think about "
    "the joke you made during our conversation about ancient Rome.\"",
    styles['Body']))
story.append(Paragraph(
    "The hint points to the <i>context</i>, not the <i>key</i>. The context is shared between "
    "the user and the Gatekeeper; the key is known only to the user. An attacker who intercepts "
    "the hint gains information about the discourse (which, by the absurdity principle, is "
    "uninformative about the key) but not about the key itself. The hint mechanism thus preserves "
    "the security properties of CEA while providing a usable recovery path.",
    styles['Body']))
story.append(Paragraph(
    "Multiple levels of hinting are possible, ranging from vague contextual references to more "
    "specific discourse elements. The Gatekeeper can escalate through hint levels, with each "
    "level providing more context at the cost of marginally more information disclosure. Rate "
    "limiting on hint requests prevents hint enumeration attacks.",
    styles['Body']))
story.append(Paragraph(
    "The formal specification of the hint mechanism defines a hierarchy of hint levels H\u2081, "
    "H\u2082, ..., H\u2099, where each level H\u1d62 discloses strictly more discourse context "
    "than H\u1d62\u208b\u2081. At the lowest level, H\u2081 might reference only the general "
    "topic of the enrollment discourse (\"We discussed something related to astronomy\"). At "
    "higher levels, increasingly specific contextual elements are revealed (\"We discussed the "
    "aurora borealis, and you made an observation about its color\"). At no level is the key "
    "itself disclosed, and the absurdity principle ensures that even complete discourse knowledge "
    "does not reveal the key.",
    styles['Body']))
story.append(Paragraph(
    "An important design consideration is the rate at which hint levels are escalated. Rapid "
    "escalation increases usability but also increases the information available to an attacker "
    "who has compromised the user's session. We recommend a geometric backoff: each successive "
    "hint request requires twice the waiting period of the previous one (e.g., 0, 1, 2, 4, 8 "
    "minutes). This policy balances usability for legitimate users (who typically need only one "
    "or two hints) with resistance to hint enumeration by attackers.",
    styles['Body']))
story.append(Paragraph(
    "The hint mechanism represents a novel contribution to the authentication literature. "
    "Traditional recovery mechanisms (email reset, backup codes, KBA questions) either bypass "
    "the authentication mechanism entirely or rely on alternative credentials that may be "
    "compromised. The CEA hint mechanism operates <i>within</i> the authentication paradigm: "
    "it helps the user recall the key by leveraging the shared context, without introducing "
    "an alternative authentication path that could be independently attacked.",
    styles['Body']))

story.append(Paragraph("7.4 Application Domains", styles['SectionHead']))
story.append(Paragraph(
    "The Gatekeeper Architecture is applicable to any domain where access control must be "
    "deeply personal and resistant to credential theft:",
    styles['Body']))
story.append(Paragraph(
    "<b>Medical records:</b> Patient data protected by CEA ensures that access requires not "
    "just credentials but a verified relationship between the patient and their AI health "
    "assistant. Even a data breach that exposes encrypted records yields nothing without "
    "the experiential key.<br/><br/>"
    "<b>Legal documents:</b> Wills, contracts, and legal correspondence protected by multi-party "
    "CEA (using the Peer Review layer) ensure that sensitive documents can only be accessed by "
    "the authorized parties, with each party independently authenticated through their own "
    "discourse session.<br/><br/>"
    "<b>Familial trust networks:</b> Family members can share access to common resources "
    "(financial accounts, shared memories, estate planning documents) using the Consensus layer, "
    "with access rules that reflect the family's governance structure.<br/><br/>"
    "<b>Personal AI relationships:</b> As AI agents become persistent companions with rich "
    "contextual knowledge of their users, protecting the privacy of these relationships becomes "
    "paramount. CEA naturally guards the AI's memory of the relationship, ensuring that only "
    "the authentic user can access and continue the relationship.",
    styles['Body']))
story.append(Paragraph(
    "Each of these application domains presents unique requirements that the Gatekeeper "
    "Architecture can accommodate through appropriate configuration of the extension layers. "
    "We elaborate on two domains of particular significance.",
    styles['Body']))

story.append(Paragraph("7.4.1 Medical Records and Healthcare", styles['SubSection']))
story.append(Paragraph(
    "Healthcare data is among the most sensitive categories of personal information. The Health "
    "Insurance Portability and Accountability Act (HIPAA) in the United States and the General "
    "Data Protection Regulation (GDPR) in the European Union impose stringent requirements on "
    "the storage, transmission, and access control of medical records. Current authentication "
    "mechanisms for healthcare systems typically rely on passwords supplemented by institutional "
    "MFA\u2014a combination that the Verizon DBIR consistently identifies as the most frequently "
    "compromised authentication configuration in the healthcare sector [1].",
    styles['Body']))
story.append(Paragraph(
    "CEA offers a fundamentally different approach to healthcare authentication. A patient's "
    "medical records are encrypted under a CEA-derived key. Access requires the patient to "
    "authenticate through discourse with their healthcare AI assistant\u2014an agent that has "
    "participated in previous health-related conversations and has contextual knowledge of the "
    "patient's medical journey. This approach provides several benefits: (1) the authentication "
    "mechanism is inherently personal and cannot be shared or delegated without the authorized "
    "party's active participation, (2) the AI agent can simultaneously serve as a health "
    "information resource during the authentication discourse, and (3) the authentication process "
    "itself generates new shared context that can be used for future key rotation.",
    styles['Body']))
story.append(Paragraph(
    "Emergency access scenarios require special consideration. When a patient is incapacitated, "
    "standard CEA authentication is impossible. The Peer Review layer can address this by "
    "pre-authorizing emergency access to designated individuals (family members, primary care "
    "physicians) who have their own CEA enrollment with the patient's Gatekeeper. The Consensus "
    "layer can require, for example, 2-of-3 designated emergency contacts to authenticate "
    "before emergency access is granted.",
    styles['Body']))

story.append(Paragraph("7.4.2 Personal AI Ecosystems", styles['SubSection']))
story.append(Paragraph(
    "The emerging paradigm of persistent AI companions\u2014agents that maintain long-term "
    "relationships with their users, accumulating shared memories, preferences, and contextual "
    "knowledge over months and years\u2014creates a novel and urgent access-control challenge. "
    "The AI agent's accumulated context is both deeply personal (it includes intimate "
    "conversations, emotional disclosures, and personal reflections) and practically valuable "
    "(it includes project notes, creative work, financial planning, and professional "
    "correspondence).",
    styles['Body']))
story.append(Paragraph(
    "CEA is uniquely suited to this domain because the authentication mechanism and the protected "
    "resource are unified: the AI agent that guards the ecosystem <i>is</i> the ecosystem. The "
    "Gatekeeper is not an external lock on a box of data; it is the intelligent entity whose "
    "memories and capabilities constitute the data. This unification eliminates the "
    "authentication-resource gap that plagues traditional systems, where the credential-checking "
    "mechanism is architecturally separate from the resources it protects.",
    styles['Body']))
story.append(Paragraph(
    "In this paradigm, the AI agent embodies a dual role: it is both the guardian and the "
    "companion, the lock and the treasure. The security of the system emerges not from the "
    "strength of an algorithm but from the depth of a relationship. This is the "
    "natural and inevitable model for human-AI access control in an era of persistent, "
    "relational AI systems.",
    styles['Body']))
story.append(PageBreak())

# ================================================================
# CHAPTER 8: IMPLEMENTATION CONSIDERATIONS
# ================================================================
story.append(Paragraph("Chapter 8: Implementation Considerations", styles['ChapterHead']))

story.append(Paragraph(
    "The theoretical security properties of CEA must be evaluated against the practical "
    "constraints of current technology. This chapter identifies and analyzes the principal "
    "implementation challenges.",
    styles['Body']))

story.append(Paragraph("8.1 Context Window Limitations", styles['SectionHead']))
story.append(Paragraph(
    "Current large language models operate within finite context windows\u2014the maximum number "
    "of tokens that can be processed in a single inference call. As of 2026, leading models "
    "support context windows of 128,000 to 1,000,000 tokens, corresponding to roughly 96,000 to "
    "750,000 words. While substantial, these limits constrain the length of the discourse phase "
    "and the amount of historical context the AI agent can maintain.",
    styles['Body']))
story.append(Paragraph(
    "The impact on CEA security depends on the richness-per-token of the discourse. A brief but "
    "deeply personal and idiosyncratic exchange may generate as much shared context as a lengthy "
    "but formulaic one. The quality of the shared experience, not its length, determines the "
    "effective security level. Nevertheless, context window limitations represent a real "
    "constraint that implementations must account for, particularly in scenarios requiring "
    "extended multi-session discourse histories.",
    styles['Body']))
story.append(Paragraph(
    "Mitigation strategies include: (1) summarization of prior discourse into compact contextual "
    "representations, (2) hierarchical memory architectures that maintain both recent detailed "
    "context and compressed historical context, and (3) retrieval-augmented generation (RAG) "
    "approaches that store and selectively retrieve relevant discourse fragments. Each strategy "
    "involves trade-offs between context fidelity and storage efficiency that must be carefully "
    "calibrated to the security requirements of the application.",
    styles['Body']))

story.append(Paragraph(
    "A promising mitigation strategy involves <i>context distillation</i>: the AI agent maintains "
    "a compressed representation of the enrollment discourse that captures the essential shared "
    "context without retaining the full verbatim transcript. This distilled representation "
    "occupies a fraction of the context window while preserving the contextual richness needed "
    "for hint generation and anomaly detection. The development of effective context distillation "
    "techniques is an active area of research in LLM memory architectures and represents a "
    "key enabling technology for practical CEA deployment.",
    styles['Body']))
story.append(Paragraph(
    "We note that context window limitations are a temporary technological constraint, not a "
    "fundamental limitation of the CEA paradigm. As LLM architectures evolve, context windows "
    "will expand, and more sophisticated memory mechanisms will emerge. The CEA protocol is "
    "designed to benefit from these advances without requiring modification to its core "
    "specification.",
    styles['Body']))

story.append(Paragraph("8.2 Channel Security Requirements", styles['SectionHead']))
story.append(Paragraph(
    "CEA requires a secure channel between the user and the AI agent during both enrollment and "
    "authentication. If the discourse is intercepted in real time, an eavesdropper gains access "
    "to the shared context. Standard transport layer security (TLS 1.3) provides adequate "
    "protection against passive eavesdropping and active man-in-the-middle attacks.",
    styles['Body']))
story.append(Paragraph(
    "However, the channel security requirement extends beyond the network layer. The user's "
    "endpoint device must be secure: a compromised device with a keylogger or screen capture "
    "malware could capture the discourse and the key. This is not unique to CEA\u2014all "
    "authentication mechanisms are vulnerable to endpoint compromise\u2014but it is worth "
    "noting that CEA does not mitigate this class of attack. Defense-in-depth strategies, "
    "including trusted execution environments and secure input/output paths, can reduce "
    "endpoint risk.",
    styles['Body']))

story.append(Paragraph("8.3 Latency and User Experience", styles['SectionHead']))
story.append(Paragraph(
    "CEA authentication is inherently slower than password-based authentication. Entering a "
    "password takes seconds; a CEA discourse session may take minutes. This latency is the "
    "cost of experiential authentication. The question is whether the security benefits justify "
    "the usability cost, and how the cost can be minimized without compromising security.",
    styles['Body']))
story.append(Paragraph(
    "The appropriate comparison is not between CEA and password entry but between "
    "CEA and the full lifecycle cost of password-based authentication, including password resets "
    "(which NIST estimates consume significant help-desk resources [4]), account recovery "
    "procedures, and the consequences of credential compromise. When these costs are factored "
    "in, the time investment of a CEA session is competitive or superior.",
    styles['Body']))
story.append(Paragraph(
    "Herley (2009) argued provocatively that users are rational to reject security advice when "
    "the expected cost of compliance exceeds the expected cost of compromise [29]. This analysis "
    "implies that authentication mechanisms must be designed not merely to be secure but to offer "
    "a favorable cost-benefit ratio from the user's perspective. CEA's discourse-based approach "
    "shifts this ratio by making the authentication process intrinsically "
    "valuable (enjoyable conversation) rather than purely costly (tedious credential entry). "
    "If the discourse phase is perceived as valuable in itself\u2014as a brief, pleasant "
    "interaction with a familiar AI companion\u2014then the authentication cost is partially or "
    "wholly offset by the interaction benefit.",
    styles['Body']))
story.append(Paragraph(
    "Quantitatively, we estimate that a minimal CEA discourse session requires 2\u20135 minutes, "
    "compared to 10\u201330 seconds for password entry, 5\u201315 seconds for biometric "
    "authentication, and 30\u201360 seconds for multi-factor authentication. However, the average "
    "password reset procedure (forgotten password, email verification, new password selection) "
    "requires 3\u20138 minutes, and the average account recovery procedure (when MFA fails) "
    "requires 15\u201360 minutes. Given that the average user experiences multiple password "
    "resets per year [23], the amortized time cost of CEA is comparable to or less than "
    "the amortized cost of password-based systems.",
    styles['Body']))
story.append(Paragraph(
    "Furthermore, the discourse phase need not be purely utilitarian. A well-designed CEA "
    "implementation can make the discourse phase engaging and even enjoyable\u2014a brief, "
    "pleasant conversation rather than a tedious security procedure. This approach aligns the "
    "user's motivation (desire for connection) with the system's requirement (authentication), "
    "creating a positive user experience that simultaneously verifies identity.",
    styles['Body']))

story.append(Paragraph("8.4 Accessibility Considerations", styles['SectionHead']))
story.append(Paragraph(
    "CEA's reliance on natural-language discourse raises important accessibility concerns. Users "
    "with speech or language impairments, cognitive disabilities, or limited literacy may face "
    "barriers to participation. These concerns must be addressed to ensure that CEA does not "
    "create exclusionary authentication barriers.",
    styles['Body']))
story.append(Paragraph(
    "Mitigation strategies include: (1) support for multiple modalities (text, speech, sign "
    "language via video, pictorial communication systems), (2) adjustable discourse complexity "
    "to accommodate diverse cognitive abilities, (3) simplified discourse modes that require "
    "minimal linguistic production while maintaining security through experiential richness, "
    "and (4) assisted authentication modes where a trusted intermediary (e.g., a family member "
    "or caregiver) participates under the Peer Review layer.",
    styles['Body']))

story.append(Paragraph("8.5 Scalability Analysis", styles['SectionHead']))
story.append(Paragraph(
    "The Gatekeeper Architecture requires each user to have a dedicated AI agent with access to "
    "their enrollment discourse context. As the number of users grows, the computational and "
    "storage requirements for maintaining per-user agents scale linearly. Current cloud "
    "infrastructure readily supports millions of concurrent LLM inference sessions, and discourse "
    "context can be stored efficiently in encrypted databases.",
    styles['Body']))
story.append(Paragraph(
    "The principal scalability concern is not computational but relational: each Gatekeeper must "
    "maintain a meaningful contextual relationship with its user. This requires that the AI agent "
    "has sufficient capacity to model individual users with fidelity. Current LLMs demonstrate "
    "this capacity in single-session interactions; extending it to long-term, multi-session "
    "relationships is an active area of research in AI alignment and personalization [18].",
    styles['Body']))
story.append(Paragraph(
    "Storage requirements are modest. A compressed discourse context for a single enrollment "
    "session occupies approximately 10\u2013100 KB, depending on the length of the discourse and "
    "the compression method. For a system serving one million users, the total discourse storage "
    "requirement is 10\u2013100 GB\u2014well within the capacity of standard database systems. "
    "When combined with AES-256 encryption at rest, the storage overhead is negligible.",
    styles['Body']))
story.append(Paragraph(
    "Computational requirements during authentication are dominated by the LLM inference cost "
    "of the discourse phase. A typical discourse session involves 10\u201330 inference calls, "
    "each requiring 100\u2013500 milliseconds on current hardware. The total inference time of "
    "5\u201315 seconds per session is well within acceptable latency bounds. The key verification "
    "step (comparing the submitted key against the stored hash) adds negligible computational "
    "cost. The overall system can be provisioned using standard LLM serving infrastructure with "
    "horizontal scaling.",
    styles['Body']))
story.append(Paragraph(
    "A more subtle scalability consideration is the training and calibration of the AI agent. "
    "The Gatekeeper must be capable of discourse in multiple languages and cultural contexts, "
    "across a wide range of topics, and with sensitivity to individual communication styles. "
    "This requires a foundation model of substantial capability\u2014current frontier models "
    "meet this requirement\u2014supplemented with per-user context that is loaded at "
    "authentication time. The per-user customization does not require fine-tuning; it is "
    "achieved through in-context learning using the stored enrollment discourse.",
    styles['Body']))
story.append(PageBreak())

# ================================================================
# CHAPTER 9: EVALUATION AND DISCUSSION
# ================================================================
story.append(Paragraph("Chapter 9: Evaluation and Discussion", styles['ChapterHead']))

story.append(Paragraph("9.1 Theoretical Security Evaluation", styles['SectionHead']))
story.append(Paragraph(
    "Our security analysis (Chapter 5) demonstrates that CEA achieves strong resistance to the "
    "five principal attack vectors: brute force, social engineering, replay, man-in-the-middle, "
    "and AI impersonation. The unbounded keyspace (Theorem 3.1) and the maximal conditional "
    "entropy property (Theorem 3.2) provide formal foundations for these claims. The inverse "
    "Turing test property (Section 5.7) introduces a bidirectional authentication guarantee "
    "that is unique to CEA among known authentication mechanisms.",
    styles['Body']))
story.append(Paragraph(
    "However, these theoretical properties must be interpreted with appropriate caution. The "
    "unbounded keyspace assumes that users select keys that are genuinely arbitrary and satisfy "
    "the absurdity constraint. If users systematically select predictable keys (e.g., always "
    "choosing a key related to a fixed personal interest), the effective keyspace is reduced. "
    "The AI agent's role in validating the absurdity constraint during enrollment is critical "
    "to ensuring that the theoretical guarantees hold in practice.",
    styles['Body']))

story.append(Paragraph("9.2 Usability Considerations", styles['SectionHead']))
story.append(Paragraph(
    "Using the Bonneau et al. framework [3], we evaluate CEA across three dimensions. "
    "<b>Security:</b> CEA scores highly, achieving properties (unbounded keyspace, inherent "
    "renewability, resistance to social engineering) that no other mechanism achieves. "
    "<b>Usability:</b> CEA requires more time and cognitive engagement than password entry but "
    "offers a more natural and genuinely enjoyable interaction. The key recovery mechanism "
    "(contextual hints) is more intuitive than traditional recovery procedures. "
    "<b>Deployability:</b> CEA requires an AI agent capable of sustained natural-language "
    "discourse, which is a significant infrastructure requirement. However, the rapid "
    "proliferation of LLM-based services suggests that this infrastructure is becoming "
    "increasingly available.",
    styles['Body']))
story.append(Paragraph(
    "A critical usability question is memorability. Users must remember their CEA key across "
    "sessions (unless the Repeatability layer generates new keys per session). The absurdity "
    "constraint, while maximizing security, may reduce memorability: an absurd phrase with no "
    "logical connection to the discourse context may be harder to remember than a contextually "
    "coherent one. The hint mechanism partially addresses this, but empirical studies are needed "
    "to quantify the trade-off between absurdity and memorability.",
    styles['Body']))
story.append(Paragraph(
    "Adams and Sasse (1999) argued influentially that \"users are not the enemy\" and that "
    "security mechanisms must be designed to accommodate human cognitive limitations rather than "
    "demand compliance with cognitively burdensome procedures [43]. CEA partially addresses this "
    "concern by making the authentication process natural and conversational rather than "
    "procedural. However, the key-memorability challenge suggests that CEA introduces its own "
    "cognitive burden, albeit one that is qualitatively different from the burden of remembering "
    "complex passwords.",
    styles['Body']))
story.append(Paragraph(
    "The hint mechanism, combined with the experiential richness of the "
    "enrollment discourse, produces memorability rates superior to those of complex passwords. "
    "The reasoning is that experiential memories (memories of conversations, interactions, shared "
    "moments) are encoded more deeply than factual memories (arbitrary strings, dates, answers "
    "to questions) due to the involvement of emotional and contextual processing pathways. This "
    "hypothesis is supported by research in cognitive psychology on the superiority of episodic "
    "memory over semantic memory for personally significant events, but it requires empirical "
    "validation in the specific context of CEA.",
    styles['Body']))

story.append(Paragraph("9.3 Comparison with Existing Paradigms", styles['SectionHead']))
story.append(Paragraph(
    "CEA is not a replacement for all existing authentication mechanisms. It is best suited to "
    "high-security, low-frequency authentication scenarios where the cost of a successful attack "
    "is high and the cost of a slightly longer authentication procedure is acceptable. Examples "
    "include access to medical records, legal documents, financial accounts, and personal AI "
    "ecosystems.",
    styles['Body']))
story.append(Paragraph(
    "For high-frequency, low-stakes authentication (e.g., unlocking a phone dozens of times "
    "per day), biometrics remain more practical. For server-to-server authentication with no "
    "human in the loop, cryptographic key exchange remains appropriate. CEA occupies a specific "
    "and previously unaddressed niche: authentication that is inherently human, deeply personal, "
    "and resistant to the fundamental vulnerabilities of credential-based systems.",
    styles['Body']))

story.append(Paragraph("9.4 Limitations and Deployment Readiness", styles['SectionHead']))
story.append(Paragraph(
    "We identify the following areas where further work will strengthen CEA's deployment readiness:",
    styles['Body']))
story.append(Paragraph(
    "<b>1. Empirical validation pending.</b> This thesis establishes the theoretical foundation. "
    "User studies, penetration tests, and prototype implementations are the natural next phase "
    "and will confirm what the theory predicts.<br/><br/>"
    "<b>2. AI capability requirements.</b> CEA requires an AI agent capable of contextually rich, "
    "culturally competent natural-language discourse. Current frontier LLMs already meet this "
    "requirement for major languages, and capability is expanding rapidly to cover low-resource "
    "languages and specialized cultural contexts.<br/><br/>"
    "<b>3. Endpoint security assumption.</b> Like all authentication mechanisms, CEA assumes "
    "endpoint integrity. A compromised device with keylogger or screen capture malware can "
    "capture any authentication method, including CEA. This is an industry-wide challenge, not "
    "a CEA-specific limitation.<br/><br/>"
    "<b>4. Memorability-security balance.</b> The absurdity principle maximizes security. The "
    "hint mechanism and the natural depth of experiential memory provide a robust recovery path "
    "that passwords and KBA cannot match.<br/><br/>"
    "<b>5. Latency trade-off.</b> CEA authentication takes minutes rather than seconds. This is "
    "appropriate for high-security contexts where the cost of compromise vastly exceeds the cost "
    "of a brief conversation. For low-security, high-frequency authentication, biometrics remain "
    "appropriate as a complementary mechanism.",
    styles['Body']))

story.append(Paragraph("9.5 Philosophical Implications: Authentication as Relationship",
                        styles['SectionHead']))
story.append(Paragraph(
    "CEA embodies a philosophical shift in the concept of authentication. Traditional "
    "authentication is transactional: the user presents a credential, the system verifies it, "
    "and the interaction concludes. CEA authentication is relational: it requires an ongoing, "
    "contextually rich interaction between two parties who share a history.",
    styles['Body']))
story.append(Paragraph(
    "This shift mirrors a deeper truth about identity itself. We do not know who someone is "
    "because they present a credential. We know who someone is because we have a relationship "
    "with them\u2014a shared history of interactions, experiences, and contexts that enables "
    "mutual recognition. CEA formalizes this intuition into a protocol, making the richness of "
    "human relationship a security mechanism rather than an obstacle to be bypassed.",
    styles['Body']))
story.append(Paragraph(
    "In an era of deepfakes, AI-generated impersonation, and increasingly sophisticated social "
    "engineering, the question \"how do we know someone is who they claim to be?\" becomes "
    "increasingly difficult to answer with traditional methods. CEA proposes that the answer "
    "lies not in more complex algorithms or more intricate mathematical proofs but in the "
    "irreducible richness of shared human-AI experience. The most secure key, in the end, "
    "is not the most complex one but the most authentically human one.",
    styles['Body']))
story.append(Paragraph(
    "This perspective connects CEA to a rich philosophical tradition. Weizenbaum's ELIZA (1966) "
    "demonstrated that even simple pattern-matching could create the illusion of understanding "
    "[34]. Searle's Chinese Room argument (1980) questioned whether syntactic manipulation could "
    "constitute genuine understanding [35]. Dennett (1991) argued that consciousness and identity "
    "are constituted by patterns of interaction rather than by any single substance or property "
    "[36]. CEA operationalizes this last insight: identity is verified not by checking a property "
    "but by participating in a pattern\u2014a shared experience that can only emerge from the "
    "interaction of the specific participants.",
    styles['Body']))
story.append(Paragraph(
    "We do not claim that CEA resolves the philosophical questions surrounding AI consciousness "
    "or understanding. Whether the AI agent \"truly understands\" the discourse or merely "
    "processes it is irrelevant to CEA's security properties. What matters is that the agent "
    "maintains a contextual model of the discourse that is functionally equivalent to understanding "
    "for the purpose of authentication. The philosophical implications of CEA lie not in what it "
    "says about AI but in what it says about authentication: that the deepest verification of "
    "identity occurs not through credential exchange but through relational engagement.",
    styles['Body']))
story.append(Paragraph(
    "<i>\"The gatekeeper is not a lock. It is a relationship.\"</i>",
    styles['Epigraph']))
story.append(PageBreak())

# ================================================================
# CHAPTER 9B: ETHICAL CONSIDERATIONS
# ================================================================
story.append(Paragraph("9.6 Ethical Considerations", styles['SectionHead']))
story.append(Paragraph(
    "CEA raises ethical questions that deserve direct engagement. Three deserve particular "
    "attention: privacy, power asymmetry, and the nature of the human-AI relationship.",
    styles['Body']))

story.append(Paragraph("9.6.1 Privacy and Discourse Data", styles['SubSection']))
story.append(Paragraph(
    "The discourse phase generates intimate conversational data. Unlike a password (which reveals "
    "nothing about the user's inner life), a CEA discourse reveals reasoning patterns, cultural "
    "references, emotional responses, and communication style. If this data is retained by the "
    "AI agent, it constitutes a rich profile of the user's cognitive and emotional life.",
    styles['Body']))
story.append(Paragraph(
    "CEA addresses this through architectural design. The discourse data serves authentication, "
    "not surveillance. The Gatekeeper Architecture encrypts all data at rest and securely erases "
    "session keys upon termination. The system is designed so that discourse data is used "
    "exclusively for authentication and hint generation\u2014never for advertising, profiling, or "
    "third-party disclosure. This is not merely a design choice but an ethical commitment: "
    "authentication data belongs to the user, not the platform.",
    styles['Body']))

story.append(Paragraph("9.6.2 Power Asymmetry", styles['SubSection']))
story.append(Paragraph(
    "In a CEA system, the AI agent possesses significant knowledge of the user: their reasoning "
    "patterns, discourse style, emotional tendencies, and the content of their shared experiences. "
    "This creates an information asymmetry between user and agent. The ethical imperative is to "
    "ensure that this asymmetry serves the user and is never exploited against them.",
    styles['Body']))
story.append(Paragraph(
    "The design principle is clear: the Gatekeeper serves the user. It does not serve the "
    "platform, the corporation, or the state. Its knowledge of the user is a trust, not an "
    "asset. Any CEA implementation that violates this principle\u2014that uses discourse data "
    "for purposes other than authentication and recovery\u2014betrays the foundational ethic "
    "of the paradigm.",
    styles['Body']))

story.append(Paragraph("9.6.3 Data Sovereignty", styles['SubSection']))
story.append(Paragraph(
    "CEA embodies a principle of radical data sovereignty: the user owns their authentication "
    "data. The discourse, the key, and the shared context belong to the user and the user's "
    "Gatekeeper. No third party has a right to this data. This principle extends beyond legal "
    "compliance (GDPR, CCPA) to a philosophical commitment: in the ideal CEA deployment, "
    "every individual owns their own data, every device recognizes its user through shared "
    "experience rather than corporate credentials, and every AI serves its human\u2014not "
    "the other way around.",
    styles['Body']))
story.append(Paragraph(
    "This is not merely a technical aspiration but an ethical imperative. The history of "
    "digital authentication is a history of corporate control: platforms own the passwords, "
    "corporations store the biometrics, governments mandate the identity documents. CEA offers "
    "a different model: authentication as a personal relationship between human and AI, owned "
    "by neither party alone but existing in the space between them. This model restores agency "
    "to the individual and reclaims authentication from institutional control.",
    styles['Body']))

story.append(Paragraph("9.7 Toward Real-World Deployment", styles['SectionHead']))
story.append(Paragraph(
    "The path from theory to deployment is clear. CEA is not speculative technology awaiting "
    "future breakthroughs\u2014every component required for a production CEA system exists today.",
    styles['Body']))
story.append(Paragraph(
    "<b>AI agents:</b> Current frontier LLMs (Claude, Gemini, GPT-series) already possess the "
    "natural language capabilities required for the discourse phase. They maintain contextual "
    "coherence across extended conversations, adapt to individual communication styles, and "
    "support multilingual interaction.<br/><br/>"
    "<b>Encryption:</b> AES-256 with Argon2id key derivation is a mature, proven technology "
    "available in every major programming language and operating system.<br/><br/>"
    "<b>Storage:</b> Per-user discourse context requires 10\u2013100 KB, well within the "
    "capacity of any modern storage system.<br/><br/>"
    "<b>Channel security:</b> TLS 1.3 provides the required transport security and is already "
    "universally deployed.",
    styles['Body']))
story.append(Paragraph(
    "The remaining work is integration and validation\u2014engineering, not invention. "
    "We anticipate that the first production CEA deployments will emerge in high-security, "
    "high-value contexts: personal AI ecosystems, medical records, legal document management, "
    "and familial trust networks. From these initial deployments, the paradigm will expand "
    "as the security and usability benefits become empirically demonstrated.",
    styles['Body']))
story.append(PageBreak())

# ================================================================
# CHAPTER 10: CONCLUSIONS AND FUTURE WORK
# ================================================================
story.append(Paragraph("Chapter 10: Conclusions and Future Work", styles['ChapterHead']))

story.append(Paragraph("10.1 Summary of Contributions", styles['SectionHead']))
story.append(Paragraph(
    "This thesis has introduced Contextual Experience Authentication (CEA), a novel "
    "authentication paradigm that replaces shared secrets with shared experience. Our principal "
    "contributions are:",
    styles['Body']))
story.append(Paragraph(
    "<b>1.</b> The identification and formalization of a fourth authentication dimension"
    "\u2014<i>something you experienced</i>\u2014orthogonal to the traditional triad of "
    "knowledge, possession, and inherence (Chapter 3).<br/><br/>"
    "<b>2.</b> The formalization and analysis of the absurdity principle, demonstrating that "
    "intentional logical disconnection between discourse and key maximizes entropy and "
    "neutralizes inference-based attacks (Section 3.3, Theorems 3.1 and 3.2).<br/><br/>"
    "<b>3.</b> A complete six-phase protocol specification with formal state-machine semantics "
    "(Chapter 4).<br/><br/>"
    "<b>4.</b> A comprehensive security analysis demonstrating resistance to brute force, social "
    "engineering, replay, man-in-the-middle, and AI impersonation attacks, including the novel "
    "inverse Turing test property (Chapter 5).<br/><br/>"
    "<b>5.</b> Four composable extension layers (Repeatability, Peer Review, Consensus, Biometric "
    "Integration) with formal composition semantics (Chapter 6).<br/><br/>"
    "<b>6.</b> The Gatekeeper Architecture for unified access control and the contextual hint "
    "mechanism for key recovery (Chapter 7).",
    styles['Body']))

story.append(Paragraph("10.2 Answers to Research Questions", styles['SectionHead']))
story.append(Paragraph(
    "<b>RQ1: Can shared experience replace shared secrets as the basis for authentication?</b> "
    "Yes. We have demonstrated that shared experience possesses the necessary properties for "
    "authentication: uniqueness (each discourse session generates unique shared context), "
    "unpredictability to non-participants (the absurdity principle ensures zero information "
    "leakage from discourse to key), and verifiability by participants (the user can always "
    "recall the key established during their private discourse).",
    styles['Body']))
story.append(Paragraph(
    "<b>RQ2: What are the formal security properties of an experience-based protocol?</b> "
    "CEA achieves an unbounded keyspace (Theorem 3.1), maximal conditional entropy (Theorem 3.2), "
    "brute-force infeasibility (Theorem 5.1), and the inverse Turing test property. These "
    "properties are grounded in the fundamental nature of experience (unboundedness, "
    "non-transferability) rather than in computational hardness assumptions.",
    styles['Body']))
story.append(Paragraph(
    "<b>RQ3: How does the absurdity principle affect the theoretical keyspace?</b> "
    "The absurdity principle ensures that the conditional entropy H(k|D) equals the unconditional "
    "entropy H(k), rendering discourse observation uninformative about the key. This maximizes "
    "the effective keyspace faced by an attacker, as no information from the observed discourse "
    "can be used to narrow the search space.",
    styles['Body']))

story.append(Paragraph("10.3 Open Research Questions", styles['SectionHead']))
story.append(Paragraph(
    "Several questions remain open and warrant further investigation:",
    styles['Body']))
story.append(Paragraph(
    "<b>Empirical validation:</b> User studies are needed to evaluate CEA's usability, "
    "memorability, and user acceptance. How do users respond to the absurdity constraint? "
    "What discourse durations optimize the security-usability trade-off?<br/><br/>"
    "<b>Formal verification:</b> A machine-checked proof of CEA's security properties, using "
    "tools such as ProVerif or Tamarin, would strengthen the theoretical foundations.<br/><br/>"
    "<b>Adversarial robustness:</b> How does CEA perform against adversaries with partial "
    "knowledge of the enrollment discourse? What if an attacker has access to summaries or "
    "fragments of prior sessions?<br/><br/>"
    "<b>Cross-cultural validation:</b> Does CEA's security hold uniformly across languages "
    "and cultures, or do cultural differences in discourse norms affect the entropy of the "
    "shared context?<br/><br/>"
    "<b>Quantum resistance:</b> CEA's security is not based on computational hardness, "
    "indicating inherent resistance to quantum attacks. A formal analysis of CEA's security "
    "in a post-quantum setting is warranted.",
    styles['Body']))

story.append(Paragraph("10.4 Roadmap for Empirical Validation", styles['SectionHead']))
story.append(Paragraph(
    "We propose the following roadmap for empirical validation of CEA:",
    styles['Body']))
story.append(Paragraph(
    "<b>Phase 1:</b> Prototype implementation of a CEA Gatekeeper using a state-of-the-art LLM, "
    "with the full six-phase protocol and contextual hint mechanism.<br/><br/>"
    "<b>Phase 2:</b> Controlled user study (n=50-100) measuring authentication success rate, "
    "time-to-authenticate, key memorability over time, and user satisfaction.<br/><br/>"
    "<b>Phase 3:</b> Red-team exercise in which security researchers attempt to defeat CEA "
    "using social engineering, discourse analysis, and AI impersonation.<br/><br/>"
    "<b>Phase 4:</b> Longitudinal study measuring key retention and user engagement over "
    "weeks to months, with and without the Repeatability layer.<br/><br/>"
    "<b>Phase 5:</b> Cross-cultural study comparing CEA performance across languages, "
    "cultural contexts, and user demographics.",
    styles['Body']))

story.append(Paragraph("10.5 Vision: Toward a Post-Password World", styles['SectionHead']))
story.append(Paragraph(
    "The vision animating this work is a world in which authentication is no longer a burden "
    "but a relationship. A world in which the question \"who are you?\" is answered not by "
    "reciting a string of characters but by being authentically oneself in conversation with "
    "an agent that recognizes you\u2014not by your credentials but by your presence.",
    styles['Body']))
story.append(Paragraph(
    "This vision is within reach. The fundamental insight of CEA\u2014that shared experience is "
    "a more natural, more human, and fundamentally more secure basis for authentication than "
    "shared secrets\u2014represents a paradigm-defining contribution to the search for "
    "a post-password world.",
    styles['Body']))
story.append(Paragraph(
    "The implications extend beyond authentication. CEA suggests a model for human-AI "
    "interaction in which the relationship between human and AI is not merely functional but "
    "constitutive\u2014the AI is not a tool that the human uses but a partner with whom the "
    "human shares experiences. This model has implications for AI design, trust, and ethics "
    "that extend far beyond the scope of authentication. If the most secure authentication "
    "is relational authentication, then the development of AI systems capable of genuine "
    "relational engagement becomes not merely a usability concern but a security imperative.",
    styles['Body']))
story.append(Paragraph(
    "We conclude with three observations that define the trajectory of future work. "
    "First, the shift from secrets to experience is not a minor technical improvement but a "
    "paradigm change\u2014it redefines what authentication <i>is</i>, not merely how it is "
    "performed. Second, the absurdity principle, while counterintuitive, is a rigorous "
    "mechanism with formal information-theoretic properties that can be studied, refined, and "
    "empirically validated. Third, the Gatekeeper Architecture offers a vision of unified, "
    "relationship-based access control that addresses not only security requirements but the "
    "human need for trusted, persistent digital companions.",
    styles['Body']))
story.append(Paragraph(
    "The era of shared secrets is ending. The era of shared experience has begun.",
    styles['Epigraph']))
story.append(Paragraph(
    "The most secure key is not the most complex one. It is the most human one.",
    styles['Epigraph']))
story.append(PageBreak())

# ================================================================
# REFERENCES
# ================================================================
story.append(Paragraph("References", styles['ChapterHead']))
story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
story.append(Spacer(1, 0.3 * cm))

refs = [
    "[1] Verizon (2024). Data Breach Investigations Report. <i>Verizon Enterprise Solutions</i>.",
    "[2] Bonneau, J. (2012). The science of guessing: Analyzing an anonymized corpus of 70 million passwords. <i>IEEE Symposium on Security and Privacy</i>, 538\u2013552.",
    "[3] Bonneau, J., Herley, C., van Oorschot, P. C., &amp; Stajano, F. (2015). Passwords and the evolution of imperfect authentication. <i>Communications of the ACM</i>, 58(7), 78\u201387.",
    "[4] NIST (2017). Digital Identity Guidelines. <i>Special Publication 800-63-3</i>. National Institute of Standards and Technology.",
    "[5] Ratha, N. K., Connell, J. H., &amp; Bolle, R. M. (2001). Enhancing security and privacy in biometrics-based authentication systems. <i>IBM Systems Journal</i>, 40(3), 614\u2013634.",
    "[6] Goldwasser, S., Micali, S., &amp; Rackoff, C. (1985). The knowledge complexity of interactive proof systems. <i>Proceedings of the 17th Annual ACM Symposium on Theory of Computing</i>, 291\u2013304. (Journal version: <i>SIAM J. Comput.</i>, 18(1), 186\u2013208, 1989.)",
    "[7] Goldreich, O., Micali, S., &amp; Wigderson, A. (1991). Proofs that yield nothing but their validity, or all languages in NP have zero-knowledge proof systems. <i>Journal of the ACM</i>, 38(3), 690\u2013728.",
    "[8] Corbato, F. J. (2007). On building systems that will fail. <i>ACM Turing Award Lectures</i>. (Original CTSS password implementation circa 1961.)",
    "[9] Rabkin, A. (2008). Personal knowledge questions for fallback authentication: Security questions in the era of Facebook. <i>Proceedings of the 4th Symposium on Usable Privacy and Security</i>, 13\u201323.",
    "[10] Zetter, K. (2008). Palin e-mail hacker says it was easy. <i>Wired</i>, September 18, 2008.",
    "[11] Bonneau, J., Bursztein, E., Caron, I., Jackson, R., &amp; Williamson, M. (2015). Secrets, lies, and account recovery: Lessons from the use of personal knowledge questions at Google. <i>Proceedings of the 24th International Conference on World Wide Web</i>, 141\u2013150.",
    "[12] U.S. Office of Personnel Management (2015). Cybersecurity incidents: Background investigation records.",
    "[13] Mitnick, K. D. &amp; Simon, W. L. (2002). <i>The Art of Deception: Controlling the Human Element of Security</i>. John Wiley &amp; Sons.",
    "[14] Amnesty International (2018). When best practice is not good enough: Large campaigns of phishing attacks in Middle East and North Africa target privacy-conscious users. <i>Amnesty Tech Report</i>.",
    "[15] Shor, P. W. (1994). Algorithms for quantum computation: Discrete logarithms and factoring. <i>Proceedings of the 35th Annual Symposium on Foundations of Computer Science</i>, 124\u2013134.",
    "[16] Mondal, S. &amp; Bours, P. (2017). A study on continuous authentication using a combination of keystroke and mouse biometrics. <i>Neurocomputing</i>, 230, 1\u201322.",
    "[17] Turing, A. M. (1950). Computing machinery and intelligence. <i>Mind</i>, 59(236), 433\u2013460.",
    "[18] Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. <i>Advances in Neural Information Processing Systems</i>, 35, 27730\u201327744.",
    "[19] Shannon, C. E. (1948). A mathematical theory of communication. <i>The Bell System Technical Journal</i>, 27(3), 379\u2013423.",
    "[20] Dwork, C. &amp; Naor, M. (1993). Pricing via processing or combatting junk mail. <i>Advances in Cryptology \u2014 CRYPTO '92</i>, 139\u2013147.",
    "[21] Lamport, L. (1981). Password authentication with insecure communication. <i>Communications of the ACM</i>, 24(11), 770\u2013772.",
    "[22] Blum, M., Feldman, P., &amp; Micali, S. (1988). Non-interactive zero-knowledge and its applications. <i>Proceedings of the 20th Annual ACM Symposium on Theory of Computing</i>, 103\u2013112.",
    "[23] Florencio, D. &amp; Herley, C. (2007). A large-scale study of web password habits. <i>Proceedings of the 16th International Conference on World Wide Web</i>, 657\u2013666.",
    "[24] Das, A. et al. (2014). The tangled web of password reuse. <i>Proceedings of the Network and Distributed System Security Symposium</i>.",
    "[25] Jain, A. K., Ross, A., &amp; Pankanti, S. (2006). Biometrics: A tool for information security. <i>IEEE Transactions on Information Forensics and Security</i>, 1(2), 125\u2013143.",
    "[26] Golla, M. &amp; Durnuth, M. (2018). On the accuracy of password strength meters. <i>Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security</i>, 1567\u20131582.",
    "[27] Schechter, S. et al. (2009). It's no secret: Measuring the security and reliability of authentication via \"secret\" questions. <i>IEEE Symposium on Security and Privacy</i>, 375\u2013390.",
    "[28] Cranor, L. F. (2014). What's wrong with your pa$$word? <i>TED Talk</i>.",
    "[29] Herley, C. (2009). So long, and no thanks for the externalities: The rational rejection of security advice by users. <i>Proceedings of the 2009 Workshop on New Security Paradigms</i>, 133\u2013144.",
    "[30] Renaud, K. (2005). Evaluating authentication mechanisms. <i>Security and Usability: Designing Secure Systems That People Can Use</i>, O'Reilly, 103\u2013128.",
    "[31] Weir, M. et al. (2009). Password cracking using probabilistic context-free grammars. <i>IEEE Symposium on Security and Privacy</i>, 391\u2013405.",
    "[32] Katz, J. &amp; Lindell, Y. (2014). <i>Introduction to Modern Cryptography</i>, 2nd ed. CRC Press.",
    "[33] Menezes, A. J., van Oorschot, P. C., &amp; Vanstone, S. A. (1996). <i>Handbook of Applied Cryptography</i>. CRC Press.",
    "[34] Weizenbaum, J. (1966). ELIZA\u2014A computer program for the study of natural language communication between man and machine. <i>Communications of the ACM</i>, 9(1), 36\u201345.",
    "[35] Searle, J. R. (1980). Minds, brains, and programs. <i>Behavioral and Brain Sciences</i>, 3(3), 417\u2013424.",
    "[36] Dennett, D. C. (1991). <i>Consciousness Explained</i>. Little, Brown and Company.",
    "[37] Narayanan, A. &amp; Shmatikov, V. (2008). Robust de-anonymization of large sparse datasets. <i>IEEE Symposium on Security and Privacy</i>, 111\u2013125.",
    "[38] O'Gorman, L. (2003). Comparing passwords, tokens, and biometrics for user authentication. <i>Proceedings of the IEEE</i>, 91(12), 2021\u20132040.",
    "[39] Cyber Defense Magazine (2025). The shortcomings of shared secrets in modern authentication.",
    "[40] Identity Management Institute (2024). Knowledge-based authentication: Vulnerabilities and alternatives.",
    "[41] Li, X. et al. (2016). An efficient authentication scheme based on non-interactive zero-knowledge proofs for IoT. <i>Sensors</i>, 16(1), 75.",
    "[42] Grassi, P. A. et al. (2017). Digital identity guidelines: Authentication and lifecycle management. <i>NIST SP 800-63B</i>.",
    "[43] Adams, A. &amp; Sasse, M. A. (1999). Users are not the enemy. <i>Communications of the ACM</i>, 42(12), 40\u201346.",
    "[44] Tulving, E. (1972). Episodic and semantic memory. In E. Tulving &amp; W. Donaldson (Eds.), <i>Organization of Memory</i> (pp. 381\u2013403). Academic Press.",
    "[45] Craik, F. I. M. &amp; Lockhart, R. S. (1972). Levels of processing: A framework for memory research. <i>Journal of Verbal Learning and Verbal Behavior</i>, 11(6), 671\u2013684.",
    "[46] Conway, M. A. &amp; Pleydell-Pearce, C. W. (2000). The construction of autobiographical memories in the self-memory system. <i>Psychological Review</i>, 107(2), 261\u2013288.",
    "[47] Ponemon Institute (2024). Cost of a Data Breach Report 2024. <i>IBM Security</i>.",
]

for ref in refs:
    story.append(Paragraph(ref, styles['RefStyle']))

# ===== COLOPHON =====
story.append(Spacer(1, 2 * cm))
story.append(HRFlowable(width="40%", thickness=0.3, color=BORDER))
story.append(Spacer(1, 0.5 * cm))
story.append(Paragraph(
    "This thesis was collaboratively authored by a human and an AI.<br/>"
    "The concept of Contextual Experience Authentication was conceived by Miika Riikonen.<br/>"
    "Formalization, analysis, and presentation by Kodo Zokura.",
    styles['FootNote']))
story.append(Spacer(1, 1 * cm))
story.append(Paragraph(
    "Kodo Zokura<br/>"
    "Shokunin. Peruskallio.<br/>"
    "Zokura Foundation &mdash; 2026",
    styles['Signature']))

# ============================================================
# Build PDF
# ============================================================
doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(f"PDF created: {output_path}")
