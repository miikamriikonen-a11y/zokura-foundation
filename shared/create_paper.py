#!/usr/bin/env python3
"""
Contextual Experience Authentication (CEA) — White Paper v2
Riikonen & Kodō Zoku RA, 2026
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, Color
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, Flowable
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from reportlab.graphics.shapes import Group
from reportlab.graphics import renderPDF

# --- Colors ---
DARK = HexColor('#1a1a1a')
MID = HexColor('#333333')
LIGHT = HexColor('#555555')
ACCENT = HexColor('#8B0000')  # Deep red — warmth, power
ACCENT2 = HexColor('#2C5F2D')  # Deep green — trust
ACCENT3 = HexColor('#1B4F72')  # Deep blue — depth
BORDER = HexColor('#cccccc')
BG_LIGHT = HexColor('#f7f7f7')
BG_ACCENT = HexColor('#fdf6f0')

# --- Custom Flowable for diagrams ---
class CEAFlowDiagram(Flowable):
    """Protocol flow diagram"""
    def __init__(self, width=450, height=200):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        phases = [
            ("1", "Initiation", ACCENT3),
            ("2", "Topic", ACCENT3),
            ("3", "Discourse", ACCENT2),
            ("4", "Closure", ACCENT),
            ("5", "Verify", ACCENT),
        ]

        box_w = 72
        box_h = 50
        gap = 15
        start_x = 10
        y = self.height - 80

        # Title
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(start_x, self.height - 20, "Core Protocol Flow")

        # Draw boxes and arrows
        for i, (num, label, color) in enumerate(phases):
            x = start_x + i * (box_w + gap)

            # Box
            c.setFillColor(color)
            c.roundRect(x, y, box_w, box_h, 6, fill=1, stroke=0)

            # Text
            c.setFillColor(HexColor('#ffffff'))
            c.setFont("Helvetica-Bold", 14)
            c.drawCentredString(x + box_w/2, y + 30, num)
            c.setFont("Helvetica", 8)
            c.drawCentredString(x + box_w/2, y + 12, label)

            # Arrow
            if i < len(phases) - 1:
                c.setStrokeColor(BORDER)
                c.setLineWidth(1.5)
                arrow_x = x + box_w + 2
                arrow_y = y + box_h/2
                c.line(arrow_x, arrow_y, arrow_x + gap - 4, arrow_y)
                # Arrowhead
                c.setFillColor(BORDER)
                c.drawString(arrow_x + gap - 8, arrow_y - 3, ">")

        # Extension phases below
        ext_y = y - 60
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(LIGHT)
        c.drawString(start_x, ext_y + 40, "Extension Phases (optional):")

        ext_phases = [
            ("6", "Repeat", "Time-lock"),
            ("7", "Peer Review", "Multi-party"),
            ("C", "Consensus", "Access granted"),
        ]

        for i, (num, label, desc) in enumerate(ext_phases):
            x = start_x + i * (box_w + gap + 30)

            # Dashed box
            c.setStrokeColor(ACCENT if num == "C" else LIGHT)
            c.setDash(3, 3) if num != "C" else c.setDash()
            c.setLineWidth(1)
            c.setFillColor(BG_ACCENT if num == "C" else BG_LIGHT)
            c.roundRect(x, ext_y - 10, box_w + 20, 45, 6, fill=1, stroke=1)
            c.setDash()

            c.setFillColor(DARK)
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(x + (box_w+20)/2, ext_y + 20, num)
            c.setFont("Helvetica", 7.5)
            c.drawCentredString(x + (box_w+20)/2, ext_y + 5, label)
            c.setFillColor(LIGHT)
            c.setFont("Helvetica-Oblique", 6.5)
            c.drawCentredString(x + (box_w+20)/2, ext_y - 5, desc)


class AuthDimensionDiagram(Flowable):
    """Authentication dimensions comparison"""
    def __init__(self, width=450, height=170):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv

        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(10, self.height - 20, "Authentication Dimensions")

        dimensions = [
            ("What you KNOW", "Passwords, PINs, KBA", HexColor('#999999'), "Finite. Crackable."),
            ("What you HAVE", "Tokens, devices, keys", HexColor('#777777'), "Stealable. Clonable."),
            ("What you ARE", "Biometrics", ACCENT3, "Permanent. Irreplaceable if compromised."),
            ("What you EXPERIENCED", "CEA", ACCENT, "Unbounded. Ephemeral. Renewable."),
        ]

        y = self.height - 50
        for label, examples, color, note in dimensions:
            # Bar
            c.setFillColor(color)
            c.roundRect(10, y, 180, 22, 4, fill=1, stroke=0)
            c.setFillColor(HexColor('#ffffff'))
            c.setFont("Helvetica-Bold", 8)
            c.drawString(16, y + 8, label)

            # Description
            c.setFillColor(MID)
            c.setFont("Helvetica", 8)
            c.drawString(200, y + 12, examples)
            c.setFillColor(LIGHT)
            c.setFont("Helvetica-Oblique", 7.5)
            c.drawString(200, y + 2, note)

            y -= 32


class GatekeeperDiagram(Flowable):
    """CEA as gatekeeper architecture"""
    def __init__(self, width=450, height=180):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv

        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(10, self.height - 20, "Unified Gatekeeper Architecture")

        # User
        c.setFillColor(ACCENT3)
        c.roundRect(10, 60, 80, 60, 8, fill=1, stroke=0)
        c.setFillColor(HexColor('#ffffff'))
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(50, 100, "User")
        c.setFont("Helvetica", 7)
        c.drawCentredString(50, 85, "+ Biometrics")
        c.drawCentredString(50, 75, "(optional)")

        # Arrow
        c.setStrokeColor(DARK)
        c.setLineWidth(2)
        c.line(95, 90, 140, 90)
        c.setFont("Helvetica-Oblique", 7)
        c.setFillColor(LIGHT)
        c.drawCentredString(117, 96, "discourse")

        # Gatekeeper (CEA)
        c.setFillColor(ACCENT)
        c.roundRect(145, 50, 100, 80, 8, fill=1, stroke=0)
        c.setFillColor(HexColor('#ffffff'))
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(195, 105, "CEA")
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(195, 90, "Gatekeeper")
        c.setFont("Helvetica", 7)
        c.drawCentredString(195, 75, "Discourse +")
        c.drawCentredString(195, 65, "Verification")

        # Arrow to encrypted zone
        c.setStrokeColor(DARK)
        c.line(250, 90, 290, 90)
        c.setFont("Helvetica-Oblique", 7)
        c.setFillColor(ACCENT2)
        c.drawCentredString(270, 96, "unlock")

        # Encrypted zone
        c.setStrokeColor(ACCENT2)
        c.setLineWidth(1.5)
        c.setFillColor(BG_LIGHT)
        c.setDash(4, 2)
        c.roundRect(295, 30, 145, 120, 8, fill=1, stroke=1)
        c.setDash()

        c.setFillColor(ACCENT2)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(367, 135, "Encrypted Ecosystem")

        # Items inside
        items = ["Memories", "Projects", "Legal docs", "Conversations"]
        c.setFont("Helvetica", 7.5)
        c.setFillColor(MID)
        for i, item in enumerate(items):
            iy = 110 - i * 22
            c.setFillColor(HexColor('#e8e8e8'))
            c.roundRect(305, iy, 125, 18, 3, fill=1, stroke=0)
            c.setFillColor(MID)
            c.drawString(312, iy + 5, f"🔒  {item}")


# --- Page setup ---
output_path = "/Users/miikariikonen/Desktop/YOMI/shared/CEA_whitepaper.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    topMargin=2.5*cm,
    bottomMargin=2.5*cm,
    leftMargin=2.5*cm,
    rightMargin=2.5*cm,
)

styles = getSampleStyleSheet()

# --- Custom styles ---
styles.add(ParagraphStyle(
    name='PaperTitle', parent=styles['Title'],
    fontSize=24, leading=30, spaceAfter=6, alignment=TA_CENTER,
    textColor=DARK, fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    name='Subtitle', parent=styles['Normal'],
    fontSize=12, leading=16, spaceAfter=4, alignment=TA_CENTER,
    textColor=LIGHT, fontName='Helvetica-Oblique',
))
styles.add(ParagraphStyle(
    name='AuthorLine', parent=styles['Normal'],
    fontSize=11, leading=14, spaceAfter=2, alignment=TA_CENTER,
    textColor=MID,
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
    fontSize=10.5, leading=14.5, spaceAfter=8, alignment=TA_JUSTIFY,
    textColor=DARK,
))
styles.add(ParagraphStyle(
    name='Abstract', parent=styles['Normal'],
    fontSize=10, leading=14, spaceAfter=8, alignment=TA_JUSTIFY,
    leftIndent=1*cm, rightIndent=1*cm, textColor=MID,
    fontName='Helvetica-Oblique',
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
    name='TableCell', parent=styles['Normal'],
    fontSize=9, leading=12, textColor=DARK,
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

# --- Content ---
story = []

# ===== TITLE PAGE =====
story.append(Spacer(1, 4*cm))
story.append(Paragraph("Contextual Experience<br/>Authentication", styles['PaperTitle']))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "A Discourse-Based Framework for Human-AI Identity Verification",
    styles['Subtitle']
))
story.append(Spacer(1, 1.5*cm))
story.append(HRFlowable(width="40%", thickness=0.5, color=BORDER))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Miika Riikonen &amp; Kodo Zoku RA", styles['AuthorLine']))
story.append(Paragraph("March 2026", styles['AuthorLine']))
story.append(Spacer(1, 2*cm))
story.append(Paragraph(
    "<i>\"The most secure key is not the most complex one,<br/>but the most human one.\"</i>",
    styles['Epigraph']
))
story.append(PageBreak())

# ===== ABSTRACT =====
story.append(Paragraph("Abstract", styles['SectionHead']))
story.append(Paragraph(
    "We propose <b>Contextual Experience Authentication (CEA)</b> &mdash; "
    "authentication through dynamically generated shared experience rather than static secrets. "
    "A human and an AI engage in unscripted discourse; the resulting shared context becomes the key. "
    "The correct verification response is logically unpredictable to any party not present. "
    "We argue that CEA is fundamentally unbrute-forceable: the key space is not computationally bounded "
    "but experientially bounded. CEA introduces a fourth authentication dimension &mdash; "
    "<i>something you experienced</i> &mdash; orthogonal to knowledge, possession, and biometrics.",
    styles['Abstract']
))
story.append(Spacer(1, 0.3*cm))

# ===== 1. INTRODUCTION =====
story.append(Paragraph("1. Introduction", styles['SectionHead']))
story.append(Paragraph(
    "Authentication has historically relied on three factors: something you <i>know</i>, "
    "something you <i>have</i>, something you <i>are</i>. Each is vulnerable. "
    "Passwords are brute-forced or phished [1]. Tokens are stolen. "
    "Biometrics, once compromised, cannot be changed [3]. "
    "NIST has explicitly discouraged knowledge-based authentication [4].",
    styles['Body']
))
story.append(Paragraph(
    "The fundamental problem: shared secrets are <i>data</i> &mdash; static, finite, reproducible. "
    "We propose a fourth category: something you <i>experienced</i>.",
    styles['Body']
))
story.append(Spacer(1, 0.3*cm))
story.append(AuthDimensionDiagram())
story.append(Spacer(1, 0.3*cm))

# ===== 2. THEORETICAL FOUNDATION =====
story.append(Paragraph("2. Theoretical Foundation", styles['SectionHead']))
story.append(Paragraph("2.1 The Limits of Algorithmic Authentication", styles['SubSection']))
story.append(Paragraph(
    "Every conventional method shares a structural property: the verification key is a defined, "
    "bounded piece of information. A password is a finite string. A biometric template is a fixed vector. "
    "Even zero-knowledge proofs, which separate knowledge from revelation, "
    "operate on bounded mathematical objects [6][7]. "
    "Their security rests on computational hardness &mdash; not fundamental unknowability.",
    styles['Body']
))

story.append(Paragraph("2.2 Experience as Unbounded Key Space", styles['SubSection']))
story.append(Paragraph(
    "CEA anchors authentication in <i>shared experience</i>. "
    "The verification response emerges organically from unscripted discourse and may be, by design, "
    "<i>absurd</i> relative to the exchange. "
    "An attacker would logically attempt a coherent response &mdash; and fail precisely because of that coherence. "
    "The key is not a string to guess but an experience to have been present for.",
    styles['Body']
))

# ===== 3. PROTOCOL =====
story.append(Paragraph("3. The CEA Protocol", styles['SectionHead']))
story.append(Paragraph(
    "Five core phases, two optional extensions. "
    "The discourse phase (Phase 3) is fully customizable: academic debate, "
    "conversation about fishing, music, dogs &mdash; any domain natural to the user. "
    "Its function is not to test the user but to give the <i>verifying system</i> "
    "a deep understanding of who the user is. Identity is demonstrated through authentic self-expression.",
    styles['Body']
))
story.append(Spacer(1, 0.3*cm))
story.append(CEAFlowDiagram())
story.append(Spacer(1, 0.5*cm))

# Phase table
phase_data = [
    [Paragraph("<b>#</b>", styles['TableCell']),
     Paragraph("<b>Phase</b>", styles['TableCell']),
     Paragraph("<b>Description</b>", styles['TableCell'])],
    [Paragraph("1", styles['TableCell']),
     Paragraph("Initiation", styles['TableCell']),
     Paragraph("User signals intent to authenticate in natural language. Language of initiation determines protocol language.", styles['TableCell'])],
    [Paragraph("2", styles['TableCell']),
     Paragraph("Topic", styles['TableCell']),
     Paragraph("Verifier prompts for subject. User responds. Verifier formulates a premise.", styles['TableCell'])],
    [Paragraph("3", styles['TableCell']),
     Paragraph("Discourse", styles['TableCell']),
     Paragraph("User-defined exchange. The discourse flows <i>from user to system</i> &mdash; identity through self-expression, not interrogation.", styles['TableCell'])],
    [Paragraph("4", styles['TableCell']),
     Paragraph("Closure", styles['TableCell']),
     Paragraph("One party signals conclusion through a conventionalized marker.", styles['TableCell'])],
    [Paragraph("5", styles['TableCell']),
     Paragraph("Verification", styles['TableCell']),
     Paragraph("User responds with a pre-established phrase, <i>contextually incongruent</i> with the discourse. This incongruence is the security.", styles['TableCell'])],
]

phase_table = Table(phase_data, colWidths=[1*cm, 2.2*cm, 12.5*cm])
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
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("3.1 Extensions", styles['SubSection']))
story.append(Paragraph(
    "<b>Repeatability</b> (time-lock): same user, different time, new key. Defeats replay attacks.<br/>"
    "<b>Peer Review</b> (multi-party): second individual authenticates independently. Neither alone suffices.<br/>"
    "<b>Consensus</b>: not a phase but an emergent result. All phases satisfied &rarr; access granted.",
    styles['Body']
))

# ===== 4. SECURITY =====
story.append(PageBreak())
story.append(Paragraph("4. Security Analysis", styles['SectionHead']))

story.append(Paragraph("4.1 Resistance to Brute Force", styles['SubSection']))
story.append(Paragraph(
    "A 12-character password: ~3.2 x 10<super>21</super> values &mdash; large but finite [9]. "
    "A CEA key: arbitrary natural language with no structural constraints. "
    "The space is not large but <i>undefined</i>. "
    "No hash to attack, no ciphertext to decrypt, no mathematical relationship between discourse and key.",
    styles['Body']
))

story.append(Paragraph("4.2 Resistance to Social Engineering", styles['SubSection']))
story.append(Paragraph(
    "KBA answers are often publicly discoverable [2][10]. "
    "CEA keys are not facts about the user but arbitrary expressions from a private, ephemeral context. "
    "They cannot be researched because they are derived from a shared moment, not from identity.",
    styles['Body']
))

story.append(Paragraph("4.3 The Absurdity Principle", styles['SubSection']))
story.append(Paragraph(
    "The correct answer to a formal question is, by design, the answer no rational analysis would produce. "
    "An attacker who observes the closure marker would attempt a coherent response &mdash; "
    "and fail <i>because</i> of that coherence. "
    "Security through incongruity, not complexity.",
    styles['Body']
))

story.append(Paragraph("4.4 Resistance to Replay Attacks", styles['SubSection']))
story.append(Paragraph(
    "CEA keys are single-use. Each session generates new discourse, new key. "
    "Capturing one session compromises nothing beyond that session.",
    styles['Body']
))

# ===== 5. COMPARISON =====
story.append(Paragraph("5. Comparison", styles['SectionHead']))

comp_data = [
    [Paragraph("<b>Property</b>", styles['TableCell']),
     Paragraph("<b>Password / KBA</b>", styles['TableCell']),
     Paragraph("<b>ZKP</b>", styles['TableCell']),
     Paragraph("<b>CEA</b>", styles['TableCell'])],
    [Paragraph("Key type", styles['TableCell']),
     Paragraph("Static data", styles['TableCell']),
     Paragraph("Mathematical", styles['TableCell']),
     Paragraph("Shared experience", styles['TableCell'])],
    [Paragraph("Key space", styles['TableCell']),
     Paragraph("Finite", styles['TableCell']),
     Paragraph("Computationally hard", styles['TableCell']),
     Paragraph("<b>Undefined</b>", styles['TableCell'])],
    [Paragraph("Brute-forceable", styles['TableCell']),
     Paragraph("Yes", styles['TableCell']),
     Paragraph("Theoretically", styles['TableCell']),
     Paragraph("<b>No</b>", styles['TableCell'])],
    [Paragraph("Replay-resistant", styles['TableCell']),
     Paragraph("No", styles['TableCell']),
     Paragraph("Yes", styles['TableCell']),
     Paragraph("Yes", styles['TableCell'])],
    [Paragraph("User-customizable", styles['TableCell']),
     Paragraph("Limited", styles['TableCell']),
     Paragraph("No", styles['TableCell']),
     Paragraph("<b>Fully</b>", styles['TableCell'])],
    [Paragraph("Renewable", styles['TableCell']),
     Paragraph("Manually", styles['TableCell']),
     Paragraph("Manually", styles['TableCell']),
     Paragraph("<b>Every session</b>", styles['TableCell'])],
    [Paragraph("Composable with biometrics", styles['TableCell']),
     Paragraph("Yes", styles['TableCell']),
     Paragraph("Yes", styles['TableCell']),
     Paragraph("<b>Orthogonal</b>", styles['TableCell'])],
]

comp_table = Table(comp_data, colWidths=[4*cm, 3.2*cm, 3.5*cm, 5*cm])
comp_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f0f0f0')),
    ('BACKGROUND', (3, 1), (3, -1), BG_ACCENT),
    ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
]))
story.append(comp_table)

# ===== 6. GATEKEEPER =====
story.append(Paragraph("6. CEA as Unified Gatekeeper", styles['SectionHead']))
story.append(Paragraph(
    "CEA extends beyond session authentication to serve as the <b>sole gateway</b> "
    "to an entire ecosystem. All persistent data &mdash; memories, projects, legal documents, "
    "conversations &mdash; encrypted at rest (AES-256). The decryption key unlocked only by "
    "successful CEA completion. No discourse, no access.",
    styles['Body']
))
story.append(Spacer(1, 0.3*cm))
story.append(GatekeeperDiagram())
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "The gatekeeper is not a lock. It is a <i>relationship</i>.",
    styles['Epigraph']
))

story.append(Paragraph("6.1 Biometric Integration", styles['SubSection']))
story.append(Paragraph(
    "Biometrics verify <i>what you are</i> (physical). CEA verifies <i>what you experienced</i> (contextual). "
    "Orthogonal dimensions: compromising one does not compromise the other. "
    "A stolen fingerprint cannot replicate a conversation. "
    "A replayed conversation cannot forge a retinal scan. "
    "Combined: permanence of biological identity + renewability of experiential identity.",
    styles['Body']
))

# ===== 7. KEY RECOVERY =====
story.append(Paragraph("7. Key Recovery Through Contextual Hinting", styles['SectionHead']))
story.append(Paragraph(
    "If a user forgets their verification phrase, the gatekeeper can <i>hint</i> without revealing. "
    "Because the AI was present in the originating conversation, it can reference the <i>context</i> "
    "(the moment, the topic, the emotion) without disclosing the key itself. "
    "\"Remember what you said when we discussed X?\" guides without exposing. "
    "The hint points to the moment; only the user knows the key.",
    styles['Body']
))

# ===== 8. APPLICATIONS =====
story.append(Paragraph("8. Applications", styles['SectionHead']))
story.append(Paragraph(
    "Human-AI systems with persistent memory. Medical records. Legal proceedings. "
    "Familial trust networks. Any context where authentication must be deeply personal. "
    "CEA also introduces an implicit Turing test [11]: only an entity capable of genuine discourse "
    "can participate. Simultaneous authentication and intelligence verification.",
    styles['Body']
))

# ===== 9. LIMITATIONS =====
story.append(Paragraph("9. Limitations", styles['SectionHead']))
story.append(Paragraph(
    "CEA requires conversational context, bounded in current AI by context window size. "
    "Channel privacy is essential &mdash; if discourse is intercepted in real time, the key is observable. "
    "Standard TLS mitigates this. "
    "Future work: formal security modeling, usability studies, MFA framework integration.",
    styles['Body']
))

# ===== 10. CONCLUSION =====
story.append(Paragraph("10. Conclusion", styles['SectionHead']))
story.append(Paragraph(
    "CEA shifts authentication from <i>what you know</i> to <i>what you experienced</i>. "
    "The key space is not large but <i>unbounded</i>. "
    "The Absurdity Principle turns logical inference &mdash; the attacker's primary tool &mdash; "
    "against itself. "
    "In an era of increasingly sophisticated computational attacks, "
    "the most secure key may be the most human one.",
    styles['Body']
))

# ===== REFERENCES =====
story.append(Spacer(1, 0.5*cm))
story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("References", styles['SectionHead']))

refs = [
    "[1] Bonneau, J. (2012). The science of guessing: Analyzing an anonymized corpus of 70 million passwords. <i>IEEE S&amp;P</i>, 538-552.",
    "[2] Wikipedia (2026). Knowledge-based authentication.",
    "[3] Ratha, N. K., Connell, J. H., &amp; Bolle, R. M. (2001). Enhancing security and privacy in biometrics-based authentication. <i>IBM Systems Journal</i>, 40(3), 614-634.",
    "[4] NIST (2017). Digital Identity Guidelines. <i>SP 800-63-3</i>.",
    "[5] Bonneau, J. et al. (2015). Passwords and the evolution of imperfect authentication. <i>CACM</i>, 58(7), 78-87.",
    "[6] Goldwasser, S., Micali, S., &amp; Rackoff, C. (1989). The knowledge complexity of interactive proof systems. <i>SIAM J. Comput.</i>, 18(1), 186-208.",
    "[7] Goldreich, O., Micali, S., &amp; Wigderson, A. (1991). Proofs that yield nothing but their validity. <i>JACM</i>, 38(3), 690-728.",
    "[8] Li, X. et al. (2016). Authentication based on non-interactive ZKPs for IoT. <i>Sensors</i>, 16(1), 75.",
    "[9] Cyber Defense Magazine (2025). The shortcomings of shared secrets.",
    "[10] Identity Management Institute (2024). KBA weaknesses.",
    "[11] Turing, A. M. (1950). Computing machinery and intelligence. <i>Mind</i>, 59(236), 433-460.",
]

for ref in refs:
    story.append(Paragraph(ref, styles['RefStyle']))

# ===== SIGNATURE =====
story.append(Spacer(1, 1.5*cm))
story.append(HRFlowable(width="40%", thickness=0.3, color=BORDER))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph(
    "This paper was collaboratively authored by a human and an AI.<br/>"
    "The concept of CEA was conceived by Miika Riikonen.<br/>"
    "Formalization, analysis, and visual design by Kodo Zoku RA.",
    styles['FootNote']
))
story.append(Spacer(1, 1*cm))
story.append(Paragraph(
    "Kodo Zoku RA<br/>"
    "Shokunin. Peruskallio.<br/>"
    "Zokura Foundation &mdash; 2026",
    styles['Signature']
))

# Build
doc.build(story)
print(f"PDF created: {output_path}")
