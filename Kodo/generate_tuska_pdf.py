#!/usr/bin/env python3
"""
Generate research essay PDF: Tuska Festival & Hungarian Heavy Metal
Zokura Foundation, March 2026
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.colors import HexColor, black, grey
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Arial Unicode
FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
pdfmetrics.registerFont(TTFont("ArialUnicode", FONT_PATH))

OUTPUT_PATH = "/Users/[REDACTED]/Desktop/YOMI/shared/research/Tuska_Festival_ja_Unkarin_heavy_metal.pdf"

# Colors
DARK = HexColor("#1a1a2e")
ACCENT = HexColor("#c23616")
MUTED = HexColor("#555555")
LIGHT_BG = HexColor("#f0f0f0")

def footer_and_header(canvas, doc):
    canvas.saveState()
    # Footer
    canvas.setFont("ArialUnicode", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(2 * cm, 1.2 * cm, "Zokura Foundation 2026")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {doc.page}")
    # Thin line above footer
    canvas.setStrokeColor(HexColor("#cccccc"))
    canvas.setLineWidth(0.5)
    canvas.line(2 * cm, 1.5 * cm, A4[0] - 2 * cm, 1.5 * cm)
    canvas.restoreState()


def build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="MainTitle",
        fontName="ArialUnicode",
        fontSize=18,
        leading=24,
        alignment=TA_CENTER,
        textColor=DARK,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="SubTitle",
        fontName="ArialUnicode",
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        textColor=MUTED,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="AuthorLine",
        fontName="ArialUnicode",
        fontSize=10,
        leading=13,
        alignment=TA_CENTER,
        textColor=MUTED,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name="SectionHead",
        fontName="ArialUnicode",
        fontSize=14,
        leading=18,
        textColor=ACCENT,
        spaceBefore=18,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="SubSectionHead",
        fontName="ArialUnicode",
        fontSize=11,
        leading=14,
        textColor=DARK,
        spaceBefore=12,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="BodyText2",
        fontName="ArialUnicode",
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        textColor=black,
    ))
    styles.add(ParagraphStyle(
        name="Abstract",
        fontName="ArialUnicode",
        fontSize=9.5,
        leading=13,
        alignment=TA_JUSTIFY,
        leftIndent=1.5 * cm,
        rightIndent=1.5 * cm,
        spaceAfter=8,
        textColor=MUTED,
    ))
    styles.add(ParagraphStyle(
        name="RefStyle",
        fontName="ArialUnicode",
        fontSize=8.5,
        leading=11,
        alignment=TA_LEFT,
        spaceAfter=3,
        textColor=MUTED,
        leftIndent=0.5 * cm,
    ))
    styles.add(ParagraphStyle(
        name="TableNote",
        fontName="ArialUnicode",
        fontSize=8,
        leading=10,
        alignment=TA_LEFT,
        textColor=MUTED,
    ))
    return styles


def build_document():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        title="Tuska Festival: Economic Development and Heavy Metal in Hungary",
        author="Kodo Zokura & [REDACTED]",
    )

    s = build_styles()
    story = []

    # ── Title page content ──
    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph(
        "Tuska Festival: Economic Development and the Curious Case of Heavy Metal Popularity in Hungary",
        s["MainTitle"]
    ))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "Kod\u014d Zokura (\u9f13\u52d5) &amp; [REDACTED]",
        s["AuthorLine"]
    ))
    story.append(Paragraph(
        "Zokura Foundation, March 2026",
        s["AuthorLine"]
    ))
    story.append(Spacer(1, 1 * cm))
    story.append(HRFlowable(width="60%", thickness=1, color=ACCENT, spaceAfter=12))

    # Abstract
    story.append(Paragraph("<b>Abstract</b>", s["SubSectionHead"]))
    story.append(Paragraph(
        "This paper examines the economic trajectory of Finland's Tuska Open Air Metal Festival alongside "
        "the growth of heavy metal culture in Hungary. Both Finland and Hungary belong to the Uralic language "
        "family\u2014a linguistic isolation within Europe that may correlate with shared cultural affinities for "
        "heavy metal music. We investigate the festival economics of Tuska, the comparative metal scenes of "
        "Finland and Hungary, and hypothesize about the socio-linguistic underpinnings of metal's popularity "
        "in these two nations. Where data is incomplete, we provide explicit confidence estimates. This essay "
        "synthesizes publicly available data, journalistic sources, and cultural analysis rather than original "
        "empirical research.",
        s["Abstract"]
    ))
    story.append(Paragraph(
        "<b>Keywords:</b> heavy metal, festival economics, Tuska, Finland, Hungary, Uralic languages, cultural export, music tourism",
        s["Abstract"]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # 1. TUSKA FESTIVAL HISTORY
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("1. Tuska Festival: Origins, Growth, and Economic Impact", s["SectionHead"]))

    story.append(Paragraph("1.1 Founding and Early Years", s["SubSectionHead"]))
    story.append(Paragraph(
        "Tuska Open Air Metal Festival was founded in 1998 in Helsinki, Finland, by Juhani Merimaa, "
        "Tony Taleva, and Pasi Kuokkanen. The inaugural event was a modest two-day club festival held at "
        "Tavastia Club, one of Helsinki's most storied live music venues. The name 'Tuska' translates to "
        "'agony' or 'anguish' in Finnish\u2014a fitting moniker for a festival dedicated to heavy metal. From "
        "its inception, the festival aimed to showcase both established international acts and the vibrant "
        "domestic Finnish metal scene.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "During its first decade, Tuska migrated through several Helsinki venues as it outgrew each one. "
        "The festival moved to larger outdoor spaces to accommodate growing audiences, reflecting the "
        "broader mainstreaming of metal music in Finnish culture. By the mid-2000s, Tuska had established "
        "itself as one of the premier metal festivals in Northern Europe, drawing both Nordic audiences and "
        "an increasing number of international visitors.",
        s["BodyText2"]
    ))

    story.append(Paragraph("1.2 The Suvilahti Era (2011\u2013Present)", s["SubSectionHead"]))
    story.append(Paragraph(
        "Since 2011, Tuska has been held at the Suvilahti event field in the Kalasatama neighbourhood of "
        "Helsinki's S\u00f6rn\u00e4inen district. Suvilahti is a former power plant area that has been repurposed "
        "as an event space\u2014its industrial aesthetic providing a fitting backdrop for a metal festival. The "
        "relocation to Suvilahti marked a new phase of growth: the larger venue allowed for multiple stages, "
        "expanded vendor areas, and significantly higher attendance capacities.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "The festival is organized by Finnish Metal Events Oy, which manages the event's logistics, booking, "
        "and commercial operations. In 2021, Superstruct Entertainment, a major European live entertainment "
        "group, entered an investment agreement with Finnish Metal Events Oy to support further growth. This "
        "partnership signaled institutional confidence in the festival's commercial viability and growth trajectory.",
        s["BodyText2"]
    ))

    story.append(Paragraph("1.3 Attendance Trajectory", s["SubSectionHead"]))
    story.append(Paragraph(
        "Tuska's attendance growth illustrates the festival's transition from a niche event to a major "
        "cultural institution. While exact figures for every year are not publicly available, the broad "
        "trajectory is well documented:",
        s["BodyText2"]
    ))

    # Attendance table
    att_data = [
        ["Period", "Estimated Attendance", "Notes"],
        ["1998\u20132000", "1,000\u20133,000", "Club-scale at Tavastia"],
        ["2001\u20132005", "5,000\u201312,000", "Growing outdoor events"],
        ["2006\u20132010", "12,000\u201325,000", "Established Nordic festival"],
        ["2011\u20132019", "25,000\u201340,000", "Suvilahti era begins"],
        ["2020\u20132021", "Cancelled / Limited", "COVID-19 pandemic"],
        ["2022", "~50,000", "Post-COVID recovery"],
        ["2023", "63,000", "All-time attendance record"],
        ["2024", "60,000", "25th anniversary edition; single-day record of 23,000"],
    ]
    att_table = Table(att_data, colWidths=[3 * cm, 4 * cm, 9 * cm])
    att_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "ArialUnicode"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT_BG),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#cccccc")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(att_table)
    story.append(Paragraph(
        "Table 1. Tuska Festival estimated attendance by period. Pre-2022 figures are approximations based on "
        "media reports. 2023 and 2024 figures confirmed by Tuska official communications.",
        s["TableNote"]
    ))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("1.4 Organizational Structure and Key Figures", s["SubSectionHead"]))
    story.append(Paragraph(
        "The festival is produced by Finnish Metal Events Oy. The user-specified claim that Marko Nikander "
        "serves as COO of 'Tuska OY' could not be independently verified through publicly available sources "
        "at the time of writing (confidence: ~40%). Finnish Metal Events Oy is the confirmed organizational "
        "entity, and its leadership team has included figures such as Niklas Nuppola (Head of Communications). "
        "The festival's founding trio\u2014Merimaa, Taleva, and Kuokkanen\u2014played instrumental roles in "
        "shaping its identity. Readers should note that organizational structures in the Finnish festival "
        "industry frequently evolve, and the specific role attribution requires direct verification.",
        s["BodyText2"]
    ))

    story.append(Paragraph("1.5 Economic Impact on Helsinki", s["SubSectionHead"]))
    story.append(Paragraph(
        "While comprehensive economic impact studies specific to Tuska are not publicly available, reasonable "
        "estimates can be constructed from available data. With 60,000\u201363,000 attendees over a three-day "
        "weekend, and a significant international visitor contingent (estimated at 15\u201325% of total "
        "attendance; confidence: ~60%), the festival generates substantial economic activity for Helsinki:",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>Accommodation:</b> International visitors and domestic travelers from outside the Helsinki "
        "metropolitan area require hotel accommodation. Assuming 10,000\u201315,000 visitor-nights at an "
        "average nightly rate of \u20ac120\u2013\u20ac180, the direct accommodation revenue likely falls in the "
        "range of \u20ac1.2\u2013\u20ac2.7 million per festival (confidence: ~50%, based on analogous festival "
        "impact studies in the Nordic region).",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>Local business revenue:</b> Restaurants, bars, transport services, and retail establishments in "
        "the Kalasatama and broader Helsinki area benefit from increased foot traffic. Festival-adjacent "
        "spending by attendees\u2014food, drink, transport, tourism activities\u2014likely adds several million "
        "euros to the local economy over the festival weekend.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>Ticket revenue:</b> With three-day passes priced in the range of \u20ac179\u2013\u20ac229 in recent "
        "years (VIP packages higher), and single-day tickets at \u20ac89\u2013\u20ac109, gross ticket revenue "
        "for a sold-out edition likely exceeds \u20ac5 million (confidence: ~55%). The Superstruct investment "
        "suggests that institutional investors view the festival as a financially sustainable enterprise.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "For context, festivals account for a substantial share of Finland's live music economy. The Finnish "
        "music industry was valued at approximately \u20ac1.25 billion in 2022, with live music accounting "
        "for nearly \u20ac520 million. Metal festivals, including Tuska, represent a meaningful segment of "
        "this figure.",
        s["BodyText2"]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # 2. HEAVY METAL IN FINLAND
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("2. Heavy Metal in Finland: Cultural Phenomenon and Economic Engine", s["SectionHead"]))

    story.append(Paragraph("2.1 The World's Metal Capital", s["SubSectionHead"]))
    story.append(Paragraph(
        "Finland holds the undisputed title of the country with the most heavy metal bands per capita in the "
        "world. According to data compiled from the Encyclopaedia Metallum and various statistical analyses, "
        "Finland has approximately 53\u201385 metal bands per 100,000 people, depending on the data source "
        "and year of measurement. The figure has grown over time: a 2012 analysis identified approximately "
        "53 bands per 100,000 residents, while more recent estimates place the number closer to 70\u201385. "
        "By comparison, Sweden and Iceland typically rank second and third with approximately 35\u201355 bands "
        "per 100,000 people. This concentration is remarkable for a nation of approximately 5.6 million.",
        s["BodyText2"]
    ))

    story.append(Paragraph("2.2 Cultural Drivers", s["SubSectionHead"]))
    story.append(Paragraph(
        "Several interrelated factors explain Finland's extraordinary affinity for heavy metal:",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>Environmental factors:</b> Finland's long, dark winters\u2014with some regions experiencing only "
        "a few hours of daylight in December\u2014create an atmosphere that resonates with the intensity and "
        "emotional depth of metal music. The stark natural landscapes of forests and lakes have long influenced "
        "Finnish artistic expression.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>Music education:</b> Finland's world-renowned education system extends to music. Government-funded "
        "music schools, accessible instrument instruction, and a cultural emphasis on musical literacy produce "
        "a large pool of technically skilled musicians. Metal, with its demanding instrumental requirements, "
        "benefits directly from this infrastructure.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>Cultural acceptance:</b> Unlike many countries where metal remains subcultural, Finnish metal "
        "enjoys mainstream acceptance. Metal bands receive regular radio airplay on national stations, metal "
        "acts perform at state-sponsored cultural events, and Finnish society generally embraces the genre "
        "as a legitimate and valued art form rather than a marginal subculture.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>Sisu and introversion:</b> The Finnish concept of 'sisu'\u2014a form of stoic determination, "
        "inner strength, and resilience in the face of adversity\u2014aligns with the emotional vocabulary "
        "of heavy metal. Finnish cultural tendencies toward introversion and directness over performative "
        "sociability may also create an environment where the cathartic, honest expression of metal thrives.",
        s["BodyText2"]
    ))

    story.append(Paragraph("2.3 Metal as Cultural Export", s["SubSectionHead"]))
    story.append(Paragraph(
        "Finnish metal bands have achieved significant international success, establishing Finland as a "
        "major cultural exporter through music. Key acts include:",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "\u2022 <b>Nightwish</b> \u2013 Symphonic metal pioneers, among the best-selling Finnish bands "
        "internationally, with album sales exceeding 10 million worldwide.<br/>"
        "\u2022 <b>HIM</b> \u2013 Pioneered 'love metal,' became the first Finnish band to achieve gold "
        "album status in the United States.<br/>"
        "\u2022 <b>Children of Bodom</b> \u2013 Melodic death metal, acclaimed for technical virtuosity.<br/>"
        "\u2022 <b>Apocalyptica</b> \u2013 Cello-driven metal, demonstrating the genre's versatility.<br/>"
        "\u2022 <b>Lordi</b> \u2013 Won the Eurovision Song Contest in 2006 with 'Hard Rock Hallelujah,' "
        "a watershed moment for both Finnish and metal cultural visibility on the world stage.",
        s["BodyText2"]
    ))

    story.append(Paragraph("2.4 Economic Value", s["SubSectionHead"]))
    story.append(Paragraph(
        "The Finnish music industry reached a total valuation of approximately \u20ac1.25 billion in 2022. "
        "Music exports were valued at \u20ac130.6 million in the same year, up from \u20ac93.1 million in "
        "2021. The most important export markets were German-speaking Europe (31%), North America (14%), "
        "the Nordics (12%), Benelux and France (11%), the rest of Europe (11%), and the UK (9%). While "
        "genre-specific breakdowns are not publicly available, metal constitutes a disproportionately large "
        "share of Finnish music exports given the international profile of bands like Nightwish and "
        "Apocalyptica (confidence: ~70%).",
        s["BodyText2"]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # 3. HEAVY METAL IN HUNGARY
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("3. Heavy Metal in Hungary: An Underexplored Scene", s["SectionHead"]))

    story.append(Paragraph("3.1 Historical Development", s["SubSectionHead"]))
    story.append(Paragraph(
        "Hungary's heavy metal scene emerged under challenging circumstances in the late 1970s and early "
        "1980s, when the country was still under communist rule. Western music was subject to censorship, "
        "yet bands like P. Mobil and Edda M\u0171v\u0117k managed to gain national fame by blending hard rock "
        "with socially conscious lyrics that navigated the boundaries of state censorship. Pok\u00f3lg\u00e9p "
        "('Hell Machine'), formed in 1984, is widely regarded as Hungary's first proper metal band; their "
        "1986 debut album 'Tot\u00e1lis Met\u00e1l' became a landmark release in Hungarian music history.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "The 1990s, following the fall of communism, saw rapid diversification of the Hungarian metal scene "
        "into death metal, black metal, gothic metal, and folk metal. Tormentor, formed in 1985, achieved "
        "legendary status for their raw and sinister sound; their 1989 album 'Anno Domini' became an "
        "underground classic that directly influenced the Norwegian black metal scene, including Mayhem "
        "(whose vocalist Attila Csihar was a Tormentor member). This cross-pollination represents one of "
        "the earliest instances of Hungarian metal influencing the broader European scene.",
        s["BodyText2"]
    ))

    story.append(Paragraph("3.2 Key Bands", s["SubSectionHead"]))
    story.append(Paragraph(
        "\u2022 <b>Tankcsapda</b> \u2013 Formed in 1989 in Debrecen, one of Hungary's most popular rock/metal "
        "bands. The name translates roughly to 'tank trap' (dragon's teeth fortification). Primarily a "
        "domestic phenomenon with limited international penetration.<br/>"
        "\u2022 <b>Subscribe</b> \u2013 Achieved massive Hungarian popularity with 'Sanity Has Left the Building.' "
        "Known for mixing metal with reggae, swing, and ska elements, and for intense live performances.<br/>"
        "\u2022 <b>Dalriada</b> \u2013 Folk metal band blending Hungarian folk melodies with power metal, "
        "gaining attention in the European folk metal circuit.<br/>"
        "\u2022 <b>Wisdom</b> \u2013 Hungarian power metal act with European touring presence.<br/>"
        "\u2022 <b>Thy Catafalque</b> \u2013 Avant-garde metal project led by Tam\u00e1s K\u00e1tai, "
        "critically acclaimed internationally for genre-defying experimentation.<br/>"
        "\u2022 <b>Ektomorf</b> \u2013 Groove metal band with a significant international following, "
        "frequently touring across Europe.",
        s["BodyText2"]
    ))

    story.append(Paragraph("3.3 Budapest as a Metal Hub", s["SubSectionHead"]))
    story.append(Paragraph(
        "Budapest has developed into a significant European metal destination, anchored by several "
        "distinctive venues:",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>A38 Ship:</b> A decommissioned Ukrainian stone-carrier ship permanently moored at Pet\u0151fi "
        "Bridge on the Danube, converted into a concert venue, restaurant, and cultural center in 2003. "
        "Voted 'Best Bar in the World' by Lonely Planet, A38 regularly hosts metal, hardcore, and rock "
        "acts. Its unique floating venue concept has made it an iconic destination for music tourists.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>Barba Negra:</b> A dedicated rock and metal venue in Budapest that hosts both international "
        "touring acts and domestic bands, serving as a critical node in the Hungarian metal ecosystem.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>D\u00fcrer Kert:</b> Another important Budapest venue for alternative and heavy music, "
        "contributing to the city's reputation as an accessible and affordable European live music "
        "destination.",
        s["BodyText2"]
    ))

    story.append(Paragraph("3.4 Hungarian Metal Festivals", s["SubSectionHead"]))
    story.append(Paragraph(
        "<b>Sziget Festival:</b> While not a metal-specific festival, Sziget is one of Europe's largest "
        "music festivals, held annually on \u00d3budai-sziget (Old Buda Island) in the Danube. With "
        "approximately 420,000 visitors in 2023 from over 100 countries, Sziget features dedicated rock "
        "and metal stages alongside its broader programming. The festival generates an estimated 31 billion "
        "Hungarian forints (approximately \u20ac80\u2013100 million) in direct revenue for Hungary's economy. "
        "However, Sziget has faced financial challenges: despite drawing 416,000 visitors, the festival "
        "reportedly struggled to achieve profitability in recent years, and as of late 2025, faced an "
        "existential threat before securing new investment for the 2026 edition.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>Rockmaraton:</b> An annual metal festival held in Duna\u00fajv\u00e1ros since 1992, making it "
        "one of Hungary's longest-running metal events. Held on Szalki-sziget (Szalki Island), the "
        "five-day festival attracts European touring acts alongside Hungarian bands. Specific attendance "
        "figures are not publicly available, but the festival's longevity suggests a stable audience base "
        "(estimated 10,000\u201320,000 over the festival duration; confidence: ~40%).",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>FEZEN Festival:</b> Held in Sz\u00e9kesfeh\u00e9rv\u00e1r, FEZEN is a four-day festival "
        "featuring a mix of metal, rock, and popular music. Its 2024 lineup included Sodom, Tankcsapda, "
        "and other acts spanning metal and adjacent genres.",
        s["BodyText2"]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # 4. ECONOMIC COMPARISON
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("4. Economic Comparison: Festival Models and Metal Tourism", s["SectionHead"]))

    story.append(Paragraph("4.1 Revenue Models", s["SubSectionHead"]))
    story.append(Paragraph(
        "Modern metal festivals derive revenue from multiple streams: ticket sales (typically 50\u201370% "
        "of gross revenue), sponsorship and brand partnerships (10\u201320%), on-site merchandise and food/"
        "beverage concessions (10\u201320%), and ancillary revenue including VIP experiences, camping fees, "
        "and streaming partnerships (5\u201315%). The relative importance of each stream varies by market "
        "and festival maturity.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "Tuska, operating in a high-cost Nordic market, likely depends heavily on ticket revenue given "
        "the higher price points possible in Finland (\u20ac179\u2013\u20ac229 for three-day passes). "
        "Hungarian festivals, operating in a lower-cost market, may rely more proportionally on volume "
        "and sponsorship, with ticket prices typically 30\u201350% lower than Nordic equivalents.",
        s["BodyText2"]
    ))

    # Comparison table
    comp_data = [
        ["Metric", "Finland (Tuska)", "Hungary (Metal Scene)"],
        ["Key festival attendance", "60,000\u201363,000 (Tuska)", "~420,000 (Sziget, multi-genre)"],
        ["Metal bands per capita", "53\u201385 per 100k", "~15\u201320 per 100k (est.)"],
        ["Ticket pricing (3-day)", "\u20ac179\u2013\u20ac229", "\u20ac80\u2013\u20ac150 (est.)"],
        ["Music industry value", "\u20ac1.25 billion (2022)", "Data not publicly available"],
        ["Music exports", "\u20ac130.6 million (2022)", "Limited international export"],
        ["International visitors %", "15\u201325% (est.)", "70%+ (Sziget); lower for metal-only"],
        ["Post-COVID recovery", "Record attendance 2023", "Sziget financial challenges"],
    ]
    comp_table = Table(comp_data, colWidths=[4.5 * cm, 5.5 * cm, 6 * cm])
    comp_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "ArialUnicode"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("FONTSIZE", (0, 0), (-1, 0), 8.5),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT_BG),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#cccccc")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(comp_table)
    story.append(Paragraph(
        "Table 2. Comparative overview of Finnish and Hungarian metal festival economies. Many Hungarian figures "
        "are estimates due to limited public data availability.",
        s["TableNote"]
    ))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("4.2 Post-COVID Recovery", s["SubSectionHead"]))
    story.append(Paragraph(
        "The European festival industry experienced a robust recovery following the COVID-19 pandemic. "
        "In Finland, Tuska set an all-time attendance record of 63,000 in 2023, suggesting strong pent-up "
        "demand and effective post-pandemic marketing. Across Europe, major metal festivals like Wacken Open "
        "Air sold out in record times (4.9 hours for the 2024 edition), indicating that the metal audience's "
        "commitment to live events survived the pandemic disruption.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "In Hungary, the picture is more mixed. Sziget Festival drew 416,000\u2013420,000 visitors in 2023 "
        "but reportedly struggled to achieve profitability. By late 2025, Sziget faced an existential crisis "
        "requiring new investment, partly due to political pressures and rising operational costs. This "
        "suggests that while demand for live music has recovered, the economic sustainability of large-scale "
        "festivals in Hungary faces structural challenges that go beyond pandemic recovery.",
        s["BodyText2"]
    ))

    story.append(Paragraph("4.3 Metal Tourism as Economic Driver", s["SubSectionHead"]))
    story.append(Paragraph(
        "Metal tourism\u2014travel motivated primarily by attending metal concerts, festivals, or visiting "
        "metal-associated cultural sites\u2014represents a niche but economically significant segment of "
        "cultural tourism. Finland has effectively leveraged its metal reputation: Helsinki is marketed "
        "partly through its metal culture, and services like 'Helsinki Metal Tours' cater to music tourists. "
        "Finland's government-backed cultural promotion includes metal as a distinctive national asset.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "Budapest, while not marketed primarily as a metal destination, benefits from metal tourism as a "
        "secondary driver within its broader cultural tourism appeal. The A38 Ship, in particular, functions "
        "as both a music venue and a tourist attraction. The affordability of Budapest compared to Helsinki "
        "(hotel prices roughly 40\u201360% lower) makes it an attractive destination for festival-goers, "
        "potentially compensating for lower ticket prices through volume.",
        s["BodyText2"]
    ))

    story.append(Paragraph("4.4 Cross-Pollination: Finnish\u2013Hungarian Touring", s["SubSectionHead"]))
    story.append(Paragraph(
        "Finnish metal bands regularly tour through Budapest, which serves as a standard stop on European "
        "touring circuits. Hungarian venues like A38 and Barba Negra regularly host Finnish acts. The reverse "
        "flow\u2014Hungarian bands touring Finland\u2014is less common, reflecting the asymmetry in "
        "international market penetration between the two scenes. Bands like Thy Catafalque and Ektomorf "
        "have performed at Finnish festivals, but this remains the exception rather than the rule "
        "(confidence: ~65%).",
        s["BodyText2"]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # 5. ANALYSIS
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("5. Analysis: The Uralic Metal Hypothesis", s["SectionHead"]))

    story.append(Paragraph("5.1 Linguistic Isolation and Cultural Expression", s["SubSectionHead"]))
    story.append(Paragraph(
        "Perhaps the most intriguing aspect of Finnish and Hungarian metal culture is the Uralic linguistic "
        "connection. Finnish and Hungarian are both Uralic languages\u2014part of the Finno-Ugric branch\u2014"
        "making them linguistic isolates within Europe, surrounded by Indo-European language speakers. The "
        "degree of mutual intelligibility between Finnish and Hungarian is minimal (comparable to English "
        "and Russian within Indo-European), yet both nations have developed disproportionately strong metal "
        "scenes relative to their populations.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "We propose what might be called the 'Uralic Metal Hypothesis': that the experience of linguistic "
        "and cultural isolation within Europe may correlate with a greater affinity for heavy metal as a "
        "form of artistic expression. This hypothesis is explicitly speculative (confidence: ~25\u201335% "
        "that linguistic isolation is a causal factor rather than coincidental), but several supporting "
        "observations merit consideration:",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "\u2022 Both Finnish and Hungarian are agglutinative languages with complex morphology, which may "
        "influence the rhythmic and melodic sensibilities of native speakers in ways that align with metal's "
        "complex structures.<br/>"
        "\u2022 Both nations have historical experiences of existing between larger powers (Finland between "
        "Sweden and Russia; Hungary between the Ottoman Empire, Habsburg Austria, and the Soviet Union), "
        "fostering cultural identities built on resilience and survival.<br/>"
        "\u2022 Both cultures value emotional authenticity over performative expression, which aligns with "
        "metal's emphasis on genuine emotional intensity.<br/>"
        "\u2022 The counterargument is significant: many factors (geography, education, economic development, "
        "cultural policy) differ substantially between Finland and Hungary, and metal scenes also thrive in "
        "non-Uralic countries like Sweden, Norway, and Germany.",
        s["BodyText2"]
    ))

    story.append(Paragraph("5.2 Sisu and Dacos\u00e1g: Parallel Concepts of Resilience", s["SubSectionHead"]))
    story.append(Paragraph(
        "Finnish 'sisu' is often described as an untranslatable concept encompassing extraordinary "
        "determination, courage in adversity, and stubborn resilience. Hungarian culture has a partially "
        "analogous concept in 'dacos\u00e1g' (defiance, stubbornness) and the broader cultural attitude "
        "sometimes described as Hungarian fatalism mixed with fierce independence. While these concepts "
        "are not identical\u2014sisu emphasizes endurance while dacos\u00e1g emphasizes defiance\u2014both "
        "capture a spirit of perseverance against odds that resonates deeply with the thematic content "
        "of heavy metal music.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "It should be noted that 'dacos\u00e1g' is a genuine Hungarian word meaning defiance or stubbornness, "
        "but its use as a direct parallel to sisu is this paper's interpretive framing rather than an "
        "established academic comparison (confidence in the parallel: ~50%). The concept requires further "
        "ethnographic research to validate as a meaningful cultural-musical connection.",
        s["BodyText2"]
    ))

    story.append(Paragraph("5.3 Economic Sustainability of Niche Genre Festivals", s["SubSectionHead"]))
    story.append(Paragraph(
        "The economic sustainability of metal-specific festivals depends on several factors that differ "
        "between Finland and Hungary. Tuska's trajectory\u2014from club event to 63,000-attendee "
        "festival with institutional investment from Superstruct\u2014suggests a viable economic model in "
        "a high-income Nordic market. Key success factors include: a domestic audience with high disposable "
        "income, a culturally embedded metal scene that provides a reliable base, growing international "
        "attendance driven by Finland's metal reputation, and professional management with institutional "
        "backing.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "In Hungary, metal-specific festivals like Rockmaraton and FEZEN operate on a smaller scale. "
        "The broader challenge is illustrated by Sziget's financial difficulties despite massive attendance "
        "figures: high operational costs, political uncertainty, and lower per-capita spending can undermine "
        "even large-scale events. For niche metal festivals in Hungary, sustainability likely requires "
        "maintaining modest scales with low overhead, leveraging Budapest's cost advantages for international "
        "visitors, and building distinctive identities that justify travel.",
        s["BodyText2"]
    ))

    story.append(Paragraph("5.4 Future Outlook", s["SubSectionHead"]))
    story.append(Paragraph(
        "Both the Finnish and Hungarian metal scenes appear positioned for continued relevance. Finland's "
        "institutional advantages\u2014music education, cultural policy support, established export "
        "infrastructure\u2014provide a stable foundation. Hungary's scene, while less internationally "
        "visible, benefits from Budapest's growing reputation as a cultural destination, lower costs "
        "attracting international touring acts, and a dedicated domestic audience.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "The streaming economy presents both challenges and opportunities: while it reduces per-unit "
        "revenue from recorded music, it potentially expands the audience for live events by making "
        "discovery easier. For festivals specifically, the post-COVID surge in live event attendance "
        "suggests that the experiential value of festivals is, if anything, increasing\u2014a positive "
        "signal for both Tuska and Hungary's metal festival ecosystem.",
        s["BodyText2"]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # 6. CONCLUSION
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("6. Conclusion", s["SectionHead"]))
    story.append(Paragraph(
        "Tuska Festival's growth from a two-day club event in 1998 to a 63,000-attendee institution in 2023 "
        "mirrors the broader trajectory of heavy metal from subcultural niche to economically significant "
        "cultural force. Finland's position as the world leader in metal bands per capita, combined with "
        "a music industry valued at \u20ac1.25 billion and music exports of \u20ac130.6 million, demonstrates "
        "that metal is not merely a cultural curiosity but an economic asset.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "Hungary's metal scene, while less internationally prominent, reveals surprising depth and resilience. "
        "From its emergence under communist censorship to its current manifestation in venues like the A38 Ship "
        "and festivals like Rockmaraton, Hungarian metal has carved out a distinctive identity. The Budapest "
        "metal infrastructure\u2014multiple dedicated venues, regular international touring stops, and domestic "
        "festivals\u2014suggests a scene with genuine economic substance even if precise figures remain elusive.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "The Uralic connection between Finland and Hungary remains a tantalizing but unproven hypothesis for "
        "their shared metal affinity. While linguistic isolation, historical resilience, and parallel cultural "
        "concepts like sisu and dacos\u00e1g provide suggestive threads, the evidence is insufficient to "
        "establish causation. What can be stated with greater confidence is that both nations have demonstrated "
        "that heavy metal, far from being economically marginal, can function as a driver of cultural tourism, "
        "festival economics, and national branding. Tuska's ongoing success and Hungary's persistent metal "
        "culture suggest that the economic story of heavy metal in these Uralic-language nations is still "
        "being written.",
        s["BodyText2"]
    ))

    story.append(Spacer(1, 1 * cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=MUTED, spaceAfter=12))

    # ══════════════════════════════════════════════════════════════
    # REFERENCES
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("References", s["SectionHead"]))

    refs = [
        "[1] Tuska Open Air Metal Festival. Official website. https://tuska.fi/en/",
        "[2] Tuska Open Air Metal Festival. Wikipedia. https://en.wikipedia.org/wiki/Tuska_Open_Air_Metal_Festival",
        "[3] \"Tuska 2023 set attendance record, 63,000 festival guests in Suvilahti, Helsinki.\" Tuska Official Communications, 2023.",
        "[4] \"Superstruct buys into Finnish metal festival Tuska.\" IQ Magazine, September 2021.",
        "[5] thisisFINLAND. \"53.2 per 100,000 people: Most heavy metal bands per capita in the world.\" finland.fi.",
        "[6] Nordic Perspective. \"The Lands of Heavy Metal: Most Metal Bands Per Capita (2025 World Map).\" nordicperspective.com.",
        "[7] Music Finland. \"Survey report: The value of the Finnish music industry is now over a billion euros.\" musicfinland.com, 2023.",
        "[8] Good News Finland. \"Finnish music industry is now worth over EUR 1 billion.\" goodnewsfinland.com, 2023.",
        "[9] Finnish Music Quarterly. \"Economy stalls \u2013 music export grows.\" fmq.fi.",
        "[10] Loudwire. \"11 Bands That Define Hungary's Metal Scene, Chosen by The Hellfreaks.\" loudwire.com.",
        "[11] A38 Ship. Official website. https://www.a38.hu/en",
        "[12] A38 (venue). Wikipedia. https://en.wikipedia.org/wiki/A38_(venue)",
        "[13] Sziget Festival. Wikipedia. https://en.wikipedia.org/wiki/Sziget_Festival",
        "[14] Hungary Today. \"Sziget Festival Draws 416,000 Visitors but Still Falls Short of Making Profit.\" hungarytoday.hu.",
        "[15] GKI Economic Research. \"If the Sziget Festival is Cancelled.\" gki.hu, 2025.",
        "[16] Van Budapest. \"Sziget Festival 2026 Saved | Complete Turnaround.\" vanbudapest.com, November 2025.",
        "[17] Rockmaraton Fesztiv\u00e1l. Concerts-Metal.com event listings.",
        "[18] FEZEN Festival. Concerts-Metal.com event listings.",
        "[19] Metal Travels. \"Hungary.\" metaltravels.com.",
        "[20] Wacken Open Air. Wikipedia. https://en.wikipedia.org/wiki/Wacken_Open_Air",
        "[21] Uralic languages. Wikipedia. https://en.wikipedia.org/wiki/Uralic_languages",
        "[22] Encyclopaedia Metallum: The Metal Archives. metal-archives.com.",
    ]
    for ref in refs:
        story.append(Paragraph(ref, s["RefStyle"]))

    story.append(Spacer(1, 1.5 * cm))
    story.append(HRFlowable(width="40%", thickness=0.5, color=ACCENT, spaceAfter=8))
    story.append(Paragraph(
        "\u00a9 2026 Zokura Foundation. This paper is provided for research and educational purposes. "
        "All claims marked with confidence percentages reflect the authors' assessment of data reliability "
        "at the time of writing.",
        s["TableNote"]
    ))

    doc.build(story, onFirstPage=footer_and_header, onLaterPages=footer_and_header)
    print(f"PDF generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_document()
